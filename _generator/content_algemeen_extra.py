"""Uitbreiding per fiche (zelfde volgorde als FICHES in content_algemeen.py)."""

EXTRA = [
    # 001 CureLytics in één minuut
    {
        "visuals": [
            ("cols", {"cols": [("Fase 1", ["Eén specialist", "Snel resultaat"]),
                               ("Fase 2", ["Team", "Meerdere rollen"]),
                               ("Fase 3", ["Platformbeheer", "Doorlopend optimaliseren"])],
                      "labels": ["groeien", "groeien"]},
             "De gefaseerde aanpak: met de klant meegroeien van één persoon naar volledige verantwoordelijkheid."),
            ("venn", {"sets": ["Publieke\nsector", "Zorg &\nonderwijs", "Bedrijfs-\nleven"], "center": "Data &\nAnalytics"},
             "Drie sectoren, één vak: data omzetten in beslissingen."),
        ],
        "praktijk": "<p>Een gemeente wil sturen op data maar heeft geen eigen data-team. CureLytics detacheert eerst één BI-specialist "
                    "die een verzuimdashboard bouwt. Dat werkt – dus volgt een data engineer voor een centraal platform, en later "
                    "neemt CureLytics het beheer van dat platform over.</p><p>Jij bent in dat verhaal de eerste persoon: de kwaliteit "
                    "van jouw werk bepaalt of er een fase 2 komt.</p>",
        "begrippen": [("Detachering", "Je bent in dienst bij CureLytics en werkt (tijdelijk) bij een klant."),
                      ("QRC Group", "De groep waar CureLytics onderdeel van is."),
                      ("Managed service", "Het beheer van (een deel van) het dataplatform uitbesteden."),
                      ("Digitale transformatie", "Werkprocessen fundamenteel verbeteren met technologie en data.")],
        "tabel": {"kop": ["Feit", "Wat je zegt"],
                  "rijen": [["Wat", "Data &amp; Analytics detachering en diensten"],
                            ["Waar", "Haarlem, hybride"],
                            ["Voor wie", "Publieke sector, zorg, onderwijs, bedrijfsleven"],
                            ["Hoe", "Gefaseerd: specialist → team → platformbeheer"],
                            ["Groei", "€2.000 opleidingsbudget per jaar"]]},
        "fouten": ["Alleen zeggen 'jullie zijn een detacheerder' zonder de data-focus en sectoren te noemen.",
                   "Geen enkele vraag over hun klanten stellen – dat lijkt desinteresse.",
                   "QRC Group verwarren met een klant; het is de groep waar ze bij horen."],
        "quiz": [("Van welke groep is CureLytics onderdeel?", "QRC Group."),
                 ("Wat zijn de drie fasen in hun aanpak?", "Eén specialist → team → volledig platformbeheer."),
                 ("Noem drie sectoren van hun klanten.", "Publieke sector, zorg, onderwijs (en bedrijfsleven)."),
                 ("Hoe hoog is het opleidingsbudget?", "€2.000 per jaar.")],
    },
    # 002 Het sollicitatieproces
    {
        "visuals": [
            ("timeline", {"points": [("Intro", "30 min online"), ("Gesprek + case", "90 min"), ("Cultuur", "en voorwaarden"),
                                     ("Aanbod", "binnen 48 uur")]},
             "Het proces als tijdlijn – snel, dus wees na elke stap klaar voor de volgende."),
            ("pyramid", {"levels": ["Hardop\ndenken", "Structuur", "Vakkennis", "Voorbereiding"],
                         "notes": ["Laat zien hoe je redeneert", "Vraag → aanpak → risico", "De fiches in jouw rolmap",
                                   "Bedrijf, vacature, STAR-verhalen"]},
             "Waar je in de case op scoort: alles rust op voorbereiding."),
        ],
        "praktijk": "<p>In de case krijg je bijvoorbeeld: <em>'Een zorginstelling wil weten waarom de wachttijden oplopen.'</em> "
                    "Een sterke kandidaat stelt eerst vragen (welke wachttijd, voor wie, welke data is er?), tekent dan de "
                    "keten en noemt pas daarna tools. Een zwakke kandidaat begint direct over Power BI.</p>",
        "begrippen": [("Case", "Praktijkopdracht waarin je hardop een aanpak bedenkt."),
                      ("Hardop denken", "Je redenering uitspreken, zodat de interviewer kan meekijken."),
                      ("Cultuurgesprek", "Gesprek over hoe je samenwerkt, wat je drijft en of je past."),
                      ("Aanbod", "Het voorstel met salaris en voorwaarden.")],
        "fouten": ["In de case meteen een oplossing roepen zonder vragen te stellen.",
                   "Stil worden als je iets niet weet – zeg hoe je het zou uitzoeken.",
                   "Geen eigen vragen hebben aan het einde van het gesprek."],
        "quiz": [("Hoe lang duurt het gesprek met de case?", "90 minuten."),
                 ("Hoe snel doet CureLytics een aanbod?", "Binnen 48 uur."),
                 ("Wat zijn de vijf stappen van je case-structuur?", "Vraag verhelderen → aannames → aanpak → risico's → volgende stap."),
                 ("Wat doe je als je iets niet weet?", "Eerlijk zeggen en uitleggen hoe je het zou uitzoeken.")],
    },
    # 003 Detachering
    {
        "visuals": [
            ("compare", {"left": ("Medewerker (vast in dienst)", ["Eén werkgever, één werkplek", "Diepe kennis van één organisatie",
                                                                   "Langzamer variatie"]),
                         "right": ("Gedetacheerde", ["Werkgever ≠ werkplek", "Veel organisaties zien", "Snel leren, snel aanpassen"])},
             "Detacheren vs gewoon in dienst bij één organisatie."),
            ("bars", {"items": [("Vakkennis", 80), ("Communicatie", 90), ("Snel inwerken", 85), ("Adviseren", 70),
                                ("Commercieel", 45)], "unit": "%"},
             "Indicatie: hoe zwaar telt elke vaardigheid voor een consultant (eigen inschatting)."),
        ],
        "praktijk": "<p>Je zit bij een waterschap. De opdrachtgever wil 'snel even' een extra tabblad, terwijl het sprintdoel iets "
                    "anders is. Als consultant zeg je niet botweg nee, maar: <em>'Kan ik het op de backlog zetten en met de PO "
                    "prioriteren? Dan weet je wanneer het komt.'</em> Zo bescherm je het team én de relatie.</p>",
        "begrippen": [("Opdrachtgever", "De persoon bij de klant voor wie je het werk doet."),
                      ("Inlener", "De organisatie waar je gedetacheerd bent."),
                      ("Trusted advisor", "Adviseur wiens mening de klant echt vertrouwt en vraagt."),
                      ("Scope creep", "Een opdracht die ongemerkt steeds groter wordt.")],
        "fouten": ["Je gedragen als 'uitzendkracht' die alleen doet wat gevraagd wordt.",
                   "Klagen over de klant bij collega's van de klant.",
                   "Vergeten contact te houden met CureLytics zelf."],
        "quiz": [("Wie is je werkgever bij detachering?", "CureLytics – je werkt bij de klant."),
                 ("Wat is scope creep?", "Een opdracht die ongemerkt groter wordt dan afgesproken."),
                 ("Hoe zeg je 'nee' als consultant?", "Met een reden en een alternatief, en leg de afspraak vast.")],
    },
    # 004 Agile & Scrum
    {
        "visuals": [
            ("compare", {"left": ("Waterval", ["Alles vooraf plannen", "Eén grote oplevering", "Wijzigen is duur"]),
                         "right": ("Agile", ["Plannen per sprint", "Elke sprint iets werkends", "Wijzigen is normaal"])},
             "Waterval vs Agile."),
            ("tree", {"root": "Scrum-team", "children": [("Product Owner", ["Wat & waarom", "Backlog prioriteren"]),
                                                          ("Scrum Master", ["Proces & obstakels", "Coacht team"]),
                                                          ("Developers", ["Hoe", "Bouwen & testen"])]},
             "De drie verantwoordelijkheden in een Scrum-team."),
        ],
        "praktijk": "<p>In een BI-team bij een provincie bestaat de sprint uit: twee nieuwe KPI's, een datakwaliteitsfix en een "
                    "spike van één dag om te onderzoeken of een nieuwe bron bruikbaar is. In de review laat het team het "
                    "dashboard live zien aan de gebruikers – die vragen meteen om een extra filter, dat gaat naar de backlog.</p>",
        "begrippen": [("Sprint", "Vaste periode (1–4 weken) waarin het team een increment oplevert."),
                      ("Backlog", "Geprioriteerde lijst met werk."),
                      ("Definition of Done", "Afspraak wanneer iets écht af is (getest, gedocumenteerd)."),
                      ("Spike", "Kort, tijdgebonden onderzoek om onzekerheid weg te nemen."),
                      ("Velocity", "Hoeveel werk een team gemiddeld per sprint afrondt.")],
        "fouten": ["Denken dat Agile 'geen planning en geen documentatie' betekent.",
                   "Sprints vullen met werk dat niet af kan (zoals ongespecificeerd data-onderzoek).",
                   "Review overslaan – dan mis je de feedback van gebruikers."],
        "quiz": [("Welke drie verantwoordelijkheden kent Scrum?", "Product Owner, Scrum Master, Developers."),
                 ("Hoe lang duurt de daily?", "Maximaal 15 minuten."),
                 ("Wat is een spike?", "Kort, tijdgebonden onderzoek om onzekerheid te verkleinen."),
                 ("Wat is SAFe?", "Een raamwerk om Agile op te schalen naar grote organisaties.")],
    },
    # 005 AVG & governance
    {
        "visuals": [
            ("cols", {"cols": [("Anoniem", ["Niet herleidbaar", "Buiten de AVG"]),
                               ("Gepseudonimiseerd", ["Herleidbaar met sleutel", "Wél persoonsdata"]),
                               ("Identificerend", ["Naam, BSN, e-mail", "Volledig AVG"])], "arrows": False},
             "Belangrijk onderscheid: pseudonimiseren verlaagt risico, maar het blijft persoonsdata."),
            ("tree", {"root": "Rollen", "children": [("Data owner", ["Beslist over gebruik", "Eindverantwoordelijk"]),
                                                      ("Data steward", ["Bewaakt kwaliteit", "Definities"]),
                                                      ("FG / privacy officer", ["Toezicht AVG", "Adviseert"])]},
             "Wie doet wat in data governance."),
        ],
        "praktijk": "<p>Een GGD wil een dashboard met vaccinatiegraad per wijk. Oplossing: de data engineer pseudonimiseert in de "
                    "bronslaag, het goud-model bevat alleen aantallen per wijk (met een minimum van bijv. 10 personen per cel "
                    "om herleidbaarheid te voorkomen), en de FG keurt de DPIA goed vóór livegang.</p>",
        "begrippen": [("AVG / GDPR", "Europese privacywet voor persoonsgegevens."),
                      ("Grondslag", "De wettelijke basis om gegevens te mogen verwerken (6 stuks)."),
                      ("DPIA", "Risicoanalyse vooraf bij verwerkingen met hoog privacyrisico."),
                      ("FG", "Functionaris Gegevensbescherming – interne toezichthouder."),
                      ("BIO", "Baseline Informatiebeveiliging Overheid.")],
        "fouten": ["Denken dat pseudonimiseren betekent dat de AVG niet meer geldt.",
                   "Een kopie van productiedata met persoonsgegevens in een testomgeving zetten.",
                   "Kleine aantallen per cel tonen (bv. 2 personen in een wijk) → herleidbaar."],
        "quiz": [("Noem de 6 grondslagen van de AVG.", "Toestemming, overeenkomst, wettelijke plicht, vitaal belang, publieke taak, gerechtvaardigd belang."),
                 ("Is gepseudonimiseerde data nog persoonsdata?", "Ja – alleen anonieme data valt buiten de AVG."),
                 ("Wanneer is een DPIA verplicht?", "Bij hoog risico, bv. grootschalige verwerking van gezondheidsgegevens."),
                 ("Wat doet een data steward?", "Bewaakt datakwaliteit en definities namens de data owner.")],
    },
    # 006 Cloud
    {
        "visuals": [
            ("stack", {"layers": ["SaaS – alles kant-en-klaar", "PaaS – platform beheerd", "IaaS – jij beheert OS"],
                       "notes": ["Power BI, Fabric", "Databricks, ADF, Synapse", "Virtuele machines"]},
             "Hoe hoger, hoe minder je zelf beheert."),
            ("bars", {"items": [("Azure", 85), ("AWS", 45), ("GCP", 20)], "unit": ""},
             "Indicatie (eigen inschatting) van hoe vaak je elke cloud tegenkomt bij Nederlandse publieke klanten."),
        ],
        "praktijk": "<p>Een hogeschool draait nog SQL Server met SSIS op eigen servers. De migratie naar Azure gebeurt in stappen: "
                    "eerst data in een data lake (ADLS) landen met ADF, dan transformaties naar Databricks of Fabric, tot slot "
                    "de Power BI-rapporten omzetten. Oude en nieuwe omgeving draaien een tijd parallel om cijfers te vergelijken.</p>",
        "begrippen": [("Region", "Datacenter-locatie (bv. West Europe = Nederland)."),
                      ("Managed identity", "Identiteit voor een dienst, zonder wachtwoord in code."),
                      ("FinOps", "Cloudkosten actief beheren en optimaliseren."),
                      ("Lift-and-shift", "Bestaande oplossing ongewijzigd naar de cloud verhuizen.")],
        "fouten": ["Clusters 24/7 laten draaien → onnodig hoge kosten.",
                   "Data buiten de EU opslaan zonder dat te checken.",
                   "Wachtwoorden in code of notebooks zetten in plaats van Key Vault."],
        "quiz": [("Wat is het Azure-equivalent van AWS Glue?", "Azure Data Factory."),
                 ("Wat is het GCP-warehouse?", "BigQuery."),
                 ("Wat betekent PaaS?", "Platform as a Service – de leverancier beheert het platform, jij de applicatie/data."),
                 ("Waarom opslag en compute scheiden?", "Zo schaal je ze onafhankelijk en betaal je compute alleen als je rekent.")],
    },
    # 007 Data-stack A–Z
    {
        "visuals": [
            ("cols", {"cols": [("Data Analist", ["Vraag & proces", "Requirements", "Adoptie"]),
                               ("Data Engineer", ["Ingestie", "Pipelines", "Platform"]),
                               ("BI Specialist", ["Datamodel", "DAX/KPI's", "Dashboard"])], "arrows": False},
             "Drie rollen, één keten – met overlap aan de randen."),
            ("hub", {"center": "Data-\nplatform", "spokes": ["Governance", "Security", "Kwaliteit", "Monitoring", "CI/CD", "Kosten"]},
             "Dwarsdoorsnijdende zorgen die over de hele keten gelden."),
        ],
        "praktijk": "<p>Een wethouder vraagt: <em>'Hoeveel jongeren wachten op jeugdzorg?'</em> De analist vertaalt dat naar een "
                    "KPI-definitie, de engineer haalt dagelijks data uit het zaaksysteem en de zorgaanbieders, de BI-specialist "
                    "bouwt het model en dashboard. Als één schakel faalt, klopt het antwoord voor de wethouder niet.</p>",
        "begrippen": [("Bronsysteem", "Applicatie waar data ontstaat (ERP, EPD, zaaksysteem)."),
                      ("Ingestie", "Data ophalen en in het platform laden."),
                      ("Semantisch model", "Bedrijfsvriendelijke laag met relaties en KPI's (bv. Power BI-dataset)."),
                      ("Data mesh", "Domeinen beheren hun eigen data als product, met centrale standaarden.")],
        "fouten": ["Beginnen bij de tool in plaats van bij de vraag.",
                   "Datakwaliteit pas aan het eind controleren.",
                   "Geen eigenaar per dataset afspreken."],
        "quiz": [("Noem de 5 stappen van bron tot presentatie.", "Bron, ingestie, opslag, transformatie, presentatie."),
                 ("Welke rol begint bij de vraag?", "De data/business analist."),
                 ("Wat is 'garbage in, garbage out'?", "Slechte brondata geeft altijd slechte uitkomsten, hoe mooi het dashboard ook is.")],
    },
    # 008 STAR
    {
        "visuals": [
            ("bars", {"items": [("Situatie", 15), ("Taak", 10), ("Actie", 50), ("Resultaat", 15), ("Reflectie", 10)], "unit": "%"},
             "Tijdsverdeling van een goed STAR-antwoord: de helft gaat naar je actie."),
            ("cols", {"cols": [("Verhaal 1", ["Probleem opgelost", "Analytisch"]), ("Verhaal 2", ["Samenwerking", "Conflict"]),
                               ("Verhaal 3", ["Iets nieuws geleerd", "Snel inwerken"]), ("Verhaal 4", ["Fout gemaakt", "Herstel"])],
                      "arrows": False},
             "Vier verhalen die samen bijna elke gedragsvraag dekken."),
        ],
        "praktijk": "<p><b>S:</b> Bij mijn vorige baan kregen managers elke maand een Excel van 40 tabbladen. <b>T:</b> Ik moest dat "
                    "overzichtelijker maken. <b>A:</b> Ik interviewde drie managers, bepaalde vijf KPI's, bouwde een Power BI-rapport "
                    "en automatiseerde de refresh. <b>R:</b> Het maandwerk ging van twee dagen naar een uur. <b>R:</b> Ik leerde dat "
                    "de interviews belangrijker waren dan de techniek.</p>",
        "begrippen": [("Gedragsvraag", "Vraag naar wat je in het verleden écht deed."),
                      ("Competentie", "Vaardigheid zoals analytisch denken, samenwerken, klantgerichtheid."),
                      ("Doorvragen", "De interviewer vraagt verder ('wat deed jij precies?').")],
        "fouten": ["'We' zeggen – dan is onduidelijk wat jij deed.",
                   "Een hypothetisch antwoord geven ('ik zou…') op een gedragsvraag.",
                   "Geen resultaat noemen, of alleen 'het ging goed'."],
        "quiz": [("Waar staan de letters STARR voor?", "Situatie, Taak, Actie, Resultaat, Reflectie."),
                 ("Welk deel krijgt de meeste tijd?", "De Actie – wat jij concreet deed."),
                 ("Hoeveel verhalen bereid je voor?", "4–5 die je voor meerdere vragen kunt inzetten.")],
    },
    # 009 Vragen die jij stelt
    {
        "visuals": [
            ("grid", {"quadrants": ["Over salaris\n(stap 3)", "Over klanten\n& opdrachten", "Algemeen\n('leuk bedrijf?')",
                                    "Over groei\n& coaching"], "x_axis": "laat interesse zien →", "y_axis": "timing goed ↑", "highlight": 1},
             "Welke vragen wanneer: rechts scoren altijd, salaris pas in het voorwaardengesprek."),
        ],
        "praktijk": "<p>Na de case vraag je: <em>'Ik merkte dat jullie de nadruk legden op stakeholders. Is dat de grootste "
                    "uitdaging bij jullie publieke klanten?'</em> – een vraag die laat zien dat je luisterde én aan de klant "
                    "denkt.</p>",
        "begrippen": [("Open vraag", "Vraag die niet met ja/nee te beantwoorden is."),
                      ("Inhaken", "Je vraag koppelen aan iets wat eerder gezegd is.")],
        "fouten": ["'Nee, ik heb geen vragen.'", "Vragen naar iets wat letterlijk op de website staat.",
                   "Als eerste vraag beginnen over thuiswerkdagen of vakantie."],
        "quiz": [("Wanneer bespreek je salaris?", "In stap 3 (cultuur & voorwaarden), niet in de intro."),
                 ("Welke drie categorieën vragen heb je?", "Werk, groei, cultuur."),
                 ("Wat vraag je altijd als laatste?", "'Wat is de volgende stap in het proces?'")],
    },
    # 010 Oefencase
    {
        "visuals": [
            ("hub", {"center": "Feit:\nAanvraag", "center_shape": "rect",
                     "spokes": ["Dim Datum\n(ingediend)", "Dim Type\nvergunning", "Dim Behandel-\nteam", "Dim Wijk", "Dim Status"]},
             "Het datamodel van de case: één rij per aanvraag."),
            ("stack", {"layers": ["KPI-kaarten: doorlooptijd · % op tijd · voorraad", "Trend per maand + target 8 weken",
                                  "Tabel: langst openstaande aanvragen"],
                       "notes": ["Hoe staan we ervoor?", "Wordt het beter?", "Waar moet ik ingrijpen?"]},
             "Wireframe van het dashboard: van overzicht naar detail."),
        ],
        "praktijk": "<p><b>Voorbeeldopening:</b> <em>'Voordat ik een oplossing schets wil ik drie dingen weten: wie gaat dit "
                    "dashboard gebruiken, welke beslissing wil die persoon ermee nemen, en uit welk systeem komen de "
                    "aanvragen?'</em></p><p>Daarna teken je de keten en zeg je bij elke stap welke rol het werk doet.</p>",
        "begrippen": [("Doorlooptijd", "Tijd tussen indienen en besluit."),
                      ("Wettelijke termijn", "Termijn waarbinnen de gemeente moet beslissen (vaak 8 weken)."),
                      ("Werkvoorraad", "Aantal openstaande aanvragen op een moment."),
                      ("MVP", "Minimum Viable Product – kleinste versie die al waarde levert.")],
        "code": ("SQL", """-- KPI: % aanvragen binnen termijn, per maand
SELECT d.jaar_maand,
       COUNT(*)                                            AS aantal,
       AVG(f.doorlooptijd_dagen)                           AS gem_doorlooptijd,
       100.0 * SUM(CASE WHEN f.doorlooptijd_dagen <= 56 THEN 1 ELSE 0 END)
             / COUNT(*)                                    AS pct_op_tijd
FROM   feit_aanvraag f
JOIN   dim_datum d ON d.datum_key = f.besluit_datum_key
GROUP  BY d.jaar_maand
ORDER  BY d.jaar_maand;"""),
        "fouten": ["Direct beginnen over Power BI-visuals zonder de vraag te kennen.",
                   "Vergeten dat 'openstaand' geen besluitdatum heeft (NULL) – meet die apart.",
                   "Persoonsgegevens van aanvragers in het model opnemen."],
        "quiz": [("Wat is de grain van de feitentabel in de case?", "Eén rij per aanvraag."),
                 ("Welke drie KPI's kies je?", "Gem. doorlooptijd, % binnen termijn, werkvoorraad."),
                 ("Hoe ga je om met reorganisaties van teams?", "SCD type 2 op de behandelteam-dimensie."),
                 ("Wat is je eerste stap in de case?", "Vragen stellen: gebruiker, beslissing, bron.")],
    },
]
