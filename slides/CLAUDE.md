# CLAUDE.md

Dieses Dokument adressiert Claude Code, Cursor, Cline, Aider und ähnliche Coding-Agenten, die nach `CLAUDE.md` im Verzeichnis suchen.

## Quelle der Wahrheit

Das **kanonische Regelwerk** für dieses Verzeichnis ist [`AGENTS.md`](AGENTS.md). Bitte zuerst dort lesen, bevor du Änderungen vornimmst oder Decks bearbeitest.

Diese Datei existiert nur, damit Tools, die `CLAUDE.md` automatisch laden, den richtigen Verweis finden — sie ist kein eigenständiges Regelwerk.

## Mono-Repo-Kontext

Dieses Verzeichnis (`slides/`) ist die **Slide-Welt** eines Mono-Repos. Die Buch-Welt liegt im Parent-Verzeichnis:

| Verzeichnis | Welt | AGENTS.md | Sprach-Stil |
|---|---|---|---|
| `..` (Repo-Root) | Buch | [`../AGENTS.md`](../AGENTS.md) | Wir-Form |
| `.` (`slides/`) | Folien | [`AGENTS.md`](AGENTS.md) | Indirekte Ansprache |

**Beim Übertrag von Buch zu Slide ist der Stilwechsel Pflicht.**

## Buch-First-Workflow ist Standard

Folien-Decks werden aus den Buch-Kapiteln generiert, nicht handgeschrieben. Pro Lesson zwei Phasen:

1. **Phase 1 — Generator-Lauf** (im Repo-Root, nicht in `slides/`): `uv run python scripts/generate_slides.py` erzeugt aus jedem Buch-Kapitel ein Roh-Deck unter `slides/<modul>/<lesson>.qmd`.
2. **Phase 2 — Feinjustierung** (hier in `slides/`): Stage-Patterns ergänzen, Speaker-Notes in indirekter Ansprache schreiben, Bild-Blöcke setzen, Pattern-Disziplin gemäß [`AGENTS.md`](AGENTS.md) durchziehen.

Vollständigen 11-Schritte-Workflow siehe Sektion „Workflow im Detail" in [`AGENTS.md`](AGENTS.md).

## Schnell-Orientierung

| Datei | Zweck |
|---|---|
| **[`AGENTS.md`](AGENTS.md)** | **Vollständiges Regelwerk.** Sprach-Stil, Patterns, Choreographie, Disziplin-Verbote, Bildgenerierung. Pflicht-Lektüre. |
| [`elements.qmd`](elements.qmd) | Pattern-Bibliothek mit gerenderten Beispielen. |
| [`video-template.qmd`](video-template.qmd) | Schablone für ein vollständiges Deck — als Referenz. |
| [`agenda-template.md`](agenda-template.md) | Legacy-Eingabe-Vertrag für Agenda-direkt-zu-Folien (Ausnahme-Pfad ohne Buch-Quelle). |
| [`prompts/anschauung-playbook.md`](prompts/anschauung-playbook.md) | Regelbuch für Anschauung-Bilder. |

## Wenn ich (KI) eine Lesson feinjustieren soll

1. Lese [`AGENTS.md`](AGENTS.md) komplett.
2. Öffne das Buch-Kapitel parallel als Inhalts-Anker (`../<modul>/<lesson>.qmd`).
3. Folge dem Phase-2-Workflow aus [`AGENTS.md`](AGENTS.md), Sektion „Workflow im Detail".
4. Liefere als Output **nur** die fertige `slides/<modul>/<lesson>.qmd`.

## Wenn ich (KI) am Repo selbst arbeite

- Bestehende Patterns in `elements.qmd` nicht löschen oder umbenennen.
- Neue CSS-Klassen niemals erfinden — wenn ein Pattern fehlt, erst Diskussion mit dem Nutzer.
- `scripts/qmd_utils.py` `ALLOWED_CLASSES` nicht ohne Pattern-Demo erweitern.
- Tests grün halten: `uv run pytest -q`.
- Validator grün halten: `uv run python scripts/validate_deck.py <deck>.qmd`.
- Vor Commit kurz prüfen, ob `quarto render` durchläuft (Buch im Repo-Root) bzw. `quarto render slides/<modul>/<lesson>.qmd` (einzelnes Deck).

## Wenn ich (KI) etwas Unerwartetes finde

Lieber nachfragen als raten. Lieber als BLOCKED reporten als halbgare Annahmen. AGENTS.md gewinnt bei Konflikt mit anderen Dokumenten.
