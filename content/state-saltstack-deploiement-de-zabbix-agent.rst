State SaltStack pour déploiement de Zabbix-agent
################################################
:date: 2016-08-10 15:36
:author: alain
:category: Supervision
:tags: automation, yaml, zabbix-agent
:slug: state-saltstack-deploiement-de-zabbix-agent
:status: published

SaltStack est un gestionnaire de configuration comparable à Ansible,
Chef ou Puppet fonctionnant sur le modèle Client/Serveur. Le serveur
Salt est appelé 'master' et les clients des 'minions'. Les states sont
des listes de commandes que le serveur fait exécuter par le client. On
utilise YAML pour écrire les states.

Comme je l'avais promis
à `@SteveDESTIVELLE <https://twitter.com/SteveDESTIVELLE>`__ voici le
state SaltStack que nous utilisons pour déployer rapidement et
simplement l'agent Zabbix sur nos serveurs.

Ce state installe zabbix-agent sur les serveur Windows 32 et 64bits, sur
les CentOS 6 et 7 ainsi que sur Debian Wheezy. Il est assez simple d'y
ajouter la prise en charge d'autres OS. Sur les linux, le repository
Zabbix est déployé pour faciliter l'installation et la mise à jour de
l'agent. Enfin, le state pousse également le fichier de configuration de
zabbix-agent. Pensez à bien y ajouter le nom ou l'adresse IP de votre
serveur (fichier files/linux/zabbix/zabbix\_agentd.conf  et
files/windows/zabbix/conf/zabbix\_agentd.win.conf ).

Enfin, le state ouvre le firewall Windows, n'oubliez pas d'ajouter l'IP
de votre serveur Zabbix ligne 122 de init.sls  .

Pour télécharger les fichiers, ça se passe `sur
github <https://github.com/aldevar/Zabbix_SaltState>`__.

