"""Curate the physical Williams The Flintstones (1994) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is a literal below, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed and the
spatial audit.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept partial: every playfield coordinate comes from one community table and none was checked
# against the factory location drawings, the flashers and G.I. strings have no socket coordinate,
# and the left up/down gate's drawing callout disagrees with the table's gate.
PARTIAL_PATH = ROOT / "machines/partial/williams/the-flintstones-1994.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/the-flintstones-1994.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/the-flintstones-1994.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/the-flintstones-1994.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/the-flintstones-1994.md"
KNOWLEDGE_PATH = "knowledge/williams/the-flintstones-1994.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts/williams.the-flintstones.1994"
EXCERPT_PREFIX = "evidence/excerpts/williams.the-flintstones.1994"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
MANUAL_SOURCE = "manual.williams.the-flintstones.1994.operations-manual"
HANGUP_SOURCE = "service-bulletin.williams.the-flintstones.16-9872"
AMENDMENT_SOURCE = "service-bulletin.williams.the-flintstones.16-9876"
ROM_SOURCE = "rom.the-flintstones.name-tables"
VPX_TABLE_SOURCE = "vpx-table.the-flintstones-1-25-7"
VPX_SCRIPT_SOURCE = "vpx-script.the-flintstones-1-25-7"
VPX_EXTRACTION_SOURCE = "vpx-extraction.the-flintstones-1-25-7"
CORPUS_SCRIPT_SOURCE = "vpx-script.the-flintstones-1-25-8"

MANUAL_NAME = "Williams_1994_The_Flintstones_English_Manual.pdf"
MANUAL_SHA256 = "6c615147ac98e217585858ad17c2dfc56d86897ee6934ea03f2e58a1599d94bb"
HANGUP_SHA256 = "4b6a7f86cd7438cc26a36d86eb314629a7aae2e49f4a686420c3cd81b6d43423"
AMENDMENT_SHA256 = "7c61c946555aebb10224182242b854e78f5202b2dcef37233b0d90d56d817ffe"
TABLE_SHA256 = "88c7a36ade06cf2df8aa78e2ede85d040b11330e45dff69897cc3402f2105384"
SCRIPT_SHA256 = "352efc7660b8257df9f3534c5b01262de8ce10934047907e1a5a8e64e124f94d"
CORPUS_SCRIPT_SHA256 = "1849b2eb5d4afca97aabbedb161289f8b619ab2951489553d6a1b49dda2199de"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CORPUS_SCRIPT_NAME = "The Flintstones (Williams 1994) v1.25.8.vbs"
ROM_ARCHIVE_SHA256 = "a041f2d31ea60013339b7edd806396256cc15eb2b03af21492fe9408273320ff"

EXTRACTION_RELATIVE_PATH = Path("williams/the-flintstones-1994/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/the-flintstones-1994/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "c748c3b416a8cb8b8974c679fe8dcb064f267dd1fb9f650b0bce597bfc4b0d88"
EXTRACTION_FILE_COUNT = 1144
EXTRACTION_TOTAL_BYTES = 386155547

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"
WAYBACK_PREFIX = "https://web.archive.org/web/"
IPDB_FILES = "https://www.ipdb.org/files/888/"

DRIVER_IDS = ("fs_lx5", "fs_lx4", "fs_lx3", "fs_lx2", "fs_la5", "fs_sp2", "fs_dx5", "fs_dx4", "fs_dx2", "fs_sp2d")
_SHARED = "It is declared with the parent's wpc_mSecurityS machine driver and shares fsGameData, so every public address is the same."
_LED = (
	"Community 'LED Ghost Fix' modification of the Williams {base} game ROM, for machines converted to LED lamps; it runs on the "
	"physical machine. {shared} The modification is not a Williams release, so the machine is not asserted identical."
)
DRIVER_COMPATIBILITY = {
	"fs_lx5": ("identical", "Williams LX-5 game ROM (flin_lx5.rom), the parent of the fs clone tree and the firmware both retained scripts run."),
	"fs_lx4": ("identical", f"Williams LX-4 game ROM (flin_lx4.rom), an earlier production revision of the same machine. {_SHARED} Its ROM name tables decode identically to LX-5's."),
	"fs_lx3": ("identical", f"Williams LX-3 game ROM (flin_lx3.rom), an earlier production revision of the same machine. {_SHARED}"),
	"fs_lx2": ("identical", f"Williams LX-2 game ROM (flin_lx2.rom), an earlier production revision of the same machine. {_SHARED} Its ROM name tables decode identically to LX-5's."),
	"fs_la5": (
		"compatible",
		f"Williams LA-5 game ROM (flin_la5.rom). {_SHARED} No retained source says what distinguishes LA-5 from LX-5, so the machine is "
		"not asserted identical.",
	),
	"fs_sp2": (
		"compatible",
		"The LX-5 game ROM (flin_lx5.rom) with the SP-2 sound ROM su2-sp2.rom (FS_P2_SOUND) in place of the production sound set; "
		f"pinned fs.c marks it '// Prototype Sound ??'. {_SHARED} Its game ROM is the LX-5 member, so its name tables are LX-5's.",
	),
	"fs_dx5": ("compatible", _LED.format(base="LX-5", shared=_SHARED)),
	"fs_dx4": ("compatible", _LED.format(base="LX-4", shared=_SHARED)),
	"fs_dx2": ("compatible", _LED.format(base="LX-2", shared=_SHARED)),
	"fs_sp2d": ("compatible", _LED.format(base="LX-5", shared=_SHARED) + " It also carries the SP-2 sound ROM (FS_P2_SOUND)."),
}

# --- Switch matrix (manual printed 2-42 and 3-2). Names follow the ROM's own switch table where the
# printed matrix and list disagree with it (31-35 and 51/53); every label is checked against the ROM.
SWITCH_LABELS = {
	11: "Launch Button", 12: "Ticket Dispenser", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Shooter Lane",
	16: "Upper 3-Bank Left Target", 17: "Upper 3-Bank Center Target", 18: "Upper 3-Bank Right Target",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Extra Ball (Buy-In) Button", 24: "Always Closed", 25: "Machine Exit",
	26: "Upper Left Single Target", 27: "Left Lane Rollover", 28: "Inner Left Lane Rollover",
	31: "Trough Jam", 32: "Trough 1", 33: "Trough 2", 34: "Trough 3", 35: "Trough 4", 36: "Ball Popper",
	37: "Right Ramp Enter", 38: "Left Ramp Enter",
	41: "4-Bank Drop Target R", 42: "4-Bank Drop Target O", 43: "4-Bank Drop Target C", 44: "4-Bank Drop Target K",
	45: "3-Bank Drop Target D", 46: "3-Bank Drop Target E", 47: "3-Bank Drop Target B", 48: "Center Lane Rollover",
	51: "Left & Right 3-Bank Upper Targets", 52: "Left & Right 3-Bank Middle Targets", 53: "Left & Right 3-Bank Lower Targets",
	54: "Lower Left Single Target", 55: "Right Single Target", 56: "Dicta-Bird Target",
	61: "Left Slingshot", 62: "Right Slingshot", 63: "Top Left Jet Bumper", 64: "Top Right Jet Bumper", 65: "Bottom Jet Bumper",
	66: "Top Rollover D", 67: "Top Rollover I", 68: "Top Rollover G",
	71: "Left Outlane", 72: "Left Return Lane", 73: "Right Return Lane", 74: "Right Outlane",
	75: "Upper Right Lane Rollover", 76: "Upper Right Lane Exit", 77: "Right Ramp Exit", 78: "Left Ramp Exit",
}
# The ROM's switch-test text for each matrix address (tools/flintstones_rom_name_tables.py).
ROM_SWITCH_TEXT = {
	11: "LAUNCH BALL", 12: "TICKET OPTO.", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "RT. SHOOTER LANE",
	16: "LFT. BOWLING TGT.", 17: "CNT. BOWLING TGT.", 18: "RGT. BOWLING TGT.", 21: "SLAM TILT", 22: "COIN DOOR CLOSED",
	23: "BUY IN", 24: "ALWAYS CLOSED", 25: "MACHINE EXIT", 26: "UP. LFT. HALF TGT.", 27: "LEFT LANE EXIT",
	28: "LFT. LOOP ENTER", 31: "TROUGH JAM", 32: "TROUGH 1", 33: "TROUGH 2", 34: "TROUGH 3", 35: "TROUGH 4",
	36: "TOP POPPER", 37: "RGHT. RMP. ENTER", 38: "LFT. RMP. ENTER", 41: "BED<R>OCK", 42: "BEDR<O>CK", 43: "BEDRO<C>K",
	44: "BEDROC<K>", 45: "BE<D>ROCK", 46: "B<E>DROCK", 47: "<B>EDROCK", 48: "CENTER LANE EXIT", 51: "LFT. RGHT. TGT. 3",
	52: "LFT. RGHT. TGT. 2", 53: "LFT. RGHT. TGT. 1", 54: "LEFT HALF TGT.", 55: "RIGHT HALF TGT.", 56: "DICTABIRD TARGET",
	61: "LEFT SLING", 62: "RIGHT SLING", 63: "LEFT BUMPER", 64: "RIGHT BUMPER", 65: "BOTM. BUMPER", 66: "<D>IG",
	67: "D<I>G", 68: "DI<G>", 71: "LEFT OUTLANE", 72: "LFT. RET. LANE", 73: "RGT. RET. LANE", 74: "RIGHT OUTLANE",
	75: "RIGHT LANE EXIT", 76: "MACHINE ENTER", 77: "RIGHT RAMP EXIT", 78: "LEFT RAMP EXIT",
}
# Printed switch-matrix cell for each address (manual printed 2-42; the 3-2 copy is identical).
PRINTED_SWITCH_TEXT = {
	11: "Launch Button", 12: "Ticket Disp.", 13: "Start Button", 14: "Plumb Tilt", 15: "Shooter Lane",
	16: 'Upper 3-Bnk Lt. Tgt. "I"', 17: 'Upper 3-Bnk Cr. Tgt. "X"', 18: 'Upper 3-Bnk Rt. Tgt. "I"', 21: "Slam",
	22: "Door Closed", 23: "Extra Ball Button", 24: "Always Closed", 25: '"Machine" Exit', 26: "Upper Lt. Sngl. Tgt.",
	27: "Lt. Lane Rollover", 28: "In. Lt. Lane Rollover", 31: "Trough #1", 32: "Trough #2", 33: "Trough #3",
	34: "Trough #4", 35: "Trough Jam", 36: "Ball Popper", 37: "Rt. Ramp Enter", 38: "Lt. Ramp Enter",
	41: "4-Bnk #1 D.Tgt.", 42: "4-Bnk #2 D. Tgt.", 43: "4-Bnk #3 D. Tgt.", 44: "4-Bnk #4 D. Tgt.", 45: "3-Bnk #1 D. Tgt.",
	46: "3-Bnk #2 D. Tgt.", 47: "3-Bnk #3 D. Tgt.", 48: "Cr. Lane Rollover", 51: "Lt. & Rt. 3-Bnk. Bot. Tgt.",
	52: "Lt. & Rt. 3-Bnk Mid. Tgt.", 53: "Lt. & Rt. 3-Bnk Up. Tgt.", 54: "Low. Lt. Sngl. Tgt.", 55: "Rt. Sngl. Tgt.",
	56: "Dicta-Bird Tgt.", 61: "Lt. Sling", 62: "Rt. Sling", 63: "Top Lt. Jet", 64: "Top Rt. Jet", 65: "Bottom Jet",
	66: 'Top Lt. Rollover "D"', 67: 'Top Cr. Rollover "I"', 68: 'Top Rt. Rollover "G"', 71: "Lt. Out Rollover",
	72: "Lt. Return Rollover", 73: "Rt. Return Rollover", 74: "Rt. Out Rollover", 75: "Up. Rt. Lane Rollover",
	76: "Up. Rt. Lane Exit Rollover", 77: "Rt. Ramp Exit", 78: "Lt. Ramp Exit",
}
UNUSED_MATRIX_ADDRESSES = {57, 58, 81, 82, 83, 84, 85, 86, 87, 88}
# Optical switches the manual's board pages construct as beams the ball breaks (printed 3-20 to 3-22).
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 45, 46, 47}
# fsGameData's inverted-switch mask {0x00,0x00,0x00,0x3f,0x7f,0x00,...} is indexed by matrix column:
# 0x3f normalizes 31-36 and 0x7f normalizes 41-47.
PINMAME_INVERTED_MASK = (0x00, 0x00, 0x00, 0x3F, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
# vpmTimer.PulseSw callers in the retained script: the targets (the 51-56 targets through its hit-target
# animation class), the ramp entrances, the slingshots and jets, the upper right lane, and Trough Jam,
# which SolRelease pulses on every trough eject.
PULSED_SWITCHES = {16, 17, 18, 26, 31, 37, 38, 51, 52, 53, 54, 55, 56, 61, 62, 63, 64, 65, 75}
TWIN_TARGET_SWITCHES = {51, 52, 53}

SWITCH_TYPES = {
	11: "button", 12: "opto", 13: "button", 14: "tilt", 15: "microswitch", 16: "leaf", 17: "leaf", 18: "leaf",
	21: "tilt", 22: "microswitch", 23: "button", 24: "other", 25: "microswitch", 26: "leaf", 27: "microswitch",
	28: "microswitch", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "microswitch",
	38: "microswitch", 41: "opto", 42: "opto", 43: "opto", 44: "opto", 45: "opto", 46: "opto", 47: "opto",
	48: "microswitch", 51: "leaf", 52: "leaf", 53: "leaf", 54: "leaf", 55: "leaf", 56: "leaf", 61: "leaf", 62: "leaf",
	63: "leaf", 64: "leaf", 65: "leaf", 66: "microswitch", 67: "microswitch", 68: "microswitch", 71: "microswitch",
	72: "microswitch", 73: "microswitch", 74: "microswitch", 75: "microswitch", 76: "microswitch", 77: "microswitch",
	78: "microswitch",
}
SWITCH_PARTS = {
	11: "20-9663-B-7", 13: "20-9663-14", 14: "A-15361", 15: "5647-12693-32", 16: "A-18606-7", 17: "A-18606-7",
	18: "A-18606-7", 21: "A-17238", 22: "5543-09268-00", 23: "20-9663-18", 24: "5643-09112-00", 25: "5647-12693-21",
	26: "A-17778-5", 27: "5647-12693-19", 28: "5647-12693-19",
	31: "A-18617 LED with A-18618 transistor", 32: "A-18617 LED with A-18618 transistor",
	33: "A-18617 LED with A-18618 transistor", 34: "A-18617 LED with A-18618 transistor",
	35: "A-18617 LED with A-18618 transistor", 36: "A-16908 LED with A-16909 transistor", 37: "5647-12693-36",
	38: "5647-12693-36", 41: "A-19103", 42: "A-19103", 43: "A-19103", 44: "A-19103", 45: "A-13609", 46: "A-13609",
	47: "A-13609", 48: "5647-12693-19", 51: "A-18606-5 (left bank) with A-18605-5 (right bank)", 52: "A-18605-5",
	53: "A-18605-5", 54: "A-17778-5", 55: "A-17778-5", 56: "A-18607-6", 61: "SW-1A-114 (kick) with SW-1A-120 (score)",
	62: "SW-1A-114 (kick) with SW-1A-120 (score)", 63: "SW-11A-37", 64: "SW-11A-37", 65: "SW-11A-37",
	66: "5647-12693-19", 67: "5647-12693-19", 68: "5647-12693-19", 71: "5647-12693-19", 72: "5647-12693-19",
	73: "5647-12693-19", 74: "5647-12693-19", 75: "5647-12693-19", 76: "5647-12693-08", 77: "5647-12693-21",
	78: "5647-12693-17",
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"),
	3: ("Green-Orange", "J207-3", "U20-16"), 4: ("Green-Yellow", "J207-4", "U20-15"),
	5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"),
	3: ("White-Orange", "J209-3", "U18-5"), 4: ("White-Yellow", "J209-4", "U18-7"),
	5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"), 3: ("Orange-Black", "J205-3"),
	4: ("Orange-Yellow", "J205-4"), 5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"),
	7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute; ROM LEFT COIN SLOT."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute; ROM CENTER COIN SLOT."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute; ROM RIGHT COIN SLOT."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute; ROM 4TH COIN OPTION."),
	5: ("Service Credits / Escape", "service.escape", "Printed Normal Service Credit, Test Escape; ROM ESCAPE."),
	6: ("Volume Down / Down", "service.down", "Printed Normal Vol. Dn, Test Down; ROM DOWN."),
	7: ("Volume Up / Up", "service.up", "Printed Normal Vol. Up, Test Up; ROM UP."),
	8: ("Begin Test / Enter", "service.enter", "Printed Normal Beg. Test, Test Enter; ROM ENTER."),
}
# address -> (label, role, switch type, part, wire, connection, printed matrix label, ROM text)
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "leaf", "SW-1A-194", "Black-Green", "J906-1", "Lower Right E.O.S.", "R. FLIPPER E.O.S."),
	112: ("Lower Right Flipper Button", "flipper.lower.right.button", "opto", "A-17316", "Blue-Violet", "J905-1", "Lower Right Opto", "R. FLIPPER BUTTON"),
	113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "leaf", "SW-1A-194", "Black-Blue", "J906-3", "Lower Left E.O.S", "L. FLIPPER E.O.S."),
	114: ("Lower Left Flipper Button", "flipper.lower.left.button", "opto", "A-17316", "Blue-Gray", "J905-2", "Lower Left Opto", "L. FLIPPER BUTTON"),
	115: ("Upper Right Flipper EOS", "internal.flipper.upper.right.eos", "leaf", "SW-1A-194", "Black-Violet", "J906-4", "Upper Right E.O.S.", "U.R. FLIPPER E.O.S."),
	116: ("Upper Right Flipper Button", "flipper.upper.right.button", "opto", "A-17316", "Black-Yellow", "J905-3", "Upper Right Opto", "U.R. FLIPPER BUT."),
}
UNUSED_FLIPPER_SWITCHES = {
	117: ("Black-Gray", "J906-5", "Upper Left E.O.S."),
	118: ("Black-Blue", "J905-5", "Upper Left Opto"),
}

# --- Normalized playfield coordinates from the retained v1.25.7 extraction, x/964 and y/2162.
# Walls use the mean of their drag points; every placement is observed (no drawing callout check).
SWITCH_POSITIONS = {
	15: [(0.934316, 0.889311)], 16: [(0.224632, 0.215841)], 17: [(0.277291, 0.209721)], 18: [(0.329925, 0.203224)],
	25: [(0.058984, 0.206603)], 26: [(0.231108, 0.311881)], 27: [(0.08779, 0.066519)], 28: [(0.140041, 0.165193)],
	31: [(0.875634, 0.872073)], 32: [(0.875634, 0.872073)], 33: [(0.875634, 0.872073)], 34: [(0.875634, 0.872073)],
	35: [(0.875634, 0.872073)], 36: [(0.324399, 0.076225)], 37: [(0.725196, 0.299369)], 38: [(0.189168, 0.486278)],
	41: [(0.489332, 0.298652)], 42: [(0.511963, 0.322123)], 43: [(0.533137, 0.344893)], 44: [(0.556132, 0.371906)],
	45: [(0.303481, 0.502294)], 46: [(0.304341, 0.475007)], 47: [(0.303208, 0.44979)], 48: [(0.412978, 0.124902)],
	51: [(0.090289, 0.577165), (0.809302, 0.575979)], 52: [(0.089948, 0.6015), (0.809544, 0.601529)],
	53: [(0.089164, 0.624795), (0.809311, 0.627556)], 54: [(0.288768, 0.531363)], 55: [(0.74956, 0.406559)],
	56: [(0.115765, 0.551925)], 61: [(0.220454, 0.738916)], 62: [(0.687495, 0.740306)], 63: [(0.51679, 0.155189)],
	64: [(0.718419, 0.188354)], 65: [(0.551214, 0.252218)], 66: [(0.604157, 0.09667)], 67: [(0.700054, 0.090914)],
	68: [(0.794721, 0.084335)], 71: [(0.06393, 0.742044)], 72: [(0.136462, 0.742044)], 73: [(0.774356, 0.743777)],
	74: [(0.846889, 0.743777)], 75: [(0.90783, 0.075941)], 76: [(0.255668, 0.043356)], 77: [(0.877653, 0.240108)],
	78: [(0.052354, 0.366811)],
}
SWITCH_OBJECTS = {
	15: "Trigger Sw15", 16: "HitTarget Sw16", 17: "HitTarget Sw17", 18: "HitTarget Sw18", 25: "Trigger Sw25",
	26: "HitTarget Sw26", 27: "Trigger Sw27", 28: "Trigger Sw28", 36: "Kicker Kicker36", 37: "Trigger Sw37",
	38: "Gate Sw38", 41: "HitTarget Sw44 (the script's dtRightDrop binds objects Sw41-Sw44 to switches 44-41)",
	42: "HitTarget Sw43 (the script's dtRightDrop binds objects Sw41-Sw44 to switches 44-41)",
	43: "HitTarget Sw42 (the script's dtRightDrop binds objects Sw41-Sw44 to switches 44-41)",
	44: "HitTarget Sw41 (the script's dtRightDrop binds objects Sw41-Sw44 to switches 44-41)",
	45: "HitTarget Sw45", 46: "HitTarget Sw46", 47: "HitTarget Sw47", 48: "Trigger Sw48",
	51: "HitTarget Sw51a (left bank) and Sw51b (right bank)", 52: "HitTarget Sw52a (left bank) and Sw52b (right bank)",
	53: "HitTarget Sw53a (left bank) and Sw53b (right bank)", 54: "HitTarget Sw54", 55: "HitTarget Sw55",
	56: "HitTarget Sw56", 61: "Wall LeftSlingShot (mean of its drag points)", 62: "Wall RightSlingShot (mean of its drag points)",
	63: "Bumper Sw63", 64: "Bumper Sw64", 65: "Bumper Sw65", 66: "Trigger Sw66", 67: "Trigger Sw67", 68: "Trigger Sw68",
	71: "Trigger Sw71", 72: "Trigger Sw72", 73: "Trigger Sw73", 74: "Trigger Sw74", 75: "Trigger Sw75", 76: "Trigger Sw76",
	77: "Trigger Sw77", 78: "Trigger Sw78",
}
TROUGH_PROJECTION = (
	"Projected onto the trough exit kicker BallRelease: the retained table models no trough opto objects (its cvpmTrough holds "
	"the balls virtually and exits them at BallRelease), so the five trough optos share the exit position."
)
SWITCH_PROJECTIONS = {address: TROUGH_PROJECTION for address in (31, 32, 33, 34, 35)}

# --- Solenoid/flasher table (manual printed 2-44; the 3-5 copy is identical).
SOLENOID_LABELS = {
	1: "Ball Trough", 2: "Ball Shooter", 3: "Top Diverter Post", 4: "Top Popper", 5: "3-Bank Drop Reset",
	6: "4-Bank Drop Reset", 7: "Knocker", 8: "Top Diverter", 9: "Right Slingshot", 10: "Left Slingshot",
	11: "Left Jet Bumper", 12: "Middle Jet Bumper", 13: "Right Jet Bumper", 14: "Dicta-Bird", 15: "Lower Left Diverter",
	16: "Lower Right Diverter", 17: "Under Left Ramp Flasher", 18: "Under Right Ramp Flasher", 19: "Flintstones Flasher",
	20: "Popper Ramp Flasher", 21: "Dino Slide Flasher", 22: "Bowl-O-Rama Flasher", 23: "Boulder Machine Motor",
	24: "Boulder Machine Flasher", 25: "Dig Millions Flasher", 26: "Flint Flasher", 27: "Stones Flasher",
	28: "Fred's Choice Flasher",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold", 35: "Right Up/Down Gate", 36: "Left Up/Down Gate",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
PRINTED_SOLENOID_TEXT = {
	1: "Ball Trough", 2: "Ball Shooter", 3: "Top Diverter Post", 4: "Top Popper", 5: "3-Bank Drop Reset", 6: "4-Bank Drop Reset",
	7: "Knocker", 8: "Top Diverter", 9: "Right Sling", 10: "Left Sling", 11: "Left Jet Bumper", 12: "Middle Jet Bumper",
	13: "Right Jet Bumper", 14: "Dictabird", 15: "Lower Lt. Diverter", 16: "Lower Rt. Diverter", 17: "Under Lt. Rmp Fls.",
	18: "Under Rt. Rmp Fls.", 19: "Flintstones Fls.", 20: "Popper Rmp Fls.", 21: "Dino Slide Fls.", 22: "Bowl-O-Rama Fls.",
	23: "Boulder Machine", 24: "Boulder Machine Fls", 25: "Dig Millions Fls.", 26: "Flint Fls.", 27: "Stones Fls.",
	28: "Fred's Choice Fls.", 35: "Top Rt. Up/Dn Gate", 36: "Top Lt. Up/Dn Gate",
}
# The ROM's coil test lists 1-16, 23, 35 and 36 in that order, and its flasher test 17-22 and 24-28.
ROM_COIL_TEXT = {
	1: "TROUGH", 2: "RIGHT SHOOTER", 3: "TOP DIVERT. POST", 4: "TOP POPPER", 5: "3 BANK RESET", 6: "4 BANK RESET",
	7: "KNOCKER", 8: "BACKPANEL DIVRTR", 9: "RIGHT SLING", 10: "LEFT SLING", 11: "TOP LEFT JET", 12: "BOTTOM JET",
	13: "TOP RIGHT JET", 14: "DICTABIRD", 15: "L. RMP. DIVERTER", 16: "R. RMP. DIVERTER", 23: "MACHINE MOTOR",
	35: "R. UP/DWN GATE", 36: "L. UP/DWN GATE",
	17: "LFT. RAMP FLS.", 18: "RGHT. RAMP FLS.", 19: "BOTTOM ARCH FLS.", 20: "BTM. 3 BNK. FLS.", 21: "TOP POPPER FLS.",
	22: '"BOWLORAMA"', 24: "MACHINE FLS.", 25: '"DIG MILLIONS"', 26: "FLINT IN BACKBOX", 27: "STONE IN BACKBOX",
	28: '"FREDS CHOICE"',
}
ROM_COIL_ENTRY = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 23: 17, 35: 18, 36: 19}
ROM_FLASHER_ENTRY = {17: 1, 18: 2, 19: 3, 20: 4, 21: 5, 22: 6, 24: 7, 25: 8, 26: 9, 27: 10, 28: 11}
FLASHERS = {17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28}
BACKBOX_FLASHERS = {26, 27}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B",
	31: "WPC Game-On State", 32: "Unused WPC State Channel 32",
	37: "Unused WPC-Security Output 37", 38: "Unused WPC-Security Output 38",
	39: "Unused WPC-Security Output 39", 40: "Unused WPC-Security Output 40",
	41: "Unused WPC-Security Output 41", 42: "Unused WPC-Security Output 42",
	43: "Unused WPC-Security Output 43", 44: "Unused WPC-Security Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# Printed 37*-44* rows: "Not Used", Low Power, with a transistor and a drive wire but no connection.
PRINTED_UNUSED_OUTPUTS = {
	37: ("Q16", "Brn-Wht"), 38: ("Q15", "Blk-Wht"), 39: ("Q14", "Org-Wht"), 40: ("Q13", "Yel-Wht"),
	41: ("Q9", "Grn-Wht"), 42: ("Q10", "Blu-Wht"), 43: ("Q11", "Vio-Wht"), 44: ("Q12", "Gry-Wht"),
}
# address -> (printed type, voltage connection, transistor, drive connection, drive wire, part or lamp)
SOLENOID_WIRING = {
	1: ("High Power", "J107-2", "Q82", "J130-1", "Vio-Brn", "AE-26-1500"),
	2: ("High Power", "J107-2", "Q80", "J130-2", "Vio-Red", "AE-23-800"),
	3: ("High Power", "J107-2", "Q78", "J130-4", "Vio-Org", "AE-27-1200"),
	4: ("High Power", "J107-2", "Q76", "J130-5", "Vio-Yel", "AE-23-800"),
	5: ("High Power", "J107-2", "Q64", "J130-6", "Vio-Grn", "AE-26-1200"),
	6: ("High Power", "J107-2", "Q66", "J130-7", "Vio-Blu", "AE-24-900"),
	7: ("High Power", "J107-2 (Backbox)", "Q68", "J130-8 (Backbox)", "Vio-Blk", "AE-23-800"),
	8: ("High Power", "J107-2", "Q70", "J130-9", "Vio-Gry", "AE-27-1200"),
	9: ("Low Power", "J107-3", "Q58", "J127-1", "Brn-Blk", "AE-26-1200"),
	10: ("Low Power", "J107-3", "Q56", "J127-3", "Brn-Red", "AE-26-1200"),
	11: ("Low Power", "J107-3", "Q54", "J127-4", "Brn-Org", "AE-26-1200"),
	12: ("Low Power", "J107-3", "Q52", "J127-5", "Brn-Yel", "AE-26-1200"),
	13: ("Low Power", "J107-3", "Q50", "J127-6", "Brn-Grn", "AE-26-1200"),
	14: ("Low Power", "J107-3", "Q48", "J127-7", "Brn-Blu", "AE-28-1500"),
	15: ("Low Power", "J107-3", "Q46", "J127-8", "Brn-Vio", "AE-27-1200"),
	16: ("Low Power", "J107-3", "Q44", "J127-9", "Brn-Gry", "AE-27-1200"),
	17: ("Low Power", "J107-6 (Playfield) / J106-5 (Backbox)", "Q42", "J126-1 (Playfield) / J125-1 (Backbox)", "Blk-Brn", "#89 (1) playfield, #906 (2) backbox"),
	18: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q40", "J126-2 (Playfield) / J125-2 (Backbox)", "Blk-Red", "#89 (1) playfield, #906 (2) backbox"),
	19: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q38", "J126-3 (Playfield) / J125-3 (Backbox)", "Blk-Org", "#906 (1) playfield, #906 (2) backbox"),
	20: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q36", "J126-4 (Playfield) / J125-5 (Backbox)", "Blk-Yel", "#89 (2) playfield, #906 (2) backbox"),
	21: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q28", "J126-5 (Playfield) / J125-6 (Backbox)", "Blu-Grn", "#89 (1) playfield, #906 (2) backbox"),
	22: ("Flasher", "J107-6", "Q30", "J126-6", "Blu-Blk", "#89(1)#906(1) playfield"),
	23: ("Motor", "J118-2", "Q34", "J126-7", "Blu-Vio", "14-7999"),
	24: ("Flasher", "J107-6", "Q32", "J126-8", "Blu-Gry", "#89 (1) playfield"),
	25: ("Gen. Purpose", "J107-6", "Q26", "J122-1", "Blu-Brn", "#89 (1) playfield"),
	26: ("Gen. Purpose", "J106-5 (Backbox)", "Q24", "J124-2 (Backbox)", "Blu-Red", "#906 (3) backbox"),
	27: ("Gen. Purpose", "J106-5 (Backbox)", "Q22", "J124-3 (Backbox)", "Blu-Org", "#906 (3) backbox"),
	28: ("Gen. Purpose", "J107-6", "Q20", "J122-4", "Blu-Yel", "#906 (2) playfield"),
	33: ("Fliptronic power", "J907-6 (Red-Vio)", "Q2", "J902-6", "Yel-Vio", "FL-11629"),
	34: ("Fliptronic hold", "J907-6 (Red-Vio)", "Q7", "J902-4", "Org-Vio", "FL-11629"),
	35: ("Fliptronic power", "J907-8 (Red-Gry)", "Q1", "J902-3", "Yel-Gry", "A-14406"),
	36: ("Fliptronic hold", "J907-8 (Red-Gry)", "Q5", "J902-1", "Org-Gry", "A-14406"),
	45: ("Fliptronic power", "J907-1 (Red-Grn)", "Q4", "J902-13", "Yel-Grn", "FL-11629"),
	46: ("Fliptronic hold", "J907-1 (Red-Grn)", "Q11", "J902-11", "Org-Grn", "FL-11629"),
	47: ("Fliptronic power", "J907-4 (Red-Blu)", "Q3", "J902-9", "Yel-Blu", "FL-11629"),
	48: ("Fliptronic hold", "J907-4 (Red-Blu)", "Q9", "J902-7", "Org-Blu", "FL-11629"),
}
# Printed flipper-circuit numbers (manual.address aliases) for the public Fliptronic addresses.
PRINTED_FLIPPER_CIRCUITS = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34", 35: "35", 36: "36"}
# Bulbs each flasher output lights: the table's parenthesized playfield counts plus its backbox counts.
FLASHER_QUANTITY = {17: 3, 18: 3, 19: 3, 20: 4, 21: 3, 22: 2, 24: 1, 25: 1, 26: 3, 27: 3, 28: 2}
SOLENOID_ASSEMBLIES = {
	1: "A-18753", 2: "A-14525", 3: "A-17932", 4: "A-15769-1", 5: "A-16032-1", 6: "A-18188", 7: "B-10686-1", 8: "A-18369",
	9: "B-9362-R-3", 10: "B-9362-L-2", 11: "A-9415-2", 12: "A-9415-2", 13: "A-9415-2", 14: "A-18078", 15: "A-19097-2",
	16: "A-19097-1", 17: "A-17983", 18: "A-17983", 19: "A-17802", 20: "A-17983", 21: "A-17803", 22: "A-17803 and A-17802",
	23: "A-17978", 24: "A-17983", 25: "A-17803", 33: "A-15849-R-2", 34: "A-15849-R-2", 35: "A-17796", 36: "A-17796",
	45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
SOLENOID_CALLBACKS = {
	1: "SolRelease (pulses switch 31 and ejects a ball from the cvpmTrough at BallRelease)",
	2: "vpmSolAutoPlungeS AutoPlunger (fires the plunger AutoPlunger)",
	3: "SolTopDiverter (makes the primitive DiverterPost collidable while the coil is on)",
	4: "bsKicker36.SolOut (ejects the ball held on Kicker36; the script's comment calls it the Bronto/Machine VUK)",
	5: "SolLeftDrop (dtLeftDrop.SolDropUp, raising sw45-sw47)",
	6: "SolRightDrop (dtRightDrop.SolDropUp, raising sw41-sw44)",
	7: "vpmSolSound Knocker",
	8: "SolBrontoDiverter (swings the flipper object BrontoDiverter to its end and moves the Diverter primitive while the coil is on)",
	9: "sRightSlingshot", 10: "sLeftSlingshot",
	14: "SetLamp 114 (a fading callback that tilts the Dictabird primitive)",
	15: "SolLeftApronDiverter (moves DiverterPostLeft and makes the DiverterLeft primitive non-collidable while the coil is on)",
	16: "SolRightApronDiverter (moves DiverterPostRight and makes the DiverterRight primitive non-collidable while the coil is on)",
	17: "FadeLights.LampMod 117 (SolModCallback)", 18: "FadeLights.LampMod 118 (SolModCallback)",
	19: "FadeLights.LampMod 119 (SolModCallback)", 20: "FadeLights.LampMod 120 (SolModCallback)",
	21: "FadeLights.LampMod 121 (SolModCallback)", 22: "FadeLights.LampMod 122 (SolModCallback)",
	23: "SolMachine (switches the cvpmTurnTable ttMachine's motor on and off)",
	24: "FadeLights.LampMod 124 (SolModCallback)", 25: "FadeLights.LampMod 125 (SolModCallback)",
	28: "SolModCallBack(28) = Flasher28 (fades lamp 128, the RG5 and RG13 plastics flasher primitives and the lights Fl002-Fl004)",
	35: "SolGateRGate (makes the gate Gate2 non-collidable while the coil is on)",
	36: "SolGateLGate (makes the gate Gate4 non-collidable while the coil is on)",
	33: "no callback of its own; SolRFlipper, bound to the lower right flipper through SolCallback(sLRFlipper), swings FlipperRight1 together with FlipperRight",
	34: "no callback of its own; SolRFlipper, bound to the lower right flipper through SolCallback(sLRFlipper), swings FlipperRight1 together with FlipperRight",
	46: "SolRFlipper through SolCallback(sLRFlipper), which swings both FlipperRight and FlipperRight1",
	48: "SolLFlipper through SolCallback(sLLFlipper)",
}
SOLENOID_POSITIONS = {
	1: [(0.875634, 0.872073)], 2: [(0.937911, 0.945584)], 3: [(0.32297, 0.019385)], 4: [(0.324399, 0.076225)],
	5: [(0.303677, 0.475697)], 6: [(0.522641, 0.334394)], 8: [(0.32433, 0.01459)], 9: [(0.687495, 0.740306)],
	10: [(0.220454, 0.738916)], 11: [(0.51679, 0.155189)], 12: [(0.551214, 0.252218)], 13: [(0.718419, 0.188354)],
	14: [(0.119528, 0.524298)], 15: [(0.098256, 0.717935)], 16: [(0.809295, 0.718312)], 23: [(0.146565, 0.079028)],
	33: [(0.842631, 0.500929)], 34: [(0.842631, 0.500929)], 35: [(0.851933, 0.04858)],
	45: [(0.6227, 0.854076)], 46: [(0.6227, 0.854076)], 47: [(0.286024, 0.85396)], 48: [(0.286024, 0.85396)],
}
SOLENOID_OBJECTS = {
	1: "Kicker BallRelease (the trough exit)", 2: "Plunger AutoPlunger",
	3: "Primitive DiverterPost (centre of its mesh's vertex bounds)", 4: "Kicker Kicker36",
	8: "Flipper BrontoDiverter", 9: "Wall RightSlingShot (mean of its drag points)", 10: "Wall LeftSlingShot (mean of its drag points)",
	11: "Bumper Sw63 (the top left jet)", 12: "Bumper Sw65 (the bottom jet)", 13: "Bumper Sw64 (the top right jet)",
	14: "Primitive Dictabird (centre of its mesh's vertex bounds)",
	15: "Primitive DiverterPostLeft (centre of its mesh's vertex bounds)", 16: "Primitive DiverterPostRight (centre of its mesh's vertex bounds)",
	23: "Trigger ttMachineTrigger (the cvpmTurnTable the script runs as the Boulder Machine)",
	33: "Flipper FlipperRight1", 34: "Flipper FlipperRight1", 35: "Gate Gate2",
	45: "Flipper FlipperRight", 46: "Flipper FlipperRight", 47: "Flipper FlipperLeft", 48: "Flipper FlipperLeft",
}
SOLENOID_PROJECTIONS = {
	5: "Projected to the mean of the three 3-bank drop targets (HitTarget Sw45-Sw47): the reset coil sits under the bank and the retained table models no coil object.",
	6: "Projected to the mean of the four 4-bank drop targets (HitTarget Sw41-Sw44): the reset coil sits under the bank and the retained table models no coil object.",
}

# --- Lamp matrix (manual printed 2-40, 3-4 and the front-matter copy) and lamp list (printed 2-41).
LAMP_LABELS = {
	11: "Top Rollover D", 12: "Top Rollover I", 13: "Top Rollover G", 14: "Mystery Mode", 15: "Fred's Choice",
	16: "Eat at Joe's Diner", 17: "Bedrock Water Buffalo", 18: "Dino Frenzy",
	21: "Upper 3-Bank Left Target", 22: "Upper 3-Bank Center Target", 23: "Upper 3-Bank Right Target",
	24: "Center Lane Extra Ball", 25: "Center Lane Search", 26: "Center Lane Drive Thru",
	27: "Left Inner Lane Super Jackpot", 28: "Left Inner Lane Playfield 2X",
	31: "Concrete C (First)", 32: "Concrete O", 33: "Concrete N", 34: "Concrete C (Second)", 35: "Concrete R",
	36: "Concrete E (First)", 37: "Concrete T", 38: "Concrete E (Second)",
	41: "Left & Right Drain Save", 42: "3-Bank Drop Target B", 43: "3-Bank Drop Target E", 44: "3-Bank Drop Target D",
	45: "4-Bank Drop Target R", 46: "4-Bank Drop Target O", 47: "4-Bank Drop Target C", 48: "4-Bank Drop Target K",
	51: "Left Bowling", 52: "Left & Right 3-Bank Upper Targets", 53: "Lower Left Frenzy", 54: "Lower Left Dino",
	55: "Left Combo 3", 56: "Left Combo 2", 57: "Left Combo 1", 58: "Lower Left Start Machine",
	61: "Lower Left Start Job Change", 62: "Lower Left Help", 63: "Left & Right 3-Bank Middle Targets",
	64: "Left & Right 3-Bank Lower Targets", 65: "Center Jackpot", 66: "Rock Again (Shoot Again)",
	67: "Left X on Left Ramp", 68: "Right X on Left Ramp",
	71: "Right Dino", 72: "Left & Right Machine Time", 73: "Right Combo 2", 74: "Right Combo 3", 75: "Right Combo 1",
	76: "Right Bowling", 77: "Right Frenzy", 78: "Right Search",
	81: "Upper Left Frenzy", 82: "Upper Left Dino", 83: "Left Lane Bronto Crane", 84: "Left Search",
	85: "Right Lane Job Change", 86: "Left & Right Start Multiball", 87: "Buy-In Button", 88: "Start Button",
}
ROM_LAMP_TEXT = {
	11: "<D>IG", 12: "D<I>G", 13: "DI<G>", 14: '"MYSTERY MODE"', 15: '"FREDS CHOICE"', 16: '"EAT AT JOES"',
	17: '"WATERBUFFALOS"', 18: '"DINO FRENZY"', 21: 'LEFT "/" TGT.', 22: 'CNTR. "X" TGT.', 23: 'RIGHT "/" TGT.',
	24: "EXTRA BALL", 25: "CENTER SEARCH", 26: "CNTR. DRIVE THRU", 27: '"SUPER JACKPOT"', 28: "START 2X",
	31: "<C>ONCRETE", 32: "C<O>NCRETE", 33: "CO<N>CRETE", 34: "CON<C>RETE", 35: "CONC<R>ETE", 36: "CONCR<E>TE",
	37: "CONCRE<T>E", 38: "CONCRET<E>", 41: '"DRAIN SAVE"', 42: "<B>EDROCK", 43: "B<E>DROCK", 44: "BE<D>ROCK",
	45: "BED<R>OCK", 46: "BEDR<O>CK", 47: "BEDRO<C>K", 48: "BEDROC<K>", 51: "LEFT BOWLING", 52: "BOTM. TGTS. 3",
	53: "LEFT FRENZY", 54: "LEFT DINO", 55: 'LEFT RAMP "3"', 56: 'LEFT RAMP "2"', 57: 'LEFT RAMP "1"', 58: "START MACHINE",
	61: "START JOB", 62: '"HELP"', 63: "BOTM. TGTS. 2", 64: "BOTM. TGTS. 1", 65: '"JACKPOT"', 66: '"ROCK AGAIN"',
	67: 'LEFT "X"', 68: 'RIGHT "X"', 71: "RIGHT DINO", 72: '"MACHINE TIME"', 73: 'RIGHT RAMP "2"', 74: 'RIGHT RAMP "3"',
	75: 'RIGHT RAMP "1"', 76: "RIGHT BOWLING", 77: "RIGHT FRENZY", 78: "RIGHT SEARCH", 81: "UP. LFT. FRENZY",
	82: "UP. LFT. DINO", 83: '"BRONTO CRANE"', 84: "LEFT SEARCH", 85: "JOB CHANGE", 86: "START MULTIBALL", 87: "BUY IN",
	88: "START BUTTON",
}
# address -> printed bulb(s); every other lamp is a single #555 (24-8768).
LAMP_BULBS = {
	31: "#44 (24-6549)", 38: "#44 (24-6549)", 65: "#44 (24-6549)", 66: "#44 (24-6549)",
	67: "#86 (24-8829)", 68: "#86 (24-8829)", 41: "#555 (24-8768) left and #44 (24-6549) right",
}
LAMP_ASSEMBLIES = {
	**{address: "A-17624" for address in (11, 12, 13)},
	**{address: "A-18555" for address in (14, 15, 16, 17, 18)},
	**{address: "A-18559" for address in (21, 22, 23, 24, 25, 26, 27, 28)},
	31: "A-17836", 38: "A-17836",
	**{address: "A-18558" for address in (32, 33, 34, 35, 36, 37)},
	41: "A-18561 (left) and A-17836 (right)",
	**{address: "A-18554" for address in (42, 43, 44)},
	**{address: "A-18556" for address in (45, 46, 47, 48)},
	**{address: "A-18561" for address in (51, 53, 54, 55, 56, 57, 58, 61, 62)},
	52: "A-18561 (left) and A-18553 (right)", 63: "A-18561 (left) and A-18553 (right)", 64: "A-18561 (left) and A-18553 (right)",
	65: "A-17835", 66: "A-17836", 67: "A-18499", 68: "A-18499",
	**{address: "A-18560" for address in (71, 73, 74, 75, 76, 77, 78)},
	72: "A-18557 (left) and A-18560 (right)",
	**{address: "A-18557" for address in (81, 82, 83, 84, 85)},
	86: "A-18557 (left) and A-18560 (right)",
	87: "20-9663-18", 88: "20-9663-14",
}
TWIN_BULB_LAMPS = {41, 52, 63, 64, 72, 86}
# The bulb light the script's Lamps collection binds for each lamp, beside the LTnn insert overlay (a classic light drawing
# g5k_insertsdim over the insert): an is_bulb_light Light without an image that shows no bulb mesh, so it marks no socket
# and the lamp is not placed (docs/SPATIAL.md, picking the bulb). Two-bulb lamps list (left, right).
TWIN_BULB_OBJECTS = {41: ("LT41d", "LT41c"), 52: ("LT52d", "LT52c"), 63: ("LT63d", "LT63c"), 64: ("LT64d", "LT64c"), 72: ("LT72c", "LT72d"), 86: ("LT86d", "LT86c")}


def lamp_bulb_objects(address: int) -> tuple[str, ...]:
	if address in TWIN_BULB_OBJECTS:
		return TWIN_BULB_OBJECTS[address]
	return (f"LT{address}",) if address in {67, 68} else (f"LT{address}a",)


LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J134-1", "Q90"), 2: ("Red-Black", "J134-2", "Q89"), 3: ("Red-Orange", "J134-4", "Q88"),
	4: ("Red-Yellow", "J134-5", "Q87"), 5: ("Red-Green", "J134-6", "Q86"), 6: ("Red-Blue", "J134-7", "Q85"),
	7: ("Red-Violet", "J134-8", "Q84"), 8: ("Red-Gray", "J134-9", "Q83"),
}
LAMP_CONNECTOR_NOTE = (
	" Connectors follow the lamp matrix, which all three printed copies print alike; the power driver board connector list "
	"(printed 3-31) instead puts the rows on J133 and the columns on J138 and marks J134 and J137 Not Used, with the same wire "
	"colours, and routes rows 6-8 and column 8 to the cabinet on J135-7/8/9 and J136-3."
)

# (label, 6.8Vac feed, feed wire, triac, switched return, return wire, printed lamps, printed table function)
GI_STRINGS = {
	0: ("Machine Lighting", "J121-7 (Playfield)", "White-Brown", "Q18", "J121-1 (Playfield)", "Brown", "#555 (24-8768)", "Machine Lighting"),
	1: ("Flintstones Logo", "J121-8 (Playfield) / J120-8 (Backbox)", "White-Orange", "Q10", "J121-2 (Playfield) / J120-2 (Backbox)", "Orange", "#44 playfield, #555 backbox", "Flintstones Logo"),
	2: ("Upper Playfield & Insert Panel", "J121-9 (Playfield) / J120-9 (Backbox)", "White-Yellow", "Q14", "J121-3 (Playfield) / J120-3 (Backbox)", "Yellow", "#44 playfield, #555 backbox", "Up Pfld & Insrt Pan."),
	3: ("Middle Playfield & Insert Panel", "J121-10 (Playfield) / J120-10 (Backbox)", "White-Green", "Q16", "J121-5 (Playfield) / J120-5 (Backbox)", "Green", "#44 playfield, #555 backbox", "Mid Pfld & Insrt Pan."),
	4: ("Lower Playfield & Insert Panel", "J121-11 (Playfield) / J119-1 (Cabinet)", "White-Violet", "Q12", "J121-6 (Playfield) / J119-3 (Cabinet)", "Violet", "#44 playfield", "Low Pfld & Insrt Pan"),
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _text_sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"The Flintstones retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained The Flintstones extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"The Flintstones retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"The Flintstones retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"The Flintstones retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "observed") -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": x,
				"y": y,
				"provenance": provenance(*source_refs, status=status),
			}
		)
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


RENDERER = "; rendered by tools/render_excerpt_image.py with PyMuPDF 1.26.3 and Pillow 12.3.0"
NATIVE = "scanned page rendered at its native resolution (embedded image xref {xref}, 2480px across 8.26in)"
# (excerpt id suffix, locator, image derivation or None); the transcription defaults to <suffix>.md.
MANUAL_EXCERPTS = (
	("switch-matrix", "PDF pages 107, 116 and 117, printed pages 2-42, 3-2 and 3-3: Switch Circuit, SWITCH CIRCUIT and DEDICATED SWITCHES", None),
	("switch-locations", "PDF page 108, printed page 2-43, Switch Locations list", None),
	(
		"switch-locations-drawing", "PDF page 108, printed page 2-43, Switch Locations drawing",
		f"{MANUAL_NAME} page 108, crop box 0.4,0.09,0.97,0.74, {NATIVE.format(xref=640)}, rendered at 149 dpi, capped to 700px wide, "
		"grayscale, 701x1129 WebP quality 60" + RENDERER,
	),
	("lamp-matrix", "PDF pages 105, 118 and 2, printed pages 2-40 and 3-4 and the front-matter copy: Lamp Circuit", None),
	("lamp-locations", "PDF page 106, printed page 2-41, Lamp Locations list", None),
	(
		"lamp-locations-drawing", "PDF page 106, printed page 2-41, Lamp Locations drawing",
		f"{MANUAL_NAME} page 106, crop box 0.4,0.09,0.94,0.63, {NATIVE.format(xref=628)}, rendered at 143 dpi, capped to 640px wide, "
		"grayscale, 641x906 WebP quality 60" + RENDERER,
	),
	("solenoid-flasher-table", "PDF pages 109 and 119, printed pages 2-44 and 3-5: Solenoid/Flashlamp Circuit with its General Illumination and Flipper Circuits blocks", None),
	("solenoid-flasher-locations", "PDF page 110, printed page 2-45, Solenoid/Flasher Locations list", None),
	(
		"solenoid-flasher-locations-drawing", "PDF page 110, printed page 2-45, Solenoid/Flasher Locations drawing",
		f"{MANUAL_NAME} page 110, crop box 0.42,0.09,0.985,0.71, {NATIVE.format(xref=652)}, rendered at 150 dpi, capped to 700px wide, "
		"grayscale, 701x1087 WebP quality 60" + RENDERER,
	),
	(
		"solenoid-wiring", "PDF page 120, printed page 3-6, SOLENOID WIRING",
		f"{MANUAL_NAME} page 120, crop box 0.07,0.05,0.99,0.92, {NATIVE.format(xref=712)}, rendered at 132 dpi, capped to 1000px wide, "
		"grayscale, 1001x1338 WebP quality 80" + RENDERER,
	),
	(
		"flashlamp-wiring", "PDF page 121, printed page 3-7, FLASHLAMP WIRING",
		f"{MANUAL_NAME} page 121, crop box 0.07,0.05,0.99,0.92, {NATIVE.format(xref=718)}, rendered at 132 dpi, capped to 1000px wide, "
		"grayscale, 1001x1338 WebP quality 80" + RENDERER,
	),
	("gi-circuit", "PDF page 124, printed page 3-10, GENERAL ILLUMINATION CIRCUIT and its block diagram", None),
	("flipper-circuits", "PDF pages 125-127, printed pages 3-11 to 3-13: FLIPPER CIRCUITS, FLIPPER COIL CIRCUIT and FLIPPER CABINET SWITCH CIRCUIT", None),
	("opto-boards", "PDF pages 134-136, printed pages 3-20 to 3-22: Outhole Trough Circuit and the A-13609 3-bank and A-19103 4-bank drop target boards", None),
	("boulder-machine-circuit", "PDF page 138, printed page 3-24: A-15542 Motor EMI Board Assembly and Boulder Machine Circuit Diagram", None),
	("power-driver-connectors", "PDF pages 143-145, printed pages 3-29 to 3-31: A-12697-3 Power Driver Board connector list", None),
	("mechanism-assemblies", "PDF pages 82, 85, 87-90 and 92-94, printed pages 2-17, 2-20, 2-22 to 2-25 and 2-27 to 2-29: assembly parts lists", None),
	("game-rules", "PDF pages 9-21, 40, 42 and 50-51: rules, shot maps, the T.14 Machine Test and T.15 Empty Balls Test, and feature adjustments", None),
)
# Several crops share one transcription.
EXCERPT_TRANSCRIPTIONS = {
	"switch-locations-drawing": "switch-locations.md",
	"lamp-locations-drawing": "lamp-locations.md",
	"solenoid-flasher-locations-drawing": "solenoid-flasher-locations.md",
}


def _excerpts(entries: tuple[tuple[str, str, str | None], ...]) -> list[dict[str, Any]]:
	records = []
	for suffix, locator, derivation in entries:
		transcription = EXCERPT_TRANSCRIPTIONS.get(suffix, f"{suffix}.md")
		record: dict[str, Any] = {
			"id": f"excerpt.the-flintstones.{suffix}",
			"locator": locator,
			"path": f"{EXCERPT_PREFIX}/{transcription}",
			"sha256": _text_sha256(EXCERPT_DIRECTORY / transcription),
		}
		if derivation is not None:
			record["image"] = f"{EXCERPT_PREFIX}/{suffix}.webp"
			record["image_sha256"] = _file_sha256(EXCERPT_DIRECTORY / f"{suffix}.webp")
			record["image_derivation"] = derivation
		record.update({"method": "manual", "transcribed_by": "curator, read from the native-resolution render", "reviewed": True})
		records.append(record)
	return records


def _bulletin_excerpt(suffix: str, locator: str) -> list[dict[str, Any]]:
	return [
		{
			"id": f"excerpt.the-flintstones.{suffix}",
			"locator": locator,
			"path": f"{EXCERPT_PREFIX}/service-bulletins.md",
			"sha256": _text_sha256(EXCERPT_DIRECTORY / "service-bulletins.md"),
			"method": "manual",
			"transcribed_by": "curator, read from the page render",
			"reviewed": True,
		}
	]


def _bulletin(identifier: str, filename: str, capture: str, sha256: str, acquired_at: str, locator: str, excerpt: tuple[str, str]) -> dict[str, Any]:
	return {
		"id": identifier,
		"kind": "service_bulletin",
		"uri": f"{WAYBACK_PREFIX}{capture}id_/{IPDB_FILES}{filename}",
		"original_filename": filename,
		"sha256": sha256,
		"acquired_at": acquired_at,
		"locator": locator,
		"license": "NOASSERTION",
		"attribution": "Williams Electronics Games, Inc.; hosted by the Internet Pinball Machine Database, retrieved from the Internet Archive's Wayback Machine",
		"rights": "NOASSERTION",
		"excerpts": _bulletin_excerpt(*excerpt),
	}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames records for fs_lx5 and its nine clones fs_dx5, fs_lx2, fs_dx2, fs_lx3, fs_sp2, fs_sp2d, fs_lx4, fs_dx4 and fs_la5",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/fs.c: CORE_GAMEDEF(fs,lx5) and CORE_CLONEDEF(fs,dx5/lx2/dx2/lx3/sp2/sp2d/lx4/dx4/la5), all with "
				"wpc_mSecurityS; WPC_ROMSTART members flin_lx5/dx5/la5/lx2/dx2/lx3/lx4/dx4.rom (fs_sp2 and fs_sp2d reuse flin_lx5.rom and "
				"flin_dx5.rom with FS_P2_SOUND's su2-sp2.rom, and fs_sp2 is commented '// Prototype Sound ??'); fsGameData GEN_WPCSECURITY "
				"with wpc_dispDMD, FLIP_SW(FLIP_L | FLIP_UR) | FLIP_SOL(FLIP_L | FLIP_UR), the inverted-switch mask {0x00, 0x00, 0x00, "
				"0x3f, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00} and the special switches {swStart, swTilt, swSlamTilt, "
				"swCoinDoor, swLaunch}; init_fs only sets core_gameData, so there is no mechanics handler, no custom solenoid and no "
				"wpc_set_fastflip_addr call. The *** PRELIMINARY *** simulator's #define block (swTroughJam 31, swTrough1-4 32-35, "
				"swLeftJet 63, swRightJet 64, swBottomJet 65, sLeftJet 11, sBottomJet 12, sRightJet 13) is cross-reference only. "
				"src/wpc/wpc.c: the fs_ output typing marks 17-22 and 24-28 as #89 20V DC bulbs. src/wpc/core.c: core_getSol (29-31 "
				"J111/game-on remap, 33/34 the synthesized upper-right flipper because FLIP_SOL covers FLIP_UR, 35/36 the raw upper-left "
				"Fliptronic bits, 37-44 zero outside WPC-95/System 11, 45-48 lower flippers) and core_updateSw's flipper mask (the EOS "
				"bits 111, 113 and 115 recomputed from the coils, the button bits carried through when keyboard handling is off)."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-security.json",
			"revision": "repository",
			"locator": "WPC-Security public switch, DIP, solenoid, lamp and five-string G.I. address rules",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": f"{WAYBACK_PREFIX}20260117015226id_/{IPDB_FILES}{MANUAL_NAME}",
			"original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-30T23:49:19Z",
			"locator": (
				"150-page image-only Williams The Flintstones Operations Manual 16-50029-101 (July 1994), IPDB machine 888 "
				"(https://www.ipdb.org/machine.cgi?id=888: Williams 'The Flintstones', July 1994, model 50029, MPU Williams WPC Security "
				"(WPC-S), 4,779 units, three flippers, automatic plunger). The PDF is IPDB's English manual file, retrieved from its Wayback "
				"Machine capture because IPDB is Cloudflare-gated. Scanned at 300 dpi; Section 2 PDF page = printed page + 65. Used: rules "
				"and shot maps (PDF 9-21), the T.14/T.15 tests (PDF 40), adjustments (PDF 42, 50-51), assembly parts lists (PDF 82-94), "
				"the lamp, switch and solenoid tables, lists and drawings (PDF 105-110, with the front-matter lamp chart on PDF 2), the "
				"circuit pages printed 3-2 to 3-13 (PDF 116-127), the opto boards (PDF 134-136), the Boulder Machine circuit (PDF 138) "
				"and the power driver board connector list (PDF 143-145). A local Windows.Media.Ocr text layer (external:pinmame-manuals/"
				"by-machine/williams.the-flintstones.1994/ipdb-888/ocr-windows) was used only to find pages; every cited cell was read "
				"from the render."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Pinball Machine Database, retrieved from the Internet Archive's Wayback Machine",
			"rights": "NOASSERTION",
			"excerpts": _excerpts(MANUAL_EXCERPTS),
		},
		_bulletin(
			HANGUP_SOURCE, "Williams_1994_The_Flintstones_Ball_Hang_up_Correction_Instructions_August_4_1994.pdf", "20251101130318",
			HANGUP_SHA256, "2026-10-30T23:49:29Z",
			"Ball Hang-up Correction Instructions 16-9872, August 4, 1994, one page: remove the washers on the posts at both sides of "
			"the bottom arch (03-9068) to stop balls hanging up there.",
			("service-bulletins", "Ball Hang-up Correction Instructions 16-9872, quoted in full"),
		),
		_bulletin(
			AMENDMENT_SOURCE, "Williams_1994_The_Flintstones_Manual_Amendment_Page_2_24_Correction_August_10_1994.pdf", "20260201074105",
			AMENDMENT_SHA256, "2026-10-30T23:49:21Z",
			"Manual Amendment 16-9876, August 10, 1994, one page: the A-17932 Diverter Assembly drawing on printed page 2-24 calls out "
			"the bell armature A-17986 as item 9 instead of item 6.",
			("manual-amendment", "Manual Amendment 16-9876, quoted in full with its parts list"),
		),
		{
			"id": ROM_SOURCE,
			"kind": "rom_static_analysis",
			"uri": "external:pinmame-review-artifacts/the-flintstones-1994/rom-name-tables.json",
			"revision": "flin_lx5.rom",
			"locator": (
				"The English switch, Fliptronic switch, coil, flasher, G.I. and lamp name tables of the game ROM of fs_lx5, fs_lx4, fs_lx2 "
				"and fs_sp2 in the local corpus, decoded by tools/flintstones_rom_name_tables.py: each table is located by its sentinel, "
				"count and English anchor entries, and every English copy must decode identically. The four sets decode identically "
				f"(fs_lx5 archive SHA-256 {ROM_ARCHIVE_SHA256}); the decoded JSON is retained beside the ROM member SHA-256s listed in "
				"the excerpt."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games program ROMs, user-authorized local copies; ROM bytes are not redistributed",
			"acquired_at": "2026-10-31T00:10:05Z",
			"excerpts": [
				{
					"id": "excerpt.the-flintstones.rom-name-tables",
					"locator": "Six English name tables of flin_lx5.rom, with the offsets of every English copy and the per-set hashes",
					"path": f"{EXCERPT_PREFIX}/rom-name-tables.md",
					"sha256": _text_sha256(EXCERPT_DIRECTORY / "rom-name-tables.md"),
					"method": "mixed",
					"transcribed_by": "tools/flintstones_rom_name_tables.py, reviewed by curator",
					"reviewed": True,
				}
			],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/the-flintstones-1994/source/The Flintstones (Williams 1994) v1.25.7.vpx",
			"original_filename": "The Flintstones (Williams 1994) v1.25.7.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working The Flintstones v1.25.7 (203,587,584 bytes; g5k, 3rdAxis and DJRobX, October 2019). Exact "
				f"playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority for named table "
				"objects only. Primitive placements use the centre of the mesh's vertex bounds (world x = pos.x + size.x * vx, "
				"y = pos.y - size.y * vy for these X-rotated meshes). Its flasher lights Fl17-Fl28 and full-playfield FlPf overlays "
				"paint light and are not sockets, and neither its LTnn insert overlays nor the bulb-mode lamp lights beside them, which "
				"show no bulb mesh, mark a lamp socket."
			),
			"license": "NOASSERTION",
			"attribution": "g5k, 3rdAxis and DJRobX",
			"rights": "NOASSERTION",
			"acquired_at": "2026-10-30T23:50:33Z",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/the-flintstones-1994/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Embedded script of the retained table (66,332 bytes): cGameName = "fs_lx5", UseSolenoids = 2, UseLamps = 0, UseGI = 1, '
				'UseVPMModSol = 1, LoadVPM "01560000", "WPC.VBS", 3.26; writes switches 22 and 24 closed at start; vpmNudge.TiltSwitch '
				"14; cvpmTrough bsTrough InitSwitches 32-35 with exit BallRelease; cvpmSaucer bsKicker36 on Kicker36 (switch 36); "
				"cvpmDropTarget dtLeftDrop (sw45-sw47 to 45-47) and dtRightDrop (sw41-sw44 to 44-41); cvpmTurnTable ttMachine on "
				"ttMachineTrigger; SolCallback for 1-10, 14-16, 23, 35, 36 and the lower flippers, SolModCallback for 17-22, 24, 25 "
				"and 28, empty callbacks for 26 and 27; InitLamps binds every light of its Lamps collection to the lamp numbered by "
				"the two digits after 'LT' in its name; UpdateGI dispatches string 0 to the Boulder Machine's lighting and string 2 "
				"to the playfield G.I. and implements no other string."
			),
			"license": "NOASSERTION",
			"attribution": "g5k, 3rdAxis and DJRobX",
			"rights": "NOASSERTION",
			"acquired_at": "2026-10-30T23:50:40Z",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/the-flintstones-1994/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
				f"bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
			"acquired_at": "2026-10-30T23:57:13Z",
		},
		{
			"id": CORPUS_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/{quote(CORPUS_SCRIPT_NAME, safe='/')}",
			"revision": VPXTABLE_SCRIPTS_REVISION,
			"sha256": CORPUS_SCRIPT_SHA256,
			"locator": (
				'The Flintstones (Williams 1994) v1.25.8.vbs (65,857 bytes), the next release of the same table: cGameName = "fs_lx5", '
				"the same solenoid, trough, popper, drop-target and turntable setup. Same lineage, so it corroborates the bindings but "
				"is not independent evidence. Script only; its table is not retained."
			),
			"license": "NOASSERTION",
			"attribution": "g5k, 3rdAxis and DJRobX; corpus by sverrewl",
			"rights": "NOASSERTION",
		},
	]


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability,
		"provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_component = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC-Security CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_component}; row receiver {return_component}",
	}


def _switch_notes(address: int, column: int, row: int) -> str:
	notes = (
		f"Printed switch-matrix drive column {column}, return row {row}, cell '{PRINTED_SWITCH_TEXT[address]}'; ROM switch-test "
		f"text '{ROM_SWITCH_TEXT[address]}'."
	)
	if row == 5:
		notes += (
			" Both copies of the matrix print the row-5 header J209-4, the same pin as row 4; the outhole trough block diagram "
			"(printed 3-20) and the drop-target board pages put row 5 on J209-5, which is recorded."
		)
	if address in OPTO_SWITCHES:
		notes += (
			" Neither copy of the matrix shades a cell or prints an opto legend. The manual's board pages construct this switch as a "
			"beam the ball or target breaks, which makes the switch read as made (printed 3-20 to 3-22), so the contact the matrix sees "
			"rests closed. Pinned PinMAME's fsGameData inverted-switch mask normalizes this address, so the public state is already "
			"normalized and must not be inverted again."
		)
	if address in {31, 32, 33, 34, 35}:
		notes += (
			" One of the LED/phototransistor pairs of the A-18753 outhole trough (Trough 7 IR LED and photo transistor boards on the "
			"A-15576 7-opto switch board, column 3 rows 1-5). The printed matrix and switch list name 31-34 'Trough #1-#4' and 35 "
			"'Trough Jam'; the ROM's switch table, pinned fs.c's simulator defines and the retained script (InitSwitches 32-35) all "
			"put Trough Jam on 31 and Trough 1-4 on 32-35, which is recorded."
		)
		if address == 31:
			notes += " The retained script's SolRelease pulses 31 on every trough eject, a table stand-in rather than a jam."
		if address == 32:
			notes += " Trough 1 is the ball at the eject end (the first entry of the script's InitSwitches)."
	if address == 36:
		notes += (
			" The popper opto rides the same 7-opto switch board (row 6, its gray-blue and orange-blue wires go to the ball popper). "
			"The switch list prints A-16908 LED with A-16909 transistor. The A-15769-1 Ball Popper & Opto Assembly list names an "
			"A-15914 LED Assembly and an 03-8561 Photo Transistor Assembly, and prints A-16909 and A-16908 beside a bracket and a "
			"screw description, so its part numbers and descriptions are misaligned. Part numbers only; the switch list is recorded."
		)
	if address in {41, 42, 43, 44}:
		notes += (
			" Opto on the A-19103 4-bank drop target board, read through the A-18188 4-Bank Drop Target Assembly. The printed "
			"matrix numbers the bank '#1-#4'; the ROM names 41-44 BED<R>OCK to BEDROC<K>, and the 4-bank lamps 45-48 carry the same "
			"letters R-O-C-K from the rear left to the front right."
		)
	if address in {45, 46, 47}:
		notes += (
			" Opto on the A-13609 3-bank drop target board of the A-16032-1 3-Bank Drop Target Assembly. The printed matrix numbers "
			"the bank '#1-#3'; the ROM names 45-47 BE<D>ROCK, B<E>DROCK and <B>EDROCK, so 47 (B) is the rear target and 45 (D) the "
			"front one, like the 3-bank lamps 42 (B) to 44 (D)."
		)
	if address in TWIN_TARGET_SWITCHES:
		position = {51: "upper", 52: "middle", 53: "lower"}[address]
		notes += (
			f" Two standup targets wired to one address: the {position} target of the left side 3-bank and the {position} target of "
			"the right side 3-bank. The printed matrix and switch list put the bottom targets on 51 and the upper ones on 53; the ROM "
			"names 51 'LFT. RGHT. TGT. 3' and 53 'TGT. 1' to match lamps 52 'BOTM. TGTS. 3' (the upper inserts) and 64 'BOTM. TGTS. 1' "
			"(the lower ones), and the retained script's targets put 51 at the top of each bank, which is recorded."
		)
	if address in {16, 17, 18}:
		notes += (
			" One of the three bowling targets of the Bowl-O-Rama bank at the upper left (the matrix prints '/', 'X' and '/' as 'I', "
			"'X' and 'I'). The switch list prints item 18 twice, for the center and right targets, and no item 17; both rows carry "
			"A-18606-7."
		)
	if address == 12:
		notes += (
			" Ticket dispenser input; the switch list prints it 'Not Used' with no part and no drawing callout. Column 1's inversion "
			"mask byte is 0x00, so the ROM reads the matrix contact directly; no dispenser is fitted as built."
		)
	if address == 24:
		notes += (
			" Physical part 5643-09112-00 is a permanently closed link that proves the matrix is connected; pinned PinMAME sets it "
			"closed at machine start and the retained script also writes it closed."
		)
	if address == 22:
		notes += " Closed while the coin door is closed; the retained script writes it closed at start."
	if address == 11:
		notes += (
			" Cabinet Launch button that fires the autoplunger (solenoid 2). Adjustment A.2 17 Flipper Plunger lets the right flipper "
			"button launch the ball when this button is broken."
		)
	if address == 23:
		notes += " Cabinet buy-in button (lamp 87 lights it); the retained script writes it from its front key."
	if address in {61, 62}:
		notes += " The slingshot kick switch (SW-1A-114) and the separate score switch (SW-1A-120) share this address."
	if address in {63, 64, 65}:
		notes += " Jet bumper skirt switch (SW-11A-37)."
	if address == 25:
		notes += (
			" The Boulder Machine's exit switch: the A-17978 bracket assembly lists an A-19098 Ball Popper Exit Sw. Assembly with "
			"its H-19142 exit switch cable."
		)
	if address == 76:
		notes += " The ROM names it MACHINE ENTER: the upper right lane runs across the top of the playfield into the Boulder Machine."
	if address == 56:
		notes += " The target at the Dicta-Bird on the left side (A-18607-6)."
	if address in SWITCH_PROJECTIONS:
		notes += " " + SWITCH_PROJECTIONS[address]
	elif address in SWITCH_OBJECTS:
		notes += f" Placement: retained table object {SWITCH_OBJECTS[address]}."
	return notes


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		dedicated_note = f"Printed dedicated grounded switch D{address}. {note}"
		if address == 5:
			dedicated_note += " The 2-42 copy's J205 pin is blurred; the 3-2 and 3-3 copies print J205-6."
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address,
				"optional" if address == 4 else "used", (MANUAL_SOURCE, ROM_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": dedicated_note},
				wiring={"board": "WPC-Security CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	cabinet_roles = {
		11: "cabinet.launch", 12: "cabinet.ticket", 13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt",
		22: "cabinet.coin-door", 23: "cabinet.buy-in",
	}
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"switch.matrix-{address}"
			physical: dict[str, Any] = {}
			if address in SWITCH_PARTS:
				physical["part_number"] = SWITCH_PARTS[address]
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if address in UNUSED_MATRIX_ADDRESSES:
				physical["notes"] = (
					f"Printed switch-matrix drive column {column}, return row {row}: 'Not Used' on the matrix and in the switch list, "
					"and the ROM's switch table names it NOT USED."
				)
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, ROM_SOURCE)
				items.append(_device(identifier, f"Not Used Matrix Position {address}", "switch", "pinmame.input.switch", address, "unused", (MANUAL_SOURCE, ROM_SOURCE, CONTROLLER_SOURCE), **extra))
				continue
			label = SWITCH_LABELS[address]
			physical["notes"] = _switch_notes(address, column, row)
			refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if address == 24:
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE, CORE_SOURCE)
				items.append(_device(identifier, label, "constant", "pinmame.input.switch", address, "used", (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE), **extra))
				continue
			# On the WPC matrix row read the CPU sees swMatrix directly, so a switch inside the inversion
			# mask that the ROM treats as active at public 1 has a matrix contact that rests closed.
			extra["normally_closed"] = address in OPTO_SWITCHES
			if address in PULSED_SWITCHES:
				extra["pulse"] = True
			availability = "used"
			if address in cabinet_roles:
				extra["roles"] = [cabinet_roles[address]]
				physical["location"] = "cabinet" if address in {11, 12, 13, 23} else "cabinet interior"
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				if address == 22:
					extra["initial_active"] = True
				if address == 12:
					availability = "optional"
					physical["location"] = "cabinet (optional ticket dispenser, not fitted as built)"
					refs = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE)
			else:
				coordinate_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) if address in SWITCH_PROJECTIONS or address in {41, 42, 43, 44} else (VPX_TABLE_SOURCE,)
				extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	for address, (label, role, switch_type, part, wire, connection, printed, rom) in FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		notes = (
			f"Printed Fliptronic grounded switch {position} '{printed}' ({wire}, {connection}); switch-locations part {part}; ROM "
			f"Fliptronic switch text '{rom}'."
		)
		if switch_type == "opto":
			notes += (
				" Cabinet flipper opto (A-17316 flipper opto board). On this generation PinMAME's WPC_FLIPPERS register read returns "
				"the complement of the whole Fliptronic column, so the public state is already normalized (1 = button pressed) and must "
				"not be inverted again. With keyboard handling off (LibPinMAME) the host's value is carried through unchanged."
			)
			if address in {112, 116}:
				notes += (
					" The right cabinet button's opto board breaks both F2 and F6 (FLIPPER CABINET SWITCH CIRCUIT, printed 3-13), so one "
					"press drives the lower and upper right flippers together and a host drives 112 and 116 together."
				)
			if address == 112:
				notes += (
					" The FLIPPER CIRCUITS (printed 3-11) and cabinet switch pages print F2 Black-Yellow and F6 Blue-Violet, the reverse "
					"of the matrix; the matrix colours are recorded."
				)
			if address == 114:
				notes += " The 2-42 matrix copy prints its connector J906-2; the 3-2 copy and the flipper pages print J905-2, which is recorded."
		else:
			notes += (
				" Plain end-of-stroke leaf switch (SW-1A-194) on the flipper assembly. fsGameData declares FLIP_SOL(FLIP_L | FLIP_UR), "
				"so core_updateSw recomputes this bit from the flipper coil every update; a host must not drive it."
			)
		items.append(
			_device(
				f"switch.generic-{address}", label, "switch", "pinmame.input.switch", address, "used",
				(MANUAL_SOURCE, ROM_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": position},
				],
				roles=[role],
				normally_closed=False,
				physical={
					"location": "cabinet flipper button" if switch_type == "opto" else "flipper assembly",
					"switch_type": switch_type,
					"part_number": part,
					"notes": notes,
				},
				wiring={"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service" if switch_type == "opto" else "internal_nonvisual", MANUAL_SOURCE),
			)
		)
	for address, (wire, connection, printed) in UNUSED_FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		items.append(
			_device(
				f"switch.generic-{address}", f"Not Used Fliptronic Position {position}", "switch",
				"pinmame.input.switch", address, "unused", (MANUAL_SOURCE, ROM_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": position},
				],
				physical={
					"location": "not installed",
					"notes": (
						f"Printed Fliptronic grounded switch {position} '{printed}' ({wire}, {connection}); the switch-locations list "
						f"prints {position} 'Not Used' and the ROM's Fliptronic switch table leaves it empty. The Flintstones has no "
						"upper left flipper; its upper-left Fliptronic circuit drives the up/down gates."
					),
				},
				spatial=not_applicable("unused", MANUAL_SOURCE),
			)
		)

	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country configuration bit)", "dip_switch",
				"pinmame.input.dip", address, "used", (CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC-Security CPU board",
					"switch_type": "dip",
					"notes": f"CPU-board country DIP SW{address}; the WPC-Security controller profile defines the eight country bits.",
				},
				spatial=not_applicable("dip_switch", CORE_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	slug = label.lower().replace("&", "and")
	for character in (" ", "/"):
		slug = slug.replace(character, "-")
	for character in ("(", ")", chr(39), "."):
		slug = slug.replace(character, "")
	return f"device.{slug}"


def _rom_coil_note(address: int) -> str:
	if address in ROM_COIL_ENTRY:
		return f" ROM coil-test entry {ROM_COIL_ENTRY[address]} '{ROM_COIL_TEXT[address]}'."
	if address in ROM_FLASHER_ENTRY:
		return f" ROM flasher-test entry {ROM_FLASHER_ENTRY[address]} '{ROM_COIL_TEXT[address]}'."
	return ""


def _solenoid_notes(address: int, printed_type: str) -> str:
	printed_number = PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")
	notes = f"Printed solenoid/flasher table entry {printed_number} ({printed_type})"
	if address in PRINTED_SOLENOID_TEXT:
		notes += f" '{PRINTED_SOLENOID_TEXT[address]}'"
	notes += "." + _rom_coil_note(address)
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
	if address in {11, 12, 13}:
		notes += (
			" The retained script binds no callback; the table's bumper physics fire on contact and pulse the switch. The printed "
			"table names 11-13 Left, Middle and Right; the ROM's coil test names them TOP LEFT JET, BOTTOM JET and TOP RIGHT JET, and "
			"pinned fs.c's simulator pairs sLeftJet 11, sBottomJet 12 and sRightJet 13 with switches 63, 65 and 64."
		)
	if address == 1:
		notes += " Kicks the ball from the Trough 1 position into the shooter lane."
	if address == 2:
		notes += (
			" A-14525 kicker bracket at the foot of the shooter lane, fired from the cabinet Launch button (11) or automatically after "
			"adjustment A.2 05 Seconds Before Autofire."
		)
	if address == 3:
		notes += (
			" A-17932 Diverter Assembly: a post on a bell armature (A-17986, the part Manual Amendment 16-9876 re-numbers on the "
			"assembly drawing) at the rear beside the popper."
		)
	if address == 4:
		notes += " A-15769-1 Ball Popper & Opto Assembly at the rear left; the ROM calls it TOP POPPER."
	if address == 5:
		notes += " The solenoid/flasher location list prints assembly A-18825; the assembly page for the coil's bank is A-16032-1, which is recorded."
	if address == 6:
		notes += " The solenoid/flasher location list prints assembly A-18812; the assembly page for the coil's bank is A-18188, which is recorded."
	if address == 7:
		notes += " Printed with backbox voltage (J107-2) and drive (J130-8) connections; the location drawing gives it no callout."
	if address == 8:
		notes += (
			" A-18369 Diverter Assembly (back diverter 01-12803) on the A-18823 Back Panel Assembly, with the 03-9131 back panel "
			"diverter guide; the ROM calls it BACKPANEL DIVRTR."
		)
	if address == 14:
		notes += " A-18078 Diverter Assembly with the A-18079 Dicta-Bird perch mounting bracket; the coil moves the Dicta-Bird figure."
	if address in {15, 16}:
		notes += (
			" A-19097 Diverter Assembly (bell armature A-19096) at the top of the outlane and return lane divider, just below the "
			"Drain Save lamp (41). The ROM's coil test calls it a ramp diverter."
		)
	if address == 23:
		notes += (
			" Not a coil: the 14-7999 motor of the A-17978 Boulder Machine bracket assembly, fed +12V from J118-2 through the "
			"A-15542 Motor EMI board (J1-1 Gray-Yellow +12V, J1-3 Blue-Violet solenoid drive #23 from J126-7; printed 3-24). The "
			"board's connector list names the J2-1 motor wire White while the circuit diagram on the same page labels it BLK. The "
			"T.14 Machine Test turns the motor on."
		)
	if address in {33, 34}:
		notes += (
			" The upper right flipper (A-15849-R-2, FL-11629 blue coil) on the Fliptronic upper-right circuit. fsGameData sets "
			"FLIP_SOL(FLIP_UR), so core_getSol publishes 33 as the power winding alone and 34 as power OR hold, like the lower flippers."
		)
	if address in {35, 36}:
		side = "Right" if address == 35 else "Left"
		notes += (
			f" The {side.lower()} up/down gate (A-17796 Ball Gate Actuator, A-14406 coil) on the {'power' if address == 35 else 'hold'} "
			"transistor of the Fliptronic upper-left circuit (J907-8). FLIP_SOL does not cover FLIP_UL, so core_getSol publishes the "
			"raw Fliptronic bit here. The note under the 3-5 copy of the table says 'IN THIS GAME, THE UPPER RIGHT FLIPPER CIRCUIT IS "
			"USED TO DRIVE THE LEFT & RIGHT UP/DOWN GATES', but the table itself, the FLIPPER CIRCUITS page (printed 3-11) and the "
			"upper right flipper's own rows put the gates on the upper-left circuit, which is recorded."
		)
		if address == 36:
			notes += (
				" No coordinate is recorded: the solenoid/flasher location drawing's callout 36 ends at the rear left beside the "
				"Boulder Machine (about x 0.21, y 0.02 by eye), while the retained script binds 36 to Gate4 at (0.516, 0.022) beside "
				"the gate flap GateFlapLeft, about 0.3 of the table width away."
			)
		else:
			notes += " The location drawing's callout 35 ends at the upper right, where the retained table's Gate2 stands."
	if address in {45, 46, 47, 48}:
		notes += (
			f" Printed flipper circuit {printed_number}; PinMAME publishes the lower flippers at 45-48, odd addresses the power winding "
			"alone and even addresses power OR hold. FL-11629 blue coils."
		)
	if address in {33, 34, 45, 46}:
		notes += (
			" The FLIPPER COIL CIRCUIT schematic (printed 3-12) draws its right flipper with the left circuit's J902 pins 9, 7, 3 and "
			"1; the solenoid table and the FLIPPER CIRCUITS page (printed 3-11) give J902-13/11 for the lower right and J902-6/4 for "
			"the upper right, which is recorded."
		)
	if address in SOLENOID_PROJECTIONS:
		notes += " " + SOLENOID_PROJECTIONS[address]
	elif address in SOLENOID_OBJECTS:
		notes += f" Placement: retained table object {SOLENOID_OBJECTS[address]}."
	return notes


def _flasher_notes(address: int, printed_type: str) -> str:
	lamps = SOLENOID_WIRING[address][5]
	notes = (
		f"Printed solenoid/flasher table entry {address:02d} ({printed_type}) '{PRINTED_SOLENOID_TEXT[address]}', flashlamps {lamps}."
		+ _rom_coil_note(address)
	)
	if address in {17, 18, 19, 20, 21}:
		notes += (
			" The same output also lights two #906 backbox insert flashers (the table's backbox column '#906 (2)' and the location "
			"list's 'Insert Flasher #906' continuation line); quantity counts the playfield and the backbox bulbs, and only the "
			"playfield ones have a location."
		)
	if address == 17:
		notes += " The table types it 'Low Power' while its neighbours print 'Flasher'; its #89 lamp is a flasher like theirs."
	if address == 20:
		notes += (
			" The location list calls it 'Popper Wire Rmp Fls.' and the location drawing calls out 20 twice, at the lower left and the "
			"lower right; the ROM calls it BTM. 3 BNK. FLS."
		)
	if address == 22:
		notes += " One #89 (A-17803) and one #906 (A-17802) playfield flasher on one output."
	if address == 24:
		notes += (
			" The location list prints flasher assembly A-17983; the A-17978 Boulder Machine bracket assembly also lists an A-11541 "
			"socket and bulb and an H-18219-3 flasher cable."
		)
	if address == 28:
		notes += (
			" The flashlamp wiring page (printed 3-7) draws its BLU-YEL drive on J122-2, while both copies of the table print J122-4, "
			"which is recorded."
		)
	if address in BACKBOX_FLASHERS:
		notes += " Backbox-only flasher (three #906 behind the backglass); the location drawing gives it no callout."
	if address == 26:
		notes += (
			" The power driver board connector list (printed 3-30) labels its Blue-Red J124-2 'sol. 25 drive to backbox playfield'; "
			"solenoid 25 is the playfield flasher on J122-1 in the same list, and the table, the wire colour and the 'sol. 27' line on "
			"J124-3 make J124-2 this output's, which is recorded."
		)
	notes += (
		" Pinned wpc.c types the fs_ outputs 17-22 and 24-28 as #89 20V DC bulbs for its brightness model; the printed lamp types "
		"are recorded."
	)
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
	if address not in BACKBOX_FLASHERS:
		notes += (
			" No coordinate is recorded: the retained table drives light objects (Fl17-Fl28 and full-playfield FlPf overlays) that "
			"paint light rather than mark sockets, and no socket was measured on the location drawing."
		)
	return notes


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_WIRING[address]
			if address in FLASHERS:
				kind = "flasher"
			elif address == 23:
				kind = "motor"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			if kind != "flasher":
				physical["part_number"] = part
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if kind == "flasher":
				if address in FLASHER_QUANTITY:
					physical["quantity"] = FLASHER_QUANTITY[address]
				physical["notes"] = _flasher_notes(address, printed_type)
			else:
				physical["notes"] = _solenoid_notes(address, printed_type)
			wiring: dict[str, Any] = {
				"board": "Fliptronic II board" if address in PRINTED_FLIPPER_CIRCUITS else "WPC-Security power driver board",
				"driver_transistor": transistor,
				"power_connection": voltage,
				"control_connection": drive,
				"control_wire": wire,
			}
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")}]
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address == 3:
				refs = refs + (AMENDMENT_SOURCE,)
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in BACKBOX_FLASHERS:
				extra["roles"] = ["cabinet.backbox-flasher"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif kind == "flasher" or address == 36:
				pass
			else:
				coordinate_refs: tuple[str, ...] = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) if address in SOLENOID_PROJECTIONS else (VPX_TABLE_SOURCE,)
				extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		used = address in {29, 30, 31}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; not a The Flintstones playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a The Flintstones playfield device.",
			31: "PinMAME publishes WPC_GILAMPS bit 7 here as the Game-On / flipper-enable state because fs.c configures no fast-flip address.",
			32: "PinMAME reports this WPC state channel as always zero; fsGameData declares no use for it.",
			49: "PinMAME's simulator-only ball-shooter channel; The Flintstones' autoplunger is solenoid 2 and has no output here.",
			50: "Reserved PinMAME output position before the first custom-output boundary; fsGameData declares no custom solenoids.",
		}.get(address, "Unused WPC-Security output: this generation has no LPDC board, so core_getSol returns constant 0 for 37-44 outside WPC-95 and System 11.")
		if address in PRINTED_UNUSED_OUTPUTS:
			transistor, wire = PRINTED_UNUSED_OUTPUTS[address]
			notes += (
				f" The solenoid table prints '{address}* Not Used', Low Power, with transistor {transistor} and drive wire {wire} but "
				"no voltage connection, drive connection or part; the 3-5 copy's footnote reads 'JX-X =8-DRIVER BOARD'."
			)
			if address == 41:
				notes += " The wire reads 'Grn-Wht' on the 2-44 copy and 'Gm-Wht' on the sharper 3-5 copy."
		roles = ["internal.wpc-state"] if used else ["internal.unused.wpc-output"]
		refs = (CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE) if address in PRINTED_UNUSED_OUTPUTS else (CONTROLLER_SOURCE, CORE_SOURCE)
		items.append(
			_device(
				output_id(label), label, "virtual", "pinmame.output.solenoid", address, "used" if used else "unused",
				refs,
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=roles,
				physical={"notes": notes},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			wiring = {
				"board": "WPC-Security power driver board",
				"drive_wire": drive_wire,
				"drive_connection": drive_connection,
				"return_wire": return_wire,
				"return_connection": return_connection,
				"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
			}
			aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]
			physical: dict[str, Any] = {"assembly_part_number": LAMP_ASSEMBLIES[address]}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}; ROM lamp-test text '{ROM_LAMP_TEXT[address]}'." + LAMP_CONNECTOR_NOTE
			if column == 4:
				notes += (
					" All three copies of the matrix print column 4's connector J137-5, the same pin as column 5; the connector list "
					"puts the Yellow-Black column 4 wire on pin 4 of the column header, which is recorded."
				)
			refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			extra: dict[str, Any] = {"aliases": aliases, "wiring": wiring, "physical": physical}
			if address in {87, 88}:
				notes += (
					" Lamp inside the illuminated cabinet button; the lamp-locations list prints its bulb number '-----' and the drawing "
					"puts its callout below the cabinet outline."
				)
				extra["roles"] = ["cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE)
			else:
				physical["quantity"] = 2 if address in TWIN_BULB_LAMPS else 1
				notes += f" Printed bulb {LAMP_BULBS.get(address, '#555 (24-8768)')}."
				if address in TWIN_BULB_LAMPS:
					left, right = TWIN_BULB_OBJECTS[address]
					notes += (
						" Two sockets on one address: the lamp list prints a second, unnumbered row for the right-hand bulb and the "
						f"drawing calls the number out twice. The retained table binds the bulb lights {left} (left) and {right} "
						"(right), which show no bulb mesh, so they mark no socket and the lamp is not placed."
					)
				else:
					notes += (
						f" The retained table binds the bulb light {lamp_bulb_objects(address)[0]}, which shows no bulb mesh, so it "
						"marks no socket and the lamp is not placed."
					)
				if address in {31, 34}:
					notes += " One of the two C inserts of the CONCRETE row; the ROM numbers the letters left to right."
				if address in {36, 38}:
					notes += " One of the two E inserts of the CONCRETE row; the ROM numbers the letters left to right."
				if address == 66:
					notes += " The matrix prints 'Shoot Again'; the lamp list and the ROM call it Rock Again."
			physical["notes"] = notes
			items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, feed, feed_wire, transistor, switched_return, return_wire, bulbs, printed) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = (
			f"Printed general-illumination string {address + 1:02d} '{printed}'; printed lamps {bulbs}; ROM G.I. test text "
			f"'ILLUM. STRING {address + 1}'. The triac switches the return pin and the 6.8Vac feed is the power connection (G.I. "
			"circuit, printed 3-10; connector list, printed 3-30). The solenoid table prints the return pins under its 'Voltage "
			"Connections' columns and the feeds under the drive columns."
		)
		if address in {1, 2, 3}:
			notes += " The connector list (printed 3-30) confirms the split: J121 pins go to the playfield and J120 pins to the backbox."
		if address == 0:
			notes += (
				" Recorded as a playfield string from the power driver board connector list (printed 3-30), which runs J121-7 White-"
				"Brown and J121-1 Brown to the playfield and marks J120-1 and J120-7 N/C; the retained script's UpdateGI dispatches "
				"this string to the Boulder Machine's lighting on the playfield, as its name says. The solenoid table instead prints "
				"backbox J120-1/J120-7 and a #555 backbox lamp type with no playfield connection."
			)
		if address == 4:
			notes += (
				" Recorded from the solenoid table, which gives lower playfield J121-6/J121-11 and cabinet J119-3/J119-1 connections and "
				"a #44 playfield lamp type, as the string's name says. The connector list (printed 3-30) instead marks J121-6 and J121-11 "
				"N/C and runs this string's White-Violet/Violet pair to the backbox on J120-11/J120-6 and to the Coin Door Board on "
				"J119-1/J119-3. The board list alone disagrees with the table's location and bulb columns and the string name, so the "
				"table is recorded; the retained script implements no case for this string."
			)
		notes += (
			" No coordinate is recorded: the manual prints no per-string socket list and the retained table places no G.I. bulb per "
			"string."
		)
		items.append(
			_device(
				identifier, label, "gi", "pinmame.output.gi", address, "used",
				(MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE) if address in {0, 2} else (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{address + 1:02d}"}],
				wiring={
					"board": "WPC-Security power driver board", "power_connection": feed, "power_wire": feed_wire,
					"driver_transistor": transistor, "control_connection": switched_return, "control_wire": return_wire,
				},
				physical={"notes": notes},
			)
		)
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
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[tuple[str, str, list[str], str]], *refs: str, assembly_part_number: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [{"id": pid, "label": plabel, "sensors": psensors, "description": pdesc} for pid, plabel, psensors, pdesc in positions]
		return record

	return [
		mechanism(
			"mechanism.trough", "Four-ball trough", "kicker", [output_id("Ball Trough")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest in the A-18753 outhole trough on the optos 32 (Trough 1, at the eject end) to 35 (Trough 4); 31 (Trough "
			"Jam) is a fifth LED/phototransistor pair. The pairs sit on the Trough 7 IR LED and photo transistor boards, wired through "
			"the A-15576 7-opto switch board (column 3, rows 1-5); a ball breaks the beam and the switch reads made, and PinMAME "
			"normalizes all five. Solenoid 1 (AE-26-1500) kicks the ball on 32 into the shooter lane. The retained script holds the "
			"balls in a cvpmTrough, exits them at BallRelease and pulses 31 with every eject. The T.15 Empty Balls Test clears every "
			"ball from the trough and the lock-up devices.",
			[
				("ball-1", "Trough 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough 4", ["switch.matrix-35"], "Fourth trough position."),
				("jam", "Trough Jam", ["switch.matrix-31"], "Jam opto of the trough."),
			],
			MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18753",
		),
		mechanism(
			"mechanism.autoplunger", "Shooter lane and autoplunger", "kicker", [output_id("Ball Shooter")],
			["switch.matrix-15", "switch.matrix-11"],
			"A ball served from the trough rests on Shooter Lane (15). The ROM fires solenoid 2 (A-14525 kicker bracket, AE-23-800) to "
			"launch it when the player presses the cabinet Launch button (11), or automatically after adjustment A.2 05 Seconds Before "
			"Autofire (printed range 10-40 seconds, factory default printed 50). Adjustment A.2 17 Flipper Plunger lets the right "
			"flipper button launch the ball when the launch button is broken. There is no manual plunger; the retained script fires "
			"its plunger AutoPlunger.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-15"], "Shooter lane rollover.")],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-14525",
		),
		mechanism(
			"mechanism.top-popper", "Top popper", "kicker", [output_id("Top Popper")], ["switch.matrix-36"],
			"A ball entering the popper at the rear left is seen by its opto (36, on the trough's 7-opto switch board) and popped up "
			"by solenoid 4 (AE-23-800) of the A-15769-1 Ball Popper & Opto Assembly. Per the shot maps, the upper lanes feed the "
			"popper when MACHINE TIME, START MULTI-BALL or BRONTO CRANE is lit. The retained script ejects it with a cvpmSaucer on "
			"Kicker36 under the comment 'Bronto/Machine VUK'.",
			[("ball", "Ball in the popper", ["switch.matrix-36"], "Popper opto.")],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-15769-1",
		),
		mechanism(
			"mechanism.boulder-machine", "Boulder Machine", "motorized", [output_id("Boulder Machine Motor")],
			["switch.matrix-76", "switch.matrix-25"],
			"A-17978 bracket assembly in the upper left corner, mounted on the A-18823 back panel: the A-18135 wheel turned by the "
			"14-7999 motor (solenoid 23, fed +12V through the A-15542 Motor EMI board), the A-18566 ramp, an A-11541 socket and bulb "
			"with its flasher cable beside the Boulder Machine Flasher (24), and the A-19098 ball popper exit switch (25). A ball reaches it from the upper right lane past Machine Enter (76, the "
			"ROM's MACHINE ENTER) and leaves past Machine Exit (25). The rules call it the Rock Slicer Machine: shooting the lit "
			"Dicta-Bird target starts its MACHINE TIME scoring round. The T.14 Machine Test runs the motor ('running' or 'off'). The "
			"retained script runs it as a clockwise cvpmTurnTable on ttMachineTrigger and briefly blocks the exit at some wheel "
			"angles to keep the ball spinning; wheel speed and timing are table-owned. G.I. string 1 (Machine Lighting) lights it.",
			[
				("enter", "Ball entering", ["switch.matrix-76"], "Machine Enter rollover at the end of the upper right lane."),
				("exit", "Ball leaving", ["switch.matrix-25"], "Machine Exit switch."),
			],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-17978",
		),
		mechanism(
			"mechanism.three-bank-drop-targets", "B-E-D 3-bank drop targets", "drop_target_bank",
			[output_id("3-Bank Drop Reset")], ["switch.matrix-45", "switch.matrix-46", "switch.matrix-47"],
			"A-16032-1 3-bank drop target assembly on the left: three targets B (47, rear), E (46) and D (45, front), each read by an "
			"opto on the A-13609 drop target board, which PinMAME normalizes; solenoid 5 (AE-26-1200) raises all three through the "
			"reset plate. The rules: completing B-E-D adds a CONCRETE letter, BEDROCK WATER BUFFALOS scores flashing targets, and "
			"completing both banks during the BEDROCK mystery mode awards 100 million.",
			[
				("b", "B down", ["switch.matrix-47"], "Rear target."),
				("e", "E down", ["switch.matrix-46"], "Middle target."),
				("d", "D down", ["switch.matrix-45"], "Front target."),
			],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-16032-1",
		),
		mechanism(
			"mechanism.four-bank-drop-targets", "R-O-C-K 4-bank drop targets", "drop_target_bank",
			[output_id("4-Bank Drop Reset")], ["switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-44"],
			"A-18188 4-bank drop target assembly in the centre, angled from the rear left to the front right: R (41), O (42), C (43) "
			"and K (44), each read by an opto on the A-19103 drop target board, which PinMAME normalizes; solenoid 6 (AE-24-900) "
			"raises the bank through its A-13453 reset plate. Completing R-O-C-K adds a CONCRETE letter.",
			[
				("r", "R down", ["switch.matrix-41"], "Rear left target."),
				("o", "O down", ["switch.matrix-42"], "Second target."),
				("c", "C down", ["switch.matrix-43"], "Third target."),
				("k", "K down", ["switch.matrix-44"], "Front right target."),
			],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18188",
		),
		mechanism(
			"mechanism.top-diverter-post", "Top diverter post", "diverter", [output_id("Top Diverter Post")], [],
			"A-17932 Diverter Assembly: an AE-27-1200 coil lifting a post on the A-17986 bell armature at the rear, beside the popper. "
			"No switch senses it. The retained script makes its DiverterPost collidable only while the coil is on.",
			[],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, AMENDMENT_SOURCE, assembly_part_number="A-17932",
		),
		mechanism(
			"mechanism.back-panel-diverter", "Back panel diverter", "diverter", [output_id("Top Diverter")], [],
			"A-18369 Diverter Assembly (back diverter 01-12803 on the A-18368 bell armature, AE-27-1200 coil) on the A-18823 Back "
			"Panel Assembly, which also carries the 03-9131 back panel diverter guide, the ball-gate bracket and the Boulder Machine. "
			"The ROM calls it BACKPANEL DIVRTR. No switch senses it. The retained script swings a flipper object, BrontoDiverter, to "
			"its end while the coil is on.",
			[],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18369",
		),
		mechanism(
			"mechanism.dicta-bird", "Dicta-Bird", "toy", [output_id("Dicta-Bird")], ["switch.matrix-56"],
			"A-18078 Diverter Assembly on the left side: an AE-28-1500 coil and A-6306-2 bell armature under the A-18079 Dicta-Bird "
			"perch mounting bracket, beside the Dicta-Bird target (56). Per the shot maps, the lit target starts MACHINE TIME, lights "
			"BARNEY'S JOB CHANGE or starts SEARCH AND RESCUE. The retained script animates the figure by tilting its Dictabird "
			"primitive while the coil is on; the figure's travel is table-owned.",
			[],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18078",
		),
		mechanism(
			"mechanism.lower-diverters", "Lower left and right diverters (drain save)", "diverter",
			[output_id("Lower Left Diverter"), output_id("Lower Right Diverter")], [],
			"A-19097-2 (left) and A-19097-1 (right) Diverter Assemblies (AE-27-1200, A-19096 bell armature) at the top of the outlane "
			"and return lane dividers, just below the Drain Save lamps (41). The rules: completing either side 3-bank lights DRAIN SAVE "
			"for a timed period (adjustment A.2 10, factory 5 seconds). The ROM's coil test calls them L. RMP. DIVERTER and R. RMP. "
			"DIVERTER. No switch senses them. While each coil is on the retained script moves its post and makes its diverter "
			"primitive non-collidable.",
			[],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-19097-1",
		),
		mechanism(
			"mechanism.up-down-gates", "Left and right up/down gates", "gate",
			[output_id("Right Up/Down Gate"), output_id("Left Up/Down Gate")], [],
			"Two A-17796 Ball Gate Actuator Assemblies (A-14406 coil, A-11146 armature, A-6892 frame and eyelet) at the rear, on the "
			"Fliptronic upper-left circuit: the right gate on its power transistor (35) and the left gate on its hold transistor (36). "
			"No switch senses either gate. The retained script makes its Gate2 (right) and Gate4 (left) non-collidable while the coil "
			"is on, so the ball passes.",
			[],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="A-17796",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other",
			[output_id("Left Jet Bumper"), output_id("Middle Jet Bumper"), output_id("Right Jet Bumper")],
			["switch.matrix-63", "switch.matrix-64", "switch.matrix-65"],
			"Three A-9415-2 jet bumpers (AE-26-1200) below the D-I-G rollovers: the top left jet (coil 11, switch 63), the bottom jet "
			"(coil 12, switch 65) and the top right jet (coil 13, switch 64), as the ROM's coil and switch tables and pinned fs.c's "
			"simulator pair them.",
			[
				("top-left", "Top left jet", ["switch.matrix-63"], "Table object Sw63."),
				("bottom", "Bottom jet", ["switch.matrix-65"], "Table object Sw65."),
				("top-right", "Top right jet", ["switch.matrix-64"], "Table object Sw64."),
			],
			MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-61", "switch.matrix-62"],
			"B-9362-L-2 (left, coil 10) and B-9362-R-3 (right, coil 9) slingshot assemblies (AE-26-1200); each carries a kick switch "
			"(SW-1A-114) and a score switch (SW-1A-120) on one address.",
			[("left", "Left slingshot", ["switch.matrix-61"], "Left slingshot."), ("right", "Right slingshot", ["switch.matrix-62"], "Right slingshot.")],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.flippers", "Three flippers", "other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"), output_id("Lower Left Flipper Power"),
				output_id("Lower Left Flipper Hold"), output_id("Upper Right Flipper Power"), output_id("Upper Right Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114", "switch.generic-115", "switch.generic-116"],
			"Lower right and upper right (A-15849-R-2) and lower left (A-15849-L-2) Fliptronic flippers with FL-11629 blue coils and "
			"separate power and hold windings, each with an end-of-stroke leaf switch (111, 113, 115). The left cabinet button's opto "
			"is 114; the right cabinet button's opto board breaks both 112 and 116, so it fires the lower and upper right flippers "
			"together. The ROM energizes both windings on the button and drops the power winding when the end-of-stroke closes. The "
			"retained script's SolRFlipper swings both right flippers.",
			[
				("lower-right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112, EOS 111."),
				("lower-left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114, EOS 113."),
				("upper-right", "Upper right flipper", ["switch.generic-115", "switch.generic-116"], "Button opto 116, EOS 115."),
			],
			MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Knocker", "other", [output_id("Knocker")], [],
			"Solenoid 7 fires the B-10686-1 knocker (AE-23-800), wired through the backbox connections and not drawn on the playfield.",
			[],
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="B-10686-1",
		),
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
			"id": "williams.the-flintstones.1994",
			"name": "The Flintstones",
			"manufacturer": "Williams",
			"year": 1994,
			"kind": "physical_pinball",
			"model_number": "50029",
			"ipdb_id": 888,
			"opdb_id": "GRK95-MQ674",
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-security",
			"hardware_generation": "0x20",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": [],
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"The Flintstones device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	observed_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device["spatial"]
		address = int(device["binding"]["device"])
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
			continue
		placement_count += len(spatial["placements"])
		(observed_inputs if spatial["status"] == "observed" else located_inputs).append(address)
	located_outputs: list[dict[str, Any]] = []
	observed_outputs: list[dict[str, Any]] = []
	unplaced_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unplaced_outputs.append(binding)
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
			continue
		placement_count += len(spatial["placements"])
		(observed_outputs if spatial["status"] == "observed" else located_outputs).append(binding)
	order = lambda item: (item["group"], item["address"])  # noqa: E731
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "observed",
		"blockers": [
			"Every placement comes from one community table's named objects and none was checked against the manual's switch, lamp "
			"or solenoid location drawings, so all of them stay observed. Promotion needs a callout check of those drawings.",
			"Lamps 11-86 have no coordinate: the retained table draws each insert with a classic LTnn overlay and binds a bulb-mode "
			"light beside it (LTnna, LTnnc/LTnnd, LT67, LT68) that shows no bulb mesh, so neither marks a socket. Placing them needs "
			"a reproducible measurement on the lamp location drawing or a table that models the insert bulbs.",
			"Flashers 17-22, 24, 25 and 28 have no coordinate: the retained table drives light objects (Fl17-Fl28 and full-playfield "
			"FlPf overlays) that paint light rather than mark sockets, and no socket was measured on the location drawing.",
			"The Left Up/Down Gate (36) has no coordinate: the location drawing's callout 36 ends at the rear left beside the Boulder "
			"Machine, about 0.3 of the table width from the Gate4 the retained script binds it to.",
			"G.I. strings 1-5 have no coordinate: the manual prints no per-string socket list and the retained table places no G.I. "
			"bulb per string.",
			"The trough optos (31-35) are projected onto the trough exit and the drop-target reset coils (5, 6) onto the mean of "
			"their bank's targets; the table models none of them.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 964.0, "bottom": 2162.0},
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/the-flintstones-1994/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"observed_input_addresses": sorted(observed_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=order),
		"observed_output_bindings": sorted(observed_outputs, key=order),
		"unplaced_output_bindings": sorted(unplaced_outputs, key=order),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=order) for reason, bindings in sorted(not_applicable_outputs.items())},
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [{"group": "pinmame.output.solenoid", "address": address, "reason": reason} for address, reason in sorted(SOLENOID_PROJECTIONS.items())],
		"coordinate_origins": {
			"drag_point_means": ["Wall LeftSlingShot (switch 61, solenoid 10)", "Wall RightSlingShot (switch 62, solenoid 9)"],
			"mesh_bounds_centres": ["Primitive DiverterPost (solenoid 3)", "Primitive Dictabird (solenoid 14)", "Primitive DiverterPostLeft (solenoid 15)", "Primitive DiverterPostRight (solenoid 16)"],
			"object_centers": "every other table placement uses its retained object's own center",
		},
		"excluded_object_classes": [
			"Flasher lights Fl17-Fl28 and the full-playfield FlPf17-FlPf28 overlays, which paint flasher light and are not sockets.",
			"Baked primitives whose object origin is not a device position (origins at 0,0 or outside the playfield); the four "
			"primitives above are placed at their mesh's vertex bounds instead.",
			"The insert overlays LTnn (single-bulb lamps) and LTnna/LTnnb (two-bulb lamps): classic lights that draw the insert "
			"image over the insert's outline. The bulb-mode lights the script binds beside them (LTnna, LTnnc/LTnnd, LT67, LT68) "
			"show no bulb mesh, so they mark no socket either. The LT11b-LT13b Flasher ambience sprites lie off the playfield.",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# The Flintstones (Williams, 1994) spatial review",
		"",
		f"Status: {report['status']}. Every switch, coil and motor that has a playfield location is placed from the retained "
		"table or carries a controlled `not_applicable` record, except the left up/down gate; the playfield lamps, the playfield "
		"flashers and the G.I. strings have no coordinate. No placement was checked against the manual's location drawings, so every placement "
		"stays `observed` and the record stays at `machines/partial/williams/the-flintstones-1994.json`.",
		"",
		f"The geometry source is the retained known-working `The Flintstones (Williams 1994) v1.25.7.vpx` (SHA-256 "
		f"`{TABLE_SHA256}`); its embedded script (SHA-256 `{SCRIPT_SHA256}`) is the runtime binding authority. Exact playfield "
		f"bounds are `{TABLE_BOUNDS}`; every table coordinate is x/964 and y/2162 rounded to six places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime authority; the July 1994 operations manual and its two bulletins are the physical "
		"inventory, construction and wiring authority; the game ROM's own name tables settle the semantic names where the printed "
		"tables disagree; pinned PinMAME owns controller topology; the retained table supplies geometry for named objects.",
		"- The script's InitLamps binds each light of its Lamps collection by the two digits of its name (LTnn), so every lamp "
		"note names its objects. Neither the LTnn insert overlay nor the bulb-mode light beside it (is_bulb_light, no image, no "
		"bulb mesh) marks a socket, so no lamp is placed.",
		"- The trough optos, the drop-target reset coils and the two right flippers' shared button are documented in the "
		"definition's device notes.",
		"- Flashers 17-21 also light #906 backbox insert flashers, and 26/27 are backbox-only; G.I. strings 2-4 also feed #555 "
		"backbox bulbs. None of those is placed.",
		"",
		"## Blockers",
		"",
	]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Explicit projections", ""]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Validated input addresses: {len(report['resolved_input_addresses'])}",
		f"- Observed-only input addresses: {len(report['observed_input_addresses'])}",
		f"- Validated output bindings: {len(report['resolved_output_bindings'])}",
		f"- Observed-only output bindings: {len(report['observed_output_bindings'])}",
		f"- Output bindings with no coordinate: {len(report['unplaced_output_bindings'])}",
	]
	lines += [f"- Inputs with a controlled `{reason}` record: {len(addresses)}" for reason, addresses in report["not_applicable_inputs"].items()]
	lines += [f"- Outputs with a controlled `{reason}` record: {len(bindings)}" for reason, bindings in report["not_applicable_outputs"].items()]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Refused. `coverage.missing` is `[\"spatial_placement\"]`: every coordinate rests on one community table without a drawing "
		"check, and the playfield flashers, the left up/down gate and the five G.I. strings are not placed at all.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Operations manual SHA-256 `{MANUAL_SHA256}`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError("Stale The Flintstones author-ready definition is still present")
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"The Flintstones artifact is missing: {path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"The Flintstones definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"The Flintstones seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"The Flintstones spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"The Flintstones spatial review drifted from its deterministic curator: {markdown_path}")
	print("The Flintstones definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, seed and spatial audit")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		print(f"The Flintstones extraction manifest written: {write_extraction_manifest(root)}")
	elif args.verify_extraction:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		verify_extraction_manifest(root)
		print("The Flintstones retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
