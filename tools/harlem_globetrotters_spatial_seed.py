#!/usr/bin/env python3
"""Freeze the Harlem Globetrotters On Tour table objects the curator uses.

Reads the retained ``vpxtool`` extraction of ``Harlem Globetrotters On Tour (Bally 1979).vpx`` and
writes ``tools/seeds/bally/harlem-globetrotters-on-tour-1979-spatial.json``: the playfield bounds and,
for every object the definition places a device on or cites, its raw centre and normalized
coordinate. Light objects also keep the lamp number the script maps them to (their timer interval,
read by ``vpmMapLights``) and whether the table draws a bulb for them, because only a light with a
modelled bulb marks a lamp socket. ``--check`` refuses drift.

    python tools/harlem_globetrotters_spatial_seed.py --extracted <vpx-sources/bally/harlem-globetrotters-on-tour-1979/extracted-vpxtool> --vpx <...vpx> [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-spatial.json"
WALLS = {"LeftSlingshot", "RightSlingshot", "Sling1", "Sling2"}
KICKERS = {"Drain", "BallRelease", "sw24", "sw32"}


def item(gameitems: Path, file: str) -> dict:
	return next(iter(json.loads((gameitems / file).read_text(encoding="utf-8")).values()))


def keep(vtype: str, name: str) -> bool:
	return (
		(vtype == "Light" and not name.startswith("gi"))
		or (vtype == "Wall" and name in WALLS)
		or vtype in {"Bumper", "Flipper", "Spinner", "HitTarget"}
		or (vtype == "Trigger" and name.startswith("sw"))
		or (vtype == "Kicker" and name in KICKERS)
	)


def build(extracted: Path, vpx: Path) -> dict:
	gamedata = json.loads((extracted / "gamedata.json").read_text(encoding="utf-8"))
	left, top, right, bottom = gamedata["left"], gamedata["top"], gamedata["right"], gamedata["bottom"]
	gameitems = extracted / "gameitems"
	objects = {}
	for file in sorted(path.name for path in gameitems.glob("*.json")):
		vtype, name = file.split(".", 1)[0], file.split(".", 1)[1][:-5]
		if not keep(vtype, name):
			continue
		value = item(gameitems, file)
		if vtype == "Wall":
			points = value["drag_points"]
			x, y, method = sum(p["x"] for p in points) / len(points), sum(p["y"] for p in points) / len(points), "drag_point_centroid"
		elif "center" in value:
			x, y, method = value["center"]["x"], value["center"]["y"], "center"
		else:
			x, y, method = value["position"]["x"], value["position"]["y"], "position"
		entry = {
			"type": vtype, "file": f"gameitems/{file}", "method": method, "raw_x": round(x, 4), "raw_y": round(y, 4),
			"x": round((x - left) / (right - left), 6), "y": round((y - top) / (bottom - top), 6),
		}
		if vtype == "Light":
			entry["timer_interval"] = value["timer_interval"]
			entry["is_bulb_light"] = value["is_bulb_light"]
			entry["show_bulb_mesh"] = value["show_bulb_mesh"]
		if vtype == "Flipper" and not value.get("is_visible", True):
			entry["visible"] = False
		objects[name] = entry
	gi = sorted((path.name for path in gameitems.glob("Light.gi*.json")), key=lambda file: int(file[len("Light.gi"):-5]))
	return {
		"bounds": {"left": left, "top": top, "right": right, "bottom": bottom},
		"extraction_manifest_sha256": (extracted / "manifest.sha256").read_text(encoding="utf-8").split()[0],
		"gi_lights": {
			"count": len(gi),
			"timer_intervals": sorted({item(gameitems, file)["timer_interval"] for file in gi}),
			"bulb_lights": sum(1 for file in gi if item(gameitems, file)["is_bulb_light"]),
		},
		"objects": dict(sorted(objects.items(), key=lambda pair: pair[0].lower())),
		"table_sha256": hashlib.sha256(vpx.read_bytes()).hexdigest(),
		"transformation": (
			f"x = (raw_x - {left}) / ({right} - {left}), y = (raw_y - {top}) / ({bottom} - {top}), rounded to six places. Wall objects use the mean of their drag points; "
			"Light, Trigger, Bumper, Flipper, Spinner and Kicker objects their stored centre; HitTarget objects their stored position."
		),
	}


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--extracted", type=Path, required=True)
	parser.add_argument("--vpx", type=Path, required=True)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = (json.dumps(build(args.extracted, args.vpx), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
	if args.check:
		if not OUTPUT.exists() or OUTPUT.read_bytes() != text:
			print("spatial seed drift", file=sys.stderr)
			return 1
		print("spatial seed matches the retained extraction")
		return 0
	OUTPUT.write_bytes(text)
	print(f"wrote {OUTPUT.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
