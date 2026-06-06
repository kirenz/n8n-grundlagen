#!/usr/bin/env python3
"""Generate slide images for a Quarto deck from image-prompt blocks.

The deck declares each image via a single HTML comment above the slide
content::

    <!-- image: profile="academic" file="hero-einstieg.png"
    A minimalist scholarly illustration with a desktop computer and
    scattered geometric shapes. No text, no people.
    -->

This script parses every such block, loads the matching profile from
``profiles/<name>.json``, calls Gemini 3 Pro Image via the google-genai
SDK, and writes the PNG to ``images/<file>``. Existing files are
cached unless ``--force`` is passed.

Usage::

    uv run python scripts/generate_images.py <deck.qmd> [--force] [--dry-run]
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

from qmd_utils import assemble_prompt, extract_image_prompts, find_repo_root


def load_profile(profile_dir: Path, name: str) -> dict:
    path = profile_dir / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Profil nicht gefunden: {path} — verfuegbar: "
            + ", ".join(sorted(p.stem for p in profile_dir.glob("*.json")))
        )
    return json.loads(path.read_text(encoding="utf-8"))



def generate_one(client: genai.Client, prompt: str, profile: dict, out_path: Path) -> None:
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=profile.get("aspect_ratio", "16:9"),
                image_size=profile.get("resolution", "2K"),
            ),
        ),
    )
    for part in response.parts:
        if getattr(part, "inline_data", None):
            image = Image.open(io.BytesIO(part.inline_data.data))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(out_path)
            return
    raise RuntimeError(f"Gemini lieferte kein Bild fuer {out_path.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="Pfad zum .qmd Deck")
    parser.add_argument("--force", action="store_true", help="vorhandene Bilder neu generieren")
    parser.add_argument("--dry-run", action="store_true", help="nur anzeigen, was generiert wuerde")
    args = parser.parse_args()

    deck_path = args.deck.resolve()
    if not deck_path.exists():
        print(f"Deck nicht gefunden: {deck_path}", file=sys.stderr)
        return 1

    repo_root = find_repo_root(deck_path)
    profile_dir = repo_root / "profiles"
    images_dir = repo_root / "images"

    try:
        specs = extract_image_prompts(deck_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not specs:
        print(f"{deck_path.name}: keine <!-- image: --> Bloecke gefunden.")
        return 0

    if args.dry_run:
        for spec in specs:
            out = images_dir / spec["file"]
            marker = "exists" if out.exists() else "missing"
            print(f"[{marker}] {spec['profile']} -> {out.relative_to(repo_root)}")
            first_line = spec["prompt"].splitlines()[0]
            print(f"  {first_line[:100]}{'...' if len(first_line) > 100 else ''}")
        return 0

    load_dotenv(repo_root / ".env")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(
            "GOOGLE_API_KEY fehlt. Lege .env nach Vorlage .env.example an.",
            file=sys.stderr,
        )
        return 1

    client = genai.Client(api_key=api_key)

    generated = skipped = 0
    for spec in specs:
        out_path = images_dir / spec["file"]
        if out_path.exists() and not args.force:
            print(f"skip (exists): {spec['file']}")
            skipped += 1
            continue

        profile = load_profile(profile_dir, spec["profile"])
        prompt = assemble_prompt(spec["prompt"], profile)
        print(f"generate: {spec['profile']} -> {spec['file']}")
        try:
            generate_one(client, prompt, profile, out_path)
        except Exception as exc:
            print(f"  Fehler: {exc}", file=sys.stderr)
            return 1
        generated += 1

    print(f"\n{deck_path.name}: {generated} generiert, {skipped} uebersprungen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
