"""Bilder für „Beispiele zum Mitmachen“: Canvas je Workflow und Panels je Bauschritt.

Aufruf: python3 scripts/build_beispiel_bilder.py  (schreibt nach images/beispiele/)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n8n_darstellung import canvas, panel  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "beispiele"
WF = ROOT / "workflows" / "beispiele"
FORM, IF, SET, WAIT = "n8n-nodes-base.formTrigger", "n8n-nodes-base.if", "n8n-nodes-base.set", "n8n-nodes-base.wait"
TABLE, SUM, SCHED = "n8n-nodes-base.dataTable", "n8n-nodes-base.summarize", "n8n-nodes-base.scheduleTrigger"
CHAIN, GEM = "@n8n/n8n-nodes-langchain.chainLlm", "@n8n/n8n-nodes-langchain.lmChatGoogleGemini"

BILDER = {
    "b1-canvas.svg": lambda: canvas(WF / "beispiel-1-kontaktanfragen.json", "Beispiel 1 · Kontaktanfragen sortieren"),
    "b1-formular.svg": lambda: panel("Kontaktformular", FORM, [
        ("Form Title", "Kontakt", "fixed"), ("Form Description", "Wir melden uns innerhalb eines Werktags.", "fixed"),
        ("Form Elements", ["Name (Text, Required Field)", "E-Mail (Email, Required Field)",
                           "Anliegen (Dropdown List: Frage zur Bestellung, Beschwerde, Rückruf)", "Nachricht (Textarea)"], "list")]),
    "b1-if.svg": lambda: panel("Beschwerde?", IF, [
        ("Conditions", "", "section"), ("Value 1", "{{ $json.Anliegen }}", "expr"),
        ("Operator", "String › is equal to", "select"), ("Value 2", "Beschwerde", "fixed")],
        hint="Ausgang true: Beschwerden. Ausgang false: alle anderen Anliegen."),
    "b1-set.svg": lambda: panel("Priorität hoch", SET, [
        ("Mode", "Manual Mapping", "select"), ("Fields to Set", "", "section"),
        ("name", "{{ $json.Name }}", "expr"), ("email", "{{ $json['E-Mail'] }}", "expr"),
        ("anliegen", "{{ $json.Anliegen }}", "expr"), ("prioritaet", "hoch", "fixed")]),
    "b2-canvas.svg": lambda: canvas(WF / "beispiel-2-rechnung-freigeben.json", "Beispiel 2 · Rechnung freigeben"),
    "b2-formular.svg": lambda: panel("Rechnung erfassen", FORM, [
        ("Form Title", "Rechnung erfassen", "fixed"),
        ("Form Elements", ["Lieferant (Text, Required Field)", "Rechnungsnummer (Text, Required Field)",
                           "Betrag (Number, Required Field)"], "list")]),
    "b2-if.svg": lambda: panel("Betrag über 1.000 €?", IF, [
        ("Conditions", "", "section"), ("Value 1", "{{ $json.Betrag }}", "expr"),
        ("Operator", "Number › is greater than", "select"), ("Value 2", "1000", "fixed")],
        hint="Ausgang true: Freigabe nötig. Ausgang false: automatisch freigeben."),
    "b2-wait.svg": lambda: panel("Freigabe einholen", WAIT, [
        ("Resume", "On Form Submitted", "select"), ("Form Title", "Rechnung freigeben", "fixed"),
        ("Form Description", "Rechnung {{ $json.Rechnungsnummer }} von {{ $json.Lieferant }} über {{ $json.Betrag }} Euro", "expr"),
        ("Form Elements", ["Entscheidung (Dropdown List: Freigeben, Ablehnen, Required Field)"], "list")],
        hint="Der Workflow hält hier an, bis eine Person das Freigabe-Formular absendet."),
    "b2-set.svg": lambda: panel("Entscheidung festhalten", SET, [
        ("Fields to Set", "", "section"),
        ("rechnung", "{{ $('Rechnung erfassen').item.json.Rechnungsnummer }}", "expr"),
        ("status", "{{ $json.Entscheidung }}", "expr")]),
    "b3-canvas.svg": lambda: canvas(WF / "beispiel-3-wochenbericht.json", "Beispiel 3 · Wochenbericht"),
    "b3-schedule.svg": lambda: panel("Montags 8 Uhr", SCHED, [
        ("Trigger Interval", "Weeks", "select"), ("Weeks Between Triggers", "1", "fixed"),
        ("Trigger on Weekdays", "Monday", "select"), ("Trigger at Hour", "8am", "select")]),
    "b3-table.svg": lambda: panel("Anfragen lesen", TABLE, [
        ("Resource", "Row", "select"), ("Operation", "Get row(s)", "select"),
        ("Data table", "customer_emails", "select"), ("Return All", "aktiviert", "toggle")],
        hint="Nach dem Import einmal customer_emails aus der Liste wählen: Tabellen sind je Instanz eigene Objekte."),
    "b3-summarize.svg": lambda: panel("Nach Status zählen", SUM, [
        ("Fields to Summarize", "", "section"), ("Aggregation", "Count", "select"), ("Field", "id", "fixed"),
        ("Fields to Split By", "status", "fixed")]),
    "b4-canvas.svg": lambda: canvas(WF / "beispiel-4-ki-einordnen.json", "Beispiel 4 · Anfrage mit Gemini einordnen"),
    "b4-credential.svg": lambda: panel("Google Gemini(PaLM) Api account", GEM, [
        ("Host", "https://generativelanguage.googleapis.com", "fixed"),
        ("API Key", "••••••••••••••••••••••••", "fixed")],
        hint="Den Schlüssel aus AI Studio einfügen und mit Save speichern. Er erscheint danach nie wieder im Klartext."),
    "b4-chain.svg": lambda: panel("Kategorie bestimmen", CHAIN, [
        ("Source for Prompt (User Message)", "Define below", "select"),
        ("Prompt (User Message)", "Ordne die folgende Kundenanfrage genau einer Kategorie zu: … Anfrage: {{ $json.Nachricht }}", "expr")]),
    "b4-modell.svg": lambda: panel("Google Gemini Chat Model", GEM, [
        ("Credential to connect with", "Google Gemini(PaLM) Api account", "select"),
        ("Model", "models/gemini-3-flash-preview", "select"), ("Options › Sampling Temperature", "0", "fixed")],
        hint="Temperatur 0: Das Modell antwortet möglichst gleichbleibend, gut für feste Kategorien."),
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in BILDER.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    print("geschrieben:", len(BILDER), "Bilder")
