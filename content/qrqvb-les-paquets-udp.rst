QRQVB : Les paquets UDP
#######################
:date: 2009-12-29 11:23
:author: alain
:category: network
:slug: qrqvb-les-paquets-udp
:status: published

Suite de la Question Réseau Qui Va Bien, nouveau billet purement réseau
donc. Je comptais me lancer dans la description des paquets TCP, mais je
pense qu’il est plus intéressant de se pencher d’abord sur UDP avant
d’appréhender TCP.

UDP (Pour *User Datagram Protocol*) se situe dans la couche 4 du `modèle
OSI <http://blog.devarieux.net/2009/08/qrqvb-le-modele-osi/>`__ (couche
transport). Pour rappel, au niveau de la couche 3 (IP), `les
datagrammes <http://blog.devarieux.net/2009/09/qrqvb-datagramme-ip/>`__
sont routés d’une machine à une autre en fonction des adresses IP (en
fait, le routage se fait en fonction de l’adresse réseau, voir `QRQVB :
L’adresse IP <http://blog.devarieux.net/2009/09/309/>`__). Lors de cette
opération de routage, aucune distinction n’est faite entre les
différents services pour lesquels ces paquets peuvent être destinés. Que
ce soit pour une connexion SSH (port 22) ou HTTP (port 80) ou autre, les
datagrammes IP sont tous indifféremment mélangés.

La couche 4 du modèle OSI ajoute un mécanisme qui permet
l’identification du service  concerné. Plusieurs programmes de plusieurs
utilisateurs pouvant simultanément circuler sur le réseau, il est
indispensable de faire un tri entre les applications. Ici, l’idée est
d’associer la destination du paquet à une fonction. L’identification de
cette fonction ce fait à l’aide d’un chiffre nommé **Port**.

En tête UDP
~~~~~~~~~~~

|encaps|

 

Lors de l’étude des `datagramme
IP <qrqvb-datagramme-ip.html>`__, nous
avions vu le contenu de l’entête du paquet (partie verte). Ici, nous
allons observer le contenu de l’entête du message (partie jaune) lorsque
l’on traite un p>aquet UDP.

Le paquet UDP est composé de 8 octets.

 |entete|

**Les 2 premiers octets contiennent le port source**. Codé sur 16 bits
donc. C’est le numéro de port de l’émetteur du paquet. C’est aussi le
numéro de port sur lequel le destinataire doit envoyer sa réponse.

**Les octets 3 et 4 stockent le port de destination.** C’est sur ce port
que sera remis le paquet lors de sa livraison à la machine ciblée.

Le port étant un entier positif de 16 bits, on en déduit que les bornes
sont 0 – 65535 (2^16). Cependant, le port 0 n’est pas exploitable.

**Les octets 5 et 6 contiennent la longueur de l’entête UDP** et du
message. Sa longueur minimal est 8 (entête UDP avec 0 données à
transporter) et sa longueur maximal 2^16 = 65535 (64ko).

**Les 2 derniers octets contiennent le cheksum**. C’est la somme de
contrôle de l’entête UDP et des données qui suivent.

Ports réservés
~~~~~~~~~~~~~~

Toute machine qui utilise la pile TCP/IP se doit de connaitre un
certains nombre de services bien connus, aussi appelé « well known port
number » pour pouvoir dialoguer avec les autres machines sur internet.
Sur une machines Unix, cette liste est placée dans le fichier
***/etc/services*** et se doit d’être lisible par tous les utilisateurs
et toutes les applications. Voici un extrait du contenu de ce fichier :

::

    Nom             Port/Protocol     Commentaire

    netstat        15/tcp
     qotd       17/tcp      quote
     msp        18/tcp      # message send protocol
     msp        18/udp
     chargen    19/tcp      ttytst source
     chargen    19/udp      ttytst source
     ftp-data   20/tcp
     ftp        21/tcp
     fsp        21/udp      fspd
     ssh        22/tcp      # SSH Remote Login Protocol
     ssh        22/udp
     telnet     23/tcp
     smtp       25/tcp      mail
     time       37/tcp      timserver
     time       37/udp      timserver
     rlp        39/udp      resource    # resource location
     nameserver 42/tcp      name        # IEN 116
     whois      43/tcp      nicname
     tacacs     49/tcp              # Login Host Protocol (TACACS)
     tacacs     49/udp
     re-mail-ck 50/tcp              # Remote Mail Checking Protocol
     re-mail-ck 50/udp
     domain     53/tcp              # name-domain server
     domain     53/udp
     mtp        57/tcp              # deprecated
     tacacs-ds  65/tcp              # TACACS-Database Service
     tacacs-ds  65/udp
     bootps     67/tcp              # BOOTP server
     bootps     67/udp
     bootpc     68/tcp              # BOOTP client
     bootpc     68/udp
     tftp       69/udp
     gopher     70/tcp              # Internet Gopher
     gopher     70/udp
     rje        77/tcp      netrjs
     finger     79/tcp
     www        80/tcp      http        # WorldWideWeb HTTP
     www        80/udp              # HyperText Transfer Protocol

Les ports 1 à 1023 sont réservés aux « well known ports ». Ils ne
peuvent être utilisés que par des applications qui s’exécutent avec des
droits privilégiés (root). Les autres ports peuvent être utilisés
librement sans privilège particulier et sont en général employés par les
applications clientes. Par exemple, sur ma machine, en ce moment, mon
client IRC utilise le port 59175 pour communiquer avec le serveur irc
holmes.freenode.net.

 

Mode non connecté
~~~~~~~~~~~~~~~~~

Contrairement à TCP, UDP est conçu pour permettre un échange de données
entre 2 applications sans échange préliminaire. UDP est utilisé si les
données à transmettre n’ont pas besoin d’être fragmentées en plusieurs
paquet. La paquet est ainsi envoyé sans s’assurer qu’il arrive bien à
destination. UDP est appelé mode de transport non connecté par
opposition à TCP. Plus particulièrement, les paquets a destination d’une
application UDP sont conservés dans une pile de type FIFO. Si
l’application destinatrice ne les “consomme” pas assez rapidement, les
plus anciens paquets risquent d’être écrasés par les plus récents… Un
risque supplémentaire de perte de données.

Nous verrons comment TCP peut palier à ce problème dans la prochaine
QRQVB

.. |encaps| image:: /images/encaps.png
   :target: /images/encaps.png
.. |entete| image:: /images/entete.png
   :target: /images/entete.png
