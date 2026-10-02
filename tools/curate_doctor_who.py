"""Curate the physical Bally Doctor Who (1992) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and
runtime-derived fact as a literal and reads two committed seeds for the placements (the table-derived
coordinates and the factory-drawing callout check), so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots.  ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the definition, its knowledge note and its spatial report.
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

MACHINE_ID = "bally.doctor-who.1992"
PARTIAL_PATH = ROOT / "machines/partial/bally/doctor-who-1992.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/doctor-who-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/doctor-who-1992.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/bally/doctor-who-1992.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/bally/doctor-who-1992-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/bally/doctor-who-1992-callouts.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools/seeds/bally/doctor-who-1992-legacy-aliases.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/doctor-who-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/doctor-who-1992.md"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = "pinmame.catalog.8371478a7640"
CORE_SOURCE = "pinmame.core.8371478a7640"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
IDENTITY_SOURCE = "identity.bally.doctor-who.1992"
MANUAL_SOURCE = "manual.bally.doctor-who.1992"
HANDY_SOURCE = "manual-chart.bally.doctor-who.1992"
AMENDMENT_SOURCE = "manual-amendment.bally.doctor-who.1992"
VPX_TABLE_SOURCE = "vpx-table.dw-vpw-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.dw-vpw-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.dw-vpw-1-1"
EDGES_SOURCE = "runtime.doctor-who.switch-edges"
SOLENOID_TEST_SOURCE = "runtime.doctor-who.solenoid-test"
FLASHER_TEST_SOURCE = "runtime.doctor-who.dw-l2.flasher-test"
MINI_PLAYFIELD_SOURCE = "runtime.doctor-who.mini-playfield-test"
CALLOUT_SOURCE = "drawing-callouts.doctor-who.2026-10-02"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-fliptronic"
RUNTIME_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"

TABLE_SHA256 = "99e92c977f98bfc129bfa3ab63fdfe803d37d0033198b475d518eb387f89a503"
SCRIPT_SHA256 = "6c31324ab557a70e4caa1920c6f4be3b96c4d97d7306bf96243584f80518e232"
MANUAL_SHA256 = "2f430808b59050a5814f3c1671c6de1a993cabc6b0366810f73e3dc2995f9235"
HANDY_SHA256 = "92798a56f1ef8693abfbf7361b31bdce78efc50f9cccdd956880a6a733c8f3bd"
AMENDMENT_SHA256 = "a702e82da3dcb98f0f16b6915dfc831a1c2b00af5056178f31c2e2a67e0dbcfd"
IPDB_PAGE_SHA256 = "64ba9ebc27162cb5bdab94f103a6cf479c22f7dfa013cf783234b9af35b57621"
PLAYFIELD_WIDTH = 952.965
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=952.965 bottom=2162"

EXTRACTION_FILE_COUNT = 1888
EXTRACTION_TOTAL_BYTES = 189042710
EXTRACTION_MANIFEST_SHA256 = "ea94e6d690dc96a37a0a05091147eda8824189cc51ea0346072a9e7d03149550"
EXTRACTION_RELATIVE_PATH = Path("bally/doctor-who-1992/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/doctor-who-1992/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / "evidence/excerpts/bally.doctor-who.1992"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("dw_l2", "dw_d2", "dw_l1", "dw_d1", "dw_p5", "dw_p6")
DRIVER_COMPATIBILITY = {
	"dw_l2": (
		"identical",
		"Production L-2 game ROM (November 1992) shipped with the physical machine; the retained known-working "
		'VPW Mod v1.1 table binds this driver directly (Const cGameName = "dw_l2"), and the runtime runs '
		"behind this definition booted it.",
	),
	"dw_d2": (
		"identical",
		"Community 'LED Ghost Fix' revision of the L-2 ROM for the same physical machine; pinned driver.c describes the fix "
		"as the 1995-era lamp-matrix driver timing correction against LED ghosting, and it changes no controller address or playfield device.",
	),
	"dw_l1": (
		"identical",
		"Production L-1 game ROM (October 1992), the first production firmware revision of the same physical "
		"machine; it runs on the same wpc_mFliptronS hardware with the same I/O.",
	),
	"dw_d1": (
		"identical",
		"Community 'LED Ghost Fix' revision of the L-1 ROM for the same physical machine, with no hardware or "
		"address change.",
	),
	"dw_p5": (
		"compatible",
		"P-5 prototype game ROM for pre-production machines; pinned dw.c pairs it with the prototype U18 sound ROM dw_u18.p4 "
		"(IPDB lists it with an L-2 sound ROM, and a dw.c comment notes an L-2 sound ROM found on a machine carrying the P-5 game ROM). It runs "
		"on the same WPC-Fliptronic controller generation. IPDB records that the sample and early prototype "
		"machines carried a motor-driven Dalek head with a front-facing opto that production machines dropped "
		"while leaving 'the wiring and software' in place; no retained source says which addresses that "
		"prototype-only hardware used, so a prototype ROM may drive hardware this production definition does "
		"not declare.",
	),
	"dw_p6": (
		"compatible",
		"P-6 prototype game ROM with the LED Ghost Fix applied, for pre-production machines; see dw_p5 for the "
		"prototype-only Dalek-head motor and opto that this production definition does not declare.",
	),
}

# --- Switch data (switch-locations.md, switch-matrix.md, handy-technician-chart.md) --------------------
# address -> (switch number cell, assembly cell, description), as printed on the Switch Locations page.
SWITCH_LOCATIONS = {
	13: ("---", "20-9663-1", "Start Button"),
	14: ("---", "20-6502-A", "Plumb Bob Tilt"),
	15: ("SW-1A-114", "B-8284-1", "Left Sling"),
	16: ("SW-1A-114", "B-8284-1", "Right Sling"),
	17: ("5647-12693-04", "A-11619", "Shooter Lane"),
	18: ("5647-12693-21", "A-12688-1", "Exit Jets"),
	21: ("---", "27-1066", "Slam Tilt"),
	22: ("---", "A-8630", "Coin Door closed"),
	24: ("---", "A-8630", "Always Closed"),
	25: ("5647-12693-08", "A-11680", "Trough 1 Ball"),
	26: ("5647-09957-00", "B-8925", "Trough 2 Balls"),
	27: ("5647-09957-00", "B-8925", "Trough 3 Balls"),
	28: ("5647-12133-12", "A-10417", "Outhole"),
	31: ("A-14231 (LED) / A-14232 (Trans)", "A-15440", "Opto Popper"),
	32: ("A-14231 (LED) / A-14232 (Trans)", "A-15634", "Mini-ply Home Opto"),
	33: ("A-14231 (LED) / A-14232 (Trans)", "A-15436", "Enter Top Ramp Opto"),
	34: ("---", "A-15896", "Launch Ball"),
	35: ("5647-12693-21", "A-15436", "Score Top Ramp"),
	36: ("5647-12693-11", "A-15904", "Enter Bottom Ramp"),
	37: ("5647-12693-21", "A-15690", "Score Bottom Ramp"),
	38: ("5647-12693-13", "A-12238", "Mini-ply Door, Middle"),
	41: ("---", "A-15631-4", "(E)-S-C-A-P-E"),
	42: ("---", "A-15631-4", "E-(S)-C-A-P-E"),
	43: ("---", "A-15631-4", "E-S-(C)-A-P-E"),
	44: ("---", "A-15631-4", "E-S-C-(A)-P-E"),
	45: ("---", "A-15631-4", "E-S-C-A-(P)-E"),
	46: ("---", "A-15631-4", "E-S-C-A-P-(E)"),
	47: ("5647-12693-19", "A-12688", "Hang On Score"),
	48: ("5647-12693-19", "A-12688-1", "Select Doctor"),
	51: ("SW-1A-178-4", "A-15439", "(R)-E-P-A-I-R"),
	52: ("SW-1A-178-4", "A-15439", "R-(E)-P-A-I-R"),
	53: ("SW-1A-178-4", "A-15439", "R-E-(P)-A-I-R"),
	54: ("SW-1A-178-4", "A-15439", "R-E-P-(A)-I-R"),
	55: ("SW-1A-178-4", "A-15439", "R-E-P-A-(I)-R"),
	56: ("SW-1A-178-4", "A-15439", "R-E-P-A-I-(R)"),
	57: ("5647-12693-36", "A-15477", "Trap Door Down"),
	58: ("---", "A-15862", "Transmat Award"),
	61: ("SW-11A-37", "B-12030-2", "Left Jet"),
	62: ("SW-11A-37", "B-12030-2", "Right Jet"),
	63: ("SW-11A-37", "B-12030-2", "Bottom Jet"),
	64: ("5647-12693-19", "A-26888", "Left Drain"),
	65: ("5647-12693-19", "A-26888", "Left Return"),
	66: ("5647-12693-19", "A-26888", "Right Return"),
	67: ("5647-12693-19", "A-26888", "Right Drain"),
	68: ("5647-12693-13", "A-12238", "Mini-ply Door, Left"),
	71: ("---", "A-15431 (Trans) & A-15432 (LED)", "Mini-ply Opto 5-Bank Right 1"),
	72: ("---", "A-15431 (Trans) & A-15432 (LED)", "Mini-ply Opto 5-Bank Right 2"),
	73: ("---", "A-15431 (Trans) & A-15432 (LED)", "Mini-ply Opto 5-Bank Middle"),
	74: ("---", "A-15431 (Trans) & A-15432 (LED)", "Mini-ply Opto 5-Bank Left 2"),
	75: ("---", "A-15431 (Trans) & A-15432 (LED)", "Mini-ply Opto 5-Bank Left 1"),
	76: ("---", "A-14231 (LED) & A-14232 (Trans)", "Mini-ply Left Opto Eject"),
	77: ("---", "A-14231 (LED) & A-14232 (Trans)", "Mini-ply Right Opto Eject"),
	78: ("---", "A-15903", "Mini-ply Target"),
	82: ("5647-12693-11", "A-15877", "Playfield Glass"),
	88: ("5647-12693-13", "A-12238", "Mini-ply Door, Right"),
}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 81, 83, 84, 85, 86, 87}
# Device labels (the manual's own wording, with the ROM's T.1 name where the harness run printed one).
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt", 15: "Left Slingshot Kick Switch", 16: "Right Slingshot Kick Switch",
	17: "Shooter Lane", 18: "Exit Jets", 21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed",
	25: "Trough 1 Ball", 26: "Trough 2 Balls", 27: "Trough 3 Balls", 28: "Outhole",
	31: "Opto Popper (Tardis)", 32: "Mini-playfield Home Opto", 33: "Enter Top Ramp Opto", 34: "Launch Ball Button",
	35: "Score Top Ramp", 36: "Enter Bottom Ramp", 37: "Score Bottom Ramp", 38: "Mini-playfield Door, Middle",
	41: "ESCAPE Target E", 42: "ESCAPE Target S", 43: "ESCAPE Target C", 44: "ESCAPE Target A", 45: "ESCAPE Target P",
	46: "ESCAPE Target E (last)",
	47: "Hang On Score", 48: "Select Doctor",
	51: "REPAIR Target R", 52: "REPAIR Target E", 53: "REPAIR Target P", 54: "REPAIR Target A", 55: "REPAIR Target I",
	56: "REPAIR Target R (last)",
	57: "Trap Door Down", 58: "Transmat Award Target", 61: "Left Jet Bumper", 62: "Right Jet Bumper",
	63: "Bottom Jet Bumper", 64: "Left Drain", 65: "Left Return", 66: "Right Return", 67: "Right Drain",
	68: "Mini-playfield Door, Left", 71: "Mini-playfield Opto 5-Bank Right 1", 72: "Mini-playfield Opto 5-Bank Right 2",
	73: "Mini-playfield Opto 5-Bank Middle", 74: "Mini-playfield Opto 5-Bank Left 2",
	75: "Mini-playfield Opto 5-Bank Left 1", 76: "Mini-playfield Left Opto Eject", 77: "Mini-playfield Right Opto Eject",
	78: "Mini-playfield Target (Lites Lock)", 82: "Playfield Glass", 88: "Mini-playfield Door, Right",
}
SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "leaf", 16: "leaf", 17: "microswitch", 18: "microswitch", 21: "tilt",
	22: "microswitch", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "button", 35: "microswitch", 36: "microswitch", 37: "microswitch",
	38: "microswitch", 41: "unknown", 42: "unknown", 43: "unknown", 44: "unknown", 45: "unknown", 46: "unknown",
	47: "microswitch", 48: "microswitch", 51: "other", 52: "other", 53: "other", 54: "other", 55: "other",
	56: "other", 57: "microswitch", 58: "unknown", 61: "leaf", 62: "leaf", 63: "leaf", 64: "microswitch",
	65: "microswitch", 66: "microswitch", 67: "microswitch", 68: "microswitch", 71: "opto", 72: "opto",
	73: "opto", 74: "opto", 75: "opto", 76: "opto", 77: "opto", 78: "unknown", 82: "microswitch", 88: "microswitch",
}
SWITCH_ROLES = {
	13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door",
	34: "cabinet.launch", 82: "cabinet.playfield-glass",
}
# The ten optos on the Opto Switch 10 PCB: public address -> board connector and wires (manual 3-12).
OPTO_BOARD_CONNECTORS = {
	31: "J6 (transmitter Gray/Black, receiver White/Green)",
	32: "J5 (transmitter Gray-Yellow/Black, receiver White/Green)",
	33: "J4 (transmitter Gray/Black, receiver White/Green)",
	71: "J1-3 transmitter Gray-Green, J2-3 receiver Orange-Green",
	72: "J1-4 transmitter Gray-Yellow, J2-4 receiver Orange-Yellow",
	73: "J1-5 transmitter Gray-Orange, J2-5 receiver Orange-Black",
	74: "J1-6 transmitter Gray-Red, J2-7 receiver Orange-Red",
	75: "J1-7 transmitter Gray-Brown, J2-8 receiver Orange-Brown",
	76: "J1-2 transmitter Gray-Blue, J2-2 receiver Orange-Blue",
	77: "J1-1 transmitter Gray-Violet, J2-1 receiver Orange-Violet",
}
# PinMAME dwGameData invSw {0x00,0x00,0x00,0x07,0x00,0x00,0x00,0x7f,0x01,...} mapped through wpc_sw2m
# (core_setSw indexes invSw by wpc_sw2m(no)/8) inverts these public addresses (computed in code by the
# test; 81 is a Not Used position).
MASKED_SWITCHES = frozenset({31, 32, 33, 71, 72, 73, 74, 75, 76, 77, 81})
OPTO_SWITCHES = frozenset({31, 32, 33, 71, 72, 73, 74, 75, 76, 77})
# T.1 SWITCH EDGES: the ROM names every one of these at public 1 except 32, which it names at public 0.
ROM_ACTIVE_AT_PUBLIC_ZERO = frozenset({32})
EDGES_SWEPT = (41, 78, 57, 47, 82, 68, 88, 38, 112, 114, 31, 32, 33, 71, 72, 73, 74, 75, 76, 77)
# The ROM's own names from the T.1 run (the top display line while the switch is active).
ROM_SWITCH_NAMES = {
	41: "<E>S-C-A-P-E", 78: "Mini. Lites Lock", 57: "Trap Door. Down", 47: "Hangon Score", 82: "Playfield Glass",
	68: "Mini. Door. Left", 88: "Mini. Door. Right", 38: "Mini. Door. Mid", 31: "Opto Popper",
	32: "Mini. Home Opto", 33: "Enter T.Ramp Opto", 71: "Mini.Opto.5Bank R1", 72: "Mini.Opto.5Bank R2",
	73: "Mini.Opto.5Bank M", 74: "Mini.Opto.5Bank L2", 75: "Mini.Opto.5Bank L1",
	76: "Mini. L. OptoEject", 77: "Mini. R. OptoEject",
}
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-Yellow", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"),
	3: ("White-Orange", "J208-3", "U18-5"), 4: ("White-Yellow", "J208-4", "U18-7"),
	5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
	7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"), 3: ("Orange-Black", "J205-3"),
	4: ("Orange-Yellow", "J205-4"), 5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"),
	7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
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
# Fliptronic grounded switches (manual 3-3, 3-9): printed number -> (public, label, wire, connector, type, role).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "Black-Green", "J906-1", "leaf", "internal.flipper.lower.right.eos", "F1"),
	112: ("Lower Right Flipper Button", "Blue-Violet", "J905-1", "opto", "flipper.lower.right.button", "F2"),
	113: ("Lower Left Flipper EOS", "Black-Blue", "J906-3", "leaf", "internal.flipper.lower.left.eos", "F3"),
	114: ("Lower Left Flipper Button", "Blue-Gray", "J905-2", "opto", "flipper.lower.left.button", "F4"),
	115: ("Not Fitted Upper Right Flipper EOS", None, None, None, "internal.unused.flipper", "F5"),
	116: ("Not Fitted Upper Right Flipper Button", None, None, None, "internal.unused.flipper", "F6"),
	117: ("Upper Left Flipper EOS", "Black-Gray", "J906-5", "leaf", "internal.flipper.upper.left.eos", "F7"),
	118: ("Upper Left Flipper Button", "Black-Blue", "J905-5", "opto", "flipper.upper.left.button", "F8"),
}

# --- Solenoid data (solenoid-flasher-table.md, solenoid-flasher-locations.md, power-driver connectors) ---
SOLENOID_LABELS = {
	1: "Trap Door", 2: "Shooter", 3: "Opto Popper", 4: "Mini-playfield Left Opto Eject",
	5: "Mini-playfield Right Opto Eject", 6: "2nd Chance Logo Flasher", 7: "Knocker", 8: "Doctor 3 Flasher",
	9: "Left Sling", 10: "Right Sling", 11: "Left Jet Bumper", 12: "Right Jet Bumper", 13: "Bottom Jet Bumper",
	14: "Backbox Head Flasher", 15: "Outhole", 16: "Trough Ball Release", 17: "Mini-playfield Doctor 7 Flasher",
	18: "5x3 Left/Left Flasher", 19: "5x3 Right/Right Flasher", 20: "Jet Bumpers Doctor 5 Flasher",
	21: "REPAIR Doctor 4 Flasher", 22: "W-(H)-O Doctor 2 Flasher", 23: "W-H-(O) Doctor 6 Flasher",
	24: "ESCAPE Doctor 1 Flasher", 27: "Mini-playfield Motor Direction", 28: "Mini-playfield Motor On/Off",
	35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_USED_SOLENOID_LABELS = {
	25: "Not Used Solenoid Position 25",
	26: "Not Used Solenoid Position 26",
	33: "Not Fitted Upper Right Flipper Power",
	34: "Not Fitted Upper Right Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC State Bit 29 (GILAMPS bit 5)",
	30: "WPC State Bit 30 (GILAMPS bit 6)",
	31: "WPC State Bit 31 (GILAMPS bit 7)",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Output 37", 38: "Unused WPC-Fliptronic Output 38",
	39: "Unused WPC-Fliptronic Output 39", 40: "Unused WPC-Fliptronic Output 40",
	41: "Unused WPC-Fliptronic Output 41", 42: "Unused WPC-Fliptronic Output 42",
	43: "Unused WPC-Fliptronic Output 43", 44: "Unused WPC-Fliptronic Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# address -> printed type, voltage connector, driver transistor, playfield connection, backbox/insert
# connection, wire colour, part / flashlamp (manual 3-5 Solenoid/Flasher Table).
SOLENOID_TABLE = {
	1: ("High Power", "J107-3", "Q82", "J130-1", None, "Vio-Brn", "AE-26-1500"),
	2: ("High Power", "J107-2", "Q80", "J130-2", None, "Vio-Red", "AE-26-1200"),
	3: ("High Power", "J107-3", "Q78", "J130-4", None, "Vio-Orn", "AE-23-800"),
	4: ("High Power", "J107-2", "Q76", "J130-5", None, "Vio-Yel", "AE-26-1500"),
	5: ("High Power", "J107-2", "Q64", "J130-6", None, "Vio-Grn", "AE-26-1500"),
	6: ("High Power", "J107-5", "Q66", "J130-7", "J131-3", "Vio-Blu", "#906"),
	7: ("High Power", "J107-3", "Q68", "J130-8", None, "Vio-Blk", "AE-23-800"),
	8: ("High Power", "J107-5", "Q70", None, "J131-5", "Vio-Gry", "#906"),
	9: ("Low Power", "J107-2", "Q58", "J127-1", None, "Brn-Blk", "AE-26-1500"),
	10: ("Low Power", "J107-2", "Q56", "J127-3", None, "Brn-Red", "AE-26-1500"),
	11: ("Low Power", "J107-2", "Q54", "J127-4", None, "Brn-Org", "AE-26-1200"),
	12: ("Low Power", "J107-2", "Q52", "J127-5", None, "Brn-Yel", "AE-26-1200"),
	13: ("Low Power", "J107-2", "Q50", "J127-6", None, "Brn-Grn", "AE-26-1200"),
	14: ("Low Power", "J107-6", "Q48", None, "J128-2", "Brn-Blu", "#906"),
	15: ("Low Power", "J107-2", "Q46", "J127-8", None, "Brn-Vio", "AE-27-1200"),
	16: ("Low Power", "J107-2", "Q44", "J127-9", None, "Brn-Gry", "AE-26-1200"),
	17: ("Flasher", "J107-5,6", "Q42", "J126-1", "J125-1", "Blk-Brn", "#906"),
	18: ("Flasher", "J107-5", "Q40", "J126-2", "J125-2", "Blk-Red", "#906"),
	19: ("Flasher", "J107-5", "Q38", "J126-3", "J125-3", "Blk-Org", "#906"),
	20: ("Flasher", "J107-5,6", "Q36", "J126-4", "J125-5", "Blk-Yel", "#906"),
	21: ("Flasher", "J107-5,6", "Q28", "J126-5", "J125-6", "Blu-Grn", "#906"),
	22: ("Flasher", "J107-5", "Q30", "J126-6", "J125-7", "Blu-Blk", "#906"),
	23: ("Low Power", "J107-5", "Q34", "J126-7", "J125-8", "Blu-Vio", "#906"),
	24: ("Low Power", "J107-5", "Q32", "J126-8", "J125-9", "Blu-Gry", "#89"),
	25: ("Flasher", None, "Q26", None, None, "Blu-Brn", None),
	26: ("Flasher", None, "Q24", None, None, "Blu-Red", None),
	27: ("Flasher", "J107-6", "Q22", "J122-3", None, "Blu-Org", "A-15680"),
	28: ("Flasher", "J107-6", "Q20", "J122-4", None, "Blu-Yel", "A-15680"),
}
# Locations-list assembly for each coil/flasher (manual 2-47).
SOLENOID_ASSEMBLIES = {
	1: "A-15641", 2: "A-15720", 3: "A-15440", 4: "A-15358-1", 5: "A-15358", 6: "A-12336-1", 7: "B-10686-1",
	9: "B-11203-R-1", 10: "B-11203-R-1", 11: "A-9415-2", 12: "A-9415-2", 13: "A-9415-2", 14: "A-12336-1",
	15: "B-8039-3", 16: "B-9362-L-2", 17: "A-16041", 18: "A-12336-1", 19: "A-12336-1", 20: "A-12336-1",
	21: "A-12336-1", 22: "A-12336-1", 23: "A-12336-1", 24: "A-8798", 27: "A-15680", 28: "A-15680",
}
FLASHER_SOLENOIDS = frozenset({6, 8, 14, 17, 18, 19, 20, 21, 22, 23, 24})
# Flasher bulbs: printed flashlamp type and printed counts (Locations list: 06 "(4)", 20 "(2)", 21 "(2)"). A quantity may exceed the placements: the circuit also feeds an insert-panel bulb.
FLASHER_COUNTS = {6: 4, 20: 2, 21: 2}
# Solenoids whose ROM name and pulse the T.4 SOLENOID TEST run observed (name as read from the frames).
T4_NAMES = {
	1: "Trap Door", 2: "Shooter", 3: "Opto Popper", 4: "Mini. L. Opto.Eject", 5: "Mini. R. Opto.Eject",
	7: "Knocker", 9: "Left Sling", 10: "Right Sling", 11: "Left Jet", 12: "Right Jet", 13: "Bottom Jet",
	15: "Outhole", 16: "Trough", 25: "Unused",
}
T4_ADDRESSES = (1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 13, 15, 16, 25)
T5_ADDRESSES = (6, 8, 14, 17, 18, 19, 20, 21, 22, 23, 24)
SOLENOID_CALLBACKS = {
	1: "SolTrapDoor", 2: "SolAutoFire", 3: "TardisExit", 4: "solmpfl", 5: "solmpfr", 6: "Flash06 (SolModCallback)",
	7: "SolKnocker", 8: "Flash08 (SolModCallback)", 15: "SolOutHole", 16: "SolBallRelease",
	17: "Flash17 (SolModCallback)", 18: "Flash18 (SolModCallback)", 19: "Flash19 (SolModCallback)",
	20: "Flash20 (SolModCallback)", 21: "Flash21 (SolModCallback)", 22: "who_h (SolModCallback)",
	23: "who_o (SolModCallback)", 24: "Flash24 (SolModCallback)", 36: "SolULFlipper", 46: "SolRFlipper",
	48: "SolLFlipper",
}
# Fliptronic circuits (manual 3-5 and 3-11): public address -> power/hold, connectors, transistor, wires.
FLIPPER_COILS = {
	35: ("power", "J907-8,9", "J902-3", "Q1", "Gray-Yellow", "Black-Blue"),
	36: ("hold", "J907-8,9", "J902-1", "Q5", "Gray-Yellow", "Orange-Gray"),
	45: ("power", "J907-1,2", "J902-13", "Q4", "Blue-Yellow", "Blue-Violet"),
	46: ("hold", "J907-1,2", "J902-11", "Q11", "Blue-Yellow", "Orange-Green"),
	47: ("power", "J907-4,5", "J902-9", "Q3", "Gray-Yellow", "Blue-Gray"),
	48: ("hold", "J907-4,5", "J902-7", "Q9", "Gray-Yellow", "Orange-Blue"),
}

# --- Lamp data (lamp-locations.md, lamp-matrix.md, power-driver connectors) -----------------------------
# address -> (bulb, assembly, description, second bulb or None); second = (bulb, assembly, location text).
LAMP_LOCATIONS = {
	11: ("24-8768", "A-15428", "(E)-S-C-A-P-E", None), 12: ("24-8768", "A-15428", "E-(S)-C-A-P-E", None),
	13: ("24-8768", "A-15428", "E-S-(C)-A-P-E", None), 14: ("24-8768", "A-15428", "E-S-C-(A)-P-E", None),
	15: ("24-8768", "A-15428", "E-S-C-A-(P)-E", None), 16: ("24-8768", "A-15428", "E-S-C-A-P-(E)", None),
	17: ("24-6549", "A-11271", "Left Drain", None), 18: ("24-6549", "A-11271", "Left Return", None),
	21: ("24-6549", "A-11271", "Right Return", None), 22: ("24-6549", "A-11271", "Right Drain", None),
	23: ("24-8768", "A-15805", "Doctor 7", ("24-6549", "A-8882", "speaker panel")),
	24: ("24-8768", "A-15427", "ESCAPE Special", None), 25: ("24-8768", "A-15427", "ESCAPE 3,000,000", None),
	26: ("24-8768", "A-15427", "ESCAPE 2,000,000", None), 27: ("24-8768", "A-15427", "ESCAPE 1,000,000", None),
	28: ("24-8768", "A-15427", "ESCAPE 500,000", None),
	31: ("24-8768", "A-15424", "5X3 Top Left 1", None), 32: ("24-8768", "A-15424", "5X3 Top Left 2", None),
	33: ("24-8768", "A-15424", "5X3 Top Middle", None), 34: ("24-8768", "A-15424", "5X3 Top Right 2", None),
	35: ("24-8768", "A-15424", "5X3 Top Right 1", None),
	36: ("24-8768", "A-15805", "Doctor 2", ("24-8768", "A-11271", "speaker panel")),
	37: ("24-6549", "A-11754", "Hang On Score", None), 38: ("24-6549", "A-11754", "Video Mode", None),
	41: ("24-8768", "A-15424", "5X3 Middle Left 1", None), 42: ("24-8768", "A-15424", "5X3 Middle Left 2", None),
	43: ("24-8768", "A-15424", "5X3 Middle Middle", None), 44: ("24-8768", "A-15424", "5X3 Middle Right 2", None),
	45: ("24-8768", "A-15424", "5X3 Middle Right 1", None),
	46: ("24-6549", "A-11754", "Transmat Award", None), 47: ("24-8768", "A-15647", "Tardis", None),
	48: ("24-8768", "A-15805", "Doctor 1", ("24-8768", "A-11271", "speaker panel")),
	51: ("24-8768", "A-15424", "5X3 Bottom Left 1", None), 52: ("24-8768", "A-15424", "5X3 Bottom Left 2", None),
	53: ("24-8768", "A-15424", "5X3 Bottom Middle", None), 54: ("24-8768", "A-15424", "5X3 Bottom Right 2", None),
	55: ("24-8768", "A-15424", "5X3 Bottom Right 1", None),
	56: ("24-6549", "A-8882", "Mini-playfield Left Lock", None), 57: ("24-6549", "A-8882", "Mini-playfield Right Lock", None),
	58: ("24-6549", "A-11905", "Mini-playfield Target", None),
	61: ("24-8768", "A-14520", "(R)-E-P-A-I-R", None), 62: ("24-8768", "A-14520", "R-(E)-P-A-I-R", None),
	63: ("24-8768", "A-14520", "R-E-(P)-A-I-R", None), 64: ("24-8768", "A-14520", "R-E-P-(A)-I-R", None),
	65: ("24-8768", "A-14520", "R-E-P-A-(I)-R", None), 66: ("24-8768", "A-14520", "R-E-P-A-I-(R)", None),
	67: ("24-8768", "A-15805", "Doctor 5", ("24-8767", "B-12224", "back panel")),
	68: ("24-6549", "A-11754", "Shoot Again", None),
	71: ("24-8768", "A-15805", "Doctor 4", ("24-8768", "A-15426", "speaker panel")),
	72: ("24-8768", "A-15805", "Doctor 6", ("24-8768", "A-15426", "speaker panel")),
	73: ("24-8768", "A-15426", "1.5X", None), 74: ("24-8768", "A-15426", "2X", None), 75: ("24-8768", "A-15426", "2.5X", None),
	76: ("24-8768", "A-15426", "3X", None), 77: ("24-8768", "A-15426", "3.5X", None), 78: ("24-8768", "A-15426", "4X", None),
	81: ("24-8768", "A-15427", "W-H-O (W)", None),
	82: ("24-8768", "A-15805", "Doctor 3", ("24-8768", "A-15427", "speaker panel")),
	83: ("24-8768", "A-15427", "W-H-O 1,000,000", None), 84: ("24-8768", "A-15427", "W-H-O 2,000,000", None),
	85: ("24-8768", "A-15427", "W-H-O Lite Extra Ball", None),
	86: ("24-6549", "A-11754", "Ball Transmat & Advance Bonus X", ("24-8768", "A-11271", "second playfield bulb")),
	87: ("20-9663-B-2", "A-15896", "Launch Ball", None), 88: (None, "20-9663-1", "Game Start", None),
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"), 3: ("Red-Orange", "J133-4", "Q88"),
	4: ("Red-Yellow", "J133-5", "Q87"), 5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
# Lamps whose second bulb the manual puts on the speaker panel or back panel (so they carry a quantity of 2).
DUAL_BULB_LAMPS = {23, 36, 48, 67, 71, 72, 82, 86}
CABINET_LAMPS = {87, 88}
MINI_PLAYFIELD_LAMPS = {56, 57, 58}
LAMP_MATRIX_LABEL_DIFFERENCES = {
	17: "Left Outlane", 18: "Left Return Lane", 21: "Right Return Lane", 22: "Right Outlane",
}

# --- General illumination (solenoid-flasher-table.md, power-driver-board-connectors.md) ----------------
# address -> (label, wire, playfield connection, insert connection, coin door connection, transistor, bulb)
GI_STRINGS = {
	0: ("Insert 1 (Back Panel Top)", "Brown", None, "J121-1", None, "Q18", "#555"),
	1: ("Insert 2 (Back Panel Bottom)", "Orange", None, "J121-2", None, "Q10", "#555"),
	2: ("Playfield A / Insert A", "Yellow", "J120-3", "J121-3", None, "Q14", "#44, #555"),
	3: ("Playfield B / Insert B", "Green", "J120-5", "J121-5", None, "Q16", "#44, #555"),
	4: ("Playfield C / Insert C / Coin Door", "Violet", "J120-6", "J121-6", "J119-3", "Q12", "#44, #555"),
}
GI_FEEDS = {
	2: ("J120-9 White-Yellow", "J121-9 White-Yellow"),
	3: ("J120-10 White-Green", "J121-10 White-Green"),
	4: ("J120-11 White-Violet", "J121-11 White-Violet"),
}


# --- Shared helpers ------------------------------------------------------------------------------------
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
		raise RuntimeError(f"Doctor Who retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Doctor Who extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Doctor Who retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Doctor Who retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Doctor Who retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


_LEGACY_ALIASES: dict[str, Any] = {}


def _legacy_aliases() -> dict[str, Any]:
	"""The legacy import's numeric and zero-padded aliases by binding group and address, kept while compatibility needs them."""
	if not _LEGACY_ALIASES:
		_LEGACY_ALIASES.update(load_json(LEGACY_ALIAS_SEED_PATH)["aliases"])
	return _LEGACY_ALIASES


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


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
	legacy = _legacy_aliases().get(group, {}).get(str(address))
	if legacy:
		device["aliases"] = list(device.get("aliases", [])) + [{"namespace": namespace, "value": value} for namespace, value in legacy]
	return device


def output_id(label: str) -> str:
	return "device." + (re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed")

# --- Placements ----------------------------------------------------------------------------------------
def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Located spatial record for one device from the committed placement seed, or None.

	Table-derived placements start as ``observed``; ``drawing_callouts.apply_to_definition`` promotes the
	ones the factory location drawings confirm. A placement read on the drawing itself is observed and
	cites the manual and the callout record only.
	"""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		refs = (MANUAL_SOURCE, CALLOUT_SOURCE) if entry.get("measured") else (VPX_TABLE_SOURCE,)
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": entry["x"],
				"y": entry["y"],
				"provenance": provenance("observed", *refs),
			}
		)
	return {"status": "observed", "placements": placements}


def _spatial(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	return located(category, address, identifier, role)


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_ic = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_ic = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


# What the retained known-working script does for each matrix switch (script-facts, switch inventory).
SWITCH_SCRIPT = {
	15: "LeftSling_Slingshot pulses it (vpmTimer.PulseSw)", 16: "RightSling_Slingshot pulses it (vpmTimer.PulseSw)",
	17: "ShooterLane_Hit/_Unhit follow the ball (Controller.Switch 1/0)", 18: "sw18_Hit pulses it",
	25: "sw25_Hit/_UnHit follow the ball (kicker sw25, the trough's release end)", 26: "sw26_Hit/_UnHit follow the ball",
	27: "sw27_Hit/_UnHit follow the ball", 28: "sw28_Hit/_UnHit follow the ball (kicker sw28, the outhole)",
	31: "TardisEntrance_hit sets it and only solenoid 3's TardisExit clears it",
	32: "UpdateMiniPF derives it in software from the mini-playfield mech position (no table object)",
	33: "sw33_Hit pulses it", 34: "the plunger key writes Controller.Switch(34)", 35: "gate5_Hit pulses it",
	36: "sw36_Hit pulses it", 37: "gate3_Hit pulses it", 38: "sw38s_Hit pulses it while the mini-playfield is at its top level",
	47: "LeftMiddle_Hit/_UnHit follow the ball", 48: "sw48_Hit pulses it", 57: "TDUpTimer_timer sets it when the trap-door primitive reaches RotX 0 with the coil on and clears it at -55",
	58: "sw58_Hit -> STHit pulses it", 61: "Bumper2_Hit pulses it", 62: "Bumper1_Hit pulses it", 63: "Bumper4_Hit pulses it",
	64: "LeftOutlane_Hit/_UnHit follow the ball", 65: "LeftInlane_Hit/_UnHit follow the ball",
	66: "RightInlane_Hit/_UnHit follow the ball", 67: "RightOutlane_Hit/_UnHit follow the ball",
	68: "sw68s_hit pulses it while the mini-playfield is at its top level",
	76: "sw76_hit/_unhit follow the locked ball (kicker sw76)", 77: "sw77_hit/_unhit follow the locked ball (kicker sw77)",
	78: "sw78_Hit -> STHit pulses it", 88: "sw88s_Hit pulses it while the mini-playfield is at its top level",
}
for _address in (41, 42, 43, 44, 45, 46, 51, 52, 53, 54, 55, 56):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit -> STHit pulses it (stand-up target animation)"
for _address in (71, 72, 73, 74, 75):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit -> STHit pulses it (droppable wall exposed only at the mini-playfield's middle level)"


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += " The Switch Locations parts list prints this position as Not Used (11-12, 81 and 83-87 as 'Not Used' rows) and the Switch Matrix and the Handy Technician's Chart print it as a Not Used cell."
		if address == 23:
			notes += (
				" The Switch Matrix prints 'Ticket Opto.' and the Switch Locations list '*Ticket Opto' with the assembly cell "
				"'Not Used'; the Handy Technician's Chart shades it as an opto. No ticket dispenser is part of the machine, so the "
				"position is a vestigial ticket-opto label with nothing fitted."
			)
		if address == 81:
			notes += " PinMAME's dwGameData inverted-switch mask nonetheless covers this position (column 8, row 1), which no device occupies."
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, HANDY_SOURCE, CONTROLLER_SOURCE),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE), **extra,
		)
	switch_no, assembly, description = SWITCH_LOCATIONS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES[address]}
	if switch_no != "---":
		physical["part_number"] = switch_no
	physical["assembly_part_number"] = assembly
	notes += f' Manual description "{description}".'
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in EDGES_SWEPT:
		refs += (EDGES_SOURCE,)
	if address in ROM_SWITCH_NAMES:
		notes += f' The ROM names it "{ROM_SWITCH_NAMES[address]}" in T.1 SWITCH EDGES.'
	if address in OPTO_SWITCHES:
		refs += (HANDY_SOURCE,)
		notes += (
			f" Opto switch: the Opto Switch 10 PCB A-15430 carries it ({OPTO_BOARD_CONNECTORS[address]}); the Handy Technician's "
			"Chart shades it 'OPTO, TYPICALLY CLOSED' while the Switch Matrix page prints no shading. The manual's opto theory "
			"reads the receiver at 0.1-0.7 V with the beam unblocked and 11-13 V blocked, and the Mini-playfield Test says an "
			"opto is active when the beam is broken, making the switch open. PinMAME's dwGameData inverted-switch mask inverts "
			"this address."
		)
		if address in ROM_ACTIVE_AT_PUBLIC_ZERO:
			notes += (
				" Mixed-level exception: the ROM's T.1 SWITCH EDGES run names this switch at public 0 and clears the name at public 1 "
				"(the name appeared when 32 was set to 0 and was absent when it was set to 1), the other way round from every other "
				"opto. Through the mask public 0 is a closed matrix contact, so the ROM reads this opto as active while its contact "
				"is closed; a consumer drives it as the retained script's UpdateMiniPF does, raw Controller.Switch(32) levels, and does "
				"not invert it again. normally_closed is false: the contact is open while the ROM reads the switch inactive, "
				"whatever the shaded legend says, because the legend marks opto construction and not the ROM's active level."
			)
		else:
			notes += (
				" The ROM's T.1 run names it at public 1 and clears the name at public 0; through the mask public 1 is an open matrix "
				"contact, so the ROM reads the opto as active with its beam broken and normally_closed is true."
			)
	elif address in EDGES_SWEPT and address < 100:
		notes += " The ROM's T.1 run names it at public 1 and clears the name at public 0, like the manual's ordinary switches."
	if address in {61, 62, 63}:
		notes += " The error list names it: the ROM counts low hits per jet bumper and reports 'Examine ... Jet Bumper Switch'."
	if address == 57:
		notes += (
			" Located on the underside of the playfield. The Trap Door Test draws a side view of the door and says 'When the TRAP DOWN "
			"switch is closed, the door will be down.'"
		)
	if address == 58:
		notes += " The Switch Locations list prints no switch part number for this standup (assembly A-15862, a stationary target with decal)."
	if address == 78:
		notes += (
			" The Switch Locations list calls it 'Mini-ply Target' (assembly A-15903, a standup target with decal; no switch part number); the "
			"Switch Matrix, the ROM and the Handy chart call it 'Mini-ply Lites Lock'. Hitting it lights the locks (game rules, Multiball)."
		)
	if address == 46:
		notes += " The Switch Locations drawing prints balloon 46, but its leader merges into the rail linework and cannot be followed; the reader's best-guess tip lies about 0.015 normalized from this placement, which is not a reading, so the placement stays observed."
	if address in {41, 42, 43, 44, 45, 46}:
		notes += " The six ESCAPE standups share assembly A-15631-4 and print no switch part number."
	if address in {51, 52, 53, 54, 55, 56}:
		notes += " The six REPAIR standups form the A-15439 6-Target Assembly (SW-1A-178-4 standup target switches)."
	if address in {15, 16}:
		notes += " The slingshot assembly B-8284-1 pairs this kick switch with the coil on the matching sling solenoid (9 and 10)."
	if address in {25, 26, 27}:
		notes += " The three trough switches count 1, 2 and 3 balls in the ball trough; the outhole (28) kicks drained balls into it and solenoid 16 releases one to the shooter lane."
	if address == 28:
		notes += " Solenoid 15 kicks the ball from the outhole into the trough."
	if address == 17:
		notes += " Shooter-lane switch beneath the ball resting in the lane; solenoid 2 (Shooter) launches it."
	if address in {76, 77}:
		notes += " Optical detection of a ball held in the mini-playfield's left or right lock hole, ejected by solenoid 4 or 5."
	if address in {71, 72, 73, 74, 75}:
		notes += " The five round white standup buttons ('dalek buttons') of the mini-playfield's 5-bank, exposed at its middle level."
	if address in {38, 68, 88}:
		notes += " One of the three doors of the mini-playfield's top level, through which the ball starts multiball and time-warps the Daleks."
	if address == 31:
		notes += " Solenoid 3 (Opto Popper) kicks the ball back out of the Tardis box; the assembly is A-15440 Cap Ball Popper."
	if address in {33, 35}:
		notes += " The manual names them 'Enter Top Ramp Opto' (33) and 'Score Top Ramp' (35) (assembly A-15436); its game rules call the top ramp the cliffhanger ramp and build the playfield multiplier from it."
	if address in {36, 37}:
		notes += " The manual names them 'Enter Bottom Ramp' (36, assembly A-15904 Switch Gate & Decal) and 'Score Bottom Ramp' (37)."
	if address in {47, 48}:
		notes += " The game rules say the Hang On Score is lit by the right return lane and collected by the W-H-O shot (H) before it times out; the Switch Locations list names 48 'Select Doctor' and the retained rules do not say which playfield feature it is."
	if address in {64, 65, 66, 67}:
		notes += f" The Handy Technician's Chart calls it '{ {64: 'Left Outlane', 65: 'Left Return Lane', 66: 'Right Return Lane', 67: 'Right Outlane'}[address] }'."
	label = SWITCH_LABELS[address]
	role = SWITCH_ROLES.get(address)
	if role:
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = "cabinet" if address in {13, 34} else "cabinet interior"
	elif address == 24:
		extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
	else:
		spatial = _spatial("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
	kind = "constant" if address == 24 else "switch"
	if address == 24:
		notes += " The same part A-8630 as the Coin Door Closed switch; the script and the matrix self-test treat it as permanently closed."
		extra["constant_active"] = True
		extra["initial_active"] = True
	else:
		# normally_closed records the matrix contact while the ROM reads the switch inactive.
		extra["normally_closed"] = address in OPTO_SWITCHES and address not in ROM_ACTIVE_AT_PUBLIC_ZERO
	if address in {22, 82}:
		extra["initial_active"] = True
		notes += " The retained script sets it closed at table start." + (" Closed while the coin door is closed." if address == 22 else " Closes when the playfield glass is in place; the manual adjusts it with T.1 switch #82.")
	if address == 34:
		notes += " Cabinet pushbutton on the left side of the cabinet with a lit lamp (87); Doctor Who has no manual plunger."
	if address == 13:
		notes += " The lit Start Button (lamp 88)."
	physical["notes"] = notes
	return _device(identifier, label, kind, SWITCH_GROUP, address, "used", refs, physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, wire, connection, switch_type, role, printed) in FLIPPER_SWITCHES.items():
		fitted = wire is not None
		notes = f"Printed Fliptronic grounded switch {printed}."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"roles": [role],
		}
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		physical: dict[str, Any] = {}
		if not fitted:
			notes += (
				" Not fitted: the game-specific Switch Locations parts list prints F1-F4 and F7-F8 but no F5 or F6 row, the Solenoid/Flasher "
				"Table and the Solenoid/Flasher Locations list name only an Upper Left, a Lower Left and a Lower Right flipper, the "
				"Fliptronic II Flipper Assembly page lists A-15205-R-4, A-15205-L-4 and A-16090-L-4 (a left-hand upper variant), and the "
				"retained script has no upper-right flipper object or callback. The Switch Matrix, the Fliptronic wiring pages and the "
				"Handy Technician's Chart print F5/F6 as generic Fliptronic II board positions, and PinMAME's dwGameData declares "
				"FLIP_SW(FLIP_L|FLIP_U), which synthesizes both upper switch pairs; none of that fits a flipper."
			)
			physical["location"] = "not installed"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			availability = "unused"
		else:
			availability = "used"
			physical["switch_type"] = switch_type
			physical["location"] = "cabinet flipper button" if role.endswith(".button") else "flipper assembly"
			extra["wiring"] = {"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection}
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service" if role.endswith(".button") else "internal_nonvisual", MANUAL_SOURCE)
			if role.endswith(".button"):
				refs += (HANDY_SOURCE, EDGES_SOURCE) if address in {112, 114} else (HANDY_SOURCE,)
				notes += (
					" Board A-15894 (Flipper Opto Board) carries two opto interrupters; the Handy Technician's Chart shades this cell as an opto. "
					"This generation's WPC_FLIPPERS read returns the complement of the flipper switch column, so the public switch state is "
					"already normalized: public 1 is the pressed button and the contact the matrix sees is open at rest, so normally_closed "
					"is false whatever the beam does."
				)
				if address in {112, 114}:
					notes += " The T.1 run set it to 1 and the ROM fired the flipper, its synthesized end-of-stroke bit rising on the matching EOS address."
				else:
					notes += " It shares the left flipper opto board with F4 (J905-5 on the second opto); the retained script's left key activates the upper left flipper but the library writes only 112 and 114."
			else:
				notes += (
					" End-of-stroke switch SW-1A-193 on the flipper assembly. PinMAME synthesizes this address from the flipper coil state after the "
					"flip stroke time, so its public level is not a measurement of the physical contact and normally_closed records the "
					"Fliptronic grounded-switch convention (closed to ground only at end of stroke)."
				)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, availability, refs, **extra))
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country/option configuration bit)", "dip_switch", DIP_GROUP, address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC CPU board", "switch_type": "dip",
					"notes": "WPC CPU-board country/option DIP bank. The retained transcription does not include the per-country chart, so no ON/OFF combination is asserted; the retained script sets DIP 0 to 0 (USA).",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items

# --- Outputs -------------------------------------------------------------------------------------------
# What the ROM's T.4 SOLENOID TEST and T.5 FLASHER TEST print for each driver (read from the retained frames).
T4_WIRES = {
	1: "VIO-BRN VIO-YEL", 2: "VIO-RED VIO-YEL", 3: "VIO-ORN VIO-YEL", 4: "VIO-YEL VIO-YEL", 5: "VIO-GRN VIO-YEL",
	7: "VIO-BLK VIO-YEL", 9: "BRN-BLK VIO-ORN", 10: "BRN-RED VIO-ORN", 11: "BRN-ORN VIO-ORN", 12: "BRN-YEL VIO-ORN",
	13: "BRN-GRN VIO-ORN", 15: "BRN-VIO VIO-ORN", 16: "BRN-GRY VIO-ORN", 25: "BLU-BRN VIO-GRN",
}
SOLENOID_NOTES = {
	1: "Trap Door Assembly A-15641 (with A-15442 Cam & Plunger and A-15444 Gate Assemblies) under the left side of the playfield; switch 57 (Trap Door Down) senses it. The game lowers it every tenth loop (Sonic Boom). The T.13 Trap Door Test cycles it with a pull-in and a hold-in phase.",
	2: "Ball Shooter Lane Feeder: Doctor Who has no manual plunger, the Launch Ball button (switch 34) asks the ROM to fire this coil and the ball in the shooter lane (switch 17) is launched.",
	3: "Cap Ball Popper Assembly A-15440 under the Tardis Box: the ball rests on the opto beam of switch 31 and this coil kicks it out.",
	4: "Mini-playfield Ball Popper Assembly A-15358-1 with an opto (switch 76) on its lock hole. In the T.14 Mini-playfield Test the 'L Kicker' sub-test pulses it.",
	5: "Mini-playfield Ball Popper Assembly A-15358 with an opto (switch 77) on its lock hole. In the T.14 Mini-playfield Test the 'R Kicker' sub-test pulses it.",
	6: "Flasher with a printed count of (4) on the Locations list; the quantity is that printed count; the drawing places two locations for it. The ROM's T.5 FLASHER TEST names it '2nd Chance Davros' (the manual prints '2nd Chance Logo'; the Locations list prints '2nd Change Logo'). It is wired both toward the playfield (J130-7) and toward the insert panel (J131-3), so its bulbs sit on the playfield and in the backbox.",
	7: "Knocker Assembly B-10686-1 in the backbox; the Locations list marks it '*' (not shown).",
	8: "Backbox flasher for the Doctor 3 lamp position; the Locations list prints '*Doctor 3, Flasher' with no assembly number. Wired only toward the insert flasher connector (J131-5): the Solenoid Table prints no playfield connection, so it has no playfield bulb. The retained script drives only a backglass flasher for it.",
	9: "Slingshot (Kicker Arm Assembly B-12665) with Coil & Bracket Assembly B-11203-R-1; kick switch 15.",
	10: "Slingshot (Kicker Arm Assembly B-12665) with Coil & Bracket Assembly B-11203-R-1; kick switch 16.",
	11: "Jet bumper coil (A-9415-2) of the Left Jet bumper; scoring switch 61. The retained script has this callback commented out (bpr1): a jet bumper does not need it to fire.",
	12: "Jet bumper coil (A-9415-2) of the Right Jet bumper; scoring switch 62. The retained script has this callback commented out (bpr2).",
	13: "Jet bumper coil (A-9415-2) of the Bottom Jet bumper; scoring switch 63. The retained script has this callback commented out (bpr3).",
	14: "Backbox Head flasher: the lamp in the Dalek topper's head. The Locations list prints '*Backbox Head, Flasher (if used)', the Solenoid Table connects it only to J128-2 (backbox), and the retained script drives no object for it.",
	15: "Outhole Kicker Assembly A-8039-3: kicks a drained ball from the outhole (switch 28) into the trough.",
	16: "Trough ball-release coil (Coil & Bracket Assembly B-9362-L-2): releases the ball at the trough's exit toward the shooter lane.",
	17: "Flasher under the mini-playfield cover (A-16041 Bulb & Light Socket Assembly; the cover A-15582 also carries the A-12336-1 socket) and in the Doctor 7 insert. The Mini-playfield Wiring Block Diagram draws it beside the motor board.",
	18: "Flasher at the left side of the 5x3 matrix, wired toward the playfield (J126-2) and the insert panel (J125-2).",
	19: "Flasher at the right side of the 5x3 matrix, wired toward the playfield (J126-3) and the insert panel (J125-3). The ROM's T.5 prints '5x3 Right/Right' with the wires BLK-ORN RED-WHT at this address.",
	20: "Flashers at the jet bumpers and the Doctor 5 position (printed count (2)), wired toward the playfield (J126-4) and the insert panel (J125-5). The retained table's FL20 is a single invisible rotated Flasher sprite carrying Doctor 5 artwork, not a socket, so the two playfield bulbs are measured on the Solenoid/Flasher Locations drawing, where callout 20 has two prongs ending on two flasher assemblies at the top edge (accurate to about 0.04; y clamped to the edge).",
	21: "Flashers on the REPAIR lamps and the Doctor 4 position (printed count (2)), wired toward the playfield (J126-5) and the insert panel (J125-6). The ROM's T.5 names it 'REPAIR/Dr.4'.",
	22: "Flasher at the W-(H)-O lamp and the Doctor 2 position, wired toward the playfield (J126-6) and the insert panel (J125-7).",
	23: "Flasher at the W-H-(O) lamp and the Doctor 6 position, wired toward the playfield (J126-7) and the insert panel (J125-8). The Solenoid Table prints its type as 'Low Power' although it is a flasher row; the Handy Technician's Chart prints 'Flasher'.",
	24: "Flasher at the ESCAPE lamps and the Doctor 1 position, wired toward the playfield (J126-8) and the insert panel (J125-9); it uses a #89 playfield flashlamp (24-8704, A-8798) rather than a #906. The Solenoid Table prints its type as 'Low Power'; the Handy Technician's Chart prints 'Flasher'.",
	25: "Printed 'Not Used' (general-purpose flasher driver Q26 with no connections). The ROM's T.4 nevertheless pulses public 25 and prints 'Unused' with BLU-BRN VIO-GRN.",
	26: "Printed 'Not Used' (general-purpose flasher driver Q24 with no connections).",
	27: "Direction line of the mini-playfield's bi-directional motor drive board A-15680 (printed 'Mini-playfield C.C.W./C.W.'). In the T.14 Mini-playfield Test the ROM first drives 28 alone, and after its error drives 27 together with 28 for the other direction, so 28 runs the motor and 27 selects the direction. The board's own page prints the wire colours on its two input pins crossed against the connector list.",
	33: "Power winding position of the upper right flipper circuit. Not fitted: the Solenoid/Flasher Table, the Solenoid/Flasher Locations list and the Fliptronic II Flipper Assembly page name only an upper left, a lower left and a lower right flipper, and the retained script has no upper right flipper object or callback. PinMAME's FLIP_SW(FLIP_L|FLIP_U) synthesizes the output regardless.",
	34: "Hold winding position of the upper right flipper circuit; not fitted for the same reasons as solenoid 33.",
	28: "Run line of the mini-playfield's bi-directional motor drive board A-15680 (printed 'Mini-playfield On/Off'); the 20 V DC motor (14-7970) turns the cam of A-15634 Motor & Cam Assembly. The retained script models the motor as a cvpmMech with sol1 = 28 and sol2 = 27.",
}
SOLENOID_ROLES = {7: "cabinet.knocker", 8: "cabinet.backbox", 14: "cabinet.backbox"}


def _solenoid_wiring(address: int) -> dict[str, Any]:
	kind, voltage, transistor, playfield, backbox, wire, part = SOLENOID_TABLE[address]
	wiring: dict[str, Any] = {"board": "WPC power driver board", "driver_transistor": transistor, "control_wire": wire}
	connections = [connection for connection in (playfield, backbox) if connection]
	if connections:
		wiring["control_connection"] = ", ".join(connections)
	if voltage:
		wiring["power_connection"] = voltage
	return wiring


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in FLIPPER_COILS:
			stage, voltage, control, transistor, supply_wire, control_wire = FLIPPER_COILS[address]
			side = "Upper Left" if address in {35, 36} else ("Lower Right" if address in {45, 46} else "Lower Left")
			label = SOLENOID_LABELS[address]
			notes = (
				f"{side} flipper {stage} winding on the Fliptronic II board (driver {transistor}, J902 pin {control.split('-')[1]}, "
				f"{control_wire}). The voltage connector {voltage} and supply {supply_wire} are the Fliptronic wiring page's; the "
				"Solenoid/Flasher Table prints the same flipper row with J902 pins and wire colours that differ in places, and the "
				"Handy Technician's Chart prints numbered flipper circuits 29-36 with YEL-/ORG- wire colours; both readings are kept in the excerpts. "
				f"The coil is an FL-15411 (orange). PinMAME publishes the {side.lower()} flipper circuits at {address}; "
				"the retained script fires them from its callbacks "
				f"({SOLENOID_CALLBACKS.get(address, 'none: the script registers only 36, 46 and 48')})."
			)
			wiring = {
				"board": "Fliptronic II controller board",
				"driver_transistor": transistor,
				"control_connection": control,
				"control_wire": control_wire,
				"power_connection": voltage,
				"power_wire": supply_wire,
			}
			identifier = output_id(label)
			spatial = _spatial("solenoid", address, identifier, "effect")
			extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}], "physical": {"part_number": "FL-15411", "notes": notes}, "wiring": wiring}
			if spatial:
				extra["spatial"] = spatial
			items.append(_device(identifier, label, "coil", SOLENOID_GROUP, address, "used", (MANUAL_SOURCE, HANDY_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra))
			continue
		if address in SOLENOID_LABELS or address in NOT_USED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_USED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			if address in SOLENOID_TABLE:
				printed_type, voltage, transistor, playfield, backbox, wire, part = SOLENOID_TABLE[address]
				notes = f"Printed solenoid table entry {address:02d} ({printed_type}, driver {transistor}, wire {wire})."
			else:
				notes = f"Printed Fliptronic circuit for the upper right flipper."
				printed_type = part = None
			notes += " " + SOLENOID_NOTES.get(address, "")
			if address in T4_WIRES:
				notes += f" T.4 SOLENOID TEST: the ROM pulses public {address} and prints \"{T4_NAMES[address]}\" with the wires {T4_WIRES[address]}."
			if address in T5_ADDRESSES:
				notes += " T.5 FLASHER TEST: the ROM pulses this public address in its flasher walk."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			elif fitted and address in {11, 12, 13}:
				pass
			elif fitted:
				notes += " The retained script registers no callback for it."
			if address in {2, 4, 5}:
				notes += (
					" The ROM's own T.4 text prints the supply wire VIO-YEL (J107-3, the Violet-Yellow +50 V) for this coil while the "
					"Solenoid Table and the Handy Technician's Chart print the voltage connector J107-2; the ROM, the manual and the "
					"chart agree on the device and its address, so the supply connector disagreement is a wiring detail."
				)
			kind = "flasher" if address in FLASHER_SOLENOIDS else ("motor" if address == 28 else ("control_signal" if address == 27 else "coil"))
			physical: dict[str, Any] = {}
			if part and kind != "flasher" and address not in {27, 28}:
				physical["part_number"] = part
			if address in {27, 28}:
				physical["part_number"] = "14-7970" if address == 28 else part
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if address in FLASHER_SOLENOIDS:
				notes += f" Printed flashlamp type {part}."
				if address in FLASHER_COUNTS:
					physical["quantity"] = FLASHER_COUNTS[address]
			if address in {6, 17, 18, 19, 20, 21, 22, 23, 24}:
				notes += " Only the playfield flashlamp is placed; the insert-panel lamp wired to the second connector is in the backbox."
			physical["notes"] = notes
			extra = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}], "physical": physical}
			if address in SOLENOID_TABLE:
				extra["wiring"] = _solenoid_wiring(address)
			refs: tuple[str, ...] = (MANUAL_SOURCE, HANDY_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address in {27, 28}:
				refs += (VPX_SCRIPT_SOURCE,)
			if address in T4_WIRES:
				refs += (SOLENOID_TEST_SOURCE,)
			if address in T5_ADDRESSES:
				refs += (FLASHER_TEST_SOURCE,)
			if address in {4, 5, 17, 27, 28}:
				refs += (MINI_PLAYFIELD_SOURCE,)
			if not fitted:
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				availability = "unused"
			elif address in SOLENOID_ROLES:
				extra["roles"] = [SOLENOID_ROLES[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				availability = "used"
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				spatial = _spatial("solenoid", address, identifier, role)
				if spatial:
					extra["spatial"] = spatial
			items.append(_device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors WPC_GILAMPS bit 5 here when the driver sets no fast-flip RAM address; dw_l2 calls no wpc_set_fastflip_addr (wpc.c: core_write_pwm_output of WPC_GILAMPS >> 5 at outputs 29-31). It is not a Doctor Who playfield device.",
			30: "PinMAME mirrors WPC_GILAMPS bit 6 here under the same rule as 29; not a playfield device.",
			31: "PinMAME mirrors WPC_GILAMPS bit 7 here under the same rule as 29, the bit that drove the game-on relay before Fliptronics; no relay exists on this machine and the harness runs found it active in the service menu. Not a playfield device.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero.",
		}.get(address, "This WPC-Fliptronic generation has no integrated LPDC board, so pinned PinMAME's core_getSol serves the 37-44 range only for WPC-95 and System 11; this address is unused space." if 37 <= address <= 44 else (
			"PinMAME's simulator-only ball-shooter channel; Doctor Who's real shooter is public solenoid 2." if address == 49 else "Reserved PinMAME output position before the first custom-output boundary; dw_l2 declares no custom solenoids."))
		items.append(
			_device(
				identifier, label, "virtual", SOLENOID_GROUP, address, availability, (CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=["internal.wpc-state"] if address in {29, 30, 31} else ["internal.unused.wpc-output"],
				physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			bulb, assembly, description, second = LAMP_LOCATIONS[address]
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			physical: dict[str, Any] = {"quantity": 2 if address in DUAL_BULB_LAMPS else 1, "assembly_part_number": assembly}
			notes = f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire}). Manual description \"{description}\"."
			if bulb:
				notes += f" Printed bulb {bulb}."
			if second:
				notes += (
					f" The Lamp Locations list prints a second bulb ({second[0]}, assembly {second[1]}) marked '{second[2]}'; "
					"the lamp matrix prints '(2 lamps)' for the Doctor lamps."
				)
			if address in {23, 36, 48, 71, 72, 82}:
				notes += (
					" The manual's lamp drawing shows the playfield bulb on the playfield and a rectangular balloon for the speaker-panel bulb in "
					"a row above the playfield outline (the 7-lamp strip under the dot-matrix display, assembly A-15805 on the Backbox Assembly page). The parts list prints A-15805 "
					"on the row labelled '(1 playfield)'; the Backbox Assembly page lists A-15805 as the 7-Lamp Board Assembly of the Speaker / Display Assembly, so the assembly "
					"number and the location label disagree. Only the playfield bulb is placed."
				)
			if address == 67:
				notes += (
					" Doctor 5: the second bulb is on the back panel (24-8767, B-12224) on the parts list, while the Power Driver Board connector list "
					"routes column 6 and row 7 to the speaker-panel connectors J138-6 and J135-8. The retained table has no Light for the playfield "
					"bulb: the lamp drawing's teardrop callout 67 ends on the playfield's top edge near the right corner, where the placement comes from."
				)
			if address == 86:
				notes += " Two bulbs, both listed on the playfield and drawn as two balloons (an arrow and a circle); the second line of the printed description reads 'Advance Bonus X'."
			if address == 47:
				notes += " Tardis lamp inside the Tardis Box Assembly A-15647 (a #555 bulb in the box's lamp socket)."
			if address in MINI_PLAYFIELD_LAMPS:
				notes += " Mounted on the mini-playfield, so it rises and falls with it; the table moves it in Z only and its x/y are the playfield position."
			if address in LAMP_MATRIX_LABEL_DIFFERENCES:
				notes += f" The Handy Technician's Chart labels this lamp '{LAMP_MATRIX_LABEL_DIFFERENCES[address]}'."
			if column == 8:
				notes += " The lamp matrix page prints column 8's connector as J138-9 while the connector list and the Handy chart print J137-9 for the playfield lamps (J138-9 is the speaker-panel branch)."
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the lit Launch Ball / Game Start button assembly; the connector list routes row 8 and column 8 to the cabinet-lamp connectors J134-9 and J136-3."
			physical["notes"] = notes
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"physical": physical,
				"wiring": {
					"board": "WPC power driver board", "drive_wire": drive_wire, "drive_connection": drive_connection,
					"return_wire": return_wire, "return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address in CABINET_LAMPS:
				extra["roles"] = ["cabinet.launch" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				spatial = _spatial("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
			items.append(
				_device(
					identifier, description, "lamp", LAMP_GROUP, address, "used",
					(MANUAL_SOURCE, HANDY_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra,
				)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, wire, playfield, insert, coin_door, transistor, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulbs {bulb}, return wire {wire}, driver {transistor}."
		wiring: dict[str, Any] = {"board": "WPC power driver board", "driver_transistor": transistor}
		connections = [connection for connection in (playfield, insert, coin_door) if connection]
		wiring["control_connection"] = ", ".join(connections)
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{address + 1:02d}"}], "wiring": wiring}
		physical: dict[str, Any] = {}
		refs: tuple[str, ...] = (MANUAL_SOURCE, HANDY_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		if address in GI_FEEDS:
			notes += (
				f" The Power Driver Board connector list brings this string out toward the playfield ({GI_FEEDS[address][0]}, return {playfield}), the insert "
				f"panel ({GI_FEEDS[address][1]}, return {insert})"
				+ (f" and the coin door (return {coin_door}, J119-1 6.8 VAC)." if coin_door else ".")
				+ " The Handy Technician's Chart places the J121 pins under 'Playfield' and prints no insert column for these strings, which disagrees with the connector list; the manual's table and the connector list are followed."
			)
			spatial = _spatial("gi", address, identifier, "emitter")
			notes += (
				" The retained table's UpdateGI drives a per-string collection of playfield Light objects for this string, whose grouping is the table author's: "
				"the placements are those lights with co-located stacked bulbs collapsed to one, kept observed and without a quantity because the manual prints no "
				"per-string bulb count and no drawing locates GI bulbs."
			)
			if spatial:
				extra["spatial"] = spatial
		else:
			notes += (
				" Backbox illumination behind the translight and insert board, matching the manual's 'Insert' classification and the connector list, which brings "
				"it out only toward the insert (J121). The retained script's UpdateGI drives only backbox glow flashers for it."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "gi", GI_GROUP, address, "used", refs, **extra))
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
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE),
		}
	]

# --- Mechanisms, drivers and conflicts -------------------------------------------------------------------
def _coil(address: int) -> str:
	return output_id(SOLENOID_LABELS[address])


def _mechanism(
	suffix: str,
	label: str,
	kind: str,
	actuators: list[str],
	sensors: list[str],
	behavior: str,
	refs: tuple[str, ...],
	positions: list[tuple[str, str, list[str], str]] | None = None,
	assembly: str | None = None,
	status: str = "observed",
) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"mechanism.{suffix}",
		"label": label,
		"kind": kind,
		"actuators": actuators,
		"sensors": sensors,
		"behavior": behavior,
		"provenance": provenance(status, *refs),
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
	flipper_refs = (MANUAL_SOURCE, HANDY_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE)
	return [
		_mechanism(
			"mini-playfield",
			"Time Expander mini-playfield",
			"motorized",
			[_coil(28), _coil(27)],
			_matrix(32),
			"A small playfield at the top of the playfield rides on a motor-driven cam and moves between three levels. A 20 V DC motor "
			"(14-7970) in the A-15634 Motor & Cam Assembly turns the cam; the Bi-directional Motor Drive board A-15680 takes two "
			"logic lines from the power driver board, solenoid 28 (printed 'On/Off') runs the motor and solenoid 27 (printed "
			"'C.C.W./C.W.') selects the direction. The ROM's T.14 test drives 28 alone for the first attempt, then 27 together with "
			"28 after it reports an error, which is how the two lines were told apart. The only position feedback is the Home Opto "
			"(switch 32, an Opto Switch 10 PCB opto, ROM-active at public 0 behind PinMAME's mask), which the manual describes only "
			"as the mini-playfield's home sensor; the manual prints no other level sensor. The retained known-working script models "
			"the motor as a one-direction cvpmMech with 360 steps over a 270-step length (sol1 = 28, sol2 = 27) and derives switch 32 "
			"from position windows of its own, so the windows are the table author's, not measurements. During normal play the "
			"mini-playfield does not move unless the coin door is closed and the playfield glass is on, and in T.14 both flipper "
			"buttons must be held before it moves. The levels: Level 1 (lowest) exposes the left and right lock holes and the "
			"Lites Lock target; Level 2 (middle) exposes the five dalek buttons; Level 3 (upper) exposes the three doors. "
			"Removal instructions place the mini-playfield 'in the down position' to remove it and in 'the middle position' when "
			"re-installing. Lamps 56-58 and the Doctor 7 flasher (solenoid 17) are mounted on it and travel with it. Manual "
			"amendment 16-9453 adds a cant-correction procedure for its guide bearings. A Dalek-head motor and opto that "
			"prototype machines carried in the backbox topper are not part of the production machine.",
			(MANUAL_SOURCE, AMENDMENT_SOURCE, IDENTITY_SOURCE, VPX_SCRIPT_SOURCE, MINI_PLAYFIELD_SOURCE),
			[
				("level-1", "Level 1 (lowest)", _matrix(76, 77, 78), "Lock holes (switches 76, 77) and the Lites Lock target (78) are reachable."),
				("level-2", "Level 2 (middle)", _matrix(71, 72, 73, 74, 75), "The five dalek buttons of the 5-bank are reachable."),
				("level-3", "Level 3 (upper)", _matrix(38, 68, 88), "The three doors are reachable; entering a door starts multiball or time-warps a Dalek."),
			],
			"A-15634",
		),
		_mechanism(
			"mini-playfield-ball-poppers",
			"Mini-playfield lock-hole poppers",
			"kicker",
			[_coil(4), _coil(5)],
			_matrix(76, 77),
			"Two Ball Popper Assemblies (A-15358-1 left, A-15358 right) each hold a ball in a lock hole of the mini-playfield "
			"over an LED/photo-transistor pair (A-14231 / A-14232); the optos are switches 76 (left) and 77 (right) and the coils "
			"are solenoids 4 and 5. The T.14 'L Kicker' and 'R Kicker' sub-tests pulse 4 and 5 (the run found 4 and 5 transition "
			"there). Ejected balls are meant to hit the lower flippers: the playfield-adjustment page gives the eject adjustment.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, MINI_PLAYFIELD_SOURCE),
			None,
			"A-15358",
		),
		_mechanism(
			"mini-playfield-5-bank",
			"Mini-playfield 5-bank (dalek buttons)",
			"other",
			[],
			_matrix(71, 72, 73, 74, 75),
			"Five round white standup buttons (the 'dalek buttons') of the A-15500 5-Target Assembly, each read by an infrared "
			"opto on the A-15431 5-Opto Board with the A-15432 5-IR LED Board opposite. They are reachable only at the "
			"middle level and, after all five are hit, drop the Davros force field. The manual's maintenance text describes a "
			"'flip-up target reset lever' the Door Release Bracket pushes so that the targets drop; no coil resets them. The "
			"retained script models them as droppable walls exposed only at the middle level.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
			None,
			"A-15500",
		),
		_mechanism(
			"mini-playfield-3-door",
			"Mini-playfield 3-door assembly",
			"gate",
			[],
			_matrix(38, 68, 88),
			"A-15356 3-Door Assembly: three hinged flyaway door targets (left, middle, right) on a shaft with a Ball Return "
			"Assembly (A-15354), read by switches 68, 38 and 88. They are reachable at the upper level. During multiball a ball "
			"entering a door time-warps a Dalek; the middle door skips a jackpot.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
			None,
			"A-15356",
		),
		_mechanism(
			"trap-door",
			"Trap door",
			"other",
			[_coil(1)],
			_matrix(57),
			"The A-15641 Trap Door Assembly is a flap in the playfield driven by a plunger coil (solenoid 1, AE-26-1500) through a "
			"cam and a gate (A-15442, A-15444). Switch 57 (Trap Door Down) closes when the door is down; the T.13 test draws a "
			"side view of the door and cycles the coil with a pull-in and a hold-in phase, entering a COOLING state when it "
			"warms. The game lowers it every tenth loop so each letter of W-H-O scores 10 million (Sonic Boom). A failure to "
			"reach its position raises the 'Trap Door Down Error' or 'Trap Door Up Error'.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None,
			"A-15641",
		),
		_mechanism(
			"tardis-popper",
			"Tardis cap-ball popper",
			"kicker",
			[_coil(3)],
			_matrix(31),
			"The A-15440 Cap Ball Popper under the Tardis (A-15647 Tardis Box) holds a ball over the Opto Popper beam (switch 31, "
			"A-14231/A-14232 optos with an AE-23-800 coil) and kicks it back to the playfield with solenoid 3. The retained script "
			"sets switch 31 when a ball enters and only the solenoid-3 callback clears it.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None,
			"A-15440",
		),
		_mechanism(
			"ball-trough",
			"Outhole and ball trough",
			"kicker",
			[_coil(15), _coil(16)],
			_matrix(28, 25, 26, 27),
			"A drained ball rolls into the outhole (switch 28) where the Outhole Kicker Assembly A-8039-3 (solenoid 15) kicks it into "
			"the ball trough; the three trough microswitches on the B-8925 plate (25, 26, 27 for one, two and three balls) count "
			"the balls held, and the trough-release coil (solenoid 16, B-9362-L-2 bracket) releases one toward the shooter lane. "
			"The machine plays with three balls.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			[
				("outhole", "Outhole", _matrix(28), "Drained-ball catch position."),
				("trough-1", "Trough, 1 ball", _matrix(25), "One ball in the trough."),
				("trough-2", "Trough, 2 balls", _matrix(26), "Two balls in the trough."),
				("trough-3", "Trough, 3 balls", _matrix(27), "Three balls in the trough."),
			],
			"A-8039-3",
		),
		_mechanism(
			"shooter-lane",
			"Shooter lane and ball feeder",
			"kicker",
			[_coil(2)],
			_matrix(17, 34),
			"There is no manual plunger: the Launch Ball cabinet button (switch 34, lamp 87) asks the ROM to fire the Ball Shooter "
			"Lane Feeder (C-9638, solenoid 2) while a ball rests on the shooter-lane switch (17). The retained script writes "
			"Controller.Switch(34) from the plunger key.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None,
			"C-9638",
		),
		_mechanism(
			"lower-right-flipper",
			"Lower right flipper",
			"other",
			[_coil(45), _coil(46)],
			["switch.generic-111", "switch.generic-112"],
			"Fliptronic II flipper assembly A-15205-R-4 with a SW-1A-193 end-of-stroke leaf switch (F1, public 111) and an FL-15411 "
			"coil with power and hold windings (solenoids 45 and 46, Q4/Q11). The cabinet button is the opto on the Flipper Opto "
			"Board A-15894 (F2, public 112). PinMAME synthesizes the end-of-stroke bit; the T.1 run showed the ROM firing the "
			"flipper when 112 was set to 1.",
			flipper_refs,
			None,
			"A-15205-R-4",
		),
		_mechanism(
			"lower-left-flipper",
			"Lower left flipper",
			"other",
			[_coil(47), _coil(48)],
			["switch.generic-113", "switch.generic-114"],
			"Fliptronic II flipper assembly A-15205-L-4 with a SW-1A-193 end-of-stroke leaf switch (F3, public 113) and an FL-15411 "
			"coil with power and hold windings (solenoids 47 and 48, Q3/Q9). The cabinet button is the second opto of the "
			"Flipper Opto Board A-15894 (F4, public 114).",
			flipper_refs,
			None,
			"A-15205-L-4",
		),
		_mechanism(
			"upper-left-flipper",
			"Upper left flipper",
			"other",
			[_coil(35), _coil(36)],
			["switch.generic-117", "switch.generic-118"],
			"An upper-left flipper (assembly A-16090-L-4) with its own SW-1A-193 end-of-stroke "
			"switch (F7, public 117) and an FL-15411 coil (solenoids 35 and 36, Q1/Q5). The cabinet side of F8 (public 118) is "
			"the same left opto board as the lower left flipper; the retained script's left key activates it. There is no "
			"upper right flipper: F5/F6 and solenoids 33/34 are PinMAME positions with nothing fitted.",
			flipper_refs,
			None,
			"A-16090-L-4",
		),
		_mechanism(
			"slingshots",
			"Slingshots",
			"kicker",
			[_coil(9), _coil(10)],
			_matrix(15, 16),
			"Two kicker-arm assemblies (B-12665) with the B-11203-R-1 coil and bracket each sit above a leaf kick switch (15 left, 16 "
			"right) and a coil (solenoids 9 and 10).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None,
			"B-8284-1",
		),
		_mechanism(
			"jet-bumpers",
			"Jet bumpers",
			"other",
			[_coil(11), _coil(12), _coil(13)],
			_matrix(61, 62, 63),
			"Three B-9414-3 jet bumpers, each with an A-9415-2 coil assembly (solenoids 11, 12, 13) and a leaf switch (61 left, 62 "
			"right, 63 bottom) on a #555 bulb socket. The ROM counts hits per bumper and reports 'Examine ... Jet Bumper Switch' "
			"when one is abnormally low; building 'Transmat power' by hitting them is a game rule.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None,
			"B-9414-3",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	return []


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
MANUAL_NAME = "Bally_1992_Doctor_Who_Manual.pdf"
HANDY_NAME = "Bally_1992_Doctor_Who_Handy_Technician_s_Chart_includes_Fuse_List.pdf"
AMENDMENT_NAME = "Bally_1992_11_04_Doctor_Who_Manual_Amendment.pdf"
TABLE_NAME = "Doctor Who (Bally 1992) VPW Mod v1.1.vpx"
MANUALS_DIRECTORY = "pinmame-manuals/by-machine/bally.doctor-who.1992/ipdb-738"
IPDB_WAYBACK = "https://web.archive.org/web/20250108052856id_/https://www.ipdb.org/machine.cgi?id=738"
RIGHTS_NOTE = "Bally/Midway; scan hosted by the Internet Pinball Machine Database"
EXCERPT_CREDIT = "curator, read from the rendered page"


def _excerpt(name: str, locator: str, *, image: str | None = None, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.doctor-who.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if image is not None:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = image
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_derivation(file: str, page: int, box: str, xref: int, width: int, dpi: int, capped: int | None, size: str) -> str:
	cap = f", capped to {capped}px wide" if capped else ""
	return (
		f"{file} page {page}, crop box {box}, scanned page rendered at its native resolution (embedded image xref {xref}, "
		f"{width}px across 8.50in), rendered at {dpi} dpi{cap}, grayscale, {size} WebP quality 80"
	)


def _manual_excerpts() -> list[dict[str, Any]]:
	m = MANUAL_NAME
	return [
		_excerpt("switch-locations", "PDF page 119, printed 2-46, Switch Locations parts list and playfield drawing",
			image=_manual_derivation(m, 119, "0.06,0.05,0.98,0.95", 628, 2550, 300, None, "2346x2970")),
		_excerpt("lamp-locations", "PDF page 118, printed 2-45, Lamp Locations parts list and playfield drawing",
			image=_manual_derivation(m, 118, "0.06,0.05,0.98,0.95", 623, 2550, 300, None, "2346x2970")),
		_excerpt("solenoid-flasher-locations", "PDF page 120, printed 2-47, Solenoid/Flasher Locations parts list and playfield drawing",
			image=_manual_derivation(m, 120, "0.06,0.05,0.98,0.95", 633, 2550, 300, None, "2346x2970")),
		_excerpt("switch-matrix", "PDF page 126, printed 3-3, Switch Matrix with the dedicated and flipper grounded-switch blocks",
			image=_manual_derivation(m, 126, "0.05,0.07,0.95,0.53", 665, 2550, 131, 1000, "1001x663")),
		_excerpt("lamp-matrix", "PDF page 125, printed 3-2, Lamp Matrix wiring table",
			image=_manual_derivation(m, 125, "0.14,0.045,0.83,0.55", 660, 2550, 145, 850, "851x806")),
		_excerpt("solenoid-flasher-table", "PDF page 128, printed 3-5, Solenoid/Flasher Table with the general-illumination and flipper-circuit rows",
			image=_manual_derivation(m, 128, "0.12,0.055,0.88,0.5", 677, 2550, 108, 700, "701x531")),
		_excerpt("power-driver-board-connectors", "PDF pages 143-145, printed 3-20 to 3-22, Power Driver Board A-12697-1 connector list (image: page 145)",
			image=_manual_derivation(m, 145, "0.05,0.04,0.95,0.97", 765, 2550, 111, 850, "851x1138")),
		_excerpt("flipper-opto-wiring", "PDF pages 132-134, printed 3-9 to 3-11, Flipper Opto Switch Board A-15894 and the Fliptronic II flipper circuits (image: page 132)",
			image=_manual_derivation(m, 132, "0.05,0.04,0.95,0.72", 698, 2550, 300, None, "2296x2244")),
		_excerpt("opto-boards-and-mini-playfield-wiring", "PDF pages 135, 137 and 138, printed 3-12, 3-14 and 3-15, Opto Switch 10 PCB, Bi-directional Motor Drive and Mini-playfield Wiring Block Diagram (image: page 135)",
			image=_manual_derivation(m, 135, "0.05,0.05,0.95,0.97", 713, 2550, 300, None, "2296x3036")),
		_excerpt("boards-and-assemblies", "PDF pages 77, 91-109, 113 and 115-117, printed 2-4, 2-19 to 2-36, 2-40, 2-42 and 2-43, backbox, mechanism and playfield parts pages",
			method="mixed", reviewed=False, credit="curator; part-number cells read from OCR text and spot-checked against the renders"),
		_excerpt("game-rules", "PDF pages 9-19, the Game Rules & Playfield Shots section",
			method="mixed", reviewed=False, credit="curator; Windows OCR with obvious character errors corrected"),
		_excerpt("service-tests", "PDF pages 3, 4, 28, 34-39, 65, 66 and 70-72, test menu, error list, opto theory and playfield-adjustment passages",
			method="mixed", reviewed=False, credit="curator; Windows OCR with obvious character errors corrected against the renders"),
	]


def source_records() -> list[dict[str, Any]]:
	def pdf(source_id: str, name: str, locator: str, sha: str, *, excerpts: list[dict[str, Any]] | None = None, acquired: str | None = None, wayback: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": source_id,
			"kind": "manual",
			"uri": f"external:{MANUALS_DIRECTORY}/{name}",
			"original_filename": name,
			"sha256": sha,
			"locator": locator + (f" Direct resource: {wayback}." if wayback else ""),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": RIGHTS_NOTE,
		}
		if acquired:
			record["acquired_at"] = acquired
		if excerpts:
			record["excerpts"] = excerpts
		return record

	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the dw_* clone tree (dw_l2, dw_d2, dw_l1, dw_d1, dw_p5, dw_p6)",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/dw.c dwGameData with GEN_WPCFLIPTRON, wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0x07,0x00,0x00,0x00,0x7f,0x01,...} (index 3 is matrix column 3, index 7 column 7 and index 8 column 8 under "
				"wpc_sw2m, so core_setSw inverts public 31, 32, 33, 71-77 and the unoccupied 81: src/wpc/wpc.c wpc_sw2m(no) = "
				"(no/10)*8+(no%10-1), src/wpc/core.c core_setSw XORs the public level with invSw[swNo/8]), FLIP_SW(FLIP_L|FLIP_U) with "
				"FLIP_SOL for the same flippers, no custom solenoids, no wpc_set_fastflip_addr call in init_dw so wpc.c mirrors "
				"WPC_GILAMPS bits 5-7 at solenoids 29-31, the synthetic flipper power/hold outputs at 33-36 and 45-48, "
				"src/wpc/core.h CORE_FIRSTCUSTSOL=51 and CORE_FIRSTUFLIPSOL=33, src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_WPCFLIPTRON=0x8. The runtime runs used a library built from 8371478a."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-fliptronic.json",
			"revision": "repository",
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp and five-GI address rules, including the no-LPDC 37-44 unused range and the Fliptronic flipper block",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=738",
			"revision": "Wayback capture 2025-01-08T05:28:56Z",
			"sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-10-02T00:44:00Z",
			"locator": (
				"IPDB machine 738 'Doctor Who' (Midway/Bally, September 1992, model 20006, Williams WPC Fliptronics 2, 4 players). IPDB is "
				f"Cloudflare-gated, so the page was read from the raw Wayback capture {IPDB_WAYBACK} (retained as ipdb-738-page-wayback.html). "
				"The title, manufacturer, date and model number match the manual's cover and the machine being curated. The page's "
				"Notes record that sample and prototype machines had a motor-driven Dalek head with a front-facing opto that "
				"production machines dropped while leaving 'the wiring and software' in place."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database contributors",
			"excerpts": [
				_excerpt("ipdb-page", f"IPDB machine 738 page, Wayback capture {IPDB_WAYBACK}", method="manual", reviewed=False, credit="curator, read from the retained HTML"),
			],
		},
		pdf(
			MANUAL_SOURCE, MANUAL_NAME,
			"Image-only 300 dpi scan of the Midway/Bally Doctor Who operations manual, model 20006 (IPDB lists it as dated October 1992, "
			"with no schematics). The PDF has no text layer; every table was read from a rendered page and a Windows OCR pass was used only "
			"to find pages. PDF 118-120 (printed 2-45 to 2-47) carry the lamp, switch and solenoid/flasher location lists, PDF 125-128 "
			"(3-2 to 3-5) the lamp matrix, switch matrix and solenoid/flasher table, PDF 132-138 (3-9 to 3-15) the Fliptronic II and opto "
			"boards, PDF 143-145 (3-20 to 3-22) the Power Driver Board connector list. PDF 150 is a foldout reprint of the two matrices.",
			MANUAL_SHA256,
			excerpts=_manual_excerpts(),
			acquired="2026-10-02T00:44:00Z",
			wayback="https://web.archive.org/web/20251203172610id_/https://www.ipdb.org/files/738/" + MANUAL_NAME,
		),
		pdf(
			HANDY_SOURCE, HANDY_NAME,
			"One-page born-digital Handy Technician's Chart (fuse list, solenoid/flasher table, lamp matrix and switch matrix) printed "
			"as a separately compiled copy of the same machine data; it shades the optos and prints numbered flipper circuits 29-36.",
			HANDY_SHA256,
			excerpts=[
				_excerpt(
					"handy-technician-chart", "Single page, solenoid/flasher, lamp and switch tables",
					image=(
						f"{HANDY_NAME} page 1, crop box 0.53,0.47,1,0.97, born-digital page rendered for legibility (smallest type in "
						"region 4.0pt, targeting 11px glyphs), rendered at 125 dpi, capped to 1000px wide, grayscale, 1001x689 WebP quality 80"
					),
				)
			],
			wayback="https://web.archive.org/web/20231021004812id_/https://www.ipdb.org/files/738/" + HANDY_NAME,
		),
		pdf(
			AMENDMENT_SOURCE, AMENDMENT_NAME,
			"Manual Amendment 16-9453 dated November 4, 1992: two new game adjustments (A.2 54 Kick Lock Holes, A.2 55 Game Start Doctor) "
			"and the mini-playfield cant correction. It changes no printed switch, lamp or solenoid cell.",
			AMENDMENT_SHA256,
			excerpts=[
				_excerpt(
					"manual-amendment", "Single page, game adjustments and mini-playfield cant repair",
					image=(
						f"{AMENDMENT_NAME} page 1, crop box 0,0,1,0.55, scanned page rendered at its native resolution (embedded image xref 11, "
						"1126px across 7.51in), rendered at 150 dpi, grayscale, 1275x907 WebP quality 80"
					),
				)
			],
			wayback="https://web.archive.org/web/20231021004813id_/https://www.ipdb.org/files/738/" + AMENDMENT_NAME,
		),
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/bally/doctor-who-1992/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME,
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW Mod v1.1 recreation of the physical machine. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT}. Geometry authority only for "
				"named table objects: the mini-playfield, its lamps and the Doctor lamps are modelled at a fixed playfield position."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/doctor-who-1992/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (176,146 bytes). Runtime and mechanism-causality authority: Const cGameName = "dw_l2" (the '
				"production parent driver), Const UseSolenoids = 2 (fast flips), the SolCallback/SolModCallback table for the coils and "
				"flashers, the mini-playfield cvpmMech (sol1 = 28, sol2 = 27, 360 steps, UpdateMiniPF deriving switch 32), and the "
				"trap-door and Tardis routines that set switches 57 and 31."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/doctor-who-1992/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": EDGES_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{EVIDENCE_DIRECTORY}/doctor-who-dw_l2-switch-edges.json",
			"revision": PINMAME_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of dw_l2 from empty NVRAM with built-in mechanisms disabled (scenario "
				"tools/harness-scenarios/wpc-fliptronic/dw-switch-edges-optos.json) that opens the ROM's T.1 SWITCH EDGES test and sets "
				"public 41, 78, 57, 47, 82, 68, 88, 38, 112, 114 and the ten opto addresses 31-33 and 71-77 to 1 and then 0. The ROM's "
				"top line names each switch while its public level is 1, except 32, which it names at public 0, the mixed-level exception "
				"PinMAME's inverted-switch mask produces."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": SOLENOID_TEST_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{EVIDENCE_DIRECTORY}/doctor-who-dw_l2-solenoid-test.json",
			"revision": PINMAME_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of dw_l2 from empty NVRAM (scenario tools/harness-scenarios/wpc-fliptronic/"
				"dw-solenoid-test.json) that steps T.4 SOLENOID TEST through solenoids 1-5, 7, 9-13, 15, 16 and 25 in repeat mode; each "
				"step names the solenoid and its wires and pulses that public address."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": FLASHER_TEST_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{EVIDENCE_DIRECTORY}/doctor-who-dw_l2-flasher-test.json",
			"revision": PINMAME_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of dw_l2 from empty NVRAM (scenario tools/harness-scenarios/wpc-fliptronic/"
				"dw-flasher-test.json) that steps T.5 FLASHER TEST through the flashers 6, 8, 14 and 17-24 in repeat mode. At step 19 the ROM "
				"pulses public solenoid 19 and prints 5x3 Right/Right with the wires BLK-ORN RED-WHT."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": MINI_PLAYFIELD_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{EVIDENCE_DIRECTORY}/doctor-who-dw_l2-mini-playfield-test.json",
			"revision": PINMAME_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of dw_l2 from empty NVRAM with built-in mechanisms disabled (scenario "
				"tools/harness-scenarios/wpc-fliptronic/dw-mini-playfield-test.json) that starts T.14 MINI-PLAYFIELD TEST, confirms its "
				"warning and holds both flipper buttons (112 and 114). Sub-test 1 drives the motor (28) and then the direction line (27) "
				"with it, sub-test 2 kicks the left and right ejects (4, 5) and sub-test 3 flashes the mini-playfield flasher (17)."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": CALLOUT_SOURCE,
			"kind": "human_review",
			"uri": "internal:tools/seeds/bally/doctor-who-1992-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-02 factory location-drawing callout check of PDF 118, 119 and 120 (printed 2-45 to 2-47): every callout transcribed "
				"independently on the retained 300 dpi renders, per-page control and callout fits; a table placement whose own callout lands "
				"within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays and generator are retained "
				"under review-artifacts with a pinned manifest."
			),
			"license": "NOASSERTION",
			"attribution": "PinMAME game definitions contributors",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Doctor Who",
			"manufacturer": "Bally",
			"year": 1992,
			"kind": "physical_pinball",
			"ipdb_id": 738,
			"opdb_id": "G4x2Y-MQwwe",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
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
		"controller": {
			"platform": "pinmame.wpc-fliptronic",
			"hardware_generation": "0x8",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/doctor-who-1992.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Doctor Who device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Doctor Who mechanism {mechanism['id']} names unknown devices: {unknown}")
	drawing_callouts.apply_to_definition(definition, load_json(CALLOUT_SEED_PATH), CALLOUT_SOURCE)
	return definition


# --- Spatial report ------------------------------------------------------------------------------------
def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	devices = definition["inputs"] + definition["outputs"]
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable = 0
	for device in devices:
		spatial = device.get("spatial")
		if spatial is None:
			if device["availability"] in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable += 1
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
			"x": f"x/{PLAYFIELD_WIDTH}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"handy_chart_sha256": HANDY_SHA256,
			"spatial_seed_sha256": _file_sha256(SPATIAL_SEED_PATH),
			"callout_seed_sha256": _file_sha256(CALLOUT_SEED_PATH),
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/doctor-who-1992/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/bally/doctor-who-1992-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": "Exact-name VPX collision object centre for the matrix switch, observed, and validated where the factory drawing's own callout agrees within the limit; switch 32 (the Home Opto, which the table models in software) is measured on the drawing instead.",
			"lamp": "Exact VPX Light centre for each lamp's playfield bulb, observed, validated where the lamp drawing's callout agrees. Lamp 67 has no table Light and is measured on the drawing. Second bulbs on the speaker panel and back panel are not placed.",
			"solenoid": "Named VPX mechanism anchor or visible effect projection, observed, validated where the solenoid/flasher drawing's own callout agrees; coils 27 and 28 have no table object and are measured on the drawing. Flipper windings print no callout and keep their table placements observed.",
			"gi": "Per-string collections of table GI lights, collapsed where bulbs are stacked, observed only: the manual prints no per-string bulb count and no drawing locates GI bulbs, so none of these placements can be validated.",
		},
		"unresolved_geometry": [
			"The general-illumination bulb coordinates of strings 3-5 rest on the retained table's own grouping; no factory drawing or bulb count locates them, so their placements stay observed and spatial_placement stays in coverage.missing.",
			"The mini-playfield is modelled at a fixed playfield position; its lamps 56-58, the Doctor 7 flasher and the lock-hole switches 76-77 travel with it, so a playfield coordinate describes the lowest-level position only.",
			"Hidden mechanism contacts (trough, end-of-stroke, trap-door, reel-like cam optos) have whole-mechanism projections, not contact centres.",
		],
		"promotion_decision": "partial: every used device has a placement or a controlled not-applicable record, and the factory drawings validate most table placements, but the general-illumination bulbs cannot be validated from any retained drawing or count.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	lines = [
		"# Doctor Who (Bally, 1992) spatial blockers",
		"",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest "
		f"`{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.",
		"",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT} rounded to at most six places "
		"(factory-drawing measurements to three).",
		"",
		"## Placement status",
		"",
	]
	for name, items in report["placement_status"].items():
		lines.append(f"- `{name}`: {len(items)} devices")
	lines += [
		f"- controlled `not_applicable` records: {report['not_applicable_device_count']}",
		f"- used devices with no placement record: {len(report['without_placements'])}",
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
		raise RuntimeError(f"Refusing to overwrite an author-ready Doctor Who artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Doctor Who author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"Doctor Who deterministic artifact drift: {path}")
	print("Doctor Who definition, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and its generated artifacts")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, knowledge note and spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Doctor Who extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Doctor Who retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
