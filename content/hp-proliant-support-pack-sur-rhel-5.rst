HP Proliant Support Pack sur RHEL 5
###################################
:date: 2013-07-23 18:07
:author: Aldevar
:category: Sysadmin
:slug: hp-proliant-support-pack-sur-rhel-5
:status: published

Dans le cadre de mon travail, je suis en train d'installer et de
configurer un serveur HP System Insight Manager (SIM). Une sorte de
Nagios amélioré pour serveur HP, avec anticipation des pannes matériel.

Ce serveur SIM nous a permis par exemple de détecter qu'une pile de
cache RAID était en train de lâcher et nous avons donc pu remplacer
cette pile avant que le problème intervienne (pas de cache RAID = temps
d'accès en écriture tout moisi et ça le fait moyen sur un serveur de
sauvegarde).

Pour que le serveur HPSIM accède aux serveurs qu'il surveille, il faut
installer un agent. Cet agent, c'est HP Proliant Support Pack. Une suite
d'utilitaires et de pilotes pour serveur HP Proliant.

J'ai donc téléchargé l'iso `sur le site
d'HP.  <http://h18004.www1.hp.com/products/servers/service_packs/en/index.html>`__\ Celle
ci contient les utilitaires pour tous les OS supportés (Windows, RedHat,
HP-UX). Une fois l'iso transférée sur le serveur, je la monte :

::

    mkdir /media/iso
    mount -o loop /tmp/fichier.iso /media/iso

Ensuite, c'est l'utilitaire HPSUM qui va s'occuper d'installer les
différents modules et utilitaires.

::

    cd /media/iso/hp/swpackages/
    ./hpsum

Cette commande utilise un serveur X.
|  Pour info, la doc complète : `Guide de l'Utilisateur, HP Smart Update
Manager <http://bizsupport1.austin.hp.com/bc/docs/support/SupportManual/c03114114/c03114114.pdf>`__

En suivant les étapes une à une, les packages sont tous compilés et
installés.

Aïe
---

Malheureusement, parfois, tout ne tourne pas rond et dans mon cas,
certains paquets n'ont pas pu être compilés. Les logs montrent un obscur
message de problème de dépendance avec ksym.

Pour résoudre ce problème et terminer l'installation des paquets, voici
la procédure ;

Installation des sources :

::

    cd /media/iso/hp/swpackages/
    rpm -ivh <paquet>.src.rpm
    rpmbuild -bb /usr/src/redhat/SPECS/<paquet>.spec
    rpm -ivh --nodeps /usr/src/redhat/RPMS/<arch>/<paquet>.rpm

On vérifie que le module a bien été installé :

::
    modinfo <nomdumondule>

On charge le module :

::
    modprobe <nomdumodule>

Ce qui donne, avec le paquet qla4xxx qui me concernait :

::

    rpm -ivh hp-qla4xxx-<version>.src.rpm
    rpmbuild -bb /usr/src/redhat/SPECS/hp-qla4xxx.spec
    rpm -ivh --nodeps /usr/src/redhat/RPMS/x86_64/kmod-hp-qla4xxx-<version>-x86_64.rpm
    modprobe qla4xxx

Explication
-----------

Les RPM utilisent les dépendances de KMP (Kernel Module Packaging) pour
s'assurer que les binaires RPM puissent être installés. Red Hat
maintient une liste blanche de \ *kernel symbols* (ksym donc) que les
RPM utilisent. Certains de ses symboles peuvent être dans le kernel mais
pas dans la liste blanche. Le résultat est que certains RPM, qui y font
référence, ne peuvent pas être installés.

L'utilisateur doit donc utiliser l'option "--nodeps" lors de
l'installation des binaires.

La paquet qla4xxx utilisent les symboles suivant sur RHEL 5 qui ne sont
pas dans la liste blanche ;

ksym(kobject\_uevent\_env) ksym(iscsi2\_session\_chkready)
ksym(pci\_get\_domain\_bus\_and\_slot)
