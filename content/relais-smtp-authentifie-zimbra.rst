Zimbra : Envoi de mails via un relais SMTP authentifié
######################################################
:date: 2016-06-24 08:30
:author: Aldevar
:category: Sysadmin
:slug: relais-smtp-authentifie-zimbra
:status: published

Héberger soi même ses données c'est bien, le faire correctement c'est
mieux. Le problème majeur lorsqu'on souhaite héberger soi même ses mails
est qu'il est difficile de s'assurer que les mails soient bien reçus par
nos correspondants.

Il arrive souvent que l'IP fournie par l’hébergeur fasse partie d'un
bloc d'IP bannie par plusieurs serveur SMTP. Il est toujours possible de
se faire débloquer des principales blacklists mais la plupart des
services mails possèdent leur propre blacklist (coucou barracuda). Même
un SPF et un DKIM bien configuré ne suffisent pas à outrepasser ces
blocages.

Plusieurs solutions s'offraient à moi pour contourner ce problème.

-  Changer d'adresse IP: ça peut fonctionner mais impossible de savoir
   tant qu'on a pas testé la nouvelle IP. Forte  probabilité que cette
   IP fasse également partie d'un bloc blacklisté
-  Passer sur un hébergeur Zimbra : Intéressant, mais souvent très cher.
   De l'ordre de 5€/mois et par compte minimum.
-  Passer par un relais SMTP : J'ai opté pour cette solution même si
   elle n'est pas idéal car cela ajoute intermédiaire et une dépendance
   pour le service.

Pour mettre cette solution en oeuvre, j'ai choisi le service smtp2go. Il
y en a beaucoup d'autres et la plupart proposent des services gratuits
pour un envoi limité de mails. Avec smtp2go, le service est gratuit
jusqu'à 1000 mails par mois ce qui devrait être suffisant.

Une fois l'inscription effectuée, il faut encore configurer Zimbra pour
qu'il utilise ce relais. L'interface web d'administration propose bien
d'ajouter des relais SMTP mais impossible de s'y authentifier. La
configuration d'un relais STMP authentifié doit être faite en ligne de
commande.

::

    [root@monzimbra]# su - zimbra
    ## On ajoute le relais SMTP
    [root@monzimbra]# zmprov ms monzimbra.mondomaine.com zimbraMtaRelayHost relaissmtp.relaisdomaine.com:port
    ## On créé un fichier text de mapping login/mdp pour le relais
    [root@monzimbra]# echo relaissmtp.relaisdomaine.com USERNAME:PASSWORD > /opt/zimbra/conf/relay_password
    ## Création de la table postfix
    [root@monzimbra]# postmap /opt/zimbra/conf/relay_password
    ## Pour tester. Cette commande doit retourner le couple login/mdp
    [root@monzimbra]# postmap -q relaissmtp.relaisdomaine.com /opt/zimbra/conf/relay_password
    ## Configuration de postfix pour qu'il utilise la map de login/mdp
    [root@monzimbra]# zmprov ms monzimbra.mondomaine.com zimbraMtaSmtpSaslPasswordMaps lmdb:/opt/zimbra/conf/relay_password
    ## Configuration de postfix pour qu'il utilise l'authentification SSL
    [root@monzimbra]# zmprov ms monzimbra.mondomaine.com zimbraMtaSmtpSaslAuthEnable yes
    ## Configuration de postfix pour qu'il n'utilise pas le canonical name du relais (problème de login/mdp sinon)
    [root@monzimbra]# zmproc ms monzimbra.mondomaine.com zimbraMtaSmtpCnameOverridesServername no
    ## Configuration de TLS
    [root@monzimbra]# zmprov ms monzimbra.mondomaine.com zimbraMtaSmtpTlsSecurityLevel may

C'est terminé, tous les domaines attachés au serveur passeront
dorénavant vers ce relais SMTP.
