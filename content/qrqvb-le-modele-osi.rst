QRQVB : Le modèle OSI
#####################
:date: 2009-08-17 18:30
:author: Aldevar
:category: Réseau
:slug: qrqvb-le-modele-osi
:status: published

Dans cette nouvelle catégorie (la Question Réseau Qui Va Bien), je vous
propose de (re)découvrir avec moi, quelques notions fondamentales de
réseau. Ces articles s'adressent en particulier à ceux qui souhaitent
comprendre les mécanismes d'Internet et/ou du routage en WAN ou en LAN.
J'essaierai d'être le plus clair possible. Si vous trouvez des erreurs,
non-sens dans ces articles, je suis ouvert à toutes critiques,
corrections. Et pour inaugurer cette catégorie, commençons donc par le
modèle OSI, qui est la base pour une bonne compréhension des mécanismes
des réseaux informatiques.

Définition
~~~~~~~~~~

Le modèle OSI est une norme définie par l'ISO pour permettre
l'interconnexion des systèmes. Il propose un modèle d'architecture
réseau afin de s'assurer que tous les systèmes interconnectés puissent
communiquer entre eux quel que soit le constructeur du matériel. Les
constructeurs informatiques ont proposé des architectures réseaux
propres à leurs équipements. Par exemple, IBM a proposé SNA, DEC a
proposé DNA... Ces architectures ont toutes le même défaut : du fait de
leur caractère propriétaire, il n'est pas facile des les interconnecter,
à moins d'un accord entre constructeurs. Le modèle OSI ne précise pas
vraiment les services et protocoles à utiliser pour chaque couches. Il
décrit plutôt ce que doivent faire ces couches. Je sais que ça ne parait
pas très clair pour le moment, mais ça va le devenir.

Schéma du modèle
~~~~~~~~~~~~~~~~

.. image:: {static}/images/modele_OSI.gif
  :target: images/modele_OSI.gif

Le modèle OSI est donc représenté en 7 couches distinctes. J'ai ici
représenté 2 machines (Système A et Système B) pour bien montrer que
lors de la communication de 2 hôtes, chaque couche 'discute' directement
avec la couche équivalente de l'hôte d'en face.

1°) Couche Physique
^^^^^^^^^^^^^^^^^^^

La couche physique s'occupe de la transmission des bits de façon brute
sur un canal de communication. Plus clairement, elle est typiquement
représentée par votre carte réseau et sa prise ethernet (et non pas le
protocole ethernet!!). La couche phyique discute directement avec l'hôte
suivant sur le réseau. C'est à dire que lors d'une communication sur
internet, cette couche ne s'occupe de l'envoie des données que vers la
machine suivante, en général un routeur. La couche physique traite
exclusivement avec des bits 0 et 1 et normalise l'écriture de ces bits
(une tension de 5V corespond à un 1, -5V un 0).

2°) Couche Liaison
^^^^^^^^^^^^^^^^^^

La couche de liaison (ou liaison de donnée) est un liant entre les 2
couches physiques des hôtes en communications. Elle fractionne les
données en trames et tente d'exempter la couche physique des erreurs de
transmissions. Elle doit être capable de renvoyer une trame lorsqu'il y
a un problème sur la ligne et intègre également un système de gestion de
flux pour éviter les engorgements. Par exemple une carte 100Mb/s relié à
une carte 1Gb/S doivent pouvoir communiquer sans que la carte 100Mb/s
recoive 10x trop de données. L'unité d'information de cette couche est
donc la trame qui est composé de quelques centaines d'octets.

3°) Couche Réseau
^^^^^^^^^^^^^^^^^

La couche réseau construit la liaison de bout en bout lors de la
communication de 2 hôtes. C'est la seule couche directement concernée
par la topologie du réseau. Elle va trouver la route parmis les routeurs
pour atteindre l'hôte cible. Lors d'un envoie de données, 2 paquets
différents peuvent emprunter des routes différentes suivant
l'architecture du réseau et ses point d'engorgement. C'est la dernière
couche supportée par TOUTES les machines du réseau (hôtes, switchs,
routeurs, serveurs). Son unité d'information est le paquet.

4°) Couche Transport
^^^^^^^^^^^^^^^^^^^^

Cette couche est responsable du bon acheminement des messages complets
au destinataire. Le rôle principal de la couche transport est de prendre
les messages de la couche session, de les découper s'il le faut en
unités plus petites et de les passer à la couche réseau et inversement
du coté du recepteur. Comme on l'a vu dans la couche réseau, 2 paquets
d'un même message peuvent prendre des routes différentes et donc arriver
dans le désordre. Le rôle de la couche transport est donc de remettre
ces paquets dans l'ordre. Elle peut aussi gérer le multiplexage lors de
communications multiples entre 2 mêmes hôtes (par exemple une connexion
http et ftp sur le même canal). Son unité d'information est le message.

5°) Couche Session
^^^^^^^^^^^^^^^^^^

Le service principale de la couche session est la synchronisation des
communications. Qui veut parler? Qui parle? Elle permet aussi de prendre
des 'snapshots' des flots de données pour pouvoir reprendre le dialogue
là où il en était avant une coupure du canal de communication.

6°) Couche Présentation
^^^^^^^^^^^^^^^^^^^^^^^

La couche présentation est chargée du codage des données de la couche
application. En effet, toutes les couches plus basses transportent des
octets sans chercher comprendre leur signification. Ici, elle va
s'occuper d'encoder du texte, des images, de la video, de la voix etc...
en données transportables, c'est à dire en octet.

7°) Couche Application
^^^^^^^^^^^^^^^^^^^^^^

Cette couche est le point de contact entre l'utilisateur et le réseau.
Elle lui apporte l'interface lui permettant de communiquer avec celui ci
(messagerie, http, ftp etc...).

Exemples de protocoles
~~~~~~~~~~~~~~~~~~~~~~

#. Physique → biphase, bipolaire simple
#. Liaison → ATM, Ethernet, PPP, TokenRing, Fiber Distributed Date
   Interface (FDDI)
#. Réseau → IP, IPX, ICMP
#. Transport → TCP, UDP (pour les plus connus)
#. Session → SIP, Appletalk
#. Présentation → ASCII, Unicode, ASN.1, Videotex
#. Application → HTTP, SMTP, POP, FTP, DNS, SNMP


