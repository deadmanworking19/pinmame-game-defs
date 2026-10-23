"""Recompute Batman Forever's observed placements from its exact retained VPX extraction.

Only script-linked physical objects are selected. Flasher sprites, cabinet and VR primitives,
helper lights and primitive origins are excluded. Primitives use world-space OBJ mesh bounds from
vpxtool export obj --units vpu, walls the mean of their drag points; the export stays outside Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
TABLE_NAME = "Batman Forever (Sega 1995) 1.3.vpx"
TABLE_SHA = "e1eb059e75fba1b6fc61c40a01e98d466a33786644125f707a0f164c8dbb1792"
MANIFEST_SHA = "7f2237c7223597ed76b651ff3c6f93f809b3ab433cebc400017585b607ed4870"
SCRIPT_SHA = "305f1827f7877d664f16722b8e9a4863457493211751c5f6f8d4f515547c78d6"
WIDTH, HEIGHT = 1093, 2162

SWITCH_OBJECTS = {
    15: "BallRelease", 16: "Trigger16", 30: "BatCaveExitKicker", 32: "VUK_Bottom",
    35: "LeftSlingshot", 36: "RightSlingshot", 41: "TopEjectKicker", 44: "BWGun",
    **{n: f"sw{n}p" for n in range(18, 22)},
    **{n: f"sw{n}t" for n in (25, 26, 27, 28, 29, 42, 43, 50, 51)},
    **{n: f"Trigger{n}" for n in (22, 23, 24, 33, 34, 37, 38, 39, 40, 47, 48, 52, 53, 54, 55, 56)},
    **{n: f"Bumper{n}" for n in (57, 58, 59)},
}
COIL_OBJECTS = {
    2: ["BallRelease"], 3: ["Plunger"], 4: ["VUK_Bottom"], 5: ["TopEjectKicker"],
    9: ["BallLock"], 12: ["pDiverter"], 14: ["pBatwing"], 15: ["BWGun"], 16: ["BatCaveExitKicker"],
    17: ["Bumper57"], 18: ["Bumper58"], 19: ["Bumper59"],
    20: ["LeftSlingshot"], 21: ["RightSlingshot"], 22: ["LaserKick"],
    25: ["FLamp1R"], 26: ["FLamp2Ra", "FLamp2Rb"], 27: ["Flasher3R"], 28: ["Flasher4R", "Flasher4Ra"],
    29: ["Flasher5r"], 30: ["Flasher6r"], 31: ["Flasher7r"], 32: ["FLamp8R"],
}
# The four C-A-V-E target primitives; the single reset coil is projected onto their mean.
DROP_BANK = ["sw18p", "sw19p", "sw20p", "sw21p"]
LAMP_OBJECTS = {
    **{n: [f"Lamp{n}"] for n in (*range(1, 33), 35, *range(39, 59), 61, 62)},
    # The object in the right turbo bumper cap; the table gives it TimerInterval 58 (see the curator).
    59: ["Lamp59"],
}
# GIString2 members toggled by SolGI (output 11), less the three bumper lamps that are matrix lamps.
GI_OBJECTS = [f"Light{n:03d}" for n in range(4, 35)]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mesh_bounds(path: Path) -> dict:
    groups: dict[str, list[list[float]]] = {}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("o "):
            current = line[2:]
        elif current is not None and line.startswith("v "):
            groups.setdefault(current, []).append(list(map(float, line.split()[1:4])))
    return {name: {"minimum": [min(v[i] for v in vertices) for i in range(3)],
                   "maximum": [max(v[i] for v in vertices) for i in range(3)]}
            for name, vertices in groups.items()}


def build(vpx_root: Path, obj: Path) -> dict:
    base = vpx_root / "sega/batman-forever-1995"
    extraction = base / "extracted-vpxtool"
    if sha(base / TABLE_NAME) != TABLE_SHA:
        raise ValueError("Batman Forever retained VPX differs from the admitted source")
    if check_manifest(extraction, "batmanf") != MANIFEST_SHA or sha(extraction / "script.vbs") != SCRIPT_SHA:
        raise ValueError("Batman Forever extraction differs from the admitted source")
    objects = {}
    for path in (extraction / "gameitems").glob("*.json"):
        kind, data = next(iter(json.loads(path.read_text(encoding="utf-8")).items()))
        objects[data["name"]] = (kind, data, path)
    game = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
    if tuple(game[n] for n in ("left", "top", "right", "bottom")) != (0, 0, WIDTH, HEIGHT):
        raise ValueError("Batman Forever table bounds changed")
    bounds = mesh_bounds(obj)

    def raw(name):
        kind, data, path = objects[name]
        if kind == "Flasher" or data.get("is_backglass"):
            raise ValueError(f"not a physical playfield anchor: {name}")
        if kind == "Primitive":
            box = bounds[name]
            x, y = ((box["minimum"][i] + box["maximum"][i]) / 2 for i in range(2))
            method = "world-space OBJ mesh-bounds centre"
        elif kind == "Wall":
            points = data["drag_points"]
            x = sum(p["x"] for p in points) / len(points)
            y = sum(p["y"] for p in points) / len(points)
            method = "mean of the wall's drag points"
        else:
            centre = data.get("center") or data.get("position")
            if centre is None:
                raise ValueError(f"no exact centre for {name}")
            x, y = centre["x"], centre["y"]
            method = "stored physical object centre/pivot"
        if not (0 <= x <= WIDTH and 0 <= y <= HEIGHT):
            raise ValueError(f"out-of-bounds anchor: {name} ({x},{y})")
        return kind, path, x, y, method

    def point(name):
        kind, path, x, y, method = raw(name)
        return {"object": name, "type": kind, "path": path.relative_to(extraction).as_posix(),
                "sha256": sha(path), "raw_x": x, "raw_y": y, "method": method,
                "x": round(x / WIDTH, 6), "y": round(y / HEIGHT, 6),
                **({"world_mesh_bounds": bounds[name]} if kind == "Primitive" else {})}

    placements = {}
    for n, name in SWITCH_OBJECTS.items():
        placements[f"switch.{n}"] = [point(name)]
    for n, names in COIL_OBJECTS.items():
        placements[f"solenoid.{n}"] = [point(name) for name in names]
    bank = [point(name) for name in DROP_BANK]
    mx = sum(p["raw_x"] for p in bank) / len(bank)
    my = sum(p["raw_y"] for p in bank) / len(bank)
    placements["solenoid.7"] = [{"object": "+".join(DROP_BANK), "type": "projection",
                                 "method": "mean of the four drop-target primitive mesh-bounds centres",
                                 "raw_x": mx, "raw_y": my, "x": round(mx / WIDTH, 6), "y": round(my / HEIGHT, 6)}]
    for n, names in LAMP_OBJECTS.items():
        placements[f"lamp.{n}"] = [point(name) for name in names]
    placements["solenoid.11"] = [point(name) for name in GI_OBJECTS]
    # Mesh-export sanity checks against independently positioned bumper objects. This checks the
    # export's coordinate convention; it does not grant independent physical validation.
    controls = []
    for mesh, anchor in (("Bumper57Base", "Bumper57"), ("Bumper58Base", "Bumper58"), ("Bumper59Base", "Bumper59")):
        box = bounds[mesh]
        b = point(anchor)
        x, y = ((box["minimum"][i] + box["maximum"][i]) / 2 for i in range(2))
        if abs(x - b["raw_x"]) > 2 or abs(y - b["raw_y"]) > 2:
            raise ValueError(f"OBJ coordinate control failed: {mesh} / {anchor}")
        controls.append({"mesh": mesh, "anchor": anchor, "dx": round(x - b["raw_x"], 5), "dy": round(y - b["raw_y"], 5)})
    return {"table_bounds": {"left": 0, "top": 0, "right": WIDTH, "bottom": HEIGHT},
            "table_sha256": TABLE_SHA, "script_sha256": SCRIPT_SHA, "manifest_sha256": MANIFEST_SHA,
            "obj_sha256": sha(obj), "export_command": "vpxtool export obj --units vpu <retained VPX>",
            "tool": "vpxtool git:v0.33.3", "placements": placements, "mesh_controls": controls,
            "mechanical_anchors": {name: point(name) for name in ("LeftFlipper", "RightFlipper", "URightFlipper", "pBatwingGun")},
            "omitted": ("Trough switches 11-14, lock-out coil 1, Batcave lock switches 60-62, cannon safety 45 and "
                        "cannon home 46 have no table object: ball stacks and a cvpmMech stand in for them. Lamps "
                        "33 and 34 are omitted because both table objects bound to 33 sit at the left edge, away "
                        "from the ramp-mounted Spot-Lite pair. Flasher 1R models one of four sockets, 3R one of "
                        "four, 4R two of three playfield and back-panel sockets, 5R-7R only their back-panel "
                        "sockets and 8R one of three; no backbox insert socket is in this space."),
            "rejected": ["All VPX Flasher objects (glow sprites, never made visible by the script)",
                         "Lamp001-Lamp060 and FLamp4R/FLamp4R001 (unreferenced lights outside every collection)",
                         "Lamp33 and Lamp34 (both TimerInterval 33, at the left edge)",
                         "Lamp57-59 as G.I. (bumper matrix lamps that the script also lists in GIString1/2)",
                         "Cabinet, VR and sound primitives (PinCab_*, VR*, KnockerPosition, RelayPosition)",
                         "Primitive position fields"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vpx-root", type=Path, required=True)
    parser.add_argument("--world-obj", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(args.vpx_root, args.world_obj), indent=2, sort_keys=True) + "\n").encode()
    path = ROOT / "tools/batman_forever_places.json"
    if args.check:
        if path.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise ValueError("Batman Forever placements drifted")
    else:
        path.write_bytes(payload)


if __name__ == "__main__":
    main()
