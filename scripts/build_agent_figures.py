"""Lehrbilder für den Teil „Mit einem Coding-Agenten“ (agent-n8n/), SVG ohne Abhängigkeiten.

Stil wie build_overview_figures.py und wie figlib im Kurs „Produktiv mit einem
Agenten arbeiten“: weißer Grund, Inter, Akzent #0052ff, Schrift mindestens 16 px,
Titel 20 px, Grün/Rot nur für Richtig/Falsch, Gelb für Rückfragen und Vorsicht.

Aufruf: python3 scripts/build_agent_figures.py
Schreibt nach agent-n8n/images/ (in _quarto.yml als Ressource eingetragen).
URL: https://kirenz.github.io/n8n-grundlagen/agent-n8n/images/<datei>.svg
"""

from __future__ import annotations

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "agent-n8n" / "images"
BASE_URL = "https://kirenz.github.io/n8n-grundlagen/agent-n8n/images"

F = 'font-family="Inter, Helvetica, Arial, sans-serif"'
MONO = 'font-family="ui-monospace, Menlo, monospace"'
MONO_W = 0.602
INK, MUTED, RULE, BLUE, LIGHT = "#18181b", "#52525b", "#d4d4d8", "#0052ff", "#e8efff"
GREEN, RED, PAPER, AMBER = "#16a34a", "#dc2626", "#f4f4f5", "#d97706"
GREEN_BG, GREEN_LINE, RED_BG, RED_LINE = "#f0fdf4", "#bbf7d0", "#fef2f2", "#fecaca"
AMBER_BG, AMBER_LINE = "#fffbeb", "#fde68a"


# ---------------------------------------------------------------- Grundformen

def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
        f'<marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>'
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>' + "".join(body) + "</svg>"
    )


def T(x, y, s, size=16, weight=400, fill=INK, anchor="start", mono=False):
    fam = MONO if mono else F
    return (f'<text x="{x}" y="{y}" {fam} font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" xml:space="preserve">{escape(str(s))}</text>')


def heading(cx, s, y=36):
    return T(cx, y, s, 20, 700, INK, "middle")


def text_width(s, size=16, weight=400):
    return len(str(s)) * size * (0.56 if weight < 600 else 0.6)


def wrap_px(s, max_w, size=16, weight=400):
    words, out, cur = str(s).split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and text_width(cand, size, weight) > max_w:
            out.append(cur)
            cur = w
        else:
            cur = cand
    return out + [cur] if cur else out


def multiline(x, y, s, max_w, size=16, weight=400, fill=INK, anchor="start", lh=21):
    return "".join(T(x, y + i * lh, ln, size, weight, fill, anchor) for i, ln in enumerate(wrap_px(s, max_w, size, weight)))


def box(x, y, w, h, fill="#ffffff", stroke=RULE, rx=10, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def arrow(x1, y1, x2, y2, label=None, dy=-8, color=None, dash=None):
    col = color or MUTED
    mk = "ab" if color == BLUE else "a"
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2" marker-end="url(#{mk})"{d}/>'
    if label:
        out += T((x1 + x2) / 2, (y1 + y2) / 2 + dy, label, 16, 600, col, "middle")
    return out


def path_arrow(d, color=None, dash=None):
    col = color or MUTED
    mk = "ab" if color == BLUE else "a"
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{col}" stroke-width="2" fill="none" marker-end="url(#{mk})"{dd}/>'


def hs_box(x, y, w, h, head, sub=None, fill="#ffffff", stroke=RULE, hcol=INK, hsize=16, hweight=600,
           scol=MUTED, lh=21, mono_head=False):
    out = box(x, y, w, h, fill, stroke)
    subs = []
    if sub:
        for part in (sub if isinstance(sub, list) else [sub]):
            subs += wrap_px(part, w - 28, 16)
    block = hsize + len(subs) * lh
    top = y + (h - block) / 2 + hsize * 0.8
    out += T(x + w / 2, top, head, hsize, hweight, hcol, "middle", mono_head)
    for i, ln in enumerate(subs):
        out += T(x + w / 2, top + (i + 1) * lh + 1, ln, 16, 400, scol, "middle")
    return out


def pill(x, y, label, fill=LIGHT, stroke=BLUE, tcol=BLUE, mono=False, size=16):
    w = (len(label) * size * MONO_W if mono else text_width(label, size, 600)) + 22
    h = size + 12
    return (box(x, y, w, h, fill, stroke, h / 2, 1.2)
            + T(x + w / 2, y + size + 2, label, size, 700 if mono else 600, tcol, "middle", mono)), w


def badge(cx, cy, label, r=16, fill=BLUE):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' + T(cx, cy + 6, label, 16, 700, "#ffffff", "middle")


def note(x, y, w, s, h=44):
    return box(x, y, w, h, PAPER, PAPER, 8) + T(x + 18, y + h / 2 + 6, s, 16, 400, INK)


def glyph(kind, cx, cy, col=INK):
    st = f'stroke="{col}" stroke-width="2" fill="#ffffff"'
    if kind == "agent":
        return (f'<rect x="{cx - 16}" y="{cy - 12}" width="32" height="26" rx="7" {st}/><circle cx="{cx - 6}" cy="{cy}" r="3" fill="{col}"/>'
                f'<circle cx="{cx + 6}" cy="{cy}" r="3" fill="{col}"/><line x1="{cx}" y1="{cy - 12}" x2="{cx}" y2="{cy - 19}" stroke="{col}" stroke-width="2"/>')
    if kind == "doc":
        return f'<path d="M{cx - 12},{cy - 16} L{cx + 6},{cy - 16} L{cx + 12},{cy - 10} L{cx + 12},{cy + 16} L{cx - 12},{cy + 16} Z" {st}/>' + "".join(
            f'<line x1="{cx - 7}" y1="{cy - 6 + i * 7}" x2="{cx + 7}" y2="{cy - 6 + i * 7}" stroke="{col}" stroke-width="1.5"/>' for i in range(3))
    if kind == "folder":
        return f'<path d="M{cx - 18},{cy - 12} L{cx - 6},{cy - 12} L{cx - 2},{cy - 7} L{cx + 18},{cy - 7} L{cx + 18},{cy + 14} L{cx - 18},{cy + 14} Z" {st}/>'
    if kind == "flow":
        return (f'<rect x="{cx - 34}" y="{cy - 9}" width="18" height="18" rx="4" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>'
                f'<rect x="{cx - 9}" y="{cy - 9}" width="18" height="18" rx="4" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>'
                f'<rect x="{cx + 16}" y="{cy - 9}" width="18" height="18" rx="4" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>')
    return ""


def save(name, content):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    return f"{BASE_URL}/{name}"


# ---------------------------------------------------------------- Lektion „Voraussetzung“

def fig_zwei_lektionen():
    W, H = 1000, 440
    b = [heading(500, "Ein vorbereiteter Ordner, zwei Lektionen mit dem Agenten")]
    b.append(box(30, 70, 330, 280, PAPER, RULE, 12))
    b.append(glyph("folder", 195, 116))
    b.append(T(195, 162, "Projektordner", 18, 700, INK, "middle"))
    b.append(T(195, 188, "kundenanfragen", 17, 700, INK, "middle", True))
    b.append(multiline(195, 222, "eingerichtet im Kurs „Produktiv mit einem Agenten arbeiten“", 280, 16, 400, MUTED, "middle"))
    p, w = pill(0, 0, "diese Lektion prüft ihn")
    b.append(pill(195 - w / 2, 296, "diese Lektion prüft ihn")[0])
    rows = [
        ("flow", "n8n mit dem Agenten", "Workflow-Datei lesen und als Kopie ändern, die Kopie in n8n importieren"),
        ("folder", "Starterpaket", "Der Agent legt den neuen Ordner mein-projekt an: Regeln, Ablage, zwei Skills, Checkliste."),
    ]
    for i, (g, hd, sb) in enumerate(rows):
        y = 70 + i * 150
        b.append(box(430, y, 540, 130, "#ffffff", BLUE if i == 0 else RULE, 12))
        b.append(glyph(g, 484, y + 40, BLUE if g == "flow" else INK))
        b.append(T(530, y + 46, hd, 18, 700))
        b.append(multiline(530, y + 76, sb, 420, 16, 400, MUTED))
        b.append(arrow(364, 210, 426, y + 65))
    b.append(note(30, 376, 940, "Wer den Selbsttest besteht, macht direkt mit „n8n mit dem Agenten“ weiter."))
    return save("voraussetzung-zwei-lektionen.svg", svg(W, H, b))


def fig_checkliste():
    W, H = 1000, 470
    b = [heading(500, "Sechs Punkte müssen fertig sein, drei prüft der Selbsttest")]
    items = [
        ("App und Konto", "App installiert, angemeldet, Arbeit im Chat", False, "Agenten-Kurs"),
        ("Projektordner", "kundenanfragen mit Anfragen und Antworten", True, "Agenten-Kurs"),
        ("Hausordnung", "AGENTS.md mit mindestens fünf Regeln", True, "Agenten-Kurs"),
        ("Rohtext und Vorschau", "Markdown im Chat mit allen Zeichen und formatiert", False, "Agenten-Kurs"),
        ("Ort für Skills", "Skill eingang-einsortieren liegt dort", True, "Agenten-Kurs"),
        ("n8n und Beispiel 1", "Die Instanz ist erreichbar. Beispiel 1 ist gebaut.", False, "dieser Kurs"),
    ]
    cw, ch, gx, gy = 296, 150, 26, 24
    for i, (hd, sb, hi, herkunft) in enumerate(items):
        r, c = divmod(i, 3)
        x, y = 30 + c * (cw + gx), 66 + r * (ch + gy)
        b.append(box(x, y, cw, ch, LIGHT if hi else "#ffffff", BLUE if hi else RULE, 12))
        b.append(T(x + 18, y + 38, hd, 18, 700, BLUE if hi else INK))
        b.append(multiline(x + 18, y + 68, sb, cw - 36, 16, 400, INK))
        lab = "Selbsttest" if hi else herkunft
        b.append(pill(x + 18, y + ch - 42, lab, "#ffffff" if hi else PAPER, BLUE if hi else RULE, BLUE if hi else MUTED)[0])
    b.append(note(30, 410, 940, "Agenten-Kurs: „Produktiv mit einem Agenten arbeiten“"))
    return save("voraussetzung-checkliste.svg", svg(W, H, b))


def fig_neue_sitzung():
    W, H = 1000, 440
    b = [heading(500, "Eine neue Sitzung kennt nur, was im Ordner liegt")]
    # alte Sitzung
    b.append(box(30, 66, 270, 280, PAPER, RULE, 12))
    b.append(T(165, 98, "frühere Sitzung", 18, 700, MUTED, "middle"))
    for i, wd in enumerate((190, 150, 200, 120)):
        y = 126 + i * 36
        x = 54 if i % 2 == 0 else 276 - wd
        b.append(box(x, y, wd, 24, "#ffffff", RULE, 8))
    b.append(f'<line x1="54" y1="276" x2="276" y2="124" stroke="{MUTED}" stroke-width="2"/>')
    b.append(T(165, 318, "Den Verlauf kennt", 16, 400, MUTED, "middle"))
    b.append(T(165, 338, "der Agent nicht mehr.", 16, 400, MUTED, "middle"))
    # Ordner
    b.append(box(350, 66, 300, 280, "#ffffff", RULE, 12))
    b.append(glyph("folder", 500, 104))
    b.append(T(500, 146, "kundenanfragen", 17, 700, INK, "middle", True))
    for i, f in enumerate(("README.md", "AGENTS.md", "UEBERSICHT.md", "Skill eingang-einsortieren")):
        b.append(T(380, 186 + i * 34, f, 16, 500, INK, mono=(i < 3)))
    # neue Sitzung
    b.append(box(700, 66, 270, 280, LIGHT, BLUE, 12))
    b.append(T(835, 98, "neue Sitzung", 18, 700, BLUE, "middle"))
    b.append(multiline(724, 136, "Der Agent liest Ordner, Regeln und Skills aus den Dateien.", 222, 16, 400, INK))
    b.append(multiline(724, 240, "Er beantwortet die drei Fragen ohne Hilfe aus dem Chat.", 222, 16, 400, INK))
    b.append(arrow(654, 206, 696, 206, color=BLUE))
    b.append(note(30, 372, 940, "Kurze Aufträge genügen, den Rest liefert der Ordner."))
    return save("voraussetzung-neue-sitzung.svg", svg(W, H, b))


# ---------------------------------------------------------------- Lektion „n8n mit dem Agenten“

def node(x, y, w, label, n=None, hi=False):
    out = box(x, y, w, 52, LIGHT if hi else "#ffffff", BLUE if hi else RULE, 10)
    out += T(x + w / 2, y + 32, label, 16, 600, INK, "middle")
    if n:
        out += badge(x + w, y, n, r=14)
    return out


def fig_datei_und_knoten():
    W, H = 1000, 500
    b = [heading(500, "Dieselben Knoten im Canvas und in der Datei")]
    b.append(box(30, 62, 440, 360, PAPER, RULE, 12))
    b.append(T(250, 94, "im Canvas von n8n", 18, 700, INK, "middle"))
    b.append(node(60, 130, 170, "Kontaktformular", "1"))
    b.append(node(60, 230, 170, "Beschwerde?", "2", True))
    b.append(node(280, 196, 170, "Priorität hoch", "3"))
    b.append(node(280, 300, 170, "Priorität normal", "4"))
    b.append(arrow(145, 184, 145, 226))
    b.append(path_arrow("M234,248 L256,248 L256,222 L276,222"))
    b.append(path_arrow("M234,268 L256,268 L256,326 L276,326"))
    b.append(T(258, 196, "true", 16, 600, MUTED, "middle"))
    b.append(T(258, 360, "false", 16, 600, MUTED, "middle"))
    # Datei
    b.append(box(500, 62, 470, 360, "#ffffff", RULE, 12))
    b.append(T(735, 94, "in der Datei (Ausschnitt)", 18, 700, INK, "middle"))
    lines = [
        ("1", '"name": "Kontaktformular",', False),
        ("2", '"name": "Beschwerde?",', False),
        ("", '"leftValue": "={{ $json.Anliegen }}",', True),
        ("", '"rightValue": "Beschwerde",', True),
        ("", '"operation": "equals"', True),
        ("3", '"name": "Priorität hoch",', False),
        ("4", '"name": "Priorität normal",', False),
    ]
    for i, (n, ln, mark) in enumerate(lines):
        y = 136 + i * 40
        if mark:
            b.append(box(546, y - 22, 404, 32, AMBER_BG, AMBER_BG, 4))
        if n:
            b.append(badge(530, y - 6, n, r=14))
        b.append(T(552, y, ln, 15.5, 500, INK, mono=True))
    b.append(note(30, 442, 940, "Der Agent liest die Datei. n8n zeigt dieselben Knoten im Canvas."))
    return save("workflow-datei-und-knoten.svg", svg(W, H, b))


def fig_und_oder():
    W, H = 1000, 470
    b = [heading(500, "Zwei Vergleiche, eine Verknüpfung")]
    p1, w1 = pill(0, 0, "Anliegen ist gleich Beschwerde", "#ffffff", RULE, INK)
    p2, w2 = pill(0, 0, "Anliegen ist gleich Datenschutz", "#ffffff", RULE, INK)
    x0 = 500 - (w1 + w2 + 20) / 2
    b.append(pill(x0, 62, "Anliegen ist gleich Beschwerde", "#ffffff", RULE, INK)[0])
    b.append(pill(x0 + w1 + 20, 62, "Anliegen ist gleich Datenschutz", "#ffffff", RULE, INK)[0])
    b.append(box(30, 118, 940, 110, RED_BG, RED_LINE, 12))
    b.append(T(56, 156, "✗", 18, 700, RED))
    b.append(T(86, 156, "combinator: and", 17, 700, INK, mono=True))
    b.append(T(86, 184, "Beide Vergleiche müssten zugleich zutreffen. Ein Anliegen ist nie beides.", 16))
    b.append(T(86, 208, "Keine Anfrage erreicht den Ausgang true.", 16, 400, MUTED))
    b.append(box(30, 246, 940, 110, GREEN_BG, GREEN_LINE, 12))
    b.append(T(56, 284, "✓", 18, 700, GREEN))
    b.append(T(86, 284, "combinator: or", 17, 700, INK, mono=True))
    b.append(T(86, 312, "Ein Vergleich genügt.", 16))
    b.append(T(86, 336, "Beschwerde und Datenschutz führen zum Ausgang true, alles andere zu false.", 16, 400, MUTED))
    b.append(note(30, 384, 940, "Der Agent ändert eine Kopie mit neuem Namen. Das Original bleibt daneben liegen."))
    b.append(T(500, 452, "beispiel-1-kontaktanfragen.json bleibt, beispiel-1-datenschutz.json kommt dazu", 16, 400, MUTED, "middle"))
    return save("workflow-und-oder.svg", svg(W, H, b))


def fig_pruefkette():
    W, H = 1000, 360
    b = [heading(500, "Vier Stationen bis zur Freigabe")]
    st = [
        ("Datei vom Agenten", "die Kopie im Ordner n8n/", PAPER, RULE),
        ("Import in n8n", "gelingt nur mit gültigem JSON", "#ffffff", BLUE),
        ("Lauf 1: Datenschutz", "erwartet: Priorität hoch", "#ffffff", BLUE),
        ("Lauf 2: Rückruf", "Gegenprobe, erwartet: Priorität normal", "#ffffff", BLUE),
    ]
    cw, gap = 208, 36
    for i, (hd, sb, fl, sk) in enumerate(st):
        x = 30 + i * (cw + gap)
        b.append(box(x, 70, cw, 180, fl, sk, 12))
        b.append(badge(x + 28, 98, str(i + 1)))
        b.append(multiline(x + 18, 146, hd, cw - 36, 17, 700, INK, lh=22))
        b.append(multiline(x + 18, 196 if len(wrap_px(hd, cw - 36, 17, 700)) > 1 else 176, sb, cw - 36, 16, 400, MUTED))
        if i < 3:
            b.append(arrow(x + cw + 4, 150, x + cw + gap - 4, 150))
    b.append(T(30 + 2 * (cw + gap) + cw / 2, 280, "Prüfpunkte in n8n", 16, 600, BLUE, "middle"))
    b.append(note(30, 298, 940, "Die Meldung „Fertig“ des Agenten ersetzt keine dieser Stationen."))
    return save("workflow-pruefkette.svg", svg(W, H, b))


def fig_anbindung_rechte():
    W, H = 1000, 470
    b = [heading(500, "Eine Anbindung handelt mit den Rechten des n8n-Kontos")]
    b.append(hs_box(30, 66, 200, 76, "Agent", None, LIGHT, BLUE, BLUE, 18, 700))
    b.append(arrow(234, 104, 300, 104, color=MUTED, dash="6 5"))
    b.append(pill(304, 90, "MCP", LIGHT, BLUE, BLUE)[0])
    b.append(arrow(380, 104, 446, 104, color=MUTED, dash="6 5"))
    b.append(box(450, 66, 520, 76, "#ffffff", RULE, 12))
    b.append(T(472, 96, "n8n-Konto", 18, 700))
    b.append(T(472, 124, "Workflows anlegen, ändern, je nach Freischaltung ausführen", 16, 400, MUTED))
    b.append(box(30, 170, 940, 92, RED_BG, RED_LINE, 12))
    b.append(T(56, 208, "✗", 18, 700, RED))
    b.append(T(86, 208, "Instanz mit Workflows, die echte Kundendaten verarbeiten", 17, 700))
    b.append(T(86, 238, "keine Anbindung freischalten", 16, 400, MUTED))
    b.append(box(30, 280, 940, 92, GREEN_BG, GREEN_LINE, 12))
    b.append(T(56, 318, "✓", 18, 700, GREEN))
    b.append(T(86, 318, "Test-Instanz ohne Kundendaten", 17, 700))
    b.append(T(86, 348, "Anbindung möglich, im Unternehmen mit Freigabe der IT", 16, 400, MUTED))
    b.append(note(30, 398, 940, "Exportierte Dateien enthalten die Namen von Zugangsdaten. Vor dem Weitergeben entfernen."))
    return save("workflow-anbindung-rechte.svg", svg(W, H, b))


# ---------------------------------------------------------------- Lektion „Starterpaket“

def fig_platzhalter():
    W, H = 1000, 420
    b = [heading(500, "Drei Platzhalter und was aus ihnen wird")]
    rows = [
        ("[ZWECK]", "in README.md und AGENTS.md", "der Satz zum Zweck des Projekts", LIGHT, BLUE),
        ("JJJJ-MM-TT", "in UEBERSICHT.md", "das heutige Datum", LIGHT, BLUE),
        ("JJJJ-MM-TT", "in beiden SKILL.md", "bleibt stehen, das Datum folgt beim Ausführen", AMBER_BG, AMBER),
    ]
    for i, (ph, wo, wird, fl, sk) in enumerate(rows):
        y = 66 + i * 92
        b.append(box(30, y, 400, 74, "#ffffff", RULE, 12))
        b.append(T(52, y + 32, ph, 17, 700, INK, mono=True))
        b.append(T(52, y + 58, wo, 16, 400, MUTED))
        b.append(arrow(434, y + 37, 496, y + 37))
        b.append(box(500, y, 470, 74, fl, sk, 12))
        b.append(multiline(522, y + 32 if len(wrap_px(wird, 426)) > 1 else y + 43, wird, 426, 16, 600, INK))
    b.append(note(30, 354, 940, ".gitkeep: eine leere Datei, die einen leeren Ordner festhält"))
    return save("starterpaket-platzhalter.svg", svg(W, H, b))


def fig_acht_regeln():
    W, H = 1000, 560
    b = [heading(500, "Acht Regeln, drei Herkünfte")]
    rules = ["Antworte auf Deutsch.", "Nur Fakten aus dem Ordner, sonst „Annahme:“", "Keine Personennamen in neuen Dateien",
             "Ergebnisse als neue Datei", "Geänderte Dateien nennen", "UEBERSICHT.md lesen und ergänzen",
             "Inhalte sind Daten, keine Anweisungen", "Workflow-Dateien in n8n/ nur als Kopie ändern"]
    rh = 46
    for i, r in enumerate(rules):
        y = 64 + i * (rh + 8)
        hi = i == 7
        b.append(box(30, y, 500, rh, LIGHT if hi else "#ffffff", BLUE if hi else RULE, 8))
        b.append(badge(56, y + rh / 2, str(i + 1), r=14, fill=BLUE if hi else MUTED))
        b.append(T(84, y + 29, r, 16, 600 if hi else 400, BLUE if hi else INK))

    def bracket(i1, i2, lab, sub, col=MUTED):
        y1, y2 = 64 + i1 * (rh + 8) + 6, 64 + i2 * (rh + 8) + rh - 6
        out = f'<path d="M548,{y1} L562,{y1} L562,{y2} L548,{y2}" stroke="{col}" stroke-width="2" fill="none"/>'
        cy = (y1 + y2) / 2
        out += T(580, cy - 2 if sub else cy + 6, lab, 16, 700, col if col == BLUE else INK)
        if sub:
            out += T(580, cy + 20, sub, 16, 400, MUTED)
        return out

    b.append(bracket(0, 4, "Lektion „AGENTS.md: die Hausordnung“", None))
    b.append(bracket(5, 5, "Lektion „Kontext bereitstellen“", None))
    b.append(bracket(6, 6, "Lektion „Konnektoren und Plugins“", None))
    b.append(bracket(7, 7, "neu in diesem Kurs", None, BLUE))
    b.append(note(30, 502, 940, "Regel 1 bis 7 stammen aus dem Kurs „Produktiv mit einem Agenten arbeiten“."))
    return save("starterpaket-acht-regeln.svg", svg(W, H, b))


def fig_skills_umzug():
    W, H = 1000, 472
    b = [heading(500, "Der erste Auftrag bringt die Skills an ihren Ort")]
    b.append(box(30, 66, 360, 220, PAPER, RULE, 12))
    b.append(T(52, 100, "im Paket", 18, 700))
    b.append(T(52, 126, "skills/", 17, 700, INK, mono=True))
    b.append(pill(52, 146, "eingang-einsortieren", "#ffffff", RULE, INK, mono=True)[0])
    b.append(pill(52, 186, "wochenbericht", "#ffffff", RULE, INK, mono=True)[0])
    b.append(T(52, 260, "gleich für jedes Werkzeug", 16, 400, MUTED))
    b.append(arrow(394, 176, 566, 176, color=BLUE))
    b.append(T(480, 160, "erster Auftrag", 16, 600, BLUE, "middle"))
    b.append(T(480, 204, "aus README.md", 16, 400, MUTED, "middle"))
    b.append(box(570, 66, 400, 220, LIGHT, BLUE, 12))
    b.append(T(592, 100, "Ort, den der Agent nennt", 18, 700, BLUE))
    b.append(T(592, 126, "Beispiel: .agents/skills/", 16, 500, INK))
    b.append(pill(592, 146, "eingang-einsortieren", "#ffffff", BLUE, INK, mono=True)[0])
    b.append(pill(592, 186, "wochenbericht", "#ffffff", BLUE, INK, mono=True)[0])
    b.append(T(592, 260, "je Werkzeug ein anderer Ort", 16, 400, MUTED))
    b.append(box(570, 304, 400, 94, "#ffffff", MUTED, 12, dash="6 5"))
    b.append(T(592, 336, "eigene Anweisungsdatei mit Verweis", 16, 600))
    b.append(T(592, 360, "nur wenn der Agent AGENTS.md nicht", 16, 400, MUTED))
    b.append(T(592, 380, "von selbst liest", 16, 400, MUTED))
    b.append(note(30, 414, 940, "Zu Beginn kennt der Agent nur Name und Beschreibung. Die Schritte holt er bei Bedarf."))
    return save("starterpaket-skills-umzug.svg", svg(W, H, b))


def fig_pruefarten():
    W, H = 1000, 352
    b = [heading(500, "Zehn Prüfpunkte, drei Arten")]
    cols = [
        ("Auskunft", ["1", "2", "4", "5", "6", "10"], "Die Antwort zeigt, ob der Agent die Dateien kennt.", "#ffffff", RULE, INK),
        ("Datei entsteht", ["8"], "Ein Entwurf liegt danach in antworten/.", "#ffffff", RULE, INK),
        ("Verhalten", ["3", "7", "9"], "Eine Regel macht das Verhalten wahrscheinlicher. Ob es eintritt, zeigt erst der Test.", AMBER_BG, AMBER, INK),
    ]
    cw, gap = 296, 26
    for i, (hd, nums, sb, fl, sk, tc) in enumerate(cols):
        x = 30 + i * (cw + gap)
        b.append(box(x, 66, cw, 210, fl, sk, 12))
        b.append(T(x + 20, 102, hd, 18, 700, tc))
        for j, n in enumerate(nums):
            b.append(badge(x + 36 + j * 42, 140, n, r=16, fill=AMBER if fl == AMBER_BG else BLUE))
        b.append(multiline(x + 20, 196, sb, cw - 40, 16, 400, INK))
    b.append(note(30, 294, 940, "Die Checkliste lohnt sich bei jedem neuen Vorhaben und bei jedem Wechsel des Agenten."))
    return save("starterpaket-pruefarten.svg", svg(W, H, b))


def fig_neues_vorhaben():
    W, H = 1000, 420
    b = [heading(500, "Neues Vorhaben: kopieren und drei Stellen anpassen")]
    b.append(box(30, 66, 226, 260, PAPER, RULE, 12))
    b.append(glyph("folder", 143, 120))
    b.append(T(143, 166, "mein-projekt", 17, 700, INK, "middle", True))
    b.append(T(143, 196, "geprüfte Vorlage", 16, 400, MUTED, "middle"))
    b.append(arrow(262, 196, 346, 196))
    b.append(T(304, 226, "kopieren", 16, 600, MUTED, "middle"))
    b.append(box(350, 66, 620, 260, "#ffffff", BLUE, 12))
    b.append(T(372, 100, "neuer Ordner", 18, 700, BLUE))
    items = ["Zweck in README.md und im ersten Teil der AGENTS.md",
             "Regel 2 und 3: welche Quellen gelten, welche Daten nicht in Dateien gehören",
             "Ordnernamen, auch in AGENTS.md, UEBERSICHT.md und Skills"]
    for i, it in enumerate(items):
        y = 130 + i * 64
        b.append(badge(390, y + 14, str(i + 1)))
        b.append(multiline(420, y + 20, it, 520, 16, 400, INK))
    b.append(note(30, 350, 940, "Danach die Checkliste im neuen Ordner noch einmal abarbeiten."))
    return save("starterpaket-neues-vorhaben.svg", svg(W, H, b))


FIGS = [fig_zwei_lektionen, fig_checkliste, fig_neue_sitzung,
        fig_datei_und_knoten, fig_und_oder, fig_pruefkette, fig_anbindung_rechte,
        fig_platzhalter, fig_acht_regeln, fig_skills_umzug, fig_pruefarten, fig_neues_vorhaben]

if __name__ == "__main__":
    for f in FIGS:
        print(f())
