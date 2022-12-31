QRQVB : Protocole TCP
#####################
:date: 2010-02-02 07:00
:author: Aldevar
:category: Réseau
:slug: qrqvb-protocole-tcp
:status: published

Nouvelle QRQVB et pas des moindres, le protocole TCP (Transmission
Control Protocol, Protocole de Contrôle de Transmission).  Comme son
petit frère UDP, TCP se situe en couche 4 du `modèle
OSI <https://web.archive.org/web/20110919035256/http://blog.aldevar.fr/?p=232>`__.

Caractéristique de TCP
~~~~~~~~~~~~~~~~~~~~~~

TCP est bien plus compliqué qu’UDP examiné au `chapitre
précédent <https://web.archive.org/web/20110919035256/http://blog.aldevar.fr/?p=493>`__.
Il apporte en contrepartie des services beaucoup plus élaborés.

-  TCP contient un mécanisme pour assurer **le bon acheminement des
   données**. Cette possibilité est absolument indispensable dès lors
   que les applications doivent transmettre de gros volumes de données
   de façon fiable. Cette fonction est assurée par un mécanisme
   d’acquittement (ou accusé de réception). Les paquets de données sont
   acquittés de bout en bout et non de point à point. C’est à dire que
   ce sont les machines sources et machines de destinations qui
   s’occupent de cela et non les routeurs qui se situent entre les 2.
-  Le protocole TCP permet l’établissement d’un **circuit virtuel**
   entre les 2 machines qui échangent de l’information (Voir a ce propos
   le `commentaire de
   Guizmo.7 <https://web.archive.org/web/20110919035256/http://blog.aldevar.fr/?p=528#comment-757>`__).
   On dit aussi que TCP  fonctionne en **mode connecté** (par opposition
   à UDP qui est en mode non connecté). En pratique, l’une des 2 machine
   doit effectuer un appel que l’autre doit accepter. S’en suit une
   discutions afin d’établir certains paramètres de communication. Une
   fois les préliminaires terminés, les protocoles informent les
   applications respectives que la connexion est établie et que le
   transfert peut débuter. Durant le transfert, le dialogue entre les
   protocoles continue, pour vérifier le bon acheminement des données.
-  TCP a la capacité de **mémoriser les données**. Les paquets pouvant
   prendre chacun un chemin différent pour arriver à destination, il
   arrive que ceux ci n’arrivent pas dans le bon ordre. Grâce à cette
   capacité de mémorisation, TCP garde les paquets un certains temps et
   les reconstitue lorsqu’ils sont tous arrivés afin de présenter les
   données à l’application.
-  TCP simule une connexion en **« full duplex »**. Pour chacune des 2
   machines en connexion, l’opération qui consiste à lire des données
   peut s’effectuer indépendamment de celle qui consiste à en écrire.

Entête TCP
~~~~~~~~~~

.. image:: {static}/images/enteteTCP1.png
  :target: /images/enteteTCP1.png

L’entête TCP est codé sur 20 octets hors options.

-  Port Source (16 bits): Port utilisé par l’application sur la machine
   source.
-  Port Destination (16 bits): Port de destination.
-  Numéro d’ordre (32 bits): Correspond au numéro du paquet. Cette
   valeur permet de situer à quel endroit du flux de données le paquet,
   qui est arrivé, doit se situer par rapport aux autres paquets.
-  Numéro d’accusé de réception (32 bits): Acquittement pour les paquets
   reçus. Cette valeur signale le prochain numéro de paquet attendu. Par
   exemple, si il vaut 1500, cela signifie que tous les datagrammes
   <1500 ont été reçus
-  Offset (4 bits): Le champ Offset est codé sur 4 bits et définit le
   nombre de mots de 32 bits dans l’entête TCP. Ce champ indique donc où
   les données commencent.
-  Réservé (6 bits): Champ inutilisé actuellement. Il était à l’origine
   prévu pour l’avenir. On peut dire aujourd’hui que ce champ restera
   vide.
-  Drapeaux (flags) (6×1 bit): Les drapeaux représentent des
   informations supplémentaires :
   URG: si ce drapeau est à 1 le paquet doit être traité de façon
   urgente.
   ACK: si ce drapeau est à 1 le paquet est un accusé de réception.
   PSH (PUSH): si ce drapeau est à 1, le paquet fonctionne suivant la
   méthode PUSH.
   RST: si ce drapeau est à 1, la connexion est réinitialisée.
   SYN: Le Flag TCP SYN indique une demande d’établissement de
   connexion.
   FIN: si ce drapeau est à 1 la connexion s’interrompt.
-  Fenêtre (16 bits): Champ permettant de connaître le nombre d’octets
   que le récepteur souhaite recevoir sans envoyer d’accusé de
   réception.
-  Somme de contrôle (Checksum ou CRC): La somme de contrôle est
   réalisée en faisant la somme des champs de données de l’en-tête, afin
   de pouvoir vérifier l’intégrité de l’en-tête
-  Pointeur d’urgence (16 bits): Indique le numéro d’ordre à partir
   duquel l’information devient urgente.

Établissement d’une connexion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: {static}/images/ConnectionTCP.png
  :target: /images/ConnectionTCP.png

Une ouverture de connexion TCP s’effectue en 3 temps.

L’émetteur du premier paquet doit avoir connaissance du couple
**`IP <https://web.archive.org/web/20110919035256/http://blog.aldevar.fr/?p=293>`__
: Port** de l’application de la machine réceptrice (par exemple, on
contact un serveur HTTP sur le port 80 qui lui est dédié). L’émetteur de
ce premier paquet est à l’origine de l’établissement du circuit virtuel.
C’est une attitude qualifiée de « \ **cliente**\ « .

Le récepteur du premier paquet accepte l’établissement de la connexion,
ce qui suppose qu’il était prêt à le faire avant que le client en prenne
l’initiative. C’est une attitude de « \ **serveur**\ « .

Le client envoie un segment comportant le drapeau SYN à 1. Le serveur
répond avec sa propre séquence (SYN = 1) mais il doit aussi acquitter le
paquet précédent, ce qu’il fait avec ACK. Le client répond alors avec un
acquittement de la séquence du serveur (ACK = 1).

Une fois achevée cette phase appelée « Three-way handshake », les 2
applications sont en mesure d’échanger des données.

 



