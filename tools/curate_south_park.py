"""Curate the physical Sega South Park (1999) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived
fact as a literal and reads one committed seed, the placements (the retained table's object coordinates, rebuilt by
tools/south_park_spatial_seed.py), so regeneration reproduces the canonical artifact byte-for-byte without reading the
external evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only path that writes the definition,
its knowledge note and its spatial report.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "sega.south-park.1999"
PARTIAL_PATH = ROOT / "machines/partial/sega/south-park-1999.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/sega/south-park-1999.json"
KNOWLEDGE_PATH = ROOT / "knowledge/sega/south-park-1999.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/sega/south-park-1999.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/sega/south-park-1999-spatial.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/sega/south-park-1999.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/sega/south-park-1999.md"
RUNTIME_103_PATH = "evidence/runtime/whitestar/south-park-sprk-103-stacking-opto-and-gameplay.json"
RUNTIME_096_PATH = "evidence/runtime/whitestar/south-park-sprk-096-gameplay.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = "pinmame.catalog.46e1a01a0f73"
CORE_SOURCE = "pinmame.core.46e1a01a0f73"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
IDENTITY_SOURCE = "identity.sega.south-park.1999"
MANUAL_SOURCE = "manual.sega.south-park.1999"
VPX_TABLE_SOURCE = "vpx-table.south-park-knorr-1-3"
VPX_SCRIPT_SOURCE = "vpx-script.south-park-knorr-1-3"
VPX_EXTRACTION_SOURCE = "vpx-extraction.south-park-knorr-1-3"
VPX_CORPUS_SOURCE = "vpx-script.51b7c24a7b284174"
VPM_LIBRARY_SOURCE = "vpm-script-library.sega-vbs"
RUNTIME_SOURCE = "runtime.south-park.sprk-103"
RUNTIME_096_SOURCE = "runtime.south-park.sprk-096"
ROM_SOURCE = "rom.sega.south-park.1-03"
ROM_096_SOURCE = "rom.sega.south-park.0-96"
RUNTIME_LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "0a2e3487cf679d8f33e1553ae9973e7023786e7bdebee8245a3d91494d14645e"
ROM_096_ARCHIVE_SHA256 = "6d50f03ef078146e07a03333c4c4cf73d9e244eb44d393f4e73d34faee9334c5"
# Retained harness run directory -> SHA-256 of its manifest.json (tools/south_park_runtime_evidence.py pins the same values).
RUN_MANIFESTS = {
	"sprk-stacking-opto": "be7e7c65c9e1b17361bf90669389efa50412b45f0aa493f614c0352f73fe2ea3",
	"sprk-103-gameplay": "fdf0355469d9fd8243c06d0be7afa6a5de97c3beada816ce491854d6477bacc2",
	"sprk-096-gameplay": "e0015636f2b4e6c63376b07fe947ae4d1b0538aef84f56e4b1289ebce3a6aed3",
}

TABLE_NAME = "South Park (Sega 1999) 1.3.vpx"
TABLE_SHA256 = "39075dcb6ca5fb8f164a9d48b6e4b393fef85eae3607892f19f28318a4f8d1a8"
SCRIPT_SHA256 = "63881ced8ea42097d1dee146ee2df7b752160dbd9f04bbfd826b90b513e408bf"
CORPUS_SCRIPT_SHA256 = "51b7c24a7b28417481b858ad2fba2b13021f0cad8c2f0cba7303b0bfef500387"
VPX_CORPUS_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
MANUAL_NAME = "Sega_1999_South_Park_Manual_English.pdf"
MANUAL_SHA256 = "c25723bfc9bb8726c12b1fc3f9a6d74df60ebe8ce7da1937e06a38ace1b59f0a"
IPDB_PAGE_SHA256 = "9c5bd74dcd5cae756b2330359373ec00017500e65fb81c9feb03a461ec45f6e5"
VPM_SEGA_SHA256 = "d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

EXTRACTION_FILE_COUNT = 884
EXTRACTION_TOTAL_BYTES = 199952552
EXTRACTION_MANIFEST_SHA256 = "aae0b1258026105af3e02909e77dbf9d258be8138705ea40968e68acbb2e512c"
EXTRACTION_RELATIVE_PATH = Path("sega/south-park-1999/v1-3/South Park (Sega 1999) 1.3")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("sega/south-park-1999/v1-3/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"
MANUALS_DIRECTORY = f"pinmame-manuals/by-machine/{MACHINE_ID}/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=4444"
IPDB_WAYBACK_URL = "https://web.archive.org/web/20261016080406id_/https://www.ipdb.org/machine.cgi?id=4444"
MANUAL_URL = "https://www.ipdb.org/files/4444/" + MANUAL_NAME
MANUAL_WAYBACK_URL = "https://web.archive.org/web/20221024013642id_/" + MANUAL_URL
EXCERPT_CREDIT = "curator, read from the rendered page"
QUOTE_CREDIT = "curator, quoted from the source file"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("sprk_090", "sprk_096", "sprk_103")
BASE_DRIVER_NOTE = (
	"segames.c builds every South Park driver from one init_sprk (INITGAME(sprk, GEN_WS, se_dmd128x32, 0): no auxiliary "
	"board) and the same de_mSES1 machine driver, so the controller routing, lamp columns and display are identical; "
)
DRIVER_NOTES = {
	"sprk_103": (
		"CPU 1.03 (spkcpu.103) with display 1.01 and the 1.00 sound set: the production firmware the retained table loads "
		"(cGameName = \"sprk_103\"). MACHINE_INIT(se) gives only this set the fast-flip byte at CPU RAM 0x00, so only sprk_103 "
		"publishes the game-on state at public 15; the harness runs saw it rise when a ball was served and fall at the drain."
	),
	"sprk_096": (
		"CPU 0.96 (spkcpu.096) with display 1.01 and the 0.90 sound set, a prototype IPDB lists as 'Prototype (Swearing) ROMs - "
		"(.96 - More completed animations)'. MACHINE_INIT(se) sets no fast-flip byte for it, so public 15 never rises; the "
		"gameplay harness run otherwise drew the same switch-to-coil responses as sprk_103."
	),
	"sprk_090": (
		"CPU 0.90 (spkcpu.090) with display 0.90 (spdspa.090) and the 0.90 sound set, the earlier prototype IPDB lists as "
		"'Prototype (Swearing) Roms (.90)'. It runs on the same hardware. No fast-flip byte, so public 15 never rises. Not exercised: the authorized ROM "
		"archive's sprk_090 set carries spdspa.101 in place of spdspa.090, so it does not load as the driver declares it."
	),
}
DRIVER_COMPATIBILITY = {"sprk_103": "identical", "sprk_096": "identical", "sprk_090": "identical"}


# --- Switch data -------------------------------------------------------------------------------------
# address -> (label, grid name, mounting class, part cell, switch type, availability, roles, pulse)
SWITCHES: dict[int, tuple[str, str, str, str, str, str, tuple[str, ...], bool]] = {
	1: ("Left Cabinet Button (UK Only)", "LEFT BUTTON (UK ONLY)", "on Cabinet side", "180-5160-00", "button", "optional", ("cabinet.uk-button-left",), False),
	2: ("4th Coin Slot", "4TH COIN SLOT", "On Coin Door", "180-5024-00", "other", "optional", ("cabinet.coin.fourth",), True),
	3: ("6th Coin Slot", "6TH COIN SLOT", "On Coin Door", "Future Use", "other", "optional", ("cabinet.coin.sixth",), True),
	4: ("Right Coin Slot", "RIGHT COIN SLOT", "On Coin Door", "180-5024-00", "other", "used", ("cabinet.coin.right",), True),
	5: ("Center Coin Slot / DBA", "CENTER COIN SLOT / DBA", "On Coin Door", "180-5024-00", "other", "used", ("cabinet.coin.center",), True),
	6: ("Left Coin Slot", "LEFT COIN SLOT", "On Coin Door", "180-5024-00", "other", "used", ("cabinet.coin.left",), True),
	7: ("5th Coin Slot", "5TH COIN SLOT", "On Coin Door", "Future Use", "other", "optional", ("cabinet.coin.fifth",), True),
	8: ("Right Cabinet Button (UK Only)", "RIGHT BUTTON (UK ONLY)", "on Cabinet side", "180-5160-00", "button", "optional", ("cabinet.uk-button-right",), False),
	10: ("5-Ball Trough 1 (Left)", "5-BALL TROUGH #1 (LEFT)", "Under P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	11: ("5-Ball Trough 2", "5-BALL TROUGH #2", "Under P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	12: ("5-Ball Trough 3", "5-BALL TROUGH #3", "Under P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	13: ("5-Ball Trough 4", "5-BALL TROUGH #4", "Under P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	14: ("5-Ball Trough VUK Opto", "5-BALL TROUGH VUK OPTO", "Under P/F", "BOT TRANS 520-5173-00 / BOT REC 520-5174-00", "opto", "used", ("ball.position",), False),
	15: ("5-Ball Stacking Opto", "5-BALL STACKING OPTO", "Under P/F", "TOP TRANS 520-5173-00 / TOP REC 520-5174-00", "opto", "used", ("ball.path",), False),
	16: ("Shooter Lane", "SHOOTER LANE", "Under P/F", "180-5157-00", "microswitch", "used", ("ball.position",), False),
	17: ("Left 5-Bank Bottom", "LEFT 5-BANK BOTTOM", "Under P/F", "500-6139-09R", "leaf", "used", (), True),
	18: ("Left 5-Bank 2", "LEFT 5-BANK #2", "Under P/F", "500-6139-09R", "leaf", "used", (), True),
	19: ("Left 5-Bank 3", "LEFT 5-BANK #3", "Under P/F", "500-6139-09R", "leaf", "used", (), True),
	20: ("Left 5-Bank 4", "LEFT 5-BANK #4", "Under P/F", "500-6139-09R", "leaf", "used", (), True),
	21: ("Left 5-Bank Top", "LEFT 5-BANK TOP", "Under P/F", "500-6139-09R", "leaf", "used", (), True),
	22: ("Center 3-Bank Left", "CENTER 3-BANK LEFT", "Under P/F", "500-6138-04R", "leaf", "used", (), True),
	23: ("Center 3-Bank Middle", "CENTER 3-BANK MIDDLE", "Under P/F", "500-6228-02", "leaf", "used", (), True),
	24: ("Center 3-Bank Right", "CENTER 3-BANK RIGHT", "Under P/F", "500-6138-04", "leaf", "used", (), True),
	25: ("Right Ramp Enter", "RIGHT RAMP ENTER", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	26: ("Right Ramp Exit", "RIGHT RAMP EXIT", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	34: ("Right 3-Bank Bottom", "RIGHT 3-BANK BOTTOM", "Under P/F", "500-6075-11R", "leaf", "used", (), True),
	35: ("Right 3-Bank Middle", "RIGHT 3-BANK MIDDLE", "Under P/F", "500-6075-11R", "leaf", "used", (), True),
	36: ("Right 3-Bank Top", "RIGHT 3-BANK TOP", "Under P/F", "500-6075-11R", "leaf", "used", (), True),
	37: ("Pop Bumper Target Left", "POP BUMPER TARGET LT", "Under P/F", "500-6139-11", "leaf", "used", (), True),
	38: ("Pop Bumper Target Right", "POP BUMPER TARGET RT", "Under P/F", "500-6139-11", "leaf", "used", (), True),
	42: ("Kenny Opto", "KENNY OPTO", "Under P/F", "TRANS 520-5082-00 / REC 520-5083-01", "opto", "used", ("ball.path",), True),
	43: ("Under-Trough (Toilet)", "UNDER- TROUGH (TOILET)", "Under P/F", "180-5057-00", "microswitch", "used", ("ball.path",), True),
	44: ("Under-Trough (Kenny)", "UNDER- TROUGH (KENNY)", "Under P/F", "180-5057-00", "microswitch", "used", ("ball.path",), True),
	45: ("Super VUK", "SVUK", "Under P/F", "180-5052-00", "microswitch", "used", ("ball.position",), False),
	46: ("Top VUK", "VUK", "Under P/F", "180-5116-01", "microswitch", "used", ("ball.position",), False),
	47: ("Left Orbit (to VUK)", "LEFT ORBIT (TO VUK)", "Under P/F", "500-6227-02", "microswitch", "used", ("ball.path",), False),
	48: ("Under-Trough Super VUK", "UNDER- TROUGH SVUK", "Under P/F", "180-5057-00", "microswitch", "used", ("ball.path",), True),
	49: ("Left Turbo Bumper", "LEFT TURBO BUMPER", "Under P/F", "180-5015-03", "leaf", "used", (), True),
	50: ("Right Turbo Bumper", "RIGHT TURBO BUMPER", "Under P/F", "180-5015-03", "leaf", "used", (), True),
	51: ("Bottom Turbo Bumper", "BOTTOM TURBO BUMPER", "Under P/F", "180-5015-03", "leaf", "used", (), True),
	54: ("Start Button", "START BUTTON", "Cabinet Front", "500-6090-02", "button", "used", ("cabinet.start",), False),
	55: ("Slam Tilt", "SLAM TILT", "On Coin Door", "180-5022-00", "tilt", "used", ("cabinet.slam-tilt",), False),
	56: ("Plumb Bob Tilt", "PLUMB BOB TILT", "Inside Cabinet", "HANGER 535-5319-00, CONTACT 535-7563-01", "tilt", "used", ("cabinet.tilt",), False),
	57: ("Left Outlane", "LEFT OUTLANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	58: ("Left Return Lane", "LEFT RETURN LANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	59: ("Left Slingshot", "LEFT SLINGSHOT", "Under P/F", "180-5054-00", "leaf", "used", (), True),
	60: ("Right Outlane", "RIGHT OUTLANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	61: ("Right Return Lane", "RIGHT RETURN LANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	62: ("Right Slingshot", "RIGHT SLINGSHOT", "Under P/F", "180-5054-00", "leaf", "used", (), True),
}
UNUSED_SWITCHES = (9, 27, 28, 29, 30, 31, 32, 33, 39, 40, 41, 52, 53, 63, 64)
DOTS_SWITCHES = (16, 45, 46)
MATRIX_DRIVE = [("GRN-BRN", "CN5-P1"), ("GRN-RED", "CN5-P3"), ("GRN-ORG", "CN5-P4"), ("GRN-YEL", "CN5-P5"), ("GRN-BLK", "CN5-P6"), ("GRN-BLU", "CN5-P7"), ("GRN-VIO", "CN5-P8"), ("GRN-GRY", "CN5-P9")]
MATRIX_RETURN = [("WHT-BRN", "CN7-P9", "U400"), ("WHT-RED", "CN7-P8", "U400"), ("WHT-ORG", "CN7-P7", "U400"), ("WHT-YEL", "CN7-P6", "U400"), ("WHT-GRN", "CN7-P5", "U401"), ("WHT-BLU", "CN7-P3", "U401"), ("WHT-VIO", "CN7-P2", "U401"), ("WHT-GRY", "CN7-P1", "U401")]
# The printed page-15 switch table's longer name where it differs from the grid.
PAGE15_NAMES = {
	17: "LEFT 5-BANK BOT. (Prp. Sq. Rear Mnt.)", 21: "LEFT 5-BANK TOP (Purp. Sq. Rear Mnt.)", 22: "CENTER 3-BANK LT. (Grn. Nar. Rear Mnt.)",
	23: "CENTER 3-BANK MID. (Red Rect. Fwd.)", 24: "CENTER 3-BANK RT. (Grn. Narrow Fwd.)", 34: "RT 3-BANK BOT. (Flo.Grn. Rnd. Rear Mnt.)",
	37: "POP BUMPER TARGT LT (Flo. Grn. Sq.)", 42: "KENNY (OPTO)", 45: "SVUK (Super Vertical Up-Kicker Switch)", 46: "VUK (Vertical Up-Kicker Switch)",
	54: "START BUTTON (Red)", 55: "SLAM TILT (On Coin Door)", 57: "LEFT OUTLANE (Rt. Mount R/O)", 59: "LEFT SLINGSHOT (Double-Switch)",
	62: "RIGHT SLINGSHOT (Double-Switch)",
}
# What the retained 1.3 table's embedded script does with each address (line numbers of that script).
SWITCH_SCRIPT = {
	10: "bsTrough.InitSw 0, 14, 13, 12, 11, 10 with Balls = 5 (lines 111-117): a cvpmBallStack holding 10 at 1 while a ball occupies that position",
	11: "bsTrough.InitSw 0, 14, 13, 12, 11, 10 with Balls = 5 (lines 111-117)",
	12: "bsTrough.InitSw 0, 14, 13, 12, 11, 10 with Balls = 5 (lines 111-117)",
	13: "bsTrough.InitSw 0, 14, 13, 12, 11, 10 with Balls = 5 (lines 111-117)",
	14: "bsTrough.InitSw 0, 14, 13, 12, 11, 10 (lines 111-117): 14 is the exit position the trough up-kicker empties, held at 1 while a ball waits there",
	15: "never written: SolRelease's 'If bsTrough.Balls = 5 Then vpmTimer.PulseSw 15' is commented out (line 156), so the table drops the stacking-opto edge",
	16: "Trigger sw16 holds 16 while the ball sits on it (lines 802-803)",
	17: "Wall T17's Hit handler pulses 17 (line 844)",
	18: "Wall T18's Hit handler pulses 18 (line 846)",
	19: "Wall T19's Hit handler pulses 19 (line 848)",
	20: "Wall T20's Hit handler pulses 20 (line 850)",
	21: "Wall T21's Hit handler pulses 21 (line 852)",
	22: "Wall T22's Hit handler pulses 22 (line 856)",
	23: "Wall T23's Hit handler pulses 23 (line 858)",
	24: "Wall T24's Hit handler pulses 24 (line 860)",
	25: "Trigger sw25 holds 25 while the ball sits on it (lines 805-806)",
	26: "Trigger sw26 holds 26 while the ball sits on it (lines 808-809)",
	34: "Wall T34's Hit handler pulses 34 (line 864)",
	35: "Wall T35's Hit handler pulses 35 (line 866)",
	36: "Wall T36's Hit handler pulses 36 (line 868)",
	37: "Wall T37's Hit handler pulses 37 (line 872)",
	38: "Wall T38's Hit handler pulses 38 (line 874)",
	42: "Trigger sw42 holds 42 while the ball passes (lines 820-821)",
	43: "ToiletKicker_Hit pulses 43 and hands the ball to the super VUK 2.4 s later (lines 592-598); ToiletKicker is enabled only while Q5 holds the seat lid up",
	44: "KennyKickerHole through KennyKickerHole5 pulse 44 and hand the ball to the super VUK 2 s later (lines 434-531)",
	45: "cvpmBallStack SuperVuk (InitSw 0, 45; InitKick sw45, lines 130-135) holds 45 while a ball waits in the super VUK",
	46: "cvpmSaucer TopVuk (InitSaucer sw46, 46, lines 121-125) holds 46 while a ball waits in the top VUK",
	47: "Trigger sw47 holds 47 while the ball sits on it (lines 824-825)",
	48: "CartmanKickerHole through CartmanKickerHole7 pulse 48 and hand the ball to the super VUK 1.2 s later (lines 203-263)",
	49: "LeftBumper's Hit handler pulses 49 (line 894)",
	50: "RightBumper's Hit handler pulses 50 (line 897)",
	51: "BottomBumper's Hit handler pulses 51 (line 900)",
	57: "Trigger sw57 holds 57 while the ball sits on it (lines 827-828)",
	58: "Trigger sw58 holds 58 while the ball sits on it (lines 830-831)",
	59: "LeftSlingShot_Slingshot pulses 59 (line 937)",
	60: "Trigger sw60 holds 60 while the ball sits on it (lines 833-834)",
	61: "Trigger sw61 holds 61 while the ball sits on it (lines 836-837)",
	62: "RightSlingShot_Slingshot pulses 62 (line 919)",
}
# Matrix switches the gameplay harness runs closed, with the outputs the ROM drove in response (step labels in the evidence).
GAMEPLAY_RESPONSE = {
	16: "a ball resting on it raised the game-on state 15 (sprk_103 only) and flashed 25-29; the ball leaving it flashed 29 and 32",
	22: "closing it once flashed 31 (Mr. Hankey/toilet)",
	23: "closing it once flashed 31 (Mr. Hankey/toilet)",
	24: "closing it once flashed 31 (Mr. Hankey/toilet)",
	25: "closing it once flashed 28 (Kyle)",
	26: "closing it once flashed 28 (Kyle) and blinked the G.I.",
	37: "closing it once flashed the pop flashers 7",
	38: "closing it once flashed the pop flashers 7",
	42: "closing it once fired the Kenny pivot 14, shook Kenny with 19 and 20 alternately, nine to ten pulses each in the step's window, and flashed 30",
	44: "closing it once, with the super VUK empty, fired the super VUK 3; sprk_103 also shook Kenny with 19 and 20 and flashed 30, and sprk_096 flashed 32",
	45: "a ball held on it drew repeated super-VUK kicks (3) and the super-VUK flasher 32",
	46: "a ball held on it flashed 30; sprk_103 fired the top VUK 4 once some seconds later, while sprk_096 fired it only during a later step",
	47: "closing it once flashed 25 (Stan)",
	48: "closing it once, with the super VUK empty, fired the super VUK 3 and flashed 32",
	49: "closing it once fired the left turbo bumper 9 and the pop flashers 7",
	50: "closing it once fired the right turbo bumper 10 and the pop flashers 7",
	51: "closing it once fired the bottom turbo bumper 11 and the pop flashers 7",
	57: "closing it once flashed 25 and blinked the G.I.",
	58: "closing it once flashed 25",
	59: "closing it once fired the left slingshot 12 and flashed 25",
	60: "closing it once flashed 29 and blinked the G.I.",
	61: "closing it once flashed 29",
	62: "closing it once fired the right slingshot 17 and flashed 29",
}
GAMEPLAY_QUIET = (17, 18, 19, 20, 21, 34, 35, 36, 43)


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
		if entry.get("projection"):
			text += f" (projection: {entry['projection']})"
		if entry.get("note"):
			text += f" ({entry['note']})"
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


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	identifier = switch_id(address)
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
	notes = f"Printed switch-matrix drive column {column + 1}, return row {row + 1}."
	if address in UNUSED_SWITCHES:
		notes += (
			" The Switch Matrix Grid (DR. 4) prints this cell NOT USED, shaded black, with no part number; the page note lists it "
			"under 'Not used: 9, 27-33, 39-41, 52-53, 63-64', the location drawing marks no switch with this number, and the "
			"retained script never writes it."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE),
			aliases=aliases, normally_closed=False, pulse=False, physical={"notes": notes}, wiring=_switch_wiring(address),
			spatial=not_applicable("unused", MANUAL_SOURCE),
		)
	label, printed, mounting, part, switch_type, availability, roles, pulse = SWITCHES[address]
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": switch_type}
	if re.fullmatch(r"\d{3}-\d{4}-\d{2}R?", part):
		physical["assembly_part_number" if part.startswith("500-") else "part_number"] = part
	notes += f' The grid prints "{printed}" with mounting class "{mounting}"; the page-15 switch table gives part "{part}"'
	notes += f' and names it "{PAGE15_NAMES[address]}".' if address in PAGE15_NAMES else "."
	if part.endswith("R"):
		notes += " The trailing R marks a reverse (rear) mounted target and switch actuator."
	if address in DOTS_SWITCHES:
		notes += " The grid tags the cell DOTS (diode on terminal strip)."
	if address in (59, 62):
		physical["quantity"] = 2
		notes += " Two parallel stack-blade contacts (180-5054-00, two per Slingshot Assembly 500-5849-01) share this matrix address."
	if address in (14, 15):
		notes += (
			" The page note: 'Sw.14/Sw.15 have both REC/TRANS on 1 board respectively'. Whitestar's switch_r hands the CPU "
			"~core_getSwCol and the driver's invSw is zero, so public 1 is the CPU's closed-contact reading. The Trough Dual OPTO "
			"boards theory of operation (printed page 89) states the construction: with light on the receiver its output "
			"transistor is off and acts as an open switch; when the beam is blocked it conducts and acts as a closed switch, so the "
			"contact rests open."
		)
	if address == 14:
		notes += " The retained script holds 14 at 1 while a ball waits at the up-kicker."
	if address == 15:
		notes += (
			" The retained script never writes 15. In the stacking-opto harness run, with five balls on 10-14, raising 15 to 1 in "
			"attract mode, lowering it and raising it again drew no coil, so the ROM's attract mode does not act on it; no run "
			"exercised it during a game."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 42:
		notes += (
			" Mounted under the playfield on the OPTO & Bracket (Long) Assembly 500-6242-02-71 (transmitter 520-5082-00, receiver "
			"520-5083-01) at Kenny. Public 1 is a blocked beam: the retained script holds 42 at 1 while the ball passes, and in "
			"the gameplay runs a 1 pulse drew the ROM's Kenny reaction. On Whitestar an opto the script and ROM treat as active "
			"at 1 has a matrix contact that rests open."
		)
	if address in (43, 44, 48):
		notes += (
			" One of three micro switches on the Under-Trough Assembly 500-6385-00-71 (printed page 75), which carries balls from "
			"under the toilet, from under Kenny and from the playfield hole above the super VUK to the super VUK."
		)
	if address in (3, 7):
		notes += " The part cell reads Future Use: the harness position is wired but no coin switch is fitted by default."
	if address == 2:
		notes += " The cabinet wiring diagram (printed page 88) labels this input '4th Coin Slot European Use'."
	if address in (1, 8):
		notes += (
			" UK only: the cabinet wiring diagram's '✻✻✻ UK ONLY ✻✻✻' box draws the EXTRA CABINET BUTTONS (SAV-A-BALL) as N.O. "
			f"switches on GRN-BRN with the {'left on WHT-BRN' if address == 1 else 'right on WHT-GRY'}. That box prints the two CN7 "
			"pin numbers crossed against the grid (WHT-BRN beside pin 1, WHT-GRY beside pin 9); the wire colours and the grid agree, "
			"and the grid's pin is recorded."
		)
	if address == 55:
		notes += " sega.vbs's swSlamTilt = 55 is the key the VPinMAME Slam Tilt key writes; the cabinet wiring diagram draws it on drive 7, return 7."
		refs += (VPM_LIBRARY_SOURCE,)
	if address == 56:
		notes += " sega.vbs's swTilt = 56; the retained script sets vpmNudge.TiltSwitch = swTilt (line 107)."
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE)
	if address == 54:
		notes += " sega.vbs's swStartButton = 54 is what the VPinMAME Start key writes. In the gameplay runs a press after three coins started a game and the ROM kicked the trough up-kicker (1)."
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE)
	if address in (4, 5, 6):
		notes += f" sega.vbs maps its coin keys to {'swCoin3 = 4' if address == 4 else 'swCoin1 = 5' if address == 5 else 'swCoin2 = 6'}."
		refs += (VPM_LIBRARY_SOURCE,)
	if address in SWITCH_SCRIPT:
		notes += f" Retained table script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in GAMEPLAY_RESPONSE:
		notes += f" In the gameplay harness runs, {GAMEPLAY_RESPONSE[address]}."
		refs += (RUNTIME_SOURCE, RUNTIME_096_SOURCE)
	elif address in GAMEPLAY_QUIET:
		notes += " The gameplay harness runs closed it once in a game and the ROM fired no coil or flasher in response, which says nothing against its fitment."
		refs += (RUNTIME_SOURCE, RUNTIME_096_SOURCE)
	if address == 5:
		notes += " In the gameplay runs each coin on 5 pulsed the optional coin-meter output 24 four times and flashed 7."
		refs += (RUNTIME_SOURCE, RUNTIME_096_SOURCE)
	extra: dict[str, Any] = {"aliases": aliases, "normally_closed": False, "pulse": pulse, "wiring": _switch_wiring(address)}
	if roles:
		extra["roles"] = list(roles)
	if address in (10, 11, 12, 13, 14):
		extra["initial_active"] = True
	if any(role.startswith("cabinet.") for role in roles):
		physical["location"] = "coin door" if mounting == "On Coin Door" else "cabinet"
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, availability, refs, physical=physical, **extra)


# address -> (label, printed name, wire, connector, location, part, roles, availability, normally_closed)
DEDICATED = {
	-3: ("Coin Door Memory Protect", "Memory Protect Switch", "BLK-RED", "CN6-P12", "coin door", None, ("cabinet.memory-protect",), "used", False),
	-2: ("Volume / Service Left (Red)", "#6 VOLUME (RED BUTTON) (In Test: LEFT)", "GRY-BLU", "CN6-P8", "coin door", None, ("service.left",), "used", False),
	-1: ("Service Credit / Service Right (Green)", "#7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT)", "GRY-VIO", "CN6-P9", "coin door", None, ("service.right",), "used", False),
	0: ("Begin Test / Service Enter (Black)", "#8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER)", "GRY-BLK", "CN6-P10", "coin door", None, ("service.enter",), "used", False),
	81: ("Right Flipper End-of-Stroke", "#4 RIGHT FLIPPER E.O.S. (End-of-Stroke)", "GRY-YEL", "CN6-P6", "playfield", "180-5149-00", ("flipper.lower.right.eos",), "used", True),
	82: ("Right Flipper Button", "#3 RIGHT FLIPPER BUTTON", "GRY-ORG", "CN6-P4", "cabinet", None, ("flipper.lower.right.button",), "used", False),
	83: ("Left Flipper End-of-Stroke", "#2 LEFT FLIPPER E.O.S (End-of-Stroke)", "GRY-RED", "CN6-P3", "playfield", "180-5149-00", ("flipper.lower.left.eos",), "used", True),
	84: ("Left Flipper Button", "#1 LEFT FLIPPER BUTTON", "GRY-BRN", "CN6-P2", "cabinet", None, ("flipper.lower.left.button",), "used", False),
}
DEDICATED_INPUT = {-2: "DS-6", -1: "DS-7", 0: "DS-8", 81: "DS-4", 82: "DS-3", 83: "DS-2", 84: "DS-1"}


def _dedicated(address: int) -> dict[str, Any]:
	label, printed, wire, connector, location, part, roles, availability, normally_closed = DEDICATED[address]
	name = f"n{-address}" if address < 0 else str(address)
	identifier = f"switch.{name}-{slug(label)}"
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
	if address in DEDICATED_INPUT:
		aliases.append({"namespace": "manual.address", "value": DEDICATED_INPUT[address]})
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": "leaf" if address in (81, 83) else "button" if address != -3 else "microswitch", "location": location}
	if part:
		physical["part_number"] = part
	if address == -3:
		notes = (
			"The cabinet/coin door wiring diagram (printed page 88) draws the Memory Protect Switch from CPU board CN6 pin 12 (BLK-RED) "
			"to ground. se.c's ram_w refuses writes to the protected RAM while public -3 is 1, and sega.vbs names the address "
			"swMemoryProtect; a closed coin door is public -3 at 1 and an open door 0."
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
		notes += " The cabinet wiring diagram draws it among the PORTALS™ SERVICE BUTTONS on the coin door."
	if address in (81, 83):
		notes += (
			" The 2-Flipper Circuit Wiring Diagram (printed page 86) prints the E.O.S. as an N.C. switch on the flipper assembly "
			"(E.O.S. switch 180-5149-00 on Flipper Assemblies 500-5944-14/-04) and explains that it opens about 1/16\" when the "
			"flipper is energized; the CPU re-pulses the coil (40 ms) when it sees the switch close again during a hold, because a "
			"shot forced the bat back. normally_closed is that construction: at rest the contact is closed (public 1) and it opens "
			"(public 0) at the end of the stroke. The driver declares FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L) without FLIP_EOS, so "
			"core_updateSw never writes this bit and the ROM reads whatever the host writes; a recreation that leaves it at 0 only "
			"loses the re-pulse. The retained script never writes it; sega.vbs names this address swURFlip/swULFlip, an "
			"upper-flipper label it writes only when an upper flipper solenoid is registered, which this table does not do."
		)
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE)
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE,)
	elif address in (82, 84):
		notes += (
			f" The flipper column bit PinMAME's core_updateSw copies into the lower-flipper outputs; sega.vbs writes it from the "
			f"{'right' if address == 82 else 'left'} flipper key (swLRFlip = 82, swLLFlip = 84). In the gameplay harness runs, holding it "
			f"made the ROM pulse {'45 and 46' if address == 82 else '47 and 48'}."
		)
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE, RUNTIME_096_SOURCE)
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, availability, refs, aliases=aliases, normally_closed=normally_closed,
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
	items.append(_device(
		"switch.88-not-used-ds-5", "Not Used Dedicated Input DS-5", "switch", SWITCH_GROUP, 88, "unused", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.switch", "value": "88"}, {"namespace": "manual.address", "value": "DS-5"}], normally_closed=False, pulse=False,
		physical={"notes": "dedswitch_r routes the flipper column's upper-flipper button bit to U206 input 5 (DS-5), which the dedicated-switch column prints NOT USED (GRY-GRN, CN6-P7). The driver declares no upper flipper."},
		wiring={"board": "Whitestar CPU/Sound board dedicated-switch input", "drive_wire": "GRY-GRN", "drive_connection": "CN6-P7", "return_component": "U206"},
		spatial=not_applicable("unused", MANUAL_SOURCE),
	))
	for number in range(1, 9):
		used = number <= 5
		items.append(_device(
			f"switch.dip-{number}", f"SW300 Country Selector Bit {number}" if used else f"Unused DIP Bit {number}", "dip_switch", DIP_GROUP, number,
			"used" if used else "unused", (CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": str(number)}],
			physical={"switch_type": "dip", "location": "Whitestar CPU/Sound board", "notes": (
				"se.c's dip_r returns the complement of PinMAME DIP bank 0; sega.vbs's DIP form sets the country code in mask 0x0f (USA 0x00, "
				"UK 0x05, Germany 0x07 and so on)." if used else "Above the bits the country selector uses; nothing reads it.")},
			spatial=not_applicable("dip_switch", CORE_SOURCE),
		))
	return items


# --- Solenoid data -------------------------------------------------------------------------------------
# Q number -> (label, printed name, kind, availability, coil/bulb cell, power wire, power connection, voltage, control wire, control connection)
YV = ("YEL-VIO", "J10-P4/5", 50)
BR = ("BRN", "J7-P1", 20)
OR = ("ORG", "J6-P10", 20)
Q_OUTPUTS: dict[int, tuple[str, str, str, str, str, str, str, int, str, str]] = {
	1: ("Trough Up-Kicker", "TROUGH UP-KICKER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BRN-BLK", "J8-P1"),
	2: ("Auto Launch", "AUTO LAUNCH", "coil", "used", "24-940 / 090-5036-00T", *YV, "BRN-RED", "J8-P3"),
	3: ("Super VUK", "SUPER VUK", "coil", "used", "24-940 / 090-5036-00T", *YV, "BRN-ORG", "J8-P4"),
	4: ("Top VUK", "TOP VUK", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BRN-YEL", "J8-P5"),
	5: ("Toilet Seat Lid", "TOILET SEAT LID", "coil", "used", "23-1100 / 090-5030-00T", *BR, "BRN-GRN", "J8-P6"),
	6: ("Mr. Hankey Latch", "MR. HANKEY LATCH", "coil", "used", "29-1000 / 090-5059-00", *YV, "BRN-BLU", "J8-P7"),
	7: ("Pop Flashers (X4)", "FLASH POPS ✻4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BRN-VIO", "J8-P8"),
	8: ("European Token Dispenser", "EUROPEAN TOKEN DISPENSER", "coil", "optional", "DL4SS / 515-6076-01", *YV, "BRN-GRY", "J8-P9"),
	9: ("Left Turbo Bumper", "LEFT TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-BRN", "J9-P1"),
	10: ("Right Turbo Bumper", "RIGHT TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-RED", "J9-P2"),
	11: ("Bottom Turbo Bumper", "BOTTOM TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-ORG", "J9-P4"),
	12: ("Left Slingshot", "LEFT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "BLU-YEL", "J9-P5"),
	13: ("Mr. Hankey (Down)", "MR. HANKEY (DOWN)", "coil", "used", "23-1100 / 090-5030-00T", *YV, "BLU-GRN", "J9-P6"),
	14: ("Kenny Pivot (Dead)", "KENNY PIVOT (DEAD)", "coil", "used", "22-1080 / 090-5032-00T", *YV, "BLU-BLK", "J9-P7"),
	15: ("Left Flipper", "LEFT FLIPPER (50v RED/YEL)", "coil", "used", "23-1100 / 090-5030-00T", "RED-YEL / GRY-YEL", "J10-P1/2", 50, "ORG-GRY", "J9-P8"),
	16: ("Right Flipper", "RIGHT FLIPPER (50v RED/YEL)", "coil", "used", "23-1100 / 090-5030-00T", "RED-YEL / BLU-YEL", "J10-P1/2", 50, "ORG-VIO", "J9-P9"),
	17: ("Right Slingshot", "RIGHT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "VIO-BRN", "J7-P2"),
	18: ("Top VUK Flasher", "FLASH TOP VUK ✻1", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "VIO-RED", "J7-P3"),
	19: ("Kenny Left", "KENNY LT", "coil", "used", "24-940 / 090-5036-00T", *BR, "VIO-ORG", "J7-P4"),
	20: ("Kenny Right", "KENNY RT", "coil", "used", "24-940 / 090-5036-00T", *BR, "VIO-YEL", "J7-P6"),
	21: ("Left Outlane Ball Deflector (UK Only)", "LT OUTLANE (UK ONLY)", "coil", "optional", "28-1050 / 090-5046-00", *BR, "VIO-GRN", "J7-P7"),
	22: ("Right Outlane Ball Deflector (UK Only)", "RT OUTLANE (UK ONLY)", "coil", "optional", "28-1050 / 090-5046-00", *BR, "VIO-BLU", "J7-P8"),
	23: ("Up/Down Post (UK Only)", "UP/DOWN POST (UK ONLY)", "coil", "optional", "23-1100 / 090-5030-00T", *BR, "VIO-BLK", "J7-P9"),
	24: ("Optional Coin Meter", "OPTIONAL COIN METER", "coil", "optional", "Meter 5v / 091-5000-00", "RED", "J16-P7", 5, "VIO-GRY", "J7-P10"),
	25: ("Stan Flashers (X2)", "FLASH STAN ✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-BRN", "J6-P1"),
	26: ("Chef Flashers (X2)", "FLASH CHEF ✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-RED", "J6-P2"),
	27: ("Kenny Flashers (X2)", "FLASH KENNY ✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-ORG", "J6-P3"),
	28: ("Kyle Flashers (X2)", "FLASH KYLE ✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-YEL", "J6-P4"),
	29: ("Cartman Flashers (X2)", "FLASH CARTMAN ✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-GRN", "J6-P5"),
	30: ("Kenny and Back Panel Flashers", "FLASH KENNY ✻1 / BACK ✻2", "flasher", "used", "#906 Bulb / 165-5004-00 and #89 Bulb / 165-5000-89", *OR, "BLK-BLU", "J6-P6"),
	31: ("Mr. Hankey / Toilet Flashers (X2)", "FLASH MR HANKEY/TOILET ✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-VIO", "J6-P7"),
	32: ("Super VUK Flasher", "FLASH SUPER VUK ✻1", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-GRY", "J6-P8"),
}
PUBLIC_BINDING = {15: 48, 16: 46}
# What the retained table does with each callback (embedded script line numbers).
SOLENOID_SCRIPT = {
	1: "SolCallback(1) = \"SolRelease\": bsTrough.ExitSol_On while balls remain (lines 154-158, 741)",
	2: "SolCallback(2) = \"AutoLaunch\": fires the table's Plunger with Autoplunger set (lines 174-181, 742)",
	3: "SolCallback(3) = \"SuperVuk.SolOut\": ejects the super-VUK ball stack on 45 (line 743)",
	4: "SolCallback(4) = \"TopVuk.SolOut\": ejects the top-VUK saucer on 46 (line 744)",
	5: "SolCallback(5) = \"ToiletSeatLid\": raises the seat (helper flipper ToiletFlipper) and enables ToiletKicker while energized, lowers it and disables the kicker on release (lines 558-567, 745)",
	6: "SolCallback(6) = \"MrHankeyUp\": rotates the helper flippers MrHankeyFlipper and CisternFlipper to their end, raising Mr. Hankey and the tank lid (lines 572-579, 746)",
	7: "SolCallback(7) = \"FlashPops\": lights FPa, FPb, FPc and FPd and the yellow dome FlasherCapYellow (lines 1200, 1298-1314)",
	9: "LeftBumper is a VPX bumper that fires itself; no callback",
	10: "RightBumper is a VPX bumper that fires itself; no callback",
	11: "BottomBumper is a VPX bumper that fires itself; no callback",
	12: "LeftSlingShot is a VPX slingshot wall that fires itself; no callback",
	13: "SolCallback(13) = \"MrHankeyDown\": rotates MrHankeyFlipper and CisternFlipper back to their start (lines 582-589, 747)",
	14: "SolCallBack(14) = \"KennyDead\": rotates the helper flipper KennyFlipper, which tips the Kenny primitive over, while energized (lines 390-397, 748)",
	17: "RightSlingShot is a VPX slingshot wall that fires itself; no callback",
	18: "SolCallback(18) = \"FlashTopVuk\": light F18, the red dome FlasherCapChef and Flasher sprites FlasherF18/FlasherF18a (lines 1201, 1336-1350)",
	19: "SolCallBack(19) = \"KennyLeft\": swings the Kenny primitive left through UpdateKennyLeft (lines 366-376, 749)",
	20: "SolCallback(20) = \"KennyRight\": swings the Kenny primitive right through UpdateKennyRight (lines 378-388, 750)",
	24: "the knocker line 'SolCallback(24) = \"vpmSolSound SoundFX(\"\"Knocker\"\",DOFKnocker),\"' is commented out (line 751)",
	25: "SolCallback(25) = \"FlashStan\": lights F1 and F1a (lines 1202, 1234-1242)",
	26: "SolCallback(26) = \"FlashChef\": lights F2 and F2a (lines 1203, 1244-1252)",
	27: "SolCallback(27) = \"FlashKenny\": lights F3 and F3a (lines 1204, 1254-1262)",
	28: "SolCallback(28) = \"FlashKyle\": lights F4 and F4a (lines 1205, 1264-1272)",
	29: "SolCallback(29) = \"FlashCartman\": lights F5 and F5a (lines 1206, 1274-1282)",
	30: "SolCallback(30) = \"FlashKennyAndBack\": light F6b at the back panel, the lit Kenny primitive KennyL and Flasher sprites FlasherF6/FlasherF6a (lines 1207, 1316-1334)",
	31: "SolCallback(31) = \"FlashMrHankeyToilet\": lights F7l and F7r (lines 1208, 1212-1232)",
	32: "SolCallback(32) = \"FlashSuperVuk\": light F8, the red dome FlasherCapRed and Flasher sprite FlasherF8 (lines 1209, 1284-1296)",
}
# What the harness runs showed for each output (evidence step labels).
SOLENOID_RUNTIME = {
	1: "the ROM fired it on Start until the served ball left the trough, and again after the drain",
	3: "a ball held on the super VUK (45) drew repeated kicks, and one closure of the under-trough switch 44 or 48, with the super VUK empty, drew one kick",
	4: "sprk_103 fired it once some seconds after a ball settled on the top VUK (46); sprk_096 fired it only later, during the under-trough steps",
	7: "it flashed with each coin, each turbo bumper and each pop-bumper target (37, 38)",
	9: "it answered the left turbo bumper switch (49)",
	10: "it answered the right turbo bumper switch (50)",
	11: "it answered the bottom turbo bumper switch (51)",
	12: "it answered the left slingshot switch (59)",
	13: "it pulsed twice at power-up and once at the drain, driving Mr. Hankey home",
	14: "it fired once from the Kenny opto (42)",
	17: "it answered the right slingshot switch (62)",
	18: "it flashed at the drain",
	19: "it alternated with 20, nine or ten pulses each, from the Kenny opto (42)",
	20: "it alternated with 19, ten pulses each, from the Kenny opto (42)",
	24: "each coin on the center slot (5) pulsed it four times, the coin-meter count",
	25: "it flashed when a ball was served, from the left slingshot, the left orbit and the left lanes, and at the drain",
	26: "it flashed when a ball was served and at the drain",
	27: "it flashed when a ball was served and at the drain",
	28: "it flashed when a ball was served, from the right ramp switches (25, 26) and at the drain",
	29: "it flashed when a ball was served and left the shooter lane, from the right slingshot and the right lanes, and at the drain",
	30: "it flashed from the Kenny opto (42), a ball on the top VUK (46) and at the drain, and on sprk_103 also from the under-trough switch 44",
	31: "it flashed from the centre 3-bank (22-24) and at the drain",
	32: "it flashed when the ball left the shooter lane, from the super VUK (45) and the under-trough switch 48 (on sprk_096 also 44), and at the drain",
}
SOLENOID_NOT_SEEN = {
	2: "No harness run provoked an auto launch.",
	5: "No harness run raised the toilet seat lid.",
	6: "No harness run fired the Mr. Hankey latch.",
}
FLASHER_LOCATIONS = {
	7: "four bulbs around the turbo bumpers, under the yellow dome", 18: "red dome at the top VUK", 25: "under the Stan inserts",
	26: "under the Chef inserts", 27: "under the Kenny inserts", 28: "under the Kyle inserts", 29: "under the Cartman inserts",
	30: "one #906 inside Kenny and two #89 on the back panel", 31: "two at the toilet (Mr. Hankey)", 32: "red dome at the super VUK",
}
FLASHER_QUANTITY = {7: 4, 25: 2, 26: 2, 27: 2, 28: 2, 29: 2, 30: 3, 31: 2}


def q_output_id(number: int) -> str:
	return f"device.q{number}-{slug(Q_OUTPUTS[number][0])}"


def _q_wiring(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	return {
		"board": "Whitestar I/O Power Driver board 520-5137-01", "driver_transistor": f"Q{number}", "control_wire": control_wire,
		"control_connection": control_connection, "power_wire": power_wire, "power_connection": power_connection,
		"nominal_voltage_v": voltage, "voltage_type": "dc",
	}


def _q_output(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	address = PUBLIC_BINDING.get(number, number)
	identifier = q_output_id(number)
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {}
	coil_part = part.split(" / ")[-1].split(" ")[0]
	if re.fullmatch(r"\d{3}-\d{4}-\d{2}[A-Z]?", coil_part):
		physical["part_number"] = coil_part
	notes = f'Coils Detailed Chart Table (DR. 6) row #{number if number <= 24 else f"F{number - 24}"} "{printed}": drive transistor Q{number}, cell "{part}".'
	if number in FLASHER_LOCATIONS:
		physical["location"] = FLASHER_LOCATIONS[number]
	if number in FLASHER_QUANTITY:
		physical["quantity"] = FLASHER_QUANTITY[number]
	if number == 4:
		notes += " The chart prints the control colour BRY-YEL; every other high-current row uses BRN-, and the J8 pin sequence puts BRN-YEL here, so the record follows BRN-YEL."
	if number in (25, 26, 27, 28, 29):
		notes += " The flash lamp location drawing (DR. 7) marks this flasher twice: one bulb under a character's face inserts and one under its arrow inserts."
	if number == 30:
		notes += (
			" The flash lamp location drawing marks F6 once on Kenny (white box, the #906 bulb inside the figure per the Kenny Assembly "
			"page) and twice side by side on the back panel at the top right; only the Kenny bulb is placed."
		)
	if number == 7:
		notes += " The flash lamp location drawing marks four '7' bulbs around the turbo bumpers."
	if number in (15, 16):
		side = "left" if number == 15 else "right"
		power = 47 if number == 15 else 45
		notes += (
			f" Physical Q{number} is removed from public {number}: se.c's se_solenoid_w masks it off and publishes it as the lower-{side} flipper "
			f"power bit {power}, and core.c synthesizes canonical callback {address} from it. Bind this one coil to public {address}, the retained "
			f"table's SolCallback(sL{'L' if number == 15 else 'R'}Flipper); public {power} is its power-phase state, not a second coil. The "
			"2-Flipper Circuit Wiring Diagram describes the drive: a 40 ms pulse on a button closure, then 1 ms every 12 ms while held, from one "
			f"50v supply through a 3A slow-blow fuse under the playfield ({'GRY-YEL' if number == 15 else 'BLU-YEL'})."
		)
		refs += (VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, RUNTIME_096_SOURCE)
	if number == 5:
		notes += " The Toilet Lid Lift Coil Assy 500-6392-00-71 (printed page 70-71) carries this 23-1100 coil."
	if number in (6, 13):
		notes += (
			" The Mr. Hankey & Tank Lid Lift Coil Assy 500-6391-00-71 carries a 23-1100 coil (Q13, MR. HANKEY (DOWN)) and the trip coil "
			"assembly 515-6985-00 with the 29-1000 coil (Q6, MR. HANKEY LATCH), described as a heavy-duty spring-loaded device: Q13 "
			"pulls Mr. Hankey and the tank lid down onto the latch, and Q6 trips the latch so the spring throws them up."
		)
	if number in (14, 19, 20):
		notes += (
			" The Kenny Assembly 500-6358-00-71 (printed pages 72-73): the centre 22-1080 coil (Q14) pivots Kenny over ('dead'), and the "
			"two 24-940 coils (Q19 left, Q20 right) swing the carriage."
		)
	if number in (21, 22, 23):
		notes += (
			" UK only: the chart row is printed on a dark grey band, and the coil location drawing draws "
			f"{'21 at the left outlane' if number == 21 else '22 at the right outlane' if number == 22 else '23 between the flippers'} "
			"in a grey box. The UK parts pages list the Lt/Rt Outlane Ball Deflector Assembly 500-5788-03 (Qty 2, coil 28-1050) "
			"and the Up/Down Post Assembly 500-6293-00 (coil 23-1100). The cabinet's UK-only Sav-A-Ball buttons (switches 1 and 8) "
			"ask the ROM for them. A standard machine fits none, and the retained US table models none."
		)
	if number == 8:
		notes += (
			" The row is printed on a grey band: the European token dispenser is optional equipment, not on a standard machine, and the "
			"retained script registers no callback."
		)
		physical["location"] = "cabinet (token dispenser, when fitted)"
	if number == 24:
		notes += (
			" The cabinet wiring diagram's TO COIN METER box routes Q24 (J7-10, 78 VIO-GRY) and +5VDC (J16-7, 22 RED) to the meter. "
			"No stock playfield device is fitted."
		)
	if number in SOLENOID_SCRIPT:
		notes += f" Retained table script: {SOLENOID_SCRIPT[number]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if number in SOLENOID_RUNTIME:
		notes += f" In the harness runs {SOLENOID_RUNTIME[number]}."
		refs += (RUNTIME_SOURCE, RUNTIME_096_SOURCE)
	if number in SOLENOID_NOT_SEEN:
		notes += f" {SOLENOID_NOT_SEEN[number]}"
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Q{number}"}], "wiring": _q_wiring(number)}
	role = "emitter" if kind == "flasher" else "effect"
	if number in (8, 24):
		extra["roles"] = ["cabinet.coin-meter"] if number == 24 else ["cabinet.token-dispenser"]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		if number == 24:
			physical["location"] = "cabinet (coin meter, when fitted)"
	else:
		spatial = located("solenoid", address, identifier, role)
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("solenoid", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, physical=physical, **extra)


def solenoid_outputs() -> list[dict[str, Any]]:
	items = [_q_output(number) for number in Q_OUTPUTS]
	items.append(_device(
		"virtual.15-fast-flip-game-on", "Whitestar Fast-Flip / Game-On State", "virtual", SOLENOID_GROUP, 15, "used",
		(CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE, RUNTIME_096_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "15"}],
		physical={"notes": (
			"se.c sets public 15 while the ROM's fast-flip byte is non-zero, i.e. while the flippers are enabled in a game; MACHINE_INIT(se) "
			"places that byte at CPU RAM 0x00 for sprk_103 only, and sets none for sprk_096 or sprk_090. sega.vbs declares GameOnSolenoid = 15. "
			"In the sprk_103 gameplay run it rose when the served ball reached the shooter lane and fell at the drain; the sprk_096 run never "
			"raised it. Physical Q15 is the left flipper at public 48; never wire this state to a transistor."
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
		items.append(_device(
			f"virtual.{address}-reserved", f"Reserved Address {address}", "virtual", SOLENOID_GROUP, address, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": "A Whitestar compatibility hole: the driver declares no auxiliary board (INITGAME hw 0), and nothing in se.c drives it for this driver."},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	for address, side, canonical, number in ((45, "right", 46, 16), (47, "left", 48, 15)):
		items.append(_device(
			f"virtual.{address}-{side}-flipper-power-phase", f"{side.capitalize()} Flipper Power-Phase State", "virtual", SOLENOID_GROUP, address, "used",
			(CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, RUNTIME_096_SOURCE), aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": (
				f"se_solenoid_w publishes physical Q{number}'s drive here and core.c synthesizes canonical {canonical} from it; one {side} flipper coil "
				f"is bound at {canonical}. In the gameplay runs, holding the {side} flipper button pulsed {address} and {canonical} together."
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
	1: ("Chef Face", "CHEF FACE", "#555 Bulb"), 2: ("Chef 2", "CHEF #2", "#555 Bulb"), 3: ("Chef 3", "CHEF #3", "#555 Bulb"),
	4: ("Chef 4", "CHEF #4", "#555 Bulb"), 5: ("Chef Arrow", "CHEF ARROW", "#555 Bulb"), 6: ("Mystery", "MYSTERY", "#555 Bulb"),
	7: ("Spooky Vision", "SPOOKY VISION", "#555 Bulb"), 8: ("Extra Ball", "EXTRA BALL", "#555 Bulb"),
	9: ("Stan Face", "STAN FACE", "#555 Bulb"), 10: ("Stan 2", "STAN #2", "#555 Bulb"), 11: ("Stan 3", "STAN #3", "#555 Bulb"),
	12: ("Stan 4", "STAN #4", "#555 Bulb"), 13: ("Stan Arrow", "STAN ARROW", "#555 Bulb"), 14: ("Skill Shot", "SKILL SHOT", "#555 Bulb"),
	15: ("Volcano", "VOLCANO", "#555 Bulb"), 16: ("Anal Probe", "ANAL PROBE", "#555 Bulb"),
	17: ("Kenny Face", "KENNY FACE", "#555 Bulb"), 18: ("Kenny 2", "KENNY #2", "#555 Bulb"), 19: ("Kenny 3", "KENNY #3", "#555 Bulb"),
	20: ("Kenny 4", "KENNY #4", "#555 Bulb"), 21: ("Kenny Arrow", "KENNY ARROW", "#555 Bulb"), 22: ("Super Jackpot", "SUPER JACKPOT", "#555 Bulb"),
	23: ("Multiball Ready", "MULTIBALL READY", "555# ulb"), 24: ("South Park Sign", "SOUTH PARK SIGN", "#555 Bulb"),
	25: ("Kyle Face", "KYLE FACE", "#555 Bulb"), 26: ("Kyle 2", "KYLE #2", "#555 Bulb"), 27: ("Kyle 3", "KYLE #3", "#555 Bulb"),
	28: ("Kyle 4", "KYLE #4", "#555 Bulb"), 29: ("Kyle Arrow", "KYLE ARROW", "#555 Bulb"), 30: ("Kenny Assembly", "KENNY ASSEMBLY", "#555 Bulb"),
	33: ("Cartman Face", "CARTMAN FACE", "#555 Bulb"), 34: ("Cartman 2", "CARTMAN #2", "#555 Bulb"), 35: ("Cartman 3", "CARTMAN #3", "#555 Bulb"),
	36: ("Cartman 4", "CARTMAN #4", "#555 Bulb"), 37: ("Cartman Arrow", "CARTMAN ARROW", "#555 Bulb"),
	38: ("Left Turbo Bumper", "LEFT TUR- BO BUMPER", "555# Bulb"), 39: ("Right Turbo Bumper", "RIGHT TUR- BO BUMPER", "555# Bulb"),
	40: ("Bottom Turbo Bumper", "BTTM TUR- BO BUMPER", "555# Bulb"),
	41: ("Left 5-Bank Bottom", "LEFT 5-BANK BOTTOM", "#555 Bulb"), 42: ("Left 5-Bank 2", "LEFT 5-BANK #2", "#555 Bulb"),
	43: ("Left 5-Bank 3", "LEFT 5-BANK #3", "#555 Bulb"), 44: ("Left 5-Bank 4", "LEFT 5-BANK #4", "#555 Bulb"), 45: ("Left 5-Bank Top", "LEFT 5-BANK TOP", "#555 Bulb"),
	46: ("Toilet Shoot-Up Left", "TOILET S-U LT", "#555 Bulb"), 48: ("Toilet Shoot-Up Right", "TOILET S-U RT", "#555 Bulb"),
	50: ("Right 3-Bank Bottom", "RT. 3-BANK BOTTOM", "#555 Bulb"), 51: ("Right 3-Bank Middle", "RT. 3-BANK MIDDLE", "#555 Bulb"),
	52: ("Right 3-Bank Top", "RT. 3-BANK TOP", "#555 Bulb"), 53: ("Left Outlane", "LEFT OUTLANE", "#555 Bulb"),
	54: ("Left Return Lane", "LEFT RE- TURN LANE", "#555 Bulb"), 55: ("Right Return Lane", "RIGHT RE- TURN LANE", "#555 Bulb"),
	56: ("Right Outlane", "RIGHT OUTLANE", "#555 Bulb"),
	57: ("Mr. Hankey: Bottom", "MR. HANKEY: BOTTOM", "#555 Bulb"), 58: ("Mr. Hankey: Body", "MR. HANKEY: BODY", "#555 Bulb"),
	59: ("Mr. Hankey: Left Hand", "MR. HANKEY: LT HAND", "#555 Bulb"), 60: ("Mr. Hankey: Right Hand", "MR. HANKEY: RT HAND", "#555 Bulb"),
	61: ("Mr. Hankey: Head", "MR. HANKEY: HEAD", "#555 Bulb"), 62: ("Mr. Hankey: Hat", "MR. HANKEY: HAT", "#555 Bulb"),
	63: ("Pop Bumper Target Left", "POP BUMPER TARGET LT", "#555 Bulb"), 64: ("Pop Bumper Target Right", "POP BUMPER TARGET RT", "#555 Bulb"),
}
UNUSED_LAMPS = (31, 32, 47, 49) + tuple(range(65, 81))
DOTS_LAMPS = (22, 23, 30, 38, 39, 40, 46, 48)
LAMP_DRIVE = [("YEL-BRN", "J13-P9", "U17"), ("YEL-RED", "J13-P8", "U16"), ("YEL-ORG", "J13-P7", "U15"), ("YEL-BLK", "J13-P6", "U14"), ("YEL-GRN", "J13-P5", "U13"), ("YEL-BLU", "J13-P4", "U12"), ("YEL-VIO", "J13-P3", "U11"), ("YEL-GRY", "J13-P1", "U10")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
LAMPS_SEEN = frozenset(range(1, 65))


def lamp_id(address: int) -> str:
	if address in LAMPS:
		return f"lamp.{address}-{slug(LAMPS[address][0])}"
	return f"lamp.{address}-not-used"


def _lamp_wiring(address: int) -> dict[str, Any]:
	row, column = divmod(address - 1, 8)
	drive_wire, drive_connection, driver = LAMP_DRIVE[column]
	return_wire, return_connection = LAMP_RETURN[row]
	return {
		"board": "Whitestar I/O Power Driver board 520-5137-01 lamp matrix", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "return_component": f"column driver {driver}; row transistor Q{33 + row}",
	}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 81):
		row, column = divmod(address - 1, 8)
		identifier = lamp_id(address)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		notes = f"Printed lamp-matrix row {row + 1}, column {column + 1}."
		if address in UNUSED_LAMPS:
			notes += " The Lamp Matrix Grid (DR. 4) prints this cell NOT USED, shaded black with no bulb line, and the lamp location drawing marks no lamp with this number."
			refs: tuple[str, ...] = (MANUAL_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE)
			if address <= 64:
				notes += (
					" The ROM's attract sweep strobes every column and row of the 64-lamp matrix, so the harness runs saw this address toggle in "
					"step with its neighbours; that is the sweep, not a fitted socket. The retained script assigns no Light to it."
				)
				refs += (VPX_SCRIPT_SOURCE,)
			else:
				notes += " The grid also prints the row heading of rows 9 and 10 NOT USED; no harness run drove an address above 64."
			items.append(_device(identifier, f"Not Used Lamp {address}", "lamp", LAMP_GROUP, address, "unused", refs,
				aliases=aliases, physical={"notes": notes}, wiring=_lamp_wiring(address), spatial=not_applicable("unused", MANUAL_SOURCE)))
			continue
		label, printed, bulb = LAMPS[address]
		refs = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE)
		physical: dict[str, Any] = {"location": label, "part_number": "165-5002-00"}
		notes += f' The grid prints "{printed}" with the bulb cell "{bulb}".'
		if bulb != "#555 Bulb":
			notes += " The cell's misprint aside, the bulb is the #555 every other cell of the grid uses."
		if address in DOTS_LAMPS:
			notes += " The cell carries the grid's DOTS (diode on terminal strip) tag."
		if address == 30:
			notes += " The Kenny Assembly page lists a #555 bulb inside Kenny for this lamp, beside the #906 bulb of flasher Q30."
		notes += " The harness runs saw the ROM drive it."
		extra: dict[str, Any] = {"aliases": aliases, "wiring": _lamp_wiring(address)}
		spatial = located("lamp", address, identifier, "emitter")
		if spatial:
			extra["spatial"] = spatial
			notes += f" Retained table script: InitLamps assigns Lights({address}) = l{address} (lines 960-1019; UseLamps = 1, line 52)."
			notes += _placement_note("lamp", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		physical["notes"] = notes
		items.append(_device(identifier, label, "lamp", LAMP_GROUP, address, "used", refs, physical=physical, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	entries = _spatial_seed()["gi"]["0"]
	placements = [{
		"id": f"gi.relay.emitter.{index}", "role": "emitter", "space": "playfield", "x": entry["x"], "y": entry["y"],
		"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
	} for index, entry in enumerate(entries, start=1)]
	notes = (
		"One G.I. relay on the I/O Power Driver board 520-5137-01 (U206 data latch D0 through R254 and Q200 2N3904, coil on 20v DC with "
		"D229 across it) switches the 6.3v AC G.I. supply from J14 to four separately fused circuits on J15 (General Illumination Circuit "
		"Detailed Wiring Diagram, printed page 83): B, F24, BRN-WHT to WHT-BRN, Left Playfield & Rt. Outlane, 7 #44; Y, F25, YELLOW to "
		"WHT-YEL, Top Lt. & Rt. Playfield, 9 #44; G, F26, GREEN to WHT-GRN, Rt. P/F & Lt. Outlane + Coin Door, 6 #44 plus 2 #555 on the "
		"coin door; V, F27, VIOLET to WHT-VIO, Mid Lt. & Rt. Playfield, 9 #44. The page warns that G.I. bulb quantities may change during "
		"production. The quantity 33 is the printed 31 playfield bulbs plus the two coin-door bulbs. se.c publishes the relay as GI 0, and "
		"the harness runs saw it switch on in attract mode and blink with the outlanes and the right ramp exit. The retained table does not "
		f"bind GI 0: its GIOn/GIOff/GiBlinking subs (lines 1098-1130) follow table events. Its GI collection pairs a bulb-drawing Gis light with "
		"a glow-only Gi double at 28 sockets, and has one lone Gis26 at the upper left; each socket is placed on its Gis light. Three more "
		"collection lights, Gis11-13, sit on the turbo bumper caps' bulbs, which are matrix lamps 38-40 (one #555 per Turbo Bumper "
		f"Assembly, printed page 68), so they are table rendering proxies and are not G.I. sockets. That leaves {len(entries)} placed sockets "
		"against the 31 playfield bulbs the page prints. They are placed as playfield bulbs, observed only; "
		"the mirrored bottom-view drawing gives no per-string assignment. The two coin-door bulbs are counted but not placed."
	)
	return [_device(
		"gi.relay", "General Illumination Relay", "gi", GI_GROUP, 0, "used", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.gi", "value": "0"}],
		physical={"location": "playfield and coin door", "quantity": 33, "notes": notes},
		wiring={"board": "Whitestar I/O Power Driver board 520-5137-01 G.I. relay", "power_wire": "YEL / YEL-WHT 6.3v AC through F24-F27", "power_connection": "J14/J15", "nominal_voltage_v": 6.3, "voltage_type": "ac"},
		spatial={"status": "observed", "placements": placements},
	)]


def displays() -> list[dict[str, Any]]:
	return [{
		"id": "display.dmd", "label": "Dot Matrix Display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32,
		"physical_location": "cabinet_or_service",
		"provenance": provenance("validated", CORE_SOURCE, RUNTIME_SOURCE),
		"spatial": not_applicable("cabinet_or_service", CORE_SOURCE),
	}]


# --- Mechanisms ----------------------------------------------------------------------------------------
def _mechanism(suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...], assembly: str | None = None) -> dict[str, Any]:
	result: dict[str, Any] = {"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior}
	if assembly:
		result["assembly_part_number"] = assembly
	result["provenance"] = provenance("validated", *refs)
	return result


def mechanisms() -> list[dict[str, Any]]:
	common = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	run = common + (RUNTIME_SOURCE, RUNTIME_096_SOURCE)
	s = switch_id
	q = q_output_id
	return [
		_mechanism("trough", "5-ball trough with up-kicker and stacking opto", "kicker", [q(1)], [s(10), s(11), s(12), s(13), s(14), s(15)],
			"Five balls rest in the trough (500-6318-25) on micro switches 10 (left), 11, 12 and 13 and on the VUK opto 14 at the up-kicker. "
			"Q1 kicks the ball on 14 up past the stacking opto 15 into the shooter lane, and the rest roll one place toward the up-kicker. "
			"Hold each occupied position at 1 and pass the kicked ball through 15 as a short 1 pulse (beam blocked). In the gameplay runs "
			"the ROM fired Q1 repeatedly on Start until the served ball left the trough. The retained table's bsTrough omits 15.",
			run, assembly="500-6318-25"),
		_mechanism("shooter", "Ball shooter and auto launch", "kicker", [q(2)], [s(16)],
			"A served ball rests on shooter-lane switch 16. The player plunges it with the ball shooter (500-6146-00-04), or Q2 fires the "
			"autoplunger arm (coil assembly 500-6092-02, arm 500-6091-00). The retained table fires its Plunger object with Autoplunger set.", common),
		_mechanism("top-vuk", "Top VUK behind the upper loop", "kicker", [q(4)], [s(46)],
			"The VUK Assembly (Right Style) 500-6290-01 at the top of the playfield: a ball from the left orbit (47) settles on 46 and Q4 "
			"lifts it onto the top wire ramp, which feeds the left ramp (Left Ramp Assembly page: 'ball enters from top wire ramp via VUK'). "
			"In the sprk_103 gameplay run the ROM flashed Q30 when the ball arrived and fired Q4 once some seconds later; sprk_096 fired Q4 only during a later step.",
			run, assembly="500-6290-01"),
		_mechanism("super-vuk", "Super VUK and under-trough", "kicker", [q(3)], [s(45), s(43), s(44), s(48)],
			"The Under-Trough Assembly 500-6385-00-71 collects balls from under the toilet (43), from under Kenny (44) and from the playfield "
			"hole above the super VUK (48), each passing one micro switch, and leads them to the Super VUK Assembly 500-6184-04-71, where the "
			"ball rests on 45 until Q3 (24-940) kicks it up onto the playfield. In the gameplay runs a ball held on 45 drew repeated Q3 kicks, "
			"and one closure of 44 or 48 with the super VUK empty drew one Q3 kick, so the ROM fires the super VUK on the under-trough switch without "
			"waiting for 45; a closure of 43 alone drew none. The retained table pulses 43, 44 and 48 from kickers and hands the ball to its SuperVuk ball stack "
			"1.2-2.4 s later.", run, assembly="500-6184-04-71"),
		_mechanism("toilet", "Toilet with seat lid and Mr. Hankey", "toy", [q(5), q(6), q(13)], [s(43)],
			"Toilet & Frame Assembly 500-6360-00-71. Q5 (23-1100, Toilet Lid Lift Coil Assy 500-6392-00-71) lifts the seat lid while "
			"energized; with the lid up the ball can enter the toilet, drop to the under-trough switch 43 and go on to the super VUK, and "
			"with it down the right ramp's ball passes over the toilet into the left ramp (Left Ramp Assembly page). Mr. Hankey and the tank "
			"lid ride the Mr. Hankey & Tank Lid Lift Coil Assy 500-6391-00-71: Q13 (23-1100) pulls them down onto a spring-loaded latch "
			"(trip coil assembly 515-6985-00), and Q6 (29-1000) trips it so the spring throws Mr. Hankey up. There is no position switch. "
			"In the harness runs Q13 pulsed twice at power-up and once at the drain; no run fired Q5 or Q6. The retained table raises its "
			"ToiletFlipper and enables ToiletKicker while Q5 is on, raises MrHankeyFlipper/CisternFlipper on Q6 and lowers them on Q13.",
			run, assembly="500-6360-00-71"),
		_mechanism("kenny", "Kenny figure", "toy", [q(14), q(19), q(20), q(30)], [s(42)],
			"Kenny Assembly 500-6358-00-71: Kenny stands on a carriage that two 24-940 coils swing left (Q19) and right (Q20), and the centre "
			"22-1080 coil (Q14) pivots him over ('dead'). A #555 bulb (lamp 30) and the #906 flasher bulb (Q30) are inside the figure. The "
			"Kenny opto 42 (OPTO & Bracket (Long) Assembly 500-6242-02-71) sees the ball reach him. In the gameplay runs one 42 closure "
			"made the ROM fire Q14 once, alternate Q19 and Q20 (nine or ten pulses each before the next step), and flash Q30. Balls that reach him drop to the under-trough "
			"switch 44. The retained table rotates its Kenny primitive from the three coils.", run, assembly="500-6358-00-71"),
		_mechanism("lower-flippers", "Lower flippers", "other", [q(15), q(16)], ["switch.84-left-flipper-button", "switch.83-left-flipper-end-of-stroke", "switch.82-right-flipper-button", "switch.81-right-flipper-end-of-stroke"],
			"Left (500-5944-14) and right (500-5944-04) flipper assemblies with 23-1100 coils on one 50v supply. The CPU applies a 40 ms pulse "
			"on a button closure and then 1 ms every 12 ms while the button is held; each N.C. end-of-stroke switch opens at full stroke, and a "
			"closure during a hold earns another 40 ms pulse. PinMAME publishes Q15 at 47/48 and Q16 at 45/46.",
			(MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, RUNTIME_096_SOURCE, VPX_SCRIPT_SOURCE)),
		_mechanism("bumpers", "Three turbo bumpers", "other", [q(9), q(10), q(11)], [s(49), s(50), s(51)],
			"Left (Q9/49), right (Q10/50) and bottom (Q11/51) turbo bumpers (515-6459-01, -04, -03) with stack-blade spoon switches 180-5015-03; "
			"each switch fired its own coil in the gameplay runs, with the four pop flashers (Q7).", run),
		_mechanism("slingshots", "Slingshots", "other", [q(12), q(17)], [s(59), s(62)],
			"Left (Q12/59) and right (Q17/62) slingshots (500-5849-01), two parallel blade contacts per side; each switch fired its own coil in "
			"the gameplay runs.", run, assembly="500-5849-01"),
		_mechanism("uk-sav-a-ball", "UK Sav-A-Ball outlane deflectors and up/down post", "other", [q(21), q(22), q(23)], [s(1), s(8)],
			"UK only: Q21 and Q22 drive the left and right outlane ball deflectors (500-5788-03, coil 28-1050) and Q23 the up/down post "
			"between the flippers (500-6293-00, coil 23-1100), all on the main I/O board. The UK-only Sav-A-Ball cabinet buttons on 1 and 8 ask "
			"the ROM for them; the ROM, not a wire, raises the deflectors. A standard machine fits none of it.", (MANUAL_SOURCE, CORE_SOURCE)),
	]


# --- Drivers -------------------------------------------------------------------------------------------
def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {driver["id"]: driver for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
	if set(by_id) != set(DRIVER_IDS):
		raise RuntimeError(f"South Park driver family differs from the catalog: {sorted(set(DRIVER_IDS) ^ set(by_id))}")
	records = []
	for driver_id in sorted(DRIVER_IDS):
		source = by_id[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = DRIVER_COMPATIBILITY[driver_id]
		record["variant_notes"] = BASE_DRIVER_NOTE + DRIVER_NOTES[driver_id]
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

RENDERER = "; rendered by tools/render_excerpt_image.py with PyMuPDF 1.26.3 and Pillow 12.3.0"
IMAGE_DERIVATIONS = {
	"switch-lamp-locations": f"{MANUAL_NAME} page 4, crop box 0.54,0.02,0.99,0.71, scanned page rendered at its native resolution (embedded image xref 28, 3216px across 16.75in), rendered at 192 dpi, grayscale, 1448x1421 WebP quality 80" + RENDERER,
	"coil-flash-locations": f"{MANUAL_NAME} page 5, crop box 0.54,0,0.99,0.72, scanned page rendered at its native resolution (embedded image xref 34, 3216px across 16.75in), rendered at 192 dpi, grayscale, 1448x1482 WebP quality 80" + RENDERER,
	"gi-wiring": f"{MANUAL_NAME} page 49, crop box 0.5,0,1,1, scanned page rendered at its native resolution (embedded image xref 304, 3216px across 16.75in), rendered at 179 dpi, capped to 1500px wide, grayscale, 1500x1920 WebP quality 80" + RENDERER,
	"flipper-circuit": f"{MANUAL_NAME} page 51, crop box 0,0,0.5,1, scanned page rendered at its native resolution (embedded image xref 316, 3216px across 16.75in), rendered at 179 dpi, capped to 1500px wide, grayscale, 1500x1920 WebP quality 80" + RENDERER,
}


def _excerpt(name: str, locator: str, *, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	record: dict[str, Any] = {"id": f"excerpt.south-park.{name}", "locator": locator, "path": f"evidence/excerpts/{MACHINE_ID}/{name}.md", "sha256": EXCERPT_FILE_HASHES[f"{name}.md"]}
	if name in IMAGE_DERIVATIONS:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = IMAGE_DERIVATIONS[name]
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("switch-matrix", "PDF page 4 (left half), printed DR. 4, Switch Matrix Grid and dedicated switches; PDF page 15 (right half), printed page 15 switch table"),
		_excerpt("lamp-matrix", "PDF page 4 (left half, lower part), printed DR. 4, Lamp Matrix Grid"),
		_excerpt("switch-lamp-locations", "PDF page 4 (right half), printed DR. 5, switch and lamp location drawings"),
		_excerpt("coil-table", "PDF page 5 (left half), printed DR. 6, Coils Detailed Chart Table"),
		_excerpt("coil-flash-locations", "PDF page 5 (right half), printed DR. 7, coil and flash lamp location drawings"),
		_excerpt("gi-wiring", "PDF page 49 (right half), printed page 83, General Illumination Circuit Detailed Wiring Diagram"),
		_excerpt("flipper-circuit", "PDF page 51 (left half), printed page 86, 2-Flipper Circuit Wiring Diagram"),
		_excerpt("cabinet-wiring", "PDF page 52 (left half), printed page 88, Cabinet / Coin Door Wiring Diagram"),
		_excerpt("mechanism-assemblies", "PDF pages 40-47 and 52, printed pages 64-78 and 89, major assemblies and the trough opto boards (selected items)", reviewed=False),
	]


def source_records() -> list[dict[str, Any]]:
	runs_103 = load_json(ROOT / RUNTIME_103_PATH)["runtime"]["raw_runs"]
	runs_096 = load_json(ROOT / RUNTIME_096_PATH)["runtime"]["raw_runs"]

	def describe(raw_runs: list[dict[str, Any]]) -> str:
		return ", ".join(f"{raw['name']} (run.json SHA-256 {raw['sha256'][:12]}..., directory manifest {RUN_MANIFESTS[raw['name']][:12]}...)" for raw in raw_runs)

	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the sprk clone tree (" + ", ".join(DRIVER_IDS) + ")",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/segames.c INITGAME macro (FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), swCol 0, lampCol 2, custSol 0) and INITGAME(sprk, GEN_WS, "
				"se_dmd128x32, 0) with the sprk_103, sprk_096 and sprk_090 ROM sets on de_mSES1 (lines 475-505); src/wpc/se.c MACHINE_INIT(se) "
				"(fast-flip byte at CPU RAM 0x00 for sprk_103 only), the fast-flip block publishing public 15, switch_r (~core_getSwCol), "
				"dedswitch_r (flipper column swapped into U206 order, complemented), dip_r, se_solenoid_w (Q15/Q16 masked off and published at "
				"47/45), the G.I. relay at gi[0], ram_w's memory-protect gate on -3; src/wpc/core.c core_updateSw (no FLIP_EOS: EOS bits untouched)."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/whitestar.json", "revision": "repository",
			"locator": "Whitestar public switch (-3..0, 1-64, 81-88), DIP 1-8, solenoid 1-50, lamp and GI 0 address rules and their notes",
			"license": "BSD-3-Clause", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-30T14:20:00Z",
			"locator": (
				"IPDB machine 4444 'South Park' (Sega Pinball, February 1999, model 71, Sega/Stern Whitestar, 6 players), read from the "
				f"Wayback Machine capture {IPDB_WAYBACK_URL} because the live site is Cloudflare-gated; the capture is retained gzip-compressed "
				f"under {MANUALS_DIRECTORY}. Its documentation list carries the 138 MB English manual whose bytes match the retained copy."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", f"IPDB machine 4444 page, {IPDB_WAYBACK_URL}", reviewed=False)],
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": f"external:{MANUALS_DIRECTORY}/{MANUAL_NAME}", "original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256, "acquired_at": "2026-10-30T13:56:00Z",
			"locator": (
				"Sega South Park operations manual (72 scanned spreads, two printed pages each, no text layer). PDF 4-5 are the front-matter "
				"Dr. Pinball sheets (DR. 4 switch and lamp matrix grids, DR. 5 switch and lamp locations, DR. 6 coil chart, DR. 7 coil and flash "
				"locations); PDF 15 the printed page-15 switch table; PDF 40-47 the major assemblies; PDF 49-52 the G.I., flipper, cabinet and "
				f"trough opto pages. IPDB's direct resource {MANUAL_URL} was fetched through the Wayback Machine ({MANUAL_WAYBACK_URL})."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Sega Pinball, Inc.; hosted by the Internet Pinball Machine Database",
			"excerpts": _manual_excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "known_working": True,
			"uri": "external:pinmame-vpx-sources/sega/south-park-1999/v1-3/" + quote(TABLE_NAME),
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				"Retained Knorr South Park 1.3 recreation (script header 'V1.3 Added DOFFlippers'). Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. Geometry authority only for the "
				"objects its embedded script binds; the placement seed tools/seeds/sega/south-park-1999-spatial.json lists them."
			),
			"license": "NOASSERTION", "attribution": "Knorr (table author)", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "known_working": True,
			"uri": "external:pinmame-vpx-sources/sega/south-park-1999/v1-3/" + quote("South Park (Sega 1999) 1.3/script.vbs"),
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256,
			"locator": (
				"The retained table's embedded script as vpxtool extracts it. Runtime authority for controller callbacks: Const cGameName = "
				"\"sprk_103\", LoadVPM \"01560000\", \"sega.VBS\", 3.36, UseLamps = 1, HandleMechanics = 0, the bsTrough/SuperVuk ball stacks "
				"and TopVuk saucer, the SolCallback table, the InitLamps Light assignments and the switch handlers. Known table defects: "
				"the stacking opto 15 is never written, G.I. 0 is not bound (table events drive the G.I.), and the EOS inputs 81/83 are never written."
			),
			"license": "NOASSERTION", "attribution": "Knorr (table author)", "rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment line of the embedded script that binds the controller, with its line number", credit=QUOTE_CREDIT)],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/sega/south-park-1999/v1-3/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under the vpxtool extraction "
				f"'{EXTRACTION_RELATIVE_PATH.as_posix()}'; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_CORPUS_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{VPX_CORPUS_REVISION}/" + quote("South Park (Sega 1999) 1.3/South Park (Sega 1999) 1.3.vbs", safe="/"),
			"revision": VPX_CORPUS_REVISION, "sha256": CORPUS_SCRIPT_SHA256,
			"locator": (
				"Pinned corpus copy of the same 1.3 table script without its 'V1.3 Added DOFFlippers' header comment: it differs from the retained "
				"script only in the flipper callbacks' DOF constant and a flipper return-speed timer. Its SolCallback table, ball stacks and switch "
				"handlers repeat the retained script's bindings; it corroborates them, not independently, because both are one table's script. "
				"The retained SHA-256 is the repository checkout's CRLF materialization; the linked Git blob is the identical LF-normalized text "
				"(SHA-256 2610d8db413b2779873b3d97430e2c4dd4fbc52e94b63f53eaad64a0a3827c7f)."
			),
			"license": "NOASSERTION", "attribution": "Authors credited in South Park (Sega 1999) 1.3/South Park (Sega 1999) 1.3.vbs and repository contributors",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-review-artifacts/vpm-script-libs/sega.vbs",
			"original_filename": "sega.vbs", "sha256": VPM_SEGA_SHA256,
			"locator": (
				"VPinMAME Sega/Stern Whitestar script library the retained table loads, copied from the contributor's Visual Pinball Scripts "
				f"folder beside the core.vbs it executes (SHA-256 {VPM_CORE_SHA256}). It defines GameOnSolenoid = 15, swBlack 0 / swGreen -1 / "
				"swRed -2 / swMemoryProtect -3, swStartButton 54, swTilt 56, swSlamTilt 55, swCoin3 4 / swCoin1 5 / swCoin2 6, swLRFlip 82, "
				"swLLFlip 84, swURFlip 81 and swULFlip 83, and the country DIP form."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME script authors",
			"excerpts": [_excerpt("vpm-script-library", "sega.vbs constants (lines 20-39), DIP form (lines 52-69) and key handlers (lines 71-139)", credit=QUOTE_CREDIT)],
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/sprk_103.zip", "revision": "1.03", "sha256": ROM_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned sprk_103 ROM set (spkcpu.103 CRC 55ca8aa1, spdspa.101 CRC 48ca598d); used to identify the ROM the harness booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Sega Pinball game code; ROM bytes remain external",
		},
		{
			"id": ROM_096_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/sprk_096.zip", "revision": "0.96", "sha256": ROM_096_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned sprk_096 ROM set (spkcpu.096 CRC 4d7e862a); used to identify the ROM the prototype harness run booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Sega Pinball game code; ROM bytes remain external",
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_103_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				f"Two hash-pinned LibPinMAME harness runs of sprk_103 (library SHA-256 {RUNTIME_LIBRARY_SHA256[:12]}..., built from "
				f"{PINMAME_REVISION[:8]}) from empty NVRAM with built-in mechanisms off: {describe(runs_103)}. Scenarios under "
				"tools/harness-scenarios/whitestar; tools/south_park_runtime_evidence.py derives the committed per-step transitions from the retained runs."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": RUNTIME_096_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_096_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				f"One hash-pinned LibPinMAME harness run of the sprk_096 prototype on the same library from empty NVRAM with built-in mechanisms "
				f"off: {describe(runs_096)}. Its scenario repeats the sprk_103 gameplay scenario step for step."
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
			"id": MACHINE_ID, "name": "South Park", "manufacturer": "Sega", "year": 1999, "kind": "physical_pinball", "model_number": "71",
			"ipdb_id": 4444, "opdb_id": "G4qbD-MQpxv",
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
		"knowledge": {"path": "knowledge/sega/south-park-1999.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"South Park device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"South Park mechanism {mechanism['id']} names unknown devices: {unknown}")
	return definition


# --- Extraction manifest -------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"South Park retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest", "version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained South Park extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"South Park retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("South Park retained extraction manifest does not match the files under the extraction")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"South Park retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
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
			"manifest_uri": "external:pinmame-vpx-sources/sega/south-park-1999/v1-3/extracted-vpxtool.manifest.json", "source_ref": VPX_EXTRACTION_SOURCE,
		},
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": "The centre of the VPX object the embedded script binds to each switch (trigger, target wall, kicker, slingshot wall, bumper). The trough switches and the stacking opto, which the table does not model, are projected onto the release kicker BallRelease; the three under-trough switches onto the kickers that pulse them; each end-of-stroke contact onto its flipper.",
			"lamp": "The centre of the Light InitLamps assigns to each lamp.",
			"solenoid": "The kicker, slingshot wall, bumper or flipper the script fires, and for flashers the script-driven Lights. The auto launch is placed on the table's Plunger; the toilet seat on the ToiletSeat primitive; the Mr. Hankey coils on the MrHankey primitive; the Kenny coils and the Kenny bulb of flasher 30 on the Kenny primitive. The UK-only coils 21-23, which the US table does not model, are projected where the coil location drawing draws them: the two outlane rollovers and the flippers' midpoint.",
			"gi": "The Light members of the table's GI collection, each render-double cluster placed on its member that draws the bulb (show_bulb_mesh); the three turbo-bumper-cap lights on matrix lamps 38-40 are excluded; observed only, without per-string assignment.",
		},
		"unresolved_geometry": [
			"The trough switches 10-15 and the under-trough switches 43, 44 and 48 are not modelled by the table; their placements are projections onto mechanism objects.",
			"The UK-only coils 21-23 are projections from the coil location drawing onto US-table objects.",
			"The toy coils (5, 6, 13, 14, 19, 20) and the Kenny flasher bulb are placed on the primitives the script animates, not on the coil bodies under the playfield.",
			"No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.",
			"The table models 29 G.I. sockets against the 31 playfield bulbs the G.I. page prints (its three GI lights in the turbo bumper caps sit on matrix lamps 38-40 and are excluded); the mirrored bottom-view drawing does not place the two it lacks.",
		],
		"promotion_decision": "partial: every used device has a placement or a controlled not-applicable record, but projections and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# South Park (Sega, 1999) spatial blockers", "",
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
		raise RuntimeError(f"Refusing to overwrite an author-ready South Park artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale South Park author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"South Park deterministic artifact drift: {path}")
	print("South Park definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"South Park extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("South Park retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
