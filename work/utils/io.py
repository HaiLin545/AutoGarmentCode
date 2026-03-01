"""File I/O and prompt-building helpers."""

from pathlib import Path

import yaml

WORK_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = WORK_DIR.parent
DEFAULT_TEMPLATE = PROJECT_ROOT / "assets" / "design_params" / "default.yaml"
DOCS_DIR = WORK_DIR / "docs"
PROMPT_PATH = DOCS_DIR / "prompt.md"
BODY_DOCS_PATH = DOCS_DIR / "body_docs.md"
DESIGN_DOCS_PATH = DOCS_DIR / "design_docs.md"


def load_text(path):
    with open(path) as f:
        return f.read()


def load_prompt() -> str:
    """Build the full system prompt by inserting body_docs and design_docs into prompt.md."""
    template = load_text(PROMPT_PATH)
    body_docs = load_text(BODY_DOCS_PATH)
    design_docs = load_text(DESIGN_DOCS_PATH)
    return template.replace("{{BODY_DOCS}}", body_docs).replace("{{DESIGN_DOCS}}", design_docs)


def build_user_prompt(body: dict) -> str:
    """Build the user-message string that accompanies the image."""
    body_yaml = yaml.dump(body, default_flow_style=False)
    return (
        f"Here are the body measurements for this person:\n\n"
        f"```yaml\n{body_yaml}```\n\n"
        f"Analyze the garment in the attached image and output the design parameters YAML."
    )
