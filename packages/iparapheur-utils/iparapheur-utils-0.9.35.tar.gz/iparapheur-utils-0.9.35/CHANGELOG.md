# Change Log
Tous les changements notables sur ce projet seront documentés dans ce fichier.

Ce format est basé sur [Keep a Changelog](http://keepachangelog.com/)
et ce projet adhère au [Semantic Versioning](http://semver.org/).

## [0.9.35] - 2020-12-02

### Evolution
- `ph-check` : Detection version 4.7.6

## [0.9.34] - 2020-10-26

### Correction
- `ph-recupArchives` : Un caractère n'était pas reconnu

## [0.9.33] - 2020-10-24

### Evolution
- `ph-check` : Ajout check multitenant, début frugalité d'output (mode verbose)

## [0.9.32] - 2020-10-01

### Correction
- `ph-check` : regression sur check https. desactivation controle du certificat en attendant un vrai correctif

## [0.9.31] - 2020-09-28

### Correction
- `ph-recuparchives` : l'argument skipped n'était pas pris en compte et provoquait un boucle infinie en 4.7

## [0.9.30] - 2020-09-28

### Evolution
- `ph-check` : detection expiration certificats HTTPS pour NginX, limitation libgs max à 9.27
- `ph-check` : Ajout detection parametres de configuration pour 4.6 et 4.7
- `ph-check` : montre sa version dans le header

## [0.9.29] - 2020-09-07

### Evolution
- `ph-check` : FIX regression pour versions inferieures à 4.7

## [0.9.28] - 2020-09-06

### Evolution
- `ph-check` : Ajout check alfresco.xml (url pes-viewer)

## [0.9.27] - 2020-09-02

### Evolution
- `ph-check` : Ajout check permissions des repertoires temporaires pes-viewer

## [0.9.26] - 2020-08-22

### Evolution
- `ph-check` : amélioration sur check side-services, plus besoin de 'deployWarIparapheur.sh'
- `ph-check` : Ajout scan vulnerabilité CVE-2020-1938 (AJP)

## [0.9.25] - 2020-08-14

### Evolution
- `ph-check` : Detection version 4.7.5, et dependances manquantes de 'libriciel-pdf'

## [0.9.24] - 2020-08-13

### Evolution
- `ph-check` : Detection Debian8 en fin de vie (obsolete), et 'killall' necessaire

## [0.9.23] - 2020-07-19

### Evolution
- `ph-check` : Detection version 4.7.4, MCA WS configuration, accès à nexus et sentry

## [0.9.22] - 2020-07-16

### Correction
- `ph-check` : Better handle unusual mysql port number

## [0.9.21] - 2020-05-22

### Correction
- `ph-check` : Fix iparapheur-utils rule in crontab

## [0.9.20] - 2020-05-19

### Evolution
- `ph-check` : Detection version 4.7.3

## [0.9.19] - 2020-05-03

### Evolution
- `ph-check` : Support basique des specificités de i-Parapheur v4.7

## [0.9.18] - 2020-03-09

### Corrections
- `ph-check` : fix sur detections `recup_crl_nginx.sh` en cas de HTTPS
- `ph-rename` : L'URL à modifier était mal définie. Maintenant, on la renseigne dans la commande.

## [0.9.17] - 2020-03-05

### Evolution
- `ph-check` : Affichage du différentiel entre la crontab du serveur et la crontab des sources selon la version du parapheur

## [0.9.16] - 2020-03-02

### Ajouts
- `ph-patch` : Ajout de la fonction ph-patch qui déploie le patch depuis un dossier contenant son archive

### Evolutions
- `ph-check` : meilleure detection de la version de i-Parapheur
- `ph-count_files` : On ne différencie plus les MONO et MULTI tenant. La requête sur les dossiers affiche les bureau et banette.

### Corrections
- `ph-recupArchives` : La récupération d'une archive se fait dans un try/except pour ne pas couper le script en cas d'anomalie.
- `ph-ipclean` : La procédure de d'optimisation des transactions ne marchait pas. 

## [0.9.15] - 2019-09-23

### Ajouts
- `ph-pushdoc` : Contribution Ifremer : Nouveau paramètre `limite` pour définir une date limite de traitement des dossiers 

## [0.9.14] - 2019-07-15

### Corrections
- `ph-recupArchives` : gestion d'un caractère spécial

## [0.9.13] - 2019-07-09

### Corrections
- `ph-recupArchives` : compatibilite ascendante en cas de paramètre `use_only_print_pdfs` manquant

## [0.9.12] - 2019-06-12

### Ajouts
- Modification de la fonction `ph-pushdoc` : les caractères "=" et "'" sont accepté dans les métadonnées

## [0.9.11] - 2019-06-04

### Ajouts
- Ajout de la fonction `reset_admin_password`: dans le cas où le mot de passe de l'admin est perdu, la fonction réinitialise le mdp à "admin".

## [0.9.10] - 2019-06-03

### Ajouts
- Pour la fonction `export`: Le fichier export.cfg permet de choisir les objets à importer. Par défaut il les importe tous.

## [0.9.9] - 2019-05-28

### Ajouts
- Nouveau paramètre pour la fonction `ph-recupArchives` : `use_only_print_pdfs` permettant de récupérer uniquement les PDF d'impression

### Modifications
- La fonction `count-files` prend en compte les parapheur multitenant.
- `ldapsearch`: la requête qui liste les utilisateurs est lancée sans caractère d'échappement.

## [0.9.8] - 2019-04-24

### Corrections
- Coquille dans le core.py pour count_files
- import_data.py: modifiction des conditions d'importation de groupe

## [0.9.7] - 2019-04-17

### Ajouts
- Ajout de la fonction `count_files` qui permet d'afficher un tableau de tous les dossiers par bureaux.

## [0.9.6] - 2019-03-12

### Ajouts
- Ajout de la fonction `ldapsearch` qui génère vérifie la présence du fichier conf, les propriétés, la requêtes LDAP et 
la liste des utilisateurs retournés.

## [0.9.5] - 2019-02-25

### Ajouts
- Ajout de la fonction `ipclean` qui génère les index (arrêt de l'application, supprime les noeuds, lance la procédure 
docleanIPtranstion.sql, supprime 2 dossiers du alf_data, relance l'application)

## [0.9.4] - 2019-02-22

### Corrections
- Mise à jour du certificat de connexion aux webservices

## [0.9.3] - 2019-01-28

### Corrections
- Meilleure detection de la version JDK dans  `ph-check`

## [0.9.2] - 2018-11-12

### Corrections
- Gestion des cas d'erreur HTTP avec la fonction `ph-recupArchives`

## [0.9.1] - 2018-10-12

### Corrections
- Message d'erreur lors de l'appel à `ph-rename` en cas de propriété manquante
- Mauvais chemin d'execution lors de l'appel à la fonction `ph-pushdoc`

## [0.9.0] - 2018-10-11

### Évolutions

- Ajout d'une fonction de traitement pour le connecteur générique pushdoc `ph-pushdoc`

## [0.8.0] - 2018-10-02

### Évolutions

- Ajout de la fonction de suppression d'utilisateurs ldap `ph-removeldap`

## [0.7.1] - 2018-09-26

### Corrections

- Faux négatif sur l'environnement Ubuntu 18.04
- Ajout de vérifications sur la date du dossier validca
- Ajout de vérifications sur la présence de la bonne URL dans le fichier iparapheur.wsdl

## [0.7.0] - 2018-09-26

### Évolutions

- Ajout de la fonction de changement de nom `ph-rename`

## [0.6.2] - 2018-09-18

### Corrections

- Problème d'import d'utilisateur n'ayant pas de nom, prénom ou mail

## [0.6.1] - 2018-08-30

### Corrections

- Problème de récupération d'archives quand la date est définie dans le filtre

## [0.6.0] - 2018-07-13

### Évolutions

- Mise à jour de la vérification sur la version du JDK
- Nouvelles vérifications sur Redis, Ubuntu 18 et le Connecteur Pastell

## [0.5.2] - 2018-02-23

### Évolutions

- Adaptation du script de suppression des archives pour déplacement immédiat vers conrentstore.deleted

### Corrections

- Corrections mineures dans le script de vérification ph-check

## [0.5.1] - 2017-12-05

### Ajouts

- Cas spécifique de contournement d'un proxy

### Corrections

- Problème de détection de version NginX sur Ubuntu

## [0.5.0] - 2017-11-24

### Évolutions

- Dépréciation de la librairie 'progressbar2' pour 'progress'
- Suppression de la librairie 'python-magic' pour support Windows

### Corrections

- Problèmes d'accents sur la récupération d'archives

## [0.4.1] - 2017-07-07

### Corrections

- Mauvaise dépendance `progressbar` au lieu de `progressbar2`

## [0.4.0] - 2017-07-07

### Ajouts

- Fonction d'import (`ph-import`) depuis un dossier local
- Fonction  d'export (`ph-export`) vers un dossier local

## [0.3.3] - 2017-06-05

### Ajouts

- La fonction `recupArchives` ne récupère plus toutes les archives à 
chaque fois mais se base sur le paramètre `waitingdays` pour filtrer.

## [0.3.2] - 2017-05-31

### Ajouts

- Sortie d'une version beta `iparapheur-utils.beta` installable 
via `pip install iparapheur-utils.beta`. Attention, avant d'installer 
cette version, il faut enlever l'ancienne `pip uninstall iparapheur-utils`

### Corrections

- La fonction recupArchives ne fonctionnait pas sans fichier de configuration

## [0.3.1] - 2017-05-29

### Corrections

- Le module `requests` a une version minimale en 2.16 pour suppression des warnings

## [0.3.0] - 2017-05-26

### Ajouts

- Changelog
- Génération d'une documentation à partir du README

### Evolutions

- Respect plus strict du versionning sémantique

### Suppressions

- Logs SSL3 sur certaines anciennes versions de python

