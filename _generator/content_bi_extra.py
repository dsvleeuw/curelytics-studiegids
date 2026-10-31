"""Uitbreiding per fiche (zelfde volgorde als FICHES in content_bi.py)."""

EXTRA = [
    # 001 Wat is BI
    {
        "visuals": [
            ("pyramid", {"levels": ["Wijsheid", "Kennis", "Informatie", "Data"],
                         "notes": ["Wat moeten we doen?", "Waarom gebeurt het?", "Wat is er gebeurd?", "Ruwe feiten"]},
             "De DIKW-piramide: BI tilt data omhoog naar informatie en kennis."),
            ("flow", {"steps": ["Beschrijvend\nwat?", "Diagnostisch\nwaarom?", "Voorspellend\nwat komt?", "Voorschrijvend\nwat doen?"],
                      "highlight": [0, 1]},
             "Vier niveaus van analyse; klassieke BI zit vooral links."),
        ],
        "praktijk": "<p>Een ziekenhuis ziet in het OK-dashboard dat de bezettingsgraad op dinsdag structureel laag is. Inzicht: "
                    "één specialisme plant te weinig. Actie: planning aangepast, 6% meer operaties per week. Dát is BI: van "
                    "getal naar besluit.</p>",
        "begrippen": [("KPI", "Key Performance Indicator: meetbare indicator voor een doel."),
                      ("Dashboard", "Overzicht van KPI's op één scherm."),
                      ("Self-service BI", "Gebruikers maken zelf analyses op een betrouwbaar model."),
                      ("Single source of truth", "Eén afgesproken bron/definitie per cijfer.")],
        "fouten": ["Dashboards bouwen die niemand gebruikt omdat de vraag nooit is opgehaald.",
                   "Elke afdeling eigen KPI-definities laten hanteren.",
                   "Te veel KPI's tegelijk – niemand ziet meer wat belangrijk is."],
        "quiz": [("Wat is het verschil tussen data en informatie?", "Informatie is data met context en structuur, zodat het betekenis heeft."),
                 ("Noem de vier soorten analyse.", "Beschrijvend, diagnostisch, voorspellend, voorschrijvend."),
                 ("Wat is self-service BI?", "Gebruikers maken zelf rapporten op een gecertificeerd datamodel.")],
    },
    # 002 DWH, ETL, ELT
    {
        "visuals": [
            ("stack", {"layers": ["Datamarts / presentatie", "Integratielaag (DV of 3NF)", "Staging", "Bronsystemen"],
                       "notes": ["Ster-schema's per onderwerp", "Historie, alle bronnen samen", "1-op-1 kopie, tijdelijk",
                                 "ERP, CRM, EPD, zaaksysteem"]},
             "Klassieke DWH-lagen van bron (onder) naar gebruiker (boven)."),
            ("compare", {"left": ("OLTP (bron)", ["Veel kleine transacties", "Genormaliseerd", "Huidige stand"]),
                         "right": ("OLAP (DWH)", ["Grote analyses", "Gedenormaliseerd (ster)", "Historie"])},
             "Waarom je niet rechtstreeks op het bronsysteem rapporteert."),
        ],
        "praktijk": "<p>Een woningcorporatie laadde elke nacht alle 2 miljoen huurtransacties opnieuw (4 uur). Overstap naar "
                    "incrementeel laden met een watermark op <code>gewijzigd_op</code>: nog maar 15 minuten, en de bron wordt "
                    "minder belast.</p>",
        "begrippen": [("Staging", "Tijdelijke landingsplek voor ruwe brondata."),
                      ("CDC", "Change Data Capture: alleen wijzigingen uit de bron ophalen."),
                      ("Watermark", "Laatst geladen tijdstip/ID, startpunt voor de volgende run."),
                      ("Full load", "Alles opnieuw laden."), ("Incremental load", "Alleen nieuw/gewijzigd laden.")],
        "code": ("SQL", """-- Incrementeel laden met een watermark
DECLARE @laatst DATETIME2 = (SELECT max_gewijzigd FROM etl.watermark WHERE tabel = 'contract');

INSERT INTO stg.contract
SELECT * FROM bron.contract
WHERE  gewijzigd_op > @laatst;

UPDATE etl.watermark
SET    max_gewijzigd = (SELECT MAX(gewijzigd_op) FROM stg.contract)
WHERE  tabel = 'contract';"""),
        "fouten": ["Rapporteren direct op het productiesysteem → traag en belastend.",
                   "Geen historie bewaren: 'hoe was het vorig jaar?' kan dan niet meer.",
                   "Verwijderde records in de bron vergeten bij incrementeel laden."],
        "quiz": [("Wat is het verschil tussen ETL en ELT?", "ETL transformeert vóór het laden, ELT laadt eerst ruw en transformeert in het DWH/lake."),
                 ("Wat is CDC?", "Change Data Capture: alleen de wijzigingen uit de bron verwerken."),
                 ("Waarom niet op OLTP rapporteren?", "Het is gemaakt voor transacties, niet voor analyses; het wordt traag en heeft geen historie.")],
    },
    # 003 Kimball
    {
        "visuals": [
            ("compare", {"left": ("Feitentabel", ["Getallen (bedrag, aantal)", "Foreign keys", "Veel rijen, smal"]),
                         "right": ("Dimensietabel", ["Beschrijvingen", "Surrogate key", "Weinig rijen, breed"])},
             "Feit vs dimensie in één oogopslag."),
            ("flow", {"steps": ["Kies het\nproces", "Bepaal de\ngrain", "Kies de\ndimensies", "Kies de\nfeiten"], "highlight": [1]},
             "Kimball's vier stappen voor dimensioneel ontwerp."),
        ],
        "praktijk": "<p>Bij een thuiszorgorganisatie: proces = geleverde zorgmomenten. Grain = één rij per bezoek. Dimensies: "
                    "cliënt (gepseudonimiseerd), medewerker, datum, tijdvak, zorgsoort, regio. Feiten: geplande minuten, "
                    "geleverde minuten, reistijd. Nu kan het management zien waar geplande en geleverde zorg uit elkaar lopen.</p>",
        "begrippen": [("Grain", "Wat één rij in de feitentabel voorstelt."),
                      ("Surrogate key", "Betekenisloze sleutel (1, 2, 3…) gemaakt in het DWH."),
                      ("Business key", "Sleutel uit de bron, bv. klantnummer."),
                      ("Conformed dimension", "Dimensie die door meerdere feitentabellen gedeeld wordt."),
                      ("Bus matrix", "Tabel: processen × gedeelde dimensies.")],
        "tabel": {"kop": ["Type feit", "Voorbeeld", "Rijen"],
                  "rijen": [["Transactie", "Elke verkoop", "Eén per gebeurtenis"],
                            ["Periodieke snapshot", "Voorraad per dag", "Eén per periode per item"],
                            ["Accumulerende snapshot", "Aanvraag: ingediend → besluit", "Eén per proces, wordt bijgewerkt"]]},
        "fouten": ["De grain niet expliciet vastleggen → dubbeltellingen.",
                   "Tekstvelden in de feitentabel zetten in plaats van in een dimensie.",
                   "Elke afdeling een eigen 'klant'-dimensie geven (niet conformed)."],
        "quiz": [("Wat is de grain?", "Wat één rij in de feitentabel betekent."),
                 ("Waarom surrogate keys?", "Onafhankelijk van de bron en nodig voor historie (SCD2)."),
                 ("Wat is een conformed dimension?", "Een dimensie die door meerdere feitentabellen hergebruikt wordt."),
                 ("Ster- vs sneeuwvlokschema?", "Ster: dimensies plat; sneeuwvlok: dimensies genormaliseerd – ster is beter voor Power BI.")],
    },
    # 004 SCD
    {
        "visuals": [
            ("timeline", {"points": [("Haarlem", "2019 – 2023"), ("Leiden", "2023 – 2025"), ("Utrecht", "2025 – nu")]},
             "SCD2: dezelfde klant krijgt per woonplaats een eigen rij met geldigheidsperiode."),
        ],
        "praktijk": "<p>Een medewerker gaat in juni van team Noord naar team Zuid. Met SCD1 zouden alle uren van januari tot juni "
                    "plotseling bij Zuid staan – de verzuimcijfers van Noord kloppen dan niet meer. Met SCD2 blijven die uren bij "
                    "Noord en tellen de nieuwe uren bij Zuid.</p>",
        "begrippen": [("SCD", "Slowly Changing Dimension – hoe je omgaat met wijzigende kenmerken."),
                      ("Geldig_van / geldig_tot", "Periode waarin een dimensierij geldig is."),
                      ("is_actueel", "Vlag voor de huidige versie van een rij."),
                      ("Late-arriving fact", "Een feit dat binnenkomt na een dimensiewijziging.")],
        "tabel": {"kop": ["klant_sk", "klant_nr", "woonplaats", "geldig_van", "geldig_tot", "actueel"],
                  "rijen": [["101", "K-77", "Haarlem", "2019-01-01", "2023-03-31", "nee"],
                            ["245", "K-77", "Leiden", "2023-04-01", "2025-06-30", "nee"],
                            ["388", "K-77", "Utrecht", "2025-07-01", "9999-12-31", "ja"]]},
        "code": ("SQL", """-- SCD2 in twee stappen
-- 1) huidige rij afsluiten als er iets veranderd is
UPDATE d SET geldig_tot = CAST(GETDATE() AS DATE) - 1, is_actueel = 0
FROM   dim_klant d JOIN stg_klant s ON s.klant_nr = d.klant_nr
WHERE  d.is_actueel = 1 AND d.woonplaats <> s.woonplaats;

-- 2) nieuwe versie invoegen
INSERT INTO dim_klant (klant_nr, woonplaats, geldig_van, geldig_tot, is_actueel)
SELECT s.klant_nr, s.woonplaats, CAST(GETDATE() AS DATE), '9999-12-31', 1
FROM   stg_klant s
LEFT JOIN dim_klant d ON d.klant_nr = s.klant_nr AND d.is_actueel = 1
WHERE  d.klant_nr IS NULL;"""),
        "fouten": ["Joinen op de business key in plaats van de surrogate key → dubbele rijen.",
                   "Overal SCD2 toepassen, ook op typfoutcorrecties.",
                   "Geen 'einddatum ver in de toekomst' gebruiken, waardoor BETWEEN-joins mislukken."],
        "quiz": [("Wat doet SCD type 1?", "Oude waarde overschrijven, geen historie."),
                 ("Wat doet SCD type 2?", "Nieuwe rij per wijziging met geldigheidsperiode."),
                 ("Waarom heb je bij SCD2 een surrogate key nodig?", "Omdat dezelfde business key meerdere rijen heeft.")],
    },
    # 005 Data Vault
    {
        "visuals": [
            ("hub", {"center": "Link\nKlant–Order", "center_shape": "rect",
                     "spokes": ["Hub Klant", "Sat Klant\n(adres)", "Hub Order", "Sat Order\n(status)"]},
             "Mini Data Vault: twee hubs verbonden door een link, elk met een satellite."),
            ("stack", {"layers": ["Information marts (Kimball)", "Business Vault (regels)", "Raw Vault (as-is)", "Staging"],
                       "notes": ["Voor Power BI", "Afgeleide berekeningen", "Hubs, links, satellites", "Ruwe bron"]},
             "Data Vault-architectuur: rapporteren gebeurt altijd via marts erbovenop."),
        ],
        "praktijk": "<p>Een provincie krijgt elk jaar nieuwe bronnen (subsidiesysteem, GIS, HR). In Data Vault voeg je per bron "
                    "satellites toe aan bestaande hubs – het bestaande model hoeft niet om. En bij een audit kun je per veld "
                    "aantonen uit welke bron en op welk moment het geladen is.</p>",
        "begrippen": [("Hash key", "Sleutel berekend als hash van de business key – maakt parallel laden mogelijk."),
                      ("Load date", "Moment waarop een record geladen is."),
                      ("Record source", "Uit welk systeem het record komt."),
                      ("PIT-tabel", "Point-in-time hulptabel om satellites snel te combineren."),
                      ("Bridge", "Hulptabel om links over meerdere hubs te versnellen.")],
        "tabel": {"kop": ["", "Kimball", "Data Vault"],
                  "rijen": [["Doel", "Rapportage, snel en begrijpelijk", "Integratie, flexibel en auditeerbaar"],
                            ["Nieuwe bron", "Model aanpassen", "Satellites toevoegen"],
                            ["Queries", "Eenvoudig", "Complex (veel joins)"],
                            ["Historie", "Via SCD", "Standaard in satellites"]]},
        "fouten": ["Power BI direct op de Raw Vault zetten – veel te complex en traag.",
                   "Business keys verkeerd kiezen (bv. een technisch ID dat per bron verschilt).",
                   "Data Vault inzetten voor een klein project met één stabiele bron."],
        "quiz": [("Wat staat er in een hub?", "Unieke business keys (+ hash key, load date, record source)."),
                 ("Wat staat er in een satellite?", "Beschrijvende attributen met volledige historie."),
                 ("Wat is een link?", "Een relatie tussen twee of meer hubs."),
                 ("Wat zet je bovenop de vault voor rapportage?", "Information marts in Kimball-stervorm.")],
    },
    # 006 Power BI-architectuur
    {
        "visuals": [
            ("compare", {"left": ("Import", ["Data in geheugen (VertiPaq)", "Zeer snel", "Refresh nodig"]),
                         "right": ("DirectQuery", ["Live query naar bron", "Altijd actueel", "Trager, bron belast"])},
             "De belangrijkste opslagkeuze in Power BI. (Fabric voegt Direct Lake toe: snel én actueel.)"),
            ("tree", {"root": "Workspace", "children": [("Semantisch model", ["Tabellen & relaties", "Measures", "RLS-rollen"]),
                                                         ("Rapporten", ["Pagina's", "Visuals"]),
                                                         ("App", ["Voor eindgebruikers", "Audiences"])]},
             "Hoe content in de Power BI Service is georganiseerd."),
        ],
        "praktijk": "<p>Een gemeente wil dat elk wijkteam alleen eigen cijfers ziet. Oplossing: één semantisch model met een "
                    "RLS-rol <code>[Wijk] = USERPRINCIPALNAME()</code>-mapping via een autorisatietabel. Eén rapport, tien "
                    "wijkteams, ieder ziet alleen zijn eigen data.</p>",
        "begrippen": [("Power Query (M)", "Taal/tool om data op te halen en te transformeren."),
                      ("VertiPaq", "In-memory kolomengine achter Import-modus."),
                      ("Gateway", "Brug tussen Power BI Service en on-premise bronnen."),
                      ("RLS", "Row-Level Security: rijen filteren per gebruiker/rol."),
                      ("Incremental refresh", "Alleen recente partities verversen.")],
        "code": ("DAX", """-- RLS-rol 'Wijkteam' op de tabel Autorisatie
[E-mail] = USERPRINCIPALNAME()

-- Autorisatie (E-mail, Wijk) heeft een relatie met dim_Wijk,
-- zodat het filter doorloopt naar alle feiten."""),
        "fouten": ["Bidirectionele relaties overal aanzetten → ambigue modellen en trage queries.",
                   "Elk rapport een eigen kopie van het model geven (geen single source of truth).",
                   "Hele tabellen met tientallen ongebruikte kolommen importeren."],
        "quiz": [("Import vs DirectQuery?", "Import = data in geheugen, snel; DirectQuery = live naar bron, actueel maar trager."),
                 ("Waarvoor dient een gateway?", "Om vanuit de Service on-premise bronnen te verversen."),
                 ("Wat is RLS?", "Row-Level Security: per rol/gebruiker alleen bepaalde rijen tonen."),
                 ("Welke certificering hoort bij Power BI?", "PL-300 (Power BI Data Analyst).")],
    },
    # 007 DAX
    {
        "visuals": [
            ("compare", {"left": ("Measure", ["Berekend bij tonen", "Reageert op filters", "Geen opslag"]),
                         "right": ("Calculated column", ["Berekend bij refresh", "Per rij vast", "Kost geheugen"])},
             "Vuistregel: aggregaties zijn measures; kolommen alleen als je erop wilt filteren/groeperen."),
            ("flow", {"steps": ["Bestaande\nfiltercontext", "CALCULATE\nwijzigt filters", "Expressie\nevalueren", "Resultaat"],
                      "highlight": [1]},
             "Wat CALCULATE doet: filters toevoegen, vervangen of verwijderen vóór de berekening."),
        ],
        "praktijk": "<p>Een controller wil '% van totaal' per afdeling. Met <code>DIVIDE([Kosten], CALCULATE([Kosten], "
                    "REMOVEFILTERS(Afdeling)))</code> blijft het totaal in de noemer gelijk, ongeacht welke afdeling in de rij "
                    "staat – maar andere filters (zoals het jaar) blijven wel werken.</p>",
        "begrippen": [("Filtercontext", "Alle filters die op een cel van toepassing zijn."),
                      ("Rijcontext", "De 'huidige rij' tijdens een iteratie (SUMX, kolommen)."),
                      ("Context transition", "CALCULATE zet rijcontext om in filtercontext."),
                      ("Iterator", "Functie die rij voor rij rekent (SUMX, AVERAGEX)."),
                      ("Time intelligence", "Functies voor YTD, vorig jaar, etc.")],
        "code": ("DAX", """Totaal Omzet = SUM ( Verkoop[Bedrag] )

Omzet VJ =
CALCULATE ( [Totaal Omzet], SAMEPERIODLASTYEAR ( 'Datum'[Datum] ) )

Groei % =
VAR Nu = [Totaal Omzet]
VAR Vj = [Omzet VJ]
RETURN DIVIDE ( Nu - Vj, Vj )

% van totaal =
DIVIDE ( [Totaal Omzet], CALCULATE ( [Totaal Omzet], REMOVEFILTERS ( Product ) ) )"""),
        "fouten": ["Calculated columns gebruiken voor sommen die een measure hadden moeten zijn.",
                   "Delen met / in plaats van DIVIDE → fouten bij delen door nul.",
                   "Time intelligence zonder aaneengesloten, gemarkeerde datumtabel."],
        "quiz": [("Measure of calculated column voor 'totale omzet'?", "Measure."),
                 ("Wat doet CALCULATE?", "Een expressie evalueren in een aangepaste filtercontext."),
                 ("Waarom DIVIDE?", "Veilig delen: geen fout bij delen door nul."),
                 ("Wat is het verschil tussen SUM en SUMX?", "SUM telt een kolom op; SUMX rekent per rij een expressie en telt die op.")],
    },
    # 008 SQL
    {
        "visuals": [
            ("venn", {"sets": ["Tabel A", "Tabel B"], "center": "INNER\nJOIN"},
             "INNER JOIN = de overlap. LEFT JOIN = heel A plus de overlap."),
            ("cols", {"cols": [("ROW_NUMBER", ["1, 2, 3, 4", "Altijd uniek"]), ("RANK", ["1, 2, 2, 4", "Gaten na gelijk"]),
                               ("DENSE_RANK", ["1, 2, 2, 3", "Geen gaten"])], "arrows": False},
             "Drie ranking-window functions – populaire interviewvraag."),
        ],
        "praktijk": "<p>Een bron levert dubbele klantrecords (dezelfde klant, meerdere updates). Met "
                    "<code>ROW_NUMBER() OVER (PARTITION BY klant_nr ORDER BY gewijzigd_op DESC)</code> houd je per klant "
                    "alleen de nieuwste rij over – een standaardpatroon in elke staging-laag.</p>",
        "begrippen": [("JOIN", "Tabellen combineren op een sleutel."),
                      ("Aggregatie", "Samenvatten: SUM, COUNT, AVG…"),
                      ("Window function", "Berekening over een groep rijen zonder ze samen te voegen."),
                      ("CTE", "Common Table Expression: tijdelijke benoemde subquery (WITH)."),
                      ("Index", "Structuur die zoeken versnelt.")],
        "code": ("SQL", """WITH geordend AS (
    SELECT o.*,
           ROW_NUMBER() OVER (PARTITION BY klant_id ORDER BY orderdatum DESC) AS rn,
           SUM(bedrag)  OVER (PARTITION BY klant_id ORDER BY orderdatum
                              ROWS UNBOUNDED PRECEDING)                  AS lopend_totaal
    FROM   orders o
)
SELECT klant_id, orderdatum, bedrag, lopend_totaal
FROM   geordend
WHERE  rn = 1;          -- meest recente order per klant"""),
        "fouten": ["<code>WHERE kolom = NULL</code> schrijven (moet IS NULL zijn).",
                   "Een LEFT JOIN ongemerkt een INNER JOIN maken door in de WHERE op de rechtertabel te filteren.",
                   "Joinen op niet-unieke sleutels → rijen vermenigvuldigen."],
        "quiz": [("Verschil WHERE en HAVING?", "WHERE filtert rijen vóór groeperen, HAVING filtert groepen erna."),
                 ("Verschil RANK en DENSE_RANK?", "RANK laat gaten na gelijke waarden, DENSE_RANK niet."),
                 ("Hoe ontdubbel je records?", "ROW_NUMBER() OVER (PARTITION BY sleutel ORDER BY datum DESC) en rn = 1 houden."),
                 ("Wat is de logische uitvoervolgorde?", "FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.")],
    },
    # 009 Cloud DWH
    {
        "visuals": [
            ("tree", {"root": "Microsoft Fabric", "children": [("OneLake", ["Eén data lake", "Delta-formaat"]),
                                                                ("Engines", ["Lakehouse (Spark)", "Warehouse (SQL)"]),
                                                                ("Power BI", ["Direct Lake", "Semantische modellen"])]},
             "Fabric in één plaatje: alle engines op één lake."),
        ],
        "praktijk": "<p>Een onderwijsinstelling met Microsoft 365 en Power BI Pro twijfelt tussen Snowflake en Fabric. Na een "
                    "proof-of-concept van twee weken kiest ze Fabric: alles in één licentie, Direct Lake maakt rapporten snel "
                    "zonder imports, en het team kent de Microsoft-tools al.</p>",
        "begrippen": [("MPP", "Massively Parallel Processing: query verdeeld over veel nodes."),
                      ("Virtual warehouse", "Snowflake-compute-cluster dat je los aan/uit zet."),
                      ("OneLake", "Het centrale data lake van Microsoft Fabric."),
                      ("Direct Lake", "Power BI leest Delta-bestanden direct, zonder import."),
                      ("Zero-copy clone", "Snowflake: kopie van een tabel zonder data te dupliceren.")],
        "tabel": {"kop": ["Platform", "Sterk in", "Let op"],
                  "rijen": [["Azure Synapse", "Bestaande Azure-omgevingen", "Microsoft verschuift focus naar Fabric"],
                            ["Microsoft Fabric", "Alles-in-één + Power BI", "Jong product, capaciteitslicenties"],
                            ["Snowflake", "Eenvoud, multi-cloud, data sharing", "Aparte licentie, kosten bewaken"],
                            ["AWS Redshift", "AWS-ecosysteem", "Scheiding opslag/compute via RA3/Serverless"],
                            ["Databricks SQL", "Lakehouse + ML", "Meer engineering-gericht"]]},
        "fouten": ["Een warehouse kiezen op basis van hype in plaats van ecosysteem en skills.",
                   "Compute niet laten auto-pauzeren → onverwachte rekeningen.",
                   "Vergeten dat migreren tussen platformen tijd en geld kost (lock-in)."],
        "quiz": [("Wat is het kernidee van cloud-DWH's?", "Opslag en compute gescheiden, onafhankelijk schalen."),
                 ("Wat is OneLake?", "Het centrale data lake van Microsoft Fabric."),
                 ("Wat is Direct Lake?", "Power BI-modus die Delta-bestanden direct leest: snel én actueel."),
                 ("Wanneer Snowflake?", "Multi-cloud, veel data sharing, of geen Microsoft-ecosysteem.")],
    },
    # 010 Dashboard design
    {
        "visuals": [
            ("grid", {"quadrants": ["Belangrijkste\nKPI", "Trend /\nvergelijking", "Verdeling\n(staaf)", "Detailtabel\n(drill)"],
                      "x_axis": "leesrichting →", "y_axis": "belang ↑", "highlight": 0},
             "Z-patroon: mensen lezen linksboven eerst – zet daar het belangrijkste getal."),
            ("cols", {"cols": [("Trend", ["Lijndiagram"]), ("Vergelijken", ["Staafdiagram"]), ("Deel v. geheel", ["Gestapelde staaf"]),
                               ("Eén getal", ["KPI-kaart"])], "arrows": False},
             "Welke grafiek bij welke vraag."),
        ],
        "praktijk": "<p>Voor een zorgbestuurder: bovenaan drie KPI-kaarten (bezetting, wachtlijst, verzuim) met kleur ten opzichte "
                    "van target. Daaronder per KPI een trendlijn over 13 maanden. Pas na doorklikken de tabel per afdeling. De "
                    "bestuurder heeft in 5 seconden het antwoord op 'staan we ervoor zoals afgesproken?'</p>",
        "begrippen": [("SMART", "Specifiek, Meetbaar, Acceptabel, Realistisch, Tijdgebonden."),
                      ("Leading indicator", "Voorspelt toekomstig resultaat (bv. aantal aanmeldingen)."),
                      ("Lagging indicator", "Meet achteraf (bv. omzet)."),
                      ("Drill-through", "Doorklikken naar een detailpagina met hetzelfde filter."),
                      ("WCAG", "Richtlijnen voor digitale toegankelijkheid.")],
        "fouten": ["Taartdiagrammen met veel stukjes.", "Getallen zonder context (target, vorig jaar).",
                   "Rood/groen als enige onderscheid → onleesbaar voor kleurenblinden."],
        "quiz": [("Waar plaats je de belangrijkste KPI?", "Linksboven."),
                 ("Welke grafiek voor een trend?", "Een lijndiagram."),
                 ("Leading vs lagging?", "Leading voorspelt, lagging meet achteraf."),
                 ("Wat betekent de 5-3-1-regel?", "Antwoord binnen 5 seconden, max 3 kernvragen, 1 doelgroep.")],
    },
    # 011 Impact- en gap-analyse
    {
        "visuals": [
            ("flow", {"steps": ["Bronkolom\nwijzigt", "Pipeline\nstg_klant", "Model\ndim_klant", "3 rapporten\n12 gebruikers"],
                      "highlight": [3]},
             "Impactanalyse via lineage: één wijziging, veel afnemers."),
            ("grid", {"quadrants": ["Vermijden", "Grote projecten\n(plannen)", "Opvullers", "Quick wins\n(eerst doen!)"],
                      "x_axis": "waarde →", "y_axis": "moeite ↑", "highlight": 3},
             "Gaps prioriteren op waarde en moeite: quick wins (veel waarde, weinig moeite) zitten rechtsonder."),
        ],
        "praktijk": "<p>Bij de overstap naar een nieuw HR-systeem maakt de BI-specialist een mappingtabel van 140 velden. 12 velden "
                    "hebben geen equivalent: dat zijn de gaps. Drie ervan raken de verzuim-KPI – die krijgen prioriteit en worden "
                    "met de business opgelost vóór de livegang.</p>",
        "begrippen": [("IST / SOLL", "Huidige / gewenste situatie."), ("Lineage", "De herkomst en route van data."),
                      ("Mapping", "Koppeling van oude naar nieuwe velden."),
                      ("Reconciliatie", "Cijfers van oud en nieuw vergelijken tot ze kloppen.")],
        "tabel": {"kop": ["Onderwerp", "Huidig", "Gewenst", "Gap", "Actie"],
                  "rijen": [["Verzuim-KPI", "Maandelijks in Excel", "Dagelijks in Power BI", "Geen pipeline", "ADF + model bouwen"],
                            ["Definitie", "Per afdeling anders", "Eén definitie", "Geen afspraak", "KPI-sessie met HR"],
                            ["Toegang", "Iedereen alles", "Per afdeling", "Geen RLS", "RLS-rollen inrichten"]]},
        "fouten": ["Alleen naar techniek kijken en organisatorische gaps vergeten.",
                   "Afnemers niet informeren vóór een wijziging.",
                   "Geen reconciliatie doen na een migratie."],
        "quiz": [("Wat is een gap-analyse?", "Vergelijking huidig vs gewenst, met acties om het verschil te dichten."),
                 ("Wat is een impactanalyse?", "Bepalen wat een wijziging raakt: data, rapporten, processen, mensen."),
                 ("Welke tool helpt bij impactanalyse?", "Data lineage (bv. Purview, dbt docs).")],
    },
    # 012 Senior BI
    {
        "visuals": [
            ("flow", {"steps": ["Ad-hoc\n(Excel)", "Gestandaar-\ndiseerd", "Centraal\nmodel", "Self-\nservice", "Voorspellend"],
                      "highlight": [2]},
             "BI-volwassenheid: waar staat de klant, wat is de volgende stap?"),
            ("timeline", {"points": [("Inventariseren", "rapporten & bronnen"), ("Rationaliseren", "wat kan weg?"),
                                     ("Bouwen", "per domein"), ("Reconciliëren", "cijfers vergelijken"), ("Uitfaseren", "oud uit")]},
             "Aanpak van een BI-migratie (bv. SSRS/SSAS → Power BI/Fabric)."),
        ],
        "praktijk": "<p>Een organisatie heeft 600 SSRS-rapporten. Na inventarisatie blijkt 40% al een jaar niet geopend. Die worden "
                    "niet gemigreerd. De rest wordt per domein omgezet naar Power BI op gedeelde, gecertificeerde modellen. Een "
                    "medior consultant bouwt; de senior reviewt, bewaakt de standaarden en rapporteert aan de stuurgroep.</p>",
        "begrippen": [("CoE", "Center of Excellence: team dat BI-standaarden en kennis bewaakt."),
                      ("Maturity model", "Model om volwassenheid in stappen te beschrijven."),
                      ("Rationaliseren", "Opruimen: alleen migreren wat waarde heeft."),
                      ("Stuurgroep", "Overleg waar opdrachtgevers besluiten nemen over het project.")],
        "fouten": ["Alles 1-op-1 migreren, inclusief rapporten die niemand gebruikt.",
                   "Als senior zelf al het bouwwerk doen in plaats van het team te laten groeien.",
                   "Standaarden pas achteraf afspreken."],
        "quiz": [("Noem de stappen van een BI-migratie.", "Inventariseren, rationaliseren, bouwen, reconciliëren, uitfaseren."),
                 ("Wat is een CoE?", "Center of Excellence dat standaarden, kennis en governance bewaakt."),
                 ("Wat zijn de vier senior-taken (ADMC)?", "Adviseren, designen, migreren, coachen.")],
    },
]
