# CureLytics – sollicitatievoorbereiding

Voorbereiding op een sollicitatiegesprek bij **CureLytics** (Haarlem, onderdeel van QRC Group) –
Data & Analytics detachering. Vacatures: https://curelytics.nl/onze-vacatures/

## Structuur

| Pad | Inhoud |
|---|---|
| `curelytics-gids.html` | **De studiegids**: alle fiches in één pagina (zijbalk, zoeken, voortgang, quiz) |
| `00-Algemeen/` … `03-Data-Analist/` | Losse fiches `NNN-onderwerp.html` + `index.html` per map |
| `_generator/content_<map>.py` | `FICHES`: kern per fiche (zin, hoofddiagram, junior, senior, ezel, vraag) |
| `_generator/content_<map>_extra.py` | `EXTRA` (zelfde index): visuals, praktijk, begrippen, code, tabel, valkuilen, quiz |
| `_generator/build.py` | Bouwt alles; `diagrams.py` = SVG-diagramtypes; `ui.css` / `ui.js` = opmaak en gedrag |
| `Lavish-Claude.bat` + `_tools/lavish-claude.ps1` | Opent de gids in Lavish en stuurt elke feedback naar `claude -p` |
| `_bronnen/` | Clones van `kunchenguid/kun` en `kunchenguid/lavish-axi` (alleen lezen) |

## Regels

- **Bewerk nooit de gegenereerde HTML.** Pas `_generator/*.py|css|js` aan en draai `python _generator/build.py`.
- Elk `<article>` in de gids heeft `id` (bv. `bi-004`) en `data-bron` (bv. `_generator/content_bi.py · FICHES[3]`).
  Index in `FICHES` en `EXTRA` is gelijk (0-gebaseerd; fiche 004 = index 3).
- Diagramtypes (`diagrams.py`): flow, stack, hub, grid, compare, cycle, cols, pyramid, timeline, venn, tree, funnel, bars.
  Labels kort houden (SVG-tekst wrapt niet); `\n` voor een tweede regel.
- Taal: Nederlands. Vaktermen in het Engels waar dat in de praktijk zo heet. Feitelijk juist blijven (AVG, AI Act, tools).
- Na een wijziging: build draaien; de build print per map het aantal fiches.

## Werkwijze (Kun)

- Explainers volgens Kun's ENTRY.md: weinig proza, één concept per diagram, inline SVG, uitleg vanaf nul.
- Review in Lavish: dubbelklik `Lavish-Claude.bat`. Handmatig: `npx -y lavish-axi curelytics-gids.html`,
  feedback ophalen met `npx -y lavish-axi poll curelytics-gids.html`. Actuele instructies: `npx -y lavish-axi --help`.
- Design: CureLytics-huisstijl (teal `#1B9C85`, navy `#06307e`, Libre Franklin), licht + donker.
