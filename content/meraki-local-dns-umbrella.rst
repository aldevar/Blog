Utilisation d'un DNS interne avec Umbrella sous Cisco Meraki
#############################################################
:date: 2021-03-02 22:20
:author: Aldevar
:category: Tech
:tags: reseau, meraki, cisco, umbrella, dns
:slug: meraki-umbrella-and-internal-dns
:status: published

Cisco Umbrella (anciennement Open DNS) est un DNS menteur qui permet de se protéger des sites malveillant et notamment des ransomwares. Le service évolue de plus en plus vers une offre SASE complète même si sa fonctionnalité première est la protection DNS.

Les équipements Cisco Meraki peuvent nativement rediriger les requêtes DNS vers Cisco Umbrella. En interceptant les requêtes DNS et en les envoyant vers Umbrella, l'équipement wifi (MR) Meraki forge une réponse DNS renvoyé au client. Que ce passe-t-il lorsqu'une organisation utilise un DNS interne pour la résolution d'un nom de domaine local? 

J'ai récemment été confronté à ce scénario et j'ai pu observer différents comportements.

Lorsque le domaine interne est un domaine "bidon", comme par exemple :code:`mycompany.local`, les requêtes DNS ne sont pas interceptées et le client recoit directement une réponse du serveur local. Aucun problème à ce niveau là. Par contre, lorsque le domaine de base existe, même si l'entreprise utilise un sous domaine dédié, cela créé des comportements aberrants.

Prenons l'exemple d'une entreprise qui dipose du nom de domaine public :code:`entreprise.com`. Pour ses besoins internes, l'entreprise utilise le sous domaine :code:`internal.entreprise.com`. La configuration réseau de l'ensemble des postes et des serveurs de l'entreprise spécifie l'utilisation du serveur DNS interne :code:`10.0.0.1` qui sert spécifiquement ce domaine. Avec cette configuration, l'ensemble des requêtes DNS qui traversent l'équipement Meraki est intercepté et envoyé vers Umbrella. Comme le sous domaine n'existe pas publiqueme, on se retrouve avec une réponse vide ou :code:`NXDOMAIN` pour domaine non existant.

Personnellement, j'ai mis beaucoup de temps à comprendre ce qui se passait. Je recevais bien une réponse :code:`NXDOMAIN` mais les captures de paquets m'indiquaient clairement que les requêtes n'arrivaient pas jusqu'au serveur DNS local. Jusqu'à ce que je jette un oeil au Meraki MR.
Afin d'empêcher Umbrella d'intercepter les requêtes DNS pour un domaine spécifique, il suffit de le préciser dans la configuration.
Cela se passe dans Wireless - Firewall & traffic shaping. En choisissant le bon SSID dans le menu déroulant en haut de la page, il possible de définir une liste de domaines dont les requêtes DNS ne seront pas routées vers Cisco Umbrella.

.. image:: /images/2021-03-02-22_12_36-Meraki-Umbrella.png
   :alt: Whitelist Meraki Umbrella