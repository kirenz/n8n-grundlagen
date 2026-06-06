#!/usr/bin/env python3
"""Export fully assembled image prompts from a Quarto deck as Markdown.

Reads all `<!-- image: profile=... file=... -->` blocks, loads the matching
profile from ``profiles/<name>.json``, and writes a Markdown file to
``exports/image-prompts-<deck-stem>.md`` containing the fully assembled
prompt (style + composition + mood + negative + user prompt).

This gives the user a ready-to-paste prompt per image for manual generation
in Codex / ChatGPT (GPT-Image-2), as an alternative to the automated Gemini
path in ``generate_images.py``.

Usage::

    uv run python scripts/export_image_prompts.py <deck.qmd>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from qmd_utils import assemble_prompt, extract_image_prompts, find_repo_root


def load_profile(profile_dir: Path, name: str) -> dict:
    path = profile_dir / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Profil nicht gefunden: {path} — verfuegbar: "
            + ", ".join(sorted(p.stem for p in profile_dir.glob("*.json")))
        )
    return json.loads(path.read_text(encoding="utf-8"))


def render_markdown(deck_name: str, entries: list[dict]) -> str:
    lines: list[str] = [
        f"# Image Prompts for {deck_name}",
        "",
        "Paste each prompt into Codex / ChatGPT with GPT-Image-2. "
        "Save the generated image under the exact filename into `images/`.",
        "",
    ]
    for entry in entries:
        lines.append(f"## `images/{entry['file']}`")
        lines.append(
            f"Profile: `{entry['profile']}` · "
            f"Aspect ratio: `{entry['aspect_ratio']}` · "
            f"Resolution: `{entry['resolution']}`"
        )
        lines.append("")
        lines.append("```")
        lines.append(entry["assembled"])
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="Pfad zum .qmd Deck")
    args = parser.parse_args()

    deck_path = args.deck.resolve()
    if not deck_path.exists():
        print(f"Deck nicht gefunden: {deck_path}", file=sys.stderr)
        return 1

    repo_root = find_repo_root(deck_path)
    profile_dir = repo_root / "profiles"
    exports_dir = repo_root / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    try:
        specs = extract_image_prompts(deck_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not specs:
        print(f"{deck_path.name}: keine <!-- image: --> Bloecke gefunden.")
        return 0

    entries: list[dict] = []
    for spec in specs:
        profile = load_profile(profile_dir, spec["profile"])
        entries.append({
            "file": spec["file"],
            "profile": spec["profile"],
            "aspect_ratio": profile.get("aspect_ratio", "16:9"),
            "resolution": profile.get("resolution", "2K"),
            "assembled": assemble_prompt(spec["prompt"], profile),
        })

    out_path = exports_dir / f"image-prompts-{deck_path.stem}.md"
    out_path.write_text(render_markdown(deck_path.name, entries), encoding="utf-8")
    print(f"{deck_path.name}: {len(entries)} Prompt(s) -> {out_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
