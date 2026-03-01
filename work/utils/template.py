"""Design-template manipulation: flatten, fill, patch."""


def flatten_values(data: dict, prefix: str = "") -> dict:
    """Flatten a nested dict to dot-separated key -> value pairs.

    Example:
        {"meta": {"upper": "Shirt"}} -> {"meta.upper": "Shirt"}
    """
    out = {}
    for key, val in data.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(val, dict):
            out.update(flatten_values(val, path))
        else:
            out[path] = val
    return out


def fill_template(template: dict, values: dict, prefix: str = ""):
    """Recursively set 'v' fields in a design template from a flat values dict.

    Each leaf in the template has the form ``{v: ..., type: ..., range: ...}``.
    This function matches ``prefix`` paths against *values* keys and writes
    the corresponding value into ``template["v"]`` with proper type coercion.
    """
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
            else:  # select / select_null
                template["v"] = None if raw is None or str(raw).lower() == "null" else raw
    else:
        for key, child in template.items():
            if isinstance(child, dict):
                fill_template(child, values, f"{prefix}.{key}" if prefix else key)


def ensure_connected_field(design: dict):
    """Add ``meta.connected`` if the template lacks it (GarmentCode's default.yaml omits it)."""
    meta = design.setdefault("meta", {})
    if "connected" not in meta:
        meta["connected"] = {
            "v": False,
            "range": [True, False],
            "type": "bool",
        }
