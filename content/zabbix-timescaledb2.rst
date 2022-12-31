Zabbix et TimescaleDB 2 - Erreur Z3005
########################################
:date: 2021-02-23 21:45
:author: Aldevar
:category: Supervision
:slug: zabbix-timescaledb2
:status: published

Depuis que Zabbix supporte officiellement le plugin PostreSQL TimescaleDB, je n'utilise plus que ce mode d'installation pour les différentes instances que j'ai à déployer.

TimescaleDB est une time serie database et est donc particulièrement adapaté pour stocker des métriques de supervision. Le logiciel se présente comme un plugin à PostgreSQL et permet de transformer certaines tables d'une base en mode time series. Le gros avantage est que cela permet de stocker l'ensemble des informations dans un endroit unique, que ce soit la configuration du logiciel (utilisateurs, droits d'accès, paramètres...) et aussi les métriques récupérées par le système de supervision. En plus de cela, timescaleDB propose le partitionnemet automatique des tables ainsi que la compression des données ayant plus de 7 jours.

On a donc d'un coté un gain opérationnel car on n'a plus q'une base de données à gérer et de l'autre un gain en ressources car les tables sont adaptées à ce qu'elles stockent et peuvent être compréssées pour des économies de stockage substantielles.

Lors de ma dernière installation, j'ai pu voir que le plugin TimescaleDB était sorti en version 2. La documentation de Zabbix ne spécifiant pas la version de TimescaleDB à installer, j'ai naturellement installé cette dernière version.

Mal m'en a pris! Cette version 2 n'est pas compatible avec Zabbix 5.2! J'ai pu le voir rapidement lors du démarrage du service :code:`zabbix-server` avec ces logs que vous n'êtes pas obligé lire en entier. C'est un gros vomi d'erreurs comme on n'aime pas en voir (TL;DR - Plusieurs erreurs Z3005 - query failed - clairement en rapport avec TimescaleDB)

.. code-block:: text

    [Z3005] query failed: [0] PGRES_FATAL_ERROR:ERROR: relation "_timescaledb_config.bgw_policy_compress_chunk s" does not exist
    LINE 1: select (p.older_than).integer_interval from _timescaledb_con...
    ^
    [select (p.older_than).integer_interval from _timescaledb_config.bgw_policy_compress_chunks p inner join _timescaledb_catalog.hypertable h on (h.id = p.hypertable_id) where h.table_name='history']
    0000000000000 [Z3005] query failed: [0] PGRES_FATAL_ERROR:ERROR: function add_compress_chunks_policy(unknown, integer) does not exist
    LINE 1: select add_compress_chunks_policy('history', integer '612000...
    ^
    HINT: No function matches the given name and argument types. You might need to add explicit type casts.
    [select add_compress_chunks_policy('history', integer '612000')]
    0000000000000 failed to add compression policy to table 'history'
    0000000000000 [Z3005] query failed: [0] PGRES_FATAL_ERROR:ERROR: relation "_timescaledb_config.bgw_policy_compress_chunk s" does not exist
    LINE 1: select (p.older_than).integer_interval from _timescaledb_con...
    ^
    [select (p.older_than).integer_interval from _timescaledb_config.bgw_policy_compress_chunks p inner join _timescaledb_catalog.hypertable h on (h.id = p.hypertable_id) where h.table_name='history_uint']
    0000000000000 [Z3005] query failed: [0] PGRES_FATAL_ERROR:ERROR: function add_compress_chunks_policy(unknown, integer) does not exist
    LINE 1: select add_compress_chunks_policy('history_uint', integer '6...
    ^
    HINT: No function matches the given name and argument types. You might need to add explicit type casts.
    [select add_compress_chunks_policy('history_uint', integer '612000')]
    0000000000000 failed to add compression policy to table 'history_uint'


Cette erreur provient d'une incompatibilité entre Zabbix 5.2 et TimescaleDB 2. Cette incompatibilité est causée par des modifications de certaines fonctions de l'API de TimescaleDB, entre autre la fonction `add_compression_policy <https://docs.timescale.com/latest/api#add_compression_policy>`_. A partir de là, on a deux solutions. 

- Soit on refait l'installation de TimescaleDB avec la dernière version 1.X.
- Soit on tente de corriger ces erreurs.

J'ai opté pour la seconde option. En fouillant, j'ai trouvé un `ticket sur le Jira <https://support.zabbix.com/projects/ZBX/issues/ZBX-18854>`_ de Zabbix qui aborde ce problème. Dans les échanges, un utilisateur propose une solution avec quelques lignes à envoyer vers la db pour corriger tout ça. Voici comment la mettre en oeuvre. 

On commence par se préparer à mettre à jour la base de données

.. code-block:: text

    # systemctl stop zabbix-server
    # sudo -u postgres psql zabbix

On peut maintenant envoyer le code SQL suivant :

.. code-block:: sql

    CREATE TYPE _timescaledb_catalog.ts_interval AS
    (is_time_interval BOOLEAN, time_interval INTERVAL, integer_interval BIGINT);
    ALTER TYPE _timescaledb_catalog.ts_interval OWNER TO zabbix;
    
    CREATE OR REPLACE VIEW _timescaledb_config.bgw_policy_compress_chunks AS
    SELECT job_id,(config->>'hypertable_id')::INTEGER AS hypertable_id,
    (FALSE,NULL,config->>'compress_after')::_timescaledb_catalog.ts_interval AS older_than
    FROM timescaledb_information.jobs WHERE proc_name='policy_compression';
    ALTER VIEW _timescaledb_config.bgw_policy_compress_chunks OWNER TO zabbix;
    
    CREATE OR REPLACE FUNCTION add_compress_chunks_policy
    (hypertable regclass,older_than anyelement,if_not_exists BOOLEAN DEFAULT FALSE)
    RETURNS INTEGER LANGUAGE sql AS $$
    SELECT add_compression_policy(hypertable,older_than,if_not_exists)
    $$;
    ALTER FUNCTION add_compress_chunks_policy OWNER TO zabbix;
    
    CREATE OR REPLACE FUNCTION drop_chunks
    (older_than anyelement DEFAULT NULL::UNKNOWN,table_name NAME DEFAULT NULL::NAME)
    RETURNS SETOF TEXT LANGUAGE sql AS $$
    SELECT drop_chunks(table_name::regclass,older_than,NULL,FALSE)
    $$;
    ALTER FUNCTION drop_chunks(anyelement,NAME) OWNER TO zabbix;


On peut maintenant redémarrer le service zabbix-server (:code:`systemctl start zabbix-server`) et on voit dans les logs que les erreurs ont disparu.
Zabbix devrait rapidement corriger cela, dans un premier temps en mettant à jour la documentation et dans un second temps en adaptant l'application.
