"""Spatial placements for the Stern Family Guy (2007) definition.

Coordinates are the normalized stored centres of the retained table's objects
(``tools/seeds/stern/family-guy-2007-spatial.json``, produced by
``pinmame_game_defs.spatial.extract_spatial_candidates`` from the exact retained table). A device
takes the object the *manual's location drawings* put it at, not the object the table's script binds
where the two disagree (the table binds its rear pop-bumper object to the manual's front bumper, and
lights the mini-playfield name LEDs under the wrong names); each such choice is stated on the device.
Every placement stays ``observed`` until the factory-drawing callout check agrees with it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import family_guy_devices as dev
from family_guy_devices import CORE, MANUAL, SCRIPT, provenance

TABLE = "vpx.table.family-guy-2020"
ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "tools/seeds/stern/family-guy-2007-spatial.json"

# switch -> (object name, exact placement role note)
SWITCH_OBJECTS: dict[int, str] = {
	1: "Wall.CPC", 2: "Wall.CPC", 3: "HitTarget.sw3", 4: "HitTarget.sw4", 5: "HitTarget.sw5", 6: "Trigger.sw6", 7: "Trigger.sw7", 8: "HitTarget.sw8", 9: "Wall.sw9", 10: "HitTarget.sw10",
	13: "Kicker.sw13", 23: "Trigger.sw23", 24: "Trigger.sw24", 25: "Trigger.sw25", 26: "Wall.LeftSlingShot", 27: "Wall.RightSlingShot", 28: "Trigger.sw28", 29: "Trigger.sw29",
	30: "Bumper.Bumper1", 31: "Bumper.Bumper2", 32: "Bumper.Bumper3", 33: "Gate.LeftGate", 35: "Wall.CastleGuardsw", 39: "Spinner.sw39", 40: "Trigger.sw40",
	41: "HitTarget.sw41", 42: "HitTarget.sw42", 43: "HitTarget.sw43", 44: "Wall.sw44", 45: "Wall.sw45", 46: "Wall.sw46", 47: "Wall.sw47", 48: "Trigger.sw48", 49: "Wall.sw49",
	50: "HitTarget.sw50", 51: "HitTarget.sw51", 52: "Trigger.sw52", 53: "Trigger.sw53", 54: "Trigger.sw54", 55: "Kicker.sw55", 57: "Trigger.sw57", 64: "Kicker.sw64",
}
# coil -> object name, or a tuple of names whose mean is the anchor
COIL_OBJECTS: dict[int, Any] = {
	1: "Kicker.BallRelease", 2: "Trigger.sw23", 3: ("Wall.sw44", "Wall.sw45", "Wall.sw46", "Wall.sw47"), 4: "Wall.CPC", 5: "Kicker.sw64", 6: "Wall.sw9", 7: "Wall.LeftSlingShot", 8: "Wall.RightSlingShot",
	9: "Bumper.Bumper3", 10: "Bumper.Bumper2", 11: "Bumper.Bumper1", 12: "Wall.CPC", 13: "Kicker.sw13", 14: "Flipper.LeftFlipperSmall", 15: "Flipper.LeftFlipper", 16: "Flipper.RightFlipper",
	17: "Flipper.MiniPF_LeftFlipper", 18: "Flipper.MiniPF_RightFlipper", 19: "Wall.CastleGuardsw", 20: "Primitive.StewieP", 21: "Kicker.sw55", 22: "Primitive.MegP",
}
FLASHER_OBJECTS: dict[int, str] = {23: "Light.F23", 29: "Light.F29", 30: "Light.F30", 31: "Light.F31", 32: "Light.F32"}
# lamp -> light name (lamp 61 is the front (bottom) bumper's LED; l61 is the table's second light on the rear bumper)
LAMP_OBJECTS: dict[int, str] = {**{n: f"Light.l{n}" for n in range(3, 59)}, 61: "Light.l61a", **{n: f"Light.l{n}" for n in (62, 63, 64, 65, 66, 67, 68, 70)}}
# mini-playfield name LEDs: public lamp -> the table's LED object lying on the same printed letter of the mini-playfield art
LED_OBJECTS: dict[int, str] = {
	84: "Light.LED1", 83: "Light.LED2", 82: "Light.LED3", 81: "Light.LED4", 97: "Light.LED5",
	98: "Light.LED6", 99: "Light.LED7", 100: "Light.LED8",
	114: "Light.LED9", 89: "Light.LED10", 90: "Light.LED11", 91: "Light.LED12", 92: "Light.LED13",
	108: "Light.LED14", 107: "Light.LED15", 106: "Light.LED16", 105: "Light.LED17",
	125: "Light.LED18", 124: "Light.LED19", 123: "Light.LED20", 122: "Light.LED21", 121: "Light.LED22",
}
NOT_APPLICABLE_SWITCH_ROLES = {15, 16}
SENSOR_KINDS = {"switch"}


def load_seed() -> dict[str, Any]:
	return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def point(seed: dict[str, Any], spec: Any) -> tuple[float, float]:
	if isinstance(spec, tuple):
		xs, ys = zip(*(point(seed, name) for name in spec))
		return round(sum(xs) / len(xs), 6), round(sum(ys) / len(ys), 6)
	x, y = seed["objects"][spec][:2]
	return x, y


def placement(identifier: str, role: str, x: float, y: float, *refs: str) -> dict[str, Any]:
	return {"id": identifier, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs, status="observed")}


def located(identifier: str, role: str, seed: dict[str, Any], spec: Any, *refs: str) -> dict[str, Any]:
	x, y = point(seed, spec)
	return {"status": "observed", "placements": [placement(identifier, role, x, y, *refs)]}


def not_applicable(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def referenced_objects() -> list[str]:
	names: set[str] = set(SWITCH_OBJECTS.values()) | set(FLASHER_OBJECTS.values()) | set(LAMP_OBJECTS.values()) | set(LED_OBJECTS.values())
	for spec in COIL_OBJECTS.values():
		names.update(spec if isinstance(spec, tuple) else (spec,))
	# controls for the drawing fits and the other bumper/flipper objects
	names.update({"Bumper.Bumper1", "Bumper.Bumper2", "Bumper.Bumper3", "Flipper.LeftFlipper", "Flipper.RightFlipper", "Plunger.Plunger", "Kicker.Drain", "Light.l61", "Light.F23a", "Light.F23b", "Light.F32a", "Light.F32b", "Flasher.F28", "Flasher.F28a", "Flasher.F25", "Flasher.F26", "Flasher.F27"})
	return sorted(names)


def build_seed(register_path: Path, manifest_sha256: str) -> dict[str, Any]:
	"""Distil the extractor's register into the committed seed (needs the working-root extraction)."""
	register = json.loads(register_path.read_text(encoding="utf-8"))
	by_name = {f"{item['type']}.{item['name']}": item for item in register["objects"]}
	objects = {}
	for name in referenced_objects():
		item = by_name[name]
		objects[name] = [item["x"], item["y"], item["type"], item.get("source_path", f"gameitems/{item['type']}.{item['name']}.json")]
	return {
		"table_sha256": register["source"]["vpx_sha256"], "table_manifest_sha256": manifest_sha256, "bounds": register["bounds"],
		"normalization": {"helper": "pinmame_game_defs.spatial.extract_spatial_candidates", "x": "(raw_x - left) / (right - left)", "y": "(raw_y - top) / (bottom - top)", "vpxtool": register["source"]["vpxtool_version"]},
		"objects": dict(sorted(objects.items())),
	}



BUMPER_NOTE = "Spatial: placed on the pop bumper the manual's switch and coil location drawings put this device at. The retained table binds its rear Bumper1 to switch 32, Bumper2 to 31 and its front Bumper3 to 30, the reverse of the manual's order for the rear and front bumpers (switch 30 / coil Q11 is the rear 'top' bumper, 32 / Q9 the front 'bottom' bumper), so the placement follows the drawing and not the script."
SWITCH_NOTES: dict[int, str] = {
	1: "Spatial: projected onto the death post wall CPC; the up and down blade switches are part of the post assembly.",
	2: "Spatial: projected onto the death post wall CPC; the up and down blade switches are part of the post assembly.",
	30: BUMPER_NOTE, 31: BUMPER_NOTE, 32: BUMPER_NOTE,
	33: "Spatial: the table's LeftGate object; it is the only table object bound to this switch and its position was checked against the drawing.",
	35: "Spatial: the table's CastleGuardsw wall, the only object the table associates with this switch.",
	50: "Spatial: the table lays the Stewie mini-playfield over the upper right of the main playfield; the manual draws it as a separate inset. The placement is the table object's stored position in the main playfield space.",
	51: "Spatial: see switch 50 (mini-playfield object in the main playfield space).",
	52: "Spatial: see switch 50 (mini-playfield object in the main playfield space).",
	53: "Spatial: see switch 50 (mini-playfield object in the main playfield space).",
	54: "Spatial: see switch 50 (mini-playfield object in the main playfield space).",
	55: "Spatial: see switch 50 (mini-playfield object in the main playfield space).",
}
COIL_NOTES: dict[int, str] = {
	2: "Spatial: shares the shooter-lane trigger point; the table's autoplunger has no object of its own.",
	3: "Spatial: the mean of the four F-A-R-T drop target walls; the reset coil body is not modelled.",
	4: "Spatial: projected onto the death post wall CPC, not the coil body.",
	12: "Spatial: projected onto the death post wall CPC, not the coil body.",
	9: BUMPER_NOTE, 10: BUMPER_NOTE, 11: BUMPER_NOTE,
	14: "Spatial: the table's LeftFlipperSmall pivot; the upper-left flipper is driven by this coil.",
	20: "Spatial: the stored position of the table's Stewie figure primitive, not the stepper motor.",
	22: "Spatial: the stored position of the table's Meg figure primitive, not the mini-coil.",
	17: "Spatial: the table lays the Stewie mini-playfield over the upper right of the main playfield (see switch 50).",
	18: "Spatial: the table lays the Stewie mini-playfield over the upper right of the main playfield (see switch 50).",
	21: "Spatial: the table lays the Stewie mini-playfield over the upper right of the main playfield (see switch 50).",
}
COIL_GENERIC = "Spatial anchor: the mechanism object the coil drives, not a winding or coil-body centre."
LAMP_NOTES: dict[int, str] = {
	61: "Spatial: the table lights both l61 (on the rear bumper) and l61a (on the front bumper) from lamp 61; the manual puts the white LED module on the bottom, front bumper, which is l61a, so l61a is the placement.",
	68: "Spatial: the table lays the Stewie mini-playfield over the upper right of the main playfield (see switch 50).",
}
LED_NOTE = "Spatial: the table's LED object lying on this printed letter of the mini-playfield art (the manual's lamp drawing shows the letters). The retained table binds its BRIAN letter objects to lamps 125-121 and its CHRIS letter objects to 84-81 and 97, the reverse of the board's wiring, so each lamp here takes the LED object on the letter the board's LED carries, not the object the script binds to it. The table lays the mini-playfield over the upper right of the main playfield."
FLASHER_NOTES: dict[int, str] = {
	23: "Spatial: the table's F23 light at the yellow lower-left flash lamp; F23a and F23b are glow helpers of the same lamp.",
	29: "Spatial: the table's F29 light (the script names it for the Shrek-era flash 'Fiona'; the manual's flash 29 is Meg).",
	30: "Spatial: the table's F30 light at the right orbit.",
	31: "Spatial: the table's F31 light at the pop bumpers.",
	32: "Spatial: the table's F32 light at the yellow lower-right flash lamp; F32a and F32b are glow helpers of the same lamp.",
}


def _append(device: dict[str, Any], text: str) -> None:
	physical = device.setdefault("physical", {})
	physical["notes"] = (physical.get("notes", "") + " " + text).strip()


def attach(definition: dict[str, Any], seed: dict[str, Any]) -> dict[str, int]:
	"""Add spatial records to the definition's devices in place; returns counts for the report."""
	counts = {"located": 0, "not_applicable": 0}
	refs = (TABLE, MANUAL)
	for device in definition["inputs"]:
		address = device["binding"]["device"]
		group = device["binding"]["group"]
		if group == "pinmame.input.dip":
			device["spatial"] = not_applicable("dip_switch", MANUAL)
		elif device["availability"] == "unused":
			device["spatial"] = not_applicable("unused", MANUAL)
		elif 1 <= address <= 64 and address in SWITCH_OBJECTS:
			device["spatial"] = located(f"placement.switch-{address}.sensor", "sensor", seed, SWITCH_OBJECTS[address], *refs, SCRIPT)
			if address in SWITCH_NOTES:
				_append(device, SWITCH_NOTES[address])
		elif 1 <= address <= 64:
			if address in NOT_APPLICABLE_SWITCH_ROLES:
				device["spatial"] = not_applicable("cabinet_or_service", MANUAL)
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
			device["spatial"] = not_applicable("unused", MANUAL if group == "pinmame.output.lamp" else CORE)
		elif group == "physical.output.ticket":
			device["spatial"] = not_applicable("cabinet_or_service", MANUAL)
		elif group == "pinmame.output.solenoid":
			if address in COIL_OBJECTS:
				device["spatial"] = located(f"placement.coil-{address}.effect", "effect", seed, COIL_OBJECTS[address], *refs, SCRIPT)
				_append(device, COIL_NOTES.get(address, COIL_GENERIC))
			elif address in FLASHER_OBJECTS:
				device["spatial"] = located(f"placement.flasher-{address}.emitter", "emitter", seed, FLASHER_OBJECTS[address], *refs, SCRIPT)
				_append(device, FLASHER_NOTES[address])
		elif group == "pinmame.output.lamp":
			if address in LAMP_OBJECTS:
				device["spatial"] = located(f"placement.lamp-{address}.emitter", "emitter", seed, LAMP_OBJECTS[address], *refs, SCRIPT)
				if address in LAMP_NOTES:
					_append(device, LAMP_NOTES[address])
			elif address in LED_OBJECTS:
				device["spatial"] = located(f"placement.lamp-{address}.emitter", "emitter", seed, LED_OBJECTS[address], *refs, SCRIPT)
				_append(device, LED_NOTE)
			elif address in (1, 2):
				device["spatial"] = not_applicable("cabinet_or_service", MANUAL)
	for device in definition["inputs"] + definition["outputs"]:
		spatial = device.get("spatial")
		if spatial:
			counts["located" if "placements" in spatial else "not_applicable"] += 1
	return counts


if __name__ == "__main__":
	import argparse
	import sys

	import build_external_evidence_manifest as manifest
	from pinmame_game_defs.jsonio import canonical_bytes

	parser = argparse.ArgumentParser(description="Write the committed spatial seed from the retained table extraction.")
	parser.add_argument("--vpx-root", required=True, type=Path, help="working-root vpx-sources/stern/family-guy-2007")
	parser.add_argument("--write", action="store_true", required=True)
	arguments = parser.parse_args()
	digest = manifest.write_manifest(arguments.vpx_root, "family-guy-2007")
	seed = build_seed(arguments.vpx_root / "analysis/spatial-candidates.json", digest)
	SEED_PATH.write_bytes(canonical_bytes(seed))
	print(f"wrote {SEED_PATH.relative_to(ROOT)} with {len(seed['objects'])} objects, extraction manifest {digest}")
