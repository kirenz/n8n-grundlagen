#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

from qmd_utils import clean_notes_text, parse_slides


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/export_speaker_notes.py <deck.qmd>", file=sys.stderr)
        return 2

    deck_path = Path(sys.argv[1]).resolve()
    if not deck_path.exists():
        print(f"Deck nicht gefunden: {deck_path}", file=sys.stderr)
        return 1

    try:
        slides = parse_slides(deck_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    export_rows = []
    for slide in slides:
        voice_text, stage_cues = clean_notes_text(slide.notes_lines)
        export_rows.append(
            {
                "slide_number": slide.index,
                "slide_title": slide.title,
                "voice_text": voice_text,
                "stage_cues": stage_cues,
            }
        )

    export_dir = deck_path.parent / "exports"
    export_dir.mkdir(exist_ok=True)
    export_path = export_dir / f"{deck_path.stem}-notes.json"
    export_path.write_text(
        json.dumps(export_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Speaker Notes exportiert nach {export_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
