#!/usr/bin/env python3
"""Freeze the Paragon table objects the curator places devices on.

Reads the retained ``vpxtool`` extraction of ``Paragon (Bally 1979).vpx`` and writes
``tools/seeds/bally/paragon-1979-spatial.json``: the playfield bounds and, for every object the
definition uses, its raw centre and normalized coordinate. ``--check`` refuses drift.

    python tools/paragon_spatial_seed.py --extracted <vpx-sources/bally/paragon-1979/extracted-vpxtool> --vpx <...vpx> [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "seeds" / "bally" / "paragon-1979-spatial.json"
WALLS = {"sw1", "sw2", "sw3", "sw4", "sw17", "sw18", "sw19", "LeftSlingShot", "RightSlingShot"}
# Collidable primitives whose geometry is baked into the mesh, with one label per connected piece,
# ordered from the front (largest y) of the playfield.
BAKED = {"sw27a": ("lower", "upper"), "sw34b": ("rebound",)}


def item(gameitems: Path, file: str) -> dict:
	return next(iter(json.loads((gameitems / file).read_text(encoding="utf-8")).values()))


def keep(vtype: str, name: str) -> bool:
	return (
		(vtype == "Light" and ((name.startswith("L") and name[1:].isdigit()) or name == "GIxx"))
		or (vtype == "Wall" and name in WALLS)
		or vtype in {"Bumper", "Flipper", "Spinner", "HitTarget"}
		or (vtype == "Trigger" and name.lower().startswith("sw"))
		or (vtype == "Kicker" and name in {"Drain", "BallRelease"})
	)


def baked_pieces(gameitems: Path, name: str) -> list[tuple[float, float]]:
	meta = item(gameitems, f"Primitive.{name}.json")
	if meta["position"] != {"x": 0.0, "y": -0.0, "z": 0.0} or any(meta["rot_and_tra"]) or len(set(meta["size"].values())) != 1:
		raise SystemExit(f"primitive {name} is no longer a baked mesh at the origin with uniform size")
	scale = meta["size"]["x"]
	vertices, faces = [], []
	for line in (gameitems / f"Primitive.{name}.obj").read_text(encoding="utf-8").splitlines():
		if line.startswith("v "):
			vertices.append([float(token) for token in line.split()[1:4]])
		elif line.startswith("f "):
			faces.append([int(token.split("/")[0]) - 1 for token in line.split()[1:]])
	parent = list(range(len(vertices)))

	def find(index: int) -> int:
		while parent[index] != index:
			index = parent[index]
		return index

	for face in faces:
		for other in face[1:]:
			parent[find(face[0])] = find(other)
	pieces = defaultdict(list)
	for index in range(len(vertices)):
		pieces[find(index)].append(index)
	centres = []
	for members in pieces.values():
		xs = [vertices[i][0] * scale for i in members]
		ys = [vertices[i][1] * scale for i in members]
		centres.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
	return sorted(centres, key=lambda point: -point[1])


def build(extracted: Path, vpx: Path) -> dict:
	gamedata = json.loads((extracted / "gamedata.json").read_text(encoding="utf-8"))
	left, top, right, bottom = gamedata["left"], gamedata["top"], gamedata["right"], gamedata["bottom"]
	gameitems = extracted / "gameitems"
	objects = {}

	def add(name: str, vtype: str, x: float, y: float, method: str, file: str) -> None:
		objects[name] = {
			"type": vtype, "file": f"gameitems/{file}", "method": method, "raw_x": round(x, 4), "raw_y": round(y, 4),
			"x": round((x - left) / (right - left), 6), "y": round((y - top) / (bottom - top), 6),
		}

	for file in sorted(path.name for path in gameitems.glob("*.json")):
		vtype, name = file.split(".", 1)[0], file.split(".", 1)[1][:-5]
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
	for name, labels in BAKED.items():
		pieces = baked_pieces(gameitems, name)
		if len(pieces) != len(labels):
			raise SystemExit(f"primitive {name} has {len(pieces)} mesh pieces, expected {len(labels)}")
		for label, (x, y) in zip(labels, pieces):
			add(f"{name}#{label}", "Primitive", x, y, "mesh_component_bbox_centre", f"Primitive.{name}.obj")
	return {
		"bounds": {"left": left, "top": top, "right": right, "bottom": bottom},
		"extraction_manifest_sha256": (extracted / "manifest.sha256").read_text(encoding="utf-8").split()[0],
		"objects": dict(sorted(objects.items(), key=lambda pair: pair[0].lower())),
		"table_sha256": hashlib.sha256(vpx.read_bytes()).hexdigest(),
		"transformation": (
			f"x = raw_x / {right}, y = raw_y / {bottom}, rounded to six places. Wall objects use the mean of their drag points; Light, Trigger, Bumper, Flipper, Spinner and Kicker objects their stored centre; "
			"HitTarget objects their stored position; the collidable primitives sw27a and sw34b, whose geometry is baked into the mesh at position (0,0,0) with no rotation, the centre of each connected mesh piece's bounding box "
			"after scaling the extracted OBJ vertices by the primitive's size (185.274)."
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
	OUTPUT.write_bytes(text)
	print(f"wrote {OUTPUT.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
