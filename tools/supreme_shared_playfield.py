"""Build a routing-only comparison between Supreme and Spider-Man excerpts.

The result deliberately compares firmware routing facts.  It does not infer
that the two titles have the same physical wiring or installed hardware.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


_EXCERPTS = "evidence/excerpts"
_SUPREME_ROUTING = "stern.supreme-x-stern.2018/rom-routing.json.txt"
_SPIDERMAN_ROUTING = "stern.spider-man-the-pin.2016/rom-routing.json.txt"
_MANUAL_FILES = {
    "coils": ("manual-drivers.md", "DR"),
    "switches": ("manual-switches-page15.md", "SW"),
    "switches_page17": ("manual-switches-page17.md", "SW"),
    "leds": ("manual-lamps-page18.md", "LP"),
    "leds_page20": ("manual-lamps-page20.md", "LP"),
}
_ADDRESS_RE = re.compile(r"^(?P<node>\d+)-(?P<kind>DR|SW|LP)-(?P<position>\d+)$")

_AUTHORITY_LIMIT = (
    "Matches prove routing only; the sibling manual proves sibling hardware; "
    "Supreme physical fitment/harness, polarity, parts and emitter counts remain unconfirmed."
)
_COORDINATE_CONVENTION = "x=0 left, x=1 right, y=0 rear/backglass end, y=1 apron/front"


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read_source(root: Path, relative_path: str) -> tuple[bytes, dict[str, str]]:
    path = root / _EXCERPTS / relative_path
    contents = path.read_bytes()
    return contents, {
        "path": _relative(path, root),
        "sha256": hashlib.sha256(contents).hexdigest(),
    }


def _load_routing(root: Path, relative_path: str) -> tuple[dict[str, Any], dict[str, str]]:
    contents, source = _read_source(root, relative_path)
    try:
        loaded = json.loads(contents.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid routing excerpt: {source['path']}") from error
    if not isinstance(loaded, dict):
        raise ValueError(f"routing excerpt must be an object: {source['path']}")
    return loaded, source


def _valid_public_address(value: Any, source: str, section: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"invalid public address in {source} {section}: {value!r}")
    return value


def _valid_coordinate(value: Any, label: str, source: str, section: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"invalid {label} in {source} {section}: {value!r}")
    return value


def _routing_rows(
    routing: dict[str, Any], *, source: str, section: str
) -> dict[tuple[int, int], dict[str, Any]]:
    table = routing.get(section)
    if not isinstance(table, dict):
        raise ValueError(f"missing {section} table in {source}")
    columns = table.get("columns")
    rows = table.get("rows")
    if not isinstance(columns, list) or not all(isinstance(column, str) for column in columns):
        raise ValueError(f"invalid {section} columns in {source}")
    if len(set(columns)) != len(columns):
        raise ValueError(f"duplicate {section} columns in {source}")
    if not isinstance(rows, list):
        raise ValueError(f"invalid {section} rows in {source}")

    required = {"node", "position", "public_address", "name"}
    missing = required - set(columns)
    if missing:
        raise ValueError(f"missing {section} columns in {source}: {sorted(missing)}")

    result: dict[tuple[int, int], dict[str, Any]] = {}
    for row_number, row in enumerate(rows, start=1):
        if not isinstance(row, list) or len(row) != len(columns):
            raise ValueError(f"invalid {section} row {row_number} in {source}")
        values = dict(zip(columns, row, strict=True))
        node = _valid_coordinate(values["node"], "node", source, section)
        position = _valid_coordinate(values["position"], "position", source, section)
        public_address = _valid_public_address(values["public_address"], source, section)
        key = (node, position)
        if key in result:
            raise ValueError(f"duplicate node-position row in {source} {section}: {key}")
        result[key] = {
            "node": node,
            "position": position,
            "public_address": public_address,
            "name": values["name"],
            **({"class_bits": values["class_bits"]} if "class_bits" in values else {}),
        }
    return result


def _table_cells(line: str) -> list[str]:
    stripped = line.strip()
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) is not None for cell in cells)


def _parse_manual_table(
    root: Path, relative_path: str, expected_kind: str
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    contents, source = _read_source(root, relative_path)
    try:
        lines = contents.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise ValueError(f"invalid manual excerpt: {source['path']}") from error

    header: list[str] | None = None
    start = 0
    for index in range(len(lines) - 1):
        if not lines[index].strip().startswith("|") or not lines[index + 1].strip().startswith("|"):
            continue
        candidate = _table_cells(lines[index])
        if _is_separator(_table_cells(lines[index + 1])):
            header = candidate
            start = index + 2
            break
    if header is None or not header or len(set(header)) != len(header):
        raise ValueError(f"missing or invalid markdown table in {source['path']}")
    if "ID" not in header or "Address" not in header:
        raise ValueError(f"manual table lacks ID or Address in {source['path']}")

    parsed: list[dict[str, Any]] = []
    for line in lines[start:]:
        if not line.strip().startswith("|"):
            break
        cells = _table_cells(line)
        if _is_separator(cells):
            continue
        if len(cells) != len(header):
            raise ValueError(f"wrong cell count in {source['path']}: {line!r}")
        row = dict(zip(header, cells, strict=True))
        address = row["Address"]
        if address in {"", "BLANK"}:
            if all(value in {"", "BLANK"} for column, value in row.items() if column != "ID"):
                continue
            raise ValueError(f"nonblank manual row without address in {source['path']}: {row!r}")
        matched = _ADDRESS_RE.fullmatch(address)
        if matched is None or matched["kind"] != expected_kind:
            raise ValueError(f"invalid {expected_kind} address in {source['path']}: {address!r}")
        identifier = row["ID"]
        if identifier.isdigit():
            public_number = int(identifier)
        elif expected_kind == "SW" and re.fullmatch(r"C([1-9]|[12][0-9]|3[0-2])", identifier):
            # Spike 1's CPU C1-C32 namespace is public 101-132, not 1-32.
            public_number = 100 + int(identifier[1:])
        else:
            raise ValueError(f"unsupported manual ID in {source['path']}: {identifier!r}")
        parsed.append(
            {
                "manual_page": source["path"],
                "manual_row": row,
                "node": int(matched["node"]),
                "position": int(matched["position"]),
                "public_number": public_number,
            }
        )
    return parsed, source


def _manual_rows(root: Path) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, str]]]:
    manual_rows = {"switches": [], "coils": [], "leds": []}
    sources: list[dict[str, str]] = []
    for key, (filename, expected_kind) in _MANUAL_FILES.items():
        section = key.removesuffix("_page17").removesuffix("_page20")
        relative_path = f"stern.spider-man-the-pin.2016/{filename}"
        rows, source = _parse_manual_table(root, relative_path, expected_kind)
        manual_rows[section].extend(rows)
        sources.append(source)
    return manual_rows, sources


def _public_manual_index(
    rows: list[dict[str, Any]], section: str
) -> dict[tuple[int, int, int], dict[str, Any]]:
    index: dict[tuple[int, int, int], dict[str, Any]] = {}
    for row in rows:
        public_number = row["public_number"]
        key = (row["node"], row["position"], public_number)
        if key in index:
            raise ValueError(f"ambiguous manual match in {section}: {key}")
        index[key] = row
    return index


def _crosswalk_section(
    supreme_rows: dict[tuple[int, int], dict[str, Any]],
    spiderman_rows: dict[tuple[int, int], dict[str, Any]],
    manual_rows: list[dict[str, Any]],
    section: str,
) -> dict[str, Any]:
    manual_index = _public_manual_index(manual_rows, section)
    shared: list[dict[str, Any]] = []
    supreme_only: list[dict[str, Any]] = []
    spiderman_only: list[dict[str, Any]] = []

    for key in sorted(set(supreme_rows) | set(spiderman_rows)):
        supreme = supreme_rows.get(key)
        spiderman = spiderman_rows.get(key)
        if supreme is None:
            entry = {
                "node": spiderman["node"],
                "position": spiderman["position"],
                "public_address": spiderman["public_address"],
                "spiderman_name": spiderman["name"],
            }
            if "class_bits" in spiderman:
                entry["spiderman_class_bits"] = spiderman["class_bits"]
            spiderman_only.append(entry)
            continue
        if spiderman is None:
            entry = {
                "node": supreme["node"],
                "position": supreme["position"],
                "public_address": supreme["public_address"],
                "supreme_name": supreme["name"],
            }
            if "class_bits" in supreme:
                entry["supreme_class_bits"] = supreme["class_bits"]
            supreme_only.append(entry)
            continue
        if supreme["public_address"] != spiderman["public_address"]:
            raise ValueError(
                f"public-address disagreement in {section} at {key}: "
                f"{supreme['public_address']} != {spiderman['public_address']}"
            )
        entry = {
            "node": supreme["node"],
            "position": supreme["position"],
            "public_address": supreme["public_address"],
            "supreme_name": supreme["name"],
            "spiderman_name": spiderman["name"],
        }
        if "class_bits" in supreme:
            entry["supreme_class_bits"] = supreme["class_bits"]
        if "class_bits" in spiderman:
            entry["spiderman_class_bits"] = spiderman["class_bits"]
        manual = manual_index.get((entry["node"], entry["position"], entry["public_address"]))
        if manual is not None:
            entry["manual_page"] = manual["manual_page"]
            entry["manual_row"] = manual["manual_row"]
        shared.append(entry)

    matched_manual = {(row["node"], row["position"], row["public_address"]) for row in shared if "manual_row" in row}
    return {
        "counts": {
            "shared": len(shared),
            "supreme_only": len(supreme_only),
            "spiderman_only": len(spiderman_only),
            "manual_matched": sum("manual_row" in row for row in shared),
        },
        "shared": shared,
        "supreme_only": supreme_only,
        "spiderman_only": spiderman_only,
        "unmatched_manual_rows": [
            {"manual_page": row["manual_page"], "manual_row": row["manual_row"]}
            for row in manual_rows
            if (row["node"], row["position"], row["public_number"]) not in matched_manual
        ],
    }


def build_crosswalk(root: Path) -> dict[str, Any]:
    """Return a deterministic, JSON-ready routing comparison under *root*.

    All paths in the result are repository-relative.  Reading occurs only when
    this function is called, so importing the module has no filesystem effects.
    """
    root = Path(root)
    supreme, supreme_source = _load_routing(root, _SUPREME_ROUTING)
    spiderman, spiderman_source = _load_routing(root, _SPIDERMAN_ROUTING)
    manual_rows, manual_sources = _manual_rows(root)

    sections = {}
    for section in ("switches", "coils", "leds"):
        sections[section] = _crosswalk_section(
            _routing_rows(supreme, source=supreme_source["path"], section=section),
            _routing_rows(spiderman, source=spiderman_source["path"], section=section),
            manual_rows[section],
            section,
        )

    return {
        "format": "supreme-shared-playfield-crosswalk",
        "version": 1,
        "coordinate_convention": _COORDINATE_CONVENTION,
        "authority_limit": _AUTHORITY_LIMIT,
        "sources": [supreme_source, spiderman_source, *manual_sources],
        "sections": sections,
    }
