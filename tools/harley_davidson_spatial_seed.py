#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Stern Harley-Davidson (1999) curator.

The curator must reproduce byte for byte without the retained table, so the objects it places are frozen in
``tools/seeds/stern/harley-davidson-1999-spatial.json``. This tool rebuilds that seed from the retained vpxtool
extraction with the repository's own normalizing helper and refuses to write when the table hash or bounds differ from
the pinned 1.2 table.

Each device lists the table objects its placement comes from. An object is chosen through the table's embedded
script binding (its Hit/Slingshot/Spin handler, cvpmBallStack/cvpmMagnet registration, SolCallback target or lamp
fader), never from its name alone. A ``projection`` text marks a device whose sensor or actuator the table does not
model and that is projected onto the object of the mechanism it belongs to; a ``midpoint`` entry is the mean of the
named objects and is always a projection.

    python tools/harley_davidson_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> [--check]
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

SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "harley-davidson-1999-spatial.json"
TABLE_SHA256 = "349bc4e4d68173138928baed0a0fbfdb0d04ef78ca07dfbcfdf8d2583255cf37"
BOUNDS = {"left": 0.0, "top": 0.0, "right": 1000.0, "bottom": 2000.0}

TROUGH = "cvpmBallStack bsTrough (InitSw 0, 14, 13, 12, 11) has no switch objects; projected onto its release kicker BallRelease"
STACKING = "the table never writes the stacking opto (SolTrough, its only writer, is not bound); projected onto the trough release kicker BallRelease"
CYCLE_TROUGH = "cvpmBallStack bsCycle (InitSw 0, 44, 43, 42, 41; InitKick Kicker1) has no switch objects; projected onto its kicker Kicker1"
LIFT = "the cvpmMech mCycle (Sol1 = 19, AddSw 35 and 36) models the lift with no switch or motor object; projected onto the motorcycle trough's kicker Kicker1"
EOS = "the end-of-stroke contact sits on the flipper assembly; projected onto the flipper the table animates"
BANK = "the reset coil sits under its 4-bank; projected onto the mean of the bank's four drop targets"
UK_LEFT = "UK only and not modelled by the US table; the cabinet wiring diagram's UK note puts the deflector at the left outlane, projected onto its rollover sw57"
UK_RIGHT = "UK only and not modelled by the US table; the cabinet wiring diagram's UK note puts the deflector at the right outlane, projected onto its rollover sw60"
DOME = "a script-driven glow Light centred on a modelled flasher dome primitive"

# Public switch -> [(VPX type, object, projection or None)]. A ("midpoint", "Type:a|Type:b", text) entry averages objects.
SWITCHES = {
	11: [("Kicker", "BallRelease", TROUGH)], 12: [("Kicker", "BallRelease", TROUGH)], 13: [("Kicker", "BallRelease", TROUGH)],
	14: [("Kicker", "BallRelease", TROUGH)], 15: [("Kicker", "BallRelease", STACKING)],
	16: [("Kicker", "Kicker2", None)],
	17: [("HitTarget", "sw17", None)], 18: [("HitTarget", "sw18", None)], 19: [("HitTarget", "sw19", None)], 20: [("HitTarget", "sw20", None)],
	21: [("HitTarget", "sw21", None)], 22: [("HitTarget", "sw22", None)], 23: [("HitTarget", "sw23", None)], 24: [("HitTarget", "sw24", None)],
	25: [("Gate", "sw25", None)], 26: [("Trigger", "Trigger26", None)], 28: [("Spinner", "Spinner1", None)],
	29: [("HitTarget", "sw29", None)], 30: [("HitTarget", "sw30", None)], 31: [("HitTarget", "sw31", None)], 32: [("HitTarget", "sw32", None)],
	33: [("Trigger", "sw33", None)], 34: [("Trigger", "sw34", None)],
	35: [("Kicker", "Kicker1", LIFT)], 36: [("Kicker", "Kicker1", LIFT)], 37: [("Trigger", "sw37", None)],
	41: [("Kicker", "Kicker1", CYCLE_TROUGH)], 42: [("Kicker", "Kicker1", CYCLE_TROUGH)], 43: [("Kicker", "Kicker1", CYCLE_TROUGH)],
	44: [("Kicker", "Kicker1", CYCLE_TROUGH)],
	45: [("Kicker", "Sw45", None)], 46: [("Kicker", "sw46", None)], 48: [("Trigger", "sw48", None)],
	49: [("Bumper", "Bumper2b", None)], 50: [("Bumper", "Bumper3b", None)], 51: [("Bumper", "Bumper1b", None)], 52: [("Bumper", "Bumper4b", None)],
	57: [("Trigger", "sw57", None)], 58: [("Trigger", "sw58", None)], 59: [("Wall", "LeftSlingShot", None)],
	60: [("Trigger", "sw60", None)], 61: [("Trigger", "sw61", None)], 62: [("Wall", "RightSlingShot", None)],
	81: [("Flipper", "RightFlipper", EOS)], 83: [("Flipper", "LeftFlipper", EOS)],
}
# Public solenoid -> [(VPX type, object, projection or None)].
SOLENOIDS = {
	1: [("Kicker", "BallRelease", None)], 2: [("Kicker", "Kicker2", None)], 3: [("Kicker", "Sw45a", None)], 4: [("Kicker", "sw46", None)],
	5: [("Kicker", "Kicker1", None)],
	6: [("midpoint", "HitTarget:sw17|HitTarget:sw18|HitTarget:sw19|HitTarget:sw20", BANK)],
	7: [("midpoint", "HitTarget:sw21|HitTarget:sw22|HitTarget:sw23|HitTarget:sw24", BANK)],
	9: [("Bumper", "Bumper2b", None)], 10: [("Bumper", "Bumper3b", None)], 11: [("Bumper", "Bumper1b", None)], 12: [("Bumper", "Bumper4b", None)],
	14: [("Trigger", "MagTrig", None)], 17: [("Wall", "LeftSlingShot", None)], 18: [("Wall", "RightSlingShot", None)],
	19: [("Kicker", "Kicker1", LIFT)],
	21: [("Trigger", "sw57", UK_LEFT)], 22: [("Trigger", "sw60", UK_RIGHT)], 23: [("Wall", "Wall32", None)],
	26: [("Light", "L102", DOME), ("Light", "L102a", DOME)], 28: [("Light", "L104", DOME), ("Light", "L104a", DOME)],
	46: [("Flipper", "RightFlipper", None)], 48: [("Flipper", "LeftFlipper", None)],
}
# Each flasher Light and the dome primitive it must sit on (within DOME_DISTANCE).
DOMES = {"L102": "Flash002", "L102a": "Flash001", "L104": "Flash26", "L104a": "Flash32"}
DOME_DISTANCE = 0.005
# Public lamp -> [(VPX type, object, note or None)]: the Light UpdateLamps fades for lamp n.
LAMPS: dict[int, list[tuple[str, str, str | None]]] = {
	address: [("Light", f"L{address}", None)] for address in list(range(1, 47)) + list(range(48, 52)) + [65, 66, 67, 68, 69, 71]
}
LAMPS[70] = [("Light", "L70", None), ("Light", "L70a", None)]
STACK_DISTANCE = 0.010  # normalized; render doubles closer than this are one socket


def _candidates(extracted: Path, vpx: Path) -> dict[tuple[str, str], dict]:
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned Harley-Davidson 1.2 table")
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


def _gi(extracted: Path, by_key: dict) -> list[dict]:
	"""One socket per render-double cluster, placed on the member that draws the bulb (docs/SPATIAL.md)."""
	collections = {item["name"]: item["items"] for item in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))}
	lights = sorted((name for name in collections["GI"] if ("Light", name) in by_key), key=str.casefold)
	if len(lights) != len(collections["GI"]):
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
	for cluster in clusters:
		def rank(name: str) -> tuple[bool, float, str]:
			light = json.loads((extracted / "gameitems" / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]
			return (not light["show_bulb_mesh"], float(light["falloff_radius"]), name.casefold())
		chosen = min(cluster, key=rank)
		if rank(chosen)[0]:
			raise SystemExit(f"GI cluster {cluster} draws no bulb")
		x, y = _point(by_key, "Light", chosen)
		groups.append({"object": chosen, "collapsed": sorted(cluster, key=str.casefold), "x": x, "y": y})
	return groups


def build(extracted: Path, vpx: Path) -> dict:
	by_key = _candidates(extracted, vpx)
	return {
		"format": "pinmame-harley-davidson-spatial-seed",
		"version": 1,
		"machine_id": "stern.harley-davidson.1999",
		"table": {"sha256": TABLE_SHA256, "width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx"},
		"switch": {str(address): _entries(by_key, rows) for address, rows in sorted(SWITCHES.items())},
		"solenoid": {str(address): _entries(by_key, rows) for address, rows in sorted(SOLENOIDS.items())},
		"lamp": {str(address): _entries(by_key, rows) for address, rows in sorted(LAMPS.items())},
		"gi": {"0": _gi(extracted, by_key)},
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
			raise SystemExit(f"Harley-Davidson spatial seed drift: {SEED_PATH}")
		print("Harley-Davidson spatial seed matches the retained extraction.")
		return
	SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"Wrote {SEED_PATH}")


if __name__ == "__main__":
	main()
