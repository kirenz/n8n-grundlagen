from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


HEADING_RE = re.compile(r"^(#{1,2})\s+(.*)$")
NOTES_START_RE = re.compile(r"^:::\s*\{[^}]*\.notes\b[^}]*\}\s*$")
CLASS_RE = re.compile(r"\.([A-Za-z_][A-Za-z0-9_-]*)")
STAGE_CUE_RE = re.compile(r"\[([A-ZÄÖÜ0-9 _-]+)\]")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
QUOTED_VALUE_RE = re.compile(r'"[^"]*"|\'[^\']*\'')
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
IMAGE_PROMPT_RE = re.compile(
    r"<!--\s*image:\s*([^\n]*?)\n(.*?)-->", re.DOTALL
)
IMAGE_ATTR_RE = re.compile(r'(\w+)="([^"]*)"')

ALLOWED_CLASSES = {
    "notes",
    "columns",
    "column",
    "fragment",
    "fade-up",
    "fade-in",
    "fade-out",
    "fade-left",
    "fade-right",
    "fade-in-then-semi-out",
    "grow",
    "shrink",
    "strike",
    "highlight-red",
    "highlight-blue",
    "highlight-green",
    "current-visible",
    "current-fragment",
    "semi-fade-out",
    "d2",
    "features",
    "feature",
    "feature-number",
    "example",
    "metrics-grid",
    "metric",
    "number",
    "label",
    "sources",
    "comparison",
    "comparison-side",
    "separator",
    "flow",
    "highlighted",
    "timeline",
    "timeline-item",
    "timeline-number",
    "timeline-title",
    "timeline-detail",
    "numbered-sections-container",
    "numbered-section",
    "section-number",
    "section-title",
    "section-subtitle",
    "quote-box",
    "formula",
    "editorial",       # .formula.editorial — Prosa-Merksatz statt Code-Formel
    "key-takeaways",
    "resource-links",
    "tiny-text",
    "small-text",
    "center",
    "text-muted",
    "accent-blue",
    "accent-green",
    "accent-orange",
    "accent-violet",
    "glow-circle",
    "glow-circle--xl",
    "glow-circle--lg",
    "glow-circle--md",
    "glow-circle--xs",
    "glow-circle--blue",
    "glow-circle--violet",
    "glow-circle--teal",
    "glow-circle--lime",
    "glow-circle__label",
    "callout-note",
    "callout-tip",
    "callout-important",
    "callout-warning",
    "callout-caution",
    "animated-list",
    "simple-animated-list",
    "blur-focus",
    "neon-pill",
    "typewriter",
    "typewriter-slow",
    "typewriter-no-cursor",
    "zoom-in",
    "zoom-in-bounce",
    "underline-animate",
    "underline-animate-green",
    "underline-animate-orange",
    "big-stat",
    "big-stat-green",
    "big-stat-orange",
    "stat-number",
    "stat-label",
    "stat-context",
    "slide-up",
    "slide-down",
    "slide-left",
    "slide-right",
    "stagger-1",
    "stagger-2",
    "stagger-3",
    "stagger-4",
    "stagger-5",
    "stagger-6",
    "highlight-yellow",
    "highlight-pink",
    "highlight-white",
    "emoji-bounce",
    "emoji-shake",
    "emoji-continuous",
    "no-anim",
    # --- Blueprint 2026-04-22 additions ---
    "stage",            # global dark-mode switch for stage slides
    "anschauung",       # full-bleed analogy-scene stage slide
    "breath",           # single-word stage slide (pause/question)
    "chapter",          # chapter-opener with number + title
    "closing",          # closing-beat stage slide (final takeaway)
    "book-bridge",      # book cross-reference card at deck end
    "big-word",         # huge centered word inside .breath
    "chapter-number",   # number element inside .chapter
    "chapter-title",    # title element inside .chapter + .book-bridge
    "fullbleed",        # full-bleed background image modifier
    "kicker",           # small uppercase label above closing/opening content
    # --- Blueprint 2026-04-22 iteration 2 ---
    "tip-box",          # inline actionable-insight box (blue, "→" icon)
    "think-box",        # inline reflective-pause box (editorial cream, serif italic)
    # --- Blueprint 2026-04-22 iteration 3: code-display ---
    "codewindow",       # macOS-style window chrome around code blocks
    "python",           # language hint for codewindow divs
    "bash",             # language hint for codewindow divs
    "sql",              # language hint for codewindow divs
    "r",                # language hint for codewindow divs
    "js",               # language hint for codewindow divs
    "typescript",       # language hint for codewindow divs
    "yaml",             # language hint for codewindow divs
    "json",             # language hint for codewindow divs
}

PROJECT_FILE_REFS = (
    Path("custom-new.scss"),
    Path("title-slide.html"),
    Path("includes/footer-nav.html"),
    Path("includes/background-animation.html"),
    Path("references.bib"),
)


@dataclass
class Slide:
    index: int
    level: int
    heading_line: int
    title: str
    content_lines: list[str]
    notes_lines: list[str]
    notes_start_line: int
    notes_end_line: int
    attr_block: str = ""


def load_body(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1]
    return text


def markdown_to_plain(text: str) -> str:
    text = re.sub(r"\{[^{}]*\}\s*$", "", text).strip()
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\{[^}]+\}", r"\1", text)
    text = re.sub(r"[`*_#]", "", text)
    return " ".join(text.split())


def iter_heading_positions(lines: list[str]) -> Iterable[tuple[int, int, str]]:
    in_code_block = False
    fence_re = re.compile(r"^```")
    for index, line in enumerate(lines):
        if fence_re.match(line):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        match = HEADING_RE.match(line)
        if match:
            yield index, len(match.group(1)), markdown_to_plain(match.group(2))


def parse_slides(path: Path) -> list[Slide]:
    lines = path.read_text(encoding="utf-8").splitlines()
    body_lines = load_body("\n".join(lines)).splitlines()
    headings = list(iter_heading_positions(body_lines))
    if not headings:
        raise ValueError("Keine Slide-Heading (`#` oder `##`) gefunden.")

    slides: list[Slide] = []
    for slide_index, (start, level, raw_title) in enumerate(headings, start=1):
        end = headings[slide_index][0] if slide_index < len(headings) else len(body_lines)
        block = body_lines[start:end]
        raw_heading = block[0] if block else ""
        attr_match = re.search(r"\{([^}]*)\}\s*$", raw_heading)
        attr_block = attr_match.group(1) if attr_match else ""
        notes_start = None
        notes_end = None
        for offset, line in enumerate(block[1:], start=1):
            if NOTES_START_RE.match(line):
                notes_start = offset
                for closing in range(offset + 1, len(block)):
                    if block[closing].strip() == ":::":  # notes blocks are not nested in this repo
                        notes_end = closing
                        break
                break
        if notes_start is None or notes_end is None:
            raise ValueError(
                f"Folie {slide_index} (`{raw_title}`) hat keinen vollstaendigen `::: {{.notes}}`-Block."
            )

        trailing_text = HTML_COMMENT_RE.sub("", "\n".join(block[notes_end + 1 :]))
        if any(line.strip() for line in trailing_text.splitlines()):
            raise ValueError(
                f"Folie {slide_index} (`{raw_title}`) hat Inhalt nach dem Notes-Block; Notes muessen am Ende stehen."
            )

        extra_notes = [
            offset
            for offset, line in enumerate(block[notes_end + 1 :], start=notes_end + 1)
            if NOTES_START_RE.match(line)
        ]
        if extra_notes:
            raise ValueError(f"Folie {slide_index} (`{raw_title}`) hat mehr als einen Notes-Block.")

        slides.append(
            Slide(
                index=slide_index,
                level=level,
                heading_line=start + 1,
                title=raw_title,
                content_lines=block[1:notes_start],
                notes_lines=block[notes_start + 1 : notes_end],
                notes_start_line=start + notes_start + 1,
                notes_end_line=start + notes_end + 1,
                attr_block=attr_block,
            )
        )
    return slides


def strip_inline_examples(text: str) -> str:
    text = FENCED_CODE_RE.sub(
        lambda m: m.group(0) if m.group(0).startswith("```{") else "",
        text,
    )
    text = HTML_COMMENT_RE.sub("", text)
    return INLINE_CODE_RE.sub("", text)


def extract_image_prompts(text: str) -> list[dict[str, str]]:
    """Return all `<!-- image: profile=... file=... -->` prompt blocks.

    Each entry has keys ``profile``, ``file`` and ``prompt``. Missing
    attributes or an empty prompt body raise ValueError.
    """
    result: list[dict[str, str]] = []
    for match in IMAGE_PROMPT_RE.finditer(text):
        attrs = dict(IMAGE_ATTR_RE.findall(match.group(1)))
        prompt = match.group(2).strip()
        profile = attrs.get("profile")
        file_name = attrs.get("file")
        if not profile or not file_name:
            raise ValueError(
                f"image block missing profile= or file=: {match.group(1).strip()!r}"
            )
        if not prompt:
            raise ValueError(f"image block for {file_name} has empty prompt")
        result.append({"profile": profile, "file": file_name, "prompt": prompt})
    return result


def extract_local_references(text: str) -> set[str]:
    scan_text = strip_inline_examples(text)
    refs: set[str] = set()
    patterns = [
        re.compile(r'background-image="([^"]+)"'),
        re.compile(r'!\[[^\]]*\]\(([^)]+)\)'),
        re.compile(r'{{<\s*include\s+([^ >]+)\s*>}}'),
        re.compile(r'file="([^"]+)"'),
        re.compile(r'<img[^>]+src="([^"]+)"'),
    ]
    for pattern in patterns:
        for match in pattern.finditer(scan_text):
            candidate = match.group(1).strip().split()[0]
            if candidate.startswith(("http://", "https://", "#", "data:")):
                continue
            if "..." in candidate:
                continue
            refs.add(candidate)
    return refs


def extract_classes(text: str) -> set[str]:
    scan_text = strip_inline_examples(text)
    classes: set[str] = set()
    for attr_match in re.finditer(r"\{[^{}]*\}", scan_text):
        block = QUOTED_VALUE_RE.sub("", attr_match.group(0))
        classes.update(CLASS_RE.findall(block))
    return classes


def resolve_reference(base_dir: Path, ref: str) -> Path:
    return (base_dir / ref).resolve()


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    # `_metadata.yml` markiert den Slides-Root in beiden Layouts:
    # Solo-Repo (Slides-Repo direkt) und Mono-Repo (`<repo>/slides/`).
    # `_quarto.yml` taugt als Marker nicht, weil im Mono-Repo die Buch-
    # `_quarto.yml` im Repo-Root liegt — eine Ebene über `slides/`.
    for candidate in [current, *current.parents]:
        if (candidate / "_metadata.yml").exists():
            return candidate
    for candidate in [current, *current.parents]:
        if (candidate / "_quarto.yml").exists():
            return candidate
    return start.resolve().parent if start.is_file() else start.resolve()


def clean_notes_text(lines: list[str]) -> tuple[str, list[str]]:
    text = "\n".join(lines).strip()
    stage_cues = [match.group(1).strip() for match in STAGE_CUE_RE.finditer(text)]
    text = STAGE_CUE_RE.sub("", text)
    paragraphs = [" ".join(part.split()) for part in re.split(r"\n\s*\n", text) if part.strip()]
    return "\n\n".join(paragraphs), stage_cues


def assemble_prompt(user_prompt: str, profile: dict) -> str:
    """Assemble the final image-generation prompt from user prompt + profile.

    Profile fields used (all optional except style_instructions):
    - style_instructions (str): overall style & aesthetic guidance
    - composition (str): spatial/compositional instructions
    - mood (str): tonality/mood adjectives
    - negative (str): negative prompt / things to exclude
    """
    parts = [f"Subject: {user_prompt.strip()}"]
    style = (profile.get("style_instructions") or "").strip()
    composition = (profile.get("composition") or "").strip()
    mood = (profile.get("mood") or "").strip()
    negative = (profile.get("negative") or "").strip()
    if style:
        parts.append(f"Style: {style}")
    if composition:
        parts.append(f"Composition: {composition}")
    if mood:
        parts.append(f"Mood: {mood}")
    if negative:
        parts.append(f"Negative: {negative}")
    return "\n\n".join(parts)


def slide_is_stage(slide: "Slide") -> bool:
    """A slide counts as 'stage' if it carries .stage or a background-image."""
    attrs = getattr(slide, "attr_block", "") or ""
    if ".stage" in attrs:
        return True
    if "background-image" in attrs:
        return True
    return False


def slide_is_book_bridge(slide: "Slide") -> bool:
    attrs = getattr(slide, "attr_block", "") or ""
    return ".book-bridge" in attrs


def extract_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter at top of a Quarto file. Returns {} if none."""
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    try:
        import yaml
        return yaml.safe_load(parts[0][4:]) or {}
    except ImportError:
        return {}
