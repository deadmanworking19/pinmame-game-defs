"""Curate the physical Williams Black Knight 2000 (1989) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail, runtime
observation, and normalized coordinate is a literal here, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed, and the
spatial report.

Black Knight 2000 runs on Williams System 11B. Switches and lamps share one sequential column-major
1-64 address space, general illumination is three ordinary solenoid addresses (9, 10, 11), and the
eight switched solenoids 1-8 are multiplexed onto 25-32 by the A/C select relay (12). See
``controllers/pinmame/system-11.json`` for the platform derivation.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

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
MACHINE_ID = "williams.black-knight-2000.1989"
PARTIAL_PATH = ROOT / "machines/partial/williams/black-knight-2000-1989.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/black-knight-2000-1989.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/williams/black-knight-2000-1989.json"
KNOWLEDGE_PATH = "knowledge/williams/black-knight-2000-1989.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/black-knight-2000-1989.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/black-knight-2000-1989.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
L4_RUNTIME_PATH = "evidence/runtime/system-11/black-knight-2000-l4-service-and-mechanisms.json"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
# (left, right) in the driver's own FLIP_SWNO macro order.
FLIP_SWNO = (58, 57)
MANUAL_SOURCE = "manual.williams.black-knight-2000.operations"
MANUAL_APRIL_SOURCE = "manual.williams.black-knight-2000.operation-manual-1989-04"
OPERATOR_SOURCE = "manual.williams.black-knight-2000.operator-message"
ROM_SOURCE = "rom.black-knight-2000.name-tables"
RUNTIME_SOURCE = "runtime.black-knight-2000.l4-service-and-mechanisms"
VPX_TABLE_SOURCE = "vpx-table.black-knight-2000-flupper-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.black-knight-2000-flupper-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.black-knight-2000-flupper-1-1"

ACQUIRED_AT = "2026-10-01T06:44:00Z"
IPDB_FILES = "https://www.ipdb.org/files/311/"
WAYBACK_PREFIX = "https://web.archive.org/web/2025id_/"
MANUAL_SHA256 = "4d9225b61d86072eaaeb8a6a1b2dd2365f1d25442641b9908a1cd1f8deff00b3"
MANUAL_APRIL_SHA256 = "d181b4ade8283588d167f35166c225fd2e1d875733ffbbfde4e27fb016dc0a97"
OPERATOR_SHA256 = "572111d29e1b3eebaccbefbfa88c179c29c08ec8f6d0408a3939b1227d455c38"
TABLE_SHA256 = "98ffb10a95b9a584bca9d11dd2da1bce7fca42108f1082d8ebf616efc0d2c7ba"
SCRIPT_SHA256 = "955bc5ba128b3be1cbab9e7d3afab87389195c76b63185c406477240a880b21d"
EXTRACTION_RELATIVE_PATH = Path("williams/black-knight-2000-1989/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/black-knight-2000-1989/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "2e49d7c77422ed9e19133163172aa28bd1e18df6b36c03be69fd68835303a764"
EXTRACTION_FILE_COUNT = 842
EXTRACTION_TOTAL_BYTES = 47134919
TABLE_WIDTH = 954.0
TABLE_HEIGHT = 2052.0
TABLE_BOUNDS = "left=0 top=0 right=954 bottom=2052"

# --- Driver tree -----------------------------------------------------------------------------
DRIVER_IDS = ("bk2k_l4", "bk2k_la2", "bk2k_lg1", "bk2k_lg3", "bk2k_pa5", "bk2k_pa7", "bk2k_pf1", "bk2k_pu1")
_SHARED = (
	"Declared with CORE_CLONEDEF against bk2k_l4 on the same s11_mS11BS machine driver, so it runs the one static "
	"bk2kGameData (GEN_S11B, s11_dispS11b2, A/C mux relay 12, FLIP_SWNO(58,57), S11_MUXSW2) and init_bk2k; no "
	"controller-address change."
)
DRIVER_COMPATIBILITY = {
	"bk2k_l4": ("identical", "Williams L-4 production game ROMs (bk2k_u26.l4 / bk2k_u27.l4), the clone-tree parent and the driver the retained known-working script binds (cGameName = \"bk2k_l4\"). The ROM name tables used for this record are this set's."),
	"bk2k_la2": ("identical", f"LA-2 game ROMs (u26-pu1.rom with bk2k_u27.la2). {_SHARED} Its switch and coil name tables match L-4's entry for entry, and its Coil Test pulses the same addresses in the same order (runtime evidence evidence/runtime/system-11/black-knight-2000-la2-coil-test.json)."),
	"bk2k_lg1": ("identical", f"LG-1 German ROMs (u26-pu1.rom with bk2k_u27.lg1; pinned s11games.c notes a one-byte difference in a redump of the second ROM). {_SHARED} Its ROM name tables were not decoded: the local bk2k_lg1.zip holds bk2kgu26.lg1 and bk2kgu27.lg1, whose CRCs do not match the ROMs pinned s11games.c declares for this set, so it was not loaded."),
	"bk2k_lg3": ("identical", f"LG-3 German ROMs. {_SHARED} Its coil-test names match L-4's; its switch table prints the KNIGHT letters (G H T K N I) for 41-46 where L-4 prints RIGHT/LEFT 3-BANK 1-3, and its adjustment texts are German. Its German Coil Test (SPULEN TEST) pulses the same addresses in the same order (runtime evidence evidence/runtime/system-11/black-knight-2000-lg3-coil-test.json); its Switch Edges test was not run."),
	"bk2k_pa5": ("compatible", f"PA-5 prototype. {_SHARED} Its switch and coil name tables match L-4's entry for entry and its Coil Test pulses the same addresses in the same order (runtime evidence evidence/runtime/system-11/black-knight-2000-pa5-coil-test.json), so no hardware difference is known; prototype game rules may differ."),
	"bk2k_pa7": ("compatible", f"PA-7 prototype. {_SHARED} Its switch and coil name tables match L-4's entry for entry and its Coil Test pulses the same addresses in the same order (runtime evidence evidence/runtime/system-11/black-knight-2000-pa7-coil-test.json), so no hardware difference is known; prototype game rules may differ."),
	"bk2k_pf1": ("compatible", f"PF-1 French prototype (pinned s11games.c comments that its two ROMs are U26 and U27 from the same CPU board of a working bk2k). {_SHARED} Its ROM archive is not in the local corpus, so its name tables were not read and it was not run."),
	"bk2k_pu1": ("compatible", f"PU-1 European prototype (u26-pu1.rom with u27-pu1.rom). {_SHARED} Its switch and coil name tables match L-4's entry for entry, and its Coil Test pulses the same addresses in the same order (runtime evidence evidence/runtime/system-11/black-knight-2000-pu1-coil-test.json)."),
}

POWER_UP_KICKERS = {
	1: " At power-up the ROM pulses it once about 1 s after start and then pulses it about every 1.45 s while the outhole switch (10) is held at 1 (runs l4-boot-*); with the trough full (11-13 at 1) it skips this sweep.",
	6: " At power-up the ROM pulses it once about 1.5 s after start and then pulses it about every 1.45 s while the ball popper switch (47) is held at 1 (runs l4-boot-*); with the trough full (11-13 at 1) it skips this sweep.",
	7: " At power-up the ROM pulses it once about 1.2 s after start and then pulses it about every 1.2 s while any of the upper lock switches (36-38) is held at 1 (runs l4-boot-*); with the trough full (11-13 at 1) it skips this sweep.",
	8: " At power-up the ROM pulses it once about 1.4 s after start and then pulses it about every 0.97 s while the right eject switch (40) is held at 1 (runs l4-boot-*); with the trough full (11-13 at 1) it skips this sweep.",
}

# --- Switches (manual printed 66/72 location lists, 67 matrix; ROM switch name table) --------------
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "A/C Relay C-Side Power", 3: "Credit Button", 4: "Right Coin Chute", 5: "Center Coin Chute",
	6: "Left Coin Chute", 7: "Slam Tilt", 8: "High Score Reset", 9: "Playfield Tilt", 10: "Outhole",
	11: "Ball Trough 1 (Right)", 12: "Ball Trough 2 (Middle)", 13: "Ball Trough 3 (Left)",
	16: "Motor Targets Up Limit", 17: "Left Jet Bumper", 18: "Left Slingshot", 19: "Right Jet Bumper", 20: "Right Slingshot",
	21: "Lower Jet Bumper", 22: "Left UPF Loop End", 23: "Right UPF Loop End", 24: "Motor Targets Down Limit",
	25: "WIN Lane W (Top UPF)", 26: "WIN Lane I (Top UPF)", 27: "WIN Lane N (Top UPF)",
	28: "WAR Lane W (Bottom UPF)", 29: "WAR Lane A (Bottom UPF)", 30: "WAR Lane R (Bottom UPF)",
	31: "UPF Wire Ramp Entry", 32: "Lower Ramp Exit (Skyway)",
	33: "Drawbridge Target (Upper)", 34: "Drawbridge Target (Middle)", 35: "Drawbridge Target (Lower)",
	36: "UPF Lock Lower", 37: "UPF Lock Middle", 38: "UPF Lock Upper", 39: "Left Outlane", 40: "Right Eject Hole",
	41: "Right 3-Bank Drop Target G (Left)", 42: "Right 3-Bank Drop Target H (Middle)", 43: "Right 3-Bank Drop Target T (Right)",
	44: "Left 3-Bank Drop Target K (Lower)", 45: "Left 3-Bank Drop Target N (Middle)", 46: "Left 3-Bank Drop Target I (Upper)",
	47: "Ball Popper", 48: "Right Outlane", 49: "U-Turn 1 (Lower Left)", 50: "U-Turn 2 (Upper Left)",
	51: "U-Turn 3 (Upper Right)", 52: "U-Turn 4 (Lower Right)", 53: "Ball Shooter Lane", 54: "Right Return Lane",
	55: "Left Return Lane", 57: "Right Flipper Button", 58: "Left Flipper Button", 59: "Magna Save Button",
}
UNUSED_SWITCHES = {14, 15, 56, 60, 61, 62, 63, 64}

# ROM switch-table text (bk2k_l4, U27 member offset 0x283a), decoded by tools/s11_rom_name_tables.py. The ROM's switch table
# has 59 entries; the five entries after it read as text of the adjustment tables that follow it and are not switch names.
# Entries 2, 14, 15 and 56 are blank.
ROM_SWITCH_NAMES = {
	1: "PLUMB TILT", 3: "CREDIT BUTTON", 4: "RIGHT COIN", 5: "MIDDLE COIN", 6: "LEFT COIN", 7: "SLAM TILT", 8: "HIGH SCORE RESET",
	9: "PLAYFIELD TILT", 10: "OUTHOLE", 11: "TROUGH 1", 12: "TROUGH 2", 13: "TROUGH 3", 16: "MOTOR UP", 17: "LEFT BUMPER",
	18: "LEFT SLING", 19: "RIGHT BUMPER", 20: "RIGHT SLING", 21: "LOWER BUMPER", 22: "LOOP END 1", 23: "LOOP END 2",
	24: "MOTOR DOWN", 25: "WIN \"W\" LANE", 26: "WIN \"I\" LANE", 27: "WIN \"N\" LANE", 28: "WAR \"W\" LANE", 29: "WAR \"A\" LANE",
	30: "WAR \"R\" LANE", 31: "UPPER RAMP ENTRY", 32: "LOWER RAMP EXIT", 33: "UPPER TARGET 3", 34: "UPPER TARGET 2",
	35: "UPPER TARGET 1", 36: "UPPER LOCK LOWER", 37: "UPPER LOCK MID", 38: "UPPER LOCK UPPER", 39: "LEFT OUTLANE",
	40: "RIGHT EJECT", 41: "RIGHT 3-BANK 1", 42: "RIGHT 3-BANK 2", 43: "RIGHT 3-BANK 3", 44: "LEFT 3-BANK 1",
	45: "LEFT 3-BANK 2", 46: "LEFT 3-BANK 3", 47: "BALL POPPER", 48: "RIGHT OUTLANE", 49: "U-TURN 1", 50: "U-TURN 2",
	51: "U-TURN 3", 52: "U-TURN 4", 53: "PLUNGER", 54: "RIGHT RETURN LN", 55: "LEFT RETURN LANE", 57: "LANE CHANGE RGHT",
	58: "LANE CHANGE LEFT", 59: "MAGNA SAVE",
}
# Printed matrix wording (printed page 67) where it differs from the working label.
MATRIX_WORDING = {
	2: "C Side Power A/C Relay", 4: "Left Coin Chute", 6: "Right Coin Chute", 11: "Ball Trough #1 (R)", 12: "Ball Trough #2 (Mid)",
	13: "Ball Trough #3 (L)", 16: "UP Motor Targets", 18: "BL Kicker (\"sling\")", 20: "BR Kicker (\"sling\")",
	21: "Lwr Jet Bumper", 22: "Left UPF Loop End", 23: "Right UPF Loop End", 24: "DOWN Motor Targets", 25: "W Lane", 26: "I Lane",
	27: "N Lane", 28: "W Lane", 29: "A Lane", 30: "R Lane", 31: "Upper Ramp Entry", 32: "Lower Ramp Exit",
	33: "Motor Targets (Upper Tgt)", 34: "Motor Targets (Middle Tgt)", 35: "Motor Targets (Lower Tgt)",
	36: "UPF Lock Lower Switch", 37: "UPF Lock Middle Switch", 38: "UPF Lock Upper Switch", 40: "Right Eject",
	41: "R 3-Bank Dr Target (left)", 42: "R 3-Bank Dr Target (mid)", 43: "R 3-Bank Dr Target (right)",
	44: "L 3-Bank Dr Target (lwr)", 45: "L 3-Bank Dr Target (mid)", 46: "L 3-Bank Dr Target (upr)",
	49: "U-Turn", 50: "U-Turn", 51: "U-Turn", 52: "U-Turn", 53: "Ball Shooter", 57: "Flipper Right", 58: "Flipper Left", 59: "Magna Save™",
}
# Lists wording (printed pages 66 and 72) where it differs from the working label.
LIST_WORDING = {
	2: "C-side: A/C Relay", 4: "R Coin Chute (USA)", 5: "Center Coin Chute (Not Used (USA))", 6: "L Coin Chute (USA)",
	8: "High Score Reset*", 11: "Ball Trough 1 (right)", 12: "Ball Trough 2 (mid)", 13: "Ball Trough 3 (left)",
	16: "UP (Motor Targets)", 18: "Left Kicker***", 20: "Right Kicker***", 24: "DOWN (Motor Targets)",
	31: "UPF Wire Ramp Entry (printed as a second \"30\")", 32: "Lower Ramp Exit", 36: "Lower Lock", 37: "Middle Lock",
	38: "Upper Lock", 40: "Right Eject Hole", 41: "R 3-Bank Dr Tgt (left)", 42: "R 3-Bank Dr Tgt (mid)", 43: "R 3-Bank Dr Tgt (rt)",
	44: "L 3-Bank Dr Tgt (lwr)", 45: "L 3-Bank Dr Tgt (mid)", 46: "L 3-Bank Dr Tgt (upr)", 49: "U Turn 1 (lwr left)",
	50: "U Turn 2 (uppr left)", 51: "U Turn 3 (upr right)", 52: "U Turn 4 (lwr right)", 53: "Ball Shooter Lane",
	57: "R Flipper Lane Change**1", 58: "L Flipper Lane Change**1", 59: "Magna Save™ Button",
}
SWITCH_PARTS = {
	1: "p/o D-11920-1", 2: "p/o D-12247", 3: "SW-1A-126", 4: "27-1092", 6: "27-1092", 7: "27-1066", 8: "27-1008", 9: "B-8306-1",
	10: "5647-12133-12", 11: "5647-12073-08", 12: "5647-09957-00", 13: "5647-09957-00", 16: "5647-12073-06",
	17: "B-8928", 19: "B-8928", 21: "B-8928", 22: "5647-12073-24", 23: "5647-12073-24", 24: "5647-12073-06",
	25: "5647-12073-18", 26: "5647-12073-18", 27: "5647-12073-18", 28: "5647-12073-18", 29: "5647-12073-18", 30: "5647-12073-18",
	31: "5647-12073-01", 32: "5647-12073-20", 33: "A-11177-1", 34: "A-11177-1", 35: "A-11315-3",
	36: "5647-12073-22", 37: "5647-12073-22", 38: "5647-12073-22", 39: "5647-12073-19", 40: "5647-12073-10",
	41: "p/o C-11318-1", 42: "p/o C-11318-1", 43: "p/o C-11318-1", 44: "p/o C-11318-1", 45: "p/o C-11318-1", 46: "p/o C-11318-1",
	47: "A-11658", 48: "5647-12073-19", 49: "5647-12073-19", 50: "5647-12073-19", 51: "5647-12073-19", 52: "5647-12073-19",
	53: "5647-12073-04", 54: "5647-12073-19", 55: "5647-12073-19", 57: "p/o D-12313", 58: "p/o D-12313", 59: "SW-1A-126",
}
SWITCH_TYPES = {
	1: "tilt", 2: "other", 3: "button", 7: "tilt", 8: "button", 9: "tilt", 41: "opto", 42: "opto", 43: "opto", 44: "opto",
	45: "opto", 46: "opto", 57: "opto", 58: "opto", 59: "button",
}
# The manual's own parts pages call the 5647- parts "Snap Action Switch/w Roller", "Subminiature Switch", "Submin. Switch" and
# "µswitch"; the ones the working tables list under that prefix are recorded as microswitches.
MICROSWITCH_PART_PREFIX = "5647-"
SWITCH_COLUMN_WIRING = {
	1: ("GRN-BRN", "1J8-1", "Q45"), 2: ("GRN-RED", "1J8-2", "Q49"), 3: ("GRN-ORN", "1J8-3", "Q44"), 4: ("GRN-YEL", "1J8-4", "Q48"),
	5: ("GRN-BLK", "1J8-5", "Q43"), 6: ("GRN-BLU", "1J8-7", "Q47"), 7: ("GRN-VIO", "1J8-8", "Q42"), 8: ("GRN-GRY", "1J8-9", "Q46"),
}
SWITCH_ROW_WIRING = {
	1: ("WHT-BRN", "1J10-9"), 2: ("WHT-RED", "1J10-8"), 3: ("WHT-ORN", "1J10-7"), 4: ("WHT-YEL", "1J10-6"),
	5: ("WHT-GRN", "1J10-5"), 6: ("WHT-BLU", "1J10-3"), 7: ("WHT-VIO", "1J10-2"), 8: ("WHT-GRY", "1J10-1"),
}
DEDICATED_SWITCHES = {
	-7: ("Advance", "service.advance", "S11_SWADVANCE: the ADVANCE button on the coin-door diagnostic switch assembly; it steps the Game Status, audit, adjustment, and diagnostic displays."),
	-6: ("Auto-Up/Manual-Down", "service.updown", "S11_SWUPDN: the AUTO-UP/MANUAL-DOWN toggle. In PinMAME's public state 1 is Auto-Up and 0 is Manual-Down."),
	-5: ("CPU Diagnostic", "service.diagnostic", "S11_SWCPUDIAG: pinned s11.c wires it to the CPU's NMI line (the CPU board's diagnostic button)."),
	-4: ("Sound Diagnostic", "service.diagnostic", "S11_SWSOUNDDIAG: pinned s11.c passes it to the sound board's diagnostic input."),
}
CABINET_SWITCH_ROLES = {1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin", 7: "cabinet.slam-tilt", 8: "cabinet.service", 9: "cabinet.tilt", 57: "cabinet.flipper", 58: "cabinet.flipper", 59: "cabinet.magna-save"}


# Normalized coordinates from the retained table (x/954, y/2052), object centres unless noted. Walls use drag-point centroids.
SWITCH_POSITIONS = {
	10: ('Kicker.Outhole', 0.498362, 0.961547),
	16: ('Wall.DBTrgt2 drag-point centroid', 0.288858, 0.226458),
	24: ('Wall.DBTrgt2 drag-point centroid', 0.288858, 0.226458),
	17: ('Bumper.Bumper1', 0.597484, 0.216846),
	19: ('Bumper.Bumper2', 0.803983, 0.194917),
	21: ('Bumper.Bumper3', 0.741614, 0.288727),
	18: ('Wall.LSling drag-point centroid', 0.222963, 0.713544),
	20: ('Wall.RSling drag-point centroid', 0.682321, 0.712494),
	22: ('Trigger.Loop1', 0.864256, 0.070175),
	23: ('Trigger.Loop2', 0.939727, 0.127741),
	25: ('Trigger.Win1', 0.541929, 0.131457),
	26: ('Trigger.Win2', 0.644392, 0.120005),
	27: ('Trigger.Win3', 0.750262, 0.110258),
	28: ('Trigger.War1', 0.460168, 0.421174),
	29: ('Trigger.War2', 0.566038, 0.455653),
	30: ('Trigger.War3', 0.669287, 0.492812),
	31: ('Trigger.URampEntry', 0.388216, 0.113495),
	32: ('Trigger.Skyway', 0.272537, 0.117934),
	33: ('Wall.DBTrgt1 drag-point centroid', 0.327300, 0.206641),
	34: ('Wall.DBTrgt2 drag-point centroid', 0.288858, 0.226458),
	35: ('Wall.DBTrgt3 drag-point centroid', 0.251628, 0.246926),
	36: ('Trigger.Lock1', 0.081237, 0.458090),
	37: ('Trigger.Lock2', 0.080713, 0.432261),
	38: ('Trigger.Lock3', 0.080713, 0.406433),
	39: ('Trigger.LOutLane', 0.050314, 0.793738),
	40: ('Kicker.REject', 0.834733, 0.467350),
	41: ('HitTarget.sw1', 0.396825, 0.406192),
	42: ('HitTarget.sw2', 0.447553, 0.424193),
	43: ('HitTarget.sw3', 0.499110, 0.442676),
	44: ('HitTarget.sw4', 0.091901, 0.520392),
	45: ('HitTarget.sw5', 0.110260, 0.493310),
	46: ('HitTarget.sw6', 0.129309, 0.465137),
	47: ('Kicker.BallPopper1', 0.419811, 0.150585),
	48: ('Trigger.ROutLane', 0.848008, 0.748173),
	49: ('Trigger.UTurn1', 0.310370, 0.347100),
	50: ('Trigger.UTurn2', 0.357966, 0.308358),
	51: ('Trigger.UTurn3', 0.544025, 0.352705),
	52: ('Trigger.UTurn4', 0.575996, 0.419712),
	53: ('Trigger.Shooter', 0.939902, 0.885478),
	54: ('Trigger.RRetLane', 0.779874, 0.715034),
	55: ('Trigger.LRetLane', 0.116876, 0.717958),
}

LAMP_POSITIONS = {
	5: ('Light5', 0.449686, 0.662524),
	8: ('Light8b', 0.046384, 0.683723),
	9: ('Light9b', 0.558962, 0.478558),
	10: ('Light10b', 0.654874, 0.517544),
	11: ('Light11b', 0.750524, 0.550804),
	12: ('Light12b', 0.175577, 0.623051),
	13: ('Light13b', 0.204403, 0.590643),
	14: ('Light14b', 0.249476, 0.562378),
	15: ('Light15b', 0.309748, 0.541667),
	16: ('Light16b', 0.376834, 0.527047),
	17: ('Light17b', 0.171908, 0.356847),
	18: ('Light18b', 0.890461, 0.259868),
	19: ('Light19', 0.848025, 0.598956),
	20: ('Light20b', 0.283543, 0.299951),
	21: ('Light21b', 0.849319, 0.681774),
	22: ('Light22b', 0.334906, 0.400585),
	23: ('Light23b', 0.045597, 0.731603),
	24: ('Light24b', 0.450734, 0.865497),
	25: ('Light25b', 0.513627, 0.068957),
	26: ('Light26b', 0.621593, 0.067982),
	27: ('Light27b', 0.729036, 0.067982),
	28: ('Light28b', 0.460954, 0.377924),
	29: ('Light29b', 0.565514, 0.413986),
	30: ('Light30b', 0.669811, 0.453216),
	31: ('Light31b', 0.594864, 0.351852),
	32: ('Light32b', 0.715933, 0.402534),
	33: ('Light33b', 0.458595, 0.266813),
	34: ('Light34b', 0.472222, 0.301779),
	35: ('Light35b', 0.489256, 0.332115),
	36: ('Light36b', 0.351677, 0.812865),
	37: ('Light37b', 0.396751, 0.799464),
	38: ('Light38b', 0.448637, 0.794347),
	39: ('Light39b', 0.500524, 0.799951),
	40: ('Light40b', 0.548218, 0.810673),
	41: ('Light41b', 0.406184, 0.455775),
	42: ('Light42b', 0.449161, 0.472222),
	43: ('Light43b', 0.495283, 0.490010),
	44: ('Light44b', 0.148323, 0.556652),
	45: ('Light45b', 0.163784, 0.530824),
	46: ('Light46b', 0.179507, 0.506579),
	47: ('Light47b', 0.274109, 0.487695),
	48: ('Light48b', 0.225629, 0.422758),
	49: ('Light49b', 0.453354, 0.572856),
	50: ('Light50b', 0.516247, 0.578947),
	51: ('Light51b', 0.572327, 0.594542),
	52: ('Light52b', 0.606918, 0.619883),
	53: ('Light53b', 0.621069, 0.649366),
	54: ('Light54b', 0.607966, 0.679337),
	55: ('Light55b', 0.570755, 0.704922),
	56: ('Light56b', 0.518344, 0.721491),
	57: ('Light57b', 0.450734, 0.731725),
	58: ('Light58b', 0.386530, 0.725755),
	59: ('Light59b', 0.336478, 0.706140),
	60: ('Light60b', 0.301887, 0.679825),
	61: ('Light61b', 0.288784, 0.649854),
	62: ('Light62b', 0.300314, 0.618421),
	63: ('Light63b', 0.337526, 0.593567),
	64: ('Light64b', 0.392558, 0.578460),
}


SWITCH_PROJECTIONS = {
	16: "UP (Motor Targets) is the roller snap-action switch (5647-12073-06) the Motor Assembly's cam (B-12465, item 6) closes at one end of the drawbridge targets' travel; no retained object models it, so it is anchored at the middle drawbridge-target wall, which the table's own motor model (cvpmMech Mech3Bank) moves.",
	24: "DOWN (Motor Targets) is the second roller snap-action switch (5647-12073-06) on the Motor Assembly's cam; anchored at the middle drawbridge-target wall for the same reason as 16.",
	18: "The slingshot switch pair (A-4834-H; A-11538-1, \"Paired Kicker Actuating Sw\") is inside the kicker; anchored at the drag-point centroid of the retained LSling wall.",
	20: "Anchored at the drag-point centroid of the retained RSling wall.",
	33: "Anchored at the drag-point centroid of the retained DBTrgt1 wall, the table's upper drawbridge target.",
	34: "Anchored at the drag-point centroid of the retained DBTrgt2 wall, the middle drawbridge target.",
	35: "Anchored at the drag-point centroid of the retained DBTrgt3 wall, the lower drawbridge target.",
	40: "The Right Eject Hole switch (5647-12073-10) closes in the eject hole; anchored at the retained REject kicker, which the script closes 40 from.",
	47: "The Ball Popper switch (A-11658, a switch and diode assembly under the popper cap) closes in the popper; anchored at the retained BallPopper1 kicker, which the script closes 47 from.",
}
# Script handlers that disagree with the manual's names (table defect, not machine doubt).
TRIGGER_NAMES = {
	22: "Loop1", 23: "Loop2", 25: "Win1", 26: "Win2", 27: "Win3", 28: "War1", 29: "War2", 30: "War3", 31: "URampEntry", 32: "Skyway",
	36: "Lock1 (swLock1)", 37: "Lock2 (swLock2)", 38: "Lock3 (swLock3)", 39: "LOutLane", 48: "ROutLane", 49: "UTurn1", 50: "UTurn2",
	51: "UTurn3", 52: "UTurn4", 53: "Shooter", 54: "RRetLane", 55: "LRetLane",
}
UNPLACED_SWITCHES = {
	11: "The retained table has no object for the trough switches: its three-ball cvpmTrough is built from the number array Array(swTrough1,swTrough2,swTrough3) and one BallRelease kicker, and no factory drawing locates the trough optos under the bottom arch, so no placement is asserted.",
	12: "See switch 11.",
	13: "See switch 11.",
}

# --- Solenoids (Solenoid Table printed 29; locations lists printed 71 and 73; ROM coil test) ---------
SOLENOID_A = {
	1: ("Outhole Kicker", "coil", "Vio-Brn", "1P11-1", "5J1-9: 5J4-9 (A)", "Q33", "AE-23-800"),
	2: ("Ball Release (Shooter Lane Feeder)", "coil", "Vio-Red", "1P11-3", "5J1-7: 5J4-8 (A)", "Q25", "AE-23-800"),
	3: ("Left 3-Bank Drop Target Reset", "coil", "Vio-Orn", "1P11-4", "5J1-6: 5J4-7 (A)", "Q32", "AE-26-1200"),
	4: ("Right 3-Bank Drop Target Reset", "coil", "Vio- Yel", "1P11-5", "5J1-5: 5J4-6 (A)", "Q24", "AE-26-1200"),
	5: ("Not Used Switched Solenoid 05A", "coil", "Vio-Grn", "1P11-6", "5J1-4: 5J4-5 (A)", "Q31", None),
	6: ("Ball Popper", "coil", "Vio-Blu", "1P11-7", "5J1-3: 5J4-4 (A)", "Q23", "AE-23-800"),
	7: ("UPF Lockup Kickback", "coil", "Vio-Blk", "1P11-8", "5J1-2: 5J4-2 (A)", "Q30", "AE-23-800"),
	8: ("Right Eject", "coil", "Vio-Gry", "1P11-9", "5J1-1: 5J4-1 (A)", "Q22", "AE-26-1500"),
}
# address -> (label, wire, cpu connection, power connection, lamp type, playfield bulbs, insert-board bulbs)
SOLENOID_C = {
	25: ("UPF Big Red Bolt Flasher", "Blk-Brn", "(Gry-Brn)", "5J5-9 (C)", "#906/#89 flashlamps", 2, 2),
	26: ("UPF Big Blue Bolt Flasher", "Blk-Red", "(Gry-Red)", "5J5-8 (C)", "#906/#89 flashlamps", 2, 2),
	27: ("Bolt Circle Center Flasher", "Blk-Orn", "(Gry-Orn)", "5J5-7(C)", "#906/#89 flashlamps", 2, 2),
	28: ("Flipper Lane Flasher", "Blk-Yel", "(Gry-Yel)", "5J5-5 (C)", "#906/#89 flashlamps", 2, 2),
	29: ("Drop Target Flasher", "Blk-Grn", "(Gry-Grn)", "5J5-4 (C)", "#906/#89 flashlamps", 1, 2),
	30: ("LPF Ramp Flasher", "Blk-Blu", "(Gry-Blu)", "5J5-3 (C)", "#906/#89 flashlamps", 2, 2),
	31: ("Right Eject and Upper Flipper Flashers", "Blk-Vio", "(Gry-Vio)", "5J5-2 (C)", "#89 flashlamps", 1, 2),
	32: ("UPF Lockup Kickback Flasher", "Blk-Gry", "(Gry-Blk)", "5J5-1 (C)", "#906/#89 flashlamps", 1, 2),
}
SOLENOID_CONTROLLED = {
	9: ("Insert Board G.I. Relay", "gi", "Brn-Blk", "1P12-1", "5J2-9: 5J6-9: 2J4-3", "Q17", "5580-09555-01"),
	10: ("UPF G.I. Relay", "gi", "Brn-Red", "1P12-2", "5J2-8: 5J6-8: 2J4-5", "Q9", "5580-09555-01"),
	11: ("LPF G.I. Relay", "gi", "Brn-Orn", "1P12-4", "5J2-6: 5J6-7: 2J4-6", "Q16", "5580-12145-01"),
	12: ("A/C Select Relay", "relay", "Brn-Yel", "1P12-5", "5J2-5", "Q8", "5580-09555-01"),
	13: ("Kickback (Left Outlane)", "coil", "Brn-Grn", "1P12-6", "5J2-4: 5J6-5", "Q15", "AE-23-800"),
	14: ("Knocker", "coil", "Brn-Blu", "1P12-7", "5J2-4: 5J6-3", "Q7", "AE-23-800"),
	15: ("Magna Save Driver", "magnet", "Brn-Vio", "1P12-8", "5J2-2: 5J6-2", "Q14", "C-12493"),
	16: ("Motor Targets (UPF) Relay", "relay", "Brn-Gry", "1P12-9", "5J2-1: 5J6-1", "Q6", "5580-12145-01"),
}
SOLENOID_SPECIAL = {
	17: ("Left Jet Bumper", "Blu-Brn", "1P19-7", "5J3-7: 5J7-7", "Q75", "AE-23-800", 1),
	18: ("Left Slingshot", "Blu-Red", "1P19-4", "5J3-6: 5J7-6", "Q71", "AE-26-1500", 2),
	19: ("Right Jet Bumper", "Blu-Orn", "1P19-3", "5J3-3: 5J7-3", "Q73", "AE-23-800", 3),
	20: ("Right Slingshot", "Blu-Yel", "1P19-6", "5J3-4: 5J7-5", "Q69", "AE-26-1500", 4),
	21: ("Lower Jet Bumper", "Blu-Grn", "1P19-8", "5J3-2:5J7-2", "Q77", "AE-23-800", 5),
	22: ("Not Used Special Solenoid 06", "Blu-Blk", "1P19-9", "5J3-1: 5J7-1", "Q79", None, 6),
}
# ROM coil-test names by public address (bk2k_l4 coil table, in coil-test order, paired with the addresses the coil test pulses).
ROM_COIL_NAMES = {
	1: "OUTHOLE", 25: "RED BOLT", 2: "BALL SERVE", 26: "BLUE BOLT", 3: "LEFT 3 BANK", 27: "CENTER FLASHER", 4: "RIGHT 3 BANK",
	28: "FLIP LANE FLASH", 5: "UNUSED", 29: "MID. DROP FLASHER", 6: "BALL POPPER", 30: "RAMP FLASHER", 7: "LEVEL 3 KICKER",
	31: "RIGHT FLASHER", 8: "RIGHT EJECT", 32: "3-LOCK FLASHER", 9: "INSERT G.I.", 10: "LEVEL 2 G.I.", 11: "LEVEL 1 G.I.",
	12: "A/C   SELECT", 13: "KICKBACK", 14: "KNOCKER", 15: "MAGNA SAVE", 16: "MOTOR 3 BANK", 17: "LEFT  BUMPER",
	18: "LEFT  KICKER", 19: "RIGHT BUMPER", 20: "RIGHT KICKER", 21: "LOWER BUMPER", 22: "UNUSED",
}
# ROM single-lamp names (bk2k_l4 Single Lamps test 04, run l4-single-lamps): the step number equals the one public lamp that blinks. The ROM has no lamp name
# table; these are the display's stable text, in which the display draws the digit 0 as the letter O and 5 as S (CENTER SOOOO is CENTER 50000).
ROM_LAMP_NAMES = {
	1: "\"R\"", 2: "\"A\"", 3: "\"N\"", 4: "\"S\"", 5: "BOLT CIRCLE MID", 6: "\"O\"", 7: "\"M\"", 8: "LEFT OUTLANE", 9: "U-TURN RIGHT", 10: "SPIN BOLT",
	11: "RIGHT EJECT BOLT", 12: "\"B\"", 13: "\"L\"", 14: "\"A\"", 15: "\"C\"", 16: "\"K\"", 17: "EXTRA BALL BOLT", 18: "BIG RED BOLT",
	19: "MAGNA SAVE", 20: "BIG BLUE BOLT", 21: "RIGHT OUTLANE", 22: "U-TURN LEFT", 23: "KICK BACK BOLT", 24: "SHOOT AGAIN", 25: "WIN \"W\" LANE",
	26: "WIN \"I\" LANE", 27: "WIN \"N\" LANE", 28: "WAR \"W\" LANE", 29: "WAR \"A\" LANE", 30: "WAR \"R\" LANE", 31: "JACKPOT BOLT", 32: "RANSOM BOLT",
	33: "UPPER TARGET 3", 34: "UPPER TARGET 2", 35: "UPPER TARGET 1", 36: "2X", 37: "3X", 38: "BONUS HOLD", 39: "4X", 40: "SX", 41: "\"G\"",
	42: "\"H\"", 43: "\"T\"", 44: "\"K\"", 45: "\"N\"", 46: "\"I\"", 47: "SKYWAY BOLT", 48: "HURRY UP", 49: "CENTER EX. BALL", 50: "CENTER SOOOO",
	51: "CENTER MAGNA SV", 52: "CENTER 1OOOO", 53: "CENTER MULTIBALL", 54: "CENTER 1OOOOO", 55: "CENTER RANSOM", 56: "CENTER 2OOOOO",
	57: "CENTER SPECIAL", 58: "CENTER 2OOOO", 59: "CENTER KICKBACK", 60: "CENTER 1SOOOO", 61: "CENTER DRAWBRG.", 62: "CENTER 7SOOO",
	63: "CENTER HURRY UP", 64: "CENTER 2SOOOO",
}
SOLENOID_CALLBACKS = {
	1: "bsTrough.SolIn (kicks the outhole ball into the trough)", 2: "bsTrough.SolOut (serves the next trough ball)",
	3: "dtKNI.SolDropUp (raises the left drop-target bank)", 4: "dtGHT.SolDropUp (raises the right drop-target bank)",
	6: "SolBallPopper (bsBallPopper.SolOut kicks the ball out of the popper)", 7: "Lock.SolExit (cvpmVLock releases a locked ball)",
	8: "SolREject (bsREject.SolOut kicks the ball out of the right eject)", 9: "SolCallback(sIGIRelay) is empty (the table does not model the insert board)",
	10: "SolUPFGIRelay (the LightsGIupf collection is off while energized)", 11: "SolLPFGIRelay (the LightsGIlpf collection is off while energized)",
	12: "SolACSelect (relay sounds only)", 13: "SolKickBack (enables the Kickback kicker for 500 ms)", 14: "vpmSolSound Knocker",
	15: "no callback: MagnaSave.Solenoid = sMagnaSave drives the table's cvpmMagnet", 16: "SolMTargets (the drawbridge sound; Mech3Bank.Sol1 = sMTargets drives the cvpmMech)",
	25: "SolRedBoltFlash", 26: "SolBlueBoltFlash", 27: "SolKnightHeadFlash", 28: "SolFlipLaneFlash", 29: "SolDTFlash",
	30: "SolSkyWayFlash", 31: "SolREjectFlash", 32: "SolLockFlash",
}
SOLENOID_POSITIONS = {
	1: ("Kicker.Outhole", [(0.498362, 0.961547)]),
	2: ("Kicker.BallRelease", [(0.872576, 0.863593)]),
	3: ("HitTarget.sw5 (middle target of the left bank it resets)", [(0.110260, 0.493310)]),
	4: ("HitTarget.sw2 (middle target of the right bank it resets)", [(0.447553, 0.424193)]),
	6: ("Kicker.BallPopper1", [(0.419811, 0.150585)]),
	7: ("Plunger.LockPlunger (the upper-playfield lockup kickback plunger)", [(0.083333, 0.487086)]),
	8: ("Kicker.REject", [(0.834733, 0.467350)]),
	13: ("Kicker.Kickback", [(0.052411, 0.800195)]),
	15: ("Trigger.MSave (the table's magnet capture zone)", [(0.777451, 0.631914)]),
	17: ("Bumper.Bumper1", [(0.597484, 0.216846)]), 19: ("Bumper.Bumper2", [(0.803983, 0.194917)]), 21: ("Bumper.Bumper3", [(0.741614, 0.288727)]),
	18: ("Wall.LSling drag-point centroid", [(0.222963, 0.713544)]), 20: ("Wall.RSling drag-point centroid", [(0.682321, 0.712494)]),
	25: ("Light.RedBoltFlash", [(0.887841, 0.259990)]),
	26: ("Light.BlueBoltFlash", [(0.255765, 0.310216)]),
	27: ("Light.KnightHeadFlash", [(0.449686, 0.653752)]),
	28: ("Light.GI14 and Light.GI15", [(0.147803, 0.793390), (0.769081, 0.787315)]),
	29: ("Light.GI17", [(0.433962, 0.375107)]),
	30: ("Light.SkyWayFlash", [(0.088613, 0.307616)]),
	31: ("Light.GI24", [(0.797966, 0.409761)]),
	32: ("Light.LockFlash", [(0.134047, 0.382320)]),
}
# Flasher circuits whose printed playfield bulb count is larger than the number of bulbs the retained table models.
PARTLY_PLACED_FLASHERS = {
	25: "the table models the flash as one light (RedBoltFlash) on the big red bolt; the second printed playfield bulb has no drawn or modelled location",
	26: "the table models the flash as one light (BlueBoltFlash) on the big blue bolt; the second printed playfield bulb has no drawn or modelled location",
	27: "the table models the flash as one light (KnightHeadFlash) at the bolt circle's center; the second printed playfield bulb has no drawn or modelled location",
	30: "the table models the flash as one light (SkyWayFlash) at the skyway ramp's lower left; the second printed playfield bulb has no drawn or modelled location",
}
# Retained-table G.I. bulbs per relay: one point per bulb; a GInb partner is the glow of the same bulb.
GI_UPPER = [
	("bumper1light1", 0.597484, 0.216968), ("bumper2light1", 0.803459, 0.194795), ("bumper3light1", 0.741090, 0.288606),
	("GI5", 0.617662, 0.474278), ("GI10", 0.594078, 0.123279), ("GI11", 0.800052, 0.103299), ("GI9", 0.695231, 0.111583),
	("GI12", 0.844983, 0.111890), ("GI22", 0.490964, 0.133098), ("GI23", 0.308183, 0.156631), ("GI26", 0.950965, 0.329537),
	("GI25", 0.931193, 0.460963), ("GI27", 0.893197, 0.386717), ("GI28", 0.955106, 0.075404), ("GI29", 0.721397, 0.511821),
	("GI6", 0.669840, 0.493049), ("GI7", 0.566727, 0.456085), ("GI30", 0.512685, 0.436447), ("GI31", 0.745001, 0.509895),
	("GI32", 0.460508, 0.419697), ("GI8", 0.405845, 0.397942), ("GI33", 0.384311, 0.395247), ("GI34", 0.385829, 0.195040),
]
GI_LOWER = [
	("GI1", 0.218800, 0.745030), ("GI2", 0.686508, 0.747993), ("GI3", 0.732180, 0.684805), ("GI4", 0.165618, 0.687241),
	("GI13", 0.210692, 0.813460), ("GI16", 0.695493, 0.811023), ("GI19", 0.058176, 0.460146), ("GI18", 0.053155, 0.547153),
	("GI20", 0.045073, 0.561998), ("GI21", 0.064551, 0.501708),
]


# --- Status and prose constants -------------------------------------------------------------------
# A placement is validated only where the manual's own location drawing carries a numbered callout whose leader ends on the retained table object
# (checked by eye on the 345 dpi renders: printed 66 for the lower-playfield switches, 70/73 for the coils); every other placement is observed.
PLACEMENT_STATUS_SWITCH: dict[int, str] = {address: "validated" for address in (32, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54)}
PLACEMENT_STATUS_SOLENOID: dict[int, str] = {address: "validated" for address in (6, 8, 13, 17, 19, 21)}
LAMP_PLACEMENT_STATUS = "observed"
# Every switch the ROM names treats public 1 as actuated in its own Switch Levels and Switch Edges tests; bk2kGameData has no inverted-switch
# mask and pinned core_getSwCol returns the matrix bits raw, so the matrix contact is open at rest and closed when actuated.
NORMALLY_CLOSED: dict[int, bool] = {address: False for address in ROM_SWITCH_NAMES}
RUNTIME_SWITCH_NOTE = (
	"In the ROM's own Switch Levels and Switch Edges tests (runtime runs l4-switch-levels and l4-switch-edges) writing public 1 makes the ROM show this "
	"name and the switch number, and public 0 shows nothing, so the ROM treats public 1 as actuated. bk2kGameData has no inverted-switch mask and pinned "
	"core_getSwCol returns the matrix bits raw, so the contact the matrix sees is open at rest and closed when the switch is actuated; the manual prints no "
	"rest state for any matrix contact."
)
DROP_TARGET_NOTE = (
	"Drop-target polarity (runtime runs l4-droptargets-*): the ROM treats public 1 as a dropped target. With every target switch at 0 it fires neither reset "
	"coil in attract mode or at game start; with this bank's switches, or even one of them, held at 1 it fires the bank's reset coil (4 for 41-43, 3 for "
	"44-46) three times after Start, about 1 s apart, and then stops retrying. The matrix is read uninverted, so the contact the matrix sees is open "
	"while the target is up and closes when it drops; the manual prints the opto construction but no rest state."
)
DROP_TARGET_BEHAVIOR = (
	"Runtime (runs l4-droptargets-*, host-held switches, no target ever moves): the ROM reads public 1 on a bank's switches as dropped and fires that "
	"bank's reset coil three times, at about 0.15, 1.3 and 2.3 s after Start, then stops retrying; the count is per bank, not per switch, and with every "
	"switch at 0 no reset fires. After the third attempt the ROM served no ball in any held-switch run and, in four of six runs, later restarted for a "
	"reason these runs do not establish."
)
DRAWBRIDGE_BEHAVIOR = (
	"Runtime (runs l4-motor-bank-* and l4-boot-motor-*, host-written stimuli with no bank model): the ROM's service test 08, MOTOR BANK TEST, energizes "
	"relay 16 and waits for either position switch, 16 (UP) or 24 (DOWN); when it sees one it shows UP or DN, releases the relay about 0.05 s later, "
	"energizes it again about 1.4 s later and waits about 3.4 s for the other switch before showing MOTOR ERROR and releasing the relay (about 6.8 s of "
	"waiting when no switch ever closes). A switch already closed at the start or closed 1 s later is accepted alike, and with both closed the ROM "
	"alternates UP and DN every 1.45 s. At power-up the ROM runs relay 16 for about 7.8 s, about 2 s longer while 16 or 24 is held. These runs do not "
	"establish which physical end each switch marks or whether the relay raises or lowers the targets."
)
FLASHER_PLAYFIELD_BULBS = {25: 2, 26: 2, 27: 2, 30: 2}
FLASHER_EXTRA_NOTES = {
	28: "The script's lights for this flash are named GI14/GI14b (left) and GI15/GI15b (right), which are not members of its G.I. collections; they are driven only by SolFlipLaneFlash. Placed at the two bulbs; the 'b' partners are glow.",
	29: "The script's light for this flash is named GI17 (with glow GI17b), not a member of its G.I. collections; it is driven only by SolDTFlash, which also switches the DisableLighting of four peg plastics.",
	31: "The script's light for this flash is named GI24 (with glow GI24b), not a member of its G.I. collections; it is driven only by SolREjectFlash. The printed name mentions both the right eject and the upper flipper; the Solenoid Table prints one playfield bulb (1p) and two insert-board bulbs (2i), and the table models one bulb.",
	25: "The Big Red Bolt is also lamp 18's insert; the script lights RedBoltFlash and Light18 together from this flash (SolRedBoltFlash).",
	26: "The Big Blue Bolt is also lamp 20's insert; the script lights BlueBoltFlash and Light20 together from this flash (SolBlueBoltFlash).",
}
VIRTUAL_SOLENOIDS = {
	23: ("Game-On / Special-Solenoid Enable", "used", ["internal.game-on-enable"], "CORE_SSFLIPENSOL / S11_GAMEONSOL: the ROM's flipper and special-solenoid enable. It has no driver-board output of its own. In the retained runs it is off in attract mode, on from the moment test mode is entered, and on from the start of a game (runs l4-coil, l4-droptargets-*)."),
	24: ("Unassigned Solenoid Slot 24", "unused", ["internal.unused-platform-slot"], "Reserved gap between the enable (23) and the C-side aliases (25-32); no System 11 driver populates it."),
	33: ("Unused Upper Flipper Slot 33", "unused", ["internal.unused-platform-slot"], "Generic upper-flipper-coil address (CORE_FIRSTUFLIPSOL). bk2kGameData declares FLIP_SWNO(58,57) with no FLIP_SOL bit, so nothing drives 33-36; the upper flipper has no CPU output."),
	34: ("Unused Upper Flipper Slot 34", "unused", ["internal.unused-platform-slot"], "See address 33."),
	35: ("Unused Upper Flipper Slot 35", "unused", ["internal.unused-platform-slot"], "See address 33."),
	36: ("Unused Upper Flipper Slot 36", "unused", ["internal.unused-platform-slot"], "See address 33."),
	37: ("Unused Sound Overlay Slot 37", "unused", ["internal.unused-platform-slot"], "System 11 sound-overlay board range 37-44. bk2kGameData sets gameSpecific1 = S11_MUXSW2 only, without S11_SNDOVERLAY, and the manual lists no sound overlay board, so 37-44 stay zero."),
	38: ("Unused Sound Overlay Slot 38", "unused", ["internal.unused-platform-slot"], "See address 37."),
	39: ("Unused Sound Overlay Slot 39", "unused", ["internal.unused-platform-slot"], "See address 37."),
	40: ("Unused Sound Overlay Slot 40", "unused", ["internal.unused-platform-slot"], "See address 37."),
	41: ("Unused Sound Overlay Slot 41", "unused", ["internal.unused-platform-slot"], "See address 37."),
	42: ("Unused Sound Overlay Slot 42", "unused", ["internal.unused-platform-slot"], "See address 37."),
	43: ("Unused Sound Overlay Slot 43", "unused", ["internal.unused-platform-slot"], "See address 37."),
	44: ("Unused Sound Overlay Slot 44", "unused", ["internal.unused-platform-slot"], "See address 37."),
	45: ("Synthetic Lower Right Flipper Power", "used", ["internal.synthetic-flipper"], "PinMAME fabricates 45/46 from the right flipper button bit at public 82, which core_updateSw also copies into matrix switch 57, because bk2kGameData declares FLIP_SWNO(58,57) with no FLIP_SOL bit. The lower right flipper (FL-11630) is wired from its cabinet switch (Right Flipper circuit Orn-Vio, 1P19-1) with no CPU output; this address is the emulator's view of that button, not a driver. In the ROM's Switch Levels and Switch Edges runs (l4-switch-levels, l4-switch-edges) writing public 82 to 1 raised 45 and 46 together and releasing it dropped them. Whether the upper flipper (the Solenoid Table also lists it under the Right Flipper circuit) belongs to this button is the subject of conflict.upper-flipper-button."),
	46: ("Synthetic Lower Right Flipper Hold", "used", ["internal.synthetic-flipper"], "See address 45."),
	47: ("Synthetic Lower Left Flipper Power", "used", ["internal.synthetic-flipper"], "PinMAME fabricates 47/48 from the left flipper button bit at public 84, which core_updateSw also copies into matrix switch 58. The left cabinet switch (Left Flipper circuit Orn-Gry, 1P19-2) fires the lower left flipper (FL-11630) directly; it has no CPU output. In the ROM's Switch Levels and Switch Edges runs (l4-switch-levels, l4-switch-edges) writing public 84 to 1 raised 47 and 48 together and releasing it dropped them."),
	48: ("Synthetic Lower Left Flipper Hold", "used", ["internal.synthetic-flipper"], "See address 47."),
	49: ("Simulator Ball-Shooter Slot", "unused", ["internal.unused-platform-slot"], "CORE_FIRSTSIMSOL: the PinMAME simulator's fake ball-shooter solenoid, not System 11 hardware."),
	50: ("Unassigned Solenoid Slot 50", "unused", ["internal.unused-platform-slot"], "Gap before the custom-solenoid base; bk2kGameData declares no custom solenoids, so PinMAME models 50 solenoid slots for this game."),
}
COVERAGE_MISSING = ["spatial_placement", "unresolved_conflicts"]
COVERAGE_DIMENSIONS = {
	"catalog_identity": "validated",
	"address_enumeration": "validated",
	"semantic_naming": "validated",
	"physical_wiring": "conflicted",
	"mechanisms": "validated",
	"variant_coverage": "validated",
	"recreation_knowledge": "validated",
	"spatial_placement": "observed",
}
OBSERVED_ONLY_NOTES: list[dict[str, Any]] = []

RUNTIME_LOCATOR = (
	"Pinned LibPinMAME runs of bk2k_l4 from empty NVRAM, each in a new state directory that inherits only the one retained initialization run's NVRAM: the "
	"Coil Test (test 05) paired step by step with the ROM coil table, the 64-lamp Single Lamps test (04), the Switch Levels (06) and Switch Edges (07) "
	"tests swept over 71 public addresses with a same-run control switch, the power-up kicker and motor probes with switches held from start, the "
	"drop-target polarity and reset runs with every combination of held bank switches, and the Motor Bank Test (08) with eight host-written "
	"switch patterns. Raw runs, their hashes and the ROM name tables are retained outside the repository."
)


# --- Lamps (Lamp-Matrix Table printed 68; lamps lists printed 69 and 72) ------------------------
LAMP_LABELS = {
	1: "Ransom R (Speaker Panel)", 2: "Ransom A (Speaker Panel)", 3: "Ransom N (Speaker Panel)", 4: "Ransom S (Speaker Panel)",
	5: "Bolt Circle Center", 6: "Ransom O (Speaker Panel)", 7: "Ransom M (Speaker Panel)", 8: "Last Chance (Left Outlane)",
	9: "U-Turn Bolt (Right)", 10: "Spin Bolt (Ball Popper)", 11: "Lock Bolt (Right Eject)", 12: "BLACK B", 13: "BLACK L",
	14: "BLACK A", 15: "BLACK C", 16: "BLACK K", 17: "Extra Ball Bolt", 18: "Big Red Bolt (UPF)", 19: "Magna Save",
	20: "Big Blue Bolt (UPF)", 21: "Last Chance (Right Outlane)", 22: "U-Turn Bolt (Left)", 23: "Kickback (Left Outlane)",
	24: "Shoot Again", 25: "WIN W Lane (Top UPF)", 26: "WIN I Lane (Top UPF)", 27: "WIN N Lane (Top UPF)",
	28: "WAR W Lane (Bottom UPF)", 29: "WAR A Lane (Bottom UPF)", 30: "WAR R Lane (Bottom UPF)", 31: "Jackpot Bolt",
	32: "Advance Ransom Bolt", 33: "Motor Target Bolt 3 (Left UPF)", 34: "Motor Target Bolt 2 (Left UPF)",
	35: "Motor Target Bolt 1 (Left UPF)", 36: "Bonus 2X", 37: "Bonus 3X", 38: "Bonus Hold", 39: "Bonus 4X", 40: "Bonus 5X",
	41: "KNIGHT G (Right 3-Bank)", 42: "KNIGHT H (Right 3-Bank)", 43: "KNIGHT T (Right 3-Bank)",
	44: "KNIGHT K (Left 3-Bank)", 45: "KNIGHT N (Left 3-Bank)", 46: "KNIGHT I (Left 3-Bank)", 47: "Skyway Bolt",
	48: "Hurry-Up Bolt", 49: "Extra Ball (Bolt Circle)", 50: "50,000 (Bolt Circle)", 51: "Magna Save (Bolt Circle)",
	52: "10,000 (Bolt Circle)", 53: "Multi-Ball (Bolt Circle)", 54: "100,000 (Bolt Circle)", 55: "Ransom (Bolt Circle)",
	56: "200,000 (Bolt Circle)", 57: "Special (Bolt Circle)", 58: "20,000 (Bolt Circle)", 59: "Kickback (Bolt Circle)",
	60: "150,000 (Bolt Circle)", 61: "Drawbridge (Bolt Circle)", 62: "75,000 (Bolt Circle)", 63: "Hurry-Up (Bolt Circle)",
	64: "250,000 (Bolt Circle)",
}
LAMP_MATRIX_WORDING = {
	1: "R (SP)", 2: "A (SP)", 3: "N (SP)", 4: "S (SP)", 5: "Bolt Circle Center", 6: "O (SP)", 7: "M (SP)", 8: "LAST CHANCE (L Outlane)",
	9: "U-Turn Bolt (Right)", 10: "Spin Bolt (Ball Popper)", 11: "Lock Bolt (R Eject)", 12: "B", 13: "L", 14: "A", 15: "C", 16: "K",
	17: "Extra Ball Bolt", 18: "Red Bolt (UPF right)", 19: "Magna Save™", 20: "Blue Bolt (UPF left)", 21: "LAST CHANCE (R Outlane)",
	22: "U-TURN (Left)", 23: "KICKBACK (L Outlane)", 24: "SHOOT AGAIN", 25: "\"W\" Lane (Top UPF)", 26: "\"I\" Lane (Top UPF)",
	27: "\"N\" Lane (Top UPF)", 28: "\"W\" Lane (Btm UPF)", 29: "\"A\" Lane (Btm UPF)", 30: "\"R\" Lane (Btm UPF)", 31: "JACKPOT Bolt",
	32: "ADVANCE RANSOM Bolt", 33: "Motor Target Bolt 3 (L UPF)", 34: "Motor Target Bolt 2 (L UPF)", 35: "Motor Target Bolt 1 (L UPF)",
	36: "2X (left)", 37: "3X", 38: "BONUS HOLD", 39: "4X", 40: "5X (right)", 41: "\"G\" (R 3-Bank Dr Tgt)", 42: "\"H\" (R 3-Bank Dr Tgt)",
	43: "\"T\" (R 3-Bank Dr Tgt)", 44: "\"K\" (L 3-Bank Dr Tgt)", 45: "\"N\" (L 3-Bank Dr Tgt)", 46: "\"I\" (L 3-Bank Dr Tgt)",
	47: "SKYWAY Bolt", 48: "HURRY-UP Bolt", 49: "EXTRA BALL (Bolt Circle)", 50: "50,000 (Bolt Circle)", 51: "MAGNA SAVE (Bolt Circle)",
	52: "10,000 (Bolt Circle)", 53: "MULTI-BALL (Bolt Circle)", 54: "100,000 (Bolt Circle)", 55: "RANSOM (Bolt Circle)",
	56: "200,000 (Bolt Circle)", 57: "SPECIAL (Bolt Circle)", 58: "20,000 (Bolt Circle)", 59: "KICKBACK (Bolt Circle)",
	60: "150,000 (Bolt Circle)", 61: "Drawbridge (Bolt Circle)", 62: "75,000 (Bolt Circle)", 63: "HURRY-UP (Bolt Circle)",
	64: "250,000 (Bolt Circle)",
}
# The lamps lists (printed 69 and 72) print only lamps 5, 8-17, 18-35 and 36-64; lamps 1-4, 6, 7 and 19 are the matrix's own (SP) cells and the Magna Save lamp.
LAMP_LIST_WORDING = {
	5: "Center, Bolt Circle", 8: "LAST CHANCE (L Outlane)", 9: "U-TURN Bolt (Right)", 10: "SPIN Bolt", 11: "LOCK Bolt (R Eject Hole)",
	12: "B (in \"BLACK\")", 13: "L (in \"BLACK\")", 14: "A (in \"BLACK\")", 15: "C (in \"BLACK\")", 16: "K (in \"BLACK\")",
	17: "EXTRA BALL Bolt", 18: "Big Red Bolt", 19: "MAGNA SAVE™", 20: "Big Blue Bolt", 21: "LAST CHANCE (R Outlane)",
	22: "U-TURN Bolt (Left)", 23: "KICKBACK Bolt (L Outlane)", 24: "SHOOT AGAIN", 25: "W (in \"WIN\")", 26: "I (in \"WIN\")",
	27: "N (in \"WIN\")", 28: "W (in \"WAR\")", 29: "A (in \"WAR\")", 30: "R (in \"WAR\")", 31: "JACKPOT Bolt", 32: "ADVANCE RANSOM Bolt",
	33: "Motor Target Bolt 3", 34: "Motor Target Bolt 2", 35: "Motor Target Bolt 1", 36: "2X (left)", 37: "3X", 38: "BONUS HOLD",
	39: "4X", 40: "5X (right)", 41: "G (R 3-b Dr Tgt)", 42: "H (R 3-b Dr Tgt)", 43: "T (R 3-b Dr Tgt)", 44: "K (L 3-b Dr Tgt)",
	45: "N (L 3-b Dr Tgt)", 46: "I (L 3-b Dr Tgt)", 47: "SKYWAY Bolt", 48: "HURRY-UP Bolt",
}
LAMP_COLUMN_WIRING = {
	1: ("YEL-BRN", "1J7-1", "Q66"), 2: ("YEL-RED", "1J7-2", "Q64"), 3: ("YEL-ORN", "1J7-3", "Q62"), 4: ("YEL-BLK", "1J7-4", "Q60"),
	5: ("YEL-GRN", "1J7-6", "Q58"), 6: ("YEL-BLU", "1J7-7", "Q56"), 7: ("YEL-VIO", "1J7-8", "Q54"), 8: ("YEL-GRY", "1J7-9", "Q52"),
}
LAMP_ROW_WIRING = {
	1: ("RED-BRN", "1J6-1", "Q80"), 2: ("RED-BLK", "1J6-2", "Q81"), 3: ("RED-ORN", "1J6-3", "Q82"), 4: ("RED-YEL", "1J6-5", "Q83"),
	5: ("RED-GRN", "1J6-6", "Q84"), 6: ("RED-BLU", "1J6-7", "Q85"), 7: ("RED-VIO", "1J6-8", "Q86"), 8: ("RED-GRY", "1J6-9", "Q87"),
}
SPEAKER_PANEL_LAMPS = {1, 2, 3, 4, 6, 7}
UPPER_PLAYFIELD_LAMPS = {18, 20} | set(range(25, 36))


# --- Helpers ---------------------------------------------------------------------------------
def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Black Knight 2000 retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Black Knight 2000 extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Black Knight 2000 retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(extraction_root)):
		raise RuntimeError(f"Black Knight 2000 retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Black Knight 2000 retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "validated") -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": {"status": status, "source_refs": list(source_refs)}})
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def output_id(label: str) -> str:
	return "device." + "-".join("".join(character if character.isalnum() else " " for character in label.casefold()).split())


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	status = extra.pop("provenance_status", "validated")
	device: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address}, "availability": availability, "provenance": provenance(*refs, status=status)}
	device.update(extra)
	return device


# (name, locator, image_derivation or None); derivation strings are copied from tools/render_excerpt_image.py's output.
_MANUAL_NAME = "Williams_1989_Black_Knight_2000_Operations_Manual.pdf"
EXCERPTS = (
	("solenoid-table", "PDF page 33, printed 29, Black Knight 2000 Solenoid Table and notes",
		_MANUAL_NAME + " page 33, crop box 0.115,0.285,0.91,0.775, scanned page rendered at its native resolution (embedded image xref 128, 2492px across 7.15in), rendered at 118 dpi, capped to 800px wide, grayscale, 801x639 WebP quality 45"),
	("solenoid-locations", "PDF page 77 (printed 73, Lower Playfield Solenoids/Flashers) and PDF page 75 (printed 71, Upper Playfield Parts and Solenoids/Flashers)",
		_MANUAL_NAME + " page 77, crop box 0.03,0.03,0.98,0.7, scanned page rendered at its native resolution (embedded image xref 304, 2821px across 8.05in), rendered at 322 dpi, capped to 2600px wide, grayscale, 2601x2374 WebP quality 80"),
	("switch-matrix", "PDF page 71, printed 67, Black Knight 2000 Switch-Matrix Table (foldout copy on PDF page 101)",
		_MANUAL_NAME + " page 71, crop box 0.07,0.63,0.91,0.95, scanned page rendered at its native resolution (embedded image xref 280, 2598px across 7.63in), rendered at 182 dpi, capped to 1300px wide, grayscale, 1301x642 WebP quality 50"),
	("switch-locations", "PDF page 70 (printed 66, Lower Playfield Switches) and PDF page 76 (printed 72, Upper Playfield Switches)",
		_MANUAL_NAME + " page 70, crop box 0.03,0.04,0.98,0.94, scanned page rendered at its native resolution (embedded image xref 276, 2614px across 7.68in), rendered at 322 dpi, capped to 2600px wide, grayscale, 2601x3189 WebP quality 80"),
	("lamp-matrix", "PDF page 72, printed 68, Black Knight 2000 Lamp-Matrix Table (foldout copy on PDF page 101)",
		_MANUAL_NAME + " page 72, crop box 0.07,0.63,0.9,0.95, scanned page rendered at its native resolution (embedded image xref 284, 2686px across 7.78in), rendered at 170 dpi, capped to 1200px wide, grayscale, 1201x600 WebP quality 50"),
	("lamp-locations", "PDF page 73 (printed 69, Lower Playfield Lamps) and PDF page 76 (printed 72, Upper Playfield Lamps)",
		_MANUAL_NAME + " page 73, crop box 0.03,0.02,0.98,0.8, scanned page rendered at its native resolution (embedded image xref 288, 2566px across 7.50in), rendered at 322 dpi, capped to 2600px wide, grayscale, 2601x2764 WebP quality 80"),
	("lower-playfield-parts", "PDF page 74, printed 70, Lower Playfield Parts list and numbered drawing", None),
	("flipper-wiring", "PDF page 80 (printed 76, Cabinet Wiring), PDF page 97 (Interconnect Board Interboard Signals), PDF pages 52-53 (printed 48-49, Lower Right Flipper, Lower Left Flipper, Upper Right Flipper); image: the flipper section of printed 76",
		_MANUAL_NAME + " page 80, crop box 0.08,0.36,0.95,0.58, scanned page rendered at its native resolution (embedded image xref 316, 2507px across 7.56in), rendered at 332 dpi, grayscale, 2455x804 WebP quality 80"),
	("mechanism-assemblies", "PDF pages 55-58, 60-62, 68 and 69, printed 51-54, 56-58, 64 and 65: trough switches, knocker, shooter-lane feeder, outhole kicker, jet bumper, eject hole, ramps, 3-bank drop target and opto board, moving targets and motor, Magna Save and high-current driver", None),
	("kickback-and-ball-popper", "71-page April 1989 edition, PDF page 57: Kickback Assembly B-12671 and Ball Popper Assembly D-11335-2", None),
	("operator-message", "An Important Message To Operators, printed pages 1, 3, 4, 5 and 9 (PDF pages 3, 5, 6, 7 and 11): selected passages", None),
)


def _excerpt(name: str, locator: str, derivation: str | None, *, method: str = "manual", transcribed_by: str = "curator, read from the rendered page") -> dict[str, Any]:
	text_path = EXCERPT_DIRECTORY / f"{name}.md"
	record: dict[str, Any] = {
		"id": f"excerpt.black-knight-2000.{name}",
		"locator": locator,
		"path": text_path.relative_to(ROOT).as_posix(),
		"sha256": hashlib.sha256(text_path.read_bytes()).hexdigest(),
	}
	if derivation is not None:
		image_path = EXCERPT_DIRECTORY / f"{name}.webp"
		record["image"] = image_path.relative_to(ROOT).as_posix()
		record["image_sha256"] = hashlib.sha256(image_path.read_bytes()).hexdigest()
		record["image_derivation"] = derivation
	record.update({"method": method, "transcribed_by": transcribed_by, "reviewed": True})
	return record


def _manual_excerpts(names: tuple[str, ...]) -> list[dict[str, Any]]:
	return [_excerpt(name, locator, derivation) for name, locator, derivation in EXCERPTS if name in names]


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned PinmameGetGames catalog records for the eight-driver bk2k_* clone tree rooted at bk2k_l4",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c: INITGAME(bk2k,GEN_S11B,s11_dispS11b2,12,FLIP_SWNO(58,57),S11_LOWALPHA|S11_DISPINV,S11_MUXSW2) (no "
				"sxx.ssSw map, no custom solenoids, no sound overlay), the bk2k_* ROM sets, CORE_GAMEDEF(bk2k,l4) and the seven "
				"CORE_CLONEDEFs, input_ports_bk2k = input_ports_s11; src/wpc/s11.c: s11_dispS11b2 (two 16-character sixteen-segment rows), "
				"MACHINE_INIT(s11)'s bk2k_ block typing 9 'Backbox GI', 10 'Upper Playfield GI' and 11 'Lower Playfield GI' as reverse-acting "
				"#44 G.I. and the 25-32 mux bank as #89 flashers, SWITCH_UPDATE(s11) copying the mux relay's state into switch 2 under "
				"S11_MUXSW2, setSSSol's WMS ssSolNo {5,4,1,2,0,3} special-solenoid map, updsol's A/C mux copy, and the switch read returning "
				"core_getSwCol without inversion; src/wpc/s11.h S11_COMPORTS and S11_SWADVANCE/-UPDN/-CPUDIAG/-SOUNDDIAG; src/wpc/core.c "
				"core_updateSw's FLIP_SWNO flipper copy and synthetic 45-48 states; src/wpc/core.h CORE_SSFLIPENSOL, CORE_FIRSTLFLIPSOL, "
				"CORE_FIRSTSIMSOL; src/wpc/driver.c lines 2725-2732 (the bk2k driver list with its 04/89 dates)."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
			"locator": "System 11 sequential switch/lamp matrices, dedicated diagnostic inputs, A/C mux, special-solenoid, and per-game G.I. address rules",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": f"{WAYBACK_PREFIX}{IPDB_FILES}Williams_1989_Black_Knight_2000_Operations_Manual.pdf",
			"original_filename": "Williams_1989_Black_Knight_2000_Operations_Manual.pdf", "sha256": MANUAL_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				"Williams Black Knight 2000 operations manual (IPDB's 'Operations Manual' file, 102 pages, Acrobat Distiller 5.0 PDF dated 2002-03-05, "
				"image-only bilevel scan at roughly 345 ppi; IPDB machine 311, https://www.ipdb.org/machine.cgi?id=311: Williams 'Black Knight 2000', "
				"April 28, 1989, model 563, MPU Williams System 11B, 5,703 units). The PDF was retrieved from the Internet Archive's Wayback Machine "
				"capture of the IPDB file (the capture of the machine page is 20251206013004) because IPDB is Cloudflare-gated. PDF page = printed "
				"page + 4 for Section 2's numbered pages (printed 66 = PDF 70) and PDF page 33 = printed 29; the PDF has no text layer, so every "
				"cited cell was read from a 345 dpi render. PDF page 59 (the page after the ramp assemblies) is blank in this edition. Retained "
				"locally under external:pinmame-manuals/by-machine/williams.black-knight-2000.1989/ipdb-311/."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; file hosted by the Internet Pinball Database", "rights": "NOASSERTION",
			"excerpts": _manual_excerpts(("solenoid-table", "solenoid-locations", "switch-matrix", "switch-locations", "lamp-matrix", "lamp-locations", "lower-playfield-parts", "flipper-wiring", "mechanism-assemblies")),
		},
		{
			"id": MANUAL_APRIL_SOURCE, "kind": "manual", "uri": f"{WAYBACK_PREFIX}{IPDB_FILES}Williams_1989_Black_Knight_2000_Manual.pdf",
			"original_filename": "Williams_1989_Black_Knight_2000_Manual.pdf", "sha256": MANUAL_APRIL_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				"Williams Black Knight 2000 'Pinball Game Operation Manual' 16-563-101 (April 1989), 71 pages, image-only 200 dpi bilevel scan "
				"with no text layer: the same file the Internet Archive holds as item arcademanual_Black_Knight_2000_OPS "
				"(Black_Knight_2000_OPS.pdf, SHA-1 6f861ddbe70951caaedc59f5a6406ec229dc9ca9, identical to this file's). Sections 1 and 2 only. "
				"Used only for the Kickback and Ball Popper assembly page (PDF 57), which the 102-page edition prints blank."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; file hosted by the Internet Pinball Database and the Internet Archive", "rights": "NOASSERTION",
			"excerpts": _manual_excerpts(("kickback-and-ball-popper",)),
		},
		{
			"id": OPERATOR_SOURCE, "kind": "manual", "uri": f"{WAYBACK_PREFIX}{IPDB_FILES}Williams_1989_Black_Knight_2000_An_Important_Message_To_Operators.pdf",
			"original_filename": "Williams_1989_Black_Knight_2000_An_Important_Message_To_Operators.pdf", "sha256": OPERATOR_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				"'An Important Message To Operators of Black Knight 2000' signed by Steve Ritchie, 22 pages, image-only bilevel scan (Canon iR3035, "
				"2010), IPDB machine 311's file of that name. Describes the game's play features and its two new electromechanical devices; "
				"used for mechanism context only, never for addresses."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; file hosted by the Internet Pinball Database", "rights": "NOASSERTION",
			"excerpts": _manual_excerpts(("operator-message",)),
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:pinmame-review-artifacts/williams.black-knight-2000.1989/runtime-stage/rom-name-tables/",
			"revision": "bk2k_u27.l4",
			"locator": (
				"Switch and coil name tables of the program ROM of every bk2k_* set in the local corpus (l4, la2, lg3, pa5, pa7, pu1), decoded by "
				"tools/bk2k_rom_name_tables.py (through tools/s11_rom_name_tables.py): the switch table runs in public-address order and the coil table in "
				"coil-test order. The member that holds them is the one named u27 in these sets. The decoded JSON per set is retained outside the repository; the excerpt lists "
				"the ROM member SHA-256s and every entry."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games program ROMs, user-authorized local copies; ROM bytes are not redistributed",
			"excerpts": [_excerpt("rom-name-tables", "bk2k_l4 switch table entries 1-59 at U27 offset 0x283a and coil table entries 1-30 at 0x1da2, with the differing entries of the other five loadable sets", None, method="mixed", transcribed_by="tools/bk2k_rom_name_tables.py, reviewed by curator")],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{L4_RUNTIME_PATH}", "revision": PINMAME_REVISION,
			"locator": RUNTIME_LOCATOR,
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/black-knight-2000-1989/source/Black%20Knight%202000%201.1.vpx",
			"original_filename": "Black Knight 2000 1.1.vpx", "sha256": TABLE_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				f"Retained Black Knight 2000 recreation by Flupper (version 1.1, a VP10 rebuild of lio's 2003 RC2 VP8 table; the contributor's collection "
				f"holds three byte-identical copies under 'Black Knight 2000 1.1.vpx', 'Black Knight 2000 (1989).vpx' and the Tables Archive's "
				f"'Black Knight 2000 1.1.vpx'). Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/954 and y/2052. Geometry "
				"authority for named table objects only."
			),
			"license": "NOASSERTION", "attribution": "lio (original VP8 table); Flupper (VPX version); upper and lower playfield redraw by Tomasaco; script review and DOF by Ninuzzu", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/black-knight-2000-1989/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True, "acquired_at": ACQUIRED_AT,
			"locator": (
				"Retained embedded script (45,205 bytes). Runtime authority: cGameName = \"bk2k_l4\" with HandleMech = 0; SolCallback 1-4, 6-8, 10-14, 16, "
				"25-32 and sLRFlipper/sLLFlipper; the three-ball trough (swTrough1-3 = 11-13, drain 10), right eject saucer (40/8), ball popper (47/6), two "
				"cvpmDropTarget banks (KNI 44-46 reset by 3, GHT 41-43 reset by 4), cvpmVLock upper-playfield lock (36-38, released by 7), cvpmMech "
				"Mech3Bank (switches 16/24, driven by 16), cvpmMagnet MagnaSave (driven by 15), and LampTimer's LightType bindings of lamps 1-64."
			),
			"license": "NOASSERTION", "attribution": "lio (original VP8 table); Flupper (VPX version); upper and lower playfield redraw by Tomasaco; script review and DOF by Ninuzzu", "rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI,
			"original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads at runtime (script.vbs line 142 LoadVPM \"00990300\", \"S11.VBS\", 3.10; S11.VBS "
				"executes core.vbs), retained from the contributor's working installation together with core.vbs (SHA-256 "
				f"{VPM_CORE_SHA256}). S11.VBS defines swLRFlip = 82 and swLLFlip = 84 and sets them from the flipper keys in vpmKeyDown/vpmKeyUp; core.vbs "
				"routes KeyDownHandler/KeyUpHandler to them. The retained library is v3.61, newer than the 3.10 the table asks for."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt(
					"vpm-script-library-flippers",
					"s11.vbs lines 37-40, 69-86 and 104-121; core.vbs lines 2061-2062, 2090, 2111-2117 and 2854-2855; script.vbs lines 142, 148, 251, 257, 267-268, 371-383 and 517-518",
					None, transcribed_by="curator, read from the library and script files",
				),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/black-knight-2000-1989/extracted-vpxtool.manifest.json", "acquired_at": ACQUIRED_AT,
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, "
				f"produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	]



def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column + 1]
	return_wire, return_connection = SWITCH_ROW_WIRING[row + 1]
	return {
		"board": "System 11B CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "driver_transistor": f"column {drive_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role, note) in DEDICATED_SWITCHES.items():
		items.append(_device(
			f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}], normally_closed=False, roles=[role],
			physical={"location": "coin door diagnostic switch assembly / CPU board", "switch_type": "button" if address != -6 else "other", "notes": note + " Read from System 11's dedicated column, not the playfield matrix."},
			spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
		))
	for address in range(1, 65):
		column, row = divmod(address - 1, 8)
		identifier = f"switch.matrix-{address}"
		unused = address in UNUSED_SWITCHES
		label = f"Not Used (Matrix Position {address})" if unused else SWITCH_LABELS[address]
		notes = [f"Printed switch-matrix column {column + 1} ({SWITCH_COLUMN_WIRING[column + 1][0]}), row {row + 1} ({SWITCH_ROW_WIRING[row + 1][0]})."]
		if address in ROM_SWITCH_NAMES:
			notes.append(f"The bk2k_l4 switch table names it \"{ROM_SWITCH_NAMES[address]}\".")
		elif address == 2:
			notes.append("The bk2k_l4 switch table leaves entry 2 blank.")
		else:
			notes.append("The bk2k_l4 switch table leaves this entry blank.")
		if address in (57, 58):
			notes.append(
				f"In the ROM's Switch Levels and Switch Edges tests (runs l4-switch-levels and l4-switch-edges) public {82 if address == 57 else 84} makes it show "
				f"\"{ROM_SWITCH_NAMES[address]}\" and {address}, and public 1 on the matrix address itself is overwritten by the flipper column on the next update."
			)
		elif address in ROM_SWITCH_NAMES:
			notes.append(RUNTIME_SWITCH_NOTE)
		elif address in (14, 15, 56):
			notes.append("In the ROM's Switch Levels and Switch Edges tests (runs l4-switch-levels and l4-switch-edges) public 1 makes the ROM show this number with no name, so it scans the position but has nothing to call it.")
		elif address >= 60:
			notes.append("In the ROM's Switch Levels and Switch Edges tests (runs l4-switch-levels and l4-switch-edges) writing public 1 changes nothing, so the ROM does not read this position.")
		if address in MATRIX_WORDING:
			notes.append(f"The matrix table (printed 67) prints \"{MATRIX_WORDING[address]}\".")
		if address in LIST_WORDING:
			notes.append(f"The switches lists (printed 66 and 72) print \"{LIST_WORDING[address]}\".")
		if address == 34:
			notes.append(
				"The Moving Target Assembly's parts page (printed 58) lists A-11177-1 as the left target assembly and A-11315-3 as the mid and right target "
				"assembly, which would make the middle target A-11315-3; the Upper Playfield Switches list (printed 72) prints A-11177-1 for 34. The record follows the "
				"switch list for the part number, and the difference does not reach a recreation."
			)
		physical: dict[str, Any] = {}
		if address in SWITCH_PARTS:
			physical["part_number"] = SWITCH_PARTS[address]
		if address in SWITCH_TYPES:
			physical["switch_type"] = SWITCH_TYPES[address]
		elif SWITCH_PARTS.get(address, "").startswith(MICROSWITCH_PART_PREFIX):
			physical["switch_type"] = "microswitch"
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]}
		availability = "used"
		if unused:
			availability = "unused"
			notes.append("Both the matrix table and the switches lists leave this position empty (\"Not Used\" or blank), and no ROM name or script binding names it.")
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, ROM_SOURCE)
		elif address == 2:
			notes.append(
				"The switches list prints item 2 as the \"C-side: A/C Relay\" contact on the Aux Power Driver Board (part of D-12247); the matrix "
				"table's \"C Side Power A/C Relay\" names the same thing. bk2kGameData sets S11_MUXSW2, so pinned SWITCH_UPDATE(s11) overwrites "
				"public switch 2 with the live state of solenoid 12 every update; a recreation reads it and never drives it."
			)
			extra["roles"] = ["internal.ac-relay-feedback"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
			refs = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
		elif address in CABINET_SWITCH_ROLES:
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			if address == 5:
				availability = "optional"
				notes.append("The switches list prints \"Not Used (USA)\" as its part number: US machines ship a two-chute door, so the center chute is fitted only on other doors.")
			if address in (4, 6):
				notes.append("The switches list and the ROM put the right chute on 4 and the left on 6, and the cabinet wiring drawing (printed 76) draws 7SW4 as the Right Coin Chute; the matrix table prints them the other way round. The list, the ROM and the drawing are followed.")
			if address == 9:
				notes.append("The retained script never asserts it; its nudge tilt is the plumb bob, vpmNudge.TiltSwitch = 1.")
				refs = refs + (VPX_SCRIPT_SOURCE,)
			if address == 1:
				notes.append("The retained script uses it as the nudge tilt (vpmNudge.TiltSwitch = 1).")
				refs = refs + (VPX_SCRIPT_SOURCE,)
			if address == 59:
				notes.append(
					"The Magna Save button on the right side of the cabinet forward of the flipper button (operator message, printed 3). It fires nothing "
					"by itself: the ROM energizes the Magna Save driver (15) while the button is held and the feature is lit. The retained script "
					"writes Controller.Switch(59) directly from its RightMagnaSave key (script.vbs lines 375 and 382)."
				)
				refs = refs + (OPERATOR_SOURCE, VPX_SCRIPT_SOURCE)
			if address in (57, 58):
				side = "right" if address == 57 else "left"
				notes.append(
					f"The switches list names it \"{side[0].upper()} Flipper Lane Change\" with footnote **1, \"Optotransistor on Backbox Interconnect "
					f"Bd\" (part of D-12313); the manual does not say more about how it senses the {side} flipper button. The cabinet switch itself "
					f"(SW-10A-48) fires the flipper coil directly. bk2kGameData declares FLIP_SWNO(58,57) without FLIP_SOL, so pinned core_updateSw "
					f"rewrites this address from the {side} flipper button bit on every update: public 1 means the button is pressed, a host write "
					f"here is overwritten, and a consumer presses the {side} flipper through public {82 if address == 57 else 84}. The retained "
					f"script never writes it; its flipper keys reach S11.VBS vpmKeyDown/vpmKeyUp, which drive public 82/84 "
					f"(switch.flipper-column-82/84)."
				)
				refs = refs + (VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE)
		else:
			if address in UNPLACED_SWITCHES:
				notes.append(UNPLACED_SWITCHES[address])
			elif address in SWITCH_POSITIONS:
				object_name = SWITCH_POSITIONS[address][0]
				if address in SWITCH_PROJECTIONS:
					notes.append(SWITCH_PROJECTIONS[address])
				elif address in TRIGGER_NAMES:
					notes.append(f"Placed at the retained table object {object_name}, the trigger the script closes {address} from ({TRIGGER_NAMES[address]}).")
				else:
					notes.append(f"Placed at the retained table object {object_name}.")
			if address in (22, 24):
				notes.append(
					f"The retained script's start-up block writes Controller.Switch({address}) = 1 with the comments \"close coin door\" and \"and keep it close\" "
					"(script.vbs lines 267-268), left over from a WPC template whose coin-door switch sits at 22: on this machine it holds "
					f"{'Left UPF Loop End' if address == 22 else 'the Motor Targets DOWN limit'} closed from power-up until the table's own events rewrite it. That is a defect of the retained table, "
					"not a fact about the machine."
				)
			if address in (41, 42, 43, 44, 45, 46):
				notes.append(DROP_TARGET_NOTE)
				refs = refs + (RUNTIME_SOURCE,)
			refs = refs + (VPX_SCRIPT_SOURCE,)
			if address in UNPLACED_SWITCHES:
				pass
			else:
				status = PLACEMENT_STATUS_SWITCH.get(address, "observed")
				extra["spatial"] = located(identifier, "sensor", [SWITCH_POSITIONS[address][1:]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status=status)
		physical["notes"] = " ".join(notes)
		extra["physical"] = physical
		extra["wiring"] = _switch_wiring(address)
		if availability in ("used", "optional") and address in NORMALLY_CLOSED:
			extra["normally_closed"] = NORMALLY_CLOSED[address]
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))
	items.append(_device(
		"switch.dip-0", "Country Jumper (USA/Germany)", "dip_switch", "pinmame.input.dip", 0, "used", (CONTROLLER_SOURCE, CORE_SOURCE),
		aliases=[{"namespace": "pinmame.dip", "value": "0"}],
		physical={"location": "System 11B CPU board", "switch_type": "dip", "notes": "S11 input port 1 'Country' jumper (0 = USA, 1 = Germany), read by the ROM through PIA2."},
		spatial=not_applicable("dip_switch", CORE_SOURCE),
	))
	items.extend(flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP_SWNO(58,57)",
		core_refs=(CORE_SOURCE, CONTROLLER_SOURCE), button_refs=(VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE),
		button_notes={
			side: (
				f"The retained known-working script drives it: BK2K_KeyDown/BK2K_KeyUp hand the {side} flipper key to vpmKeyDown/vpmKeyUp "
				f"(script.vbs lines 377 and 383), which set Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} (excerpt vpm-script-library-flippers). "
				f"The physical counterpart is the {side} cabinet flipper button, which fires its coil"
				f"{'s' if side == 'left' else ''} directly and is sensed by the Flipper Lane Change optotransistor at matrix "
				f"{58 if side == 'left' else 57}."
			)
			for side in ("left", "right")
		},
		unused_notes={
			address: note + (
				" The retained table's script contains no NoUpperLeftFlipper/NoUpperRightFlipper call and defines neither cSingleLFlip nor cSingleRFlip "
				"(it is Option Explicit, so core.vbs's cvpmFlips2.Init skips its own call), which leaves both solenoid numbers at their defaults: the "
				"library therefore does write this address when a staged flipper key is pressed, and the machine ignores it."
			)
			for address, note in vpm_staged_flipper_notes().items()
		},
		unused_note_refs=(VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE),
	))
	return items



def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []

	def emit(identifier: str, label: str, kind: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> None:
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))

	def rom_note(address: int) -> str:
		return f" The bk2k_l4 coil table names the matching step \"{ROM_COIL_NAMES[address]}\", and the ROM's Coil Test (run l4-coil) pulses this address in that step." if address in ROM_COIL_NAMES else ""

	def callback_note(address: int) -> str:
		return f" Retained script: {SOLENOID_CALLBACKS[address]}." if address in SOLENOID_CALLBACKS else ""

	for address, (label, kind, wire, control, power, driver, part) in SOLENOID_A.items():
		identifier = output_id(label)
		notes = f"Solenoid Table entry {address:02d}A (Switched): pulsed while the A/C select relay (12) is released." + rom_note(address) + callback_note(address)
		wiring = {"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": wire, "control_connection": control, "power_connection": power}
		refs = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = refs + (VPX_SCRIPT_SOURCE,)
		physical: dict[str, Any] = {}
		if part:
			physical["part_number"] = part
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}A"}], "wiring": wiring}
		availability = "used"
		if address == 5:
			availability = "unused"
			notes += (
				" The table prints 05A \"Not Used\" with no part, and the lower- and upper-playfield solenoid lists omit it; its driver Q31 and harness "
				"pin exist only for the C side (29). The ROM's Coil Test still pulses it for about 0.1 s at step 05 A SIDE, which the coil table names UNUSED; a pulse is ROM activity, not proof of a load."
			)
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, ROM_SOURCE)
		elif address == 3 or address == 4:
			side = "left" if address == 3 else "right"
			notes += f" Resets the {side} 3-bank drop-target bank (C-11223-1, item 9 in the lower-playfield drawing)."
			object_name, positions = SOLENOID_POSITIONS[address]
			notes += f" Placed at {object_name}."
			extra["spatial"] = located(identifier, "effect", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status="observed")
		else:
			object_name, positions = SOLENOID_POSITIONS[address]
			notes += f" Placed at {object_name}."
			if address == 7:
				notes += (
					" The Solenoid Table prints AE-24-900 for 07A, while the Upper Playfield Solenoids/Flashers list prints AE-23-800 for \"3-Ball Lock "
					"Kickback\" and the Kickback Assembly's own parts page (B-12671) prints AE-23-800. The record follows the list and the assembly's own "
					"page, two sources against the table's one; the coil winding is not something a recreation can express, so the disagreement is stated "
					"here and not recorded as a conflict. The Upper Playfield Parts list prints the same assembly B-12671 as item 1 \"3-Ball Lockup Kickback\"."
				)
				extra["roles"] = ["mechanism.lock-release"]
			if address == 8:
				notes += " The Solenoids/Flashers lists print \"Right Eject Hole\" AE-26-1500 and the Eject Hole Arm Assembly (B-9361-R-5) lists AE-26-1500; the Solenoid Table prints Right Eject, AE-26-1500."
			if address == 2:
				notes += " The shooter-lane feeder assembly (C-9638) is item 31 in the lower-playfield drawing."
			if address == 6:
				notes += " The Ball Popper Assembly D-11335-2 is item 17 in the lower-playfield drawing."
			if address in POWER_UP_KICKERS:
				notes += POWER_UP_KICKERS[address]
			extra["spatial"] = located(identifier, "effect", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status=PLACEMENT_STATUS_SOLENOID.get(address, "observed"))
		physical["notes"] = notes
		extra["physical"] = physical
		emit(identifier, label, kind, address, availability, refs, **extra)

	for address, (label, kind, wire, control, power, driver, part) in SOLENOID_CONTROLLED.items():
		identifier = output_id(label)
		notes = f"Solenoid Table entry {address:02d} (Controlled)." + rom_note(address) + callback_note(address)
		wiring = {"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": wire, "control_connection": control, "power_connection": power}
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = refs + (VPX_SCRIPT_SOURCE,)
		physical: dict[str, Any] = {}
		if part:
			physical["part_number"] = part
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}], "wiring": wiring}
		availability = "used"
		if address in (9, 10, 11):
			relay_board = {9: "C-11998-1 (4a), mounted inside the insert board", 10: "C-11998-1 (4a), on the playfield underside", 11: "C-11902-1 (4b), on the playfield underside"}[address]
			notes += (
				f" A 24 V relay on the {relay_board} per the Solenoid Table's note 4 and the lists' footnotes. G.I. is lit while the relay is released "
				"and dark while it is energized: pinned s11.c types the address as reverse-acting #44 G.I., and the retained script turns its lights off "
				"when the callback is enabled."
			)
		if address == 9:
			extra["roles"] = ["gi.insert-board"]
			notes += " The insert board is the backbox lamp insert behind the backglass; pinned s11.c calls it 'Backbox GI'. The retained table does not model it."
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 10:
			extra["roles"] = ["gi.upper-playfield"]
			notes += f" The retained table's lightsGIupf collection holds {len(GI_UPPER)} bulbs for it (one point per bulb, glow partners merged); the manual prints no G.I. bulb count."
			extra["spatial"] = located(identifier, "emitter", [(x, y) for _, x, y in GI_UPPER], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE, status="observed")
			physical["quantity"] = len(GI_UPPER)
		elif address == 11:
			extra["roles"] = ["gi.lower-playfield"]
			notes += f" The retained table's lightsGIlpf collection holds {len(GI_LOWER)} bulbs for it (one point per bulb, glow partners merged); the manual prints no G.I. bulb count."
			extra["spatial"] = located(identifier, "emitter", [(x, y) for _, x, y in GI_LOWER], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE, status="observed")
			physical["quantity"] = len(GI_LOWER)
		elif address == 12:
			extra["roles"] = ["internal.ac-select-relay"]
			notes += " Mounted on the Aux Power Driver board (D-12247) in the backbox. Released, drives 1-8 reach their A-side loads; energized, the same drives reach the C-side loads published as 25-32. Its C-side power contact is read back as switch 2."
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 14:
			notes += " The Solenoids/Flashers list prints \"Knocker/Ticket Dispenser (b)\" for the Controlled entry (and the Upper Playfield list's Backbox Solenoids table prints Knocker 14, AE-23-800): the same drive serves a ticket dispenser where one is fitted. A cabinet device."
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 15:
			extra["roles"] = ["mechanism.magna-save"]
			notes += (
				" The High Current Driver C-12493 (a TIP36C, 220 ohm base resistor and 1N4004 flyback diode; its connector J1 pins 5/6, 1 and 3/4 take "
				"RED-WHT from 5J11-12, BRN-VIO from 1J12-8 and BLK from 5J11-7) switches the Magna Save coil (A-12831, a larger 50 V coil per the operator message). "
				"The Solenoid Table prints C-12493 in its coil-part column."
			)
			object_name, positions = SOLENOID_POSITIONS[address]
			notes += f" Placed at {object_name}."
			extra["spatial"] = located(identifier, "effect", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status=PLACEMENT_STATUS_SOLENOID.get(address, "observed"))
		elif address == 16:
			extra["roles"] = ["mechanism.drawbridge-motor"]
			notes += (
				" A 24 V relay on relay board C-11902-1 (4b) that switches the 11 RPM Moving Target Assembly motor (14-7941-3, Motor Assembly B-12465); "
				"the motor's cam closes the UP (16) and DOWN (24) snap-action switches. The retained script's SolMTargets only plays the drawbridge "
				"sound; Mech3Bank (cvpmMech linear, length 60, 50 steps, one solenoid) turns the relay's state into target travel."
			)
			extra["spatial"] = located(identifier, "effect", [(0.288858, 0.226458)], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status="observed")
			notes += " Placed at the middle drawbridge-target wall (DBTrgt2) the table's motor model moves; the motor itself is under the upper playfield and no source draws its position."
			notes += " " + DRAWBRIDGE_BEHAVIOR
		else:
			object_name, positions = SOLENOID_POSITIONS[address]
			notes += f" Placed at {object_name}."
			extra["spatial"] = located(identifier, "effect", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status=PLACEMENT_STATUS_SOLENOID.get(address, "observed"))
			if address == 13:
				notes += " The Left Outlane Kickback assembly is item 4 (B-11873-1) in the lower-playfield drawing; the lower-playfield list calls it the left outlane's kickback and the operator message describes it as the automatic KICKBACK on the left side drain."
		physical["notes"] = notes
		extra["physical"] = physical
		emit(identifier, label, kind, address, availability, refs, **extra)

	for address, (label, wire, control, power, driver, part, special) in SOLENOID_SPECIAL.items():
		identifier = output_id(label)
		notes = f"Solenoid Table entry {address} (Special #{special}); pinned setSSSol maps the special-solenoid PIA outputs onto 17-22 in Special #1-#6 order." + rom_note(address) + callback_note(address)
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Special #{special}"}],
			"wiring": {"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": wire, "control_connection": control, "power_connection": power},
		}
		if address == 22:
			availability = "unused"
			kind = "coil"
			notes += " The Solenoid Table prints 22 \"Not Used\" with no part and the solenoid lists omit it; Special #6's driver Q79 and harness pin exist but carry no load. The ROM's Coil Test still pulses it for about 0.1 s at step 22, which the coil table names UNUSED; a pulse is ROM activity, not proof of a load."
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, ROM_SOURCE)
			refs = refs
			extra["physical"] = {"notes": notes}
			emit("device.not-used-special-solenoid-06", label, kind, address, availability, refs, **extra)
			continue
		kind = "coil"
		notes += (
			f" Placed at {SOLENOID_POSITIONS[address][0]}" + (" (manual coil drawing: 17 left, 19 upper right, 21 lower bumper)." if address in (17, 19, 21) else ".")
		)
		if address == 21:
			notes += " The Solenoid Table and the Upper Playfield Solenoids/Flashers list both print \"Lower Jet Bumper\"; the retained script's Bumper3 is the same bumper."
		extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address][1], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status=PLACEMENT_STATUS_SOLENOID.get(address, "observed"))
		extra["physical"] = {"part_number": part, "notes": notes}
		emit(identifier, label, kind, address, "used", refs, **extra)

	for address, (label, availability, roles, note) in VIRTUAL_SOLENOIDS.items():
		refs = (CONTROLLER_SOURCE, CORE_SOURCE) + ((RUNTIME_SOURCE,) if address == 23 else ())
		emit(
			output_id(label), label, "virtual", address, availability, refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}], roles=roles, physical={"notes": note},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)

	for address, (label, wire, cpu, power, lamp_type, playfield_bulbs, insert_bulbs) in SOLENOID_C.items():
		identifier = output_id(label)
		a_address = address - 24
		notes = (
			f"Solenoid Table entry {a_address:02d}C (Switched): driver {SOLENOID_A[a_address][5]} of {a_address:02d}A routed to this load while the "
			f"A/C select relay (12) is energized; pinned updsol publishes it as {address}. {lamp_type}, {playfield_bulbs}p,{insert_bulbs}i "
			f"(the table's own legend: i = insert board, p = playfield): {playfield_bulbs} on the playfield and {insert_bulbs} in the backbox insert board."
			+ rom_note(address) + callback_note(address)
		)
		refs = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		object_name, positions = SOLENOID_POSITIONS[address]
		if address in PARTLY_PLACED_FLASHERS:
			notes += " Only the playfield bulbs the table models are placed: " + PARTLY_PLACED_FLASHERS[address] + "."
		else:
			notes += f" Placed at {object_name}."
		notes += (
			" The retained script drives only its own light objects for this flash; the matching backbox insert-board bulbs (the \"i\" count) flash "
			"in sync with it per IPDB's notes and are backbox hardware without a playfield coordinate."
		)
		if address in FLASHER_EXTRA_NOTES:
			notes += " " + FLASHER_EXTRA_NOTES[address]
		emit(
			identifier, label, "flasher", address, "used", refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{a_address:02d}C"}],
			physical={"quantity": playfield_bulbs + insert_bulbs, "notes": notes},
			wiring={"board": "System 11B CPU board", "driver_transistor": SOLENOID_A[a_address][5], "drive_wire": wire, "power_connection": f"{power}, CPU {cpu}"},
			spatial=located(identifier, "emitter", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status=PLACEMENT_STATUS_SOLENOID.get(address, "observed")),
		)
	return sorted(items, key=lambda item: item["binding"]["device"])


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, row = divmod(address - 1, 8)
		identifier = f"lamp.matrix-{address}"
		notes = [f"Printed lamp-matrix column {column + 1}, row {row + 1}."]
		if address in LAMP_MATRIX_WORDING:
			notes.append(f"The matrix table (printed 68) prints \"{LAMP_MATRIX_WORDING[address]}\".")
		if address in LAMP_LIST_WORDING:
			notes.append(f"The lamps lists (printed 69 and 72) print \"{LAMP_LIST_WORDING[address]}\".")
		refs: tuple[str, ...] = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": {
				"board": "System 11B CPU board", "drive_wire": LAMP_COLUMN_WIRING[column + 1][0], "drive_connection": LAMP_COLUMN_WIRING[column + 1][1],
				"driver_transistor": f"column {LAMP_COLUMN_WIRING[column + 1][2]}, row {LAMP_ROW_WIRING[row + 1][2]}",
				"return_wire": LAMP_ROW_WIRING[row + 1][0], "return_connection": LAMP_ROW_WIRING[row + 1][1],
			},
		}
		if address in SPEAKER_PANEL_LAMPS:
			notes.append(
				"One of the six R-A-N-S-O-M letters in the speaker/display panel under the score displays (\"SP = Speaker Panel\"; the lamps list's note says "
				"\"Switches 1 - 4 and 6 - 7 are on the Speaker/Display Panel (R-A-N-S-O-M)\"). The retained script lights it through a backbox Flasher object "
				"(the FlasherR/A/N/S/O/M set, labelled \"Backbox\" in its LightType table)."
			)
			extra["roles"] = ["cabinet.speaker-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			object_name = LAMP_POSITIONS[address][0]
			if address in UPPER_PLAYFIELD_LAMPS:
				notes.append("An upper-playfield lamp (the matrix legend's UPF; the retained table models the upper playfield in the same x/y frame, offset in height).")
			if address == 19:
				notes.append(
					"The Magna Save lamp, on the lower playfield per the matrix legend. The retained script lights the Magna Save ready sign (Light19/Light19b, "
					"the bulbyellow primitive and two peg plastics) from it (LightType 1); it is placed at Light19, the lamp's own light object."
				)
			if object_name.endswith("b"):
				notes.append(
					f"Placed at the retained bulb light {object_name}, this lamp's illumination source (is_bulb_light, a small circular bulb shape). The table also draws the "
					f"insert as the textured render overlay {object_name[:-1]} (is_bulb_light false, a playfield-image layer); that overlay is not a bulb object and is not "
					"used for the position."
				)
			else:
				notes.append(f"Placed at the retained bulb light {object_name} (is_bulb_light), this lamp's own light object; the table also lights a {object_name}b partner for it.")
			extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address][1:]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status=LAMP_PLACEMENT_STATUS)
		notes.append(f"In the ROM's Single Lamps test (run l4-single-lamps, step {address}) it is the one lamp that blinks and the ROM calls it '{ROM_LAMP_NAMES[address]}' (the display draws 0 as O and 5 as S).")
		refs = refs + (RUNTIME_SOURCE,)
		physical = {"quantity": 1}
		physical["notes"] = " ".join(notes)
		extra["physical"] = physical
		items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
	return items



def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.upper-alphanumeric", "label": "Upper sixteen-character alphanumeric display", "kind": "segment",
			"controller_index": 0, "segment_start": 0, "width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE), "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
		{
			"id": "display.lower-alphanumeric", "label": "Lower sixteen-character alphanumeric display", "kind": "segment",
			"controller_index": 1, "segment_start": 20, "width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE), "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly:
			record["assembly_part_number"] = assembly
		return record

	return [
		mechanism(
			"mechanism.trough", "Outhole and three-ball trough", "kicker",
			[output_id("Outhole Kicker"), output_id("Ball Release (Shooter Lane Feeder)")], ["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13", "switch.matrix-53"],
			"A drained ball rests on the outhole switch (10); the Outhole Kicker (1, assembly B-8039-2) kicks it into the trough, which holds three balls "
			"on Trough 3 (13, left), Trough 2 (12) and Trough 1 (11, right) (the Ball Trough Switches page, printed 51: two 5647-09957-00 micro-switches "
			"for the center and left positions, one A-11680 right switch). The Ball Release / Shooter Lane Feeder (2, assembly C-9638) feeds the ball at 11 "
			"into the shooter lane (53), and the stack rolls down. The retained script creates its three balls on a cvpmTrough whose switches are the "
			"numbers 11-13 and whose entry switch is 10.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="B-8039-2",
		),
		mechanism(
			"mechanism.eject-hole", "Right eject hole (Knight's Challenge)", "kicker", [output_id("Right Eject")], ["switch.matrix-40"],
			"A ball in the right eject hole (assembly B-9361-R, item 23 in the lower-playfield drawing, with a red plastic seat) closes 40; the Right Eject "
			"coil (8, AE-26-1500, Eject Hole Arm Assembly B-9361-R-5) kicks it back out. The operator message describes it as the right side kick-out hole "
			"that a U-turn shot lights for 2-ball DOUBLE KNIGHT'S CHALLENGE multi-ball, where the locked ball waits and a second ball appears at the plunger.",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="B-9361-R-5",
		),
		mechanism(
			"mechanism.ball-popper", "Ball popper (spin lane)", "kicker", [output_id("Ball Popper")], ["switch.matrix-47"],
			"The Ball Popper Assembly D-11335-2 (item 17 in the lower-playfield drawing, at the head of the skyway ramp) holds a ball over its switch-and-diode "
			"assembly A-11658 (47); the Ball Popper coil (6, AE-23-800) lifts it to the upper playfield. The operator message says the ball lands in the popper "
			"from the SPIN lane when it is lit, one of the Lightning Wheel's awards is given, and the ball is popped up to the upper playfield directed at the flipper.",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="D-11335-2",
		),
		mechanism(
			"mechanism.left-drop-targets", "Left 3-bank drop targets (K-N-I)", "drop_target_bank", [output_id("Left 3-Bank Drop Target Reset")],
			["switch.matrix-44", "switch.matrix-45", "switch.matrix-46"],
			"Three drop targets (C-11223-1) lettered K (lower, 44), N (middle, 45) and I (upper, 46), sensed by the opto interrupters of a C-12559 board; "
			"the reset coil (3, AE-26-1200) raises all three through one reset plate. The operator message says completing the KNIGHT banks lights MAGNA-SAVE and "
			"the left kickback and advances B-L-A-C-K, and that the two banks are timed independently. " + DROP_TARGET_BEHAVIOR,
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, assembly="C-11223-1",
		),
		mechanism(
			"mechanism.right-drop-targets", "Right 3-bank drop targets (G-H-T)", "drop_target_bank", [output_id("Right 3-Bank Drop Target Reset")],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43"],
			"Three drop targets (C-11223-1) lettered G (left, 41), H (middle, 42) and T (right, 43), sensed by the opto interrupters of a second C-12559 board; "
			"the reset coil (4, AE-26-1200) raises all three. " + DROP_TARGET_BEHAVIOR,
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, assembly="C-11223-1",
		),
		mechanism(
			"mechanism.drawbridge-targets", "Drawbridge moving target bank", "motorized", [output_id("Motor Targets (UPF) Relay")],
			["switch.matrix-16", "switch.matrix-24", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"The Moving Target Assembly (C-12464) on the upper playfield carries three targets (33 upper, 34 middle, 35 lower) that a Motor Assembly (B-12465: an 11 RPM motor, cam and a snap-action switch with roller 5647-12073-06) raises and lowers, "
			"switched by the Motor Targets relay (16). The assembly's parts page (printed 58) lists A-11177-1 as the left target assembly and A-11315-3 as the "
			"mid and right target assembly, while the Upper Playfield Switches list (printed 72) prints A-11177-1 for 33 and 34 and A-11315-3 for 35, so the "
			"two disagree about the middle target; a recreation cannot express the difference. The UP (16) and DOWN (24) switches report the two ends of the travel. The operator message calls it a "
			"three-target version of the Pin-Bot five-target raising/lowering motor bank and says the targets must be completed to gain access to the "
			"Drawbridge ramp. The retained script models it as a cvpmMech (linear, length 60, 50 steps, one solenoid): position 0 closes 16 and position 50 "
			"closes 24, the targets are dropped from position 49 and raised at 0. " + DRAWBRIDGE_BEHAVIOR,
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, assembly="C-12464",
		),
		mechanism(
			"mechanism.upper-lock", "Upper playfield three-ball lock", "kicker", [output_id("UPF Lockup Kickback")],
			["switch.matrix-31", "switch.matrix-36", "switch.matrix-37", "switch.matrix-38"],
			"The Upper Playfield Parts page lists a 3-Ball Lockup Kickback (B-12671, solenoid 07A) and a 3-Ball Lockup Wire Ramp (B-12693). A ball entering the "
			"wire ramp closes the UPF Wire Ramp Entry switch (31, 5647-12073-01) and reaches the Drawbridge lock, whose three positions are sensed by the Lower "
			"(36), Middle (37) and Upper (38) lock switches (5647-12073-22); the kickback releases the locked balls. The operator message says shooting three "
			"balls up the Drawbridge starts 3-ball multi-ball and that LAST CHANCE releases any locked balls on the last ball. The retained script models it as a "
			"cvpmVLock released by solenoid 7.",
			MANUAL_SOURCE, MANUAL_APRIL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="B-12671",
		),
		mechanism(
			"mechanism.kickback", "Left outlane kickback", "kicker", [output_id("Kickback (Left Outlane)")], ["switch.matrix-39"],
			"The Left Outlane Kickback assembly (B-11873-1, item 4 in the lower-playfield drawing) kicks a ball in the left outlane (39) back to the playfield "
			"when the Kickback coil (13, AE-23-800) fires. The operator message says the automatic KICKBACK can be set on or off at the start of every ball, "
			"for the first ball only, or earned by the player. The retained script enables its Kickback kicker for 500 ms when the coil is energized.",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE,
		),
		mechanism(
			"mechanism.magna-save", "Magna Save", "other", [output_id("Magna Save Driver")], ["switch.matrix-59"],
			"The Magna Save Assembly (A-12831: bracket and pole plus a larger 50 V coil-magnet and breaker) at the right drain is driven by the High Current "
			"Driver (C-12493, solenoid 15). The player holds the Magna Save button (59) on the right side of the cabinet forward of the flipper button; the "
			"magnet freezes the ball before it drains and the ball is returned to the lower right flipper (operator message, printed 3).",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="A-12831",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Lower Jet Bumper")], ["switch.matrix-17", "switch.matrix-19", "switch.matrix-21"],
			"Special solenoids 17 (left), 19 (right) and 21 (lower) fire the jet bumpers (B-9414-2); their skirt switches carry the same numbers, 17, 19 and 21 "
			"(B-8928). Pinned bk2kGameData has no sxx.ssSw map, so the ROM, not a switch-to-coil wire, fires each bumper.",
			MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, assembly="B-9414-2",
		),
		mechanism(
			"mechanism.slingshots", "Slingshots", "other", [output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-18", "switch.matrix-20"],
			"Special solenoids 18 (left) and 20 (right), AE-26-1500, kick from the slingshots (Kicker Arm Assembly B-12665, item 6 in the lower-playfield drawing); "
			"each has a paired actuating switch (A-4834-H; A-11538-1) read as 18 and 20.",
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly="B-12665",
		),
		mechanism(
			"mechanism.u-turn", "U-turn loop", "other", [], ["switch.matrix-49", "switch.matrix-50", "switch.matrix-51", "switch.matrix-52"],
			"Four wire-form switches (5647-12073-19) along the U-turn loop at the center of the lower playfield: 49 (lower left), 50 (upper left), 51 (upper right) "
			"and 52 (lower right). The operator message says making repetitive U-turn shots lights MULTI-BALL for a timed interval and that a U-turn shot "
			"lights the right side kick-out hole for 2-ball multi-ball.",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE,
		),
		mechanism(
			"mechanism.skyway", "Skyway ramp", "other", [], ["switch.matrix-32"],
			"The long Skyway ramp on the left of the lower playfield (Skyway Ramp Assembly B-12636, item 16; entry plate 01-9122) brings the ball to the upper playfield; "
			"its Lower Ramp Exit switch (32, subminiature switch 5647-12073-20) is read when a ball leaves it. The operator message says the top of the ramp "
			"must be slightly above or even with the edge of the upper playfield's wood surface.",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="B-12636",
		),
		mechanism(
			"mechanism.upper-playfield-loops", "Upper playfield loops and lanes", "other", [], [
				"switch.matrix-22", "switch.matrix-23", "switch.matrix-25", "switch.matrix-26", "switch.matrix-27",
				"switch.matrix-28", "switch.matrix-29", "switch.matrix-30",
			],
			"The upper playfield carries a loop with two end switches (Left UPF Loop End 22 and Right UPF Loop End 23), the W-I-N lanes (25-27, top) and the "
			"W-A-R lanes (28-30, bottom). The operator message says three consecutive loops light Bonus X holdover, that the W-I-N lanes advance the bonus "
			"multiplier to 5X and light Ransom, and that W-A-R during normal play lights HURRY UP in the Skyway ramp.",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE,
		),
		mechanism(
			"mechanism.lightning-wheel", "Lightning Wheel lamp ring", "other", [], [],
			"The Lightning Wheel is the operator message's name for a 'wheel of fortune' award feature with sixteen awards: the bolt-circle inserts around the "
			"center of the lower playfield (lamps 49-64). The message lists the awards in the order lamps 49 to 64 print them (EXTRA BALL, 50,000, MAGNA-SAVE, "
			"10,000, MULTI-BALL, 100,000, RANSOM, 200,000, SPECIAL, 20,000, KICKBACK, 150,000, DRAWBRIDGE, 75,000, HURRY UP, 250,000) starting at the top of "
			"the wheel, and says it spins when the ball is shot into the lit SPIN lane and lands in the ball popper. It is a lamp animation, not a moving part: "
			"neither the manual nor the script has a motor, switch or coil for it.",
			MANUAL_SOURCE, OPERATOR_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.flippers", "Three flippers", "other", [], ["switch.matrix-57", "switch.matrix-58"],
			"Lower right and lower left flippers (C-11626-R-3 / C-11626-L-3, FL-11630 coils) and an upper flipper on the right of the upper playfield (D-12702-R-1, "
			"FL-11630). Each flipper assembly has an end-of-stroke switch (03-7811) that opens the power winding and is not in the switch matrix. The CPU sees only "
			"the lane-change optos 57/58 (and PinMAME's synthetic 45-48). In PinMAME a consumer presses the flippers through public 82 (right) and 84 (left); "
			"core_updateSw copies them to 57/58 every update and overwrites any direct write there. Which cabinet button fires the upper flipper is open: "
			"see conflict.upper-flipper-button.",
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.ac-relay-switch-2", "kind": "direct", "source": output_id("A/C Select Relay"), "destination": "switch.matrix-2",
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		},
		*flipper_column_relationships(
			flip_swno=FLIP_SWNO, matrix_ids={57: "switch.matrix-57", 58: "switch.matrix-58"}, refs=(CORE_SOURCE,),
		),
	]



def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.upper-flipper-button",
			"path": "inputs.switch.matrix-57 / inputs.switch.matrix-58 and outputs.synthetic flipper states 45-48",
			"description": (
				"Which cabinet flipper button fires the upper-playfield flipper (D-12702-R-1, a right-hand flipper that its parts page and the Upper Playfield "
				"Parts list call the Upper Right Flipper) is not settled by the manual's own pages. The Solenoid Table (printed 29) groups it under the "
				"\"Right Flipper\" circuit (Orn-Vio, 1P19-1, 2J5-5: 2J10-7) with the coil connection [2J10-4: 2J8-12] and wire [Blk-Yel]. The Cabinet "
				"Wiring drawing (printed 76) draws the contact that feeds 2J10 pin 4 as the \"Upr Left Flipper Button\", a second contact on the left "
				"flipper circuit (2J10-8, Orn-Gry from 1P19-2) beside the \"Lwr Left Flipper Button\", and labels the wire on 2J8 pin 12 BLK-BLU, not "
				"Blk-Yel. The Interconnect Board Interboard Signals table (PDF page 97) prints 2J8-12 and 2J10-4 as No Connection, so the board list gives "
				"that coil no cabinet-switch lead at all. Only the Lower Right Flipper assembly (C-12898) lists a \"Flipper Switch\" SW-1A-183 (item 26, on "
				"switch plate 01-3670) and a Blue/Yellow wire (item 24, the same colour as the +50 Vdc flipper supply BLU/YEL at 2J8-9 and 2J5-2); the Lower "
				"Left and Upper Right assemblies mark items 24-26 Not Used. The retained known-working script moves URightFlipper from its right-flipper "
				"solenoid callback (SolRFlipper), that is, from the right button, and secondary web reports describe the upper flipper as chained from the "
				"lower right flipper's stroke; those reports are leads, not authority. Those facts are consistent with the upper flipper firing from the "
				"right button through a switch in the lower right assembly, but the cabinet drawing and the Solenoid Table's connector column, which are "
				"wiring documents of equal rank, say otherwise, so the question stays open. PinMAME cannot arbitrate: the driver declares FLIP_SWNO(58,57) "
				"with no FLIP_SOL, so the CPU neither fires nor reads any flipper coil, and the synthetic 45-48 states follow only the lower buttons. A "
				"recreation must choose a button for the upper flipper. "
				"Resolution path: continuity or a photograph of an unrestored machine's lower-right flipper assembly harness (does the SW-1A-183 stage switch "
				"carry the Blue/Yellow lead to the upper flipper coil?) and of the cabinet flipper-switch contacts on 2J10, or a play video that shows which "
				"button raises the upper flipper."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
		},
	]


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items: list[dict[str, Any]] = []
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


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Black Knight 2000", "manufacturer": "Williams", "year": 1989, "kind": "physical_pinball",
			"ipdb_id": 311, "opdb_id": "GrxPP-Ml91r",
			"playfield": {"width": TABLE_WIDTH, "height": TABLE_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": STATUS,
			"missing": COVERAGE_MISSING,
			"dimensions": COVERAGE_DIMENSIONS,
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
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Black Knight 2000 device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	unresolved_inputs: list[int] = []
	observed_inputs: list[int] = []
	placement_count = 0
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
			placement_count += len(spatial["placements"])
			if spatial["status"] != "validated":
				observed_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	observed_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	unresolved_outputs: list[dict[str, Any]] = []
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
			placement_count += len(spatial["placements"])
			if spatial["status"] != "validated":
				observed_outputs.append(binding)
	key = lambda item: (item["group"], item["address"])
	return {
		"format": "pinmame-spatial-audit" if STATUS == "author_ready" else "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": STATUS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": TABLE_WIDTH, "bottom": TABLE_HEIGHT},
			"x": "x/954; 0=left, 1=right",
			"y": "y/2052; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/black-knight-2000-1989/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {"embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256, "table_sha256": TABLE_SHA256},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=key),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=key) for reason, bindings in sorted(not_applicable_outputs.items())},
		"unresolved": [{"group": "pinmame.input.switch", "address": address} for address in sorted(unresolved_inputs)] + sorted(unresolved_outputs, key=key),
		"observed_only": OBSERVED_ONLY_NOTES + [
			{"group": "pinmame.input.switch", "addresses": sorted(observed_inputs), "reason": "Placement status is observed, not validated: each rests on a retained-table object whose side and order the manual's drawings agree with, with a projection or centroid where the sensor itself is not modelled."},
			{"group": "pinmame.output", "addresses": sorted(item["address"] for item in observed_outputs), "reason": "Placement status is observed, not validated (flasher glow objects, centroids, G.I. collections, lamp light objects, coil projections)."},
		],
		"partly_placed": [
			{"group": "pinmame.output.solenoid", "address": address, "printed_quantity": FLASHER_PLAYFIELD_BULBS[address], "placed": 1, "reason": reason}
			for address, reason in sorted(PARTLY_PLACED_FLASHERS.items())
		],
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())
		] + [
			{"group": "pinmame.output.solenoid", "address": 3, "reason": "Left Drop Target Reset placed on the middle target (sw5) of the bank it resets."},
			{"group": "pinmame.output.solenoid", "address": 4, "reason": "Right Drop Target Reset placed on the middle target (sw2) of the bank it resets."},
			{"group": "pinmame.output.solenoid", "address": 16, "reason": "Motor Targets relay placed on the middle drawbridge-target wall (DBTrgt2) the table's motor model moves."},
		],
		"ordering_decisions": [
			"Coin chutes follow the switches list, the ROM and the cabinet wiring drawing (4 right, 6 left) over the matrix table's reversed pair.",
			"Drawbridge targets follow the matrix and list (33 upper, 34 middle, 35 lower), which the retained table's DBTrgt1-3 walls agree with; the ROM numbers them UPPER TARGET 3, 2, 1 for 33, 34, 35.",
			"Jet bumpers: switches 17/19/21 and coils 17/19/21 are the left, right and lower bumpers; the retained table's Bumper1/2/3 are the same left-to-right order and the script pulses 17, 19 and 21 from them.",
		],
		"visual_review_cache": {"root": "external:pinmame-manuals/by-machine/williams.black-knight-2000.1989/ipdb-311/"},
		"excluded_object_classes": [
			"Light<n>b glow lights co-located with Light<n> (same lamp's glow)",
			"RanSom backbox FlasherR/A/N/S/O/M objects (speaker-panel lamps 1-4, 6, 7)",
			"Primitives and Flasher sprites of the table (Flasher1 ambience sprite, PegPlastic*, bulbyellow)",
			"Glowball*, forglowball and other ball-glow helper lights",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Black Knight 2000 (Williams, 1989) spatial review",
		"",
		f"Status: {report['status']}.",
		"",
		f"Geometry comes from the retained known-working Flupper 1.1 table (SHA-256 `{TABLE_SHA256}`), whose embedded script (SHA-256 "
		f"`{SCRIPT_SHA256}`) is the runtime authority. Exact bounds are `{TABLE_BOUNDS}`; every coordinate is x/954 and y/2052. The retained table models the "
		"split-level playfield in one x/y frame. The Williams operations manual is the physical authority; its location drawings were used to check sides and order, "
		"not to measure positions, except where a measured reconciliation is named below.",
		"",
		"## Evidence decisions",
		"",
	]
	lines += [f"- {decision}" for decision in report["ordering_decisions"]]
	lines += [
		"- Speaker-panel R-A-N-S-O-M lamps (1-4, 6, 7), the insert-board G.I. (9), the knocker (14) and the A/C relay (12) take controlled non-playfield records.",
		"- G.I. strings 10 and 11 are placed at the retained lightsGIupf and lightsGIlpf collections' bulbs; the manual prints no G.I. bulb count.",
		"",
		"## Blocking gaps",
		"",
	]
	lines += [f"- Solenoid {entry['address']}: {entry['printed_quantity']} playfield bulbs printed, {entry['placed']} placed; {entry['reason']}." for entry in report["partly_placed"]]
	lines += [f"- {entry['group']} {', '.join(str(address) for address in entry['addresses'])}: {entry['reason']}" for entry in report["observed_only"]]
	lines += [
		"",
		"## Explicit projections",
		"",
	]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved records: {len(report['unresolved'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Manual SHA-256 `{MANUAL_SHA256}`; committed excerpts under `evidence/excerpts/{MACHINE_ID}/`.",
		f"- Runtime evidence `{L4_RUNTIME_PATH}`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	write_json(definition_path, definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return definition_path


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		raise RuntimeError(f"Stale Black Knight 2000 definition is still present: {stale}")
	expected = canonical_bytes(build())
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Black Knight 2000 definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Black Knight 2000 seed is not byte-identical to the canonical definition: {seed_path}")
	report = build_spatial_report(build())
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Black Knight 2000 spatial report drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Black Knight 2000 spatial review drifted from its deterministic curator: {markdown_path}")
	print("Black Knight 2000 definition, seed, and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, and spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Black Knight 2000 extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Black Knight 2000 retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
