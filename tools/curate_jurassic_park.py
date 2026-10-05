"""Deterministic, game-scoped curation of Data East Jurassic Park (1993).

Factory tables are literal checked transcriptions in jurassic_park_data.py. Geometry is pinned to one
retained complete extraction (jurassic_park_geometry.json, rebuilt by build_jurassic_park_geometry.py),
runtime evidence to the retained fresh-state runs (jurassic_park_runtime.json, rebuilt by
jurassic_park_runtime.py). --check regenerates in memory and refuses all drift. External verification
is separate and explicit; bare CI needs no private files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes
from pinmame_game_defs.workspace import pinmame_source_at
from pinmame_flipper_column import flipper_column_inputs, flipper_column_relationships
from jurassic_park_data import (
    AUX_COILS, ASSEMBLY_COILS, DIRECT_DRIVES, FLIPPER_CHART, LAMP_COLUMNS, LAMP_LABEL_OVERRIDES,
    LAMP_LIST_NAMES, LAMP_NAMES, LAMP_ROWS, LASER_KICK_PAIRS, LR_DRIVES, ROM_COIL_NAMES, ROM_LAMP_NAMES,
    ROM_SWITCH_NAMES, SWITCH_COLUMNS, SWITCH_NAMES, SWITCH_PARTS, SWITCH_ROWS, TREX_TEST_LABELS,
    TWO_BULB_LAMPS, DRAWING_TWO_BULB_LAMPS,
)

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.jurassic-park.1993"
STEM = "data-east/jurassic-park-1993"
EXCERPTS = f"evidence/excerpts/{STEM}"
PIN = "pinmame.core.8371478a7640"
MANUAL = "manual.jurassic-park.1993"
TABLE = "vpx-table.jurassic-park.dark-and-friends-1-03"
SCRIPT = "vpx-script.jurassic-park.dark-and-friends-1-03"
CORPUS = "vpx-script.jurassic-park.corpus-1-03"
VPW = "vpx-script.jurassic-park.vpw-1-0"
VBS = "vpm-library.jurassic-park"
CORE_VBS = "vpm-core-library.jurassic-park"
RT_SWITCH = "runtime.jurassic-park.active-switch-test"
RT_LAMP = "runtime.jurassic-park.lamp-test"
RT_COIL = "runtime.jurassic-park.coil-cycle"
RT_LASER = "runtime.jurassic-park.laser-kick-test"
RT_TREX = "runtime.jurassic-park.trex-test"
RUNTIME_REFS = (RT_SWITCH, RT_LAMP, RT_COIL, RT_LASER, RT_TREX)
REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
PIN_FILES = (
    ("core.h", "9d2fa69f7fa6963adc793b272bb5cbfbf94e929c0d7f6b928b1b02a8ee15b2b3",
     "139-165,300-360; FLIP_SWNO and address bands"),
    ("core.c", "84aa5ccddc077b60c1331e32ee13d3d577fd5109d4e7a90001692f737a1c7963",
     "1700-1777,2182-2224,2591; button copies, synthetic outputs, no simData initialization"),
    ("s11.c", "cd1b989ac1eec8c95126e743829a8a3726e76a9b838a29339776d4025d75d2d4",
     "371-410,558-650,870-877,1188-1196; printer, mux, PIA and brightness models"),
    ("sim.c", "20579da60adf58538d5b8c93a0bf22bd8c6d4e3ea6657234cd371293bd05c405",
     "238; simulator-only output 49"),
)
PIN_REFS = (PIN, *(f"pinmame.{name.replace('.', '-')}.8371478a7640" for name, _, _ in PIN_FILES))
DEGAMES_SHA = "4b0b026de796c07dcddd4753c47859c39c08092a1e87739f85a6b9e12a3af1c1"
TABLE_SUBDIR = "data-east/jurassic-park-1993/extractions/de-1.03-dcd0e2e88abe"
TABLE_FILE = "data-east/jurassic-park-1993/tables/de-1.03-dcd0e2e88abe/Jurassic Park (Data East 1993)1.03.vpx"
TABLE_SHA = "dcd0e2e88abe9bf9956e2dba57bd8abd7891a668d49666c22ea0fd2b6e740ba9"
SCRIPT_SHA = "8d5045162f3ad7011e924b424a12123ffc0fcee49c598a8d6b649cd993e21b8b"
EXTRACTION_FILES, EXTRACTION_BYTES = 1045, 151666688
EXTRACTION_MANIFEST = "96b1b1c5488bf15885bf47dfa54920e2e0dd2aeea0a8c23f2fb7c2f596586335"
CORPUS_SHA = "6bf0baeb0dd7098ec3eee893c6bdd76899a227a8c0c021cdae420940ad7b0a00"
CORPUS_FILE = "Jurassic Park (Data East 1993)1.03.vbs"
VPW_SHA = "07d5090461cd2c1f1f0b6e3d71e25a23ad635c10a3b0621dc430afbede510c49"
VPW_FILE = "Jurassic Park (Data East 1993) VPW 1.0.vbs"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
DE_VBS_SHA = "8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04"
CORE_VBS_SHA = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
MANUAL_FILENAME = "Data_East_1993_Jurassic_Park_Manual.pdf"
MANUAL_SHA = "49857ebbca277bcb2539c289cf0b4077225752d9503027cbfe31b880843145fd"
TRANSCRIBER = "primary Sonnet 5.5 curator, 2026-10-01"
GEOMETRY = load_json(ROOT / "tools/jurassic_park_geometry.json")
LEGACY = load_json(ROOT / "tools/jurassic_park_legacy.json")
RUNTIME = load_json(ROOT / "tools/jurassic_park_runtime.json")
MANUAL_PROVENANCE = load_json(ROOT / "tools/jurassic_park_manual_provenance.json")
RUNTIME_PROVENANCE = load_json(ROOT / "tools/jurassic_park_runtime_provenance.json")
OBJECTS = GEOMETRY["objects"]
TREX_SENSORS = {31, 32, 36, 57, 58}
UNUSED_SWITCHES = {n for n in range(1, 65) if SWITCH_NAMES[n - 1] == "Not Used"}
PULSED_SWITCHES = {25, 26, 27, 37, 38, 39, 40, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 59, 60}
INITIAL_ACTIVE_SWITCHES = {9, 10, 11, 12, 13, 14, 36, 57}
MICROSWITCHES = {9, 10, 11, 12, 13, 14, 15, 31, 32, 36, 57, 58, 61}


def prov(*refs: str, status: str = "validated") -> dict:
    # PIN names the controller contract; retain every exact file in its chain.
    expanded = [item for ref in refs for item in
                (PIN_REFS if ref == PIN else (VBS, CORE_VBS) if ref == VBS else (ref,))]
    return {"status": status, "source_refs": list(dict.fromkeys(expanded))}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def place(identifier: str, role: str, name: str, *refs: str, suffix: str = "") -> dict:
    obj = OBJECTS[name]
    return {"id": f"{identifier}.{role}-{(suffix or name).lower()}", "role": role, "space": "playfield",
            "x": obj["xy"][0], "y": obj["xy"][1], "provenance": prov(*refs, status="observed")}


def spatial(identifier: str, role: str, names, *refs: str) -> dict:
    return {"status": "observed",
            "placements": [place(identifier, role, name, *(refs or (TABLE, SCRIPT, MANUAL))) for name in names]}


def legacy(group: str, address: int, fallback: str) -> tuple[str, list]:
    key = str(address) if group == "pinmame.input.switch" else f"{group}:{address}"
    old = LEGACY["inputs" if group == "pinmame.input.switch" else "outputs"].get(key)
    namespace = {"pinmame.input.switch": "pinmame.switch", "pinmame.output.lamp": "pinmame.lamp",
                 "pinmame.output.solenoid": "pinmame.solenoid"}.get(group)
    return (old["id"], old["aliases"]) if old else (
        fallback, [{"namespace": namespace, "value": str(address)}] if namespace else [])


def device(group: str, address: int, label: str, kind: str, availability: str, *refs: str) -> dict:
    identifier, aliases = legacy(group, address, f"{kind}.address-{address}".replace("--", "-minus-"))
    return {"id": identifier, "label": label, "kind": kind,
            "binding": {"group": group, "device": address}, "aliases": aliases,
            "availability": availability, "provenance": prov(*refs)}


def squash(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch.isalnum())


# ---------------------------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------------------------
SWITCH_NOTES = {
    1: "Plumb bob tilt on the cabinet's inside left panel; the manual notes the game has no ball-roll tilt.",
    2: "Printed 4th Coin with no part number; cabinet coin-door column.",
    3: "Credit (Start) push button on the front of the cabinet.",
    7: "Slam tilt in the coin door.",
    15: ("Real seventh trough contact at the release position, not a software-only sensor. The matrix chart "
         "prints Trough #7 Right with part 180-5119-00 while the trough BOM lists one miniature 180-5118-00 "
         "beside twelve subminiature 180-5119-00; the part-number detail is not settled and nothing "
         "in a recreation depends on it."),
    16: ("Shooter lane switch at the foot of the right plunger lane. The retained table binds it to swPLS "
         "(Hit sets 1, UnHit sets 0)."),
    29: ("Raptor pit hole. The ROM's Laser Kick Test fires the raptor-pit coil 9 when this closes; the table "
         "holds the ball in a kicker (sw29) and kicks it out from RaptorKick."),
    35: "Left scoop of the double scoop assembly; the ROM's Laser Kick Test fires coil 4 when it closes.",
    37: ("The ROM names it MIDDLE SCOOP. No coil fires when it closes in the Laser Kick Test: the table "
         "treats it as a gravity trough and only pulses the switch (vpmTimer.PulseSw 37)."),
    41: ("The factory's shooter-gun trigger. The ROM reports LAUNCH BUTTON; the T-REX TEST pulses the jaw "
         "coil 13 when it closes."),
    42: "The shooter gun's smart-bomb button; the manual's rules call it the smart missile, usable once per game.",
    48: ("Mosquito captive ball target; the ROM reports CAPTIVE BALL. The table models the captive ball "
         "as a kicker (Captive) and a hit target."),
    55: ("T-Rex saucer (dino eject cup). Closing it in the Laser Kick Test fires coil 7 (T-REX EJECT). The "
         "table kicks the held ball out when the coil fires and, separately, lets the bending T-Rex lift a ball held in the cup."),
    56: ("The manual's Right Saucer Eject is the ROM's TOP RIGHT EJECT, the table's boat dock; closing it in "
         "the Laser Kick Test fires coil 1."),
    59: ("Trough exit switch (the manual's T.Rex Trough, part 180-5057-00). No coil follows it; the table pulses it when a "
         "ball passes (vpmTimer.PulseSw 59)."),
    60: ("Trough exit switch of the right scoop (ROM: RIGHT SCOOP). No coil follows it; the table pulses it "
         "(vpmTimer.PulseSw 60)."),
    61: "Right vertical up-kicker. The Laser Kick Test fires coil 5 (twice, a retry) when it closes.",
}
ROM_DIFFERENCE_NOTES = {
    42: "The manual prints Smart Bomb Button; the ROM displays SMART MISSILE.",
    48: "The manual prints Mosquito Captive Ball; the ROM displays CAPTIVE BALL.",
    49: "The manual prints Baryonyx Target; the ROM displays BARYONYX.",
    50: "The manual prints Gallimimus Target; the ROM displays GALLIMIMUS.",
    52: "The manual prints Triceritops Target (and 'Triceritop' in the matrix); the ROM displays TRICERATOPS.",
    56: "The manual prints Right Saucer Eject; the ROM displays TOP RIGHT EJECT.",
    55: "The manual prints T.Rex Saucer Eject; the ROM displays T-REX EJECT.",
    57: "The manual prints T.Rex Top (Up); the ROM displays T-REX UP.",
    58: "The manual prints T.Rex Bottom (Down); the ROM displays T-REX DOWN.",
    37: "The manual prints Center Scoop; the ROM displays MIDDLE SCOOP.",
    60: "The manual prints Right Scoop Trough; the ROM displays RIGHT SCOOP.",
    41: "The manual prints Launch Trigger; the ROM displays LAUNCH BUTTON.",
}


def switch_placement(address: int, identifier: str) -> dict | None:
    if address in TREX_SENSORS:
        return {"status": "observed", "placements": [{
            "id": f"{identifier}.sensor-trex-pivot", "role": "sensor", "space": "playfield",
            "x": OBJECTS[GEOMETRY["mechanisms"]["trex-pivot"]]["xy"][0],
            "y": OBJECTS[GEOMETRY["mechanisms"]["trex-pivot"]]["xy"][1],
            "provenance": prov(TABLE, SCRIPT, MANUAL, status="observed")}]}
    name = GEOMETRY["switches"].get(str(address))
    return spatial(identifier, "sensor", [name]) if name else None


def inputs() -> list:
    records = []
    for address, label in enumerate(SWITCH_NAMES, 1):
        unused = label == "Not Used"
        refs = (MANUAL, PIN, SCRIPT, RT_SWITCH)
        d = device("pinmame.input.switch", address, label, "switch",
                   "unused" if unused else "used", *refs)
        col, row = divmod(address - 1, 8)
        drive, drive_pin, transistor = SWITCH_COLUMNS[col]
        ret, ret_pin = SWITCH_ROWS[row]
        d["wiring"] = {"board": "CPU", "drive_wire": drive, "drive_connection": drive_pin,
                       "driver_transistor": transistor, "return_wire": ret, "return_connection": ret_pin}
        part = SWITCH_PARTS[address - 1]
        physical = {"notes": f"Factory switch matrix column {col + 1}, row {row + 1}; the ROM's Active Switch "
                             f"Test displays {ROM_SWITCH_NAMES[address - 1]} {drive} {ret} #{address:02d}."}
        if unused:
            d["spatial"] = na("unused", MANUAL, RT_SWITCH)
            physical["notes"] += " Factory prints Not Used and the ROM still names the address NOT USED; no contact is fitted."
        else:
            d["normally_closed"] = False
            d["pulse"] = address in PULSED_SWITCHES
            if address in INITIAL_ACTIVE_SWITCHES:
                d["initial_active"] = True
            if part not in {"-", "See Cabinet"}:
                physical["part_number"] = part
            if address in MICROSWITCHES:
                physical["switch_type"] = "microswitch"
            physical["notes"] += (
                " Public 1 is the active closure: the ROM names the switch while the host holds the address at 1, "
                "the Data East matrix read is uncomplemented and the driver's invSw is zero. Do not reinvert.")
        if address in ROM_DIFFERENCE_NOTES:
            physical["notes"] += " " + ROM_DIFFERENCE_NOTES[address]
        if address in SWITCH_NOTES:
            physical["notes"] += " " + SWITCH_NOTES[address]
        if address in {9, 10, 11, 12, 13, 14}:
            physical["notes"] += (" Six balls rest on 9-14; the retained table starts them closed (bsTrough.Initsw 0,14,13,12,11,10,9,0, Balls = 6). "
                                  "No table object models the individual trough contacts, so none is placed.")
        if address in TREX_SENSORS:
            physical["notes"] += (
                f" The ROM's T-REX TEST prints ON beside {TREX_TEST_LABELS[address]} when this address is held at 1. "
                "The retained table writes it from its T-Rex position model and starts the toy homed with 36 and 57 "
                "closed (Init_Trex). The ROM's boot T-Rex diagnostic depends on it: with both closed it drives the up/down motor, then "
                "pulses the rotation motor, jaw and direction relay; with them open it drives the up/down motor for about 3.4 s and "
                "starts nothing else (coil-cycle and coil-cycle-trex-homed boot events).")
            physical["notes"] += " Placement projects the sensor onto the T-Rex pivot (TrexPlastic), the toy's fixed object."
        d["physical"] = physical
        if address in CABINET_ONLY:
            d["spatial"] = na("cabinet_or_service", MANUAL, PIN)
        elif not unused:
            placement = switch_placement(address, d["id"])
            if placement:
                d["spatial"] = placement
                if address not in TREX_SENSORS:
                    d["physical"]["notes"] += (f" Geometry anchor: {GEOMETRY['switches'][str(address)]}; it is the object the "
                                               "script's own handler binds, a sensor location on the named mechanism.")
        if address in {63, 64}:
            d["physical"]["notes"] += (
                f" ROM-readable copy only; direct writes are overwritten by core_updateSw. A consumer drives host button "
                f"{84 if address == 63 else 82}. The ROM names this address {ROM_SWITCH_NAMES[address - 1]} while the "
                "cabinet button is held; the cabinet leaf switches are 180-5048-01 (left) and 180-5022-00 (right) in the switch list, while the cabinet "
                "parts list prints 15 Left Flipper Leaf Switch 180-5048-01 and 15a Right Flipper Leaf Switch 180-5122-00 (marked not shown).")
            d["provenance"] = prov(MANUAL, PIN, VBS, RT_SWITCH)
        records.append(d)
    for address, label in [(-7, "Black Advance"), (-6, "Green Up/Down Toggle")]:
        d = device("pinmame.input.switch", address, label, "switch", "used", PIN, MANUAL)
        d["spatial"] = na("cabinet_or_service", PIN, MANUAL)
        d["physical"] = {"switch_type": "button", "notes": (
            "DE_COMPORTS named keyboard port: Black is momentary; Green toggles service "
            "direction on a press edge. Use named keys; do not substitute persistent matrix writes.")}
        d["pulse"] = address == -7
        records.append(d)
    records.extend(flipper_column_inputs(
        flip_swno=(63, 64), flip_swno_text="FLIP6364 (FLIP_SWNO(63,64))",
        core_refs=PIN_REFS, button_refs=(VBS, CORE_VBS, SCRIPT, RT_SWITCH),
        button_notes={
            "left": "The ROM's Active Switch Test names matrix 63 LEFT FLIPPER while this button is held.",
            "right": "The ROM's Active Switch Test names matrix 64 RIGHT FLIPPER while this button is held; the same button also operates the upper right flipper.",
        },
        unused_notes={88: "No upper staged control exists: the upper right flipper follows the right button."},
        unused_note_refs=(VBS, CORE_VBS, SCRIPT),
    ))
    records.append({
        "id": "dip.country", "label": "Country select (PinMAME dip 0)", "kind": "dip_switch",
        "availability": "used", "binding": {"group": "pinmame.input.dip", "device": 0},
        "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
        "spatial": na("dip_switch", PIN),
        "physical": {"switch_type": "dip", "notes": "pia2a_r reads core_getDip(0)<<7; the Jurassic Park driver uses the shared Data East input ports."},
        "provenance": prov(PIN),
    })
    return records


CABINET_ONLY = {1, 2, 3, 4, 5, 6, 7, 8, 41, 42, 63, 64}


# ---------------------------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------------------------
LR_BY_DRIVE = {row[0]: row for row in LR_DRIVES}
DIRECT_BY_DRIVE = {row[0]: row for row in DIRECT_DRIVES}
AUX_BY_COIL = {row[0]: row for row in AUX_COILS}
HIGH_VOLTAGE_DRIVES = {3, 5, 9}
RELAY_DRIVES = {10, 11, 12, 14, 15}
COIL_OBJECT_EFFECTS = {int(n): name for n, name in GEOMETRY["coils"].items()}
SOLENOID_KIND = {13: "coil", 16: "coil", 22: "motor"}

SOLENOID_NOTES = {
    1: ("The ROM's cycle test names it TOP RGT EJECT; the retained table calls it the boat-dock eject (switch 56) "
        "and the Laser Kick Test fires it when 56 closes."),
    2: "Releases the staged seventh ball from the trough to the shooter lane (the retained table's TroughRelease).",
    3: ("The ROM names it AUTO LAUNCH 50V. Its drive passes through PPB board transistor Q5 (TIP security, J8). "
        "The schematic's box prints +32 VL, but the coil is wired at J7 where the 50 VDC rail enters, and the PPB "
        "fuse chart puts F5 on 'Flipper Power & 50Volt coils'."),
    4: "Left scoop of the double scoop; the Laser Kick Test fires it when switch 35 closes.",
    5: ("Right VUK, driven through PPB board transistor Q3 (TIP security, J8) from the 50 V rail like coil 3. The "
        "Laser Kick Test fires it twice (a retry) when switch 61 closes."),
    6: ("The right ramp's diverter (ROM: RAMP DIVERTER). The retained table drops the diverter wall (IsDropped) and rotates "
        "the arm while the coil is on."),
    7: "T-Rex saucer eject (ROM: T-REX EJECT); the Laser Kick Test fires it when switch 55 closes.",
    8: "Cabinet knocker (ROM: KNOCKER); the table plays a knocker sound.",
    9: ("Raptor pit kicker, +50 VDC at PPB J7-3 through board transistor Q4 (TIP security). The playfield major-assembly "
        "drawing (printed page 33) puts item 1, Kickback Assy 500-5081-00, on the raptor pit, where the unique-parts page lists "
        "coil 23-800 (090-5001-01); the schematic prints type 23-840. The Laser Kick Test fires it when switch 29 closes."),
    10: ("The PPB board's left/right coil relay (terminals 9 and 7 on the schematic): asserted it routes drives 1-8 to the right-hand flash lamp banks "
         "(public 25-32), released to the left-hand coils (public 1-8). PinMAME's muxSol is 10, so its output "
         "layer republishes drives 1-8 as 25-32 while 10 is on. The retained table leaves 10 unbound."),
    11: ("General-illumination relay K-1 on the power supply board. The retained table asserts GIRelay(1) to switch the "
         "playfield GI off and releases it to restore GI, i.e. the relay's asserted state cuts GI. PinMAME models it as "
         "a reversed #44 6.3 VAC brightness output. Detail A of the game illustration shows four 5A slow-blow GI "
         "fuses on the PPB board: F1 Playfield, F2 Backbox Door & Speaker Panel, F3 Playfield & Coin Door, F4 Backbox "
         "Door; neither the manual nor the table gives a count of fitted GI sockets."),
    12: ("T-Rex rotation direction relay (ROM: RELAY: MOTOR L/R). The T-REX TEST latches it on for a right-flipper "
         "press and leaves it off for the left; it is only a direction select for motor 15."),
    13: ("T-Rex jaw coil (ROM: T-REX MOUTH); the T-REX TEST pulses it when the launch trigger (41) closes. Dino "
         "assembly BOM lists coil 25-1240 (090-5034-00)."),
    14: ("T-Rex up/down motor relay (ROM: RELAY: MOTOR UP/DWN) on relay board 520-5010-00, which the schematic feeds 28 VAC from BR2 "
         "(the Dino BOM lists a 24 VAC Bowman 11 RPM motor for the bend). The CYCLING COILS test prints the name without a public "
         "transition; the T-REX TEST's Start press and the boot diagnostic drive it."),
    15: ("T-Rex rotation motor on/off relay (ROM: RELAY: MOTOR ON/OFF) through bi-directional relay board 520-5066-00; "
         "the T-REX TEST's flipper presses pulse it. The schematic prints a 9 VDC motor and the Dino BOM a 5 VDC "
         "multi-purpose motor (041-5025-00); that wiring detail does not change the control contract."),
    16: ("Trough lock-out (ROM: LOCK OUT), Lock Ball Assembly 500-5684-00 with coil 25-1240 (090-5034-00): the retained "
         "table's TroughLockout moves one ball from the six-ball stack to the staged seventh position."),
    17: "Top turbo bumper coil (ROM: TOP TURBO).", 18: "Left turbo bumper coil (ROM: LEFT TURBO).",
    19: "Right turbo bumper coil (ROM: RIGHT TURBO).", 20: "Left slingshot coil (ROM: LEFT SLING).",
    21: "Right slingshot coil (ROM: RIGHT SLING).",
    22: ("Cabinet shaker motor (ROM: SHAKER MOTOR). The printed auxiliary row gives power VIO-YEL J7-3 and a 23-800 type, which the "
         "drawing on PDF 55 (printed page 51) contradicts: it shows a 12VDC cabinet shaker motor with a 1/2 to 1 ohm resistor fed from power supply "
         "CN1 pins 11 (GRY) and 10 (GRY-GRN), 9VAC through 2.5A fuses and 1N5404 diodes, switched by the BLU-BLK control line. The structured "
         "wiring follows the drawing."),
}


def coil_device(address: int) -> dict:
    refs = (MANUAL, PIN, SCRIPT, RT_COIL)
    if address in LR_BY_DRIVE:
        n, name, rom, transistor, pin, control, coil_wire, flash_wire, bulbs, rom_fl = LR_BY_DRIVE[address]
        d = device("pinmame.output.solenoid", address, name, "coil", "used", *refs)
        high = address in HIGH_VOLTAGE_DRIVES
        d["wiring"] = {"board": "CPU", "driver_transistor": transistor, "control_wire": control,
                       "control_connection": f"CPU {pin} to PPB J1-{n}",
                       "power_wire": "YEL-VIO" if high else "BRN",
                       "power_connection": "PPB J7-8/9" if high else "PPB J6-3",
                       "nominal_voltage_v": 50 if high else 32, "voltage_type": "dc"}
        physical = {"quantity": 1}
        if address in ASSEMBLY_COILS:
            assembly, printed, part = ASSEMBLY_COILS[address]
            physical.update(part_number=part, assembly_part_number=assembly)
            physical["notes"] = (f"Left-set coil of drive {n}: coil lead {coil_wire}; ROM cycle test name {rom}. "
                                 f"Assembly {assembly} lists coil {printed} ({part}); the schematic prints the generic "
                                 "type 23-840 for the whole left set, which the unique-parts pages supersede.")
        else:
            physical["part_number"] = "23-840"
            physical["notes"] = (f"Left-set coil of drive {n}: coil lead {coil_wire}; ROM cycle test name {rom}. The "
                                 "schematic prints coil type 23-840 and no unique-parts page names this assembly.")
        physical["notes"] += " " + SOLENOID_NOTES[address]
        d["physical"] = physical
        if address in COIL_OBJECT_EFFECTS:
            d["spatial"] = spatial(d["id"], "effect", [GEOMETRY["coils"][str(address)]])
            d["physical"]["notes"] += " Placement projects the coil's effect onto its mechanism object, not a winding centre."
        elif address == 8:
            d["spatial"] = na("cabinet_or_service", MANUAL)
        return d
    if address in DIRECT_BY_DRIVE:
        n, name, rom, transistor, pin, wire, switches = DIRECT_BY_DRIVE[address]
        kind = "relay" if address in RELAY_DRIVES else SOLENOID_KIND.get(address, "coil")
        d = device("pinmame.output.solenoid", address, name, kind, "used", *refs)
        d["wiring"] = {"board": "CPU", "driver_transistor": transistor, "control_wire": wire,
                       "control_connection": pin}
        if address in HIGH_VOLTAGE_DRIVES:
            d["wiring"].update(power_wire="VIO/YEL", power_connection="PPB J7-3",
                               nominal_voltage_v=50, voltage_type="dc")
        elif address in (13, 16):
            d["wiring"].update(power_wire="RED", power_connection="PS CN3-6/7/8", nominal_voltage_v=32, voltage_type="dc")
        d["physical"] = {"quantity": 1, "notes": f"{name}: {switches}. ROM cycle test name: {rom}. " + SOLENOID_NOTES[address]}
        if address in ASSEMBLY_COILS:
            assembly, printed, part = ASSEMBLY_COILS[address]
            d["physical"].update(part_number=part, assembly_part_number=assembly)
        if address in COIL_OBJECT_EFFECTS:
            d["spatial"] = spatial(d["id"], "effect", [GEOMETRY["coils"][str(address)]])
            d["physical"]["notes"] += " Placement projects the coil's effect onto its mechanism object, not a winding centre."
        elif address in (10, 11):
            d["spatial"] = na("internal_nonvisual", MANUAL, PIN)
        elif address in (12, 14, 15):
            d["spatial"] = {"status": "observed", "placements": [{
                "id": f"{d['id']}.effect-trex-pivot", "role": "effect", "space": "playfield",
                "x": OBJECTS[GEOMETRY["mechanisms"]["trex-pivot"]]["xy"][0],
                "y": OBJECTS[GEOMETRY["mechanisms"]["trex-pivot"]]["xy"][1],
                "provenance": prov(TABLE, SCRIPT, MANUAL, status="observed")}]}
            d["physical"]["notes"] += " Placement projects the control onto the T-Rex pivot (TrexPlastic), the toy's fixed object."
        elif address == 13:
            d["spatial"] = {"status": "observed", "placements": [{
                "id": f"{d['id']}.effect-trex-jaw", "role": "effect", "space": "playfield",
                "x": OBJECTS[GEOMETRY["mechanisms"]["trex-jaw"]]["xy"][0],
                "y": OBJECTS[GEOMETRY["mechanisms"]["trex-jaw"]]["xy"][1],
                "provenance": prov(TABLE, SCRIPT, MANUAL, status="observed")}]}
            d["physical"]["notes"] += " Placement is the T-Rex jaw primitive (TrexJaw), the toy the coil moves."
        elif address in (16,):
            pass
        return d
    n, name, control, connection, power_wire, power_connection, transistor, coil_type = AUX_BY_COIL[address]
    kind = SOLENOID_KIND.get(address, "coil")
    d = device("pinmame.output.solenoid", address, name.replace(" (See Schematic)", ""), kind, "used", *refs)
    d["wiring"] = {"board": "CPU", "driver_transistor": transistor, "control_wire": control,
                   "control_connection": connection, "power_wire": power_wire, "power_connection": power_connection,
                   "nominal_voltage_v": 32, "voltage_type": "dc"}
    if address == 22:
        # PDF 55 (printed 51) draws the cabinet shaker motor as 12VDC fed from PS CN1 pins 11 (GRY) and 10 (GRY-GRN), 9VAC through
        # fuses and diodes; the printed auxiliary row's VIO-YEL J7-3 and 23-800 were copied from the neighbouring coils.
        d["wiring"].update(power_wire="GRY / GRY-GRN", power_connection="PS CN1-11 / CN1-10 (9VAC, fused and rectified)",
                           nominal_voltage_v=12, voltage_type="dc")
    d["physical"] = {"quantity": 1}
    if address in ASSEMBLY_COILS:
        assembly, printed, part = ASSEMBLY_COILS[address]
        d["physical"].update(part_number=part, assembly_part_number=assembly)
        d["physical"]["notes"] = (f"Auxiliary solenoid driven straight from the CPU board. The printed table gives coil type "
                                  f"{coil_type}; assembly {assembly} lists {printed} ({part}). " + SOLENOID_NOTES[address])
    else:
        d["physical"]["assembly_part_number"] = "500-5228-00"
        d["physical"]["notes"] = ("Shaker motor assembly 500-5228-00 on motor board 520-5065-00. " + SOLENOID_NOTES[address])
    if address in COIL_OBJECT_EFFECTS:
        d["spatial"] = spatial(d["id"], "effect", [GEOMETRY["coils"][str(address)]])
        d["physical"]["notes"] += " Placement projects the coil's effect onto its mechanism object, not a winding centre."
    else:
        d["spatial"] = na("cabinet_or_service", MANUAL)
    return d


def flasher_device(address: int) -> dict:
    drive = address - 24
    n, name, rom, transistor, pin, control, coil_wire, flash_wire, bulbs, rom_fl = LR_BY_DRIVE[drive]
    d = device("pinmame.output.solenoid", address, f"Flash Lamps {drive}R ({rom_fl[4:]})", "flasher", "used",
               MANUAL, PIN, SCRIPT, RT_COIL)
    d["wiring"] = {"board": "CPU", "driver_transistor": transistor, "control_wire": control,
                   "control_connection": f"CPU {pin} to PPB J1-{n}", "power_wire": "ORG",
                   "power_connection": "PPB J6-4/5 (+32 VR)", "nominal_voltage_v": 32, "voltage_type": "dc"}
    d["physical"] = {
        "quantity": 4, "location": f"{bulbs.lower()} (printed schematic)",
        "notes": (f"Right-set bank {drive}R: four bulbs on lead {flash_wire}, supplied from PPB J6-4/5 (+32 VR) through "
                  f"drive {drive}'s resistor path; printed bulb text {bulbs}; ROM cycle test name {rom_fl}. Public {address} "
                  f"is drive {drive} republished while the left/right relay (10) is on; the bulb type is not printed in the "
                  "manual's bank schematic, so none is asserted (PinMAME models #89 32 VDC brightness for 25-32). "
                  "Quantity counts the schematic's four bulb symbols per bank, which include backbox and insert bulbs; only the "
                  "playfield bulbs are placed."),
    }
    if address == 25:
        d["physical"]["notes"] += (" The ROM text counts 2 raptor bulbs and 1 insert bulb and the PDF 34 location drawing shows two playfield "
                                   "1R locations, where the schematic draws 3 raptor bulbs and 1 insert: the quantity of 4 is the schematic's "
                                   "and is disputed (conflict.flash-bank-1r-bulb-count).")
    if address == 28 or address == 29:
        d["physical"]["notes"] += (" The ROM names the six right-ramp flash lamps 1.3.5 (this bank) and 2.4.6 (the other); "
                                   "the schematic's upper-right-playfield bulbs are those ramp bulbs.")
    if address == 31:
        d["physical"]["notes"] += " The ROM splits the four bulbs as three by the pop bumpers and one T-Rex bulb."
    names = GEOMETRY["flashers"].get(str(address))
    if names:
        d["spatial"] = {"status": "observed", "placements": [
            place(d["id"], "emitter", name, TABLE, SCRIPT, MANUAL) for name in names]}
        d["physical"]["notes"] += (f" Spatial: {len(names)} playfield bulb position{'s' if len(names) > 1 else ''} taken from the "
                                   f"script-driven Light object{'s' if len(names) > 1 else ''} {', '.join(names)}, never a glow, "
                                   "reflection or shadow twin.")
    return d


VIRTUAL_NAMES = {
    23: "Game-on / switched-solenoid enable (AC relay)", 24: "Unimplemented S11 bit 24",
    33: "Unimplemented upper-right power alias", 34: "Unimplemented upper-right hold alias",
    35: "Unimplemented upper-left power alias", 36: "Unimplemented upper-left alias",
    45: "Synthetic lower-right power state", 46: "Synthetic lower-right combined state",
    47: "Synthetic lower-left power state", 48: "Synthetic lower-left combined state",
    49: "Shared simulator shooter-release signal", 50: "Reserved pre-custom gap",
}


def virtual_device(address: int) -> dict:
    meaningful = address in {23, 45, 46, 47, 48}
    label = VIRTUAL_NAMES.get(address, f"Unused output {address}")
    if 37 <= address <= 44:
        label = f"Raw printer line bit {address - 37}"
    d = device("pinmame.output.solenoid", address, label, "virtual",
               "used" if meaningful else ("unknown" if 37 <= address <= 44 else "unused"), PIN)
    d["spatial"] = na("virtual", PIN)
    d["physical"] = {"notes": (
        "Public compatibility namespace, not a fitted winding. Jurassic Park publishes 32 solenoids and no custom "
        "solenoids (hw.custSol 0), so 51-64 return zero. The shared core has no Data East upper 33-36 return and 50 is "
        "a gap; the matrix and PIA writers never set bit 24.")}
    if address == 23:
        d["physical"]["notes"] = (
            "The switched-solenoid / game-on enable PinMAME passes to core_updateSw as locals.ssEn. The ROM raises it when a "
            "service test enables outputs and the retained table ties its nudge logic to it (SolCallback(23) = "
            "RelayAC -> vpmNudge.SolGameOn). Every service-test run waits on it before stimulus.")
        d["provenance"] = prov(PIN, SCRIPT, MANUAL, RT_SWITCH, RT_LASER)
    if 37 <= address <= 44:
        d["physical"]["notes"] = (
            f"Raw printer-line transport bit {address - 37}: the driver sets S11_PRINTERLINE, so PinMAME publishes the CPU "
            "board's printer byte here (non-inverted, s11.c). The ROM carries a PRINT OUT feature string, but the manual "
            "(searched through its OCR text) documents no printer connector or device and no run observed a transition; whether the byte can reach a "
            "fitted device is not settled, so the address stays unknown.")
        d["provenance"] = prov(PIN, MANUAL, status="unknown")
    if 45 <= address <= 48:
        d["physical"]["notes"] = (
            "core_updateSw fabricates button-derived lower-flipper states while 23 enables the game; 46/48 combine power "
            "or hold. The Active Switch Test runs show the host left button producing 47/48 and the right button 45/46. "
            "These have no independent physical quantity and are not four fitted coils.")
        d["provenance"] = prov(PIN, RT_SWITCH)
    if address == 49:
        d["physical"]["notes"] = (
            "Shared core reserves simulated manual-shooter release at 49. Jurassic Park has no simData and therefore never "
            "publishes meaningful shooter state here in a fresh run.")
    return d


def lamp_device(address: int) -> dict:
    manual = LAMP_NAMES[address - 1]
    label = LAMP_LABEL_OVERRIDES.get(address, manual)
    d = device("pinmame.output.lamp", address, label, "lamp", "used", MANUAL, PIN, SCRIPT, RT_LAMP)
    col, row = divmod(address - 1, 8)
    wire, pin, transistor = LAMP_COLUMNS[col]
    ret, ret_pin, ret_q = LAMP_ROWS[row]
    d["wiring"] = {"board": "CPU", "drive_wire": wire, "drive_connection": pin, "driver_transistor": transistor,
                   "return_wire": ret, "return_connection": ret_pin, "return_component": ret_q}
    quantity = 2 if address in TWO_BULB_LAMPS | DRAWING_TWO_BULB_LAMPS else 1
    rom = ROM_LAMP_NAMES[address - 1]
    notes = (f"Factory lamp matrix column {col + 1}, row {row + 1}; the ROM's single-lamp test displays {rom} {wire} {ret} "
             f"#{address:02d} while only this lamp is lit.")
    if address in LAMP_LABEL_OVERRIDES:
        notes += {
            6: " The matrix chart and location list print only the word Map; the ROM names it BARYONYX - MAP, the sixth species map.",
            20: (" The manual prints Raptor Multi-Million; the ROM displays MOSQUITO MULTI MIL. and the table's playfield "
                 "artwork prints MULTI MOSQUITO MILLIONS in the computer grid, which is the game's Mosquito Millions round "
                 "(rule 18). The printed name is a misprint."),
            30: (" The manual prints Jackpot Map; the ROM displays JACKPOT RAMP, and the rules light the Jackpot for the "
                 "helicopter loop (29) and the ramp (30), so no map jackpot exists. The printed name is a misprint."),
            48: (" The matrix chart and location list print \"C\" Arch; the ROM displays ARCH \"E\", which completes the "
                 "T-R-E-X arch letters 2, 47, 48 and 60. The printed letter is a misprint."),
            50: " The matrix chart prints only #2 here; the ROM names it GALLIMIMUS, the second target-species lamp after Baryonyx Target (49).",
        }[address]
    elif squash(manual) != squash(rom):
        notes += f" The manual prints {manual}."
    if address == 19:
        notes += " The ROM spells it HELIPAD X2 where the manual prints Helo."
    if address == 37:
        notes += " The ROM names it PLFD T-REX X2 where the manual prints T-Rex Map; the table models one light for it and omits the second."
    if address == 64:
        notes += " The manual prints Smart Bomb X2; the ROM names it SMART MISSILE X2."
    if address in TWO_BULB_LAMPS:
        notes += " The printed lamp list marks it (2 Bulbs)."
    if address in DRAWING_TWO_BULB_LAMPS:
        notes += (" The printed lamp list does not mark it (2 Bulbs), but the PDF 33 location drawing shows two separate 37 locations and "
                  "the ROM names it PLFD T-REX X2.")
    d["physical"] = {"quantity": quantity, "notes": notes}
    names = GEOMETRY["lamps"].get(str(address))
    if address == 9:
        d["spatial"] = na("cabinet_or_service", MANUAL)
        d["physical"]["notes"] += " The credit-button lamp is in the cabinet's front button, not on the playfield."
    elif names:
        d["spatial"] = {"status": "observed", "placements": [
            place(d["id"], "emitter", name, TABLE, SCRIPT, MANUAL) for name in names]}
        d["physical"]["notes"] += (f" Spatial: {', '.join(names)} - the script-driven Light object{'s' if len(names) > 1 else ''} "
                                   "UpdateLamps binds to this lamp, not its glow or halo twins.")
        if quantity > len(names):
            d["physical"]["notes"] += f" The table models {len(names)} of the {quantity} printed bulbs."
    else:
        d["physical"]["notes"] += (" No bulb of its own is modelled: the table lights this lamp with a coloured glow light only, "
                                   "which is not a bulb position, so no placement is claimed.")
    if address in (31, 32, 62):
        d["physical"]["notes"] += (" The retained table also flashes this turbo-bumper bulb from the bumper's solenoid "
                                   f"callback (SetLamp {address}); that is a table effect, the ROM drives the lamp.")
    return d


def outputs() -> list:
    records = []
    for address in range(1, 65):
        if address <= 22:
            records.append(coil_device(address))
        elif 25 <= address <= 32:
            records.append(flasher_device(address))
        else:
            records.append(virtual_device(address))
    for address in range(1, 65):
        records.append(lamp_device(address))
    return records


# ---------------------------------------------------------------------------------------------
# Mechanisms
# ---------------------------------------------------------------------------------------------
def mechanisms(ins: list, outs: list) -> list:
    sw = {d["binding"]["device"]: d["id"] for d in ins if d["binding"]["group"] == "pinmame.input.switch"}
    sol = {d["binding"]["device"]: d["id"] for d in outs if d["binding"]["group"] == "pinmame.output.solenoid"}
    rows = [
        ("trough", "Six-ball trough, lock-out and release", "kicker", [16, 2], list(range(9, 16)),
         "500-5683-00",
         "Six balls rest on the trough switches 9-14 and the seventh contact, 15, is the staged release position. The "
         "6 Ball Outhole-Trough assembly (printed page 71) pairs a switch assembly 500-5683-00 with a Lock Ball "
         "Assembly 500-5684-00: coil 16 (25-1240) pulls the lock ball plunger to let one ball from the stack onto the "
         "release position, and coil 2 ejects that ball to the shooter lane. The retained table starts 9-14 closed "
         "with six balls, moves one ball to 15 on every TroughLockout and kicks it out on TroughRelease. The ROM's "
         "ball search and missing-ball handling were not exercised."),
        ("shooter-lane", "Shooter lane and auto launch", "kicker", [3], [16], "500-5477-00",
         "Coil 3 (50 V, Ball Launch assembly 500-5477-00, coil 23-800) kicks the ball up the right shooter lane; switch 16 "
         "senses a ball at the foot of the lane. The retained table's Autofire fires its Plunger1 on the coil. The "
         "launch trigger (41) belongs to the gun, not to this lane."),
        ("shooter-gun", "Shooter gun (launch trigger and smart-bomb button)", "other", [], [41, 42], "500-5673-00",
         "The cabinet's Shooter Gun Assy (cabinet parts item 1, 500-5673-00): a trigger switch (180-5111-00, ROM "
         "LAUNCH BUTTON) used for the skill shot and for stunning dinosaurs, and a smart-bomb button (515-5825-00, ROM "
         "SMART MISSILE) usable once per game. The retained table maps both to host keys. In the ROM's T-REX TEST the "
         "trigger pulses the jaw coil (13)."),
        ("t-rex", "T-Rex dinosaur (rotation, bend and jaw)", "motorized", [12, 13, 14, 15], [31, 32, 36, 57, 58],
         "500-5667-00",
         "Dino Assembly (printed page 70, 500-5667-00): a rotation motor (BOM item 1: 5 VDC motor; the coil schematic prints a "
         "9 VDC motor behind bi-directional relay board 520-5066-00), a Bowman 11 RPM 24 VAC motor for the up/down bend "
         "(item 19, relay board 520-5010-00), a jaw coil 25-1240, four micro switches 180-5040-00 and a roller micro switch "
         "180-5123-00. Public 12 selects the rotation direction, 15 switches the rotation motor and 14 the up/down "
         "motor. Switches: 57 TOP (up), 58 BOTTOM (down), 36 CENTER (rotation), 31 RIGHT and 32 LEFT, "
         "displayed by the ROM's T-REX TEST as ON when held at public 1. The manual's T-Rex test says Top must be ON "
         "to move left and right and Center ON to move up and down. The ROM runs a power-up T-Rex diagnostic: with 36 "
         "and 57 closed it drives 14 for about 3 s, then pulses 15, the jaw 13 and the direction relay 12; with them open it "
         "drives 14 for about 3.4 s and starts nothing else. In the T-REX TEST (57 held closed) the left flipper button pulses 15 alone, the "
         "right button latches 12 and pulses 15, Start pulses 14 (with or without 36 closed) and the launch trigger pulses "
         "13; the ROM did not wait for 36 before moving up and down in this run. The retained table integrates positions from the motor outputs: 57 is closed when the head is raised, "
         "58 when bent forward, 31 and 32 at the rotation limits (-23 and -3 degrees) and 36 near -13; it starts homed with "
         "36 and 57 closed. Those thresholds are the table's model, not measured contact positions."),
        ("t-rex-eject", "T-Rex saucer (dino eject)", "kicker", [7], [55], "500-5665-00",
         "Ball Eject Assy (Dino) 500-5665-00 with coil 27-1500 (090-5004-02). Coil 7 (ROM T-REX EJECT) ejects the ball "
         "held on switch 55; the ROM's Laser Kick Test fires it when 55 closes. In the rules the dinosaur 'eats' the "
         "ball here to score Feed T-Rex. The retained table lets the bending T-Rex pick the ball up from 55 and "
         "release it at the top, which is its own animation of that feature."),
        ("double-scoop", "Double scoop (left scoop and center scoop)", "kicker", [4], [35, 37], "515-5772-00",
         "Double Scoop Sub-Assembly 515-5772-00 with coil 23-800 and micro switch 180-5116-00; the playfield major-assembly "
         "drawing shows two of them, at the left scoop and beside the center scoop. Coil 4 ejects the ball held in the left "
         "scoop, switch 35 (the Laser Kick Test fires 4 when 35 closes). The center scoop's switch 37 (ROM MIDDLE SCOOP, part "
         "500-5442-01) fires no coil in the Laser Kick Test and the retained table treats it as a gravity path."),
        ("top-right-eject", "Top right eject (boat dock)", "kicker", [1], [56], "500-5664-00",
         "Ball Eject Assy (Saucer) 500-5664-00, coil 24-940 (090-5636-02); ROM TOP RGT EJECT. The Laser Kick Test fires it when "
         "switch 56 closes. The rules light it for Two Ball Play, Lite Extra Ball and the Escape Isla Nublar boat dock."),
        ("right-vuk", "Right vertical up-kicker", "kicker", [5], [61], "500-5116-04",
         "Super VUK 500-5116-04 with coil 23-800 (090-5001-01) and micro switch 180-5064-00 (the ROM calls the coil RIGHT VUK 50V "
         "and the schematic wires it at the 50 V J7 connector). The Laser Kick Test fires it, twice, when 61 closes."),
        ("raptor-pit", "Raptor pit kicker", "kicker", [9], [29], "500-5081-00",
         "Kickback Assy 500-5081-00 (coil 23-800 per its unique-parts page) is the raptor pit's kicker: a 50 V coil (ROM RAPTOR PIT 50V, "
         "schematic type 23-840, drive 9 through board transistor Q4) that kicks the ball "
         "out of the raptor pit sensed by switch 29. The ROM's Laser Kick Test ('put ball in raptors') fires it when 29 "
         "closes. The rules mention a ball-freeze protector that kicks while the danger lamp is on."),
        ("ramp-diverter", "Right ramp and diverter", "diverter", [6], [33, 34], "500-5661-00",
         "Diverter Plunger & Crank Arm Assembly 500-5661-00 (coil 27-1500, 090-5004-02) with the 515-5781-00 diverter arm "
         "steers balls at the right ramp, whose enter (33) and exit (34) switches count shots. The retained table drops the "
         "diverter's collision wall and rotates its arm while the coil is on. The ramp switches report ball passage, not "
         "diverter position; no home or limit sensor is fitted in the switch chart."),
        ("scoop-exits", "Gravity scoop exits (T-Rex trough and right scoop)", "other", [], [59, 60], None,
         "Switches 59 (T.Rex Trough) and 60 (Right Scoop Trough), both part 180-5057-00, sit in exit paths. Closing either in the "
         "Laser Kick Test fired no coil, and the retained table only pulses them as a ball passes."),
        ("captive-ball", "Mosquito captive ball", "toy", [], [48], None,
         "One captive ball rests in front of the mosquito target; switch 48 (180-5114-08) scores each hit and the rules crack a "
         "dinosaur egg (lamp 61) with every shot, with MOSQUITO MILLIONS lighting the target. The retained table models it as "
         "a kicker (Captive) plus a hit target."),
        ("turbo-bumper-top", "Top turbo bumper", "kicker", [17], [45], "500-5227-00",
         "Turbo Bumper assembly 500-5227-00: skirt switch 180-5015-01 closes on impact and the ROM drives coil 17 (23-800, "
         "090-5001-00). Its bulb is lamp 31."),
        ("turbo-bumper-left", "Left turbo bumper", "kicker", [18], [46], "500-5227-00",
         "As the top bumper: switch 46, coil 18, lamp 62."),
        ("turbo-bumper-right", "Right turbo bumper", "kicker", [19], [47], "500-5227-00",
         "As the top bumper: switch 47, coil 19, lamp 32."),
        ("slingshot-left", "Left slingshot", "kicker", [20], [43], "500-5226-00",
         "Slingshot Assembly 500-5226-00: two slingshot switches 180-5054-00 behind the rubber close the matrix circuit 43 and "
         "the ROM drives coil 20 (23-800, 090-5001-02)."),
        ("slingshot-right", "Right slingshot", "kicker", [21], [44], "500-5226-00",
         "As the left slingshot: switch 44, coil 21."),
        ("knocker", "Cabinet knocker", "other", [8], [], "500-5081-00",
         "The knocker coil of Kickback & Knocker assembly 500-5081-00 (23-800, 090-5001-01) strikes the cabinet stop; the "
         "ROM's cycle test names it KNOCKER. It has no sensor and no playfield emitter."),
        ("shaker", "Cabinet shaker motor", "other", [22], [], "500-5228-00",
         "Shaker Motor Assy 500-5228-00 on motor board 520-5065-00, driven by coil output 22 (ROM SHAKER MOTOR). The retained "
         "table plays a motor sound and leaves its nudge effect commented out."),
        ("lower-left-flipper", "Lower left flipper", "other", [48], [84, 63], "500-5606-78",
         "Cabinet-wired flipper, coil 090-5020-30 (23-900): the left button's circuit (ORN-GRY, CPU CN19-2) fires it directly "
         "through the solid-state flipper board, which takes 50 VDC and 8 VAC. The ROM never drives a flipper coil: output 23 "
         "enables PinMAME's synthetic 47/48 from host button 84, which the table's SolLFlipper follows through 48. The "
         "flipper's own leaf switch (180-5048-01) is the cabinet button; its matrix copy is 63. The unique-parts page prints "
         "flipper assemblies 500-5693-02 (left, uses switch 180-5124-00), 500-5693-01 (right) and 500-5694-01 (upper right), "
         "the major-assembly list 500-5606-78/77/79; both numberings are kept."),
        ("lower-right-flipper", "Lower right flipper", "other", [46], [82, 64], "500-5606-77",
         "As the lower left flipper with the right button (ORN-VIO, CPU CN19-1, leaf switch 180-5022-00 in the switch list and 180-5122-00 as cabinet part 15a) and public 45/46, 82 and 64."),
        ("upper-right-flipper", "Upper right flipper", "other", [], [82, 64], "500-5606-79",
         "Third flipper, coil 090-5041-00 (25-1800, BLK-YEL at flipper board CN2-1,2; the unique-parts page prints '500-5694-01 Upper Right "
         "(uses coil 090-5030-00)' instead, and both readings are kept), operated from the same right button "
         "and the same CPU CN19-1 line as the lower right flipper (its flip-board switch input is GRY-VIO at CN1-12). No "
         "separate ROM output, EOS or button exists, and the retained table moves it with the lower right flipper."),
    ]
    result = []
    for key, label, kind, actuators, sensors, assembly, behavior in rows:
        m = {"id": f"mechanism.{key}", "label": label, "kind": kind,
             "actuators": [sol[n] for n in actuators], "sensors": [sw[n] for n in sensors],
             "behavior": behavior, "provenance": prov(MANUAL, PIN, SCRIPT)}
        if assembly:
            m["assembly_part_number"] = assembly
        if key in {"t-rex", "t-rex-eject", "double-scoop", "top-right-eject", "right-vuk", "raptor-pit", "trough"}:
            m["provenance"] = prov(MANUAL, PIN, SCRIPT, VPW, RT_LASER, RT_TREX, RT_COIL, RT_SWITCH)
        if "flipper" in key:
            m["provenance"] = prov(MANUAL, PIN, VBS, CORE_VBS, SCRIPT, RT_SWITCH)
        result.append(m)
    return result


def relationships(ins: list, outs: list) -> list:
    sw = {d["binding"]["device"]: d["id"] for d in ins if d["binding"]["group"] == "pinmame.input.switch"}
    sol = {d["binding"]["device"]: d["id"] for d in outs if d["binding"]["group"] == "pinmame.output.solenoid"}
    result = [
        {"id": f"relationship.mux-{n}", "kind": "relay_gated", "source": sol[10], "destination": sol[n],
         "provenance": prov(MANUAL, PIN, RT_COIL)}
        for n in range(25, 33)
    ]
    result.extend(flipper_column_relationships(
        flip_swno=(63, 64), matrix_ids=sw, refs=(*PIN_REFS, RT_SWITCH)))
    return result


def displays() -> list:
    return [{"id": "display.dmd", "label": "128x32 dot matrix", "kind": "dmd", "controller_index": 0,
             "width": 128, "height": 32, "physical_location": "cabinet_or_service",
             "spatial": na("cabinet_or_service", PIN, MANUAL), "provenance": prov(PIN, MANUAL, RT_SWITCH)}]


# ---------------------------------------------------------------------------------------------
# Excerpts and sources
# ---------------------------------------------------------------------------------------------
def table_text(title: str, headers: list, rows: list, note: str = "") -> str:
    return (f"# {title}\n\nVisually checked against the rendered factory PDF by {TRANSCRIBER}. Literal full table "
            "region; Not Used rows and printed misprints are retained. OCR was navigation only." + (f" {note}" if note else "")
            + "\n\n| " + " | ".join(headers) + " |\n| " + " | ".join(["---"] * len(headers)) + " |\n"
            + "".join("| " + " | ".join(str(x) for x in row) + " |\n" for row in rows))


def transcriptions() -> dict[str, str]:
    switch_rows, lamp_rows = [], []
    for n in range(1, 65):
        col, row = divmod(n - 1, 8)
        switch_rows.append((n, SWITCH_NAMES[n - 1], SWITCH_PARTS[n - 1], col + 1, row + 1, *SWITCH_COLUMNS[col],
                            *SWITCH_ROWS[row], ROM_SWITCH_NAMES[n - 1]))
        lamp_rows.append((n, LAMP_NAMES[n - 1], LAMP_LIST_NAMES.get(n, "(as matrix)"), "2 bulbs" if n in TWO_BULB_LAMPS else "1 bulb",
                          col + 1, row + 1, *LAMP_COLUMNS[col], *LAMP_ROWS[row], ROM_LAMP_NAMES[n - 1]))
    coil_rows = [(f"{n}L / {n}R", name, rom, transistor, pin, control, coil_wire, flash_wire, bulbs, rom_fl)
                 for n, name, rom, transistor, pin, control, coil_wire, flash_wire, bulbs, rom_fl in LR_DRIVES]
    result = {
        "switch-chart.md": table_text(
            "Switch matrix and parts: printed pages 26-27 / PDF 30-31",
            ["Address", "Printed name", "Part", "Column", "Row", "Drive wire", "Drive connection", "Transistor",
             "Return wire", "Return connection", "ROM Active Switch Test name"], switch_rows,
            "The matrix chart's column 6 prints CN8-7 and its row 6 prints CN10-3: the CPU board's connector keys sit at CN8-6 and "
            "CN10-4 (PDF 51), so those pins are not skipped switches. Printed asterisks 01*-07* mark the coin-door and cabinet "
            "switches; the printed names 'Left Flip. Cab' and 'Right Flip. Cab' name 63 and 64 in the parts list while the matrix "
            "prints Left Flipper and Right Flipper. The matrix prints 'Triceritop Target' (cell edge) where the parts list prints "
            "'Triceritops Target'."),
        "lamp-chart.md": table_text(
            "Lamp matrix and locations: printed pages 28-29 / PDF 32-33",
            ["Address", "Printed matrix name", "Printed location-list name", "Bulbs", "Column", "Row", "Drive wire",
             "Drive connection", "Drive transistor", "Return wire", "Return connection", "Return transistor",
             "ROM single-lamp test name"], lamp_rows,
            "The printed matrix names 6 only 'Map', 50 only '#2' and 48 '\"C\" Arch'; the matrix prints 'Raptor Pit 5 Milion' where "
            "the list prints '5 Million'; the list spells 18 'Left scoop Top' and 'Lite Extra Ball'."),
        "coil-chart.md": table_text(
            "Coil / flash-lamp drives 1-8: printed page 31 / PDF 35, drive schematic",
            ["Drive", "Printed left-set coil", "ROM cycle-test coil name", "CPU transistor", "CPU connector pin",
             "Control wire to PPB J1", "Coil lead wire", "Flash-lamp lead wire", "Printed right-set bulb text",
             "ROM cycle-test flash name"], coil_rows,
            "Drives 1-8 drive a left-set coil and a right-set flash-lamp bank through the PPB board's left/right relay (public "
            "10). Drives 3 and 5 pass through PPB board transistors Q5 and Q3 ('TIP SEC') at J8 and connect at J7; the "
            "printed PPB boxes show +32 VL / +32 VR. The J2 and J9 pin boxes are in the retained crop (coil-schematic) and are not transcribed."
        ) + "\n" + table_text(
            "Drives 9-16: printed page 31 / PDF 35 and CPU CN12 (PDF 51)",
            ["Drive", "Printed name", "ROM cycle-test name", "CPU transistor", "CPU connection", "Wire", "What it switches"],
            [row for row in DIRECT_DRIVES]
        ) + "\n" + table_text(
            "CPU Controlled Auxiliary Solenoids: printed page 30 / PDF 34",
            ["Coil", "Printed name", "Control wire", "Control connection", "Power wire", "Power connection",
             "Drive transistor", "Printed coil type"], [row for row in AUX_COILS]
        ) + "\n" + table_text(
            "Flipper solenoids: printed page 30 / PDF 34",
            ["Coil", "Part", "Flipper GND (CPU to flip switch)", "Flip switch to flip PCB", "Power lines flip PCB to coil",
             "Printed coil type", "Power input to flip PCB"], [row for row in FLIPPER_CHART]
        ) + "\n" + table_text(
            "Coil parts from the unique-parts assembly pages: printed pages 33-43 / PDF 41-47",
            ["Coil", "Assembly", "Coil printed on that page", "Coil part"],
            [(n, *ASSEMBLY_COILS[n]) for n in sorted(ASSEMBLY_COILS)],
            "The schematic prints coil type 23-840 for the whole left set; the unique-parts pages give each assembly's own coil."
        ),
    }
    result["coil-schematic.md"] = (
        "# Coil / flash-lamp schematic: printed page 31 / PDF 35\n\n"
        f"Visually checked against the rendered factory PDF by {TRANSCRIBER}. The drawing (retained crop) is the claim; "
        "this text states what was read from it.\n\n"
        "- Drives 1-8: CPU board 'SIDE L 0n / SIDE R 0n' transistor Q46..Q39 -> GRY wire -> PPB board J1 pin n; from the left/right "
        "relay the left side reaches the coil (VIO wire from J2, coil 'BRN' return at J6-3 +32 VL) and the right side the flash-lamp "
        "bank (BLK wire from J9, bulbs returned on ORG to J6-4/5 +32 VR).\n"
        "- 1 TOP EJECT 23-840, 2 BALL RELEASE 23-840, 3 AUTO LAUNCH 23-840 (WHT-ORG -> J8 Q5 TIP SEC -> VIO-ORG, YEL-VIO to J7-8/9), "
        "4 LEFT SCOOP 23-840, 5 RIGHT VUK 23-840 (WHT-GRN -> J8 Q3 TIP SEC -> VIO-GRN, YEL-VIO to J7-8/9), 6 DIVERTER 23-840, "
        "7 DINO EJECT 23-840, 8 KNOCKER 23-840.\n"
        "- Right-set bulb legends: 1R (3) RAPTOR PIT (1) INSERT; 2R (3) PLFD RIGHT SIDE (1) INSERT; 3R (4) ORBIT SHOT; 4R (3) UPPER RIGHT "
        "PLFD (1) UPPER RIGHT CORNER; 5R (3) UPPER RIGHT PLFD (1) UPPER LEFT CORNER; 6R (3) LEFT SIDE PLFD (1) INSERT; 7R (4) TURBO "
        "BUMPER; 8R (1) MOSQUITO (1) PLFD (2) TOP DISPLAY.\n"
        "- Lower block, CPU CN12: 09 Q30 pin 1 WHT/BRN -> J8 Q4 TIP SEC -> BRN-BLK -> RAPTOR PIT 23-840 -> VIO/YEL -> J7-3 50 VDC; 10 Q29 pin 2 "
        "BLK-RED -> L/R COIL RELAY (terminals 9 and 7) -> RED/WHT to PS CN3-5 +32V; 11 Q28 pin 4 BRN-ORG -> PS CN7-1/3 K-1 GENERAL ILLUM. RELAY; "
        "13 Q26 pin 6 BRN-GRN -> DINO MOUTH coil -> RED; 16 Q23 pin 9 BRN-GRY -> TROUGH LOCKOUT coil -> RED; 14 Q25 pin 7 BRN-BLU -> relay board "
        "520-5010-00 (N.O. / N.C. / COMM, 28 VAC FROM BR2, WHT/RED); 15 Q24 pin 8 BRN-VIO -> bi-directional relay 520-5066-00 (28 VAC, "
        "(LEFT/RIGHT) BRN/YEL input, MOTOR 9VDC GRY/BLU and BLU, T REX BI DIRECTIONAL MOTOR 9 VDC, PO SHAKER MOTOR BOARD 520-5065-00 with D1 1N5404 and "
        "F1 2-1/2 AMP 250 V); 12 Q27 pin 5 BRN-YEL -> the (LEFT/RIGHT) input of that relay.\n"
        "- CPU CN12 (PDF 51 connector block): 9 LOCKOUT BRN/GRY, 8 MOTOR RELAY ON/OFF BRN/VIO, 7 MOTOR RELAY UP/DOWN BRN/BLU, 6 DINO MOUTH BRN/GRN, "
        "5 MOTOR (LEFT/RIGHT) BRN/YEL, 4 G.I. RELAY BRN/ORG, 3 KEY, 2 A/B RELAY BLK/RED, 1 RAPTOR PIT.\n")
    result["assembly-tables.md"] = (
        f"# Assembly and parts regions\n\nVisually checked against the rendered factory PDF by {TRANSCRIBER}. Repeated item "
        "numbers and generic alternates are retained; do not infer fitment from a generic part list alone.\n\n"
        "## PDF 37 / printed page 33: Playfield - Major Assemblies\n\n"
        "1 Kickback Assy. 500-5081-00 (drawn at the raptor pit); 2 Super VUK 500-5116-04; 3 Sling Shot Assy. 500-5226-00; 4 Pop Bumper "
        "500-5277-00; 5 Ball Launch 500-5477-00; 6 Flipper Right 500-5606-77; 7 Flipper Left 500-5606-78; 8 Flipper Right Upper "
        "500-5606-79; 9 S/U Narrow Tgt. Assy. 500-5639-12; 10 S/U Tgt. 1 Bank Green 500-5639-14; 11 1 Bank ST/UP Target 500-5640-14; "
        "12 1 Bank ST/UP Target 500-5640-18; 13 3 Bank ST/UP Target 500-5640-32; 14 3 Bank ST/UP Target 500-5641-00; 15 6 Ball Switch Assy. "
        "500-5645-00; 16 Diverter Assy. 500-5661-00; 17 Ball Eject 500-5664-00; 18 Dino Eject 500-5665-00; 19 Dinosaur Assy. 500-5667-00; "
        "20 Double Scoop 515-5772-00 (drawn twice); 21 Outhole Ball Deflector 535-6568-00; 22 Wire Ramp 535-6531-00; 23 Ramp Assembly 500-5669-00.\n\n"
        "## PDF 40 / printed page 36: Lamp Bulb Part Numbers\n\n"
        "1 #44 Bulb 165-5000-44; 2 #89 Bulb 165-5000-89; 3 #555 Bulb 165-5002-00; 4 # 906 Bulb 165-5004-00. The drawing numbers the "
        "bulbs by position; the three turbo bumpers carry #555.\n\n"
        "## PDF 41-47 / printed pages 37-43: unique parts (coil lines)\n\n"
        "Ball Eject Assy (Saucer) 500-5664-00: 090-5636-02 24-940 COIL, sleeve 260-0004-00. Super VUK 500-5116-04: item 2 Micro Switch 180-5064-00, "
        "item 10 Coil 23-800 090-5001-01, item 11 1N4004 Diode 112-5003-00. Slingshot Assembly 500-5226-00: item 6 23-800 Coil w/Sleeve "
        "090-5001-02, item 10 Slingshot Switch (2) 180-5054-00, item 13 Diode 1N4004 (2) 112-5004-00. Ball Eject Assy (Dino) 500-5665-00: "
        "090-5004-02 27-1500 COIL. Turbo Bumper 500-5227-00: Switch 180-5015-01, Diode IN4001 112-5004-00, Coil 090-5001-00 (AE-23-800). Shaker "
        "Motor Ass'y 500-5228-00. Kickback & Knocker Assembly 500-5081-00: Coil 090-5001-01 (AE-23-800). Ball Launch Ass'y 500-5477-00: item 3 Coil 23-800 "
        "090-5001-01. Diverter Plunger & Crank Arm Assy 500-5661-00: Coil 090-5004-02 27-1500; Ramp Diverter Arm 515-5781-00. Double Scoop "
        "Sub-Assembly 515-5772-00: COIL 090-5001-01, SWITCH 180-5116-00, MICRO SWT. ASSY 500-5700-00, DIODE 112-5001-00. Flipper "
        "Assemblies: 500-5693-01 Right, 500-5693-02 Left (uses Switch 180-5124-00), 500-5694-01 Upper Right (uses coil 090-5030-00); item 12 flipper coil 23-900 090-5020-30. "
        "The flipper table (PDF 34) prints the upper right coil as 090-5041-00 25-1800.\n\n"
        "## PDF 36 / printed page 32: cabinet parts (switch lines)\n\n"
        "1 Shooter Gun Assy. 500-5673-00; 14 Push Button Switch 180-0028-00; 15 Left Flipper Leaf Switch 180-5048-01; 15a Right Flipper Leaf Switch * 180-5122-00 (* not shown); 17 Plumb Bob Tilt Assembly 500-5023-00; "
        "25 S.S.Flipper P.C.B. 520-5033-02.\n\n"
        "## PDF 97-98 / printed page 70: Dino Assembly BOM\n\n"
        "1 041-5025-00 5VDC MOTOR-MULTI; 4 180-5040-00 MICRO SWITCH (4); 19 041-5026-00 BOWMAN 11 RPM 24 VAC; 24 535-6641-00 DINO JAW; 25 535-6643-00 DINO NECK; "
        "29 090-5034-00 COIL-25-1240; 32 530-5013-01 PLUNGER; 39 180-5123-00 MICRO SWITCH ROLLER; 42 036-5300-00 DINO BASE CABLE; 43 036-5304-00 "
        "UP-DOWN CABLE.\n\n"
        "## PDF 99-100 / printed page 71: 6 Ball Outhole-Trough Assembly\n\n"
        "Ball Switch Assembly 500-5683-00 (items 1-16): item 4 180-5118-00 SWITCH, MINIATURE (1); item 5 180-5119-00 SWITCH, SUBMINIATURE (12); item 9 "
        "090-5001-00 COIL, 23-800 (1). Lock Ball Assembly 500-5684-00 (items 17-31): item 23 090-5034-00 COIL, 25-1240 (1); item 31 036-5301-01 WIRING HARNESS.\n")
    result["factory-notes.md"] = (
        f"# Factory notes read from the manual\n\nVisually checked against the rendered factory PDF by {TRANSCRIBER}.\n\n"
        "## PDF 2 / front matter: CPU jumper table and fuse chart\n\n"
        "Jurassic Park: CPU Version Ver 3, ROM location 5C, jumpers installed J1b, J3, J5, J5b, J6b, J7b & J8; removed J1a, J2, J4, J5a, J6a & J7a. "
        "PPB board fuses: F1-F4 5A Slo-Blo G.I. 6.3VAC; F5 5A Slo-Blo Flipper Power & 50Volt coils; F6 5A Slo-Blo Flash Lamps (34VDC). Power "
        "supply board: F4 8A Slo-Blo Switched Illumination Buss (18VDC); F5 5A Solenoid (34VDC) Bumpers Slingshots etc.; F6 5A Solenoid Buss "
        "(34VDC). Motor Control Board F1-F3 2.5 A.\n\n"
        "## PDF 6 / game illustration Detail A: G.I. fuses (all 5A S.B.)\n\n"
        "F1 Playfield; F2 Backbox Door & Speaker Panel; F3 Playfield & Coin Door; F4 Backbox Door. F5 (50VDC) and F6 are on the same PPB board.\n\n"
        "## PDF 7 / printed page 3\n\n"
        "'Note that this game is not equipped with a ball roll tilt.'\n\n"
        "## PDF 29 / printed page 25: T-REX Test and Laser Kick Test\n\n"
        "T-REX Test: 'This test shows the status of all the switches on the T-Rex mechanism, and provides motor control when the appropriate "
        "switches are properly adjusted. To move the creature left and right, use the left and right flipper buttons. Note: The T-REX Top "
        "Switch must indicate ON to allow left and right movement. To move the creature up and down, use the start button. Note: The T-REX Center "
        "Switch must indicate ON to allow up and down movement ... Operating the trigger switch should pulse the Jaw coil.' Laser Kick Test: "
        "'by rolling the ball over the left outlane switch the Laser Kick should fire' (the retained ROM's own screen reads PUT BALL IN RAPTORS) and "
        "'similar tests may be performed on Vertical Up Kickers or Saucers in the game.'\n\n"
        "## PDF 8-12 / printed pages 4-8: game-specific features (rules paraphrased from the OCR text, for names only; not a visually checked transcription)\n\n"
        "Skill shot with the tazer gun; smart missile once per game; tri-ball and CHAOS letters; Raptor Pit/Wild Raptors; the twelve computer "
        "mini-games (Electric Fences, Spitter Attack, 2 Ball Play at the boat dock, System Boot, Raptors Rampage, Lighting Extra Ball, Mosquito "
        "Millions, Feed T-Rex, Bone Busting, Escape Isla Nublar, Stampede, System Failure); captive-ball egg; ramp molecules; T-Rex paddock "
        "jackpot; Advance X; Hammonds Bunker; Death Save.\n")
    result["geometry.md"] = (
        "# Exact retained geometry\n\n"
        f"Selected Dark & Friends table, sha256 {TABLE_SHA}. Full vpxtool git:v0.33.3 extraction: {EXTRACTION_FILES} files, "
        f"{EXTRACTION_BYTES} bytes. Canonical manifest: {EXTRACTION_MANIFEST}. Manifest algorithm: every relative POSIX path sorted "
        "case-sensitively, byte size and full-file SHA256; UTF8 compact JSON array of {path,sha256,size_bytes} with sorted keys, no final newline.\n\n"
        "Bounds left 0, top 0, right 952, bottom 2162. x=raw_x/952; y=raw_y/2162; six-decimal rounding. Slingshots use the signed "
        "shoelace area centroid of their wall; targets use the HitTarget position, bumpers, triggers and kickers their own center; lamps "
        "and flash-lamp bulbs the center of the script-driven Light object. No Flasher sprite, glow, halo, reflection or shadow light is a "
        "placement. Exact JSON paths, hashes and raw coordinates are in tools/jurassic_park_geometry.json (tools/build_jurassic_park_geometry.py).\n\n"
        "Only one factory-layout table is retained, so no placement is cross-validated against a second table. The playfield artwork "
        "image (images/playfield.png, 2048x4652) was read to settle the lamp 20 and 30 legends.\n")
    pin_files = "".join(f"- src/wpc/{name}: `{digest}`; lines {locator}.\n" for name, digest, locator in PIN_FILES)
    result["transport-and-runtime.md"] = (
        "# Exact runtime and transport contract\n\n"
        f"Pinned PinMAME {REVISION}:\n"
        "degames.c lines 967-1017 declare jupk_513 (root) and the clones jupk_600, jupk_501, jupk_g51, jupk_305 and jupk_307 on "
        "INITGAMES11(jupk, GEN_DEDMD32, de_128x32DMD, FLIP6364, SNDBRD_DE2S, SNDBRD_DEDMD32, S11_PRINTERLINE): hw.flippers FLIP_SWNO(63,64) "
        "(no FLIP_SOL), no extra switch or lamp columns, no custom solenoids, no simData, an all-zero invSw and mux solenoid 10 "
        "(the {10} initializer). The 5.13 ROM set (jpcpua.513, jpdspa.510, jpu7/17/21.dat) was checked member by member against the driver's CRC and SHA1.\n"
        "core.h lines 300-330: extension 37, custom 51. s11.c lines 392-410: printer byte non-inverted, published at 37-44; lines 558-584: mux 10 routes "
        "1-8 to 25-32; lines 618-625: Data East special-solenoid order pia1ca2->20, pia1cb2->21, pia3ca2->22, pia3cb2->18, pia4ca2->17, pia4cb2->19; "
        "lines 628-650: eight-bit switch strobe, uncomplemented core_getSwCol; lines 1188-1196 name jupk_ with the DataEast/Sega 3 brightness models: "
        "solenoid 11 reversed #44 6.3 VAC (GI) and 25-32 #89 32 VDC (a brightness model, not fitment).\n"
        "core.c lines 1700-1753: 82->64, 84->63; game-on 23 gates synthetic 45-48. Lines 2182-2224: 33-36 dead for Data East, 37-44 raw printer "
        "extension, 49 simulator, 50 gap, 51+ custom (none). No upper ROM coil exists.\n\n"
        f"Exact retained Dark & Friends 1.03 embedded script sha256 {SCRIPT_SHA}: script.vbs line 325 cGameName=jupk_513; 270-274 LoadVPM de.vbs; "
        "334-336 HandleMechanics 0 and HandleKeyboard 0; 415-437 SolCallback(1-23); 443-444 sLRFlipper/sLLFlipper; 500-700 kickers, VUK, boat dock, "
        "raptor pit, diverter, jets; 905-1015 matrix Hit/UnHit and PulseSw; 1043-1300 T-Rex saucer, toy model and motors; 1503-1640 flash lamps; "
        "1655-1900 UpdateLamps (Controller.ChangedLamps then nFadeL/nFadeLm).\n"
        f"The corpus sidecar `{CORPUS_FILE}` (sha256 {CORPUS_SHA}) is the same table with sound edits and the VPW 1.0 script (sha256 {VPW_SHA}, "
        "ROM jupk_600) is a later rebuild; both agree with the embedded script on every switch, solenoid and T-Rex binding used here and add "
        "real triggers sw9-sw14 for the trough contacts.\n"
        "de.vbs and core.vbs: swLRFlip 82, swLLFlip 84, sLRFlipper 46, sLLFlipper 48. "
        f"de.vbs sha256 {DE_VBS_SHA}; core.vbs sha256 {CORE_VBS_SHA}.\n\n"
        "Runtime: fresh empty-CMOS runs of jupk_513 on the pinned DLL (see runtime-provenance.md). The committed scenarios use named service keys and "
        "exact DMD title fingerprints (tools/jurassic_park_harness.py); output 23 marks readiness for the Active Switch and Laser Kick tests. "
        "Expected causal results: each Active Switch closure prints its ROM name; the lamp test lights one lamp per press and prints its name; the "
        "cycling-coils test pulses 1-9, 11-13 and 16-22 with 25-32 on the right set; closing 29/35/55/56/61 in the Laser Kick Test fires 9/4/7/1/5; the "
        "T-REX TEST turns ON the label of 57/58/36/31/32; host left/right buttons produce 47/48 and 45/46. Host switch readback alone is never ROM "
        "evidence. Complete raw runs, snapshots and manifests remain external.\n\n"
        "Exact pinned transport files (full-file SHA256):\n\n" + pin_files + f"- src/wpc/degames.c: `{DEGAMES_SHA}`; lines 75-82, 967-1017.\n")
    summary = json.dumps(RUNTIME, indent=1, sort_keys=True, ensure_ascii=False)
    result["runtime-summary.md"] = ("# Checked runtime transitions and visually read ROM names\n\n```json\n" + summary + "\n```\n")
    for stem, title, payload in (
        ("runtime-provenance", "Exact runtime provenance and external manifest", RUNTIME_PROVENANCE),
        ("manual-provenance", "Retained document identities and acquisition URLs", MANUAL_PROVENANCE),
    ):
        result[f"{stem}.md"] = f"# {title}\n\n```json\n{canonical_bytes(payload).decode()}```\n"
    return result


IMAGES = {
    "switch-chart.md": ("switch-locations", "ecf13c0c8806051045961866461a25f31a1482f2ddf229ecab5472b3eb36a7e3",
        "Data_East_1993_Jurassic_Park_Manual.pdf page 31, crop box 0.15,0.27,0.5,0.83, scanned page rendered at its native resolution (embedded image xref 150, 2550px across 8.50in), rendered at 300 dpi, grayscale, 893x1848 WebP quality 80"),
    "lamp-chart.md": ("lamp-locations", "e06249428ecdcf9246c4c9646ccda5fe88eae96c0be656ec0e53c56e4b20b39a",
        "Data_East_1993_Jurassic_Park_Manual.pdf page 33, crop box 0.14,0.24,0.47,0.8, scanned page rendered at its native resolution (embedded image xref 160, 2550px across 8.50in), rendered at 300 dpi, grayscale, 842x1848 WebP quality 80"),
    "coil-chart.md": ("coil-locations", "81cb499bf19451f037a0fda36671628581d811b40b3520146584a7562e797a46",
        "Data_East_1993_Jurassic_Park_Manual.pdf page 34, crop box 0.09,0.4,0.39,0.89, scanned page rendered at its native resolution (embedded image xref 165, 2550px across 8.50in), rendered at 300 dpi, grayscale, 766x1617 WebP quality 80"),
    "coil-schematic.md": ("coil-schematic", "c926c05f140c39931aeb062aca1a0c8050d461267a383983c195f988e8dc0090",
        "Data_East_1993_Jurassic_Park_Manual.pdf page 35, crop box 0.13,0.05,0.86,0.97, scanned page rendered at its native resolution (embedded image xref 170, 2550px across 8.50in), rendered at 290 dpi, capped to 1800px wide, grayscale, 1801x2937 WebP quality 80"),
}


def excerpt(name: str, locator: str, text: str) -> dict:
    return {"id": "excerpt.jurassic-park." + name.removesuffix(".md"), "locator": locator,
            "path": f"{EXCERPTS}/{name}", "sha256": hashlib.sha256(text.encode()).hexdigest(), "method": "manual",
            "transcribed_by": TRANSCRIBER, "reviewed": True}


def sources(texts: dict) -> list:
    def ex(name: str, locator: str) -> dict:
        e = excerpt(name, locator, texts[name])
        if name in IMAGES:
            stem, digest, derivation = IMAGES[name]
            e.update(image=f"{EXCERPTS}/{stem}.webp", image_sha256=digest, image_derivation=derivation)
        return e

    def source(identifier: str, kind: str, uri: str, digest: str, locator: str, excerpts: list, attribution: str, **extra) -> dict:
        record = {"id": identifier, "kind": kind, "uri": uri, "sha256": digest, "locator": locator,
                  "excerpts": excerpts, "attribution": attribution, "rights": "NOASSERTION", "license": "NOASSERTION", **extra}
        return record

    manual_record = next(r for r in MANUAL_PROVENANCE["records"] if r["original_filename"] == MANUAL_FILENAME)
    provenance_excerpt = ex("manual-provenance.md", "Verified IPDB 1343 machine page, resolved Wayback captures, acquisition timestamp and digest")
    run_excerpt = ex("runtime-summary.md", "Checked per-frame readings, hashes and per-step transitions")
    run_meta = {"revision": REVISION, "attribution": "Primary curator; legally supplied user ROMs"}

    def runtime(identifier: str, key: str, name: str, locator: str) -> dict:
        entry = RUNTIME[key]
        return source(identifier, "runtime_scenario",
                      f"external:pinmame-review-artifacts/{KEY}/session-20261001/runtime/{name}/run.json",
                      entry["raw_sha256"], f"{locator}; scenario {entry['scenario_sha256']}",
                      [ex("transport-and-runtime.md", "Causal expectations and retained raw-run identity"), run_excerpt,
                       ex("runtime-provenance.md", "ROM/DLL/harness/scenario/raw hashes, fresh-state setup, command and complete directory manifest")],
                      run_meta["attribution"], revision=REVISION)

    result = [
        source(MANUAL, "manual", f"external:manuals/by-machine/{KEY}/ipdb/{MANUAL_FILENAME}", MANUAL_SHA,
               "PDF 30-35 / printed pages 26-31 diagnostics; PDF 36-47 parts; PDF 51 CPU connectors; PDF 97-100 dino and trough assemblies",
               [ex("switch-chart.md", "PDF 30-31 complete matrix and parts table, switch-location drawing"),
                ex("lamp-chart.md", "PDF 32-33 complete lamp matrix, location list and drawing"),
                ex("coil-chart.md", "PDF 34-35 coil, flash-lamp, auxiliary-solenoid and flipper tables"),
                ex("coil-schematic.md", "PDF 35 coil / flash-lamp schematic and CPU CN12 block"),
                ex("assembly-tables.md", "PDF 37, 40-47, 97-100 assemblies, bulbs, dino and trough BOMs"),
                ex("factory-notes.md", "PDF 2, 6, 7, 8-12, 29 front matter, test text and rules"), provenance_excerpt],
               "Data East USA, Inc.", original_filename=MANUAL_FILENAME, source_id="IPDB1343",
               acquired_at=manual_record["acquired_at"]),
        source(PIN, "pinmame_core", f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/degames.c", DEGAMES_SHA,
               "degames.c lines 75-82, 967-1017; jupk driver and game-data declarations",
               [ex("transport-and-runtime.md", "Pinned source chain, every Jurassic Park address band")],
               "PinMAME contributors", revision=REVISION),
        *[source(identifier, "pinmame_core", f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/{name}", digest,
                 f"src/wpc/{name} lines {locator}",
                 [ex("transport-and-runtime.md", f"Exact {name} controller-contract region")],
                 "PinMAME contributors", revision=REVISION)
          for identifier, (name, digest, locator) in zip(PIN_REFS[1:], PIN_FILES)],
        source(TABLE, "vpx_table", f"external:vpx-sources/{TABLE_FILE}", TABLE_SHA,
               "complete vpxtool extraction; gamedata.json bounds; gameitems per jurassic_park_geometry.json",
               [ex("geometry.md", "Exact extraction manifest and source JSON locators")],
               "Dark & Friends (Dark, bodydump, Flupper1, HauntFreaks, randr, rothbauerw, Lobotomy; retained table metadata)",
               known_working=True, original_filename="Jurassic Park (Data East 1993)1.03.vpx"),
        source(SCRIPT, "vpx_script", f"external:vpx-sources/{TABLE_SUBDIR}/script.vbs", SCRIPT_SHA,
               "script.vbs lines 270-336,415-444,500-700,905-1300,1503-1900; embedded script, not a corpus sidecar",
               [ex("transport-and-runtime.md", "Exact embedded script callbacks and switch bindings")],
               "Dark & Friends; embedded header credits", known_working=True),
        source(CORPUS, "vpx_script",
               f"https://github.com/vpinball/vpxtable_scripts/blob/{SCRIPT_REVISION}/Jurassic%20Park%20(Data%20East%201993)1.03.vbs",
               CORPUS_SHA, "whole file; same table with Thalamus sound edits",
               [ex("transport-and-runtime.md", "Corpus sidecar comparison")],
               "Dark & Friends; Thalamus", revision=SCRIPT_REVISION, known_working=True),
        source(VPW, "vpx_script",
               f"https://github.com/vpinball/vpxtable_scripts/blob/{SCRIPT_REVISION}/Jurassic%20Park%20(Data%20East%201993)%20VPW%201.0.vbs",
               VPW_SHA, "lines 127,392-443,832-864,1099,1192-1230,1633-1725; ROM jupk_600",
               [ex("transport-and-runtime.md", "Pinned VPW runtime semantics")],
               "VPinWorkshop contributors", revision=SCRIPT_REVISION, known_working=True),
        source(VBS, "vpx_script", "external:pinmame-review-artifacts/vpm-script-libs/de.vbs", DE_VBS_SHA,
               "de.vbs vpmKeyDown/vpmKeyUp and shared input mapping",
               [ex("transport-and-runtime.md", "DE library key transport")], "VPinMAME scripting library contributors"),
        source(CORE_VBS, "vpx_script", "external:pinmame-review-artifacts/vpm-script-libs/core.vbs", CORE_VBS_SHA,
               "core.vbs sLRFlipper/sLLFlipper constants and cvpmFlips2",
               [ex("transport-and-runtime.md", "Core library flipper constants")], "VPinMAME scripting library contributors"),
        runtime(RT_SWITCH, "active_switch_test", "active-switch-test",
                "fresh state, ACTIVE SWITCH TEST: every public matrix switch 1-62 closed in turn plus the host flipper buttons"),
        runtime(RT_LAMP, "lamp_test", "lamp-test", "fresh state, single-lamp test: one lamp per Start press, names and wire colours"),
        runtime(RT_COIL, "coil_cycle", "coil-cycle",
                "fresh state, CYCLING COILS test and power-up T-Rex diagnostic; the T-Rex-homed twin is cited in runtime-summary.md"),
        runtime(RT_LASER, "laser_kick_test", "laser-kick-test", "fresh state, LASER KICK TEST closures"),
        runtime(RT_TREX, "trex_test", "trex-test", "fresh state, T-REX TEST closures and motor controls"),
    ]
    return result


DRIVER_NOTES = {
    "jupk_513": ("5.13 (the production US set the retained table and every runtime run use); all six drivers share jupkGameData, "
                 "the controller transport and the production wiring."),
    "jupk_501": "5.01 US firmware; same CPU board, DMD, sound hardware and I/O as 5.13.",
    "jupk_g51": "5.01 German: the same CPU ROM with a German DMD ROM (jpdspg.501); display text differs, hardware and I/O are unchanged.",
    "jupk_305": "3.05 early production code; the display ROM is borrowed from 3.07 (4.00) in the PinMAME set; hardware is unchanged.",
    "jupk_307": "3.07 early production code with the 4.00 display ROM; hardware is unchanged.",
    "jupk_600": ("6.00 unofficial 2015 MOD; the declaration reuses jupkGameData and documents no hardware change. Its firmware, "
                 "not its wiring, differs, so only the shared I/O map is claimed."),
}


def build() -> dict:
    texts = transcriptions()
    ins, outs = inputs(), outputs()
    machine = {
        "format": "pinmame-machine-definition", "schema_version": 1,
        "machine": {"id": KEY, "name": "Jurassic Park", "manufacturer": "Data East", "year": 1993,
                    "kind": "physical_pinball", "ipdb_id": 1343, "opdb_id": "G4ZVB-MJ5lE", "model_number": "500-5520-01",
                    "playfield": {"width": 952, "height": 2162, "units": "vpx",
                                  "provenance": prov(TABLE, status="observed")}},
        "controller": {"platform": "pinmame.dataeast", "hardware_generation": "0x4000", "inversion_applied_by_emulator": True},
        "drivers": [
            {"id": name, "description": description, "year": year, "manufacturer": "Data East", "flags": 0,
             "physical_compatibility": "identical", "variant_notes": DRIVER_NOTES[name],
             **({"clone_of": "jupk_513"} if name != "jupk_513" else {})}
            for name, description, year in [
                ("jupk_513", "Jurassic Park (5.13)", "1993"), ("jupk_305", "Jurassic Park (3.05)", "1993"),
                ("jupk_307", "Jurassic Park (3.07)", "1993"), ("jupk_501", "Jurassic Park (5.01)", "1993"),
                ("jupk_600", "Jurassic Park (6.00 unofficial MOD)", "2015"),
                ("jupk_g51", "Jurassic Park (5.01 German)", "1993")]],
        "inputs": ins, "outputs": outs, "displays": displays(),
        "mechanisms": mechanisms(ins, outs), "relationships": relationships(ins, outs),
        "sources": sources(texts),
        "knowledge": {"path": f"knowledge/{STEM}.md", "status": "complete"},
        "coverage": {"status": "partial", "missing": ["output_semantics", "spatial_placement", "unresolved_conflicts"],
                     "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated",
                                    "semantic_naming": "validated", "physical_wiring": "observed",
                                    "mechanisms": "observed", "variant_coverage": "validated",
                                    "recreation_knowledge": "validated", "spatial_placement": "observed",
                                    "runtime_observation": "observed", "causal_exercise": "observed"}},
        "conflicts": [{
            "id": "conflict.flash-bank-1r-bulb-count",
            "path": "outputs.device.flasher-1-top-middle",
            "description": ("The coil / flash-lamp schematic (PDF 35) draws four bulb symbols for bank 1R and prints '(3) RAPTOR PIT (1) INSERT'; "
                            "the location drawing (PDF 34) shows two playfield 1R locations beside the raptor lane and the right ramp; the ROM's "
                            "cycle test names it FL: 2-RAPTOR 1-INS. The bank therefore has either four bulbs or three, which decides how many "
                            "emitters an author builds. Resolution path: count the 1R bulbs on a production machine or in teardown photographs of the "
                            "raptor-pit area and backbox insert (IPDB's playfield photographs of IPDB 1343 are the first place to look)."),
            "source_refs": [MANUAL, RT_COIL], "status": "unresolved"}],
    }
    return machine


def report(machine: dict) -> dict:
    unplaced = [d["id"] for d in machine["inputs"] + machine["outputs"]
                if d.get("availability") == "used" and "spatial" not in d]
    unknown = [d["id"] for d in machine["outputs"] if d.get("availability") == "unknown"]
    gi = next(d["id"] for d in machine["outputs"] if d["binding"] == {"group": "pinmame.output.solenoid", "device": 11})
    partial_flashers = [d["id"] for d in machine["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"
                        and 25 <= d["binding"]["device"] <= 32]
    return {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": KEY,
        "decision": "partial; independent cross-provider review belongs to the coordinator",
        "coordinate_convention": "x=0 left, 1 right; y=0 rear, 1 front", "bounds": GEOMETRY["bounds"],
        "transform": "x=raw_x/952; y=raw_y/2162; round to 6 decimals. Slingshot walls use the signed area centroid.",
        "selected_extraction": {"root": "external:vpx-sources/" + TABLE_SUBDIR, "files": EXTRACTION_FILES,
                                "bytes": EXTRACTION_BYTES, "manifest_sha256": EXTRACTION_MANIFEST,
                                "algorithm": "Sorted POSIX paths, sizes and full SHA256; compact sorted-key UTF8 JSON array, no newline."},
        "object_evidence": GEOMETRY["objects"],
        "manual_crosschecks": ["PDF 31 switch-location drawing: counts and sides of the placed switches",
                               "PDF 33 lamp-location drawing: the two-bulb lamps 1, 10, 19, 28 and 55 each match two table lights",
                               "PDF 34 coil / flash-lamp location drawing",
                               "PDF 37 major-assembly drawing: assembly numbers and mechanism positions"],
        "projections": {
            "sensor_object": "A switch is placed on the object its script handler binds (triggers, kickers, bumpers, hit targets); slingshots on their wall's area centroid.",
            "trex_pivot": "The five T-Rex sensors and the rotation, up/down and direction controls project onto the TrexPlastic toy pivot; the toy's switches are the table's position model, not objects.",
            "coil_effect": "A coil's effect projects onto its mechanism object, not a winding centre.",
            "lamp_bulb": "A lamp is placed at the script-driven Light object UpdateLamps binds, never its glow or halo twin.",
            "flash_bank": "A flash bank is placed at the PlayfieldLights or dome-bulb Light objects its FlashN routine drives; banks the table models with fewer bulbs than the factory fits stay partial."},
        "unplaced_records": unplaced,
        "blockers": [
            {"dimension": "spatial_placement", "records": unplaced,
             "reason": ("Only one factory-layout table is retained, so no placement is cross-validated, and no drawing callout check "
                        "has been made, so every placement stays observed. The seven trough contacts have no table object; the "
                        "left, center and right scoop, T-Rex-scoop and gate lamps are glow-only in the table; the flash banks are "
                        "partial (the table omits backbox and insert bulbs the factory fits)."),
             "resolution": "A second retained factory-layout table, or a callout check of PDF 31, 33 and 34 against the table (tools/drawing_callouts.py), plus measured trough and scoop positions."},
            {"dimension": "output_semantics", "records": [gi, *unknown],
             "reason": ("GI relay identity, wiring and fuse groups are settled, but the fitted GI sockets, their count and their playfield, "
                        "backbox and coin-door split are not; raw printer bits 37-44 are an unexplained PinMAME transport the manual "
                        "does not document."),
             "resolution": "Count the GI strings from the power-supply schematic pages or socket photographs (fuses F1-F4: Playfield; Backbox Door & Speaker Panel; Playfield & Coin Door; Backbox Door); run the ROM's print-out feature to see whether the printer byte is ever written."},
        ],
        "partial_flash_banks": partial_flashers,
        "promotion": {"allowed": False, "missing": machine["coverage"]["missing"]},
        "evidence_paths": {"manual": "external:manuals/by-machine/" + KEY,
                           "vpx": "external:vpx-sources/data-east/jurassic-park-1993",
                           "runtime": f"external:pinmame-review-artifacts/{KEY}/session-20261001/runtime"},
    }


def knowledge(machine: dict) -> str:
    text = """# Jurassic Park (Data East, 1993)

This definition describes the production machine (IPDB 1343, model 500-5520-01, DataEast/Sega Version 3 CPU board, 128x32 dot-matrix
display, DE2S sound) and all six pinned drivers: the production 5.13 set and its 3.05, 3.07, 5.01, German 5.01 and unofficial 6.00
siblings, which share one game-data declaration and one wiring. It is partial: the I/O contract, names, wiring, polarity, mechanisms and
runtime behaviour are enumerated and evidenced; the fitted GI sockets, the raw printer bits and the validation of every spatial placement
are not.

## What the ROM itself proves

The ROM's service menus name every switch, lamp and coil, so these runs (fresh empty CMOS, pinned LibPinMAME, jupk_513) are the strongest
naming evidence here. The Active Switch Test names every matrix switch 1-62 while the host holds it at public 1, with its wire colours and
number, and the host flipper buttons 82/84 appear as LEFT/RIGHT FLIPPER 63/64 and produce the synthetic outputs 47/48 and 45/46. The
single-lamp test lights one lamp per Start press and prints its name, colours and number for all 64 lamps. The CYCLING COILS test names and
pulses coils 1-9, 11-13 and 16-22 and flash banks 25-32 (14 and 15 are named but not pulsed). The T-REX TEST turns ON TOP, BOTTOM, CENTER, RIGHT and
LEFT SWITCH for public 57, 58, 36, 31 and 32 and moves the creature from the flipper and Start buttons. The Laser Kick Test fires 9, 4, 7, 1 and 5
when 29, 35, 55, 56 and 61 close. Switch 62 and the other Not Used addresses are named NOT USED by the ROM, and the matrix is read uncomplemented:
public 1 is the active closure.

## Printed names the ROM corrects

The manual's lamp matrix prints a bare "Map" at 6 (the ROM: BARYONYX - MAP), "#2" at 50 (GALLIMIMUS), a "C" arch at 48 (ARCH "E", completing the
T-R-E-X arch letters 2, 47, 48, 60), "Raptor Multi-Million" at 20 (the ROM and the artwork say Mosquito Multi Millions, the game's Mosquito Millions
round) and "Jackpot Map" at 30 (JACKPOT RAMP, beside Jackpot Loop at 29). The matrix also prints "Smart Bomb" where the ROM says Smart Missile at 42 and 64 and
"Right Saucer Eject" where the ROM says TOP RIGHT EJECT at 56. The retained legacy definition mislabelled 9 as Drain, numbered the trough backwards, called 15 a
shooter-lane lockout, called 37 a scoop trough and gave 52 the Gallimimus name; the stable IDs are kept for compatibility but the labels follow the factory and the ROM.
Legacy lamp numbers 100-128 appear to be script-side SetLamp helper numbers, not controller lamps (the PinMAME lamp range here is 1-64).

## Switches, lamps and outputs

The 64-address Data East matrix is column-major (public n = 8 x (column - 1) + row), CPU connectors CN8 (strobes, with a key at 6) and CN10 (returns,
key at 4). Cabinet switches 1-7 are the coin-door and front-panel column, and the game has no ball-roll tilt. Six trough switches 9-14 hold six balls and 15 is a real seventh
contact at the release position; the table starts 9-14 closed. 41 and 42 are the shooter gun's trigger and smart-missile button and are not on the playfield. 63 and 64 are
read-only copies of the host buttons 84 and 82, which a consumer must drive instead. The upper right flipper shares the right button and has no ROM output, EOS or button.

Outputs 1-9 are left-set coils and 25-32 their right-set flash banks: drives 1-8 share transistors and the PPB left/right relay (public 10) routes
them. Each right-set bank draws four bulbs; the manual's printed bulb text, the ROM's own names (4-ORBIT, 3-POPS 1-TREX, TOP RGT. RMP 1.3.5) and the
table agree on where they are, except that the ROM counts one raptor-pit bulb fewer than the schematic in bank 1R. Only their playfield bulbs are placed. Output 11 is a physical general-illumination relay (K-1): asserting it cuts GI, although
PinMAME models it as a reversed #44 6.3 VAC brightness output. The manual fuses four 6.3 VAC GI strings (F1 Playfield, F2 Backbox Door & Speaker Panel, F3 Playfield
& Coin Door, F4 Backbox Door) but gives no socket count. Outputs 12-15 are the T-Rex direction and motor relays and 13 the jaw coil; 16 is the trough lock-out; 17-21 the turbo
bumpers and slingshots, and 22 the cabinet shaker. Output 23 is the game-on / switched-solenoid enable, 24, 33-36 and 50 dead addresses, 45-48 PinMAME's synthetic flipper
states (only while 23 is on), 49 the shared simulator output and 51-64 return zero. The raw printer bits 37-44 are published but never observed and the manual documents no printer.

Lamps 1-64 are all fitted. The credit button lamp (9) is in the cabinet; 1, 10, 19, 28, 46, 55 and 64 print (2 Bulbs); 31, 32 and 62 are the turbo-bumper bulbs; 41-45 spell CHAOS.
The retained table lights 31, 32 and 62 from the bumper solenoids as an effect, drives lamps through Controller.ChangedLamps with nFadeL/nFadeLm twins for glow, and models only a coloured
glow for the left, center and right scoop and gate lamps (17, 18, 33, 34, 57, 58, 46), which therefore have no placement.

## Recreation notes

The retained Dark & Friends 1.03 table starts the T-Rex homed (36 and 57 closed) and the trough with six balls, ties 23 to its nudge logic, drives the flippers from the synthetic outputs
46 and 48 (sLRFlipper, sLLFlipper) and simulates the toy's switches from the up/down and rotation motor outputs. The ROM's power-up T-Rex diagnostic needs that: with 36 and 57 closed it runs 14, 15, 13 and 12 and goes on, with them open it drives 14 for about
3.4 s and starts nothing else. A recreation must therefore present the dinosaur's position switches to the ROM, not just move a model.

"""
    for mechanism in machine["mechanisms"]:
        text += f"## {mechanism['label']}\n\n{mechanism['behavior']}\n\n"
    text += (
        "## Evidence and remaining work\n\n"
        f"Factory transcriptions and crops: {EXCERPTS}/. Exact object locators and hashes: tools/jurassic_park_geometry.json. Runtime "
        "readings, hashes and expected transitions: tools/jurassic_park_runtime.json, with the reusable scenarios tools/harness-scenarios/"
        "data-east/jupk-513-*.json and the DMD title adapter tools/jurassic_park_harness.py. Complete originals, extraction manifests, ROM inventory, "
        "fresh-state traces and native renders remain under the external working root. Remaining: the fitted GI sockets; the raw printer bits; "
        "a callout check or second table to validate the placements; the seven trough contacts' positions.\n")
    return text


def artifacts() -> dict[Path, bytes]:
    machine = build()
    result = {
        Path(f"machines/partial/{STEM}.json"): canonical_bytes(machine),
        Path(f"tools/seeds/{STEM}.json"): canonical_bytes(machine),
        Path(f"knowledge/{STEM}.md"): knowledge(machine).encode(),
        Path(f"reports/spatial/{STEM}.json"): canonical_bytes(report(machine)),
    }
    result.update({Path(f"{EXCERPTS}/{name}"): text.encode() for name, text in transcriptions().items()})
    return result


def verify_external(working: Path) -> None:
    from build_external_evidence_manifest import check_manifest
    extraction = working / "vpx-sources" / TABLE_SUBDIR
    files = [{"path": p.relative_to(extraction).as_posix(), "size_bytes": p.stat().st_size,
              "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
             for p in sorted(extraction.rglob("*"), key=lambda p: p.relative_to(extraction).as_posix()) if p.is_file()]
    digest = hashlib.sha256(json.dumps(files, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if digest != EXTRACTION_MANIFEST or len(files) != EXTRACTION_FILES or sum(f["size_bytes"] for f in files) != EXTRACTION_BYTES:
        raise ValueError("Complete VPX extraction manifest drift")
    for record in GEOMETRY["objects"].values():
        if hashlib.sha256((extraction / record["file"]).read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError("Geometry source file drift")
    table = working / "vpx-sources" / TABLE_FILE
    if hashlib.sha256(table.read_bytes()).hexdigest() != TABLE_SHA:
        raise ValueError("Retained table drift")
    manual = working / "manuals" / "by-machine" / KEY / "ipdb" / MANUAL_FILENAME
    if hashlib.sha256(manual.read_bytes()).hexdigest() != MANUAL_SHA:
        raise ValueError("Factory manual drift")
    for record in MANUAL_PROVENANCE["records"]:
        path = working / "manuals" / record["relative_path"]
        if path.stat().st_size != record["bytes"] or hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError(f"Retained document acquisition drift: {record['original_filename']}")
    for source in sources(transcriptions()):
        uri = source["uri"]
        if uri.startswith("external:"):
            path = working / uri.removeprefix("external:").replace("pinmame-review-artifacts/", "review-artifacts/", 1)
        elif source["id"] == PIN:
            path = pinmame_source_at(REVISION, ROOT) / "src/wpc/degames.c"
        elif source["id"] in PIN_REFS[1:]:
            path = pinmame_source_at(REVISION, ROOT) / "src/wpc" / PIN_FILES[PIN_REFS[1:].index(source["id"])][0]
        elif source["id"] in (CORPUS, VPW):
            path = working / "source-checkouts/vpxtable_scripts" / (CORPUS_FILE if source["id"] == CORPUS else VPW_FILE)
        else:
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"Retained source drift: {source['id']}")
    runtime = working / "review-artifacts" / KEY / "session-20261001" / "runtime"
    import jurassic_park_runtime
    if json.dumps(jurassic_park_runtime.build(runtime), indent=2, sort_keys=True, ensure_ascii=False) + "\n" != \
            (ROOT / "tools/jurassic_park_runtime.json").read_bytes().decode().replace("\r\n", "\n"):
        raise ValueError("Runtime summary drift")
    if check_manifest(runtime, "jupk_513") != RUNTIME_PROVENANCE["manifest"]["sha256"]:
        raise ValueError("Runtime directory manifest drift")
    library = Path("E:/_vpe-2025/pinmame/build-p2k-current/Release/pinmame64.dll")
    if library.is_file() and hashlib.sha256(library.read_bytes()).hexdigest() != RUNTIME_PROVENANCE["library_sha256"]:
        raise ValueError("Retained pinned DLL drift")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--evidence-root", type=Path)
    args = parser.parse_args()
    if (args.repository_root / f"machines/author-ready/{STEM}.json").exists():
        raise ValueError("Refusing to overwrite an existing author-ready artifact")
    for path, payload in artifacts().items():
        target = args.repository_root / path
        if args.check:
            if not target.is_file() or target.read_bytes().replace(b"\r\n", b"\n") != payload:
                raise ValueError(f"Curator drift: {path}")
        else:
            write_bytes(target, payload)
    for stem, digest, _ in IMAGES.values():
        if hashlib.sha256((args.repository_root / f"{EXCERPTS}/{stem}.webp").read_bytes()).hexdigest() != digest:
            raise ValueError(f"Factory diagram crop drift: {stem}")
    if args.evidence_root:
        verify_external(args.evidence_root)
    print("Jurassic Park artifacts match; partial blockers remain explicit.")


if __name__ == "__main__":
    main()
