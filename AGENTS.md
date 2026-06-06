# AGENTS.md — Mono-Repo für Lernplattform-Kurse

Dieses Dokument ist die **kanonische Quelle der Wahrheit** für jede KI, die in diesem Repo arbeitet. Wenn andere Dokumente widersprechen, gilt AGENTS.md.

Geschrieben am Beispiel `n8n-ai-agents`. Wer einen neuen Kurs anlegt, übernimmt dieses Dokument als Schablone.

---

## Repo-Struktur — Mono-Repo

Dieses Repo enthält **drei eng verbundene Welten** in einem Repository:

```
.
├── _quarto.yml              # Buch-Build-Konfiguration (project: book)
├── AGENTS.md                # Dieses Regelwerk — Buch-Stil
├── README.md                # Mono-Repo-Beschreibung
│
│  # — Buch-Welt (kanonische Quelle) —
├── index.qmd                # Buch-Willkommen
├── introduction.qmd         # Buch-Einführung
├── <modul-slug>/            # Pro Modul ein Verzeichnis mit Lessons
│   └── *.qmd
│
│  # — Slide-Welt (aus Buch generiert + feinjustiert) —
├── slides/
│   ├── AGENTS.md            # Slide-Stilregeln (gilt für slides/ ausschließlich)
│   ├── modul-XX/<lesson>.qmd
│   └── …
│
│  # — Kursbegleitende Ressourcen —
├── infra/                   # Hetzner-Setup für Demo-Instanzen
├── workflows/               # n8n-Demo-Workflows als JSON-Export
└── scripts/                 # Buch → Slides Generator
```

**Welche AGENTS.md gilt wann:**

- Beim Arbeiten an Buch-Kapiteln (`*.qmd` im Repo-Root oder in den Modul-Verzeichnissen außer `slides/`): **diese Datei** gilt — Wir-Form, Callouts, Buch-Disziplin.
- Beim Arbeiten an Slide-Decks (`slides/**/*.qmd`): **`slides/AGENTS.md`** gilt — indirekte Ansprache, Pattern-Bibliothek, Stage-Choreographie.

**Wichtigster Stilwechsel beim Übertrag:** Buch-Prosa nutzt **Wir-Form** („Wir bauen…"), Slide-Text und Speaker-Notes nutzen **indirekte Ansprache** („Drei Knoten reichen…"). Wer Inhalte vom Buch in ein Slide-Deck überträgt, schaltet bewusst um.

**Buch-First-Workflow:** Pro Lesson **erst** Buch-Kapitel schreiben, **dann** Slide-Deck via `scripts/generate_slides.py` daraus erzeugen und feinjustieren. Keine Slide-Inhalte ohne entsprechendes Buch-Kapitel als Quelle.

---

## TL;DR — KI-Schnellstart

Wenn ein Curriculum übergeben wird, in dieser Reihenfolge arbeiten:

1. **Lesen**: Diese Datei komplett. Plus `_quarto.yml` (Kapitel-Reihenfolge).
2. **Lesson-Granularität festlegen**: 2–4 Lessons pro Modul, 5–15 Min Lernzeit pro Lesson, **eine Lesson = ein `.qmd`-Kapitel = ein späteres Slide-Deck**.
3. **Pro Modul ein Verzeichnis** mit `index.qmd` (Modul-Übersicht in Wir-Form) + Lesson-Kapitel.
4. **Pro Lesson ein Kapitel** mit H1-Titel, Wir-Form-Prosa, Callouts für Vertiefungen, Tabellen für Vergleiche, Code-Blöcken mit Erklärung im Folge-Callout.
5. **Erstentwurf-Marker** am Anfang jedes nicht voll ausgearbeiteten Kapitels: `::: {.callout-note title="Status — Erstentwurf"}` plus am Ende einen Block `## Was als Nächstes ausgebaut werden muss` mit konkreten Vertiefungs-TODOs.
6. **Rendern**: `quarto render`. Output in `_book/`. Errors beheben, bevor an die Generator-Pipeline weitergereicht wird.
7. **Folien generieren** (separate Aktion): `uv run python scripts/generate_slides.py` erzeugt aus jedem Buch-Kapitel ein Reveal.js-Deck.

Output an den Nutzer: nur die Buch-Kapitel. Keine Meta-Erklärungen.

---

## Verbindliche Disziplin-Regeln (gelten überall)

### 1. Sprach-Stil: Wir-Form

**In sichtbarem Buch-Text** wird durchgängig die **Wir-Form** verwendet. Das ist der bewusste Unterschied zu den Folien-Decks im Slide-Repo, wo indirekte Ansprache gilt. Im Buch wirkt die Wir-Form persönlicher und führt die Leserinnen und Leser durch die Schritte.

| Verwenden | Vermeiden |
|---|---|
| „Wir öffnen den Editor und ziehen den Trigger-Knoten…" | „Du öffnest den Editor…" / „Sie öffnen den Editor…" |
| „Wir können den Workflow als JSON exportieren." | „Man kann den Workflow exportieren." |
| „Im nächsten Schritt prüfen wir das Ergebnis." | „Im nächsten Schritt prüfst du…" |
| „Drei Knoten reichen für den Anfang." | (auch okay — beschreibend, ohne Anrede) |

**Begründung:** Der Stil orientiert sich an [`books/data-science-de`](../data-science-de). Die Wir-Form schafft eine kollegiale Tonalität, ohne belehrend zu wirken.

**Speaker-Notes-Stil-Regel des Slide-Repos gilt hier NICHT.** Wer Inhalte zwischen Buch und Folien überträgt, achtet bewusst auf den Stilwechsel: Buch = Wir-Form, Folien = indirekte Ansprache.

### 2. Callout-Disziplin

Drei Callout-Typen sind Standard:

- `::: {.callout-tip}` — Hinweise, Faustregeln, Analogien. Mit `collapse="true"` einklappbar, wenn die Analogie ausführlicher ist.
- `::: {.callout-note}` — neutrale Hintergrund-Information, Querverweise, Detail-Erklärungen.
- `::: {.callout-important}` — Pflicht-Aufmerksamkeit, Sicherheits-Hinweise, häufige Fallstricke.

Pro Kapitel **maximal 4–5 Callouts.** Wenn mehr Vertiefungen nötig sind, wird das Kapitel zu lang — dann lieber teilen.

**Title in Callouts ist Pflicht** bei allen `.callout-tip` und `.callout-important`. Bei `.callout-note` optional, aber empfohlen.

### 3. Analogie-Auswahl

Analogien kommen aus der **Berufsalltagswelt** der Zielgruppe (Business-Professionals, Fachkräfte, Studierende mit beruflichem Bezug):

**Geeignet:**

- Werkstatt, Werkbank, Werkzeug an der Wand
- Bibliothek, Bibliothekarin, Dossier, Regal
- Büro, Assistenz, Schreibtisch, Korrespondenz
- Küche, Rezept, Zutat, Kochutensil
- Labor, Qualitätskontrolle, Messgerät
- Kontrollraum, Cockpit, Dashboard

**Nicht geeignet** (gleiche Verbots-Liste wie im Slide-Repo):

- Märchen, Mythologie, Zauberei
- Cartoon-Tiere, anthropomorphisierte Objekte
- Kindergarten-Beispiele (Bauklötze, Ampelmännchen)
- Superhelden, Videospiele
- „cute"-Stil

Eine Analogie pro Hauptbegriff reicht. Mehrere Analogien für denselben Begriff verwirren.

### 4. Pro Lesson ein Kapitel

**Eine Lesson = ein `.qmd`-Kapitel = später ein Slide-Deck.** Das ist die strikte Granularitäts-Regel.

- Wer einen Begriff einführt und sofort drei Use-Cases zeigt, hat zwei Lessons.
- Wer ein Konzept erklärt und parallel ein zweites Konzept einführt, hat zwei Lessons.
- Pro Kapitel ein H1, mehrere H2, optional H3 für Unter-Aspekte.

**Lernzeit pro Kapitel: 5–15 Minuten.** Wer länger braucht, hat zu viel Stoff im selben Kapitel.

### 5. Erstentwurf-Workflow

Ein neues Buch entsteht in zwei Stufen:

**Stufe A — Erstentwurf aus Speaker-Notes oder Recherche.**
Pro Lesson ein Kapitel mit:

- H1-Titel (kann später angepasst werden)
- Status-Callout am Anfang:
  ```
  ::: {.callout-note title="Status — Erstentwurf"}
  Erstentwurf aus den Speaker-Notes des zugehörigen Decks. Ausbau-Punkte am Ende.
  :::
  ```
- Wir-Form-Prosa der zentralen Aussagen
- Mindestens ein Callout (tip oder important) für Vertiefung
- Am Ende: TODO-Block
  ```
  ## Was als Nächstes ausgebaut werden muss

  - Konkreter Punkt 1 (etwa: Schritt-für-Schritt-Anleitung mit Screenshots)
  - Konkreter Punkt 2 (etwa: Konfigurations-Beispiel)
  - …
  ```

**Stufe B — Vollausbau pro Lesson.**

- Status-Callout entfernen
- TODO-Punkte abarbeiten: Screenshots ergänzen, Code-Beispiele, ausführliche Anleitungen, Vergleichs-Tabellen
- Zusätzliche Callouts für Tipps, Warnungen, vertiefende Analogien
- Zwei bis drei Mal so lang wie der Erstentwurf

Der Generator strippt den Status-Callout und den TODO-Block automatisch beim Erzeugen des Slide-Decks. Beide sind also für den Folien-Output unsichtbar.

### 6. Hands-on-Kapitelstruktur

Kapitel, in denen Leserinnen und Leser etwas in einem Tool selbst bauen (Workflows in n8n, Code in einem Editor, Pipelines in einer Plattform), folgen einer einheitlichen Struktur. **Theorie steht nicht in Vorab-Sektionen, sondern in Callouts neben dem jeweiligen Bauschritt.**

**Verbindliche Reihenfolge der H2-Sektionen:**

1. Kurze Einleitung (1–2 Sätze, Anknüpfung an das vorige Kapitel)
2. `## Zielbild` — Bild oder D2-Diagramm des fertigen Ergebnisses plus kurze Liste der Stationen
3. `## Schnellstart per Import` (optional) — Verweis auf eine begleitende JSON- oder Code-Datei; gehört VOR den Bauteil, weil er ein alternativer Einstieg ist („wer den Workflow zuerst sehen will, importiert ihn")
4. `## Schritt für Schritt selbst bauen` — Vorbereitung, dann durchnummerierte `### Schritt 1`, `### Schritt 2`, …
5. `## Fehler diagnostizieren` — Symptom-Tabelle mit wahrscheinlicher Ursache und nächstem Prüfschritt
6. `## Kontrollpunkt für Modul XX` — Bullet-Liste der Lernziele in Verb-Infinitiv-Form

**Keine Verweise auf spätere Kapitel.** Vorgriffe wie „in Modul 04 bauen wir …" verwirren mehr, als sie helfen, und veralten schnell, wenn sich die Modul-Reihenfolge ändert. Das gilt auch für eine eigene `## Wie es weitergeht`-Sektion am Kapitelende. Wenn eine Beobachtung im Kapitel später wieder aufgenommen wird, beschreiben wir sie dort, nicht hier vorab.

**Theorie wandert in Callouts neben den passenden Schritt:**

- Begriffs-Definitionen, Operator-Klassen, Vergleichstabellen, „Wann das eine, wann das andere?"-Entscheidungen
- Lange Konzept-Callouts mit `collapse="true"`, damit der Lesefluss nicht reißt
- Eine Daumenregel: Wer ein Konzept in einem eigenen H2-Block vor dem ersten `### Schritt` erklären will, baut stattdessen einen Callout neben den passenden Schritt

**Vorbild im Repo:** `first-workflows/first-workflow.qmd`. Wer ein neues Hands-on-Kapitel schreibt, orientiert sich an dieser Struktur.

**Was rausfliegt:**

- Eigenständige Vorab-Theorie-Sektionen wie „Vom geraden Pfad zur Verzweigung" oder „Switch im Detail" als H2-Block vor dem Bauen
- Reines Konzept-Kapitel als eigene Datei, wenn sich der Stoff in einen Callout neben dem Bauschritt einbetten lässt; Beispiel: das ehemalige `editor-orientierung.qmd` wurde in `first-workflow.qmd` integriert

### 7. Disziplin-Verbote

- **Direkt-Anrede** (du, Sie) — das ist der Folien-Stil, nicht der Buch-Stil
- **„man"-Konstruktionen** — wirken altbacken
- **Cartoon-Emojis im Fließtext** — Ausnahme: Status-Marker in Tabellen (✅ 🟡)
- **Lange Code-Blöcke ohne Folge-Callout-Erklärung** — wer Code zeigt, erklärt ihn auch
- **Marketing-Sprache** — keine Superlative, keine „revolutionäre" oder „bahnbrechende" Tools
- **Tippfehler-konservierte Anglizismen** im sichtbaren Text — „Unlimited workflows" → „Unbegrenzte Workflows" (Anglizismus nur, wenn er der etablierte Fachbegriff ist und im selben Satz erklärt wird)

---

## Repo-Struktur

```
.
├── _quarto.yml               # Buch-Konfiguration, Kapitel-Reihenfolge
├── index.qmd                 # Willkommen — Wer das Buch ist, was drin steht
├── introduction.qmd          # Begriffe in zwei Sätzen erklärt (Glossar-Vorzug)
│
├── <modul-slug-1>/           # Pro Modul ein Verzeichnis
│   ├── index.qmd             # Modul-Übersicht ("Wir werden ...")
│   ├── <lesson-1>.qmd        # Lesson 1 = späteres Slide-Deck
│   ├── <lesson-2>.qmd
│   └── ...
├── <modul-slug-2>/
│   └── ...
│
├── images/                   # Diagramme, Screenshots
├── scripts/
│   └── generate_slides.py    # Erzeugt Reveal.js-Decks aus Buch-Kapiteln
├── README.md                 # Repo-Beschreibung, Bauen, Stand
└── AGENTS.md                 # Diese Datei
```

**Modul-Verzeichnis-Slug**: kebab-case, beschreibend, kein „modul-XX"-Präfix nötig (Reihenfolge steht in `_quarto.yml`).

**Lesson-Datei-Slug**: kebab-case, beschreibt das Lesson-Thema, kein „lesson-XX"-Präfix.

---

## `_quarto.yml`-Schablone

```yaml
project:
  type: book

lang: de

execute:
  freeze: auto

book:
  title: "<Buch-Titel>"
  description: "<Untertitel oder Kernnutzen>"
  author: "Jan Kirenz"

  search:
    type: overlay
  page-footer:
    left: |
      © [Jan Kirenz](https://www.kirenz.com/), <JAHR>

  chapters:
    - index.qmd
    - introduction.qmd

    - part: <modul-1-slug>/index.qmd
      chapters:
        - <modul-1-slug>/<lesson-1>.qmd
        - <modul-1-slug>/<lesson-2>.qmd
        - …

    # … weitere Module

format:
  html:
    toc: true
    theme: cosmo
    code-copy: true
    highlight-style: github-dark
    code-overflow: wrap
    author-meta: "Jan Kirenz"
    callout-appearance: simple
```

---

## Index-Seiten — Konvention

### Top-Level `index.qmd`

- Titel `Willkommen {.unnumbered}`
- 2–3 Absätze: Wer das Buch ist, welcher Kurs damit verbunden ist, welcher Demo-Pfad sich durchzieht
- Nummerierte Liste mit Beispielen für den Einsatz des Themas
- `.callout-note` mit branchenübergreifenden Anwendungsfeldern
- `.callout-tip` mit Lernempfehlung am Ende

### `introduction.qmd`

- Titel `Einführung {.unnumbered}`
- Pro zentralen Begriff ein H2 mit zwei Sätzen Erklärung
- Reihenfolge folgt der späteren Buch-Reihenfolge

### Modul-`index.qmd`

- Titel `<Modul-Titel> {.unnumbered}`
- 1 Absatz: Worum es im Modul geht, was am Ende erreicht ist
- Aufzählung „Wir werden …": die Outcomes als Bulletpoints

---

## D2-Diagramme

D2-Diagramme folgen einer reduzierten Palette nach dem Vorbild von Anthropic- und OpenAI-Dokumentationen: ruhig, dezent, ein einziger Fokus. **Buch und Slides nutzen dieselben Diagrammquellen** im zentralen `d2/`-Ordner — kein doppeltes Bauen. Wer ein Diagramm anlegt, hält sich an folgende Regel.

**Palette — drei Werte, mehr nicht:**

| Rolle | Farbe | Einsatz |
|---|---|---|
| Neutral-Fill | `#ffffff` | alle Standard-Knoten |
| Neutral-Stroke / Edges | `#e4e4e7` (Rahmen) bzw. `#a1a1aa` (Kanten) | Standard-Rahmen, alle Verbindungen |
| Akzent | `#18181b` als Fill, `#fafafa` als Schrift | **genau ein** zentraler Knoten pro Diagramm |

**Strukturregeln:**

- `border-radius: 8` für alle Knoten
- `stroke-width: 1` für Standard-Knoten, `stroke-width: 2` für Kanten und den Akzent-Knoten
- `font-color: "#18181b"` für Standard-Knoten, `font-color: "#fafafa"` für den Akzent-Knoten
- Akzent-Knoten zusätzlich `bold: true`
- Keine weiteren Farben (kein Blau, kein Grün, kein Orange) — der einzelne dunkle Knoten trägt den Fokus
- Pro Diagramm **maximal sechs Knoten**, sonst wird das Bild zu komplex für den Buch-Lesefluss

**Beispiel als Schablone:** `d2/intro-rag-meta.d2` (vier Knoten mit Mehrfach-Eingang) oder `d2/m02-workflow-overview.d2` (lineare Drei-Schritt-Pipeline).

**Eingebunden im Kapitel:**

```markdown
![Bildunterschrift in einem Satz, ohne Selbstlob.](d2/<file>.svg){#fig-<slug> width="80%"}
```

`width="80%"` (oder `70%` bei kurzen Drei-Knoten-Pipelines) verhindert, dass das Diagramm im HTML-Buch ranzig groß rendert.

**Render-Workflow:** `scripts/render_d2.sh` rendert alle `.d2`-Dateien zu SVG. Vor jedem Commit einmal laufen lassen.

---

## Generator-Schnittstelle

Das Skript `scripts/generate_slides.py` produziert aus jedem Lesson-Kapitel ein Reveal.js-Deck unter `slides/<modul>/<lesson>.qmd`. Erwartet wird:

1. **Genau ein H1** pro Kapitel (= Slide-Titel)
2. **H2-Sektionen** als Slide-Brüche (Reveal.js-Konvention)
3. **H3 wird zu H2 demoted** im Generator (wegen Reveal.js-Sektionierung)
4. **Status-Callouts** werden vom Generator gestrippt
5. **TODO-Block** am Ende wird vom Generator gestrippt
6. **Tabellen, Code-Blöcke, Listen** wandern unverändert ins Deck — werden in der Folie kondensiert sichtbar

**Konsequenz für die Schreibarbeit:** Wer ein Buch-Kapitel verfasst, hat bereits die Slide-Struktur im Kopf. Eine H2 sollte einen abgeschlossenen Gedanken tragen, der auch als eigene Folie Sinn ergibt.

---

## Was im Buch nichts zu suchen hat

- **Speaker-Notes-Blöcke** (`::: {.notes}`) — gehören ins Slide-Deck, nicht ins Buch
- **Reveal.js-spezifische Markup** wie `{.stage}`, `.fragment`, `.codewindow`, `.key-badge`
- **Bild-Profile-Kommentare** (`<!-- image: profile="..." -->`) — gehören ins Slide-Deck
- **D2-Diagramme als Inline-Code** — Quelle als `.d2`-Datei im zentralen `d2/`-Ordner ablegen, mit `scripts/render_d2.sh` zu SVG rendern und über `![](d2/<file>.svg)` einbinden. Palette siehe Sektion „D2-Diagramme" oben.

---

## Validierung vor Commit

```bash
quarto render
```

Errors müssen behoben sein. Warnings inhaltlich prüfen.

Optional: vor größeren Stand-Wechseln kurz die Generator-Pipeline durchlaufen lassen, um sicherzugehen, dass der Stripper noch alle Erstentwurf-Marker korrekt erkennt:

```bash
uv run python scripts/generate_slides.py
```

---

## Anbindung an die Lernplattform

Die Lernplattform (`hdm/lernplattform`) verlangt pro Lesson drei Quellen:

- `quarto_url` — Link zum HTML-Kapitel **dieses** Buches
- `slide_url` — Link zum gerenderten Reveal.js-Deck (wird vom Generator erzeugt)
- `youtube_video_id` — Videoaufzeichnung der Folien

Die Plattform spielt diese drei Quellen pro Lesson zusammen aus. Das Buch liefert den ausführlichen Lehrtext, das Deck die Verdichtung, das Video die mündliche Erklärung.
