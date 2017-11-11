RHEL 5.5 et chipset broadcom BCM5709
####################################
:date: 2010-06-28 19:36
:author: alain
:category: Tech
:tags: broadcom, Linux, pilote, Red hat, réseau
:slug: rhel-5-5-et-chipset-broadcom-bcm5709
:status: published

Nous avons récemment installé une nouvelle machine qui sert de serveur
principal pour notre nouveau système de sauvegarde. Lors des tests des
sauvegardes complètes du week end, le chipset réseau du serveur
s'écroulait lamentablement sous la charge du nombre de paquets qui
arrivaient. Même si le réseau semblait toujours fonctionnel (service
réseau lancé, ifconfig ne signal rien d'anormal), la machine était
injoignable et ne répondait pas au ping. Dans certains cas, un
redémarrage du service réseau ne suffit pas à retrouver une
connectivité.

A l'heure où la sauvegarde s'arrêtait, voici ce qu'on pouvait trouver
dans /var/log/messages :

::

    server1 kernel: NETDEV WATCHDOG: eth0: transmit timed out
    server1 kernel: bnx2: eth0 NIC Copper Link is Down

La résolution du problème passe par une mise à jour du pilote. On trouve
le pilote pour ce chipset à cette page :
http://www.broadcom.com/support/ethernet_nic/netxtremeii.php Après avoir
extrait l'archive, on installe les sources :

::

    rpm -ivh netxtreme2-<version>.src.rpm

Installation de kernel-devel pour pouvoir compiler les sources du
pilotes :

::

    yum install kernel-devel

Construction du paquet :

::

    cd /usr/src/redhat
    rpm -bb SPECS/netxtreme2.spec

Installation du paquet fraichement installé :

::

    rpm -ivh RPMS/<arch>/netxtreme2-<version>.<arch>.rpm

déchargement de l'ancien module :

::

    rmmode bnx2

Chargement du nouveau module :

::

    modprobe bnx2

Suite à cette petite manipulation, plus de soucis de chipset réseau qui
ne répond plus. Problème résolu :D

