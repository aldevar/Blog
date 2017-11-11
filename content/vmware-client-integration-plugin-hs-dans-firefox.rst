Vmware Client Integration Plugin HS dans Firefox
################################################
:date: 2015-08-23 14:00
:author: alain
:category: Tech
:slug: vmware-client-integration-plugin-hs-dans-firefox
:status: published

Depuis quelques semaines, le plugin d'intégration client VMware ne
fonctionne plus dans Firefox. La case "Utiliser les identifiants
Windows" est grisée et d'après l'interface de vCenter, le plugin n'est
pas installé sur votre machine.

Ce problème est apparu avec Firefox 39 et concerne toutes les nouvelles
versions de Firefox depuis. Cela a plusieurs conséquences.

-  Impossible d'ouvrir les consoles des VM (la console HTML5, VMRC
   fonctionne quant à lui)
-  Impossible de déposer un fichier depuis son PC vers un Datastore via
   le navigateur HTML5
-  Impossible de déployer un template OVF depuis son PC via l'option de
   déploiement de fichier OVF local.

Pour corriger ce problème, il faut désactiver les options
security.ssl3.dhe de Firefox.

Pour cela, se rendre dans about:config, rechercher security.ssl3.dhe.
Vous devriez vous retrouver avec 2 entrées :

-  security.ssl3.dhe\_rsa\_aes\_128\_sha
-  security.ssl3.dhe\_rsa\_aes\_256\_sha

Faire un clique droit sur chacune de ses entrées et cliquer sur
**Inverser** (Toggle).

Il ne reste plus qu'à rafraîchir la page vcenter.

Source `Vmware KB
2125623 <http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2125623>`__
