Bash : Script de sauvegarde
###########################
:date: 2014-07-24 11:14
:author: alain
:category: sysadmin
:tags: bash, centos, cron, ftp, gz, Linux, pydio, sauvegarde, script, tar
:slug: bash-script-de-sauvegarde
:status: published

On ne le dira jamais assez : **FAITES DES SAUVEGARDES!!!!!**
Ayant un petit serveur dédié sous CentOS, j'ai évidemment appliqué
cet adage à moi même. Je vous présente donc un script duquel vous pouvez
librement vous inspirer afin de l'adapter à votre environnement.
Ce script place quelques répertoires et quelques exports de base de
données dans un fichier tar.gz puis envoie ce fichier sur 2 serveurs FTP
(ceinture + bretelles) et enfin déplace l'archive dans un répertoire de
`pydio <http://pyd.io>`__ afin de pouvoir facilement récupérer le
fichier sur ma machine personnelle.

::

    #!/bin/bash
    #Fichier de Backup créé par Alain Devarieux
    # - créer un fichier tar.gz contenant plusieurs élements de l'arborescence
    # - Envoie ce fichier tar.gz sur un serveur FTP dédié au backup
    # - Dépose une copie du fichier tar.gz dans un repertoire local
    # - Ceinture ET Bretelles : Envoie le fichier tar.gz sur un 2nd serveur FTP
    logger -t backup "########## Debut de la sauvegarde ##########"
    # Nom du fichier de Backup
    backup_file="/sauv/backup-$(hostname)-$(date +%Y-%m-%d).tar.gz"
    #Variable : Premier Serveur FTP de Backup
    bckftp01="server01"
    bckftp01_user="user01"
    bckftp01_mdp="Enter password here"
    #Variable : Second Serveur de Backup
    bckftp02="server02"
    bckftp02_user="user02"
    bckftp02_mdp="Enter password here"
    #Varibales : Dossier de destination du tar.gz en local
    destdir="/var/www/html/pydio/data/files/"
    #Liste des dossiers à sauvegarder
    backup_list="/etc /var/www/html /sauv/sql /sauv/packagelist.txt"
    #Le dossier a exclure
    backup_exclude="/var/www/html/pydio/data"

    #Liste des paquets installés
    rpm -qa > /sauv/packagelist.txt

    #Dump des bases SQL
    #Base01
    if ! mysqldump -u userbase01 -pPassword base01 > /sauv/sql/base01.sql; then
    statusbase01="Warning : Erreur lors de l'export de la base Base01"
    else
    statusbase01="Succes de l'export de la base Base01"
    fi
    logger -t backup "$statusbase01"
    #Base02
    if ! mysqldump -u userbase02 -pPassword Base02 > /sauv/sql/base02.sql; then
    statusbase02="Warning : Erreur lors de l'export de la base Base02"
    else
    statusbase02="Succes de l'export de la base Base02"
    fi
    logger -t backup "$statusbase02"

    #Creation du tar
    #On commence par enregistrer la seconde de debut
    start=$(date '+%s')
    if ! tar czf $backup_file --exclude=$backup_exclude $backup_list; then
    statustar="echec de la commande tar" || exit 1
    else
    statustar="Succes creation fichier tar taille=$(stat -c%s $backup_file) duree=$((`date '+%s'` - $start))"
    fi
    #On log le resultat
    logger -t backup "$statustar"

    #Envoie vers le ftp01
    if ! lftp $bckftp01_user:$bckftp01_mdp@$bckftp01 -e "put $backup_file; exit"; then
    statusftp01="Echec de l'envoie FTP vers $bckftp01"
    else
    statusftp01="Succes de l'envoie FTP vers $bckftp01"
    fi
    #On log le resultat
    logger -t backup "$statusftp01"

    #Envoie vers le ftp02
    if ! lftp $bckftp02_user:$bckftp02_mdp@$bckftp02 -e "put $backup_file; exit"; then
    statusftp02="Echec de l'envoie FTP vers $bckftp02"
    else
    statusftp02="Succes de l'envoie FTP vers $bckftp02"
    fi
    #On log le resultat
    logger -t backup "$statusftp02"

    #Deplacer le fichier dans pydio
    if ! mv $backup_file $destdir; then
    statusmv="Warning : Echec du déplacement de $backup_file dans Pydio"
    else
    statusmv="Fichier $backup_file déplacé dans Pydio"
    fi
    logger -t backup "$statusmv"
    logger -t backup "########## Fin de la sauvegarde ##########"
    exit 0

Le script est planifié pour être lancé tous les dimanche à 5h00.
J'ai écris un 2nd script qui m'envoie un email avec les logs de la
sauvegarde afin que je puisse surveillé que tout c'est bien passé

::

    #!/bin/bash
    #Envoie d'un mail suite à l'execution du script de sauvegarde
    datejour=$(LC_ALL="en_EN.UTF-8" date "+%b %d")
    grep backup /var/log/messages |grep "$datejour" | mail -s "Backup du mois de $(date "+%B")" adresse@email.com adresse2@email.com

Petite explication sur le LC\_ALL="en\_EN.UTF-8"
Lorsque je tape

::

    date "+%b"

J'obtiens la version courte et francisée du mois. Par exemple, pour le
mois de juillet, je vais avoir comme retour *juil*. Hors syslog lui
écris dans le fichier */var/log/messages* en anglais. Ce qui donne pour
le mois de juillet : *jul* pour *july.* Pour pouvoir réussir mon grep
dans mon fichier de log, j'ai besoin de que la commande *date* me
retourne les informations en anglais également. C'est ce qui explique le
positionnement de cette variable en amont.

Ce second script est également placé dans un cron et est lancé a 5h15
tous les dimanches.
