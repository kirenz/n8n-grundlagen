"""Erzeugt die importierbaren Beispiel-Workflows für „Beispiele zum Mitmachen“.

Aufruf: python3 scripts/build_beispiel_workflows.py
Schreibt nach workflows/beispiele/. Knotenversionen geprüft gegen n8n 2.39.
Die Dateien enthalten keine Zugangsdaten und keine instanzlokalen IDs
(Data-Table-Auswahl erfolgt nach dem Import).
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "workflows" / "beispiele"


def node(nid, name, ntype, version, pos, params):
    return {"parameters": params, "id": nid, "name": name, "type": ntype, "typeVersion": version, "position": pos}


def field(label, ftype="text", required=False, options=None, placeholder=None):
    f = {"fieldLabel": label}
    if ftype != "text":
        f["fieldType"] = ftype
    if placeholder:
        f["placeholder"] = placeholder
    if options:
        f["fieldOptions"] = {"values": [{"option": o} for o in options]}
    if required:
        f["requiredField"] = True
    return f


def assign(aid, name, value, vtype="string"):
    return {"id": aid, "name": name, "value": value, "type": vtype}


def set_node(nid, name, pos, assignments):
    return node(nid, name, "n8n-nodes-base.set", 3.4, pos, {"assignments": {"assignments": assignments}, "options": {}})


def if_node(nid, name, pos, left, op_type, operation, right):
    return node(nid, name, "n8n-nodes-base.if", 2.2, pos, {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [{"id": f"{nid}-c1", "leftValue": left, "rightValue": right,
                            "operator": {"type": op_type, "operation": operation}}],
            "combinator": "and",
        },
        "options": {},
    })


def link(*pairs):
    conns = {}
    for src, dst, out in pairs:
        conns.setdefault(src, {"main": []})
        main = conns[src]["main"]
        while len(main) <= out:
            main.append([])
        main[out].append({"node": dst, "type": "main", "index": 0})
    return conns


def wf(name, nodes, connections):
    return {"name": name, "nodes": nodes, "connections": connections, "settings": {"executionOrder": "v1"}, "pinData": {}}


def kontakt():
    nodes = [
        node("form", "Kontaktformular", "n8n-nodes-base.formTrigger", 2.2, [0, 0], {
            "formTitle": "Kontakt",
            "formDescription": "Wir melden uns innerhalb eines Werktags.",
            "formFields": {"values": [
                field("Name", required=True),
                field("E-Mail", "email", required=True),
                field("Anliegen", "dropdown", True, ["Frage zur Bestellung", "Beschwerde", "Rückruf"]),
                field("Nachricht", "textarea"),
            ]},
            "options": {},
        }),
        if_node("if", "Beschwerde?", [260, 0], "={{ $json.Anliegen }}", "string", "equals", "Beschwerde"),
        set_node("hoch", "Priorität hoch", [520, -100], [
            assign("h1", "name", "={{ $json.Name }}"), assign("h2", "email", "={{ $json['E-Mail'] }}"),
            assign("h3", "anliegen", "={{ $json.Anliegen }}"), assign("h4", "prioritaet", "hoch")]),
        set_node("normal", "Priorität normal", [520, 100], [
            assign("n1", "name", "={{ $json.Name }}"), assign("n2", "email", "={{ $json['E-Mail'] }}"),
            assign("n3", "anliegen", "={{ $json.Anliegen }}"), assign("n4", "prioritaet", "normal")]),
    ]
    return wf("Beispiel 1 · Kontaktanfragen sortieren", nodes,
              link(("Kontaktformular", "Beschwerde?", 0), ("Beschwerde?", "Priorität hoch", 0), ("Beschwerde?", "Priorität normal", 1)))


def rechnung():
    nodes = [
        node("form", "Rechnung erfassen", "n8n-nodes-base.formTrigger", 2.2, [0, 0], {
            "formTitle": "Rechnung erfassen",
            "formDescription": "Eingangsrechnung zur Prüfung erfassen.",
            "formFields": {"values": [
                field("Lieferant", required=True),
                field("Rechnungsnummer", required=True),
                field("Betrag", "number", required=True, placeholder="Betrag in Euro"),
            ]},
            "options": {},
        }),
        if_node("if", "Betrag über 1.000 €?", [260, 0], "={{ $json.Betrag }}", "number", "gt", 1000),
        node("wait", "Freigabe einholen", "n8n-nodes-base.wait", 1.1, [520, -100], {
            "resume": "form",
            "formTitle": "Rechnung freigeben",
            "formDescription": "=Rechnung {{ $json.Rechnungsnummer }} von {{ $json.Lieferant }} über {{ $json.Betrag }} Euro",
            "formFields": {"values": [field("Entscheidung", "dropdown", True, ["Freigeben", "Ablehnen"])]},
            "options": {},
        }),
        set_node("ergebnis", "Entscheidung festhalten", [780, -100], [
            assign("e1", "rechnung", "={{ $('Rechnung erfassen').item.json.Rechnungsnummer }}"),
            assign("e2", "status", "={{ $json.Entscheidung }}")]),
        set_node("auto", "Automatisch freigeben", [520, 100], [
            assign("a1", "rechnung", "={{ $json.Rechnungsnummer }}"),
            assign("a2", "status", "automatisch freigegeben")]),
    ]
    return wf("Beispiel 2 · Rechnung freigeben", nodes,
              link(("Rechnung erfassen", "Betrag über 1.000 €?", 0), ("Betrag über 1.000 €?", "Freigabe einholen", 0),
                   ("Betrag über 1.000 €?", "Automatisch freigeben", 1), ("Freigabe einholen", "Entscheidung festhalten", 0)))


def bericht():
    nodes = [
        node("sched", "Montags 8 Uhr", "n8n-nodes-base.scheduleTrigger", 1.2, [0, -100], {
            "rule": {"interval": [{"field": "weeks", "triggerAtDay": [1], "triggerAtHour": 8}]}}),
        node("manual", "Zum Testen starten", "n8n-nodes-base.manualTrigger", 1, [0, 100], {}),
        node("read", "Anfragen lesen", "n8n-nodes-base.dataTable", 1, [260, 0], {
            "resource": "row", "operation": "get", "returnAll": True,
            "dataTableId": {"__rl": True, "mode": "list", "value": ""}}),
        node("sum", "Nach Status zählen", "n8n-nodes-base.summarize", 1.1, [520, 0], {
            "fieldsToSummarize": {"values": [{"aggregation": "count", "field": "id"}]},
            "fieldsToSplitBy": "status", "options": {}}),
        set_node("zeile", "Berichtszeile", [780, 0], [
            assign("z1", "zeile", "=Status {{ $json.status }}: {{ $json.count_id }} Anfragen")]),
    ]
    return wf("Beispiel 3 · Wochenbericht", nodes,
              link(("Montags 8 Uhr", "Anfragen lesen", 0), ("Zum Testen starten", "Anfragen lesen", 0),
                   ("Anfragen lesen", "Nach Status zählen", 0), ("Nach Status zählen", "Berichtszeile", 0)))


def ki_einordnen():
    prompt = ("=Ordne die folgende Kundenanfrage genau einer Kategorie zu: Lieferung, Rücksendung, Rechnung oder Sonstiges. "
              "Antworte nur mit dem Namen der Kategorie.\n\nAnfrage: {{ $json.Nachricht }}")
    nodes = [
        node("form", "Kundenanfrage", "n8n-nodes-base.formTrigger", 2.2, [0, 0], {
            "formTitle": "Kundenanfrage",
            "formDescription": "Beschreiben Sie Ihr Anliegen.",
            "formFields": {"values": [field("Nachricht", "textarea", True)]},
            "options": {},
        }),
        node("chain", "Kategorie bestimmen", "@n8n/n8n-nodes-langchain.chainLlm", 1.7, [260, 0], {
            "promptType": "define", "text": prompt}),
        node("gemini", "Google Gemini Chat Model", "@n8n/n8n-nodes-langchain.lmChatGoogleGemini", 1.1, [260, 220], {
            "modelName": "models/gemini-3-flash-preview", "options": {"temperature": 0}}),
        set_node("out", "Ergebnis", [560, 0], [
            assign("k1", "kategorie", "={{ $json.text.trim() }}"),
            assign("k2", "nachricht", "={{ $('Kundenanfrage').item.json.Nachricht }}")]),
    ]
    conns = link(("Kundenanfrage", "Kategorie bestimmen", 0), ("Kategorie bestimmen", "Ergebnis", 0))
    conns["Google Gemini Chat Model"] = {"ai_languageModel": [[{"node": "Kategorie bestimmen", "type": "ai_languageModel", "index": 0}]]}
    return wf("Beispiel 4 · Anfrage mit Gemini einordnen", nodes, conns)


FILES = {"beispiel-1-kontaktanfragen.json": kontakt, "beispiel-2-rechnung-freigeben.json": rechnung,
         "beispiel-3-wochenbericht.json": bericht,
         "beispiel-4-ki-einordnen.json": ki_einordnen}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FILES.items():
        (OUT / name).write_text(json.dumps(fn(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("geschrieben:", name)
