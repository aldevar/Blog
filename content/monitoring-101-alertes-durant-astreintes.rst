Monitoring 101 : Les alertes durant les astreintes
##################################################
:date: 2017-10-29 19:30
:author: alain
:category: sysadmin
:slug: monitoring-101-alertes-durant-astreintes
:status: published

Introduction
============

Après avoir déployé un système de supervision dans une infrastructure de
taille moyenne et avoir passé quelques temps en rotation dans une équipe
d'astreinte, j'ai tiré un certains nombre de conclusions sur ce que
devrait être la supervision et surtout les alertes qui doivent être
levées lors des astreintes. L'écriture et l'audit de règles d'alertes
doivent respecter certains principes afin que les astreintes se
déroulent le plus sereinement possible:

-  Une alerte envoyée en astreinte doit être urgente, réelle et
   concrète. C'est à dire qu'il doit être possible d'intervenir pour
   corriger le problème.
-  Une alerte doit être levée pour des problèmes imminent ou en cours.
-  Ne pas hésiter à supprimer les alertes générant du bruit. L'excès de
   supervision nuit à la supervision.
-  La meilleur façon de comprendre un problème est d'alerter sur ses
   symptômes.
-  Corollaire : Eviter d'alerter directement sur les causes.

Avant de détailler un peu plus ces principes, voici les 3 règles majeurs
qui, à mon sens, doivent servir de guide:

-  A chaque fois que je reçois une alerte, **je dois la considérer comme
   urgente** et agir comme tel. Je ne peux agir comme ça trop souvent
   avant de ressentir une lassitude.
-  **Chaque alerte doit être concrète**. Je dois pouvoir réaliser une
   action pour la corriger.
-  Chaque action sur alerte doit se faire avec un certain **niveau
   d'expertise**. Si le problème peut être traité par un script, alors
   je n'aurais pas du être dérangé.

Vu comme ça, c'est un peu ambitieux mais ces règles doivent avant tout
servir de guides pour l'écriture et la revue des alertes. Voici quelques
questions qu'on peut se poser lors de l'écriture d'une nouvelle règle:

-  Cette nouvelle règle ne vient-elle pas surcharger une règle déjà
   existante qui est elle-même urgente, concrète et impactante.
-  Vais-je un jour ignorer cette alerte sachant qu'elle est bénigne?
   Puis-je affiner cette règle pour éviter cette situation?
-  Cette alerte se lève-t-elle pour une condition qui va réellement
   impacter les utilisateurs?
-  Il y a-t-il des actions à mener en réponse à cette alerte? Cette
   action doit-elle être réalisée tout de suite ou peut-elle attendre
   demain matin, ou lundi, ou le trimestre prochain?

Evidemment, aucun système d'alerte dans une infrastructure croissante et
changeante n'est aussi parfait que celui que je viens de décrire mais ce
sont quelques règles qui permettent de s'en approcher autant que
possible.

Avoir une vue utilisateurs
==========================

C'est ce que qu'on appelle la "**supervision des symptômes**\ ", opposée
à la "**supervision des causes**\ ". Un petit exemple afin de préciser
le propos : vos utilisateurs se soucient-ils de savoir si votre serveur
SQL est down? Non, ils s'inquiètent si leur requêtes sont en échecs (je
vous entends déjà pleurer sur vos petits check 'SQL Server' Nagios).

En général, les utilisateurs se soucient d'un petit nombre d’éléments:

-  **Disponibilité**. Pas d'erreur 500, de requête en attente, de pages
   a moitié chargées. Un service qui ne fonctionne pas pleinement doit
   être considéré comme un service non disponible.
-  **Latence.** ça doit aller vite!
-  **Exactitude des données**. Les données doivent être en sécurité.
   Elles doivent aussi être à jour.
-  **Fonctionnalités.**\ Le service doit fournir toutes ses
   fonctionnalités, même si ce n'est pas une fonction principale du
   service. Par exemple, l'auto-complétion dans un champ de recherche.

C'est à peu prêt tout.

La différence entre un serveur de base de données *down* et des données
utilisateurs non disponible est très importante. La première est une
cause, la seconde est un symptôme et l’indisponibilité des données peu
provenir de plusieurs choses. On peut avoir un problème d'I/O ou de CPU
sur le serveur de BDD, rendant les temps de réponses trop long. Vous
n'allez pas pour autant lever une alerte chaque fois que le CPU est à
100% ou chaque fois que l'I/O Wait monte à 60%. Avoir une vue
utilisateur permet de directement savoir si un problème nécessite une
intervention.

Alerter sur les causes, c'est nul! (mais parfois, on n'a pas le choix)
======================================================================

On sait bien que si le serveur de BDD est down les utilisateurs n'auront
pas accès à leur données et il est très tentant de superviser juste le
serveur de BDD et d'ajouter une supervision sur la bonne connexion du
service à la BDD. Ceci pose d'autres problèmes :

-  Il faudra de toute façon vérifier les symptômes. Peut être avons nous
   des déconnexions réseaux intempestives, de la contention sur le CPU
   ou sur les performances du stockages (qui a dit backup en cours?) ou
   une tonnes d'autres problèmes auxquels on ne pense pas. On doit donc
   vérifier les symptômes.
-  Si on attrape les symptômes et les causes, on se retrouve avec une
   redondance des alertes et on a donc soit de la duplication d'alerte
   soit la mise en place d'un système de dépendances entre les alertes
   qui ajoute de la complexité.
-  Peut être qu'un cluster de base de données a été créé et qu'on ne se
   soucie plus de savoir qu'un serveur est tombé.

Mais il est vrai que parfois, les alertes sur les causes sont
nécessaires. Par exemple, en général, il n'y a pas de symptômes sur des
problèmes d'espace disque plein à 95% et il est pourtant nécessaire
d'agir avant qu'un manque d'espace ne vienne perturber le service. Ce
type d'alerte est à utiliser avec parcimonie.

Des tickets, des emails...
==========================

Qu'on le veuille ou non, on se retrouve toujours avec des alertes qu'on
peut qualifier de non critique. Elles méritent qu'on s'en occupe, mais
pas forcement maintenant. 

-  Dans ce cas, l'ouverture d'un ticket peut-être utile. Votre
   plateforme du supervision ouvre un ticket que vous pourrez traiter
   lorsque vous aurez plus de temps (après la nuit par exemple).
-  Chaque alerte devrait automatiquement être tracée quelque part. Par
   seulement les envoyer par e-mail, sur un canal IRC ou dans un canal
   Slack. En général, ce type d'envoie permet juste de mieux ignorer les
   alertes.

Le point soulevé ici est qu'il est important de créer un système
d'astreinte qui limite la lassitude, responsabilise sur la réactivité et
qui ne va pas trop régulièrement réveiller la personne d'astreinte,
l'interrompre dans son dîner ou l'empêcher de passer du temps avec sa
famille.

Procédure
=========

Il est préférable d'avoir une documentation dédiée pour chaque alerte ou
famille d'alerte qui est susceptible d'être levée. Cette documentation
doit expliquer ce que signifie l'alerte et comment elle peut être
résolue.

Cette documentation ne doit pas être un long pavé expliquant toute
l'architecture en long et en large. Elle doit expliquer brièvement les
points à vérifier et les différentes actions à mener.

Inversement, la documentation ne doit pas être une simple commande à
taper ou une action simpliste à réaliser. Cela signifierai que l'action
de correction est scriptable et n'aurait pas du déranger la personne
d'astreinte. L'alerte devrait être levée si l’exécution du script ne
corrige pas le problème et nécessite alors une intervention humaine.

 

Ne soyez pas naïf!
==================

Voici quelques bonnes raisons de ne pas respecter ces règles : 

-  **Vous avez une cause connue qui fait qu'un service répond de façon
   aléatoire**. Dans ce cas, alerter sur un les symptômes ne sera pas
   d'une grande aide et il est plus simple d'alerter sur la cause.
-  **Les symptômes apparaissent quand c'est déjà trop tard**, par
   exemple quand il n'y a plus d'espace disque.
-  **Le système d'alerte semble être plus complexe que le problème qu'il
   tente de détecter**. Le but est de tendre vers plus de simplicité,
   plus de robustesse et des système auto-réparant. Avant d'atteindre
   cet objectif sur le moyen terme, il est possible qu'il soit plus
   efficace d'avoir un système d'alerte complexe mais qui soit fiable et
   ne lève pas trop de faux positifs.

