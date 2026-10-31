#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Stern Elvis (2004) curator.

The curator must reproduce byte for byte without the retained table, so the objects it places are frozen in
``tools/seeds/stern/elvis-2004-spatial.json``. This tool rebuilds that seed from the retained vpxtool extraction with the
repository's own normalizing helper and refuses to write when the table hash or bounds differ from the pinned 1.0.2
table.

Each device lists the table objects its placement comes from. An object is chosen through the table's embedded script
binding (its Hit/Slingshot/Spin handler, cvpmBallStack/cvpmMagnet/cvpmImpulseP/cvpmDropTarget registration, SolCallback
target or lamp fader), never from its name alone. A ``projection`` text marks a device whose sensor or actuator the table
does not model and that is projected onto the object of the mechanism it belongs to; a ``midpoint`` entry is the mean of
the named objects and is always a projection. Lamp entries are the insert Lights UpdateLamps fades; the curator places
none of them, because every one is an insert overlay with no bulb, and only names the Light in the lamp's note.

    python tools/elvis_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> [--check]
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

SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "elvis-2004-spatial.json"
TABLE_SHA256 = "d53202dea8620d92b6598894e71b26de59db1a0932234ceb5938f0844d22afc6"
BOUNDS = {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2115.0}

TROUGH = "cvpmBallStack bsTrough (InitSw 0, 14, 13, 12, 11) has no switch objects; projected onto its release kicker BallRelease"
STACKING = "the table writes the stacking opto only as a vpmTimer pulse inside SolTrough and has no object for it; projected onto the trough release kicker BallRelease"
ELVIS = (
	"the cvpmMech mElvis (Sol1 = 25, AddSw 33) models the figure's travel with no switch, motor or coil object; projected onto "
	"the figure's stand primitive pStand, which UpdateElvis moves"
)
EOS = "the end-of-stroke contact sits on the flipper assembly; projected onto the flipper the table animates"
BANK = "the reset coil sits under the 5-bank; projected onto the mean of the bank's five drop targets"
DOME = "a script-driven glow Light centred on a modelled flasher dome primitive"
INSERT = "an insert Light UpdateLamps fades; no bulb (is_bulb_light and show_bulb_mesh false)"

# Public switch -> [(VPX type, object, projection or None)]. A ("midpoint", "Type:a|Type:b", text) entry averages objects.
SWITCHES = {
	9: [("HitTarget", "sw9", None)],
	11: [("Kicker", "BallRelease", TROUGH)], 12: [("Kicker", "BallRelease", TROUGH)], 13: [("Kicker", "BallRelease", TROUGH)],
	14: [("Kicker", "BallRelease", TROUGH)], 15: [("Kicker", "BallRelease", STACKING)],
	16: [("Trigger", "swPlunger", None)],
	17: [("HitTarget", "sw17", None)], 18: [("HitTarget", "sw18", None)], 19: [("HitTarget", "sw19", None)], 20: [("HitTarget", "sw20", None)],
	21: [("HitTarget", "sw21", None)], 22: [("HitTarget", "sw22", None)], 23: [("HitTarget", "sw23", None)], 24: [("HitTarget", "sw24", None)],
	25: [("Spinner", "sw25", None)], 26: [("Trigger", "sw26", None)], 27: [("Trigger", "sw27", None)], 28: [("Trigger", "sw28", None)],
	30: [("Trigger", "sw30", None)], 31: [("Trigger", "sw31", None)], 32: [("Kicker", "sw32", None)],
	33: [("Primitive", "pStand", ELVIS)], 34: [("Kicker", "sw34", None)],
	36: [("HitTarget", "sw36", None)], 37: [("HitTarget", "sw37", None)], 38: [("HitTarget", "sw38", None)], 39: [("HitTarget", "sw39", None)],
	40: [("HitTarget", "sw40", None)], 41: [("Trigger", "sw41", None)], 42: [("Trigger", "sw42", None)], 43: [("Trigger", "sw43", None)],
	45: [("Trigger", "sw45", None)], 46: [("Trigger", "sw46", None)], 47: [("Trigger", "sw47", None)], 48: [("Trigger", "sw48", None)],
	49: [("Bumper", "Bumper1", None)], 50: [("Bumper", "Bumper2", None)], 51: [("Bumper", "Bumper3", None)],
	52: [("HitTarget", "sw52", None)], 53: [("HitTarget", "sw53", None)],
	57: [("Trigger", "sw57", None)], 58: [("Trigger", "sw58", None)], 59: [("Wall", "LeftSlingshot", None)],
	60: [("Trigger", "sw60", None)], 61: [("Trigger", "sw61", None)], 62: [("Wall", "RightSlingshot", None)],
	63: [("Trigger", "sw63", None)], 64: [("Primitive", "sw64", None)],
	81: [("Flipper", "RightFlipper", EOS)], 83: [("Flipper", "LeftFlipper", EOS)],
}
# Public solenoid -> [(VPX type, object, projection or None)].
SOLENOIDS = {
	1: [("Kicker", "BallRelease", None)], 2: [("Trigger", "swPlunger", None)],
	3: [("midpoint", "HitTarget:sw17|HitTarget:sw18|HitTarget:sw19|HitTarget:sw20|HitTarget:sw21", BANK)],
	5: [("Trigger", "Magnet", None)], 6: [("Kicker", "sw34", None)], 7: [("Kicker", "HLock", None)], 8: [("Gate", "CGate", None)],
	9: [("Bumper", "Bumper1", None)], 10: [("Bumper", "Bumper2", None)], 11: [("Bumper", "Bumper3", None)], 12: [("Kicker", "sw32", None)],
	13: [("Flipper", "LeftFlipper1", None)], 14: [("Flipper", "RightFlipper1", None)],
	17: [("Wall", "LeftSlingshot", None)], 18: [("Wall", "RightSlingshot", None)], 19: [("Wall", "doorwall", None)],
	22: [("Light", "Flasherlight3", DOME)],
	25: [("Primitive", "pStand", ELVIS)], 26: [("Primitive", "pStand", ELVIS)], 27: [("Primitive", "pStand", ELVIS)],
	28: [("Primitive", "pStand", ELVIS)], 29: [("Primitive", "pStand", ELVIS)], 30: [("Primitive", "pStand", ELVIS)],
	32: [("Light", "Flasherlight1", DOME), ("Light", "Flasherlight2", DOME)],
	46: [("Flipper", "RightFlipper", None)], 48: [("Flipper", "LeftFlipper", None)],
}
# Each flasher Light and the dome primitive it must sit on (within DOME_DISTANCE).
DOMES = {"Flasherlight1": "Flasherbase1", "Flasherlight2": "Flasherbase2", "Flasherlight3": "Flasherbase3"}
DOME_DISTANCE = 0.005
# Public lamp -> [(VPX type, object, note)]: the insert Light UpdateLamps fades for lamp n.
LAMPS: dict[int, list[tuple[str, str, str | None]]] = {
	address: [("Light", f"l{address}", INSERT)] for address in list(range(1, 60)) + [63, 64]
}
STACK_DISTANCE = 0.010  # normalized; render doubles closer than this are one socket


def _candidates(extracted: Path, vpx: Path) -> dict[tuple[str, str], dict]:
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned Elvis 1.0.2 table")
	if candidates["bounds"] != BOUNDS:
		raise SystemExit(f"unexpected table bounds {candidates['bounds']}")
	return {(item["type"], item["name"]): item for item in candidates["objects"]}


def _point(by_key: dict, kind: str, name: str) -> tuple[float, float]:
	found = by_key.get((kind, name))
	if found is None:
		raise SystemExit(f"missing table object {kind} {name}")
	return found["x"], found["y"]


def _entries(by_key: dict, rows: list[tuple[str, str, str | None]]) -> list[dict]:
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
			if name in DOMES:
				dome = DOMES[name]
				if math.dist((x, y), _point(by_key, "Primitive", dome)) >= DOME_DISTANCE:
					raise SystemExit(f"{name} no longer sits on the dome primitive {dome}")
				entry["dome"] = dome
		if note:
			entry["note" if kind == "Light" else "projection"] = note
		entries.append(entry)
	return entries


def _gi(extracted: Path, by_key: dict) -> dict[str, list]:
	"""One socket per render-double cluster that draws a bulb, placed on that member (docs/SPATIAL.md).

	A cluster none of whose Lights shows its bulb mesh sits on no bulb: no primitive models a socket under it (the nearest are
	posts, pegs and screws), so it makes no socket and is listed as unplaced instead.
	"""
	collections = {item["name"]: item["items"] for item in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))}
	lights = sorted((name for name in collections["aGiLights"] if ("Light", name) in by_key), key=str.casefold)
	if len(lights) != len(collections["aGiLights"]):
		raise SystemExit("a GI collection member is not a playfield Light")
	clusters: list[list[str]] = []
	for name in lights:
		point = _point(by_key, "Light", name)
		for cluster in clusters:
			if math.dist(_point(by_key, "Light", cluster[0]), point) < STACK_DISTANCE:
				cluster.append(name)
				break
		else:
			clusters.append([name])
	groups: list[dict] = []
	unplaced: list[str] = []
	for cluster in clusters:
		def rank(name: str) -> tuple[bool, float, str]:
			light = json.loads((extracted / "gameitems" / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]
			return (not (light["is_bulb_light"] and light["show_bulb_mesh"]), float(light["falloff_radius"]), name.casefold())
		chosen = min(cluster, key=rank)
		if rank(chosen)[0]:
			unplaced.extend(cluster)
			continue
		x, y = _point(by_key, "Light", chosen)
		groups.append({"object": chosen, "collapsed": sorted(cluster, key=str.casefold), "x": x, "y": y})
	return {"placed": groups, "no_bulb": sorted(unplaced, key=str.casefold)}


def build(extracted: Path, vpx: Path) -> dict:
	by_key = _candidates(extracted, vpx)
	gi = _gi(extracted, by_key)
	return {
		"format": "pinmame-elvis-spatial-seed",
		"version": 1,
		"machine_id": "stern.elvis.2004",
		"table": {"sha256": TABLE_SHA256, "width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx"},
		"switch": {str(address): _entries(by_key, rows) for address, rows in sorted(SWITCHES.items())},
		"solenoid": {str(address): _entries(by_key, rows) for address, rows in sorted(SOLENOIDS.items())},
		"lamp": {str(address): _entries(by_key, rows) for address, rows in sorted(LAMPS.items())},
		"gi": {"0": gi["placed"]},
		"gi_without_bulb": {"0": gi["no_bulb"]},
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
			raise SystemExit(f"Elvis spatial seed drift: {SEED_PATH}")
		print("Elvis spatial seed matches the retained extraction.")
		return
	SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"Wrote {SEED_PATH}")


if __name__ == "__main__":
	main()
