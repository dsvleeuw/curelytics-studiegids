"""Exporteert per rol één .txt-bestand om als bron in NotebookLM te plakken (voor uitlegvideo's).

Gebruik:  python _generator/export_notebooklm.py
Uitvoer:  _generator/notebooklm-<map>.txt  (BI Specialist, Data Engineer, Data Analist)

Bron = dezelfde FICHES/EXTRA als de studiegids, dus na een inhoudswijziging opnieuw draaien.
Visuals worden in woorden beschreven, HTML wordt platte tekst.
"""
import html
import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build import SECTIONS, load  # noqa: E402

ROLLEN = [s for s in SECTIONS if s[3] != "alg"]
# Algemene fiches die als korte context bovenaan elke rol komen
CONTEXT_IDX = [0, 2]  # 001 CureLytics, 003 detachering


def txt(s):
    """HTML → platte tekst."""
    s = re.sub(r"<br\s*/?>|</p>\s*<p>", "\n", s or "")
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).replace(" ", " ").strip()


def lab(s):
    # "Bedrijfs-\nleven" (afbreking in een diagramlabel) → "Bedrijfsleven"
    return re.sub(r"-\n(?=[a-z])", "", txt(str(s))).replace("\n", " ").strip()


def describe(kind, a):
    """Beschrijf een diagram in één of enkele zinnen."""
    if kind in ("flow", "cycle"):
        steps = [lab(s) for s in a["steps"]]
        labels = a.get("labels") or []
        out = steps[0]
        for i, s in enumerate(steps[1:]):
            via = f" —({lab(labels[i])})→ " if i < len(labels) and labels[i] else " → "
            out += via + s
        return ("Cyclus (herhaalt zich): " + out + " → terug naar het begin") if kind == "cycle" else ("Stappen: " + out)
    if kind == "compare":
        (lh, li), (rh, ri) = a["left"], a["right"]
        return (f"Vergelijking. {lab(lh)}: {'; '.join(map(lab, li))}. "
                f"Tegenover {lab(rh)}: {'; '.join(map(lab, ri))}.")
    if kind == "cols":
        parts = [f"{lab(h)}: {'; '.join(map(lab, items))}" for h, items in a["cols"]]
        sep = " → " if a.get("arrows", True) else " | "
        return "Kolommen: " + sep.join(parts)
    if kind in ("stack", "pyramid", "funnel"):
        notes = a.get("notes") or []
        items = a.get("layers") or a.get("levels") or a.get("stages")
        parts = [lab(x) + (f" ({lab(notes[i])})" if i < len(notes) and notes[i] else "") for i, x in enumerate(items)]
        head = {"stack": "Lagen, van boven (dichtst bij de gebruiker) naar onder",
                "pyramid": "Piramide, van top naar basis",
                "funnel": "Trechter, van breed naar smal"}[kind]
        return f"{head}: " + "; ".join(parts)
    if kind == "hub":
        sl = a.get("spoke_labels") or []
        parts = [lab(s) + (f" ({lab(sl[i])})" if i < len(sl) and sl[i] else "") for i, s in enumerate(a["spokes"])]
        return f"Centraal begrip {lab(a['center'])}, met daaromheen: " + "; ".join(parts)
    if kind == "grid":
        q = [lab(x) for x in a["quadrants"]]
        return (f"2x2-matrix (horizontaal: {lab(a['x_axis'])}; verticaal: {lab(a['y_axis'])}). "
                f"Linksboven: {q[0]}. Rechtsboven: {q[1]}. Linksonder: {q[2]}. Rechtsonder: {q[3]}.")
    if kind == "timeline":
        return "Tijdlijn: " + " → ".join(f"{lab(p)} ({lab(s)})" for p, s in a["points"])
    if kind == "venn":
        c = f"; in de overlap: {lab(a['center'])}" if a.get("center") else ""
        return "Overlappende gebieden: " + ", ".join(map(lab, a["sets"])) + c
    if kind == "tree":
        parts = [f"{lab(c)} ({', '.join(map(lab, kids))})" if kids else lab(c) for c, kids in a["children"]]
        return f"{lab(a['root'])} vertakt in: " + "; ".join(parts)
    if kind == "bars":
        u = a.get("unit", "")
        return "Staafdiagram: " + "; ".join(f"{lab(n)} {v}{u}" for n, v in a["items"])
    return ""


def fiche_txt(nr, it, kort=False):
    L = [f"### {nr} — {lab(it['title'])}", "", f"Kern: {txt(it['zin'])}", ""]
    L.append(f"Visual: {describe(*it['diagram'])}")
    if it.get("caption"):
        L.append(f"Toelichting: {txt(it['caption'])}")
    L.append("")
    if kort:
        L += ["Wat je moet weten:"] + [f"- {txt(x)}" for x in it["junior"] + it["senior"]] + [""]
        return "\n".join(L)
    for kind, args, cap in it.get("visuals", []):
        L.append(f"Extra visual: {describe(kind, args)}")
        if cap:
            L.append(f"Toelichting: {txt(cap)}")
    if it.get("visuals"):
        L.append("")
    L += ["Junior-niveau (de basis):"] + [f"- {txt(x)}" for x in it["junior"]] + [""]
    L += ["Senior-niveau (verdieping):"] + [f"- {txt(x)}" for x in it["senior"]] + [""]
    if it.get("praktijk"):
        L += ["Praktijkvoorbeeld:", txt(it["praktijk"]), ""]
    if it.get("begrippen"):
        L += ["Begrippen:"] + [f"- {lab(t)}: {txt(d)}" for t, d in it["begrippen"]] + [""]
    if it.get("tabel"):
        t = it["tabel"]
        L += ["Voorbeeldtabel (" + " | ".join(map(lab, t["kop"])) + "):"]
        L += ["- " + " | ".join(map(lab, r)) for r in t["rijen"]] + [""]
    if it.get("code"):
        taal, code = it["code"][0], it["code"][1]
        L += [f"Codevoorbeeld ({taal}):", code.strip(), ""]
    if it.get("fouten"):
        L += ["Veelgemaakte fouten:"] + [f"- {txt(x)}" for x in it["fouten"]] + [""]
    L += [f"Ezelsbruggetje: {txt(it['ezel'])}", ""]
    L += [f"Oefenvraag uit een sollicitatiegesprek: {txt(it['vraag'])}", "Sterke antwoordrichting:"]
    L += [f"- {txt(x)}" for x in it["antwoord"]] + [""]
    if it.get("quiz"):
        L += ["Snelle controlevragen:"] + [f"- V: {txt(q)} A: {txt(a)}" for q, a in it["quiz"]] + [""]
    L += [f"Waarom dit telt bij CureLytics: {txt(it['curelytics'])}", ""]
    return "\n".join(L)


def main():
    _, alg = load("content_algemeen")
    context = "\n".join(fiche_txt(f"Context {i + 1:03d}", alg[i], kort=True) for i in CONTEXT_IDX)
    for folder, module, label, short, *_ in ROLLEN:
        mod, items = load(module)
        intro = txt(getattr(mod, "INTRO", ""))
        inhoud = "\n".join(f"{i + 1:03d}. {lab(it['title'])}" for i, it in enumerate(items))
        doc = [
            f"# CureLytics — {label}: studiemateriaal voor uitlegvideo's",
            "",
            "Doel van deze bron: korte, heldere uitlegvideo's maken voor iemand die zich voorbereidt op een "
            f"sollicitatiegesprek bij CureLytics voor de rol {label}. Leg elk onderwerp uit vanaf nul, "
            "eerst op junior-niveau en daarna de senior-verdieping, met de praktijkvoorbeelden en "
            "ezelsbruggetjes uit dit document. Taal: Nederlands; vaktermen in het Engels zoals in de praktijk.",
            "",
            f"Over de vacature: {intro}",
            "",
            "## Context: het bedrijf en de rol van consultant",
            "",
            context,
            "## Inhoud",
            "",
            inhoud,
            "",
            "## Onderwerpen",
            "",
        ]
        doc += [fiche_txt(f"{i + 1:03d}", it) for i, it in enumerate(items)]
        out = HERE / f"notebooklm-{folder.lower()}.txt"
        out.write_text("\n".join(doc).rstrip() + "\n", encoding="utf-8")
        print(f"{out.name}: {len(items)} onderwerpen, {len(out.read_text(encoding='utf-8').split())} woorden")


if __name__ == "__main__":
    main()
