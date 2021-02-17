Cisco Hyperflex - Supprimer la configuration réseau de réplication
###################################################################
:date: 2021-02-03 21:40
:author: Aldevar
:category: Tech
:tags: hyperflex, cisco
:slug: reset-hyperflex-replication-network
:status: published

Cette semaine, j'ai pris le temps de jouer avec une instance de demo Cisco Hyperflex sur `dcloud.cisco.com <https://dcloud.cisco.com/>`_. Cette demo permet de jouer un peu avec deux instances Hyperflex et notamment de mettre en place un PRA entre ces deux instances.
Pour mettre en oeuvre ce PRA, il faut au préalable configurer un réseau de réplication (Replication Network) qui doit permettre aux clusters Hyperflex de communiquer entre eux et transférer les données. Malheureusement, par inattention, j'ai fait une erreur lors de la configuration de ce réseau. J'ai paramétré une mauvaise adresse de réseau et une mauvaise gateway et la réplication refusait de fonctionner. 

Cette erreur de configuration m'a posé plus de problèmes que ce que je pensais car il n'est pas possible de reconfigurer ce réseau une fois qu'il est enregistré... Cela est indiqué noir sur blanc dans la `documenation Cisco Hyperflex <https://www.cisco.com/c/en/us/td/docs/hyperconverged_systems/HyperFlex_HX_DataPlatformSoftware/AdminGuide/2_5/b_HyperFlexSystems_AdministrationGuide_2_5/b_HyperFlexSystems_AdministrationGuide_2_5_chapter_01111.html#task_agm_yqs_m1b>`__.

Ce problème ne peut pas se régler par l'interface graphique. Il faut passer par la ligne de commande, directement sur le cluster. Ces commandes doivent être exécutées sur une des controller VM du cluster.
Le première commande permet de supprimer un appairage déjà existant entre 2 cluster. La suivante supprime effectivement la confguration du réseau de réplication.

.. code-block:: bash

    stcli dp peer forget --all
    stcli drnetwork cleanup

Une fois ces commandes executées, on peut de nouveau configurer le réseau de réplication.

.. image:: /images/drnetwork.png
   :alt: Hyperflex Replication Network
