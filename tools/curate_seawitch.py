#!/usr/bin/env python3
"""Deterministic, fail-closed Seawitch curation.

Reviewed facts, geometry candidates and provenance are pinned inputs. Generation
does not read external roots or recalculate evidence hashes to bless drift.
--check checks all products and excerpts; --verify-evidence checks exact retained
sources, every extraction file and the independently recomputed runtime bundle.
An existing author-ready record is never overwritten or removed.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_game_defs.spatial import _round_point
from pinmame_game_defs.validation import validate_machine
from build_external_evidence_manifest import check_manifest, build_manifest
import seawitch_data as data

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = data.MACHINE_ID
DEFINITION = Path("machines/partial/stern/seawitch-1980.json")
AUTHOR_READY = Path("machines/author-ready/stern/seawitch-1980.json")
SEED = Path("tools/seeds/stern/seawitch-1980.json")
GEOMETRY = Path("tools/seeds/stern/seawitch-1980-geometry.json")
CROPS = Path("tools/seeds/stern/seawitch-1980-crops.json")
PROVENANCE = Path("tools/seeds/stern/seawitch-1980-provenance.json")
KNOWLEDGE_SEED = Path("tools/seeds/stern/seawitch-1980-knowledge.md")
KNOWLEDGE = Path("knowledge/stern/seawitch-1980.md")
REPORT = Path("reports/spatial/stern/seawitch-1980.json")
REPORT_MD = Path("reports/spatial/stern/seawitch-1980.md")
RUNTIME = Path("evidence/runtime/stern/seawitch-diagnostics-and-gameplay.json")
CORE = "pinmame.core.97aa922bf8e4"
MANUAL = "manual.seawitch.1980"
SCHEMATIC = "manual.seawitch.schematics"
TABLE = "vpx-table.seawitch.archive-2-0-0"
SCRIPT = "vpx-script.seawitch.archive-2-0-0"
SELF_TEST = "runtime.seawitch.self-test"
SWITCH_TEST = "runtime.seawitch.switch-test"
GAMEPLAY = "runtime.seawitch.gameplay"
IPDB = "ipdb.seawitch.2089"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def provenance(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def aliases(channel: str, address: int) -> list[dict]:
    provider_channel = "solenoid" if channel == "coil" else channel
    result = [{"namespace": f"pinmame.{provider_channel}", "value": str(address)}]
    if address > 0 and channel in ("switch", "coil", "lamp"):
        result += [{"namespace": f"vpe-legacy.{channel}", "value": value}
                   for value in dict.fromkeys((str(address), f"{address:02}", f"{address:03}"))]
    return result


def located(identifier: str, role: str, names: list[str], geometry: dict) -> dict:
    points = []
    for index, name in enumerate(names, 1):
        obj = geometry["objects"][name]
        points.append({"id": f"{identifier}.{role}.{index}", "role": role, "space": "playfield",
                       "x": _round_point((obj["x"] - geometry["bounds"]["left"]) / data.TABLE_WIDTH),
                       "y": _round_point((obj["y"] - geometry["bounds"]["top"]) / data.TABLE_HEIGHT),
                       "provenance": provenance(TABLE, SCRIPT, MANUAL, SCHEMATIC, status="observed")})
    return {"status": "observed", "placements": points}


def switch_anchor(address: int) -> str:
    return {9: "Bumper1", 10: "Bumper2", 12: "LeftSlingShot", 13: "RightSlingShot", 14: "Bumper3", 33: "Drain"}.get(address, f"sw{address}")


def build_inputs(geometry: dict) -> list[dict]:
    result = []
    for address, label, kind, availability in [(-7, "Self test", "switch", "used"), (-6, "MPU S33 / CPU diagnostic NMI", "switch", "used"), (-5, "ST300 sound diagnostic / voice-select state", "virtual", "used")]:
        identifier = {-7: "switch.self-test", -6: "switch.mpu-diagnostic-s33", -5: "input.sound-diagnostic-voice-select"}[address]
        item = {"id": identifier, "label": label, "kind": kind, "binding": {"group": "pinmame.input.switch", "device": address},
                "aliases": aliases("switch", address), "availability": availability,
                "provenance": provenance(CORE, MANUAL, SCHEMATIC), "spatial": na("virtual" if address == -5 else "cabinet_or_service", CORE, MANUAL),
                "physical": {"notes": "The generic sound-diagnostic input is consumed by the ST300 st300_switch_w handler, which stores voiceSw for st300_ctrl_w; it is a meaningful emulator route. No fitted Seawitch sound-diagnostic button is established here. Do not infer physical fitment from that route."}}
        if address in (-7, -6):
            item.update(normally_closed=False, pulse=False, roles=["service.test"])
            item["physical"].update(switch_type="button", location="Inside coin door" if address == -7 else "MPU board",
                                    notes="Self Test: normally-open coin-door button A4J3-1 (R) to A3J2-7 (Y-R)." if address == -7 else "On-board S33 pushbutton pulls the 6800 NMI input low in the MPU circuit. PinMAME's generic CPU Diagnostic input asserts that NMI. The assembly drawing calls S33 MEMORY CLEAR. Its separate remote door contact at A4J3-5 is recorded outside the public matrix API; no equivalence of those two electrical paths is assumed.")
        result.append(item)

    for address, label in enumerate(data.SWITCH_LABELS, 1):
        unused = address in data.UNUSED_SWITCHES
        identifier = "switch." + (f"unused-{address}" if unused else slug(label))
        item = {"id": identifier, "label": label, "kind": "switch",
                "binding": {"group": "pinmame.input.switch", "device": address}, "aliases": aliases("switch", address) + [{"namespace": "manual.self-test", "value": str(address)}],
                "availability": "unused" if unused else "used", "provenance": provenance(MANUAL, SCHEMATIC, CORE, SWITCH_TEST)}
        if unused:
            item["physical"] = {"notes": "The game's switch-identification table explicitly marks this position unused (26 literally 'No Used'); its test number still appears in the ROM's full matrix sweep. No physical contact is inferred from ROM recognition."}
            item["spatial"] = na("unused", MANUAL, SCHEMATIC)
        else:
            item.update(normally_closed=False, pulse=address in {5, 9, 10, 12, 13, 14, 17, 18, 19, 20})
            switch_type = "tilt" if address in (7, 8) else "button" if address in (4, 6, 25) else "leaf"
            item["physical"] = {"switch_type": switch_type, "notes": "Normally-open contact in this game's matrix/cabinet drawing, with a series 1N4004 diode. The unmasked BY35 row-read path and the ROM's switch diagnostic agree: use public 1 for closure; do not invert the public state again."}
            if address in data.CABINET_SWITCHES:
                wire, pin = data.CABINET_RETURNS[address]
                item["wiring"] = {"board": "MPU A4", "control_wire": "R-Y", "control_connection": "A4J3-2", "return_wire": wire, "return_connection": f"A4J3-{pin}"}
                item["physical"]["location"] = "Cabinet / coin door / tilt board"
                if address != 8:
                    item["spatial"] = na("cabinet_or_service", MANUAL, SCHEMATIC)
                if address == 7:
                    item["physical"].update(quantity=2, notes="Roll tilt and pendulum tilt share public 7 (manual p19); both are normally open on the cabinet drawing. Tilt drops flipper-enable relay public 19 in the retained game.")
                    item["roles"] = ["cabinet.tilt"]
                if address == 8:
                    item["physical"]["notes"] += " Manual p5 describes door, tilt-board and playfield slam contacts and allows operator additions; p19 lists the first two outside the playfield. The playfield contact is not located by the retained geometry, so the aggregate has no not_applicable spatial record and no asserted total quantity."
                if address in (1, 2, 3):
                    item["roles"] = [f"cabinet.coin-{address}"]
                if address == 6:
                    item["roles"] = ["cabinet.start"]
            else:
                strobe, row = divmod(address - 1, 8)
                sw, sp = data.STROBES[strobe]
                rw, rp = data.RETURNS[row]
                item["wiring"] = {"board": "MPU A4", "control_wire": sw, "control_connection": f"A4J2-{sp}", "return_wire": rw, "return_connection": f"A4J2-{rp}"}
                item["spatial"] = located(identifier, "sensor", [switch_anchor(address)], geometry)
                item["provenance"]["source_refs"] += [SCRIPT, GAMEPLAY]
                if address in (12, 13):
                    item["physical"]["notes"] += " Spatial anchor is the mean of the sling wall's drag-point vertices, a projection onto the rubber mechanism, not a measured leaf-contact position."
                if address == 13:
                    item["physical"]["notes"] += " Retained 2.0.0 table defect: RightSlingShot_Slingshot pulses 42, outside the game's matrix. Factory switch 13 and the ROM response (public coil 5) settle the correct binding."
                if address == 33:
                    item["initial_active"] = True
                    item["physical"]["notes"] += " Single-ball out-hole switch starts closed with the ball present. Drain is the table's ball-collection proxy, not a measured leaf or hidden kicker socket; its coordinate is an observed projection only."
                if address in (4, 25):
                    item["physical"].update(part_number="4B-275", quantity=1)
                if address in {21, 22, 23, 24, 29, 30, 31, 32, 38, 39, 40}:
                    item["physical"]["notes"] += " Latches closed while its drop target is down; release after the bank reset physically raises it."
        result.append(item)

    for address, side in ((82, "right"), (84, "left"), (81, "upper-right"), (83, "upper-left")):
        used = address in (82, 84)
        identifier = "switch." + side + "-flipper-button" if used else "input.unused-" + side + "-flipper-position"
        item = {"id": identifier, "label": side.title().replace("-", " ") + (" flipper button" if used else " generic flipper position (unused)"),
                "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": address},
                "aliases": aliases("switch", address), "availability": "used" if used else "unused",
                "provenance": provenance(CORE, MANUAL, SCHEMATIC, GAMEPLAY),
                "spatial": na("cabinet_or_service" if used else "unused", CORE, MANUAL),
                "physical": {"notes": "Two cabinet buttons each operate two physical flippers. The driver declares FLIP_SW(FLIP_L) only; the upper generic positions have no independent button and cannot reach the CPU's row-read path. Upper physical flippers share the lower callback of their side. This is a static read-path proof, corroborated by the game probe; absence of a transition alone is not the proof."}}
        if used:
            item.update(normally_closed=False, pulse=False, roles=[f"flipper.button.{side}"])
            item["physical"].update(switch_type="button", quantity=1)
            item["wiring"] = {"board": "Hard-wired cabinet flipper circuit", "control_connection": "A3J2-2" if side == "left" else "A3J2-1", "control_wire": "BLU" if side == "left" else "R"}
        result.append(item)

    for address, label in sorted(data.DIPS.items()):
        result.append({"id": f"dip.option-{address}", "label": label, "kind": "dip_switch",
                       "binding": {"group": "pinmame.input.dip", "device": address}, "aliases": aliases("dip", address) + [{"namespace": "manual.address", "value": f"S{address}"}],
                       "availability": "unused" if address in (5, 13) else "used", "physical": {"switch_type": "dip", "location": "MPU option-switch banks in backbox", "notes": "Physical S1-S32 option switch. Grouped pricing/award settings and every printed ON/OFF combination are retained in the options excerpt; S33 is a separate memory-clear pushbutton."},
                       "provenance": provenance(MANUAL, CORE), "spatial": na("dip_switch", MANUAL)})
    for address, side, names in ((1, "left", ["LeftFlipper", "LeftFlipper1"]), (2, "right", ["RightFlipper", "RightFlipper1"])):
        identifier = f"switch.{side}-flipper-winding-bypass-contacts"
        result.append({"id": identifier, "label": f"{side.title()} flipper winding-bypass EOS contacts", "kind": "switch", "binding": {"group": "physical.input.direct", "device": address},
                       "aliases": [{"namespace": "manual.address", "value": f"{side}-flipper-eos"}], "availability": "used", "normally_closed": True,
                       "physical": {"switch_type": "leaf", "quantity": 2, "notes": "One winding-bypass contact is drawn on each of the two dual-winding flippers on this side. Closed bypass at rest, opens at stroke to insert the hold winding. These hard-wired contacts are not MPU switches. Placed by projection on the lower and upper flipper pivots. The extra E.O.S.-labelled series marks in the pair returns are preserved in the circuit excerpt; no independent public channel or additional contact quantity is inferred from those marks."},
                       "provenance": provenance(MANUAL, SCHEMATIC), "spatial": located(identifier, "sensor", names, geometry)})
    result.append({"id": "switch.remote-memory-clear", "label": "Remote S33 memory clear", "kind": "switch",
                   "binding": {"group": "physical.input.direct", "device": 3}, "aliases": [{"namespace": "manual.address", "value": "remote-s33"}],
                   "availability": "used", "normally_closed": False, "pulse": False,
                   "physical": {"switch_type": "button", "location": "Inside coin door", "notes": "Normally-open MEMORY CLEAR S33 contact on the cabinet sheet, A4J3-5 W to A3J2-7 Y-R. The MPU sheet labels J3-5 EXT. BOOKKEEPING RESET. It is distinct from matrix switches and the separately drawn on-board NMI pushbutton. This profile-local physical binding has no controller transport; no ROM effect is claimed from a host matrix write."},
                   "wiring": {"board": "MPU external bookkeeping-reset circuit", "control_connection": "A4J3-5", "control_wire": "W", "return_connection": "A3J2-7", "return_wire": "Y-R"},
                   "provenance": provenance(MANUAL, SCHEMATIC, CORE), "spatial": na("cabinet_or_service", MANUAL, SCHEMATIC)})
    return result


def build_outputs(geometry: dict) -> list[dict]:
    result = []
    physical_to_public = dict(zip(data.PUBLIC_TO_Q, data.SOLENOID_ADDRESSES))
    for q, label, connection, wire, part, anchor in data.COILS:
        address = physical_to_public[q]
        unused = label == "OPEN"
        kind = "relay" if q == 15 else "coil"
        identifier = f"output.unfitted-solenoid-{address}" if unused else kind + "." + slug(label)
        note = f"Physical SDU transistor/test position Q{q}; public {address}. The public order is derived from this game's U2 74154 and PB4-PB7 wiring, then checked against burn-in and the isolated gameplay actions."
        if unused:
            note += " Factory chart prints OPEN and the driver drawing supplies no load. Burn-in still pulses it without establishing a fitted coil."
            if address in (17, 20):
                note += " The gameplay run also records [1, 0] during boot stabilization, before any scripted input. These are startup transitions on continuous PIA PB4/PB7 lines, exposed by by35.c pia1b_w's inverted high-nibble export, rather than diagnostic-only activity. No particular ROM instruction or fitted load is inferred."
            else:
                note += " Its retained activity is the diagnostic decoder sweep."
        if q == 3:
            note += " Cabinet drawing prints B-Y, whereas the SDU connector annotation prints G-B for this same knocker. Structured wire follows the game's cabinet wiring; this wiring-detail disagreement does not change identity or fitment."
        if q == 14:
            note += " The table callback ejects ballrelease in the shooter lane. That kicker is a virtual serve destination, not the hidden physical out-hole coil. The observed effect anchor is instead projected on Drain, where the ball enters the out-hole model."
        if q in (4, 8, 13):
            note += " Effect is projected on a member of its own drop bank; it is not a measured under-playfield coil centre. The bank's complete geometry and reset behavior are in the mechanism record."
        wiring = {"board": "SDU B-432-FJ A3", "driver_transistor": f"Q{q}", "drive_connection": "A3" + connection,
                  "nominal_voltage_v": 43, "voltage_type": "dc"}
        if wire:
            wiring["drive_wire"] = wire
        physical = {"notes": note}
        if part:
            physical["part_number"] = part
            physical["quantity"] = 1
        item = {"id": identifier, "label": label if not unused else f"OPEN SDU Q{q}", "kind": kind,
                "binding": {"group": "pinmame.output.solenoid", "device": address},
                "aliases": aliases("coil", address) + [{"namespace": "manual.self-test", "value": str(q)}, {"namespace": "manual.address", "value": f"SDU-Q{q}"}],
                "availability": "unused" if unused else "used", "physical": physical, "wiring": wiring,
                "provenance": provenance(SCHEMATIC, MANUAL, CORE, SELF_TEST, GAMEPLAY)}
        if unused:
            item["spatial"] = na("unused", MANUAL, SCHEMATIC, SELF_TEST)
        elif q in (3, 19):
            item["spatial"] = na("cabinet_or_service", MANUAL, SCHEMATIC)
        elif q == 15:
            item["spatial"] = na("internal_nonvisual", MANUAL, SCHEMATIC)
            item["roles"] = ["game.on", "flipper.enable"]
        else:
            item["spatial"] = located(identifier, "effect", [anchor], geometry)
        result.append(item)

    for side, held, power, names in (("right", 46, 45, ["RightFlipper", "RightFlipper1"]), ("left", 48, 47, ["LeftFlipper", "LeftFlipper1"])):
        identifier = f"coil.{side}-flippers"
        result.append({"id": identifier, "label": f"{side.title()} flippers (lower and upper)", "kind": "coil",
                       "binding": {"group": "pinmame.output.solenoid", "device": held}, "aliases": aliases("coil", held), "availability": "used",
                       "physical": {"quantity": 2, "notes": "Lower coil J-25-475/34-4500 and upper coil J-25-600/34-4500 (factory parts list). Two physical flippers share this side's button and callback. The physical +43 V circuit is gated by SDU Q15's relay. PinMAME's paired outputs are simultaneous held button states; they do not model winding current, EOS timing or an independent upper flipper command."},
                       "wiring": {"board": "Hard-wired flipper pair", "drive_connection": "A3J1-8" if side == "left" else "A3J1-9", "drive_wire": "G" if side == "left" else "O", "power_connection": "A2J1-6", "power_wire": "BLU-W", "nominal_voltage_v": 43, "voltage_type": "dc"},
                       "provenance": provenance(MANUAL, SCHEMATIC, CORE, SCRIPT, GAMEPLAY), "spatial": located(identifier, "effect", names, geometry)})
        result.append({"id": f"output.{side}-flipper-power-state", "label": f"{side.title()} synthetic flipper power state", "kind": "virtual",
                       "binding": {"group": "pinmame.output.solenoid", "device": power}, "aliases": aliases("coil", power), "availability": "used",
                       "physical": {"notes": f"Meaningful synthetic state, asserted and released with {held} for the full enabled button closure. This is not another physical coil, nor a measured power winding."},
                       "provenance": provenance(CORE, GAMEPLAY), "spatial": na("virtual", CORE, GAMEPLAY)})

    q_to_public = {q: 16*k + a + 1 for k, group in enumerate(data.DECODER_SCRS) for a, q in enumerate(group)}
    loads: dict[int, list[tuple]] = {}
    for label, wire, jack, pin in data.LAMP_ROWS:
        q = data.LDA_CONNECTORS[jack][int(pin)]
        loads.setdefault(q_to_public[q], []).append((label, wire, jack, int(pin)))
    for q, address in sorted(q_to_public.items(), key=lambda row: row[1]):
        rows = loads.get(address, [])
        known = bool(rows)
        label = "Shoot again (playfield and backbox)" if len(rows) == 2 else rows[0][0].capitalize() if known else f"Unresolved load on LDA SCR Q{q}"
        identifier = "lamp." + ("shoot-again" if len(rows) == 2 else slug(rows[0][0]) if known else f"unresolved-scr-q{q}")
        k, s = divmod(address - 1, 16)
        note = f"Discrete SCR Q{q}, decoder U{k+1} output S{s}, resistor R{q}; public {address}. Connector branches do not establish a bulb quantity."
        if known:
            note += " Game-specific printed load: " + "; ".join(f"{r[0]} ({r[2]}-{r[3]}, {r[1]})" for r in rows) + "."
            if address == 11:
                note += " The driver list calls J2-21 SHOOT AGAIN (INSERT); the separate bottom row and playfield sheet identify J1-26 as PLAYFIELD, so INSERT is the backbox insert-panel lamp. The two locations share Q3."
        else:
            note += " No load is named in either of this game's two lamp lists. Omission and runtime silence do not prove non-fitment. Availability remains unknown. Public 51 changes in the retained game as well as burn-in; the other three appear in burn-in only. A socket/harness trace is needed for fitment."
        wiring = {"board": "LDA-100 B-431 A5", "driver_transistor": f"Q{q}", "drive_connection": "; ".join(f"A5{r[2]}-{r[3]}" for r in rows) if known else "; ".join(f"A5{jack}-{pin}" for jack, pins in data.LDA_CONNECTORS.items() for pin, scr in pins.items() if scr == q)}
        if known:
            wiring["drive_wire"] = rows[0][1]
        physical = {"notes": note}
        if known:
            physical["part_number"] = "#44 (8A-101)"
        backbox = known and rows[0][0] in ("GAME OVER", "HIGH SCORE TO DATE", "MATCH", "TILT")
        item = {"id": identifier, "label": label, "kind": "lamp", "binding": {"group": "pinmame.output.lamp", "device": address},
                "aliases": aliases("lamp", address) + [{"namespace": "manual.address", "value": f"LDA-Q{q}"}],
                "availability": "used" if known else "unknown", "physical": physical, "wiring": wiring,
                "provenance": provenance(SCHEMATIC, CORE, SELF_TEST, GAMEPLAY, status="validated" if known else "candidate")}
        if len(rows) == 2:
            physical["location"] = "Playfield and backbox insert-panel loads; total socket quantity not established"
        elif backbox:
            physical["location"] = "Backbox insert panel"
            item["spatial"] = na("cabinet_or_service", MANUAL, SCHEMATIC, IPDB)
        # All retained lN objects are overlays with no bulb mesh. They stay in
        # the report's candidate register, never canonical emitter placements.
        result.append(item)
    result.append({"id": "gi.general-illumination", "label": "Uncontrolled general illumination", "kind": "gi", "binding": {"group": "physical.output.gi", "device": 1},
                   "aliases": [], "availability": "used", "physical": {"notes": "Transformer-fed general illumination, with playfield and front-door wiring on this game's sheets and backbox lamps corroborated by the retained physical photograph. Playfield drawing: A2J1-8 W to A2J1-1 R, labelled 6 VAC. Exact backbox harness pins are not established from the generic transformer drawing. No ROM relay, lamp address or PinMAME GI callback controls this circuit. The table's 54 GI collection occurrences contain a duplicate and render helpers; they prove neither bulb quantity nor socket positions. Quantity and playfield emitter coordinates remain unset."},
                   "wiring": {"board": "Transformer/rectifier A2, uncontrolled GI circuit", "power_connection": "A2J1-8 (playfield); A2J2-1 (front door)", "return_connection": "A2J1-1; A2J2-5", "voltage_type": "ac", "nominal_voltage_v": 6},
                   "provenance": provenance(MANUAL, SCHEMATIC, IPDB)})
    return result


def build_mechanisms(inputs: list[dict], outputs: list[dict]) -> tuple[list[dict], list[dict]]:
    switches = {i["binding"]["device"]: i["id"] for i in inputs if i["binding"]["group"] == "pinmame.input.switch"}
    coils = {i["binding"]["device"]: i["id"] for i in outputs if i["binding"]["group"] == "pinmame.output.solenoid"}
    mechanisms, relationships = [], []
    def add(identifier, label, kind, actuators, sensors, behavior, part=None):
        item = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
                "provenance": provenance(MANUAL, SCHEMATIC, CORE, SCRIPT, GAMEPLAY)}
        if part:
            item["assembly_part_number"] = part
        mechanisms.append(item)
    for name, label, addresses, coil, part in [("center", "Center four-target bank", [21,22,23,24],7,"D-580-4B"), ("left", "Left three-target bank", [38,39,40],8,"D-580-3A"), ("top-right", "Top right four-target bank", [29,30,31,32],9,"D-580-4B")]:
        add(f"mech.{name}-drop-bank", label, "drop_target_bank", [coils[coil]], [switches[a] for a in addresses],
            f"Targets {addresses} run highest to lowest in player view. Each target drops independently, latching its normally-open switch closed. One common reset bar/coil raises the whole bank, opening its switches. The known script's bank initializer explicitly preserves this membership (the left/right arrays are listed in reverse object order). At game start the ROM resets all three banks. Completing this bank in the retained game pulses public {coil}; a host holds targets down until that reset and then releases them. Targets start up. Repeat reset attempts with a held switch or a ball remaining in the out-hole are documented ROM behavior, not extra reset actuators. A target stuck down or a jammed reset bar leaves its sensor closed; reproduce the physical feedback rather than clearing it on a timer. Bank completion spots the corresponding loop/extra-ball award and advances the bonus multiplier when its increase lamp is on. Physical reset-pulse width and target animation remain table tuning.", part)
        for address in addresses:
            relationships.append({"id": f"rel.reset-{name}-{address}", "kind": "pulse", "source": coils[coil], "destination": switches[address], "provenance": provenance(MANUAL, SCHEMATIC, SCRIPT, GAMEPLAY)})
    add("mech.outhole-and-launch", "Single-ball drain, outhole and manual launch", "kicker", [coils[10]], [switches[33]],
        "One ball and no storage trough. Drain routes the ball onto switch 33; initialize it occupied. Credit/start resets the three banks and kicks the out-hole until the ball leaves 33. Its physical eject feeds the shooter lane, where the player operates the manual plunger. The table's ballrelease kicker is the virtual destination of this feed, not another physical coil or switch. A ball still holding 33 produces repeat out-hole and bank-reset pulses; do not keep 33 closed after a successful serve. On drain the ROM counts bonus, advances player/ball and serves again; an earned extra ball is played immediately without advancing player/ball. Tilt suppresses that ball's bonus and flippers, returning to normal at the next serve. No powered plunger, shooter-lane sensor, multiball trough or eject-position feedback is fitted in these sources.")
    add("mech.spinner", "Right spinner", "rotary", [], [switches[5]], "Free-spinning target A-563-13, target/wire 14A-7-12. Each revolution closes switch 5 briefly; no coil or home sensor. Ball passes the spinner in the right runway. The four value lamps describe the ROM's value ladder; initial score is 200 plus 200 per lit value, up to 1,000 (manual p10).", "A-563-13")
    for address, label in ((4,"Rear loop star roll-over"),(25,"Runway star roll-over")):
        add(f"mech.star-{address}", label, "other", [], [switches[address]], "Passive ball-operated roll-over button 4B-275. Normally open, closed while depressed; no actuator, latch or separate home sensor. The top button scores the lit loop value; the runway button adds 3,000 bonus and can collect special (manual p10).", "4B-275")
    for sw, coil, label in ((9,1,"Top thumper"),(10,2,"Left thumper"),(14,11,"Right thumper"),(12,4,"Left slingshot"),(13,5,"Right slingshot")):
        add("mech."+slug(label),label,"kicker",[coils[coil]],[switches[sw]],f"Ball displaces the skirt/rubber and closes switch {sw}; the ROM fires public {coil}, mechanically striking the ball away. Spring return opens the switch. This pairing is isolated in the retained game. No independent position sensor or motor. A stuck contact can repeatedly request action; preserve ROM drive timing, with mechanical speed table-owned.")
        relationships.append({"id": f"rel.switch-{sw}-coil-{coil}", "kind": "pulse", "source": switches[sw], "destination": coils[coil], "provenance": provenance(MANUAL, SCHEMATIC, GAMEPLAY)})
    for side, button, held in (("left",84,48),("right",82,46)):
        eos = f"switch.{side}-flipper-winding-bypass-contacts"
        add(f"mech.{side}-flipper-pair",f"{side.title()} lower/upper flipper pair","other",[coils[held]],[switches[button],eos],
            "Two spring-return dual-winding flippers: one lower by the apron and one upper beside its target bank. The single cabinet button and flipper-enable relay supply the side's circuit. Four winding-bypass contacts (two per side) are drawn across hold windings, conducting at rest and opening at stroke; they are hard-wired and absent from MPU switch tests. Preserve the factory E.O.S. series marks literally rather than inventing another public channel. The retained table moves both flippers of the side on its one lower callback. PinMAME asserts both synthetic outputs together throughout an enabled button closure and does not simulate physical current, EOS staging or independent upper motion; mechanical stroke/return timing is table-owned.")
        relationships.append({"id": f"rel.enable-{side}-flippers", "kind": "relay_gated", "source": coils[19], "destination": coils[held], "provenance": provenance(SCHEMATIC, CORE, GAMEPLAY)})
    add("mech.runway-gate", "Passive runway gate", "gate", [], [], "Ball-operated gate beside the upper-right flipper/runway, with no solenoid or sensor binding. The script's SLS/SLS2 handlers animate a one-way barrier from ball direction and passage, with no SolCallback. This is passive ball routing; do not invent a powered diverter or controller output. Gate travel speed in the table is a recreation parameter.")
    return mechanisms, relationships


def build_definition(root: Path = ROOT) -> dict:
    geometry = load_json(root / GEOMETRY)
    required_sources = {CORE, MANUAL, SCHEMATIC, TABLE, SCRIPT, SELF_TEST, SWITCH_TEST, GAMEPLAY, IPDB}
    sources = load_json(root / PROVENANCE)["sources"]
    if not required_sources <= {source["id"] for source in sources}:
        raise RuntimeError("Seawitch provenance seed is incomplete")
    if len(data.SWITCH_LABELS) != 40 or set(data.DIPS) != set(range(1, 33)):
        raise RuntimeError("Seawitch switch/DIP inventory is incomplete")
    if {row[0] for row in data.COILS} != set(range(1, 20)) or len(data.COILS) != 19:
        raise RuntimeError("Seawitch SDU inventory is incomplete")
    if len(data.DECODER_SCRS) != 4 or any(len(group) != 15 for group in data.DECODER_SCRS) or {q for group in data.DECODER_SCRS for q in group} != set(range(1, 61)):
        raise RuntimeError("Seawitch LDA decoder inventory is incomplete or duplicated")
    if len(data.LAMP_ROWS) != 57 or geometry["bounds"] != {"left": 0, "top": 0, "right": 956, "bottom": 1979}:
        raise RuntimeError("Seawitch reviewed lamp table or coordinate frame is incomplete")
    inputs, outputs = build_inputs(geometry), build_outputs(geometry)
    mechanisms, relationships = build_mechanisms(inputs, outputs)
    drivers = []
    rows = [("seawitch", "Seawitch", "1980", "Stern"), ("seawitcha", "Seawitch (MOD rev. 5)", "2021", "Stern / Idleman"), ("seawitchb", "Seawitch (MOD rev. 6)", "2021", "Stern / Idleman"), ("seawitchc", "Seawitch (MOD rev. 7)", "2021", "Stern / Idleman"), ("seawitchd", "Seawitch (MOD rev. 8)", "2021", "Stern / Idleman"), ("seawitche", "Seawitch (MOD rev. 9)", "2023", "Stern / slochar"), ("seawitchf", "Seawitch (MOD rev. 9.3)", "2024", "Stern / slochar"), ("seawitfp", "Seawitch (Free Play)", "1980", "Stern")]
    for identifier, description, year, manufacturer in rows:
        item = {"id": identifier, "description": description, "year": year, "manufacturer": manufacturer, "flags": 0,
                "physical_compatibility": "identical", "variant_notes": "Same GEN_STMPU200, dispst7, FLIP_SW(FLIP_L), zero extra lamp columns/custom solenoids, ST300 and input_ports_st in the pinned per-driver declarations. Production hardware family; free-play/rules ROM revisions change firmware, not a physical edition. Only production seawitch was exercised; no measurements of modified-rule scoring are claimed."}
        if identifier != "seawitch":
            item["clone_of"] = "seawitch"
        drivers.append(item)
    displays = []
    for index, start, width, label in ((0,1,7,"Player 1"),(1,9,7,"Player 2"),(2,17,7,"Player 3"),(3,25,7,"Player 4"),(4,35,2,"Credits"),(5,38,2,"Match / ball in play")):
        displays.append({"id": "display."+slug(label), "label": label, "kind": "segment", "controller_index": index, "segment_start": start, "width": width, "height": 1,
                         "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", MANUAL, CORE, IPDB), "provenance": provenance(MANUAL, CORE, GAMEPLAY)})
    return {"format": "pinmame-machine-definition", "schema_version": 2,
            "machine": {"id": MACHINE_ID, "name": "Seawitch", "manufacturer": "Stern", "year": 1980, "model_number": "123", "ipdb_id": 2089, "opdb_id": "GR6kB-MDz81", "kind": "physical_pinball",
                        "playfield": {"width": data.TABLE_WIDTH, "height": data.TABLE_HEIGHT, "units": "vpx", "provenance": provenance(TABLE)}},
            "controller": {"platform": "pinmame.stern-mpu200", "hardware_generation": "0x1000000", "inversion_applied_by_emulator": True},
            "coverage": {"status": "partial", "missing": ["output_semantics", "spatial_placement"], "dimensions": {
                "catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate", "physical_wiring": "candidate", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "observed", "diagnostic_enumeration": "validated", "runtime_observation": "observed", "causal_exercise": "observed", "emulator_normalization": "validated"}},
            "drivers": drivers, "inputs": inputs, "outputs": outputs, "displays": displays, "mechanisms": mechanisms, "relationships": relationships,
            "sources": sources, "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "complete"}, "conflicts": []}


def build_report(definition: dict, root: Path = ROOT) -> dict:
    geometry = load_json(root / GEOMETRY)
    records = [*definition["inputs"], *definition["outputs"], *definition["displays"]]
    return {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
            "decision": "partial; no author-ready promotion", "coordinate_convention": "x=0 left, x=1 right; y=0 rear/backglass, y=1 apron; normalized VPX/player view",
            "bounds": geometry["bounds"], "normalization": "(x-left)/(right-left), (y-top)/(bottom-top), repository _round_point to six decimals",
            "evidence": {"table_sha256": data.TABLE_SHA256, "script_sha256": data.SCRIPT_SHA256, "vpxtool": "git:v0.33.3", "extraction_path": "external:pinmame-vpx-sources/"+data.EXTRACTION_RELATIVE, "manifest_algorithm": "tools/build_external_evidence_manifest.py; case-sensitive POSIX path order, compact canonical JSON plus LF, root manifest files excluded", "manifest_sha256": data.EXTRACTION_SHA256, "file_count": data.EXTRACTION_FILES, "total_bytes": data.EXTRACTION_BYTES, "geometry_seed": GEOMETRY.as_posix(), "geometry_seed_sha256": sha256(root / GEOMETRY), "crop_metadata": CROPS.as_posix(), "crop_metadata_sha256": sha256(root / CROPS), "runtime": RUNTIME.as_posix(), "runtime_sha256": sha256(root / RUNTIME)},
            "unresolved_records": [{"id": i["id"], "label": i["label"], "binding": i.get("binding"), "availability": i.get("availability")} for i in records if "spatial" not in i or i.get("availability") == "unknown"],
            "projections": ["Sling sensor/effect: mean of that mechanism wall's own drag-point vertices, not a leaf/coil survey.", "Drop reset effects: target member in their own bank, not a hidden coil socket.", "EOS winding-bypass contacts: corresponding lower and upper flipper pivots.", "Out-hole sensor/effect: Drain ball-collection proxy; ballrelease is the virtual shooter-lane serve destination and is excluded as a physical coil anchor."],
            "lamp_overlay_candidates": [{"object": name, **obj, "normalized_x": _round_point(obj["x"]/data.TABLE_WIDTH), "normalized_y": _round_point(obj["y"]/data.TABLE_HEIGHT), "reason": "Insert overlay, is_bulb_light=false and show_bulb_mesh=false; no canonical emitter coordinate."} for name,obj in geometry["objects"].items() if obj["type"] == "Light"],
            "blockers": ["Public lamps 29/Q15/J2-23, 41/Q42/J3-21, 51/Q51/J3-15 and 57/Q56/J3-10 have no printed load in either Seawitch list. All four fitments remain unknown; 51 changes during gameplay. Resolve by tracing an unrestored LDA harness/socket, not by another all-lamp sweep.", "The lN insert overlays do not model bulbs. Locate each real controlled-lamp socket using a bulb-level drawing or independently reconciled underside photograph; retain its measured centers and the transform. Shoot again has separate playfield/backbox loads on Q3.", "Uncontrolled GI is fitted but its emitter inventory/positions are unproved. The GI collection has 54 member occurrences, 53 distinct names and duplicate Light35; render/glow membership is not a socket count.", "Switches and coil effects have observed table geometry/projections only. The retained location diagrams have been visually reconciled for side/order/topology but no independent quantified control fit has validated coordinates. The playfield slam contact and hidden out-hole hardware remain unlocated."],
            "readiness": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"], "unresolved_conflicts": len(unresolved_conflicts(definition))}}


def render_report(report: dict) -> str:
    lines = ["# Seawitch (1980) spatial evidence", "", "**Decision: partial.** The contribution does not claim author-ready placement.", "", report["coordinate_convention"]+".", "", "Bounds: left 0, top 0, right 956, bottom 1979 VPX units. "+report["normalization"]+".", "", "## Evidence", "", f"Table SHA-256 `{data.TABLE_SHA256}`; embedded script `{data.SCRIPT_SHA256}`.", f"vpxtool git:v0.33.3 extraction: {data.EXTRACTION_FILES} files, {data.EXTRACTION_BYTES} bytes; canonical manifest `{data.EXTRACTION_SHA256}`.", "The JSON report pins the reviewed geometry seed, runtime bundle and crop metadata. Original PDFs, photographs, table and complete raw runs stay in the external evidence roots.", "", "## Projections", ""]
    lines += ["- "+s for s in report["projections"]]
    lines += ["", "## Remaining blockers", ""]+["- "+s for s in report["blockers"]]
    lines += ["", "## Unresolved records", "", "| Device | Label |", "| --- | --- |"]
    lines += [f"| `{i['id']}` | {i['label']} |" for i in report["unresolved_records"]]
    lines += ["", "The JSON candidate register preserves every lN overlay's exact raw coordinate, extracted file, normalized coordinate and exclusion reason. No overlay, GI glow, duplicate collection member or VPX Flasher object is counted as a physical emitter.", ""]
    return "\n".join(lines)


def verify_portable_evidence(root: Path = ROOT) -> None:
    metadata = load_json(root / PROVENANCE)
    drawing_excerpts = {}
    for source in metadata["sources"]:
        for excerpt in source.get("excerpts", []):
            if "image" in excerpt:
                drawing_excerpts[excerpt["id"]] = excerpt
            for field, digest_field in (("path", "sha256"), ("image", "image_sha256")):
                if field in excerpt and (not (root / excerpt[field]).is_file() or sha256(root / excerpt[field]) != excerpt[digest_field]):
                    raise RuntimeError(f"Seawitch excerpt missing or changed: {excerpt[field]}")
    crops = load_json(root / CROPS)
    if {"excerpt.seawitch." + name for name in crops} != set(drawing_excerpts):
        raise RuntimeError("Seawitch crop metadata inventory disagrees with the drawing excerpts")
    for name, crop in crops.items():
        excerpt = drawing_excerpts["excerpt.seawitch." + name]
        if any(crop[field] != excerpt[field] for field in ("image", "image_sha256", "image_derivation")) or crop["bytes"] != (root / crop["image"]).stat().st_size:
            raise RuntimeError(f"Seawitch crop metadata changed: {name}")
    if sha256(root / RUNTIME) != metadata["runtime_sha256"]:
        raise RuntimeError("Seawitch compact runtime evidence changed")


def verify_evidence(root: Path = ROOT) -> None:
    verify_portable_evidence(root)
    names = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
    if any(not os.environ.get(n) for n in names):
        raise RuntimeError("All Seawitch evidence roots must be configured for --verify-evidence")
    vpx, manuals, review = (Path(os.environ[n]) for n in names)
    extraction = vpx / data.EXTRACTION_RELATIVE
    digest = check_manifest(extraction, "seawitch")
    manifest = build_manifest(extraction, "seawitch")
    if (digest, len(manifest["files"]), sum(i["size"] for i in manifest["files"])) != (data.EXTRACTION_SHA256, data.EXTRACTION_FILES, data.EXTRACTION_BYTES):
        raise RuntimeError("Seawitch extraction identity changed")
    if sha256(vpx / data.TABLE_RELATIVE) != data.TABLE_SHA256 or sha256(extraction / "script.vbs") != data.SCRIPT_SHA256:
        raise RuntimeError("Seawitch retained table/script changed")
    for row in load_json(root / PROVENANCE)["external_manual_files"]:
        if sha256(manuals / "by-machine" / MACHINE_ID / row["filename"]) != row["sha256"]:
            raise RuntimeError(f"Seawitch manual/photo changed: {row['filename']}")
    native_path = review / MACHINE_ID / "native-and-rom-identity.json"
    if sha256(native_path) != load_json(root / PROVENANCE)["native_identity_sha256"]:
        raise RuntimeError("Seawitch native/ROM build identity record changed")
    native = load_json(native_path)
    if native["revision"] != data.PINMAME_REVISION or native["source_status"] or native["library_sha256"] != data.LIBRARY_SHA256 or native["rom_archive"]["sha256"] != data.ROM_SHA256:
        raise RuntimeError("Seawitch native/ROM identity disagrees with pinned evidence")
    library = review.parent / "builds/seawitch-pinned/Release/pinmame64.dll"
    if sha256(library) != data.LIBRARY_SHA256:
        raise RuntimeError("Seawitch retained native binary changed")
    from summarize_seawitch_runtime import build
    if canonical_bytes(build(review / MACHINE_ID / "harness")) != (root / RUNTIME).read_bytes():
        raise RuntimeError("Seawitch raw runtime evidence disagrees with the compact evidence")
    geometry = load_json(root / GEOMETRY)
    for name, obj in geometry["objects"].items():
        raw = load_json(extraction / obj["file"])
        value = raw.get(obj["type"], raw)
        from pinmame_game_defs.spatial import _item_point
        x, y, _ = _item_point(obj["type"], value)
        if (x, y) != (obj["x"], obj["y"]):
            raise RuntimeError(f"Seawitch coordinate drift: {name}")
        if obj["type"] == "Light" and (value["is_bulb_light"] or value["show_bulb_mesh"]):
            raise RuntimeError(f"Seawitch overlay classification drift: {name}")
    print("Seawitch retained files, complete extraction, coordinates and runtime match pinned evidence.")


def products(root: Path = ROOT) -> dict[Path, bytes]:
    verify_portable_evidence(root)
    definition = build_definition(root)
    errors = validate_machine(definition, root)
    if errors:
        raise RuntimeError("Invalid Seawitch contribution: " + "; ".join(errors))
    report = build_report(definition, root)
    return {DEFINITION: canonical_bytes(definition), SEED: canonical_bytes(definition),
            KNOWLEDGE: (root / KNOWLEDGE_SEED).read_bytes(), REPORT: canonical_bytes(report), REPORT_MD: render_report(report).encode("utf-8")}


def check(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY).exists():
        raise RuntimeError("Seawitch has an author-ready artifact despite unresolved fitment and spatial evidence")
    for path, payload in products(root).items():
        if not (root / path).is_file() or (root / path).read_bytes() != payload:
            raise RuntimeError(f"Seawitch deterministic artifact missing or drifted: {path}")
    print("Seawitch definition, seed, knowledge, excerpts and spatial reports match the deterministic curator.")


def generate(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY).exists():
        raise RuntimeError("Refusing to overwrite an author-ready Seawitch artifact")
    for path, payload in products(root).items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_bytes(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    mode.add_argument("--verify-evidence", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    elif args.verify_evidence:
        verify_evidence()
    else:
        generate()


if __name__ == "__main__":
    main()
