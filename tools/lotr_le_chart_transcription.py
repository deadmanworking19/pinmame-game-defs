"""Transcribe the Lord of the Rings Limited Edition cabinet chart from its PDF text layer.

The chart is an LE owner's edit of Stern's 11x17 Lord of the Rings cabinet chart, published as
``LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf``: the switch matrix with the dedicated switches, the coils
detailed chart and the lamp matrix, each with its wire colours and connectors. It is a vector
document, so every printed value is a text object and is read exactly rather than from a rendering.
Words are assigned to the chart's grid cells by position; the result is the seed
``tools/seeds/stern/lord-of-the-rings-limited-edition-2009-chart.json`` that the Limited Edition
curator consumes.

The text layer is not the whole page. Text objects the chart does not print are left out: white
text on the white coil-type cells (a ``0`` under several of them) and ``on Cabinet Side``, which sits under the #23
control-connector cell where the cell's fill covers it. A few printed marks are drawn as images, not
text: the rotation mark that flags a coil as available as -00B or -00T, the fraction in the ring
magnet's 20 1/2-480 wrap, the DOTS badge on #7 and the flash-test note under the coils. Those are
read from the page rendered at 300 dpi and listed in ``DRAWN`` below.

    python -B tools/lotr_le_chart_transcription.py --write <chart.pdf>
    python -B tools/lotr_le_chart_transcription.py --check <chart.pdf>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import load_json, write_json  # noqa: E402

SEED_PATH = ROOT / "tools/seeds/stern/lord-of-the-rings-limited-edition-2009-chart.json"
CHART_SHA256 = "a7eeefd8f739d48cea1c80ef18c48d42a08d5e9c2438ed7d2b2c6cbfe9e94d02"
SWITCH_COLUMNS_X = [66, 97, 130, 162, 195, 228, 260, 293]
SWITCH_ROWS_Y = [100, 125, 150, 176, 201, 226, 251, 276]
LAMP_COLUMNS_X = [849, 891, 934, 976, 1019, 1062, 1104, 1147]
LAMP_ROWS_Y = [100, 120, 141, 161, 181, 202, 222, 242, 262, 283]
COIL_ROWS_Y = {
	1: 89, 2: 100, 3: 111, 4: 123, 5: 134, 6: 145, 7: 156, 8: 167,
	9: 195, 10: 206, 11: 217, 12: 229, 13: 240, 14: 251, 15: 262, 16: 273,
	17: 301, 18: 312, 19: 323, 20: 335, 21: 346, 22: 357, 23: 368, 24: 379,
	25: 407, 26: 418, 27: 430, 28: 441, 29: 452, 30: 463, 31: 474, 32: 485,
	"AUX 1": 513, "AUX 2": 524, "AUX 3": 536,
}
# Coil chart columns by x range: (field, first x, last x).
COIL_COLUMNS = (
	("name", 410, 545), ("transistor", 545, 562), ("board", 562, 590), ("power_wire", 590, 638),
	("power_connection", 638, 668), ("power_voltage", 668, 690), ("control_wire", 690, 735),
	("control_connection", 735, 760), ("coil", 760, 800),
)
# The covered text object under the #23 control-connector cell (see the module docstring).
HIDDEN = {("on", 742), ("Cabinet", 748), ("Side", 763)}
# Printed marks drawn as images rather than text, read from the page rendered at 300 dpi.
DRAWN = {
	"rotation_marked": [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 15, 16, 17, 18, 19, 21, "AUX 1", "AUX 2", "AUX 3"],
	"coil_text": {6: ("20 -480", "20½-480")},
	"dots": [7],
	"flash_note": "Note: In Test Flash Lamps Menu (\"Flash\" Icon), Flashers tested are all Flash Lamps located between Q1-Q32 (This Game: Q14, Q23 & Q25-Q27, Q29-Q32)",
	"coil_note_mark": "↻ Coil Note: ↻ Either -00B or -00T can be used for coil replacements. B/T listed is preferable for easier diode access & may differ on game.",
}


def _within(words, x0, x1, y0, y1):
	return [w for w in words if x0 <= w[0] < x1 and y0 <= w[1] < y1]


def _lines(words) -> list[str]:
	rows: list[list] = []
	for word in sorted(words, key=lambda w: (w[1], w[0])):
		for row in rows:
			if abs(row[0][1] - word[1]) <= 1.6:
				row.append(word)
				break
		else:
			rows.append([word])
	return [" ".join(w[4] for w in sorted(row, key=lambda w: w[0])) for row in rows]


def _header(lines: list[str]) -> tuple[str, str, str]:
	designator = lines[0].split(":", 1)[1].strip()
	return designator, lines[1], lines[2]


def switch_matrix(words) -> dict:
	columns = []
	for index, x in enumerate(SWITCH_COLUMNS_X, start=1):
		drive, wire, connector = _header(_lines(_within(words, x - 6, x + 28, 74, 94)))
		columns.append({"column": index, "connector": connector, "drive": drive, "wire": wire})
	rows = []
	for index, y in enumerate(SWITCH_ROWS_Y, start=1):
		ic, wire, connector = _header(_lines(_within(words, 28, 62, y - 2, y + 18)))
		rows.append({"connector": connector, "ic": ic, "row": index, "wire": wire})
	switches = []
	for c, x in enumerate(SWITCH_COLUMNS_X, start=1):
		for r, y in enumerate(SWITCH_ROWS_Y, start=1):
			cell = _within(words, x - 4, x + 29, y - 2, y + 24)
			part = [w for w in cell if abs(w[1] - (y + 19)) <= 2.5]
			dots = [w for w in cell if w[4] in {"D", "OTS", "DO", "TS"} and w[0] >= x + 20]
			body = _lines([w for w in cell if w not in part and w not in dots])
			number, _, location = body[0].partition(" ")
			if int(number) != (c - 1) * 8 + r:
				raise SystemExit(f"switch cell {c}/{r} prints {number}")
			entry = {"address": int(number), "name": " ".join(body[1:])}
			if location:
				entry["location"] = location
			if part:
				entry["part"] = _lines(part)[0]
			if dots:
				entry["dots"] = True
			switches.append(entry)
	dedicated = []
	for index, y in enumerate(SWITCH_ROWS_Y, start=1):
		ic, wire, connector = _header(_lines(_within(words, 328, 362, y - 2, y + 18)))
		cell = _lines(_within(words, 362, 400, y - 2, y + 24))
		designator, _, location = cell[0].partition(" ")
		entry = {"address": designator, "connector": connector, "ic": ic, "wire": wire}
		if location:
			entry["location"] = location
		body = cell[1:]
		if body and re.fullmatch(r"\d{3}-\d{4}-\d{2}( on Flipper)?", body[-1]):
			entry["part"] = body.pop()
		entry["name"] = " ".join(body)
		dedicated.append(entry)
	ground = _lines(_within(words, 362, 400, 74, 94))
	return {
		"columns": sorted(columns, key=lambda c: c["column"]),
		"dedicated_ground": {"wire": ground[1], "connector": ground[2]},
		"dedicated_switches": dedicated,
		"notes": _lines(_within(words, 195, 330, 360, 420)),
		"rows": rows,
		"switches": sorted(switches, key=lambda s: s["address"]),
	}


def lamp_matrix(words) -> dict:
	columns = []
	for index, x in enumerate(LAMP_COLUMNS_X, start=1):
		ic, wire, connector = _header(_lines(_within(words, x - 3, x + 40, 74, 94)))
		columns.append({"column": index, "connector": connector, "ic": ic, "wire": wire})
	rows = []
	for index, y in enumerate(LAMP_ROWS_Y, start=1):
		drive, wire, connector = _header(_lines(_within(words, 812, 846, y - 2, y + 15)))
		rows.append({"connector": connector, "drive": drive, "row": index, "wire": wire})
	lamps = []
	for c, x in enumerate(LAMP_COLUMNS_X, start=1):
		for r, y in enumerate(LAMP_ROWS_Y, start=1):
			lines = _lines(_within(words, x - 2, x + 41, y - 2, y + 17))
			printed, _, bulb = lines[0].partition(" ")
			entry = {"address": (r - 1) * 8 + c, "bulb": bulb.removesuffix(" Bulb"), "name": " ".join(lines[1:])}
			if int(printed) != entry["address"]:
				entry["printed_number"] = printed
			lamps.append(entry)
	notes = _lines(_within(words, 1060, 1224, 500, 540))
	return {"columns": columns, "lamps": sorted(lamps, key=lambda l: l["address"]), "notes": notes, "rows": rows}


def coil_table(words) -> dict:
	words = [w for w in words if (w[4], round(w[0])) not in HIDDEN or not 360 < w[1] < 375]
	coils, auxiliary = [], []
	for address, y in COIL_ROWS_Y.items():
		band = _within(words, 410, 800, y - 5.5, y + 5.6)
		entry: dict = {"address": address}
		for field, x0, x1 in COIL_COLUMNS:
			lines = _lines([w for w in band if x0 <= w[0] < x1])
			if field == "name":
				text = " ".join(lines)
				prefix = f"{address}:" if isinstance(address, str) else f"#{address}"
				if not text.startswith(prefix):
					raise SystemExit(f"coil row {address} prints {text!r}")
				entry["name"] = text[len(prefix):].strip()
			elif field == "board":
				continue
			elif field == "coil" and lines:
				printed, replacement = DRAWN["coil_text"].get(address, (None, None))
				if printed is not None:
					if lines[0] != printed:
						raise SystemExit(f"coil row {address} prints {lines[0]!r}, not {printed!r}")
					lines[0] = replacement
				entry["coil"] = " / ".join(lines)
			elif lines:
				entry[field] = " ".join(lines)
		if address in DRAWN["rotation_marked"]:
			entry["either_00b_or_00t"] = True
		if address in DRAWN["dots"]:
			entry["dots"] = True
		(auxiliary if isinstance(address, str) else coils).append(entry)
	board = _lines(_within(words, 562, 590, 508, 540))
	note = " ".join(_lines(_within(words, 410, 800, 541, 548)))
	if not note.startswith("Coil Note: Either -00B or -00T"):
		raise SystemExit(f"coil note reads {note!r}")
	return {
		"auxiliary_uk_only": {"board": " ".join(board), "coils": auxiliary},
		"coil_note": DRAWN["coil_note_mark"],
		"coils": coils,
		"flash_test_note": DRAWN["flash_note"],
	}


def transcribe(pdf: Path) -> dict:
	import pymupdf

	data = pdf.read_bytes()
	digest = hashlib.sha256(data).hexdigest()
	if digest != CHART_SHA256:
		raise SystemExit(f"{pdf} is not the retained chart (sha256 {digest})")
	page = pymupdf.open(stream=data, filetype="pdf")[0]
	# White text is printed on the black header bands; only on the white coil-type cells is it invisible.
	# The words API merges such a span into the visible word it touches, so it is cut off the word.
	white = [(pymupdf.Rect(span["bbox"]), span["text"]) for block in page.get_text("dict")["blocks"] for line in block.get("lines", [])
	         for span in line["spans"] if span["color"] == 0xFFFFFF and 760 <= span["bbox"][0] < 800 and 84 <= span["bbox"][1] < 545]
	words = []
	for word in page.get_text("words"):
		text = word[4]
		for rect, hidden in white:
			if abs(rect.y0 - word[1]) < 1 and abs(rect.x1 - word[2]) < 1 and text.endswith(hidden):
				text = text[: -len(hidden)]
		if text:
			words.append((*word[:4], text, *word[5:]))
	return {
		"format": "lotr-le-cabinet-chart-transcription",
		"lamp_matrix": lamp_matrix(words),
		"source": {
			"document": "LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf",
			"method": "read from the PDF text layer by grid position with tools/lotr_le_chart_transcription.py, and checked against the page rendered at 300 dpi",
			"sha256": digest,
		},
		"coil_table": coil_table(words),
		"switch_matrix": switch_matrix(words),
		"version": 1,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", type=Path, metavar="CHART_PDF")
	mode.add_argument("--check", type=Path, metavar="CHART_PDF")
	args = parser.parse_args()
	if args.write:
		write_json(SEED_PATH, transcribe(args.write))
		print(f"Wrote {SEED_PATH.relative_to(ROOT)}")
		return
	if load_json(SEED_PATH) != transcribe(args.check):
		raise SystemExit(f"{SEED_PATH.relative_to(ROOT)} does not match the chart's text layer")
	print("Lord of the Rings Limited Edition chart transcription matches the retained chart.")


if __name__ == "__main__":
	main()
