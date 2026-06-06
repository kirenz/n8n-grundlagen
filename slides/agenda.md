# Agenda — n8n-Grundlagen

## Deck-Metadaten

- `title:` n8n-Grundlagen — von der Workflow-Idee zur produktiven KI-Automation
- `subtitle:` Asynchroner Standardkurs für Fachkräfte
- `author:` Jan Kirenz
- `language:` de
- `slug:` n8n-ai-agents
- `target_audience:` Fachkräfte aus Marketing, Operations, Sales — keine Vorkenntnisse in Workflow-Automation oder KI vorausgesetzt
- `tone:` editorial, gedeckt, indirekt; nutzenorientiert; pragmatisch ohne Pädagogik-Jargon
- `deck_goal:` Lernende können nach dem Kurs einen produktiven n8n-Workflow selbst bauen, KI-Bausteine bewusst integrieren und entscheiden, wo deterministische Steps und wo Agent-Logik hingehören.
- `expected_length_minutes:` ca. 45–60 Minuten Gesamt-Lernzeit über sechs Module verteilt

## Kursnutzen

Nach diesem Kurs:
- Einen produktiven n8n-Workflow aus Trigger, Nodes und Integrationen selbst bauen und debuggen
- Entscheiden, wo deterministische Schritte und wo KI-Schritte hingehören
- Eine eigene n8n-Instanz mit AI-Agent-Cluster, RAG-Pipeline und HITL-Approval-Gates produktiv betreiben

## Roter Faden — ein Workflow, der mit jedem Modul wächst

Ein einziger Demo-Workflow läuft durch alle sechs Module. Lernende erweitern ihn Schritt für Schritt. Tool-Stack ist bewusst inklusiv:

- **Mail-Anbindung:** generischer IMAP/SMTP-Knoten — funktioniert mit Gmail, Outlook, GMX, Web.de, eigenem Server
- **Datenspeicher:** n8n Data Tables (eingebaut, kein externes Konto)
- **Kein Slack, kein Teams, kein CRM nötig** — alles solo testbar mit einer beliebigen Mail-Adresse

| Modul | Erweiterung |
|---|---|
| 02 | Mail an sich selbst → automatische Bestätigung zurück → Eintrag in n8n Data Table |
| 03 | + Klassifikation per IF/Switch (Frage / Beschwerde / Sonstiges) → unterschiedliche Bestätigungs-Texte und Tags. Augmented View: optionale Plug-In-Punkte für Slack/Teams/Notion |
| 04 | KI liest die Mail → legt einen personalisierten Antwort-Draft als Entwurf in der eigenen Mail-Inbox ab (kein Auto-Versand) |
| 05 | Eine kleine FAQ in einer Data Table → Draft greift inhaltlich darauf zu |
| 06 | Approval-Schritt vor dem Senden, Eval-Trigger misst Draft-Qualität gegen ein Mini-Golden-Set |

## Inhalts-Sektionen

### Sektion 01 — Positionierung

- `chapter_number:` Modul 01
- **Schwerpunkt:** Positionierung, Pricing, Cloud vs. Self-Hosted
- **Quellen:** [[n8n]], `@green2026RelearnAgentTools`, n8n-Hosting-Docs (Web)
- **Folien:**
  - Ein erstes, ganz einfaches Beispiel (Timeline, Kontaktformular-Pattern)
  - Was n8n im Kern leistet (Two-Column, einsteigerfreundlich)
  - Pricing macht den Unterschied (Comparison)
  - 20+ Stunden pro Woche (Big-Stat-Stage)
  - Cloud, Self-Hosted oder Managed Hosting (Numbered Sections)
  - Was bei der Entscheidung zählt (Feature-Cards)

### Sektion 02 — Erste Workflows

- `chapter_number:` Modul 02
- **Schwerpunkt:** Trigger, Nodes, Daten — der erste echte Workflow. Mail-an-sich-selbst-Pattern, IMAP-Trigger, Bestätigungs-Mail, Eintrag in n8n Data Table.
- **Quellen:** `@n8nDocsFirstWorkflow`, `@n8nDocsNodes`
- **Folien (5):**
  - Workflow-Überblick (Numbered Sections: 01 Auslöser / 02 Antworten / 03 Festhalten)
  - Drei Trigger-Typen (Feature Cards: Manual / Schedule / E-Mail)
  - Daten zwischen Schritten weitergeben (Two-Column: Expressions, Item-Arrays)
  - Send confirmation + Data-Table-Eintrag (Numbered Sections)
  - Schritt für Schritt prüfen (Two-Column: Inline-Logs, Test-Run)

### Sektion 03 — Integrationen

- `chapter_number:` Modul 03
- **Schwerpunkt:** Workflow erweitert um IF/Switch-Klassifikation. Augmented View für Slack/Teams/Notion-Optionen, ohne sie zu erzwingen.
- **Quellen:** Use-Case-Web-Quellen (Robiz, DarwinApps, Anglara)
- **Folien (5):**
  - Vom geraden Pfad zur Verzweigung (Two-Column oder Numbered Sections)
  - IF/Switch-Knoten erklärt (Two-Column)
  - Drei Bestätigungs-Pfade (Feature Cards: Frage / Beschwerde / Sonstiges)
  - Augmented View: optionale Plug-In-Punkte (Comparison: Mail-only vs. Mail+Push)
  - Credentials sicher verwalten (Two-Column: Secrets, OAuth, App-Passwörter)

### Sektion 04 — KI-Cluster

- `chapter_number:` Modul 04
- **Schwerpunkt:** AI-Agent-Cluster-Node, Hybrid-Pattern. KI liest die Mail und legt einen Draft als Entwurf in der eigenen Inbox ab — kein Auto-Versand.
- **Quellen:** [[n8n]], [[ai-agents]], `@wiertz2025LLMAgentsGuide`, `@saravia2026DeterministicAISteps`, `@farcas2025BuildFirstAgent`, `@dmitrievna2025AIAgentsExplained`
- **Folien (5–6):**
  - Was KI im Workflow leistet (Two-Column)
  - Der AI-Agent-Cluster (Feature Cards: Chat-Model, Memory, Tools)
  - Hybrid-Pattern: deterministisch + KI (Comparison)
  - Praxis: Draft erstellen statt senden (Numbered Sections)
  - Stage-Moment: Quote oder Big-Stat aus Production AI Playbook

### Sektion 05 — RAG

- `chapter_number:` Modul 05
- **Schwerpunkt:** RAG-Pattern als Bausteine. FAQ-Tabelle als Wissensbasis, Draft greift inhaltlich darauf zu.
- **Quellen:** [[rag]], [[cloud-sovereignty]], `@dmitrievna2026RAGSystemArchitecture`, `@clement2025RAGPipelineN8N`, `@petton2026SovereignRAGOVHcloud`
- **Folien (5):**
  - Was RAG bedeutet — am Beispiel (Anschauung oder Two-Column)
  - Vier Bausteine: Ingestion / Vector-DB / Reranking / Generation (Numbered Sections)
  - Praxis: FAQ-Tabelle als Wissensbasis im Demo-Workflow (Two-Column)
  - Souveräne Variante: OVHcloud + pgvector (Comparison: Cloud-RAG vs. EU-RAG)
  - Stage-Moment: Wann RAG, wann anders?

### Sektion 06 — Production-Disziplin

- `chapter_number:` Modul 06
- **Schwerpunkt:** HITL-Approval vor dem Senden, Eval-Trigger gegen Mini-Golden-Set.
- **Quellen:** [[ai-governance]], [[llm-evaluation]], `@saravia2026HumanOversight`, `@n8n2026EvaluationMonitoring`, `@mann2025ComparativeMetrics`, `@green2025PracticalEvaluation`
- **Folien (5–6):**
  - Wo Approval Pflicht ist (Comparison: autonom vs. mit Approval)
  - HITL-Pattern (Feature Cards: Inline / Gate / Multi-Channel)
  - Eval-Klassen kompakt (Numbered Sections: Match/Similarity, Code, LLM-as-Judge, Safety)
  - Komparative > absolute Metriken (Two-Column)
  - Silent-Drift im laufenden Betrieb (Two-Column oder Tip-Box-Ersatz)
  - Closing-Beat: Was bleibt
