"""YAML loading / saving / parsing utilities."""

import re
import yaml


class NoAliasDumper(yaml.Dumper):
    """YAML dumper that expands all aliases to full content."""
    def ignore_aliases(self, data):
        return True


def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def save_yaml(data: dict, path: str):
    with open(path, "w") as f:
        yaml.dump(
            data, f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            Dumper=NoAliasDumper,
        )


def extract_yaml_from_response(text: str) -> dict:
    """Extract the first YAML code block from an LLM response string.

    Handles both bare YAML and ``` fenced blocks.
    """
    match = re.search(r"```(?:yaml)?\s*\n(.*?)```", text, re.DOTALL)
    raw = match.group(1) if match else text
    return yaml.safe_load(raw)


def dump_yaml_string(data: dict) -> str:
    """Serialize a dict to a YAML string (no aliases)."""
    return yaml.dump(
        data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        Dumper=NoAliasDumper,
    )
