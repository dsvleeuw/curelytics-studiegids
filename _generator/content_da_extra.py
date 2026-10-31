"""Uitbreiding per fiche (zelfde volgorde als FICHES in content_da.py)."""

EXTRA = [
    # 001 De rol
    {
        "visuals": [
            ("venn", {"sets": ["Business-\nkennis", "Data &\nIT", "Communicatie"], "center": "Analist"},
             "De analist combineert drie werelden."),
            ("timeline", {"points": [("Ophalen", "interviews, workshops"), ("Analyseren", "processen, data"), ("Vastleggen", "requirements"),
                                     ("Begeleiden", "bouw & test"), ("Borgen", "adoptie")]},
             "De analist door een project heen."),
        ],
        "praktijk": "<p>De afdeling Schulddienstverlening wil 'een dashboard'. De analist ontdekt in drie gesprekken dat de "
                    "eigenlijke vraag is: <em>waarom vallen cliënten na 3 maanden uit?</em> Dat vraagt om een andere KPI, een "
                    "andere bron én een procesaanpassing – iets wat met alleen een dashboard nooit was opgelost.</p>",
        "begrippen": [("Elicitatie", "Behoeften en eisen ophalen bij stakeholders."), ("Requirement", "Eis waaraan een oplossing moet voldoen."),
                      ("Stakeholder", "Iedereen met belang bij of invloed op het project."),
                      ("Product Owner", "Bepaalt in Scrum wat er gebouwd wordt en in welke volgorde.")],
        "fouten": ["De gevraagde oplossing bouwen in plaats van het echte probleem te zoeken.",
                   "Alleen met managers praten, niet met de mensen die het werk doen.",
                   "Te technisch communiceren naar de business."],
        "quiz": [("Wat is de kern van de analistenrol?", "Business-vragen vertalen naar eisen voor IT/data, en terug naar advies."),
                 ("Wat is elicitatie?", "Behoeften en eisen ophalen bij stakeholders."),
                 ("Wat doe je als iemand 'een dashboard' vraagt?", "Doorvragen naar het onderliggende probleem en besluit.")],
    },
    # 002 Procesanalyse
    {
        "visuals": [
            ("cols", {"cols": [("Supplier", ["Burger"]), ("Input", ["Aanvraag"]), ("Process", ["Beoordelen"]), ("Output", ["Besluit"]),
                               ("Customer", ["Burger"])]},
             "SIPOC: een proces in één regel – handig als eerste overzicht."),
            ("hub", {"center": "Lange\ndoorlooptijd", "spokes": ["Mensen", "Methode", "Machine\n(systemen)", "Materiaal\n(data)", "Meting", "Milieu"]},
             "Visgraat (Ishikawa) in hub-vorm: zoek oorzaken in zes categorieën."),
        ],
        "praktijk": "<p>Bij de afhandeling van WMO-aanvragen blijkt uit process mining dat 30% van de zaken twee keer langs dezelfde "
                    "beoordelaar gaat, omdat informatie ontbreekt. To-be: een slimmer intakeformulier dat ontbrekende informatie "
                    "vooraf afvangt. Doorlooptijd daalt met 2 weken.</p>",
        "begrippen": [("As-is / to-be", "Huidig / gewenst proces."), ("SIPOC", "Supplier, Input, Process, Output, Customer."),
                      ("Process mining", "Processen reconstrueren uit event logs van systemen."),
                      ("TIMWOODS", "Acht soorten verspilling in Lean."), ("5× waarom", "Vijf keer 'waarom' vragen om tot de kern te komen.")],
        "fouten": ["Het as-is proces tekenen zoals het 'zou moeten', niet zoals het echt gaat.",
                   "Direct naar oplossingen springen zonder oorzaakanalyse.",
                   "Uitvoerenden niet betrekken bij het to-be ontwerp."],
        "quiz": [("Wat is SIPOC?", "Supplier, Input, Process, Output, Customer – procesoverzicht op hoofdlijnen."),
                 ("Wat is process mining?", "Het echte proces reconstrueren uit event logs."),
                 ("Noem een techniek voor oorzaakanalyse.", "5× waarom of het visgraatdiagram.")],
    },
    # 003 BPMN
    {
        "visuals": [
            ("cols", {"cols": [("Events ○", ["Start", "Tussen (timer, bericht)", "Eind"]),
                               ("Activiteiten ▭", ["Taak", "Subproces"]),
                               ("Gateways ◇", ["XOR – één pad", "AND – parallel", "OR – één of meer"])], "arrows": False},
             "De drie kernsymbolen van BPMN."),
            ("stack", {"layers": ["Lane: Aanvrager", "Lane: Klantcontactcentrum", "Lane: Vergunningverlener"],
                       "notes": ["Dient aanvraag in", "Checkt volledigheid", "Beoordeelt en besluit"]},
             "Swimlanes: wie doet welke stap."),
        ],
        "praktijk": "<p>Bij een gemeente toont de BPMN-plaat van de parkeervergunning dat de aanvraag vier keer tussen lanes "
                    "heen en weer gaat. Elke overdracht kost wachttijd. Door de controle bij het KCC te automatiseren verdwijnen "
                    "twee overdrachten.</p>",
        "begrippen": [("Pool", "Organisatie of deelnemer in een proces."), ("Lane", "Rol of afdeling binnen een pool."),
                      ("Sequence flow", "Volgorde binnen een pool (doorgetrokken lijn)."),
                      ("Message flow", "Communicatie tussen pools (gestippelde lijn)."), ("DMN", "Notatie voor beslisregels.")],
        "fouten": ["Gateways zonder alle uitgangen ('nee'-pad vergeten).", "Eén enorme plaat in plaats van subprocessen.",
                   "Sequence flow tussen pools tekenen (moet message flow zijn)."],
        "quiz": [("Wat betekent een ruit in BPMN?", "Een gateway: beslissing of splitsing."),
                 ("XOR vs AND gateway?", "XOR kiest één pad; AND splitst in parallelle paden."),
                 ("Wat is een swimlane?", "Een baan die aangeeft welke rol/afdeling de taken uitvoert."),
                 ("Message flow vs sequence flow?", "Message flow tussen pools (gestippeld), sequence flow binnen een pool.")],
    },
    # 004 Requirements
    {
        "visuals": [
            ("compare", {"left": ("Functioneel", ["Wat moet het doen?", "Filter per afdeling", "Export naar Excel"]),
                         "right": ("Niet-functioneel", ["Hoe goed?", "Laadt binnen 3 sec", "Alleen eigen team zichtbaar"])},
             "Twee soorten requirements."),
            ("flow", {"steps": ["Given\n(situatie)", "When\n(actie)", "Then\n(resultaat)"], "highlight": [2]},
             "Acceptatiecriteria in Given-When-Then."),
        ],
        "praktijk": "<p><b>User story:</b> Als teamleider wil ik het verzuim van mijn team per maand zien, zodat ik tijdig een "
                    "gesprek kan plannen.<br><b>Acceptatie:</b> Given ik ben teamleider van Team Noord, when ik het dashboard "
                    "open, then zie ik alleen medewerkers van Team Noord en het verzuim% van de afgelopen 13 maanden.</p>",
        "begrippen": [("User story", "Als [rol] wil ik [functie] zodat [waarde]."), ("Acceptatiecriteria", "Voorwaarden waaraan een story moet voldoen."),
                      ("MoSCoW", "Must, Should, Could, Won't."), ("INVEST", "Kenmerken van een goede user story."),
                      ("Traceability", "Requirement herleidbaar naar ontwerp en test.")],
        "tabel": {"kop": ["Slecht", "Beter"],
                  "rijen": [["Het dashboard moet snel zijn.", "Elke pagina laadt binnen 3 seconden."],
                            ["Gebruiksvriendelijk.", "Een teamleider vindt zonder training het verzuim van zijn team."],
                            ["Alle data tonen.", "Toont verzuim per team per maand, 13 maanden terug."]]},
        "fouten": ["Vage requirements ('snel', 'gebruiksvriendelijk') die niet testbaar zijn.",
                   "Oplossingen voorschrijven in plaats van behoeften beschrijven.",
                   "Niet-functionele eisen (security, privacy) vergeten."],
        "quiz": [("Formuleer een user story.", "Als [rol] wil ik [functie] zodat [waarde]."),
                 ("Wat betekent MoSCoW?", "Must, Should, Could, Won't (this time)."),
                 ("Geef een niet-functionele eis.", "Bijvoorbeeld: elke pagina laadt binnen 3 seconden."),
                 ("Wat is Given-When-Then?", "Format voor acceptatiecriteria: situatie, actie, verwacht resultaat.")],
    },
    # 005 Use cases
    {
        "visuals": [
            ("hub", {"center": "Systeem:\nVerzuim-\ndashboard", "center_shape": "rect",
                     "spokes": ["Teamleider:\nteam bekijken", "HR:\nalle teams", "Medewerker:\neigen verzuim", "Systeem:\nnachtelijke refresh"]},
             "Use case-overzicht: actoren rond het systeem."),
        ],
        "praktijk": "<p>Voor een AI-traject bij een ziekenhuis worden 12 mogelijke data-use cases verzameld (no-show voorspellen, "
                    "beddenplanning, …). Na scoren op waarde, beschikbaarheid van data en risico kiest de stuurgroep er twee "
                    "voor een pilot.</p>",
        "begrippen": [("Actor", "Persoon of systeem die met het systeem interacteert."),
                      ("Hoofdscenario", "Het 'happy flow'-pad."), ("Alternatief scenario", "Aftakking bij een uitzondering."),
                      ("Pre-/post-conditie", "Wat waar is vóór en na de use case.")],
        "tabel": {"kop": ["Onderdeel", "Voorbeeld"],
                  "rijen": [["Naam", "Teamleider bekijkt verzuim"], ["Actor", "Teamleider"], ["Pre-conditie", "Ingelogd met teamleidersrol"],
                            ["Hoofdscenario", "1. Opent dashboard 2. Kiest maand 3. Klikt op medewerker"],
                            ["Alternatief", "2a. Data niet ververst → melding met datum"], ["Post-conditie", "Teamleider kent verzuimstatus"]]},
        "fouten": ["Alleen de happy flow beschrijven.", "Use cases zo gedetailleerd maken dat het een technisch ontwerp wordt.",
                   "Systeemactoren (geplande jobs) vergeten."],
        "quiz": [("Wat is een actor?", "Persoon of systeem die met het systeem interacteert."),
                 ("Use case vs user story?", "Use case is uitgebreider, met scenario's en uitzonderingen."),
                 ("Hoe prioriteer je data-use cases?", "Op waarde, haalbaarheid (data) en risico.")],
    },
    # 006 Stakeholdermanagement
    {
        "visuals": [
            ("cols", {"cols": [("R", ["Responsible", "Doet het werk"]), ("A", ["Accountable", "Eindverantwoordelijk"]),
                               ("C", ["Consulted", "Wordt gevraagd"]), ("I", ["Informed", "Wordt geïnformeerd"])], "arrows": False},
             "RACI: per taak precies één A."),
            ("flow", {"steps": ["Identificeren", "Analyseren\n(macht/belang)", "Plan per\ngroep", "Betrekken &\ncommuniceren",
                                "Evalueren"], "highlight": [1]},
             "Stappen in stakeholdermanagement."),
        ],
        "praktijk": "<p>De controller van een zorginstelling ziet het nieuwe dashboard als bedreiging voor 'haar' Excel-rapportage. "
                    "De analist vraagt haar mee te beslissen over de KPI-definities. Zij wordt de belangrijkste ambassadeur – en "
                    "haar kennis van de cijfers voorkomt drie fouten.</p>",
        "begrippen": [("Mendelow-matrix", "Macht-belang-matrix om stakeholders in te delen."), ("RACI", "Wie is Responsible, Accountable, Consulted, Informed."),
                      ("Sponsor", "Opdrachtgever die het project steunt en financiert."),
                      ("Weerstand", "Tegenwerking, vaak uit zorg of onzekerheid.")],
        "fouten": ["Stakeholders pas betrekken als het product af is.", "Iedereen hetzelfde informeren, ongeacht macht/belang.",
                   "Weerstand negeren in plaats van begrijpen."],
        "quiz": [("Wat doe je met 'veel macht, veel belang'?", "Nauw betrekken – dat zijn de sleutelspelers."),
                 ("Wat betekent RACI?", "Responsible, Accountable, Consulted, Informed."),
                 ("Hoeveel A's per taak?", "Precies één.")],
    },
    # 007 Business case
    {
        "visuals": [
            ("bars", {"items": [("Jaar 0 (bouw)", 20), ("Jaar 1", 45), ("Jaar 2", 70), ("Jaar 3", 95)], "unit": "%"},
             "Indicatief: cumulatieve baten groeien, terwijl de kosten vooral vooraf zitten."),
            ("compare", {"left": ("Kosten", ["Bouw & inrichting", "Licenties & cloud", "Beheer & training"]),
                         "right": ("Baten", ["Tijd bespaard", "Betere besluiten", "Minder fouten/risico"])},
             "Kosten en baten op een rij."),
        ],
        "praktijk": "<p>Business case managementdashboard: controllers besteden 16 uur per maand aan rapportages × 4 controllers × "
                    "€75 = €57.600 per jaar. Kosten: €40.000 bouw + €8.000 per jaar beheer en licenties. Terugverdientijd: "
                    "minder dan een jaar – en dan zijn betere besluiten nog niet meegerekend.</p>",
        "begrippen": [("ROI", "Return on Investment: (baten − kosten) / kosten."), ("TCO", "Total Cost of Ownership over de hele levensduur."),
                      ("Terugverdientijd", "Hoe lang tot de baten de kosten dekken."), ("NPV / NCW", "Netto contante waarde van toekomstige kasstromen."),
                      ("Nuloptie", "'Niets doen' als vergelijkingsbasis.")],
        "tabel": {"kop": ["Post", "Eenmalig", "Per jaar"],
                  "rijen": [["Bouw dashboard + model", "€40.000", "–"], ["Licenties & cloud", "–", "€5.000"],
                            ["Beheer", "–", "€3.000"], ["Tijdsbesparing controllers", "–", "−€57.600"]]},
        "fouten": ["Alleen harde baten tellen of juist alleen zachte.", "Structurele kosten (beheer, licenties) vergeten.",
                   "Geen nuloptie meenemen."],
        "quiz": [("Wat zijn de onderdelen van een business case?", "Probleem, opties (incl. niets doen), kosten/baten, risico's, advies."),
                 ("Wat is TCO?", "Totale kosten over de hele levensduur."),
                 ("Waarom een nuloptie?", "Als vergelijkingsbasis: wat kost niets doen?")],
    },
    # 008 BI-tools
    {
        "visuals": [
            ("bars", {"items": [("Integratie M365", 90), ("Kosten", 80), ("Visuele verkenning", 65), ("Gebruiksgemak", 75)], "unit": ""},
             "Indicatieve score Power BI (eigen inschatting) – gebruik zo'n score in een toolselectie."),
        ],
        "praktijk": "<p>Een toolselectie bij een hogeschool: criteria gewogen (integratie 30%, kosten 25%, gebruiksgemak 25%, "
                    "governance 20%). Power BI en Tableau scoren beide voldoende; door bestaande Microsoft-licenties wint Power BI. "
                    "Een proof-of-concept met echte docenten bevestigt de keuze.</p>",
        "begrippen": [("Semantisch model", "Laag met relaties en KPI's waarop rapporten draaien."), ("Embedded analytics", "BI ingebouwd in een andere applicatie."),
                      ("Copilot", "AI-assistent in Power BI/Fabric."), ("Gecertificeerde dataset", "Officieel goedgekeurde bron voor rapporten.")],
        "tabel": {"kop": ["Criterium", "Power BI", "Tableau"],
                  "rijen": [["Ecosysteem", "Microsoft", "Salesforce / onafhankelijk"], ["Prijs", "Laag per gebruiker", "Hoger"],
                            ["Sterk in", "Modelleren (DAX), integratie", "Visuele verkenning"], ["Taal", "DAX, Power Query (M)", "Calculated fields, VizQL"]]},
        "fouten": ["Een tool kiezen op demo-indruk in plaats van op criteria.", "Self-service zonder governance → chaos van rapporten.",
                   "Training en adoptie niet in het plan opnemen."],
        "quiz": [("Twee bekendste BI-tools?", "Power BI en Tableau."),
                 ("Hoe adviseer je over een tool?", "Requirements, gewogen criteria, proof-of-concept met echte gebruikers."),
                 ("Wat is een gecertificeerde dataset?", "Officieel goedgekeurd model als single source of truth.")],
    },
    # 009 AI/ML
    {
        "visuals": [
            ("flow", {"steps": ["Historische\ndata", "Trainen\n(model leert)", "Valideren\n(testset)", "Voorspellen\n(nieuwe data)",
                                "Monitoren\n(drift)"], "highlight": [1]},
             "De levenscyclus van een ML-model."),
            ("pyramid", {"levels": ["Verboden", "Hoog risico", "Transparantieplicht", "Minimaal risico"],
                         "notes": ["bv. social scoring", "bv. beslissen over uitkeringen", "bv. chatbots", "bv. spamfilter"]},
             "EU AI Act: risico per toepassing."),
        ],
        "praktijk": "<p>Een ziekenhuis wil no-shows voorspellen. De analist helpt: wat is de waarde (lege OK-tijd), welke data is er "
                    "(afspraakhistorie), wat zijn de risico's (bias naar wijk of leeftijd)? De pilot stuurt alleen een extra "
                    "herinnering – een mens beslist, het model adviseert.</p>",
        "begrippen": [("Supervised learning", "Leren van gelabelde voorbeelden."), ("Classificatie", "Categorie voorspellen (ja/nee)."),
                      ("Regressie", "Getal voorspellen."), ("RAG", "Retrieval-Augmented Generation: LLM antwoordt op basis van eigen documenten."),
                      ("Model drift", "Model wordt slechter omdat de werkelijkheid verandert."), ("Hallucinatie", "GenAI verzint overtuigend klinkende onzin.")],
        "fouten": ["Beginnen met 'we willen AI' in plaats van met een probleem.", "Bias in historische data niet controleren.",
                   "Vertrouwelijke data in publieke AI-tools plakken."],
        "quiz": [("Classificatie vs regressie?", "Classificatie voorspelt een categorie, regressie een getal."),
                 ("Wat is RAG?", "Een LLM die antwoordt op basis van opgehaalde eigen documenten, met bronnen."),
                 ("Hoe deelt de AI Act risico in?", "Per toepassing: verboden, hoog, transparantie, minimaal."),
                 ("Wat is model drift?", "Het model wordt slechter omdat de data/werkelijkheid verandert.")],
    },
    # 010 Adoptie
    {
        "visuals": [
            ("timeline", {"points": [("Urgentie", "waarom nu?"), ("Coalitie", "sponsors"), ("Visie", "waar naartoe"), ("Quick wins", "laat zien"),
                                     ("Verankeren", "nieuwe norm")]},
             "Kotter (vereenvoudigd): verandering in stappen."),
            ("bars", {"items": [("Innovators", 3), ("Early adopters", 13), ("Early majority", 34), ("Late majority", 34), ("Laggards", 16)], "unit": "%"},
             "Rogers' adoptiecurve: begin bij de early adopters als ambassadeurs."),
        ],
        "praktijk": "<p>Na livegang van een nieuw rapportageplatform gebruikt slechts 20% het. De analist zoekt per afdeling een key "
                    "user, organiseert korte 'dashboard-koffie'-sessies, en het MT spreekt af dat maandcijfers alleen nog uit het "
                    "dashboard komen. Na drie maanden: 75% actief gebruik.</p>",
        "begrippen": [("ADKAR", "Awareness, Desire, Knowledge, Ability, Reinforcement."), ("Key user", "Ervaren gebruiker die collega's helpt."),
                      ("Adoptie", "De mate waarin mensen een oplossing echt gebruiken."), ("Usage metrics", "Gebruiksstatistieken (bv. in Power BI).")],
        "fouten": ["Training alleen bij livegang, daarna niets.", "De oude werkwijze laten bestaan naast de nieuwe.",
                   "Het 'waarom' niet uitleggen."],
        "quiz": [("Waar staat ADKAR voor?", "Awareness, Desire, Knowledge, Ability, Reinforcement."),
                 ("Hoe meet je adoptie?", "Usage metrics, tevredenheid en procesindicatoren."),
                 ("Wie zijn je eerste ambassadeurs?", "Early adopters / key users.")],
    },
    # 011 Informatiestromen
    {
        "visuals": [
            ("stack", {"layers": ["Business (processen, organisatie)", "Applicaties (systemen)", "Technologie (infra, cloud)"],
                       "notes": ["Wat doen we?", "Waarmee?", "Waarop draait het?"]},
             "ArchiMate-lagen: architectuur van business tot techniek."),
            ("compare", {"left": ("Traditioneel", ["Data in elke applicatie", "Veel kopieën", "Koppelingen-spaghetti"]),
                         "right": ("Common Ground", ["Data bij de bron", "Opvragen via API's", "Applicaties ontkoppeld"])},
             "Het principe achter Common Ground bij gemeenten."),
        ],
        "praktijk": "<p>Bij een gemeente staan adresgegevens in zeven systemen, die soms van elkaar verschillen. Met het principe "
                    "'eenmalig vastleggen, meervoudig gebruiken' wordt de BRP/BAG de enige bron en halen andere systemen adressen "
                    "via een API op.</p>",
        "begrippen": [("TOGAF", "Raamwerk voor enterprise-architectuur."), ("ArchiMate", "Modelleertaal voor architectuur."),
                      ("NORA / GEMMA", "Referentiearchitecturen voor overheid / gemeenten."), ("Common Ground", "Gemeentelijke visie: data scheiden van applicaties."),
                      ("Basisregistratie", "Wettelijk aangewezen bron (BRP, BAG, KvK).")],
        "fouten": ["Data kopiëren 'omdat het makkelijk is'.", "Architectuurprincipes noemen zonder ze toe te passen in keuzes.",
                   "Handmatige overdrachten niet als risico benoemen."],
        "quiz": [("Noem een belangrijk architectuurprincipe.", "Eenmalig vastleggen, meervoudig gebruiken."),
                 ("Wat is GEMMA?", "De referentiearchitectuur voor gemeenten."),
                 ("Wat is Common Ground?", "Gemeentelijke visie: data bij de bron, applicaties ontkoppeld via API's.")],
    },
    # 012 Roadmap
    {
        "visuals": [
            ("cols", {"cols": [("Nu (0–3 mnd)", ["Quick wins", "KPI-definities", "Governance-start"]),
                               ("Straks (3–12 mnd)", ["Centraal platform", "Kerndomeinen", "Training"]),
                               ("Later (12+ mnd)", ["Self-service", "AI-pilots", "Data als product"])], "labels": ["", ""]},
             "Roadmap in drie horizonten."),
            ("flow", {"steps": ["Initieel", "Herhaalbaar", "Gedefinieerd", "Beheerst", "Optimaliserend"], "highlight": [2]},
             "Data-volwassenheid in vijf niveaus (gebaseerd op CMM)."),
        ],
        "praktijk": "<p>Een directie wil 'datagedreven' worden. De senior analist doet een maturity-scan (niveau 2 van 5), laat drie "
                    "scenario's zien (klein, middel, groot) met kosten en waarde, en adviseert het middelscenario: quick wins én "
                    "fundament tegelijk. De directie kiest – omdat de keuze helder en onderbouwd was.</p>",
        "begrippen": [("Roadmap", "Gefaseerd plan met initiatieven over tijd."), ("Maturity assessment", "Meting van volwassenheid."),
                      ("DAMA-DMBOK", "Standaardwerk over datamanagement met 11 kennisgebieden."),
                      ("Scenario", "Alternatieve route met eigen kosten, waarde en risico.")],
        "fouten": ["Een roadmap vol techniek zonder koppeling aan strategische doelen.", "Eén scenario presenteren – dan heeft de directie niets te kiezen.",
                   "De roadmap nooit herijken."],
        "quiz": [("Drie horizonten van een roadmap?", "Nu, straks, later."),
                 ("Wat is DAMA-DMBOK?", "Standaardwerk over datamanagement."),
                 ("Hoe presenteer je aan een directie?", "Kort, onderbouwd, met 2–3 scenario's om uit te kiezen.")],
    },
]
