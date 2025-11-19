'''
(templates)

Utilities to load external prompt templates stored as .txt files.
'''
from __future__ import annotations

from typing import Dict
import os

_PROMPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def load_template(name: str) -> str:
    """Load a prompt template by filename (without extension) from templates dir."""
    path = os.path.join(_PROMPTS_DIR, f"{name}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(name: str, variables: Dict[str, str]) -> str:
    """Fill a template by replacing only provided {placeholders}.

    Avoids Python's str.format so that literal braces in templates (e.g., JSON
    examples/schemas) are preserved without needing to escape them.
    """
    tmpl = load_template(name)
    for key, value in variables.items():
        tmpl = tmpl.replace("{" + key + "}", str(value))
    return tmpl
