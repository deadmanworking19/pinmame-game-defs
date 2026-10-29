#!/usr/bin/env python3
"""Deterministic, partial Stars curation; no external reads during generation.

--verify-evidence separately checks retained bytes and recomputes the traces.
Neither generation nor checking blesses a changed evidence hash. Lamp Light
objects without physical bulb evidence remain report candidates, not sockets.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine
from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_game_defs.spatial import _item_point, _round_point
from build_external_evidence_manifest import build_manifest, check_manifest
from summarize_stars_runtime import build as runtime_build, COIL_TEST
from drawing_callouts import evaluate as evaluate_callouts, placements_of, verify_retained

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "stern.stars.1978"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
DEFINITION = Path("machines/partial/stern/stars-1978.json")
AUTHOR_READY = Path("machines/author-ready/stern/stars-1978.json")
SEED = Path("tools/seeds/stern/stars-1978.json")
EVIDENCE = Path("tools/seeds/stern/stars-1978-evidence.json")
LAMPS = Path("tools/seeds/stern/stars-1978-lamps.json")
COIL_DECODER = Path("tools/seeds/stern/stars-1978-coil-decoder.json")
CALLOUTS = Path("tools/seeds/stern/stars-1978-callouts.json")
PROVENANCE = Path("tools/seeds/stern/stars-1978-provenance.json")
KNOWLEDGE_SEED = Path("tools/seeds/stern/stars-1978-knowledge.md")
KNOWLEDGE = Path("knowledge/stern/stars-1978.md")
REPORT = Path("reports/spatial/stern/stars-1978.json")
REPORT_MD = Path("reports/spatial/stern/stars-1978.md")
RUNTIME = Path("evidence/runtime/stern/stars-diagnostics-and-gameplay.json")
CORE = "pinmame.stars.46e1a01a"
MANUAL = "manual.stars.103"
SCRIPT = "vpx-script.stars.primary"
TABLE = "vpx-table.stars.primary"
TRACE = "runtime.stars.original"
IDENTITY = "ipdb.stars.2366"
SWITCHES = {
    1: "Left spinner", 4: "Left outlane", 5: "Left return lane", 6: "Credit button",
    7: "Tilt", 8: "Outhole", 9: "Coin 3 right", 10: "Coin 2 center", 11: "Coin 1 left",
    12: "Right outlane", 13: "Right return lane", 15: "Bonus rollovers", 16: "Slam contacts",
    17: "Right spinner", 20: "Star 5", 21: "Star 4", 22: "Star 3", 23: "Star 2", 24: "Star 1",
    25: "Ten point rebounds", 27: "Drop target 5", 28: "Drop target 2", 29: "Drop target 6",
    30: "Drop target 4", 31: "Drop target 3", 32: "Drop target 1",
    36: "Right slingshot", 37: "Left slingshot", 38: "Thumper bumper",
}
COILS = {
    1: ("Ten point chime", "Q2", "A3J2-4 / A3J1-3", "W-B"),
    2: ("Hundred point chime", "Q1", "A3J2-9 / A3J1-2", "W-O"),
    3: ("Thousand point chime", "Q5", "A3J2-10", "W-BRN"),
    4: ("Ten thousand point chime", "Q6", "A3J2-11", "W-G"),
    5: ("Unfitted momentary driver 5", "Q7", "A3J2-12", ""),
    6: ("Knocker", "Q3", "A3J3-4 / A3J2-5", "BLU-Y"),
    7: ("Outhole kicker", "Q4", "A3J1-5", "BRN-Y"),
    8: ("Unfitted momentary driver 8", "Q8", "A3J5-10", ""),
    9: ("Left drop bank reset", "Q13", "A3J5-12", "R-W"),
    10: ("Upper right drop bank reset", "Q14", "A3J5-11", "O-W"),
    11: ("Unfitted momentary driver 11", "Q9", "A3J5-9", ""),
    12: ("Unfitted momentary driver 12", "Q10", "A3J5-15", ""),
    13: ("Thumper bumper", "Q12", "A3J5-13", "B-BLU"),
    14: ("Right slingshot", "Q11", "A3J5-14", "B-Y"),
    15: ("Left slingshot", "Q16", "A3J5-8 / A3J2-6 / A3J3-7", "R-B"),
    17: ("Unfitted continuous PB4", "Q17", "A3J5-7", ""),
    18: ("Coin lockout", "Q19", "A3J2-8", "Y-W"),
    19: ("Flipper enable relay", "Q15", "On-board flipper enable relay terminal 8", ""),
    20: ("Unfitted continuous PB7", "Q18", "A3J5-3 / A3J2-15 / A3J3-9", ""),
}
UNFITTED_COILS = {5, 8, 11, 12, 17, 20}
CABINET = {6, 7, 9, 10, 11}
DROP_SWITCHES = {27, 28, 29, 30, 31, 32}
DIP_LABELS = {
    **{i: "Center coin chute pricing" for i in range(1, 6)}, 6: "High score award", 7: "Balls per game",
    8: "Chime melody", **{i: "Right coin chute pricing" for i in range(9, 14)},
    14: "Not used", 15: "High game to date", 16: "Left coin chute pricing",
    17: "Maximum credits", 18: "Maximum credits", 19: "Maximum credits", 20: "Credit display",
    21: "Match feature", 22: "Bonus countdown", 23: "Not used", 24: "Target sets down for triple bonus",
    25: "Two or four player operation", 26: "Extra ball enable", 27: "Multiplayer enable bulletin 8",
    28: "Not used", 29: "Not used", 30: "Star special selection", 31: "Special award", 32: "Special award",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def prov(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def device(channel: str, address: int, label: str, kind: str, refs: tuple[str, ...],
           availability: str = "used", group: str | None = None, status: str = "validated") -> dict:
    group = group or f"pinmame.{'input' if channel in ('switch', 'dip') else 'output'}.{channel}"
    aliases = [{"namespace": f"pinmame.{channel}", "value": str(address)}] if group.startswith("pinmame.") else []
    if channel in ("switch", "solenoid", "lamp") and address > 0 and group.startswith("pinmame."):
        aliases += [{"namespace": "vpe-legacy." + ("coil" if channel == "solenoid" else channel), "value": v}
                    for v in dict.fromkeys((str(address), f"{address:02}", f"{address:03}"))]
    prefix = {"solenoid": "output", "dip": "dip"}.get(channel, channel)
    return {"id": prefix + "." + slug(label), "label": label, "kind": kind,
            "binding": {"group": group, "device": address}, "aliases": aliases,
            "availability": availability, "provenance": prov(*refs, status=status)}


def located(identifier: str, role: str, names: list[str], evidence: dict) -> dict:
    table = evidence["tables"]["primary"]
    bounds = table["bounds"]
    placements = []
    for i, name in enumerate(names, 1):
        point = table["objects"][name]
        x = _round_point((point["x"] - bounds["left"]) / (bounds["right"] - bounds["left"]))
        y = _round_point((point["y"] - bounds["top"]) / (bounds["bottom"] - bounds["top"]))
        if not 0 <= x <= 1 or not 0 <= y <= 1:
            raise RuntimeError(f"Stars object is outside its retained bounds: {name}")
        placements.append({"id": f"{identifier}.{role}.{i}", "role": role, "space": "playfield", "x": x, "y": y,
                           "provenance": prov(TABLE, SCRIPT, MANUAL, status="observed")})
    return {"status": "observed", "placements": placements}


def build_definition(root: Path = ROOT) -> dict:
    evidence = load_json(root / EVIDENCE)
    sources = load_json(root / PROVENANCE)["sources"]
    inputs, outputs, mechanisms, relationships = [], [], [], []
    for n, label, kind, availability in ((-7, "Self test", "switch", "used"), (-6, "MPU diagnostic S33", "switch", "used"),
                                         (-5, "Unfitted sound diagnostic", "virtual", "unused")):
        item = device("switch", n, label, kind, (CORE, MANUAL), availability)
        item["spatial"] = na("unused" if n == -5 else "cabinet_or_service", CORE, MANUAL)
        item["physical"] = {"notes": "SNDBRD_NONE has no sound diagnostic handler or fitted electronic sound board." if n == -5 else
                            "Separate normally-open service pushbutton; not a matrix position."}
        if n != -5:
            item.update(normally_closed=False, pulse=False)
            item["physical"].update(switch_type="button", quantity=1, location="Coin door" if n == -7 else "MPU board")
        if n == -6:
            item["aliases"].append({"namespace": "manual.mpu", "value": "S33"})
            item["physical"]["notes"] += " Factory Figure 3 locates S33 on the MPU. The adjustment instructions use it to clear the selected bookkeeping/high-game value. The pinned by35 CPU-diagnostic branch drives NMI and explicitly uses lisy35_get_SW_S33 in its hardware-backed branch. This record represents that one physical service button, separate from coin-door self test; it does not promise an unconditional bookkeeping-clear API."
        inputs.append(item)
    for address in range(1, 49):
        used = address in SWITCHES
        item = device("switch", address, SWITCHES.get(address, f"Unfitted matrix {address}"), "switch", (MANUAL, CORE, TRACE),
                      "used" if used else "unused")
        item["aliases"].append({"namespace": "manual.self-test", "value": str(address)})
        if not used:
            item["spatial"] = na("unused", MANUAL, CORE)
            item["physical"] = {"notes": "The factory matrix marks N/U, or this is beyond its five fitted columns. The ROM diagnostic recognizes all 1-40, including unfitted positions; recognition does not establish a physical contact. The diagnostic did not name 41-48."}
        else:
            item.update(normally_closed=False, pulse=address in {1, 17, 20, 21, 22, 23, 24, 25, 36, 37, 38})
            item["physical"] = {"switch_type": "button" if address == 6 else "tilt" if address in (7, 16) else "leaf",
                                "notes": "Normally-open matrix contact in the factory schematic. Public 1 means closure; no second inversion."}
            if address in DROP_SWITCHES:
                item["physical"]["notes"] += " Drop contacts remain closed while down, and open when reset raises the targets."
            if address in CABINET:
                item["physical"]["location"] = "Cabinet / coin door"
                item["spatial"] = na("cabinet_or_service", MANUAL)
            else:
                names = {8: ["Drain"], 15: ["sw15a", "sw15b"], 25: [f"sw25{v}" for v in "abcdefg"],
                         36: ["RightSlingShot"], 37: ["LeftSlingShot"], 38: ["Bumper1"]}.get(address, [f"sw{address}"])
                if address != 16:
                    item["spatial"] = located(item["id"], "sensor", names, evidence)
                item["physical"]["location"] = "Playfield and cabinet" if address == 16 else "Playfield"
                if address in {8, 25, 36, 37, 38}:
                    item["physical"]["notes"] += " Placement is an observed projection onto the table's ball/assembly/rubber object, not a measurement of the hidden leaf contacts."
                if address in {36, 37}:
                    item["physical"]["notes"] += " Both older 32assassin retained tables swap LeftSlingshot/RightSlingshot switch writes. The factory map and isolated ROM responses settle left=37/coil15 and right=36/coil14; the physical-side object is used here. Bord1.0.2 corrects those bindings."
                if address == 15:
                    item["physical"]["notes"] += " The independently read factory upper-rollover callout fails the 0.07 drawing fit (0.1063 control / 0.0938 callout offset); the table coordinate is retained as observed, never moved to fit. The lower rollover agrees."
                if address == 8:
                    item["initial_active"] = True
                    item["physical"]["notes"] += " One ball begins on the outhole switch. Drain is a ball-collection proxy; BallRelease is in the shooter lane and is not the outhole's physical location."
                if address == 16:
                    item["physical"]["notes"] += " Factory quantity three: coin door, tilt board, and underside of playfield. The playfield contact has no retained measured location, so this aggregate deliberately has no not_applicable record."
            if address in (7, 15, 16, 25):
                item["physical"]["quantity"] = {7: 2, 15: 2, 16: 3, 25: 7}[address]
            if address == 6:
                item["roles"] = ["cabinet.start"]
            if address in (9, 10, 11):
                item["roles"] = [f"cabinet.coin-{12-address}"]
            if address not in CABINET and address != 16:
                strobe, row = divmod(address - 1, 8)
                item["wiring"] = {"board": "MPU A4", "control_connection": f"A4J2-{strobe+1}",
                                  "control_wire": ("W-R", "BRN-W", "W-BLU", "W-Y", "Y-R")[strobe],
                                  "return_connection": f"A4J2-{row+8}",
                                  "return_wire": ("BRN", "GREY", "W-O", "W-B", "W-G", "W-BRN", "BRN-Y", "O")[row]}
        inputs.append(item)
    for address in range(81, 89):
        used = address in (82, 84)
        side = "Right" if address == 82 else "Left"
        item = device("switch", address, side + " flipper button" if used else f"Unused generic flipper position {address}",
                      "switch", (CORE, SCRIPT, TRACE, MANUAL), "used" if used else "unused")
        item["spatial"] = na("cabinet_or_service" if used else "unused", CORE, MANUAL)
        item["physical"] = {"notes": "The ROM never reads this generic column. Lower button bits still control PinMAME's synthetic flipper pairs. Other positions have no fitted Stars contact or reachable ROM row."}
        if used:
            item.update(normally_closed=False, pulse=False)
            item["physical"].update(location="Cabinet", quantity=1, switch_type="button")
        inputs.append(item)
    for address, label in DIP_LABELS.items():
        item = device("dip", address, f"S{address} {label}", "dip_switch", (MANUAL, "bulletin.stars.8", CORE),
                      "unused" if address in {14, 23, 28, 29} else "used")
        item["spatial"] = na("dip_switch", MANUAL, CORE)
        item["physical"] = {"switch_type": "dip", "location": "MPU board",
                            "notes": "Configuration ordinal, independent of the playfield switch with this number. Four banks of eight. Manual corrections apply to S16 and S15; Bulletin 8 supersedes N/U at S27 and requires ON for multiplayer. No default state is invented."}
        inputs.append(item)
    for address, side in ((1, "Left"), (2, "Right")):
        item = device("switch", address, side + " flipper EOS", "switch", (MANUAL,), group="physical.input.direct")
        item.update(normally_closed=True, pulse=False)
        item["physical"] = {"switch_type": "leaf", "quantity": 1, "location": "Playfield flipper assembly",
                            "notes": "Normally-closed bypass across the power winding, opening near end of stroke. No public switch callback. Observed projection onto the flipper pivot; actual leaf position is not measured."}
        item["spatial"] = located(item["id"], "sensor", [side + "Flipper"], evidence)
        inputs.append(item)
    for address, (label, transistor, connector, wire) in COILS.items():
        unused = address in UNFITTED_COILS
        item = device("solenoid", address, label, "virtual" if unused else "relay" if address == 19 else "coil",
                      (MANUAL, CORE, TRACE, "bulletin.stars.9") if address < 16 else (MANUAL, CORE, TRACE), "unused" if unused else "used")
        item["wiring"] = {"board": "Solenoid driver A3", "driver_transistor": transistor, "drive_connection": connector}
        if wire:
            item["wiring"].update(drive_wire=wire, nominal_voltage_v=43, voltage_type="dc")
        if address in COIL_TEST:
            item["aliases"].append({"namespace": "manual.self-test", "value": str(COIL_TEST[address])})
        item["physical"] = {"notes": "Factory N/U output. The ROM service sweep still pulses momentary positions; PB4/PB7 also pulse briefly during power-up port initialization, without a documented load." if unused else
                            "Public binding comes from the ROM's own numbered coil test, independently exercised in play where applicable; the printed test number is not the public address."}
        if address < 16:
            item["physical"]["notes"] += " Public address is the U2 selector plus one. Native PDF25/26 collector paths identify every connector branch; Engineering Bulletin9 corroborates the CA3081 base/collector pins. The decoder, collector routes, numbered fitted loads and ROM test agree."
        if address in {5, 8, 11, 12}:
            item["physical"]["notes"] += " The printed test number is blank; public routing is derived from the decoder and collector path without filling that printed cell."
        if address in {1, 2, 6, 15}:
            item["physical"]["notes"] += " The additional connector branches are explicitly N/U. The drive wire describes the named fitted load branch; no wire colour or extra fitted load is assigned to the N/U branches."
        if address == 19:
            item["wiring"].update(power_connection="A3J3-5", power_wire="Y-W", nominal_voltage_v=43, voltage_type="dc")
            item["physical"]["notes"] += " Q15 collector drives on-board relay terminal8. Terminal7 receives +43V through A3J3-5; that connector is the relay supply, not an off-board collector output."
        if address == 20:
            item["physical"]["notes"] += " Q18 collector branches to A3J5-3, A3J2-15 and A3J3-9, all printed N/U."
        if unused or address in {1, 2, 3, 4, 6, 18, 19}:
            item["spatial"] = na("unused" if unused else "cabinet_or_service", MANUAL, CORE)
            if not unused:
                item["physical"].update(quantity=1, location="Cabinet" if address != 19 else "Backbox solenoid driver board")
        else:
            anchor = {7: "Drain", 9: "sw28", 10: "sw27", 13: "Bumper1", 14: "RightSlingShot", 15: "LeftSlingShot"}[address]
            item["spatial"] = located(item["id"], "effect", [anchor], evidence)
            item["physical"].update(quantity=1, location="Playfield",
                                    notes=item["physical"]["notes"] + " Observed projection onto its mechanism (bank middle target, bumper center, sling centroid, or Drain proxy); not a measured under-playfield coil center.")
        outputs.append(item)
    for address, side in ((45, "Right"), (46, "Right"), (47, "Left"), (48, "Left")):
        duplicate = address in (45, 47)
        item = device("solenoid", address, side + (" flipper duplicate state" if duplicate else " flipper"),
                      "control_signal" if duplicate else "coil", (CORE, SCRIPT, TRACE, MANUAL))
        item["physical"] = {"notes": "Synthetic pair rises together for the enabled button closure. This is not measured power/hold winding or EOS timing; only one physical flipper exists per side."}
        if duplicate:
            item["spatial"] = na("virtual", CORE)
        else:
            item["physical"].update(quantity=1, location="Playfield")
            item["spatial"] = located(item["id"], "effect", [side + "Flipper"], evidence)
        outputs.append(item)
    for row in load_json(root / LAMPS):
        named = [e for e in row["endpoints"] if e["label"] != "[blank]"]
        blank = [e for e in row["endpoints"] if e["label"] == "[blank]"]
        label = named[0]["label"].title() if named else f"Unidentified lamp driver {row['public']}"
        item = device("lamp", row["public"], label, "lamp", (MANUAL, CORE),
                      "used" if named else "unknown", status="validated" if named else "candidate")
        item["wiring"] = {"board": "Lamp driver A5", "driver_transistor": row["scr"],
                          "drive_connection": " / ".join(e["pin"] for e in row["endpoints"])}
        if named:
            item["wiring"].update(drive_wire=named[0]["wire"], power_connection="A2J1-7", power_wire="BLU")
        item["physical"] = {"notes": f"Schematic B-431-S-103 decoder U{row['decoder']} selector {row['selector']} through {row['resistor']} to {row['scr']}. Blank connector labels are retained in the excerpt; they are not proof of absent load. Local table insert/glow Light objects do not establish physical bulb centers or quantity."}
        if row["public"] in {27, 45, 60}:
            item["physical"]["notes"] += " Bord1.0.2's VR backglass callback labels45 as Match and60 as Game Over; the factory identifies Match at27 and Game Over at45. This table mapping defect does not override the circuit or identify blank parallel branches."
        if named and blank:
            named_regions = sorted({"Backbox insert panel" if e["pin"].startswith("A5J2-") else "Playfield" for e in named})
            item["physical"]["notes"] += " Named branch region: " + " / ".join(named_regions) + "."
            item["physical"]["notes"] += " Unnamed parallel branch " + " / ".join(e["pin"] for e in blank) + ": load identity, physical location and quantity are unknown. The named branch does not establish the aggregate's complete location or socket quantity; no cabinet-only spatial exemption is justified."
        if named and not blank and all(e["pin"].startswith("A5J2-") for e in row["endpoints"]):
            item["physical"]["location"] = "Backbox insert panel"
            item["spatial"] = na("cabinet_or_service", MANUAL)
        elif named and not blank and all(not e["pin"].startswith("A5J2-") for e in row["endpoints"]):
            item["physical"]["location"] = "Playfield"
        outputs.append(item)
    gi = device("gi", 1, "General illumination", "gi", (MANUAL, TABLE, SCRIPT), group="physical.output.gi", status="observed")
    gi["physical"] = {"notes": "Transformer-fed uncontrolled lighting, not a PinMAME callback. Nineteen older mesh-on GI candidates are retained; their neighboring broad helpers are excluded. Bord1.0.2 groups sixteen render lights with no bulb meshes, not a physical wiring or quantity cross-check. Backbox/cabinet and hidden sockets and complete string quantity remain unverified; the VPX grouping does not establish wiring."}
    gi["spatial"] = located(gi["id"], "emitter", [f"GI_{i}" for i in range(2, 39, 2)], evidence)
    outputs.append(gi)
    ins = {i["binding"]["device"]: i["id"] for i in inputs if i["binding"]["group"] == "pinmame.input.switch"}
    outs = {i["binding"]["device"]: i["id"] for i in outputs if i["binding"]["group"] == "pinmame.output.solenoid"}
    for name, coil, switches in (("Left drop bank", 9, [32, 28, 31]), ("Upper right drop bank", 10, [30, 27, 29])):
        mechanisms.append({"id": "mechanism." + slug(name), "label": name, "kind": "drop_target_bank",
                           "actuators": [outs[coil]], "sensors": [ins[n] for n in switches], "assembly_part_number": "D-393-3",
                           "behavior": "Three independently latched targets. A hit closes its contact until this bank's common reset coil raises it and opens its contacts. Factory and retained script give the target order. The ROM resets both banks on startup; both reset outputs fire when either bank is completed in the retained gameplay sequence. The factory rules and S24 determine later triple-bonus completion conditions. No numeric mechanical timing or modeled jam sensor is established.",
                           "provenance": prov(MANUAL, SCRIPT, TRACE)})
        for n in switches:
            relationships.append({"id": f"relationship.reset-{coil}-opens-{n}", "kind": "inverted", "source": outs[coil], "destination": ins[n], "provenance": prov(MANUAL, SCRIPT, TRACE)})
    for label, kind, actuators, sensors, behavior in [
        ("Outhole and shooter feed", "kicker", [outs[7]], [ins[8]], "One ball drains onto the outhole contact, bonus is counted and the kicker feeds the manual shooter lane. The host releases 8 when the ball leaves. BallRelease is a shooter proxy; this is not a multiball trough."),
        ("Thumper bumper", "kicker", [outs[13]], [ins[38]], "Ball closes switch 38; ROM fires coil 13. Physical ring/skirt mechanism returns mechanically."),
        ("Left slingshot", "kicker", [outs[15]], [ins[37]], "Rubber hit closes 37; ROM fires coil 15. Local tables' opposite switch write is a defect."),
        ("Right slingshot", "kicker", [outs[14]], [ins[36]], "Rubber hit closes 36; ROM fires coil 14. Local tables' opposite switch write is a defect."),
        ("Left spinner", "rotary", [], [ins[1]], "Passive spinning target, one closure per contact actuation. No motor or home sensor."),
        ("Right spinner", "rotary", [], [ins[17]], "Passive spinning target, one closure per contact actuation. No motor or home sensor."),
        ("Manual plunger", "other", [], [], "Player-powered shooter serves one ball. No launch coil or shooter-lane switch is listed; strength is table-owned."),
        ("Chime unit", "other", [outs[n] for n in range(1, 5)], [], "Four electromechanical chime coils for 10, 100, 1000 and 10000. The fourth is EXTRA CHIME on the schematic. No electronic sound board or feedback switch."),
        ("Left flipper", "other", [outs[48]], [ins[84], "switch.left-flipper-eos"], "Cabinet button and enable relay switch a dual-winding flipper. Normally-closed EOS bypass opens near full stroke. Synthetic 47/48 do not simulate real EOS or winding timing."),
        ("Right flipper", "other", [outs[46]], [ins[82], "switch.right-flipper-eos"], "Cabinet button and enable relay switch a dual-winding flipper. Normally-closed EOS bypass opens near full stroke. Synthetic 45/46 do not simulate real EOS or winding timing."),
    ]:
        mechanisms.append({"id": "mechanism." + slug(label), "label": label, "kind": kind,
                           "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": prov(MANUAL, SCRIPT, TRACE)})
    for n in (45, 46, 47, 48):
        relationships.append({"id": f"relationship.enable-{n}", "kind": "relay_gated", "source": outs[19], "destination": outs[n], "provenance": prov(CORE, MANUAL, TRACE)})
    displays = [{"id": f"display.player-{i+1}", "label": f"Player {i+1}", "kind": "segment", "controller_index": i,
                 "segment_start": 2+8*i, "width": 6, "height": 1, "physical_location": "cabinet_or_service",
                 "spatial": na("cabinet_or_service", MANUAL, CORE), "provenance": prov(MANUAL, CORE)} for i in range(4)]
    for index, label, start in ((4, "Credits", 35), (5, "Ball in play and match", 38)):
        displays.append({"id": "display." + slug(label), "label": label, "kind": "segment", "controller_index": index,
                         "segment_start": start, "width": 2, "height": 1, "physical_location": "cabinet_or_service",
                         "spatial": na("cabinet_or_service", MANUAL, CORE), "provenance": prov(MANUAL, CORE)})
    drivers = load_json(root / PROVENANCE)["drivers"]
    result = {"format": "pinmame-machine-definition", "schema_version": 2,
              "machine": {"id": MACHINE_ID, "name": "Stars", "manufacturer": "Stern", "year": 1978, "kind": "physical_pinball",
                          "model_number": "103", "ipdb_id": 2366, "opdb_id": "GrXEW-MDEwr",
                          "playfield": {"width": 952, "height": 1974, "units": "vpx", "provenance": prov(TABLE, status="observed")}},
              "controller": {"platform": "pinmame.stern-mpu100", "hardware_generation": "0x800000", "inversion_applied_by_emulator": True},
              "drivers": drivers, "inputs": inputs, "outputs": outputs, "displays": displays, "mechanisms": mechanisms,
              "relationships": relationships, "sources": sources, "conflicts": [],
              "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "partial"},
              "coverage": {"status": "partial", "missing": ["output_semantics", "variant_differences", "provenance", "spatial_placement"],
                           "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate",
                                          "physical_wiring": "observed", "mechanisms": "validated", "variant_coverage": "candidate",
                                          "recreation_knowledge": "validated", "emulator_normalization": "validated",
                                          "diagnostic_enumeration": "validated", "runtime_observation": "validated",
                                          "spatial_placement": "observed"}}}
    if unresolved_conflicts(result):
        raise RuntimeError("Stars unexpected unresolved conflict")
    return result


def lamp_inventory(rows: list[dict]) -> dict:
    blank = lambda row: [e for e in row["endpoints"] if e["label"] == "[blank]"]
    partial = [r for r in rows if 0 < len(blank(r)) < len(r["endpoints"])]
    return {"output_count": len(rows), "endpoint_count": sum(len(r["endpoints"]) for r in rows),
            "unnamed_outputs": [r["public"] for r in rows if len(blank(r)) == len(r["endpoints"])],
            "blank_endpoint_count": sum(len(blank(r)) for r in rows),
            "partially_named_outputs": {str(r["public"]): blank(r) for r in partial},
            "blank_split_endpoint_count": sum(len(blank(r)) for r in partial)}


def lamp_inventory_summary(inventory: dict) -> str:
    return (f"{len(inventory['unnamed_outputs'])} lamp-driver outputs have no named load; "
            f"{inventory['blank_endpoint_count']} connector endpoints have blank load labels in total, "
            f"including {inventory['blank_split_endpoint_count']} additional blank branches on "
            f"{len(inventory['partially_named_outputs'])} partially named split outputs. "
            "Runtime activity does not establish fitment, location or quantity of those branches.")


def build_report(definition: dict, root: Path = ROOT) -> dict:
    evidence = load_json(root / EVIDENCE)
    devices = definition["inputs"] + definition["outputs"]
    callouts = load_json(root / CALLOUTS)
    drawing = evaluate_callouts(callouts, placements_of(definition), callouts["limit"])
    lamps = lamp_inventory(load_json(root / LAMPS))
    return {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID, "promotion": "blocked",
            "coordinate_convention": "x=0 left, x=1 right; y=0 rear, y=1 front",
            "transformation": "x=(X-left)/(right-left); y=(Y-top)/(bottom-top); round once to six decimals",
            "evidence": evidence, "runtime": RUNTIME.as_posix(),
            "lamp_inventory": lamps,
            "coil_decoder_routing": {"seed": COIL_DECODER.as_posix(), "sha256": sha256(root / COIL_DECODER),
                                        "readings": load_json(root / COIL_DECODER)},
            "coil_collector_retrace": evidence["collector_retrace"],
            "projection_classes": {"sling": "wall drag-point centroid onto rubber assembly", "rebound": "each rubber wall centroid onto its contact assembly",
                                   "bumper": "bumper center onto hidden switch/coil", "bank": "middle target onto common reset mechanism",
                                   "flipper": "pivot onto coil/EOS assembly", "outhole": "Drain collection proxy, not shooter BallRelease"},
            "unplaced_devices": [d["id"] for d in devices if "spatial" not in d],
            "unknown_fitment": [d["id"] for d in devices if d.get("availability") == "unknown"],
            "placement_count": sum(len(d.get("spatial", {}).get("placements", [])) for d in devices),
            "lamp_candidates": {n: obj for n, obj in evidence["tables"]["primary"]["objects"].items() if obj["type"] == "Light" and n.startswith("L")},
            "bord_lamp_candidates": {address: {name: evidence["tables"]["bord-1.0.2"]["objects"][name] for name in names}
                                     for address, names in evidence["tables"]["bord-1.0.2"]["lamp_bindings"].items()},
            "manual_callouts": {"seed": CALLOUTS.as_posix(), "sha256": sha256(root / CALLOUTS), **drawing,
                                "status_policy": "Agreement corroborates identity, count, side and order; no table point is moved. Mechanism/ball/rubber projections and the unreconciled multi-table geometry remain observed. Upper bonus rollover fails. All per-page controls, full reads, affine fits and leave-one-out offsets are retained."},
            "blockers": [lamp_inventory_summary(lamps),
                         "Controlled playfield lamp socket coordinates/quantities need physical bulb or factory-drawing evidence; the older 42 and bord44 Light bindings do not establish sockets. Bord has no mesh-on Light bulbs.",
                         "Underside playfield slam contact, complete GI socket inventory, and hidden mechanism contact/coil positions remain unmeasured.",
                         "Factory drawing controls now corroborate most switch anchors, but the upper bonus rollover fails; projected coils and multi-table geometry remain observed. The two older tables share ancestry.",
                         "Community rev.103 firmware differences and the related seven-digit readme's exact pinned-ROM lineage remain unverified; no MOD ROM archive is present."]}


def render_report(report: dict) -> str:
    return ("# Stars (Stern 1978) spatial blockers\n\nCoverage remains **partial**. "
            "Two older local VPX revisions and user-supplied bord1.0.2 were retained.\n\n"
            + report["coordinate_convention"] + ". " + report["transformation"] + ".\n\n"
            + "\n".join("- " + b for b in report["blockers"]) + "\n\n"
            + "The JSON report lists every candidate, exact source/extraction hashes, raw table coordinates, "
              "projection classes, unplaced records and unknown fitment. Nineteen mesh-on GI candidates "
              "are observed; their nineteen broad-light partners are excluded. Proven cabinet/backbox-only devices "
              "carry controlled not_applicable records; partially named split lamp outputs remain unplaced, including Match27's blank A5J1-4 branch. Controlled-lamp glow centers are retained only "
              "as candidates in this report, never as physical socket placements. Independent factory "
              "drawing reads and reproducible fits are included; no coordinate is shifted to pass them.\n")


def verify_portable(root: Path = ROOT) -> None:
    metadata = load_json(root / PROVENANCE)
    for path, digest in metadata["portable_sha256"].items():
        if not (root / path).is_file() or sha256(root / path) != digest:
            raise RuntimeError(f"Stars pinned portable evidence missing or changed: {path}")
    lamps = load_json(root / LAMPS)
    if {r["public"] for r in lamps} != {16*d+s+1 for d in range(4) for s in range(15)}:
        raise RuntimeError("Stars lamp decoder inventory is incomplete")
    pins = [e["pin"] for r in lamps for e in r["endpoints"]]
    if len(pins) != 68 or len(set(pins)) != 68:
        raise RuntimeError("Stars lamp connector branches collide")


def products(root: Path = ROOT) -> dict[Path, bytes]:
    verify_portable(root)
    definition = build_definition(root)
    errors = validate_machine(definition, root)
    if errors:
        raise RuntimeError("Invalid Stars: " + "; ".join(errors))
    report = build_report(definition, root)
    return {DEFINITION: canonical_bytes(definition), SEED: canonical_bytes(definition),
            KNOWLEDGE: (root / KNOWLEDGE_SEED).read_text(encoding="utf-8").replace("{{LAMP_INVENTORY}}", lamp_inventory_summary(report["lamp_inventory"])).encode("utf-8"),
            REPORT: canonical_bytes(report), REPORT_MD: render_report(report).encode("utf-8")}


def check(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY).exists():
        raise RuntimeError("Stars still has authoring-critical gaps; refusing an author-ready artifact")
    for path, payload in products(root).items():
        if not (root / path).is_file() or (root / path).read_bytes() != payload:
            raise RuntimeError(f"Stars deterministic artifact missing or drifted: {path}")


def generate(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY).exists():
        raise RuntimeError("Refusing to overwrite an author-ready Stars artifact")
    for path, payload in products(root).items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_bytes(payload)


def verify_evidence(root: Path = ROOT) -> None:
    check(root)
    names = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
    if any(not os.environ.get(n) for n in names):
        raise RuntimeError("All three Stars external evidence roots must be configured")
    vpx, manuals, review = (Path(os.environ[n]) for n in names)
    evidence = load_json(root / EVIDENCE)
    library = review.parent / "builds/pinmame-46e1a01a/Release/pinmame64.dll"
    if sha256(library) != "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5":
        raise RuntimeError("Stars retained pinned native binary changed")
    for tag, table in evidence["tables"].items():
        original = vpx / table["table_path"]
        extraction = original.parent / f"{tag}-extracted"
        manifest = build_manifest(extraction, "stars")
        if (check_manifest(extraction, "stars"), len(manifest["files"]), sum(f["size"] for f in manifest["files"])) != (table["manifest_sha256"], table["files"], table["bytes"]):
            raise RuntimeError(f"Stars {tag} extraction manifest changed")
        if sha256(original) != table["table_sha256"] or sha256(extraction / "script.vbs") != table["script_sha256"]:
            raise RuntimeError(f"Stars {tag} retained table/script changed")
        if tag == "bord-1.0.2":
            bindings = {}
            for match in re.finditer(r"(?im)^\s*NFadeLm\s+(\d+)\s*,\s*(\w+)", (extraction / "script.vbs").read_text(encoding="utf-8")):
                bindings.setdefault(match[1], []).append(match[2])
            gi = next(c["items"] for c in load_json(extraction / "collections.json") if c["name"].casefold() == "gi")
            lights = [data["Light"] for path in (extraction / "gameitems").glob("Light.*.json") if "Light" in (data := load_json(path))]
            meshes = sorted(light["name"] for light in lights if light.get("show_bulb_mesh"))
            if (bindings, gi, len(lights), meshes) != (table["lamp_bindings"], table["gi_collection"], table["light_count"], table["visible_bulb_mesh_lights"]):
                raise RuntimeError("Stars bord render bindings or bulb-mesh inventory changed")
        for name, point in table["objects"].items():
            path = extraction / point["file"]
            raw = load_json(path)[point["type"]]
            if sha256(path) != point["sha256"] or _item_point(point["type"], raw) != (point["x"], point["y"], point["method"]):
                raise RuntimeError(f"Stars {tag} geometry changed: {name}")
            for flag in ("show_bulb_mesh", "is_bulb_light", "falloff_radius", "has_static_bulb_mesh", "is_backglass"):
                if flag in point and raw.get(flag) != point[flag]:
                    raise RuntimeError(f"Stars {tag} lamp evidence changed: {name} {flag}")
    for manual in evidence["manuals"]:
        if sha256(manuals / manual["path"]) != manual["sha256"]:
            raise RuntimeError(f"Stars manual changed: {manual['path']}")
    verify_retained(load_json(root / CALLOUTS), root, manuals, review)
    for source in evidence["retained_review_sources"]:
        if sha256(review / source["path"]) != source["sha256"]:
            raise RuntimeError(f"Stars retained source changed: {source['path']}")
    retrace = load_json(review / evidence["collector_retrace"]["path"])
    for source in retrace["sources"].values():
        native = manuals / "by-machine" / MACHINE_ID / "ipdb-2366/native-renders" / Path(source["path"]).name
        if sha256(native) != source["sha256"]:
            raise RuntimeError(f"Stars collector retrace native render changed: {native}")
    for source in evidence["source_files"]:
        repository = review.parent / "source-checkouts" / source["repository"]
        if subprocess.check_output(["git", "-C", str(repository), "rev-parse", "HEAD"], text=True).strip() != source["revision"]:
            raise RuntimeError(f"Stars source checkout revision changed: {repository}")
        if subprocess.check_output(["git", "-C", str(repository), "status", "--porcelain"], text=True).strip():
            raise RuntimeError(f"Stars source checkout dirty: {repository}")
        if sha256(repository / source["path"]) != source["sha256"]:
            raise RuntimeError(f"Stars pinned source bytes changed: {source['path']}")
    if canonical_bytes(runtime_build(review / MACHINE_ID / "harness")) != (root / RUNTIME).read_bytes():
        raise RuntimeError("Stars retained traces disagree with compact evidence")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    mode.add_argument("--verify-evidence", action="store_true")
    args = parser.parse_args()
    (check if args.check else verify_evidence if args.verify_evidence else generate)()
    print("Stars deterministic curation verified" if args.check or args.verify_evidence else "Stars partial definition regenerated")


if __name__ == "__main__":
    main()
