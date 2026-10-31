"""Curate the physical Data East The Adventures of Rocky and Bullwinkle and Friends (1993) machine definition.

Side-effect free and deterministic. The printed tables are parsed from the hand-transcribed excerpts committed
under ``evidence/excerpts/data-east.adventures-of-rocky-and-bullwinkle-and-friends.1993/`` (``rab_manual``), the
semantic naming is in ``rab_semantics``, the normalized coordinates resolved from the retained recreation are in
``tools/rab_places.json`` (``tools/build_rab_places.py``), the ROM's own service-test and in-game readings are in
``tools/rab_runtime.json`` (``tools/build_rab_runtime_evidence.py``), and the ROM inventory is parsed from pinned
PinMAME and embedded below. ``--regenerate`` reproduces the canonical artifacts byte-for-byte without reading any
external evidence root; ``--check`` refuses drift. ``--write-extraction-manifest`` and ``--verify-extraction``
write and verify the canonical manifest of the retained vpxtool extraction under PINMAME_VPX_SOURCES_ROOT.

The definition, its pinned seed, the spatial report and the knowledge note are all generated here from the same
objects, so prose cannot outlive the data behind it.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes, write_json, write_text
from pinmame_flipper_column import (
    VPM_CORE_SHA256,
    VPM_DE_LIBRARY_SOURCE,
    VPM_DE_LIBRARY_URI,
    VPM_DE_SHA256,
    flipper_column_inputs,
    flipper_column_relationships,
    vpm_staged_flipper_notes,
)
import rab_manual
import rab_semantics as sem

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.adventures-of-rocky-and-bullwinkle-and-friends.1993"
SLUG = "adventures-of-rocky-and-bullwinkle-and-friends-1993"
DEFINITION_PATH = ROOT / f"machines/partial/data-east/{SLUG}.json"
AUTHOR_READY_PATH = ROOT / f"machines/author-ready/data-east/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/data-east/{SLUG}.json"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.md"
KNOWLEDGE_PATH = ROOT / f"knowledge/data-east/{SLUG}.md"
PLACES_PATH = ROOT / "tools/rab_places.json"
RUNTIME_PATH = ROOT / "tools/rab_runtime.json"
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/adventures-of-rocky-and-bullwinkle-and-friends-rab_320-service-tests.json"
KNOWLEDGE_TEMPLATE = ROOT / "tools/rab_knowledge.md"
EXCERPT_DIR = ROOT / "evidence/excerpts" / KEY

REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
SHORT = REVISION[:12]
MANUAL = f"manual.{KEY}"
IPDB = f"ipdb.{KEY}"
CATALOG = f"pinmame.catalog.{SHORT}"
CORE = f"pinmame.core.{SHORT}"
CORE_H = f"pinmame.core-h.{SHORT}"
CORE_C = f"pinmame.core-c.{SHORT}"
S11_C = f"pinmame.s11-c.{SHORT}"
S11_H = f"pinmame.s11-h.{SHORT}"
TABLE = "vpx-table.rocky-and-bullwinkle-cyberpez-1-0"
SCRIPT_REF = "vpx-script.rocky-and-bullwinkle-cyberpez-1-0"
EXTRACTION = "vpx-extraction.rocky-and-bullwinkle-cyberpez-1-0"
CORPUS_SAME_LINEAGE = "vpx-script.rocky-and-bullwinkle-cyberpez-1-06"
CORPUS_INDEPENDENT = "vpx-script.rocky-and-bullwinkle-zedonius-0-96"
RUNTIME_SRC = "runtime.adventures-of-rocky-and-bullwinkle-and-friends.rab-320-service-tests"

MANUAL_NAME = "Data_East_1993_Adventures_of_Rocky_and_Bullwinkle_and_Friends_Full_Manual.pdf"
MANUAL_SHA256 = "1f50634e743bccf6276e170dcb5da05c92e5c4769a4650147338fab59b36a381"
MANUAL_URL = f"https://web.archive.org/web/20210731210449id_/https://www.ipdb.org/files/23/{MANUAL_NAME}"
MANUAL_ACQUIRED = "2026-10-31T05:27:35Z"
IPDB_CAPTURE = "https://web.archive.org/web/20261016075449id_/https://www.ipdb.org/machine.cgi?id=23"
IPDB_SHA256 = "9717a2f15d8225895e4b6836907dde0c4df61a73ac0562eb627590545ae8ed09"
IPDB_ACQUIRED = "2026-10-31T05:26:54Z"
TABLE_NAME = "The Adventures of Rocky and Bullwinkle and Fiends (Data East 1993) 1.0.vpx"
TABLE_SHA256 = "eb8806c40a3b1102ef7ee4d706dfb322dcc39b5909ae23b0132a7888f7971fa2"
TABLE_ACQUIRED = "2026-10-31T05:29:25Z"
SCRIPT_SHA256 = "09f43d857b0a97eb2c6c1384db91e5f2aee6ab55541fcdb64292a77f8b4eb464"
EXTRACTION_ACQUIRED = "2026-10-31T05:29:20Z"
ROM_ARCHIVE_SHA256 = "efe4c395840d66c2b51b63f38686429d4889e9915f364f1f8471714800c2d788"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CORPUS_SAME_LINEAGE_NAME = "Adventures of Rocky and Bullwinkle and Friends (Data East 1993) v1.06.vbs"
CORPUS_SAME_LINEAGE_SHA256 = "6486cf41c8112d9a4dc32463781eabe0aedd4ee6b7ef0016e88364f35b36a7f7"
CORPUS_INDEPENDENT_NAME = "Rocky & Bullwinkle And Friends 1.0.vbs"
CORPUS_INDEPENDENT_SHA256 = "c61fcaf9d88b05bb85a9652ed324aed464bc851c5567ebd62dfe1aaaa0a88053"

SOURCE_DIRECTORY = "data-east/adventures-of-rocky-and-bullwinkle-and-friends-1993"
EXTRACTION_RELATIVE_PATH = Path(SOURCE_DIRECTORY) / "extracted-vpxtool"
EXTRACTION_MANIFEST_RELATIVE_PATH = Path(SOURCE_DIRECTORY) / "extracted-vpxtool.manifest.json"
EXTRACTION_MANIFEST_SHA256 = "d5df345d6ca4c736a12f0ac5a6c80845a842d16f7985e14a5c377bc525c831f7"
EXTRACTION_FILE_COUNT = 1374
EXTRACTION_TOTAL_BYTES = 131952476
VPXTOOL_VERSION = "vpxtool git:v0.33.3"
# The world-space export the placement builder's MESH_BOUNDS come from (tools/build_rab_places.py --world-obj).
WORLD_OBJ_SHA256 = "561cf123e5c23d1a45c03ba2613586ca9fd52b17f9b1d8979c04a236f7055466"
WORLD_OBJ_URI = (
    "external:pinmame-review-artifacts/adventures-of-rocky-and-bullwinkle-and-friends-1993/world-obj/"
    "The Adventures of Rocky and Bullwinkle and Fiends (Data East 1993) 1.0.obj"
)
PIN_FILE_SHA256 = {
    "degames.c": "223623584396cc530c8baef577772d4b96d39784aa2624f04746871c8f89f5d8",
    "core.h": "b6c03b20a09fbadff1ce16f9f1cfc9e5bace08857cb998b92d8f304695ec97c0",
    "core.c": "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00",
    "s11.c": "03784af9fe444b3da56f72192a5b04da1aa72938435f3d902d94ab47c0f8bd9e",
    "s11.h": "743b0836cc84e41e793d65786a964a595fb403c4fdba29b2961e8a36a937f614",
}

# The five PinMAME drivers, parsed from src/wpc/degames.c at the pinned revision (lines 926-972). Roles: CPU,
# display, then the three sound ROMs (U7, U17, U21). All five share rabGameData and every sound ROM.
ROLES = ("CPU", "display", "sound U7", "sound U17", "sound U21")
SOUND = ["rab.u7", "rab.u17", "rab.u21"]
ROM_SETS = {
    "rab_320": ["rabcpua.320", "rbdspa.300", *SOUND],
    "rab_130": ["rabcpua.130", "rbdspa.130", *SOUND],
    "rab_110be": ["Rocky-Bull_1.10_Belgium-C5.bin", "rbdspa.130", *SOUND],
    "rab_103it": ["rabcpu.103", "Rocky-Bull_1.03_Italian_Disp-rom0.bin", *SOUND],
    "rab_103": ["rabcpu.103", "rabdspsp.103", *SOUND],
}
ROOT_DRIVER = "rab_320"
DRIVER_LABELS = {
    "rab_320": "Adventures of Rocky and Bullwinkle and Friends, The (3.20)",
    "rab_130": "Adventures of Rocky and Bullwinkle and Friends, The (1.30)",
    "rab_110be": "Adventures of Rocky and Bullwinkle and Friends, The (1.10 Belgian, Display 1.30)",
    "rab_103it": "Adventures of Rocky and Bullwinkle and Friends, The (1.03 Italian)",
    "rab_103": "Adventures of Rocky and Bullwinkle and Friends, The (1.03 Spanish)",
}

SW = rab_manual.switch_data()
LAMP = rab_manual.lamp_data()
COIL = rab_manual.coil_data()
ASSEMBLIES = {row["Item"]: row for row in rab_manual.table(rab_manual.read_tables(EXCERPT_DIR / "assemblies-and-features.md"), "Playfield - Major Assemblies")}
PLACES = load_json(PLACES_PATH)
FACTS = load_json(RUNTIME_PATH)
ROM_SWITCH = FACTS["rom_switch_names"]
ROM_LAMP = FACTS["rom_lamp_names"]
COIL_TEST = FACTS["coil_test"]
CYCLE = FACTS["cycling_coils_order"]
SERVE = FACTS["trough_serve"]
SWITCHED_PAIRS = {int(switch): fired for switch, fired in FACTS["switched_solenoid_pairs"].items()}
LASER_KICK_TEST = {int(switch): fired for switch, fired in FACTS["laser_kick_test"].items()}
HAT_TARGETS = FACTS["hat_targets"]
AWARDS = FACTS["hat_trick_awards"]
NELL = FACTS["save_nell"]

if PLACES.get("table_bounds") != {"width": 952.0, "height": 2162.0}:
    raise SystemExit(f"tools/rab_places.json must carry the retained table's 952 x 2162 bounds, not {PLACES.get('table_bounds')}")


def prov(status: str, refs) -> dict:
    return {"status": status, "source_refs": list(refs)}


def not_applicable(reason: str, refs) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov("validated", refs)}


def aliases(namespace: str, address: int) -> list[dict]:
    return [{"namespace": namespace, "value": str(address)}]


PLACE_REFS = [TABLE, SCRIPT_REF, EXTRACTION]


def spatial_for(device_id: str, role: str, key: str, *, status: str = "observed") -> dict | None:
    hits = PLACES["placements"].get(key)
    if not hits:
        return None
    hits = sorted(hits, key=lambda hit: (hit["x"], hit["y"]))
    placements = []
    for index, hit in enumerate(hits, start=1):
        suffix = "" if len(hits) == 1 else f".{index}"
        placements.append({
            "id": f"{device_id}.{role}{suffix}", "role": role, "space": "playfield",
            "x": hit["x"], "y": hit["y"], "provenance": prov(status, PLACE_REFS),
        })
    return {"status": status, "placements": placements}


def placed_objects(key: str) -> str:
    hits = sorted(PLACES["placements"].get(key, []), key=lambda hit: (hit["x"], hit["y"]))
    return ", ".join(
        f"{hit['object_type']} {hit['object']}" + (" at its world-space mesh-bounds centre" if hit["coordinate_origin"] == "mesh-bounds-center" else "")
        for hit in hits
    )


def unplaced_reason(key: str) -> str:
    reasons = [entry["reason"] for entry in PLACES["unplaced"] if entry["key"] == key]
    if len(reasons) != 1:
        raise SystemExit(f"tools/rab_places.json must give exactly one unplaced reason for {key}")
    return reasons[0]


def rejected_objects(key: str, marker: str) -> list[str]:
    return sorted(entry["object"] for entry in PLACES["rejected"] if entry["key"] == key and marker in entry["reason"])


def playfield_bulbs(note: str) -> int:
    """Bulbs outside the backbox in a printed flash-lamp note such as '(3) PLFD (1) INSERT (4) NO. 89'."""
    groups = re.findall(r"\((\d+)\) (PLFD|INSERT|LEFT RAMP)", note)
    total = re.search(r"\((\d+)\) NO\. 89$", note)
    if not total or sum(int(count) for count, _ in groups) != int(total.group(1)):
        raise SystemExit(f"cannot read the flash-lamp bulb note {note!r}")
    return sum(int(count) for count, where in groups if where != "INSERT")


def asm(item: str) -> str:
    return ASSEMBLIES[item]["Part No."]


inputs: list[dict] = []
outputs: list[dict] = []

# --- Inputs: the 8 x 8 switch matrix -----------------------------------------------------------------------------
FLIP_SWNO = (15, 16)
HAT_CONFLICTED = (22, 24)
SCRIPT_SWITCH_NOTES = {
    9: "The retained table writes it from the plunger key (Rab_KeyUp/RaB_KeyDown, script lines 356 and 374).",
    10: "The retained table sets it from its Drain kicker (Drain_hit/Drain_UnHit, script lines 2618-2628).",
    11: "The retained table sets it from its trough kicker Kicker3 (script lines 2549-2550).",
    12: "The retained table sets it from its trough kicker Kicker2 (script lines 2551-2552).",
    13: "The retained table sets it from its trough kicker Kicker1 (script lines 2553-2554), the one SolCallback(2) kicks into the shooter lane.",
    14: "The retained table's cvpmImpulseP auto-plunger on its swPlunger trigger reports the switch (plungerIM .switch 14, script line 291).",
    17: "The retained table's cvpmDropTarget dtDrop maps its targets t17-t21 to 17-21 (script line 300).",
    29: "The retained table sets it from its sw29 kicker (sw29_Hit, script lines 1800-1808); its cvpmBallStack bsLEjet names the same switch (line 275).",
    30: "The retained table pulses it from its LeftSlingShot wall (script line 2456).",
    37: (
        "The retained table sets it from its SW37 trigger (script lines 1795-1797), in a subway entered from the playfield that delivers the ball to the "
        "Super VUK kicker sw29; that routing is the table's model, not a printed fact."
    ),
    38: "The retained table pulses it from its RightSlingShot wall (script line 2470).",
    52: "The retained table holds the ball in its sw52 kicker (sw52_Hit, script line 1975) until SolCallback(4) kicks it up.",
}
for _address in (18, 19, 20, 21):
    SCRIPT_SWITCH_NOTES[_address] = SCRIPT_SWITCH_NOTES[17]

for address in range(1, 65):
    chart = SW["chart"][address]
    part = SW["parts"][address]
    unused = address in sem.UNUSED_SWITCHES
    suffix, label = (f"unused-{address}", f"Unused Switch {address}") if unused else sem.SWITCHES[address]
    device_id = f"switch.{suffix}"
    notes = [f"Printed switch-matrix column {chart['column']}, row {chart['row']}; the chart prints '{chart['printed']}'."]
    if unused:
        notes.append(
            f"The Switch Part Numbers table prints '{part['description']}' with the part cell '{part['part_printed']}': the address is strobed but carries no device."
        )
    else:
        notes.append(
            f"The Switch Part Numbers table prints '{part['description']}'"
            + (f", part {part['part']}." if part["part"] else f", with the part cell printed '{part['part_printed']}'.")
        )
    if part["cabinet"]:
        notes.append("The table marks the address with an asterisk, which its footnote reads '* Indicates Cabinet Switches'.")
    if address == 2:
        notes.append(
            "Pinned PinMAME's shared DE_COMPORTS labels this position 'Ball Tilt', a generic platform label; this machine's chart and parts table print '4th Coin'."
        )
    if address == 3:
        notes.append("DE_COMPORTS binds PinMAME's Start input (IPT_START1) to this position; the chart names it Credit Button.")
    if address in HAT_CONFLICTED:
        notes.append(
            "The manual and the ROM disagree on which hat target this is (see the definition's conflict hat-target-switch-order): the chart and the parts table print "
            f"'{part['description']}', and the switch-location drawing reads the stacked callouts top to bottom as 24, 23, 22, while the ROM's Active Switch Test names it "
            f"'{ROM_SWITCH[str(address)]['name']}'. The label follows the ROM; the placement is the retained table's "
            + ("top target t22 (t22_Hit pulses 22, script line 2333)" if address == 22 else "bottom target T24 (t24_Hit pulses 24, script line 2355)")
            + ", and both are marked conflicted."
        )
    if address == 23:
        notes.append("The retained table pulses it from its middle hat target t23 (t23_Hit, script line 2344).")
    if address in (44, 45, 46):
        notes.append(
            "The manual's switch-location drawing puts 44 on the left bumper and 46 on the upper right one, and prints the lower bumper's callout 47 (no 45 appears on a bumper); "
            "the ROM names 44 LEFT, 45 CENTER and 46 RIGHT TURBO BUMPER, so 45 is the lower, center bumper. "
            + {
                44: "The retained table pulses 44 from its left bumper Bumper1 (script line 2422).",
                45: (
                    "The retained table pulses 45 from its upper right bumper Bumper2 and 46 from its lower bumper Bumper3 (script lines 2424 and 2426), swapped against the drawing "
                    "and the ROM; that is a table defect, so 45 is placed on Bumper3, the lower bumper."
                ),
                46: (
                    "The retained table pulses 46 from its lower bumper Bumper3 and 45 from its upper right bumper Bumper2 (script lines 2424 and 2426), swapped against the drawing "
                    "and the ROM; that is a table defect, so 46 is placed on Bumper2, the upper right bumper."
                ),
            }[address]
        )
    if address in SCRIPT_SWITCH_NOTES:
        notes.append(SCRIPT_SWITCH_NOTES[address])
    rom = ROM_SWITCH[str(address)]
    entry: dict[str, Any] = {
        "id": device_id,
        "label": label,
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": address},
        "aliases": aliases("pinmame.switch", address),
        "availability": "unused" if unused else "used",
        "provenance": prov(
            "conflicted" if address in HAT_CONFLICTED else "validated",
            [MANUAL, CORE_H, RUNTIME_SRC] + ([] if unused or address in (2, 3, 4, 5, 6, 7) else [SCRIPT_REF]),
        ),
        "physical": {"notes": ""},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": chart["drive"]["transistor"],
            "drive_wire": chart["drive"]["wire"],
            "drive_connection": chart["drive"]["connector"],
            "return_wire": chart["return"]["wire"],
            "return_connection": chart["return"]["connector"],
        },
    }
    if address in FLIP_SWNO:
        side = "left" if address == 15 else "right"
        button = 84 if address == 15 else 82
        notes.append(
            f"The chart prints the address '{chart['printed']}' and the parts table '{part['description']}' (part {part['part']}, a cabinet switch). Both names denote what "
            f"PinMAME publishes here, the {side} cabinet flipper button: the game data declares FLIP1516 = FLIP_SWNO(15,16) with no FLIP_SOL, so PinMAME models no "
            f"end-of-stroke switch on this machine, and core.c's core_updateSw rewrites this switch on every update from PinMAME's flipper-column button bit {button}. "
            f"A consumer drives {button}, not {address}. The retained table writes {address} itself from the {side} flipper key before handing the key to de.vbs, which writes "
            f"{button} (Rab_KeyUp/RaB_KeyDown, script lines {353 if address == 15 else 354} and {371 if address == 15 else 372}); PinMAME rewrites {address} from {button} on "
            "its next update, so such a write cannot be held."
        )
        notes.append(
            f"ROM evidence (3.20 Active Switch Test): a host write of 1 to public {address} showed '{rom['name']}', wires {rom['wires']} and '#{address}' but fired no flipper "
            f"output, while holding {button} showed the same frame and fired {'47/48' if side == 'left' else '45/46'}; with every public switch at 0 the screen shows NONE."
        )
        entry["roles"] = [f"flipper.lower.{side}.matrix-copy"]
    else:
        notes.append(
            f"ROM evidence (3.20 Active Switch Test): holding public {address} at 1 shows '{rom['name']}', wires {rom['wires']} and '#{address:02d}'; "
            "with every public switch at 0 the same screen shows NONE, so the ROM treats public 1 as the closed contact"
            + (" and names the address NOT USED." if unused else ".")
        )
    if not unused:
        entry["normally_closed"] = False
        notes.append(
            "Contact: the switch-matrix chart shades no cell and marks no opto or normally closed position, so the fitted contact rests open."
        )
    entry["physical"]["notes"] = " ".join(notes)
    if part["part"]:
        entry["physical"]["part_number"] = part["part"]
    if address in sem.SWITCH_TYPES:
        entry["physical"]["switch_type"] = sem.SWITCH_TYPES[address]
    if address in sem.CABINET_ROLES:
        entry["roles"] = [sem.CABINET_ROLES[address]]
    if unused:
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif address in sem.CABINET_ROLES or address in FLIP_SWNO:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, CORE_H] if address in FLIP_SWNO else [MANUAL])
    else:
        located = spatial_for(device_id, "sensor", f"switch.{address}", status="conflicted" if address in HAT_CONFLICTED else "observed")
        if not located:
            raise SystemExit(f"switch {address} is a playfield switch with no retained placement")
        entry["spatial"] = located
        entry["physical"]["notes"] += f" Placed on the retained table's {placed_objects(f'switch.{address}')}."
    inputs.append(entry)

for address, suffix, label, port_label in (
    (-7, "service-advance", "Advance (Black Button)", "Black Button"),
    (-6, "service-up-down", "Up/Down (Green Button)", "Green Button"),
):
    inputs.append({
        "id": f"switch.{suffix}",
        "label": label,
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": address},
        "aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [S11_H, S11_C, MANUAL, RUNTIME_SRC]),
        "physical": {"notes": (
            f"Coin-door diagnostic button, named '{port_label}' by s11.h's DE_COMPORTS and placed in switch column 0 rather than the playfield matrix; Data East defines only "
            "these two (DE_SWADVANCE -7, DE_SWUPDN -6). "
            + (
                "The manual's coil-test text tells the operator to 'depress the STEP push-button switch once' to return to game over. Every retained service run pulses it at "
                "level 1 for 250 ms while the ROM steps to the next test on each pulse and stays put at 0, so public 1 is the depressed button. s11.c hands the PIA the complement "
                "(!core_getSw(DE_SWADVANCE)), the level a contact closing to ground presents, so a momentary push-button that rests released rests with its contact open."
                if address == -7 else
                "PinMAME's port declares it a toggle (COREPORT_BITTOG), and every retained service run sets it to 1 before stepping into the diagnostics. Unlike the Black "
                "button, s11.c hands the PIA the level uncomplemented (core_getSw(DE_SWUPDN)), and no retained page draws the coin-door switch circuit, so which position closes "
                "the contact is not established. Its contact polarity is left undeclared, which keeps the polarity requirement open."
            )
        )},
        **({"normally_closed": False} if address == -7 else {}),
        "spatial": not_applicable("cabinet_or_service", [S11_H, S11_C, MANUAL]),
    })

_FLIPPER_ROWS = {"left": COIL["flippers"]["Left Flipper"], "right": COIL["flippers"]["RightFlipper"]}
_flipper_items = flipper_column_inputs(
    flip_swno=FLIP_SWNO, flip_swno_text="FLIP1516 = FLIP_SWNO(15,16)",
    core_refs=(CORE, CORE_H, CORE_C, S11_C), button_refs=(SCRIPT_REF, VPM_DE_LIBRARY_SOURCE),
    button_notes={
        side: (
            f"The retained known-working script drives it: Rab_KeyUp/RaB_KeyDown hand the {side} flipper key to de.vbs vpmKeyDown/vpmKeyUp (script lines 355 and 373), "
            f"which set Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with {'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} "
            f"(excerpt vpm-script-library-flippers). The physical counterpart is the {side} cabinet flipper button."
        )
        for side in ("left", "right")
    },
    unused_notes=vpm_staged_flipper_notes(library="DE.VBS"),
    unused_note_refs=(VPM_DE_LIBRARY_SOURCE,),
)
for _item in _flipper_items:
    _address = _item["binding"]["device"]
    if _address in (82, 84):
        _matrix = 16 if _address == 82 else 15
        _row = _FLIPPER_ROWS["left" if _address == 84 else "right"]
        _item["provenance"]["source_refs"] += [RUNTIME_SRC, MANUAL]
        _item["physical"]["notes"] += (
            f" ROM evidence (3.20 Active Switch Test): holding public {_address} at 1 shows '{ROM_SWITCH[str(_matrix)]['name']}', the wires "
            f"{ROM_SWITCH[str(_matrix)]['wires']} and '#{_matrix}', the matrix switch core_updateSw copies it into, while the other six flipper-column addresses "
            "(81, 83 and 85-88) show NONE, so the ROM cannot see them."
            f" Contact: the manual's Flipper Solenoids table routes the flipper ground '{_row['CPU to coil']}' through the cabinet flipper switch to the flipper board "
            f"('{_row['Switch to Flip. PCB']}'). A switch in series with the flipper's ground energises the coil while it is closed, so the released button rests open; "
            "public 1 is the pressed button."
        )
        _item["normally_closed"] = False
    else:
        _item["provenance"]["source_refs"].append(RUNTIME_SRC)
        _item["physical"]["notes"] += " ROM evidence: holding this address at 1 in the 3.20 Active Switch Test shows NONE."
inputs.extend(_flipper_items)

inputs.append({
    "id": "dip.jumper-w7",
    "label": "Jumper W7",
    "kind": "dip_switch",
    "binding": {"group": "pinmame.input.dip", "device": 0},
    "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
    "availability": "unknown",
    "provenance": prov("observed", [S11_C]),
    "physical": {"notes": (
        "s11.c declares MDRV_DIPS(1), commented '(actually a jumper)', and pia2a_r reads it as core_getDip(0) << 7 on PIA2 PA7, annotated 'PA7 (I) Jumper W7'. No retained "
        "page of this machine's manual describes W7, so the meaning of the bit is not stated by any retained source."
    )},
    "spatial": not_applicable("dip_switch", [S11_C]),
})

# --- Outputs: drives 1-8, the left (coil) half of the Left/Right relay pair ------------------------------------------
DRIVES = COIL["drives"]
WIRING_LABELS = {1: "1L", 2: "2L", 3: "50V 3L", 4: "50V 4L", 5: "50V 5L", 6: "6L", 7: "7L", 8: "8L"}
LEFT_IDS = {
    1: ("coil.outhole", "Outhole"),
    2: ("coil.trough-eject", "Trough Eject"),
    3: ("coil.hat-trick-lion", "Hat Trick Lion (Backbox)"),
    4: ("coil.playfield-vuk", "Playfield VUK"),
    5: ("coil.super-vuk", "Super VUK"),
    6: ("coil.hat-trick-rocky", "Hat Trick Rocky (Backbox)"),
    7: ("coil.hat-trick-rhino", "Hat Trick Rhino (Backbox)"),
    8: ("coil.knocker", "Knocker"),
}
# (control wire, control connection, power wire, power connection, volts); each value must appear in the printed cell.
LEFT_WIRING = {
    1: ("VIO-BRN", "PPB J2-9", "BRN", "PPD J6-1", 50),
    2: ("VIO-RED", "PPB J2-8", "BRN", "PPD J6-1", 50),
    3: ("VIO-ORN", "PPB J8-2", "YEL-VIO", "PPD J7-8,9", 50),
    4: ("VIO-YEL", "PPB J8-7", "YEL-VIO", "PPD J7-8,9", 50),
    5: ("VIO-GRN", "PPB J8-4", "YEL-VIO", "PPD J7-8,9", 50),
    6: ("VIO-BLU", "PPB J2-4", "WHT", "PPD J6-3", 32),
    7: ("VIO-BLK", "PPB J2-2", "WHT", "PPD J6-3", 32),
    8: ("VIO-GRY", "PPB J2-1", "BRN", "PPD J7-1", None),
}
SCRIPT_BOUND_LEFT = {
    1: "SolCallback(1) = kisort, which kicks the ball held in its Drain kicker into the trough (script lines 163 and 2607-2615)",
    2: "SolCallback(2) = KickBallToLane, which kicks the ball in its trough kicker Kicker1 (switch 13) into the shooter lane and clears 13 (script lines 164 and 2577-2592)",
    3: "SolCallback(3) = HatTrickLion, which raises its backbox lion figure while the solenoid is on and lowers it when off (script lines 165, 1876-1888 and 1919-1971)",
    4: "SolCallback(4) = KickBallUp, which kicks the ball in its sw52 kicker up (script lines 166 and 1977-1980)",
    5: "SolCallback(5) = sw29kick, which kicks the ball in its sw29 kicker out and clears 29 (script lines 167 and 1810-1817)",
    6: "SolCallback(6) = HatTrickRocky, which raises its backbox Rocky figure while the solenoid is on and lowers it when off (script lines 168, 1890-1902 and 1919-1971)",
    7: "SolCallback(7) = HatTrickRhino, which raises its backbox rhino figure while the solenoid is on and lowers it when off (script lines 169, 1904-1917 and 1919-1971)",
    8: "SolCallback(8) = vpmSolSound Knocker (script line 170)",
}
LEFT_ASSEMBLIES = {1: "3", 2: "1", 4: "7", 5: "4"}

for address in range(1, 9):
    row = DRIVES[address]
    device_id, label = LEFT_IDS[address]
    drawn_name, drawn_type = row["Coil as drawn"].rsplit(" ", 1)
    wired = COIL["wiring"][WIRING_LABELS[address]]
    control_wire, control_connection, power_wire, power_connection, volts = LEFT_WIRING[address]
    for value, cell in ((control_wire, "Coil path"), (control_connection.removeprefix("PPB "), "Coil path"), (power_wire, "Coil power"), (power_connection, "Coil power")):
        if value not in row[cell]:
            raise SystemExit(f"drive {address}: {value!r} is not in the schematic's {cell} cell {row[cell]!r}")
    notes = [
        f"Left half of the Left/Right relay pair on drive {address} (the coil chart schematic's '{row['Side labels as printed']}', CPU transistor {row['Transistor']}, CN-11 pin "
        f"{row['CN-11 pin']}, '{row['CPU wire']}' into PPB J1-{row['PPB J1 pin']}); the right half is published at {address + 24}. The schematic draws the coil '{row['Coil as drawn']}' "
        f"on '{row['Coil path']}' with power '{row['Coil power']}'; the Playfield Coil / Flash Lamp Wiring Diagram labels position '{wired['Position label']}' "
        f"'{wired['Coil as labelled']}' {wired['Coil type']}.",
        f"The retained table binds {SCRIPT_BOUND_LEFT[address]}.",
    ]
    if address in (3, 4, 5):
        notes.append(
            "The drive reaches the coil through a TIP 36C booster transistor on the PPB board, as the schematic draws it; the control connection recorded here is the booster's output."
        )
    if address in (3, 6, 7):
        notes.append(
            "A backbox figure coil: page 28's location drawing puts its boxed balloon in the backbox outline, the schematic marks it '(INSERT)', and the Game Specific Features page "
            "says Bullwinkle pulls animals out of his hat when the ball goes into the hole (Rocky lights Extra Ball, Rhino starts the Rhino Bonus countdown, Lion starts the Jackpot). "
            "How the figure moves is not documented in any retained source."
        )
    if address in (6, 7):
        notes.append(
            "The ROM's Coil Test (below) shows the supply wire BRN where the schematic prints WHT; the sources agree on the device and its address, so the structured wiring follows the "
            "schematic and the difference stays here."
        )
    if address == 2:
        notes.append("'THROUGH EJECT' is the schematic's own spelling; the wiring diagram and the ROM print TROUGH EJECT.")
    if address == 8:
        notes.append(
            "The coil chart schematic types the knocker 23-800 and the wiring diagram 22-600, so no part number is recorded. The schematic's left power box prints '+' with no "
            "voltage, so no nominal voltage is recorded either. Page 28's coil location drawing carries no 8L balloon, so the knocker is not placed."
        )
    entry = {
        "id": device_id,
        "label": label,
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC, SCRIPT_REF]),
        "physical": {"notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": row["Transistor"],
            "control_wire": control_wire,
            "control_connection": control_connection,
            "power_wire": power_wire,
            "power_connection": power_connection,
        },
    }
    if volts:
        entry["wiring"].update({"nominal_voltage_v": volts, "voltage_type": "dc"})
    if address != 8:
        if drawn_type != wired["Coil type"]:
            raise SystemExit(f"drive {address}: the schematic's {drawn_type} disagrees with the wiring diagram's {wired['Coil type']}")
        entry["physical"]["part_number"] = drawn_type
    if address in LEFT_ASSEMBLIES:
        entry["physical"]["assembly_part_number"] = asm(LEFT_ASSEMBLIES[address])
    if address in (3, 6, 7):
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    elif address != 8:
        located = spatial_for(device_id, "effect", f"solenoid.{address}")
        if not located:
            raise SystemExit(f"solenoid {address} has no retained placement")
        entry["spatial"] = located
        entry["physical"]["notes"] += (
            f" Placed on the retained table's {placed_objects(f'solenoid.{address}')}, the table's model of the mechanism this coil actuates, not a claimed winding centre."
        )
    outputs.append(entry)

# --- Outputs: drives 9-16, direct on CPU CN12 -------------------------------------------------------------------------
DIRECT = COIL["direct"]
DIRECT_IDS = {
    9: ("motor", "motor.saw", "Saw Motor Relay"),
    10: ("relay", "relay.left-right-relay", "Left/Right Relay"),
    11: ("gi", "gi.general-illumination", "G.I. Relay"),
    12: ("coil", "coil.ramp-diverter", "Ramp Diverter"),
    13: ("coil", "coil.playfield-diverter", "Playfield Diverter"),
    14: ("coil", "coil.top-control-gate", "Top Control Gate"),
    15: ("coil", "coil.drop-target-reset", "Drop Target Reset"),
    16: ("coil", "coil.auto-launch", "Auto Launch"),
}
# (power wire, power connection, volts); the wire must appear in the printed power cell.
DIRECT_POWER = {
    9: ("RED", None, 32), 10: ("RED-WHT", "P.S. CN3-5", 32), 11: (None, None, None), 12: ("RED", "P.S. CN3-6/7/8", 32),
    13: ("RED", None, 32), 14: ("RED", None, 32), 15: ("RED", None, 32), 16: ("VIO-YEL", "PPB J7-3", 50),
}
DIRECT_NOTES = {
    9: (
        "The relay coil switches the saw motor of Nell's Log Assembly (Major Assemblies item 14, 500-5638-00): the relay's normally open contact passes 28 VAC from BR2 to "
        "the SAW MOTOR, so the motor runs while the solenoid is on. Page 28's location drawing puts balloon 9 on the right side above the shooter lane, beside the drop-target "
        "bank. The retained table binds SolCallback(9) = SolNell, which swings its log back and forth between two limits and spins its saw blade while the solenoid is on and "
        "stops both where they are when it turns off (script lines 171 and 1347-1397)."
    ),
    10: (
        "Energising it re-routes drives 1-8 from the coils (left set) to the flash lamps (right set): page 28 says the relay switches +32 volts between them, and pinned "
        "PinMAME publishes the right set at 25-32 (s11.c updsol, muxSol 10). The schematic draws the L/R COIL RELAY on the P/O PPD board (J6-9 to J6-7) where page 28's text "
        "says the relay is located on the PPB board; the two pages agree on the device and its drive and differ only on the board. The wiring diagram's note names the relay's "
        "normally closed side LEFT (A) and its normally open side RIGHT (B). The retained table binds nothing to 10: its flash-lamp callbacks are bound to 25-32."
    ),
    11: (
        "There is no GI channel on this platform: the general illumination is solenoid 11, the G.I. relay on the power-supply board (the schematic's 'GENERAL ILLUM. RELAY' at "
        "P.S. CN7-1/3). s11.c types it CORE_MODOUT_BULB_44_6_3V_AC_REV for the rab_ games, so a consumer shows the G.I. lit while solenoid 11 is off; the retained table's SolGi "
        "(SolCallback(11), script lines 172 and 2683-2698) turns its G.I. off while the solenoid is on, fading the 84 bulb-mode Lights of its TheGICollection (line 2879). "
        "Only two of those Lights, gi5a and gi6a, draw a bulb, and no retained page counts or locates the G.I. bulbs, so no quantity or coordinate is claimed."
    ),
    12: (
        "The retained table binds SolCallback(12) = SolDiverter2, which swings its ramp diverter open while the solenoid is on and back when it turns off (script lines 173 and 1240-1256)."
    ),
    13: (
        "The retained table binds SolCallback(13) = SolDiverter1, which swings its playfield diverter open while the solenoid is on and back when it turns off (script lines 174 and 1301-1317)."
    ),
    14: (
        "The Major Assemblies list's item 28 is the Gate Lift Coil (515-5711-00), its balloon at the top centre. The retained table binds SolCallback(14) = TopGate, which makes "
        "its gate Gate2 non-collidable while the solenoid is on (script lines 175 and 1286-1296)."
    ),
    15: (
        "It resets the five-bank (Major Assemblies item 12, 5 Bank Drop Target Assy). The retained table binds SolCallback(15) = DropsUp, which raises all five of its targets "
        "when the solenoid turns on (script lines 176 and 2256-2265)."
    ),
    16: (
        "The coil chart schematic types the coil 23-800 and the wiring diagram 22-600, so no part number is recorded. The CPU line WHT-GRY from CN12-9 drives the PPB booster Q1 "
        "(TIP 36C); the schematic draws the booster's input and output on J8-11 and J8-12 with VIO-GRY to the coil, while the wiring diagram draws the pins the other way round "
        "and BRN-GRY. The sources agree on the device, its drive and its supply, so the structured wiring records the CPU side and the difference stays here. The retained table "
        "binds SolCallback(16) = SolAutoPlungerIM, which fires its impulse plunger on the swPlunger trigger (script lines 177 and 1225-1230)."
    ),
}
DIRECT_PARTS = {12: "27-1400", 13: "23-800", 14: "31-1800", 15: "22-600"}
DIRECT_ASSEMBLIES = {9: "14", 14: "28", 15: "12", 16: "9"}
for address in range(9, 17):
    row = DIRECT[address]
    kind, device_id, label = DIRECT_IDS[address]
    power_wire, power_connection, volts = DIRECT_POWER[address]
    if power_wire and power_wire not in row["Power"]:
        raise SystemExit(f"drive {address}: {power_wire!r} is not in the printed power cell {row['Power']!r}")
    if address in DIRECT_PARTS and DIRECT_PARTS[address] not in row["Load as drawn"]:
        raise SystemExit(f"drive {address}: part {DIRECT_PARTS[address]} is not in the printed load {row['Load as drawn']!r}")
    notes = [
        f"The coil chart schematic draws drive {row['Drive']} (CPU transistor {row['Transistor']}, pin {row['Pin']}, {row['Wire']}) to '{row['Load as drawn']}' with power "
        f"'{row['Power']}'; the wiring diagram's CPU legend prints the pin as CN12-{row['Pin']}.",
        DIRECT_NOTES[address],
    ]
    entry = {
        "id": device_id,
        "label": label,
        "kind": kind,
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC] + ([] if address == 10 else [SCRIPT_REF])),
        "physical": {"notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": row["Transistor"],
            "control_wire": row["Wire"],
            "control_connection": f"CPU CN12-{row['Pin']}",
        },
    }
    if power_wire:
        entry["wiring"]["power_wire"] = power_wire
    if power_connection:
        entry["wiring"]["power_connection"] = power_connection
    if volts:
        entry["wiring"].update({"nominal_voltage_v": volts, "voltage_type": "dc"})
    if address in DIRECT_PARTS:
        entry["physical"]["part_number"] = DIRECT_PARTS[address]
    if address in DIRECT_ASSEMBLIES:
        entry["physical"]["assembly_part_number"] = asm(DIRECT_ASSEMBLIES[address])
    if address == 11:
        entry["roles"] = ["playfield.general-illumination"]
    if address == 10:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    elif address != 11:
        located = spatial_for(device_id, "effect", f"solenoid.{address}")
        if not located:
            raise SystemExit(f"solenoid {address} has no retained placement")
        entry["spatial"] = located
        entry["physical"]["notes"] += (
            f" Placed on the retained table's {placed_objects(f'solenoid.{address}')}"
            + (
                ", a projection: the table models no reset coil, so the coordinate is the middle drop target, where DropsUp plays its reset sound."
                if address == 15 else
                ", the table's model of the mechanism this output drives, not a claimed winding or motor centre."
            )
        )
    outputs.append(entry)

# --- Solenoids 17-22: the CPU-controlled auxiliary (switched) solenoids ------------------------------------------------
SWITCHED = COIL["switched"]
AUX_IDS = {
    17: ("coil.left-turbo-bumper", "Left Turbo Bumper", 44),
    18: ("coil.center-turbo-bumper", "Center Turbo Bumper", 45),
    19: ("coil.right-turbo-bumper", "Right Turbo Bumper", 46),
    20: ("coil.left-slingshot", "Left Slingshot", 30),
    21: ("coil.right-slingshot", "Right Slingshot", 38),
    22: ("coil.laser-kick", "Laser Kick", 32),
}
AUX_SCRIPT = {
    17: "leaves SolCallback(17) commented out (script line 178): its VPX bumper Bumper1 kicks the ball on contact",
    18: "leaves SolCallback(18) commented out (script line 179): its VPX bumpers kick the ball on contact",
    19: "leaves SolCallback(19) commented out (script line 180): its VPX bumpers kick the ball on contact",
    20: "binds nothing to 20: its LeftSlingShot wall kicks the ball on contact (script line 2456)",
    21: "binds nothing to 21: its RightSlingShot wall kicks the ball on contact (script line 2470)",
    22: "binds SolCallback(22) = AutoPlungeLK, which enables its LaserKick kicker only while the solenoid is on (script lines 181 and 1851-1857); LaserKick_Hit kicks the ball back out (line 1859)",
}
for address in range(17, 23):
    row = SWITCHED[address]
    device_id, label, switch = AUX_IDS[address]
    control_wire, control_connection = row["Control line"].split(" ", 1)
    power_wire, power_connection = row["Power line"].split(" ", 1)
    proof = LASER_KICK_TEST if address == 22 else SWITCHED_PAIRS
    if proof.get(switch) != [address]:
        raise SystemExit(f"solenoid {address}: the ROM run did not fire it from switch {switch}")
    notes = [
        f"Page 28's CPU Controlled Auxiliary Solenoids table prints coil {address} '{row['Description']}', control '{row['Control line']}', power '{row['Power line']}', "
        f"transistor {row['Drive transistor']} and type {row['Coil type']}. One of the six switched solenoids: CORE_FIRSTSSSOL is 17 and Data East's PIA permutation publishes "
        "them at 17 + ssSolNo, so the printed coil number and the public address are different identities that only a ROM run can pair (see the ROM evidence below).",
        f"The retained table {AUX_SCRIPT[address]}.",
        (
            f"ROM evidence (3.20 Laser Kick Test): closing the left outlane switch {switch} fires public {address} and nothing else."
            if address == 22 else
            f"ROM evidence (3.20, a game in play): closing switch {switch} fires public {address}."
        ),
    ]
    if address in (17, 18, 19):
        notes.append("Page 47's Playfield Special Coil Diagram calls the bumpers THUMPER BUMPER where page 28 prints Turbo Bumper; both name the same coils.")
    if address == 18:
        notes.append("'Cemter' is page 28's own spelling.")
    if address == 22:
        notes.append(
            "Page 47's Playfield Special Coil Diagram draws the line at CN19-9 as WHT-BRN through a Q2 booster on PPB J8 pins 10 and 9 with BLK-BLU to the coil, where pages 28 "
            "and 46 print BLU-BLK; the structured wiring follows the two agreeing pages. Major Assemblies item 2 (Kick Back Assembly) is this kicker."
        )
    entry = {
        "id": device_id,
        "label": label,
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC, SCRIPT_REF]),
        "physical": {"part_number": row["Coil type"], "notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board", "driver_transistor": row["Drive transistor"],
            "control_wire": control_wire, "control_connection": control_connection,
            "power_wire": power_wire, "power_connection": power_connection,
            "nominal_voltage_v": 50 if address == 22 else 32, "voltage_type": "dc",
        },
    }
    entry["physical"]["assembly_part_number"] = asm({17: "6", 18: "6", 19: "6", 20: "5", 21: "5", 22: "2"}[address])
    located = spatial_for(device_id, "effect", f"solenoid.{address}")
    if not located:
        raise SystemExit(f"solenoid {address} has no retained placement")
    entry["spatial"] = located
    entry["physical"]["notes"] += f" Placed on the retained table's {placed_objects(f'solenoid.{address}')}."
    outputs.append(entry)

outputs.append({
    "id": "control.game-on",
    "label": "Game On / Switched Solenoid Enable",
    "kind": "control_signal",
    "binding": {"group": "pinmame.output.solenoid", "device": 23},
    "aliases": aliases("pinmame.solenoid", 23),
    "availability": "used",
    "provenance": prov("validated", [S11_C, S11_H]),
    "physical": {"notes": (
        "S11_GAMEONSOL is 23, driven by PIA0 CB2 (s11.c pia0cb2_w). It enables the switched solenoids and gates the flippers rather than driving a device of its own; "
        "core_updateSw passes it to the flipper synthesis as the enable. The retained table binds nothing to 23."
    )},
    "spatial": not_applicable("virtual", [S11_C]),
})
outputs.append({
    "id": "virtual.unused-24",
    "label": "Unused Solenoid 24",
    "kind": "virtual",
    "binding": {"group": "pinmame.output.solenoid", "device": 24},
    "aliases": aliases("pinmame.solenoid", 24),
    "availability": "unused",
    "provenance": prov("validated", [S11_C, RUNTIME_SRC]),
    "physical": {"notes": "Reserved slot between the switched solenoids and the muxed right set; s11.c publishes nothing here, and no retained run moved it."},
    "spatial": not_applicable("unused", [S11_C]),
})

# --- Solenoids 25-32: the right half of the relay pair, all flash lamps ------------------------------------------------
for address in range(25, 33):
    drive = address - 24
    row = DRIVES[drive]
    test = next(item for item in COIL_TEST if item["number"] == f"#{drive}R")
    flash_wire = row["Flash path"].split(", ")[1]
    notes = (
        f"Right half of the Left/Right relay pair on drive {drive}; the left half is published at {drive}. The coil chart schematic draws the flash path '{row['Flash path']}' "
        f"from PPB J9 to four No. 89 bulbs on '{row['Flash power']}' and labels them '{row['Bulb note as drawn']}'; PinMAME types the whole 25-32 block as No. 89 flashers "
        f"('8 muxed flasher outputs (K1 relay is solenoid #10)', s11.c line 1202). The retained table binds SolCallback({address}) = SetLamp {100 + drive} (script line {184 + drive}). "
        "'INSERT' is the backbox: page 28's location drawing puts 1R, 4R, 6R, 7R and two 8R balloons in its backbox outline."
    )
    if drive in (1, 6):
        notes += (
            f" The ROM's Coil Test (below) shows the flash return '{test['wires'].split(' ')[1]}' where the schematic prints {flash_wire}; the sources agree on the device and its "
            "address, so the structured wiring follows the schematic and the difference stays here."
        )
    if drive == 5:
        notes += " The schematic prints this drive's side label 'SIDE R 06' (sic); the wiring diagram and the ROM put the group on 5R."
    if drive == 4:
        notes += (
            " The wiring diagram on page 46 draws four bulbs for this group under '(3) PLFD (1) INSERT' but labels them '(3) NO. 89', where every other group "
            "reads '(4) NO. 89'; the drawn bulbs, the group label's three plus one and this schematic all give four, which the quantity follows."
        )
    if drive == 7:
        notes += " The schematic's fourth bulb is an insert; the ROM's name for it is '1 TOP' (below)."
    entry = {
        "id": f"flasher.{drive}r",
        "label": f"Flash Lamps {drive}R ({test['name'].removeprefix('FL: ')})",
        "kind": "flasher",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, SCRIPT_REF, RUNTIME_SRC]),
        "physical": {"part_number": "#89", "quantity": 4, "notes": notes},
        "wiring": {
            "board": "CPU Board", "driver_transistor": row["Transistor"],
            "control_wire": flash_wire, "control_connection": f"PPB {row['Flash path'].split(', ')[0]}",
            "power_wire": "ORN", "power_connection": "PPD J6-4,5",
            "nominal_voltage_v": 32, "voltage_type": "dc",
        },
    }
    if "ORG" in row["Flash power"]:
        entry["physical"]["notes"] += " The schematic prints the supply wire 'ORG' on this drive and 'ORN' on drives 1, 2 and 8; both denote orange and are recorded as ORN."
    key = f"solenoid.{address}"
    located = spatial_for(entry["id"], "emitter", key)
    outside = playfield_bulbs(row["Bulb note as drawn"])
    no_bulb = rejected_objects(key, "draws no bulb")
    if located:
        entry["spatial"] = located
        hits = sorted(PLACES["placements"][key], key=lambda hit: (hit["x"], hit["y"]))
        several = len(hits) > 1
        entry["physical"]["notes"] += (
            f" Placed on the bulb{'s' if several else ''} the retained table models for the group, {placed_objects(key)}: its script fades the filament and glass "
            f"primitives on {'each' if several else 'the'} base with SetLamp {100 + drive}, and the bound Light{'s' if several else ''} "
            f"{' and '.join(hit['bound_light'] for hit in hits)} sit{'' if several else 's'} inside the glass but draw{'' if several else 's'} no bulb of "
            f"{'their' if several else 'its'} own. The table models {len(hits)} of the {outside} bulbs the schematic counts outside the backbox, so the placements are "
            "the table's modelled bulbs, not a socket survey."
        )
    else:
        entry["physical"]["notes"] += f" Not placed: {unplaced_reason(key).split(': ', 1)[1]}."
    if located and no_bulb:
        plural = len(no_bulb) > 1
        entry["physical"]["notes"] += (
            f" The script also fades the bulb-mode Light{'s' if plural else ''} {', '.join(no_bulb)} with this group; {'they draw' if plural else 'it draws'} no bulb "
            f"(show_bulb_mesh false) and sit{'' if plural else 's'} on no modelled bulb, so a placement there would not be a socket."
        )
    outputs.append(entry)

# --- 33-36: inert on this generation --------------------------------------------------------------------------------
for address in range(33, 37):
    outputs.append({
        "id": f"virtual.inert-{address}",
        "label": f"Inert Solenoid Address {address}",
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address),
        "availability": "unused",
        "provenance": prov("validated", [CORE_C]),
        "physical": {"notes": (
            "core_getSol serves 33-36 only for the WPC and SAM generations (driver-specific flipper and game-on remaps); the rab_ game data is GEN_DEDMD32, so the address always reads 0."
        )},
        "spatial": not_applicable("virtual", [CORE_C]),
    })

# --- 37-44: PIA2 port B, the CN3 printer data lines ---------------------------------------------------------------------
PRINTER_PINS = {0: 9, 1: 8, 2: 7, 7: 1}
for index, address in enumerate(range(37, 45)):
    pin = PRINTER_PINS.get(index)
    pin_text = (
        f"CN3 pin {pin}" if pin is not None else
        "a CN3 pin the comment elides: it states pins 9, 8 and 7 for bits 0-2 and pin 1 for bit 7, so bits 3-6 occupy four of pins 2-6"
    )
    outputs.append({
        "id": f"virtual.cn3-line-{address}",
        "label": f"CN3 Printer Data Line {index}" + (f" (CN3 pin {pin})" if pin is not None else ""),
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address),
        "availability": "unknown",
        "provenance": prov("candidate", [CORE_C, S11_C, MANUAL, RUNTIME_SRC]),
        "physical": {"notes": (
            f"The game data sets S11_PRINTERLINE, so s11.c's pia2b_w publishes PIA2 port B bit {index} here as the extSol bit that core_getSol reads at 37 + {index} ({pin_text}; "
            "the comment heads the list 'CN3 Printer Data Lines (Used by various games)'). The same handler also writes the byte to the modulated-output block starting at "
            "CORE_MODOUT_SOL0 + 40. ROM evidence (3.20): the line never changed in any retained run - the service tests, a game start and five in-game probes. No retained page of "
            "this machine's manual shows anything fitted to CN3, and failure to observe a change does not prove the line unused, so its availability stays unknown."
        )},
        "spatial": not_applicable("virtual", [S11_C]),
    })

# --- 45-48: PinMAME's synthetic lower flipper outputs ---------------------------------------------------------------------
FLIPPERS = {
    45: ("Synthetic Lower Right Flipper Power", "right"), 46: ("Synthetic Lower Right Flipper Hold", "right"),
    47: ("Synthetic Lower Left Flipper Power", "left"), 48: ("Synthetic Lower Left Flipper Hold", "left"),
}
for address, (label, side) in FLIPPERS.items():
    row = _FLIPPER_ROWS[side]
    control_wire, control_connection = row["CPU to coil"].split(" ", 1)
    power_wire, power_connection = row["Power line, Flip. PCB to coil"].split(" ", 1)
    notes = (
        "Not a CPU-driven output on this machine. The game data declares no FLIP_SOL, so core.c's core_updateSw synthesises these bits whenever the switched-solenoid enable "
        f"(public 23) is on and the corresponding cabinet button bit of PinMAME's flipper column is set: public {82 if side == 'right' else 84}, the same bit it copies into matrix "
        f"switch {16 if side == 'right' else 15}. Power and hold therefore assert and release together and are not independently controllable; a recreation must not model them as "
        f"two coils. The physical coil ({row['Coil type']}, Major Assemblies item {'10 Flipper Assy. Right' if side == 'right' else '11 Flipper Assy Left'}) is driven from the "
        f"flipper board: the manual's Flipper Solenoids table prints the flipper ground '{row['CPU to coil']}', the switch line '{row['Switch to Flip. PCB']}' and the power line "
        f"'{row['Power line, Flip. PCB to coil']}'."
    )
    if side == "right":
        notes += " The right flipper's power cell prints CN1-1, the same pin as its switch line; both are literal, and the pin is recorded as printed."
    if address in (46, 48):
        notes += (
            f" The retained table binds SolCallback({'sLRFlipper' if address == 46 else 'sLLFlipper'}) = {'solRFlipper' if address == 46 else 'solLFlipper'} "
            f"(script line {162 if address == 46 else 161}; core.vbs defines sLRFlipper = 46 and sLLFlipper = 48), which rotates its flipper to the end while the output is on "
            "(script lines 1405-1423)."
        )
    else:
        notes += f" The retained table binds nothing to {address}."
    outputs.append({
        "id": f"virtual.flipper-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE_C, CORE_H] + ([SCRIPT_REF, VPM_DE_LIBRARY_SOURCE] if address in (46, 48) else [])),
        "physical": {
            "part_number": row["Coil type"],
            "assembly_part_number": asm("10" if side == "right" else "11"),
            "notes": notes,
        },
        "wiring": {
            "board": "Flipper Board", "control_wire": control_wire, "control_connection": control_connection,
            "power_wire": power_wire, "power_connection": power_connection,
        },
        "spatial": not_applicable("virtual", [MANUAL, CORE_C]),
    })
for address, label, note in (
    (49, "Simulation Ball Shooter", "CORE_FIRSTSIMSOL is 49; a simulator slot, not machine hardware."),
    (50, "Reserved Solenoid 50", "The last address below CORE_FIRSTCUSTSOL (51); the rab_ game data declares no custom solenoid."),
):
    outputs.append({
        "id": f"virtual.reserved-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address),
        "availability": "unused",
        "provenance": prov("validated", [CORE_C]),
        "physical": {"notes": note},
        "spatial": not_applicable("virtual", [CORE_C]),
    })

# --- Lamps 1-64 ---------------------------------------------------------------------------------------------------------
for address in range(1, 65):
    chart = LAMP["chart"][address]
    location = LAMP["location"][address]
    suffix, label = sem.LAMPS[address]
    drive_wire = re.sub(r"-\s+", "-", chart["drive"]["wire"])
    notes = [f"Printed lamp-matrix column {chart['column']}, row {chart['row']}; the chart prints '{chart['printed']}' and the lamp number table '{location}'."]
    if drive_wire != chart["drive"]["wire"]:
        notes.append(f"The chart's column header prints the drive wire '{chart['drive']['wire']}' with a space after the hyphen; it is recorded as {drive_wire}.")
    if address == 16:
        notes.append("The lamp-location drawing prints callout 16 twice, at the left ramp entrance and at the upper right above 54; one lamp is claimed.")
    if address == 53:
        notes.append("The lamp-location drawing prints no callout 53.")
    if address in sem.CABINET_LAMPS:
        notes.append(
            "A cabinet lamp: it lights the " + ("Credit (Start) button" if address == 15 else "Launch Button") + ", and the lamp-location drawing gives it no callout."
        )
    elif address <= 14:
        notes.append("One of the Spin & Win pie insert lamps at the top right of the playfield; the retained script binds only a primitive and a Flasher sprite to it, never a bulb.")
    elif address in (16, 53):
        notes.append(
            "The retained script fades a raised bulb primitive and a Flasher sprite with this lamp ("
            + ("FadePri4m 16, pRbulb and Flashc 16, flasher16b, script lines 2960-2966" if address == 16 else "FadePri4m 53, pWBbulb and Flashc 53, flasher16a, script lines 2949-2955")
            + "), but it binds lamp 16 to the bulb at the right ramp entrance (beside switch 49) and 53 to the one at the left ramp entrance (beside switch 47), crossed against "
            "the chart, the lamp drawing's left-ramp callout 16 and the ROM's names (16 LEFT RAMP ENTRANCE, 53 RIGHT RAMP ENTRANCE). That crossing is a table defect. The drawing "
            "prints no 53, so the lamp is not placed until a check against the drawing settles which bulb is which."
        )
    else:
        notes.append("The retained script binds only an insert overlay, primitive or sprite to it, never a bulb, so the lamp is not placed.")
    rom = ROM_LAMP[str(address)]
    notes.append(
        f"ROM evidence (3.20 Lamp Test): the single-lamp test lights public lamp {address} under '{rom['name']}', wires {rom['wires']}, '#{address:02d}', and no other lamp."
    )
    entry = {
        "id": f"lamp.{suffix}",
        "label": label,
        "kind": "lamp",
        "binding": {"group": "pinmame.output.lamp", "device": address},
        "aliases": aliases("pinmame.lamp", address),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE_C, S11_C, RUNTIME_SRC]),
        "physical": {"notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": chart["drive"]["transistor"],
            "drive_wire": drive_wire,
            "drive_connection": chart["drive"]["connector"],
            "return_wire": chart["return"]["wire"],
            "return_connection": chart["return"]["connector"],
            "return_component": chart["return"]["transistor"],
        },
    }
    if address in sem.CABINET_LAMPS:
        entry["roles"] = [sem.CABINET_LAMPS[address]]
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    outputs.append(entry)

# --- ROM evidence on the outputs ------------------------------------------------------------------------------------------
_BY_ADDRESS: dict[int, list[dict]] = {}
for _entry in COIL_TEST:
    for _number in _entry["fired"]:
        if _number != 10:
            _BY_ADDRESS.setdefault(_number, []).append(_entry)


def rom_output_note(address: int) -> str | None:
    """The ROM's own name and the Coil Test's response for one public solenoid address."""
    sentences = []
    for entry in _BY_ADDRESS.get(address, []):
        relay = " with the relay at 10 turned on first" if 10 in entry["fired"] else ""
        sentences.append(
            f"ROM evidence (3.20 Coil Test): entry {entry['number']} is named '{entry['name']}' with the wires '{entry['wires']}', and pressing Start on it fires public "
            f"{address}{relay} and nothing else."
        )
    if address in CYCLE:
        sentences.append(f"The automatic Cycling Coils test fires public {address} as step {CYCLE.index(address) + 1} of its {len(CYCLE)}-step cycle.")
    if address == 10:
        sentences.append(
            "ROM evidence (3.20): the Coil Test has no entry #10; each R entry turns public 10 on before it fires its flash lamps, and Cycling Coils asserts 10 before each of 25-32."
        )
    return " ".join(sentences) or None


for entry in outputs:
    group, address = entry["binding"]["group"], entry["binding"]["device"]
    if group == "pinmame.output.solenoid":
        note = rom_output_note(address)
        if note:
            entry["physical"]["notes"] += " " + note
            if RUNTIME_SRC not in entry["provenance"]["source_refs"]:
                entry["provenance"]["source_refs"].append(RUNTIME_SRC)
for _address in [*range(1, 10), *range(11, 23), *range(25, 33)]:
    if _address not in _BY_ADDRESS:
        raise SystemExit(f"the Coil Test fired nothing at public {_address}")

# --- Displays -----------------------------------------------------------------------------------------------------------
displays = [{
    "id": "display.dmd",
    "label": "128x32 Dot Matrix Display",
    "kind": "dmd",
    "controller_index": 0,
    "width": 128,
    "height": 32,
    "physical_location": "cabinet_or_service",
    "provenance": prov("validated", [CORE, RUNTIME_SRC]),
    "spatial": not_applicable("cabinet_or_service", [CORE]),
}]

# --- Mechanisms -------------------------------------------------------------------------------------------------------------
MECH_REFS = [MANUAL, SCRIPT_REF]
_first, _repeat = AWARDS[0], AWARDS[1]
mechanisms = [
    {
        "id": "mechanism.trough",
        "label": "Outhole, Three-Ball Trough and Trough Eject",
        "kind": "kicker",
        "actuators": ["coil.outhole", "coil.trough-eject"],
        "sensors": ["switch.outhole", "switch.trough-1-left", "switch.trough-2-center", "switch.trough-3-right", "switch.shooter-lane"],
        "assembly_part_number": asm("1"),
        "behavior": (
            f"The Outhole Assy ({asm('3')}) on drive 1 kicks a drained ball from the outhole switch 10 into a three-ball trough (11 left, 12 center, 13 right, the release "
            f"position), and the Ball Feed Assy (Trough Eject, {asm('1')}) on drive 2 kicks the ball at 13 into the shooter lane, where switch 14 senses it. ROM evidence (3.20 "
            f"game start, the host moving the balls): with balls on 11-13 the ROM pulsed the Trough Eject {SERVE['trough_eject_pulses_after_start_with_13_closed']} times after "
            f"Start while 13 stayed closed and {SERVE['trough_eject_pulses_with_the_ball_on_14']} times while the served ball rested on 14; it pulsed the Outhole "
            f"{SERVE['outhole_pulses_while_10_closed']} times while a drained ball held 10 closed, and once that ball reached 11 it pulsed the Trough Eject "
            f"{SERVE['trough_eject_pulses_after_the_drained_ball_reached_11']} times to serve the next ball. The host moved every ball, so the counts are the ROM's retries, not "
            "travel times. The retained table rests its balls on three trough kickers and kicks them on the same two solenoids."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.auto-launch",
        "label": "Auto Launch",
        "kind": "kicker",
        "actuators": ["coil.auto-launch"],
        "sensors": ["switch.shooter-lane", "switch.launch-button"],
        "assembly_part_number": asm("9"),
        "behavior": (
            f"The Ball Launch Assy ({asm('9')}) on drive 16, through the PPB booster at 50 V, launches the ball waiting on the shooter lane switch 14 when the player presses the "
            "cabinet Launch Button 9. Adjustment 47 (Trigger Enabled) lets the button fire the launcher during the Bomb Fuse animation. ROM evidence (3.20 game start): with the "
            f"ball on 14 the ROM fired nothing until the Launch Button was pressed, which fired {SERVE['launch_button_with_ball_on_14_fired']}. The retained table fires a "
            "cvpmImpulseP auto-plunger on its swPlunger trigger from the solenoid."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.laser-kick",
        "label": "Laser Kick (Left Outlane Kickback)",
        "kind": "kicker",
        "actuators": ["coil.laser-kick"],
        "sensors": ["switch.left-outlane"],
        "assembly_part_number": asm("2"),
        "behavior": (
            f"The Kick Back Assembly ({asm('2')}) on switched solenoid 22, 23-800 through a PPB booster at 50 V, kicks a ball back out of the left outlane. The Game Specific Features "
            "page says return-lane rollovers raise the Laser Kick value and the right orbit relights and collects it. ROM evidence (3.20 Laser Kick Test): closing the left outlane "
            "switch 32 fires public 22. The retained table arms its LaserKick kicker only while 22 is on."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.super-vuk",
        "label": "Super VUK (Left Rail)",
        "kind": "kicker",
        "actuators": ["coil.super-vuk"],
        "sensors": ["switch.super-vuk"],
        "assembly_part_number": asm("4"),
        "behavior": (
            f"The Super VUK ({asm('4')}, balloon boxed on the left rail) on drive 5, through a PPB booster at 50 V, raises the ball from switch 29. ROM evidence (3.20 Laser Kick "
            "Test): closing 29 fires public 5. In the retained table the Under Trough switch 37 sits in a subway entered from the playfield that delivers the ball to the Super VUK; "
            "that routing is the table's model, and no ROM run tied 37 to 5."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.playfield-vuk",
        "label": "Playfield VUK (Hat Trick Hole)",
        "kind": "kicker",
        "actuators": ["coil.playfield-vuk"],
        "sensors": ["switch.vuk"],
        "assembly_part_number": asm("7"),
        "behavior": (
            f"The Vertical Up Kicker ({asm('7')}) on drive 4, through a PPB booster at 50 V, raises the ball from the Hat Trick hole (switch 52) at the upper left onto the VUK "
            f"Ramp ({asm('18')}). ROM evidence (3.20): the Laser Kick Test fires public 4 from 52, and in the Hat Trick probes the ROM kicked "
            f"{min(a['vuk_4_kick_after_52_closed_s'] for a in AWARDS)}-{max(a['vuk_4_kick_after_52_closed_s'] for a in AWARDS)} s after 52 closed."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.playfield-diverter",
        "label": "Playfield Diverter (Left Orbit to the Hat Trick Hole)",
        "kind": "diverter",
        "actuators": ["coil.playfield-diverter"],
        "sensors": [],
        "behavior": (
            "The Playfield Diverter coil (drive 13, 23-800) diverts a ball rolling up the left orbit into the Hat Trick hole while Hat Trick is lit. No switch reports its "
            f"position. ROM evidence (3.20 Hat Trick probes): the ROM turned 13 on as the ball passed the left orbit bottom switch 33, held it about {_first['diverter_13_on_s']} s "
            f"and dropped it {min(a['diverter_13_off_after_52_closed_s'] for a in AWARDS)}-{max(a['diverter_13_off_after_52_closed_s'] for a in AWARDS)} s after the hole switch 52 "
            "closed, so the diverter is a held output. The retained table swings its diverter while 13 is on. Which of the two Diverter Assemblies in the Major Assemblies list "
            "(items 15 and 16) this coil moves is not stated."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.ramp-diverter",
        "label": "Ramp Diverter",
        "kind": "diverter",
        "actuators": ["coil.ramp-diverter"],
        "sensors": [],
        "behavior": (
            "The Ramp Diverter coil (drive 12, 27-1400) moves a ramp diverter at the upper left. No switch reports its position, and no retained run exercised it in a game. The "
            "retained table swings its diverter open while 12 is on and back when it turns off."
        ),
        "provenance": prov("observed", MECH_REFS),
    },
    {
        "id": "mechanism.top-gate",
        "label": "Top Control Gate",
        "kind": "gate",
        "actuators": ["coil.top-control-gate"],
        "sensors": [],
        "assembly_part_number": asm("28"),
        "behavior": (
            f"The Gate Lift Coil ({asm('28')}, drive 14, 31-1800) lifts a control gate at the top centre of the playfield. No switch reports its position, and no retained run "
            "exercised it in a game. The retained table makes its gate non-collidable while 14 is on."
        ),
        "provenance": prov("observed", MECH_REFS),
    },
    {
        "id": "mechanism.drop-targets",
        "label": "Five-Bank Drop Targets",
        "kind": "drop_target_bank",
        "actuators": ["coil.drop-target-reset"],
        "sensors": [f"switch.{sem.SWITCHES[a][0]}" for a in range(17, 22)],
        "assembly_part_number": asm("12"),
        "behavior": (
            f"The 5 Bank Drop Target Assy ({asm('12')}) on the right of the playfield: targets 17 (top) to 21 (bottom), reset together by drive 15 (22-600). ROM evidence (3.20 "
            f"Save Nell probes): with all five held down after a completed bank, the ROM pulsed the reset coil {NELL['save-nell']['reset_15_pulses_after_bank_1_with_the_targets_held_down']} "
            "times; a recreation should raise the bank on each pulse and expect the ROM to retry while a switch stays closed."
        ),
        "positions": [
            {"id": f"mechanism.drop-targets.{sem.SWITCHES[a][0].removeprefix('drop-target-')}", "label": sem.SWITCHES[a][1], "sensors": [f"switch.{sem.SWITCHES[a][0]}"]}
            for a in range(17, 22)
        ],
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.turbo-bumpers",
        "label": "Turbo Bumpers",
        "kind": "other",
        "actuators": ["coil.left-turbo-bumper", "coil.center-turbo-bumper", "coil.right-turbo-bumper"],
        "sensors": ["switch.left-turbo-bumper", "switch.center-turbo-bumper", "switch.right-turbo-bumper"],
        "assembly_part_number": asm("6"),
        "behavior": (
            f"Three Turbo Bumper Assys ({asm('6')}) sensed at 44-46 (part 180-5015-00) and fired by switched solenoids 17-19 (23-800). The center bumper is the lower one between "
            "the other two. ROM evidence (3.20, a game in play): closing 44, 45 and 46 fires 17, 18 and 19, and the ROM names them LEFT, CENTER and RIGHT."
        ),
        "positions": [
            {"id": "mechanism.turbo-bumpers.left", "label": "Left Turbo Bumper", "sensors": ["switch.left-turbo-bumper"]},
            {"id": "mechanism.turbo-bumpers.center", "label": "Center (Lower) Turbo Bumper", "sensors": ["switch.center-turbo-bumper"]},
            {"id": "mechanism.turbo-bumpers.right", "label": "Right (Upper Right) Turbo Bumper", "sensors": ["switch.right-turbo-bumper"]},
        ],
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.slingshots",
        "label": "Slingshots",
        "kind": "other",
        "actuators": ["coil.left-slingshot", "coil.right-slingshot"],
        "sensors": ["switch.left-slingshot", "switch.right-slingshot"],
        "assembly_part_number": asm("5"),
        "behavior": (
            f"Two Sling Shot Assys ({asm('5')}) sensed at 30 and 38 (part 180-5054-00) and fired by switched solenoids 20 and 21 (23-800). ROM evidence (3.20, a game in play): "
            "closing 30 fires 20 and closing 38 fires 21."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.bomb-targets",
        "label": "BOMB Stand-Up Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.bomb-target-b-first", "switch.bomb-target-o", "switch.bomb-target-m", "switch.bomb-target-b-last"],
        "behavior": (
            "Four small stand-up targets 25-28 (printed '\"B\"', '\"O\"', '\"M\"', '\"B\"' Stand-Up Target) spelling BOMB, each with its lamp 25-28. No reset coil: they are "
            "stand-ups. Adjustment 48 (Spot Bomb Style) sets how the ramps spot them."
        ),
        "provenance": prov("validated", [MANUAL]),
    },
    {
        "id": "mechanism.hat-targets",
        "label": "Hat Targets (3 Bank Standup)",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.hat-target-22", "switch.hat-target-middle", "switch.hat-target-24"],
        "assembly_part_number": asm("8"),
        "behavior": (
            f"The 3 Bank Standup ({asm('8')}) stacks three stand-up targets (500-5640-36) on the left of the playfield, with lamps 57-59 and Hat Trick 60. ROM evidence (3.20 "
            "hat-target probes): closing 22 changes only lamp 57 (Top Hat Target) and 23 only lamp 58 (Middle Hat Target); 24, hit last, completes the set, changing 57-59 and "
            "lighting Hat Trick 60. Which physical target is 22 and which is 24 is conflicted (see hat-target-switch-order)."
        ),
        "provenance": prov("conflicted", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.backbox-hat-trick",
        "label": "Backbox Hat Trick Figures",
        "kind": "toy",
        "actuators": ["coil.hat-trick-lion", "coil.hat-trick-rocky", "coil.hat-trick-rhino"],
        "sensors": [],
        "behavior": (
            "IPDB describes a mechanical backbox animation in which Bullwinkle pulls Rocky, a rhino or a lion out of his hat; the coils on drives 3 (Lion), 6 (Rocky) and 7 (Rhino) "
            "sit in the backbox. The Game Specific Features page: shooting the left orbit into the hole while Hat Trick is lit lets Bullwinkle pull an animal out of his hat; "
            "Rocky lights Extra Ball, Rhino starts the Rhino Bonus countdown and Lion starts the Jackpot. ROM evidence (3.20 Hat Trick probes): about "
            f"{_first['hat_coil_first_on_after_34_closed_s']} s after the left orbit top switch 34 closed, the ROM energised one figure coil; on the first award of a figure it "
            f"held the coil {_first['hat_coil_on_s'][0]} s, then switched it on again for {_first['hat_coil_on_s'][1]} s starting just before the VUK fired, and a repeated "
            f"award of the same figure held it once for {_repeat['hat_coil_on_s'][0]} s. Awards 1 and 2 used the Lion (Jackpot lamp 54 flashing afterwards), awards 3 and 4 "
            "the Rhino (Rhino Bonus lamp 61); Rocky was not awarded. The figures' physical motion, travel and return are not documented in any retained source; the retained "
            "table animates a figure up while its coil is on and down when it turns off."
        ),
        "provenance": prov("candidate", MECH_REFS + [IPDB, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.save-nell",
        "label": "Save Nell (Nell's Log and Saw)",
        "kind": "motorized",
        "actuators": ["motor.saw"],
        "sensors": [],
        "assembly_part_number": asm("14"),
        "behavior": (
            f"Nell's Log Assembly ({asm('14')}, beside the drop-target bank) is a motor driving a saw disc through an O-ring belt and a gear rack under a log carrier; the "
            "Relay Board 520-5010-00 switches 28 VAC to the motor while solenoid 9 is on. No switch reports its position, and how the carrier returns is not legible on the assembly drawing. "
            "The Game Specific Features page: completing the drop targets advances a value 5-4-3-2-1, the Nell timer starts when all lamps flash, and hitting drop targets saves "
            "Nell before time expires; Adjustment 51 (Any Drop Wins Nell) chooses between any drop target and the whole bank. ROM evidence (3.20 Save Nell probes): the ROM switched "
            f"9 on {NELL['save-nell']['relay_9_on_after_bank_2_completed_s']} s after the second completed bank (not after the first) and held it {NELL['save-nell']['relay_9_on_s']} s "
            f"until a drop-target hit saved Nell (dropping it {NELL['save-nell']['relay_9_off_after_the_save_hit_s']} s after the hit), and {NELL['nell-expires']['relay_9_on_s']} s "
            "when nothing was hit. The two retained recreation lineages disagree on the travel: one swings the log back and forth while 9 is on and stops it in place when 9 turns "
            "off, the other moves it one way while 9 is on and back when 9 turns off."
        ),
        "provenance": prov("candidate", MECH_REFS + [CORPUS_INDEPENDENT, RUNTIME_SRC]),
    },
]
relationships = [
    {
        "id": f"relationship.left-right-relay-{drive}",
        "kind": "relay_gated",
        "source": "relay.left-right-relay",
        "destination": f"flasher.{drive}r",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC]),
    }
    for drive in range(1, 9)
] + flipper_column_relationships(
    flip_swno=FLIP_SWNO, matrix_ids={15: "switch.left-flipper-copy", 16: "switch.right-flipper-copy"}, refs=(CORE_C, CORE_H),
)

conflicts = [
    {
        "id": "hat-target-switch-order",
        "path": "inputs[id=switch.hat-target-22]; inputs[id=switch.hat-target-24]",
        "description": (
            "The manual's switch-matrix chart and Switch Part Numbers table print 22 'Hat Target Bottom' and 24 'Hat Target Top', and its switch-location drawing reads the three "
            "stacked hat-target callouts top to bottom as 24, 23, 22 (the second digit of the top callout hidden under a leader line). The ROM's Active Switch Test names 22 "
            "'TOP HAT TARGET' and 24 'BOTTOM HAT TARGET' with the same wires (WHT-BLU and WHT-GRY returns), the game lights the Top Hat Target lamp 57 when 22 closes, and the "
            "retained table pulses 22 from its top target and 24 from its bottom one. A recreation consumes the answer as the physical position of each switch. Labels follow "
            "the ROM and the placements follow the table, both marked conflicted. Resolution path: on a physical machine, hit the top hat target in the Active Switch Test and "
            "read the switch number, or trace the WHT-BLU row-6 return (CN10-3) to the target it reaches."
        ),
        "source_refs": [MANUAL, RUNTIME_SRC, SCRIPT_REF],
        "status": "unresolved",
    },
]

# --- Drivers --------------------------------------------------------------------------------------------------------------
_root = ROM_SETS[ROOT_DRIVER]
drivers = []
for driver_id in sorted(ROM_SETS):
    roms = ROM_SETS[driver_id]
    if driver_id == ROOT_DRIVER:
        note = (
            "Clone-tree root and the latest firmware pinned PinMAME carries (3.20, display ROM rbdspa.300). Every rab_ set shares one game-data block (INITGAMES11(rab, "
            "GEN_DEDMD32, de_128x32DMD, FLIP1516, SNDBRD_DE2S, SNDBRD_DEDMD32, S11_PRINTERLINE), muxSol 10) and the three sound ROMs, so all five present identical playfield "
            "hardware and identical public addresses. The retained known-working table runs it (cGameName rab_320, script line 126, with rab_130 kept as a commented alternative) "
            "and every harness run used it; its Display Version screen reads BULLWINKLE A3.00 and 5/24/1993."
        )
    else:
        differing = [(role, mine) for role, mine, theirs in zip(ROLES, roms, _root) if mine != theirs]
        note = ("Differs from the root in " + ", ".join(f"the {role} ROM ({rom})" for role, rom in differing) + ".") if differing else "Byte-identical ROM set to the root."
        note += " The shared game data means the address model is unchanged."
        if driver_id == "rab_110be":
            note += (
                " Labelled Belgian: a regional firmware for the same hardware. PinMAME's comment says the Belgian CPU ROM came in one dump with an Italian display ROM that was "
                "probably not meant to be used with it, so the set pairs it with the 1.30 display ROM."
            )
        if driver_id == "rab_103it":
            note += " Labelled Italian: a language firmware for the same hardware. PinMAME's comment says the CPU ROM is taken from the Spanish 1.03 dump."
        if driver_id == "rab_103":
            note += " Labelled Spanish: a language firmware for the same hardware, and the earliest revision PinMAME carries."
        if driver_id == "rab_130":
            note += " An earlier factory revision."
    drivers.append({
        "id": driver_id,
        "description": DRIVER_LABELS[driver_id],
        "year": "1993",
        "manufacturer": "Data East",
        "flags": 0,
        "physical_compatibility": "identical",
        "variant_notes": note,
        **({} if driver_id == ROOT_DRIVER else {"clone_of": ROOT_DRIVER}),
    })
for _driver in drivers:
    for _role, _mine, _theirs in zip(ROLES, ROM_SETS[_driver["id"]], _root):
        if _mine != _theirs and _mine not in _driver["variant_notes"]:
            raise SystemExit(f"{_driver['id']}: {_role} ROM {_mine} differs from the root but the note omits it")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def excerpt_record(name: str, locator: str, **extra) -> dict:
    record = {
        "id": f"excerpt.rocky-and-bullwinkle.{name.rsplit('.', 1)[0]}",
        "locator": locator,
        "path": f"evidence/excerpts/{KEY}/{name}",
        "sha256": file_sha256(EXCERPT_DIR / name),
    }
    record.update(extra)
    return record


CHECKED = {
    "method": "manual",
    "transcribed_by": "curator, read from native-resolution (300 dpi) renders of the image-only scan; OCR was used only to find pages",
    "reviewed": True,
}
EXCERPTS_MANUAL = [
    excerpt_record(
        "switch-matrix.md",
        "printed pages 24-25 (PDF 28-29), Switch Matrix Chart, the complete Switch Part Numbers table and the Switch Locations drawing", **CHECKED,
    ),
    excerpt_record(
        "lamp-matrix.md",
        "printed pages 26-27 (PDF 30-31), Lamp Matrix Chart, Lamp Matrix No. and Description and the Lamp Locations drawing", **CHECKED,
    ),
    excerpt_record(
        "coil-drivers.md",
        "printed pages 28, 29, 46 and 47 (PDF 32, 33, 51-52 and 53-54), the coil text, CPU Controlled Auxiliary Solenoids, Flipper Solenoids, the coil chart schematic, the "
        "Playfield Coil / Flash Lamp Wiring Diagram, the Playfield Special Coil Diagram and the coil and flash-lamp location drawings", **CHECKED,
    ),
    excerpt_record(
        "assemblies-and-features.md",
        "printed pages 4, 20, 31 and 66 (PDF 8, 24, 35, 91 and 92), Game Specific Features, Adjustments 47-52, Playfield - Major Assemblies and the Nell Log Assembly drawing",
        **CHECKED,
    ),
]


def pin_source(identifier: str, filename: str, locator: str) -> dict:
    return {
        "id": identifier, "kind": "pinmame_core",
        "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/{filename}",
        "revision": REVISION, "sha256": PIN_FILE_SHA256[filename], "locator": locator,
        "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
    }


def corpus_uri(name: str) -> str:
    return f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/{quote(name, safe='/')}"


sources = [
    {
        "id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": REVISION,
        "locator": "PinmameGetGames; src/wpc/degames.c lines 926-972 (rab_320 root, four clones)", "license": "BSD-3-Clause",
        "attribution": "PinMAME contributors",
    },
    pin_source(CORE, "degames.c", "lines 77-80 (INITGAMES11, muxSol 10), 85-89 (FLIP1516) and 926-972 (rab block, input_ports_rab, five drivers and ROM sets)"),
    pin_source(CORE_H, "core.h", "lines 159 (FLIP_SWNO) and 298-332 (output bands, CORE_FIRSTSSSOL 17, CORE_FIRSTSIMSOL 49, CORE_FIRSTCUSTSOL 51, CORE_FLIPPERSWCOL)"),
    pin_source(CORE_C, "core.c", "lines 1793-1870 (core_updateSw flipper copies and synthetic outputs) and 2456-2530 (core_getSol)"),
    pin_source(
        S11_C, "s11.c",
        "lines 371-372 and 727 (Jumper W7 on PIA2 PA7), 392-410 (pia2b_w printer lines), 537-650 (setSSSol, updsol, muxing, game-on), 875-883 (lamp and solenoid typing), "
        "1195-1203 (DataEast/Sega 3 output typing for rab_) and 1331 (MDRV_DIPS(1))",
    ),
    pin_source(S11_H, "s11.h", "lines 30-42 (DE_COMPORTS), 89-93 (S11_GAMEONSOL, DE_SWADVANCE, DE_SWUPDN) and 227 (S11_PRINTERLINE)"),
    {
        "id": MANUAL, "kind": "manual",
        "uri": MANUAL_URL,
        "locator": (
            f"{MANUAL_NAME}; printed pages 4, 20, 24-29, 31, 46, 47 and 66 (PDF 8, 24, 28-33, 35, 51-54 and 91-92); IPDB-hosted scan of Data East Pinball's 1993 manual, "
            "106 pages, image-only, retrieved through a Wayback capture of IPDB's file URL"
        ),
        "sha256": MANUAL_SHA256, "original_filename": MANUAL_NAME,
        "acquired_at": MANUAL_ACQUIRED,
        "excerpts": EXCERPTS_MANUAL,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Data East Pinball, Inc.; hosted by the Internet Pinball Machine Database",
    },
    {
        "id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=23",
        "locator": (
            "IPDB machine #23, 'The Adventures of Rocky and Bullwinkle and Friends' (Data East Pinball), date of manufacture February 01, 1993 (production February 1 to "
            "April 23, 1993), model number 500-5522-01, MPU DataEast/Sega Version 3, 5,500 units; design Tim Seckel, art Kevin O'Connor, mechanics Norm Wurz; a mechanical "
            f"backbox animation in which Bullwinkle pulls Rocky, a rhino or a lion out of his hat. Retained Wayback capture {IPDB_CAPTURE}. Identity cross-checked against the "
            "manual's title, the PinMAME driver description and the retained script's header (ipdb.org machine id 23)."
        ),
        "sha256": IPDB_SHA256, "acquired_at": IPDB_ACQUIRED,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
    },
    {
        "id": RUNTIME_SRC, "kind": "runtime_scenario",
        "uri": "internal:" + RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix(),
        "locator": FACTS["source_locator"],
        "revision": REVISION, "sha256": file_sha256(RUNTIME_EVIDENCE_PATH),
        "license": "NOASSERTION", "attribution": "Curator; user-authorized local ROM copies, ROM bytes are not redistributed",
    },
    {
        "id": TABLE, "kind": "vpx_table",
        "uri": f"external:pinmame-vpx-sources/{SOURCE_DIRECTORY}/source/{TABLE_NAME}",
        "original_filename": TABLE_NAME,
        "locator": (
            "Retained known-working recreation by cyberpez, 1.0 (85,962,752 bytes; the file name spells 'Fiends'); playfield 952 x 2162; runs cGameName rab_320. Geometry "
            "authority for named script-bound objects only; normalized coordinates are x/952 and y/2162. A lamp or flash lamp is placed only on a script-bound bulb: a Light "
            "that is a bulb Light and draws its bulb mesh (none in this table does), or a modelled bulb primitive the script fades with the lamp. Primitives are placed at "
            f"the centre of their world-space mesh bounds from a {VPXTOOL_VERSION} 'export obj --units vpu' export (SHA-256 {WORLD_OBJ_SHA256}, retained under the review "
            "artifacts root)."
        ),
        "sha256": TABLE_SHA256, "known_working": True, "acquired_at": TABLE_ACQUIRED,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "cyberpez",
    },
    {
        "id": SCRIPT_REF, "kind": "vpx_script",
        "uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE_PATH.as_posix()}/script.vbs",
        "original_filename": "script.vbs",
        "locator": (
            "Embedded script of the retained table (header 'Created by: cyberpez', ipdb.org machine id 23): cGameName = \"rab_320\" (line 126), LoadVPM \"01560000\", \"DE.VBS\", "
            "3.1 (line 153), HandleMechanics 0 and HandleKeyboard 0 (lines 225-226), SolCallback map (lines 161-192), key handling (lines 351-374), mechanism subs (lines "
            "1225-1423, 1795-1980, 2256-2265 and 2549-2698), target, bumper and slingshot handlers (lines 2333-2470). It differs from the sidecar script shipped beside the "
            "table; the embedded copy is the one cited."
        ),
        "sha256": SCRIPT_SHA256, "known_working": True, "acquired_at": EXTRACTION_ACQUIRED,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "cyberpez",
    },
    {
        "id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI,
        "original_filename": "de.vbs", "sha256": VPM_DE_SHA256, "acquired_at": "2026-09-25T23:32:01Z",
        "locator": (
            "The VPinMAME script library the retained table loads at runtime (script.vbs line 153 LoadVPM \"01560000\", \"DE.VBS\", 3.1; de.vbs executes core.vbs), retained from "
            f"the contributor's working installation together with core.vbs (SHA-256 {VPM_CORE_SHA256}). de.vbs defines swLRFlip = 82 and swLLFlip = 84 and sets them from the "
            "flipper keys in vpmKeyDown/vpmKeyUp, and names the staged upper flipper keys swURFlip/swULFlip at 86 and 88."
        ),
        "license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
        "excerpts": [excerpt_record(
            "vpm-script-library-flippers.md",
            "de.vbs lines 21-36 and 62-111; core.vbs lines 2090, 2854-2855 and 2862-2865; script.vbs lines 1, 126-127, 153, 161-162, 225-226, 351-374 and 1405-1423",
            **{**CHECKED, "transcribed_by": "curator, read from the script files"},
        )],
    },
    {
        "id": EXTRACTION, "kind": "vpx_table",
        "uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}",
        "locator": (
            "Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
            f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with {VPXTOOL_VERSION} from the "
            "retained table. Bounds are 952 x 2162."
        ),
        "sha256": EXTRACTION_MANIFEST_SHA256, "acquired_at": EXTRACTION_ACQUIRED,
        "license": "NOASSERTION", "attribution": "vpxtool extraction",
    },
    {
        "id": CORPUS_SAME_LINEAGE, "kind": "vpx_script",
        "uri": corpus_uri(CORPUS_SAME_LINEAGE_NAME), "revision": VPXTABLE_SCRIPTS_REVISION, "sha256": CORPUS_SAME_LINEAGE_SHA256,
        "locator": (
            f"{CORPUS_SAME_LINEAGE_NAME} (183,650 bytes), a later release of the retained table's lineage: cGameName = \"rab_320\" (line 157, rab_130 commented at 158), "
            "LoadVPM \"DE.VBS\" 3.1 (line 243), the same solenoid map (lines 249-279) and the same bumper switch assignment (Bumper1/2/3_hit pulse 44/45/46, lines 2489-2491). "
            "Same lineage, so it corroborates the bindings but is not independent evidence. Script only; its table is not retained."
        ),
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "cyberpez, with later changes by TastyWasps, passion4pins and others credited in the header; corpus by sverrewl",
    },
    {
        "id": CORPUS_INDEPENDENT, "kind": "vpx_script",
        "uri": corpus_uri(CORPUS_INDEPENDENT_NAME), "revision": VPXTABLE_SCRIPTS_REVISION, "sha256": CORPUS_INDEPENDENT_SHA256,
        "locator": (
            f"{CORPUS_INDEPENDENT_NAME} (49,466 bytes), an independent lineage ('FS Ver. 0.96', Zedonius 27/05/2017, crediting Javier15): cGameName = \"rab_320\" (line 58), "
            "LoadVPM \"DE.VBS\" 3.38 (line 79) and the same addresses bound with different code (SolCallbacks lines 100-127); its SolNell moves the log one way while 9 is on "
            "and back when it turns off (lines 232-250). Script only; its table is not retained and none of its geometry is used."
        ),
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Javier15 and Zedonius; corpus by sverrewl",
    },
]

# --- Coverage ---------------------------------------------------------------------------------------------------------------
# Every requirement whose evidence is not complete, each with the device or record that keeps it open:
# input_semantics, Jumper W7 whose meaning no retained source states, and the hat-target identity of 22 and 24;
# output_semantics, CN3 printer lines 37-44, which no retained run or page assigns;
# mechanism_behavior, the travel of Nell's log and the backbox Hat Trick figures' motion;
# polarity, the Green Up/Down button (-6);
# spatial_placement, every placement observed from one recreation lineage, with the lamps, G.I., knocker and 2R/7R unplaced;
# unresolved_conflicts, hat-target-switch-order.
MISSING = ["input_semantics", "output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"]
DIMENSIONS = {
    "catalog_identity": "validated",
    "address_enumeration": "validated",
    "semantic_naming": "observed",
    "physical_wiring": "observed",
    "mechanisms": "observed",
    "variant_coverage": "validated",
    "recreation_knowledge": "validated",
    "runtime_observation": "observed",
    "causal_exercise": "observed",
    "spatial_placement": "observed",
}

definition = {
    "format": "pinmame-machine-definition",
    "schema_version": 2,
    "machine": {
        "id": KEY,
        "name": "Adventures of Rocky and Bullwinkle and Friends",
        "manufacturer": "Data East",
        "year": 1993,
        "kind": "physical_pinball",
        "model_number": "500-5522-01",
        "ipdb_id": 23,
        "opdb_id": "G5vnL-MJP3y",
        "playfield": {
            "width": PLACES["table_bounds"]["width"], "height": PLACES["table_bounds"]["height"], "units": "vpx",
            "provenance": prov("observed", [TABLE]),
        },
    },
    "controller": {"platform": "pinmame.dataeast", "hardware_generation": "0x4000", "inversion_applied_by_emulator": True},
    "coverage": {"status": "partial", "dimensions": DIMENSIONS, "missing": MISSING},
    "drivers": drivers,
    "inputs": inputs,
    "outputs": outputs,
    "displays": displays,
    "mechanisms": mechanisms,
    "relationships": relationships,
    "conflicts": conflicts,
    "sources": sources,
    "knowledge": {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"},
}
_identifiers = [device["id"] for device in inputs + outputs]
_duplicates = sorted({identifier for identifier in _identifiers if _identifiers.count(identifier) > 1})
if _duplicates:
    raise SystemExit(f"device identifiers are not unique: {_duplicates}")
_known = set(_identifiers)
for _mechanism in mechanisms:
    for _ref in _mechanism["actuators"] + _mechanism["sensors"]:
        if _ref not in _known:
            raise SystemExit(f"{_mechanism['id']} names an unknown device {_ref}")

# --- Spatial report -----------------------------------------------------------------------------------------------------------
PROJECTIONS = {
    ("pinmame.output.solenoid", 15): (
        "The drop-target reset coil is projected onto the middle drop target t19, where the retained table plays its reset sound; the table models no coil."
    ),
}


def build_spatial_report(document: dict[str, Any]) -> dict[str, Any]:
    located_inputs: list[int] = []
    observed_inputs: list[int] = []
    conflicted_inputs: list[int] = []
    unplaced_inputs: list[int] = []
    not_applicable_inputs: dict[str, list[int]] = {}
    placement_count = 0
    for device in document["inputs"]:
        spatial = device.get("spatial")
        address = int(device["binding"]["device"])
        if spatial is None:
            unplaced_inputs.append(address)
            continue
        if spatial["status"] == "not_applicable":
            not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
            continue
        placement_count += len(spatial["placements"])
        {"observed": observed_inputs, "conflicted": conflicted_inputs}.get(spatial["status"], located_inputs).append(address)
    located_outputs: list[dict[str, Any]] = []
    observed_outputs: list[dict[str, Any]] = []
    unplaced_outputs: list[dict[str, Any]] = []
    not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
    for device in document["outputs"]:
        binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
        spatial = device.get("spatial")
        if spatial is None:
            unplaced_outputs.append(binding)
            continue
        if spatial["status"] == "not_applicable":
            not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
            continue
        placement_count += len(spatial["placements"])
        (observed_outputs if spatial["status"] == "observed" else located_outputs).append(binding)
    order = lambda item: (item["group"], item["address"])  # noqa: E731
    return {
        "format": "pinmame-spatial-blockers",
        "version": 1,
        "machine_id": document["machine"]["id"],
        "status": "observed",
        "blockers": [
            "Every placement comes from one community table (cyberpez's 1.0) and none was checked against the manual's switch, lamp or coil location drawings, so all of them "
            "stay observed. Promotion needs a callout check of those drawings or a second, independent table lineage.",
            "Hat targets 22 and 24 are placed on the retained table's top and bottom targets but stay conflicted: the manual prints 22 at the bottom and 24 at the top, the ROM "
            "the other way round (conflict hat-target-switch-order).",
            "The 62 playfield lamps have no coordinate: the retained script binds only insert overlays, primitives and sprites to them, the raised bulbs it fades for 16 and 53 "
            "are bound crossed against the manual's chart and the ROM's names, and the lamp-location drawing was not used for placement.",
            "Flash lamps 1R (25), 4R (28), 6R (30) and 8R (32) have no coordinate: the script fades only bulb-mode Lights that draw no bulb (show_bulb_mesh false) and sit on "
            "no modelled bulb, plus insert overlays and sprites. 2R (26) and 7R (31) have none either: the script binds only insert-overlay Lights to them.",
            "Flash lamps 3R (27) and 5R (29) are placed on the three bulbs the table models as primitives, one and two of the four bulbs the schematic counts outside the "
            "backbox for each group; the rest of their bulbs have no coordinate.",
            "The G.I. relay 11 has no coordinate: its fade drives 84 bulb-mode Lights of which only gi5a and gi6a draw a bulb, and no retained page counts or locates the "
            "G.I. bulbs, so no G.I. emitter survey was made.",
            "The knocker 8 has no coordinate: page 28's coil location drawing carries no 8L balloon and no other retained page locates it.",
            "The drop-target reset coil 15 is a projection onto the middle drop target.",
        ],
        "coordinate_convention": {
            "space": "playfield",
            "source_bounds": {"left": 0.0, "top": 0.0, "right": PLACES["table_bounds"]["width"], "bottom": PLACES["table_bounds"]["height"]},
            "x": "x/952; 0=left, 1=right",
            "y": "y/2162; 0=rear/backglass, 1=apron/player",
        },
        "extraction": {
            "fail_closed": True,
            "file_count": EXTRACTION_FILE_COUNT,
            "manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
            "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
            "manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}",
            "source_ref": EXTRACTION,
            "total_bytes": EXTRACTION_TOTAL_BYTES,
            "vpxtool_version": VPXTOOL_VERSION,
        },
        "source_hashes": {
            "embedded_script_sha256": SCRIPT_SHA256,
            "manual_sha256": MANUAL_SHA256,
            "table_sha256": TABLE_SHA256,
            "world_obj_sha256": WORLD_OBJ_SHA256,
        },
        "world_space_export": {
            "command": "vpxtool export obj --units vpu <retained VPX>",
            "sha256": WORLD_OBJ_SHA256,
            "uri": WORLD_OBJ_URI,
            "use": "x/y mesh bounds of every placed primitive, embedded in tools/build_rab_places.py and re-derived by its --world-obj check",
        },
        "placement_count": placement_count,
        "resolved_input_addresses": sorted(located_inputs),
        "observed_input_addresses": sorted(observed_inputs),
        "conflicted_input_addresses": sorted(conflicted_inputs),
        "unplaced_input_addresses": sorted(unplaced_inputs),
        "resolved_output_bindings": sorted(located_outputs, key=order),
        "observed_output_bindings": sorted(observed_outputs, key=order),
        "unplaced_output_bindings": sorted(unplaced_outputs, key=order),
        "not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
        "not_applicable_outputs": {reason: sorted(bindings, key=order) for reason, bindings in sorted(not_applicable_outputs.items())},
        "projections": [{"group": group, "address": address, "reason": reason} for (group, address), reason in sorted(PROJECTIONS.items())],
        "coordinate_origins": {
            "computed_centroids": ["Wall LeftSlingShot (switch 30, solenoid 20)", "Wall RightSlingShot (switch 38, solenoid 21)"],
            "mesh_bounds_centres": sorted(
                f"Primitive {hit['object']} ({key.replace('.', ' ')})"
                for key, hits in PLACES["placements"].items() for hit in hits if hit["coordinate_origin"] == "mesh-bounds-center"
            ),
            "object_centers": "every other placement uses its retained object's own stored center (Light, Kicker, Trigger, Bumper, Gate) or position (HitTarget)",
        },
        "excluded_object_classes": [
            "Bulb-mode Lights that draw no bulb (show_bulb_mesh false) and sit on no modelled bulb, bound to flash lamps 1R, 3R, 4R, 5R, 6R and 8R: a light that sits on no "
            "bulb makes no socket.",
            "Insert-overlay Lights (is_bulb_light false), insert primitives and Flasher sprites bound to lamps or flash lamps: they paint an insert or a glow and are not sockets.",
            "The raised ramp-entrance bulbs pRbulb and pWBbulb: modelled bulbs, but bound to lamps 16 and 53 crossed against the chart and the ROM.",
            "The 84 G.I. Lights, of which only gi5a and gi6a draw a bulb; no source counts the G.I. sockets.",
            "Bulb Lights the script never binds to a lamp, such as the l1-l14 Lights on the spin-and-win surface.",
            "The manual's switch, lamp and coil location drawings: read and transcribed, but not used for any coordinate.",
        ],
        "unresolved": PLACES.get("unplaced", []),
    }


def render_spatial_report(report: dict[str, Any]) -> str:
    lines = [
        "# The Adventures of Rocky and Bullwinkle and Friends (Data East, 1993) spatial review",
        "",
        f"Status: {report['status']}. Every playfield switch and every coil or flash-lamp group the retained table models with a script-bound object is placed from that "
        "table; cabinet, backbox, virtual and unused addresses carry a controlled `not_applicable` record. The playfield lamps, the G.I., the knocker and flash lamps 1R, 2R, 4R, "
        "6R, 7R and 8R have no coordinate. No placement was checked against the manual's location drawings, so every placement stays `observed` (hat targets 22 and 24 `conflicted`) and the "
        f"record stays at `machines/partial/data-east/{SLUG}.json`.",
        "",
        f"The geometry source is the retained known-working `{TABLE_NAME}` (SHA-256 `{TABLE_SHA256}`); its embedded script (SHA-256 `{SCRIPT_SHA256}`) is the runtime binding "
        "authority. Exact playfield bounds are 952 x 2162; every table coordinate is x/952 and y/2162 rounded to six places.",
        "",
        "## Evidence decisions",
        "",
        "- The embedded script is the runtime authority; the 1993 manual is the physical inventory, construction and wiring authority; the 3.20 ROM's own service tests settle "
        "names and switch-to-coil pairs; pinned PinMAME owns controller topology; the retained table supplies geometry for script-bound objects only.",
        "- A lamp or flash lamp is placed only on a script-bound bulb: a Light that is a bulb Light and draws its bulb mesh, or a modelled bulb primitive the script fades "
        "with the lamp. Every flash-lamp Light in the table draws no bulb, so only 3R and 5R, which the table models with three upright bulb primitives, are placed; no "
        "playfield lamp is placed.",
        f"- Primitives are placed at the centre of their world-space mesh bounds from the retained `vpxtool export obj --units vpu` export (SHA-256 `{WORLD_OBJ_SHA256}`), "
        "never at their stored positions; the diverters' stored positions are their pivots.",
        "- The retained table pulses 45 from its upper right bumper and 46 from its lower one; the manual's drawing and the ROM's names put 46 on the upper right and 45 on the "
        "lower, center bumper, so 45 is placed on Bumper3 and 46 on Bumper2. That swap is a table defect, recorded on the devices.",
        "- The backbox figure coils 3, 6 and 7 and the Left/Right relay 10 are cabinet or backbox devices; flash-lamp bulbs in the backbox insert are not placed.",
        "",
        "## Blockers",
        "",
    ]
    lines += [f"- {blocker}" for blocker in report["blockers"]]
    lines += ["", "## Explicit projections", ""]
    lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
    lines += [
        "",
        "## Counts",
        "",
        f"- Placements: {report['placement_count']}",
        f"- Validated input addresses: {len(report['resolved_input_addresses'])}",
        f"- Observed-only input addresses: {len(report['observed_input_addresses'])}",
        f"- Conflicted input addresses: {len(report['conflicted_input_addresses'])}",
        f"- Validated output bindings: {len(report['resolved_output_bindings'])}",
        f"- Observed-only output bindings: {len(report['observed_output_bindings'])}",
        f"- Output bindings with no coordinate: {len(report['unplaced_output_bindings'])}",
    ]
    lines += [f"- Inputs with a controlled `{reason}` record: {len(addresses)}" for reason, addresses in report["not_applicable_inputs"].items()]
    lines += [f"- Outputs with a controlled `{reason}` record: {len(bindings)}" for reason, bindings in report["not_applicable_outputs"].items()]
    lines += [
        "",
        "## Promotion decision",
        "",
        "Refused. `coverage.missing` lists `spatial_placement` because every coordinate rests on one community table without a drawing check and the lamps, the G.I., the "
        "knocker, six of the eight flash-lamp groups and most bulbs of the other two are not placed; the hat-target conflict and the other open requirements keep the record "
        "partial as well.",
        "",
        "## Retained evidence",
        "",
        f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
        f"- World-space export `{WORLD_OBJ_URI}`, SHA-256 `{WORLD_OBJ_SHA256}`.",
        f"- Manual SHA-256 `{MANUAL_SHA256}`.",
        "",
    ]
    return "\n".join(lines)


SPATIAL_REPORT = build_spatial_report(definition)

# --- Knowledge note -------------------------------------------------------------------------------------------------------------
KNOWLEDGE_TEXT = KNOWLEDGE_TEMPLATE.read_bytes().decode("utf-8")
knowledge_note = KNOWLEDGE_TEXT.replace("{driver_count}", str(len(drivers))).replace("{placed}", str(SPATIAL_REPORT["placement_count"]))
if "{" in re.sub(r"`[^`]*`", "", knowledge_note):
    raise SystemExit("the knowledge template still carries an unfilled placeholder")


def build() -> dict:
    """Return the canonical definition assembled from the embedded literals."""
    return definition


# --- Retained extraction ---------------------------------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
    if not extraction_root.is_dir():
        raise RuntimeError(f"The Adventures of Rocky and Bullwinkle retained extraction is missing: {extraction_root}")
    paths = sorted(
        (path for path in extraction_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(extraction_root).as_posix(),
    )
    return {
        "format": "pinmame-vpx-extraction-manifest",
        "version": 1,
        "files": [
            {"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": file_sha256(path)}
            for path in paths
        ],
    }


def configured_vpx_sources_root(*, required: bool) -> Path | None:
    value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if not value:
        if required:
            raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained The Adventures of Rocky and Bullwinkle extraction")
        return None
    return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
    extraction_root = source_root / EXTRACTION_RELATIVE_PATH
    manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
    if not manifest_path.is_file():
        raise RuntimeError(f"The Adventures of Rocky and Bullwinkle extraction manifest is missing: {manifest_path}")
    actual = load_json(manifest_path)
    expected = build_extraction_manifest(extraction_root)
    if canonical_bytes(actual) != canonical_bytes(expected):
        raise RuntimeError(f"The Adventures of Rocky and Bullwinkle extraction manifest does not match all files under {extraction_root}")
    files = actual["files"]
    identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
    if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
        raise RuntimeError(f"The Adventures of Rocky and Bullwinkle extraction identity mismatch: {identity}")
    script = extraction_root / "script.vbs"
    if file_sha256(script) != SCRIPT_SHA256:
        raise RuntimeError(f"The Adventures of Rocky and Bullwinkle embedded script is not the cited one: {script}")
    return actual


def write_extraction_manifest(source_root: Path) -> Path:
    manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
    write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
    return manifest_path


# --- Artifacts ---------------------------------------------------------------------------------------------------------------------
def _artifacts() -> tuple[tuple[Path, bytes], ...]:
    definition_bytes = canonical_bytes(definition)
    return (
        (DEFINITION_PATH, definition_bytes),
        (SEED_PATH, definition_bytes),
        (SPATIAL_REPORT_PATH, canonical_bytes(SPATIAL_REPORT)),
        (SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(SPATIAL_REPORT).encode("utf-8")),
        (KNOWLEDGE_PATH, knowledge_note.encode("utf-8")),
    )


def generate(root: Path = ROOT) -> Path:
    stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
    if stale.exists() and definition["coverage"]["status"] != "author_ready":
        raise RuntimeError(f"refusing to curate while an author-ready artifact exists (preserved): {stale}")
    for path, payload in _artifacts():
        target = root / path.relative_to(ROOT)
        if path.suffix == ".md":
            write_text(target, payload.decode("utf-8"))
        else:
            write_bytes(target, payload)
    return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
        raise RuntimeError("A stale The Adventures of Rocky and Bullwinkle author-ready definition is present")
    for path, expected in _artifacts():
        target = root / path.relative_to(ROOT)
        if not target.is_file():
            raise RuntimeError(f"The Adventures of Rocky and Bullwinkle artifact is missing: {target}")
        if target.read_bytes() != expected:
            raise RuntimeError(f"The Adventures of Rocky and Bullwinkle artifact drifted from its deterministic curator: {target}")
    report = load_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT))
    placements = sum(len(d.get("spatial", {}).get("placements", [])) for c in ("inputs", "outputs") for d in definition[c])
    if report.get("format") != "pinmame-spatial-blockers" or report.get("machine_id") != KEY or report.get("placement_count") != placements:
        raise RuntimeError("The Adventures of Rocky and Bullwinkle spatial report must be a blockers report naming this machine and its placement count")
    print("The Adventures of Rocky and Bullwinkle definition, seed, spatial report and knowledge note match the deterministic curator.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and the canonical artifacts")
    mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, spatial report and knowledge note")
    mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
    mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
    args = parser.parse_args()
    if args.write_extraction_manifest:
        root = configured_vpx_sources_root(required=True)
        assert root is not None
        print(f"The Adventures of Rocky and Bullwinkle extraction manifest written: {write_extraction_manifest(root)}")
    elif args.verify_extraction:
        root = configured_vpx_sources_root(required=True)
        assert root is not None
        verify_extraction_manifest(root)
        print("The Adventures of Rocky and Bullwinkle retained extraction matches its pinned manifest identity.")
    elif args.check:
        check(ROOT)
    else:
        print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
    main()
