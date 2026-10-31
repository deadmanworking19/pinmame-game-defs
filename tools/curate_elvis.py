"""Curate the physical Stern Elvis (2004) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived
fact as a literal and reads two committed seeds, the placements (the retained table's object coordinates, rebuilt by
tools/elvis_spatial_seed.py) and the pinned DMD frame readings of the ROM's own service tests (checked against the
retained frames by tools/elvis_runtime_evidence.py), so regeneration reproduces the canonical artifact byte-for-byte
without reading the external evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only path that
writes the definition, its knowledge note and its spatial report.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "stern.elvis.2004"
PARTIAL_PATH = ROOT / "machines/partial/stern/elvis-2004.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/elvis-2004.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/elvis-2004.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/stern/elvis-2004-knowledge.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/stern/elvis-2004-spatial.json"
FRAME_READINGS_PATH = ROOT / "tools/seeds/stern/elvis-2004-frame-readings.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/elvis-2004.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/stern/elvis-2004.md"
RUNTIME_PATH = "evidence/runtime/whitestar/elvis-service-tests-and-gameplay.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = "pinmame.catalog.46e1a01a0f73"
CORE_SOURCE = "pinmame.core.46e1a01a0f73"
SIM_SOURCE = "pinmame.sim.elvis.46e1a01a0f73"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
IDENTITY_SOURCE = "identity.stern.elvis.2004"
MANUAL_SOURCE = "manual.stern.elvis.2004"
VPX_TABLE_SOURCE = "vpx-table.elvis-1-0-2"
VPX_SCRIPT_SOURCE = "vpx-script.elvis-1-0-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.elvis-1-0-2"
VPX_CORPUS_SOURCE = "vpx-script.3a91c538688f7243"
VPM_LIBRARY_SOURCE = "vpm-script-library.sega-vbs"
RUNTIME_SOURCE = "runtime.elvis.elvis-5-00"
ROM_SOURCE = "rom.stern.elvis.5-00"
RUNTIME_LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "41c03d0d0fab430d29ff382d86d091139f482e23e61964f43672c15fdf7eb34b"
SIM_FILE_SHA256 = "9d36797b3426ec02c87bc6b879744f13e736744db9b8dd83fe7a2513d9dc2b15"
SE_FILE_SHA256 = "62a75510b900b98ae3d22b2c1e1eb41e7bcf582721375955a3cb5a6b24aef751"
CORE_FILE_SHA256 = "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00"
# Retained harness run directory -> SHA-256 of its manifest.json (tools/elvis_runtime_evidence.py pins the same values).
RUN_MANIFESTS = {
	"elvis-switch-test": "48aeb1628a2055d8f99b33eb0524d0c646ff87d8d7ab4b31e1624d39c8077b82",
	"elvis-switch-timing-probe": "c3f5e3602901a3942d67bdb200581113f9a3f2c6c5fb4d8f26fb079cbcc7ec87",
	"elvis-dedicated-switch-test": "c99c5cc5da4d36ea674eb0294f67a361a598493a57ce54d599c6870482b1b034",
	"elvis-single-coil-test": "c1247d97fe5c97346b30b0d4f0a4aa402a5089fb4d157f4802384283ac4e9f69",
	"elvis-single-lamp-test": "1aa40d05953353fac69cc84e3b2650ba494a2af39a8227d14ab4a482ca056566",
	"elvis-elvis-test": "8e64c2edd1c67b7e0b9101f47ee591d17a773bf796724ecb411ffcb864dc902d",
	"elvis-stacking-opto": "15b5ec75a3ab2268c8b64b5ad01dc27ae731045b692fbae95b00c07ad3c6fc1e",
	"elvis-gameplay": "1107ea371c63b9e4531275f288d676586e62522e800a6b87629a51f6e59ecf7e",
	"elvis-hound-dog-probe": "fcb00a9da6a59e7f23336a00a263aa5fd2bfa285bc830c7d2047d0f99dc79317",
}

TABLE_NAME = "elvis_mod_1.0.vpx"
TABLE_SHA256 = "d53202dea8620d92b6598894e71b26de59db1a0932234ceb5938f0844d22afc6"
SCRIPT_SHA256 = "51594f64207eca7afec821dea1ecd607d7cc756187d8ff63d7a815bb4c6c17ad"
CORPUS_SHA256 = "3a91c538688f724325c1c9ffc988a9c943baa7332131bd60648c1b4e2b632363"
CORPUS_NAME = "Elvis (Stern 2004) WED SSF Mod.vbs"
VPXTABLE_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
MANUAL_NAME = "Elvis_Manual.pdf"
MANUAL_SHA256 = "83593eb6de4c468c3acfb842c38a81563bc0f4bfbfa6d3a9ff39123b86342125"
MANUAL_URL = "https://wp.sternpinball.com/wp-content/uploads/2018/12/Elvis_Manual.pdf"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=4983"
IPDB_CAPTURE_URL = "https://web.archive.org/web/20261016065404id_/https://www.ipdb.org/machine.cgi?id=4983"
IPDB_PAGE_SHA256 = "8a5c0ff918472c65f2b69a861009067328001b005146d67e4d70daeb0efacc02"
IPDB_CAPTURE_GZIP_SHA256 = "d10bf11caf94cfef1717f6878c404472c7216547dce9992fe81e613bedcd846b"
VPM_SEGA_SHA256 = "d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2115.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2115"

EXTRACTION_FILE_COUNT = 1119
EXTRACTION_TOTAL_BYTES = 43639921
EXTRACTION_MANIFEST_SHA256 = "43fad35f4be49537c2ff14cba101defb2f6dfe0117d15f4889642f92743a2fea"
EXTRACTION_RELATIVE_PATH = Path("stern/elvis-2004/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("stern/elvis-2004/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"
EXCERPT_CREDIT = "curator, read from the rendered page"
QUOTE_CREDIT = "curator, quoted from the source file"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


@functools.lru_cache(maxsize=None)
def _frame_readings() -> dict[str, dict[str, str]]:
	runs = load_json(FRAME_READINGS_PATH)["runs"]
	return {run: {label: entry["reading"] for label, entry in readings.items()} for run, readings in runs.items()}


def _reading(run: str, label: str) -> str:
	"""The pinned reading of one retained DMD frame; a missing pin is a curator error, never a silent gap."""
	readings = _frame_readings().get(run, {})
	if label not in readings:
		raise RuntimeError(f"Elvis frame readings do not pin {run!r} / {label!r}")
	return readings[label]


def _service_line(reading: str) -> str:
	"""The lines below the test's title, as the ROM printed them."""
	return reading.split(" / ", 1)[1]


# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = (
	"elv100", "elv302", "elv302f", "elv302g", "elv302i", "elv302l", "elv303", "elv303f", "elv303g", "elv303i", "elv303l",
	"elv400", "elv400f", "elv400g", "elv400i", "elv400l", "elvis", "elvisf", "elvisg", "elvisi", "elvisl",
)
BASE_DRIVER_NOTE = (
	"src/wpc/sims/se/prelim/elvis.c builds every Stern Elvis driver on the de_mSES3 machine driver with one init_elvis, which "
	"installs elvisGameData (GEN_WS, a 128x32 DMD, FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), lamp columns 2, no custom solenoids, no "
	"auxiliary board, no inverted switches, start/tilt/slam 54/56/55) and the elvis_w stepper model on the solenoid latches "
	"0x2000-0x2003. MACHINE_INIT(se3) gives every set the fast-flip byte at CPU RAM 0x04 and the Elvis root's sets the #89 "
	"bulb model on 20-23 and 31-32. The controller routing, lamp columns and display are therefore identical; a language set "
	"pairs that language's CPU, display and sound/voice ROMs. "
)
# driver -> (CPU version, CPU ROM, CRC, display ROM, CRC, language, sound set macro)
DRIVER_ROMS = {
	"elvis": ("5.00", "elvscpua.500", "aae9d65d", "elvsdspa.500", "76a672cb", "English", "ELVIS_SND"),
	"elvisl": ("5.00", "elvscpul.500", "d6813d67", "elvsdspl.500", "68946b3b", "Spanish", "ELVIS_SND_SP"),
	"elvisg": ("5.00", "elvscpug.500", "1582dd3a", "elvsdspg.500", "4b6e7d37", "German", "ELVIS_SND_GR"),
	"elvisf": ("5.00", "elvscpuf.500", "e977fdb0", "elvsdspf.500", "e4ce2da7", "French", "ELVIS_SND_FR"),
	"elvisi": ("5.00", "elvscpui.500", "11bafdbb", "elvsdspi.500", "3ecbadb2", "Italian", "ELVIS_SND_IT"),
	"elv400": ("4.00", "elvscpua.400", "385be9ed", "elvsdspa.401", "fb08d5c3", "English", "ELVIS_SND"),
	"elv400l": ("4.00", "elvscpul.400", "536d4e3c", "elvsdspl.401", "57fc6ed2", "Spanish", "ELVIS_SND_SP"),
	"elv400g": ("4.00", "elvscpug.400", "c5992b96", "elvsdspg.401", "a694f642", "German", "ELVIS_SND_GR"),
	"elv400f": ("4.00", "elvscpuf.400", "9ae4f3c4", "elvsdspf.401", "1ddd1823", "French", "ELVIS_SND_FR"),
	"elv400i": ("4.00", "elvscpui.400", "dd2876fc", "elvsdspi.401", "51f92cec", "Italian", "ELVIS_SND_IT"),
	"elv303": ("3.03", "elvscpua.303", "a0dd77d8", "elvsdspa.302", "892da6d2", "English", "ELVIS_SND"),
	"elv303l": ("3.03", "elvscpul.303", "691b9882", "elvsdspl.302", "f75ea4cb", "Spanish", "ELVIS_SND_SP"),
	"elv303g": ("3.03", "elvscpug.303", "66b50538", "elvsdspg.302", "6340bb11", "German", "ELVIS_SND_GR"),
	"elv303f": ("3.03", "elvscpuf.303", "bc5cc2b9", "elvsdspf.302", "410b6ae5", "French", "ELVIS_SND_FR"),
	"elv303i": ("3.03", "elvscpui.303", "11f47b7a", "elvsdspi.302", "217c7d17", "Italian", "ELVIS_SND_IT"),
	"elv302": ("3.02", "elvscpua.302", "52fd7068", "elvsdspa.302", "892da6d2", "English", "ELVIS_SND"),
	"elv302l": ("3.02", "elvscpul.302", "0c6f1897", "elvsdspl.302", "f75ea4cb", "Spanish", "ELVIS_SND_SP"),
	"elv302g": ("3.02", "elvscpug.302", "9d907782", "elvsdspg.302", "6340bb11", "German", "ELVIS_SND_GR"),
	"elv302f": ("3.02", "elvscpuf.302", "893a5ac6", "elvsdspf.302", "410b6ae5", "French", "ELVIS_SND_FR"),
	"elv302i": ("3.02", "elvscpui.302", "a2c15460", "elvsdspi.302", "217c7d17", "Italian", "ELVIS_SND_IT"),
	"elv100": ("1.00", "Elvis_cpu_1.00.bin", "5ca9aadc", "Elvis_display_1.00.bin", "8feffc70", "English", "ELVIS_SND"),
}
DRIVER_COMPATIBILITY = {driver_id: "identical" for driver_id in DRIVER_IDS}


def _driver_note(driver_id: str) -> str:
	version, cpu, cpu_crc, display, display_crc, language, sound = DRIVER_ROMS[driver_id]
	note = (
		f"CPU {version} ({cpu}, CRC {cpu_crc}) with the {language} display ROM {display} (CRC {display_crc}) and the {sound} sound "
		"and voice set."
	)
	if version == "4.00":
		note += (
			" The manual's firmware appendix names game ROM A4.00 (check sum $90FF, U210) and display ROM A4.01 ($0502, U5), the "
			"USA pair elv400 loads (elvscpua.400 and elvsdspa.401)."
		)
	elif version in ("3.03", "3.02"):
		note += " The 3.02 and 3.03 sets share their display ROMs. No document this record holds names a 3.0x release."
	elif version == "1.00":
		note += " No document this record holds names a 1.00 release."
	else:
		note += " No document this record holds names a 5.00 release; it is pinned PinMAME's latest Elvis code and the catalog root."
	if driver_id == "elvis":
		note += (
			" The retained table loads it (Const cGameName = \"elvis\"), and all nine harness runs booted it from the "
			"user-authorized elvis.zip."
		)
	else:
		note += " No harness run booted it."
	return note


# --- Switch data -------------------------------------------------------------------------------------
# address -> (label, grid name, mounting class, part cell, switch type, availability, roles, pulse)
SWITCHES: dict[int, tuple[str, str, str, str, str, str, tuple[str, ...], bool]] = {
	1: ("Left Cabinet Button (UK Only)", "LT BUTTON (UK ONLY)", "Cabinet Side", "180-5160-00", "button", "optional", ("cabinet.uk-button-left",), False),
	2: ("4th Coin Slot", "4TH COIN SLOT", "Coin Door", "180-5204-00", "other", "optional", ("cabinet.coin.fourth",), True),
	3: ("6th Coin Slot", "6TH COIN SLOT", "Coin Door", "Future Use", "other", "optional", ("cabinet.coin.sixth",), True),
	4: ("Right Coin Slot", "RIGHT COIN SLOT", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.right",), True),
	5: ("Center Coin Slot / DBA", "CENTER COIN SLOT / DBA", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.center",), True),
	6: ("Left Coin Slot", "LEFT COIN SLOT", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.left",), True),
	7: ("5th Coin Slot", "5TH COIN SLOT", "Coin Door", "Future Use", "other", "optional", ("cabinet.coin.fifth",), True),
	8: ("Right Cabinet Button (UK Only)", "RT BUTTON (UK ONLY)", "Cabinet Side", "180-5160-00", "button", "optional", ("cabinet.uk-button-right",), False),
	9: ("Spot Note Standup", "SPOT NOTE STANDUP", "Below P/F", "515-5162-08", "leaf", "used", (), True),
	10: ("Shooter Lane Exit", "SHOOTER LANE EXIT", "Above P/F", "180-5190-28", "microswitch", "used", ("ball.path",), False),
	11: ("4-Ball Trough 1 (Left)", "4-BALL TROUGH #1 (LEFT)", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	12: ("4-Ball Trough 2", "4-BALL TROUGH #2", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	13: ("4-Ball Trough 3", "4-BALL TROUGH #3", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	14: ("4-Ball Trough VUK Opto", "4-BALL TROUGH VUK OPTO", "Below P/F", "See Sw. 14 Note", "opto", "used", ("ball.position",), False),
	15: ("4-Ball Stacking Opto", "4-BALL STACKING OPTO", "Below P/F", "See Sw. 15 Note", "opto", "used", ("ball.path",), False),
	16: ("Shooter Lane", "SHOOTER LANE", "Below P/F", "180-5157-00", "unknown", "used", ("ball.position",), False),
	17: ("ELVIS Drop Target E", "( E )LVIS", "Below P/F", "180-5158-00", "leaf", "used", (), False),
	18: ("ELVIS Drop Target L", "E( L )VIS", "Below P/F", "180-5158-00", "leaf", "used", (), False),
	19: ("ELVIS Drop Target V", "EL( V )IS", "Below P/F", "180-5158-00", "leaf", "used", (), False),
	20: ("ELVIS Drop Target I", "ELV( I )S", "Below P/F", "180-5158-00", "leaf", "used", (), False),
	21: ("ELVIS Drop Target S", "ELVI( S )", "Below P/F", "180-5158-00", "leaf", "used", (), False),
	22: ("TCB Target T", "( T )CB", "Below P/F", "515-5162-08", "leaf", "used", (), True),
	23: ("TCB Target C", "T( C )B", "Below P/F", "515-5162-08", "leaf", "used", (), True),
	24: ("TCB Target B", "TC( B )", "Below P/F", "515-5162-08", "leaf", "used", (), True),
	25: ("Spinner", "SPINNER", "Above P/F", "180-5010-04", "unknown", "used", (), True),
	26: ("Left Orbit High", "LEFT ORBIT HI", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), False),
	27: ("Inner Loop", "INNER LOOP", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), False),
	28: ("Right Ramp Exit", "RIGHT RAMP EXIT", "Above P/F", "180-5010-01", "microswitch", "used", ("ball.path",), False),
	30: ("Left Ramp Made", "LEFT RAMP MADE", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), False),
	31: ("Left Ramp Exit", "LEFT RAMP EXIT", "Above P/F", "180-5010-01", "microswitch", "used", ("ball.path",), False),
	32: ("Top Saucer Eject", "TOP SAUCER EJECT", "Below P/F", "180-5186-00", "microswitch", "used", ("ball.position",), False),
	33: ("Elvis Home", "ELVIS HOME", "Below P/F", "180-5189-00", "microswitch", "used", ("mechanism.position",), False),
	34: ("Center Saucer Eject", "CENTER SAUCER EJECT", "Below P/F", "180-5186-00", "microswitch", "used", ("ball.position",), False),
	36: ("KING Target K", "( K )ING", "Below P/F", "515-7381-00", "leaf", "used", (), True),
	37: ("KING Target I", "K( I )NG", "Below P/F", "515-7381-00", "leaf", "used", (), True),
	38: ("KING Target N", "KI( N )G", "Below P/F", "515-7381-00", "leaf", "used", (), True),
	39: ("KING Target G", "KIN( G )", "Below P/F", "515-7381-00", "leaf", "used", (), True),
	40: ("Scarf Standup", "SCARF STANDUP", "Below P/F", "515-5967-02", "leaf", "used", (), True),
	41: ("Left Top Lane", "LEFT TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	42: ("Middle Top Lane", "MIDDLE TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	43: ("Right Top Lane", "RIGHT TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	45: ("Right Ramp Made", "RIGHT RAMP MADE", "Above P/F", "180-5190-28", "microswitch", "used", ("ball.path",), False),
	46: ("Right Orbit Low", "RIGHT ORBIT LOW", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), False),
	47: ("Right Orbit High", "RIGHT ORBIT HI", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), False),
	48: ("Hotel Post", "HOTEL POST", "Above P/F", "180-5189-00", "microswitch", "used", ("ball.position",), False),
	49: ("Left Bumper", "LEFT BUMPER", "Below P/F", "180-5015-05", "leaf", "used", (), True),
	50: ("Right Bumper", "RIGHT BUMPER", "Below P/F", "180-5015-05", "leaf", "used", (), True),
	51: ("Bottom Bumper", "BOTTOM BUMPER", "Below P/F", "180-5015-05", "leaf", "used", (), True),
	52: ("Top Hotel Standup", "TOP HOTEL STANDUP", "Mini P/F", "515-5162-08", "leaf", "used", (), True),
	53: ("Bottom Hotel Standup", "BOTTOM HOTEL STANDUP", "Mini P/F", "515-5162-08", "leaf", "used", (), True),
	54: ("Start Button", "START BUTTON", "In Cabinet", "180-5174-00", "button", "used", ("cabinet.start",), False),
	55: ("Tournament Start", "TOURNAMENT START", "In Cabinet", "180-5174-00", "button", "optional", ("cabinet.tournament-start",), False),
	56: ("Plumb Bob Tilt", "PLUMB BOB TILT", "In Cabinet", "See Sw. 56 Note", "tilt", "used", ("cabinet.tilt",), False),
	57: ("Left Outlane", "LEFT OUTLANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	58: ("Left Return Lane", "LEFT RETURN LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	59: ("Left Slingshot", "LEFT SLINGSHOT", "Below P/F", "180-5054-00 (x2)", "leaf", "used", (), True),
	60: ("Right Outlane", "RIGHT OUTLANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	61: ("Right Return Lane", "RIGHT RETURN LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	62: ("Right Slingshot", "RIGHT SLINGSHOT", "Below P/F", "180-5054-00 (x2)", "leaf", "used", (), True),
	63: ("Hotel Door", "HOTEL DOOR", "Above P/F", "180-5119-02", "microswitch", "used", (), False),
	64: ("Hound Dog", "HOUND DOG", "Above P/F", "180-5190-28", "microswitch", "used", (), False),
}
UNUSED_SWITCHES = (29, 35, 44)
DOTS_SWITCHES = (17, 18, 19, 20, 21)
MATRIX_DRIVE = [("GRN-BRN", "CN5-P1"), ("GRN-RED", "CN5-P3"), ("GRN-ORG", "CN5-P4"), ("GRN-YEL", "CN5-P5"), ("GRN-BLK", "CN5-P6"), ("GRN-BLU", "CN5-P7"), ("GRN-VIO", "CN5-P8"), ("GRN-GRY", "CN5-P9")]
MATRIX_RETURN = [("WHT-BRN", "CN7-P9", "U400"), ("WHT-RED", "CN7-P8", "U400"), ("WHT-ORG", "CN7-P7", "U400"), ("WHT-YEL", "CN7-P6", "U400"), ("WHT-GRN", "CN7-P5", "U401"), ("WHT-BLU", "CN7-P3", "U401"), ("WHT-VIO", "CN7-P2", "U401"), ("WHT-GRY", "CN7-P1", "U401")]
# What the retained 1.0.2 table's embedded script does with each address (line numbers of that script).
SWITCH_SCRIPT = {
	4: "sega.vbs maps a coin key to swCoin3 = 4",
	5: "sega.vbs maps a coin key to swCoin1 = 5",
	6: "sega.vbs maps a coin key to swCoin2 = 6",
	9: "sw9_Hit pulses 9 (line 377)",
	10: "sw10_Hit and sw10_unHit write 10 (lines 379-380), but the table contains no sw10 object, so 10 is never written",
	11: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 84-89): a cvpmBallStack holding 11 at 1 while a ball occupies that position",
	12: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 84-89)",
	13: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 84-89)",
	14: "bsTrough.InitSw 0, 14, 13, 12, 11 (lines 84-89): 14 is the exit position the release kicker BallRelease empties, held at 1 while a ball waits there",
	15: "only SolTrough writes it, as vpmTimer.PulseSw 15 each time Q1 fires (lines 313-316): the kicked ball passing the upper beam",
	16: "the impulse plunger plungerIM (InitImpulseP swplunger; .switch 16; lines 137-141) holds 16 while a ball rests on the trigger swPlunger",
	17: "cvpmDropTarget dtBankL (initdrop sw17-sw21 to 17-21, lines 102-104; sw17_Hit, line 381) holds 17 at 1 while its target is down",
	18: "cvpmDropTarget dtBankL (lines 102-104; sw18_Hit, line 382) holds 18 at 1 while its target is down",
	19: "cvpmDropTarget dtBankL (lines 102-104; sw19_Hit, line 383) holds 19 at 1 while its target is down",
	20: "cvpmDropTarget dtBankL (lines 102-104; sw20_Hit, line 384) holds 20 at 1 while its target is down",
	21: "cvpmDropTarget dtBankL (lines 102-104; sw21_Hit, line 385) holds 21 at 1 while its target is down",
	22: "sw22_Hit pulses 22 (line 386)",
	23: "sw23_Hit pulses 23 (line 387)",
	24: "sw24_Hit pulses 24 (line 388)",
	25: "sw25_Spin pulses 25 on every spin (line 389)",
	26: "Trigger sw26 holds 26 while the ball sits on it (lines 391-392)",
	27: "Trigger sw27 holds 27 while the ball sits on it (lines 393-394)",
	28: "Trigger sw28 holds 28 while the ball sits on it (lines 395-396)",
	30: "Trigger sw30 holds 30 while the ball sits on it (lines 397-398)",
	31: "Trigger sw31 holds 31 while the ball sits on it (lines 399-400)",
	32: "the saucer bsUpper (InitSaucer sw32, 32; lines 126-128; sw32_Hit, line 401) holds 32 while a ball rests in it",
	33: (
		"the cvpmMech mElvis (vpmMechOneSol + vpmMechReverse + vpmMechLinear, Sol1 = 25, Length and Steps 150, AddSw 33, 0, 0; "
		"lines 147-154) holds 33 at 1 at step 0, the end the mech starts from"
	),
	34: "the saucer bsJail (InitSaucer sw34, 34; lines 117-119; sw34_Hit, line 402) holds 34 while a ball rests in it",
	36: "sw36_Hit pulses 36 (line 403)",
	37: "sw37_Hit pulses 37 (line 404)",
	38: "sw38_Hit pulses 38 (line 405)",
	39: "sw39_Hit pulses 39 (line 406)",
	40: "sw40_Hit pulses 40 (line 407)",
	41: "Trigger sw41 holds 41 while the ball sits on it (lines 408-409)",
	42: "Trigger sw42 holds 42 while the ball sits on it (lines 410-411)",
	43: "Trigger sw43 holds 43 while the ball sits on it (lines 412-413)",
	45: "Trigger sw45 holds 45 while the ball sits on it (lines 414-415)",
	46: "Trigger sw46 holds 46 while the ball sits on it (lines 416-417)",
	47: "Trigger sw47 holds 47 while the ball sits on it (lines 418-419)",
	48: "Trigger sw48 holds 48 while the ball sits on it (lines 421-422), and the ball stack bsLock (InitSw 0, 48; InitKick HLock; lines 109-112) holds it while a ball is locked",
	49: "Bumper1_Hit pulses 49 (line 425)",
	50: "Bumper2_Hit pulses 50 (line 426)",
	51: "Bumper3_Hit pulses 51 (line 427)",
	52: "sw52_Hit pulses 52 (line 429)",
	53: "sw53_Hit pulses 53 (line 430)",
	54: "sega.vbs's swStartButton = 54 is what the VPinMAME Start key writes",
	55: (
		"If keyUpperLeft Then Controller.Switch(55) = 1 / = 0 (lines 176 and 183) tests an identifier that neither the script nor "
		"the retained sega.vbs and core.vbs define, instead of the keycode the other key handlers compare"
	),
	56: "vpmNudge.TiltSwitch = 56 (line 79); sega.vbs's swTilt = 56",
	57: "Trigger sw57 holds 57 while the ball sits on it (lines 431-432)",
	58: "Trigger sw58 holds 58 while the ball sits on it (lines 433-434)",
	59: "the left slingshot handler pulses 59 (line 469)",
	60: "Trigger sw60 holds 60 while the ball sits on it (lines 435-436)",
	61: "Trigger sw61 holds 61 while the ball sits on it (lines 437-438)",
	62: "the right slingshot handler pulses 62 (line 488)",
	63: "Trigger sw63 holds 63 while the ball sits on it (lines 502-503)",
	64: (
		"sw64_Hit pulses 64 to 1 (lines 505-506) and leaves it at 0 between hits, which is the level the ROM reads as a hit, so "
		"the table presents a resting hound dog as permanently hit and a hit as a brief return to rest; HoundDog.TransZ animates "
		"the dog (line 522)"
	),
}
# Matrix switches the gameplay run closed in a game, with the outputs the ROM drove during that step (evidence step labels).
GAMEPLAY_RESPONSE = {
	5: "each coin pulsed the optional output 24 four times and flashed 20-23, 31 and 32",
	10: "closing it once after the ball left the shooter lane fired no playfield coil; the figure's outputs 25-30 kept running",
	16: (
		"the served ball resting on it for 6 s drew no auto launch (2); the G.I., off since Start, came back on about 0.6 s after "
		"it closed, and the figure began to move"
	),
	17: "knocking it down and leaving it down ran the shaker output 4 and pulsed the arms coil 30",
	18: "knocking it down and leaving it down ran the shaker output 4",
	19: "knocking it down and leaving it down ran the shaker output 4",
	21: "knocking it down after 17-20 completed the bank: the ROM fired the 5-bank reset 3 three times, 0.33, 0.74 and 1.14 s later, and flashed 22 and 32",
	24: "closing it once flashed the back-panel TCB flasher 21 and the spot light 31, pulsed the arms coil 30 and blinked the G.I.",
	25: "closing it once flashed the spinner flasher 22",
	26: "closing it once ran the shaker motor output 4",
	28: "closing it once ran the shaker output 4 and the figure (25-30)",
	30: "closing it once ran the shaker output 4 and flashed 20-23, 31 and 32",
	32: "a ball resting on it drew one top-eject kick (12) 5.7 s after it arrived, switched the hotel door coil 19 on and flashed 20-23 and 32",
	34: "a ball resting on it drew the centre-eject kick (6) 4.3 s after it arrived and two more about 0.7 s apart, switched 19 on and flashed 20-23 and 32",
	36: "closing it once ran the shaker output 4 and the figure (25-30)",
	37: "closing it once ran the shaker output 4 and pulsed the legs and arms coils 29 and 30",
	38: "closing it once ran the shaker output 4 and pulsed the legs coil 29",
	39: "closing it once ran the shaker output 4 and blinked the G.I.",
	40: "closing it once ran the shaker output 4, pulsed the arms coil 30 and blinked the G.I.",
	41: "closing it once ran the shaker output 4",
	42: "closing it once ran the shaker output 4",
	43: "closing it once ran the shaker output 4",
	45: "closing it once ran the shaker output 4, flashed 20-23, 31 and 32 and pulsed the arms coil 30",
	46: "closing it once ran the shaker output 4 and the figure (25-30)",
	47: "closing it once ran the shaker output 4 and pulsed the legs coil 29",
	48: "a ball resting on it for 6 s drew no hotel lock release (7); the ROM switched the hotel door coil 19 on, flashed 20-23, 31 and 32 and pulsed 29 and 30",
	49: "closing it once fired the left bumper coil 9, ran the shaker output 4, flashed 20 and moved the figure (25-30)",
	50: "closing it once fired the right bumper coil 10, ran the shaker output 4, flashed 20 and moved the figure (25-30)",
	51: "closing it once fired the bottom bumper coil 11, ran the shaker output 4, flashed 20 and moved the figure (25-30)",
	52: "closing it once switched the hotel door coil 19 on, ran the shaker output 4 and flashed 20 and 21",
	53: "closing it once ran the shaker output 4 and flashed 20",
	54: (
		"a press after three coins started a game: the ROM switched the G.I. off, raised the game-on state 15, reset the drop "
		"bank (3) and fired the trough up-kicker 1 about 1.1 s later and twice more about 1.25 s apart before the scenario moved "
		"the served ball to 16"
	),
	57: "closing it once ran the shaker output 4",
	58: "closing it once ran the shaker output 4",
	59: "closing it once fired the left slingshot coil 17, flashed the slingshot flashers 32 and pulsed the legs coil 29",
	60: "closing it once ran the shaker output 4",
	61: "closing it once ran the shaker output 4",
	62: "closing it once fired the right slingshot coil 18 and flashed the slingshot flashers 32",
	63: (
		"closing it once ran the shaker output 4 and flashed 20; in the hound-dog probe, raising it to 1 switched the hotel door "
		"coil 19 on 0.13 s later"
	),
}
GAMEPLAY_QUIET = (9, 20, 22, 23, 27, 31)


def switch_id(address: int) -> str:
	if address in SWITCHES:
		return f"switch.{address}-{slug(SWITCHES[address][0])}"
	return f"switch.{address}-not-used"


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Observed spatial record for one device from the committed placement seed, or None."""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": entry["x"], "y": entry["y"],
			"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
		})
	return {"status": "observed", "placements": placements}


def _placement_note(category: str, address: int) -> str:
	entries = _spatial_seed()[category].get(str(address)) or []
	parts = []
	for entry in entries:
		text = f"{entry['type']} {entry['object']}"
		if entry.get("dome"):
			text += f" on the dome primitive {entry['dome']}"
		if entry.get("projection"):
			text += f" (projection: {entry['projection']})"
		parts.append(text)
	return f" Placement from the retained table's {', '.join(parts)}." if parts else ""


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], status: str = "validated", **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(status, *refs),
	}
	device.update({key: value for key, value in extra.items() if value is not None})
	return device


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	drive_wire, drive_connection = MATRIX_DRIVE[column]
	return_wire, return_connection, receiver = MATRIX_RETURN[row]
	return {
		"board": "Whitestar CPU/Sound board switch matrix", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "return_component": f"column drive Q{column + 1}; row receiver {receiver}",
	}


def _switch_test(address: int) -> str:
	return _reading("elvis-switch-test", f"switch {address} closed in the Switch Test")


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	identifier = switch_id(address)
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
	notes = f"Printed switch-matrix drive column {column + 1}, return row {row + 1}."
	if address in UNUSED_SWITCHES:
		notes += (
			" The Switch Matrix Grid (DR. 4) prints this cell NOT USED in a black box on a grey cell, with no location and no part; "
			"the location drawing calls out no switch with this number, and the retained script never writes it. The 5.00 ROM's "
			f"own Switch Test agrees: closing it printed \"{_service_line(_switch_test(address))}\"."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE),
			aliases=aliases, normally_closed=False, pulse=False, physical={"notes": notes}, wiring=_switch_wiring(address),
			spatial=not_applicable("unused", MANUAL_SOURCE),
		)
	label, printed, mounting, part, switch_type, availability, roles, pulse = SWITCHES[address]
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE)
	physical: dict[str, Any] = {"switch_type": switch_type}
	match = re.match(r"(\d{3}-\d{4}-\d{2})", part)
	if match:
		number = match.group(1)
		physical["assembly_part_number" if number.startswith(("500-", "515-")) else "part_number"] = number
	notes += f' The grid prints "{printed}" with the location "{mounting}" and the part cell "{part}".'
	if part.startswith(("500-", "515-")):
		notes += " The page's part note: 'Part Numbers which start with 515- or 500- include the bracket, target, and/or housing.'"
	reading = _switch_test(address)
	if address == 3:
		notes += (
			" The 5.00 ROM's Switch Test reported nothing for it: closing it, holding it for 1.5 s and, in the timing probe, holding "
			"it for 3 s, releasing it and pulsing it for 100 ms all left the display at NONE. The cabinet wiring diagram draws its "
			"wire to the coin door as '6th Coin Slot Future Use'; whether this ROM reads the input at all is not settled."
		)
	elif address == 64:
		notes += (
			" The 5.00 ROM's Switch Test reports it only on its fall from 1 to 0: closing it and holding it at 1 for 1.5 s (Switch "
			"Test run) or for 1 and 3 s (timing probe) left the display at NONE, as did the instant of release, while 0.5 s after "
			f"the release, and 0.5 s after a 100 ms pulse began, it printed \"{_service_line(_reading('elvis-switch-timing-probe', 'switch 64 open, 0.50 s after its release'))}\". "
			"Every other switch the probe exercised, such as the hotel door 63, is reported 0.5 s after it rises. The ROM therefore "
			"treats 64 as actuated at public 0: the contact rests closed, and a hit opens it. The grid and its legend print no N.O. "
			"or N.C. marking for any matrix switch. Hold 64 at 1 at rest and drop it to 0 for the duration of a hit. In the "
			"hound-dog probe, during a game, each fall of 64 from 1 to 0 made the ROM switch the hotel door coil 19 on about 65 ms "
			"later, and with 64 held at 1 it switched 19 off 2.0-2.5 s later. The Hound Dog Pop-Up Target page (assembly reference "
			"500-6781-00) carries the Micro Switch (Short Flat Actuator) 180-5190-28, the dog 500-6820-00 and a deflector pad, and no coil."
		)
	else:
		notes += f" The 5.00 ROM's Switch Test names it \"{_service_line(reading)}\"."
		if address == 5:
			notes += " The ROM prints CENTER COIN SLOT/DBA without the grid's spaces around the slash."
	if address in DOTS_SWITCHES:
		notes += (
			" The grid tags the cell DOTS (diode on terminal strip). The 5-Bank D/T page lists five Switch (D/T) 180-5158-00 and five "
			"white drop targets 545-6102-01, and notes that the switch diodes, 1N4001, are not on the assembly."
		)
	if address in (59, 62):
		physical["quantity"] = 2
		notes += (
			" Two slingshot stack (blade) switches 180-5054-00 share this matrix address (the grid's '(x2)'); the Slingshots page notes "
			"'Only 1 of the 2 Switches has a Diode', and the location drawing marks the number twice."
		)
	if address in (14, 15):
		notes += (
			" The grid's part note: 'Transmitter & Receiver OPTO PC Boards are used as Switches: Transmitter: 515-0173-00 (Sw. 14 & "
			"15); Receiver: 515-0174-00 (Sw. 14 & 15)'; the board table names the Dual OPTO boards '4-Ball Trough over Up-Kicker'. "
			"Whitestar's switch_r hands the CPU ~core_getSwCol and the driver's invSw is zero, so public 1 is the CPU's closed-contact "
			"reading. The Dual OPTO theory page states the construction: with light on the receiver its output transistor is off "
			"and acts as an OPEN SWITCH; when the beam is blocked it conducts and acts as a CLOSED SWITCH, so the contact rests open. "
			f"The alignment test names LED1 the lower and LED2 the upper beam, the one a 'double-stacked' ball breaks; this is "
			f"{'LED1, the beam the ball waiting at the up-kicker blocks' if address == 14 else 'LED2, the stacking beam'}."
		)
	if address == 15:
		notes += (
			" In the stacking-opto harness run, with four balls on 11-14, raising 15 to 1 in attract mode made the ROM fire the "
			"trough up-kicker 1 six times about 0.8 s apart, starting about 1.1 s after the rise, and then the auto launch 2 once; "
			"lowering it drew nothing, and a second rise drew the same sequence. The ROM treats a blocked upper beam as a jam to clear."
		)
	if address == 16:
		notes += (
			" The part cell 180-5157-00 names a switch type the manual's assembly pages do not show, so the switch type is left "
			"unknown. The Diagnostic Aids page uses '#16 Shooter Lane & #2 Auto Launch' as its example of a coil the CPU activates "
			"about ten times while its switch stays closed."
		)
	if address == 10:
		notes += " The retained table contains no object for it, so it carries no placement."
	if address == 25:
		notes += " The manual's assembly pages carry no spinner switch drawing, so the switch type is left unknown."
	if address in (28, 31):
		notes += (
			f" The {'Right' if address == 28 else 'Left'} Ramps page (drawing labelled SW. {address}) lists the Micro Switch (1-5/8\" Actuator) "
			"180-5010-01."
		)
	if address == 45:
		notes += " The Right Ramps page (drawing labelled SW. 45) lists the Ramp Gate Switch (Right) 500-6593-00 with Micro Switch 180-5190-28."
	if address in (32, 34):
		notes += (
			f" The Ball Eject ({'Right' if address == 32 else 'Left'}) page, drawing labelled SW. {address}, carries an AP-B Switch "
			"Assembly with Micro Switch 180-5186-00 and the 24-940 eject coil."
		)
	if address == 33:
		notes += (
			" The Elvis figure page (assembly reference 500-6796-00) labels SW. 33 on its switch bracket: a Micro Switch (Short "
			"Actuator, Bend) 180-5189-00. The ELVIS test page: 'If the BOX is solid, Switch 33 is \"Closed\" (Elvis should be in the "
			"Home Position or closest to the Upper Playfield).' The contact closes at home and rests open elsewhere; set it to 1 "
			"before the controller starts. In the ELVIS-test harness run the box was drawn filled on entry, empty after RUN, filled "
			"after a second RUN and empty after PULSE. LibPinMAME's elvis.c writes 33 itself on every non-zero stepper phase write "
			"(1 at its position zero, 0 elsewhere), so under LibPinMAME the host's own write is overwritten as soon as the ROM steps "
			"the motor; VPinMAME builds compile that line out and leave 33 to the table."
		)
		refs += (SIM_SOURCE,)
	if address in (36, 37, 38, 39):
		notes += (
			" One of four 1\" Sq. S/U Targets (Side-Lugs, No Brkt) 515-7381-00 on the Elvis figure's base (drawing labels SW. 36-39); "
			"they travel with the figure."
		)
	if address == 48:
		notes += " The location drawing puts it at the hotel lock, where the hotel lock release coil 7 holds a ball."
	if address in (49, 50, 51):
		notes += (
			" The Bumper Top, Bot. & Sw. page lists the Bumper Stack (Blade) Switch Assy. 180-5015-05 with 'ASSEMBLY NOTE: This "
			"Switch is -05 because it is mounted in reverse.'"
		)
	if address in (52, 53, 63):
		notes += (
			" The Hotel Door Coil, Frame, Stand-Up pages label SW. 63, SW. 52 and SW. 53: the door's Micro Switch (Roller Actuator, "
			"Lite-Force) 180-5119-02 and two 1\" Sq. Stand-Up Targets 515-5162-08 behind it."
		)
	if address in (2, 3, 7):
		notes += (
			" The cabinet wiring diagram labels it "
			f"'{ {2: '4th Coin Slot European Use', 3: '6th Coin Slot Future Use', 7: '5th Coin Slot Future Use'}[address] }', "
			"and all coin door switches 'Normally Open (N.O.)'."
		)
	if address in (1, 8):
		notes += (
			" UK only: the grid prints the name on a grey panel, and the cabinet wiring diagram's boxed note reads 'UK ONLY: 2 Extra "
			"Cabinet Buttons for the Post Save™ Feature are used. The Left Button operates the Left Outlane Ball Deflector. The Right "
			"Button operates the Right Outlane Ball Deflector. Both buttons pushed together operate the Center Up/Down Post. Both "
			f"buttons are located under the Flipper Buttons.' Its UK drawing puts the {'LEFT' if address == 1 else 'RIGHT'} BUTTON, "
			f"N.O., on {'WHT-BRN (CN7 pin 9)' if address == 1 else 'WHT-GRY (CN7 pin 1)'} and GRN-BRN (CN5 pin 1). PinMAME publishes "
			"none of the UK post-save coils (see the auxiliary outputs), so a recreation has no deflector to drive from this button."
		)
	if address in (54, 55, 56):
		notes += (
			f" The cabinet wiring diagram draws {'START BUTTON SW. 54' if address == 54 else 'TOURNIE BUTTON SW. 55' if address == 55 else 'PLUMB BOB TILT SW. 56'} "
			"N.O. on GRN-VIO (CN5 pin 8)."
		)
	if address == 55:
		notes += (
			" The grid's black panel beside it reads 'Optional Tournament Kit Required'. Elvis has no slam tilt switch: PinMAME's "
			"start/tilt/slam triple for this driver names 55 swSlamTilt and sega.vbs calls it swSlamTilt, two names for the same input."
		)
		refs += (SIM_SOURCE, VPM_LIBRARY_SOURCE)
	if address == 56:
		notes += " The grid's part note: 'The Switch is comprised of a Hanger Bracket (535-5319-00) and Contact Wire (535-7563-01) located in the Cabinet.'"
	if address in SWITCH_SCRIPT:
		notes += f" Retained table script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
		if address in (4, 5, 6, 54, 56):
			refs += (VPM_LIBRARY_SOURCE,)
	if address in GAMEPLAY_RESPONSE:
		notes += f" In the harness runs, {GAMEPLAY_RESPONSE[address]}."
	elif address in GAMEPLAY_QUIET:
		notes += " The gameplay run actuated it once in a game and the ROM drove no output during that step, which says nothing against its fitment."
	extra: dict[str, Any] = {"aliases": aliases, "normally_closed": address == 64, "pulse": pulse, "wiring": _switch_wiring(address)}
	if roles:
		extra["roles"] = list(roles)
	if address in (11, 12, 13, 14, 33, 64):
		extra["initial_active"] = True
	if any(role.startswith("cabinet.") for role in roles):
		physical["location"] = "coin door" if mounting == "Coin Door" else "cabinet"
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, availability, refs, physical=physical, **extra)


# address -> (label, printed function, wire, connector, location, part, roles, normally_closed)
DEDICATED = {
	-3: ("Coin Door Memory Protect", "Memory Protect Switch", "BLK-RED", "CN6-P12", "coin door", None, ("cabinet.memory-protect",), False),
	-2: ("Volume / Service Left (Red)", "#6 VOLUME (RED BUTTON) (In Test: LEFT)", "GRY-BLU", "CN6-P8", "coin door", "180-5192-02", ("service.left",), False),
	-1: ("Service Credit / Service Right (Green)", "#7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT)", "GRY-VIO", "CN6-P9", "coin door", "180-5192-04", ("service.right",), False),
	0: ("Begin Test / Service Enter (Black)", "#8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER)", "GRY-BLK", "CN6-P10", "coin door", "180-5192-00", ("service.enter",), False),
	81: ("Right Flipper End-of-Stroke", "#4 RIGHT FLIPPER E.O.S. (End-of-Stroke)", "GRY-YEL", "CN6-P6", "playfield", "180-5149-00", ("internal.flipper.lower.right.eos",), True),
	82: ("Right Flipper Button", "#3 RIGHT FLIPPER BUTTON", "GRY-ORG", "CN6-P4", "cabinet", "180-5164-00", ("flipper.lower.right.button",), False),
	83: ("Left Flipper End-of-Stroke", "#2 LEFT FLIPPER E.O.S (End-of-Stroke)", "GRY-RED", "CN6-P3", "playfield", "180-5149-00", ("internal.flipper.lower.left.eos",), True),
	84: ("Left Flipper Button", "#1 LEFT FLIPPER BUTTON", "GRY-BRN", "CN6-P2", "cabinet", "180-5160-00", ("flipper.lower.left.button", "flipper.upper.left.button"), False),
	88: ("Upper Right Flipper Button", "#5 UPPER RT. FLIPPER BUTTON", "GRY-GRN", "CN6-P7", "cabinet", "180-5164-00", ("flipper.upper.right.button",), False),
}
DEDICATED_INPUT = {-2: "DS-6", -1: "DS-7", 0: "DS-8", 81: "DS-4", 82: "DS-3", 83: "DS-2", 84: "DS-1", 88: "DS-5"}
DEDICATED_TEST_LABEL = {
	81: "right flipper end-of-stroke (public 81) held in the Dedicated Switch Test",
	82: "right flipper button (public 82) held in the Dedicated Switch Test",
	83: "left flipper end-of-stroke (public 83) held in the Dedicated Switch Test",
	84: "left flipper button (public 84) held in the Dedicated Switch Test",
	88: "dedicated input 88 (DS-5) (public 88) held in the Dedicated Switch Test",
}


def dedicated_id(address: int) -> str:
	name = f"n{-address}" if address < 0 else str(address)
	return f"switch.{name}-{slug(DEDICATED[address][0])}"


def _dedicated_test(address: int) -> str:
	return _service_line(_reading("elvis-dedicated-switch-test", DEDICATED_TEST_LABEL[address])).replace(" / PRESS START TO EXIT TEST", "")


def _dedicated(address: int) -> dict[str, Any]:
	label, printed, wire, connector, location, part, roles, normally_closed = DEDICATED[address]
	identifier = dedicated_id(address)
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
	if address in DEDICATED_INPUT:
		aliases.append({"namespace": "manual.address", "value": DEDICATED_INPUT[address]})
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": "leaf" if address in (81, 83) else "button" if address != -3 else "microswitch", "location": location}
	if part:
		physical["part_number"] = part
	if address == -3:
		notes = (
			"The cabinet/coin door wiring diagram (PDF page 125) draws the Memory Protect Switch, N.O., from CPU board CN6 pin 12 "
			"(BLK-RED) to the BLK ground. se.c's ram_w refuses writes to the protected RAM while public -3 is 1, and sega.vbs names the "
			"address swMemoryProtect; a closed coin door is public -3 at 1 and an open door 0. The Diagnostic Aids page: 'Opening "
			"the Coin Door will initiate a Factory Restore (Reset), by opening the Memory Protect Switch.'"
		)
		refs += (VPM_LIBRARY_SOURCE,)
		extra: dict[str, Any] = {"initial_active": True, "wiring": {"board": "Whitestar CPU/Sound board memory-protect input", "drive_wire": wire, "drive_connection": connector}}
	else:
		notes = (
			f"Printed dedicated switch {DEDICATED_INPUT[address]} ({printed}), wired {wire} to {connector} on IC U206's inputs and returned "
			"to ground (BLK, CN6-P1/-P11). se.c's dedswitch_r swaps PinMAME's flipper column into U206's order and returns the complement, "
			"so public 1 is a closed contact."
		)
		extra = {"wiring": {"board": "Whitestar CPU/Sound board dedicated-switch input", "drive_wire": wire, "drive_connection": connector, "return_wire": "BLK", "return_connection": "CN6-P1/-P11", "return_component": "U206"}}
	if address in (-2, -1, 0):
		notes += " The cabinet wiring diagram draws it among the PORTALS™ SERVICE BUTTONS on the coin door; the harness runs drove the ROM's service menus with it."
		refs += (RUNTIME_SOURCE,)
	if address in (81, 83):
		side = "right" if address == 81 else "left"
		canonical = 46 if address == 81 else 48
		notes += (
			f" The grid prints its location 'Below Playfield' and its part '180-5149-00 on Flipper'; the 4-Flipper Circuit Wiring "
			f"Diagram (PDF page 123) draws it as the {side.upper()} E.O.S. ON ASSY., N.C., and the Flipper ({side.capitalize()}) page "
			"lists the Power (EOS / End-of-Stroke) Switch 180-5149-00. Its Technical Overview: 'The E.O.S. Switch is a normally "
			"closed switch which opens approximately 1/16\" when the flipper is energized', and the CPU applies another 40 ms pulse "
			"when it sees the switch close during a hold. normally_closed is that construction. PinMAME, not a host, writes this "
			"address: elvisGameData declares FLIP_SOL(FLIP_L), and core.h defines FLIP_SOL(x) to include FLIP_EOS(x), so core.c's "
			f"flipMask holds the lower {side} EOS bit and core_updateSw rewrites it on every update from the lower {side} flipper "
			f"solenoid ({canonical}): 1 once that solenoid has been on for CORE_FLIPSTROKETIME (two VBLANKs), 0 otherwise. A host "
			"write is overwritten, so a recreation leaves it alone and drives only the buttons. The ROM's Dedicated Switch Test, "
			f"which reports a held contact, printed \"{_dedicated_test(address)}\" while the host held it, the host's write never "
			"reaching the ROM. That run watched the address, and every snapshot read 0, including while the host held it, as core.c's "
			"rewrite predicts with the flipper solenoid off; no gameplay run timed the end-of-stroke against a flip. The retained "
			"script never writes it, which is right; sega.vbs "
			f"names it {'swURFlip' if address == 81 else 'swULFlip'}."
		)
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE)
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE,)
	elif address == 82:
		notes += (
			" The grid's part cell reads '180-5164-00 Doubled': the right cabinet button is double-stacked. The 4-Flipper Circuit "
			"Wiring Diagram: 'Pressing half-way down operates the Lower Right Flipper; pressing full down operates both the Lower "
			"Flipper & Upper Right Flipper(if used) simultaneously.' This contact is the half-way one, DS-3. It is in the flipper "
			"column core_updateSw copies into the lower-flipper outputs; sega.vbs writes it from the right flipper key (swLRFlip = 82). "
			f"The ROM's Dedicated Switch Test printed \"{_dedicated_test(address)}\" while it was held. In the gameplay run holding it "
			"for 1.5 s made the ROM pulse 45 and 46 and not the upper right flipper 14."
		)
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE)
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	elif address == 84:
		notes += (
			" The 4-Flipper Circuit Wiring Diagram: 'The Outside LEFT FLIPPER BUTTON located on the Cabinet operates both the Left "
			"Flipper & Upper Left Flipper (if used).' sega.vbs writes it from the left flipper key (swLLFlip = 84). The ROM's "
			f"Dedicated Switch Test printed \"{_dedicated_test(address)}\" while it was held. In the gameplay run holding it for 1.5 s "
			"made the ROM pulse the lower left flipper (47 and 48) and the upper left flipper 13 together."
		)
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE)
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	elif address == 88:
		notes += (
			" The grid prints DS-5 '#5 UPPER RT. FLIPPER BUTTON' with the part cell 'Same as DS-3 above.', the second contact of "
			"the doubled right cabinet button (180-5164-00 Doubled), closed by a full press. The 4-Flipper Circuit Wiring Diagram "
			"draws 'UPPER RIGHT FLIPPER IN CABINET DEDICATED SWITCH DS-5', N.O., and the cabinet wiring diagram 'D.S. 5 UPPER RIGHT "
			"FLIPPER BUTTON' on GRY-GRN, CN6 pin 7. se.c's dedswitch_r reads it as DED #5 from flipper-column bit 0x80 (its own "
			"comment: 'Not Used (Upper Flipper on some games!)'). elvisGameData declares FLIP_SW(FLIP_L) only, so core.c's flipMask "
			"omits that bit and a host write reaches the ROM unchanged. In the gameplay run, holding it for 1.5 s made the ROM drive "
			"the upper right flipper 14, alone and with 82 held, and releasing it dropped 14; 82 alone never drove 14. The ROM's "
			f"Dedicated Switch Test printed its generic label \"{_dedicated_test(address)}\" while it was held, so the test's label "
			"table says nothing about the fitment its game code acts on. Drive 82 and 88 together from a full press of the right "
			"flipper button, and 82 alone from a half press. The retained table never writes 88."
		)
		refs += (RUNTIME_SOURCE, VPX_SCRIPT_SOURCE)
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, "used", refs, aliases=aliases, normally_closed=normally_closed,
		pulse=False, roles=list(roles), physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items = [_dedicated(address) for address in (-3, -2, -1, 0)]
	items.extend(_matrix_switch(address) for address in range(1, 65))
	items.extend(_dedicated(address) for address in (81, 82, 83, 84))
	for address in (85, 86, 87):
		items.append(_device(
			f"switch.{address}-flipper-column-hole", f"Unused Flipper-Column Input {address}", "switch", SWITCH_GROUP, address, "unused",
			(CORE_SOURCE, CONTROLLER_SOURCE), aliases=[{"namespace": "pinmame.switch", "value": str(address)}], normally_closed=False, pulse=False,
			physical={"notes": "dedswitch_r reads only the flipper column's four low bits and its top bit (public 81-84 and 88); this bit reaches no input of U206."},
			spatial=not_applicable("unused", CORE_SOURCE),
		))
	items.append(_dedicated(88))
	for number in range(1, 9):
		used = number <= 5
		items.append(_device(
			f"switch.dip-{number}", f"SW300 Country Setting Position {number}" if used else f"Unused SW300 Position {number}", "dip_switch", DIP_GROUP, number,
			"used" if used else "unused", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": str(number)}, {"namespace": "manual.address", "value": f"SW300-{number}"}],
			physical={"switch_type": "dip", "location": "Whitestar CPU/Sound board SW300 (right of CN6, top middle)", "notes": (
				f"Position {number} of the eight-position CPU DIP switch SW300 (KSD08H). se.c's dip_r returns the complement of PinMAME DIP "
				"bank 0. The manual's CPU Country Setting charts (DR. 3) set positions 1-5 for twenty-two countries (USA all off; "
				"Croatia, Japan, New Zealand, Portugal, South Africa and Spain use position 5) and never turn 6-8 on." if used else
				f"Position {number} of the eight-position CPU DIP switch SW300. No printed country setting turns positions 6-8 on; PinMAME "
				"publishes the full eight-address bank regardless.")},
			spatial=not_applicable("dip_switch", MANUAL_SOURCE),
		))
	return items


# --- Solenoid data -------------------------------------------------------------------------------------
# Q number -> (label, printed name, kind, availability, coil/bulb cell, power wire, power connection, voltage, control wire, control connection)
YV = ("YEL-VIO", "J10-P4/5", 50)
BR = ("BRN", "J7-P1", 20)
OR = ("ORG", "J6-P10", 20)
ST = ("GRY-RED", "J16-P3", 12)
Q_OUTPUTS: dict[int, tuple[str, str, str, str, str, str, str, int | None, str, str]] = {
	1: ("Trough Up-Kicker", "TROUGH UP-KICKER", "coil", "used", "26-1200 / 090-5044-00B", *YV, "BRN-BLK", "J8-P1"),
	2: ("Auto Launch", "AUTO LAUNCH", "coil", "used", "23-800 / 090-5001-00B", *YV, "BRN-RED", "J8-P3"),
	3: ("Elvis 5-Bank Reset", "ELVIS 5-BANK RESET", "coil", "used", "24-940 / 090-5036-00B", *YV, "BRN-ORG", "J8-P4"),
	4: ("Shaker Motor (Optional)", "(OPT) SHAKER MOTOR", "motor", "optional", "Motor Only / 041-5029-01", "RED-WHT", "J17-P7", None, "BRN-YEL", "J8-P5"),
	5: ("Magnet", "MAGNET", "magnet", "used", "22-650 / 090-5042-00", "VIO-YEL", "J10-P3", 50, "BRN-GRN", "J8-P6"),
	6: ("Center Eject", "CENTER EJECT", "coil", "used", "24-940 / 090-5036-00B", *YV, "BRN-BLU", "J8-P7"),
	7: ("Hotel Lock Release", "HOTEL LOCK RELEASE", "coil", "used", "23-800 / 090-5001-00B", *YV, "BRN-VIO", "J8-P8"),
	8: ("Control Gate", "CONTROL GATE", "coil", "used", "32-1800 / 090-5031-00B", *YV, "BRN-GRY", "J8-P9"),
	9: ("Left Bumper", "LEFT BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-BRN", "J9-P1"),
	10: ("Right Bumper", "RIGHT BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-RED", "J9-P2"),
	11: ("Bottom Bumper", "BOTTOM BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-ORG", "J9-P4"),
	12: ("Top Eject", "TOP EJECT", "coil", "used", "24-940 / 090-5036-00B", *YV, "BLU-YEL", "J9-P5"),
	13: ("Upper Left Flipper", "UPPER LEFT FLIPPER", "coil", "used", "23-900 / 090-5020-30", "RED-YEL, GRY-YEL after its 3A fuse", "J10-P1/2", 50, "BLU-GRN", "J9-P6"),
	14: ("Upper Right Flipper", "UPPER RIGHT FLIPPER", "coil", "used", "23-900 / 090-5020-30", "RED-YEL, BLU-YEL after its 3A fuse", "J10-P1/2", 50, "BLU-BLK", "J9-P7"),
	15: ("Left Flipper", "LEFT FLIPPER (50v RED/YEL)", "coil", "used", "22-900 / 090-5020-20T", "RED-YEL, GRY-YEL after its 3A fuse", "J10-P1/2", 50, "ORG-GRY", "J9-P8"),
	16: ("Right Flipper", "RIGHT FLIPPER (50v RED/YEL)", "coil", "used", "22-900 / 090-5020-20T", "RED-YEL, BLU-YEL after its 3A fuse", "J10-P1/2", 50, "ORG-VIO", "J9-P9"),
	17: ("Left Slingshot", "LEFT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "VIO-BRN", "J7-P2"),
	18: ("Right Slingshot", "RIGHT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "VIO-RED", "J7-P3"),
	19: ("Hotel Door", "HOTEL DOOR", "coil", "used", "27-1500 / 090-5004-00B", *BR, "VIO-ORG", "J7-P4"),
	20: ("Back Panel Flashers (X2)", "FLASH:  BACK PANEL X2", "flasher", "used", "#89 Bulb / 165-5000-89-HF", *OR, "VIO-YEL", "J7-P6"),
	21: ("Back Panel TCB Flasher", "FLASH:  BACKPANEL TCB", "flasher", "used", "#89 Bulb / 165-5000-89-HF", *OR, "VIO-GRN", "J7-P7"),
	22: ("Spinner Flasher", "FLASH:  SPINNER", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "VIO-BLU", "J7-P8"),
	23: ("Upper Right Flipper Flashers (X2)", "FLASH:  UPR RT FLIPPER X2", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "VIO-BLK", "J7-P9"),
	24: ("Optional Coil (Q24 Option)", "OPTIONAL COIL", "coil", "optional", "Opt. 5v", "RED", "J16-P7", 5, "VIO-GRY", "J7-P10"),
	25: ("Stepper Phase 1", "STEPPER #1", "motor", "used", "Stepper Motor Only / 041-5069-00", *ST, "RED", "J6-P1"),
	26: ("Stepper Phase 2", "STEPPER #2", "motor", "used", "Stepper Motor Only / 041-5069-00", *ST, "GRN", "J6-P2"),
	27: ("Stepper Phase 3", "STEPPER #3", "motor", "used", "Stepper Motor Only / 041-5069-00", *ST, "BLK", "J6-P3"),
	28: ("Stepper Phase 4", "STEPPER #4", "motor", "used", "Stepper Motor Only / 041-5069-00", *ST, "BLU", "J6-P4"),
	29: ("Elvis Legs", "ELVIS LEGS", "coil", "used", "29-1400 / 090-5072-03", *BR, "BLK-GRN", "J6-P5"),
	30: ("Elvis Arms", "ELVIS ARMS", "coil", "used", "29-1400 / 090-5072-03", *BR, "BLK-BLU", "J6-P6"),
	31: ("Elvis Spot Light Flasher", "FLASH:  ELVIS SPOT LIGHT", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-VIO", "J6-P7"),
	32: ("Slingshot Flashers (X2)", "FLASH:  SLINGS X2", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-GRY", "J6-P8"),
}
PUBLIC_BINDING = {15: 48, 16: 46}
# What the retained table does with each callback (embedded script line numbers).
SOLENOID_SCRIPT = {
	1: "SolCallBack(1) = \"SolTrough\" (line 303) kicks the trough ball stack out of BallRelease and pulses the stacking opto 15 (lines 313-316)",
	2: "SolCallBack(2) = \"Auto_Plunger\" (line 304) fires the impulse plunger plungerIM (lines 320-322); the table also has a manual Plunger object",
	3: "SolCallBack(3) = \"dtBankL.SolDropUp\" (line 305) raises the five drop targets sw17-sw21",
	5: "no callback; the cvpmMagnet mMag (InitMagnet Magnet, 60; .Solenoid = 5; lines 93-96) grabs balls around the trigger Magnet while 5 is on",
	6: "SolCallBack(6) = \"bsJail.SolOut\" (line 306) kicks the saucer sw34",
	7: "SolCallBack(7) = \"bsLock.SolOut\" (line 307) kicks the ball stack bsLock out of the kicker HLock (lines 109-112)",
	8: "SolCallBack(8) = \"CGate.Open =\" (line 308) holds the gate CGate open while 8 is on",
	9: "no callback; Bumper1 is a VPX bumper that fires itself",
	10: "no callback; Bumper2 is a VPX bumper that fires itself",
	11: "no callback; Bumper3 is a VPX bumper that fires itself",
	12: "SolCallBack(12) = \"bsUpper.SolOut\" (line 309) kicks the saucer sw32",
	13: "no callback reads 13; SolLFlipper, the callback of the lower left flipper (48), rotates LeftFlipper1 together with LeftFlipper (lines 208 and 210-218)",
	14: "no callback reads 14; SolRFlipper, the callback of the lower right flipper (46), rotates RightFlipper1 together with RightFlipper (lines 207 and 222-230), so the table's upper right flipper follows the half press",
	15: "SolCallback(sLLFlipper) = \"SolLFlipper\" (line 208)",
	16: "SolCallback(sLRFlipper) = \"SolRFlipper\" (line 207)",
	17: "no callback; LeftSlingShot is a VPX slingshot wall that fires itself",
	18: "no callback; RightSlingShot is a VPX slingshot wall that fires itself",
	19: "SolCallBack(19) = \"SolHotelDoor\" (line 310) swings the door flipper fDoor open and drops doorwall while 19 is on (lines 326-332)",
	20: "SolCallBack(20) = \"SetLamp 100,\" (line 339) drives the Flasher sprites f20 and f20a-c and the Flupper domes Flasherbase6 and Flasherbase4 (lines 656-661)",
	21: "SolCallback(21) = \"SetLamp 101,\" (line 340) drives the Flasher sprite f21 and the Flupper dome Flasherbase5 (lines 662-663)",
	22: "SolCallBack(22) = \"SetLamp 102,\" (line 341) drives the Flupper dome Flasherbase3 and its glow Light Flasherlight3 (line 664)",
	23: "SolCallBack(23) = \"SetLamp 103,\" (line 342) fades the Lights f23a and f23 (lines 665-666)",
	24: "SolCallBack(24) plays a knocker sound (line 311); the factory default for this output is a coin meter",
	25: "the cvpmMech mElvis moves the figure while 25 is on (Sol1 = 25, lines 147-154), and UpdateElvis moves the stand primitive pStand (lines 190-196)",
	26: "nothing reads it: mElvis is a one-solenoid mech on 25",
	27: "nothing reads it: mElvis is a one-solenoid mech on 25",
	28: "nothing reads it: mElvis is a one-solenoid mech on 25",
	29: "SolCallBack(29) = \"ElvisLegs\" (line 350) rotates the legs flipper fLegs (lines 353-358)",
	30: "SolCallBack(30) = \"ElvisArms\" (line 351) rotates the arms flipper fArms (lines 362-366)",
	31: "SolCallBack(31) = \"SetLamp 105,\" (line 344) drives the Flasher sprites f31a and f31 (lines 669-670)",
	32: "SolCallBack(32) = \"SetLamp 104,\" (line 343) drives the Flupper domes Flasherbase1 and Flasherbase2 with their glow Lights (lines 667-668)",
}
# What the harness runs showed for each output (evidence step labels).
SOLENOID_RUNTIME = {
	1: (
		"the ROM fired it about 1.1 s after Start and twice more about 1.25 s apart before the scenario moved the served ball to 16; "
		"in the stacking-opto run a rise of 15 drew six kicks about 0.8 s apart; once the scenario released the ball it had held on "
		"the hotel post 48, it fired about every 1.25 s for the rest of the run, no ball reaching 16"
	),
	2: (
		"it did not fire while the served ball rested on 16 for 6 s; it fired 0.17 s after the right flipper button 82 was pressed "
		"while no ball was on 16, in the ball-search pass, and after the six up-kicks the stacking opto drew"
	),
	3: "it fired at boot, at Start, and three times 0.33, 0.74 and 1.14 s after the fifth drop target went down; also in the ball-search pass",
	4: (
		"the ROM ran it with nearly every scoring switch from the bumpers onward, whether or not the kit is fitted: the bumpers, "
		"orbits, ramps, KING targets, scarf, top and return lanes and hotel standups"
	),
	5: "it fired only in the ball-search pass at the end of the gameplay run; no run held a ball where the magnet acts",
	6: "a ball resting on the centre saucer 34 drew it 4.3 s after arrival and twice more about 0.7 s apart; also in the ball-search pass",
	7: "a ball held on the hotel post 48 for 6 s drew no release; it fired only in the ball-search pass",
	8: "only the Single Coil Test fired it; no gameplay step did",
	9: "it answered the left bumper switch 49 and fired in the ball-search pass",
	10: "it answered the right bumper switch 50 and fired in the ball-search pass",
	11: "it answered the bottom bumper switch 51 and fired in the ball-search pass",
	12: "a ball resting on the top saucer 32 drew one kick 5.7 s after it arrived; also in the ball-search pass",
	13: "holding the left flipper button 84 drove it together with the lower left flipper (47 and 48)",
	14: "holding the full-press contact 88 drove it, with or without 82; holding 82 alone did not",
	17: "it answered the left slingshot switch 59 and fired in the ball-search pass",
	18: "it answered the right slingshot switch 62 and fired in the ball-search pass",
	19: (
		"the ROM held it on for long stretches: it switched it on when the top hotel standup 52 closed, while a ball rested in either "
		"saucer or on the hotel post 48, and in the hound-dog probe 0.13 s after the hotel door switch 63 rose; with the hound dog "
		"64 held at 1 it switched it off 2.0-2.5 s later, and each fall of 64 to 0 switched it on again about 65 ms later; it also "
		"fired in the ball-search pass"
	),
	20: "it flashed with each coin, at Start, with the bumpers, the ramps, the hotel standups and door, and while a ball rested in a saucer or on the hotel post",
	21: "it flashed with each coin, at Start, with the TC(B) target 24, the ramps, the top hotel standup 52 and a ball resting in a saucer or on the hotel post",
	22: "it flashed with each coin, at Start, with the spinner 25 and the ramps, when the fifth drop target went down and repeatedly while the bank stayed down, and while a ball rested in a saucer or on the hotel post",
	23: "it flashed with each coin, at Start, with the ramps and while a ball rested in a saucer or on the hotel post",
	24: "each coin pulsed it four times, the coin-meter count of its factory default",
	25: "the ROM drove the four phases at boot, while the figure danced in play, and on RUN and PULSE in the ELVIS test",
	26: "the ROM drove the four phases at boot, while the figure danced in play, and on RUN and PULSE in the ELVIS test",
	27: "the ROM drove the four phases at boot, while the figure danced in play, and on RUN and PULSE in the ELVIS test",
	28: "the ROM drove the four phases at boot, while the figure danced in play, and on RUN and PULSE in the ELVIS test",
	29: "LEGS in the ELVIS test energized it; in play it pulsed with many scoring switches while the figure danced",
	30: "ARMS in the ELVIS test energized it; in play it pulsed with many scoring switches while the figure danced",
	31: "it flashed with each coin, at Start, with the TC(B) target 24, the ramps and a ball resting on the hotel post",
	32: "it flashed with each coin, at Start, with both slingshots, the ramps, the fifth drop target and while a ball rested in a saucer or on the hotel post",
}
FLASHER_LOCATIONS = {
	20: "back panel face, its lower left and upper right corners",
	21: "back panel face, left of the HEART BREAK HOTEL insert strip",
	22: "playfield left edge, about halfway down (spinner)",
	23: "two along the playfield's right edge, by the upper right flipper",
	31: "above the playfield, drawn beside the Elvis figure's stepper callouts",
	32: "one above each slingshot",
}
FLASHER_QUANTITY = {20: 2, 21: 1, 22: 1, 23: 2, 32: 2}
FLASHER_DRAWING = {
	20: "the coil and flash lamp location drawing (DR. 7) draws 20 twice in grey (not on playfield) boxes on the back panel face, at its lower left and upper right corners, labelled Yellow (mini-mars colour)",
	21: "DR. 7 draws 21 once in a grey box on the back panel face, left of the vertical HEART BREAK HOTEL insert strip, labelled Clear",
	22: "DR. 7 draws 22 once in a white (above playfield) box at the plan's left edge, about halfway down, labelled Red",
	23: "DR. 7 draws 23 twice in white boxes along the plan's right edge, beside 5 and beside 14",
	31: "DR. 7 draws 31 once in a white box right of the stepper callout 28 and below 11",
	32: "DR. 7 draws 32 twice in white boxes labelled Red, one above each slingshot coil callout (17, 18)",
}
DRIVER_BOARD_LOAD = {
	20: "#20 Flash: Back Panel X2 (bulb glyph '#89 Clear Bulb X2')",
	21: "#21 Flash: Back Panel TCB (bulb glyph '#89 Clear Bulb X1')",
	22: "#22 Flash: Spinner (bulb glyph '#906 Clear Bulb X1')",
	23: "#23 Flash:Upper Right Flipper X2 (bulb glyph '#906 Clear Bulb X2')",
	31: "#31 Flash: Elvis Spot Lights X2 (bulb glyph '#906 Clear Bulb X1')",
	32: "#32 Flash: Slingshots X2 (bulb glyph '#906 Clear Bulb X2')",
}


def q_output_id(number: int) -> str:
	return f"device.q{number}-{slug(Q_OUTPUTS[number][0])}"


def _q_wiring(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	wiring: dict[str, Any] = {
		"board": "Whitestar I/O Power Driver board 520-5137-01", "driver_transistor": f"Q{number}", "control_wire": control_wire,
		"control_connection": control_connection, "power_wire": power_wire, "power_connection": power_connection,
	}
	if voltage is not None:
		wiring["nominal_voltage_v"] = voltage
		wiring["voltage_type"] = "dc"
	return wiring


def _coil_test(number: int) -> str:
	return _service_line(_reading("elvis-single-coil-test", f"Black ENTER button (public 0) pressed on +: coil step {number} selected"))


def _q_output(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	address = PUBLIC_BINDING.get(number, number)
	identifier = q_output_id(number)
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE)
	physical: dict[str, Any] = {}
	coil_part = part.split(" / ")[-1].split(" ")[0]
	if re.fullmatch(r"\d{3}-\d{4}-\d{2}[A-Z]?(-HF)?", coil_part):
		physical["part_number"] = coil_part
	notes = (
		f'Coils Detailed Chart Table (DR. 6) row #{number} "{printed}": drive transistor Q{number}, control {control_wire} '
		f'{control_connection}, cell "{part}". The 5.00 ROM\'s Single Coil Test names it "{_coil_test(number)}" (power wire, then '
		"control wire)."
	)
	if number in FLASHER_LOCATIONS:
		physical["location"] = FLASHER_LOCATIONS[number]
	if number in FLASHER_QUANTITY:
		physical["quantity"] = FLASHER_QUANTITY[number]
	if kind == "flasher":
		notes += (
			f" The driver board diagram prints the load {DRIVER_BOARD_LOAD[number]}; {FLASHER_DRAWING[number]}. The chart's note: 'In "
			"Test Flash Lamps Menu (\"Flash\" Icon), Flashers tested are all Flash Lamps located between Q1-Q32 (This Game: Q20-Q23, "
			"Q31-Q32)'. se.c gives the Elvis root's sets the #89 20v DC bulb model on 20-23 and 31-32; only 20 and 21 carry #89 "
			"bulbs, so the model is an emulator rendering choice, not wiring."
		)
		refs += (SIM_SOURCE,)
	if number in (20, 21):
		notes += (
			" The Back Panel page lists three 2-Lug Stand-Up Short Sockets with #89 Bulb (Clear) Heavy Filament 165-5000-89-HF, "
			"Q20's two and Q21's one. The retained table models them with Flupper domes on the back panel's plane behind the "
			"playfield's rear edge and with backbox-space Flasher sprites, so the flasher is not placed."
		)
	if number == 31:
		notes += (
			" That load name and bulb glyph disagree on the count, and the chart prints the bulb type only, so the record states no "
			"quantity. The retained table "
			"draws it only with the Flasher sprites f31 and f31a, render helpers that are not bulb sockets, so it is not placed."
		)
	if number == 23:
		notes += (
			" The retained table's f23 and f23a are bulb-mode Lights that show no bulb mesh, and no primitive models a socket under "
			"either, so they sit on no bulb and the flasher is not placed."
		)
	if number == 2:
		notes += (
			" The Ball Shooter (Plunger) Autoplunger Arm page lists the 23-800 coil 090-5001-00B. The Diagnostic Aids page's Operator "
			"Alert example is '#2 AUTO LAUNCH COIL MALFUNCTION', and it states that the CPU activates such a coil about ten times while "
			"its switch (16) stays closed."
		)
	if number == 1:
		notes += " The 4-Ball Trough page lists the 26-1200 coil 090-5044-00B, the Plunger Assembly 515-5941-01 and the two Dual OPTO boards."
	if number == 3:
		notes += " The 5-Bank Drop Target page lists the 24-940 coil 090-5036-00B and plunger 530-5410-01."
	if number == 4:
		physical["location"] = "cabinet (shaker motor, when fitted)"
		notes += (
			" The row is printed on a grey band: optional equipment. The power cell prints '16v AC' over '12v DC'; the record keeps the "
			"wire and connector and states no single voltage. The driver board diagram: 'order Shaker Motor Kit 502-5027-00-84', "
			"'OPTIONAL +12V DC SHAKER MOTOR 041-5029-01 Located in Cabinet', driven through the SHAKER MOTOR BOARD 520-5065-00, "
			"Located in Cabinet OPTIONAL. DR. 7 draws no callout for 4. The retained script registers no callback."
		)
	if number == 5:
		notes += (
			" The Magnet Coil, Bracket and Ball Lock page lists the Magnet Coil, 22-650 (6\" Leads + Conn.) 500-6808-00, whose diode "
			"(1N4004) is in its connector; the driver board diagram feeds it from VIO-YEL High Power 50v DC on J10-P3."
		)
	if number in (6, 12):
		notes += (
			f" The Ball Eject ({'Left' if number == 6 else 'Right'}) page, drawing labelled SW. {34 if number == 6 else 32}, lists the "
			"24-940 coil 090-5036-00B."
		)
	if number == 7:
		notes += (
			" The Magnet Coil, Bracket and Ball Lock page lists the 23-800 coil 090-5001-00T and the Solid Plunger Assembly (Short) "
			"515-6119-02 for the hotel ball lock; the chart prints 090-5001-00B, and its coil note allows either."
		)
	if number == 8:
		notes += (
			" The general parts page lists the Mini-Coil Assembly (for Control Gate) 515-6543-00 with the 32-1800 coil 090-5031-00. "
			"The manual names no switch for the gate."
		)
	if number in (9, 10, 11):
		notes += " The Bumper Top, Bot. & Sw. page carries the 26-1200 coil 090-5044-00T and a #555 wedge bulb under each cap."
	if number in (13, 14):
		side = "left" if number == 13 else "right"
		notes += (
			f" The Flipper (Upper {side.capitalize()}) page lists the 23-900 (GREEN) coil and two spacers in place of an E.O.S. switch: "
			"'Upper Flippers do not require an E.O.S Switch', and on this game the upper bat bushing is red. The 4-Flipper Circuit "
			f"Wiring Diagram draws the UPPER {side.upper()} FLIPPER COIL, 23-900 GREEN, on {control_wire} through a 3A SLO-BLO fuse "
			"under the playfield. The upper flipper coils are ordinary outputs: PinMAME publishes Q13 and Q14 at 13 and 14 and "
			"synthesizes nothing for them."
		)
		refs += (VPX_SCRIPT_SOURCE,)
	if number in (15, 16):
		side = "left" if number == 15 else "right"
		power = 47 if number == 15 else 45
		notes += (
			f" Physical Q{number} is removed from public {number}: se.c's se_solenoid_w masks it off and publishes it as the lower-{side} flipper "
			f"power bit {power}, and core.c synthesizes canonical callback {address} from it. Bind this one coil to public {address}, the retained "
			f"table's SolCallback(sL{'L' if number == 15 else 'R'}Flipper); public {power} is its power-phase state, not a second coil. The "
			"4-Flipper Circuit Wiring Diagram describes the drive: a 40 ms pulse on a button closure, then 1 ms every 12 ms while held, from one "
			f"50v supply through a 3A slow-blow fuse under the playfield ({'GRY-YEL' if number == 15 else 'BLU-YEL'}); the LOWER "
			f"{side.upper()} FLIPPER COIL is a 22-900 with a YELLOW wrap on the Flipper ({side.capitalize()}) assembly."
		)
		refs += (VPX_SCRIPT_SOURCE,)
	if number in (17, 18):
		notes += " The Slingshots page carries the 23-800 coil 090-5001-00T and two stack (blade) switches 180-5054-00 per side."
	if number == 19:
		notes += (
			" The Hotel Door Coil, Frame, Stand-Up pages list the 27-1500 coil 090-5004-00B, the Plunger Assembly 515-7409-00, the "
			"Actuator Arm 535-9478-00 and the Metal Door (Hotel) 535-9477-00."
		)
	if number == 24:
		physical["location"] = "cabinet (coin meter, token dispenser or knocker, when fitted)"
		notes += (
			" The row is printed on a grey band with no part number. DR. 7: 'Coil Q24 is Optional. If either a Coin Meter, Token "
			"Dispenser or Knocker (all optional equipment) is required, call Technical Support'. Standard adjustment 46: 'Q24 OPTION: "
			"Set to COIN METER, TOKEN DISPENSER or KNOCKER. Default is COIN METER. This Coil (Solenoid) Location is left \"open\" at "
			"the Factory'. The cabinet wiring diagram's TO COIN METER box routes 'J16-7 +5V DC' (22 RED) and 'J7-10 Q24' (78 VIO-GRY) "
			"to the meter, as the chart does; the driver board diagram feeds its optional coil 'FROM RED Power Out +5v DC J16-P8', a "
			"different J16 pin. The chart and the cabinet diagram agree, so the record follows J16-P7. The general parts page offers the "
			"optional meter as '+12v DC w/Diode' (G-0053-013-102), while the chart, the driver board diagram and the cabinet diagram feed "
			"the output +5v DC; the record states the chart's 5 V."
		)
	if number in (25, 26, 27, 28):
		notes += (
			" The type cell is merged across rows #25-#28 and printed once. The driver board diagram draws 'STEPPER MOTOR 041-5069-00 "
			"Haydon Nº 46868-12-002' as two centre-tapped windings, its RED, GRN, BLK and BLU leads on J6-1 to J6-4 and both centre "
			"taps on a lug under the playfield fed 'FROM GRY-RED Power Out +12v DC J16-P3'. The Elvis figure parts page lists the "
			"same Haydon motor (46868-12-002, 12v DC 10W) as 041-5089-00; both part readings are kept, and the record states the "
			"chart's. elvis.c's elvis_w reads the four phases from the low nibble of the Q25-Q32 latch: the order 0x0c, 0x06, 0x03, "
			"0x09 counts the figure's position up and the reverse order counts it down to zero, where LibPinMAME writes the home "
			"switch 33 at 1."
		)
		refs += (SIM_SOURCE,)
		physical["location"] = "Elvis figure stepper motor under the playfield"
	if number in (29, 30):
		part_word = "legs" if number == 29 else "arms"
		notes += (
			f" The chart prints the control cell 'RED-WHT TO {control_wire}' and the power cell 'RED-WHT TO BROWN': the coil's own "
			f"RED-WHT leads meet the harness wires. The driver board diagram draws the 29-1400 'ELVIS {part_word.upper()}' coil with "
			"RED-WHT at both ends and 'Diode in Conn.'. The Elvis figure page lists two Coil (29-1400) & Conn. assemblies 500-6818-00 "
			f"and -01 on the carrier with the Actuator Wire (for {part_word.capitalize()}) {'535-9452-00' if number == 29 else '535-9451-00'}. "
			f"elvis.c reads it as bit {4 if number == 29 else 5} of the Q25-Q32 latch."
		)
		refs += (SIM_SOURCE,)
	if number in SOLENOID_SCRIPT:
		notes += f" Retained table script: {SOLENOID_SCRIPT[number]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if number in SOLENOID_RUNTIME:
		notes += f" In the harness runs {SOLENOID_RUNTIME[number]}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Q{number}"}], "wiring": _q_wiring(number)}
	role = "emitter" if kind == "flasher" else "effect"
	if number in (4, 24):
		extra["roles"] = ["cabinet.shaker"] if number == 4 else ["cabinet.q24-option"]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("solenoid", address, identifier, role)
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("solenoid", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, physical=physical, **extra)


AUX_POSTS = {
	33: ("AUX 1", "LEFT UP/DOWN POST", "26-1200 / 090-5044-00T", "WHITE", "J2-P3"),
	34: ("AUX 2", "CENTER UP/DOWN POST", "23-1100 / 090-5030-00T", "RED", "J2-P4"),
	35: ("AUX 3", "RIGHT UP/DOWN POST", "26-1200 / 090-5044-00T", "ORANGE", "J2-P7"),
}


def solenoid_outputs() -> list[dict[str, Any]]:
	items = [_q_output(number) for number in Q_OUTPUTS]
	items.append(_device(
		"virtual.15-fast-flip-game-on", "Whitestar Fast-Flip / Game-On State", "virtual", SOLENOID_GROUP, 15, "used",
		(CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "15"}],
		physical={"notes": (
			"se.c sets public 15 while the ROM's fast-flip byte is non-zero, i.e. while the flippers are enabled in a game; "
			"MACHINE_INIT(se3) places that byte at CPU RAM 0x04 for every se3 game, so all twenty-one Elvis sets publish it. sega.vbs "
			"declares GameOnSolenoid = 15. In the gameplay and hound-dog runs it rose at Start. Physical Q15 is the left flipper at "
			"public 48; never wire this state to a transistor."
		)},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	items.append(_device(
		"virtual.16-remapped-flipper-hole", "Unused Remapped-Flipper Address 16", "virtual", SOLENOID_GROUP, 16, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "16"}],
		physical={"notes": "se_solenoid_w masks physical Q16 off public 16 and publishes it at 45/46; nothing else drives 16."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	for address in range(33, 45):
		if address in AUX_POSTS:
			aux, name, coil, wire, pin = AUX_POSTS[address]
			notes = (
				"A Whitestar compatibility hole that elvisGameData leaves unpublished. The coil chart's auxiliary group, printed for UK "
				f"machines only on the UK 3X Trans. Driver Board, lists '{aux}: {name}' (driver Q{address - 32}, {wire} {pin}, BROWN J7-P1 "
				f"20v DC, {coil}); the board table lists the 'for UK ONLY Aux. Driver Bd. 520-5068-01'. elvisGameData declares no "
				"auxiliary board, so PinMAME publishes none of the three posts, here or anywhere: in the Single Coil Test run the ROM "
				f"stepped to \"{_coil_test(address)}\" and no public solenoid changed. A UK machine's post-save devices therefore have "
				"no address a recreation could drive."
			)
			refs: tuple[str, ...] = (CORE_SOURCE, CONTROLLER_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE)
		else:
			notes = "A Whitestar compatibility hole: elvisGameData declares no auxiliary board, and nothing in se.c drives it for this driver."
			refs = (CORE_SOURCE, CONTROLLER_SOURCE)
		items.append(_device(
			f"virtual.{address}-reserved", f"Reserved Address {address}", "virtual", SOLENOID_GROUP, address, "unused", refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": notes},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	for address, side, canonical, number in ((45, "right", 46, 16), (47, "left", 48, 15)):
		items.append(_device(
			f"virtual.{address}-{side}-flipper-power-phase", f"{side.capitalize()} Flipper Power-Phase State", "virtual", SOLENOID_GROUP, address, "used",
			(CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE), aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": (
				f"se_solenoid_w publishes physical Q{number}'s drive here and core.c synthesizes canonical {canonical} from it; one {side} flipper coil "
				f"is bound at {canonical}. In the gameplay run, holding the {side} flipper button pulsed {address} and {canonical} together."
			)},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	items.append(_device(
		"virtual.49-simulated-shooter", "Unused Simulated Ball Shooter", "virtual", SOLENOID_GROUP, 49, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "49"}],
		physical={"notes": "PinMAME's reserved simulation output; the machine's auto launch is Q2 at public 2."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	items.append(_device(
		"virtual.50-reserved", "Reserved Address 50", "virtual", SOLENOID_GROUP, 50, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "50"}],
		physical={"notes": "The last address below PinMAME's custom-solenoid boundary (custSol is 0 for this driver); nothing drives it."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	return sorted(items, key=lambda item: item["binding"]["device"])


# --- Lamps ---------------------------------------------------------------------------------------------
# address -> (label, grid name, bulb cell)
LAMPS: dict[int, tuple[str, str, str]] = {
	1: ("Rock Again", "ROCK AGAIN", "#555 Clear Bulb"), 2: ("Left Outlane", "LEFT OUTLANE", "#555 Clear Bulb"),
	3: ("Left Return Lane", "LEFT RETURN LANE", "#555 Clear Bulb"), 4: ("Right Return Lane", "RIGHT RETURN LANE", "#555 Clear Bulb"),
	5: ("Right Outlane", "RIGHT OUTLANE", "#555 Clear Bulb"), 6: ("Spot Note", "SPOT NOTE", "#555 Clear Bulb"),
	7: ("Scarf", "SCARF", "#555 Clear Bulb"), 8: ("TCB T", "( T )CB", "#555 Clear Bulb"),
	9: ("Hound Dog", "HOUND DOG", "#555 Clear Bulb"), 10: ("Blue Suede Shoes", "BLUE SUEDE SHOES", "#555 Clear Bulb"),
	11: ("Heartbreak Hotel", "HEARTBREAK HOTEL", "#555 Clear Bulb"), 12: ("Jailhouse Rock", "JAILHOUSE ROCK", "#555 Clear Bulb"),
	13: ("All Shook Up", "ALL SHOOK UP", "#555 Clear Bulb"), 14: ("Hits Completed", "HITS COMPLETED", "#555 Clear Bulb"),
	15: ("Elvis Collected", "ELVIS COLLECTED", "#555 Clear Bulb"), 16: ("Top 10 Completed", "TOP 10 COMPLETED", "#555 Clear Bulb"),
	17: ("Top 10 Ladder 10", "10", "#555 Clear Bulb"), 18: ("Top 10 Ladder 9", "9", "#555 Clear Bulb"),
	19: ("Top 10 Ladder 8", "8", "#555 Clear Bulb"), 20: ("Top 10 Ladder 7", "7", "#555 Clear Bulb"),
	21: ("Top 10 Ladder 6", "6", "#555 Clear Bulb"), 22: ("Left Ramp Arrow", "LEFT RAMP ARROW", "#555 Clear Bulb"),
	23: ("Shook", "SHOOK", "#555 Clear Bulb"), 24: ("Left Ramp Note", "LEFT RAMP NOTE", "#555 Clear Bulb"),
	25: ("Top 10 Ladder 5", "5", "#555 Clear Bulb"), 26: ("Top 10 Ladder 4", "4", "#555 Clear Bulb"),
	27: ("Top 10 Ladder 3", "3", "#555 Clear Bulb"), 28: ("Top 10 Ladder 2", "2", "#555 Clear Bulb"),
	29: ("Top 10 Ladder 1", "1", "#555 Clear Bulb"), 30: ("Right Ramp Arrow", "RIGHT RAMP ARROW", "#555 Clear Bulb"),
	31: ("Up", "UP", "#555 Clear Bulb"), 32: ("Right Ramp Note", "RIGHT RAMP NOTE", "#555 Clear Bulb"),
	33: ("ELVIS E", "( E )LVIS", "#44 Clear Bulb"), 34: ("ELVIS L", "E( L )VIS", "#44 Clear Bulb"),
	35: ("ELVIS V", "EL( V )IS", "#44 Clear Bulb"), 36: ("ELVIS I", "ELV( I )S", "#44 Clear Bulb"),
	37: ("ELVIS S", "ELVI ( S )", "#44 Clear Bulb"), 38: ("Right Orbit Arrow", "RIGHT ORBIT ARROW", "#44 Clear Bulb"),
	39: ("Gift From Elvis", "GIFT FROM ELVIS", "#555 Clear Bulb"), 40: ("Right Orbit Note", "RIGHT ORBIT NOTE", "#555 Clear Bulb"),
	41: ("Left Orbit Arrow", "LEFT ORBIT ARROW", "#555 Clear Bulb"), 42: ("Left Orbit Blue Suede Shoes", "L. ORBIT BLUE SUEDE SHOES", "#555 Clear Bulb"),
	43: ("All", "ALL", "#555 Clear Bulb"), 44: ("Left Orbit Note", "LEFT ORBIT NOTE", "#555 Clear Bulb"),
	45: ("KING K", "( K )ING", "#44 Clear Bulb"), 46: ("KING I", "K( I )NG", "#44 Clear Bulb"),
	47: ("KING N", "KI( N )G", "#44 Clear Bulb"), 48: ("KING G", "KIN( G )", "#44 Clear Bulb"),
	49: ("Hound", "HOUND", "#555 Clear Bulb"), 50: ("Dog", "DOG", "#555 Clear Bulb"),
	51: ("Center Loop Arrow", "CENTER LOOP ARROW", "#555 Clear Bulb"), 52: ("Center Loop Blue Suede Shoes", "C. LOOP BLUE SUEDE SHOES", "#555 Clear Bulb"),
	53: ("Center Loop Note", "CENTER LOOP NOTE", "#555 Clear Bulb"), 54: ("Lock", "LOCK", "#555 Clear Bulb"),
	55: ("Jackpot", "JACKPOT", "#555 Clear Bulb"), 56: ("Super Jackpot", "SUPER JACKPOT", "#555 Clear Bulb"),
	57: ("Left Top Lane", "LEFT TOP LANE", "#555 Clear Bulb"), 58: ("Middle Top Lane", "MIDDLE TOP LANE", "#555 Clear Bulb"),
	59: ("Right Top Lane", "RIGHT TOP LANE", "#555 Clear Bulb"), 60: ("Heart", "HEART", "#44 Clear Bulb"),
	61: ("Break", "BREAK", "#44 Clear Bulb"), 62: ("Hotel", "HOTEL", "#44 Clear Bulb"),
	63: ("TCB C", "T( C )B", "#555 Clear Bulb"), 64: ("TCB B", "TC( B )", "#555 Clear Bulb"),
	65: ("Video Mode", "VIDEO MODE", "#44 Yellow Bulb"), 66: ("Gold Record", "GOLD RECORD", "#44 Yellow Bulb"),
	67: ("King of Rock n Roll", "KING OF ROCK N ROLL", "#44 Yellow Bulb"), 68: ("Lite Extra Ball", "LITE EXTRA BALL", "#44 Yellow Bulb"),
	69: ("Encore Letter", "ENCORE LETTER", "#44 Yellow Bulb"), 70: ("Graceland", "GRACELAND", "#44 Blue Bulb"),
	71: ("Special", "SPECIAL", "#44 Red Bulb"), 72: ("Extra Ball", "EXTRA BALL", "#44 Orange Blb."),
	73: ("ENCORE E (First)", "( E )NCORE", "#44 Clear Bulb"), 74: ("ENCORE N", "E( N )CORE", "#44 Clear Bulb"),
	75: ("ENCORE C", "EN( C )ORE", "#44 Clear Bulb"), 76: ("ENCORE O", "ENC( O )RE", "#44 Clear Bulb"),
	77: ("ENCORE R", "ENCO( R )E", "#44 Clear Bulb"), 78: ("ENCORE E (Last)", "ENCOR( E )", "#44 Clear Bulb"),
	79: ("Tournament Button", "TOURNAMENT BUTTON", "#555 Clear Bulb"), 80: ("Start Button", "START BUTTON", "#555 Clear Bulb"),
}
LAMP_DRIVE = [("YEL-BRN", "J13-P9", "U17"), ("YEL-RED", "J13-P8", "U16"), ("YEL-ORG", "J13-P7", "U15"), ("YEL-BLK", "J13-P6", "U14"), ("YEL-GRN", "J13-P5", "U13"), ("YEL-BLU", "J13-P4", "U12"), ("YEL-VIO", "J13-P3", "U11"), ("YEL-GRY", "J13-P1", "U10")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
BULB_PARTS = {
	"#555 Clear Bulb": "165-5002-00", "#44 Clear Bulb": "165-5000-44-HF", "#44 Yellow Bulb": "165-5053-06", "#44 Blue Bulb": "165-5053-05",
	"#44 Red Bulb": "165-5053-02", "#44 Orange Blb.": "165-5053-07",
}
BACK_PANEL_LAMPS = (60, 61, 62, 73, 74, 75, 76, 77, 78)
ABOVE_PLAYFIELD_LAMPS = (65, 66, 67, 68, 69, 70, 71, 72)
CABINET_LAMPS = (79, 80)
# Lamp -> the table objects its fader drives, beyond the insert Light lN (embedded script lines 570-653).
LAMP_FLASHERS = {57: ("l57a",), 58: ("l58a",), 59: ("l59a",), 70: ("l70a", "l70"), 71: ("l71a", "l71"), 72: ("l72a", "l72")}


def lamp_id(address: int) -> str:
	return f"lamp.{address}-{slug(LAMPS[address][0])}"


def _lamp_wiring(address: int) -> dict[str, Any]:
	row, column = divmod(address - 1, 8)
	drive_wire, drive_connection, driver = LAMP_DRIVE[column]
	return_wire, return_connection = LAMP_RETURN[row]
	return {
		"board": "Whitestar I/O Power Driver board 520-5137-01 lamp matrix", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "return_component": f"column driver {driver}; row transistor Q{33 + row}",
	}


def _lamp_table_note(address: int) -> str:
	if address in CABINET_LAMPS:
		return " The retained script assigns no table object to it."
	if address <= 56 or address in (63, 64):
		return (
			f" Retained table script: the lamp fader drives the Light l{address} (UpdateLamps, lines 570-636; UseLamps = 0, line 39), "
			"an insert overlay that draws an insert image with no bulb (is_bulb_light and show_bulb_mesh false), so the lamp is not placed."
		)
	if address in (57, 58, 59):
		return (
			f" Retained table script: the lamp fader drives the Light l{address} and the Flasher sprite l{address}a (lines 626-631); the "
			"Light is an insert overlay with no bulb and the Flasher a render helper, so the lamp is not placed."
		)
	objects = LAMP_FLASHERS.get(address, (f"l{address}",))
	return (
		f" Retained table script: the lamp fader drives only the Flasher sprite{'s' if len(objects) > 1 else ''} "
		f"{' and '.join(objects)} (lines 632-653), a render helper that is not a bulb socket, so the lamp is not placed."
	)


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 81):
		row, column = divmod(address - 1, 8)
		identifier = lamp_id(address)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		label, printed, bulb = LAMPS[address]
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE)
		if address in BACK_PANEL_LAMPS:
			location = "rear of the back panel"
		elif address in ABOVE_PLAYFIELD_LAMPS:
			location = "above the playfield"
		elif address in CABINET_LAMPS:
			location = "cabinet front (tournament button lamp)" if address == 79 else "cabinet front (start button lamp)"
		else:
			location = "playfield insert"
		physical: dict[str, Any] = {"location": location, "part_number": BULB_PARTS[bulb]}
		test = _service_line(_reading("elvis-single-lamp-test", f"Black ENTER button (public 0) pressed on +: lamp step {address}"))
		notes = (
			f'Printed lamp-matrix row {row + 1}, column {column + 1}. The Lamp Matrix Grid (DR. 5) prints "{printed}" with the bulb cell '
			f'"{bulb}"; the page\'s part notes give {BULB_PARTS[bulb]}. The 5.00 ROM\'s Single Lamp Test names it "{test}" (column '
			"wire, row wire)."
		)
		if address == 15:
			notes += " The ROM prints ELVIS COMPLETED where the grid prints ELVIS COLLECTED; the label follows the grid."
		if address in BACK_PANEL_LAMPS:
			notes += (
				" The location drawing's rear-view inset puts it in a grey (not on playfield) box: 'Lamps 60-62 & 73-78 are located on "
				"the rear of the Back Panel.' The Back Panel page lists ten 2-Lug Staple-Down and nine 3-Lug Laydown sockets with #44 "
				"Bulb (Clear) Heavy Filament."
			)
		elif address in ABOVE_PLAYFIELD_LAMPS:
			notes += (
				" The location drawing puts it in a white (above playfield) box, "
				f"{'in a row on the plan' if address <= 69 else 'in a row at the plan rear edge'}."
			)
		elif address in CABINET_LAMPS:
			notes += (
				" The location drawing puts it in a grey box at the cabinet front, and the cabinet wiring diagram's START / TOURNIE BUTTON "
				f"LAMPS draw 'Lamp {address} {'Tournie' if address == 79 else 'Start'}' with a diode, the two lamps fed by RED from J12 pin 11 and "
				"returning on YEL-VIO (J13 pin 3) and YEL-GRY (J13 pin 1), which the grid assigns to columns 7 and 8."
			)
			if address == 79:
				notes += " The grid's black panel beside 79 reads 'Optional Tournament Kit Required'."
		else:
			notes += " The location drawing puts it in a black (below playfield) box on the plan: a playfield insert lit from below."
		notes += " The harness runs saw the ROM drive it."
		notes += _lamp_table_note(address)
		refs += (VPX_SCRIPT_SOURCE,)
		extra: dict[str, Any] = {"aliases": aliases, "wiring": _lamp_wiring(address)}
		if address in CABINET_LAMPS:
			extra["roles"] = ["cabinet.tournament-button-lamp"] if address == 79 else ["cabinet.start-button-lamp"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		items.append(_device(identifier, label, "lamp", LAMP_GROUP, address, "optional" if address == 79 else "used", refs, physical=physical, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	entries = _spatial_seed()["gi"]["0"]
	without_bulb = _spatial_seed()["gi_without_bulb"]["0"]
	placements = [{
		"id": f"gi.relay.emitter.{index}", "role": "emitter", "space": "playfield", "x": entry["x"], "y": entry["y"],
		"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
	} for index, entry in enumerate(entries, start=1)]
	notes = (
		"One G.I. relay on the I/O Power Driver Board 520-5137-01 (U206 74HCT273 data latch output 1Q from D0 through R254 1K to the "
		"Q200 2N3904 relay driver, coil on 20v DC with D229 1N4004 across it) switches the 5.7v AC G.I. supply from J14 (YEL pins 1-3, "
		"YEL-WHT pins 4-6) through four 5A slow-blow fuses to the four circuits on J15 (General Illumination Circuit Detailed Wiring "
		"Diagram, PDF page 120): B, F24, BRN-WHT to WHT-BRN, 'Back Panel X10; Pops X3 Upper Right Corner X1', 11 #44 and 3 #555; Y, "
		"F25, YELLOW to WHT-YEL, 'Mid Left & Lower Playfield X15', 15 #44 and 1 #555; G, F26, GREEN to WHT-GRN, 'Upper Playfield X10 "
		"+ US Coin Door X2 (Euro X3)', 10 #44 then 2 #555 on the coin door; V, F27, VIOLET to WHT-VIO, 'Mid Right Playfield X6', 5 #44 "
		"and 1 #555 (its last socket printed #5*). The quantity 48 is those printed counts with the US coin door's two; the page warns "
		"'* G.I. Bulb quantities may change during production.' The pop bumper bulbs are G.I. (the Bumper page lists a #555 under each "
		"cap), and the back panel's ten 'GIs on rear Back Panel' are circuit B. se.c publishes the relay as GI 0 (on while its latch "
		"bit is low). The harness runs saw it on in attract mode, off from Start until the served ball reached the shooter lane, and "
		"blinking with the TC(B) target 24, the KIN(G) target 39, the scarf standup 40 and a ball arriving in either saucer or on the "
		"hotel post. The retained table declares UseGI = 0 (line 40) and sets GICallback = GetRef(\"GIUpdate\") (line 1038), whose "
		f"sub switches the aGiLights and aGiFlashers collections. The placements are the {len(entries)} members of aGiLights that "
		f"draw their bulb mesh ({', '.join(entry['object'] for entry in entries)}), observed only; the drawing's circuit discs have "
		f"not been matched to them, so no placement carries a string. The other {len(without_bulb)} members "
		f"({', '.join(without_bulb)}) are bulb-mode Lights that show no bulb mesh, with no primitive modelling a socket under them, "
		"so they sit on no bulb and make no socket. The rest of the 48, including the back panel's ten and the coin door's two, are "
		"counted but not placed."
	)
	return [_device(
		"gi.relay", "General Illumination Relay", "gi", GI_GROUP, 0, "used", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.gi", "value": "0"}],
		physical={"location": "playfield, back panel and coin door", "quantity": 48, "notes": notes},
		wiring={"board": "Whitestar I/O Power Driver board 520-5137-01 G.I. relay", "power_wire": "YEL / YEL-WHT 5.7v AC through F24-F27", "power_connection": "J14/J15", "nominal_voltage_v": 5.7, "voltage_type": "ac"},
		spatial={"status": "observed", "placements": placements},
	)]


def displays() -> list[dict[str, Any]]:
	return [{
		"id": "display.dmd", "label": "Dot Matrix Display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32,
		"physical_location": "cabinet_or_service",
		"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		"spatial": not_applicable("cabinet_or_service", CORE_SOURCE),
	}]


# --- Mechanisms ----------------------------------------------------------------------------------------
def _mechanism(suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...], assembly: str | None = None, positions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
	result: dict[str, Any] = {"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior}
	if assembly:
		result["assembly_part_number"] = assembly
	if positions:
		result["positions"] = positions
	result["provenance"] = provenance("validated", *refs)
	return result


def mechanisms() -> list[dict[str, Any]]:
	common = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	run = common + (RUNTIME_SOURCE,)
	s = switch_id
	d = dedicated_id
	q = q_output_id
	return [
		_mechanism("trough", "4-ball trough with up-kicker and stacking opto", "kicker", [q(1)], [s(11), s(12), s(13), s(14), s(15)],
			"Four balls rest in the 4-Ball Trough on micro switches 11 (left), 12 and 13 (Roller Actuator, Lite-Force, 180-5119-02) and on "
			"the up-kicker opto 14; the Dual OPTO boards carry 14 on the lower beam (LED1) and the stacking opto 15 on the upper beam "
			"(LED2), which only a double-stacked ball breaks. Q1 (26-1200) kicks the ball on 14 up past 15 into the shooter lane, and the "
			"rest roll one place toward the up-kicker. Hold each occupied position at 1 and pass the kicked ball through 15 as a short 1 "
			"pulse (beam blocked). In the gameplay run the ROM fired Q1 about 1.1 s after Start and repeated it about every 1.25 s until "
			"the scenario moved the served ball to 16; in the stacking-opto run a rise of 15 drew six Q1 kicks and then the auto launch Q2, the "
			"ROM's jam clearing. The retained table pulses 15 from its Q1 callback.", run),
		_mechanism("shooter", "Shooter lane and auto launch", "kicker", [q(2)], [s(16), s(10)],
			"A served ball comes to rest on the shooter-lane switch 16 and leaves past the shooter lane exit switch 10. The Ball Shooter "
			"(Plunger) Autoplunger Arm assembly carries the auto-launch coil Q2 (23-800); the cabinet also has a manual plunger, which "
			"the retained table models beside its impulse plunger. In the gameplay run the ROM did not fire Q2 while the ball rested on "
			"16 for 6 s, and fired it 0.17 s after the right flipper button was pressed while no ball was on 16 and in ball search; "
			"the Diagnostic Aids page names '#16 Shooter Lane & #2 Auto Launch' as a pair the CPU retries about ten times before "
			"reporting the switch.", run),
		_mechanism("elvis-figure", "Dancing Elvis figure", "motorized", [q(25), q(26), q(27), q(28), q(29), q(30)], [s(33), s(36), s(37), s(38), s(39)],
			"The Elvis assembly (reference 500-6796-00) carries the molded figure (torso, legs and two arms) on a platform riveted "
			"assembly over a welded carrier frame; a Haydon 46868-12-002 12 V DC stepper motor (Stepper Motor Assembly 500-6809-00) "
			"turns a 7.25\" threaded shaft that moves it. The ELVIS test page describes one full RUN cycle as back-to-front or "
			"front-to-back, and the home switch 33 (Micro Switch (Short Actuator, Bend) 180-5189-00) as closed with Elvis 'in the Home "
			"Position or closest to the Upper Playfield'. The stepper's four phases are Q25-Q28; elvis.c counts the order 0x0c, 0x06, "
			"0x03, 0x09 as one direction and the reverse as the other. Two Coil (29-1400) & Conn. assemblies (500-6818-00 and -01) pull "
			"the actuator wires for the legs (Q29) and the arms (Q30); IPDB describes the toy's shaking hips and gesturing hands, which "
			"bring the microphone to his lips. The four KING stand-up targets 36-39 (515-7381-00) sit on the figure's base and travel "
			"with it. The ELVIS test: RUN runs the stepper one full cycle, PULSE pulses it, LEGS and ARMS energize Q29 and Q30, and on "
			"power-up the mechanism returns to its HOME position. In the ELVIS-test harness run, RUN drove the phases and left 33 open, a "
			"second RUN closed it, PULSE moved the figure off home, and LEGS and ARMS drove Q29 and Q30; every run drove the phases at "
			"boot and left 33 closed. In a game the ROM ran the phases with the legs and arms from many scoring switches. The retained "
			"table moves the stand primitive with a one-solenoid cvpmMech on Q25 alone (150 steps, 33 at step 0), a stand-in that "
			"ignores Q26-Q28 and the direction.",
			run + (SIM_SOURCE, IDENTITY_SOURCE), assembly="500-6796-00",
			positions=[
				{"id": "mechanism.elvis-figure.home", "label": "Home", "sensors": [s(33)], "description": "Figure at the end of its travel closest to the upper playfield; the position after power-up."},
			]),
		_mechanism("elvis-drop-bank", "ELVIS 5-bank drop targets", "drop_target_bank", [q(3)], [s(17), s(18), s(19), s(20), s(21)],
			"The 5-Bank Drop Target assembly: five white drop targets (545-6102-01) on drop-target switches 17-21 (180-5158-00, diodes "
			"on the terminal strip), spelling E-L-V-I-S, and the 24-940 reset coil Q3. A down target holds its switch closed. In the "
			"gameplay run the ROM pulsed Q3 0.33 s after the fifth target went down and twice more 0.41 s apart; it also reset the bank "
			"at boot and at Start.", run),
		_mechanism("hotel-door", "Heartbreak Hotel door", "gate", [q(19)], [s(63), s(52), s(53)],
			"The Hotel Door Coil, Frame, Stand-Up assembly: a 27-1500 coil (Q19) with the Plunger Assembly 515-7409-00 and Actuator Arm "
			"535-9478-00 moves the Metal Door (Hotel) 535-9477-00. The door's micro switch 63 (180-5119-02) and the two 1\" stand-up "
			"targets 52 (top) and 53 (bottom) on the mini-playfield behind it complete it. The ROM holds Q19 on for long stretches: in the "
			"gameplay run it switched Q19 on when 52 closed and while a ball rested in either saucer or on the hotel post, and in the "
			"hound-dog probe 0.13 s after 63 rose and about 65 ms after each hound-dog hit. The retained table drops doorwall and swings "
			"the flipper-shaped door fDoor open while Q19 is on.", run),
		_mechanism("hotel-lock", "Hotel ball lock", "other", [q(7)], [s(48)],
			"A ball held at the hotel post rests on micro switch 48 (180-5189-00); the hotel lock release Q7 (23-800, with the Solid "
			"Plunger Assembly (Short) 515-6119-02 on the Magnet Coil, Bracket and Ball Lock page) releases it. In the gameplay run a ball "
			"held on 48 for 6 s drew no Q7; Q7 fired only in ball search. The retained table holds the ball in the kicker HLock and "
			"kicks it on Q7.", run),
		_mechanism("center-saucer", "Center saucer (Ball Eject Left)", "kicker", [q(6)], [s(34)],
			"The Ball Eject (Left) assembly, drawing labelled SW. 34: a ball resting on micro switch 34 (180-5186-00) is kicked out by "
			"Q6 (24-940). In the gameplay run the ROM kicked about 4.3 s after the ball arrived and twice more about 0.7 s apart while it "
			"stayed.", run),
		_mechanism("top-saucer", "Top saucer (Ball Eject Right)", "kicker", [q(12)], [s(32)],
			"The Ball Eject (Right) assembly, drawing labelled SW. 32: a ball resting on micro switch 32 (180-5186-00) is kicked out by "
			"Q12 (24-940, TOP EJECT). In the gameplay run the ROM kicked once about 5.7 s after the ball arrived.", run),
		_mechanism("magnet", "Magnet", "other", [q(5)], [],
			"A 22-650 magnet coil (500-6808-00, diode in its connector) under the playfield on Q5; it has no switch of its own. In the "
			"gameplay run it fired only in ball search. The retained table models it as a cvpmMagnet around the trigger Magnet that "
			"grabs balls while Q5 is on.", run, assembly="500-6808-00"),
		_mechanism("control-gate", "Control gate", "gate", [q(8)], [],
			"A mini-coil assembly (515-6543-00, coil 32-1800) on Q8; the manual names no switch for it. Only the ROM's Single Coil Test "
			"fired it in the harness runs. The retained table holds the gate CGate open while Q8 is on.", run, assembly="515-6543-00"),
		_mechanism("hound-dog", "Hound dog pop-up target", "toy", [], [s(64)],
			"The Hound Dog Pop-Up Target (assembly reference 500-6781-00): the dog figure 500-6820-00 on a base bracket with an actuator "
			"bracket, a deflector pad and the micro switch 64 (180-5190-28); it has no coil. The ROM reads 64 as hit at public 0, so the "
			"contact rests closed and a hit opens it. In the hound-dog probe each hit made the ROM switch the hotel door Q19 on about 65 ms "
			"later. The retained table animates the dog primitive and pulses 64 to 1, the opposite level.", run, assembly="500-6781-00"),
		_mechanism("lower-flippers", "Lower flippers", "other", [q(15), q(16)], [d(84), d(83), d(82), d(81)],
			"Left and right lower flipper assemblies with 22-900 (YELLOW) coils and E.O.S. switches 180-5149-00, on one 50v supply. The "
			"CPU applies a 40 ms pulse on a button closure and then 1 ms every 12 ms while the button is held; each N.C. end-of-stroke "
			"switch opens at full stroke, and a closure during a hold earns another 40 ms pulse. PinMAME publishes Q15 at 47/48 and Q16 "
			"at 45/46 and writes the E.O.S. inputs 81 and 83 itself.", (MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE)),
		_mechanism("upper-flippers", "Upper flippers", "other", [q(13), q(14)], [d(84), d(88)],
			"Upper left and upper right flipper assemblies with 23-900 (GREEN) coils, red bat bushings and spacers in place of an E.O.S. "
			"switch. The left cabinet button (84) works both left flippers; the right cabinet button is double-stacked, a half press "
			"(82) working the lower right flipper and a full press (82 and 88) both right flippers. In the gameplay run 84 drove Q13 with "
			"the lower left flipper, 88 drove Q14, and 82 alone never drove Q14. The retained table rotates its upper flippers from the "
			"lower-flipper callbacks.", (MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE)),
		_mechanism("bumpers", "Three pop bumpers", "other", [q(9), q(10), q(11)], [s(49), s(50), s(51)],
			"Left (Q9/49), right (Q10/50) and bottom (Q11/51) pop bumpers with 26-1200 coils, stack switches 180-5015-05 mounted in "
			"reverse and #555 G.I. bulbs under the caps; each switch fired its own coil in the gameplay run.", run),
		_mechanism("slingshots", "Slingshots", "other", [q(17), q(18)], [s(59), s(62)],
			"Left (Q17/59) and right (Q18/62) slingshots with 23-800 coils, two blade contacts per side, only one of them with a diode; "
			"each switch fired its own coil in the gameplay run.", run),
		_mechanism("uk-post-save", "UK post save (unpublished)", "other", [], [s(1), s(8)],
			"UK only: the coil chart's auxiliary group drives a left up/down post (AUX 1, 26-1200), a centre up/down post (AUX 2, "
			"23-1100) and a right up/down post (AUX 3, 26-1200) from the UK 3X Transistor Driver Board 520-5068-01; the cabinet wiring "
			"diagram calls the outer two the outlane ball deflectors, and the parts pages show a UK Up/Down Post and a UK Ball Deflector. "
			"The UK cabinet buttons 1 (left deflector) and 8 (right deflector), pressed together for the centre post, ask the ROM for "
			"them, and standard adjustment 39 enables the feature (UK default YES). elvisGameData declares no auxiliary board, so "
			"PinMAME publishes none of the three outputs; the mechanism has no actuator a recreation can bind.", (MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE)),
	]


# --- Drivers -------------------------------------------------------------------------------------------
def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {driver["id"]: driver for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
	if set(by_id) != set(DRIVER_IDS):
		raise RuntimeError(f"Elvis driver family differs from the catalog: {sorted(set(DRIVER_IDS) ^ set(by_id))}")
	records = []
	for driver_id in sorted(DRIVER_IDS):
		source = by_id[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = DRIVER_COMPATIBILITY[driver_id]
		record["variant_notes"] = BASE_DRIVER_NOTE + _driver_note(driver_id)
		records.append(record)
	return records


# --- Sources -------------------------------------------------------------------------------------------
def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _excerpt_digests() -> dict[str, str]:
	return {path.name: _file_sha256(path) for path in sorted(EXCERPT_ROOT.glob("*")) if path.is_file()}


EXCERPT_FILE_HASHES = _excerpt_digests()


def _excerpt(name: str, locator: str, *, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	return {
		"id": f"excerpt.elvis.{name}", "locator": locator, "path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"], "method": method, "transcribed_by": credit, "reviewed": reviewed,
	}


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("diagnostic-aids-and-dip-switches", "PDF page 5, printed DR. 3, Diagnostic Aids and CPU DIP Switch Settings (SW300 country charts)"),
		_excerpt("switch-matrix", "PDF page 6, printed DR. 4, Switch Matrix Grid, Dedicated Switches & Locations"),
		_excerpt("lamp-matrix", "PDF page 7, printed DR. 5, Lamp Matrix Grid & Locations"),
		_excerpt("coil-table", "PDF page 8, printed DR. 6, Coils Detailed Chart Table"),
		_excerpt("coil-flash-locations", "PDF page 9, printed DR. 7, Coil & Flash Lamp Locations"),
		_excerpt("service-adjustments", "PDF pages 42 and 63, Portals Service Menu: Knocker test and standard adjustments 39 and 46"),
		_excerpt("elvis-test", "PDF page 43, printed Section 3, Chapter 2, Page 27, ELVIS Test (Stepper Motor Test)"),
		_excerpt("driver-board-wiring", "PDF page 118, printed Section 5, Chapter 1, Page 101, Backbox I/O Power Driver Board Detailed Wiring Diagram"),
		_excerpt("gi-wiring", "PDF page 120, printed Section 5, Chapter 2, Page 103, General Illumination Circuit Detailed Wiring Diagram"),
		_excerpt("flipper-circuit", "PDF page 123, printed Section 5, Chapter 2, Page 106, 4-Flipper Circuit Wiring Diagram"),
		_excerpt("cabinet-wiring", "PDF page 125, printed Section 5, Chapter 3, Page 108, Cabinet / Coin Door Wiring Diagram"),
		_excerpt("opto-boards", "PDF pages 126-128, printed Section 5, Chapter 4, Pages 109-111, Trough Up-Kicker Dual OPTO boards"),
		_excerpt("firmware-board-tables", "PDF pages 168, 170 and 172, Appendices A (firmware), C (production) and D (board types), Elvis rows"),
		_excerpt("mechanism-assemblies", "PDF pages 95-117 (printed 76-98), major assemblies; PDF pages 82 and 85 general parts (selected items)", reviewed=False),
	]


def source_records() -> list[dict[str, Any]]:
	raw_runs = load_json(ROOT / RUNTIME_PATH)["runtime"]["raw_runs"]
	described = ", ".join(f"{raw['name']} (run.json SHA-256 {raw['sha256'][:12]}..., directory manifest {RUN_MANIFESTS[raw['name']][:12]}...)" for raw in raw_runs)
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the elvis clone tree (" + ", ".join(DRIVER_IDS) + ")",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				f"src/wpc/se.c (SHA-256 {SE_FILE_SHA256}): MACHINE_INIT(se3) (line 263; fast-flip byte at CPU RAM 0x04 for every se3 game, "
				"the Elvis #89 bulb model on 20-23 and 31-32 at lines 322-324), the fast-flip block publishing public 15 (lines 181-191), "
				"ram_w's memory-protect gate on -3 (lines 257 and 593-596), switch_r (~core_getSwCol, line 641), dedswitch_r (flipper column swapped "
				"into U206 order and complemented, DED #5 from bit 0x80, lines 654-662), dip_r (line 665), se_solenoid_w (Q15/Q16 masked "
				"off and published at 47/45, line 669) and the G.I. relay at gi[0] (line 829); src/wpc/core.h FLIP_SOL(x), which includes "
				f"FLIP_EOS(x) (lines 158-161); src/wpc/core.c (SHA-256 {CORE_FILE_SHA256}) core_updateSw (lines 1793-1870: the EOS "
				"simulation of the lower flippers and the flipMask rewrite) and the flipMask built from the driver's flipper flags "
				"(lines 2831-2839); src/wpc/sims/se/prelim/elvis.c elvisGameData (lines 473-489: GEN_WS, a 128x32 DMD, FLIP_SW(FLIP_L) | "
				"FLIP_SOL(FLIP_L), swCol 0, lampCol 2, custSol 0, invSw all zero, start/tilt/slam 54/56/55), the twenty-one game "
				"definitions on de_mSES3 (lines 426-450) and init_elvis (line 523)."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": SIM_SOURCE, "kind": "pinmame_sim", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "sha256": SIM_FILE_SHA256,
			"locator": (
				"src/wpc/sims/se/prelim/elvis.c: the simulator's switch and coil names (lines 100-124: swStart 54, swSlamTilt 55, swTilt "
				"56, trough 11-15, shooter 16, lanes and slings 57-62; sTrough 1, sLaunch 2, slings 17 and 18) and elvis_w (lines 493-518), "
				"which passes every solenoid latch write to se_solenoid_w and, on the Q25-Q32 latch, counts the stepper phase order 0x0c, "
				"0x06, 0x03, 0x09 up and its reverse down to zero, reads the legs (bit 4) and arms (bit 5), and outside VPinMAME writes "
				"switch 33 as 1 at position zero on every non-zero phase write. A simulation model, not physical authority."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/whitestar.json", "revision": "repository",
			"locator": "Whitestar public switch (-3..0, 1-64, 81-88), DIP 1-8, solenoid 1-50, lamp and GI 0 address rules and their notes",
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-31T04:08:02Z",
			"locator": (
				"IPDB machine 4983 'Elvis®' (Stern Pinball, August 2004, model I-0084, Stern Whitestar (modified), design by Steve "
				f"Ritchie), read from the Internet Archive capture {IPDB_CAPTURE_URL} because the live site is Cloudflare-gated; the "
				f"capture is retained gzip-compressed as served (SHA-256 {IPDB_CAPTURE_GZIP_SHA256}) and decompressed (the recorded hash) "
				"under pinmame-manuals/by-machine/stern.elvis.2004/ipdb-archive. Its Notable Features line says 'Flippers (3)', which the "
				"manual's four-flipper wiring diagram, coil chart and the ROM's coil test contradict; the record follows the manual."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", "IPDB machine page 4983, Internet Archive capture of 2026-10-16", reviewed=False)],
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": MANUAL_URL, "original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256, "acquired_at": "2026-08-31T12:00:00Z", "source_id": "official-stern",
			"locator": (
				"Stern Elvis service manual (185 pages; manual part number 780-5084-00 per its Appendix C, production start AUG 04), "
				"downloaded from Stern's own manuals page (https://www.sternpinball.com/manuals/), local cache "
				"manufacturer.official-stern.stern.elvis-2004.2026-08-31, retained as "
				"external:pinmame-manuals/by-machine/stern.elvis-2004/Elvis_Manual.pdf. PDF 5-9 are the front-matter Dr. Pinball sheets "
				"(DR. 3 diagnostic aids and DIP settings, DR. 4 switch grid and locations, DR. 5 lamp grid and locations, DR. 6 coil chart, "
				"DR. 7 coil and flash locations), PDF 42-43 and 63 the service menu, PDF 82-117 the parts and major assemblies (printed "
				"pages = PDF - 19), PDF 118-128 the wiring diagrams and opto boards and PDF 168-172 the appendices."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Stern Pinball, Inc.",
			"excerpts": _manual_excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "known_working": True,
			"uri": "external:pinmame-vpx-sources/stern/elvis-2004/" + quote(TABLE_NAME),
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				"Retained Elvis VPX recreation, table version 1.0.2 (info.json: jpsalas, 16.11.2017, 'Elvis and Hound dog objects by Steve "
				f"Paradis'). Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and "
				f"y/{PLAYFIELD_HEIGHT:g}. Geometry authority only for the objects its embedded script binds; the placement seed "
				"tools/seeds/stern/elvis-2004-spatial.json lists them. Retained by copying the contributor's table collection file "
				"(modified 2020-01-20T01:38:34Z) into the working root."
			),
			"acquired_at": "2026-08-31T06:38:44Z",
			"license": "NOASSERTION", "attribution": "jpsalas (table author); Elvis and Hound Dog objects by Steve Paradis", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "known_working": True,
			"uri": "external:pinmame-vpx-sources/stern/elvis-2004/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256,
			"locator": (
				"The retained table's embedded script as vpxtool extracts it; the table ships no sidecar. Runtime authority for controller "
				"callbacks: Const cGameName = \"elvis\" with UseSolenoids = 1, UseLamps = 0 and UseGI = 0, LoadVPM \"01560000\", "
				"\"SEGA.VBS\", 3.26, .HandleMechanics = 0, the bsTrough/bsLock ball stacks, the bsJail/bsUpper saucers, the dtBankL drop "
				"targets, the mMag magnet, the plungerIM impulse plunger, the mElvis mech, the SolCallback table, the lamp faders and the "
				"switch handlers. Known table defects: 64 is pulsed to 1 where the ROM reads a hit at 0; 55 is written only through an "
				"undefined keyUpperLeft; switch 10 has no object; no callback reads 13 or 14 and no key writes 88; the Elvis mech follows "
				"Q25 alone; Q24 plays a knocker. Extracted from the retained table with vpxtool git:v0.33.3."
			),
			"acquired_at": "2026-10-31T03:21:13Z",
			"license": "NOASSERTION", "attribution": "jpsalas (table author); Elvis and Hound Dog objects by Steve Paradis", "rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment line of the embedded script that binds the controller, with its line number", credit=QUOTE_CREDIT)],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/elvis-2004/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under the vpxtool extraction "
				f"'{EXTRACTION_RELATIVE_PATH.as_posix()}'; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table at 2026-10-31T03:21:12Z; the "
				f"manifest was written at 2026-10-31T05:05:32Z. Bounds are {TABLE_BOUNDS}."
			),
			"acquired_at": "2026-10-31T03:21:12Z",
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_CORPUS_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_REVISION}/" + quote(CORPUS_NAME, safe="/"),
			"revision": VPXTABLE_REVISION, "sha256": CORPUS_SHA256,
			"locator": (
				"Pinned corpus script of a sound and lighting modification of the same VPX 1.0.2 table (header 'Elvis - Stern 2004', "
				"'VPX 1.0.2 by JPSalas July 2017'), Const cGameName = \"elvis\" (line 33), LoadVPM \"01560000\", \"SEGA.VBS\", 3.26 "
				"(line 47), UseSolenoids = 2 (line 53), vpmNudge.TiltSwitch = 56 (line 94), bsTrough.InitSw 0, 14, 13, 12, 11 (line 101), "
				"mElvis Sol1 = 25 and AddSw 33, 0, 0 (lines 165 and 168), the same keyUpperLeft writes of 55 (lines 191 and 198), "
				"SolCallBack(19) = \"SolHotelDoor\" (line 258), the PulseSw 15 in SolTrough (line 264), the PulseSw 64 (line 437) and "
				"GICallback (line 791). It corroborates the retained script's bindings without being independent of it."
			),
			"license": "NOASSERTION", "attribution": f"Authors credited in {CORPUS_NAME} and repository contributors",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-review-artifacts/vpm-script-libs/sega.vbs",
			"original_filename": "sega.vbs", "sha256": VPM_SEGA_SHA256,
			"locator": (
				"VPinMAME Sega/Stern Whitestar script library the retained table loads, copied from the contributor's Visual Pinball Scripts "
				f"folder beside the core.vbs it executes (SHA-256 {VPM_CORE_SHA256}). It defines GameOnSolenoid = 15, swBlack 0 / swGreen -1 / "
				"swRed -2 / swMemoryProtect -3, swStartButton 54, swTilt 56, swSlamTilt 55, swCoin3 4 / swCoin1 5 / swCoin2 6, swLRFlip 82, "
				"swLLFlip 84, swURFlip 81 and swULFlip 83; core.vbs defines sLRFlipper 46 and sLLFlipper 48."
			),
			"acquired_at": "2026-10-09T18:43:45Z",
			"license": "NOASSERTION", "attribution": "VPinMAME script authors",
			"excerpts": [_excerpt("vpm-script-library", "sega.vbs constants (lines 20-39) and key handlers (lines 71-105); core.vbs flipper constants (lines 2862-2865)", credit=QUOTE_CREDIT)],
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/elvis.zip", "revision": "5.00", "sha256": ROM_ARCHIVE_SHA256,
			"locator": (
				"User-authorized read-only archive whose members match the pinned elvis ROM set (elvscpua.500 CRC aae9d65d, elvsdspa.500 "
				"CRC 76a672cb, sound elvis.u7 CRC 1df6c1b5, voice elvis.u17/u21/u36/u37 CRCs ff032897, c3c19a40, e98f0dc9, 88ba0966); used "
				"to identify the ROM the harness booted. ROM bytes stay external."
			),
			"license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external",
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				f"Nine hash-pinned LibPinMAME harness runs of elvis (5.00) (library SHA-256 {RUNTIME_LIBRARY_SHA256[:12]}..., built from "
				f"{PINMAME_REVISION[:8]}) from empty NVRAM with built-in mechanisms off: {described}. Scenarios under "
				"tools/harness-scenarios/whitestar; tools/elvis_runtime_evidence.py derives the committed per-step transitions from the "
				"retained runs, and the service-test runs' DMD frames as diagnostic snapshots whose readings "
				"tools/seeds/stern/elvis-2004-frame-readings.json pins by pixel SHA-256. LibPinMAME's elvis.c writes switch 33 itself "
				"from the stepper phases; the evidence reports those writes as the emulator's, never as ROM observations."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Elvis", "manufacturer": "Stern", "year": 2004, "kind": "physical_pinball", "model_number": "I-0084",
			"ipdb_id": 4983, "opdb_id": "G4qbX-MJw5r",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
				"mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.whitestar", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": [],
		"sources": source_records(),
		"knowledge": {"path": "knowledge/stern/elvis-2004.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Elvis device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		named = mechanism["actuators"] + mechanism["sensors"] + [sensor for position in mechanism.get("positions", []) for sensor in position["sensors"]]
		unknown = [item for item in named if item not in known]
		if unknown:
			raise RuntimeError(f"Elvis mechanism {mechanism['id']} names unknown devices: {unknown}")
	return definition


# --- Extraction manifest -------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Elvis retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest", "version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Elvis extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Elvis retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Elvis retained extraction manifest does not match the files under the extraction")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Elvis retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


# --- Spatial report ------------------------------------------------------------------------------------
def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	devices = definition["inputs"] + definition["outputs"]
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable_count = 0
	for device in devices:
		spatial = device.get("spatial")
		if spatial is None:
			if device["availability"] in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_count += 1
			continue
		statuses[spatial["status"]].append(device["id"])
	return {
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield", "source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:g}; 0=left, 1=right", "y": f"y/{PLAYFIELD_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256, "embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256,
			"spatial_seed_sha256": _file_sha256(SPATIAL_SEED_PATH),
		},
		"extraction": {
			"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "total_bytes": EXTRACTION_TOTAL_BYTES, "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/stern/elvis-2004/extracted-vpxtool.manifest.json", "source_ref": VPX_EXTRACTION_SOURCE,
		},
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": (
				"The centre of the VPX object the embedded script binds to each switch (trigger, spinner, hit target, kicker, slingshot "
				"wall, bumper, primitive). The trough switches 11-14 and the stacking opto 15, which the table does not model, are "
				"projected onto the release kicker BallRelease; the home switch 33 onto the figure's stand primitive pStand, which the "
				"mech moves; each end-of-stroke contact onto its flipper."
			),
			"lamp": "None: every lamp the table fades is an insert overlay Light with no bulb or a Flasher sprite, so no lamp is placed.",
			"solenoid": (
				"The kicker, slingshot wall, bumper, flipper, trigger, gate or wall the script fires; the drop-target reset on the mean of "
				"its bank's five targets; the stepper phases 25-28 and the legs and arms coils 29 and 30 on the stand primitive pStand; "
				"flashers 22 and 32 on the script-driven glow Lights centred on their modelled Flupper domes. Flasher 23 is not "
				"placed: its faded Lights f23 and f23a show no bulb mesh and sit on no modelled socket."
			),
			"gi": (
				f"The {len(_spatial_seed()['gi']['0'])} members of the table's aGiLights collection that draw their bulb mesh, after "
				"collapsing co-located Lights; observed only, without per-string assignment. Members that show no bulb mesh sit on no "
				"bulb and are not placed."
			),
		},
		"unresolved_geometry": [
			"Every lamp 1-78 is unplaced: the table draws 1-59, 63 and 64 with insert overlay Lights that have no bulb and 57-78 with Flasher sprites; placing them needs the lamp location drawing (DR. 5) fitted to the table by a callout check, or playfield photographs.",
			"The back-panel flashers 20 and 21, the back-panel lamps 60-62 and 73-78 and the back panel's ten G.I. bulbs stand on the back panel behind the playfield's rear edge; the table models the flashers as Flupper domes on that plane outside the playfield bounds, so they need the back-panel elevation rule and a drawing fit.",
			"The Elvis spot light 31 is drawn by the table only with Flasher sprites; DR. 7 draws it right of the stepper callouts.",
			"The upper right flipper flasher 23 (two #906 bulbs) is drawn by the table only with bulb-mode Lights that show no bulb mesh and sit on no modelled socket; DR. 7 draws it twice along the right edge.",
			"The shooter lane exit switch 10 has no table object.",
			"The trough switches 11-15, the home switch 33, the stepper phases 25-28, the legs and arms coils 29 and 30, the drop-bank reset 3 and the end-of-stroke switches 81 and 83 are projections onto mechanism objects.",
			"No placement has been checked against the factory location drawings (DR. 4, DR. 5, DR. 7) by a callout fit, so every placement stays observed.",
			(
				f"The table draws {len(_spatial_seed()['gi']['0'])} G.I. bulbs against the 48 the G.I. page counts; "
				f"{len(_spatial_seed()['gi_without_bulb']['0'])} more aGiLights members show no bulb mesh and are not placed, and "
				"matching the placed ones to the drawing's circuit discs is not done."
			),
		],
		"promotion_decision": "partial: unplaced lamps and back-panel devices, projections, and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Elvis (Stern, 2004) spatial blockers", "",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest `{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.", "",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g} rounded to at most six places.", "",
		"## Placement status", "",
	]
	for name, items in report["placement_status"].items():
		lines.append(f"- `{name}`: {len(items)} devices")
	lines += [f"- controlled `not_applicable` records: {report['not_applicable_device_count']}", f"- used devices with no placement record: {len(report['without_placements'])}", ""]
	lines += [f"  - `{item}`" for item in report["without_placements"]]
	lines += ["", "## Projection classes", ""]
	lines += [f"- **{name}:** {text}" for name, text in report["projection_classes"].items()]
	lines += ["", "## Unresolved physical geometry", ""]
	lines += [f"- {item}" for item in report["unresolved_geometry"]]
	lines += ["", "## Promotion decision", "", report["promotion_decision"], ""]
	return "\n".join(lines)


# --- Generation ----------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready Elvis artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Elvis author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"Elvis deterministic artifact drift: {path}")
	print("Elvis definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"Elvis extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Elvis retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
