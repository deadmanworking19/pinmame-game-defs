"""Curate the physical Stern The Lord of the Rings Limited Edition (2009) machine definition.

The Limited Edition is the 2003 machine built again in 2009 on a later I/O power driver board, with
its own firmware (10.02, ``lotr_le``). It has its own record because its wiring differs, but its
playfield, switch matrix, lamp matrix and coil set are the 2003 machine's. This builder therefore
derives the edition from the 2003 curator (``tools/curate_lord_of_the_rings.py``), which it imports,
and applies only what the edition's own evidence says:

- the LE cabinet chart (``tools/seeds/stern/lord-of-the-rings-limited-edition-2009-chart.json``,
  transcribed by ``tools/lotr_le_chart_transcription.py``) supplies every wire colour and connector,
  and its switch, lamp and coil tables are compared cell by cell with the 2003 machine's before a
  device is carried over;
- the right Helm's Deep flasher moves from driver 14 to driver 28, 14 is left unconnected and 12
  becomes the optional shaker motor, as the chart, the owner's report and the 10.02 firmware agree;
- the Balrog flasher carries the red LED module Stern's service bulletin 148 introduced.

Every other device, mechanism, display and placement comes from the 2003 definition unchanged except
for the Limited Edition sources added to its provenance. ``--check`` byte-compares the definition,
its seed, the spatial report, the knowledge note and the generated excerpts; ``--regenerate`` writes
them and retires the edition's earlier partial file.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path

from pinmame_game_defs.jsonio import load_json, write_json
import curate_lord_of_the_rings as base

ROOT = base.ROOT
MACHINE_ID = "stern.lord-of-the-rings-limited-edition.2009"
DEFINITION_PATH = ROOT / "machines/author-ready/stern/lord-of-the-rings-limited-edition-2009.json"
PARTIAL_PATH = ROOT / "machines/partial/stern/lord-of-the-rings-limited-edition-2009.json"
SEED_PATH = ROOT / "tools/seeds/stern/lord-of-the-rings-limited-edition-2009.json"
CHART_PATH = ROOT / "tools/seeds/stern/lord-of-the-rings-limited-edition-2009-chart.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/lord-of-the-rings-limited-edition-2009.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/lord-of-the-rings-limited-edition-2009.md"
EXCERPT_DIR = ROOT / "evidence/excerpts/stern.lord-of-the-rings-limited-edition.2009"
CHART = load_json(CHART_PATH)
IO_PARTS_PATH = ROOT / "tools/seeds/stern/lord-of-the-rings-limited-edition-2009-io-board-parts.json"
IO_PARTS = load_json(IO_PARTS_PATH)

CATALOG = "pinmame.catalog.97aa922bf8e4"
CORE = "pinmame.core.97aa922bf8e4"
IPDB = "ipdb.5558"
REPORT = "human-review.lotr-le.owner-report-2010"
CHART_SOURCE = "human-review.lotr-le.owner-tech-chart"
PAGES = "human-review.lotr-le.owner-annotated-manual-pages"
OWNER_PAGE = "human-review.lotr-le.owner-documentation-page"
KNOCKER_PAGE = "human-review.lotr-le.owner-knocker-page"
SHAKER_POST = "human-review.lotr-le.owner-shaker-post"
SB148 = "service-bulletin.stern.148"
IO_BOARD = "schematic.stern.io-power-driver-520-5249-00"
RUNTIME_FLASH = "runtime.lord-of-the-rings-limited-edition.flash-test"
RUNTIME_GAMEPLAY = "runtime.lord-of-the-rings-limited-edition.gameplay"
RUNTIME_FLASH_PATH = "evidence/runtime/whitestar/lord-of-the-rings-limited-edition-flash-test.json"
RUNTIME_GAMEPLAY_PATH = "evidence/runtime/whitestar/lord-of-the-rings-limited-edition-gameplay.json"
LIBRARY_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
FIREPOWER = "https://firepowerpinball.com/2ya/"
OWNER = "Richard Harvey (firepower)"
# 2003 sources this record does not cite: the 2003 machine's driver catalog revision and legacy
# migration input, and the 10.00 flash test, whose 10.02 counterpart this record cites instead.
DROPPED_BASE_SOURCES = {"pinmame.catalog.4ec52ff0ac13", "legacy.game.lotr", "runtime.lord-of-the-rings.flash-test"}

SW_COLS = {c["column"]: c for c in CHART["switch_matrix"]["columns"]}
SW_ROWS = {r["row"]: r for r in CHART["switch_matrix"]["rows"]}
SWITCHES = {s["address"]: s for s in CHART["switch_matrix"]["switches"]}
DEDICATED = {d["address"]: d for d in CHART["switch_matrix"]["dedicated_switches"]}
LA_COLS = {c["column"]: c for c in CHART["lamp_matrix"]["columns"]}
LA_ROWS = {r["row"]: r for r in CHART["lamp_matrix"]["rows"]}
LAMPS = {l["address"]: l for l in CHART["lamp_matrix"]["lamps"]}
COILS = {c["address"]: c for c in CHART["coil_table"]["coils"]}
AUX = {a["address"]: a for a in CHART["coil_table"]["auxiliary_uk_only"]["coils"]}

# The owner's vector overlays on his scans of manual Section 5 pages 100-106, which are the 2003
# manual's pages. Each entry is (where on the page, what the scan prints there, what the overlay
# prints). Positions were read from the PDF's text layer and every entry checked on the rendered page.
OVERLAYS = [
	("100", "Coils Detailed Chart Table", [
		("#1 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#2 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#2 Drive Transistor Control Line Color", "BRN-RED", "RED-BRN"),
		("#3 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#4 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#5 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#5 Drive Transistor Control Line Color", "BRN-GRN", "ORG-YEL"),
		("#6 Power Line Color", "VIO-YEL", "VIO-YEL"),
		("#7 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#9 Drive Transistor Control Line Color", "BLU-BRN", "GRY-YEL"),
		("#9 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#10 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#11 Power Line Color", "YEL-VIO", "BRN-BLU"),
		("#13 Power Line Color", "BRN", "YEL-BLU"),
		("#14 function", "FLASH: HELMS DEEP RT", "NOT USED      N.C. J9-P7"),
		("#15 Power Line Color, second line", "RED-YEL", "BRN-BLU"),
		("#15 Power Line Connection", "J10-P1/2", "J10-P4/5"),
		("#16 Power Line Color, first line", "BLU-YEL~3A", "ORG-BRN"),
		("#16 Power Line Color, second line", "RED-YEL", "BRN-BLU"),
		("#16 Power Line Connection", "J10-P1/2", "J10-P4/5"),
		("#16 Drive Transistor Control Line Color", "ORG-VIO", "BRN-ORG"),
		("#17-#22 Power Line Color", "BRN in each row", "one box, YEL-BLU in #17 with an arrow drawn down through #22"),
		("#23 Power Line Color", "ORG", "YEL-ORG"),
		("#25-#32 Power Line Color", "ORG in each row", "one box, YEL-ORG in #25 with an arrow drawn down through #32"),
		("#28 row", "#28 NOT USED, Q28, blank power cells, BLK-YEL, J6-P4", "#28  FLASH: HELMS DEEP RT.  Q28 | J6-P10 | 20v DC | BLU-BLK | J6-P4 | #906 Bulb"),
	]),
	("101", "Backbox I/O Power Driver Board Detailed Wiring Diagram", [
		("Board title", "Partial View I/O Power Driver Board 520-5137-01", "520-5249-00 in place of 520-5137-01"),
		("J6 pin 1 wire (#25 Flash: Pop Bumper X3)", "BLK-BRN", "BLK"),
		("J6 pin 2 wire (#26 Flash: Back Panel Ring)", "BLK-RED", "BLK-YEL"),
		("J6 pin 4 (#28)", "BLK-YEL, #28 Not Used", "BLU-BLK, #906 Clear x1, #28 Flash Helms Deep RT"),
		("J6 pin 10 low-power feed", "ORG 20V DC LOW POWER", "YEL-ORG 20V DC LOW POWER"),
		("J7 pin 1 low-power feed", "BRN 20V DC LOW POWER", "YEL-BLU 20V DC LOW POWER"),
		("Bridge 2 transformer feed at J17-P6", "FROM WHT-RED Transformer 16v AC", "FROM VIO-GRY Transformer 16v AC"),
		("Bridge 2 fuse", "F7", "F10"),
		("Bridge 2 and controlled-lamp bridge outputs", "unmarked", "+ beside each bridge's positive output"),
		("Controlled-lamp bridge", "BRIDGE 20, BRDG 20", "BRIDGE 4, BRDG 4"),
		("Controlled-lamp bridge feed at J17-P8", "FROM BLU-WHT Transformer 13v AC", "FROM VIO-WHT Transformer 13v AC"),
		("Controlled-lamp bridge feed at J17-P9", "FROM BLU-WHT Transformer 13v AC", "FROM VIO-WHT Transformer 13v AC"),
		("Controlled-lamp bridge fuse", "F22", "F9"),
		("J8 pin 3 wire (#2 Auto Launch)", "BRN-RED", "RED-BRN"),
		("J8 pin 6 wire (#5 Right VUK)", "BRN-GRN", "GRY-BLK"),
		("Balrog relay board low-power feed", "FROM ORG Low Power 20v DC J6-P10", "FROM YEL-ORG Low Power 20v DC J6-P10"),
		("Ring magnet high-power feed", "FROM VIO-YEL High Power 50v DC J10-P3", "J10-P8"),
		("Orbit pin low-power feed", "FROM BRN Low Power 20v DC J7-P1", "FROM YEL-BLU Low Power 20v DC J7-P1"),
		("J9 pin 1 wire (#9 Left Bumper)", "BLU-BRN", "GRY-YEL"),
		("J9 pin 7 (#14)", "BLU-BLK, #906 Clear X1, #14 Flash: Helm's Deep Rt.", "N.C.   NOT USED  (See #28 J6-4)"),
		("J9 pin 9 wire (#16 Right Flipper)", "ORG-VIO", "BRN-ORG"),
		("Right flipper fuse feed", "BLU-YEL", "ORG-BRN"),
		("J10 pins 1, 2 high-power line", "RED-YEL 50V DC HIGH POWER", "BRN-BLU 50V DC HIGH POWER, pins relabelled 10,9"),
		("J10 pin 3", "3", "8"),
		("J10 pins 4, 5 high-power line", "YEL-VIO 50V DC HIGH POWER", "YEL-BLK 50V DC HIGH POWER, pins relabelled 7,6"),
		("High-current bridge, upper feed", "J11-P3 I/O BD., FROM BLK-YEL AC Voltages IN 48v AC, 7A Slo-Blo F6", "J11-P2 I/O BD., FROM BLK-ORG AC Voltages IN 48v AC, 7A Slo-Blo (T) F5"),
		("High-current bridge, lower feed", "J11-P2 I/O BD., FROM BLK-ORG AC Voltages IN 48v AC", "J11-P3 I/O BD., FROM BLK-YEL AC Voltages IN 48v AC"),
		("Ring magnet fuse", "F20 Slo-Blo FOR MAGNET", "F7 4A* Slo-Blo (T), Ring Magnet *May need 5A S.B."),
		("High-current coil fuse", "3A Slo-Blo F21", "F8 3A Slo-Blo (T)"),
		("High-current bridge labels", "BRIDGE 1 50v HIGH CURRENT COILS, GND, BRDG1", "the same three labels, redrawn unchanged with the rest of that corner"),
	]),
	("103", "General Illumination Circuit Detailed Wiring Diagram", [
		("J15 pin 9 wire", "VIOLET", "GRY-YEL"),
		("J15 pin 8 wire", "GREEN", "YEL-GRY"),
		("J15 pin 7 wire", "YELLOW", "WHT-BLK"),
		("J15 pin 3 wire", "WHT-GRN", "YEL-GRN"),
		("Circuit 2 legend", "J15-P7 to J15-P2 (Fuse F25) = YEL to WHT-YEL", "WHT-BLK to WHT-YEL"),
		("Circuit 2 drawing, lower wire label", "YEL", "WHT-BLK"),
		("Circuit 3 legend", "J15-P8 to J15-P3 (Fuse F26) = GRN to WHT-GRN", "YEL-GRY to YEL-GRN"),
		("Circuit 3 drawing, upper wire label", "WHT-GRN", "YEL-GRN"),
		("Circuit 3 drawing, lower wire label", "GRN", "YEL-GRY"),
		("Circuit 4 legend", "J15-P9 to J15-P4 (Fuse F27) = VIO to WHT-VIO", "GRY-YEL to WHT-VIO"),
		("Circuit 4 drawing, lower wire label", "VIO", "GRY-YEL"),
	]),
	("104", "Playfield Switch Wiring Diagram and Playfield Lamp Wiring Diagram", [
		("Switch column 1 drive wire (CN5-P1, Q1)", "GRN-BRN", "PINK-GRY"),
		("Switch column 2 drive wire (CN5-P3, Q2)", "GRN-RED", "GRN-BLK"),
		("Switch column 3 drive wire (CN5-P4, Q3)", "GRN-ORG", "GRN"),
		("Switch column 7 drive wire (CN5-P8, Q7)", "GRN-VIO", "BRN-WHT"),
		("Switch row 3 return wire (CN7-P7, U400)", "WHT-ORG", "VIO"),
		("Switch row 4 return wire (CN7-P6, U400)", "WHT-YEL", "PINK-VIO"),
		("Switch row 8 return wire (CN7-P1, U401)", "WHT-GRY", "GRN-WHT"),
		("Lamp column 2 drive wire (J13-P8, U16)", "YEL-RED", "BLK-YEL"),
		("Lamp column 3 drive wire (J13-P7, U15)", "YEL-ORG", "GRN-ORG"),
		("Lamp column 5 drive wire (J13-P5, U13)", "YEL-GRN", "GRY-BLK"),
		("Lamp column 6 drive wire (J13-P4, U12)", "YEL-BLU", "GRY-RED"),
		("Lamp column 7 drive wire (J13-P3, U11)", "YEL-VIO", "BLU-WHT"),
		("Lamp row 2 return wire (J12-P2, Q34)", "RED-BLK", "BRN-BLK"),
		("Lamp row 3 return wire (J12-P3, Q35)", "RED-ORG", "BRN-BLK"),
		("Lamp row 4 return wire (J12-P4, Q36)", "RED-YEL", "ORG-YEL"),
		("Lamp row 6 return wire (J12-P6, Q38)", "RED-BLU", "ORG-VIO"),
		("Lamp row 8 return wire (J12-P9, Q40)", "RED-GRY", "BRN-BLK"),
		("Lamp row 9 return wire (J12-P10, Q41)", "RED-WHT", "ORG-WHT"),
		("Both grids", "unlabelled", "column labels C1-C8 and row labels R1-R8 (switches) and R1-R10 (lamps)"),
		("Captions beside switches 3 and 7", "*Future Expansion, printed rotated beside each", "*Future Expansion, redrawn unchanged beside each"),
	]),
	("105", "Playfield Terminal Strips, Fuses & Misc. Wiring Descriptions & Locations", [
		("Terminal strip D (Q25 Pops X3 jumper)", "ORANGE", "ORANGE to YEL-ORG"),
	]),
	("106", "2-Flipper Circuit Wiring Diagram", [
		("J10 pin labels", "10 ... 1", "5 4 written at the pins the 50v line leaves from, and 1"),
		("J10 50v line", "RED-YEL 50v", "BRN-BLU 50v"),
		("Right flipper control wire", "ORG-VIO", "BRN-ORG"),
		("Right flipper fuse feed", "BLU-YEL", "ORG-BRN"),
		("Left flipper fuse feed from J10", "RED-YEL", "BRN-BLU"),
		("50V DC feed under the flipper fuses", "RED-YEL 50V DC", "BRN-BLU 50V DC"),
	]),
]
# Where the overlays disagree with the chart this record follows, by device, for the device notes.
SWITCH_COLUMN_OVERLAY = {1: "PINK-GRY", 2: "GRN-BLK", 3: "GRN", 7: "BRN-WHT"}
SWITCH_ROW_OVERLAY = {3: "VIO", 4: "PINK-VIO", 8: "GRN-WHT"}
_COIL_BUS = (
	"The owner's annotated manual page 100 also reads BRN-BLU at J10-P4/5. His page 101 relabels the 2003 drawing's J10 pins 4,5 as 7,6, the board-side pins of the 520-5249-00 behind the \"Z\" adapter, "
	"and draws that 50v bus YEL-BLK; this chart keeps the harness-side J10-P4/5 and BRN-BLU."
)
COIL_OVERLAY_NOTES = {
	**{address: _COIL_BUS for address in (1, 2, 3, 4, 7, 9, 10, 11)},
	5: "The owner's annotated manual page 100 reads its control line as ORG-YEL; his page 101 and this chart print GRY-BLK. " + _COIL_BUS,
	6: "The owner's annotated manual page 101 relabels the magnet's high-power feed J10-P3 as J10-P8, the board-side pin of the 520-5249-00, and its fuse F20 as F7, 4A, with \"*May need 5A S.B.\"; this chart keeps J10-P3.",
	8: "The owner's annotated manual page 100 leaves this row's printed GRY-YEL~3A Fuse~YEL-VIO unannotated; his page 101 draws the bus that feeds it, J10 pins 1,2 on the 2003 board relabelled 10,9, as BRN-BLU, as this chart prints.",
	25: "The owner's annotated manual page 101 reads its control line at J6 pin 1 as BLK; this chart prints BLK-BRN.",
	26: "The owner's annotated manual page 101 reads its control line at J6 pin 2 as BLK-YEL; this chart prints BLK-RED.",
	46: "The owner's annotated manual pages 100 and 106 read its fuse feed as ORG-BRN~3A Fuse~BRN-BLU from J10-P4/5, and page 101 draws the board-side 50v line as BRN-BLU on J10 pins 10,9; this chart prints BLU-YEL~3A Fuse~YEL-BLK at J10-P1/2.",
	48: "The owner's annotated manual pages 100 and 106 read its fuse feed as GRY-YEL~3A Fuse~BRN-BLU from J10-P4/5, and page 101 draws the board-side 50v line as BRN-BLU on J10 pins 10,9; this chart prints GRY-YEL~3A Fuse~YEL-BLK at J10-P1/2.",
}


def _md(value) -> str:
	"""A table cell as printed. A cell holding ``~`` goes in a code span, where Markdown cannot read it as strikethrough."""
	if isinstance(value, str) and "~" in value:
		return f"`{value}`"
	if value is None or value == "":
		return "*(blank)*"
	return str(value).replace("|", "\\|")


def _table(headers: list[str], rows: list[list]) -> str:
	lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
	lines.extend("| " + " | ".join(_md(value) for value in row) + " |" for row in rows)
	return "\n".join(lines)


def _excerpt_contents() -> dict[Path, str]:
	sm, lm, ct = CHART["switch_matrix"], CHART["lamp_matrix"], CHART["coil_table"]
	chart = "\n\n".join([
		"# The Limited Edition cabinet chart",
		"`LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf`, published by an LE owner, Richard Harvey (\"firepower\"), as the `LOTR LE Cabinet Matrix`, an 11x17\" page to go inside the LE's lower cabinet: "
		"https://firepowerpinball.com/2ya/lotr/LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf, byte-identical to the copy mirrored as https://www.pinballrebel.com/pinball/cards/Tech_Charts/Stern_Lord_of_the_Rings_LE_Tech_Chart.pdf "
		f"(SHA-256 `{CHART['source']['sha256']}`). It is Stern's Lord of the Rings cabinet chart (`SPI Nr. 755-5310-80`) as the owner corrected it for his Limited Edition, titled `LORD of the RINGS LE` "
		"and `Switch Matrix, Coils Detailed Chart Table, Lamp Matrix, Playfield Maps, Switch, Coil & Lamp Wiring & Schematics, and Bulb Types`. Its owner's page says it documents his own game's wiring and that other LEs may use different wire colours.",
		"The three tables below are complete. They were read from the PDF's text layer by grid position (`tools/lotr_le_chart_transcription.py`), with runs of spaces folded to one, and checked against the page rendered at 300 dpi. "
		"The marks the chart draws as images rather than text were read from that rendering: the rotation mark beside a coil type, the fraction in `20½-480`, the DOTS badge on #7 and the flash-test note. "
		"The same sheet also carries the service-menu icon strips, the switch, coil and lamp location maps of the playfield and back panel, and the typical switch, coil and lamp wiring panels; those are drawings, cited by the records but not transcribed.",
		"## Switch matrix: drive columns\n\n" + _table(["Column", "Drive", "Wire", "Connector"], [[c["column"], c["drive"], c["wire"], c["connector"]] for c in sm["columns"]]),
		"## Switch matrix: return rows\n\n" + _table(["Row", "IC", "Wire", "Connector"], [[r["row"], r["ic"], r["wire"], r["connector"]] for r in sm["rows"]]),
		"## Switch matrix: cells\n\nA blank location or part cell is printed blank. The DOTS column says whether the cell carries the Diode On Terminal Strip badge.\n\n" + _table(
			["Switch", "Location", "Name", "Part", "DOTS"],
			[[s["address"], s.get("location"), s["name"], s.get("part"), "yes" if s.get("dots") else "no"] for s in sm["switches"]],
		),
		"## Dedicated switches\n\n" + f"Ground: `GROUND`, {sm['dedicated_ground']['wire']} {sm['dedicated_ground']['connector']}.\n\n" + _table(
			["Input", "IC", "Wire", "Connector", "Location", "Name", "Part"],
			[[d["address"], d["ic"], d["wire"], d["connector"], d.get("location"), d["name"], d.get("part")] for d in sm["dedicated_switches"]],
		),
		"## Switch notes\n\n" + "\n".join(f"> {line}" for line in sm["notes"]),
		"## Coils detailed chart table\n\nEach group's `Driver Ouput Board` cell is one merged `I/O Power Driver` cell, not repeated below. Rows #12, #14 and #24 are shaded grey; #12 and #14 print no power line, voltage or coil type. The DOTS column says whether the function cell carries the Diode On Terminal Strip badge; the last column, whether the coil-type cell carries the rotation mark that the coil note says lets -00B or -00T be used. Power-line cells printed on two lines are joined with a space.\n\n" + _table(
			["#", "Function", "Drive Transistor", "Power Line Color", "Power Line Connection", "Power Voltage", "D.T. Control Line Color", "D.T. Control Line Connect", "Coil GA-Turn or Bulb Type", "DOTS", "-00B or -00T"],
			[[f"#{c['address']}", c["name"], c["transistor"], c.get("power_wire"), c.get("power_connection"), c.get("power_voltage"), c["control_wire"], c["control_connection"], c.get("coil"), "yes" if c.get("dots") else "no", "yes" if c.get("either_00b_or_00t") else "no"] for c in ct["coils"]],
		),
		f"The note under the flasher rows, its last parenthesis printed in red: `{ct['flash_test_note']}`. It lists Q14 and omits Q28, the 2003 machine's flasher set: the owner did not update it with the rows above it.",
		f"## Auxiliary (UK only)\n\nDriver board, one merged cell: `{ct['auxiliary_uk_only']['board']}`.\n\n" + _table(
			["Aux", "Function", "Drive Transistor", "Power Line Color", "Power Line Connection", "Power Voltage", "D.T. Control Line Color", "D.T. Control Line Connect", "Coil GA-Turn", "-00B or -00T"],
			[[a["address"], a["name"], a["transistor"], a["power_wire"], a["power_connection"], a["power_voltage"], a["control_wire"], a["control_connection"], a["coil"], "yes" if a.get("either_00b_or_00t") else "no"] for a in ct["auxiliary_uk_only"]["coils"]],
		),
		f"> {ct['coil_note']}",
		"## Lamp matrix: columns (18v)\n\n" + _table(["Column", "IC", "Wire", "Connector"], [[c["column"], c["ic"], c["wire"], c["connector"]] for c in lm["columns"]]),
		"## Lamp matrix: rows (ground)\n\n" + _table(["Row", "Transistor", "Wire", "Connector"], [[r["row"], r["drive"], r["wire"], r["connector"]] for r in lm["rows"]]),
		"## Lamp matrix: cells\n\nThe chart prints lamp 5's number as `4`; its position, between lamps 4 and 6 in row 1, makes it lamp 5.\n\n" + _table(
			["Lamp", "Printed number", "Bulb", "Name"],
			[[l["address"], l.get("printed_number", l["address"]), l["bulb"], l["name"]] for l in lm["lamps"]],
		),
		"## Lamp notes\n\n" + "\n".join(f"> {line}" for line in lm["notes"]),
	]) + "\n"
	overlay_parts = [
		"# The owner's annotated manual pages 100-106",
		"`Stern-2009-LOTR-LE-Missing-Pages-100-to-106.pdf`, published by the same LE owner as `Pages 100-106 which are missing from Stern LOTR LE Manual 2009`: https://firepowerpinball.com/2ya/lotr/Stern-2009-LOTR-LE-Missing-Pages-100-to-106.pdf "
		"(SHA-256 `3745b609874e0f48994101a57067a8a78c0bb62c49cc74338c534c26926c5d74`). Each of its seven pages is a scan of the Lord of the Rings manual's Section 5 pages 100-106 with the owner's corrections laid over it as vector text and boxes.",
		"The scans are the 2003 manual's pages, not Limited Edition ones: page 100 matches the coils chart of Stern's current reissue of the 2003 manual (`Lord_of_the_Rings_Manual-2022.pdf`, PDF 118) cell for cell, still printing #14 FLASH: HELMS DEEP RT and #28 NOT USED, and page 101 is titled `Partial View I/O Power Driver Board 520-5137-01`, the 2003 board. So everything the scans print describes the 2003 machine, and everything the owner changed describes his Limited Edition. "
		"His page says these are his own game's wiring and that Stern may have used different wire colours on other LEs.",
		"Below is every overlay, page by page: where it sits, what the scan prints there, and what the overlay prints. The overlay texts were read from the PDF's text layer and each placement checked on the page rendered at 150-220 dpi; boxes, arrows and other drawn marks were read from the rendering. Where an overlay hides the printed value completely, the value given under it is the one the same page of Stern's 2022 reissue prints in that place.",
	]
	for page, title, entries in OVERLAYS:
		overlay_parts.append(f"## Page {page}: {title}\n\n" + _table(["Where", "The scan prints", "The overlay prints"], [list(entry) for entry in entries]))
	overlay_parts.append("Page 102 (the backbox board layout) carries no overlay. Unannotated cells keep the scan's printed value, which the owner left standing; that is weaker evidence than an overlay, since nothing shows he checked them.")
	overlays = "\n\n".join(overlay_parts) + "\n"
	documentation = "\n\n".join([
		"# The LE owner's documentation, knocker and shaker pages",
		"Three pages by the same LE owner, Richard Harvey (\"firepower\"), who kept a blog about his new-in-box Limited Edition. None is a factory document; each is his first-hand account of his own machine. Passages are quoted as printed.",
		"## Lord of the Rings manuals and schematics page",
		"https://firepowerpinball.com/2ya/14-lotr.html (retained HTML SHA-256 `076909fb4a19067f13d0ac8377cd4074766bf31d941e51f58aee922ca20040db`). The page heads `Game: Stern LOTR (LE)`, `Model: I-0080 (LE: I-00B4)`, `Game first made: Dec 2003 (LE first made: Dec 2009)`. Its document table, in order:",
		_table(["Item", "Location", "Type"], [
			["Complete LOTR Manual (2003)", "lotr/LOTR-2003-Complete.pdf, 100dpi Original Manual", "Scan"],
			["Complete LOTR Manual (2003)", "lotr/LOTR-2003-Complete-hi-res.pdf, High res Original Manual", "Scan"],
			["Section 4 Pink/Blue Pages, missing from the IPDB hosted LOTR Manual (2003)", "lotr/Missing-pgs-58-to-118-from-LOTR-2003.pdf", "Scan"],
			["Section-5 Ch-4 Ball Trough/Optos (in Color)", "lotr/LOTR-Sec5-Ch4-109-111-BallTrough.pdf", "PDF"],
			["LOTR Cabinet Matrix *new*", "lotr/LOTR-Cabinet-Matrix-11x17.pdf", "PDF"],
			["Leg protector Template *new*", "lotr/leg-protector-template.pdf", "PDF"],
			["LOTR LE Manual 2009 Complete to Pg102", "lotr/LOTR-LE-complete-to-pg102.pdf, Draft of a complete LOTR LE Manual - no schematics (yet)", "PDF"],
			["LOTR LE Manual 2009 Find it in Front", "lotr/LOTR-LE-Find-It-In-Front-DR1-10.pdf, Quick Reference guide DR1-10 for LOTR LE", "PDF"],
			["Pages 100-106 which are missing from Stern LOTR LE Manual 2009", "lotr/Stern-2009-LOTR-LE-Missing-Pages-100-to-106.pdf", "Scan"],
			["LOTR LE I/O Driver Board Schematic *new*", "lotr/Sec 5 Chp 4-3 IO-520-5249-schematics-11x17.pdf, SAM I/O Power Driver Board 520-5249-00", "PDF"],
			["LOTR LE Cabinet Matrix *new*", "lotr/LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf, 11x17\" Page to go inside LE lower cabinet.", "PDF"],
			["Stern Shaker Motor Install Instructions", "lotr/stern-revb-shaker.pdf, Scan of Rev B. Shaker Install Instructions", "PDF"],
		]),
		"The LE manual draft, the LE quick reference and the shaker instructions return 404 and have no archived copy; the other LE files are retained.",
		"> Notes: Manual Pages and Schematics given in Red are for LOTR LE only. These are not the same Manual files hosted on the IPDB LOTR page",
		"> Disclaimer: I am only documenting my LOTR LE game wiring *. If you use the above pages, then you do so at your risk.",
		"Under `LOTR LE EXTRA FEATURES INCLUDED`, with the page's separate list lines joined by ` / `:",
		"> Cosmetic changes for \"gold trim\" ( parts list PDF ): Lockbar, Legs, Hinges, and Siderails are plated and polished / Bolts such as leg bolts, hinge bolts are in brass / \"500 Game Limited Edition\" plate and gold grills on speaker panel / Gold trim around backbox / Real backglass with (HD) gold effect",
		"> Playfield Changes: Arwen playfield plastic returns (Yay!) / No mounting holes in playfield plastics / No AOME plastic figures installed / Balrog has LED upgrade / Centre ramp has post upgrade / Playfield Signed by Gary Stern and George Gomez / Extra clearcoats over playfield and nice finish",
		"> Board / Wiring Changes: 520-5249-00 SAM I/O Power Driver used (instead of 520-5137-01 White Star): Fuse numbers and positions changed / BR numbers and positions changed / Helms Deep Rt. (Flash Lamp) moved from Sol #14 to Sol #28 / 520-5300-B4 White Star CPU/Sound Board II /w ATMEL Processor / ROM version 10.xx (shipped with 10.02) / Support on wiring harness for a Shaker Motor with above ROMs / Wiring color changes at CPU and I/O Driver connectors: *This is true for the wiring loom on my machine, Stern may have used different wire colors on your LE.",
		"> Poor quality LE Manual Supplied by Stern: /rant mode=on/ Changes appear to be hand edited with whiteout and a photocopier. It's still got mistakes and not worthy of this great game which was around $5,000 NIB",
		"> Stern Shaker Motor Kit (Rev B) ~ $170 (wiring harness exists in the LE game).",
		"## Adding a hardware knocker",
		"https://firepowerpinball.com/2ya/15-lotr-knocker.html (retained HTML SHA-256 `7482b85e586f8bd22fde29c8d61bbf771216f6515236d78152e53ac5acad95b4`).",
		"> Set #46 -Q24 option to \"knocker\" and turn #34 \"software knocker\" volume to off. On my LOTR LE those are the adjustment settings #'s from the Service Menu.",
		"> Set Q24 option to: coin meter and the \"software knocker\" volume to LOW (50%) or NORMAL (100%) and you swap back to the software knocker.",
		"> Test the knocker on the \"optional Q24 coil test\" by firing that coil (well you can on my LOTR version).",
		"> Here is the circuit diagram and pinouts for a SAM I/O driver board which was on my LOTR LE (check your manual to see if they are the right pins on your game).",
		"## LOTR LE Shaker Motor",
		"Blog post of 30 Sept 2010, https://lotrpinball.blogspot.com/2010/09/lotr-le-shaker-motor.html (retained HTML SHA-256 `b9317e92600d96482502e464c23951a241ab4487bfa138c200c693cd82f3bb08`).",
		"> BTW - Do not be frightened of buying the right kit (Stern rev B) and doing the install.  The LOTR LE was designed to allow you to add this feature.",
		"> The BRN/GRY wire 72\" it talks about on a male connector.  This connects to a BLU/YEL female connector  coming from the head that can be found at the back of the cabinet on an LOTR LE.  It has a single BLU/YEL wire in the same place as the BRN/GRY wire in the 72\" harness.",
		"> The RED/WHT connector is short and will exactly match another RED/WHT connector found in the wire harness on the LOTR LE around the plumb-bob tilt area..",
		"> Doing that would let you take the cover off the shaker motor (for adjustments or oil, in future) without having to remove the Shaker Motor PCB above.",
	]) + "\n"
	bulletin = "\n\n".join([
		"# Stern service bulletin 148: Balrog LED kit",
		"`SB148-Balrog.pdf`, retrieved from https://o.pinside.com/d/92/71/d92717f07a36715dfaabf2aff576ad70aaea1c77.pdf (SHA-256 `db1529d1ef0b16c58c890eb5943ba11d8db2d8bf7844f97f86b28caa8ca8b979`). One page. The announcement was read from the PDF's text layer; the installation steps, which are drawn, from the page rendered at 150 dpi.",
		"Header: `Nº 148 SERVICE BULLETIN`, Stern Pinball, Inc. Parts Sales & Technical Support. `TO: Parts & Service Mgrs.`, `DATE: April 29, 2004`, `SUBJ: Balrog LED Kit!`",
		"> The initial production run of Lord of the Rings Pinball, used a #89 Bayonet bulb to light up the Balrog (Motor & Gate) Asm. Current production is using a LED (Red) Module.  Although the LED (Red) Module is not as bright, it is more reliable!",
		"> Your LOTR Pinball may already have the LED Module installed in the Balrog, but your game manual may not have included the part numbers on Page 87 (the Blue Pages).  You will be able to easily tell the differences of the Module & Socket upon inspection (view 6C & 3B in the graphic).  For the LED (Red) Module Bayonet 12.8v 20-25mA, use SPI Part # 112-5023-02 and for the 2-Lug Laydown Bayonet Socket (Modified), use SPI Part # 077-5003-00-80.",
		"> The optional Balrog LED Kit is now available (ask for SPI Part # 502-5022-00).",
		"> Use the SINGLE COIL TEST (Q32) to check your bulb operation.",
		"The drawn panel `Balrog LED Module Installation SPI Kit Nr.: 502-5022-00` lists the kit as `LED (Red) Module Bayonet 12.8v 20-25mA (112-5023-02), 2-Lug Laydown Bayonet Socket, Modified (077-5003-00-80), and Shrink-Wrap Tubing (605-5002-00, 2 pcs.)`. Step 4 unsolders `the Orange (ORG) and the Black-Gray (BLK-GRY) wires from the lugs of the Lamp socket`; step 6 solders `the ORG wire to the outside lug (6A) and ... the BLK-GRY to center lug (6B)`; step 10 tests it in `SINGLE COIL TEST ... Q32`.",
	]) + "\n"
	board = "\n\n".join([
		"# I/O Power Driver PCB S.A.M. System (520-5249-00)",
		"`Sec 5 Chp 4-3 IO-520-5249-schematics-11x17.pdf`, a Stern manual chapter the LE owner published as `SAM I/O Power Driver Board 520-5249-00`: https://firepowerpinball.com/2ya/lotr/Sec%205%20Chp%204-3%20IO-520-5249-schematics-11x17.pdf (SHA-256 `ab5c8226945de803b1236db9d06d69043e9a744e7f46fbe140a787a660d15492`). Seven pages, vector; read from the text layer.",
		"Page titles: `I/O POWER DRIVER PCB S.A.M. System (520-5249-00) Schematic (Sheet 1 of 4)` to `(Sheet 4 of 4)` on Section 5, Chapter 4 pages 118-125, `... Component Layout` on page 128 and `... Parts` on page 129.",
		f"The complete parts list of page 129, `{IO_PARTS['title']}`, as printed: the assembly line and items 1-67. Read from the text layer by column with `tools/lotr_le_io_board_parts.py` "
		"(seed `tools/seeds/stern/lord-of-the-rings-limited-edition-2009-io-board-parts.json`); a reference or description printed on two lines is joined with a space. Four cells are given as the page renders them: "
		"the page overprints two words of items 33 and 39 on each other, its text layer drops item 55's ohm sign, and item 62's manufacturer number runs into the next column.",
		f"Header: `{IO_PARTS['header']}`.",
		_table(["Item", "Qty.", "SPI part number", "(Mfg. P.N.)", "Ref-designator", "Description"],
		       [[e["item"], e["qty"], e["part"], e["mfg"], e["ref"], e["description"]] for e in IO_PARTS["items"]]),
		"So the 520-5249-00 board carries the same driver designators the Limited Edition chart prints: Q1-Q32 for the solenoids, Q33-Q42 for the lamp rows and U10-U17 for the lamp columns.",
	]) + "\n"
	return {
		EXCERPT_DIR / "cabinet-chart.md": chart,
		EXCERPT_DIR / "owner-annotated-manual-pages.md": overlays,
		EXCERPT_DIR / "owner-documentation-pages.md": documentation,
		EXCERPT_DIR / "service-bulletin-148.md": bulletin,
		EXCERPT_DIR / "io-power-driver-520-5249-00.md": board,
	}


EXCERPT_CONTENTS = _excerpt_contents()


def _excerpt(name: str, excerpt_id: str, locator: str, method: str, transcribed_by: str) -> dict:
	path = EXCERPT_DIR / name
	return {
		"id": excerpt_id,
		"locator": locator,
		"method": method,
		"path": path.relative_to(ROOT).as_posix(),
		"reviewed": True,
		"sha256": hashlib.sha256(EXCERPT_CONTENTS[path].encode("utf-8")).hexdigest(),
		"transcribed_by": transcribed_by,
	}


# The identity, driver and sources the edition's earlier identity-only record established, unchanged.
PREVIOUS = json.loads(
	r"""{"driver": {"clone_of": "lotr", "description": "Lord of the Rings, The (10.02 Limited Edition)", "flags": 0, "id": "lotr_le", "manufacturer": "Stern", "physical_compatibility": "identical", "variant_notes": "Stern game ROM revision 10.02, the firmware of the 2009 Limited Edition. PinMAME declares it a clone of lotr sharing init_lotr, which is shared emulator routing, not shared hardware. Against the 2003 machine's root driver it differs only in the CPU game ROM (lotrcpua.a02 against lotrcpua.a00); the display ROM lotrdspa.a00 and the LOTR_SND sound set are the same. Its own flash-lamp test pulses solenoid 28, which the 2003 firmware never drives. It is this edition's production firmware, so it is identical to the machine it describes.", "year": "2008"}, "machine": {"id": "stern.lord-of-the-rings-limited-edition.2009", "ipdb_id": 5558, "kind": "physical_pinball", "manufacturer": "Stern", "model_number": "I-00B4", "name": "Lord of the Rings Limited Edition", "opdb_id": "GrqZX-MDEPd", "year": 2009}, "sources": [{"attribution": "PinMAME contributors", "id": "pinmame.catalog.97aa922bf8e4", "kind": "pinmame_catalog", "license": "BSD-3-Clause", "locator": "PinmameGetGames", "revision": "97aa922bf8e4b6970126192ec1ac1fb0305a4f62", "uri": "https://github.com/vpinball/pinmame"}, {"attribution": "PinMAME contributors", "id": "pinmame.core.97aa922bf8e4", "kind": "pinmame_core", "license": "BSD-3-Clause", "locator": "src/wpc/segames.c:1852-1858 SE128_ROMSTART(lotr_le, \"lotrcpua.a02\") with DE_DMD32ROM8x(\"lotrdspa.a00\") and LOTR_SND, input_ports_lotr_le and init_lotr_le defined as the lotr ones, and CORE_CLONEDEFNV(lotr_le,lotr,\"Lord of the Rings, The (10.02 Limited Edition)\",2008,\"Stern\",de_mSES3,0); src/wpc/segames.c:1498-1500 lotrGameData GEN_WS with se_dmd128x32 and board identifiers SE_BOARDID_520_5068_01 | SE_BOARDID_520_5242_00; src/wpc/driver.c:1751 DRIVERNV(lotr_le)", "revision": "97aa922bf8e4b6970126192ec1ac1fb0305a4f62", "uri": "https://github.com/vpinball/pinmame"}, {"acquired_at": "2026-10-22T00:09:00Z", "attribution": "The Internet Pinball Database", "excerpts": [{"id": "excerpt.lotr-le.ipdb-5558", "locator": "IPDB machine 5558: identity fields, notes and the list of factory changes", "method": "manual", "path": "evidence/excerpts/stern.lord-of-the-rings-limited-edition.2009/ipdb-5558.md", "reviewed": true, "sha256": "5be67f88c8e7923bde1715236e8b6f666a739f6295612eb0f020318c786fa21f", "transcribed_by": "curator, read from the retained page text"}], "id": "ipdb.5558", "kind": "human_review", "license": "NOASSERTION", "locator": "IPDB machine id 5558, The Lord of the Rings (Limited Edition): December 2009, Stern, model number I-00B4, MPU Stern Whitestar (modified), about 500 units, 'Limited Edition version of Stern's 2003 The Lord of the Rings', with the shaker-motor option among its listed factory changes. Retained page text: review-artifacts/lord-of-the-rings-2003/completion-2026-10-21/edition-research/ipdb-5558.txt.", "rights": "Rights not asserted; the retained copy is the page text only, kept locally for curation", "sha256": "e6cda5e6af77e79cf9ccc31c3932a472d35c050304dbe0b325b93eebb498b957", "uri": "https://www.ipdb.org/machine.cgi?id=5558"}, {"acquired_at": "2026-10-21T21:44:19Z", "attribution": "Richard Harvey (firepower), LOTR Pinball blog", "excerpts": [{"id": "excerpt.lotr-le.owner-shop-out-matrix", "locator": "The blog post's hardware passages, and coils chart rows 11-14 and 27-29 with the flash-test note", "method": "manual", "path": "evidence/excerpts/stern.lord-of-the-rings-limited-edition.2009/owner-shop-out-matrix-2010.md", "reviewed": true, "sha256": "2d38193e2bee295031f11e7fbe7571ee5a7e4b4786bb24a653ac309d9dcff3c3", "transcribed_by": "curator, read from the retained post and from the chart rendered at 220 dpi"}], "id": "human-review.lotr-le.owner-report-2010", "kind": "human_review", "license": "NOASSERTION", "locator": "Owner's first-hand report on their own Limited Edition, 'Shop-out Matrix for LOTR LE Cabinet and documentation', 29 Oct 2010: the I/O power driver board is a 520-5249-00 with a 'Z' connector adapting J10, coil 12 is the optional shaker motor, 14 is unused and 28 is the right Helm's Deep flasher. Retained HTML: review-artifacts/lord-of-the-rings-2003/completion-2026-10-21/richard-le-wiring-2010.html.", "rights": "NOASSERTION; the blog asks to be contacted before its content is reused, so only the cited passages are transcribed", "sha256": "ab7dc2457789de5f70aa83d240f9d5e748e5a20ad6fcbf7d9c961551959904c8", "uri": "https://lotrpinball.blogspot.com/2010/10/shopout-pages-for-lotr-le.html"}, {"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external", "id": "runtime.lord-of-the-rings-limited-edition.flash-test", "kind": "runtime_scenario", "license": "NOASSERTION", "locator": "Hash-pinned LibPinMAME run of lotr_le (10.02) from empty NVRAM through the ROM's own DIAG > TEST FLASH LAMPS (scenario tools/harness-scenarios/whitestar/lotr-le-flash-test.json, compact evidence evidence/runtime/whitestar/lord-of-the-rings-limited-edition-flash-test.json built by tools/lotr_flash_test_evidence.py). Each of its eight CYCLING FLASHERS steps pulses exactly solenoids 14, 23, 25-32; the same walk on the 2003 firmware lotr never pulses 28.", "revision": "97aa922bf8e4b6970126192ec1ac1fb0305a4f62", "uri": "internal:evidence/runtime/whitestar/lord-of-the-rings-limited-edition-flash-test.json"}]}"""
)
_PREVIOUS_SOURCES = {source["id"]: source for source in PREVIOUS["sources"]}


def _kept(source_id: str) -> dict:
	"""A source the edition's earlier record already carried, unchanged."""
	return copy.deepcopy(_PREVIOUS_SOURCES[source_id])


LE_SOURCES = [
	_kept(CATALOG),
	_kept(CORE),
	_kept(IPDB),
	_kept(REPORT),
	{
		"acquired_at": "2026-10-23T11:55:04Z",
		"attribution": f"{OWNER}, from Stern's Lord of the Rings cabinet chart",
		"excerpts": [
			_excerpt("cabinet-chart.md", "excerpt.lotr-le.cabinet-chart",
			         "The whole sheet's switch matrix with the dedicated switches, coils detailed chart table and lamp matrix, every cell, header and note",
			         "mixed", "curator, from the PDF text layer by tools/lotr_le_chart_transcription.py, checked against the page rendered at 300 dpi; the drawn marks read from that rendering"),
		],
		"id": CHART_SOURCE,
		"kind": "human_review",
		"license": "NOASSERTION",
		"locator": "LOTR LE Cabinet Matrix, the owner's correction of Stern's 11x17 Lord of the Rings cabinet chart (SPI Nr. 755-5310-80) for his Limited Edition: the complete switch matrix with dedicated switches, coils detailed chart table and lamp matrix with every wire colour and connector, and the switch, coil and lamp location maps. Published at https://firepowerpinball.com/2ya/lotr/LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf and mirrored byte-identically by pinballrebel.com. Structured transcription tools/seeds/stern/lord-of-the-rings-limited-edition-2009-chart.json. Retained PDF: manuals/by-machine/stern.lord-of-the-rings-limited-edition.2009/firepowerpinball/LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf.",
		"rights": "NOASSERTION",
		"sha256": CHART["source"]["sha256"],
		"uri": "https://firepowerpinball.com/2ya/lotr/LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf",
	},
	{
		"acquired_at": "2026-10-23T11:55:05Z",
		"attribution": f"{OWNER}; the scanned pages are Stern's",
		"excerpts": [
			_excerpt("owner-annotated-manual-pages.md", "excerpt.lotr-le.owner-annotated-manual-pages",
			         "Every overlay on the seven pages, with the printed value it covers",
			         "manual", "curator, overlay texts from the PDF text layer, each placement checked on the rendered page"),
		],
		"id": PAGES,
		"kind": "human_review",
		"license": "NOASSERTION",
		"locator": "Scans of Stern's Lord of the Rings manual Section 5 pages 100-106 (the 2003 manual's coils chart, backbox I/O board wiring, board layout, G.I. wiring, switch and lamp wiring, terminal strips and flipper circuit), which the owner says were missing from the LE manual Stern supplied, with his vector overlays giving his LE's wiring: #14 not connected, #28 the right Helm's Deep flasher, the 520-5249-00 board, and changed wire colours. Retained PDF: manuals/by-machine/stern.lord-of-the-rings-limited-edition.2009/firepowerpinball/Stern-2009-LOTR-LE-Missing-Pages-100-to-106.pdf.",
		"rights": "NOASSERTION; the scanned pages remain Stern's",
		"sha256": "3745b609874e0f48994101a57067a8a78c0bb62c49cc74338c534c26926c5d74",
		"uri": "https://firepowerpinball.com/2ya/lotr/Stern-2009-LOTR-LE-Missing-Pages-100-to-106.pdf",
	},
	{
		"acquired_at": "2026-10-23T11:55:06Z",
		"attribution": OWNER,
		"excerpts": [
			_excerpt("owner-documentation-pages.md", "excerpt.lotr-le.owner-documentation-pages",
			         "The documentation page's document table and LE feature lists, the knocker page's Q24 passages and the shaker post's harness passages",
			         "manual", "curator, read from the retained HTML"),
		],
		"id": OWNER_PAGE,
		"kind": "human_review",
		"license": "NOASSERTION",
		"locator": "The owner's Lord of the Rings documentation page: his LE's model number I-00B4, the LE documents he published, and his lists of the edition's cosmetic, playfield and board/wiring changes (520-5249-00 SAM I/O power driver board, Helm's Deep right flasher moved from 14 to 28, shaker-motor harness, wire colour changes). Retained HTML: manuals/by-machine/stern.lord-of-the-rings-limited-edition.2009/firepowerpinball/14-lotr.html.",
		"rights": "NOASSERTION",
		"sha256": "076909fb4a19067f13d0ac8377cd4074766bf31d941e51f58aee922ca20040db",
		"uri": f"{FIREPOWER}14-lotr.html",
	},
	{
		"acquired_at": "2026-10-23T12:00:48Z",
		"attribution": OWNER,
		"id": KNOCKER_PAGE,
		"kind": "human_review",
		"license": "NOASSERTION",
		"locator": "The owner's page on fitting a hardware knocker to his LE on the optional Q24 driver through adjustment #46 Q24 option; transcribed in excerpt excerpt.lotr-le.owner-documentation-pages. Retained HTML: manuals/by-machine/stern.lord-of-the-rings-limited-edition.2009/firepowerpinball/15-lotr-knocker.html.",
		"rights": "NOASSERTION",
		"sha256": "7482b85e586f8bd22fde29c8d61bbf771216f6515236d78152e53ac5acad95b4",
		"uri": f"{FIREPOWER}15-lotr-knocker.html",
	},
	{
		"acquired_at": "2026-10-23T12:25:05Z",
		"attribution": f"{OWNER}, LOTR Pinball blog",
		"id": SHAKER_POST,
		"kind": "human_review",
		"license": "NOASSERTION",
		"locator": "LOTR LE Shaker Motor, 30 Sept 2010: the LE's harness ends in a single-wire BLU/YEL connector at the back of the cabinet and a RED/WHT connector near the plumb-bob tilt for Stern's Rev B shaker kit, which brings its own shaker motor board; transcribed in excerpt excerpt.lotr-le.owner-documentation-pages. Retained HTML: manuals/by-machine/stern.lord-of-the-rings-limited-edition.2009/lotrpinball-blog/lotr-le-shaker-motor.html.",
		"rights": "NOASSERTION; the blog asks to be contacted before its content is reused, so only the cited passages are transcribed",
		"sha256": "b9317e92600d96482502e464c23951a241ab4487bfa138c200c693cd82f3bb08",
		"uri": "https://lotrpinball.blogspot.com/2010/09/lotr-le-shaker-motor.html",
	},
	{
		"acquired_at": "2026-10-21T21:47:05Z",
		"attribution": "Stern Pinball, Inc. Parts Sales & Technical Support",
		"excerpts": [
			_excerpt("service-bulletin-148.md", "excerpt.lotr-le.service-bulletin-148",
			         "The whole bulletin: announcement, kit contents and the wiring steps",
			         "mixed", "curator, announcement from the PDF text layer, drawn steps from the page rendered at 150 dpi"),
		],
		"id": SB148,
		"kind": "service_bulletin",
		"license": "NOASSERTION",
		"locator": "Stern service bulletin 148, 29 April 2004, Balrog LED Kit: production after the initial run lights the Balrog (Q32) with a red LED module 112-5023-02 in socket 077-5003-00-80 instead of the #89 bulb. Retained PDF: review-artifacts/lord-of-the-rings-2003/completion-2026-10-21/SB148-Balrog.pdf.",
		"rights": "NOASSERTION; Stern's document",
		"sha256": "db1529d1ef0b16c58c890eb5943ba11d8db2d8bf7844f97f86b28caa8ca8b979",
		"uri": "https://o.pinside.com/d/92/71/d92717f07a36715dfaabf2aff576ad70aaea1c77.pdf",
	},
	{
		"acquired_at": "2026-10-23T11:55:05Z",
		"attribution": f"Stern Pinball, Inc.; published by {OWNER} as the LE's I/O driver board schematic",
		"excerpts": [
			_excerpt("io-power-driver-520-5249-00.md", "excerpt.lotr-le.io-power-driver-520-5249-00",
			         "The page titles and the complete parts list of page 129, assembly line and items 1-67",
			         "mixed", "curator, from the PDF text layer by tools/lotr_le_io_board_parts.py, the four rendered cells read at 220 dpi"),
		],
		"id": IO_BOARD,
		"kind": "manual",
		"license": "NOASSERTION",
		"locator": "Stern manual Section 5, Chapter 4 pages 118-129: I/O Power Driver PCB S.A.M. System (520-5249-00) schematic sheets 1-4, component layout and parts list, the board the LE owner reports in his Limited Edition. Retained PDF: manuals/by-machine/stern.lord-of-the-rings-limited-edition.2009/firepowerpinball/Sec 5 Chp 4-3 IO-520-5249-schematics-11x17.pdf.",
		"rights": "NOASSERTION; Stern's document",
		"sha256": "ab5c8226945de803b1236db9d06d69043e9a744e7f46fbe140a787a660d15492",
		"uri": f"{FIREPOWER}lotr/Sec%205%20Chp%204-3%20IO-520-5249-schematics-11x17.pdf",
	},
	_kept(RUNTIME_FLASH),
	{
		"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		"id": RUNTIME_GAMEPLAY,
		"kind": "runtime_scenario",
		"license": "NOASSERTION",
		"locator": f"Two hash-pinned LibPinMAME runs of one game, served and played by closing every ordinary playfield switch twice, on lotr_le (10.02) and on lotr (10.00) (scenarios tools/harness-scenarios/whitestar/lotr-le-gameplay.json and lotr-gameplay.json, compact evidence {RUNTIME_GAMEPLAY_PATH} built by tools/lotr_le_gameplay_evidence.py). 10.02 switches 28 on and off together with 14 every time, each pair of solenoid callbacks within 1 ms of each other on the harness clock; 10.00 drives 14 and never 28.",
		"revision": LIBRARY_REVISION,
		"uri": f"internal:{RUNTIME_GAMEPLAY_PATH}",
	},
]
LE_SOURCE_IDS = {source["id"] for source in LE_SOURCES}

# Device identities the edition changes.
HELMS_DEEP_RIGHT = "device.helms-deep-right-flasher"
SHAKER = "device.shaker-motor"
UNUSED_14 = "device.solenoid-14-unused"
BALROG_FLASHER = "device.balrog-flasher"


def _add_refs(provenance: dict, *refs: str) -> None:
	for ref in refs:
		if ref not in provenance["source_refs"]:
			provenance["source_refs"].append(ref)


def _append_note(device: dict, note: str) -> None:
	physical = device.setdefault("physical", {})
	physical["notes"] = f"{physical['notes']} {note}" if physical.get("notes") else note


def _words(text: str) -> str:
	"""A printed cell compared by its words: the chart spaces ``( K ) EEP`` where the 2003 table has ``(K) EEP``."""
	return " ".join(text.replace("( ", "(").replace(" )", ")").split()).upper()


def _switch(device: dict, address: int) -> None:
	printed = SWITCHES[address]
	column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
	col, rw = SW_COLS[column], SW_ROWS[row]
	wiring = {
		"board": "CPU/Sound Board II",
		"drive_connection": col["connector"],
		"drive_wire": col["wire"],
		"driver_transistor": col["drive"],
		"return_component": rw["ic"],
		"return_connection": rw["connector"],
		"return_wire": rw["wire"],
	}
	if device.get("wiring") != wiring:
		raise SystemExit(f"switch {address}: the LE chart's wiring {wiring} is not the 2003 machine's {device.get('wiring')}")
	base_record = base.SW[address]
	compared = (
		(_words(printed["name"]), _words(base_record.get("name") or "NOT USED")),
		(printed.get("location"), base_record.get("location")),
		# The 2003 transcription keeps a part cell that points at a note in its own note field.
		(printed.get("part"), base_record.get("part") or (base_record.get("note") or "").split(":")[0] or None),
	)
	if any(le != original for le, original in compared):
		raise SystemExit(f"switch {address}: the LE chart prints {printed}, the 2003 table {base_record}")
	_add_refs(device["provenance"], CHART_SOURCE)
	readings = []
	if column in SWITCH_COLUMN_OVERLAY:
		readings.append(f"its column drive as {SWITCH_COLUMN_OVERLAY[column]}")
	if row in SWITCH_ROW_OVERLAY:
		readings.append(f"its row return as {SWITCH_ROW_OVERLAY[row]}")
	if readings:
		_append_note(device, (
			f"The LE owner's annotated manual page 104 reads {' and '.join(readings)} on his machine; his LE cabinet chart, "
			f"followed here, prints {col['wire'] if column in SWITCH_COLUMN_OVERLAY else rw['wire']}"
			+ (f" and {rw['wire']}" if column in SWITCH_COLUMN_OVERLAY and row in SWITCH_ROW_OVERLAY else "")
			+ ", as the 2003 manual does."
		))


def _lamp(device: dict, address: int) -> None:
	printed = LAMPS[address]
	column, row = (address - 1) % 8 + 1, (address - 1) // 8 + 1
	col, rw = LA_COLS[column], LA_ROWS[row]
	old = device["wiring"]
	wiring = dict(old)
	wiring.update({
		"drive_connection": rw["connector"],
		"drive_wire": rw["wire"],
		"driver_transistor": rw["drive"],
		"return_component": col["ic"],
		"return_connection": col["connector"],
		"return_wire": col["wire"],
	})
	for field in ("drive_connection", "driver_transistor", "return_component", "return_connection"):
		if wiring[field] != old[field]:
			raise SystemExit(f"lamp {address}: the LE chart moves {field} from {old[field]} to {wiring[field]}")
	base_lamp = base.LAMPS[address]
	# The 2003 scan prints LEGOLES for lamps 15 and 33 and its 300 dpi reading took Grn. as Gm.; the chart prints LEGOLAS and Grn.
	if printed["bulb"].replace("Grn.", "Gm.") != base_lamp["bulb"] or _words(printed["name"]).replace("LEGOLAS", "LEGOLES") != _words(base_lamp["name"]):
		raise SystemExit(f"lamp {address}: the LE chart prints {printed}, the 2003 table {base_lamp}")
	device["wiring"] = wiring
	_add_refs(device["provenance"], CHART_SOURCE, IO_BOARD)
	changed = [f"{label} {wiring[key]} where the 2003 manual prints {old[key]}" for key, label in (("drive_wire", "row wire"), ("return_wire", "column wire")) if wiring[key] != old[key]]
	if changed:
		_append_note(device, f"The Limited Edition chart prints {' and '.join(changed)}; the LE owner's annotated manual page 104 reads the same.")


# Coil rows whose printed name the LE chart changes; every other row's name and coil type must be the 2003 table's.
RENAMED_COILS = {15: "LEFT FLIPPER (50v YEL/BLK)", 16: "RIGHT FLIPPER (50v YEL/BLK)", 24: "OPTIONAL COIL (KNOCKER)"}


def _coil_type(text: str | None) -> str:
	return " ".join((text or "").replace("20.5", "20\u00bd").replace(" / ", " ").split())


def _check_coil_row(address: int) -> None:
	printed, original = COILS[address], base.COILS[address]
	expected_name = RENAMED_COILS.get(address, original.get("name"))
	if printed["name"] != expected_name or _coil_type(printed.get("coil")) != _coil_type(original.get("coil_spec")):
		raise SystemExit(f"coil {address}: the LE chart prints {printed}, the 2003 table {original}")


def _coil(device: dict, record: dict, address_label: str) -> None:
	if record in COILS.values():
		_check_coil_row(record["address"])
	old = device["wiring"]
	wiring = dict(old)
	for src, dst in (("power_wire", "power_wire"), ("power_connection", "power_connection"), ("control_wire", "control_wire"), ("control_connection", "control_connection")):
		if record.get(src):
			wiring[dst] = record[src]
	if record.get("power_voltage"):
		wiring["nominal_voltage_v"] = float(record["power_voltage"].split("v")[0])
	if wiring.get("driver_transistor") != record["transistor"]:
		raise SystemExit(f"{address_label}: the LE chart drives it from {record['transistor']}, the 2003 record from {wiring.get('driver_transistor')}")
	if wiring["control_connection"] != old["control_connection"]:
		raise SystemExit(f"{address_label}: the LE chart moves its control line from {old['control_connection']} to {wiring['control_connection']}")
	device["wiring"] = wiring
	_add_refs(device["provenance"], CHART_SOURCE)
	if record in COILS.values():
		_add_refs(device["provenance"], IO_BOARD)
	labels = {"power_wire": "power line", "power_connection": "power connection", "control_wire": "control line", "nominal_voltage_v": "voltage"}
	changed = [f"{labels[key]} {wiring[key]} where the 2003 manual prints {old.get(key)}" for key in labels if wiring.get(key) != old.get(key)]
	if changed:
		_append_note(device, f"The Limited Edition chart prints {'; '.join(changed)}.")


def _transform_outputs(outputs: list[dict]) -> list[dict]:
	result = []
	for device in outputs:
		group, address = device["binding"]["group"], device["binding"]["device"]
		if group == "pinmame.output.lamp" and address <= 80:
			_lamp(device, address)
		elif group == "pinmame.output.lamp":
			_add_refs(device["provenance"], CORE)
		elif group == "pinmame.output.gi":
			_add_refs(device["provenance"], PAGES)
			_append_note(device, (
				"On the Limited Edition the LE owner's annotated G.I. page (manual page 103) reads circuit 2 as WHT-BLK to WHT-YEL, circuit 3 as YEL-GRY to YEL-GRN and circuit 4 as GRY-YEL to WHT-VIO, "
				"where the 2003 page prints YEL to WHT-YEL, GRN to WHT-GRN and VIO to WHT-VIO; circuit 1 is unchanged. Nothing else about the circuits differs."
			))
		elif group == "pinmame.output.solenoid" and address == 12:
			device = _shaker(device)
		elif group == "pinmame.output.solenoid" and address == 14:
			device = _unused_14(device)
		elif group == "pinmame.output.solenoid" and address == 28:
			continue
		elif group == "pinmame.output.solenoid" and address in (46, 48):
			record = COILS[int(device["wiring"]["driver_transistor"][1:])]
			_coil(device, record, f"solenoid {address}")
			_append_note(device, f"The Limited Edition chart prints this row as {record['name']}.")
			_append_note(device, COIL_OVERLAY_NOTES[address])
		elif group == "pinmame.output.solenoid" and device.get("wiring", {}).get("driver_transistor"):
			if address in (33, 34, 35):
				# The chart abbreviates the board UK 3X Trans. Driver Board; the 2003 record's name is kept.
				_coil(device, AUX[base.UK_AUX[address]], f"aux {address}")
			else:
				number = int(device["wiring"]["driver_transistor"][1:])
				_coil(device, COILS[number], f"solenoid {address}")
			if address in COIL_OVERLAY_NOTES:
				_append_note(device, COIL_OVERLAY_NOTES[address])
			if address == 24:
				_add_refs(device["provenance"], KNOCKER_PAGE)
				_append_note(device, "The Limited Edition chart names this row OPTIONAL COIL (KNOCKER). The LE owner fitted a hardware knocker here, selected by adjustment #46 Q24 option set to knocker, and fired it from the single coil test.")
			if device["id"] == BALROG_FLASHER:
				_add_refs(device["provenance"], SB148, OWNER_PAGE)
				_append_note(device, (
					"The LE owner lists 'Balrog has LED upgrade' among the edition's playfield changes. Stern's service bulletin 148 (April 2004) describes it: after the initial run the Balrog is lit by a red LED module, "
					"112-5023-02 (12.8v, 20-25mA) in the modified 2-lug socket 077-5003-00-80, soldered to the flasher's two wires (the bulletin names them ORG and BLK-GRY), instead of the #89 bulb the chart still prints. It is dimmer than the bulb and is still driven as Q32."
				))
		result.append(device)
	result.append(_helms_deep_right(next(o for o in outputs if o["id"] == HELMS_DEEP_RIGHT)))
	return sorted(result, key=lambda o: (o["binding"]["group"], o["binding"]["device"]))


def _shaker(previous: dict) -> dict:
	record = COILS[12]
	return {
		"aliases": [{"namespace": "pinmame.solenoid", "value": "12"}, {"namespace": "manual.address", "value": "#12"}],
		"availability": "optional",
		"binding": {"device": 12, "group": "pinmame.output.solenoid"},
		"id": SHAKER,
		"kind": "motor",
		"label": "Shaker Motor",
		"physical": {"notes": (
			"Printed #12 OPTIONAL SHAKER MOTOR on the Limited Edition chart, driven by Q12 on control line BLU-YEL at J9-P5, with no power line, voltage or part printed. "
			"IPDB lists the option to add a shaker motor among the edition's factory changes, with the shaker code added to 10.02. The LE harness carries the BLU-YEL drive line to a single-wire connector at the back of the cabinet, "
			"plus a RED/WHT supply connector near the plumb-bob tilt, for Stern's Rev B shaker kit, which brings its own motor and shaker motor board and mounts on the cabinet floor; the LE owner fitted one. "
			"No shaker is fitted from the factory, and the gameplay runs never drove 12 with 10.02's default settings. On the 2003 machine this driver is NOT USED."
		)},
		"provenance": {"source_refs": [CHART_SOURCE, IPDB, SHAKER_POST, OWNER_PAGE, CORE], "status": "validated"},
		"roles": ["cabinet.shaker"],
		"spatial": {"provenance": {"source_refs": [SHAKER_POST, CHART_SOURCE], "status": "validated"}, "reason": "cabinet_or_service", "status": "not_applicable"},
		"wiring": {"board": previous["wiring"]["board"], "control_connection": record["control_connection"], "control_wire": record["control_wire"], "driver_transistor": record["transistor"]},
	}


def _unused_14(previous: dict) -> dict:
	record = COILS[14]
	return {
		"aliases": copy.deepcopy(previous["aliases"]),
		"availability": "unused",
		"binding": {"device": 14, "group": "pinmame.output.solenoid"},
		"id": UNUSED_14,
		"kind": "coil",
		"label": "Unused Solenoid 14",
		"physical": {"notes": (
			f"Printed #14 {record['name']} on the Limited Edition chart, its row shaded grey with no power line, voltage or bulb, and its control cells still printing {record['control_wire']} at {record['control_connection']}: "
			"the wire the 2003 machine runs from J9-P7 to its right Helm's Deep flasher, which the edition moves to J6-P4 and driver 28. The LE owner's annotated manual pages 100 and 101 read 'NOT USED N.C. J9-P7' and 'N.C. NOT USED (See #28 J6-4)'. "
			"Nothing is connected, yet the 10.02 firmware still drives 14: in its own flash-lamp test and in play it switches 14 and 28 together every time, each pair of transitions reaching the harness within 1 ms of each other, so a cabinet wired like the 2003 machine would still light the flasher. "
			"That mirror is what PinMAME publishes here; on the Limited Edition no load answers it."
		)},
		"provenance": {"source_refs": [CHART_SOURCE, PAGES, REPORT, OWNER_PAGE, RUNTIME_FLASH, RUNTIME_GAMEPLAY, CORE], "status": "validated"},
		"spatial": {"provenance": {"source_refs": [CHART_SOURCE, PAGES], "status": "validated"}, "reason": "unused", "status": "not_applicable"},
		"wiring": {"board": "I/O Power Driver Board", "control_connection": record["control_connection"], "driver_transistor": record["transistor"]},
	}


def _helms_deep_right(previous: dict) -> dict:
	record = COILS[28]
	device = copy.deepcopy(previous)
	device["aliases"] = [{"namespace": "pinmame.solenoid", "value": "28"}, {"namespace": "manual.address", "value": "#28"}]
	device["binding"] = {"device": 28, "group": "pinmame.output.solenoid"}
	device["physical"] = {"notes": (
		f"Printed #28 {record['name']} on the Limited Edition chart, in low current group 2, bulb type {record['coil']}. The 2003 machine wires this flasher to driver 14; on the Limited Edition the LE owner's report, "
		"his chart and his annotated manual pages all move it to Q28, control line BLU-BLK at J6-P4, and his page lists 'Helms Deep Rt. (Flash Lamp) moved from Sol #14 to Sol #28' among the board changes. "
		"The 10.02 firmware drives 28 in its flash-lamp test, which 10.00 never does, and in play switches 28 together with 14. The chart prints power line YEL-ORG at J6-P10 and 20v DC; "
		"the 2003 manual prints this flasher's power as ORG at J6-P10, 50v DC, on driver 14. "
		"The retained recreations, scripted for 10.00, bind the flasher at 14, which 10.02 also drives."
	)}
	device["provenance"] = {"source_refs": [CHART_SOURCE, REPORT, PAGES, OWNER_PAGE, RUNTIME_FLASH, RUNTIME_GAMEPLAY, IO_BOARD, CORE, *previous["provenance"]["source_refs"]], "status": "validated"}
	device["wiring"] = {
		"board": previous["wiring"]["board"],
		"control_connection": record["control_connection"],
		"control_wire": record["control_wire"],
		"driver_transistor": record["transistor"],
		"nominal_voltage_v": float(record["power_voltage"].split("v")[0]),
		"power_connection": record["power_connection"],
		"power_wire": record["power_wire"],
		"voltage_type": "dc",
	}
	for placement in device["spatial"]["placements"]:
		_add_refs(placement["provenance"], CHART_SOURCE, PAGES)
	return device


def _transform_inputs(inputs: list[dict]) -> list[dict]:
	for device in inputs:
		group, address = device["binding"]["group"], device["binding"]["device"]
		if group == "pinmame.input.switch" and 1 <= address <= 64:
			_switch(device, address)
		elif group == "pinmame.input.switch" and address in base.DEDICATED_MANUAL:
			printed, original = DEDICATED[base.DEDICATED_MANUAL[address]], next(d for d in base.transcription["switch_matrix"]["dedicated_switches"] if d["address"] == base.DEDICATED_MANUAL[address])
			expected_name = (original["name"] or "NOT USED") + (f" (In Test: {original['in_test']})" if original.get("in_test") else "")
			compared = (
				*((printed[field], original[field]) for field in ("connector", "ic", "wire")),
				(_words(printed["name"]).replace(".", ""), _words(expected_name).replace(".", "")),
				(printed.get("part"), original.get("part")),
				# The chart leaves DS-3's location cell blank; the 2003 table prints on Cabinet Side.
				(printed.get("location"), original.get("location") if printed["address"] != "DS-3" else None),
			)
			if any(le != old for le, old in compared):
				raise SystemExit(f"{printed['address']}: the LE chart prints {printed}, the 2003 table {original}")
			_add_refs(device["provenance"], CHART_SOURCE)
	return inputs


def _add_placement_refs(collection: list[dict]) -> None:
	for device in collection:
		for placement in device.get("spatial", {}).get("placements", []):
			_add_refs(placement["provenance"], CHART_SOURCE, PAGES)


def _driver() -> dict:
	driver = copy.deepcopy(PREVIOUS["driver"])
	driver["variant_notes"] = (
		"Stern game ROM revision 10.02, the firmware of the 2009 Limited Edition. PinMAME declares it a clone of lotr sharing init_lotr, which is shared emulator routing, not shared hardware. "
		"Against the 2003 machine's root driver it differs only in the CPU game ROM (lotrcpua.a02 against lotrcpua.a00); the display ROM lotrdspa.a00 and the LOTR_SND sound set are the same. "
		"It drives the right Helm's Deep flasher on both 14 and 28, switching them together, where 10.00 drives 14 alone; the Limited Edition wires the flasher to 28. "
		"It is this edition's production firmware, so it is identical to the machine it describes."
	)
	return driver


def _sources() -> list[dict]:
	carried = [copy.deepcopy(source) for source in base.definition["sources"] if source["id"] not in DROPPED_BASE_SOURCES | LE_SOURCE_IDS]
	return [copy.deepcopy(source) for source in LE_SOURCES] + carried


def _used_refs(definition: dict) -> set[str]:
	used: set[str] = set()

	def walk(node) -> None:
		if isinstance(node, dict):
			for key, value in node.items():
				if key == "source_refs":
					used.update(value)
				else:
					walk(value)
		elif isinstance(node, list):
			for value in node:
				walk(value)

	for collection in ("inputs", "outputs", "displays", "mechanisms", "relationships", "conflicts"):
		walk(definition.get(collection, []))
	return used


def _build_definition() -> dict:
	derived = copy.deepcopy(base.definition)
	derived["machine"] = copy.deepcopy(PREVIOUS["machine"])
	derived["drivers"] = [_driver()]
	derived["knowledge"] = {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"}
	derived["inputs"] = _transform_inputs(derived["inputs"])
	derived["outputs"] = _transform_outputs(derived["outputs"])
	_add_placement_refs(derived["inputs"])
	_add_placement_refs([o for o in derived["outputs"] if o["id"] != HELMS_DEEP_RIGHT])
	for display in derived["displays"]:
		_add_refs(display["provenance"], CORE)
	for mechanism in derived["mechanisms"]:
		_add_refs(mechanism["provenance"], CHART_SOURCE)
		if mechanism["id"] == "mechanism.ring-magnet":
			_add_refs(mechanism["provenance"], PAGES)
			mechanism["behavior"] += (
				" On the Limited Edition's 520-5249-00 board the LE owner's annotated manual page 101 numbers the magnet's fuse F7, 4A, with \"*May need 5A S.B.\"; F20 is the 2003 board's number."
			)
	used = _used_refs(derived)
	derived["sources"] = _sources()
	missing = used - {source["id"] for source in derived["sources"]}
	if missing:
		raise SystemExit(f"the Limited Edition cites sources it does not carry: {sorted(missing)}")
	# The catalog source identifies the driver rather than any device.
	unused = LE_SOURCE_IDS - used - {CATALOG}
	if unused:
		raise SystemExit(f"the Limited Edition adds sources nothing cites: {sorted(unused)}")
	return derived


definition = _build_definition()
placement_total = sum(len(d.get("spatial", {}).get("placements", [])) for c in ("inputs", "outputs") for d in definition[c])
if placement_total != base.placement_total:
	raise SystemExit(f"the Limited Edition carries {placement_total} placements, the 2003 machine {base.placement_total}")


def _base_section(heading: str) -> str:
	"""One section of the 2003 machine's knowledge note, verbatim, so the two notes cannot drift apart."""
	marker = f"\n## {heading}\n"
	start = base.knowledge_note.index(marker) + 1
	end = base.knowledge_note.find("\n## ", start + len(marker))
	return base.knowledge_note[start:end if end != -1 else None].rstrip("\n")


def _lamp_wire_changes() -> list[str]:
	lines = []
	for column in range(1, 9):
		le, old = LA_COLS[column], base.LA_COLS[column]
		if le["wire"] != old["wire"]:
			lines.append(f"lamp column {column} ({le['connector']}, {le['ic']}) {old['wire']} -> {le['wire']}")
	for row in range(1, 11):
		le, old = LA_ROWS[row], base.LA_ROWS[row]
		if le["wire"] != old["wire"]:
			lines.append(f"lamp row {row} ({le['connector']}, {le['drive']}) {old['wire']} -> {le['wire']}")
	return lines


_lamp_changes = "- lamp wires: " + "; ".join(_lamp_wire_changes()) + "."

knowledge_note = f"""# The Lord of the Rings Limited Edition (Stern, 2009)

Coverage: **{definition['coverage']['status']} - the 2003 machine's playfield, matrices, mechanisms and {placement_total} validated placements, carried to this edition because its own cabinet chart prints the same switch, lamp and coil tables and the same playfield maps, with the edition's own wiring, its right Helm's Deep flasher moved to driver 28, its optional shaker motor and its 10.02 firmware.** The 2003 production machine's record, `stern.lord-of-the-rings.2003`, holds the evidence the shared parts rest on, and its knowledge note explains it in full; the sections at the end of this note are copied from it.

## Identity

IPDB 5558 (`ipdb-5558` excerpt) lists The Lord of the Rings (Limited Edition) as a Stern game of December 2009, model number I-00B4, on a "Stern Whitestar (modified)" MPU, about 500 units, and calls it the "Limited Edition version of Stern's 2003 'The Lord of the Rings'". OPDB's record `GrqZX-MDEPd`, "Lord of the Rings (LE)", carries the same IPDB number; the 2003 machine is `GrqZX-MD15w`. The LE owner whose documents this record rests on gives the same model number and "LE first made: Dec 2009". The year here is the physical build year. PinMAME's catalog dates the `lotr_le` firmware 2008, and that date stays on the driver.

PinMAME has one driver for this edition, `lotr_le` (10.02). It is declared a clone of `lotr` and shares `init_lotr`, so the emulator routes it exactly like the 2003 firmware. Against that machine's root driver it changes only the CPU game ROM, `lotrcpua.a02` for `lotrcpua.a00`, and keeps the display ROM `lotrdspa.a00` and the `LOTR_SND` set (`src/wpc/segames.c:1852-1858`). A string search of both ROM sets finds the service menus' switch, lamp and coil names in that shared display ROM and none in either CPU ROM; its coil table spells each number in letters from `a` for 0, so `#be FLASH:HELMS DEEP RT` is 14 and `#ci NOT USED` is 28. 10.02 therefore names every address exactly as 10.00 does; the names cannot tell the editions apart and are evidence for neither.

## Why this is its own record

Shared routing does not make shared hardware, and three independent kinds of evidence say the hardware changed:

- **The factory list.** IPDB's list of factory changes includes "Game has the option to add a Shaker Motor", which the 2003 game never had, and quotes Lonnie Ropp's confirmation that the shaker code was added to the original code and secured with a new PAL chip version.
- **An owner's first-hand documents.** Richard Harvey ("firepower") documented his new-in-box Limited Edition on a blog and a documentation page: a report that the cabinet chart Stern stapled into the LE was the 2003 one and that "wire colors and 2 solenoids positions were changed"; a corrected LE cabinet chart; the manual's Section 5 pages 100-106 annotated with his machine's wiring; and a list of the edition's changes, including "520-5249-00 SAM I/O Power Driver used (instead of 520-5137-01 White Star)" and "Helms Deep Rt. (Flash Lamp) moved from Sol #14 to Sol #28".
- **The firmware.** 10.02 drives the right Helm's Deep flasher on 14 and 28 together, 10.00 on 14 alone. Hash-pinned runs of each ROM's own flash-lamp test (`evidence/runtime/whitestar/lord-of-the-rings-flash-test.json`, `{RUNTIME_FLASH_PATH}`) and of a served and played game (`{RUNTIME_GAMEPLAY_PATH}`) show 10.02 switching 28 on and off together with 14 every time, each pair of solenoid callbacks reaching the harness within 1 ms of each other, and 10.00 never touching 28.

## The Limited Edition evidence

No factory Limited Edition document is available. The owner says Stern supplied the LE with a manual hand-edited from the 2003 one, "with whiteout and a photocopier", still with mistakes and missing pages 100-106; his own draft of a complete LE manual, his LE quick reference and Stern's shaker kit instructions are no longer online and were never archived. What is retained:

- **The LE cabinet chart** (`cabinet-chart` excerpt, structured as `tools/seeds/stern/lord-of-the-rings-limited-edition-2009-chart.json`). Stern's 11x17 Lord of the Rings cabinet chart (SPI Nr. 755-5310-80) as the owner corrected it for his LE and published it "to go inside LE lower cabinet". It is the edition's only complete wiring table, so the structured wiring follows it. Its switch matrix, dedicated switches and lamp matrix match the 2003 manual's cell for cell - every name, location, switch part number and bulb - apart from four printing differences: it spells lamps 15 and 33 LEGOLAS where the 2003 scan prints LEGOLES, prints lamp 5's number as `4`, its green POTD bulbs read `Grn.` where the 2003 transcription read `Gm.`, and it leaves DS-3's location cell blank where the 2003 manual prints `on Cabinet Side`. Its coil table matches too, except rows #12, #14 and #28 and the wire colours. The chart also carries the switch, coil and lamp location maps of the playfield.
- **The annotated manual pages** (`owner-annotated-manual-pages` excerpt). The scans are the 2003 manual's own Section 5 pages - page 100 matches Stern's reissue of the 2003 manual cell for cell - so only the owner's overlays describe the LE. They agree with the chart on rows 14 and 28, the 520-5249-00 board and the lamp wiring (page 100 still prints 12 NOT USED; the shaker on 12 rests on the chart, the owner's notes and IPDB's change list), and disagree with it on several wire colours and on which J10 pins feed the flippers (see below).
- **The owner's documentation, knocker and shaker pages** (`owner-documentation-pages` excerpt).
- **Stern's 520-5249-00 I/O power driver board schematic** (`io-power-driver-520-5249-00` excerpt): the board carries the same driver designators the chart prints, Q1-Q32 for the solenoids, Q33-Q42 for the lamp rows and U10-U17 for the lamp columns.
- **Stern service bulletin 148** (`service-bulletin-148` excerpt), for the Balrog LED module.

The owner's documents are one person's account of one machine, and he says himself that Stern may have used different wire colours on other LEs. They agree with each other on everything a recreation consumes, and with IPDB's factory list and the firmware on the changed drivers.

## What carries over from the 2003 machine, and why

Every switch, lamp, coil, flasher, the G.I. channel, the display, all {len(definition['mechanisms'])} mechanisms, the {len(definition['relationships'])} relationships and all {placement_total} placements come from the 2003 record, with their evidence: the 2003 manual and its 2022 reissue, three retained recreations of the 2003 machine, the factory drawings the placements were checked on, and harness runs of the 2003 firmware 10.00 (the stacking opto and the 19-LED board). That evidence was gathered on the 2003 machine. It holds for the LE because:

- the LE chart prints the same switch matrix, dedicated switches, lamp matrix and coil set, cell for cell but for the printing differences above, and the same switch, coil and lamp location maps; the curator (`tools/curate_lord_of_the_rings_le.py`) refuses to build if any other switch, dedicated-switch or lamp cell, connector, driver or IC differs from the 2003 tables;
- the owner's annotated pages keep the 2003 under-playfield drawing (page 105) and the switch and lamp wiring diagrams (page 104) with every name, changing only wire colours;
- what the owner lists as the LE's playfield changes leaves every device where it was: the Arwen playfield plastic returns, the plastics have no mounting holes and carry no Armies of Middle Earth figures, the Balrog has the LED upgrade, the centre ramp has a post upgrade, and the playfield is signed and extra-clearcoated. The rest is cabinet trim: plated and polished lockdown bar, legs, hinges and side rails, brass bolts, gold trim, a gold-effect real-glass backglass and the 500 Game Limited Edition plate.

Each carried device and placement cites the LE chart (and placements the annotated pages) beside its 2003 evidence, and each device note keeps the 2003 wording, which names the 2003 documents.

## Edition differences a recreation needs

- **Right Helm's Deep flasher on 28.** Bind it to public solenoid 28. The LE chart prints #28 FLASH: HELMS DEEP RT on Q28, control line BLU-BLK at J6-P4, power YEL-ORG at J6-P10, 20v DC; the 2003 machine has it on 14.
- **Solenoid 14 is unconnected.** The chart prints #14 NOT USED NC J9-P7. 10.02 still drives 14 as an exact mirror of 28, so the state published at 14 is the flasher's, with no load behind it on this edition. Do not bind a second flasher there.
- **Solenoid 12 is the optional shaker motor.** The LE harness brings the BLU-YEL drive line from Q12 (J9-P5) to a single-wire connector at the back of the cabinet, and a RED/WHT supply connector near the plumb-bob tilt, for Stern's Rev B shaker kit, which brings its own motor and shaker board and mounts on the cabinet floor. No shaker is fitted from the factory; 10.02 never drove 12 in the gameplay runs at default settings.
- **Optional coil 24** is unchanged; the LE chart names it OPTIONAL COIL (KNOCKER), and the owner fitted a hardware knocker there through adjustment #46 Q24 option.
- **The Balrog flasher (32) is a red LED module.** Service bulletin 148 replaced the initial run's #89 bulb with LED module 112-5023-02 (12.8v, 20-25mA) in socket 077-5003-00-80 from April 2004; the owner lists "Balrog has LED upgrade" for the LE, though the chart still prints #89 Bulb. It is dimmer than the bulb and still driven on 32.
- **Boards.** The LE runs a Stern 520-5249-00 S.A.M. I/O power driver board in place of the 2003 machine's 520-5137-01, fed through a "Z" connector that adapts the old J10 harness plug to the new board; the owner's page 101 relabels the board-side J10 pins 10,9 / 8 / 7,6 where the 2003 page prints 1,2 / 3 / 4,5, while the chart keeps the harness-side J10-P1/2, P3 and P4/5. Fuse and bridge numbers changed with the board, as the owner's page lists; his page 101 relabels the 2003 page's fuses F6 (7A, the 48v AC feed of the 50v bridge) as F5, F20 (the ring magnet's) as F7 4A with "*May need 5A S.B.", F21 (3A) as F8, F7 (the 20v bridge's feed) as F10 and F22 (the controlled-lamp bridge's feed) as F9, and BRIDGE 20 as BRIDGE 4. The owner's page gives the CPU/Sound board as a 520-5300-B4 White Star CPU/Sound Board II with an Atmel processor, his 2010 post as a 520-5300-00 Rev A.

## Wire colours

The structured wiring follows the LE chart, the edition's own wiring table, as `docs/INSTRUCTIONS.md` directs when sources disagree only on wiring detail. Against the 2003 manual the chart changes:

- coil power lines: 50v YEL-VIO -> BRN-BLU (#1-5, #7, #9-11), the loop diverter's GRY-YEL~3A Fuse~YEL-VIO -> GRY-YEL~3A Fuse~BRN-BLU, the flippers' ~RED-YEL -> ~YEL-BLK (rows renamed "(50v YEL/BLK)"), 20v BRN -> YEL-BLU (#13, #17-22) and flasher ORG -> YEL-ORG;
- coil control lines: #2 BRN-RED -> RED-BRN, #5 BRN-GRN -> GRY-BLK, #9 BLU-BRN -> GRY-YEL, #16 ORG-VIO -> BRN-ORG;
{_lamp_changes}

The switch matrix and dedicated switches keep the 2003 colours on the chart. The owner's annotated pages read some wires differently from his own chart: switch column drives 1, 2, 3 and 7 as PINK-GRY, GRN-BLK, GRN and BRN-WHT and row returns 3, 4 and 8 as VIO, PINK-VIO and GRN-WHT (page 104); #5's control line as ORG-YEL (page 100, while page 101 agrees with the chart's GRY-BLK); #25 and #26 as BLK and BLK-YEL (page 101); the flipper fuse feeds as ~BRN-BLU from J10-P4/5 (pages 100 and 106; the right one also ORG-BRN before the fuse), with page 101 drawing the board-side 50v buses as BRN-BLU on J10 pins 10,9 and YEL-BLK on pins 7,6; the G.I. wires of circuits 2-4, where YEL, GRN and VIO become WHT-BLK, YEL-GRY and GRY-YEL and circuit 3's WHT-GRN becomes YEL-GRN (page 103); and the bridge feeds from the transformer as VIO-GRY and VIO-WHT. Each affected device's note gives the other reading. None of it changes which device sits on which address.

## Firmware

`lotr_le` is the edition's production firmware, 10.02. Beyond the flasher mirror it behaves like 10.00 in the retained runs: the same trough serve, and the same coils and flashers answering the same switches; the shaker on 12 stays off at default settings. The shaker code and its adjustment were not exercised.

{_base_section("The 520-5242-00 LED board: nineteen separately addressable emitters")}

{_base_section("Addresses that are synthetic, mirrored or reserved")}
- On this edition, public 14 is the 10.02 firmware's mirror of the right Helm's Deep flasher on 28, with nothing connected; 12 is the optional shaker motor.

{_base_section("Opto polarity: PinMAME normalizes nothing here")}

{_base_section("Custom mechanisms")}
- **On the Limited Edition** the One Ring magnet's own fuse is numbered F7 on the 520-5249-00 board, 4A, which the LE owner's annotated page 101 says "*May need 5A S.B."; F20 is the 2003 board's number.

{_base_section("How coordinates were resolved")}

{_base_section("General illumination")}

{_base_section("Recreation guidance")} On the Limited Edition, bind the right Helm's Deep flasher at 28, leave 14 unbound, and treat 12 as an optional cabinet shaker.
"""


def _spatial_report() -> dict:
	report = copy.deepcopy(base.spatial_report)
	report["machine_id"] = MACHINE_ID
	report["status"] = definition["coverage"]["status"]
	report["edition_derivation"] = {
		"from_machine": "stern.lord-of-the-rings.2003",
		"basis": "The Limited Edition's own cabinet chart prints the 2003 machine's switch matrix, lamp matrix and coil set cell for cell and the same switch, coil and lamp location maps; the owner's annotated manual pages keep the 2003 under-playfield drawing; the edition's listed playfield changes are plastics, figures, the Balrog LED module, a ramp post and finish. Every placement below is the 2003 machine's, validated there, and cites the LE chart and annotated pages beside its 2003 evidence.",
		"moved": [{"device": HELMS_DEEP_RIGHT, "placement": f"{HELMS_DEEP_RIGHT}.emitter", "from_public_solenoid": 14, "to_public_solenoid": 28}],
		"added_without_placement": [{"device": SHAKER, "public_solenoid": 12, "reason": "cabinet_or_service"}, {"device": UNUSED_14, "public_solenoid": 14, "reason": "unused"}],
		"sources": [CHART_SOURCE, PAGES],
	}
	report["promotion_decision"] = (
		"Promoted to author_ready: every placement is the 2003 machine's validated placement, carried because the edition's own chart and annotated pages print the same tables and playfield; "
		"every device assertion and the driver's physical compatibility are validated; and the edition's moved, unconnected and added drivers (28, 14, 12) are settled by its chart, its owner's documents and its firmware."
	)
	return report


spatial_report = _spatial_report()


def build() -> dict:
	"""Return the canonical definition derived from the 2003 machine and this edition's evidence."""
	return definition


def _definition_bytes() -> bytes:
	with tempfile.TemporaryDirectory() as scratch:
		probe = Path(scratch) / "definition.json"
		write_json(probe, definition)
		return probe.read_bytes()


def _artifacts() -> tuple[tuple[Path, bytes], ...]:
	report_bytes = (json.dumps(spatial_report, indent="\t", sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
	definition_bytes = _definition_bytes()
	return (
		(DEFINITION_PATH, definition_bytes),
		(SEED_PATH, definition_bytes),
		(SPATIAL_REPORT_PATH, report_bytes),
		(KNOWLEDGE_PATH, knowledge_note.encode("utf-8")),
		*((path, content.encode("utf-8")) for path, content in sorted(EXCERPT_CONTENTS.items())),
	)


def _write(root: Path) -> None:
	for path, payload in _artifacts():
		target = root / path.relative_to(ROOT)
		target.parent.mkdir(parents=True, exist_ok=True)
		with target.open("wb") as stream:
			stream.write(payload)
	# Promotion moves the record: the earlier identity-only partial is retired.
	partial = root / PARTIAL_PATH.relative_to(ROOT)
	if partial.is_file():
		partial.unlink()


def _check(root: Path) -> None:
	if (root / PARTIAL_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"the retired partial record still exists: {PARTIAL_PATH.relative_to(ROOT)}")
	for path, expected in _artifacts():
		target = root / path.relative_to(ROOT)
		if not target.is_file():
			raise RuntimeError(f"Lord of the Rings Limited Edition artifact is missing: {target}")
		if base._comparable(target.read_bytes()) != base._comparable(expected):
			raise RuntimeError(f"Lord of the Rings Limited Edition artifact does not match the deterministic curator: {target}")
	print("Lord of the Rings Limited Edition definition, seed, spatial audit, knowledge note and excerpts match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and the canonical artifacts.")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, its seed, report, note and excerpts.")
	parser.add_argument("--repository-root", type=Path, default=ROOT, help="Repository root to operate on.")
	args = parser.parse_args()
	root = args.repository_root.resolve()
	if args.regenerate:
		_write(root)
		print(f"Wrote {DEFINITION_PATH.relative_to(ROOT)} and its seed, report, note and excerpts")
		return
	_check(root)


if __name__ == "__main__":
	main()
