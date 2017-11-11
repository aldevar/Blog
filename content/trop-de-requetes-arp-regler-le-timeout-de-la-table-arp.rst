Trop de requêtes ARP - Régler le timeout de la table ARP
########################################################
:date: 2015-01-21 20:18
:author: alain
:category: Tech
:tags: arp, kernel, Linux, osi, requête, table
:slug: trop-de-requetes-arp-regler-le-timeout-de-la-table-arp
:status: published

Pour des besoins spécifiques, nous avons fait l'acquisition d'un serveur
chez SoYouStart.

Le serveur étant assez puissant, nous avons décidé d'y installer un
hyperviseur Proxmox qui hébergera des VM CentOS

Avant de mettre en place les applications dont j'ai besoin sur ce
serveur, je l'ai installé et laissé tourner quelques temps pour
m'assurer de sa stabilité. Et le premier dimanche suivant l'installe,
voici le mail que je reçois, venant d'un bot de chez OVH et concernant
une des VM :

::

    Bonjour,

    Nous avons constaté que votre serveur diffuse inutilement un nombre important de requêtes sur le
    réseau via son IP failover XX.XX.XX.XX, ceci est dû à une mauvaise configuration de celle-ci.
    Nous vous avons demandé dans un mail précédant de bien vouloir reconfigurer votre IP failover, 
    constatant que le problème persiste, nous nous permettons de réitérer cette demande. 
    Si le problème n'est pas résolu dans un délais de 24 heures, nous nous verrons dans l'obligation de 
    bloquer votre IP. 

    Dans ce cas, il vous sera possible de la débloquer dans votre manager une fois la reconfiguration 
    faite. 

    Ceci est le dernier avertissement avant le blocage de votre IP !
    -------  EXTRAIT DES REQUETES  -------

    Thu Jan 8 06:47:25 2015 : arp who-has IP.DE.LA.GW tell XX.XX.XX.XX 
    Thu Jan 8 06:47:55 2015 : arp who-has IP.DE.LA.GW tell XX.XX.XX.XX 
    Thu Jan 8 06:48:25 2015 : arp who-has IP.DE.LA.GW tell XX.XX.XX.XX 
    Thu Jan 8 06:48:55 2015 : arp who-has IP.DE.LA.GW tell XX.XX.XX.XX 
    Thu Jan 8 06:49:25 2015 : arp who-has IP.DE.LA.GW tell XX.XX.XX.XX 
    Thu Jan 8 06:49:55 2015 : arp who-has IP.DE.LA.GW tell XX.XX.XX.XX 
    Thu Jan 8 06:50:25 2015 : arp who-has IP.DE.LA.GW tell XX.XX.XX.XX 

    -------   FIN DE L'EXTRAIT   -------

Une requête toutes les 30 secondes, c'est en effet beaucoup.

J'ai longtemps cherché d'où pouvait venir le problème. J'ai commencer
par changer de modèle de carte réseau dans Proxmox (E1000, VirtIO,
Vmxnet3) sans succès. J'ai reconfiguré et rereconfiguré le réseau en
ajoutant ou retirant des options dans le fichier ifcfg-eth0, rien à
faire, toujours autant de requêtes ARP.

En faisant tout ça, je me rendais bien compte d'une aberration dans les
opérations que je mettais en œuvre : je travaillais sur du niveau 3 (IP)
alors que j'avais un problème qui se situait entre la couche 2 et la
couche 3 (ARP).

Après moult recherches, j'ai fini par trouver où étaient les fichiers
qui pourraient m'aider.

Voici les fichiers concernés, avec leurs valeurs par défaut.

::

    /proc/sys/net/ipv4/neigh/default/anycast_delay:100
    /proc/sys/net/ipv4/neigh/default/app_solicit:0
    /proc/sys/net/ipv4/neigh/default/base_reachable_time:30
    /proc/sys/net/ipv4/neigh/default/base_reachable_time_ms:1200
    /proc/sys/net/ipv4/neigh/default/delay_first_probe_time:5
    /proc/sys/net/ipv4/neigh/default/gc_interval:30
    /proc/sys/net/ipv4/neigh/default/gc_stale_time:60
    /proc/sys/net/ipv4/neigh/default/gc_thresh1:128
    /proc/sys/net/ipv4/neigh/default/gc_thresh2:512
    /proc/sys/net/ipv4/neigh/default/gc_thresh3:1024
    /proc/sys/net/ipv4/neigh/default/locktime:100
    /proc/sys/net/ipv4/neigh/default/mcast_solicit:3
    /proc/sys/net/ipv4/neigh/default/proxy_delay:80
    /proc/sys/net/ipv4/neigh/default/proxy_qlen:64
    /proc/sys/net/ipv4/neigh/default/retrans_time:100
    /proc/sys/net/ipv4/neigh/default/ucast_solicit:3
    /proc/sys/net/ipv4/neigh/default/unres_qlen:3

Ici, les fichiers qui nous intéressent sont base\_reachable\_time (ou
base\_reachable\_time\_ms) et gc\_stale\_time.

Le fichier gc\_stale\_time définit la fréquence à laquelle l'état
'stale' (obsolète) des entrées de la table ARP sera vérifié. Le défaut
est à 60 secondes. Le fichier base\_reachable\_time quant à lui définit
la durée durant laquelle une entrée de la table ARP est considérée
valide. La durée de validité de cette entrée sera un chiffre choisi au
hasard entre (base\_reachable\_time/2) et (3\*base\_reachable\_time/2).
La valeur par défaut est de 30 secondes.

Un simple echo du chiffre souhaité dans le fichier suffit. CentOS permet
d'avoir ces valeurs en dure et persistante après un redémarrage (les
autres distributions aussi sans doute, mais je ne sais par quel moyen).

Pour CentOS donc, dans le fichier /etc/sysctl.conf, ajouter ces lignes :

::

    ##### Pour limiter le nombre de requête ARP ##########
    ##### Equivalent a 30 minutes ###########
    net.ipv4.neigh.default.base_reachable_time_ms = 1200000
    net.ipv4.neigh.default.gc_stale_time = 3600

Ces valeurs vont donner une durée de validité des entrées de la table
ARP entre 15 et 45 minutes.
