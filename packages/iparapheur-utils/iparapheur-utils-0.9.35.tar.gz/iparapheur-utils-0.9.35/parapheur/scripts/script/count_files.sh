#!/bin/bash


PROP_PATH="/opt/iParapheur/tomcat/shared/classes/alfresco-global.properties"

if [ -f "$PROP_PATH" ]
then
  while IFS='=' read -r key value
  do
    key=$(echo $key | tr '.' '_')
    eval "${key}"=\${"value"} 2> /dev/null
  done < "$PROP_PATH"
else
  echo "- LE FICHIER DE PROPRIETE $1 EST INTROUVABLE : FIN DU SCRIPT"
  exit 1
fi


## -- Des variables
alfresco="/etc/init.d/alfresco"
PATH_IP="/opt/iParapheur/tomcat/shared/classes/"
db_url=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $1 }'`
db_port=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $2 }'`
DATA_PATH="$dir_root/contentstore/"
if [ -z "$db_port" ]
then
  db_port="3306"
fi
mysql="-h $db_url -P $db_port -u $db_username -p$db_password"

## -- Quelques test
IF_FILE_EXIST ()
{
if [ ! -f $1 ]; then
  echo "- LE DOSSIER $1 N'EXISTE PAS"
  echo " -FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


IF_DIR_EXIST ()
{
if [ ! -d $1 ]; then
  echo "LE DOSSIER $1 N'EXISE PAS"
  echo "- FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}

TEST_SERVICE ()
{
if ! which $1 >/dev/null; then
  echo "- LE SERVICE $1 N EXISTE PAS"
  echo "FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


## -- ON LANCE LES TESTS
echo -e "\n ** PREREQUIS **\n"
IF_FILE_EXIST $alfresco
IF_DIR_EXIST $PATH_IP
IF_FILE_EXIST $PROP_PATH
TEST_SERVICE "mysql"
IF_DIR_EXIST $DATA_PATH


mysql $mysql -e 'exit' $db_name
if [ $? -ne 0 ]; then
    echo "- CONNEXION A LA BASE DE DONNEES IMPOSSIBLE"
    echo "- FIN DU SCRIPT"
    exit 1
fi
echo -e "\n- CONNEXION A LA BASE DE DONNEES => OK\n"


## Procédures stockées
{
  echo "DELIMITER //";
  echo "CREATE PROCEDURE count_files_by_tenant()";
  echo "bEGIN";
  echo "SELECT alf_store.identifier, bureau.qname_localname AS Bureau_Name, banette.qname_localname AS Banette_Name, COUNT(dossier.child_node_id) AS Dossiers_Count" ;
  echo "FROM alf_child_assoc AS bureau" ;
  echo "JOIN alf_child_assoc AS banette ON bureau.child_node_id = banette.parent_node_id" ;
  echo "JOIN alf_child_assoc AS dossier ON dossier.parent_node_id = banette.child_node_id" ;
  echo "JOIN alf_node on alf_node.id=dossier.child_node_id" ;
  echo "JOIN alf_store on alf_store.id=alf_node.store_id" ;
  echo "WHERE bureau.parent_node_id in (SELECT child_node_id FROM alf_child_assoc where child_node_name='parapheurs')" ;
  echo "AND banette.qname_localname IN ('retournes', 'a-archiver', 'a-traiter', 'en-preparation', 'en-retard', 'dossiers-delegues')" ;
  echo "GROUP BY bureau.qname_localname, banette.qname_localname" ;
  echo "HAVING Dossiers_Count >= 0" ;
  echo "order by identifier, Bureau_Name, Banette_Name ;" ;
  echo "END;" ;
  echo "CREATE PROCEDURE count_files_archives_by_tenant()" ;
  echo "bEGIN" ;
  echo "SELECT identifier, COUNT(*) " ;
  echo "FROM alf_node AS n, alf_qname AS q, alf_store AS s " ;
  echo "WHERE n.type_qname_id=q.id " ;
  echo "AND n.store_id=s.id " ;
  echo "AND q.local_name='archive' " ;
  echo "AND s.protocol='workspace' " ;
  echo "AND n.node_deleted=0 GROUP BY store_id;" ;
  echo "END;" ;
  echo "//" ;
  echo "DELIMITER ;"
} > myproc.sql

## -- ON injecte la procédure
echo 'DROP PROCEDURE count_files'
mysql $mysql -e 'DROP PROCEDURE IF EXISTS count_files;' $db_name
echo 'DROP count_files_by_tenant'
mysql $mysql -e 'DROP PROCEDURE IF EXISTS count_files_by_tenant;' $db_name
echo 'DROP count_files_archives_by_tenant'
mysql $mysql -e 'DROP PROCEDURE IF EXISTS count_files_archives_by_tenant;' $db_name
echo 'CREATE PROCEDURE'
mysql $mysql $db_name < myproc.sql >/dev/null 2>&1


## -- On lance les procédures stockées s
mysql $mysql -e 'CALL count_files_by_tenant();' $db_name
mysql $mysql -e 'CALL count_files_archives_by_tenant();' $db_name

exit 0