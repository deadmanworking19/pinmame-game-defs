"""Deterministic, deliberately partial Blackout (Williams, 1980) curation.

Authority: the instruction booklet and the instruction manual and drawing set for physical
construction and wiring; the pinned PinMAME source for transport; the retained blkou_l1 harness runs
for observed ROM behavior; the two pinned corpus scripts for runtime bindings. Placements come from
one retained community table and stay `observed`; no lamp is placed because no public lamp in that
table sits on a bulb.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_external_evidence_manifest import check_manifest, write_manifest  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
import blackout_runtime_evidence as runtime_evidence  # noqa: E402
import blackout_spatial as spatial  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.blackout.1980"
GAME = "blkou_l1"
BASE = "2506047a1f986894b6b9fe8982fbe8ef8676b473"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
LIBRARY_SHA = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_SHA = "88d335971251be6aa26901e51bc47bae6febaaaf0917ed1b8aac4a2fdd306dc1"
ROM_MEMBERS = {
	"gamerom.716": (2048, "46a2afcfc2d969c5acae18b57a678265257a6102"),
	"green1.716": (2048, "ddf63208559a3a08d4e88327c55426b0eed27654"),
	"green2.716": (2048, "1959184764643d58f1740c54bb74c2aad7d667d2"),
	"sound2.716": (2048, "cc77af54fdb192f0b334d9d1028210618c3f1d95"),
	"v_ic5.532": (4096, "879127a88b3640bbb202c64cbf8678869c964177"),
	"v_ic6.532": (4096, "c073cb4bdea189085ae074e9c16872752b6ffba0"),
	"v_ic7.532": (4096, "d03c71efc0431f30a07c8194c0614c96fb683710"),
}
NVRAM_SHA = "f99409fbe04cff06460649a5b9a5befe6824aa9423f9d6578fa19410a012c9f1"
HARNESS = runtime_evidence.HARNESS
HARNESS_MANIFEST_SHA = "e5518329cebb092f177c4cac4096c15832f0b0828d1a163facc50dc88e85487f"
OPDB_SHA = "690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93"
DEFINITION = Path("machines/partial/williams/blackout-1980.json")
SEED = Path("tools/seeds/williams/blackout-1980.json")
KNOWLEDGE = Path("knowledge/williams/blackout-1980.md")
REPORT = Path("reports/spatial/williams/blackout-1980.json")
REPORT_MD = REPORT.with_suffix(".md")
RUNTIME = runtime_evidence.OUTPUT
RUNTIME_SHA = "8f8844c88cac5d81619864b882ff930a3499b1856774e92c43670e4783497d5b"
READINGS = runtime_evidence.READINGS
READINGS_SHA = "092835d55fd0a590eb815e5c86582586c7eeb06ded3d49c38fdb0d82ee1b209f"
MANUAL_DIRECTORY = Path("by-machine") / MACHINE_ID
WAYBACK = "https://web.archive.org/web/{stamp}id_/https://www.ipdb.org/files/317/{name}"
# Generation times: the committer dates of the pinned PinMAME and script-corpus revisions, the creation time of the
# retained table's extracted-vpxtool/script.vbs, and the persistence time of the last raw harness trace (play.json).
REVISION_COMMITTED = "2026-10-25T20:16:49Z"
SCRIPT_REVISION_COMMITTED = "2026-07-07T06:37:05Z"
EXTRACTED = "2026-10-31T10:25:25Z"
RUN_PERSISTED = "2026-10-31T10:50:36Z"
OPDB_ACQUIRED = "2026-08-14T17:53:43Z"
MANUAL_RIGHTS = "NOASSERTION; retained for local research; original copyright retained; full document not redistributed"
MANUAL_ATTRIBUTION = "Williams Electronics, Inc.; hosted by the Internet Pinball Database, retrieved from the Internet Archive's Wayback Machine"
BOARD = "Williams System 6 driver board"

MANUAL = "manual.blackout-booklet"
DRAWINGS = "manual.blackout-drawing-set"
IPDB = "ipdb.blackout"
OPDB = "opdb.blackout"
SOURCE = "pinmame.blackout"
CORE = "pinmame.system-6-current"
SCRIPT = "vpx.blackout-sbr34-1-0-1"
MOD_SCRIPT = "vpx.blackout-mod-s34-1-1"
TABLE = spatial.TABLE
EMBEDDED = spatial.EMBEDDED
RUN = "runtime.blackout"

# (filename, SHA-256, bytes, PDF pages, Wayback capture, revision, document type, acquisition time)
DOCUMENTS = {
	MANUAL: ("Williams_1980_Blackout_Operators_Handbook.pdf", "d3d437d7f85e4b91b7eccc96b1aace3580d214517156d9eca910e270aeb9128d", 1105735, 12,
		"20180814111143", "16P-495-103", "instruction booklet", "2026-10-31T10:14:35Z"),
	DRAWINGS: ("Williams_1980_Blackout_Manual_with_paginated_schematics.pdf", "6872d8897436feb4cc5cd5d82634c5223d3d53287e4d3f85b235f5a6fc3f2dbf", 31087603, 23,
		"20180814111822", "16P-495-101", "instruction manual and drawing set", "2026-10-31T10:14:49Z"),
}
IPDB_PAGE = ("ipdb-317.html", "e2e18c1948b5684673b49d3b360b9a8ea1fee2bad33f9997dd61482f53e2399f", 29948)
IPDB_ACQUIRED = "2026-10-31T10:15:24Z"
SOURCE_FILES = {
	"LICENSE": "21cde7ac6cffe0fa9e3a66beb89e0db1b78caa7bb8b8041d1b483f36460e026e",
	"src/wpc/core.c": "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00",
	"src/wpc/core.h": "b6c03b20a09fbadff1ce16f9f1cfc9e5bace08857cb998b92d8f304695ec97c0",
	"src/wpc/driver.c": "165dbb7d4f3ebf38d668e90c9283df87881048de1b531c73a23d9c4122a5667d",
	"src/wpc/s6.c": "8a409aed0d8b9eadb47f81875644fd8a4c1bec6c998afd1597cf7c427ae953f2",
	"src/wpc/s6.h": "7b40c0264c280b7a8b6dec081e01e498c9afdf39ca234e5d30cb557b062af30a",
	"src/wpc/s6games.c": "f46e6ab0b1c6ce9dd184849b9dd70d3908f7c92236e44a904fce02c526725d82",
	"src/wpc/wmssnd.c": "5d9d431416150e22fddf850b59e377d7f923fa7bda067e830729891670eff82f",
}
SCRIPT_FILES = {
	SCRIPT: ("Blackout (Williams 1980) v1.0.1 - SBR34.vbs", "eafdb30a3009065c143e3a385141cef1c50a2a9b66ee08d93a4596dc660a5ab6"),
	MOD_SCRIPT: ("Blackout (Williams 1980) Mod - S34 v1.1.vbs", "1853655480d0e3f423dd9a8ad384ea99d47c5687daf4c704c0d7badb01f24b8b"),
}
EXCERPTS = {
	"cabinet-and-power.md": "ca050b5aa1f20eb720f7c8bd83ade8c02a0950434ed12747fd86d609ec2d04cf",
	"diagnostics.md": "703a8ab64fd46e66df72a5f577cfff5a97a0403ad3a94586c82c07e5bfbec651",
	"game-operation.md": "fc454e248557c4e4a680897afcf6025bebfd6c07213cd4aaa5db14b02019fb1f",
	"identity.md": "4be023dfa9de0ccd023440d4da75867d1ba7a32f70eb69071aeb0261dd617569",
	"insert-board.md": "fa6c93350a7bcb8cd4a142a98c7519493c7e5ec4f52c6455e598e838ecfd858f",
	"lamp-matrix.md": "72b68686ab0e59d91d673285de9c107cc01741077c164d7f978506b14f7ff04e",
	"lamp-wiring.md": "27545e84a52fd25b19d1f010ea6cc77715a92c47011f8388807bacf362646960",
	"script-bindings.md": "1d79ead0a051e9fd5594bdc70c922a425788c502cf544a48a9dc50551b424002",
	"solenoid-connections.md": "ada14bb28091e3bd0b2816968ec0fc2ac9660931cbbcf80120cb14d49b41337b",
	"sound-board.md": "8c3d2355988de81645fe300f483be7c67543345c7665978081bc443f4c0e1c9e",
	"spatial-method.md": spatial.EXCERPT_SHA,
	"switch-matrix.md": "0e33a7816b6b31a5d8e569d674d5b37ac8009f7f0363e467bdba7ed7f798a3f5",
}
LOCATORS = {
	"cabinet-and-power.md": "Drawing set PDF page 20 / printed 23 Power Wiring Diagram (special relay 6L15 and the 6.3 VAC G.I. outputs), PDF page 21 left half / printed 24 Cabinet Wiring Diagram, PDF page 3 / printed 4-5 Inspection; booklet Table 3 row 15; IPDB 317 notes",
	"diagnostics.md": "Booklet PDF pages 3, 4 and 7 / printed 3, 4 and 7: Bookkeeping and Evaluation Totals, Game Adjustment Procedure, Diagnostic Procedures, Table 1 Game Adjustments, Resetting Audit Totals and Auto-Cycle, Figures 1 and 2",
	"game-operation.md": "Booklet PDF pages 1-2 / printed 1-2, board requirements and Game Operation; drawing set PDF page 2 / printed 2-3 Foreword and PDF page 4 / printed 6 Power Turn-On, Electrical Adjustments and Special Maintenance Information",
	"identity.md": "IPDB 317 capture fields, OPDB snapshot entries GRwYo and GRwYo-MQoPw, the pinned s6games.c blkou block, s6.c s6_6digit_disp, driver.c comments and the two documents' covers",
	"insert-board.md": "Drawing set PDF page 23 / printed 28, Insert Board Wiring Diagram: every 9J1 pin, the lamps and the general illumination string",
	"lamp-matrix.md": "Booklet PDF page 12 / printed 12, Figure 6 Lamp Matrix: all 64 cells and the column and row headers",
	"lamp-wiring.md": "Drawing set PDF page 22 right half / printed 27, Playfield Lamp Wiring Diagram: column and row wiring, the matrix drawing, the bulb list and general illumination",
	"script-bindings.md": "Embedded S34 v1.1 script lines 6-403, Mod - S34 v1.1 lines 43-76 and v1.0.1 - SBR34 lines 9-3640: solenoid callbacks, switch handlers, ball stacks, drop banks, the special-relay G.I. handlers and lamp bindings",
	"solenoid-connections.md": "Booklet PDF page 9 / printed 9 Table 3 (every row, column and note) and PDF page 8 / printed 8 Figure 3 chart and locations; drawing set PDF page 21 right half / printed 25 Playfield Solenoid Wiring Diagram and left half / printed 24 cabinet coils",
	"sound-board.md": "Drawing set PDF page 13 / printed 15/16 Sound Board Logic Diagram 16D-8224: DS1, R2/C2, R4/C4, the SR1 pull-ups, jumpers W4/W9 and IC10 PB5/PB6; the Electrical Adjustments; s6.h S6_COMPORTS and wmssnd.c s67s_cmd_w",
	"spatial-method.md": "Retained table identity and extraction, every object and point method, the unplaced devices, the general-illumination bulbs and the not-applicable devices",
	"switch-matrix.md": "Booklet PDF page 11 / printed 11 Figure 5 Switch Matrix (all 64 cells and headers) and PDF page 10 / printed 10 Figure 4 switch chart and locations; drawing set PDF page 22 left half / printed 26 Playfield Switch Wiring Diagram and PDF page 21 / printed 24 cabinet switches",
}
UNREVIEWED = {"identity.md", "script-bindings.md", "spatial-method.md"}
# Rendered crops of drawings: excerpt -> (image file, image SHA-256, image_derivation printed by tools/render_excerpt_image.py).
IMAGES = {"sound-board.md": ("sound-board-ds1.webp", "341c4bbb875602dde20c97e37fbb50e9acdde9b0ae83c3ce47f43a9765cad3c7", "Williams_1980_Blackout_Manual_with_paginated_schematics.pdf page 13, crop box 0.165,0.27,0.505,0.705, scanned page rendered at its native resolution (embedded image xref 83, 3216px across 16.75in), rendered at 192 dpi, grayscale, 1095x897 WebP quality 80")}

SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "Ball Roll Tilt", 3: "Credit Button", 4: "Right Coin Switch", 5: "Center Coin Switch", 6: "Left Coin Switch", 7: "Slam Switch", 8: "High Score Reset",
	9: "Outhole", 10: "Left Outside Rollover", 11: "Green Target #1 (Bottom)", 12: "Green Target #2", 13: "Green Target #3", 14: "Green Target #4", 15: "Green Target #5 (Top)",
	18: "Left Spinner", 19: "Left Spinner Standup", 20: "Upper Left Target", 21: "Right Jet Bumper", 22: "Left Jet Bumper", 23: "Bottom Jet Bumper",
	25: "Center 3 Bank (Left)", 26: "Center 3 Bank (Center)", 27: "Center 3 Bank (Right)", 28: "Center 3 Bank Series", 29: "1 Rollover", 30: "2 Rollover", 31: "3 Rollover", 32: "Playfield Tilt",
	33: "Top 3 Bank (Left)", 34: "Top 3 Bank (Center)", 35: "Top 3 Bank (Right)", 36: "Top 3 Bank Series", 37: "Upper Right Spinner", 38: "Middle Right Standup", 39: "Middle Right Spinner", 40: "Eject Hole",
	41: "Right Outside Rollover", 42: "Right Inside Rollover", 43: "Right Kicker", 44: "Left Kicker", 45: "Left Inside Rollover", 46: "Right Flipper Lane Change Switch",
}
UNUSED_SWITCHES = {16, 17, 24, *range(47, 65)}
LAMP_LABELS = [
	"Same Player Shoots Again (Playfield)", "1,000 Bonus", "2,000 Bonus", "3,000 Bonus", "4,000 Bonus", "5,000 Bonus", "6,000 Bonus", "7,000 Bonus",
	"8,000 Bonus", "9,000 Bonus", None, "10,000 Bonus", "2X Bonus Multiplier", "3X Bonus Multiplier", "4X Bonus Multiplier", "5X Bonus Multiplier",
	"Green Target #1 Arrow (Bottom)", "Green Target #2 Arrow", "Green Target #3 Arrow", "Green Target #4 Arrow", "Green Target #5 Arrow (Top)",
	"Center 3 Bank Arrow (Left)", "Center 3 Bank Arrow (Center)", "Center 3 Bank Arrow (Right)",
	"Right Jet Bumper", "Left Jet Bumper", "Bottom Jet Bumper", "\"1\" Rollover", "\"2\" Rollover", "\"3\" Rollover", "Left Inside Rollover", "Right Inside Rollover",
	"Loop 5,000", "Loop 10,000", "Loop 15,000", "Loop 20,000", "Extra Ball When Lit", "Top 3 Bank Arrow (Left)", "Top 3 Bank Arrow (Center)", "Top 3 Bank Arrow (Right)",
	"Top Right Spinner", "Middle Right Spinner", "Eject Hole Green 5,000", "Eject Hole Yellow 5,000", "Eject Hole Red 5,000", "Eject Hole BLACKOUT", "Left Special", "Right Special",
	"20,000 Bonus", "1 Can Play", "2 Can Play", "3 Can Play", "4 Can Play", "Match", "Ball in Play", "Credits (Playfield)",
	"#1 Player Up", "#2 Player Up", "#3 Player Up", "#4 Player Up", "Tilt", "Game Over", "Same Player Shoots Again (Backbox)", "High Score to Date",
]
BACKBOX_LAMPS = {*range(50, 56), *range(57, 65)}
# Insert board names as printed on the drawing set's sheet, and the bulbs it draws.
INSERT_BOARD = {50: ("1 CAN PLAY", 1), 51: ("2 CAN PLAY", 1), 52: ("3 CAN PLAY", 1), 53: ("4 CAN PLAY", 1), 54: ("MATCH", 1), 55: ("BALL IN PLAY", 1),
	57: ("PLAYER 1 UP", 1), 58: ("PLAYER 2 UP", 1), 59: ("PLAYER 3 UP", 1), 60: ("PLAYER 4 UP", 1), 61: ("TILT", 1), 62: ("GAME OVER", 2),
	63: ("SAME PLAYER SHOOTS", 2), 64: ("HIGH SCORE", 2)}
# Table 3 values as printed: label, kind, wire, connections, driver transistor, part number, load drawn on the wiring sheets.
SOLENOIDS = {
	1: ("Ball Release", "coil", "GRY-BRN", "2P11-4, 8P3-17", "Q15", "SA-23-850-DC", "8L1 BALL RELEASE, diode 8D129"),
	4: ("Center 3-Bank Reset", "coil", "GRY-YEL", "2P11-8, 8P3-20", "Q21", "SA3-23-850-DC", "8L4 CENTER 3-BANK RESET, diode 8D132"),
	5: ("Top 3-Bank Reset", "coil", "GRY-GRN", "2P11-9, 8P3-21", "Q23", "SA3-23-850-DC", "8L5 TOP 3-BANK RESET, diode 8D133"),
	6: ("Eject Hole", "coil", "GRY-BLU", "2P11-3, 8P3-22", "Q25", "SG-23-850-DC", "8L6 EJECT HOLE, diode 8D135"),
	9: ("Sound Line 1", "control_signal", "BRN-BLK", "2P9-9, 10P3-3", "Q31", None, None),
	10: ("Sound Line 2", "control_signal", "BRN-RED", "2P9-7, 10P3-2", "Q33", None, None),
	11: ("Sound Line 3", "control_signal", "BRN-ORN", "2P9-1, 10P3-5", "Q35", None, None),
	12: ("Sound Line 4", "control_signal", "BRN-YEL", "2P9-2, 10P3-4", "Q37", None, None),
	13: ("Sound Line 5", "control_signal", "BRN-GRN", "2P9-3, 10P3-7", "Q39", None, None),
	14: ("Credit Knocker", "coil", "BRN-BLU", "2P9-4, 7P1-16", "Q41", "SA2-23-850-DC", "7L14 CREDIT KNOCKER, diode 7D9"),
	15: ("Special Relay", "relay", "BRN-VIO", "2P9-5, 6P2", "Q43", "5A-9384", "6L15 SPECIAL RELAY, diode drawn across the coil"),
	16: ("Coin Lockout", "coil", "BRN-GRY", "2P9-6, 7P1-18, 7P2-4", "Q45", "SM-35-4000-DC", "7L16 COIN LOCKOUT, diode 7D10"),
	17: ("Left Jet Bumper", "coil", "BLU-BRN", "2P12-7, 8P3-11", "Q2", "SG-23-850-DC", "8L17 LEFT JET BUMPER, diode 8D137"),
	18: ("Right Jet Bumper", "coil", "BLU-RED", "2P12-4, 8P3-12", "Q4", "SG-23-850-DC", "8L18 RIGHT JET BUMPER, diode 8D138"),
	19: ("Bottom Jet Bumper", "coil", "BLU-ORN", "2P12-3, 8P3-13", "Q6", "SG-23-850-DC", "8L19 BOTTOM JET BUMPER, diode 8D139"),
	20: ("Left Kicker", "coil", "BLU-YEL", "2P12-6, 8P3-14", "Q8", "SG-23-850-DC", "8L20 LEFT KICKER, diode 8D140"),
	21: ("Right Kicker", "coil", "BLU-GRN", "2P12-8, 8P3-15", "Q10", "SG-23-850-DC", "8L21 RIGHT KICKER, diode 8D143"),
}
# Table 3 rows printed Not Used: wire, connections, driver transistor.
UNUSED_SOLENOIDS = {2: ("GRY-RED", "2P11-5, 8P3-18", "Q17"), 3: ("GRY-ORN", "2P11-7, 8P3-19", "Q19"), 7: ("GRY-VIO", "2P11-2, 8P3-23", "Q27"),
	8: ("GRY-BLK", "2P11-1, 8P3-24", "Q29"), 22: ("BLU-BLK", "2P12-9, 8P3-16", "Q12")}
# Public special slot -> scoring matrix switch (INITGAMEFULL ss17-ss21) and Table 3 note 1's special switch wiring.
SPECIAL_SWITCHES = {17: 22, 18: 21, 19: 23, 20: 44, 21: 43}
SPECIAL_WIRING = {17: ("ORN-BRN", "2P13-5, 8P3-5", "8SW65"), 18: ("ORN-RED", "2P13-3, 8P3-6", "8SW66"), 19: ("ORN-BLK", "2P13-2, 8P3-7", "8SW67"),
	20: ("ORN-YEL", "2P13-4, 8P3-8", "8SW68"), 21: ("ORN-GRN", "2P13-8, 8P3-9", "8SW69")}
MISSING = ["spatial_placement"]
POLARITY = ("Normally open: the playfield switch sheet draws every matrix switch as an open contact in series with its diode, the cabinet sheet draws 7SW1-7SW8 the same way, "
	"s6.c returns the switch rows through core_getSwCol without inversion and blkou_l1 declares no inversion mask, and the Test 03 run shows each held public 1 as a closure.")


def sha(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(label: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def provenance(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def base(identifier: str, label: str, kind: str, group: str, address: int, *refs: str, availability: str = "used") -> dict[str, Any]:
	namespace = group.replace(".input", "").replace(".output", "")
	values = [str(address)]
	if group == "pinmame.input.switch" and address > 0:
		values = list(dict.fromkeys([str(address), f"{address:02d}", f"{address:03d}"]))
	return {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address}, "availability": availability,
		"aliases": [{"namespace": namespace, "value": value} for value in values], "provenance": provenance(*refs)}


def switch_id(address: int) -> str:
	return f"switch.{slug(SWITCH_LABELS[address])}" if address in SWITCH_LABELS else f"switch.unused-{address}"


def lamp_id(address: int) -> str:
	label = LAMP_LABELS[address - 1]
	return f"lamp.{slug(label)}" if label else f"lamp.not-used-{address}"


def solenoid_id(address: int) -> str:
	if address == 23:
		return "relay.game-on-flipper-enable"
	if address in SOLENOIDS:
		label, kind, *_ = SOLENOIDS[address]
		return f"{ {'coil': 'coil', 'relay': 'relay', 'control_signal': 'signal'}[kind] }.{slug(label)}".replace(" ", "")
	if 45 <= address <= 48:
		return f"virtual.{'right' if address <= 46 else 'left'}-flipper-{'power' if address % 2 else 'hold'}-synthetic"
	return f"solenoid.not-used-{address}"


def matrix_wiring(address: int, lamp: bool = False) -> dict[str, str]:
	"""Column and row wiring printed on the booklet's Figure 5 / Figure 6 headers and the drawing set's wiring sheets."""
	col, row = divmod(address - 1, 8)
	if lamp:
		cw = ["BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY"]
		cp = ["2J5-8", "2J5-9", "2J5-6", "2J5-7", "2J5-3", "2J5-5", "2J5-1", "9J1-7 (insert board; this game's sheets print no 2J5 pin for column 8)"]
		rw = ["BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY"]
		rp = [1, 2, 3, 4, 5, 6, 9, 8]
		rc, dp, rpfx = "2J7", "YEL", "RED"
	else:
		cw = ["BRN", "RED", "ORN", "YEL", "BLK", "BLU", "VIO", "GRY"]
		cp = [f"2J2-{p}" for p in (9, 8, 7, 6, 5, 3, 2, 1)]
		rw = ["BRN", "RED", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY"]
		rp = [9, 8, 7, 6, 5, 4, 3, 1]
		rc, dp, rpfx = "2J3", "GRN", "WHT"
	return {"board": BOARD, "drive_wire": f"{dp}-{cw[col]}", "drive_connection": cp[col], "return_wire": f"{rpfx}-{rw[row]}", "return_connection": f"{rc}-{rp[row]}"}


SWITCH_NOTES = {
	1: "Cabinet sheet 7SW1 PLUMB BOB TILT, diode 7D1. The third closure tilts the ball in play (booklet Tilts paragraph; Function 29 sets 1-9, factory 03).",
	2: "Cabinet sheet 7SW2 BALL ROLL TILT, diode 7D2. The first closure tilts the ball in play; the gameplay run drops game-on 23 0.03 s after the closure and lights TILT 61.",
	3: "Cabinet sheet 7SW3 CREDIT BUTTON, diode 7D3. Starts a game; in Game Adjustment it raises (Auto-Up) or lowers (Manual-Down) the value shown.",
	4: "Cabinet sheet 7SW4 RIGHT COIN CHUTE, diode 7D4, on the coin door. The gameplay run's coin fires the credit knocker 14 and lights the playfield credits lamp 56.",
	5: "Cabinet sheet 7SW5 CENTER COIN CHUTE, diode 7D5, on the coin door.",
	6: "Cabinet sheet 7SW6 LEFT COIN CHUTE, diode 7D6, on the coin door. Table 1 Function 01 counts the left chute, 'closest to coin door hinge'.",
	7: "Cabinet sheet 7SW7 SLAM TILT, diode 7D7, on the coin door. Returns the game to Game Over (booklet Tilts paragraph).",
	8: "Cabinet sheet 7SW8 HIGH SCORE RESET, diode 7D8, on the coin door (booklet Figure 1). Pressing it sets the current high score to date to Function 13.",
	9: "Ball-presence contact: closed while a drained ball rests in the outhole. In the gameplay run a closure fires the 3-bank resets 4 and 5 and then ball release 1 1.06 s later.",
	10: "Scores 2,000 (switch chart). Figure 4 draws it in the left outlane.",
	11: "Bottom one of the five green standup targets, 2,000 or 5,000 when lit. Making all five scores 10,000 and lights eject-hole green lamp 43 (booklet Green Targets paragraph; the gameplay run lit 43 on the fifth).",
	15: ("Top green standup target. Figure 5 prints this cell `5 BANK #5 (TOP)`; the switch chart and the wiring sheet's list call it a green target, which the record follows. "
		"The wiring sheet draws 8SW15 in lighter print."),
	18: "Scores 100. With the upper right spinner 37 it makes the spinner loop that collects and advances the left spinner lamps 33-36 (booklet Spinner Loop paragraph).",
	19: "Scores 50. The retained table and both corpus scripts model it as a rubber hit contact; no assembly drawing was read.",
	20: "Scores 1,000 and advances the bonus; with the center 3-bank it controls the jet bumper lamps (booklet).",
	21: "Scoring contact of the right jet bumper; PinMAME also uses it as the special-switch slot for solenoid 18. The factory's direct-drive special contact is 8SW66 on the special-switch harness, which is not a public input.",
	22: "Scoring contact of the left jet bumper; special-switch slot for solenoid 17 (factory special contact 8SW65).",
	23: "Scoring contact of the bottom jet bumper; special-switch slot for solenoid 19 (factory special contact 8SW67).",
	25: "Closed while the target is down. Center 3-bank reset 4 raises the bank.",
	26: "Closed while the target is down. Center 3-bank reset 4 raises the bank.",
	27: "Closed while the target is down. Center 3-bank reset 4 raises the bank.",
	28: ("The bank's series switch, one matrix contact 8SW28 with its own diode. The ROM treats the bank as made when it closes: in the gameplay run the reset 4 fired at the closure "
		"and not while the three targets were down with 28 open. The embedded script sets 28 while 25-27 are all down. Making the bank lights eject-hole red lamp 45."),
	29: "Top rollover \"1\", 1,000 and a bonus advance; lights lamp 28. Spotting \"1-2-3\" advances the bonus multiplier, and the right flipper rotates the lit lamps (Lane Change).",
	30: "Top rollover \"2\", 1,000; lights lamp 29.",
	31: "Top rollover \"3\", 1,000; lights lamp 30.",
	32: "Playfield tilt contact; the first closure tilts (booklet Tilts paragraph). Figure 4 prints 32 near the base of the right flipper.",
	33: "Closed while the target is down. Top 3-bank reset 5 raises the bank; the top 3-bank targets advance the bonus.",
	34: "Closed while the target is down. Top 3-bank reset 5 raises the bank.",
	35: "Closed while the target is down. Top 3-bank reset 5 raises the bank.",
	36: ("The top bank's series switch 8SW36. In the gameplay run the reset 5 fired 0.015 s after it closed, and making the bank lit eject-hole yellow lamp 44 and BLACKOUT 46. "
		"The embedded script sets 36 while 33-35 are all down."),
	37: "Scores 100, or 1,000 when lit (lamp 41).",
	38: "Scores 50. The retained table and both corpus scripts model it as a rubber hit contact; no assembly drawing was read.",
	39: ("Scores 100, or 1,000 when lit (lamp 42). The wiring sheet's matrix drawing leaves the column 5, row 7 position empty (no 8SW39), while its own switch list, Figure 5, "
		"the chart, the Test 03 run and both scripts carry 39; the omission is a drafting gap, not a missing switch."),
	40: ("Ball-presence contact of the eject hole: closed while a ball rests in it. Solenoid 6 kicks it out; with BLACKOUT lit, entering it runs the special-relay sequence first "
		"(see the knowledge note)."),
	41: "Scores 2,000; the right outlane.",
	42: "Scores 1,000, or 3,000 when lit (lamp 32).",
	43: "Scoring contact of the right kicker (slingshot), 10; special-switch slot for solenoid 21 (factory special contact 8SW69, drawn as two contacts in parallel).",
	44: "Scoring contact of the left kicker (slingshot), 10; special-switch slot for solenoid 20 (factory special contact 8SW68, drawn as two contacts in parallel).",
	45: "Scores 1,000, or 3,000 when lit (lamp 31).",
}
SWITCH_ROLES = {1: (["cabinet.tilt"], "cabinet", "tilt"), 2: (["cabinet.tilt"], "cabinet", "tilt"), 3: (["cabinet.start"], "cabinet", "button"),
	4: (["cabinet.coin"], "coin door", None), 5: (["cabinet.coin"], "coin door", None), 6: (["cabinet.coin"], "coin door", None),
	7: (["cabinet.slam-tilt"], "coin door", "tilt"), 8: (["service.high-score-reset"], "coin door", "button")}


def inputs() -> list[dict[str, Any]]:
	devices = []
	services = {
		-7: ("switch.advance", "Advance", "button", "coin door", ["service.advance"],
			"Cabinet sheet 7SW75 ADVANCE on the coin door, wired GRN to CPU connector 1J4-3 (7P1-5, 7P2-14). PinMAME constant S6_SWADVANCE, sampled into the display PIA's CA1. "
			"Steps the bookkeeping functions, adjustments and diagnostic tests with Auto-Up/Manual-Down; the harness pressed it to walk Tests 01-03."),
		-6: ("switch.auto-up-manual-down", "Auto-Up / Manual-Down", "other", "coin door", ["service.auto-manual"],
			"Cabinet sheet 7SW74 AUTO-UP / MANUAL-DOWN on the coin door, wired BLU to CPU connector 1J4-4 (7P1-6, 7P2-15). PinMAME constant S6_SWUPDN, sampled into the display PIA's CB1. "
			"Public 1 is Auto-Up: the retained runs enter the lamp and switch tests with 1 and the solenoid test with 0, as the booklet's procedure requires. A two-position switch has no rest "
			"state; normally_closed follows that public convention."),
		-5: ("switch.cpu-diagnostic", "CPU Diagnostic", "button", "backbox", ["service.cpu-diagnostic"],
			"The DIAGNOSTIC pushbutton beside the Master Command switches (booklet Figure 2). PinMAME constant S6_SWCPUDIAG: s6.c asserts the CPU's NMI line while it is 1."),
		-4: ("switch.sound-diagnostic", "Sound Diagnostic", "button", "backbox", ["service.sound-diagnostic"],
			"The sound board's diagnostic pushbutton: the drawing set's Special Maintenance Information says pressing it produces eight electronic sounds and then, with the Speech Module, "
			"the BLACKOUT vocabulary, repeating until the game is turned off and on. PinMAME constant S6_SWSOUNDDIAG, passed to the sound board's diagnostic input."),
		-3: ("switch.master-command-enter", "Master Command Enter", "button", "backbox", ["service.master-command-enter"],
			"The MASTER COMMAND ENTER pushbutton beside the Master Command slide switches, behind the insert door (booklet page 7 and Figure 2): pressing it enters the Master Command "
			"setting and blinks the LEDs once. PinMAME constant S6_ENTER: s6_dips_r returns the Master Command bank to the ROM only while it is held."),
	}
	for address, (identifier, label, switch_type, location, roles, notes) in services.items():
		d = base(identifier, label, "switch", "pinmame.input.switch", address, CORE, SOURCE, MANUAL, DRAWINGS)
		d["normally_closed"] = False
		d.update(roles=roles, spatial=na("cabinet_or_service", MANUAL, DRAWINGS), physical={"location": location, "switch_type": switch_type, "notes": notes})
		if address in {-7, -6}:
			d["provenance"] = provenance(CORE, SOURCE, MANUAL, DRAWINGS, RUN)
		devices.append(d)
	for address in range(1, 65):
		used = address not in UNUSED_SWITCHES
		label = SWITCH_LABELS[address] if used else f"Not Used matrix switch {address}"
		d = base(switch_id(address), label, "switch", "pinmame.input.switch", address, MANUAL, DRAWINGS, CORE, RUN, availability="used" if used else "unused")
		d["wiring"] = matrix_wiring(address)
		d["aliases"].append({"namespace": "manual.address", "value": f"{address:02d}"})
		if not used:
			d["spatial"] = na("unused", MANUAL, DRAWINGS)
			if address in {16, 17, 24}:
				d["physical"] = {"notes": (f"Figure 5 and the switch chart print {address:02d} NOT USED and the playfield switch sheet draws no 8SW{address} in its column. Test 03 still names a held "
					f"{address}, because the ROM reports every closure it reads in columns 1-6; that is the test's sweep, not a fitted switch.")}
			else:
				d["physical"] = {"notes": (f"Figure 5 prints {address} NOT USED. Columns 7 and 8 (GRN-VIO 2J2-2, GRN-GRY 2J2-1) end at playfield pins 8P1-6 and 8P1-7, both printed N/C. "
					"Test 03 leaves its previous reading (46) shown while this switch is held, which agrees.")}
		elif address == 46:
			d.update(kind="virtual", spatial=na("virtual", CORE, SOURCE))
			wiring = d.pop("wiring")
			d["provenance"] = provenance(MANUAL, DRAWINGS, SOURCE, CORE, RUN, SCRIPT)
			d["physical"] = {"notes": (
				"The factory right flipper lane-change contact is a playfield matrix switch at this address: Figure 5 prints 46 RIGHT FLIPPER LANE CHANGE SWITCH and the playfield switch sheet "
				f"draws 8SW46 in column 6 ({wiring['drive_wire']} {wiring['drive_connection']}, {wiring['return_wire']} {wiring['return_connection']}). The booklet rotates the \"1-2-3\" lamps 'by "
				"actuating right flipper', and Figure 4 draws 46 in a dashed circle; its mounting is not drawn. In PinMAME a consumer cannot drive this address: INITGAMEFULL declares "
				"FLIP_SWNO(0,46), and core_updateSw copies cabinet button 82 into 46 on every update. The Test 03 run shows holding 82 report 46; a one-shot write to 46 reached the "
				"Test 03 display once but read back 0 at its snapshot because the next update rewrote it from 82. SBR34 writes 46 from its right-flipper solenoid callback, which the "
				"same copy overwrites. A consumer drives 82.")}
		else:
			d["normally_closed"] = False
			d["physical"] = {"location": "playfield", "notes": (SWITCH_NOTES.get(address, "") + " " + POLARITY).strip()}
			if address in SWITCH_ROLES:
				roles, location, switch_type = SWITCH_ROLES[address]
				d["physical"]["location"] = location
				if switch_type:
					d["physical"]["switch_type"] = switch_type
				d.update(roles=roles, spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
			elif address == 32:
				d["physical"]["switch_type"] = "tilt"
		devices.append(d)
	for address in range(81, 89):
		used = address in {82, 84}
		side = "right" if address == 82 else "left"
		label = f"{side.title()} Flipper Button" if used else f"Unused flipper-column position {address}"
		d = base(f"switch.{side}-flipper-button" if used else f"virtual.flipper-column-{address}", label, "virtual", "pinmame.input.switch", address,
			CORE, SOURCE, *([RUN, DRAWINGS] if used else []), availability="used" if used else "unused")
		if used:
			d["roles"] = [f"flipper.lower.{side}.button"]
		d.update(spatial=na("virtual", CORE), physical={"notes": (
			(f"PinMAME's cabinet right flipper button. The physical button is cabinet switch 7SW72, wired through the driver board's relay Z1 contact (ORN-VIO 2P12-1, 7P1-7) to the right "
			"flipper coil, not into the switch matrix. PinMAME copies it into lane-change switch 46 on every update and, while game-on 23 is set, fabricates outputs 45/46 from it; the "
			"Test 03 and gameplay runs show both.") if address == 82 else
			(f"PinMAME's cabinet left flipper button. The physical button is cabinet switch 7SW73, wired through relay Z1 (ORN-GRY 2P12-2, 7P1-9) to the left flipper coil. "
			"FLIP_SWNO(0,46) names no left matrix switch, so the ROM never reads it; PinMAME only fabricates outputs 47/48 from it while game-on 23 is set, and the gameplay run's "
			"left button changed no lamp.") if used else
			"Generic flipper-column bit outside blkou_l1's FLIP_SWNO(0,46): core_updateSw copies only the right button into the matrix, so the ROM never reads this position.")})
		devices.append(d)
	# Public DIP -> (DS1 position, IC10 pin, id suffix, label, meaning of public 0, meaning of public 1, PinMAME default) from sound-board.md.
	sound = {1: (2, "PB5", "switch-2-speech", "Speech Enable", "ON, speech enabled", "OFF, speech inhibited", 0),
		2: (1, "PB6", "switch-1-sound-select", "Sound Select", "ON, musical notes", "OFF, synthesized sounds", 1)}
	for address, (position, pin, suffix, function, zero, one, default) in sound.items():
		d = base(f"dip.sound-board-ds1-{suffix}", f"Sound Board DS1 Switch {position} - {function}", "dip_switch", "pinmame.input.dip", address, CORE, SOURCE, DRAWINGS)
		d.update(spatial=na("dip_switch", CORE, DRAWINGS), physical={"location": "backbox, sound board", "switch_type": "dip", "notes": (
			f"Miniature switch {position} of DS1 on the sound board. The Sound Board Logic Diagram (16D-8224) wires DS1 position {position} to the 6821 IC10's {pin} "
			f"({'through R2 and jumper W9' if position == 2 else 'through R4'}), with a 4.7K pull-up, and the switch grounds the line when ON. PinMAME's S6_COMPORTS calls this "
			f"bit Sound Dip {address}, and wmssnd.c s67s_cmd_w copies Sound Dip 1 and 2 uninverted onto PB5 and PB6, so public 0 is {zero} and public 1 is {one}; PinMAME's "
			f"default is {default}. The drawing set's Electrical Adjustments: "
			+ ("'Set miniature switch 2 to ON to enable speech; set it to OFF to inhibit speech.' Without the Speech Module its setting does not matter."
				if position == 2 else "'Set switch 1 to OFF to select synthesized sounds, set it to ON to select musical notes.'")
			+ " The printed switch number and PinMAME's number are crossed: public DIP 1 is switch 2 and public DIP 2 is switch 1.")})
		devices.append(d)
	for address in range(9, 17):
		position = address - 8
		d = base(f"dip.cpu-board-lower-function-bank-f{position}", f"CPU Board Function Bank F{position}", "dip_switch", "pinmame.input.dip", address, CORE, SOURCE, MANUAL, availability="unused")
		d.update(spatial=na("dip_switch", CORE, MANUAL), physical={"location": "backbox", "switch_type": "dip", "notes": (
			f"PinMAME's F{position} (bank 1 bit {position - 1}), which s6_dips_r returns only at display strobe positions 0 and 1; the source comment 's6 games only want dipcol 2' "
			"records that System 6 ROMs never read them. The booklet's Figure 2 labels the second eight-position bank NOT USED.")})
		devices.append(d)
	master = {17: ("8", "Zero Audit Totals", "'To zero audit totals (Functions 01-11) set switch 8 to ON'", "D1 Clear Audits"),
		18: ("7", "Restore Factory Settings", "'To restore factory settings and zero audit totals, set switch 7 to ON. Coin Door must remain open to restore factory settings.'", "D2 Reset Defaults"),
		19: ("6", "Auto-Cycle Mode", "'For Auto-Cycle Mode set switch 6 to ON.'", "D3 Auto-Cycle Mode")}
	for address in range(17, 25):
		position = address - 16
		if address in master:
			number, function, quote_, name = master[address]
			d = base(f"dip.master-command-switch-{number}-{slug(function)}", f"Master Command Switch {number} - {function}", "dip_switch", "pinmame.input.dip", address, CORE, SOURCE, MANUAL)
			notes = (f"PinMAME's {name} (bank 2 bit {position - 1}). The booklet (page 7): {quote_}, then momentarily press MASTER COMMAND ENTER; Figure 2 labels position {number} "
				f"{function.upper()}.")
		else:
			d = base(f"dip.master-command-bank-d{position}", f"Master Command Bank D{position}", "dip_switch", "pinmame.input.dip", address, CORE, SOURCE, MANUAL, availability="unused")
			notes = (f"PinMAME's D{position} (bank 2 bit {position - 1}). " + ("It is in the nibble the ROM samples, but the booklet assigns no function to any Master Command position other than 8, 7 and 6."
				if address == 20 else "s6_dips_r returns it only at display strobe position 3, which the source comment says System 6 ROMs do not sample. The booklet assigns it no function."))
		d.update(spatial=na("dip_switch", CORE, MANUAL), physical={"location": "backbox, behind the insert door", "switch_type": "dip", "notes": notes})
		devices.append(d)
	return devices


LAMP_NOTES = {
	1: "The playfield shoot-again insert; lamp 63 is the backbox SAME PLAYER SHOOTS insert.",
	11: "",
	23: "Figure 6 prints this cell `CENTER 3 BANK ARROW` with no qualifier; the bulb list gives `(Center)`, which the record uses.",
	24: "Figure 6 prints this cell `CENTER 3 BANK ARROW` with no qualifier; the bulb list gives `(Right)`, which the record uses.",
	31: "Figure 6 prints `LEFT INSIDE ROLLOVER (CENTER)`; the bulb list prints `Left Inside Rollover`.",
	32: "Figure 6 prints `RIGHT INSIDE ROLLOVER (RIGHT)`; the bulb list prints `Right Inside Rollover`.",
	44: "Figure 6 prints YELLOW, the bulb list Amber; the booklet's Top 3-Bank paragraph says the eject hole yellow lamp.",
	46: "Lit when the eject hole green, yellow and red lamps are lit; when lit it doubles the eject hole value (booklet BLACKOUT paragraph). Entering the eject hole with it lit runs the special-relay sequence.",
	56: ("The booklet's attract mode cycles 'all playfield lamps except for credit lamp'; the gameplay run's coin lit it and the start that used the only credit put it out. "
		"Neither corpus script nor the embedded script binds lamp 56."),
}


def outputs() -> list[dict[str, Any]]:
	devices = []
	for address in range(1, 65):
		used = address != 11
		label = LAMP_LABELS[address - 1] or "Not Used lamp 11"
		d = base(lamp_id(address), label, "lamp", "pinmame.output.lamp", address, MANUAL, DRAWINGS, CORE, RUN, availability="used" if used else "unused")
		d["wiring"] = matrix_wiring(address, True)
		d["aliases"].append({"namespace": "manual.address", "value": f"{address:02d}"})
		if not used:
			d["spatial"] = na("unused", MANUAL, DRAWINGS)
			d["physical"] = {"notes": (
				"Figure 6 and the bulb list print 11 NOT USED, and the playfield lamp sheet leaves the column 2, row 3 position blank (no 8B11 and no 8D75). PinMAME still publishes this "
				"matrix position when the ROM drives every lamp: the Lamp Test (Test 01) and the gameplay run's eject-hole sequence, which lights 1-64 one by one. Both explain the state; "
				"no bulb is fitted.")}
		elif address in BACKBOX_LAMPS:
			name, bulbs = INSERT_BOARD[address]
			column, row = divmod(address - 1, 8)
			d.update(roles=["cabinet.backglass"], spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
			d["physical"] = {"location": "backbox insert board", "quantity": bulbs, "notes": (
				f"Insert board sheet: LAMP COLUMN {column + 1} (9J1-{column}) and LAMP ROW {row + 1} (9J1-{row + 8}), drawn as "
				+ ("one bulb" if bulbs == 1 else "two bulbs in parallel") + f" through its own series diode, labelled \"{name}\"."
				+ (" Every column 8 (YEL-GRY) lamp is on this board." if column == 7 else " Column 7 rows 1 and 8 (lamps 49 and 56) are playfield lamps instead.")
				+ (" The embedded script's binding for it is commented out (`'Set Lights(54)=l54 'Match`); SBR34 reads it directly." if address == 54 else ""))}
		else:
			d["physical"] = {"location": "playfield", "quantity": 1, "notes": (
				f"The playfield lamp sheet draws this cell as one designated bulb 8B{address} with its own diode 8D{64 + address}; no cell draws more than one bulb. " + LAMP_NOTES.get(address, "")).strip()}
		devices.append(d)
	for address in [*range(1, 24), *range(45, 49)]:
		if address in SOLENOIDS:
			label, kind, wire, connection, transistor, part, load = SOLENOIDS[address]
			refs = (MANUAL, DRAWINGS, CORE, RUN)
			d = base(solenoid_id(address), label, kind, "pinmame.output.solenoid", address, *refs)
			d["aliases"].append({"namespace": "manual.address", "value": f"{address:02d}"})
			d["wiring"] = {"board": BOARD, "drive_wire": wire, "drive_connection": connection, "driver_transistor": transistor}
			notes = f"Table 3 wiring{' and part number' if part else ''} as printed; the Test 02 run pulses this public address at step {address:02d}."
			d["physical"] = {"location": "playfield"}
			if part:
				d["physical"]["part_number"] = part
			if load:
				notes += f" The wiring sheet draws {load}."
			if address == 1:
				notes += (" Kicks the drained ball from the outhole (switch 9) into the shooter lane: the gameplay run fires it 3.80 s after Start and 1.06 s after a drain, and the "
					"embedded script's one-ball trough serves the ball with it. Figure 3 prints 01 below the outhole, under the apron.")
				d["provenance"] = provenance(*refs, SCRIPT)
			if address == 4:
				notes += (" Raises the center 3-bank (25-27); Figure 3's chart calls it Center 3-Bank Drop Targets Reset and prints 04 under the bank. The gameplay run fires it at Start "
					"(3.25 s), at once on the series switch 28 and again on a drain.")
				d["provenance"] = provenance(*refs, SCRIPT)
			if address == 5:
				notes += (" Raises the top 3-bank (33-35); Figure 3 prints 05 on the bank at the upper right. The gameplay run fires it at Start (3.34 s), 0.015 s after the series "
					"switch 36 and again on a drain.")
				d["provenance"] = provenance(*refs, SCRIPT)
			if address == 6:
				notes += (" Kicks the ball out of the eject hole (switch 40); Figure 3 prints 06 at the hole on the right side. With BLACKOUT lit the gameplay run fires it 5.09 s after the "
					"entry, once the special-relay sequence is over.")
				d["provenance"] = provenance(*refs, SCRIPT)
			if kind == "control_signal":
				d.update(spatial=na("internal_nonvisual", MANUAL, DRAWINGS))
				d["physical"] = {"location": "backbox", "notes": (
					f"Printed Sound in Table 3. Driver {transistor} feeds the sound board's input at {connection.split(', ')[1]}; PinMAME passes the inverted port byte to the sound board "
					"(sndbrd_0_data_w) and publishes the same bits as solenoids 9-16, so these addresses carry sound commands, not coils. The gameplay run shows them pulsing throughout play.")}
				d["wiring"]["return_component"] = "sound board sound/speech select input"
				devices.append(d)
				continue
			if address == 14:
				d.update(roles=["cabinet.knocker"], spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
				d["physical"]["location"] = "cabinet"
				d["wiring"].update(power_wire="RED", power_connection="3J3-7, 7P1-3 (+28V)", nominal_voltage_v=28, voltage_type="dc", return_component="coil 7L14 with diode 7D9")
				notes += " The gameplay run's coin fires it once (booklet: 'Insert coin; knocker sounds')."
			if address == 15:
				d.update(roles=["cabinet.general-illumination-relay"], spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
				d["physical"]["location"] = "backbox"
				d["wiring"].update(power_wire="RED", power_connection="6J2-1 (+28V from the power supply)", nominal_voltage_v=28, voltage_type="dc",
					return_component="coil 6L15; its contact, drawn closed, is in series with transformer terminal 6T1-19 on the 6.3 VAC G.I. winding")
				notes += (" The power wiring diagram puts its coil on 6J2/6P2 (pin 1 RED +28V, pin 2 BRN-VIO from SOL. 15, pin 3 N/C) and draws its contact closed, in series with 6T1-19 on "
					"the 6.3 VAC winding. Every 6.3 VAC GENERAL ILLUMINATION output returns through that contact: YEL-WHT to 7P1-2 (coin door G.I.) and WHT-YEL to 8P2-2 (playfield) and "
					"9P1-2 and 9P1-5 (insert board). Energizing 15 opens the contact and darkens all of them; de-energized, the G.I. is on. The scripts agree: the embedded script's SolSpecial "
					"turns its GI collection off while 15 is on, and SBR34 calls 15 'inverted, enabled = OFF'. In the gameplay run 15 pulsed seven times when the ball entered the eject hole "
					"with BLACKOUT lit, the fourth pulse holding it 2.30 s. IPDB's notes call it the G.I. Relay on the backbox floor that 'cut power to all playfield lamps'; the power sheet, "
					"which the record follows, shows it switching the coin door and insert board G.I. as well. It is not a controller G.I. channel: System 6 publishes none.")
				d["provenance"] = provenance(*refs, IPDB, SCRIPT)
			if address == 16:
				d.update(roles=["cabinet.coin-lockout"], spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
				d["physical"].update(location="coin door", quantity=1)
				d["wiring"].update(power_wire="RED", power_connection="7P2-3 (+28V from 7P1-3)", nominal_voltage_v=28, voltage_type="dc", return_component="coil 7L16 with diode 7D10")
				notes += (" Energized from power-up so coins are accepted; it de-energizes, rejecting coins, until the credits fall below the maximum (booklet Credit Posting, whose last "
					"sentence misprints 'energized'). The Test 02 run pulses it from that energized rest; in the gameplay run's eject-hole sequence it dropped 0.08 s after the entry and "
					"re-energized at 4.56 s.")
			if address in SPECIAL_SWITCHES:
				wire, pins, contact = SPECIAL_WIRING[address]
				notes += (f" Special solenoid: its direct-drive special switch {contact} is wired {wire} {pins} (Table 3 note 1). In PinMAME the scoring matrix switch "
					f"{SPECIAL_SWITCHES[address]} supplies this slot while game-on 23 is set; the gameplay run fires {address} within 16 ms of a closure of {SPECIAL_SWITCHES[address]}, "
					f"and the Test 03 run holds it on while {SPECIAL_SWITCHES[address]} is held.")
				d["provenance"] = provenance(*refs, SOURCE)
			d["physical"]["notes"] = notes
		elif address in UNUSED_SOLENOIDS:
			wire, connection, transistor = UNUSED_SOLENOIDS[address]
			d = base(solenoid_id(address), f"Not Used solenoid {address}", "coil", "pinmame.output.solenoid", address, MANUAL, DRAWINGS, CORE, RUN, availability="unused")
			d["aliases"].append({"namespace": "manual.address", "value": f"{address:02d}"})
			d["wiring"] = {"board": BOARD, "drive_wire": wire, "drive_connection": connection, "driver_transistor": transistor}
			d["spatial"] = na("unused", MANUAL, DRAWINGS)
			special = (" Its special-switch input (ORN-BLU 2P13-9, 8P3-10) is printed N/C too, and INITGAMEFULL gives slot 22 no switch." if address == 22 else "")
			d["physical"] = {"notes": (
				f"Table 3 prints {address:02d} Not Used with a dash for the part, and the solenoid sheet draws driver {transistor}'s output to 8P3-{connection.split('8P3-')[1]} as N/C.{special} "
				f"The Solenoid Test pulses every driver, and the Test 02 run sees {address} pulse at step {address:02d}; the gameplay run never sets it. That sweep explains the published "
				"state; no load is fitted.")}
		elif address == 23:
			d = base(solenoid_id(address), "Game On (Flipper Relay and Special Solenoid Enable)", "relay", "pinmame.output.solenoid", address, CORE, SOURCE, DRAWINGS, RUN)
			d.update(roles=["cabinet.flipper-enable-relay"], spatial=na("internal_nonvisual", CORE, DRAWINGS), physical={"location": "backbox, driver board", "notes": (
				"PinMAME's CORE_SSFLIPENSOL: the game-on line on the standard-solenoid PIA's CB2 (s6_gameon_w). It enables the six special solenoid drivers and, on the driver board, "
				"relay Z1, whose contact grounds both flipper-button returns (2P12-1 ORN-VIO, 2P12-2 ORN-GRY). Table 3 has no row for it. The gameplay run energizes it 1.00 s after the "
				"credit button and drops it 0.03 s after the ball roll tilt closes; entering Test 02 energizes it.")})
			d["wiring"] = {"board": BOARD, "control_connection": "standard-solenoid PIA CB2 game-on line, relay Z1", "return_component": "relay Z1 contact to ground on 2P12-1/2P12-2"}
		else:
			side = "right" if address <= 46 else "left"
			winding = "power" if address % 2 else "hold"
			d = base(solenoid_id(address), f"Synthetic {side} flipper {winding} state", "virtual", "pinmame.output.solenoid", address, CORE, SOURCE, MANUAL, DRAWINGS, RUN)
			coil = ("BLU-VIO 7P1-8, 8P3-3" if side == "right" else "BLU-GRY 7P1-10, 8P3-4")
			d.update(spatial=na("virtual", CORE), physical={"notes": (
				f"Fabricated by PinMAME from button {82 if side == 'right' else 84} while game-on 23 is set, because no System 6 driver declares FLIP_SOL; the pair "
				f"{'45/46' if side == 'right' else '47/48'} asserts together and models no winding or end-of-stroke switch (the gameplay run). The physical {side} flipper is one "
				f"SFL-19-400/30-750-DC coil (Table 3: {coil}) switched by the cabinet button through relay Z1, with an end-of-stroke contact drawn across the coil; the CPU does not "
				"drive it. The playfield solenoid sheet labels the coils the other way round (8L25 RIGHT FLIPPER on BLU-GRY 8P3-4, 8L24 LEFT FLIPPER on BLU-VIO 8P3-3, and 2P12-1 LEFT); "
				"Table 3, its note 2 and the cabinet sheet's 7SW72 RIGHT FLIPPER between 7P1-7 and 7P1-8 agree with each other, so the record follows them.")})
		devices.append(d)
	return devices


def mechanisms() -> list[dict[str, Any]]:
	s, c = switch_id, solenoid_id
	refs = (MANUAL, DRAWINGS, SOURCE, CORE, RUN)
	specs = [
		("outhole-and-ball-release", "Outhole and ball release", "kicker", [c(1)], [s(9)],
			"A drained ball comes to rest in the outhole on switch 9. The ball release 1 kicks it into the shooter lane, and the player plunges by hand. Start fires 1 3.80 s after "
			"the credit button (after the 3-bank resets 4 and 5), and a drain fires 4 and 5 again and then 1 1.06 s later. No transcribed page counts the balls installed; the rules "
			"have no multiball, both scripts load one ball, and the gameplay run served one ball at a time.", refs + (SCRIPT,)),
		("center-3-bank", "Center 3-bank drop targets", "drop_target_bank", [c(4)], [s(n) for n in (25, 26, 27, 28)],
			"Three drop targets below the bottom jet bumper. Each target switch is closed while its target is down; the series switch 28 tells the ROM the bank is made, and the "
			"reset 4 raises all three. In the gameplay run 4 fired at the closure of 28 and not while the three targets were down with 28 open. Making the bank lights the eject hole "
			"red lamp 45; the center 3-bank arrow lamps rotate from the spinners.", refs + (SCRIPT,)),
		("top-3-bank", "Top 3-bank drop targets", "drop_target_bank", [c(5)], [s(n) for n in (33, 34, 35, 36)],
			"Three drop targets at the upper right. Series switch 36 and reset 5 as for the center bank (5 fired 0.015 s after 36 closed). Making the bank lights the eject hole "
			"yellow lamp 44, advances the top 3-bank arrow lamps, lights the right spinners and lights BLACKOUT 46.", refs + (SCRIPT,)),
		("eject-hole", "Eject hole", "kicker", [c(6)], [s(40)],
			"Kick-out hole on the right side. Ball-presence switch 40 is closed while a ball rests in it; kicker 6 ejects it. With BLACKOUT 46 lit (eject hole green, yellow and red "
			"lit) the hole's value doubles and the special-relay sequence runs before the ball is kicked: in the gameplay run 6 fired 5.09 s after the entry. When lit for Extra Ball "
			"(the spinner loop collecting 20,000, or the five green targets while loop 20,000 is lit) it awards the Extra Ball; the booklet gives the lit Specials to the outlanes, not the eject hole.",
			refs + (SCRIPT,)),
		("blackout-general-illumination", "Blackout: special relay and general illumination", "other", [c(15)], [s(40)],
			"The special relay 6L15 (solenoid 15) has a normally closed contact in series with the 6.3 VAC G.I. winding, so energizing 15 darkens the coin door, playfield and insert board "
			"G.I. In the gameplay run a ball entering the eject hole with BLACKOUT lit pulsed 15 seven times, the fourth pulse holding it 2.30 s; every lamp went out 0.09 s after the "
			"entry, lamps 1-64 then lit one by one during the long hold, the coin lockout 16 dropped at 0.08 s and returned at 4.56 s, and the eject kicker 6 fired at 5.09 s with "
			"lamps 43-46 out. Whether the sequence also runs without BLACKOUT lit was not observed. Relay timing beyond these readings and the visual fade belong to the table.",
			refs + (SCRIPT, MOD_SCRIPT)),
		("lane-change", "1-2-3 rollovers and Lane Change", "other", [], [s(n) for n in (29, 30, 31, 46)] + ["switch.right-flipper-button"],
			"Three top rollovers 29, 30 and 31 light the \"1\", \"2\" and \"3\" lamps 28-30; spotting all three advances the bonus multiplier. Actuating the right flipper rotates the lit "
			"lamps (LANE CHANGE): PinMAME copies the right button 82 into 46. In the gameplay run the right button moved a lit \"1\" to \"2\" and then to \"3\", and the left button changed "
			"nothing.", refs),
	]
	for address, sensor in SPECIAL_SWITCHES.items():
		label = SOLENOIDS[address][0]
		specs.append((slug(label), label, "kicker" if address >= 20 else "other", [c(address)], [s(sensor)],
			f"{label}: scoring matrix switch {sensor} and a separate direct-drive special switch {SPECIAL_WIRING[address][2]} on the same assembly fire special solenoid {address} through "
			f"the special driver while game-on 23 enables it. PinMAME derives slot {address} from {sensor}; the gameplay run fires {address} within 16 ms of a closure. Power and stroke "
			"are table-owned.", refs))
	for side, button, pair in [("right", 82, (45, 46)), ("left", 84, (47, 48))]:
		specs.append((f"{side}-flipper", f"{side.title()} flipper", "other", [c(n) for n in pair], [f"switch.{side}-flipper-button"],
			f"One {side} flipper with a dual-wound SFL-19-400/30-750-DC coil and an end-of-stroke contact across it, switched by the cabinet button through relay Z1 while game-on 23 "
			f"holds it. A consumer drives button {button}; PinMAME fabricates {pair[0]}/{pair[1]} together"
			+ (" and copies the button into lane-change switch 46." if side == "right" else ".") + " Travel, end-of-stroke behavior and tuning belong to the table.", (MANUAL, DRAWINGS, SOURCE, CORE, RUN)))
	return [{"id": f"mech.{key}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs_)}
		for key, label, kind, actuators, sensors, behavior, refs_ in specs]


def excerpt(name: str) -> dict[str, Any]:
	script = name in {"script-bindings.md", "spatial-method.md", "identity.md"}
	return {"id": f"excerpt.{slug(name.removesuffix('.md'))}", "locator": LOCATORS[name], "path": f"evidence/excerpts/{MACHINE_ID}/{name}", "sha256": EXCERPTS[name],
		"method": "manual", "transcribed_by": "curator; source text and data files read directly" if script else "curator; native page images read visually",
		"reviewed": name not in UNREVIEWED} | ({"image": f"evidence/excerpts/{MACHINE_ID}/{IMAGES[name][0]}", "image_sha256": IMAGES[name][1],
		"image_derivation": IMAGES[name][2]} if name in IMAGES else {})


def document(identifier: str, names: list[str]) -> dict[str, Any]:
	filename, digest, size, pages, stamp, revision, kind, acquired = DOCUMENTS[identifier]
	return {"id": identifier, "kind": "manual", "uri": f"https://www.ipdb.org/files/317/{filename}", "sha256": digest, "revision": revision, "source_id": "ipdb:317",
		"original_filename": filename, "acquired_at": acquired, "license": "NOASSERTION", "rights": MANUAL_RIGHTS, "attribution": MANUAL_ATTRIBUTION,
		"locator": (f"Williams {kind} for game 495 from IPDB machine https://www.ipdb.org/machine.cgi?id=317, downloaded from {WAYBACK.format(stamp=stamp, name=filename)} because IPDB "
			f"is Cloudflare-gated; retained unchanged at external:pinmame-manuals/{(MANUAL_DIRECTORY / filename).as_posix()}; {pages} PDF pages, {size} bytes, scanned images read visually."),
		"excerpts": [excerpt(n) for n in names]}


def sources(root: Path) -> list[dict[str, Any]]:
	common = {"license": "BSD-3-Clause", "attribution": "PinMAME contributors", "revision": REVISION, "acquired_at": REVISION_COMMITTED}
	table = spatial.read_seed(root)["table"]
	records = [
		document(MANUAL, ["lamp-matrix.md", "switch-matrix.md", "solenoid-connections.md", "game-operation.md", "diagnostics.md", "cabinet-and-power.md"]),
		document(DRAWINGS, ["lamp-wiring.md", "insert-board.md", "cabinet-and-power.md", "switch-matrix.md", "solenoid-connections.md", "game-operation.md", "sound-board.md"]),
		{"id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=317", "sha256": IPDB_PAGE[1], "source_id": "ipdb:317", "acquired_at": IPDB_ACQUIRED,
			"locator": (f"IPDB machine 317 page as captured by the Wayback Machine (capture 20250218215702, fetched through its id_ address), retained at "
				f"external:pinmame-manuals/{(MANUAL_DIRECTORY / IPDB_PAGE[0]).as_posix()}, {IPDB_PAGE[2]} bytes: Blackout, Williams, June 1980, model 495, System 6, 7,050 units. "
				"Its notes describe the G.I. relay; its file links supplied the two retained documents."),
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database; capture by the Internet Archive's Wayback Machine", "excerpts": [excerpt("identity.md"), excerpt("cabinet-and-power.md")]},
		{"id": OPDB, "kind": "human_review", "uri": "https://mp-data.sfo3.cdn.digitaloceanspaces.com/latest-opdb.json", "sha256": OPDB_SHA, "acquired_at": OPDB_ACQUIRED,
			"locator": "Retained external:pinmame-review-artifacts/opdb-import/latest-opdb.json; group GRwYo and machine GRwYo-MQoPw, Blackout, Williams, IPDB 317, manufactureDate 1980-06-01.",
			"license": "NOASSERTION", "attribution": "Open Pinball Database contributors", "excerpts": [excerpt("identity.md")]},
		{"id": SOURCE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/s6games.c", "sha256": SOURCE_FILES["src/wpc/s6games.c"],
			"locator": ("INITGAMEFULL macro; the blkou block: INITGAMEFULL(blkou,s6_6digit_disp,0,46,22,21,23,44,43,0), the S6_ROMSTART/S67S members of l1, l1ff, f1, f1ff, t1 and t1ff, "
				"CORE_GAMEDEF(blkou,l1,\"Blackout (L-1)\",1980,\"Williams\",s6_mS6S,0) and its five CORE_CLONEDEF clones; the header comment on green1fpfix.716."), **common},
		{"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/s6.c", "sha256": SOURCE_FILES["src/wpc/s6.c"],
			"locator": ("s6_6digit_disp, s6_dips_r, s6_swrow_r, s6_sol9_16_w, setSSSol, s6_gameon_w, the PIA map, s6_vblank (special solenoids from ssSw) and SWITCH_UPDATE(s6). Also "
				"s6.h S6_COMPORTS and the S6_SW* constants, core.c core_updateSw and the flipper column, core.h FLIP_SWNO and CORE_CLONEDEF, wmssnd.c s67s_cmd_w and driver.c's "
				"blkou comments at the same revision."), **common},
	]
	for filename in ["src/wpc/core.c", "src/wpc/core.h", "src/wpc/driver.c", "src/wpc/s6.h", "src/wpc/wmssnd.c"]:
		records.append({"id": "pinmame.dependency." + slug(filename), "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/{filename}",
			"sha256": SOURCE_FILES[filename], "revision": REVISION, "acquired_at": REVISION_COMMITTED,
			"locator": "Source read-path, flipper, driver-list and sound dependency cited by pinmame.system-6-current. LICENSE SHA-256 " + SOURCE_FILES["LICENSE"],
			"license": "BSD-3-Clause" if filename.endswith("s6.h") else "LicenseRef-PinMAME-Old-MAME", "attribution": "PinMAME contributors",
			"rights": "Pinned repository LICENSE distinguishes explicitly marked BSD files from inherited old-MAME files; no blanket BSD assertion for unmarked core, driver-list and sound dependencies."})
	sbr_name, sbr_digest = SCRIPT_FILES[SCRIPT]
	mod_name, mod_digest = SCRIPT_FILES[MOD_SCRIPT]
	records += [
		{"id": SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/{quote(sbr_name, safe='/')}", "revision": SCRIPT_REVISION,
			"sha256": sbr_digest, "acquired_at": SCRIPT_REVISION_COMMITTED,
			"locator": (f"{sbr_name} in the pinned known-working script corpus, 3765 lines; cGameName blkou_l1, S6.vbs. Runtime authority for the solenoid callbacks (1 trough, 4 and 5 the "
				"bank resets, 6 the eject saucer, 14 knocker, 15 the G.I. 'inverted, enabled = OFF'), the one-ball trough on 9, the series switches 28 and 36 and the switch and lamp "
				"bindings. Its writes to 46 are overwritten by PinMAME's flipper copy; it binds no lamp 11 or 56."),
			"license": "NOASSERTION", "attribution": "Not named in the script; its option comments credit Sixtoe's original walls and floor and other contributors' routines", "known_working": True,
			"excerpts": [excerpt("script-bindings.md")]},
		{"id": MOD_SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/{quote(mod_name, safe='/')}", "revision": SCRIPT_REVISION,
			"sha256": mod_digest, "acquired_at": SCRIPT_REVISION_COMMITTED,
			"locator": (f"{mod_name} in the same corpus, 782 lines, header 'Thalamus 2018-07-24'; the lineage of the retained table's embedded script, with the same bindings and "
				"UseSolenoids=2. It agrees with SBR34 on every address it binds."),
			"license": "NOASSERTION", "attribution": "Thalamus (2018 revision) and the earlier S34 table author, who is not named in the script", "known_working": True,
			"excerpts": [excerpt("script-bindings.md")]},
		{"id": TABLE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{table['path']}/{table['filename']}", "original_filename": table["filename"], "sha256": table["sha256"],
			"acquired_at": table["acquired_at"],
			"locator": (f"Community table (release label S34 v1.1; the embedded table info names no author) from the operator's read-only table archive, {table['size']} bytes; no download "
				f"URL is asserted and it is not known to have been played. {table['extractor']} extraction {table['extraction']}: {table['file_count']} files, {table['byte_count']} bytes, "
				f"manifest SHA-256 {table['manifest_sha256']} (tools/build_external_evidence_manifest.py). Bounds left 0, top 0, right 952, bottom 1974. The geometry source of every "
				"observed placement."),
			"license": "NOASSERTION", "attribution": "S34 table author, not named in the file; redistribution rights not granted", "rights": "NOASSERTION", "excerpts": [excerpt("spatial-method.md")]},
		{"id": EMBEDDED, "kind": "vpx_script", "uri": f"external:pinmame-vpx-sources/{table['path']}/{table['extraction']}/script.vbs", "original_filename": "script.vbs",
			"sha256": table["script_sha256"], "acquired_at": EXTRACTED,
			"locator": ("The retained table's embedded script (S34 v1.1, ASCII, CRLF, 684 lines). It has the Mod - S34 v1.1 bindings: the one-ball bsTrough on 9, the eject saucer on 40, "
				"both drop banks with AllDownSw 28 and 36, SolSpecial switching the GI collection from 15, and lamp bindings 1-10, 12-53, 55 and 57-64. It names each placed object."),
			"license": "NOASSERTION", "attribution": "S34 table author, not named in the file", "known_working": False, "excerpts": [excerpt("script-bindings.md"), excerpt("spatial-method.md")]},
	]
	runtime = load_json(root / RUNTIME)
	records.append({"id": RUN, "kind": "runtime_scenario", "uri": "repo:" + RUNTIME.as_posix(), "sha256": sha(root / RUNTIME), "revision": REVISION,
		"locator": ("Compact evidence derived by tools/blackout_runtime_evidence.py from four retained blkou_l1 runs (init, Test 02, Test 03, gameplay) on the 46e1a01a LibPinMAME build; "
			"raw traces under external:pinmame-review-artifacts/" + HARNESS.as_posix() + ", pinned by manifest SHA-256 " + HARNESS_MANIFEST_SHA + ". Every cited display frame is pinned in "
			+ READINGS.as_posix() + ". " + runtime["recreation_notes"][0]["text"]),
		"acquired_at": RUN_PERSISTED, "license": "NOASSERTION", "attribution": "pinmame-game-defs curator; acquired_at is final raw trace persistence time"})
	return records


DRIVER_NOTES = {
	"blkou_l1": ("Williams L-1 production set: game ROM, green flipper ROMs 1 and 2, sound ROM 2 and the Speech Module ROMs (IC7, IC5, IC6), matching the pinned s6games.c SHA-1 values. "
		"The booklet requires green-labeled BLACKOUT PROMs or game ROM and green-labeled flipper ROMs on a revision 6 CPU board. Every harness run uses this driver.", "identical"),
	"blkou_l1ff": ("L-1 with the community free-play fix: flipper ROM 1 replaced by green1fpfix.716, which keeps the credit knocker working when free play is set (s6games.c header "
		"comment). Same init data, hardware and addresses.", "identical"),
	"blkou_f1": ("L-1 with French speech ROMs (speech4f-7f.532) on the Speech Module; IPDB lists a French Speech romset and credits Paul Dussault with the French speech processing. "
		"Same game and flipper ROMs, hardware and addresses.", "identical"),
	"blkou_f1ff": ("French speech with the free-play-fix flipper ROM 1. Same hardware and addresses.", "identical"),
	"blkou_t1": ("Ted Estes's T-1 revision (driver.c: /10 scoring): flipper ROM 2 replaced by green2a.716 on the L-1 set. Same hardware and addresses; it was not run here.", "identical"),
	"blkou_t1ff": ("T-1 with the free-play-fix flipper ROM 1. Same hardware and addresses.", "identical"),
}
DRIVER_DESCRIPTIONS = {"blkou_l1": "Blackout (L-1)", "blkou_l1ff": "Blackout (L-1 Free Play Fix)", "blkou_f1": "Blackout (L-1, French Speech)",
	"blkou_f1ff": "Blackout (L-1, French Speech, Free Play Fix)", "blkou_t1": "Blackout (T-1 Ted Estes)", "blkou_t1ff": "Blackout (T-1 Ted Estes, Free Play Fix)"}


def drivers() -> list[dict[str, Any]]:
	out = []
	for identifier in sorted(DRIVER_DESCRIPTIONS):
		notes, compatibility = DRIVER_NOTES[identifier]
		d = {"id": identifier, "description": DRIVER_DESCRIPTIONS[identifier], "manufacturer": "Williams", "year": "1980", "flags": 0,
			"physical_compatibility": compatibility, "variant_notes": notes}
		if identifier != GAME:
			d["clone_of"] = GAME
		out.append(d)
	return out


def build(root: Path = ROOT) -> dict[str, Any]:
	displays = []
	layouts = [("player-1-score", "Player 1 score, six digits", 0, 0, 6), ("player-2-score", "Player 2 score, six digits", 1, 8, 6),
		("player-3-score", "Player 3 score, six digits", 2, 20, 6), ("player-4-score", "Player 4 score, six digits", 3, 28, 6),
		("credits", "Credit display, two digits (tests and bookkeeping show their test number here)", 4, 14, 2),
		("ball-in-play", "Ball in play and match display, two digits (functions, solenoid and switch numbers in diagnostics)", 5, 6, 2)]
	for key, label, index, start, width in layouts:
		displays.append({"id": f"display.{key}", "label": label, "kind": "segment", "controller_index": index, "segment_start": start, "width": width,
			"physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", CORE, MANUAL), "provenance": provenance(CORE, SOURCE, MANUAL, RUN)})
	relationships = [{"id": f"relationship.special-{sensor}-{address}", "kind": "direct", "source": switch_id(sensor), "destination": solenoid_id(address),
		"provenance": provenance(CORE, SOURCE, MANUAL, RUN)} for address, sensor in SPECIAL_SWITCHES.items()]
	relationships.append({"id": "relationship.right-button-lane-change", "kind": "direct", "source": "switch.right-flipper-button", "destination": switch_id(46),
		"provenance": provenance(CORE, SOURCE, RUN)})
	definition = {"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Blackout", "manufacturer": "Williams", "year": 1980, "model_number": "495", "kind": "physical_pinball", "ipdb_id": 317, "opdb_id": "GRwYo-MQoPw"},
		"controller": {"platform": "pinmame.system-6", "hardware_generation": "0x20000", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": inputs(), "outputs": outputs(), "displays": displays, "mechanisms": mechanisms(), "relationships": relationships,
		"coverage": {"status": "partial", "missing": MISSING, "dimensions": {
			"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
			"mechanisms": "observed", "variant_coverage": "validated", "recreation_knowledge": "observed", "spatial_placement": "observed"}},
		"conflicts": [], "sources": sources(root), "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "partial"}}
	ids = [d["id"] for key in ("inputs", "outputs", "displays", "mechanisms", "relationships") for d in definition[key]]
	if len(ids) != len(set(ids)):
		raise RuntimeError("duplicate device identifiers")
	return spatial.apply(definition, root)


KNOWLEDGE_TEXT = """# Blackout (Williams, 1980)

Coverage remains **partial**: every requirement except spatial placement is met. Addresses,
names, wiring, polarity, displays and mechanisms come from the instruction booklet and the
instruction manual and drawing set, the pinned PinMAME source, four retained runs of the `blkou_l1`
ROM and the two pinned corpus scripts. Placements are `observed` readings of one community table,
and no lamp has a placement.

## Identity

Williams game 495, IPDB 317, OPDB `GRwYo-MQoPw`, System 6. IPDB gives June 1980 and 7,050 units;
OPDB's `manufactureDate` 1980-06-01 agrees. OPDB's `display: alphanumeric` is wrong for this
machine: PinMAME declares six-digit seven-segment player displays and two-digit credit and
ball-in-play displays, and the booklet and the harness read only numerals from them. The
instruction booklet is 16P-495-103 (April 1980); the drawing set's cover reads 16P-495-101. IPDB
records that the playfield layout was reused for Rowamet's Heavy Metal and Taito do Brasil's Vortex,
and nearly so for Williams' Warlok; those are other machines.

Six drivers run on this one machine and share one game data block (`CORE_CLONEDEF` of `blkou_l1`),
so their addresses are identical. `l1` is the Williams production set; `f1` swaps in French speech
ROMs; `t1` swaps flipper ROM 2 for Ted Estes's `/10 Scoring` revision; each `ff` variant swaps
flipper ROM 1 for the community free-play fix. Only `blkou_l1` was run. The authorized ROM library also
holds `blkou_hf.zip`, byte-identical to `blkou_l1.zip`; no pinned driver is named `blkou_hf`, so it
is not a driver of this record.

## Controller and address dispositions

System 6 (`0x20000`), `s6_6digit_disp`. Switches and lamps number `(column - 1) * 8 + row`, which
the booklet's Figure 5 and Figure 6 follow.

- Service inputs: -7 Advance (7SW75) and -6 Auto-Up / Manual-Down (7SW74) on the coin door, wired
  to CPU connector 1J4; -5 the DIAGNOSTIC pushbutton and -3 MASTER COMMAND ENTER beside the
  Master Command switches behind the insert door; -4 the sound board's diagnostic pushbutton.
  Public -6 reads 1 for Auto-Up.
- Matrix switches 1-15, 18-23 and 25-45 are fitted (1-8 in the cabinet and on the coin door, the
  rest on the playfield). 16, 17, 24 and 47-64 are printed NOT USED, and the playfield switch
  sheet draws no contact for 16, 17 or 24; Test 03 still names a held 16, 17 or 24 because the ROM
  reports every closure it reads in columns 1-6.
- 46 is the playfield RIGHT FLIPPER LANE CHANGE SWITCH on the real machine, but PinMAME copies the
  right cabinet flipper button (82) into it on every update (`FLIP_SWNO(0,46)`), so a consumer
  drives 82. The left button (84) is copied nowhere. 81, 83 and 85-88 are unused.
- DIP 1 and 2 are the sound board's DS1 miniature switches, crossed against their printed numbers:
  the Sound Board Logic Diagram wires DS1 position 2 to IC10 PB5 and position 1 to PB6, an ON switch
  grounds its line, and PinMAME copies Sound Dip 1 and 2 uninverted onto PB5 and PB6. So public
  DIP 1 is switch 2, speech (0 enabled, 1 inhibited), and public DIP 2 is switch 1, the sound
  select (0 musical notes, 1 synthesized sounds). DIP 17, 18 and 19 are Master Command switches 8 (zero audit totals), 7 (restore factory settings) and 6
  (auto-cycle). 9-16 and 20-24 are unused.
- Every matrix contact is normally open: the switch sheets draw each as an open contact with a
  diode, the read path is not inverted, and Test 03 shows each held public 1. A drop target switch
  is closed while its target is down; each 3-bank also has a series switch (28, 36).
- Lamps 1-10, 12-49 and 56 are playfield inserts, one designated bulb each. 50-55 and 57-64 are
  insert board lamps in the backbox (62 Game Over, 63 Same Player Shoots and 64 High Score have two
  bulbs in parallel). 11 is not fitted: the lamp sheet leaves its cell blank.
- Solenoids 1, 4, 5, 6, 14, 16 and 17-21 are coils as Table 3 prints them; 9-13 are sound command
  lines to the sound board; 15 is the Special Relay; 2, 3, 7, 8 and 22 are printed Not Used and drawn
  N/C, and only the Solenoid Test pulses them. 23 is game-on: it pulls in the flipper relay Z1 and
  enables the specials. 45-48 are PinMAME's synthetic flipper states.

Four six-digit player displays map to controller indices 0-3 and the credit and ball-in-play
displays to 4 and 5. The booklet's tests show their number in the credit display and the function,
solenoid or switch number in the ball-in-play display, where the match digits also appear.

## Ball path and mechanisms

A drained ball rests on the outhole switch 9; the ball release 1 kicks it into the shooter lane and
the player plunges. No transcribed page counts the balls installed; the rules have no multiball,
both scripts load one ball, and the gameplay run served one ball at a time. Start fires game-on 23,
the 3-bank resets 4 and 5 and then 1; a drain fires 4, 5 and 1 again.

Two 3-banks of drop targets: the center bank (25-27, series 28, reset 4) below the bottom jet
bumper and the top bank (33-35, series 36, reset 5) at the upper right. Each reset raises its whole
bank. The ROM resets a bank when its series switch closes, not when the three target switches are
merely down. The center bank lights the eject hole red lamp; the top bank the yellow lamp and
BLACKOUT.

Five green standup targets (11 at the bottom to 15 at the top) light the eject hole green lamp.
The left spinner 18 and the upper right spinner 37 make the spinner loop, which collects and
advances the loop lamps 33-36; advancing past 20,000 lights the eject hole for Extra Ball. Standups
19 and 38 score 50.

Three jet bumpers (17 left, 18 right, 19 bottom) and two kickers (20 left, 21 right) are special
solenoids. Each has a scoring matrix switch (22, 21, 23, 44, 43) that PinMAME uses for the slot and
a separate direct-drive special contact (8SW65-8SW69, the kickers' drawn as two contacts in
parallel) that is not a public input. Slot 22 has no switch and no load.

Each flipper is one SFL-19-400/30-750-DC coil with an end-of-stroke contact across it, switched by
its cabinet button through Z1. PinMAME publishes 45/46 (right) and 47/48 (left) together while 23
is set; they model neither winding nor end of stroke. The right flipper is also the Lane Change:
the "1-2-3" lamps rotate when it is actuated. In the gameplay run the right button moved a lit
"1" to "2" and then "3".

## The Blackout sequence and the general illumination

The 6.3 VAC general illumination returns through a normally closed contact of the Special Relay
6L15, which solenoid 15 drives. That contact carries every G.I. output on the power sheet: the coin
door (7P1-2), the playfield (8P2-2) and the insert board (9P1-2, 9P1-5). Energizing 15 darkens all
of them. IPDB calls it the G.I. Relay on the backbox floor and says it cut the playfield lamps; the
power sheet shows the wider reach, and the record follows it. Most System 6 games feed their G.I.
from an unswitched winding, and System 6 publishes no G.I. channel; on Blackout the G.I. is an
ordinary solenoid output.

With the eject hole's green, yellow and red lamps lit, BLACKOUT 46 lights and doubles the eject
hole value. In the gameplay run a ball entering the eject hole then pulsed 15 seven times, the
fourth pulse holding it 2.30 s. Every lamp went out 0.09 s after the entry, lamps 1-64 then lit one
by one during the long hold, the coin lockout 16 dropped at 0.08 s and returned at 4.56 s, and the
eject kicker 6 fired at 5.09 s with lamps 43-46 out. Whether the sequence also runs without BLACKOUT
lit was not observed. The embedded script's `BlackoutMode = 1` (a 'fantasy mode' that keeps the
G.I. off until the drain) is the table's own option, not the machine.

## Sources that disagree, and what the record follows

None of these is a conflict: each is a wiring detail, a misprint, a label variant or a defect in
a consumed table.

- The playfield solenoid sheet labels the flipper coils the other way round from Table 3 (8L25
  RIGHT FLIPPER on BLU-GRY 8P3-4, 8L24 LEFT on BLU-VIO 8P3-3, 2P12-1 LEFT). Table 3, its note 2 and
  the cabinet sheet's 7SW72 RIGHT FLIPPER agree with each other, and the record follows them.
- Figure 5 prints switch 15 `5 BANK #5 (TOP)`; the chart and the wiring sheet call it a green
  target. The wiring sheet's matrix drawing omits 8SW39 although its own switch list carries 39.
- Figure 6 and the bulb list place the position qualifiers differently on lamps 23, 24, 31 and 32;
  Figure 6 prints lamp 44 YELLOW and the bulb list Amber.
- The booklet's Credit Posting paragraph ends 'coins are rejected while lockout is energized'; its
  own preceding sentence and the Test 02 run make the lockout energized while coins are accepted.
- The drawing set's foreword names IC14 and IC16 sockets where the booklet prints IC14 and IC26, and
  adds 'and magnet' to the F4 line; Blackout has no magnet.
- IPDB's G.I. relay sentence (above) and OPDB's display type.
- The embedded script comments out lamp 54 (Match), and SBR34 writes the lane-change switch 46
  directly; neither changes the machine.

## Runtime evidence

Four runs of the authorized `blkou_l1` ROM on the 46e1a01a LibPinMAME build, each in a fresh state
directory: an initialization run from empty CMOS (which stops in the diagnostic mode the drawing set
describes, credits 04, ball in play 00 and `1495 1`), then the Solenoid Test, the Switch Test and a
scripted game seeded from that run's NVRAM. Test 02 steps 01-22 pulse public 1-22 one at a time and
then wrap to 01, which pairs every printed solenoid number with its public address; Test 03 names
each held switch 1-46; the game exercises the coin, the start sequence, every special, both banks,
the lane change, the Blackout sequence, the outhole and the ball roll tilt. The compact evidence lives
in `evidence/runtime/system-6/blackout-1980.json`, and every display frame it cites is pinned in
`tools/seeds/williams/blackout-1980-display-readings.json`. A run shows what a public address does
under those conditions; it does not prove bulb counts or locations.

## What would complete this record

Spatial placement is the one open requirement:

- Lamps 1-10, 12-49 and 56 have no placement. The retained table draws every insert as a light with
  no bulb, which marks no socket, and has no light for 56; no lamp-location drawing was measured. A
  table that models the bulbs, or a measured factory playfield drawing, would supply them.
- Switches 9, 19, 32 and 38 and solenoid 1 have no defensible position in the retained table; the
  spatial report gives the reason for each.
- Every placement is `observed` from one community table that is not known to have been played.
  Measuring the callouts of Figure 3 and Figure 4 against the table would validate them.
"""


def verify_files(root: Path = ROOT) -> None:
	spatial.read_seed(root)
	for name, digest in [*EXCERPTS.items(), *((image, digest) for image, digest, _ in IMAGES.values())]:
		path = root / "evidence/excerpts" / MACHINE_ID / name
		if not path.is_file() or sha(path) != digest:
			raise RuntimeError(f"excerpt absent or changed: {path}")
	for relative, digest in [(RUNTIME, RUNTIME_SHA), (READINGS, READINGS_SHA)]:
		if not (root / relative).is_file() or sha(root / relative) != digest:
			raise RuntimeError(f"runtime evidence absent or changed: {relative}")
	for run in load_json(root / RUNTIME)["runtime"]["raw_runs"]:
		path = root / run["scenario_path"]
		if not path.is_file() or sha(path) != run["scenario_sha256"]:
			raise RuntimeError(f"scenario absent or changed: {path}")


def expected_artifacts(root: Path = ROOT) -> dict[Path, bytes]:
	verify_files(root)
	definition = build(root)
	report = spatial.report(definition, root)
	return {DEFINITION: canonical_bytes(definition), SEED: canonical_bytes(definition), KNOWLEDGE: KNOWLEDGE_TEXT.encode("utf-8"),
		REPORT: canonical_bytes(report), REPORT_MD: spatial.report_markdown(report).encode("utf-8")}


def guard_destination(root: Path) -> None:
	tail = DEFINITION.relative_to("machines/partial")
	for directory in ["author-ready", "stubs"]:
		path = root / "machines" / directory / tail
		if path.exists():
			raise RuntimeError(f"refusing stale or author-ready destination: {path}")
	path = root / DEFINITION
	if path.exists():
		try:
			status = load_json(path)["coverage"]["status"]
		except (ValueError, KeyError, TypeError) as exc:
			raise RuntimeError(f"curator drift: invalid destination {DEFINITION}") from exc
		if status == "author_ready":
			raise RuntimeError("refusing to overwrite an existing author-ready artifact")


def regenerate(root: Path = ROOT) -> None:
	guard_destination(root)
	verify_external(root)
	for relative, content in expected_artifacts(root).items():
		path = root / relative
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(content)


def check(root: Path = ROOT) -> None:
	guard_destination(root)
	for relative, content in expected_artifacts(root).items():
		path = root / relative
		if not path.is_file() or path.read_bytes() != content:
			raise RuntimeError(f"curator drift: {relative}")


def configured_root(variable: str) -> Path | None:
	value = os.environ.get(variable)
	if value is None:
		return None
	path = Path(value)
	if not value.strip() or not path.is_dir():
		raise RuntimeError(f"configured evidence root unavailable: {variable}={value!r}")
	return path


def manifest_targets() -> list[tuple[str, Path, str]]:
	"""(root variable, directory under that root, pinned manifest SHA-256) for each retained directory."""
	table = load_json(ROOT / spatial.SEED)["table"]
	return [("PINMAME_VPX_SOURCES_ROOT", Path(table["path"]) / table["extraction"], table["manifest_sha256"]),
		("PINMAME_REVIEW_ARTIFACTS_ROOT", HARNESS, HARNESS_MANIFEST_SHA)]


def write_manifests() -> None:
	"""Write the canonical manifests of the retained extraction and harness directories; refuse a result that differs from the pin."""
	for variable, relative, pinned in manifest_targets():
		root = configured_root(variable)
		if root is None:
			raise RuntimeError(f"{variable} must be set to write its manifest")
		digest = write_manifest(root / relative, GAME)
		if digest != pinned:
			raise RuntimeError(f"rewritten manifest {relative} is {digest}, not the pinned {pinned}")


def verify_external(root: Path = ROOT) -> None:
	"""Optional roots are skipped when absent and fail closed when configured."""
	verify_files(root)
	manuals = configured_root("PINMAME_MANUALS_ROOT")
	if manuals is not None:
		directory = manuals / MANUAL_DIRECTORY
		for filename, digest, size, *_ in [*DOCUMENTS.values(), IPDB_PAGE]:
			path = directory / filename
			if not path.is_file() or path.stat().st_size != size or sha(path) != digest:
				raise RuntimeError(f"retained document absent or changed: {path}")
	review = configured_root("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if review is not None:
		try:
			digest = check_manifest(review / HARNESS, GAME)
		except ValueError as exc:
			raise RuntimeError(f"raw harness directory manifest absent or changed: {exc}") from exc
		if digest != HARNESS_MANIFEST_SHA:
			raise RuntimeError("raw harness directory manifest absent or changed")
		runtime_evidence.check(review, root)
		nvram = review / HARNESS / f"init-state/nvram/{GAME}.nv"
		if not nvram.is_file() or sha(nvram) != NVRAM_SHA:
			raise RuntimeError("initialization NVRAM absent or changed")
		snapshot = review / "opdb-import/latest-opdb.json"
		if not snapshot.is_file() or sha(snapshot) != OPDB_SHA:
			raise RuntimeError("retained OPDB snapshot absent or changed")
	checkout = configured_root("PINMAME_SOURCE_ROOT")
	if checkout is not None:
		for name, digest in SOURCE_FILES.items():
			path = checkout / name
			if not path.is_file() or sha(path) != digest:
				raise RuntimeError(f"pinned source absent or changed: {path}")
	scripts = configured_root("PINMAME_VPX_SCRIPTS_ROOT")
	if scripts is not None:
		for name, digest in SCRIPT_FILES.values():
			path = scripts / name
			if not path.is_file() or sha(path) != digest:
				raise RuntimeError(f"pinned script absent or changed: {path}")
	roms = configured_root("PINMAME_ROM_LIBRARY_ROOT")
	if roms is not None:
		archive = roms / f"{GAME}.zip"
		if not archive.is_file() or sha(archive) != ROM_SHA:
			raise RuntimeError("authorized ROM archive absent or changed")
		with ZipFile(archive) as z:
			members = {m.filename: (m.file_size, hashlib.sha1(z.read(m)).hexdigest()) for m in z.infolist()}
		if members != ROM_MEMBERS:
			raise RuntimeError("ROM members differ from the pinned s6games.c declarations")
	spatial.verify_external(root, configured_root)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	mode.add_argument("--write-manifests", action="store_true", help="rewrite the retained extraction and harness manifests and require the pinned digests")
	args = parser.parse_args()
	if args.check:
		check()
		verify_external()
		print("Blackout definition, seed, knowledge, excerpts, runtime evidence and spatial blockers match.")
	elif args.write_manifests:
		write_manifests()
		print("Blackout extraction and harness manifests rewritten and match their pins.")
	else:
		regenerate()
		print("Regenerated Blackout partial artifacts.")


if __name__ == "__main__":
	main()
