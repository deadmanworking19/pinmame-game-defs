#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Star Gazer (Stern 1980) curator.

The curator must reproduce byte for byte without the 240 MB table, so the objects it places are
frozen in ``tools/seeds/stern/star-gazer-1980-spatial.json``. This tool rebuilds that seed from a
retained vpxtool extraction with the repository's own normalizing helper and refuses to write when
the extraction's source hash differs from the pinned table.

    python tools/star_gazer_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> [--check]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.spatial import extract_spatial_candidates  # noqa: E402

SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "star-gazer-1980-spatial.json"
TABLE_SHA256 = "b15a49d6902164ae27b946b2f67d1c5682f92bd382288f2c94e2641045128085"

# (VPX type, object name) the curator places, in the order they are frozen.
SWITCH_OBJECTS = {
	4: ("Spinner", "sw4"), 5: ("Spinner", "sw5"), 9: ("Spinner", "sw9"),
	10: ("HitTarget", "sw10"), 11: ("HitTarget", "sw11"), 17: ("HitTarget", "sw17"), 18: ("HitTarget", "sw18"),
	19: ("HitTarget", "sw19"), 20: ("HitTarget", "sw20"), 21: ("HitTarget", "sw21"),
	31: ("HitTarget", "sw31"), 32: ("HitTarget", "sw32"), 38: ("HitTarget", "sw38"), 39: ("HitTarget", "sw39"), 40: ("HitTarget", "sw40"),
	12: ("Bumper", "Bumper1"), 13: ("Bumper", "Bumper2"), 14: ("Bumper", "Bumper3"),
	15: ("Wall", "RightSlingshot"), 16: ("Wall", "LeftSlingshot"),
	22: ("Wall", "sw22"), 23: ("Wall", "sw23"), 24: ("Wall", "sw24"),
	25: ("Wall", "sw25"), 26: ("Wall", "sw26"), 27: ("Wall", "sw27"),
	28: ("Wall", "sw28"), 29: ("Wall", "sw29"), 30: ("Wall", "sw30"),
	33: ("Kicker", "Drain"),
	34: ("Trigger", "sw34"), 35: ("Trigger", "sw35"), 36: ("Trigger", "sw36"), 37: ("Trigger", "sw37"),
}
EXTRA_OBJECTS = {
	"LeftFlipper": ("Flipper", "LeftFlipper"), "RightFlipper": ("Flipper", "RightFlipper"),
	"BallRelease": ("Kicker", "BallRelease"),
}
LIGHT_NAMES = [f"l{n}" for n in range(1, 64)] + ["l90", "l250", "l410", "l570"]


def wanted() -> dict[str, tuple[str, str]]:
	items: dict[str, tuple[str, str]] = {}
	for kind, name in list(SWITCH_OBJECTS.values()) + list(EXTRA_OBJECTS.values()):
		items[name] = (kind, name)
	for name in LIGHT_NAMES:
		items[name] = ("Light", name)
	return items


def build(extracted: Path, vpx: Path) -> dict:
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned Star Gazer v2.0.0 table")
	by_key = {(o["type"], o["name"]): o for o in candidates["objects"]}
	objects = {}
	for name, key in sorted(wanted().items()):
		found = by_key.get(key)
		if found is None:
			if re.fullmatch(r"l\d+", name):
				continue  # lamps the table does not model are simply absent
			raise SystemExit(f"missing table object {key}")
		objects[name] = {"type": found["type"], "x": found["x"], "y": found["y"]}
	return {
		"format": "pinmame-star-gazer-spatial-seed",
		"version": 1,
		"table_sha256": TABLE_SHA256,
		"bounds": candidates["bounds"],
		"objects": objects,
	}


def canonical(value: dict) -> str:
	return json.dumps(value, indent=1, sort_keys=True) + "\n"


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--extracted", type=Path, required=True)
	parser.add_argument("--vpx", type=Path, required=True)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = canonical(build(args.extracted, args.vpx))
	if args.check:
		if SEED_PATH.read_bytes().decode("utf-8") != text:
			print("seed drift", file=sys.stderr)
			return 1
		print("seed matches")
		return 0
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"wrote {SEED_PATH.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
