"""Curate the physical Stern Harley-Davidson (1999) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived
fact as a literal and reads one committed seed, the placements (the retained table's object coordinates, rebuilt by
tools/harley_davidson_spatial_seed.py), so regeneration reproduces the canonical artifact byte-for-byte without reading
the external evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only path that writes the
definition, its knowledge note and its spatial report.
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

MACHINE_ID = "stern.harley-davidson.1999"
PARTIAL_PATH = ROOT / "machines/partial/stern/harley-davidson-1999.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/harley-davidson-1999.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/harley-davidson-1999.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/stern/harley-davidson-1999-knowledge.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/stern/harley-davidson-1999-spatial.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/harley-davidson-1999.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/stern/harley-davidson-1999.md"
RUNTIME_A40_PATH = "evidence/runtime/whitestar/harley-davidson-harl-a40-motorcycle-and-gameplay.json"
RUNTIME_A30_PATH = "evidence/runtime/whitestar/harley-davidson-harl-a30-gameplay.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = "pinmame.catalog.46e1a01a0f73"
CORE_SOURCE = "pinmame.core.46e1a01a0f73"
SIM_SOURCE = "pinmame.sim.harley.46e1a01a0f73"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
IDENTITY_SOURCE = "identity.stern.harley-davidson.1999"
MANUAL_SOURCE = "manual.stern.harley-davidson.1999"
TECH_BRIEF_SOURCE = "service-bulletin.stern.harley-davidson.tech-brief-49"
VPX_TABLE_SOURCE = "vpx-table.harley-davidson-1-2"
VPX_SCRIPT_SOURCE = "vpx-script.harley-davidson-1-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.harley-davidson-1-2"
VPX_CORPUS_119_SOURCE = "vpx-script.6c9fb236b2931fc9"
VPX_CORPUS_112_SOURCE = "vpx-script.e101da5130f14724"
VPM_LIBRARY_SOURCE = "vpm-script-library.sega-vbs"
RUNTIME_SOURCE = "runtime.harley-davidson.harl-a40"
RUNTIME_A30_SOURCE = "runtime.harley-davidson.harl-a30"
ROM_SOURCE = "rom.stern.harley-davidson.4-00"
ROM_A30_SOURCE = "rom.stern.harley-davidson.3-00"
RUNTIME_LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "44b92f640fea2b9769fcdb50b2745b50c6d56be747efc360fd8acf20f7b3133f"
ROM_A30_ARCHIVE_SHA256 = "741d57f93a6ac346e07decc3ae668bbfe145a6c717c0c52b96537bc5a91ff07c"
SIM_FILE_SHA256 = "070ee2efff5af57872edd5ec1c60c63b91fa24d58e41370f740035f3673d7f14"
# Retained harness run directory -> SHA-256 of its manifest.json (tools/harley_davidson_runtime_evidence.py pins the same values).
RUN_MANIFESTS = {
	"harl-a40-motorcycle-home-search": "b5b1652b85c5ea18cf933168ae8fea9cafa8acd541c872e85f403843ae0c43bc",
	"harl-a40-motorcycle-up-at-boot": "e33a9563155600a0808659178623d1ea9c8e0e40ced4f9e3777107952e94a303",
	"harl-a40-motorcycle-down-at-boot": "ab722436d9dc30c86c5c6b5d3de40ca1ba7643755c93ecc0a14f1499b4b56cdd",
	"harl-a40-motorcycle-ball-start-lift": "c5cf2be5b730b80633be12bbf6816c1295668fa0058717a0a09b445a87d29721",
	"harl-a40-stacking-opto": "f58375074e35f7ac681f56ce61caeffa8d904c89bdb4870591369868d2b280c2",
	"harl-a40-gameplay": "64ad60eb6410fc13edc32dedf90696bf2c008aaee64ff770bfd76d2d31ca34e4",
	"harl-a40-launch-scoop-opto": "33081f05b4e3e9976e1e1aed002f4656d3cee6b5eea43e96907b2c80a03d09ee",
	"harl-a40-ds5-probe": "03eb45b89755b60c573863128f26133b6cd89fb203fc03981cf985719508598e",
	"harl-a40-dedicated-switch-test": "0eac4e3108c51f6bda3ca464a4adb0b5d7741bc6b9b82f9349802c9da7713c85",
	"harl-a30-gameplay": "099691b8988b6cddea825f9a72714893e8b14de6e75e4fea61971f5cf1f5923d",
}

TABLE_NAME = "Harley Davidson (Sega 1999) 1.2.vpx"
TABLE_SHA256 = "349bc4e4d68173138928baed0a0fbfdb0d04ef78ca07dfbcfdf8d2583255cf37"
SCRIPT_SHA256 = "eb0960bc9670cd367f7f2ce838e2969d4546b98abe5c8fc4d4df3fd53d32bc50"
CORPUS_119_SHA256 = "6c9fb236b2931fc94734143ff7cbeaa45a08e6e19c7c5b0f1963d2f5548be7f1"
CORPUS_112_SHA256 = "e101da5130f14724de2e5b55456c6d008b7cd84742a96245f4b0cd131abc3aad"
CORPUS_112_LF_SHA256 = "b8c020353c369a0429a19f3c4bc9250da804eec1c92d885aa9af465f691ba950"
VPXTABLE_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
MANUAL_NAME = "Stern_Harley_Davidson_3rd_Edition_Pinball_Game_Service_Manual.pdf"
MANUAL_SHA256 = "a10e91542f9c8ab965d18908626114d1d03cba499f36fa47751045e8adae4731"
TECH_BRIEF_NAME = "Stern_1999_Harley_Davidson_1st_Edition_Technical_Brief_49_Rev.pdf"
TECH_BRIEF_SHA256 = "7605f4c4a875ab9e2e1f599a772e2f06e001f10fa557e573e8a7114f11c9624d"
IPDB_PAGE_SHA256 = "0e2e981a588917393eeb3c2f14526144a0186b2a97d0033bdf2e224049f7463e"
IPDB_PAGE_SHA256S = {
	5277: "cbd90ef38f782554a73e00df6fdb1bf386bc0481f9a6077eab0b02b1bf4c56f6",
	4664: "f98ab92c17b14b7a0a1103c7426eb589990bb6be72e96d7fa8f34aa937178d2a",
	4453: "13da86a8b46e2fe6dd002d285948885973969426b3700138adc4b41eb6356c1f",
}
VPM_SEGA_SHA256 = "d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
PLAYFIELD_WIDTH = 1000.0
PLAYFIELD_HEIGHT = 2000.0
TABLE_BOUNDS = "left=0 top=0 right=1000 bottom=2000"

EXTRACTION_FILE_COUNT = 691
EXTRACTION_TOTAL_BYTES = 136344516
EXTRACTION_MANIFEST_SHA256 = "c92e6bba4c9c6b5400b5e2a24e8bbd7f8d7018b8ef4337404291f1bd96fb17fc"
EXTRACTION_RELATIVE_PATH = Path("stern/harley-davidson-1999/v1-2/Harley Davidson (Sega 1999) 1.2")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("stern/harley-davidson-1999/v1-2/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"
MANUALS_DIRECTORY = f"pinmame-manuals/by-machine/{MACHINE_ID}/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=4455"
MANUAL_URL = "https://www.ipdb.org/files/5277/" + MANUAL_NAME
TECH_BRIEF_URL = "https://www.ipdb.org/files/4455/" + TECH_BRIEF_NAME
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
DRIVER_IDS = (
	"harl_a18", "harl_a30", "harl_a40", "harl_f18", "harl_f30", "harl_f40", "harl_g18", "harl_g30", "harl_g40",
	"harl_i18", "harl_i30", "harl_i40", "harl_l18", "harl_l30", "harl_l40",
)
BASE_DRIVER_NOTE = (
	"src/wpc/sims/se/prelim/harley.c builds every Stern Harley-Davidson driver on the de_mSES1 machine driver with the same "
	"HARLEY_SOUND set (hdsnd.u7 and the voice ROMs hdvc1-4) and one init_harl, which installs harlGameData: GEN_WS, a 128x32 "
	"DMD, FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), lamp columns 2, no custom solenoids, no auxiliary board, and harley_handleMech. "
	"The controller routing, lamp columns and display are therefore identical. The 3rd-edition manual's board table lists one "
	"row for the '1st-3rd Editions', and its firmware appendix lists the original A1.03 (display A1.04), the 2nd edition "
	"A1.08 (display A1.05) and the 3rd edition A3.00 (display A3.00); the editions differ in art, trim and the motorcycle "
	"models, not in wiring. "
)
DISPLAY_ROMS = {
	"harl_a40": ("4.00", "hddispa.400", "e2c98397", "English"), "harl_f40": ("4.00", "hddispf.400", "d061c238", "French"),
	"harl_g40": ("4.00", "hddispg.400", "4bc89a23", "German"), "harl_i40": ("4.00", "hddispi.400", "c4fc4990", "Italian"),
	"harl_l40": ("4.00", "hddispl.400", "96096e73", "Spanish"),
	"harl_a30": ("3.00", "hddispa.300", "61b274f8", "English"), "harl_f30": ("3.00", "hddispf.300", "106f7f1f", "French"),
	"harl_g30": ("3.00", "hddispg.300", "8f7da748", "German"), "harl_i30": ("3.00", "hddispi.300", "686d3cf6", "Italian"),
	"harl_l30": ("3.00", "hddispl.300", "4cc7251b", "Spanish"),
	"harl_a18": ("1.08", "hddispa.105", "401a7b9f", "English"), "harl_f18": ("1.08", "hddispf.105", "31c77078", "French"),
	"harl_g18": ("1.08", "hddispg.105", "aed5a82f", "German"), "harl_i18": ("1.08", "hddispi.105", "49c53391", "Italian"),
	"harl_l18": ("1.08", "hddisps.105", "6d6f2a7c", "Spanish"),
}
CPU_ROMS = {"4.00": ("harcpu.400", "752ed258"), "3.00": ("harcpu.300", "c4ba9df5"), "1.08": ("harcpu.108", "a8e24328")}
DRIVER_COMPATIBILITY = {driver_id: "identical" for driver_id in DRIVER_IDS}


def _driver_note(driver_id: str) -> str:
	version, display, display_crc, language = DISPLAY_ROMS[driver_id]
	cpu, cpu_crc = CPU_ROMS[version]
	note = f"CPU {version} ({cpu}, CRC {cpu_crc}) with the {language} display ROM {display} (CRC {display_crc})."
	if version == "4.00":
		note += (
			" No factory document this record holds names a 4.00 release; the firmware appendix ends at the 3rd edition's A3.00."
		)
	elif version == "3.00":
		note += " The 3rd-edition firmware (Appendix A: game ROM A3.00, display A3.00, 2004)."
	else:
		note += " The 2nd-edition firmware (Appendix A: game ROM A1.08, display A1.05, 2002-2003)."
	if driver_id == "harl_l18":
		note += " Its Spanish display ROM is named hddisps.105, where the 3.00 and 4.00 Spanish sets use hddispl."
	if driver_id == "harl_a30":
		note += (
			" The retained table loads it (Const cGameName=\"harl_a30\"). MACHINE_INIT(se) gives only this set the fast-flip byte at "
			"CPU RAM 0x00, so only harl_a30 publishes the game-on state at public 15. Its gameplay harness run drew the same "
			"switch-to-output responses as harl_a40 apart from public 15 and lamp 69."
		)
	elif driver_id == "harl_a40":
		note += " MACHINE_INIT(se) sets no fast-flip byte for it, so public 15 never rises. Nine harness runs booted it."
	else:
		note += " MACHINE_INIT(se) sets no fast-flip byte for it, so public 15 never rises. No harness run booted it."
	return note


# --- Switch data -------------------------------------------------------------------------------------
# address -> (label, grid name, mounting class, part cell, switch type, availability, roles, pulse)
SWITCHES: dict[int, tuple[str, str, str, str, str, str, tuple[str, ...], bool]] = {
	1: ("Left Cabinet Button (UK Only)", "LEFT BUTTON (UK ONLY)", "on Cabinet side", "180-5160-00", "button", "optional", ("cabinet.uk-button-left",), False),
	2: ("4th Coin Slot", "4TH COIN SLOT", "On Coin Door", "180-5024-00", "other", "optional", ("cabinet.coin.fourth",), True),
	3: ("6th Coin Slot", "6TH COIN SLOT", "On Coin Door", "(Future Use)", "other", "optional", ("cabinet.coin.sixth",), True),
	4: ("Right Coin Slot", "RIGHT COIN SLOT", "On Coin Door", "180-5024-00", "other", "used", ("cabinet.coin.right",), True),
	5: ("Center Coin Slot / DBA", "CENTER COIN SLOT / DBA", "On Coin Door", "180-5024-00", "other", "used", ("cabinet.coin.center",), True),
	6: ("Left Coin Slot", "LEFT COIN SLOT", "On Coin Door", "180-5024-00", "other", "used", ("cabinet.coin.left",), True),
	7: ("5th Coin Slot", "5TH COIN SLOT", "On Coin Door", "(Future Use)", "other", "optional", ("cabinet.coin.fifth",), True),
	8: ("Right Cabinet Button (Skill)", "RIGHT BUTTON (SKILL)", "on Cabinet side", "180-5160-00", "button", "used", ("cabinet.post-button",), False),
	11: ("4-Ball Trough 1 (Left)", "4-BALL TROUGH #1 (LEFT)", "Under P/F", "180-5119-00", "microswitch", "used", ("ball.position",), False),
	12: ("4-Ball Trough 2", "4-BALL TROUGH #2", "Under P/F", "180-5119-00", "microswitch", "used", ("ball.position",), False),
	13: ("4-Ball Trough 3", "4-BALL TROUGH #3", "Under P/F", "180-5119-00", "microswitch", "used", ("ball.position",), False),
	14: ("4-Ball Trough VUK Opto", "4-BALL TROUGH VUK OPTO", "Under P/F", "BOT TRANS: 520-5173-00 / BOT REC: 520-5174-00", "opto", "used", ("ball.position",), False),
	15: ("4-Ball Stacking Opto", "4-BALL STACKING OPTO", "Under P/F", "TOP TRANS: 520-5173-00 / TOP REC: 520-5174-00", "opto", "used", ("ball.path",), False),
	16: ("Shooter Lane", "SHOOTER LANE", "Under P/F", "180-5100-01", "unknown", "used", ("ball.position",), False),
	17: ("Left 4-Bank Drop Target L", "LT 4-BANK D/T (L) IVE", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	18: ("Left 4-Bank Drop Target I", "LT 4-BANK D/T L (I) VE", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	19: ("Left 4-Bank Drop Target V", "LT 4-BANK D/T LI (V) E", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	20: ("Left 4-Bank Drop Target E", "LT 4-BANK D/T LIV (E)", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	21: ("Right 4-Bank Drop Target R", "RT 4-BANK D/T (R) IDE", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	22: ("Right 4-Bank Drop Target I", "RT 4-BANK D/T R (I) DE", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	23: ("Right 4-Bank Drop Target D", "RT 4-BANK D/T RI (D) E", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	24: ("Right 4-Bank Drop Target E", "RT 4-BANK D/T RID (E)", "Under P/F", "180-5104-00", "leaf", "used", (), False),
	25: ("Right Ramp Enter", "RIGHT RAMP ENTER", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	26: ("Right Ramp Exit", "RIGHT RAMP EXIT", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	27: ("Right Ramp Mid", "RIGHT RAMP MID", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	28: ("Spinner", "SPINNER", "Above P/F", "180-5010-04", "unknown", "used", (), True),
	29: ("Motorcycle Stand-Up Target Left", "S-U TRGT LT (M-CYCLE)", "Under P/F", "500-6138-02", "leaf", "used", (), True),
	30: ("Motorcycle Stand-Up Target Right", "S-U TRGT RT (M-CYCLE)", "Under P/F", "500-6138-02", "leaf", "used", (), True),
	31: ("Right Ramp Stand-Up Target Left", "S-U TRGT LT (RT RAMP)", "Under P/F", "500-6138-02", "leaf", "used", (), True),
	32: ("Right Ramp Stand-Up Target Right", "S-U TRGT RT (RT RAMP)", "Under P/F", "500-6138-02", "leaf", "used", (), True),
	33: ("Left Orbit", "LEFT ORBIT", "Under P/F", "500-6227-03", "microswitch", "used", ("ball.path",), False),
	34: ("Right Orbit", "RIGHT ORBIT", "Under P/F", "500-6227-04", "microswitch", "used", ("ball.path",), False),
	35: ("Motor Up", "MOTOR UP", "Under P/F", "180-5052-00", "microswitch", "used", ("mechanism.position",), False),
	36: ("Motor Down", "MOTOR DOWN", "Under P/F", "180-5052-00", "microswitch", "used", ("mechanism.position",), False),
	37: ("Motorcycle Enter Opto", "OPTO", "Under P/F", "TRANS 180-5082-00 / REC 180-5083-01", "opto", "used", ("ball.path",), True),
	41: ("Motorcycle Trough 4 (Top)", "M-CYCLE TROUGH #4 (TOP)", "Under P/F", "(1) 4-Position Membrane Switch: 181-5001-00", "other", "used", ("ball.position",), False),
	42: ("Motorcycle Trough 3", "M-CYCLE TROUGH #3", "Under P/F", "(1) 4-Position Membrane Switch: 181-5001-00", "other", "used", ("ball.position",), False),
	43: ("Motorcycle Trough 2", "M-CYCLE TROUGH #2", "Under P/F", "(1) 4-Position Membrane Switch: 181-5001-00", "other", "used", ("ball.position",), False),
	44: ("Motorcycle Trough 1 (Bottom)", "M-CYCLE TROUGH #1 (BOT)", "Under P/F", "(1) 4-Position Membrane Switch: 181-5001-00", "other", "used", ("ball.position",), False),
	45: ("Super VUK", "SUPER VUK", "Under P/F", "180-5052-00", "microswitch", "used", ("ball.position",), False),
	46: ("Ball Eject (Scoop)", "BALL EJECT (SCOOP)", "Under P/F", "180-5057-00", "microswitch", "used", ("ball.position",), False),
	48: ("Behind Top VUK", "BEHIND TOP VUK", "Under P/F", "180-5057-00", "microswitch", "used", ("ball.path",), True),
	49: ("Left Turbo Bumper", "LEFT TURBO BUMPER", "Under P/F", "180-5015-03", "leaf", "used", (), True),
	50: ("Right Turbo Bumper", "RIGHT TURBO BUMPER", "Under P/F", "180-5015-03", "leaf", "used", (), True),
	51: ("Bottom Turbo Bumper", "BOTTOM TURBO BUMPER", "Under P/F", "180-5015-03", "leaf", "used", (), True),
	52: ("Top Turbo Bumper", "TOP TURBO BUMPER", "Under P/F", "180-5015-03", "leaf", "used", (), True),
	53: ("Launch Button", "LAUNCH BUTTON", "Cabinet Front", "500-6121-06", "button", "used", ("cabinet.launch",), False),
	54: ("Start Button", "START BUTTON", "Cabinet Front", "500-6090-02", "button", "used", ("cabinet.start",), False),
	55: ("Slam Tilt", "SLAM TILT", "On Coin Door", "180-5022-00", "tilt", "used", ("cabinet.slam-tilt",), False),
	56: ("Plumb Bob Tilt", "PLUMB BOB TILT", "Inside Cabinet", "HANGER 535-5319-00 / CONTACT 535-7563-01", "tilt", "used", ("cabinet.tilt",), False),
	57: ("Left Outlane", "LEFT OUTLANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	58: ("Left Return Lane", "LEFT RETURN LANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	59: ("Left Slingshot", "LEFT SLINGSHOT", "Under P/F", "180-5054-00", "leaf", "used", (), True),
	60: ("Right Outlane", "RIGHT OUTLANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	61: ("Right Return Lane", "RIGHT RETURN LANE", "Under P/F", "500-6227-02", "microswitch", "used", (), False),
	62: ("Right Slingshot", "RIGHT SLINGSHOT", "Under P/F", "180-5054-00", "leaf", "used", (), True),
}
UNUSED_SWITCHES = (9, 10, 38, 39, 40, 47, 63, 64)
DOTS_SWITCHES = (45, 46)
DODB_SWITCHES = (41, 42, 43, 44)
MATRIX_DRIVE = [("GRN-BRN", "CN5-P1"), ("GRN-RED", "CN5-P3"), ("GRN-ORG", "CN5-P4"), ("GRN-YEL", "CN5-P5"), ("GRN-BLK", "CN5-P6"), ("GRN-BLU", "CN5-P7"), ("GRN-VIO", "CN5-P8"), ("GRN-GRY", "CN5-P9")]
MATRIX_RETURN = [("WHT-BRN", "CN7-P9", "U400"), ("WHT-RED", "CN7-P8", "U400"), ("WHT-ORG", "CN7-P7", "U400"), ("WHT-YEL", "CN7-P6", "U400"), ("WHT-GRN", "CN7-P5", "U401"), ("WHT-BLU", "CN7-P3", "U401"), ("WHT-VIO", "CN7-P2", "U401"), ("WHT-GRY", "CN7-P1", "U401")]
# The printed page-15 switch table's longer description where it differs from the grid.
PAGE15_NAMES = {
	6: "LEFT COIN SLOT", 25: "RIGHT RAMP ENTER (Switch Gate)", 26: "RIGHT RAMP EXIT (Switch Gate)", 27: "RIGHT RAMP MID (Switch Gate)",
	29: "S-U TRGT LT (M-CYLE) (Nar. Trgt. Red)", 30: "S-U TRGT RT (M-CYLE) (Nar. Trgt. Red)", 31: "S-U TRGT LT (RT RAMP) (Nar. Trgt. Red)",
	32: "S-U TRGT RT (RT RAMP) (Nar. Trgt. Red)", 33: "LEFT ORBIT (Lt. Mount Roll-Over Lite Sw.)", 34: "RIGHT ORBIT (Rt. Mount Roll-Over Lite Sw.)",
	46: "BALL EJECT (Power Scoop / Kick Big)", 48: "BEHIND TOP VUK (Metal Under-Trough)", 53: "LAUNCH BUTTON (Yel.)", 54: "START BUTTON (Red)",
	55: "SLAM TILT (On Coin Door)", 57: "LEFT OUTLANE (Rt. Mount Roll-Over Sw.)", 58: "LEFT RETURN LANE (Rt. Mnt. R-O Sw.)",
	59: "LEFT SLINGSHOT (Double-Switch)", 60: "RIGHT OUTLANE (Rt. Mount R-O Sw.)", 61: "RT RETURN LANE (Rt. Mount R-O Sw.)",
	62: "RIGHT SLINGSHOT (Double-Switch)",
}
# What the retained 1.2 table's embedded script does with each address (line numbers of that script).
SWITCH_SCRIPT = {
	11: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 156-159): a cvpmBallStack holding 11 at 1 while a ball occupies that position",
	12: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 156-159)",
	13: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 156-159)",
	14: (
		"bsTrough.InitSw 0, 14, 13, 12, 11 (lines 156-159): 14 is the exit position the trough up-kicker empties, held at 1 while a "
		"ball waits there. The script also sets vpmNudge.TiltSwitch=14 (line 152), so the table's nudge tilt writes this trough "
		"opto instead of the plumb-bob tilt 56; both pinned corpus scripts of the later table set vpmNudge.TiltSwitch=56"
	),
	15: "never written: SolTrough, the only sub that pulses 15 (lines 70-74), is bound to no callback, because SolCallback(1) is bsTrough.SolOut",
	16: "cvpmBallStack bsLaunch (InitSaucer Kicker2, 16, 0, 44; line 172) holds 16 while a ball waits in the shooter lane",
	17: "cvpmDropTarget dtL (InitDrop sw17-sw20 to 17-20, line 181) holds 17 at 1 while its target is down (Sw17_Dropped, line 251)",
	18: "cvpmDropTarget dtL (line 181) holds 18 at 1 while its target is down (Sw18_Dropped, line 252)",
	19: "cvpmDropTarget dtL (line 181) holds 19 at 1 while its target is down (Sw19_Dropped, line 253)",
	20: "cvpmDropTarget dtL (line 181) holds 20 at 1 while its target is down (Sw20_Dropped, line 254)",
	21: "cvpmDropTarget dtR (InitDrop sw21-sw24 to 21-24, line 185) holds 21 at 1 while its target is down (Sw21_Dropped, line 256)",
	22: "cvpmDropTarget dtR (line 185) holds 22 at 1 while its target is down (Sw22_Dropped, line 257)",
	23: "cvpmDropTarget dtR (line 185) holds 23 at 1 while its target is down (Sw23_Dropped, line 258)",
	24: "cvpmDropTarget dtR (line 185) holds 24 at 1 while its target is down (Sw24_Dropped, line 259)",
	25: (
		"sw25_hit sets 25 and sw25_unhit clears it (lines 262-263), but sw25 is a VPX gate, which raises Hit and no Unhit event, so "
		"once the first ball passes the table leaves 25 at 1"
	),
	26: "Trigger26 holds 26 while the ball sits on it (lines 264-265)",
	27: (
		"trigger27_hit and trigger27_unhit (lines 266-267) name an object the table does not contain, so 27 is never written; the "
		"table's wire gate on the ramp near the top centre is named Trigger27q, and no handler names it"
	),
	28: "Spinner1_Spin pulses 28 on every spin (line 287)",
	29: "sw29_hit pulses 29 (line 290)",
	30: "sw30_hit pulses 30 (line 291)",
	31: "sw31_hit pulses 31 (line 292)",
	32: "sw32_hit pulses 32 (line 293)",
	33: "Trigger sw33 holds 33 while the ball sits on it (lines 271-272)",
	34: "Trigger sw34 holds 34 while the ball sits on it (lines 273-274)",
	35: "the cvpmMech mCycle (Sol1 = 19, Length 100, Steps 25, vpmMechOneSol + vpmMechReverse + vpmMechLinear; lines 196-203) holds 35 at 1 at its end step 24 (AddSw 35, 24, 24)",
	36: "the cvpmMech mCycle (lines 196-203) holds 36 at 1 at step 0 (AddSw 36, 0, 0), where mCycle.Start leaves the lift",
	37: "sw37_Hit pulses 37 when Status is 0 (lines 316-317); Status is declared and never assigned, so every pass pulses it",
	41: "cvpmBallStack bsCycle (InitSw 0, 44, 43, 42, 41; lines 162-163) holds 41 at 1 while a fourth ball is stacked",
	42: "cvpmBallStack bsCycle (lines 162-163) holds 42 at 1 while a third ball is stacked",
	43: "cvpmBallStack bsCycle (lines 162-163) holds 43 at 1 while a second ball is stacked",
	44: "cvpmBallStack bsCycle (lines 162-163) holds 44 at 1 while a ball waits at the kicker Kicker1, which Q5 empties",
	45: "cvpmBallStack bsSVUK (InitSw 0, 45; InitKick sw45a; lines 176-177) holds 45 while a ball waits in the super VUK",
	46: "cvpmBallStack bsScoop (InitSw 0, 46; InitKick sw46; lines 167-168) holds 46 while a ball waits in the scoop",
	48: "Trigger sw48 holds 48 while the ball sits on it (lines 275-276)",
	49: "Bumper2b's Hit handler pulses 49 (line 297)",
	50: "Bumper3b's Hit handler pulses 50 (line 298)",
	51: "Bumper1b's Hit handler pulses 51 (line 296)",
	52: "Bumper4b's Hit handler pulses 52 (line 299)",
	53: "the plunger key writes 53 while held (lines 215 and 225)",
	57: "Trigger sw57 holds 57 while the ball sits on it (lines 277-278)",
	58: "Trigger sw58 holds 58 while the ball sits on it (lines 279-280)",
	59: "the left slingshot handler pulses 59 (line 659)",
	60: "Trigger sw60 holds 60 while the ball sits on it (lines 281-282)",
	61: "Trigger sw61 holds 61 while the ball sits on it (lines 283-284)",
	62: "the right slingshot handler pulses 62 (line 640)",
	8: "the left and right MagnaSave keys and the upper flipper keys all write 8 while held (lines 216-219 and 226-229)",
}
# Matrix switches the gameplay harness runs closed, with the outputs the ROM drove in response (step labels in the evidence).
GAMEPLAY_RESPONSE = {
	8: "holding it for 1.5 s raised the up/down post 23, alongside a ball-search pass",
	16: (
		"a ball resting on it drew the auto launch 2 40 ms later and flashed 29 and 32; while the ball stayed, the ROM fired 2 again "
		"2.3 s later and then eight more times about 0.5 s apart, ten kicks in all, and gave up, as the manual's Operator Alert "
		"paragraph describes"
	),
	20: "knocking it down after 17-19 completed the left bank and fired the left reset 6 at once",
	24: "knocking it down after 21-23 completed the right bank and fired the right reset 7 at once",
	25: "closing it once flashed the speedometer flashers 32",
	26: "closing it once ran the shaker 13, flashed the ramp-top flashers 28 and blinked the G.I.",
	27: "closing it once flashed the speedometer flashers 32",
	28: "closing it once ran the shaker 13",
	29: "closing it once ran the shaker 13 and flashed the super-VUK flashers 30",
	30: "closing it once ran the shaker 13 and flashed the super-VUK flashers 30",
	31: "closing it once ran the shaker 13 and flashed the super-VUK flashers 30",
	32: "closing it once ran the shaker 13 and flashed the super-VUK flashers 30",
	34: "closing it once flashed the ramp-left flashers 26",
	44: (
		"a ball held on it for 10 s drew the trough up-kicker 1, the shaker 13 and flashers 29 and 30, and the motor relay 19, "
		"which had been running before the ball arrived, switched off about 3.4 s later; no motorcycle ball launch 5 fired while "
		"the ball stayed, and when it emptied the ROM fired 1 and 2"
	),
	45: "a ball held on it drew repeated super-VUK kicks (3)",
	46: (
		"in the launch-scoop-opto run, with no other switch closed, a ball held on it flashed the scoop flasher 20 three times "
		"and drew the scoop kick 4 about 1.1 s after it arrived, then again every 0.75 s, ten kicks in all, while it stayed; in "
		"the gameplay runs, later in a game, a ball held on it for 6 s flashed 25 and 30 and drew no kick while it stayed"
	),
	48: "closing it once fired no coil and switched the G.I. off for the ROM's video mode; on harl_a30 the game-on state 15 fell about 2 s later",
	49: "closing it once fired the left turbo bumper 9 and the shaker 13",
	50: "closing it once fired the right turbo bumper 10, the shaker 13 and the bumper flashers 27",
	51: "closing it once fired the bottom turbo bumper 11, the shaker 13 and the bumper flashers 27",
	52: "closing it once fired the top turbo bumper 12, the shaker 13 and the bumper flashers 27",
	57: "closing it once flashed the left drop-target flashers 25 and blinked the G.I.",
	58: "closing it once ran the shaker 13 and flashed the ramp-top flashers 28",
	59: "closing it once fired the left slingshot 17, ran the shaker 13 and flashed 25",
	60: "closing it once flashed the right drop-target flashers 31 and blinked the G.I.",
	61: "closing it once ran the shaker 13 and flashed 31",
	62: "closing it once fired the right slingshot 18, ran the shaker 13 and flashed 31",
}
GAMEPLAY_QUIET = (17, 18, 19, 21, 22, 23, 33)


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


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	identifier = switch_id(address)
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
	notes = f"Printed switch-matrix drive column {column + 1}, return row {row + 1}."
	if address in UNUSED_SWITCHES:
		notes += (
			" The Switch Matrix Grid (DR. 4) prints this cell NOT USED, shaded black, with no part number; the page-15 switch table "
			"lists it under 'The following switches are not used: 9 10 38 39 40 47 63 64', the location drawing (DR. 5) marks no "
			"switch with this number, and the retained script never writes it."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE),
			aliases=aliases, normally_closed=False, pulse=False, physical={"notes": notes}, wiring=_switch_wiring(address),
			spatial=not_applicable("unused", MANUAL_SOURCE),
		)
	label, printed, mounting, part, switch_type, availability, roles, pulse = SWITCHES[address]
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": switch_type}
	if re.fullmatch(r"\d{3}-\d{4}-\d{2}", part):
		physical["assembly_part_number" if part.startswith("500-") else "part_number"] = part
	notes += f' The grid prints "{printed}" with mounting class "{mounting}"; the page-15 switch table gives part "{part}"'
	notes += f' and describes it as "{PAGE15_NAMES[address]}".' if address in PAGE15_NAMES and PAGE15_NAMES[address] != printed else "."
	if address in DOTS_SWITCHES:
		notes += " The grid and the page-15 table tag it DOTS (diode on terminal strip)."
	if address in DODB_SWITCHES:
		notes += (
			" The grid and the page-15 table tag it DODB (diode on diode board): the four motorcycle-trough positions are one 4-position "
			"membrane switch on the Kick-Out Trough Assembly 500-6397-00, whose ribbon cable runs to the Diode PC Board 520-5146-00. "
			"The manual's Motorcycle Test counts them 44 (bottom, the first ball in) to 41 (top, the fourth)."
		)
	if address in (59, 62):
		physical["quantity"] = 2
		notes += " Two parallel stack-blade contacts (180-5054-00, two per Slingshot Assembly) share this matrix address."
	if address in (14, 15):
		notes += (
			" The page-15 note: 'Sw. 14 / Sw. 15 have both REC/TRANS on 1 board respectively'; the board table names the Dual OPTO "
			"boards 515-0173-00 and 515-0174-00 '4-Ball Trough over Up-Kicker'. Whitestar's switch_r hands the CPU ~core_getSwCol and the "
			"driver's invSw is zero, so public 1 is the CPU's closed-contact reading. The Trough Up-Kicker Dual OPTO boards theory "
			"(PDF page 107) states the construction: with light on the receiver its output transistor is off and acts as an open "
			"switch; when the beam is blocked it conducts and acts as a closed switch, so the contact rests open."
		)
	if address == 15:
		notes += (
			" In the stacking-opto harness run, with four balls on 11-14, raising 15 to 1 in attract mode, lowering it and raising it "
			"again drew no coil, so the ROM's attract mode does not act on it; no run exercised it during a game."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 16:
		notes += (
			" The part cell 180-5100-01 names a switch type the manual's assembly pages do not show, so the switch type is left "
			"unknown. The Diagnostic Aids page uses '#16 Shooter Lane & #2 Auto Launch' as its example of a coil the CPU activates "
			"about ten times while its switch stays closed. On harl_a30 the game-on state 15 rose when the served ball reached it."
		)
		refs += (RUNTIME_A30_SOURCE,)
	if address in (17, 21):
		notes += (
			" The 4-Bank Drop Target Assembly 500-5799-04 (PDF page 93) carries four 'Leaf-Switches (Drop Target Style)' 180-5104-00 "
			"and the 23-700 reset coil; the drop target bank harness is 500-6372-00-67 (left) or 500-6372-01-67 (right)."
		)
	if address in (25, 26, 27):
		notes += " The right ramp's parts list carries two Micro-Switches (for Wire Gate) 180-5087-00 with gate assemblies 515-6556-04."
	if address == 28:
		notes += " The manual's assembly pages carry no spinner switch drawing, so the switch type is left unknown."
	if address in (35, 36):
		notes += (
			" One of the two Micro-Switches 180-5052-00 on the Lift (Motor) Assembly 500-6396-00-67, whose cam the motor turns. The "
			f"Motorcycle Test page draws the cam with '{'UP Position Sw. 35' if address == 35 else 'DOWN Position Sw. 36'}' and its "
			"display shows the motorcycle's position from 35 and 36. In the harness runs with built-in mechanisms off, the ROM ran the "
			"motor relay 19 at power-up until 36 closed and never ran it when 36 was closed at boot; when the served ball reached the "
			"shooter lane it ran 19 until 35 closed."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 36:
		notes += " The Motorcycle Test page states that the motorcycle returns to the DOWN position on a game reset."
	if address == 37:
		notes += (
			" The page-15 note: 'Sw. 37 has both REC/TRANS on the same board'. The table prints its boards as TRANS 180-5082-00 / REC "
			"180-5083-01, but the board table's second OPTO row, the Long-Hop board pages and the Stop Light Assembly 500-6400-00-67, "
			"whose OPTO Mtng Bracket 515-7026-00 carries the pair, all give 520-5082-00 and 520-5083-01; the 180- prefix is a misprint. "
			"The Long-Hop page's note: 'In this game, this Combo OPTO Board is used as a P/F Detection Switch for the Motorcycle Enter "
			"Trough... PCBs are used for Switch 37, (GRN-BLK, WHT-GRN)'. Public 1 is a blocked beam: the retained script pulses 37 to "
			"1 as the ball passes, and on Whitestar an opto the script treats as active at 1 has a matrix contact that rests open. "
			"The Long-Hop board's theory text says a lit receiver drives the output transistor and makes the switch, but read "
			"against the LM311's pinout its drawn circuit makes the switch when the beam is blocked, like the trough Dual OPTO boards; "
			"normally_closed follows the read path and the script. In the launch-scoop-opto run two 1 pulses, after the ROM had "
			"given up its scoop kicks, drew no coil. In the gameplay runs a 1 pulse three seconds after the scenario had emptied the "
			"scoop, which the ROM had not kicked while the ball stayed, was followed about 20 ms later by a scoop kick (4); the record "
			"claims no coil response for 37 from that one coincidence."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 48:
		notes += (
			" The Ball Under-Trough Assembly 500-6401-00 carries a Micro-Switch (High Form) 180-5057-00 and leads the ball to the "
			"super VUK. PinMAME's simulator for this game routes a ball caught behind the traffic light by the magnet to 'Behind VUK' "
			"(48) and on to the super VUK (45)."
		)
		refs += (SIM_SOURCE,)
	if address in (49, 50, 51, 52):
		notes += (
			" The Turbo Bumper Assembly page lists the stack switch assembly as 180-5015-04 with spoon actuator 545-5610-02, against "
			"the grid's 180-5015-03."
		)
	if address == 49:
		notes += " The page-15 table prints its column and row as '7 4'; the grid and the matrix arithmetic give column 7, row 1."
	if address in (45, 46):
		notes += (
			" The Super VUK Assembly 500-6184-05 carries Micro-Switch 180-5052-00." if address == 45 else
			" The Kick-Big (Power Scoop) Assembly 500-6398-00 carries Micro Switch (High Form) 180-5057-00; the diode note's terminal-strip "
			"decal lists 'Switch 46 Ball Eject (Scoop)'."
		)
	if address in (3, 7):
		notes += " The part cell reads (Future Use): the harness position is wired but no coin switch is fitted by default."
	if address == 2:
		notes += " The cabinet wiring diagram (PDF page 106) labels this input '4th Coin Slot European Use'."
	if address == 1:
		notes += (
			" UK only: the cabinet wiring diagram's boxed note reads 'UK ONLY: 2 Extra Cabinet Buttons for the Post Save™ Feature are "
			"used. The Left Button operates the Left Outlane Ball Deflector. The Right Button operates the Right Outlane Ball Deflector. "
			"Both buttons pushed together operate the Center Up/Down Post.' It draws the LEFT BUTTON as N.O. on GRN-BRN (CN5-P1) and "
			"WHT-BRN (CN7-P9), as the grid does."
		)
	if address == 8:
		notes += (
			" The cabinet wiring diagram's vertical note reads 'USA ONLY: The Extra Right Button is used to operate the Up/Down Center "
			"Post.', and its UK box draws the RIGHT BUTTON as N.O. on GRN-BRN and WHT-GRY (CN7-P1), as the grid does. The page-15 "
			"table: 'Switches for Up/Down Post: ( 8 )'. The cell is shaded light grey on the grid and the location drawing puts 08 "
			"in a grey (cabinet) box right of the shooter lane."
		)
		refs += (RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	if address == 53:
		notes += (
			" The cabinet wiring diagram draws the LAUNCH (FIRE) BUTTON, N.O., on WHT-GRN (CN7 pin 5) and GRN-VIO (CN5-8), with its lamp "
			"'Lamp 47 Launch'. The Motorcycle Test page calls it the 'AUTO LAUNCH' Button (Cabinet Front Right Side) and uses it to "
			"eject the motorcycle trough's balls in that test. In the launch-scoop-opto harness run a press at 51.70 s, with the ball "
			"still on 16 after the ROM's auto-launch retries had stopped, drew no coil."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 55:
		notes += " sega.vbs's swSlamTilt = 55 is the key the VPinMAME Slam Tilt key writes; the cabinet wiring diagram draws it on the coin door."
		refs += (VPM_LIBRARY_SOURCE,)
	if address == 56:
		notes += (
			" sega.vbs's swTilt = 56. The retained script points vpmNudge.TiltSwitch at 14 instead (line 152), a table defect; both "
			"pinned corpus scripts of the later table use 56."
		)
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE, VPX_CORPUS_119_SOURCE, VPX_CORPUS_112_SOURCE)
	if address == 54:
		notes += " sega.vbs's swStartButton = 54 is what the VPinMAME Start key writes. In the gameplay runs a press after three coins started a game and the ROM kicked the trough up-kicker (1)."
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	if address in (4, 5, 6):
		notes += f" sega.vbs maps its coin keys to {'swCoin3 = 4' if address == 4 else 'swCoin1 = 5' if address == 5 else 'swCoin2 = 6'}."
		refs += (VPM_LIBRARY_SOURCE,)
	if address in SWITCH_SCRIPT:
		notes += f" Retained table script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in GAMEPLAY_RESPONSE:
		notes += f" In the harness runs, {GAMEPLAY_RESPONSE[address]}."
		refs += (RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	elif address in GAMEPLAY_QUIET:
		notes += " The gameplay harness runs closed it once in a game and the ROM fired no coil or flasher of its own in response, which says nothing against its fitment."
		refs += (RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	if address == 5:
		notes += " In the gameplay runs each coin on 5 pulsed the optional coin-meter output 24 four times and flashed the bumper flashers 27."
		refs += (RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	extra: dict[str, Any] = {"aliases": aliases, "normally_closed": False, "pulse": pulse, "wiring": _switch_wiring(address)}
	if roles:
		extra["roles"] = list(roles)
	if address in (11, 12, 13, 14, 36):
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
			"The cabinet/coin door wiring diagram (PDF page 106) draws the Memory Protect Switch, N.O., from CPU board CN6 pin 12 "
			"(BLK-RED) to BLK ground. se.c's ram_w refuses writes to the protected RAM while public -3 is 1, and sega.vbs names the "
			"address swMemoryProtect; a closed coin door is public -3 at 1 and an open door 0. The Diagnostic Aids page: opening the "
			"Coin Door after a CMOS RAM failure 'will initiate a Factory Restore (Reset), by opening the Memory Protect Switch'."
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
		side = "right" if address == 81 else "left"
		notes += (
			f" The grid prints its location 'in Cabinet side' like the flipper buttons; the 2-Flipper Circuit Wiring Diagram (PDF page "
			f"104) draws it 'ON ASSY.' as an N.C. switch, and the {side} Flipper Assembly ({'500-6307-00' if address == 81 else '500-6307-10'}) "
			"lists the Power (End of Stroke) Switch 180-5149-00. The diagram explains that the switch opens about 1/16\" when the "
			"flipper is energized and that the CPU applies another 40 ms pulse when it sees the switch close during a hold, because a "
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
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
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
		"switch.88-not-used-ds-5", "Not Used Dedicated Input DS-5", "switch", SWITCH_GROUP, 88, "unused",
		(MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.switch", "value": "88"}, {"namespace": "manual.address", "value": "DS-5"}], normally_closed=False, pulse=False,
		physical={"notes": (
			"dedswitch_r routes the flipper column's upper-flipper button bit to U206 input 5 (DS-5). The dedicated-switch column prints "
			"'#5 NOT USED' in a black cell (GRY-GRN, CN6-P7), and the 2-Flipper Circuit Wiring Diagram draws 'UPPER LT or RT FLIPPER IN "
			"CABINET DEDICATED SWITCH DS-5' in green with a NOT USED tag. The ROM's own wiring table agrees: in the "
			"dedicated-switch-test harness run, harl_a40's Portals Dedicated Switch Test printed '#5 NOT USED / CN6-7 GRY-GRN CN6-1 "
			"BLK' while 88 was held, where the flipper-button controls printed '#1 LEFT FLIPPER BUTTON / CN6-2 GRY-BRN CN6-1 BLK' (84) "
			"and '#3 RIGHT FLIPPER BUTTON / CN6-4 GRY-ORG CN6-1 BLK' (82). Only the cabinet wiring diagram disagrees: it draws an "
			"'UPPER RIGHT FLIPPER BUTTON' on GRY-GRN, CN6 pin 7, its label and wire in red, the colour the page also uses for the "
			"Start and Launch buttons and lamp 47. That page's 'USA ONLY: The Extra Right Button is used to operate the Up/Down Center "
			"Post' is matrix switch 8, not DS-5: the coil table prints 'Switches for Up/Down Post: ( 8 )', and in the ds5-probe "
			"harness run holding 8 for 1.5 s pulsed the up/down post 23 within 0.08 s, while holding 88 for 1.5 s in attract mode, "
			"twice during play and once after that control switched no solenoid on. The record follows the switch table, the flipper "
			"circuit diagram and the ROM's wiring table, which all name DS-5 NOT USED, and keeps the red button as that one page's "
			"disagreement; the driver declares no upper flipper."
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
				f"Position {number} of the eight-position CPU DIP switch SW300 (KSD08H). se.c's dip_r returns the complement of PinMAME DIP "
				"bank 0. The manual's CPU Country Setting charts (DR. 3) set positions 1-5 for nineteen countries (USA all off; New "
				"Zealand, Portugal and Spain use position 5) and never turn 6-8 on. sega.vbs's DIP form covers only mask 0x0f, and three "
				"of its labels (UK 0x05, Japan 0x09, Brazil 0x0d) name other countries than this game's chart (Finland, Denmark, "
				"Australia); the chart is this game's own." if used else
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
Q_OUTPUTS: dict[int, tuple[str, str, str, str, str, str, str, int | None, str, str]] = {
	1: ("Trough Up-Kicker", "TROUGH UP-KICKER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BRN-BLK", "J8-P1"),
	2: ("Auto Launch", "AUTO LAUNCH", "coil", "used", "24-940 / 090-5036-00T", *YV, "BRN-RED", "J8-P3"),
	3: ("Super VUK", "SUPER VUK", "coil", "used", "23-800 / 090-5001-00T", *YV, "BRN-ORG", "J8-P4"),
	4: ("Power Scoop / Kick Big", "POWER SCOOP/KICK BIG", "coil", "used", "23-800 / 090-5001-00T", *YV, "BRN-YEL", "J8-P5"),
	5: ("Motorcycle Ball Launch", "MOTORCYCLE BALL LAUNCH", "coil", "used", "24-940 / 090-5036-00B", *YV, "BRN-GRN", "J8-P6"),
	6: ("Left 4-Bank Drop Target Reset", "LEFT 4-BANK DROP TARGET", "coil", "used", "23-700 / 090-5022-00T", *YV, "BRN-BLU", "J8-P7"),
	7: ("Right 4-Bank Drop Target Reset", "RIGHT 4-BANK DROP TARGET", "coil", "used", "23-700 / 090-5022-00T", *YV, "BRN-VIO", "J8-P8"),
	8: ("European Token Dispenser", "EUROPEAN TOKEN DISPENSER", "coil", "optional", "DL4SS / 515-6076-01", *YV, "BRN-GRY", "J8-P9"),
	9: ("Left Turbo Bumper", "LEFT TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-BRN", "J9-P1"),
	10: ("Right Turbo Bumper", "RIGHT TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-RED", "J9-P2"),
	11: ("Bottom Turbo Bumper", "BOTTOM TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-ORG", "J9-P4"),
	12: ("Top Turbo Bumper", "TOP TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-YEL", "J9-P5"),
	13: ("Shaker Motor", "SHAKER MOTOR", "motor", "used", "Motor Only / 041-5029-01", "RED-WHT", "J17-P7", None, "BLU-GRN", "J9-P6"),
	14: ("Magnet", "MAGNET", "magnet", "used", "22-650 / 090-5042-01", "VIO-YEL", "J10-P3", 50, "BLU-BLK", "J9-P7"),
	15: ("Left Flipper", "LEFT FLIPPER (50v RED/YEL)", "coil", "used", "22-1080 / 090-5032-00T", "RED-YEL / GRY-YEL", "J10-P1/2", 50, "ORG-GRY", "J9-P8"),
	16: ("Right Flipper", "RIGHT FLIPPER (50v RED/YEL)", "coil", "used", "23-1100 / 090-5030-00T", "RED-YEL / BLU-YEL", "J10-P1/2", 50, "ORG-VIO", "J9-P9"),
	17: ("Left Slingshot", "LEFT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "VIO-BRN", "J7-P2"),
	18: ("Right Slingshot", "RIGHT SLINGSHOT", "coil", "used", "23-800 / 090-5001-00T", *BR, "VIO-RED", "J7-P3"),
	19: ("Motor Relay", "MOTOR RELAY", "relay", "used", "Relay Bd. / 520-5010-00", *BR, "VIO-ORG", "J7-P4"),
	20: ("Scoop Flasher", "FLASH: SCOOP X1", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "VIO-YEL", "J7-P6"),
	21: ("Left Outlane Ball Deflector (UK Only)", "LT OUTLANE (UK ONLY)", "coil", "optional", "28-1050 / 090-5046-00", *BR, "VIO-GRN", "J7-P7"),
	22: ("Right Outlane Ball Deflector (UK Only)", "RT OUTLANE (UK ONLY)", "coil", "optional", "28-1050 / 090-5046-00", *BR, "VIO-BLU", "J7-P8"),
	23: ("Up/Down Post (Skill)", "UP/DOWN POST (SKILL)", "coil", "used", "23-1100 / 090-5030-00T", *BR, "VIO-BLK", "J7-P9"),
	24: ("Optional Coin Meter", "OPTIONAL COIN METER", "coil", "optional", "Meter 5v / 091-5000-00", "RED", "J16-P7", 5, "VIO-GRY", "J7-P10"),
	25: ("Left Drop Target Flashers (X2)", "FLASH: LEFT DROP TARGET X2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-BRN", "J6-P1"),
	26: ("Ramp Left Flashers (X2)", "FLASH: RAMP LEFT X2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-RED", "J6-P2"),
	27: ("Turbo Bumper Flashers (X4)", "FLASH: TURBO BUMPER X4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-ORG", "J6-P3"),
	28: ("Ramp Top Flashers (X2)", "FLASH: RAMP TOP X2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-YEL", "J6-P4"),
	29: ("Motorcycle Flashers (X4)", "FLASH: MOTORCYCLE X4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-GRN", "J6-P5"),
	30: ("Super VUK Flashers (X2)", "FLASH: SUPER VUK X2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-BLU", "J6-P6"),
	31: ("Right Drop Target Flashers (X2)", "FLASH: RT. DROP TARGET X2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-VIO", "J6-P7"),
	32: ("Speedometer Flashers (X2)", "FLASH: SPEEDOMETER X2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-GRY", "J6-P8"),
}
PUBLIC_BINDING = {15: 48, 16: 46}
# What the retained table does with each callback (embedded script line numbers).
SOLENOID_SCRIPT = {
	1: "SolCallback(1)=\"bsTrough.SolOut\" (line 18) kicks the trough ball stack out of BallRelease (lines 156-159)",
	2: "SolCallback(2)=\"bsLaunch.SolOut\" (line 19) kicks the shooter-lane saucer Kicker2 (line 172)",
	3: "SolCallback(3)=\"bsSVUK.SolOut\" (line 20) kicks the super-VUK ball stack out of sw45a (lines 176-177)",
	4: "SolCallback(4)=\"bsScoop.SolOut\" (line 21) kicks the scoop ball stack out of sw46 (lines 167-168)",
	5: "SolCallback(5)=\"bsCycle.SolOut\" (line 22) kicks the motorcycle-trough ball stack out of Kicker1 (lines 162-163), whatever the lift's position",
	6: "SolCallback(6)=\"dtL.SolDropUp\" (line 23) raises the left drop targets sw17-sw20",
	7: "SolCallback(7)=\"dtR.SolDropUp\" (line 24) raises the right drop targets sw21-sw24",
	9: "the bumper callback SolCallback(9) is commented out (line 25); Bumper2b is a VPX bumper that fires itself",
	10: "the bumper callback SolCallback(10) is commented out (line 26); Bumper3b is a VPX bumper that fires itself",
	11: "the bumper callback SolCallback(11) is commented out (line 27); Bumper1b is a VPX bumper that fires itself",
	12: "the bumper callback SolCallback(12) is commented out (line 28); Bumper4b is a VPX bumper that fires itself",
	13: "SolCallback(13)=\"SolShake\" (line 29), whose body comments out the shake timer (lines 80-86), so the table shakes nothing",
	14: "'SolCallback(14)=magnet is commented out (line 30); the cvpmMagnet mMagnet (InitMagnet MagTrig, 75; Solenoid = 14; GrabCenter; lines 189-192) follows 14 itself",
	17: "SolCallback(17) is commented out (line 32); LeftSlingShot is a VPX slingshot wall that fires itself",
	18: "SolCallback(18) is commented out (line 33); RightSlingShot is a VPX slingshot wall that fires itself",
	19: (
		"'SolCallback(19)=\"SolCycle\" 'Shake Bike is commented out (line 34); the cvpmMech mCycle (Sol1 = 19, one-solenoid reversing "
		"linear travel over 25 steps; lines 196-203) moves the lift while 19 is on and reverses at each end, and UpdateCycle tilts the "
		"motorcycle primitives P3, Platform and PlatPost and stands Wall40 only at step 0 (lines 320-329)"
	),
	20: "SolCallback(20)=\"SetLamp 120,\" 'Flash Scoop x1 (line 35), but its only fader, NFadeL 120, F120, is commented out (line 486), so it draws nothing",
	23: "SolCallback(23)=\"SolPost\" (line 36) raises Wall32 while energized and drops it on release (lines 95-102); Wall32 starts dropped (line 205)",
	25: "SolCallBack(25)=\"SetLamp 101,\" 'Left drop target X2 (line 37) drives the Flasher objects F101 and F101a (lines 488-489)",
	26: "SolCallBack(26)=\"SetLamp 102,\" 'Ramp Left X2 Flashers (line 38) drives the Lights L102 and L102a and the Flasher F102b (lines 491-494)",
	27: "SolCallBack(27)=\"SetLamp 103,\" 'Turbo Bumper X4 (line 39) drives the Flasher objects F103, F103a and F103b (lines 496-498)",
	28: "SolCallBack(28)=\"SetLamp 104,\" 'Ramp Top X2 Flashers (line 40) drives the Lights L104 and L104a and the Flasher F104b (lines 500-502)",
	29: "SolCallBack(29)=\"SetLamp 105,\" 'Motorcycle X4 (line 41) drives the Flasher objects F105 and F105a-c (lines 504-507)",
	30: "SolCallBack(30)=\"SetLamp 106,\" 'Super VUK X2 (line 42) drives the Flasher objects F106 and F106a and the glow Lights L106c-L106i (lines 509-517)",
	31: "SolCallBack(31)=\"SetLamp 107,\" 'Right Drop Target X2 (line 43) drives the Flasher objects F107 and F107a (lines 519-520)",
	32: "SolCallBack(32)=\"SetLamp 108,\" 'Speedometer X2 (line 44) drives the Flasher objects F108 and F108a (lines 522-523)",
}
# What the harness runs showed for each output (evidence step labels).
SOLENOID_RUNTIME = {
	1: "the ROM fired it on Start, again after the drain, and when a ball was held in the motorcycle trough (44)",
	2: (
		"the ROM fired it 40 ms after the served ball reached the shooter lane (16) and, while the ball stayed, again 2.3 s later and "
		"then eight more times about 0.5 s apart; it also fired when the motorcycle trough's bottom switch 44 emptied, and in each ball-search pass"
	),
	3: "a ball held on the super VUK (45) drew repeated kicks; it also fired in each ball-search pass",
	4: (
		"a ball held in the scoop (46) with no other switch closed drew a kick about 1.1 s after it arrived and then one every 0.75 s, ten "
		"in all; a 6 s hold later in a game drew none; it also fired in each ball-search pass"
	),
	6: "it fired the moment the fourth left drop target (20) went down",
	7: "it fired the moment the fourth right drop target (24) went down",
	9: "it answered the left turbo bumper switch (49) and fired in each ball-search pass",
	10: "it answered the right turbo bumper switch (50) and fired in each ball-search pass",
	11: "it answered the bottom turbo bumper switch (51) and fired in each ball-search pass",
	12: "it answered the top turbo bumper switch (52) and fired in each ball-search pass",
	13: (
		"it ran with most scoring switches (the bumpers, slingshots, spinner, stand-up targets, ramp exit and return lanes), when a "
		"ball was served or held in the motorcycle trough, at the drain and in each ball-search pass"
	),
	14: "its only activity was the ROM's ball search; no run held a ball where the magnet acts",
	17: "it answered the left slingshot switch (59) and fired in each ball-search pass",
	18: "it answered the right slingshot switch (62) and fired in each ball-search pass",
	20: "a ball held in the scoop (46) with no other switch closed flashed it three times before the first scoop kick; no other step drew it",
	23: "holding the right cabinet button (8) for 1.5 s raised it",
	24: "each coin on the center slot (5) pulsed it four times, the coin-meter count",
	25: "it flashed from the left slingshot (59), the left outlane (57) and a ball held in the scoop, and at the drain",
	26: "it flashed from the right orbit (34) and at the drain",
	27: "it flashed with each coin, the right, bottom and top turbo bumpers (50-52) and at the drain",
	28: "it flashed from the right ramp exit (26), the left return lane (58) and at the drain",
	29: "it flashed when a ball was served, when a ball was held in the motorcycle trough (44) and at the drain",
	30: "it flashed from the four stand-up targets (29-32), a ball in the super VUK or the scoop, the motorcycle trough (44) and at the drain",
	31: "it flashed from the right slingshot (62), the right outlane and return lane (60, 61) and at the drain",
	32: "it flashed when a ball was served, from the right ramp enter and mid switches (25, 27) and at the drain",
}
SOLENOID_NOT_SEEN = {
	5: "No harness run fired the motorcycle ball launch: no run had the ROM eject the motorcycle trough.",
}
FLASHER_LOCATIONS = {
	20: "scoop flasher below the centre turbo bumper",
	25: "two at the left drop-target bank",
	26: "two on the left: one at the upper left and one at the left edge level with the scoop",
	27: "four by the turbo bumpers: one at the upper left and three beside the top bumper",
	28: "two on the rear discs at the top of the playfield",
	29: "four around the motorcycle, two on each side",
	30: "two at the super VUK (top right)",
	31: "two down the right ramp's side",
	32: "two at the speedometer insert",
}
FLASHER_QUANTITY = {20: 1, 25: 2, 26: 2, 27: 4, 28: 2, 29: 4, 30: 2, 31: 2, 32: 2}


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
	if kind == "flasher":
		notes += (
			" se.c gives every harl_ set the #89 20v DC bulb model on 20 and 25-32. The chart's note: 'In Test Flash Lamps Menu ... "
			"Flashers tested are all Flash Lamps located between Q1-Q32 (This Game: Q20 & Q25-Q32)'."
		)
	if number in (25, 27, 29, 30, 31, 32):
		notes += (
			" The retained table draws it only with Flasher overlay objects, render helpers that are not bulb sockets, so it is not placed; "
			f"the flash lamp location drawing (DR. 7) draws it {FLASHER_LOCATIONS[number]}."
		)
	if number == 20:
		notes += (
			" The flash lamp location drawing (DR. 7) draws 20 below the centre bumper. The retained table's callback draws nothing, so "
			"it is not placed."
		)
	if number == 2:
		notes += (
			" The Ball Auto Launch Assembly page lists the coil as 090-5036-00B where the chart prints -00T; the chart's number is "
			"recorded. The Diagnostic Aids page's Operator Alert example is '#2 AUTO LAUNCH COIL MALFUNCTION', and it states that "
			"the CPU activates such a coil about ten times while its switch (16) stays closed."
		)
	if number == 3:
		notes += " The Super VUK Assembly 500-6184-05 lists the 23-800 coil and notes that the earlier -04 assembly used a 24-940."
	if number == 4:
		notes += " The Kick-Big (Power Scoop) Assembly 500-6398-00 carries this 23-800 coil and the Power Scoop Weldment Assembly 515-6022-00."
	if number == 5:
		notes += (
			" The Kick-Out Trough Assembly 500-6397-00 carries this 24-940 coil at the low end of the motorcycle trough. The Motorcycle "
			"Test: 'To eject the balls and to test the Motorcycle Ball Launch (Coil Q5), press the \"AUTO LAUNCH\" Button'."
		)
	if number in (6, 7):
		notes += " The 4-Bank Drop Target Assembly 500-5799-04 carries the 23-700 reset coil and four drop targets 545-5048-01."
	if number in (9, 10, 11, 12):
		notes += " The Turbo Bumper Assembly page carries the 26-1200 coil and a red bumper cap 550-5057-02 (Qty. 4)."
	if number == 13:
		physical["location"] = "cabinet (shaker motor)"
		notes += (
			" The power cell prints '16v AC' over '12v DC'; the record keeps the wire and connector and states no single voltage. The "
			"coil location drawing puts 13 in a grey (cabinet) box at the lower left, and the board table lists the Shaker Mtr. Bd. "
			"520-5065-00. IPDB's 2nd- and 3rd-edition pages list a shaker motor."
		)
	if number == 14:
		notes += (
			" The Magnet Assembly 515-6142-01 secures the 22-650 coil (12\" leads) under the playfield; the fuse table lists '3A 250v S.B. "
			"50V DC Magnet (Top Orbit) (VIO-YEL BLK)' under the playfield and 'F20 4A 250v S.B. 50V DC Magnet(s)' on the I/O board, and "
			"the diode note puts the magnet's diode on a solder lug for the magnet fuse. The coil location drawing draws 14 at the top "
			"centre between the two rear discs. PinMAME's simulator for this game uses the magnet to stop a ball behind the traffic light "
			"and send it to 48 and the super VUK."
		)
		refs += (SIM_SOURCE,)
	if number in (15, 16):
		side = "left" if number == 15 else "right"
		power = 47 if number == 15 else 45
		notes += (
			f" Physical Q{number} is removed from public {number}: se.c's se_solenoid_w masks it off and publishes it as the lower-{side} flipper "
			f"power bit {power}, and core.c synthesizes canonical callback {address} from it. Bind this one coil to public {address}, the retained "
			f"table's SolCallback(sL{'L' if number == 15 else 'R'}Flipper); public {power} is its power-phase state, not a second coil. The "
			"2-Flipper Circuit Wiring Diagram describes the drive: a 40 ms pulse on a button closure, then 1 ms every 12 ms while held, from one "
			f"50v supply through a 3A slow-blow fuse under the playfield ({'GRY-YEL' if number == 15 else 'BLU-YEL'}). The left coil is a 22-1080 "
			"with a YEL-GRN wrap and the right a 23-1100 with an ORANGE wrap, on Flipper Assemblies 500-6307-10 (left) and 500-6307-00 (right)."
		)
		refs += (VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	if number in (17, 18):
		notes += " The Slingshot Assembly (Qty. 2) carries the 23-800 coil and two stack-blade switches 180-5054-00."
	if number == 19:
		physical["location"] = "Relay PC Board on the Lift (Motor) Assembly under the playfield"
		notes += (
			" Q19 drives the Relay PC Board 520-5010-00, whose contact runs the lift motor: the Lift (Motor) Assembly 500-6396-00-67 carries "
			"the Motor & Connector Assembly 515-7025-00-67 (motor 'Autotrol 20 RPM 24v AC CCW' 041-5072-02 with a capacitor and a neon "
			"bulb), the Lift Cam Assembly 515-7021-00 and the position switches 35 and 36. The Motorcycle Test: the motor 'is controlled "
			"by a Relay driven by Q19 on the I/O Power Driver Board'; RUN moves the motorcycle to the opposite position and PULSE moves it "
			"one pulse at a time. Technical Brief 49 (October 21, 1999) adds a 50Hz Interface Harness 036-5425-01 with a 68 Ω 2 W "
			"resistor between the motor and game harness connectors, because some motors stuttered on 50 Hz mains. The coil location "
			"drawing draws 19 twice, joined by a line: a white diamond at the upper left and a white box right of the motorcycle trough. "
			"In the harness runs with built-in mechanisms off, the ROM ran it at power-up until 36 closed, and when the served ball "
			"reached the shooter lane until 35 closed; it also ran in each ball-search pass."
		)
		refs += (TECH_BRIEF_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	if number in (21, 22):
		notes += (
			" UK only: the chart row is printed on a dark grey band and the coil location drawing does not draw it. The cabinet wiring "
			f"diagram's UK note: 'The {'Left' if number == 21 else 'Right'} Button operates the {'Left' if number == 21 else 'Right'} "
			"Outlane Ball Deflector.' The UK ONLY OPTIONAL Ball Deflector Assemblies 500-5788-02 (Qty. 2) list a 26-1200 coil "
			"(090-5044-00T), on a Ball Deflector Coil Mounting Bracket 535-6857-02, where the chart "
			"prints 28-1050; the chart's number is recorded. A standard machine fits neither, and the retained US table models neither."
		)
	if number == 23:
		notes += (
			" The Up/Down Post Assembly 500-6293-00 carries the 23-1100 coil; the coil location drawing draws 23 between the flippers. "
			"The cabinet wiring diagram: on USA machines the extra right button (8) operates the up/down centre post; on UK machines "
			"both buttons pushed together do. IPDB's 3rd-edition page: 'The up-post is controlled by both the machine and the player.'"
		)
		refs += (IDENTITY_SOURCE,)
	if number == 8:
		notes += (
			" The row is printed on a light grey band: the European token dispenser is optional equipment, not on a standard machine, and "
			"the retained script registers no callback."
		)
		physical["location"] = "cabinet (token dispenser, when fitted)"
	if number == 24:
		notes += (
			" The cabinet wiring diagram's TO COIN METER box routes Q24 (J7-10, 78 VIO-GRY) and +5VDC (J16-7, 22 RED) to the meter. "
			"No stock playfield device is fitted."
		)
		physical["location"] = "cabinet (coin meter, when fitted)"
	if number in SOLENOID_SCRIPT:
		notes += f" Retained table script: {SOLENOID_SCRIPT[number]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if number in SOLENOID_RUNTIME:
		notes += f" In the harness runs {SOLENOID_RUNTIME[number]}."
		refs += (RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	if number in SOLENOID_NOT_SEEN:
		notes += f" {SOLENOID_NOT_SEEN[number]}"
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Q{number}"}], "wiring": _q_wiring(number)}
	role = "emitter" if kind == "flasher" else "effect"
	if number in (8, 13, 24):
		extra["roles"] = ["cabinet.coin-meter"] if number == 24 else ["cabinet.token-dispenser"] if number == 8 else ["cabinet.shaker"]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
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
		(CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "15"}],
		physical={"notes": (
			"se.c sets public 15 while the ROM's fast-flip byte is non-zero, i.e. while the flippers are enabled in a game; MACHINE_INIT(se) "
			"places that byte at CPU RAM 0x00 for harl_a30 only and sets none for the other fourteen Harley-Davidson sets. sega.vbs declares "
			"GameOnSolenoid = 15. In the harl_a30 gameplay run it rose when the served ball reached the shooter lane, fell about 2 s after "
			"the Behind Top VUK switch 48 started the ROM's video mode, rose again during play and fell at the drain; the harl_a40 runs "
			"never raised it. Physical Q15 is the left flipper at public 48; never wire this state to a transistor."
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
			physical={"notes": "A Whitestar compatibility hole: harlGameData declares no auxiliary board, and nothing in se.c drives it for this driver."},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	for address, side, canonical, number in ((45, "right", 46, 16), (47, "left", 48, 15)):
		items.append(_device(
			f"virtual.{address}-{side}-flipper-power-phase", f"{side.capitalize()} Flipper Power-Phase State", "virtual", SOLENOID_GROUP, address, "used",
			(CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE), aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
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
	1: ("Harley H", "(H) ARLEY", "#555 Bulb"), 2: ("Harley A", "H (A) RLEY", "#555 Bulb"), 3: ("Harley R", "HA (R) LEY", "#555 Bulb"),
	4: ("Harley L", "HAR (L) EY", "#555 Bulb"), 5: ("Harley E", "HARL (E) Y", "#555 Bulb"), 6: ("Harley Y", "HARLE (Y)", "#555 Bulb"),
	7: ("Super Jackpot Red", "SUPER JACK-PO T (RED)", "#44 Bulb"), 8: ("Super Jackpot Green", "SUPER JACK-PO T (GRN)", "#44 Bulb"),
	9: ("Live L", "(L) IVE", "#44 Bulb"), 10: ("Live I", "L (I) VE", "#555 Bulb"), 11: ("Live V", "LI (V) E", "#555 Bulb"),
	12: ("Live E", "LIV (E)", "#555 Bulb"), 13: ("Ride R", "(R) IDE", "#555 Bulb"), 14: ("Ride I", "R (I) DE", "#555 Bulb"),
	15: ("Ride D", "RI (D) E", "#555 Bulb"), 16: ("Ride E", "RID (E)", "#44 Bulb"),
	17: ("Left Orbit Green", "LT ORBIT GRN LIGHT", "#555 Bulb"), 18: ("Left Orbit Yellow", "LT ORBIT YEL LIGHT", "#555 Bulb"),
	19: ("Left Orbit Red", "LT ORBIT RED LIGHT", "#555 Bulb"), 20: ("1st Gear", "1ST GEAR", "#555 Bulb"), 21: ("2nd Gear", "2ND GEAR", "#555 Bulb"),
	22: ("3rd Gear", "3RD GEAR", "#555 Bulb"), 23: ("4th Gear", "4TH GEAR", "#555 Bulb"), 24: ("5th Gear", "5TH GEAR", "#555 Bulb"),
	25: ("Motorcycle Green", "M-CYCLE GRN LIGHT", "#555 Bulb"), 26: ("Motorcycle Yellow", "M-CYCLE YEL LIGHT", "#555 Bulb"),
	27: ("Motorcycle Red", "M-CYCLE RED LIGHT", "#555 Bulb"), 28: ("Left Turbo Bumper", "LEFT TURBO BUMPER", "#555 Bulb"),
	29: ("Right Turbo Bumper", "RT TURBO BUMPER", "#555 Bulb"), 30: ("Bottom Turbo Bumper", "BOT TURBO BUMPER", "#555 Bulb"),
	31: ("Top Turbo Bumper", "TOP TURBO BUMPER", "#555 Bulb"), 32: ("Speedometer (X2)", "SPEEDO- METER X2", "#555 Bulb"),
	33: ("Super VUK Green", "SUPER VUK GRN LIGHT", "#555 Bulb"), 34: ("Super VUK Yellow", "SUPER VUK YEL LIGHT", "#555 Bulb"),
	35: ("Super VUK Red", "SUPER VUK RED LIGHT", "#555 Bulb"), 36: ("Bike Stand-Up Target Left", "BIKE S-U TARGET (LT)", "#555 Bulb"),
	37: ("Bike Stand-Up Target Right", "BIKE S-U TARGET (RT)", "#555 Bulb"), 38: ("Ramp Stand-Up Target Left", "RAMP S-U TARGET (LT)", "#555 Bulb"),
	39: ("Ramp Stand-Up Target Right", "RAMP S-U TARGET (RT)", "#555 Bulb"), 40: ("Slippery When Wet", "SLIPPERY WHEN WET", "#555 Bulb"),
	41: ("Right Ramp Green", "RT RAMP GRN LIGHT", "#555 Bulb"), 42: ("Right Ramp Yellow", "RT RAMP YEL LIGHT", "#555 Bulb"),
	43: ("Right Ramp Red", "RT RAMP RED LIGHT", "#555 Bulb"), 44: ("Patch", "PATCH", "#555 Bulb"), 45: ("Bikers Back", "BIKERS BACK", "#555 Bulb"),
	46: ("Red Light Multiball", "RED LIGHT MULTIBALL", "#555 Bulb"), 47: ("Auto Launch", "AUTO LAUNCH", "#555 Bulb"),
	48: ("Lite Mystery Rider", "LITE MYST- ERY RIDER", "#555 Bulb"),
	49: ("Right Orbit Green", "RT ORBIT GRN LIGHT", "#555 Bulb"), 50: ("Right Orbit Yellow", "RT ORBIT YEL LIGHT", "#555 Bulb"),
	51: ("Right Orbit Red", "RT ORBIT RED LIGHT", "#555 Bulb"),
	57: ("Stop Light Green", "STOP LIGHT GRN LIGHT", "#44 Bulb"), 58: ("Stop Light Yellow", "STOP LIGHT YEL LIGHT", "#44 Bulb"),
	59: ("Stop Light Red", "STOP LIGHT RED LIGHT", "#44 Bulb"),
	65: ("2 Extra Balls Left Outlane", "2 XTRA BALLS LT OUTLANE", "#555 Bulb"), 66: ("Advance Gear Left Return", "ADVANCE GEAR LT RETURN", "#555 Bulb"),
	67: ("Lite Mystery Right Return", "LITE MYSTERY... RT RETURN", "#555 Bulb"), 68: ("2 Extra Balls Right Outlane", "2 XTRA BALLS RT OUTLANE", "#555 Bulb"),
	69: ("Motorcycle Headlight", "M-CYCLE HEADLIGHT", "#555 Bulb"), 70: ("Ride Again (X2)", "RIDE AGAIN X2", "#555 Bulb"),
	71: ("Mystery Rider", "MYSTERY RIDER", "#44 Bulb"), 72: ("Next City", "NEXT CITY", "#44 Bulb"),
}
# Printed NOT USED, but both exercised ROMs switch them during play; nothing available explains what they drive.
UNRESOLVED_LAMPS = (52, 53, 54)
UNUSED_LAMPS = (55, 56, 60, 61, 62, 63, 64) + tuple(range(73, 81))
LAMP_DRIVE = [("YEL-BRN", "J13-P9", "U17"), ("YEL-RED", "J13-P8", "U16"), ("YEL-ORG", "J13-P7", "U15"), ("YEL-BLK", "J13-P6", "U14"), ("YEL-GRN", "J13-P5", "U13"), ("YEL-BLU", "J13-P4", "U12"), ("YEL-VIO", "J13-P3", "U11"), ("YEL-GRY", "J13-P1", "U10")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
BULB_PARTS = {"#555 Bulb": "165-5002-00", "#44 Bulb": "165-5000-44"}
LAMPS_SEEN_A40 = frozenset(range(1, 47)) | frozenset((48, 49, 50, 51, 57, 58, 59, 65, 66, 67, 68, 70, 71, 72))
LAMP_QUANTITY = {32: 2, 70: 2}
LAMP_LOCATIONS = {
	47: "cabinet front right (launch button lamp)",
	57: "stop light (traffic light) assembly at the motorcycle entrance", 58: "stop light (traffic light) assembly at the motorcycle entrance",
	59: "stop light (traffic light) assembly at the motorcycle entrance",
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
	for address in range(1, 81):
		row, column = divmod(address - 1, 8)
		identifier = lamp_id(address)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		notes = f"Printed lamp-matrix row {row + 1}, column {column + 1}."
		if address in UNRESOLVED_LAMPS:
			notes += (
				" The Lamp Matrix Grid (DR. 4) prints this cell NOT USED, black with no bulb line, and the lamp location drawing (DR. 5) "
				"marks no lamp with this number, so the 3rd-edition machine the manual describes fits no bulb here. Yet both exercised "
				"ROMs (harl_a40 and harl_a30) switch 52, 53 and 54 during play: from about 1 s after the served ball reaches the shooter "
				"lane, usually all three at the same instant and in step with lamp effects on 36, 37, 42 and 49, never in attract mode, "
				"while 55 and 56 stay dark. No retained script binds them. Nothing available here explains what that state reaches, so "
				"availability stays unknown. Resolution path: the 1st- or 2nd-edition manual's lamp grid (manual part numbers "
				"780-5067-01 and 780-5067-10, neither retained) or the ROM's Single Lamp test, read on a harness run, would show whether "
				"an earlier edition fitted bulbs here."
			)
			items.append(_device(identifier, f"Unresolved Lamp {address}", "lamp", LAMP_GROUP, address, "unknown",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE, VPX_SCRIPT_SOURCE), status="candidate",
				aliases=aliases, physical={"notes": notes}, wiring=_lamp_wiring(address)))
			continue
		if address in UNUSED_LAMPS:
			notes += " The Lamp Matrix Grid (DR. 4) prints this cell NOT USED, black with no bulb line, and the lamp location drawing marks no lamp with this number."
			refs: tuple[str, ...] = (MANUAL_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
			if address <= 64:
				notes += " No harness run saw the ROM drive it, and the retained script assigns no Light to it."
				refs += (VPX_SCRIPT_SOURCE,)
			else:
				notes += " Row 10's heading is black and reads NOT USED; no harness run drove an address above 72."
			items.append(_device(identifier, f"Not Used Lamp {address}", "lamp", LAMP_GROUP, address, "unused", refs,
				aliases=aliases, physical={"notes": notes}, wiring=_lamp_wiring(address), spatial=not_applicable("unused", MANUAL_SOURCE)))
			continue
		label, printed, bulb = LAMPS[address]
		refs = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
		physical: dict[str, Any] = {"location": LAMP_LOCATIONS.get(address, label), "part_number": BULB_PARTS[bulb]}
		if address in LAMP_QUANTITY:
			physical["quantity"] = LAMP_QUANTITY[address]
		notes += f' The grid prints "{printed}" with the bulb cell "{bulb}".'
		if address in (28, 29, 30, 31):
			notes += (
				" The cell carries the grid's DOTS (diode on terminal strip) tag. The Turbo Bumper Assembly page lists one #555 wedge bulb "
				"165-5002-00 under each red bumper cap."
			)
		if address in (7, 8):
			notes += " The retained table puts L7 and L8 at the same point, one two-colour Super Jackpot insert."
		if address in (57, 58, 59):
			notes += (
				" The Stop Light Assembly 500-6400-00-67 (PDF page 98) carries three #44 bulbs 165-5000-44 in 3-lug sockets with 1N4001 "
				"diodes and the OPTO Mtng Bracket 515-7026-00 that holds switch 37's boards, so the stop light stands at the motorcycle "
				"entrance; the lamp location drawing shows it in a 'Stop Light Front View' inset with 59 at the top and 57 at the bottom. "
				"The retained table draws it with Flasher objects F57-F59, render helpers that are not bulb sockets, so it is not placed."
			)
		if address == 47:
			notes += (
				" The cabinet wiring diagram's LAUNCH (FIRE) BUTTON LAMP: 'Lamp 47 Launch', RED-BLU to J12 pin 6 through a diode and YEL-VIO "
				"to J13 pin 3, the grid's row 6 and column 7. The lamp location drawing puts 47 in a grey (cabinet) box beside the shooter "
				"lane. No harness run saw the ROM light it, and the retained script comments its fader out (line 462)."
			)
		if address == 72:
			notes += (
				" The lamp location drawing draws 72 in a white (above-playfield) box below the centre bumper. The retained table drives "
				"the Flasher objects F72 and F72a ('Scoop LED'; lines 480-481), render helpers that are not bulb sockets, so it is not placed."
			)
		if address == 32:
			notes += " The lamp location drawing marks 32 twice around the speedometer insert; the retained table models one Light, L32."
		if address == 70:
			notes += " The lamp location drawing marks 70 twice, at the two inlane ends above the flipper tips; the retained table fades L70 and L70a (lines 477-478)."
		if address == 69:
			notes += " Only the harl_a30 gameplay run saw the ROM light it; the harl_a40 runs never did, which says nothing against its fitment."
		elif address in LAMPS_SEEN_A40:
			notes += " The harness runs saw both ROMs drive it."
		extra: dict[str, Any] = {"aliases": aliases, "wiring": _lamp_wiring(address)}
		if address == 47:
			extra["roles"] = ["cabinet.launch-button-lamp"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			spatial = located("lamp", address, identifier, "emitter")
			if spatial:
				extra["spatial"] = spatial
				notes += " Retained table script: the lamp fader drives the Light named in the placement (lines 412-481; UseLamps = 0, line 9)."
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
		"One G.I. relay on the I-O Power Driver Board 520-5137-01 (U206 74HCT273 data latch output D0 through R254 1K and the Q200 "
		"2N3904 relay driver, coil on 20v DC with D229 1N4004 across it) switches the 6.3v AC G.I. supply from J14 to the four "
		"separately fused circuits on J15 (General Illumination Circuit Detailed Wiring Diagram, PDF page 101): B, F24, BRN-WHT to "
		"WHT-BRN, Upper Left Playfield, 10 #44; Y, F25, YEL to WHT-YEL, Upr. Rt. & Lwr. Right P/F, 10 #44; G, F26, GRN to WHT-GRN, "
		"Lower Left P/F + Coin Door, 8 #44 plus 2 #555 on the coin door; V, F27, VIO to WHT-VIO, Upper Right Playfield, 10 #44. The "
		"page warns that G.I. bulb quantities may change during production; its bottom-of-playfield drawing marks 38 circuit-lettered "
		"sockets. The quantity 40 is those 38 playfield bulbs plus the two coin-door bulbs. se.c publishes the relay as GI 0, and the "
		"harness runs saw it on in attract mode, blink with each coin, the right ramp exit (26) and the outlanes (57, 60), and switch "
		"off during the video mode the Behind Top VUK switch (48) starts. The retained table does not bind GI 0 (UseGI = 0, line 9; "
		"its PFGI sub, lines 107-117, is bound to no callback), so its GI collection stays lit. That collection holds the 20 Lights "
		"GI_001 to GI_020, each a single socket; each is placed, observed only, as a playfield bulb. They are 20 of the 38 playfield "
		"sockets; the drawing's circuit letters have not been matched to them, so no placement carries a string, and the other 18 "
		"and the two coin-door bulbs are counted but not placed."
	)
	return [_device(
		"gi.relay", "General Illumination Relay", "gi", GI_GROUP, 0, "used", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE),
		aliases=[{"namespace": "pinmame.gi", "value": "0"}],
		physical={"location": "playfield and coin door", "quantity": 40, "part_number": "165-5000-44", "notes": notes},
		wiring={"board": "Whitestar I/O Power Driver board 520-5137-01 G.I. relay", "power_wire": "YEL / YEL-WHT 6.3v AC through F24-F27", "power_connection": "J14/J15", "nominal_voltage_v": 6.3, "voltage_type": "ac"},
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
	run = common + (RUNTIME_SOURCE, RUNTIME_A30_SOURCE)
	s = switch_id
	q = q_output_id
	return [
		_mechanism("trough", "4-ball trough with up-kicker and stacking opto", "kicker", [q(1)], [s(11), s(12), s(13), s(14), s(15)],
			"Four balls (the manual's front page: 'FOUR (4) PINBALLS MUST BE INSTALLED!') rest in the Ball Trough Assembly on micro "
			"switches 11 (left), 12 and 13 and on the VUK opto 14 at the up-kicker; the two Dual OPTO board pairs carry 14 at the bottom "
			"and the stacking opto 15 at the top. Q1 (26-1200) kicks the ball on 14 up past 15 into the shooter lane, and the rest roll "
			"one place toward the up-kicker. Hold each occupied position at 1 and pass the kicked ball through 15 as a short 1 pulse "
			"(beam blocked). In the gameplay runs the ROM fired Q1 on Start and after the drain. The retained table's bsTrough never "
			"writes 15.", run),
		_mechanism("auto-launch", "Shooter lane and auto launch", "kicker", [q(2)], [s(16)],
			"A served ball comes to rest on shooter-lane switch 16, and Q2 (24-940, Ball Auto Launch Assembly with plunger assembly "
			"515-5000-02) fires it up the lane. The cabinet wiring diagram names the cabinet's button 53 the LAUNCH (FIRE) BUTTON, but in "
			"the harness runs the ROM launched without it and a press changed nothing. The ROM fired Q2 40 ms after the ball reached 16 "
			"and, while the ball stayed, again 2.3 s later and eight more times about 0.5 s apart before giving up, which is the "
			"Operator Alert behaviour the manual's Diagnostic Aids page describes. The retained table holds the ball in "
			"the saucer Kicker2 until Q2 fires.", run),
		_mechanism("motorcycle-lift", "Motorcycle lift", "motorized", [q(19)], [s(35), s(36)],
			"The Lift (Motor) Assembly 500-6396-00-67 turns a cam (Lift Cam Assembly 515-7021-00) with an Autotrol 24 V AC motor "
			"(041-5072-02) that the Relay PC Board 520-5010-00 switches from Q19; the Lift Plate & Cycle Assembly 500-6362-01-67 carries "
			"the H-D FLSTF Fat Boy 1:10 motorcycle model and raises it in a 'wheelie' together with the kick-out trough. Micro switch 35 "
			"closes at the top of the cam (UP) and 36 at the bottom (DOWN). Q19 only runs the motor; the ROM stops it when the wanted "
			"position switch closes, so the direction comes from the cam, not from the controller. The manual's Motorcycle Test loads "
			"the trough only with the motorcycle UP and states that it returns DOWN on a game reset. In the harness runs with built-in "
			"mechanisms off, the ROM ran Q19 at power-up until 36 closed (with 35 closed at boot as well as with neither closed; with 36 "
			"closed at boot it never ran), and when the served ball reached the shooter lane it ran Q19 until 35 closed; 35 alone did "
			"not stop the power-up search, and the ball search ran Q19 through any position change. Technical Brief 49 adds a 68 Ω "
			"adapter harness for motors that stutter on 50 Hz mains. The retained table models the lift as a one-solenoid reversing "
			"cvpmMech of 25 steps with 35 at the end step and 36 at step 0, and tilts its motorcycle primitives with it.",
			run + (TECH_BRIEF_SOURCE,), assembly="500-6396-00-67",
			positions=[
				{"id": "mechanism.motorcycle-lift.up", "label": "Up", "sensors": [s(35)], "description": "Motorcycle raised; the kick-out trough can take balls."},
				{"id": "mechanism.motorcycle-lift.down", "label": "Down", "sensors": [s(36)], "description": "Motorcycle lowered; the home position after power-up and a game reset."},
			]),
		_mechanism("kick-out-trough", "Motorcycle kick-out trough", "kicker", [q(5)], [s(37), s(44), s(43), s(42), s(41)],
			"The Kick-Out Trough Assembly 500-6397-00 rides under the motorcycle: a sloped trough over one 4-position membrane switch "
			"181-5001-00, 44 at the bottom (the first ball in) to 41 at the top (the fourth), with its diodes on the Diode PC Board "
			"520-5146-00, and the Q5 24-940 coil at its low end. The motorcycle-enter opto 37 (Long-Hop boards on the Stop Light "
			"Assembly's bracket) sees a ball entering. The Motorcycle Test loads balls by hand with the motorcycle UP and ejects them "
			"with Q5 from the Launch button. PinMAME's simulator for this game lets a ball into the trough only when the lift is at least "
			"half up and otherwise returns it to the playfield. In the gameplay runs a ball held on 44 for 10 s drew the trough up-kicker "
			"Q1 (a new ball), the shaker and flashers 29 and 30, and switched off the motor relay Q19 that had been running, but drew no "
			"Q5; no run fired Q5. The retained table stacks "
			"balls entering Kicker1 in bsCycle and ejects them on Q5 whatever the lift's position.", run + (SIM_SOURCE,), assembly="500-6397-00"),
		_mechanism("super-vuk", "Super VUK and under-trough", "kicker", [q(3)], [s(45), s(48)],
			"The Ball Under-Trough Assembly 500-6401-00 carries a micro switch (48, 'Behind Top VUK (Metal Under-Trough)') and leads "
			"the ball to the Super VUK Assembly 500-6184-05, where it rests on micro switch 45 until Q3 (23-800) kicks it up. In the "
			"gameplay runs a ball held on 45 drew repeated Q3 kicks; a closure of 48 fired no coil and started the ROM's video mode, "
			"with the G.I. off. PinMAME's simulator routes a ball the magnet catches behind the traffic light to 48 and on to 45. The "
			"retained table kicks the ball out of sw45a.", run + (SIM_SOURCE,), assembly="500-6184-05"),
		_mechanism("scoop", "Power scoop (Kick Big)", "kicker", [q(4)], [s(46)],
			"The Kick-Big (Power Scoop) Assembly 500-6398-00 below the bumpers: a ball resting on micro switch 46 is kicked out by Q4 "
			"(23-800) through the Power Scoop Weldment 515-6022-00. In the launch-scoop-opto run a ball held on 46 drew three flashes of "
			"the scoop flasher 20 and the first Q4 kick about 1.1 s after it arrived, then one every 0.75 s, ten in all, while it stayed.",
			run, assembly="500-6398-00"),
		_mechanism("left-drop-bank", "Left 4-bank drop targets (LIVE)", "drop_target_bank", [q(6)], [s(17), s(18), s(19), s(20)],
			"4-Bank Drop Target Assembly 500-5799-04 with four white drop targets on leaf switches 180-5104-00 (17-20, spelling L-I-V-E "
			"from the bottom) and the 23-700 reset coil Q6. A down target holds its switch closed. In the gameplay runs the ROM fired Q6 "
			"the moment the fourth target went down and the bank stood again.", run, assembly="500-5799-04"),
		_mechanism("right-drop-bank", "Right 4-bank drop targets (RIDE)", "drop_target_bank", [q(7)], [s(21), s(22), s(23), s(24)],
			"4-Bank Drop Target Assembly 500-5799-04 with four white drop targets on leaf switches 180-5104-00 (21-24, spelling R-I-D-E "
			"from the top) and the 23-700 reset coil Q7. A down target holds its switch closed. In the gameplay runs the ROM fired Q7 "
			"the moment the fourth target went down and the bank stood again.", run, assembly="500-5799-04"),
		_mechanism("magnet", "Top orbit magnet", "other", [q(14)], [],
			"Magnet Assembly 515-6142-01: a 22-650 coil secured under the playfield at the top centre (the fuse table's 'Magnet (Top "
			"Orbit)'). It has no switch of its own. PinMAME's simulator uses it to stop a ball behind the traffic light and send it to "
			"the Behind Top VUK switch 48 and the super VUK. The retained table models it as a cvpmMagnet around MagTrig that grabs the "
			"ball while 14 is on. No harness run held a ball where it acts.", common + (SIM_SOURCE,), assembly="515-6142-01"),
		_mechanism("up-down-post", "Up/down post between the flippers", "other", [q(23)], [s(8)],
			"Up/Down Post Assembly 500-6293-00 with a 23-1100 coil, between the flippers. On USA machines the extra right cabinet button "
			"(8) asks for it; on UK machines both cabinet buttons pushed together do; the ROM, not a wire, raises it. In the gameplay "
			"runs holding 8 for 1.5 s raised Q23. The retained table raises Wall32 while Q23 is on.", run, assembly="500-6293-00"),
		_mechanism("lower-flippers", "Lower flippers", "other", [q(15), q(16)], ["switch.84-left-flipper-button", "switch.83-left-flipper-end-of-stroke", "switch.82-right-flipper-button", "switch.81-right-flipper-end-of-stroke"],
			"Left (500-6307-10, 22-1080 coil) and right (500-6307-00, 23-1100 coil) flipper assemblies on one 50v supply. The CPU applies "
			"a 40 ms pulse on a button closure and then 1 ms every 12 ms while the button is held; each N.C. end-of-stroke switch opens "
			"at full stroke, and a closure during a hold earns another 40 ms pulse. PinMAME publishes Q15 at 47/48 and Q16 at 45/46.",
			(MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, RUNTIME_A30_SOURCE, VPX_SCRIPT_SOURCE)),
		_mechanism("bumpers", "Four turbo bumpers", "other", [q(9), q(10), q(11), q(12)], [s(49), s(50), s(51), s(52)],
			"Left (Q9/49), right (Q10/50), bottom (Q11/51) and top (Q12/52) turbo bumpers with 26-1200 coils, stack switches and red "
			"caps over #555 bulbs (lamps 28-31); each switch fired its own coil in the gameplay runs.", run),
		_mechanism("slingshots", "Slingshots", "other", [q(17), q(18)], [s(59), s(62)],
			"Left (Q17/59) and right (Q18/62) slingshots with 23-800 coils, two parallel blade contacts per side; each switch fired its "
			"own coil in the gameplay runs.", run),
		_mechanism("uk-post-save", "UK Post Save outlane deflectors", "other", [q(21), q(22)], [s(1), s(8)],
			"UK only: Q21 and Q22 drive the left and right outlane ball deflectors (Ball Deflector Assemblies 500-5788-02, UK only optional). The UK "
			"Post Save buttons ask the ROM for them: the left button (1) the left deflector, the right button (8) the right one, both "
			"together the centre up/down post. A standard machine fits neither deflector.", (MANUAL_SOURCE, CORE_SOURCE)),
		_mechanism("stop-light", "Stop light", "toy", ["lamp.57-stop-light-green", "lamp.58-stop-light-yellow", "lamp.59-stop-light-red"], [s(37)],
			"Stop Light Assembly 500-6400-00-67: a plastic traffic-light housing (515-7030-00) with three #44 bulbs, lamps 59 (red, top), "
			"58 (yellow) and 57 (green, bottom), and the opto bracket that carries the motorcycle-enter opto 37. It has no moving part. "
			"IPDB's 2nd- and 3rd-edition pages list the traffic light among the toys.", (MANUAL_SOURCE, IDENTITY_SOURCE), assembly="500-6400-00-67"),
	]


# --- Drivers -------------------------------------------------------------------------------------------
def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {driver["id"]: driver for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
	if set(by_id) != set(DRIVER_IDS):
		raise RuntimeError(f"Harley-Davidson driver family differs from the catalog: {sorted(set(DRIVER_IDS) ^ set(by_id))}")
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

RENDERER = "; rendered by tools/render_excerpt_image.py with PyMuPDF 1.26.3 and Pillow 12.3.0"
IMAGE_DERIVATIONS = {
	"switch-lamp-locations": (
		f"{MANUAL_NAME} page 7, crop box 0.11,0.02,0.95,0.745, scanned page rendered at its native resolution (tiled scan at consistent "
		"native resolution: embedded image xref 333, 1339px across 3.40in; embedded image xref 6341, 1339px across 3.40in), rendered at "
		"210 dpi, capped to 1500px wide, grayscale, 1501x1676 WebP quality 80" + RENDERER
	),
	"coil-flash-locations": (
		f"{MANUAL_NAME} page 9, crop box 0.11,0.02,0.95,0.745, scanned page rendered at its native resolution (tiled scan at consistent "
		"native resolution: embedded image xref 488, 1339px across 3.40in; embedded image xref 489, 1339px across 3.40in), rendered at "
		"210 dpi, capped to 1500px wide, grayscale, 1501x1676 WebP quality 80" + RENDERER
	),
	"gi-wiring": (
		f"{MANUAL_NAME} page 101, crop box 0.08,0.07,0.99,0.93, born-digital page rendered for legibility (smallest type in region "
		"5.1pt, targeting 11px glyphs), rendered at 157 dpi, grayscale, 1212x1482 WebP quality 80" + RENDERER
	),
	"flipper-circuit": (
		f"{MANUAL_NAME} page 104, crop box 0.05,0.03,0.99,0.97, born-digital page rendered for legibility (smallest type in region "
		"5.0pt, targeting 11px glyphs), rendered at 158 dpi, grayscale, 1266x1639 WebP quality 80" + RENDERER
	),
}


def _excerpt(name: str, locator: str, *, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	record: dict[str, Any] = {"id": f"excerpt.harley-davidson.{name}", "locator": locator, "path": f"evidence/excerpts/{MACHINE_ID}/{name}.md", "sha256": EXCERPT_FILE_HASHES[f"{name}.md"]}
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
		_excerpt("motorcycle-test", "PDF page 2, Harley-Davidson Specific (Motorcycle Test), with its display photographs and the kick-out trough and lift drawings"),
		_excerpt("diagnostic-aids-and-dip-switches", "PDF page 5, printed DR. 3, Diagnostic Aids and CPU DIP Switch Settings (SW300 country charts)"),
		_excerpt("switch-matrix", "PDF page 6 (upper part), printed DR. 4, Switch Matrix Grid and dedicated switches; PDF page 33, printed Section 3, Chapter 2, Page 15 switch table"),
		_excerpt("lamp-matrix", "PDF page 6 (lower part), printed DR. 4, Lamp Matrix Grid"),
		_excerpt("switch-lamp-locations", "PDF page 7, printed DR. 5, switch and lamp matrix grid location drawings"),
		_excerpt("coil-table", "PDF page 8, printed DR. 6, Coils Detailed Chart Table"),
		_excerpt("coil-flash-locations", "PDF page 9, printed DR. 7, coil and flash lamp location drawings"),
		_excerpt("gi-wiring", "PDF page 101, printed Section 5, Chapter 2, Page 85, General Illumination Circuit Detailed Wiring Diagram"),
		_excerpt("flipper-circuit", "PDF page 104, printed Section 5, Chapter 2, Page 88, 2-Flipper Circuit Wiring Diagram"),
		_excerpt("cabinet-wiring", "PDF page 106, printed Section 5, Chapter 3, Page 90, Cabinet / Coin Door Wiring Diagram"),
		_excerpt("opto-boards", "PDF pages 107 and 140 (printed page 124), Trough Up-Kicker Dual OPTO boards and Playfield Switch OPTO Long-Hop boards"),
		_excerpt("firmware-board-tables", "PDF pages 142-143, 145 and 146, Appendices A (firmware), C (production) and D (board types), Harley-Davidson rows"),
		_excerpt("mechanism-assemblies", "PDF pages 82-98 (printed 64-80), major assemblies; PDF page 62 fuse table; PDF page 103 diode note (selected items)", reviewed=False),
	]


def source_records() -> list[dict[str, Any]]:
	runs_a40 = load_json(ROOT / RUNTIME_A40_PATH)["runtime"]["raw_runs"]
	runs_a30 = load_json(ROOT / RUNTIME_A30_PATH)["runtime"]["raw_runs"]

	def describe(raw_runs: list[dict[str, Any]]) -> str:
		return ", ".join(f"{raw['name']} (run.json SHA-256 {raw['sha256'][:12]}..., directory manifest {RUN_MANIFESTS[raw['name']][:12]}...)" for raw in raw_runs)

	ipdb_pages = "; ".join(f"machine {number} page SHA-256 {digest}" for number, digest in IPDB_PAGE_SHA256S.items())
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the harl_a40 clone tree (" + ", ".join(DRIVER_IDS) + ")",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/se/prelim/harley.c harlGameData (GEN_WS, se_dmd128x32, FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), swCol 0, lampCol 2, "
				"custSol 0, harley_handleMech, invSw all zero, start/tilt/slam 54/56/55), init_harl and the fifteen Stern ROM sets on "
				"de_mSES1 (lines 510-590); src/wpc/se.c MACHINE_INIT(se) (fast-flip byte at CPU RAM 0x00 for harl_a30 only), the "
				"fast-flip block publishing public 15, the harl_ PWM bulb model on 20 and 25-32, switch_r (~core_getSwCol), dedswitch_r "
				"(flipper column swapped into U206 order, complemented), dip_r, se_solenoid_w (Q15/Q16 masked off and published at "
				"47/45), the G.I. relay at gi[0], ram_w's memory-protect gate on -3; src/wpc/core.c core_updateSw (no FLIP_EOS: EOS bits untouched)."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": SIM_SOURCE, "kind": "pinmame_sim", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "sha256": SIM_FILE_SHA256,
			"locator": (
				"src/wpc/sims/se/prelim/harley.c: the switch and coil names (lines 127-241), the ball-state table (from line 254), the "
				"magnet routing of a ball behind the traffic light to 'Behind VUK' 48 and the super VUK 45, stMotoEntrance admitting a "
				"ball to the motorcycle trough only when the lift is at least half up (MOTO_UP 50, MOTO_DOWN 0, lines 69-70 and 355-362), "
				"and harley_handleMech, which moves the lift while relay 19 is on and writes 35 and 36 when built-in mechanisms are "
				"enabled. A simulation lead, not physical authority."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/whitestar.json", "revision": "repository",
			"locator": "Whitestar public switch (-3..0, 1-64, 81-88), DIP 1-8, solenoid 1-50, lamp and GI 0 address rules and their notes",
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-30T18:49:00Z",
			"locator": (
				"IPDB machine 4455 'Harley-Davidson® (1st Edition)' (Stern, 1999, model PINBALL-HD, Sega/Stern Whitestar), fetched live "
				"through an authenticated browser session because the site is Cloudflare-gated, with the 2nd-edition page 4664 "
				"(November 2002, PINBALL-HD2, about 600 units), the 3rd-edition page 5277 (PINBALL I-0087) and Sega's page 4453 (model "
				f"67, context only) ({ipdb_pages}). Each page is retained, with a gzip-compressed Wayback Machine capture, under {MANUALS_DIRECTORY}."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-pages", "IPDB machine pages 4455, 4664, 5277 and 4453", reviewed=False)],
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": f"external:{MANUALS_DIRECTORY}/{MANUAL_NAME}", "original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256, "acquired_at": "2026-10-30T18:41:43Z",
			"locator": (
				"Stern Harley-Davidson 3rd Edition Pinball Game Service Manual (160 pages; manual part number 780-5087-00 per its Appendix "
				"C). PDF 2 is the Motorcycle Test, PDF 5-9 the front-matter Dr. Pinball sheets (DR. 3 diagnostic aids and DIP settings, "
				"DR. 4 switch and lamp grids, DR. 5 switch and lamp locations, DR. 6 coil chart, DR. 7 coil and flash locations), PDF 33 "
				"the page-15 switch table, PDF 82-98 the major assemblies (printed pages 64-80, the PDF page less 18), PDF 101-107 the G.I., "
				"flipper, cabinet and trough opto pages, PDF 140 the Long-Hop opto board and PDF 142-146 the appendices. Downloaded from "
				f"IPDB's direct resource {MANUAL_URL} through an authenticated browser session."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Stern Pinball, Inc.; hosted by the Internet Pinball Machine Database",
			"excerpts": _manual_excerpts(),
		},
		{
			"id": TECH_BRIEF_SOURCE, "kind": "service_bulletin", "uri": f"external:{MANUALS_DIRECTORY}/{TECH_BRIEF_NAME}", "original_filename": TECH_BRIEF_NAME,
			"sha256": TECH_BRIEF_SHA256, "acquired_at": "2026-10-30T18:41:41Z",
			"locator": (
				"Stern Technical Brief Nº 49 (Rev.), October 21, 1999, two pages: the Autotrol motor 50Hz Interface Kit (harness "
				f"036-5425-01 with a 68 Ω 2 W resistor). Downloaded from IPDB's direct resource {TECH_BRIEF_URL} through an authenticated browser session."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Stern Pinball, Inc.; hosted by the Internet Pinball Machine Database",
			"excerpts": [_excerpt("tech-brief", "Both pages, from the text layer and a render")],
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "known_working": True,
			"uri": "external:pinmame-vpx-sources/stern/harley-davidson-1999/v1-2/" + quote(TABLE_NAME),
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				"Retained Harley Davidson 1.2 recreation (table description 'VPX Conversion by: Goldchicco & 32assassin'). Exact playfield "
				f"bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. Geometry authority only "
				"for the objects its embedded script binds; the placement seed tools/seeds/stern/harley-davidson-1999-spatial.json lists them."
			),
			"license": "NOASSERTION", "attribution": "Goldchicco and 32assassin (table authors)", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "known_working": True,
			"uri": "external:pinmame-vpx-sources/stern/harley-davidson-1999/v1-2/" + quote("Harley Davidson (Sega 1999) 1.2/script.vbs"),
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256,
			"locator": (
				"The retained table's embedded script as vpxtool extracts it, byte-identical to the retained sidecar .vbs. Runtime authority "
				"for controller callbacks: Const cGameName=\"harl_a30\" with UseLamps=0 and UseGI=0, LoadVPM \"01200000\",\"SEGA.VBS\",3.1, "
				".HandleMechanics=0, the bsTrough/bsCycle/bsScoop/bsSVUK ball stacks, the bsLaunch saucer, the dtL/dtR drop targets, the "
				"mMagnet and mCycle objects, the SolCallback table, the lamp faders and the switch handlers. Known table defects: the "
				"stacking opto 15 is never written, vpmNudge.TiltSwitch names 14 instead of 56, the gate sw25 never clears 25, 27 is never "
				"written, flasher 20 draws nothing, G.I. 0 is not bound, and the EOS inputs 81/83 are never written."
			),
			"license": "NOASSERTION", "attribution": "Goldchicco and 32assassin (table authors)", "rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment line of the embedded script that binds the controller, with its line number", credit=QUOTE_CREDIT)],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/harley-davidson-1999/v1-2/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under the vpxtool extraction "
				f"'{EXTRACTION_RELATIVE_PATH.as_posix()}'; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_CORPUS_119_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_REVISION}/" + quote("Harley Davidson (Sega 1999) v1.19e.vbs", safe="/"),
			"revision": VPXTABLE_REVISION, "sha256": CORPUS_119_SHA256,
			"locator": (
				"Pinned corpus script of a later table of this machine (header 'Harley-Davidson® (1st Edition) / IPD No. 4455', "
				"'Harley Davidson (Sega 1999) NestorGian'), Const cGameName=\"harl_a30\" (line 42). It sets vpmNudge.TiltSwitch=56 "
				"(line 304), binds SolCallback(5) to its own SolBsCycle (line 155), comments out callbacks 14 and 19 (lines 163 and 166) "
				"and writes the stacking opto 15; it corroborates the retained script's bindings without being independent of it."
			),
			"license": "NOASSERTION", "attribution": "Authors credited in Harley Davidson (Sega 1999) v1.19e.vbs and repository contributors",
		},
		{
			"id": VPX_CORPUS_112_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{STANDALONE_REVISION}/" + quote("Harley Davidson (Sega 1999) v1.12/Harley Davidson (Sega 1999) v1.12.vbs", safe="/"),
			"revision": STANDALONE_REVISION, "sha256": CORPUS_112_SHA256,
			"locator": (
				"Pinned corpus script of an earlier release of the same later table, Const cGameName=\"harl_a30\" (line 37): "
				"SolCallback(1)=\"bsTrough.SolOut\" (line 146), SolCallback(5)=\"bsCycle.SolOut\" (line 150), vpmNudge.TiltSwitch=56 "
				"(line 309). The retained SHA-256 is the repository checkout's CRLF materialization; the linked Git blob is the identical "
				f"LF-normalized text (SHA-256 {CORPUS_112_LF_SHA256})."
			),
			"license": "NOASSERTION", "attribution": "Authors credited in Harley Davidson (Sega 1999) v1.12/Harley Davidson (Sega 1999) v1.12.vbs and repository contributors",
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
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/harl_a40.zip", "revision": "4.00", "sha256": ROM_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned harl_a40 ROM set (harcpu.400 CRC 752ed258, hddispa.400 CRC e2c98397); used to identify the ROM the harness booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external",
		},
		{
			"id": ROM_A30_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/harl_a30.zip", "revision": "3.00", "sha256": ROM_A30_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned harl_a30 ROM set (harcpu.300 CRC c4ba9df5, hddispa.300 CRC 61b274f8); used to identify the ROM the harl_a30 harness run booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external",
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_A40_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				f"Nine hash-pinned LibPinMAME harness runs of harl_a40 (library SHA-256 {RUNTIME_LIBRARY_SHA256[:12]}..., built from "
				f"{PINMAME_REVISION[:8]}) from empty NVRAM: {describe(runs_a40)}. The four motorcycle runs have built-in mechanisms off and "
				"write 35 and 36 themselves; the stacking-opto, gameplay, launch-scoop-opto, ds5-probe and dedicated-switch-test runs let PinMAME's motorcycle simulation "
				"write 35 and 36. Scenarios under tools/harness-scenarios/whitestar; tools/harley_davidson_runtime_evidence.py derives the "
				"committed per-step transitions from the retained runs, and the dedicated-switch-test run's Portals frames as diagnostic "
				"snapshots whose readings tools/seeds/stern/harley-davidson-1999-frame-readings.json pins by pixel SHA-256."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": RUNTIME_A30_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_A30_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				f"One hash-pinned LibPinMAME harness run of harl_a30 on the same library from empty NVRAM with PinMAME's motorcycle "
				f"simulation on: {describe(runs_a30)}. Its scenario repeats the harl_a40 gameplay scenario step for step."
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
			"id": MACHINE_ID, "name": "Harley Davidson", "manufacturer": "Stern", "year": 1999, "kind": "physical_pinball", "model_number": "PINBALL-HD",
			"ipdb_id": 4455, "opdb_id": "G56lO-MDXpW",
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
		"knowledge": {"path": "knowledge/stern/harley-davidson-1999.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Harley-Davidson device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		named = mechanism["actuators"] + mechanism["sensors"] + [sensor for position in mechanism.get("positions", []) for sensor in position["sensors"]]
		unknown = [item for item in named if item not in known]
		if unknown:
			raise RuntimeError(f"Harley-Davidson mechanism {mechanism['id']} names unknown devices: {unknown}")
	return definition


# --- Extraction manifest -------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Harley-Davidson retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest", "version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Harley-Davidson extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Harley-Davidson retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Harley-Davidson retained extraction manifest does not match the files under the extraction")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Harley-Davidson retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
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
			"manifest_uri": "external:pinmame-vpx-sources/stern/harley-davidson-1999/v1-2/extracted-vpxtool.manifest.json", "source_ref": VPX_EXTRACTION_SOURCE,
		},
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": (
				"The centre of the VPX object the embedded script binds to each switch (trigger, gate, spinner, hit target, kicker, slingshot "
				"wall, bumper). The trough switches 11-14 and the stacking opto 15, which the table does not model, are projected onto the "
				"release kicker BallRelease; the motorcycle-trough switches 41-44 onto the kicker Kicker1 its ball stack uses; the lift "
				"switches 35 and 36, which a cvpmMech models without objects, onto Kicker1; each end-of-stroke contact onto its flipper."
			),
			"lamp": "The centre of the Light the lamp fader drives for each lamp; lamp 70's two sockets on its two Lights.",
			"solenoid": (
				"The kicker, slingshot wall, bumper, flipper, trigger or wall the script fires; the drop-target resets on the mean of their "
				"bank's four targets; the motor relay on Kicker1 under the motorcycle; for flashers 26 and 28 the script-driven Lights centred "
				"on their modelled dome primitives. The UK-only deflectors 21 and 22, which the US table does not model, are projected onto "
				"the outlane rollovers the cabinet wiring diagram's UK note names."
			),
			"gi": "The 20 Light members of the table's GI collection, each a single socket; observed only, without per-string assignment.",
		},
		"unresolved_geometry": [
			"The trough switches 11-15, the motorcycle-trough switches 41-44 and the lift switches 35 and 36 are not modelled by the table; their placements are projections onto mechanism objects.",
			"Switch 27 (right ramp mid) has no bound table object; the table's unbound wire gate Trigger27q on the ramp near the top centre is a candidate, not used.",
			"The stop light lamps 57-59, the Next City lamp 72 and the flashers 20, 25, 27 and 29-32 are drawn by the table only with Flasher overlay objects or not at all; they need the factory drawings (DR. 5 and DR. 7) or playfield photographs to place.",
			"The UK-only deflectors 21 and 22 are projections onto US-table objects.",
			"No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.",
			"The table models 20 G.I. sockets against the 38 playfield sockets the G.I. page draws; matching them to the circuit-lettered sockets of its mirrored bottom-view drawing is not done.",
		],
		"promotion_decision": "partial: devices without placements, projections, and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Harley-Davidson (Stern, 1999) spatial blockers", "",
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
		raise RuntimeError(f"Refusing to overwrite an author-ready Harley-Davidson artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Harley-Davidson author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"Harley-Davidson deterministic artifact drift: {path}")
	print("Harley-Davidson definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"Harley-Davidson extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Harley-Davidson retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
