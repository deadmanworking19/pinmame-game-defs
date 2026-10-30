#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Sega South Park (1999) curator.

The curator must reproduce byte for byte without the retained table, so the objects it places are frozen in
``tools/seeds/sega/south-park-1999-spatial.json``. This tool rebuilds that seed from the retained vpxtool extraction
with the repository's own normalizing helper and refuses to write when the table hash or bounds differ from the pinned
Knorr 1.3 table.

Each device lists the table objects its placement comes from. An object is chosen through the table's embedded
script binding (its Hit/Slingshot handler, cvpmBallStack/cvpmSaucer registration, SolCallback target or lamp
assignment), never from its name alone. A ``projection`` text marks a device whose sensor or actuator the table does
not model and that is projected onto the object of the mechanism it belongs to; a ``midpoint`` entry is the mean of
two named objects and is always a projection.

    python tools/south_park_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> [--check]
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

SEED_PATH = ROOT / "tools" / "seeds" / "sega" / "south-park-1999-spatial.json"
TABLE_SHA256 = "39075dcb6ca5fb8f164a9d48b6e4b393fef85eae3607892f19f28318a4f8d1a8"
BOUNDS = {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2162.0}

TROUGH = "cvpmBallStack bsTrough (InitSw 0, 14, 13, 12, 11, 10) has no switch objects; projected onto its release kicker BallRelease"
STACKING = "the table models no stacking opto (SolRelease's PulseSw 15 is commented out); projected onto the trough release kicker BallRelease"
EOS = "the end-of-stroke contact sits on the flipper assembly; projected onto the flipper the table animates"
UNDER_TOILET = "ToiletKicker_Hit pulses 43 for the under-trough switch below the toilet; projected onto that kicker"
UNDER_KENNY = "KennyKickerHole through KennyKickerHole5 pulse 44 for the under-trough switch below Kenny; projected onto KennyKickerHole"
UNDER_SVUK = "CartmanKickerHole through CartmanKickerHole7 pulse 48 for the under-trough switch below the playfield hole; projected onto CartmanKickerHole"
AUTO = "AutoLaunch fires the table's Plunger object with Autoplunger set"
TOILET = "ToiletSeatLid rotates the invisible helper flipper ToiletFlipper that the ToiletSeat primitive follows; projected onto that primitive"
HANKEY = "MrHankeyUp/MrHankeyDown rotate the helper flippers MrHankeyFlipper and CisternFlipper the MrHankey primitive follows; projected onto that primitive"
KENNY = "KennyDead/KennyLeft/KennyRight rotate the Kenny primitive; projected onto it"
KENNY_FLASH = "FlashKennyandBack swaps the Kenny primitive for its lit copy KennyL; the #906 bulb inside Kenny is projected onto the Kenny primitive"
UK_LEFT = "the US table models no UK outlane deflector; the coil location drawing (DR. 7) draws coil 21 at the left outlane, projected onto its rollover sw57"
UK_RIGHT = "the US table models no UK outlane deflector; the coil location drawing (DR. 7) draws coil 22 at the right outlane, projected onto its rollover sw60"
UK_POST = "the US table models no UK up/down post; the coil location drawing (DR. 7) draws coil 23 between the flippers, projected onto the flippers' midpoint"

# Public switch -> [(VPX type, object, projection or None)]. A ("midpoint", "a|b", text) entry averages two objects.
SWITCHES = {
	10: [("Kicker", "BallRelease", TROUGH)], 11: [("Kicker", "BallRelease", TROUGH)], 12: [("Kicker", "BallRelease", TROUGH)],
	13: [("Kicker", "BallRelease", TROUGH)], 14: [("Kicker", "BallRelease", TROUGH)], 15: [("Kicker", "BallRelease", STACKING)],
	16: [("Trigger", "sw16", None)],
	17: [("Wall", "T17", None)], 18: [("Wall", "T18", None)], 19: [("Wall", "T19", None)], 20: [("Wall", "T20", None)], 21: [("Wall", "T21", None)],
	22: [("Wall", "T22", None)], 23: [("Wall", "T23", None)], 24: [("Wall", "T24", None)],
	25: [("Trigger", "sw25", None)], 26: [("Trigger", "sw26", None)],
	34: [("Wall", "T34", None)], 35: [("Wall", "T35", None)], 36: [("Wall", "T36", None)], 37: [("Wall", "T37", None)], 38: [("Wall", "T38", None)],
	42: [("Trigger", "sw42", None)], 43: [("Kicker", "ToiletKicker", UNDER_TOILET)], 44: [("Kicker", "KennyKickerHole", UNDER_KENNY)],
	45: [("Kicker", "sw45", None)], 46: [("Kicker", "sw46", None)], 47: [("Trigger", "sw47", None)], 48: [("Kicker", "CartmanKickerHole", UNDER_SVUK)],
	49: [("Bumper", "LeftBumper", None)], 50: [("Bumper", "RightBumper", None)], 51: [("Bumper", "BottomBumper", None)],
	57: [("Trigger", "sw57", None)], 58: [("Trigger", "sw58", None)], 59: [("Wall", "LeftSlingShot", None)],
	60: [("Trigger", "sw60", None)], 61: [("Trigger", "sw61", None)], 62: [("Wall", "RightSlingShot", None)],
	81: [("Flipper", "FlipperRight", EOS)], 83: [("Flipper", "FlipperLeft", EOS)],
}
# Public solenoid -> [(VPX type, object, projection or None)].
SOLENOIDS = {
	1: [("Kicker", "BallRelease", None)], 2: [("Plunger", "Plunger", AUTO)], 3: [("Kicker", "sw45", None)], 4: [("Kicker", "sw46", None)],
	5: [("Primitive", "ToiletSeat", TOILET)], 6: [("Primitive", "MrHankey", HANKEY)],
	7: [("Light", "FPa", None), ("Light", "Fpb", None), ("Light", "FPc", None), ("Light", "FPd", None)],
	9: [("Bumper", "LeftBumper", None)], 10: [("Bumper", "RightBumper", None)], 11: [("Bumper", "BottomBumper", None)],
	12: [("Wall", "LeftSlingShot", None)], 13: [("Primitive", "MrHankey", HANKEY)], 14: [("Primitive", "Kenny", KENNY)],
	17: [("Wall", "RightSlingShot", None)], 18: [("Light", "F18", None)], 19: [("Primitive", "Kenny", KENNY)], 20: [("Primitive", "Kenny", KENNY)],
	21: [("Trigger", "sw57", UK_LEFT)], 22: [("Trigger", "sw60", UK_RIGHT)], 23: [("midpoint", "Flipper:FlipperLeft|Flipper:FlipperRight", UK_POST)],
	25: [("Light", "F1", None), ("Light", "F1a", None)], 26: [("Light", "F2", None), ("Light", "F2a", None)],
	27: [("Light", "F3", None), ("Light", "F3a", None)], 28: [("Light", "F4", None), ("Light", "F4a", None)],
	29: [("Light", "F5", None), ("Light", "F5a", None)], 30: [("Primitive", "Kenny", KENNY_FLASH)],
	31: [("Light", "F7l", None), ("Light", "F7r", None)], 32: [("Light", "F8", None)],
	45: [("Flipper", "FlipperRight", None)], 46: [("Flipper", "FlipperRight", None)],
	47: [("Flipper", "FlipperLeft", None)], 48: [("Flipper", "FlipperLeft", None)],
}
# Public lamp -> [(VPX type, object, note or None)]: the Light InitLamps assigns to Lights(n).
LAMPS: dict[int, list[tuple[str, str, str | None]]] = {
	address: [("Light", f"l{address}", None)] for address in list(range(1, 31)) + list(range(33, 47)) + [48] + list(range(50, 65))
}
STACK_DISTANCE = 0.010  # normalized; the table doubles each GI socket as a Gi/Gis pair up to 0.009 apart


def _candidates(extracted: Path, vpx: Path) -> dict[tuple[str, str], dict]:
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned South Park 1.3 table")
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
			entry = {"object": name.replace("|", " + "), "type": "midpoint", "x": x, "y": y}
		else:
			x, y = _point(by_key, kind, name)
			entry = {"object": name, "type": kind, "x": x, "y": y}
		if note:
			entry["projection" if kind != "Light" else "note"] = note
		entries.append(entry)
	return entries


def _gi(extracted: Path, by_key: dict) -> list[dict]:
	collections = {item["name"]: item["items"] for item in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))}
	lights = sorted((name for name in collections["GI"] if ("Light", name) in by_key), key=str.casefold)
	groups: list[dict] = []
	for name in lights:
		x, y = _point(by_key, "Light", name)
		for group in groups:
			if math.dist((group["x"], group["y"]), (x, y)) < STACK_DISTANCE:
				group["collapsed"].append(name)
				break
		else:
			groups.append({"object": name, "collapsed": [name], "x": x, "y": y})
	return groups


def build(extracted: Path, vpx: Path) -> dict:
	by_key = _candidates(extracted, vpx)
	return {
		"format": "pinmame-south-park-spatial-seed",
		"version": 1,
		"machine_id": "sega.south-park.1999",
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
			raise SystemExit(f"South Park spatial seed drift: {SEED_PATH}")
		print("South Park spatial seed matches the retained extraction.")
		return
	SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"Wrote {SEED_PATH}")


if __name__ == "__main__":
	main()
