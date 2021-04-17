Pilotage de Caddy par API
###########################
:date: 2021-02-21 00:23
:author: Aldevar
:category: web
:tags: caddy, web, automatisation
:slug: caddy-api
:status: published

Comme promis dans l'article précédent sur Caddy, je vais parler de l'utilisation de l'API de Caddy. Un prochain article décrira comment générer un certificat wildcard pour un domaine hébergé chez OVH. 

En plus de permettre de lire la configuration, l'API de Caddy permet aussi d'en pousser une nouvelle, en totalité ou en partie. L'avantage est que, si la configuration envoyée est valide, celle ci est chargée à chaud et sinon un code retour autre que 200 est renvoyé, précisant l'erreur rencontrée.

Attention au mode d'execution du service Caddy lorsqu'on commence à le configurer par API. Il est nécessaire d'utiliser le fichier de service décrit `dans la documentation <https://caddyserver.com/docs/install#linux-service>`_. Sans cela, les modifications apportées seront perdues au prochain redémarrage du service. 

L'API est disponible par defaut seulement sur la boucle locale, port 2019. On peut déjà commencer par visualiser la configuration avant de commencer à en pousser une nouvelle.

.. code-block:: text

    curl http://localhost:2019/config/ | python3 -m json.tool

Le pipe vers la commande python permet d'obtenir directement un affichage json en mode pretty print.

Pousser une configuration complète
====================================

La configuration à envoyer vers Caddy est préparée dans un fichier, qu'on va appeler :code:`config.json`. Ce fichier sera ensuite envoyé en tant que payload dans l'appel API.

Première configuration simple avec un reverse proxy.

.. code-block:: json

    {
    "apps": {
        "http": {
            "servers": {
                "srv0": {
                    "listen": [
                        ":443"
                    ],
                    "routes": [
                        {
                            "handle": [
                                {
                                    "handler": "reverse_proxy",
                                    "upstreams": [
                                        {
                                            "dial": "10.0.0.1:80"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    }


Avec cette configuration, on a la génération du certificat TLS via Let's Encrypt ainsi que la redirection HTTP vers HTTPS. On pousse cette configuration avec la commande suivante :

.. code-block:: text

    curl 127.0.0.1:2019/load -X POST -H "Content-Type: application/json" -d @config.json

Passons maintenant à l'étape suivante. Nous allons ajouter plusieurs éléments de configuration

.. code-block:: json

    {
    "admin": {
        "listen": "127.0.0.1:2019"
    },
    "apps": {
        "http": {
            "servers": {
                "srv0": {
                    "listen": [
                        ":443"
                    ],
                    "routes": [
                        {
                            "handle": [
                                {
                                    "handler": "reverse_proxy",
                                    "transport": {
                                        "protocol": "http",
                                        "tls": {}
                                    },
                                    "upstreams": [
                                        {
                                            "dial": "10.0.0.1:443"
                                        }
                                    ]
                                }
                            ],
                            "match": [
                                {
                                    "host": [
                                        "sub.domain.com"
                                    ]
                                }
                            ]
                        },

                    ],
                    "tls_connection_policies": [
                        {
                            "certificate_selection": {
                                "any_tag": [
                                    "companycert"
                                ]
                            }
                        }
                    ]
                }
            }
        },
        "tls": {
            "certificates": {
                "load_files": [
                    {
                        "certificate": "/etc/pki/tls/certs/companycert.crt",
                        "key": "/etc/pki/tls/private/companycert.key",
                        "tags": [
                            "companycert"
                        ]
                    }
                ]
            }
        }
    }
    }

Qu'avons nous exactement? 
Premièrement, nous créons une route qui utilise un handle. Un handle est un processus de Caddy qui permet d'activer certaines fonctionnalités spécifiques. Ici nous utilisons le handle :code:`reverse_proxy` mais il y en a `bien d'autres <https://caddyserver.com/docs/json/apps/http/servers/routes/handle/>`_.

Ensuite, avec la directive :code:`"upstream" "dial"`, on spécifie le serveur de backend à utiliser. En précisant :code:`:443`, on force le reverse proxy à se connecter au backend en HTTPS.

Puis la directive :code:`"match" "host"` permet de répondre aux requêtes destinées à :code:`sub.domain.com`. 

On termine enfin avec la configuration TLS. D'une part, on indique la politique TLS du serveur "srv0". La possibilitée d'utiliser des tags est assez pratique pour ne pas avoir à répéter les chemins des certificats lorsqu'on utilise plusieurs éléments "server" dans la même configuration. Il est même possible de spécifier plusieurs tags, correspondant à plusieurs certificats. Caddy choisira le certificat le plus adapté au SNI de destination.

De la même façon, on pousse la configuration complète vers Caddy.

.. code-block:: text

    curl 127.0.0.1:2019/load -X POST -H "Content-Type: application/json" -d @config.json




Mettre à jour une partie de la configuration
==============================================

Pour mettre à jour ou remplacer une partie de la configuration, on va utiliser le chemin JSON qu'on souhaite mettre à jour et changer de verbe HTTP.


POST /config/[chemin]
    Configure ou remplace un objet. Si l'objet est une liste, l'élément est ajouté à la liste.

Voici par exemple comment ajouter l'écoute sur le port 80, ce qui désactive la redirection automatique de HTTP vers HTTPS

.. code-block:: text

    curl -X POST -H "Content-Type: application/json" -d '":80"' "http://127.0.0.1:2019/config/apps/http/servers/srv0/listen"



PUT /config/[chemin]
    Créé un nouvel objet. Insert dans un liste

Pour continuer sur l'exemple du port d'écoute, on peut ajouter le port d'écoute 80 de cette façon :

.. code-block:: text

    curl -X PUT -H "Content-Type: application/json" -d '":80"' "http://127.0.0.1:2019/config/apps/http/servers/srv0/listen/0"



PATCH /config/[chemin]
    Remplace un objet ou une liste

Dison qu'on souhaite remettre en place la redirection du port 80 vers 443. Cela est automatique lorsqu'on demande à Caddy d'écouter seulement sur le port 443. Cette commande va remplacer la liste :code:`[":80", ":443"]` par simplement :code:`[":443"]`.

.. code-block:: text

    curl -X PATCH -H "Content-Type: application/json" -d '":443"' "http://127.0.0.1:2019/config/apps/http/servers/srv0/listen/"



Voilà pour un tour rapide de l'utilisation de l'API de Caddy. Dans un prochain article j'expliquerai comment compiler Caddy avec des plugins et comment générer un certificat wildcard pour un domaine hébergé chez OVH, en remplissant le challenge DNS proposé par Let's Encrypt.