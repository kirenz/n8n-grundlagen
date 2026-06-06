from pathlib import Path
import json
import textwrap
import pytest


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def profile_dir(repo_root: Path) -> Path:
    return repo_root / "profiles"


@pytest.fixture
def fake_repo(tmp_path: Path) -> Path:
    """Create a minimal fake repo with _quarto.yml, a deck, and one profile."""
    (tmp_path / "_quarto.yml").write_text("project:\n  type: default\n")
    (tmp_path / "profiles").mkdir()
    (tmp_path / "profiles" / "test-profile.json").write_text(json.dumps({
        "name": "test-profile",
        "style_instructions": "Editorial style",
        "composition": "Subject lower-right",
        "negative": "no text",
        "aspect_ratio": "16:9",
        "resolution": "2K",
    }))
    (tmp_path / "images").mkdir()
    (tmp_path / "exports").mkdir()
    deck = tmp_path / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        ---
        title: Deck
        ---

        <!-- image: profile="test-profile" file="hero-one.png"
        A scene of a librarian in a quiet reading room.
        -->

        # Opener {background-image="images/hero-one.png"}

        ::: {.notes}
        Intro.
        :::
    """).lstrip())
    return tmp_path
