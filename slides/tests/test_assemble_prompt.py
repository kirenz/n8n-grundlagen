from qmd_utils import assemble_prompt


def test_minimal_profile_style_only():
    result = assemble_prompt(
        user_prompt="A library scene",
        profile={"style_instructions": "Editorial photography"},
    )
    assert "Subject: A library scene" in result
    assert "Style: Editorial photography" in result
    assert "Composition:" not in result
    assert "Negative:" not in result


def test_full_profile_all_fields():
    result = assemble_prompt(
        user_prompt="A workbench",
        profile={
            "style_instructions": "Cinematic lighting",
            "composition": "Subject in lower-right third",
            "mood": "calm, professional",
            "negative": "no text, no faces",
        },
    )
    # Order matters: Subject, Style, Composition, Mood, Negative
    lines = result.split("\n\n")
    assert lines[0].startswith("Subject:")
    assert lines[1].startswith("Style:")
    assert lines[2].startswith("Composition:")
    assert lines[3].startswith("Mood:")
    assert lines[4].startswith("Negative:")


def test_empty_composition_is_skipped():
    result = assemble_prompt(
        user_prompt="Scene",
        profile={
            "style_instructions": "Style A",
            "composition": "",
            "negative": "no 3D",
        },
    )
    assert "Composition:" not in result
    assert "Negative: no 3D" in result


def test_legacy_profile_without_new_fields():
    """Existing academic/minimal/agentic_ai_diagrams profiles must still work."""
    legacy = {
        "style_instructions": "Scholarly clean illustration",
        "mood": "educational",
    }
    result = assemble_prompt("A diagram", legacy)
    assert "Subject: A diagram" in result
    assert "Style: Scholarly clean illustration" in result
    assert "Mood: educational" in result
    assert "Composition:" not in result
    assert "Negative:" not in result


def test_user_prompt_is_stripped():
    result = assemble_prompt(
        user_prompt="  A scene with trailing whitespace   \n",
        profile={"style_instructions": "X"},
    )
    assert "Subject: A scene with trailing whitespace" in result
