#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Stern Terminator 3: Rise of the Machines (2003) curator.

The curator must reproduce byte for byte without the 78 MB table, so the objects it places are frozen in
``tools/seeds/stern/terminator-3-rise-of-the-machines-2003-spatial.json``. This tool rebuilds that seed from the
retained vpxtool extraction with the repository's own normalizing helper and refuses to write when the table hash or
bounds differ from the pinned Hanibal 1.5 table.

Each device lists the table objects its placement comes from. An object is chosen through the table's embedded
script binding (its Hit/Slingshot handler, cvpmBallStack/cvpmDropTarget/cvpmImpulseP registration, SolCallback target
or lamp copy), never from its name alone. Devices the manual mounts off the playfield (the back-panel switch 52,
ball stop Q21 and flashers Q30, and the backbox insert) are not placed here; the curator records them as cabinet
devices. A ``projection`` text marks a device whose sensor or actuator the table does
not model and that is projected onto the object of the mechanism it belongs to; a ``midpoint`` entry is the mean of
the named objects and is always a projection.

A light that sits on no bulb makes no socket (docs/SPATIAL.md, "Picking the bulb"), so a lamp is placed on a Light the
script drives for it only when that Light is a bulb Light (``is_bulb_light``) that shows its bulb mesh
(``show_bulb_mesh``). The script drives a bulb-mode Light for every lamp it binds: the Flasherupdate timer copies each
matrix insert ``l<n>`` onto ``l<n>a``, Lights(64) and Lights(71) bind ``l64`` and ``l71`` directly, and the timer copies
``l64`` onto ``l64a``. None of them shows a bulb mesh in the pinned table, so every lamp is listed under
``lamp_unplaced`` with the Light's two flags and any primitive drawing the image ``bulb`` within
``BULB_PRIMITIVE_DISTANCE`` of it, and ``lamp`` stays empty. Flashers 31 and 32 sit on bulb Lights that coincide with the
Flupper dome primitives the script swaps between DomeOn and DomeOff (within ``DOME_DISTANCE``). G.I. sockets are the
table's GIGruppe Lights collapsed into render doubles; a cluster with no member that draws a bulb mesh makes no socket
and is listed under ``gi_excluded`` instead.

    python tools/terminator_3_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> [--check]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.spatial import extract_spatial_candidates  # noqa: E402

SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "terminator-3-rise-of-the-machines-2003-spatial.json"
TABLE_SHA256 = "73376fbd167c87f8057b28bf3cd7a3cddb4ec9dc452be7819bde28ffdd44b303"
BOUNDS = {"left": 0.0, "top": 0.0, "right": 1025.0, "bottom": 2325.0}

TROUGH = "cvpmBallStack bsTrough (InitSw 0, 14, 13, 12, 11) has no switch objects; projected onto its release kicker BallRelease"
STACKING = "the table never writes the stacking opto (no handler or ball stack names switch 15); projected onto the trough release kicker BallRelease"
LOCKUP = "cvpmBallStack bstxhole (InitSw 0, 33, 34, 35) has no switch objects; projected onto its entry kicker txshot, whose Hit handler adds the ball"
TX_VUK = "bstxhole kicks from tvukout, the ball's exit at the cannon ramp; the manual's coil location drawing puts the T-X VUK coil in front of the T-X figure at the lockup, so it is projected onto the lockup entry kicker txshot"
EOS = "the end-of-stroke contact sits on the flipper assembly; projected onto the flipper the table animates"
DROP = "the 1-bank drop target's {coil} coil acts on the target dtdroptarget registers (initdrop sw25, 25); projected onto that target"
AUTO = "cvpmImpulseP plungerIM fires from the shooter-lane trigger swplunger"
UK_LEFT = "UK only and not modelled by the table; the coil location drawing (DR. 7) puts AUX 1 at the left outlane, projected onto its rollover sw57"
UK_CENTER = "UK only and not modelled by the table; the coil location drawing (DR. 7) puts AUX 2 between the flippers, projected onto the flippers' midpoint"
UK_RIGHT = "UK only and not modelled by the table; the coil location drawing (DR. 7) puts AUX 3 at the right outlane, projected onto its rollover sw60"

# Public switch -> [(VPX type, object, projection or None)]. A ("midpoint", "Type:a|Type:b", text) entry averages objects.
SWITCHES = {
	10: [("HitTarget", "sw10", None)],
	11: [("Kicker", "BallRelease", TROUGH)], 12: [("Kicker", "BallRelease", TROUGH)], 13: [("Kicker", "BallRelease", TROUGH)],
	14: [("Kicker", "BallRelease", TROUGH)], 15: [("Kicker", "BallRelease", STACKING)],
	16: [("Trigger", "ShooterLane", None)],
	17: [("HitTarget", "sw17", None)], 18: [("HitTarget", "sw18", None)], 19: [("HitTarget", "sw19", None)],
	20: [("HitTarget", "sw20", None)], 21: [("HitTarget", "sw21", None)], 22: [("HitTarget", "sw22", None)],
	23: [("HitTarget", "sw23", None)], 24: [("Trigger", "sw24", None)], 25: [("Wall", "sw25", None)],
	28: [("Trigger", "sw28", None)], 29: [("Trigger", "sw29", None)], 30: [("Trigger", "sw30", None)],
	31: [("Kicker", "txshot", None)], 32: [("Trigger", "sw32", None)],
	33: [("Kicker", "txshot", LOCKUP)], 34: [("Kicker", "txshot", LOCKUP)], 35: [("Kicker", "txshot", LOCKUP)],
	36: [("Kicker", "tophole", None)],
	37: [("Trigger", "sw37", None)], 38: [("Trigger", "sw38", None)], 39: [("Trigger", "sw39", None)], 40: [("Trigger", "sw40", None)],
	46: [("Trigger", "sw46", None)],
	49: [("Bumper", "Lbumper", None)], 50: [("Bumper", "RBumper", None)], 51: [("Bumper", "BBumper", None)],
	57: [("Trigger", "sw57", None)], 58: [("Trigger", "sw58", None)], 59: [("Wall", "LeftSlingshot", None)],
	60: [("Trigger", "sw60", None)], 61: [("Trigger", "sw61", None)], 62: [("Wall", "RightSlingshot", None)],
	81: [("Flipper", "RightFlipper", EOS)], 83: [("Flipper", "LeftFlipper", EOS)],
}
# Public solenoid -> [(VPX type, object, projection or None)].
SOLENOIDS = {
	1: [("Kicker", "BallRelease", None)], 2: [("Trigger", "swplunger", AUTO)],
	3: [("Wall", "sw25", DROP.format(coil="reset"))], 8: [("Wall", "sw25", DROP.format(coil="trip"))],
	9: [("Bumper", "Lbumper", None)], 10: [("Bumper", "RBumper", None)], 11: [("Bumper", "BBumper", None)],
	12: [("Plunger", "Kickback", None)], 13: [("Kicker", "vukout", None)], 14: [("Kicker", "txshot", TX_VUK)],
	17: [("Wall", "LeftSlingshot", None)], 18: [("Wall", "RightSlingshot", None)],
	22: [("Wall", "LeftPost", None)], 23: [("Wall", "CenterPost", None)],
	31: [("Light", "Flasher31a", None), ("Light", "Flasher31b", None)],
	32: [("Light", "Flasher32a", None), ("Light", "Flasher32b", None)],
	33: [("Trigger", "sw57", UK_LEFT)], 34: [("midpoint", "Flipper:LeftFlipper|Flipper:RightFlipper", UK_CENTER)],
	35: [("Trigger", "sw60", UK_RIGHT)],
	45: [("Flipper", "RightFlipper", None)], 46: [("Flipper", "RightFlipper", None)],
	47: [("Flipper", "LeftFlipper", None)], 48: [("Flipper", "LeftFlipper", None)],
}
# Each flasher Light and the dome primitive it must sit in front of (within DOME_DISTANCE).
DOMES = {
	"Flasher31a": "Flasher31p1", "Flasher31b": "Flasher31p2", "Flasher32a": "Flasher32p1", "Flasher32b": "Flasher32p2",
}
DOME_DISTANCE = 0.002  # normalized; the light and its dome coincide
# Public lamp -> [(Light the script drives for it, how the script drives it)].
LAMP_LIGHTS: dict[int, list[tuple[str, str]]] = {
	address: [(f"l{address}a", f"the Flasherupdate timer's Kombilicht {address} copies insert l{address} onto it")]
	for address in list(range(1, 53)) + list(range(55, 63)) + [72, 80]
}
LAMP_LIGHTS[64] = [("l64", "Lights(64) binds it directly"), ("l64a", "the Flasherupdate timer's Kombiflasher2 136 copies l64 onto it")]
LAMP_LIGHTS[71] = [("l71", "Lights(71) binds it directly")]
BULB_PRIMITIVE_DISTANCE = 0.006  # normalized
STACK_DISTANCE = 0.010  # normalized; render doubles closer than this are one socket


def _candidates(extracted: Path, vpx: Path) -> dict[tuple[str, str], dict]:
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned Terminator 3 Hanibal 1.5 table")
	if candidates["bounds"] != BOUNDS:
		raise SystemExit(f"unexpected table bounds {candidates['bounds']}")
	return {(item["type"], item["name"]): item for item in candidates["objects"]}


def _point(by_key: dict, kind: str, name: str) -> tuple[float, float]:
	found = by_key.get((kind, name))
	if found is None:
		raise SystemExit(f"missing table object {kind} {name}")
	return found["x"], found["y"]


def _light(extracted: Path, name: str) -> dict:
	return json.loads((extracted / "gameitems" / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]


def _primitive(extracted: Path, name: str) -> dict:
	return json.loads((extracted / "gameitems" / f"Primitive.{name}.json").read_text(encoding="utf-8"))["Primitive"]


def _entries(extracted: Path, by_key: dict, rows: list[tuple[str, str, str | None]]) -> list[dict]:
	entries = []
	for kind, name, note in rows:
		if kind == "midpoint":
			points = [_point(by_key, *part.split(":")) for part in name.split("|")]
			x = round(sum(p[0] for p in points) / len(points), 6)
			y = round(sum(p[1] for p in points) / len(points), 6)
			entry = {"object": " + ".join(part.split(":")[1] for part in name.split("|")), "type": "midpoint", "x": x, "y": y}
		else:
			x, y = _point(by_key, kind, name)
			entry = {"object": name, "type": kind, "x": x, "y": y}
			if kind == "Light":
				light = _light(extracted, name)
				if not light.get("is_bulb_light") or light.get("is_backglass"):
					raise SystemExit(f"{name} is not a playfield bulb Light")
			if name in DOMES:
				dome = DOMES[name]
				if math.dist((x, y), _point(by_key, "Primitive", dome)) >= DOME_DISTANCE:
					raise SystemExit(f"{name} no longer sits at the dome primitive {dome}")
				if str(_primitive(extracted, dome).get("image") or "").casefold() != "domeoff":
					raise SystemExit(f"{dome} is no longer a Flupper dome drawing DomeOff at rest")
				entry["dome"] = dome
		if note:
			entry["note" if kind == "Light" else "projection"] = note
		entries.append(entry)
	return entries


def _lamps(extracted: Path, by_key: dict) -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
	"""Lamp -> placements on the Lights that show their bulb mesh, and lamp -> the Lights that show none.

	Fail closed: a Light is placed only when ``is_bulb_light`` and ``show_bulb_mesh`` are both true. A primitive drawing
	the image ``bulb`` near an unplaced Light is recorded for the note, never used as a placement."""
	bulb_primitives = []
	for (kind, name), item in by_key.items():
		if kind == "Primitive":
			primitive = _primitive(extracted, name)
			if str(primitive.get("image") or "").casefold() == "bulb":
				bulb_primitives.append((name, primitive.get("material"), (item["x"], item["y"])))
	placed: dict[str, list[dict]] = {}
	unplaced: dict[str, list[dict]] = {}
	for address, rows in sorted(LAMP_LIGHTS.items()):
		for name, binding in rows:
			x, y = _point(by_key, "Light", name)
			light = _light(extracted, name)
			if light.get("is_backglass"):
				raise SystemExit(f"{name} is a backglass Light")
			if light.get("is_bulb_light") is True and light.get("show_bulb_mesh") is True:
				placed.setdefault(str(address), []).append({"object": name, "type": "Light", "x": x, "y": y, "note": binding})
				continue
			near = sorted(
				({"object": primitive, "material": material, "distance": round(math.dist((x, y), point), 4)}
					for primitive, material, point in bulb_primitives if math.dist((x, y), point) < BULB_PRIMITIVE_DISTANCE),
				key=lambda item: (item["distance"], item["object"]),
			)
			unplaced.setdefault(str(address), []).append({
				"object": name, "binding": binding, "is_bulb_light": bool(light.get("is_bulb_light")),
				"show_bulb_mesh": bool(light.get("show_bulb_mesh")), "bulb_primitives": near,
			})
	return placed, unplaced


def _gi(extracted: Path, by_key: dict) -> tuple[list[dict], list[dict]]:
	"""One socket per render-double cluster that draws a bulb, placed on that member (docs/SPATIAL.md)."""
	collections = {item["name"]: item["items"] for item in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))}
	members = collections["GIGruppe"]
	lights = sorted((name for name in members if ("Light", name) in by_key), key=str.casefold)
	if len(lights) != len(members):
		raise SystemExit("a GIGruppe member is not a playfield Light")
	clusters: list[list[str]] = []
	for name in lights:
		point = _point(by_key, "Light", name)
		for cluster in clusters:
			if math.dist(_point(by_key, "Light", cluster[0]), point) < STACK_DISTANCE:
				cluster.append(name)
				break
		else:
			clusters.append([name])
	placed: list[dict] = []
	excluded: list[dict] = []
	for cluster in clusters:
		def rank(name: str) -> tuple[bool, float, str]:
			light = _light(extracted, name)
			return (not light["show_bulb_mesh"], float(light["falloff_radius"]), name.casefold())
		chosen = min(cluster, key=rank)
		x, y = _point(by_key, "Light", chosen)
		entry = {"object": chosen, "collapsed": sorted(cluster, key=str.casefold), "x": x, "y": y}
		(excluded if rank(chosen)[0] else placed).append(entry)
	return placed, excluded


def build(extracted: Path, vpx: Path) -> dict:
	by_key = _candidates(extracted, vpx)
	placed, excluded = _gi(extracted, by_key)
	lamps, unplaced_lamps = _lamps(extracted, by_key)
	return {
		"format": "pinmame-terminator-3-spatial-seed",
		"version": 1,
		"machine_id": "stern.terminator-3-rise-of-the-machines.2003",
		"table": {"sha256": TABLE_SHA256, "width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx"},
		"switch": {str(address): _entries(extracted, by_key, rows) for address, rows in sorted(SWITCHES.items())},
		"solenoid": {str(address): _entries(extracted, by_key, rows) for address, rows in sorted(SOLENOIDS.items())},
		"lamp": lamps,
		"lamp_unplaced": unplaced_lamps,
		"gi": {"0": placed},
		"gi_excluded": {"0": excluded},
	}


def canonical(value: dict) -> str:
	return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--extracted", type=Path, required=True)
	parser.add_argument("--vpx", type=Path, required=True)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = canonical(build(args.extracted, args.vpx))
	if args.check:
		if not SEED_PATH.is_file() or SEED_PATH.read_bytes() != text.encode("utf-8"):
			raise SystemExit(f"Terminator 3 spatial seed drift: {SEED_PATH}")
		print("Terminator 3 spatial seed matches the retained extraction.")
		return
	SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"Wrote {SEED_PATH}")


if __name__ == "__main__":
	main()
