# slides/ — Lernplattform-Decks

Dieses Verzeichnis hält die aus den Buch-Modulen abgeleiteten Workshop-Decks der Lernplattform, ein `.qmd` pro Modul auf gleicher Ebene (z. B. `agentic-ai.qmd` zum gleichnamigen Buch-Modul). Das kanonische Regelwerk ist [`AGENTS.md`](AGENTS.md), die Pattern-Bibliothek liegt in [`elements.qmd`](elements.qmd), und das Vorbild für neue Module ist [`agentic-ai.qmd`](agentic-ai.qmd): Opener-Stage plus acht Chapter-Opener mit jeweils 3 bis 5 Desktop-Folien, eingestreuten Anschauung-Stages, Closing-Beat, Buch-Brücke und Literatur.

Pflicht vor jedem Commit: `uv run python scripts/validate_deck.py <deck>.qmd` und `quarto render slides/<deck>.qmd` aus dem Repo-Root, plus ein Cross-Check, dass alle im Deck zitierten Keys in `slides/references.bib` existieren (die Slides-bib ist eigenständig und wird bei Bedarf aus der Root-`references.bib` ergänzt).
