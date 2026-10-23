"""Curate the physical Bally Creature from the Black Lagoon (1992) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail, runtime-derived
fact and table coordinate as a literal and reads one committed seed (the factory-drawing callout check), so
regeneration reproduces the canonical artifact byte-for-byte without reading the external evidence roots.
``--check`` refuses drift, and ``--regenerate`` is the only path that writes the definition, its pinned seed and its
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

MACHINE_ID = "bally.creature-from-the-black-lagoon.1992"
# Partial: the 32 chase bulbs of the swirl ramp and the bowl cannot be placed on their strings, so lamps 91-98 and G.I.
# 0 and 3 carry no placement, and the manual's chase-board diagram and its parts list disagree on which ramp boards each
# group drives (conflict.chase-light-board-group-assignment).
PARTIAL_PATH = ROOT / "machines/partial/bally/creature-from-the-black-lagoon-1992.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/creature-from-the-black-lagoon-1992.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/creature-from-the-black-lagoon-1992.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/bally/creature-from-the-black-lagoon-1992-callouts.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/creature-from-the-black-lagoon-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/creature-from-the-black-lagoon-1992.md"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/creature-from-the-black-lagoon-1992.md"
EXCERPT_DIRECTORY = f"evidence/excerpts/{MACHINE_ID}"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.bally.creature-from-the-black-lagoon.1992"
PARTS_LIST_SOURCE = "parts-list.bally.creature-from-the-black-lagoon.1992.ipdb"
VPX_TABLE_SOURCE = "vpx-table.cftbl-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.cftbl-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.cftbl-vpw-1-0"
CALLOUT_SOURCE = "drawing-callouts.creature.2026-10-23"
FLASHER_TEST_SOURCE = "runtime.creature.flasher-test"
EDGES_SOURCE = "runtime.creature.switch-edges-fliptronic"
FLIPPER_TEST_SOURCE = "runtime.creature.flipper-coil-test"
RAMP_LIGHTS_SOURCE = "runtime.creature.ramp-lights-test"
SUBWAY_SOURCE = "runtime.creature.subway-awards"
P3_FLASHER_TEST_SOURCE = "runtime.creature.p3.flasher-test"
P3_EDGES_SOURCE = "runtime.creature.p3.switch-edges-fliptronic"
P3_FLIPPER_TEST_SOURCE = "runtime.creature.p3.flipper-coil-test"
P3_RAMP_LIGHTS_SOURCE = "runtime.creature.p3.ramp-lights-test"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-fliptronic"

TABLE_NAME = "Creature from the Black Lagoon (Williams 1992) VPW v1.0.vpx"
TABLE_SHA256 = "960ebdd19b1a0f6d88822add16bbaf8a05d11bd5f1b8b26dc387a6db21705def"
SCRIPT_SHA256 = "110d85325e33cbaf465f5a60f3aeeb2069329c55719435e7b76380748ba70ea6"
MANUAL_NAME = "Creature_From_The_Black_Lagoon_OPS.pdf"
MANUAL_SHA256 = "d84d28a807505339f57676e0222adc6cc6fe7bef7371d31f9a9076ec33021d97"
PARTS_LIST_NAME = "Bally_1992_Creature_from_the_Black_Lagoon_Parts_List.txt"
PARTS_LIST_SHA256 = "17fe20d30906d64655ebb7d5d6e5ba492c84b5d395e604c7ce2d7af9ef012e14"
PARTS_LIST_WAYBACK = "https://web.archive.org/web/20231225170707id_/https://www.ipdb.org/files/588/" + PARTS_LIST_NAME

EXTRACTION_RELATIVE_PATH = Path("bally/creature-from-the-black-lagoon-1992/vpw-1-0/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/creature-from-the-black-lagoon-1992/vpw-1-0/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "bd06526a5fd2c0327964545403eb276fc7be4e982c2b7f1f1e5b065be5752cf9"
EXTRACTION_FILE_COUNT = 3345
EXTRACTION_TOTAL_BYTES = 898771914

PLAYFIELD_WIDTH = 964.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------------------
DRIVER_IDS = ("cftbl_l4", "cftbl_l4c", "cftbl_d4", "cftbl_l3", "cftbl_d3", "cftbl_l2", "cftbl_d2", "cftbl_p3")
DRIVER_COMPATIBILITY = {
	"cftbl_l4": (
		"identical",
		"Bally production L-4 game ROM, PinMAME's parent driver (the catalog year 1993 is the firmware's). The retained known-working "
		'VPW v1.0 table binds it (Const cGameName="cftbl_l4") and every runtime run behind this definition booted it.',
	),
	"cftbl_l4c": (
		"identical",
		"2020 community L-4C 'Competition + LED Ghost MOD' revision of the L-4 ROM for the same physical machine; it changes the rules and "
		"the lamp-matrix timing, not a controller address or a playfield device.",
	),
	"cftbl_d4": ("identical", "Community 'LED Ghost Fix' revision of the L-4 ROM, a lamp-matrix timing correction with no I/O change."),
	"cftbl_l3": ("identical", "Bally production L-3 game ROM, an earlier firmware revision of the same physical machine."),
	"cftbl_d3": ("identical", "Community 'LED Ghost Fix' revision of the L-3 ROM, with no I/O change."),
	"cftbl_l2": ("identical", "Bally production L-2 game ROM, an earlier firmware revision of the same physical machine."),
	"cftbl_d2": ("identical", "Community 'LED Ghost Fix' revision of the L-2 ROM, with no I/O change."),
	"cftbl_p3": (
		"compatible",
		"P-3 prototype game ROM (it identifies itself THE CREATURE 20018 REV. P-3), paired in pinned driver.c with the prototype sound "
		"ROM u18-sp1.rom and sharing cftblGameData. No retained source describes the prototype machines' own hardware, but the ROM "
		"drives this machine's devices: replayed on it, the T.1, T.5, T.12 and T.15 service-test scenarios name and drive the same "
		"public addresses with the same wires as L-4, including the backbox insert flashers 33-36 and the second flipper optos 116 "
		"and 118 (runtime evidence creature-cftbl_p3-*.json). Only display strings differ: T.5 names flasher 2 LFT SUBWAY FLHR and "
		"flasher 11 CREATURE FLSHR, and T.1 names switch 25 P OF PAID.",
	),
}
# The P-3 ROM's names where they differ from L-4's.
P3_T5_NAMES = {2: "LFT SUBWAY FLHR", 11: "CREATURE FLSHR"}

# --- Switches (switch-locations.md, switch-matrix.md) -------------------------------------------------------------
SWITCH_LABELS = {
	13: "Credit/Start Button", 14: "Plumb Bob Tilt", 15: "Top Left Rollover", 16: "Left Subway",
	17: "Center Subway", 18: "Center Shot",
	21: "Slam Tilt", 22: "Coin Door",
	25: "P of P-A-I-D", 26: "A of P-A-I-D", 27: "I of P-A-I-D", 28: "D of P-A-I-D",
	33: "Bottom Jet", 34: "Right Popper", 35: "Right Ramp Enter", 36: "Left Ramp Enter",
	37: "Lower Right Popper", 38: "Ramp Up/Down",
	41: "Cola", 42: "Hot Dog", 43: "Popcorn", 44: "Ice Cream",
	45: "Left Jet", 46: "Right Jet", 47: "Left Slingshot", 48: "Right Slingshot",
	51: "Left Out Lane", 52: "Left Return Lane", 53: "Start Combo", 54: "Right Out Lane",
	55: "Outhole", 56: "Right Trough", 57: "Center Trough", 58: "Left Trough",
	61: "Right Ramp Exit", 62: "Left Ramp Exit", 63: "Center Lane Exit", 64: "Upper Ramp",
	65: "Bowl", 66: "Shooter",
}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 24, 31, 32, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# The Switch Locations list prints an LED (A-14231) over a phototransistor (A-14232) for these two poppers.
OPTO_SWITCHES = {34, 37}
# cftblGameData's inverted-switch mask: column 1 0x10 (switch 15) and column 3 0xc8 (switches 34, 37 and 38).
PINMAME_INVERTED_SWITCHES = {15, 34, 37, 38}
SWITCH_PARTS = {
	13: "20-9663-1", 14: "20-6502-A", 15: "5647-12693-19", 16: "5647-12693-21", 17: "5647-12693-21", 18: "5647-12693-36",
	21: "27-1066", 22: "5643-09288-00", 25: "5647-12693-19", 26: "5647-12693-19", 27: "5647-12693-19", 28: "5647-12693-19",
	33: "SW-11A-37", 34: "A-14231 (LED) with A-14232 (Trans.)", 35: "5647-12693-26", 36: "5647-12693-21",
	37: "A-14231 (LED) with A-14232 (Trans.)", 38: "5647-12693-11", 41: "A-16206-2", 42: "A-16206-2", 43: "A-16206-2",
	44: "A-16206-2", 45: "SW-11A-37", 46: "SW-11A-37", 47: "SW-1A-114", 48: "SW-1A-114",
	51: "5647-12693-19", 52: "5647-12693-19", 53: "5647-12693-19", 54: "5647-12693-19",
	55: "5647-12133-12", 56: "5647-12693-08", 57: "5647-09957-00", 58: "5647-09957-00",
	61: "5647-12693-36", 62: "5647-12693-21", 63: "5647-12693-19", 64: "5647-12693-21", 65: "5647-12693-21", 66: "5647-12693-04",
}
SWITCH_TYPES = {13: "button", 14: "tilt", 21: "tilt", 22: "microswitch", 33: "leaf", 34: "opto", 37: "opto", 41: "leaf", 42: "leaf",
	43: "leaf", 44: "leaf", 45: "leaf", 46: "leaf", 47: "leaf", 48: "leaf", 55: "leaf"}
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
	1: ("Orange-Brown", "J205-1", "U18-11"), 2: ("Orange-Red", "J205-2", "U18-9"),
	3: ("Orange-Black", "J205-3", "U18-5"), 4: ("Orange-Yellow", "J205-4", "U18-7"),
	5: ("Orange-Green", "J205-6", "U19-11"), 6: ("Orange-Blue", "J205-7", "U19-9"),
	7: ("Orange-Violet", "J205-8", "U19-5"), 8: ("Orange-Gray", "J205-9", "U19-7"),
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
CABINET_SWITCHES = {13: ("cabinet.start", "cabinet front"), 14: ("cabinet.tilt", "cabinet interior"), 21: ("cabinet.slam-tilt", "coin door"),
	22: ("cabinet.coin-door", "coin door")}
# What the retained VPW script does for each matrix switch (vpw-script-bindings.md).
SWITCH_SCRIPT = {
	15: "the table's start-up sets it to 1, sw15_Hit writes 0 and sw15_Unhit writes 1",
	16: "sw16_Hit pulses it at the left hole", 17: "sw17_Hit pulses it at the centre hole", 18: "sw18_Hit pulses it",
	33: "Bumper3_Hit pulses it (the lower jet bumper)",
	34: "sw34_Hit sets it and RightUpperKicker (solenoid 1) clears it as it kicks the ball out",
	37: "sw37_Hit sets it and RightLowerKicker (solenoid 3) clears it as it kicks the ball out",
	38: "SolRampUp (solenoid 23) writes 0 and SolRampDown (solenoid 26) writes 1; no table object carries the switch",
	45: "Bumper1_Hit pulses it (the upper left jet bumper)", 46: "Bumper2_Hit pulses it (the upper right jet bumper)",
	47: "LeftSlingShot_Slingshot pulses it", 48: "RightSlingShot_Slingshot pulses it",
	55: "sw55_Hit sets it and sw55_UnHit clears it; SolOuthole (solenoid 12) kicks the ball on into the trough",
	56: "sw56_Hit/_UnHit follow the ball and the table's start-up sets it (three balls in the trough)",
	57: "sw57_Hit/_UnHit follow the ball and the table's start-up sets it",
	58: "sw58_Hit/_UnHit follow the ball and the table's start-up sets it",
	66: "sw66_Hit/_UnHit follow the ball",
}
for _address in (25, 26, 27, 28, 35, 36, 51, 52, 53, 54, 61, 62, 63, 64, 65):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit pulses it"
for _address in (41, 42, 43, 44):
	SWITCH_SCRIPT[_address] = f"sw{_address}_Hit pulses it through STHit (stand-up target)"
SWITCH_NOTES = {
	15: (
		"A micro switch rollover that closes while a ball rolls over it. Pinned PinMAME's cftblGameData marks public 15 inverted "
		"(inverted-switch mask column 1 0x10), so its public level is the complement of the contact: a recreation publishes 1 while no "
		"ball is on the rollover and 0 while one is, the opposite of every other rollover on the machine, as the retained script does."
	),
	16: (
		"The left hole, which awards K-I-S-S (Taillight Park): in a game the ROM flashes K (lamp 21) when public 16 closes and shows the "
		"kissing-couple animation on the next closure. Both the left and the centre hole drop the ball into the subway that feeds the lower "
		"right popper (switch 37)."
	),
	17: "The centre hole, the Snack Bar: in a game the ROM lights the first Snack Bar target lamp (53, Cola) and shows HIT TARGETS TO OPEN SNACKBAR when public 17 closes.",
	18: "The Center Shot switch on the right wall of the centre lane (Move Your Car).",
	22: "Closed while the coin door is closed.",
	34: "The right (upper) popper's opto, the F-I-L-M hole; solenoid 1 kicks the ball back out.",
	37: "The lower right popper's opto at the end of the subway from the left and centre holes; solenoid 3 kicks the ball out.",
	38: (
		"The lift ramp's position switch on the A-16042 Lift Ramp Assembly under the playfield. Public 1 means the ramp is down: the "
		"retained script writes 1 when the down coil (26) fires and 0 when the up coil (23) fires, and pinned cftbl_handleMech sets it "
		"from the same commands. cftblGameData marks public 38 inverted, so the contact the matrix sees closes while the ramp is up."
	),
	53: (
		'The Switch Locations and Switch Matrix pages name it by its rule ("Start Combo"); it is the right return lane, wired and placed as '
		"the mirror of 52 (Left Return Lane)."
	),
	55: "The outhole switch at the left end of the trough; the outhole kicker (solenoid 12) kicks a drained ball from here into the trough.",
	56: "The trough position at the ball release (solenoid 4), which feeds the shooter lane.",
	57: "The middle trough position.",
	58: "The trough position nearest the outhole.",
	62: "The switch at the head of the swirl ramp, where the ramp drawing (printed 2-44) puts the A-15621 ramp's switch.",
	64: "The switch at the top of the upper (Creature) ramp, where the ramp drawing (printed 2-44) puts the A-15622 ramp's switch.",
	65: "The micro switch on the A-15993 bowl assembly; the ball passes it as it circles the bowl.",
	66: "Shooter-lane switch under the ball waiting at the manual plunger.",
}
# Table objects the drawing places elsewhere: why the definition measures the switch on the drawing instead.
TABLE_OFFSETS = {
	18: "The retained table's Trigger sw18 lies across the centre lane, about 0.09 normalized left of the switch that callout 18 marks on the lane's right wall on the switch drawing (printed 2-41).",
	35: "The retained table's Trigger sw35 sits in the right ramp's mouth, about 0.08 normalized from the switch at the ramp's entrance flap that callout 35 marks on the switch drawing (printed 2-41).",
	36: "The retained table's Trigger sw36 sits at the left ramp's mouth on the playfield, about 0.09 normalized below the switch on the ramp that callout 36 marks on the switch drawing (printed 2-41).",
	61: "The retained table's Trigger sw61 sits about 0.08 normalized up and to the right of the switch on the right ramp's descent that callout 61 marks on the switch drawing (printed 2-41).",
	62: "The retained table binds sw62 at the top centre of the ramps, where the switch drawing (printed 2-41) and the ramp drawing (printed 2-44) put switch 64, and sw64 where they put switch 62: the table's two triggers are swapped, a defect of that table.",
	64: "The retained table binds sw64 at the head of the swirl ramp, where both drawings put switch 62 (see switch 62).",
}
DRAWING = "drawing"
# Raw VPX coordinates of the object the retained script binds to each switch, or DRAWING for a drawing measurement.
SWITCH_POSITIONS: dict[int, list[Any]] = {
	15: [(54.88843, 435.2344)], 16: [(185.70245, 895.2191)], 17: [(440.02298, 836.84863)], 18: [DRAWING],
	25: [(506.74835, 211.56068)], 26: [(598.0778, 203.31921)], 27: [(690.0637, 192.31628)], 28: [(781.71173, 181.59569)],
	33: [(596.6361, 582.17413)], 34: [(818.87225, 777.9191)], 35: [DRAWING], 36: [DRAWING], 37: [(802.25464, 1286.8251)],
	38: [DRAWING],
	41: [(174.0728, 1062.7982)], 42: [(174.49063, 992.6859)], 43: [(528.09686, 970.78)], 44: [(547.03046, 1037.8466)],
	45: [(490.05524, 396.90234)], 46: [(703.3054, 396.61447)],
	47: [(217.26187333333334, 1589.8259333333333)], 48: [(659.79007, 1590.6405333333332)],
	51: [(55.075928, 1602.518)], 52: [(127.55868, 1603.0255)], 53: [(749.60803, 1602.383)], 54: [(820.8035, 1601.9904)],
	55: [(453.89474, 2097.9526)], 56: [(785.05237, 1914.9645)], 57: [(729.40393, 1946.2665)], 58: [(675.2189, 1979.2662)],
	61: [DRAWING], 62: [DRAWING], 63: [(404.9699, 161.00128)], 64: [DRAWING], 65: [(810.6823, 1697.7782)],
	66: [(907.2565, 1913.9208)],
}
SWITCH_OBJECTS = {
	15: "Trigger sw15", 16: "Kicker sw16", 17: "Kicker sw17", 25: "Trigger sw25", 26: "Trigger sw26", 27: "Trigger sw27", 28: "Trigger sw28",
	33: "Bumper Bumper3", 34: "Kicker sw34", 37: "Kicker sw37", 41: "HitTarget sw41", 42: "HitTarget sw42", 43: "HitTarget sw43",
	44: "HitTarget sw44", 45: "Bumper Bumper1", 46: "Bumper Bumper2", 47: "Wall LeftSlingShot (centroid of its points)",
	48: "Wall RightSlingShot (centroid of its points)", 51: "Trigger sw51", 52: "Trigger sw52", 53: "Trigger sw53", 54: "Trigger sw54",
	55: "Kicker sw55", 56: "Kicker sw56", 57: "Kicker sw57", 58: "Kicker sw58", 63: "Trigger sw63", 65: "Trigger sw65", 66: "Trigger sw66",
}
# Fliptronic block (switch-matrix.md, fliptronic-ii-board.md, flipper-opto-board.md):
# public -> (label, wire, connector, printed F number, switch type, role, availability).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "Black-Green", "J906-1", "F1", "leaf", "internal.flipper.lower.right.eos", "used"),
	112: ("Lower Right Flipper Button", "Blue-Violet", "J905-1", "F2", "opto", "flipper.lower.right.button", "used"),
	113: ("Lower Left Flipper EOS", "Black-Blue", "J906-3", "F3", "leaf", "internal.flipper.lower.left.eos", "used"),
	114: ("Lower Left Flipper Button", "Blue-Gray", "J905-2", "F4", "opto", "flipper.lower.left.button", "used"),
	115: ("Not Fitted Upper Right Flipper EOS", "Black-Violet", "J906-4", "F5", None, "internal.unused.flipper", "unused"),
	116: ("Right Flipper Button Second Opto", "Black-Yellow", "J905-3", "F6", "opto", "flipper.lower.right.button-second-opto", "used"),
	117: ("Not Fitted Upper Left Flipper EOS", "Black-Gray", "J906-5", "F7", None, "internal.unused.flipper", "unused"),
	118: ("Left Flipper Button Second Opto", "Black-Blue", "J905-5", "F8", "opto", "flipper.lower.left.button-second-opto", "used"),
}

# --- Solenoids (solenoid-flasher-locations.md, solenoid-flasher-wiring.md, power-driver-board-connectors.md) -------
SOLENOID_LABELS = {
	1: "Top Right Popper", 2: "Left Subway Enter Flasher", 3: "Lower Right Popper", 4: "Trough (Ball Release)",
	5: "Right Slingshot", 6: "Left Slingshot", 7: "Knocker", 8: "Bottom Right Flasher",
	9: "Back Flashers", 10: "Bowl Flasher", 11: "Creature Flasher (Insert)", 12: "Outhole",
	13: "Left Jet", 14: "Right Jet", 15: "Bottom Jet", 16: "Right Popper Slide Flasher",
	17: "Bottom Left Flasher", 18: "Right Ramp Flasher", 19: "Left Ramp Flasher",
	20: "Sequential G.I. #1 Select", 21: "Hologram Push Motor", 22: "Center Hole Flasher",
	23: "Up/Down Ramp (Up)", 24: "Sequential G.I. #2 Select", 25: "Start Movie Flashers",
	26: "Up/Down Ramp (Down)", 27: "Creature Mirror Motor", 28: "Hologram Lamp",
	33: "Creature Insert Flasher 1", 34: "Creature Insert Flasher 2", 35: "Creature Insert Flasher 3", 36: "Creature Insert Flasher 4",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC State Bit 29 (GILAMPS bit 5)", 30: "WPC State Bit 30 (GILAMPS bit 6)", 31: "WPC State Bit 31 (GILAMPS bit 7)",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Output 37", 38: "Unused WPC-Fliptronic Output 38", 39: "Unused WPC-Fliptronic Output 39",
	40: "Unused WPC-Fliptronic Output 40", 41: "Unused WPC-Fliptronic Output 41", 42: "Unused WPC-Fliptronic Output 42",
	43: "Unused WPC-Fliptronic Output 43", 44: "Unused WPC-Fliptronic Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
SOLENOID_KINDS = {
	1: "coil", 2: "flasher", 3: "coil", 4: "coil", 5: "coil", 6: "coil", 7: "coil", 8: "flasher", 9: "flasher", 10: "flasher",
	11: "flasher", 12: "coil", 13: "coil", 14: "coil", 15: "coil", 16: "flasher", 17: "flasher", 18: "flasher", 19: "flasher",
	20: "control_signal", 21: "motor", 22: "flasher", 23: "coil", 24: "control_signal", 25: "flasher", 26: "coil", 27: "motor",
	28: "flasher", 33: "flasher", 34: "flasher", 35: "flasher", 36: "flasher", 45: "coil", 46: "coil", 47: "coil", 48: "coil",
}
# address -> (printed type, driver, drive connection, drive wire, voltage connection, part / flashlamp) from the
# Solenoid/Flasher Table; flashers with a backbox insert print a second drive connection.
SOLENOID_TABLE = {
	1: ("High Power", "Q82", "J130-1", "Vio-Brn", "J107-3", "AE-23-800"),
	2: ("High Power", "Q80", "J130-2 / J132-2 (insert)", "Vio-Red", "J107-5 / J106-5 (insert)", "#89, #906 (2) insert"),
	3: ("High Power", "Q78", "J130-4", "Vio-Org", "J107-3", "AE-26-1200"),
	4: ("High Power", "Q76", "J130-5", "Vio-Yel", "J107-3", "AE-26-1200"),
	5: ("High Power", "Q64", "J130-6", "Vio-Grn", "J107-3", "AE-27-1200"),
	6: ("High Power", "Q66", "J130-7", "Vio-Blu", "J107-3", "AE-27-1200"),
	7: ("High Power", "Q68", "J130-8", "Vio-Blk", "J107-3", "AE-23-800"),
	8: ("High Power", "Q70", "J130-9 / J131-5 (insert)", "Vio-Gry", "J107-5 / J106-5 (insert)", "#89, #906 (2) insert"),
	9: ("Low Power", "Q58", "J127-1", "Brn-Blk", "J107-6", "#89 (2)"),
	10: ("Low Power", "Q56", "J127-3 / J129-2 (insert)", "Brn-Red", "J107-6 / J106-5 (insert)", "#89, #906 (2) insert"),
	11: ("Low Power", "Q54", "J129-4 (insert)", "Brn-Org", "J106-5 (insert)", "#906 (2) insert"),
	12: ("Low Power", "Q52", "J127-5", "Brn-Yel", "J107-2", "AE-27-1200"),
	13: ("Low Power", "Q50", "J127-6", "Brn-Grn", "J107-2", "AE-26-1200"),
	14: ("Low Power", "Q48", "J127-7", "Brn-Blu", "J107-2", "AE-26-1200"),
	15: ("Low Power", "Q46", "J127-8", "Brn-Vio", "J107-2", "AE-26-1200"),
	16: ("Low Power", "Q44", "J127-9 / J128-5 (insert)", "Brn-Gry", "J107-5 / J106-5 (insert)", "#89, #906 (2) insert"),
	17: ("Flasher", "Q42", "J126-1 / J125-1 (insert)", "Blk-Brn", "J107-5 / J106-5 (insert)", "#89, #906 (1) insert"),
	18: ("Flasher", "Q40", "J126-2 / J125-2 (insert)", "Blk-Red", "J107-5 / J106-5 (insert)", "#89, #906 (2) insert"),
	19: ("Flasher", "Q38", "J126-3 / J125-3 (insert)", "Blk-Org", "J107-5 / J106-5 (insert)", "#89, #906 (2) insert"),
	20: ("Flasher", "Q36", "J126-4", "Blk-Yel", "J118-2", "#86"),
	21: ("Flasher", "Q28", "J126-5", "Blu-Grn", "J104-1,2", "14-7977 48VAC"),
	22: ("Flasher", "Q30", "J126-6 / J125-7 (insert)", "Blu-Blk", "J107-6 / J106-5 (insert)", "#89, #906 (2) insert"),
	23: ("Low Power", "Q34", "J126-7", "Blu-Vio", "J107-1", "SM1-2B-900-DC"),
	24: ("Low Power", "Q32", "J126-8", "Blu-Gry", "J118-2", "#86"),
	25: ("Flasher", "Q26", "J122-1", "Blu-Brn", "J107-6", "#89 (2)"),
	26: ("Flasher", "Q24", "J122-2", "Blu-Red", "J107-1", "AE-26-1200"),
	27: ("Flasher", "Q22", "J123-4", "Blu-Org", "J104-1,2", "14-7977 48VAC"),
	28: ("Flasher", "Q20", "J123-5", "Blu-Yel", "J118-2", "#1156"),
}
SOLENOID_ASSEMBLIES = {
	1: "A-15769", 2: "A-8798", 3: "A-15842", 4: "B-9362-L-2", 5: "A-14369-R", 6: "A-14369-L", 7: "B-10686-1", 8: "A-8798",
	9: "A-8798", 10: "A-9359", 12: "A-8039-3", 13: "A-9415-2", 14: "A-9415-2", 15: "A-9415-2", 16: "A-8798", 17: "A-8798",
	18: "A-8798", 19: "A-8798", 20: "A-15541", 21: "A-15988", 22: "A-8798", 23: "A-16042", 24: "A-15541", 25: "A-9302",
	26: "A-16042", 27: "A-15988", 28: "A-15857",
}
# Flashlamp count per flasher: playfield bulbs and backbox insert bulbs as the Solenoid/Flasher Table prints them.
FLASHER_BULBS = {2: (1, 2), 8: (1, 2), 9: (2, 0), 10: (1, 2), 11: (0, 2), 16: (1, 2), 17: (1, 1), 18: (1, 2), 19: (1, 2),
	22: (1, 2), 25: (2, 0)}
SOLENOID_SCRIPT = {
	1: "RightUpperKicker kicks the ball out of sw34", 2: "SolModCallBack Flasher2 drives Light f2",
	3: "RightLowerKicker kicks the ball out of sw37", 4: "SolRelease kicks the ball out of sw56",
	8: "SolModCallBack Flasher8 drives Light f8", 9: "SolModCallBack Flasher9 drives Lights f9 and f9b",
	10: "SolModCallBack Flasher10 drives Light f10", 11: "SolModCallBack Flasher11 drives Light f11, which sits off the playfield",
	12: "SolOuthole kicks the ball out of sw55", 16: "SolModCallBack Flasher16 drives Light f16",
	17: "SolModCallBack Flasher17 drives Light f17", 18: "SolModCallBack Flasher18 drives Light f18",
	19: "SolModCallBack Flasher19 drives Light f19", 20: "SolCallBack stores the decoder bit (ChaseLightBit1=)",
	22: "SolModCallBack Flasher22 drives Light f22", 23: "SolRampUp raises the lift ramp (LRampF) and writes switch 38 = 0",
	24: "SolCallBack stores the decoder bit (ChaseLightBit2=)", 25: "SolModCallBack Flasher25 drives Lights f25 and f25b",
	26: "SolRampDown lowers the lift ramp and writes switch 38 = 1", 27: "CreatureMotorMirror runs the hologram animation",
	28: "HoloLamp shows the hologram image", 33: "SolModCallBack Flasher33 drives Light f33, which sits off the playfield",
	34: "SolModCallBack Flasher34 drives Light f34, off the playfield", 35: "SolModCallBack Flasher35 drives Light f35, off the playfield",
	36: "SolModCallBack Flasher36 drives Light f36, off the playfield",
	45: "core.vbs sLRFlipper drives SolRFlipper", 47: "core.vbs sLLFlipper drives SolLFlipper",
}
# T.5 FLASHER TEST (runtime evidence creature-cftbl_l4-flasher-test.json): public -> (ROM name, ROM wires).
T5_NAMES = {
	2: ("LFT SUBWAY FLSHR", "VIO-RED"), 8: ("BOTM RGHT FLSHR", "VIO-GRY"), 9: ("BACK FLASHERS", "BRN-BLK"),
	10: ("BOWL FLASHER", "BRN-RED"), 11: ("3D FLSHR", "BRN-ORN"), 16: ("R. POPPER FLSHR", "BRN-GRY"), 17: ("BOTM LFT FLSHR", "BLK-BRN"),
	18: ("RGHT RAMP FLSHR", "BLK-RED"), 19: ("LFT RMP FLSHR", "BLK-ORN"), 22: ("CNTR HOLE FLSHR", "BLU-BLK"),
	25: ("START MOVIE FL.", "BLU-BRN"), 33: ("CREATURE FL. 1", "BLK-YEL"), 34: ("CREATURE FL. 2", "ORN-VIO"),
	35: ("CREATURE FL. 3", "BLK-BLU"), 36: ("CREATURE FL. 4", "ORN-GRY"),
}
# Fliptronic II J902 lines of the upper-flipper circuits, printed "to insert flashers" (fliptronic-ii-board.md).
INSERT_FLASHER_LINES = {33: ("J902-6", "Black-Yellow"), 34: ("J902-4", "Orange-Violet"), 35: ("J902-3", "Black-Blue"), 36: ("J902-1", "Orange-Gray")}
# Flipper Circuits table and Fliptronic II connector list: public -> (stage, side, J902 pin, control wire, J907 supply,
# supply wire, printed transistors, coil, assembly, ROM name, ROM wires).
FLIPPER_COILS = {
	45: ("power", "lower right", "J902-13", "Blue-Violet", "J907-1,2", "Blue-Yellow", "Q3 (power) / Q9 (holding)", "FL-11629", "A-15205-R-2", "R. FLIP. POWER", "BLU-VIO BLU-YEL"),
	46: ("hold", "lower right", "J902-11", "Orange-Green", "J907-1,2", "Blue-Yellow", "Q3 (power) / Q9 (holding)", "FL-11629", "A-15205-R-2", "R. FLIP. HOLD", "ORN-GRN BLU-YEL"),
	47: ("power", "lower left", "J902-9", "Blue-Gray", "J907-4,5", "Gray-Yellow", "Q2 (power) / Q7 (holding)", "FL-15411", "A-15205-L-4", "L. FLIP. POWER", "BLU-GRY GRY-YEL"),
	48: ("hold", "lower left", "J902-7", "Orange-Blue", "J907-4,5", "Gray-Yellow", "Q2 (power) / Q7 (holding)", "FL-15411", "A-15205-L-4", "L. FLIP. HOLD", "ORN-BLU GRY-YEL"),
}
SOLENOID_NOTES = {
	1: "The upper right popper (A-15769, the F-I-L-M hole): kicks a ball resting on opto 34 back to the playfield.",
	2: "Left subway entrance flasher dome on the left of the playfield with two #906 bulbs on the backbox insert.",
	3: "The lower right popper (A-15842): kicks the ball the subway delivers onto opto 37 back to the playfield.",
	4: "Ball release coil and bracket (B-9362-L-2) at the trough's exit end: releases the ball on switch 56 into the shooter lane.",
	5: "Right slingshot kicker (A-14369-R); kick switch 48.",
	6: "Left slingshot kicker (A-14369-L); kick switch 47.",
	7: "Knocker (B-10686-1), marked '*Not shown' on the Locations list: cabinet-mounted.",
	9: "The two back flashers in the top left and top right corners of the playfield (the Locations list prints 'Top Left & Right Flashers', two #89).",
	10: "The bowl flasher (A-9359) at the whirlpool bowl, with two #906 bulbs on the backbox insert.",
	11: "The Locations list prints it 'Hologram Creature Flasher (Insert)' with two #906 bulbs and no playfield entry: both bulbs are on the backbox insert.",
	12: "Outhole kicker (A-8039-3) under the trough's outhole end: kicks a drained ball from switch 55 into the trough.",
	13: "Top left jet bumper coil (A-9415-2); scoring switch 45.",
	14: "Top right jet bumper coil (A-9415-2); scoring switch 46.",
	15: "Bottom jet bumper coil (A-9415-2); scoring switch 33.",
	16: "The flasher beside the right popper's slide; the Solenoid/Flasher Table names it 'Right Popper Flasher'.",
	20: (
		"Not a coil or a bulb: select line DRIV. 1 of the Chase Light II board A-15541 under the playfield. The board's 2N4403 Q18 turns "
		"the driver's low into a high on the A inputs of both halves of a 74LS139 decoder, so solenoids 20 and 24 choose which of each "
		"group's four chase strings goes dark (see lamps 91-98). The Solenoid/Flasher Table prints it 'Flasher' with part '#86', the chase "
		"bulbs' type; the Power Driver Board connector list sends it to the board's J2-2, where the chase board's own page puts it on J2-1."
	),
	21: "The hologram push motor (14-7977, 48 VAC) of the A-15988 motor and cable assembly, under the playfield ('†Located under playfield').",
	23: (
		"The up coil (SM1-2B-900-DC) of the A-16042 Lift Ramp Assembly under the playfield at the head of the left ramp; a DC coil with a "
		"tieback diode (Solenoid/Flasher Table footnote ** J126-12, Violet-Green)."
	),
	24: (
		"Not a coil or a bulb: select line DRIVE. 2 of the Chase Light II board (2N4403 Q17 to the B inputs of both 74LS139 halves). The "
		"Solenoid/Flasher Table prints it 'Low Power' with part '#86'; the Power Driver Board connector list sends it to the board's J2-1, "
		"where the chase board's own page puts it on J2-2."
	),
	25: "The two Start Movie flashers, one on each lane wall above the inlanes (two #89 on the playfield, no insert bulb).",
	26: "The down coil (AE-26-1200) of the A-16042 Lift Ramp Assembly, with a tieback diode (footnote * J122-6, Violet-Green).",
	27: "The hologram's mirror motor (14-7977, 48 VAC) in the cabinet bottom ('ΔLocated in cabinet bottom').",
	28: "The hologram lamp (#1156, A-15857) in the cabinet bottom ('ΔLocated in cabinet bottom'); it lights the image the mirror projects into the playfield window.",
}
SOLENOID_ROLES = {7: "cabinet.knocker", 11: "cabinet.insert-panel", 27: "cabinet.hologram", 28: "cabinet.hologram",
	33: "cabinet.insert-panel", 34: "cabinet.insert-panel", 35: "cabinet.insert-panel", 36: "cabinet.insert-panel"}
# Raw VPX coordinates of the object each solenoid's placement takes, or DRAWING.
SOLENOID_POSITIONS: dict[int, list[Any]] = {
	1: [(818.87225, 777.9191)], 2: [(109.28775, 738.3097)], 3: [(802.25464, 1286.8251)], 4: [(785.05237, 1914.9645)],
	5: [(659.79007, 1590.6405333333332)], 6: [(217.26187333333334, 1589.8259333333333)], 8: [(827.8641, 1143.0247)],
	9: [(72.48907, 67.832504), (896.9054, 93.02302)], 10: [(759.11017, 1795.496)], 12: [(453.89474, 2097.9526)],
	13: [(490.05524, 396.90234)], 14: [(703.3054, 396.61447)], 15: [(596.6361, 582.17413)], 16: [(821.42303, 620.17896)],
	17: [(53.041885, 1268.9775)], 18: [(682.303, 867.28876)], 19: [(178.98378, 419.1753)], 21: [DRAWING],
	22: [(529.44226, 781.6267)], 23: [DRAWING], 25: [(52.712185, 942.5067), (820.017, 940.5652)], 26: [DRAWING],
	45: [(605.09, 1839.0)], 46: [(605.09, 1839.0)], 47: [(271.7546, 1839.0)], 48: [(271.7546, 1839.0)],
}
SOLENOID_OBJECTS = {
	1: "the popper Kicker sw34 the coil kicks from (projection)", 2: "Light f2", 3: "the popper Kicker sw37 (projection)",
	4: "the trough-exit ball seat Kicker sw56 the coil kicks from (projection)", 5: "Wall RightSlingShot (centroid of its points)",
	6: "Wall LeftSlingShot (centroid of its points)", 8: "Light f8", 9: "Lights f9 (left) and f9b (right)", 10: "Light f10",
	12: "the outhole ball seat Kicker sw55 the kicker strikes (projection)", 13: "Bumper Bumper1", 14: "Bumper Bumper2",
	15: "Bumper Bumper3", 16: "Light f16", 17: "Light f17", 18: "Light f18", 19: "Light f19", 22: "Light f22",
	25: "Lights f25 (left) and f25b (right)", 45: "Flipper RightFlipper's pivot", 46: "Flipper RightFlipper's pivot",
	47: "Flipper LeftFlipper's pivot", 48: "Flipper LeftFlipper's pivot",
}

# --- Lamps (lamp-locations.md, lamp-matrix.md) ----------------------------------------------------------------------
LAMP_LABELS = {
	11: "(P)-A-I-D", 12: "P-(A)-I-D", 13: "P-A-(I)-D", 14: "P-A-I-(D)", 15: "Left Jet", 16: "Right Jet", 17: "Bottom Jet", 18: "Admit One",
	21: "(K)-I-S-S", 22: "K-(I)-S-S", 23: "K-I-(S)-S", 24: "K-I-S-(S)", 25: "10 Million", 26: "20 Million", 27: "30 Million", 28: "Specials",
	31: "Start Mega Menu", 32: "Playground Award", 33: "Lite Big Millions", 34: "Slide", 35: "Right Search", 36: "Right Video",
	37: "Right Start Movie", 38: "Mega Menu",
	41: "Lips", 42: "Left Search", 43: "Left Video", 44: "Left Start Movie", 45: "Combo Award", 46: "Parking O.K.", 47: "Move Your Car",
	48: "Extra Ball",
	51: "Snack Bar", 52: "Center Search", 53: "Cola", 54: "Hotdog", 55: "Super Jackpot", 56: "Jackpot", 57: "Rescue", 58: "Multiball Restart",
	61: "Free Pass", 62: "Build Combo", 63: "Unlimited Millions", 64: "Creature Feature", 65: "Extra Ball Countdown", 66: "Big Millions",
	67: "Movie Madness", 68: "Snack Attack",
	71: "C (Creature)", 72: "R (Creature)", 73: "E (Creature)", 74: "A (Creature)", 75: "T (Creature)", 76: "U (Creature)",
	77: "R (Creature)", 78: "E (Creature)",
	81: "(F)-I-L-M", 82: "F-(I)-L-M", 83: "F-I-(L)-M", 84: "F-I-L-(M)", 85: "Start Combo", 86: "Popcorn", 87: "Ice Cream", 88: "Start Button",
}
# address -> (bulb part, lamp assembly) as the Lamp Locations list prints them.
LAMP_PARTS = {
	**{a: ("24-8768", "A-15731") for a in (11, 12, 13, 14)}, **{a: ("24-8768", "A-15727") for a in (15, 16, 17)}, 18: ("24-6549", "A-11754"),
	**{a: ("24-8768", "A-15734") for a in (21, 22, 23, 24, 25, 26)}, 27: ("24-6549", "A-11271"), 28: ("24-6549", "A-11271"),
	31: ("24-6549", "A-11754"), 32: ("24-6549", "A-8882"), 33: ("24-6549", "A-11754"), 34: ("24-6549", "A-8882"),
	35: ("24-8768", "A-15728"), 36: ("24-8768", "A-15728"), 37: ("24-8768", "A-15728 (also A-11271)"), 38: ("24-6549", "A-8882"),
	41: ("24-8768", "A-15730"), 42: ("24-8768", "A-15730"), 43: ("24-8768", "A-15730"), 44: ("24-8768", "A-15730 (also A-11271)"),
	**{a: ("24-8768", "A-15733") for a in (45, 46, 47, 48)}, 51: ("24-6549", "A-11733"), 52: ("24-6549", "A-11754"),
	53: ("24-6549", "A-11754"), 54: ("24-6549", "A-11754"), **{a: ("24-8768", "A-14305") for a in (55, 56, 57, 58)},
	61: ("24-6549", "A-11754"), 62: ("24-6549", "A-11271"), **{a: ("24-8768", "C-12709") for a in (63, 64, 65, 66, 67, 68)},
	**{a: ("24-8768", None) for a in range(71, 79)}, **{a: ("24-8768", "A-15732") for a in (81, 82, 83, 84)},
	85: ("24-6549", "A-11271"), 86: ("24-6549", "A-11754"), 87: ("24-6549", "A-11754"), 88: (None, "20-9663-1"),
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J138-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"), 3: ("Red-Orange", "J133-4", "Q88"),
	4: ("Red-Yellow", "J133-5", "Q87"), 5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
# Raw VPX coordinates of the Light each lamp's TimerInterval binds through vpmMapLights, or DRAWING. Lamps 28, 37
# and 44 have two bulbs: the lamp drawing draws two balloons 28 and two pointers each for 37 and 44.
LAMP_POSITIONS: dict[int, list[Any]] = {
	11: [(503.13593, 102.427124)], 12: [(593.58795, 93.52061)], 13: [(687.52515, 83.676285)], 14: [(779.30365, 72.78169)],
	15: [(533.0495, 497.1774)], 16: [(661.47235, 497.83652)], 17: [(604.011, 382.9561)], 18: [DRAWING],
	21: [(214.1092, 1341.445)], 22: [(222.80566, 1284.9)], 23: [(243.30151, 1231.4684)], 24: [(278.42786, 1190.6813)],
	25: [(143.6138, 1403.0112)], 26: [(124.96765, 1457.6073)], 27: [(153.48425, 1691.7328)],
	28: [(53.33925, 1706.4656), (819.91797, 1700.2234)],
	31: [(627.9112, 1496.1843)], 32: [(659.3338, 1418.8923)], 33: [(683.7814, 1345.385)], 34: [(717.5353, 1253.5405)],
	35: [(746.4578, 1168.1364)], 36: [(760.3135, 1118.663)], 37: [(818.2061, 1015.9875), (817.8542, 873.3433)],
	38: [(367.48398, 1131.9235)],
	41: [(168.74643, 1226.5785)], 42: [(122.71624, 1172.4371)], 43: [(109.008766, 1116.7499)],
	44: [(61.48176, 1014.9741), (60.601196, 873.984)], 45: [(343.28223, 912.8095)], 46: [(343.2113, 834.1399)],
	47: [(344.32434, 762.7736)], 48: [(345.04626, 683.5857)],
	51: [DRAWING], 52: [(424.84192, 892.05505)], 53: [(213.88728, 1069.6548)], 54: [(212.99535, 995.3015)],
	55: [DRAWING], 56: [DRAWING], 57: [DRAWING], 58: [DRAWING],
	61: [(437.89117, 1880.6482)], 62: [(228.61053, 797.9342)],
	63: [DRAWING], 64: [DRAWING], 65: [DRAWING], 66: [DRAWING], 67: [DRAWING], 68: [DRAWING],
	81: [(341.53357, 1748.067)], 82: [(404.75006, 1738.351)], 83: [(470.768, 1739.8956)], 84: [(534.47473, 1752.1008)],
	85: [(747.67523, 1459.0895)], 86: [(486.3151, 976.0685)], 87: [(505.7866, 1050.1157)],
}
LAMP_NOTES = {
	18: (
		"The lamp drawing (printed 2-40) prints balloon 18 above the playfield outline at the top right, its pointer ending in a shaded "
		"box drawn above the frame: the Admit One lamp is on the back panel. The placement takes the drawing's x and the playfield's "
		"rear edge (the drawing measures the box about 0.02 normalized behind it), and the retained table's Light L18 is a "
		"placeholder off the playfield."
	),
	28: "Two bulbs, one at each outlane: the lamp drawing (printed 2-40) prints balloon 28 at both, and the retained table binds Lights L28 and L28b.",
	37: "Two bulbs on the right lane's two inserts: the Lamp Locations list prints two assemblies (A-15728 and A-11271) and the lamp drawing (printed 2-40) draws two pointers 37; the retained table binds L37 and L37b.",
	44: "Two bulbs on the left lane's two inserts: the Lamp Locations list prints two assemblies (A-15730 and A-11271) and the lamp drawing (printed 2-40) draws two pointers 44; the retained table binds L44 and L44b.",
	51: "The retained table's Light L51 is a placeholder off the playfield (it models the insert only in its baked light maps), so the placement is measured on the lamp drawing (printed 2-40), where callout 51 ends below the right ramp's mouth.",
	55: "Top socket of the four-socket A-14305 board in the centre of the swirl. The retained table's Light L55 is a placeholder off the playfield, so the placement is the socket centre measured on the lamp drawing (printed 2-40).",
	56: "Second socket of the A-14305 board in the centre of the swirl, measured on the lamp drawing (printed 2-40); the table's L56 is a placeholder.",
	57: "Third socket of the A-14305 board, measured on the lamp drawing (printed 2-40); the table's L57 is a placeholder.",
	58: "Bottom socket of the A-14305 board, measured on the lamp drawing (printed 2-40); the table's L58 is a placeholder.",
	63: "Top socket of the C-12709 three-lamp board at the upper left, measured on the lamp drawing (printed 2-40); the table's L63 is a placeholder.",
	64: "Middle socket of the upper-left C-12709 board, measured on the lamp drawing (printed 2-40); the table's L64 is a placeholder.",
	65: "Bottom socket of the upper-left C-12709 board, measured on the lamp drawing (printed 2-40); the table's L65 is a placeholder.",
	66: "Top socket of the C-12709 three-lamp board right of centre, measured on the lamp drawing (printed 2-40); the table's L66 is a placeholder.",
	67: "Middle socket of the right C-12709 board, measured on the lamp drawing (printed 2-40); the table's L67 is a placeholder.",
	68: "Bottom socket of the right C-12709 board, measured on the lamp drawing (printed 2-40); the table's L68 is a placeholder.",
	88: "The Start button lamp (20-9663-1), in the cabinet; the lamp drawing prints balloon 88 below the playfield outline.",
}
# Drawing measurements whose measured coordinate lies outside the playfield: the y the drawing gives is clamped.
CLAMPED_MEASUREMENTS = {"lamp.matrix-18.emitter"}
# The switch drawing labels the trough switches with pointerless balloons one ball position up the trough from the switches
# they name, so it cannot check them; the trough switches and the two coils projected onto their ball seats stay observed.
UNCHECKED_TROUGH_PLACEMENTS = {
	"switch.matrix-55.sensor", "switch.matrix-56.sensor", "switch.matrix-57.sensor", "switch.matrix-58.sensor",
	"device.trough-ball-release.effect", "device.outhole.effect",
}

# --- General illumination (solenoid-flasher-wiring.md, power-driver-board-connectors.md) ----------------------------
# public -> (printed string, label, voltage connection, drive connection, drive wire, driver, playfield bulb, backbox bulb).
GI_STRINGS = {
	0: ("01", "Sequential G.I. #1", "J120-1", "J120-7", "White-Brown", "Q18", "#86", None),
	1: ("02", "Insert/Playfield Middle", "J120-2 / J121-2 (insert)", "J120-8 / J121-8 (insert)", "White-Orange", "Q10", "#44", "#555"),
	2: ("03", "Insert/Playfield Upper", "J120-3 / J121-3 (insert)", "J120-9 / J121-9 (insert)", "White-Yellow", "Q14", "#44", "#555"),
	3: ("04", "Sequential G.I. #2", "J120-5", "J120-10", "White-Green", "Q15", "#86", None),
	4: ("05", "Insert/Playfield Lower", "J120-6 / J121-6 (insert)", "J120-11 / J121-11 (insert)", "White-Violet", "Q12", "#44", "#555"),
}
# The retained script's UpdateGI drives these Light collections for G.I. 1, 2 and 4 (raw VPX coordinates).
GI_POSITIONS = {
	1: [(848.0314, 564.2358), (761.52924, 944.7972), (583.14557, 922.69086), (355.67224, 360.6262), (106.71763, 694.26935),
		(258.2822, 593.482), (107.28428, 423.7252)],
	2: [(551.53107, 205.95128), (644.07306, 198.07965), (735.09753, 188.47542), (595.6668, 460.11108)],
	4: [(673.792, 1653.8799), (707.7573, 1583.634), (826.9575, 1354.3866), (200.7687, 1652.9733), (167.73697, 1583.1692),
		(53.68336, 1340.6044), (54.358036, 1198.4846), (831.4056, 1104.512)],
}
GI_COLLECTIONS = {1: "GI_Middle (l141, l141b-l141g)", 2: "GI_Upper (l142a-l142d)", 4: "GI_Lower (l140a-l140h)"}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


# Committed excerpts are hashed from the files on disk; the validator checks the same digests fail-closed.
EXCERPT_FILE_HASHES = {path.name: _file_sha256(path) for path in sorted((ROOT / EXCERPT_DIRECTORY).iterdir()) if path.is_file()}


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Creature retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Creature extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Creature retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(extraction_root)):
		raise RuntimeError(f"Creature retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Creature retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


def normalized(point: tuple[float, float]) -> tuple[float, float]:
	"""Raw VPX playfield coordinates to the canonical space, rounded to six places."""
	x, y = point
	return round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6)


def _callout_seed() -> dict[str, Any]:
	return load_json(CALLOUT_SEED_PATH)


def _placement_ids(identifier: str, role: str, count: int) -> list[str]:
	return [f"{identifier}.{role}" + (f".{index}" if count > 1 else "") for index in range(1, count + 1)]


def located(identifier: str, role: str, positions: list[Any], *source_refs: str, drawn: bool = True, status: str = "validated") -> dict[str, Any]:
	"""Placements for one device, each with the status its evidence gives it before the callout check.

	A placement the callout seed checks starts ``observed`` and only ``drawing_callouts.apply_to_definition`` can validate
	it. A placement the seed excludes (a projection, a part the drawing does not draw, or a callout a documented finding
	puts on another part) keeps the status its own reasoning gives it, ``observed`` for the trough positions the drawing
	labels one ball position away (UNCHECKED_TROUGH_PLACEMENTS). A ``DRAWING`` placement takes the seed's reproducible
	measurement and stays ``observed``: no retained table object corroborates its position. A device that no drawing
	locates (``drawn=False``: the G.I. strings) keeps ``status``; any other placement the seed does not account for is
	refused.
	"""
	seed = _callout_seed()
	placements = []
	for placement_id, position in zip(_placement_ids(identifier, role, len(positions)), positions):
		if position == DRAWING:
			x, y = drawing_callouts.measured(seed, placement_id)
			if placement_id in CLAMPED_MEASUREMENTS:
				x, y = min(max(x, 0.0), 1.0), min(max(y, 0.0), 1.0)
			placement_provenance = provenance("observed", MANUAL_SOURCE, CALLOUT_SOURCE)
		else:
			x, y = normalized(position)
			placement_provenance = provenance(status, *source_refs)
			if placement_id in UNCHECKED_TROUGH_PLACEMENTS:
				if placement_id not in seed["excluded_checks"]:
					raise RuntimeError(f"Creature callout seed must exclude the trough placement {placement_id}")
				placement_provenance["status"] = "observed"
			elif not drawn or placement_id in seed["excluded_checks"]:
				pass
			elif placement_id in seed["checks"]:
				placement_provenance["status"] = "observed"
			else:
				raise RuntimeError(f"Creature callout seed neither checks nor excludes {placement_id}")
		placements.append({"id": placement_id, "role": role, "space": "playfield", "x": x, "y": y, "provenance": placement_provenance})
	rank = {"candidate": 0, "observed": 1, "validated": 2}
	return {"status": min((p["provenance"]["status"] for p in placements), key=rank.__getitem__), "placements": placements}


def callout_checks() -> dict[str, tuple[str, str]]:
	"""Every table placement a factory location drawing can check: placement id -> (printed label, page)."""
	checks: dict[str, tuple[str, str]] = {}
	for address, positions in SWITCH_POSITIONS.items():
		for placement_id, position in zip(_placement_ids(f"switch.matrix-{address}", "sensor", len(positions)), positions):
			if position != DRAWING:
				checks[placement_id] = (str(address), "2-41")
	for address, positions in SOLENOID_POSITIONS.items():
		role = "emitter" if SOLENOID_KINDS[address] == "flasher" else "effect"
		for placement_id, position in zip(_placement_ids(output_id(SOLENOID_LABELS[address]), role, len(positions)), positions):
			if position != DRAWING:
				checks[placement_id] = (str(address), "2-43")
	for address, positions in LAMP_POSITIONS.items():
		for placement_id, position in zip(_placement_ids(f"lamp.matrix-{address}", "emitter", len(positions)), positions):
			if position != DRAWING:
				checks[placement_id] = (str(address), "2-40")
	return checks


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
	return "device." + re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


# --- Inputs ----------------------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_ic = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_ic = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC Fliptronic CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += " The Switch Locations parts list and the Switch Matrix wiring page both mark this position Not Used."
		return _device(identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE), **extra)
	part = SWITCH_PARTS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES.get(address, "microswitch")}
	physical["part_number" if not part.startswith("A-") else "assembly_part_number"] = part
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
	if address in OPTO_SWITCHES:
		notes += (
			" The Switch Locations list prints an LED (A-14231) over a phototransistor (A-14232) for it: the beam is unbroken and the contact "
			"the matrix sees closed while no ball is in the popper. cftblGameData's inverted-switch mask normalizes it, so public 1 means a "
			"ball is in the popper."
		)
		if address == 34:
			notes += " The T.1 run named RIGHT POPPER while public 34 was 1 and cleared it at 0."
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in SWITCH_NOTES:
		notes += " " + SWITCH_NOTES[address]
	if address == 25:
		notes += " The T.1 run named <P>AID while public 25 was 1 and cleared it at 0; the P-3 prototype ROM names it P OF PAID."
		refs += (EDGES_SOURCE, P3_EDGES_SOURCE)
	if address == 34:
		refs += (EDGES_SOURCE, P3_EDGES_SOURCE)
	if address in (16, 17, 37):
		refs += (SUBWAY_SOURCE,)
	if address in TABLE_OFFSETS:
		notes += " " + TABLE_OFFSETS[address]
	if address in SWITCH_OBJECTS:
		notes += f" The placement is the retained table's {SWITCH_OBJECTS[address]}."
	if address in {16, 17}:
		notes += (
			" The switch drawing (printed 2-41) transposes callouts 16 and 17 (its 16 ends on the centre hole and its 17 on the left hole); "
			"the ROM's awards, the game rules and the printed names (Left Subway, Center Subway) agree with the table, so the placement "
			"follows the table and is not checked against the drawing."
		)
	if address in {55, 56, 57, 58}:
		notes += (
			" The switch drawing prints balloons 55-58 without pointers in a row along the trough, each one ball position up the trough from "
			"the switch it names (55 on the outhole end), so it does not mark the switch: the placement follows the table's ball seat, is "
			"not checked against the drawing and stays observed."
		)
	if address in CABINET_SWITCHES:
		role, location = CABINET_SWITCHES[address]
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = location
	else:
		extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	extra["normally_closed"] = address in OPTO_SWITCHES
	if address in {15, 22}:
		extra["initial_active"] = True
	physical["notes"] = notes
	return _device(identifier, SWITCH_LABELS[address], "switch", SWITCH_GROUP, address, "used", refs, physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, ic = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address, "optional" if address == 4 else "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC Fliptronic CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": ic},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, wire, connection, printed, switch_type, role, availability) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed} ({wire}, {connection})."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"roles": [role],
			"wiring": {"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection},
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
		physical: dict[str, Any] = {}
		if availability == "unused":
			if address == 115:
				notes += " Not fitted: the Fliptronic II connector list prints J906-4 Not Used."
			else:
				notes += (
					" Not fitted: the connector list still prints J906-5 'Black-Gray, to upper left end-of-stroke switch', but the machine has "
					"no upper flipper. The upper left flipper's holding and power lines J902-1 and J902-3 run to the backbox insert flashers "
					"(solenoids 36 and 35), and the flipper tables list only the two lower flippers."
				)
			notes += (
				" cftblGameData declares FLIP_SOL(FLIP_L) only, so PinMAME synthesizes no upper end-of-stroke state, and the T.1 run drove "
				f"public {address} to 1: the switch grid marked it closed, but the ROM named no switch and drove no output. The P-3 prototype "
				"ROM does the same."
			)
			physical["location"] = "not installed"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			refs += (EDGES_SOURCE, P3_EDGES_SOURCE)
			physical["notes"] = notes
			items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, "unused", refs, physical=physical, **extra))
			continue
		physical["switch_type"] = switch_type
		extra["normally_closed"] = False
		if role.startswith("flipper."):
			side = "right" if address in {112, 116} else "left"
			opto = "Opto 1 (SW-1, J1-1, 'lower flipper')" if address in {112, 114} else "Opto 2 (SW-2, J1-2, 'upper flipper')"
			physical["location"] = "cabinet flipper button"
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			notes += (
				f" {opto} of the {side} cabinet Flipper Opto Switch Board A-15894, which has two LED/phototransistor pairs that "
				f"the {side} button breaks together. This generation's WPC_FLIPPERS read complements the Fliptronic column, so public 1 is the "
				"pressed button and the contact the CPU sees is open at rest: normally_closed is false whatever the beam does."
			)
			if address in {116, 118}:
				coils = "45/46" if address == 116 else "47/48"
				eos = "R FLIPPER EOS" if address == 116 else "L FLIPPER EOS"
				notes += (
					" The machine has no upper flipper; the switch-matrix page still prints this position 'Upper "
					f"{side.capitalize()} Flipper Opto'. The T.1 run drove public {address} to 1 and the ROM fired the lower {side} flipper "
					f"({coils}, power then hold while the input stayed at 1) and named the synthesized end-of-stroke bit {eos}, so the ROM "
					f"treats it as the {side} button: a recreation drives it together with public {address - 4}. The P-3 prototype ROM does "
					"the same."
				)
				refs += (EDGES_SOURCE, P3_EDGES_SOURCE)
		else:
			physical["location"] = "flipper assembly"
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			notes += (
				" End-of-stroke leaf switch of the lower flipper assembly. cftblGameData declares FLIP_SOL(FLIP_L), so PinMAME synthesizes "
				"this address from the flipper coil state after the stroke time and its public level is not a measurement of the contact; "
				"normally_closed records the Fliptronic grounded-switch convention (closed to ground only at end of stroke). The T.1 run "
				"showed the ROM naming the synthesized bit when it fired the flipper."
			)
			refs += (EDGES_SOURCE,)
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
					"location": "WPC Fliptronic CPU board", "switch_type": "dip",
					"notes": "WPC CPU-board country/option DIP bank. No ON/OFF combination of this bank is asserted here.",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# --- Outputs ---------------------------------------------------------------------------------------------------------
def _flipper_coil(address: int) -> dict[str, Any]:
	stage, side, control, control_wire, supply, supply_wire, transistors, part, assembly, rom_name, rom_wires = FLIPPER_COILS[address]
	label = SOLENOID_LABELS[address]
	identifier = output_id(label)
	notes = (
		f"The {side} flipper's {stage} winding on the Fliptronic II board ({control}, {control_wire}; supply {supply}, {supply_wire}). The "
		f"Flipper Circuits table prints the transistors {transistors}. Coil {part} in assembly {assembly}. The ROM's T.12 FLIPPER COIL TEST "
		f"names it \"{rom_name}\" with the wires {rom_wires}"
	)
	notes += " and publishes the hold winding together with the power winding in that step." if stage == "power" else " and publishes it alone."
	callback = SOLENOID_SCRIPT.get(address)
	notes += f" Retained script: {callback}." if callback else " The retained script registers no callback for it (UseSolenoids = 2 fast flips drive the flipper from the power address)."
	notes += (
		" The Solenoid/Flasher Locations list prints the flipper coils '*Not shown', so the placement is the projection onto the table's "
		f"flipper pivot ({SOLENOID_OBJECTS[address]}) and is not checked against the drawing."
	)
	notes += " The P-3 prototype ROM's T.12 names and drives it the same way."
	refs: tuple[str, ...] = (MANUAL_SOURCE, FLIPPER_TEST_SOURCE, P3_FLIPPER_TEST_SOURCE, CORE_SOURCE) + ((VPX_SCRIPT_SOURCE,) if callback else ())
	return _device(
		identifier, label, "coil", SOLENOID_GROUP, address, "used", refs,
		aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
		physical={"part_number": part, "assembly_part_number": assembly, "notes": notes},
		wiring={"board": "Fliptronic II board", "driver_transistor": transistors, "control_connection": control, "control_wire": control_wire,
			"power_connection": supply, "power_wire": supply_wire},
		spatial=located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE),
	)


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in FLIPPER_COILS:
			items.append(_flipper_coil(address))
			continue
		if address in VIRTUAL_SOLENOID_LABELS:
			label = VIRTUAL_SOLENOID_LABELS[address]
			notes = {
				29: "PinMAME mirrors WPC_GILAMPS bit 5 here when the driver sets no fast-flip RAM address; init_cftbl calls no wpc_set_fastflip_addr (wpc.c core_write_pwm_output of WPC_GILAMPS >> 5 at outputs 29-31). It is not a playfield device.",
				30: "PinMAME mirrors WPC_GILAMPS bit 6 here under the same rule as 29; not a playfield device.",
				31: "PinMAME mirrors WPC_GILAMPS bit 7 here under the same rule as 29, the bit that drove the game-on relay before Fliptronics; no relay exists on this machine, and every runtime run found it active in the service menu. Not a playfield device.",
				32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero.",
				49: "PinMAME's simulator-only ball-shooter channel; the machine has a manual plunger and no ball-shooter coil.",
				50: "Reserved PinMAME output position before the first custom-output boundary; cftblGameData declares no custom solenoids.",
			}.get(address, "This WPC-Fliptronic generation has no integrated LPDC board, so pinned PinMAME's core_getSol serves the 37-44 range only for WPC-95 and System 11; this address is unused space.")
			refs = (CONTROLLER_SOURCE, CORE_SOURCE) + ((FLASHER_TEST_SOURCE,) if address == 31 else ())
			items.append(
				_device(
					output_id(label), label, "virtual", SOLENOID_GROUP, address, "used" if address in {29, 30, 31} else "unused", refs,
					aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
					roles=["internal.wpc-state"] if address in {29, 30, 31} else ["internal.unused.wpc-output"],
					physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
				)
			)
			continue
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		kind = SOLENOID_KINDS[address]
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		physical: dict[str, Any] = {}
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if address in SOLENOID_TABLE:
			printed_type, transistor, drive, wire, voltage, part = SOLENOID_TABLE[address]
			aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type}, driver {transistor}, wire {wire}, drive {drive}, voltage {voltage}, part {part})."
			wiring: dict[str, Any] = {"board": "WPC Fliptronic power driver board", "driver_transistor": transistor, "control_connection": drive,
				"control_wire": wire, "power_connection": voltage}
			if kind in {"coil", "motor"} and not part.startswith("#"):
				physical["part_number"] = part.split()[0]
		else:
			control, wire = INSERT_FLASHER_LINES[address]
			notes = (
				f"The Fliptronic II board's upper-flipper line {control} ({wire}), which this machine's connector list prints 'to insert "
				"flashers': the machine has no upper flipper, and cftblGameData's FLIP_SOL(FLIP_L) leaves the upper Fliptronic outputs to the "
				"ROM. The manual prints no part or bulb count for these backbox flashers."
			)
			wiring = {"board": "Fliptronic II board", "control_connection": control, "control_wire": wire}
		if address in SOLENOID_ASSEMBLIES:
			physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
		if address in SOLENOID_NOTES:
			notes += " " + SOLENOID_NOTES[address]
		if address in FLASHER_BULBS:
			playfield, insert = FLASHER_BULBS[address]
			physical["quantity"] = playfield + insert
			if insert and playfield:
				notes += f" {playfield + insert} bulbs: {playfield} on the playfield, which the placement locates, and {insert} on the backbox insert."
		if address in T5_NAMES:
			name, rom_wire = T5_NAMES[address]
			notes += f" T.5 FLASHER TEST: the ROM pulses public {address} and prints \"{name}\" with the wires {rom_wire} RED-WHT."
			p3_name = P3_T5_NAMES.get(address)
			notes += f" The P-3 prototype ROM pulses it with the same wires and prints \"{p3_name}\"." if p3_name else " The P-3 prototype ROM prints the same."
			refs += (FLASHER_TEST_SOURCE, P3_FLASHER_TEST_SOURCE)
		if address in SOLENOID_SCRIPT:
			notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
			refs += (VPX_SCRIPT_SOURCE,)
		elif address in {5, 6, 13, 14, 15}:
			notes += " The retained script registers no callback: the table's own slingshot or bumper object fires it."
			refs += (VPX_SCRIPT_SOURCE,)
		else:
			notes += " The retained script registers no callback for it."
		if address in {20, 24}:
			refs += (RAMP_LIGHTS_SOURCE, P3_RAMP_LIGHTS_SOURCE)
			notes += " In the T.15 RAMP LIGHTS TEST the ROM steps 20 and 24 through the four decoder codes (runtime evidence creature-cftbl_l4-ramp-lights-test.json), and the P-3 prototype ROM does the same."
		if address == 3:
			refs += (SUBWAY_SOURCE,)
			notes += " The Locations list prints 'Bottom Right Popper' for it."
		if address == 7 or address in SOLENOID_ROLES:
			extra_spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in {20, 24}:
			extra_spatial = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		else:
			role = "emitter" if kind == "flasher" else "effect"
			extra_spatial = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			if address in SOLENOID_OBJECTS:
				notes += f" The placement is the retained table's {SOLENOID_OBJECTS[address]}."
			if address in {4, 12}:
				square = "04" if address == 4 else "12"
				notes += (
					f" The solenoid drawing (printed 2-43) draws square {square} on the coil beside the trough, so the projection is not checked "
					"against it, and it stays observed like the trough ball seat it projects onto."
				)
			if address in {21, 23, 26}:
				notes += " No table object models it: the placement is its square measured on the solenoid drawing (printed 2-43)."
		physical["notes"] = notes
		items.append(
			_device(identifier, label, kind, SOLENOID_GROUP, address, "used", refs, aliases=aliases,
				roles=[SOLENOID_ROLES[address]] if address in SOLENOID_ROLES else None, physical=physical, wiring=wiring, spatial=extra_spatial)
		)
	return items


def _chase_lamp(address: int) -> dict[str, Any]:
	group = "A" if address <= 94 else "B"
	string = (address - 91) % 4 + 1
	gi = 0 if group == "A" else 3
	connector, pin = ("J4", string + 2) if group == "A" else ("J3", {1: 2, 2: 4, 3: 5, 4: 6}[string])
	triac = {91: "Q4", 92: "Q3", 93: "Q8", 94: "Q7", 95: "Q12", 96: "Q11", 97: "Q16", 98: "Q15"}[address]
	wire = {91: "Orange-Brown", 92: "Orange-Red", 93: "Orange-Black", 94: "Orange-Yellow", 95: "Orange-Green", 96: "Orange-Blue",
		97: "Orange-Violet", 98: "Orange-Gray"}[address]
	notes = (
		f"Chase string LAMP {string}{group} of the Chase Light II board A-15541 ({connector}-{pin}, {wire}, triac {triac}), powered by G.I. "
		f"string {'01' if group == 'A' else '04'} (public G.I. {gi}). Not a lamp-matrix position: cftblGameData declares lampCol = 1 and "
		"pinned wpc.c's WPC_CFTBL handling writes the public lamp matrix's ninth column, public 91-98, as 0x11 shifted by the decoder "
		"code (solenoid 20 plus twice solenoid 24), so this address and its partner in the other group are 1 while the code is "
		f"{string - 1}, whatever the G.I. does; only PinMAME's separate physical-output (modulated lamp) path ANDs the selection with "
		"the G.I. triacs. The selected code is the output the 74LS139 pulls low, and on the board the low output turns its string off "
		f"while the other three conduct (Chase Light II Schematic, printed 3-15). So this address is 1 while string {string}{group} is "
		f"the dark one: the string's bulbs are lit while G.I. {gi} is on and public {address} is 0. The T.15 RAMP LIGHTS TEST cycles 91, "
		"92, 93, 94 in order, each of 95-98 with its partner, and stopping it switches G.I. 0 and 3 off while PinMAME keeps publishing "
		"the selected pair. The retained VPW script lights its chase phase while the address is 1 and its G.I. is on, one phase lit and "
		"three dark, the inverse of the board."
	)
	notes += (
		" The ramp's and the bowl's 32 #86 chase bulbs are on three eight-lamp boards on the swirl ramp and one in the bowl; which bulbs "
		"belong to this string, and which ramp boards this group drives, are unresolved (conflict.chase-light-board-group-assignment), "
		"so the device has no placement and no quantity."
	)
	return _device(
		f"lamp.chase-{address}", f"Chase Lamp {string}{group}", "lamp", LAMP_GROUP, address, "used",
		(MANUAL_SOURCE, PARTS_LIST_SOURCE, CORE_SOURCE, RAMP_LIGHTS_SOURCE, P3_RAMP_LIGHTS_SOURCE, VPX_SCRIPT_SOURCE),
		status="conflicted",
		aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
		physical={"assembly_part_number": "A-15541", "notes": notes},
		wiring={"board": "Chase Light II board A-15541", "driver_transistor": triac, "control_connection": f"{connector}-{pin}", "control_wire": wire},
	)


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"lamp.matrix-{address}"
			bulb, assembly = LAMP_PARTS[address]
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			positions = LAMP_POSITIONS.get(address, [])
			physical: dict[str, Any] = {"quantity": max(len(positions), 1)}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire})."
			if bulb:
				notes += f" Printed bulb {bulb}."
			if address in LAMP_NOTES:
				notes += " " + LAMP_NOTES[address]
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"wiring": {
					"board": "WPC Fliptronic power driver board", "drive_wire": drive_wire, "drive_connection": drive_connection,
					"return_wire": return_wire, "return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
			if 71 <= address <= 78:
				notes += ' Printed "*Located on backbox insert": one letter of the backbox C-R-E-A-T-U-R-E header.'
				extra["roles"] = ["cabinet.insert-panel"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 88:
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				refs += (VPX_SCRIPT_SOURCE,)
				extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
				if DRAWING not in positions:
					lights = {28: "L28 and L28b", 37: "L37 and L37b", 44: "L44 and L44b"}.get(address, f"L{address}")
					notes += f" The placement is the retained table's Light {lights}, which vpmMapLights binds through its TimerInterval."
			if address in {21, 53}:
				refs += (SUBWAY_SOURCE,)
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(identifier, LAMP_LABELS[address], "lamp", LAMP_GROUP, address, "used", refs, **extra))
	for address in range(91, 99):
		items.append(_chase_lamp(address))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (printed, label, voltage, drive, wire, transistor, playfield, backbox) in GI_STRINGS.items():
		identifier = f"gi.string-{address}"
		notes = f"Printed general-illumination string {printed} '{label}', driver {transistor}, drive {drive} ({wire}), voltage {voltage}; printed playfield bulb {playfield}"
		notes += f" and backbox insert bulb {backbox}." if backbox else "."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"wiring": {"board": "WPC Fliptronic power driver board", "driver_transistor": transistor, "control_connection": drive,
				"control_wire": wire, "power_connection": voltage},
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		status = "validated"
		if address in {0, 3}:
			group = "A" if address == 0 else "B"
			lamps = "91-94" if address == 0 else "95-98"
			cable = "H-15871" if address == 0 else "H-16213 ('front chase lite cable') and the bowl cable H-15870"
			notes += (
				f" It feeds only the chase strings of group {group} on the Chase Light II board (J1-{7 if address == 0 else 6} 'G.I. "
				f"({1 if address == 0 else 2})'): the board's triacs switch it onto the four strings LAMP 1{group}-4{group} (lamps {lamps}), "
				f"three of which are lit while it is on. Its colours run in the parts list's {cable}. Stopping the T.15 RAMP LIGHTS TEST "
				"switches G.I. 0 and 3 off and no other string; PinMAME's lamps 91-98 do not follow the G.I. (see lamp 91). The retained VPW "
				"script gates its ramp chase with G.I. 0 and its bowl chase with G.I. 3; which ramp bulbs this string actually powers is "
				"unresolved (conflict.chase-light-board-group-assignment), so it has no placement."
			)
			refs += (PARTS_LIST_SOURCE, RAMP_LIGHTS_SOURCE, P3_RAMP_LIGHTS_SOURCE)
			status = "conflicted"
			extra["physical"] = {"notes": notes}
		else:
			notes += (
				f" The retained script's UpdateGI drives the Light collection {GI_COLLECTIONS[address]} for it. Those lights are invisible "
				"sources for the table's baked light maps (no bulb mesh), not modelled sockets, and the manual prints no per-string bulb "
				"count and no drawing locates G.I. bulbs, so the placements are only candidates for where the string's bulbs sit and the "
				"device carries no quantity."
			)
			extra["physical"] = {"notes": notes}
			extra["spatial"] = located(identifier, "emitter", GI_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, drawn=False, status="candidate")
		items.append(_device(identifier, label, "gi", GI_GROUP, address, "used", refs, status=status, **extra))
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


# --- Mechanisms, conflicts and drivers ----------------------------------------------------------------------------------
def _mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...],
		positions: list[tuple[str, str, list[str], str]] | None = None, assembly: str | None = None) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
		"provenance": provenance("validated", *refs),
	}
	if assembly:
		record["assembly_part_number"] = assembly
	if positions:
		record["positions"] = [{"id": pid, "label": plabel, "sensors": psensors, "description": text} for pid, plabel, psensors, text in positions]
	return record


def _coil(address: int) -> str:
	return output_id(SOLENOID_LABELS[address])


def mechanisms() -> list[dict[str, Any]]:
	return [
		_mechanism(
			"mechanism.trough", "Outhole and three-ball trough", "kicker", [_coil(12), _coil(4)],
			["switch.matrix-55", "switch.matrix-56", "switch.matrix-57", "switch.matrix-58"],
			"A drained ball rolls onto the outhole switch 55 at the trough's outhole end; the outhole kicker (solenoid 12, A-8039-3) kicks it "
			"into the trough. The three balls rest on switches 58 (nearest the outhole), 57 and 56 (at the exit end), and the ball release coil "
			"(solenoid 4, B-9362-L-2) kicks the ball on 56 into the shooter lane, the others rolling down behind it.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
			[("outhole", "Ball in the outhole", ["switch.matrix-55"], "Outhole switch."),
			("ball-1", "Trough ball at the release", ["switch.matrix-56"], "Released by solenoid 4."),
			("ball-2", "Middle trough ball", ["switch.matrix-57"], "Second position."),
			("ball-3", "Trough ball nearest the outhole", ["switch.matrix-58"], "Third position.")],
		),
		_mechanism(
			"mechanism.shooter-lane", "Manual plunger shooter lane", "other", [], ["switch.matrix-66"],
			"No solenoid drives the shooter lane: the player plunges the ball resting on switch 66 with the manual plunger, up past the "
			"P-A-I-D lanes (25-28).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
		),
		_mechanism(
			"mechanism.right-popper", "Top right popper (F-I-L-M hole)", "kicker", [_coil(1)], ["switch.matrix-34"],
			"A ball in the F-I-L-M hole breaks the beam of opto 34; the popper coil (solenoid 1, A-15769) kicks it back to the playfield.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), assembly="A-15769",
		),
		_mechanism(
			"mechanism.subway", "Left and centre holes, subway and lower right popper", "kicker", [_coil(3)],
			["switch.matrix-16", "switch.matrix-17", "switch.matrix-37"],
			"The left hole (switch 16, K-I-S-S) and the centre hole (switch 17, Snack Bar) drop the ball into a subway under the playfield that "
			"delivers it to the lower right popper, where it breaks opto 37; the popper coil (solenoid 3, A-15842) kicks it back to the "
			"playfield. In the subway run the ROM fired solenoid 3 for the ball the host delivered to 37 after either hole.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, SUBWAY_SOURCE),
			[("left-hole", "Left hole (K-I-S-S)", ["switch.matrix-16"], "Subway entry."),
			("centre-hole", "Centre hole (Snack Bar)", ["switch.matrix-17"], "Subway entry."),
			("popper", "Ball in the lower right popper", ["switch.matrix-37"], "Subway exit.")],
			assembly="A-15842",
		),
		_mechanism(
			"mechanism.lift-ramp", "Lift ramp at the head of the left ramp", "motorized", [_coil(23), _coil(26)],
			["switch.matrix-38", "switch.matrix-36", "switch.matrix-62", "switch.matrix-64"],
			"The A-16042 Lift Ramp Assembly under the head of the left ramp carries an up coil (solenoid 23, SM1-2B-900-DC, a DC solenoid) and a "
			"down coil (solenoid 26, AE-26-1200), both with tieback diodes, and the position switch 38. Public 38 is 1 while the ramp is down: "
			"the retained script writes 1 when 26 fires and 0 when 23 fires, and pinned cftbl_handleMech sets it from the same commands. "
			"Pinned cftbl.c's simulator sends a ball entering the left ramp (switch 36) up the upper (Creature) ramp to switch 64 while 38 is "
			"1 and along the swirl ramp past switch 62 otherwise; that routing is the simulator's, not a measured fact.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
			[("down", "Ramp down", ["switch.matrix-38"], "Public 38 = 1, after solenoid 26."),
			("up", "Ramp up", ["switch.matrix-38"], "Public 38 = 0, after solenoid 23.")],
			assembly="A-16042",
		),
		_mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other", [_coil(13), _coil(14), _coil(15)],
			["switch.matrix-45", "switch.matrix-46", "switch.matrix-33"],
			"Three jet bumpers (A-9415-2 coils, SW-11A-37 skirt switches): the top left one fires solenoid 13 from switch 45, the top right "
			"one 14 from 46 and the bottom one 15 from 33.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
		),
		_mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other", [_coil(6), _coil(5)], ["switch.matrix-47", "switch.matrix-48"],
			"Two kicking slingshots (SW-1A-114 switches): the left one (A-14369-L) fires solenoid 6 from switch 47 and the right one "
			"(A-14369-R) solenoid 5 from switch 48.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
		),
		_mechanism(
			"mechanism.snack-bar-targets", "Snack Bar stand-up targets", "other", [],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-44"],
			"Four stand-up targets (A-16206-2): Cola (41) and Hot Dog (42) on the left, Popcorn (43) and Ice Cream (44) in the centre. "
			"Completing them opens the Snack Bar in the centre hole.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SUBWAY_SOURCE),
		),
		_mechanism(
			"mechanism.bowl", "Whirlpool bowl", "other", [_coil(10)], ["switch.matrix-65"],
			"The A-15993 bowl: the ball circles the whirlpool past its micro switch 65 and drops through the centre. The bowl flasher "
			"(solenoid 10) lights it, and the A-15672 board under it carries eight chase bulbs on the Sequential G.I. #2 group (see "
			"mechanism.sequential-gi-chase).",
			(MANUAL_SOURCE, PARTS_LIST_SOURCE, VPX_SCRIPT_SOURCE),
			assembly="A-15993",
		),
		_mechanism(
			"mechanism.sequential-gi-chase", "Sequential G.I. chase lights", "other", [_coil(20), _coil(24), "gi.string-0", "gi.string-3"],
			[],
			"The Chase Light II board A-15541 under the playfield switches two G.I. strings onto eight chase strings: G.I. string 01 "
			"(public G.I. 0) onto LAMP 1A-4A on J4 and string 04 (public G.I. 3) onto LAMP 1B-4B on J3. Solenoids 20 and 24 select one of four "
			"codes on a 74LS139 whose two halves see the same bits; the selected string of each group goes dark and the other three stay lit, "
			"so the chase is a dark string stepping through each group. PinMAME publishes the selected (dark) string as lamps 91-98 (see "
			"those devices). The T.15 RAMP LIGHTS TEST cycles the codes 0, 1, 2, 3 and stopping it switches G.I. 0 and 3 off. The 32 #86 "
			"chase bulbs sit on three eight-lamp boards on the swirl ramp (A-16089, and A-16088 chained to A-16087) and on the bowl's A-15672; "
			"the bowl's cable carries the J3 group. Which ramp boards each group drives and which bulbs belong to which string are unresolved "
			"(conflict.chase-light-board-group-assignment).",
			(MANUAL_SOURCE, PARTS_LIST_SOURCE, CORE_SOURCE, RAMP_LIGHTS_SOURCE, VPX_SCRIPT_SOURCE),
			assembly="A-15541",
		),
		_mechanism(
			"mechanism.hologram", "Creature hologram", "other", [_coil(21), _coil(27), _coil(28)], [],
			"The hologram that makes the Creature appear in the playfield window: the hologram lamp (solenoid 28, #1156) and the mirror motor "
			"(solenoid 27, 48 VAC) sit in the cabinet bottom, and the push motor (solenoid 21, 48 VAC) under the playfield. The retained script "
			"shows its hologram image while 28 is on and animates it while 27 runs.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
			assembly="A-15958",
		),
		_mechanism(
			"mechanism.flippers", "Lower flipper pair", "other", [_coil(45), _coil(46), _coil(47), _coil(48)],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114", "switch.generic-116", "switch.generic-118"],
			"Two Fliptronic flippers: lower right (FL-11629, A-15205-R-2; power 45, hold 46) and lower left (FL-15411, A-15205-L-4; power 47, "
			"hold 48). Each cabinet button breaks both optos of its Flipper Opto Switch Board (112 and 116 right, 114 and 118 left), and the "
			"ROM fires the flipper from either. PinMAME synthesizes the end-of-stroke bits 111 and 113 from the coil state.",
			(MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE),
			[("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112", "switch.generic-116"], "End of stroke 111, buttons 112 and 116."),
			("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114", "switch.generic-118"], "End of stroke 113, buttons 114 and 118.")],
		),
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.chase-light-board-group-assignment",
			"path": "outputs[binding.group=pinmame.output.lamp,binding.device=91..98]; outputs[binding.group=pinmame.output.gi,binding.device=0,3]",
			"description": (
				"Which chase bulbs each Chase Light II group lights. The board's block diagram (printed 3-14) draws J4 (G.I. string 01, public "
				"G.I. 0, lamps 91-94) to A-16087 alone and J3 (string 04, G.I. 3, lamps 95-98) to A-16088 chained on to A-16089, and draws no "
				"bowl board. The factory parts list instead puts the strip socket A-16088 plugs into on A-16087, so A-16087 and A-16088 form "
				"the chained pair and A-16089 takes its own cable; it runs one ramp cable in the J4 colours (H-15871) and one in the J3 "
				"colours (H-16213, 'front chase lite cable') without saying which board each plugs into, and the bowl cable H-15870 in the J3 "
				"colours. The manual's cable list adds an H-16214 'Center Chase Light Cable' that neither assembly lists. No source gives the "
				"socket order of the four strings on any of the four boards, and the Power Driver Board connector list puts solenoids 20 and "
				"24 on the opposite J2 pins from the chase board's page, which would swap strings 2 and 3 of each group. A recreation therefore "
				"cannot tell which ramp bulbs go dark with which address or which G.I. string switches which ramp section. Resolution path: on "
				"a machine, pull J3 and then J4 at the Chase Light II board and note which ramp and bowl bulbs go dark, then film the ramp and "
				"bowl while the T.15 RAMP LIGHTS TEST cycles (stopping it switches the chase power off) and note which bulbs go dark together "
				"and in which order, or with the ramp off check continuity from each board's header pins to its sockets; any owner of a "
				"working machine can do it in minutes."
			),
			"source_refs": [MANUAL_SOURCE, PARTS_LIST_SOURCE, CORE_SOURCE],
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


# --- Sources ---------------------------------------------------------------------------------------------------------
CROP_DERIVATIONS = {
	"switch-locations": "page 101, crop box 0.065,0.17,0.44,0.83, scanned page rendered at its native resolution (embedded image xref 426, 1727px across 8.64in), rendered at 200 dpi, 637x1541 WebP quality 80",
	"switch-matrix": "page 106, crop box 0.04,0.05,0.97,0.9, scanned page rendered at its native resolution (embedded image xref 448, 1696px across 8.48in), rendered at 200 dpi, 1579x1984 WebP quality 80",
	"lamp-locations": "page 100, crop box 0.055,0.15,0.48,0.92, scanned page rendered at its native resolution (embedded image xref 421, 1723px across 8.62in), rendered at 200 dpi, 722x1798 WebP quality 80",
	"lamp-matrix": "page 108, crop box 0.13,0.045,0.97,0.91, scanned page rendered at its native resolution (embedded image xref 456, 1696px across 8.48in), rendered at 200 dpi, 1426x2014 WebP quality 80",
	"solenoid-flasher-locations": "page 103, crop box 0.045,0.15,0.56,0.9, scanned page rendered at its native resolution (embedded image xref 435, 1696px across 8.48in), rendered at 200 dpi, 874x1751 WebP quality 80",
	"solenoid-flasher-wiring": "page 109, crop box 0.04,0.045,0.97,0.9, scanned page rendered at its native resolution (embedded image xref 461, 1696px across 8.48in), rendered at 200 dpi, 1579x1996 WebP quality 80",
	"lamp-drawing": "page 100, crop box 0.43,0.16,0.88,0.91, scanned page rendered at its native resolution (embedded image xref 421, 1723px across 8.62in), rendered at 200 dpi, grayscale, 764x1751 WebP quality 80",
	"switch-drawing": "page 101, crop box 0.46,0.17,0.92,0.9, scanned page rendered at its native resolution (embedded image xref 426, 1727px across 8.64in), rendered at 200 dpi, grayscale, 781x1704 WebP quality 80",
	"solenoid-flasher-drawing": "page 103, crop box 0.48,0.16,0.92,0.87, scanned page rendered at its native resolution (embedded image xref 435, 1696px across 8.48in), rendered at 200 dpi, grayscale, 747x1657 WebP quality 80",
}


def _excerpt(name: str, locator: str, *, credit: str = "curator, read from the rendered page", method: str = "manual") -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.creature.{name}",
		"locator": locator,
		"path": f"{EXCERPT_DIRECTORY}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if name in CROP_DERIVATIONS:
		record["image"] = f"{EXCERPT_DIRECTORY}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = f"{MANUAL_NAME} {CROP_DERIVATIONS[name]}"
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = True
	return record


def _runtime(source_id: str, filename: str, scenario: str, locator: str, game: str = "cftbl_l4") -> dict[str, Any]:
	return {
		"id": source_id,
		"kind": "runtime_scenario",
		"uri": f"internal:{EVIDENCE_DIRECTORY}/{filename}",
		"revision": PINMAME_REVISION,
		"locator": (
			f"One hash-pinned LibPinMAME harness run of {game} from empty NVRAM with built-in mechanisms disabled (scenario "
			f"tools/harness-scenarios/wpc-fliptronic/{scenario}.json; every cited DMD frame is pinned with the curator's reading in "
			f"tools/seeds/bally/creature-from-the-black-lagoon-1992-frame-readings.json). {locator}"
		),
		"license": "NOASSERTION",
		"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
	}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the cftbl_* clone tree (" + ", ".join(DRIVER_IDS) + ")",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/cftbl.c cftblGameData: GEN_WPCFLIPTRON, wpc_dispDMD, FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L), "
				"lampCol = 1, gameSpecific1 = WPC_CFTBL (commented '8 ramp lights Chase Light wired between GI outputs 1/4 and 2 bit decoder "
				"wired on solenoid outputs 20/24'), the inverted-switch mask {0x00, 0x10, 0x00, 0xc8, ...} (switches 15, 34, 37 and 38), no "
				"wpc_set_fastflip_addr call in init_cftbl, cftbl_handleMech (core_setSw(swRampUpDown, creaturerampPos) from the ramp-down and "
				"ramp-up solenoids) and the simulator's stLRamp routing; src/wpc/wpc.c's WPC_CFTBL handling, which computes chase_2b from "
				"solenoids 20 (bit 0) and 24 (bit 1) and writes 0x11 << chase_2b to the classic lamp state at 91-98, while its physical-output "
				"(modulated lamp) path ANDs that selection with G.I. triacs 0 and 3, "
				"and the WPC_GILAMPS mirror at solenoids 29-31; src/wpc/core.h CORE_FIRSTUFLIPSOL = 33 and CORE_FIRSTLFLIPSOL = 45; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCFLIPTRON = 0x8. The runtime runs used a library built from this revision."
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
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": f"external:pinmame-manuals/by-machine/{MACHINE_ID}/arcade-museum/{MANUAL_NAME}",
			"original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256,
			"locator": (
				"134-page scan of the Bally Creature from the Black Lagoon operations manual with an OCR text layer that garbles its tables, "
				"retrieved from arcade-museum.com. Every table used here was read from rendered pages: PDF 97 (printed 2-37) the cable list, "
				"PDF 100, 101 and 103 (2-40, 2-41, 2-43) the lamp, switch and solenoid/flasher location lists and drawings, PDF 106, 108 and "
				"109 (3-2, 3-4, 3-5) the switch matrix, lamp matrix and solenoid/flasher table, PDF 118-120 (3-14 to 3-16) the Chase Light II "
				"board and schematic and the flipper opto board, PDF 123 (3-19) the Fliptronic II connector list and PDF 127 (3-23) the Power "
				"Driver Board connectors."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "Bally Manufacturing Corporation; scan hosted by arcade-museum.com",
			"excerpts": [
				_excerpt("switch-locations", "PDF page 101, printed 2-41, Switch Locations parts list"),
				_excerpt("switch-drawing", "PDF page 101, printed 2-41, Switch Locations playfield drawing"),
				_excerpt("switch-matrix", "PDF page 106, printed 3-2, switch matrix with the dedicated and flipper grounded switches"),
				_excerpt("lamp-locations", "PDF page 100, printed 2-40, Lamp Locations parts list"),
				_excerpt("lamp-drawing", "PDF page 100, printed 2-40, Lamp Locations playfield drawing"),
				_excerpt("lamp-matrix", "PDF page 108, printed 3-4, lamp matrix"),
				_excerpt("solenoid-flasher-locations", "PDF page 103, printed 2-43, Solenoid/Flasher Locations, General Illumination and Flipper Coils lists"),
				_excerpt("solenoid-flasher-drawing", "PDF page 103, printed 2-43, Solenoid/Flasher Locations playfield drawing"),
				_excerpt("solenoid-flasher-wiring", "PDF page 109, printed 3-5, Solenoid/Flasher Table with the general-illumination and flipper circuits"),
				_excerpt("chase-light-board", "PDF pages 118 and 119, printed 3-14 and 3-15, Chase Light II board connectors, block diagram and schematic"),
				_excerpt("flipper-opto-board", "PDF page 120, printed 3-16, Flipper Opto Switch Board A-15894 and the end-of-stroke switches"),
				_excerpt("fliptronic-ii-board", "PDF page 123, printed 3-19, Fliptronic II board A-15472 connector list"),
				_excerpt("power-driver-board-connectors", "PDF page 127, printed 3-23, Power Driver Board connectors J118, J120 and J126"),
			],
		},
		{
			"id": PARTS_LIST_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/588/" + PARTS_LIST_NAME,
			"original_filename": PARTS_LIST_NAME,
			"sha256": PARTS_LIST_SHA256,
			"acquired_at": "2026-10-23T12:10:06Z",
			"locator": (
				"The indented factory parts list IPDB hosts for machine 588 'Creature from the Black Lagoon' (Bally, 1992), read from the raw "
				f"Wayback capture {PARTS_LIST_WAYBACK} because IPDB is Cloudflare-gated. Items 1009-1064 (the A-15621-1 ramp assembly with its "
				"chase cables and boards) and 1359-1390 (the A-15993 bowl assembly). The excerpt also reproduces the manual's own cable list "
				"(PDF 97, printed 2-37)."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "Bally Manufacturing Corporation; file hosted by the Internet Pinball Database",
			"excerpts": [_excerpt("parts-list", "Items 1009-1064 and 1359-1390, and the manual's Cable List (PDF 97, printed 2-37)", credit="curator, copied from the text file and read from the rendered cable list")],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/bally/creature-from-the-black-lagoon-1992/vpw-1-0/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME,
			"sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPW v1.0 recreation of the physical machine (table version 1.0, saved 2025-05-30). Exact playfield "
				f"bounds are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority only for the named objects its "
				"script binds; its lamp, flasher and G.I. lights feed baked light maps, and the lamps on the three socket boards, lamp 51, lamp "
				"18 and the chase lamps are placeholders off the playfield."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "VPW",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"external:pinmame-vpx-sources/bally/creature-from-the-black-lagoon-1992/vpw-1-0/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW v1.0 script (206,801 bytes). Runtime authority: Const cGameName="cftbl_l4", UseSolenoids = 2, '
				"HandleMechanics = 0, vpmMapLights AllLamps, the SolCallback/SolModCallBack table, UpdateGI and UpdateChaseLight, the switch "
				"handlers and the lift-ramp, kicker and trough code."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "VPW table authors",
			"excerpts": [_excerpt("vpw-script-bindings", "Every non-comment script line that binds the controller, with its line number", credit="curator, quoted from the script file")],
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under vpw-1-0/extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		_runtime(FLASHER_TEST_SOURCE, "creature-cftbl_l4-flasher-test.json", "cftbl-flasher-test",
			"It steps T.5 FLASHER TEST in repeat mode: the ROM names and pulses 2, 8, 9, 10, 11, 16, 17, 18, 19, 22, 25 and then 33-36 "
			"(CREATURE FL. 1-4) with their wires, and wraps."),
		_runtime(EDGES_SOURCE, "creature-cftbl_l4-switch-edges-fliptronic.json", "cftbl-switch-edges-fliptronic",
			"In T.1 SWITCH EDGES it drives the controls 25 and 34 and the upper Fliptronic positions 115-118 to 1 and back: the ROM names 25 "
			"and 34, names nothing for 115 and 117, and fires the lower right flipper for 116 and the lower left flipper for 118."),
		_runtime(FLIPPER_TEST_SOURCE, "creature-cftbl_l4-flipper-coil-test.json", "cftbl-flipper-coil-test",
			"It steps T.12 FLIPPER COIL TEST: four items, the lower right and lower left flippers' power and hold windings (45/46, 46, 47/48, "
			"48), named with their wires; it never drives 33-36."),
		_runtime(RAMP_LIGHTS_SOURCE, "creature-cftbl_l4-ramp-lights-test.json", "cftbl-ramp-lights-test",
			"It runs T.15 RAMP LIGHTS TEST: cycling, the ROM steps solenoids 20 and 24 through the four decoder codes and PinMAME's chase "
			"lamps come on in the order 91, 92, 93, 94 with 95-98 alongside; stopping it switches G.I. 0 and 3 off while PinMAME keeps "
			"publishing the selected pair."),
		_runtime(SUBWAY_SOURCE, "creature-cftbl_l4-subway-awards.json", "cftbl-subway-awards",
			"In a game, closing switch 16 flashes K-I-S-S lamp 21 and closing 17 lights Snack Bar lamp 53 with HIT TARGETS TO OPEN SNACKBAR; "
			"the ball the host then delivers to 37 is kicked out by solenoid 3."),
		_runtime(P3_FLASHER_TEST_SOURCE, "creature-cftbl_p3-flasher-test.json", "cftbl-flasher-test",
			"The L-4 flasher-test scenario replayed on the P-3 prototype ROM: it names and pulses the same fifteen flashers with the same "
			"wires, printing LFT SUBWAY FLHR for 2 and CREATURE FLSHR for 11.", "cftbl_p3"),
		_runtime(P3_EDGES_SOURCE, "creature-cftbl_p3-switch-edges-fliptronic.json", "cftbl-switch-edges-fliptronic",
			"The L-4 switch-edges scenario replayed on the P-3 prototype ROM: the same responses, with switch 25 named P OF PAID.", "cftbl_p3"),
		_runtime(P3_FLIPPER_TEST_SOURCE, "creature-cftbl_p3-flipper-coil-test.json", "cftbl-flipper-coil-test",
			"The L-4 flipper-coil-test scenario replayed on the P-3 prototype ROM: the same four items with the same names and wires.", "cftbl_p3"),
		_runtime(P3_RAMP_LIGHTS_SOURCE, "creature-cftbl_p3-ramp-lights-test.json", "cftbl-ramp-lights-test",
			"The L-4 ramp-lights-test scenario replayed on the P-3 prototype ROM: the same chase order and the same G.I. 0 and 3 switching.",
			"cftbl_p3"),
		{
			"id": CALLOUT_SOURCE,
			"kind": "human_review",
			"uri": "internal:tools/seeds/bally/creature-from-the-black-lagoon-1992-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-23 factory location-drawing callout check of PDF 100, 101 and 103 (printed 2-40, 2-41, 2-43): every callout transcribed "
				"by readers working only from the committed drawing crops, per-page control and callout fits; a table placement whose own "
				"callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py), and the placements no table "
				"object supplies are measured on the drawings. Reads, tiles and the seed generator are retained under review-artifacts with a "
				"pinned manifest."
			),
			"license": "NOASSERTION",
			"attribution": "PinMAME game definitions contributors",
		},
	]


# --- Build -------------------------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Creature from the Black Lagoon",
			"manufacturer": "Bally",
			"year": 1992,
			"kind": "physical_pinball",
			"ipdb_id": 588,
			"opdb_id": "GrNWn-MQdqZ",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx", "provenance": provenance("validated", VPX_TABLE_SOURCE)},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "conflicted",
			},
		},
		"controller": {"platform": "pinmame.wpc-fliptronic", "hardware_generation": "0x8", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": [],
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/creature-from-the-black-lagoon-1992.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Creature device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Creature mechanism {mechanism['id']} names unknown devices: {unknown}")
	drawing_callouts.apply_to_definition(definition, _callout_seed(), CALLOUT_SOURCE)
	return definition


# --- Spatial report ----------------------------------------------------------------------------------------------------
def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable_count = 0
	for device in definition["inputs"] + definition["outputs"]:
		spatial = device.get("spatial")
		if spatial is None:
			if device["availability"] in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_count += 1
			continue
		statuses[spatial["status"]].append(device["id"])
	seed = _callout_seed()
	check = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition), seed.get("limit", drawing_callouts.LIMIT))
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"parts_list_sha256": PARTS_LIST_SHA256,
			"callout_seed_sha256": _file_sha256(CALLOUT_SEED_PATH),
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/bally/creature-from-the-black-lagoon-1992-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": (
				"The VPX collision object the retained script binds to each matrix switch (trigger, kicker, target, bumper or slingshot wall), "
				"observed and validated where the switch drawing's own callout agrees within the limit. Switches 16 and 17, whose callouts the "
				"drawing transposes, keep the table object without a check. The trough switches 55-58, which the drawing labels with "
				"pointerless balloons one ball position away, keep the table's ball seats without a check and stay observed. The ramp switches 18, 35, 36, 61, 62 and "
				"64, whose table triggers sit 0.08 or more from the drawn switches or are swapped (62/64), and the lift ramp switch 38, which has "
				"no table object, are measured on the switch drawing and stay observed."
			),
			"lamp": (
				"The Light each lamp's TimerInterval binds, observed and validated where the lamp drawing's callout agrees; 28, 37 and 44 place "
				"both bulbs. The sockets of the A-14305 and C-12709 boards (55-58, 63-68) and lamp 51, which the table models only as "
				"placeholders, are measured on the lamp drawing and stay observed; the Admit One lamp 18 on the back panel takes the "
				"drawing's x at the playfield's rear edge. The backbox letters 71-78 and the Start button lamp 88 are controlled not-applicable "
				"records."
			),
			"solenoid": (
				"The script-driven flasher Light, the popper kicker, the slingshot wall or the jet bumper for each solenoid, observed and "
				"validated where the solenoid drawing's own symbol agrees. The trough and outhole coils project onto the ball seats they kick "
				"and stay observed with them, and the flipper windings project onto the flipper pivots, without a check; the hologram push motor and the lift ramp coils are "
				"measured on the drawing."
			),
			"gi": (
				"The table's G.I. light collections for strings 1, 2 and 4, as candidates only: the lights are invisible light-map sources, not "
				"modelled sockets, and no drawing or bulb count locates G.I. bulbs."
			),
		},
		"unresolved_geometry": [
			"The 32 #86 chase bulbs on the swirl ramp's three boards and the bowl's board: which bulbs belong to which of the eight strings "
			"(lamps 91-98) and which ramp boards G.I. 0 and G.I. 3 power are unresolved (conflict.chase-light-board-group-assignment), so "
			"lamps 91-98 and G.I. 0 and 3 have no placement.",
			"The general-illumination bulbs of strings 1, 2 and 4 rest on the retained table's light-map sources; no modelled socket, "
			"drawing or count locates them, so they are only candidates.",
			"The trough switches 55-58 and the trough and outhole coils rest on the table's ball seats, which the switch drawing does not "
			"mark, so they stay observed.",
			"Drawing measurements stay observed: no retained table object corroborates their positions.",
		],
		"promotion_decision": (
			"partial: the factory drawings validate most table placements, but the chase-light strings and G.I. 0 and 3 cannot be placed "
			"until their wiring is settled, the G.I. strings are only candidates, and the trough and the drawing measurements stay observed."
		),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	lines = [
		"# Creature from the Black Lagoon (Bally, 1992) spatial blockers",
		"",
		f"Retained VPW v1.0 VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest "
		f"`{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.",
		"",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/964 and y/2162 rounded to at most six places (factory-drawing "
		"measurements to three).",
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


# --- Generation ----------------------------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready Creature artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Stale Creature author-ready artifact: {AUTHOR_READY_PATH}")
	definition = build()
	report = build_spatial_report(definition)
	expected = (
		(DEFINITION_PATH, canonical_bytes(definition)),
		(SEED_PATH, canonical_bytes(definition)),
		(SPATIAL_REPORT_PATH, canonical_bytes(report)),
		(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report).encode("utf-8")),
	)
	for path, content in expected:
		target = root / path.relative_to(ROOT)
		if not target.is_file() or target.read_bytes() != content:
			raise RuntimeError(f"Creature deterministic artifact drift: {target}")
	print("Creature definition, seed and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and its generated artifacts")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, its pinned seed and the spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Creature extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Creature retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
