"""Derive the pinned Jurassic Park geometry table from the retained vpxtool extraction.

Reads the retained Dark & Friends 1.03 extraction (never a different table), takes the exact object
each placement names through the embedded script's own bindings, and writes
tools/jurassic_park_geometry.json: file, SHA-256, object type, method, raw and normalized position.
Normalization is x = raw_x / right and y = raw_y / bottom of the table bounds (x = 0 left, y = 0 rear).

    python tools/build_jurassic_park_geometry.py <extraction-dir>          # rewrite the JSON
    python tools/build_jurassic_park_geometry.py <extraction-dir> --check  # refuse drift
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "jurassic_park_geometry.json"
TABLE_SHA256 = "dcd0e2e88abe9bf9956e2dba57bd8abd7891a668d49666c22ea0fd2b6e740ba9"
SCRIPT_SHA256 = "8d5045162f3ad7011e924b424a12123ffc0fcee49c598a8d6b649cd993e21b8b"

# Switch address -> the object the embedded script's Hit/Slingshot/Controller.Switch code binds.
SWITCH_OBJECTS = {
    16: ("Trigger", "swPLS"),
    **{n: ("Trigger", f"sw{n}") for n in (17, 18, 19, 20, 21, 22, 23, 24, 33, 34, 37, 59, 60)},
    **{n: ("HitTarget", f"sw{n}") for n in (25, 26, 27, 38, 39, 40, 48, 49, 50, 52, 53)},
    29: ("Kicker", "sw29"), 35: ("Kicker", "sw35"), 55: ("Kicker", "sw55"), 56: ("Kicker", "sw56"),
    61: ("Kicker", "VUK"),
    43: ("Wall", "LeftSlingShot"), 44: ("Wall", "RightSlingShot"),
    45: ("Bumper", "sw45"), 46: ("Bumper", "sw46"), 47: ("Bumper", "sw47"),
}
# Coil effect anchors (the mechanism object the coil acts on, never a winding centre).
COIL_OBJECTS = {
    1: ("Kicker", "sw56"), 2: ("Kicker", "BallRelease"), 3: ("Plunger", "Plunger1"),
    4: ("Kicker", "sw35"), 5: ("Kicker", "VUK"), 6: ("Wall", "Diverter_On"), 7: ("Kicker", "sw55"),
    9: ("Kicker", "sw29"), 17: ("Bumper", "sw45"), 18: ("Bumper", "sw46"), 19: ("Bumper", "sw47"),
    20: ("Wall", "LeftSlingShot"), 21: ("Wall", "RightSlingShot"),
}
# T-Rex mechanism objects: the toy pivot the script rotates, and the jaw.
MECHANISM_OBJECTS = {"trex-pivot": ("Primitive", "TrexPlastic"), "trex-jaw": ("Primitive", "TrexJaw"),
                     "drain": ("Kicker", "Drain")}
# Lamp address -> the script-driven Light objects that are the bulbs themselves (the final nFadeL /
# nFadeLm calls of UpdateLamps minus every glow, halo, reflection and shadow light named ...b, ...ab,
# ...b1). Lamps with no bulb object of their own (glow-only scoop and gate lights) are omitted.
LAMP_LIGHTS = {
    1: ("l1", "l1a"), 2: ("l2",), 3: ("l3",), 4: ("l4",), 5: ("l5",), 6: ("l6",), 7: ("l7",), 8: ("l8",),
    10: ("l10", "l10a"), 11: ("l11",), 12: ("l12",), 13: ("l13",), 14: ("l14",), 15: ("l15",),
    16: ("l16",), 19: ("l19", "l19a"), 20: ("l20",), 21: ("l21",), 22: ("l22",), 23: ("l23",),
    24: ("l24",), 25: ("L25",), 26: ("l26",), 27: ("l27",), 28: ("l28", "l28a"), 29: ("l29",),
    30: ("l30",), 31: ("l31",), 32: ("l32",), 35: ("l35",), 36: ("l36",), 37: ("l37",), 38: ("l38",),
    39: ("l39",), 40: ("l40",), 41: ("l41",), 42: ("l42",), 43: ("l43",), 44: ("l44",), 45: ("l45",),
    47: ("l47",), 48: ("l48",), 49: ("l49",), 50: ("l50",), 51: ("l51",), 52: ("l52",), 53: ("l53",),
    54: ("l54",), 55: ("L55", "L55a"), 56: ("l56",), 59: ("l59",), 60: ("l60",), 61: ("l61",),
    62: ("l62",), 63: ("l63",), 64: ("l64",),
}
# Flash-lamp bank (public solenoid 25-32) -> the PlayfieldLights or dome-bulb Light objects the script's
# FlashN routines drive, one per modelled bulb. The ...b / ...ab / ...bb twins, the large-falloff glows
# (l2r1, l2ra, l3rc, l4rc, l6rb) and the textured glows are not bulbs. Banks the table models with fewer
# bulbs than the factory fits stay partial; the other bulbs are backbox or insert bulbs the table omits.
FLASHER_LIGHTS = {
    25: ("l1r",), 26: ("l2rb",), 27: ("l3r", "l3ra", "l3rb", "l3rd"), 28: ("l4r", "l4ra", "l4rb"),
    29: ("l5r", "l5ra", "l5rb"), 30: ("l6ra",), 31: ("l7ra", "l7rb", "l7rc", "l7rd"), 32: ("l8r",),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def polygon_centroid(points: list[dict]) -> tuple[float, float]:
    """Signed shoelace area centroid of a wall's drag points."""
    area = cx = cy = 0.0
    for a, b in zip(points, points[1:] + points[:1]):
        cross = a["x"] * b["y"] - b["x"] * a["y"]
        area += cross
        cx += (a["x"] + b["x"]) * cross
        cy += (a["y"] + b["y"]) * cross
    if abs(area) < 1e-9:
        raise ValueError("degenerate polygon")
    return cx / (3 * area), cy / (3 * area)


def locate(kind: str, data: dict) -> tuple[str, tuple[float, float]]:
    if kind == "Wall":
        return "polygon_area_centroid", polygon_centroid(data["drag_points"])
    if kind in {"HitTarget", "Primitive"}:
        return "object_position", (data["position"]["x"], data["position"]["y"])
    return "object_center", (data["center"]["x"], data["center"]["y"])


def build(extraction: Path) -> dict:
    items = extraction / "gameitems"
    bounds_source = load(extraction / "gamedata.json")
    left, top = bounds_source["left"], bounds_source["top"]
    right, bottom = bounds_source["right"], bounds_source["bottom"]
    objects: dict[str, dict] = {}
    # The script names objects case-insensitively (VBScript); the extraction keeps the table's own case.
    actual = {path.name.lower(): path for path in items.iterdir()}

    def find(kind: str, name: str) -> Path:
        return actual[f"{kind}.{name}.json".lower()]

    def take(kind: str, name: str) -> None:
        if name in objects:
            return
        path = find(kind, name)
        data = load(path)[kind]
        method, (x, y) = locate(kind, data)
        objects[name] = {
            "file": f"gameitems/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "type": kind, "method": method, "raw_xy": [round(x, 5), round(y, 5)],
            "xy": [round((x - left) / (right - left), 6), round((y - top) / (bottom - top), 6)],
        }

    for table in (SWITCH_OBJECTS, COIL_OBJECTS, MECHANISM_OBJECTS):
        for kind, name in table.values():
            take(kind, name)
    for names in (*LAMP_LIGHTS.values(), *FLASHER_LIGHTS.values()):
        for name in names:
            take("Light", name)
    for name, light in ((n, objects[n]) for names in (*LAMP_LIGHTS.values(), *FLASHER_LIGHTS.values()) for n in names):
        data = load(find("Light", name))["Light"]
        light["light"] = {"falloff_radius": data["falloff_radius"], "image": data["image"],
                          "show_bulb_mesh": data["show_bulb_mesh"], "surface": data["surface"]}
    return {
        "bounds": [left, top, right, bottom],
        "table_sha256": TABLE_SHA256, "script_sha256": SCRIPT_SHA256,
        "switches": {str(n): name for n, (_, name) in sorted(SWITCH_OBJECTS.items())},
        "coils": {str(n): name for n, (_, name) in sorted(COIL_OBJECTS.items())},
        "mechanisms": {key: name for key, (_, name) in MECHANISM_OBJECTS.items()},
        "lamps": {str(n): list(names) for n, names in sorted(LAMP_LIGHTS.items())},
        "flashers": {str(n): list(names) for n, names in sorted(FLASHER_LIGHTS.items())},
        "objects": dict(sorted(objects.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extraction", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    script = args.extraction / "script.vbs"
    if hashlib.sha256(script.read_bytes()).hexdigest() != SCRIPT_SHA256:
        raise SystemExit("not the retained Dark & Friends 1.03 extraction")
    payload = (json.dumps(build(args.extraction), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    if args.check:
        if OUTPUT.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise SystemExit("geometry drift")
        print("geometry matches")
    else:
        OUTPUT.write_bytes(payload)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
