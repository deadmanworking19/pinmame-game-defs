"""Deterministic, deliberately partial Barracora (Williams, 1981) curation.

Authority: the instruction booklet, drawing set and parts supplement for physical construction and
wiring; the pinned PinMAME source for transport; the retained barra_l1 harness runs for observed ROM
behavior; the pinned VR Room script for runtime bindings. Placements come from one retained community
table and stay `observed`; no lamp is placed because no public lamp in that table sits on a bulb.
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
import barracora_runtime_evidence as runtime_evidence  # noqa: E402
import barracora_spatial as spatial  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.barracora.1981"
GAME = "barra_l1"
BASE = "40fe189b4cfd47786350e667303aa3789b095563"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
LIBRARY_SHA = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_SHA = "3f9e8a3b4cce3112a1293c26746552a91e0c8e9c35b7d0027b982e0b9115f88d"
ROM_MEMBERS = {
	"ic14.716": (2048, "0fa17b7912f8129e40de5fed8c3ccccc0a2a9366"),
	"ic17.532": (4096, "fb0b7f247673dae0744d4188e1a03749a2237165"),
	"ic20.716": (2048, "bcf017b01236f755cee419e398bbd8955ae3576a"),
	"ic26.716": (2048, "f1f2d4c1baed698d3b7cf2e88a2c28056e859920"),
	"sound4.716": (2048, "f81e97183442736d5766a7e5e074bc6539e8ced0"),
}
NVRAM_SHA = "9bdd907251c4ef7b765bbf9f02fddeb38fd21ba9ee7bd03e7d76ed1bbb1afd79"
HARNESS = runtime_evidence.HARNESS
HARNESS_MANIFEST_SHA = "28f8a624635a8830cabeaebf0f9f7bbcdbd72ae49a9e609f314edea8c140623e"
OPDB_SHA = "690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93"
DEFINITION = Path("machines/partial/williams/barracora-1981.json")
SEED = Path("tools/seeds/williams/barracora-1981.json")
KNOWLEDGE = Path("knowledge/williams/barracora-1981.md")
REPORT = Path("reports/spatial/williams/barracora-1981.json")
REPORT_MD = REPORT.with_suffix(".md")
RUNTIME = runtime_evidence.OUTPUT
RUNTIME_SHA = "c5d6c2f68d6cc9a5e3ce37b4a08b7349ce840b165b4f5159861942f079f46cb7"
READINGS = runtime_evidence.READINGS
READINGS_SHA = "38dedb4e7edea78f4c9ea1251394c874906b3aaa3abc663888b55c228aa205f2"
MANUAL_DIRECTORY = Path("by-machine") / MACHINE_ID
WAYBACK = "https://web.archive.org/web/{stamp}id_/https://www.ipdb.org/files/177/{name}"
ACQUIRED = "2026-10-31T06:54:31Z"
# Generation times: the committer dates of the pinned PinMAME and script-corpus revisions, and the creation time of the
# retained table's extracted-vpxtool/script.vbs.
REVISION_COMMITTED = "2026-10-25T20:16:49Z"
SCRIPT_REVISION_COMMITTED = "2026-07-07T06:37:05Z"
EXTRACTED = "2026-10-31T07:01:54Z"
MANUAL_RIGHTS = "NOASSERTION; retained for local research; original copyright retained; full document not redistributed"
MANUAL_ATTRIBUTION = "Williams Electronics, Inc.; hosted by the Internet Pinball Database, retrieved from the Internet Archive's Wayback Machine"

MANUAL = "manual.barracora-booklet"
DRAWINGS = "manual.barracora-drawing-set"
PARTS = "manual.barracora-parts-supplement"
IPDB = "ipdb.barracora"
OPDB = "opdb.barracora"
SOURCE = "pinmame.barracora"
CORE = "pinmame.system-7-current"
SCRIPT = "vpx.barracora-vr-room-2-1-3"
OLD_SCRIPT = "vpx.barracora-mod-1-3"
TABLE = spatial.TABLE
EMBEDDED = spatial.EMBEDDED
RUN = "runtime.barracora"

# (source id, filename, SHA-256, bytes, PDF pages, Wayback capture, revision, document type)
DOCUMENTS = {
	MANUAL: ("Williams_1981_Barracora_Operators_Handbook.pdf", "ef8950deb1916fc1cb516fd3b8eae53fd6a7b776d805c610160981c3bba3d7fa", 846126, 15, "20260212205538", "16P-510-103", "instruction booklet"),
	DRAWINGS: ("Williams_1981_Barracora_Instruction_and_Drawing_Set_paginated_schematics_cover_page_missing.pdf", "ea5062c37dfb44d0132bef77ac2aefff1e80d45dc295be87a936de26198397ef", 4384576, 21, "20260216084601", "game 510 drawing set", "drawing set"),
	PARTS: ("Williams_1981_Barracora_Parts_Suppliment.pdf", "2204a860f05472cd36cc17a69e73edcdd5762a5714ea038d145501bfe6ad175b", 3404660, 13, "20260214123952", "16P-510-110 October 1981", "parts supplement"),
}
IPDB_PAGE = ("ipdb-177.html", "fd5e5f84a97ee26bfc74cc5607b5346e87589df17ecad71dc83a5becf32b2ddd", 49386)
SOURCE_FILES = {
	"LICENSE": "21cde7ac6cffe0fa9e3a66beb89e0db1b78caa7bb8b8041d1b483f36460e026e",
	"src/wpc/core.c": "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00",
	"src/wpc/core.h": "b6c03b20a09fbadff1ce16f9f1cfc9e5bace08857cb998b92d8f304695ec97c0",
	"src/wpc/s7.h": "00849d86671f0cfc3e2ce3bed12a2e2023c5df0dc81ee50123433514d70379ae",
	"src/wpc/wmssnd.c": "5d9d431416150e22fddf850b59e377d7f923fa7bda067e830729891670eff82f",
	"src/wpc/s7games.c": "cc9cf65dc56416331b537f4595b8f6ce6415e018d2bcf502a74d3b974377e6d7",
	"src/wpc/s7.c": "908c575b40483e47fe0296943b69f74506c10081d3fea8ee361611ef7f6a9f85",
}
SCRIPT_FILES = {
	SCRIPT: ("Barracora (Williams 1981) w VR Room v2.1.3.vbs", "89135c332343e5d7bd8a31498e18268f1afa94a195034a55dd2d7bfc9eab05eb"),
	OLD_SCRIPT: ("Barracora (Williams 1981) mod v1.3.vbs", "ca7e4764770a67c57b0e4088ad03c14ceb70b7306690cc631b7707bed4f9bc77"),
}
EXCERPTS = {
	"board-switches.md": "d876f905cdc7299c26b2dfd3113686fe51a8ac6e6b6d3cd1c9548a4585df74cc",
	"cabinet-and-power.md": "41aa7b6753858430890efe152ea2af6d2d81ab5bc704a38e77cc20fc6dce3b81",
	"diagnostics.md": "af5216cdf02b356af0dfd796c4bb760361a5cd71f89cc1ef22a41d4dbd877a43",
	"game-operation.md": "c5e81067185ed9007220e9bb72a6f000cb1f01b8ee97a434f9129f2f0473e77b",
	"identity.md": "1524aa44768d7bd7f817751ead5756d0abd47af9b8d58a1060f2d4dba6bc2779",
	"insert-board.md": "ec01aa36ba7b9bed2e23f403683a3fa52b68b6a463486df3b2d408730a2423f0",
	"lamp-matrix.md": "99db91908c9fce59370623260e10ab9af750c8ae77b39d8a23fe26ebfefbe906",
	"lamp-wiring.md": "05109718a24a13ede887f3463525c794009e8585f5a0d17557e52bd8bb127abd",
	"parts-supplement.md": "52d77aeb507baaa90bbee4cf515e38aa91ea1fe3f94c4e319027807cde2fbe3b",
	"script-bindings.md": "b77f335b7f5dcbf3e3f0ffc05b77990d51864ec3aad94b3cb5724dec268a1b44",
	"solenoid-connections.md": "aaacf50125709c74b923a537941835c6b473d32961eef37e17dbd687d5802cf3",
	"spatial-method.md": spatial.EXCERPT_SHA,
	"switch-matrix.md": "39536dbdaf016acdb521f0757d490539a890ef4194858364000babeceaa54811",
}
LOCATORS = {
	"board-switches.md": "Drawing set PDF page 12 / printed 16, sound board bill of material switch rows; PDF page 5 / printed 8, CPU board bill of material switch rows and the assembly view checked for DS1/DS2",
	"cabinet-and-power.md": "Drawing set PDF page 18 / printed 23 Cabinet Wiring Diagram, PDF page 11 / printed 15 Power Wiring Diagram (K1 and fuses), PDF page 1 foreword board requirements; booklet page 1 fuse sentence",
	"diagnostics.md": "Booklet PDF pages 7, 8, 10, 11, 12 and 14: Display Digits, Sound, Lamp, Solenoid and Switch tests, Auto-Cycle, CPU and sound board self-tests, transcribed in full",
	"game-operation.md": "Booklet PDF pages 1-2 / printed 1-2, board requirements and Game Operation; drawing set PDF page 3, Power Turn-On and Game Setup (first half)",
	"identity.md": "IPDB 177 capture fields, OPDB snapshot entries GRo7K and GRo7K-MQ4e3, the pinned s7games.c barra block and the three documents' covers",
	"insert-board.md": "Drawing set PDF page 14 / printed 19, Insert Board Wiring Diagram: lamp section on 9P1 and display section",
	"lamp-matrix.md": "Booklet PDF page 9 / printed 9, Figure 1 Lamp Matrix: all 64 cells and the column and row headers",
	"lamp-wiring.md": "Drawing set PDF page 19 / printed 24, Playfield Lamp Wiring Diagram: column and row wiring, all 64 location cells, bulb list and general illumination",
	"parts-supplement.md": "Parts supplement 16P-510-110 PDF pages 2, 5 and 6: ROM summary, 3-bank drop target and Ball Gate Lock Assembly parts lists",
	"script-bindings.md": "VR Room v2.1.3 lines 107-850, mod v1.3 lines 48-355 and the retained table's embedded script: solenoid callbacks, switch handlers, ball stacks and the gate handler",
	"solenoid-connections.md": "Booklet PDF pages 10-11 / printed 10-11: Table 4 (every row, column and note), Solenoid Test and Figure 2 chart; drawing set PDF page 20 / printed 25, Playfield Solenoid Wiring Diagram",
	"spatial-method.md": "Retained table identity and extraction, every object and point method, the unplaced devices and the not-applicable devices",
	"switch-matrix.md": "Booklet PDF pages 11-13 / printed 11-13: Figure 5 Switch Matrix (all 64 cells and headers), Figure 3 switch chart and the Switch Test; drawing set PDF page 21 / printed 26 location row",
}
UNREVIEWED = {"identity.md", "script-bindings.md", "spatial-method.md"}

SWITCH_LABELS = [
	"Plumb Bob Tilt", "Ball Roll Tilt", "Credit Button", "Right Coin Switch", "Center Coin Switch", "Left Coin Switch", "Slam Tilt", "High Score Reset",
	"\"BARRACORA\" Lane Rollover", "Upper Eject Hole", "Lower Eject Hole", "Outhole", "Left Ball Ramp Switch", "Center Ball Ramp Switch", "Right Ball Ramp Switch", "Ball Shooter Trough Rollover",
	"1/4 Lane Rollover", "2/5 Lane Rollover", "3/6 Lane Rollover", "Left Jet Bumper", "Right Jet Bumper", "Bottom Jet Bumper", "Left Outside Rollover", "Right Outside Rollover",
	"Spinner Target", "Right Turnaround", "Left Bull's-Eye Target", "Right Bull's-Eye Target", "Left Kicker", "Right Kicker", "Left Inside Rollover", "Right Inside Rollover",
	"Upper Right Bull's-Eye Target", "Left Flipper Lane Change Switch", "Right Flipper Lane Change Switch", "Playfield Tilt", "Upper Right Standup", "Lower Standup", "5-Bank Standup", "Lower Left Standup",
	"B Drop Target", "A Drop Target (B-A-RR bank)", "RR Drop Target", "A Drop Target (A-C-O-R-A bank, first)", "C Drop Target", "O Drop Target", "R Drop Target", "A Drop Target (A-C-O-R-A bank, last)",
]
LAMP_LABELS = [
	"Same Player Shoots Again (Backbox)", "Ball in Play", "Tilt", "Game Over", "Match", "High Score to Date", "B-A-RR Drop Target Bank", "A-C-O-R-A Drop Target Bank",
	"BARRACORA B", "BARRACORA A (2nd letter)", "BARRACORA RR", "BARRACORA A (4th letter)", "BARRACORA C", "BARRACORA O", "BARRACORA R", "BARRACORA A (last letter)",
	"Top Lane Lamp 1", "Top Lane Lamp 2", "Top Lane Lamp 3", "Top Lane Lamp 4", "Top Lane Lamp 5", "Top Lane Lamp 6", "Left Special", "Right Special",
	"Spinner x1000 When Lit", "Shoot Again (Playfield)", "Lower Eject Hole 30", "Lower Eject Hole 60", "Lower Eject Hole 90", "Lower Eject Hole Lock Arrow", "Upper Eject Hole Lock Arrow", "Upper Eject Hole Collect Bonus",
	"Upper Right Bull's-Eye Target 20,000", "Upper Right Bull's-Eye Target 40,000", "Upper Right Bull's-Eye Target Extra Ball When Lit",
	"Left Bull's-Eye Target 5,000", "Left Bull's-Eye Target 10,000", "Left Bull's-Eye Target 15,000", "Left Bull's-Eye Target 20,000", "Left Bull's-Eye Target 25,000",
	"Right Bull's-Eye Target 2X", "Right Bull's-Eye Target 3X", "Right Bull's-Eye Target 4X", "Right Bull's-Eye Target 5X", "Right Bull's-Eye Target 10X",
	"Super 2X Bonus Multiplier", "Super 3X Bonus Multiplier", "Super 4X Bonus Multiplier", "Super 5X Bonus Multiplier",
	"2X Bonus Multiplier", "3X Bonus Multiplier", "4X Bonus Multiplier", "5X Bonus Multiplier",
	"Bonus 1", "Bonus 2", "Bonus 3", "Bonus 4", "Bonus 5", "Bonus 6", "Bonus 7", "Bonus 8", "Bonus 9", "Bonus 10", "Bonus 20",
]
# Table 4 values as printed (solenoid 3's 8P3 pin comes from the drawing set's solenoid sheet).
SOLENOIDS = {
	1: ("B Drop Target Reset", "coil", "GRY-BRN", "2P11-4, 8P3-1", "Q15", "SA5-24-750-DC"),
	2: ("A Drop Target Reset (B-A-RR bank)", "coil", "GRY-RED", "2P11-5, 8P3-2", "Q17", "SA5-24-750-DC"),
	3: ("RR Drop Target Reset", "coil", "GRY-ORN", "2P11-7, 8P3-3", "Q19", "SA5-24-750-DC"),
	4: ("A Drop Target Reset (A-C-O-R-A bank, first)", "coil", "GRY-YEL", "2P11-8, 8P3-4", "Q21", "SA5-24-750-DC"),
	5: ("C Drop Target Reset", "coil", "GRY-GRN", "2P11-9, 8P3-5", "Q23", "SA5-24-750-DC"),
	6: ("O Drop Target Reset", "coil", "GRY-BLU", "2P11-3, 8P3-6", "Q25", "SA5-24-750-DC"),
	7: ("R Drop Target Reset", "coil", "GRY-VIO", "2P11-2, 8P3-7", "Q27", "SA5-24-750-DC"),
	8: ("A Drop Target Reset (A-C-O-R-A bank, last)", "coil", "GRY-BLK", "2P11-1, 8P3-8", "Q29", "SA5-24-750-DC"),
	9: ("B-A-RR Drop Target Bank Release", "coil", "BRN-BLK", "2P9-9, 8P3-9", "Q31", "SA6-24-750-DC"),
	10: ("A-C-O-R-A Drop Target Bank Release", "coil", "BRN-RED", "2P9-7, 8P3-10", "Q33", "SA6-24-750-DC"),
	11: ("Ball Release", "coil", "BRN-ORN", "2P9-1, 8P3-11", "Q35", "SA3-23-850-DC"),
	12: ("Ball Ramp Thrower", "coil", "BRN-YEL", "2P9-2, 8P3-12", "Q37", "SG1-23-850-DC"),
	13: ("Upper Eject Hole", "coil", "BRN-GRN", "2P9-3, 8P3-13", "Q39", "SG1-23-850-DC"),
	14: ("Lower Eject Hole", "coil", "BRN-BLU", "2P9-4, 8P3-14", "Q41", "SG1-23-850-DC"),
	15: ("Bell", "coil", "BRN-VIO", "2P9-5, 7P1-17", "Q43", "SM-29-100-DC"),
	16: ("Coin Lockout", "coil", "BRN-GRY", "2P9-6, 7P1-18, 7P2-4", "Q45", "SM-35-4000-DC"),
	17: ("Upper Eject Hole Gate", "coil", "BLU-BRN", "2P12-7, 8P3-17", "Q2", "SM-35-4000-DC"),
	18: ("Left Jet Bumper", "coil", "BLU-RED", "2P12-4, 8P3-18", "Q4", "SG1-23-850-DC"),
	19: ("Right Jet Bumper", "coil", "BLU-ORN", "2P12-3, 8P3-19", "Q6", "SG1-23-850-DC"),
	20: ("Bottom Jet Bumper", "coil", "BLU-YEL", "2P12-6, 8P3-20", "Q8", "SG1-23-850-DC"),
	21: ("Left Kicker", "coil", "BLU-GRN", "2P12-8, 8P3-21", "Q10", "SG1-23-850-DC"),
	22: ("Right Kicker", "coil", "BLU-BLK", "2P12-9, 8P3-22", "Q12", "SG1-23-850-DC"),
}
# Public special slot -> scoring matrix switch (INITGAMEFULL ss18-ss22) and Table 4's special switch wiring.
SPECIAL_SWITCHES = {18: 20, 19: 21, 20: 22, 21: 29, 22: 30}
SPECIAL_WIRING = {18: ("ORN-RED", "2P13-3, 8P3-25", "8SW66"), 19: ("ORN-BLK", "2P13-2, 8P3-26", "8SW67"), 20: ("ORN-YEL", "2P13-4, 8P3-27", "8SW68"),
	21: ("ORN-GRN", "2P13-8, 8P3-28", "8SW69"), 22: ("ORN-BLU", "2P13-9, 8P3-29", "8SW70")}
CABINET_SOLENOIDS = {15, 16}
MISSING = ["spatial_placement"]
POLARITY = ("Normally open: the drawing set's switch wiring sheet draws its TYPICAL matrix cell as an open contact in series with a diode, s7.c reads the switch "
	"columns without inversion and barra_l1 declares no inversion mask, and the Test 03 run shows each held public 1 as a closure.")


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
	return f"switch.{slug(SWITCH_LABELS[address - 1])}" if address <= 48 else f"switch.unused-{address}"


def lamp_id(address: int) -> str:
	return f"lamp.{slug(LAMP_LABELS[address - 1])}" if address <= 64 else f"lamp.unused-{address}"


def solenoid_id(address: int) -> str:
	if address == 25:
		return "relay.game-on-flipper-relay"
	if address in SOLENOIDS:
		label, kind, *_ = SOLENOIDS[address]
		return f"{kind}.{slug(label)}"
	if 45 <= address <= 48:
		return f"virtual.{'right' if address <= 46 else 'left'}-flipper-{'power' if address % 2 else 'hold'}"
	return f"virtual.unused-solenoid-{address}"


def matrix_wiring(address: int, lamp: bool = False) -> dict[str, str]:
	"""Column and row wiring printed on the booklet's Figure 1 / Figure 5 headers."""
	col, row = divmod(address - 1, 8)
	if lamp:
		cw = ["BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY"]
		cp = [8, 9, 6, 7, 3, 5, 1, 2]
		rw = ["BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY"]
		rp = [1, 2, 3, 4, 5, 6, 9, 8]
		dc, rc, dp, rpfx = "2J5", "2J7", "YEL", "RED"
	else:
		cw = ["BRN", "RED", "ORN", "YEL", "BLK", "BLU", "VIO", "GRY"]
		cp = [9, 8, 7, 6, 5, 3, 2, 1]
		rw = ["BRN", "RED", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY"]
		rp = [9, 8, 7, 6, 5, 4, 3, 1]
		dc, rc, dp, rpfx = "2J2", "2J3", "GRN", "WHT"
	return {"board": "Williams System 7 driver board", "drive_wire": f"{dp}-{cw[col]}", "drive_connection": f"{dc}-{cp[col]}",
		"return_wire": f"{rpfx}-{rw[row]}", "return_connection": f"{rc}-{rp[row]}"}


SWITCH_NOTES = {
	1: "Cabinet sheet 7SW1 PLUMB BOB TILT. Third closure tilts the ball in play (booklet Tilt paragraph; the count is adjustable).",
	2: "Cabinet sheet 7SW2 BALL ROLL TILT. First closure tilts the ball in play; the gameplay run drops game-on 25 0.04 s after the closure.",
	3: "Cabinet sheet 7SW3 CREDIT BUTTON. Starts a game when three balls rest on the ball ramp or shooter switches.",
	4: "Cabinet sheet 7SW4 RIGHT COIN CHUTE. The gameplay run's coin rings the bell 15 three times.",
	5: "Cabinet sheet 7SW5 CENTER COIN CHUTE.",
	6: "Cabinet sheet 7SW6 LEFT COIN CHUTE.",
	7: "Cabinet sheet 7SW7 SLAM TILT. Returns the game to Game Over (booklet Tilt paragraph).",
	8: "Cabinet sheet 7SW8 HIGH SCORE RESET.",
	9: "Lane rollover scoring 10,000 and one bonus advance per lit BARRACORA letter.",
	10: "Ball-presence contact of the upper eject hole: closed while a ball rests in the hole. Solenoid 13 kicks the ball out.",
	11: "Figure 5 prints this cell `LOWER / HOLE`; the chart, the wiring sheet and the solenoid chart call it the Lower Eject Hole. Ball-presence contact: closed while a ball rests in the hole. Solenoid 14 kicks the ball out.",
	12: "Ball-presence contact: closed while a drained ball rests in the outhole; the gameplay run's closure fires ball release 11.",
	13: "Ball-ramp storage position (the chart's left position), closed while a ball rests there. The VR Room script's ball-ramp objects put 15 at the thrower, 14 in the centre and 13 on the left.",
	14: "Ball-ramp storage position, closed while a ball rests there.",
	15: "Ball-ramp position at the thrower: closed while a ball waits for ball ramp thrower 12.",
	16: "Shooter-lane contact: closed while a served ball rests in the shooter lane. The booklet allows at most one ball here when a game starts.",
	20: "Scoring contact of the left jet bumper. PinMAME also uses it as the special-switch slot for solenoid 18; the factory's direct-drive special contact is 8SW66 on the special-switch harness, which is not a public input.",
	21: "Scoring contact of the right jet bumper; special-switch slot for solenoid 19 (factory special contact 8SW67).",
	22: "Scoring contact of the bottom jet bumper; special-switch slot for solenoid 20 (factory special contact 8SW68).",
	29: "Scoring contact of the left kicker (slingshot); special-switch slot for solenoid 21 (factory special contact 8SW69).",
	30: "Scoring contact of the right kicker (slingshot); special-switch slot for solenoid 22 (factory special contact 8SW70).",
	33: "Score doubled and tripled in 2- and 3-ball Multi-Ball (chart footnote).",
	36: "Playfield tilt contact; the third closure tilts (booklet Tilt paragraph). The Switch Test's 'rectangle' example names it.",
	37: "The chart calls 37-40 standups scoring 10. The retained table and both corpus scripts model them as rubber hit contacts; no assembly drawing was read.",
	38: "The chart calls it `LOWER STANDUP`; the retained table's contact strip for 38 is on the left side beside the upper half of the playfield, where Figure 3 also prints 38 (its leader was not measured).",
	41: "Closed while the target is down (Switch Test item 5). Solenoid 1 raises this target; bank release 9 drops the bank.",
	42: "Closed while the target is down. Solenoid 2 raises this target; bank release 9 drops the bank.",
	43: "Closed while the target is down. Solenoid 3 raises this target; bank release 9 drops the bank.",
	44: "Closed while the target is down; the Switch Test calls it the top \"A\" target. Solenoid 4 raises this target; bank release 10 drops the bank.",
	45: "Closed while the target is down. Solenoid 5 raises this target; bank release 10 drops the bank.",
	46: "Closed while the target is down. Solenoid 6 raises this target; bank release 10 drops the bank.",
	47: "Closed while the target is down. Solenoid 7 raises this target; bank release 10 drops the bank.",
	48: "Closed while the target is down. Solenoid 8 raises this target; bank release 10 drops the bank.",
}


def inputs() -> list[dict[str, Any]]:
	devices = []
	services = {
		-7: ("switch.advance", "Advance", "button", "cabinet (coin-door service switch 7SW75)",
			"Cabinet sheet 7SW75 ADVANCE on CPU connector 1J4-3 (GRN, 7P1-5). Steps the diagnostic tests and adjustments together with Auto-Up/Manual-Down; the harness pressed it to walk Test 02 and Test 03."),
		-6: ("switch.auto-up-manual-down", "Auto-Up / Manual-Down", "other", "cabinet (coin-door service switch 7SW74)",
			"Cabinet sheet 7SW74, positions AUTO-UP and MANUAL-DOWN, on CPU connector 1J4-4 (BLU, 7P1-6). PinMAME's Auto/Manual input is a toggle that reads 1 for Auto-Up; a two-position switch has no rest state, and normally_closed follows that public convention."),
		-5: ("switch.cpu-diagnostic", "CPU Diagnostic", "button", "backbox CPU board",
			"The CPU board's DIAGNOSTIC pushbutton (booklet CPU Board Self-Test; the assembly view draws it beside IC24, and its TP2 inset shows the NMI line low while it is depressed). s7.c asserts the CPU's NMI while this input is 1."),
		-4: ("switch.sound-diagnostic", "Sound Diagnostic", "button", "backbox sound board",
			"Sound board SW1, MOMENTARY SWITCH SPDT (bill of material item 46); pressing it starts the booklet's Sound Board Self-Test, a sequence of sounds that repeats until the game is turned off and on again. s7.c passes the input to the S67S sound board, which asserts the sound CPU's NMI while it is 1. Which throw of the SPDT part the board uses was not read; the press-to-activate contact is recorded."),
	}
	for address, (identifier, label, switch_type, location, notes) in services.items():
		d = base(identifier, label, "switch", "pinmame.input.switch", address, CORE, MANUAL, DRAWINGS)
		d["normally_closed"] = False
		d.update(roles=["service"], spatial=na("cabinet_or_service", CORE, DRAWINGS),
			physical={"location": location, "switch_type": switch_type, "notes": notes})
		if address in {-7, -6}:
			d["provenance"] = provenance(CORE, MANUAL, DRAWINGS, RUN)
		devices.append(d)
	enter = base("virtual.master-command-enter", "Master Command Enter", "virtual", "pinmame.input.switch", -3, CORE, DRAWINGS, availability="optional")
	enter.update(spatial=na("virtual", CORE, DRAWINGS), physical={"location": "emulator configuration only", "notes": (
		"s7.c's s7_dips_r returns the F and D DIP nibbles only while this input is held. No Master Command Enter control appears in the cabinet wiring or "
		"the CPU board assembly view; the CPU bill of material counts two momentary switches against a note that was not read, and only the DIAGNOSTIC "
		"pushbutton is drawn. The booklet's adjustment procedures use Advance and Auto-Up/Manual-Down only. Optional emulator input; nothing in play needs it.")})
	devices.append(enter)
	for address in range(1, 65):
		used = address <= 48
		label = SWITCH_LABELS[address - 1] if used else f"Not Used matrix switch {address}"
		d = base(switch_id(address), label, "switch", "pinmame.input.switch", address, MANUAL, DRAWINGS, CORE, RUN, availability="used" if used else "unused")
		d["wiring"] = matrix_wiring(address)
		d["aliases"].append({"namespace": "manual.address", "value": str(address)})
		if not used:
			d["spatial"] = na("unused", MANUAL, DRAWINGS)
			d["physical"] = {"notes": "Figure 5 prints NOT USED and the wiring sheet's location row reads NOT USED; columns 7 and 8 run to playfield pins 8J1-6 and 8J1-7, both printed NC. Test 03 shows nothing for a held 49-64, which agrees but is not itself the basis of this disposition."}
		elif address in {34, 35}:
			side, button = ("left", 84) if address == 34 else ("right", 82)
			d.update(kind="virtual", spatial=na("virtual", CORE, SOURCE))
			d.pop("wiring")
			d["provenance"] = provenance(MANUAL, DRAWINGS, SOURCE, CORE, RUN)
			d["physical"] = {"notes": (
				f"The factory {side} flipper lane-change contact is a PLAYFIELD matrix switch at this address (Figure 5 and the wiring sheet). In PinMAME a consumer cannot drive this address directly: "
				f"INITGAMEFULL declares FLIP_SWNO(34,35), and core_updateSw copies cabinet button {button} into {address} on every update, so a direct write is overwritten "
				f"(the Test 03 run shows a one-shot write to {address} vanish while holding {button} reports {address}). A consumer drives {button}. Both corpus scripts write {address} "
				f"from the flipper key as well; that write has no effect. Matrix wiring as printed: {matrix_wiring(address)['drive_wire']} {matrix_wiring(address)['drive_connection']}, "
				f"{matrix_wiring(address)['return_wire']} {matrix_wiring(address)['return_connection']}.")}
		else:
			cabinet = address <= 8
			d["normally_closed"] = False
			d["physical"] = {"location": "cabinet" if cabinet else "playfield", "notes": (SWITCH_NOTES.get(address, "") + " " + POLARITY).strip()}
			if address in {1, 2, 7, 36}:
				d["physical"]["switch_type"] = "tilt"
			elif address == 3:
				d["physical"]["switch_type"] = "button"
			if cabinet:
				d.update(roles=["cabinet"], spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
		devices.append(d)
	for address in range(81, 89):
		used = address in {82, 84}
		side = "right" if address == 82 else "left"
		label = f"{side.title()} Flipper Button" if used else f"Unused flipper-column position {address}"
		d = base(f"switch.{side}-flipper-button" if used else f"virtual.flipper-column-{address}", label, "virtual", "pinmame.input.switch", address,
			CORE, SOURCE, *( [RUN, DRAWINGS] if used else []), availability="used" if used else "unused")
		d.update(spatial=na("virtual", CORE), physical={"notes": (
			f"PinMAME's cabinet {side} flipper button. The physical button is cabinet switch {'7SW72' if address == 82 else '7SW73'} wired through contacts of relay Z1 to the "
			f"{side} flipper coil, not into the switch matrix. PinMAME copies it into lane-change switch {35 if address == 82 else 34} on every update and, while game-on 25 is "
			f"set, fabricates outputs {'45/46' if address == 82 else '47/48'} from it."
			if used else "Generic flipper-column bit outside barra_l1's FLIP_SWNO(34,35) pair: core_updateSw copies only the two declared buttons into the matrix, so the ROM never reads this position.")})
		devices.append(d)
	for address in [1, 2]:
		d = base(f"dip.sound-dip-{address}", f"Sound Dip {address}", "dip_switch", "pinmame.input.dip", address, CORE, DRAWINGS)
		d.update(spatial=na("dip_switch", CORE, DRAWINGS), physical={"location": "backbox sound board", "switch_type": "dip", "notes": (
			f"Position {address} of the sound board's DS1, a 2-position DIP switch (bill of material item 47). PinMAME's s67s_cmd_w folds the two bits into the command the sound "
			f"CPU reads; its default is Sound Dip 1 = 0 and Sound Dip 2 = 1. The retained pages do not give Barracora's setting: the sound board drawing is the generic System 6/7 "
			"sheet, and the drawing set foreword lists only jumpers.")})
		devices.append(d)
	for address in range(9, 25):
		bank, position = ("F", address - 8) if address <= 16 else ("D", address - 16)
		label = f"Master Command {bank}{position}"
		d = base(f"virtual.{slug(label)}", label, "virtual", "pinmame.input.dip", address, CORE, DRAWINGS, availability="optional")
		d.update(spatial=na("dip_switch", CORE, DRAWINGS), physical={"location": "emulator configuration only", "notes": (
			"s7.c's s7_dips_r returns the inverted F (public 9-16) and D (public 17-24) nibbles only while Master Command Enter (-3) is held. The CPU bill of material lists "
			"DS1,DS2 8 STD DIP SWITCHES, quantity 2, but the assembly view of the same drawing shows no DS1 or DS2 and no DIP-switch bank, and the booklet never uses CPU DIP "
			"switches. Whether any production board carried them is not settled here; they are optional emulator configuration either way.")})
		devices.append(d)
	return devices


LAMP_NOTES = {
	1: "Insert board 9P1-5 (RED-BRN, diode 9D1): 9B1 is drawn as two bulbs in parallel, labelled SHOOT AGAIN.",
	2: "Insert board 9P1-6 (RED-BLK, diode 9D2), bulb 9B2 BALL IN PLAY.",
	3: "Insert board 9P1-7 (RED-ORN, diode 9D3), bulb 9B3 TILT.",
	4: "Insert board 9P1-8 (RED-YEL, diode 9D4), bulb 9B4 GAME OVER.",
	5: "Insert board 9P1-9 (printed REN-GRN; the lamp matrix and the playfield lamp sheet give row 5 as RED-GRN), diode 9D5, bulb 9B5 MATCH.",
	6: "Insert board 9P1-10 (RED-BLU, diode 9D6), bulb 9B6 HIGH SCORE.",
	7: "The playfield lamp sheet prints the column-1 asterisk beside cell 07 too, but the cell reads PLAYFIELD and the insert board carries only rows 1-6.",
	57: "The lamp sheet's bulb list skips 57 (it runs 56 Bonus 3, 58 Bonus 5); its matrix draws cell 57 PLAYFIELD and Figure 1 prints BONUS 4 there.",
}


def outputs() -> list[dict[str, Any]]:
	devices = []
	for address in range(1, 97):
		used = address <= 64
		label = LAMP_LABELS[address - 1] if used else f"Not Used lamp {address}"
		d = base(lamp_id(address), label, "lamp", "pinmame.output.lamp", address, *((MANUAL, DRAWINGS, CORE, RUN) if used else (SOURCE, CORE)), availability="used" if used else "unused")
		if not used:
			d["spatial"] = na("unused", SOURCE, CORE)
			d["physical"] = {"notes": "Auxiliary lamp columns beyond the 8x8 matrix: barra_l1's game data leaves the extra lamp-column count at 0, so PinMAME publishes nothing here."}
			devices.append(d)
			continue
		d["wiring"] = matrix_wiring(address, True)
		d["aliases"].append({"namespace": "manual.address", "value": str(address)})
		if address <= 6:
			d.update(roles=["backbox"], spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
			d["physical"] = {"location": "backbox insert board", "quantity": 2 if address == 1 else 1, "notes": (
				"The playfield lamp sheet marks cells 01-06 BACKBOX and refers to the insert board sheet, which wires column 1 rows 1-6 to these bulbs. " + LAMP_NOTES[address])}
		else:
			d["physical"] = {"location": "playfield", "notes": (
				"The playfield lamp sheet marks this cell PLAYFIELD and its TYPICAL inset draws one bulb and diode per cell; how many sockets each insert carries is not drawn. "
				+ LAMP_NOTES.get(address, "")).strip()}
			if 17 <= address <= 22:
				d["physical"]["notes"] += (" Top-lane lamps: a top rollover lights 1, 2 or 3, or 4, 5 or 6 beneath an already lit one; the lane-change buttons rotate them "
					"(see the knowledge note for the rotation the ROM performs).")
		devices.append(d)
	for address in [*range(1, 26), *range(45, 49), *range(51, 61)]:
		if address in SOLENOIDS:
			label, kind, wire, connection, transistor, part = SOLENOIDS[address]
			d = base(solenoid_id(address), label, kind, "pinmame.output.solenoid", address, MANUAL, DRAWINGS, SOURCE, RUN)
			d["wiring"] = {"board": "Williams System 7 driver board", "drive_wire": wire, "drive_connection": connection, "driver_transistor": transistor}
			notes = "Table 4 wiring and part number as printed; the Test 02 run pulses this public address at step " + f"{address:02d}."
			d["physical"] = {"part_number": part, "location": "cabinet" if address in CABINET_SOLENOIDS else "playfield"}
			if address in CABINET_SOLENOIDS:
				d.update(roles=["cabinet"], spatial=na("cabinet_or_service", MANUAL, DRAWINGS))
			if address <= 8:
				notes += f" Raises drop target {40 + address} (VR Room script SolCallback({address}) raises {40 + address}); the gameplay run raises a completed bank one target at a time in descending order."
				d["provenance"] = provenance(MANUAL, DRAWINGS, PARTS, SCRIPT, RUN)
			if address in {9, 10}:
				notes += (f" Drops the whole {'B-A-RR' if address == 9 else 'A-C-O-R-A'} bank (VR Room script); Start fires 9 and 10 and then 1-8. "
					"The parts supplement's 3-bank parts list carries both SA6-24-750-DC and the per-target SA5-24-750-DC coils.")
				d["provenance"] = provenance(MANUAL, DRAWINGS, PARTS, SCRIPT, RUN)
			if address == 1:
				notes += " Table 4 also prints a first row `01 Top Eject Hole ... SG-23-850-DC` with solenoid 01's wire, pins and transistor; Figure 2, the wiring sheet and the Test 02 run give 01 only as the B Drop Target Reset, and 13 is the eject hole kicker. Retained literally in the excerpt."
			if address == 3:
				notes += " Table 4 prints only 2P11-7; the drawing set's solenoid sheet runs SOL. 3 to 8P3-3, which is recorded here."
			if address == 11:
				notes += (" The outhole kicker: it kicks a drained ball out of the outhole (switch 12), after which the balls rest on the ball ramp switches 13-15 (booklet Game Start); "
					"the gameplay run fires it on an outhole closure, and the VR Room script binds it to its outhole kicker. The corpus scripts' `BallRelease` object is the thrower 12, not this coil.")
			if address == 12:
				notes += " Serves a ball from the ball ramp's thrower end (switch 15) into the shooter lane (switch 16); Start fires it, and so does a ball locked in a lit eject hole."
			if address == 13:
				notes += " The drawing set's solenoid sheet labels coil 8L13 TOP LEFT CORNER EJECT HOLE."
			if address == 14:
				notes += (" The drawing set's solenoid sheet labels coil 8L14 UPPER LEFT EJECT HOLE. Its cabinet sheet also draws a SOL. 14 branch to 7P1-3, printed NC on the "
					"cabinet side; the playfield sheet and Table 4 run 14 to 8P3-14.")
			if address == 15:
				notes += " Cabinet sheet 7L15 BELL with diode 7D15 and a series contact shunted by 7C1 0.1 uF. The gameplay run rings it three times for one coin."
			if address == 16:
				notes += (" The cabinet sheet draws one coil, 7L16 COIN LOCKOUT. Energized in Game Over and play so coins are accepted; it de-energizes, rejecting coins, when the "
					"maximum credits are reached (booklet Credit Posting). The Test 02 run pulses it from that energized rest and leaves it off.")
				d["physical"]["quantity"] = 1
			if address == 17:
				notes += (" Ball Gate Lock Assembly (parts supplement: armature A-8874, coil SM-35-4000-DC, return spring 10-96). The solenoid sheet labels coil 8L17 TOP EJECT HOLE GATE; "
					"its special-switch wire ORN-BRN ends at 8P3-24 printed NC, so 17 has no special switch. The gameplay run holds it on during play and drops it while a ball is "
					"locked in the upper eject hole; the VR Room script opens the table's gate while 17 is on. Which way the physical gate moves is not drawn in the retained pages.")
				d["provenance"] = provenance(MANUAL, DRAWINGS, PARTS, SOURCE, SCRIPT, RUN)
			if address in SPECIAL_SWITCHES:
				wire, pins, contact = SPECIAL_WIRING[address]
				notes += (f" Special solenoid: its direct-drive special switch {contact} is wired {wire} {pins} (Table 4 note 1). In PinMAME the scoring matrix switch "
					f"{SPECIAL_SWITCHES[address]} supplies this slot, and the gameplay run fires {address} within 20 ms of a closure of {SPECIAL_SWITCHES[address]}.")
			d["physical"]["notes"] = notes
		elif address == 25:
			d = base(solenoid_id(address), "Game On / Flipper Relay", "relay", "pinmame.output.solenoid", address, CORE, MANUAL, DRAWINGS, RUN)
			d.update(roles=["internal"], spatial=na("internal_nonvisual", CORE, MANUAL), physical={"location": "driver board in backbox", "notes": (
				"S7_GAMEONSOL: PinMAME publishes the PIA game-on line at 25. It drives the driver board's flipper relay Z1, whose contacts carry the flipper button returns "
				"(2P12-1 ORN-VIO, 2P12-2 ORN-GRY), and enables the special solenoids. Table 4 has no row for it. The booklet's Solenoid Test says the flipper relay is de-energized "
				"with subtest 25, and the Test 02 run pulses 25 off from its energized rest; the ball roll tilt drops it. It is not the power board's K1, whose coil pins this game leaves N.C.")})
		elif 45 <= address <= 48:
			side = "right" if address <= 46 else "left"
			winding = "power" if address % 2 else "hold"
			d = base(solenoid_id(address), f"Synthetic {side} flipper {winding} state", "virtual", "pinmame.output.solenoid", address, CORE, SOURCE, RUN)
			d.update(spatial=na("virtual", CORE), physical={"notes": (
				f"Fabricated by PinMAME from button {82 if side == 'right' else 84} while game-on 25 is set; the pair {'45/46' if side == 'right' else '47/48'} asserts together and models no "
				f"winding or end-of-stroke switch. The physical {side} flipper is one SFL-19-400/30-750-DC coil (Table 4: {'BLU-VIO 7P1-8, 8P3-34' if side == 'right' else 'BLU-GRY 7P1-10, 8P3-32'}) "
				f"switched by the cabinet button through Z1, with its own flipper contact {'8SW46' if side == 'right' else '8SW45'} on the playfield; the CPU does not drive it.")})
		else:
			slot = address in {23, 24}
			d = base(solenoid_id(address), f"Unfitted special slot {address}" if slot else f"Unavailable solenoid {address}", "virtual", "pinmame.output.solenoid",
				address, *( (SOURCE, CORE, MANUAL, DRAWINGS, RUN) if slot else (SOURCE, CORE)), availability="unused")
			d["spatial"] = na("unused", *((CORE, MANUAL, DRAWINGS) if slot else (SOURCE, CORE)))
			d["physical"] = {"notes": (
				"setSSSol publishes special slots 23 and 24, but Table 4 has no row for them and the solenoid sheet draws special drivers only for 17-22; the booklet's Solenoid Test "
				"pulses 01-24 and the Test 02 run sees 23 and 24 pulse there, while the gameplay run never sets them. That sweep explains the published state; no load is fitted."
				if slot else "Custom solenoids 51-60 need a game callback; barra_l1 declares none, so PinMAME publishes nothing here.")}
		devices.append(d)
	return devices


def mechanisms() -> list[dict[str, Any]]:
	s, c = switch_id, solenoid_id
	refs = (MANUAL, DRAWINGS, SOURCE, CORE, RUN)
	specs = [
		("ball-ramp-and-outhole", "Outhole, ball ramp and thrower", "kicker", [c(11), c(12)], [s(n) for n in (12, 13, 14, 15, 16)],
			"Three balls rest on the ball ramp positions 13, 14 and 15 (15 at the thrower end) or, at most one, in the shooter lane on 16; a game starts only then. "
			"Start fires the ball ramp thrower 12, which serves the ball at 15 into the shooter lane, and the remaining balls roll down the ramp. The player plunges by hand. "
			"A drained ball rests on outhole switch 12 and ball release 11 kicks it onto the ball ramp. The gameplay run observes 12 on Start and on each lock, and 11 on an outhole closure; "
			"the host moved every ball, so ramp travel times are not measured.", refs + (SCRIPT,)),
		("b-a-rr-drop-target-bank", "B-A-RR 3-bank drop targets", "drop_target_bank", [c(n) for n in (1, 2, 3, 9)], [s(n) for n in (41, 42, 43)],
			"Three drop targets (the parts supplement's 3-bank, first used in Barracora). Each target switch is closed while its target is down. Bank release 9 drops the whole bank; "
			"reset coils 1, 2 and 3 raise one target each. Start fires 9 and then 1-3 (with 10 and 4-8). Making B, A, RR in sequence spots BARRACORA lamps; the gameplay run raises a "
			"target knocked down out of sequence at once (3 alone for RR) and, on completing the bank in sequence, raises 3, 2, 1 one at a time with no bank release. "
			"Completing it advances the bonus multiplier and lights the lower eject hole lock arrow. Drop targets are remembered per player.", refs + (PARTS, SCRIPT)),
		("a-c-o-r-a-drop-target-bank", "A-C-O-R-A 5-bank drop targets", "drop_target_bank", [c(n) for n in (4, 5, 6, 7, 8, 10)], [s(n) for n in (44, 45, 46, 47, 48)],
			"Five drop targets, 44 at the top to 48 at the bottom. Bank release 10 drops the bank; reset coils 4-8 raise one target each. Completing the bank in sequence raises "
			"8, 7, 6, 5, 4 one at a time in the gameplay run, advances the bonus multiplier and lights the upper eject hole lock arrow; completing both banks advances the super bonus multiplier.",
			refs + (SCRIPT,)),
		("upper-eject-hole", "Upper eject hole", "kicker", [c(13)], [s(10)],
			"Kick-out hole at the top left. Ball-presence switch 10 is closed while a ball rests in it; kicker 13 ejects it. With its lock arrow lit, a ball entering locks: "
			"the gameplay run serves a new ball with thrower 12 0.18 s after 10 closes. 5.14 s after the plunge that follows the second lock, the gate 17 energizes and 13 kicks "
			"the locked ball out. With lamps 1-6 complete it also collects the bonus.", refs + (SCRIPT,)),
		("upper-eject-hole-gate", "Upper eject hole gate", "gate", [c(17)], [s(10)],
			"Ball Gate Lock Assembly (coil, armature and return spring) at the mouth of the upper eject hole. The gameplay run energizes 17 5.13 s after the shooter switch 16 opens "
			"and keeps it on in play, drops it 0.03 s after the thrower serves the next ball for an upper-hole lock, and energizes it again just before 13 releases the locked ball. "
			"The VR Room script opens the table's gate while 17 is on and closes it when 17 drops. The retained pages do not draw the gate's swing, so whether energized means open "
			"on the machine is the script's reading, not a drawn fact.", refs + (PARTS, SCRIPT)),
		("lower-eject-hole", "Lower eject hole", "kicker", [c(14)], [s(11)],
			"Kick-out hole on the left below the upper hole. Ball-presence switch 11 is closed while a ball rests in it; kicker 14 ejects it. With its lock arrow lit, a ball entering "
			"starts 2-ball Multi-Ball, or 3-ball when a ball is already locked above: the gameplay run serves a new ball with 12 3.09 s after 11 closes, and kicks 14 when the upper "
			"hole's switch 10 opens during the 3-ball release. A ball locked first here gives only 2-ball play.", refs + (SCRIPT,)),
		("top-lanes", "Top lanes and Lane Change", "other", [], [s(n) for n in (17, 18, 19, 34, 35)],
			"Three top rollover lanes 17, 18 and 19 light lamps 1, 2 and 3, or 4, 5 and 6 beneath an already lit one. The flipper buttons rotate the lit lamps (Lane Change): "
			"PinMAME copies the right button into 35 and the left into 34. Lamps 1-3 advance the lower eject hole values, lamps 4-6 the upper right bull's-eye values, and all six "
			"light the upper eject hole bonus collect. The gameplay run lit lamp 17 from lane 17 and the right button moved it to 18.", refs),
	]
	for address, sensor in SPECIAL_SWITCHES.items():
		label = SOLENOIDS[address][0]
		specs.append((slug(label), label, "kicker" if address >= 21 else "other", [c(address)], [s(sensor)],
			f"{label}: scoring matrix switch {sensor} and a separate direct-drive special switch on the same assembly fire special solenoid {address} through the special driver "
			f"while game-on 25 enables it. PinMAME derives slot {address} from {sensor}; the gameplay run fires {address} within 20 ms of a closure. Power and stroke are table-owned.",
			(MANUAL, DRAWINGS, SOURCE, CORE, RUN)))
	for side, button, pair in [("right", 82, (45, 46)), ("left", 84, (47, 48))]:
		specs.append((f"{side}-flipper", f"{side.title()} flipper", "other", [c(n) for n in pair], [f"switch.{side}-flipper-button"],
			f"One {side} flipper with a dual-wound SFL-19-400/30-750-DC coil and its own flipper contact, switched by the cabinet button through relay Z1 while game-on 25 holds it. "
			f"A consumer drives button {button}; PinMAME fabricates {pair[0]}/{pair[1]} together and copies the button into lane-change switch {35 if side == 'right' else 34}. "
			"Travel, end-of-stroke behavior and tuning belong to the table.", (MANUAL, DRAWINGS, SOURCE, CORE, RUN)))
	return [{"id": f"mech.{key}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs_)}
		for key, label, kind, actuators, sensors, behavior, refs_ in specs]


def excerpt(name: str) -> dict[str, Any]:
	script = name in {"script-bindings.md", "spatial-method.md", "identity.md"}
	return {"id": f"excerpt.{slug(name.removesuffix('.md'))}", "locator": LOCATORS[name], "path": f"evidence/excerpts/{MACHINE_ID}/{name}", "sha256": EXCERPTS[name],
		"method": "manual", "transcribed_by": "curator; source text and data files read directly" if script else "curator; native page images read visually",
		"reviewed": name not in UNREVIEWED}


def document(identifier: str, names: list[str]) -> dict[str, Any]:
	filename, digest, size, pages, stamp, revision, kind = DOCUMENTS[identifier]
	return {"id": identifier, "kind": "manual", "uri": f"https://www.ipdb.org/files/177/{filename}", "sha256": digest, "revision": revision, "source_id": "ipdb:177",
		"original_filename": filename, "acquired_at": ACQUIRED, "license": "NOASSERTION", "rights": MANUAL_RIGHTS, "attribution": MANUAL_ATTRIBUTION,
		"locator": (f"Williams {kind} for game 510 from IPDB machine https://www.ipdb.org/machine.cgi?id=177, downloaded from {WAYBACK.format(stamp=stamp, name=filename)} because IPDB "
			f"is Cloudflare-gated; retained unchanged at external:pinmame-manuals/{(MANUAL_DIRECTORY / filename).as_posix()}; {pages} PDF pages, {size} bytes, scanned images read visually."),
		"excerpts": [excerpt(n) for n in names]}


def sources(root: Path) -> list[dict[str, Any]]:
	common = {"license": "BSD-3-Clause", "attribution": "PinMAME contributors", "revision": REVISION, "acquired_at": REVISION_COMMITTED}
	table = spatial.read_seed(root)["table"]
	records = [
		document(MANUAL, ["lamp-matrix.md", "switch-matrix.md", "solenoid-connections.md", "game-operation.md", "diagnostics.md"]),
		document(DRAWINGS, ["lamp-wiring.md", "insert-board.md", "cabinet-and-power.md", "board-switches.md", "switch-matrix.md", "solenoid-connections.md", "game-operation.md"]),
		document(PARTS, ["parts-supplement.md"]),
		{"id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=177", "sha256": IPDB_PAGE[1], "source_id": "ipdb:177", "acquired_at": ACQUIRED,
			"locator": (f"IPDB machine 177 page as captured by the Wayback Machine (archived 2025-11-24), retained at external:pinmame-manuals/{(MANUAL_DIRECTORY / IPDB_PAGE[0]).as_posix()}, "
				f"{IPDB_PAGE[2]} bytes: Barracora, Williams, September 1981, model 510, System 7, 2,350 units. Its file links supplied the three retained documents."),
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database; capture by the Internet Archive's Wayback Machine", "excerpts": [excerpt("identity.md")]},
		{"id": OPDB, "kind": "human_review", "uri": "https://mp-data.sfo3.cdn.digitaloceanspaces.com/latest-opdb.json", "sha256": OPDB_SHA, "acquired_at": "2026-08-14T17:53:43Z",
			"locator": "Retained external:pinmame-review-artifacts/opdb-import/latest-opdb.json; group GRo7K and machine GRo7K-MQ4e3, Barracora, Williams, IPDB 177, manufactureDate 1981-01-09.",
			"license": "NOASSERTION", "attribution": "Open Pinball Database contributors", "excerpts": [excerpt("identity.md")]},
		{"id": SOURCE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/s7games.c", "sha256": SOURCE_FILES["src/wpc/s7games.c"],
			"locator": "INITGAMEFULL macro; the barra block: INITGAMEFULL(barra,s7_dispS7,34,35,0, 0,20,21,22,29,30), S7_ROMSTART8088 members and CORE_GAMEDEF(barra,l1,\"Barracora (L-1)\",1981,\"Williams\",s7_mS7S,0); s7_dispS7.", **common},
		{"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/s7.c", "sha256": SOURCE_FILES["src/wpc/s7.c"],
			"locator": "s7_vblank (CPU and sound diagnostic inputs), setSSSol, the switch-column read, s7_dips_r and MACHINE_DRIVER_START(s7). Also core.c core_updateSw and the flipper column, core.h FLIP_SWNO, s7.h S7_COMPORTS and S7_GAMEONSOL, and wmssnd.c s67s_cmd_w and s67s_diag at the same revision.", **common},
	]
	for filename in ["src/wpc/core.c", "src/wpc/core.h", "src/wpc/s7.h", "src/wpc/wmssnd.c"]:
		records.append({"id": "pinmame.dependency." + slug(filename), "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/{filename}",
			"sha256": SOURCE_FILES[filename], "revision": REVISION, "acquired_at": REVISION_COMMITTED, "locator": "Source read-path, flipper and sound dependency cited by pinmame.system-7-current. LICENSE SHA-256 " + SOURCE_FILES["LICENSE"],
			"license": "BSD-3-Clause" if filename.endswith("s7.h") else "LicenseRef-PinMAME-Old-MAME", "attribution": "PinMAME contributors",
			"rights": "Pinned repository LICENSE distinguishes explicitly marked BSD files from inherited old-MAME files; no blanket BSD assertion for unmarked core/sound dependencies."})
	vr_name, vr_digest = SCRIPT_FILES[SCRIPT]
	old_name, old_digest = SCRIPT_FILES[OLD_SCRIPT]
	records += [
		{"id": SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/{quote(vr_name, safe='/')}", "revision": SCRIPT_REVISION, "sha256": vr_digest,
			"acquired_at": SCRIPT_REVISION_COMMITTED,
			"locator": (f"{vr_name} in the pinned known-working script corpus, 4478 lines, header 'Version 2.0 by UnclePaulie 2022'; cGameName barra_l1, S7.VBS. Runtime authority for the "
				"solenoid callbacks (1-8 raise targets 41-48, 9 and 10 drop the banks, 11 outhole, 12 the thrower's kicker, 13 and 14 the eject holes, 15 bell, 17 the gate both ways), "
				"the ball-ramp objects on 13-15 and the switch handlers. Its writes to 34 and 35 are overwritten by PinMAME's flipper copy; it binds no callback to 16 or 18-22."),
			"license": "NOASSERTION", "attribution": "UnclePaulie (version 2.0), redbone (2.1 playfield and plastics) and earlier authors credited in the script", "known_working": True,
			"excerpts": [excerpt("script-bindings.md")]},
		{"id": OLD_SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/{quote(old_name, safe='/')}", "revision": SCRIPT_REVISION, "sha256": old_digest,
			"acquired_at": SCRIPT_REVISION_COMMITTED,
			"locator": (f"{old_name} in the same corpus, header 'Barracora - Williams 1981 by Dids666', 'Ver 1.1', 'Thalamus 2018-07-19'; the lineage of the retained table's embedded script. "
				"A lead only: its gate handler opens Gate1 on every call and never closes it, and it defines Sub sw18_Hit three times and Sub sw16_Hit twice."),
			"license": "NOASSERTION", "attribution": "Dids666, Thalamus and earlier authors credited in the script", "known_working": False, "excerpts": [excerpt("script-bindings.md")]},
		{"id": TABLE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{table['path']}/{table['filename']}", "original_filename": table["filename"], "sha256": table["sha256"],
			"acquired_at": table["acquired_at"],
			"locator": (f"Community table by {table['author']} (embedded info: January 2018, VPX 10.5) from the operator's read-only table archive, {table['size']} bytes; no download URL is asserted "
				f"and it is not known to have been played. {table['extractor']} extraction {table['extraction']}: {table['file_count']} files, {table['byte_count']} bytes, manifest SHA-256 "
				f"{table['manifest_sha256']} (tools/build_external_evidence_manifest.py). Bounds left 0, top 0, right 952, bottom 1974. The geometry source of every observed placement."),
			"license": "NOASSERTION", "attribution": "Dids666; redistribution rights not granted", "rights": "NOASSERTION", "excerpts": [excerpt("spatial-method.md")]},
		{"id": EMBEDDED, "kind": "vpx_script", "uri": f"external:pinmame-vpx-sources/{table['path']}/{table['extraction']}/script.vbs", "original_filename": "script.vbs", "sha256": table["script_sha256"],
			"acquired_at": EXTRACTED,
			"locator": ("The retained table's embedded script (Dids666 v1.1, ASCII, CRLF). It has the mod v1.3 bindings at nearby lines: vpmMapLights AllLights, the bsTrough ball stack on 15, 14, 13, "
				"both eject saucers, both drop banks and the gate handler that cannot close the gate. It names each placed object."),
			"license": "NOASSERTION", "attribution": "Dids666 and Thalamus", "known_working": False, "excerpts": [excerpt("script-bindings.md"), excerpt("spatial-method.md")]},
	]
	runtime = load_json(root / RUNTIME)
	records.append({"id": RUN, "kind": "runtime_scenario", "uri": "repo:" + RUNTIME.as_posix(), "sha256": sha(root / RUNTIME), "revision": REVISION,
		"locator": ("Compact evidence derived by tools/barracora_runtime_evidence.py from four retained barra_l1 runs (init, Test 02, Test 03, gameplay) on the 46e1a01a LibPinMAME build; "
			"raw traces under external:pinmame-review-artifacts/" + HARNESS.as_posix() + ", pinned by manifest SHA-256 " + HARNESS_MANIFEST_SHA + ". Every cited display frame is pinned in "
			+ READINGS.as_posix() + ". " + runtime["recreation_notes"][0]["text"]),
		"acquired_at": "2026-10-31T07:14:30Z", "license": "NOASSERTION", "attribution": "pinmame-game-defs curator; acquired_at is final raw trace persistence time"})
	return records


def build(root: Path = ROOT) -> dict[str, Any]:
	displays = []
	layouts = [("player-1", "Player 1 score", 2, 1, 7), ("player-2", "Player 2 score", 3, 9, 7), ("player-3", "Player 3 score", 0, 21, 7), ("player-4", "Player 4 score", 1, 29, 7),
		("ball-tens", "Ball in Play / Match tens", 4, 0, 1), ("ball-units", "Ball in Play / Match units", 5, 8, 1),
		("credit-tens", "Credits tens", 6, 20, 1), ("credit-units", "Credits units", 7, 28, 1)]
	for key, label, index, start, width in layouts:
		displays.append({"id": f"display.{key}", "label": label, "kind": "segment", "controller_index": index, "segment_start": start, "width": width,
			"physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", DRAWINGS, SOURCE), "provenance": provenance(SOURCE, DRAWINGS, MANUAL, RUN)})
	relationships = [{"id": f"relationship.special-{sensor}-{address}", "kind": "direct", "source": switch_id(sensor), "destination": solenoid_id(address),
		"provenance": provenance(CORE, SOURCE, MANUAL, RUN)} for address, sensor in SPECIAL_SWITCHES.items()]
	for side, button, copy in [("right", 82, 35), ("left", 84, 34)]:
		relationships.append({"id": f"relationship.{side}-button-lane-change", "kind": "direct", "source": f"switch.{side}-flipper-button",
			"destination": switch_id(copy), "provenance": provenance(CORE, SOURCE, RUN)})
	definition = {"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Barracora", "manufacturer": "Williams", "year": 1981, "model_number": "510", "kind": "physical_pinball", "ipdb_id": 177, "opdb_id": "GRo7K-MQ4e3"},
		"controller": {"platform": "pinmame.system-7", "hardware_generation": "0x10000", "inversion_applied_by_emulator": True},
		"drivers": [{"id": GAME, "description": "Barracora (L-1)", "manufacturer": "Williams", "year": "1981", "flags": 0, "physical_compatibility": "identical",
			"variant_notes": ("The only PinMAME driver for game 510; its five ROM members match the pinned s7games.c SHA-1 values and the parts supplement's ROM summary (Sound ROM 4). "
				"Source comments name a tournament ROM mod and a 2x/3x playfield multiplier mod; neither is a driver and neither is covered here.")}],
		"inputs": inputs(), "outputs": outputs(), "displays": displays, "mechanisms": mechanisms(), "relationships": relationships,
		"coverage": {"status": "partial", "missing": MISSING, "dimensions": {
			"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
			"mechanisms": "observed", "variant_coverage": "validated", "recreation_knowledge": "observed", "spatial_placement": "observed"}},
		"conflicts": [], "sources": sources(root), "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "partial"}}
	return spatial.apply(definition, root)


KNOWLEDGE_TEXT = """# Barracora (Williams, 1981)

Coverage remains **partial**: every requirement except spatial placement is met. Addresses,
names, wiring, polarity, displays and mechanisms come from the instruction booklet, the drawing
set and the parts supplement, the pinned PinMAME source, four retained runs of the `barra_l1` ROM
and the pinned VR Room script. Placements are `observed` readings of one community table, and no
lamp has a placement.

## Identity

Williams game 510, IPDB 177, OPDB `GRo7K-MQ4e3`, System 7. IPDB gives September 1981 and 2,350
units; OPDB's `manufactureDate` 1981-01-09 agrees on the year only. OPDB's `display:
alphanumeric` is wrong for this machine: the insert board sheet draws seven-digit numeric player
displays and a credits / ball-in-play board. The instruction booklet is 16P-510-103 and the parts
supplement 16P-510-110 (October 1981). IPDB's notes record that the game was renamed from
'Las Vegas' to 'Jet Orbit' to 'Barracora', which they give as the reason two letters share one
insert (the RR lamp, public 11).

`barra_l1` is the only driver. Its ROM members match pinned `s7games.c`, and the parts supplement
lists Sound ROM 4, which matches `sound4.716`. The source comments mention a tournament ROM mod and
a 2x/3x playfield multiplier mod; neither is a driver and neither is covered.

## Controller and address dispositions

System 7 (`0x10000`), `s7_dispS7`. Switches and lamps number `(column - 1) * 8 + row`, which the
lamp sheet's numbers 01-64 and the switch matrix's printed numbers follow.

- Service inputs: -7 Advance (7SW75) and -6 Auto-Up / Manual-Down (7SW74) on CPU connector 1J4;
  -5 the CPU board's DIAGNOSTIC pushbutton (NMI); -4 the sound board's SW1. -3 Master Command
  Enter is optional emulator input: no such control is drawn in the cabinet wiring or the CPU
  board assembly view.
- Matrix switches 1-48 are fitted (1-8 in the cabinet, 9-48 on the playfield); 49-64 are printed
  NOT USED and columns 7 and 8 end at playfield pins printed NC.
- 34 and 35 are the playfield lane-change contacts on the real machine, but PinMAME copies the left
  (84) and right (82) cabinet flipper buttons into them on every update (`FLIP_SWNO(34,35)`), so a
  consumer drives 84 and 82. 81, 83 and 85-88 are unused.
- DIP 1 and 2 are positions of the sound board's 2-position DS1. DIP 9-24 are PinMAME's
  Master Command F and D bits, read only while -3 is held. The CPU bill of material lists DS1 and
  DS2 (two 8-position DIP switches), but the assembly view of the same drawing shows neither, and
  the booklet never uses them; they stay optional.
- Every matrix contact is normally open: the switch sheet's TYPICAL cell is an open contact with a
  diode, the cabinet sheet draws 7SW1-7SW8 open, the read path is not inverted and Test 03 shows
  each held public 1. A drop target switch is closed while its target is down.
- Lamps 1-64 are all fitted. 1-6 (Same Player Shoots Again, Ball in Play, Tilt, Game Over, Match,
  High Score to Date) are insert board lamps in the backbox; 1 has two bulbs in parallel. 7-64 are
  playfield inserts. 65-96 are unused auxiliary columns.
- Solenoids 1-22 are fitted as Table 4 prints them. 23 and 24 are special slots with no driver or
  load; the Solenoid Test sweeps them. 25 is game-on: it drives the flipper relay Z1 and enables
  the specials. 45-48 are PinMAME's synthetic flipper states. 51-60 are unavailable, and 26-44 and
  49-50 are transport holes with no device.
- System 7 publishes no G.I. channel, and on this game nothing on the CPU side switches the 6.3 VAC
  general illumination: the power board's K1 special relay has all its coil pins printed N.C.,
  so its contact stays as drawn, closed. The sheets draw G.I. strings on the playfield, the
  cabinet and the insert board with continuation dashes and print no bulb count.
- The coin door's 7SW76 Memory Protect Interlock (CPU connector 1J4-1) has no PinMAME input.

Four seven-digit player displays map to controller indices 2, 3, 0 and 1, and the credits and
ball-in-play digits to 6/7 and 4/5. The booklet's "Match display" is the ball-in-play display.

## Ball path and mechanisms

Three balls. A game starts only with all three on the ball ramp switches 13, 14 and 15 or, at most
one, in the shooter lane on 16. Start fires game-on 25, bank releases 9 and 10, target resets 1-8
in order and the ball ramp thrower 12, which serves the ball resting on 15 into the shooter lane.
The player plunges. A drain closes outhole 12, and ball release 11 kicks the ball onto the ball
ramp. The Williams name `Ball Release` is the outhole kicker 11; the corpus scripts call the
thrower's kicker `BallRelease`.

The B-A-RR 3-bank (41-43) and A-C-O-R-A 5-bank (44 at the top to 48) each have one reset coil
per target (1-3, 4-8, raising it) and a bank release (9, 10, dropping the bank). The ROM raises a
target hit out of sequence at once, and raises a completed bank one target at a time from the
last letter back, with no bank release. Bank completion advances the bonus multiplier and lights
an eject-hole lock arrow; both banks together advance the super bonus multiplier.

Two kick-out holes on the left: upper eject hole 10 with kicker 13 and lower eject hole 11 with
kicker 14. A ball locked in a lit hole is replaced by a new ball from the thrower (0.18 s after
10 closes, 3.09 s after 11 closes in the gameplay run). Locking upper then lower gives 3-ball
Multi-Ball, lower first only 2-ball. The upper hole's gate 17 is a Ball Gate Lock Assembly (coil,
armature and return spring). The ROM holds 17 on in play, drops it while a ball is locked in the
upper hole, and turns it back on just before 13 releases the ball; the VR Room script opens the
table's gate while 17 is on. The retained pages do not draw the gate's swing.

Three jet bumpers (18 left, 19 right, 20 bottom) and two kickers (21 left, 22 right) are special
solenoids. Each has a scoring matrix switch (20, 21, 22, 29, 30) that PinMAME uses for the slot,
and a separate direct-drive special contact (8SW66-8SW70) that is not a public input. Slot 17 is
the gate, which has no special switch (its special-switch wire ends at a pin printed NC).

Each flipper is one SFL-19-400/30-750-DC coil, switched by its cabinet button through Z1 and with
its own flipper contact (8SW45 left, 8SW46 right). PinMAME publishes 45/46 (right) and 47/48
(left) together while 25 is set; they model neither winding nor end of stroke.

The top lanes 17, 18 and 19 light lamps "1"-"3", or "4"-"6" beneath an already lit one, and the
flipper buttons rotate them. The booklet says the right button rotates 1-3 "from right to left"
and the left button 4-6 "from left to right". In the gameplay run the right button moved a lit
"1" to "2"; in the retained table lane 1 is the leftmost, which would make that move left to
right. The lanes' order is not measured on a factory drawing, so the record follows the ROM and
leaves the prose's direction as a note.

## Sources that disagree, and what the record follows

None of these is a conflict: each is a wiring detail, a misprint or a defect in a consumed table.

- Table 4's first row `01 Top Eject Hole ... SG-23-850-DC` repeats solenoid 01's wiring; Figure 2,
  the solenoid sheet and Test 02 give 01 as the B Drop Target Reset. Table 4 prints 03 without its
  8P3 pin; the solenoid sheet gives 8P3-3.
- The solenoid sheet names 13 TOP LEFT CORNER EJECT HOLE, 14 UPPER LEFT EJECT HOLE and 17 TOP EJECT
  HOLE GATE; Table 4 and Figure 2 say Upper Eject Hole, Lower Eject Hole and Upper Eject Hole Gate.
  The record uses Table 4's names.
- The cabinet sheet's SOL. 14 branch to 7P1-3 (NC) and its flipper-coil pins 8P3-3/15/4/9 do not
  match the playfield sheet and Table 4, which the record follows.
- F4 is 10A in the booklet and on the power sheet, 20A SB in the drawing set's foreword.
- The lamp sheet's bulb list skips 57; its own matrix and Figure 1 fill the cell (Bonus 4). It
  also prints the column-1 asterisk beside cell 07, which reads PLAYFIELD. The insert board prints
  row 5's wire `REN-GRN`.
- Figure 5 prints 11 as `LOWER / HOLE`. The chart calls 38 `LOWER STANDUP`, but its contact is on
  the left side beside the upper playfield in the retained table and on Figure 3.
- The Dids666-lineage scripts open the gate from 17 and never close it, define `sw18_Hit` three
  times, and both corpus scripts write the lane-change switches 34 and 35 directly; none of this
  changes the machine.

## Runtime evidence

Four runs of the authorized `barra_l1` ROM on the 46e1a01a LibPinMAME build, each in a fresh
state directory: an initialization run from empty CMOS (which stops in the Diagnostic Mode the
drawing set describes), then the Solenoid Test, the Switch Test and a scripted game seeded from
that run's NVRAM. Test 02 steps 01-25 pulse public 1-25 one at a time, which pairs every printed
solenoid number with its public address; Test 03 shows each held switch 1-48 and nothing for
49-64; the game exercises the start sequence, every special, both banks, both locks, 3-ball
Multi-Ball, the outhole and the ball roll tilt. The compact evidence lives in
`evidence/runtime/system-7/barracora-1981.json`, and every display frame it cites is pinned in
`tools/seeds/williams/barracora-1981-display-readings.json`. A run shows what a public address
does under those conditions; it does not prove bulb counts or locations.

## What would complete this record

Spatial placement is the one open requirement:

- Lamps 7-64 have no placement. The retained table draws every insert as a light with no bulb,
  which marks no socket, and no lamp-location drawing was measured. A table that models the bulbs,
  or a measured factory playfield drawing, would supply them, together with the socket count of
  each insert.
- Switches 12-15 (outhole and ball ramp) and 36-40, and solenoids 11 and 12, have no defensible
  position in the retained table; the spatial report gives the reason for each.
- Every placement is `observed` from one community table that is not known to have been played.
  Measuring the callouts of Figure 2 and Figure 3 against the table would validate them.
"""


def verify_files(root: Path = ROOT) -> None:
	spatial.read_seed(root)
	for name, digest in EXCERPTS.items():
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
		nvram = review / HARNESS / "init-state/nvram/barra_l1.nv"
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
			raise RuntimeError("ROM members differ from the pinned s7games.c declarations")
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
		print("Barracora definition, seed, knowledge, excerpts, runtime evidence and spatial blockers match.")
	elif args.write_manifests:
		write_manifests()
		print("Barracora extraction and harness manifests rewritten and match their pins.")
	else:
		regenerate()
		print("Regenerated Barracora partial artifacts.")


if __name__ == "__main__":
	main()
