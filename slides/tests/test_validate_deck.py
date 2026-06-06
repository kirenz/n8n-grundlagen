import subprocess
import sys
import textwrap
from pathlib import Path


def run_validate(repo: Path, deck_name: str) -> subprocess.CompletedProcess:
    script = Path(__file__).resolve().parent.parent / "scripts" / "validate_deck.py"
    return subprocess.run(
        [sys.executable, str(script), deck_name],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def _minimal_fake_repo(tmp_path: Path) -> Path:
    (tmp_path / "_quarto.yml").write_text("project:\n  type: default\n")
    (tmp_path / "profiles").mkdir()
    # Create dummy profiles so existing profile-validation passes:
    for name in ["stage-hero", "content-support"]:
        (tmp_path / "profiles" / f"{name}.json").write_text(
            '{"name": "%s", "style_instructions": "x"}' % name
        )
    # Satisfy PROJECT_FILE_REFS existence checks:
    (tmp_path / "custom-new.scss").write_text("")
    (tmp_path / "title-slide.html").write_text("")
    (tmp_path / "references.bib").write_text("")
    (tmp_path / "includes").mkdir()
    (tmp_path / "includes" / "footer-nav.html").write_text("")
    (tmp_path / "includes" / "background-animation.html").write_text("")
    return tmp_path


def test_rhythm_warning_when_too_many_desktop_in_row(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::

        ## D1

        x

        ::: {.notes}
        x
        :::

        ## D2

        x

        ::: {.notes}
        x
        :::

        ## D3

        x

        ::: {.notes}
        x
        :::

        ## D4

        x

        ::: {.notes}
        x
        :::

        ## D5

        x

        ::: {.notes}
        x
        :::

        ## D6

        x

        ::: {.notes}
        x
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    # Should exit 0 (no errors) but print warning about rhythm
    assert "Rhythmus" in (result.stdout + result.stderr)


def test_no_rhythm_warning_when_stage_every_4_slides(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::

        ## D1

        ::: {.notes}
        x
        :::

        ## D2

        ::: {.notes}
        x
        :::

        ## Stage1 {.stage}

        ::: {.notes}
        x
        :::

        ## D3

        ::: {.notes}
        x
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    assert "Rhythmus" not in (result.stdout + result.stderr)


def test_book_bridge_required_when_chapter_slug_set(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        ---
        title: T
        book:
          chapter_slug: foo
        ---

        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::

        ## Literatur

        ::: {.notes}
        Refs.
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    combined = result.stdout + result.stderr
    assert "Buch-Brücke" in combined or "book-bridge" in combined.lower()


def test_h3_in_slide_body_is_rejected(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::

        ## Vergleich

        :::: {.comparison}

        ::: {.comparison-side}
        ### Linke Seite

        - Punkt A
        :::

        ::: {.comparison-side .highlighted}
        ### Rechte Seite

        - Punkt B
        :::

        ::::

        ::: {.notes}
        x
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    combined = result.stdout + result.stderr
    assert result.returncode != 0, combined
    assert "###" in combined or "verschachtelt" in combined.lower()


def test_image_block_before_first_heading_is_rejected(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        <!-- image: profile="stage-hero" file="hero-opener.png"
        Some prompt.
        -->

        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    combined = result.stdout + result.stderr
    assert result.returncode != 0, combined
    assert "Opener-Image-Block" in combined or "leere Folie" in combined


def test_image_block_inside_opener_is_allowed(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        # Opener {.stage}

        <!-- image: profile="stage-hero" file="hero-opener.png"
        Some prompt.
        -->

        ::: {.notes}
        Hi.
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined


def test_h3_inside_fenced_code_is_allowed(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::

        ## Code-Beispiel

        ```markdown
        ### Diese Überschrift ist nur Beispielcode
        ```

        ::: {.notes}
        x
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined


def test_book_bridge_not_required_when_no_chapter_slug(tmp_path: Path):
    repo = _minimal_fake_repo(tmp_path)
    deck = repo / "deck.qmd"
    deck.write_text(textwrap.dedent("""
        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::

        ## Literatur

        ::: {.notes}
        Refs.
        :::
    """).lstrip())
    result = run_validate(repo, "deck.qmd")
    combined = result.stdout + result.stderr
    assert "Buch-Brücke" not in combined
