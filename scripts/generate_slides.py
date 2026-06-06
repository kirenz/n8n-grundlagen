"""Generiert Reveal.js-Folien-Decks aus den Buch-Kapiteln.

Stub-Implementierung — adaptiert das Muster aus
`books/data-science-de/create_slides.py`.

Workflow:
    1. Liest jedes `.qmd` aus den Modul-Verzeichnissen
    2. Entfernt die `Status — Erstentwurf`-Callouts
    3. Verdichtet `.callout-*`-Blöcke zu Stichpunkten
    4. Demoted H3/H4 zu H2 für Reveal.js-Sektionen
    5. Schreibt das Ergebnis nach `slides/<modul>/<lesson>.qmd`

Aktuell ist die Verdichtungs-Logik bewusst minimal — die produktive Version
wird parallel zur Entwicklung der Decks im Repo `kurse/n8n-ai-agents`
ausgearbeitet, sobald die Buch-Kapitel auf Vollausbau-Niveau sind.

Aufruf:
    uv run python scripts/generate_slides.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "slides"

MODULE_DIRS = [
    "positionierung",
    "erste-workflows",
    "integrationen",
    "ki-im-workflow",
    "rag",
    "production",
]

REVEAL_FRONTMATTER = """---
title: {title}
subtitle: {subtitle}
author: Jan Kirenz
lang: de
format:
  revealjs:
    theme: [default, custom.scss]
    incremental: true
    transition: slide
    code-copy: true
    slide-number: c
    preview-links: auto
    chalkboard:
      buttons: false
    footer: "n8n-Grundlagen | Jan Kirenz"
---
"""

STATUS_CALLOUT_RE = re.compile(
    r":::\s*\{\.callout-note\s+title=\"Status — Erstentwurf\"\}.*?:::",
    re.DOTALL,
)
TODO_BLOCK_RE = re.compile(
    r"##\s+Was als Nächstes ausgebaut werden muss.*$",
    re.DOTALL | re.MULTILINE,
)


def process_chapter(input_path: Path, module_slug: str) -> None:
    """Liest ein Buch-Kapitel und schreibt das abgeleitete Deck."""
    text = input_path.read_text(encoding="utf-8")

    # Status-Callout und TODO-Liste raus — gehört nicht ins Deck
    text = STATUS_CALLOUT_RE.sub("", text)
    text = TODO_BLOCK_RE.sub("", text)

    # H1 als Titel extrahieren, Body danach
    h1_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if not h1_match:
        print(f"  [skip] {input_path.name}: kein H1 gefunden")
        return

    title = h1_match.group(1).strip()
    body = text[h1_match.end():].lstrip()

    # H3 → H2, H4 → H3 (Reveal.js zeigt H2 als neue Folie)
    body = re.sub(r"^####\s+", "### ", body, flags=re.MULTILINE)
    body = re.sub(r"^###\s+", "## ", body, flags=re.MULTILINE)

    # Frontmatter zusammenbauen
    frontmatter = REVEAL_FRONTMATTER.format(
        title=title,
        subtitle=f"Modul: {module_slug}",
    )

    # Output-Pfad
    output_dir = OUTPUT_DIR / module_slug
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / input_path.name

    output_path.write_text(frontmatter + "\n" + body, encoding="utf-8")
    print(f"  [ok]   {input_path.name} → {output_path.relative_to(ROOT)}")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    for module_slug in MODULE_DIRS:
        module_dir = ROOT / module_slug
        if not module_dir.is_dir():
            continue

        print(f"Modul: {module_slug}")
        for qmd in sorted(module_dir.glob("*.qmd")):
            if qmd.name == "index.qmd":
                continue
            process_chapter(qmd, module_slug)

    print(f"\nFolien-Decks geschrieben nach {OUTPUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
