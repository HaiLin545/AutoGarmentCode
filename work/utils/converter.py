"""
Bidirectional conversion between compact garment format and full design-param format.

Compact format: nested YAML with only values (no range/type/default_prob).
Full format:    nested YAML where every leaf is {v, range, type, [default_prob]}.

    compact_to_design(compact, template) -> full design dict
    design_to_compact(design)            -> compact dict
"""

from copy import deepcopy
from .yaml_utils import load_yaml, save_yaml
from .io import DEFAULT_TEMPLATE


# ---------------------------------------------------------------------------
# compact → design param (full)
# ---------------------------------------------------------------------------

def compact_to_design(
    compact: dict,
    template_path: str = None,
) -> dict:
    """Convert a compact garment dict into the full design-param format.

    For every value in *compact*, the corresponding ``v`` field in the
    template is overwritten.  Parameters absent from *compact* keep
    their template defaults.

    Returns the complete ``{"design": {...}}`` dict ready for GarmentCode.
    """
    template = load_yaml(template_path or str(DEFAULT_TEMPLATE))
    design = deepcopy(template)

    _ensure_connected(design["design"])
    flat = _flatten(compact)
    _fill(design["design"], flat)

    return design


def compact_file_to_design(compact_path: str, template_path: str = None) -> dict:
    compact = load_yaml(compact_path)
    return compact_to_design(compact, template_path)


# ---------------------------------------------------------------------------
# design param (full) → compact
# ---------------------------------------------------------------------------

def design_to_compact(design: dict) -> dict:
    """Extract only the ``v`` values from a full design-param dict.

    Returns a nested dict with the same key hierarchy but values
    instead of ``{v, range, type, ...}`` leaf nodes.
    """
    if "design" in design:
        design = design["design"]
    return _strip(design)


def design_file_to_compact(design_path: str) -> dict:
    design = load_yaml(design_path)
    return design_to_compact(design)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _flatten(data: dict, prefix: str = "") -> dict:
    """Flatten nested dict to dot-separated key → value."""
    out = {}
    for key, val in data.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(val, dict):
            out.update(_flatten(val, path))
        else:
            out[path] = val
    return out


def _fill(template: dict, values: dict, prefix: str = ""):
    """Write flat values into the template's ``v`` fields."""
    if not isinstance(template, dict):
        return
    if "v" in template and "type" in template:
        if prefix in values:
            raw = values[prefix]
            t = template["type"]
            if t == "bool":
                template["v"] = bool(raw)
            elif t == "int":
                template["v"] = int(round(float(raw)))
            elif t == "float":
                template["v"] = float(raw)
            else:
                template["v"] = None if raw is None or str(raw).lower() == "null" else raw
    else:
        for key, child in template.items():
            if isinstance(child, dict):
                _fill(child, values, f"{prefix}.{key}" if prefix else key)


def _strip(node: dict) -> dict:
    """Recursively strip metadata, keeping only values."""
    out = {}
    for key, val in node.items():
        if not isinstance(val, dict):
            continue
        if "v" in val and "type" in val:
            out[key] = val["v"]
        else:
            child = _strip(val)
            if child:
                out[key] = child
    return out


def _ensure_connected(design: dict):
    meta = design.setdefault("meta", {})
    if "connected" not in meta:
        meta["connected"] = {
            "v": False,
            "range": [True, False],
            "type": "bool",
        }
