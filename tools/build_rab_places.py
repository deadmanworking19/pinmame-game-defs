#!/usr/bin/env python3
"""Resolve normalized playfield coordinates for The Adventures of Rocky and Bullwinkle and Friends (Data East 1993).

Reads the retained cyberpez 1.0 extraction (``gamedata.json`` bounds, ``gameitems/*.json`` and ``script.vbs``)
and writes ``tools/rab_places.json`` in the ``pinmame-vpx-placement-resolution`` format used by the other
Data East records. Every table object is chosen by what ``script.vbs`` binds to the ROM switch, lamp or coil,
or, where the script's binding disagrees with the manual's location drawings and the ROM's own switch-to-coil
pairing, by those (the two turbo bumpers below). The choice, the reason and the script patterns that prove
the binding are hard-coded here, and the builder fails closed when a named object is missing, ambiguous,
outside the table, of the wrong type, hidden, or when a binding pattern no longer matches the script.

A lamp or flash-lamp placement needs a real bulb (docs/SPATIAL.md, picking the bulb): a Light counts only when
both ``is_bulb_light`` and ``show_bulb_mesh`` are set, and a bulb the table models as primitives counts when the
script fades those primitives with the same lamp. Bulb-mode Lights that draw no bulb, insert overlays, render
lights and Flasher sprites never make a socket; the builder refuses to place one and lists each as rejected.

Coordinate convention: x = 0 is the left side and x = 1 the right side, y = 0 is the rear/backglass end and
y = 1 the front/apron end. ``x = raw_x / 952`` and ``y = raw_y / 2162``, rounded to six decimals.

Origins:

``measured-center``
    the object's stored centre (Light, Kicker, Trigger, Bumper, Gate) or position (HitTarget).
``computed-centroid``
    the mean of a Wall's drag points (the slingshots).
``mesh-bounds-center``
    the centre of the x/y bounding box of a primitive's world-space mesh. The meshes are exported with
    ``vpxtool export obj --units vpu``; the bounds are embedded in ``MESH_BOUNDS`` below so the builder needs
    no external file. ``--world-obj`` re-derives them from the retained export and fails on a mismatch.

Usage::

    python tools/build_rab_places.py --extracted <extracted dir> --output tools/rab_places.json
    python tools/build_rab_places.py --extracted <extracted dir> --output tools/rab_places.json --check
    python tools/build_rab_places.py --extracted <extracted dir> --output tools/rab_places.json --check --world-obj <export .obj>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

WIDTH = 952.0
HEIGHT = 2162.0

SCRIPT_SHA256 = "09f43d857b0a97eb2c6c1384db91e5f2aee6ab55541fcdb64292a77f8b4eb464"
VPX_SHA256 = "eb8806c40a3b1102ef7ee4d706dfb322dcc39b5909ae23b0132a7888f7971fa2"

WORLD_OBJ_NAME = "The Adventures of Rocky and Bullwinkle and Fiends (Data East 1993) 1.0.obj"
WORLD_OBJ_SHA256 = "561cf123e5c23d1a45c03ba2613586ca9fd52b17f9b1d8979c04a236f7055466"
WORLD_OBJ_RELATIVE = "adventures-of-rocky-and-bullwinkle-and-friends-1993/world-obj/" + WORLD_OBJ_NAME

SOURCE = (
    "cyberpez 1.0 extraction (gamedata.json bounds, gameitems, script.vbs sha256 " + SCRIPT_SHA256
    + ") of the retained VPX (sha256 " + VPX_SHA256 + "), objects chosen from script.vbs bindings and reconciled with the manual's location drawings; "
    "primitive mesh bounds from the vpxtool git:v0.33.3 'export obj --units vpu' world-space export (sha256 " + WORLD_OBJ_SHA256 + ")"
)

ORIGIN = {"center": "measured-center", "centroid": "computed-centroid", "mesh": "mesh-bounds-center"}

# x/y bounding boxes (xmin, ymin, xmax, ymax) of world-space meshes in the table's saved pose, rounded to four
# decimals. The OBJ export maps world x/y to OBJ x/y and negates the height. pSawBlade's stored position lies 2.6
# units left of its mesh; the two diverters' stored positions are their pivots, at one corner of the flap.
# pRampDiverter's mesh reaches 418 units in height, so only its x/y footprint is used. Each pBulb set is one
# upright modelled bulb: base, filament and glass share one centre, and its stored position equals that centre.
MESH_BOUNDS = {
    "pBulbBase1": (678.3595, 611.1428, 696.8160, 629.5993),
    "pBulbBase2": (693.1519, 547.5540, 711.6083, 566.0105),
    "pBulbBase3": (198.4335, 177.5874, 216.8900, 196.0439),
    "pBulbFilament1": (682.3152, 619.3946, 692.8602, 621.3474),
    "pBulbFilament2": (697.1076, 555.8058, 707.6525, 557.7585),
    "pBulbFilament3": (202.3893, 185.8392, 212.9343, 187.7920),
    "pBulbFlasher1": (668.9312, 601.5741, 706.4482, 639.0911),
    "pBulbFlasher2": (683.7235, 537.9853, 721.2405, 575.5023),
    "pBulbFlasher3": (189.0052, 168.0188, 226.5222, 205.5357),
    "pPFDiverter": (142.6677, 288.0139, 165.2086, 477.7709),
    "pRampDiverter": (147.0541, 504.4283, 241.3691, 631.2045),
    "pSawBlade": (865.0562, 827.8663, 867.9388, 923.9566),
}

# Flash-lamp groups whose bulb the table models as primitives the script fades with the group's lamp:
# public solenoid -> (SetLamp number, ((bulb set index, the bound Light that sits on that bulb), ...)).
BULB_FLASHERS = {
    27: (103, ((3, "f3b"),)),
    29: (105, ((1, "f5a"), (2, "f5b"))),
}
# Every Light the script fades with a flash-lamp group that draws no bulb and sits on no modelled bulb.
NON_BULB_FLASH_LIGHTS = {
    25: (101, ("f1a", "f1b")),
    27: (103, ("f3a",)),
    28: (104, ("f4a",)),
    29: (105, ("fl5a", "fl5a2", "fl5b", "fl5b2")),
    30: (106, ("f6a", "f6b")),
    32: (108, ("f8a",)),
}
# The G.I. collection the G.I. relay's fade drives, and the only members that draw their own bulb.
GI_COLLECTION = "TheGICollection"
GI_COLLECTION_SIZE = 84
GI_BULB_MESH_LIGHTS = ("gi5a", "gi6a")


class BuildError(RuntimeError):
    pass


class Choice:
    """One table object chosen for a key, with the reason and the script patterns proving the binding."""

    def __init__(self, obj, typ, why, bind, mode="center", doubles=(), bulb=None):
        self.obj = obj
        self.typ = typ
        self.why = why
        self.bind = list(bind)
        self.mode = mode
        self.doubles = list(doubles)
        self.bulb = bulb  # (bulb set index, the bound Light that sits on the bulb) for a modelled flash-lamp bulb


def solcb(n, name):
    return rf'SolCallback\({n}\)\s*=\s*"{name}"'


# --------------------------------------------------------------------------------------------------
# Switches (public switch number -> chosen table object)
# --------------------------------------------------------------------------------------------------

SWITCHES = {
    10: [Choice("Drain", "Kicker", "outhole: Drain_hit sets Controller.Switch(10) and Drain_UnHit clears it",
                [r"Sub Drain_hit\(\)", r"controller\.switch\(10\)\s*=\s*true", r"Controller\.Switch\(10\)\s*=\s*0"])],
    11: [Choice("kicker3", "Kicker", "trough #1 left: Kicker3_Hit/_UnHit set and clear Controller.Switch(11)",
                [r"Sub Kicker3_Hit\(\):Controller\.Switch\(11\)\s*=\s*1"])],
    12: [Choice("kicker2", "Kicker", "trough #2 center: Kicker2_Hit/_UnHit set and clear Controller.Switch(12)",
                [r"Sub Kicker2_Hit\(\):Controller\.Switch\(12\)\s*=\s*1"])],
    13: [Choice("kicker1", "Kicker", "trough #3 right, the release end: Kicker1_Hit/_UnHit set and clear Controller.Switch(13)",
                [r"Sub Kicker1_Hit\(\):Controller\.Switch\(13\)\s*=\s*1"])],
    14: [Choice("swPlunger", "Trigger", "shooter lane: the cvpmImpulseP plunger is initialised on swPlunger with .switch 14",
                [r"\.InitImpulseP swplunger", r"^\s*\.switch 14\b"])],
    29: [Choice("sw29", "Kicker", "super VUK: sw29_Hit sets Controller.Switch(29), and bsLEjet is InitSw 0,29 with InitKick Sw29",
                [r"Sub sw29_Hit\(\)", r"\.InitSw 0,29,", r"\.InitKick Sw29,"])],
    30: [Choice("LeftSlingShot", "Wall", "left slingshot: LeftSlingShot_Slingshot pulses switch 30",
                [r"Sub LeftSlingShot_Slingshot:.*vpmTimer\.PulseSw 30"], mode="centroid")],
    38: [Choice("RightSlingShot", "Wall", "right slingshot: RightSlingShot_Slingshot pulses switch 38",
                [r"Sub RightSlingShot_Slingshot:.*vpmTimer\.PulseSw 38"], mode="centroid")],
    52: [Choice("sw52", "Kicker", "playfield VUK under the hat trick: the ball-control loop sets Controller.Switch(52) when a ball rests in the pUpKicker square and enables sw52, which KickBallUp kicks",
                [r"Controller\.Switch\(52\)\s*=\s*1", r"sw52\.enabled = true", r"Sub sw52_Hit\(\)"])],
    44: [Choice("Bumper1", "Bumper", "left turbo bumper: Bumper1_hit pulses switch 44, and both manual location drawings put 44 and coil 17 on the left bumper",
                [r"Sub Bumper1_hit:vpmTimer\.PulseSw\(44\)"])],
    45: [Choice("Bumper3", "Bumper",
                "center turbo bumper: the switch-location drawing puts its lowest bumper callout (printed 47) and the coil-location drawing puts coil 18 "
                "(the ROM's CENTER POP) on the lower bumper, and the ROM fires 18 when 45 closes; the script pulses 46 from this bumper instead (a table defect)",
                [r"Sub Bumper3_hit:vpmTimer\.PulseSw\(46\)"])],
    46: [Choice("Bumper2", "Bumper",
                "right turbo bumper: both manual location drawings put 46 and coil 19 (the ROM's RIGHT POP) on the upper right bumper, and the ROM fires 19 when 46 "
                "closes; the script pulses 45 from this bumper instead (a table defect)",
                [r"Sub Bumper2_hit:vpmTimer\.PulseSw\(45\)"])],
}
for _n in range(17, 22):
    SWITCHES[_n] = [Choice(f"t{_n}", "HitTarget", f"drop target {_n - 16} of the five-bank: dtDrop is Initdrop Array(t17,...,t21), Array(17,...,21)",
                           [r"\.Initdrop Array\(t17,t18,t19,t20,t21\), Array\(17,18,19,20,21\)"])]
for _n, _where in ((22, "top"), (23, "middle"), (24, "bottom")):
    SWITCHES[_n] = [Choice(f"t{_n}", "HitTarget", f"hat target, the {_where} of the three in the table: t{_n}_Hit pulses switch {_n}",
                           [rf"Sub t{_n}_Hit:vpmTimer\.PulseSw\({_n}\)"])]
for _n in range(25, 29):
    SWITCHES[_n] = [Choice(f"t{_n}", "HitTarget", f"BOMB stand-up target: t{_n}_Hit pulses switch {_n}", [rf"Sub t{_n}_Hit:vpmTimer\.PulseSw\({_n}\)"])]
for _n, _what in (
    (31, "left return lane"), (32, "left outlane"), (33, "left orbit bottom"), (34, "left orbit top"), (35, "right orbit top"),
    (36, "right orbit bottom"), (37, "under-trough subway"), (39, "right return lane"), (40, "right outlane"), (41, "left top lane"),
    (42, "center top lane"), (43, "right top lane"), (47, "left ramp entrance"), (48, "left ramp exit"), (49, "right ramp entrance"),
    (50, "right ramp exit"),
):
    SWITCHES[_n] = [Choice(f"sw{_n}", "Trigger", f"{_what}: sw{_n}_Hit sets Controller.Switch({_n}) and its UnHit clears it",
                           [rf"Sub sw{_n}_Hit", rf"Controller\.Switch\({_n}\)\s*=\s*1"])]

# --------------------------------------------------------------------------------------------------
# Solenoids (public coil number -> chosen mechanism or flasher bulb)
# --------------------------------------------------------------------------------------------------

SOLENOIDS = {
    1: [Choice("Drain", "Kicker", "outhole: kisort kicks the Drain kicker", [solcb(1, "kisort"), r"Drain\.Kick 70,20"])],
    2: [Choice("kicker1", "Kicker", "trough eject: KickBallToLane kicks Kicker1, the release end of the trough", [solcb(2, "KickBallToLane"), r"Kicker1\.Kick 70,12"])],
    4: [Choice("sw52", "Kicker", "playfield VUK: KickBallUp kicks sw52", [solcb(4, "KickBallUp"), r"sw52\.Kick 0,50"])],
    5: [Choice("sw29", "Kicker", "super VUK: sw29kick kicks sw29", [solcb(5, "sw29kick"), r"sw29\.Kick 0,45"])],
    9: [Choice("pSawBlade", "Primitive", "saw motor relay: SolNell runs the RotateSaw and MoveNell timers, spinning pSawBlade and sliding the log (mesh bounds centre)",
               [r'SolCallBack\(9\)\s*=\s*"SolNell"', r"RotateSaw\.Enabled = 1", r"pSawBlade\.RotY = pSawBlade\.RotY \+ 5"], mode="mesh")],
    12: [Choice("pRampDiverter", "Primitive", "ramp diverter: SolDiverter2 swings pRampDiverter and swaps Diverter2a/Diverter2b (mesh bounds centre; the stored position is the pivot)",
                [r'solcallback\(12\)\s*=\s*"SolDiverter2"', r"pRampDiverter\.ObjRotZ"], mode="mesh")],
    13: [Choice("pPFDiverter", "Primitive", "playfield diverter: SolDiverter1 swings pPFDiverter and swaps Diverter1a/Diverter1b (mesh bounds centre; the stored position is the pivot)",
                [r'solcallback\(13\)\s*=\s*"SolDiverter1"', r"pPFDiverter\.ObjRotZ"], mode="mesh")],
    14: [Choice("Gate2", "Gate", "top control gate: TopGate makes Gate2 non-collidable while the solenoid is on",
                [r'solCallback\(14\)\s*=\s*"TopGate"', r"Gate2\.Collidable = false"])],
    15: [Choice("t19", "HitTarget", "drop target reset: DropsUp raises all five targets of the bank; the placement is the bank's middle target t19, where DropsUp plays its sound",
                [r'solCallback\(15\)\s*=\s*"DropsUp"', r'PlaySoundAt SoundFX\("DropsUp",DOFTargets\),t19'])],
    16: [Choice("swPlunger", "Trigger", "ball launcher: SolAutoPlungerIM fires the cvpmImpulseP plunger initialised on swPlunger",
                [r'SolCallBack\(16\)\s*=\s*"SolAutoPlungerIM"', r"PlungerIM\.AutoFire", r"\.InitImpulseP swplunger"])],
    17: [Choice("Bumper1", "Bumper", "left pop: the coil-location drawing puts 17 on the left bumper; the script leaves SolCallback(17) commented out and lets the VPX bumper kick",
                [r"'SolCallback\(17\)", r"Sub Bumper1_hit"])],
    18: [Choice("Bumper3", "Bumper", "center pop: the coil-location drawing puts 18 on the lower bumper; the script leaves SolCallback(18) commented out",
                [r"'SolCallback\(18\)", r"Sub Bumper3_hit"])],
    19: [Choice("Bumper2", "Bumper", "right pop: the coil-location drawing puts 19 on the upper right bumper; the script leaves SolCallback(19) commented out",
                [r"'SolCallback\(19\)", r"Sub Bumper2_hit"])],
    20: [Choice("LeftSlingShot", "Wall", "left slingshot: the script binds no callback to 20 and lets the VPX slingshot kick",
                [r"Sub LeftSlingShot_Slingshot"], mode="centroid")],
    21: [Choice("RightSlingShot", "Wall", "right slingshot: the script binds no callback to 21 and lets the VPX slingshot kick",
                [r"Sub RightSlingShot_Slingshot"], mode="centroid")],
    22: [Choice("LaserKick", "Kicker", "laser kick: AutoPlungeLK enables the LaserKick kicker at the left outlane while the solenoid is on, and LaserKick_Hit kicks the ball back out",
                [r'SolCallBack\(22\)\s*=\s*"AutoPlungeLK"', r"LaserKick\.Enabled=True", r"Sub LaserKick_Hit:Me\.Kick 0,45"])],
}


def _bulb_choice(n, lamp, index, light):
    base = f"pBulbBase{index}"
    patterns = [
        rf"Solcallback\({n}\)\s*=\s*\"SetLamp {lamp},\"",
        rf"FadePri4m {lamp}, pBulbFilament{index}\b",
        rf"FadeMaterialP {lamp}, pBulbFlasher{index}\b",
        rf"NFadeLm? {lamp}, {light}\b",
    ]
    return Choice(
        base, "Primitive",
        f"flash-lamp bulb: the script fades the modelled bulb pBulbFilament{index}/pBulbFlasher{index} on {base} with SetLamp {lamp}, which "
        f"SolCallback({n}) drives; the bound Light {light} sits inside the bulb's glass and draws no bulb of its own (mesh bounds centre of the base)",
        patterns, mode="mesh", bulb=(index, light),
    )


for _n, (_lamp, _bulbs) in BULB_FLASHERS.items():
    SOLENOIDS[_n] = [_bulb_choice(_n, _lamp, _index, _light) for _index, _light in _bulbs]

# --------------------------------------------------------------------------------------------------
# Unplaced keys and the script-bound objects that are not placements
# --------------------------------------------------------------------------------------------------

SPIN_LAMPS = tuple(range(1, 15))
CABINET_LAMPS = (15, 48)
PRIMITIVE_BULB_LAMPS = {16: ("pRbulb", "flasher16b"), 53: ("pWBbulb", "flasher16a")}
INSERT_LAMPS = tuple(n for n in range(17, 65) if n not in (48, 53))

UNPLACED = {
    "solenoid.8": "knocker: the script only plays a sound on it (vpmSolSound Knocker) and the table models no knocker; the coil location drawing carries no 8L balloon",
    "solenoid.11": (
        f"general illumination: the G.I. relay's fade drives the {GI_COLLECTION_SIZE} bulb-mode Lights of {GI_COLLECTION}, of which only gi5a and gi6a "
        "draw a bulb; no retained page counts or locates the G.I. sockets, so two bulbs of an uncounted string are not placed as a survey"
    ),
    "solenoid.25": "flash lamps 1R: the script fades only the bulb-mode Lights f1a and f1b (show_bulb_mesh false, on no modelled bulb) and the insert overlay l1a",
    "solenoid.26": "flash lamps 2R (hat trick): the script binds only the insert-overlay Lights l2a-l2d (is_bulb_light false) to 102, no bulb",
    "solenoid.28": "flash lamps 4R: the script fades only the bulb-mode Light f4a (show_bulb_mesh false, on no modelled bulb) and the insert overlay l4a",
    "solenoid.30": "flash lamps 6R: the script fades only the bulb-mode Lights f6a and f6b (show_bulb_mesh false, on no modelled bulb), the insert overlays l6a and l6b and the sprite f6c",
    "solenoid.31": "flash lamps 7R: the script binds only the insert-overlay Lights l7a-l7c (is_bulb_light false) to 107, no bulb",
    "solenoid.32": "flash lamps 8R: the script fades only the bulb-mode Light f8a (show_bulb_mesh false, on no modelled bulb) and the insert overlay l8a",
}
for _n in SPIN_LAMPS:
    UNPLACED[f"lamp.{_n}"] = f"spin-and-win pie lamp: the script binds only the primitive s2wB{_n} and the Flasher sprite s2wF{_n}; no bulb is bound to the lamp"
for _n in CABINET_LAMPS:
    UNPLACED[f"lamp.{_n}"] = "cabinet button lamp: not on the playfield, and the script binds nothing to it"
for _n, (_prim, _sprite) in PRIMITIVE_BULB_LAMPS.items():
    UNPLACED[f"lamp.{_n}"] = (
        f"ramp entrance lamp: the script fades the raised bulb primitive {_prim} and the Flasher sprite {_sprite}, but it binds lamp 16 to the bulb at the "
        "right ramp entrance and 53 to the one at the left, crossed against the manual's chart, the lamp drawing's left-ramp callout 16 and the ROM's names "
        "(16 LEFT RAMP ENTRANCE, 53 RIGHT RAMP ENTRANCE); the drawing prints no 53, so neither bulb is placed until a drawing check settles which is which"
    )
for _n in INSERT_LAMPS:
    UNPLACED[f"lamp.{_n}"] = "insert lamp: the script binds only an insert-overlay Light (is_bulb_light false), which is never a socket"

# Keys whose placement must be a bulb: the flash-lamp groups and the G.I.
FLASH_KEYS = {"solenoid.11", *(f"solenoid.{_n}" for _n in range(25, 33))}


class Table:
    def __init__(self, extracted: Path):
        gamedata = json.loads((extracted / "gamedata.json").read_text(encoding="utf-8"))
        bounds = (gamedata["left"], gamedata["top"], gamedata["right"], gamedata["bottom"])
        if bounds != (0.0, 0.0, WIDTH, HEIGHT):
            raise BuildError(f"gamedata.json bounds {bounds} are not (0, 0, {WIDTH}, {HEIGHT})")
        script_bytes = (extracted / "script.vbs").read_bytes()
        digest = hashlib.sha256(script_bytes).hexdigest()
        if digest != SCRIPT_SHA256:
            raise BuildError(f"script.vbs sha256 {digest} differs from the pinned {SCRIPT_SHA256}")
        # The script is Windows-1252 text (it carries a 0xB0 degree sign); Latin-1 keeps every byte and its line breaks.
        self.lines = script_bytes.decode("latin-1").replace("\r\n", "\n").split("\n")
        self.items = {}
        for path in sorted((extracted / "gameitems").glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            typ = next(iter(data))
            value = data[typ]
            # VBScript identifiers are case-insensitive, so the lookup is too; the stored name is kept.
            self.items.setdefault(value["name"].lower(), []).append((typ, value))
        self.collections = {
            entry["name"].lower(): list(entry["items"])
            for entry in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))
        }

    def get(self, name, typ):
        entries = self.items.get(name.lower())
        if not entries:
            raise BuildError(f"object {name!r} is not in the table")
        if len(entries) != 1:
            raise BuildError(f"object name {name!r} is ambiguous: {[t for t, _ in entries]}")
        got, value = entries[0]
        if got != typ:
            raise BuildError(f"object {name!r} is a {got}, expected {typ}")
        return value

    def find_lines(self, pattern):
        regex = re.compile(pattern, re.IGNORECASE)
        return [i + 1 for i, line in enumerate(self.lines) if regex.search(line)]


def stored_xy(typ, value):
    if typ in ("Light", "Kicker", "Trigger", "Bumper", "Gate"):
        return value["center"]["x"], value["center"]["y"]
    if typ in ("HitTarget", "Primitive"):
        return value["position"]["x"], value["position"]["y"]
    raise BuildError(f"no stored centre for object type {typ}")


def centroid_xy(value):
    points = value["drag_points"]
    return (round(sum(p["x"] for p in points) / len(points), 6), round(sum(p["y"] for p in points) / len(points), 6))


def mesh_centre(name):
    if name not in MESH_BOUNDS:
        raise BuildError(f"{name} has no embedded world-space mesh bounds")
    xmin, ymin, xmax, ymax = MESH_BOUNDS[name]
    return round((xmin + xmax) / 2, 4), round((ymin + ymax) / 2, 4)


def shows_bulb(value):
    """A Light makes a socket only when it is a bulb Light that also draws its bulb mesh."""
    return bool(value.get("is_bulb_light")) and bool(value.get("show_bulb_mesh"))


def inside(name, x, y):
    xmin, ymin, xmax, ymax = MESH_BOUNDS[name]
    return xmin <= x <= xmax and ymin <= y <= ymax


def check_bulb(table: Table, key: str, choice: Choice):
    """Fail closed unless the chosen base carries one upright modelled bulb with the bound Light inside its glass."""
    index, light = choice.bulb
    parts = (f"pBulbBase{index}", f"pBulbFilament{index}", f"pBulbFlasher{index}")
    centres = [mesh_centre(part) for part in parts]
    for part in parts:
        if not table.get(part, "Primitive").get("is_visible"):
            raise BuildError(f"{key}: bulb part {part} is hidden")
    if max(abs(a - b) for centre in centres for a, b in zip(centre, centres[0])) > 0.2:
        raise BuildError(f"{key}: bulb parts {parts} do not share one centre: {centres}")
    stored = table.get(parts[0], "Primitive")["position"]
    if abs(stored["x"] - centres[0][0]) > 0.2 or abs(stored["y"] - centres[0][1]) > 0.2:
        raise BuildError(f"{key}: {parts[0]}'s stored position is not its mesh centre, so the bulb is not upright")
    bound = table.get(light, "Light")
    if shows_bulb(bound):
        raise BuildError(f"{key}: {light} draws its own bulb; place the Light rather than the modelled bulb")
    if not bound.get("is_bulb_light") or not inside(parts[2], bound["center"]["x"], bound["center"]["y"]):
        raise BuildError(f"{key}: the bound Light {light} is not a bulb-mode Light inside the glass of {parts[2]}")


def resolve(table: Table, key: str, choice: Choice):
    value = table.get(choice.obj, choice.typ)
    if choice.typ == "Flasher":
        raise BuildError(f"{key}: {choice.obj} is a Flasher sprite, never a socket")
    if choice.typ == "Light" and not shows_bulb(value):
        raise BuildError(f"{key}: {choice.obj} draws no bulb (is_bulb_light and show_bulb_mesh must both be set)")
    if choice.typ == "Light" and value.get("is_backglass"):
        raise BuildError(f"{key}: {choice.obj} is a backglass light")
    if choice.typ == "Primitive" and not value.get("is_visible"):
        raise BuildError(f"{key}: {choice.obj} is a hidden primitive")
    if key.startswith("lamp.") and choice.typ != "Light":
        raise BuildError(f"{key}: a lamp is placed only on a Light that draws its bulb")
    if key in FLASH_KEYS and not (choice.typ == "Light" or choice.bulb):
        raise BuildError(f"{key}: a flash lamp is placed only on a bulb")
    if choice.bulb:
        check_bulb(table, key, choice)
    if choice.mode == "center":
        if choice.typ == "Primitive":
            raise BuildError(f"{key}: a primitive is placed at its world-space mesh centre, never its stored position")
        raw_x, raw_y = stored_xy(choice.typ, value)
    elif choice.mode == "centroid":
        raw_x, raw_y = centroid_xy(value)
    elif choice.mode == "mesh":
        raw_x, raw_y = mesh_centre(choice.obj)
    else:
        raise BuildError(f"{key}: unknown mode {choice.mode}")
    x, y = round(raw_x / WIDTH, 6), round(raw_y / HEIGHT, 6)
    if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
        raise BuildError(f"{key}: {choice.obj} is outside the playfield: raw ({raw_x}, {raw_y}) -> ({x}, {y})")
    for pattern in choice.bind:
        if not table.find_lines(pattern):
            raise BuildError(f"{key}: binding pattern {pattern!r} for {choice.obj} does not match script.vbs")
    for double in choice.doubles:
        other = table.get(double, "Light")
        if not shows_bulb(other):
            raise BuildError(f"{key}: collapsed double {double!r} draws no bulb")
        ox, oy = stored_xy("Light", other)
        if abs(ox - raw_x) > 2.0 or abs(oy - raw_y) > 2.0:
            raise BuildError(f"{key}: collapsed double {double!r} is not at {choice.obj}'s position")
    placement = {
        "coordinate_origin": ORIGIN[choice.mode],
        "object": value["name"],
        "object_type": choice.typ,
        "raw": {"x": raw_x, "y": raw_y},
        "x": x,
        "y": y,
    }
    if choice.doubles:
        placement["collapsed_from"] = sorted(set(choice.doubles))
    if choice.bulb:
        index, light = choice.bulb
        placement["bulb_parts"] = [f"pBulbBase{index}", f"pBulbFilament{index}", f"pBulbFlasher{index}"]
        placement["bound_light"] = table.get(light, "Light")["name"]
    return placement


def rejected_entries(table: Table):
    """Script-bound lamp objects that are not sockets, each verified against the script and the table."""
    out = []
    for n in INSERT_LAMPS:
        objs = ["l52a", "l52b"] if n == 52 else [f"l{n}"]
        for obj in objs:
            value = table.get(obj, "Light")
            if value.get("is_bulb_light"):
                raise BuildError(f"lamp.{n}: {obj} is a bulb Light; it should be placed, not rejected")
            if not table.find_lines(rf"NFadeLm? {n}, {obj}\b"):
                raise BuildError(f"lamp.{n}: {obj} is not bound to the lamp")
            out.append({"key": f"lamp.{n}", "object": value["name"], "reason": "insert-overlay Light (is_bulb_light false) bound by NFadeL(m); not a bulb socket"})
    for n in SPIN_LAMPS:
        table.get(f"s2wB{n}", "Primitive")
        table.get(f"s2wF{n}", "Flasher")
        if not table.find_lines(rf"FadePri4m {n}, s2wB{n}\b") or not table.find_lines(rf"Flashc {n}, s2wF{n}\b"):
            raise BuildError(f"lamp.{n}: s2wB{n}/s2wF{n} are not bound to the lamp")
        bulb = table.get(f"l{n}", "Light")
        if table.find_lines(rf"\b{n}, l{n}\b"):
            raise BuildError(f"lamp.{n}: l{n} is bound to the lamp after all")
        out.append({"key": f"lamp.{n}", "object": bulb["name"], "reason": f"bulb Light on the spin-and-win surface {bulb.get('surface')!r} that the script never binds to a lamp"})
    for n, (prim, sprite) in PRIMITIVE_BULB_LAMPS.items():
        table.get(prim, "Primitive")
        table.get(sprite, "Flasher")
        if not table.find_lines(rf"FadePri4m {n}, {prim}\b") or not table.find_lines(rf"Flashc {n}, {sprite}\b"):
            raise BuildError(f"lamp.{n}: {prim}/{sprite} are not bound to the lamp")
        out.append({
            "key": f"lamp.{n}", "object": table.get(prim, "Primitive")["name"],
            "reason": "raised bulb primitive faded by FadePri4m, but bound crossed against the manual's chart and the ROM's names (see unplaced); not placed",
        })
    bulb_glasses = [name for name in MESH_BOUNDS if name.startswith("pBulbFlasher")]
    for n, (lamp, objs) in NON_BULB_FLASH_LIGHTS.items():
        for obj in objs:
            value = table.get(obj, "Light")
            if not value.get("is_bulb_light") or shows_bulb(value) or not table.find_lines(rf"NFadeLm? {lamp}, {obj}\b"):
                raise BuildError(f"solenoid.{n}: {obj} must be a bound bulb-mode Light that draws no bulb")
            on = [glass for glass in bulb_glasses if inside(glass, value["center"]["x"], value["center"]["y"])]
            if on:
                raise BuildError(f"solenoid.{n}: {obj} sits on the modelled bulb {on}; place that bulb")
            out.append({
                "key": f"solenoid.{n}", "object": value["name"],
                "reason": f"bulb-mode Light bound to {lamp} that draws no bulb (show_bulb_mesh false) and sits on no modelled bulb; not a socket",
            })
    gi = table.collections.get(GI_COLLECTION.lower())
    if gi is None or len(gi) != GI_COLLECTION_SIZE:
        raise BuildError(f"{GI_COLLECTION} must hold {GI_COLLECTION_SIZE} items, not {None if gi is None else len(gi)}")
    if not table.find_lines(rf"UpdateGIobjectsSingle 200, {GI_COLLECTION}\b") or not table.find_lines(r"^SetLamp 200, 0"):
        raise BuildError(f"the G.I. relay's fade no longer drives {GI_COLLECTION}")
    gi_lights = [table.get(name, "Light") for name in gi]
    drawn = tuple(sorted(light["name"] for light in gi_lights if shows_bulb(light)))
    if drawn != GI_BULB_MESH_LIGHTS or not all(light.get("is_bulb_light") for light in gi_lights):
        raise BuildError(f"{GI_COLLECTION}: the Lights that draw a bulb are {drawn}, not {GI_BULB_MESH_LIGHTS}")
    for name in GI_BULB_MESH_LIGHTS:
        out.append({
            "key": "solenoid.11", "object": table.get(name, "Light")["name"],
            "reason": f"one of the only two of the {GI_COLLECTION_SIZE} {GI_COLLECTION} Lights that draw a bulb; the G.I. is left unplaced (see unplaced)",
        })
    for n, lamp, objs in ((26, 102, ("l2a", "l2b", "l2c", "l2d")), (31, 107, ("l7a", "l7b", "l7c"))):
        for obj in objs:
            value = table.get(obj, "Light")
            if value.get("is_bulb_light") or not table.find_lines(rf"NFadeLm? {lamp}, {obj}\b"):
                raise BuildError(f"solenoid.{n}: {obj} is a bulb or unbound")
            out.append({"key": f"solenoid.{n}", "object": value["name"], "reason": f"insert-overlay Light (is_bulb_light false) bound to {lamp}; not a bulb socket"})
    for n, lamp, obj in ((25, 101, "l1a"), (27, 103, "l3a"), (27, 103, "l3b"), (28, 104, "l4a"), (30, 106, "l6a"), (30, 106, "l6b"), (32, 108, "l8a")):
        value = table.get(obj, "Light")
        if value.get("is_bulb_light") or not table.find_lines(rf"NFadeLm? {lamp}, {obj}\b"):
            raise BuildError(f"solenoid.{n}: {obj} is a bulb or unbound")
        out.append({"key": f"solenoid.{n}", "object": value["name"], "reason": f"insert-overlay Light (is_bulb_light false) bound to {lamp}; not a bulb socket"})
    for n, sprites in ((29, ("f5c1", "f5c2", "f5d1", "f5d2")), (30, ("f6c",))):
        for obj in sprites:
            table.get(obj, "Flasher")
            out.append({"key": f"solenoid.{n}", "object": obj, "reason": "Flasher sprite bound to the flash lamp; never a socket"})
    return sorted(out, key=lambda e: (e["key"], e["object"]))


def build(table: Table):
    if not table.find_lines(r'SolCallback\(8\)\s*=\s*"vpmSolSound ""Knocker"",'):
        raise BuildError("solenoid.8: the script no longer only sounds the knocker")
    placements = {}
    for prefix, group in (("switch", SWITCHES), ("solenoid", SOLENOIDS)):
        for number in sorted(group):
            key = f"{prefix}.{number}"
            placements[key] = sorted((resolve(table, key, choice) for choice in group[number]), key=lambda p: p["object"])
    overlap = set(placements) & set(UNPLACED)
    if overlap:
        raise BuildError(f"keys both placed and unplaced: {sorted(overlap)}")
    return {
        "format": "pinmame-vpx-placement-resolution",
        "placements": placements,
        "rejected": rejected_entries(table),
        "source": SOURCE,
        "table_bounds": {"height": HEIGHT, "width": WIDTH},
        "unplaced": [{"key": key, "reason": reason} for key, reason in sorted(UNPLACED.items())],
        "version": 1,
    }


def render(document) -> bytes:
    return (json.dumps(document, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def derive_mesh_bounds(obj_path: Path) -> dict:
    """Recompute MESH_BOUNDS from the retained world-space OBJ export, refusing any other export."""
    digest = hashlib.sha256()
    with obj_path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    if digest.hexdigest() != WORLD_OBJ_SHA256:
        raise BuildError(f"{obj_path} sha256 {digest.hexdigest()} is not the pinned world-space export {WORLD_OBJ_SHA256}")
    bounds: dict[str, list[float]] = {}
    current = None
    with obj_path.open("rb") as stream:
        for line in stream:
            if line.startswith(b"o "):
                current = line[2:].strip().decode("utf-8")
            elif line.startswith(b"v ") and current in MESH_BOUNDS:
                x, y = (float(value) for value in line.split()[1:3])
                box = bounds.setdefault(current, [x, y, x, y])
                box[0], box[1], box[2], box[3] = min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y)
    return {name: tuple(round(value, 4) for value in box) for name, box in sorted(bounds.items())}


def check_mesh_bounds(obj_path: Path) -> None:
    derived = derive_mesh_bounds(obj_path)
    if derived != dict(sorted(MESH_BOUNDS.items())):
        raise BuildError(f"embedded MESH_BOUNDS differ from the world-space export: {derived}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--extracted", required=True, type=Path, help="retained vpxtool extraction directory")
    parser.add_argument("--output", required=True, type=Path, help="rab_places.json to write (or compare with --check)")
    parser.add_argument("--check", action="store_true", help="compare --output with the generated bytes")
    parser.add_argument("--world-obj", type=Path, help="retained 'vpxtool export obj --units vpu' export; re-derives MESH_BOUNDS and fails on a mismatch")
    args = parser.parse_args(argv)
    try:
        if args.world_obj:
            check_mesh_bounds(args.world_obj)
            print(f"MESH_BOUNDS match {args.world_obj}")
        data = render(build(Table(args.extracted)))
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.check:
        current = args.output.read_bytes().replace(b"\r\n", b"\n") if args.output.is_file() else None
        if current != data:
            print(f"DRIFT: {args.output} differs from the regenerated placements", file=sys.stderr)
            return 1
        print(f"{args.output} is up to date")
        return 0
    args.output.write_bytes(data)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
