Ajouter Duckduckgo comme moteur de recherche dans SailfishOS
############################################################
:date: 2015-08-20 22:10
:author: Aldevar
:category: Tech
:slug: ajouter-duckduckgo-comme-moteur-de-recherche-dans-sailfishos
:status: published

Par défaut, le navigateur de SailfishOS propose Bing, Yahoo ou Google
comme moteur de recherche et il n'y a pas d'interface pour ajouter de
nouveaux moteurs de recherche.

Je vous propose ici une méthode pour ajouter un nouveau moteur de
recherche dans cette liste. Ici ce sera
`Duckduckgo <https://duckduckgo.com/>`__

La manipulation consiste à ajouter un fichier de description du moteur
de recherche dans le répertoire adéquat.

La première étape est d'activer le mode développeur et de se connecter
en SSH à son Jolla. Si vous ne savez pas comment vous y prendre, vous
pouvez `suivre ce
tuto <http://blog.devarieux.net/2015/03/se-connecter-en-ssh-a-son-jolla/>`__

Une fois connecté en SSH, se connecter en root :

::

    [nemo@Jolla ~]$ devel-su

Se rendre dans /usr/lib/mozembedlite/chrome/embedlite/content/

::

    [root@Jolla nemo]# cd /usr/lib/mozembedlite/chrome/embedlite/content/

Créer un fichier duckduckgo.xml

::

    [root@Jolla nemo]# vi duckduckgo.xml

Coller le contenu de ce fichier :
`duckduckgo.xml <http://blog.devarieux.net/wp-content/uploads/2015/08/duckduckgo.xml>`__

Ou plus simplement

::

    [root@Jolla content]# curl  http://blog.devarieux.net/wp-content/uploads/2015/08/duckduckgo.xml -o duckduckgo.xml

Il ne reste plus qu'à fermer se rendre sur le téléphone, fermer
l'application 'Réglages', la relancer, se rendre dans 'Application' >
'Navigateur' et choisir le moteur de recherche Duckduckgo.

Enjoy!

.. image:: {static}/images/20150820220621-169x300.jpg
  :target: /images/20150820220621.jpg


