QRQVB : Datagramme IP
#####################
:date: 2009-09-16 11:07
:author: Aldevar
:category: Réseau
:slug: qrqvb-datagramme-ip
:status: published

Je vais tenter dans cet article de décortiquer un datagramme IP et
notamment son en-tête. Nous allons commencer par l’observation des
encapsulations des données suivant le `modèle
OSI <http://blog.devarieux.net/2009/08/qrqvb-le-modele-osi/>`__ que nous
avons étudié la dernière fois. Les données (couche application) sont
encapsulées dans un message (couche 4, transport) qui est lui même
encapsulé dans un paquet (couche 3, réseau), lui même encapsulé dans une
trame (couche 2, liaison). Rien ne vaut un bon dessin pour
comprendre.\ 

.. image:: {static}/images/encaps.png
  :target: /images/encaps.png

Aujourd’hui, on va donc s’intéresser à ce que contient le petit carré
vert lorsque le paquet est un paquet IP.

Cet en-tête est codé par défaut sur 20 octets. Nous allons donc nous
appliquer à décrypter le contenu de chacun de ses octets. J’ai fait pour
cela un schéma pas terrible mais qui me servira de support pour les
explications :p.

 

.. image:: {static}/images/entete1.png
  :target: /images/entete1.png

 

-  **Le premier octet contient 2 informations.**

   -  La première est la version du protocole utilisé, codée sur 4 bits.
      pour le protocole IPv4, on utilisera le code 0100 qui correspond
      au 4 décimal. Pour IPv6, c’est 0110 (6 décimal).
   -  La seconde information, codée également sur 4 bits contient l’IHM.
      C’est la longueur, en mot de 32bits (4 octets), de l’en-tête du
      datagramme. Par défaut, ces bits sont positionnés sur 0101, ce qui
      correspond au 5 décimal, ce qui est logique pour un en-tête par
      défaut de 20 octets.

 

-  **Le deuxième octet est le TOS (type of service)** et va définir la
   manière dont le datagramme doit être traité. Il se décompose lui
   aussi en 2 :

   -  3 bits pour la priorité à donner au datagramme (0 à 7)
   -  4 bits qui définissent chacun une option activée ou pas (1 option
      activée, 0 option desactivée)

      -  1er bit : D → Positionné sur 1 pour privilégier le délai
         d’acheminement
      -  2ème bit : T → Positionné sur 1 pour privilégier le débit
      -  3ème bit : R → Positionné sur 1 pour privilégier la fiabilité
      -  4ème bit : C → Positionné sur 1 pour privilégier le coût

   -  1 bit qui ne contient aucune information. Il est appelé MBZ pour
      Must Be Zero. comme son nom l’indique, ce bit doit être positionné
      sur 0.

-  **Les 3ème et 4ème octets contiennent le champ Longueur Totale (Total
   Lenght)**. Codé sur 16 bits, il contient la taille, en octet, du
   datagramme complet (en-tête + données). On en déduit donc que la
   longueur totale du paquet ne peut dépasser 65535 octets. Grâce à
   cette valeur, on peut calculer la taille des données :

   -  longueur données = Longueur totale – (IHM x 4)

-  **Les 5ème et 6ème octets contiennent le champ Identification**.
   Celui ci intervient lors du ré-assemblage des paquets pour
   reconstituer les données lorsque celles ci sont fragmentées.
-  **Les 7ème et 8ème octets contiennent 2 informations.**

   -  3 bits correspondent au champ **flag**. Il sert a déterminer
      l’état de fragmentation.

      -  1er bit : Réservé, il doit être sur 0
      -  2ème bit : Don’t Fragment. Indique si la fragmentation est
         autorisée.
      -  3ème bit : More Fragment. Positionné sur 1 il signifie que ce
         datagramme n’est pas le dernier fragment.
      -  13 bits correspondent au champ **Position Fragment**. Ce champ
         indique la position du fragment par rapport au premier
         datagramme et interviendra lors de la reconstitution du
         message.

-  **Le 9ème octet contient le TTL (Time to Live).** ‘Durée de vie’ en
   français. Il indique le nombre maximal de routeurs que peut traverser
   le datagramme. Il est initialisé par la station émettrice et
   décrémenté de 1 par chaque routeur qui reçoit le datagramme et le
   réexpédie. Si un routeur reçoit un datagramme dont le TTL est nul, il
   le détruit et renvoie à l’expéditeur un message ICMP. Le but de ce
   champ est d’éviter les paquets fantômes qui circuleraient en boucle
   sur le réseau sans atteindre leur destination.

    Pour la petite histoire, c’est de cette manière que fonctionne
    l’application **traceroute**. Lorsqu’on lance traceroute
    `www.devarieux.net <http://www.devarieux.net>`__, traceroute envoie
    un ping vers www.devarieux.net avec un TTL de 1. Lorsque le premier
    routeur reçoit le paquet, il le détruit et renvoie à l’expediteur un
    message ICMP l’informant que le paquet a été détruit (time to live
    exceeded). Ce message ICMP contient dans son en-tête l’adresse IP du
    routeur. Suite à cela, traceroute recommence l’opération mais avec
    un TTL de 2 et ainsi de suite jusqu’à toucher www.aldevar.fr. Et
    c’est de cette manière qu’on obtient la route prise par notre
    paquet. Attention ceci dit car 2 paquets envoyés vers la même
    destination peuvent emprunter des routes différentes.

-  **Le 10ème octet sert à coder le protocole** qui se trouve dans les
   données qui suivent l’en-tête. Il est codé sur 8 bits. Les protocoles
   les plus communs sont ICMP (0000.0001), TCP (0000.0110) et UDP
   (0001.0001).
-  **11ème et 12ème octets : Le checksum**. C’est la somme de contrôle
   de l’en-tête du datagramme. Chaque machine qui reçoit le paquet doit
   recalculer ce checksum car la modification du TTL modifie celui ci.
-  Les octets 13 à 16 contiennent l’\ **adresse IP de la machine
   émétrice**. C’est également l’adresse de réponse.
-  Et enfin les 4 derniers octets contiennent eux l’\ **adresse IP de
   destination**.

Capture de trame
~~~~~~~~~~~~~~~~

Puisqu’il n’est pas particulièrement évident pour nous, simples mortels,
de lire ces bits pour comprendre ce que contient le datagramme, on peut
utiliser un logiciel de capture de trame tel que **wireshark** en mode
graphique ou **tcpdump** en mode commande. Je vous laisse vous même
découvrir ces applications. Je vais me contenter ici de montrer un
screenshot d’une capture faite avec wireshark qui montre ce que ce
logiciel peut nous dire sur le contenu de nos paquets.

.. image:: {static}/images/trame01.png
  :target: /images/trame01.png

Voici le type de paquet que nous avons capturé. C’est un
simple ping entre 2 machines se situant sur des réseaux différents.
Wireshark nous dit déjà que c’est un paquet ICMP. Voyons le détail de ce
datagramme :

.. image:: {static}/images/trame02.png
  :target: /images/trame02.png

En dépliant le contenu de l’en-tête IP, voici ce que wireshark peut nous
dire :

-  Nous sommes en IPv4.
-  Le header fait 20 octets (bytes et non bits).
-  La longueur total du datagramme est de 60 octets. On en conclue donc
   que nous avons 40 octets de données.
-  Le message n’est pas fragmenté.
-  Le TTL est de 128 ce qui signifie qu’après avoir traversé 128
   routeurs, le paquet sera détruit.
-  Le protocole contenu dans les data est ICMP
-  Le checksum est correct.
-  Enfin, à la fin, les IP de départ et de destination.

Voilà, c’est terminé pour l’analyse de paquet de niveau 3. La prochaine
fois, j’essaierai d’expliquer le contenu d’un en-tête  de niveau 4
(couche transport : UDP, TCP etc…) ou de niveau 2 (couche liaison, trame
ethernet). Si vous trouvez que cet article manque de précision n’hésitez
pas à m’en faire part.









