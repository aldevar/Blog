Zabbix - Authentification SAML avec Keycloak et provider Google Auth
#####################################################################
:date: 2021-12-29 00:23
:author: Aldevar
:category: Supervision
:slug: zabbix-saml-keycloak-google
:status: published

Depuis Zabbix 5.0, l'application permet de configurer une authentification SSO SAML. Le protocol SAML est utilisé par des services tel que Microsoft ADFS et Azure AD ou encore Okta.
De mon coté, j'utilise Keycloak pour mon intégration SSO. Un des providers utilisé est Google Auth.

Cela fait plusieurs mois que ce chantier est mis de coté et je viens enfin de trouver le temps de finaliser la mise en oeuvre de l'authentification des comptes utilisateurs sur Zabbix en SAML, avec Keycloak et le provider Google Auth. Je vais décrire ici les étapes afin d'avoir ce type d'authentification fonctionnelle.
Je pars du principe que vous avez déjà un serveur Keycloak installé et que votre provider Google Auth est configuré.

L'objectif est que, au sein d'une entreprise utilisant Google Workspace, les utilisateurs de Zabbix puissent s'authentifier directement avec leurs comptes Google Workspace. Dans mon cas, Keycloak est le backend d'authentification global de l'entreprise et est utilisé par plusieurs autres applications, qu'elles soient internes ou à destination des clients.

|


Gestion des certificats
=========================

La première étape est de générer un certificat pour Zabbix. Cela se passe dans :code:`/usr/share/zabbix/conf/certs`. On utilise openssl pour le générer.

.. code-block:: text

    cd /usr/share/zabbix/conf/certs
    openssl req -x509 -sha256 -newkey rsa:2048 -keyout sp.key -out sp.crt -days 3650 -nodes -subj '/CN=My Zabbix Server'

Cette commande génère un certificat et une clé privée pour les échanges SAML.

La seconde étape consiste à récupérer le certificat X509 de l'identity provider (IDP) de Keycloak. Pour moi, le plus rapide a été de me rendre sur cette URL pour y copier la chaine du certificat.

.. code-block:: text

   https://<keycloakaddress>/auth/realms/<realmname>/protocol/saml/descriptor

Cette page doit afficher un bloc XML avec le nom du certificat et le certificat au format X509 entre les balises :code:`<ds:X509Certificate>`. Après avoir copié ce certificat, il faut le coller sur le serveur Zabbix dans le fichier :code:`/usr/share/zabbix/conf/certs/idp.crt`. Le fichier doit ressembler à ça : 

.. code-block:: text

   -----BEGIN CERTIFICATE-----
   MIICmSF...........g20plgaFEwvQERGH=
   -----END CERTIFICATE-----

Puis changer les permissions du fichier.

.. code-block:: text

   chmod 755 idp.crt

|
|

Configuration de Keycloak
=========================

Dans l'interface de Keycloak, sur votre realm, créer un client ayant pour id :code:`zabbix` et pour protocol :code:`SAML`.

.. image:: {static}/images/Keycloak-Client-Zabbix.png
    :alt: Creation du client Zabbix dans Keycloak
    :scale: 50 %
    :target: /images/Keycloak-Client-Zabbix.png

|

Une fois le client ajouté, il faut l'éditer pour terminer sa configuration. Voici les paramètres à configurer *(note : mon installation de Zabbix est joignable à la racine du serveur web et non via le chemin /zabbix comme dans la configuration par defaut. Prenez soin de bien mettre le chemin complet vers votre serveur Zabbix)* :

- Master SAML Processing URL : ``https://zabbix.domain.tld/index_sso.php?acs``
- Valid Redirect URL : ``https://zabbix.domain.tld/*``
- Dans la section Fine Grain, Logout Service Redirect Binding URL : ``https://zabbix.domain.tld/index_sso.php?sls``
- Les paramètres devant être sur 'ON' sont : ``Include AuthnStatement, Sign Document, Force POST Binding, Front Channel Logout et Force Name ID Format.``
- Le Name ID Format est code : ``email``


.. image:: {static}/images/Keycloak-Client-Zabbix-Configuration.png
    :alt: Configuration du client Zabbix dans Keycloak
    :scale: 50 %
    :target: /images/Keycloak-Client-Zabbix-Configuration.png

|

Créer ensuite le Mapper, dans l'onglet Mapper du client Zabbix.

- Name: ``zabbixuser``
- Mapper Type : ``User Attribute``
- User Attribute : ``email``
- Friendly Name : ``email``
- SAML Attribute Name : ``email``

.. image:: {static}/images/Keycloak-Client-Zabbix-Mapper.png
    :alt: Mapper du client Zabbix dans Keycloak
    :scale: 50 %
    :target: /images/Keycloak-Client-Zabbix-Mapper.png

|

Sauvegarder cette configuration.

Dernière étape de la configuration de Keycloak. Aller dans :code:`Client Scopes` et sélectionner :code:`role_list` et dans l'onglet Mapper, editer le mapper :code:`role list`. Activer :code:`Single Role Attribute`.

.. image:: {static}/images/Keycloak-Client-Scopes.png
    :alt: Client Scopes dans Keycloak
    :scale: 50 %
    :target: /images/Keycloak-Client-Scopes.png


|
|


Configuration de Zabbix
=======================

Connectez-vous sur Zabbix avec un compte Super Admin. Dans Administration > Authentication selectionner l'onglet SAML, l'activer et le configurer de cette façon : 

- IdP entity ID : ``https://<keycloakaddress>/auth/realms/<realmname>``
- SSO service URL :``https://<keycloakaddress>/auth/realms/<realmname>/protocol/saml``
- SLO service URL : ``https://<keycloakaddress>/auth/realms/<realmname>/protocol/saml``
- Username attribute : ``email``
- SP entity ID : ``zabbix``
- SP name ID format : ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

Il faut ensuite créer les utilisateurs dans Zabbix. En effet, comme pour l'authentification LDAP / Active Directory, Zabbix s'appuit sur ces services pour authentifier des utilisateurs existants. Il faut au préalable les ajouter dans la base des utilisateurs avec les droits associés à leur compte.

Dans Administration > Users, créer un compte ayant pour Alias l'adresse email de l'utilisateur. Il est nécessaire de lui mettre un mot de passe, même si celui ci ne sera pas utilisé.

Dans une nouvelle fenêtre en navigation privée, vous pouvez vous connecter sur Zabbix en cliquant d'abord sur **Sign in with Single Sign-On (SAML)** puis sur la fenêtre Keycloak qui s'affiche, un bouton Google permet de finaliser l'authentification.

.. image:: {static}/images/Zabbix-Auth-SAML.png
    :alt: Page d'Authentification Zabbix avec option SAML
    :scale: 50 %
    :target: /images/Zabbix-Auth-SAML.png


|

.. image:: {static}/images/Keycloak-Auth-Google.png
    :alt: Page d'Authentification Keycloak avec option Google
    :scale: 50 %
    :target: /images/Keycloak-Auth-Google.png
    
|

Le bouton Logout de Zabbix doit vous ramener sur la page d'authentification de Zabbix et également vous déconnecter de Keycloak.

Pour moi, la prochaine étape est de faire la même chose avec Netbox.
