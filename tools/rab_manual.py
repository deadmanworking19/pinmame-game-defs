"""Parsers for the hand-transcribed The Adventures of Rocky and Bullwinkle and Friends manual excerpts.

The excerpts under ``evidence/excerpts/data-east.adventures-of-rocky-and-bullwinkle-and-friends.1993/`` are the
single source of the printed tables: this module reads their Markdown tables back into plain data, so the
definition cannot disagree with the transcription a reader can open. Every parsed value is a string exactly as
transcribed; the curator decides what each means.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCERPT_DIR = ROOT / "evidence/excerpts/data-east.adventures-of-rocky-and-bullwinkle-and-friends.1993"


def read_tables(path: Path) -> dict[str, list[dict[str, str]]]:
    """Every pipe table in ``path``, keyed by the nearest preceding ``##`` heading.

    A heading that carries two tables (the coil chart schematic draws drives 1-8 and 09-16) keys the second
    as ``<heading> #2``.
    """
    tables: dict[str, list[dict[str, str]]] = {}
    heading = ""
    header: list[str] | None = None
    key = ""
    for raw in path.read_bytes().decode("utf-8").split("\n"):
        line = raw.rstrip("\r")
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            header = None
            continue
        if not line.startswith("|"):
            header = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            key = heading
            count = 2
            while key in tables:
                key = f"{heading} #{count}"
                count += 1
            tables[key] = []
            continue
        if all(re.fullmatch(r"-+", cell) for cell in cells):
            continue
        if len(cells) != len(header):
            raise ValueError(f"{path.name}: ragged table row under {heading!r}: {line}")
        tables[key].append(dict(zip(header, cells)))
    return tables


def table(tables: dict[str, list[dict[str, str]]], prefix: str, nth: int = 1) -> list[dict[str, str]]:
    """The ``nth`` table under the one heading that starts with ``prefix``."""
    suffix = "" if nth == 1 else f" #{nth}"
    matches = [rows for heading, rows in tables.items() if heading.startswith(prefix) and heading.endswith(suffix) and (nth > 1 or not re.search(r" #\d+$", heading))]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one table under a heading starting {prefix!r}, found {len(matches)}")
    return matches[0]


def _matrix(tables: dict, chart_heading: str, *, return_transistor: bool) -> dict[int, dict]:
    columns = {int(row["Column"]): row for row in table(tables, "Column drives")}
    rows = {int(row["Row"]): row for row in table(tables, "Row returns")}
    if sorted(columns) != list(range(1, 9)) or sorted(rows) != list(range(1, 9)):
        raise ValueError("the matrix headers must print columns 1-8 and rows 1-8")
    chart = {}
    for row in table(tables, chart_heading):
        address = int(row["Addr"])
        column, line = int(row["Column"]), int(row["Row"])
        if address != (column - 1) * 8 + line:
            raise ValueError(f"{address} is not column-major position ({column}, {line})")
        returned = {"wire": rows[line]["Wire"], "connector": rows[line]["Connector"]}
        if return_transistor:
            returned["transistor"] = rows[line]["Return transistor"]
        chart[address] = {
            "printed": row["Printed cell"], "column": column, "row": line,
            "drive": {"transistor": columns[column]["Drive transistor"], "wire": columns[column]["Wire"], "connector": columns[column]["Connector"]},
            "return": returned,
        }
    if sorted(chart) != list(range(1, 65)):
        raise ValueError("the matrix chart must cover addresses 1-64 exactly")
    return chart


def switch_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "switch-matrix.md")
    chart = _matrix(tables, "Switch Matrix Chart", return_transistor=False)
    parts = {}
    for row in table(tables, "Switch Part Numbers"):
        number = row["Addr"]
        address = int(number.rstrip("*"))
        part = row["Part no."]
        parts[address] = {
            "description": row["Description"], "cabinet": number.endswith("*"),
            "part": None if part in {"-", "See Cabinet"} else part, "part_printed": part,
        }
    if sorted(parts) != list(range(1, 65)):
        raise ValueError("the switch part table must cover addresses 1-64 exactly")
    return {"chart": chart, "parts": parts}


def lamp_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "lamp-matrix.md")
    chart = _matrix(tables, "Lamp Matrix Chart", return_transistor=True)
    location = {int(row["No."]): row["Description"] for row in table(tables, "Lamp Matrix No.")}
    if sorted(location) != list(range(1, 65)):
        raise ValueError("the lamp number table must cover lamps 1-64 exactly")
    return {"chart": chart, "location": location}


def coil_data() -> dict:
    tables = read_tables(EXCERPT_DIR / "coil-drivers.md")
    switched = {int(row["Coil"]): row for row in table(tables, "CPU Controlled Auxiliary Solenoids")}
    flippers = {row["Coil description"]: row for row in table(tables, "Flipper Solenoids")}
    drives = {int(row["Drive"]): row for row in table(tables, "Coil chart schematic")}
    direct = {int(row["Drive"]): row for row in table(tables, "Coil chart schematic", 2)}
    wiring = {row["Position label"]: row for row in table(tables, "Playfield Coil / Flash Lamp Wiring Diagram")}
    special = {row["Position"]: row for row in table(tables, "Playfield Special Coil Diagram")}
    if sorted(switched) != list(range(17, 23)):
        raise ValueError("the auxiliary solenoid table must cover 17-22 exactly")
    if sorted(drives) != list(range(1, 9)) or sorted(direct) != list(range(9, 17)):
        raise ValueError("the coil chart schematic must draw drives 1-8 and 09-16 exactly")
    if sorted(flippers) != ["Left Flipper", "RightFlipper"]:
        raise ValueError("the flipper table must print the left and right flipper exactly")
    if sorted(special) != [f"SP{n}" for n in range(1, 7)]:
        raise ValueError("the special coil diagram must draw SP1-SP6 exactly")
    return {"switched": switched, "flippers": flippers, "drives": drives, "direct": direct, "wiring": wiring, "special": special}
