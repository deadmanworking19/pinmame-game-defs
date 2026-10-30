#!/usr/bin/env python3
"""Deterministic, fail-closed curation of Williams Space Shuttle (1984, System 9).

The reviewed manual tables live in space_shuttle_data.py, the excerpts under
evidence/excerpts/williams.space-shuttle.1984/, the compact runtime evidence in
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
from pinmame_flipper_column import FLIPPER_COLUMN_ADDRESSES, VPM_LIBRARY_SOURCE, VPM_LIBRARY_URI, VPM_S11_SHA256, flipper_column_id
import space_shuttle_data as data

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = data.MACHINE_ID
DEFINITION = Path("machines/partial/williams/space-shuttle-1984.json")
AUTHOR_READY = Path("machines/author-ready/williams/space-shuttle-1984.json")
GEOMETRY = Path("tools/seeds/williams/space-shuttle-1984-geometry.json")
KNOWLEDGE_SEED = Path("tools/seeds/williams/space-shuttle-1984-knowledge.md")
KNOWLEDGE = Path("knowledge/williams/space-shuttle-1984.md")
REPORT = Path("reports/spatial/williams/space-shuttle-1984.json")
REPORT_MD = Path("reports/spatial/williams/space-shuttle-1984.md")
RUNTIME = Path("evidence/runtime/williams/space-shuttle-l7-diagnostics-and-gameplay.json")
RUNTIME_L3 = Path("evidence/runtime/williams/space-shuttle-l3-solenoid-test.json")
EXCERPTS = Path("evidence/excerpts") / MACHINE_ID
REVIEW_FOLDER = "space-shuttle-1984"

CATALOG = "pinmame.catalog.46e1a01a0f73"
CORE = "pinmame.core.46e1a01a0f73"
PROFILE = "controller-profile.pinmame-system-11"
MANUAL = "manual.williams.space-shuttle.1984"
IPDB = "ipdb.2260"
SCRIPT = "vpx-script.space-shuttle.2-0"
LIBRARY = VPM_LIBRARY_SOURCE
RUNTIME_SOURCE = "runtime.space-shuttle.l7-diagnostics-and-gameplay"
RUNTIME_L3_SOURCE = "runtime.space-shuttle.l3-solenoid-test"
TABLE = "vpx-table.space-shuttle.bord"
EXTRACTION = "vpx-extraction.space-shuttle.bord"

SCRIPT_SHA256 = "91e15d488be3f71c40324abbad2612c0b1dbe5f0f9b0813a292b8db1ea3e2ab2"
SCRIPT_CORPUS_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
SCRIPT_CORPUS_PATH = "Space Shuttle (Williams 1984)2.0/Space Shuttle (Williams 1984).vbs"
IPDB_PAGE_SHA256 = "f9cec8f58afaa60bd282a92fb54ffacc337268523d0755e00b810d855fbe7b4e"
RUNTIME_MANIFEST_SHA256 = "1b5e297daab34a7533a3ebe57979f755d0741a10637007b337feb777d29608a9"

# excerpt id: (file, locator)
EXCERPT_FILES = {
	"switch-matrix": ("switch-matrix.md", "Instruction Manual PDF16 (lower half), complete System 9 Switch-Matrix Table"),
	"lamp-matrix": ("lamp-matrix.md", "Instruction Manual PDF16 (upper half), complete System 9 Lamp-Matrix Table"),
	"solenoid-table": ("solenoid-table.md", "Instruction Manual PDF14, complete System-9 Solenoid Table and notes"),
	"location-parts-lists": ("location-parts-lists.md", "Instruction Manual PDF19 Switch Location Diagram, PDF4 Solenoid Location Diagram and PDF20 Lamp Location Diagram parts lists"),
	"playfield-solenoid-wiring": ("playfield-solenoid-wiring.md", "Instruction Manual PDF17, System 9 Playfield-Solenoid & Special-Switch Wiring Diagram"),
	"cpu-connectors": ("cpu-connectors.md", "Instruction Manual PDF18 Back Box Wiring Diagram and PDF25 CPU schematic: 1J6, 1J7, 1J8 and 1J10"),
	"operation-and-diagnostics": ("operation-and-diagnostics.md", "Instruction Manual PDF3 corrections, PDF7 ROM summary, PDF8 game play, PDF10-11 adjustments, PDF13 test procedures"),
	"pinmame-contract": ("pinmame-contract.md", "driver.c 2713-2714; s11games.c 38-41, 64-88; s11.c 194-195, 372, 919-923; s11.h; core.h"),
	"script-contract": ("script-contract.md", "Space Shuttle (Williams 1984).vbs controller bindings"),
	"script-library": ("script-library.md", "s11.vbs lines 23-40 cabinet and flipper constants"),
}
EXCERPT_DIGESTS = {
	"switch-matrix": "9c5393945bda6c3bc15eb2c84a30b84b32266dc16122ea0b4114679347881dc6",
	"lamp-matrix": "920e9e009133f3938b0c58df229799bb25b431a6a33a2e8f107842f200f605de",
	"solenoid-table": "49e5da8383f304448f7fac38880d841889ae9ccc3ffaba128085359098f4c604",
	"location-parts-lists": "bcea4f955bcb639600aa7e6593d1aaf0b2e2748e213c44f765e065e62fa702b4",
	"playfield-solenoid-wiring": "dd2ce4b2bc3d499816233af1b12b36cdd55493c889574d52486b3623f4f5c80b",
	"cpu-connectors": "d8f187cd52c3253470a1cf34a27f539ed2163716637a2be479a3e6f74a779de3",
	"operation-and-diagnostics": "0bb519fd823caa714c8d245a2b1eb40468a3d5ce0f15daad3402bacffdc3b96a",
	"pinmame-contract": "5317673b030a45f0399442553398262abfcd1cb7c8e34f4d41bbc44b66648650",
	"script-contract": "9406d6dc0aa3e20a0c5ecb01ac457c4a9e0c811f460df3e5ae993e3955100519",
	"script-library": "71b05fba56320fd54934ee78a167c5fb92ecada6fb5601f8b4f94edf8575942d",
}
MANUAL_EXCERPTS = ("switch-matrix", "lamp-matrix", "solenoid-table", "location-parts-lists", "playfield-solenoid-wiring", "cpu-connectors", "operation-and-diagnostics")


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


def mesh_centre(obj_path: Path, position: dict, size: dict) -> tuple[float, float]:
	xs, ys = [], []
	for line in obj_path.read_text(encoding="utf-8", errors="replace").splitlines():
		if line.startswith("v "):
			x, y = (float(t) for t in line.split()[1:3])
			xs.append(x)
			ys.append(y)
	return (position["x"] + size["x"] * (min(xs) + max(xs)) / 2, position["y"] + size["y"] * (min(ys) + max(ys)) / 2)


# ---------------------------------------------------------------- inputs

def switch_wiring(address: int) -> dict:
	column, row = divmod(address - 1, 8)
	drive_wire, drive = data.SWITCH_COLUMNS[column]
	return_wire, ret = data.SWITCH_ROWS[row]
	printed = data.SWITCH_ROWS_PRINTED[row]
	wiring = {"board": "System 9 CPU Board D-10534 switch matrix", "drive_connection": drive, "drive_wire": drive_wire,
	          "return_connection": ret, "return_wire": return_wire}
	return wiring, printed


SPECIAL_NOTE = ("PinMAME's sxx.ssSw for sshtl is {{39, 40, 27, 26, 25, 0}}, so a closure of this switch publishes special solenoid {published} while the game-on enable 23 is set (switch-test and gameplay runs). "
                "On the machine this contact shares the {device} with special solenoid {physical} (solenoid table, solenoid and switch location lists, playfield special-switch wiring); "
                "the bumper's own special switch {special} fires that coil through the CPU board without the ROM, and this matrix contact scores. PinMAME's 25/26/27 order is rotated against the machine, so a recreation fires the bumper locally and does not drive it from {published}.")
SWITCH_NOTES = {
	1: "Cabinet plumb-bob tilt. The known-working script's vpmNudge uses it as its tilt switch (TiltSwitch = 1); the manual's tilt paragraph says the third closure (adjustment 29) tilts the ball.",
	2: "Cabinet ball-roll tilt. Space Shuttle sets no S11_MUXSW2, so PinMAME leaves this address to the host; it is not an A/C-relay feedback here.",
	3: "Cabinet credit (start) button; the gameplay runs start each game with it.",
	4: "Coin-door right coin chute; S11.VBS calls it swCoin3.",
	5: "Coin-door centre coin chute. The switch-location list prints its assembly as Blank for Domestic: domestic games ship without a centre coin mechanism, so the input is optional.",
	6: "Coin-door left coin chute; S11.VBS calls it swCoin1. The gameplay runs coin up with it.",
	7: "Coin-door slam tilt; the manual says it returns the game to the Game-Over mode.",
	8: "High-score reset button.",
	9: "Outhole switch. A ball resting here makes the ROM fire the outhole kicker (1), which lifts it onto the ball ramp (gameplay run: one pulse for each of three outhole closures). The switch-location list prints its assembly as A-10417- with a trailing dash and no suffix.",
	10: "The top of the three ball-ramp (trough) positions. The list names it Upper Left Ball Ramp; the switch-location drawing's trough balloons run 12, 11, 10 left to right under the apron, the reverse of the list's names, and the list, the script and the ROM's serve logic agree on 12 being the release position. The retained script holds 10, 11 and 12 closed at boot with three balls home.",
	11: "The middle ball-ramp (trough) position.",
	12: "The lower ball-ramp position next to the ball-ramp release (the list's Lower Right Ball Ramp). The ROM serves from here with the ball-ramp release (2) into the shooter lane.",
	13: "Right outlane rollover. At factory settings the gameplay run shows this closure energizing the outlane gate (13), which the ROM then holds until the 3-bank is completed (Game-Adjustments #4 and #7 change the gate behaviour).",
	14: "Left flipper return lane rollover. In the gameplay run its closure lowered the post (down-post coil 8).",
	15: "Right flipper return lane rollover.",
	16: "Left eject (kick-out) hole. A ball resting here is locked: the ROM flashes the space, shuttle and insert flash lamps (9, 10, 14) and serves another ball (gameplay run); the left eject coil (3) kicks it out at multi-ball.",
	20: "The \"T\" drop target in the centre of the S-H-U-T-T-L-E row; the contact latches closed while the target is down and opens when its reset coil (5) raises it. Hitting it last awards 100,000 bonus (manual game play); IPDB calls it a timed drop target.",
	24: "Right eject (kick-out) hole. A ball resting here is locked and the ROM serves another ball (gameplay run); the right eject coil (4) kicks it out at multi-ball, about 3 s after the left one.",
	28: "Left outlane rollover.",
	32: "The long ramp's upper switch at the top right, where the ramp turns down the right side. With balls locked in both eject holes a closure starts multi-ball: the ROM raises the post (7), fires the left eject (3) at once and the right eject (4) about 3 s later (gameplay run). Ramp shots also ring the bell (15) and, in the credit-award run, posted the replay credit.",
	36: "Shooter-lane switch; closed while a served ball waits at the manual plunger.",
	37: "Spinner; a spinner closes this contact briefly once per revolution and the retained script pulses it from sw37_Spin.",
	38: "Ramp bull's-eye target at the end of the right ramp; it re-selects the S-H-U-T-T-L-E value (manual game play). In the gameplay run the ROM reset the \"T\" drop target (5) after it.",
	39: "Left kicker (slingshot) switch. PinMAME's sxx.ssSw makes it the trigger of special solenoid 17, the left kicker, as on the machine: a closure publishes 17 while the game-on enable 23 is set (switch-test and gameplay runs). The retained script pulses it from LeftSlingShot_Slingshot.",
	40: "Right kicker (slingshot) switch, trigger of special solenoid 18 (the right kicker) through PinMAME's sxx.ssSw, as on the machine. The retained script pulses it from RightSlingShot_Slingshot.",
	41: (
		"Lane change switch B-9951; the switch-location drawing's balloon 41 points at the right flipper, so it is a contact operated with the right flipper rather than a cabinet button, and the ROM moves the lit lane on it (IPDB lists a lane change). "
		"The driver declares FLIP_SWNO(0,41) with no FLIP_SOL, so with keyboard handling off core_updateSw copies PinMAME flipper-column button 82 into this address on every update: drive 82, not 41. The gameplay run shows 41 following 82."
	),
	45: (
		"The long ramp's lower switch. The switch-location drawing draws it dashed (under the ramp) beside the spinner at the ramp entrance, in front of the upper switch 32. "
		"The retained table's sw45 is an invisible trigger on its raised rampswitchwall further up the ramp, behind its sw32, so it marks where the table scores the ramp rather than where the contact is, and this switch carries no placement."
	),
	49: "Playfield tilt. In the L-7 gameplay run two closures did not tilt the ball and the third did, dropping the game-on enable 23 and turning the GI off; the manual's tilt paragraph says the first closure tilts. A recreation follows the ROM. The retained script does not model it.",
}
STANDUPS = {42: "bottom left", 43: "left lower", 44: "left upper", 46: "centre", 47: "upper right", 48: "lower right"}
SHUTTLE_LETTERS = {17: "S", 18: "H", 19: "U", 21: "T", 22: "L", 23: "E"}
TOP_LANES = {29: "U", 30: "S", 31: "A"}
DROP_BANK = {33: "left (lowest)", 34: "centre", 35: "right (highest)"}

# Placements that are not a measured switch contact or coil: the table object they sit on.
PROJECTIONS = {
	("switch", 9): "Placed on the Drain kicker, the table's outhole ball-collection object, not on the contact itself.",
	("switch", 10): "Placed on the Slot3 kicker, the table's top ball-ramp position.",
	("switch", 11): "Placed on the Slot2 kicker, the table's middle ball-ramp position.",
	("switch", 12): "Placed on the Slot1 kicker, the table's ball-ramp exit position.",
	("switch", 16): "Placed on the sw16 kicker, the table's left eject hole.",
	("switch", 20): "Placed on the mean of the sw20 drop-target wall's drag points.",
	("switch", 24): "Placed on the sw24 kicker, the table's right eject hole.",
	("switch", 25): "Placed on the sw25 jet-bumper centre (the left bumper), not on its skirt contact.",
	("switch", 26): "Placed on the sw26 jet-bumper centre (the right bumper), not on its skirt contact.",
	("switch", 27): "Placed on the sw27 jet-bumper centre (the lower bumper), not on its skirt contact.",
	("switch", 33): "Placed on the mean of the sw33 drop-target wall's drag points.",
	("switch", 34): "Placed on the mean of the sw34 drop-target wall's drag points.",
	("switch", 35): "Placed on the mean of the sw35 drop-target wall's drag points.",
	("switch", 39): "Placed on the mean of the LeftSlingShot wall's drag points, a projection onto the slingshot rather than its leaf contacts.",
	("switch", 40): "Placed on the mean of the RightSlingShot wall's drag points, a projection onto the slingshot rather than its leaf contacts.",
	("switch", 41): "Placed on the RightFlipper pivot, the part the switch-location drawing's balloon 41 points at; the switch itself is on the flipper mechanism.",
	("switch", 42): "Placed on the centre of the sw42 collidable sensor mesh's world bounds (primitive vertices times size plus position), the table's rebound/standup sensor.",
	("switch", 43): "Placed on the centre of the sw43 collidable sensor mesh's world bounds.",
	("switch", 44): "Placed on the centre of the sw44 collidable sensor mesh's world bounds.",
	("switch", 46): "Placed on the centre of the sw46 collidable sensor mesh's world bounds.",
	("switch", 47): "Placed on the centre of the sw47 collidable sensor mesh's world bounds.",
	("switch", 48): "Placed on the centre of the sw48 collidable sensor mesh's world bounds.",
	("solenoid", 1): "Effect placed on the Drain kicker (outhole), not a measured coil centre.",
	("solenoid", 2): "Effect placed on the Slot1 kicker (ball-ramp exit), not a measured coil centre.",
	("solenoid", 3): "Effect placed on the sw16 kicker (left eject hole), not a measured coil centre.",
	("solenoid", 4): "Effect placed on the sw24 kicker (right eject hole), not a measured coil centre.",
	("solenoid", 5): "Effect placed on the \"T\" drop target (sw20 wall), not a measured reset-coil centre.",
	("solenoid", 6): "Effect placed on the centre drop target (sw34 wall), not a measured reset-coil centre.",
	("solenoid", 7): "Effect placed on the centre of the centerpost primitive's mesh world bounds (checked against the centerpostcollide wall), the post both post coils drive; not a measured coil centre.",
	("solenoid", 8): "Effect placed on the centre of the centerpost primitive's mesh world bounds, the post both post coils drive; not a measured coil centre.",
	("solenoid", 9): "Emitter placed on the centre of the pHotDogSol9 flash-dome mesh's world bounds, the table's left (space) flash-lamp dome; the solenoid location drawing carries no balloon for the flash lamps.",
	("solenoid", 10): "Emitter placed on the centre of the pHotDogSol10 flash-dome mesh's world bounds, the table's right (shuttle) flash-lamp dome; the solenoid location drawing carries no balloon for the flash lamps.",
	("solenoid", 13): "Effect placed on the bottomgate flipper pivot, the gate the retained script rotates from 13; not a measured coil centre.",
	("solenoid", 17): "Effect placed on the mean of the LeftSlingShot wall's drag points.",
	("solenoid", 18): "Effect placed on the mean of the RightSlingShot wall's drag points.",
	("solenoid", 19): "Effect placed on the sw25 jet-bumper centre (the left bumper).",
	("solenoid", 20): "Effect placed on the sw27 jet-bumper centre (the lower bumper).",
	("solenoid", 21): "Effect placed on the sw26 jet-bumper centre (the right bumper).",
}


def disclose(item: dict, kind: str, address: int, geometry: dict | None) -> None:
	if geometry is not None and (kind, address) in PROJECTIONS and "spatial" in item and "placements" in item["spatial"]:
		item["physical"]["notes"] = item["physical"]["notes"].rstrip() + " " + PROJECTIONS[(kind, address)]


def build_inputs(geometry: dict | None) -> tuple[list[dict], dict[int, str]]:
	result = []
	for address, identifier, label, location, note in (
		(-7, "switch.advance", "Advance", "coin door", "The coin-door ADVANCE button; the manual's test procedures step every test with it. PinMAME constant S11_SWADVANCE, a direct input outside the 8x8 matrix. The diagnostic runs step the solenoid and switch tests with it."),
		(-6, "switch.auto-up-manual-down", "Auto-Up / Manual-Down", "coin door", "The coin-door AUTO-UP / MANUAL-DOWN switch the manual's test procedures use. Public 1 is Auto-Up; the solenoid-test runs hold a step with 0. PinMAME constant S11_SWUPDN."),
		(-5, "switch.cpu-diagnostic", "CPU Diagnostic", "backbox, CPU board", "The CPU board's diagnostic switch that starts the System 9 memory-chip test the manual's corrections sheet refers to. PinMAME constant S11_SWCPUDIAG."),
		(-4, "switch.sound-diagnostic", "Sound Diagnostic", "backbox, CPU board", "The CPU board's sound-section diagnostic switch. PinMAME constant S11_SWSOUNDDIAG; the System 9 controller profile records it."),
	):
		result.append({"id": identifier, "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": address},
		               "aliases": aliases("pinmame.switch", address), "availability": "used", "normally_closed": False,
		               "physical": {"location": location, "switch_type": "other" if address == -6 else "button", "notes": note},
		               "provenance": provenance(MANUAL, CORE, PROFILE, *((RUNTIME_SOURCE,) if address in (-7, -6) else ())),
		               "roles": [f"service.{identifier.split('.')[1]}"], "spatial": na("cabinet_or_service", MANUAL, CORE)})

	matrix_ids = {}
	for address in range(1, 65):
		wiring, printed = switch_wiring(address)
		if address in data.UNUSED_SWITCHES:
			identifier = f"switch.unused-{address}"
			note = ("The switch matrix prints no switch here and the switch-location list prints 50-64 as Not Used. "
			        "The ROM's switch test shows nothing for a closure here (switch-test run), so the ROM does not scan this position.")
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
		if address in SHUTTLE_LETTERS:
			note = f"Standup target A-9618 that spots the {SHUTTLE_LETTERS[address]} of S-H-U-T-T-L-E ({'left' if address < 20 else 'right'} bank)."
		elif address in TOP_LANES:
			note = f"Top-lane rollover that spots the {TOP_LANES[address]} of U-S-A."
		elif address in DROP_BANK:
			note = f"The {DROP_BANK[address]} drop target of the 3-bank along the long ramp's left side; the contact latches closed while the target is down and opens when the reset coil (6) raises the bank."
		elif address in STANDUPS:
			note = f"The {STANDUPS[address]} standup/rebound switch ({assembly})."
		elif address in (25, 26, 27):
			physical = data.PHYSICAL_SPECIAL_SWITCH
			coil = next(sol for sol, switch in physical.items() if switch == address)
			special = data.SPECIAL_SWITCH_WIRING[coil]
			device = {25: "left jet bumper", 26: "right jet bumper", 27: "lower (bottom) jet bumper"}[address]
			note = SPECIAL_NOTE.format(published=data.PINMAME_SPECIAL_SWITCH_SOLENOIDS[address], device=device, physical=coil,
			                           special=f"{special[4]} on CPU 1J18 pin {special[2].split('-')[1]}")
		note = (note + " " if note else "") + (
			f"Printed matrix cell '{literal}', switch-location item '{function}'. Normally open: System 9 reads the matrix uninverted "
			"(s11.c pia4a_r through core_getSwCol, invSw zero) and the ROM's switch test reports this address while it is held at public 1.")
		if printed != wiring["return_connection"]:
			note += (f" The switch-matrix table prints this row's return on {printed}; the CPU schematic and the backbox wiring diagram, which agree, "
			         f"wire it to {wiring['return_connection']}, and the structured wiring follows them.")
		physical = {"location": "cabinet" if location == "cabinet" else "playfield", "switch_type": switch_type, "notes": note}
		if assembly != "Blank for Domestic":
			physical["part_number"] = assembly
		item = {"id": identifier, "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": address},
		        "aliases": aliases("pinmame.switch", address), "availability": "optional" if address == 5 else "used",
		        "normally_closed": False, "physical": physical, "wiring": wiring,
		        "provenance": provenance(MANUAL, CORE, *(() if address == 5 else (RUNTIME_SOURCE,)), *(() if address in data.CABINET_SWITCHES or address == 49 else (SCRIPT,)))}
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
		elif address == 9:
			item["initial_active"] = False
		elif address in (10, 11, 12):
			item["initial_active"] = True
		result.append(item)

	for address in FLIPPER_COLUMN_ADDRESSES:
		base = (f"PinMAME flipper switch column (CORE_FLIPPERSWCOL, internal column 11), published at {address} through "
		        "core_swSeq2m(n) = n + 7.")
		if address == 82:
			result.append({"id": flipper_column_id(82), "label": "Right Flipper Button (PinMAME Flipper Column)", "kind": "switch",
			               "binding": {"group": "pinmame.input.switch", "device": 82}, "aliases": aliases("pinmame.switch", 82, padded=False),
			               "availability": "used", "normally_closed": False, "roles": ["flipper.lower.right.button"],
			               "physical": {"location": "cabinet flipper button", "switch_type": "button", "notes": base + " This is the right cabinet flipper button (ORN-VIO / BLU-VIO on 7P1-7 and 7P1-8) as the ROM receives it. The driver declares FLIP_SWNO(0,41) with no FLIP_SOL, so with keyboard handling off core_updateSw reads this bit as the host wrote it, copies it into matrix switch 41 (Lane Change) on every update and fabricates the synthetic 45/46 while the enable 23 is on; the gameplay run shows all three. S11.VBS writes it as swLRFlip."},
			               "provenance": provenance(CORE, PROFILE, LIBRARY, RUNTIME_SOURCE, MANUAL), "spatial": na("cabinet_or_service", CORE, MANUAL)})
		elif address == 84:
			result.append({"id": flipper_column_id(84), "label": "Left Flipper Button (PinMAME Flipper Column)", "kind": "switch",
			               "binding": {"group": "pinmame.input.switch", "device": 84}, "aliases": aliases("pinmame.switch", 84, padded=False),
			               "availability": "used", "normally_closed": False, "roles": ["flipper.lower.left.button"],
			               "physical": {"location": "cabinet flipper button", "switch_type": "button", "notes": base + " This is the left cabinet flipper button (ORN-GRY / BLU-GRY on 7P1-9 and 7P1-10). FLIP_SWNO(0,41) gives the left side no matrix switch, so core_updateSw copies this bit nowhere; it only fabricates the synthetic 47/48 while the enable 23 is on (gameplay run). S11.VBS writes it as swLLFlip."},
			               "provenance": provenance(CORE, PROFILE, LIBRARY, RUNTIME_SOURCE, MANUAL), "spatial": na("cabinet_or_service", CORE, MANUAL)})
		else:
			kind = "end-of-stroke" if address % 2 else "button"
			result.append({"id": flipper_column_id(address), "label": f"Unused Flipper Column {kind.title()} ({address})", "kind": "switch",
			               "binding": {"group": "pinmame.input.switch", "device": address}, "aliases": aliases("pinmame.switch", address, padded=False),
			               "availability": "unused",
			               "physical": {"location": "internal public address space", "switch_type": "other", "notes": base + " FLIP_SWNO(0,41) sets no FLIP_EOS, FLIP_SOL or upper FLIP_SW bit, so core_updateSw neither synthesizes nor copies this bit, and s11.c's pia4a_r reads only matrix columns 1-8: the ROM cannot see it. PinMAME models no end-of-stroke switch on this machine; the E.O.S. contacts drawn on the two flipper coils are not ROM inputs." + (" S11.VBS names it swURFlip/swULFlip, constants that do not follow this column; Space Shuttle has no upper flipper." if address in (81, 83) else "")},
			               "provenance": provenance(CORE, PROFILE), "spatial": na("unused", CORE)})

	result.append({"id": "dip.jumper-w5", "label": "Country Jumper W5 (fitted)", "kind": "dip_switch",
	               "binding": {"group": "pinmame.input.dip", "device": 0}, "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
	               "availability": "used",
	               "physical": {"location": "backbox, CPU board", "switch_type": "dip", "notes": "PinMAME's pia2a_r returns core_getDip(0)<<7 for PIA 2800 port A, the System 9 CPU board input that jumper W5 ties to ground. The manual's corrections sheet lists W5 among the jumpers that should be connected (W2, W5 through W7, W9 and W12). A fitted W5 reads 0, PinMAME's default for this game, which every runtime run used."},
	               "provenance": provenance(CORE, MANUAL, PROFILE), "spatial": na("dip_switch", MANUAL)})
	return result, matrix_ids


# ---------------------------------------------------------------- outputs

SOLENOID_IDS = {1: "coil.outhole-kicker", 2: "coil.ball-ramp-release", 3: "coil.left-eject-hole", 4: "coil.right-eject-hole",
                5: "coil.t-drop-target-reset", 6: "coil.three-bank-drop-target-reset", 7: "coil.up-post", 8: "coil.down-post",
                9: "flasher.space-flash-lamps", 10: "flasher.shuttle-flash-lamps", 11: "relay.general-illumination",
                13: "coil.outlane-gate", 14: "flasher.insert-flash-lamps", 15: "coil.bell", 16: "coil.coin-lockout",
                17: "coil.left-kicker", 18: "coil.right-kicker", 19: "coil.left-jet-bumper", 20: "coil.lower-jet-bumper", 21: "coil.right-jet-bumper"}
SOLENOID_LABELS = {1: "Outhole Kicker", 2: "Ball Ramp Release", 3: "Left Eject Hole", 4: "Right Eject Hole",
                   5: "\"T\" Drop Target Reset", 6: "3-Bank Drop Target Reset", 7: "Up Post", 8: "Down Post",
                   9: "Space Flash Lamps", 10: "Shuttle Flash Lamps", 11: "General Illumination Relay",
                   13: "Right Outlane Gate", 14: "Insert Flash Lamps", 15: "Bell", 16: "Coin Lockout Coil",
                   17: "Left Kicker (Slingshot)", 18: "Right Kicker (Slingshot)", 19: "Left Jet Bumper", 20: "Lower Jet Bumper", 21: "Right Jet Bumper"}
SOLENOID_KINDS = {9: "flasher", 10: "flasher", 11: "relay", 14: "flasher"}
SOLENOID_NOTES = {
	1: "Kicks a drained ball from the outhole (9) up onto the ball ramp (10-12). The gameplay run shows one pulse per outhole closure.",
	2: "The ball-ramp release: kicks the ball on the lower ramp position (12) into the shooter lane (36). The ROM serves with it at game start, after a ball is locked in an eject hole and after the last ball in play drains (gameplay run).",
	3: "Kicks a locked ball out of the left eject hole (16). With balls in both holes, the long-ramp shot (32) makes the ROM fire it at once and the right eject (4) about 3 s later (gameplay run).",
	4: "Kicks a locked ball out of the right eject hole (24), about 3 s after the left eject at multi-ball (gameplay run).",
	5: "Raises the single \"T\" drop target (20). The ROM fires it at game start and, in the gameplay run, after the ramp bull's-eye (38).",
	6: "Raises the three targets of the 3-bank (33-35). The ROM fires it at game start and when all three are down (gameplay run).",
	7: "Drives the post between the flippers (the manual's heat shield) up. The manual: a centre-ramp shot raises the heat shield; in the gameplay run the long-ramp shot (32) fired it at multi-ball. A two-coil latching post with no position switch; lamp 7 lights the post.",
	8: "Drives the post between the flippers down. The ROM fires it at game start and, in the gameplay run, on the left return lane (14). Default: down.",
	9: "Space flash lamps, the left of the two flash-lamp domes on the centre playfield in the retained table (the script's 'Playfield Space Flasher'). PinMAME types 9 and 10 as #89 flash bulbs. The playfield wiring sheet's flash-lamp note draws four bulbs per flash-lamp circuit but does not say which circuits it applies to, so the bulb count stays unstated. The ROM flashes it when a ball is locked (gameplay run).",
	10: "Shuttle flash lamps, the right of the two flash-lamp domes on the centre playfield in the retained table (the script's 'Playfield Shuttle Flasher'); a #89 flash-bulb load in PinMAME. The ROM flashes it when a ball is locked (gameplay run).",
	11: (
		"Relay 5580-09555-00 on the power supply (solenoid table 3P7-1), which switches the general illumination. "
		"Public 1 energizes the relay and turns the GI off: PinMAME types 11 as a reversed 6.3 V AC GI output (CORE_MODOUT_BULB_44_6_3V_AC_REV) and the retained script's PFGI treats enabled as GI off. The ROM blinks it with effects and turns the GI off on tilt (gameplay run). "
		"Bulb positions and the split of the GI strings between playfield and backbox are not printed in the retained manual."
	),
	13: (
		"Holding coil of the right outlane gate (IPDB: right outlane detour gate). Game-Adjustment #7 says the old gate energizes to let the ball drain and the new gate energizes to return the ball to the flipper, and #4 sets whether it starts each turn or game open or closed. "
		"At factory settings the gameplay run shows the right outlane rollover (13) energizing it and the ROM holding it until the 3-bank is completed. Lamp 28 (Gate Open) shows its state. The retained script rotates its bottomgate flipper object to its end while 13 is enabled."
	),
	15: "Cabinet bell, the game's award sounder instead of a knocker (IPDB). It rings with ramp scoring and with the replay credit award (gameplay and credit-award runs); the retained script plays a bell sound from it (SolKnocker, commented 'Modified to play bell instead of knocker').",
	16: "Coin lockout coil behind the coin door; energized while credits may be accepted (manual credit posting; held through attract and play in the runs).",
}
SCRIPT_SOLENOIDS = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15})
LAMP_QUANTITY = {5: "X2", 7: "X2", 15: "two balloons", 38: "X2", 40: "X2", 41: "X2", 49: "X2"}
INSERT_FLASH_NOTE = (
	"Insert flash lamps. The solenoid table connects BRN-BLU SOL. 14 through the playfield plug 8P3-14, while the known-working script lights only a backglass rocket-plume object from it (SolCallback(14) = \"SetLamp 103,\" with Lampz 103 = BGFL40a, commented 'Backglass Rocket Plume Flasher'); the same manual calls the backbox lamps 39 and 40 'Insert Panel', and the solenoid location drawing places no balloon for 14. "
	"Where its bulbs are mounted is therefore unresolved (see conflict conflict.insert-flash-lamps-location) and it carries no placement. PinMAME types it as a #89 flash bulb. The ROM flashes it with locks and ramp shots (gameplay run)."
)


def build_outputs(geometry: dict | None) -> list[dict]:
	result = []
	for address in range(1, 65):
		binding = {"group": "pinmame.output.solenoid", "device": address}
		if address in data.SOLENOIDS:
			function, wire, cpu, field, transistor, part = data.SOLENOIDS[address]
			diagram = data.SOLENOID_DIAGRAM.get(address)
			structured_transistor = diagram[1] if diagram and diagram[0] == "transistor" else transistor
			structured_field = diagram[1] if diagram and diagram[0] == "playfield" else field
			cpu_pin = cpu.replace("1P-19-", "1P19-")
			wiring = {"board": "System 9 CPU Board D-10534", "driver_transistor": structured_transistor, "drive_connection": f"{cpu_pin}; {structured_field}", "drive_wire": wire}
			table = f"Solenoid table: '{function}', {wire}, {cpu}, {field}, {transistor}" + (f", {part}." if part else ", part number printed '-'.")
			if address == 2:
				table += " The playfield wiring diagram draws SOL. 2 on driver Q48 and the table prints no other Q48; the structured wiring follows the diagram, a wiring-detail disagreement that does not change the device or its address."
			elif address == 21:
				table += " The table's playfield cell repeats 8P3-12, the pin row 12 carries; the playfield wiring diagram runs SP. SOL. 5 on 8P3-21, in sequence with 17-22 on 8P3-17 to -22, and the structured wiring follows it."
			if address in data.UNUSED_SOLENOIDS:
				note = f"The solenoid table and the solenoid location list print Not Used. {table}"
				if address == 12:
					note += " The playfield wiring diagram ends SOL. 12 (Q57) at '8L12 NOT USED'. The ROM pulses 12 only in its solenoid-test sweep, never in the gameplay or credit-award runs; the sweep is not fitment."
				else:
					note += " Special #6 has a driver (Q85) and a trigger input (1J18-9, 8SW70 NOT USED) on the board, but PinMAME's sxx.ssSw slot for 22 is 0 and no switch fires it; nothing published it in any run."
				result.append({"id": f"coil.not-used-{address}", "label": f"Not Used ({structured_transistor})", "kind": "coil", "binding": binding,
				               "aliases": aliases("pinmame.solenoid", address), "availability": "unused",
				               "physical": {"location": "no fitted load", "notes": note}, "wiring": wiring,
				               "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE), "spatial": na("unused", MANUAL, RUNTIME_SOURCE)})
				continue
			identifier = SOLENOID_IDS[address]
			note = SOLENOID_NOTES.get(address, "")
			if address == 14:
				note = INSERT_FLASH_NOTE
			if address in data.PHYSICAL_SPECIAL_SWITCH:
				physical_switch = data.PHYSICAL_SPECIAL_SWITCH[address]
				published_switch = next(sw for sw, sol in data.PINMAME_SPECIAL_SWITCH_SOLENOIDS.items() if sol == address)
				sp_wire, sp_note, sp_cpu, sp_field, sp_name = data.SPECIAL_SWITCH_WIRING[address]
				note = (f"Special solenoid (SP. SOL. {address - 16}): on the machine its own special switch {sp_name} ({sp_wire}, CPU {sp_cpu}, playfield {sp_field}; the table's note 1 prints {sp_note}) fires it through the CPU board while the game-on enable 23 is set, and matrix switch {physical_switch} on the same device scores. "
				        f"PinMAME publishes it whenever matrix switch {published_switch} closes while 23 is set (sxx.ssSw), which the switch-test and gameplay runs show; the solenoid test does not step it, as the manual says.")
				if published_switch != physical_switch:
					note += f" PinMAME's pairing is rotated against the machine: switch {published_switch} sits on a different bumper, so a recreation fires this bumper from its own hit and treats {address} as informational. The known-working script binds no callback to 17-22 and lets the bumper objects fire themselves."
			note += " " + table
			physical = {"notes": note}
			if part:
				physical["part_number"] = part
			location = {11: "backbox, power supply board", 15: "cabinet", 16: "cabinet", 14: "unresolved: routed through playfield plug 8P3-14; the known-working script shows it in the backglass"}.get(address, "playfield")
			physical["location"] = location
			refs = [MANUAL, CORE, RUNTIME_SOURCE]
			if address <= 16:
				refs.append(RUNTIME_L3_SOURCE)
			if address in SCRIPT_SOLENOIDS:
				refs.append(SCRIPT)
			item = {"id": identifier, "label": SOLENOID_LABELS[address], "kind": SOLENOID_KINDS.get(address, "coil"), "binding": binding,
			        "aliases": aliases("pinmame.solenoid", address), "availability": "used", "physical": physical, "wiring": wiring,
			        "provenance": provenance(*refs, status="conflicted" if address == 14 else "validated")}
			if address in (15, 16):
				item["spatial"] = na("cabinet_or_service", MANUAL)
			elif address == 11:
				item["roles"] = ["cabinet.general-illumination-relay"]
				item["spatial"] = na("cabinet_or_service", MANUAL)
			elif address != 14:
				spatial = located(identifier, "emitter" if address in (9, 10) else "effect", anchors(geometry, "solenoid", address), geometry)
				if spatial:
					item["spatial"] = spatial
					disclose(item, "solenoid", address, geometry)
			result.append(item)
			continue
		if address == 23:
			result.append({"id": "relay.game-on-flipper-enable", "label": "Game On (Flipper Relay and Special Solenoid Enable)", "kind": "relay", "binding": binding,
			               "aliases": aliases("pinmame.solenoid", address), "availability": "used", "roles": ["cabinet.flipper-enable-relay"],
			               "physical": {"location": "backbox, CPU board", "notes": "PinMAME's S11_GAMEONSOL: the special-solenoid and flipper enable, published while the ROM enables play. The playfield wiring diagram draws the flipper relay contact between CPU 1J19-1 and 1J19-2, the flipper-button grounds. The gameplay run shows 23 rising at game start and dropping at the tilting playfield-tilt closure; the switch-test run shows it set throughout diagnostics. The manual's 'flipper relay is de-energized with subtest 25' is the generic System 9 text: this ROM's solenoid test stops at 16."},
			               "provenance": provenance(CORE, PROFILE, MANUAL, RUNTIME_SOURCE), "spatial": na("cabinet_or_service", MANUAL, CORE)})
			continue
		if address in (45, 46, 47, 48):
			side = "Right" if address < 47 else "Left"
			power = address in (45, 47)
			result.append({"id": f"virtual.{side.lower()}-flipper-{'power' if power else 'hold'}-synthetic", "label": f"{side} Flipper {'Power' if power else 'Hold'} (synthetic)",
			               "kind": "virtual", "binding": binding, "aliases": aliases("pinmame.solenoid", address), "availability": "used",
			               "physical": {"notes": f"PinMAME fabricates this state from flipper-column button {82 if side == 'Right' else 84} while the game-on enable 23 is set, because the driver declares no FLIP_SOL; both of the pair assert together (gameplay run). There is no CPU driver behind it: the cabinet button switches the {side.lower()} flipper (FL23/600-30-2600-50VDC, a 50 V coil the solenoid table requires) directly through the flipper relay. A recreation drives that flipper from this pair."},
			               "provenance": provenance(CORE, PROFILE, MANUAL, RUNTIME_SOURCE, SCRIPT), "spatial": na("virtual", CORE)})
			continue
		reasons = {24: "Reserved System 9/11 public output between the game-on enable and the C-side range; the driver populates nothing here.",
		           49: "CORE_FIRSTSIMSOL: the simulator's fake ball-shooter solenoid; nothing on this machine drives it."}
		if address in reasons:
			note = reasons[address]
		elif 25 <= address <= 32:
			note = "C-side relay alias: sxx.muxSol is 0 for Space Shuttle, so updsol never copies 1-8 here and the machine has no A/C relay."
		elif 33 <= address <= 36:
			note = "Generic upper-flipper range; core_getSol serves it only on WPC and SAM generations, so it reads 0 on System 9."
		elif 37 <= address <= 44:
			note = "Sound-overlay/printer range; Space Shuttle's gameSpecific1 is 0 (no S11_SNDOVERLAY or S11_PRINTERLINE), so nothing is published here."
		else:
			note = "Custom-solenoid space; the driver declares no custom solenoids, so PinMAME publishes no output here." if address >= 51 else "Unassigned gap below the custom-solenoid base."
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
		printed = data.LAMP_ASSEMBLY_PRINTED.get(address)
		if printed == '"':
			note += f" The lamp-location list prints its assembly as a ditto mark under {assembly}."
		elif printed:
			note += f" The lamp-location list prints its assembly as '{printed}', lamp {printed.split()[1]}'s {assembly}."
		if location == "backbox":
			note += " A backbox lamp: the playfield lamp-location drawing carries no balloon for it, and the retained script binds it to a backglass object."
		if address in LAMP_QUANTITY:
			note += (" The matrix cell prints X2, two bulbs on this address." if LAMP_QUANTITY[address] == "X2" else " The lamp-location drawing shows balloon 15 twice, one socket beside each flipper return lane.")
			if address == 41:
				note += " The lamp-location drawing shows balloon 41 twice, one on each side."
		if column == 3:
			note += " The lamp-matrix table prints this column on the key pin 1J7-5; the CPU schematic and backbox wiring diagram wire column 4 to 1J7-4."
		if row == 3:
			note += " The lamp-matrix table prints this row on the key pin 1J6-4; the backbox wiring diagram wires row 4 to 1J6-5."
		physical = {"location": "backbox" if location == "backbox" else "playfield", "notes": note}
		if address in LAMP_QUANTITY:
			physical["quantity"] = 2
		if assembly:
			physical["part_number"] = assembly
		item = {"id": identifier, "label": label, "kind": "lamp", "binding": {"group": "pinmame.output.lamp", "device": address},
		        "aliases": aliases("pinmame.lamp", address), "availability": "used", "physical": physical,
		        "wiring": {"board": "System 9 CPU Board D-10534 lamp matrix", "drive_connection": drive, "drive_wire": drive_wire,
		                   "return_connection": ret, "return_wire": return_wire},
		        "provenance": provenance(MANUAL, CORE, SCRIPT)}
		if location == "backbox":
			item["spatial"] = na("cabinet_or_service", MANUAL)
		else:
			names = anchors(geometry, "lamp", address)
			spatial = located(identifier, "emitter", names, geometry)
			if spatial:
				item["spatial"] = spatial
				if address == 7:
					item["physical"]["notes"] += " Placed on the table's lp2 centre-post light, the post the lamp lights; the script's CPFlash1/CPFlash2 doubles are excluded. Both bulbs share that one placement."
				elif len(names) == 2:
					item["physical"]["notes"] += f" Placed on the table's {names[0]} and {names[1]} lights, the two sockets the script binds; their bloom doubles are excluded."
				else:
					item["physical"]["notes"] += f" Placed on the table's {names[0]} insert light, the one the script's Lampz binds; its {names[0]}B bloom double is excluded." + (" Both bulbs share that one placement." if address in LAMP_QUANTITY else "")
		result.append(item)
	return result


# ---------------------------------------------------------------- mechanisms

def build_mechanisms(matrix_ids: dict[int, str], outputs: list[dict]) -> tuple[list[dict], list[dict]]:
	coils = {o["binding"]["device"]: o["id"] for o in outputs if o["binding"]["group"] == "pinmame.output.solenoid"}
	mechanisms, relationships = [], []

	def add(identifier, label, kind, actuators, sensors, behavior, *refs):
		mechanisms.append({"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
		                   "behavior": behavior, "provenance": provenance(MANUAL, CORE, RUNTIME_SOURCE, SCRIPT, *refs)})

	add("mech.outhole-and-ball-ramp", "Outhole, three-ball ramp and shooter lane", "kicker",
	    [coils[1], coils[2]], [matrix_ids[9], matrix_ids[10], matrix_ids[11], matrix_ids[12], matrix_ids[36]],
	    "Three balls. A drained ball falls into the outhole (9); the outhole kicker (1) lifts it onto the ball ramp (trough) under the apron, where balls rest on the lower (12), middle (11) and top (10) positions. Initialize 10, 11 and 12 closed and 9 open with all three balls home. "
	    "The ball-ramp release (2) kicks the ball on 12 into the shooter lane, where it rests on 36 until the manual plunger launches it; the next ball rolls down onto 12. "
	    "The ROM serves at game start (with the \"T\" reset 5, the 3-bank reset 6, the post down 8 and the game-on enable 23), after a ball is locked in an eject hole, and after the last ball in play drains.")
	add("mech.eject-hole-locks-and-multiball", "Left and right eject-hole locks and multi-ball", "kicker",
	    [coils[3], coils[4]], [matrix_ids[16], matrix_ids[24], matrix_ids[32]],
	    "Two kick-out holes, left (16) and right (24), are locks. A ball resting in either one is held; the ROM flashes the space (9), shuttle (10) and insert (14) flash lamps and serves another ball from the ball ramp (2). "
	    "With balls in both holes, the long-ramp shot (32) starts multi-ball: the ROM raises the post (7), fires the left eject (3) at once and the right eject (4) about 3 s later (gameplay run). IPDB lists 2-ball and 3-ball multiball. "
	    "The ROM fires an eject only on its own schedule, so model each hole as a saucer that holds a ball until its coil fires, and release the hole's switch as the ball leaves.")
	add("mech.three-bank-drop-targets", "3-bank drop targets", "drop_target_bank",
	    [coils[6]], [matrix_ids[33], matrix_ids[34], matrix_ids[35]],
	    "Three drop targets along the long ramp's left side (33 lowest to 35 highest), each latching its normally open switch closed while down. One reset coil (6) raises the bank. The ROM resets it at game start and when all three are down; a host holds the targets down until the reset and then releases them. "
	    "Completion increases the spinner value (manual game play) and, at factory settings, released the outlane gate (13) in the gameplay run.")
	add("mech.t-drop-target", "\"T\" drop target", "drop_target_bank",
	    [coils[5]], [matrix_ids[20]],
	    "A single drop target in the centre of the S-H-U-T-T-L-E row, latching switch 20 closed while down, with its own reset coil (5). The ROM resets it at game start and, in the gameplay run, after the ramp bull's-eye (38). Hitting it last awards 100,000 bonus (manual); IPDB calls it a timed drop target.")
	add("mech.heat-shield-post", "Up post between the flippers (heat shield)", "other",
	    [coils[7], coils[8]], [],
	    "One post between the flippers, driven up by the up-post coil (7) and down by the down-post coil (8): a two-coil latching post with no position switch, so its state is the last coil fired. Default: down. The manual: a centre-ramp shot raises the heat shield. In the gameplay run the long-ramp shot (32) raised it at multi-ball, and game start and the left return lane (14) lowered it. Lamp 7 (two bulbs) lights the post.")
	add("mech.right-outlane-gate", "Right outlane gate", "gate",
	    [coils[13]], [matrix_ids[13]],
	    "A holding coil (13) on the right outlane gate. Game-Adjustment #7 selects the old gate, which energizes to let the ball drain, or the new gate, which energizes to return the ball to the flipper; #4 sets whether it starts each turn or game open or closed. "
	    "At factory settings the right outlane rollover (13) made the ROM energize the gate, which stayed held until the 3-bank was completed (gameplay run). Lamp 28 (Gate Open) shows its state.")
	for coil, label in ((17, "Left kicker (slingshot)"), (18, "Right kicker (slingshot)")):
		switch = data.PHYSICAL_SPECIAL_SWITCH[coil]
		add(f"mech.{slug(label.split(' (')[0])}", label, "kicker", [coils[coil]], [matrix_ids[switch]],
		    f"The ball closes switch {switch} and the special solenoid {coil} kicks it away; on the machine the kicker's own special switch fires the coil through the CPU board while the game-on enable 23 is set, and in PinMAME a closure of {switch} publishes {coil} (sxx.ssSw). The solenoid test does not step it. Strength and recovery are table-owned.")
		relationships.append({"id": f"rel.switch-{switch}-fires-{coil}", "kind": "pulse", "source": matrix_ids[switch], "destination": coils[coil],
		                      "provenance": provenance(CORE, MANUAL, RUNTIME_SOURCE)})
	for coil, label in ((19, "Left jet bumper"), (20, "Lower jet bumper"), (21, "Right jet bumper")):
		switch = data.PHYSICAL_SPECIAL_SWITCH[coil]
		published = next(sw for sw, sol in data.PINMAME_SPECIAL_SWITCH_SOLENOIDS.items() if sol == coil)
		add(f"mech.{slug(label)}", label, "kicker", [coils[coil]], [matrix_ids[switch]],
		    f"A jet bumper: a ball on the skirt closes the bumper's special switch, which fires coil {coil} through the CPU board while the game-on enable 23 is set, and the matrix switch {switch} on the same bumper scores. "
		    f"PinMAME's sxx.ssSw is rotated against the machine: it publishes {coil} when switch {published} (a different bumper) closes. Fire this bumper locally from its own hit and report {switch}; do not drive it from PinMAME's {coil}. The known-working script does exactly that. Strength and recovery are table-owned.")
	add("mech.spinner", "Spinner", "rotary", [], [matrix_ids[37]],
	    "Free-spinning target at the long ramp entrance; each revolution closes switch 37 briefly. No coil. Its value (lamps 33-35, 1,000 / 2,000 / 4,000) is increased by completing the 3-bank (manual game play).")
	add("mech.right-flipper", "Right flipper and lane change switch", "other", [coils[45], coils[46]], [flipper_column_id(82), matrix_ids[41]],
	    "One 50 V right flipper (FL23/600-30-2600-50VDC) wired to the right cabinet button through the flipper relay. The B-9951 lane change switch on the right flipper closes with it, and the ROM moves the lit lane on it. PinMAME takes both from flipper-column button 82: it copies 82 into 41 and fabricates 45/46 while 23 is set. The solenoid table also prints a Top Flipper row with no wiring; no drawing shows a third flipper and IPDB lists two. Stroke timing is table-owned.")
	add("mech.left-flipper", "Left flipper", "other", [coils[47], coils[48]], [flipper_column_id(84)],
	    "One 50 V left flipper (FL23/600-30-2600-50VDC) wired to the left cabinet button through the flipper relay. PinMAME fabricates 47/48 from button 84 while 23 is set; the left side has no matrix switch. Stroke timing is table-owned.")
	relationships.append({"id": "rel.flipper-column-82-to-matrix-41", "kind": "direct", "source": flipper_column_id(82), "destination": matrix_ids[41],
	                      "provenance": provenance(CORE, PROFILE, RUNTIME_SOURCE)})
	for address in (45, 46, 47, 48):
		relationships.append({"id": f"rel.game-on-gates-{address}", "kind": "relay_gated", "source": "relay.game-on-flipper-enable", "destination": coils[address],
		                      "provenance": provenance(CORE, MANUAL, RUNTIME_SOURCE)})
	for switch in (33, 34, 35):
		relationships.append({"id": f"rel.reset-raises-{switch}", "kind": "pulse", "source": coils[6], "destination": matrix_ids[switch],
		                      "provenance": provenance(MANUAL, RUNTIME_SOURCE, SCRIPT)})
	relationships.append({"id": "rel.reset-raises-20", "kind": "pulse", "source": coils[5], "destination": matrix_ids[20],
	                      "provenance": provenance(MANUAL, RUNTIME_SOURCE, SCRIPT)})
	return mechanisms, relationships


# ---------------------------------------------------------------- conflicts

def build_conflicts() -> list[dict]:
	return [{
		"id": "conflict.insert-flash-lamps-location",
		"path": "outputs.solenoid.14 / flasher.insert-flash-lamps",
		"description": (
			"Where the bulbs of solenoid 14, Insert Flash-Lamps, are mounted. The solenoid table routes BRN-BLU SOL. 14 (Q59, CPU 1P12-7) through the playfield plug 8P3-14, in the same column that sends 11 to the power supply (3P7-1) and 15 and 16 to the cabinet (7P1), which puts its load on or under the playfield; "
			"the known-working script lights only a backglass rocket-plume flasher from it (SolCallback(14) = \"SetLamp 103,\" with Lampz 103 = BGFL40a) and nothing on the playfield, and the manual itself calls the backbox lamps 39 and 40 'Insert Panel'. "
			"The solenoid location drawing gives 14 no balloon, and the playfield wiring diagram's 8L14 designator does not settle it because the same sheet gives the backbox GI relay and the cabinet bell 8L designators too. "
			"Runtime binding is not in doubt; the physical location and therefore the placement are. "
			"Resolution path: a photograph or wiring trace of a real Space Shuttle showing where the BRN-BLU SOL. 14 wire ends, at the backbox insert board or at playfield flash-lamp sockets (and how many bulbs), which an owner or restorer could supply; no source this project holds shows it."
		),
		"source_refs": [MANUAL, SCRIPT],
	}]


# ---------------------------------------------------------------- sources

def excerpt_records() -> list[dict]:
	records = []
	for excerpt_id, (filename, locator) in EXCERPT_FILES.items():
		path = EXCERPTS / filename
		records.append({"id": excerpt_id, "locator": locator, "method": "manual", "path": path.as_posix(),
		                "reviewed": True, "sha256": EXCERPT_DIGESTS[excerpt_id], "transcribed_by": "curator"})
	return records


def build_sources(root: Path, geometry: dict | None) -> list[dict]:
	excerpts = {e["id"]: e for e in excerpt_records()}
	runtime = load_json(root / RUNTIME)
	sources = [
		{"id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": data.PINMAME_REVISION,
		 "locator": "Pinned catalog driver records sshtl_l7 (root) and sshtl_l3 (clone)", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/tree/{data.PINMAME_REVISION}", "revision": data.PINMAME_REVISION,
		 "locator": "src/wpc/driver.c sshtl drivers; src/wpc/s11games.c dispSshtl and sshtl INITGAMEFULL and ROM blocks; src/wpc/s11.c setSSSol, pia2a_r, pia4a_r, updsol, sshtl_ PWM block; src/wpc/core.c core_updateSw, core_getSol, core_swSeq2m; s11.h; core.h",
		 "license": "BSD-3-Clause", "attribution": "PinMAME contributors", "excerpts": [excerpts["pinmame-contract"]]},
		{"id": PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
		 "locator": "Williams System 9/11 public address rules: matrix 1-64, diagnostics -7 to -4, flipper column 81-88, solenoids 1-64 with the game-on enable at 23, lamps 1-64, GI on an ordinary solenoid address",
		 "license": "MIT", "attribution": "pinmame-game-defs curation"},
		{"id": MANUAL, "kind": "manual", "uri": "https://www.ipdb.org/files/2260/" + data.MANUAL_FILENAME,
		 "original_filename": data.MANUAL_FILENAME, "sha256": data.MANUAL_SHA256, "acquired_at": "2026-10-30T16:18:00Z",
		 "locator": f"Space Shuttle Instruction Manual dated Nov 3, 1984, with schematics, 33 pages (scan), IPDB machine 2260, retrieved through the Internet Archive capture https://web.archive.org/web/20250310003816id_/https://www.ipdb.org/files/2260/{data.MANUAL_FILENAME}; retained at external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb-2260/ with 300 dpi renders of the cited pages beside it. Exact pages in the excerpts.",
		 "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
		 "excerpts": [excerpts[e] for e in MANUAL_EXCERPTS]},
		{"id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=2260", "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-30T16:32:00Z",
		 "locator": f"IPDB machine 2260 through the Internet Archive capture https://web.archive.org/web/20261016074208id_/https://www.ipdb.org/machine.cgi?id=2260, retained as external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb-2260/machine-2260.html: Space Shuttle, Williams, December 1984, model number 535, Williams System 9, 7,000 units; notable features flippers (2), pop bumpers (3), slingshots (2), kick-out holes (2), 3-bank drop targets (1), timed drop target (1), standup targets (7), spinning target (1), multiball (2 ball, 3 ball), ramps (2), right outlane detour gate, lane change, up-post between flippers; uses a ringing bell instead of a knocker; has speech; toy: plastic shuttle replica; design by Barry Oursler and Joe Kaminkow.",
		 "license": "NOASSERTION", "attribution": "The Internet Pinball Database"},
		{"id": SCRIPT, "kind": "vpx_script", "known_working": True,
		 "uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{SCRIPT_CORPUS_REVISION}/Space%20Shuttle%20%28Williams%201984%292.0/Space%20Shuttle%20%28Williams%201984%29.vbs",
		 "revision": SCRIPT_CORPUS_REVISION, "sha256": SCRIPT_SHA256,
		 "locator": f"Pinned known-working corpus script '{SCRIPT_CORPUS_PATH}' (155,947 bytes) for the VPX table by bord: cGameName sshtl_l7, S11.VBS, UseSolenoids 2, Lampz fader. Runtime authority for the solenoid callbacks, switch handlers and ball routing in the excerpt.",
		 "license": "NOASSERTION", "attribution": "bord; Rawd; UnclePaulie; Sixtoe; rothbauerw", "excerpts": [excerpts["script-contract"]]},
		{"id": LIBRARY, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "sha256": VPM_S11_SHA256,
		 "locator": "Retained machine-neutral s11.vbs that the table loads with LoadVPM \"01560000\", \"S11.vbs\", 3.36: cabinet constants and the flipper-column buttons swLRFlip 82 and swLLFlip 84.",
		 "license": "NOASSERTION", "attribution": "VPinMAME script library contributors", "excerpts": [excerpts["script-library"]]},
		{"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": RUNTIME.as_posix(), "sha256": sha256(root / RUNTIME), "revision": data.PINMAME_REVISION,
		 "locator": f"Compact evidence recomputed by tools/summarize_space_shuttle_runtime.py from four LibPinMAME harness runs of sshtl_l7 (solenoid test, switch test, gameplay, credit award), each from a newly initialized state directory, library SHA-256 {data.LIBRARY_SHA256}, ROM archive {data.ROM_SHA256['sshtl_l7']}; raw runs under external:pinmame-review-artifacts/{REVIEW_FOLDER}/harness, manifest SHA-256 {runtime['source']['sha256']}.",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs curation; ROM bytes and NVRAM excluded"},
		{"id": RUNTIME_L3_SOURCE, "kind": "runtime_scenario", "uri": RUNTIME_L3.as_posix(), "sha256": sha256(root / RUNTIME_L3), "revision": data.PINMAME_REVISION,
		 "locator": f"Compact evidence recomputed by tools/summarize_space_shuttle_runtime.py from the sshtl_l3 solenoid-test run (ROM archive {data.ROM_SHA256['sshtl_l3']}), retained beside the L-7 runs.",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs curation; ROM bytes and NVRAM excluded"},
	]
	if geometry is not None:
		sources += geometry["sources"]
	return sources


# ---------------------------------------------------------------- definition

def build_definition(root: Path = ROOT) -> dict:
	geometry = load_geometry(root)
	if set(data.SWITCHES) | data.UNUSED_SWITCHES != set(range(1, 65)) or set(data.SWITCHES) & data.UNUSED_SWITCHES:
		raise RuntimeError("Space Shuttle switch inventory is incomplete or overlapping")
	if set(data.SOLENOIDS) != set(range(1, 23)) or set(data.LAMPS) != set(range(1, 65)):
		raise RuntimeError("Space Shuttle solenoid or lamp inventory is incomplete")
	runtime = load_json(root / RUNTIME)
	if runtime["source"]["sha256"] != RUNTIME_MANIFEST_SHA256 or load_json(root / RUNTIME_L3)["source"]["sha256"] != RUNTIME_MANIFEST_SHA256:
		raise RuntimeError("Space Shuttle runtime evidence cites an unexpected raw-run manifest")
	inputs, matrix_ids = build_inputs(geometry)
	outputs = build_outputs(geometry)
	mechanisms, relationships = build_mechanisms(matrix_ids, outputs)
	conflicts = build_conflicts()
	common = "Both drivers select the same sshtlGameData: GEN_S9, dispSshtl, no A/C relay, FLIP_SWNO(0,41), special switches 39/40/27/26/25, and the same U49 sound and U4-U6 speech ROMs; only the U20 game ROM differs."
	drivers = [
		{"id": "sshtl_l7", "description": "Space Shuttle (L-7)", "year": "1984", "manufacturer": "Williams", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "Production L-7 game software, the known-working script's cGameName. " + common + " Service tests, gameplay and the credit award were run on this ROM. The retained archive's sound ROM reads CRC 20e77990 rather than the listed 8050ae27; it does not drive the switch matrix, solenoids or lamps."},
		{"id": "sshtl_l3", "clone_of": "sshtl_l7", "description": "Space Shuttle (L-3)", "year": "1984", "manufacturer": "Williams", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "Earlier production L-3 game software. " + common + " Its solenoid test steps the identical 01-16 sequence (runtime evidence); no L-3 gameplay run is claimed."},
	]
	displays = []
	for index, start, width, identifier, label in (
		(0, 21, 7, "display.player-1", "Player 1 score, seven 7-segment digits with commas"),
		(1, 29, 7, "display.player-2", "Player 2 score, seven 7-segment digits with commas"),
		(2, 1, 7, "display.player-3", "Player 3 score, seven 7-segment digits with commas"),
		(3, 9, 7, "display.player-4", "Player 4 score, seven 7-segment digits with commas"),
		(4, 0, 1, "display.credits-left", "Credits, left digit (credit / ball-in-play display)"),
		(5, 8, 1, "display.credits-right", "Credits, right digit (credit / ball-in-play display)"),
		(6, 20, 1, "display.ball-in-play-match-left", "Ball In Play / Match, left digit (credit / ball-in-play display)"),
		(7, 28, 1, "display.ball-in-play-match-right", "Ball In Play / Match, right digit (credit / ball-in-play display)"),
	):
		displays.append({"id": identifier, "label": label, "kind": "segment", "controller_index": index, "segment_start": start, "width": width, "height": 1,
		                 "physical_location": "cabinet_or_service", "provenance": provenance(CORE, MANUAL, RUNTIME_SOURCE),
		                 "spatial": na("cabinet_or_service", MANUAL, CORE)})
	missing = [] if geometry is not None and geometry.get("complete") else ["spatial_placement"]
	if unresolved_conflicts({"conflicts": conflicts}):
		missing.append("unresolved_conflicts")
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Space Shuttle", "manufacturer": "Williams", "year": 1984, "model_number": "535", "ipdb_id": 2260,
		            "opdb_id": "G4q3L-MKN50", "kind": "physical_pinball",
		            **({"playfield": geometry["playfield"]} if geometry is not None else {})},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x800", "inversion_applied_by_emulator": True},
		"coverage": {"status": "partial" if missing else "author_ready", "missing": missing, "dimensions": {
			"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
			"mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "display_inventory": "validated",
			"diagnostic_enumeration": "validated", "runtime_observation": "validated", "causal_exercise": "validated", "emulator_normalization": "validated",
			"spatial_placement": "validated" if "spatial_placement" not in missing else ("observed" if geometry is not None else "unknown")}},
		"drivers": drivers, "inputs": inputs, "outputs": outputs, "displays": displays, "mechanisms": mechanisms, "relationships": relationships,
		"sources": build_sources(root, geometry), "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "complete"}, "conflicts": conflicts,
	}
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
		"callout_check": None,
		"blockers": [
			"No factory drawing callout check has been run against the switch (PDF 19), solenoid (PDF 4) and lamp (PDF 20) location drawings, so every table placement stays observed rather than validated.",
			"Solenoid 14 (insert flash lamps) has no placement: its physical location is the open conflict conflict.insert-flash-lamps-location.",
			"Switch 45 (long ramp lower switch) has no placement: the switch-location drawing puts it beside the spinner at the ramp entrance, in front of switch 32, while the retained table's sw45 trigger sits further up the ramp behind sw32. Measuring balloon 45 on the drawing, or a table object at that spot, would place it.",
			"Switch 49 (playfield tilt) has no placement: no drawing balloon or table object locates the mechanism.",
		],
		"readiness": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"], "unresolved_conflicts": len(unresolved_conflicts(definition))},
	}


def render_report(report: dict) -> str:
	lines = ["# Space Shuttle (1984) spatial evidence", "", f"**Decision: {report['readiness']['status']}.** Missing: {', '.join(report['readiness']['missing']) or 'nothing'}.", "",
	         report["coordinate_convention"] + ".", ""]
	if report["geometry_seed"]:
		lines += [f"Geometry seed `{report['geometry_seed']}` SHA-256 `{report['geometry_seed_sha256']}`.", ""]
	else:
		lines += ["No retained table geometry yet: every playfield device is unplaced.", ""]
	lines += ["## Blockers", ""] + [f"- {b}" for b in report["blockers"]]
	lines += ["", "## Placed devices", "", "| Device | Binding | Placements |", "| --- | --- | --- |"]
	lines += [f"| `{r['id']}` | {r['binding']['group']} {r['binding']['device']} | " + "; ".join(f"({p['x']}, {p['y']}) {p['provenance']['status']}" for p in r["placements"]) + " |" for r in report["located"]]
	if report["projections"]:
		lines += ["", "## Projections", ""] + [f"- {p['kind']} {p['address']}: {p['disclosure']}" for p in report["projections"]]
	lines += ["", "## Unplaced devices", "", "| Device | Label |", "| --- | --- |"]
	lines += [f"| `{r['id']}` | {r['label']} |" for r in report["unplaced"]]
	lines.append("")
	return "\n".join(lines)


# ---------------------------------------------------------------- products

def verify_excerpts(root: Path = ROOT) -> None:
	for excerpt_id, (filename, _locator) in EXCERPT_FILES.items():
		path = root / EXCERPTS / filename
		if not path.is_file() or sha256(path) != EXCERPT_DIGESTS[excerpt_id]:
			raise RuntimeError(f"Space Shuttle excerpt missing or changed: {path}")


def products(root: Path = ROOT) -> dict[Path, bytes]:
	verify_excerpts(root)
	definition = build_definition(root)
	errors = validate_machine(definition, root)
	if errors:
		raise RuntimeError("Invalid Space Shuttle definition: " + "; ".join(errors))
	report = build_report(definition, root)
	path = AUTHOR_READY if definition["coverage"]["status"] == "author_ready" else DEFINITION
	return {path: canonical_bytes(definition), KNOWLEDGE: (root / KNOWLEDGE_SEED).read_bytes(),
	        REPORT: canonical_bytes(report), REPORT_MD: render_report(report).encode("utf-8")}


def check(root: Path = ROOT) -> None:
	result = products(root)
	stale = DEFINITION if AUTHOR_READY in result else AUTHOR_READY
	if (root / stale).exists():
		raise RuntimeError(f"Space Shuttle has a stale opposing-status record: {stale}")
	for path, payload in result.items():
		if not (root / path).is_file() or (root / path).read_bytes() != payload:
			raise RuntimeError(f"Space Shuttle deterministic artifact missing or drifted: {path}")
	print("Space Shuttle definition, knowledge note, excerpts and spatial reports match the deterministic curator.")


def generate(root: Path = ROOT) -> None:
	result = products(root)
	if AUTHOR_READY not in result and (root / AUTHOR_READY).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Space Shuttle record with a partial one")
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
			raise RuntimeError("Space Shuttle retained table or embedded script changed")
		manifest = build_manifest(extraction, "sshtl_l7")
		if (check_manifest(extraction, "sshtl_l7"), len(manifest["files"]), sum(f["size"] for f in manifest["files"])) != (table["manifest_sha256"], table["file_count"], table["total_bytes"]):
			raise RuntimeError("Space Shuttle table extraction changed")
		for name, obj in geometry["objects"].items():
			raw = load_json(extraction / obj["file"])
			value = raw.get(obj["type"], raw)
			if sha256(extraction / obj["file"]) != obj["file_sha256"]:
				raise RuntimeError(f"Space Shuttle geometry object drifted: {name}")
			if obj["method"] == "mesh_world_bounds":
				if sha256(extraction / obj["mesh_file"]) != obj["mesh_file_sha256"] or mesh_centre(extraction / obj["mesh_file"], value["position"], value["size"]) != (obj["x"], obj["y"]):
					raise RuntimeError(f"Space Shuttle geometry mesh drifted: {name}")
			elif _item_point(obj["type"], value)[:2] != (obj["x"], obj["y"]):
				raise RuntimeError(f"Space Shuttle geometry object drifted: {name}")
	folder = manuals / "by-machine" / MACHINE_ID / "ipdb-2260"
	if sha256(folder / data.MANUAL_FILENAME) != data.MANUAL_SHA256 or sha256(folder / "machine-2260.html") != IPDB_PAGE_SHA256:
		raise RuntimeError("Space Shuttle retained manual or IPDB page changed")
	if sha256(review / "vpm-script-libs" / "s11.vbs") != VPM_S11_SHA256:
		raise RuntimeError("Retained s11.vbs changed")
	from summarize_space_shuttle_runtime import OUTPUTS, build
	if any(canonical_bytes(value) != (root / OUTPUTS[game]).read_bytes() for game, value in build(review / REVIEW_FOLDER / "harness").items()):
		raise RuntimeError("Space Shuttle raw runtime evidence disagrees with the compact evidence")
	print("Space Shuttle retained manual, IPDB page, script library, raw runs and table geometry match the pinned evidence.")


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
