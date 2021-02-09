Rapport de stage sur la mise en place de Squid et Egroupware
############################################################
:date: 2010-01-06 15:05
:author: alain
:category: Tech
:slug: rapport-de-stage-sur-la-mise-en-place-de-squid-et-egroupware
:status: published

J’ai longuement hésité à mettre ce rapport de stage en ligne pour
plusieurs raisons. Tout d’abord, ce rapport n’est pas vraiment
représentatif du travail fournit. La majorité des solutions expliquées
m’ont demandées beaucoup de temps de recherche et d’arrachage de cheveux
(notamment pour la migration des comptes sous Lotus Notes). Ensuite, la
qualité rédactionnel est loin d’être au rendez-vous. On m’a beaucoup
reproché que ce rapport était trop technique et c’est plutôt vrai.
Enfin, ce document ne décrit pas vraiment l’installation de Squid et
d’Egroupware. Ces parties sont survolées et je m’attarde plus sur la
résolution des problèmes rencontrés (résoudre un conflit de schéma LDAP
quand on a jamais vu OpenLDAP de sa vie n’est pas chose aisée).

Un mois après la fin de la formation, je me décide tout de même à le
mettre en ligne. Je pense que ce rapport décrit plutôt bien ce que peut
être le métier de technicien réseau dans une administration ou une PME.
Le problème lors de la mise en place d’un nouveau service n’est pas
l’installation et la configuration de ce service mais la migration des
anciens services utilisés vers les nouveaux. Surtout lorsque l’ancien
service est un système propriétaire vieillissant (Je veux parler ici de
Lotus Notes 5).

`Squid <https://web.archive.org/web/20110722200015/http://www.squid-cache.org/>`__
est un proxy http très utilisé, dont j’ai pu découvrir une partie des
possibilités.
`Egroupware <https://web.archive.org/web/20110722200015/http://www.egroupware.org/>`__
est un groupware fournissant un agenda, un client mail, un carnet
d’adresses, un système de réservations des ressources et plusieurs
autres choses, le tout dans une interface web. Je vous invite à tester
la `demo sur le site du
projet. <https://web.archive.org/web/20110722200015/http://www.stylite.de/egroupware_demo_login>`__

Ce rapport fait 38 pages et voici son sommaire:

#. **Remerciements**
#. **Objectif du stage**
#. **L’entreprise**

   #. Historique
   #. La structure actuelle
   #. Le service informatique

#. **Spécifications**

   #. Environnement de travail
   #. L’existant
   #. Besoins et contraintes

      #. *Squid*
      #. *Egroupware*

#. **Mise en œuvre**

   #. Proxy

      #. *Planning prévisionnel*
      #. *Mise en œuvre*

         #. Squid
         #. Sarg
         #. Squidguard

      #. *Problèmes rencontrés*
      #. *Annexes*

   #. eGroupware

      #. *Schéma fonctionnel*
      #. *Planning previsionnel*
      #. *Mise en œuvre*

         #. Configuration de openldap

      #. *Problèmes rencontrés*

         #. Conflit de schéma openldap
         #. Configuration de felamimail

      #. *Préparation de la migration des utilisateurs*

         #. Création du carnet d’adresses principal
         #. Importation des agendas Lotus Notes
         #. Importation des carnet d’adresse Lotus Notes
         #. Exportation des mails depuis LotusNotes dans eGroupware
         #. Importation mail depuis roundcube

      #. *Annexes*

#. **Procédure de migration serveur**

   #. Sur Revy
   #. Sur Revnew

`RapportDeStage-Squid-Egroupware <http://blog.devarieux.net/wp-content/uploads/2015/08/RapportDeStage-Squid-Egroupware.pdf>`__
