GNS3 - Créer son premier Lab
############################
:date: 2015-08-26 10:03
:author: Aldevar
:category: Réseau
:slug: gns3-creer-son-premier-lab
:status: published

Premier Lancement
~~~~~~~~~~~~~~~~~

Après avoir installé GNS3 et ses différents modules dans `un précédent
article <https://blog.devarieux.net/2015/08/prise-en-main-de-gns3-pour-la-simulation-reseau.html>`__,
nous allons maintenant voir comment créer un Lab et faire un petit
exercice simple de configuration de routes statiques. La première chose
est d'ajouter un nouveau routeur dans la configuration de GNS3. Ici, ce
sera un c2691, qui est un vieux routeur possédant 4 emplacements. Si
vous me demandez gentiment, je peux peut-être vous fournir l'image IOS
pour ce modèle.

Au premier lancement de GNS3, il vous est proposé de créer un projet, ce
que nous allons faire tout de suite en enregistrant ce projet sous le
nom FirstLab.

.. image:: {static}/images/2015-08-25-21_47_47-Prise-en-main-de-GNS3-pour-la-simulation-réseau-À-La-Benne-Nightly.png
  :target: /images/2015-08-25-21_47_47-Prise-en-main-de-GNS3-pour-la-simulation-réseau-À-La-Benne-Nightly.png


.. image:: {static}/images/2015-08-25-21_48_59-New-project.png
  :target: /images/2015-08-25-21_48_59-New-project.png 
 
Une fois le projet créé, on va ajouter un routeur dans la configuration de GNS3.
Pour cela, on se rend dans Edit > Preferences.

.. image:: {static}/images/2015-08-25-21_51_11-Preferences.png
  :target: /images/2015-08-25-21_51_11-Preferences.png

Je vous laisse parcourir les options afin que vous puissiez comprendre un peu mieux le logiciel. Si vous avez des VM VirtualBox, GNS3 les trouvera et vous les listera dans le menu VirtualBox.

.. image:: {static}/images/2015-08-25-22_00_01-Preferences.png
  :target: /images/2015-08-25-22_00_01-Preferences.png

Ajout d'un routeur
~~~~~~~~~~~~~~~~~~

Pour ajouter un routeur Cisco, on se rend dans Dynamips > IOS Router et
on clique sur New. Il suffit ensuite de suivre les indications et de
fournir l'image IOS du routeur qu'on souhaite voir apparaître.

.. image:: {static}/images/2015-08-25-21_55_51-Preferences.png
  :target: /images/2015-08-25-21_55_51-Preferences.png

.. image:: {static}/images/2015-08-25-21_56_47-New-IOS-router-template.png
  :target: /images/2015-08-25-21_56_47-New-IOS-router-template.png

.. image:: {static}/images/2015-08-25-21_57_08-New-IOS-router-c2691-jk9s-mz.123-17.image_.png
  :target: /images/2015-08-25-21_57_08-New-IOS-router-c2691-jk9s-mz.123-17.image_.png

.. image:: {static}/images/2015-08-25-21_57_22-New-IOS-router-c2691-jk9s-mz.123-17.image_.png
  :target: /images/2015-08-25-21_57_22-New-IOS-router-c2691-jk9s-mz.123-17.image_.png

.. image:: {static}/images/2015-08-25-21_58_01-New-IOS-router-c2691-jk9s-mz.123-17.image_.png
  :target: /images/2015-08-25-21_58_01-New-IOS-router-c2691-jk9s-mz.123-17.image_.png

.. image:: {static}/images/2015-08-25-21_59_26-New-IOS-router-c2691-jk9s-mz.123-17.image_.png
  :target: /images/2015-08-25-21_59_26-New-IOS-router-c2691-jk9s-mz.123-17.image_.png|

Pour la valeur de Idle-PC, ne recopiez pas bêtement ce qui est écrit dans cette fenêtre. Ce chiffre correspond seulement à ma machine. Cliquez sur le bouton Idle-Pc finder et GNS3 trouvera la valeur de lui même. Cela peut prendre un peu de temps à calculer. 

.. image:: {static}/images/2015-08-25-21_59_40-Preferences.png
  :target: /images/2015-08-25-21_59_40-Preferences.png

Voilà, nous avons notrevrouteur c2691. On peut maintenant fermer la fenêtre de configuration et commencer notre projet.

Le Lab
~~~~~~

Nous allons mettre en place un Lab très basique de routage statique
entre 2 routeurs. Un premier routeur situé à Rennes aura une interface
Loopback ayant pour IP 2.2.2.2/24, et un second routeur à Paris aura une
interface Loopback ayant 1.1.1.1/24 pour IP.

Sur chacun de ces 2 routeurs, nous allons ajouter une carte ayant 4
ports séries. Nous utiliserons 2 de ces ports. Le port Serial1/0 de
Rennes sera branché au port Serial1/0 de Paris et le port Serial1/1 de
Rennes sera branché sur le port Serial1/1 de Paris.

Les configurations IP seront les suivantes :

-  Rennes Serial1/0 : 192.168.1.1/24
-  Rennes Serial1/1 : 192.168.2.1/24
-  Paris Serial1/0 : 192.168.1.2/24
-  Paris Serial1/1 : 192.168.2.2/24

Et pour rappel, les interfaces Loopback

-  Rennes Loopback0 : 2.2.2.2/24
-  Paris Loopback0 : 1.1.1.1/24

Une fois tout cela mis en place, le but sera de réussir à pinger l'IP
1.1.1.1 depuis Rennes et pinger l'IP 2.2.2.2 depuis Paris en mettant en
place des routes statiques.

Pour la mise en place du Lab, suivez le guide...

Cliquez sur *Browse Routers* dans la colonne de gauche puis glissez 2
fois le routeur c2691 dans le projet. Sur le routeur R1, faites un
clique droit : *Configure*

.. image:: {static}/images/2015-08-25-22_02_55-FirstLab.gns3_-—-GNS3.png
  :target: /images/2015-08-25-22_02_55-FirstLab.gns3_-—-GNS3.png


Renommez le en **Rennes** et dans l'onglet *slot*, ajoutez lui une carte NM-4T dans le
Slot 1. Faites de même pour le routeur R2 en le renommant **Paris**.

.. image:: {static}/images/2015-08-25-22_05_43-Node-configurator.png
  :target: /images/2015-08-25-22_05_43-Node-configurator.png

Une fois de retour sur le
projet, cliquez sur '*Add a Link'* dans la colonne de gauche et créer 2
liens séries en cliquant dans un premier temps sur *Rennes > Serial 1/0*
puis *Paris > Serial 1/0* pour le premier lien et *Rennes > Serial 1/1*
puis *Paris > Serial 1/1* pour le second lien.

.. image:: {static}/images/2015-08-25-22_07_19-FirstLab.gns3_-—-GNS3.png
  :target: /images/2015-08-25-22_07_19-FirstLab.gns3_-—-GNS3.png

Vous devriez avoir quelque chose qui ressemble à ça :

.. image:: {static}/images/2015-08-25-22_11_04-FirstLab.gns3_-—-GNS3.png
  :target: /images/2015-08-25-22_11_04-FirstLab.gns3_-—-GNS3.png

J'ai moi même ajouté les
notes sur les réseaux grâce aux notes que l'on peut insérer dans le
projet.

Une fois que c'est terminé, cliquez sur le Play vert qui se trouve en
haut de l'interface afin de démarrer les routeurs.

Nous allons enfin pouvoir ouvrir notre première console Cisco. Pour
cela, clique droit sur un routeur > *Console*\ 

.. image:: {static}/images/2015-08-25-22_19_50-FirstLab.gns3-—-GNS3.png
  :target: /images/2015-08-25-22_19_50-FirstLab.gns3-—-GNS3.png

Pour préparer le lab, voici les
commandes à taper dans la console de Rennes :

IOS supporte la tabulation et les raccourcis. Par exemple, pour taper
``configure terminal``, je peux taper ``conf<tab> t<tab>`` ou tout
simplement ``conf t``

::

    Rennes#enable                    //active le mode privilège
    Rennes#conf t                    //configure terminal
    Rennes(config)#int loopback0     //configurer l'interface Loopback0
    Rennes(config-ig)#ip add 2.2.2.2 255.255.255.0    
    Rennes(config-if)#no shut        //monter l'interface (état up)
    Rennes(config-if)#exit
    Rennes(config)#int Serial1/0
    Rennes(config-if)#ip add 192.168.1.1 255.255.255.0
    Rennes(config-if)#no shut
    Rennes(config-if)#exit
    Rennes(config)#int Serial1/1
    Rennes(config-if)#ip add 192.168.2.1 255.255.255.0
    Rennes(config-if)#no shut
    Rennes(config-if)#exit
    Rennes(config)#

Même manipulation sur le routeur de Paris :

::

    Paris#enable
    Paris#conf t
    Paris(config)#int loopback0
    Paris(config-ig)#ip add 1.1.1.1 255.255.255.0    
    Paris(config-if)#no shut
    Paris(config-if)#exit
    Paris(config)#int Serial1/0
    Paris(config-if)#ip add 192.168.1.2 255.255.255.0
    Paris(config-if)#no shut
    Paris(config-if)#exit
    Paris(config)#int Serial1/1
    Paris(config-if)#ip add 192.168.2.2 255.255.255.0
    Paris(config-if)#no shut
    Paris(config-if)#exit
    Paris(config)#

Afin de voir l'état de vos interfaces, vous pouvez taper la commande
suivantes : ``do show ip int brief``

::

    Rennes(config)#do show ip int brief
    Interface                  IP-Address      OK? Method Status                Protocol
    FastEthernet0/0            unassigned      YES unset  administratively down down
    FastEthernet0/1            unassigned      YES unset  administratively down down
    Serial1/0                  192.168.1.1     YES manual up                    up
    Serial1/1                  192.168.2.1     YES manual up                    up
    Serial1/2                  unassigned      YES unset  administratively down down
    Serial1/3                  unassigned      YES unset  administratively down down
    Loopback0                  2.2.2.2         YES manual up                    up

Arriver ici, le but est de pinger l'interface Loopback de Rennes depuis
Paris en passant par le réseau 192.168.1.0 et l'interface Loopback de
Paris depuis Rennes en passant par le réseau 192.168.2.0.

Pour arriver à cet objectif, nous allons dire au routeur de Paris que
pour rejoindre le réseau 2.2.2.0/24 il doit passer par l'interface de
Rennes 192.168.1.1 qu'il connait car il est directement branché dessus.

De la même manière, nous allons dire au routeur de Rennes qu'il soit
passer par l'interface 192.168.2.2 de Paris pour joindre le réseau
1.1.1.0/24.

Voici donc les commandes à taper en console

::

    Paris(config)#ip route 2.2.2.0 255.255.255.0 192.168.1.1
    Paris(config)#do ping 2.2.2.2

    Type escape sequence to abort.
    Sending 5, 100-byte ICMP Echos to 2.2.2.2, timeout is 2 seconds:
    !!!!!
    Success rate is 100 percent (5/5), round-trip min/avg/max = 112/243/288 ms
    Paris(config)#

Le ping fonctionne!!

Depuis Rennes

::

    Rennes(config)#ip route 1.1.1.0 255.255.255.0 192.168.2.2
    Rennes(config)#do ping 1.1.1.1

    Type escape sequence to abort.
    Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
    !!!!!
    Success rate is 100 percent (5/5), round-trip min/avg/max = 128/136/148 ms
    Rennes(config)#do show ip route        //pour voir les routes statiques
    Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
           D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
           N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
           E1 - OSPF external type 1, E2 - OSPF external type 2
           i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
           ia - IS-IS inter area, * - candidate default, U - per-user static route
           o - ODR, P - periodic downloaded static route

    Gateway of last resort is not set

         1.0.0.0/24 is subnetted, 1 subnets
    S       1.1.1.0 [1/0] via 192.168.2.2
         2.0.0.0/24 is subnetted, 1 subnets
    C       2.2.2.0 is directly connected, Loopback0
    C    192.168.1.0/24 is directly connected, Serial1/0
    C    192.168.2.0/24 is directly connected, Serial1/1

Voilà pour la prise en main de GNS3 et la configuration basique de 2
routeurs. Vous n'avez plus qu'à créer vos propres labs, ajouter des VM
et tenter de les faire communiquer par exemple.

Je vous proposerais peut être moi même de nouveaux labs d'ici quelques
temps

