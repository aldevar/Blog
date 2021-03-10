Firefox comme navigateur par défaut de SailfishOS
#################################################
:date: 2015-08-24 09:17
:author: alain
:category: jolla
:slug: firefox-comme-navigateur-par-defaut-de-sailfishos
:status: published

Jolla et son SailfishOS sont vraiment de beaux outils mais il faut
avouer qu'ils ont quand même un problème majeur, c'est la piètre qualité
des navigateurs intégrés et surtout du navigateur par défaut.

Malheureusement, l'interface ne propose actuellement aucune option pour
modifier ce comportement. Ainsi, lorsqu'on clique sur un lien dans une
autre application c'est forcement ce navigateur tout moisi qui s'ouvre
et qui met 3 heures à charger la page. Heureusement, avec quelques
bidouille, il est possible de paramétrer Firefox comme navigateur par
défaut, c'est d'ailleurs ce que je viens de faire :)

Si vous avez déjà Firefox d'installé, vous pouvez directement vous
rendre au paragraphe 'Paramétrage d'ADB'.

Installation d'Aptoide
----------------------

La première étape est d'installer le market Aptoide si ce n'est pas déjà
fait. Pour cela, il faut se rendre dans la Boutique Jolla, puis dans
'Place de marché' tout en bas et installer le market Aptoide Appstore

[gallery size="medium" columns="2" link="file" ids="571,572"]

Installation de Firefox
-----------------------

L'installation de Firefox se fait via Aptoide, il faut donc ouvrir
l'application nouvellement installée et dans la zone de recherche, taper
Firefox. Il faut ensuite trouver l'application **Firefox Browser for
Android** et l'installer.

[gallery link="file" columns="2" size="medium" ids="575,576,577,578"]

Paramétrage d'ADB
-----------------

C'est partie pour le bricolage. Il faut d'abord `se connecter en
SSH <http://blog.devarieux.net/2015/03/se-connecter-en-ssh-a-son-jolla/>`__
à l'appareil afin d'y modifier le comportement d'Alien. Pour cela, il
faut éditer le fichier /opt/alien/system/build.prop et ajouter à la fin
:

::

    persist.service.adb.enable=1
    service.adb.tcp.port=5555

Une fois cette modification faite, on relance Alien Dalvik

::

    [root@Jolla ~]# systemctl restart aliendalvik.service

Maintenant, un process adb doit apparaitre

::

    [root@Jolla ~]# ps aux | grep adb
     shell     5162  0.0  0.0   6532    92 ?        Ssl  23:04   0:00 /system/root/sbin/adbd
     root      5592  0.0  0.0   3984   288 pts/0    Sl   23:06   0:00 adb fork-server server
     root      7330  0.0  0.0   2256   544 pts/0    S+   23:57   0:00 grep adb

::

    [root@Jolla ~]# lsof -p 5162 | grep android_adb
     adbd    5162 shell   10u   CHR      10,25      0t0  1437 /opt/alien/dev/android_adb

Une fois que tout ça est ok, on lance en root :

::

    [root@localhost bin]# /opt/alien/system/bin/adb kill-server
    [root@localhost bin]# /opt/alien/system/bin/adb devices    
    * daemon not running. starting it now on port 5038 *
    * daemon started successfully *
    List of devices attached 
    emulator-5554   device

    [root@localhost bin]#

Paramétrage de SailfishOS
-------------------------

La système est maintenant prêt à accueillir nos modifications. Toujours
dans la connexion SSH, se rendre dans /usr/share/applications, faire une
copie de sauvegarde du fichier open-url.desktop et le modifier pour
qu'il ne prenne plus en charge les types MIME http et https

::

    cd /usr/share/applications
    cp -a open-url.desktop open-url.desktop.ori
    vi open-url.desktop

Une fois dans le fichier, on supprime la ligne

.. code::

    MimeType=text/html;x-maemo-urischeme/http;x-maemo-urischeme/https;

Le fichier doit maintenant ressembler à cela

::

    [root@Jolla applications]# cat open-url.desktop
    [Desktop Entry]
    Type=Application
    Name=Browser
    NotShowIn=X-MeeGo;
    X-MeeGo-Logical-Id=sailfish-browser-ap-name
    X-MeeGo-Translation-Catalog=sailfish-browser
    X-Maemo-Service=org.sailfishos.browser
    X-Maemo-Method=org.sailfishos.browser.openUrl

Créer ensuite le fichier firefox-as-default.desktop et y mettre ce
contenu

::

    [Desktop Entry]
    Type=Application
    Name=Browser
    NotShowIn=X-MeeGo;
    X-MeeGo-Logical-Id=sailfish-browser-ap-name
    X-MeeGo-Translation-Catalog=sailfish-browser
    X-Maemo-Service=org.sailfishos.browser
    X-Maemo-Method=org.sailfishos.browser.openUrl
    [root@Jolla applications]# cat firefox-as-default.desktop
    [Desktop Entry]
    Exec=/opt/alien/system/bin/adb -e shell am start -a android.intent.action.VIEW -n org.mozilla.firefox/.App -d ' %U'
    Name=Firefox HTTP handler (opener)
    Type=Application
    MimeType=text/html;x-maemo-urischeme/http;x-maemo-urischeme/https;
    X-Nemo-Application-Type=no-invoker
    X-Nemo-Single-Instance=no
    X-apkd-apkfile=/data/app/org.mozilla.firefox.apk
    NoDisplay=true

Afin de prendre ces modifications en compte, on met à jour le cache des
types MIME

::

    [root@Jolla applications]# update-desktop-database

Le fichier mimeinfo.cache devrait maintenant contenir 2 lignes de ce
type

::

    x-maemo-urischeme/http=firefox-as-default.desktop;
    x-maemo-urischeme/https=firefox-as-default.desktop;

Dorénavant, lorsqu'un lien sera cliqué dans une application (message,
twitter...) celui s'ouvrir avec Firefox.
