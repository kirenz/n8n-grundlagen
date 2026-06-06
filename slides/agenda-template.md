# Agenda-Vorlage für KI-generierte Decks

Eingabe-Vertrag für die KI-Deck-Generierung. Diese Datei kopieren als `agenda.md` (oder Beliebigem), Felder ausfüllen, dann zusammen mit einem Verweis auf [`prompts/deck-generation.md`](prompts/deck-generation.md) an die KI übergeben.

Die KI liest die Agenda, plant den dramaturgischen Rhythmus, wählt Patterns aus [`elements.qmd`](elements.qmd) und schreibt eine renderbare `video-<slug>.qmd`.

---

## Deck-Metadaten

- `title:` — Haupttitel des Videos
- `subtitle:` — kurze Unterzeile (optional)
- `author:` Jan Kirenz
- `language:` de
- `slug:` — Datei-Suffix für `video-<slug>.qmd` (z.B. `agenten-grundlagen`)
- `target_audience:` — Zielgruppe (Default: Business-Professionals, Mid-/Senior-Level)
- `tone:` — gewünschte Tonalität (Default: editorial, gedeckt, indirekt)
- `deck_goal:` — was der Lernende nach dem Video wissen / können soll (1–2 Sätze)
- `book_chapter_slug:` — falls ein Online-Buch-Kapitel zum Video existiert (optional, triggert die Buch-Brücke)
- `book_chapter_title:` — Anzeigename des Kapitels in der Buch-Brücke (optional)
- `expected_length_minutes:` — Ziel-Länge des Videos in Minuten (5–7 typisch, beeinflusst Folien-Anzahl: ~10–14 Folien für 5–7 Min)

## Inhalts-Sektionen (mehrere möglich)

Wenn der Stoff in Kapitel zerfällt: pro Kapitel eine Sektion. Jede Sektion erzeugt einen `# Chapter-Opener {.stage .chapter ...}` plus die enthaltenen Content-Folien.

### Sektion 01

- `chapter_title:` — Anzeigename, kommt auf den Chapter-Opener (z.B. "Werkzeuge")
- `chapter_number:` — z.B. "Kapitel 02" (nur wenn mehrere Sektionen)
- `slides:` — Liste der Content-Folien (siehe Slide-Block-Schema unten)

### Slide-Block-Schema

Pro Folie:

- `slide_type:` — eines aus der Pattern-Liste unten
- `goal:` — was diese eine Folie erreichen soll (ein Satz)
- `key_points:` — 2–5 kurze Stichpunkte für die sichtbare Folie
- `evidence:` — Quellen / Zahlen / `@citationKey`-Referenzen für `.sources`-Block (optional)
- `visual_direction:` — Hinweis auf Bild / Diagramm / Code, ohne neue CSS-Idee
- `speaker_intent:` — was im `::: {.notes}`-Block gesprochen werden soll (vollständige Sätze, indirekte Ansprache)

## Anschauung-Slots (optional, 1–3 pro Deck)

Konzepte, die im Deck eine Anschauung-Folie verdienen — also ohne ein bildhaft einrastendes Beispiel nicht zünden:

- `concept:` — das abstrakte Konzept (z.B. "RAG", "Context Window", "Tool Use")
- `analogy_role:` — die berufliche Rolle / Szene aus Business-Welt (z.B. "Bibliothekarin ohne Zutritt"). Tonalität / Verbote siehe [`prompts/anschauung-playbook.md`](prompts/anschauung-playbook.md).
- `position_after_slide:` — nach welcher Content-Folie die Anschauung eingefügt werden soll (Folien-Nummer oder -Titel)

## Code-Slots (optional)

Wenn Code gezeigt werden soll:

- `language:` — `python`, `bash`, `sql`, `r`, `js`, `typescript`, `yaml`, `json`
- `code_block:` — der Code selbst (idiomatisch, kompakt)
- `explanation_lines:` — Liste von Zeilen-Erklärungen mit `.neon-pill`-Bezug, z.B. `[(1, "Import"), (3, "Konstruktor")]` — leer lassen, wenn Erklärung nur in Speaker-Notes erfolgen soll
- `layout:` — `two-column-with-explanation`, `full-width-reference`, oder `three-column-with-d2`

---

## Gültige `slide_type`-Werte

Stage-Patterns (Bühne, dunkel — `background-color="#0a0a0f"` Pflicht):

- `opener` — erste Folie, Hero-Bild
- `chapter-opener` — `#`-Abschnittsfolie für neuen Stoffabschnitt
- `anschauung` — Analogie-Szene (siehe Playbook)
- `breath` — ein Wort, riesig zentriert
- `closing-beat` — letzte inhaltliche Folie, ruhiger Schluss-Satz
- `big-stat-stage` — eine dominante Zahl auf dunklem Grund
- `quote-stage` — ein großes Zitat auf dunklem Grund

Content-Patterns (Schreibtisch, hell):

- `two-column-explainer` — Standard für konzeptionelle Erklärungen
- `media-split` — 45 % Bild + 55 % Text
- `metrics-grid` — 2–4 Kennzahlen
- `big-stat` — eine dominante Zahl, hell
- `feature-cards` — 2–5 gleichwertige Karten
- `timeline` — Entwicklungslinie / Roadmap
- `comparison` — Zwei-Seiten-Vergleich (mit `.highlighted` für die Zielseite)
- `quote-box` — kurzes Zitat, hell
- `formula` — Einzeilen-Gleichung / Merksatz
- `numbered-sections` — 3 nummerierte Spalten
- `animated-list` — Bullet-Liste, fadet ein
- `simple-animated-list` — ohne Bullets
- `key-takeaways` — Abschluss einer Sektion mit Merksätzen

Code-Patterns:

- `code-with-explanation` — Codewindow + Zeilen-Erklärung über `.neon-pill`
- `code-reference` — Codewindow allein, Erklärung in Speaker-Notes
- `code-with-diagram` — Drei-Spalten: D2 + Code + Text

Spezial:

- `book-bridge` — Übergang zum Online-Buch (am Deck-Ende)
- `progressive-d2-reveal` — Diagramm über mehrere Folien aufgebaut (3–6 Folien, je `slug_1.d2` bis `slug_n.d2`)

Inline-Boxen, die **innerhalb** anderer Patterns nutzbar sind:

- `tip-box` — handlungsleitende Einsicht (1–2 Sätze, blauer Linkenrand)
- `think-box` — reflektive Frage / Gedankenexperiment (Cream + Ocker)

---

## Choreographie-Default (von der KI angewandt, wenn nicht überschrieben)

Wenn die Agenda nichts anderes vorgibt, wendet die KI dieses Schema an:

```
Folie 1:           opener (stage)
Folien 2–4:        Desktop-Block (Content-Patterns)
Folie 5:           Anschauung oder Big-Stat-Stage (stage)
Folien 6–8:        Desktop-Block
Folie 9 (optional): zweite Anschauung oder Stage-Moment
Folien …:          weitere Desktop-Blöcke
Letzte Content-Folie:  closing-beat (stage)
Falls book_chapter_slug: book-bridge
Letzte Folie:      ## Literatur
```

Disziplin-Anker:

- niemals mehr als 5 Desktop-Folien hintereinander ohne Stage-Moment
- niemals mehr als 2 Stage-Folien hintereinander
- 1–3 Anschauung-Folien pro Deck, nicht mehr
- Sprach-Stil: indirekte Ansprache (kein "du", "Sie", "man")

Vollständiges Regelwerk: [`AGENTS.md`](AGENTS.md).

---

## Hinweise an die KI

- Wenn `slide_type` einer Folie unklar oder ungültig ist: nachfragen, nicht raten.
- Wenn Anschauung-Slot fehlt aber dem Stoff nach naheliegend: einen vorschlagen, nicht eigenmächtig setzen.
- Wenn `evidence` leer ist und ein Big-Stat oder Studie gemacht werden soll: Quelle anfragen, sonst kein Big-Stat.
- Bei Code-Slot ohne `code_block`-Inhalt: nicht selbst Code erfinden — beim Nutzer nachfragen.
- Wenn Frontmatter-Felder fehlen, die das Deck strukturell brauchen (`title`, `slug`, `target_audience`): nachfragen.
