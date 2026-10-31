"""Curate the physical Bally Mousin' Around! (1989) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and table
coordinate is a literal here, so regeneration reproduces the canonical definition, its pinned seed,
the knowledge note and the spatial report byte for byte without reading the external evidence roots.
``--check`` refuses drift, and ``--regenerate`` is the only path that writes them.

Mousin' Around! runs on Williams System 11B hardware (pinned PinMAME ``GEN_S11B``, the manual's
"WILLIAMS ELECTRONICS GAMES System 11B"). ``mousnGameData`` sets ``sxx.muxSol = 12``, so the eight
switched "A" loads are published at 1-8 while the A/C select relay is released and their "C"
flashers at 25-32 while it is energized; ``S11_MUXSW2`` copies the relay's state into switch 2, no
switch-driven special solenoid is declared, and ``FLIP_SWNO(58,57)`` copies the cabinet flipper
buttons into matrix switches 58 and 57. The display layout is two sixteen-character alphanumeric
rows. The game's mechanisms are two motorless ball-eating traps, a motorized center target bank, a
three-ball mouse hole lock with a drop kick on the back panel, a ball diverter, a kickback and a top
lanes gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_flipper_column import (
	VPM_CORE_SHA256,
	VPM_LIBRARY_SOURCE,
	VPM_LIBRARY_URI,
	VPM_S11_SHA256,
	flipper_column_inputs,
	flipper_column_relationships,
	vpm_staged_flipper_notes,
)


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.mousin-around.1989"
PARTIAL_PATH = ROOT / "machines/partial/bally/mousin-around-1989.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/mousin-around-1989.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/bally/mousin-around-1989.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/mousin-around-1989.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/mousin-around-1989.md"
KNOWLEDGE_PATH = "knowledge/bally/mousin-around-1989.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/mousin-around-l4-service-and-mechanisms.json"
VARIANT_GAMES = ("mousn_l1", "mousn_lu")


def variant_evidence_path(game: str) -> Path:
	return ROOT / f"evidence/runtime/system-11/mousin-around-{game.split('_', 1)[1]}-service-tests.json"


def variant_source(game: str) -> str:
	return f"runtime.mousin-around.{game.replace('_', '-')}-service-tests"


PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.bally.mousin-around.1989"
RUNTIME_SOURCE = "runtime.mousin-around.l4-service-and-mechanisms"
# When each driver's last retained raw run finished (UTC, from the retained run files).
RUN_AT = {"mousn_l4": "2026-10-31T08:56:33Z", "mousn_l1": "2026-10-31T08:50:51Z", "mousn_lu": "2026-10-31T08:50:51Z"}
VPX_TABLE_SOURCE = "vpx-table.mousin-around-herweh-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.mousin-around-herweh-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.mousin-around-herweh-1-0"
VPX_CORPUS_SOURCE = "vpx-script.ffec259adb8149d5"
VPX_STANDALONE_SOURCE = "vpx-script.c3b3d0bde70f1aa3"

VPXTABLE_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
CORPUS_NAME = "Mousin' Around! (Bally 1989) w VR Room v2.1.vbs"
CORPUS_SHA256 = "ffec259adb8149d5b4c3424770f04017905c24b069196260da60e975d42a2e72"
STANDALONE_NAME = "Mousin' Around! (Bally 1989) w VR Room v2.1/Mousin' Around! (Bally 1989) w VR Room v2.1.vbs"
STANDALONE_SHA256 = "c3b3d0bde70f1aa369cee7e6518f4808cc9c76d762177add3168f7b81ea6c7e3"
STANDALONE_LF_SHA256 = "d9a9ff5f339c7836366501167d7ff33682c2f00ebcaca05a90993ab3b88c2bb2"

# (left, right) in the driver's own FLIP_SWNO macro order.
FLIP_SWNO = (58, 57)
AC_RELAY = 12

MANUAL_SHA256 = "6dcd83d1485a1b2e9909cc65b07d9ce23e1e7757e87cdf4a002984465b02d9f0"
IPDB_PAGE_SHA256 = "7916e5326183b6b94fb37504e15d30b133060923f50524678c3122e5f498d7a3"
TABLE_SHA256 = "6c914b95a3062036b285f751b606b1468f86d93a12f86943fc29405ed2be4c9d"
SCRIPT_SHA256 = "959acd6b408903f3c71c8c0cf1fedf3345a3cc1105f0399e42824e22dd1cf282"

EXTRACTION_RELATIVE_PATH = Path("bally/mousin-around-1989/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/mousin-around-1989/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 1842
EXTRACTION_TOTAL_BYTES = 91050505
# SHA-256 of the canonical manifest bytes, so a changed extraction with a refreshed manifest is refused.
EXTRACTION_MANIFEST_SHA256 = "25887ce6b293d7d5998f87f2de2d6c1f2969cc794076523fe24009e4e98d64a3"

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"
PLAYFIELD_WIDTH = 964.0
PLAYFIELD_HEIGHT = 2162.0


def norm(x: float, y: float) -> tuple[float, float]:
	"""Normalize a retained-table coordinate (VPX units) into the canonical playfield space."""
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


DRIVER_IDS = ("mousn_l4", "mousn_l1", "mousn_lu", "mousn_l4c")
_SHARED = (
	"Shares mousnGameData/init_mousn with the parent through CORE_CLONEDEF (pinned src/wpc/s11games.c lines 1122 and "
	"1179-1183), and so the same GEN_S11B generation, disp16oneline display layout, A/C select relay 12, S11_MUXSW2 "
	"switch-2 copy and FLIP_SWNO(58,57) flipper wiring."
)
DRIVER_COMPATIBILITY = {
	"mousn_l4": (
		"identical",
		"Bally LA-4 production game ROMs (mous_u26.l4, mous_u27.l4), the pinned clone-tree parent and the driver the retained "
		"known-working table binds (cGameName = \"mousn_l4\"). The runtime evidence was recorded on it.",
	),
	"mousn_l1": (
		"compatible",
		"Bally LA-1 game ROMs (u26-la1.rom, u27-la1.rom) with the L-1 sound ROMs mous_u4.l1 and mous_u19.l1. " + _SHARED + " Its "
		"Coil, Single Lamps and Switch Levels tests name every address exactly as LA-4 does except switch 37, which LA-1 calls "
		"\"RAMP DRAIN\" where LA-4 calls it \"MADE LEFT RAMP\" (run mousn_l1 in the variant evidence). The manual prints switch "
		"37 as Left Ramp Exit; no source says whether that rename reflects a change on the playfield.",
	),
	"mousn_lu": (
		"compatible",
		"Bally LU-1 European game ROMs (U26 u26-la1.rom with U27 u27-lu1.rom) and the L-1 sound ROMs. " + _SHARED + " Like LA-1, "
		"its service tests name every address exactly as LA-4 does except switch 37 (\"RAMP DRAIN\"; run mousn_lu in the variant "
		"evidence).",
	),
	"mousn_l4c": (
		"unknown",
		"2019 community \"LA-4C Competition MOD\": patched LA-4 game ROMs (the pinned source loads the patch d87f set and keeps "
		"the patch 0a45 and f51e sets as comments; a further Rev 5.0 of October 2021 is mentioned but not loaded). " + _SHARED +
		" Shared game data proves PinMAME routes it like the production machine; its archive is not in the local ROM corpus, "
		"so its service tests, which name every address the ROM drives, could not be compared.",
	),
}

# --- Switch matrix (public address = (column-1)*8+row; System 11 sequential column-major).
# Labels of record follow the Switch Matrix (printed page 2-28) with detail from the Switches parts list
# (printed page 2-29); the ROM's own Switch Levels names are kept per address.
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "A/C Relay C-Side Switch", 3: "Credit Button", 4: "Right Coin Chute", 5: "Center Coin Chute",
	6: "Left Coin Chute", 7: "Slam Tilt", 8: "High Score Reset",
	9: "Outhole", 11: "Trough 1 (Right)", 12: "Trough 2 (Middle)", 13: "Trough 3 (Left)", 14: "Shooter Lane",
	15: "Right Return Loop", 16: "Left Return Loop",
	17: "M (MOUSE Standup)", 18: "O (MOUSE Standup)", 19: "U (MOUSE Standup)", 20: "S (MOUSE Standup)", 21: "E (MOUSE Standup)",
	22: "Top Lane Left", 23: "Top Lane Middle", 24: "Top Lane Right",
	25: "T (TRAP Standup)", 26: "R (TRAP Standup)", 27: "A (TRAP Standup)", 28: "P (TRAP Standup)",
	29: "Left Center Target (Motor Bank)", 30: "Middle Center Target (Motor Bank)", 31: "Right Center Target (Motor Bank)",
	32: "Mouse Hole Enter",
	33: "Trap 1 Up/Down (Right Ball Eater)", 34: "Trap 2 Up/Down (Left Ball Eater)", 35: "Center Ramp",
	36: "Playfield Multiply (Right Standup)", 37: "Left Ramp Exit", 38: "Left Return Lane", 39: "Right Return Lane",
	40: "Right Outlane", 41: "Trap 1 Ball (Right Ball Eater)", 42: "Trap 2 Ball (Left Ball Eater)", 43: "Motor Bank Up",
	44: "Right Ramp Enter", 46: "Right Ramp Exit", 47: "Left Ramp Enter",
	49: "Ball Diverter", 50: "Motor Bank Down", 51: "Left Outlane (Kickback Lane)", 52: "Left Jet Bumper",
	53: "Right Jet Bumper", 54: "Bottom Jet Bumper", 55: "Left Slingshot", 56: "Right Slingshot", 57: "Right Flipper",
	58: "Left Flipper", 59: "Mouse Hole Lock 1", 60: "Mouse Hole Lock 2", 61: "Mouse Hole Lock 3",
}
UNUSED_SWITCHES = frozenset({10, 45, 48, 62, 63, 64})
# Switch Matrix cell wording, kept where it differs from the label of record.
MATRIX_WORDING = {
	2: "Not Used", 8: "High Score Rset", 11: "Trough 1 Right", 12: "Trough 2 Middle", 13: "Trough 3 Left",
	17: "M", 18: "O", 19: "U", 20: "S", 21: "E", 22: "Top Lanes Left", 23: "Top Lanes Middle", 24: "Top Lanes Right",
	25: "T", 26: "R", 27: "A", 28: "P", 29: "Left Center Target", 30: "Middle Center Target", 31: "Right Center Target",
	33: "Trap 1 Up/Down", 34: "Trap 2 Up/Down", 36: "Playfield Multiply", 41: "Trap 1 Ball", 42: "Trap 2 Ball",
	51: "Left Outlane", 52: "Left Jet", 53: "Right Jet", 54: "Bottom Jet", 55: "Left Sling", 56: "Right Sling",
}
# Switches parts list (printed page 2-29) description, kept where it differs from the label of record.
PARTS_LIST_WORDING = {
	2: "Not Used", 4: "Right Coin Sw.", 5: "Center Coin Sw.", 6: "Left Coin Sw.", 11: "Trough 1, Right",
	12: "Trough 2, Middle", 13: "Trough 3, Left", 15: "RT. Ret. Lane Loop", 16: "LT. Ret. Lane Loop",
	17: "M (in Mouse)", 18: "O (in Mouse)", 19: "U (in Mouse)", 20: "S (in Mouse)", 21: "E (in Mouse)",
	22: "Top Lanes Left", 23: "Top Lanes Mid.", 24: "Top Lanes Rt.", 25: "T (in Trap)", 26: "R (in Trap)",
	27: "A (in Trap)", 28: "P (in Trap)", 29: "Left Center Tgt.", 30: "Mid. Center Tgt.", 31: "Rt. Center Tgt.",
	33: "Trap 1 Up/Down", 34: "Trap 2 Up/Down", 36: "Playfield Multiply", 41: "Trap 1 Ball", 42: "Trap 2 Ball",
	43: "Motor Up", 50: "Motor Down", 51: "Left Outlane", 52: "Left Jet", 53: "Right Jet", 54: "Bottom Jet",
	55: "Left Sling ( kicker)", 56: "Right Sling (kicker)", 59: "Mouse Hole Lock1",
}
# The ROM's Switch Levels names, read with the display font's 5/S and 0/O folding resolved.
ROM_SWITCH_NAMES = {
	1: "PLUMB TILT", 2: "NOT USED", 3: "CREDIT BUTTON", 4: "RT. COIN SWITCH", 5: "CNTR. COIN SWITCH", 6: "LEFT COIN SWITCH",
	7: "SLAM TILT", 8: "HIGH SCORE RESET", 9: "OUTHOLE", 10: "NOT USED", 11: "TROUGH 1 BALL", 12: "TROUGH 2 BALLS",
	13: "TROUGH 3 BALLS", 14: "SHOOTER LANE", 15: "RIGHT RET. LOOP", 16: "LEFT RET. LOOP", 17: "MOUSE - M", 18: "MOUSE - O",
	19: "MOUSE - U", 20: "MOUSE - S", 21: "MOUSE - E", 22: "TOP LANES - L", 23: "TOP LANES - M", 24: "TOP LANES - R",
	25: "TRAP - T", 26: "TRAP - R", 27: "TRAP - A", 28: "TRAP - P", 29: "CNTR. STANDUP - L", 30: "CNTR. STANDUP - M",
	31: "CNTR. STANDUP - R", 32: "ENTER MOUSE HOLE", 33: "TRAP 1 UP/DOWN", 34: "TRAP 2 UP/DOWN", 35: "CENTER RAMP",
	36: "RIGHT STANDUP", 37: "MADE LEFT RAMP", 38: "LEFT RET. LANE", 39: "RIGHT RET. LANE", 40: "RIGHT OUTLANE",
	41: "TRAP 1 BALL", 42: "TRAP 2 BALL", 43: "CNTR. STANDUPS UP", 44: "ENTER RIGHT RAMP", 45: "NOT USED",
	46: "MADE RIGHT RAMP", 47: "ENTER LEFT RAMP", 48: "MADE LEFT RAMP", 49: "BALL DIVERTER", 50: "CNTR. STANDUPS DN",
	51: "KICKBACK", 52: "LEFT JET", 53: "RIGHT JET", 54: "BOTTOM JET", 55: "LEFT SLING", 56: "RIGHT SLING",
	57: "RIGHT FLIPPER", 58: "LEFT FLIPPER", 59: "HOLE LOCK 1", 60: "HOLE LOCK 2", 61: "HOLE LOCK 3", 62: "NOT USED",
	63: "NOT USED", 64: "NOT USED",
}
SWITCH_PARTS = {
	1: "20-6502-A", 3: "SW-1A-126", 4: "27-1092", 6: "27-1092", 7: "27-1066", 8: "27-1008", 9: "A-10417",
	11: "5647-12073-00", 12: "5647-09957-00", 13: "5647-09957-00", 14: "5647-12073-04", 15: "A-12866", 16: "5647-12133-04",
	17: "B-12912-16", 18: "B-12912-16", 19: "B-12912-16", 20: "B-12912-16", 21: "B-12912-16",
	22: "5647-12073-19", 23: "5647-12073-19", 24: "5647-12073-19",
	25: "B-12912-16", 26: "B-12912-16", 27: "B-12912-16", 28: "B-12912-16",
	29: "A-11177-1", 30: "A-11315-3", 31: "A-11315-3", 32: "A-11991", 33: "p/o B-20-9629", 34: "p/o B-20-9629",
	35: "5647-12073-31", 36: "B-11696-6", 37: "A-12238", 38: "A-12688", 39: "A-12688", 40: "A-12688",
	41: "p/o B-20-9629", 42: "p/o B-20-9629", 43: "5647-12073-06", 44: "A-12238", 46: "5647-12133-04", 47: "A-12238",
	49: "A-12953", 50: "5647-12073-06", 51: "5647-12073-19", 52: "SW-11A-37", 53: "SW-11A-37", 54: "SW-11A-37",
	55: "SW-1A-114", 56: "SW-1A-114", 57: "03-7811", 58: "03-7811", 59: "p/o C-13061", 60: "p/o C-13061", 61: "p/o C-13061",
}
# Construction is asserted only where a part number or assembly page identifies it.
SWITCH_TYPES = {1: "tilt", 2: "other", 3: "button", 4: "other", 5: "other", 6: "other", 7: "tilt", 8: "button"}
MICROSWITCH_PARTS = ("5647-12073-", "5647-09957-")
MICROSWITCH_NOTE = (
	" Its 5647-series part is a microswitch: the Ball Trough Switches page (printed 2-16) labels both 5647-09957-00 and "
	"5647-12073-08 \"MICROSWITCH\"."
)
SWITCH_COLUMN_WIRING = {
	1: ("GRN-BRN", "1J8-1", "Q45"), 2: ("GRN-RED", "1J8-2", "Q49"), 3: ("GRN-ORN", "1J8-3", "Q44"),
	4: ("GRN-YEL", "1J8-4", "Q48"), 5: ("GRN-BLK", "1J8-5", "Q43"), 6: ("GRN-BLU", "1J8-7", "Q47"),
	7: ("GRN-VIO", "1J8-8", "Q42"), 8: ("GRN-GRY", "1J8-9", "Q46"),
}
SWITCH_ROW_WIRING = {
	1: ("WHT-BRN", "1J10-9"), 2: ("WHT-RED", "1J10-8"), 3: ("WHT-ORN", "1J10-7"), 4: ("WHT-YEL", "1J10-6"),
	5: ("WHT-GRN", "1J10-5"), 6: ("WHT-BLU", "1J10-3"), 7: ("WHT-VIO", "1J10-2"), 8: ("WHT-GRY", "1J10-1"),
}
DEDICATED_LABELS = {
	-7: ("Advance (Diagnostic)", "service.advance"), -6: ("Auto-Up/Manual-Down (Diagnostic)", "service.updown"),
	-5: ("CPU Diagnostic", "service.cpu-diag"), -4: ("Sound Diagnostic", "service.sound-diag"),
}
CABINET_SWITCH_ROLES = {
	1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin",
	7: "cabinet.slam-tilt", 8: "cabinet.service", 57: "cabinet.flipper", 58: "cabinet.flipper",
}

# --- Retained-table objects in VPX units (bounds 964 x 2162).
DRAIN = (456.749, 2080.9575)
BALL_RELEASE = (830.0902, 1876.4113)
RIGHT_TRAP = (808.228, 884.1773)
LEFT_TRAP = (168.4438, 352.1403)
MOUSE_HOLE = (735.5594, 37.6466)
KICKBACK_KICKER = (42.8752, 1750.6572)
MOTOR_BANK_MIDDLE = (437.8127, 968.5033)
DIVERTER_ARM = (382.9156, 124.2674)
TOP_GATE = (613.1231, 229.3609)
BUMPERS = {52: (369.7802, 565.9415), 53: (574.7341, 568.1612), 54: (471.887, 751.6578)}
SLINGS = {55: (216.8619, 1562.7523), 56: (641.4618, 1564.7176)}
FLASHER_28_DOME = (875.889, 83.2223)

# Switch placements: the object the script binds to each address.
SWITCH_OBJECTS = {
	9: ("Kicker Drain", DRAIN),
	14: ("Trigger sw14", (904.0748, 1909.05)), 15: ("Trigger sw15", (708.3034, 270.0019)),
	16: ("Trigger sw16", (114.4473, 418.9412)),
	17: ("HitTarget sw17", (89.7976, 1021.8088)), 18: ("HitTarget sw18", (88.8772, 1081.0287)),
	19: ("HitTarget sw19", (89.9307, 1140.551)), 20: ("HitTarget sw20", (89.4039, 1203.7609)),
	21: ("HitTarget sw21", (89.4039, 1268.0242)),
	22: ("Trigger sw22", (318.6828, 372.2816)), 23: ("Trigger sw23", (419.7674, 370.7501)),
	24: ("Trigger sw24", (520.4266, 371.7286)),
	25: ("HitTarget sw25", (716.2914, 840.7529)), 26: ("HitTarget sw26", (714.4858, 904.2164)),
	27: ("HitTarget sw27", (713.4453, 969.143)), 28: ("HitTarget sw28", (713.9539, 1032.4047)),
	29: ("HitTarget sw29", (381.6992, 960.8782)), 30: ("HitTarget sw30", (438.1395, 960.7479)),
	31: ("HitTarget sw31", (494.0024, 960.7481)),
	32: ("Trigger sw32", (139.6667, 45.6666)), 35: ("Trigger sw35", (438.783, 959.418)),
	36: ("HitTarget sw36", (810.2015, 672.8691)), 37: ("Trigger sw37", (43.7178, 1159.1907)),
	38: ("Trigger sw38", (117.5467, 1573.485)), 39: ("Trigger sw39", (742.2926, 1584.2703)),
	40: ("Trigger sw40", (819.915, 1583.2955)),
	41: ("Kicker rightTrap41", RIGHT_TRAP), 42: ("Kicker leftTrap42", LEFT_TRAP),
	44: ("Trigger sw44", (702.3333, 431.0)), 46: ("Trigger sw46", (44.9087, 714.8511)),
	47: ("Trigger sw47", (155.6429, 589.5092)), 51: ("Trigger sw51", (41.7079, 1724.0604)),
	52: ("Bumper Bumper52", BUMPERS[52]), 53: ("Bumper Bumper53", BUMPERS[53]), 54: ("Bumper Bumper54", BUMPERS[54]),
	55: ("Wall LeftSlingshot (drag-point mean)", SLINGS[55]), 56: ("Wall RightSlingshot (drag-point mean)", SLINGS[56]),
	59: ("Kicker MouseHole", MOUSE_HOLE), 60: ("Trigger sw60", (675.9501, 32.8719)), 61: ("Trigger sw61", (619.568, 32.8719)),
}
# Documented projections: a sensor with no table object of its own, placed on its own mechanism's object.
SWITCH_PROJECTIONS = {
	11: (BALL_RELEASE, (
		"Projected onto the table's ball-release kicker (Kicker BallRelease, object centre): the retained script models the "
		"trough as one three-ball cvpmBallStack (bsTrough.InitSw 0, 11, 12, 13 with InitKick BallRelease, script lines "
		"191-196) and has no object per trough position. The switch drawing places 11 at the right end of the trough."
	)),
	12: (BALL_RELEASE, "Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11."),
	13: (BALL_RELEASE, "Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11."),
	33: (RIGHT_TRAP, (
		"Projected onto the table's right trap kicker (Kicker rightTrap41), the ball eater whose up/down switch this is "
		"(part of B-20-9629); the script writes it from its trap routines (lines 615-708) and has no object for it."
	)),
	34: (LEFT_TRAP, (
		"Projected onto the table's left trap kicker (Kicker leftTrap42), the ball eater whose up/down switch this is (part "
		"of B-20-9629); the script writes it from its trap routines (lines 615-708) and has no object for it."
	)),
	43: (MOTOR_BANK_MIDDLE, (
		"Projected onto the middle target of the table's motorized bank (Primitive pTarget30, object position): the motor "
		"limit switches sit on the motor under the playfield, and the script writes 43 and 50 from its motor-bank timer "
		"(lines 751-821)."
	)),
	50: (MOTOR_BANK_MIDDLE, "Projected onto the middle target of the table's motorized bank (Primitive pTarget30); see switch 43."),
	49: (DIVERTER_ARM, (
		"Projected onto the table's diverter arm (Primitive pDiverterArm, object position), the moving part of the C-12902-1 "
		"Ball Deflector whose A-12953 Mini Switch this is; the script toggles 49 on each diverter pulse (lines 709-745)."
	)),
}
SWITCH_OBJECT_NOTES = {
	9: "The script's Drain_Hit pulses 9 (lines 347-353).",
	41: "The script's trap routine sets 41 while a ball rests in the right trap and clears it when the trap kicks it out (lines 615-708).",
	42: "The script's trap routine sets 42 while a ball rests in the left trap and clears it when the trap kicks it out (lines 615-708).",
	59: (
		"The script's MouseHole_Hit sets 59 (lines 589-592) and SolMouseHoleRelease clears it as the hole kicks (lines 593-600). "
		"The manual puts the mouse hole on the back panel (\"Solenoid #16 is on the Back Panel\"); the table stands its kicker at "
		"the top edge of the playfield."
	),
	60: "The second and third mouse-hole lock switches stand behind the first along the table's back-panel lane.",
	61: "See switch 60.",
}

# --- Solenoid Table (printed page 2-30) and Solenoid/Flashers list (printed page 2-31).
# Switched A/C pairs: (A-side public, C-side public, CPU connection, A-side power, C-side power, driver, C-side CPU bracket).
AC_PAIRS = {
	1: (1, 25, "1P11-1", "5J1-9: 5J4-9 (A)", "5J5-9 (C)", "Q33", "(Gry-Brn)"),
	2: (2, 26, "1P11-3", "5J1-7: 5J4-8 (A)", "5J5-8 (C)", "Q25", "(Gry-Red"),
	3: (3, 27, "1P11-4", "5J1-6: 5J4-7 (A)", "5J5-7(C)", "Q32", "(Gry-Orn"),
	4: (4, 28, "1P11-5", "5J1-5: 5J4-6 (A)", "5J5-5 (C)", "Q24", "(Gry-Yel)"),
	5: (5, 29, "1P11-6", "5J1-4: 5J4-5 (A)", "5J5-4 (C)", "Q31", "(Gry-Grn)"),
	6: (6, 30, "1P11-7", "5J1-3: 5J4-4 (A)", "5J5-3 (C)", "Q23", "(Gry-Blu)"),
	7: (7, 31, "1P11-8", "5J1-2: 5J4-2 (A)", "5J5-2 (C)", "Q30", "(Gry-Vio"),
	8: (8, 32, "1P11-9", "5J1-1: 5J4-1 (A)", "5J5-1 (C)", "Q22", "(Gry-Blk]"),
}
SOLENOID_LABELS = {
	1: "Outhole Kicker", 2: "Ball Shooter Lane Feeder", 3: "Trap 1 Up (Right Ball Eater)", 4: "Trap 2 Up (Left Ball Eater)",
	5: "Trap 1 Down (Right Ball Eater)", 6: "Not Used Solenoid 6 (A Side, Unfitted)", 7: "Knocker",
	8: "Trap 2 Down (Left Ball Eater)",
	9: "Insert Board G.I. Relay", 10: "Playfield G.I. Relay", 11: "Motor Relay (Center Target Bank)", 12: "A/C Select Relay",
	13: "Kickback", 14: "Ball Diverter", 15: "Center Flashers", 16: "Mouse Hole Exit (Drop Kick)",
	17: "Left Jet Bumper", 18: "Left Slingshot", 19: "Right Jet Bumper", 20: "Right Slingshot", 21: "Lower Jet Bumper",
	22: "Top Lanes Gate",
	25: "Right Flipper Flasher", 26: "Left Flipper Flasher", 27: "Left Side Flasher", 28: "Back Panel Flasher",
	29: "Top Right Flasher", 30: "Right Ramp Flasher", 31: "Left Ramp Flashers", 32: "Timer Flasher",
}
SOLENOID_MANUAL_NUMBER = {address: f"{address:02d}A" for address in range(1, 9)}
SOLENOID_MANUAL_NUMBER.update({address: f"{address - 24:02d}C" for address in range(25, 33)})
SOLENOID_MANUAL_NUMBER.update({address: f"{address:02d}" for address in range(9, 23)})
SOLENOID_TABLE_WORDING = {
	1: "Outhole Kicker", 2: "Ball Shooter Lane Feeder", 3: "Trap 1 Up", 4: "Trap 2 Up", 5: "Trap 1 Down", 6: "Not Used",
	7: "Knocker", 8: "Trap 2 Down", 9: "Insert Board Gnl Illum Relay", 10: "Playfield Gnl Illum Relay", 11: "Motor Relay",
	12: "A/C Select", 13: "Kickback (L Outlane)", 14: "Ball Diverter", 15: "Center Flashers", 16: "Mouse Hole Exit",
	17: "Left Jet Bumper", 18: "Left Kicker (\"sling\")", 19: "Right Jet Bumper", 20: "Right Kicker (\"sling\")",
	21: "Lower Jet Bumper", 22: "Top Lanes Gate", 25: "Right Flipper Flasher", 26: "Left Flipper Flasher",
	27: "Left Side Flasher", 28: "Back Panel Flasher", 29: "Top Right Flasher", 30: "Right Ramp Flasher",
	31: "Left Ramp Flashers", 32: "Timer Flasher",
}
LIST_WORDING = {
	1: "Outhole", 2: "Ball Shooter Lane Feeder", 3: "Trap 1 Up", 4: "Trap 2 Up", 5: "Trap 1 Down", 6: "Not Used",
	7: "Knocker", 8: "Trap 2 Down", 9: "Insert Bd. Gen. Illum.", 10: "Playfield Gen. Illum.", 11: "Motor Relay",
	12: "Solenoid A/C Select", 13: "Kickback", 14: "Ball Diverter", 15: "Center Flashers", 16: "Mouse Hole Exit",
	17: "Left Jet Bumper", 18: "Left Kicker (sling)", 19: "Right Jet Bumper", 20: "Right Kicker (sling)",
	21: "Lower Jet Bumper", 22: "Top Lanes Gate", 25: "Right Flipper Flasher", 26: "Left Flipper Flasher",
	27: "Left side Flasher", 28: "Back Panel Flasher", 29: "Top Right Flasher", 30: "Right Ramp Flasher",
	31: "Left Ramp Flashers", 32: "Timer Flashers",
}
ROM_COIL_NAMES = {
	1: "OUTHOLE", 25: "RT. FLIP. FLASHERS", 2: "BALL RELEASE", 26: "LT. FLIP. FLASHERS", 3: "TRAP 1 UP", 27: "LEFT SIDE FLSHER",
	4: "TRAP 2 UP", 28: "BACKPANEL FLSHER", 5: "TRAP 1 DOWN", 29: "TOP RT. FLASHER", 6: "NOT USED", 30: "RT. RAMP FLASHERS",
	7: "KNOCKER", 31: "LT. RAMP FLASHERS", 8: "TRAP 2 DOWN", 32: "TIMER FLASHER", 9: "INSERT G.I.", 10: "PLAYFIELD G.I.",
	11: "STANDUP MOTOR", 12: "A/C SELECT", 13: "KICKBACK", 14: "BALL DIVERTER", 15: "CENTER FLASHER",
	16: "MOUSE HOLE EJECT", 17: "LEFT JET", 18: "LEFT SLING", 19: "RIGHT JET", 20: "RIGHT SLING", 21: "BOTTOM JET",
	22: "SHOOTER GATE",
}
COIL_TEST_ORDER = (1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22)
SOLENOID_WIRE = {
	1: "Vio-Brn", 25: "Blk-Brn", 2: "Vio-Red", 26: "Blk-Red", 3: "Vio-Orn", 27: "Blk-Orn", 4: "Vio- Yel", 28: "Blk-Yel",
	5: "Vio-Grn", 29: "Blk-Grn", 6: "Vio-Blu", 30: "Blk-Blu", 7: "Vio-Blk", 31: "Blk-Vio", 8: "Vio-Gry", 32: "Blk-Gry",
	9: "Brn-Blk", 10: "Brn-Red", 11: "Brn-Orn", 12: "Brn-Yel", 13: "Brn-Grn", 14: "Brn-Blu", 15: "Brn-Vio",
	16: "Brn-Gry", 17: "Blu-Brn", 18: "Blu-Red", 19: "Blu-Orn", 20: "Blu-Yel", 21: "Blu-Grn", 22: "Blu-Blk",
}
CONTROLLED = {
	9: ("1P12-1", "5J2-9: 5J6-9: 2J4-3", "Q17"), 10: ("1P12-2", "5J2-8: 5J6-8: 2J4-5", "Q9"),
	11: ("1P12-4", "5J2-6: 5J6-7: 2J4-6", "Q16"), 12: ("1P12-5", "5J2-5", "Q8"),
	13: ("1P12-6", "5J2-4: 5J6-5", "Q15"), 14: ("1P12-7", "5J2-4: 5J6-3", "Q7"),
	15: ("1P12-8", "5J2-2: 5J6-2", "Q14"), 16: ("1P12-9", "5J2-1: 5J6-1", "Q6"),
	17: ("1P19-7", "5J3-7: 5J7-7", "Q75"), 18: ("1P19-4", "5J3-6: 5J7-6", "Q71"), 19: ("1P19-3", "5J3-3: 5J7-3", "Q73"),
	20: ("1P19-6", "5J3-4: 5J7-5", "Q69"), 21: ("1P19-8", "5J3-2:5J7-2", "Q77"), 22: ("1P19-9", "5J3-1: 5J7-1", "Q79"),
}
SOLENOID_PART = {
	1: "AE-23-800", 25: "#89 flashlamps", 2: "AE-23-800", 26: "#89 flashlamps", 3: "AE-26-1400", 27: "#89 flashlamps",
	4: "AE-26-1400", 28: "#906 flashlamp", 5: "SM1-28-800", 29: "#89 flashlamp", 30: "#89 flashlamp", 7: "AE-23-800",
	31: "#89 flashlamp", 8: "SM1-28-800", 32: "#89 flashlamps", 9: "5580-09555-01", 10: "5580-09555-01",
	11: "5580-12145-01", 12: "5580-09555-01", 13: "AE-24-900", 14: "AE-23-800", 15: "#89 flashlamps", 16: "AE-26-1200",
	17: "AE-23-800", 18: "AE-26-1500", 19: "AE-23-800", 20: "AE-26-1500", 21: "AE-23-800", 22: "SM2-35-4000",
}
# The Solenoid Table's quantity suffix (p = playfield, b = printed without a legend entry).
FLASHLAMP_QUANTITY = {25: 2, 26: 2, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 2, 15: 1}
SOLENOID_KIND = {
	1: "coil", 2: "coil", 3: "coil", 4: "coil", 5: "coil", 6: "coil", 7: "coil", 8: "coil", 9: "gi", 10: "gi",
	11: "relay", 12: "relay", 13: "coil", 14: "coil", 15: "flasher", 16: "coil", 17: "coil", 18: "coil", 19: "coil",
	20: "coil", 21: "coil", 22: "coil", 25: "flasher", 26: "flasher", 27: "flasher", 28: "flasher", 29: "flasher",
	30: "flasher", 31: "flasher", 32: "flasher",
}
# What the retained known-working script does with each address (script.vbs).
SOLENOID_CALLBACKS = {
	1: "SolOuthole (line 304), bsTrough.SolIn, which kicks a drained ball from Kicker Drain into the trough",
	2: "SolBallRelease (line 305), bsTrough.SolOut, kicking the next trough ball from Kicker BallRelease",
	3: "SolRightTrapUp (line 306), which raises the right trap and kicks out a ball resting in it (lines 615-708)",
	4: "SolLeftTrapUp (line 307), which raises the left trap and kicks out a ball resting in it (lines 615-708)",
	5: "SolRightTrapDown (line 308), which lowers the right trap and closes switch 33 (lines 615-708)",
	7: "vpmSolSound with the Knocker sound (line 310)",
	8: "SolLeftTrapDown (line 309), which lowers the left trap and closes switch 34 (lines 615-708)",
	10: "SolGI (line 311), which turns the table's G.I. off while the solenoid is on (lines 1188-1204)",
	11: (
		"SolMotorBank (line 312), which moves the three center target primitives down from the up limit or up from the down "
		"limit over about 2 s, opening the limit it leaves and closing 50 or 43 at the far end (lines 751-821)"
	),
	13: "SolKickback (line 313), which enables the Kickback kicker in the left outlane (lines 444-458)",
	14: (
		"SolMouseHoleDiverter (line 314), which swings pDiverterArm, toggles switch 49 and makes the WallDiverter wall solid "
		"while 49 is closed; the right-ramp entry switch's handler makes WallGuideToTop solid while 49 is open (lines 709-745)"
	),
	15: "Flash 15 (line 321), fading fLight15 and fBulb15 (InitFlasher, line 897)",
	16: "SolMouseHoleRelease (line 315), which kicks the ball out of Kicker MouseHole and clears switch 59 (lines 593-599)",
	22: "SolOrbitGate (line 316), which opens GateTopRight while the solenoid is on (lines 464-466)",
	25: "Flash 25 (line 322), fading fLight25, fPlasticsLight25 and fBulb25 (InitFlasher, line 899)",
	26: "Flash 26 (line 323), fading fLight26, fPlasticsLight26 and fBulb26 (InitFlasher, line 901)",
	27: (
		"Flash 27 (line 324), fading fLight27, fPlasticsLight27, fBulb27, fLight27a, fPlasticsLight27a, fBulb27a and fLight27b "
		"(InitFlasher, line 903)"
	),
	28: "Flash28 (lines 325 and 1016-1021), switching the pFlasher28 dome's image and material and its f28/f28a lights",
	29: "Flash 29 (line 326), fading fLight29, fPlasticsLight29 and fBulb29 (InitFlasher, line 905)",
	30: (
		"Flash 30 (line 327), fading fLight30, fPlasticsLight30, fBulb30, fLight30a, fPlasticsLight30a, fBulb30a, fLight30b, "
		"fPlasticsLight30b and fBulb30b (InitFlasher, line 907)"
	),
	31: (
		"Flash 31 (line 328), fading fLight31, fPlasticsLight31, fBulb31, fLight31a, fPlasticsLight31a and fBulb31a "
		"(InitFlasher, line 909)"
	),
	32: "Flash 32 (line 329), fading fLight32 only (InitFlasher, line 911)",
}
# Placements: (object, coordinate in VPX units) per bulb or effect location.
SOLENOID_OBJECTS = {
	1: [("Kicker Drain", DRAIN)], 2: [("Kicker BallRelease", BALL_RELEASE)],
	3: [("Kicker rightTrap41", RIGHT_TRAP)], 5: [("Kicker rightTrap41", RIGHT_TRAP)],
	4: [("Kicker leftTrap42", LEFT_TRAP)], 8: [("Kicker leftTrap42", LEFT_TRAP)],
	11: [("Primitive pTarget30, the bank's middle target (object position)", MOTOR_BANK_MIDDLE)],
	13: [("Kicker Kickback", KICKBACK_KICKER)], 14: [("Primitive pDiverterArm (object position)", DIVERTER_ARM)],
	16: [("Kicker MouseHole", MOUSE_HOLE)],
	17: [("Bumper Bumper52", BUMPERS[52])], 19: [("Bumper Bumper53", BUMPERS[53])], 21: [("Bumper Bumper54", BUMPERS[54])],
	18: [("Wall LeftSlingshot (drag-point mean)", SLINGS[55])], 20: [("Wall RightSlingshot (drag-point mean)", SLINGS[56])],
	22: [("Gate GateTopRight", TOP_GATE)],
	15: [("Primitive pBulb12 (hidden bulb under fBulb15)", (438.8021, 847.5373))],
	25: [("Primitive pBulb5 (bulb under fBulb25)", (721.3393, 1728.1726))],
	26: [("Primitive pBulb2 (bulb under fBulb26)", (138.0832, 1726.6729))],
	28: [("Primitive pFlasher28 (dome, object position)", FLASHER_28_DOME)],
	29: [("Primitive pBulb22 (bulb under fBulb29)", (863.2949, 163.3134))],
}
# Placements that are documented projections rather than the device's own table object.
SOLENOID_PROJECTED = {
	1: "the drain kicker the script's ball stack receives balls on; the B-8039-2 outhole kicker coil has no object of its own",
	2: "the ball-release kicker the script kicks from; the C-9638-1 feeder coil has no object of its own",
	3: "the right trap's kicker; the ball eater's AE-26-1400 up coil sits under the playfield and has no object of its own",
	5: "the right trap's kicker; the ball eater's SM1-28-800 down coil sits under the playfield and has no object of its own",
	4: "the left trap's kicker; the ball eater's AE-26-1400 up coil sits under the playfield and has no object of its own",
	8: "the left trap's kicker; the ball eater's SM1-28-800 down coil sits under the playfield and has no object of its own",
	11: "the motorized bank's middle target; the motor and its relay sit under the playfield and have no object of their own",
	14: "the diverter arm; the C-12902-1 Ball Deflector's AE-23-800 coil has no object of its own",
}
FLASHER_NOTES = {
	15: (
		"The Solenoid Table prints \"#89 flashlamps\" with quantity 1p, and the function \"Center Flashers\" in the plural; the "
		"quantity follows the 1p. The placement is the table's bulb primitive pBulb12 under fBulb15, which the table "
		"hides (is_visible false); it is the only bulb the script lights for this address. Pinned PinMAME types 15 and 16 as "
		"#89 bulbs (s11.c mousn_ block); 16 is the Mouse Hole Exit coil, so that typing is right for 15 only."
	),
	25: (
		"The Solenoid Table prints 2p: two playfield bulbs. The solenoid drawing prints callout 01C twice, once at each edge, "
		"while the retained table models one bulb (pBulb5 under fBulb25 beside the right flipper), which is the one placement; "
		"the second bulb has no table object."
	),
	26: (
		"The Solenoid Table prints 2p: two playfield bulbs. The retained table models one (pBulb2 under fBulb26 beside the "
		"left flipper), which is the one placement; the second bulb has no table object."
	),
	28: (
		"The Solenoid Table prints a #906 flashlamp with quantity 1b (the heading's legend names only d and p) and the "
		"function \"Back Panel Flasher\". The retained table models it as a flasher dome at the top right of the playfield "
		"(pFlasher28) whose position is the placement, the back-panel socket projected on the panel's plane."
	),
	29: "The Solenoid Table prints 1p. The placement is the table's bulb pBulb22 under fBulb29 at the top right.",
}
UNPLACED_FLASHER_NOTES = {
	27: (
		"The Solenoid Table prints \"#89 flashlamps\" with quantity 1p, one playfield bulb, and the solenoid drawing one 03C "
		"callout on the left edge, but the retained script lights two table bulbs for it, pBulb8 under fBulb27 at (44.1, 1264.4) and pBulb10 under fBulb27a at "
		"(43.4, 904.2) VPX units, plus a bulbless light fLight27b. Which of the two is the machine's socket no source settles, "
		"so the spatial key is omitted."
	),
	30: (
		"The Solenoid Table prints 1p and the solenoid drawing one 06C callout on the right edge, between 05C and the right jet "
		"bumper (19), but the retained script lights three table bulbs for it: pBulb11 under fBulb30 at (687.3, 372.7), pBulb21 "
		"under fBulb30b at (786.0, 561.1) and pBulb23 under fBulb30a at (739.0, 936.2) VPX units. Which of them is the machine's "
		"socket no source settles, so the spatial key is omitted."
	),
	31: (
		"The Solenoid Table prints \"#89 flashlamp\" with quantity 1p under the plural function \"Left Ramp Flashers\", and the "
		"Solenoid/Flashers list prints \"#89 Flashlamps\"; the retained script lights two table bulbs for it, pBulb28 under fBulb31 at (170.9, 468.0) "
		"and pBulb13 under fBulb31a at (59.0, 297.8) VPX units. The count and the sockets stay unsettled, so the spatial key "
		"is omitted."
	),
	32: (
		"The Solenoid Table prints 2p (the list says \"Timer Flashers\") and the solenoid drawing marks 08C on the right edge, "
		"but the retained table lights only a bulbless light, fLight32, for it, so the spatial key is omitted."
	),
}

VIRTUAL_SOLENOIDS = {
	23: ("Game-On / Special-Solenoid Enable", "used", "internal.game-on-enable", (
		"PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL (pinned src/wpc/s11.h S11_GAMEONSOL 23), set from PIA0 CB2 in pia0cb2_w "
		"and used to gate the six special solenoids and the synthetic flipper outputs 45-48. It has no driver transistor and "
		"no Sol. No. of its own. In the gameplay run it is 0 in attract mode, rises 0.054 s after the Credit button starts a "
		"game, falls 0.069 s after the third plumb-bob closure and rises again 0.45 s before the feeder serves ball 2."
	)),
	24: ("Unassigned Solenoid Slot 24", "unused", "internal.unused-platform-slot", (
		"Unassigned platform gap between the special-solenoid enable (23) and the A/C-relay C-side bank (25-32); no System 11 "
		"driver populates it and no Mousin' Around run published it."
	)),
	45: ("Synthetic Lower Right Flipper Power", "used", "internal.synthetic-flipper", (
		"PinMAME's synthetic lower-right flipper power output (CORE_FIRSTLFLIPSOL = 45). mousnGameData declares "
		"FLIP_SWNO(58,57) with no FLIP_SOL, so core_updateSw fabricates 45/46 from the right button bit at public 82 and 47/48 "
		"from the left bit at public 84 while the enable (23) is on. The manual confirms there is no driver behind them: the "
		"two flipper rows of the Solenoid Table carry no Sol. No. and no transistor, and note 1 says the CPU-board wire runs to "
		"the flipper switch. The retained script binds SolCallback(sLLFlipper) and SolCallback(sLRFlipper), core.vbs's 48 and "
		"46, to its flipper subs (lines 318-319)."
	)),
	46: ("Synthetic Lower Right Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-right flipper hold output, which the retained script's SolRFlipper follows; see address 45."),
	47: ("Synthetic Lower Left Flipper Power", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper power output; see address 45."),
	48: ("Synthetic Lower Left Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper hold output, which the retained script's SolLFlipper follows; see address 45."),
	49: ("PinMAME Simulator Ball-Shooter Channel", "unused", "internal.unused-platform-slot", (
		"Platform-wide simulator-only output (CORE_FIRSTSIMSOL = 49); mousnGameData declares no simulator."
	)),
	50: ("Unassigned Solenoid Slot 50", "unused", "internal.unused-platform-slot", (
		"Unassigned gap below the custom-solenoid base (51). mousnGameData declares no custSol, so MACHINE_INIT(s11) sizes "
		"coreGlobals.nSolenoids as CORE_FIRSTCUSTSOL-1+0 = 50 and nothing above 50 is modelled."
	)),
}
UPPER_FLIPPER_NOTE = (
	"Platform generic upper-flipper address (CORE_FIRSTUFLIPSOL = 33). mousnGameData's FLIP_SWNO(58,57) sets no upper FLIP_SW "
	"or FLIP_SOL bit and core_getSol serves 33-36 only for WPC and SAM generations, so it reads as always zero. Mousin' Around "
	"has two flippers only: the Solenoid Table and the Solenoid/Flashers list name a right and a left flipper and nothing else."
)
OVERLAY_NOTE = (
	"Platform sound-overlay range (37-44). mousnGameData's hw.gameSpecific1 is S11_MUXSW2 only, so S11_SNDOVERLAY is unset and "
	"pia5cb2_w never diverts the sound byte to a solenoid pattern. Unpopulated on this machine."
)

# --- Lamp matrix (public address = (column-1)*8+row). Labels from the Lamp Matrix (printed page 2-26).
LAMP_LABELS = {
	1: "Shoot Again", 2: "Set Trap 2", 3: "Return Loop 50K", 4: "Return Loop 100K", 5: "Return Loop 150K",
	6: "Return Loop 200K", 7: "Return Loop 250K", 8: "Jackpot",
	9: "C (in CHEESE)", 10: "H (in CHEESE)", 11: "E (in CHEESE, first)", 12: "E (in CHEESE, second)", 13: "S (in CHEESE)",
	14: "E (in CHEESE, third)", 15: "2X Bonus", 16: "3X Bonus",
	17: "M (in MOUSE)", 18: "O (in MOUSE)", 19: "U (in MOUSE)", 20: "S (in MOUSE)", 21: "E (in MOUSE)",
	22: "Top Lane Left", 23: "Top Lane Middle", 24: "Top Lane Right",
	25: "T (in TRAP)", 26: "R (in TRAP)", 27: "A (in TRAP)", 28: "P (in TRAP)",
	29: "Left Center Target", 30: "Middle Center Target", 31: "Right Center Target", 32: "Double Playfield Value Timer",
	33: "Set Trap 1", 34: "Playfield Multiply", 35: "Spot Cheese 3", 36: "Kickback", 37: "Left Outlane", 38: "Left Return Lane",
	39: "Right Return Lane", 40: "Right Outlane", 41: "Qualify Million 1", 42: "Extra Ball 1", 43: "Spot Cheese 1",
	44: "Qualify Million 2", 45: "Extra Ball 2", 46: "Spot Cheese 2", 47: "Right Stand-up Target", 48: "Cheezy Bonus (Right Ramp)",
	49: "N (in MILLION, Back Panel)", 50: "O (in MILLION, Back Panel)", 51: "I (in MILLION, Back Panel, second)",
	52: "L (in MILLION, Back Panel, second)", 53: "L (in MILLION, Back Panel, first)", 54: "I (in MILLION, Back Panel, first)",
	55: "M (in MILLION, Back Panel)", 56: "Build Jackpot (Back Panel)",
	57: "Jackpot 1 Million (Insert Board)", 58: "Jackpot 1.5 Million (Insert Board)", 59: "Jackpot 2 Million (Insert Board)",
	60: "Jackpot 2.5 Million (Insert Board)", 61: "Jackpot 3 Million (Insert Board)", 62: "Jackpot 4 Million (Insert Board)",
	63: "Jackpot 5 Million (Insert Board)",
}
LAMP_MATRIX_WORDING = {
	3: "50 K", 4: "100 K", 5: "150 K", 6: "200 K", 7: "250 K", 9: "C", 10: "H", 11: "E", 12: "E", 13: "S", 14: "E",
	17: "M", 18: "O", 19: "U", 20: "S", 21: "E", 22: "Top Lanes Left", 23: "Top Lanes Middle", 24: "Top Lanes Right",
	25: "T", 26: "R", 27: "A", 28: "P", 32: "Double Plyd Value Timer", 41: "Qualify Million 1 • •",
	44: "Qualify Million 2 • •", 48: "Cheezy Bonus • •", 49: "N", 50: "O", 51: "I", 52: "L", 53: "L",
	54: "I", 55: "M", 56: "Build Jackpot", 57: "Jackpot 1 Million", 58: "Jackpot 1.5 Million", 59: "Jackpot 2 Million",
	60: "Jackpot 2.5 Million", 61: "Jackpot 3 Million", 62: "Jackpot 4 Million", 63: "Jackpot 5 Million",
}
LAMP_LIST_WORDING = {
	3: "50K", 4: "100K", 5: "150K", 6: "200K", 7: "250K", 9: "C (IN \"CHEESE\")", 10: "H (IN \"CHEESE\")",
	11: "E (IN \"CHEESE\")", 12: "E (IN \"CHEESE\")", 13: "S (IN \"CHEESE\")", 14: "E (IN \"CHEESE\")",
	17: "M (IN \"MOUSE\")", 18: "O (IN \"MOUSE\")", 19: "U (IN \"MOUSE\")", 20: "S (IN \"MOUSE\")", 21: "E (IN \"MOUSE\")",
	22: "Top Lanes Left", 23: "Top Lanes Middle", 24: "Top Lanes Right", 25: "T (IN \"TRAP\")", 26: "R (IN \"TRAP\")",
	27: "A (IN \"TRAP\")", 28: "P (IN \"TRAP\")", 32: "Timer", 47: "Right Stand-up", 48: "Cheezy Bonus",
}
# The ROM's Single Lamps names, read with the display font's 5/S and 0/O folding resolved.
ROM_LAMP_NAMES = {
	1: "SHOOT AGAIN", 2: "TRAP 2 SET", 3: "RETURN LOOP 50K", 4: "RETURN LOOP 100K", 5: "RETURN LOOP 150K",
	6: "RETURN LOOP 200K", 7: "RETURN LOOP 250K", 8: "JACKPOT", 9: "CHEESE - C", 10: "CHEESE - H", 11: "CHEESE - E",
	12: "CHEESE - E", 13: "CHEESE - S", 14: "CHEESE - E", 15: "BONUS - 2X", 16: "BONUS - 3X", 17: "MOUSE - M",
	18: "MOUSE - O", 19: "MOUSE - U", 20: "MOUSE - S", 21: "MOUSE - E", 22: "TOP LANES - L", 23: "TOP LANES - M",
	24: "TOP LANES - R", 25: "TRAP - T", 26: "TRAP - R", 27: "TRAP - A", 28: "TRAP - P", 29: "CNTR. STANDUP - L",
	30: "CNTR. STANDUP - M", 31: "CNTR. STANDUP - R", 32: "TIMER", 33: "TRAP 1 SET", 34: "PLAYFLD MULTIPLY",
	35: "SPOT CHEESE - 3", 36: "KICK BACK", 37: "LEFT OUTLANE", 38: "LEFT RETURN LANE", 39: "RT. RETURN LANE",
	40: "RIGHT OUTLANE", 41: "SPOT MILL. - 1", 42: "EXTRA BALL - 1", 43: "SPOT CHEESE - 1", 44: "SPOT MILL. - 2",
	45: "EXTRA BALL - 2", 46: "SPOT CHEESE - 2", 47: "RIGHT STANDUP", 48: "RIGHT RAMP", 49: "MILLION - N", 50: "MILLION - O",
	51: "MILLION - I", 52: "MILLION - L", 53: "MILLION - L", 54: "MILLION - I", 55: "MILLION - M", 56: "BUILD JACKPOT",
	57: "JACKPOT 1 MILL.", 58: "JACKPOT 1.5 MILL.", 59: "JACKPOT 2 MILL.", 60: "JACKPOT 2.5 MILL.", 61: "JACKPOT 3 MILL.",
	62: "JACKPOT 4 MILL.", 63: "JACKPOT 5 MILL.", 64: "NOT USED",
}
FOLDED_LAMP_NAMES = frozenset({3, 4, 5, 6, 7, 58, 60, 63})
LAMP_COLUMN_WIRING = {
	1: ("YEL-BRN", "1J7-1", "Q66"), 2: ("YEL-RED", "1J7-2", "Q64"), 3: ("YEL-ORN", "1J7-3", "Q62"),
	4: ("YEL-BLK", "1J7-4", "Q60"), 5: ("YEL-GRN", "1J7-6", "Q58"), 6: ("YEL-BLU", "1J7-7", "Q56"),
	7: ("YEL-VIO", "1J7-8", "Q54"), 8: ("YEL-GRY", "1J7-9", "Q52"),
}
LAMP_ROW_WIRING = {
	1: ("RED-BRN", "1J6-1", "Q80"), 2: ("RED-BLK", "1J6-2", "Q81"), 3: ("RED-ORN", "1J6-3", "Q82"),
	4: ("RED-YEL", "1J6-5", "Q83"), 5: ("RED-GRN", "1J6-6", "Q84"), 6: ("RED-BLU", "1J6-7", "Q85"),
	7: ("RED-VIO", "1J6-8", "Q86"), 8: ("RED-GRY", "1J6-9", "Q87"),
}
# Playfield G.I.: the bulb primitive under every GIBulbN light of the retained GIBulbs collection, plus the bulb-mesh
# light in each jet bumper cap (GIBumperLights).
GI_BULBS = (
	("pBulb3 (GIBulb1)", (200.8505, 1770.3907)), ("pBulb24 (GIBulb2)", (51.3096, 1333.9236)),
	("pBulb9 (GIBulb3)", (195.7371, 1638.8982)), ("pBulb1 (GIBulb4)", (162.1292, 1570.3989)),
	("pBulb27 (GIBulb5)", (50.069, 1184.4529)), ("pBulb25 (GIBulb6)", (49.7146, 1085.7936)),
	("pBulb4 (GIBulb7)", (658.2485, 1770.8356)), ("pBulb6 (GIBulb8)", (660.6439, 1643.4591)),
	("pBulb7 (GIBulb9)", (690.2316, 1549.1819)), ("pBulb29 (GIBulb10)", (842.6863, 1288.7249)),
	("pBulb16 (GIBulb11)", (842.9403, 1099.7227)), ("pBulb19 (GIBulb12)", (740.3066, 998.2328)),
	("pBulb17 (GIBulb13)", (857.5576, 958.2907)), ("pBulb18 (GIBulb14)", (738.1997, 871.2863)),
	("pBulb33 (GIBulb15)", (856.7675, 771.4264)), ("pBulb26 (GIBulb16)", (49.664, 986.7797)),
	("pBulb30 (GIBulb17)", (35.9614, 855.1535)), ("pBulb31 (GIBulb18)", (383.1751, 851.9863)),
	("pBulb32 (GIBulb19)", (493.4961, 852.0261)), ("pBulb43 (GIBulb20)", (268.1575, 370.9432)),
	("pBulb44 (GIBulb21)", (367.7326, 371.2553)), ("pBulb42 (GIBulb22)", (468.6956, 371.2553)),
	("pBulb41 (GIBulb23)", (570.1436, 368.4459)), ("pBulb14 (GIBulb24)", (622.5783, 388.7843)),
	("pBulb15 (GIBulb25)", (621.5247, 449.8872)), ("pBulb20 (GIBulb27)", (833.5412, 559.1876)),
	("pBulb40 (GIBulb28)", (54.8572, 217.215)), ("pBulb39 (GIBulb29)", (249.4523, 186.8789)),
	("pBulb38 (GIBulb30)", (453.0534, 137.2012)), ("pBulb37 (GIBulb31)", (575.2201, 143.0149)),
	("pBulb36 (GIBulb32)", (744.8333, 197.27)), ("pBulb35 (GIBulb33)", (855.9774, 268.3812)),
	("pBulb34 (GIBulb34)", (901.8045, 383.2124)),
	("l52b (left jet bumper cap)", (369.8499, 567.0652)), ("l53b (right jet bumper cap)", (573.324, 568.545)),
	("l54b (lower jet bumper cap)", (471.9568, 752.0416)),
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Mousin' Around retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Mousin' Around extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Mousin' Around retained extraction manifest is missing: {manifest_path}")
	if _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Mousin' Around retained extraction manifest is not the pinned one: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Mousin' Around retained extraction manifest does not match the extracted files")
	if len(actual["files"]) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"Mousin' Around retained extraction file count mismatch: {len(actual['files'])} != {EXTRACTION_FILE_COUNT}")
	if sum(item["size"] for item in actual["files"]) != EXTRACTION_TOTAL_BYTES:
		raise RuntimeError("Mousin' Around retained extraction byte count does not match the pinned total")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def placement(identifier: str, role: str, xy: tuple[float, float], status: str, *refs: str) -> dict[str, Any]:
	x, y = norm(*xy)
	return {"id": identifier, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs, status=status)}


def located(identifier: str, role: str, points: list[tuple[float, float]], status: str, *refs: str) -> dict[str, Any]:
	placements = [
		placement(f"{identifier}.{role}" + (f".{index}" if len(points) > 1 else ""), role, xy, status, *refs)
		for index, xy in enumerate(points, start=1)
	]
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def output_id(address: int) -> str:
	if address in SOLENOID_LABELS:
		return f"device.{slug(SOLENOID_LABELS[address])}"
	return f"device.{slug(VIRTUAL_SOLENOIDS[address][0]) if address in VIRTUAL_SOLENOIDS else slug(solenoid_platform_label(address))}"


def solenoid_platform_label(address: int) -> str:
	if 33 <= address <= 36:
		return f"Unused Upper Flipper Slot {address}"
	if 37 <= address <= 44:
		return f"Unused Sound Overlay Slot {address}"
	raise KeyError(address)


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def _excerpt(identifier: str, locator: str, filename: str, transcribed_by: str = "curator, read from the rendered pages") -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	return {
		"id": identifier, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path),
		"method": "manual", "transcribed_by": transcribed_by, "reviewed": True,
	}


def _corpus_uri(repository: str, revision: str, relative_path: str) -> str:
	return f"{repository}/blob/{revision}/{quote(relative_path, safe='/')}"


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned PinmameGetGames catalog records for the four-driver mousn_* clone tree rooted at mousn_l4",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c lines 33-36 INITGAME macro, lines 45-47 disp16oneline (two sixteen-character CORE_SEG16 displays, "
				"display-memory starts 0 and 20, laid out side by side) and line 1122 INITGAME(mousn,GEN_S11B,disp16oneline,12,FLIP_SWNO(58,57),S11_LOWALPHA|"
				"S11_DISPINV,S11_MUXSW2): sxx.muxSol = 12, no sxx.ssSw entries, hw.display S11_LOWALPHA|S11_DISPINV and "
				"gameSpecific1 S11_MUXSW2; lines 1123-1177 the mousn_* ROM sets (with the commented-out l4c patch sets) and lines "
				"1179-1183 CORE_GAMEDEF(mousn,l4) and the three CORE_CLONEDEFs on machine driver s11a_one; src/wpc/s11.h "
				"S11_GAMEONSOL 23, the diagnostic switch numbers -7 to -4 and the S11_MUXSW2/S11_SNDOVERLAY flags; src/wpc/s11.c "
				"pia2a_r (line 372, the Country jumper W7), setSSSol (line 537) and its WMS ssSolNo table, updsol (line 558, the "
				"muxSol copy of the low solenoid byte to 25-32 while 12 is pulsed), pia0cb2_w (line 611, S11_GAMEONSOL), pia4a_r "
				"(line 644) returning core_getSwCol without inversion, SWITCH_UPDATE(s11) line 800 (S11_MUXSW2: core_setSw(2, "
				"core_getSol(muxSol))), MACHINE_INIT(s11) (line 827) output sizing and the mousn_ output-type block (lines 1037-1042: "
				"9 as a reverse #44 \"Backbox GI output\", 10 as a reverse #44 \"Playfield GI output\", 15-16 and 25-32 as #89 "
				"bulbs, commented \"Mux relay is solenoid #12\"); src/wpc/core.h CORE_FIRSTSSSOL 17, CORE_SSFLIPENSOL 23, "
				"CORE_FIRSTUFLIPSOL 33, CORE_FIRSTLFLIPSOL 45, CORE_FIRSTSIMSOL 49 and CORE_FIRSTCUSTSOL 51; src/wpc/core.c "
				"core_updateSw's FLIP_SWNO copy and synthetic 45-48; src/wpc/gen.h GEN_S11B = GEN_S11X (0x100)"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
			"locator": "System 11 sequential switch/lamp matrices, dedicated diagnostic inputs, the Country jumper, the A/C mux alias bank, the S11_MUXSW2 switch-2 copy, special solenoids, the sound-overlay range, synthetic flipper outputs and the 81-88 flipper column",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "https://web.archive.org/web/20250904073734id_/https://www.ipdb.org/files/1635/Bally_1989_Mousin_Around_Manual.pdf",
			"original_filename": "Bally_1989_Mousin_Around_Manual.pdf",
			"sha256": MANUAL_SHA256, "acquired_at": "2026-10-31T08:26:10Z", "source_id": "ipdb.1635",
			"locator": (
				"IPDB machine 1635 (Mousin' Around!, Midway Manufacturing Company under the Bally name, model number 2009, MPU "
				"\"Williams System 11B\", manufactured November 20, 1989, 2,996 units; machine page https://www.ipdb.org/machine.cgi?id=1635, "
				"read through https://web.archive.org/web/20251204104221id_/https://www.ipdb.org/machine.cgi?id=1635, retained "
				f"capture SHA-256 {IPDB_PAGE_SHA256}; resource https://www.ipdb.org/files/1635/Bally_1989_Mousin_Around_Manual.pdf) "
				"downloaded through the Wayback Machine: the 120-page image-only MOUSIN' AROUND manual (© 1989 Midway "
				"Manufacturing Company; instruction manual part 16-2009-101). Pages were found with a Windows OCR pass and read from "
				"renders. PDF 4 game rules; PDF 8 connector identification (System 11B); PDF 40-47 Test/Diagnostic Procedures; PDF "
				"68-71 slingshot, feeder, outhole, shooter, trough, knocker, ball eater, drop kick and diverter assemblies; PDF 80-85 "
				"the Lamp Matrix, Playfield Lamp Locations, Switch Matrix, Switches list, Solenoid Table and Solenoid/Flashers list "
				"with their numbered location drawings."
			),
			"license": "NOASSERTION", "attribution": "Bally Midway Mfg. Co.; hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.mousin-around.switch-matrix", "PDF page 82 (printed Switches 2-28), Switch Matrix table and wiring drawing", "switch-matrix.md"),
				_excerpt("excerpt.mousin-around.lamp-matrix", "PDF page 80 (printed Lamps 2-26), Lamp Matrix table and wiring drawing", "lamp-matrix.md"),
				_excerpt("excerpt.mousin-around.solenoid-table", "PDF page 84 (printed Solenoid 2-30), Solenoid Table and its notes", "solenoid-table.md"),
				_excerpt("excerpt.mousin-around.switch-locations", "PDF page 83 (printed Switches 2-29), Switches parts list, note and drawing callouts", "switch-locations.md"),
				_excerpt("excerpt.mousin-around.lamp-locations", "PDF page 81 (printed Lamp 2-27), Playfield Lamp Locations list, note and drawing callouts", "lamp-locations.md"),
				_excerpt("excerpt.mousin-around.solenoid-flasher-locations", "PDF page 85 (printed Solenoids 2-31), Solenoid/Flashers list, note and drawing callouts", "solenoid-flasher-locations.md"),
				_excerpt("excerpt.mousin-around.mechanism-assemblies", "PDF pages 68-71 (printed 2-14 to 2-17), mechanism assembly parts lists", "mechanism-assemblies.md"),
				_excerpt("excerpt.mousin-around.diagnostics-and-operation", "PDF pages 4, 8, 40 and 47, game rules, System 11B identification and Test/Diagnostic Procedures", "diagnostics-and-operation.md"),
			],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(RUNTIME_EVIDENCE_PATH), "acquired_at": RUN_AT["mousn_l4"],
			"locator": (
				"Pinned LibPinMAME runs of mousn_l4, each from a new state directory inheriting only the retained initialization "
				"run's NVRAM: the Coil Test paired step by step with the name the ROM displays, the Single Lamps test stepped through "
				"designators 01-64 with the Credit button, the Switch Levels test over public 1-64 and 81-88, the C-Side test, three "
				"Motor Bank Test runs, sixteen power-up probes with switches held from start and a gameplay run. Every display "
				"reading cited is pinned in tools/seeds/bally/mousin-around-1989-frame-readings.json by the SHA-256 of the frame's "
				"segments. The local mousn_l4 archive carries the game ROMs the pinned source names but L-1 sound ROMs at U4 and U19 "
				"(CRCs 643add1e and 7b4941f7 where the pinned set names d311db4a and c7a6f494); no sound evidence is used. Raw runs, "
				"manifest and hashes are retained outside the repository."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external",
		},
	] + [
		{
			"id": variant_source(game), "kind": "runtime_scenario", "uri": f"internal:{variant_evidence_path(game).relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(variant_evidence_path(game)), "acquired_at": RUN_AT[game],
			"locator": (
				f"Pinned LibPinMAME Coil, Single Lamps and Switch Levels runs of {game}, from its own initialized NVRAM, each compared "
				"name by name and address by address with the mousn_l4 run of the same test."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external",
		}
		for game in VARIANT_GAMES
	] + [
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/mousin-around-1989/source/" + quote("Mousin_ Around! (Bally 1989).vpx"),
			"original_filename": "Mousin_ Around! (Bally 1989).vpx", "sha256": TABLE_SHA256, "acquired_at": "2026-10-31T08:30:17Z",
			"locator": (
				"Retained known-working VPX recreation of the physical machine by Herweh (\"Development by Herweh 2019 for Visual "
				"Pinball 10\", \"Version 1.0\", per the script header), copied from the contributor's table collection. Exact "
				f"playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority for "
				"script-bound table objects, read against the manual's numbered location drawings."
			),
			"license": "NOASSERTION", "attribution": "Herweh and the contributors credited in the script", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/mousin-around-1989/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Retained embedded script (1,796 lines). Runtime authority: cGameName = \"mousn_l4\" (line 126), LoadVPM "
				"\"01560000\", \"S11.VBS\", 3.26 (line 139) with HandleMechanics and HandleKeyboard off (lines 164-165), "
				"vpmNudge.TiltSwitch = 1 (line 186), the three-ball bsTrough on 11, 12 and 13 (lines 191-196), SolCallback 1-5, 7, 8, "
				"10, 11, 13, 14, 16, 22, the flipper callbacks and the flashers 15 and 25-32 (lines 304-329), Drain_Hit (347-353), "
				"the slingshots (407, 424), the kickback (444-458), the top gate (464), the standup targets (473-500, 551), the "
				"rollovers and ramp switches (503-549), the mouse hole (589-600), the two traps (615-708), the diverter (709-745), "
				"the motor bank (751-821), the lamp and flasher tables (830-916) and SolGI (1188-1204)."
			),
			"license": "NOASSERTION", "attribution": "Herweh and the contributors credited in the script", "rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads (script.vbs line 139 LoadVPM \"01560000\", \"S11.VBS\", 3.26), "
				f"retained with core.vbs (SHA-256 {VPM_CORE_SHA256}). S11.VBS defines swLRFlip = 82 and swLLFlip = 84 and sets them "
				"from the flipper keys in vpmKeyDown/vpmKeyUp, which the table's key handlers call; core.vbs names the synthetic "
				"flipper outputs sLRFlipper = 46 and sLLFlipper = 48."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.mousin-around.vpm-script-library-flippers", "s11.vbs lines 37-40, 69-80 and 104-115; core.vbs lines 2862-2863; script.vbs lines 139, 164-165, 237-244, 258-260 and 318-319", "vpm-script-library-flippers.md", transcribed_by="curator, read from the library and script files"),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/mousin-around-1989/extracted-vpxtool.manifest.json",
			"sha256": EXTRACTION_MANIFEST_SHA256, "acquired_at": "2026-10-31T08:30:29Z",
			"locator": (
				f"Retained vpxtool git:v0.33.3 extraction of the retained table, {EXTRACTION_FILE_COUNT} files and "
				f"{EXTRACTION_TOTAL_BYTES} bytes, with a full sorted path/size/SHA-256 manifest whose own SHA-256 is this record's "
				f"sha256. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_CORPUS_SOURCE, "kind": "vpx_script",
			"uri": _corpus_uri("https://github.com/sverrewl/vpxtable_scripts", VPXTABLE_REVISION, CORPUS_NAME),
			"revision": VPXTABLE_REVISION, "sha256": CORPUS_SHA256,
			"locator": (
				"Pinned corpus script of a later edit of the same Herweh table (header \"Original Development by Herweh 2019\", VR "
				"room and VPW physics updates through version 2.1, here with a further ball-velocity patch): Const cGameName = "
				"\"mousn_l4\" (line 141), LoadVPM \"01560000\", \"S11.VBS\", 3.26 (line 161), vpmNudge.TiltSwitch = 1 (line 188), "
				"the same Controller.Switch(57)/(58) key writes (lines 320-377) and SolCallback entries for the same addresses, 1-5, 7, 8, 10, 11, "
				"13, 14, 16, 22, the flippers and the flashers 15 and 25-32 (lines 392-418). It corroborates the retained script's "
				"bindings without being independent of it."
			),
			"license": "NOASSERTION", "attribution": f"Authors credited in {CORPUS_NAME} and repository contributors",
		},
		{
			"id": VPX_STANDALONE_SOURCE, "kind": "vpx_script",
			"uri": _corpus_uri("https://github.com/jsm174/vpx-standalone-scripts", STANDALONE_REVISION, STANDALONE_NAME),
			"revision": STANDALONE_REVISION, "sha256": STANDALONE_SHA256,
			"locator": (
				"Pinned standalone copy of the same version 2.1 script, differing from the vpxtable_scripts copy in whitespace, a "
				"cabinet-mode test, one parenthesized SolGI test and the absent ball-velocity patch: Const cGameName = \"mousn_l4\" (line 141), LoadVPM (line 161) "
				"and the same SolCallback entries (lines 391-417). The retained SHA-256 is the repository checkout's CRLF "
				"materialization; the linked Git blob is the identical LF-normalized text "
				f"(SHA-256 {STANDALONE_LF_SHA256})."
			),
			"license": "NOASSERTION", "attribution": f"Authors credited in {STANDALONE_NAME} and repository contributors",
		},
	]


def _switch_wiring(column: int, row: int) -> dict[str, Any]:
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "System 11B CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "driver_transistor": f"column {drive_component}",
	}


RUNTIME_SWITCH_NOTE = (
	" In the ROM's Switch Levels test (run switch-levels) holding public {address} at 1 makes the upper display show the ROM's "
	"name for it and the lower display \"06 {address:02d}\", so the ROM reads it active at 1. mousnGameData has no inverted-switch "
	"mask and pia4a_r returns core_getSwCol raw, so the contact the matrix sees is open at rest and closed when actuated."
)
# Behaviour each switch showed in the runs, appended to its note.
SWITCH_RUNTIME = {
	9: "With 9 held from power-up the ROM fired the outhole kicker (1) ten times in 12 s (power-up probe).",
	11: "With 11, 12 and 13 all held from power-up the ROM gave only its power-up pulse and ran no ball search, whatever else was held (power-up probes).",
	12: "See switch 11.",
	13: "See switch 11.",
	29: "See switch 31.",
	30: "See switch 31.",
	31: "In the gameplay run closing it as the third center target energized the Motor Relay (11) 0.025 s later, lowering the bank.",
	33: (
		"It is closed while the trap is down: in the gameplay run, once MOUSE TRAP was spelled, the ROM pulsed Trap 1 Up (3) "
		"while the host held 33 closed and stopped once it opened, and at power-up the ROM's ball search pulses Trap 1 Down (5) "
		"while 33 is open and Trap 1 Up instead while it is held (power-up probes). The retained script closes it when its trap "
		"goes down."
	),
	34: (
		"It is closed while the trap is down: the ROM pulses Trap 2 Up (4) while it is held and Trap 2 Down (8) in its ball search "
		"while it is open (gameplay run and power-up probes), as for switch 33."
	),
	43: (
		"The manual's Motor Test says switch 43 tells the CPU the bank is up. In the Motor Bank Test runs the motor relay "
		"released 0.08 s after the host closed 43 while the lower display read \"UP 00 09\", and the display read \"DN 01 "
		"ERROR\" after a 7.6 s run in which 50 never closed."
	),
	49: (
		"With 49 held from power-up the ROM pulsed the diverter (14) at 0.21, 2.67 and 3.42 s, where with 49 open its ball search "
		"pulses it seven times up to 8.1 s (power-up probes)."
	),
	50: (
		"The manual's Motor Test says switch 50 tells the CPU the bank is down. In the gameplay run the motor relay released "
		"0.27 s after the host closed 50, and in the Motor Bank Test it released 0.09 s after the host closed 50."
	),
	51: "In the gameplay run its closure fired the kickback (13) 0.012 s later.",
	52: "In the gameplay run its closure fired the left jet bumper (17) 0.004 s later.",
	53: "In the gameplay run its closure fired the right jet bumper (19) 0.003 s later.",
	54: "In the gameplay run its closure fired the lower jet bumper (21) 0.001 s later.",
	55: "In the gameplay run its closure fired the left slingshot (18) 0.015 s later.",
	56: "In the gameplay run its closure fired the right slingshot (20) 0.014 s later.",
	59: (
		"In the gameplay run its closure made the ROM energize the motor relay (11) 0.49 s later and fire the Mouse Hole Exit "
		"(16) 0.93 s later; with 59 held from power-up the ROM fired 16 six times from 1.97 s to 10.97 s, about 1.8 s apart, "
		"where with 59 open its ball search fires it once (power-up probes)."
	),
}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role) in DEDICATED_LABELS.items():
		refs: tuple[str, ...] = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE) if address in (-7, -6) else (CONTROLLER_SOURCE, CORE_SOURCE)
		notes = "System 11 diagnostic input on the S11_COMINPORT keyboard port."
		if address in (-7, -6):
			notes += (
				" The manual's Test/Diagnostic Procedures enter and step every test with the ADVANCE button and the "
				"AUTO-UP/MANUAL-DOWN switch, and the retained runs enter and step the tests with -6 and -7."
			)
		else:
			notes += " The excerpts transcribed for this record do not name this switch; it is the platform's CPU-board diagnostic input."
		items.append(_device(
			f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used", refs,
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}], roles=[role], normally_closed=False,
			physical={"location": "coin door and CPU board diagnostic switches", "switch_type": "button", "notes": notes},
			spatial=not_applicable("cabinet_or_service", CORE_SOURCE, CONTROLLER_SOURCE),
		))
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"switch.matrix-{address}"
		unused = address in UNUSED_SWITCHES
		label = f"Not Used (Matrix Position {address})" if unused else SWITCH_LABELS[address]
		physical: dict[str, Any] = {}
		notes = f"Printed switch-matrix column {column} ({SWITCH_COLUMN_WIRING[column][0]}), row {row} ({SWITCH_ROW_WIRING[row][0]})."
		notes += f" The ROM's Switch Levels test names it \"{ROM_SWITCH_NAMES[address]}\"."
		if unused:
			notes += " The Switch Matrix prints \"Not Used\" here and the Switches parts list prints \"Not Used\" with no part."
			if address == 48:
				notes += (
					" Every ROM the record holds (LA-4, LA-1 and LU-1) still names it \"MADE LEFT RAMP\", which LA-4 also calls "
					"switch 37, the manual's Left Ramp Exit; the retained table never writes 48. The ROM's name proves only that it "
					"scans the position, not that a switch is fitted, so the manual's \"Not Used\" stands."
				)
			else:
				notes += " The Switch Levels test still reports a closure here as \"NOT USED\", so the ROM scans the position; no switch is fitted."
		else:
			if address in SWITCH_PARTS:
				physical["part_number"] = SWITCH_PARTS[address]
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			elif address in SWITCH_PARTS and SWITCH_PARTS[address].startswith(MICROSWITCH_PARTS):
				physical["switch_type"] = "microswitch"
				notes += MICROSWITCH_NOTE
			elif address == 49:
				physical["switch_type"] = "microswitch"
				notes += " The C-12902-1 Ball Deflector assembly (printed 2-17) lists it as item 13, A-12953 \"Mini µSwitch Assy.\"."
			if address != 2 and address in MATRIX_WORDING and MATRIX_WORDING[address] != label:
				notes += f" The Switch Matrix prints \"{MATRIX_WORDING[address]}\"."
			if address != 2 and address in PARTS_LIST_WORDING and PARTS_LIST_WORDING[address] != label:
				notes += f" The Switches parts list prints \"{PARTS_LIST_WORDING[address]}\"."
			if address == 2:
				notes += (
					" The Switch Matrix and the Switches parts list both print \"Not Used\" at 2, and the ROM's Switch Levels name "
					"is \"NOT USED\", but the manual's C-SIDE TEST checks a \"C-Side Switch\" that shows whether the Solenoid A/C "
					"Select Relay (12) is in its C position, and reports \"Err\" when it fails. mousnGameData sets S11_MUXSW2, so "
					"pinned SWITCH_UPDATE(s11) overwrites public switch 2 with the live state of solenoid 12 on every update: a "
					"recreation reads it and never drives it, whichever matrix position the relay contact is wired to. In the ROM's "
					"C-Side test (run c-side-test, title \"C-SIDE SW. TEST\", lower display 08) the ROM energized 12 five times for "
					"about 1.93 s, 1.85 s apart; 0.2 s after every rise the upper display read \"SELECTED C-SIDE\" and the lower "
					"\"C-SIDE 08\", and after every fall \"SELECTED A-SIDE\" and \"08\", so the ROM reads 2 closed while 12 is "
					"energized. The Switch Levels test showed \"NOT USED\" for 2 only while the harness rewrote it to 1 on every poll."
				)
			if address == 5:
				notes += (
					" The Switches parts list prints \"Not Used\" in the part-number column of item 5 (Center Coin Sw.), while the "
					"Switch Matrix names the position and the ROM names and reads it, so it is recorded optional: the parts list fits "
					"no switch there, and a coin door with a center chute would close it."
				)
			if address == 11:
				notes += (
					" The Ball Trough Switches page (printed 2-16) lists the right trough switch as A-11680 with a 5647-12073-08 "
					"Submini Switch and a 1N4001 diode, where the Switches parts list prints 5647-12073-00; the part number follows "
					"the parts list."
				)
			if address in (12, 13):
				notes += " The Ball Trough Switches page prints \"µswitch; Cntr & L Ball Trough\" for this part, with a 1N4001 diode."
			if address in (17, 18, 19, 20, 21, 25, 26, 27, 28):
				notes += " One of the nine MOUSE TRAP standups; the rules say spelling M-O-U-S-E T-R-A-P sets the traps that lock the balls."
			if address in (29, 30, 31):
				notes += (
					" One of the three targets of the motorized center bank; the rules say hitting them in sequence lowers the bank "
					"and lights the kickback."
				)
			if address in (33, 34, 41, 42):
				notes += (
					" The Switches note: \"Each Ball Eater has two switches. The center is #41 & #42 and tells the CPU if a ball is "
					"in the Ball Eater. The switch to the back and side is #33 & #34 and tells the CPU if the Ball Eater is up or "
					"down.\" Trap 1 is the right ball eater (its lamp 33 Set Trap 1 and its coils 03A and 05A stand on the right "
					"edges of the drawings) and Trap 2 the left."
				)
			if address in (43, 50):
				notes += (
					" The Switches note: \"The Motorized Target also has two switches. The right side switch tells the CPU the target "
					"is down, the left side switch tells the CPU the target is up.\""
				)
			if address == 36:
				notes += (
					" The Switches list prints its part B-11696-6 as \"Playfield Multiply\"; the ROM calls the same address \"RIGHT "
					"STANDUP\". The switch drawing's right edge puts 36 just above the T standup (25), where the lamp drawing's right "
					"edge puts lamp 47 \"Right Stand-up\" just above lamp 25."
				)
			if address == 37:
				notes += (
					" The LA-1 and LU-1 ROMs name this address \"RAMP DRAIN\" (variant runs); LA-4 calls it \"MADE LEFT RAMP\", the "
					"manual \"Left Ramp Exit\"."
				)
			if address == 51:
				notes += " The ROM calls it \"KICKBACK\": the left outlane carries the kickback (13, \"Kickback (L Outlane)\")."
			if address in (55, 56):
				notes += (
					f" The Switches list prints two parts for this slingshot: item {address}, SW-1A-114 \"(kicker)\", and item "
					f"{address}a, SW-1A-120 \"(score)\"; both carry this one matrix number."
				)
			if address in (59, 60, 61):
				notes += " Part of the C-13061 mouse hole lock on the back panel; the drop kick (16) releases the locked balls."
			if address in (57, 58):
				side = "right" if address == 57 else "left"
				button = 82 if address == 57 else 84
				notes += (
					f" It senses the {side} cabinet flipper switch (03-7811 in the Switches list); the flipper button fires the coil "
					"through the flipper circuit itself (Solenoid Table note 1: the Orn-Vio and Orn-Gry wires \"connect from CPU Board "
					"to flipper switch\"). mousnGameData's FLIP_SWNO(58,57) without FLIP_SOL makes core_updateSw rewrite this address "
					f"from PinMAME's flipper column, public {button}, on every update, so a consumer cannot drive it directly: it drives "
					f"{button}, and the Switch Levels test shows \"{ROM_SWITCH_NAMES[address]}\" and \"06 {address}\" while {button} is "
					f"held. The retained script also writes Controller.Switch({address}) from the {side} flipper key (lines 237-238 and "
					"258-259), which PinMAME overwrites on its next update, a defect with no effect."
				)
			if address in SWITCH_RUNTIME:
				notes += " " + SWITCH_RUNTIME[address]
			if address != 2:
				notes += RUNTIME_SWITCH_NOTE.format(address=address)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": _switch_wiring(column, row),
		}
		refs = (MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if unused:
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE)
		elif address == 2:
			availability = "used"
			extra["roles"] = ["internal.ac-relay-feedback"]
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address in CABINET_SWITCH_ROLES:
			availability = "optional" if address == 5 else "used"
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			if address in (57, 58):
				refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, VPM_LIBRARY_SOURCE)
		else:
			availability = "used"
			extra["normally_closed"] = False
			refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in SWITCH_PROJECTIONS:
				xy, reason = SWITCH_PROJECTIONS[address]
				extra["spatial"] = located(identifier, "sensor", [xy], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
				notes += " " + reason
			else:
				obj, xy = SWITCH_OBJECTS[address]
				extra["spatial"] = located(identifier, "sensor", [xy], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
				notes += f" Placed at the retained table's {obj}, which the script binds to this address."
				if address in SWITCH_OBJECT_NOTES:
					notes += " " + SWITCH_OBJECT_NOTES[address]
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	column = flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP_SWNO(58,57)",
		core_refs=(CORE_SOURCE, CONTROLLER_SOURCE), button_refs=(VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE),
		button_notes={
			side: (
				f"The retained known-working script drives it: MousinAround_KeyDown and MousinAround_KeyUp pass the {side} flipper "
				"key to S11.VBS vpmKeyDown/vpmKeyUp (script lines 244 and 260), which set "
				f"Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} (excerpt vpm-script-library-flippers). In the Switch Levels "
				f"run holding this address showed \"{'LEFT FLIPPER' if side == 'left' else 'RIGHT FLIPPER'}\" and "
				f"\"06 {58 if side == 'left' else 57}\". The physical counterpart is the {side} cabinet flipper switch, which fires the "
				"flipper coil through the flipper circuit and is read by the CPU at its matrix address."
			)
			for side in ("left", "right")
		},
		unused_notes=vpm_staged_flipper_notes(), unused_note_refs=(VPM_LIBRARY_SOURCE,),
	)
	for item in column:
		if item["availability"] == "used":
			item["normally_closed"] = False
	items.extend(column)
	items.append(_device(
		"switch.dip-0", "Country Jumper (W7)", "dip_switch", "pinmame.input.dip", 0, "used",
		(CONTROLLER_SOURCE, CORE_SOURCE),
		aliases=[{"namespace": "pinmame.dip", "value": "0"}],
		physical={
			"location": "System 11B CPU board", "switch_type": "dip",
			"notes": (
				"System 11's single Country jumper, read via core_getDip(0)<<7 on PIA2 PA7 (pinned s11.c labels it \"Jumper W7\"). "
				"The excerpts transcribed for this record do not cover the manual's jumper table."
			),
		},
		spatial=not_applicable("dip_switch", CORE_SOURCE),
	))
	return items


# Behaviour each output showed in the runs, appended to its note.
SOLENOID_RUNTIME = {
	1: (
		"In the gameplay run the ROM fired it 0.56 s after the drained ball closed the outhole switch (9); with 9 held from "
		"power-up it fired ten times in 12 s, and with no ball anywhere the ROM's ball search pulses it twice (power-up probes)."
	),
	2: (
		"In the gameplay run the ROM fired it 0.42 s after game-on (23) rose at Start, and twice more (76.54 and 78.51 s) as it "
		"served ball 2."
	),
	3: (
		"In the gameplay run, once MOUSE TRAP was spelled, the ROM pulsed it four times about 0.8 s apart while switch 33 read "
		"closed (trap down) and stopped once 33 opened; with 33 and 34 held from power-up it pulsed six times (power-up probe)."
	),
	4: (
		"In the gameplay run, once MOUSE TRAP was spelled, the ROM pulsed it four times about 0.8 s apart while switch 34 read "
		"closed (trap down) and stopped once 34 opened; with 33 and 34 held from power-up it pulsed six times (power-up probe)."
	),
	5: "At power-up with switch 33 open the ROM's ball search pulses it six times 0.8 s apart, and never while 33 is held closed (power-up probes).",
	8: "At power-up with switch 34 open the ROM's ball search pulses it six times about 0.8 s apart, and never while 34 is held closed (power-up probes).",
	11: (
		"In the gameplay run the third center target (31) energized it 0.025 s later and it released 0.27 s after the host "
		"closed the bank-down switch 50; the closure of mouse hole lock 1 (59) energized it again 0.49 s later. In the Motor "
		"Bank Test it released 0.09 s after the host closed 50 and 0.08 s after the host closed 43, and with neither switch "
		"closing it stayed on for 15.2 s before the display read \"00 ERROR\". At power-up with an empty trough the ROM ran it "
		"for 7.6-7.9 s at a time while neither limit changed (power-up probes)."
	),
	12: (
		"The ROM energizes it ahead of every C-side step of the Coil Test and releases it for every A-side step; in the C-Side "
		"test it energized it five times for about 1.93 s, 1.85 s apart (run c-side-test)."
	),
	13: "In the gameplay run the ROM fired it 0.012 s after the kickback lane switch (51) closed.",
	14: (
		"In the gameplay run the ROM pulsed it 24 times; at power-up with an empty trough its ball search pulses it seven times "
		"up to 8.1 s, and only at 0.21, 2.67 and 3.42 s with the diverter switch (49) held (power-up probes)."
	),
	15: "In the gameplay run the ROM pulsed it eight times between power-up and 49.5 s.",
	16: (
		"In the gameplay run the ROM fired it 0.93 s after mouse hole lock 1 (59) closed; with 59 held from power-up it fired "
		"six times from 1.97 s to 10.97 s, about 1.8 s apart (power-up probes)."
	),
	17: "In the gameplay run the ROM fired it 0.004 s after switch 52 closed.",
	18: "In the gameplay run the ROM fired it 0.015 s after switch 55 closed.",
	19: "In the gameplay run the ROM fired it 0.003 s after switch 53 closed.",
	20: "In the gameplay run the ROM fired it 0.014 s after switch 56 closed.",
	21: "In the gameplay run the ROM fired it 0.001 s after switch 54 closed.",
	22: "In the gameplay run the ROM energized it 2.8 s after the first ball was served and held it until ball 2 was being served.",
}


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	pair_of = {a: pair for pair, (a, c, *_rest) in AC_PAIRS.items() for a in (a, c)}
	for address in list(range(1, 23)) + list(range(25, 33)):
		identifier = output_id(address)
		label = SOLENOID_LABELS[address]
		kind = SOLENOID_KIND[address]
		number = SOLENOID_MANUAL_NUMBER[address]
		step = COIL_TEST_ORDER.index(address) + 1
		notes = f"Solenoid Table entry {number} (\"{SOLENOID_TABLE_WORDING[address]}\")"
		if LIST_WORDING[address] != SOLENOID_TABLE_WORDING[address]:
			notes += f"; the Solenoid/Flashers list prints \"{LIST_WORDING[address]}\""
		notes += "."
		if address in pair_of:
			pair = pair_of[address]
			a_side, c_side, cpu, power_a, power_c, driver, cpu_bracket = AC_PAIRS[pair]
			notes += (
				f" Switched pair {pair:02d}A/{pair:02d}C on driver {driver}: the \"A\" load is pulsed with the A/C Select Relay (12) "
				f"de-energized and the \"C\" load with it energized (the table's note 3). Pinned updsol publishes the A load at "
				f"{a_side} and the C load at {c_side}."
			)
			wiring = {
				"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": SOLENOID_WIRE[address],
				"control_connection": cpu if address == a_side else f"{cpu} (C side, through the A/C Select Relay)",
				"power_connection": power_a if address == a_side else power_c,
			}
			if address == c_side:
				notes += f" The table's CPU Bd column prints \"{cpu_bracket}\" on this row, the bracketed wire of note 3."
		else:
			cpu, power, driver = CONTROLLED[address]
			kind_word = "Controlled" if address <= 16 else f"Special #{address - 16}"
			notes += f" Solenoid Type \"{kind_word}\"."
			wiring = {
				"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": SOLENOID_WIRE[address],
				"control_connection": cpu, "power_connection": power,
			}
		notes += (
			f" The ROM's Coil Test (run coil-test) pulses this address at step {step} of {len(COIL_TEST_ORDER)} while the upper "
			f"display shows \"{ROM_COIL_NAMES[address]}\"."
		)
		if 17 <= address <= 22:
			notes += (
				" mousnGameData is a plain INITGAME with no sxx.ssSw entries, so PinMAME publishes this special solenoid only when "
				"the ROM drives its PIA line itself (setSSSol, WMS ssSolNo order); the Coil Test shows the printed Special numbers "
				"1-6 at public 17-22."
			)
		if address in SOLENOID_RUNTIME:
			notes += " " + SOLENOID_RUNTIME[address]
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
		else:
			notes += " The retained script has no callback for this address."
		physical: dict[str, Any] = {}
		if address in SOLENOID_PART:
			physical["part_number"] = SOLENOID_PART[address]
		if address in FLASHLAMP_QUANTITY:
			physical["quantity"] = FLASHLAMP_QUANTITY[address]
		extra_roles: list[str] = []
		spatial: dict[str, Any] | None = None
		availability = "used"
		handled = True
		refs: tuple[str, ...] = (MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		if address == 6:
			notes += (
				" The Solenoid Table prints \"Not Used\" with a blank part-number cell and the Solenoid/Flashers list prints item "
				"06A blank and \"Not Used\": no load is fitted on the A side of pair 06. The Coil Test names it \"NOT USED\" and is "
				"the only run that pulsed it, so the state PinMAME publishes here is that test's pulse."
			)
			availability = "unused"
			spatial = not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE)
		elif address == 7:
			notes += " The B-10686-1 Knocker Assembly (printed 2-16) carries its AE-23-800 coil; the drawing gives it no playfield callout."
			extra_roles = ["cabinet.knocker"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 9:
			notes += (
				" The insert-board G.I. relay (5580-09555-01 on Relay Board C-11998-1, the table's note 4a). Pinned PinMAME types it "
				"as a reverse-acting #44 \"Backbox GI output\", so energized means the insert-board general illumination is off."
			)
			extra_roles = ["gi.backbox"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 10:
			notes += (
				" The playfield G.I. relay (5580-09555-01 on Relay Board C-11998-1, the table's note 4a). Energized means G.I. off: "
				"pinned PinMAME types it as a reverse-acting #44 \"Playfield GI output\" and the retained script's SolGI(IsOff) "
				"turns its G.I. off while it is on. This record cites no G.I. bulb list or layout from the manual; the placements are "
				"the bulb under each light of the retained table's GIBulbs collection and the bulb-mesh light in each jet bumper "
				"cap (GIBumperLights). A table's G.I. grouping is not the machine's wiring, so these placements stay observed and no "
				"quantity is asserted."
			)
			extra_roles = ["gi.playfield"]
			spatial = located(identifier, "emitter", [xy for _, xy in GI_BULBS], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
			refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		elif address == 11:
			notes += (
				" The Motor Relay (5580-12145-01 on Relay Board C-11902-1, the table's note 4b) switches the motor that raises and "
				"lowers the three center targets; the ROM's Coil Test calls it \"STANDUP MOTOR\". The same relay output "
				"lowers and raises the bank: in the Motor Bank Test one span ended when 50 closed and the next, shown as \"UP\", "
				"when 43 closed."
			)
			handled = False
		elif address == 12:
			notes += (
				" The A/C select relay (5580-09555-01, note 5: \"Relay mounted on Aux. Power Driver Bd., D-12247\"). Pinned PinMAME "
				"publishes its own state here and, while it is pulsed, moves the low solenoid byte to 25-32; it also copies this "
				"state into switch 2 (S11_MUXSW2), the relay's C-side switch the ROM reads."
			)
			extra_roles = ["internal.ac-select-relay"]
			spatial = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 13:
			notes += " Rows 13 and 14 both print 5J2-4 as their first power connection; the render was checked and the digit is the same in each."
			handled = False
		elif address == 14:
			notes += " Rows 13 and 14 both print 5J2-4 as their first power connection; the render was checked and the digit is the same in each."
			handled = False
		elif address == 16:
			notes += (
				" The coil of the B-13081 Drop Kick Mech. Assembly \"(Mouse Hole Exit)\" (AE-26-1200, printed 2-17); the Solenoid/"
				"Flashers note says \"Solenoid #16 is on the Back Panel\". Pinned PinMAME's mousn_ output-type block types 15 and 16 "
				"as #89 bulbs, which is wrong for this coil."
			)
			handled = False
		elif address == 18:
			notes += (
				" The Solenoid/Flashers list prints AE-23-1500 for this coil, where the Solenoid Table and the slingshot assembly's "
				"associated parts (printed 2-14) print AE-26-1500; the part number follows the two agreeing pages."
			)
			handled = False
		elif address in UNPLACED_FLASHER_NOTES:
			notes += " " + UNPLACED_FLASHER_NOTES[address]
			spatial = None
		else:
			handled = False
		if not handled:
			if address not in SOLENOID_OBJECTS:
				raise RuntimeError(f"no spatial disposition for solenoid {address}")
			objects = SOLENOID_OBJECTS[address]
			role = "emitter" if kind in ("flasher", "gi", "lamp") else "effect"
			spatial = located(identifier, role, [xy for _, xy in objects], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
			if address in SOLENOID_PROJECTED:
				notes += f" Placed at the retained table's {objects[0][0]}, a documented projection onto {SOLENOID_PROJECTED[address]}."
			elif kind == "flasher":
				notes += " " + FLASHER_NOTES[address]
			else:
				notes += f" Placed at the retained table's {objects[0][0]}."
		if address == 7:
			extra_roles = ["cabinet.knocker"]
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": number}]
		if 17 <= address <= 22:
			aliases.append({"namespace": "manual.special-solenoid", "value": f"Special #{address - 16}"})
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		if extra_roles:
			extra["roles"] = extra_roles
		if spatial is not None:
			extra["spatial"] = spatial
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
	for address in (23, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
		if address in VIRTUAL_SOLENOIDS:
			label, availability, role, notes = VIRTUAL_SOLENOIDS[address]
		elif address <= 36:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", UPPER_FLIPPER_NOTE
		else:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", OVERLAY_NOTE
		refs = (CONTROLLER_SOURCE, CORE_SOURCE)
		if availability == "used":
			refs = (CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE) if address == 23 else (CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
		items.append(_device(
			f"device.{slug(label)}", label, "virtual", "pinmame.output.solenoid", address, availability, refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}], roles=[role], physical={"notes": notes},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"lamp.matrix-{address}"
		wiring = {
			"board": "System 11B CPU board",
			"drive_wire": LAMP_COLUMN_WIRING[column][0], "drive_connection": LAMP_COLUMN_WIRING[column][1],
			"return_wire": LAMP_ROW_WIRING[row][0], "return_connection": LAMP_ROW_WIRING[row][1],
			"driver_transistor": f"column {LAMP_COLUMN_WIRING[column][2]}, row {LAMP_ROW_WIRING[row][2]}",
		}
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		label = "Not Used (Lamp Matrix Position 64)" if address == 64 else LAMP_LABELS[address]
		notes = (
			f"Printed lamp-matrix column {column}, row {row}. In the Single Lamps test (run single-lamps) designator {address:02d} "
			f"blinks this address while the upper display shows \"{ROM_LAMP_NAMES[address]}\""
		)
		if address in FOLDED_LAMP_NAMES:
			notes += " (the display draws 5 and S, and 0 and O, with one glyph each; digits are read in the value)"
		notes += "."
		if address in LAMP_MATRIX_WORDING and LAMP_MATRIX_WORDING[address] != label:
			notes += f" The Lamp Matrix prints \"{LAMP_MATRIX_WORDING[address]}\"."
		if address in LAMP_LIST_WORDING and LAMP_LIST_WORDING[address] != label:
			notes += f" The Playfield Lamp Locations list prints \"{LAMP_LIST_WORDING[address]}\"."
		if address in (41, 44, 48):
			notes += " The Lamp Matrix prints a pair of bullets under the name and no legend for them."
		if address == 41 or address == 44:
			notes += f" The ROM calls it \"{ROM_LAMP_NAMES[address]}\"."
		if address == 48:
			notes += " The ROM calls it \"RIGHT RAMP\", so the label carries both names."
		refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {}
		availability = "used"
		if address == 64:
			notes += (
				" The Lamp Matrix prints \"Not Used\" and the lamp page's note says \"#64, Is Not Used\": no lamp is fitted. The "
				"Single Lamps test is the only run that drove it."
			)
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE)
			refs = (MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		elif 57 <= address <= 63:
			notes += (
				" The lamp page's note says \"#57-#63, Are on the Insert Board\": one of the seven jackpot values in the backbox. "
				f"The retained script drives its backglass light l{address} with SetValue (LampTimer, lines 843-877)."
			)
			extra["roles"] = ["cabinet.backglass-indicator"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif 49 <= address <= 56:
			notes += (
				" The lamp page's note says \"#49-#56, Are on the Back Panel\": the MILLION letters, printed in reverse order "
				"(N-O-I-L-L-I-M), and Build Jackpot stand on the back panel above the playfield. The retained table shows a "
				f"backboard Flasher decal l{address} for it (LampTimer and BackboardLampTimer, lines 843-889), not a bulb, so it marks no socket and the "
				"spatial key is omitted."
			)
		elif address == 8:
			notes += (
				" The lamp page lists it among the playfield lamps 1-48, but no callout on its drawing carries the number 8, and the "
				"retained table shows it as a backboard Flasher decal l8 together with the back-panel lamps 49-56 (LampTimer, lines "
				"843-889). Whether it is a playfield insert or a back-panel lamp no source settles; either way the table draws no "
				"bulb for it, so the spatial key is omitted."
			)
		else:
			notes += (
				" The retained table draws this insert with Light objects of its InsertLights collection (TimerInterval "
				f"{address}) that show no bulb and sit on no bulb primitive, so under the bulb-picking rule they mark no socket and "
				"the spatial key is omitted."
			)
		physical: dict[str, Any] = {"notes": notes}
		items.append(_device(
			identifier, label, "lamp", "pinmame.output.lamp", address, availability, refs,
			aliases=aliases, wiring=wiring, physical=physical, **extra,
		))
	return items


def displays() -> list[dict[str, Any]]:
	def display(identifier: str, label: str, index: int, start: int) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": "segment", "controller_index": index, "segment_start": start,
			"width": 16, "height": 1, "physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		}

	return [
		display("display.upper-alphanumeric", "Upper sixteen-character alphanumeric display (Player 1 and 2)", 0, 0),
		display("display.lower-alphanumeric", "Lower sixteen-character alphanumeric display (Player 3 and 4)", 1, 20),
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly:
			record["assembly_part_number"] = assembly
		return record

	m = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	return [
		mechanism(
			"mechanism.trough", "Outhole and three-ball trough", "kicker", [output_id(1), output_id(2)],
			["switch.matrix-9", "switch.matrix-13", "switch.matrix-12", "switch.matrix-11", "switch.matrix-14"],
			"A drained ball rests on the outhole switch (9) and the Outhole Kicker (1, B-8039-2, AE-23-800) kicks it into the "
			"trough, where up to three balls queue on Trough 3 (13, left), Trough 2 (12, middle) and Trough 1 (11, right; the ROM "
			"calls 11-13 TROUGH 1-3 BALL(S)). The Ball Shooter Lane Feeder (2, C-9638-1, AE-23-800) kicks the lead ball into the "
			"shooter lane (14). In the gameplay run the ROM fed the first ball 0.42 s after game-on rose and kicked the outhole "
			"0.56 s after 9 closed. With the trough empty at power-up the ROM runs a ball search through 1, 5, 8, 11, 14 and 16; "
			"with all three trough switches held it runs none. The retained script models the trough as one three-ball "
			"cvpmBallStack.",
			*m, assembly="C-9638-1 with B-8039-2",
		),
		mechanism(
			"mechanism.trap-1", "Trap 1 (right ball eater)", "other", [output_id(3), output_id(5)],
			["switch.matrix-33", "switch.matrix-41"],
			"A Trap (Ball Eater) Assembly (B-20-9629: the 20-9629 Ball Eater, an AE-26-1400 coil and an SM1-28-800 coil) on the "
			"right side. Trap 1 Up (3, AE-26-1400) raises the ball eater and Trap 1 Down (5, SM1-28-800) lowers it; switch 33 "
			"closes while it is down and switch 41 reports a ball in it. The rules: spelling M-O-U-S-E T-R-A-P sets the traps "
			"that lock the balls, two balls are trapped and the third releases them when it is put into play (Multi-ball); after "
			"Multi-ball the traps stay up and must trap the mice again for the Jackpot. In the gameplay run, once MOUSE TRAP was "
			"spelled, the ROM pulsed the up coil about every 0.8 s while 33 stayed closed and stopped once it opened; at "
			"power-up the ball search pulses the down coil while 33 is open. The retained script raises the trap with 3 and kicks "
			"out a ball resting in it, and lowers it with 5.",
			*m, assembly="B-20-9629",
		),
		mechanism(
			"mechanism.trap-2", "Trap 2 (left ball eater)", "other", [output_id(4), output_id(8)],
			["switch.matrix-34", "switch.matrix-42"],
			"The second B-20-9629 ball eater, on the left side: Trap 2 Up (4, AE-26-1400) raises it, Trap 2 Down (8, SM1-28-800) "
			"lowers it, switch 34 closes while it is down and 42 reports a ball in it. It behaves as Trap 1 in every run.",
			*m, assembly="B-20-9629",
		),
		mechanism(
			"mechanism.motor-bank", "Motorized center target bank", "motorized", [output_id(11)],
			["switch.matrix-43", "switch.matrix-50", "switch.matrix-29", "switch.matrix-30", "switch.matrix-31", "switch.matrix-35"],
			"Three center targets (29-31) on a motorized bank that the Motor Relay (11, 5580-12145-01) raises and lowers. Two "
			"limit switches on the motor (5647-12073-06) report its ends: 43 when the bank is up (the Switches note's left side "
			"switch) and 50 when it is down (the right side switch). The rules: hitting the center targets in sequence lowers "
			"the targets and lights the kickback. The retained table puts the Center Ramp switch (35) directly behind the bank, "
			"and its script makes the targets and a wall behind them non-collidable while the bank is down. The ROM releases "
			"the relay once the limit it is waiting for closes: in the gameplay run the third target energized it and it "
			"released 0.27 s after 50 closed, and the mouse hole lock energized it again; the Motor Bank Test raises and lowers "
			"the bank, released the relay 0.09 s after 50 and 0.08 s after 43 closed, and shows an error when a limit does not "
			"close (\"DN 01 ERROR\" after 7.6 s without 50, \"00 ERROR\" after 15.2 s with neither). The retained script "
			"moves the three target primitives over about 2 s each way and writes 43 and 50 at the ends.",
			*m,
		),
		mechanism(
			"mechanism.mouse-hole", "Mouse hole lock and drop kick (back panel)", "kicker", [output_id(16)],
			["switch.matrix-32", "switch.matrix-59", "switch.matrix-60", "switch.matrix-61"],
			"A shot enters the mouse hole past Mouse Hole Enter (32) and queues on Mouse Hole Lock 1-3 (59-61, part of C-13061) on "
			"the back panel; the Mouse Hole Exit (16, the B-13081 Drop Kick Mech. Assembly with an AE-26-1200 coil and the "
			"B-13082 ball tray) releases a ball. The rules: completing C-H-E-E-S-E opens the mouse hole to build the Jackpot, "
			"sending the last mouse home to the mouse hole after Multi-ball collects it, and spelling MILLION opens it for 1,000,000 "
			"points. In the gameplay run the ROM fired 16 0.93 s after 59 closed; with 59 held from power-up it fired it six "
			"times about 1.8 s apart. The retained script holds the ball in its MouseHole kicker while 59 is set.",
			*m, assembly="B-13081",
		),
		mechanism(
			"mechanism.diverter", "Ball diverter", "diverter", [output_id(14)], ["switch.matrix-49"],
			"The Ball Deflector (Diverter) C-12902-1 with its B-12858 Diverter Mech. Assembly: an AE-23-800 coil drives the A-12957-1 "
			"D/A shaft actuator through a flat cam, and the A-12953 Mini Switch (49) reports the diverter's position. The retained "
			"script names it SolMouseHoleDiverter: each pulse swings its arm, toggles switch 49 and with it which of two walls "
			"(WallDiverter or WallGuideToTop) is solid. At power-up with an empty trough the ball search pulses 14 seven times, "
			"three with 49 held.",
			*m, assembly="C-12902-1",
		),
		mechanism(
			"mechanism.kickback", "Left outlane kickback", "kicker", [output_id(13)], ["switch.matrix-51"],
			"A kickback (13, AE-24-900, \"Kickback (L Outlane)\") in the left outlane, whose switch (51) the ROM calls \"KICKBACK\". "
			"Lamp 36 (Kickback) shows it lit; the rules light it when the center targets lower. In the gameplay run the ROM fired 13 0.012 s after "
			"51 closed. The retained script enables its Kickback kicker while 13 is on.",
			*m,
		),
		mechanism(
			"mechanism.top-lanes-gate", "Top lanes gate", "gate", [output_id(22)],
			["switch.matrix-22", "switch.matrix-23", "switch.matrix-24"],
			"The Top Lanes Gate (22, Special #6, SM2-35-4000; the ROM's Coil Test calls it \"SHOOTER GATE\") above the three top "
			"lanes (22-24). The rules: a plunger skill shot through the lit top lanes scores 100,000 times the ball number, and "
			"completing the top lanes earns the 2X and 3X bonus multipliers. In the gameplay run the ROM energized the gate 2.8 s "
			"after the first ball was served and held it until ball 2 was being served. The retained script opens its GateTopRight "
			"while 22 is on.",
			*m,
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other", [output_id(17), output_id(19), output_id(21)],
			["switch.matrix-52", "switch.matrix-53", "switch.matrix-54"],
			"Three jet bumpers in the upper centre: Left (17, switch 52), Right (19, switch 53) and Lower (21, switch 54), each with "
			"an AE-23-800 coil and an SW-11A-37 skirt switch. They are special solenoids, but mousnGameData maps no switch to them "
			"in PinMAME: the ROM fires each through its PIA line, 0.001-0.004 s after its switch closed in the gameplay run, so a "
			"consumer drives only the switch.",
			*m,
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other", [output_id(18), output_id(20)], ["switch.matrix-55", "switch.matrix-56"],
			"Two B-12665 slingshot kickers above the flippers (AE-26-1500 coils): Left (18) with switch 55 and Right (20) with 56, "
			"each address carrying an SW-1A-114 kicker switch and an SW-1A-120 score switch. In PinMAME the ROM fires each special "
			"solenoid itself, 0.014-0.015 s after its switch closed in the gameplay run.",
			*m, assembly="B-12665",
		),
		mechanism(
			"mechanism.flippers", "Two flippers, cabinet-wired", "other", [], ["switch.matrix-58", "switch.matrix-57"],
			"Two flippers with FL11630/50VDC coils (the Solenoid Table's spelling; the list prints \"Fl 11630/50VDC\"). The cabinet flipper switches fire the coils through the flipper circuit, so "
			"no Sol. No. or driver is printed for them and PinMAME fabricates 45-48 from the buttons at public 82 and 84; the CPU "
			"reads the switches at 58 (left) and 57 (right), which core_updateSw copies from 84 and 82.",
			*m,
		),
		mechanism(
			"mechanism.ac-select", "A/C solenoid select relay", "other", [output_id(12)], ["switch.matrix-2"],
			"The A/C Select Relay (12) on the Aux Power Driver Board switches the solenoid supply between the \"A\" and \"C\" "
			"terminals so that each of the eight switched drivers (Q22-Q25, Q30-Q33) serves an \"A\" coil while it is released and "
			"a \"C\" flasher while it is energized. Pinned PinMAME publishes the C loads separately at 25-32 and copies the relay's "
			"state into switch 2, the C-side switch the ROM checks in its C-Side test.",
			MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Knocker", "other", [output_id(7)], [],
			"The A-side load of pair 07 (7, AE-23-800) raps the B-10686-1 Knocker Assembly.",
			MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly="B-10686-1",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.ac-relay-switch-2", "kind": "direct", "source": output_id(AC_RELAY), "destination": "switch.matrix-2",
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
	] + flipper_column_relationships(flip_swno=FLIP_SWNO, matrix_ids={57: "switch.matrix-57", 58: "switch.matrix-58"}, refs=(CORE_SOURCE, RUNTIME_SOURCE))


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items = []
	for driver_id in DRIVER_IDS:
		record = by_id[driver_id]
		item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		items.append(item)
	return items


COVERAGE_MISSING = ["variant_differences", "spatial_placement"]


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Mousin' Around!", "manufacturer": "Bally", "year": 1989, "kind": "physical_pinball",
			"model_number": "2009", "ipdb_id": 1635, "opdb_id": "G43oq-MJp02",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE)},
		},
		"coverage": {
			"status": STATUS,
			"missing": COVERAGE_MISSING,
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
				"physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "candidate",
				"recreation_knowledge": "validated", "display_inventory": "validated", "spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Mousin' Around device identifiers are not unique: {duplicates}")
	return definition


SPATIAL_BLOCKERS = [
	"Lamps 1-7 and 9-48: the retained table draws every playfield insert with Light objects that show no bulb and sit on no "
	"bulb primitive, so under the bulb-picking rule no insert has a socket and their spatial keys are omitted. A table that "
	"models the insert bulbs (the pinned corpus script of the later version 2.1 edit mentions 3D inserts, but that table is "
	"not retained), or a measured lamp drawing, would place them.",
	"Lamp 8 (Jackpot): the lamp page lists it among the playfield lamps but its drawing has no callout for it, and the table "
	"shows it as a backboard decal with the back-panel lamps; its spatial key is omitted.",
	"Lamps 49-56 (MILLION letters and Build Jackpot) stand on the back panel; the table shows them as backboard decals, not "
	"bulbs, so their spatial keys are omitted.",
	"Solenoids 27, 30 and 31 (Left Side, Right Ramp and Left Ramp flashers): the Solenoid Table prints one playfield bulb each, "
	"but the table lights two, three and two bulbs for them, and no source says which is the machine's socket, so their spatial "
	"keys are omitted.",
	"Solenoid 32 (Timer Flasher): the Solenoid Table prints two playfield bulbs and the drawing marks 08C, but the table lights "
	"only a bulbless light for it, so its spatial key is omitted.",
	"Solenoids 25 and 26 (flipper flashers): the Solenoid Table prints two playfield bulbs each and the table models one, so "
	"each keeps one observed placement and the second bulb has none.",
	"Solenoid 10 (Playfield G.I. Relay): the 36 placements are the bulbs of the retained table's G.I. collections; this record "
	"cites no G.I. layout from the manual and a table's grouping is not the machine's wiring, so they stay observed without a "
	"quantity.",
	"No placement was checked against the manual's numbered location drawings, whose callouts were read only for their order "
	"along each edge; every located placement keeps the table's observed status.",
]


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs, located_outputs, omitted = [], [], []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	statuses: dict[str, int] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			na_inputs.setdefault(spatial["reason"], []).append(device["binding"]["device"])
		else:
			located_inputs.append(device["binding"]["device"])
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": device["binding"]["device"]}
		spatial = device.get("spatial")
		if spatial is None:
			omitted.append(binding)
		elif spatial["status"] == "not_applicable":
			na_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	unvalidated = sorted(
		item["id"] for collection in ("inputs", "outputs") for device in definition[collection]
		for item in (device.get("spatial") or {}).get("placements", []) if item["provenance"]["status"] != "validated"
	)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "observed",
		"blockers": SPATIAL_BLOCKERS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "source_ref": VPX_EXTRACTION_SOURCE},
		"source_hashes": {"embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256, "table_sha256": TABLE_SHA256},
		"placement_count": placement_count,
		"placement_status_counts": dict(sorted(statuses.items())),
		"unvalidated_placements": unvalidated,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(values, key=lambda item: (item["group"], item["address"])) for reason, values in sorted(na_outputs.items())},
		"omitted_outputs": sorted(omitted, key=lambda item: (item["group"], item["address"])),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, (_, reason) in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto {reason}."} for address, reason in sorted(SOLENOID_PROJECTED.items())]
		),
		"excluded_object_classes": [
			"Light objects of the InsertLights collection (lN and lNa): insert lights that show no bulb and sit on no bulb primitive",
			"Flasher objects l8 and l49-l56: backboard decals the script fades for the back-panel lamps",
			"GIBulbN Light objects: glow lights over the G.I. bulb primitives, which are the placements",
			"fLightN, fLightNa/b, fPlasticsLightN and fBulbN: flasher glow objects over and beside the bulb primitives, and the bulbless fLight27b and fLight32",
			"l52a, l53a and l54a: bumper glow companions of the bulb-mesh lights l52b, l53b and l54b",
			"Primitives pLeftTrap and pRightTrap: trap meshes baked at a local origin; the trap kickers are the placements",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Mousin' Around! (Bally, 1989) spatial review",
		"",
		"Status: the machine record stays `partial` at `machines/partial/bally/mousin-around-1989.json`; its spatial dimension "
		f"stays open because of the {len(report['blockers'])} spatial blockers below.",
		"",
		f"The geometry source is the retained known-working `Mousin_ Around! (Bally 1989).vpx` by Herweh (version 1.0), SHA-256 "
		f"`{TABLE_SHA256}`, whose embedded script (SHA-256 `{SCRIPT_SHA256}`) is the binding authority. Bounds are "
		f"`{TABLE_BOUNDS}`; every coordinate is x/964 and y/2162, rounded to at most six places.",
		"",
		"## Evidence decisions",
		"",
		"- A switch placement is the centre of the table object the script binds to the address: a trigger, target, kicker, "
		"bumper or slingshot wall.",
		"- A flasher or G.I. placement is the bulb primitive the script lights (`pBulbN`), or the bulb-mesh light in a bumper cap, "
		"or the back-panel flasher's dome; a light that sits on no bulb marks no socket.",
		"- Sensors and coils with no table object of their own (the trough, trap up/down, motor-limit and diverter switches, and "
		"the outhole, feeder, trap, motor and diverter drives) are documented projections onto their own mechanism's object.",
		"- Where the table lights more bulbs for a flasher than the Solenoid Table prints, the spatial key is omitted rather than "
		"guessing which one is the socket.",
		"- Backbox and cabinet devices take controlled `not_applicable` records: the insert-board jackpot lamps 57-63, the insert "
		"G.I. relay (9), the knocker, the A/C relay and its switch, the cabinet, flipper and diagnostic switches, the Country "
		"jumper and both displays.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		short = "Switch" if entry["group"] == "pinmame.input.switch" else "Solenoid"
		lines.append(f"- {short} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({', '.join(f'{k} {v}' for k, v in report['placement_status_counts'].items())})",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Outputs with an omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, values in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(values)}")
	for reason, values in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(values)}")
	lines += ["", "## Blockers", ""] + [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the "
		"mechanisms are covered, and polarity is settled by the ROM's Switch Levels test. Promotion to `author_ready` is "
		"refused: the playfield inserts and several flashers have no socket in the retained table, the G.I. placements come "
		"only from the table's grouping, no placement was checked against the manual's drawings, and the LA-4C competition "
		"driver's ROM is not available, so `coverage.missing` is `[\"variant_differences\", \"spatial_placement\"]`. A table "
		"that models the insert bulbs, measured lamp and flasher drawings, and the LA-4C ROM (whose service tests name every "
		"address it drives) would close them.",
		"",
	]
	return "\n".join(lines)


KNOWLEDGE_TEXT = r'''# Bally Mousin' Around! (1989)

Coverage: **partial**. Every controller address has a sourced disposition, wiring and polarity, and the
mechanisms are documented; the record stays partial for `variant_differences` (the LA-4C competition
driver's ROM is not available) and `spatial_placement` (no playfield insert has a socket in the retained
table, several flashers are unplaced, and nothing was checked against the manual's drawings). This note
is generated by `tools/curate_mousin_around.py`.

## Identity

- IPDB 1635: Mousin' Around!, Midway Manufacturing Company under the Bally name, model number 2009,
  design by Ward Pemberton, manufactured November 20, 1989, 2,996 units; IPDB names its MPU "Williams
  System 11B". OPDB `G43oq-MJp02`.
- The manual (Bally_1989_Mousin_Around_Manual.pdf, 120 image-only pages) says "MOUSIN' AROUND is using
  WILLIAMS ELECTRONICS GAMES System 11B". Pinned PinMAME agrees: `INITGAME(mousn,GEN_S11B,...)`, machine
  driver `s11a_one`, so `controller.hardware_generation` is `0x100` (GEN_S11B = GEN_S11X).
- Drivers: `mousn_l4` (LA-4, the parent and the driver the runs and the retained table use), `mousn_l1`
  (LA-1), `mousn_lu` (LU-1 Europe) and `mousn_l4c` (a 2019 community "LA-4C Competition MOD" of the LA-4
  game ROMs). LA-1 and LU-1 name every address exactly as LA-4 does except switch 37, which they call
  "RAMP DRAIN" where LA-4 says "MADE LEFT RAMP". LA-4C's archive is not in the local ROM corpus.

## Platform facts a recreation needs

- Switch matrix 1-64, column-major (`(column-1)*8+row`), read raw: the ROM's Switch Levels test shows a
  switch's name while its public address is held at 1, so every matrix contact is open at rest.
- A/C select relay 12: pulses on 1-8 are the "A" coils with the relay released; while it is energized
  PinMAME publishes the same drivers' "C" flashers at 25-32. Switch 2 is copied from 12 (S11_MUXSW2), so a
  recreation reads 2 and never drives it. The manual's matrix prints "Not Used" at 2, but its C-Side
  Test checks a "C-Side Switch"; the ROM's C-Side test ("C-SIDE SW. TEST", lower display 08, where
  the manual says 09) energizes the relay for about 1.93 s, 1.85 s apart, and shows "SELECTED C-SIDE"
  and "C-SIDE" while it is energized.
- Special solenoids 17-22 (jets, slingshots, top lanes gate) are fired by the ROM through its PIA lines;
  PinMAME maps no switch to them, so a consumer drives only the switches.
- Game-on 23 rises when a game starts and falls at a tilt; it gates the special solenoids and the
  synthetic flipper outputs 45-48, which PinMAME fabricates from the cabinet buttons at 82 (right) and 84
  (left) and also copies into matrix switches 57 and 58. Write the buttons at 82 and 84.
- 9 and 10 are reverse-acting G.I. relays (energized = off): 9 the insert board, 10 the playfield.
- Two sixteen-character alphanumeric displays: PinMAME index 0 (segment start 0), which the manual's
  test text calls the Player 1 and 2 displays and this record the upper display, and index 1 (segment
  start 20), the Player 3 and 4 displays, the lower one. The font draws 5 and S, and 0 and O, with one
  glyph each, so the ROM's lamp names "RETURN LOOP SOK" and "JACKPOT 1.S MILL." read as 50K and 1.5.

## Mechanisms

### Trough

Outhole switch 9 and the Outhole Kicker (1) feed a three-ball trough (13 left, 12 middle, 11 right);
the Ball Shooter Lane Feeder (2) serves the shooter lane (14). With the trough empty at power-up the ROM
runs a ball search through 1, 5, 8, 11, 14 and 16; with 11-13 held it runs none.

### Traps (ball eaters)

Two Trap (Ball Eater) Assemblies, B-20-9629, each with an up coil (AE-26-1400) and a down coil
(SM1-28-800). Trap 1 is the right one (Up 3, Down 5, up/down switch 33, ball switch 41); Trap 2 the
left (Up 4, Down 8, switches 34 and 42). The up/down switch is closed while the trap is down: the ROM
pulses the Up coil about every 0.8 s while it reads closed and stops when it opens, and its power-up
ball search pulses the Down coil while it reads open. Spelling M-O-U-S-E T-R-A-P (standups 17-21 and
25-28, or lit return lanes) sets the traps; two trapped balls and the third released into play start
Multi-ball, and after it the traps stay up to trap the mice again for the Jackpot. The retained script
kicks a resting ball out when its trap rises.

### Motorized center target bank

The Motor Relay (11) runs a motor that raises and lowers the three center targets (29-31). Limit
switches report the ends: 43 up, 50 down (the Switches note: right side switch down, left side switch
up). The ROM releases the relay about 0.1 s after the limit it waits for closes (0.27 s in the
gameplay run); the Motor Bank Test shows "DN 01 ERROR" after 7.6 s without 50 and "00 ERROR" after
15.2 s with neither, and at power-up the ROM gives up after 7.6-7.9 s. Hitting the targets in sequence
lowers the bank and lights the kickback; the retained table's Center Ramp switch (35) sits directly
behind the bank. The retained script moves the bank over about 2 s each way.

### Mouse hole

On the back panel: Mouse Hole Enter (32), three lock switches (59-61, C-13061) and the Mouse Hole Exit
drop kick (16, B-13081, AE-26-1200). The ROM fires 16 about 0.93 s after 59 closes and retries about
every 1.8 s while 59 stays closed. C-H-E-E-S-E opens the hole to build the Jackpot; MILLION opens it for
a million.

### Diverter, kickback and top lanes gate

The Ball Diverter (14, C-12902-1) is a coil-driven deflector whose A-12953 Mini Switch (49) reports
its position; the retained script toggles it on each pulse. The kickback (13) sits in the left outlane, whose switch 51 the ROM calls "KICKBACK"; it
fires 0.012 s after 51 closes. The Top Lanes Gate (22, SM2-35-4000, the ROM's "SHOOTER GATE") was held
from 2.8 s after the first ball was served until the next ball's serve.

## Lamps and flashers

- Lamps 1-48 are playfield inserts; lamp 8 (Jackpot) is listed with them but has no callout, and the
  retained table puts it on the backboard with 49-56. Lamps 49-56 (N-O-I-L-L-I-M, Build Jackpot) are on
  the back panel, 57-63 (Jackpot 1 to 5 Million) on the insert board, and 64 is not used.
- Flasher quantities follow the Solenoid Table: 25 and 26 two playfield bulbs each, 27, 29, 30 and 31
  one each, 32 two, 15 one, and 28 one #906 on the back panel. The retained table models one bulb for
  25 and 26, two for 27, three for 30, two for 31 and none for 32.

## Source disagreements, none of them conflicts

- Solenoid 18: the Solenoid/Flashers list prints AE-23-1500; the Solenoid Table and the slingshot
  assembly print AE-26-1500, which the record follows.
- Solenoids 13 and 14 both print power connection 5J2-4 in the Solenoid Table.
- Switch 11: the parts list prints 5647-12073-00, the trough assembly 5647-12073-08.
- Switch 48: the manual prints "Not Used", every ROM names it "MADE LEFT RAMP"; the record follows the
  manual.
- Switch 2: the manual prints "Not Used"; PinMAME and the ROM's C-Side test use it as the relay's
  C-side switch, which PinMAME drives itself.
- The manual numbers the C-Side test 09 and prints "UP ERROR"/"DOWN ERROR" for the motor test; the
  LA-4 ROM shows 08 and "DN 01 ERROR".
- The retained script writes switches 57 and 58 from the flipper keys; PinMAME overwrites them from 82
  and 84, so the writes have no effect.
- Pinned PinMAME types solenoid 16 (the mouse hole drop kick coil) as a #89 bulb.

## Evidence

- Manual: IPDB 1635 through the Wayback Machine, SHA-256
  `6dcd83d1485a1b2e9909cc65b07d9ce23e1e7757e87cdf4a002984465b02d9f0`; excerpts under
  `evidence/excerpts/bally.mousin-around.1989/`.
- Retained table: Herweh's version 1.0, SHA-256
  `6c914b95a3062036b285f751b606b1468f86d93a12f86943fc29405ed2be4c9d`, with its vpxtool extraction and
  manifest. Two pinned corpus scripts of the later version 2.1 edit carry the same bindings.
- Runtime: `evidence/runtime/system-11/mousin-around-l4-service-and-mechanisms.json` and the LA-1/LU-1
  service-test comparisons, with display readings pinned in
  `tools/seeds/bally/mousin-around-1989-frame-readings.json` and scenarios under
  `tools/harness-scenarios/system-11/mousn-*.json`.
'''


def generate(root: Path = ROOT) -> Path:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		if STATUS != "author_ready":
			raise RuntimeError(f"refusing to replace the author-ready Mousin' Around definition with a {STATUS} one: {stale}")
		stale.unlink()
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	write_text(root / KNOWLEDGE_PATH, KNOWLEDGE_TEXT)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / STALE_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Mousin' Around is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	definition = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Mousin' Around definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Mousin' Around seed is not byte-identical to the definition: {seed_path}")
	knowledge_path = root / KNOWLEDGE_PATH
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != KNOWLEDGE_TEXT.encode("utf-8"):
		raise RuntimeError(f"Mousin' Around knowledge note drifted from its deterministic curator: {knowledge_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Mousin' Around spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_bytes() != render_spatial_report(report).encode("utf-8"):
		raise RuntimeError(f"Mousin' Around spatial review drifted from its deterministic curator: {markdown_path}")
	print("Mousin' Around definition, seed, knowledge note and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed, the knowledge note and the spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Mousin' Around extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Mousin' Around retained extraction matches its pinned manifest.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
