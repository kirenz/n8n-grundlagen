"""Abbildungen für den Teil „Plattform und Auswahl“ (SVG, ohne Abhängigkeiten).

Aufruf: python3 scripts/build_overview_figures.py
Schreibt nach images/lektionen/. Zahlen stammen aus overview/pricing.qmd und
overview/hosting.qmd (Größenordnungen, Tarife ändern sich).
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images" / "lektionen"
F = 'font-family="Inter, Helvetica, Arial, sans-serif"'
INK, MUTED, RULE, BLUE, LIGHT = "#18181b", "#52525b", "#d4d4d8", "#0052ff", "#e8efff"
GREEN, RED, PAPER = "#16a34a", "#dc2626", "#f4f4f5"


def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>'
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>' + "".join(body) + "</svg>"
    )


def text(x, y, s, size=14, weight=400, fill=INK, anchor="start"):
    return f'<text x="{x}" y="{y}" {F} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


def box(x, y, w, h, fill="#ffffff", stroke=RULE, rx=10, sw=1.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arrow(x1, y1, x2, y2, label=None, dy=-8, dx=0):
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>'
    if label:
        out += text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, label, 13, 600, MUTED, "middle")
    return out


def card(x, y, w, h, title, sub=None, fill="#ffffff", stroke=RULE, tcol=INK):
    out = box(x, y, w, h, fill, stroke)
    out += text(x + w / 2, y + (h / 2 if not sub else h / 2 - 6), title, 15, 600, tcol, "middle")
    if sub:
        out += text(x + w / 2, y + h / 2 + 14, sub, 12, 400, MUTED if tcol == INK else tcol, "middle")
    return out


def schicht():
    """n8n als Schicht zwischen vorhandenen Werkzeugen (Kontaktformular-Fall)."""
    b = [text(450, 34, "n8n verbindet vorhandene Werkzeuge, statt sie zu ersetzen", 17, 700, INK, "middle")]
    b.append(card(30, 150, 170, 70, "Kontaktformular", "neue Nachricht"))
    b.append(box(270, 70, 360, 240, LIGHT, BLUE, 14, 2))
    b.append(text(450, 100, "n8n-Workflow", 16, 700, BLUE, "middle"))
    steps = [("1", "Eingang erkennen", "Trigger"), ("2", "Bestätigung senden", "Knoten"), ("3", "Zeile eintragen", "Knoten")]
    for i, (n, t, k) in enumerate(steps):
        y = 120 + i * 60
        b.append(box(295, y, 310, 46, "#ffffff", RULE, 8))
        b.append(f'<circle cx="320" cy="{y + 23}" r="12" fill="{BLUE}"/>')
        b.append(text(320, y + 28, n, 13, 700, "#ffffff", "middle"))
        b.append(text(342, y + 28, t, 14, 600))
        b.append(text(590, y + 28, k, 12, 400, MUTED, "end"))
    b.append(arrow(200, 185, 268, 185))
    b.append(card(700, 110, 170, 60, "Postfach", "Bestätigung an Absender"))
    b.append(card(700, 210, 170, 60, "Tabelle", "neue Zeile"))
    b.append(arrow(632, 165, 698, 140))
    b.append(arrow(632, 225, 698, 240))
    b.append(text(450, 345, "Kein eigenes Entwicklungsprojekt: Die drei Schritte werden im Editor zusammengeklickt.", 13, 400, MUTED, "middle"))
    return svg(900, 370, b)


def daten_ki():
    """Rechnung → n8n → KI-Dienst → n8n → Ablage."""
    b = [text(450, 30, "Zwei Kernaufgaben in einem Workflow: Daten bewegen und KI nutzen", 17, 700, INK, "middle")]
    b.append(card(225, 50, 190, 60, "KI-Dienst", "z. B. OpenAI, Anthropic"))
    b.append(card(20, 185, 150, 70, "Rechnung (PDF)", "per Mail"))
    b.append(box(220, 160, 200, 120, LIGHT, BLUE, 14, 2))
    b.append(text(320, 195, "n8n", 18, 700, BLUE, "middle"))
    b.append(text(320, 222, "liest Betrag, Absender", 12, 400, INK, "middle"))
    b.append(text(320, 240, "und Text der Rechnung", 12, 400, INK, "middle"))
    b.append(arrow(170, 220, 218, 220))
    b.append(arrow(285, 158, 285, 112))
    b.append(text(275, 140, "Text", 12, 600, MUTED, "end"))
    b.append(arrow(355, 112, 355, 158))
    b.append(text(365, 140, "Kategorie: Büromaterial", 12, 600, BLUE))
    b.append(card(710, 185, 170, 70, "Ablage", "Ordner Büromaterial"))
    b.append(arrow(420, 220, 708, 220, "in passenden Ordner ablegen", -10))
    b.append(box(20, 300, 860, 46, PAPER, PAPER, 8))
    b.append(text(40, 328, "Daten bewegen: über 500 fertige Integrationen.  KI nutzen: KI-Bausteine sind Teil des Editors.", 13, 400, INK))
    return svg(900, 360, b)


def ist_nicht():
    b = [text(450, 34, "Was n8n ist und was nicht", 17, 700, INK, "middle")]
    left = ["verbindet Werkzeuge zu einem Ablauf", "steuert die Reihenfolge der Schritte", "bindet KI-Dienste als Baustein ein", "protokolliert jeden Durchlauf"]
    right = ["kein vollwertiger Code-Editor", "kein Daten-Warehouse (Datenlager)", "kein eigenes KI-Modell", "kein Ersatz für CRM oder Buchhaltung"]
    b.append(box(30, 60, 410, 230, "#f0fdf4", "#bbf7d0", 12))
    b.append(box(460, 60, 410, 230, "#fef2f2", "#fecaca", 12))
    b.append(text(235, 92, "n8n ist die Orchestrierung", 15, 700, GREEN, "middle"))
    b.append(text(665, 92, "n8n ist nicht", 15, 700, RED, "middle"))
    for i, (l, r) in enumerate(zip(left, right)):
        y = 135 + i * 40
        b.append(text(55, y, "✓", 16, 700, GREEN))
        b.append(text(80, y, l, 14))
        b.append(text(485, y, "✗", 16, 700, RED))
        b.append(text(510, y, r, 14))
    return svg(900, 310, b)


def vorher_nachher():
    b = [text(450, 34, "Was sich für das Team ändert", 17, 700, INK, "middle")]
    rows = [("Eingang bemerken", "jemand prüft irgendwann das Postfach", "Trigger erkennt jede Nachricht sofort"),
            ("Bestätigung", "wird von Hand getippt", "geht automatisch raus"),
            ("Tabelle", "Eintrag von Hand übertragen", "Zeile entsteht automatisch"),
            ("Ergebnis", "abhängig von Tagesform", "bei jeder Nachricht gleich")]
    b.append(text(250, 72, "Von Hand", 15, 700, MUTED, "middle"))
    b.append(text(650, 72, "Mit n8n", 15, 700, BLUE, "middle"))
    for i, (k, v, n) in enumerate(rows):
        y = 90 + i * 56
        b.append(text(30, y + 32, k, 13, 600, MUTED))
        b.append(box(150, y + 8, 320, 40, PAPER, PAPER, 8))
        b.append(text(165, y + 33, v, 13))
        b.append(box(500, y + 8, 370, 40, LIGHT, LIGHT, 8))
        b.append(text(515, y + 33, n, 13, 600, INK))
    return svg(900, 330, b)


def rechnungseinheit():
    """Ein Durchlauf mit 50 Schritten: 50 Tasks oder 1 Execution."""
    b = [text(450, 34, "Derselbe Durchlauf mit 50 Schritten, zwei Rechnungen", 17, 700, INK, "middle")]
    b.append(text(30, 80, "Zapier oder Make: jeder Schritt zählt", 15, 700))
    for i in range(50):
        x = 30 + (i % 25) * 26
        y = 95 + (i // 25) * 26
        b.append(f'<rect x="{x}" y="{y}" width="20" height="20" rx="4" fill="{RED}" opacity="0.8"/>')
    b.append(text(700, 125, "= 50 Tasks", 22, 700, RED))
    b.append(text(30, 205, "n8n: der ganze Durchlauf zählt einmal", 15, 700))
    for i in range(50):
        x = 30 + (i % 25) * 26
        y = 220 + (i // 25) * 26
        b.append(f'<rect x="{x}" y="{y}" width="20" height="20" rx="4" fill="{BLUE}" opacity="0.25"/>')
    b.append(f'<rect x="24" y="214" width="656" height="58" rx="8" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    b.append(text(700, 250, "= 1 Execution", 22, 700, BLUE))
    return svg(900, 300, b)


def kontingent():
    """Verbrauch eines Monats gegen das Kontingent des Einstiegstarifs."""
    b = [text(450, 30, "100 Durchläufe im Monat: Verbrauch im Verhältnis zum Einstiegstarif", 16, 700, INK, "middle")]
    b.append(text(450, 52, "Zapier ab ca. 73 € für 750 Tasks · Make ab ca. 16 € für 10.000 Operations · n8n Cloud ab ca. 24 € für 2.500 Executions", 12, 400, MUTED, "middle"))
    groups = [("Workflow mit 5 Schritten", [("Zapier", 500, 750), ("Make", 500, 10000), ("n8n", 100, 2500)]),
              ("Workflow mit 50 Schritten", [("Zapier", 5000, 750), ("Make", 5000, 10000), ("n8n", 100, 2500)])]
    x0, bw, maxpct = 200, 560, 200
    y = 85
    for title, rows in groups:
        b.append(text(30, y + 18, title, 14, 700))
        y += 30
        for name, used, quota in rows:
            pct = used / quota * 100
            w = min(pct, maxpct) / maxpct * bw
            col = RED if pct > 100 else (BLUE if name == "n8n" else MUTED)
            b.append(text(30, y + 17, name, 13))
            b.append(box(x0, y + 2, bw, 20, PAPER, PAPER, 4))
            b.append(f'<rect x="{x0}" y="{y + 2}" width="{max(w, 3):.1f}" height="20" rx="4" fill="{col}"/>')
            label = f"{used:,} von {quota:,}".replace(",", ".") + (f" ({pct:.0f} %)" if pct < 1000 else "")
            if pct > maxpct:
                label = f"{used:,} von {quota:,}".replace(",", ".") + f" (das {used / quota:.1f}-Fache)".replace(".", ",", 1)
            b.append(text(x0 + bw + 10, y + 17, label, 12, 600, col if pct > 100 else INK))
            y += 30
        y += 14
    b.append(f'<line x1="{x0 + bw / 2}" y1="105" x2="{x0 + bw / 2}" y2="{y - 10}" stroke="{INK}" stroke-dasharray="4 4"/>')
    b.append(text(x0 + bw / 2, y + 4, "Kontingent des Einstiegstarifs", 11, 400, MUTED, "middle"))
    return svg(1000, y + 20, b)


def zwei_teams():
    b = [text(450, 34, "Dieselbe Software, zwei Ausgangslagen", 17, 700, INK, "middle")]
    teams = [(40, "Arztpraxis", ["verarbeitet Patientendaten", "Daten sollen in der EU bleiben", "niemand für Server-Pflege"]),
             (470, "Marketing-Team", ["keine sensiblen Daten", "will heute Nachmittag starten", "keine eigene IT"])]
    for x, name, pts in teams:
        b.append(box(x, 60, 390, 190, "#ffffff", RULE, 12))
        b.append(text(x + 24, 98, name, 17, 700))
        for i, p in enumerate(pts):
            b.append(f'<circle cx="{x + 30}" cy="{126 + i * 34}" r="4" fill="{BLUE}"/>')
            b.append(text(x + 44, 131 + i * 34, p, 14))
    b.append(text(450, 285, "Welche Betriebsform passt jeweils? Die Antwort steht am Ende der Lektion.", 13, 400, MUTED, "middle"))
    return svg(900, 300, b)


def entscheidung():
    """Entscheidungsbaum für die Betriebsform, mit den beiden Teams aus dem Einstieg."""
    b = [text(450, 30, "Welche Betriebsform passt?", 17, 700, INK, "middle")]

    def q(x, y, s):
        return box(x, y, 260, 56, "#ffffff", INK, 10, 2) + text(x + 130, y + 33, s, 14, 600, INK, "middle")

    def leaf(x, y, s, sub):
        return box(x, y, 190, 60, LIGHT, BLUE, 10, 2) + text(x + 95, y + 26, s, 15, 700, BLUE, "middle") + text(x + 95, y + 46, sub, 11, 400, MUTED, "middle")

    b.append(q(320, 50, "Sensible Daten im eigenen Haus?"))
    b.append(q(90, 170, "IT-Kapazität für Pflege?"))
    b.append(q(550, 170, "Sehr viele Durchläufe und IT?"))
    b.append(arrow(390, 106, 230, 168, "ja", -6, -22))
    b.append(arrow(510, 106, 670, 168, "nein", -6, 26))
    b.append(leaf(10, 300, "Self-Hosted", "volle Kontrolle, eigene Pflege"))
    b.append(leaf(225, 300, "Managed Hosting", "Kontrolle ohne Server-Pflege"))
    b.append(leaf(465, 300, "Self-Hosted", "keine Lizenzkosten"))
    b.append(leaf(690, 300, "Cloud", "Start in Minuten"))
    b.append(arrow(170, 226, 110, 298, "ja", 0, -20))
    b.append(arrow(260, 226, 315, 298, "nein", 0, 26))
    b.append(arrow(640, 226, 565, 298, "ja", 0, -20))
    b.append(arrow(740, 226, 780, 298, "nein", 0, 26))
    for x, s in ((320, "Arztpraxis"), (785, "Marketing-Team")):
        b.append(f'<rect x="{x - 60}" y="372" width="120" height="26" rx="13" fill="{INK}"/>')
        b.append(text(x, 390, s, 12, 600, "#ffffff", "middle"))
    return svg(900, 410, b)


def drei_fragen():
    """Kapitelüberblick: drei Fragen, drei Lektionen."""
    b = [text(450, 32, "Drei Fragen vor dem ersten Workflow", 17, 700, INK, "middle")]
    cards = [("1", "Was leistet n8n?", "und wofür ist es nicht gebaut", "Was n8n leistet"),
             ("2", "Welches Werkzeug?", "n8n, Zapier oder Make", "Werkzeuge im Vergleich"),
             ("3", "Wie betreiben?", "Cloud, Managed oder Self-Hosted", "Betrieb wählen")]
    for i, (n, q, sub, lesson) in enumerate(cards):
        x = 30 + i * 290
        b.append(box(x, 60, 260, 170, "#ffffff", RULE, 12))
        b.append(f'<circle cx="{x + 36}" cy="96" r="18" fill="{BLUE}"/>')
        b.append(text(x + 36, 102, n, 16, 700, "#ffffff", "middle"))
        b.append(text(x + 24, 150, q, 18, 700))
        b.append(text(x + 24, 176, sub, 13, 400, MUTED))
        b.append(box(x + 16, 192, 228, 28, LIGHT, LIGHT, 14))
        b.append(text(x + 130, 211, "Lektion: " + lesson, 12, 600, BLUE, "middle"))
        if i < 2:
            b.append(arrow(x + 262, 145, x + 288, 145))
    b.append(text(450, 262, "Ergebnis: eine begründete Wahl für Werkzeug und Betrieb, bevor gebaut wird.", 13, 400, MUTED, "middle"))
    return svg(900, 280, b)


def glyph(kind, cx, cy):
    """Kleines BPMN-Symbol als Erkennungszeichen."""
    st = f'stroke="{INK}" stroke-width="2" fill="#ffffff"'
    if kind == "grund":
        return (f'<circle cx="{cx - 34}" cy="{cy}" r="9" {st}/><rect x="{cx - 18}" y="{cy - 10}" width="36" height="20" rx="4" {st}/>'
                f'<circle cx="{cx + 34}" cy="{cy}" r="9" stroke="{INK}" stroke-width="4" fill="#ffffff"/>')
    if kind == "gateway":
        return f'<polygon points="{cx},{cy - 14} {cx + 14},{cy} {cx},{cy + 14} {cx - 14},{cy}" {st}/><text x="{cx}" y="{cy + 5}" {F} font-size="13" font-weight="700" text-anchor="middle">X</text>'
    if kind == "ereignis":
        return f'<circle cx="{cx}" cy="{cy}" r="13" {st}/><circle cx="{cx}" cy="{cy}" r="9" {st}/><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 6}" stroke="{INK}" stroke-width="2"/><line x1="{cx}" y1="{cy}" x2="{cx + 5}" y2="{cy}" stroke="{INK}" stroke-width="2"/>'
    if kind == "pool":
        return f'<rect x="{cx - 40}" y="{cy - 15}" width="80" height="30" {st}/><line x1="{cx - 28}" y1="{cy - 15}" x2="{cx - 28}" y2="{cy + 15}" stroke="{INK}" stroke-width="2"/><line x1="{cx - 28}" y1="{cy}" x2="{cx + 40}" y2="{cy}" stroke="{INK}" stroke-width="1.5"/>'
    if kind == "n8n":
        return (f'<rect x="{cx - 40}" y="{cy - 11}" width="22" height="22" rx="5" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>'
                f'<rect x="{cx - 11}" y="{cy - 11}" width="22" height="22" rx="5" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>'
                f'<rect x="{cx + 18}" y="{cy - 11}" width="22" height="22" rx="5" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>')
    if kind == "uebung":
        return f'<rect x="{cx - 14}" y="{cy - 16}" width="28" height="32" rx="3" {st}/>' + "".join(
            f'<line x1="{cx - 8}" y1="{cy - 8 + i * 8}" x2="{cx + 8}" y2="{cy - 8 + i * 8}" stroke="{INK}" stroke-width="1.5"/>' for i in range(3))
    if kind == "key":
        return f'<circle cx="{cx - 12}" cy="{cy}" r="9" {st}/><line x1="{cx - 3}" y1="{cy}" x2="{cx + 22}" y2="{cy}" stroke="{INK}" stroke-width="3"/><line x1="{cx + 16}" y1="{cy}" x2="{cx + 16}" y2="{cy + 8}" stroke="{INK}" stroke-width="3"/>'
    return ""


def lernweg(title, items, cols, note, h_card=150):
    rows = (len(items) + cols - 1) // cols
    cw, gap = (840 - (cols - 1) * 30) / cols, 30
    H = 70 + rows * (h_card + 30) + 30
    b = [text(450, 32, title, 17, 700, INK, "middle")]
    for i, (g, name, sub) in enumerate(items):
        r, c = divmod(i, cols)
        x, y = 30 + c * (cw + gap), 55 + r * (h_card + 30)
        b.append(box(x, y, cw, h_card, "#ffffff", RULE, 12))
        b.append(f'<circle cx="{x + 26}" cy="{y + 26}" r="14" fill="{BLUE}"/>')
        b.append(text(x + 26, y + 31, str(i + 1), 13, 700, "#ffffff", "middle"))
        b.append(glyph(g, x + cw - 60, y + 28))
        b.append(text(x + 18, y + 80, name, 15, 700))
        b.append(text(x + 18, y + 104, sub, 12, 400, MUTED))
        if c < cols - 1 and i < len(items) - 1:
            b.append(arrow(x + cw + 2, y + h_card / 2, x + cw + gap - 2, y + h_card / 2))
    b.append(text(450, H - 14, note, 13, 400, MUTED, "middle"))
    return svg(900, H, b)


def kapitel_bpmn():
    return lernweg("Sechs Lektionen vom Ablauf zum Modell", [
        ("grund", "Grundelemente", "Start, Aufgabe, Ende, gute Namen"),
        ("gateway", "Gateways", "verzweigen und zusammenführen"),
        ("ereignis", "Ereignisse", "warten, Fristen, reagieren"),
        ("pool", "Teilnehmer und Daten", "Pools, Lanes, Datenspeicher"),
        ("n8n", "Vom Modell zum Workflow", "Modell in n8n-Knoten übersetzen"),
        ("uebung", "Übung Kulanzantrag", "vollständiges Modell zeichnen"),
    ], 3, "Jede Lektion baut auf der vorigen auf. Wer BPMN kennt, startet mit der Übung als Selbsttest.", 125)


def kapitel_workflows():
    return lernweg("Zwei Lektionen bis zum laufenden Workflow", [
        ("key", "Credentials vorbereiten", "Zugänge anlegen, getrennt vom Workflow"),
        ("n8n", "Der erste Workflow", "Kundenmail bestätigen und eintragen"),
    ], 2, "Ergebnis: ein getesteter Workflow mit fünf Knoten und eine neue Zeile in customer_emails.", 125)


FIGS = {
    "grundlagen-formularfluss.svg": schicht,
    "grundlagen-daten-und-ki.svg": daten_ki,
    "uebersicht-ist-nicht.svg": ist_nicht,
    "vorher-nachher-team.svg": vorher_nachher,
    "preis-rechnungseinheit.svg": rechnungseinheit,
    "preis-schrittzahl.svg": kontingent,
    "hosting-zwei-teams.svg": zwei_teams,
    "hosting-leitfragen.svg": entscheidung,
    "kapitel-plattform-fragen.svg": drei_fragen,
    "kapitel-bpmn-lernweg.svg": kapitel_bpmn,
    "kapitel-workflows-lernweg.svg": kapitel_workflows,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGS.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
        print("geschrieben:", name)
