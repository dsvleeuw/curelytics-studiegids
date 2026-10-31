"""Inline-SVG diagrammen voor de fiches.

Elke functie geeft een complete <svg> terug. Ids en url(#...) gebruiken het
teken '§' als plaatshouder; build.py vervangt dat door een unieke prefix, zodat
meerdere diagrammen op één pagina (de studiegids) niet botsen.
Kleuren lopen via CSS-variabelen (light/dark). Labels kort houden: SVG-tekst wrapt niet.
"""
import html
import math

e = html.escape


def _text(x, y, label, cls="lbl", size=15, anchor="middle"):
    parts = label.split("\n")
    start = y - (len(parts) - 1) * size * 0.6
    return "".join(
        f'<text x="{x:.0f}" y="{start + i * size * 1.2:.0f}" class="{cls}" text-anchor="{anchor}" '
        f'dominant-baseline="middle">{e(p)}</text>' for i, p in enumerate(parts))


def _box(id_, x, y, w, h, label, kind="node", rx=14):
    tip = label.replace("\n", " ")
    return (f'<g id="§{id_}" class="{kind}"><title>{e(tip)}</title>'
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}"/>'
            f'{_text(x + w / 2, y + h / 2, label)}</g>')


def _tw(label, size=15):
    """Geschatte tekstbreedte (px) van de langste regel."""
    return max((len(r) for r in (label or "").split(chr(10))), default=0) * size * 0.58


def _arrow(id_, x1, y1, x2, y2, label=None):
    lab = ""
    if label:
        lab = (f'<text x="{(x1 + x2) / 2:.0f}" y="{min(y1, y2) - 10:.0f}" class="edge-lbl" '
               f'text-anchor="middle">{e(label)}</text>')
    return (f'<g id="§{id_}" class="edge"><title>{e(label or "")}</title>'
            f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" marker-end="url(#§arr)"/>{lab}</g>')


DEFS = ('<defs>'
        '<marker id="§arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrowhead"/></marker>'
        '<linearGradient id="§grad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" class="g0"/>'
        '<stop offset="1" class="g1"/></linearGradient>'
        '<filter id="§sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="3" '
        'stdDeviation="4" class="shadow"/></filter>'
        '</defs>')


def _svg(w, h, body, title):
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{e(title)}" '
            f'xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>')


# ------------------------------------------------------------------ typen

def flow(steps, title, labels=None, highlight=None):
    """Horizontale keten van stappen met pijlen. Gat en breedte groeien mee met de labels."""
    n = len(steps)
    gap = max([36] + [_tw(l, 13) + 22 for l in (labels or []) if l])
    bw = max(max(_tw(s) for s in steps) + 28, 120)
    w = max(880, 40 + n * bw + (n - 1) * gap)
    bw = (w - 40 - gap * (n - 1)) / n
    bh, y = 100, 44
    body = []
    for i, s in enumerate(steps):
        x = 20 + i * (bw + gap)
        kind = "node hl" if highlight and i in highlight else "node"
        body.append(f'<text x="{x + 16:.0f}" y="{y - 12}" class="step-no">{i + 1:02d}</text>')
        body.append(_box(f"stap-{i + 1}", x, y, bw, bh, s, kind))
        if i < n - 1:
            lab = labels[i] if labels and i < len(labels) else None
            body.append(_arrow(f"pijl-{i + 1}", x + bw + 4, y + bh / 2, x + bw + gap - 4, y + bh / 2, lab))
    return _svg(w, 170, "".join(body), title)


def stack(layers, title, notes=None):
    """Verticale lagen; boven = dichtst bij de gebruiker."""
    lh, gap = 58, 12
    body = []
    for i, layer in enumerate(layers):
        y = 15 + i * (lh + gap)
        inset = i * 14
        body.append(_box(f"laag-{i + 1}", 30 + inset, y, 480 - 2 * inset, lh, layer,
                         "node hl" if i == 0 else ("node alt" if i % 2 else "node")))
        if notes and i < len(notes) and notes[i]:
            body.append(f'<g id="§noot-{i + 1}" class="note"><title>{e(notes[i])}</title>'
                        f'<line x1="{520 - inset}" y1="{y + lh / 2}" x2="556" y2="{y + lh / 2}" class="dash"/>'
                        f'<circle cx="556" cy="{y + lh / 2}" r="4" class="dot"/>'
                        f'<text x="568" y="{y + lh / 2}" class="note-txt" dominant-baseline="middle">{e(notes[i])}</text></g>')
    return _svg(880, 30 + len(layers) * (lh + gap), "".join(body), title)


def hub(center, spokes, title, center_shape="circle", spoke_labels=None):
    """Centraal begrip met satellieten (ook: ster-schema)."""
    cx, cy, rx, ry = 440, 210, 300, 150
    n = len(spokes)
    pos = [(cx + rx * math.cos(-math.pi / 2 + 2 * math.pi * i / n),
            cy + ry * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    body = []
    for i, (x, y) in enumerate(pos):
        lab = spoke_labels[i] if spoke_labels else ""
        body.append(f'<g id="§lijn-{i + 1}" class="edge plain"><title>{e(lab)}</title>'
                    f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}"/></g>')
    if center_shape == "rect":
        body.append(_box("kern", cx - 100, cy - 44, 200, 88, center, "node hl"))
    else:
        body.append(f'<g id="§kern" class="node hl"><title>{e(center.replace(chr(10), " "))}</title>'
                    f'<circle cx="{cx}" cy="{cy}" r="72"/>{_text(cx, cy, center)}</g>')
    for i, (x, y) in enumerate(pos):
        body.append(_box(f"punt-{i + 1}", x - 84, y - 30, 168, 60, spokes[i]))
    return _svg(880, 420, "".join(body), title)


def grid(quadrants, title, x_axis, y_axis, highlight=1):
    """2x2-matrix: linksboven, rechtsboven, linksonder, rechtsonder."""
    x0, y0, s, h = 200, 20, 240, 150
    body = []
    for i, q in enumerate(quadrants):
        body.append(_box(f"kwadrant-{i + 1}", x0 + (i % 2) * s + 6, y0 + (i // 2) * h + 6, s - 12, h - 12, q,
                         "node hl" if i == highlight else "node"))
    yb = y0 + 2 * h
    body.append(f'<g class="edge"><line x1="{x0}" y1="{yb + 14}" x2="{x0 + 2 * s}" y2="{yb + 14}" marker-end="url(#§arr)"/>'
                f'<text x="{x0 + s}" y="{yb + 38}" class="edge-lbl" text-anchor="middle">{e(x_axis)}</text></g>')
    body.append(f'<g class="edge"><line x1="{x0 - 14}" y1="{yb}" x2="{x0 - 14}" y2="{y0}" marker-end="url(#§arr)"/>'
                f'<text x="{x0 - 28}" y="{(y0 + yb) / 2}" class="edge-lbl" text-anchor="end" dominant-baseline="middle">{e(y_axis)}</text></g>')
    return _svg(880, yb + 54, "".join(body), title)


def compare(left, right, title):
    """Twee kolommen: (kop, [punten])."""
    body = []
    for side, (head, items) in enumerate((left, right)):
        x = 30 + side * 430
        body.append(_box(f"kop-{side + 1}", x, 15, 390, 56, head, "node hl"))
        for j, it in enumerate(items):
            body.append(_box(f"punt-{side + 1}-{j + 1}", x + 16, 88 + j * 56, 358, 44, it, "node soft", rx=10))
    body.append('<circle cx="440" cy="43" r="22" class="vs-c"/><text x="440" y="44" class="vs" '
                'text-anchor="middle" dominant-baseline="middle">vs</text>')
    rows = max(len(left[1]), len(right[1]))
    return _svg(880, 100 + rows * 56, "".join(body), title)


def cycle(steps, title):
    """Cyclus (iteratief proces)."""
    cx, cy, r = 440, 200, 150
    n = len(steps)
    body = [f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 1.75:.0f}" ry="{r}" class="orbit"/>']
    for i, s in enumerate(steps):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + r * 1.75 * math.cos(ang), cy + r * math.sin(ang)
        body.append(_box(f"fase-{i + 1}", x - 88, y - 30, 176, 60, s, "node hl" if i == 0 else "node"))
    body.append(_text(cx, cy, "herhaal\nelke sprint", "center-lbl", 16))
    return _svg(880, 400, "".join(body), title)


def cols(cols, title, labels=None, arrows=True):
    """Kolommen links→rechts, elk met kop en items. Gat en breedte groeien mee met de labels."""
    n = len(cols)
    gap = max([30] + [_tw(l, 13) + 18 for l in (labels or []) if l]) if arrows else 30
    need = max(max([_tw(c[0])] + [_tw(it) + 16 for it in c[1]]) + 28 for c in cols)
    w = max(880, 40 + n * need + (n - 1) * gap)
    cw = (w - 40 - gap * (n - 1)) / n
    rows = max(len(c[1]) for c in cols)
    body = []
    for i, (head, items) in enumerate(cols):
        x = 20 + i * (cw + gap)
        body.append(_box(f"kolom-{i + 1}", x, 15, cw, 56, head, "node hl"))
        for j, it in enumerate(items):
            body.append(_box(f"item-{i + 1}-{j + 1}", x + 8, 84 + j * 52, cw - 16, 42, it, "node soft", rx=10))
        if arrows and i < n - 1:
            lab = labels[i] if labels and i < len(labels) else None
            body.append(_arrow(f"pijl-{i + 1}", x + cw + 3, 43, x + cw + gap - 3, 43, lab))
    return _svg(w, 100 + rows * 52, "".join(body), title)


def pyramid(levels, title, notes=None):
    """Piramide; levels van top naar basis."""
    n = len(levels)
    top_y, h = 15, 64
    body = []
    for i, lab in enumerate(levels):
        y = top_y + i * h
        half_top = 40 + i * 60
        half_bot = 40 + (i + 1) * 60
        cx = 300
        pts = f"{cx - half_top},{y} {cx + half_top},{y} {cx + half_bot},{y + h - 6} {cx - half_bot},{y + h - 6}"
        kind = "node hl" if i == 0 else ("node alt" if i % 2 else "node")
        body.append(f'<g id="§niveau-{i + 1}" class="{kind}"><title>{e(lab)}</title>'
                    f'<polygon points="{pts}"/>{_text(cx, y + (h - 6) / 2, lab)}</g>')
        if notes and i < len(notes) and notes[i]:
            body.append(f'<g class="note"><line x1="{cx + half_bot + 8}" y1="{y + h / 2 - 3}" x2="640" y2="{y + h / 2 - 3}" class="dash"/>'
                        f'<text x="650" y="{y + h / 2 - 3}" class="note-txt" dominant-baseline="middle">{e(notes[i])}</text></g>')
    return _svg(880, top_y + n * h + 10, "".join(body), title)


def timeline(points, title):
    """Tijdlijn: [(label, sublabel)]."""
    n = len(points)
    x0, x1, y = 70, 810, 90
    body = [f'<line x1="{x0 - 30}" y1="{y}" x2="{x1 + 30}" y2="{y}" class="tl-line"/>']
    for i, (lab, sub) in enumerate(points):
        x = x0 + (x1 - x0) * (i / (n - 1) if n > 1 else 0.5)
        up = i % 2 == 0
        body.append(f'<g id="§moment-{i + 1}" class="tl"><title>{e(lab)} – {e(sub)}</title>'
                    f'<circle cx="{x:.0f}" cy="{y}" r="11" class="tl-dot"/>'
                    f'<text x="{x:.0f}" y="{y + 1}" class="tl-no" text-anchor="middle" dominant-baseline="middle">{i + 1}</text>'
                    f'{_text(x, y - 40 if up else y + 40, lab, "lbl", 15)}'
                    f'{_text(x, y - 18 if up else y + 64, sub, "edge-lbl", 13)}</g>')
    return _svg(880, 180, "".join(body), title)


def venn(sets, title, center=None):
    """2 of 3 overlappende cirkels."""
    body = []
    if len(sets) == 2:
        pos = [(350, 160), (530, 160)]
        r = 130
        lab_pos = [(290, 160), (590, 160)]
        cpos = (440, 160)
    else:
        pos = [(370, 140), (510, 140), (440, 255)]
        r = 115
        lab_pos = [(320, 115), (560, 115), (440, 305)]
        cpos = (440, 180)
    for i, (x, y) in enumerate(pos):
        body.append(f'<g id="§set-{i + 1}" class="venn v{i}"><title>{e(sets[i].replace(chr(10), " "))}</title>'
                    f'<circle cx="{x}" cy="{y}" r="{r}"/></g>')
    for i, (x, y) in enumerate(lab_pos):
        body.append(_text(x, y, sets[i]))
    if center:
        body.append(f'<g id="§midden" class="venn-c"><title>{e(center)}</title>{_text(*cpos, center, "center-lbl", 15)}</g>')
    return _svg(880, 400 if len(sets) == 3 else 320, "".join(body), title)


def tree(root, children, title):
    """Boom: root met kinderen [(label, [kleinkinderen])]."""
    n = len(children)
    cw = 840 / n
    body = [_box("root", 340, 12, 200, 56, root, "node hl")]
    for i, (lab, kids) in enumerate(children):
        cx = 20 + cw * i + cw / 2
        body.append(f'<g class="edge plain"><path d="M440,68 C440,95 {cx:.0f},95 {cx:.0f},118" fill="none"/></g>')
        body.append(_box(f"tak-{i + 1}", cx - cw / 2 + 8, 118, cw - 16, 52, lab))
        for j, k in enumerate(kids):
            body.append(_box(f"blad-{i + 1}-{j + 1}", cx - cw / 2 + 18, 186 + j * 48, cw - 36, 38, k, "node soft", rx=10))
    rows = max((len(k) for _, k in children), default=0)
    return _svg(880, 200 + rows * 48, "".join(body), title)


def funnel(stages, title, notes=None):
    """Trechter: van breed naar smal."""
    n = len(stages)
    h = 58
    body = []
    for i, s in enumerate(stages):
        y = 12 + i * (h + 6)
        wt = 520 - i * (360 / n)
        wb = 520 - (i + 1) * (360 / n)
        cx = 300
        pts = f"{cx - wt / 2},{y} {cx + wt / 2},{y} {cx + wb / 2},{y + h} {cx - wb / 2},{y + h}"
        body.append(f'<g id="§fase-{i + 1}" class="{"node hl" if i == n - 1 else "node"}"><title>{e(s)}</title>'
                    f'<polygon points="{pts}"/>{_text(cx, y + h / 2, s)}</g>')
        if notes and i < len(notes):
            body.append(f'<text x="600" y="{y + h / 2}" class="note-txt" dominant-baseline="middle">{e(notes[i])}</text>')
    return _svg(880, 24 + n * (h + 6), "".join(body), title)


def bars(items, title, unit=""):
    """Horizontale staafjes: [(label, waarde)] – waarde 0..100."""
    body = []
    for i, (lab, val) in enumerate(items):
        y = 14 + i * 46
        body.append(f'<text x="210" y="{y + 16}" class="lbl" text-anchor="end" dominant-baseline="middle">{e(lab)}</text>'
                    f'<rect x="224" y="{y + 2}" width="560" height="28" rx="8" class="bar-bg"/>'
                    f'<g id="§staaf-{i + 1}" class="bar"><title>{e(lab)}: {val}{unit}</title>'
                    f'<rect x="224" y="{y + 2}" width="{5.6 * val:.0f}" height="28" rx="8"/></g>'
                    f'<text x="{232 + 5.6 * val:.0f}" y="{y + 16}" class="edge-lbl" dominant-baseline="middle">{val}{unit}</text>')
    return _svg(880, 24 + len(items) * 46, "".join(body), title)


DIAGRAMS = {
    "flow": flow, "stack": stack, "hub": hub, "grid": grid, "compare": compare, "cycle": cycle,
    "cols": cols, "pyramid": pyramid, "timeline": timeline, "venn": venn, "tree": tree,
    "funnel": funnel, "bars": bars,
}


def render(kind, args, title, prefix):
    return DIAGRAMS[kind](**args, title=title).replace("§", prefix)
