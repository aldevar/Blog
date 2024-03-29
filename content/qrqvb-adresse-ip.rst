QRQVB : L'adresse IP
####################
:date: 2009-09-16 19:12
:author: Aldevar
:category: Réseau
:slug: qrqvb-adresse-ip
:status: published

Définition :
~~~~~~~~~~~~

Une adresse IP identifie de manière unique une machine ainsi que le
réseau sur lequel elle est située. Chaque adresse est une série de 4
octets dont une partie correspond à l’\ **identificateur du réseau** et
l’autre partie à l’\ **identificateur de la machine**.
|  Exemple d’adresse IP : 172.19.174.125.

Concrètement, qu’est ce que cela signifie? En fait, puisque les machines
ne savent traiter qu’avec des nombres binaires (0 ou 1) l’adresse est
codée en binaire sur 4 octets. Sachant qu’un octet correspond à 8 bits,
cela nous donne, pour chaque octet 256 possibilités (2^8) pour une
valeur comprise en 0 et 255.

Allons un peu plus loin!
~~~~~~~~~~~~~~~~~~~~~~~~

C’est bien sympa d’avoir une adresse, encore faut-il qu’on puisse m’y
contacter! On vient de voir dans la définition que l’adresse IP est
divisée en 2 sous parties : **l’identificateur de
réseau** et **l’identificateur d’hôte**. C’est là qu’intervient le
masque de réseau. Alors puisque je ne suis pas fort en blablatage, je
vais plutôt vous montrer un exemple.
|  Voici une adresse IP : 192.168.1.15
|  Voici un masque de réseau : 255.255.255.0

.. image:: {static}/images/netmask1.png
  :target: /images/netmask1.png

En fait, pour être plus précis, les bits se situant dans la partie de
l’identificateur réseau sont tous positionnés sur 1 et les bits de la
partie hôte sur 0. En procédant à une opération de ET logique entre
l’adresse IP et le masque de réseau, on trouve l’adresse réseau. Les
opérations de ET logique suivent cette règle :

::

    0 ET 0 = 0
    0 Et 1 = 0
    1 ET 0 = 0
    1 ET 1 = 1

Grâce à cette adresse réseau, un routeur pourra déterminer quel chemin
doivent emprunter nos paquets IP. Pour bien comprendre ce système, nous
allons jouer un peu avec le binaire, même si je sais que ça va en
rebuter plus d’un :p

.. image:: {static}/images/binaire.png
  :target: /images/binaire.png

Ceci est important puisque c’est de cette manière qu’on va pouvoir
déterminer le nombre maximal de machines qui peuvent appartenir à un
réseau. Il faut également savoir que sur 1 réseau, 2 adresses sont
réservées. L’adresse \ **‘bits hôte à 0′** car c’est elle qui va définir
justement l’adresse de notre réseau, comme on vient de le voir, et
l’adresse \ **‘bits hôte à 1′** car elle correspond à l’adresse de
diffusion (broadcast). L’adresse de broadcast est nécessaire pour
diffuser un message sur tout le réseau. Le message de ce genre le plus
classique est la requête ARP. Celle ci permet à une machine de trouver
une autre machine sur le réseau en l’appelant.

Voici un exemple de capture de trame avec wireshark :

.. image:: {static}/images/arp2.png
  :target: /images/arp2.png

Le premier paquet est donc une requête ARP. La machine source envoie ce
message sur tout le réseau : ‘who has 192.168.1.51?  Tell 192.168.1.25′.
La machine qui a pour IP 192.168.1.51 envoie donc sa réponse directement
à 192.168.1.15 et lui dit que c’est l’adresse MAC 00:0a:78:9e:8a qui
possède cette IP. Tout ça pour vous dire que l’adresse IP ‘bits hôte à
1′ est donc réservée pour ce type de message.

Dimensionnement de réseau
~~~~~~~~~~~~~~~~~~~~~~~~~

Puisque le masque de réseau détermine le nombre maximal de machines sur
un réseau et que les adresses IP ne sont pas illimitées, on va pouvoir
travailler sur le dimensionnement du réseau en modifiant le masque. En
effet, \ **il est possible d’emprunter des bits à la partie hôte pour
les donner à la partie réseau**. Par exemple, le masque 255.255.255.0
permet d’avoir 256-2 = 254 hôtes différents sur le même réseau. Hors,
rares sont ceux qui disposent de 254 machines à interconnecter.

Admettons que mon réseau possède l’ip 192.168.1.0 (totalement au
hasard!) de masque 255.255.255.0 . Je dispose de 5 machines à connecter
sur ce réseau, jamais plus.

-  Si je garde 1bit dans la partie hôte, je vais disposer de 2^1 = 2
   hôtes possibles.  On vient de voir plus haut que 2 adresses sont
   reservées sur le réseau, (sisi, rapellez vous, juste au dessus!).
   Donc 2-2 = 0, ce qui me fait 0 hôte disponible.
-  Si je garde 2 bits pour ma partie hôte, il va me rester (2^2)-2 = 2
   hôtes possibles. Ce n’est toujours pas suffisant!!
-  Si je garde 3 bits pour la partie hôtes, j’obtiens (3^2)-2 = 6 hôtes
   possibles. Ouf!! j’ai assez de place pour caser mes machines. On va
   donc construire notre masque de réseau en gardant ces 3 bits sur 0,
   ce qui nous donne :

| 11111111.11111111.11111111.11111    000
|  Partie réseau                                         Partie hôte
|  Ce qui, transformé en décimal nous donne un masque : 255.255.255.248.

Ce qu’on vient de faire ici, c’est de créer des sous réseaux du réseau
192.168.1.0. Plusieurs sous réseaux composé chacun de 8 adresses IP.

::

    Sous réseau 1 : de 192.168.1.0 à 192.168.1.7 (avec 192.168.1.0 adresse de sous réseau et 192.168.1.7 adresse de broadcast)
    Sous réseau 2 : de 192.168.1.8 (adresse du réseau) à 192.168.1.15 (adresse de broadcast)
    Sous réseau 3 : de 192.168.1.16(adresse du réseau) à 192.168.1.23 (adresse de broadcast)
    etc etc..
    dernier sous réseau : de 192.168.1.248 (adresse de réseau) à 192.168.1.255 (adresse de broadcast)

Voilà donc ce qui se cache derrière les adresses IP. Plus mon sous
réseau sera petit, moins j’aurais de broadcast sur ce réseau. Parce que
mine ça papote pas mal la dedans et ça a tendance à broadcaster dans
tous les sens. Malheureusement, le broadcast n’est pas gratuit. Il coûte
de la bande passante. Et quand la bande passante sature, on commence à
perdre des paquets.

C’est pour ça qu’il est important, en entreprise en tout cas, de bien
calculer le dimensionnement de son réseau et l’adressage IP de
l’entreprise, sans oublier de prévoir que si l’entreprise s’agrandit, il
va falloir rajouter des hôtes sur certains sous réseaux et en plus
ajouter un nouveau sous réseau à notre entreprise pour y connecter un
nouveau bâtiment par exemple. Ça a vite tendance à tourner cacahuète si
on fait pas attention.




