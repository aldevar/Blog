Accéder en webdav à son fichier Keepass
#######################################
:date: 2014-09-05 22:54
:author: alain
:category: Tech
:tags: apache, centos, keepass, ssl, webdav
:slug: acceder-en-webdav-a-son-fichier-keepass
:status: published

Keepass est un gestionnaire de mot de passe que j'utilise
personnellement et professionnellement. Il permet notamment de partager
un coffre fort entre plusieurs personne en offrant un support pour ftp
et http/webdav. Certains plugins ajoutent le support sftp et ftps.

Sur CentOS, apache est livré avec le module webdav. Ce n'est pas
forcement le cas de toutes les distributions.

La configuration utilisée est la suivante :

-  Un sous domaine créé pour contenir le fichier kdbx
-  une protection par mot de passe pour l'accès au fichier en lui même
   (anciennement .htaccess)
-  L'autorisation d'accéder au sous domaine en webdav
-  Et enfin, un mot de passe **ultra solide** pour le fichier kdbx qui
   peut contenir des données sensibles.

Dans mon cas, j'ai utilisé un sous domaine du type keepass.domain.tld et
le fichier est stocké en local sur le serveur sous /var/www/keepass/

::

    root# mkdir /var/www/keepass
    root# chown apache. /var/www/keepass
    root# chmod 770 /var/www/keepass
    root# vim /etc/httpd/conf.d/keepass.conf

Pour ne pas que le mot de passe passe en clair sur le net, nous allons
forcer l'utilisation de https

::

    <VirtualHost *:80>
     ServerName keepass.domain.tld
     ServerAdmin admin@domain.tld
     Redirect permanent / https://keepass.domain.tld/
     ErrorLog /var/log/httpd/keepass.err
     CustomLog /var/log/httpd/keepass.log combined
     DocumentRoot /var/www/keepass
    </VirtualHost>
    <VirtualHost *:443>
     SSLEngine on
     SSLCertificateFile /etc/pki/tls/certs/ca.crt
     SSLCertificateKeyFile /etc/pki/tls/private/ca.key
     ServerName keepass.domain.tld
     ServerAdmin admin@domain.tld
     ErrorLog /var/log/httpd/keepass.err
     CustomLog /var/log/httpd/keepass.log combined
     DocumentRoot /var/www/keepass
    <Directory "/var/www/keepass">
     DAV On
     SSLRequireSSL
     Options None
     AuthType Basic
     AuthName WebDAV
     AuthUserFile /etc/httpd/conf/.htpasswd
     <LimitExcept GET OPTIONS>
     Order allow,deny
     Allow from X.X.X.X #IP que vous autorisez, 'all' pour tout le monde
     Require valid-user
     </LimitExcept>
    </Directory>
    </VirtualHost>

Voici les étapes pour la création du fichier .htpasswd

::

    root# htpasswd -c /etc/httpd/conf/.htpasswd NomUtilisateur
    root# /etc/init.d/httpd restart

Il ne reste plus qu'à placer le fichier kdbx dans /var/www/keepass et
donner à apache les droits en écriture sur ce fichier.

Enfin, dans Keepass en ouvrant une url, le logiciel demande de fournir
l'URL et si besoin un couple login/mdp.

L'URL sera de type https://keepass.domain.tld/fichier.kdbx et le couple
login/mdp est celui créé lors de l’exécution de la commande htpasswd
