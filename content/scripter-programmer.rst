Scripter, programmer
####################
:date: 2015-09-25 07:14
:author: alain
:category: humeur
:slug: scripter-programmer
:status: published

Il y a quelques mois, `Jon Hudson <https://twitter.com/_Desmoden>`__,
ingénieur réseau chez Brocade, a présenté un discours très intéressant
au `Network Field Day 9 <http://techfieldday.com/event/nfd9>`__ sur le
sujet de la programmabilité en réseau.

Durant la conversation (qui vaut vraiment le coup d'être vu), une
question de John Herbert de
`MovingPackets.net <http://movingpackets.net/>`__ a été posée : "*Les
ingénieurs réseaux deviendront-ils des programmeurs?*\ ". La réponse de
Jon Hudson a suscité les applaudissements de l'audience :

    "Le problème que j'ai avec cette affirmation est que la majorité des
    ingénieurs réseaux que je connais, moi y compris, savent comment
    coder. Nous avons fait des études dans ce domaine et nous avons
    choisi de ne pas le faire." – Jon Hudson

    “The trouble I have with that statement is, most network engineers I
    know, like myself, we know how to code. We went to school for it,
    and we chose not to.” – Jon Hudson

Il ne faut pas oublier en effet qu'il y a une différence fondamentale
entre scripter, écrire des outils d'administration et programmer.

Le script, c'est le petit programme qu'on écrit à l'école pour
s’entraîner. *"Calculer les années bissextile pour les 300 prochaines
années"*, ou *"Parcourir les lignes de ce fichier et effectuer X
traitements sur cette ligne"*. C'est fun, souvent pratique, mentalement
stimulant et facile à réutiliser. Il résout un problème spécifique et
peu facilement être dupliqué ou modifié pour résoudre un autre problème.
Par contre la plupart de ces scripts sont fragiles, peu efficaces et
souvent non sécurisés.

Je ne suis pas du tout développeur mais du peu que je sache, écrire un
programme, pour moi, ça ressemble à: *"La fonction recevra en entrée un
pointeur vers un vecteur contenant une valeur qui doit être validée par
rapport au contenu du dictionnaire. Chaque exception durant l’exécution
de la routine doit être gérée. La fonction doit retourner un pointeur à
la fonction appelante qui va référencer un nouveau vecteur contenant la
valeur calculée de l'espace de nom de la fonction appelée. Documenter le
code en détail et démontrer que le code rédigé s’exécute en utilisant le
moins de demande d'allocation mémoire."*

Ce que je viens d'écrire est sans doute un ramassis de n'importe quoi
mais c'est environ a ce niveau là que je décroche de la programmation et
que mon intérêt pour cette compétence se réduit à peau de chagrin. Il me
semble que le scripting et la programmation sont 2 choses bien
différentes que certaines personnes ont tendance à mélanger.

Ainsi, quand on nous assène qu'en tant que sysadmin ou ingé / technicien
réseau on DOIT savoir coder, je suis plutôt d'accord, surtout à l'heure
du Software Define Network, Software Define Storage ou plus globalement
du Software Define Datacenter et de l'hyperconvergence des
infrastructures. On pourra toujours tout faire à la main, que ce soit en
ligne de commande ou via une GUI, mais quand on travail dans un système
distribué possédant des APIs, il est bien plus facile d'utiliser un
script (qui a dit Python?) ou des outils comme Puppet/Ansible/Salt.
Attention cependant à la sémantique. Coder (écrire du code) ce n'est pas
la même chose que programmer (écrire un programme).

Il est important, quand on travail dans l'IT, de savoir scripter. Il y a
plein de tâches répétitives, ennuyeuses qu'on souhaite automatiser au
maximum. Il y aussi plein d'autres tâches plus rapide à faire à la main
et parfois difficile à automatiser. Pour résumer, construisez votre
script quand celui ci vous permet de faire votre tâche plus vite, mieux
et moins cher tout en évitant que le code soit instaurer comme nouvelle
religion de l'IT. Si vous avez besoin d'une scie, utilisez une scie. Si
vous avez besoin d'une scie sauteuse pour mieux scier, construisez votre
scie sauteuse mais faite attention de ne pas devenir un constructeur de
scie sauteuse qui a oublié comment scier.

 
