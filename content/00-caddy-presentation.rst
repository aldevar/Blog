Présentation de Caddy
#######################
:date: 2021-02-19 06:55
:author: Aldevar
:category: Tech
:tags: caddy, web
:slug: caddy-presentation
:status: published

Dans un tweet récent, j'expliquais voir trop peu de publication d'articles sur le server web / reverse proxy `Caddy <https://caddyserver.com/>`_. Je pense que Caddy gagne a être connu, voici donc un premier article de présentation. 

.. raw:: html

    <blockquote class="twitter-tweet" data-partner="tweetdeck"><p lang="fr" dir="ltr">Je vois pas mal de partage d&#39;articles sur Traefik dans mon fil Twitter. J&#39;aime beaucoup Traefik mais je lui préfère <a href="https://twitter.com/caddyserver?ref_src=twsrc%5Etfw">@caddyserver</a>.<br>Je profite donc de la reprise des activités sur mon blog pour vous préparer quelques articles sur Caddy et l&#39;utilisation de son API.</p>&mdash; Alain Devarieux (@landvarx) <a href="https://twitter.com/landvarx/status/1362078709436592130?ref_src=twsrc%5Etfw">February 17, 2021</a></blockquote>
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Caddy est un serveur web, de même que Apache ou Nginx. Il dispose également d'une fonctionnalité de reverse proxy et utilise des options de sécurités avancées par défaut (HTTPS par défaut avec Let's Encrypt ou ZeroSSL, TLS 1.3, OCSP Stapling, Cipher Suite modernes). Le logiciel est écrit en Go.
En plus de ces fonctionnalités de sécurités, Caddy est multiplateforme, il fonctionne avec un seul binaire, supporte les plugins et supporte plusieurs types de challenges ACME.
Je ne vais revenir sur son installation, parfaitement décrite dans `la documentation <https://caddyserver.com/docs/install>`_.

Configuration
==============

Caddy peut se configurer de deux manières. Via le fichier de configuration, appelé Caddyfile ou via son API avec un payload JSON. L'utilisation de l'API sera décrite dans un prochain article.
J'utilise Caddy principalement pour ses fonctionnalités de reverse proxy. Voyons donc quelques exemples de configuration de Caddy via le Caddyfile.

.. code-block:: text

    sub.domain.com {
        reverse_proxy 10.0.0.1:8000
        log {
            output file /var/log/caddy/sub.domain.com_access.log
        }
    }

Bien, avec ça, nous avons un reverse proxy qui écoute sur le port 80 et 443, avec redirection automatique HTTP vers HTTPS. Les logs seront renvoyés vers un fichier. Avec cette configuration, le certificat Let's Encrypt est généré (si le DNS est bien configuré et que Caddy est accessible depuis l'exterieur) et seul les protocoles TLS 1.2 et 1.3 sont supportés. Niveau sécurité, on est pas mal.
De la même façon, le header :code:`X-Forwarded-For` est automatiquement intégré dans l'entête HTTP envoyé au serveur de backend. Cette intégration permet de gagner quelques lignes de configurations.
Voyons maintenant comment gérer l'utilisation de deux backend différents pour des URI différentes.

.. code-block:: text

    sub.domain.com {
    reverse_proxy /api/v1/* 10.0.0.2:4000
    reverse_proxy / 10.0.0.1:3000

    log {
            output file /var/log/caddy/sub.domain.com_access.log {
                    roll_size 10MiB
                    roll_keep 10
                    }
            }
    }


Là encore, c'est assez simple. On traite d'abord les requêtes vers :code:`/api/v1` qui sont envoyées vers un premier backend et le reste des requêtes est envoyée vers :code:`10.0.0.1`. J'en ai profité pour ajouter une rotation des logs.

Tout cela fonctionne bien qd on un site disponible publiquement et pour lequel Caddy peut générer un certificat Let's Encrypt. Voyons maintenant comment intégrer son porpre certificat (autosigné ou non). Pour cet exemple, je m'appuie sur une configuration de Caddy pour servir un serveur Graylog

.. code:: text

    logs.domain.com {
            reverse_proxy 127.0.0.1:9000
            header X-Graylog-Server-URL https://logs.domain.com/
            tls /etc/pki/tls/certs/companycert.crt /etc/pki/tls/private/companycert.key
    log {
            output file /var/log/caddy/graylog.log {
                    roll_size 10MiB
                    roll_keep 10
                    }
            }
    }

L'option :code:`tls` permet de passer directement le certificat puis la clé privée du certificat. L'ajout un header se fait de façon assez simple ici aussi.

Enfin, comment faire lorsqu'on souhaite servir son site en plain HTTP, sans TLS. L'option est assez simple et plutot ingénieuse. Il suffit de forcer le site en HTTP dans l'URL.

.. code:: text

    http://sub.domain.com {
        reverse_proxy 10.0.0.1:8000
        log {
            output file /var/log/caddy/sub.domain.com_access.log
        }
    }

Avec cette configuration, Caddy ne va pas tenter de générer le certificat Let's Encrypt ni proposer de redirection HTTP vers HTTPS.

Dans le prochain article nous verrons comment utiliser l'API de Caddy en lecture et en écriture totale ou partielle de configuration.