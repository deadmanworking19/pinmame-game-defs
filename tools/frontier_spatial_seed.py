#!/usr/bin/env python3
"""Freeze the Frontier table objects the curator uses.

Reads the retained ``vpxtool`` extraction of ``Frontier (Bally 1980).vpx`` and writes
``tools/seeds/bally/frontier-1980-spatial.json``: the playfield bounds; for every object the
definition places a device on, its raw centre and normalized coordinate; every lamp light ``L<n>``
with its bulb flags; and every bulb-mesh primitive with the light nearest to it. The last two show
why no lamp is placed: no lamp light draws a bulb mesh and every bulb primitive sits on a G.I.
light. ``--check`` refuses drift.

    python tools/frontier_spatial_seed.py --extracted <vpx-sources/bally/frontier-1980/extracted-vpxtool> --vpx <...vpx> [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "seeds" / "bally" / "frontier-1980-spatial.json"
WALLS = {"sw1a1", "sw1a2", "sw1a3", "sw1a4", "LeftSlingShot", "RightSlingShot"}
TRIGGERS = {"sw2", "sw3", "sw4", "sw5", "sw13", "sw14", "sw15", "sw25"}
KICKERS = {"Drain", "sw12"}
GATES = {"Gate2"}
LAMP_LIGHT = re.compile(r"^L(\d+)$")
BULB_PRIMITIVE = re.compile(r"^Bulb(Fil|Top)\d*$")


def item(gameitems: Path, file: str) -> dict:
	return next(iter(json.loads((gameitems / file).read_text(encoding="utf-8")).values()))


def keep(vtype: str, name: str) -> bool:
	return (
		(vtype == "Wall" and name in WALLS)
		or (vtype == "Trigger" and name in TRIGGERS)
		or (vtype == "Kicker" and name in KICKERS)
		or (vtype == "Gate" and name in GATES)
		or vtype in {"Bumper", "Flipper", "Spinner", "HitTarget"}
	)


def build(extracted: Path, vpx: Path) -> dict:
	gamedata = json.loads((extracted / "gamedata.json").read_text(encoding="utf-8"))
	left, top, right, bottom = gamedata["left"], gamedata["top"], gamedata["right"], gamedata["bottom"]
	gameitems = extracted / "gameitems"
	objects, lamp_lights, lights, bulbs = {}, {}, {}, {}

	def norm(x: float, y: float) -> tuple[float, float]:
		return round((x - left) / (right - left), 6), round((y - top) / (bottom - top), 6)

	def add(name: str, vtype: str, x: float, y: float, method: str, file: str) -> None:
		nx, ny = norm(x, y)
		objects[name] = {"type": vtype, "file": f"gameitems/{file}", "method": method, "raw_x": round(x, 4), "raw_y": round(y, 4), "x": nx, "y": ny}

	for file in sorted(path.name for path in gameitems.glob("*.json")):
		vtype, name = file.split(".", 1)[0], file.split(".", 1)[1][:-5]
		if vtype == "Light":
			value = item(gameitems, file)
			lights[name] = (value["center"]["x"], value["center"]["y"])
			match = LAMP_LIGHT.match(name)
			if match:
				lamp_lights[name] = {
					"raw_x": round(value["center"]["x"], 4), "raw_y": round(value["center"]["y"], 4),
					"is_bulb_light": value["is_bulb_light"], "show_bulb_mesh": value["show_bulb_mesh"],
				}
			continue
		if vtype == "Primitive" and BULB_PRIMITIVE.match(name):
			value = item(gameitems, file)
			bulbs[name] = (value["position"]["x"], value["position"]["y"])
			continue
		if not keep(vtype, name):
			continue
		value = item(gameitems, file)
		if vtype == "Wall":
			points = value["drag_points"]
			add(name, vtype, sum(p["x"] for p in points) / len(points), sum(p["y"] for p in points) / len(points), "drag_point_centroid", file)
		elif "center" in value:
			add(name, vtype, value["center"]["x"], value["center"]["y"], "center", file)
		else:
			add(name, vtype, value["position"]["x"], value["position"]["y"], "position", file)
	bulb_meshes = {}
	for name, (x, y) in sorted(bulbs.items(), key=lambda pair: pair[0].lower()):
		nearest = min(lights, key=lambda light: (math.dist((x, y), lights[light]), light))
		bulb_meshes[name] = {"raw_x": round(x, 4), "raw_y": round(y, 4), "nearest_light": nearest, "distance": round(math.dist((x, y), lights[nearest]), 3)}
	return {
		"bounds": {"left": left, "top": top, "right": right, "bottom": bottom},
		"bulb_meshes": bulb_meshes,
		"extraction_manifest_sha256": (extracted / "manifest.sha256").read_text(encoding="utf-8").split()[0],
		"lamp_lights": dict(sorted(lamp_lights.items(), key=lambda pair: int(pair[0][1:]))),
		"objects": dict(sorted(objects.items(), key=lambda pair: pair[0].lower())),
		"table_sha256": hashlib.sha256(vpx.read_bytes()).hexdigest(),
		"transformation": (
			f"x = raw_x / {right}, y = raw_y / {bottom}, rounded to six places. Wall objects use the mean of their drag points; Trigger, Bumper, Flipper, Spinner, Gate and Kicker objects their stored centre; "
			"HitTarget objects their stored position. Lamp lights and bulb primitives are recorded raw: the lights with their is_bulb_light and show_bulb_mesh flags, the BulbFil/BulbTop primitives at their "
			"stored position with the nearest Light object by Euclidean distance in table units."
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
		if OUTPUT.read_bytes() != text:
			print("spatial seed drift", file=sys.stderr)
			return 1
		print("spatial seed matches the retained extraction")
		return 0
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	OUTPUT.write_bytes(text)
	print(f"wrote {OUTPUT.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
