Migration OpenLDAP 2.2 vers OpenLDAP 2.4
########################################
:date: 2015-10-30 23:24
:author: alain
:category: Tech
:tags: centos, migration, openldap, slap
:slug: migration-openldap-2-2-vers-openldap-2-4
:status: published

Parfois, certains serveurs sont là depuis tellement longtemps qu'on n'y
prête même plus attention. Et pourtant, il arrive qu'ils fassent tourner
des applications assez sensible, parfois même critique.

C'est le cas de ce serveur OpenLDAP qui tourne sur une RedHat 5, sans
licence (donc sans yum) et dont la version 2.2 d'OpenLDAP installée a
été compilée dans /usr/local. Typiquement le genre de serveur dont
personne ne veut s'occuper parce qu'il est difficile à maintenir et il
est également difficile de s'en débarrasser car il faut pouvoir sortir
les applications qui y tournent.

Avec un collègue nous nous sommes donc attelé à cette tâche, non sans
peine. Il n'était à priori pas difficile de sortir un annuaire OpenLDAP
2.2 vers un nouvel annuaire OpenLDAP 2.2 mais l’intérêt de cette
manipulation était assez limité. Nous avons donc décidé de migrer vers
la version 2.4 d'OpenLDAP proposée dans les dépôts de CentOS 7. Nous
souhaitions également profiter de cette migration pour passer d'une
configuration fichier (slapd.conf) à une configuration en base (olc, en
gros OpenLDAP stock sa configuration dans une base LDAP). Voici la
méthode employée pour réussir cette opération :

La première étape est de récupérer les informations dont nous avons
besoin sur l'ancien serveur. Nous avons besoin de son fichier de
configuration (slapd.conf, que nous allons renommer vieuxslapd.conf) et
du contenu de la base. Pour cela nous allons utiliser l'outil
``slapcat`` qui va générer un fichier ``ldif``. Ces 2 fichiers seront à
transférer sur le nouveau serveur. Si vous utilisez des schémas
spécifique, il faudra également les récupérer.

.. code::

    [aldevar@vieuxserveur]# slapcat -f /chemin/vers/vieuwslapd.conf -l /tmp/vieuxslap.ldif

Sur notre nouvelle machine CentOS 7, à jour, on installe
openldap-servers et openldap-clients

::

    [aldevar@serveur]# yum -y install openldap-servers openldap-clients

Configuration des logs d'OpenLDAP

::

    [aldevar@serveur]# echo "local4.*       /var/log/slapd.log" > /etc/rsyslog.d/slapd.conf
    [aldevar@serveur]# systemctl restart rsyslog.service

Dans notre cas, il était nécessaire de nettoyer l'ancien fichier de
configuration.
|  Pour vérifier si que le fichier de conf est valide, on utilise
``slaptest``

::

    [aldevar@serveur]# slaptest -f vieuxslapd.conf

Celui ci nous retourne des erreurs que nous corrigeons.

::

    [aldevar@serveur]# sed -i -e "s/attr=/attrs=/g" vieuxslapd.conf
    [aldevar@serveur]# sed -i -e "/pidfile/d" /root/vieuxslapd.conf
    [aldevar@serveur]# sed -i -e "/argsfile/d" /root/vieuxslapd.conf
    [aldevar@serveur]# sed -i -e "s;directory /var/ldap/annuaireldap;directory /var/lib/ldap;" /root/vieuxslapd.conf

Nous utilisons le schéma de samba, pour le récupérer nous installons
samba

::

    [aldevar@serveur]# yum -y install samba

On copie les fichiers schéma récupérés sur l'ancien serveur dans le bon
répertoire :

::

    [aldevar@serveur]# cp *.schema /etc/openldap/schema/
    [aldevar@serveur]# chown ldap. /etc/openldap/schema/*

Maintenant, nous allons corriger une incompatibilité sur laquelle nous
avons bloqué un bon moment. OpenLDAP ajoute pour chaque entrée un
attribut ``entryUUID`` qu'il provisionne automatiquement. Entre la
version 2.2 et notre version 2.4, la format de la valeur
d'\ ``entryUUID`` a changé. Il est passé d'une suite de caractères
aléatoire à 4 série de caractères hexadécimaux séparés par des ``-``.
Tant que nous n'avions pas trouver de solution à cette incompatibilité,
aucune entrée de ne pouvait être ajoutée dans notre nouvelle base. C'est
d’ailleurs la raison pour laquelle nous ne pouvions pas mettre en place
de synchronisation entre les 2 instances.

La solution, radicale et rapide est de supprimer les entrées
``entryUUID``

::

    [aldevar@serveur]# sed -i -e "/entryUUID/d" vieuxslap.ldif

Une fois ces étapes effectuée, nous devrions être prêt pour tester
l'import des données. Pour cela, nous utilisons l'outil ``slapadd`` qui
à l'avantage de pouvoir travailler sans daemon ldap actif. En lui
fournissant le fichier de configuration il est capable d'écrire
directement dans les fichiers de la base. Dans un premier temps, nous le
lançons avec l'option ``-u`` afin de le lancer en mode ``dry-run``.

::

    [aldevar@serveur]# slapadd -f vieuxslapd.conf  -c -u -o schema-check=yes -l vieuxslap.ldif

Si cette commande ne sort pas d'erreurs, on peut la faire en réelle.

::

    [aldevar@serveur]# slapadd -f vieuxslapd.conf  -c -o schema-check=yes -l vieuxslap.ldif

A partir de là, on dispose d'une base ldap fonctionnelle et si on lance
la daemon slapd en lui fournissant le fichier de configuration, tout
devrait fonctionner.

::

    [aldevar@serveur]# slapd -u ldap -f vieuxslapd.conf

Mais, comme je l'ai dit plus haut, la bonne pratique est plutôt de
stocker la configuration en base olc. Cette base se trouve dans
``/etc/openldap/slapd.d`` et contient déjà de quoi faire fonctionner un
slapd basique mais vide. L'utilitaire ``slaptest`` que nous avons
utilisé pour vérifier le fichier de configuration est également utilisé
pour faire cette migration. En lui fournissant d'un coté le fichier de
configuration et de l'autre le dossier de destination, il va transformer
le contenu du fichier en instructions ldif.

Avant tout, on supprime le contenu actuel du répertoire.

::

    [aldevar@serveur]# rm -Rf /etc/openldap/slapd.d/*

On lance la migration de la configuration

::

    [aldevar@serveur]# slaptest -f vieuxslapd.conf -F /etc/openldap/slapd.d/

0n corrige les droits pour que le daemon puisse travailler

::

    [aldevar@serveur]# chown -R ldap. /etc/openldap/slapd.d/

Enfin, on importe le fichier ``DB_CONFIG`` afin d'avoir des performances
normales sur la base

::

    [aldevar@serveur]# cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
    [aldevar@serveur]# chown ldap. /var/lib/ldap/DB_CONFIG

Pour finir, on peut démarrer le daemon

::

    [aldevar@serveur]# systemctl start slapd
    [aldevar@serveur]# systemctl enable slapd

