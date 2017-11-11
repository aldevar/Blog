Pydio - migration, upgrade, package [EN]
########################################
:date: 2016-05-27 23:02
:author: alain
:category: Tech
:tags: centos, Linux, pydio
:slug: pydio-migration-upgrade-package-en
:status: published

Cet article est également disponible `en
français <http://blog.devarieux.net/2016/05/pydio-migration-upgrade-package-fr/>`__.

This unclear title reveals an operation i've just done to make 3 moves
in one. Pydio 6.0.7 was running on a CentOS 6 server, installed via the
tar.gz archive.

The primary goal was to upgrade Pydio to 6.4. Unfortunately, there was
dependcies problems with php. Pydio 6.4 needs php 5.4 and CentOS only
brings 5.3 (you can install php 5.4 via other repos but I didn't want
this). The first was to create a new Centos7 VM, then install Pydio on
it using yum and the Pydio repo and finally import the old config in the
brand new Pydio.

Installing Pydio through the package manager allows you to update it
easily and it also ease the automation for an autmatic deployement.
Also, the plugin management is facilitated.

These are the steps I'll describe here.

Install mariadb and httpd

.. code:: sh

    yum install -y mariadb mariadb-server
    systemctl start mariadb.service
    systemctl enable mariadb.service
    mysql_secure_installation
    yum install httpd
    systemctl enable httpd.service
    systemctl start httpd.service

Installing Pydio dependancies :

.. code:: 

    yum -y install php php-gd php-ldap php-pear php-xml php-xmlrpc php-mbstring curl php-mcrypt* php-mysql

Installing Pydio repositories

.. code:: 

    wget https://download.pydio.com/pub/linux/centos/7/pydio-release-1-1.el7.centos.noarch.rpm

If you own a licence (free up to 10 users), you can also have the
enterprise repo.

.. code:: 

    wget https://API_KEY:API_SECRET@download.pydio.com/auth/linux/centos/7/x86_64/pydio-enterprise-release-1-1.el7.centos.noarch.rpm

With API\_KEY and API\_SECRET  in your dashboard on pydio.com, licence
tab

.. code:: 

    rpm -ivh pydio-release-1-1.el7.centos.noarch.rpm
    rpm -ivh pydio-enterprise-release-1-1.el7.centos.noarch.rpm

Edit the repo file to add your API\_KEY and API\_SECRET

.. code:: 

    vim /etc/yum.repos.d/pydio-enterprise.repo

InstallPydio

.. code:: 

    yum update
    yum install pydio-enterprise

I use to modify the default vhost file /etc/httpd/conf.d/pydio.conf

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

Customize the charset in /etc/pydio/bootstrap\_conf.php

.. code:: 

    define("AJXP_LOCALE", "fr_FR.UTF-8");

Create the database:

.. code:: 

    mysql -u root -p
    create database pydio;
    create user pydio@localhost identified by 'mypassword';
    grant all privileges on pydio.* to pydio@localhost identified by 'mypassword';
    use mysql
    update mysql.users set Super_Priv='Y' where user like pydio;

The last command gives the Super Privileges to the pydio user for it to
be able to create triggers.

Install the Pydio plugins;

.. code:: 

    yum install pydio-plugin*

The last step is to import your old pydio database in your brand new one

.. code:: 

    mysql -u pydio -p pydio < mondumppydio.sql

Finally, you can go to the pydio page and go through the First Run
Wizard. Once done, you should be able to connect with your account and
find all your files.
