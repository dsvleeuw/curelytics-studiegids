# CureLytics – studiegids voor het sollicitatiegesprek

**Open [`curelytics-gids.html`](curelytics-gids.html)** – alles op één plek:
zijbalk met 48 fiches, zoeken (`/`), voortgang ("gekend"), junior/senior-schakelaar, licht/donker,
flashcards en een **quiz-modus** (spatie = omdraaien, ← nog oefenen, → wist ik).

Per fiche: één zin · 2–3 visuals · junior & senior · praktijkvoorbeeld · begrippen · code/tabel ·
valkuilen · ezelsbruggetje · oefenvraag (eerst zelf antwoorden) · flashcards.

| Map | Fiches |
|---|---|
| `00-Algemeen` (10) | bedrijf · proces · detachering · Agile · AVG · cloud · data-stack · **STAR** · **eigen vragen** · **oefencase** |
| `01-BI-Specialist` (12) | BI · DWH/ETL · Kimball · SCD · Data Vault · Power BI · DAX · SQL · cloud-DWH · dashboards · impact/gap · senior |
| `02-Data-Engineer` (14) | rol · streaming · lakehouse · medallion · Spark · Delta · orchestratie · dbt · idempotentie · kwaliteit · IaC · security · governance · CI/CD |
| `03-Data-Analist` (12) | rol · procesanalyse · BPMN · requirements · use cases · stakeholders · business case · BI-tools · AI/ML · adoptie · architectuur · roadmap |

## Feedback geven met Lavish → Claude

Dubbelklik **`Lavish-Claude.bat`**. Het script:

1. bouwt de fiches,
2. opent de gids in Lavish Editor (`http://127.0.0.1:4387/...`),
3. wacht tot jij in de browser iets aanklikt/typt en op **Send to Agent** drukt,
4. stuurt die feedback naar Claude Code (`claude -p`), dat de bron aanpast en opnieuw bouwt,
5. toont Claude's samenvatting in Lavish en wacht op je volgende feedback.

Stoppen: **End session** of **Send & End** in Lavish, of Ctrl+C. Logs staan in `_tools/log/`.

Vereist: Python, Node.js (`npx`) en een ingelogde Claude CLI (`claude`, eenmalig `/login`).

## Zelf aanpassen

Wijzig `_generator/content_*.py` (kern) of `_generator/content_*_extra.py` (uitbreiding) en draai:

```
python _generator/build.py
```
