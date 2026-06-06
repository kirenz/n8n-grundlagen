# n8n-Grundlagen — Kurs-Mono-Repo

Mono-Repo für den Kurs **n8n-Grundlagen** auf der Lernplattform. Buch und Folien-Decks liegen zusammen, plus alle kursbegleitenden Ressourcen (Demo-Workflow, Hosting-Setup).

Der Kurs vermittelt das deterministische Fundament von n8n: Plattform einordnen, Instanz einrichten, ersten Workflow bauen. Der Aufbaukurs **KI-Agenten in n8n** (eigenes Repo `n8n-ai-agents`) setzt darauf auf.

## Struktur

```
.
├── _quarto.yml              # Buch-Build-Konfiguration
├── README.md                # diese Datei
├── references.bib           # Quellen für das Buch
├── book-theme.scss          # Buch-Theme (Plattform-Mirror-Look)
├── .gitignore
│
│  # — Buch (kanonische Quelle) —
├── index.qmd                # Willkommen
├── introduction.qmd         # Begriffs-Einführung
├── overview/                # Modul 01 — Plattform und Auswahl (3 Lessons)
├── first-workflows/         # Modul 02 — Erste Workflows (2 Lessons)
│
│  # — Slides (aus Buch generiert + feinjustiert) —
├── slides/
│   ├── AGENTS.md            # Slide-Stilregeln (indirekte Ansprache)
│   ├── _extensions/         # Quarto-Extensions
│   ├── custom-new.scss      # Slide-Theme
│   ├── elements.qmd         # Pattern-Bibliothek
│   ├── prompts/             # Bild-Generierung-Prompts
│   ├── profiles/            # Bild-Profile (anschauung, hero, ...)
│   ├── includes/            # Reveal-Bausteine (Hintergrund, Fonts, Footer)
│   ├── images/              # Slide-Bilder
│   ├── references.bib       # BibTeX
│   ├── scripts/             # validate_deck.py, generate_images.py
│   ├── tests/               # Validator-Tests
│   ├── slides-template.qmd  # Layout-Vorlage
│   └── video-n8n-grundlagen.qmd  # Legacy-All-in-One-Deck
│
│  # — Kursbegleitende Ressourcen —
├── infra/                   # Hosting-Setup für Demo-Instanzen
├── workflows/               # n8n-Demo-Workflow als JSON-Export
├── images/                  # Buch-Bilder (Diagramme, Screenshots)
├── d2/                      # D2-Diagramm-Quellen + gerenderte SVGs
└── scripts/
    └── generate_slides.py   # Buch → Slides
```

## Stilwelten

| Welt | Wo | Stil | AGENTS.md |
|---|---|---|---|
| Buch | Repo-Root + Modul-Verzeichnisse | **Wir-Form**, Callouts, Analogien | `./AGENTS.md` |
| Slides | `slides/` | **Indirekte Ansprache**, Patterns, Stages | `slides/AGENTS.md` |

Der Stilwechsel beim Übertragen von Buch zu Slide ist Pflicht.

## Buch-First-Workflow

Pro Lesson:

1. **Buch-Kapitel schreiben** (im Repo-Root unter dem passenden Modul-Verzeichnis) — Wir-Form, mit Callouts, Erstentwurf-Marker bei nicht ausgearbeiteten Kapiteln
2. **Generator laufen lassen**: `uv run python scripts/generate_slides.py` — erzeugt das Slide-Deck aus dem Buch-Kapitel
3. **Slide-Deck feinjustieren**: Stage-Momente ergänzen, Speaker-Notes in indirekter Ansprache, Bild-Blöcke für Anschauung-Folien, Pattern-Disziplin gemäß `slides/AGENTS.md`
4. **Validieren**: `cd slides && uv run python scripts/validate_deck.py <deck>.qmd`

Keine Slide-Inhalte ohne entsprechendes Buch-Kapitel als Quelle.

## Bauen

### Buch

```bash
quarto render
open _book/index.html
```

Das Buch-Build erfasst nur die in `_quarto.yml` unter `project.render` aufgelisteten Pfade. Slides, `infra/`, `workflows/` und `scripts/` werden ausgelassen.

### Einzelnes Slide-Deck

```bash
quarto render slides/video-n8n-grundlagen.qmd
```

Das Slide-Deck wird standalone gerendert mit dem im File-Frontmatter definierten Reveal.js-Format.

## Lernplattform-Anbindung

Pro Lesson liefert das Repo drei Quellen:

- `quarto_url` — HTML-Kapitel des Buches (`_book/<modul>/<lesson>.html`)
- `slide_url` — Reveal.js-Deck (`slides/<deck>.html` nach Render)
- `youtube_video_id` — Videoaufzeichnung des Decks (manuell ergänzt)

## Arbeitsstand

| Modul | Buch | Slides |
|---|---|---|
| 01 — Plattform und Auswahl | ✅ Vollausbau | 🟡 Im Legacy-Deck |
| 02 — Erste Workflows | ✅ Gezielt ausgebaut | 🟡 Im Legacy-Deck |

**Migrationspfad:** Das Legacy-Deck `video-n8n-grundlagen.qmd` deckt noch Module aus dem früheren Gesamtkurs ab. Schrittweise pro Lesson ein eigenes Deck erzeugen und das Legacy-Deck auf die zwei Grundlagen-Module eindampfen.

## Lizenz

Inhalt: © Jan Kirenz, 2026.
