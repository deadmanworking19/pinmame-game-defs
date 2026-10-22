"""Curate the physical Williams Terminator 2 machine definition.

The semantic builder is intentionally side-effect free.  The spatial curator
owns the canonical output so a later semantic regeneration cannot erase the
reviewed table geometry.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-alpha"
MANUAL_SOURCE = "manual.williams.terminator-2-judgment-day.1991"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.terminator-2-judgment-day.1991"
VPX_TABLE_SOURCE = "vpx-table.t2-vpw-0022"
VPX_SCRIPT_SOURCE = "vpx-script.t2-vpw-0022"
VPX_EXTRACTION_SOURCE = "vpx-extraction.t2-vpw-0022"
NFOZZY_TABLE_SOURCE = "vpx-table.t2-nfozzy-1-12a"
NFOZZY_EXTRACTION_SOURCE = "vpx-extraction.t2-nfozzy-1-12a"
G5K_SCRIPT_SOURCE = "vpx-script.t2-g5k-v1-1a"
MODERN_SCRIPT_SOURCE = "vpx-script.t2-modern-comparison"
ROM_SOURCE = "rom.t2-l8-authorized-corpus"
RUNTIME_SOURCE = "runtime.terminator-2.t2-l8.solenoid-flasher-tests"
RUNTIME_GI_SOURCE = "runtime.terminator-2.t2-l8.gi-test"
CALLOUT_SOURCE = "drawing-callouts.terminator-2.2026-10-22"
RUNTIME_PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
RUNTIME_GI_PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"

TABLE_SHA256 = "3727bf57102fceb13b9f8e6370bd7bc4fbd2571d95affb7bff34eb7c5f2e9f8c"
SCRIPT_SHA256 = "b5153ac46f6d4b58afb676c1f7bfdff17c6ffb953941daed8dd841c679f4e831"
EXTRACTION_MANIFEST_SHA256 = "f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9"
NFOZZY_TABLE_SHA256 = "2bae1ce5cf8c17233b5d4679032d6aa8c81e31ed32b2219a9363ad8cba244ded"
NFOZZY_SCRIPT_SHA256 = "89547dd4b1bf41314e99237868e30bc7fe5b1c5ce3f66c1f7c2fce6b5a1b7a53"
NFOZZY_MANIFEST_SHA256 = "ce5765a02329975e00b0e52d9bba1be86eea49f01def99c62221b8621a902213"
MANUAL_SHA256 = "8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b"
ROM_SHA256 = "4cdd95d435334c3bd6fe19556b410b558e67266b30e7fb767f52f4d14ed525b1"

EXTRACTION_RELATIVE_PATH = Path("williams/terminator-2-judgment-day-1991/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 548
EXTRACTION_TOTAL_BYTES = 132477924
NFOZZY_EXTRACTION_RELATIVE_PATH = Path("williams/terminator-2-judgment-day-1991/nfozzy-1-12a/extracted-vpxtool")
NFOZZY_MANIFEST_RELATIVE_PATH = Path("williams/terminator-2-judgment-day-1991/nfozzy-1-12a/extracted-vpxtool.manifest.json")
NFOZZY_FILE_COUNT = 938
NFOZZY_TOTAL_BYTES = 53404733

DRIVER_IDS = (
	"t2_d2", "t2_d3", "t2_d4", "t2_d6", "t2_d8", "t2_l2", "t2_l2sp1",
	"t2_l3", "t2_l4", "t2_l6", "t2_l8", "t2_l81", "t2_l82", "t2_l83",
	"t2_l84", "t2_p2f", "t2_p2g", "t2_f19", "t2_f20", "t2_f32",
)

MATRIX_LABELS = {
	11: "Right Flipper", 12: "Left Flipper", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Trough Left", 16: "Trough Center", 17: "Trough Right", 18: "Outhole",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Ticket Dispenser", 24: "Test Position Always Closed",
	25: "Left Outlane", 26: "Left Return Lane", 27: "Right Return Lane", 28: "Right Outlane",
	31: "Gun Loaded", 32: "Gun Mark", 33: "Gun Home", 34: "Grip Trigger",
	36: "Mid Left Standup Target", 37: "Mid Center Standup Target", 38: "Mid Right Standup Target",
	41: "Left Jet", 42: "Right Jet", 43: "Bottom Jet", 44: "Left Sling", 45: "Right Sling",
	46: "Top Right Standup Target", 47: "Mid Right Standup Target", 48: "Bottom Right Standup Target",
	51: "Left Lock", 53: "Low Escape Route", 54: "High Escape Route", 55: "Top Lock",
	56: "Top Lane Left", 57: "Top Lane Center", 58: "Top Lane Right",
	61: "Left Ramp Entry", 62: "Left Ramp Made", 63: "Right Ramp Entry", 64: "Right Ramp Made",
	65: "Low Chase Loop", 66: "High Chase Loop", 71: "Target 1 High", 72: "Target 2",
	73: "Target 3", 74: "Target 4", 75: "Target 5 Low", 76: "Ball Popper",
	77: "Drop Target", 78: "Shooter",
}
MATRIX_PULSES = {11, 12, 13, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 61, 63, 71, 72, 73, 74, 75}
# The retained VPW script pulses 42 from Bumper2 and 43 from Bumper3, but both factory location drawings put the Right Jet
# (switch 42, coil 14) on the right-hand bumper, Bumper3, and the Bottom Jet (43, coil 15) on the lowest one, Bumper2.
JET_BINDING_NOTE = (
	"The retained VPW script pulses switch 42 from its Bumper2 object and switch 43 from Bumper3. Both factory location drawings "
	"(switch callouts 41-43 printed inside the bumper caps on 2-37, coil balloons 13-15 on 2-39) put the Right Jet, switch 42 and "
	"coil 14, on the right-hand bumper (Bumper3) and the Bottom Jet, switch 43 and coil 15, on the lowest bumper (Bumper2); the "
	"table swaps the two bindings, which changes nothing it scores. The placement follows the drawings."
)

LAMP_LABELS = {
	11: "Multiplier 2x", 12: "Multiplier 4x", 13: "Hold Bonus", 14: "Multiplier 6x", 15: "Multiplier 8x", 16: "Shoot Again", 17: "Mouth", 18: "Not Used",
	21: "Kickback", 22: "Special", 23: "Left Return Lane", 24: "Right Return Lane", 25: "Data Base 3", 26: "Load Gun", 27: "Extra Ball", 28: "Load for Jackpot",
	31: "Target 1 High", 32: "Target 2", 33: "Target 3", 34: "Target 4", 35: "Target 5 Low", 36: "Middle Target Bank Left", 37: "Middle Target Bank Center", 38: "Middle Target Bank Right",
	41: "Lock Two", 42: "Data Base 2", 43: "10 Million", 44: "Extra Ball", 45: "Multi-ball", 46: "Light Hurry Up", 47: "Hold Bonus", 48: "Security Pass",
	51: "Eyes Lower", 52: "Eyes Upper", 53: "5 Million", 54: "3 Million", 55: "1 Million", 56: "750 Thousand", 57: "500 Thousand", 58: "250 Thousand",
	61: "Left CPU Lit", 62: "Left Vault Key", 63: "Left Silent Alarm", 64: "Left Passcode", 65: "Left Checkpoint", 66: "Lock 1", 67: "Data Base 1", 68: "Left Ramp",
	71: "Right CPU Lit", 72: "Right Vault Key", 73: "Right Silent Alarm", 74: "Right Passcode", 75: "Right Checkpoint", 76: "Right Bank Top", 77: "Right Bank Middle", 78: "Right Bank Bottom",
	81: "Chase Values", 82: "Right Ramp", 83: "Hurry Up", 84: "Start Button", 85: "Drop Target", 86: "Top Lane Left", 87: "Top Lane Center", 88: "Top Lane Right",
}

SOLENOID_LABELS = {
	1: "Ball Popper", 2: "Gun Kicker", 3: "Outhole", 4: "Trough", 5: "Right Sling", 6: "Left Sling", 7: "Knocker", 8: "Kickback", 9: "Plunger", 10: "Top Lock", 11: "Gun Motor", 12: "Knock Down", 13: "Left Jet", 14: "Right Jet", 15: "Bottom Jet", 16: "Left Lock",
	17: "Hot Dog Flashlamps", 18: "Right Sling Flashlamps", 19: "Left Sling Flashlamps", 20: "Left Lock Flashlamps", 21: "Gun Flashlamps", 22: "Right Ramp Flashlamps", 23: "Left Ramp Flashlamps", 24: "Backglass Flashlamp", 25: "Targets Flashlamps", 26: "Left Popper Flashlamps", 27: "Right Popper Flashlamps", 28: "Drop Target",
}

SOLENOID_SCRIPT_CALLBACKS = {
	1: "SolSkull (retained script callback; opens the skull/ball-popper path from switch 76)", 2: "SolFireGun", 3: "bsTrough.SolIn (outhole)", 4: "bsTrough.SolOut (ball release)", 7: "Knocker sound callback", 8: "SolAPlunger (fires Plunger1, the left outer-lane kicker saver)", 9: "SolShooter (bsShooter.SolOut, the shooter-lane saucer at switch 78)", 10: "SolTopPopper", 11: "MECHGUN motor", 16: "SolLeftPopper", 28: "dtDrop1.SolDropUp",
}

SOLENOID_WIRING = {
	1: ("Vio-Brn", "J130-1", "Q82", "AE-23-800"), 2: ("Vio-Red", "J130-2", "Q80", "AE-24-900"), 3: ("Vio-Orn", "J130-4", "Q78", "AE-27-1200"), 4: ("Vio-Yel", "J130-5", "Q76", "AE-26-1200"),
	5: ("Vio-Grn", "J130-6", "Q64", "AE-26-1500"), 6: ("Vio-Blu", "J130-7", "Q66", "AE-26-1500"), 7: ("Vio-Blk", "J130-8", "Q68", "AE-23-800"), 8: ("Vio-Gry", "J130-9", "Q70", "AE-23-800"),
	9: ("Brn-Blk", "J127-1", "Q58", "AE-23-800"), 10: ("Brn-Red", "J127-3", "Q56", "AE-26-1500"), 11: ("Brn-Orn", "J127-4", "Q54", "14-7963"), 12: ("Brn-Yel", "J127-5", "Q52", "SM1-26-600"),
	13: ("Brn-Grn", "J127-6", "Q50", "AE-26-1200"), 14: ("Brn-Blu", "J127-7", "Q48", "AE-26-1200"), 15: ("Brn-Vio", "J127-8", "Q46", "AE-26-1200"), 16: ("Brn-Gry", "J127-9", "Q44", "AE-26-1500"),
	17: ("Blk-Brn", "J126-1", "Q42", "#906 (4 PL)"), 18: ("Blk-Red", "J126-2", "Q40", "#906 (1 BB), #89 (1 PL)"), 19: ("Blk-Orn", "J126-3", "Q38", "#906 (1 BB), #89 (1 PL)"), 20: ("Blk-Yel", "J126-4 + J125-2", "Q36", "#906 (1 BB), #89 (1 PL)"),
	21: ("Blu-Grn", "J126-5 + J125-3", "Q28", "#89 (2 PL)"), 22: ("Blu-Blk", "J126-6 + J125-5", "Q30", "#906 (1 BB), #89 (1 PL)"), 23: ("Blu-Vio", "J126-7", "Q34", "#906 (1 BB), #89 (1 PL)"), 24: ("Blu-Gry", "J125-7", "Q32", "#906 (1 BB)"),
	25: ("Blu-Brn", "J122-1 + J125-8", "Q26", "#89 (2 PL)"), 26: ("Blu-Red", "J122-2 + J125-9", "Q24", "#89 (2 PL)"), 27: ("Blu-Orn", "J122-3", "Q22", "#89 (2 PL)"), 28: ("Blu-Yel", "J122-4", "Q20", "AE-26-1200"),
}
# Printed bulbs per flashlamp output (PL playfield, BB backbox) from the 1-28 and 2-38 solenoid tables.
FLASHER_QUANTITY = {17: 4, 18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 1, 25: 2, 26: 2, 27: 2}
# The 2-38 copy prints the J125 insert pins half a row lower than the 1-28 copy and the 3-8 interboard table do.
J125_OFFSET_NOTE = (
	"The 2-38 copy of the solenoid table prints its six J125 insert pins between rows, half a row lower than the 1-28 copy and "
	"the 3-8 interboard wiring table, beside the six rows with a backbox bulb (18-20 and 22-24); the 1-28 copy and the 3-8 table "
	"agree on J125-2 for 20, J125-3 for 21, J125-5 for 22, J125-7 for 24, J125-8 for 25 and J125-9 for 26, and the wiring follows "
	"them. A wiring-detail disagreement only: the device, its public address and its fitment are not in doubt."
)

# Public GI address -> (ROM T.6 name, 2-39 list name, ROM wire print, return wire, return connection, triac).
GI_STRINGS = {
	0: ("TOP INSERT", "Top Insert String", "WHT-BRN BRN", "Wht-Brn", "J120-7", "Q18"),
	1: ("BOTTOM INSERT", "Bottom Insert String", "WHT-ORN ORN", "Wht-Orn", "J120-8", "Q10"),
	2: ("RIGHT PLAYFIELD", "Right Playfield String", "WHT-YEL YEL", "Wht-Yel", "J121-9", "Q14"),
	3: ("CPU STRING", "CPU String", "WHT-GRN GRN", "Wht-Grn", "J121-10", "Q16"),
	4: ("LEFT PLAYFIELD", "Left Playfield String", "WHT-VIO VIO", "Wht-Vio", "J121-11 + J119-1", "Q12"),
}
GI_TABLE_PRINT = {
	0: "01 Top Insert G.I., Wht-Brn, J120-7, Q18, #555",
	1: "02 Left Playfield G.I., Wht-Vio, J119-1, Q10, #555",
	2: "03 Right Playfield G.I., Wht-Yel, J121-9, Q14, #555",
	3: "04 Not Used, Wht-Orn, J120-8, Q16, blank bulb",
	4: "05 Bottom Insert G.I., Wht-Grn, J120-10, Q12, #555",
}
GI_TABLE_NOTE = (
	"The ROM's T.6 GEN'L. ILLUM. test names the five public strings in the order of the 2-39 Solenoid Locations list (01 Top "
	"Insert, 02 Bottom Insert, 03 Right Playfield, 04 CPU String, 05 Left Playfield) and prints the board-standard wire pairs, "
	"brown, orange, yellow, green and violet for strings 1 to 5. The 1-28 and 2-38 solenoid tables keep the board's triacs in that "
	"string order (Q18, Q10, Q14, Q16, Q12) but print their names and return wires as 02 Left Playfield Wht-Vio, 04 Not Used "
	"Wht-Orn and 05 Bottom Insert Wht-Grn, and the 3-9 interboard table numbers its feeds in yet another order; owner repair "
	"reports agree with the ROM (the violet string lights the whole left side of the playfield and the coin-door lamps, the green "
	"string the CPU inserts). The definition follows the ROM, the 2-39 list and the 3-9 routing; each table's own row is "
	"transcribed in its excerpt."
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"T2 retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained T2 extraction")
		return None
	return Path(value).expanduser().resolve()


def _verify_manifest(source_root: Path, extraction: Path, manifest: Path, identity: tuple[int, int, str]) -> dict[str, Any]:
	extraction_root = source_root / extraction
	manifest_path = source_root / manifest
	if not manifest_path.is_file():
		raise RuntimeError(f"T2 retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"T2 retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != identity:
		raise RuntimeError(
			"T2 retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	return _verify_manifest(source_root, EXTRACTION_RELATIVE_PATH, EXTRACTION_MANIFEST_RELATIVE_PATH, (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256))


def verify_nfozzy_manifest(source_root: Path) -> dict[str, Any]:
	return _verify_manifest(source_root, NFOZZY_EXTRACTION_RELATIVE_PATH, NFOZZY_MANIFEST_RELATIVE_PATH, (NFOZZY_FILE_COUNT, NFOZZY_TOTAL_BYTES, NFOZZY_MANIFEST_SHA256))


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	verify_extraction_manifest(source_root)
	return manifest_path


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(refs)}


def aliases(namespace: str, address: int, *extra: str) -> list[dict[str, str]]:
	return [{"namespace": namespace, "value": str(address)}, *({"namespace": "manual.address", "value": value} for value in extra)]


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


EXCERPT_ROOT = "evidence/excerpts/williams.terminator-2-judgment-day.1991"
EXCERPT_RECORDS = (
	("excerpt.t2.switch-matrix", "PDF page 46, printed page 1-26, Switch Matrix wiring table", "switch-matrix.md", "9c81830621e03aa9e7e943879ca0aca219e74d9c7dea6f3675a20c2f42c3cd5d", "switch-matrix.webp", "8304c477a8f4eacf1aba998a4fe92ac7a77b0bc83f9ae1fc8cad674ca4686875", "Terminator 2 Judgement Day Operations Manual.pdf page 46, crop box 0.15,0.09,0.88,0.48, scanned page rendered at its native resolution (embedded image xref 405, 2551px across 8.26in), rendered at 166 dpi, capped to 1000px wide, grayscale, 1001x757 WebP quality 75"),
	("excerpt.t2.solenoid-table-01-08", "PDF page 48, printed page 1-28, Solenoid Table rows 1-8", "solenoid-and-gi-table.md", "2e50c90430e49c2c7e183478abf7bee1e1a3a0869deda29c2e0383fdeaa90e91", "solenoid-table-01-08.webp", "e45beaccfecb8c8bafaad73e2c8c3a1d2bc23c3c1ab505580caf7a40a81ec769", "Terminator 2 Judgement Day Operations Manual.pdf page 48, crop box 0.13,0.11,0.9,0.35, scanned page rendered at its native resolution (embedded image xref 423, 2551px across 8.26in), rendered at 157 dpi, capped to 1000px wide, grayscale, 1001x442 WebP quality 75"),
	("excerpt.t2.solenoid-table-09-16", "PDF page 48, printed page 1-28, Solenoid Table rows 9-16", "solenoid-and-gi-table.md", "2e50c90430e49c2c7e183478abf7bee1e1a3a0869deda29c2e0383fdeaa90e91", "solenoid-table-09-16.webp", "fbd2d495b2b46bd483309e38e09428466b5f99f2be8633d91f8a7bc01884abc8", "Terminator 2 Judgement Day Operations Manual.pdf page 48, crop box 0.13,0.33,0.9,0.47, scanned page rendered at its native resolution (embedded image xref 423, 2551px across 8.26in), rendered at 157 dpi, capped to 1000px wide, grayscale, 1001x258 WebP quality 75"),
	("excerpt.t2.solenoid-table-flashers-gi", "PDF page 48, printed page 1-28, Solenoid Table rows 17-28, GI, and lower flippers", "solenoid-and-gi-table.md", "2e50c90430e49c2c7e183478abf7bee1e1a3a0869deda29c2e0383fdeaa90e91", "solenoid-table-flashers-gi.webp", "fc62aae625f1ba34e5087f9437b3c35909f9b186d22a94901e7cb2698a33160c", "Terminator 2 Judgement Day Operations Manual.pdf page 48, crop box 0.13,0.42,0.9,0.76, scanned page rendered at its native resolution (embedded image xref 423, 2551px across 8.26in), rendered at 157 dpi, capped to 1000px wide, grayscale, 1001x626 WebP quality 75"),
	("excerpt.t2.lamp-matrix", "PDF page 53, printed page 1-33, Lamp Matrix table and circuit header", "lamp-matrix.md", "c05984d0ba65fac031f076261701d80b02880b137147a6a799a344b220869b7c", "lamp-matrix.webp", "1748b20212ac4eb29f52df64b1d04474301d16b6957d61edb9cf35841a045e20", "Terminator 2 Judgement Day Operations Manual.pdf page 53, crop box 0.2,0.09,0.84,0.73, scanned page rendered at its native resolution (embedded image xref 468, 2551px across 8.26in), rendered at 151 dpi, capped to 800px wide, grayscale, 800x1133 WebP quality 75"),
	("excerpt.t2.lamp-schematic", "PDF page 100, printed page 2-34, lamp matrix schematic J137 column and J133 row connector labels", "lamp-schematic.md", "0739f55100d6aa1e03844e594d426ad8c3d2ba2a9c0f5303a9d2a93b9a8cbf92", "lamp-schematic.webp", "1faee311290e94dc4250eaaae3a34fc5426fa33ca71a0109b4226fad580a55be", "Terminator 2 Judgement Day Operations Manual.pdf page 100, crop box 0.2,0.075,0.68,0.415, scanned page rendered at its native resolution (embedded image xref 891, 2551px across 8.26in), rendered at 252 dpi, capped to 1000px wide, grayscale, 1001x1003 WebP quality 80"),
	("excerpt.t2.major-mechanisms-map", "PDF page 70, printed page 2-4, Locations Diagram - Game Major Mechanisms", "major-mechanisms-map.md", "bbdc51d23a9e5143a37be92319f566f5792ab741f133eac907de834fa6ec566e", "major-mechanisms-map.webp", "2c0c0a9434ee7cdc0414ed66fe40a7e7d79b460fad7e1be7eb95f9bd5035999a", "Terminator 2 Judgement Day Operations Manual.pdf page 70, crop box 0.05,0.03,0.92,0.84, scanned page rendered at its native resolution (embedded image xref 621, 2551px across 8.26in), rendered at 139 dpi, capped to 1000px wide, grayscale, 1001x1319 WebP quality 70"),
	("excerpt.t2.cannon-platform-assembly", "PDF page 90, printed page 2-24, A-14504 Platform Gun Assembly", "cannon-platform-assembly.md", "b20bc68978416c288342b9215e367c30a1c922fb66082eaefc785abc510bfa50", "cannon-platform-assembly.webp", "681630fcd4d00357057db4bffa645919217d5ee154968f4e05a465a327f4e5f7", "Terminator 2 Judgement Day Operations Manual.pdf page 90, crop box 0.05,0.07,0.95,0.93, scanned page rendered at its native resolution (embedded image xref 801, 2551px across 8.26in), rendered at 121 dpi, capped to 900px wide, grayscale, rotated 270 degrees counter-clockwise, 1218x900 WebP quality 70"),
	("excerpt.t2.lamp-board-legend", "PDF page 70, printed page 2-4, Lamp Boards legend A-K below the major-mechanisms map", "lamp-board-legend.md", None, "lamp-board-legend.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 70, crop box 0.12,0.775,0.92,0.95, scanned page rendered at its native resolution (embedded image xref 621, 2551px across 8.26in), rendered at 309 dpi, grayscale, 2041x633 WebP quality 80"),
	("excerpt.t2.drop-target-assembly", "PDF page 89, printed page 2-23, A-14615 1-Bank Drop Target Assembly drawing and parts list", "drop-target-assembly.md", None, "drop-target-assembly.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 89, crop box 0.02,0.04,0.98,0.94, scanned page rendered at its native resolution (embedded image xref 792, 2551px across 8.26in), rendered at 126 dpi, capped to 1000px wide, grayscale, 1001x1328 WebP quality 80"),
	("excerpt.t2.lamp-locations", "PDF page 101, printed page 2-35, Lamp Locations drawing", "lamp-locations.md", None, "lamp-locations.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 101, crop box 0.5,0.08,0.9,0.72, scanned page rendered at its native resolution (embedded image xref 900, 2551px across 8.26in), rendered at 309 dpi, grayscale, 1021x2312 WebP quality 80"),
	("excerpt.t2.switch-locations", "PDF page 103, printed page 2-37, Switch Locations drawing", "switch-locations.md", None, "switch-locations.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 103, crop box 0.4,0.11,0.97,0.86, scanned page rendered at its native resolution (embedded image xref 918, 2551px across 8.26in), rendered at 309 dpi, grayscale, 1455x2708 WebP quality 80"),
	("excerpt.t2.solenoid-table-2-38-01-16", "PDF page 104, printed page 2-38, Solenoid Table (second copy) rows 1-16", "solenoid-table-2-38.md", None, "solenoid-table-2-38-01-16.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 104, crop box 0.12,0.1,0.9,0.39, scanned page rendered at its native resolution (embedded image xref 927, 2551px across 8.26in), rendered at 171 dpi, capped to 1100px wide, grayscale, 1101x580 WebP quality 80"),
	("excerpt.t2.solenoid-table-2-38-17-flippers", "PDF page 104, printed page 2-38, Solenoid Table (second copy) rows 16-28, G.I. and lower flippers", "solenoid-table-2-38.md", None, "solenoid-table-2-38-17-flippers.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 104, crop box 0.12,0.37,0.9,0.68, scanned page rendered at its native resolution (embedded image xref 927, 2551px across 8.26in), rendered at 171 dpi, capped to 1100px wide, grayscale, 1101x620 WebP quality 80"),
	("excerpt.t2.solenoid-locations-lists-1", "PDF page 105, printed page 2-39, Solenoid Locations list 01-28", "solenoid-locations-lists.md", None, "solenoid-locations-lists-1.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 105, crop box 0.06,0.1,0.52,0.56, scanned page rendered at its native resolution (embedded image xref 936, 2551px across 8.26in), rendered at 210 dpi, capped to 800px wide, grayscale, 801x1133 WebP quality 80"),
	("excerpt.t2.solenoid-locations-lists-2", "PDF page 105, printed page 2-39, Solenoid Locations General Illumination Circuits and Flippers lists", "solenoid-locations-lists.md", None, "solenoid-locations-lists-2.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 105, crop box 0.06,0.54,0.52,0.8, scanned page rendered at its native resolution (embedded image xref 936, 2551px across 8.26in), rendered at 210 dpi, capped to 800px wide, grayscale, 801x641 WebP quality 80"),
	("excerpt.t2.solenoid-locations", "PDF page 105, printed page 2-39, Solenoid Locations drawing", "solenoid-locations.md", None, "solenoid-locations.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 105, crop box 0.42,0.11,0.97,0.86, scanned page rendered at its native resolution (embedded image xref 936, 2551px across 8.26in), rendered at 309 dpi, grayscale, 1404x2708 WebP quality 80"),
	("excerpt.t2.interboard-solenoid-circuits-1", "PDF page 114, printed page 3-8, Interboard Wiring: Solenoid Circuits 1-14", "interboard-solenoid-circuits.md", None, "interboard-solenoid-circuits-1.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 114, crop box 0.08,0.04,0.94,0.34, scanned page rendered at its native resolution (embedded image xref 1017, 2551px across 8.26in), rendered at 155 dpi, capped to 1100px wide, grayscale, 1101x544 WebP quality 80"),
	("excerpt.t2.interboard-solenoid-circuits-2", "PDF page 114, printed page 3-8, Interboard Wiring: Solenoid Circuits 14-28 and the tieback diode", "interboard-solenoid-circuits.md", None, "interboard-solenoid-circuits-2.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 114, crop box 0.08,0.32,0.94,0.62, scanned page rendered at its native resolution (embedded image xref 1017, 2551px across 8.26in), rendered at 155 dpi, capped to 1100px wide, grayscale, 1101x544 WebP quality 80"),
	("excerpt.t2.interboard-solenoid-circuits-3", "PDF page 114, printed page 3-8, Interboard Wiring: Flipper Circuits", "interboard-solenoid-circuits.md", None, "interboard-solenoid-circuits-3.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 114, crop box 0.08,0.6,0.94,0.93, scanned page rendered at its native resolution (embedded image xref 1017, 2551px across 8.26in), rendered at 155 dpi, capped to 1100px wide, grayscale, 1101x598 WebP quality 80"),
	("excerpt.t2.interboard-gi-circuits", "PDF page 115, printed page 3-9, Interboard Wiring: General Illumination Circuits", "interboard-gi-circuits.md", None, "interboard-gi-circuits.webp", None, "Terminator 2 Judgement Day Operations Manual.pdf page 115, crop box 0.08,0.05,0.92,0.33, scanned page rendered at its native resolution (embedded image xref 1026, 2551px across 8.26in), rendered at 187 dpi, capped to 1300px wide, grayscale, 1301x614 WebP quality 80"),
)


def manual_excerpts() -> list[dict[str, Any]]:
	"""Return the reviewed proof crops derived from the exact ARC ARC manual bytes.

	The earlier excerpts pin their digests here; the later ones are hashed from the committed files, which the validator
	checks fail-closed against the same digests.
	"""
	records = []
	for identifier, locator, markdown, markdown_sha256, image, image_sha256, image_derivation in EXCERPT_RECORDS:
		records.append({
			"id": identifier, "locator": locator, "path": f"{EXCERPT_ROOT}/{markdown}",
			"sha256": markdown_sha256 or _file_sha256(ROOT / EXCERPT_ROOT / markdown),
			"image": f"{EXCERPT_ROOT}/{image}", "image_sha256": image_sha256 or _file_sha256(ROOT / EXCERPT_ROOT / image),
			"image_derivation": image_derivation,
			"method": "manual", "reviewed": True, "transcribed_by": "curator, manually read and visually checked against the retained crop",
		})
	return records


def source_records() -> list[dict[str, Any]]:
	return [
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "Pinned catalog driver records for the t2_* family", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "sha256": "e894868e68958d1343abfd89dcd229ff7c7d629effb364026b57d8aedb6924e7", "locator": "src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCDMD=0x4; src/wpc/sims/wpc/full/t2.c GEN_WPCDMD, wpc_dispDMD, FLIP_SWNO(12,11) without FLIP_SOL, t2 driver family; src/wpc/core.c core_getSol 45-48 synthetic lower-flipper states; src/wpc/wpc.c wpc_r WPC_FLIPPERS returns ~swMatrix[CORE_FLIPPERSWCOL] on pre-WPC-95 generations", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-alpha.json", "revision": "repository", "locator": "WPC public switch, lamp, solenoid, and five-GI address rules; emulator lamp remapping", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/williams.terminator-2-judgment-day.1991/arcarc/Terminator%202%20Judgement%20Day%20Operations%20Manual.pdf", "original_filename": "Terminator 2 Judgement Day Operations Manual.pdf", "sha256": MANUAL_SHA256, "locator": "ARC ARC manifest ID other.arcarc.williams.terminator-2-judgment-day.1991.8540d654b39c; retained 118-page image-only Williams operations manual. The attached crops were rendered directly from the exact 8540d654... bytes: switch matrix p.46, solenoid/GI table p.48 (1-28), lamp matrix p.53, major-mechanism map and lamp-board legend p.70, drop-target assembly p.89, platform-gun assembly p.90, lamp schematic p.100, lamp, switch and solenoid location drawings p.101, p.103 and p.105, the second solenoid table p.104 (2-38), the 2-39 location lists p.105, and the 3-8/3-9 interboard wiring tables p.114-115.", "excerpts": manual_excerpts(), "license": "NOASSERTION", "attribution": "Williams Electronics"},
		{"id": MANUAL_SUPPORT_SOURCE, "kind": "human_review", "uri": "external:pinmame-manuals/by-machine/williams.terminator-2-judgment-day.1991/arcarc/extracted", "locator": "Retained page index, mechanism notes, rendered pages, contact sheets, and reference PNGs used for visual verification", "license": "NOASSERTION", "attribution": "Williams manual extraction"},
		{"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/source/Terminator%202%20VPW_0022.vpx", "original_filename": "Terminator 2 VPW_0022.vpx", "sha256": TABLE_SHA256, "locator": "Retained known-working VPW 0022 physical table; geometry source for named VPX objects and embedded-script container", "license": "NOASSERTION", "attribution": "VPW table authors"},
		{"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/extracted-vpxtool/script.vbs", "original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True, "locator": "Retained embedded VPW script; evidence authority is semantic_controller and mechanism_causality: cGameName=t2_l8, callbacks, switch semantics, ball stacks, gun mechanism, drop target, flashers, and GI callback behavior", "license": "NOASSERTION", "attribution": "VPW table authors"},
		{"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json", "locator": f"Canonical manifest covers every sorted relative POSIX path, byte size, and SHA-256 under extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, bounds left=0 top=0 right=964 bottom=2162; normalized coordinates are x/964 and y/2162", "license": "NOASSERTION", "attribution": "vpxtool extraction"},
		{"id": NFOZZY_TABLE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/nfozzy-1-12a/source/Terminator%202%20%28Williams%201991%29%201.12a.vpx", "original_filename": "Terminator 2 (Williams 1991) 1.12a.vpx", "sha256": NFOZZY_TABLE_SHA256, "locator": f"Retained nFozzy 1.12a table (cGameName t2_l8; embedded script SHA-256 {NFOZZY_SCRIPT_SHA256}, whose G.I. block matches the pinned comparison script). Used only for its general-illumination model: it reads Controller.ChangedGIStrings and binds public G.I. 0 to its backglass sprite, 2 to the right-playfield lightmaps and the GI_bulbR bulb mesh, 3 to the four Lgi CPU-insert sprites and 4 to the left-playfield lightmaps and the GI_bulbL bulb mesh. Its mechanisms and other geometry are not used.", "license": "NOASSERTION", "attribution": "nFozzy and community table authors"},
		{"id": NFOZZY_EXTRACTION_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/nfozzy-1-12a/extracted-vpxtool.manifest.json", "locator": f"Canonical manifest covers every sorted relative POSIX path, byte size, and SHA-256 under nfozzy-1-12a/extracted-vpxtool; manifest SHA-256 {NFOZZY_MANIFEST_SHA256}; {NFOZZY_FILE_COUNT} files, {NFOZZY_TOTAL_BYTES} bytes, bounds left=0 top=0 right=952.94116 bottom=2164.706; its points are compared after normalizing by these bounds", "license": "NOASSERTION", "attribution": "vpxtool extraction"},
		{"id": G5K_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Terminator%202%20%28Williams%201991%29%20g5k%20v1.1a.vbs", "revision": "0c036bb61b4b4e8c778c37559f6795df8cd1521e", "sha256": "f6c3d5ec0aa95bb6c3ac3160b35adff9a6b1c6d282e64e15a3709f426f08949a", "known_working": False, "locator": "Corroborating g5k script inventory; consulted where it agrees with the retained VPW script, never promoted over it", "license": "NOASSERTION", "attribution": "g5k table authors"},
		{"id": MODERN_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Terminator%202%20%28Williams%201991%29.vbs", "revision": "0c036bb61b4b4e8c778c37559f6795df8cd1521e", "sha256": "1bbcc5873a1db87fe59d1daefbb69b68872cf58f029320a9d7d9410db7c59d97", "known_working": False, "locator": "Comparison copy of the nFozzy script; its four-position trough, pulsed 62/64, virtual devices, and keyframed/magnet cannon are excluded from this physical VPW definition. Its G.I. block (Flashers.obj(0)-(4)) is cited for the per-string grouping only, together with the ROM's own G.I. test", "license": "NOASSERTION", "attribution": "Modern community table authors"},
		{"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:pinmame-roms/t2_l8.zip", "sha256": ROM_SHA256, "locator": "Pre-existing authorized local ROM evidence; bytes are not copied into this repository. A byte scan of the program ROMs of every T2 driver in the library for the WPC_FLIPPERS register address 0x3FD4 finds no read in any Williams build (L-2 only writes it; FreeWPC 0.19 reads it with LDB)", "license": "NOASSERTION", "attribution": "Authorized local evidence"},
		{"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "internal:evidence/runtime/wpc-alpha/terminator-2-t2_l8-solenoid-flasher-tests.json", "revision": RUNTIME_PINMAME_REVISION, "locator": "One hash-pinned LibPinMAME harness run of t2_l8 from empty NVRAM (scenario tools/harness-scenarios/wpc-alpha/t2-solenoid-flasher-tests.json) that steps T.4 SOLENOID TEST through solenoids 1-14 and T.5 FLASHER TEST through flashers 17-27 in repeat mode. Each step pulses one public address while the ROM prints its name and wire colours: solenoid 12 is KNOCK DOWN (BRN-YEL VIO-ORN) and flasher 24 is F.L. C. BACKGLASS (BLU-GRY RED-WHT).", "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_GI_SOURCE, "kind": "runtime_scenario", "uri": "internal:evidence/runtime/wpc-alpha/terminator-2-t2_l8-gi-test.json", "revision": RUNTIME_GI_PINMAME_REVISION, "locator": "One hash-pinned LibPinMAME harness run of t2_l8 from empty NVRAM (scenario tools/harness-scenarios/wpc-alpha/t2-gi-test.json) that steps T.6 GEN'L. ILLUM. through all illumination and then each string; every step changes one public G.I. output alone while the ROM prints its name and wires: public 0 TOP INSERT (WHT-BRN BRN), 1 BOTTOM INSERT (WHT-ORN ORN), 2 RIGHT PLAYFIELD (WHT-YEL YEL), 3 CPU STRING (WHT-GRN GRN), 4 LEFT PLAYFIELD (WHT-VIO VIO). After the fresh-NVRAM restart the ROM also flickers public 3 by itself.", "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	]


def _device_base(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, label, role in (
		(1, "Coin Chute 1", "cabinet.coin.1"), (2, "Coin Chute 2", "cabinet.coin.2"), (3, "Coin Chute 3", "cabinet.coin.3"), (4, "Coin Chute 4", "cabinet.coin.4"),
		(5, "Coin-Door Cancel", "service.cancel"), (6, "Coin-Door Down", "service.down"), (7, "Coin-Door Up", "service.up"), (8, "Coin-Door Enter", "service.enter"),
	):
		items.append(_device_base(f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address, "optional" if address == 4 else "used", (CONTROLLER_SOURCE, MANUAL_SOURCE), aliases=aliases("pinmame.switch", address), normally_closed=False, roles=[role], physical={"location": "coin door / cabinet"}))
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = MATRIX_LABELS.get(address, f"Unused matrix position {address}")
			unused = address not in MATRIX_LABELS
			kind = "constant" if address == 24 else "switch"
			extra: dict[str, Any] = {"aliases": aliases("pinmame.switch", address, f"{column}-{row}")}
			if kind == "constant":
				extra["constant_active"] = True
				extra["initial_active"] = True
			elif not unused:
				extra["normally_closed"] = address in {21, 22}
				extra["pulse"] = address in MATRIX_PULSES
			if address in {11, 12}:
				extra["roles"] = ["flipper.lower.right.button" if address == 11 else "flipper.lower.left.button"]
			elif address == 13:
				extra["roles"] = ["cabinet.start"]
			elif address == 14:
				extra["roles"] = ["cabinet.tilt"]
			elif address == 21:
				extra["roles"] = ["cabinet.slam-tilt"]
			elif address == 22:
				extra["roles"] = ["cabinet.coin-door"]
				extra["initial_active"] = True
			elif address == 23:
				extra["roles"] = ["service.ticket"]
			extra["physical"] = {"switch_type": "microswitch" if not unused else "unknown", "notes": f"Printed WPC switch matrix column {column}, row {row}; {'retained VPW switch semantic' if not unused else 'printed Not Used position'}."}
			if address in {11, 12}:
				extra["physical"]["switch_type"] = "button"
				extra["physical"]["notes"] = f"Printed WPC switch matrix column {column}, row {row}: the cabinet {'right' if address == 11 else 'left'} flipper button. t2GameData declares FLIP_SWNO(12,11) with no FLIP_SOL, so core_updateSw rewrites this switch from generic cabinet input {112 if address == 11 else 114} on every update; it cannot be driven directly."
			elif address in {41, 42, 43}:
				extra["physical"]["notes"] += " " + JET_BINDING_NOTE
			items.append(_device_base(f"switch.matrix-{address}", label, kind, "pinmame.input.switch", address, "unused" if unused else "used", (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) if not unused else (MANUAL_SOURCE, CORE_SOURCE), **extra))
	# t2GameData declares FLIP_SWNO(12,11) with no FLIP_SOL: the flippers are cabinet-wired, core_updateSw copies the generic
	# button bits 112/114 into matrix switches 11/12 on every update, and core.c's EOS simulation never runs. The EOS bits
	# 111/113 stay host-writable and wpc_r serves the column at WPC_FLIPPERS on this generation; no Williams T2 program ROM in
	# the library addresses that register, but the FreeWPC 0.19 build reads it, so they stay optional.
	for address in range(111, 119):
		button = address in {112, 114}
		eos = address in {111, 113}
		right = address in {111, 112}
		side = "right" if right else "left"
		if button:
			items.append(_device_base(f"switch.generic-{address}", f"Lower {side.title()} Flipper Button", "switch", "pinmame.input.switch", address, "used", (CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases("pinmame.switch", address), normally_closed=False, roles=[f"flipper.lower.{side}.button"], physical={"location": "cabinet flipper button", "switch_type": "button", "notes": f"Live generic cabinet-flipper input from PinMAME's flipper switch column. t2GameData declares FLIP_SWNO(12,11) with no FLIP_SOL, so core_updateSw copies it to matrix switch {11 if right else 12} on every update; a consumer drives this address, not the matrix one."}))
		elif eos:
			items.append(_device_base(f"switch.generic-{address}", f"Lower {side.title()} Flipper EOS", "switch", "pinmame.input.switch", address, "optional", (CONTROLLER_SOURCE, CORE_SOURCE, ROM_SOURCE), aliases=aliases("pinmame.switch", address), normally_closed=False, roles=[f"internal.flipper.lower.{side}.eos"], physical={"location": "internal public address space", "switch_type": "unknown", "notes": "PinMAME's generic end-of-stroke bit for this flipper. Terminator 2's flippers are cabinet-wired (FLIP_SWNO(12,11) with no FLIP_SOL), so core.c's EOS simulation never runs and nothing synthesizes it; no CPU-side contact is wired to it, so it rests open (0) unless a host writes it. On this pre-WPC-95 generation wpc_r serves the flipper column at WPC_FLIPPERS (0x3FD4). No Williams T2 program ROM in the authorized library addresses that register, but the FreeWPC 0.19 build (t2_f19) reads it, so the bit stays optional rather than unused."}))
		else:
			items.append(_device_base(f"switch.generic-{address}", f"Unused Generic Flipper Input {address}", "switch", "pinmame.input.switch", address, "unused", (CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases("pinmame.switch", address), normally_closed=False, roles=["internal.unused.flipper"], physical={"location": "lower flipper cabinet/playfield interface", "switch_type": "unknown"}))
	for address in range(1, 9):
		items.append(_device_base(f"switch.dip-{address}", f"CPU/Sound Board DIP {address}", "dip_switch", "pinmame.input.dip", address, "used", (CONTROLLER_SOURCE, MANUAL_SOURCE, CORE_SOURCE), aliases=aliases("pinmame.dip", address), physical={"location": "CPU/Sound board"}))
	return items


def _solenoid_output(address: int, label: str, kind: str, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	return _device_base(output_id(label), label, kind, "pinmame.output.solenoid", address, availability, refs, aliases=aliases("pinmame.solenoid", address), **extra)


def output_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 29):
		kind = "flasher" if 17 <= address <= 27 else "coil"
		physical: dict[str, Any] = {"notes": f"Manual physical device: {SOLENOID_LABELS[address]}; printed on the 1-28 and 2-38 solenoid tables, the 2-39 Solenoid Locations list and the 3-8 interboard wiring table."}
		wire_color, connection, transistor, part_number = SOLENOID_WIRING[address]
		physical["part_number"] = part_number
		if address in FLASHER_QUANTITY:
			physical["quantity"] = FLASHER_QUANTITY[address]
		if address in SOLENOID_SCRIPT_CALLBACKS:
			physical["notes"] += f" Retained script callback: {SOLENOID_SCRIPT_CALLBACKS[address]}."
		if address == 12:
			physical["assembly_part_number"] = "A-14908"
			physical["notes"] += (
				" The drop-target knock-down coil. The 2-23 A-14615 1-Bank Drop Target Assembly parts list includes item 23, A-14908 "
				"Target Knock Down Assembly (01-8647-L actuator, A-14913 frame and eyelet, SM1-26-600 coil), bolted beside the AE-26-1200 "
				"reset coil of solenoid 28; the 1-28 solenoid table and the 2-39 Solenoid Locations list print solenoid 12 as Knock Down "
				"with that SM1-26-600 coil, and the 2-39 drawing prints balloon 12 on the drop-target assembly. The 2-38 copy of the "
				"solenoid table prints the row as Not Used and blanks its part-number cell, but keeps its Low Power type, Brn-Yel wire, "
				"J127-5 connection and Q52 transistor, and the 3-8 interboard table wires Solenoid 12 Brown/Yellow to J127-5 and Q52. "
				"The L-8 ROM's T.4 SOLENOID TEST names solenoid 12 KNOCK DOWN with the printed BRN-YEL wire and pulses public 12. The "
				"retained VPW script has no SolCallback(12), and the nFozzy comparison script keeps a SolDTdown handler for it commented "
				"out as a cut feature; owner repair reports describe the small knock-down coil fitted on the drop-target assembly but not "
				"seen to fire in normal play, consistent with Not Used on 2-38 meaning that the game rules leave it idle. A recreation fits "
				"the coil so that a pulse drops the target and closes switch 77."
			)
		if address == 24:
			physical["notes"] += " The manual identifies a backglass flashlamp on the Blu-Gry / J125-7 / Q32 branch, and the L-8 ROM's T.5 FLASHER TEST prints F.L. C. BACKGLASS with the wires BLU-GRY RED-WHT and pulses public 24. The retained VPW script has no SolCallback(24); that is a gap in the table, which renders no backglass, and says nothing against the machine."
		if address in {18, 19, 20, 21, 22, 23, 24, 25, 26}:
			physical["notes"] += " " + J125_OFFSET_NOTE
		if address in {14, 15}:
			physical["notes"] += " " + JET_BINDING_NOTE
		sources = (MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE) if address == 12 else (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, RUNTIME_SOURCE) if address == 24 else (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_solenoid_output(address, SOLENOID_LABELS[address], kind, "used", sources, physical=physical, wiring={"board": "WPC driver board", "control_wire": wire_color, "control_connection": connection, "driver_transistor": transistor}))
	for address in range(29, 51):
		if address in {29, 30}:
			items.append(_solenoid_output(address, f"WPC State Channel {address}", "virtual", "used", (CONTROLLER_SOURCE, CORE_SOURCE), roles=["internal.wpc-state"], physical={"notes": f"PinMAME mirrors WPC_GILAMPS bit {address - 24}, one of the CPU board's J111 state bits, to public address {address}; a live controller state channel, not a playfield device."}))
		elif address == 31:
			items.append(_solenoid_output(address, "Game-On Solenoid Relay", "relay", "used", (CONTROLLER_SOURCE, CORE_SOURCE), roles=["internal.wpc-state", "cabinet.game-on-relay"], physical={"notes": "On this pre-Fliptronic WPC generation, pinned wpc.c identifies public address 31 as the real Game-On solenoid controlled by WPC_GILAMPS bit 7 through the power-driver relay chain to the cabinet switch and flippers; pinned core.c also gates the synthetic flipper states on it. It is a cabinet/flipper-enable relay, not a playfield device."}))
		elif address == 32:
			items.append(_solenoid_output(address, f"Unused WPC State/Generic Output {address}", "virtual", "unused", (CONTROLLER_SOURCE, CORE_SOURCE), roles=["internal.unused.wpc-output"], physical={"notes": "PinMAME's WPC remap has no fourth state bit; this public address is constant zero and is not a physical output."}))
		elif address in {45, 46, 47, 48}:
			right = address in {45, 46}
			side = "Right" if right else "Left"
			wire = ("Blu-Yel", "J109-7") if right else ("Gry-Yel", "J109-5")
			if address in {45, 47}:
				items.append(_solenoid_output(address, f"Synthetic Lower {side} Flipper Power", "virtual", "used", (CONTROLLER_SOURCE, CORE_SOURCE), roles=["internal.synthetic-flipper"], physical={"notes": f"Fabricated by core_updateSw from the live lower-{side.lower()} flipper button while the Game-On relay (31) is on: core_getSol {address} reads the power bit of PinMAME's synthetic flipper state. The physical FL-11630 flipper takes its power from the power driver board ({wire[0]}, {wire[1]}) through the Game-On relay and is switched by the cabinet button; there is no CPU flipper drive."}))
			else:
				items.append(_solenoid_output(address, f"Synthetic Lower {side} Flipper", "virtual", "used", (CONTROLLER_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE), roles=["internal.synthetic-flipper", f"flipper.lower.{side.lower()}"], physical={"notes": f"PinMAME's combined lower-{side.lower()} flipper state (sL{side[0]}Flipper) that the retained script's SolCallback(sL{side[0]}Flipper) consumes to animate the bat; not an additional coil. The physical FL-11630 flipper takes its power from the power driver board ({wire[0]}, {wire[1]}) through the Game-On relay and is switched by the cabinet button."}))
		else:
			items.append(_solenoid_output(address, f"Unused WPC State/Generic Output {address}", "virtual", "unused", (CONTROLLER_SOURCE, CORE_SOURCE), roles=["internal.unused.wpc-output"], physical={"notes": "PinMAME compatibility/state channel; Terminator 2 declares no upper flippers, no custom solenoids and no simulator ball-shooter state, so nothing drives this public address."}))
	return items


def lamp_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in sorted(LAMP_LABELS):
		unused = address == 18
		availability = "unused" if unused else "optional" if address == 84 else "used"
		extra: dict[str, Any] = {"aliases": aliases("pinmame.lamp", address, f"{address:03d}"), "physical": {"notes": f"Printed lamp matrix address {address // 10}-{address % 10}; manual lamp address {address}."}}
		if address == 84:
			extra["roles"] = ["cabinet.start"]
		if address == 18:
			extra["physical"]["notes"] += " Printed lamp matrix says Not Used; no L18 object exists in the retained VPX table."
		if address in {51, 52}:
			extra["physical"]["quantity"] = 2
			extra["physical"]["part_number"] = "#44"
		column, row = divmod(address, 10)
		table_column, table_row = column if column < 8 else 9, row if row < 3 else row + 1
		extra["physical"]["notes"] += (
			f" Connector labels differ between printed sheets: the 1-33 lamp matrix table prints column {column} on J138-{table_column} and row {row} on J133-{table_row};"
			f" the 2-34 lamp schematic draws them on J137-{column} and J133-{row}. Both give the same wires and address, so this is a wiring detail, not a conflict"
			" (conflict.lamp-schematic-connector-labels is ignored)."
		)
		refs = (MANUAL_SOURCE, CORE_SOURCE) if unused else (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device_base(f"lamp.matrix-{address}", LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, availability, refs, **extra))
	return items


def gi_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(5):
		rom_name, list_name, rom_wires, wire, connection, triac = GI_STRINGS[address]
		physical: dict[str, Any] = {
			"part_number": "#555",
			"notes": (
				f"General-illumination string {address + 1}, {list_name}: the L-8 ROM's T.6 GEN'L. ILLUM. test changes public G.I. {address} "
				f"alone while it prints {rom_name} and {rom_wires}, and the 2-39 Solenoid Locations list prints {address + 1:02d} #555 {list_name}. "
				f"The 1-28 and 2-38 solenoid tables print this row as {GI_TABLE_PRINT[address]}. {GI_TABLE_NOTE}"
			),
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, RUNTIME_GI_SOURCE, CORE_SOURCE)
		if address == 0:
			physical["location"] = "backbox insert panel, top"
			physical["notes"] += " The 3-9 interboard table routes the brown string to the insert only (feed J120-1, return J120-7): it lights the upper half of the backbox insert panel behind the translite. The retained VPW script's UpdateGI Case 0 does nothing, and the nFozzy table drives only its backglass sprite from public 0."
		elif address == 1:
			physical["location"] = "backbox insert panel, bottom"
			physical["notes"] += " The 3-9 interboard table prints the insert pins J120-2 (feed) and J120-8 (return) on its Green row and no connector at all on its Orange row, while the 1-28 and 2-38 tables put J120-8 on Wht-Orn; on the WPC power driver board J120-2/J120-8 are the orange string's insert pins, and the ROM names the orange string BOTTOM INSERT, so this string lights the lower half of the backbox insert panel. The retained VPW script has no Case 1 at all."
		elif address == 2:
			physical["notes"] += " The 3-9 interboard table routes the yellow string to the playfield only (feed J121-3, return J121-9). The retained VPW script drives every playfield G.I. light it has from public 2 (UpdateGI Case 2: arrays GI2 and GI3) and has no Case 4, so it lights the left side from this string as well; that is a simplification of the table, not a property of the machine."
			refs += (VPX_SCRIPT_SOURCE, NFOZZY_TABLE_SOURCE, MODERN_SCRIPT_SOURCE)
		elif address == 3:
			physical["quantity"] = 4
			physical["assembly_part_number"] = "A-14518"
			physical["notes"] += " The 3-9 interboard table routes the green string's playfield pins J121-5 (feed) and J121-10 (return). The 2-4 major-mechanisms map marks one G. I. Lamp Assembly, A-14518 (lamp board C), a straight four-socket board on the playfield centre line under the CPU inserts; the retained VPW script's UpdateGI Case 3 switches its four Light2-Light5 lights there, and the nFozzy table drives its four Lgi CPU-insert sprites from public 3. After the fresh-NVRAM restart the ROM flickers this string by itself, so it carries effects of its own."
			refs += (VPX_SCRIPT_SOURCE, NFOZZY_TABLE_SOURCE, MODERN_SCRIPT_SOURCE)
		else:
			physical["notes"] += " The 3-9 interboard table routes the violet string to the playfield (feed J121-6, return J121-11) and to the cabinet (feed J119-3, return J119-1): besides the left side of the playfield it lights the coin-door lamps, which are not placed. The retained VPW script's UpdateGI Case 4 is a bare Exit Sub under the comment Left Playfield, so the table lights this side from public 2 instead (see public 2)."
			refs += (VPX_SCRIPT_SOURCE, NFOZZY_TABLE_SOURCE, MODERN_SCRIPT_SOURCE)
		roles = ["cabinet.insert-panel"] if address in {0, 1} else None
		extra: dict[str, Any] = {"aliases": aliases("pinmame.gi", address), "physical": physical, "wiring": {"board": "WPC driver board", "control_wire": wire, "control_connection": connection, "driver_transistor": triac}}
		if roles:
			extra["roles"] = roles
		items.append(_device_base(f"gi.string-{address + 1}", list_name, "gi", "pinmame.output.gi", address, "used", refs, **extra))
	return items


def displays() -> list[dict[str, Any]]:
	return [{"id": "display.dmd", "label": "128x32 dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE)}, "provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE)}]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[tuple[str, str, list[str], str]], *refs: str) -> dict[str, Any]:
		return {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "positions": [{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description} for position_id, position_label, position_sensors, description in positions], "behavior": behavior, "provenance": provenance(*refs)}
	return [
		mechanism("mechanism.three-ball-trough", "Three-ball trough and outhole", "other", [output_id("Trough"), output_id("Outhole")], ["switch.matrix-15", "switch.matrix-16", "switch.matrix-17", "switch.matrix-18"], "Retained VPW initialization is bsTrough.InitSw 18,17,16,15 with Balls=3; BallRelease kicks at 90 degrees and strength 8. The script does not prove a four-ball trough.", [("left", "Left trough", ["switch.matrix-15"], "Manual trough left position."), ("center", "Center trough", ["switch.matrix-16"], "Manual trough center position."), ("right", "Right trough", ["switch.matrix-17"], "Manual trough right position."), ("outhole", "Outhole", ["switch.matrix-18"], "Manual outhole position.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.shooter-lane", "Shooter lane and auto plunger", "kicker", [output_id("Plunger")], ["switch.matrix-78"], "The retained saucer stack uses switch 78, a 0-degree/50-strength kick, and kick-force variance 3.", [("shooter", "Shooter lane", ["switch.matrix-78"], "Shooter switch and lane.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.left-lock", "Left lock saucer", "kicker", [output_id("Left Lock")], ["switch.matrix-51"], "The retained left lock stack uses switch 51 and kicks at 160 degrees with strength 13.", [("locked", "Left lock occupied", ["switch.matrix-51"], "Left lock saucer.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.top-lock", "Top lock saucer", "kicker", [output_id("Top Lock")], ["switch.matrix-55"], "The retained top lock stack uses switch 55, kicks at 270 degrees with strength 5, and has kick-force variance 6.", [("locked", "Top lock occupied", ["switch.matrix-55"], "Top lock saucer.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.gun-traverse", "Motorized cannon traverse", "motorized", [output_id("Gun Motor")], ["switch.matrix-31", "switch.matrix-32", "switch.matrix-33"], "cvpmMech one-solenoid/reverse/non-linear; solenoid 11, length 240, steps 240; home switch 33 window 0-5, mark switch 32 window 98-105; visual callback uses CurrentPos=aNewPos/3. The retained script moves T2_Gun and its held ball, not a keyframed or magnet cannon.", [("home", "Gun home", ["switch.matrix-33"], "Position window 0-5."), ("mark", "Gun mark", ["switch.matrix-32"], "Position window 98-105."), ("loaded", "Gun loaded", ["switch.matrix-31"], "Ball-loaded sensor at the cannon." )], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.gun-fire", "Cannon fire and gun-loaded kicker", "kicker", [output_id("Gun Kicker")], ["switch.matrix-31", "switch.matrix-34"], "Solenoid 2 fires the loaded ball from switch 31 by -CurrentPos at strength 45, clears the loaded ball, and is commanded by the grip trigger switch 34.", [("loaded", "Gun loaded", ["switch.matrix-31"], "Loaded-ball firing state.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.skull-ball-popper", "Skull ball popper", "toy", [output_id("Ball Popper")], ["switch.matrix-76", "switch.matrix-77"], "SolSkull is the retained callback: manual solenoid 1 Ball Popper opens the skull/ball path from switch 76. The callback name is retained and is not turned into a virtual skull device.", [("popper", "Ball popper", ["switch.matrix-76"], "Ball popper switch."), ("skull-down", "Skull target down", ["switch.matrix-77"], "Drop-target state." )], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.drop-target", "Single skull drop target with knock-down", "drop_target_bank", [output_id("Drop Target"), output_id("Knock Down")], ["switch.matrix-77"], "One A-14615 drop target under the skull, sensed by switch 77. Solenoid 28 (AE-26-1200 reset coil) raises it; the retained script models this as dtDrop1.SolDropUp. Solenoid 12 (the A-14908 knock-down sub-assembly's SM1-26-600 coil, 2-23 parts list) drops it from below without a ball strike; the retained VPW script has no callback for 12 and the production game is not seen to use it in play, but the ROM's solenoid test pulses it, so a recreation that fits it must drop the target and close switch 77 on a pulse.", [("target", "Drop target", ["switch.matrix-77"], "Single-bank target.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
		mechanism("mechanism.kickback", "Left outer-lane kickback", "kicker", [output_id("Kickback")], ["switch.matrix-25"], "SolAPlunger fires Plunger1, the left outer-lane kicker saver; it is distinct from the auto-plunger output 9.", [("left-outlane", "Left outlane", ["switch.matrix-25"], "Kickback entry switch.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.flippers", "Direct-wired lower flippers", "other", [output_id("Synthetic Lower Right Flipper"), output_id("Synthetic Lower Left Flipper")], ["switch.generic-112", "switch.generic-114", "switch.matrix-11", "switch.matrix-12"], "Two C-13174 lower flipper assemblies with FL-11630 coils, powered from the power driver board (right Blu-Yel J109-7, left Gry-Yel J109-5) through the Game-On relay (31) and switched by the cabinet buttons; there is no CPU flipper drive. PinMAME fabricates public 45-48 from the buttons for animation, and the matrix copies 11/12 tell the ROM a button is held.", [("lower-right", "Lower-right flipper", ["switch.generic-112", "switch.matrix-11"], "Animate from synthetic state 46."), ("lower-left", "Lower-left flipper", ["switch.generic-114", "switch.matrix-12"], "Animate from synthetic state 48.")], MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{"id": "conflict.lamp-schematic-connector-labels", "path": "outputs.pinmame.output.lamp", "description": "The lamp matrix table on printed page 1-33 (repeated on PDF page 117, and on 2-34 where the scan fills in column 8's pin digit) prints columns on J138-1 to J138-7 and J138-9 and rows on J133-1, J133-2 and J133-4 to J133-9, while the lamp matrix schematic on printed page 2-34 draws columns on J137-1 to J137-8 and rows on J133-1 to J133-8; the 1-33 lamp-circuit example also routes its column through J137. Read address by address at native resolution, both sheets give the same eight column and row wire colours and the same addresses 11-88, and the schematic names no lamps. Matrix address/name identity is preserved from the printed matrix table; neither connector reading is synthesized into wiring fields. Resolution path: a photograph of an unrestored machine's power driver board lamp connectors, showing whether the column harness plugs J137 or J138 and which J133 pins the rows use.", "status": "ignored", "rationale": "A wiring-detail disagreement, not a conflict (runbook, What is not a conflict): the two sheets differ only in connector labels and agree on every lamp's address and on its column and row wires, so nothing a recreation consumes is in doubt. Lamp identity follows the printed matrix table, and each lamp note states both connector readings.", "source_refs": [MANUAL_SOURCE, MANUAL_SUPPORT_SOURCE, CORE_SOURCE]},
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
		item["physical_compatibility"] = "compatible" if driver_id in {"t2_l83", "t2_l84", "t2_f19", "t2_f20", "t2_f32"} else "identical"
		item["variant_notes"] = {
			"t2_l83": "Community profanity/bugfix/MOD ROM; retained as a physical-compatible ROM variant with the same Williams WPC-DMD I/O and playfield.",
			"t2_l84": "Community profanity/bugfix/MOD ROM; retained as a physical-compatible ROM variant with the same Williams WPC-DMD I/O and playfield.",
			"t2_f19": "FreeWPC alternative firmware for the stock physical T2 machine; it is a compatible controller variant, not a separate physical machine or retheme. Unlike the Williams builds it reads the WPC_FLIPPERS register.",
			"t2_f20": "FreeWPC alternative firmware for the stock physical T2 machine; it is a compatible controller variant, not a separate physical machine or retheme.",
			"t2_f32": "FreeWPC alternative firmware for the stock physical T2 machine; it is a compatible controller variant, not a separate physical machine or retheme.",
		}.get(driver_id, "Firmware, sound, attract-score, profanity, or LED ghost-fix revision; physical playfield, controller generation, and I/O are unchanged.")
		items.append(item)
	return items


def build_semantic() -> dict[str, Any]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": "williams.terminator-2-judgment-day.1991", "name": "Terminator 2: Judgment Day", "manufacturer": "Williams", "year": 1991, "kind": "physical_pinball", "ipdb_id": 2524, "model_number": "T2", "opdb_id": "GR9Bx-MQkd5"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "validated"}},
		"controller": {"platform": "pinmame.wpc-alpha", "hardware_generation": "0x4", "inversion_applied_by_emulator": True},
		"drivers": drivers(), "inputs": input_devices(), "outputs": output_devices() + lamp_devices() + gi_devices(), "displays": displays(), "mechanisms": mechanisms(),
		"relationships": [
			{"id": "relationship.trough-release", "kind": "pulse", "source": output_id("Trough"), "destination": "switch.matrix-15", "provenance": provenance(MANUAL_SOURCE, VPX_SCRIPT_SOURCE)},
			{"id": "relationship.drop-target-reset", "kind": "pulse", "source": output_id("Drop Target"), "destination": "switch.matrix-77", "provenance": provenance(MANUAL_SOURCE, VPX_SCRIPT_SOURCE)},
			{"id": "relationship.drop-target-knock-down", "kind": "pulse", "source": output_id("Knock Down"), "destination": "switch.matrix-77", "provenance": provenance(MANUAL_SOURCE, RUNTIME_SOURCE)},
		],
		"sources": source_records(), "knowledge": {"path": "knowledge/williams/terminator-2-judgment-day-1991.md", "status": "complete"}, "conflicts": conflicts(),
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true", help="Delegate a non-destructive determinism check to the spatial curator")
	mode.add_argument("--regenerate", action="store_true", help="Delegate canonical generation to the spatial curator")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write and verify the retained full-file VPX extraction manifest")
	args = parser.parse_args()
	from curate_terminator_2_spatial import check, generate
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"T2 extraction manifest written and verified: {write_extraction_manifest(source_root)}")
	elif args.check:
		check(ROOT)
	else:
		generate(ROOT)


if __name__ == "__main__":
	main()
