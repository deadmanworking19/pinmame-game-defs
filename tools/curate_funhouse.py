"""Curate the physical Williams FunHouse (1990) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring
detail, and normalized coordinate as a literal, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift,
and ``--regenerate`` is the only path that writes the canonical definition and its pinned seed.

Note on directory naming: the seeding task brief for this game named the target paths
``machines/<state>/bally/`` and ``tools/seeds/bally/funhouse.json``. FunHouse is unambiguously a
Williams machine (pinned ``CORE_GAMEDEF(fh,l9,...,"Williams",...)`` in ``fh.c``), and every other
path this task specifies (``knowledge/williams/``, ``reports/spatial/williams/``) already uses
the correct manufacturer, so "bally" is treated as a template artifact carried over from a
different game's brief -- the same class of deviation recorded for Stern The Simpsons Pinball
Party. This curator writes under ``machines/<state>/williams/`` and ``tools/seeds/williams/``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text

import drawing_callouts


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/williams/funhouse-1990.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/funhouse-1990.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/funhouse-1990.json"
CALLOUT_SEED_RELATIVE = "tools/seeds/williams/funhouse-1990-callouts.json"
CALLOUT_SEED_PATH = ROOT / CALLOUT_SEED_RELATIVE
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/funhouse-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/funhouse-1990.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-alpha"
MANUAL_SOURCE = "manual.williams.funhouse.1990"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.funhouse.1990"
OPERATOR_HANDBOOK_SOURCE = "manual.williams.funhouse.1990.operator-handbook"
PLAYFIELD_PHOTO_SOURCE = "photo.williams.funhouse.1990.a13"
VPX_TABLE_SOURCE = "vpx-table.fh-1-3"
VPX_SCRIPT_SOURCE = "vpx-script.fh-1-3"
VPX_EXTRACTION_SOURCE = "vpx-extraction.fh-1-3"
REVISION_TABLE_SOURCE = "vpx-table.fh-2-0c"
REVISION_EXTRACTION_SOURCE = "vpx-extraction.fh-2-0c"
VPXTABLE_SCRIPTS_SOURCE = "vpx-script.funhouse-community-current"
RUNTIME_GI_SOURCE = "runtime.funhouse.fh-l9.gi-test"
RUNTIME_GI_PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
PINSIDE_ORANGE_SOURCE = "forum.pinside.funhouse-gi-orange-string"
PINSIDE_VIOLET_SOURCE = "forum.pinside.funhouse-gi-violet-string"
CALLOUT_SOURCE = "human-review.funhouse.drawing-callouts"

TABLE_SHA256 = "69c37fa9a84e669a2934d6da0e5ee0277c4a0ef01e71eaa19e7271ba3396873e"
SCRIPT_SHA256 = "322fba2dec939b50e0730da8caca177545aa8f8bc055ba136360ae55deb4e863"
MANUAL_SHA256 = "b658e7d0985a5e8588981c974d9c9448ea7cc574b2d21e5acb386c718a1f0f47"
OPERATOR_HANDBOOK_SHA256 = "bb30eacaac0ee7001f59339102da5a1bfe528c2a4dbd63d2247e00fba89f1b13"
PLAYFIELD_PHOTO_SHA256 = "b56821de487adc55f128e4a94d8d55a4ef2c2e23cd1c0291f1118363c6ecaa81"

EXTRACTION_RELATIVE_PATH = Path("williams/funhouse-1990/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/funhouse-1990/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "85620e05458bd72bc57c2e203001a0f35db9806431e66e07ee08f05e90346ba9"
EXTRACTION_FILE_COUNT = 2212
EXTRACTION_TOTAL_BYTES = 219908807
# Version 2.0c of the same table, retained for the bulbs it models at the G.I. sockets.
REVISION_TABLE_SHA256 = "45ee7c7bb500749feecabd96eef6b5ffe1d4a9ff4b611176bf1155a60ca2b413"
REVISION_SCRIPT_SHA256 = "446c6bf558fd1b471000b2552c63225780535c509683b7f098c18eb709570749"
REVISION_EXTRACTION_RELATIVE_PATH = Path("williams/funhouse-1990/v2-0c/extracted-vpxtool")
REVISION_MANIFEST_RELATIVE_PATH = Path("williams/funhouse-1990/v2-0c/extracted-vpxtool.manifest.json")
REVISION_MANIFEST_SHA256 = "f05e57012e5f7290f74bd50e986e6668b5721c066cf9d1c0612c18747f5b7595"
REVISION_FILE_COUNT = 2695
REVISION_TOTAL_BYTES = 216969293

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

# --- Driver tree -----------------------------------------------------------------------------
DRIVER_IDS = (
	"fh_l9", "fh_d9", "fh_l9b", "fh_d9b", "fh_905h", "fh_905hbs", "fh_906h", "fh_907h", "fh_pa1",
	"fh_l2", "fh_l3", "fh_d3", "fh_l4", "fh_d4", "fh_l5", "fh_d5", "fh_f91",
)
DRIVER_COMPATIBILITY = {
	"fh_l9": ("identical", "Williams production L-9 game ROM (sound level SL-3) shipped with the physical machine; the switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are the reference for this definition."),
	"fh_d9": ("identical", "D-9 game ROM; an LED ghost-fix revision of L-9 with no controller-address or playfield change."),
	"fh_l9b": ("identical", "L-9 with an unofficial improved German translation MOD; no controller-address or playfield change."),
	"fh_d9b": ("identical", "D-9 with the same unofficial improved German translation MOD and LED ghost fix; no controller-address or playfield change."),
	"fh_905h": ("identical", "9.05H game ROM. This is the driver the retained known-working script binds to (Const cGameName=\"fh_905h\"); it drives the identical I/O inventory as L-9."),
	"fh_906h": ("identical", "9.06H Coin Play game ROM; a later firmware revision of the same physical machine with no controller-address or playfield change."),
	"fh_905hbs": ("identical", "9.05H with a 2026 ball-saver MOD by whaslbeck, made independently of 9.07H; the pinned source declares it a CORE_CLONEDEF of L-9 on the same game data, so no controller-address or playfield change."),
	"fh_907h": ("identical", "9.07H ball-saver MOD, a community patch of 9.05H (which already carries the LED ghost fix); no controller-address or playfield change."),
	"fh_pa1": ("compatible", "Prototype PA-1 game ROM (labeled L-2, System 11 sound). Pinned PinMAME binds it to a distinct GEN_WPCALPHA_1 core_tGameData (fhpa1GameData) rather than the production fhGameData, reflecting the earlier WPC-Alpha-1/System-11 sound-board generation used before the machine's WPC-Alpha-2 sound board shipped. The switch, solenoid, lamp, and mechanism definitions transcribed here are unchanged between the two structs. The prototype struct also retains a stale gameSpecific1=1 copied before production FunHouse was corrected: pinned wpc.c therefore executes the unrelated WPC_CFTBL chase-light integrator and writes internal PWM lamp slots 65-72 from solenoids 20/24 and G.I. bits 0/3, but lampCol=0 keeps the public lamp count at 64. Those internal slots are a pinned-source defect, not fitted FunHouse lamps. This remains the same physical playfield with an earlier sound subsystem, not a different machine."),
	"fh_l2": ("identical", "L-2 game ROM, the earliest production-generation firmware retained by PinMAME; no controller-address or playfield change from L-9."),
	"fh_l3": ("identical", "L-3 game ROM; no controller-address or playfield change."),
	"fh_d3": ("identical", "D-3 game ROM, an LED ghost-fix revision of L-3; no controller-address or playfield change."),
	"fh_l4": ("identical", "L-4 game ROM; no controller-address or playfield change."),
	"fh_d4": ("identical", "D-4 game ROM, an LED ghost-fix revision of L-4; no controller-address or playfield change."),
	"fh_l5": ("identical", "L-5 game ROM; no controller-address or playfield change."),
	"fh_d5": ("identical", "D-5 game ROM, an LED ghost-fix revision of L-5; no controller-address or playfield change."),
	"fh_f91": ("identical", "FreeWPC 0.91 community firmware for the same physical hardware; no controller-address or playfield change asserted by the pinned driver record."),
}

# --- Printed switch tables (manual pages 2-38 locations, 2-39 wiring/matrix) ------------------
SWITCH_LABELS = {
	11: "Right Flipper", 12: "Left Flipper", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Steps Lights Frenzy", 16: "Upper Ramp Switch", 17: 'S-T-E-P "S"', 18: "Left Jet Bumper",
	21: "Slam Tilt", 22: "Front Door", 24: "Test Position (Always Closed)",
	25: "Lock Mech Right", 26: "Steps Lights Ex. Ball", 27: "Lock Mech Center", 28: "Lock Mech Left",
	31: 'S-T-E-P "P"', 32: "Top Superdog Standup Target", 33: "Lt. Gangway Rollunder",
	34: "Bottom Superdog Standup Target", 35: "Steps Track Lower", 36: "Steps 500,000",
	37: "Center Superdog Standup Target", 38: "Steps Track Upper",
	41: "Left Slingshot", 42: "Lt. Flipper Return Lane", 43: "Left Outlane",
	44: "Wind Tunnel Hole", 45: "Trap Door Open", 46: "Rudy Hideout Kickbig",
	47: "Left Ballshooter", 48: "Ramp Exit Track",
	51: "Dummy Jaw", 52: "Right Outlane", 53: "Right Slingshot", 54: 'S-T-E-P "T"',
	55: "Steps Superdog", 56: "Ramp Entrance", 57: "Jet Bumper Lane", 58: "Tunnel Kickout",
	61: "Rt. Inside Return Lane", 62: "Right Ballshooter", 63: "Right Trough", 64: 'S-T-E-P "E"',
	65: "Dummy Eject Hole", 66: "Right Gangway Lane", 67: "Lower Right Drop Hole", 68: "Lower Jet Bumper",
	71: "Rt. Outside Return Lane", 72: "Left Trough", 73: "Outhole", 74: "Center Trough",
	75: "Upper Right Loop", 76: "Trap Door Closed", 77: "Right Jet Bumper",
}
# 78, 81-88 are all printed "Not Used"; 23 (Ticket Dispenser) is separately printed "Not Used".
UNUSED_MATRIX_ADDRESSES = {23, 78, 81, 82, 83, 84, 85, 86, 87, 88}
STEPS_SWITCHES = {15, 26, 36}
# The only two switches this manual marks "(opto)" anywhere -- neither the switch-locations page
# nor the switch-matrix page shades any cell for opto construction on this machine.
OPTO_SWITCHES = {51, 55}
SWITCH_PARTS = {
	11: "A-9990-1", 12: "A9989-1", 13: "20-9663-1", 14: "20-6502-A", 15: "5647-12073-21",
	16: "5647-12073-21", 17: "B-12001-1", 18: "B-12030-2",
	21: "27-1066", 22: "A-8630", 24: "A-8630",
	25: "A-14138", 26: "5647-12073-21", 27: "A-14138", 28: "A-14138",
	31: "B-12001-1", 32: "B-12001-4", 33: "A-12010", 34: "B-12001-4", 35: "5647-12073-21",
	36: "5647-12073-21", 37: "B-12001-4", 38: "5647-12073-21",
	41: "A-4834-H", 42: "A-12688", 43: "A-12688", 44: "A-12238", 45: "A-12238",
	46: "A-11608", 47: "A-11619-1", 48: "5647-12073-21",
	51: "A-13901", 52: "A-12688", 53: "A-4843-H", 54: "B-12583-1", 55: "A-13901",
	56: "5647-12073-21", 57: "A-12688", 58: "5647-12073-25",
	61: "A-12688", 62: "A-11619", 63: "p/o B-8925", 64: "B-12583-1", 65: "5647-12073-43",
	66: "A-12688", 67: "A-12238", 68: "B-12030-2",
	71: "A-12688", 72: "A-11680", 73: "A-10417", 74: "p/o B-8925", 75: "A-12688",
	76: "5647-12001-00", 77: "B-12030-2",
}
SWITCH_TYPES = {
	11: "leaf", 12: "leaf", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch",
	17: "microswitch", 18: "other", 21: "leaf", 22: "microswitch", 24: "other",
	25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "microswitch", 32: "microswitch", 33: "microswitch", 34: "microswitch",
	35: "microswitch", 36: "microswitch", 37: "microswitch", 38: "microswitch",
	41: "leaf", 42: "microswitch", 43: "microswitch", 44: "microswitch", 45: "microswitch",
	46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "opto", 52: "microswitch", 53: "leaf", 54: "microswitch", 55: "opto",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch",
	65: "microswitch", 66: "microswitch", 67: "microswitch", 68: "other",
	71: "microswitch", 72: "microswitch", 73: "microswitch", 74: "microswitch",
	75: "microswitch", 76: "microswitch", 77: "other",
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-7"),
	3: ("Orange-Black", "J205-3", "U17-11"), 4: ("Orange-Yellow", "J205-4", "U17-9"),
	5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
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
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"),
	3: ("Green-Orange", "J207-3", "U20-16"), 4: ("Green-Yellow", "J207-4", "U20-15"),
	5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-8", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"),
	3: ("White-Orange", "J209-3", "U18-5"), 4: ("White-Yellow", "J209-4", "U18-7"),
	5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}

# --- Printed solenoid/GI table (manual page 2-40) ---------------------------------------------
SOLENOID_LABELS = {
	1: "Outhole", 2: "Ramp Diverter", 3: "Kickbig", 4: "Tunnel Kickbig",
	5: "Trap Door Open", 6: "Trap Door Closed", 7: "Knocker", 8: "Multi-ball Release",
	9: "Left Jet Bumper", 10: "Right Jet Bumper", 11: "Lower Jet Bumper",
	12: "Left Slingshot", 13: "Right Slingshot", 14: "Steps Gate", 15: "Trough",
	16: "Dummy Eject Hole", 17: "3 Blue Flashers", 18: "Dummy Flashers", 19: "2 Clock Flashers",
	20: "2 Superdog Flashers", 21: "Mouth Motor", 22: "Up/Down Driver", 23: "3 Red Flashers",
	24: "3 Clear Flashers", 25: "Eyes Right", 26: "Eyelids Open", 27: "Eyelids Close", 28: "Eyes Left",
}
SOLENOID_PARTS = {
	1: "AE-26-1200", 2: "AE-26-1200", 3: "AE-26-1500", 4: "AE-26-1200", 5: "AE-26-1500",
	6: "SM1-26-600", 7: "AE-23-800", 8: "A-14189", 9: "AE-26-1200", 10: "AE-26-1200",
	11: "AE-26-1200", 12: "AE-26-1500", 13: "AE-26-1500", 14: "SZ-34-3500", 15: "AE-26-1200",
	16: "AE-26-1500", 17: "#906", 18: "#906", 19: "#906", 20: "#906", 21: "A-13997",
	22: "C-13963", 23: "#906", 24: "#906", 25: "SM-30-1100", 26: "SM-30-1100",
	27: "SM-30-1100", 28: "SM-30-1100",
}
FLASHER_QUANTITIES = {17: 3, 18: 1, 19: 2, 20: 2, 23: 3, 24: 3}
SOLENOID_WIRING = {
	1: dict(control_connection="J130-1", driver_transistor="Q82", printed_type="High Power"),
	2: dict(control_connection="J130-2", driver_transistor="Q80", printed_type="High Power"),
	3: dict(control_connection="J130-4", driver_transistor="Q78", printed_type="High Power"),
	4: dict(control_connection="J130-5", driver_transistor="Q76", printed_type="High Power"),
	5: dict(control_connection="J130-6", driver_transistor="Q64", printed_type="High Power"),
	6: dict(control_connection="J130-7", driver_transistor="Q66", printed_type="High Power"),
	7: dict(control_connection="J130-8", driver_transistor="Q68", printed_type="High Power"),
	8: dict(control_connection="J130-9", driver_transistor="Q70", printed_type="High Power"),
	9: dict(control_connection="J127-1", driver_transistor="Q58", printed_type="Low Power"),
	10: dict(control_connection="J127-2", driver_transistor="Q56", printed_type="Low Power"),
	11: dict(control_connection="J127-4", driver_transistor="Q54", printed_type="Low Power"),
	12: dict(control_connection="J127-5", driver_transistor="Q52", printed_type="Low Power"),
	13: dict(control_connection="J127-6", driver_transistor="Q50", printed_type="Low Power"),
	14: dict(control_connection="J127-7", driver_transistor="Q48", printed_type="Low Power"),
	15: dict(control_connection="J127-8", driver_transistor="Q46", printed_type="Low Power"),
	16: dict(control_connection="J127-9", driver_transistor="Q44", printed_type="Low Power"),
}
# Retained VPW-style script callbacks (SolCallback array), per solenoid address.
SOLENOID_CALLBACKS = {
	1: "kisort (Outhole)", 2: "SolRampDiverter", 3: "bsHideout.SolOut", 4: "SolKickout",
	5: "SolTrapDoorO", 6: "SolTrapDoorC", 7: 'vpmSolSound SoundFX("fx_knocker",DOFKnocker)',
	8: "MBRelease", 14: "SolFlipperDiverter", 15: "KickBallToLane", 16: "bsRudy.SolOut",
	17: "SetBlueDome", 18: "setlamp 118,", 19: "setlamp 119,", 20: "setlamp 120,",
	23: "SetRedDome", 24: "SetWhiteDome", 25: "SolEyesRight", 26: "SolEyesOpen",
	27: "SolEyesClosed", 28: "SolEyesLeft",
}

# --- General illumination (ROM T.6 test, manual page 2-40, handbook page 5) --------------------
# Labels are the names the L-9 ROM's T.6 G.I. test prints for each public string.
GI_LABELS = {
	0: "Backglass Upper G.I.", 1: "Rudy / Backglass G.I.", 2: "Rear Playfield G.I.",
	3: "Backglass Center G.I.", 4: "Front Playfield G.I.",
}
# T.6 screens per public string: name, Start screen (wires), P.F. pins, B.B. pins, fuse, driver.
GI_ROM_SCREENS = {
	0: ("BACKGLASS UPPER", "WHT-BRN BRN", "P.F. J120-7 120-1", "B.B. J121-7 121-1", "F110 5 AMP S.B.", "DRIVER Q18"),
	1: ("RUDY / BACKGLASS", "WHT-ORN ORN", "P.F. J120-8 120-2", "B.B. J121-8 121-2", "F109 5 AMP S.B.", "DRIVER Q10"),
	2: ("REAR PLAYFIELD", "WHT-YEL YEL", "P.F. J120-9 120-3", "B.B. J121-9 121-3", "F108 5 AMP S.B.", "DRIVER Q14"),
	3: ("BACKGLASS CENTER", "WHT-GRN GRN", "P.F. J120-10 120-5", "B.B. J121-10 121-5", "F107 5 AMP S.B.", "DRIVER Q16"),
	4: ("FRONT PLAYFIELD", "WHT-VIO VIO", "P.F. J120-11 120-6", "B.B. J121-11 121-6", "F106 5 AMP S.B.", "DRIVER Q12"),
}
# The printed row of the same number, literally: the 2-40 list name and the handbook's name, return wire, pin and triac.
GI_PRINTED_ROWS = {
	0: ('2-40 "01 Upper Backglass G.I."', 'handbook "01 Upper Backglass, White-Brown, J120-7, Q18"'),
	1: ('2-40 "02 Front Playfield G.I."', 'handbook "02 Front Playfield, White-Violet, J119-1, Q10"'),
	2: ('2-40 "03 Rear Playfield G.I."', 'handbook "03 Rear Playfield, White-Yellow, J121-9, Q14"'),
	3: ('2-40 "04 Cntr Bckglss/Rt. Rr Plfld G.I."', 'handbook "04 Center Backglass / Right Rear Playfield, White-Orange, J120-8, Q16"'),
	4: ('2-40 "05 Top Playfield G.I."', 'handbook "05 Top Playfield, White-Green, J120-10, Q12"'),
}
GI_PRINTED_NOTE = (
	"Both printed lists keep their transistor column in string order (Q18, Q10, Q14, Q16, Q12 for strings 1-5), but rows 02, "
	"04 and 05 carry their names, wires and pins one string out of place: on the power driver board Q10 drives orange "
	"(J120-2/J120-8), Q16 green (J120-5/J120-10) and Q12 violet (J120-6/J120-11 and the J119 cabinet branch), and the ROM's "
	"T.6 test prints exactly those wires, pins and fuses for public strings 1, 3 and 4. The name follows the wire: \"Front "
	"Playfield\" (white-violet, J119-1) is public 4, \"Center Backglass / Right Rear Playfield\" (white-orange, J120-8) is "
	"public 1, and \"Top Playfield\" (white-green, J120-10) stands where the ROM names public 3 BACKGLASS CENTER. This is a "
	"wiring-detail misprint of the kind Terminator 2's tables carry, not a disagreement about the machine."
)
GI_SCRIPT_REGIONS = {
	0: "Upper BackGlass (Case 0, no handler)", 1: "Rudy (Case 1)", 2: "Upper Playfield (Case 2)",
	3: "Center BackGlass (Case 3, no handler)", 4: "Lower Playfield (Case 4)",
}
# Board-internal wiring per public string, as the ROM's T.6 screens print it; J119 is the violet cabinet branch the
# 2-40 interboard table (3-17) prints.
GI_FEED_WIRING = {
	0: dict(control_connection="J120-1", control_wire="Brown", driver_transistor="Q18", insert_connection="J121-1", return_connection="J120-7 / J121-7", return_wire="White-Brown", return_component="F110"),
	1: dict(control_connection="J120-2", control_wire="Orange", driver_transistor="Q10", insert_connection="J121-2", return_connection="J120-8 / J121-8", return_wire="White-Orange", return_component="F109"),
	2: dict(control_connection="J120-3", control_wire="Yellow", driver_transistor="Q14", insert_connection="J121-3", return_connection="J120-9 / J121-9", return_wire="White-Yellow", return_component="F108"),
	3: dict(control_connection="J120-5", control_wire="Green", driver_transistor="Q16", insert_connection="J121-5", return_connection="J120-10 / J121-10", return_wire="White-Green", return_component="F107"),
	4: dict(control_connection="J120-6 / J119-3", control_wire="Violet", driver_transistor="Q12", insert_connection="J121-6", return_connection="J120-11 / J121-11 / J119-1", return_wire="White-Violet", return_component="F106"),
}

# --- Printed lamp table (manual pages 2-36 locations, 2-37 wiring) ----------------------------
LAMP_LABELS = {
	11: "Gangway 75,000", 12: "Gangway 100,000", 13: "Gangway 150,000", 14: "Gangway 200,000",
	15: "Gangway 250,000", 16: "Gangway Lights Extra Ball", 17: "Shoot Again", 18: "Steps Open (Gate)",
	21: "Clock 45 Minutes", 22: "Clock 8 O'Clock", 23: "Clock 6 O'Clock", 24: "Clock 25 Minutes",
	25: "Clock 15 Minutes", 26: "Clock 10 Minutes", 27: "Clock 12 Minutes", 28: "Clock 0 Minutes",
	31: "Clock 40 Minutes", 32: "Clock 35 Minutes", 33: "Clock 30 Minutes", 34: "Clock 20 Minutes",
	35: "Clock 3 O'Clock", 36: "Clock 1 O'Clock", 37: "Clock 11 O'Clock", 38: "Clock 50 Minutes",
	41: "Clock 9 O'Clock", 42: "Clock 7 O'Clock", 43: "Clock 5 O'Clock", 44: "Clock 4 O'Clock",
	45: "Clock 2 O'Clock", 46: "Clock 5 Minutes", 47: "Clock 55 Minutes", 48: "Clock 10 O'Clock",
	51: "Lower Jet Bumper", 52: "Upper Jet Bumper", 53: "Superdog Lamp", 54: "Steps Lights Frenzy",
	55: "Steps Lights Ex. Ball", 56: "Steps 500,000", 57: "Ramp Overhead Lamp",
	58: "Rt. Gangway Overhead Lamp", 61: "Rt. Flipper Lanes", 62: 'S-T-E-P "S"',
	63: "Trap Door Bonus", 64: "Ramp Scores 250,000", 65: 'S-T-E-P "T"', 66: "Upper Lt. Gangway Lane",
	67: "Extra Ball Lamp", 68: "Lock", 71: "Magic Mirror Lights Ex. Ball", 72: "Upper Rt. Jet Bumper",
	73: 'S-T-E-P "P"', 74: "Magic Mirror Lights Million", 75: "Magic Mirror Lights Jet Bumper",
	76: "Magic Mirror Lights Superdog", 77: "Magic Mirror Opens Gate",
	78: "Magic Mirror Lights Quick Multi-ball", 81: "Million Plus", 82: "Special Outlanes",
	83: "Trap Door Frenzy", 84: 'Ramp "Steps" Lamp', 85: "Magic Mirror Arrow", 86: 'S-T-E-P "E"',
	87: "Million", 88: "Start Button",
}
LAMP_BULBS = {addr: ("#44" if addr in {17, 53, 57, 58, 61, 62, 65, 66, 73, 82, 85, 86, 87} else "#555") for addr in LAMP_LABELS}
LAMP_QUANTITIES = {53: 2, 61: 2, 82: 2}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J138-1", "Q98"), 2: ("Yellow-Red", "J138-2", "Q97"),
	3: ("Yellow-Orange", "J138-3", "Q96"), 4: ("Yellow-Black", "J138-4", "Q95"),
	5: ("Yellow-Green", "J138-5", "Q94"), 6: ("Yellow-Blue", "J138-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-3", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}

# --- Normalized playfield coordinates from the retained VPX extraction (x/964, y/2162) --------
# The Steps switches 15, 26 and 36 and the Steps lamps 54-56 are drawing measurements in the callout seed instead.
SWITCH_POSITIONS = {
	16: [(0.687465, 0.112309)], 17: [(0.15384, 0.596574)], 18: [(0.615994, 0.443693)],
	25: [(0.288262, 0.135109)], 27: [(0.239196, 0.147339)],
	28: [(0.193812, 0.158922)], 31: [(0.554663, 0.521479)], 32: [(0.512372, 0.454203)],
	33: [(0.158116, 0.067089)], 34: [(0.528313, 0.504013)], 35: [(0.140276, 0.628762)],
	37: [(0.520533, 0.479226)], 38: [(0.761925, 0.390557)],
	41: [(0.211364, 0.738475)], 42: [(0.131072, 0.7303)], 43: [(0.054941, 0.715251)],
	44: [(0.374725, 0.280513)], 45: [(0.711618, 0.346901)], 46: [(0.78147, 0.13193)],
	47: [(0.059097, 0.89204)], 48: [(0.831538, 0.427095)], 51: [(0.630723, 0.273491)],
	52: [(0.875051, 0.75622)], 53: [(0.657699, 0.73899)], 54: [(0.209337, 0.383022)],
	55: [(0.400243, 0.157399)], 56: [(0.262034, 0.325482)], 57: [(0.859425, 0.623967)],
	58: [(0.732298, 0.567893)], 61: [(0.73663, 0.720266)], 62: [(0.943105, 0.888831)],
	63: [(0.877269, 0.863859)],
	64: [(0.33837, 0.348324)], 65: [(0.660429, 0.20844)], 66: [(0.93145, 0.187398)],
	67: [(0.820074, 0.578718)], 68: [(0.764603, 0.518256)], 71: [(0.804597, 0.71963)],
	72: [(0.769422, 0.891111)], 74: [(0.824195, 0.877197)], 75: [(0.849795, 0.10813)],
	76: [(0.81201, 0.238809)], 77: [(0.843763, 0.431839)],
	73: [(0.500721, 0.960313)],
}
SOLENOID_POSITIONS = {
	1: [(0.500721, 0.960313)], 2: [(0.900092, 0.335841)], 3: [(0.78147, 0.13193)],
	4: [(0.693624, 0.61287)], 5: [(0.81201, 0.238809)], 6: [(0.81201, 0.238809)],
	8: [(0.194789, 0.184393)], 9: [(0.615994, 0.443693)], 10: [(0.843763, 0.431839)],
	11: [(0.764603, 0.518256)], 12: [(0.211364, 0.738475)], 13: [(0.657699, 0.73899)],
	14: [(0.100533, 0.84034)], 15: [(0.877269, 0.863859)], 16: [(0.660429, 0.20844)],
	# The back-panel Flupper domes Flasher1, Flasher2 and Flasher6 are placed at their world-space mesh bounds centres.
	17: [(0.605635, 0.075096), (0.257915, 0.313511), (0.931763, 0.490629)],
	18: [(0.585264, 0.326788)],
	19: [(0.434362, 0.658164)],
	20: [(0.446452, 0.46247), (0.460268, 0.512137)],
	23: [(0.764751, 0.096573), (0.252168, 0.291859), (0.932054, 0.531739)],
	24: [(0.927329, 0.118305), (0.247033, 0.270019), (0.932168, 0.572932)],
	21: [(0.630723, 0.273491)], 22: [(0.630723, 0.273491)],
	# PrLids' world-space mesh bounds centre (vpxtool export obj --units vpu): x 528.0463..725.6938, y 454.4735..537.1692.
	25: [(0.65028, 0.229335)], 26: [(0.65028, 0.229335)],
	27: [(0.65028, 0.229335)], 28: [(0.65028, 0.229335)],
}

LAMP_POSITIONS = {
	11: [(0.277891, 0.790845)], 12: [(0.333362, 0.807742)], 13: [(0.402002, 0.816214)],
	14: [(0.466973, 0.815765)], 15: [(0.532204, 0.80782)], 16: [(0.588464, 0.791557)],
	17: [(0.433283, 0.874712)], 18: [(0.054838, 0.789026)], 21: [(0.278513, 0.657338)],
	22: [(0.359429, 0.676949)], 23: [(0.434301, 0.69581)], 24: [(0.510799, 0.716611)],
	25: [(0.58777, 0.658429)], 26: [(0.568217, 0.624502)], 27: [(0.43313, 0.609972)],
	28: [(0.433493, 0.564827)], 31: [(0.299, 0.691676)], 32: [(0.356261, 0.71648)],
	33: [(0.432843, 0.725435)], 34: [(0.567373, 0.692154)], 35: [(0.519884, 0.657824)],
	36: [(0.476797, 0.625099)], 37: [(0.390122, 0.625103)], 38: [(0.299934, 0.623783)],
	41: [(0.347821, 0.657825)], 42: [(0.390515, 0.690546)], 43: [(0.476207, 0.690458)],
	44: [(0.509063, 0.676773)], 45: [(0.508473, 0.638964)], 46: [(0.511423, 0.59882)],
	47: [(0.356393, 0.598672)], 48: [(0.359823, 0.638964)], 51: [(0.765445, 0.51738)],
	# 57 and 58 are the overhead BulbFil2 and BulbFil1 filament bulbs, not the wf_on_blur sprites the script flashes.
	52: [(0.61674, 0.442817)], 57: [(0.262382, 0.322563)], 58: [(0.665407, 0.535709)],
	53: [(0.453204, 0.476406), (0.459149, 0.498521)],
	61: [(0.129717, 0.690238), (0.735779, 0.675768)], 62: [(0.185918, 0.623502)],
	63: [(0.437713, 0.41654)], 64: [(0.283597, 0.377782)], 65: [(0.230091, 0.418084)],
	66: [(0.158393, 0.410765)], 67: [(0.468272, 0.293594)], 68: [(0.47594, 0.255018)],
	# The Magic Mirror lamps 71 and 74-78 are the L71 and L74-L78 lamp-glass primitives at their world-space mesh bounds
	# centres; F71 and F71a are f_refl sprites.
	71: [(0.337732, 0.202892)],
	72: [(0.844033, 0.430917)], 73: [(0.542804, 0.551548)], 74: [(0.337743, 0.205808)],
	75: [(0.337751, 0.209287)], 76: [(0.337771, 0.21355)], 77: [(0.337741, 0.217175)],
	78: [(0.33772, 0.223001)], 81: [(0.267608, 0.453786)], 82: [(0.054208, 0.678508), (0.876241, 0.698937)],
	83: [(0.357697, 0.433994)], 84: [(0.302018, 0.41577)], 85: [(0.391661, 0.348521)],
	86: [(0.350594, 0.378278)], 87: [(0.4368, 0.382814)],
}
# Rudy's spotlight: the RudyShade Light under the pShade1/pShade2 lamp-shade primitives. RudySign1/RudySign2 are f_refl
# glow sprites the table paints on Rudy and are not sockets.
GI_RUDY_POSITIONS = [(0.76868, 0.317499)]
# Public string: (retained 1.3 table's G.I. collection the script's handler drives, the 2.0c table's bulb collection the
# same string drives through ModLampz.MassAssign).
GI_COLLECTIONS = {2: ("GI_Upper", "GI_UpperBulbs"), 4: ("GI_Lower", "GI_LowerBulbs")}
GI_MATCH_LIMIT = 0.01
# Playfield G.I. sockets of public 2 and 4, rear to front: (the retained 1.3 table's Light, the bulb glass primitive the 2.0c
# revision of the same table models under a Light its script drives from the same string, the 1.3 Light's normalized
# position). Each 1.3 Light within GI_MATCH_LIMIT of such a bulb joins that bulb's socket, and of the co-located render
# doubles the placement is the one that shows its own bulb mesh, else the one on a BulbFil filament primitive, else the one
# with the smallest falloff radius. A Light no 2.0c bulb lies under makes no socket (docs/SPATIAL.md, picking the bulb).
# derive_gi_sockets() recomputes this table and GI_UNMATCHED from both retained extractions.
GI_SOCKETS: dict[int, tuple[tuple[str, str, tuple[float, float]], ...]] = {
	2: (
		("Light18", "pBulb21", (0.159636, 0.026365)), ("Light24", "pBulb23", (0.893615, 0.028146)),
		("Light17", "pBulb22", (0.056362, 0.061723)), ("Light25", "pBulb24", (0.952628, 0.064875)),
		("Light20", "pBulb20", (0.299793, 0.083924)), ("Light19", "pBulb19", (0.176233, 0.11846)),
		("Light23", "pBulb18", (0.540764, 0.131754)), ("Light21", "pBulb17", (0.358806, 0.189862)),
		("Light39", "pBulb16", (0.166603, 0.275318)), ("Light12", "pBulb14", (0.049908, 0.331432)),
		("Light8", "pBulb15", (0.191442, 0.334527)), ("Light26", "pBulb25", (0.897303, 0.336229)),
		("Light13", "pBulb13", (0.063739, 0.371313)), ("Light14", "pBulb12", (0.078492, 0.40256)),
	),
	4: (
		("LowerGI_B19", "pBulb8", (0.563099, 0.472939)), ("Light38", "pBulb11", (0.060409, 0.506492)),
		("Light34", "pBulb9", (0.121318, 0.570539)), ("Light35", "pBulb10", (0.120396, 0.583696)),
		("Light37", "pBulb7", (0.777842, 0.623165)), ("Light33", "pBulb1", (0.215693, 0.767503)),
		("Light30", "pBulb6", (0.661275, 0.768162)), ("Light29", "pBulb5", (0.767688, 0.792313)),
		("Light31", "pBulb2", (0.150942, 0.807551)), ("Light27", "pBulb4", (0.686954, 0.817347)),
		("Light32", "pBulb3", (0.20094, 0.8229)),
	),
}
GI_UNMATCHED = {2: ("Light22",), 4: ("Bottom_GI_32", "Bottom_GI_39", "LowerGI_B14")}
GI_UPPER_POSITIONS = [position for _, _, position in GI_SOCKETS[2]]
GI_LOWER_POSITIONS = [position for _, _, position in GI_SOCKETS[4]]


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"FunHouse retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{
				"path": path.relative_to(extraction_root).as_posix(),
				"size": path.stat().st_size,
				"sha256": _file_sha256(path),
			}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained FunHouse extraction")
		return None
	return Path(value).expanduser().resolve()


def _verify_manifest(source_root: Path, extraction: Path, manifest: Path, identity: tuple[int, int, str]) -> dict[str, Any]:
	extraction_root = source_root / extraction
	manifest_path = source_root / manifest
	if not manifest_path.is_file():
		raise RuntimeError(f"FunHouse retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"FunHouse retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != identity:
		raise RuntimeError(
			f"FunHouse retained extraction identity mismatch under {extraction_root}: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	identity = (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256)
	return _verify_manifest(source_root, EXTRACTION_RELATIVE_PATH, EXTRACTION_MANIFEST_RELATIVE_PATH, identity)


def verify_revision_manifest(source_root: Path) -> dict[str, Any]:
	identity = (REVISION_FILE_COUNT, REVISION_TOTAL_BYTES, REVISION_MANIFEST_SHA256)
	return _verify_manifest(source_root, REVISION_EXTRACTION_RELATIVE_PATH, REVISION_MANIFEST_RELATIVE_PATH, identity)


def _gameitem(extraction_root: Path, kind: str, name: str) -> dict[str, Any]:
	return json.loads((extraction_root / "gameitems" / f"{kind}.{name}.json").read_text(encoding="utf-8"))[kind]


def _collection(extraction_root: Path, name: str) -> list[str]:
	collections = json.loads((extraction_root / "collections.json").read_text(encoding="utf-8"))
	return next(item["items"] for item in collections if item["name"] == name)


def _primitives(extraction_root: Path, prefix: str) -> dict[str, tuple[float, float]]:
	items = {}
	for path in (extraction_root / "gameitems").glob(f"Primitive.{prefix}*.json"):
		item = json.loads(path.read_text(encoding="utf-8"))["Primitive"]
		items[item["name"]] = (item["position"]["x"], item["position"]["y"])
	return items


def _normalized(x: float, y: float) -> tuple[float, float]:
	return round(x / 964.0, 6), round(y / 2162.0, 6)


def derive_gi_sockets(source_root: Path) -> tuple[dict[int, tuple[tuple[str, str, tuple[float, float]], ...]], dict[int, tuple[str, ...]]]:
	"""Recompute GI_SOCKETS from both retained extractions, and name each driven light no 2.0c bulb lies under."""
	table = source_root / EXTRACTION_RELATIVE_PATH
	revision = source_root / REVISION_EXTRACTION_RELATIVE_PATH
	filaments = _primitives(table, "BulbFil")
	glasses = _primitives(revision, "pBulb")
	sockets: dict[int, tuple[tuple[str, str, tuple[float, float]], ...]] = {}
	unmatched: dict[int, tuple[str, ...]] = {}
	for public, (collection, bulb_collection) in GI_COLLECTIONS.items():
		bulbs: dict[str, tuple[float, float]] = {}
		for name in _collection(revision, bulb_collection):
			centre = _gameitem(revision, "Light", name)["center"]
			under = [glass for glass, (x, y) in glasses.items() if math.hypot(x - centre["x"], y - centre["y"]) <= 1.0]
			if len(under) != 1:
				raise RuntimeError(f"2.0c light {name} must sit on exactly one bulb glass, found {under}")
			bulbs[under[0]] = _normalized(*glasses[under[0]])
		groups: dict[str, list[tuple[tuple[bool, bool, float, str], str, tuple[float, float]]]] = {}
		missing = []
		for name in _collection(table, collection):
			light = _gameitem(table, "Light", name)
			x, y = light["center"]["x"], light["center"]["y"]
			position = _normalized(x, y)
			distance, bulb = min((math.dist(position, centre), glass) for glass, centre in bulbs.items())
			if distance > GI_MATCH_LIMIT:
				missing.append(name)
				continue
			on_filament = any(math.hypot(fx - x, fy - y) <= 1.0 for fx, fy in filaments.values())
			rank = (not light["show_bulb_mesh"], not on_filament, light["falloff_radius"], name)
			groups.setdefault(bulb, []).append((rank, name, position))
		chosen = [(min(members)[1], bulb, min(members)[2]) for bulb, members in groups.items()]
		sockets[public] = tuple(sorted(chosen, key=lambda item: (item[2][1], item[2][0])))
		unmatched[public] = tuple(sorted(missing))
	return sockets, unmatched


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
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
				"provenance": provenance(*source_refs),
			}
		)
	return {"status": "validated", "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def measured(identifier: str, role: str) -> dict[str, Any]:
	"""Place a device from its drawing measurements in the callout seed, each reproduced through its page's control fit."""
	seed = load_json(CALLOUT_SEED_PATH)
	keys = sorted(key for key, item in seed["measurements"].items() if item["device"] == identifier)
	if not keys:
		raise RuntimeError(f"no drawing measurement for {identifier}")
	placements = []
	for key in keys:
		if not key.startswith(f"{identifier}.{role}."):
			raise RuntimeError(f"drawing measurement {key} does not belong to {identifier}")
		x, y = drawing_callouts.measured(seed, key)
		placements.append({"id": key, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(OPERATOR_HANDBOOK_SOURCE, CALLOUT_SOURCE)})
	return {"status": "validated", "placements": placements}


# Committed crops are binary, so unlike the transcriptions they are hashed from
# the file on disk rather than from a literal in this curator.
EXCERPT_IMAGE_HASHES = {
	path.name: hashlib.sha256(path.read_bytes()).hexdigest()
	for path in sorted((ROOT / "evidence/excerpts/williams.funhouse.1990").glob("*.webp"))
}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the fh_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/fh.c fhGameData GEN_WPCALPHA_2 with wpc_dispAlpha, FLIP_SWNO(12,11) "
				"(flipper switches only, no FLIP_SOL -- no CPU-controlled flipper solenoid is declared for this "
				"driver), the inverted-switch mask {0x00,0x00,0x00,0x00,0x00,0x11,0x00,0x00,0x00,0x00,0x00,0x00} "
				"(column 5 = 0x11 = bits 1 and 5 = addresses 51 and 55), swStart/swTilt/swSlamTilt/swCoinDoor "
				"dedicated switches, every swXX/sXX #define, fh_handleMech (diverter, step gate, trap door, Rudy "
				"jaw/eyes causality), fhpa1GameData (GEN_WPCALPHA_1 prototype variant), and init_fh's driver-name "
				"dispatch between the two; src/wpc/wpc.c wpc_dispAlpha layout and GENWPC_HASFLIPTRON/GENWPC_HASDMD "
				"exclusion of GEN_WPCALPHA_1/GEN_WPCALPHA_2; src/wpc/core.h CORE_MAXSWCOL=16 (columns 0-9 matrix, "
				"10 coin door, 11 cabinet/flippers), CORE_FIRSTLFLIPSOL/CORE_FIRSTUFLIPSOL/CORE_FIRSTSIMSOL, "
				"core_updateSw's generic flipper input column 111-118, matrix copies 112->11 and 114->12, "
				"synthetic-flipper fallback, and core_getSol's complete 1-50 public dispatch; fh.c simulator "
				"states that consume sShooterRel (CORE_FIRSTSIMSOL=49); src/wpc/wpc.c's WPC_GILAMPS/J111/Game-On "
				"mapping, wpc_init public lamp count, and WPC_CFTBL chase-light integration; git history showing "
				"the prototype struct added with the copied flag in bc2649ff8fe25699c0c1a7fd21857913cec9c5af and "
				"production FunHouse corrected to zero in 1302113d46d00aff945f688d066cca022b8625b2 without updating fhpa1GameData; src/wpc/gen.h "
				"GEN_WPCALPHA_1/GEN_WPCALPHA_2 definitions."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-alpha.json",
			"revision": "repository",
			"locator": "WPC-Alpha public switch, DIP, solenoid, lamp, and five-GI address rules, reused unchanged for this first WPC-Alpha machine curated in the project",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "https://archive.org/details/arcademanual_Funhouse_OPS",
			"source_id": "arcademanual_Funhouse_OPS",
			"original_filename": "Funhouse_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-08-07T00:18:16Z",
			"locator": (
				"Locally retained 122-page derivative of the Williams FunHouse operations-manual scan from Internet Archive item "
				"arcademanual_Funhouse_OPS (details URL above; item uploader manuallibrary@textfiles.com; public date "
				"2017-09-20). Its byte identity is the local SHA-256 recorded here and must not be conflated with a "
				"current Archive.org derivative. It has a working but multi-column-scrambled text layer. Printed pages "
				"2-36 through 2-40 carry the lamp/switch/solenoid/G.I. location parts lists and their matrix and "
				"wiring tables; printed pages 2-24 and 2-32 carry the Jaw Drive/Eject Assembly and Unique Parts "
				"pages that fix Rudy's and the trap door's mechanism construction; Section 3 (printed 3-15 "
				"through 3-17) carries the Interboard Wiring switch/lamp/solenoid/G.I./flipper circuit tables."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.funhouse.switch-locations",
					"locator": "PDF page 99, printed 2-38, switch-locations parts list",
					"path": "evidence/excerpts/williams.funhouse.1990/switch-locations.md",
					"sha256": "998d63a2d06cc9b5afcf444ad652179af47e1b1af392fb26d22cd6dee789fcbb",
					"image": "evidence/excerpts/williams.funhouse.1990/switch-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["switch-locations.webp"],
					"image_derivation": "Funhouse_OPS.pdf page 99, crop box 0.06,0.06,0.9,0.93, scanned page rendered at its native resolution (embedded image xref 416, 2556px across 8.52in), rendered at 300 dpi, 2138x2857 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.switch-matrix",
					"locator": "PDF page 100, printed 2-39, FUNHOUSE Switch Matrix wiring table",
					"path": "evidence/excerpts/williams.funhouse.1990/switch-matrix.md",
					"sha256": "93d8858c53f0a3a961fe99b17ff7218707e6110cc2d4eef3dc495eabb738a610",
					"image": "evidence/excerpts/williams.funhouse.1990/switch-matrix.webp",
					"image_sha256": "d2221b041e00de17f4831c5fd1c9445e146024542ab5a9a3461d79611a84abc8",
					"image_derivation": "Funhouse_OPS.pdf page 100, crop box 0.08,0.04,0.68,0.46 of the page, rendered at 300 dpi with pdftoppm, reduced to 900px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.lamp-locations",
					"locator": "PDF page 97, printed 2-36, lamp-locations parts list",
					"path": "evidence/excerpts/williams.funhouse.1990/lamp-locations.md",
					"sha256": "6cb17cb8ed46b1c501b7d45625532e6cbb070e0d9a67b791bd4299909771a677",
					"image": "evidence/excerpts/williams.funhouse.1990/lamp-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-locations.webp"],
					"image_derivation": "Funhouse_OPS.pdf page 97, crop box 0.08,0.07,0.86,0.93, scanned page rendered at its native resolution (embedded image xref 406, 2550px across 8.50in), rendered at 300 dpi, 1985x2824 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.lamp-matrix",
					"locator": "PDF page 98, printed 2-37, lamp matrix wiring table",
					"path": "evidence/excerpts/williams.funhouse.1990/lamp-matrix.md",
					"sha256": "b70eee7219327b65aca8b5f8b251d849adc8c722f882568ea5cd4cf609e1cfe9",
					"image": "evidence/excerpts/williams.funhouse.1990/lamp-matrix.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-matrix.webp"],
					"image_derivation": "Funhouse_OPS.pdf page 98, crop box 0.055,0.48,0.965,0.915, scanned page rendered at its native resolution (embedded image xref 411, 2563px across 8.54in), rendered at 156 dpi, capped to 1200px wide, 1201x741 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page (address 12 confirmed at 600 dpi)",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.solenoid-locations",
					"locator": "PDF page 101, printed 2-40, solenoid and general-illumination locations parts list",
					"path": "evidence/excerpts/williams.funhouse.1990/solenoid-locations.md",
					"sha256": "c692640c182a3187131057414b4c71a1415ff9fb61042166cd491ac02718cb2b",
					"image": "evidence/excerpts/williams.funhouse.1990/solenoid-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["solenoid-locations.webp"],
					"image_derivation": "Funhouse_OPS.pdf page 101, crop box 0.06,0.06,0.58,0.65, scanned page rendered at its native resolution (embedded image xref 425, 2550px across 8.50in), rendered at 300 dpi, 1324x1938 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.switch-lamp-solenoid-circuits",
					"locator": "PDF page 119, printed 3-16, Switch/Lamp/Solenoid Circuits interboard wiring tables",
					"path": "evidence/excerpts/williams.funhouse.1990/switch-lamp-solenoid-circuits.md",
					"sha256": "b5b143551a0fd5255ee211d7cdc959a52cd776db56ffa708c9ceff95c7d45de4",
					"image": "evidence/excerpts/williams.funhouse.1990/switch-lamp-solenoid-circuits.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["switch-lamp-solenoid-circuits.webp"],
					"image_derivation": "Funhouse_OPS.pdf page 119, crop box 0.03,0.035,0.97,0.78, scanned page rendered at its native resolution (embedded image xref 512, 3297px across 10.99in), rendered at 253 dpi, capped to 2600px wide, 2601x1598 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.general-illumination-flipper-circuits",
					"locator": "PDF page 120, printed 3-17, General Illumination/Flipper/Power/Logic/Display Circuits interboard wiring tables",
					"path": "evidence/excerpts/williams.funhouse.1990/general-illumination-flipper-circuits.md",
					"sha256": "5b682f43d7552c7bef3779db37ec6bba0f44fd756675195c6bbd7219d93b7dce",
					"image": "evidence/excerpts/williams.funhouse.1990/general-illumination-flipper-circuits.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["general-illumination-flipper-circuits.webp"],
					"image_derivation": "Funhouse_OPS.pdf page 120, crop box 0.03,0.035,0.97,0.78, scanned page rendered at its native resolution (embedded image xref 517, 3287px across 10.96in), rendered at 253 dpi, capped to 2600px wide, 2601x1598 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.rudy-mechanism-parts",
					"locator": "PDF pages 85 and 93, printed 2-24 and 2-32, Jaw Drive/Eject Assembly and Unique Parts pages",
					"path": "evidence/excerpts/williams.funhouse.1990/rudy-mechanism-parts.md",
					"sha256": "45a06c3150ef08f2380452187cd7baec4f77ad8448e7e0990e0c6307ceb81966",
					"image": "evidence/excerpts/williams.funhouse.1990/rudy-mechanism-parts.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["rudy-mechanism-parts.webp"],
					"image_derivation": "Funhouse_OPS.pdf page 85, crop box 0.08,0.045,0.92,0.9, scanned page rendered at its native resolution (embedded image xref 354, 2588px across 8.63in), rendered at 300 dpi, 2138x2807 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/funhouse/manual-transcription.md",
			"revision": "2026-08-07",
			"acquired_at": "2026-08-07T00:00:00Z",
			"locator": (
				"Consolidated retained human transcription of every rendered manual table used by this "
				"definition, together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/williams.funhouse.1990/. Duplicates the in-repository "
				"evidence excerpts in one document for reviewer convenience."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": OPERATOR_HANDBOOK_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.funhouse.1990/maintainer-supplied-2026-08-14/Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf",
			"original_filename": "Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf",
			"sha256": OPERATOR_HANDBOOK_SHA256,
			"acquired_at": "2026-08-14T17:36:41Z",
			"locator": "Eleven-page November 1990 Williams operator handbook supplied by the maintainer. PDF pages 5-10 contain the solenoid/G.I., lamp, and switch tables and location drawings used to resolve the remaining FunHouse evidence questions.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; maintainer-supplied scan",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.funhouse.operator-handbook-lamps",
					"locator": "PDF pages 7-8, lamp matrix and lamp-location drawing",
					"path": "evidence/excerpts/williams.funhouse.1990/operator-handbook-lamp-evidence.md",
					"sha256": "9f5f69e9c1b0ba87228f32e0a5a0deb77283bc706b6bc1b709cfd1dc35fe5567",
					"image": "evidence/excerpts/williams.funhouse.1990/operator-handbook-lamp-evidence.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["operator-handbook-lamp-evidence.webp"],
					"image_derivation": "Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf page 8, crop box 0.13,0.24,0.58,0.56, scanned page rendered at its native resolution (embedded image xref 21, 3300px across 5.50in), rendered at 485 dpi, capped to 1200px wide, 1201x1319 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from rendered page images",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.operator-handbook-switch-gi",
					"locator": "PDF pages 5 and 9-10, G.I. table and switch matrix/location drawing",
					"path": "evidence/excerpts/williams.funhouse.1990/operator-handbook-switch-gi-evidence.md",
					"sha256": "e5eba5a25eea0b97fe419d43e62c5805a0b3c7dca0bb91085555bf9505b99d5d",
					"image": "evidence/excerpts/williams.funhouse.1990/operator-handbook-switch-gi-evidence.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["operator-handbook-switch-gi-evidence.webp"],
					"image_derivation": "Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf page 5, crop box 0.1,0.15,0.9,0.77, scanned page rendered at its native resolution (embedded image xref 12, 3300px across 5.50in), rendered at 136 dpi, capped to 600px wide, 600x720 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from rendered page images",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.operator-handbook-solenoid-locations",
					"locator": "PDF page 6, printed 5, Solenoid Locations drawing",
					"path": "evidence/excerpts/williams.funhouse.1990/operator-handbook-solenoid-locations.md",
					"sha256": "af6ea22289eeb30b963e82380439a8c77995ef7c00f9897d6e332b0ed9c37ac9",
					"image": "evidence/excerpts/williams.funhouse.1990/operator-handbook-solenoid-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["operator-handbook-solenoid-locations.webp"],
					"image_derivation": "Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf page 6, crop box 0.25,0.11,0.91,0.91, scanned page rendered at its native resolution (embedded image xref 15, 3300px across 5.50in), rendered at 600 dpi, grayscale, 2178x4080 WebP quality 80; rendered with tools/render_excerpt_image.py on PyMuPDF 1.26.3 and Pillow 12.3.0 (Python 3.12.9)",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page; every callout position also transcribed by an independent reader (tools/seeds/williams/funhouse-1990-callouts.json)",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.operator-handbook-lamp-locations",
					"locator": "PDF page 8, printed 7, Lamp Locations drawing",
					"path": "evidence/excerpts/williams.funhouse.1990/operator-handbook-lamp-locations.md",
					"sha256": "bb08ebe03378e6927dce7274d90289c5b5adaa428d5c656cf6656ddad03e8a0d",
					"image": "evidence/excerpts/williams.funhouse.1990/operator-handbook-lamp-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["operator-handbook-lamp-locations.webp"],
					"image_derivation": "Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf page 8, crop box 0.23,0.11,0.86,0.92, scanned page rendered at its native resolution (embedded image xref 21, 3300px across 5.50in), rendered at 600 dpi, grayscale, 2079x4131 WebP quality 80; rendered with tools/render_excerpt_image.py on PyMuPDF 1.26.3 and Pillow 12.3.0 (Python 3.12.9)",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page; every callout position also transcribed by an independent reader (tools/seeds/williams/funhouse-1990-callouts.json)",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.operator-handbook-switch-locations",
					"locator": "PDF page 10, printed 9, Switch Locations drawing",
					"path": "evidence/excerpts/williams.funhouse.1990/operator-handbook-switch-locations.md",
					"sha256": "63ea3194e70c3374aad9cd5586987facbd2c597d9d12b3dcc3e3967d83a25718",
					"image": "evidence/excerpts/williams.funhouse.1990/operator-handbook-switch-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["operator-handbook-switch-locations.webp"],
					"image_derivation": "Williams_1990_Funhouse_Operator_s_Handbook_November_1990_OCR_searchable.pdf page 10, crop box 0.15,0.09,0.89,0.92, scanned page rendered at its native resolution (embedded image xref 27, 3300px across 5.50in), rendered at 600 dpi, grayscale, 2442x4233 WebP quality 80; rendered with tools/render_excerpt_image.py on PyMuPDF 1.26.3 and Pillow 12.3.0 (Python 3.12.9)",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page; every callout position also transcribed by an independent reader (tools/seeds/williams/funhouse-1990-callouts.json)",
					"reviewed": True,
				},
			],
		},
		{
			"id": PLAYFIELD_PHOTO_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-manuals/by-machine/williams.funhouse.1990/maintainer-supplied-2026-08-14/funhouse-image-A13.jpg",
			"original_filename": "funhouse-image-A13.jpg",
			"sha256": PLAYFIELD_PHOTO_SHA256,
			"acquired_at": "2026-08-14T17:37:39Z",
			"locator": "Maintainer-supplied 500 by 375 lower-playfield photograph showing the Gangway 100,000 and 200,000 insert legends.",
			"license": "NOASSERTION",
			"attribution": "Maintainer-supplied photograph; photographer unknown",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.funhouse.playfield-photo-gangway",
					"locator": "Visible lower-playfield Gangway inserts",
					"path": "evidence/excerpts/williams.funhouse.1990/playfield-photo-gangway.md",
					"sha256": "788613103dfbec9958f3b05cb36592be94bca1e4ff8cc82d5598357c6a771ea0",
					"method": "manual",
					"transcribed_by": "curator, read from the supplied image",
					"reviewed": True,
				},
			],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/source/Funhouse%20%28Williams%201990%29_1.3.vpx",
			"original_filename": "Funhouse (Williams 1990)_1.3.vpx",
			"sha256": TABLE_SHA256,
			"acquired_at": "2026-08-07T15:17:32Z",
			"locator": (
				f"Retained known-working recreation of the physical machine, version 1.3. Exact playfield bounds "
				f"are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority only for "
				"named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPX table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": "322fba2dec939b50e0730da8caca177545aa8f8bc055ba136360ae55deb4e863",
			"known_working": True,
			"acquired_at": "2026-08-07T15:17:33Z",
			"locator": (
				'Retained embedded script (80,593 bytes). Runtime and mechanism-causality authority: '
				'Const cGameName = "fh_905h" (line 64; the commented-out line 63 reads "fh_905" and is not the '
				"active binding), the SolCallback table for solenoids 1-8, 14-28, the UpdateLamps per-address "
				"light bindings, the UpdateGI/UpdateGI2 G.I. region dispatch (Case 0/1/2/3/4), the trap door "
				"TrapMover_Timer state machine (Controller.Switch(76) set from PrTrap.RotX), and the "
				"SolCallback(sLRFlipper)/SolCallback(sLLFlipper) registration that consumes PinMAME's synthetic "
				"button-driven flipper states because fhGameData declares no FLIP_SOL; SolLFlipper drives both "
				"LeftFlipper and LeftFlipper1, independently corroborating the lower-left plus upper-left physical pair."
			),
			"license": "NOASSERTION",
			"attribution": "table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPXTABLE_SCRIPTS_SOURCE,
			"kind": "vpx_script",
			"uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Funhouse%20%28Williams%201990%29.vbs",
			"revision": "0c036bb61b4b4e8c778c37559f6795df8cd1521e",
			"original_filename": "Funhouse (Williams 1990).vbs",
			"sha256": "37cf4e41a6dc9772968cc8a1b13797e7ffb6f504d7e43cd15a6bb12926e9ae3d",
			"known_working": True,
			"acquired_at": "2026-08-14T00:00:00Z",
			"locator": "Pinned community script corpus at revision 0c036bb61b4b4e8c778c37559f6795df8cd1521e, lines 2444-2446: output 20 is assigned to the distinct F20 and F20a Light objects (plus render helper f20b).",
			"license": "NOASSERTION",
			"attribution": "VPX table-script authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool.manifest.json",
			"acquired_at": "2026-08-07T15:17:33Z",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds are "
				f"{TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": REVISION_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/v2-0c/source/Funhouse%20%28Williams%201990%29.vpx",
			"original_filename": "Funhouse (Williams 1990).vpx",
			"sha256": REVISION_TABLE_SHA256,
			"acquired_at": "2026-10-23T14:13:47Z",
			"locator": (
				"A later edit of the same community table, from the local table library: its table info gives version 2.0c "
				"where the retained 1.3 file gives 1.2d, and both keep release date 2/19/2017 and the Rev1.3 description. "
				f"Embedded script SHA-256 {REVISION_SCRIPT_SHA256}, with the same active cGameName fh_905h. "
				"Bounds left=0 top=0 right=964 bottom=2162, as in version 1.3. Used only for the G.I. bulbs it models: a pBulb "
				"glass, pFiliment filament and pFBase base primitive under each Light of GI_UpperBulbs, which its script "
				"assigns to public G.I. 2 (ModLampz.MassAssign(2)), and of GI_LowerBulbs, assigned to public G.I. 4. It shares "
				"its authors with version 1.3, so it confirms where they model a bulb, not the position independently. Its "
				"other geometry and its script are not used."
			),
			"license": "NOASSERTION",
			"attribution": "VPX table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": REVISION_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/v2-0c/extracted-vpxtool.manifest.json",
			"acquired_at": "2026-10-23T14:13:47Z",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"v2-0c/extracted-vpxtool; manifest SHA-256 {REVISION_MANIFEST_SHA256}; {REVISION_FILE_COUNT} files, "
				f"{REVISION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained version 2.0c table."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": RUNTIME_GI_SOURCE,
			"kind": "runtime_scenario",
			"uri": "internal:evidence/runtime/wpc-alpha/funhouse-fh_l9-gi-test.json",
			"revision": RUNTIME_GI_PINMAME_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of fh_l9 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-alpha/fh-gi-test.json) that steps T.6 GEN'L. ILLUM. through all illumination and "
				"then each circuit; every brightness step changes one public G.I. output alone while the ROM names it, and Start "
				"then Up show its wires, playfield and backbox pins, fuse and driver: public 0 BACKGLASS UPPER (WHT-BRN BRN, "
				"J120-7/120-1, J121-7/121-1, F110, Q18), 1 RUDY / BACKGLASS (WHT-ORN ORN, J120-8/120-2, J121-8/121-2, F109, Q10), "
				"2 REAR PLAYFIELD (WHT-YEL YEL, J120-9/120-3, J121-9/121-3, F108, Q14), 3 BACKGLASS CENTER (WHT-GRN GRN, "
				"J120-10/120-5, J121-10/121-5, F107, Q16), 4 FRONT PLAYFIELD (WHT-VIO VIO, J120-11/120-6, J121-11/121-6, F106, Q12)."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": PINSIDE_ORANGE_SOURCE,
			"kind": "human_review",
			"uri": "https://pinside.com/pinball/forum/topic/funhouse-gi-wiring-electrical-help-please",
			"acquired_at": "2026-10-23T00:00:00Z",
			"locator": (
				"Pinside topic \"Funhouse: GI wiring / electrical help please *SOLVED*\", posts #1-#9: an owner finds the spotlight "
				"that shines on Rudy and the lower third of the backbox G.I. dark on one orange/white-orange string entering J120 "
				"(pins 2 and 8), and replacing fuse F109 restores both."
			),
			"license": "NOASSERTION",
			"attribution": "Pinside contributors pezpunk and Schwaggs",
			"excerpts": [
				{
					"id": "excerpt.funhouse.pinside-gi-orange-string",
					"locator": "Posts #1, #6, #7 and #9",
					"path": "evidence/excerpts/williams.funhouse.1990/pinside-gi-orange-string.md",
					"sha256": "1fe17759c0938c8a87f1ceeb8dd7c63fe049d648e4de63b0f116a78b6f0205e6",
					"method": "manual",
					"transcribed_by": "curator, copied from the rendered forum page",
					"reviewed": True,
				},
			],
		},
		{
			"id": PINSIDE_VIOLET_SOURCE,
			"kind": "human_review",
			"uri": "https://pinside.com/pinball/forum/topic/funhouse-gi-problem",
			"acquired_at": "2026-10-23T00:00:00Z",
			"locator": (
				"Pinside topic \"Funhouse G.I. Problem (SOLVED)\", posts #1-#16: an owner's front-playfield G.I. and coin-door lamps "
				"go dark together on the white-violet string with fuse F106 (triac Q12, connectors J119 and J121) until a shorted "
				"lamp socket is found; a parts supplier notes G.I. bulbs under the apron."
			),
			"license": "NOASSERTION",
			"attribution": "Pinside contributors provato, ChrisHibler and Lermods",
			"excerpts": [
				{
					"id": "excerpt.funhouse.pinside-gi-violet-string",
					"locator": "Posts #1, #12, #13 and #16",
					"path": "evidence/excerpts/williams.funhouse.1990/pinside-gi-violet-string.md",
					"sha256": "b470b20dcbe92b15bba48a3304a0c18f84a24e79920b7fc3a0910b1ece1e7bc1",
					"method": "manual",
					"transcribed_by": "curator, copied from the rendered forum page",
					"reviewed": True,
				},
			],
		},
		{
			"id": CALLOUT_SOURCE,
			"kind": "human_review",
			"uri": f"internal:{CALLOUT_SEED_RELATIVE}",
			"sha256": hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest(),
			"locator": (
				"2026-10-23 factory location-drawing callout check of the November 1990 handbook's three drawings (printed 5 "
				"solenoids and flashlamps, 7 lamps, 9 switches) on the committed native-resolution excerpt crops: every callout "
				"transcribed by an independent reader working only from the page, per-page control fits from the three jet-bumper "
				"caps, the three flipper pivots and the outer frame's top corners, and the callout fit; a table placement whose own "
				"callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py), and the seed's "
				"measurements give the Steps switches and lamps read off the drawing. Reads, tiles, overlays and generators are "
				"retained under review-artifacts with a pinned manifest."
			),
			"license": "NOASSERTION",
			"attribution": "PinMAME game definitions contributors",
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
		"board": "WPC-Alpha CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_component}; row receiver {return_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-Alpha CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = address in UNUSED_MATRIX_ADDRESSES or label is None
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			part_number = SWITCH_PARTS.get(address)
			physical: dict[str, Any] = {}
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The switch-locations and switch-matrix pages both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				notes += (
					' Printed "(opto)" on both the switch-locations page (2-38) and the switch-matrix page '
					"(2-39) -- the only two switch-matrix positions on this machine identified as optical "
					"construction. Pinned PinMAME's fhGameData inverted-switch mask (column 5 = 0x11 = bits 1 "
					"and 5) normalizes both addresses, so the public switch state is already normalized and "
					"must not be inverted again. This is the only pair of optos in the entire FunHouse switch "
					"matrix; every other position is a plain leaf/microswitch/button/tilt construction with no "
					"opto marking on either printed page."
				)
			if address == 24:
				notes += " Physical part A-8630, the same part number printed for switch 22 (Front Door); a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 23:
				notes += ' Pinned fh.c declares a vestigial #define swTicket 23 never referenced elsewhere in the driver, matching the manual\'s "Not Used" fitment; treated as unfitted.'
			if address == 63:
				notes += " The November 1990 handbook places this at the rightmost trough position; the retained script's ballrelease kicker asserts this switch while occupied and clears it when solenoid 15 ejects the ball, so that kicker supplies the validated coordinate."
			if address == 73:
				notes += " Projected onto the retained table's Drain kicker object, which the outhole solenoid (1) also shares; no separate switch-only object exists."
			if address in STEPS_SWITCHES:
				notes += (
					" One of the three step switches on the Steps ramp (15 lowest, 26 middle, 36 top; the handbook's switch-locations "
					"drawing leads each number to its own wire slot across the Steps track). The coordinate is the centre of that slot "
					"measured on the drawing: the retained table's invisible star trigger for this switch sits on the track's right rail, "
					"0.06-0.07 normalized from the slot's centre and beyond the 0.07 limit from the leader's end, with the three triggers "
					"spread twice as far apart as the drawn slots."
				)
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Matrix Position {address}"
			elif kind == "constant":
				availability = "used"
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
			else:
				availability = "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				if address in {11, 12}:
					role = "flipper.lower.right.button" if address == 11 else "flipper.left.button"
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
					physical["location"] = "cabinet flipper-button input"
					physical["notes"] += (
						" This CPU-facing matrix state is copied from PinMAME's generic cabinet flipper input "
						f"{112 if address == 11 else 114}; it is not an EOS contact or a playfield-positioned sensor."
					)
				elif address in {13, 14, 21, 22}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet"
					if address == 22:
						extra["initial_active"] = True
				elif address in STEPS_SWITCHES:
					extra["spatial"] = measured(identifier, "sensor")
				else:
					spatial_refs = (OPERATOR_HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE) if address == 63 else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *spatial_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	for address in range(111, 119):
		used = address in {112, 114}
		right = address == 112
		label = (
			"Generic Right Flipper Button State" if right else
			"Generic Left Flipper Button State" if address == 114 else
			f"Unused Generic Flipper Input {address}"
		)
		notes = (
			"Live generic cabinet-flipper input published from PinMAME's switch column 11. "
			+ (
				"core_updateSw copies this state to matrix switch 11; it represents the right cabinet button and the physical lower-right flipper assembly."
				if right else
				"core_updateSw copies this state to matrix switch 12; the one left cabinet button directly drives both the lower-left and upper-left physical flipper assemblies."
			)
			if used else
			"Public generic-flipper-column position. FunHouse declares no input at this position, so it is explicitly unused."
		)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"physical": {
				"location": "cabinet flipper button" if used else "internal public address space",
				"switch_type": "button" if used else "other",
				"notes": notes,
			},
			"normally_closed": False,
			"spatial": not_applicable("cabinet_or_service" if used else "unused", CORE_SOURCE, CONTROLLER_SOURCE),
		}
		if used:
			extra["roles"] = ["flipper.lower.right.button" if right else "flipper.left.button"]
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used" if used else "unused",
				(CORE_SOURCE, CONTROLLER_SOURCE),
				**extra,
			)
		)

	dip_labels = {n: f"CPU DIP {n} (country/option configuration bit)" for n in range(1, 9)}
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}",
				dip_labels[address],
				"dip_switch",
				"pinmame.input.dip",
				address,
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.dip", "value": str(address)},
					{"namespace": "manual.address", "value": f"SW{address}"},
				],
				physical={
					"location": "WPC-Alpha CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC-Alpha CPU-board country/option configuration DIP bank. The retained transcription of "
						"this manual does not include a per-country switch-combination chart, so no specific "
						"ON/OFF combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{label.lower().replace(chr(39), '').replace('/', '-').replace(',', '').replace('.', '').replace(' ', '-')}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 29):
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		is_flasher = address in FLASHER_QUANTITIES
		kind = "flasher" if is_flasher else "motor" if address in {21, 22} else "coil"
		physical: dict[str, Any] = {}
		part_number = SOLENOID_PARTS.get(address)
		if part_number and not is_flasher:
			physical["part_number"] = part_number
		notes = f"Printed solenoid table entry {address:02d}."
		if is_flasher:
			quantity = FLASHER_QUANTITIES[address]
			physical["quantity"] = quantity
			notes += f" Printed flashlamp complement: {quantity} {part_number} bulb(s) on this circuit."
			if address in {17, 23, 24}:
				notes += (
					" The three bulbs are a dome on the back panel at the top right (the table's Flupper dome primitive, placed at its "
					"world-space mesh bounds centre), a diamond insert "
					"beside the Steps (the table's Light under it) and a dome on the right side wall (the table's Light at it); the "
					"handbook's solenoid-locations drawing prints the number on both playfield sockets and once more in the row of "
					"leader-less back-panel labels along the top rail."
				)
			elif address == 19:
				notes += (
					" Both bulbs light the clock from under its centre, where the handbook's solenoid-locations drawing prints 19 once "
					"and the retained table models one Light fixture, so they share one placement."
				)
			elif address == 20:
				notes += " The retained table supplies distinct F20 and F20a Light objects, and the pinned community script assigns both to output 20; each printed Superdog socket therefore has its own placement."
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
		if address == 7:
			notes += " Cabinet-mounted knocker; no playfield location."
		if address in {21, 22}:
			notes += (
				" Rudy's jaw is driven by a continuously-running DC gearmotor (A-13997, Jaw Drive Assembly) "
				"through a worm gear/sector pair, not a coil stroke; solenoid 22 (Up/Down Driver) is the "
				"motor's direction relay. Pinned fh_handleMech opens the jaw when both 21 and 22 are energized "
				"together and closes it when 21 alone is energized. Projected onto switch 51 (Dummy Jaw), the "
				"only fixed point recorded for Rudy's Head Assembly, since no dedicated jaw-motor VPX object "
				"was identified separately from the head figure itself."
			)
		if address in {25, 26, 27, 28}:
			notes += (
				" One of four independent drive lines on Rudy's Head Assembly: 25/28 select eye left/right "
				"position, 26/27 latch the eyelids open/closed. Pinned fh_handleMech treats eyelid open/close "
				"as a persistent latch and eye left/right as a momentary position read each mechanics tick. "
				"Projected onto Rudy's eyelid assembly, the centre of the PrLids primitive's world-space mesh bounds, which spans "
				"both eyes; the eye and eyelid drives sit inside the head behind the face, where the handbook's solenoid-locations "
				"drawing prints 25-28 inside Rudy's head outline."
			)
		if address == 8:
			notes += (
				" Placed on the lock-release gate the retained script's MBRelease handler swings (Lock_Release_Prim, together "
				"with the hidden Flipper1 gate and the WaSw28 lock wall it drops); the handbook's solenoid-locations drawing prints "
				"8 on the release box there, beside the lock switches 25, 27 and 28."
			)
		if address in {5, 6}:
			notes += " Trap door open/close drive; trap-door-closed switch 76 is set programmatically from the trap door's own rotation angle rather than read from a separate switch object (see mechanism.trap-door)."
		physical["notes"] = notes

		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.solenoid", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address:02d}"},
			],
			"physical": physical,
		}
		if address in SOLENOID_WIRING:
			wiring_data = SOLENOID_WIRING[address]
			extra["wiring"] = {
				"board": "WPC-Alpha power driver board",
				"control_connection": wiring_data["control_connection"],
				"driver_transistor": wiring_data["driver_transistor"],
			}
		role = "emitter" if is_flasher else "effect" if kind == "motor" else "effect"
		if address == 7:
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			spatial_refs = (VPX_TABLE_SOURCE, VPXTABLE_SCRIPTS_SOURCE) if address == 20 else (VPX_TABLE_SOURCE,)
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], *spatial_refs)
		refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) if address in SOLENOID_CALLBACKS else (MANUAL_SOURCE, CORE_SOURCE)
		if address == 20:
			refs += (VPXTABLE_SCRIPTS_SOURCE,)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
	public_state_outputs = {
		29: ("device.wpc-j111-state-29", "WPC J111 State 29", "virtual", "used", ["internal.wpc-state"], "PinMAME mirrors WPC_GILAMPS bit 5, one of the CPU board's J111 GPIO state bits, to public address 29. It is a live controller state channel rather than a separate physical playfield device."),
		30: ("device.wpc-j111-state-30", "WPC J111 State 30", "virtual", "used", ["internal.wpc-state"], "PinMAME mirrors WPC_GILAMPS bit 6, one of the CPU board's J111 GPIO state bits, to public address 30. It is a live controller state channel rather than a separate physical playfield device."),
		31: ("device.game-on-solenoid-relay", "Game-On Solenoid Relay", "relay", "used", ["internal.wpc-state", "cabinet.game-on-relay"], "The real pre-Fliptronic Game-On relay controlled by WPC_GILAMPS bit 7. Pinned wpc.c documents the chain from CPU board U4/J121 through power-driver J113, the relay, J110, the cabinet switch, and J109 to the flippers. This cabinet/flipper-enable relay is not a playfield coil."),
		32: ("device.unused-wpc-state-output-32", "Unused WPC State Output 32", "virtual", "unused", ["internal.unused.wpc-output"], "PinMAME's WPC state remap has no fourth bit at public address 32, so this position is constant zero."),
	}
	for address in range(33, 45):
		public_state_outputs[address] = (
			f"device.unused-wpc-output-{address}",
			f"Unused WPC Output {address}",
			"virtual",
			"unused",
			["internal.unused-platform-slot"],
			("Generic upper-flipper-shaped public position; FunHouse declares no CPU-controlled FLIP_SOL bits, so PinMAME never drives it even though the physical machine has a direct-wired upper-left flipper." if address <= 36 else "Platform public-output position not served by this WPC-Alpha generation; PinMAME returns zero."),
		)
	public_state_outputs.update({
		45: ("device.synthetic-lower-right-flipper-power", "Synthetic Lower Right Flipper Power", "virtual", "used", ["internal.synthetic-flipper"], "PinMAME's synthetic lower-right power bit. Because FunHouse has no CPU-controlled flipper solenoids, core_updateSw fabricates addresses 45-48 from the live flipper-button states while the real Game-On relay is enabled. The physical coil remains direct-wired through the flipper driver board."),
		46: ("device.synthetic-lower-right-flipper", "Synthetic Lower Right Flipper", "virtual", "used", ["internal.synthetic-flipper", "flipper.lower.right"], "PinMAME's combined lower-right public flipper state. It mirrors the same fabricated button-driven state as address 45 and is the sLRFlipper callback consumed by the retained script; it does not represent an additional physical coil."),
		47: ("device.synthetic-left-flipper-power", "Synthetic Left Flipper Power", "virtual", "used", ["internal.synthetic-flipper"], "PinMAME's synthetic left-side power bit. It is fabricated from the live left-flipper button state under the same conditions as address 45 and has no physical driver-board output of its own; the one state covers both direct-wired left bats."),
		48: ("device.synthetic-left-flipper", "Synthetic Left Flipper", "virtual", "used", ["internal.synthetic-flipper", "flipper.lower.left", "flipper.upper.left"], "PinMAME's combined left-side public flipper state. It mirrors the same fabricated button-driven state as address 47 and is the sLLFlipper callback consumed by the retained script; that callback rotates both LeftFlipper and LeftFlipper1, matching the physical lower-left and upper-left bats. It does not represent an additional physical coil."),
		49: ("device.pinmame-simulator-ball-shooter", "PinMAME Simulator Ball-Shooter Channel", "virtual", "used", ["internal.simulator-ball-shooter"], "Platform simulator-only fake ball-shooter solenoid (sShooterRel). The built-in FunHouse simulator consumes it in both left- and right-shooter state transitions; it remains virtual and has no physical FunHouse driver-board circuit."),
		50: ("device.unassigned-solenoid-slot-50", "Unassigned Solenoid Slot 50", "virtual", "unused", ["internal.unused-platform-slot"], "Reserved platform gap before custom outputs. FunHouse declares no custom solenoids, so no address above 50 is published for this game."),
	})
	for address in range(29, 51):
		identifier, label, kind, availability, roles, notes = public_state_outputs[address]
		reason = "cabinet_or_service" if address == 31 else "virtual"
		items.append(
			_device(
				identifier,
				label,
				kind,
				"pinmame.output.solenoid",
				address,
				availability,
				(CORE_SOURCE, CONTROLLER_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=roles,
				physical={"notes": notes},
				spatial=not_applicable(reason, CORE_SOURCE, CONTROLLER_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS.get(address)
			unused = label is None
			identifier = f"lamp.matrix-{address}"
			bulb = LAMP_BULBS.get(address)
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += f' The lamp-matrix page marks this insert "(x {LAMP_QUANTITIES[address]})" and the retained table binds that many distinct, non-co-located bulb positions.'
			if address == 12:
				notes += (
					' The older lamp-locations page (2-36) reads "Gangway 10,000", but its matrix page, the '
					"November 1990 handbook, and the maintainer-supplied physical playfield photograph all identify "
					"the insert as Gangway 100,000. The isolated 10,000 entry is a resolved one-digit typo."
				)
			if address == 51:
				notes += ' The lamp-matrix page additionally prints "(Left)" on this cell; the lamp-locations page has no such qualifier, and there are only three jet bumpers on this machine (Left/Right/Lower per the solenoid table), so this is read as a positional descriptor rather than a naming conflict.'
			if address == 88:
				notes += " Cabinet Start-button backlight, explicitly annotated \"(cabinet)\" on the lamp-locations page."
			if address in {57, 58}:
				sprite, bulb = ("F57_FS", "BulbFil2 filament in its BulbTop2 glass") if address == 57 else ("F58_FS", "BulbFil1 filament in its BulbTop1 glass")
				notes += (
					f" The script flashes {sprite} and its partner and desktop copies, wf_on_blur glow sprites; the bulb is the "
					f"overhead {bulb}, 12 units from them, placed at its centre."
				)
			if address in {71, 74, 75, 76, 77, 78}:
				notes += (
					f" One of the Magic Mirror's column of six lamps. The bulb is the L{address} lamp-glass primitive, placed at the "
					"centre of its world-space mesh bounds (its stored position lies 0.0024 normalized behind that)"
					+ ("; F71 and F71a, which the script also flashes, are f_refl glow sprites." if address == 71 else ".")
				)
			if address in {54, 55, 56}:
				notes += (
					" One of the three Steps lamps (54 bottom, 55 middle, 56 top). The handbook's lamp-locations drawing prints each "
					"number on the Steps track's left rail beside its own small round socket; the coordinate is the centre of that "
					"socket measured on the drawing. The retained table lights the Steps award from `_finger_1` hotspots raised about "
					"200 units on a sign 0.05-0.08 normalized rear of and beside the drawn sockets (`_finger_2` to `_finger_4` are "
					"render layers), so the three bulbs of the assembly are all measured rather than splitting it between the two sources."
				)
			physical["notes"] = notes

			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"physical": physical,
				"wiring": {
					"board": "WPC-Alpha power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Lamp Position {address}"
			elif address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in {54, 55, 56}:
				availability = "used"
				extra["spatial"] = measured(identifier, "emitter")
			else:
				availability = "used"
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(
				_device(
					identifier,
					label,
					"lamp",
					"pinmame.output.lamp",
					address,
					availability,
					(MANUAL_SOURCE, OPERATOR_HANDBOOK_SOURCE, PLAYFIELD_PHOTO_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE) if address == 12 else (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
					**extra,
				)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, label in GI_LABELS.items():
		identifier = f"gi.string-{address}"
		wiring_data = GI_FEED_WIRING[address]
		name, wires, playfield_pins, backbox_pins, fuse, driver = GI_ROM_SCREENS[address]
		list_row, handbook_row = GI_PRINTED_ROWS[address]
		notes = (
			f"General-illumination string {address + 1}. The L-9 ROM's T.6 G.I. test changes public G.I. {address} alone while it "
			f"shows {name}, and on Start prints {wires} / {playfield_pins} / {backbox_pins} / {fuse} / {driver}. The printed row of "
			f"the same number reads {list_row} and {handbook_row}. {GI_PRINTED_NOTE} The retained script's runtime region is "
			f"{GI_SCRIPT_REGIONS[address]}. Insert-panel connector: {wiring_data['insert_connection']}."
		)
		refs = (MANUAL_SOURCE, OPERATOR_HANDBOOK_SOURCE, RUNTIME_GI_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
		"wiring": {
				"board": "WPC-Alpha power driver board",
				"control_wire": wiring_data["control_wire"],
				"control_connection": wiring_data["control_connection"],
				"driver_transistor": wiring_data["driver_transistor"],
				"return_wire": wiring_data["return_wire"],
				"return_connection": wiring_data["return_connection"],
				"return_component": wiring_data["return_component"],
			},
		}
		physical: dict[str, Any] = {}
		gi_spatial_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_GI_SOURCE)
		if address == 0:
			notes += " A backbox string: it lights the upper part of the backglass insert panel and has no playfield socket."
			extra["roles"] = ["cabinet.backglass"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, OPERATOR_HANDBOOK_SOURCE, RUNTIME_GI_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 1:
			notes += (
				" It feeds the spotlight that lights Rudy's face and the lower part of the backbox insert panel: an owner traced "
				"both to the orange/white-orange pair on J120-2/J120-8 and fuse F109 (Pinside). The playfield socket is that "
				"spotlight, the retained table's RudyShade Light under its pShade1/pShade2 lamp-shade primitives at the front "
				"right of Rudy. RudySign1 and RudySign2, which the script's Case 1 also drives, are f_refl glow sprites the "
				"table paints on Rudy and make no socket. The backbox branch is not placed, and no source gives a bulb count, "
				"so no quantity is asserted."
			)
			refs += (PINSIDE_ORANGE_SOURCE,)
			extra["spatial"] = located(identifier, "emitter", GI_RUDY_POSITIONS, *gi_spatial_refs, PINSIDE_ORANGE_SOURCE)
		elif address == 2:
			notes += (
				" The script's Case 2 drives the GI_Upper collection, 19 render Lights of which only three sit on a bulb the "
				"retained table draws (BulbFil filament primitives). Version 2.0c of the same table models a bulb, with glass, "
				"filament and base primitives, under each of the 14 Lights its script drives from this string through "
				"GI_UpperBulbs, and each placement is the 1.3 Light within 0.002 normalized of one of them: 14 sockets, one per "
				"bulb, collapsing render doubles to the one on a BulbFil primitive. Light22, 0.026 normalized from the Light23 "
				"socket, has no 2.0c bulb and makes no socket. Both tables split this string from public 4 as the ROM's REAR and "
				"FRONT PLAYFIELD names do. No source gives a bulb count, so no quantity is asserted."
			)
			refs += (REVISION_TABLE_SOURCE,)
			extra["spatial"] = located(identifier, "emitter", GI_UPPER_POSITIONS, *gi_spatial_refs, REVISION_TABLE_SOURCE)
		elif address == 3:
			notes += (
				" A backbox string. The ROM names it BACKGLASS CENTER, the retained script drives nothing on the playfield from it, "
				"and the backbox's upper and lower parts are on public 0 and public 1; the printed \"Top Playfield\" name on its "
				"white-green row is the misplaced name described above, not a playfield branch."
			)
			extra["roles"] = ["cabinet.backglass"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, OPERATOR_HANDBOOK_SOURCE, RUNTIME_GI_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 4:
			notes += (
				" It feeds the front playfield and the coin-door lamps through the J119 cabinet branch: an owner traced both to the "
				"violet/white-violet pair, fuse F106 and triac Q12 (Pinside). The script's Case 4 drives the GI_Lower collection, "
				"45 Lights at 11 sockets once co-located render doubles are collapsed: seven sit on BulbFil filament primitives "
				"and four show their own bulb mesh, and version 2.0c of the same table models a bulb at each of the 11 under the "
				"Lights it drives from this string through GI_LowerBulbs. The parts supplier in the same thread names G.I. bulbs "
				"under the apron, which neither table models: the two Bottom_GI render lights below the flippers sit on no bulb, so "
				"they are not placed, and since no source gives the apron bulbs' number or positions this string's placements are "
				"incomplete and the record stays partial. LowerGI_B14, the halo partner of LowerGI_B4 at Light33's socket and 0.014 normalized from it, "
				"sits on no bulb either. The coin-door lamps are not placed, and no source gives a bulb count, so no quantity is "
				"asserted."
			)
			refs += (REVISION_TABLE_SOURCE, PINSIDE_VIOLET_SOURCE)
			extra["spatial"] = located(identifier, "emitter", GI_LOWER_POSITIONS, *gi_spatial_refs, REVISION_TABLE_SOURCE, PINSIDE_VIOLET_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "gi", "pinmame.output.gi", address, "used", refs, **extra))
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.player-1-alphanumeric",
			"label": "Player 1/3 sixteen-character alphanumeric display",
			"kind": "segment",
			"controller_index": 0,
			"segment_start": 0,
			"width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "display.player-2-alphanumeric",
			"label": "Player 2/4 sixteen-character alphanumeric display",
			"kind": "segment",
			"controller_index": 1,
			"segment_start": 20,
			"width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		},
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(
		identifier: str,
		label: str,
		kind: str,
		actuators: list[str],
		sensors: list[str],
		behavior: str,
		positions: list[tuple[str, str, list[str], str]],
		*refs: str,
	) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}
		if positions:
			record["positions"] = [
				{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
				for position_id, position_label, position_sensors, description in positions
			]
		return record

	return [
		mechanism(
			"mechanism.rudy-jaw",
			"Rudy's motorized jaw",
			"motorized",
			[output_id("Mouth Motor"), output_id("Up/Down Driver")],
			["switch.matrix-51"],
			"A DC gearmotor (A-13997 Jaw Motor Assembly) drives Rudy's jaw open and closed through a worm "
			"gear/sector pair (Jaw Drive Assembly A-13752), not a coil stroke. Pinned fh_handleMech: if the "
			"jaw is open and solenoid 21 (Mouth Motor) is energized while solenoid 22 (Up/Down Driver) is "
			"not, the jaw closes; if the jaw is closed and both 21 and 22 are energized together, the jaw "
			"opens. Dummy Jaw opto 51 senses a ball landing in Rudy's open mouth (printed opto, normalized "
			"by PinMAME's inverted-switch mask).",
			[("open", "Jaw open", ["switch.matrix-51"], "Ball can land in Rudy's mouth.")],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.rudy-eyes",
			"Rudy's eyes",
			"motorized",
			[output_id("Eyes Right"), output_id("Eyelids Open"), output_id("Eyelids Close"), output_id("Eyes Left")],
			[],
			"Four independent drive lines on Rudy's Head Assembly. Eyelids open (solenoid 26) and close "
			"(solenoid 27) latch a persistent open/closed state; eyes right (25) and eyes left (28) are read "
			"as momentary position signals each mechanics tick, with neither held meaning the eyes rest "
			"straight ahead. Pinned fh_handleMech tracks both the open/closed latch and the left/right/"
			"straight position independently. There is no dedicated switch for eye position or eyelid state; "
			"it is purely a scored callback effect with no sensor feedback to the controller.",
			[],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.trap-door",
			"Trap door",
			"gate",
			[output_id("Trap Door Open"), output_id("Trap Door Closed")],
			["switch.matrix-76", "switch.matrix-75"],
			"Solenoid 5 opens and solenoid 6 closes a trap door in the upper-right loop path. Pinned "
			"fh_handleMech and the retained script's TrapMover_Timer both derive Trap Door Closed switch 76 "
			"directly from the door's own rotation angle rather than reading a separate contact switch -- the "
			"retained script sets Controller.Switch(76)=1 once the door primitive's RotX falls to 90 degrees "
			"(closed) and clears it back to 0 once the door opens past 90 degrees. Upper Right Loop switch 75 "
			"senses a ball taking the loop shot when the door is closed, and the printed manual documents a "
			"scoring loop feature (Trap Door Bonus lamp 63, Trap Door Frenzy lamp 83) tied to whether the "
			"door is open when a ball reaches it.",
			[
				("closed", "Trap door closed", ["switch.matrix-76"], "Door primitive RotX at or below 90 degrees; projected onto the door's own mechanism (no separate contact switch object)."),
				("loop", "Upper right loop shot", ["switch.matrix-75"], "Ball takes the loop path past the trap door."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.step-gate",
			"Left outlane step gate",
			"gate",
			[output_id("Steps Gate")],
			[],
			"Solenoid 14 (printed \"Steps Gate\"; the retained script's own comment calls it the \"Steps "
			"shooter lane diverter\") opens a gate that reroutes a ball in the left outlane back to the left "
			"ballshooter lane (switch 47) instead of draining, functioning as a kickback-style save feature "
			"gated by whatever awards the STEP letters. Pinned fh_handleMech holds the gate open for a fixed "
			"50-tick timer after the solenoid fires, then auto-closes it; there is no separate open/closed "
			"sensor switch for the gate itself.",
			[],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.ramp-diverter",
			"Upper ramp/Steps track diverter",
			"diverter",
			[output_id("Ramp Diverter")],
			["switch.matrix-16", "switch.matrix-35", "switch.matrix-38"],
			"Solenoid 2 diverts a ball on the upper ramp between the Steps track (S-T-E-P letters, switches "
			"17/31/54/64/86/73) and the main upper-ramp path (Upper Ramp Switch 16, Steps Track Lower/Upper "
			"35/38, Ramp Exit Track 48, Ramp Entrance 56). Pinned fh_handleMech asserts the diverter open for "
			"a fixed 25-tick window after the solenoid fires (matching the printed \"Ramp Diverter\" high-"
			"power coil, AE-26-1200) and auto-closes it afterward; there is no separate diverter-position "
			"sensor switch.",
			[],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.trough-and-shooters",
			"Ball trough, outhole, and dual shooter lanes",
			"kicker",
			[output_id("Outhole"), output_id("Trough")],
			["switch.matrix-73", "switch.matrix-72", "switch.matrix-74", "switch.matrix-63", "switch.matrix-47", "switch.matrix-62"],
			"FunHouse has two manual shooter lanes (left, switch 47; right, switch 62) feeding a shared trough. "
			"Solenoid 1 (Outhole) kicks a drained ball into the trough; solenoid 15 (Trough, retained script "
			"comment \"Main trough kickout\") ejects a trough ball back to a shooter lane. Trough positions are "
			"Left Trough (72), Center Trough (74), and Right Trough (63). The handbook places 63 at the "
			"rightmost trough position, and the retained script asserts it on the ballrelease kicker until "
			"solenoid 15 ejects that ball into a shooter lane.",
			[
				("outhole", "Ball in outhole", ["switch.matrix-73"], "Drain sensor before the trough kickout."),
				("right-trough", "Ball at right trough / release", ["switch.matrix-63"], "Rightmost trough sensor on the ballrelease kicker."),
				("left-shooter", "Left shooter lane", ["switch.matrix-47"], "Manual left plunger lane."),
				("right-shooter", "Right shooter lane", ["switch.matrix-62"], "Manual right plunger lane."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.tunnel-kickout",
			"Tunnel kickout hole",
			"kicker",
			[output_id("Tunnel Kickbig")],
			["switch.matrix-58"],
			"A ball resting on opto-free microswitch 58 (Tunnel Kickout) is kicked back to the playfield by "
			"solenoid 4 (printed \"Tunnel Kickbig\"). The retained script's SolKickout handler fires two "
			"physical kicker objects in sequence (a primary kick followed by a delayed second-chute kick), "
			"consistent with the tunnel's own captive ball-return geometry rather than a single simple "
			"saucer.",
			[("held", "Ball in the tunnel kickout", ["switch.matrix-58"], "Tunnel kickout switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.rudys-hideout",
			"Rudy's Hideout kickback",
			"kicker",
			[output_id("Kickbig")],
			["switch.matrix-46"],
			"A ball landing behind Rudy's head (Rudy Hideout Kickbig switch 46, a skill-shot landing spot per "
			"the printed player rules) is returned to play by solenoid 3.",
			[("held", "Ball in Rudy's Hideout", ["switch.matrix-46"], "Rudy Hideout Kickbig switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.dummy-eject-hole",
			"Dummy eject hole",
			"kicker",
			[output_id("Dummy Eject Hole")],
			["switch.matrix-65"],
			"A separate saucer near Rudy's head (Dummy Eject Hole switch 65) is kicked back to play by "
			"solenoid 16 (retained script comment \"Rudy's mouth kickout\", though it is a distinct switch "
			"and coil from the jaw mechanism proper).",
			[("held", "Ball in the dummy eject hole", ["switch.matrix-65"], "Dummy eject hole switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.multiball-lock",
			"Three-ball lock and multi-ball release",
			"kicker",
			[output_id("Multi-ball Release")],
			["switch.matrix-25", "switch.matrix-27", "switch.matrix-28"],
			"Three lock switches (Lock Mech Right 25, Lock Mech Center 27, Lock Mech Left 28) share one "
			"printed 3-Switch Assembly (A-14138). The retained script's MBRelease handler fires solenoid 8, "
			"drops the WaSw28 lock wall, and rotates a release object to feed all locked balls to the "
			"trough together for multi-ball.",
			[
				("right", "Right lock position", ["switch.matrix-25"], "Rightmost of the three lock positions."),
				("center", "Center lock position", ["switch.matrix-27"], "Middle lock position."),
				("left", "Left lock position", ["switch.matrix-28"], "Leftmost lock position, released by MBRelease."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Lower Jet Bumper")],
			["switch.matrix-18", "switch.matrix-77", "switch.matrix-68"],
			"Three jet bumpers. The retained script's Bumper1_Hit, Bumper2_Hit, and Bumper3_Hit handlers "
			"pulse switches 18, 77, and 68 and fire coils 9, 10, and 11 respectively, matching printed Left/"
			"Right/Lower Jet Bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-18"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-77"], "Right bumper of the nest."),
				("lower", "Lower jet bumper", ["switch.matrix-68"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-41", "switch.matrix-53"],
			"Each slingshot (printed \"Kicker\" on the solenoid table, \"(sling) Kicker\"/\"Slingshot "
			"(Kicker)\" on the switch tables) fires its own coil on the same event. The retained script's "
			"LeftSlingShot_Slingshot and RightSlingShot_Slingshot handlers pulse matrix addresses 41 and 53 "
			"and fire coils 12/13 together.",
			[
				("left", "Left slingshot", ["switch.matrix-41"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-53"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.flippers",
			"Three direct-wired flippers with two synthetic PinMAME states",
			"other",
			["device.synthetic-lower-right-flipper", "device.synthetic-left-flipper"],
			["switch.generic-112", "switch.generic-114", "switch.matrix-11", "switch.matrix-12"],
			"FunHouse is a pre-Fliptronics WPC-Alpha machine: fhGameData declares FLIP_SWNO(12,11) (flipper "
			"switches only) with no FLIP_SOL() call, so no public address represents a CPU-controlled physical "
			"flipper driver. PinMAME nevertheless fabricates public states 45-48 from the live button inputs "
			"while the Game-On relay is enabled; retained callbacks sLRFlipper (46) and sLLFlipper (48) use "
			"those synthetic states to animate the digital flippers. SolLFlipper rotates both LeftFlipper and "
			"LeftFlipper1. The handbook's coil inventory and the printed Flipper Circuits wiring page confirm "
			"three fitted physical assemblies: lower right FL-11630, lower left FL-11630, and upper left FL-11753; "
			"the upper-right board position is unfitted. They are wired through a dedicated flipper driver board (J109/J110) directly to "
			"the flipper buttons and end-of-stroke switches, entirely separate from the CPU-addressable "
			"solenoid matrix (1-50). Generic public inputs 112 and 114 represent the cabinet buttons; core_updateSw "
			"copies them to ordinary matrix inputs 11 and 12 for the ROM. Neither 11 nor 12 is a playfield EOS "
			"contact. The one left button and synthetic left state drive both fitted left bats, and states 45-48 "
			"must not be recreated as four additional coils.",
			[
				("lower-right", "Lower-right flipper", ["switch.generic-112", "switch.matrix-11"], "Direct-wired FL-11630 assembly; animate from synthetic public state 46."),
				("lower-left", "Lower-left flipper", ["switch.generic-114", "switch.matrix-12"], "Direct-wired FL-11630 assembly; animate from synthetic public state 48."),
				("upper-left", "Upper-left flipper", ["switch.generic-114", "switch.matrix-12"], "Direct-wired FL-11753 assembly; the same left callback/state animates this bat together with the lower-left bat."),
			],
			CORE_SOURCE, MANUAL_SOURCE, OPERATOR_HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	return []


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


def build_with_decisions() -> tuple[dict[str, Any], dict[str, Any]]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": "williams.funhouse.1990",
			"name": "FunHouse",
			"manufacturer": "Williams",
			"year": 1990,
			"kind": "physical_pinball",
			"ipdb_id": 966,
			"opdb_id": "G5Dz7-Mq139",
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
				"spatial_placement": "unknown",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-alpha",
			"hardware_generation": "0x2",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/funhouse-1990.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"FunHouse device identifiers are not unique: {duplicates}")
	return definition, check_against_drawings(definition, load_json(CALLOUT_SEED_PATH))


def build() -> dict[str, Any]:
	return build_with_decisions()[0]


def check_against_drawings(definition: dict[str, Any], seed: dict[str, Any]) -> dict[str, Any]:
	"""Check every placement the factory drawings mark and refuse any that disagrees.

	A checked placement whose callout agrees also cites the callout seed. A placement whose label the drawing prints only
	at a nearer placement of the same device (a second bulb under one drawn insert) keeps its table status, as does every
	placement the seed does not check.
	"""
	decisions = drawing_callouts.apply_to_definition(definition, seed, CALLOUT_SOURCE)
	failed = sorted(pid for pid, decision in decisions["placements"].items() if not decision["agrees"] and decision["read"] is not None)
	if failed:
		raise RuntimeError(f"FunHouse placements disagree with their factory-drawing callouts: {failed}")
	agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			for placement in (device.get("spatial") or {}).get("placements") or []:
				refs = placement["provenance"]["source_refs"]
				if placement["id"] in agreeing and CALLOUT_SOURCE not in refs:
					refs.append(CALLOUT_SOURCE)
	not_validated = sorted(
		device["id"] for device in definition["inputs"] + definition["outputs"]
		if (device.get("spatial") or {}).get("status") not in {"validated", "not_applicable"}
	)
	if not_validated:
		raise RuntimeError(f"FunHouse devices without validated or not-applicable spatial records: {not_validated}")
	return decisions


PROJECTIONS = [
	{"group": "pinmame.input.switch", "address": 73, "reason": "Projected onto the retained table's Drain kicker object, shared with the outhole solenoid (1)."},
	{"group": "pinmame.input.switch", "address": 76, "reason": "Projected onto the trap door primitive's own rotation state (PrTrap.RotX); the retained script sets this switch programmatically rather than reading a separate contact-switch object."},
	{"group": "pinmame.output.solenoid", "address": 3, "reason": "Projected onto switch 46's position; the retained script's bsHideout saucer helper shares switch 46's own kicker object."},
	{"group": "pinmame.output.solenoid", "address": 5, "reason": "Projected onto the trap door primitive; open/close solenoids share the mechanism's own position with switch 76."},
	{"group": "pinmame.output.solenoid", "address": 6, "reason": "Projected onto the trap door primitive; see solenoid 5."},
	{"group": "pinmame.output.solenoid", "address": 16, "reason": "Projected onto switch 65's position; the retained script's bsRudy saucer helper shares switch 65's own kicker object."},
	{"group": "pinmame.output.solenoid", "address": 21, "reason": "Projected onto switch 51 (Dummy Jaw) at Rudy's mouth; no dedicated jaw-motor VPX object exists apart from the head figure."},
	{"group": "pinmame.output.solenoid", "address": 22, "reason": "Projected onto switch 51 (Dummy Jaw); see solenoid 21."},
	{"group": "pinmame.output.solenoid", "address": 25, "reason": "Projected onto Rudy's eyelid assembly, the centre of the PrLids primitive's world-space mesh bounds, which spans both eyes."},
	{"group": "pinmame.output.solenoid", "address": 26, "reason": "Projected onto Rudy's eyelid assembly; see solenoid 25."},
	{"group": "pinmame.output.solenoid", "address": 27, "reason": "Projected onto Rudy's eyelid assembly; see solenoid 25."},
	{"group": "pinmame.output.solenoid", "address": 28, "reason": "Projected onto Rudy's eyelid assembly; see solenoid 25."},
]
WORLD_BOUNDS = {
	"export": "vpxtool git:v0.33.3 export obj --units vpu of the retained table; world x and y are table x and y, z is minus height",
	"export_sha256": "ac1ab343fa91d845ae2deaed128a808499212e518c77cc2bac90a44f47453046",
	"retained": "external:pinmame-review-artifacts/funhouse-1990/vpx-world-obj",
	"objects": {
		"PrLids": {"x": [528.0463, 725.6938], "y": [454.4735, 537.1692], "centre": [0.65028, 0.229335], "use": "projection of solenoids 25-28"},
		"pShade1": {"x": [686.1957, 794.5472], "y": [638.7455, 715.9221], "centre": [0.76802, 0.31329], "use": "lamp shade over the RudyShade light, public G.I. 1's socket"},
		"Flasher1": {"x": [551.4502, 616.2143], "y": [133.9312, 190.782], "centre": [0.605635, 0.075096], "use": "back-panel dome of flasher 17"},
		"Flasher2": {"x": [704.8377, 769.6018], "y": [180.365, 237.2157], "centre": [0.764751, 0.096573], "use": "back-panel dome of flasher 23"},
		"Flasher6": {"x": [861.563, 926.3271], "y": [227.349, 284.1997], "centre": [0.927329, 0.118305], "use": "back-panel dome of flasher 24"},
		"BulbFil1": {"x": [631.8482, 651.056], "y": [1148.5985, 1167.8063], "centre": [0.665407, 0.535709], "use": "lamp 58's overhead bulb"},
		"BulbFil2": {"x": [243.3322, 262.54], "y": [687.7782, 706.986], "centre": [0.262382, 0.322563], "use": "lamp 57's overhead bulb"},
		"L71": {"x": [316.3575, 334.7896], "y": [419.3924, 457.911], "centre": [0.337732, 0.202892], "use": "lamp 71's glass"},
		"L74": {"x": [316.3682, 334.8003], "y": [425.697, 464.2156], "centre": [0.337743, 0.205808], "use": "lamp 74's glass"},
		"L75": {"x": [316.3756, 334.8077], "y": [433.2191, 471.7376], "centre": [0.337751, 0.209287], "use": "lamp 75's glass"},
		"L76": {"x": [316.3953, 334.8274], "y": [442.4356, 480.9542], "centre": [0.337771, 0.21355], "use": "lamp 76's glass"},
		"L77": {"x": [316.366, 334.7981], "y": [450.2728, 488.7914], "centre": [0.337741, 0.217175], "use": "lamp 77's glass"},
		"L78": {"x": [316.3456, 334.7777], "y": [462.8688, 501.3874], "centre": [0.33772, 0.223001], "use": "lamp 78's glass"},
	},
	"note": "Lock_Release_Prim (solenoid 8) is not in the export; its local mesh is symmetric about its origin (x -41.85..41.85, y -38.05..38.05) and unrotated, so its position (187.77698, 398.6577) is its plan centre.",
}
GI_METHOD = (
	"Public G.I. names, wires, pins, fuses and triacs come from the L-9 ROM's T.6 test. Public 1's socket is the spotlight, the "
	"RudyShade Light under the table's lamp-shade primitives (Case 1). For public 2 and 4 the retained 1.3 table draws a bulb at "
	"only some of the Lights its script drives (Case 2 GI_Upper, Case 4 GI_Lower), so the bulbs come from version 2.0c of the same "
	"table, which models a bulb (pBulb glass, pFiliment filament, pFBase base) under each Light its script assigns to the same "
	"public string (GI_UpperBulbs, GI_LowerBulbs). A socket is a 2.0c bulb with a driven 1.3 Light within 0.01 normalized; of the "
	"co-located 1.3 render doubles the placement is the one that shows its own bulb mesh, else the one on a BulbFil filament "
	"primitive, else the one with the smallest falloff radius. A 1.3 Light under no 2.0c bulb makes no socket. Both tables split "
	"the strings as the ROM's names do (Rudy's spotlight, rear playfield, front playfield) and as the owners traced the orange and "
	"violet strings, no retained table contradicts the split, and public 0 and 3 light only the backbox (docs/SPATIAL.md, G.I. "
	"string membership). The manuals draw no G.I. socket and give no per-string bulb count, so no quantity is asserted."
)
APRON_GI_BLOCKER = (
	"Public G.I. 4 (FRONT PLAYFIELD) also feeds G.I. bulbs under the apron, which a parts supplier names in the owner thread "
	"on the violet string and which the retained 1.3 table suggests with two render lights under its apron instruction cards. "
	"No manual page, drawing or parts list draws them, and neither retained table models a bulb there, so their number and "
	"positions are unknown and the string's placements are incomplete. Resolution path: a recreation that models those "
	"bulbs, or a drawing that locates them, checked for number and sockets against a photograph of a FunHouse playfield "
	"with the apron removed, which any owner can take."
)
GI_NOT_PLACED = {
	"RudySign1, RudySign2": "f_refl glow sprites Case 1 drives on Rudy's face; the spotlight that lights them is RudyShade",
	"Light22": "public 2 render light 0.026 normalized from the Light23 socket; neither table models a bulb under it",
	"Bottom_GI_32, Bottom_GI_39": (
		"public 4 render lights under the apron instruction cards; neither table models a bulb there, and the apron G.I. "
		"bulbs a parts supplier names are the record's blocker"
	),
	"LowerGI_B14": "halo partner of LowerGI_B4 at Light33's socket, 0.014 normalized from it and on no bulb",
	"public 1 backbox branch, public 4 coin-door lamps": "cabinet parts of playfield strings, not placed",
}


def build_spatial_report(definition: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition and the drawing check so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	for device in definition["inputs"]:
		spatial = device["spatial"]
		address = int(device["binding"]["device"])
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
	placements = drawing_callouts.placements_of(definition)
	seed = load_json(CALLOUT_SEED_PATH)
	seed_sha256 = hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest()
	gi = {device["binding"]["device"]: device for device in definition["outputs"] if device["binding"]["group"] == "pinmame.output.gi"}
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "partial",
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
			"manifest_uri": "external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"revision_extraction": {
			"fail_closed": True,
			"file_count": REVISION_FILE_COUNT,
			"manifest_sha256": REVISION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/funhouse-1990/v2-0c/extracted-vpxtool.manifest.json",
			"source_ref": REVISION_EXTRACTION_SOURCE,
			"total_bytes": REVISION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"world_bounds": WORLD_BOUNDS,
		"source_hashes": {
			"callout_seed_sha256": seed_sha256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"operator_handbook_sha256": OPERATOR_HANDBOOK_SHA256,
			"playfield_photo_sha256": PLAYFIELD_PHOTO_SHA256,
			"table_sha256": TABLE_SHA256,
			"revision_table_sha256": REVISION_TABLE_SHA256,
			"revision_script_sha256": REVISION_SCRIPT_SHA256,
		},
		"placement_count": len(placements),
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"drawing_callout_check": drawing_callouts.summary(seed, decisions, CALLOUT_SEED_RELATIVE, seed_sha256),
		"excluded_checks": seed["excluded_checks"],
		"drawing_measurements": {
			key: {"page": item["page"], "label": item["label"], "pixel": item["pixel"], "normalized": item["normalized"], "note": item["note"]}
			for key, item in sorted(seed["measurements"].items())
		},
		"general_illumination": {
			"method": GI_METHOD,
			"placed": {str(address): [[placement["x"], placement["y"]] for placement in gi[address]["spatial"]["placements"]] for address in sorted(gi) if gi[address]["spatial"]["status"] != "not_applicable"},
			"sockets": {str(public): [{"light": light, "revision_bulb": bulb} for light, bulb, _ in sockets] for public, sockets in GI_SOCKETS.items()},
			"match_limit": GI_MATCH_LIMIT,
			"backbox_only": [address for address in sorted(gi) if gi[address]["spatial"]["status"] == "not_applicable"],
			"not_placed": GI_NOT_PLACED,
		},
		"projections": PROJECTIONS,
		"unresolved": [],
		"blockers": [APRON_GI_BLOCKER],
		"promotion_decision": (
			"partial: the apron G.I. bulbs of public G.I. 4 are known but unplaced. Otherwise every used switch, coil, motor, flasher, "
			"lamp and G.I. string has a validated placement or a controlled "
			"not-applicable record, every placement the factory drawings mark agrees with its callout, and the definition carries "
			"no conflict."
		),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	pages = ", ".join(f"{key} ({page['locator'].split(' (')[0].split(': ')[-1]}; {page['controls']} controls, control leave-one-out at most {page['control_loo_max']}, {page['callout_pairs']} callout pairs)" for key, page in sorted(check["pages"].items()))
	lines = [
		"# FunHouse (Williams, 1990) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record lives at `machines/partial/williams/funhouse-1990.json`.",
		"",
		f"The matching source is the retained known-working `Funhouse (Williams 1990)_1.3.vpx` at SHA-256 `{TABLE_SHA256}`. Its embedded script at SHA-256 `{SCRIPT_SHA256}` is the runtime and causality authority. Exact playfield bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime address and causality authority; the Williams manuals are the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry, checked against the factory location drawings.",
		"- Each placement is the table object the script binds for the device: the trigger, target, kicker, bumper or slingshot wall for a switch, the object a solenoid callback moves, and for a lamp or flasher the Light the script fades, or the bulb the table models where the script flashes only a glow sprite (lamps 57 and 58 on their overhead BulbFil filaments). A primitive is placed at the centre of its world-space mesh bounds, never at its stored position: the Magic Mirror lamp glasses L71 and L74-L78 and the back-panel flasher domes.",
		f"- Drawing check: {check['rule']} Pages: {pages}. {check['validated']} of {check['checked']} checked placements agree; the others are second bulbs under an insert the drawing marks once.",
		"- The November 1990 handbook prints the factory drawings at 600 dpi; they are the same artwork as the operations manual's 2-36, 2-38 and 2-40 drawings. Each page is fitted on its three jet-bumper caps, its three flipper pivots and its outer frame's top corners, which match the table bounds.",
		"- A number the drawing prints with no leader in open space or along an edge marks no part, so it checks nothing; the placements whose only read is such a number are listed as excluded checks. The flashers 17, 23 and 24 each have a back-panel dome, which the drawing labels only in a leader-less row along the top rail.",
		"- The three Steps switches (15, 26, 36) and the three Steps lamps (54, 55, 56) are drawing measurements: the drawing puts the switches on three wire slots across the Steps track and the lamps on small sockets on its left rail, while the table's invisible star triggers lie 0.06-0.07 from the slots, outside the drawn track and twice as far apart, and its raised `_finger_1` sign hotspots 0.05-0.08 from the sockets.",
		"- Solenoid 8 (Multi-ball Release) is the lock-release gate primitive the script's MBRelease swings, where the drawing prints 8; the coils of Rudy's eyes and eyelids (25-28) project onto the eyelid assembly inside his head.",
		"- Lamp 12 is `Gangway 100,000`: two Williams lamp-matrix pages and the physical playfield photograph agree, resolving the older lamp-location page's isolated `10,000` as a typo.",
		"- Switch 63 is placed on the retained `ballrelease` kicker because the handbook locates it at the right trough and the script asserts and clears that exact switch as the kicker receives and releases the ball.",
		"- FunHouse is pre-Fliptronics WPC-Alpha hardware. It has lower-right, lower-left, and upper-left direct-wired physical flippers. PinMAME publishes two button-driven synthetic sides at 45-48 for digital animation; the left callback drives both fitted left bats, and those virtual states have no playfield coordinates of their own.",
		"",
		"## General illumination",
		"",
		report["general_illumination"]["method"],
		"",
	]
	for address, positions in report["general_illumination"]["placed"].items():
		sockets = report["general_illumination"]["sockets"].get(address, [])
		detail = ", ".join("{} ({})".format(item["light"], item["revision_bulb"]) for item in sockets)
		lines.append(f"- Public {address}: {len(positions)} socket{'s' if len(positions) != 1 else ''}{': ' + detail if detail else ''}.")
	lines.append(f"- Public {' and '.join(str(address) for address in report['general_illumination']['backbox_only'])}: backbox only, controlled `cabinet_or_service` records.")
	for name, reason in report["general_illumination"]["not_placed"].items():
		lines.append(f"- Not placed, {name}: {reason}.")
	lines += ["", "## Drawing measurements", ""]
	for key, item in report["drawing_measurements"].items():
		lines.append(f"- `{key}` on {item['page']} at pixel {item['pixel']}: ({item['normalized'][0]}, {item['normalized'][1]}). {item['note']}")
	lines += ["", "## Excluded checks", ""]
	for key, reason in report["excluded_checks"].items():
		lines.append(f"- `{key}`: {reason}.")
	lines += ["", "## Explicit projections", ""]
	for entry in report["projections"]:
		lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += ["", "## Blockers", ""]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		report["promotion_decision"],
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Version 2.0c table SHA-256 `{REVISION_TABLE_SHA256}`, extraction manifest `{report['revision_extraction']['manifest_uri']}`, "
		f"SHA-256 `{REVISION_MANIFEST_SHA256}`, {REVISION_FILE_COUNT} files, {REVISION_TOTAL_BYTES} bytes.",
		f"- World-space OBJ export SHA-256 `{report['world_bounds']['export_sha256']}`, retained at `{report['world_bounds']['retained']}`.",
		f"- Drawing-callout reads, tiles, overlays and generators: `external:pinmame-review-artifacts/{check['retained_artifacts']['directory']}`, manifest SHA-256 `{check['retained_artifacts']['manifest_sha256']}`.",
		"- Human transcription of every printed table read from the rendered original manual pages: `external:pinmame-review-artifacts/funhouse/manual-transcription.md`.",
		f"- Maintainer-supplied November 1990 operator handbook SHA-256 `{OPERATOR_HANDBOOK_SHA256}` and lower-playfield photograph SHA-256 `{PLAYFIELD_PHOTO_SHA256}`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition, decisions = build_with_decisions()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition, decisions)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale_author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready.exists():
		stale_author_ready.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale_author_ready_path = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready_path.exists():
		raise RuntimeError(f"Stale FunHouse author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"FunHouse definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"FunHouse seed is missing: {seed_path}")
	definition, decisions = build_with_decisions()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"FunHouse definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"FunHouse seed is not byte-identical to the canonical definition: {seed_path}")
	report = build_spatial_report(definition, decisions)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"FunHouse spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"FunHouse spatial review drifted from its deterministic curator: {markdown_path}")
	print("FunHouse definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"FunHouse extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		verify_revision_manifest(source_root)
		if derive_gi_sockets(source_root) != (GI_SOCKETS, GI_UNMATCHED):
			raise RuntimeError("FunHouse G.I. sockets drifted from the two retained extractions")
		print("FunHouse retained extractions match their pinned manifest identities and the G.I. sockets.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
