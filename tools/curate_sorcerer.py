#!/usr/bin/env python3
"""Deterministic, fail-closed curation of Williams Sorcerer (1985, System 9).

The reviewed manual tables live in sorcerer_data.py, the excerpts under
evidence/excerpts/williams.sorcerer.1985/, the compact runtime evidence in
evidence/runtime/williams/ and the table geometry in a pinned seed. Generation
reads none of the external roots. --check refuses drift in every product and
excerpt; --verify-evidence re-derives the external evidence when the roots are
configured. An existing author-ready record is never overwritten.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_game_defs.spatial import _round_point
from pinmame_game_defs.validation import validate_machine
import drawing_callouts
from pinmame_flipper_column import FLIPPER_COLUMN_ADDRESSES, VPM_LIBRARY_SOURCE, VPM_LIBRARY_URI, VPM_S11_SHA256, flipper_column_id
import sorcerer_data as data

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = data.MACHINE_ID
DEFINITION = Path("machines/partial/williams/sorcerer-1985.json")
AUTHOR_READY = Path("machines/author-ready/williams/sorcerer-1985.json")
GEOMETRY = Path("tools/seeds/williams/sorcerer-1985-geometry.json")
CALLOUTS = Path("tools/seeds/williams/sorcerer-1985-callouts.json")
KNOWLEDGE_SEED = Path("tools/seeds/williams/sorcerer-1985-knowledge.md")
KNOWLEDGE = Path("knowledge/williams/sorcerer-1985.md")
REPORT = Path("reports/spatial/williams/sorcerer-1985.json")
REPORT_MD = Path("reports/spatial/williams/sorcerer-1985.md")
RUNTIME = Path("evidence/runtime/williams/sorcerer-l2-diagnostics-and-gameplay.json")
RUNTIME_L1 = Path("evidence/runtime/williams/sorcerer-l1-solenoid-test.json")
EXCERPTS = Path("evidence/excerpts") / MACHINE_ID

CATALOG = "pinmame.catalog.97aa922bf8e4"
CORE = "pinmame.core.97aa922bf8e4"
PROFILE = "controller-profile.pinmame-system-11"
MANUAL = "manual.williams.sorcerer.1985"
IPDB = "ipdb.2242"
SCRIPT = "vpx-script.sorcerer.v4-0-4"
LIBRARY = VPM_LIBRARY_SOURCE
RUNTIME_SOURCE = "runtime.sorcerer.l2-diagnostics-and-gameplay"
RUNTIME_L1_SOURCE = "runtime.sorcerer.l1-solenoid-test"
TABLE = "vpx-table.sorcerer.v4-0-4"
EXTRACTION = "vpx-extraction.sorcerer.v4-0-4"
CALLOUT_SOURCE = "drawing-callouts.sorcerer.2026-10-16"

SCRIPT_SHA256 = "2222f6be1fcd5598fd4f925e99f936bdcb5f53704420e55d7731048a1a93e377"
SCRIPT_CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
IPDB_PAGE_SHA256 = "3c5f60d9074d6fb2bb6ae2c0d652851a14cce12ef527f66ad5d23b32ad44c8e9"
RUNTIME_MANIFEST_SHA256 = "0a04a8d2d92399bf28a73b4205e47bf7675ce5d26ea3b5f5d3fe86c5e239bbfc"

# excerpt id: (file, locator, method, image file or None)
EXCERPT_FILES = {
	"switch-matrix": ("switch-matrix.md", "Instruction Manual PDF33 printed14 (reprinted PDF13 printed33), complete System 9 Switch-Matrix Table", None),
	"lamp-matrix": ("lamp-matrix.md", "Instruction Manual PDF33 printed14 (reprinted PDF13 printed33), complete System 9 Lamp-Matrix Table", None),
	"solenoid-table": ("solenoid-table.md", "Instruction Manual PDF14 printed13, complete System-9 Solenoid Table and notes", None),
	"location-parts-lists": ("location-parts-lists.md", "Instruction Manual PDF19-20, Switch Locations, Solenoids and Lamp Locations parts lists", None),
	"operation-and-diagnostics": ("operation-and-diagnostics.md", "Instruction Manual PDF2, PDF6 and PDF11: ROM summary, control locations, game play, test procedures", None),
	"backbox-wiring": ("backbox-wiring.md", "Instruction Manual PDF18 Backbox Wiring: power supply 3J7-3J9 and CPU 1J18/1J19", None),
	"cpu-flipper-relay": ("cpu-flipper-relay.md", "Instruction Manual PDF24, CPU schematic 16-8923 sheet 1: flipper relay K1 and jumper W5", "cpu-flipper-relay.webp"),
	"cabinet-wiring": ("cabinet-wiring.md", "Instruction Manual PDF21, System 9 Cabinet Wiring Diagram", "cabinet-wiring.webp"),
	"pinmame-contract": ("pinmame-contract.md", "driver.c 2686-2687; s11games.c 38-41, 93-114; s11.c 56-60, 372, 907-912; s11.h; core.h", None),
	"script-contract": ("script-contract.md", "Sorcerer (Williams 1985) v4.0.4.vbs controller bindings", None),
	"script-library": ("script-library.md", "s11.vbs lines 23-40 cabinet and flipper constants", None),
}
EXCERPT_DIGESTS = {
	"switch-matrix": "4e5c4c8fa4c564e58845fd34e4bd88ebd2bd34e41e77c5d3f12500dde6506d9d",
	"lamp-matrix": "8407d92ef79b44997dfd2cdebceb7b61adacb14fc32f911f67a1aecd13218d1c",
	"solenoid-table": "5011df56203ffb25edaa523b2cde697d258128779738c12c2249e8c3592bea15",
	"location-parts-lists": "9731cb0ecada4d2bdab3bb0a1a2a6d745a8c170676a851ec86fe87799b5aa4de",
	"operation-and-diagnostics": "5a456bf9e85f5fa7c225a7b990786dbcdb80441ebd5a6e64b8ddae0c6d526796",
	"backbox-wiring": "9f047be161a25e58607a16c2e61f34d1e68ca7b522fe014b62237e24f76893ed",
	"cpu-flipper-relay": "e7e5ec35d3b6c8a9f71c7303e5df02d967fc3a3c7aba3c4daa993dc1adc8a108",
	"cabinet-wiring": "949eb4aafe0a6367f67184c18b91edcfe83dbf1832e6a0914d689dd2e68eb154",
	"pinmame-contract": "3030168d9bf284fba0e157b8debf0c11a173a6c3d1f7ea345415b636e943c081",
	"script-contract": "9c4cf5ebfa0ab3df711b9bf07d78c0e8233c454bacb241c26f9fb381252e5a9a",
	"script-library": "13062073ce29547ae067eec5cf024dee328da8594131921663c17c4bd53bf0ee",
}
IMAGE_DERIVATIONS = {
	"cpu-flipper-relay": ("24dfa33e3b0c82fdf679f5bf8ee18effbb096085b905c8f56f0143f25f63ee58", "Williams_1985_Sorcerer_Instruction_Manual_with_schematics.pdf page 24, crop box 0.66,0.57,0.935,0.745, born-digital page rendered for legibility (vector line art, no type in region), rendered at 200 dpi, grayscale, 935x385 WebP quality 80"),
	"cabinet-wiring": ("e7d4e11bd1019e8f735f08d2d54babd2f2131ba3e83e7af08632ff6c8edc7f3b", "Williams_1985_Sorcerer_Instruction_Manual_with_schematics.pdf page 21, crop box 0.127,0.379,0.46,0.66, scanned page rendered at its native resolution (embedded image xref 191, 1616px across 10.77in), rendered at 150 dpi, grayscale, 850x464 WebP quality 80"),
}


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(label: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def provenance(*refs: str, status: str = "validated") -> dict:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def aliases(namespace: str, address: int, *, padded: bool = True) -> list[dict]:
	values = [str(address)]
	if padded and address > 0:
		values += [f"{address:02}", f"{address:03}"]
	return [{"namespace": namespace, "value": value} for value in dict.fromkeys(values)]


# ---------------------------------------------------------------- spatial

def load_geometry(root: Path) -> dict | None:
	path = root / GEOMETRY
	return load_json(path) if path.is_file() else None


def located(identifier: str, role: str, names: list[str], geometry: dict | None, status: str = "observed") -> dict | None:
	if geometry is None or not names:
		return None
	bounds = geometry["bounds"]
	width, height = bounds["right"] - bounds["left"], bounds["bottom"] - bounds["top"]
	points = []
	for index, name in enumerate(names, 1):
		obj = geometry["objects"][name]
		points.append({"id": f"{identifier}.{role}.{index}", "role": role, "space": "playfield",
		               "x": _round_point((obj["x"] - bounds["left"]) / width),
		               "y": _round_point((obj["y"] - bounds["top"]) / height),
		               "provenance": provenance(TABLE, SCRIPT, MANUAL, status=status)})
	return {"status": status, "placements": points}


def anchors(geometry: dict | None, kind: str, address: int) -> list[str]:
	if geometry is None:
		return []
	return list(geometry.get("anchors", {}).get(kind, {}).get(str(address), []))


# ---------------------------------------------------------------- inputs

def switch_wiring(address: int) -> dict:
	column, row = divmod(address - 1, 8)
	drive_wire, drive = data.SWITCH_COLUMNS[column]
	return_wire, ret = data.SWITCH_ROWS[row]
	return {"board": "System 9 CPU Board D-10534 switch matrix", "drive_connection": drive, "drive_wire": drive_wire,
	        "return_connection": ret, "return_wire": return_wire}


SWITCH_NOTES = {
	1: "Cabinet pendulum tilt 7SW1 on the cabinet sheet, column 1J8-1 with diode 7D1. The retained script's vpmNudge uses it as its tilt switch.",
	2: "Cabinet ball-roll tilt 7SW2 (diode 7D2). Sorcerer sets no S11_MUXSW2, so PinMAME leaves this address to the host; it is not an A/C-relay feedback here.",
	3: "Cabinet credit (start) button 7SW3 (diode 7D3).",
	4: "Coin-door right coin chute 7SW4; S11.VBS calls it swCoin3.",
	5: "Coin-door centre coin chute 7SW5. The switch-location list prints its assembly as BLANK FOR DOMESTIC: domestic games ship without a centre coin mechanism, so the input is optional; the wiring is still in the harness.",
	6: "Coin-door left coin chute 7SW6; S11.VBS calls it swCoin1.",
	7: "Coin-door slam tilt 7SW7.",
	8: "Coin-door high-score reset button 7SW8; the control-locations page puts it on the back of the coin door.",
	9: "Spinner B-8307 on the left, which also spots the S of S-O-R-C-E-R-E-R. A spinner closes this contact briefly once per revolution; the retained script pulses it from sw9_Spin.",
	16: "Spinner B-8307 on the right, which also spots the last R of S-O-R-C-E-R-E-R; the retained script pulses it from sw16_Spin.",
	21: "Jet-bumper skirt switch. PinMAME's sxx.ssSw makes it the trigger of special solenoid 19 (left jet bumper): while the game-on enable 23 is set, a closure publishes 19 (switch-test and gameplay runs). On the machine the bumper's own special switch on 1J18 fires the coil through the CPU board, and this matrix contact scores.",
	22: "Jet-bumper skirt switch, trigger of special solenoid 20 (lower jet bumper) through PinMAME's sxx.ssSw; the switch-test and gameplay runs show 20 following a closure.",
	23: "Jet-bumper skirt switch, trigger of special solenoid 21 (right jet bumper) through PinMAME's sxx.ssSw; the switch-test and gameplay runs show 21 following a closure.",
	28: "Outhole switch A-10417. A ball resting here makes the ROM fire the outhole kicker (1), which lifts it onto the ball ramp (gameplay run).",
	29: "The upper of the two ball-ramp (trough) positions, the manual's Ramp 1. The retained script holds 29 and 30 closed at boot with both balls home.",
	30: "The lower ball-ramp position next to the ramp eject, the manual's Ramp 2. The ROM serves from here with the ramp eject (2) into the shooter lane.",
	31: "Shooter-lane switch B-8677; closed while a served ball waits at the plunger.",
	32: "Left kicker (slingshot) switch B-8284, trigger of special solenoid 17 through PinMAME's sxx.ssSw (switch-test and gameplay runs). The retained script pulses it from LeftSlingShot_Slingshot.",
	33: "Right kicker (slingshot) switch B-8284, trigger of special solenoid 18 through PinMAME's sxx.ssSw. The retained script pulses it from RightSlingShot_Slingshot.",
	34: "Drop target A-9417 in the 3-bank; the contact latches closed while the target is down and opens when the reset bar (4) raises it.",
	35: "Drop target A-9417 in the 3-bank; latches closed while down.",
	36: "Drop target A-9417 in the 3-bank; latches closed while down.",
	37: "The multi-ball lock: the matrix calls it Multi-Ball Ramp and the switch-location list Ramp Eject for MULTIBALL (A-10590). A ball resting here is locked and the ROM serves the next ball (gameplay run); the multi-ball eject (3) kicks it out. The retained script models it as the saucer sw37.",
	38: "The ramp switch for MULTIBALL (A-8659), on the ramp behind the lock. A second ball resting here while a ball is locked on 37 makes the ROM fire the multi-ball eject (3) and start multiball (gameplay run).",
	39: "Rebound switch A-4834-K on the lower right; the retained script pulses it from a rubber sensor (Phys_RB_Sensor_sw39).",
	40: "Rebound switch A-4834-K on the lower left (Phys_RB_Sensor_sw40 in the retained script).",
	42: "Rebound switch A-4834-K on the upper left (Phys_RB_Sensor_sw42 in the retained script).",
	43: "The matrix prints Lane Switch and the switch-location list Lamp Shift for this A-4834-J rebound switch at the top of the playfield, two names for one device (Phys_RB_Sensor_sw43 in the retained script).",
	44: (
		"Lane Change switch B-9951. The switch-location drawing's balloon 44 points at the right flipper, so this is a contact operated with the right flipper rather than a cabinet button, and the ROM uses it to change the lit lane. "
		"The driver declares FLIP_SWNO(0,44) with no FLIP_SOL, so with keyboard handling off core_updateSw copies PinMAME flipper-column button 82 into this address on every update: drive 82, not 44. "
		"The gameplay run shows 44 at 1 while 82 is held and at 0 while 84 is held. The retained script also writes 44 directly from the right flipper key; that write is overwritten on the next update and has no lasting effect."
	),
	45: "Playfield tilt B-8306. One closure tilts the ball in the gameplay run (game-on 23 drops at the first closure). The retained script does not model it.",
}
DRAIN_LANES = {24: "left", 25: "right"}

# Placements that are not a measured switch contact or coil: the table object they sit on.
PROJECTIONS = {
	("switch", 21): "Placed on the Bumper1 jet-bumper centre the script binds to 21, not on its skirt contact.",
	("switch", 22): "Placed on the Bumper3 jet-bumper centre the script binds to 22, not on its skirt contact.",
	("switch", 23): "Placed on the Bumper2 jet-bumper centre the script binds to 23, not on its skirt contact.",
	("switch", 28): "Placed on the Drain kicker, the table's outhole ball-collection object, not on the contact itself.",
	("switch", 29): "Placed on the Slot1 kicker, the table's upper ball-ramp position.",
	("switch", 30): "Placed on the BallRelease kicker, the table's ball-ramp exit position.",
	("switch", 32): "Placed on the mean of the LeftSlingshot wall's drag points, a projection onto the slingshot rather than its leaf contacts.",
	("switch", 33): "Placed on the mean of the RightSlingshot wall's drag points, a projection onto the slingshot rather than its leaf contacts.",
	("switch", 34): "Placed on the mean of the sw34 drop-target wall's drag points.",
	("switch", 35): "Placed on the mean of the sw35 drop-target wall's drag points.",
	("switch", 36): "Placed on the mean of the sw36 drop-target wall's drag points.",
	("switch", 37): "Placed on the sw37 kicker, the table's lock kick-out hole.",
	("switch", 39): "Placed on the mean of the Phys_RB_Sensor_sw39 rubber wall's drag points, a projection onto the rubber the rebound switch sits behind.",
	("switch", 40): "Placed on the mean of the Phys_RB_Sensor_sw40 rubber wall's drag points, a projection onto the rubber the rebound switch sits behind.",
	("switch", 42): "Placed on the mean of the Phys_RB_Sensor_sw42 rubber wall's drag points, a projection onto the rubber the rebound switch sits behind.",
	("switch", 43): "Placed on the mean of the Phys_RB_Sensor_sw43 rubber wall's drag points, a projection onto the rubber the rebound switch sits behind.",
	("switch", 44): "Placed on the RightFlipper pivot, the part the switch-location drawing's balloon 44 points at; the switch itself is on the flipper mechanism.",
	("solenoid", 1): "Effect placed on the Drain kicker (outhole), not a measured coil centre.",
	("solenoid", 2): "Effect placed on the BallRelease kicker (ball-ramp exit), not a measured coil centre.",
	("solenoid", 3): "Effect placed on the sw37 kicker (lock kick-out hole), not a measured coil centre.",
	("solenoid", 4): "Effect placed on the centre drop target (sw35 wall), not a measured reset-coil centre.",
	("solenoid", 6): "Emitter placed on the F6 light, the table's light source for the 3-bank flash; no factory drawing numbers the flash lamps.",
	("solenoid", 7): "Emitter placed on the F7 light, the table's light source for the S-O-R-C-E-R-E-R bank flash; no factory drawing numbers the flash lamps.",
	("solenoid", 17): "Effect placed on the mean of the LeftSlingshot wall's drag points.",
	("solenoid", 18): "Effect placed on the mean of the RightSlingshot wall's drag points.",
	("solenoid", 19): "Effect placed on the Bumper1 jet-bumper centre.",
	("solenoid", 20): "Effect placed on the Bumper3 jet-bumper centre.",
	("solenoid", 21): "Effect placed on the Bumper2 jet-bumper centre.",
}


def disclose(item: dict, kind: str, address: int, geometry: dict | None) -> None:
	if geometry is not None and (kind, address) in PROJECTIONS and "spatial" in item and "placements" in item["spatial"]:
		item["physical"]["notes"] = item["physical"]["notes"].rstrip() + " " + PROJECTIONS[(kind, address)]


def build_inputs(geometry: dict | None) -> list[dict]:
	result = []
	for address, identifier, label, location, note in (
		(-7, "switch.advance", "Advance", "coin door", "The coin-door ADVANCE button 7SW75 on the cabinet sheet, wired to CPU 1J14-3 (GRN). PinMAME constant S11_SWADVANCE, a direct input outside the 8x8 matrix. The diagnostic runs step every test with it."),
		(-6, "switch.auto-up-manual-down", "Auto-Up / Manual-Down", "coin door", "The coin-door AUTO-UP / MANUAL-DOWN switch 7SW74, wired to CPU 1J14-4 (BLU). Public 1 is Auto-Up; the solenoid-test runs hold a step with 0. PinMAME constant S11_SWUPDN."),
		(-5, "switch.cpu-diagnostic", "CPU Diagnostic", "backbox, CPU board", "The CPU board's DIAGNOSTIC SWITCH SW1, on the CPU's NMI line; it starts the memory-chip test. PinMAME constant S11_SWCPUDIAG."),
		(-4, "switch.sound-diagnostic", "Sound Diagnostic", "backbox, CPU board", "The CPU board's sound DIAGNOSTIC SWITCH SW2 near the batteries, which starts the sound-section test. PinMAME constant S11_SWSOUNDDIAG."),
	):
		result.append({"id": identifier, "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": address},
		               "aliases": aliases("pinmame.switch", address), "availability": "used", "normally_closed": False,
		               "physical": {"location": location, "switch_type": "other" if address == -6 else "button", "notes": note},
		               "provenance": provenance(MANUAL, CORE, PROFILE, RUNTIME_SOURCE), "roles": [f"service.{identifier.split('.')[1]}"],
		               "spatial": na("cabinet_or_service", MANUAL, CORE)})

	matrix_ids = {}
	for address in range(1, 65):
		wiring = switch_wiring(address)
		if address in data.UNUSED_SWITCHES:
			identifier = f"switch.unused-{address}"
			note = ("The matrix and the switch-location list both print Not Used. " +
			        ("The ROM's switch test still reports a closure here as 41; recognition by the ROM is not a fitted contact." if address == 41 else
			         "The ROM's switch test shows nothing for a closure here, so the ROM does not scan this position."))
			result.append({"id": identifier, "label": f"Not Used ({address})", "kind": "switch",
			               "binding": {"group": "pinmame.input.switch", "device": address}, "aliases": aliases("pinmame.switch", address),
			               "availability": "unused", "physical": {"location": "no fitted switch", "notes": note}, "wiring": wiring,
			               "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE), "spatial": na("unused", MANUAL, RUNTIME_SOURCE)})
			matrix_ids[address] = identifier
			continue
		label, literal, function, assembly, switch_type, location = data.SWITCHES[address]
		identifier = "switch." + slug(label)
		matrix_ids[address] = identifier
		note = SWITCH_NOTES.get(address, "")
		if address in DRAIN_LANES:
			note = f"Outlane rollover B-8410 on the {DRAIN_LANES[address]}; the manual calls the outlanes drains."
		elif address in range(10, 16):
			note = f"Standup target A-9267 in the S-O-R-C-E-R-E-R row; it spots letter {literal}."
		elif address in range(17, 21):
			note = f"Top-lane rollover B-8410 that spots {literal} of A-B-C-D (manual game play: A-B-C-D advances the bonus multiplier)."
		elif address in (26, 27):
			note = f"Flipper return lane rollover B-8410 on the {'left' if address == 26 else 'right'}; completing the 3-bank lights one return lane."
		note = (note + " " if note else "") + (
			f"Printed matrix cell '{literal}', switch-location item '{function}'. Normally open: System 9 reads the matrix uninverted "
			"(s11.c pia4a_r through core_getSwCol, invSw zero) and the ROM's switch test reports this address while it is held at public 1.")
		physical = {"location": "cabinet" if location == "cabinet" else "playfield", "switch_type": switch_type, "notes": note}
		if assembly != "BLANK FOR DOMESTIC":
			physical["part_number"] = assembly
		item = {"id": identifier, "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": address},
		        "aliases": aliases("pinmame.switch", address), "availability": "optional" if address == 5 else "used",
		        "normally_closed": False, "physical": physical, "wiring": wiring,
		        "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE, *(() if address in data.CABINET_SWITCHES or address == 45 else (SCRIPT,)))}
		if address in data.CABINET_SWITCHES:
			item["spatial"] = na("cabinet_or_service", MANUAL)
		else:
			spatial = located(identifier, "sensor", anchors(geometry, "switch", address), geometry)
			if spatial:
				item["spatial"] = spatial
				disclose(item, "switch", address, geometry)
		if address == 1:
			item["roles"] = ["cabinet.tilt"]
		elif address == 3:
			item["roles"] = ["cabinet.start"]
		elif address in (4, 5, 6):
			item["roles"] = [f"cabinet.coin-{ {6: 1, 5: 2, 4: 3}[address] }"]
		elif address == 7:
			item["roles"] = ["cabinet.slam-tilt"]
		elif address == 28:
			item["initial_active"] = False
		elif address in (29, 30):
			item["initial_active"] = True
		result.append(item)

	for address in FLIPPER_COLUMN_ADDRESSES:
		base = (f"PinMAME flipper switch column (CORE_FLIPPERSWCOL, internal column 11), published at {address} through "
		        "core_swSeq2m(n) = n + 7.")
		if address == 82:
			result.append({"id": flipper_column_id(82), "label": "Right Flipper Button (PinMAME Flipper Column)", "kind": "switch",
			               "binding": {"group": "pinmame.input.switch", "device": 82}, "aliases": aliases("pinmame.switch", 82, padded=False),
			               "availability": "used", "normally_closed": False, "roles": ["flipper.lower.right.button"],
			               "physical": {"location": "cabinet flipper button", "switch_type": "button", "notes": base + " This is the right cabinet flipper button (7SW72) as the ROM receives it. The driver declares FLIP_SWNO(0,44) with no FLIP_SOL, so with keyboard handling off core_updateSw reads this bit as the host wrote it, copies it into matrix switch 44 (Lane Change) on every update and fabricates the synthetic 45/46 while the enable 23 is on; the gameplay run shows all three. S11.VBS writes it as swLRFlip."},
			               "provenance": provenance(CORE, PROFILE, LIBRARY, RUNTIME_SOURCE, MANUAL), "spatial": na("cabinet_or_service", CORE, MANUAL)})
		elif address == 84:
			result.append({"id": flipper_column_id(84), "label": "Left Flipper Button (PinMAME Flipper Column)", "kind": "switch",
			               "binding": {"group": "pinmame.input.switch", "device": 84}, "aliases": aliases("pinmame.switch", 84, padded=False),
			               "availability": "used", "normally_closed": False, "roles": ["flipper.lower.left.button"],
			               "physical": {"location": "cabinet flipper button", "switch_type": "button", "notes": base + " This is the left cabinet flipper button (7SW73), which also closes the upper-left flipper contact. FLIP_SWNO(0,44) gives the left side no matrix switch, so core_updateSw copies this bit nowhere; it only fabricates the synthetic 47/48 while the enable 23 is on (gameplay run). S11.VBS writes it as swLLFlip."},
			               "provenance": provenance(CORE, PROFILE, LIBRARY, RUNTIME_SOURCE, MANUAL), "spatial": na("cabinet_or_service", CORE, MANUAL)})
		else:
			kind = "end-of-stroke" if address % 2 else "button"
			result.append({"id": flipper_column_id(address), "label": f"Unused Flipper Column {kind.title()} ({address})", "kind": "switch",
			               "binding": {"group": "pinmame.input.switch", "device": address}, "aliases": aliases("pinmame.switch", address, padded=False),
			               "availability": "unused",
			               "physical": {"location": "internal public address space", "switch_type": "other", "notes": base + " FLIP_SWNO(0,44) sets no FLIP_EOS, FLIP_SOL or upper FLIP_SW bit, so core_updateSw neither synthesizes nor copies this bit, and s11.c's pia4a_r reads only matrix columns 1-8: the ROM cannot see it. PinMAME models no end-of-stroke switch on this machine." + (" S11.VBS names it swURFlip/swULFlip, constants that do not follow this column." if address in (81, 83) else "")},
			               "provenance": provenance(CORE, PROFILE), "spatial": na("unused", CORE)})

	result.append({"id": "dip.jumper-w5", "label": "Country Jumper W5 (fitted)", "kind": "dip_switch",
	               "binding": {"group": "pinmame.input.dip", "device": 0}, "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
	               "availability": "used",
	               "physical": {"location": "backbox, CPU board", "switch_type": "dip", "notes": "PinMAME's pia2a_r returns core_getDip(0)<<7 for PIA 2800 port A. On the System 9 CPU schematic that is U5's PA7, pulled up through SR14-10 and tied to ground by jumper W5, which the manual lists among the jumpers that should be connected. A fitted W5 reads 0, PinMAME's default for this game."},
	               "provenance": provenance(CORE, MANUAL, PROFILE), "spatial": na("dip_switch", MANUAL)})
	return result, matrix_ids


# ---------------------------------------------------------------- outputs

SOLENOID_IDS = {1: "coil.outhole-kicker", 2: "coil.ramp-eject", 3: "coil.multi-ball-eject", 4: "coil.three-bank-drop-target-reset",
                5: "flasher.demon-background", 6: "flasher.three-bank", 7: "flasher.sorcerer-bank", 8: "relay.flash-eyes",
                11: "relay.special-relay-general-illumination", 15: "coil.bell", 16: "coil.coin-lockout",
                17: "coil.left-kicker", 18: "coil.right-kicker", 19: "coil.left-jet-bumper", 20: "coil.lower-jet-bumper", 21: "coil.right-jet-bumper"}
SOLENOID_LABELS = {1: "Outhole Kicker", 2: "Ramp Eject (Ball Ramp Release)", 3: "Multi-Ball Eject", 4: "3-Bank Drop Target Reset",
                   5: "Demon Background Flashers", 6: "3-Bank Flashers", 7: "SORCERER Bank Flashers", 8: "Flash Eyes Relay",
                   11: "Special Relay K1 (General Illumination)", 15: "Bell", 16: "Coin Lockout Coil",
                   17: "Left Kicker (Slingshot)", 18: "Right Kicker (Slingshot)", 19: "Left Jet Bumper", 20: "Lower Jet Bumper", 21: "Right Jet Bumper"}
SOLENOID_KINDS = {5: "flasher", 6: "flasher", 7: "flasher", 8: "relay", 11: "relay"}
SOLENOID_NOTES = {
	1: "Kicks a drained ball from the outhole (28) up onto the ball ramp (29/30). The gameplay run shows one pulse per outhole closure.",
	2: "The ball-ramp release: kicks the ball on Ramp 2 (30) into the shooter lane (31). The manual's 'ramp' is the ball trough; the retained script names the callback SolBallRelease. The ROM serves with it at game start, after a lock and after a drain.",
	3: "Kicks the locked ball out of the multi-ball lock (37). The gameplay run fires it when a second ball rests on the ramp switch 38 behind the locked ball.",
	4: "Raises the three targets of the 3-bank (34-36). The ROM fires it at game start and when the bank is completed (gameplay run).",
	5: "#63 flash lamps behind the Demon art (Demon Background). The table's solenoid type 'controlled' and PinMAME's #89 bulb model for 5-7 both treat it as a lamp load, not a coil; the coil parts list prints NOT USED for 5-7 because it lists coils only. Bulb count is not printed.",
	6: "#63 flash lamps at the 3-bank drop targets. The gameplay run flashes it with the 3-bank effects.",
	7: "#63 flash lamps at the S-O-R-C-E-R-E-R target bank. The gameplay run flashes it when the word is completed.",
	8: (
		"Relay 5580-08994-00 that flashes the Sorcerer's eyes: the game's solenoid table prints 'Flash Eyes (cabinet)', IPDB describes glowing/flashing Sorcerer's eyes in the back panel, the retained script drives the back-panel eye flashers and a backbox flasher from it, and the gameplay runs show the ROM flashing it in bursts with game effects (SORCERER completed, lanes, lock, credit award) while never holding it through play. "
		"The coil parts list prints 'Flipper-Enable Relay' for item 8 with the same part number; on System 9 the flipper relay is K1 on the CPU board, switched with the game-on enable 23 (CPU schematic), so that label is a parts-list error, not a second device. PinMAME's pwm block leaves 8 untyped for the same reason. The eye bulbs the relay switches are not counted in the manual."
	),
	11: (
		"Drives relay K1 on the D-8345 power supply (3J7 SPECIAL RELAY, pin 1 SOL 11), which switches the 6.3 VAC general-illumination strings on 3J8 (GEN. ILLUM. OUT), including the three coin-door lamps on the cabinet sheet. "
		"Public 1 energizes the relay and turns the GI off: PinMAME types 11 as a reversed 6.3 V AC GI output and the retained script's SolGi turns the GI off while it is on. The gameplay run blinks it with game effects. "
		"Bulb positions and the string split between playfield and backbox are not printed in the retained manual."
	),
	15: "Cabinet bell SM-29-1000-DC (7L15, diode 7D15), BRN-VIO on 7J1-17. The ROM rings it on the 3-bank completion and on a credit award (gameplay and special-award runs).",
	16: "Coin lockout coil SM-35-4000-DC (7L16) behind the coin door; energized while credits may be accepted (active at boot and during the runs).",
}
LAMP_MISPRINTS = {
	22: ("The manual's lamp tables and lamp drawing call public 22 Bonus Hold Over and number the Demon triangle at the 3-bank 23, but the ROM leaves 22 dark until S-O-R-C-E-R-E-R is completed, then lights it until the 3-bank is completed (gameplay run, checked by tools/summarize_sorcerer_runtime.py), which is the manual's own game-play rule for DEMON; IPDB describes the same rule and the known-working script binds 22 to the triangle at the 3-bank. "
	     "Those independent sources settle it: public 22 is the Demon lamp, and the printed 22/23 names are swapped. The literal cells stay in the excerpts."),
	23: ("The manual's lamp tables and lamp drawing call public 23 Demon and number the large round insert below the centre 22, but the ROM lights 23 when the 3-bank is completed with 22 lit and keeps it lit into the next ball (gameplay run), which is the manual's rule for BONUS HELD OVER; the known-working script binds 23 to that round insert. "
	     "Public 23 is the Bonus Hold Over lamp, and the printed 22/23 names are swapped."),
}
SCRIPT_SOLENOIDS = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 11, 15})
SPECIAL_SWITCH = {17: 32, 18: 33, 19: 21, 20: 22, 21: 23}


def build_outputs(geometry: dict | None) -> list[dict]:
	result = []
	for address in range(1, 65):
		binding = {"group": "pinmame.output.solenoid", "device": address}
		if address in data.SOLENOIDS:
			function, sol_type, wire, cpu, field, transistor, part = data.SOLENOIDS[address]
			wiring = {"board": "System 9 CPU Board D-10534", "driver_transistor": transistor, "drive_connection": f"{cpu}; {field}", "drive_wire": wire}
			if address in data.UNUSED_SOLENOIDS:
				note = f"The solenoid table prints Not Used ({sol_type}, {transistor}) and the coil parts list NOT USED."
				if address == 14:
					note += (" The table's part-number cell carries SA-4-23-850-DC and its playfield cell 8P3-14, but the function is Not Used, the coil list prints NOT USED and the cabinet sheet ends SOL.14 (Q59) at 1P12-7 NC, so no load is fitted. "
					         "The ROM still pulses 14 once when it awards a credit (special-award run), the knocker routine of a game that ships without a knocker; the retained script plays a knocker sound from it (SolKnocker), a recreation choice rather than a fitted device.")
				elif address == 22:
					note += " Special #6 has a driver (Q85) and a trigger input (1J18-9) on the board, but PinMAME's sxx.ssSw slot for 22 is 0 and no switch fires it."
				else:
					note += " The solenoid test sweeps it with the others; the sweep is not fitment."
				result.append({"id": f"coil.not-used-{address}", "label": f"Not Used ({transistor})", "kind": "coil", "binding": binding,
				               "aliases": aliases("pinmame.solenoid", address), "availability": "unused",
				               "physical": {"location": "no fitted load", "notes": note}, "wiring": wiring,
				               "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE), "spatial": na("unused", MANUAL, RUNTIME_SOURCE)})
				continue
			identifier = SOLENOID_IDS[address]
			note = SOLENOID_NOTES.get(address, "")
			if address in SPECIAL_SWITCH:
				sp_wire, sp_cpu, sp_field = data.SPECIAL_SWITCH_WIRING[address]
				note = (f"{sol_type.capitalize()} (SP SOL.-{address - 16}): on the machine its own special switch ({sp_wire}, {sp_cpu}, {sp_field}) fires it through the CPU board while the game-on enable 23 is set. "
				        f"PinMAME publishes it whenever matrix switch {SPECIAL_SWITCH[address]} closes while 23 is set (sxx.ssSw), which the switch-test and gameplay runs show; the solenoid test does not step it, as the manual says.")
			note += f" Solenoid table: '{function}', {sol_type}, {wire}, {cpu}, {field}, {transistor}, {part}."
			if address == 16:
				note = note.replace("1P12-9,", "1P12-9 (printed so; every other controlled row reads 1J12-n),")
			physical = {"notes": note}
			if part and not part.startswith("#"):
				physical["part_number"] = part
			location = "cabinet" if address in (15, 16) else ("cabinet and playfield back panel" if address == 8 else ("backbox, power supply board" if address == 11 else "playfield"))
			physical["location"] = location
			item = {"id": identifier, "label": SOLENOID_LABELS[address], "kind": SOLENOID_KINDS.get(address, "coil"), "binding": binding,
			        "aliases": aliases("pinmame.solenoid", address), "availability": "used", "physical": physical, "wiring": wiring,
			        "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE, *((RUNTIME_L1_SOURCE,) if address <= 16 else ()), *((SCRIPT,) if address in SCRIPT_SOLENOIDS else ()))}
			if address in (15, 16):
				item["spatial"] = na("cabinet_or_service", MANUAL)
			elif address == 8:
				item["spatial"] = na("cabinet_or_service", MANUAL)
			elif address == 11:
				item["roles"] = ["cabinet.general-illumination-relay"]
				item["spatial"] = na("cabinet_or_service", MANUAL)
			else:
				spatial = located(identifier, "emitter" if address in (5, 6, 7) else "effect", anchors(geometry, "solenoid", address), geometry)
				if spatial:
					item["spatial"] = spatial
					disclose(item, "solenoid", address, geometry)
			result.append(item)
			continue
		if address == 23:
			result.append({"id": "relay.game-on-flipper-enable", "label": "Game On (Flipper Relay K1 and Special Solenoid Enable)", "kind": "relay", "binding": binding,
			               "aliases": aliases("pinmame.solenoid", address), "availability": "used", "roles": ["cabinet.flipper-enable-relay"],
			               "physical": {"location": "backbox, CPU board", "notes": "PinMAME's S11_GAMEONSOL: the special-solenoid and flipper enable, published while the ROM enables play. The System 9 CPU schematic draws relay K1 (SA-8994) on the CPU board, switched by Q86 from the same 7402 gating as the special-solenoid drivers; its contacts carry solenoid ground onto 1J19-1 and 1J19-2, the flipper grounds of the cabinet buttons. The gameplay run shows 23 rising at game start and dropping at the tilting playfield-tilt closure; the switch-test run shows it set throughout diagnostics. The manual's 'flipper relay is de-energized with sub-test 25' is the generic System 9 text: this ROM's solenoid test stops at 16."},
			               "provenance": provenance(CORE, PROFILE, MANUAL, RUNTIME_SOURCE), "spatial": na("cabinet_or_service", MANUAL, CORE)})
			continue
		if address in (45, 46, 47, 48):
			side = "Right" if address < 47 else "Left"
			power = address in (45, 47)
			flippers = "the right flipper (FL23/600-30/2600-50VDC)" if side == "Right" else "the lower-left flipper (FL23) and the top flipper (FL24/600-30/2600-50VDC), both wired to the left button"
			result.append({"id": f"virtual.{side.lower()}-flipper-{'power' if power else 'hold'}-synthetic", "label": f"{side} Flipper {'Power' if power else 'Hold'} (synthetic)",
			               "kind": "virtual", "binding": binding, "aliases": aliases("pinmame.solenoid", address), "availability": "used",
			               "physical": {"notes": f"PinMAME fabricates this state from flipper-column button {82 if side == 'Right' else 84} while the game-on enable 23 is set, because the driver declares no FLIP_SOL; both of the pair assert together (gameplay run). There is no CPU driver behind it: the cabinet button switches {flippers} directly through relay K1. A recreation drives those flippers from this pair."},
			               "provenance": provenance(CORE, PROFILE, MANUAL, RUNTIME_SOURCE, SCRIPT), "spatial": na("virtual", CORE)})
			continue
		reasons = {24: "Reserved System 9/11 public output between the game-on enable and the C-side range; the driver populates nothing here.",
		           49: "CORE_FIRSTSIMSOL: the simulator's fake ball-shooter solenoid; nothing on this machine drives it."}
		if address in reasons:
			note = reasons[address]
		elif 25 <= address <= 32:
			note = "C-side relay alias: sxx.muxSol is 0 for Sorcerer, so updsol never copies 1-8 here and the machine has no A/C relay."
		elif 33 <= address <= 36:
			note = "Generic upper-flipper range; core_getSol serves it only on WPC and SAM generations, so it reads 0 on System 9."
		elif 37 <= address <= 44:
			note = "Sound-overlay/printer range; Sorcerer's gameSpecific1 is 0 (no S11_SNDOVERLAY or S11_PRINTERLINE), so nothing is published here."
		else:
			note = "Custom-solenoid space; the driver declares custSol 0, so PinMAME publishes no output here." if address >= 51 else "Unassigned gap below the custom-solenoid base."
		result.append({"id": f"virtual.solenoid-{address}", "label": f"Unused Solenoid {address}", "kind": "virtual", "binding": binding,
		               "aliases": aliases("pinmame.solenoid", address), "availability": "unused", "physical": {"notes": note},
		               "provenance": provenance(CORE, PROFILE, RUNTIME_SOURCE), "spatial": na("unused", CORE)})

	for address in range(1, 65):
		label, literal, function, assembly, location = data.LAMPS[address]
		column, row = divmod(address - 1, 8)
		drive_wire, drive = data.LAMP_COLUMNS[column]
		return_wire, ret = data.LAMP_ROWS[row]
		identifier = "lamp." + slug(label)
		note = f"Lamp matrix cell '{literal}', lamp-location item '{function}'."
		if location == "backbox":
			note += " A backbox lamp: the playfield lamp-location drawing carries no balloon for it."
			if address >= 56:
				note += " The lamp matrix names 56-60 Backglass Effect and 61-64 Backglass SORCERER art; the lamp-location list lumps 56-64 under GENERAL ILLUMINATION, a grouping of the backbox lamps, not the GI relay circuit."
		if address in LAMP_MISPRINTS:
			note += " " + LAMP_MISPRINTS[address]
		physical = {"location": "backbox" if location == "backbox" else "playfield", "notes": note}
		if assembly:
			physical["part_number"] = assembly
		item = {"id": identifier, "label": label, "kind": "lamp", "binding": {"group": "pinmame.output.lamp", "device": address},
		        "aliases": aliases("pinmame.lamp", address), "availability": "used", "physical": physical,
		        "wiring": {"board": "System 9 CPU Board D-10534 lamp matrix", "drive_connection": drive, "drive_wire": drive_wire,
		                   "return_connection": ret, "return_wire": return_wire},
		        "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE)}
		if location == "backbox":
			item["spatial"] = na("cabinet_or_service", MANUAL)
		else:
			spatial = located(identifier, "emitter", anchors(geometry, "lamp", address), geometry)
			if spatial:
				item["spatial"] = spatial
				item["physical"]["notes"] += f" Placed on the table's li{address} insert light, the one vpmMapLights binds through its TimerInterval; its li{address}a bloom double is excluded."
		result.append(item)
	return result


# ---------------------------------------------------------------- mechanisms

def build_mechanisms(matrix_ids: dict[int, str], outputs: list[dict]) -> tuple[list[dict], list[dict]]:
	coils = {o["binding"]["device"]: o["id"] for o in outputs if o["binding"]["group"] == "pinmame.output.solenoid"}
	mechanisms, relationships = [], []

	def add(identifier, label, kind, actuators, sensors, behavior, *refs):
		mechanisms.append({"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
		                   "behavior": behavior, "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE, SCRIPT, *refs)})

	add("mech.outhole-and-ball-ramp", "Outhole, two-ball ramp and shooter lane", "kicker",
	    [coils[1], coils[2]], [matrix_ids[28], matrix_ids[29], matrix_ids[30], matrix_ids[31]],
	    "Two balls. A drained ball rolls into the outhole (28); the outhole kicker (1) lifts it onto the ball ramp, where balls rest on Ramp 1 (29) and Ramp 2 (30), the lower one next to the ramp eject. Initialize both ramp positions closed and the outhole open. "
	    "The ramp eject (2) kicks the ball on 30 into the shooter lane, where it rests on 31 until the manual plunger launches it; the ball on 29 then rolls down onto 30. "
	    "The ROM serves at game start (with the 3-bank reset 4), after a ball is locked, and after the last ball in play drains. It keeps firing 2 while 30 stays closed after a serve, so release 30 once the ball has left (the exploratory run that did not do so recorded repeated serves).")
	add("mech.multi-ball-lock", "Ramp lock and multi-ball eject", "kicker",
	    [coils[3]], [matrix_ids[37], matrix_ids[38]],
	    "The ramp shot feeds a kick-out lock (37). The first ball to come to rest on 37 is locked: the ROM flashes the Demon background (5) and the eyes (8) and serves the second ball from the ball ramp (2). "
	    "A second ramp shot leaves that ball resting on the ramp switch (38) behind the locked one; the ROM then fires the multi-ball eject (3), with the 5-8 flashers, and both balls are in play (manual: second time starts MULTI-BALL; each further ramp shot advances the playfield multiplier, lamps 28-30). "
	    "After the eject release 37 and then 38 as the balls roll out. When both balls have drained through the outhole the ROM serves the next ball.")
	add("mech.three-bank-drop-targets", "3-bank drop targets", "drop_target_bank",
	    [coils[4]], [matrix_ids[34], matrix_ids[35], matrix_ids[36]],
	    "Three drop targets (left 34, centre 35, right 36), each latching its normally open switch closed while down. One reset coil (4) raises the bank. The ROM resets it at game start and when all three are down; a host holds the targets down until the reset and then releases them. Completion lights a flipper return lane, awards the flashing value, awards an extra ball when lit and spots bonus held over with Demon lit (manual game play); the gameplay run shows the 3-bank flashers (6), a GI blink (11) and the bell (15) with the reset.")
	for coil, switch, label in ((17, 32, "Left kicker (slingshot)"), (18, 33, "Right kicker (slingshot)"), (19, 21, "Left jet bumper"), (20, 22, "Lower jet bumper"), (21, 23, "Right jet bumper")):
		add(f"mech.{slug(label.split(' (')[0])}", label, "kicker", [coils[coil]], [matrix_ids[switch]],
		    f"The ball closes switch {switch} and the special solenoid {coil} kicks it away; on the machine the device's own special switch fires the coil through the CPU board while the game-on enable 23 is set, and in PinMAME a closure of {switch} publishes {coil} (sxx.ssSw). The solenoid test does not step it. Mechanical strength and recovery are table-owned.")
		relationships.append({"id": f"rel.switch-{switch}-fires-{coil}", "kind": "pulse", "source": matrix_ids[switch], "destination": coils[coil],
		                      "provenance": provenance(CORE, MANUAL, RUNTIME_SOURCE)})
	for switch, side in ((9, "left"), (16, "right")):
		add(f"mech.{side}-spinner", f"{side.title()} spinner", "rotary", [], [matrix_ids[switch]],
		    f"Free-spinning target B-8307; each revolution closes switch {switch} briefly. No coil. It spots the {'S' if switch == 9 else 'last R'} of S-O-R-C-E-R-E-R, and spinner value lamps light after the word is spelled (manual game play).")
	add("mech.right-flipper", "Right flipper and lane change switch", "other", [coils[45], coils[46]], [flipper_column_id(82), matrix_ids[44]],
	    "One 50 V right flipper (FL23/600-30/2600-50VDC) wired to the right cabinet button through relay K1. The B-9951 Lane Change switch on the right flipper closes with it; the ROM changes the lit lane on it. PinMAME takes both from flipper-column button 82: it copies 82 into 44 and fabricates 45/46 while 23 is set. Stroke timing is table-owned.")
	add("mech.left-and-top-flippers", "Left and top flippers", "other", [coils[47], coils[48]], [flipper_column_id(84)],
	    "The left cabinet button has two contacts: one fires the lower-left flipper (FL23) and the other the top flipper (FL24/600-30/2600-50VDC, with an E.O.S. contact drawn on its coil on the playfield sheet), which sits in the centre of the playfield beside the lower jet bumper and which the cabinet sheet calls UPPER LEFT FLIPPER, both through relay K1. PinMAME fabricates 47/48 from button 84 while 23 is set; the left side has no matrix switch. The retained script moves the top flipper (LeftFlipper1) through its own SolULFlipper callback on sULFlipper and the lower-left one through SolLFlipper; S11.VBS's staged-flipper handling fires both from the left flipper key.")
	relationships.append({"id": "rel.flipper-column-82-to-matrix-44", "kind": "direct", "source": flipper_column_id(82), "destination": matrix_ids[44],
	                      "provenance": provenance(CORE, PROFILE, RUNTIME_SOURCE)})
	for address in (45, 46, 47, 48):
		relationships.append({"id": f"rel.game-on-gates-{address}", "kind": "relay_gated", "source": "relay.game-on-flipper-enable", "destination": coils[address],
		                      "provenance": provenance(CORE, MANUAL, RUNTIME_SOURCE)})
	for switch in (34, 35, 36):
		relationships.append({"id": f"rel.reset-raises-{switch}", "kind": "pulse", "source": coils[4], "destination": matrix_ids[switch],
		                      "provenance": provenance(MANUAL, RUNTIME_SOURCE, SCRIPT)})
	return mechanisms, relationships


# ---------------------------------------------------------------- sources

def excerpt_records(root: Path) -> list[dict]:
	records = []
	for excerpt_id, (filename, locator, image) in EXCERPT_FILES.items():
		path = EXCERPTS / filename
		record = {"id": excerpt_id, "locator": locator, "method": "manual", "path": path.as_posix(),
		          "reviewed": True, "sha256": EXCERPT_DIGESTS[excerpt_id], "transcribed_by": "curator"}
		if image:
			digest, derivation = IMAGE_DERIVATIONS[excerpt_id]
			record.update(image=(EXCERPTS / image).as_posix(), image_sha256=digest, image_derivation=derivation)
		records.append(record)
	return records


def build_sources(root: Path, geometry: dict | None) -> list[dict]:
	excerpts = {e["id"]: e for e in excerpt_records(root)}
	manual_ids = ["switch-matrix", "lamp-matrix", "solenoid-table", "location-parts-lists", "operation-and-diagnostics", "backbox-wiring", "cpu-flipper-relay", "cabinet-wiring"]
	runtime = load_json(root / RUNTIME)
	sources = [
		{"id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": data.PINMAME_REVISION,
		 "locator": "Pinned catalog driver records sorcr_l2 (root) and sorcr_l1 (clone)", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/tree/{data.PINMAME_REVISION}", "revision": data.PINMAME_REVISION,
		 "locator": "src/wpc/s11games.c sorcr INITGAMEFULL and driver blocks; src/wpc/s11.c s11_dispS9, pia2a_r, pia4a_r, setSSSol, updsol, sorcr_ PWM block; src/wpc/core.c core_updateSw, core_getSol, core_swSeq2m; s11.h; core.h",
		 "license": "BSD-3-Clause", "attribution": "PinMAME contributors", "excerpts": [excerpts["pinmame-contract"]]},
		{"id": PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
		 "locator": "Williams System 9/11 public address rules: matrix 1-64, diagnostics -7 to -4, flipper column 81-88, solenoids 1-64 with the game-on enable at 23, lamps 1-64, GI on an ordinary solenoid address",
		 "license": "MIT", "attribution": "pinmame-game-defs curation"},
		{"id": MANUAL, "kind": "manual", "uri": "https://www.ipdb.org/files/2242/" + data.MANUAL_FILENAME,
		 "original_filename": data.MANUAL_FILENAME, "sha256": data.MANUAL_SHA256, "acquired_at": "2026-10-16T19:35:00Z",
		 "locator": "Sorcerer Instruction Manual with schematics, 34 pages (Xerox scan), IPDB machine 2242, retrieved through the Internet Archive capture https://web.archive.org/web/20260210164153id_/https://www.ipdb.org/files/2242/Williams_1985_Sorcerer_Instruction_Manual_with_schematics.pdf; retained at external:pinmame-manuals/by-machine/williams.sorcerer.1985/ipdb/. Exact pages in the excerpts.",
		 "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
		 "excerpts": [excerpts[e] for e in manual_ids]},
		{"id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=2242", "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-16T19:35:00Z",
		 "locator": "IPDB machine 2242 through the Internet Archive capture https://web.archive.org/web/20251129044014/https://www.ipdb.org/machine.cgi?id=2242, retained as external:pinmame-manuals/by-machine/williams.sorcerer.1985/ipdb/machine-2242.html: Sorcerer, Williams, March 1985, model number 532, Williams System 9, 3,700 units; notable features flippers (3), pop bumpers (3), slingshots (2), standup targets (6), spinning targets (2), kick-out hole (1), 3-bank drop targets (1), ramp (1), 2-ball multiball, glowing/flashing Sorcerer's eyes in back panel; two playfield colour schemes that differ only in artwork.",
		 "license": "NOASSERTION", "attribution": "The Internet Pinball Database"},
		{"id": SCRIPT, "kind": "vpx_script", "known_working": True, "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_CORPUS_REVISION}/Sorcerer%20%28Williams%201985%29%20v4.0.4.vbs",
		 "revision": SCRIPT_CORPUS_REVISION, "sha256": SCRIPT_SHA256,
		 "locator": "Pinned known-working corpus script for the VPX table version 4.0.4 by UnclePaulie (from the 2018 original by JPSalas): cGameName sorcr_l2, S11.VBS, UseSolenoids 2, vpmMapLights AllLamps. Runtime authority for the solenoid callbacks, switch handlers and ball routing in the excerpt.",
		 "license": "NOASSERTION", "attribution": "UnclePaulie; JPSalas; credited contributors", "excerpts": [excerpts["script-contract"]]},
		{"id": LIBRARY, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "sha256": VPM_S11_SHA256,
		 "locator": "Retained machine-neutral s11.vbs that the table loads with LoadVPM \"01550000\", \"S11.VBS\", 3.26: cabinet constants and the flipper-column buttons swLRFlip 82 and swLLFlip 84.",
		 "license": "NOASSERTION", "attribution": "VPinMAME script library contributors", "excerpts": [excerpts["script-library"]]},
		{"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": RUNTIME.as_posix(), "sha256": sha256(root / RUNTIME), "revision": data.PINMAME_REVISION,
		 "locator": f"Compact evidence recomputed by tools/summarize_sorcerer_runtime.py from four LibPinMAME harness runs of sorcr_l2 (solenoid test, switch test, gameplay, special award), each from a newly initialized state directory, library SHA-256 {data.LIBRARY_SHA256}, ROM archive {data.ROM_SHA256['sorcr_l2']}; raw runs under external:pinmame-review-artifacts/{MACHINE_ID}/harness, manifest SHA-256 {runtime['source']['sha256']}.",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs curation; ROM bytes and NVRAM excluded"},
		{"id": RUNTIME_L1_SOURCE, "kind": "runtime_scenario", "uri": RUNTIME_L1.as_posix(), "sha256": sha256(root / RUNTIME_L1), "revision": data.PINMAME_REVISION,
		 "locator": f"Compact evidence recomputed by tools/summarize_sorcerer_runtime.py from the sorcr_l1 solenoid-test run (ROM archive {data.ROM_SHA256['sorcr_l1']}), retained beside the L-2 runs.",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs curation; ROM bytes and NVRAM excluded"},
	]
	if geometry is not None:
		sources += geometry["sources"]
	if (root / CALLOUTS).is_file():
		sources.append({"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:" + CALLOUTS.as_posix(), "sha256": sha256(root / CALLOUTS),
		                "locator": "2026-10-16 factory location-drawing callout check of the switch (PDF 19), solenoid and lamp (PDF 20) drawings: every callout read independently on gridded tiles of the retained renders without table data, verifier corrections recorded with their reasons, per-page control and callout fits; a table placement whose own callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py).",
		                "license": "NOASSERTION", "attribution": "pinmame-game-defs curation"})
	return sources


# ---------------------------------------------------------------- definition

def build_definition(root: Path = ROOT) -> dict:
	geometry = load_geometry(root)
	if set(data.SWITCHES) | data.UNUSED_SWITCHES != set(range(1, 65)) or set(data.SWITCHES) & data.UNUSED_SWITCHES:
		raise RuntimeError("Sorcerer switch inventory is incomplete or overlapping")
	if set(data.SOLENOIDS) != set(range(1, 23)) or set(data.LAMPS) != set(range(1, 65)):
		raise RuntimeError("Sorcerer solenoid or lamp inventory is incomplete")
	runtime = load_json(root / RUNTIME)
	if runtime["source"]["sha256"] != RUNTIME_MANIFEST_SHA256 or load_json(root / RUNTIME_L1)["source"]["sha256"] != RUNTIME_MANIFEST_SHA256:
		raise RuntimeError("Sorcerer runtime evidence cites an unexpected raw-run manifest")
	inputs, matrix_ids = build_inputs(geometry)
	outputs = build_outputs(geometry)
	mechanisms, relationships = build_mechanisms(matrix_ids, outputs)
	common = "Both drivers select the same sorcrGameData: GEN_S9, s11_dispS9, no A/C relay, FLIP_SWNO(0,44), special switches 32/33/21/22/23, and the same sound and speech ROMs; only the U19/U20 game ROMs differ."
	drivers = [
		{"id": "sorcr_l2", "description": "Sorcerer (L-2)", "year": "1985", "manufacturer": "Williams", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "Production L-2 game software, the retained table's cGameName. " + common + " Service tests, gameplay and the credit award were run on this ROM."},
		{"id": "sorcr_l1", "clone_of": "sorcr_l2", "description": "Sorcerer (L-1)", "year": "1985", "manufacturer": "Williams", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "Earlier production L-1 game software. " + common + " Its solenoid test steps the identical 01-16 sequence (runtime evidence); no L-1 gameplay run is claimed."},
	]
	displays = []
	for index, start, width, identifier, label in (
		(2, 21, 7, "display.player-1", "Player 1 score, seven 7-segment digits with commas (upper left)"),
		(3, 29, 7, "display.player-2", "Player 2 score, seven 7-segment digits with commas (upper right)"),
		(0, 1, 7, "display.player-3", "Player 3 score, seven 7-segment digits with commas (lower left)"),
		(1, 9, 7, "display.player-4", "Player 4 score, seven 7-segment digits with commas (lower right)"),
		(4, 0, 1, "display.credits-left", "Credits, left digit (C-8365 4-digit display)"),
		(5, 8, 1, "display.credits-right", "Credits, right digit (C-8365 4-digit display)"),
		(6, 20, 1, "display.ball-in-play-match-left", "Ball In Play / Match, left digit (C-8365 4-digit display)"),
		(7, 28, 1, "display.ball-in-play-match-right", "Ball In Play / Match, right digit (C-8365 4-digit display)"),
	):
		displays.append({"id": identifier, "label": label, "kind": "segment", "controller_index": index, "segment_start": start, "width": width, "height": 1,
		                 "physical_location": "cabinet_or_service", "provenance": provenance(CORE, MANUAL, RUNTIME_SOURCE),
		                 "spatial": na("cabinet_or_service", MANUAL, CORE)})
	missing = [] if geometry is not None and geometry.get("complete") else ["spatial_placement"]
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Sorcerer", "manufacturer": "Williams", "year": 1985, "model_number": "532", "ipdb_id": 2242,
		            "opdb_id": "G4qxv-MJPyv", "kind": "physical_pinball",
		            **({"playfield": geometry["playfield"]} if geometry is not None else {})},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x800", "inversion_applied_by_emulator": True},
		"coverage": {"status": "partial" if missing else "author_ready", "missing": missing, "dimensions": {
			"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
			"mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "display_inventory": "validated",
			"diagnostic_enumeration": "validated", "runtime_observation": "validated", "causal_exercise": "validated", "emulator_normalization": "validated",
			"spatial_placement": "validated" if not missing else ("observed" if geometry is not None else "unknown")}},
		"drivers": drivers, "inputs": inputs, "outputs": outputs, "displays": displays, "mechanisms": mechanisms, "relationships": relationships,
		"sources": build_sources(root, geometry), "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "complete"}, "conflicts": [],
	}
	if (root / CALLOUTS).is_file():
		drawing_callouts.apply_to_definition(definition, load_json(root / CALLOUTS), CALLOUT_SOURCE)
	return definition


def build_report(definition: dict, root: Path = ROOT) -> dict:
	records = [*definition["inputs"], *definition["outputs"], *definition["displays"]]
	geometry = load_geometry(root)
	return {
		"format": "pinmame-spatial-blockers" if definition["coverage"]["status"] == "partial" else "pinmame-spatial-audit", "version": 1, "machine_id": MACHINE_ID,
		"coordinate_convention": "x=0 left, x=1 right; y=0 rear/backglass, y=1 apron; normalized VPX/player view",
		"geometry_seed": GEOMETRY.as_posix() if geometry is not None else None,
		"geometry_seed_sha256": sha256(root / GEOMETRY) if geometry is not None else None,
		"located": [{"id": r["id"], "label": r["label"], "binding": r["binding"], "placements": r["spatial"]["placements"]}
		            for r in records if isinstance(r.get("spatial"), dict) and "placements" in r["spatial"]],
		"unplaced": [{"id": r["id"], "label": r["label"], "binding": r.get("binding")} for r in records if "spatial" not in r],
		"not_applicable": [{"id": r["id"], "reason": r["spatial"]["reason"]} for r in records if isinstance(r.get("spatial"), dict) and r["spatial"].get("status") == "not_applicable"],
		"projections": [{"kind": kind, "address": address, "disclosure": text} for (kind, address), text in sorted(PROJECTIONS.items())] if geometry is not None else [],
		"callout_check": callout_summary(definition, root),
		"readiness": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"], "unresolved_conflicts": len(unresolved_conflicts(definition))},
	}


def callout_summary(definition: dict, root: Path) -> dict | None:
	if not (root / CALLOUTS).is_file():
		return None
	seed = load_json(root / CALLOUTS)
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition), seed.get("limit", drawing_callouts.LIMIT))
	return drawing_callouts.summary(seed, decisions, CALLOUTS.as_posix(), sha256(root / CALLOUTS))


def render_report(report: dict) -> str:
	lines = [f"# Sorcerer (1985) spatial evidence", "", f"**Decision: {report['readiness']['status']}.** Missing: {', '.join(report['readiness']['missing']) or 'nothing'}.", "",
	         report["coordinate_convention"] + ".", ""]
	if report["geometry_seed"]:
		lines += [f"Geometry seed `{report['geometry_seed']}` SHA-256 `{report['geometry_seed_sha256']}`.", ""]
	else:
		lines += ["No retained table geometry yet: every playfield device is unplaced.", ""]
	lines += ["## Placed devices", "", "| Device | Binding | Placements |", "| --- | --- | --- |"]
	lines += [f"| `{r['id']}` | {r['binding']['group']} {r['binding']['device']} | " + "; ".join(f"({p['x']}, {p['y']}) {p['provenance']['status']}" for p in r["placements"]) + " |" for r in report["located"]]
	check = report["callout_check"]
	if check:
		lines += ["", "## Factory drawing callout check", "", check["rule"], "",
		          f"Seed `{check['seed']}` SHA-256 `{check['seed_sha256']}`: {check['validated']} of {check['checked']} checked placements validated.", ""]
		for key, page in check["pages"].items():
			lines.append(f"- `{key}` ({page['locator']}): {page['controls']} controls, control RMS {page['control_rms']}, {page['callout_fit_pairs']} of {page['callout_pairs']} callout pairs in the fit, leave-one-out max {page['callout_loo_max']}.")
		if check["not_validated"]:
			lines += ["", "Not validated:", ""]
			lines += [f"- `{pid}`: callout {d['label']}" + (f", {d['reason']}" if "reason" in d else f", offsets {d['control_offset']} / {d['callout_offset']}") for pid, d in check["not_validated"].items()]
	if report["projections"]:
		lines += ["", "## Projections", ""] + [f"- {p['kind']} {p['address']}: {p['disclosure']}" for p in report["projections"]]
	lines += ["", "## Unplaced devices", "", "| Device | Label |", "| --- | --- |"]
	lines += [f"| `{r['id']}` | {r['label']} |" for r in report["unplaced"]]
	lines.append("")
	return "\n".join(lines)


# ---------------------------------------------------------------- products

def verify_excerpts(root: Path = ROOT) -> None:
	for excerpt_id, (filename, _locator, image) in EXCERPT_FILES.items():
		path = root / EXCERPTS / filename
		if not path.is_file() or sha256(path) != EXCERPT_DIGESTS[excerpt_id]:
			raise RuntimeError(f"Sorcerer excerpt missing or changed: {path}")
		if image and sha256(root / EXCERPTS / image) != IMAGE_DERIVATIONS[excerpt_id][0]:
			raise RuntimeError(f"Sorcerer excerpt image missing or changed: {image}")


def products(root: Path = ROOT) -> dict[Path, bytes]:
	verify_excerpts(root)
	definition = build_definition(root)
	errors = validate_machine(definition, root)
	if errors:
		raise RuntimeError("Invalid Sorcerer definition: " + "; ".join(errors))
	report = build_report(definition, root)
	path = AUTHOR_READY if definition["coverage"]["status"] == "author_ready" else DEFINITION
	return {path: canonical_bytes(definition), KNOWLEDGE: (root / KNOWLEDGE_SEED).read_bytes(),
	        REPORT: canonical_bytes(report), REPORT_MD: render_report(report).encode("utf-8")}


def check(root: Path = ROOT) -> None:
	result = products(root)
	stale = DEFINITION if AUTHOR_READY in result else AUTHOR_READY
	if (root / stale).exists():
		raise RuntimeError(f"Sorcerer has a stale opposing-status record: {stale}")
	for path, payload in result.items():
		if not (root / path).is_file() or (root / path).read_bytes() != payload:
			raise RuntimeError(f"Sorcerer deterministic artifact missing or drifted: {path}")
	print("Sorcerer definition, knowledge note, excerpts and spatial reports match the deterministic curator.")


def generate(root: Path = ROOT) -> None:
	result = products(root)
	if AUTHOR_READY not in result and (root / AUTHOR_READY).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Sorcerer record with a partial one")
	for path, payload in result.items():
		(root / path).parent.mkdir(parents=True, exist_ok=True)
		(root / path).write_bytes(payload)
	if AUTHOR_READY in result and (root / DEFINITION).exists():
		(root / DEFINITION).unlink()


def verify_evidence(root: Path = ROOT) -> None:
	verify_excerpts(root)
	names = ("PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_VPX_SOURCES_ROOT")
	if any(not os.environ.get(n) for n in names):
		raise RuntimeError("PINMAME_MANUALS_ROOT, PINMAME_REVIEW_ARTIFACTS_ROOT and PINMAME_VPX_SOURCES_ROOT must be configured for --verify-evidence")
	manuals, review, vpx = (Path(os.environ[n]) for n in names)
	geometry = load_geometry(root)
	if geometry is not None:
		from build_external_evidence_manifest import build_manifest, check_manifest
		from pinmame_game_defs.spatial import _item_point
		table = geometry["table"]
		extraction = vpx / table["extraction"]
		if sha256(vpx / table["path"]) != table["sha256"] or sha256(extraction / "script.vbs") != table["embedded_script_sha256"]:
			raise RuntimeError("Sorcerer retained table or embedded script changed")
		manifest = build_manifest(extraction, "sorcr_l2")
		if (check_manifest(extraction, "sorcr_l2"), len(manifest["files"]), sum(f["size"] for f in manifest["files"])) != (table["manifest_sha256"], table["file_count"], table["total_bytes"]):
			raise RuntimeError("Sorcerer table extraction changed")
		for name, obj in geometry["objects"].items():
			raw = load_json(extraction / obj["file"])
			if sha256(extraction / obj["file"]) != obj["file_sha256"] or _item_point(obj["type"], raw.get(obj["type"], raw))[:2] != (obj["x"], obj["y"]):
				raise RuntimeError(f"Sorcerer geometry object drifted: {name}")
	if (root / CALLOUTS).is_file():
		drawing_callouts.verify_retained(load_json(root / CALLOUTS), root, manuals, review)
	folder = manuals / "by-machine" / MACHINE_ID / "ipdb"
	if sha256(folder / data.MANUAL_FILENAME) != data.MANUAL_SHA256 or sha256(folder / "machine-2242.html") != IPDB_PAGE_SHA256:
		raise RuntimeError("Sorcerer retained manual or IPDB page changed")
	if sha256(review / "vpm-script-libs" / "s11.vbs") != VPM_S11_SHA256:
		raise RuntimeError("Retained s11.vbs changed")
	from summarize_sorcerer_runtime import OUTPUTS, build
	if any(canonical_bytes(value) != (root / OUTPUTS[game]).read_bytes() for game, value in build(review / MACHINE_ID / "harness").items()):
		raise RuntimeError("Sorcerer raw runtime evidence disagrees with the compact evidence")
	print("Sorcerer retained manual, IPDB page, script library, raw runs, table geometry and callout renders match the pinned evidence.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	mode.add_argument("--verify-evidence", action="store_true")
	args = parser.parse_args()
	if args.check:
		check()
	elif args.verify_evidence:
		verify_evidence()
	else:
		generate()


if __name__ == "__main__":
	main()
