Pas à pas - monter un cluster Galera Mariadb
############################################
:date: 2016-06-20 22:40
:author: alain
:category: sysadmin
:tags: bdd, cluster, galera, Linux, mariadb
:slug: monter-cluster-galera-mariadb
:status: published

Lorsque je me suis mis dans l'idée de monter un cluster Galera Mariadb
pour remplacer notre cluster Mysql, je pensais trouver facilement de la
documentation en ligne. On trouve en effet beaucoup d'articles de blogs
expliquant comment créer son cluster Galera malheureusement cette techno
évolue vite et les articles sont rarement à jour.

La documentation qu'on peut trouver sur le site de mariadb est également
assez succinct et c'est en compilant des articles depuis plusieurs
sources que j'ai pu monter ce cluster.

Galera est une technologie de clusterisation de base de données bien
plus efficace que ce qu'on peut faire actuellement avec mysql. Un
cluster classique mysql fonctionne en mode actif/passif et si le nœud
actif tombe, il est nécessaire de faire une opération manuelle pour
passer un des nœud passif en actif. De plus, si un nœud reste éteint
durant une période prolongée, il ne peut plus rattraper son retard sur
le nœud primaire et sort du cluster. Galera règle ces problèmes avec un
cluster de nœuds actifs/actifs. Chaque nœud est capable de recevoir des
écritures et Galera s'occupe de synchroniser tout ça.

Pour réaliser le cluster, j'ai utilisé 4 serveurs Centos 7 : 3 nœuds
mariadb (il faut un chiffre impair pour respecter le quorum) et un
serveur haproxy en frontal en mode répartition de charge (leastconn) qui
fait office de passerelle d'accès. Les machines s'appellent
respectivement mariadb01, mariadb02, mariadb03 et mariadb-proxy.

Cet article s'attache à la mise en oeuvre du cluster en lui même. Un
second article détaillera `le déploiement
d'haproxy <http://blog.devarieux.net/2016/06/galera-load-balancing-failover-haproxy/>`__.

Configuration du nœud mariadb01
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On commence par récupérer le repo mariadb pour CentOS
ici \ https://downloads.mariadb.org/mariadb/repositories/ ce qui devrait
vous donner quelque chose comme ça:

.. code::

    # Put this file in /etc/yum.repos.d/
    # MariaDB 10.1 CentOS repository list - created 2016-06-20 19:31 UTC
    # http://downloads.mariadb.org/mariadb/repositories/
    [mariadb]
    name = MariaDB
    baseurl = http://yum.mariadb.org/10.1/centos7-amd64
    gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
    gpgcheck=1

On peut ensuite installer les paquets nécessaires

| ``yum -y install MariaDB-server MariaDB-client galera rsync xinetd``
|  On édite ensuite le fichier de configuration de galera
|  ``vim /etc/my.cnf.d/server.conf``
|  Et dans la zone du fichier dédiée à galera:

::

    [galera]
    # Mandatory settings
    wsrep_on=ON
    wsrep_provider='/lib64/galera/libgalera_smm.so'
    wsrep_cluster_address='gcomm://'
    wsrep_cluster_name='galera'
    wsrep_node_name='mariadb01'
    wsrep_sst_method=rsync
    binlog_format=row
    default_storage_engine=InnoDB
    innodb_autoinc_lock_mode=2
    bind-address=0.0.0.0

On ne donne aucune adresse pour le moment au cluster. On laisse la
valeur par défaut gcomm://. On reviendra sur cette partie plus tard.

Avant de démarrer le premier nœud du cluster, on lance la sécurisation
de l'instance mariadb avec la commande mysql\_secure\_installation.

Une fois cette étape effectuée, on peut démarrer le cluster. Cette
commande ne doit être lancée qu'une seule fois et seulement sur le
premier noeud configuré.

::

    galera_new_cluster

On se connecte ensuite sur l'instance mysql pour vérifier que le cluster
est bien opérationnel:

::

    [root@mariadb01 ~]# mysql -u root -p
    Enter password:
    Welcome to the MariaDB monitor. Commands end with ; or \g.
    Your MariaDB connection id is 18705
    Server version: 10.1.14-MariaDB MariaDB Server

    Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> SHOW GLOBAL STATUS WHERE Variable_name IN ('wsrep_ready', 'wsrep_cluster_size', 'wsrep_cluster_status', 'wsrep_connected');
    +----------------------+---------+
    | Variable_name        | Value   |
    +----------------------+---------+
    | wsrep_cluster_size   |    1    |
    | wsrep_cluster_status | Primary |
    | wsrep_connected      |    ON   |
    | wsrep_ready          |    ON   |
    +----------------------+---------+
    4 rows in set (0.01 sec)

Et voilà notre cluster Galera composée de 1 nœud pour le moment :)

Configuration de mariadb02 et mariadb03
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On reprend les mêmes étapes que pour mariadb01 en adaptant le fichier de
configuration. On n'oublie pas de lancer mysql\_secure\_installation.

Le fichier de conf de mariadb02 :

::

    [galera]
    # Mandatory settings
    wsrep_on=ON
    wsrep_provider='/lib64/galera/libgalera_smm.so'
    wsrep_cluster_address='gcomm://mariadb01,mariadb02'
    wsrep_cluster_name='galera'
    wsrep_node_name='mariadb02'
    wsrep_sst_method=rsync
    binlog_format=row
    default_storage_engine=InnoDB
    innodb_autoinc_lock_mode=2
    bind-address=0.0.0.0

On peut lancer le service mariadb de façon classique et vérifier que le
cluster est opérationnel :

::

    [root@mariadb02 ~]# systemctl start mariadb
    [root@mariadb02 ~]# mysql -u root -p
    Enter password:
    Welcome to the MariaDB monitor. Commands end with ; or \g.
    Your MariaDB connection id is 18905
    Server version: 10.1.14-MariaDB MariaDB Server

    Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> SHOW GLOBAL STATUS WHERE Variable_name IN ('wsrep_ready', 'wsrep_cluster_size', 'wsrep_cluster_status', 'wsrep_connected');
    +----------------------+---------+
    | Variable_name        | Value   |
    +----------------------+---------+
    | wsrep_cluster_size   |    2    |
    | wsrep_cluster_status | Primary |
    | wsrep_connected      |    ON   |
    | wsrep_ready          |    ON   |
    +----------------------+---------+
    4 rows in set (0.01 sec)

On a bien 2 nœuds dans notre cluster, passons à mariadb03

Le fichier de conf de mariadb03 :

::

    [galera]
    # Mandatory settings
    wsrep_on=ON
    wsrep_provider='/lib64/galera/libgalera_smm.so'
    wsrep_cluster_address='gcomm://mariadb01,mariadb02,mariadb03'
    wsrep_cluster_name='galera'
    wsrep_node_name='mariadb03'
    wsrep_sst_method=rsync
    binlog_format=row
    default_storage_engine=InnoDB
    innodb_autoinc_lock_mode=2
    bind-address=0.0.0.0

Idem, on lance le service et on vérifie que tout est ok:

::

    [root@mariadb02 ~]# systemctl start mariadb
    [root@mariadb02 ~]# mysql -u root -p
    Enter password:
    Welcome to the MariaDB monitor. Commands end with ; or \g.
    Your MariaDB connection id is 18905
    Server version: 10.1.14-MariaDB MariaDB Server

    Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> SHOW GLOBAL STATUS WHERE Variable_name IN ('wsrep_ready', 'wsrep_cluster_size', 'wsrep_cluster_status', 'wsrep_connected');
    +----------------------+---------+
    | Variable_name        | Value   |
    +----------------------+---------+
    | wsrep_cluster_size   |    3    |
    | wsrep_cluster_status | Primary |
    | wsrep_connected      |    ON   |
    | wsrep_ready          |    ON   |
    +----------------------+---------+
    4 rows in set (0.01 sec)

Trois nœuds dans le cluster, c'est bon!

Configuration finale
^^^^^^^^^^^^^^^^^^^^

On corrige maintenant les adresses de cluster sur les serveurs mariadb01
et mariadb02 en y mettant la même valeur que dans le fichier de conf de
mariadb03

::

    wsrep_cluster_address='gcomm://mariadb01,mariadb02,mariadb03'

Puis on redémarrer les services

::

    [root@mariadb02 ~]# systemctl restart mariadb

::

    [root@mariadb01 ~]# systemctl restart mariadb

C'est terminé.

A ce stade, vous devez pouvoir vous connecter sur n'importe quel noeud,
créer une base, elle sera dupliquée dans la foulée sur les autres nœuds.
