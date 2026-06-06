# AGENTS.md — Regelwerk für Lernplattform-Decks

Dieses Dokument ist die **kanonische Quelle der Wahrheit** für jede KI, die in diesem Repo Decks erzeugt oder bearbeitet. Wenn andere Dokumente widersprechen, gilt AGENTS.md.

---

## Buch-First-Workflow ist Standard

Für die Lernplattform gilt: **Das Buch im Repo-Root (Parent-Verzeichnis von `slides/`) ist die kanonische Quelle.** Folien-Decks werden aus den Buch-Kapiteln generiert, nicht handgeschrieben.

- Pro Lesson-Buch-Kapitel entsteht **ein eigenes Slide-Deck** (nicht ein gemeinsames `video-<slug>.qmd` für alle Module).
- Die generierten Decks landen in `slides/<modul>/<lesson>.qmd`. Erzeugt werden sie über `scripts/generate_slides.py` im Repo-Root.
- **Stilwechsel beim Übertragen:** Buch nutzt **Wir-Form** (siehe [`../AGENTS.md`](../AGENTS.md) im Repo-Root; vollständig ausgearbeitetes Vorbild: `kurse/n8n-ai-agents/AGENTS.md`). Slide-Decks und Speaker-Notes nutzen **indirekte Ansprache** (siehe Disziplin-Regel 1 unten). Speaker-Notes werden beim Feinjustieren neu geschrieben — nicht 1:1 aus dem Buch übernommen.
- Wer Folien ohne entsprechendes Buch-Kapitel anlegt oder ändert, bricht den Buch-First-Workflow. Erst Buch-Kapitel pflegen, dann generieren, dann feinjustieren.

Skill-Workflow: [`kurs-lernplattform-builder`](~/.agents/skills/kurs-lernplattform-builder/SKILL.md). Phase 5a = Buch-Kapitel, Phase 5b = Folien daraus.

---

## TL;DR — KI-Schnellstart (Folien-Feinjustierung nach Generator)

Wenn ein generiertes Slide-Deck zur Feinjustierung vorliegt — oder, in Altfällen, eine Agenda direkt zu Folien werden soll — in dieser Reihenfolge arbeiten:

1. **Lesen**: Diese Datei komplett. Plus [`prompts/anschauung-playbook.md`](prompts/anschauung-playbook.md) bei jedem Anschauung-Slot. Plus [`elements.qmd`](elements.qmd) als Pattern-Referenz.
2. **Buch-Kapitel als Quelle prüfen**: Falls das Deck aus einem Buch generiert wurde, das zugehörige `<book>/<modul>/<lesson>.qmd` parallel offen halten — Inhalts-Anker.
3. **Planen**: Den dramaturgischen Rhythmus festlegen (Opener Stage → Desktop-Blöcke → Stage-Momente → Closing-Beat). Maximal 5 Desktop-Folien zwischen Stages, niemals mehr als 2 Stages in Folge.
4. **1–3 Anschauung-Slots identifizieren**: Konzepte, die ohne vivid-Example-Bild nicht zünden.
5. **Pattern wählen** pro Folie aus `elements.qmd`. Keine neuen CSS-Klassen erfinden.
6. **Bild-Blöcke** als HTML-Kommentar direkt über Stage-/Hero-/Anschauung-/Media-Split-Folien.
7. **Speaker-Notes** pro Folie als `::: {.notes}`-Block — **immer in indirekter Ansprache**, kein "du"/"Sie"/"man". Beim Übertrag aus Buch-Prosa: Wir-Form bewusst zu indirekter Ansprache umformulieren.
8. **Validieren**: `uv run python scripts/validate_deck.py <deck>.qmd`. Errors beheben, Warnings prüfen.
9. **Bilder generieren** wahlweise via Gemini (`generate_images.py`) oder Codex-Export (`export_image_prompts.py`).
10. **Rendern**: `quarto render <deck>.qmd`.

Output: nur der Inhalt der `.qmd`. Keine zusätzlichen Erklärungen.

---

## Verbindliche Disziplin-Regeln (gelten überall)

### 1. Sprach-Stil: indirekte Ansprache

**In sichtbarem Folien-Text UND in Speaker-Notes**: keine direkte Anrede. Weder "du" / "dir" / "dein" noch "Sie" / "Ihnen" / "Ihr". Auch kein "man". Keine Imperative ("Stell dir vor", "Denk an", "Überlege").

Stattdessen: **beschreibende Indikativsätze, Nominalphrasen, Szenen-Titel**.

| Vermeiden | Stattdessen |
|---|---|
| "Stell dir einen Handwerker vor" | "Der Handwerker am Morgen" |
| "Im Buch findest du weiterführende Beispiele" | "Im Buch liegen weiterführende Beispiele bereit" |
| "Bevor du die Pipeline baust, überleg ..." | "Ein Gedankenexperiment vor der Pipeline: ..." |
| "Sie sehen hier die drei Rollen" | "Die drei Rollen im Workflow" |
| "Man nehme eine Projektleiterin" | "Projektleiterin am Whiteboard" |

**Warum:** Die Zielgruppe sind Business-Professionals in Lehrvideos. Eine direkte Anrede wirkt belehrend ("Sie") oder vertraulich ("du"); "man" wirkt altbacken. Eine beschreibende Tonalität lässt den Lernenden Raum für eigene Einordnung und passt zum editorialen Charakter des Blueprints.

**Ausnahme:** Zitate aus externen Quellen dürfen die Original-Ansprache behalten. Alles **Selbstgeschriebene** bleibt indirekt.

### 2. Inline-Highlight-Semantik

`.highlight-*`-Klassen sind **Bedeutung**, nicht Deko. Farbe = Rolle:

- `.highlight-green` — bestätigend, positiv, Lösung, Erfolg
- `.highlight-yellow` — Kernzahl, zentraler Merksatz, "das bitte behalten"
- `.highlight-blue` — technischer Begriff, Konzept, Definition
- `.highlight-orange` — Warnung, Vorsicht, Problem, Trade-off
- `.highlight-pink` — nur Ausnahme (z.B. Markenname wie Anthropic)
- `.highlight-white` — nur auf Stage, neutrale Hervorhebung

**Disziplin: maximal zwei `.highlight-*`-Markierungen pro Folie.** Wenn mehr Wörter betont werden müssen, **Bold** (`**Wort**`) nutzen oder kürzen. Vier oder fünf gefärbte Wörter heben nichts mehr hervor — sie wirken zufällig.

### 3. Disziplin-Verbote

Tabu im Premium-Blueprint:

- **Cartoon-Emojis in CTAs**: 🚀 💻 🎉 🎊 🎈 — zu Bootcamp-y für Business-Zielgruppe.
- **Emojis in Folientiteln** — wirkt plakativ. Ausnahme: `1️⃣ 2️⃣ 3️⃣` in nummerierten Listen, sparsam.
- **`.typewriter*` auf Fließtext** — Zuschauer wartet auf Text, statt zuzuhören. Höchstens für ein einzelnes Schlüsselwort.
- **Absolute-positionierte Icons mit Pixel-Koordinaten** — bricht auf Mobile / im PDF. Stattdessen Media-Split oder `{{< fa <icon> >}}` inline.
- **Mehr als 2 Fragment-Animations-Klassen pro Folie** (`.blur-focus + .zoom-in-bounce + .slide-right + ...`). Eine bis zwei reichen.
- **Neue CSS-Klassen erfinden**, neue Layoutsysteme, neue Include-Konventionen — alles strikt aus `elements.qmd`.

---

## Slide-Hierarchie und Strukturregeln

### Slide-Einstiege

- **`#`** für Abschnittsfolien (Opener, Chapter-Opener, Anschauung, Breath). Immer Stage.
- **`##`** für Content-Folien (Schreibtisch, hell). Auch für explizite Stage-Patterns (Closing-Beat, Quote-Stage, Big-Stat-Stage).
- **`###`, `####` etc. sind im gesamten Folien-Body verboten** — auch innerhalb von `.comparison-side`, `.feature` oder `.column`. Pandoc rendert sie als verschachteltes `<section>`-Element; Reveal.js interpretiert das als vertikale Sub-Folie und bricht die Right-Arrow-Navigation (Folge: Deck wirkt nach der betroffenen Folie „abgebrochen"). Für visuelle Sub-Überschriften im Content `**Bold**`-Absätze nutzen. Der Validator weist `###`-Headings im Body als Error zurück.

### Notes-Block-Pflicht

Jede Folie braucht direkt im Anschluss **genau einen** `::: {.notes}`-Block mit dem vollständig formulierten TTS-Text. Regeln:

- Vollständig formulierte Sätze, keine Stichpunkte.
- Nur Sprechtext, keine Meta-Kommentare zum Deck oder zur Technik.
- Regiehinweise nur in eckigen Klammern: `[KLICK]`, `[PAUSE]`, `[WEITER]`. Werden vom TTS-Exporter automatisch entfernt.
- Indirekte Ansprache (siehe Disziplin-Regel 1).

### Stage-Folien: Hintergrund-Regel

Für **jede** Stage-Folie ist `background-color="#0a0a0f"` als Quarto-Attribut **Pflicht**. Sonst zeigt Reveal.js einen weißen Rand um die Slide-Content-Box.

Mit Hero-Bild:
```
# Titel {.stage background-image="../images/hero-<slug>.png" background-color="#0a0a0f" background-opacity="0.75"}
```

Ohne Hero-Bild (Closing, Breath etc.):
```
## Was bleibt {.stage .closing background-color="#0a0a0f"}
```

Was die Attribute tun:
- `background-image` — das Hero-Bild selbst (optional)
- `background-color="#0a0a0f"` — dunkler Fallback. Pflicht. Füllt den Viewport (Reveal.js-Layer).
- `background-opacity="0.75"` — dimmt das Bild leicht für Titel-Lesbarkeit (0.65–0.85, nur mit Bild)

Hintergrund: Reveal.js rendert `data-background-*`-Attribute in einer separaten Layer, die den **gesamten Viewport** füllt — nicht nur das Section-Element. SCSS hat einen `:has()`-Fallback für die Viewport-Farbe, aber die Quarto-Attribute sind robuster.

### Choreographie: dramaturgischer Rhythmus

Jedes Deck folgt diesem Schema:

```
Opener (stage)
→ n × [ Desktop-Block (3–5 hell) + Stage-Moment (1 dunkel) ]
→ Closing-Beat (stage)
→ optional: Buch-Brücke
→ Literatur
```

- **Erste Folie**: immer Stage-Opener (`# Titel {.stage ...}`).
- **Zwischen Stages**: 3–5 Desktop-Folien. Niemals mehr als 5 in Folge.
- **Stage-Momente** unterbrechen den Schreibtisch-Strom: Big-Stat-Stage, Quote-Stage, Anschauung, Breath, Chapter-Opener.
- Niemals **mehr als 2 Stage-Folien hintereinander**.
- **Letzte inhaltliche Folie**: Closing-Beat (`{.stage .closing}`).
- Wenn `book.chapter_slug` im Frontmatter gesetzt: davor die Buch-Brücke (`{.book-bridge}`).

Validator warnt bei Verstößen, kommittet aber keine Errors — Legacy-Decks bleiben gültig.

---

## Stage-Patterns

Sieben Stage-Slide-Typen (alle dunkel, alle erfordern `background-color="#0a0a0f"`):

| Typ | Markdown-Skelett | Wann |
|---|---|---|
| **Opener** | `# Hook-Satz {.stage background-image="..." background-color="#0a0a0f" background-opacity="0.75"}` | Erste manuelle Folie. **Heading muss vom YAML-`title:` abweichen** — sonst entsteht eine Doppelung mit dem Quarto-Auto-Title-Slide (siehe `video-template.qmd`: YAML „Video-Titel" / Opener „Einstieg ins Thema"). Sinnvoll: ein Hook-Satz, eine Spannungsfrage oder ein Drei-Wort-Programm. |
| **Chapter-Opener** | `# Kapitel 02 · Werkzeuge {.stage .chapter background-color="#0a0a0f"}` mit `::: {.chapter-number}` und `::: {.chapter-title}` | Bei jedem `#`-Abschnitt |
| **Anschauung** | `# Die Bibliothekarin ohne Zutritt {.stage .anschauung background-image="..." background-color="#0a0a0f"}` | 1–3 pro Deck, wenn Konzept bildlich einrasten soll |
| **Breath** | `# {.stage .breath background-color="#0a0a0f"}` mit `::: {.big-word}` Ein Wort `:::` | Vor Aha-Momenten, sehr sparsam |
| **Closing-Beat** | `## Was bleibt {.stage .closing background-color="#0a0a0f"}` plus ein Body-Absatz | Letzte inhaltliche Folie. **H2 IST der Kicker-Label, der Body-Absatz ist der Schluss-Satz** — kein separater `.kicker`-Block. |
| **Big-Stat-Stage** | `## Titel {.stage}` mit `:::: {.big-stat .fragment .zoom-in-bounce}` | Wenn Evidenz den Rhythmus trägt |
| **Quote-Stage** | `## Titel {.stage}` mit `::: {.quote-box}` | Wenn eine Stimme pointieren soll |

### Anschauung-spezifisch

Punktuell, didaktisch — kein Designsystem. Detailregeln in [`prompts/anschauung-playbook.md`](prompts/anschauung-playbook.md): Zielgruppe-Anker (Business-Professionals), Tonalität (editorial, gedeckt), Beispieltabelle (Bibliothekarin / Projektleiterin / Fachredakteurin / ...), GPT-Image-2-Prompt-Template.

Slide-Titel der Anschauung-Folie ist immer **beschreibend**, nicht anredend (siehe Disziplin-Regel 1).

---

## Content-Patterns (Schreibtisch)

Alle Patterns mit lebendem Beispiel in [`elements.qmd`](elements.qmd). Zulässige Patterns:

- **Two-Column-Explainer** (`{.columns}` + `{.column width="50%"}`)
- **Media-Split** (45 % Bild / 55 % Text)
- **Metrics Grid** (`{.metrics-grid}` mit mehreren `.metric`)
- **Big-Stat** (eine dominante Zahl)
- **Feature Cards** (`{.features}`)
- **Timeline** (`{.timeline}`)
- **Comparison** (`{.comparison}`)
- **Quote Box** (`{.quote-box}`)
- **Formula** — zwei Varianten:
  - `{.formula}` (Default): Monospace-Schrift, **für Code-artige Gleichungen** (z. B. `Agenda + Template = Lernvideo`).
  - `{.formula .editorial}`: Inter-Schrift, etwas größer, gehobenes Tracking — **für Prosa-Merksätze und Thesen**. Beispiel: `Skalierungs-Probleme sind Design-Probleme — bevor sie zu Code werden.` Mono-Anmutung wäre hier deplatziert.
- **Numbered Sections** (`{.numbered-sections-container}`)
- **Animated List** (`{.animated-list}` für Bullets, `{.simple-animated-list}` ohne)
- **Neon Pill** (kleine Inline-Labels für Codezeilen-Erklärungen)

Visuelle Akzent-Optionen: `.accent-blue`, `.accent-green`, `.accent-orange`, `.accent-violet` für FontAwesome-Icons via `{{< fa <icon> >}}`.

Fragment-Effekte sparsam (max. 2 pro Folie): `.blur-focus`, `.zoom-in-bounce`, `.slide-up/down/left/right`. Staffelung über `.stagger-1` bis `.stagger-6`.

### Inline-Reflexion: Tip-Box und Think-Box

Zwei komplementäre Inline-Patterns für Content-Folien:

- `::: {.tip-box}` — eine handlungsleitende Einsicht in ein bis zwei Sätzen. Blauer Linkenrand, Pfeil-Icon. Maximal eine pro Folie.
- `::: {.think-box}` — eine reflektive Frage oder ein Gedankenexperiment. Warmes Cream, Ocker-Rahmen. Unterbricht den Informationsfluss bewusst.

**Pro Folie höchstens eine** dieser Boxen. Wenn sowohl Tipp als auch Reflexion: zwei Folien.

---

## Code-Display-Patterns

Für Folien mit Code ist `.codewindow` Pflicht — keine nackten Fenced-Code-Blöcke:

```markdown
::: {.codewindow .python width="420px"}

\`\`\`python
from google.adk import Agent
root_agent = Agent(name="coding_agent", model="gemini-2.0-flash")
\`\`\`

:::
```

Sprachen-Hint zwingend: `.python`, `.bash`, `.sql`, `.r`, `.js`, `.typescript`, `.yaml`, `.json`.
Breite proportional zur Spalte: ~`420px` bei 45 %-Spalte, `800px` bei Full-Width.

### Drei Code-Display-Patterns

1. **Code mit Zeilen-Erklärung** — Zwei-Spalten-Layout mit Codewindow links und `.neon-pill`-Liste rechts:

```markdown
:::: {.columns}
::: {.column width="45%"}
::: {.codewindow .python width="420px"}
\`\`\`python
# code
\`\`\`
:::
:::
::: {.column width="55%"}
- <span class="neon-pill">1.</span> kurze Erklärung
- <span class="neon-pill">3-5.</span> Bereich-Erklärung
:::
::::
```

2. **Code ohne Zeilen-Erklärung** — einspaltig, voll Breite, Erklärung in Speaker-Notes via TTS.

3. **Code in Media-Split mit D2** — drei Spalten: Diagramm (30 %) — Code (40 %) — Text (30 %).

### Progressive D2-Reveal

Komplexe Diagramme über **3–6 Folien aufbauen**, nicht fertig zeigen:

- Dateinamens-Konvention: `../d2/<slug>_1.d2` bis `<slug>_n.d2` (zentraler Repo-Ordner `d2/`)
- Pro Folie wächst das Diagramm um genau **einen Knoten oder eine Kante**
- Parallel wächst die Erklär-Liste um genau **einen Punkt**
- Jede Zwischenfolie muss für sich lesbar sein
- Eigene Speaker-Notes pro Folie

Konvention für **fertige** D2-Dateien: `direction: right` oder `down`, `shape: rectangle` (bzw. `diamond` für Verzweigungen), `border-radius: 8`. Buch und Slides teilen **dieselbe Palette** — siehe `AGENTS.md` im Repo-Root, Sektion „D2-Diagramme". Kurz: weiße Fills `#ffffff` mit dezentem Rahmen `#e4e4e7`, genau **ein** dunkler Akzent-Knoten (`fill: "#18181b"`, weiße Schrift), neutrale Kanten `#a1a1aa` mit `stroke-width: 2`. Keine weiteren Farben.

---

## Buch-Brücke

Wenn Frontmatter `book.chapter_slug` gesetzt ist, **muss** vor `## Literatur` die Folie `## Weiter im Buch {.book-bridge}` stehen — drei-spaltig, links ein Thumbnail (Profil `book-hero`), rechts der Kapitel-Titel + ein Zwei-Sätze-Teaser + ein Link zum Online-Buch.

Validator warnt, wenn `chapter_slug` ohne `.book-bridge` gesetzt ist.

---

## Bildgenerierung

### Bild-Prompt-Block-Syntax

Direkt **über** der Folie, die das Bild nutzt:

```
<!-- image: profile="<name>" file="<slug>.png"
<2–4 Sätze Prompt: Motiv + Komposition + Stil + Negativraum.
Ohne Text, ohne Menschen-Gesichter, große Negativfläche für Overlays.>
-->
```

**Ausnahme — Opener (allererstes `#`-Heading)**: hier muss der Image-Block **innerhalb** der Section direkt nach dem Heading stehen, **nicht davor**. Pandoc erzeugt sonst eine leere `<section>` aus dem Kommentar (er liegt vor dem ersten Heading und wird zu einer eigenen Folie). Beispiel:

```
# Opener-Titel {.stage background-image="..." ...}

<!-- image: profile="stage-hero" file="hero-opener.png"
... Prompt ...
-->

::: {.notes}
...
:::
```

Bei allen weiteren `#`/`##`-Folien bleibt der Block **über** dem Heading — er wird dann von der vorhergehenden Section absorbiert und erzeugt keine leere Folie.

Stage- / Hero-Folien referenzieren das Bild via `background-image="../images/<slug>.png"`.
Content-Folien (Media-Split) via `![](../images/<slug>.png)` in der 45 %-Bildspalte.

Bilder leben im **zentralen Repo-Ordner `images/`** auf Mono-Repo-Root — Buch und Slides ziehen aus derselben Quelle. Aus Slide-Subverzeichnissen (`slides/<modul>/<lesson>.qmd`) wird der Pfad entsprechend `../../images/<slug>.png`.

### Rollenbasierte Image-Profile (Standard)

Diese sechs Profile sind das Standardrepertoire:

| Profil | Rolle | Dateiname-Präfix |
|---|---|---|
| `stage-hero` | Opener / Chapter-Opener (dunkel-atmosphärisch) | `hero-<slug>.png` |
| `book-hero` | Buch-Kapitel-Opener (hell-editorial) | `book-hero-<slug>.png` |
| `anschauung` | Anschauung-Szene (full-bleed, business-Tonalität) | `anschauung-<slug>.png` |
| `annotated-diagram` | Schaubild im Media-Split | `diagram-<slug>.png` |
| `emotion-tile` | Breath-Folie / Closing (ein Objekt, viel Negativraum) | `tile-<slug>.png` |
| `content-support` | Inline-Bild (heller, dezenter) | `photo-<slug>.png` |

**Legacy-Profile** (`academic`, `minimal`, `agentic_ai_diagrams`) bleiben gültig für Kompatibilität, sind aber für **neue** Decks nicht mehr Standard.

### Bildmodell-Pfade

Beide Pfade nutzen dieselben Profile.

- **Pfad A — automatisch via Gemini 3 Pro Image**:
  ```
  uv run python scripts/generate_images.py <deck>.qmd
  ```
  Liest die `<!-- image: ... -->`-Blöcke, lädt das Profil, ruft Gemini auf, schreibt nach `../images/` (Mono-Repo-Root).

- **Pfad B — manuell via GPT-Image-2 in Codex/ChatGPT**:
  ```
  uv run python scripts/export_image_prompts.py <deck>.qmd
  ```
  Erzeugt `exports/image-prompts-<deck>.md` mit fertig zusammengebauten Prompts. Datei in Codex hineinkopieren, Bilder generieren lassen, manuell unter den vorgegebenen Dateinamen ins zentrale `../images/` (Mono-Repo-Root) ablegen.

### Anschauung-Bilder

Für jeden Anschauung-Slot zuerst [`prompts/anschauung-playbook.md`](prompts/anschauung-playbook.md) konsultieren — Zielgruppe-Anker, verbotene Tonalitäten, Prompt-Template, Beispieltabelle.

---

## Visuelle Sprache

### Typografie

Durchgängig **Inter** (Sans-Serif), Gewichte markieren den Ton:

- 400 Regular für Body
- 500 Medium für Zitate auf Stage
- 600 SemiBold für Closing-Beat
- 700 Bold für Chapter-Opener und Book-Bridge-Titel
- 800 ExtraBold für Anschauung-Titel

Keine Serif-Schriften im Blueprint.

### Farb- und Akzent-Regeln

- Auf **Stage-Folien**: maximal 1 Akzent pro Folie, meistens keiner. Bühne lebt von Ruhe.
- Auf **Buch-Brücke**: ausschließlich `$color-paper`, `$accent-editorial`, Schwarz — markiert den Medienwechsel zum Buch.
- Auf **Schreibtisch-Folien**: max. 2 der vier Accent-Farben (`accent-blue`, `accent-green`, `accent-orange`, `accent-violet`) gleichzeitig.

### D2-Diagramme

Konvention oben unter "Progressive D2-Reveal".

### Visualtyp-Entscheidung

- **D2-Diagramm** für Architekturen, Pipelines, Flows, Abhängigkeiten — alles mit Knoten und Kanten.
- **Static Diagram** (Profil `annotated-diagram`) für bildhafte Schaubilder ohne echte Graph-Struktur (2x2-Matrix, Quadranten, stilisierte Illustrationen).
- **FontAwesome** (`{{< fa <icon> >}}`) nur für einzelne Symbole in Feature-Cards, Badges oder Inline-Akzenten.
- **Anschauung-Bild** (Profil `anschauung`) für didaktische Analogie-Szenen.

---

## Theme-Konfiguration

Default ist **Variante A — Pure Platform-Mirror**: 1:1-Port der Lernplattform-DNA (Geist-Font, OKLch-Tokens, Cream-Paper, Ochre/Terracotta-Akzente, eine ruhige `editorial-rise`-Animation). Das alte **Premium-Blueprint-Theme** (Inter, weiße Hintergründe, Glow-Effekte, bouncy Animationen) bleibt als Override-Optik nutzbar.

| Aspekt | Default — Variante A (`redesign/`) | Override — Premium-Blueprint (`custom-new.scss`) |
|---|---|---|
| Font | Geist (via Google Fonts) | Inter |
| Hintergrund | Cream-Paper (`oklch(0.985 0.004 85)`) | Reinweiß |
| Akzente | Ochre, Terracotta, Plattform-Blau | Green, Violet, Blau, Orange |
| Karten | Outline-only, `--rule`-Border, **keine Schatten** | Schatten, Gradients, Glows |
| Animation | eine ruhige `editorial-rise` (fade + 8 px translateY) | bouncy (`zoom-in-bounce`, `typewriter`) |
| Charakter | „maximal ruhig", editorial | AI-Lab, Premium-Blueprint |

`custom-new.scss` bleibt unter A geladen — die Pattern-Klassen (`.feature`, `.timeline`, `.codewindow`, `.glow-circle`, `.fragment`-Animationen, `.book-bridge`, `.stage`) sind dort definiert. A überschreibt nur die globale Optik (Tokens, Title-Slide, Cards, Motion).

**Wann auf Premium-Blueprint umschalten:** wenn ein einzelnes Deck den AI-Lab-Look braucht (Stage-Folien mit Glow-Hero, dunkle Hintergründe mit Gradient-Title). Pro Deck per Frontmatter-Override:

```yaml
---
title: "Deck-Titel"
subtitle: "Untertitel"
title-slide-attributes:
  data-background-iframe: "includes/background-animation.html"
format:
  revealjs:
    theme:
      - default
      - custom-new.scss
    template-partials:
      - title-slide.html
    include-in-header:
      - includes/fonts.html
    include-after-body:
      - includes/footer-nav.html
---
```

Die Override-Felder spielen die `_metadata.yml`-Defaults zurück, die A leer lässt: animierter Hintergrund, custom Title-Slide-Layout, Inter-Font-Preconnect, Footer-Navigation.

**Lebende Demo für Pure A** (ohne `custom-new.scss`-Patterns, also wirklich nur die A-Optik): [`elements-redesign-a.qmd`](elements-redesign-a.qmd) bindet `redesign/_shared-content.qmd` ein.

---

## Quellen, Zitationen, Literatur

- Faktenlastige Folien bekommen einen `::: {.sources}`-Block mit Quelle am Folienende.
- Zitiert wird über Pandoc-Keys: `Quelle: @citationKey`. Der Key muss in `references.bib` existieren.
- Jedes Deck endet mit `## Literatur` und `::: {#refs}` + `:::` — das Literaturverzeichnis baut sich automatisch aus den im Deck zitierten Keys.

---

## Workflow im Detail

Standard ist Buch-First (siehe oben). Eine Lesson durchläuft zwei Phasen — erst der Generator, dann die Feinjustierung im Slide-Deck.

**Phase 1 — Generator-Lauf im Repo-Root:**

1. **Buch-Kapitel pflegen**: `<modul>/<lesson>.qmd` im Repo-Root in Wir-Form (siehe [`../AGENTS.md`](../AGENTS.md)).
2. **Generator laufen lassen**: `uv run python scripts/generate_slides.py` im Repo-Root. Output: `slides/<modul>/<lesson>.qmd` als Roh-Deck (Status-Callouts, TODO-Block und HTML-Kommentare bereits gestrippt).

**Phase 2 — Feinjustierung im Slide-Deck:**

1. **Generiertes Deck öffnen**: `slides/<modul>/<lesson>.qmd`. Buch-Kapitel parallel offen halten als Inhalts-Anker.
2. **Plane den Rhythmus** — siehe Choreographie oben. Opener (Stage), Desktop-Blöcke mit Stage-Momenten, Closing-Beat (Stage), optional Buch-Brücke.
3. **Identifiziere 1–3 Anschauung-Konzepte**. Konsultiere [`prompts/anschauung-playbook.md`](prompts/anschauung-playbook.md) für Tonalität und Motiv-Wahl.
4. **Wähle pro Folie ein Pattern** aus [`elements.qmd`](elements.qmd). Keine neuen CSS-Klassen.
5. **Bild-Blöcke** für Stage-Hero / Anschauung / Media-Split / Book-Bridge-Thumbnail. Profile aus dem Standardrepertoire (oben).
6. **Frontmatter ergänzen**: `book.chapter_slug` setzen, falls eine Buch-Brücke nötig ist.
7. **Speaker-Notes** pro Folie in indirekter Ansprache. Beim Übertrag aus Buch-Prosa: Wir-Form bewusst zu indirekter Ansprache umformulieren — nicht 1:1.
8. **Buch-Brücke** ergänzen, falls `chapter_slug` gesetzt.
9. **Validieren**: `uv run python scripts/validate_deck.py <modul>/<lesson>.qmd` aus `slides/`. Errors beheben, Warnings inhaltlich prüfen.
10. **Bilder erzeugen** über Pfad A (Gemini) oder Pfad B (Codex/GPT-Image-2).
11. **Rendern**: `quarto render slides/<modul>/<lesson>.qmd` aus dem Repo-Root. Sichtkontrolle im Browser.

Output an den Nutzer: nur die fertige `slides/<modul>/<lesson>.qmd`. Keine Meta-Erklärungen.

**Legacy: Agenda direkt zu Folien.** In Altfällen ohne Buch-Quelle (z. B. Einzel-Decks außerhalb der Lernplattform) gilt der alte Pfad: [`agenda-template.md`](agenda-template.md) als Eingabe-Vertrag, dann direkt `video-<slug>.qmd` schreiben. Im Mono-Repo-Kontext der Lernplattform ist dieser Pfad der Ausnahmefall, nicht die Regel.
