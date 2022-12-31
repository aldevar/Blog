Pydio : migration, upgrade, package [FR]
########################################
:date: 2016-05-27 23:02
:author: Aldevar
:category: Sysadmin
:slug: pydio-migration-upgrade-package-fr
:status: published

The article is also available `in
english <http://blog.devarieux.net/2016/05/pydio-migration-upgrade-package-en/>`__.

Sous ce titre peu clair se cache une opération de que je viens de mener
afin d'opérer 3 opérations sur une instance pydio. Pour mettre les
choses dans leur contexte, Pydio était installé via l'archive tar.gz,
sur un serveur CentOS 6 et la version utilisée était la 6.0.7.

L'objectif initial est de mettre à jour Pydio en version 6.4.
Malheureusement, la version de php nécessaire n'est pas présente dans
Centos 6 (sauf via des dépôts externe que je ne souhaitais pas
utiliser). La première étape est donc de monter une nouvelle VM Centos7
puis d'installer Pydio avec yum via le dépôt Pydio et d'importer
l'ancienne configuration dans cette nouvelle instance.

Installer Pydio via le gestionnaire de paquet permet de plus facilement
le mettre à jour et facilite également l'automation  pour un déploiement
automatique de Pydio ainsi que la gestion des plugins.

Ce sont ces étapes que je vais détailler ici.

Installation de mariadb et httpd

.. code:: sh

    yum install -y mariadb mariadb-server
    systemctl start mariadb.service
    systemctl enable mariadb.service
    mysql_secure_installation
    yum install httpd
    systemctl enable httpd.service
    systemctl start httpd.service

Installation des dépendances pour Pydio :

.. code:: 

    yum -y install php php-gd php-ldap php-pear php-xml php-xmlrpc php-mbstring curl php-mcrypt* php-mysql

Installation des dépots Pydio

.. code:: 

    wget https://download.pydio.com/pub/linux/centos/7/pydio-release-1-1.el7.centos.noarch.rpm

Si vous avez une licence pydio (gratuit jusqu'à 10 utilisateurs), vous
devez aussi récupérer le dépot enterprise

.. code:: 

    wget https://API_KEY:API_SECRET@download.pydio.com/auth/linux/centos/7/x86_64/pydio-enterprise-release-1-1.el7.centos.noarch.rpm

Avec API\_KEY et API\_SECRET  dans votre dashboard sur pydio.com, onglet
licence

.. code:: 

    rpm -ivh pydio-release-1-1.el7.centos.noarch.rpm
    rpm -ivh pydio-enterprise-release-1-1.el7.centos.noarch.rpm

Edition du dépot pour ajouter API\_KEY et API\_SECRET

.. code:: 

    vim /etc/yum.repos.d/pydio-enterprise.repo

Installation de pydio

.. code:: 

    yum update
    yum install pydio-enterprise

Modification du vhost par defaut :

.. code:: apache

    <VirtualHost nom.du.vhost:80>
    Alias / /usr/share/pydio/
    Alias /pydio_public /var/lib/pydio/public/

    <Directory /usr/share/pydio/>
    Options FollowSymLinks
    AllowOverride Limit FileInfo
    Require all granted
    php_value error_reporting 2
    php_value upload_max_filesize 100M
    php_value post_max_size 100M
    php_value output_buffering Off

    </Directory>

    <Directory /var/lib/pydio/public/>
    AllowOverride Limit FileInfo
    Require all granted
    php_value error_reporting 2
    </Directory>
    </VirtualHost>

Modification du charset dans /etc/pydio/bootstrap\_conf.php

.. code:: 

    define("AJXP_LOCALE", "fr_FR.UTF-8");

Création de la base de données:

.. code:: 

    mysql -u root -p
    create database pydio;
    create user pydio@localhost identified by 'mypassword';
    grant all privileges on pydio.* to pydio@localhost identified by 'mypassword';
    update mysql.users set Super_Priv='Y' where user like pydio;

La dernière commande sert à donner les super privilège à l'utilisateur
pydio afin qu'il puisse créer des triggers.

Vient ensuite l'installation des plugins pydio:

.. code:: 

    yum install pydio-plugin*

On termine par l'import de la base de données

.. code:: 

    mysql -u pydio -p pydio < mondumppydio.sql

Enfin, on lance l'interface de pydio et on passe via le wizard pour la
première configuration. Une fois terminé, on doit pouvoir se connecter
avec son compte habituel et retrouver tous ses fichiers.
