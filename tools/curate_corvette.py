"""Curate the physical Bally Corvette (1994) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived fact
as a literal, so regeneration reproduces the canonical artifact byte-for-byte without reading the external evidence roots.
``--check`` refuses drift, and ``--regenerate`` is the only path that writes the definition, its knowledge note and its
spatial report.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
import drawing_callouts


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "bally.corvette.1994"
PARTIAL_PATH = ROOT / "machines/partial/bally/corvette-1994.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/corvette-1994.json"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/corvette-1994.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/bally/corvette-1994.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/corvette-1994.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/corvette-1994.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/bally/corvette-1994-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/bally/corvette-1994-callouts.json"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
IDENTITY_SOURCE = "identity.bally.corvette.1994"
MANUAL_SOURCE = "manual.bally.corvette.1994"
AMENDMENT_SOURCE = "manual-amendment-16-9890.bally.corvette.1994"
DISASSEMBLY_SOURCE = "unit-disassembly-16-9887.bally.corvette.1994"
EDGES_SOURCE = "runtime.corvette.switch-edges"
SOLENOID_TEST_SOURCE = "runtime.corvette.solenoid-test"
FLASHER_TEST_SOURCE = "runtime.corvette.flasher-test"
FLIPPER_TEST_SOURCE = "runtime.corvette.flipper-coil-test"
GI_TEST_SOURCE = "runtime.corvette.gi-test"
LAMP_TEST_SOURCE = "runtime.corvette.single-lamps"
ENGINE_TEST_SOURCE = "runtime.corvette.engine-test"
ENGINE_FAILED_SOURCE = "runtime.corvette.engine-test-no-mech"
ZR1_ADJUST_SOURCE = "runtime.corvette.zr1-adjust"
RACE_TEST_SOURCE = "runtime.corvette.race-test"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-security"
VPX_TABLE_SOURCE = "vpx-table.corvette-1-4-2"
VPX_SCRIPT_SOURCE = "vpx-script.corvette-1-4-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.corvette-1-4-2"
CALLOUT_SOURCE = "drawing-callouts.corvette.2026-10-17"

TABLE_NAME = "Corvette (Bally 1994).vpx"
TABLE_SHA256 = "4b500c6b33b280b0076e49b2e817fad2d1131095efeb57fd58bd160b7d8a010c"
SCRIPT_SHA256 = "d30534b6664ed214a3c8b33597ab1021bcc66e979363611e218d4fccb35e5bb5"
PLAYFIELD_WIDTH = 979.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=979 bottom=2162"
EXTRACTION_FILE_COUNT = 1390
EXTRACTION_TOTAL_BYTES = 235785204
EXTRACTION_MANIFEST_SHA256 = "4ea1e9978b46256fc5ed1f8776dabb543cc5a78ecbd578c7546f29125ee74b89"
EXTRACTION_RELATIVE_PATH = Path("bally/corvette-1994/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/corvette-1994/extracted-vpxtool.manifest.json")

MANUAL_NAME = "Bally_1994_Corvette_Manual.pdf"
MANUAL_SHA256 = "60a87faf6ef22fec895f5c5adde5a92bff731e34d54fb838af1b29d3bd428e34"
AMENDMENT_NAME = "Bally_1994_Corvette_Manual_Amendment_16_9890.pdf"
AMENDMENT_SHA256 = "7f37f597ef259c9da3a976eeb22a9321ac287e1abe6c536415a666fbc5ee9d42"
DISASSEMBLY_NAME = "Bally_1994_Corvette_Unit_Disassembly_For_Repair_16_9887.pdf"
DISASSEMBLY_SHA256 = "c683b5e88bde5381119e2b4879abfb61794331a0f9ee5f778a0ef3edb9d2f5ff"
IPDB_PAGE_SHA256 = "1ae235354bcbb96c241d1dd181f1582f7bbed71319fd62aefcfbc41b22bd553a"
MANUALS_DIRECTORY = "pinmame-manuals/by-machine/bally.corvette.1994/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=570"
ACQUIRED_AT = "2026-10-16T19:37:00Z"
RIGHTS_NOTE = "Midway Manufacturing Company (trade name Bally); scan hosted by the Internet Pinball Machine Database"

EXCERPT_ROOT = ROOT / "evidence/excerpts" / MACHINE_ID

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("corv_21", "corv_px3", "corv_px4", "corv_px5", "corv_la1", "corv_lx1", "corv_dx1", "corv_la2", "corv_lx2", "corv_f61")
SAME_MAP = " Pinned corv.c declares it on wpc_mSecurityS with the same corvGameData I/O map as corv_21."
PROTOTYPE = (
	" IPDB quotes the designer: the first design had drop targets and a four-speed shifter on the cabinet, seventeen prototypes "
	"were built and some carried those features, so a prototype ROM may expect hardware the production machine lacks; no retained "
	"source says what this ROM was built for, and its physical compatibility stays unknown."
)
DRIVER_COMPATIBILITY = {
	"corv_21": ("identical", "Game ROM 2.1 (corv_2_1.rom) with the corvsnd2-7 sound ROMs, the parent driver; it identifies itself as CORVETTE / 50036 REV. 2.1 and every service-test run behind this definition booted it."),
	"corv_la1": ("identical", "L-1 production game ROM, LA build (u6-la1.rom), with sound L-1 (su2-sl1.rom); an exploratory boot identifies it as CORVETTE / 50036 REV. LA-1 and opens the same menu path." + SAME_MAP),
	"corv_lx1": ("identical", "L-1 production game ROM, LX build (u6-lx1.rom; IPDB lists LX-1 as the export game ROM), with sound L-1." + SAME_MAP),
	"corv_la2": ("identical", "L-2 production game ROM, LA build (u6-la2.rom), with sound L-1." + SAME_MAP),
	"corv_lx2": ("identical", "L-2 production game ROM, LX build (u6-lx2.rom), with sound L-1; an exploratory boot identifies it as CORVETTE / 50036 REV. LX-2 and opens the same menu path." + SAME_MAP),
	"corv_dx1": ("identical", "DX-1, the community LED Ghost Fix revision of the LX build (u6-dx1.rom), which changes lamp-matrix timing against LED ghosting and no controller address or playfield device." + SAME_MAP),
	"corv_px3": ("unknown", "PX-3 prototype game ROM (u6-px3.rom) with the prototype sound ROM su2-sp2.rom." + SAME_MAP + PROTOTYPE),
	"corv_px4": ("unknown", "PX-4 prototype game ROM (u6-px4.rom; IPDB lists PX-4 as the prototype export game ROM)." + SAME_MAP + PROTOTYPE),
	"corv_px5": ("unknown", "PX-5, which pinned corv.c comments as PX-4 with the LED Ghost Fix (u6-px5.rom)." + SAME_MAP + PROTOTYPE),
	"corv_f61": ("identical", "FreeWPC 0.61 community firmware (corf0_61.rom) with the corvsnd2-7 sound ROMs: an independently written game program for the unmodified physical machine, on the same generation, display and sound hardware and the same addresses; only its rules and display content differ." + SAME_MAP),
}

# --- Switch data (switch-matrix.md, switch-locations.md, section-3-boards.md) ---------------------------
# address -> (switch part cell, printed description) from the Switch Locations list (2-46, 2-47).
SWITCH_LOCATIONS = {
	11: ("5647-12693-32", "Left Out Lane"), 12: ("5647-12693-19", "Right Out Lane"), 13: ("20-9663-2", "Start Button"),
	14: ("A-15361", "*Plumb Bob Tilt"), 15: ("5647-12693-32", "Plunger"), 16: ("5647-12693-19", "Left Return Lane"),
	17: ("5647-12693-19", "Right Return Lane"), 18: ("5647-12693-60", "Spinner"), 21: ("A-17238", "*Slam Tilt"),
	22: ("5643-09288-00", "*Coin Door Closed"), 23: ("20-9663-18", "Buy In Button"), 24: ("5643-09112-00", "*Always Closed"),
	25: ("---", "1st Gear (optional)"), 26: ("---", "2nd Gear (optional)"), 27: ("---", "3rd Gear (optional)"), 28: ("---", "4th Gear (optional)"),
	31: ("A-18617 / A-18618", "Trough Ball 1 (LED) / (Transistor)"), 32: ("A-18617 / A-18618", "Trough Ball 2 (LED) / (Transistor)"),
	33: ("A-18617 / A-18618", "Trough Ball 3 (LED) / (Transistor)"), 34: ("A-18617 / A-18618", "Trough Ball 4 (LED) / (Transistor)"),
	35: ("A-16908 / A-16909", "Route 66 Entry (LED) / (Transistor)"), 36: ("A-16908 / A-16909", "Pit Stop Popper (LED) / (Transistor)"),
	37: ("A-18617 / A-18618", "Trough Eject (LED) / Trough Eject ((Transistor)"), 38: ("5647-12693-31", "Inner Loop Entry"),
	41: ("A-16908 / A-16909", "ZR-1 Bottom Entry (LED) / (Transistor)"), 42: ("A-16908 / A-16909", "ZR-1 Top Entry (LED) / (Transistor)"),
	43: ("A-16908 / A-16909", "Skid Pad Entry (LED) / (Transistor)"), 44: ("5647-12693-21", "Skid Pad Exit"), 45: ("5647-12693-21", "Route 66 Exit"),
	46: ("A-19294", "Left Standup 3"), 47: ("A-19294", "Left Standup 2"), 48: ("A-19294", "Left Standup 1"),
	51: ("A-19141", "Left Race Start"), 52: ("A-19141", "Right Race Start"), 55: ("A-18821", "Left Race Encoder"),
	56: ("A-18821", "Right Race Encoder"), 57: ("5647-12693-21", "Route 66 Kickout"), 58: ("5647-12693-13", "Skid Route 66 Exit"),
	61: ("SW-1A-114 / SW-1A-120", "Left Slingshot"), 62: ("A-17612 / A-17613", "Right Slingshot"), 63: ("SW-11A-37", "Left Jet"),
	64: ("SW-11A-37", "Bottom Jet"), 65: ("SW-11A-37", "Right Jet"), 66: ("5647-12693-19", "Left Rollover"),
	67: ("5647-12693-19", "Middle Rollover"), 68: ("5647-12693-19", "Right Rollover"), 71: ("A-18951", "ZR-1 Full Left"),
	72: ("A-18951", "ZR-1 Full Right"), 75: ("5647-12693-31", "ZR-1 Exit"), 76: ("5647-12133-11", "ZR-1 Lock Ball 1"),
	77: ("5647-12693-53", "ZR-1 Lock Ball 2"), 78: ("5647-12693-54", "ZR-1 Lock Ball 3"), 81: ("A-16816-4", "Standup Million"),
	82: ("A-17226-4", "Skid Pad Standup"), 83: ("A-18019-4", "Right Standup"), 84: ("SW-1A-120", "Right Rubber"),
	86: ("SW-1A-120", "Jet Rubber"), 87: ("5647-12693-19", "Left Outer Loop"), 88: ("5647-12693-19", "Right Outer Loop"),
}
SWITCH_LABELS = {
	11: "Left Out Lane", 12: "Right Out Lane", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Plunger", 16: "Left Return Lane",
	17: "Right Return Lane", 18: "Spinner", 21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy In Button", 24: "Always Closed",
	25: "1st Gear (Shifter)", 26: "2nd Gear (Shifter)", 27: "3rd Gear (Shifter)", 28: "4th Gear (Shifter)", 31: "Trough Ball 1",
	32: "Trough Ball 2", 33: "Trough Ball 3", 34: "Trough Ball 4", 35: "Route 66 Entry", 36: "Pit Stop Popper", 37: "Trough Eject",
	38: "Inner Loop Entry", 41: "ZR-1 Bottom Entry", 42: "ZR-1 Top Entry", 43: "Skid Pad Entry", 44: "Skid Pad Exit",
	45: "Route 66 Exit", 46: "Left Standup 3", 47: "Left Standup 2", 48: "Left Standup 1", 51: "Left Race Start",
	52: "Right Race Start", 55: "Left Race Encoder", 56: "Right Race Encoder", 57: "Route 66 Kickout", 58: "Skid Route 66 Exit",
	61: "Left Slingshot", 62: "Right Slingshot", 63: "Left Jet", 64: "Bottom Jet", 65: "Right Jet", 66: "Left Rollover",
	67: "Middle Rollover", 68: "Right Rollover", 71: "ZR-1 Full Left", 72: "ZR-1 Full Right", 75: "ZR-1 Exit",
	76: "ZR-1 Lock Ball 1", 77: "ZR-1 Lock Ball 2", 78: "ZR-1 Lock Ball 3", 81: "Million Standup", 82: "Skid Pad Standup",
	83: "Right Standup", 84: "Right Rubber", 86: "Jet Rubber", 87: "Left Outer Loop", 88: "Right Outer Loop",
}
SWITCH_TYPES = {
	11: "microswitch", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "microswitch", 21: "tilt", 22: "microswitch", 23: "button", 24: "other", 25: "unknown", 26: "unknown", 27: "unknown",
	28: "unknown", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "opto", 38: "microswitch",
	41: "opto", 42: "opto", 43: "opto", 44: "microswitch", 45: "microswitch", 46: "other", 47: "other", 48: "other", 51: "opto",
	52: "opto", 55: "opto", 56: "opto", 57: "microswitch", 58: "microswitch", 61: "leaf", 62: "leaf", 63: "leaf", 64: "leaf",
	65: "leaf", 66: "microswitch", 67: "microswitch", 68: "microswitch", 71: "opto", 72: "opto", 75: "microswitch",
	76: "microswitch", 77: "microswitch", 78: "microswitch", 81: "other", 82: "other", 83: "other", 84: "leaf", 86: "leaf",
	87: "microswitch", 88: "microswitch",
}
SWITCH_ROLES = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.buy-in"}
SWITCH_LOCATIONS_TEXT = {13: "cabinet front", 14: "cabinet interior", 21: "coin door", 22: "coin door", 23: "cabinet front"}
SHIFTER_SWITCHES = frozenset({25, 26, 27, 28})
UNUSED_MATRIX_ADDRESSES = frozenset({53, 54, 73, 74, 85})
# PinMAME's corvGameData invSw {0x00,0x00,0x00,0x7f,0x07,0x33,0x00,0x03,0x00,...} inverts these public addresses through
# wpc_sw2m (core_setSw indexes invSw by wpc_sw2m(no)/8); the test recomputes the set from the mask.
MASKED_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 51, 52, 55, 56, 71, 72})
# Cells the matrix page shades "Opto, Typically Closed" (switch-matrix.md).
SHADED_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 51, 52, 55, 56, 71, 72, 112, 114, 116, 118})
# The ROM's own T.1 names (switch-edges run).
ROM_SWITCH_NAMES = {
	11: "LEFT OUT LANE", 12: "RIGHT OUT LANE", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "PLUNGER", 16: "L. RETURN LANE",
	17: "R. RETURN LANE", 18: "SPINNER", 21: "SLAM TILT", 23: "BUY IN BUTTON", 24: "ALWAYS CLOSED", 25: "1ST GEAR (OPT)",
	26: "2ND GEAR (OPT)", 27: "3RD GEAR (OPT)", 28: "4TH GEAR (OPT)", 31: "TROUGH BALL 1", 32: "TROUGH BALL 2", 33: "TROUGH BALL 3",
	34: "TROUGH BALL 4", 35: "ROUTE 66 ENTRY", 36: "PIT STOP POPPER", 37: "TROUGH EJECT", 38: "INNER LOOP ENTRY",
	41: "ZR1 BOTTOM ENTRY", 42: "ZR1 TOP ENTRY", 43: "SKID PAD ENTRY", 44: "SKID PAD EXIT", 45: "ROUTE 66 EXIT",
	46: "L. STANDUP 3", 47: "L. STANDUP 2", 48: "L. STANDUP 1", 51: "L. RACE START", 52: "R. RACE START", 55: "L. RACE ENCODER",
	56: "R. RACE ENCODER", 57: "ROUTE 66 KICKOUT", 58: "SKID RTE66 EXIT", 61: "L. SLINGSHOT", 62: "R. SLINGSHOT",
	63: "LEFT JET", 64: "BOTTOM JET", 65: "RIGHT JET", 66: "L. ROLLOVER", 67: "M. ROLLOVER", 68: "R. ROLLOVER",
	71: "ZR1 FULL LEFT", 72: "ZR1 FULL RIGHT", 75: "ZR1 EXIT", 76: "ZR1 LOCK BALL 1", 77: "ZR1 LOCK BALL 2",
	78: "ZR1 LOCK BALL 3", 81: "MILLION STANDUP", 82: "SKID PAD STANDUP", 83: "R. STANDUP", 84: "R. RUBBER", 86: "JET RUBBER",
	87: "L. OUTER LOOP", 88: "R. OUTER LOOP",
}
# Switches whose closure makes the ROM fire their own coil even inside T.1 (switch-edges run).
SWITCH_FIRES = {61: 9, 62: 10, 63: 11, 64: 12, 65: 13}
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"), 3: ("Green-Orange", "J207-3", "U20-16"),
	4: ("Green-Yellow", "J207-4", "U20-15"), 5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"), 3: ("White-Orange", "J209-3", "U18-5"),
	4: ("White-Yellow", "J209-4", "U18-7"), 5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-7"), 3: ("Orange-Black", "J205-3", "U17-11"),
	4: ("Orange-Yellow", "J205-4", "U17-9"), 5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
	7: ("Orange-Violet", "J205-8", "U16-7"), 8: ("Orange-Gray", "J205-9", "U16-5"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}
# Opto boards behind the shaded switches (section-3-boards.md): address -> board sentence.
OPTO_BOARDS = {
	31: "position BALL 1 of the Trough 7 IRED P.C.B. A-18617 (J1-6) and the Trough 7 IR TSTR P.C.B. A-18618, read through the 10-opto board A-18159's opto 1",
	32: "position BALL 2 of the trough LED board A-18617 (J1-5) and photo-transistor board A-18618, read through the 10-opto board's opto 2",
	33: "position BALL 3 of the trough LED board A-18617 (J1-4) and photo-transistor board A-18618, read through the 10-opto board's opto 3",
	34: "position BALL 4 of the trough LED board A-18617 (J1-3) and photo-transistor board A-18618, read through the 10-opto board's opto 4",
	35: "an LED Board A-16908 and Photo Transistor Board A-16909 pair on the 10-opto board A-18159's opto 5",
	36: "an LED Board A-16908 and Photo Transistor Board A-16909 pair on the 10-opto board's opto 6",
	37: "position JAM BALL of the trough LED board A-18617 (J1-7) and photo-transistor board A-18618, read through the 10-opto board's opto 7",
	41: "an LED Board A-16908 and Photo Transistor Board A-16909 pair on the 10-opto board's opto 8 (J6)",
	42: "an LED Board A-16908 and Photo Transistor Board A-16909 pair on the 10-opto board's opto 9 (J5)",
	43: "an LED Board A-16908 and Photo Transistor Board A-16909 pair on the 10-opto board's opto 10 (J4)",
	51: "the Opto Track Limit P.C.B. A-18821 at the left lane's start; its pin list (3-20) takes column 5 (J207-5) and row 1 (J209-1). Amendment 16-9890 replaces the board with A-19606",
	52: "the Opto Track Limit P.C.B. A-18821 at the right lane's start; its pin list (3-20) takes column 5 and row 2 (J209-2). Amendment 16-9890 replaces the board with A-19606",
	55: "the Opto Track Encoder P.C.B. A-18822 on the left cord pulley; its pin list (3-21) takes column 5 (J207-5) and row 5 (J209-5)",
	56: "the Opto Track Encoder P.C.B. A-18822 on the right cord pulley; its pin list (3-21) takes column 5 and row 6 (J209-7)",
	71: "the Engine Full-Stroke Opto P.C.B. A-18951 in the engine block; its pin list (3-22) takes column 7 (J207-7) and row 1 (J209-1)",
	72: "the Engine Full-Stroke Opto P.C.B. A-18951; its pin list (3-22) takes column 7 and row 2 (J209-2)",
}
TRACK_DISAGREEMENT = (
	" The Switch Locations list prints the start optos with part A-19141 (the Track list's Opto Board Assembly, which carries the "
	"encoder P.C.B.) and the encoders with A-18821 (the limit P.C.B.), crossed against the Section 3 board pages, and Manual Amendment "
	"16-9890's page for the Opto Track Encoder P.C.B. A-18822 re-wires it to column 7 rows 1 and 2, which are the engine full-stroke "
	"optos 71/72 in the matrix, the ROM and the engine board's own page. The ROM's T.1 names and its accepted race self test place the "
	"start optos at 51/52 and the encoders at 55/56, so the device and public address are not in doubt; the records follow the matrix "
	"and the Section 3 pages."
)
# The table and ROM name each optional shifter position; IPDB explains them.
SHIFTER_NOTE = (
	" IPDB quotes the designer: a four-speed shifter bolted to the cabinet shifted gears in the dragstrip mode on prototypes, and "
	"its code is still in the game. The production manual lists the position with no part and '(optional)', so the switch is not "
	"fitted on a production machine; a recreation of the prototype feature writes the selected gear here."
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _excerpt_digests() -> dict[str, str]:
	return {path.name: _file_sha256(path) for path in sorted(EXCERPT_ROOT.glob("*")) if path.is_file()}


EXCERPT_FILE_HASHES = _excerpt_digests()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Corvette retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Corvette extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Corvette retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(extraction_root)):
		raise RuntimeError(f"Corvette retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Corvette retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], status: str = "validated", **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability,
		"provenance": provenance(status, *refs),
	}
	device.update({key: value for key, value in extra.items() if value is not None})
	return device


def output_id(label: str) -> str:
	return "device." + (re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed")


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


# Placements projected onto a table object that models the device's mechanism rather than the device itself: the manual
# locates the device in that mechanism (trough, lock, engine, race track), so it is cited beside the table and script.
PROJECTED_PLACEMENTS = frozenset(
	{("switch", a) for a in (31, 32, 33, 34, 37, 51, 52, 55, 56, 71, 72, 76, 77, 78)} | {("solenoid", 18), ("solenoid", 19)}
)


def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Located spatial record for one device from the committed placement seed, or None.

	Table-derived placements start as ``observed``, citing the table for the coordinate and the script for the binding that
	picks the object (and, for 55/56, the finish constants that give the point); a projection also cites the manual.
	``drawing_callouts.apply_to_definition`` promotes the ones the factory location drawings confirm.
	"""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) + ((MANUAL_SOURCE,) if (category, address) in PROJECTED_PLACEMENTS else ())
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": entry["x"], "y": entry["y"],
			"provenance": provenance("observed", *refs),
		})
	return {"status": "observed", "placements": placements}


def _spatial_note(category: str, address: int) -> str:
	entries = _spatial_seed()[category].get(str(address)) or []
	notes = [entry["note"] for entry in entries if entry.get("note")]
	return (" " + " ".join(dict.fromkeys(notes))) if notes else ""


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_ic = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_ic = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC Security CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


SWITCH_NOTES = {
	11: "The left outlane; the rules' kickback (coil 3) returns a ball from this lane when lit.",
	15: "The shooter-lane switch: the ball rests on it before the manual ball shooter launches it (no auto-launch coil).",
	18: "The spinner (5647-12693-60); the SPINNER ARROW lamp (57) lights it.",
	23: "The cabinet BUY IN button (20-9663-18); its lamp is 87. IPDB: maximum 1 buy-in ball per player (operator option).",
	35: "The Route 66 (right) ramp entrance opto.",
	36: "The pit stop popper opto in the Popper Assembly A-19005 (LED A-16908, photo transistor A-16909); the PIT STOP POPPER coil (4) kicks the ball out.",
	38: "The inner loop entrance switch.",
	41: "The lower entrance opto of the ZR-1/LT-5 ramp.",
	42: "The upper entrance opto of the ZR-1/LT-5 ramp.",
	43: "The skid pad ramp entrance opto.",
	44: "The skid pad ramp exit switch.",
	45: "The Route 66 ramp exit switch.",
	46: "The third of the three left standup targets (3-Bank Standup Target A-19294).",
	47: "The middle of the three left standup targets (A-19294).",
	48: "The first of the three left standup targets (A-19294).",
	57: "The Route 66 kickout switch (Sub Miniature Switch 5647-12693-21 on the Kick-Out Coil Assembly A-19006 on the back panel); the ROUTE 66 KICKOUT coil (8) ejects the ball.",
	58: "Printed 'Skid Route 66 Exit' (ROM: SKID RTE66 EXIT), a ramp exit switch shared by the skid pad and Route 66 paths.",
	66: "The left of the three top rollovers (LT-1 lanes; the rules' lane change rotates them).",
	67: "The middle top rollover.",
	68: "The right top rollover.",
	75: "The ZR-1 exit switch.",
	76: "The first ZR-1/LT-5 lock position: the rules lock up to three balls in the engine mechanism.",
	77: "The second ZR-1/LT-5 lock position.",
	78: "The third ZR-1/LT-5 lock position.",
	81: "The MILLION standup target (A-16816-4); the matrix prints 'Million Standup', the list 'Standup Million'.",
	82: "The skid pad standup target (A-17226-4).",
	83: "The right standup target (A-18019-4).",
	84: "A rubber switch (SW-1A-120) on the right.",
	86: "A rubber switch (SW-1A-120) among the jet bumpers.",
	87: "The left outer loop switch.",
	88: "The right outer loop switch.",
}


# What the retained known-working version 1.4.2 script does for each matrix switch.
SWITCH_SCRIPT = {
	13: "the start key sets it while held", 14: "vpmNudge.TiltSwitch = 14", 18: "sw18_Spin pulses it",
	22: "Table1_Init sets Controller.Switch(22) = 1 (door closed)", 23: "the front (buy-in) key sets it while held",
	24: "Table1_Init sets Controller.Switch(24) = 1",
	31: "the trough ball stack bsTrough (InitSw 0,31,32,33,34) holds it with four balls", 32: "the trough ball stack bsTrough holds it",
	33: "the trough ball stack bsTrough holds it", 34: "the trough ball stack bsTrough holds it",
	36: "the pit stop ball stack bsL (InitSw 0,36) holds it; the entry kicker sw36a adds balls to it",
	37: "solTrough pulses it each time solenoid 1 ejects a ball",
	41: "sw41_Hit sets it (and arms the engine magnets) and sw41_unHit clears it",
	44: "sw44_Hit pulses it", 45: "sw45_Hit pulses it", 46: "sw46_Hit pulses it", 47: "sw47_Hit pulses it", 48: "sw48_Hit pulses it",
	51: "no script binding: PinMAME's car model writes it (HandleMechanics 7) and Mech_Timer moves the cars from GetMech(0) and GetMech(1)",
	52: "no script binding: PinMAME's car model writes it (HandleMechanics 7)", 55: "no script binding: PinMAME's car model writes it (HandleMechanics 7)",
	56: "no script binding: PinMAME's car model writes it (HandleMechanics 7)",
	57: "the Route 66 ball stack bsR (InitSw 0,57) holds it; the kickers sw57a and Kicker3 add balls to it",
	61: "LeftSlingShot_Slingshot pulses it", 62: "RightSlingShot_Slingshot pulses it",
	63: "Bumper2_Hit pulses it", 64: "Bumper1_Hit pulses it", 65: "Bumper3_Hit pulses it",
	71: "the rubber SW71 beside the engine sets it on a hit, which PinMAME's engine model (HandleMechanics 7) overwrites from the engine position every update",
	72: "the rubber SW72 beside the engine sets it on a hit, which PinMAME's engine model overwrites from the engine position every update",
	75: "sw75_Hit pulses it",
	76: "the lock ball stack bsLock (InitSw 0,76,77,78) holds it; the kicker Kicker1 adds balls to it", 77: "the lock ball stack bsLock holds it",
	78: "the lock ball stack bsLock holds it",
	81: "sw81_Hit pulses it", 82: "sw82_Hit pulses it", 83: "sw83_Hit pulses it", 84: "sw84_Hit pulses it", 86: "sw86_Hit pulses it",
}
for _address in (11, 12, 15, 16, 17, 38, 66, 67, 68, 87, 88):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit sets it and sw{_address}_UnHit clears it"
for _address in (35, 42, 43, 58):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit sets it and sw{_address}_unHit clears it"


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += (
			" The Switch Matrix and the Switch Locations list print 'Not Used' for this position. The ROM still scans it: in its T.1 "
			"SWITCH EDGES sweep a host write of 1 drew 'NOT USED', and 0 cleared it."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, EDGES_SOURCE),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE),
			normally_closed=False, **extra,
		)
	part, description = SWITCH_LOCATIONS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES[address]}
	if " / " in part:
		physical["assembly_part_number"] = part
	elif part != "---":
		physical["part_number"] = part
	notes += f" Switch Locations description \"{description}\"."
	if description.startswith("*"):
		notes += " The list's '*' marks a switch the location drawing does not show."
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE)
	if address == 22:
		notes += (
			" Every service-test run held public 22 at 0 (door open), as the WPC service buttons require, so T.1 did not sweep it; the "
			"controller profile and the coin door wiring give its role."
		)
		refs = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	elif address == 24:
		notes += (
			" PinMAME holds public 24 at 1 from power-up. In T.1 SWITCH EDGES the redundant write of 1 drew nothing new and the 1 -> 0 "
			"edge drew 'ALWAYS CLOSED / T.1 LAST SW 24', so the ROM reports this position when it opens."
		)
	else:
		notes += f" The ROM names it \"{ROM_SWITCH_NAMES[address]}\" in T.1 SWITCH EDGES while the host holds public {address} at 1, and clears the name at 0."
	if address in SWITCH_FIRES:
		notes += f" Closing it made the ROM fire its own coil, public solenoid {SWITCH_FIRES[address]}, even inside T.1."
	if address in MASKED_SWITCHES:
		notes += (
			" PinMAME's corvGameData inverted-switch mask inverts this address, so public 1 is an open matrix contact; the ROM reads the "
			"switch as active at public 1, so its matrix contact rests closed and normally_closed is true. The matrix page shades the cell "
			"'Opto, Typically Closed'."
		)
	if address in OPTO_BOARDS:
		notes += f" It is {OPTO_BOARDS[address]}."
	if address in {31, 32, 33, 34}:
		notes += f" It reports the trough holding at least {address - 30} ball{'s' if address > 31 else ''} (Corvette is a four-ball game)."
	if address == 37:
		notes += " It sees the ball at the trough's eject position, over the TROUGH EJECT coil (solenoid 1)."
	if address in {51, 52, 55, 56}:
		side = "left" if address in {51, 55} else "right"
		role = "start (home) opto" if address in {51, 52} else "encoder opto, pulsed as the car moves"
		notes += (
			f" The {side} lane's {role} of the race track (Track Assembly A-19004). The ROM's T.17 RACE TEST shows it as the {side.upper()} "
			"START or POS box; with PinMAME's car models answering (mechanism bits 0 and 1) its self test drove each car to the far end, "
			"counting the encoder, and back to the start opto, and accepted the model's pairing."
		)
		notes += TRACK_DISAGREEMENT
		refs += (RACE_TEST_SOURCE, AMENDMENT_SOURCE)
	if address in {71, 72}:
		side = "LEFT" if address == 71 else "RIGHT"
		notes += (
			f" It reports the engine at its FULL {side} stop. The ROM's T.16 ZR1-LT5 TEST self test sweeps the engine until this opto closes "
			f"and records the position ({'63' if address == 71 else '192'} with PinMAME's engine model, which closes 71 below register value 64 "
			"and 72 above 191); ENGINE LEFT stopped with FULL LEFT marked. With nothing answering, the self test fails."
		)
		refs += (ENGINE_TEST_SOURCE, ENGINE_FAILED_SOURCE)
	if address in SHIFTER_SWITCHES:
		notes += SHIFTER_NOTE
		refs += (IDENTITY_SOURCE,)
	if address in SWITCH_NOTES:
		notes += " " + SWITCH_NOTES[address]
	if address in {61, 62}:
		notes += " The slingshot kick switch and score switch share this address."
	if address in {63, 64, 65}:
		notes += f" One of three jet bumpers (Jet Bumper Assembly B-9414-3, coil {SWITCH_FIRES[address]})."
	label = SWITCH_LABELS[address]
	role = SWITCH_ROLES.get(address)
	if role:
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = SWITCH_LOCATIONS_TEXT[address]
	elif address == 24:
		extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
	elif address in SHIFTER_SWITCHES:
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, IDENTITY_SOURCE)
		physical["location"] = "cabinet side (prototype shifter)"
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _spatial_note("switch", address)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	kind = "constant" if address == 24 else "switch"
	if address == 24:
		extra["constant_active"] = True
		extra["initial_active"] = True
	else:
		extra["normally_closed"] = address in MASKED_SWITCHES
	if address == 22:
		extra["initial_active"] = True
		notes += " It is closed while the coin door is closed; the amendment says the door must be closed to power the engine and the race track."
		refs += (AMENDMENT_SOURCE,)
	physical["notes"] = notes
	availability = "optional" if address in SHIFTER_SWITCHES else "used"
	return _device(identifier, label, kind, SWITCH_GROUP, address, availability, refs, physical=physical, **extra)


# Fliptronic column (switch-matrix.md; fliptronic-board.md; section-3-boards.md):
# public -> (label, printed position, matrix wire, connector, type, role, availability).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "F1", "Black-Green", "J906-1", "leaf", "internal.flipper.lower.right.eos", "used"),
	112: ("Right Flipper Button Opto (F2)", "F2", "Black-Violet", "J905-1", "opto", "flipper.lower.right.button", "used"),
	113: ("Lower Left Flipper EOS", "F3", "Black-Blue", "J906-3", "leaf", "internal.flipper.lower.left.eos", "used"),
	114: ("Left Flipper Button Opto (F4)", "F4", "Black-Gray", "J905-2", "opto", "flipper.lower.left.button", "used"),
	115: ("Not Used Fliptronic Position F5", "F5", "Black-Violet", "J906-4", "leaf", None, "unused"),
	116: ("Right Flipper Button Opto (F6)", "F6", "Black-Yellow", "J905-3", "opto", "flipper.lower.right.button", "used"),
	117: ("Upper Left Flipper EOS", "F7", "Black-Gray", "J906-5", "leaf", "internal.flipper.upper.left.eos", "used"),
	118: ("Left Flipper Button Opto (F8)", "F8", "Black-Blue", "J905-5", "opto", "flipper.upper.left.button", "used"),
}
FLIPPER_ROM_TEXT = {112: ("R. FLIPPER E.O.S.", "F1 BLK-GRN ORN"), 114: ("L. FLIPPER E.O.S.", "F3 BLK-BLU ORN"), 116: ("R. FLIPPER E.O.S.", "F1 BLK-GRN ORN"), 118: ("U.L. FLIPPER E.O.S.", "F7 BLK-GRY ORN")}
FLIPPER_FIRES = {112: "the lower right flipper (public 45 and 46)", 114: "the lower left flipper (public 47 and 48)", 116: "the lower right flipper (public 45 and 46)", 118: "the upper left flipper (public 35 and 36)"}
FLIPPER_BOARD_WIRES = {112: "Black-Violet, to right flipper opto", 114: "Blue-Gray, to left flipper opto", 116: "Blue-Yellow, to right flipper opto", 118: "Black-Blue, to left flipper opto"}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
		if address == 4:
			note += " The Dedicated Switches drawing (3-3) prints no coin-door pin for the D4 line."
		if address == 5:
			note += " The matrix prints 'Ser Credits'; the Dedicated Switches drawing spells it 'Service Credits'."
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note} The dedicated switches reach the CPU through the Coin Door Interface P.C.B. A-17051-1; the IC pins come from the Dedicated Switches drawing (3-3)."},
				wiring={"board": "WPC Security CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, printed, wire, connection, switch_type, role, availability) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed} ({wire}, {connection} on the Fliptronic II board)."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"wiring": {"board": "Fliptronic II board A-15472-1", "drive_wire": wire, "drive_connection": connection},
		}
		if role:
			extra["roles"] = [role]
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, EDGES_SOURCE)
		physical: dict[str, Any] = {"switch_type": switch_type}
		if address in {111, 113, 117}:
			physical["part_number"] = "SW-1A-194"
			physical["location"] = "flipper assembly"
			flipper = {111: "lower right", 113: "lower left", 117: "upper left"}[address]
			notes += (
				f" End-of-stroke switch SW-1A-194 on the {flipper} flipper. corvGameData declares FLIP_SOL(FLIP_L | FLIP_UL), so PinMAME "
				"rewrites this bit from the flipper coil state on every update: in the T.1 sweep a host write of 1 read back 0 and drew no "
				"name. Its public level is not a measurement of the contact; normally_closed records the grounded switch's open rest state."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		elif address == 115:
			notes += (
				" The matrix prints F5 'Upper Right Flipper EOS', but the Switch Locations list prints F5 Not Used, the Fliptronic II pin "
				"list prints J906-4 Not Used, Corvette has no upper right flipper (its Fliptronic upper-right circuit drives the ramp "
				"diverter, 33/34), and in the T.1 sweep a host write of 1 round-tripped and drew no name."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		else:
			side = "right" if address in {112, 116} else "left"
			rom_name, rom_text = FLIPPER_ROM_TEXT[address]
			physical["location"] = "cabinet flipper button"
			physical["assembly_part_number"] = "A-17316"
			notes += (
				f" An opto of the {side} Flipper Opto P.C.B. A-17316 at the {side} cabinet button; the Fliptronic II pin list prints "
				f"'{FLIPPER_BOARD_WIRES[address]}'. Each button's board carries two optos ({'F2 and F6' if side == 'right' else 'F4 and F8'}), "
				"so one press interrupts both. WPC-Security reads the flipper column complemented (WPC_FLIPPERS returns ~swMatrix), so public 1 "
				"is the pressed button and the contact the column sees is open at rest: normally_closed is false. The matrix shades the cell as "
				f"an opto. In the T.1 sweep a host write of 1 named '{rom_name}' ({rom_text}) and fired {FLIPPER_FIRES[address]}."
			)
			if address == 116:
				notes += (
					" The matrix prints F6 'Upper Right Flipper Opto' and the Switch Locations list prints F6 Not Used, but the Fliptronic II "
					"list wires J905-3 to the right flipper opto and the ROM fires the lower right flipper from it as from F2, so it is the right "
					"button's second opto with the button's role; a consumer writes 112 and 116 together from the right button. The matrix "
					"prints its wire Black-Yellow where the Fliptronic II list prints Blue-Yellow; the device and address agree, so the colour "
					"is a wiring detail."
				)
			if address == 118:
				notes += (
					" The Switch Locations list prints F8 '*Upper Left Flipper Cabinet': the left button's second opto works the upper left "
					"flipper, so a consumer writes 114 and 118 together from the left button."
				)
			if address == 114:
				notes += " The Fliptronic II list prints this line Blue-Gray where the matrix prints Black-Gray; the device and address agree."
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, availability, refs, **extra))
	chart = {1: "Off, Off, Off, Off, Off", 2: "Off, Off, Off, Off, Off", 3: "On, On, On, On, On", 4: "On, On, On, On, On", 5: "On, On, On, On, Off", 6: "On, Off, On, On, On", 7: "On, On, Off, On, On", 8: "On, On, Off, Off, On"}
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP SW{address} (country setting)", "dip_switch", DIP_GROUP, address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC Security CPU board", "switch_type": "dip",
					"notes": f"CPU-board DIP position SW{address}. The printed Dip Switch Chart (PDF page 2) sets it, for America, Euopean [sic], French, German and Spain in that order: {chart[address]}.",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# --- Solenoid data (solenoid-flasher-table.md, solenoid-flasher-locations.md, power-driver-board.md) ------
SOLENOID_LABELS = {
	1: "Trough Eject", 2: "ZR-1 Low Rev Gate", 3: "Kickback", 4: "Pit Stop Popper", 5: "ZR-1 Up Rev Gate", 6: "Not Used Driver 6",
	7: "Knocker", 8: "Route 66 Kickout", 9: "Left Slingshot", 10: "Right Slingshot", 11: "Left Jet", 12: "Bottom Jet",
	13: "Right Jet", 14: "Not Used Driver 14", 15: "ZR-1 Lockup", 16: "Loop Gate", 17: "Race Direction", 18: "Left Race Enable",
	19: "Right Race Enable", 20: "Tenth Corvette Flasher", 21: "Jets Flasher", 22: "Right Ramps Flasher", 23: "Upper Left Flipper Flasher",
	24: "Catch Me Flasher", 25: "ZR-1 Ramp Flasher", 26: "ZR-1 Underside Flasher", 27: "Right Rear Panel Flasher", 28: "Right Standup Flasher",
	33: "Diverter Power", 34: "Diverter Hold", 35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
	51: "Engine Drive Enable (Disable A/B Lines)", 52: "Engine LED A Lines", 53: "Engine LED B Lines",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B", 31: "WPC Game-On State",
	32: "Unused WPC State Channel 32", 37: "Unused WPC-Security Output 37", 38: "Unused WPC-Security Output 38",
	39: "Unused WPC-Security Output 39", 40: "Unused WPC-Security Output 40", 41: "Unused WPC-Security Output 41",
	42: "Unused WPC-Security Output 42", 43: "Unused WPC-Security Output 43", 44: "Unused WPC-Security Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# address -> printed (type, voltage connection, transistor, drive connection, wire, part or flashlamp), Solenoid/Flasher Table (2-48).
SOLENOID_TABLE = {
	1: ("High Power", "J107-2", "Q82", "J130-1", "Vio-Brn", "AE-26-1500"), 2: ("High Power", "J107-2", "Q80", "J130-2", "Vio-Red", "SM1-28-900-DC"),
	3: ("High Power", "J107-2", "Q78", "J130-4", "Vio-Org", "AE-23-800"), 4: ("High Power", "J107-2", "Q76", "J130-5", "Vio-Yel", "AE-23-800"),
	5: ("High Power", "J107-2", "Q64", "J130-6", "Vio-Grn", "SM1-35-4000-DC"), 6: ("High Power", "J107-2", "Q66", "J130-7", "Vio-Blu", None),
	7: ("High Power", "J107-2 (backbox)", "Q68", "J130-8 (backbox)", "Vio-Blk", "AE-23-800"), 8: ("High Power", "J107-2", "Q70", "J130-9", "Vio-Gry", "AE-23-800"),
	9: ("Low Power", "J107-3", "Q58", "J127-1", "Brn-Blk", "AE-26-1200"), 10: ("Low Power", "J107-3", "Q56", "J127-3", "Brn-Red", "AE-26-1200"),
	11: ("Low Power", "J107-3", "Q54", "J127-4", "Brn-Org", "AE-26-1200"), 12: ("Low Power", "J107-3", "Q52", "J127-5", "Brn-Yel", "AE-26-1200"),
	13: ("Low Power", "J107-3", "Q50", "J127-6", "Brn-Grn", "AE-26-1200"), 14: ("Low Power", "J107-3", "Q48", "J127-7", "Brn-Blu", None),
	15: ("Low Power", "J107-3", "Q46", "J127-8", "Brn-Vio", "AE-30-2000"), 16: ("Low Power", "J107-3", "Q44", "J127-9", "Brn-Gry", "A-14406"),
	17: ("Flasher", "J107-6", "Q42", "J126-1", "Blk-Brn", "A-19159"), 18: ("Flasher", "J107-6", "Q40", "J126-2", "Blk-Red", "14-8015"),
	19: ("Flasher", "J107-6", "Q38", "J126-3", "Blk-Org", "14-8015"), 20: ("Flasher", "J106-5 (backbox)", "Q36", "J125-5 (backbox)", "Blk-Yel", "24-8802"),
	21: ("Flasher", "J107-6", "Q28", "J126-5", "Blu-Grn", "24-8704"), 22: ("Flasher", "J107-6, J106-5", "Q30", "J126-6, J125-7", "Blu-Blk", "24-8704, 24-8802"),
	23: ("Flasher", "J107-6, J106-5", "Q34", "J126-7, J125-8", "Blu-Vio", "24-8704, 24-8802"), 24: ("Flasher", "J107-6, J106-5", "Q32", "J126-8, J125-9", "Blu-Gry", "24-8704, 24-8802"),
	25: ("Gen. Purpose", "J107-6, J106-5", "Q26", "J122-1, J124-1", "Blu-Brn", "24-8802, 24-8802"), 26: ("Gen. Purpose", "J107-6, J106-5", "Q24", "J122-2, J124-2", "Blu-Red", "24-8704, 24-8802"),
	27: ("Gen. Purpose", "J107-6, J106-5", "Q22", "J122-3, J124-3", "Blu-Org", "24-8802, 24-8802"), 28: ("Gen. Purpose", "J107-6, J106-5", "Q20", "J122-4, J124-5", "Blu-Yel", "24-8802, 24-8802"),
	33: ("High Power", "J907-6,7", "Q2", "J902-6", "Yel-Vio", "A-15943-1"), 34: ("Low Power", "J907-6,7", "Q7", "J902-4", "Org-Vio", "A-15943-1"),
}
# Locations-list assembly for each coil/flasher (solenoid-flasher-locations.md, 2-48 and 2-49).
SOLENOID_ASSEMBLIES = {
	1: "A-18753", 2: "A-19140", 3: "B-11873", 4: "A-19005", 5: "A-19006", 7: "B-16086-1", 8: "A-19006", 9: "B-9362-R-3", 10: "B-9362-L-2",
	11: "A-9415-2", 12: "A-9415-2", 13: "A-9415-2", 15: "A-15368-1", 16: "A-17796", 17: "A-19159", 18: "A-19134", 19: "A-19134",
	21: "A-17803", 22: "A-17983", 23: "A-17803", 24: "A-17803", 25: "A-19008", 26: "A-17983", 27: "B-12156", 33: "A-17241", 34: "A-17241",
}
# The ROM's own T.4 and T.5 names and wires (solenoid-test and flasher-test runs).
ROM_SOLENOID_NAMES = {
	1: ("TROUGH EJECT", "VIO-BRN RED-BRN"), 2: ("ZR1 LOW REV GATE", "VIO-RED RED-BRN"), 3: ("KICKBACK", "VIO-ORN RED-BRN"),
	4: ("PIT STOP POPPER", "VIO-YEL RED-BRN"), 5: ("ZR1 UP REV GATE", "VIO-GRN RED-BRN"), 7: ("KNOCKER", "VIO-BLK RED-BRN"),
	8: ("ROUTE 66 KICKOUT", "VIO-GRY RED-BRN"), 9: ("L. SLINGSHOT", "BRN-BLK RED-BLK"), 10: ("R. SLINGSHOT", "BRN-RED RED-BLK"),
	11: ("LEFT JET", "BRN-ORN RED-BLK"), 12: ("BOTTOM JET", "BRN-YEL RED-BLK"), 13: ("RIGHT JET", "BRN-GRN RED-BLK"),
	14: ("NOT USED", "BRN-BLU RED-BLK"), 15: ("ZR1 LOCKUP", "BRN-VIO RED-BLK"), 16: ("LOOP GATE", "BRN-GRY RED-BLK"),
	17: ("RACE DIRECTION", "BLK-BRN RED-WHT"), 18: ("L. RACE ENABLE", "BLK-RED RED-WHT"), 19: ("R. RACE ENABLE", "BLK-ORN RED-WHT"),
	20: ("TENTH CORVETTE", "BLK-YEL RED-WHT"), 21: ("JETS", "BLU-GRN RED-WHT"), 22: ("R. RAMPS", "BLU-BLK RED-WHT"),
	23: ("U. L. FLIPPER", "BLU-VIO RED-WHT"), 24: ("CATCH ME", "BLU-GRY RED-WHT"), 25: ("ZR1 RAMP", "BLU-BRN RED-WHT"),
	26: ("ZR1 UNDERSIDE", "BLU-RED RED-WHT"), 27: ("R. REAR PANEL", "BLU-ORN RED-WHT"), 28: ("R. STANDUP", "BLU-YEL RED-WHT"),
	33: ("DIVERTER POWER", "YEL-VIO RED-VIO"), 34: ("DIVERTER HOLD", "ORN-VIO RED-VIO"),
	35: ("U.L. FLIP. POWER", "YEL-GRY RED-GRY"), 36: ("U.L. FLIP. HOLD", "ORN-GRY RED-GRY"), 45: ("R. FLIP. POWER", "YEL-GRN RED-GRN"),
	46: ("R. FLIP. HOLD", "ORN-GRN RED-GRN"), 47: ("L. FLIP. POWER", "YEL-BLU RED-BLU"), 48: ("L. FLIP. HOLD", "ORN-BLU RED-BLU"),
}
T5_ADDRESSES = frozenset(range(20, 29))
T12_ADDRESSES = frozenset({35, 36, 45, 46, 47, 48})
FLASHER_SOLENOIDS = frozenset({20, 21, 22, 23, 24, 25, 26, 27, 28})
SOLENOID_NOTES = {
	1: "The TROUGH EJECT coil (AE-26-1500, Outhole Ball Trough Assembly A-18753): it kicks the ball over the trough eject opto (37) into the shooter lane.",
	2: "The ZR-1 LOW REV GATE coil (SM1-28-900-DC), part of the Engine & Ramp Assembly A-19140 that the locations list names; the engine ramp carries a flopgate, a front gate and a back gate (Engine Ramp Assembly A-19008), and no retained source says which of them this coil moves or when the ROM fires it.",
	3: "The KICKBACK coil (AE-23-800, Kicker Bracket Assembly B-11873) at the left outlane (switch 11); the rules light it from the LITE KICKBACK lamp (67) and show it on KICKBACK ARROW (71).",
	4: "The PIT STOP POPPER coil (AE-23-800, Popper Assembly A-19005, with a bell armature): it kicks the ball out of the pit stop popper (opto 36).",
	5: "The ZR-1 UP REV GATE coil (SM1-35-4000-DC). The locations list gives it the Kick-Out Coil Assembly A-19006, and Manual Amendment 16-9890 adds a Ball Gate Actuator assembly with the same SM1-35-4000-DC coil to the back panel; no retained source says when the ROM fires it.",
	6: "Printed 'Not Used': the table prints transistor Q66 and connector J130-7 but no coil part, and the locations list prints '---'. The ROM's T.4 skips the driver entirely.",
	7: "The KNOCKER (AE-23-800, B-16086-1); the table prints its voltage (J107-2) and drive (J130-8) connections in the Backbox columns, and the location drawing has no callout for it.",
	8: "The ROUTE 66 KICKOUT coil (AE-23-800, Kick-Out Coil Assembly A-19006 on the back panel, with the kickout switch 57): it ejects a ball from the Route 66 kickout behind the race track.",
	9: "The left slingshot coil (AE-26-1200); the ROM fired it when the T.1 sweep closed 61. The locations list prints assembly B-9362-R-3 for the left and B-9362-L-2 for the right slingshot.",
	10: "The right slingshot coil (AE-26-1200); the ROM fired it when the T.1 sweep closed 62.",
	11: "The left jet bumper coil (AE-26-1200, A-9415-2); the ROM fired it when the T.1 sweep closed 63.",
	12: "The bottom jet bumper coil (AE-26-1200, A-9415-2; the list prints 'Buttom Jet'); the ROM fired it when the T.1 sweep closed 64.",
	13: "The right jet bumper coil (AE-26-1200, A-9415-2); the ROM fired it when the T.1 sweep closed 65.",
	14: "Printed 'Not Used': the table prints transistor Q48 and connector J127-7 but no coil part, and the locations list prints '---'. The ROM's T.4 still offers the driver and prints NOT USED while it pulses public 14, so the pulse is the sweep, not a fitted load.",
	15: "The ZR-1 LOCKUP coil (AE-30-2000, Eject Assembly A-15368-1) of the ZR-1/LT-5 lock (switches 76-78). Adjustment A.2 13 ENDGAME LOCK REL. decides whether locked balls are released at the end of a game; no retained source says which way the coil moves them.",
	16: "The LOOP GATE (A-14406 on assembly A-17796).",
	17: "RACE DIRECTION: the Dual H-Drive Motor Controller A-19159's direction input for both race cars (power driver J126-1). In the ROM's T.17 RACE TEST it is on whenever a car runs forward, with PinMAME's car models moving the car toward the finish while it is on.",
	18: "LEFT RACE ENABLE: runs the left car's gear-box motor (14-8015, Gear Box Assembly A-19134) through the Dual H-Drive controller (J126-2). T.17's LEFT FORWARD raises it with 17 while the left car's encoder (55) counts.",
	19: "RIGHT RACE ENABLE: runs the right car's motor (14-8015, A-19134) through the Dual H-Drive controller (J126-3). T.17's self test raised it with 17 while the right car's encoder (56) counted.",
	20: "The TENTH CORVETTE flasher: a #906 (24-8802) in the backbox that lights the tenth, future car in the backglass art when the puzzle completes.",
	21: "The JETS flasher: a #89 (24-8704) on the playfield (A-17803) among the jet bumpers.",
	22: "The RIGHT RAMPS flasher circuit: a #89 (24-8704) on the playfield (A-17983) and a #906 (24-8802) in the backbox, on separate playfield (J126-6) and backbox (J125-7) drive connections of one driver.",
	23: "The UPPER LEFT FLIPPER flasher circuit (the locations list prints 'Upper Left Playfield'): a #89 on the playfield (A-17803) and a #906 in the backbox.",
	24: "The CATCH ME flasher circuit: a #89 on the playfield (A-17803) and a #906 in the backbox.",
	25: "The ZR-1 RAMP flasher circuit (Gen. Purpose driver): a #906 in the Engine Ramp Assembly A-19008 (its parts list carries the 24-8802 bulb) and a #906 in the backbox.",
	26: "The ZR-1 UNDERSIDE flasher circuit (Gen. Purpose driver): a #89 on the playfield (A-17983) and a #906 in the backbox.",
	27: "The RIGHT REAR PANEL flasher circuit (Gen. Purpose driver): a #906 on the back panel (B-12156) and a #906 in the backbox.",
	28: "The RIGHT STANDUP flasher circuit (Gen. Purpose driver): the table prints a #906 for the playfield and a #906 for the backbox, the locations list prints no assembly, and the solenoid/flasher drawing (2-49) balloons 28 twice on the playfield, once on each side, so the number of playfield bulbs on this circuit is not settled.",
	33: "The ramp DIVERTER power winding (Flipper Coil Assembly A-15943-1, assembly A-17241; Amendment 16-9890 renumbers the Ramp Diverter Assembly A-19630). It is wired to the Fliptronic II upper-right flipper circuit (Q2, J902-6), whose coil cells print NOT USED.",
	34: "The ramp DIVERTER hold winding (A-15943-1), on the Fliptronic II upper-right hold circuit (Q7, J902-4).",
	51: "Custom output 1: corvGameData declares three custom solenoids, and corv_getSol publishes bit 0 of the CPU's extension register 3 here (CORE_CUSTSOLNO(1)). That register is the Motor Driver Master Board A-18532's U2 latch (strobe DIS2 from CPU J204), whose bit-0 output drives both the DISABLE A and DISABLE B lines through the ULN2803 to the Slave Board, the engine coils' driver. The ROM raises it on entering T.16 ZR1-LT5 TEST and keeps it on, raises it alone in T.18 ZR-1 ADJUST, and drops it when the self test fails, so it is the engine power enable.",
	52: "Custom output 2: bit 1 of extension register 3, which the Master Board's U2 latch sends through the ULN2803 as the LEDA1 and LEDA2 lines to the Slave Board. The ROM toggles it with 53 while the engine moves in T.16. What the Slave Board does with the LED lines is not traced beyond the Master Board.",
	53: "Custom output 3: bit 2 of extension register 3, sent as the LEDB1 and LEDB2 lines to the Slave Board; the ROM toggles it with 52 while the engine moves in T.16.",
}
# What the retained known-working version 1.4.2 script does for each solenoid (SolCallback table and the subs it names).
SOLENOID_SCRIPT = {
	1: "SolCallback(1) = \"solTrough\": the trough ball stack bsTrough ejects a ball from the kicker BallRelease and pulses switch 37",
	2: "SolCallback(2) = \"SolLGate\" ('Lock Gate 1'): while the coil is on, the engine-ramp gate LGate is closed and the wall Wall12 is raised; off, LGate opens and Wall12 drops",
	3: "SolCallback(3) = \"SolKickback\": fires the plunger KickBack on, pulls it back off",
	4: "SolCallback(4) = \"bsL.SolOut\": the pit stop ball stack (switch 36) kicks its ball out of the kicker sw36",
	5: "SolCallback(5) = \"SolGateU\" ('Lock Gate 2'): the upper engine-ramp gate GateU is open while the coil is on and closed off",
	8: "SolCallback(8) = \"bsR.SolOut\": the Route 66 ball stack (switch 57) kicks its ball out of the kicker sw57",
	15: "SolCallback(15) = \"bsLock.SolOut\": the lock ball stack (switches 76-78) ejects one ball at the kicker Kicker3, below the lock entry",
	16: "SolCallback(16) = \"SolTGate\": the loop gate TGate is open while the coil is on and closed off",
	17: "SolCallback(17) = \"SetLamp 117,\", commented 'motor controller and Flasher'; nothing draws lamp 117 ('Not Shown in the Service Manual No clue where it goes'), so the table consumes the direction only through PinMAME's car models",
	18: "SolCallback(18) = \"SetLamp 118,\" ('motor controller'): lights the proxy flashers Flasher118/Flasher118a; the car itself moves from GetMech(0)",
	19: "SolCallback(19) = \"SetLamp 119,\" ('motor controller'): lights the proxy flashers Flasher119/Flasher119a; the car itself moves from GetMech(1)",
	20: "SolCallback(20) = \"SetLamp 120,\", commented 'Backglass Only' (light L120)",
	26: "SolCallback(26) = \"SolEngine\", commented 'motor controller and flasher': it lights Flasher126 and L126, enables the four engine magnet triggers Magnet1-4 (the cvpmMagnet mag1 also names solenoid 26), and rocks the engine primitive 5 degrees each way as the output toggles, on top of the engine angle drawn from GetMech(2)",
	33: "SolCallback(33) is commented out: the table moves the diverter from the hold winding alone",
	34: "SolCallback(34) = \"SolDiv\": while the hold winding is on, DiverterON is raised, DiverterOFF dropped and the hidden flipper DivFlipper rotated to its end",
	35: "no SolCallback: the table's SolLFlipper (the lower left flipper's callback) rotates the upper left flipper LeftFlipper1 with the lower left one",
	36: "no SolCallback: the table's SolLFlipper rotates LeftFlipper1 with the lower left flipper",
	45: "SolCallback(sLRFlipper) = \"SolRFlipper\" rotates RightFlipper", 46: "SolCallback(sLRFlipper) = \"SolRFlipper\" rotates RightFlipper",
	47: "SolCallback(sLLFlipper) = \"SolLFlipper\" rotates LeftFlipper (and LeftFlipper1)", 48: "SolCallback(sLLFlipper) = \"SolLFlipper\" rotates LeftFlipper (and LeftFlipper1)",
	51: "no SolCallback: the engine moves from GetMech(2), which PinMAME's engine model serves (HandleMechanics 7)",
	52: "no SolCallback", 53: "no SolCallback",
	6: "the SolCallback table comments '6 Not Used'", 14: "the SolCallback table comments '14 Not Used'",
	7: "no SolCallback: the knocker sound routine KnockerSolenoid is never called",
}
for _address in (21, 22, 23, 24, 25, 27):
	SOLENOID_SCRIPT[_address] = f"SolCallback({_address}) = \"SetLamp 1{_address},\", drawn by NFadeL 1{_address} on the light L1{_address}"
SOLENOID_SCRIPT[28] = "SolCallback(28) = \"SetLamp 128,\", drawn on two lights (NFadeLm 128, L128 and NFadeL 128, L128b)"
for _address in (9, 10, 11, 12, 13):
	SOLENOID_SCRIPT[_address] = "no SolCallback (the vpmSolSound line is commented out): the table fires the " + (
		"slingshot" if _address < 11 else "jet bumper"
	) + " from its own physics event"
FLIPPER_COILS = {
	45:("power", "29", "Lwr. Rt. Power", "J907-1 (Red-Grn)", "Q4", "J902-13", "Yel-Grn", "FL-11629", "BLUE", "A-19223-R"),
	46: ("hold", "30", "Lwr. Rt. Hold", "J907-1 (Red-Grn)", "Q11", "J902-11", "Org-Grn", "FL-11629", "BLUE", "A-19223-R"),
	47: ("power", "31", "Lwr. Lt. Power", "J907-4 (Red-Blu)", "Q3", "J902-9", "Yel-Blu", "FL-11629", "BLUE", "A-15849-L-2"),
	48: ("hold", "32", "Lwr. Lt. Hold", "J907-4 (Red-Blu)", "Q9", "J902-7", "Org-Blu", "FL-11629", "BLUE", "A-15849-L-2"),
	35: ("power", "35", "Upr. Lt. Power", "J907-8 (Red-Gry)", "Q1", "J902-3", "Yel-Gry", "FL-11630", "RED", "A-15849-L"),
	36: ("hold", "36", "Upr. Lt. Hold", "J907-8 (Red-Gry)", "Q5", "J902-1", "Org-Gry", "FL-11630", "RED", "A-15849-L"),
}


def _solenoid_wiring(address: int) -> dict[str, Any]:
	printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
	board = "Fliptronic II board A-15472-1" if address in {33, 34} else "WPC power driver board A-12697-3"
	return {"board": board, "control_wire": wire, "driver_transistor": transistor, "control_connection": drive, "power_connection": voltage}


def _rom_note(address: int) -> str:
	if address not in ROM_SOLENOID_NAMES:
		return ""
	name, wires = ROM_SOLENOID_NAMES[address]
	test = "T.5 FLASHER TEST" if address in T5_ADDRESSES else ("T.12 FLIPPER COIL TEST" if address in T12_ADDRESSES else "T.4 SOLENOID TEST")
	return f" {test}: the ROM pulses public {address} and prints \"{name}\" with the wires {wires}."


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 54):
		if address in FLIPPER_COILS:
			stage, printed, printed_type, voltage, transistor, control, wire, coil, colour, assembly = FLIPPER_COILS[address]
			flipper = {35: "upper left", 36: "upper left", 45: "lower right", 46: "lower right", 47: "lower left", 48: "lower left"}[address]
			label = SOLENOID_LABELS[address]
			notes = (
				f"The {flipper} flipper's {stage} winding (coil {coil}, printed coil colour {colour}, flipper assembly {assembly}), printed "
				f"Fliptronic circuit '{printed_type}' (driver {transistor}, {control}, {wire}, supply {voltage})."
			)
			if address in {45, 46, 47, 48}:
				notes += " PinMAME publishes the lower flipper windings at 45-48."
			else:
				notes += " corvGameData declares FLIP_SOL(FLIP_L | FLIP_UL), so PinMAME publishes the upper left flipper's ROM drive at 35-36."
			notes += _rom_note(address)
			number = {45: 1, 46: 2, 47: 3, 48: 4, 35: 7, 36: 8}[address]
			notes += f" T.12 numbers it {number:02d}."
			notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, FLIPPER_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE)
			spatial = located("solenoid", address, output_id(label), "effect")
			notes += _spatial_note("solenoid", address)
			items.append(_device(
				output_id(label), label, "coil", SOLENOID_GROUP, address, "used", refs,
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=[{35: "flipper.upper.left", 36: "flipper.upper.left", 45: "flipper.lower.right", 46: "flipper.lower.right", 47: "flipper.lower.left", 48: "flipper.lower.left"}[address]],
				physical={"part_number": coil, "assembly_part_number": assembly, "notes": notes},
				wiring={"board": "Fliptronic II board A-15472-1", "driver_transistor": transistor, "control_connection": control, "control_wire": wire, "power_connection": voltage},
				spatial=spatial,
			))
			continue
		if address in {51, 52, 53}:
			label = SOLENOID_LABELS[address]
			refs = (MANUAL_SOURCE, CORE_SOURCE, ENGINE_TEST_SOURCE, ENGINE_FAILED_SOURCE, VPX_SCRIPT_SOURCE)
			if address == 51:
				refs += (ZR1_ADJUST_SOURCE,)
			notes = SOLENOID_NOTES[address] + f" Retained script: {SOLENOID_SCRIPT[address]}."
			items.append(_device(
				output_id(label), label, "control_signal", SOLENOID_GROUP, address, "used", refs,
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				physical={"location": "Motor Driver Master Board in the backbox", "assembly_part_number": "A-18532", "notes": notes},
				wiring={"board": "Motor Driver Master Board A-18532", "control_connection": "J3 ribbon to Slave Board A-18533 J3", "driver_transistor": "ULN2803 (U4)"},
				spatial=not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE),
			))
			continue
		if address in SOLENOID_TABLE:
			label = SOLENOID_LABELS[address]
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
			notes = f"Printed solenoid table entry {address:02d} ({printed_type}, driver {transistor}, wire {wire}). " + SOLENOID_NOTES[address]
			notes += _rom_note(address)
			if address == 6:
				notes += " T.4 skips from 05 to 07."
			unused = address in {6, 14}
			kind = "flasher" if address in FLASHER_SOLENOIDS else ("motor" if address in {18, 19} else ("control_signal" if address == 17 else "coil"))
			physical: dict[str, Any] = {"notes": notes}
			if SOLENOID_ASSEMBLIES.get(address):
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if part and kind != "control_signal":
				physical["part_number"] = part
			if address in {22, 23, 24, 25, 26, 27}:
				physical["quantity"] = 2
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in ROM_SOLENOID_NAMES:
				refs += (FLASHER_TEST_SOURCE,) if address in T5_ADDRESSES else (SOLENOID_TEST_SOURCE,)
			if address in {9, 10, 11, 12, 13}:
				refs += (EDGES_SOURCE,)
			if address in {17, 18, 19}:
				refs += (RACE_TEST_SOURCE,)
			if address in {5, 33}:
				refs += (AMENDMENT_SOURCE,)
			notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
			refs += (VPX_SCRIPT_SOURCE,)
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"wiring": _solenoid_wiring(address),
			}
			if address in {7, 20}:
				extra["roles"] = ["cabinet.knocker"] if address == 7 else ["cabinet.backbox"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "backbox"
			elif unused:
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			elif address == 17:
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
				physical["location"] = "Dual H-Drive Motor Controller A-19159"
			else:
				role = "emitter" if kind == "flasher" else "effect"
				spatial = located("solenoid", address, output_id(label), role)
				if spatial:
					extra["spatial"] = spatial
					notes += _spatial_note("solenoid", address)
					if address in {22, 23, 24, 25, 26, 27}:
						notes += " The placement is the circuit's playfield bulb; its backbox bulb has no playfield position."
				elif address == 26:
					notes += (
						" It has no placement: the script lights the Flasher sprite Flasher126, a glow under the engine, and the light L126, "
						"which is parked off the playfield, so the table has no socket for the playfield bulb."
					)
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(output_id(label), label, kind, SOLENOID_GROUP, address, "unused" if unused else "used", refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		used = address in {29, 30, 31}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Corvette playfield device. The service-test runs saw it change in the menus.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a Corvette playfield device.",
			31: "PinMAME publishes WPC_GILAMPS bit 7 here as the game-on / flipper-enable state because corv.c configures no fast-flip address; the runs saw it change as tests started.",
			32: "PinMAME reports this WPC state channel as always zero; corvGameData declares no use for it.",
			49: "PinMAME's simulator ball-shooter channel: core_getSol serves 49 from sim_getSol, the keyboard simulator's shooter-release flag, which corvSimData's manual shooter raises only while PinMAME keyboard handling runs its simulator. It carries no ROM or machine state and stayed 0 in every run here (keyboard handling off); Corvette has a manual ball shooter and no launch coil.",
			50: "Reserved PinMAME output position before the first custom-output boundary (51).",
		}.get(address, "Unused WPC-Security output: this generation has no LPDC board, so core_getSol returns constant 0 for 37-44 outside WPC-95 and System 11.")
		roles = ["internal.wpc-state"] if used else ["internal.unused.wpc-output"]
		items.append(_device(
			output_id(label), label, "virtual", SOLENOID_GROUP, address, "used" if used else "unused", (CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			roles=roles, physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
		))
	return items


# --- Lamp data (lamp-matrix.md, lamp-locations.md) -------------------------------------------------------
# address -> (bulb part number, lamp assembly, printed description), Lamp Locations lists (2-44, 2-45).
LAMP_LOCATIONS = {
	11: ("24-8768", "A-17624", "Left Rollover"), 12: ("24-8768", "A-17624", "Middle Rollover"), 13: ("24-8768", "A-17624", "Right Rollover"),
	14: ("24-8768", "A-19039", "Skid Pad Arrow"), 15: ("24-8768", "A-19039", "Sticky Tires"), 16: ("24-8768", "A-19039", "Skid Pad Jackpot"),
	17: ("24-8768", "A-19038", "Route 66 Arrow"), 18: ("24-8768", "A-19038", "Race Today"), 21: ("24-8768", "A-19035", "Inner Loop Arrow"),
	22: ("24-8768", "A-19035", "Fuelie"), 23: ("24-8768", "A-19035", "Nitrous"), 24: ("24-8768", "A-19035", "Inner Loop Jackpot"),
	25: ("24-8768", "A-19035", "R Outer Loop Arrow"), 26: ("24-8768", "A-19035", "Z07 Suspension"), 27: ("24-8768", "A-19035", "Big Brakes"),
	28: ("24-8768", "A-19035", "Super Charger"), 31: ("24-8768", "A-19035", "L Outer Loop Arrow"), 32: ("24-8768", "A-19035", "Lite Lock"),
	33: ("24-8768", "A-19035", "Qualify"), 34: ("24-8768", "A-19035", "Big Block"), 35: ("24-8768", "A-19035", "ZR-1 Ramp Lock"),
	36: ("24-8768", "A-19035", "6 Speed Trans"), 37: ("24-8768", "A-19035", "Hi Lift Cams"), 38: ("24-8768", "A-19035", "ZR-1 Ramp Arrow"),
	41: ("24-8768", "A-19037", "Corvette 6"), 42: ("24-8768", "A-19037", "Corvette 3"), 43: ("24-8768", "A-19037", "Corvette 1"),
	44: ("24-8768", "A-19037", "Corvette 2"), 45: ("24-8768", "A-19037", "Corvette 4"), 46: ("24-8768", "A-17347", "Left Standup 3"),
	47: ("24-8768", "A-17347", "Left Standup 2"), 48: ("24-8768", "A-17347", "Left Standup 1"), 51: ("24-8768", "A-19037", "Corvette 9"),
	52: ("24-8768", "A-19037", "Corvette 8"), 53: ("24-8768", "A-17272", "*Pit Stop"), 54: ("24-8768", "A-19037", "Corvette 7"),
	55: ("24-8768", "A-19037", "Corvette 5"), 56: ("24-6549", "A-17807", "Pit Stop Arrow"), 57: ("24-6549", "A-17835", "Spinner Arrow"),
	58: ("24-6549", "A-17807", "Drive Again"), 61: ("24-8768", "A-19036", "Left Outer Tail"), 62: ("24-8768", "A-19036", "Left Inner Tail"),
	63: ("24-8768", "A-19036", "Catch Me"), 64: ("24-8768", "A-19036", "Right Inner Tail"), 65: ("24-8768", "A-19036", "Right Outer Tail"),
	66: ("24-8768", "A-19038", "Right Standup Arrow"), 67: ("24-8768", "A-19038", "Lite Kickback"), 68: ("24-8768", "A-17272", "*Start Challenge"),
	71: ("24-6549", "A-17807", "Kickback Arrow"), 72: ("24-6549", "A-17835", "Left Return Lane"), 73: ("24-6549", "A-17835", "Right Return Lane"),
	74: ("24-6549", "A-17835", "Right Out Lane"), 75: ("24-6549", "A-17835", "Million Standup"), 76: ("24-8768", "A-17826", "Side Pipe 1"),
	77: ("24-8768", "A-17826", "Side Pipe 2"), 78: ("24-8768", "A-17826", "Side Pipe 3"), 81: ("24-8768", "A-18820", "*Right Tree Red"),
	82: ("24-8768", "A-18820", "*Left Tree Red"), 83: ("24-8768", "A-18820", "*Tree Bottom Yellow"), 84: ("24-8768", "A-18820", "*Tree Top Yellow"),
	85: ("24-8768", "A-18820", "*Right Tree Green"), 86: ("24-8768", "A-18820", "*Left Tree Green"), 87: ("20-9663-18", None, "**Buy In"),
	88: ("20-9663-2", None, "**Start Button"),
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"), 3: ("Red-Orange", "J133-4", "Q88"),
	4: ("Red-Yellow", "J133-5", "Q87"), 5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
# The ROM's T.8 SINGLE LAMPS names (single-lamps run).
ROM_LAMP_NAMES = {
	11: "L. ROLLOVER", 12: "M. ROLLOVER", 13: "R. ROLLOVER", 14: "SKID PAD ARROW", 15: "STICKY TIRES", 16: "SKID PAD JACKPOT",
	17: "ROUTE 66 ARROW", 18: "RACE TODAY", 21: "INNER LOOP ARROW", 22: "FUELIE", 23: "NITROUS", 24: "IN. LOOP JACKPOT",
	25: "R. O. LOOP ARROW", 26: "Z07 SUSPENSION", 27: "BIG BRAKES", 28: "SUPER CHARGER", 31: "L. O. LOOP ARROW", 32: "LITE LOCK",
	33: "QUALIFY", 34: "BIG BLOCK", 35: "ZR1 RAMP LOCK", 36: "6 SPEED TRANS", 37: "HI LIFT CAMS", 38: "ZR1 RAMP ARROW",
	41: "CORVETTE 6", 42: "CORVETTE 3", 43: "CORVETTE 1", 44: "CORVETTE 2", 45: "CORVETTE 4", 46: "L. STANDUP 3",
	47: "L. STANDUP 2", 48: "L. STANDUP 1", 51: "CORVETTE 9", 52: "CORVETTE 8", 53: "PIT STOP", 54: "CORVETTE 7",
	55: "CORVETTE 5", 56: "PIT STOP ARROW", 57: "SPINNER ARROW", 58: "DRIVE AGAIN", 61: "L. OUTER TAIL", 62: "L. INNER TAIL",
	63: "CATCH ME", 64: "R. INNER TAIL", 65: "R. OUTER TAIL", 66: "R. STANDUP ARROW", 67: "LITE KICKBACK", 68: "START CHALLENGE",
	71: "KICKBACK ARROW", 72: "L. RETURN LANE", 73: "R. RETURN LANE", 74: "R. OUT LANE", 75: "MILLION STANDUP", 76: "SIDE PIPE 1",
	77: "SIDE PIPE 2", 78: "SIDE PIPE 3", 81: "R. TREE RED", 82: "L. TREE RED", 83: "TREE BOT. YELLOW", 84: "TREE TOP YELLOW",
	85: "R. TREE GREEN", 86: "L. TREE GREEN", 87: "BUY IN", 88: "START BUTTON",
}
LAMP_MATRIX_TEXT = {35: "ZR-1 Ramp", 73: "Right Return lane", 74: "Right Our Lane"}
# Lamps the retained script draws on flasher sprites rather than lights (UpdateLamps).
RACE_TREE_LAMPS = frozenset({81, 82, 83, 84, 85, 86})
LAMP_FLASH_BINDINGS = {address: f"Flash {address}, f{address} draws it on the flasher sprite f{address}" for address in (53, 68, 76, 77, 78, 81, 82, 85, 86)}
LAMP_FLASH_BINDINGS.update({address: f"Flashm {address}, f{address}a and Flash {address}, f{address} draw it on two flasher sprites" for address in (83, 84)})
ROW_WIRE = ("BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY")
COLUMN_WIRE = ("BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY")


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			bulb, assembly, description = LAMP_LOCATIONS[address]
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			physical: dict[str, Any] = {"quantity": 1, "part_number": bulb}
			if assembly:
				physical["assembly_part_number"] = assembly
			bulb_name = {"24-8768": "#555", "24-6549": "#44"}.get(bulb)
			notes = (
				f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire}). Lamp Locations description "
				f"\"{description}\", bulb {bulb}" + (f" ({bulb_name})." if bulb_name else ".")
			)
			if address in LAMP_MATRIX_TEXT:
				notes += f" The matrix cell prints \"{LAMP_MATRIX_TEXT[address]}\"."
			if address == 62:
				notes += " The matrix cell prints its lamp number as a single '2' in all three printings."
			notes += (
				f" The Power Driver Board's pin list (3-30, 3-31) prints J133 and J137 Not Used and routes the playfield lamp columns on J138-{(1, 2, 3, 4, 5, 6, 7, 9)[column - 1]} "
				f"and the rows on J135-{(1, 2, 4, 5, 6, 7, 8, 9)[row - 1]}, where the Lamp Matrix prints J137/J138 columns and J133 rows; the wire colours agree, so the "
				"connector is a wiring detail and the wiring record follows the game's own matrix page."
			)
			notes += (
				f" The ROM's T.8 SINGLE LAMPS TEST lights public lamp {address} alone and names it \"{ROM_LAMP_NAMES[address]}\" "
				f"(RED-{ROW_WIRE[row - 1]} YEL-{COLUMN_WIRE[column - 1]})."
			)
			if address in {53, 68}:
				notes += " The list's '*' marks the lamps whose bulb sleeve colour the bulb-sleeve footnote covers."
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"wiring": {
					"board": "WPC power driver board A-12697-3", "drive_wire": drive_wire, "drive_connection": drive_connection,
					"return_wire": return_wire, "return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address in {83, 84}:
				physical["quantity"] = 2
				notes += (
					" The lamp drawing's Race Tree Lamps inset draws eight bulbs and runs two leaders from this callout, to the "
					+ ("second" if address == 83 else "top") + " pair, so this circuit lights two bulbs."
				)
			if address in RACE_TREE_LAMPS:
				physical["location"] = "race tree over the race track"
				notes += " One of the six lamp circuits (eight bulbs) of the race 'Christmas tree' (Xmas Tree Lamp & Bracket assembly) by the race track."
			if address in {87, 88}:
				extra["roles"] = ["cabinet.buy-in"] if address == 87 else ["cabinet.start-button-lamp"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "cabinet button"
				notes += " The list's '**' reads 'Located on Cabinet': the lamp inside the lit " + ("Buy In" if address == 87 else "Start") + " button."
				notes += " Retained script: no binding (the table draws no cabinet button lamps)."
			else:
				identifier = f"lamp.matrix-{address}"
				spatial = located("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
				if address in LAMP_FLASH_BINDINGS:
					notes += f" Retained script: {LAMP_FLASH_BINDINGS[address]}."
				if address in LAMP_FLASH_BINDINGS and not spatial:
					notes += (
						" It has no placement: a Flasher sprite is a glow, not evidence of a socket, and the table has no Light or socket "
						"object for this lamp"
					)
					if address in RACE_TREE_LAMPS:
						notes += (
							"; the race tree sprites are hidden (is_visible false), and the lamp drawing shows the race tree only in its own "
							"Race Tree Lamps inset, which has no playfield frame to measure in."
						)
					else:
						notes += "."
				elif address not in LAMP_FLASH_BINDINGS:
					notes += f" Retained script: NFadeL {address}, l{address} draws it on the light l{address}."
				notes += _spatial_note("lamp", address)
			physical["notes"] = notes
			extra["physical"] = physical
			label = description.lstrip("*").replace("R Outer", "Right Outer").replace("L Outer", "Left Outer")
			items.append(_device(f"lamp.matrix-{address}", label, "lamp", LAMP_GROUP, address, "used", (MANUAL_SOURCE, CORE_SOURCE, LAMP_TEST_SOURCE, VPX_SCRIPT_SOURCE), **extra))
	return items


# --- General illumination (solenoid-flasher-table.md G.I. block; gi-test run) ---------------------------------
# public -> (string, printed name, triac, playfield voltage, backbox voltage, playfield drive, backbox drive, wire, playfield bulb, backbox bulb, ROM name, ROM wires)
GI_STRINGS = {
	0: (1, "Upper Left", "Q18", "J121-1", None, "J121-7", None, "Wht-Brn", "#44", None, "UPPER LEFT", "WHT-BRN BRN"),
	1: (2, "Upper Right", "Q10", "J121-2", None, "J121-8", None, "Wht-Org", "#44", None, "UPPER RIGHT", "WHT-ORN ORN"),
	2: (3, "Lower Left", "Q14", "J121-3", "J120-3", "J121-9", "J120-9", "Wht-Yel", "#44", "#555", "LOWER LEFT", "WHT-YEL YEL"),
	3: (4, "Lower Right", "Q16", "J121-5", "J120-5", "J121-10", "J120-10", "Wht-Grn", "#44", "#555", "LOWER RIGHT", "WHT-GRN GRN"),
	4: (5, "Backbox Title", "Q12", None, "J120-6", None, "J120-11", "Wht-Vio", None, "#555", "BACK BOX TITLE", "WHT-VIO VIO"),
}


# Where the retained table's light collection for each public GI channel sits (its lights' own centres, raw 979 x 2162 units).
GI_SCRIPT_BULBS = {
	0: "seven lights sit on the lower left of the playfield (x 65-201, y 800-1776), not the upper left the string's name gives",
	1: "seven lights sit on the lower right (x 666-846, y 1015-1777), not the upper right",
	2: "six lights sit on the upper left (x 74-453, y 71-514), not the lower left",
	3: "eleven lights sit on the upper right (x 467-923, y 58-872), not the lower right",
}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (string, name, triac, pf_voltage, bb_voltage, pf_drive, bb_drive, wire, pf_bulb, bb_bulb, rom_name, rom_wires) in GI_STRINGS.items():
		places = []
		if pf_drive:
			places.append(f"playfield (voltage {pf_voltage}, drive {pf_drive}, {pf_bulb} bulbs)")
		if bb_drive:
			places.append(f"backbox (voltage {bb_voltage}, drive {bb_drive}, {bb_bulb} bulbs)")
		notes = (
			f"Printed general-illumination row {string:02d} '{name}': triac {triac}, wire {wire}; it feeds the {' and the '.join(places)}. "
			f"The Solenoid/Flasher Locations G.I. list calls it G.I. String {string}. The ROM's T.6 GENERAL ILLUMINATION TEST names it "
			f"'{rom_name}' ({rom_wires}) and steps its brightness on public GI {address} alone."
		)
		notes += (
			" The Power Driver Board's pin list (3-30) labels J121 'Return G.I. to insert' / '6.8VAC to insert' and J120 '... to playfield', the "
			"reverse of the table's Playfield and Backbox columns. The table's columns agree with its bulb columns (#44 for playfield, #555 for "
			"backbox) and its string names (Upper Left, Upper Right, Backbox Title), so the records follow the table and the board list's labels "
			"are noted here as a disagreement of that page alone."
		)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{string:02d}"}],
			"wiring": {"board": "WPC power driver board A-12697-3", "driver_transistor": triac, "control_connection": ", ".join(x for x in (pf_drive, bb_drive) if x), "control_wire": wire, "power_connection": ", ".join(x for x in (pf_voltage, bb_voltage) if x)},
		}
		if address == 4:
			notes += " Retained script: UpdateGi has no case for 4 ('GI5 is Backglass Only')."
			extra["roles"] = ["cabinet.backbox"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			extra["physical"] = {"location": "backbox", "notes": notes}
		else:
			notes += (
				f" Retained script: GiCallBack2 UpdateGi switches the light collection GI{address + 1} from public GI {address}, and those "
				f"{GI_SCRIPT_BULBS[address]}. The table's bulbs are not this string's playfield position: see the G.I. string conflict, so the "
				"string has no placement."
			)
			extra["physical"] = {"notes": notes}
		items.append(_device(f"gi.string-{string}", f"General Illumination {name}", "gi", GI_GROUP, address, "used", (MANUAL_SOURCE, CORE_SOURCE, GI_TEST_SOURCE, VPX_SCRIPT_SOURCE), **extra))
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 dot-matrix display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE),
		},
	]


# --- Mechanisms, drivers and conflicts -------------------------------------------------------------------
def _coil(address: int) -> str:
	return output_id(SOLENOID_LABELS[address])


def _mechanism(
	suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...],
	positions: list[tuple[str, str, list[str], str]] | None = None, assembly: str | None = None, status: str = "observed",
) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
		"behavior": behavior, "provenance": provenance(status, *refs),
	}
	if assembly:
		record["assembly_part_number"] = assembly
	if positions:
		record["positions"] = [
			{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
			for position_id, position_label, position_sensors, description in positions
		]
	return record


def _matrix(*addresses: int) -> list[str]:
	return [f"switch.matrix-{address}" for address in addresses]


def mechanisms() -> list[dict[str, Any]]:
	flipper_refs = (MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE)
	return [
		_mechanism(
			"zr1-engine", "ZR-1/LT-5 engine (ball shaker)", "other", [_coil(51), _coil(52), _coil(53)], _matrix(71, 72),
			"An engine-shaped toy (Engine & Ramp Assembly A-19140) that rocks left and right as a ball shaker. The engine block A-19135 carries "
			"four coils (AE-25-1000 on coil brackets; its drawing shows four coil positions and the repair bulletin 16-9887 lists ENGINE COILS (4)) "
			"against an engine-shake weldment with a magnet (A-19137); a Hall-effect sensor (A-19230) reads its angle and the "
			"Engine Full-Stroke Opto P.C.B. A-18951 reports FULL LEFT (71) and FULL RIGHT (72). The CPU runs it as a servo: it writes the commanded "
			"angle to extension register 2, which the Motor Driver Master Board A-18532 latches (U1) for the Slave Board A-18533's AD7524 DAC and "
			"LM324/TIP102 coil drivers, and three control bits to extension register 3 (U2), published as 51 (both DISABLE lines, the engine power "
			"enable), 52 (LED A lines) and 53 (LED B lines). The commanded angle is not an output address: with mechanism handling bit 2 on, PinMAME's "
			"engine model takes the register byte as the position, closes 71 below 64 and 72 above 191, and GetMech(2) returns it. The ROM's T.16 "
			"ZR1-LT5 TEST self test raised 51, swept the position down until FULL LEFT closed (63), up until FULL RIGHT closed (192) and parked it "
			"at 127, toggling 52 and 53 while the engine moved; ENGINE LEFT drove it to 63. Without an engine answering, the self test drops 51 after "
			"about 13 s and shows POSITION OFF and FAILED. T.18 ZR-1 ADJUST raises 51 alone and holds the engine centred while a potentiometer on "
			"the Hall Offset Adjust board (Amendment 16-9890) is set; the amendment says the coin door must be closed for engine power, and "
			"Adjustment A.2 16 DISABLE ZR-1/LT-5 runs the game with the engine locked down. The retained known-working table turns on "
			"PinMAME's engine model (HandleMechanics 7) and draws the engine primitive EngineP at (GetMech(2) - 127) / 7 degrees, ignoring "
			"jumps of 30 or more; it binds nothing to 51-53. Its ball shake is a table approximation, not the machine's causality: four "
			"magnet triggers in the engine (cvpmMagnet, solenoid 26, the ZR-1 UNDERSIDE flasher) grab a ball while that flasher output is "
			"on, armed when the ball passes ZR-1 BOTTOM ENTRY (41) and disarmed after more than 100 hits on the rubbers beside the engine "
			"(71/72) until a flipper button resets the count.",
			(MANUAL_SOURCE, AMENDMENT_SOURCE, DISASSEMBLY_SOURCE, CORE_SOURCE, ENGINE_TEST_SOURCE, ENGINE_FAILED_SOURCE, ZR1_ADJUST_SOURCE, VPX_SCRIPT_SOURCE),
			[
				("full-left", "Full left", _matrix(71), "The engine at its left stop; 71 reads 1."),
				("centre", "Centre", [], "Neither full-stroke opto closed; the self test parks the engine at register value 127."),
				("full-right", "Full right", _matrix(72), "The engine at its right stop; 72 reads 1."),
			],
			"A-19140",
		),
		_mechanism(
			"zr1-lock", "ZR-1/LT-5 ramp lock", "kicker", [_coil(2), _coil(5), _coil(15)], _matrix(41, 42, 75, 76, 77, 78),
			"The ZR-1/LT-5 ramp runs into the engine mechanism, where up to three balls lock (ZR-1 LOCK BALL 1-3, switches 76-78) for the "
			"Mid-Ohio Endurance multiball; the ramp has entry optos ZR-1 BOTTOM ENTRY (41) and ZR-1 TOP ENTRY (42) and a ZR-1 EXIT switch (75). "
			"The ZR-1 LOW REV GATE (2, SM1-28-900-DC, in the engine ramp, which carries a flopgate, a front gate and a back gate), the ZR-1 UP "
			"REV GATE (5, SM1-35-4000-DC, which the amendment's back-panel Ball Gate Actuator carries) and the ZR-1 LOCKUP coil (15, AE-30-2000, "
			"Eject Assembly A-15368-1) act on the lock. The rules light LT-5 LOCK from the left outer loop; Adjustment A.2 13 ENDGAME LOCK REL. "
			"decides whether locked balls are released at game end. The retained known-working table gives each coil its runtime contract, "
			"and the ROM decides when to fire them: while 2 (its 'Lock Gate 1') is on, the gate LGate on the engine ramp is closed and the "
			"wall Wall12 beside it raised, and both open when it drops; while 5 ('Lock Gate 2') is on, the upper engine-ramp gate GateU is "
			"open; a ball that reaches the lock kicker Kicker1 joins a ball stack that holds 76, 77 and 78 for one, two and three balls, and "
			"each pulse of 15 ejects one ball at Kicker3, below the lock entry, back onto the playfield. The table puts ZR-1 EXIT (75) as a "
			"gate switch on a ramp at the playfield's upper left corner. No retained source draws the physical gate linkage.",
			(MANUAL_SOURCE, AMENDMENT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE),
			[
				("lock-1", "Lock 1", _matrix(76), "One ball locked."),
				("lock-2", "Lock 2", _matrix(77), "Two balls locked."),
				("lock-3", "Lock 3", _matrix(78), "Three balls locked; multiball follows."),
			],
			"A-19140",
		),
		_mechanism(
			"race-track", "Race track (Corvette Challenge)", "motorized", [_coil(17), _coil(18), _coil(19)], _matrix(51, 55, 52, 56),
			"Two cars race in lanes on the Race Track A-19004 along the right side of the playfield, where the retained table runs the lanes up to the top right corner the rules page's shot map points RACE TRACK at (left car A-19145, the player's blue car; right car "
			"A-19146, the machine's red car), pulled by cords from a Gear Box A-19134 with two 14-8015 motors. The Dual H-Drive Motor Controller "
			"A-19159 takes RACE DIRECTION (17) for both cars and LEFT/RIGHT RACE ENABLE (18, 19) for each motor. Each lane has a start (limit) opto, "
			"51 left and 52 right, and an encoder opto on its cord pulley, 55 and 56. The ROM's T.17 RACE TEST self test drove the left car with 17 "
			"and 18 on, counting its encoder to 670 while 51 opened, then the right car with 17 and 19 to 638, then returned both to their start "
			"optos at count 0; LEFT FORWARD raised 17 and 18 and the left car's count climbed while Enter was held. With PinMAME's car models "
			"(mechanism bits 0 and 1), which move a car forward while 17 is on, that is consistent with 17 on meaning forward. During the CORVETTE "
			"CHALLENGE the machine's car moves at a steady pace and the player's car advances as shots are made; a six-lamp race tree (81-86) "
			"stands over the track. The retained known-working table runs PinMAME's car models (HandleMechanics 7), which write 51, 52, 55 "
			"and 56, and moves the blue (left) and red (right) car primitives along their lanes from GetMech(0) and GetMech(1), mapping counts "
			"0-675 from the start to the finish end at the top of the playfield.",
			(MANUAL_SOURCE, AMENDMENT_SOURCE, DISASSEMBLY_SOURCE, CORE_SOURCE, RACE_TEST_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE),
			[
				("left-start", "Left car at the start", _matrix(51), "The left car on its start opto."),
				("right-start", "Right car at the start", _matrix(52), "The right car on its start opto."),
			],
			"A-19004",
		),
		_mechanism(
			"ball-trough", "Ball trough", "kicker", [_coil(1)], _matrix(31, 32, 33, 34, 37),
			"Outhole Ball Trough Assembly A-18753 with the Trough 7 IRED and IR TSTR boards and four balls: drained balls collect over the "
			"TROUGH BALL 1-4 optos (31-34) and the TROUGH EJECT coil (1) kicks the lowest ball past the TROUGH EJECT opto (37) into the shooter "
			"lane. The optos read a ball at public 1.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("trough-eject", "Trough eject", _matrix(37), "Ball at the eject position."),
				("trough-1", "Trough, 1 ball", _matrix(31), "At least one ball in the trough."),
				("trough-2", "Trough, 2 balls", _matrix(32), "At least two balls."),
				("trough-3", "Trough, 3 balls", _matrix(33), "At least three balls."),
				("trough-4", "Trough, 4 balls", _matrix(34), "All four balls."),
			],
			"A-18753",
		),
		_mechanism(
			"pit-stop-popper", "Pit stop popper", "kicker", [_coil(4)], _matrix(36),
			"The Popper Assembly A-19005 (coil AE-23-800 with a bell armature, LED A-16908 and photo transistor A-16909): a ball in the popper "
			"breaks opto 36 and the PIT STOP POPPER coil (4) kicks it out. The rules start a CORVETTE CHALLENGE from the pitstop shot when START "
			"CHALLENGE is lit.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE), None, "A-19005",
		),
		_mechanism(
			"route-66-kickout", "Route 66 kickout", "kicker", [_coil(8)], _matrix(57),
			"The Kick-Out Coil Assembly A-19006 on the back panel (coil AE-23-800, bell armature, drag flap, and the kickout switch 5647-12693-21, "
			"public 57): the ROUTE 66 KICKOUT coil (8) ejects a ball that the Route 66 ramp delivers behind the race track.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE), None, "A-19006",
		),
		_mechanism(
			"kickback", "Left outlane kickback", "kicker", [_coil(3)], _matrix(11),
			"The KICKBACK coil (3, AE-23-800, Kicker Bracket Assembly B-11873) returns a ball from the left outlane (11) when the kickback is lit "
			"(LITE KICKBACK lamp 67, KICKBACK ARROW 71).",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE, LAMP_TEST_SOURCE), None, "B-11873",
		),
		_mechanism(
			"loop-gate", "Loop gate", "gate", [_coil(16)], [],
			"The LOOP GATE coil (16, A-14406 on assembly A-17796) moves a gate on the loops. The retained known-working table puts the gate "
			"TGate at the top of the playfield, across the loop between the left (87) and right (88) outer-loop switches, and holds it open "
			"while 16 is on and closed when it drops.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, VPX_SCRIPT_SOURCE), None, "A-17796",
		),
		_mechanism(
			"ramp-diverter", "Ramp diverter", "diverter", [_coil(33), _coil(34)], [],
			"The ramp DIVERTER (Flipper Coil Assembly A-15943-1; Ramp Diverter Assembly A-19630 in Amendment 16-9890, with a diverter plunger and "
			"drive arm) runs on the Fliptronic II upper-right circuit: 33 is its power winding and 34 its hold winding. The retained "
			"known-working table moves it from the hold winding alone: while 34 is on it raises the wall DiverterON, drops DiverterOFF and "
			"turns the diverter flipper DivFlipper, at the right of the playfield behind the jet bumpers, and restores them when 34 drops.",
			(MANUAL_SOURCE, AMENDMENT_SOURCE, SOLENOID_TEST_SOURCE, VPX_SCRIPT_SOURCE), None, "A-17241",
		),
		_mechanism(
			"slingshots", "Slingshots", "kicker", [_coil(9), _coil(10)], _matrix(61, 62),
			"Two slingshots with kick and score switches on 61 and 62; the ROM fired 9 for 61 and 10 for 62 even inside the T.1 test.",
			(MANUAL_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE),
		),
		_mechanism(
			"jet-bumpers", "Jet bumpers", "other", [_coil(11), _coil(12), _coil(13)], _matrix(63, 64, 65),
			"Three jet bumpers (B-9414-3, coil assemblies A-9415-2): left (switch 63, coil 11), bottom (64, 12) and right (65, 13). The ROM fired "
			"each coil for its own switch even inside T.1. QUADRAJETS multiplies their value (rules page G).",
			(MANUAL_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE), None, "B-9414-3",
		),
		_mechanism(
			"lower-right-flipper", "Lower right flipper", "other", [_coil(45), _coil(46)], ["switch.generic-111", "switch.generic-112", "switch.generic-116"],
			"Flipper assembly A-19223-R with an FL-11629 coil (power 45, hold 46) and an end-of-stroke switch (F1, 111) that PinMAME synthesizes. "
			"The right cabinet button's board carries two optos, F2 (112) and F6 (116), and the ROM fires this flipper from either.",
			flipper_refs, None, "A-19223-R",
		),
		_mechanism(
			"lower-left-flipper", "Lower left flipper", "other", [_coil(47), _coil(48)], ["switch.generic-113", "switch.generic-114"],
			"Flipper assembly A-15849-L-2 with an FL-11629 coil (power 47, hold 48) and an end-of-stroke switch (F3, 113) that PinMAME "
			"synthesizes, worked by the left button's F4 opto (114).",
			flipper_refs, None, "A-15849-L-2",
		),
		_mechanism(
			"upper-left-flipper", "Upper left flipper", "other", [_coil(35), _coil(36)], ["switch.generic-117", "switch.generic-118"],
			"Flipper assembly A-15849-L with an FL-11630 coil (power 35, hold 36) and an end-of-stroke switch (F7, 117) that PinMAME "
			"synthesizes, worked by the left button's second opto (F8, 118); the left button therefore fires both left flippers.",
			flipper_refs, None, "A-15849-L",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.gi-string-halves",
			"path": "outputs[binding.group=pinmame.output.gi,binding.device=0|1|2|3].spatial",
			"description": (
				"The manual's Solenoid/Flasher Table names G.I. strings 1-4 Upper Left, Upper Right, Lower Left and Lower Right, and the ROM's "
				"T.6 GENERAL ILLUMINATION TEST names public GI 0-3 UPPER LEFT, UPPER RIGHT, LOWER LEFT and LOWER RIGHT with the same wires, "
				"but the retained known-working table drives its lower-left bulbs from GI 0, its lower-right bulbs from GI 1, its upper-left "
				"bulbs from GI 2 and its upper-right bulbs from GI 3: the top and bottom halves are swapped. Which bulbs a string feeds is a "
				"physical fact; the manual's string names claim it, but no retained wiring drawing, bulb list or location drawing assigns "
				"individual playfield bulbs to a string, so neither reading is proven and no G.I. string has a placement. "
				"Resolution path: run T.6 on a physical Corvette and note which playfield bulbs dim for UPPER LEFT; an owner of the machine "
				"could do it in a minute."
			),
			"source_refs": [MANUAL_SOURCE, GI_TEST_SOURCE, VPX_SCRIPT_SOURCE],
		},
	]


def drivers() -> list[dict[str, Any]]:
	by_id = {item["id"]: item for item in load_json(ROOT / "catalog/pinmame.json")["drivers"]}
	result = []
	for driver_id in DRIVER_IDS:
		item = {key: value for key, value in by_id[driver_id].items() if key in {"id", "clone_of", "description", "year", "manufacturer", "flags"}}
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		result.append(item)
	return result


# --- Sources -------------------------------------------------------------------------------------------
TRANSCRIBED = "curator, read from the rendered page"
DELEGATED = "delegated transcription from the rendered page; spot-checked by the curator, not checked cell by cell"


DRAWING_DERIVATIONS = {
	"switch-locations": "Bally_1994_Corvette_Manual.pdf page 109, crop box 0.37,0.04,0.87,0.6, scanned page rendered at its native resolution (embedded image xref 435, 2128px across 7.21in), rendered at 295 dpi, grayscale, 1221x1792 WebP quality 80",
	"lamp-locations": "Bally_1994_Corvette_Manual.pdf page 107, crop box 0.49,0.075,0.995,0.875, scanned page rendered at its native resolution (embedded image xref 427, 2448px across 8.18in), rendered at 299 dpi, grayscale, 1250x2594 WebP quality 80",
	"solenoid-flasher-locations": "Bally_1994_Corvette_Manual.pdf page 111, crop box 0.28,0.04,0.81,0.565, scanned page rendered at its native resolution (embedded image xref 443, 2336px across 7.88in), rendered at 296 dpi, grayscale, 1299x1687 WebP quality 80",
}


def _excerpt(name: str, locator: str, *, image: bool = False, method: str = "manual", reviewed: bool = True, credit: str = TRANSCRIBED) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.corvette.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if image:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = DRAWING_DERIVATIONS[name]
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("dip-switch-chart", "PDF page 2, DIP SWITCH SETTINGS AND JUMPERS"),
		_excerpt("switch-matrix", "PDF page 108, printed 2-46, Switch Matrix with the dedicated and flipper grounded-switch blocks and the opto shading; Section 3 reprint PDF 116 (3-2) compared; Dedicated Switches drawing PDF 117 (3-3)", credit="delegated transcription from the rendered page; checked against the page by the curator"),
		_excerpt("switch-locations", "PDF pages 108-109, printed 2-46 and 2-47, Switch Locations list and the callout numbers of its drawing (image: the playfield drawing)", image=True, credit="delegated transcription from the rendered page; checked against the page by the curator"),
		_excerpt("lamp-matrix", "PDF page 106, printed 2-44, Lamp Matrix; reprints PDF 118 (3-4) and PDF 155 compared", credit="delegated transcription from the rendered page; checked against the page by the curator"),
		_excerpt("lamp-locations", "PDF pages 106-107, printed 2-44 and 2-45, Lamp Locations list and the callout numbers of its drawing (image: the playfield drawing)", image=True, credit="delegated transcription from the rendered page; checked against the page by the curator"),
		_excerpt("solenoid-flasher-table", "PDF page 110, printed 2-48, Solenoid/Flasher Table with the general-illumination and flipper-circuit blocks; reprint PDF 119 (3-5) compared", credit="delegated transcription from the rendered page; checked cell by cell against the page by the curator"),
		_excerpt("solenoid-flasher-locations", "PDF pages 110-111, printed 2-48 and 2-49, Solenoid/Flasher Locations, G.I. and flipper-coil lists and the callout numbers of the drawing (image: the playfield drawing)", image=True, credit="delegated transcription from the rendered page; checked against the page by the curator"),
		_excerpt("solenoid-wiring-pages", "PDF pages 120-124, printed 3-6 to 3-10, solenoid, flasher, high-power, flashlamp and G.I. circuit drawings", reviewed=False, credit=DELEGATED),
		_excerpt("power-driver-board", "PDF pages 143-145, printed 3-29 to 3-31, Power Driver Board A-12697-3 drawing and connector list", reviewed=False, credit=DELEGATED),
		_excerpt("cpu-board", "PDF page 146, printed 3-32, Security CPU Board A-17651-50036 drawing and connector list", reviewed=False, credit=DELEGATED),
		_excerpt("fliptronic-board", "PDF page 142, printed 3-28, Fliptronic II Board A-15472-1 drawing and connector list", reviewed=False, credit=DELEGATED),
		_excerpt("coin-door-board", "PDF pages 149-150, printed 3-35 and 3-36, Coin Door Interface P.C.B. A-17051-1 and schematic", reviewed=False, credit=DELEGATED),
		_excerpt("section-3-boards", "PDF pages 125-136, printed 3-11 to 3-22, LED and flipper opto boards, flipper circuits, trough boards, 10-opto board, track limit, track encoder and engine full-stroke opto boards; Amendment 16-9890 pages 7 and 8 compared", reviewed=False, credit=DELEGATED),
		_excerpt("motor-boards", "PDF pages 137-141, printed 3-23 to 3-27, Motor Driver Slave and Master boards and the Dual H-Drive Motor Controller; Amendment 16-9890 pages 8, 9, 11 and 12 (A-19625 slave board, Hall adjustment)", reviewed=False, credit="delegated transcription from the rendered page; the Master Board latch trace checked against the page by the curator"),
		_excerpt("mechanism-assemblies", "PDF pages 64, 73-77, 81 and 86-97, printed 2-2 to 2-35, backbox, board, trough, popper, engine, ramp, exhaust, back panel, kick-out, track and gear box parts lists; Amendment 16-9890 pages 10, 11 and 13", reviewed=False, credit=DELEGATED),
		_excerpt("game-rules", "PDF pages 11-18, printed A-H, shot maps and game rules; Amendment 16-9890 page 3 rule changes", reviewed=False, credit=DELEGATED),
		_excerpt("service-tests", "PDF pages 31-35, printed 1-13 to 1-17, the Test menu and T.1-T.18; Amendment 16-9890 pages 1-6 (T.16-T.19, difficulty tables, new adjustments)", reviewed=False, credit=DELEGATED),
		_excerpt("opto-led-fuse", "PDF pages 57-59, printed 1-39 to 1-41, opto theory, LED list and fuse list", reviewed=False, credit=DELEGATED),
	]


RUNTIME_SOURCES = (
	(EDGES_SOURCE, "switch-edges", "One hash-pinned LibPinMAME harness run of corv_21 from empty NVRAM with built-in mechanisms disabled (tools/harness-scenarios/wpc-security/cv-switch-edges.json): inside T.1 SWITCH EDGES every public matrix address 11-88 except 22 and every Fliptronic address 111-118 is set to 1 and back to 0. The ROM names each fitted switch at public 1 (24 on its 1 -> 0 edge; 53, 54, 73, 74 and 85 as NOT USED; 111, 113, 115 and 117 never), fires the sling and jet coils 9-13 for 61-65, the lower right flipper for 112 and 116, the lower left for 114 and the upper left for 118."),
	(SOLENOID_TEST_SOURCE, "solenoid-test", "One hash-pinned run of corv_21 (cv-solenoid-test.json) stepping T.4 SOLENOID TEST: it walks 1-5, 7-19, 33 and 34, naming each driver and its wires and pulsing that public address, and wraps."),
	(FLASHER_TEST_SOURCE, "flasher-test", "One hash-pinned run of corv_21 (cv-flasher-test.json) stepping T.5 FLASHER TEST through 20-28, each named and pulsed, and wrapping."),
	(FLIPPER_TEST_SOURCE, "flipper-coil-test", "One hash-pinned run of corv_21 (cv-flipper-coil-test.json) stepping T.12 FLIPPER COIL TEST: R. FLIP. POWER drives 45 and 46, R. FLIP. HOLD 46, L. FLIP. POWER 47 and 48, L. FLIP. HOLD 48, U.L. FLIP. POWER 35 and 36, U.L. FLIP. HOLD 36."),
	(GI_TEST_SOURCE, "gi-test", "One hash-pinned run of corv_21 (cv-gi-test.json) stepping T.6 GEN'L. ILLUM.: ALL ILLUMINATION dims public GI 0-4, then UPPER LEFT, UPPER RIGHT, LOWER LEFT, LOWER RIGHT and BACK BOX TITLE dim GI 0-4 alone in that order."),
	(LAMP_TEST_SOURCE, "single-lamps", "One hash-pinned run of corv_21 (cv-single-lamps.json) stepping T.8 SINGLE LAMPS TEST through public lamps 11-88, each lit alone and named, and wrapping."),
	(ENGINE_TEST_SOURCE, "engine-test", "One hash-pinned run of corv_21 (cv-engine-test.json) with PinMAME's engine and race-car models on (--handle-mechanics 7): T.16 ZR1-LT5 TEST raises 51, its self test finds FULL LEFT at 63 and FULL RIGHT at 192 and parks the engine at 127, toggling 52 and 53, and ENGINE LEFT drives it to 63."),
	(ENGINE_FAILED_SOURCE, "engine-test-no-mech", "One hash-pinned run of corv_21 (cv-engine-test.json) with built-in mechanisms disabled: nothing answers the full-stroke optos, and the T.16 self test drops 51 and shows POSITION OFF and FAILED."),
	(ZR1_ADJUST_SOURCE, "zr1-adjust", "One hash-pinned run of corv_21 (cv-zr1-adjust.json): T.18 ZR-1 ADJUST raises 51 alone and shows TURN ADJUSTMENT TO CENTER ENGINE."),
	(RACE_TEST_SOURCE, "race-test", "One hash-pinned run of corv_21 (cv-race-test.json) with PinMAME's car models on: T.17 RACE TEST's self test drives each car to the far end with 17 and its enable on, counting its encoder, and returns both to the start optos; LEFT FORWARD raises 17 and 18 while Enter is held."),
)


def source_records() -> list[dict[str, Any]]:
	def pdf(source_id: str, kind: str, name: str, locator: str, sha: str, excerpts: list[dict[str, Any]]) -> dict[str, Any]:
		record = {
			"id": source_id,
			"kind": kind,
			"uri": f"external:{MANUALS_DIRECTORY}/{name}",
			"original_filename": name,
			"sha256": sha,
			"acquired_at": ACQUIRED_AT,
			"locator": locator + f" Direct resource: https://www.ipdb.org/files/570/{name}, downloaded through an interactive browser session.",
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": RIGHTS_NOTE,
		}
		if excerpts:
			record["excerpts"] = excerpts
		return record

	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the corv_* clone tree (corv_21 parent; corv_px3, corv_px4, corv_px5, corv_la1, corv_lx1, corv_dx1, corv_la2, corv_lx2, corv_f61)",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/corv.c (a preliminary simulator) corvGameData: GEN_WPCSECURITY, wpc_dispDMD, FLIP_SW(FLIP_L | FLIP_U) | "
				"FLIP_SOL(FLIP_L | FLIP_UL), three custom solenoids served by corv_getSol from wpc_data[WPC_EXTBOARD3] bits 0-2, the inverted-switch "
				"mask {0x00,0x00,0x00,0x7f,0x07,0x33,0x00,0x03,0x00,0x00,0x00,0x00} (public 31-37, 41-43, 51, 52, 55, 56, 71 and 72 under "
				"wpc_sw2m), corv_handleMech (mechanism bits 0 and 1: the race-car models on 17-19, 51, 52, 55 and 56; bit 2: the engine position "
				"from wpc_data[WPC_EXTBOARD2], 71 below 64 and 72 above 191), corv_getMech and the ROM set definitions; src/wpc/wpc.c WPC_FLIPPERS "
				"returning ~swMatrix and the 29-31 state mirror; src/wpc/core.c core_getSol (37-44 constant zero outside WPC-95) and core_updateSw "
				"(end-of-stroke synthesis); src/wpc/vpintf.c vp_getMech (GetMech returns the driver's getMech while mechanism handling is on). "
				"The runtime runs used a library built from this revision."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-security.json", "revision": "repository",
			"locator": "WPC-Security public switch, DIP, solenoid (including custom outputs from 51), lamp and five-GI address rules with the Fliptronic normalization notes",
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "revision": "retained page, 2026-10-16",
			"sha256": IPDB_PAGE_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				"IPDB machine 570 'Corvette' (Midway Manufacturing Company, trade name Bally, August 1994, model 50036, Williams WPC Security, 5,001 "
				"units, three flippers, an engine-shaped ball shaker and a Matchbox car racetrack), read through an interactive browser session and "
				"retained as ipdb570.html. Its model number matches the manual and the ROM's own identification (50036); its notes quote the "
				"designer on the prototypes' drop targets and four-speed shifter."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", "IPDB machine 570 page, title line to documentation list", reviewed=True, credit="curator, from the retained HTML")],
		},
		pdf(
			MANUAL_SOURCE, "manual", MANUAL_NAME,
			"Midway/Bally Corvette operations manual 16-50036-101 (August 1994): a 156-page scan without a text layer (Windows OCR used only to "
			"find pages). PDF 106-111 carry the lamp, switch and solenoid matrices, the location lists and drawings (2-44 to 2-49), PDF 115-150 "
			"Section 3 wiring.",
			MANUAL_SHA256, _manual_excerpts(),
		),
		pdf(
			AMENDMENT_SOURCE, "service_bulletin", AMENDMENT_NAME,
			"Manual Amendment 16-9890 (September 2, 1994): the new T.18 ZR-1 ADJUST, the changed T.16 and T.17 descriptions (door closed for "
			"engine and track power), T.19 Empty Balls, rule changes, difficulty tables and new adjustments (A.2 13-17), the changed Opto Track "
			"Encoder P.C.B. page, the A-19606 track limit and A-19625 slave boards, the Hall adjustment assembly, the Ramp Diverter A-19630, the "
			"revised Engine Ramp and Track lists and the added Ball Gate Actuator. Its pages are transcribed within the manual's excerpts.",
			AMENDMENT_SHA256, [],
		),
		pdf(
			DISASSEMBLY_SOURCE, "service_bulletin", DISASSEMBLY_NAME,
			"Unit Disassembly For Repair 16-9887 (August 29, 1994): service instructions for the race track (track limit board, track opto board, "
			"cords and springs, gear train, motors) and the engine mechanism. Used for the mechanisms' construction; it changes no address.",
			DISASSEMBLY_SHA256, [_excerpt("unit-disassembly-engine", "PDF page 6, REMOVE RAMP ONLY FROM ENGINE ASSEMBLY procedure and its repair table")],
		),
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/bally/corvette-1994/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working recreation of the physical machine (Goldchicco, 32assassin, Mussinger; table_version 1.4.2, saved "
				f"2026-03-24). Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and "
				f"y/{PLAYFIELD_HEIGHT:g}. Geometry authority only for named table objects."
			),
			"license": "NOASSERTION", "attribution": "Goldchicco, 32assassin, Mussinger", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/corvette-1994/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Retained embedded version 1.4.2 script (3,605 lines). Runtime and mechanism-causality authority: cGameName = \"corv_21\", "
				"HandleMechanics = 7 (PinMAME's engine and race-car models), Controller.Switch(22) and (24) set to 1 at start-up, the "
				"SolCallback table and the subs it names, the cvpmBallStack trough, pit stop, Route 66 and lock stacks, the switch event "
				"subs, Mech_Timer (GetMech(0) and GetMech(1)), UpdateLamps (GetMech(2) and the lamp bindings) and GiCallBack2 UpdateGi."
			),
			"license": "NOASSERTION", "attribution": "Goldchicco, 32assassin, Mussinger", "rights": "NOASSERTION",
			"excerpts": [_excerpt(
				"vpx-script-contract", "script.vbs lines 10-972: eleven verbatim blocks with their line numbers (controller, SolCallback table and "
				"callbacks, G.I., init and ball stacks, engine magnets, kickers, switch events, car animation, lamp bindings, slingshots)",
				credit="curator; quoted verbatim from the retained script by a line-range generator retained under review-artifacts",
			)],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/corvette-1994/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"0.33.3 from the retained version 1.4.2 table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	] + [
		{
			"id": source_id, "kind": "runtime_scenario", "uri": f"internal:{EVIDENCE_DIRECTORY}/corvette-corv_21-{name}.json",
			"revision": PINMAME_REVISION, "locator": locator, "license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		}
		for source_id, name, locator in RUNTIME_SOURCES
	] + [
		{
			"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:tools/seeds/bally/corvette-1994-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-17 factory location-drawing callout check of the manual's lamp drawing 2-45, switch drawing 2-47 and solenoid/flasher "
				"drawing 2-49 (the committed excerpt crops): every callout transcribed by an independent reader working only from the page, per-page control "
				"fits from the jet bumper caps and flipper pivots, and the callout fit; a table placement whose own callout lands within 0.07 "
				"normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays and generators are retained under "
				"review-artifacts with a pinned manifest."
			),
			"license": "NOASSERTION", "attribution": "PinMAME game definitions contributors",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
MISSING = ["variant_differences", "spatial_placement", "unresolved_conflicts"]


def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Corvette",
			"manufacturer": "Bally",
			"year": 1994,
			"kind": "physical_pinball",
			"model_number": "50036",
			"ipdb_id": 570,
			"opdb_id": "GrjDz-MJKN6",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": MISSING,
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "observed",
				"variant_coverage": "observed",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.wpc-security", "hardware_generation": "0x20", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/corvette-1994.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Corvette device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Corvette mechanism {mechanism['id']} names unknown devices: {unknown}")
	seed = load_json(CALLOUT_SEED_PATH)
	drawing_callouts.apply_to_definition(definition, seed, CALLOUT_SOURCE)
	return definition


# --- Spatial report ------------------------------------------------------------------------------------
def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	devices = definition["inputs"] + definition["outputs"] + definition["displays"]
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable_count = 0
	for device in devices:
		spatial = device.get("spatial")
		if spatial is None:
			if device.get("availability", "used") in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_count += 1
			continue
		statuses[spatial["status"]].append(device["id"])
	seed = load_json(CALLOUT_SEED_PATH)
	check = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition), seed.get("limit", drawing_callouts.LIMIT))
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:g}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"amendment_sha256": AMENDMENT_SHA256,
			"spatial_seed_sha256": _file_sha256(SPATIAL_SEED_PATH),
			"callout_seed_sha256": _file_sha256(CALLOUT_SEED_PATH),
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/corvette-1994/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/bally/corvette-1994-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": (
				"The retained table's object for the switch (trigger, gate, target, kicker, bumper, slingshot wall or rubber wall), chosen by "
				"what the script binds, observed and validated where the switch drawing's own callout agrees. Projections, where the table "
				"has no object at the switch: the trough optos 31-34 and the trough eject opto 37 onto the trough kicker BallRelease (the "
				"table's trough is a virtual ball stack); the lock switches 76-78 onto the lock kicker Kicker1; the engine full-stroke optos "
				"71/72 onto the engine primitive EngineP; the race start optos 51/52 onto each car primitive's start point and the encoders "
				"55/56 onto each lane's finish end (the script's finish constants)."
			),
			"lamp": (
				"The script-bound Light's own centre, validated where the lamp drawing's callout agrees. 53 and 68, which the script "
				"draws only on glow sprites, sit on the table's stacked pair of bulb meshes L81P1 and L81P4 (the colour-to-lamp pairing is "
				"unsourced and moves neither by more than 0.0005). The lamps the script draws only on Flasher sprites with no bulb model "
				"(76-78 and the hidden race tree sprites 81-86) have no placement, because a sprite is a glow and not a socket; the race "
				"tree is drawn only in the lamp drawing's separate inset. The cabinet button lamps 87 and 88 are not applicable."
			),
			"solenoid": (
				"The object the solenoid callback moves or lights (trough kicker, gates, kickback plunger, popper and kickout kickers, lock "
				"eject kicker Kicker3, diverter wall, flippers, flasher Lights) or, for the slingshots and jet bumpers, the object that fires "
				"the coil; the race motors 18/19 are projected onto each car's lane start. The flasher circuits 22-25 and 27 carry a backbox "
				"bulb as well; only the playfield bulb is placed. 26 has no placement: the script lights only a glow sprite and a light "
				"parked off the playfield. Validated where the solenoid drawing's callout agrees."
			),
			"gi": (
				"None: the retained table's G.I. collections disagree with the manual's and the ROM's string names on which half of the "
				"playfield each string lights (see the conflict), so strings 0-3 have no placement; string 4 lights the backbox title only and "
				"is not applicable."
			),
		},
		"unresolved_geometry": [
			"General illumination strings 0-3 (public GI 0-3): the table drives its lower bulbs from GI 0/1 and its upper bulbs from GI 2/3, "
			"the reverse of the manual's and the ROM's names, and no retained source assigns individual bulbs to a string, so no string has "
			"a placement until a physical machine's T.6 test settles it.",
			"The trough, lock, engine full-stroke and race-track optos are projections onto the nearest table object that models their "
			"mechanism, not observed sockets; their placements stay observed and are not checked against the drawings.",
			"Lamps 76-78 and 81-86 and the playfield bulb of flasher circuit 26 have no placement: the table draws them only on "
			"Flasher sprites (hidden ones for the race tree) or a light parked off the playfield, and the race tree appears only in the "
			"lamp drawing's inset, which has no playfield frame. Measuring them on the location drawings would place them.",
			"Placements the switch and solenoid drawings do not confirm keep their observed status; the drawing callout check lists them "
			"with the distance or reason.",
		],
		"promotion_decision": (
			"partial: the four playfield G.I. strings have no placement while the table and the manual disagree on which bulbs each "
			"string lights, and nine sprite-only lamps and the playfield bulb of flasher circuit 26 have no socket in the table; every "
			"other fitted playfield device has an observed or validated placement or a controlled not-applicable record."
		),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	lines = [
		"# Corvette (Bally, 1994) spatial blockers",
		"",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest "
		f"`{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`; Manual Amendment 16-9890 `{AMENDMENT_SHA256}`.",
		"",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g} rounded to at most six places.",
		"",
		"## Placement status",
		"",
	]
	for name, items in report["placement_status"].items():
		lines.append(f"- `{name}`: {len(items)} devices")
	lines += [
		f"- controlled `not_applicable` records: {report['not_applicable_device_count']}",
		f"- used devices with no placement record: {len(report['without_placements'])} ({', '.join(f'`{item}`' for item in report['without_placements'])})",
		"",
		"## Projection classes",
		"",
	]
	lines += [f"- **{name}:** {text}" for name, text in report["projection_classes"].items()]
	lines += [
		"",
		"## Drawing callout check",
		"",
		f"{check['rule']} It validates {check['validated']} of the {check['checked']} table placements it checks "
		f"([seed](../../../{check['seed']})); the rest keep their observed status:",
		"",
	]
	for placement_id, item in check["not_validated"].items():
		if "control_offset" in item:
			lines.append(f"- `{placement_id}`: callout {item['label']} on {item['page']}, {max(item['control_offset'], item['callout_offset']):.3f} normalized away.")
		else:
			lines.append(f"- `{placement_id}`: callout {item['label']} on {item['page']}, {item['reason']}.")
	lines += ["", "## Unresolved physical geometry", ""]
	lines += [f"- {item}" for item in report["unresolved_geometry"]]
	lines += ["", "## Promotion decision", "", report["promotion_decision"], ""]
	return "\n".join(lines)


# --- Generation ----------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready Corvette artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Corvette author-ready artifact: {AUTHOR_READY_PATH}")
	definition = build()
	report = build_spatial_report(definition)
	expected = (
		(PARTIAL_PATH, canonical_bytes(definition)),
		(SPATIAL_REPORT_PATH, canonical_bytes(report)),
		(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report).encode("utf-8")),
		(KNOWLEDGE_PATH, KNOWLEDGE_SEED_PATH.read_bytes()),
	)
	for path, content in expected:
		if not path.is_file() or path.read_bytes() != content:
			raise RuntimeError(f"Corvette deterministic artifact drift: {path}")
	print("Corvette definition, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and its generated artifacts")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, knowledge note and spatial report")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
