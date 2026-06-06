import textwrap
from pathlib import Path
from qmd_utils import parse_slides, slide_is_stage, slide_is_book_bridge


def _write(tmp_path: Path, content: str) -> Path:
    deck = tmp_path / "t.qmd"
    deck.write_text(textwrap.dedent(content).lstrip())
    return deck


def test_slide_is_stage_true_when_class_present(tmp_path: Path):
    deck = _write(tmp_path, """
        # Opener {.stage}

        ::: {.notes}
        Hi.
        :::
    """)
    slides = parse_slides(deck)
    assert slide_is_stage(slides[0]) is True


def test_slide_is_stage_true_when_background_image_set(tmp_path: Path):
    deck = _write(tmp_path, """
        # Opener {background-image="images/hero.png"}

        ::: {.notes}
        Hi.
        :::
    """)
    slides = parse_slides(deck)
    assert slide_is_stage(slides[0]) is True


def test_slide_is_stage_false_for_plain_slide(tmp_path: Path):
    deck = _write(tmp_path, """
        ## Plain content

        Some text.

        ::: {.notes}
        Notes.
        :::
    """)
    slides = parse_slides(deck)
    assert slide_is_stage(slides[0]) is False


def test_slide_is_book_bridge(tmp_path: Path):
    deck = _write(tmp_path, """
        ## Weiter im Buch {.book-bridge}

        Link.

        ::: {.notes}
        Hinweis.
        :::
    """)
    slides = parse_slides(deck)
    assert slide_is_book_bridge(slides[0]) is True
