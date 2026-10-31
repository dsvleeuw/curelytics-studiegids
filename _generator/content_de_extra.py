"""Uitbreiding per fiche (zelfde volgorde als FICHES in content_de.py)."""

EXTRA = [
    # 001 Wat doet een data engineer
    {
        "visuals": [
            ("venn", {"sets": ["Software-\nengineering", "Data &\ndatabases", "Cloud &\ninfra"], "center": "Data\nEngineer"},
             "De data engineer zit op het snijvlak van drie vakgebieden."),
            ("hub", {"center": "Data\nEngineer", "spokes": ["BI Specialist", "Data Analist", "Data Scientist", "Security", "Bron-eigenaren", "Platform/IT"]},
             "Met wie je samenwerkt: je levert data aan iedereen en haalt het bij de bron-eigenaren."),
        ],
        "praktijk": "<p>Een waterschap wil sensordata van gemalen combineren met weerdata. De data engineer bouwt een pipeline die "
                    "elk kwartier sensordata ophaalt via een API, dagelijks KNMI-data binnenhaalt, alles in Delta-tabellen "
                    "zet en een goud-tabel levert waarop de BI-specialist het dashboard bouwt.</p>",
        "begrippen": [("Pipeline", "Geautomatiseerde reeks stappen die data verplaatst en bewerkt."),
                      ("SLA", "Afspraak over beschikbaarheid/tijdigheid (bv. data om 07:00 klaar)."),
                      ("Data product", "Dataset met eigenaar, documentatie en kwaliteitsgarantie."),
                      ("API", "Interface om data programmatisch op te halen.")],
        "fouten": ["Alleen bouwen, niet monitoren – fouten merk je dan via boze gebruikers.",
                   "Geen documentatie: niemand anders kan de pipeline onderhouden.",
                   "Elke pipeline anders bouwen in plaats van met herbruikbare patronen."],
        "quiz": [("Wat doet een data engineer in één zin?", "Bouwt en onderhoudt de pipelines en het platform waarmee data betrouwbaar bij gebruikers komt."),
                 ("Wat is een SLA?", "Afspraak over beschikbaarheid of tijdigheid van data."),
                 ("Wie zijn je 'klanten'?", "BI-specialisten, analisten, data scientists.")],
    },
    # 002 Batch vs streaming
    {
        "visuals": [
            ("flow", {"steps": ["Producer\n(sensor/app)", "Topic\n(Kafka)", "Stream-\nprocessing", "Delta /\nwarehouse",
                                "Dashboard\n/ alert"], "highlight": [1]},
             "Een typische streaming-architectuur."),
            ("compare", {"left": ("Kappa", ["Alles is een stream", "Eén verwerkingspad", "Eenvoudiger"]),
                         "right": ("Lambda", ["Batch + streaming", "Twee paden", "Complex, dubbel werk"])},
             "Twee architectuurpatronen voor real-time data."),
        ],
        "praktijk": "<p>Een vervoerder wil meldingen als een bus meer dan 5 minuten te laat is. Busposities komen elke 10 seconden "
                    "binnen via Event Hubs; Spark Structured Streaming berekent vertraging per rit en schrijft afwijkingen naar "
                    "een alerttabel. De maandrapportage over stiptheid draait gewoon als nachtelijke batch.</p>",
        "begrippen": [("Topic", "Benoemde stroom berichten in Kafka."), ("Partition", "Deel van een topic voor parallel verwerken."),
                      ("Offset", "Positie van een consumer in een partitie."),
                      ("Exactly-once", "Elk event precies één keer verwerkt."),
                      ("Watermark (streaming)", "Hoe lang je wacht op late events.")],
        "code": ("Python", """# Spark Structured Streaming: vertraging per rit, elke minuut
from pyspark.sql import functions as F

stream = (spark.readStream.format("kafka")
          .option("subscribe", "busposities").load()
          .select(F.from_json(F.col("value").cast("string"), schema).alias("e")).select("e.*"))

vertraging = (stream.withWatermark("tijd", "5 minutes")
              .groupBy(F.window("tijd", "1 minute"), "rit_id")
              .agg(F.max("vertraging_sec").alias("max_vertraging")))

(vertraging.writeStream.format("delta")
 .option("checkpointLocation", "/chk/vertraging").toTable("goud.vertraging"))"""),
        "fouten": ["Streaming bouwen terwijl elk uur verversen ruim genoeg was.",
                   "Geen checkpointing → na een crash data dubbel of kwijt.",
                   "Geen rekening houden met events die te laat binnenkomen."],
        "quiz": [("Wat is Kafka?", "Platform om event-berichten op te slaan en te distribueren via topics."),
                 ("Azure-variant van Kinesis?", "Event Hubs."),
                 ("Wat is micro-batch?", "Streaming verwerkt in heel kleine batches (bv. elke paar seconden)."),
                 ("Eerste vraag bij 'real-time'?", "Hoe snel moet de data er écht zijn, en welk besluit hangt ervan af?")],
    },
    # 003 Lake / warehouse / lakehouse
    {
        "visuals": [
            ("timeline", {"points": [("DWH", "jaren 90"), ("Hadoop / lake", "± 2010"), ("Cloud DWH", "± 2015"), ("Lakehouse", "± 2020")]},
             "Korte geschiedenis: van warehouse via lake naar lakehouse."),
            ("compare", {"left": ("CSV / JSON", ["Rij- of tekstgebaseerd", "Groot, traag", "Geen schema"]),
                         "right": ("Parquet / Delta", ["Kolomgebaseerd", "Gecomprimeerd, snel", "Schema + statistieken"])},
             "Waarom analytische platformen Parquet gebruiken."),
        ],
        "praktijk": "<p>Een universiteit heeft een data lake vol CSV's zonder documentatie – niemand weet meer wat actueel is (een "
                    "'data swamp'). Migratie naar een lakehouse: alles in Delta, tabellen geregistreerd in Unity Catalog met "
                    "eigenaar en beschrijving, en toegang per laag.</p>",
        "begrippen": [("Schema-on-read", "Structuur pas bepalen bij het lezen (lake)."),
                      ("Schema-on-write", "Structuur afdwingen bij het schrijven (DWH)."),
                      ("Parquet", "Kolomgebaseerd, gecomprimeerd bestandsformaat."),
                      ("Data swamp", "Ongeorganiseerd data lake waar niemand meer wijs uit wordt."),
                      ("Open table format", "Delta, Iceberg, Hudi: tabellen bovenop bestanden.")],
        "fouten": ["Een lake vullen zonder catalog of eigenaar.", "Alles als CSV opslaan.",
                   "Data dubbel bewaren in lake én warehouse zonder reden."],
        "quiz": [("Lake vs warehouse?", "Lake: alle formaten, goedkoop, schema-on-read. Warehouse: tabellen, schema-on-write, snel."),
                 ("Wat voegt een lakehouse toe aan een lake?", "Warehouse-functies: ACID, schema, prestaties."),
                 ("Waarom Parquet?", "Kolomgebaseerd en gecomprimeerd → snel en goedkoop voor analyses.")],
    },
    # 004 Medallion
    {
        "visuals": [
            ("funnel", {"stages": ["Brons – alles", "Zilver – opgeschoond", "Goud – wat de business gebruikt"],
                        "notes": ["Volume groot, kwaliteit ruw", "Ontdubbeld, getypt, gekoppeld", "Klein, betrouwbaar, gemodelleerd"]},
             "Van veel ruwe data naar weinig, zeer betrouwbare data."),
        ],
        "praktijk": "<p>Brons: dagelijkse JSON-export van het EPD, ongewijzigd. Zilver: één rij per opname, datums als datum, "
                    "dubbelingen eruit, cliënt-ID gepseudonimiseerd. Goud: feit_opname + dimensies, klaar voor Power BI. "
                    "Bij een bug in de zilverlogica herbouw je zilver en goud vanuit brons, zonder het EPD opnieuw te bevragen.</p>",
        "begrippen": [("Append-only", "Alleen toevoegen, nooit wijzigen (brons)."),
                      ("Conformeren", "Data uit bronnen gelijk trekken (types, codes)."),
                      ("Expectations", "Kwaliteitsregels die bij elke laag gecontroleerd worden.")],
        "tabel": {"kop": ["Laag", "Wie gebruikt het", "Kwaliteit", "Voorbeeld"],
                  "rijen": [["Brons", "Engineers", "Ruw", "raw_epd_opnames_json"],
                            ["Zilver", "Engineers, data scientists", "Gevalideerd", "opname (1 rij per opname)"],
                            ["Goud", "BI, analisten", "Business-ready", "feit_opname, dim_afdeling"]]},
        "fouten": ["Transformaties in brons doen – dan ben je de ruwe waarheid kwijt.",
                   "Analisten direct op brons laten werken.",
                   "Geen kwaliteitschecks tussen de lagen."],
        "quiz": [("Wat staat er in brons?", "Ruwe data zoals uit de bron, append-only."),
                 ("Wat gebeurt er in zilver?", "Opschonen, ontdubbelen, types corrigeren, koppelen."),
                 ("Wat staat er in goud?", "Business-ready data: ster-schema's, KPI-tabellen.")],
    },
    # 005 Spark & Databricks
    {
        "visuals": [
            ("compare", {"left": ("Transformaties (lazy)", ["select, filter", "join, groupBy", "Bouwt alleen een plan"]),
                         "right": ("Actions (voeren uit)", ["count, show", "write, collect", "Start de berekening"])},
             "Lazy evaluation: niets gebeurt tot je een action aanroept."),
            ("stack", {"layers": ["Notebooks & Jobs", "Unity Catalog (governance)", "Spark / Photon (compute)", "Delta Lake (opslag)"],
                       "notes": ["Waar je werkt", "Rechten, lineage, catalog", "Clusters, serverless", "In jouw cloud-opslag"]},
             "Databricks in lagen."),
        ],
        "praktijk": "<p>Een job die 2 miljoen ritten koppelt aan 300 haltes duurt 40 minuten. In de Spark UI blijkt een grote "
                    "shuffle. Oplossing: de kleine haltes-tabel broadcasten. De job duurt daarna 4 minuten.</p>",
        "begrippen": [("Driver / executor", "Driver plant, executors (workers) voeren uit."),
                      ("Partition", "Deel van de data dat één taak verwerkt."),
                      ("Shuffle", "Data herverdelen tussen nodes (duur)."),
                      ("Broadcast join", "Kleine tabel naar elke node kopiëren om shuffle te vermijden."),
                      ("Photon", "Snelle C++-engine van Databricks.")],
        "code": ("Python", """from pyspark.sql import functions as F

ritten = spark.read.table("zilver.ritten")
haltes = spark.read.table("zilver.haltes")          # klein

resultaat = (ritten
    .filter(F.col("datum") >= "2026-01-01")           # vroeg filteren
    .join(F.broadcast(haltes), "halte_id")            # shuffle vermijden
    .groupBy("halte_naam")
    .agg(F.count("*").alias("aantal_ritten")))

resultaat.write.mode("overwrite").saveAsTable("goud.ritten_per_halte")  # action"""),
        "fouten": ["<code>.collect()</code> op een grote dataset → driver loopt vol.",
                   "All-purpose clusters gebruiken voor geplande jobs (duurder dan job clusters).",
                   "Duizenden kleine bestanden laten ontstaan (small files problem)."],
        "quiz": [("Wat is lazy evaluation?", "Transformaties bouwen een plan; pas een action voert het uit."),
                 ("Waarom is een shuffle duur?", "Data moet over het netwerk tussen nodes herverdeeld worden."),
                 ("Wanneer een broadcast join?", "Als één van de twee tabellen klein is."),
                 ("Wat is Unity Catalog?", "De governance-laag van Databricks: rechten, lineage, catalog.")],
    },
    # 006 Delta Lake
    {
        "visuals": [
            ("timeline", {"points": [("v0", "CREATE"), ("v1", "INSERT"), ("v2", "MERGE"), ("v3", "DELETE"), ("v4", "OPTIMIZE")]},
             "Elke schrijfactie is een nieuwe versie in het transaction log – je kunt naar elke versie terug."),
        ],
        "praktijk": "<p>Na een foute deploy staan er in de goud-tabel dubbele rijen. Met <code>DESCRIBE HISTORY</code> zie je welke "
                    "versie het was, en met <code>RESTORE TABLE goud.feit TO VERSION AS OF 41</code> staat alles binnen een minuut "
                    "weer goed.</p>",
        "begrippen": [("Transaction log", "_delta_log: lijst van alle wijzigingen aan de tabel."),
                      ("Time travel", "Een eerdere versie van de tabel opvragen."),
                      ("OPTIMIZE", "Kleine bestanden samenvoegen tot grotere."),
                      ("VACUUM", "Oude, niet meer gebruikte bestanden verwijderen."),
                      ("Deletion vectors", "Rijen markeren als verwijderd zonder bestanden te herschrijven.")],
        "code": ("SQL", """MERGE INTO zilver.klant AS doel
USING stg.klant      AS bron
ON    doel.klant_nr = bron.klant_nr
WHEN MATCHED AND doel.hash <> bron.hash THEN UPDATE SET *
WHEN NOT MATCHED                        THEN INSERT *;

DESCRIBE HISTORY zilver.klant;                       -- versies bekijken
SELECT * FROM zilver.klant VERSION AS OF 12;         -- time travel
OPTIMIZE zilver.klant;                               -- kleine bestanden samenvoegen"""),
        "fouten": ["Nooit OPTIMIZE draaien → steeds tragere queries.",
                   "VACUUM met te korte retentie → time travel werkt niet meer.",
                   "Denken dat DELETE meteen fysiek verwijdert (bij deletion vectors niet)."],
        "quiz": [("Wat betekent ACID?", "Atomic, Consistent, Isolated, Durable."),
                 ("Hoe ga je terug naar een oude versie?", "Time travel (VERSION AS OF) of RESTORE TABLE."),
                 ("Wat doet OPTIMIZE?", "Kleine bestanden samenvoegen voor snellere queries."),
                 ("Waarop is Delta gebouwd?", "Parquet-bestanden + een transaction log.")],
    },
    # 007 Orchestratie
    {
        "visuals": [
            ("tree", {"root": "Nachtelijke DAG", "children": [("Extract A", ["API klanten"]), ("Extract B", ["DB orders"]),
                                                              ("Transform", ["wacht op A + B", "dbt build"]),
                                                              ("Publiceren", ["Power BI refresh", "Alert bij fout"])]},
             "Afhankelijkheden in een DAG: Transform start pas als beide extracts klaar zijn."),
        ],
        "praktijk": "<p>Een metadata-gedreven ADF-pipeline bij een gemeente: één generieke 'copy'-pipeline leest een configtabel met "
                    "85 brontabellen (naam, bron, laadtype, watermark). Een nieuwe tabel toevoegen = één rij in de configtabel, "
                    "geen nieuwe pipeline.</p>",
        "begrippen": [("DAG", "Directed Acyclic Graph: taken met afhankelijkheden zonder lussen."),
                      ("Scheduler", "Start taken op tijd of bij een event."),
                      ("Backfill", "Een pipeline voor oude periodes opnieuw draaien."),
                      ("Linked service", "ADF-verbinding naar een bron of doel."),
                      ("Sensor", "Taak die wacht tot een voorwaarde waar is (bv. bestand aanwezig).")],
        "code": ("Python", """from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("nacht", start_date=datetime(2026, 1, 1), schedule="0 2 * * *",
         catchup=False, default_args={"retries": 2}) as dag:
    extract_a = BashOperator(task_id="extract_klanten", bash_command="python extract.py klanten")
    extract_b = BashOperator(task_id="extract_orders",  bash_command="python extract.py orders")
    transform = BashOperator(task_id="dbt_build",       bash_command="dbt build")
    refresh   = BashOperator(task_id="refresh_pbi",     bash_command="python refresh_pbi.py")

    [extract_a, extract_b] >> transform >> refresh"""),
        "fouten": ["Taken bouwen die niet veilig opnieuw kunnen draaien.",
                   "Alles in één gigantische taak stoppen – dan kun je niet gericht herstarten.",
                   "Geen alerting: een gefaalde run wordt pas na dagen ontdekt."],
        "quiz": [("Wat is een DAG?", "Graaf van taken met afhankelijkheden, zonder lussen."),
                 ("Managed Airflow op GCP?", "Cloud Composer."),
                 ("Wat is een backfill?", "Een pipeline voor historische periodes opnieuw draaien."),
                 ("Wat is metadata-gedreven?", "Eén generieke pipeline gestuurd door een configtabel.")],
    },
    # 008 dbt
    {
        "visuals": [
            ("cols", {"cols": [("Generiek", ["unique", "not_null"]), ("Relaties", ["relationships", "accepted_values"]),
                               ("Eigen", ["SQL-test", "dbt-expectations"])], "arrows": False},
             "Soorten dbt-tests."),
            ("compare", {"left": ("view / table", ["Elke run volledig", "Simpel", "Kleine tabellen"]),
                         "right": ("incremental", ["Alleen nieuwe rijen", "Sneller, goedkoper", "Grote feiten"])},
             "Materialisaties kiezen."),
        ],
        "praktijk": "<p>Een team heeft 200 losse SQL-scripts die in een vaste volgorde moeten draaien – niemand durft iets aan te "
                    "passen. Omzetting naar dbt: elke query wordt een model met <code>ref()</code>, er komen tests op sleutels, "
                    "en bij elke pull request draait CI. Wijzigingen worden weer gewoon.</p>",
        "begrippen": [("Model", "Eén .sql-bestand met een SELECT."), ("ref()", "Verwijzing naar een ander model."),
                      ("source()", "Verwijzing naar een ruwe brontabel."), ("Materialization", "Hoe een model wordt opgeslagen."),
                      ("Snapshot", "dbt-mechanisme voor SCD2-historie.")],
        "code": ("SQL", """-- models/marts/fct_orders.sql
{{ config(materialized='incremental', unique_key='order_id') }}

select o.order_id, o.klant_id, o.besteldatum, o.bedrag
from {{ ref('stg_orders') }} o
{% if is_incremental() %}
where o.besteldatum > (select max(besteldatum) from {{ this }})
{% endif %}

-- models/marts/schema.yml
-- - name: fct_orders
--   columns:
--     - name: order_id
--       tests: [unique, not_null]"""),
        "fouten": ["Hardgecodeerde tabelnamen in plaats van ref()/source().",
                   "Geen tests – dan is dbt alleen een duurdere manier om SQL te draaien.",
                   "Één enorm model met alle logica in plaats van stappen (staging → marts)."],
        "quiz": [("Wat is een dbt-model?", "Een SQL SELECT in een bestand die dbt als tabel/view bouwt."),
                 ("ref() vs source()?", "ref() tussen modellen, source() naar ruwe brontabellen."),
                 ("Noem vier standaardtests.", "unique, not_null, relationships, accepted_values."),
                 ("Hoe doe je SCD2 in dbt?", "Met snapshots.")],
    },
    # 009 Idempotentie
    {
        "visuals": [
            ("flow", {"steps": ["Run voor\n2026-10-30", "Overschrijf\npartitie 30-10", "Run nogmaals\n(retry)", "Zelfde\nresultaat"],
                      "highlight": [3]},
             "Idempotent laden per datumpartitie: opnieuw draaien is veilig."),
        ],
        "praktijk": "<p>Een pipeline faalt halverwege en wordt automatisch herstart. Omdat hij met <code>INSERT</code> werkte, staan "
                    "de eerste 50.000 rijen er nu dubbel in en kloppen de omzetcijfers niet. Na ombouw naar "
                    "<code>MERGE</code> op order_id is een retry altijd veilig.</p>",
        "begrippen": [("Idempotent", "Meerdere keren uitvoeren = zelfde resultaat als één keer."),
                      ("Upsert", "Update als het bestaat, insert als het nieuw is."),
                      ("Run-datum", "Expliciete datum waarvoor een run draait (niet 'nu')."),
                      ("pytest", "Python-testframework.")],
        "code": ("Python", """def laad_dag(spark, run_datum: str) -> None:
    \"\"\"Idempotent: overschrijft alleen de partitie van run_datum.\"\"\"
    df = (spark.read.table("brons.orders")
          .where(f"order_datum = '{run_datum}'")
          .dropDuplicates(["order_id"]))
    (df.write.format("delta").mode("overwrite")
       .option("replaceWhere", f"order_datum = '{run_datum}'")
       .saveAsTable("zilver.orders"))

def test_dubbel_draaien_geeft_zelfde_aantal(spark):
    laad_dag(spark, "2026-10-30"); a = spark.table("zilver.orders").count()
    laad_dag(spark, "2026-10-30"); b = spark.table("zilver.orders").count()
    assert a == b"""),
        "fouten": ["<code>datetime.now()</code> in de logica → herstarten op een andere dag geeft andere data.",
                   "Secrets in code zetten.", "Notebooks zonder functies, tests of versiebeheer."],
        "quiz": [("Wat betekent idempotent?", "Twee keer draaien geeft hetzelfde resultaat als één keer."),
                 ("Noem twee idempotente technieken.", "MERGE op een sleutel; partitie overschrijven per datum."),
                 ("Waarom een expliciete run-datum?", "Zodat herstarts en backfills hetzelfde resultaat geven.")],
    },
    # 010 Datakwaliteit
    {
        "visuals": [
            ("flow", {"steps": ["Nieuwe data", "Checks\n(tests)", "Goed → door\nnaar zilver", "Fout →\nquarantaine",
                                "Alert +\nissue"], "highlight": [1]},
             "Kwaliteitspoort in de pipeline: foute records apart zetten in plaats van alles stoppen."),
            ("hub", {"center": "Observability", "spokes": ["Versheid", "Volume", "Schema", "Distributie", "Lineage"]},
             "De vijf pijlers van data observability."),
        ],
        "praktijk": "<p>Op maandag levert het HR-systeem plots 40% minder rijen. Een volumecheck vangt dit om 06:30 af; het "
                    "dashboard toont een waarschuwing 'data van vrijdag' in plaats van foute cijfers, en het team belt de "
                    "bron-eigenaar vóór de managers om 09:00 kijken.</p>",
        "begrippen": [("Reconciliatie", "Aantallen/totalen vergelijken met de bron."),
                      ("Data contract", "Afspraak met de bron over schema en kwaliteit."),
                      ("Quarantaine", "Tabel waarin afgekeurde records worden geparkeerd."),
                      ("Freshness", "Hoe actueel de data is.")],
        "code": ("SQL", """-- Eenvoudige kwaliteitschecks (falen = rijen teruggeven)
SELECT 'dubbele sleutel' AS check, order_id FROM zilver.orders GROUP BY order_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'bedrag negatief', order_id FROM zilver.orders WHERE bedrag < 0
UNION ALL
SELECT 'niet ververst', NULL WHERE (SELECT MAX(laad_tijd) FROM zilver.orders) < DATEADD(hour, -26, GETDATE());"""),
        "fouten": ["Alleen testen of de pipeline draait, niet of de data klopt.",
                   "Bij elke fout de hele pipeline stoppen in plaats van quarantaine.",
                   "Kwaliteitsproblemen stil oplossen zonder de bron-eigenaar te informeren."],
        "quiz": [("Noem de zes kwaliteitsdimensies.", "Juistheid, volledigheid, tijdigheid, consistentie, uniciteit, validiteit."),
                 ("Wat is data observability?", "Automatisch volgen van versheid, volume, schema en distributie."),
                 ("Wat is een data contract?", "Afspraak met de bron-eigenaar over schema en kwaliteit.")],
    },
    # 011 IaC
    {
        "visuals": [
            ("compare", {"left": ("ClickOps (portal)", ["Niet herhaalbaar", "Geen review", "Drift tussen omgevingen"]),
                         "right": ("Infrastructure as Code", ["Reproduceerbaar", "Review via Git", "Dev = test = prod"])},
             "Waarom IaC."),
            ("cols", {"cols": [("dev", ["klein cluster", "testdata"]), ("test", ["zelfde code", "acceptatie"]),
                               ("prod", ["grote capaciteit", "goedkeuring"])], "labels": ["promote", "promote"]},
             "Eén codebase, drie omgevingen met andere variabelen."),
        ],
        "praktijk": "<p>De productie-workspace van een zorginstelling wordt per ongeluk verkeerd geconfigureerd in de portal. "
                    "Omdat alles in Terraform staat, laat <code>terraform plan</code> precies zien wat er afwijkt en zet "
                    "<code>apply</code> het binnen minuten terug.</p>",
        "begrippen": [("Declaratief", "Je beschrijft de eindtoestand, niet de stappen."),
                      ("State", "Terraform's administratie van wat er bestaat."),
                      ("Module", "Herbruikbaar blok IaC-code."),
                      ("Drift", "Werkelijkheid wijkt af van de code."),
                      ("Bicep", "Azure-taal voor IaC.")],
        "code": ("HCL", """resource "azurerm_resource_group" "data" {
  name     = "rg-data-${var.omgeving}"
  location = "westeurope"
}

resource "azurerm_storage_account" "lake" {
  name                     = "stlake${var.omgeving}"
  resource_group_name      = azurerm_resource_group.data.name
  location                 = azurerm_resource_group.data.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  is_hns_enabled           = true          # ADLS Gen2
}"""),
        "fouten": ["Terraform state lokaal bewaren → kwijt of conflicten in het team.",
                   "Toch nog handmatig wijzigen in de portal (drift).",
                   "Secrets hardcoded in .tf-bestanden."],
        "quiz": [("Wat doet terraform plan?", "Laat zien wat er zou veranderen zonder het uit te voeren."),
                 ("Wat is drift?", "Werkelijke infrastructuur wijkt af van de code."),
                 ("IaC-tool per cloud?", "Bicep (Azure), CloudFormation (AWS); Terraform werkt op alle clouds.")],
    },
    # 012 Security
    {
        "visuals": [
            ("stack", {"layers": ["Data (RLS, maskering, grants)", "Identiteit (Entra ID, rollen)", "Netwerk (private endpoints)",
                                  "Infrastructuur (encryptie)"],
                       "notes": ["Wie ziet welke rijen/kolommen?", "Wie ben je, wat mag je?", "Waar mag verkeer vandaan?",
                                 "Opslag versleuteld"]},
             "Defense in depth: meerdere beveiligingslagen."),
            ("cols", {"cols": [("Engineers", ["Schrijven brons", "Schrijven zilver"]), ("Analisten", ["Lezen goud"]),
                               ("Pipelines", ["Managed identity", "Alleen eigen pad"]), ("Lezers", ["Alleen rapporten"])],
                      "arrows": False},
             "Voorbeeld rollenmodel voor een lakehouse."),
        ],
        "praktijk": "<p>Een pipeline draaide onder het persoonlijke account van een vertrokken medewerker. Toen dat account werd "
                    "uitgeschakeld, stopte alles. Oplossing: managed identities voor alle pipelines, rechten via groepen, en "
                    "een kwartaal-access-review.</p>",
        "begrippen": [("IAM", "Identity & Access Management."), ("RBAC", "Rechten via rollen."),
                      ("ABAC", "Rechten op basis van attributen (bv. gevoeligheidslabel)."),
                      ("Least privilege", "Precies genoeg rechten."), ("Managed identity", "Identiteit voor een dienst, zonder wachtwoord.")],
        "code": ("SQL", """-- Unity Catalog: rechten per groep en laag
GRANT USE CATALOG ON CATALOG zorg TO `analisten`;
GRANT SELECT ON SCHEMA zorg.goud TO `analisten`;
GRANT ALL PRIVILEGES ON SCHEMA zorg.zilver TO `data-engineers`;

-- kolom maskeren voor wie niet in de groep zit
CREATE FUNCTION zorg.mask_bsn(bsn STRING) RETURN
  CASE WHEN is_account_group_member('privacy-ok') THEN bsn ELSE '***' END;
ALTER TABLE zorg.zilver.client ALTER COLUMN bsn SET MASK zorg.mask_bsn;"""),
        "fouten": ["Rechten aan personen geven in plaats van aan groepen.",
                   "Iedereen 'Contributor' geven omdat het makkelijk is.",
                   "Pipelines onder persoonlijke accounts laten draaien."],
        "quiz": [("Authenticatie vs autorisatie?", "Authenticatie = wie ben je; autorisatie = wat mag je."),
                 ("Wat is least privilege?", "Alleen de rechten die nodig zijn, niet meer."),
                 ("Waarom managed identities?", "Geen wachtwoorden in code en niet afhankelijk van personen."),
                 ("AWS-tool voor tabel/kolomrechten op de lake?", "Lake Formation.")],
    },
    # 013 Governance
    {
        "visuals": [
            ("flow", {"steps": ["Bron:\nzaaksysteem", "brons.zaken", "zilver.zaak", "goud.feit_zaak", "Rapport\nDoorlooptijd"],
                      "highlight": [4]},
             "Lineage: van welke bron via welke tabellen komt een cijfer in het rapport?"),
            ("cols", {"cols": [("Openbaar", ["Open data"]), ("Intern", ["Bedrijfsdata"]), ("Vertrouwelijk", ["Personeel, financiën"]),
                               ("Bijzonder", ["Gezondheid, BSN"])], "arrows": False},
             "Dataclassificatie: hoe gevoeliger, hoe strenger toegang en logging."),
        ],
        "praktijk": "<p>Een auditor vraagt: 'Waar komt het getal 1.243 wachtenden in het bestuursrapport vandaan?' Dankzij lineage "
                    "in Purview toon je in twee minuten de route van bron tot rapport, inclusief welke transformaties en wie "
                    "eigenaar is.</p>",
        "begrippen": [("Metadata", "Data over data: eigenaar, beschrijving, type, gevoeligheid."),
                      ("Lineage", "Herkomst en route van data."), ("Data catalog", "Zoekbare inventaris van datasets."),
                      ("ISMS", "Information Security Management System (ISO 27001)."),
                      ("Classificatie", "Data indelen naar gevoeligheid.")],
        "fouten": ["Governance als papieren beleid zonder technische borging.",
                   "Geen eigenaar per dataset.", "Recht op vergetelheid alleen in de bron uitvoeren, niet in alle lagen en back-ups."],
        "quiz": [("Wat is lineage?", "De herkomst en route van data van bron tot rapport."),
                 ("Noem twee data catalogs.", "Microsoft Purview, Unity Catalog (of AWS Glue Data Catalog)."),
                 ("Wat is ISO 27001?", "Norm voor een risicogebaseerd ISMS met beheersmaatregelen (Annex A)."),
                 ("Hoeveel maatregelen telt Annex A (2022)?", "93.")],
    },
    # 014 CI/CD
    {
        "visuals": [
            ("cycle", {"steps": ["Plan", "Code", "Test", "Deploy", "Monitor"]},
             "De DataOps-cyclus: monitoring voedt de volgende planning."),
            ("cols", {"cols": [("Feature branch", ["Ontwikkelen", "Lokaal testen"]), ("Pull request", ["Review", "CI-tests"]),
                               ("main", ["Deploy test", "Deploy prod"])], "labels": ["PR", "merge"]},
             "Van branch naar productie."),
        ],
        "praktijk": "<p>Een collega past een dbt-model aan en opent een pull request. CI bouwt alleen de gewijzigde modellen en hun "
                    "afnemers (slim CI), draait alle tests en ziet dat een <code>not_null</code>-test faalt. De fout komt nooit in "
                    "productie.</p>",
        "begrippen": [("CI", "Continuous Integration: automatisch bouwen en testen bij elke wijziging."),
                      ("CD", "Continuous Delivery/Deployment: automatisch uitrollen."),
                      ("Pull request", "Verzoek om code samen te voegen, met review."),
                      ("OTAP", "Ontwikkel, Test, Acceptatie, Productie."),
                      ("Rollback", "Terug naar de vorige werkende versie.")],
        "code": ("YAML", """# .github/workflows/dbt-ci.yml
on: pull_request
jobs:
  dbt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install dbt-databricks
      - run: dbt deps
      - run: dbt build --select state:modified+ --defer --state ./prod-artifacts
        env:
          DBT_TOKEN: ${{ secrets.DBT_TOKEN }}"""),
        "fouten": ["Direct in productie wijzigen ('even snel').", "CI zonder echte tests.",
                   "Geen rollback-plan bij een deploy."],
        "quiz": [("Wat is CI?", "Automatisch bouwen en testen bij elke wijziging."),
                 ("Wat betekent OTAP?", "Ontwikkel, Test, Acceptatie, Productie."),
                 ("Wat is slim CI in dbt?", "Alleen gewijzigde modellen en hun afnemers bouwen en testen.")],
    },
]
