Vmware tools, Centos 7 et customisation
#######################################
:date: 2015-08-14 22:39
:author: alain
:category: sysadmin
:slug: vmware-tools-centos-7-et-customisation
:status: published

Depuis quelques temps, lorsqu'on souhaite déployer les VMware tools dans
une VM Centos 7 / RedHat 7, le script d'installation hurle de ne pas
utiliser le script perl fournit mais de passer plutôt par les
open-vm-tools qu'on peut directement trouvé dans le gestionnaire de
paquet.

::

    yum install open-vm-tools

C'est simple, rapide, ça facilite les mise à jour des tools et c'est
conseillé par VMware directement, il y a même `un
KB <http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2073803>`__
pour ça et `un projet
GitHub <https://github.com/vmware/open-vm-tools>`__.

Pour rappel, l'insallation des vm-tools permet d'accéder à ces
fonctionnalité vSphere :

-  Synchronisation de l'horloge de l'OS invité avec celle de la
   plateforme de virtualisation
-  Permet à l'hyperviseur de procéder à des appels système afin par
   exemple de demander à l'OS de s'arréter.
-  Support de vSphere High Availability (HA) grace à un système de
   heartbeat.
-  Permet à l'hyperviseur de récolter des informations sur la
   consommation des ressources CPU, RAM, réseau.

Dans cette liste, il manque tout de même un outil important. Si vous
clonez ou si vous créez un template à partir d'une VM ayant les
open-vm-tools, vous serez dans l'incapacité de customiser la nouvelle VM
à sa création. Exit donc le changement du mot de passe root et surtout
la configuration réseau. Cette fonctionnalité est apportée par un plugin
pour open-vm-tools nommé DeployPkg.

La page `Red Hat Enterprise Linux 7 Guest Operating System Installation
Guide <http://partnerweb.vmware.com/GOSIG/RHEL_7.html>`__ mentionne bien
ce plugin mais il y manque certaines informations. La procédure complète
est mieux décrite dans la `Knowledge Base de
VMware. <http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2075048>`__\ Celle
ci consiste a récupérer les clés public du dépots VMware, importer les
clés, créer le fichier de repo pour yum et procéder enfin à
l'installation.

Dans un premier temps, on récupère les clés ici
http://packages.vmware.com/tools/keys et on les place dans le répertoire
/tmp du serveur

On importe les clés avec rpm

::

    rpm --import /tmp/key1
    rpm --import /tmp/key2

Création du fichier */etc/yum.repos.d/vmware-tools.repo* avec ce contenu
:

::

    [vmware-tools]
    name = VMware Tools
    baseurl = http://packages.vmware.com/packages/rhel7/x86_64/
    enabled = 1
    gpgcheck = 1

Installation du paquet

::

    yum install open-vm-tools-deploypkg

Installation de perl, nécessaire pour les scripts de customisation

::

    yum install perl

On termine par le rechargement du service pour prendre en compte
l'installation du plugin

::

    systemctl restart vmtoolsd

Vous pouvez maintenant transformer votre VM en template en toute
sérénité.
