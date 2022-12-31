Debian abandonne la Linux Standard Base
#######################################
:date: 2015-10-20 21:56
:author: Aldevar
:category: None
:slug: debian-abandonne-la-linux-standard-base
:status: published

`LWN a annoncé <https://lwn.net/Articles/658809/>`__ il y a déjà
quelques jours que la communauté Debian abandonnait le support de la
`Linux Standard Base <http://refspecs.linuxfoundation.org/lsb.shtml>`__
(LSB). La LSB tente de se définir comme un standard de compatibilité des
différentes distributions. En suivant ces règles, chaque binaire devrait
simplement fonctionner sur chaque distribution, que ce soit Debian, RHEL
ou SLES.

Difficile d'en vouloir aux mainteneurs Debian. La LSB est très vaste et
`très peu
d'applications <https://www.linuxbase.org/lsb-cert/productdir.php?by_lsb>`__\ ont
reçu la certification LSB. Ajoutez à cela que le gestionnaire de paquet
RPM est celui qui a été choisi et vous avez un standard dont les specs
vont à l'encontre de ce que propose Debian.

Le fait que Debian stoppe les efforts pour rester compatible avec LSB ne
signifie pas forcement qu'elle va devenir incompatible avec les autres
distributions. Debian prévoie de rester compatible avec le standard de
hiérarchie des systèmes de fichiers (`Filesystem Hierarchy
Standard <http://www.linuxfoundation.org/collaborate/workgroups/lsb/fhs>`__),
un des éléments de LSB qui défini où doivent se trouver certains
fichiers et répertoires. C'est en effet un des standard majeur pour
conserver un semblant de compatibilité entre distributions.

Sur le court terme, cela ressemble à un non événement. A plus long
terme, on peut se demander ce qu'il va advenir de l'écosystème Linux.
Créer une distribution et la maintenir est déjà une tâche
particulièrement difficile.Imaginez alors ce que cela doit être de
coordonner des standards a travers plusieurs distributions ...

Parmi les distributions majeures, nous avons typiquement 2 camps:
Debian/Ubuntu et Fedora/RHEL. Ces 2 camps ont réussi à ne pas trop
s'éloigner l'un de l'autre et on peut penser que systemd avait commencé
ce processus de coordination. Les normes sont importantes, mais
seulement dans la mesure où elles sont respectées. Jusqu'ici GNU/Linux a
évité le problème `des normes concurrentes <https://xkcd.com/927/>`__.

Cela va-t-il rester le cas?
