import subprocess
import sys
from pathlib import Path


def run_export(repo: Path, deck_name: str) -> subprocess.CompletedProcess:
    script = Path(__file__).resolve().parent.parent / "scripts" / "export_image_prompts.py"
    return subprocess.run(
        [sys.executable, str(script), deck_name],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def test_exports_to_markdown_file(fake_repo: Path):
    result = run_export(fake_repo, "deck.qmd")
    assert result.returncode == 0, result.stderr
    out_file = fake_repo / "exports" / "image-prompts-deck.md"
    assert out_file.exists()


def test_export_contains_full_assembled_prompt(fake_repo: Path):
    run_export(fake_repo, "deck.qmd")
    content = (fake_repo / "exports" / "image-prompts-deck.md").read_text()
    assert "images/hero-one.png" in content
    assert "test-profile" in content
    assert "Subject: A scene of a librarian" in content
    assert "Style: Editorial style" in content
    assert "Composition: Subject lower-right" in content
    assert "Negative: no text" in content


def test_export_lists_aspect_ratio_and_resolution(fake_repo: Path):
    run_export(fake_repo, "deck.qmd")
    content = (fake_repo / "exports" / "image-prompts-deck.md").read_text()
    assert "16:9" in content
    assert "2K" in content


def test_returns_1_when_deck_missing(fake_repo: Path):
    result = run_export(fake_repo, "missing.qmd")
    assert result.returncode == 1
