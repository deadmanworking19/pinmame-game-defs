"""Spatial placements for the Stern NBA (2009) definition.

Coordinates are the normalized stored centres of the retained table's objects
(``tools/seeds/stern/nba-2009-spatial.json``, produced by
``pinmame_game_defs.spatial.extract_spatial_candidates`` from the exact retained table). Stern's
public NBA document has no location drawings, so no placement can be checked against a factory
drawing and every placement stays ``observed``; the pop-bumper placements are ``conflicted`` with
the pop-bumper side conflict. Flash lamps are placed only on a bulb light at a modelled dome or
under an insert, never on a VPX ``Flasher`` sprite. The insert lamps are only ``candidate``
placements: the table draws each at an insert light that renders the playfield image and sits on
no bulb, and such a render light never makes a socket on its own (``docs/SPATIAL.md``).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import nba_devices as dev
from nba_devices import CORE, MANUAL, RT_POPS, SCRIPT, TABLE, provenance

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "tools/seeds/stern/nba-2009-spatial.json"

# switch -> object name. The pop bumpers follow the ROM's names (31 LEFT, 32 RIGHT); the table's
# own bumper objects are named the other way round (conflict.pop-bumper-sides).
SWITCH_OBJECTS: dict[int, str] = {
	1: "HitTarget.sw1", 2: "HitTarget.sw2", 3: "HitTarget.sw3", 4: "HitTarget.sw4", 5: "HitTarget.sw5", 6: "HitTarget.sw6", 7: "HitTarget.sw7",
	8: "Gate.Sw8", 9: "Kicker.RightEject", 10: "HitTarget.sw10", 11: "HitTarget.sw11", 12: "HitTarget.sw12", 13: "HitTarget.sw13", 14: "Trigger.SW14",
	23: "Trigger.sw23", 24: "Trigger.Sw24", 25: "Trigger.Sw25", 26: "Wall.sw26", 27: "Wall.sw27", 28: "Trigger.Sw28", 29: "Trigger.Sw29",
	30: "Bumper.sw30", 31: "Bumper.sw32", 32: "Bumper.sw31", 33: "Trigger.sw33", 34: "Trigger.sw34", 35: "Kicker.shooter", 36: "Trigger.SW36", 37: "Gate.Sw37", 47: "HitTarget.sw47",
}
# coil -> object name, or a tuple of names whose mean is the mechanism anchor
COIL_OBJECTS: dict[int, Any] = {
	1: "Kicker.BallRelease", 2: "Trigger.sw23", 3: "Trigger.magtrigger", 4: "Kicker.shooter", 5: ("Wall.div1", "Wall.div2"), 6: "Trigger.spinningdisk",
	7: ("HitTarget.sw11", "HitTarget.sw12", "HitTarget.sw13"), 9: "Bumper.sw30", 10: "Bumper.sw32", 11: "Bumper.sw31", 12: "Primitive.RampDiverter",
	15: "Flipper.LeftFlipper", 16: "Flipper.RightFlipper", 17: "Wall.sw26", 18: "Wall.sw27", 20: "Kicker.RightEject", 21: "Wall.ODiv",
}
# flash lamp -> one bulb light per physical lamp
FLASHER_OBJECTS: dict[int, tuple[str, ...]] = {
	14: ("Light.F14a", "Light.F14b"), 23: ("Light.F23",), 25: ("Light.F25a",), 26: ("Light.F26a",), 27: ("Light.F27a",), 28: ("Light.F28a",),
	29: ("Light.F29",), 30: ("Light.F30a",), 32: ("Light.F32a", "Light.F32b"),
}
LAMP_OBJECTS: dict[int, str] = {n: ("Light.L41" if n == 41 else f"Light.l{n}a" if n in (60, 61, 62) else f"Light.l{n}") for n in dev.LAMPS if n not in (1, 2)}
# the only lamp lights the table models as bulb lights; every other lamp light is an insert render light
BULB_LAMPS = frozenset({60, 61, 62})
INSERT_LAMPS = tuple(sorted(set(LAMP_OBJECTS) - BULB_LAMPS))
CABINET_COILS = {8, 24}
INTERNAL_COILS = {22}
CONFLICTED_SWITCHES, CONFLICTED_COILS, CONFLICTED_LAMPS = dev.BUMPER_SIDE_SWITCHES, dev.BUMPER_SIDE_COILS, dev.BUMPER_SIDE_LAMPS


def load_seed() -> dict[str, Any]:
	return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def point(seed: dict[str, Any], spec: Any) -> tuple[float, float]:
	if isinstance(spec, tuple):
		xs, ys = zip(*(point(seed, name) for name in spec))
		return round(sum(xs) / len(xs), 6), round(sum(ys) / len(ys), 6)
	x, y = seed["objects"][spec][:2]
	return x, y


def placement(identifier: str, role: str, x: float, y: float, *refs: str, status: str = "observed") -> dict[str, Any]:
	return {"id": identifier, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs, status=status)}


def located(identifier: str, role: str, seed: dict[str, Any], spec: Any, *refs: str, status: str = "observed") -> dict[str, Any]:
	x, y = point(seed, spec)
	return {"status": status, "placements": [placement(identifier, role, x, y, *refs, status=status)]}


def not_applicable(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def referenced_objects() -> list[str]:
	names: set[str] = set(SWITCH_OBJECTS.values()) | set(LAMP_OBJECTS.values())
	for spec in COIL_OBJECTS.values():
		names.update(spec if isinstance(spec, tuple) else (spec,))
	for lights in FLASHER_OBJECTS.values():
		names.update(lights)
	# the render doubles, dome primitives and helper objects the notes cite
	names.update({"Light.F25b", "Light.F26b", "Light.F27b", "Light.F28b", "Light.F30b", "Light.F31a", "Light.F31b", "Light.f19c", "Flasher.F13", "Flasher.f19", "Flasher.f19a", "Flasher.f19b",
		"Primitive.LDome", "Primitive.RDome", "Primitive.LDome1", "Primitive.RDome1", "Primitive.diverterP", "Trigger.BMagHelp", "Gate.sw22", "Kicker.Drain", "Plunger.Plunger"})
	return sorted(names)


def build_seed(register_path: Path, manifest_sha256: str) -> dict[str, Any]:
	"""Distil the extractor's register into the committed seed (needs the working-root extraction)."""
	register = json.loads(register_path.read_text(encoding="utf-8"))
	by_name = {f"{item['type']}.{item['name']}": item for item in register["objects"]}
	objects = {}
	for name in referenced_objects():
		if name not in by_name:
			continue
		item = by_name[name]
		objects[name] = [item["x"], item["y"], item["type"], item.get("source_path", f"gameitems/{item['type']}.{item['name']}.json")]
	return {
		"table_sha256": register["source"]["vpx_sha256"], "table_manifest_sha256": manifest_sha256, "bounds": register["bounds"],
		"normalization": {"helper": "pinmame_game_defs.spatial.extract_spatial_candidates", "x": "(raw_x - left) / (right - left)", "y": "(raw_y - top) / (bottom - top)"},
		"objects": dict(sorted(objects.items())),
	}


BUMPER_NOTE = "Spatial: placed on the pop bumper on the side the ROM's service tests name (top: Bumper.sw30; left: Bumper.sw32 at x 0.364; right: Bumper.sw31 at x 0.562). The retained table names and binds its bumper objects the other way round (object sw31 on the right pulses switch 31, sw32 on the left pulses 32), as the parts book's bumper callouts do, while it lights lamp 61 on the left bumper (l61a) and lamp 62 on the right (l62a) as the ROM does; the placement stays conflicted with conflict.pop-bumper-sides."
SWITCH_NOTES: dict[int, str] = {
	8: "Spatial: the table's Sw8 gate, the only object it binds to this switch; it sits high on the right ramp, above the ramp's entrance sound trigger RREnter.",
	9: "Spatial: the table's RightEject kicker (bsTEject, switch 9).",
	11: "Spatial: the table's sw11 drop target, the front target of the bank.",
	13: "Spatial: the table's sw13 drop target, the rear target of the bank.",
	31: BUMPER_NOTE, 32: BUMPER_NOTE,
	34: "Spatial: the table's sw34 trigger in the Magna-hoop, beside the magnet trigger and the ring block.",
	35: "Spatial: the table's kicker object named \"shooter\" (bsSEject, switch 35), which is the left eject hole, not the shooter lane.",
	37: "Spatial: the table's Sw37 gate, the only object it binds to this switch.",
}
COIL_NOTES: dict[int, str] = {
	1: "Spatial: the table's BallRelease kicker at the trough exit; the up-kicker coil is below the playfield.",
	2: "Spatial: shares the shooter-lane trigger point; the table's autoplunger has no object of its own.",
	3: "Spatial: the table's magtrigger, where its basket magnet catches the ball; the magnet is behind the basket's backboard.",
	4: "Spatial: the left eject hole (the table's kicker object named \"shooter\").",
	5: "Spatial: the mean of the table's two diverter walls div1 and div2, which the script raises and drops in turn; the diverter coil is not modelled.",
	6: "Spatial: the centre of the table's spinning-disk turntable trigger (its WheelP disk primitive is at the same point).",
	7: "Spatial: the mean of the three MVP drop target objects; the reset coil body is not modelled.",
	9: BUMPER_NOTE, 10: BUMPER_NOTE, 11: BUMPER_NOTE,
	12: "Spatial: the stored position of the table's RampDiverter primitive, which the script rotates; the BMagHelp trigger the same routine toggles lies within 0.013 of it, so the stored position is not a baked-mesh offset.",
	17: "Spatial: the table's left slingshot wall sw26.",
	18: "Spatial: the table's right slingshot wall sw27.",
	20: "Spatial: the right eject hole (the table's RightEject kicker).",
	21: "Spatial: the table's ODiv wall that the script raises across the orbit (its diverterP post primitive is at the same point).",
}
COIL_GENERIC = "Spatial anchor: the mechanism object the coil drives, not a winding or coil-body centre."
FLASHER_NOTES: dict[int, str] = {
	14: "Spatial: the table's two bulb lights F14a and F14b on the left ramp, one per lamp.",
	23: "Spatial: the table's F23 bulb light inside its left-side dome primitive LDome1.",
	25: "Spatial: the table's F25a bulb light under the left ramp arrow insert; F25b is a wider-falloff render double at the same insert.",
	26: "Spatial: the table's F26a bulb light under the left eject arrow insert (beside lamp 26); F26b is a render double.",
	27: "Spatial: the table's F27a bulb light under the right eject arrow insert (beside lamp 27); F27b is a render double.",
	28: "Spatial: the table's F28a bulb light under the right ramp arrow insert; F28b is a render double.",
	29: "Spatial: the table's F29 bulb light inside its right-side dome primitive RDome1.",
	30: "Spatial: the table's F30a bulb light at the captive ball; F30b is a render double.",
	32: "Spatial: the table's F32a and F32b bulb lights inside the slingshot dome primitives LDome and RDome, one per lamp.",
}
UNPLACED_FLASHER_NOTES: dict[int, str] = {
	13: "Spatial: not placed. The retained table has no bulb light for these lamps, only the VPX Flasher sprite F13 at the playfield's rear edge, which is not a socket.",
	19: "Spatial: not placed. The retained table drives only the VPX Flasher sprites f19, f19a and f19b and the light f19c, which lies beyond the playfield's rear edge, for these lamps; none of them is a socket on the playfield.",
	31: "Spatial: not placed. The ROM names three pop-bumper flash lamps, but the retained table lights only one co-located render double (F31a/F31b) beside the pop bumpers, so it does not say where the three lamps are.",
}
LAMP_NOTES: dict[int, str] = {
	60: "Spatial: the table's l60a light on the top bumper.",
	61: BUMPER_NOTE, 62: BUMPER_NOTE,
}
INSERT_LAMP_NOTE = "Spatial: a candidate only, at the centre of the table's insert light {name}. That light renders the playfield image through the insert and sits on no bulb (is_bulb_light and show_bulb_mesh false), so it does not locate the socket; the socket is expected under this insert, but no bulb object or drawing places it."
TROUGH_NOTE = "Spatial: not placed. The retained table models the trough in its script (cvpmTrough), with no object for this sensor below the playfield."


def _append(device: dict[str, Any], text: str) -> None:
	physical = device.setdefault("physical", {})
	physical["notes"] = (physical.get("notes", "") + " " + text).strip()


def attach(definition: dict[str, Any], seed: dict[str, Any]) -> dict[str, int]:
	"""Add spatial records to the definition's devices in place; returns counts for the report."""
	counts = {"located": 0, "not_applicable": 0}
	refs = (TABLE, SCRIPT)
	for device in definition["inputs"]:
		address = device["binding"]["device"]
		group = device["binding"]["group"]
		if group == "pinmame.input.dip":
			device["spatial"] = not_applicable("dip_switch", CORE)
		elif device["availability"] == "unused":
			device["spatial"] = not_applicable("unused", CORE)
		elif 1 <= address <= 64 and address in SWITCH_OBJECTS:
			conflicted = address in CONFLICTED_SWITCHES
			sources = refs + ((dev.ROM, RT_POPS, MANUAL) if conflicted else ())
			device["spatial"] = located(f"placement.switch-{address}.sensor", "sensor", seed, SWITCH_OBJECTS[address], *sources, status="conflicted" if conflicted else "observed")
			if address in SWITCH_NOTES:
				_append(device, SWITCH_NOTES[address])
		elif 1 <= address <= 64:
			if address in (15, 16):
				device["spatial"] = not_applicable("cabinet_or_service", MANUAL)
			else:
				_append(device, TROUGH_NOTE)
		elif address in (83, 81):
			device["spatial"] = not_applicable("internal_nonvisual", MANUAL)
		else:
			device["spatial"] = not_applicable("cabinet_or_service", MANUAL)
	for device in definition["outputs"]:
		address = device["binding"]["device"]
		group = device["binding"]["group"]
		if device["kind"] == "virtual":
			device["spatial"] = not_applicable("virtual", CORE)
		elif device["availability"] == "unused":
			device["spatial"] = not_applicable("unused", CORE)
		elif group == "pinmame.output.solenoid":
			conflicted = address in CONFLICTED_COILS
			if address in COIL_OBJECTS:
				sources = refs + ((dev.ROM, RT_POPS, MANUAL) if conflicted else ())
				device["spatial"] = located(f"placement.coil-{address}.effect", "effect", seed, COIL_OBJECTS[address], *sources, status="conflicted" if conflicted else "observed")
				_append(device, COIL_NOTES.get(address, COIL_GENERIC))
			elif address in FLASHER_OBJECTS:
				lights = FLASHER_OBJECTS[address]
				placements = [placement(f"placement.flasher-{address}.emitter" + (f"-{index + 1}" if len(lights) > 1 else ""), "emitter", *point(seed, light), *refs) for index, light in enumerate(lights)]
				device["spatial"] = {"status": "observed", "placements": placements}
				_append(device, FLASHER_NOTES[address])
			elif address in UNPLACED_FLASHER_NOTES:
				_append(device, UNPLACED_FLASHER_NOTES[address])
			elif address in CABINET_COILS:
				device["spatial"] = not_applicable("cabinet_or_service", MANUAL)
			elif address in INTERNAL_COILS:
				device["spatial"] = not_applicable("internal_nonvisual", MANUAL)
		elif group == "pinmame.output.lamp":
			if address in LAMP_OBJECTS:
				conflicted = address in CONFLICTED_LAMPS
				sources = refs + ((dev.ROM, RT_POPS, MANUAL) if conflicted else ())
				status = "conflicted" if conflicted else "observed" if address in BULB_LAMPS else "candidate"
				device["spatial"] = located(f"placement.lamp-{address}.emitter", "emitter", seed, LAMP_OBJECTS[address], *sources, status=status)
				_append(device, LAMP_NOTES.get(address) or INSERT_LAMP_NOTE.format(name=LAMP_OBJECTS[address].split(".", 1)[1]))
			elif address in (1, 2):
				device["spatial"] = not_applicable("cabinet_or_service", MANUAL)
	for device in definition["inputs"] + definition["outputs"]:
		spatial = device.get("spatial")
		if spatial:
			counts["located" if "placements" in spatial else "not_applicable"] += 1
	return counts


if __name__ == "__main__":
	import argparse

	import build_external_evidence_manifest as manifest
	from pinmame_game_defs.jsonio import canonical_bytes

	parser = argparse.ArgumentParser(description="Write the committed spatial seed from the retained table extraction.")
	parser.add_argument("--vpx-root", required=True, type=Path, help="working-root vpx-sources/stern/nba-2009")
	parser.add_argument("--write", action="store_true", required=True)
	arguments = parser.parse_args()
	digest = manifest.write_manifest(arguments.vpx_root, "nba-2009")
	seed = build_seed(arguments.vpx_root / "analysis/spatial-candidates.json", digest)
	SEED_PATH.write_bytes(canonical_bytes(seed))
	print(f"wrote {SEED_PATH.relative_to(ROOT)} with {len(seed['objects'])} objects, extraction manifest {digest}")
