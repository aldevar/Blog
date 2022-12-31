Caddy, OVH et les certificats wildcard
########################################
:date: 2021-04-05 08:55
:author: Aldevar
:category: Sysadmin
:slug: caddy-ovh-acme
:status: published

Après avoir présenté dans un `premier article </2021/02/caddy-presentation.html>`_ ce qu'est Caddy et son utilisation de façon basique, puis dans `un second </2021/02/caddy-api.html>`_ le pilotage de Caddy par API ainsi qu'une configuration un peu plus avancée, je souhaites ici aborder le sujet de la génération de certificats TLS via Let's Encrypt avec le challenge `DNS-01 <https://letsencrypt.org/fr/docs/challenge-types/#d%C3%A9fi-dns-01>`_.

Le challenge DNS à l'avantage de pouvoir être utilisé pour générer un certificat DV wildcard. Une fois passé un certain nombre de sous domaines servis par un reverse proxy, il devient intéressant d'utiliser ce type de certificat afin d'éviter de générer trop de requêtes vers les serveurs de Let's Encrypt. De plus, avec un seul certificat à gérer pour l'ensemble des sous domaines, la gestion devient simplifiée, et notamment la supervision ou même le renouvellement.

Caddy intègre de base la gestion de Let's Encrypt pour les challenges HTTP-01 car celui-ci est universel et ne dépend d'aucun autre services. C'est un échange réalisé directement entre le serveur Caddy et les serveurs de Let's Encrypt. Pour le challenge DNS-01, il y a un intermédiaire. Cet intermédiaire est le serveur DNS du domaine pour lequel on souhaite générer un certificat wildcard. De part la multitude de serveurs disponibles et de prestataires fournissant ces services, il est difficile d'avoir un protocole unifié de modification distante des entrées DNS. A ma connaissance, le seul standard qui existe pour cela est la `RFC 2136 <https://tools.ietf.org/html/rfc2136>`_ qui ne semble pas être implémentée chez la plupart des fournisseurs de services DNS.

Nous allons donc voir comment, avec Caddy, générer un certificat wildcard avec OVH en fournisseur de service DNS. La procédure est assez similaire avec les autres fournisseurs qui ont, je l'espère, pris plus de soin dans la documentation de cette fonctionnalité. 

Caddy n'intègre pas, de base, l'ensemble des plugins permettant de résoudre les challenges DNS de tous les fournisseurs. Pour intégrer le bon plugin, il est nécessaire de compiler Caddy. L'opération est particulièrement simple à réaliser et à l'avantage de produire en sortie un binaire unique qu'il est ensuite facile de déployer sur ses serveurs. La compilation de Caddy est assez bien expliquée dans `la documentation <https://caddyserver.com/docs/build#xcaddy>`_ et voici la liste des `plugins disponible <https://caddyserver.com/docs/modules/>`_. A ce jour, aucun plugin spécifique n'a été écrit pour OVH, il faut donc se rabattre sur le module `Lego Deprecated <https://github.com/caddy-dns/lego-deprecated>`_. Ce module utilise une ancienne API mais est actuellement le seul qui permet de gérer un grand nombre de fournisseurs de DNS, dont OVH.

Compilation de Caddy
======================

Pour compiler Caddy, nous avons besoin de 2 choses. Golang et le binaire xcaddy qui permet de facilement compiler caddy avec les modules spécifiés. On commence donc par installer Golang et déclarer son binaire dans le PATH.

.. code-block:: text

    # wget https://golang.org/dl/go<version>.linux-amd64.tar.gz
    # tar -C /usr/local -xzf go<version>.linux-amd64.tar.gz
    # rm -f go<version>.linux-amd64.tar.gz

On édite le fichier ``/etc/profile`` pour ajouter le binaire go dans le PATH. A la fin du fichier on ajoute : 

.. code-block:: text

    export PATH=$PATH:/usr/local/go/bin

Puis, on source le fichier pour mettre à jour le PATH et on s'assure que go est bien installé en affichant la version (ici 1.16).

.. code-block:: text

    # source /etc/profile
    # go version
    go version go1.16 linux/amd64

Puis on récupère le binaire xcaddy et on le rend exécutable. Lors de la rédaction cet article, la dernière version disponible est la 0.1.8.

.. code-block:: text

    # wget https://github.com/caddyserver/xcaddy/releases/download/v0.1.8/xcaddy_0.1.8_linux_amd64.tar.gz
    # tar xvzf xcaddy_0.1.8_linux_amd64.tar.gz
    # ls
    LICENSE  README.md  xcaddy  xcaddy_0.1.8_linux_amd64.tar.gz
    # chmod o+x xcaddy

Enfin, avec l'aide de xcaddy, on compile caddy avec le plugin lego-deprecated. On se retrouve avec le binaire caddy dans le répertoire.

.. code-block:: text

    ./xcaddy build --with github.com/caddy-dns/lego-deprecated
    # ls
    LICENSE  README.md  caddy  xcaddy  xcaddy_0.1.8_linux_amd64.tar.gz

Configuration d'OVH
=====================

Il faut autoriser Caddy à créer et supprimer des entrées DNS sur les serveurs d’OVH. Pour cela, il faut créer une application chez OVH, via ce lien : https://eu.api.ovh.com/createApp/

On rentre son account ID et mot de passe. On choisit un nom d’application ici ``xcaddy-dns-challenge`` ainsi qu’une description. OVH affiche alors l’Application Key et l’Application Secret. On les conserve bien au chaud pour la suite.

Ensuite, il faut donner des droits à cette application. On réalise cela par un call API directement sur la console OVH.


.. code-block:: text

    curl -XPOST -H "X-Ovh-Application: <Application Key>" -H "Content-type: application/json" https://eu.api.ovh.com/1.0/auth/credential -d '{"accessRules":[{"method":"POST","path":"/domain/zone/<Nom De Domaine>/record"},{"method":"POST","path":"/domain/zone/<Nom De Domaine>/refresh"},{"method":"DELETE","path":"/domain/zone/<Nom De Domaine>/record/*"}],"redirection": "https://www.foo.com"}'
 

La partie redirection a la fin ne nous intéresse pas mais est obligatoire. Elle indique vers quelle page l’application doit être redirigée une fois connectée.

En retour, on obtient un JSON avec la consumer Key. C’est cette info qu’il faut conserver.

.. code-block:: json

    {"validationUrl":"https://eu.api.ovh.com/auth/?credentialToken=xxxxxxxxxxxxxxx","consumerKey":"<The Consumer Key>","state":"pendingValidation"}


On voit que l'état est “Pending Validation”. Afin de valider, il faut se rendre sur le lien validationUrl.

Sur ce lien, on entre de nouveau ses codes d'accès OVH puis on choisi la durée de validité de l’accès. 
On a maintenant toutes les infos dont nous avons besoin :

- Application Key
- Application Secret
- Consumer Key


Configuration de Caddy
========================

Voyons maintenant comment générer un certificat wildcard pour un domaine puis servir plusieurs sous-domaines en dessous. J'ai mis un peu de temps à trouver la bonne façon de faire, la voici servie pour vous sur un plateau :)
Voici un extrait de mon fichier de configuration, je vais décrire en dessous les différentes sections.

.. code-block:: text

    *.domain.com {
        tls {
                dns lego_deprecated ovh
        }

        @backend host backend.domain.com
        reverse_proxy @backend 10.0.0.2:3001

        @prodapi {
                host prod.domain.com
                path /api/v1/*
        }

        @prod {
                host prod.domain.com
                not path /api/v1/
        }

        reverse_proxy @prodapi 10.0.0.1:3001
        reverse_proxy @prod 10.0.0.1:3000


        }

On déclare d'abord ``*.domain.com`` qui est le domaine pour lequel on souhaite que Caddy génère un certificat wildcard. Pour cela, une première section tls avec l'entrée ``dns lego_deprecated ovh`` signifie : 

- dns: Résolution du challenge DNS-01
- lego_deprecated: Utilisation du module lego_deprecated
- ovh: Parmi les providers proposés par lego_deprecated, utiliser OVH.

L'entrée ``@backend host backend.domain.com`` est un ``matcher``. C'est à dire qu'on place sous le nom ``backend`` l'ensemble des requêtes dont le SNI est ``backend.domain.com``. Puis, juste en dessous, l'ensemble des requêtes qui matchent ``@backend`` sont reverse proxyfiées (oui, je sais...) vers 10.0.0.2:3001.

Les 2 entrées suivantes sont un peu similaires au matcher ``@backend`` mais comme je devais spécifié plusieurs filtres (1 sur le SNI et 1 sur le path), les filtres sont placés dans un bloc d'accolades. Ensuite, les matchers ``@prodapi`` et ``@prod`` sont également reverse proxyfiés (oui, bon, ça va...) vers leurs serveurs respectifs.

On est prêt à lancer Caddy. Il faut cependant trouver un moyen de lui spécifier les clés et secret OVH pour que le module lego_deprecated puisse se connecter et générer les entrées DNS. Pour cela, plusieurs solutions. La plus simple est d'executer Caddy depuis le terminal avec les variables d'environnement, de cette façon : 

.. code-block:: text

    OVH_APPLICATION_KEY=<Application Key> OVH_APPLICATION_SECRET=<Application Secret> OVH_CONSUMER_KEY=<Consumer Key> OVH_ENDPOINT=ovh-eu ./caddy run --config Caddyfile

C'est bien, ça fonctionne mais c'est pas vraiment production ready. L'autre solution est de placer ces variables d'environnement directement dans le fichier systemd de Caddy. Dans la section ``[Service]`` on peut ajouter des variables d'environnement de cette façon : 

.. code-block:: text

    [Service]
    User=caddy
    Group=caddy
    ExecStart=/usr/bin/caddy run --environ --config /etc/caddy/Caddyfile
    ExecReload=/usr/bin/caddy reload --config /etc/caddy/Caddyfile
    TimeoutStopSec=5s
    LimitNOFILE=1048576
    LimitNPROC=512
    PrivateTmp=true
    ProtectSystem=full
    AmbientCapabilities=CAP_NET_BIND_SERVICE
    Environment='OVH_APPLICATION_KEY=<Application Key>'
    Environment='OVH_APPLICATION_SECRET=<Application Secret>'
    Environment='OVH_CONSUMER_KEY=<Consumer Key>'
    Environment='OVH_ENDPOINT=ovh-eu'

Normalement, dans les logs, on devrait voir quelque chose comme ça. En tout cas, c'est ce qu'on vise :)

.. code-block:: text

    systemd[1]: Started Caddy.
    caddy[575954]: caddy.HomeDir=/var/lib/caddy
    caddy[575954]: caddy.AppDataDir=/var/lib/caddy/.local/share/caddy
    caddy[575954]: caddy.AppConfigDir=/var/lib/caddy/.config/caddy
    caddy[575954]: caddy.ConfigAutosavePath=/var/lib/caddy/.config/caddy/autosave.json
    caddy[575954]: caddy.Version=v2.3.0
    caddy[575954]: runtime.GOOS=linux
    caddy[575954]: runtime.GOARCH=amd64
    caddy[575954]: runtime.Compiler=gc
    caddy[575954]: runtime.NumCPU=1
    caddy[575954]: runtime.GOMAXPROCS=1
    caddy[575954]: runtime.Version=go1.16
    caddy[575954]: os.Getwd=/
    caddy[575954]: LANG=C.UTF-8
    caddy[575954]: PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
    caddy[575954]: HOME=/var/lib/caddy
    caddy[575954]: LOGNAME=caddy
    caddy[575954]: USER=caddy
    caddy[575954]: OVH_APPLICATION_KEY=<Application Key>
    caddy[575954]: OVH_APPLICATION_SECRET=<Application Secret>
    caddy[575954]: OVH_CONSUMER_KEY=<Consumer Key>
    caddy[575954]: OVH_ENDPOINT=ovh-eu
    caddy[575954]: {"level":"info","ts":1615295347.2837744,"msg":"using provided configuration","config_file":"/etc/caddy/Caddyfile","config_adapter":""}
    caddy[575954]: {"level":"info","ts":1615295347.294112,"logger":"admin","msg":"admin endpoint started","address":"tcp/localhost:2019",enforce_origin":false,"origins":["localhost:2019","[::1]:2019","127.0.0.1:2019"]}
    caddy[575954]: {"level":"info","ts":1615295347.2947812,"logger":"http","msg":"server is listening only on the HTTPS port but has no TLS connection policies; adding one to enable TLS","server_name":"srv0","https_port":443}
    caddy[575954]: {"level":"info","ts":1615295347.2949548,"logger":"http","msg":"enabling automatic HTTP->HTTPS redirects","server_name":"srv0"}
    caddy[575954]: {"level":"info","ts":1615295347.2992623,"logger":"http","msg":"enabling automatic TLS certificate management","domains":["*.domain.com"]}
    caddy[575954]: {"level":"info","ts":1615295347.3005319,"msg":"autosaved config","file":"/var/lib/caddy/.config/caddy/autosave.json"}
    caddy[575954]: {"level":"info","ts":1615295347.3007138,"msg":"serving initial configuration"}
    caddy[575954]: {"level":"info","ts":1615295347.3020074,"logger":"tls.obtain","msg":"acquiring lock","identifier":"*.domain.com"}
    caddy[575954]: {"level":"info","ts":1615295347.3032272,"logger":"tls.obtain","msg":"lock acquired","identifier":"*.domain.com"}
    caddy[575954]: {"level":"info","ts":1615295347.3185842,"logger":"tls.cache.maintenance","msg":"started background certificate maintenance","cache":"0xc0009a20e0"}
    caddy[575954]: {"level":"info","ts":1615295347.3187766,"logger":"tls","msg":"cleaned up storage units"}
    caddy[575954]: {"level":"info","ts":1615295348.2573807,"logger":"tls.issuance.acme","msg":"waiting on internal rate limiter","identifiers":["*.domain.com"]}
    caddy[575954]: {"level":"info","ts":1615295348.2576807,"logger":"tls.issuance.acme","msg":"done waiting on internal rate limiter","identifiers":["*.domain.com"]}
    caddy[575954]: {"level":"info","ts":1615295348.582178,"logger":"tls.issuance.acme.acme_client","msg":"trying to solve challenge","identifier":"*.domain.com","challenge_type":"dns-01","ca":"https://acme-v02.api.letsencrypt.org/directory"}
    caddy[575954]: {"level":"info","ts":1615295360.2630491,"logger":"tls.issuance.acme.acme_client","msg":"validations succeeded; finalizing order","order":"https://acme-v02.api.letsencrypt.org/acme/order/11111/2222222"}
    caddy[575954]: {"level":"info","ts":1615295361.126138,"logger":"tls.issuance.acme.acme_client","msg":"successfully downloaded available certificate chains","count":2,"first_url":"https://acme-v02.api.letsencrypt.org/acme/cert/aaaaaaaabbbbbbb"}
    caddy[575954]: {"level":"info","ts":1615295361.1281288,"logger":"tls.obtain","msg":"certificate obtained successfully","identifier":"*.domain.com"}
    Mcaddy[575954]: {"level":"info","ts":1615295361.1286106,"logger":"tls.obtain","msg":"releasing lock","identifier":"*.domain.com"}


Cet article ne fait qu'effleurer les possiblités offerte par Caddy. Comme toujours, je vous invite à vous plonger dans la documentation du logiciel et à parcourir la liste des plugins disponible. Si vous souhaitez voir d'autres fonctionnalités de Caddy détaillées sur ce blog n'hésitez pas à m'en faire part directement.