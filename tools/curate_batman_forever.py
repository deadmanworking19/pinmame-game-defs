"""Deterministically curate Sega Batman Forever (1995), Data East 3b, from reviewed evidence.

The complete printed regions in evidence/excerpts are the tabular input; the ROM's own service-test
readings are pinned in tools/seeds and evidence/runtime; batman_forever_places.json holds recomputable
observed geometry. No external evidence is needed to regenerate. Optional evidence roots are verified
fail-closed when provided. A partial cannot overwrite an author-ready record.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes
from pinmame_game_defs.conflicts import unresolved_conflicts
import drawing_callouts
from pinmame_flipper_column import (
    flipper_column_inputs, flipper_column_relationships, vpm_staged_flipper_notes,
    VPM_DE_LIBRARY_SOURCE, VPM_DE_LIBRARY_URI, VPM_DE_SHA256,
)

ROOT = Path(__file__).resolve().parents[1]
KEY = "sega.batman-forever.1995"
SLUG = "batman-forever-1995"
REV = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
MANUAL = "manual.batman-forever.production"
CHART = "manual.batman-forever.tech-chart"
CORE = "pinmame.batman-forever.core"
SCRIPT = "vpx-script.batman-forever.1-3"
TABLE = "vpx-table.batman-forever.1-3"
EXTRACTION = "vpx-extraction.batman-forever.1-3"
RUNTIME = "runtime.batman-forever.batmanf"
GEOMETRY = "geometry.batman-forever.1-3"
CALLOUTS = "drawing-callouts.batman-forever.2026-10-23"
DEFINITION_PATH = ROOT / f"machines/partial/sega/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/sega/{SLUG}.json"
READINGS_PATH = ROOT / f"tools/seeds/sega/{SLUG}-runtime-readings.json"
RUNTIME_PATH = ROOT / "evidence/runtime/data-east/batman-forever-batmanf-service-tests.json"
KNOWLEDGE_PATH = ROOT / f"knowledge/sega/{SLUG}.md"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/sega/{SLUG}.json"
CALLOUT_SEED = ROOT / f"tools/seeds/sega/{SLUG}-callouts.json"
EXCERPTS = ROOT / "evidence/excerpts" / KEY
MISSING = ["input_semantics", "output_semantics", "spatial_placement"]
MANUAL_NAME = "Sega_1995_Batman_Forever_Manual_with_schematics_duplicate_pages_33_34_missing_pages_143_144.pdf"
CHART_NAME = "Sega_1995_Batman_Forever_Tech_Chart_switch_matrix_lamp_matrix_fuse_list_coil_list.pdf"
MANUALS = {
    MANUAL_NAME: ("e4ffe85699953dcaa7f1882eae8d0e3b4d01926d60039800965d62616d34d3d4", "20250908084329", "2026-10-23T18:46:17Z"),
    CHART_NAME: ("c8606a3d6c968f2ce04a028e38503430e76584ad3d614554a98517bf50c1fcc4", "20230406205120", "2026-10-23T18:46:19Z"),
}
UNUSED_SWITCHES = {9, 10, 17, 31}
CABINET_SWITCHES = {1, 2, 3, 4, 5, 6, 7, 8, 49, 63, 64}
UNUSED_LAMPS = {36, 37, 38, 60}
CABINET_LAMPS = {63, 64}
UNUSED_DRIVERS = {6, 13}
SWITCH_LABELS = (
    "Plumb Bob Tilt|4th Coin Slot|Start Button|Right Coin Slot|Center Coin Slot / DBA|Left Coin Slot|Slam Tilt|"
    "Extra Ball Buy-in / League Button|Unused 9|Unused 10|Trough Ball 1 Left|Trough Ball 2|Trough Ball 3|"
    "Trough Ball 4 Right|Trough VUK Opto|Shooter Lane|Unused 17|Drop Target C|Drop Target A|Drop Target V|"
    "Drop Target E|Top Lane B|Top Lane A|Top Lane T|Left Ramp Stand-up Left|Left Ramp Stand-up Right|"
    "VUK Stand-up|Right Ramp Stand-up Left|Right Ramp Stand-up Right|Batcave Exit Kicker|Unused 31|VUK|"
    "Laser Kick Left Outlane|Left Return Lane|Left Slingshot|Right Slingshot|Right Return Lane Inside|"
    "Right Return Lane Outside|Right Outlane|U-Turn Mini-Ramp|Top Eject|Top Good Heads Stand-up|"
    "Top Bad Heads Stand-up|Batwing Cannon Loaded|Batwing Cannon Safety|Batwing Cannon Home|Left Orbit|"
    "Right Orbit|Gun Trigger|Right Good Heads Stand-up|Right Bad Heads Stand-up|Left Ramp Enter|Left Ramp Exit|"
    "Middle Ramp Exit|Right Ramp Enter|Right Ramp Exit|Left Turbo Bumper|Bottom Turbo Bumper|Right Turbo Bumper|"
    "Batcave Lock 3 Top|Batcave Lock 2 Middle|Batcave Lock 1 Bottom|Left Flipper Button Matrix Copy|"
    "Right Flipper Button Matrix Copy"
).split("|")
LAMP_LABELS = (
    "Rooftop Chase|Question Marks Mode|Face Two-Face|Crime Spree|Brain Drain|Safe Trap|Lite Extra Ball|Forever|"
    "Top Lane B|Top Lane A|Top Lane T|Left Ramp Stand-up Left|Left Ramp Stand-up Right|VUK Stand-up|"
    "Right Ramp Stand-up Left|Right Ramp Stand-up Right|Riddler Throne|Drop Target C|Drop Target A|"
    "Drop Target V|Drop Target E|All Bat Signals Sighted|Good Heads Matched|Bad Heads Matched|Mr. E VUK|"
    "Bat Signal Left Orbit|Bat Signal Left Ramp|Bat Signal Middle Ramp|Bat Signal U-Turn|Bat Signal Right Ramp|"
    "Bat Signal Right Orbit|Bat Signal VUK|Spotlight Mid Ramp Left|Spotlight Mid Ramp Right|Super Jackpot U-Turn|"
    "Unused Lamp 36|Unused Lamp 37|Unused Lamp 38|Left Return Lane|Left Outlane Special|Top Good Heads|"
    "Top Bad Heads|Right Good Heads|Right Bad Heads|Laser Kick|Right Return Inside|Right Return Outside|"
    "Right Outlane Special|Arm Batwing|Jackpot Left Ramp|Double Jackpot|Crime Spree Right Ramp|"
    "Jackpot Right Ramp|Extra Ball U-Turn|Lock Arrow VUK|Gotham Event|Left Turbo Bumper|Bottom Turbo Bumper|"
    "Right Turbo Bumper|Unused Lamp 60|Batwing Cannon|The Bat Lives|Extra Ball Buy-in / League Button|Start Button"
).split("|")
# Number, label and kind of every fitted driver; flashers 25-32 are the PPB's right-side loads 1R-8R.
COILS = {
    1: ("Trough Ball Lockout", "coil"), 2: ("Trough Up-Kicker", "coil"), 3: ("Autolaunch", "coil"),
    4: ("VUK", "coil"), 5: ("Top Eject", "coil"), 7: ("4-Bank Drop Target Reset", "coil"),
    8: ("Knocker", "coil"), 9: ("Batcave Ball Lock", "coil"), 10: ("Left Right A-B Relay", "relay"),
    11: ("General Illumination Relay", "gi"), 12: ("Batwing Ramp Diverter", "coil"),
    14: ("Batwing Cannon Motor", "motor"), 15: ("Batwing Cannon Launch", "coil"), 16: ("Batcave Exit Kicker", "coil"),
    17: ("Left Turbo Bumper", "coil"), 18: ("Bottom Turbo Bumper", "coil"), 19: ("Right Turbo Bumper", "coil"),
    20: ("Left Slingshot", "coil"), 21: ("Right Slingshot", "coil"), 22: ("Laser Kick", "coil"),
    25: ("Flasher 1R 4-Bank and Left Inlane", "flasher"), 26: ("Flasher 2R Left Ramp", "flasher"),
    27: ("Flasher 3R Left Orbit", "flasher"), 28: ("Flasher 4R Top Left, Back Panel and Insert", "flasher"),
    29: ("Flasher 5R Left Ramp, Back Panel and Inserts", "flasher"),
    30: ("Flasher 6R Mini Ramp, Back Panel and Inserts", "flasher"),
    31: ("Flasher 7R Top Right, Back Panel and Insert", "flasher"),
    32: ("Flasher 8R Right 2-Bank, Right Inlane and Insert", "flasher"),
}
DRIVER_ROWS = (
    ("batmanf", "Batman Forever (4.0)", "1995"), ("batmanf1", "Batman Forever (1.02)", "1995"),
    ("batmanf2", "Batman Forever (2.02)", "1995"), ("batmanf3", "Batman Forever (3.0)", "1995"),
    ("batmanf5", "Batman Forever (5.0 unofficial MOD)", "2024"), ("batmanf501", "Batman Forever (5.01 unofficial MOD)", "2025"),
    ("bmf_at", "Batman Forever (4.0 Austrian)", "1995"), ("bmf_be", "Batman Forever (4.0 Belgian)", "1995"),
    ("bmf_ch", "Batman Forever (4.0 Swiss)", "1995"), ("bmf_cn", "Batman Forever (4.0 Canadian)", "1995"),
    ("bmf_de", "Batman Forever (4.0 German)", "1995"), ("bmf_fr", "Batman Forever (4.0 French)", "1995"),
    ("bmf_it", "Batman Forever (4.0 Italian, Display 4.01)", "1995"), ("bmf_it2", "Batman Forever (4.0 Italian, Display 4.0)", "1995"),
    ("bmf_it3", "Batman Forever (4.0 Italian, Display 4.0, Early sound)", "1995"), ("bmf_jp", "Batman Forever (4.0 Japanese)", "1995"),
    ("bmf_nl", "Batman Forever (4.0 Dutch)", "1995"), ("bmf_nl302", "Batman Forever (3.02 Dutch, Display 4.01)", "1995"),
    ("bmf_no", "Batman Forever (4.0 Norwegian)", "1995"), ("bmf_sp", "Batman Forever (4.0 Spanish)", "1995"),
    ("bmf_sv", "Batman Forever (4.0 Swedish)", "1995"), ("bmf_time", "Batman Forever (4.0 Timed Play)", "1995"),
    ("bmf_uk", "Batman Forever (4.0 English)", "1995"),
)
SW_DRIVE = [("Q55", "GRN-BRN", "CN8-1"), ("Q54", "GRN-RED", "CN8-2"), ("Q53", "GRN-ORG", "CN8-3"), ("Q52", "GRN-YEL", "CN8-4"),
            ("Q51", "GRN-BLK", "CN8-5"), ("Q50", "GRN-BLU", "CN8-7"), ("Q49", "GRN-VIO", "CN8-8"), ("Q48", "GRN-GRY", "CN8-9")]
SW_RETURN = [("WHT-BRN", "CN10-9"), ("WHT-RED", "CN10-8"), ("WHT-ORG", "CN10-7"), ("WHT-YEL", "CN10-6"),
             ("WHT-GRN", "CN10-5"), ("WHT-BLU", "CN10-3"), ("WHT-VIO", "CN10-2"), ("WHT-GRY", "CN10-1")]
LAMP_DRIVE = [("Q71", "YEL-BRN", "CN7-1"), ("Q70", "YEL-RED", "CN7-2"), ("Q69", "YEL-ORG", "CN7-3"), ("Q68", "YEL-BLK", "CN7-4"),
              ("Q67", "YEL-GRN", "CN7-5"), ("Q66", "YEL-BLU", "CN7-7"), ("Q65", "YEL-VIO", "CN7-8"), ("Q64", "YEL-GRY", "CN7-9")]
LAMP_RETURN = [("Q72", "RED-BRN", "CN6-1"), ("Q73", "RED-BLK", "CN6-2"), ("Q74", "RED-ORG", "CN6-3"), ("Q75", "RED-YEL", "CN6-5"),
               ("Q76", "RED-GRN", "CN6-6"), ("Q77", "RED-BLU", "CN6-7"), ("Q78", "RED-VIO", "CN6-8"), ("Q79", "RED-GRY", "CN6-9")]
BULB_PARTS = {"#555": "#555 wedge 165-5002-00", "#44": "#44 bayonet 165-5000-44"}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def prov(*refs, status="validated"): return {"status": status, "source_refs": list(dict.fromkeys(refs))}
def na(reason, *refs): return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}
def slug(text): return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
def aliases(group, n, manual=None):
    return [{"namespace": f"pinmame.{group}", "value": str(n)}] + ([] if manual is None else [{"namespace": "manual.address", "value": manual}])


def rows(filename, columns, first=r"\d+[LR]?"):
    """Parse only complete pipe rows of a declared width whose first cell is an address."""
    result = []
    for line in (EXCERPTS / filename).read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) == columns and re.fullmatch(first, cells[0]):
            result.append(cells)
    return result


def checked_excerpt(filename, locator):
    path = EXCERPTS / filename
    return {"id": slug(path.stem), "locator": locator, "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha(path), "method": "manual",
            "transcribed_by": "Curator; direct visual verification of retained native-resolution renders", "reviewed": True}


def readings():
    """The ROM's own SWITCH, LAMP and COIL TEST texts, pinned to frame digests in the readings seed."""
    seed = load_json(READINGS_PATH)
    found = {}
    for item in seed["readings"]:
        if item["group"] in ("switch", "lamp", "solenoid"):
            found.setdefault((item["group"], item["address"]), item)
    return found


def spatial(key, identifier, role, places, *refs):
    hits = places["placements"].get(key, [])
    if not hits:
        return None
    sources = refs or (TABLE, SCRIPT, GEOMETRY)
    return {"status": "observed", "placements": [
        {"id": f"{identifier}.{role}.{i}", "role": role, "space": "playfield", "x": h["x"], "y": h["y"],
         "provenance": prov(*sources, status="observed")} for i, h in enumerate(hits, 1)]}


def measured_spatial(identifier):
    """A device's placements measured on a factory location drawing, as candidates."""
    seed = load_json(CALLOUT_SEED)
    ids = sorted(pid for pid, item in seed["measurements"].items() if item["device"] == identifier)
    if not ids:
        raise ValueError(f"no drawing measurement for {identifier}")
    return {"status": "candidate", "placements": [
        {"id": pid, "role": "emitter", "space": "playfield", "x": drawing_callouts.measured(seed, pid)[0],
         "y": drawing_callouts.measured(seed, pid)[1], "provenance": prov(MANUAL, CALLOUTS, status="candidate")} for pid in ids]}


def switch_type(n, part):
    if n == 15:
        return "opto"
    if n in (1, 7):
        return "tilt"
    if n in (3, 8, 49, 63, 64):
        return "button"
    if part in ("180-5119-00", "180-5087-00", "180-5093-00", "180-5057-00"):
        return "microswitch"
    return "other"


def build():
    grid = {int(r[0]): r for r in rows("switches.md", 4)}
    lamp_grid = {int(r[0]): r for r in rows("lamps.md", 3)}
    lamp_names = {int(r[0]): r[1] for r in rows("lamps.md", 2)}
    coils = {r[0]: r for r in rows("coils.md", 10)}
    if set(grid) != set(range(1, 65)) or set(lamp_grid) != set(range(1, 65)) or set(lamp_names) != set(range(1, 65)):
        raise ValueError("incomplete Batman Forever printed switch or lamp tables")
    if len([c for c in coils if re.fullmatch(r"\d+[LR]", c)]) != 16 or not {str(n) for n in range(9, 23)} <= set(coils):
        raise ValueError("incomplete Batman Forever printed driver table")
    if len(SWITCH_LABELS) != 64 or len(LAMP_LABELS) != 64:
        raise ValueError("incomplete Batman Forever semantic inventory")
    rom = readings()
    places = load_json(ROOT / "tools/batman_forever_places.json")
    inputs, outputs = [], []

    for n in range(1, 65):
        cells = grid[n]
        label = SWITCH_LABELS[n - 1]
        identifier = "switch." + slug(label)
        col, row = (n - 1) // 8, (n - 1) % 8
        unused = n in UNUSED_SWITCHES
        part = cells[3] if re.match(r"\d{3}-", cells[3]) else None
        reading = rom.get(("switch", n))
        notes = f"Matrix grid: {cells[1]}. Parts list: {cells[2]}; part {cells[3]}."
        if reading:
            notes += f" The ROM's SWITCH TEST prints {reading['name']}" + (f" and part {reading['part']}" if reading.get("part") else "") + f", {reading['return_wire']} RETURN {reading['return_pin']} and {reading['drive']}."
        if n == 15:
            notes += " The manual's OPTO Theory of Operation (PDF 111) says a clear beam is an open matrix switch and a blocked beam a closed one; the public state is 1 while a ball blocks the up-kicker opto, with no extra host inversion."
        if n == 51:
            notes += " The parts list prints RIGHT GOOD HEADS STAND-UP BOTTOM; the grid, the Tech Chart and the ROM agree on RIGHT BAD HEADS, matching lamp 44."
        if n in (53, 54):
            notes += " The parts list swaps 53 and 54; the grid, the Tech Chart, the ROM and the table's own comment (\"Manual is wrong\") agree on 53 LEFT RAMP EXIT and 54 MIDDLE RAMP EXIT."
            notes += f" The location drawing on the same page labels the two exit switches the parts list's way: its {54 if n == 53 else 53} callout ends within {0.015 if n == 53 else 0.043} normalized of this placement and its {n} callout at the other exit."
        if n in (25, 26, 27, 28, 29, 42, 43, 50, 51):
            notes += " The parts list's stand-up part number differs from the ROM and Tech Chart's switch part; the printed values are kept in the excerpts."
        if n in (11, 12, 13, 14):
            notes += " A subminiature microswitch in the inclined 4-Ball Trough (OPTO) Assembly 500-5989-01-38; balls rest from 11 (left) up to 14 (right) at the lock-out cam. The table models the trough as a ball stack, so there is no switch object."
        if n == 32:
            notes += " The ROM debounces this kicker switch for about 0.6 s before naming it."
        if n in (44, 45, 46):
            notes += {44: " The micro switch 180-5057-00 at the open end of the Batwing Cannon Assembly 515-6321-00-38, where a ball rests in front of the plunger. The table's BWGun kicker sets it.",
                      45: " Listed \"On Asm.\" with part 180-5119-00. Neither the manual nor the ROM says what it senses; the table only pulses it when output 15 fires and has no object for it. The ROM debounces it for about 0.9 s.",
                      46: " The micro switch 180-5119-00 on the Cannon Motor Drive Assembly 500-6018-00-38, beside the large cam link. The table derives it from a cvpmMech (Sol1 14, 200 steps, closed at steps 0-3 and 197-200), not from an object."}[n]
        if n in (60, 61, 62):
            notes += " A Batcave lock position on the VUK wire ramp (\"(On Ramp)\"); the table's bsBallLock stack sets it (InitSw 0,62,61,60) and has no per-switch object. The ROM debounces it for about 1.2 s."
        if n == 49:
            notes += " The micro switch 180-5111-00 inside the Bat Gun Assembly 500-5945-00-38 on the cabinet front; the table writes it from the plunger key."
        if n in (63, 64):
            notes += f" FLIP6364 copies {'84' if n == 63 else '82'} into this matrix address on every update, so drive that flipper-column button, not {n}: the table's direct writes to {n} are overwritten, and only its de.vbs call writes the effective button."
            notes += " The parts list calls 63 the lower left flipper switch stack and 64 the upper and lower right flipper switch stack: the right cabinet button also enables the upper right flipper on the 3-flipper board." if n == 64 else ""
        if n in (1, 2, 5, 6, 7):
            notes += " A cabinet or coin-door switch not drawn on the playfield."
        item = {"id": identifier, "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": n},
                "aliases": aliases("switch", n, str(n)), "availability": "unused" if unused else "used",
                "provenance": prov(MANUAL, CHART, CORE, RUNTIME, *([] if unused or n in (2, 3, 4, 5, 6, 7, 8) else [SCRIPT])),
                "physical": {"notes": notes},
                "wiring": {"board": "CPU", "driver_transistor": SW_DRIVE[col][0], "drive_wire": SW_DRIVE[col][1],
                           "drive_connection": SW_DRIVE[col][2], "return_wire": SW_RETURN[row][0], "return_connection": SW_RETURN[row][1]}}
        if not unused:
            item["normally_closed"] = False
            item["physical"]["switch_type"] = switch_type(n, part)
            if part:
                item["physical"]["part_number"] = part
            elif n == 15:
                item["physical"]["part_number"] = "520-5124-00; 520-5125-00"
        if n in (63, 64):
            item["roles"] = [f"flipper.lower.{'left' if n == 63 else 'right'}.matrix-copy"]
        if unused:
            item["spatial"] = na("unused", MANUAL, RUNTIME)
        elif n in CABINET_SWITCHES:
            item["spatial"] = na("cabinet_or_service", MANUAL, CORE)
        elif (s := spatial(f"switch.{n}", identifier, "sensor", places)):
            item["spatial"] = s
        inputs.append(item)

    for n, label in ((-7, "Black Begin Test / Enter Button"), (-6, "Green Select Button")):
        inputs.append({
            "id": f"switch.service-{'enter' if n == -7 else 'select'}", "label": label, "kind": "switch",
            "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": aliases("switch", n),
            "availability": "used", "pulse": True, "normally_closed": False,
            "physical": {"switch_type": "button", "location": "inside coin door",
                         "notes": "The cabinet wiring drawing (PDF 104 / printed 96) draws the two PORTAL SERVICE BUTTONS as normally-open contacts wired BLU to CPU CN14-4 and GRN to CN14-3 with WHT ground on CN14-2; it does not say which wire serves which button. The Portals text (PDF 22) names the Black Begin Test / Enter and Green Select buttons. des112 uses DE_COMPORTS2, whose Green input is momentary; the table's de.vbs toggles -6 on each key press instead."},
            "provenance": prov(MANUAL, CORE, RUNTIME, VPM_DE_LIBRARY_SOURCE),
            "spatial": na("cabinet_or_service", MANUAL),
        })
    inputs.extend(flipper_column_inputs(
        flip_swno=(63, 64), flip_swno_text="FLIP6364 = FLIP_SWNO(63,64)", core_refs=(CORE,),
        button_refs=(SCRIPT, VPM_DE_LIBRARY_SOURCE, RUNTIME),
        button_notes={side: f"The table's key handler writes {63 if side == 'left' else 64} directly and then calls de.vbs vpmKeyDown, whose swL{'L' if side == 'left' else 'R'}Flip is {84 if side == 'left' else 82}; the harness read back {63 if side == 'left' else 64} = 1 only while {84 if side == 'left' else 82} was held. " + ("The left cabinet button switches the lower left flipper on the 3-flipper board." if side == "left" else "The right cabinet button stack switches both the lower right and the upper right flipper on the 3-flipper board.") for side in ("left", "right")},
        unused_notes=vpm_staged_flipper_notes(library="DE.VBS"), unused_note_refs=(VPM_DE_LIBRARY_SOURCE,)))
    for item in inputs:
        if item["binding"]["device"] in (82, 84):
            item["normally_closed"] = False
            item["provenance"]["source_refs"].append(MANUAL)
            item["physical"]["notes"] += " The 3-flipper board diagram (PDF 115) draws the FLIPPER CABINET SWITCHES as normally-open contacts."
    inputs.append({"id": "dip.country-jumper-w7", "label": "Country Jumper W7", "kind": "dip_switch",
                   "binding": {"group": "pinmame.input.dip", "device": 0}, "aliases": [], "availability": "unknown",
                   "physical": {"notes": "s11.c pia2a_r reads core_getDip(0)<<7. No retained Batman Forever evidence assigns its two values to a country or a fitted jumper position."},
                   "provenance": prov(CORE, status="observed"), "spatial": na("dip_switch", CORE)})

    for n in range(1, 65):
        manual_number = f"{n}L" if n <= 8 else f"{n - 24}R" if 25 <= n <= 32 else str(n)
        printed = coils.get(manual_number)
        reading = rom.get(("solenoid", n))
        if n in COILS:
            label, kind = COILS[n]
            identifier = f"{kind}." + slug(label)
            notes = f"Driver chart {manual_number}: {printed[1]}."
            if reading:
                notes += f" The ROM's COIL TEST prints {reading['name']}" + (f" with CPU {reading['cpu']}" if reading.get("cpu") else "") + " and fires this address alone."
            physical = {"notes": notes}
            if kind in ("coil",):
                physical["part_number"] = printed[9]
            if kind == "flasher":
                physical["quantity"] = 4
                physical["part_number"] = printed[9]
            elif kind == "coil":
                physical["quantity"] = 1
            extra = {
                1: " The 25-1240 coil of the Lock Ball Assembly 500-5684-01 releases one ball from trough position 14 toward the up-kicker; the table has no object for it.",
                2: " The 23-800 up-kicker at the trough's upper end lifts the ball past opto 15 into shooter lane 16.",
                3: " Autolaunch Assembly 500-5477-01 under the butyrate at the shooter lane. On the first serve the ROM waits for the gun trigger (skill shot); later serves launched without it.",
                4: " Vertical Up-Kicker Assembly 500-5839-01 at the upper right; the ball goes up the wire ramp to the Batcave.",
                5: " Ball Eject (Saucer) Assembly 500-5664-00 at the upper left, the Gotham Event saucer.",
                7: " One reset coil for the 4-Bank Drop Target Assembly 500-5799-04; its placement is projected onto the mean of the four target primitives, not a measured coil centre. The Tech Chart prints 50v L; the manual and the ROM's BRN 32V DC agree on 32v.",
                8: " Knocker Assembly 500-5081-00 in the cabinet.",
                9: " Batcave Ball Lock 500-5947-00-38 on the left side: releases the bottom ball of the three-ball lock stack 62/61/60 toward the Batcave exit kicker.",
                10: " K1 A/B relay on the PPB selects the 1L-8L coil loads (off) or the 1R-8R flasher loads (on) on drives 1-8; these are eight shared drivers with alternate loads. The COIL TEST has no entry for it.",
                11: " A 24v DC relay on the power supply board switches the 6.3 VAC G.I. supply; the ROM's COIL TEST prints its PS traces. The table hides its G.I. lights while the relay is energized. Placements are the table's G.I. bulb lights; the physical socket count and string allocation are not settled.",
                12: " Ramp Diverter Assembly 500-5940-00-38 (27-1500 coil) moves the Bridge Diverter on the Double Stack Wire Ramp 500-5932-00-38, sending a left-ramp ball down the lower wire ramp to the Batwing Cannon.",
                14: " Not a solenoid: the driver energizes a 24v DC 10A DPDT relay on relay board 520-5010-00 (part number printed by the ROM and the Tech Chart) whose N.O. contact switches 28 VAC from BR2 to the Cannon Motor Drive Assembly 500-6018-00-38 (motor 515-6383-00). Through a crank and cam links the motor swings the Batwing Cannon; home switch 46 sits on the drive.",
                15: " The 23-800 coil and plunger of the Batwing Cannon Assembly 515-6321-00-38 fire a ball loaded at 44 in the direction the cannon points.",
                16: " Batcave Exit Kicker 500-5948-00-38 (24-940) kicks the ball from 30 down the wire ramp over the lower arch onto the playfield.",
                22: " Laser Kick Assembly 500-5838-00 under the arch at the left outlane, fired from switch 33 when lit.",
                27: " The table's single light for this circuit, Flasher3R, sits where the flash lamp location drawing puts 5R's ramp socket (\"On the Ramp.\"); the drawing's four 3R sockets run along the left orbit and have no table object.",
                29: " The wiring diagram's branch label names a 2-bank stand-up; the driver chart, its location table and drawing (\"On the Ramp.\") and the ROM's text put the playfield socket at the left/middle ramp.",
            }.get(n, "")
            physical["notes"] += extra
            if kind == "flasher":
                physical["notes"] += " Four sockets on this branch per the driver chart and the wiring diagram, which agree on the #89/#906 mix; the backbox insert drawing locates the insert sockets."
            if n == 14:
                physical["part_number"] = "515-6383-00"
                physical["quantity"] = 1
            if n in (10, 11):
                physical["part_number"] = printed[9]
            item = {"id": identifier, "label": label, "kind": kind, "binding": {"group": "pinmame.output.solenoid", "device": n},
                    "aliases": aliases("solenoid", n, manual_number), "availability": "used", "physical": physical,
                    "provenance": prov(MANUAL, CHART, CORE, RUNTIME, *([] if n == 8 else [SCRIPT]))}
            item["wiring"] = {"board": printed[3].strip("{}"), "driver_transistor": printed[2].strip("{}"),
                              "control_wire": printed[4], "control_connection": printed[5],
                              "power_wire": printed[6], "power_connection": printed[7]}
            if n in (8, 10):
                item["spatial"] = na("cabinet_or_service", MANUAL)
            elif (s := spatial(f"solenoid.{n}", identifier, "emitter" if kind in ("gi", "flasher") else "effect", places)):
                item["spatial"] = s
        elif n in UNUSED_DRIVERS:
            label = f"Unused Driver {manual_number}"
            identifier = "virtual." + slug(label)
            item = {"id": identifier, "label": label, "kind": "virtual", "binding": {"group": "pinmame.output.solenoid", "device": n},
                    "aliases": aliases("solenoid", n, manual_number), "availability": "unused",
                    "physical": {"notes": (f"Driver chart row {manual_number} is printed shaded NOT USED with {printed[2]}, {printed[4]} and {printed[5]} but dashes for the coil. "
                                           + ("The coil wiring diagram (PDF 108) prints \"NO COIL AT THIS LOCATION Q41CPU 6L\". " if n == 6 else "The coil wiring diagram (PDF 108) draws loads only on CPU CN12 pins 1, 5 and 7, none on CN12-6, and the 3-flipper board takes no CPU driver. ")
                                           + ("The ROM's own diagnostics publish state here: CYCLING COILS pulses 6 while it displays #6L: NOT USED, and the COIL TEST shows #6L: NOT USED without a RUN entry." if n == 6 else "The ROM's own diagnostics publish state here: RUN on #13: NOT USED in the COIL TEST holds 13 on until the selection moves, and CYCLING COILS holds it for about 2.5 s while displaying #13: NOT USED.")
                                           + " No gameplay or attract run published it. The diagnostics walk every driver slot, so this state drives no load.")},
                    "provenance": prov(MANUAL, CHART, CORE, RUNTIME), "spatial": na("unused", MANUAL, RUNTIME),
                    "wiring": {"board": "CPU", "driver_transistor": printed[2], "control_wire": printed[4], "control_connection": printed[5]}}
        else:
            is_aux, is_flip = 37 <= n <= 44, 45 <= n <= 48
            label = (f"CN3 Printer Data Bit {n - 37}" if is_aux else
                     f"Synthetic Lower {'Right' if n <= 46 else 'Left'} Flipper {'Power' if n % 2 else 'Hold'}" if is_flip else
                     f"Unused Solenoid Address {n}")
            identifier = f"virtual.{slug(label)}"
            printer_pin = {37: 9, 38: 8, 39: 7, 44: 1}.get(n)
            note = ("S11_PRINTERLINE publishes PIA2:B bit " + str(n - 37) + " here. " + (f"The pinned pia2b_w comment names CN3 pin {printer_pin}. " if printer_pin is not None else "The pinned pia2b_w comment elides bits 3-6, so no connector pin is asserted. ") + "The cabinet wiring diagram draws a printer board on the CPU data lines and the manual describes printer adjustments 52-54, but the USA 4.01 ROM's main menu has no PRNT icon and its adjustments end at Sega 43 and Batman 52 (Novice Game Available). No run saw a transition here, and non-observation is not proof of non-use."
                    if is_aux else
                    "core_updateSw fabricates the paired power/hold states together from cabinet button " + str(82 if n <= 46 else 84) + " while 23 enables flippers; they are not independently wired CPU coils. The table's sLRFlipper callback (46) moves both the lower right and the upper right flipper, matching the shared right button stack; sLLFlipper (48) moves the lower left flipper."
                    if is_flip else
                    "No Batman Forever load or producer is present at this address: 24 has no Data East state producer, 33-36 have no core_getSol path, 49 is a simulator slot with no Batman Forever simulator, 50 is reserved, and 51-64 would need a custom solenoid count or getSol, which INITGAMES11 does not declare.")
            item = {"id": identifier, "label": label, "kind": "virtual", "binding": {"group": "pinmame.output.solenoid", "device": n},
                    "aliases": aliases("solenoid", n), "availability": "unknown" if is_aux else "used" if is_flip or n == 23 else "unused",
                    "provenance": prov(CORE, *([RUNTIME, SCRIPT] if is_flip else []), status="observed" if is_aux else "validated"),
                    "physical": {"notes": note}, "spatial": na("virtual" if is_aux or is_flip or n == 23 else "unused", CORE)}
            if n == 23:
                item["id"] = "virtual.game-on-enable"
                item["label"] = "Game On / Switched Solenoid Enable"
                item["physical"]["notes"] = "S11_GAMEONSOL = 23 is the PIA0 CB2 switched-solenoid enable and gates the synthetic flipper states; the ROM raises it during play and its coil tests. No physical coil is fitted at this public address."
                item["provenance"]["source_refs"].append(RUNTIME)
        outputs.append(item)

    for n in range(1, 65):
        cells = lamp_grid[n]
        label = LAMP_LABELS[n - 1]
        identifier = "lamp." + slug(label)
        col, row = (n - 1) // 8, (n - 1) % 8
        reading = rom.get(("lamp", n))
        unused = n in UNUSED_LAMPS
        bulb = re.match(r"(#\d+)", cells[2])
        note = f"Matrix grid: {cells[1]}, {cells[2]}. Wiring-diagram list: {lamp_names[n]}."
        if reading:
            note += f" The ROM's SINGLE LAMP TEST prints {reading['name']}" + (f" with bulb {reading['bulb']}" if reading.get("bulb") else "") + " and lights this address alone."
        physical = {"notes": note}
        if unused:
            physical["notes"] += " The lamp location drawing lists it among \"The following Lamps are not used\" and the ROM prints NOT USED without wiring; the lamp test's walk of every address explains its published state."
        else:
            part = BULB_PARTS[bulb.group(1)] if bulb else None
            if n == 50:
                part = BULB_PARTS["#44"]
                physical["notes"] += " The manual grid prints #555; the Tech Chart 820-6104-05 and the ROM both print #44, which this record follows."
            if n in (49, 50):
                physical["notes"] += " The wiring-diagram list puts 49 and 50 at the left ramp enter. The left/middle ramp assembly's rollunder gate carries \"LIGHTS on Sign\" with two #555 wedge bulbs and red and yellow covers but names no lamp numbers, so the sign lights are not tied to these addresses here."
            if n in (33, 34):
                physical["notes"] += (" One of the two #555 sockets of the Spot-Lite Assembly 500-5818-01 on the left/middle ramp. Both table lights for this pair carry TimerInterval 33 and sit at the table's left edge, so the table never drives a light from lamp 34 and neither object stands for a socket."
                                      " Spatial: measured on the lamp location drawing (PDF 37) at its open box, through that page's bumper-cap and flipper-pivot fit (tools/seeds/sega/batman-forever-1995-callouts.json); the box marks the lamp, not its socket centre, so the placement is a candidate.")
            if n == 58:
                physical["notes"] += " The table also binds Lamp59 (in the right bumper cap) to 58 by TimerInterval, a table defect; only Lamp58 is placed here."
            if n == 59:
                physical["notes"] += " The table's light in this bumper cap, Lamp59, carries TimerInterval 58, so the table never lights it from 59. Its position is retained as the right turbo bumper cap, not as a script binding."
            if n in (57, 58, 59):
                physical["notes"] += " The table also lists the three bumper lamps in its G.I. collections; they are matrix lamps here."
            if part:
                physical["part_number"] = part
            physical["quantity"] = 1
        item = {"id": identifier, "label": label, "kind": "lamp", "binding": {"group": "pinmame.output.lamp", "device": n},
                "aliases": aliases("lamp", n, str(n)), "availability": "unused" if unused else "used", "physical": physical,
                "provenance": prov(MANUAL, CHART, CORE, RUNTIME, *([] if unused or n in (34, 59) else [SCRIPT]))}
        if not unused:
            item["wiring"] = {"board": "CPU", "driver_transistor": LAMP_DRIVE[col][0], "drive_wire": LAMP_DRIVE[col][1],
                              "drive_connection": LAMP_DRIVE[col][2], "return_wire": LAMP_RETURN[row][1],
                              "return_connection": LAMP_RETURN[row][2], "return_component": LAMP_RETURN[row][0]}
            if col == 4:
                item["physical"]["notes"] += " The manual grid prints the drive connector as GN7-5; the Tech Chart and the ROM print CN7-5."
        if unused:
            item["spatial"] = na("unused", MANUAL, RUNTIME)
        elif n in CABINET_LAMPS:
            item["spatial"] = na("cabinet_or_service", MANUAL)
        elif n == 59:
            item["spatial"] = spatial("lamp.59", identifier, "emitter", places, TABLE, GEOMETRY, MANUAL)
        elif n in (33, 34):
            item["spatial"] = measured_spatial(identifier)
        elif (s := spatial(f"lamp.{n}", identifier, "emitter", places)):
            item["spatial"] = s
        outputs.append(item)

    sw = {x["binding"]["device"]: x["id"] for x in inputs if x["binding"]["group"] == "pinmame.input.switch"}
    sol = {x["binding"]["device"]: x["id"] for x in outputs if x["binding"]["group"] == "pinmame.output.solenoid"}
    mechanisms = []

    def mech(key, label, kind, act, sensors, behavior, assembly=None, refs=(MANUAL, SCRIPT, CORE, RUNTIME)):
        item = {"id": "mech." + key, "label": label, "kind": kind, "actuators": [sol[n] for n in act],
                "sensors": [sw[n] for n in sensors], "behavior": behavior, "provenance": prov(*refs)}
        if assembly:
            item["assembly_part_number"] = assembly
        mechanisms.append(item)

    mech("trough", "Four-ball trough and up-kicker", "kicker", [1, 2], [11, 12, 13, 14, 15],
         "Four balls rest on subminiature switches 11 (left) to 14 (right) in the inclined trough under the right apron. Output 1, the lock-out cam, releases the ball at 14 toward the up-kicker; the remaining balls roll down one position. A ball at the up-kicker blocks opto 15, and output 2 lifts it into shooter lane 16. In the harness, the ROM fired 1 to serve, then 2 once 15 closed. The table models the trough as bsTrough (InitSw 0,14,13,12,11) and a separate bsBallRelease saucer at 15.",
         "500-5989-01-38")
    mech("autolaunch", "Gun-trigger autolaunch", "kicker", [3], [16, 49],
         "Shooter lane 16 feeds the autolaunch under the butyrate (output 3), which shoots the ball up the shooter lane ramp. On the first serve of a ball the ROM shows the skill-shot choice and launches when the cabinet gun trigger 49 is pulled; a ball served to replace a locked ball launched without the trigger. If 16 stays closed after launching, the ROM retries and reports OPERATOR ALERT! AUTOLAUNCH NOT WORKING.",
         "500-5477-01")
    mech("top-eject", "Top eject saucer", "kicker", [5], [41],
         "The upper-left saucer 41 holds a ball until output 5 kicks it out (0.17 s after 41 closed in the harness gameplay run); it starts lit Gotham Events.", "500-5664-00")
    mech("vuk", "VUK to the Batcave", "kicker", [4], [32],
         "The upper-right vertical up-kicker 32 lifts a ball with output 4 (5.6 s after 32 closed in the harness gameplay run) up the wire ramp to the Batcave on the left side, where it reaches the lock stack 62/61/60.", "500-5839-01")
    mech("batcave-lock", "Batcave ball lock", "kicker", [9], [62, 61, 60],
         "The Batcave holds up to three balls on 62 (bottom), 61 (middle) and 60 (top). When the C-A-V-E bank has lit locks, a ball arriving at 62 is held and the ROM serves a replacement from the trough (observed: 62 closing answered by lock-out 1). Output 9 releases the bottom ball toward the Batcave exit kicker 30. The table models the lock as bsBallLock (InitSw 0,62,61,60) kicked out by 9.",
         "500-5947-00-38")
    mech("batcave-exit", "Batcave exit kicker", "kicker", [16], [30],
         "A ball at 30 is kicked by output 16 (0.93 s after 30 closed in the harness gameplay run) down the Batcave exit wire ramp over the lower arch onto the playfield.", "500-5948-00-38")
    mech("drops", "C-A-V-E four-target drop bank", "drop_target_bank", [7], [18, 19, 20, 21],
         "Targets 18-21 (C, A, V, E) latch down independently and stay closed while down. Output 7 resets the whole bank; in the harness gameplay run it fired 0.2 s after the fourth target dropped. The table raises all four with DTRaise.", "500-5799-04")
    mech("ramp-diverter", "Batwing ramp diverter", "diverter", [12], [52, 44],
         "Output 12 moves the Bridge Diverter on the double stack wire ramp that leaves the left/middle ramp: energized, it sends a left-ramp ball (entering at 52) down the lower wire ramp to the Batwing Cannon, where it closes 44; at rest the ball continues on the upper wire. Rules: ARM BATWING lit on the left ramp loads the cannon. The table makes RampDiverter non-collidable while 12 is on.",
         "500-5940-00-38")
    mech("batwing-cannon", "Batwing cannon", "motorized", [14, 15], [44, 45, 46, 49],
         "A ball delivered to the cannon closes 44. The ROM then energizes motor relay 14 (about 2 s after 44 in the harness), and the AC motor swings the cannon through a crank and cam links; home switch 46 marks the home position on the drive. Pulling the cabinet gun trigger 49 fires output 15 (about 0.1 s later), shooting the ball the way the cannon points. During FOREVER the cannon oscillates and a ball must be caught as it passes home. Switch 45 BATWING CANNON SAFETY is on the assembly, but no source says what it senses. The table drives the swing with a cvpmMech on 14 (500 ms per 200 steps, reversing, 46 closed at both ends).",
         "515-6321-00-38")
    mech("bumpers", "Three turbo bumpers", "other", [17, 18, 19], [57, 58, 59],
         "Left, bottom and right switches 57, 58 and 59 fire special-solenoid outputs 17, 18 and 19 within milliseconds in the harness.", "500-5966-00")
    mech("slings", "Left and right slingshots", "other", [20, 21], [35, 36],
         "Left 35 and right 36 fire outputs 20 and 21 within milliseconds in the harness.", "500-5849-00")
    mech("laser-kick", "Left outlane Laser Kick", "kicker", [22], [33],
         "When the feature is lit, left outlane switch 33 fires output 22 (within 10 ms in the harness), kicking the ball back up the outlane from under the arch. Completing the top lanes relights it.", "500-5838-00")
    mech("player-flippers", "Cabinet-controlled flippers", "other", [45, 46, 47, 48], [82, 84],
         "Three flippers: lower left (22-1080), lower right (22-900) and upper right (23-900) on the solid state 3-flipper board 520-5076-00. The left cabinet button enables the lower left flipper; the right button stack enables both right flippers. Only the lower flippers have N.C. EOS switches; the upper flipper's EOS is printed Not Used. PinMAME copies 82/84 to matrix 64/63 and fabricates 45/46 and 47/48 in pairs, so use one state per side. No CPU driver reaches the flipper board.")
    mech("knocker", "Cabinet knocker", "other", [8], [], "Output 8 pulses the cabinet knocker 500-5081-00; it has no playfield sensor or placement.", "500-5081-00")
    mech("lighting-control", "PPB bank selection and G.I. control", "other", [10, 11], [],
         "Relay 10 on the PPB switches drives 1-8 between the coil loads 1L-8L and the flasher loads 1R-8R (25-32). Relay 11 on the power supply board switches the G.I. supply; the table's G.I. is lit while 11 is off.")
    relationships = flipper_column_relationships(flip_swno=(63, 64), matrix_ids={63: sw[63], 64: sw[64]}, refs=(CORE, RUNTIME))
    for n in range(25, 33):
        relationships.append({"id": f"relationship.mux-{n}", "kind": "relay_gated", "source": sol[10], "destination": sol[n], "provenance": prov(MANUAL, CORE, RUNTIME)})
    for s, o in ((57, 17), (58, 18), (59, 19), (35, 20), (36, 21)):
        relationships.append({"id": f"relationship.switch-{s}-coil-{o}", "kind": "pulse", "source": sw[s], "destination": sol[o], "provenance": prov(MANUAL, CORE, RUNTIME)})
    conflicts = []
    definition = {
        "format": "pinmame-machine-definition", "schema_version": 2,
        "machine": {"id": KEY, "name": "Batman Forever", "manufacturer": "Sega", "year": 1995, "kind": "physical_pinball",
                    "model_number": "38", "ipdb_id": 3593, "opdb_id": "G59zN-MLy0N",
                    "playfield": {"width": 1093, "height": 2162, "units": "vpx", "provenance": prov(TABLE, status="observed")}},
        "controller": {"platform": "pinmame.dataeast", "hardware_generation": "0x8000", "inversion_applied_by_emulator": True},
        "coverage": {"status": "partial", "missing": MISSING + (["unresolved_conflicts"] if unresolved_conflicts({"conflicts": conflicts}) else []),
                     "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
                                    "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated",
                                    "recreation_knowledge": "validated", "runtime_observation": "observed", "causal_exercise": "observed",
                                    "spatial_placement": "observed"}},
        "drivers": [{"id": n, "description": label, "year": year, "manufacturer": "Sega", "flags": 0,
                     **({"clone_of": "batmanf"} if n != "batmanf" else {}), "physical_compatibility": "identical",
                     "variant_notes": "All 23 drivers use init_batmanf / GEN_DEDMD64 / de_192x64DMD / FLIP6364 / SNDBRD_DE2S and the same physical I/O; they differ in CPU, display and sound ROM images (language, timed play, revision). The 2024 and 2025 unofficial firmware revisions run on the same machine; their catalog years are firmware dates. Only the batmanf-prefixed drivers match s11.c's Batman Forever PWM branch (G.I. and flasher brightness models); the bmf_ clones use the default output model."}
                    for n, label, year in DRIVER_ROWS],
        "inputs": inputs, "outputs": outputs,
        "displays": [{"id": "display.main-dmd", "label": "Backbox 192 x 64 DMD", "kind": "dmd", "controller_index": 0, "width": 192, "height": 64,
                      "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", CORE, MANUAL), "provenance": prov(CORE, MANUAL, RUNTIME)}],
        "mechanisms": mechanisms, "relationships": relationships, "sources": build_sources(),
        "conflicts": conflicts, "knowledge": {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"},
    }
    # Factory location-drawing callouts promote the placements they confirm.
    drawing_callouts.apply_to_definition(definition, load_json(CALLOUT_SEED), CALLOUTS)
    return definition


def build_sources():
    places = load_json(ROOT / "tools/batman_forever_places.json")
    base = {"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Sega Pinball, Inc.; hosted by IPDB"}
    manual_sha, manual_capture, manual_at = MANUALS[MANUAL_NAME]
    chart_sha, chart_capture, chart_at = MANUALS[CHART_NAME]
    return [
        {"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REV}/src/wpc/degames.c", "revision": REV,
         "locator": "degames.c 77-89 INITGAMES11/des112/FLIP6364 and Batman Forever block 1532-1843; s11.c setSSSol, updsol, pia2b_w, pia2a_r, pia4a_r/pia4b_w and the DataEast/Sega 3b PWM branch 1252-1257; s11.h DE_COMPORTS2 and S11_GAMEONSOL; core.c core_updateSw/core_getSol; gen.h GEN_DEDMD64.",
         "license": "BSD-3-Clause", "attribution": "PinMAME contributors", "excerpts": [checked_excerpt("controller.md", "pinned sources, exact symbols and public arithmetic")]},
        {"id": "pinmame.batman-forever.catalog", "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": REV,
         "locator": "PinmameGetGames and degames.c batmanf root plus 22 clones", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
        {"id": MANUAL, "kind": "manual", "uri": f"https://web.archive.org/web/{manual_capture}id_/https://www.ipdb.org/files/3593/{MANUAL_NAME}",
         "original_filename": MANUAL_NAME, "source_id": "IPDB 3593", "sha256": manual_sha, "acquired_at": manual_at,
         "locator": "Verified IPDB machine https://www.ipdb.org/machine.cgi?id=3593 (Sega 'Batman Forever', model 38, July 1995, DataEast/Sega Version 3b). 152-page scan; PDF 13-19 overview and rules (printed 7-13), PDF 30-37 switch, coil and lamp tables (printed 24-31), PDF 66-100 assemblies, PDF 104 cabinet wiring, PDF 108-111 coil, lamp and opto diagrams, PDF 115 3-flipper board. External manuals/by-machine/sega.batman-forever.1995.",
         **base, "excerpts": [
             checked_excerpt("switches.md", "PDF 30-31, printed 24-25, complete switch grid, parts list and location legend; PDF 111 opto theory"),
             checked_excerpt("lamps.md", "PDF 36-37, printed 30-31, complete lamp grid and location legend; PDF 110 description table; PDF 97 ramp lights"),
             checked_excerpt("coils.md", "PDF 32-34, printed 26-28, complete driver, flipper, location and backbox flasher tables; PDF 108 flasher branches"),
             checked_excerpt("mechanisms.md", "PDF 13-19, 66, 80-97, 108 and 115: routing, rules, assemblies, CN12 loads and 3-flipper board")]},
        {"id": CHART, "kind": "manual", "uri": f"https://web.archive.org/web/{chart_capture}id_/https://www.ipdb.org/files/3593/{CHART_NAME}",
         "original_filename": CHART_NAME, "source_id": "IPDB 3593", "sha256": chart_sha, "acquired_at": chart_at,
         "locator": "One-page Tech Chart 820-6104-05 (switch grid with part numbers, lamp grid with bulbs, fuse list, coil table); verified IPDB machine https://www.ipdb.org/machine.cgi?id=3593. External manuals/by-machine/sega.batman-forever.1995.",
         **base, "excerpts": [checked_excerpt("tech-chart.md", "switch part numbers and lamp bulbs in full; every cell differing from the manual")]},
        {"id": TABLE, "kind": "vpx_table", "uri": "external:vpx-sources/sega/batman-forever-1995/Batman%20Forever%20%28Sega%201995%29%201.3.vpx",
         "sha256": places["table_sha256"], "known_working": True,
         "locator": "Batman Forever (Sega 1995) 1.3: mfuegemann VP9 1.2, VPX conversion by DevaL, updates by drakkon, Sheltemke, TastyWasps and Sixtoe; 1093 x 2162 VPX units; cGameName batmanf; retained from the authorized local table library",
         "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "mfuegemann, DevaL, drakkon and contributors credited in the retained table", "acquired_at": "2026-10-23T18:45:21Z"},
        {"id": SCRIPT, "kind": "vpx_script", "uri": "external:vpx-sources/sega/batman-forever-1995/extracted-vpxtool/script.vbs",
         "sha256": places["script_sha256"], "known_working": True,
         "locator": "lines 126-190 library and solenoid callbacks; 318-399 init, ball stacks and cannon mech; 420-686 kickers, flashers, cannon and keys; 700-925 switch handlers; 3540-3878 drop and stand-up targets",
         "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "mfuegemann, DevaL, drakkon and contributors credited in the retained table",
         "excerpts": [checked_excerpt("script-bindings.md", "machine-specific I/O bindings, mechanisms and table defects, summarized factually")]},
        {"id": EXTRACTION, "kind": "vpx_table", "uri": "external:vpx-sources/sega/batman-forever-1995/extracted-vpxtool/manifest.json",
         "sha256": places["manifest_sha256"],
         "locator": "vpxtool git:v0.33.3; 1,849 payload files / 119,050,497 bytes; tools/build_external_evidence_manifest.py --game batmanf sorts relative POSIX paths, records size/SHA256, canonical JSON plus LF; manifest files excluded from their own payload",
         "license": "NOASSERTION", "attribution": "mfuegemann, DevaL, drakkon and contributors; extraction by project contributors"},
        {"id": GEOMETRY, "kind": "human_review", "uri": "internal:tools/batman_forever_places.json", "sha256": sha(ROOT / "tools/batman_forever_places.json"),
         "locator": "build_batman_forever_places.py: script-linked object selection, stored centres, wall drag-point means and exported world-mesh bounds; OBJ SHA256 " + places["obj_sha256"] + ". One recreation lineage, all positions observed; rejected helpers and omitted devices are listed.",
         "license": "NOASSERTION", "attribution": "Primary curator; table geometry by the retained table's authors"},
        {"id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI, "sha256": VPM_DE_SHA256,
         "locator": "de.vbs lines 20-36 and vpmKeyDown/vpmKeyUp 66-114; retained machine-neutral library loaded by LoadVPM at script line 136",
         "license": "NOASSERTION", "attribution": "VPinMAME script-library maintainers", "excerpts": [checked_excerpt("controller.md", "de.vbs constants and key handlers")]},
        {"id": CALLOUTS, "kind": "human_review", "uri": "internal:" + CALLOUT_SEED.relative_to(ROOT).as_posix(), "sha256": sha(CALLOUT_SEED),
         "locator": "2026-10-23 factory location-drawing callout check of PDF 31, 33 (coil and flash lamp drawings) and 37 (printed 25, 27, 31): every callout transcribed independently on the retained 300 dpi page renders, controls read on gridded crops (turbo bumper caps and flipper pivots; on the flash lamp drawing, which draws neither, eight lamp inserts), per-page control and callout fits; a table placement whose own callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py), and lamps 33/34 are measured. Reads, overlays and generator are retained under review-artifacts/sega.batman-forever.1995/callout-check.",
         "license": "NOASSERTION", "attribution": "Primary curator and independent readers; Sega drawings"},
        {"id": RUNTIME, "kind": "runtime_scenario", "uri": "internal:" + RUNTIME_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RUNTIME_PATH), "revision": REV,
         "locator": "Fresh-state batmanf (USA CPU 4.01NV, display A4.01) SWITCH, SINGLE LAMP, COIL and CYCLING COILS tests and a gameplay run; visually read DMD frames pinned to pixel digests in tools/seeds/sega/batman-forever-1995-runtime-readings.json; raw runs, frames and NVRAM external under review-artifacts/sega.batman-forever.1995/final.",
         "license": "NOASSERTION", "attribution": "Primary curator; user-authorized existing ROM"},
    ]


def verify_external():
    if manual_root := os.environ.get("PINMAME_MANUALS_ROOT"):
        for filename, (digest, _, _) in MANUALS.items():
            path = Path(manual_root) / "by-machine" / KEY / filename
            if not path.is_file() or sha(path) != digest:
                raise ValueError(f"Batman Forever retained manual missing or changed: {path}")
    vpx_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    manuals = os.environ.get("PINMAME_MANUALS_ROOT")
    drawing_callouts.verify_retained(load_json(CALLOUT_SEED), ROOT, Path(manuals) if manuals else None, Path(review_root) if review_root else None)
    if review_root:
        from build_batman_forever_runtime import build as build_runtime

        review = Path(review_root)
        places = load_json(ROOT / "tools/batman_forever_places.json")
        obj = review / KEY / "world-obj/Batman Forever (Sega 1995) 1.3.obj"
        if not obj.is_file() or sha(obj) != places["obj_sha256"]:
            raise ValueError(f"Batman Forever retained OBJ missing or changed: {obj}")
        if build_runtime(review) != load_json(RUNTIME_PATH):
            raise ValueError("Batman Forever runtime evidence differs from the retained runs")
        if vpx_root:
            from build_batman_forever_places import build as build_places

            # This builder verifies the VPX/script identities and extraction manifest itself.
            if build_places(Path(vpx_root), obj) != places:
                raise ValueError("Batman Forever placements differ from the retained extraction and OBJ")
    elif vpx_root:
        from build_external_evidence_manifest import check_manifest
        from build_batman_forever_places import MANIFEST_SHA, TABLE_SHA, SCRIPT_SHA, TABLE_NAME

        base = Path(vpx_root) / "sega/batman-forever-1995"
        if (sha(base / TABLE_NAME) != TABLE_SHA or sha(base / "extracted-vpxtool/script.vbs") != SCRIPT_SHA
                or check_manifest(base / "extracted-vpxtool", "batmanf") != MANIFEST_SHA):
            raise ValueError("Batman Forever external source identity mismatch")


def artifacts():
    definition = build()
    places = load_json(ROOT / "tools/batman_forever_places.json")
    count = sum(len(d.get("spatial", {}).get("placements", [])) for group in ("inputs", "outputs") for d in definition[group])
    absent = [d["id"] for group in ("inputs", "outputs") for d in definition[group] if d.get("availability") in ("used", "unknown") and "spatial" not in d]
    seed = load_json(CALLOUT_SEED)
    check = drawing_callouts.summary(seed, drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition)),
                                     CALLOUT_SEED.relative_to(ROOT).as_posix(), sha(CALLOUT_SEED))
    report = {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": KEY, "status": "partial",
        "coordinate_convention": "x=0 left, x=1 right; y=0 rear, y=1 apron; x=raw_x/1093, y=raw_y/2162. Six decimal places preserve deterministic table precision, not survey accuracy.",
        "placement_count": count,
        "source": {"table_sha256": places["table_sha256"], "extraction_manifest_sha256": places["manifest_sha256"], "obj_sha256": places["obj_sha256"]},
        "placements": places["placements"], "omitted_spatial_key_devices": absent,
        "blockers": [
            {"id": "single-recreation-lineage", "severity": "major", "detail": f"All table coordinates come from one recreation lineage (mfuegemann's VP9 table, converted and updated to 1.3); the two pinned community scripts are the same 1.3 table. The factory location-drawing callout check validates {check['validated']} of the {check['checked']} placements it covers; the rest stay observed, each with a note on its device, and lamps 33/34 are drawing-measured candidates."},
            {"id": "missing-trough-lock-and-cannon-geometry", "severity": "major", "detail": places["omitted"]},
            {"id": "gi-socket-survey", "severity": "major", "detail": "The table supplies 31 G.I. lights under output 11, but the manual gives no complete G.I. socket list or string allocation; the physical G.I. total is not asserted."},
        ],
        "projection_notes": {
            "solenoid.7": "Reset-coil coordinate projected onto the mean of the four drop-target primitives; not a surveyed coil position.",
            "switch.15": "BallRelease is the up-kicker saucer that also stands for the opto's ball position.",
            "solenoid.14": "pBatwing mesh-bounds centre: the cannon the motor swings, not the motor under the playfield.",
            "solenoid.12": "pDiverter mesh-bounds centre: the bridge diverter the coil moves.",
            "lamp.59": "Lamp59 sits in the right turbo bumper cap; the table binds it to 58 by TimerInterval.",
        },
        "rejected": places["rejected"],
        "mechanical_anchors": places["mechanical_anchors"],
        "drawing_callout_check": check,
    }
    knowledge = (ROOT / "tools/batman_forever_knowledge.md").read_bytes()
    return [(DEFINITION_PATH, canonical_bytes(definition)), (SEED_PATH, canonical_bytes(definition)),
            (KNOWLEDGE_PATH, knowledge), (SPATIAL_REPORT_PATH, canonical_bytes(report))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--regenerate", action="store_true")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.repository_root.resolve()
    verify_external()
    existing = root / f"machines/author-ready/sega/{SLUG}.json"
    if existing.exists():
        raise ValueError(f"refusing to overwrite an existing author-ready Batman Forever artifact: {existing}")
    for path, payload in artifacts():
        target = root / path.relative_to(ROOT)
        if args.check:
            if not target.is_file() or target.read_bytes().replace(b"\r\n", b"\n") != payload.replace(b"\r\n", b"\n"):
                raise ValueError(f"Batman Forever artifact missing or drifted: {target}")
        else:
            write_bytes(target, payload)
    print("Batman Forever definition, seed, knowledge and spatial report match the curator." if args.check else "Regenerated Batman Forever definition, seed, knowledge and spatial report.")


if __name__ == "__main__":
    main()
