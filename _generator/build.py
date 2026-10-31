"""Bouwt de studiegids, alle fiches (NNN-*.html) en de index-pagina's.

Bron:  content_<map>.py        (FICHES: kern van elke fiche)
       content_<map>_extra.py  (EXTRA: visuals, praktijk, valkuilen, begrippen, code, tabel, quiz)
Gebruik:  python _generator/build.py
"""
import html
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from diagrams import render  # noqa: E402

SECTIONS = [
    # (map, module, label, korte id, accentkleur-klasse, icoon)
    ("00-Algemeen", "content_algemeen", "Algemeen", "alg", "a0", "◎"),
    ("01-BI-Specialist", "content_bi", "BI Specialist", "bi", "a1", "▤"),
    ("02-Data-Engineer", "content_de", "Data Engineer", "de", "a2", "⛁"),
    ("03-Data-Analist", "content_da", "Data Analist", "da", "a3", "◇"),
]
GIDS = "curelytics-gids.html"

e = html.escape


def slugify(text):
    text = text.lower()
    for a, b in (("é", "e"), ("ë", "e"), ("ï", "i"), ("&", "en")):
        text = text.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def load(module):
    mod = importlib.import_module(module)
    try:
        extra = importlib.import_module(module + "_extra").EXTRA
    except ModuleNotFoundError:
        extra = []
    items = []
    for i, it in enumerate(mod.FICHES):
        merged = dict(it)
        if i < len(extra) and extra[i]:
            merged.update(extra[i])
        items.append(merged)
    return mod, items


# ------------------------------------------------------------------ fiche-render

def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def figure(fid, kind, args, title, caption, big=False):
    svg = render(kind, args, title, fid + "-")
    return (f'<figure class="viz{" big" if big else ""}" id="{fid}">'
            f'<button type="button" class="zoom-btn" data-zoom aria-label="Vergroot deze visual" title="Vergroot">⤢</button>{svg}'
            f'<figcaption>{caption}</figcaption></figure>')


def render_fiche(sec, idx, item, n_total, standalone=False):
    folder, module, label, sid, accent, icon = sec
    num = f"{idx:03d}"
    aid = f"{sid}-{num}"
    bron = f"_generator/{module}.py · FICHES[{idx - 1}]"
    out = [f'<article class="fiche {accent}" id="{aid}" data-bron="{e(bron)}" data-titel="{e(item["title"])}" '
           f'data-search="{e((item["title"] + " " + strip_tags(item["zin"])).lower())}">']

    # hero
    out.append('<header class="hero">'
               f'<div class="hero-meta"><span class="chip sec">{icon} {e(label)}</span>'
               f'<span class="chip">fiche {num} / {n_total:03d}</span>'
               '<span class="chip lvl j">Junior</span><span class="chip lvl s">Senior</span></div>'
               f'<h1><span class="num">{num}</span>{e(item["title"])}</h1>'
               f'<p class="zin" id="{aid}-zin">{item["zin"]}</p>'
               '<div class="hero-actions">'
               f'<button class="btn known" data-known="{aid}" type="button"><span class="ic">○</span> Markeer als gekend</button>'
               '<div class="seg" role="group" aria-label="Niveau">'
               '<button type="button" data-level="beide" class="on">Beide</button>'
               '<button type="button" data-level="junior">Junior</button>'
               '<button type="button" data-level="senior">Senior</button></div></div>'
               '</header>')

    # in-page navigatie
    toc = [("visueel", "Visueel"), ("niveaus", "Junior & senior")]
    if item.get("praktijk"):
        toc.append(("praktijk", "Praktijk"))
    if item.get("begrippen"):
        toc.append(("begrippen", "Begrippen"))
    if item.get("code") or item.get("tabel"):
        toc.append(("detail", "Detail"))
    if item.get("fouten"):
        toc.append(("valkuilen", "Valkuilen"))
    toc.append(("oefenen", "Oefenen"))
    out.append('<nav class="toc">' + "".join(f'<a href="#{aid}-{k}" data-jump>{v}</a>' for k, v in toc) + "</nav>")

    # visuals
    vis = [figure(f"{aid}-v0", *item["diagram"], item["title"], item.get("caption", ""), big=True)]
    extra_vis = item.get("visuals", [])
    gallery = "".join(figure(f"{aid}-v{j + 1}", kind, args, item["title"], cap)
                      for j, (kind, args, cap) in enumerate(extra_vis))
    out.append(f'<section class="block" id="{aid}-visueel"><h2 class="bh"><span>01</span>Visueel</h2>{vis[0]}'
               + (f'<div class="gallery">{gallery}</div>' if gallery else "") + "</section>")

    # niveaus
    out.append(f'<section class="block levels" id="{aid}-niveaus"><h2 class="bh"><span>02</span>Junior &amp; senior</h2>'
               '<div class="lv-grid">'
               f'<div class="card lv junior"><div class="lv-h"><span class="dot"></span>Junior – de kern</div>{ul(item["junior"])}</div>'
               f'<div class="card lv senior"><div class="lv-h"><span class="dot"></span>Senior – de diepte</div>{ul(item["senior"])}</div>'
               '</div></section>')

    n = 3
    if item.get("praktijk"):
        out.append(f'<section class="block" id="{aid}-praktijk"><h2 class="bh"><span>{n:02d}</span>Praktijkvoorbeeld</h2>'
                   f'<div class="card praktijk"><div class="pk-ic">↳</div><div>{item["praktijk"]}</div></div></section>')
        n += 1
    if item.get("begrippen"):
        terms = "".join(f'<div class="term"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in item["begrippen"])
        out.append(f'<section class="block" id="{aid}-begrippen"><h2 class="bh"><span>{n:02d}</span>Begrippen</h2>'
                   f'<dl class="terms">{terms}</dl></section>')
        n += 1
    if item.get("code") or item.get("tabel"):
        body = ""
        if item.get("code"):
            lang, code = item["code"]
            body += (f'<div class="code"><div class="code-h"><span></span><span></span><span></span><em>{e(lang)}</em></div>'
                     f'<pre><code>{e(code.strip())}</code></pre></div>')
        if item.get("tabel"):
            t = item["tabel"]
            head = "".join(f"<th>{h}</th>" for h in t["kop"])
            rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in t["rijen"])
            body += f'<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
        out.append(f'<section class="block" id="{aid}-detail"><h2 class="bh"><span>{n:02d}</span>In detail</h2>{body}</section>')
        n += 1
    if item.get("fouten"):
        cards = "".join(f'<div class="pit"><span>!</span><p>{f}</p></div>' for f in item["fouten"])
        out.append(f'<section class="block" id="{aid}-valkuilen"><h2 class="bh"><span>{n:02d}</span>Valkuilen</h2>'
                   f'<div class="pits">{cards}</div></section>')
        n += 1

    # oefenen
    quiz = item.get("quiz", [])
    flash = "".join(
        f'<button type="button" class="flash" data-q="{e(strip_tags(q))}" data-a="{e(strip_tags(a))}" data-fiche="{aid}">'
        f'<span class="f-in"><span class="f-front"><small>Vraag</small>{q}</span>'
        f'<span class="f-back"><small>Antwoord</small>{a}</span></span></button>' for q, a in quiz)
    out.append(f'<section class="block" id="{aid}-oefenen"><h2 class="bh"><span>{n:02d}</span>Oefenen</h2>'
               f'<div class="ezel"><small>Ezelsbruggetje</small>{item["ezel"]}</div>'
               f'<div class="card vraag"><small>Mogelijke interviewvraag</small><p class="q">“{item["vraag"]}”</p>'
               f'<details><summary>Eerst zelf antwoorden – dan klik voor de antwoordrichting</summary>{ul(item["antwoord"])}</details></div>'
               + (f'<div class="flashes">{flash}</div><p class="hint">Klik op een kaart om hem om te draaien.</p>' if flash else "")
               + "</section>")
    if item.get("curelytics"):
        out.append(f'<p class="cl"><strong>Waarom dit telt bij CureLytics</strong>{item["curelytics"]}</p>')
    out.append("</article>")
    return "".join(out)


# ------------------------------------------------------------------ pagina's

def asset(name):
    return (Path(__file__).resolve().parent / name).read_text(encoding="utf-8")


HEAD = """<!doctype html>
<html lang="nl" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<script>try{{var t=localStorage.getItem('cl-theme');if(t)document.documentElement.dataset.theme=t;else if(matchMedia('(prefers-color-scheme: dark)').matches)document.documentElement.dataset.theme='dark'}}catch(_){{}}</script>
<style>{css}</style></head>
"""


def gids_page(sections):
    css = asset("ui.css")
    js = asset("ui.js")
    side, arts, cards = [], [], []
    total = 0
    for sec, items in sections:
        folder, module, label, sid, accent, icon = sec
        total += len(items)
        links = "".join(
            f'<a href="#{sid}-{i + 1:03d}" class="nav-f" data-id="{sid}-{i + 1:03d}" data-search="'
            f'{e((it["title"] + " " + strip_tags(it["zin"])).lower())}"><span class="n">{i + 1:03d}</span>'
            f'<span class="t">{e(it["title"])}</span><span class="k">✓</span></a>' for i, it in enumerate(items))
        side.append(f'<div class="nav-sec {accent}" data-sec="{sid}"><button type="button" class="nav-h">'
                    f'<span class="ic">{icon}</span><span class="lb">{e(label)}</span>'
                    f'<span class="pr" data-progress="{sid}">0/{len(items)}</span></button>'
                    f'<div class="nav-list">{links}</div></div>')
        for i, it in enumerate(items):
            arts.append(render_fiche(sec, i + 1, it, len(items)))
        mod = importlib.import_module(module)
        cards.append(f'<a class="sec-card {accent}" href="#{sid}-001"><span class="ic">{icon}</span>'
                     f'<strong>{e(label)}</strong><span>{len(items)} fiches</span><p>{strip_tags(mod.INTRO)}</p>'
                     f'<span class="bar"><i data-bar="{sid}"></i></span></a>')

    home = f"""<section class="view home" id="home">
<div class="home-hero"><span class="chip sec">Sollicitatie · dinsdag</span>
<h1>CureLytics<br><span class="grad">studiegids</span></h1>
<p>{total} fiches over alles wat CureLytics zoekt in BI Specialists, Data Engineers en Data Analisten.
Per fiche: één zin, visuals, junior- én seniorniveau, praktijk, valkuilen, oefenvragen en flashcards.</p>
<div class="hero-cta"><a class="btn primary" href="#alg-001">Start bij 001</a><a class="btn" href="#quiz">⚡ Quiz-modus</a></div>
<div class="stats"><div><b data-stat="known">0</b><span>gekend</span></div><div><b>{total}</b><span>fiches</span></div>
<div><b data-stat="cards">0</b><span>flashcards</span></div></div></div>
<div class="sec-cards">{''.join(cards)}</div>
<div class="plan card"><h2>Plan tot dinsdag</h2><ol>
<li><b>Vandaag:</b> 00 Algemeen helemaal (bedrijf, proces, STAR, eigen vragen).</li>
<li><b>Dag 2:</b> de map van jouw rol – per fiche eerst de zin + visual, dan junior.</li>
<li><b>Dag 3:</b> senior-kolommen en valkuilen; oefenvragen hardop beantwoorden.</li>
<li><b>Maandag:</b> quiz-modus tot alles groen is; oefencase (alg-010) één keer helemaal doen.</li>
<li><b>Dinsdag ochtend:</b> alleen de ezelsbruggetjes doorlopen. Rust.</li></ol></div>
</section>"""

    quiz = """<section class="view quiz" id="quiz"><div class="quiz-wrap">
<div class="quiz-top"><h1>⚡ Quiz-modus</h1><div class="quiz-filter" role="group" aria-label="Map">
<button type="button" data-qf="alle" class="on">Alles</button><button type="button" data-qf="alg">Algemeen</button>
<button type="button" data-qf="bi">BI</button><button type="button" data-qf="de">DE</button><button type="button" data-qf="da">DA</button></div></div>
<div class="quiz-progress"><i></i></div><p class="quiz-count"></p>
<button type="button" class="flash big" id="quiz-card"><span class="f-in"><span class="f-front"><small>Vraag</small><span class="qq"></span></span>
<span class="f-back"><small>Antwoord</small><span class="qa"></span></span></span></button>
<div class="quiz-actions"><button type="button" class="btn" data-qa="again">↺ Nog oefenen</button>
<button type="button" class="btn primary" data-qa="know">✓ Wist ik</button></div>
<p class="hint">Spatie = omdraaien · ← nog oefenen · → wist ik · <a href="#" data-qsrc>naar de fiche</a></p></div></section>"""

    body = f"""<body class="app">
<aside class="side"><div class="side-top"><div class="brand"><span class="logo">C</span><div><b>CureLytics</b><small>studiegids</small></div>
<button type="button" class="icon-btn" data-side-toggle aria-label="Zijbalk inklappen" title="Zijbalk inklappen ( [ )">«</button>
<button type="button" class="icon-btn" data-theme-toggle aria-label="Licht/donker">◐</button></div>
<label class="search"><span>⌕</span><input type="search" placeholder="Zoek concept… ( / )" id="q" autocomplete="off"></label></div>
<nav class="nav"><a href="#home" class="nav-top" data-id="home">⌂ Overzicht</a><a href="#quiz" class="nav-top" data-id="quiz">⚡ Quiz-modus</a>{''.join(side)}</nav>
<div class="side-foot"><div class="ring"><svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="15.5" class="rb"/><circle cx="18" cy="18" r="15.5" class="rf" id="ring"/></svg><b id="ring-t">0%</b></div>
<span>van alle fiches gekend</span></div></aside>
<button type="button" class="menu-btn" aria-label="Menu">☰</button>
<button type="button" class="side-open" data-side-toggle aria-label="Zijbalk openen" title="Zijbalk openen ( [ )">☰</button>
<main class="main">{home}{quiz}<div class="fiches">{''.join(arts)}</div>
<nav class="pager"><a href="#" data-prev>← vorige</a><span data-pos></span><a href="#" data-next>volgende →</a></nav></main>
<script>{js}</script></body></html>
"""
    return HEAD.format(title="CureLytics – studiegids", css=css) + body


def standalone_page(sec, idx, item, n_total, prev_name, next_name):
    folder, module, label, sid, accent, icon = sec
    css = asset("ui.css")
    js = asset("ui.js")
    aid = f"{sid}-{idx:03d}"
    nav = (f'<nav class="pager solo">{f"<a href={chr(34)}{prev_name}{chr(34)}>← vorige</a>" if prev_name else "<span></span>"}'
           f'<a href="index.html">overzicht</a>'
           f'{f"<a href={chr(34)}{next_name}{chr(34)}>volgende →</a>" if next_name else "<span></span>"}</nav>')
    body = (f'<body class="solo"><header class="solo-top"><a href="../{GIDS}#{aid}" class="brand-s"><span class="logo">C</span>'
            f'CureLytics studiegids</a><span class="crumb"><a href="index.html">{e(label)}</a> / {idx:03d}</span>'
            f'<button type="button" class="icon-btn" data-theme-toggle aria-label="Licht/donker">◐</button></header>'
            f'<main class="main solo-main">{render_fiche(sec, idx, item, n_total, True)}{nav}</main><script>{js}</script></body></html>\n')
    return HEAD.format(title=f"{idx:03d} {e(item['title'])}", css=css) + body


def index_page(title, intro, cards, back=True):
    css = asset("ui.css")
    js = asset("ui.js")
    top = (f'<header class="solo-top"><a href="{"../" if back else ""}{GIDS}" class="brand-s"><span class="logo">C</span>'
           f'CureLytics studiegids</a><button type="button" class="icon-btn" data-theme-toggle aria-label="Licht/donker">◐</button></header>')
    grid = "".join(f'<a class="idx-card" href="{h}"><span class="n">{n}</span><strong>{e(t)}</strong><p>{z}</p></a>'
                   for h, n, t, z in cards)
    body = (f'<body class="solo">{top}<main class="main solo-main"><div class="home-hero small"><h1>{e(title)}</h1><p>{intro}</p></div>'
            f'<div class="idx-grid">{grid}</div></main><script>{js}</script></body></html>\n')
    return HEAD.format(title=e(title), css=css) + body


def main():
    loaded = []
    root_cards = []
    for sec in SECTIONS:
        folder, module, label, sid, accent, icon = sec
        mod, items = load(module)
        loaded.append((sec, items))
        out = ROOT / folder
        out.mkdir(exist_ok=True)
        for old in out.glob("[0-9][0-9][0-9]-*.html"):
            old.unlink()
        names = [f"{i + 1:03d}-{slugify(it['title'])}.html" for i, it in enumerate(items)]
        for i, it in enumerate(items):
            page = standalone_page(sec, i + 1, it, len(items),
                                   names[i - 1] if i else None, names[i + 1] if i + 1 < len(items) else None)
            (out / names[i]).write_text(page, encoding="utf-8")
        cards = [(names[i], f"{i + 1:03d}", it["title"], strip_tags(it["zin"])) for i, it in enumerate(items)]
        (out / "index.html").write_text(index_page(label, mod.INTRO, cards), encoding="utf-8")
        root_cards.append((f"{folder}/index.html", folder[:2], label, f"{len(items)} fiches – {strip_tags(mod.INTRO)}"))
        n_extra = sum(1 for it in items if it.get("quiz"))
        print(f"{folder}: {len(items)} fiches ({n_extra} uitgebreid)")
    (ROOT / GIDS).write_text(gids_page(loaded), encoding="utf-8")
    (ROOT / "index.html").write_text(index_page(
        "CureLytics – alle fiches",
        f"Losse fiches per map. Liever alles op één plek met zoeken, voortgang en quiz? Open <a href='{GIDS}'>de studiegids</a>.",
        root_cards, back=False), encoding="utf-8")
    print(f"studiegids: {GIDS}")


if __name__ == "__main__":
    main()
