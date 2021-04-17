Owncloud et fail2ban derrière un reverse proxy
##############################################
:date: 2013-12-05 18:32
:author: alain
:category: sysadmin
:tags: fail2ban, owncloud, proxy, remote log, reverse, reverse proxy, rsyslog, syslog
:slug: owncloud-et-fail2ban-derriere-un-reverse-proxy
:status: published

Dans le `dernier
article </mise-en-oeuvre-de-fail2ban-pour-owncloudldap.html>`_,
j'expliquais comment mettre en place fail2ban sur son serveur pour
protéger son instance Owncloud lorsqu'elle est connectée sur un serveur
Ldap.

En général, lorsqu'on utilise un serveur Ldap pour l'authentification,
c'est qu'on se trouve en entreprise et les choses ne sont pas alors pas
si simple. Par exemple, dans mon cas, le serveur owncloud ne se trouve
pas directement en frontale sur le net mais est caché derrière un
reverse proxy.

Du coup, le serveur owncloud ne voit qu'une seule IP : celle du reverse
proxy. La mise en place de fail2ban sur ce serveur poserait alors un
gros problème car cela reviendrait à faire bannir l'IP du reverse proxy
et interdire tout accès à owncloud depuis l’extérieur. Dans cet article,
nous allons donc voir comment corriger ce problème à l'aide de syslog.

Sur le serveur Owncloud
-----------------------

Modification d'owncloud
~~~~~~~~~~~~~~~~~~~~~~~

Configuration du serveur owncloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Afin d’assurer une cohérence dans l’écriture des logs, il faut que la
timezone soit correctement configurée sur le serveur.

::

    [root@owncloud]# tzselect

Création du fichier qui recevra les écritures des logs des échecs de
connexions :

::

    [root@owncloud]# touch /var/log/owncloud-fail.log
    [root@owncloud]# chmod 660 /var/log/owncloud-fail.log
    [root@owncloud]# chown root.apache /var/log/owncloud-fail.log


Modification du backend d'owncloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dans le fichier */var/www/html/owncloud/lib/user/database.php*, ligne
202. Dans la fonction **checkPassword**, entre le else et le return
false, insérez le code suivant :

::

    $headers = apache_request_headers();
    $real_client_ip = $headers["X-Forwarded-for"];
    $IPClient=$_SERVER['REMOTE_ADDR'];
    openlog("owncloud", LOG_PID, LOG_LOCAL0);
    syslog(LOG_WARNING, "Password check failed for: " . "$IPClient" . " " . "$real_client_ip");
    closelog();

Dans le fichier */var/www/html/owncloud/apps/user\_ldap/user\_ldap.php*,
ligne 75. Dans la fonction **checkPassword**, entre le
if(count($ldap\_users) < 1) { et le return false; insérez le code
suivant :

::

    if($uid!="admin") {
    $headers = apache_request_headers();
    $real_client_ip = $headers["X-Forwarded-For"];
    $IPClient=$_SERVER['REMOTE_ADDR'];
    openlog("owncloud", LOG_PID, LOG_LOCAL0);
    syslog(LOG_WARNING, "Password check failed for: " . "$IPClient" . " " . "$real_client_ip");
    closelog();

Puis, en dessous du return false, fermez l’instruction if en ajoutant un

``}``

Toujours dans le même fichier, ligne 97, juste après
**if(!$this→areCredentialsValid($dn, $password)) {** Et au-dessus du
**return false;** correspondant ajouter le code suivant :

::

    $headers = apache_request_headers();
    $real_client_ip = $headers["X-Forwarded-For"];
    $IPClient=$_SERVER['REMOTE_ADDR'];
    openlog("owncloud", LOG_PID, LOG_LOCAL0);
    syslog(LOG_WARNING, "Password check failed for: " . "$IPClient" . " " . "$real_client_ip");
    closelog();

Explication du code
^^^^^^^^^^^^^^^^^^^

::

    $headers = apache_request_headers()

Récupère l’entête des requêtes http venant du reverse proxy sous forme
de tableau

::

    $real_client_ip = $headers[ "X-forwarded-For "] ;

Récupère l’adresse IP réelle du client dans le tableau $headers

::

    $IPClient = $_SERVER[‘REMOTE_ADDR’] ;

Récupère l’adresse IP du client. Si le client vient de l’extérieur du
SIB, cette IP sera celle du reverse proxy.

Openlog, Syslog et closelog sont les fonctions PHP pour écrire les
échecs de connexions en passant par syslog.

Configuration de rsyslog
~~~~~~~~~~~~~~~~~~~~~~~~

Log locaux
^^^^^^^^^^

Pour loguer les échecs de connexion venant d’owncloud, il faut dire à
rsyslog ce qu’il doit faire avec ces entrées. On crée pour cela un
fichier supplémentaire */etc/rsyslog.d/owncloud.conf* contenant une
seule ligne :

::

    local0.*   /var/log/owncloud-fail.log

Ainsi, tous les messages reçus sur l’interface LOCAL0 de rsyslog seront
redirigé vers le fichier */var/log/owncloud-fail.log*

Log distant
^^^^^^^^^^^

Le serveur owncloud ne peut pas bannir lui-même les IP car il ne voit
que l’IP du reverse proxy pour toutes les connexions venant de
l’extérieur. Il faut donc remonter les logs des échecs de connexions
vers le reverse proxy qui bannira lui-même les IP. On crée pour cela un
nouveau fichier de configuration de rsyslog :
*/etc/rsyslog.d/fail2ban.conf*.

::

    local0.*        @nomdevotrereverse.proxy:514

Ceci a pour effet d’envoyer tous les messages reçu sur l’interface
LOCAL0 de rsyslog vers le service syslog du reverse proxy.

Prise en compte des modifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On redémarre le service rsyslog

::

    /etc/init.d/rsyslog restart

Afin de voir si les modifications effectuées n’ont pas générée d’erreur
:

::

    grep rsyslog /var/log/messages

Sur le reverse proxy
--------------------

Configuration de syslog
~~~~~~~~~~~~~~~~~~~~~~~

Par défaut, le service syslog n’écoute pas le réseau et ne peut donc pas
recevoir de logs distants. Pour corriger cela, on édite le fichier
*/etc/sysconfig/syslog*. Modification de la ligne SYSLOGD\_OPTIONS en
ajoutant l’option –r

::

    SYSLOGD_OPTIONS="-r -m 0"

Puis, on relance le service afin d’activer l’écoute réseau :

::

    /etc/init.d/syslog restart

Configuration de fail2ban
~~~~~~~~~~~~~~~~~~~~~~~~~

Installation
^^^^^^^^^^^^

L’installation se fait simplement par le gestionnaire de paquet :

::

    yum install fail2ban

Configuration de la prison
^^^^^^^^^^^^^^^^^^^^^^^^^^

On édite pour cela le fichier */etc/fail2ban/jail.conf* et on y ajoute
les lignes suivantes :

::

    [owncloud]
    enabled = true
    port = https
    filter = owncloud
    action = iptables[name=httpd,port=https,protocal=all]
    logpath = /var/log/messages
    maxretry = 5

Toutes les autres prisons peuvent être positionnées sur enabled = false
puisque nous n’en avons pas besoin ici.

Création du filtre
^^^^^^^^^^^^^^^^^^

Dans la configuration du jail, nous avons dit à fail2ban d’utiliser le
filtre owncloud, nous allons maintenant créer le filtre :

Création du fichier */etc/fail2ban/filter.d/owncloud.conf*

::

    [Definition]
    failregex = Password check failed for: ip.du.reverse.proxy <HOST>
    ignoreregex =

Puisque nous ne souhaitons que bannir les IP externes, nous ne
récupérons que les lignes qui contiennent l’IP du reverse proxy ET l’IP
réelle du client. Le ligne ignoreregex n’est pas nécessaire mais il faut
tout de même qu’elle soit présente afin que fail2ban valide la
configuration.

Démarrage du service
^^^^^^^^^^^^^^^^^^^^

On lance le service fail2ban :

::

    /etc/init.d/fail2ban start

Si le lancement tombe en échec, c’est qu’il y a un problème de
configuration. Pour repérer ce problème, il faut lancer le daemon à la
main :

::

    fail2ban-server

Puis on lance un reload du client qui va tester pour nous la
configuration

::

    fail2ban-client reload

S’il y a une erreur, cette commande nous le dira.

Test de la configuration
^^^^^^^^^^^^^^^^^^^^^^^^

Afin de tester la valididité de la regex, fail2ban propose l’outil
fail2ban-regex. Créer pour cela quelques échecs de connexion et tester
avec la commande :

::

    fail2ban-regex /var/log/messages /etc/fail2ban/filter.d/owncloud.conf

::

    Running tests
    =============
    Use regex file : /etc/fail2ban/filter.d/owncloud.conf
    Use log file   : /var/log/messages

    Results 
    ======= 
    Failregex 
    |- Regular expressions: 
    |  [1] Password check failed for: ip.du.reverse.proxy <HOST>
    |
    `- Number of matches:
       [1] 6 match(es)

    Ignoreregex
    |- Regular expressions:
    |
    `- Number of matches:

    Summary
    =======

    Addresses found:
    [1]
        X.X.X.X (Thu Dec 05 10:02:11 2013)
        X.X.X.X (Thu Dec 05 10:05:24 2013)
        X.X.X.X (Thu Dec 05 10:05:34 2013)
        X.X.X.X (Thu Dec 05 10:05:42 2013)
        X.X.X.X (Thu Dec 05 10:05:47 2013)
        X.X.X.X (Thu Dec 05 10:05:53 2013)

    Date template hits:
    18154 hit(s): MONTH Day Hour:Minute:Second

    Success, the total number of match is 6
    However, look at the above section 'Running tests' which could contain important info


