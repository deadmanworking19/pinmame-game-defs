from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .jsonio import load_json, write_text


PINSIDE_TOP100_PATH = Path("docs") / "pinside-top100.md"
_TABLE_ROW = re.compile(r"^ {0,3}\|(?P<first>[^|]*)\|")
_PINSIDE_ROW = re.compile(r"^ {0,3}\| *(?P<rank>\d+) *\| *(?P<game>[^|]*?) *\| *`(?P<machine>[^`]+)` *\| *(?P<completion>\d+)% *\| *$")


def pinside_rows(text: str) -> list[tuple[int, re.Match[str]]]:
	"""Return (line index, match) for every ranked row; a table row that looks ranked but does not parse is an error."""
	rows = []
	for index, line in enumerate(text.split("\n")):
		table_row = _TABLE_ROW.match(line)
		if table_row is None or not (table_row["first"].strip().isdigit() or "`" in line):
			continue
		match = _PINSIDE_ROW.match(line)
		if match is None:
			raise ValueError(f"{PINSIDE_TOP100_PATH.as_posix()} line {index + 1} is not a `| rank | game | `machine` | N% |` row: {line!r}")
		rows.append((index, match))
	return rows


def refresh_pinside_top100(text: str, catalog: dict[str, Any]) -> str:
	"""Rewrite every ranked row's Completion cell from the catalog's generated completion_score."""
	scores = {machine["id"]: machine["completion_score"] for machine in catalog["machines"]}
	lines = text.split("\n")
	for index, match in pinside_rows(text):
		machine_id = match["machine"]
		if machine_id not in scores:
			raise ValueError(f"{PINSIDE_TOP100_PATH.as_posix()} names {machine_id}, which is not a catalog record")
		lines[index] = f"| {match['rank']} | {match['game']} | `{machine_id}` | {scores[machine_id]}% |"
	return "\n".join(lines)


def write_pinside_top100(repository_root: Path) -> None:
	path = repository_root / PINSIDE_TOP100_PATH
	if not path.is_file():
		return
	catalog = load_json(repository_root / "catalog" / "pinmame.json")
	write_text(path, refresh_pinside_top100(path.read_text(encoding="utf-8"), catalog))
