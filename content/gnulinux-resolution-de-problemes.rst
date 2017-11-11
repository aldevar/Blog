GNU/Linux : Résolution de problèmes
###################################
:date: 2009-12-25 19:34
:author: alain
:category: Tech
:tags: aide, GNU, Linux, probleme
:slug: gnulinux-resolution-de-problemes
:status: published

Une grande partie du travail sur les forums concernant les logiciels
libres est d'obtenir plus d'informations sur les problèmes des novices.
Il est très agréable d'aider les autres comme il peut être assez agaçant
d'essayer d'aider quelqu'un qui ne montre aucun effort pour s'aider
lui-même. Je ne pense pas que cela soit dû à de la fainéantise de la
part de celui qui pose la question. C'est simplement parce que les
novices ne connaissent pas les premières étapes de résolution des
problèmes sur GNU/Linux et ne savent pas quels types d'informations
rechercher ni comment les obtenir. J'espère que ce petit guide sera
utile pour ceux qui font leurs premiers pas sur linux.

I - Diagnostiquer soi-même
--------------------------

1 - La première étape est la collecte d'informations.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si un programme plante ou ne fait pas ce qu'il est censé faire, il faut
se poser et réfléchir calmement.

Ouvrez un nouveau fichier dans votre éditeur de texte favori et
écrivez-y ce que vous faisiez quand le problème est apparu ainsi que
tous les messages d'erreurs reçus. Ces messages d'erreurs doivent être
recopiés exactement tel qu'ils sont apparus. Utilisez le copier/coller
si cela est possible.

Ouvrez un terminal et tapez **tail /var/log/messages**. Cette commande
affichera les 10 dernières lignes des logs du système. Si celui ci
contient un ou des messages qui sont clairement en rapport avec votre
problème, recopiez les également.

Les erreurs des applications graphiques sont en général dans le fichier
.Xsession-errors ou .xsession-errors dans votre dossier /home. La
commande pour visualiser les 10 dernières lignes est donc **tail
~/.xsession-errors**. Comme pour le fichier /var/log/messages, ajoutez
les lignes en rapport avec votre problème dans votre fichier de départ.
Si vous n'avez trouvé aucune information dans ces fichiers, essayez de
lancer l'application concernée depuis votre terminal. Lors de
l'apparition du bug, des messages devraient s'afficher.

Si votre système ne démarre plus suite à un problème, démarrez alors sur
une autre distribution (soit en dual-boot si vous en avez soit depuis un
live-cd). Il est toujours bon d'avoir un live-cd sous la main pour ce
genre d'opération. Une fois que vous avez démarré sur le live-cd, montez
votre partition root et récupérez les informations dans les fichiers
cités plus haut.

2 - Le problème est-il reproductible?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

S'il est possible de reproduire le problème facilement, faites-le.
N'oubliez pas de le faire sur des fichiers peu important ou sur une
copie du fichier concerné afin de ne pas endommager vos données.

3 - Est-ce un problème matériel ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les problèmes non reproductibles sont souvent dus au matériel. Si vous
pensez que c'est le cas, regardez alors dans le fichier
**/var/log/boot** ainsi que **/var/log/kern.log** ou
**/var/log/kernel.log** suivant votre distribution pour voir si le
kernel reconnait bien votre matériel. Ce fichier étant très long, la
commande tail ne vous sera pas d'un grand secours. Utilisez plutôt
**less /var/log/boot**\ et parcourez les pages à la recherche d'un
message en rapport avec votre problème. Recopiez également ce message
dans votre fichier de départ.

4 - Lisez la documentation du programme.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ceci est à faire en particulier si le programme ne réagit pas de la
manière souhaitée. Lisez l'aide en ligne du programme et utilisez
également le manuel universel (dans un terminal : man
nom\_du\_programme).

5 - Recherchez votre message d'erreur sur internet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copiez/collez le message d'erreur dans un moteur de recherche ou un
meta-moteur tel que ixquick et ajoutez-y le nom du programme. Vous
trouverez certainement des messages sur des forums d'utilisateurs qui
ont le même problème que vous. Lisez le thread complet, vous y trouverez
peut-être une solution.

6 - Réfléchissez avec logique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si, arrivé ici, vous commencez à avoir une idée sur la cause du
problème, vous pouvez peut être tester cette idée. Il y a beaucoup de
petites commandes simples qui peuvent vous aider à recueillir plus
d'informations sur votre problème et votre système, qui vont seront d'un
grand secours.

-  **lspci** pour lister votre matériel
-  **lsusb** pour lister les périphériques usb
-  **cat /proc/cpuinfo** pour avoir les caractéristiques de votre CPU
-  **free -m** pour connaitre le taux de charge de votre RAM

7 - Maintenant, vous pouvez penser à demander de l'aide.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si après tout ça, vous n'avez toujours pas résolu votre problème, il est
temps de demander de l'aide sur un forum d'utilisateurs. Avant de passer
à cette étape, rappelez vous que les utilisateurs des forums ne sont pas
payés pour répondre à vos questions. Ce sont seulement des utilisateurs
ayant une certaine expérience et qui font cela bénévolement.

II - Obtenir de l'aide
----------------------

1 - D'abord, observer
~~~~~~~~~~~~~~~~~~~~~

Commencez par choisir votre forum. Il est préférable dans un premier
temps de choisir le forum de votre distribution, puis le forum du
programme concerné. Si ce forum possède une FAQ, lisez-la. Lisez aussi
les règles du forum. Si votre question ne respecte pas les règles, il y
a de grandes chances pour que vous n'obteniez pas de réponse.

2 - Ne soyez pas hors-sujet
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trouvez le sous-forum qui correspond à votre problème. Ne postez pas
votre message dans plusieurs sous-forums, ceci est très mal vu.

3 - Choisissez bien le titre de votre topic.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

N'utilisez pas de sujet tel que "Besoin d'aide" ou "J'ai un problème".
Ceci a tendance à irriter les gens.

Votre titre doit indiquer le plus clairement quel problème vous avez.
Ainsi, une personne qui pense pouvoir vous aider sera plus encline à
lire votre sujet et poster une réponse. Soyez aussi précis que possible.
Par exemple "Impossible d'obtenir une adresse IP" sera plus utile que
"Je n'arrive pas à aller sur internet".

4 - Donnez des informations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans le corps de votre message, donnez le nom et la version de votre
distribution, le nom et la version du programme utilisé et les
informations sur votre matériel si cela est nécessaire. Recopiez-y aussi
les messages d'erreurs (c'est là que le fichier que vous avez créé au
début devient utile). Indiquez ce que vous avez fait pour tenter de
résoudre le problème. En faisant cela, vous montrerez aux autres que
vous ne vous êtes pas jeté sur le forum dès que le problème est apparu.

5 - Pas de langage SMS
~~~~~~~~~~~~~~~~~~~~~~

Ça saoule! Ça n'aide pas à vous faire comprendre et on vous répondra
d'autant moins.

6 - Ne perdez pas une opportunité d'apprendre
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ne suivez pas les conseils aveuglément. Vous êtes ici pour apprendre
quelque chose. Si on vous demande d'utiliser un outil en ligne de
commande, utilisez les pages man pour savoir à quoi sert cet outil. Vous
pourrez ensuite réutiliser cet outil si vous rencontrez un problème
similaire. Si on vous demande de poster un fichier pour plus
d'informations, recherchez l'utilité de ce fichier. Les fichiers
systèmes importants possèdent souvent une page man dédiée.

7 - Dites merci
~~~~~~~~~~~~~~~

Les logiciels libres reposent sur la communauté. Personne n'est payé
pour vous aider. Les personnes qui vous aident le font car elles ont
elles-mêmes reçu de l'aide dans le passé et veulent rendre la pareille.
En plus de dire merci, vous pouvez également aider les autres qui ne
savent peut-être pas quelque chose que vous savez. Vous ressentirez
alors une certaine satisfaction que les logiciels propriétaires ne
peuvent vous apporter.
