"""Curate the physical Stern Terminator 3: Rise of the Machines (2003) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived
fact as a literal and reads committed inputs only: the placement seed (the retained table's object coordinates, rebuilt
by tools/terminator_3_spatial_seed.py), the compact runtime evidence (derived by tools/terminator_3_runtime_evidence.py)
and the excerpts. The term3 ROM's own Portals service tests print a name and wire colours for every switch, lamp and
coil; the builder reads those frames back from the runtime evidence and refuses to build unless each one agrees with the
manual's grids and coil chart, apart from the wording and wiring differences pinned below. ``--check`` refuses drift,
and ``--regenerate`` is the only path that writes the definition, its knowledge note and its spatial report.
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

MACHINE_ID = "stern.terminator-3-rise-of-the-machines.2003"
SLUG_PATH = "terminator-3-rise-of-the-machines-2003"
PARTIAL_PATH = ROOT / f"machines/partial/stern/{SLUG_PATH}.json"
AUTHOR_READY_PATH = ROOT / f"machines/author-ready/stern/{SLUG_PATH}.json"
KNOWLEDGE_PATH = ROOT / f"knowledge/stern/{SLUG_PATH}.md"
KNOWLEDGE_SEED_PATH = ROOT / f"tools/seeds/stern/{SLUG_PATH}-knowledge.md"
SPATIAL_SEED_PATH = ROOT / f"tools/seeds/stern/{SLUG_PATH}-spatial.json"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/stern/{SLUG_PATH}.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / f"reports/spatial/stern/{SLUG_PATH}.md"
RUNTIME_PATH = "evidence/runtime/whitestar/terminator-3-term3-service-tests-and-gameplay.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = "pinmame.catalog.46e1a01a0f73"
CORE_SOURCE = "pinmame.core.46e1a01a0f73"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
IDENTITY_SOURCE = "identity.stern.terminator-3-rise-of-the-machines.2003"
MANUAL_SOURCE = "manual.stern.terminator-3-rise-of-the-machines.2003"
VPX_TABLE_SOURCE = "vpx-table.terminator-3-hanibal-1-5"
VPX_SCRIPT_SOURCE = "vpx-script.terminator-3-hanibal-1-5"
VPX_EXTRACTION_SOURCE = "vpx-extraction.terminator-3-hanibal-1-5"
VPX_CORPUS_SIGGI_SOURCE = "vpx-script.1c88e99f0fa1319d"
VPX_CORPUS_HANIBAL_SOURCE = "vpx-script.33aaf9c0d4b89d15"
VPM_LIBRARY_SOURCE = "vpm-script-library.sega-vbs"
RUNTIME_SOURCE = "runtime.terminator-3.term3"
ROM_SOURCE = "rom.stern.terminator-3.4-00"
RUNTIME_LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "64503f35d34ec28a6bb69eaf2b77e6e870dfff988c49364b07c2c6f0ed5a76b6"
SEGAMES_SHA256 = "205dca0bd34d32c711aa99ac9c40dc02e91a0caaf3d3ccb1108f98aee03d69d4"
SE_SHA256 = "62a75510b900b98ae3d22b2c1e1eb41e7bcf582721375955a3cb5a6b24aef751"
CORE_C_SHA256 = "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00"
# Retained harness run directory -> SHA-256 of its manifest.json (tools/terminator_3_runtime_evidence.py pins the same values).
RUN_MANIFESTS = {
	"term3-switch-test": "2b56dc51fd0bf142e21cf0a0739fc7768f280d94740fb49457dd46a7fef6f9fa",
	"term3-dedicated-switch-test": "4392d52a214e4c203fa1a17cf1afdd51e1970e90a79c47ea188a1f9688d0e4b3",
	"term3-single-lamp-test": "850c1f3127882064b2d6a601b65a82b436d7f54443a0ed6a9c76ab332c56b63c",
	"term3-single-coil-test": "6d8dbaf14ff2b2398e4ea92b8f4289aac56f576294a97e1855d8581b8ae03749",
	"term3-stacking-opto": "9298cd4150c9b61fabf557a1ee9ce7b06caf6b5f9b7881d087127ee89f0875c2",
	"term3-ball-serve": "bb0df4fc125f28f535e4a1b8ffbab584301026f8559a9808597623d839fa4804",
	"term3-gameplay": "de605d80941a83534ca2c25625689db77f07181d5f63c63618c8fe4519a998b5",
}

TABLE_NAME = "Terminator 3 (Stern 2003) Hanibal v1.5.vpx"
TABLE_SHA256 = "73376fbd167c87f8057b28bf3cd7a3cddb4ec9dc452be7819bde28ffdd44b303"
SCRIPT_SHA256 = "33aaf9c0d4b89d15b57a0295f568f8fcce3381035f0749a9a0cd05981802e8b6"
HANIBAL_CORPUS_LF_SHA256 = "881d8506181263739065fe1f32283ec4278498577094a96700915eccb1652f93"
HANIBAL_CORPUS_PATH = "Terminator 3 (Stern 2003) Hanibal v1.5/VP10-Terminator 3 (Stern 2003) Hanibal v1.5.vbs.original"
SIGGI_SHA256 = "1c88e99f0fa1319d5435daf335adee5822154e3306aa18251e44f45611dab3de"
SIGGI_PATH = "Terminator 3 (Stern 2003) Siggi-TW VLM mod.vbs"
VPXTABLE_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
MANUAL_NAME = "Stern_2003_Terminator_3_Rise_of_the_Machines_Pinball_Game_Service_Manual.pdf"
MANUAL_SHA256 = "fc11f0a19bd78b83857de36338339fb598386b962f934fe47dfbe1696d5e1a9b"
IPDB_PAGE_NAME = "ipdb-4787-wayback.html"
IPDB_PAGE_SHA256 = "e91a2eb6504d61b83b807e4a57c75762f1676e8a23fcaecb3990c7886e6f10ca"
VPM_SEGA_SHA256 = "d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
PLAYFIELD_WIDTH = 1025.0
PLAYFIELD_HEIGHT = 2325.0
TABLE_BOUNDS = "left=0 top=0 right=1025 bottom=2325"

EXTRACTION_FILE_COUNT = 1166
EXTRACTION_TOTAL_BYTES = 89138527
EXTRACTION_MANIFEST_SHA256 = "bd30347a848250c81d6e15a066bdbfd367fe96215beb13ae39b2bb10c533b8d7"
EXTRACTION_RELATIVE_PATH = Path(f"stern/{SLUG_PATH}/hanibal-1-5/Terminator 3 (Stern 2003) Hanibal v1.5")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path(f"stern/{SLUG_PATH}/hanibal-1-5/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"
MANUALS_DIRECTORY = f"pinmame-manuals/by-machine/{MACHINE_ID}/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=4787"
MANUAL_URL = "https://www.ipdb.org/files/4787/" + MANUAL_NAME
MANUAL_WAYBACK_URL = "https://web.archive.org/web/20221024025923id_/" + MANUAL_URL
IPDB_WAYBACK_URL = "https://web.archive.org/web/20251124094710id_/" + IPDB_URL
EXCERPT_CREDIT = "curator, read from the rendered page"
QUOTE_CREDIT = "curator, quoted from the source file"
FRAME_CREDIT = "curator"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = (
	"term3", "term3_2", "term3_3", "term3f", "term3f_2", "term3f_3", "term3g", "term3g_3", "term3i", "term3i_2", "term3i_3",
	"term3l", "term3l_2", "term3l_3",
)
BASE_DRIVER_NOTE = (
	"src/wpc/segames.c builds every Terminator 3 driver from INITGAME(term3, GEN_WS, se_dmd128x32, SE_BOARDID_520_5068_01) "
	"(line 1368): GEN_WS, a 128x32 DMD, FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), lamp columns 2, no custom solenoids and the "
	"auxiliary driver board 520-5068-01 with three latched outputs. Every set runs on de_mSES2 with the same T3_SND sound ROMs "
	"(t3100.u7, t3100.u17, t3100.u21, t3100.u36 and t3100.u37) and init_term3, and se.c matches every set by the name prefix "
	"term3 for the fast-flip byte (CPU RAM 0x04) and the PWM bulb model. The controller routing, lamp columns and display are "
	"therefore identical; the sets differ in game code and display language. "
)
DISPLAY_ROMS = {
	"term3": ("4.00", "t3dispa.400", "6b7cc4f8", "English"), "term3l": ("4.00", "t3displ.400", "2e21caba", "Spanish"),
	"term3g": ("4.00", "t3dispg.400", "20da21b2", "German"), "term3f": ("4.00", "t3dispf.400", "0645fe6d", "French"),
	"term3i": ("4.00", "t3dispi.400", "e8ea9ab8", "Italian"),
	"term3_3": ("3.01", "t3dispa.300", "79b68a2f", "English"), "term3l_3": ("3.01", "t3displ.300", "2df35b3f", "Spanish"),
	"term3f_3": ("3.01", "t3dispf.300", "d5c68903", "French"), "term3g_3": ("3.01", "t3dispg.300", "9115ea52", "German"),
	"term3i_3": ("3.01", "t3dispi.300", "30573629", "Italian"),
	"term3_2": ("2.05", "t3dispa.201", "a314acd1", "English"), "term3l_2": ("2.05", "t3displ.201", "180b55a2", "Spanish"),
	"term3f_2": ("2.05", "t3dispf.201", "ced87154", "French"), "term3i_2": ("2.05", "t3dispi.201", "c1f3604f", "Italian"),
}
CPU_ROMS = {"4.00": ("t3cpu.400", "872f9351"), "3.01": ("t3cpu.301", "172a0b83"), "2.05": ("t3cpu.205", "219d8155")}


def _driver_note(driver_id: str) -> str:
	version, display, display_crc, language = DISPLAY_ROMS[driver_id]
	cpu, cpu_crc = CPU_ROMS[version]
	note = f"CPU {version} ({cpu}, CRC {cpu_crc}) with the {language} display ROM {display} (CRC {display_crc})."
	if version == "2.05":
		note += " Pinned PinMAME has no German 2.05 set."
	if driver_id == "term3":
		note += (
			" The retained table's script and both pinned corpus scripts load it (cGameName = \"term3\"), and every harness run "
			"booted it from empty NVRAM; its "
			"Portals service tests supply the ROM's own name and wire colours for each address."
		)
	else:
		note += " No harness run booted it."
	return note


# --- Switch data -------------------------------------------------------------------------------------
# address -> (label, grid name, mounting cell, part cell, switch type, availability, roles, pulse)
SWITCHES: dict[int, tuple[str, str, str, str, str, str, tuple[str, ...], bool]] = {
	1: ("Left Cabinet Button (UK Only)", "LEFT BUTTON (UK ONLY)", "Cabinet Side", "180-5160-00", "button", "optional", ("cabinet.uk-button-left",), False),
	2: ("4th Coin Slot", "4TH COIN SLOT", "Coin Door", "180-5204-00", "other", "optional", ("cabinet.coin.fourth",), True),
	3: ("6th Coin Slot (Future Use)", "6TH COIN SLOT", "Coin Door", "Future Use", "other", "unused", (), False),
	4: ("Right Coin Slot", "RIGHT COIN SLOT", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.right",), True),
	5: ("Center Coin Slot / DBA", "CENTER COIN SLOT / DBA", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.center",), True),
	6: ("Left Coin Slot", "LEFT COIN SLOT", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.left",), True),
	7: ("5th Coin Slot", "5TH COIN SLOT", "Coin Door", "Future Use", "other", "optional", ("cabinet.coin.fifth",), True),
	8: ("Right Cabinet Button (UK Only)", "RIGHT BUTTON (UK ONLY)", "Cabinet Side", "180-5160-00", "button", "optional", ("cabinet.uk-button-right",), False),
	10: ("Standup", "STANDUP", "Below P/F", "515-5967-06", "leaf", "used", (), True),
	11: ("4-Ball Trough 1 (Left)", "4-BALL TROUGH #1 (LEFT)", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	12: ("4-Ball Trough 2", "4-BALL TROUGH #2", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	13: ("4-Ball Trough 3", "4-BALL TROUGH #3", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	14: ("4-Ball Trough VUK Opto", "4-BALL TROUGH VUK OPTO", "Below P/F", "See Sw. Part Note", "opto", "used", ("ball.position",), False),
	15: ("4-Ball Stacking Opto", "4-BALL STACKING OPTO", "Below P/F", "See Sw. Part Note", "opto", "used", ("ball.path",), False),
	16: ("Shooter Lane", "SHOOTER LANE", "Below P/F", "500-6227-01", "microswitch", "used", ("ball.position",), False),
	17: ("Left 3-Bank Stand-Up Bottom", "LT 3-BANK S-U BOT", "Below P/F", "515-5162-02", "leaf", "used", (), True),
	18: ("Left 3-Bank Stand-Up Middle", "LT 3-BANK S-U MID", "Below P/F", "515-5162-02", "leaf", "used", (), True),
	19: ("Left 3-Bank Stand-Up Top", "LT 3-BANK S-U TOP", "Below P/F", "515-5162-02", "leaf", "used", (), True),
	20: ("Right 3-Bank Stand-Up Top", "RT 3-BANK S-U TOP", "Below P/F", "515-5162-02", "leaf", "used", (), True),
	21: ("Right 3-Bank Stand-Up Middle", "RT 3-BANK S-U MID", "Below P/F", "515-5162-02", "leaf", "used", (), True),
	22: ("Right 3-Bank Stand-Up Bottom", "RT 3-BANK S-U BOT", "Below P/F", "515-5162-02", "leaf", "used", (), True),
	23: ("Captive Ball", "CAPTIVE BALL", "Below P/F", "500-6139-02", "leaf", "used", (), True),
	24: ("Right Orbit Bottom", "RIGHT ORBIT BOTTOM", "Below P/F", "500-6227-02", "microswitch", "used", ("ball.path",), False),
	25: ("Drop Target", "DROP TARGET", "Below P/F", "180-5158-00", "microswitch", "used", ("position.down",), False),
	28: ("Left Orbit Bottom", "LEFT ORBIT BOTTOM", "Below P/F", "500-6227-02", "microswitch", "used", ("ball.path",), False),
	29: ("Left Orbit Top", "LEFT ORBIT TOP", "Below P/F", "500-6227-02", "microswitch", "used", ("ball.path",), False),
	30: ("Left Ramp", "LEFT RAMP", "Above P/F", "180-5190-48", "microswitch", "used", ("ball.path",), False),
	31: ("T-X Made", "T-X MADE", "Above P/F", "180-5190-28", "microswitch", "used", ("ball.path",), True),
	32: ("Right Ramp", "RIGHT RAMP", "Above P/F", "180-5190-48", "microswitch", "used", ("ball.path",), False),
	33: ("Lockup 1 (Right)", "LOCKUP 1 (RIGHT)", "Below P/F", "See Sw. Part Note", "opto", "used", ("ball.position",), False),
	34: ("Lockup 2", "LOCKUP 2", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	35: ("Lockup 3 (Left)", "LOCKUP 3 (LEFT)", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	36: ("VUK", "VUK", "Below P/F", "180-5116-01", "microswitch", "used", ("ball.position",), False),
	37: ("Left Top Lane", "LEFT TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	38: ("Middle Top Lane", "MIDDLE TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	39: ("Right Top Lane", "RIGHT TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	40: ("Center Ramp", "CENTER RAMP", "Above P/F", "180-5190-28", "microswitch", "used", ("ball.path",), False),
	41: ("Backbox 5-Bank Target Top", "BACKBOX 5-BANK (TOP)", "Backbox", "515-6027-08", "leaf", "used", ("cabinet.backbox",), True),
	42: ("Backbox 5-Bank Target 2", "BACKBOX 5-BANK 2", "Backbox", "515-6027-08", "leaf", "used", ("cabinet.backbox",), True),
	43: ("Backbox 5-Bank Target 3", "BACKBOX 5-BANK 3", "Backbox", "515-6027-08", "leaf", "used", ("cabinet.backbox",), True),
	44: ("Backbox 5-Bank Target 4", "BACKBOX 5-BANK 4", "Backbox", "515-6027-08", "leaf", "used", ("cabinet.backbox",), True),
	45: ("Backbox 5-Bank Target Bottom", "BACKBOX 5-BANK (BOT)", "Backbox", "515-6027-08", "leaf", "used", ("cabinet.backbox",), True),
	46: ("Right Orbit Top", "RIGHT ORBIT TOP", "Below P/F", "500-6227-01", "microswitch", "used", ("ball.path",), False),
	49: ("Left Bumper", "LEFT BUMPER", "Below P/F", "180-5015-03", "leaf", "used", (), True),
	50: ("Right Bumper", "RIGHT BUMPER", "Below P/F", "180-5015-03", "leaf", "used", (), True),
	51: ("Bottom Bumper", "BOTTOM BUMPER", "Below P/F", "180-5015-03", "leaf", "used", (), True),
	52: ("Skill Shot", "SKILL SHOT", "Backpanel", "180-5163-01", "unknown", "used", ("cabinet.rear-panel",), False),
	53: ("Tournament Start Button", "TOURNAMENT START", "In Cabinet", "180-5174-00", "button", "optional", ("cabinet.tournament-start",), False),
	54: ("Start Button", "START BUTTON", "In Cabinet", "180-5174-00", "button", "used", ("cabinet.start",), False),
	55: ("Gun Trigger", "GUN TRIGGER", "Gun on Cab.", "180-5111-00", "microswitch", "used", ("cabinet.launch",), False),
	56: ("Plumb Bob Tilt", "PLUMB BOB TILT", "In Cabinet", "See Sw. 56 Note", "tilt", "used", ("cabinet.tilt",), False),
	57: ("Left Outlane", "LEFT OUTLANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	58: ("Left Return Lane", "LEFT RETURN LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	59: ("Left Slingshot", "LEFT SLINGSHOT", "Below P/F", "180-5054-00 (x2)", "leaf", "used", (), True),
	60: ("Right Outlane", "RIGHT OUTLANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	61: ("Right Return Lane", "RIGHT RETURN LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	62: ("Right Slingshot", "RIGHT SLINGSHOT", "Below P/F", "180-5054-00 (x2)", "leaf", "used", (), True),
}
UNUSED_SWITCHES = (9, 26, 27, 47, 48, 63, 64)
DOTS_SWITCHES = (25, 36)
MATRIX_DRIVE = [("GRN-BRN", "CN5-P1"), ("GRN-RED", "CN5-P3"), ("GRN-ORG", "CN5-P4"), ("GRN-YEL", "CN5-P5"), ("GRN-BLK", "CN5-P6"), ("GRN-BLU", "CN5-P7"), ("GRN-VIO", "CN5-P8"), ("GRN-GRY", "CN5-P9")]
MATRIX_RETURN = [("WHT-BRN", "CN7-P9", "U400"), ("WHT-RED", "CN7-P8", "U400"), ("WHT-ORG", "CN7-P7", "U400"), ("WHT-YEL", "CN7-P6", "U400"), ("WHT-GRN", "CN7-P5", "U401"), ("WHT-BLU", "CN7-P3", "U401"), ("WHT-VIO", "CN7-P2", "U401"), ("WHT-GRY", "CN7-P1", "U401")]
# What the retained Hanibal 1.5 table's embedded script does with each address (line numbers of that script).
SWITCH_SCRIPT = {
	10: "sw10_Hit pulses 10 (line 975)",
	11: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 72-78): a cvpmBallStack holding 11 at 1 while a ball occupies that position",
	12: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 72-78)",
	13: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 72-78)",
	14: "bsTrough.InitSw 0, 14, 13, 12, 11 (lines 72-78): 14 is the exit position BallRelease empties, held at 1 while a ball waits there",
	15: "never written: no handler, ball stack or key names 15",
	16: "shooterlane_Hit and shooterlane_Unhit hold 16 while the ball sits on the trigger (line 290)",
	17: "sw17_Hit pulses 17 (line 978)", 18: "sw18_Hit pulses 18 (line 981)", 19: "sw19_Hit pulses 19 (line 984)",
	20: "sw20_Hit pulses 20 (line 988)", 21: "sw21_Hit pulses 21 (line 991)", 22: "sw22_Hit pulses 22 (line 994)",
	23: "sw23_Hit pulses 23 (line 997)",
	24: "sw24_Hit and sw24_Unhit hold 24 while the ball sits on the trigger (lines 928-929)",
	25: "cvpmDropTarget dtdroptarget (initdrop sw25, 25; lines 101-102) holds 25 at 1 while the target is down; sw25_hit knocks it down (line 999)",
	28: "sw28_Hit and sw28_Unhit hold 28 (lines 931-932)", 29: "sw29_Hit and sw29_Unhit hold 29 (lines 934-935)",
	30: "sw30_Hit and sw30_Unhit hold 30 (lines 937-938)",
	31: "txshot_hit pulses 31 and adds the ball to the lockup ball stack bstxhole (line 784)",
	32: "sw32_Hit and sw32_Unhit hold 32 (lines 940-941)",
	33: "bstxhole.InitSw 0, 33, 34, 35 (lines 92-95) holds 33 at 1 while a ball waits at the lockup's first position",
	34: "bstxhole.InitSw 0, 33, 34, 35 (lines 92-95) holds 34 at 1 while a second ball is locked",
	35: "bstxhole.InitSw 0, 33, 34, 35 (lines 92-95) holds 35 at 1 while a third ball is locked",
	36: "bsvuk.InitSw 0, 36 (lines 83-86) holds 36 while a ball waits; Tophole_hit adds the ball (line 780)",
	37: "sw37_Hit and sw37_Unhit hold 37 (lines 943-944)", 38: "sw38_Hit and sw38_Unhit hold 38 (lines 946-947)",
	39: "sw39_Hit and sw39_Unhit hold 39 (lines 949-950)", 40: "sw40_Hit and sw40_Unhit hold 40 (lines 952-953)",
	41: "sw41_Hit and sw41a_Hit pulse 41 (lines 617 and 627)", 42: "sw42_Hit and sw42a_Hit pulse 42 (lines 619 and 629)",
	43: "sw43_Hit and sw43a_Hit pulse 43 (lines 621 and 631)", 44: "sw44_Hit and sw44a_Hit pulse 44 (lines 623 and 633)",
	45: "sw45_Hit and sw45a_Hit pulse 45 (lines 625 and 635)",
	46: "sw46_Hit and sw46_Unhit hold 46 (lines 955-956)",
	49: "LBumper_Hit pulses 49 (line 912)", 50: "RBumper_Hit pulses 50 (line 917)", 51: "BBumper_Hit pulses 51 (line 921)",
	52: "sw52_Hit and sw52_Unhit hold 52 while the ball sits on the trigger (lines 958-959)",
	53: "the keyfront key writes 53 while held (lines 213 and 235)",
	55: "the plunger key writes 55 while held (lines 212 and 234)",
	56: "vpmNudge.TiltSwitch = 56 (line 183)",
	57: "sw57_Hit and sw57_Unhit hold 57 (lines 961-962)", 58: "sw58_Hit and sw58_Unhit hold 58 (lines 964-965)",
	59: "LeftSlingShot_Slingshot pulses 59 (line 274)",
	60: "sw60_Hit and sw60_Unhit hold 60 (lines 967-968)", 61: "sw61_Hit and sw61_Unhit hold 61 (lines 970-971)",
	62: "RightSlingShot_Slingshot pulses 62 (line 277)",
}
# Matrix switches the gameplay run closed in a game, with the outputs the ROM drove in response (step labels in the evidence).
GAMEPLAY_RESPONSE = {
	1: "holding it fired no coil and releasing it fired the drop-target trip coil 8; no UK auxiliary output 33-35 fired",
	8: "holding it fired the drop-target reset 3 and trip 8; no UK auxiliary output 33-35 fired",
	22: "closing it once blinked the backbox switched G.I. 4 and the G.I.",
	23: "closing it once blinked 4 and the G.I. and flashed 30, 31 and 32",
	24: "closing it once fired the left and center up posts 22 and 23",
	28: "closing it once fired the left and center up posts 22 and 23",
	29: "closing it once fired the left and center up posts 22 and 23",
	31: "closing it once blinked 4 and the G.I. and flashed 30, 31 and 32",
	39: "closing it once fired the drop-target reset 3",
	43: "closing it once fired the drop-target trip coil 8",
	44: "closing it once fired the drop-target reset 3",
	46: "closing it once fired the left and center up posts 22 and 23",
	49: "closing it once fired the left bumper 9",
	50: "closing it once fired the right bumper 10",
	51: "closing it once fired the bottom bumper 11",
	52: "closing it once fired the back-panel coil 21",
	57: "closing it once fired the kickback 12",
	59: "closing it once fired the left slingshot 17",
	62: "closing it once fired the right slingshot 18",
}
GAMEPLAY_QUIET = (10, 17, 18, 19, 20, 21, 30, 32, 37, 38, 40, 41, 42, 45, 58, 60, 61)


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
			text += f" at the Flupper dome primitive {entry['dome']}"
		if entry.get("projection"):
			text += f" (projection: {entry['projection']})"
		if entry.get("note"):
			text += f" ({entry['note']})"
		parts.append(text)
	return f" Placement from the retained table's {', '.join(parts)}." if parts else ""


def _unplaced_lamp_note(address: int) -> str:
	"""Note for a lamp the script binds to Lights that show no bulb mesh (the seed's lamp_unplaced), or an empty string."""
	entries = _spatial_seed()["lamp_unplaced"].get(str(address)) or []
	if not entries:
		return ""
	if any(entry["is_bulb_light"] and entry["show_bulb_mesh"] for entry in entries):
		raise RuntimeError(f"Terminator 3 lamp {address}: the seed lists a Light that shows its bulb mesh as unplaced")
	lights = " and ".join(f"{entry['object']} ({entry['binding']})" for entry in entries)
	plural = len(entries) > 1
	note = (
		f" The retained table's script drives the bulb-mode light{'s' if plural else ''} {lights}, which "
		f"{'show' if plural else 'shows'} no bulb mesh, so {'they mark' if plural else 'it marks'} no socket and the lamp is not placed."
	)
	near = [
		f"the toy primitive {primitive['object']} (image 'bulb', material {primitive['material']}) lies {primitive['distance']:g} from {entry['object']}"
		for entry in entries for primitive in entry["bulb_primitives"]
	]
	if near:
		note += (
			f" In the head {' and '.join(near)}; the record does not take "
			f"{'them as the lamp sockets' if len(near) > 1 else 'it as the lamp socket'} without a check against the lamp "
			"location drawing."
		)
	return note


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


OPTO_NOTE = (
	" Whitestar's switch_r hands the CPU ~core_getSwCol and term3 inverts no switch, so public 1 is the CPU's closed-contact "
	"reading. The opto board pages state the construction: with light on the receiver its output transistor is off and acts as "
	"an OPEN SWITCH, and when the beam is blocked it conducts and acts as a CLOSED SWITCH (OPTO Troubleshooting: 'CLOSED OPTO "
	"(Light Blocked) = SWITCH CLOSED'), so the contact rests open and a ball in the beam reads 1."
)


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	identifier = switch_id(address)
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
	notes = f"Printed switch-matrix drive column {column + 1}, return row {row + 1}."
	if address in UNUSED_SWITCHES:
		notes += (
			" The Switch Matrix Grid (DR. 4) prints this cell NOT USED in a black name cell with no mounting or part line, the "
			"location drawing marks no switch with this number, and the retained script never writes it."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE),
			aliases=aliases, normally_closed=False, pulse=False, physical={"notes": notes}, wiring=_switch_wiring(address),
			spatial=not_applicable("unused", MANUAL_SOURCE),
		)
	label, printed, mounting, part, switch_type, availability, roles, pulse = SWITCHES[address]
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": switch_type}
	match = re.fullmatch(r"(\d{3}-\d{4}-\d{2})(?: \(x2\))?", part)
	if match:
		physical["assembly_part_number" if part.startswith(("500-", "515-")) else "part_number"] = match.group(1)
	notes += f' The grid prints "{printed}" with mounting "{mounting}" and part "{part}".'
	if address in DOTS_SWITCHES:
		notes += " The cell carries the grid's DOTS (diode on terminal strip) box."
	if address in (59, 62):
		physical["quantity"] = 2
		notes += " Two parallel stack-blade contacts (Stack (Blade) Switch 180-5054-00, two per Slingshot Assembly 500-5849-00) share this matrix address."
	if address in (14, 15):
		notes += (
			" The grid's part note: 'Transmitter & Receiver OPTO PC Boards are used for Switches 14, 15 (Trans: 515-0173-00; Rec: "
			"515-0174-00)', the Trough Up-Kicker Dual OPTO boards of the 4-Ball Trough 500-6318-14, whose two circuits carry 14 "
			"and 15." + OPTO_NOTE
		)
	if address == 15:
		notes += (
			" In the stacking-opto harness run, with four balls on 11-14 in attract mode, raising 15 to 1 made the ROM fire the "
			"trough up-kicker 1 six times, about 0.8 s apart from 1.0 s after the rise, and then the auto launch 2 once, 9.1 s after "
			"the rise; lowering it fired nothing, and raising it again repeated the pattern."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 33:
		notes += (
			" The grid's part note: 'Transmitter & Receiver OPTO PC Boards are used for Switches ... 33 (Trans: 515-7307-00; Rec: "
			"515-7308-00)', the single opto of the TX Cannon Trough Assembly 500-6655-00. The single receiver repeats the dual "
			"receiver's circuit (the LED's photovoltage on a 2N5460 gate driving a 2N3906 output), though its parts list pairs the "
			"two transistor part numbers the other way round; the page prints no theory text of its own." + OPTO_NOTE
		)
	if address in (34, 35):
		notes += " The TX Cannon Trough Assembly 500-6655-00 holds the locked balls; the grid gives its two micro switches the trough part 180-5119-02."
	if address == 16:
		notes += (
			" A Roll-Over Left Bracket Assembly (500-6227-01, playfield switch parts page) in the shooter lane. The Diagnostic Aids "
			"page uses '#16 Shooter Lane & #2 Auto Launch' as its example of a switch whose coil the CPU activates about ten times "
			"while the switch stays closed. In the ball-serve run the up-kicker 1 served the ball, it rested on 16 for 10 s, and the "
			"ROM fired the auto launch 2 only after the gun trigger 55 was pulled. In the gameplay run the scenario closed 16 before "
			"the ROM had served a ball; the ROM never fired 1 and fired 2 0.76 s later, without a trigger pull, then every 1.6-1.7 s "
			"while the ball stayed on 16 and once 43 ms after the gun trigger was pulled, seven times in all, the last 0.18 s after "
			"the ball left."
		)
		refs += (RUNTIME_SOURCE,)
	if address in (24, 28, 29, 37, 38, 39, 46, 57, 58, 60, 61):
		notes += f" A Roll-Over {'Left' if part == '500-6227-01' else 'Right'} Bracket Assembly ({part}, playfield switch parts page)."
	if address in (17, 18, 19, 20, 21, 22):
		notes += " A 1-inch square red Switch & Target Assembly (515-5162-02, playfield switch parts page)."
	if address == 10:
		notes += " A 1-inch narrow yellow Switch & Target Assembly (515-5967-06, playfield switch parts page)."
	if address == 23:
		notes += (
			" The Modular S-U Target Square (Red) 500-6139-02 of the playfield switch parts page; the location drawing puts 23 at the "
			"captive ball, and IPDB lists a captive ball among the notable features."
		)
	if address == 25:
		notes += (
			" The Micro Switch (on Drop Target) 180-5158-00 of the 1-Bank Drop Target Assembly 500-6440-01, whose reset coil is Q3 "
			"and whose mini trip coil is Q8. In the gameplay run the target going down and coming back up each drew the trip coil 8."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 36:
		notes += (
			" The Micro Sw. (Heavy Duty 'Y' Flat Actuator) 180-5116-01 of the VUK Left Style Assembly 500-6290-00, labelled SW. 36 "
			"there. In the Switch Test run closing it fired the VUK coil 13, and in the gameplay run a ball resting on it drew 13 with "
			"3, 8 and 30."
		)
		refs += (RUNTIME_SOURCE,)
	if address in (33, 34, 35):
		notes += f" In the Switch Test run closing it fired the T-X VUK coil 14."
		refs += (RUNTIME_SOURCE,)
	if address == 33:
		notes += " In the gameplay run a ball resting on it drew 14 with the backbox switched G.I. 4 and flashers 26 and 30, and blinked the G.I."
	if address in (30, 32):
		notes += " A ramp micro switch 180-5190-48; the ramps page carries the same part on the shooter-lane steel ramp."
	if address in (31, 40):
		notes += " A ramp micro switch 180-5190-28 above the playfield."
	if address == 31:
		notes += (
			" The location drawing puts 31 (white) beside the lockup switches 33-35 nearer the rear rail; both retained scripts pulse "
			"31 as the ball enters the lockup."
		)
	if address in (41, 42, 43, 44, 45):
		physical["location"] = "backbox insert (RPG cannon targets)"
		notes += (
			" The location drawing's backbox-insert inset stacks 41-45 (grey, not on the playfield) beside a fan of five targets on "
			"the edge of the RPG cannon's arc. The Backbox Insert assembly (PDF page 113) lists four Stand-Up Targets 1\" X 1-1/2\" "
			"Rect. Wht 500-6698-08 (item 12, its callout on the SW. 41 target) and one 500-6698-08-79 (item 13, 'Identical to "
			"Item 12 EXCEPT the lugs are turned to the side (Required!)', its callout on the SW. 42 target). For individual parts "
			"it names the 'Switch & White Rectangular Target Sub-Assy. (515-6027-08)', the number the switch grid prints, so the "
			"grid gives each target's switch subassembly and the assembly page the whole target; the grid's number is recorded. "
			"The RPG Backbox Test names them the BACKBOX SWITCHES and draws a box per target. IPDB: 'Backbox reciprocating cannon "
			"shoots Delrin Ball horizontally at 5 targets'."
		)
		refs += (IDENTITY_SOURCE,)
	if address in (49, 50, 51):
		notes += " The bumper assembly page lists the stack switch 180-5015-03 and labels 'SW. 49 Left', 'SW. 50 Right' and 'SW. 51 Bot.'; the location drawing puts 49, 50 and 51 at the three bumpers."
	if address == 52:
		physical["location"] = "back panel, under the back-panel trough"
		notes += (
			" The location drawing marks 52 grey (not on the playfield) outside the rear rail, and its back-panel inset notes 'Switch "
			"52 located behind the Back Panel, under the Back Panel Trough.' The part 180-5163-01 names a switch type the manual's "
			"assembly pages do not show, so the switch type is left unknown. The back panel's Kicker (Ball Stop) Assembly holds "
			"the ball in that trough while Q21 is energized."
		)
	if address in (3, 7):
		notes += " The cabinet wiring diagram's coin door block prints it 'Future Use' (WHT-ORG CN7 pin 7 for the 6th slot, WHT-VIO CN7 pin 2 for the 5th)."
	if address == 3:
		notes += (
			" The term3 ROM ignores this position: its Portals Switch Test still prints NONE while it is closed, so no switch is fitted "
			"and none would be read."
		)
	if address == 7:
		notes += " The term3 ROM's Switch Test names the position, so an operator-fitted coin switch would be read; no switch is fitted by default."
	if address == 2:
		notes += " The cabinet wiring diagram labels this input '4th Coin Slot European Use' (WHT-RED, CN7 pin 8)."
	if address in (1, 8):
		side = "Left" if address == 1 else "Right"
		notes += (
			" UK only: the cabinet wiring diagram's boxed note reads 'UK ONLY: 2 Extra Cabinet Buttons for the Post Save™ Feature are "
			"used. The Left Button operates the Left Outlane Ball Deflector. The Right Button operates the Right Outlane Ball "
			"Deflector. Both buttons pushed together operate the Center Up/Down Post. Both buttons are located under the Flipper "
			f"Buttons.' It draws the {side.upper()} BUTTON as N.O. on GRN-BRN (CN5 pin 1) and "
			f"{'WHT-BRN (CN7 pin 9)' if address == 1 else 'WHT-GRY (CN7 pin 1)'}, as the grid does. The grid prints the name on a "
			"light grey band, and the location drawing does not draw it. The retained table never writes it."
		)
		refs += (VPX_SCRIPT_SOURCE,)
	if address == 53:
		notes += (
			" The cabinet wiring diagram draws the TOURNIE BUTTON, N.O., on WHT-GRN (CN7 pin 5) and SW DRIVE 7, with its lamp 'Lamp 54 "
			"Tournie'; the location drawing marks 53 grey at the front centre with the note 'Optional Tournament Kit Required', and "
			"the front page names an optional Tournament Kit."
		)
	if address == 54:
		notes += (
			" The cabinet wiring diagram draws the START BUTTON, N.O., on WHT-BLU (CN7 pin 3) and SW DRIVE 7, with its lamp 'Lamp 53 "
			"Start'; the location drawing marks 54 grey at the cabinet's left front. sega.vbs's swStartButton = 54 is what the "
			"VPinMAME Start key writes. In the ball-serve and gameplay runs a press after four coins started a game: the ROM fired "
			"the drop-target reset 3, flashed 30-32 and blinked the G.I., and raised the game-on state 15 about 5.4 s after the "
			"press; in the ball-serve run it then kicked the trough up-kicker 1."
		)
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE)
	if address == 55:
		notes += (
			" The Gun Shooter Connector Assembly 500-5698-02-79 carries the Micro Sw. w/Lg Roller Actuator (Happ) 180-5111-00; when "
			"the gun is not wanted, the Ball Launch Button 500-6709-06-79 with micro switch 180-5111-01 and a #555 bulb takes its "
			"place. IPDB lists the gun handle on the front of the cabinet among the toys. sega.vbs names 55 swSlamTilt, a generic "
			"Whitestar assignment: this game's grid prints no slam tilt, so the VPinMAME slam-tilt key would pull the gun trigger. "
			"In the ball-serve and gameplay runs a pull fired the auto launch 2 with the drop-target trip coil 8 and the T-X "
			"flashers 26."
		)
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE)
	if address == 56:
		notes += (
			" The grid's Switch 56 Part Note: 'The Switch is comprised of a Hanger Bracket (535-5319-00) and Contact Wire "
			"(535-7563-01) located in the Cabinet.' The cabinet wiring diagram draws the PLUMB BOB TILT, N.O., on WHT-GRY (CN7 pin "
			"1) and GRN-VIO (CN5 pin 8). sega.vbs's swTilt = 56."
		)
		refs += (VPM_LIBRARY_SOURCE,)
	if address in (4, 5, 6):
		notes += (
			f" The cabinet wiring diagram's coin door block prints '{ {4: 'Right Coin Slot', 5: 'U.S. Bill Acceptor Center Coin Slot', 6: 'Left Coin Slot'}[address] }' "
			f"on {'WHT-YEL (CN7 pin 6)' if address == 4 else 'WHT-GRN (CN7 pin 5)' if address == 5 else 'WHT-BLU (CN7 pin 3)'} and SW DRIVE 1. "
			f"sega.vbs maps its coin keys to {'swCoin3 = 4' if address == 4 else 'swCoin1 = 5' if address == 5 else 'swCoin2 = 6'}."
		)
		refs += (VPM_LIBRARY_SOURCE,)
	if address == 5:
		notes += " In the ball-serve and gameplay runs each coin on 5 pulsed the optional coin-meter output 24 four times."
		refs += (RUNTIME_SOURCE,)
	if address in SWITCH_SCRIPT:
		notes += f" Retained table script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in GAMEPLAY_RESPONSE:
		notes += f" In the gameplay run, {GAMEPLAY_RESPONSE[address]}."
		refs += (RUNTIME_SOURCE,)
	elif address in GAMEPLAY_QUIET:
		notes += " The gameplay run closed it once in a game and the ROM fired no coil or flasher in response, which says nothing against its fitment."
		refs += (RUNTIME_SOURCE,)
	extra: dict[str, Any] = {"aliases": aliases, "normally_closed": False, "pulse": pulse, "wiring": _switch_wiring(address)}
	if roles:
		extra["roles"] = list(roles)
	if address in (11, 12, 13, 14):
		extra["initial_active"] = True
	if availability == "unused":
		physical["location"] = "coin door"
		extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
	elif any(role.startswith("cabinet.") for role in roles):
		physical.setdefault("location", "coin door" if mounting == "Coin Door" else "cabinet")
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
	-2: ("Volume / Service Left (Red)", "#6 VOLUME (RED BUTTON) (In Test: LEFT)", "GRY-BLU", "CN6-P8", "coin door", "180-5192-02", ("service.left",), "used", False),
	-1: ("Service Credit / Service Right (Green)", "#7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT)", "GRY-VIO", "CN6-P9", "coin door", "180-5192-04", ("service.right",), "used", False),
	0: ("Begin Test / Service Enter (Black)", "#8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER)", "GRY-BLK", "CN6-P10", "coin door", "180-5192-00", ("service.enter",), "used", False),
	81: ("Right Flipper End-of-Stroke", "#4 RIGHT FLIPPER E.O.S. (End-of-Stroke)", "GRY-YEL", "CN6-P6", "playfield, on the right flipper assembly", "180-5149-00", ("flipper.lower.right.eos",), "used", True),
	82: ("Right Flipper Button", "#3 RIGHT FLIPPER BUTTON", "GRY-ORG", "CN6-P4", "cabinet", "180-5160-00", ("flipper.lower.right.button",), "used", False),
	83: ("Left Flipper End-of-Stroke", "#2 LEFT FLIPPER E.O.S (End-of-Stroke)", "GRY-RED", "CN6-P3", "playfield, on the left flipper assembly", "180-5149-00", ("flipper.lower.left.eos",), "used", True),
	84: ("Left Flipper Button", "#1 LEFT FLIPPER BUTTON", "GRY-BRN", "CN6-P2", "cabinet", "180-5160-00", ("flipper.lower.left.button",), "used", False),
}
DEDICATED_INPUT = {-2: "DS-6", -1: "DS-7", 0: "DS-8", 81: "DS-4", 82: "DS-3", 83: "DS-2", 84: "DS-1"}


def dedicated_id(address: int) -> str:
	name = f"n{-address}" if address < 0 else str(address)
	return f"switch.{name}-{slug(DEDICATED[address][0])}"


def _dedicated(address: int) -> dict[str, Any]:
	label, printed, wire, connector, location, part, roles, availability, normally_closed = DEDICATED[address]
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
			"The cabinet/coin door wiring diagram (PDF page 126) draws the Memory Protect Switch, N.O., from CPU board CN6 pin 12 "
			"(BLK-RED). se.c's ram_w refuses writes to the protected RAM while public -3 is 1, and sega.vbs names the address "
			"swMemoryProtect; a closed coin door is public -3 at 1 and an open door 0. The Diagnostic Aids page: opening the Coin "
			"Door after a CMOS RAM failure 'will initiate a Factory Restore (Reset), by opening the Memory Protect Switch'."
		)
		refs += (VPM_LIBRARY_SOURCE,)
		extra: dict[str, Any] = {"initial_active": True, "wiring": {"board": "Whitestar CPU/Sound board memory-protect input", "drive_wire": wire, "drive_connection": connector}}
	else:
		notes = (
			f"Printed dedicated switch {DEDICATED_INPUT[address]} ({printed}), wired {wire} to {connector} on IC U206's inputs and "
			"returned to ground (BLK, CN6-P1/-P11). se.c's dedswitch_r swaps PinMAME's flipper column into U206's order and returns "
			"the complement, so public 1 is a closed contact."
		)
		extra = {"wiring": {"board": "Whitestar CPU/Sound board dedicated-switch input", "drive_wire": wire, "drive_connection": connector, "return_wire": "BLK", "return_connection": "CN6-P1/-P11", "return_component": "U206"}}
	if address in (-2, -1, 0):
		notes += " The cabinet wiring diagram draws it, N.O., among the PORTALS™ SERVICE BUTTONS on the coin door."
	if address in (81, 83):
		side = "right" if address == 81 else "left"
		notes += (
			f" The grid prints its mounting 'Below Playfield' and its part '180-5149-00 on Flipper'; the 2-Flipper Circuit Wiring "
			f"Diagram (PDF page 124) draws it 'ON ASSY.' as an N.C. switch, and the {side} Flipper Assembly "
			f"({'500-6682-02' if address == 81 else '500-6682-12'}) lists the EOS switch 180-5149-00. The diagram explains that the "
			"switch opens about 1/16\" when the flipper is energized and that the CPU applies another 40 ms pulse when it sees the "
			"switch close during a hold. normally_closed records that construction: at rest the contact is closed. PinMAME does not "
			"pass that level through: term3 declares FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), core.h defines FLIP_SOL(x) to include "
			"FLIP_EOS(x), and core.c's flipper update therefore rewrites this input on every update, 0 while the flipper solenoid is "
			"off and 1 once it has been on for CORE_FLIPSTROKETIME (2) updates. PinMAME's model reads open at rest and closed at the "
			"end of the stroke, the opposite of the construction, and a host write never reaches the ROM: in the Dedicated Switch "
			"Test run holding it left the display at NONE, and in the gameplay run host writes of 1 and 0 to "
			f"{'this input' if address == 83 else 'the left end-of-stroke input 83'} while the left flipper button was held changed "
			"no output. A consumer receives PinMAME's simulated level and need not write this input. The retained script never "
			f"writes it; sega.vbs names this address {'swURFlip' if address == 81 else 'swULFlip'}, an upper-flipper label it writes "
			"only when an upper flipper solenoid is registered, which the retained table does not do."
		)
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE)
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE,)
	elif address in (82, 84):
		notes += (
			f" The grid prints its mounting 'on Cabinet Side' and part 180-5160-00. The flipper column bit PinMAME's flipper update "
			f"copies into the lower-flipper outputs; sega.vbs writes it from the {'right' if address == 82 else 'left'} flipper key "
			f"(swLRFlip = 82, swLLFlip = 84). In the gameplay run holding it made the ROM pulse "
			f"{'45 and 46' if address == 82 else '47 and 48'}."
		)
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE)
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, availability, refs, aliases=aliases, normally_closed=normally_closed,
		pulse=False, roles=list(roles), physical=physical, **extra)


DIP_COUNTRIES = (
	"USA all off; Austria 1; Australia 1, 3, 4; Belgium 2; Canada 1, 2; Denmark 1, 4; Finland 1, 3; France 2, 3; Germany 1, 2, 3; "
	"Greece 1-4; Italy 4; Netherlands 3; New Zealand 5; Norway 2, 4; Portugal 1, 5; Spain 2, 5; Sweden 1, 2, 4; Switzerland 3, 4; UK 2, 3, 4"
)


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
		"switch.88-not-used-ds-5", "Not Used Dedicated Input DS-5", "switch", SWITCH_GROUP, 88, "unused",
		(MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.switch", "value": "88"}, {"namespace": "manual.address", "value": "DS-5"}], normally_closed=False, pulse=False,
		physical={"notes": (
			"dedswitch_r routes the flipper column's upper-flipper button bit to U206 input 5 (DS-5). The grid's dedicated-switch "
			"column prints DS-5 NOT USED in a black name cell (GRY-GRN, CN6-P7), the cabinet wiring diagram draws no switch on CN6 "
			"pin 7, and term3 declares no upper flipper."
		)},
		wiring={"board": "Whitestar CPU/Sound board dedicated-switch input", "drive_wire": "GRY-GRN", "drive_connection": "CN6-P7", "return_component": "U206"},
		spatial=not_applicable("unused", MANUAL_SOURCE),
	))
	for number in range(1, 9):
		used = number <= 5
		items.append(_device(
			f"switch.dip-{number}", f"SW300 Country Setting Position {number}" if used else f"Unused SW300 Position {number}", "dip_switch", DIP_GROUP, number,
			"used" if used else "unused", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": str(number)}, {"namespace": "manual.address", "value": f"SW300-{number}"}],
			physical={"switch_type": "dip", "location": "Whitestar CPU/Sound board SW300 (right of CN6, top middle)", "notes": (
				f"Position {number} of the eight-position CPU DIP switch SW300. se.c's dip_r returns the complement of PinMAME DIP bank 0. "
				f"The manual's CPU Country Setting charts (DR. 3) set positions 1-5 for nineteen countries ({DIP_COUNTRIES}) and never "
				"turn 6-8 on. sega.vbs's DIP form covers only mask 0x0f, so it cannot set position 5 (New Zealand, Portugal, Spain), "
				"and three of its labels (0x05 UK, 0x09 Japan, 0x0d Brazil) name other countries than this game's chart (Finland, "
				"Denmark, Australia; the UK is 2, 3 and 4 on, its 'UK (New)'); follow the chart." if used else
				f"Position {number} of the eight-position CPU DIP switch SW300. No country chart on DR. 3 turns positions 6-8 on; PinMAME "
				"publishes the full eight-address bank regardless.")},
			spatial=not_applicable("dip_switch", MANUAL_SOURCE),
		))
	return items


# --- Solenoid data -------------------------------------------------------------------------------------
# Q number -> (label, printed name, kind, availability, coil/bulb cell, power wire, power connection, voltage, voltage type, control wire, control connection)
YV = ("YEL-VIO", "J10-P4/5", 50, "dc")
BR = ("BRN", "J7-P1", 20, "dc")
OR = ("ORG", "J6-P10", 20, "dc")
NONE = (None, None, None, None)
Q_OUTPUTS: dict[int, tuple[Any, ...]] = {
	1: ("Trough Up-Kicker", "TROUGH UP-KICKER", "coil", "used", "26-1200 / 090-5044-00B", *YV, "BRN-BLK", "J8-P1"),
	2: ("Auto Launch", "AUTO LAUNCH", "coil", "used", "22-1080 / 090-5032-00B", *YV, "BRN-RED", "J8-P3"),
	3: ("Drop Target Reset", "DROP TARGET RESET", "coil", "used", "27-1500 / 090-5004-00B", *YV, "BRN-ORG", "J8-P4"),
	4: ("Backbox RPG Switched G.I.", "BACKBOX RPG SW. GI", "gi", "used", "#44 Bulb x8 / 090-5000-44", "GRY / GRY-GRN", "J17-P2/3", 19, "ac", "BRN-YEL", "J8-P5"),
	5: ("Backbox Kicker", "BACKBOX KICKER", "coil", "used", "23-800 / 090-5001-00B", *YV, "BRN-GRN", "J8-P6"),
	6: ("Not Used Driver Q6", "NOT USED", "coil", "unused", "", *NONE, "BRN-BLU", "J8-P7"),
	7: ("Not Used Driver Q7", "NOT USED", "coil", "unused", "", *NONE, "BRN-VIO", "J8-P8"),
	8: ("Drop Target Down", "DROP TARGET DOWN", "coil", "used", "32-1250 / 515-6916-01", *YV, "BRN-GRY", "J8-P9"),
	9: ("Left Bumper", "LEFT BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-BRN", "J9-P1"),
	10: ("Right Bumper", "RIGHT BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-RED", "J9-P2"),
	11: ("Bottom Bumper", "BOTTOM BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-ORG", "J9-P4"),
	12: ("Kickback", "KICKBACK", "coil", "used", "23-800 / 090-5001-00B", *YV, "BLU-YEL", "J9-P5"),
	13: ("VUK", "VUK", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-GRN", "J9-P6"),
	14: ("T-X VUK", "T-X VUK", "coil", "used", "26-1200 / 090-5044-00B", *YV, "BLU-BLK", "J9-P7"),
	15: ("Left Flipper", "LEFT FLIPPER (50v RED/YEL)", "coil", "used", "22-1080 / 090-5032-00T", "GRY-YEL~3A Fuse~RED-YEL", "J10-P1/2", 50, "dc", "ORG-GRY", "J9-P8"),
	16: ("Right Flipper", "RIGHT FLIPPER (50v RED/YEL)", "coil", "used", "22-1080 / 090-5032-00T", "BLU-YEL~3A Fuse~RED-YEL", "J10-P1/2", 50, "dc", "ORG-VIO", "J9-P9"),
	17: ("Left Slingshot", "LEFT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "VIO-BRN", "J7-P2"),
	18: ("Right Slingshot", "RIGHT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "VIO-RED", "J7-P3"),
	19: ("Not Used Driver Q19", "NOT USED", "coil", "unused", "", *NONE, "VIO-ORG", "J7-P4"),
	20: ("Backbox Motor Relay", "BACKBOX MOTOR RELAY", "relay", "used", "Relay / 500-6700-00", *BR, "VIO-YEL", "J7-P6"),
	21: ("Back Panel Diverter", "BACK PANEL DIVERTER", "coil", "used", "26-1200 / 090-5044-00B", *BR, "VIO-GRN", "J7-P7"),
	22: ("Left Up Post", "LEFT UP POST", "coil", "used", "26-1200 / 090-5044-00T", *BR, "VIO-BLU", "J7-P8"),
	23: ("Center Up Post", "CENTER UP POST", "coil", "used", "26-1200 / 090-5044-00T", *BR, "VIO-BLK", "J7-P9"),
	24: ("Optional Coil (Coin Meter)", "OPTIONAL COIL", "coil", "optional", "Opt. 5v", "RED", "J16-P7", 5, "dc", "VIO-GRY", "J7-P10"),
	25: ("Not Used Driver Q25", "NOT USED", "coil", "unused", "", *NONE, "BLK-BRN", "J6-P1"),
	26: ("T-X Flashers (X2)", "FLASH:  T-X X2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-RED", "J6-P2"),
	27: ("Backbox Left Flashers (X4)", "FLASH:  BACK BOX LEFT X4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-ORG", "J6-P3"),
	28: ("Backbox Right Flashers (X4)", "FLASH:  BACK BOX RIGHT X4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-YEL", "J6-P4"),
	29: ("Super Jackpot Flasher", "FLASH:  SUPER JP", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-GRN", "J6-P5"),
	30: ("Back Panel Flashers (X4)", "FLASH:  BACK PANEL X4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-BLU", "J6-P6"),
	31: ("Mid Left and Right Flashers (X2)", "FLASH:  MID L&R X2", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-VIO", "J6-P7"),
	32: ("Bottom Left and Right Flashers (X2)", "FLASH:  BOT L&R X2", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-GRY", "J6-P8"),
}
PUBLIC_BINDING = {15: 48, 16: 46}
CABINET_ROLES = {4: "cabinet.backbox", 5: "cabinet.backbox", 20: "cabinet.backbox", 21: "cabinet.rear-panel", 24: "cabinet.coin-meter", 27: "cabinet.backbox", 28: "cabinet.backbox", 30: "cabinet.rear-panel"}
FLASHER_QUANTITY = {26: 2, 27: 4, 28: 4, 29: 1, 30: 4, 31: 2, 32: 2}
OUTPUT_LOCATIONS = {
	4: "backbox insert, eight small lamps around the RPG cannon's arc",
	5: "backbox insert, RPG cannon kicker",
	20: "backbox insert, RPG cannon motor relay",
	21: "back panel, ball stop in the back-panel trough",
	24: "cabinet (coin meter, when fitted)",
	26: "two at the T-X figure (rear left), blue mini-mars",
	27: "backbox insert, four down its left side",
	28: "backbox insert, four down its right side",
	29: "below the playfield at the centre",
	30: "back panel, four across its top row, red mini-mars",
	31: "two at mid-field, left and right, red mini-mars",
	32: "two at the slingshots' outer ends, red mini-mars",
}
# What the retained table does with each callback (embedded script line numbers).
SOLENOID_SCRIPT = {
	1: "Solcallback(1) = \"bstrough.solout\" (line 310) kicks the trough ball stack out of BallRelease (lines 72-78)",
	2: "Solcallback(2) = \"Auto_plunger\" (line 311) fires the cvpmImpulseP plungerIM on the shooter-lane trigger swplunger (PlungerIM.AutoFire, lines 294-304)",
	3: "Solcallback(3) = \"dtdroptarget.soldropup\" (line 312) raises the drop target sw25",
	4: "Solcallback(4) = \"Flash4\" (line 313) switches the backbox RPG lights (lines 1091-1098)",
	5: "Solcallback(5) = \"sol5\" (line 314, commented '5 backbox kicker') calls kickit only while a ball is in the backbox (lines 884-887)",
	8: "Solcallback(8) = \"dtdroptarget.solhit 1,\" (line 315) knocks the drop target down",
	9: "no callback: LBumper is a VPX bumper that fires itself",
	10: "no callback: RBumper is a VPX bumper that fires itself",
	11: "no callback: BBumper is a VPX bumper that fires itself",
	12: "Solcallback(12) = \"sol12\" (line 316) fires the plunger Kickback and pulls it back on release (lines 767-773); it starts pulled back (line 193)",
	13: "Solcallback(13) = \"bsvuk.solout\" (line 317) kicks the VUK ball stack out of vukout (lines 83-86)",
	14: "Solcallback(14) = \"bstxhole.solout\" (line 318) kicks the lockup ball stack out of tvukout (lines 92-95)",
	17: "no callback: LeftSlingShot is a VPX slingshot wall that fires itself",
	18: "no callback: RightSlingShot is a VPX slingshot wall that fires itself",
	20: "Solcallback(20) = \"Sol20\" (line 319) runs sol20timer while energized (lines 833-847; the timer at line 360)",
	21: "Solcallback(21) = \"sol21\" (line 320) drops the wall Bwdiverter1 and raises Bwdiverter1a while energized and restores both on release (lines 870-877); Bwdiverter1a starts dropped (line 191)",
	22: "Solcallback(22) = \"sol22\" (line 321) raises the wall LeftPost while energized and drops it on release (lines 805-811); it starts dropped (line 190)",
	23: "Solcallback(23) = \"sol23\" (line 322) raises the wall CenterPost while energized and drops it on release (lines 819-825); it starts dropped (line 189)",
	26: "Solcallback(26) = \"Flash26\" (line 323) lights the objects Flasher26a-c (lines 1110-1114), which are not bulb Lights",
	27: "Solcallback(27) = \"Flash27\" (line 324) lights the backbox flashers (lines 1125-1133)",
	28: "Solcallback(28) = \"Flash28\" (line 325) lights the backbox flashers (lines 1145-1148)",
	29: "Solcallback(29) = \"\"'\"SetLamp 129,\" (line 328) leaves it unbound, so the table draws nothing for it",
	30: "Solcallback(30) = \"Flash30\" (line 329) lights the four back-panel flashers Flasher30a-d and their domes (lines 1159-1173)",
	31: "Solcallback(31) = \"Flash31\" (line 330) lights the bulb Lights Flasher31a and Flasher31b (lines 1193-1200)",
	32: "Solcallback(32) = \"Flash32\" (line 331) lights the bulb Lights Flasher32a and Flasher32b (lines 1213-1217)",
}
# What the harness runs showed for each output (evidence step labels).
SOLENOID_RUNTIME = {
	1: (
		"the ROM fired it 0.7 s after the game-on state rose in the ball-serve run, and in the stacking-opto run six times, about "
		"0.8 s apart, each time 15 was raised in attract mode; in the gameplay run, where the scenario put a ball on 16 before the "
		"ROM served one, it never fired"
	),
	2: (
		"in the stacking-opto run it fired once, 9.1 s after each rise of 15 in attract mode, after the six fires of 1; in the "
		"ball-serve run the served ball rested on 16 for "
		"10 s and the ROM fired it 81 ms after the gun trigger 55 was pulled, then again 1.67 s and 3.34 s after that; in the "
		"gameplay run, where the ball reached 16 before the ROM served one, it fired 0.76 s later without a trigger pull, then "
		"every 1.6-1.7 s while the ball stayed on 16 and once 43 ms after the gun trigger was pulled, seven times in all, the last "
		"0.18 s after the ball left"
	),
	3: "it fired at power-up, on Start, at the drain, with the right top lane 39, the backbox target 44, a ball in the VUK 36 and while the UK right button 8 was held",
	4: (
		"the ROM switched it on during boot in every run; it switched it off and on with the G.I. after Start, with the right "
		"3-bank 22, the captive ball 23, T-X made 31 and while a ball sat at lockup 1 (33), and off with the G.I. at the drain"
	),
	5: "only the Single Coil Test fired it",
	8: "it fired three times from about 1.6 s after the gun trigger launched the ball, with the backbox target 43, when the drop target 25 went down and when it came back up, with a ball in the VUK 36, when the UK left button 1 was released and while the UK right button 8 was held",
	9: "it answered the left bumper switch 49",
	10: "it answered the right bumper switch 50",
	11: "it answered the bottom bumper switch 51",
	12: "it answered the left outlane switch 57",
	13: "it answered the VUK switch 36 in the Switch Test and a ball resting on 36 in the gameplay run",
	14: "it answered each of the lockup switches 33, 34 and 35 in the Switch Test and a ball resting on 33 in the gameplay run",
	17: "it answered the left slingshot switch 59",
	18: "it answered the right slingshot switch 62",
	20: "only the Single Coil Test fired it",
	21: "it answered the skill shot switch 52",
	22: "the ROM held it and 23 on for about 2.1 s each, starting within 0.5 s of each other, whenever one of the orbit switches 24, 28, 29 or 46 closed",
	23: "the ROM held it and 22 on for about 2.1 s each, starting within 0.5 s of each other, whenever one of the orbit switches 24, 28, 29 or 46 closed",
	24: "each coin on the center slot 5 pulsed it four times",
	26: (
		"it lit about 1.6 s after the gun trigger was pulled (in the gameplay run it then stayed lit for 15.8 s), and again "
		"while a ball sat at lockup 1 (33), for 14.5 s"
	),
	27: "only the Single Coil Test fired it",
	28: "only the Single Coil Test fired it",
	29: "only the Single Coil Test fired it",
	30: "it flashed after Start, with the captive ball 23, T-X made 31, a ball in the VUK 36 and a ball at lockup 1 (33)",
	31: "it flashed after Start, with the captive ball 23 and T-X made 31",
	32: "it flashed after Start, with the captive ball 23 and T-X made 31",
}


def q_output_id(number: int) -> str:
	return f"device.q{number}-{slug(Q_OUTPUTS[number][0])}"


def _q_wiring(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, voltage_type, control_wire, control_connection = Q_OUTPUTS[number]
	wiring: dict[str, Any] = {"board": "Whitestar I/O Power Driver board 520-5137-01", "driver_transistor": f"Q{number}", "control_wire": control_wire, "control_connection": control_connection}
	if power_wire:
		wiring["power_wire"] = power_wire
		wiring["power_connection"] = power_connection
		wiring["nominal_voltage_v"] = voltage
		wiring["voltage_type"] = voltage_type
	return wiring


def _q_output(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, voltage_type, control_wire, control_connection = Q_OUTPUTS[number]
	address = PUBLIC_BINDING.get(number, number)
	identifier = q_output_id(number)
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {}
	notes = f'Coils Detailed Chart Table (DR. 6) row #{number} "{printed}": drive transistor Q{number}'
	notes += f', cell "{part}".' if part else ", with blank power and coil cells and a dark grey name cell."
	if availability == "unused":
		notes += (
			" The coil and flash lamp location drawing (DR. 7) does not draw it, the retained script registers no callback for it, "
			"and the only run that fired it is the Single Coil Test, which fires every driver."
		)
		physical["notes"] = notes
		return _device(identifier, label, kind, SOLENOID_GROUP, address, "unused", refs + (VPX_SCRIPT_SOURCE, RUNTIME_SOURCE), physical=physical,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Q{number}"}],
			wiring=_q_wiring(number), spatial=not_applicable("unused", MANUAL_SOURCE))
	coil_part = part.split(" / ")[-1]
	if re.fullmatch(r"(090|165)-\d{4}-\d{2}[A-Z]?", coil_part) and number != 4:
		physical["part_number"] = coil_part
	elif re.fullmatch(r"515-\d{4}-\d{2}", coil_part):
		physical["part_number"] = coil_part
	elif number == 20:
		physical["assembly_part_number"] = "500-6700-00"
	if number in OUTPUT_LOCATIONS:
		physical["location"] = OUTPUT_LOCATIONS[number]
	if number in FLASHER_QUANTITY:
		physical["quantity"] = FLASHER_QUANTITY[number]
	if kind == "flasher":
		notes += (
			" The chart's note: 'In Test Flash Lamps Menu (\"Flash\" Icon), Flashers tested are all Flash Lamps located between Q1-Q32 "
			"(This Game: Q26-Q32)'. se.c gives every term3 set the #89 20v DC bulb model on 26-32."
		)
	if number in (31, 32):
		notes += " The chart prints #906 bulbs (165-5004-00) for this row, so PinMAME's #89 model is an approximation of these two sockets."
	if number in (26, 27, 28, 29, 30, 31, 32):
		notes += f" Where the coil and flash lamp location drawing (DR. 7) draws it: {OUTPUT_LOCATIONS[number]}."
	if number == 26:
		notes += " The TX Head, Arm and Cannon assembly page lists the Q26 sockets with #89 bulbs at the T-X figure."
	if number == 30:
		notes += (
			" The Back Panel assembly lists Q30's four #89 sockets. The term3 ROM's Single Coil Test prints its power wire BRN where "
			"the chart prints ORG; the two agree on the driver, its address and its fitment, so the record keeps the chart's wire "
			"and notes the difference."
		)
	if number in (27, 28):
		notes += " The Backbox Insert assembly lists the Q27 and Q28 sockets."
	if number == 29:
		notes += " The drawing marks it black (below the playfield) at the centre. The retained Hanibal table leaves it unbound; the pinned Siggi corpus script binds it as its 'Super JP' flasher."
		refs += (VPX_CORPUS_SIGGI_SOURCE,)
	if number == 4:
		physical["part_number"] = "165-5000-44"
		physical["quantity"] = 8
		notes += (
			" The chart's note: 'Q4 Note: Power Line Color is GRY~3A Fuse~RED-YEL and GRY-GRN~3A Fuse~YEL-RED', and the power cell "
			"prints 19v AC on J17-P2/3. The lamp location drawing's backbox inset: 'Center RPG Area X8 Small Lamps are Switched GIs', "
			"and DR. 7 draws 4 (grey) in the centre of the cannon's arc with arrows to eight small lamps. The cell prints the bulb's "
			"part as 090-5000-44 where the lamp part note gives the #44 bulb as 165-5000-44; the record keeps the bulb part. se.c "
			"models it as #44 bulbs on 19 V less a 0.7 V drop ('Backbox GI: 19V AC switched #44 Bulbs')."
		)
	if number == 5:
		notes += (
			" The RPG Cannon Kicker Bracket page: Kicker (on RPG Cannon) Assembly 500-6697-00, 'When energized, the ball is shot into "
			"the targets in the Backbox Insert'. The RPG Backbox Test fires it from the gun trigger or the optional auto-launch button."
		)
	if number == 20:
		notes += (
			" The Backbox Insert's Relay (Picker) & Cable Assembly 500-6700-00 switches the Motor & Drive Wheel assembly's 24V AC 21 "
			"RPM motor (041-5079-01); its eccentric Drive Wheel 535-9277-01 moves the RPG cannon's kicker bracket up and down. The "
			"G.I. page's backbox inset labels the motor feed 'MOTOR via Q20 WHT YEL-BLK'. DR. 7 draws 20 twice, beside the Relay and "
			"beside the Motor, joined by a dotted line. The RPG Backbox Test's RUN cycles the motor through one full cycle."
		)
	if number == 21:
		notes += (
			" The Back Panel assembly's Kicker (Ball Stop) Assembly 500-6219-01: 'When energized, the ball is held in Back Channel "
			"Trough on the Back Panel'. DR. 7 draws 21 grey (not on the playfield) on a coil in the back-panel trough and again on "
			"the playfield's rear edge below it."
		)
	if number in (22, 23):
		notes += (
			" The Ball Deflector Assemblies 500-6657-00 (Qty. 2): 'When energized, it deflects the ball into the Top VUKs or Top "
			f"Lanes'; the chart calls them up posts. DR. 7 draws {'22 between the T-X flashers at the T-X figure' if number == 22 else '23 behind the bumpers'}."
		)
	if number == 2:
		notes += (
			" The Ball Auto Launch Assembly 500-6668-00 (22-1080 coil) works with the gun shooter. The Diagnostic Aids page's "
			"Operator Alert example is '#2 AUTO LAUNCH COIL MALFUNCTION': the CPU activates a coil about ten times while its switch "
			"(16) stays closed."
		)
	if number == 1:
		notes += " The 4-Ball Trough 500-6318-14 carries this 26-1200 coil under the up-kicker."
	if number == 3:
		notes += " The 1-Bank Drop Target Assembly 500-6440-01's reset coil 27-1500 raises the target on switch 25."
	if number == 8:
		notes += " The 1-Bank Drop Target Assembly 500-6440-01's mini trip coil 32-1250 (515-6916-01) knocks the target down under ROM control."
	if number in (9, 10, 11):
		notes += " The bumper assembly page lists the 26-1200 coil (090-5044-00T); DR. 7 draws 9, 10 and 11 at the left, right and bottom bumpers."
	if number == 12:
		notes += " The Laser Kick Back Assembly 500-6697-01: 'When energized, kicks ball back into play from the Left Outlane'; DR. 7 draws 12 (white) at the left outlane kickback."
	if number == 13:
		notes += " The VUK Left Style Assembly 500-6290-00: 'Ball launches into the VUK Chute above the Playfield onto the Wire Ramp'."
	if number == 14:
		notes += (
			" The TX Vertical Up-Kicker 500-6656-00 works with the TX Cannon Trough 500-6655-00 that holds the lockup balls on 33-35; "
			"DR. 7 draws 14 (black) in front of the T-X figure. IPDB: 'T-X ball cannon (shoots ball at right flipper)'."
		)
		refs += (IDENTITY_SOURCE,)
	if number in (15, 16):
		side = "left" if number == 15 else "right"
		power = 47 if number == 15 else 45
		notes += (
			f" Physical Q{number} is removed from public {number}: se.c's se_solenoid_w masks it off and publishes it as the lower-{side} "
			f"flipper power bit {power}, and core.c synthesizes canonical callback {address} from it. Bind this one coil to public "
			f"{address}, the retained table's SolCallback(sL{'L' if number == 15 else 'R'}Flipper); public {power} is its power-phase "
			"state, not a second coil. The 2-Flipper Circuit Wiring Diagram describes the drive: a 40 ms pulse on a button closure, "
			"then 1 ms every 12 ms while held, from one 50v DC supply (RED-YEL from J10 pins 1 and 2) through a 3A slow-blow fuse "
			f"located under the playfield near the flipper to {'GRY-YEL' if number == 15 else 'BLU-YEL'}, which the chart's "
			"power cell prints as one run with the fuse between the colours. Both coils are 22-1080 with a YEL-GRN wrap, on "
			"Flipper Assemblies 500-6682-12 (left) and 500-6682-02 (right)."
		)
		refs += (VPX_SCRIPT_SOURCE, RUNTIME_SOURCE)
	if number in (17, 18):
		notes += " The Slingshot Assembly 500-5849-00 (Qty. 2) carries the 23-800 coil and two stack-blade switches 180-5054-00."
	if number == 24:
		notes += (
			" The row is printed on a light grey band. The cabinet wiring diagram's TO COIN METER box routes Q24 (J7-10, 78 VIO-GRY) "
			"and +5V DC (J16-7, 22 RED) to the meter. No stock playfield device is fitted."
		)
	if number in SOLENOID_SCRIPT:
		notes += f" Retained table script: {SOLENOID_SCRIPT[number]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if number in SOLENOID_RUNTIME:
		notes += f" In the harness runs {SOLENOID_RUNTIME[number]}."
		refs += (RUNTIME_SOURCE,)
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Q{number}"}], "wiring": _q_wiring(number)}
	role = "emitter" if kind in ("flasher", "gi") else "effect"
	if number in CABINET_ROLES:
		extra["roles"] = [CABINET_ROLES[number]]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("solenoid", address, identifier, role)
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("solenoid", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		elif number in (26, 29):
			notes += " The retained table models no bulb Light for it, so it is not placed."
	physical["notes"] = notes
	return _device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, physical=physical, **extra)


# AUX output (public address) -> (AUX number, chart name, label, coil cell, control wire, control connection)
AUX_OUTPUTS = {
	33: (1, "LEFT UP/DOWN POST", "Left Outlane Ball Deflector (UK Only)", "26-1200 / 090-5044-00T", "WHT", "CN2-P5"),
	34: (2, "CENTER UP/DOWN POST", "Center Up/Down Post (UK Only)", "23-1100 / 090-5030-00T", "RED", "CN2-P4"),
	35: (3, "RIGHT UP/DOWN POST", "Right Outlane Ball Deflector (UK Only)", "26-1200 / 090-5044-00T", "ORG", "CN2-P3"),
}


def aux_output_id(address: int) -> str:
	return f"device.aux{AUX_OUTPUTS[address][0]}-{slug(AUX_OUTPUTS[address][2])}"


def _aux_output(address: int) -> dict[str, Any]:
	number, printed, label, part, control_wire, control_connection = AUX_OUTPUTS[address]
	identifier = aux_output_id(address)
	notes = (
		f'Coils Detailed Chart Table (DR. 6), Auxiliary (UK ONLY) group, row "AUX {number}: {printed}": board "Solenoid Expander '
		f'Auxiliary", transistor Q{number} on that board, cell "{part}"; the whole group is printed on a light grey band. se.c '
		"drives the auxiliary board 520-5068-01 from the latch the ESTB strobe loads and publishes its three outputs at 33-35. "
	)
	if address == 34:
		notes += (
			"The UK only assembly page lists the Up/Down Post Assy 500-6293-00 with a 23-1100 (ORG) coil for AUX 2, and the cabinet "
			"wiring diagram's UK note: 'Both buttons pushed together operate the Center Up/Down Post.' DR. 7 draws Aux. 2 (black) "
			"between the flippers."
		)
	else:
		side = "Left" if address == 33 else "Right"
		notes += (
			f"The chart and the ROM call it the {side.upper()} UP/DOWN POST, but the UK only assembly page lists Ball Deflector "
			f"Assemblies 500-5788-02 (26-1200 coil) for AUX 1 and AUX 3, the cabinet wiring diagram's UK note reads 'The {side} "
			f"Button operates the {side} Outlane Ball Deflector', and DR. 7 draws Aux. {number} (black) at the {side.lower()} "
			"outlane. Both names denote this one UK-only output; the record labels it by its assembly."
		)
	notes += (
		" A standard machine fits none of the three, and the retained US table models none. In the gameplay run on term3's default "
		"settings, holding either UK cabinet button fired none of 33-35."
	)
	notes += _placement_note("solenoid", address)
	return _device(identifier, label, "coil", SOLENOID_GROUP, address, "optional",
		(MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"AUX {number}"}],
		physical={"part_number": part.split(" / ")[-1], "location": f"UK only, {'between the flippers' if address == 34 else ('left' if address == 33 else 'right') + ' outlane'}", "notes": notes},
		wiring={"board": "Whitestar Solenoid Expander Auxiliary board 520-5068-01", "driver_transistor": f"Q{number}", "control_wire": control_wire, "control_connection": control_connection, "power_wire": "BRN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"},
		spatial=located("solenoid", address, identifier, "effect"),
	)


def solenoid_outputs() -> list[dict[str, Any]]:
	items = [_q_output(number) for number in Q_OUTPUTS]
	items.extend(_aux_output(address) for address in AUX_OUTPUTS)
	items.append(_device(
		"virtual.15-fast-flip-game-on", "Whitestar Fast-Flip / Game-On State", "virtual", SOLENOID_GROUP, 15, "used",
		(CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "15"}],
		physical={"notes": (
			"se.c sets public 15 while the ROM's fast-flip byte is non-zero, i.e. while the flippers are enabled in a game; "
			"MACHINE_INIT(se) places that byte at CPU RAM 0x04 for every set whose name starts with term3. sega.vbs declares "
			"GameOnSolenoid = 15. In the ball-serve and gameplay runs it rose about 5.4 s after Start, before the trough up-kick in "
			"one run and after the scenario had put a ball on 16 in the other, and in the gameplay run it fell at the drain. "
			"Physical Q15 is the left flipper at public 48; never wire this state to a transistor."
		)},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	items.append(_device(
		"virtual.16-remapped-flipper-hole", "Unused Remapped-Flipper Address 16", "virtual", SOLENOID_GROUP, 16, "unused", (CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "16"}],
		physical={"notes": "se_solenoid_w masks physical Q16 off public 16 and publishes it at 45/46; nothing else drives 16, and no harness run saw it."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	items.append(_device(
		"virtual.36-aux-latch-bit-3", "Unused Auxiliary Latch Bit 36", "virtual", SOLENOID_GROUP, 36, "unused", (CORE_SOURCE, CONTROLLER_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "36"}],
		physical={"notes": (
			"se.c's ESTB handler shifts the whole auxiliary latch into the legacy solenoid word's bits for 33-36, so the latch's "
			"fourth bit would land here, but the board 520-5068-01 has three outputs ('Auxiliary driver board with 3 latched solenoid outputs'), its PWM path "
			"writes 33-35 only, and the coil chart's auxiliary group has three rows. No harness run, the Single Coil Test included, "
			"saw it."
		)},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	for address in range(37, 45):
		items.append(_device(
			f"virtual.{address}-reserved", f"Reserved Address {address}", "virtual", SOLENOID_GROUP, address, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": "A Whitestar compatibility hole: nothing in se.c drives it for this driver."},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	for address, side, canonical, number in ((45, "right", 46, 16), (47, "left", 48, 15)):
		items.append(_device(
			f"virtual.{address}-{side}-flipper-power-phase", f"{side.capitalize()} Flipper Power-Phase State", "virtual", SOLENOID_GROUP, address, "used",
			(CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE), aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": (
				f"se_solenoid_w publishes physical Q{number}'s drive here and core.c synthesizes canonical {canonical} from it; one {side} "
				f"flipper coil is bound at {canonical}. In the gameplay run holding the {side} flipper button raised {address} and "
				f"{canonical} together until it was released, and the Single Coil Test's #{number} raised both. In the ball-serve and "
				"gameplay runs all four of 45-48 rose for a single update as the game-on state 15 rose."
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
	1: ("Left Security Level 1", "LEFT SECURITY LEVEL 1", "#555 Bulb"), 2: ("Left Security Level 2", "LEFT SECURITY LEVEL 2", "#555 Bulb"),
	3: ("Left Security Level 3", "LEFT SECURITY LEVEL 3", "#555 Bulb"), 4: ("Left Security Level 4", "LEFT SECURITY LEVEL 4", "#555 Bulb"),
	5: ("Left Security Level 5", "LEFT SECURITY LEVEL 5", "#555 Bulb"), 6: ("Left 3-Bank Bottom", "LEFT 3-BANK BOT", "#555 Bulb"),
	7: ("Left 3-Bank Middle", "LEFT 3-BANK MID", "#555 Bulb"), 8: ("Left 3-Bank Top", "LEFT 3-BANK TOP", "#555 Bulb"),
	9: ("Right Security Level 1", "RIGHT SECURITY LEVEL 1", "#555 Bulb"), 10: ("Right Security Level 2", "RIGHT SECURITY LEVEL 2", "#555 Bulb"),
	11: ("Right Security Level 3", "RIGHT SECURITY LEVEL 3", "#555 Bulb"), 12: ("Right Security Level 4", "RIGHT SECURITY LEVEL 4", "#555 Bulb"),
	13: ("Right Security Level 5", "RIGHT SECURITY LEVEL 5", "#555 Bulb"), 14: ("Right 3-Bank Bottom", "RIGHT 3-BANK BOT", "#555 Bulb"),
	15: ("Right 3-Bank Middle", "RIGHT 3-BANK MID", "#555 Bulb"), 16: ("Right 3-Bank Top", "RIGHT 3-BANK TOP", "#555 Bulb"),
	17: ("Spot Weapon", "SPOT WEAPON", "#555 Bulb"), 18: ("Security Level", "SECURITY LEVEL", "#555 Bulb"),
	19: ("Hurry Up", "HURRY UP", "#555 Bulb"), 20: ("Video Mode", "VIDEO MODE", "#555 Bulb"), 21: ("Extra Ball", "EXTRA BALL", "#555 Bulb"),
	22: ("Assault", "ASSAULT", "#555 Bulb"), 23: ("Left Ramp Arrow", "LEFT RAMP ARROW", "#555 Bulb"), 24: ("ABC A", "(A) BC", "#555 Bulb"),
	25: ("100,000", "100,000", "#555 Bulb"), 26: ("200,000", "200,000", "#555 Bulb"), 27: ("300,000", "300,000", "#555 Bulb"),
	28: ("500,000", "500,000", "#555 Bulb"), 29: ("750,000", "750,000", "#555 Bulb"), 30: ("1,000,000", "1,000,000", "#555 Bulb"),
	31: ("Right Ramp Arrow", "RIGHT RAMP ARROW", "#555 Bulb"), 32: ("ABC C", "AB (C)", "#555 Bulb"),
	33: ("Left Outlane", "LEFT OUTLANE", "#555 Bulb"), 34: ("Left Return Lane", "LEFT RETURN LANE", "#555 Bulb"),
	35: ("Right Return Lane", "RIGHT RETURN LANE", "#555 Bulb"), 36: ("Right Outlane", "RIGHT OUTLANE", "#555 Bulb"),
	37: ("Kick Back", "KICK BACK", "#555 Bulb"), 38: ("Left Top Lane", "LEFT TOP LANE", "#555 Bulb"),
	39: ("Middle Top Lane", "MIDDLE TOP LANE", "#555 Bulb"), 40: ("Right Top Lane", "RIGHT TOP LANE", "#555 Bulb"),
	41: ("Left RPG", "LEFT RPG", "#555 Bulb"), 42: ("Left Final Battle", "LEFT FINAL BATTLE", "#555 Bulb"),
	43: ("Left Orbit Arrow", "LEFT ORBIT ARROW", "#555 Bulb"), 44: ("Left Hurry Up", "LEFT HURRY UP", "#555 Bulb"),
	45: ("RED R", "(R) ED", "#555 Bulb"), 46: ("RED E", "R (E) D", "#555 Bulb"), 47: ("RED D", "RE (D)", "#555 Bulb"),
	48: ("Advance RED", "ADVANCE RED", "#555 Bulb"), 49: ("Right RPG", "RIGHT RPG", "#555 Bulb"), 50: ("Mystery", "MYSTERY", "#555 Bulb"),
	51: ("Right Orbit Arrow", "RIGHT ORBIT ARROW", "#555 Bulb"), 52: ("Right Hurry Up", "RIGHT HURRY UP", "#555 Bulb"),
	53: ("Start Button Lamp", "START BUTTON", "#555 Bulb"), 54: ("Tournament Button Lamp", "TOURNAMENT BUTTON", "#555 Bulb"),
	55: ("Center Ramp Arrow", "CENTER RAMP ARROW", "#555 Bulb"), 56: ("ABC B", "A (B) C", "#555 Bulb"),
	57: ("Assault Arrow", "ASSAULT ARROW", "#44 Bulb"), 58: ("T-X Arrow", "T-X ARROW", "#555 Bulb"), 59: ("Lock Arrow", "LOCK ARROW", "#555 Bulb"),
	60: ("Jackpot Arrow", "JACKPOT ARROW", "#555 Bulb"), 61: ("Super Jackpot Arrow", "SUPER JACKPOT ARROW", "#555 Bulb"),
	62: ("Special", "SPECIAL", "#555 Bulb"), 64: ("T-X", "T-X", "#44 Bulb"),
	65: ("Backbox Target Lamp Top", "BACK BOX (TOP)", "#555 Bulb"), 66: ("Backbox Target Lamp 2", "BACK BOX 2", "#555 Bulb"),
	67: ("Backbox Target Lamp 3", "BACK BOX 3", "#555 Bulb"), 68: ("Backbox Target Lamp 4", "BACK BOX 4", "#555 Bulb"),
	69: ("Backbox Target Lamp Bottom", "BACK BOX (BOT)", "#555 Bulb"), 71: ("Terminator Eye", "TERMINATOR EYE", "Big Red LED"),
	72: ("Question Mark", "( ? )", "#555 Bulb"), 73: ("Super Jackpot", "SUPER JACKPOT", "#555 Bulb"), 74: ("Assault Insert", "ASSAULT", "#555 Bulb"),
	75: ("Max Escape", "MAX ESCAPE", "#555 Bulb"), 76: ("Payback Time", "PAYBACK TIME", "#555 Bulb"), 77: ("RPG", "RPG", "#555 Bulb"),
	78: ("Final Battle", "FINAL BATTLE", "#555 Bulb"), 79: ("Auto Launch Button Lamp (Optional)", "AUTO LAUNCH (OPT.)", "#555 Bulb"),
	80: ("Shoot Again", "SHOOT AGAIN", "#555 Bulb"),
}
UNRESOLVED_LAMPS = (63,)
UNUSED_LAMPS = (70,)
LAMP_DRIVE = [("YEL-BRN", "J13-P9", "U17"), ("YEL-RED", "J13-P8", "U16"), ("YEL-ORG", "J13-P7", "U15"), ("YEL-BLK", "J13-P6", "U14"), ("YEL-GRN", "J13-P5", "U13"), ("YEL-BLU", "J13-P4", "U12"), ("YEL-VIO", "J13-P3", "U11"), ("YEL-GRY", "J13-P1", "U10")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
BULB_PARTS = {"#555 Bulb": "165-5002-00", "#44 Bulb": "165-5000-44"}
CABINET_LAMPS = {
	53: ("cabinet.start-button-lamp", "used", "cabinet left front (start button lamp)"),
	54: ("cabinet.tournament-button-lamp", "optional", "cabinet front centre (tournament button lamp, optional tournament kit)"),
	65: ("cabinet.backbox", "used", "backbox insert, beside the RPG targets"), 66: ("cabinet.backbox", "used", "backbox insert, beside the RPG targets"),
	67: ("cabinet.backbox", "used", "backbox insert, beside the RPG targets"), 68: ("cabinet.backbox", "used", "backbox insert, beside the RPG targets"),
	69: ("cabinet.backbox", "used", "backbox insert, beside the RPG targets"),
	79: ("cabinet.launch-button-lamp", "optional", "cabinet (optional Ball Launch Button lamp)"),
}


def lamp_id(address: int) -> str:
	if address in LAMPS:
		return f"lamp.{address}-{slug(LAMPS[address][0])}"
	if address in UNRESOLVED_LAMPS:
		return f"lamp.{address}-unresolved"
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
	driven_outside_test = set(load_runtime()["runtime"]["observations"]["lamp_addresses_driven_outside_self_test"])
	if driven_outside_test & set(UNUSED_LAMPS) or not set(UNRESOLVED_LAMPS) <= driven_outside_test:
		raise RuntimeError("Terminator 3 runtime evidence no longer matches the unused and unresolved lamp decisions")
	for address in range(1, 81):
		row, column = divmod(address - 1, 8)
		identifier = lamp_id(address)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		notes = f"Printed lamp-matrix row {row + 1}, column {column + 1}."
		if address in UNRESOLVED_LAMPS:
			notes += (
				" The Lamp Matrix Grid (DR. 5) prints this cell NOT USED in a black name cell with a grey bulb line, the lamp location "
				"drawing marks no lamp with this number, and the term3 ROM's own Single Lamp Test names it NOT USED. Yet the ROM drives "
				"it: in every harness run but the lamp test it switched at exactly the same instants as the T-X lamp 64, from about 9.3 s "
				"after power-up through attract mode and play. No retained script binds it. Nothing available here explains what "
				"that state reaches: a second socket wired with 64, a socket an earlier build fitted, or none. Availability stays "
				"unknown. Resolution path: an under-playfield look or a continuity check at row 8, column 7 (RED-GRY J12-P9 / YEL-VIO "
				"J13-P3) on a production machine, or another revision of the manual's lamp grid, would show whether a bulb is fitted here."
			)
			items.append(_device(identifier, f"Unresolved Lamp {address}", "lamp", LAMP_GROUP, address, "unknown",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE), status="candidate",
				aliases=aliases, physical={"notes": notes}, wiring=_lamp_wiring(address)))
			continue
		if address in UNUSED_LAMPS:
			notes += (
				" The Lamp Matrix Grid (DR. 5) prints this cell NOT USED in a black name cell with a grey bulb line, the lamp location "
				"drawing marks no lamp with this number, the term3 ROM's Single Lamp Test names it NOT USED, no other harness run saw "
				"the ROM drive it, and the retained script assigns no Light to it."
			)
			items.append(_device(identifier, f"Not Used Lamp {address}", "lamp", LAMP_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE),
				aliases=aliases, physical={"notes": notes}, wiring=_lamp_wiring(address), spatial=not_applicable("unused", MANUAL_SOURCE)))
			continue
		label, printed, bulb = LAMPS[address]
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE)
		role, availability, location = CABINET_LAMPS.get(address, (None, "used", label))
		physical: dict[str, Any] = {"location": location}
		if bulb in BULB_PARTS:
			physical["part_number"] = BULB_PARTS[bulb]
		notes += f' The grid prints "{printed}" with the bulb cell "{bulb}".'
		if address == 53:
			notes += (
				" The cabinet wiring diagram's START / TOURNIE BUTTON LAMPS draw 'Lamp 53 Start' and 'Lamp 54 Tournie', each with a "
				"diode, on RED-VIO to J12 pin 7, YEL-GRN to J13 pin 5 and YEL-BLU to J13 pin 6; the grid's row 7 and columns 5 and 6 "
				"are RED-VIO J12-P8, YEL-GRN J13-P5 and YEL-BLU J13-P4. The two pages agree on the lamps and their wire colours and "
				"differ on two pin numbers (J12 pin 7 against P8, and J13 pin 6 against P4 for YEL-BLU); the record keeps the grid's. "
				"The location drawing marks 53 grey at the cabinet's left front, where switch 54 START BUTTON sits."
			)
		if address == 54:
			notes += (
				" The cabinet wiring diagram draws 'Lamp 54 Tournie' with 'Lamp 53 Start' on YEL-BLU to J13 pin 6 where the grid's "
				"column 6 is YEL-BLU J13-P4 (see lamp 53). The location drawing marks 54 grey at the front centre beside the note "
				"'Optional Tournament Kit Required'. No harness run saw the ROM light it outside the lamp test."
			)
		if address == 79:
			notes += (
				" The location drawing does not draw it. The Gun Shooter Connector Assembly page offers the Ball Launch Button "
				"500-6709-06-79 with a #555 bulb in place of the gun, and the RPG Backbox Test names the optional Auto Launch Button. "
				"In the ball-serve and gameplay runs the ROM blinked it from just after the game-on state 15 rose until about the "
				"moment it fired the drop-target trip coil 8 and the T-X flashers 26 after the gun-trigger launch."
			)
		if address in (65, 66, 67, 68, 69):
			notes += (
				" The location drawing's backbox-insert inset stacks 65-69 (grey, not on the playfield) along the edge of the cannon's "
				"arc beside the targets 41-45, and the RPG Backbox Test lights the Insert Lamps 65-69."
			)
		if address == 64:
			notes += " The TX Head, Arm and Cannon assembly page lists a #44 bulb in the T-X head; the location drawing puts 64 at the T-X figure."
		if address == 71:
			notes += (
				" The T-850 Head with LED Assembly 500-6701-00; the location drawing puts 71 beside the top lanes. IPDB lists the "
				"Terminator and T-X heads on the playfield among the toys."
			)
			refs += (IDENTITY_SOURCE,)
		if address == 57:
			notes += " The only #44 insert on the grid besides the T-X lamp 64."
		if address in (73, 74, 75, 76, 77, 78):
			notes += (
				" The location drawing marks it black (below the playfield) "
				+ ("between the flippers" if address in (73, 74, 75, 78) else "in the arc in front of the security levels" if address == 76 else "in the value arc")
				+ ". The retained table's script copies no lamp in 73-79 onto a Light, so it is not placed."
			)
		if address in CABINET_LAMPS:
			extra: dict[str, Any] = {"aliases": aliases, "wiring": _lamp_wiring(address), "roles": [role], "spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE)}
		else:
			extra = {"aliases": aliases, "wiring": _lamp_wiring(address)}
			spatial = located("lamp", address, identifier, "emitter")
			unplaced = _unplaced_lamp_note(address)
			if (spatial or unplaced) and address in range(73, 80) or not (spatial or unplaced) and address not in range(73, 80):
				raise RuntimeError(f"Terminator 3 lamp {address}: the spatial seed no longer matches the script's lamp bindings")
			if spatial or unplaced:
				notes += (
					" Retained table script: UseLamps = 1 (line 23) and line 1239 bind Lights(n) to the table Light L<n>, and the "
					"Flasherupdate timer copies each insert onto its bulb-mode Light (lines 1346-1453)."
				)
				refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			if spatial:
				extra["spatial"] = spatial
				notes += _placement_note("lamp", address)
			notes += unplaced
		if address in driven_outside_test:
			notes += " The harness runs saw the ROM drive it outside the Single Lamp Test."
		physical["notes"] = notes
		items.append(_device(identifier, label, "lamp", LAMP_GROUP, address, availability, refs, physical=physical, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	seed = _spatial_seed()
	entries = seed["gi"]["0"]
	excluded = seed["gi_excluded"]["0"]
	placements = [{
		"id": f"gi.relay.emitter.{index}", "role": "emitter", "space": "playfield", "x": entry["x"], "y": entry["y"],
		"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
	} for index, entry in enumerate(entries, start=1)]
	rear = sum(1 for entry in entries if entry["y"] < 0.07)
	notes = (
		"One G.I. relay on the I/O Power Driver Board 520-5137-01 (U206 74HCT273 data latch output D0 through R254 1K and the Q200 "
		"2N3904 relay driver, coil on 20v DC with D229 1N4004 across it) switches the 5.7v AC G.I. supply from J14 to four separately "
		"fused circuits on J15 (General Illumination Circuit Detailed Wiring Diagram, PDF page 121): B, F24, BRN-WHT to WHT-BRN, "
		"'Back Panel X10, Insert X6, and above Playfield X2', 16 #44 and 2 #555; Y, F25, YEL to WHT-YEL, 'Left & Lower Playfield "
		"X18', 18 #44; G, F26, GRN to WHT-GRN, 'Backbox Insert X17 + US Coin Door X2 (Euro X1)', 17 #44 and 2 #555 on the coin door; "
		"V, F27, VIO to WHT-VIO, 'Right Playfield X20', 20 #44 including 'GIs in Pop Bumpers (X3)'. The page warns that G.I. bulb "
		"quantities may change during production, and its text layer also carries 'Note: GI above P/F is #555 Bulb.', which the "
		"rendered page does not show. The bumper assembly page (PDF page 101) names the bumper bulb more specifically: item 1, "
		"'#555 Wedge Base Bulb' 165-5002-00, one per bumper, labelled 'Gen. Illum. (GI) X3'. So the three pop-bumper G.I. "
		"bulbs that the wiring page counts among circuit V's #44 bulbs are #555 on the assembly page; both readings are kept, "
		"and the circuit counts below follow the wiring page. The quantity 75 is the four circuits' printed bulbs: 40 at the playfield (the "
		"two above-playfield reflector bulbs pointing at the T-X and T-850 figures among them), ten on the back panel's light "
		"board, 23 in the backbox insert and two on the coin door. se.c publishes the relay as GI 0; in the harness runs the ROM "
		"switched it on during boot, blinked it after Start, with the right 3-bank 22, the captive ball 23 and T-X made 31 and "
		"while a ball sat at lockup 1 (33), and switched it off at the drain. Retained table script: UseGI = 0 (line 24), but line 1250 sets GICallback to "
		"GIUpdate, which switches every member of the GIGruppe collection with G.I. 0 (lines 1252-1255). Its "
		f"{len(entries) + len(excluded)} render-double clusters of GIGruppe Lights give {len(entries)} sockets that draw a bulb "
		f"mesh, each placed, observed only, on its bulb Light; the {len(excluded)} clusters that draw no bulb are render helpers "
		f"and are not placed. {rear} of the placed sockets lie within 0.07 of the rear edge, where the back panel's ten-bulb light "
		"board stands; the circuit letters have not been matched to the sockets, so no placement carries a string, and the "
		"placements are not a one-to-one census of the 40 playfield bulbs."
	)
	return [_device(
		"gi.relay", "General Illumination Relay", "gi", GI_GROUP, 0, "used", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.gi", "value": "0"}],
		physical={"location": "playfield, back panel, backbox insert and coin door", "quantity": 75, "notes": notes},
		wiring={"board": "Whitestar I/O Power Driver board 520-5137-01 G.I. relay", "power_wire": "YEL / YEL-WHT", "power_connection": "J14-P1-3 / J14-P4-6", "nominal_voltage_v": 5.7, "voltage_type": "ac"},
		spatial={"status": "observed", "placements": placements},
	)]


def displays() -> list[dict[str, Any]]:
	return [{
		"id": "display.dmd", "label": "Dot Matrix Display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32,
		"physical_location": "cabinet_or_service",
		"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		"spatial": not_applicable("cabinet_or_service", CORE_SOURCE),
	}]


# --- The term3 ROM's service tests -------------------------------------------------------------------
# Where the ROM's wording differs from the manual's beyond spacing and case: address -> (the manual's exact text, the
# ROM's exact text). Both sides are pinned, so a changed manual transcription cannot ride on an allowed difference.
SWITCH_WORDING = {1: ("LEFT BUTTON (UK ONLY)", "LT BUTTON (UK ONLY)"), 8: ("RIGHT BUTTON (UK ONLY)", "RT BUTTON (UK ONLY)")}
LAMP_WORDING = {
	6: ("LEFT 3-BANK BOT", "LT 3-BANK BOT"), 7: ("LEFT 3-BANK MID", "LT 3-BANK MID"), 8: ("LEFT 3-BANK TOP", "LT 3-BANK TOP"),
	14: ("RIGHT 3-BANK BOT", "RT 3-BANK BOT"), 15: ("RIGHT 3-BANK MID", "RT 3-BANK MID"), 16: ("RIGHT 3-BANK TOP", "RT 3-BANK TOP"),
}
COIL_WORDING: dict[int, tuple[str, str]] = {}
# Driver -> (the chart's power wire, the power wire the ROM prints) where they differ.
COIL_POWER_DIFFERENCE = {30: ("ORG", "BRN")}
# The chart prints no power wire for its four NOT USED rows; the ROM prints the bank's supply wire for each.
UNUSED_COIL_POWER = {6: "YEL-VIO", 7: "YEL-VIO", 19: "BRN", 25: "ORG"}
COIL_PUBLIC = {15: [47, 48], 16: [45, 46]}
SWITCH_TEST_RUN = "term3-switch-test"
DEDICATED_TEST_RUN = "term3-dedicated-switch-test"
LAMP_TEST_RUN = "term3-single-lamp-test"
COIL_TEST_RUN = "term3-single-coil-test"
DEDICATED_TEST = {
	84: "left flipper button (public 84) held in the Dedicated Switch Test",
	83: "left flipper end-of-stroke input (public 83) held in the Dedicated Switch Test",
	88: "dedicated input 88 (DS-5) (public 88) held in the Dedicated Switch Test",
	82: "right flipper button (public 82) held in the Dedicated Switch Test",
	81: "right flipper end-of-stroke input (public 81) held in the Dedicated Switch Test",
}


def _normalized(text: str) -> str:
	return re.sub(r"\s+", "", text).casefold()


def load_runtime() -> dict[str, Any]:
	return load_json(ROOT / RUNTIME_PATH)


def _snapshots(evidence: dict[str, Any]) -> dict[str, str]:
	return {item["label"]: item["interpreted_text"] for item in evidence["runtime"]["observations"]["diagnostic_snapshots"]}


def _reading(snapshots: dict[str, str], run: str, label: str, title: str, parts: int) -> list[str]:
	text = snapshots.get(f"{run} snapshot: {label}")
	if text is None:
		raise RuntimeError(f"Terminator 3 runtime evidence lacks the frame '{run}: {label}'")
	fields = text.split(" / ")
	if len(fields) != parts or fields[0] != title:
		raise RuntimeError(f"Terminator 3 frame '{run}: {label}' does not read as a {title} frame: {text!r}")
	return fields[1:]


def _check_name(kind: str, address: int, printed: str, rom: str, wording: dict[int, tuple[str, str]]) -> None:
	if address in wording:
		manual, expected = wording[address]
		if printed != manual or rom != expected or _normalized(rom) == _normalized(printed):
			raise RuntimeError(f"Terminator 3 {kind} {address}: the ROM prints {rom!r} where the manual prints {printed!r}; the wording table expects {expected!r} against {manual!r}")
	elif _normalized(rom) != _normalized(printed):
		raise RuntimeError(f"Terminator 3 {kind} {address}: the ROM prints {rom!r} where the manual prints {printed!r}")


def switch_test_readings(evidence: dict[str, Any]) -> dict[int, tuple[str, str]]:
	"""Matrix switch -> (name, wire text) the term3 Portals Switch Test printed while the scenario held it closed, refused
	unless the name matches the Switch Matrix Grid and the wires and number match the matrix drive and return. Switch 3,
	which the ROM does not read, must print NONE."""
	snapshots = _snapshots(evidence)
	readings: dict[int, tuple[str, str]] = {}
	for address in range(1, 65):
		label = f"switch {address} closed in the Switch Test"
		if address == 3:
			if _reading(snapshots, SWITCH_TEST_RUN, label, "SWITCH TEST", 3) != ["NONE", "DOOR BUTTONS OPERATE MENU"]:
				raise RuntimeError("Terminator 3 switch 3: the Switch Test no longer prints NONE")
			readings[address] = ("NONE", "")
			continue
		name, wires, footer = _reading(snapshots, SWITCH_TEST_RUN, label, "SWITCH TEST", 4)
		column, row = divmod(address - 1, 8)
		if footer != "DOOR BUTTONS OPERATE MENU" or wires != f"{MATRIX_DRIVE[column][0]} {MATRIX_RETURN[row][0]} #{address:02d}":
			raise RuntimeError(f"Terminator 3 switch {address}: the Switch Test prints {wires!r} / {footer!r}")
		if address not in SWITCHES and address not in UNUSED_SWITCHES:
			raise RuntimeError(f"Terminator 3 switch {address} is in neither switch table")
		printed = SWITCHES[address][1] if address in SWITCHES else "NOT USED"
		_check_name("switch", address, printed, name, SWITCH_WORDING)
		readings[address] = (name, wires)
	return readings


def dedicated_test_readings(evidence: dict[str, Any]) -> dict[int, tuple[str, str]]:
	"""Dedicated input -> (name, wire text) the term3 Dedicated Switch Test printed while the scenario held it, refused unless
	the flipper buttons and DS-5 print the grid's names and wires and the two end-of-stroke inputs, which core.c rewrites,
	leave the test at NONE."""
	snapshots = _snapshots(evidence)
	expected = {84: "#1 LEFT FLIPPER BUTTON", 82: "#3 RIGHT FLIPPER BUTTON", 88: "#5 NOT USED"}
	wires = {84: ("GRY-BRN", "CN6-P2"), 82: ("GRY-ORG", "CN6-P4"), 88: ("GRY-GRN", "CN6-P7")}
	readings: dict[int, tuple[str, str]] = {}
	for address, label in DEDICATED_TEST.items():
		if address in (81, 83):
			if _reading(snapshots, DEDICATED_TEST_RUN, label, "DEDICATED SWITCH TEST", 3) != ["NONE", "PRESS START TO EXIT TEST"]:
				raise RuntimeError(f"Terminator 3 dedicated input {address}: the Dedicated Switch Test no longer prints NONE")
			readings[address] = ("NONE", "")
			continue
		name, wire_text, footer = _reading(snapshots, DEDICATED_TEST_RUN, label, "DEDICATED SWITCH TEST", 4)
		wire, connector = wires[address]
		if address != 88 and (wire, connector) != DEDICATED[address][2:4]:
			raise RuntimeError(f"Terminator 3 dedicated input {address}: the grid's wire changed")
		if name != expected[address] or wire_text != f"CN6-{connector.removeprefix('CN6-P')} {wire} CN6-1 BLK" or footer != "PRESS START TO EXIT TEST":
			raise RuntimeError(f"Terminator 3 dedicated input {address}: the Dedicated Switch Test prints {name!r} / {wire_text!r}")
		readings[address] = (name, wire_text)
	return readings


def lamp_test_readings(evidence: dict[str, Any]) -> dict[int, tuple[str, str]]:
	"""Lamp -> (name, wire text) the term3 Single Lamp Test printed at that step, refused unless the name matches the Lamp
	Matrix Grid (NOT USED for the unused and unresolved cells), the wires match the lamp matrix, and the step changed this
	lamp and at most the one the previous step lit."""
	snapshots = _snapshots(evidence)
	changed: dict[int, set[int]] = {}
	for observation in evidence["runtime"]["observations"]["named_action_observations"]:
		match = re.fullmatch(rf"{LAMP_TEST_RUN} step \d+: Black ENTER button \(public 0\) pressed on \+: lamp step (\d+); lamps changed during the step: (.+)", observation["label"])
		if match:
			changed[int(match.group(1))] = set() if match.group(2) == "none" else {int(item) for item in match.group(2).split(", ")}
	readings: dict[int, tuple[str, str]] = {}
	for address in range(1, 81):
		name, wires = _reading(snapshots, LAMP_TEST_RUN, f"Black ENTER button (public 0) pressed on +: lamp step {address}", "SINGLE LAMP TEST", 3)
		row, column = divmod(address - 1, 8)
		if wires != f"{LAMP_DRIVE[column][0]} {LAMP_RETURN[row][0]} #{address:02d}":
			raise RuntimeError(f"Terminator 3 lamp {address}: the Single Lamp Test prints {wires!r}")
		if address not in changed.get(address, set()) or changed[address] - {address - 1, address}:
			raise RuntimeError(f"Terminator 3 lamp {address}: its Single Lamp Test step changed lamps {sorted(changed.get(address, ()))}")
		printed = LAMPS[address][1] if address in LAMPS else "NOT USED"
		_check_name("lamp", address, printed, name, LAMP_WORDING)
		readings[address] = (name, wires)
	if _reading(snapshots, LAMP_TEST_RUN, "Black ENTER button (public 0) pressed on +: lamp step 81", "SINGLE LAMP TEST", 2) != ["NONE"]:
		raise RuntimeError("Terminator 3 Single Lamp Test: the step after lamp 80 no longer shows NONE")
	return readings


def coil_test_readings(evidence: dict[str, Any]) -> dict[int, tuple[str, str]]:
	"""Public output -> (name, wire text) the term3 Single Coil Test printed when it was selected (Q1-Q32, then AUX 1-3),
	refused unless the name matches the coil chart, the wires match its power and control wires (the unused rows print no
	power on the chart), and firing it there pulsed exactly its public address (both published flipper states for Q15 and
	Q16). The step after AUX 3 must wrap to #1."""
	snapshots = _snapshots(evidence)
	fired = {}
	for observation in evidence["runtime"]["observations"]["named_action_observations"]:
		match = re.fullmatch(rf"{COIL_TEST_RUN} step \d+: Black ENTER button \(public 0\) pressed on RUN: coil step (\d+) fired(?:;.*)?", observation["label"])
		if match:
			fired[int(match.group(1))] = observation["transitioned_solenoid_addresses"]
	readings: dict[int, tuple[str, str]] = {}
	for step in range(1, 36):
		name, wires = _reading(snapshots, COIL_TEST_RUN, f"Black ENTER button (public 0) pressed on +: coil step {step} selected", "SINGLE COIL TEST", 3)
		power, _, control = wires.partition(" ")
		if step <= 32:
			label, printed, kind, availability, part, power_wire, _connection, _voltage, _type, control_wire, _control_connection = Q_OUTPUTS[step]
			prefix = f"#{step} "
			chart_power = re.split(r" / |~3A Fuse~", power_wire or "")
			if step in COIL_POWER_DIFFERENCE:
				chart, rom = COIL_POWER_DIFFERENCE[step]
				power_ok = power == rom and chart_power == [chart]
			elif availability == "unused":
				power_ok = power_wire is None and power == UNUSED_COIL_POWER[step]
			else:
				power_ok = power in chart_power
			if not name.startswith(prefix) or not power_ok or control != control_wire:
				raise RuntimeError(f"Terminator 3 coil {step}: the Single Coil Test prints {name!r} / {wires!r}")
			_check_name("coil", step, printed, name.removeprefix(prefix), COIL_WORDING)
			public = COIL_PUBLIC.get(step, [step])
			key = public[-1]
		else:
			number, printed, _label, _part, control_wire, _control_connection = AUX_OUTPUTS[step]
			prefix = f"AUX {number}: "
			if not name.startswith(prefix) or power != "BRN" or control != control_wire:
				raise RuntimeError(f"Terminator 3 AUX {number}: the Single Coil Test prints {name!r} / {wires!r}")
			_check_name("coil", step, printed, name.removeprefix(prefix), COIL_WORDING)
			public = [step]
			key = step
		if fired.get(step) != public:
			raise RuntimeError(f"Terminator 3 coil step {step}: firing it in the Single Coil Test pulsed {fired.get(step)}")
		readings[key] = (name, wires)
	wrapped = _reading(snapshots, COIL_TEST_RUN, "Black ENTER button (public 0) pressed on +: coil step 36 selected", "SINGLE COIL TEST", 3)
	if wrapped != ["#1 TROUGH UP-KICKER", "YEL-VIO BRN-BLK"]:
		raise RuntimeError(f"Terminator 3 Single Coil Test: the step after AUX 3 reads {wrapped!r}")
	return readings


def append_service_test_readings(definition: dict[str, Any], evidence: dict[str, Any]) -> None:
	switches, dedicated, lamps, coils = switch_test_readings(evidence), dedicated_test_readings(evidence), lamp_test_readings(evidence), coil_test_readings(evidence)
	sentences: dict[tuple[str, int], str] = {}
	for address, (name, wires) in switches.items():
		if address == 3:
			sentences[(SWITCH_GROUP, 3)] = " The term3 ROM's Portals Switch Test prints \"NONE\" while it is closed."
		else:
			sentences[(SWITCH_GROUP, address)] = f' The term3 ROM\'s Portals Switch Test prints "{name} / {wires}" while it is closed.'
	for address, (name, wires) in dedicated.items():
		if address in (81, 83):
			sentences[(SWITCH_GROUP, address)] = " The term3 ROM's Dedicated Switch Test prints \"NONE\" while the host holds it."
		else:
			sentences[(SWITCH_GROUP, address)] = f' The term3 ROM\'s Dedicated Switch Test prints "{name} / {wires}" while it is held.'
	for address, (name, wires) in lamps.items():
		sentences[(LAMP_GROUP, address)] = f' The term3 ROM\'s Single Lamp Test prints "{name} / {wires}" and lights it at that step.'
	for key, (name, wires) in coils.items():
		if key in AUX_OUTPUTS:
			sentences[(SOLENOID_GROUP, key)] = f' The term3 ROM\'s Single Coil Test prints "{name} / {wires}", and firing it there pulsed public {key}.'
			continue
		number = {48: 15, 46: 16}.get(key, key)
		public = COIL_PUBLIC.get(number, [number])
		effect = f"raised public {public[0]} and {public[1]}" if len(public) == 2 else f"pulsed public {number}"
		sentences[(SOLENOID_GROUP, key)] = f' The term3 ROM\'s Single Coil Test prints "{name} / {wires}" for Q{number}, and firing it there {effect}.'
	for device in definition["inputs"] + definition["outputs"]:
		sentence = sentences.pop((device["binding"]["group"], device["binding"]["device"]), None)
		if sentence is None:
			continue
		device["physical"]["notes"] += sentence
		refs = device["provenance"]["source_refs"]
		if RUNTIME_SOURCE not in refs:
			refs.append(RUNTIME_SOURCE)
	if sentences:
		raise RuntimeError(f"Terminator 3 service-test readings name no device: {sorted(sentences)}")


# --- Mechanisms ----------------------------------------------------------------------------------------
def _mechanism(suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...], assembly: str | None = None) -> dict[str, Any]:
	result: dict[str, Any] = {"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior}
	if assembly:
		result["assembly_part_number"] = assembly
	result["provenance"] = provenance("validated", *refs)
	return result


def mechanisms() -> list[dict[str, Any]]:
	common = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	run = common + (RUNTIME_SOURCE,)
	s = switch_id
	q = q_output_id
	return [
		_mechanism("trough", "4-ball trough with up-kicker and stacking opto", "kicker", [q(1)], [s(11), s(12), s(13), s(14), s(15)],
			"Four balls (the front page requires four pinballs) rest in the 4-Ball Trough 500-6318-14 on micro switches 11 (left), "
			"12 and 13 and at the up-kicker on the VUK opto 14; the trough's Dual OPTO boards carry 14 and the stacking opto 15. Q1 "
			"(26-1200) kicks the ball on 14 up into the shooter lane and the rest roll one place toward the up-kicker. Hold each "
			"occupied position at 1 and pass the kicked ball through 15 as a short 1 pulse (beam blocked). In the ball-serve run "
			"the ROM fired Q1 0.7 s after the game-on state rose; in the gameplay run, where the scenario put a ball on 16 before "
			"the ROM served one, it never fired Q1. In the stacking-opto run, with four balls on 11-14 in attract mode, raising 15 to "
			"1 made the ROM fire Q1 six times about 0.8 s apart and then the auto launch Q2 once, 9.1 s after the rise; lowering it "
			"fired nothing and raising it again repeated the pattern. The "
			"retained table's bsTrough never writes 15.", run, assembly="500-6318-14"),
		_mechanism("auto-launch", "Shooter lane, gun trigger and auto launch", "kicker", [q(2)], [s(16), s(55)],
			"A served ball comes to rest on the shooter-lane rollover 16 in front of the Ball Auto Launch Assembly 500-6668-00, whose "
			"Q2 (22-1080) fires it up the lane onto the shooter-lane steel ramp. The player fires it with the gun on the cabinet front "
			"(Gun Shooter Connector Assembly 500-5698-02-79, trigger micro switch 55); an operator may fit the Ball Launch Button "
			"500-6709-06-79 with its lamp 79 instead. In the ball-serve run Q1 served the ball, the scenario emptied the trough opto "
			"14 and let the next ball block it, and the ROM held the served ball on 16 for 10 s and fired Q2 81 ms after the trigger "
			"was pulled, then 1.67 s and 3.34 s after that. In the gameplay run the scenario closed 16 before the ROM had served a "
			"ball and left 14 blocked; the ROM never fired Q1 and fired Q2 0.76 s later without a trigger pull, then every 1.6-1.7 s "
			"while the ball stayed on 16 and once 43 ms after the trigger was pulled, seven times in all, the last 0.18 s after the "
			"ball left. The record does not claim which condition makes the ROM launch on its own. The Diagnostic "
			"Aids page: the CPU activates the auto launch about ten times while 16 stays closed before it reports an Operator Alert. "
			"In both runs the ROM blinked lamp 79 from just after the game-on state rose until about 1.4-1.6 s after the trigger was "
			"pulled. The retained table fires a cvpmImpulseP from the trigger "
			"swplunger.", run + (IDENTITY_SOURCE,), assembly="500-6668-00"),
		_mechanism("kickback", "Left outlane kickback", "kicker", [q(12)], [s(57)],
			"Laser Kick Back Assembly 500-6697-01: 'When energized, kicks ball back into play from the Left Outlane', with a 23-800 "
			"coil. In the gameplay run closing the left outlane 57 once fired Q12. The ROM, not a wire, decides whether it is armed; "
			"lamp 37 is printed KICK BACK. The retained table fires a plunger object and pulls it back on release.", run, assembly="500-6697-01"),
		_mechanism("vuk", "VUK", "kicker", [q(13)], [s(36)],
			"VUK Left Style Assembly 500-6290-00: a ball resting on the heavy-duty micro switch 36 is kicked by Q13 (26-1200); 'Ball "
			"launches into the VUK Chute above the Playfield onto the Wire Ramp'. In the Switch Test run closing 36 fired Q13, and "
			"in the gameplay run a ball resting on it drew Q13 with the drop-target coils 3 and 8 and flasher 30. The retained table "
			"catches the ball in tophole and kicks it out of vukout.", run, assembly="500-6290-00"),
		_mechanism("tx-cannon", "T-X cannon lockup and up-kicker", "kicker", [q(14)], [s(31), s(33), s(34), s(35)],
			"The TX Cannon Trough 500-6655-00 at the T-X figure holds up to three balls: lockup 1 (right) on the single opto 33, "
			"lockup 2 and lockup 3 (left) on micro switches 34 and 35; the location drawing puts the above-playfield switch 31 "
			"(T-X MADE) beside them, and both retained scripts pulse 31 as the ball enters the lockup. The trough 'works with' the TX Vertical Up-Kicker "
			"500-6656-00, whose Q14 (26-1200) kicks the ball up into the T-X cannon's wire ramp; IPDB: 'T-X ball cannon (shoots ball "
			"at right flipper)'. In the Switch Test run closing 33, 34 or 35 fired Q14. In the gameplay run a ball resting on 33 drew "
			"Q14 with the backbox switched G.I. 4 and flashers 26 and 30 and blinked the G.I. The retained table stacks the balls in "
			"bstxhole and kicks them out of tvukout.", run + (IDENTITY_SOURCE, VPX_CORPUS_SIGGI_SOURCE), assembly="500-6655-00"),
		_mechanism("drop-target", "1-bank drop target", "drop_target_bank", [q(3), q(8)], [s(25)],
			"1-Bank Drop Target 500-6440-01: one target on the micro switch 25 (180-5158-00), raised by the reset coil Q3 (27-1500) "
			"and knocked down by the mini trip coil Q8 (32-1250, 515-6916-01); the page includes a target-height adjustment. The ROM "
			"drives both coils as game logic: it fired Q3 at power-up, on Start, after the drain and with several scoring switches, "
			"and Q8 three times from about 1.6 s after the gun trigger launched the ball, when backbox target 43 closed and when the target went down and came "
			"back up. The retained table's cvpmDropTarget holds 25 at 1 while the target is down.", run, assembly="500-6440-01"),
		_mechanism("up-posts", "Left and center up posts (ball deflectors)", "diverter", [q(22), q(23)], [],
			"Ball Deflector Assemblies 500-6657-00 (Qty. 2), each with a 26-1200 coil: 'When energized, it deflects the ball into the "
			"Top VUKs or Top Lanes'. The coil chart calls them the LEFT UP POST (Q22) and CENTER UP POST (Q23); DR. 7 draws 22 at "
			"the T-X figure and 23 behind the bumpers. Neither has a switch of its own. In the gameplay run each orbit switch (24, "
			"28, 29, 46) made the ROM hold both on for about 2.1 s, the second starting 0.2-0.5 s after the first. The retained table raises the walls LeftPost and CenterPost while each is energized.",
			run, assembly="500-6657-00"),
		_mechanism("back-panel-ball-stop", "Back-panel ball stop and skill shot", "gate", [q(21)], [s(52)],
			"The back panel carries a wire ramp (535-9241-00) into a back-channel trough and the Kicker (Ball Stop) Assembly "
			"500-6219-01 (26-1200, Q21, which the coil chart names BACK PANEL DIVERTER): 'When energized, the ball is held in Back "
			"Channel Trough on the Back Panel'. The skill-shot switch 52 sits behind the back panel under that trough. In the "
			"gameplay run closing 52 once fired Q21. The retained table models the stop as two walls on the playfield's rear edge "
			"that Q21 swaps.", run, assembly="500-6219-01"),
		_mechanism("rpg-cannon", "RPG backbox cannon and targets", "motorized", [q(20), q(5)], [s(41), s(42), s(43), s(44), s(45)],
			"IPDB: 'Backbox reciprocating cannon shoots Delrin Ball horizontally at 5 targets'. In the backbox insert, Q20 drives "
			"the Relay (Picker) & Cable Assembly 500-6700-00, which runs a 24V AC 21 RPM motor (041-5079-01); its eccentric Drive "
			"Wheel 535-9277-01 moves the RPG cannon's kicker bracket up and down, so the cannon sweeps its arc. The RPG Cannon "
			"Kicker Assembly 500-6697-00 (23-800, Q5) shoots the cannon's own ball into the five Stand-Up Targets 41 (top) to 45 "
			"(bottom). The grid lists no switch for the cannon's position. The front page: 'Remove Shipping Post Ref. A from the "
			"Backbox Insert under the RPG Cannon before Powering Up'. The RPG Backbox Test runs the motor through one full cycle, "
			"fires the kicker from the gun trigger (or the optional auto-launch button) and lights the insert lamps 65-69; the "
			"switched G.I. Q4 lights eight lamps in the centre of the arc and Q27/Q28 flash four lamps on each side. In the "
			"gameplay run closing each target once drew neither Q5 nor Q20; only the Single Coil Test fired them. The retained table "
			"fires its backbox kicker only while its own ball is in the backbox and runs a timer from Q20.",
			run + (IDENTITY_SOURCE,), assembly="500-6700-00"),
		_mechanism("bumpers", "Three bumpers", "other", [q(9), q(10), q(11)], [s(49), s(50), s(51)],
			"Left (Q9/49), right (Q10/50) and bottom (Q11/51) bumpers with 26-1200 coils and stack switches 180-5015-03; the G.I. "
			"circuit V lights all three ('GIs in Pop Bumpers (X3)'), each with one #555 wedge-base bulb on the bumper assembly "
			"page, which the G.I. wiring page counts as #44. Each switch fired its own coil in the gameplay run.", run),
		_mechanism("slingshots", "Slingshots", "other", [q(17), q(18)], [s(59), s(62)],
			"Left (Q17/59) and right (Q18/62) slingshots, Slingshot Assemblies 500-5849-00 with 23-800 coils and two parallel blade "
			"contacts per side; each switch fired its own coil in the gameplay run.", run, assembly="500-5849-00"),
		_mechanism("lower-flippers", "Lower flippers", "other", [q(15), q(16)], [dedicated_id(84), dedicated_id(83), dedicated_id(82), dedicated_id(81)],
			"Left (500-6682-12) and right (500-6682-02) flipper assemblies, both with 22-1080 coils, on one 50v supply. The CPU "
			"applies a 40 ms pulse on a button closure and then 1 ms every 12 ms while the button is held; each N.C. end-of-stroke "
			"switch opens at full stroke, and a closure during a hold earns another 40 ms pulse. PinMAME publishes Q15 at 47/48 and "
			"Q16 at 45/46 and writes the end-of-stroke inputs 81 and 83 itself from the solenoid state.",
			(MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE)),
		_mechanism("uk-post-save", "UK Post Save deflectors and center post", "other", [aux_output_id(33), aux_output_id(34), aux_output_id(35)], [s(1), s(8)],
			"UK only: the Solenoid Expander Auxiliary board 520-5068-01 drives AUX 1 and AUX 3, the left and right outlane Ball "
			"Deflector Assemblies 500-5788-02, and AUX 2, the center Up/Down Post Assy 500-6293-00 between the flippers. The Post "
			"Save buttons under the flipper buttons ask the ROM for them: the left button (1) the left deflector, the right button (8) "
			"the right one, both together the center post. A standard machine fits none of them; on term3's default settings the "
			"gameplay run's button holds fired none.", (MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE)),
		_mechanism("captive-ball", "Captive ball", "other", [], [s(23)],
			"IPDB lists a captive ball. The location drawing puts switch 23 CAPTIVE BALL, a Modular S-U Target Square (Red) "
			"500-6139-02, at it: the struck captive ball hits that target. In the gameplay run a closure blinked the G.I. and the "
			"backbox switched G.I. and flashed 30-32.", run + (IDENTITY_SOURCE,)),
		_mechanism("heads", "T-X and T-850 heads", "toy", [lamp_id(64), lamp_id(71), q(26)], [],
			"IPDB: 'Terminator and T-X heads on playfield'. The TX Head 545-6086-00 with its arm cover and cannon carries the #44 "
			"bulb of lamp 64 and the Q26 flasher sockets; the T-850 Head with LED Assembly 500-6701-00 carries lamp 71, the 'Big Red "
			"LED' TERMINATOR EYE. The coil chart lists no driver that moves either head; two above-playfield G.I. reflector bulbs "
			"point at the T-X and T-850.", (MANUAL_SOURCE, IDENTITY_SOURCE)),
	]


# --- Drivers -------------------------------------------------------------------------------------------
def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {driver["id"]: driver for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
	if set(by_id) != set(DRIVER_IDS):
		raise RuntimeError(f"Terminator 3 driver family differs from the catalog: {sorted(set(DRIVER_IDS) ^ set(by_id))}")
	records = []
	for driver_id in sorted(DRIVER_IDS):
		source = by_id[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
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
		"id": f"excerpt.terminator-3.{name}", "locator": locator, "path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"], "method": method, "transcribed_by": credit, "reviewed": reviewed,
	}


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("diagnostic-aids-and-dip-switches", "PDF page 5, printed DR. 3, Diagnostic Aids and CPU DIP Switch Settings (SW300 country charts)"),
		_excerpt("switch-matrix", "PDF page 6, printed DR. 4, Switch Matrix Grid, Dedicated Switches & Locations"),
		_excerpt("lamp-matrix", "PDF page 7, printed DR. 5, Lamp Matrix Grid & Locations"),
		_excerpt("coil-table", "PDF page 8, printed DR. 6, Coils Detailed Chart Table"),
		_excerpt("coil-flash-locations", "PDF page 9, printed DR. 7, Coil & Flash Lamp Locations"),
		_excerpt("gi-wiring", "PDF page 121, printed Section 5, Chapter 2, Page 103, General Illumination Circuit Detailed Wiring Diagram, including two notes found only in its text layer, and the bumper bulb item on PDF page 101"),
		_excerpt("flipper-circuit", "PDF page 124, 2-Flipper Circuit Wiring Diagram"),
		_excerpt("cabinet-wiring", "PDF page 126, printed Section 5, Chapter 3, Page 108, Cabinet / Coin Door Wiring Diagram"),
		_excerpt("opto-boards", "PDF pages 127-128 (Trough Up-Kicker Dual OPTO boards, OPTO Troubleshooting) and 169 (Single OPTO boards)"),
		_excerpt("mechanism-assemblies", "PDF page 2 (front page), 41 (RPG Backbox Test), 84 (playfield switch parts) and 94-116 (major assemblies, printed 76-98; selected items)", reviewed=False),
	]


def source_records() -> list[dict[str, Any]]:
	raw_runs = load_runtime()["runtime"]["raw_runs"]
	runs = ", ".join(f"{raw['name']} (run.json SHA-256 {raw['sha256'][:12]}..., directory manifest {RUN_MANIFESTS[raw['name']][:12]}...)" for raw in raw_runs)
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the term3 clone tree (" + ", ".join(DRIVER_IDS) + ")",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				f"src/wpc/segames.c (SHA-256 {SEGAMES_SHA256}) INITGAME (line 12: FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), swCol 0, lampCol 2, "
				"custSol 0), T3_SND and the fourteen term3 ROM sets on de_mSES2 (lines 1358-1478); src/wpc/se.c (SHA-256 "
				f"{SE_SHA256}) MACHINE_INIT(se) (the fast-flip byte at CPU RAM 0x04 for every term3 set, lines 380-381), the "
				"fast-flip block publishing public 15, the term3 PWM bulb models (#44 on 4, #89 on 26-32; lines 538-541), switch_r "
				"(~core_getSwCol), dedswitch_r, dip_r, se_solenoid_w (Q15/Q16 masked off and published at 47/45), the G.I. relay at "
				"gi[0] and the auxiliary board 520-5068-01 latch on 33-35 (lines 829-836), ram_w's memory-protect gate on -3; "
				"src/wpc/se.h SE_BOARDID_520_5068_01 ('Auxiliary driver board with 3 latched solenoid outputs'); src/wpc/core.h "
				f"FLIP_SOL(x) including FLIP_EOS(x) and CORE_FLIPSTROKETIME 2; src/wpc/core.c (SHA-256 {CORE_C_SHA256}) "
				"core_updateSw's EOS simulation (lines 1848-1866)."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/whitestar.json", "revision": "repository",
			"locator": "Whitestar public switch (-3..0, 1-64, 81-88), DIP 1-8, solenoid 1-50, lamp and GI 0 address rules and their notes",
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-31T05:42:36Z",
			"locator": (
				"IPDB machine 4787 'Terminator 3: Rise of the Machines' (Stern Pinball, June 2003, Sega/Stern Whitestar), retained "
				f"from the Wayback Machine capture {IPDB_WAYBACK_URL} because IPDB is Cloudflare-gated, as {IPDB_PAGE_NAME} under "
				f"{MANUALS_DIRECTORY}. Title, manufacturer, date and player and ball counts match the manual and the pinned catalog."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors; retrieved from the Internet Archive's Wayback Machine",
			"excerpts": [_excerpt("ipdb-page", "The retained capture's machine fields, features, toys, credits, notes, ROM and documentation links", credit=QUOTE_CREDIT)],
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": f"external:{MANUALS_DIRECTORY}/{MANUAL_NAME}", "original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256, "acquired_at": "2026-10-31T05:42:55Z",
			"locator": (
				"Stern Terminator 3: Rise of the Machines Pinball Game Service Manual (218 pages). PDF 2 is the front page, PDF 5-9 the "
				"front-matter Dr. Pinball sheets (DR. 3 diagnostic aids and DIP settings, DR. 4 switch grid and locations, DR. 5 lamp "
				"grid and locations, DR. 6 coil chart, DR. 7 coil and flash locations), PDF 41 the RPG Backbox Test, PDF 84 the "
				"playfield switch parts, PDF 94-116 the major assemblies (printed pages 76-98, the PDF page less 18), PDF 121-128 the "
				"G.I., flipper, cabinet and trough opto pages and PDF 169 the single opto boards. Its text layer uses a re-encoded font, "
				"so every cited region was read from renders. Retrieved from the Wayback Machine capture "
				f"{MANUAL_WAYBACK_URL} of IPDB's direct resource {MANUAL_URL}, because IPDB is Cloudflare-gated."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Stern Pinball, Inc.; hosted by the Internet Pinball Database, retrieved from the Internet Archive's Wayback Machine",
			"excerpts": _manual_excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "known_working": True,
			"uri": f"external:pinmame-vpx-sources/stern/{SLUG_PATH}/hanibal-1-5/" + quote(TABLE_NAME),
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				"Retained Terminator 3 Hanibal 1.5 recreation (table info: 'Terminator 3 - Rise of the Machines' by Hanibal, released "
				"05.01.2018; script header 'Terminator 3 Hanibal 4k VPX Version', 'Optimizations by Darthmarino'). Exact playfield "
				f"bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. Geometry "
				f"authority only for the objects its embedded script binds; the placement seed tools/seeds/stern/{SLUG_PATH}-spatial.json "
				"lists them. Retained by copying the contributor's table collection file (modified 2018-01-30T15:13:58Z) into the "
				"working root."
			),
			"acquired_at": "2026-10-31T05:54:51Z",
			"license": "NOASSERTION", "attribution": "Hanibal (table author); optimizations by Darthmarino", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "known_working": True,
			"uri": f"external:pinmame-vpx-sources/stern/{SLUG_PATH}/hanibal-1-5/" + quote("Terminator 3 (Stern 2003) Hanibal v1.5/script.vbs"),
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256,
			"locator": (
				"The retained table's embedded script as vpxtool extracts it, byte-identical to the retained sidecar .vbs (written "
				"beside the retained table at 2026-10-31T05:54:57Z; the collection file has no sidecar) and to the pinned standalone "
				"corpus's .vbs.original checkout. Runtime authority for controller callbacks: cGameName = \"term3\" "
				"with UseSolenoids = 1, UseLamps = 1 and UseGI = 0, LoadVPM \"01560000\", \"SEGA.VBS\", 3.26, .HandleMechanics = 0, "
				"the bsTrough, bsvuk and bstxhole ball stacks, the dtdroptarget drop target, the plungerIM impulse plunger, the "
				"Solcallback table, the lamp copies and the switch handlers. Known table defects: the stacking opto 15, the UK buttons "
				"1 and 8 and the EOS inputs 81/83 are never written, flasher 29 is unbound, lamps 73-79 are drawn on no Light, and "
				"the backbox kicker fires only while the table's own ball is in the backbox. Extracted from the retained table with "
				"vpxtool git:v0.33.3."
			),
			"acquired_at": "2026-10-31T05:55:31Z",
			"license": "NOASSERTION", "attribution": "Hanibal (table author)", "rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment line of the embedded script that binds the controller, with its line number", credit=QUOTE_CREDIT)],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under the vpxtool extraction "
				f"'{EXTRACTION_RELATIVE_PATH.as_posix()}'; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table at 2026-10-31T05:55:30Z; the "
				f"manifest was written at 2026-10-31T07:20:31Z. Bounds are {TABLE_BOUNDS}."
			),
			"acquired_at": "2026-10-31T05:55:30Z",
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_CORPUS_SIGGI_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_REVISION}/" + quote(SIGGI_PATH, safe="/"),
			"revision": VPXTABLE_REVISION, "sha256": SIGGI_SHA256,
			"locator": (
				"Pinned corpus script of a different table lineage (header 'VPX by jpsalas 2022, version 4.0.0', 'Artistic Re-Skin by "
				"Siggi 2022', 'Physics/Sound/VR upgrade by TastyWasps 2024'), cGameName \"term3\" (line 136): vpmNudge.TiltSwitch = 56 "
				"(line 370), the trough InitSw 0, 14, 13, 12, 11 (line 377), the VUK InitSw 0, 36 (line 389), the lockup InitSw 0, 33, "
				"34, 35 (line 399), InitDrop sw25, 25 (line 407), switch 55 and 53 key writes (lines 602-655), sw31_Hit pulsing 31 "
				"into the lockup (line 813), the backbox targets 41-45 (lines 873-877) and the solenoid table (lines 923-946), which "
				"names 5 the backbox kicker, 20 the RPG motor, 21 the back-panel diverter, 22 and 23 the left and center up posts and "
				"29 the 'Super JP' flasher, and marks 19 and 25 not used and 24 optional. It corroborates the retained bindings from "
				"an independent table."
			),
			"license": "NOASSERTION", "attribution": "Authors credited in Terminator 3 (Stern 2003) Siggi-TW VLM mod.vbs and repository contributors",
		},
		{
			"id": VPX_CORPUS_HANIBAL_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{STANDALONE_REVISION}/" + quote(HANIBAL_CORPUS_PATH, safe="/"),
			"revision": STANDALONE_REVISION, "sha256": SCRIPT_SHA256,
			"locator": (
				"Pinned corpus copy of the retained table's own script (the folder's unpatched .vbs.original), so it adds no "
				"independent support; it pins the retained script to a public revision. The retained SHA-256 is the repository "
				"checkout's CRLF materialization; the linked Git blob is the identical LF-normalized text (SHA-256 "
				f"{HANIBAL_CORPUS_LF_SHA256})."
			),
			"license": "NOASSERTION", "attribution": "Authors credited in Terminator 3 (Stern 2003) Hanibal v1.5 and repository contributors",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-review-artifacts/vpm-script-libs/sega.vbs",
			"original_filename": "sega.vbs", "sha256": VPM_SEGA_SHA256,
			"locator": (
				"VPinMAME Sega/Stern Whitestar script library the retained table loads, copied from the contributor's Visual Pinball "
				f"Scripts folder beside the core.vbs it executes (SHA-256 {VPM_CORE_SHA256}). It defines GameOnSolenoid = 15, swBlack 0 "
				"/ swGreen -1 / swRed -2 / swMemoryProtect -3, swStartButton 54, swTilt 56, swSlamTilt 55, swCoin3 4 / swCoin1 5 / "
				"swCoin2 6, swLRFlip 82, swLLFlip 84, swURFlip 81 and swULFlip 83, and the country DIP form."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME script authors",
			"excerpts": [_excerpt("vpm-script-library", "sega.vbs constants (lines 20-39), DIP form (lines 52-69) and key handlers (lines 71-139)", credit=QUOTE_CREDIT)],
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/term3.zip", "revision": "4.00", "sha256": ROM_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned term3 ROM set (t3cpu.400 CRC 872f9351, t3dispa.400 CRC 6b7cc4f8, T3_SND); used to identify the ROM the harness booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external",
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				f"Seven hash-pinned LibPinMAME harness runs of term3 (library SHA-256 {RUNTIME_LIBRARY_SHA256[:12]}..., built from "
				f"{PINMAME_REVISION[:8]}) from empty NVRAM with mechanism handling off: {runs}. Four walk the Portals Switch, Dedicated "
				"Switch, Single Lamp and Single Coil Tests; three exercise the stacking opto, a ball serve with the gun-trigger launch "
				"and a scripted game. Scenarios under tools/harness-scenarios/whitestar; tools/terminator_3_runtime_evidence.py derives "
				"the committed per-step transitions from the retained runs and the service-test frames as diagnostic snapshots whose "
				f"readings tools/seeds/stern/{SLUG_PATH}-frame-readings.json pins by pixel SHA-256."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
def _check_unused_outputs(definition: dict[str, Any], evidence: dict[str, Any]) -> None:
	"""Refuse to build if any run other than the Single Coil Test, which fires every driver, saw an unused solenoid address
	or a UK auxiliary output change, or if PinMAME published a G.I. string other than 0."""
	observations = evidence["runtime"]["observations"]
	outside = set()
	for observation in observations["named_action_observations"]:
		if not observation["label"].startswith(f"{COIL_TEST_RUN} "):
			outside |= set(observation["transitioned_solenoid_addresses"])
	quiet = set(AUX_OUTPUTS) | {
		device["binding"]["device"] for device in definition["outputs"]
		if device["binding"]["group"] == SOLENOID_GROUP and device["availability"] == "unused"
	}
	if outside & quiet:
		raise RuntimeError(f"Terminator 3 runtime evidence saw unused or UK-only outputs outside the Single Coil Test: {sorted(outside & quiet)}")
	if observations["gi_addresses_seen"] != [0]:
		raise RuntimeError(f"Terminator 3 runtime evidence saw G.I. strings {observations['gi_addresses_seen']}")


def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Terminator 3: Rise of the Machines", "manufacturer": "Stern", "year": 2003, "kind": "physical_pinball",
			"ipdb_id": 4787, "opdb_id": "GR91N-MLOyE",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["output_semantics", "spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate", "physical_wiring": "validated",
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
		"knowledge": {"path": f"knowledge/stern/{SLUG_PATH}.md", "status": "complete"},
		"conflicts": [],
	}
	evidence = load_runtime()
	append_service_test_readings(definition, evidence)
	_check_unused_outputs(definition, evidence)
	identifiers =[device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Terminator 3 device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Terminator 3 mechanism {mechanism['id']} names unknown devices: {unknown}")
	return definition


# --- Extraction manifest -------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Terminator 3 retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest", "version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Terminator 3 extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Terminator 3 retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Terminator 3 retained extraction manifest does not match the files under the extraction")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Terminator 3 retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
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
	seed = _spatial_seed()
	near_bulbs = [
		(int(address), entry, primitive)
		for address, entries in sorted(seed["lamp_unplaced"].items(), key=lambda item: int(item[0]))
		for entry in entries for primitive in entry["bulb_primitives"]
	]
	if not near_bulbs:
		raise RuntimeError("Terminator 3 spatial seed: the report expects the head primitives drawing 'bulb' beside lamps 64 and 71")
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
			"manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}", "source_ref": VPX_EXTRACTION_SOURCE,
		},
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": (
				"The centre of the VPX object the embedded script binds to each switch (trigger, hit target, kicker, slingshot wall, "
				"bumper, drop-target wall). The trough switches 11-14 and the stacking opto 15, which the table does not model, are "
				"projected onto the release kicker BallRelease; the lockup switches 33-35 onto the lockup entry kicker txshot; each "
				"end-of-stroke contact onto its flipper."
			),
			"lamp": (
				"None placed. A lamp is placed only on a Light the script drives for it that is a bulb Light showing its bulb mesh "
				"(is_bulb_light and show_bulb_mesh). The script drives the bulb-mode Lights l<n>a (the Flasherupdate timer's copy "
				"of insert l<n>) for lamps 1-52, 55-62, 72 and 80, l64 and its copy l64a for lamp 64, and l71 for lamp 71; none "
				"shows a bulb mesh, so none marks a socket (docs/SPATIAL.md, picking the bulb)."
			),
			"solenoid": (
				"The kicker, slingshot wall, bumper, flipper, plunger or wall the script fires; the drop-target coils on the target "
				"sw25; the auto launch on the shooter-lane trigger swplunger its impulse plunger fires from; the T-X VUK on the "
				"lockup entry kicker txshot; for flashers 31 and 32 the bulb Lights that coincide (within 0.002) with the Flupper "
				"dome primitives Flasher31p1/p2 and Flasher32p1/p2 the script switches between DomeOn and DomeOff. The UK-only auxiliary outputs, which the US table does not model, are projected onto the outlane "
				"rollovers 57 and 60 and the flippers' midpoint, where the coil location drawing draws them."
			),
			"gi": (
				f"The {len(seed['gi']['0'])} GIGruppe render-double clusters that draw a bulb mesh, each placed on its bulb Light; "
				f"the {len(seed['gi_excluded']['0'])} clusters that draw none are render helpers and are listed in the seed, not placed."
			),
		},
		"unresolved_geometry": [
			"The trough switches 11-15 and the lockup switches 33-35 are not modelled by the table; their placements are projections onto mechanism objects.",
			"The T-X flashers 26 and the Super Jackpot flasher 29 have no bulb Light in the table; they need the coil and flash lamp location drawing (DR. 7) or playfield photographs to place.",
			(
				"No playfield lamp has a coordinate. The bulb-mode Lights the script drives for lamps 1-52, 55-62, 64, 71, 72 and 80 "
				"show no bulb mesh, the table models no bulb primitive or baked bulb mesh under the inserts, and lamps 73-78 are "
				"drawn on no Light. Placing lamps 1-80 needs a table that models the insert bulbs or a reproducible measurement on "
				f"the lamp location drawing (DR. 5). {len(near_bulbs)} toy primitives drawing the image 'bulb' sit in the heads beside "
				"these Lights: "
				+ "; ".join(f"{primitive['object']} ({primitive['material']}) {primitive['distance']:g} from {entry['object']} (lamp {address})" for address, entry, primitive in near_bulbs)
				+ f"; whether they mark the sockets of lamps {' and '.join(sorted({str(address) for address, _, _ in near_bulbs}, key=int))} is not decided here."
			),
			"The UK-only auxiliary outputs 33-35 are projections onto US-table objects.",
			"The table's G.I. sockets are not a census of the 40 playfield G.I. bulbs the G.I. page counts, five of them lie by the rear edge where the back panel's light board stands, and none is matched to a circuit.",
			"No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.",
		],
		"promotion_decision": "partial: devices without placements, projections, and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Terminator 3: Rise of the Machines (Stern, 2003) spatial blockers", "",
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
		raise RuntimeError(f"Refusing to overwrite an author-ready Terminator 3 artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Terminator 3 author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"Terminator 3 deterministic artifact drift: {path}")
	print("Terminator 3 definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"Terminator 3 extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Terminator 3 retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
