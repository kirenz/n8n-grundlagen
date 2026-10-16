"""Bilder für „Erste Workflows“: erster Workflow (Canvas, Panels, Datenfluss) und Credentials.

Aufruf: python3 scripts/build_workflow_figures.py  (schreibt nach images/erste-workflows/)
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_overview_figures import BLUE, GREEN, INK, LIGHT, MUTED, PAPER, RED, RULE, arrow, box, svg, text  # noqa: E402
from n8n_darstellung import canvas, panel  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "images" / "erste-workflows"
SET, MAIL, TABLE = "n8n-nodes-base.set", "n8n-nodes-base.emailSend", "n8n-nodes-base.dataTable"


def erster_canvas():
    names = [("Start workflow manually", "n8n-nodes-base.manualTrigger"), ("Receive email", SET),
             ("Send confirmation", MAIL), ("Prepare table entry", SET), ("Save table entry", TABLE)]
    nodes = [{"name": n, "type": ty, "typeVersion": 1, "position": [i * 200, 0], "parameters": {}} for i, (n, ty) in enumerate(names)]
    conns = {names[i][0]: {"main": [[{"node": names[i + 1][0], "type": "main", "index": 0}]]} for i in range(4)}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"nodes": nodes, "connections": conns}, f)
    return canvas(f.name, "Der erste Workflow: fünf Knoten", highlight=None)


def datenfluss():
    b = [text(450, 30, "Was zwischen den Knoten wandert", 17, 700, INK, "middle")]
    cols = [("Receive email", ["sender: max@example.com", "subject: Question about …", "text: Hello, I ordered …", "received_at: 2026-10-16T09:12"], "erzeugt vier Felder"),
            ("Send confirmation", ["An: {{ $json.sender }}", "Betreff: Thank you …", "reicht die Felder", "unverändert weiter"], "nutzt sender"),
            ("Prepare table entry", ["sender ← Receive email", "subject ← Receive email", "received_at ← Receive email", "status: new"], "holt Werte per Knotenname"),
            ("Save table entry", ["neue Zeile in", "customer_emails", "mit vier Spalten", ""], "speichert")]
    for i, (name, lines, note) in enumerate(cols):
        x = 20 + i * 220
        b.append(box(x, 55, 200, 44, LIGHT, BLUE, 10, 2))
        b.append(text(x + 100, 82, name, 14, 700, BLUE, "middle"))
        b.append(box(x, 110, 200, 120, "#ffffff", RULE, 8))
        for j, ln in enumerate(lines):
            b.append(text(x + 12, 134 + j * 24, ln, 12, 400, INK))
        b.append(text(x + 100, 252, note, 12, 600, MUTED, "middle"))
        if i < 3:
            b.append(arrow(x + 200, 77, x + 218, 77))
    b.append(box(20, 272, 860, 66, PAPER, PAPER, 10))
    b.append(text(40, 298, "{{ $json.feld }} liest ein Feld des direkt vorigen Knotens.", 13, 600, INK))
    b.append(text(40, 322, "{{ $('Receive email').item.json.feld }} liest gezielt aus einem früheren Knoten, egal was dazwischen liegt.", 13, 400, INK))
    return svg(900, 350, b)


def falsch_richtig():
    b = [text(450, 30, "Zugangsdaten: so nicht, so richtig", 17, 700, INK, "middle")]
    left = ["Hauptpasswort des Team-Postfachs", "steht direkt im Workflow", "Token mit Vollzugriff auf Slack", "Export enthält das Geheimnis"]
    right = ["App-Passwort oder OAuth statt Hauptpasswort", "liegt als Credential getrennt vom Workflow", "Token nur mit den nötigen Rechten", "Export enthält nur den Namen des Credentials"]
    b.append(box(30, 55, 410, 200, "#fef2f2", "#fecaca", 12))
    b.append(box(460, 55, 410, 200, "#f0fdf4", "#bbf7d0", 12))
    b.append(text(235, 86, "So nicht", 15, 700, RED, "middle"))
    b.append(text(665, 86, "So richtig", 15, 700, GREEN, "middle"))
    for i, (l, r) in enumerate(zip(left, right)):
        y = 124 + i * 36
        b.append(text(52, y, "✗", 16, 700, RED))
        b.append(text(76, y, l, 13))
        b.append(text(482, y, "✓", 16, 700, GREEN))
        b.append(text(506, y, r, 13))
    return svg(900, 270, b)


def trennung():
    b = [text(450, 30, "Credentials liegen getrennt vom Workflow", 17, 700, INK, "middle")]
    b.append(box(30, 60, 300, 170, LIGHT, BLUE, 12, 2))
    b.append(text(180, 90, "Workflow", 15, 700, BLUE, "middle"))
    b.append(box(55, 110, 250, 44, "#ffffff", RULE, 8))
    b.append(text(70, 137, "Knoten: Google Gemini Chat Model", 13, 600))
    b.append(text(70, 182, "kennt nur den Namen:", 12, 400, MUTED))
    b.append(text(70, 204, "„Google Gemini(PaLM) Api account“", 12, 600, INK))
    b.append(box(370, 60, 230, 170, "#ffffff", INK, 12, 2))
    b.append(text(485, 90, "Credential", 15, 700, INK, "middle"))
    b.append(text(485, 122, "API-Schlüssel, verschlüsselt", 12, 400, MUTED, "middle"))
    b.append(text(485, 142, "in n8n gespeichert", 12, 400, MUTED, "middle"))
    b.append(text(485, 180, "für mehrere Knoten", 12, 600, INK, "middle"))
    b.append(text(485, 200, "nutzbar", 12, 600, INK, "middle"))
    b.append(box(640, 105, 230, 80, "#ffffff", RULE, 12))
    b.append(text(755, 140, "Dienst", 15, 700, INK, "middle"))
    b.append(text(755, 162, "z. B. Google Gemini", 12, 400, MUTED, "middle"))
    b.append(arrow(330, 145, 368, 145))
    b.append(arrow(600, 145, 638, 145))
    b.append(text(619, 200, "meldet sich an", 11, 600, MUTED, "middle"))
    b.append(text(450, 262, "Wer den Workflow exportiert oder teilt, gibt den Schlüssel nicht mit weiter.", 13, 400, MUTED, "middle"))
    return svg(900, 280, b)


def arten():
    b = [text(450, 30, "Drei Arten von Zugangsdaten", 17, 700, INK, "middle")]
    items = [("App-Passwort", "für Mail-Postfächer (IMAP, SMTP)", ["eigenes Passwort nur für n8n", "einzeln widerrufbar", "Hauptpasswort bleibt geheim"]),
             ("OAuth", "für Gmail, Microsoft 365 und viele Dienste", ["Anmeldung beim Anbieter", "Rechte beim Anbieter sichtbar", "jederzeit widerrufbar"]),
             ("API-Schlüssel", "für Dienste wie Google Gemini", ["vom Anbieter erzeugt", "wie ein Passwort behandeln", "bei Verlust sofort löschen"])]
    for i, (name, sub, pts) in enumerate(items):
        x = 30 + i * 290
        b.append(box(x, 55, 260, 190, "#ffffff", RULE, 12))
        b.append(text(x + 20, 88, name, 17, 700))
        b.append(text(x + 20, 110, sub, 12, 400, MUTED))
        for j, p in enumerate(pts):
            b.append(f'<circle cx="{x + 26}" cy="{146 + j * 30}" r="4" fill="{BLUE}"/>')
            b.append(text(x + 38, 151 + j * 30, p, 13))
    b.append(text(450, 272, "Für alle drei gilt: nur so viele Rechte, wie der Workflow wirklich braucht.", 13, 600, INK, "middle"))
    return svg(900, 290, b)


def schluessel_weg():
    b = [text(450, 30, "Vom Gemini-Schlüssel zum Workflow", 17, 700, INK, "middle")]
    steps = [("1", "AI Studio", "aistudio.google.com/apikey"), ("2", "Create API key", "Schlüssel kopieren"),
             ("3", "n8n Credential", "Google Gemini(PaLM) Api"), ("4", "Gemini-Knoten", "Credential auswählen")]
    for i, (n, name, sub) in enumerate(steps):
        x = 20 + i * 220
        b.append(box(x, 60, 200, 100, "#ffffff", RULE, 12))
        b.append(f'<circle cx="{x + 28}" cy="88" r="14" fill="{BLUE}"/>')
        b.append(text(x + 28, 93, n, 13, 700, "#ffffff", "middle"))
        b.append(text(x + 20, 128, name, 15, 700))
        b.append(text(x + 20, 148, sub, 12, 400, MUTED))
        if i < 3:
            b.append(arrow(x + 200, 110, x + 218, 110))
    b.append(box(20, 180, 860, 50, "#fff7ed", "#fed7aa", 10))
    b.append(text(40, 211, "Kostenlose Stufe: Google nutzt Eingaben zur Produktverbesserung. Keine Kunden- oder Personaldaten senden.", 13, 600, "#9a3412"))
    return svg(900, 245, b)


def erster_bausteine():
    names = [("Send confirmation", MAIL), ("Start workflow manually", "n8n-nodes-base.manualTrigger"), ("Save table entry", TABLE),
             ("Receive email", SET), ("Prepare table entry", SET)]
    pos = [[0, 0], [220, 120], [440, 0], [660, 120], [880, 0]]
    nodes = [{"name": n, "type": ty, "typeVersion": 1, "position": pos[i], "parameters": {}} for i, (n, ty) in enumerate(names)]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"nodes": nodes, "connections": {}}, f)
    return canvas(f.name, "Fünf Bausteine, noch ohne Reihenfolge")


def cred_plan():
    b = [text(450, 30, "Der Plan des Kollegen", 17, 700, INK, "middle")]
    b.append(box(200, 55, 500, 190, "#ffffff", RULE, 12))
    b.append(text(450, 85, "Demo-Workflow geht live", 15, 700, INK, "middle"))
    rows = [("Postfach-Knoten", "Hauptpasswort des Team-Postfachs direkt eingetragen"),
            ("Slack-Knoten", "Token mit Vollzugriff auf den Workspace"),
            ("Testlauf", "separate Testadresse"),
            ("Tabellen", "Test- und Produktions-Tabelle getrennt")]
    for i, (k, v) in enumerate(rows):
        y = 118 + i * 30
        b.append(text(225, y, k, 13, 600, MUTED))
        b.append(text(370, y, v, 13))
    b.append(text(450, 268, "Was davon ist ein Risiko?", 13, 600, BLUE, "middle"))
    return svg(900, 285, b)


BILDER = {
    "erster-canvas.svg": erster_canvas,
    "erster-bausteine.svg": erster_bausteine,
    "cred-plan.svg": cred_plan,
    "erster-datenfluss.svg": datenfluss,
    "erster-receive.svg": lambda: panel("Receive email", SET, [
        ("Mode", "Manual Mapping", "select"), ("Fields to Set", "", "section"),
        ("sender", "max@example.com", "fixed"), ("subject", "Question about delivery time", "fixed"),
        ("text", "Hello, I ordered yesterday and was wondering when delivery will arrive. Best regards, Max", "fixed"),
        ("received_at", "{{ $now.toISO() }}", "expr")]),
    "erster-send.svg": lambda: panel("Send confirmation", MAIL, [
        ("From Email", "info@company.com", "fixed"), ("To Email", "{{ $json.sender }}", "expr"),
        ("Subject", "Thank you for your message", "fixed"), ("Email Format", "Text", "select"),
        ("Text", "Hello, thank you for your message. … Subject of your inquiry: {{ $json.subject }} …", "expr")],
        hint="Ohne Mail-Credential den Knoten über das Drei-Punkte-Menü deaktivieren (Deactivate)."),
    "erster-prepare.svg": lambda: panel("Prepare table entry", SET, [
        ("Fields to Set", "", "section"),
        ("sender", "{{ $('Receive email').item.json.sender }}", "expr"),
        ("subject", "{{ $('Receive email').item.json.subject }}", "expr"),
        ("received_at", "{{ $('Receive email').item.json.received_at }}", "expr"),
        ("status", "new", "fixed")]),
    "erster-save.svg": lambda: panel("Save table entry", TABLE, [
        ("Resource", "Row", "select"), ("Operation", "Insert", "select"),
        ("Data table", "customer_emails", "select"), ("Mapping Column Mode", "Map Automatically", "select")],
        hint="Map Automatically ordnet Felder und Spalten mit gleichem Namen einander zu."),
    "cred-falsch-richtig.svg": falsch_richtig,
    "cred-trennung.svg": trennung,
    "cred-arten.svg": arten,
    "cred-schluessel-weg.svg": schluessel_weg,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in BILDER.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    print("geschrieben:", len(BILDER), "Bilder")
