#!/bin/bash

echo "PH-DEPLOY"

## VARIABLES
IPARAPHEUR=$1
URL=$(echo "$2" | /bin/sed -r 's/\<secure-//g')
FOLDER=$PWD

IF_FILE_EXIST ()
{
if [ ! -f $1 ]; then
  echo "Le fichier $1 n'existe pas"
  echo "FIN DU SCRIPT"
  exit 1
else
  echo "$1 => OK"
fi
}

IF_DIR_EXIST ()
{
if [ ! -d $1 ]; then
  echo "Le dossier $1 n'existe pas"
  echo "FIN DU SCRIPT"
  exit 1
else
  echo "$1 => OK"
fi
}

## Check les éléments
CHECK (){
  echo -e "\n- CHECK DES DOSSIERS ET FICHIERS"
  IF_FILE_EXIST *.tar.gz
  IF_DIR_EXIST $IPARAPHEUR
  IF_DIR_EXIST $IPARAPHEUR/amps
  IF_FILE_EXIST /etc/init.d/alfresco
  IF_FILE_EXIST $IPARAPHEUR/iparaph-updateAMP.sh
  IF_FILE_EXIST $IPARAPHEUR/tomcat/webapps/iparapheur.war
  IF_FILE_EXIST $IPARAPHEUR/tomcat/webapps/alfresco/WEB-INF/wsdl/iparapheur.wsdl
  IF_FILE_EXIST $IPARAPHEUR/custom-wsdl.sh
}

## Décompresser les sources iparapheur-vXXX.tar.gz et confs.tar.gz
ARCHIVE(){
  echo -e "- DECOMPRESSION DE L'ARCHIVE"
  tar xzf *.tar.gz
  cd iParapheur* || exit
  IF_FILE_EXIST confs.tar.gz
  mkdir dir_confs
  cd dir_confs || exit
  tar xzf ../confs.tar.gz
  IF_DIR_EXIST confs*
}

## Arrêt de l'appliction alfresco
ALFRESCO_STOP (){
  echo -e "- ARRET DE L'APPLICATION"
  /etc/init.d/alfresco stop > /dev/null 2>&1
  kill $(ps aux | grep '/opt/iParapheur/java/bin/java' | awk '{print $2}') > /dev/null 2>&1
  kill $(ps aux | grep '/opt/jre/bin/java' | awk '{print $2}') > /dev/null 2>&1
  if [ -f $FILE ]; then
     rm $FILE
  fi
}

## Copier les scripts iparaph-update et deployWar
COPY_SCRIPT(){
  echo -e "- COPIE DES SCRIPTS"
  cd confs* || exit
  cp iparaph-updateAMP.sh $IPARAPHEUR
  cp deployWarIparapheur.sh $IPARAPHEUR
}

## Remplacement de l'AMPS
DEPLOY_AMPS(){
  echo -e "- DEPLOIEMENT DE L'AMP"
  rm $IPARAPHEUR/amps/*
  cp $FOLDER/iparapheur*/*.amp $IPARAPHEUR/amps
  bash $IPARAPHEUR/iparaph-updateAMP.sh
}

## Lancer le script custom avec l’url
CUSTOM_URL(){
  echo -e "- PERSONNALISATION DU WSDL"
  cd $IPARAPHEUR || exit
  bash $IPARAPHEUR/custom-wsdl.sh $URL
}

## Copier le WAR et deploiement
DEPLOY_WAR(){
  echo -e "- DEPLOIEMENT DU WAR"
  cd $FOLDER/iParapheur* || exit
  cp *.war $IPARAPHEUR/tomcat/webapps/iparapheur.war
  bash $IPARAPHEUR/deployWarIparapheur.sh
}

## alfresco start
ALFRESCO_START (){
  echo -e "- DEMARRAGE DE L'APPLICATION"
  sleep 10
  /etc/init.d/alfresco start && tail -f $IPARAPHEUR/tomcat/logs/catalina.out | sed '/^INFOS: Server startup in/ q'
  echo "FIN DU SCRIPT"
  exit 0
}

CHECK
ARCHIVE
ALFRESCO_STOP
COPY_SCRIPT
DEPLOY_AMPS
CUSTOM_URL
DEPLOY_WAR
ALFRESCO_START