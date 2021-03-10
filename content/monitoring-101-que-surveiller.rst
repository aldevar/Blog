Monitoring 101 : Que faut-il surveiller?
########################################
:date: 2017-11-12 16:52
:author: aldevar
:category: sysadmin
:slug: monitoring-101-que-surveiller
:status: published

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

|
|

Les Métriques Applicatives
--------------------------

C'est ici qu'est mesurée l'experience utilisateur ainsi que la santé global du service. Comme pour les métriques système, elles sont classées en plusieurs catégories.

- **Performance**: Cette métrique quantifie l'efficacité d'un composant. La métrique de performance la plus commune est la latence, qui représente le temps nécessaire pour accomplir une tâche. Il y a plusieurs façon d'exprimer cette métrique. On peut en faire une moyenne ou utiliser les percentiles, du type "99% des requêtes ont reçu une réponse en moins de 0.2 secondes".

- **Debit**: ou également **entrées sorties**. C'est la quantité de requêtes traitée par unité de temps. Par exemple, un nombre de pages affichées par seconde.

- **Succès**: C'est le pourcentage d'entrées sorties traitées dont l'execution s'est bien déroulée. Par exemple, le nombre de code HTTP 2XX.

- **Echec**: A l'inverse, le pourcentage d'entrée sorties traitées dont l'execution s'est mal déroulée. Par exemple, le nombre de code HTTP 5XX.

Ces métriques permettent de rapidement répondre aux questions qui intéressent les utilisateurs finaux du service. Le service est-il disponible et remplit-il sa mission? A quelle vitesse le fait-il? Avec quelles résultats?

Voici quelques exemples de métriques applicatives pour un service web:

=========== ======================================= =======
Catégorie   Description                             Valeur
=========== ======================================= =======
Performance 99ème percentil du temps de réponse (s) 0.3
Débit       Requêtes par seconde                    220
Succès      Pourcentage de code retour HTTP 2XX     99.5
Echec       Pourcentage de code retour HTTP 5XX     0.2
=========== ======================================= =======

|
|

Les Evenements
--------------

En plus des métriques systèmes et applicatives, il y a certaine information qu'on souhaite récupérer de façon plus sporadique. Certains systèmes permettent de superviser des évenements. Les évenements n'ont pas lieu de façon fréquentes et il est souvent difficile voir impossible de les prévoir. 

- Tâche planifiée en échec

- Virus détecté dans un système de fichier

- Trap SNMP

Contrairement aux métriques qui doivent être analysées dans leur context, les évenements contiennent en général en eux-même suffisamment d'informations pour être directement interprétés. 

Conclusion
----------

Dans le doute, ne pas hésiter à collecter les données. Sachant que ces données doivent être **bien comprises** (je sais ce que cette donnée signifie), avoir une **granularité** adequat (si la granularité est trop large, je perds en précision; si la granularité est trop fine je risque d'impacter le système que je supervise) et être **conservée suffisamment** longtemps pour comprendre quels sont les comportements normaux et anormaux.

