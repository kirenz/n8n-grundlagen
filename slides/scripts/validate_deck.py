#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from qmd_utils import (
    ALLOWED_CLASSES,
    PROJECT_FILE_REFS,
    extract_classes,
    extract_image_prompts,
    extract_local_references,
    find_repo_root,
    parse_slides,
    resolve_reference,
)


def _check_rhythm(slides: list) -> list[str]:
    """Return warnings (not errors) for stage-rhythm violations."""
    from qmd_utils import slide_is_stage  # local import avoids circular
    warnings: list[str] = []

    # Rule 1: first slide must be stage or have background-image.
    if slides and not slide_is_stage(slides[0]):
        warnings.append("Erste Folie ist keine Stage-Folie (Opener sollte `.stage` oder `background-image=` tragen).")

    # Rule 2: at least one stage slide per 5 content slides (walking window).
    desktop_streak = 0
    for slide in slides:
        if slide_is_stage(slide):
            desktop_streak = 0
        else:
            desktop_streak += 1
            if desktop_streak > 5:
                warnings.append(
                    f"Rhythmus: Folie {slide.index} liegt in einer Serie von >5 Desktop-Folien ohne Stage-Moment."
                )
                desktop_streak = 0  # avoid spam, reset

    # Rule 3: no more than 2 consecutive stage slides.
    stage_streak = 0
    for slide in slides:
        if slide_is_stage(slide):
            stage_streak += 1
            if stage_streak > 2:
                warnings.append(
                    f"Rhythmus: Folie {slide.index} ist Teil von >2 aufeinanderfolgenden Stage-Folien."
                )
                stage_streak = 0
        else:
            stage_streak = 0

    return warnings


def _check_no_image_block_before_first_heading(deck_text: str) -> list[str]:
    """Forbid `<!-- image: ... -->` blocks before the first `#` heading.

    Pandoc wraps any non-heading content above the first heading into its own
    `<section>`. If that content is just an image-prompt comment, the result
    is an orphan empty slide between the auto-generated title slide and the
    real opener. The opener's image-prompt must therefore live INSIDE the
    opener section, directly after its heading.
    """
    import re as _re
    body = deck_text
    if body.startswith("---\n"):
        parts = body.split("\n---\n", 1)
        if len(parts) == 2:
            body = parts[1]
    first_heading_match = _re.search(r"(?m)^#{1,2}\s+\S", body)
    if not first_heading_match:
        return []
    head_region = body[: first_heading_match.start()]
    image_block = _re.search(r"<!--\s*image:\s*", head_region)
    if image_block:
        return [
            "Opener-Image-Block liegt VOR dem ersten `#`-Heading. "
            "Pandoc erzeugt daraus eine leere Folie zwischen Titel-Slide und Opener. "
            "Block stattdessen direkt nach der Opener-Heading-Zeile platzieren."
        ]
    return []


def _check_no_subheadings_in_body(slides: list) -> list[str]:
    """Forbid `###`+ headings inside slide bodies.

    Pandoc renders any `###` heading as a nested `<section>` element, even
    when it sits inside a `:::` div. Reveal.js then treats those as vertical
    sub-slides, which silently breaks horizontal navigation. The deck still
    renders, the validator stays green, but `Right` arrow skips slides.

    Use `**Bold**` paragraphs for visual sub-headings inside content blocks
    (e.g. inside `.comparison-side`, `.feature`, `.column`).
    """
    import re as _re
    fence_re = _re.compile(r"^```")
    bad_heading_re = _re.compile(r"^(#{3,6})\s+\S")
    errors: list[str] = []
    for slide in slides:
        in_code = False
        for offset, line in enumerate(slide.content_lines):
            if fence_re.match(line):
                in_code = not in_code
                continue
            if in_code:
                continue
            match = bad_heading_re.match(line)
            if match:
                line_no = slide.heading_line + 1 + offset
                errors.append(
                    f"Folie {slide.index} (`{slide.title}`), Zeile {line_no}: "
                    f"`{match.group(1)}`-Heading im Folien-Body. "
                    f"Pandoc rendert das als verschachteltes `<section>`, was Reveal.js-"
                    f"Navigation bricht. Stattdessen `**{line.strip().lstrip('#').strip()}**` "
                    f"als Bold-Absatz nutzen."
                )
    return errors


def _check_book_bridge(deck_text: str, slides: list) -> list[str]:
    from qmd_utils import extract_frontmatter, slide_is_book_bridge
    warnings: list[str] = []
    fm = extract_frontmatter(deck_text)
    chapter_slug = (fm.get("book") or {}).get("chapter_slug")
    if not chapter_slug:
        return warnings

    bridge_seen = False
    for slide in slides:
        if slide_is_book_bridge(slide):
            bridge_seen = True
            break
    if not bridge_seen:
        warnings.append(
            "Buch-Brücke fehlt: Deck setzt `book.chapter_slug`, aber es gibt keine Folie mit `.book-bridge`."
        )
    return warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_deck.py <deck.qmd>", file=sys.stderr)
        return 2

    deck_path = Path(sys.argv[1]).resolve()
    if not deck_path.exists():
        print(f"Deck nicht gefunden: {deck_path}", file=sys.stderr)
        return 1

    errors: list[str] = []

    try:
        slides = parse_slides(deck_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if any(slide.level not in (1, 2) for slide in slides):
        errors.append("Nur `#` und `##` duerfen als Slide-Heading verwendet werden.")

    deck_text = deck_path.read_text(encoding="utf-8")
    classes = extract_classes(deck_text)
    disallowed = sorted(name for name in classes if name not in ALLOWED_CLASSES)
    if disallowed:
        errors.append(
            "Nicht erlaubte Klassen gefunden: " + ", ".join(disallowed)
        )

    try:
        image_prompts = extract_image_prompts(deck_text)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    managed_images = {entry["file"] for entry in image_prompts}
    pending_managed: list[str] = []

    repo_root = find_repo_root(deck_path)
    profile_dir = repo_root / "profiles"
    for entry in image_prompts:
        profile_file = profile_dir / f"{entry['profile']}.json"
        if not profile_file.exists():
            errors.append(
                f"Unbekanntes Bild-Profil `{entry['profile']}` fuer {entry['file']}"
                f" — erwartet wird {profile_file.relative_to(repo_root)}."
            )

    for ref in sorted(extract_local_references(deck_text)):
        if resolve_reference(deck_path.parent, ref).exists():
            continue
        if Path(ref).name in managed_images:
            pending_managed.append(ref)
        else:
            errors.append(f"Fehlende lokale Referenz in Deck: {ref}")

    quarto_path = repo_root / "_quarto.yml"
    if quarto_path.exists():
        quarto_text = quarto_path.read_text(encoding="utf-8")
        for ref in sorted(extract_local_references(quarto_text)):
            if not resolve_reference(repo_root, ref).exists():
                errors.append(f"Fehlende Referenz in _quarto.yml: {ref}")
    for project_ref in PROJECT_FILE_REFS:
        if not (repo_root / project_ref).exists():
            errors.append(f"Projektdatei fehlt: {project_ref}")

    for slide in slides:
        if not any(line.strip() for line in slide.notes_lines):
            errors.append(f"Folie {slide.index} (`{slide.title}`) hat leere Speaker Notes.")

    errors.extend(_check_no_subheadings_in_body(slides))
    errors.extend(_check_no_image_block_before_first_heading(deck_text))

    warnings = _check_rhythm(slides)
    warnings.extend(_check_book_bridge(deck_text, slides))
    for warning in warnings:
        print(f"WARN: {warning}")

    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{deck_path.name}: {len(slides)} Folien erfolgreich validiert.")
    if pending_managed:
        print(
            f"  Hinweis: {len(pending_managed)} generierbare Bild(er) noch nicht vorhanden"
            f" — `uv run python scripts/generate_images.py {deck_path.name}` ausfuehren:"
        )
        for ref in pending_managed:
            print(f"    - {ref}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
