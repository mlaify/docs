#!/usr/bin/env python3
"""Write content/attackmap/sdk-reference.md: every public name in `attackmap.sdk`.

Run it with a Python that has AttackMap installed at a release tag, and commit
the result (the site build never installs AttackMap):

    python3 -m venv /tmp/am && /tmp/am/bin/pip install "attackmap @ git+https://github.com/mlaify/AttackMap.git@v0.6.2"
    /tmp/am/bin/python -I scripts/gen-attackmap-sdk-reference.py v0.6.2

`attackmap.sdk.__all__` is the stable analyzer contract (see the module's own
docstring); anything else in `attackmap` is internal, so this page documents
exactly that list, in its order. Models list their fields from pydantic,
functions their signatures, constants their values. Docstrings are kept as
written, with Sphinx roles (:class:`X`, ``x``) turned into Markdown code.
"""
from __future__ import annotations

import dataclasses
import inspect
import re
import sys
import typing
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "content" / "attackmap" / "sdk-reference.md"
REPO = "https://github.com/mlaify/AttackMap"


def clean_type(t) -> str:
    """A type annotation as readers would write it: no module prefixes, no typing. noise."""
    s = t.__name__ if isinstance(t, type) and not typing.get_args(t) else str(t)
    s = s.replace("typing.", "").replace("NoneType", "None")
    s = re.sub(r"\b(?:[a-z_][\w]*\.)+([A-Za-z_]\w*)", r"\1", s)  # attackmap.models.Route -> Route
    return s


def clean_doc(doc: str | None) -> str:
    if not doc:
        return ""
    doc = inspect.cleandoc(doc)
    doc = re.sub(r":(?:class|func|data|meth|attr|mod):`~?([^`]+)`", r"`\1`", doc)
    doc = re.sub(r"``([^`]+)``", r"`\1`", doc)
    # Docstring headings must sit below this page's own (### per name).
    doc = re.sub(r"(?m)^(#{1,3}) ", lambda m: "#" * (len(m.group(1)) + 3) + " ", doc)
    # Hugo would run a shortcode delimiter; there are none today, so fail loudly if one appears.
    if "{{<" in doc or "{{%" in doc:
        sys.exit("a docstring contains Hugo shortcode syntax; escape it in the generator")
    return doc


def is_literal_alias(o) -> bool:
    return typing.get_origin(o) is typing.Literal


def kind_of(o) -> str:
    if inspect.ismodule(o):
        return "module"
    if is_literal_alias(o):
        return "type"
    if inspect.isclass(o):
        if hasattr(o, "model_fields"):
            return "model"
        if getattr(o, "_is_protocol", False):
            return "protocol"
        return "class"
    if inspect.isfunction(o) or inspect.isbuiltin(o):
        return "function"
    return "constant"


def model_section(o) -> list[str]:
    out = [clean_doc(o.__doc__), ""]
    fields = o.model_fields
    if fields:
        out += ["| Field | Type | Default |", "|---|---|---|"]
        for name, f in fields.items():
            if f.is_required():
                default = "required"
            elif f.default_factory is not None:
                default = f"`{f.default_factory.__name__}()`"
            else:
                default = f"`{f.default!r}`"
            ann = clean_type(f.annotation).replace("|", "\\|")
            out.append(f"| `{name}` | `{ann}` | {default} |")
        out.append("")
    return out


def protocol_section(o) -> list[str]:
    out = [clean_doc(o.__doc__), ""]
    members = []
    for name, member in o.__dict__.items():
        if name.startswith("_"):
            continue
        if isinstance(member, property):
            members.append(f"- `{name}` (property)")
        elif inspect.isfunction(member):
            members.append(f"- `{name}{signature(member)}`")
    for name, ann in getattr(o, "__annotations__", {}).items():
        members.insert(0, f"- `{name}: {clean_type(ann)}`")
    if members:
        out += ["Members:", "", *members, ""]
    return out


def signature(o) -> str:
    """The signature with string annotations resolved (the SDK uses `from __future__ import annotations`),
    so they print bare while string defaults keep their quotes."""
    try:
        sig = inspect.signature(o, eval_str=True)
    except Exception:
        sig = inspect.signature(o)
    return re.sub(r"\b(?:[a-z_][\w]*\.)+([A-Za-z_]\w*)", r"\1", str(sig))


def function_section(o, qual: str) -> list[str]:
    sig = signature(o)
    return ["```python", f"def {qual}{sig}", "```", "", clean_doc(o.__doc__), ""]


def constant_section(o) -> list[str]:
    if isinstance(o, (tuple, frozenset, set, list)):
        items = sorted(o) if isinstance(o, (frozenset, set)) else list(o)
        return [f"{type(o).__name__} of {len(items)}: " + ", ".join(f"`{i}`" for i in items), ""]
    return [f"`{o!r}`", ""]


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].startswith("v"):
        sys.exit("usage: gen-attackmap-sdk-reference.py <release tag, e.g. v0.6.2>")
    tag = sys.argv[1]
    import attackmap
    import attackmap.sdk as sdk

    installed = getattr(attackmap, "__version__", None)
    if installed and installed != tag.lstrip("v"):
        sys.exit(f"installed attackmap is {installed}, not {tag}: install the tag first")

    names = list(sdk.__all__)
    groups: dict[str, list[str]] = {"Analyzer contract": [], "Signal models": [], "Allowed values": [],
                                    "Filesystem helpers": [], "Taint sink plugins": []}
    for n in names:
        o = getattr(sdk, n)
        k = kind_of(o)
        if k == "module":
            continue  # `fs`: its members are exported too, and listed under Filesystem helpers
        if n in getattr(sdk.fs, "__all__", ()) or n in ("walk_repo", "is_contained", "contained_file", "read_repo_text"):
            groups["Filesystem helpers"].append(n)
        elif n.startswith("Analyzer") or n == "normalize_analyzer_metadata":
            groups["Analyzer contract"].append(n)
        elif "TAINT" in n or "taint" in n:
            groups["Taint sink plugins"].append(n)
        elif k in ("type", "constant"):
            groups["Allowed values"].append(n)
        elif k == "function":
            groups["Filesystem helpers"].append(n)
        else:
            groups["Signal models"].append(n)

    lines = [
        "---",
        'title: "SDK reference"',
        f'description: "Every public name in attackmap.sdk at {tag}: the analyzer protocol, the signal models and their fields, the allowed values, and the filesystem helpers."',
        "weight: 110",
        'group: "Extending"',
        f'source: "{REPO}/tree/{tag}/src/attackmap/sdk"',
        "---",
        "",
        "{{< callout type=\"note\" >}}",
        f"Generated from `attackmap.sdk` at [{tag}]({REPO}/tree/{tag}/src/attackmap/sdk) by",
        "`scripts/gen-attackmap-sdk-reference.py`. Anything importable from `attackmap.sdk` is",
        "the stable analyzer contract; anything else in `attackmap` is internal. The",
        "[Analyzer SDK](sdk.md) guide explains how the pieces fit together.",
        "{{< /callout >}}",
        "",
    ]
    first_name: dict[int, str] = {}  # one object exported under two names (AnalyzerResult is ScanResult)
    for n in names:
        first_name.setdefault(id(getattr(sdk, n)), n)
    for group, members in groups.items():
        if not members:
            continue
        lines += [f"## {group}", ""]
        for n in members:
            o = getattr(sdk, n)
            k = kind_of(o)
            lines += [f"### `{n}` {{#{n.lower()}}}", ""]
            alias_of = first_name[id(o)]
            if alias_of != n and k in ("model", "class", "protocol"):
                lines += [f"The same class as [`{alias_of}`](#{alias_of.lower()}), exported under a second name.", ""]
                continue
            if k == "model":
                lines += [f"*Model* (pydantic). Module `{o.__module__.replace('attackmap.sdk.', 'attackmap.sdk.')}`.", ""]
                lines += model_section(o)
            elif k == "protocol":
                lines += ["*Protocol*.", ""] + protocol_section(o)
            elif k == "class":
                lines += ["*Class*.", "", clean_doc(o.__doc__), ""]
            elif k == "function":
                lines += function_section(o, n)
            elif k == "type":
                lines += ["*Type*: one of " + ", ".join(f"`{a!r}`" for a in typing.get_args(o)) + ".", ""]
            else:
                lines += constant_section(o)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(OUT.parent.parent.parent)}: {sum(len(v) for v in groups.values())} names from {tag}")


if __name__ == "__main__":
    main()
