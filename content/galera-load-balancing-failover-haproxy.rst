Galera Mariadb: Load balancing et Failover HAproxy
##################################################
:date: 2016-06-21 21:47
:author: alain
:category: Linux, Tech
:tags: cluster, failover, galera, ha, haproxy, mariadb, mysql
:slug: galera-load-balancing-failover-haproxy
:status: published

Après avoir mis en place le `cluster Galera
Mariadb <http://blog.devarieux.net/2016/06/monter-cluster-galera-mariadb/>`__,
nous avons besoin d'un point d'accès au cluster. Ce point d'accès peut
être un proxy mysql ou tout autre serveur HA.

Nous allons configurer HAproxy avec l'option leastconn pour qu'il envoie
les paquets vers la machine ayant le moins de connexions (Load
Balancing) et nous allons mettre en place un check http pour qu'en cas
de problème sur un noeud, HAproxy ne lui envoie plus de paquets
(FailOver).

Pour cela, nous avons besoin du script clustercheck présent
ici \ https://github.com/olafz/percona-clustercheck. Ce script doit être
présent sur chaque noeud du cluster mariadb.

Préparation des nœuds du cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Toutes les opérations détaillées dans cette section doivent être
effectuées sur tous les nœuds du cluster mariadb.

On commence par récupérer le script clustercheck, puis on créé un
utilisateur mysql pour l’exécution du script et on place le script au
bon endroit

::

    wget https://raw.githubusercontent.com/olafz/percona-clustercheck/master/clustercheck
    mysql> GRANT PROCESS ON *.* TO 'clustercheckuser'@'localhost' IDENTIFIED BY 'clustercheckpassword!'
    chmod +x clustercheck
    mv clustercheck /usr/bin

L'étape suivante consiste à créer un service xinetd dont la tâche sera
de lancer le script clustercheck à la demande.

Création du fichier \ ``/etc/xinetd.d/mariadbcheck``:

::

    # default: on
    # description: mariadbcheck
    service mariadbcheck
    {
            disable = no
            flags = REUSE
            socket_type = stream
            port = 9200
            wait = no
            user = nobody
            server = /usr/bin/clustercheck clustercheckuser clustercheckpassword! 
            log_on_failure += USERID 
            only_from = 0.0.0.0/0 
            per_source = UNLIMITED }

Dans le champ only\_from, vous pouvez mettre l'adresse ip d'HAproxy si
vous le souhaitez (avec un /32 à la fin).

Pour avoir un service propre et bien configuré, on l'ajoute aussi dans
``/etc/services`` en commentant les anciens services utilisant le port
9200 (service wap, a priori votre serveur ne devrait pas en avoir besoin
:) )

::

    mariadbcheck     9200/tcp                # mariadbcheck
    #wap-wsp         9200/tcp                # WAP connectionless session service
    #wap-wsp         9200/udp                # WAP connectionless session service

On redémarre xinetd et on devrait avoir le port 9200 en écoute.

Pour vérifier que ça fonctionne, lancez la commande ``clustercheck``.
Elle doit renvoyer du text contenant ``HTTP/1.1 200 OK`` qui sera le
retour attendu par HAproxy pour s'assurer que le noeud du cluster est
atteignable.

Configuration d'HAproxy
^^^^^^^^^^^^^^^^^^^^^^^

La plus gros du boulot est fait. Reste à définir le cluster dans
HAproxy.

Ceci se fait dans le fichier de conf en y ajoutant à la fin :

::

    listen galera-mariadb 0.0.0.0:3306
      balance leastconn
      option httpchk
      mode tcp
      server mariadb01 ip.de.mariadb.01:3306 check port 9200 inter 5000 fastinter 2000 rise 2 fall 2
      server mariadb02 ip.de.mariadb.02:3306 check port 9200 inter 5000 fastinter 2000 rise 2 fall 2
      server mariadb03 ip.de.mariadb.03:3306 check port 9200 inter 5000 fastinter 2000 rise 2 fall 2

Après avoir redémarré HAproxy, le cluster doit être joignable et on doit
pouvoir prouver le load balancing :

::

    [root@haproxy]# mysql -uroot -p -h127.0.0.1 -e "show variables like 'wsrep_node_name' ;"
    +-----------------+---------------+
    | Variable_name   | VALUE         |
    +-----------------+---------------+
    | wsrep_node_name |   mariadb01   |
    +-----------------+---------------+

::

    [root@haproxy]# mysql -uroot -p -h127.0.0.1 -e "show variables like 'wsrep_node_name' ;"
    +-----------------+---------------+
    | Variable_name   | VALUE         |
    +-----------------+---------------+
    | wsrep_node_name |   mariadb02   |
    +-----------------+---------------+

::

    [root@haproxy]# mysql -uroot -p -h127.0.0.1 -e "show variables like 'wsrep_node_name' ;"
    +-----------------+---------------+
    | Variable_name   | VALUE         |
    +-----------------+---------------+
    | wsrep_node_name |   mariadb03   |
    +-----------------+---------------+

 
