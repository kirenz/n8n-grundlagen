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


WEBHOOK_TYPES = {"n8n-nodes-base.formTrigger", "n8n-nodes-base.wait", "@n8n/n8n-nodes-langchain.chatTrigger"}


def wf(name, nodes, connections):
    import uuid
    for n in nodes:
        if n["type"] in WEBHOOK_TYPES:
            n["webhookId"] = str(uuid.uuid5(uuid.NAMESPACE_URL, f"kirenz-n8n-grundlagen/{name}/{n['name']}"))
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


FAQ = """Beispiel-FAQ des Online-Shops (erfundene Angaben für den Kurs)

Lieferung: Der Standardversand dauert innerhalb Deutschlands 2 bis 4 Werktage. Ab 50 Euro Bestellwert ist der Versand kostenlos, darunter kostet er 4,90 Euro. Expressversand kostet 9,90 Euro und kommt am nächsten Werktag, wenn die Bestellung bis 12 Uhr eingeht.

Rücksendung: Es gilt ein Rückgaberecht von 30 Tagen ab Erhalt der Ware. Das Rücksendeetikett steht im Kundenkonto unter Bestellungen. Die Erstattung erfolgt innerhalb von 5 Werktagen nach Eingang der Rücksendung.

Beschädigte Ware: Schäden bitte innerhalb von 7 Tagen mit einem Foto an den Kundenservice melden. Dann gibt es Ersatz oder eine Gutschrift.

Zahlung: Möglich sind Rechnung, Kreditkarte und PayPal. Rechnungen sind innerhalb von 14 Tagen zu zahlen.

Kundenkonto: Das Passwort lässt sich über Passwort vergessen auf der Anmeldeseite zurücksetzen. Die Lieferadresse ändert man im Kundenkonto unter Profil."""


def sub(src, dst, ctype):
    return {src: {ctype: [[{"node": dst, "type": ctype, "index": 0}]]}}


def rag():
    gem_emb = ("@n8n/n8n-nodes-langchain.embeddingsGoogleGemini", 1, {"modelName": "models/gemini-embedding-001"})
    nodes = [
        node("load", "Wissen laden", "n8n-nodes-base.manualTrigger", 1, [0, 0], {}),
        set_node("faq", "FAQ-Text", [220, 0], [assign("f1", "text", FAQ)]),
        node("insert", "FAQ speichern", "@n8n/n8n-nodes-langchain.vectorStoreInMemory", 1.3, [460, 0], {
            "mode": "insert", "memoryKey": {"__rl": True, "mode": "list", "value": "shop_faq"}, "clearStore": True}),
        node("emb1", "Embeddings (Speichern)", gem_emb[0], gem_emb[1], [360, 220], gem_emb[2]),
        node("loader", "Default Data Loader", "@n8n/n8n-nodes-langchain.documentDefaultDataLoader", 1.1, [580, 220], {
            "jsonMode": "expressionData", "jsonData": "={{ $json.text }}", "textSplittingMode": "custom", "options": {}}),
        node("split", "Text Splitter", "@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter", 1, [680, 420], {
            "chunkSize": 300, "chunkOverlap": 0, "options": {}}),
        node("chat", "Chat", "@n8n/n8n-nodes-langchain.chatTrigger", 1.5, [0, 640], {"options": {}}),
        node("agent", "FAQ-Agent", "@n8n/n8n-nodes-langchain.agent", 3.1, [300, 640], {"options": {"systemMessage":
            "Du bist der Kundenservice-Assistent des Online-Shops. Beantworte Fragen nur mit Informationen aus dem Werkzeug FAQ durchsuchen. "
            "Wenn die FAQ keine Antwort enthalten, sage das ehrlich und verweise auf den Kundenservice. Antworte kurz und auf Deutsch."}}),
        node("model", "Google Gemini Chat Model", "@n8n/n8n-nodes-langchain.lmChatGoogleGemini", 1.1, [200, 860], {
            "modelName": "models/gemini-3-flash-preview", "options": {"temperature": 0}}),
        node("tool", "FAQ durchsuchen", "@n8n/n8n-nodes-langchain.vectorStoreInMemory", 1.3, [460, 860], {
            "mode": "retrieve-as-tool", "memoryKey": {"__rl": True, "mode": "list", "value": "shop_faq"},
            "toolDescription": "Durchsucht die FAQ des Online-Shops zu Lieferung, Rücksendung, beschädigter Ware, Zahlung und Kundenkonto.",
            "topK": 3}),
        node("emb2", "Embeddings (Suchen)", gem_emb[0], gem_emb[1], [460, 1060], gem_emb[2]),
    ]
    conns = link(("Wissen laden", "FAQ-Text", 0), ("FAQ-Text", "FAQ speichern", 0), ("Chat", "FAQ-Agent", 0))
    for part in (sub("Embeddings (Speichern)", "FAQ speichern", "ai_embedding"), sub("Default Data Loader", "FAQ speichern", "ai_document"),
                 sub("Text Splitter", "Default Data Loader", "ai_textSplitter"), sub("Google Gemini Chat Model", "FAQ-Agent", "ai_languageModel"),
                 sub("FAQ durchsuchen", "FAQ-Agent", "ai_tool"), sub("Embeddings (Suchen)", "FAQ durchsuchen", "ai_embedding")):
        conns.update(part)
    return wf("Beispiel 5 · FAQ-Agent mit RAG", nodes, conns)


FILES = {"beispiel-1-kontaktanfragen.json": kontakt, "beispiel-2-rechnung-freigeben.json": rechnung,
         "beispiel-3-wochenbericht.json": bericht,
         "beispiel-4-ki-einordnen.json": ki_einordnen,
         "beispiel-5-faq-agent-rag.json": rag}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FILES.items():
        (OUT / name).write_text(json.dumps(fn(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("geschrieben:", name)
