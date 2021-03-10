Migrer des règles de NAT VyOS vers NSX-V
########################################
:date: 2021-02-10 09:22
:author: Aldevar
:category: automatisation
:tags: automatisation, python, vyos, nsx, reseau
:slug: migrate-nat-vyos-nsxv
:status: published

Il y a quelques temps, j'ai procédé une modification majeure de l'architecture BGP d'un hébergeur. Cette modification imposait de transposer les règles de NAT présentent sur les routeurs BGP VyOS vers les routeurs NSX-V, plus proche du coeur de réseau.
Il y avait environ 400 règles de NAT à transposer. Ceux qui ont déjà fait du NAT sur NSX savent que réaliser ce genre de manipulation manuellement n'est pas une sinécure. L'interface n'est clairement pas adaptée pour ce genre de tâche. Par contre, NSX dispose d'une API plutot bien documentée.
De l'autre coté, VyOS. VyOS est un système d'exploitation réseau, basé sur Debian avec des commandes similaires à ce qu'on peut trouver sur un routeur. 

En discutant avec `Daniil Baturin <https://baturin.org/>`__, principal mainteneur de VyOS, sur la meilleur façon de procéder, celui ci m'a indiqué la `lib configtree <https://github.com/vyos/vyos-1x/blob/current/python/vyos/configtree.py>`__ qui permet de manipuler un fichier de configuration VyOS. Avec l'aide de cette lib, j'ai pu écrire ce script Python qui lit le fichier vyos.conf préalablement récupéré par mes soins et génére puis pousse les règles de NAT vers NSX-V.

.. include:: extra/Migration_NSX_to_vyos.py
