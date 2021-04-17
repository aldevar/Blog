Zabbix - Superviser un cluster Ceph
###################################
:date: 2016-07-05 21:45
:author: alain
:category: sysadmin
:tags: ceph, devops, python, zabbix
:slug: zabbix-superviser-cluster-ceph
:status: published

Ceph est une solution open source de stockage distribué avec réplication
des données et une forte tolérance aux pannes. Différentes commandes
existent pour vérifier l'état du cluster et nous allons voir comment les
exploiter avec des scripts Python pour que Zabbix puisse récupérer les
métriques.

|Ceph_Logo|

Je suis parti d'un `template déjà
existant <https://github.com/thelan/ceph-zabbix>`__, avec un script bash
qui exécute les commandes, parse la sortie et retourne la métrique
attendue. Ce script, à mon avis, a cependant un problème. A chaque
exécution, il exécute toutes les commandes, parse toutes les réponses et
retourne enfin la métrique attendue suivant l'argument passé en entrée.
Ce comportement peu optimisé induit que parfois, suivant la charge du
serveur, l’exécution du script peut prendre trop de temps et l'item
Zabbix tombe en timeout. Ce n'est évidemment pas un comportement que
nous souhaitons avoir.

Puisqu'il fallait reprendre le script, je me suis lancé dans sa complète
réécriture en Python. J'ai pu ainsi profiter du format json proposé par
les outils Ceph pour l'output des données et également du module json
inclus dans Python. Cela m'a permis de gagner du temps (pour moi et le
processeur) car je peux parser les données plus facilement. Le script
bash utilise beaucoup d'expressions régulières via sed. Dorénavant, je
n'ai qu'à appeler le bon objet json et l'afficher.

La version actuel du template comporte 3 scripts. Je peux encore
optimisé tout cela en 1 seul fichier, ce sera pour la prochaine version.
Le premier script nommé cephpools.py permet la découverte automatique
des pools rados Ceph. Le second, cephimages.py, permet quant à lui la
découverte automatique des images rbd de chaque pool. C'est également ce
script qui est appelé pour récupérer la taille des images.

Enfin, le script principal ceph-status.py s'occupe de retourner les
valeurs des métriques à  Zabbix : état des pg, santé du cluster, IOPS,
état des mon etc.

Vous pouvez retrouver ces scripts et template zabbix `sur la page github
dédiée <https://github.com/aldevar/ceph-zabbix>`__

.. |Ceph_Logo| image:: /images/Ceph_Logo.png
