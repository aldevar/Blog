Comprendre la prédiction de noms des interfaces réseau de systemd
#################################################################
:date: 2015-08-22 23:58
:author: alain
:category: Tech
:slug: comprendre-la-prediction-de-noms-des-interfaces-reseau-de-systemd
:status: published

*Cet article est une traduction d'\ `un article
original <https://major.io/2015/08/21/understanding-systemds-predictable-network-device-names/>`__
de Major Hayden, publié `sur son blog <https://major.io/>`__ le 21 Aout
2015. Article traduit avec son aimable autorisation.*

J'ai un peu parlé des nom des interfaces réseau de systemd dans un de
mes premiers post sur `systemd-networkd et le
bonding <https://major.io/2015/08/21/using-systemd-networkd-with-bonding-on-rackspaces-onmetal-servers/>`__.
J'avais alors eu quelques questions sur la manière dont systemd
détermine le nom final des interfaces réseau. La prédictibilité de ces
noms m'a `pris de court l'été
dernier <https://major.io/2014/08/06/unexpected-predictable-network-naming-systemd/>`__
quand je n'ai pas pu comprendre comment ces noms étaient construits.
|  Observons donc ce processus

Que contient le nom?
~~~~~~~~~~~~~~~~~~~~

Dans l'article sur le bonding avec systemd-networkd, j'avais utilisé une
carte réseau Intel dual port montée sur un port hotplug

::

    # udevadm info -e | grep -A 9 ^P.*eth0
    P: /devices/pci0000:00/0000:00:03.2/0000:08:00.0/net/eth0
    E: DEVPATH=/devices/pci0000:00/0000:00:03.2/0000:08:00.0/net/eth0
    E: ID_BUS=pci
    E: ID_MODEL_FROM_DATABASE=82599ES 10-Gigabit SFI/SFP+ Network Connection (Ethernet OCP Server Adapter X520-2)
    E: ID_MODEL_ID=0x10fb
    E: ID_NET_DRIVER=ixgbe
    E: ID_NET_LINK_FILE=/usr/lib/systemd/network/99-default.link
    E: ID_NET_NAME_MAC=enxa0369f2cec90
    E: ID_NET_NAME_PATH=enp8s0f0
    E: ID_NET_NAME_SLOT=ens9f0

Dans ce dump de la base de donnée udev, on voit que l'interface réseau
possède plusieurs noms

-  ID\_NET\_NAME\_MAC=enxa0369f2cec90
-  ID\_NET\_NAME\_PATH=enp8s0f0
-  ID\_NET\_NAME\_SLOT=ens9f0

D'où viennent ces noms? Nous pouvons nous plonger dans la code source de
systemd pour comprendre l'origine de ces noms et lequel est sélectionné
au final.

Descendre dans le terrier de udev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Voici un extrait du fichier
`src/udev/udev-builtin-net\_id.c <https://github.com/systemd/systemd/blob/master/src/udev/udev-builtin-net_id.c>`__:

.. code:: c

    /*
     * Predictable network interface device names based on:
     *  - firmware/bios-provided index numbers for on-board devices
     *  - firmware-provided pci-express hotplug slot index number
     *  - physical/geographical location of the hardware
     *  - the interface's MAC address
     *
     * http://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames
     *
     * Two character prefixes based on the type of interface:
     *   en -- ethernet
     *   sl -- serial line IP (slip)
     *   wl -- wlan
     *   ww -- wwan
     *
     * Type of names:
     *   b<number>                             -- BCMA bus core number
     *   ccw<name>                             -- CCW bus group name
     *   o<index>[d<dev_port>]                 -- on-board device index number
     *   s<slot>[f<function>][d<dev_port>]     -- hotplug slot index number
     *   x<MAC>                                -- MAC address
     *   [P<domain>]p<bus>s<slot>[f<function>][d<dev_port>]
     *                                         -- PCI geographical location
     *   [P<domain>]p<bus>s<slot>[f<function>][u<port>][..][c<config>][i<interface>]
     *                                         -- USB port number chain

Voici donc la manière dont sont nommées nos interfaces. Les cartes
Ethernet commenceront toujours par *en*, elles peuvent ensuite être
suivie d'un *p* (pour port PCI), un *s* (pour port PCI-E), un *o* (pour
carte interne (onboard)). En descendant un peu dans le fichier, on
trouve des exemples à partir de la ligne 56.

De vrais exemples
~~~~~~~~~~~~~~~~~

Nous avons vu plus haut le nommage des interfaces PCI-E sur un serveur
OnMetal de chez Rackspace. Elles étaient nommées *ens9f0* et *ens9f1*.
Cela signifie qu'elles sont sur un port PCI-E qui se trouve être le port
numéro 9. Les indexes sont à 0 et 1 (pour les 2 ports Ethernet sur
l'Intel 82599ES).

Firewall Linux avec une carte PCI dual-port.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Voici un exemple avec mon firewall Linux personnel. C'est un Dell
Optiplex 3020 avec une carte Intel I350-T2(dual-port):

::

    # udevadm info -e | grep -A 10 ^P.*enp1s0f1
     P: /devices/pci0000:00/0000:00:01.0/0000:01:00.1/net/enp1s0f1
     E: DEVPATH=/devices/pci0000:00/0000:00:01.0/0000:01:00.1/net/enp1s0f1
     E: ID_BUS=pci
     E: ID_MODEL_FROM_DATABASE=I350 Gigabit Network Connection (Ethernet Server Adapter I350-T2)
     E: ID_MODEL_ID=0x1521
     E: ID_NET_DRIVER=igb
     E: ID_NET_LINK_FILE=/usr/lib/systemd/network/99-default.link
     E: ID_NET_NAME=enp1s0f1
     E: ID_NET_NAME_MAC=enxa0369f6e5227
     E: ID_NET_NAME_PATH=enp1s0f1
     E: ID_OUI_FROM_DATABASE=Intel Corporate

L'affichage de lspci:

::

    # lspci -s 01:00
     01:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
     01:00.1 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)

Cette carte est branchée sur le premier bus PCI (enp1), slot 0 (s0).
Comme c'est une carte dual-port, elle possède 2 indexes (f0 et f1). Cela
fait donc apparaître 2 noms prédictibles : *enp1s0f1* et *enp1s0f0*.

Serveur 1U avec 4 ports Ethernet.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prenons un autre exemple. Voici un serveur SuperMicro X9SCA 1U avec 4
cartes Ethernet PCI internes.

::

    # udevadm info -e | grep -A 10 ^P.*enp2s0
     P: /devices/pci0000:00/0000:00:1c.4/0000:02:00.0/net/enp2s0
     E: DEVPATH=/devices/pci0000:00/0000:00:1c.4/0000:02:00.0/net/enp2s0
     E: ID_BUS=pci
     E: ID_MODEL_FROM_DATABASE=82574L Gigabit Network Connection
     E: ID_MODEL_ID=0x10d3
     E: ID_NET_DRIVER=e1000e
     E: ID_NET_LINK_FILE=/usr/lib/systemd/network/99-default.link
     E: ID_NET_NAME=enp2s0
     E: ID_NET_NAME_MAC=enx00259025963a
     E: ID_NET_NAME_PATH=enp2s0
     E: ID_OUI_FROM_DATABASE=Super Micro Computer, Inc.

Voici les 4 cartes dans lspci

::

    # for i in `seq 2 5`; do lspci -s 0${i}:; done
     02:00.0 Ethernet controller: Intel Corporation 82574L Gigabit Network Connection
     03:00.0 Ethernet controller: Intel Corporation 82574L Gigabit Network Connection
     04:00.0 Ethernet controller: Intel Corporation 82574L Gigabit Network Connection
     05:00.0 Ethernet controller: Intel Corporation 82574L Gigabit Network Connection

C'est assez intéressant car elles ne sont pas toutes sur le même bus
PCI. Elles se situent sur les bus 2 à 5 du slot 0. Il n'y a donc pas de
numéro d'index dans ce cas. Elles sont donc nommées de *enp2s0* à
*enp5s0*. Ce ne sont pas de vraies cartes internes, elles sont donc
nommées en fonction de leur localisation.

Serveur de stockage avec carte ethernet interne
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Voici un exemple de serveur avec une vrai carte ethernet interne
(onboard):

::

    $ udevadm info -e | grep -A 11 ^P.*eno1
     P: /devices/pci0000:00/0000:00:19.0/net/eno1
     E: DEVPATH=/devices/pci0000:00/0000:00:19.0/net/eno1
     E: ID_BUS=pci
     E: ID_MODEL_FROM_DATABASE=Ethernet Connection I217-V
     E: ID_MODEL_ID=0x153b
     E: ID_NET_DRIVER=e1000e
     E: ID_NET_LABEL_ONBOARD=en Onboard LAN
     E: ID_NET_LINK_FILE=/usr/lib/systemd/network/99-default.link
     E: ID_NET_NAME_MAC=enxe03f49b159c0
     E: ID_NET_NAME_ONBOARD=eno1
     E: ID_NET_NAME_PATH=enp0s25
     E: ID_OUI_FROM_DATABASE=ASUSTek COMPUTER INC.

L'affichage de lspci

::

    $ lspci -s 00:19.0
     00:19.0 Ethernet controller: Intel Corporation Ethernet Connection I217-V (rev 05)

Cette carte a un nouveau type de nom dans udev :
ID\_NET\_NAME\_ONBOARD. Le code de udev pour systemd a une prise en
charge spécifique des cartes internes car elles se situent en général
sur le bus principal. Le nommage peut devenir assez laid car le 19
devrait être converti en hexadécimal dans le nom.
|  Si systemd ne prenait pas en charge cette carte différemment, elle
aurait du être nommée *enp0s13* (car 19 devient 13 en hexa). Cela peut
mener à des confusions.

Choix du nom finale
~~~~~~~~~~~~~~~~~~~

Comme nous l'avons vu plus haut, udev contient une grande liste de nom
dans sa base. Cependant, il ne peut y avoir qu'un seul nom dans l'OS.
|  Retournons dans le code. Cette fois, jetons un oeil a
`src/udev/net/link-config.c <https://github.com/systemd/systemd/blob/master/src/udev/net/link-config.c#L403>`__
à partir de la ligne 403:

.. code:: c

    if (ctx->enable_name_policy && config->name_policy) {
            NamePolicy *policy;
     
            for (policy = config->name_policy;
                 !new_name && *policy != _NAMEPOLICY_INVALID; policy++) {
                    switch (*policy) {
                            case NAMEPOLICY_KERNEL:
                                    respect_predictable = true;
                                    break;
                            case NAMEPOLICY_DATABASE:
                                    new_name = udev_device_get_property_value(device, "ID_NET_NAME_FROM_DATABASE");
                                    break;
                            case NAMEPOLICY_ONBOARD:
                                    new_name = udev_device_get_property_value(device, "ID_NET_NAME_ONBOARD");
                                    break;
                            case NAMEPOLICY_SLOT:
                                    new_name = udev_device_get_property_value(device, "ID_NET_NAME_SLOT");
                                    break;
                            case NAMEPOLICY_PATH:
                                    new_name = udev_device_get_property_value(device, "ID_NET_NAME_PATH");
                                    break;
                            case NAMEPOLICY_MAC:
                                    new_name = udev_device_get_property_value(device, "ID_NET_NAME_MAC");
                                    break;
                            default:
                                    break;
                    }
            }
    }

Si on regarde le case dans son ensemble, on voit que la première
correspondance est conservée et donne le nom à l'interface. En partant
du haut vers le bas, udev prend le premier de cette liste:

-  ID\_NET\_NAME\_FROM\_DATABASE
-  ID\_NET\_NAME\_ONBOARD
-  ID\_NET\_NAME\_SLOT
-  ID\_NET\_NAME\_PATH
-  ID\_NET\_NAME\_MAC

Si on retourne sur le serveur OnMetal en haut de l'article, on peut
suivre cette logique. La base udev contient:

::

    E: ID_NET_NAME_MAC=enxa0369f2cec90
    E: ID_NET_NAME_PATH=enp8s0f0
    E: ID_NET_NAME_SLOT=ens9f0

Le daemon udev commencerait par ID\_NET\_NAME\_FROM\_DATABASE, mais
cela n'existe pas pour cette carte. Il passe ensuite à
ID\_NET\_NAME\_ONBOARD, qui n'est pas présent. Vient ensuite
ID\_NET\_NAME\_SLOT, voilà la correspondance! L'entrée
ID\_NET\_NAME\_SLOT contient *ens9f0*, qui est donc le nom final de
l'interface réseau.
|  Cette boucle gère aussi quelques cas spéciaux. La première est de
vérifier si udev n'est pas configuré pour ne pas utiliser les noms
prédictible. Nous l'avions vu dans le post sur le\ `bonding avec
systemd-networkd <https://major.io/2015/08/21/using-systemd-networkd-with-bonding-on-rackspaces-onmetal-servers/>`__
quand la configuration du bootloader contenait net.ifnames=0. Si cette
commande noyau est présente, les noms prédictibles ne sont pas utilisés.
|  Un autre cas spécial est ID\_NET\_NAME\_FROM\_DATABASE. Ces ports
viennent de la `base de donnée matériel interne de
udev <https://github.com/systemd/systemd/blob/master/hwdb/20-net-ifname.hwdb>`__.
Ce fichier ne contient pour le moment qu'une seule entrée et c'est pour
une carte réseau particulière iDRAC de DELL.

Confondu par l'hexa
~~~~~~~~~~~~~~~~~~~

Si les numéros des ports PCI ne semblent pas se suivre, lisez mon
`post de l'été
dernier <https://major.io/2014/08/06/unexpected-predictable-network-naming-systemd/>`__.
J'avais eu affaire à un serveur Dell particulier avec une carte Intel
dual-port sur le bus PCI 42. Le nom de l'interface était *enp66s0f0* et
j'en étais resté perplexe.
|  Le nom *enp66s0f0* semble signifier que nous avons une carte sur le
bus PCI 66, slot 0, avec de multiple fonction d'index. Cependant,
systemd fait une conversion des numéros de slot PCI en hexa. La décimal
42 devient donc 66 en hexa.
|  La plupart des serveurs n'auront pas cette complexité mais il est
important de se souvenir de la conversion en hexa.

Feedback
~~~~~~~~

Ces articles sur systemd sont ils intéressant? Je suis un grand fan de
systemd et j'adore écrire à son sujet.
