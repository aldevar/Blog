Monitoring 101 : Que faut-il surveiller?
########################################
:date: 2017-10-29 16:52
:author: aldevar
:category: Non classé
:slug: monitoring-101-que-surveiller
:status: draft

Introduction
============

Les métriques sont la partie la plus visible d'une architecture de supervision. Ce sont des données en général facile à récupérer et à stocker. Par conséquent, il arrive souvent qu'on n'investisse pas assez de temps dans la compréhension des données collectées, du pourquoi nous les collectons et ce que nous en faisons. Dans la manjorité des architectures de supervision, on se concentre sur la détection simple des problèmes: détecter si un evènement ou un état à eu lieu (une ligne d'erreur dans un log, un processus qui tombe). Puis, quand on reçoit la notification du problème, on se connecte sur la plateforme de supervision pour visualiser les métriques et essayer de comprendre ce qu'il se passe. Dans cette version de la supervision, les métriques sont vues comme un supplément à la detection d'erreurs.

Afin de tenter de sortir de l'ornière et utiliser pleinement les métriques comme moyen d'alerte, nous devons nous mettre d'accord sur la définition de métrique. Je vous donne donc ma version de cette définition.
Les métriques sont les mesures des propriétés d'une partie d'un logiciel ou de materiel. Pour qu'une métrique soit utile, il faut conserver une trace de son état en général en enregistrant l'observation d'une valeur à un temps donné. Une observation contient une valeur, un timestamp et parfois des propriétés (source, tag...)

Les Métriques
=============

Il y a 3 catégories de métriques. Les métriques systèmes, les métriques applicatives et les évenements. Chacune de ses catégories se traite différemment et ne sert pas le même objectif. 

Les Métriques Systèmes
----------------------

Ce sont les métriques liées à l'infrastructure servant la partie applicative. Cette infrastrcuture est composée de différentes ressources qui peuvent être de bas niveau comme le materiel physique (CPU, RAM, Disques, Réseau) ou de plus haut niveau comme une base de données qui peut aussi être considéré comme une ressource afin qu'une application puisse fournir des résultats. C'est la notion de middleware. Ces métriques peuvent être classées en 3 grandes catégories : 
- **Taux de disponiblité**: Pourcentage de temps durant lequel la ressource est capable de répondre à des requêtes.
- **Taux d'utilisation**: Pourcentage de temps durant lequel la ressource est occupée à répondre à des requêtes. 
- **Contention**: C'est la quantité de requêtes que la ressource ne peut servir car elle est occupée. Cela peut être une file d'attente, des I/O Wait...

Voici quelques exemples de métriques systèmes : 

===============  =================  ======================  ===================
Ressource        Disponibilité      Utilisation             Contention
===============  =================  ======================  ===================
Base de données  % de temps durant  % de temps durant       Nombre de requêtes
                 lequel la DB est   lequel chaque           en file d'attente
                 joignable          connection est occupée
Mémoire Vive     N/A                % de la RAM totale      Utilisation du swap
                                    utilisée
===============  =================  ======================  ===================

Les Métriques Applicatives
--------------------------

C'est ici qu'est mesurée l'experience utilisateur ainsi que la santé global du service. 
