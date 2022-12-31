Mise en oeuvre de Fail2Ban pour Owncloud/Ldap
#############################################
:date: 2013-11-27 20:30
:author: Aldevar
:category: Sysadmin
:slug: mise-en-oeuvre-de-fail2ban-pour-owncloudldap
:status: published

Si vous stockez des données personnelles ou à caractères sensibles sur
votre serveur owncloud, vous souhaitez sans doute que les malandrins
s'aventurant à tester vos couples *Login / Mot de passe* par brutforce
soient éjectés de votre serveur après un certains nombre de tentatives
infructueuses.

Fail2Ban fera le travail pour vous, mais pour cela, il a besoin que les
échecs de connexions soient logués, ce qu'Owncloud ne fait
malheureusement pas. Il faut donc, avant de mettre en oeuvre Fail2Ban,
procéder à quelques modifications dans le code d'Owncloud.

Vous trouverez beaucoup d'article vous expliquant comment faire cela
avec une connexion classique via la base de donnée d'Owncloud, par
exemple
`ici <http://www.dataparadis.net/osp/gnu-linux-server/cloud-server/owncloud-and-fail2ban-update/>`__.
Dans cet article, nous verrons plutôt comment régler le problème
lorsqu'on utilise une authentification via un serveur Ldap.

Préparer le terrain
-------------------

Afin d'assurer une cohérence dans l'écriture des logs, il faut que la
timezone soit correctement configurée sur le serveur. Vous pouvez faire
cela à l'aide de la commande :

::

    [root@server1]# tzselect

On va ensuite, créer le fichier qui servira à loguer les échecs de
connexions

::

    [root@server1]# touch /var/log/owncloud-fail.log
    [root@server1]# chmod 660 /var/log/owncloud-fail.log
    [root@server1]# chown root.apache /var/log/owncloud-fail.log

 

Modification du backend d'Owncloud
----------------------------------

Dans le fichier lib/user/database.php, ligne 202. Dans la fonction
checkPassword, entre le **else** et le **return false**, insérez le code
suivant :

::

    $today = new DateTime();
    date_timezone_set($today, timezone_open('Europe/Paris'));
    $IPClient=$_SERVER['REMOTE_ADDR'];
    $logAuth=fopen('/var/log/owncloud-fail.log', 'a+');
    fputs($logAuth, date_format($today, 'Y/m/d H:i:s') . " Password check failed for: \t" . $IPClient . "\n");
    fclose($logAuth);

Dans le fichier apps/user\_ldap/user\_ldap.php, ligne 75. Dans la
fonction checkPassword, entre le  **if(count($ldap\_users) < 1)
{** et le  **return false;** insérez le code suivant :

::

    if($uid!="admin") {
    date_default_timezone_set('Europe/Paris');
    $today = date("Y/m/d H:i:s");
    $IPClient=$_SERVER['REMOTE_ADDR'];
    $logAuth=fopen('/var/log/owncloud-fail.log', 'a+');
    fputs($logAuth, $today . " Password check failed for: \t" . $IPClient . "\n");
    fclose($logAuth);

Puis, en dessous du return false, fermez l'instruction if en ajoutant un

::

    }

**Explication du code :**

Il y a un utilisateur qui est inscrit en base de donnée et qui n'est pas
dans le ldap, c'est l'admin d'owncloud. Afin ne ne pas loguer une
connexion de l'utilisateur 'admin' en tant qu'erreur de connexion, il
est nécessaire de vérifier que que c'est pas cet utilisateur qui se
connecte. D'où le **if($uid!="admin"){}**. Veillez à modifier cette
valeur suivant la votre.

La variable **$ldap\_users** est un tableau contenant la liste des
utilisateurs qui correspondent à la valeur saisie dans le login. Si
cette table est vide, alors il y aura un échec de connexion logué.

Le dernier ajout à faire se trouve un petit peu plus bas dans ce
fichier, ligne 97, juste en dessous
de \ **if(!$this->areCredentialsValid($dn, $password)) {** et au dessus
de **return false;**\ ajoutez le code suivant :

::

    date_default_timezone_set('Europe/Paris');
    $today = date("Y/m/d H:i:s");
    $IPClient=$_SERVER['REMOTE_ADDR'];
    $logAuth=fopen('/var/log/owncloud-fail.log', 'a+');
    fputs($logAuth, $today . " Password check failed for: \t" . $IPClient . "\n");
    fclose($logAuth);

 

Configuration de Fail2Ban
-------------------------

Dans votre fichier /etc/fail2ban/jail.conf (ou équivalent suivant votre
distribution) :

::

    [Owncloud]
    enabled  = true
    port     = http,https
    filter   = owncloud
    logpath  = /var/log/owncloud-fail.log
    maxretry = 5

Et enfin, le fichier de filtre /etc/fail2ban/filter.d/owncloud.conf

::

    # /etc/fail2ban/filter.d/owncloud.conf
    #
    # Fail2Ban configuration file
    # Owncloud
    #

    [Definition]
    # Option: failregex
    failregex = <HOST>$

Relancez fail2ban et le tour est joué.

 
