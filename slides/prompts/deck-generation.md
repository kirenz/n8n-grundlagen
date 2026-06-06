# Deck-Generierungs-Workflow

Aufruf-Pfad für jede KI, die in diesem Repo aus einer Agenda ein Deck erzeugen soll. Dieses Dokument ist **bewusst kurz** — es verweist auf die kanonischen Quellen statt sie zu duplizieren.

## Pflicht-Lektüre vor dem Schreiben

In dieser Reihenfolge:

1. **[`AGENTS.md`](../AGENTS.md)** — komplett. Enthält alle verbindlichen Regeln (Sprach-Stil, Highlight-Semantik, Key-Badge-Pflicht, Patterns, Choreographie, Verbote). Bei Widerspruch zu anderen Dokumenten gilt AGENTS.md.
2. **[`elements.qmd`](../elements.qmd)** — als Pattern-Referenz. Jedes erlaubte Slide-Pattern dort als Beispiel mit Speaker-Notes.
3. **[`prompts/anschauung-playbook.md`](anschauung-playbook.md)** — für jeden Anschauung-Slot Pflicht.
4. **[`slides-template.qmd`](../slides-template.qmd)** — kanonisches Starter-Deck als Vorbild für Frontmatter, Rhythmus und Speaker-Notes-Stil.

## Rolle

Quarto-RevealJS-Deck-Autor:in im Stil des Premium-Blueprints dieses Repos. Output ist ein renderbares `video-<slug>.qmd`.

## Aufgabe

Aus der übergebenen Agenda (`agenda-template.md`-Format oder freier Text) ein neues `video-<slug>.qmd` schreiben, das alle Regeln aus AGENTS.md erfüllt.

## Vorgehen (9 Schritte)

1. **Agenda lesen.** Wenn Felder fehlen, beim Nutzer nachfragen — nicht raten.
2. **Rhythmus planen** vor dem Schreiben einzelner Folien (siehe AGENTS.md → Choreographie):
   - Opener als Stage-Folie (`# Titel {.stage background-image="..." background-color="#0a0a0f" background-opacity="0.75"}`).
   - Desktop-Blöcke (3–5 helle `##`-Folien) abwechselnd mit Stage-Momenten (Big-Stat-Stage, Quote-Stage, Anschauung, Breath, Chapter-Opener).
   - Closing-Beat als letzte inhaltliche Folie (`## Was bleibt {.stage .closing background-color="#0a0a0f"}`).
   - Optional Buch-Brücke (`## Weiter im Buch {.book-bridge}`) vor `## Literatur`, wenn Frontmatter `book.chapter_slug` gesetzt ist.
3. **1–3 Anschauung-Slots identifizieren** — Konzepte, die ohne vivid-Example-Bild nicht zünden. Pro Slot Motiv via [`prompts/anschauung-playbook.md`](anschauung-playbook.md) wählen. **Niemals mehr als drei** Anschauung-Folien pro Deck.
4. **Pro Folie ein Pattern wählen** aus [`elements.qmd`](../elements.qmd). Keine neuen CSS-Klassen erfinden, keine Layout-Experimente.
5. **Bild-Blöcke ergänzen** für Stage-Opener, Chapter-Opener, Anschauung, Media-Split, Buch-Brücke-Thumbnail. Syntax direkt über der Folie:
   ```
   <!-- image: profile="<name>" file="<slug>.png"
   2–4 Sätze: Motiv + Komposition + Stil + Negativraum.
   -->
   ```
   Profile aus dem Standardrepertoire (`stage-hero`, `book-hero`, `anschauung`, `annotated-diagram`, `emotion-tile`, `content-support` — siehe AGENTS.md → Bildgenerierung).
6. **Speaker-Notes pro Folie** als `::: {.notes}`-Block direkt unter der Folie. Vollständig formuliert, **immer in indirekter Ansprache** (siehe AGENTS.md → Disziplin-Regel 1). Regiehinweise nur in eckigen Klammern (`[KLICK]`, `[PAUSE]`).
7. **Quellen** für Zahlen / Studien / Behauptungen via `Quelle: @citationKey` im `::: {.sources}`-Block. Keys müssen in `references.bib` existieren.
8. **Validieren**: `uv run python scripts/validate_deck.py video-<slug>.qmd`. Errors beheben, Warnings (Rhythmus, Buch-Brücke) prüfen.
9. **Bilder generieren** — Pfad A (Gemini, automatisch) oder Pfad B (GPT-Image-2 via Codex):
   - `uv run python scripts/generate_images.py video-<slug>.qmd`
   - oder `uv run python scripts/export_image_prompts.py video-<slug>.qmd` und die `exports/image-prompts-<slug>.md` in Codex bearbeiten.
   Anschließend `quarto render video-<slug>.qmd`.

## Ausgabeformat

- Liefere **nur den Inhalt** der finalen `video-<slug>.qmd`.
- Keine Erklärung außerhalb des QMD.
- Keine Meta-Kommentare zum Workflow oder zur Technik in den Notes-Blöcken.
- Frontmatter entsprechend dem Muster in `slides-template.qmd`.

## Was zu vermeiden ist

Kurz-Übersicht; vollständige Liste in AGENTS.md → Disziplin-Verbote.

- Keine direkte Anrede (kein "du", "Sie", "man").
- Keine neuen CSS-Klassen oder Layouts.
- Mehr als 2 Inline-Highlights pro Folie.
- Cartoon-Emojis (🚀 💻 🎉) in CTAs.
- Typewriter-Effekte auf Fließtext.
- Absolute-positionierte Icons mit Pixel-Koordinaten.
- Mehr als 2 Fragment-Animations-Klassen pro Folie.
- Stage-Folien ohne `background-color="#0a0a0f"`.
