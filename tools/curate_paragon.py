#!/usr/bin/env python3
"""Deterministic curator for Bally Paragon (1979).

Regenerates the Paragon definition, its knowledge note and its spatial audit from the tables below
and the pinned seeds, so the artifacts reproduce byte for byte and drift is detected. ``--check``
refuses drift and never writes; ``--regenerate`` writes. Generation never reads the external
evidence roots; ``tests/test_paragon.py`` rechecks the seeds against them when they are present.

The tables are the curated result of the evidence in the priority the runbook sets out: the
retained ROM's own self tests and gameplay for the public-address translation and runtime
semantics, the IPDB manual and schematics for construction, wiring and the printed identification
numbers, the known-working table for runtime bindings and coordinates, and pinned PinMAME for
emulator topology. Two facts here look like tidy-ups and are not:

- the printed solenoid numbers are self-test numbers, not public addresses (the ROM pairs them);
- public lamp 43 is the playfield SAME PLAYER S.A. insert, not the backglass Shoot Again (public 11).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256  # noqa: E402
import drawing_callouts  # noqa: E402

MACHINE_ID = "bally.paragon.1979"
PARTIAL_PATH = ROOT / "machines" / "partial" / "bally" / "paragon-1979.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "paragon-1979.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "paragon-1979.md"
REPORT_JSON_PATH = ROOT / "reports" / "spatial" / "bally" / "paragon-1979.json"
REPORT_MD_PATH = ROOT / "reports" / "spatial" / "bally" / "paragon-1979.md"
SPATIAL_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "paragon-1979-spatial.json"
EXCERPT_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "paragon-1979-excerpts.json"
CALLOUT_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "paragon-1979-callouts.json"
KNOWLEDGE_SOURCE_PATH = ROOT / "tools" / "seeds" / "bally" / "paragon-1979-knowledge.md"
RUNTIME_SUMMARY = "evidence/runtime/by35/paragon-1979-harness.json"
EXCERPT_DIR = "evidence/excerpts/bally.paragon.1979"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

S_CATALOG = "pinmame.catalog.97aa922bf8e4"
S_CORE = "pinmame.core.97aa922bf8e4"
S_PROFILE = "controller-profile.pinmame-by35"
S_IPDB = "ipdb.1755"
S_MANUAL = "manual.bally.paragon.1979"
S_SCHEMATIC = "schematic.bally.paragon.1979"
S_KMIEC = "ipdb.1755.kmiec-treasure-chamber"
S_LIBRARY = "vpinmame-library.bally-vbs"
S_SCRIPT = "vpx-script.paragon.2-37"
S_TABLE = "vpx-table.paragon.2-37"
S_RUNTIME = "runtime.paragon.harness"
S_CALLOUTS = "drawing-callouts.paragon.2026-10-16"

SEED = json.loads(SPATIAL_SEED_PATH.read_text(encoding="utf-8"))
OBJECTS = SEED["objects"]
BOUNDS = SEED["bounds"]


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def prov(status: str, *refs: str) -> dict:
	return {"status": status, "source_refs": list(refs)}


def aliases(*pairs: tuple[str, object]) -> list[dict]:
	return [{"namespace": namespace, "value": str(value)} for namespace, value in pairs]


def at(name: str) -> tuple[float, float]:
	item = OBJECTS[name]
	return item["x"], item["y"]


def placement(placement_id: str, role: str, point: tuple[float, float], status: str, *refs: str) -> dict:
	return {"id": placement_id, "role": role, "space": "playfield", "x": point[0], "y": point[1], "provenance": prov(status, *refs)}


def located(status: str, *placements: dict) -> dict:
	return {"status": status, "placements": list(placements)}


def not_applicable(reason: str, *refs: str) -> dict:
	return {"status": "not_applicable", "reason": reason, "provenance": prov("validated", *refs)}


LEAF_NOTE = (
	"The manual's assembly adjustments state that all switch assemblies are leaf springs \"adjusted for a 1/16\\\" gap in the open position\", "
	"and the switch test shows the ROM reading this address active at public 1; the CPU reads the matrix uninverted, so the contact rests open."
)

# ----------------------------------------------------------------------------------------------
# Switches
# ----------------------------------------------------------------------------------------------

# number -> (label, switch_type, pulse, roles, location, printed description, table objects)
SWITCHES = {
	1: ("In-line drop target D (top)", "leaf", False, [], "Valley of Demons in-line drop targets on the left wall, rearmost", 'Drop target (in line) "D" (top)', ["sw1"]),
	2: ("In-line drop target C", "leaf", False, [], "Valley of Demons in-line drop targets, third from the front", 'Drop target (in line) "C"', ["sw2"]),
	3: ("In-line drop target B", "leaf", False, [], "Valley of Demons in-line drop targets, second from the front", 'Drop target (in line) "B"', ["sw3"]),
	4: ("In-line drop target A (bottom)", "leaf", False, [], "Valley of Demons in-line drop targets, frontmost", 'Drop target (in line) "A" (bottom)', ["sw4"]),
	6: ("Credit button", "button", False, ["cabinet.credit-button"], "Coin door", "Credit button", []),
	7: ("Tilt (panel, plumb bob and ball tilts)", "tilt", False, ["cabinet.tilt"], "Cabinet: panel tilt under the playfield, plumb bob and ball tilt on the left cabinet side near the door", "Tilt (3)", []),
	8: ("Outhole", "leaf", False, ["internal.trough"], "Outhole below the flippers", "Outhole", ["Drain"]),
	9: ("Coin III (right)", "other", True, ["cabinet.coin-door"], "Coin door, right chute (chute #3)", "Coin III (right)", []),
	10: ("Coin I (left)", "other", True, ["cabinet.coin-door"], "Coin door, left chute (chute #1, hinge side)", "Coin I (left)", []),
	11: ("Coin II (middle)", "other", True, ["cabinet.coin-door"], "Coin door, middle chute (chute #2)", "Coin II (middle)", []),
	16: ("Slam (door and cabinet)", "tilt", False, ["cabinet.slam-tilt"], "Front door slam switch and a cabinet slam switch", "Slam (2)", []),
	17: ("Waterfall drop target C (bottom)", "leaf", False, [], "Right three-bank waterfall drop targets, front", 'Drop target "C" (bottom)', ["sw17"]),
	18: ("Waterfall drop target B", "leaf", False, [], "Right three-bank waterfall drop targets, middle", 'Drop target "B"', ["sw18"]),
	19: ("Waterfall drop target A (top)", "leaf", False, [], "Right three-bank waterfall drop targets, rear", 'Drop target "A" (top)', ["sw19"]),
	22: ("Right outlane", "leaf", True, [], "Right outlane", "Right outlane", ["sw22"]),
	23: ("Right flip feeder lane", "leaf", True, [], "Right return lane feeding the lower right flipper", "Right flip feeder lane", ["sw23"]),
	24: ("Paragon saucer", "leaf", False, [], "Top right Paragon saucer", "Paragon saucer", ["sw24"]),
	26: ("Top center rollover button", "leaf", True, [], "Star rollover under the top arch, centre", "Top center rollover button", ["sw26"]),
	27: ("500 point rebound", "leaf", True, [], "Two rebound rubbers: inside the upper-left curved guide and on the left lane guide below the in-line targets", "500 point rebound (2)", ["sw27a#upper", "sw27a#lower"]),
	28: ("Waterfall rollover button", "leaf", True, [], "Star rollover in the right-hand waterfall lane", "Waterfall rollover button", ["sw28"]),
	29: ("Center target", "leaf", True, [], "Advance-bonus stand-up target below the centre thumper bumper", "Center target", ["sw29"]),
	30: ("Top center target", "leaf", True, [], "Advance-bonus stand-up target in the top triangle between the saucers", "Top center target", ["sw30"]),
	31: ("Treasure chamber saucer", "leaf", False, [], "Upper-left Treasure Chamber saucer", "Treasure chamber saucer", ["SW31"]),
	32: ("Golden cliffs saucer", "leaf", False, [], "Top left-centre Golden Cliffs saucer", "Golden cliffs saucer", ["sw32"]),
	33: ("Spinner", "leaf", True, [], "Spinner on the left, beside the four spinner-value inserts", "Spinner", ["sw33"]),
	34: ("Top right, golden cliffs rollover button and drop target rebound", "leaf", True, [], "Three parallel contacts: the star rollover above the Golden Cliffs saucer, the star rollover at the top right and the rebound rubber beside the waterfall drop targets", "Top right, golden cliffs rollover button and drop target rebound.", ["sw34", "sw34a", "sw34b#rebound"]),
	35: ("Right slingshot", "leaf", True, [], "Right slingshot", "Right slingshot", ["RightSlingShot"]),
	36: ("Left slingshot", "leaf", True, [], "Left slingshot", "Left slingshot", ["LeftSlingShot"]),
	37: ("Bottom thumper bumper", "leaf", True, [], "Lower-left thumper bumper skirt", "Bottom thumper bumper", ["Bumper1"]),
	38: ("Center thumper bumper", "leaf", True, [], "Centre thumper bumper skirt", "Center thumper bumper", ["Bumper2"]),
	39: ("Right thumper bumper", "leaf", True, [], "Upper-right thumper bumper skirt", "Right thumper bumper", ["Bumper3"]),
	40: ("Left thumper bumper", "leaf", True, [], "Upper-left thumper bumper skirt", "Left thumper bumper", ["Bumper4"]),
}
QUANTITY = {7: 3, 16: 2, 27: 2, 34: 3}
CABINET = {6, 7, 9, 10, 11, 16}
BLANK = (5, 12, 13, 14, 15, 20, 21, 25)
PLACEMENT_SUFFIX = {
	27: ("upper-rebound", "lower-rebound"),
	34: ("golden-cliffs-rollover", "top-right-rollover", "drop-target-rebound"),
}

SWITCH_NOTES = {
	1: "The script raises 1-4 together from output 2. In play, knocking down this target last (the fourth of the bank) lit the 3X bonus lamp (public 22), the award the manual gives target #4.",
	2: "In play, knocking down this target third lit the 2X bonus lamp (public 6), the award the manual gives target #3. The VPinMAME Bally library's generic constant swBallRollTilt also names public 2; it is a Bally-wide default, the Paragon table does not use it, and the game's own manual and ROM make public 2 this drop target (the ball tilt is one of the three contacts on public 7).",
	6: "Pressing it with credits starts a game: the ROM fires the in-line and waterfall drop-target resets (2 and 17), kicks the outhole (7) and raises the flipper-enable relay (19).",
	7: "The manual's installation page lists three normally open tilt switches on this address: the panel tilt on the bottom of the playfield panel, the plumb bob on the left side of the cabinet near the front door, and the ball tilt above the plumb bob. Closing it in play makes the ROM drop the flipper-enable relay (19) and light the TILT lamp (61).",
	8: "The ball drains into the outhole and closes this switch; the ROM scores the bonus and fires the outhole kicker (7). Figure V prints 08 beside the outhole and 01 (the kicker) at it.",
	9: "Figure V's legend puts 09 on the door.",
	10: "Figure V's legend puts 10 on the door. The VPinMAME Bally library calls public 10 swCoin2 and public 11 swCoin1; the game's own manual calls 10 Coin I (left), and its coin options call the left chute #1 (hinge side).",
	11: "Figure V's legend puts 11 on the door.",
	16: "The manual says there is one factory slam switch on the front door and that operators may add more; Figure V's legend puts 16 on both the cabinet and the door, and the switch table prints (2).",
	17: "The script raises 17-19 together from output 17, which the ROM fires once all three are down.",
	22: "There is no left outlane switch: the manual lists none, and the left lane is the Beast's Lair ramp that returns the ball to the flippers.",
	24: "The ROM fires the Paragon saucer kicker (10) while the ball rests on this switch, after scoring and spotting the lit PARAGON letter.",
	27: "The switch table prints (2): two rebound contacts on one address. The retained table models both rubbers as the two pieces of one collidable primitive, sw27a; its separate sw27b_Hit handler has no object.",
	29: "The manual's bonus feature calls the top and centre targets the \"Advance Bonus\" targets.",
	30: "The manual's bonus feature calls the top and centre targets the \"Advance Bonus\" targets.",
	31: "The ROM fires the Treasure Chamber kicker (8) while the ball rests on this switch. Greg Kmiec's IPDB note describes the saucer's lane: a clear plastic guide on the left directs the ball into a metal deadening piece on the right so it drops into the saucer instead of jumping it, and the saucer kicks up towards the top of the playfield.",
	32: "The ROM fires the Golden Cliffs kicker (9) while the ball rests on this switch, scoring and advancing the lit golden cliffs value.",
	33: "The spinner's closure lit spinner lamp 14 in play.",
	34: "The switch table prints this as one address with three named contacts; the retained table binds the two star rollovers (sw34, sw34a) and the rebound rubber (sw34b) to it.",
	35: "The ROM fires the right slingshot coil (15) for a closure.",
	36: "The ROM fires the left slingshot coil (14) for a closure.",
	37: "The ROM fires the bottom thumper bumper coil (1) for a closure.",
	38: "The ROM fires the centre thumper bumper coil (13) for a closure.",
	39: "The ROM fires the right thumper bumper coil (12) for a closure.",
	40: "The ROM fires the left thumper bumper coil (11) for a closure.",
}


def matrix_wiring(number: int) -> dict:
	column, row = (number - 1) // 8, (number - 1) % 8
	if number in CABINET:
		return {"board": "MPU module A4", "control_connection": f"A4J3-{2 + column}", "return_connection": f"A4J3-{9 + row}"}
	return {"board": "MPU module A4", "control_connection": f"A4J2-{1 + column}", "return_connection": f"A4J2-{8 + row}"}


def switch_sources(number: int) -> list[str]:
	refs = [S_MANUAL, S_SCHEMATIC, S_RUNTIME]
	if SWITCHES[number][6]:
		refs.extend([S_SCRIPT, S_TABLE])
	if number in (2, 6, 7, 9, 10, 11, 16):
		refs.append(S_LIBRARY)
	return refs


def switch_placements(number: int) -> dict:
	label, _, _, roles, _, _, objects = SWITCHES[number]
	if not objects or "internal.trough" not in roles and roles:
		return not_applicable("cabinet_or_service", S_MANUAL, S_SCHEMATIC)
	base = f"switch.{slug(label)}"
	suffixes = PLACEMENT_SUFFIX.get(number, ("sensor",))
	points = [
		placement(f"{base}.{suffix}" if len(objects) > 1 else f"{base}.sensor", "sensor", at(name), "observed", S_TABLE, S_SCRIPT, S_MANUAL)
		for suffix, name in zip(suffixes, objects)
	]
	return located("observed", *points)


def matrix_switch(number: int) -> dict:
	label, switch_type, pulse, roles, location, printed, objects = SWITCHES[number]
	physical: dict = {"switch_type": switch_type, "location": location}
	notes = [f'Printed switch description "{printed}", self-test display number {number:02d}; the ROM\'s switch test shows {number:02d} when public {number} closes.']
	if number in SWITCH_NOTES:
		notes.append(SWITCH_NOTES[number])
	if number in QUANTITY:
		notes.append(f"{QUANTITY[number]} physical contacts are wired in parallel on this one address, so the controller cannot tell which closed.")
		physical["quantity"] = QUANTITY[number]
	notes.append(LEAF_NOTE)
	physical["notes"] = " ".join(notes)
	item = {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases(("pinmame.switch", number), ("manual.address", number)),
		"normally_closed": False,
		"pulse": pulse,
		"availability": "used",
		"physical": physical,
		"wiring": matrix_wiring(number),
		"provenance": prov("validated", *switch_sources(number)),
		"spatial": switch_placements(number),
	}
	if roles:
		item["roles"] = roles
	return item


def unused_switch(number: int) -> dict:
	if number in BLANK:
		note = (
			f"The manual's switch table prints {number:02d} with no description, the switch location drawing has no {number:02d}, and the retained table binds nothing to it. "
			f"The ROM's switch test still shows {number:02d} when the host closes it, which proves only that the matrix position is readable, not that a switch is fitted."
		)
		refs = (S_MANUAL, S_SCRIPT, S_RUNTIME)
	else:
		note = (
			"Paragon wires five switch columns: the manual's switch table stops at 40, the MPU's playfield and cabinet strobe connectors carry ST0-ST4 only, "
			"and the retained table binds nothing above 40. PinMAME's sixth column (41-48) has nothing behind it on this game."
		)
		refs = (S_MANUAL, S_SCHEMATIC, S_CORE)
	return {
		"id": f"switch.unused-{number}",
		"label": f"Unused switch matrix position {number}",
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases(("pinmame.switch", number)),
		"availability": "unused",
		"physical": {"notes": note},
		"provenance": prov("validated", *refs),
		"spatial": not_applicable("unused", *refs),
	}


def service_switch(number: int, label: str, location: str, notes: str, role: str) -> dict:
	return {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases(("pinmame.switch", number)),
		"normally_closed": False,
		"pulse": False,
		"availability": "used",
		"physical": {"switch_type": "button", "location": location, "notes": notes},
		"roles": [role],
		"provenance": prov("validated", S_LIBRARY, S_CORE, S_MANUAL),
		"spatial": not_applicable("cabinet_or_service", S_LIBRARY, S_CORE),
	}


def flipper_button(number: int, label: str, availability: str, side: str) -> dict:
	item = {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases(("pinmame.switch", number)),
		"availability": availability,
		"physical": {"switch_type": "button", "location": "Cabinet side"},
	}
	if availability == "used":
		output = 46 if side == "right" else 48
		item["normally_closed"] = False
		item["pulse"] = False
		item["roles"] = [f"flipper.button.{side}"]
		item["physical"]["notes"] = (
			f"Public {number} is the {side} cabinet flipper button. Paragon's buttons are not in the switch matrix: the plug-connector sheet wires them to the solenoid driver ({'A3J2-1 R. FLIP SW.' if side == 'right' else 'A3J2-2 L. FLIP SW.'}) "
			f"so each switches its side's two flipper coils through the K1 flipper-enable relay. The driver declares FLIP_SW(FLIP_L) without FLIP_SOL, so PinMAME reads this position of its own flipper column "
			f"and raises the {side} flipper output {output} while the button is held and the relay (19) is up; the ROM never reads it. In play, holding {number} raised {output}, and after a tilt it raised nothing."
		)
		item["provenance"] = prov("validated", S_CORE, S_LIBRARY, S_SCHEMATIC, S_RUNTIME)
		item["spatial"] = not_applicable("cabinet_or_service", S_CORE, S_SCHEMATIC)
	else:
		item["physical"]["notes"] = (
			f"Public {number} is PinMAME's generic upper-{side} flipper button position. Paragon has no separate upper button: its extra flippers share the lower buttons, "
			"the driver declares FLIP_SW(FLIP_L) only, the VPinMAME library writes this position only when the table configures an upper flipper solenoid (it does not), and holding it in play changed no output."
		)
		item["provenance"] = prov("validated", S_CORE, S_LIBRARY, S_RUNTIME)
		item["spatial"] = not_applicable("unused", S_CORE, S_RUNTIME)
	return item


DIP_FUNCTIONS = {
	1: "Credits per coin, coin chute #1 (hinge side), bit of S1-S5",
	2: "Credits per coin, coin chute #1 (hinge side), bit of S1-S5",
	3: "Credits per coin, coin chute #1 (hinge side), bit of S1-S5",
	4: "Credits per coin, coin chute #1 (hinge side), bit of S1-S5",
	5: "Credits per coin, coin chute #1 (hinge side), bit of S1-S5",
	6: "High score to date award, with S7 (no award, one, two or three credits)",
	7: "High score to date award, with S6",
	8: "Sound option, with S32 (tunes, chimes and noises)",
	9: "Credits per coin, coin chute #3, bit of S9-S13",
	10: "Credits per coin, coin chute #3, bit of S9-S13",
	11: "Credits per coin, coin chute #3, bit of S9-S13",
	12: "Credits per coin, coin chute #3, bit of S9-S13",
	13: "Credits per coin, coin chute #3, bit of S9-S13",
	14: "High score and special award mode, with S15 (replay, extra ball or novelty)",
	15: "High score and special award mode, with S14",
	16: "Balls per game (ON 5, OFF 3)",
	17: "Maximum credits, with S18 and S19 (5 to 40)",
	18: "Maximum credits, with S17 and S19",
	19: "Maximum credits, with S17 and S18",
	20: "Credit display (ON shown)",
	21: "Match feature (ON enabled)",
	22: "In-line targets spot a PARAGON letter (ON liberal)",
	23: "Paragon saucer score (ON 3,000 and 2 bonus advances, OFF 500 and 1)",
	24: "Paragon saucer letters (ON advance one at a time, OFF scan)",
	25: "Credits per coin, coin chute #2, bit of S25-S28 (all off = same as chute #1)",
	26: "Credits per coin, coin chute #2, bit of S25-S28",
	27: "Credits per coin, coin chute #2, bit of S25-S28",
	28: "Credits per coin, coin chute #2, bit of S25-S28",
	29: "Waterfall lane 5,000 lite on at the start of a ball (ON liberal)",
	30: "In-line drop target score (ON 3,000 and 2 bonus advances, OFF 1,000 and 1)",
	31: "Waterfall drop target special (ON once, then 25,000 lites; OFF repeatable)",
	32: "Sound option, with S8",
}


def dip_switch(number: int) -> dict:
	return {
		"id": f"dip.option-switch-{number}",
		"label": f"MPU option switch S{number}",
		"kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": number},
		"aliases": aliases(("pinmame.dip", number), ("manual.address", f"S{number}")),
		"availability": "used",
		"physical": {
			"switch_type": "dip",
			"location": "MPU module A4, back box",
			"notes": f"Printed function: {DIP_FUNCTIONS[number]}. The manual's game-adjustment pages assign all thirty-two switches; their tables are transcribed in the game-adjustment excerpt.",
		},
		"provenance": prov("validated", S_MANUAL, S_CORE),
		"spatial": not_applicable("dip_switch", S_MANUAL),
	}


def all_inputs() -> list[dict]:
	items = [
		service_switch(-7, "Self-test button", "Inside the coin door", "The manual's self-test button inside the front door. In the retained runs, three presses reach the solenoid test, a fourth ends it and a fifth starts the switch test; the manual's bookkeeping pages say nine presses reach the first bookkeeping entry.", "service.self-test"),
		service_switch(-6, "CPU diagnostic button", "MPU module", "Named swCPUDiag in the retained VPinMAME Bally library; the manual does not describe this input.", "service.diagnostic"),
		service_switch(-5, "Sound diagnostic button", "Sound module", "Named swSoundDiag in the retained VPinMAME Bally library; the manual does not describe this input.", "service.diagnostic"),
	]
	for number in range(1, 49):
		items.append(matrix_switch(number) if number in SWITCHES else unused_switch(number))
	items.extend([
		flipper_button(81, "Upper-right flipper button position", "unused", "right"),
		flipper_button(82, "Right flipper button", "used", "right"),
		flipper_button(83, "Upper-left flipper button position", "unused", "left"),
		flipper_button(84, "Left flipper button", "used", "left"),
	])
	items.extend(dip_switch(number) for number in range(1, 33))
	return items


# ----------------------------------------------------------------------------------------------
# Solenoids
# ----------------------------------------------------------------------------------------------

# public -> (self-test number, label, kind, connection, printed connector name, part, object, roles, notes)
COILS = {
	1: (10, "Bottom thumper bumper", "coil", "A3J1-3", "LT. BOT. T.B.", "AN-26-1200", "Bumper1", [], "Fired by switch 37."),
	2: (12, "In-line drop target reset", "coil", "A3J1-2", "DR. TAR. (IN LINE)", "NO-26-1900", "inline-bank", [],
		"Raises the four Valley of Demons targets 1-4 together. The ROM fires it at game start and at the start of each ball, not when the bank is completed: the manual says the Treasure Chamber saucer resets the targets on its second entry in a ball. It is placed at the bank's centre (the mean of the four primary target walls) because the coil is a hidden assembly under the bank."),
	6: (2, "Knocker", "coil", "A3J2-5", "KNOCKER", "AR-26-1200", None, ["cabinet.knocker"], "Figure V's legend puts solenoid 02 in the cabinet."),
	7: (1, "Outhole kicker", "coil", "A3J1-5", "OUTHOLE", "AN-26-1200", "Drain", ["internal.trough"],
		"Kicks the ball from the outhole to the shooter lane. The ROM fires it when a credit starts a game and after each drain while switch 8 is closed."),
	8: (3, "Treasure chamber saucer kicker", "coil", "A3J5-10", "TREASURE CHAMBER SAUCER", "AO-27-1300", "SW31", [], "Fired by the ball resting on switch 31."),
	9: (5, "Golden cliffs saucer kicker", "coil", "A3J5-12", "GOLDEN CLIFFS SAUCER", "AO-27-1300", "sw32", [], "Fired by the ball resting on switch 32."),
	10: (4, "Paragon saucer kicker", "coil", "A3J5-11", "PARAGON SAUCER", "AO-27-1300", "sw24", [], "Fired by the ball resting on switch 24."),
	11: (8, "Left thumper bumper", "coil", "A3J5-9", "LEFT THUMPER BUMPER", "AN-26-1200", "Bumper4", [], "Fired by switch 40."),
	12: (9, "Right thumper bumper", "coil", "A3J5-15", "RIGHT THUMPER BUMPER", "AN-26-1200", "Bumper3", [], "Fired by switch 39."),
	13: (11, "Center thumper bumper", "coil", "A3J5-13", "CENTER THUMPER BUMPER", "AN-26-1200", "Bumper2", [], "Fired by switch 38."),
	14: (6, "Left slingshot", "coil", "A3J5-14", "LEFT SLINGSHOT", "AN-26-1200", "LeftSlingShot", [], "Fired by switch 36."),
	15: (7, "Right slingshot", "coil", "A3J5-8", "RIGHT SLINGSHOT", "AN-26-1200", "RightSlingShot", [], "Fired by switch 35."),
	17: (13, "Waterfall drop target reset", "coil", "A3J5-7", "DROP TARGET (3)", "NO-26-1900", "sw18", [],
		"Raises the three waterfall targets 17-19. The ROM fires it at game start, at the start of each ball and once all three targets are down. It is a continuous output (PIA1:B bit 4, published at 17) that the ROM pulses. It is placed on the bank's middle target because the coil is a hidden assembly behind the bank."),
	18: (14, "Coin lockout door", "coil", "A3J2-8", "COIN LOCKOUT", "FO-36-7000", None, ["cabinet.coin-door"], "A continuous output. Figure V's legend puts solenoid 14 on the door; the ROM holds it energized in attract mode and play."),
	19: (15, "K1 relay (flipper enable)", "relay", None, None, None, None, ["cabinet.relay"],
		"A continuous output. Raised by the ROM when a credit starts a game and held until game over; a tilt drops it and the flipper buttons then do nothing. Figure V's legend puts solenoid 15 in the back box, and the drawing prints 15 beside all four flippers, whose coils it switches."),
}
UNUSED_MOMENTARY = (3, 4, 5)


def coil_output(address: int) -> dict:
	test, label, kind, connection, printed, part, obj, roles, notes = COILS[address]
	device_id = f"device.{slug(label)}"
	physical: dict = {"location": label}
	if part:
		physical["part_number"] = part
	text = (
		f"Printed self-test number {test:02d}. The printed number is the order in which the ROM's solenoid test fires the coils, not a public address; "
		f"the retained solenoid test fires public {address} while it shows {test:02d}, identically on all four drivers."
	)
	if printed:
		text += f' The plug-connector sheet names connector pin {connection} "{printed}".'
	text += " " + notes
	physical["notes"] = text
	item = {
		"id": device_id,
		"label": label,
		"kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address), ("manual.self-test", test)),
		"availability": "used",
		"physical": physical,
		"provenance": prov("validated", S_MANUAL, S_SCHEMATIC, S_RUNTIME, *((S_SCRIPT,) if address in (2, 6, 7, 8, 9, 10, 17, 19) else ())),
	}
	if connection:
		item["wiring"] = {"board": "Solenoid driver / voltage regulator A3", "drive_connection": connection}
	if roles:
		item["roles"] = roles
	if obj is None:
		item["spatial"] = not_applicable("cabinet_or_service", S_MANUAL)
	else:
		point = INLINE_BANK_CENTRE if obj == "inline-bank" else at(obj)
		item["spatial"] = located("observed", placement(f"{device_id}.effect", "effect", point, "observed", S_TABLE, S_MANUAL))
	return item


def _inline_bank_centre() -> tuple[float, float]:
	xs = [OBJECTS[name]["raw_x"] for name in ("sw1", "sw2", "sw3", "sw4")]
	ys = [OBJECTS[name]["raw_y"] for name in ("sw1", "sw2", "sw3", "sw4")]
	return round(sum(xs) / 4 / BOUNDS["right"], 6), round(sum(ys) / 4 / BOUNDS["bottom"], 6)


INLINE_BANK_CENTRE = _inline_bank_centre()


def unused_coil(address: int) -> dict:
	if address == 20:
		note = (
			"The fourth continuous output. The manual's solenoid table names fifteen loads and none of them is on this address, the plug-connector sheet names no load for it, "
			"and the retained runs show it asserted only in the power-on pulse that briefly drives all four continuous outputs, never during the self tests or a game."
		)
		label = "Unused continuous output 20"
	else:
		note = (
			f"The manual's solenoid table names fifteen loads and the ROM's solenoid test fires fifteen public addresses, none of them {address}; "
			f"the retained runs never assert {address}. The A3 J1, J2 and J5 load connectors carry no further named coil."
		)
		label = f"Unused solenoid output {address}"
	return {
		"id": f"device.unused-solenoid-{address}",
		"label": label,
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address)),
		"availability": "unused",
		"physical": {"notes": note},
		"provenance": prov("validated", S_MANUAL, S_SCHEMATIC, S_RUNTIME),
		"spatial": not_applicable("unused", S_MANUAL, S_RUNTIME),
	}


def flipper_output(address: int, side: str) -> dict:
	objects = ("LeftFlipper", "LeftFlipper1") if side == "left" else ("RightFlipper", "RightFlipper1")
	extra = "the small upper-left flipper on the left wall, aimed at the Valley of Demons targets" if side == "left" else "the right flipper above the lower right one, aimed at the waterfall targets"
	connection = "A3J1-8" if side == "left" else "A3J1-9"
	printed = "L. FLIP COIL" if side == "left" else "R. FLIP COIL"
	notes = (
		f"Two flipper coils: the lower {side} flipper and {extra}. The parts list counts Flipper (4), AQ-25-500/34-4500. The coils are not on a driver transistor: "
		f"the plug-connector sheet runs them to {connection} \"{printed}\" and the {side} button to the solenoid driver, switched through the K1 flipper-enable relay (19). "
		f"PinMAME publishes the generic lower-{side} flipper output {address} while the {side} button ({82 if side == 'right' else 84}) is held with the relay up, and also raises {address - 1}, "
		f"which the BY35 controller profile does not declare. The known-working script drives both {side} flippers from {address}."
	)
	if side == "right":
		notes += " IPDB records that some machines shipped to Europe (reportedly all French ones) had only three flippers: the upper right flipper was not installed and a ball guide and post replaced it, so on those machines this output drives one coil."
	return {
		"id": f"device.{side}-flippers",
		"label": f"{side.title()} flippers (lower and {'upper-left' if side == 'left' else 'upper-right'})",
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address), ("manual.self-test", 15)),
		"availability": "used",
		"physical": {"location": f"{side.title()} flipper assemblies", "part_number": "AQ-25-500/34-4500", "quantity": 2, "notes": notes},
		"wiring": {"board": "Hard-wired flipper circuit switched by the K1 relay", "drive_connection": connection, "control_connection": "A3J2-1" if side == "right" else "A3J2-2"},
		"provenance": prov("validated", S_MANUAL, S_SCHEMATIC, S_SCRIPT, S_CORE, S_RUNTIME, S_IPDB),
		"spatial": located("observed", *(
			placement(f"device.{side}-flippers.{'lower' if name.endswith('Flipper') else 'upper'}", "effect", at(name), "observed", S_TABLE, S_MANUAL)
			for name in objects
		)),
	}


# ----------------------------------------------------------------------------------------------
# Lamps
# ----------------------------------------------------------------------------------------------

# public -> (label, connector pin, printed function, art identification)
LAMPS = {
	1: ("1K bonus", "A5J1-18", "1K BONUS", "an insert printed 1 Thousand in the bonus ladder"),
	2: ("5K bonus", "A5J1-19", "5K BONUS", "an insert printed 5 Thousand in the bonus ladder"),
	3: ("9K bonus", "A5J1-17", "9K BONUS", "an insert printed 9 Thousand in the bonus ladder"),
	4: ("40K super bonus", "A5J1-23", "40 K SUPER BONUS", "an insert printed 40 Thousand in the super bonus row"),
	5: ("25K drop target", "A5J1-14", "25 K DROP TARGET", "the insert beside 25,000 in the waterfall drop-target value column"),
	6: ("2X bonus", "A5J1-15", "2X BONUS", "an insert printed 2x"),
	7: ('Saucer "P"', "A5J1-16", 'SAUCER "P"', "the first letter, P, of the PARAGON arc around the Paragon saucer"),
	8: ('Saucer "G"', "A5J1-28", 'SAUCER "G"', "the G of the PARAGON arc around the Paragon saucer"),
	9: ('Center "P"', "A5J1-24", 'CENTER "P"', "the first letter, P, of the centre PARAGON row"),
	10: ('Center "G"', "A5J1-25", 'CENTER "G"', "the G of the centre PARAGON row"),
	11: ("Shoot again", "A5J2-21", "SHOOT AGAIN", None),
	12: ("2K golden cliff", "A5J1-27", "2K GOLDEN CLIFF", "an insert printed 2 Thousand in the golden cliffs row"),
	13: ("Ball in play", "A5J2-22", "BALL IN PLAY", None),
	14: ("Spinner 1 (bottom)", "A5J2-16", "SPINNER (1) BOTTOM", "the bottom of the four plain spinner-value inserts beside the spinner"),
	15: ("10K waterlane", "A5J2-14", "10 K WATERLANE", "the insert above 10000 in the waterfall lane"),
	17: ("2K bonus", "A5J1-1", "2K BONUS", "an insert printed 2 Thousand in the bonus ladder"),
	18: ("6K bonus", "A5J1-9", "6K BONUS", "an insert printed 6 Thousand in the bonus ladder"),
	19: ("10K bonus", "A5J1-8", "10K BONUS", "an insert printed 10 Thousand in the bonus ladder"),
	20: ("10K drop target", "A5J1-3", "10K DROP TARGET", "the insert beside 10,000 in the waterfall drop-target value column"),
	21: ("Water lane special", "A5J1-2", "WATER LANE SPECIAL", "the red insert above Special in the waterfall lane"),
	22: ("3X bonus", "A5J1-10", "3X BONUS", "an insert printed 3x"),
	23: ('Saucer "A" (left)', "A5J1-7", 'SAUCER "A" (LEFT)', "the second letter, A, of the PARAGON arc around the Paragon saucer"),
	24: ('Saucer "O"', "A5J1-6", 'SAUCER "O"', "the O of the PARAGON arc around the Paragon saucer"),
	25: ('Center "A" (left)', "A5J1-5", 'CENTER "A" (LEFT)', "the second letter, A, of the centre PARAGON row"),
	26: ('Center "O"', "A5J1-11", 'CENTER "O"', "the O of the centre PARAGON row"),
	27: ("Match", "A5J2-8", "MATCH", None),
	28: ("4K golden cliff", "A5J1-12", "4K GOLDEN CLIFF", "an insert printed 4 Thousand in the golden cliffs row"),
	29: ("High score to date", "A5J2-23", "HIGH SCORE TO DATE", None),
	30: ("Spinner 2", "A5J2-20", "SPINNER (2)", "the second of the four plain spinner-value inserts, counted from the bottom"),
	31: ("5K waterlane", "A5J2-15", "5 K WATERLANE", "the insert above 5000 in the waterfall lane"),
	33: ("3K bonus", "A5J3-26", "3K BONUS", "an insert printed 3 Thousand in the bonus ladder"),
	34: ("7K bonus", "A5J3-25", "7K BONUS", "an insert printed 7 Thousand in the bonus ladder"),
	35: ("20K super bonus", "A5J3-19", "20 K SUPER BONUS", "an insert printed 20 Thousand in the super bonus row"),
	36: ("15K drop target", "A5J3-17", "15 K DROP TARGET", "the insert beside 15,000 in the waterfall drop-target value column"),
	37: ("Paragon saucer special", "A5J3-16", "PARAGON SAUCER SPECIAL", "the red insert under the caption Saucer Scores SPECIAL"),
	38: ("5X bonus", "A5J3-23", "5X BONUS", "an insert printed 5x"),
	39: ('Saucer "R"', "A5J3-27", 'SAUCER "R"', "the R of the PARAGON arc around the Paragon saucer"),
	40: ('Saucer "N"', "A5J1-13", 'SAUCER "N"', "the last letter, N, of the PARAGON arc around the Paragon saucer"),
	41: ('Center "R"', "A5J3-21", 'CENTER "R"', "the R of the centre PARAGON row"),
	42: ('Center "N"', "A5J3-20", 'CENTER "N"', "the last letter, N, of the centre PARAGON row"),
	43: ("Same player shoots again", "A5J3-22", "SAME PLAYER S.A.", "the red insert printed SHOOT AGAIN on the playfield"),
	44: ("6K golden cliff", "A5J3-24", "6 K GOLDEN CLIFF", "an insert printed 6 Thousand in the golden cliffs row"),
	45: ("Game over", "A5J2-11", "GAME OVER", None),
	46: ("Spinner 3", "A5J2-6", "SPINNER (3)", "the third of the four plain spinner-value inserts, counted from the bottom"),
	47: ("10K golden cliff", "A5J2-2", "10 K GOLDEN CLIFF", "an insert printed 10 Thousand in the golden cliffs row"),
	49: ("4K bonus", "A5J3-1", "4K BONUS", "an insert printed 4 Thousand in the bonus ladder"),
	50: ("8K bonus", "A5J3-12", "8K BONUS", "an insert printed 8 Thousand in the bonus ladder"),
	51: ("30K super bonus", "A5J3-15", "30 K SUPER BONUS", "an insert printed 30 Thousand in the super bonus row"),
	52: ("20K drop target", "A5J3-11", "20 K DROP TARGET", "the insert beside 20,000 in the waterfall drop-target value column"),
	53: ("5X treasure saucer", "A5J3-9", "5X TREASURE SAUCER", "the white insert above 5X in the Treasure Chamber lane"),
	54: ("Extra ball treasure saucer", "A5J3-3", "EXTRA BALL TREASURE SAUCER", "the lower of the two red inserts in the Treasure Chamber lane, beside the plastic's caption EXTRA BALL When LIT"),
	55: ('Saucer "A" (right)', "A5J3-4", 'SAUCER "A" (RIGHT)', "the fourth letter, A, of the PARAGON arc around the Paragon saucer"),
	56: ("Special treasure saucer", "A5J3-2", "SPECIAL TREASURE SAUCER", "the upper of the two red inserts in the Treasure Chamber lane, beside the plastic's caption SPECIAL When LIT"),
	57: ('Center "A" (right)', "A5J3-10", 'CENTER "A" RIGHT', "the fourth letter, A, of the centre PARAGON row"),
	58: ("Special drop target", "A5J3-18", "SPECIAL DROP TARGET", "the red insert beside SPECIAL in the waterfall drop-target value column"),
	59: ("Credit indicator", "A5J3-13", "CREDIT INDICATOR", "the credit window in the apron"),
	60: ("8K golden cliff", "A5J3-14", "8 K GOLDEN CLIFF", "an insert printed 8 Thousand in the golden cliffs row"),
	61: ("Tilt", "A5J2-10", "TILT", None),
	62: ("Spinner 4 (top)", "A5J2-7", "SPINNER (4) (TOP)", "the top of the four plain spinner-value inserts beside the spinner"),
	63: ("20K golden cliff", "A5J2-1", "20 K GOLDEN CLIFF", "an insert printed 20 Thousand in the golden cliffs row"),
}
BACKBOX_LAMPS = {11, 13, 27, 29, 45, 61}
J2_PLAYFIELD = {14, 15, 30, 31, 46, 47, 62, 63}
RUNTIME_LAMPS = {6, 14, 22, 61}
SPINNER_LAMPS = (14, 30, 46, 62)

LAMP_CHAIN = (
	"PinMAME publishes the main lamp board as public = 16 * d + a + 1 (d the lamp-data line PD0-PD3, a the latched decoder address 0-14), and the AS-2518-23 board takes each decoder output "
	"through its own SCR to a fixed connector pin; this record takes that board chain from the Kiss record, which carries the same board and derived it from its own sheets. "
	"The function on each pin is read from Paragon's own A5 lamp driver schematic (W-1182-15) and plug-connector sheet (W-1187-11), which agree pin for pin."
)


def lamp_output(public: int) -> dict:
	label, connection, printed, art = LAMPS[public]
	device_id = f"lamp.{slug(label)}"
	notes = [f'Connector pin {connection}, printed "{printed}".']
	physical: dict = {}
	if public in BACKBOX_LAMPS:
		physical["location"] = "backglass"
		notes.append("The A5 J2 connector is marked TO BACKBOX and the plug-connector sheet's A1 insert block labels this line, so it is a back box lamp with no playfield position.")
		if public == 11:
			notes.append("It is the backglass Shoot Again; the playfield SHOOT AGAIN insert is public 43. The retained table's VR backglass reads lamp 43 for its shoot-again flasher, and its light named L11 is a GI rollover lamp, not this output.")
		if public == 13:
			notes.append("The pinned script binds Lights(13) to an object L13 that the retained table does not contain; the retained table comments that line out and reads lamp 13 for its VR backglass Ball In Play.")
		if public == 27:
			notes.append("The retained table's VR backglass reads lamp 45, not 27, for its Match flasher (a defect in that table), and its light named L27 is a GI rollover lamp, not this output.")
		if public == 29:
			notes.append("The retained table's light named L29 is a GI rollover lamp, not this output.")
		if public == 61:
			notes.append("A tilt in play lit it.")
	else:
		physical["location"] = "playfield"
		if public in J2_PLAYFIELD:
			notes.append("Its pin is on A5 J2, which the sheet brackets TO BACKBOX, but the function is a playfield lamp and the plug-connector sheet's Table B routes this pin on through the panel-to-back-cab plug to the playfield.")
		if public == 43:
			notes.append("The plug-connector sheet calls it SAME PLAYER S.A.; it is the playfield insert, distinct from the backglass SHOOT AGAIN on public 11.")
		if public in SPINNER_LAMPS:
			notes.append("The four plain inserts carry no printed value; the sheet numbers the lamps 1 (bottom) to 4 (top), the table's lights run in that order up the column, and a fifth insert below them is lit from the table's GI.")
		if public == 14:
			notes.append("A spinner closure in play lit it.")
		if public in (6, 22):
			notes.append(f"Knocking down in-line target {'C (public 2) third' if public == 6 else 'D (public 1) last'} in play lit it.")
		notes.append(f"Its placement is the table's light L{public}, which sits on {art} in the table's playfield scan.")
	notes.append(LAMP_CHAIN)
	physical["notes"] = " ".join(notes)
	sources = [S_SCHEMATIC, S_SCRIPT, S_TABLE]
	if public in RUNTIME_LAMPS:
		sources.append(S_RUNTIME)
	item = {
		"id": device_id,
		"label": label,
		"kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": public},
		"aliases": aliases(("pinmame.lamp", public), ("manual.address", connection)),
		"availability": "used",
		"physical": physical,
		"wiring": {"board": "Lamp driver A5 (AS-2518-23)", "drive_connection": connection},
	}
	if public in BACKBOX_LAMPS:
		item["roles"] = ["cabinet.backglass"]
		item["provenance"] = prov("validated", S_SCHEMATIC, S_MANUAL, *((S_RUNTIME,) if public == 61 else ()))
		item["spatial"] = not_applicable("cabinet_or_service", S_SCHEMATIC, S_MANUAL)
		return item
	item["provenance"] = prov("validated", *sources)
	item["spatial"] = located("validated", placement(f"{device_id}.emitter", "emitter", at(f"L{public}"), "validated", S_TABLE, S_SCHEMATIC))
	return item


def all_outputs() -> list[dict]:
	items = [coil_output(address) for address in sorted(COILS)]
	items.extend(unused_coil(address) for address in (*UNUSED_MOMENTARY, 20))
	items.extend([flipper_output(46, "right"), flipper_output(48, "left")])
	items.extend(lamp_output(public) for public in sorted(LAMPS))
	items.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return items


# ----------------------------------------------------------------------------------------------
# Mechanisms, relationships, displays, drivers, sources
# ----------------------------------------------------------------------------------------------

def sid(number: int) -> str:
	return f"switch.{slug(SWITCHES[number][0])}"


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, part: str | None = None) -> dict:
	item = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": prov("validated", *refs)}
	if part:
		item["assembly_part_number"] = part
	return item


def mechanisms() -> list[dict]:
	return [
		mechanism(
			"mechanism.outhole", "Outhole and shooter feed", "kicker", ["device.outhole-kicker"], [sid(8)],
			"Paragon is a one-ball game with no trough: the ball drains into the outhole below the flippers, closing switch 8, and the outhole kicker (public 7) serves it to the shooter alley, where the player launches it with the plunger. "
			"The ROM adds the bonus when the ball enters the outhole, then kicks it; a credit with the ball in the outhole starts the game, kicks the ball and resets both drop-target banks in the same step.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.valley-of-demons-in-line-drop-targets", "Valley of Demons four in-line drop targets", "drop_target_bank", ["device.in-line-drop-target-reset"], [sid(4), sid(3), sid(2), sid(1)],
			"Four drop targets standing one behind the other on the left wall, A (switch 4) at the front to D (switch 1) at the back; the ball can reach each only once the ones in front of it are down. "
			"Each target scores and advances the bonus; the third (C) awards the 2X multiplier and the fourth (D) the 3X. Completing the bank does not reset it: the Treasure Chamber saucer resets the targets on its second entry in a ball, "
			"and the ROM fires the shared reset coil (public 2) at game start and at each new ball. Option S22 lets each target spot a PARAGON letter.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="NO-26-1900"),
		mechanism(
			"mechanism.waterfall-drop-targets", "Waterfall three-bank drop targets", "drop_target_bank", ["device.waterfall-drop-target-reset"], [sid(17), sid(18), sid(19)],
			"Three drop targets on the right, C (switch 17) at the front to A (switch 19) at the rear, each scoring 500. Knocking all three down scores the lit value (10,000, 15,000, 20,000, 25,000, then special), advances the waterfall lane value, "
			"and makes the ROM fire the shared reset coil (public 17). The value is remembered from ball to ball.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="NO-26-1900"),
		mechanism(
			"mechanism.treasure-chamber-saucer", "Treasure Chamber saucer", "kicker", ["device.treasure-chamber-saucer-kicker"], [sid(31)],
			"An upper-left saucer at the end of a narrow lane: a clear plastic guide on the lane's left and a metal deadening piece on its right slow the ball so it drops in, and the saucer kicks it up towards the top of the playfield (public 8). "
			"It always scores 5,000; its first entry in a ball awards 5X, its second the same-player-shoots-again lite and resets the in-line targets, and once all four targets are down again it awards a special.",
			S_MANUAL, S_KMIEC, S_SCRIPT, S_RUNTIME, part="AO-27-1300"),
		mechanism(
			"mechanism.golden-cliffs-saucer", "Golden Cliffs saucer", "kicker", ["device.golden-cliffs-saucer-kicker"], [sid(32)],
			"A top left-centre saucer that scores the lit golden cliffs value (2,000 up to 20,000), advances it one step, and kicks the ball out (public 9). The value is remembered from ball to ball; IPDB notes that each entry adds a note to a tune.",
			S_MANUAL, S_IPDB, S_SCRIPT, S_RUNTIME, part="AO-27-1300"),
		mechanism(
			"mechanism.paragon-saucer", "Paragon saucer", "kicker", ["device.paragon-saucer-kicker"], [sid(24)],
			"A top right saucer ringed by the seven PARAGON letters. Each entry spots the lit letter in the centre PARAGON row, scores and advances the bonus, and kicks the ball out (public 10). With all seven spotted the special lite lights; the next entry scores 25,000 and a special and resets the letters.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AO-27-1300"),
		mechanism(
			"mechanism.thumper-bumpers", "Four thumper bumpers", "other",
			["device.left-thumper-bumper", "device.right-thumper-bumper", "device.center-thumper-bumper", "device.bottom-thumper-bumper"], [sid(40), sid(39), sid(38), sid(37)],
			"Three bumpers in the upper middle (left, right and centre) and one at the lower left above the Beast's Lair. Each skirt switch makes the ROM fire its own coil: 40 fires 11, 39 fires 12, 38 fires 13 and 37 fires 1.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.slingshots", "Two slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], [sid(36), sid(35)],
			"The pair above the lower flippers: switch 36 makes the ROM fire the left slingshot (14) and switch 35 the right (15).",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.spinner", "Spinner", "other", [], [sid(33)],
			"A spinner on the left whose switch closes once per rotation. The manual says it advances the bonus; its four lamps (14, 30, 46, 62, bottom to top) sit in a column the art captions ADVANCE BONUS When LIT, and a closure in play lit lamp 14.",
			S_MANUAL, S_SCRIPT, S_RUNTIME),
		mechanism(
			"mechanism.flippers", "Four flippers", "other", ["device.left-flippers", "device.right-flippers", "device.k1-relay-flipper-enable"],
			["switch.left-flipper-button", "switch.right-flipper-button"],
			"Two lower flippers and two extra Paragon flippers: a small one on the left wall aimed at the Valley of Demons targets and one on the right above the lower right flipper aimed at the waterfall targets. Each button fires both flippers of its side. "
			"The K1 relay (public 19) switches the flipper circuits: it is raised from game start to game over and dropped by a tilt. European machines that shipped with three flippers lack the upper right flipper.",
			S_MANUAL, S_SCHEMATIC, S_SCRIPT, S_RUNTIME, S_IPDB, part="AQ-25-500/34-4500"),
	]


def relationships() -> list[dict]:
	items = [
		("rel.left-slingshot", "direct", sid(36), "device.left-slingshot"),
		("rel.right-slingshot", "direct", sid(35), "device.right-slingshot"),
		("rel.left-thumper-bumper", "direct", sid(40), "device.left-thumper-bumper"),
		("rel.right-thumper-bumper", "direct", sid(39), "device.right-thumper-bumper"),
		("rel.center-thumper-bumper", "direct", sid(38), "device.center-thumper-bumper"),
		("rel.bottom-thumper-bumper", "direct", sid(37), "device.bottom-thumper-bumper"),
		("rel.treasure-chamber-saucer", "pulse", sid(31), "device.treasure-chamber-saucer-kicker"),
		("rel.golden-cliffs-saucer", "pulse", sid(32), "device.golden-cliffs-saucer-kicker"),
		("rel.paragon-saucer", "pulse", sid(24), "device.paragon-saucer-kicker"),
		("rel.outhole", "pulse", sid(8), "device.outhole-kicker"),
		("rel.left-flippers", "relay_gated", "switch.left-flipper-button", "device.left-flippers"),
		("rel.right-flippers", "relay_gated", "switch.right-flipper-button", "device.right-flippers"),
	]
	return [{"id": rid, "kind": kind, "source": source, "destination": destination, "provenance": prov("validated", S_MANUAL, S_RUNTIME)} for rid, kind, source, destination in items]


def displays() -> list[dict]:
	refs = (S_CORE, S_MANUAL, S_RUNTIME)
	items = []
	for number, start in enumerate((2, 10, 18, 26), start=1):
		items.append({
			"id": f"display.player-{number}-score", "label": f"Player {number} score, six digits", "kind": "segment",
			"controller_index": number - 1, "segment_start": start, "width": 6,
			"provenance": prov("validated", *refs), "spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
		})
	items.append({
		"id": "display.credits", "label": "Credits, two digits", "kind": "segment", "controller_index": 4, "segment_start": 35, "width": 2,
		"provenance": prov("validated", *refs), "spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
	})
	items.append({
		"id": "display.ball-in-play-match", "label": "Match and ball in play, two digits", "kind": "segment", "controller_index": 5, "segment_start": 38, "width": 2,
		"provenance": prov("validated", *refs), "spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
	})
	return items


def drivers() -> list[dict]:
	seven = [
		{"target": f"display.player-{number}-score", "segment_start": start, "width": 7, "provenance": prov("validated", S_CORE, S_RUNTIME)}
		for number, start in enumerate((1, 9, 17, 25), start=1)
	]
	return [
		{"id": "paragon", "description": "Paragon", "year": "1979", "manufacturer": "Bally", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "The 1979 production ROM set and the reference for this definition: GEN_BY35, six-digit displays (dispBy6), FLIP_SW(FLIP_L), lampCol 0, sound board SNDBRD_BY50."},
		{"id": "paragonb", "clone_of": "paragon", "description": "Paragon (7-digit conversion rev. 20)", "year": "2004", "manufacturer": "Bally / Oliver", "flags": 0, "physical_compatibility": "compatible",
		 "variant_notes": "A 2004 Bally/Oliver conversion ROM that widens the four player displays to seven digits (dispBy7); it needs seven-digit display hardware and otherwise drives the same machine: in the retained solenoid test it fires the same fifteen outputs in the same order and publishes the same sixty lamps.",
		 "display_overrides": seven},
		{"id": "paragonc", "clone_of": "paragon", "description": "Paragon (Free Play rev. 3)", "year": "2008", "manufacturer": "Bally / Oliver", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "A 2008 Bally/Oliver free-play ROM for the production hardware with six-digit displays; its retained solenoid test matches the production set's."},
		{"id": "paragond", "clone_of": "paragon", "description": "Paragon (/10 Scoring Free Play)", "year": "2008", "manufacturer": "Bally / Oliver", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "A 2008 free-play ROM that divides scoring by ten to fit six digits; same hardware, and its retained solenoid test matches the production set's."},
	]


def excerpt_entries(source_id: str) -> list[dict]:
	seed = json.loads(EXCERPT_SEED_PATH.read_text(encoding="utf-8"))
	entries = []
	for item in seed["excerpts"]:
		if item["source"] != source_id:
			continue
		path = ROOT / EXCERPT_DIR / f"{item['name']}.md"
		entry = {
			"id": f"excerpt.paragon.{item['name']}",
			"locator": item["locator"],
			"path": f"{EXCERPT_DIR}/{item['name']}.md",
			"sha256": file_sha256(path),
			"method": item.get("method", "manual"),
			"transcribed_by": item.get("transcribed_by", "curator, read from the rendered page"),
			"reviewed": True,
		}
		if item.get("image_derivation"):
			image = ROOT / EXCERPT_DIR / f"{item['name']}.webp"
			entry["image"] = f"{EXCERPT_DIR}/{item['name']}.webp"
			entry["image_sha256"] = file_sha256(image)
			entry["image_derivation"] = item["image_derivation"]
		entries.append(entry)
	return entries


MANUAL_SHA = "3da1eceb7cb3b27f268f11ad438c8e00ced0ad150051a137d55bf662515725f6"
SCHEMATIC_SHA = "a440fdc38cbc9243154fe64a3aeec3ee61c8973893ecaf434d3a28346ae01c9a"


def sources() -> list[dict]:
	return [
		{"id": S_CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
		 "locator": "PinmameGetGames entries paragon, paragonb, paragonc and paragond (the last three clones of paragon)", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
		 "locator": "src/wpc/by35games.c lines 17-26 (dispBy6 and dispBy7 layouts) and 528-561 (paragon, paragonb, paragonc, paragond: INITGAME GEN_BY35, FLIP_SW(FLIP_L), lampCol 0, SNDBRD_BY50; paragonb dispBy7); src/wpc/by35.c (PIA handlers, by35_lampStrobe, core_updateSw(core_getSol(19))); src/wpc/core.c core_updateSw (flipper column and the synthetic flipper outputs); src/wpc/core.h sLRFlip 46 and sLLFlip 48",
		 "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/by35.json", "revision": PINMAME_REVISION,
		 "locator": "Controller profile pinmame.by35: public ranges for switches (-7..-5, 1..48, 81..88), option switches 1..32, solenoids 1..15, 17..20, 46 and 48, and lamps; momentary address = selector + 1, continuous outputs at 17-20",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs contributors"},
		{"id": S_IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=1755", "acquired_at": "2026-10-16T20:51:00Z",
		 "sha256": "ad11743bb3bf09b293793c493c94eacd4cb83005f7b4bcc314434fb0f4d4769d", "original_filename": "ipdb1755.html",
		 "locator": "IPDB machine id 1755: Paragon, Bally Manufacturing Corporation, project date December 05, 1978, manufactured June 1979, model number 1167-E, MPU Bally AS-2518-35, 9,120 units, widebody; notable features 'Flippers (4), Pop bumpers (4), Slingshots (2), 4-in-line drop targets (1), 3-bank drop targets (1), Kick-out holes (3), Standup targets (2), Star rollovers (4), Spinning target (1)'; design Greg Kmiec, art Paul Faris. The notes record that an unknown quantity of machines shipped to Europe (reportedly all in France) had three flippers, with a ball guide and a single post replacing the upper right flipper and a mini-post added in the Beast's Lair. Retained as the Internet Archive capture https://web.archive.org/web/2024id_/https://www.ipdb.org/machine.cgi?id=1755.",
		 "license": "NOASSERTION", "attribution": "The Internet Pinball Database", "rights": "Rights not asserted; the retained copy is the page only, kept locally for curation"},
		{"id": S_MANUAL, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/bally.paragon.1979/Bally_1979_Paragon_Manual.pdf",
		 "sha256": MANUAL_SHA, "original_filename": "Bally_1979_Paragon_Manual.pdf", "source_id": "ipdb.1755", "acquired_at": "2026-10-16T20:51:00Z",
		 "rights": "Copyright Bally Manufacturing Corporation; retained locally for curation and not redistributed",
		 "locator": "35-page image-only scan of the Bally game #1167-E Paragon installation and general game operation instructions (IPDB file Bally_1979_Paragon_Manual.pdf, fetched through https://web.archive.org/web/20251204093753id_/https://www.ipdb.org/files/1755/Bally_1979_Paragon_Manual.pdf). PDF pages 4-8: installation, general operation, bookkeeping, feature operation and scoring; 9-12: game adjustments; 21: solenoid and switch identification; 22: Figure V switch and solenoid locations; 23-24: assembly adjustments and parts list.",
		 "license": "NOASSERTION", "attribution": "Bally Manufacturing Corporation; hosted by IPDB", "excerpts": excerpt_entries(S_MANUAL)},
		{"id": S_SCHEMATIC, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/bally.paragon.1979/Bally_1979_Paragon_Schematic_Diagrams_paginated.pdf",
		 "sha256": SCHEMATIC_SHA, "original_filename": "Bally_1979_Paragon_Schematic_Diagrams_paginated.pdf", "source_id": "ipdb.1755", "acquired_at": "2026-10-16T20:51:00Z",
		 "rights": "Copyright Bally Manufacturing Corporation; retained locally for curation and not redistributed",
		 "locator": "Twelve scanned schematic sheets (IPDB file Bally_1979_Paragon_Schematic_Diagrams_paginated.pdf, fetched through https://web.archive.org/web/20260127053947id_/https://www.ipdb.org/files/1755/Bally_1979_Paragon_Schematic_Diagrams_paginated.pdf). PDF page 3: A5 lamp driver schematic W-1182-15 for Paragon; page 5: plug connectors W-1187-11 for Paragon.",
		 "license": "NOASSERTION", "attribution": "Bally Manufacturing Corporation; hosted by IPDB", "excerpts": excerpt_entries(S_SCHEMATIC)},
		{"id": S_KMIEC, "kind": "human_review", "uri": "external:pinmame-manuals/by-machine/bally.paragon.1979/Bally_1979_Paragon_Greg_Kmiec_Discusses_Treasure_Chamber_Design.pdf",
		 "sha256": "d2a881029678f8297b590739f72b710c645062ed149001267703ad36850960de", "original_filename": "Bally_1979_Paragon_Greg_Kmiec_Discusses_Treasure_Chamber_Design.pdf", "source_id": "ipdb.1755",
		 "acquired_at": "2026-10-16T20:51:00Z",
		 "locator": "IPDB file for machine 1755 reproducing Greg Kmiec's 27 October 2012 reply to IPDB about the Treasure Chamber saucer (fetched through https://web.archive.org/web/20221024020948id_/https://www.ipdb.org/files/1755/Bally_1979_Paragon_Greg_Kmiec_Discusses_Treasure_Chamber_Design.pdf).",
		 "license": "NOASSERTION", "attribution": "Greg Kmiec and the Internet Pinball Database", "rights": "Short quotation for curation; the file is not redistributed", "excerpts": excerpt_entries(S_KMIEC)},
		{"id": S_LIBRARY, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/paragon-1979/library/Bally.vbs",
		 "sha256": "d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c",
		 "locator": "Bally.vbs (header 'Last Updated in VBS v3.61') and core.vbs (SHA-256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69), the VPinMAME libraries the table loads: cabinet-switch constants, flipper key handlers and the flipper solenoid constants.",
		 "license": "NOASSERTION", "attribution": "VPinMAME contributors", "excerpts": excerpt_entries(S_LIBRARY)},
		{"id": S_SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/special_audiopan_and_audiofade_patched/bord_probably/Paragon%20%28Bally%201979%29.vbs",
		 "revision": SCRIPT_REVISION, "sha256": "c61b0824933bea6f136dcd3b06da8304e175dbfe7b1e88725635dd5e7b053bcc", "known_working": True,
		 "locator": "Paragon (Bally 1979).vbs, bord's v2.37 on a base script by 32assassin: cGameName paragon, SolCallback and flipper callbacks, switch handlers, lamp bindings, VR backglass lamp reads. The retained table's embedded script equals this file except for whitespace, the corpus's audio patch and one commented-out lamp binding (Lights(13)).",
		 "license": "NOASSERTION", "attribution": "bord, 32assassin, iaakki, TastyWasps and vpxtable_scripts contributors", "excerpts": excerpt_entries(S_SCRIPT)},
		{"id": S_TABLE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/paragon-1979/source/Paragon (Bally 1979).vpx",
		 "sha256": SEED["table_sha256"], "original_filename": "Paragon (Bally 1979).vpx", "known_working": True, "acquired_at": "2026-10-16T20:53:00Z",
		 "locator": f"vpxtool git:v0.33.3 extraction, canonical manifest {SEED['extraction_manifest_sha256']}; playfield bounds left=0 top=0 right={BOUNDS['right']} bottom={BOUNDS['bottom']}, so normalized coordinates are x/{BOUNDS['right']} and y/{BOUNDS['bottom']}. Lamp positions are the Light objects L<address>; switch and coil positions are the objects the script binds (see the geometry excerpt), frozen in tools/seeds/bally/paragon-1979-spatial.json.",
		 "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "bord, 32assassin, iaakki, TastyWasps and VPW contributors", "excerpts": excerpt_entries(S_TABLE)},
		{"id": S_CALLOUTS, "kind": "human_review", "uri": "internal:tools/seeds/bally/paragon-1979-callouts.json", "sha256": file_sha256(CALLOUT_SEED_PATH),
		 "locator": "2026-10-16 factory location-drawing callout check of the manual's Figure V (PDF 22, printed 18), switch circles and solenoid squares checked as two pages: every number transcribed independently on gridded tiles of the retained native render, per-page control and callout fits; a table placement whose own callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads and overlays are retained under review-artifacts with a pinned manifest.",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs contributors", "rights": "NOASSERTION"},
		{"id": S_RUNTIME, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_SUMMARY}", "revision": PINMAME_REVISION, "sha256": file_sha256(ROOT / RUNTIME_SUMMARY),
		 "locator": "Pinned LibPinMAME harness runs from empty NVRAM: the solenoid test of paragon, paragonb, paragonc and paragond paired with its displayed numbers, the switch test over all forty matrix addresses, and gameplay and tilt probes of paragon. Raw runs, scenarios and hashes are listed in the summary.",
		 "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	]


# Placements the callout seed excludes from the label check, and how each is decided instead.
FLIPPER_CONTROLS = {
	"device.left-flippers.lower": "LeftFlipper", "device.left-flippers.upper": "LeftFlipper1",
	"device.right-flippers.lower": "RightFlipper", "device.right-flippers.upper": "RightFlipper1",
}
PROJECTIONS = {
	"device.in-line-drop-target-reset.effect": "the centre of the four in-line target walls",
	"device.waterfall-drop-target-reset.effect": "the waterfall bank's middle target",
}
SAME_OBJECT = {
	"switch.outhole.sensor": "device.outhole-kicker.effect",
	"switch.bottom-thumper-bumper.sensor": "device.bottom-thumper-bumper.effect",
	"switch.center-thumper-bumper.sensor": "device.center-thumper-bumper.effect",
	"device.treasure-chamber-saucer-kicker.effect": "switch.treasure-chamber-saucer.sensor",
}


def control_offsets(seed: dict, page: str) -> dict[str, float]:
	controls = seed["pages"][page]["controls"]
	offsets = drawing_callouts.leave_one_out([(tuple(c["pixel"]), tuple(c["xy"])) for c in controls])
	return {c["object"]: offset for c, offset in zip(controls, offsets)}


def decide_excluded(definition: dict, seed: dict, decisions: dict) -> None:
	"""Validate the excluded placements by the route the seed names, or leave them observed."""
	limit = seed.get("limit", drawing_callouts.LIMIT)
	offsets = control_offsets(seed, "figure-v-solenoids")
	points = drawing_callouts.placements_of(definition)
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			notes = []
			for item in (device.get("spatial") or {}).get("placements") or []:
				pid = item["id"]
				if pid not in seed["excluded_checks"]:
					continue
				refs = item["provenance"]["source_refs"]
				if pid in FLIPPER_CONTROLS:
					obj = FLIPPER_CONTROLS[pid]
					control = next(c for c in seed["pages"]["figure-v-solenoids"]["controls"] if c["object"] == obj)
					if tuple(control["xy"]) != (item["x"], item["y"]) or offsets[obj] > limit:
						continue
					notes.append(f"Figure V prints 15 beside, not on, this flipper, so its callout cannot check it; the drawn flipper pivot is a control of the drawing fit, and the fit on the other seven controls puts it {offsets[obj]:.3f} normalized from the table's {obj} pivot, within the {limit} limit.")
				elif pid in PROJECTIONS:
					notes.append(f"The coil is a hidden assembly under its bank; the placement is a documented projection onto {PROJECTIONS[pid]}, which the callout limit exempts.")
				elif pid in SAME_OBJECT:
					other = SAME_OBJECT[pid]
					decision = decisions["placements"].get(other)
					if not decision or not decision["agrees"] or points[other] != (item["x"], item["y"]):
						continue
					notes.append(f"Figure V prints this device's number beside the part, beyond the callout limit; the placement is the same table object as {other}, whose own callout validates it.")
				else:
					continue
				item["provenance"]["status"] = "validated"
				if pid not in PROJECTIONS and S_CALLOUTS not in refs:
					refs.append(S_CALLOUTS)
			if notes:
				physical = device.setdefault("physical", {})
				physical["notes"] = (physical.get("notes", "") + " " + " ".join(notes)).strip()


def build_definition() -> dict:
	definition = _build_definition()
	seed = json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8"))
	decisions = drawing_callouts.apply_to_definition(definition, seed, S_CALLOUTS)
	decide_excluded(definition, seed, decisions)
	unvalidated = [
		item["id"]
		for collection in ("inputs", "outputs") for device in definition[collection]
		for item in (device.get("spatial") or {}).get("placements", []) if item["provenance"]["status"] != "validated"
	]
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			spatial = device.get("spatial")
			if spatial and spatial["status"] != "not_applicable":
				spatial["status"] = "validated" if all(p["provenance"]["status"] == "validated" for p in spatial["placements"]) else "observed"
	if unvalidated:
		definition["coverage"]["status"] = "partial"
		definition["coverage"]["missing"] = ["spatial_placement"]
		definition["coverage"]["dimensions"]["spatial_placement"] = "observed"
		definition["knowledge"]["status"] = "partial"
	return definition


def _build_definition() -> dict:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Paragon", "manufacturer": "Bally", "year": 1979, "kind": "physical_pinball",
			"ipdb_id": 1755, "opdb_id": "GrXy3-ML0Ey",
			"playfield": {"width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx", "provenance": prov("validated", S_TABLE)},
		},
		"coverage": {
			"status": "author_ready",
			"missing": [],
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
				"mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "display_inventory": "validated",
				"spatial_placement": "validated",
			},
		},
		"controller": {"platform": "pinmame.by35", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": all_inputs(),
		"outputs": all_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": sources(),
		"knowledge": {"path": "knowledge/bally/paragon-1979.md", "status": "complete"},
		"conflicts": [],
	}


def build_report(definition: dict) -> tuple[dict, str]:
	seed = json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8"))
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition))
	by_status: dict[str, int] = {}
	not_applicable_counts: dict[str, int] = {}
	unplaced = []
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			spatial = device.get("spatial")
			if spatial is None:
				if device.get("availability") == "used":
					unplaced.append(device["id"])
				continue
			if spatial["status"] == "not_applicable":
				not_applicable_counts[spatial["reason"]] = not_applicable_counts.get(spatial["reason"], 0) + 1
				continue
			for item in spatial["placements"]:
				by_status[item["provenance"]["status"]] = by_status.get(item["provenance"]["status"], 0) + 1
	unvalidated = sorted(
		item["id"]
		for collection in ("inputs", "outputs") for device in definition[collection]
		for item in (device.get("spatial") or {}).get("placements", []) if item["provenance"]["status"] != "validated"
	)
	promoted = definition["coverage"]["status"] == "author_ready"
	report = {
		"format": "pinmame-spatial-audit" if promoted else "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {"space": "playfield", "x": "0=left, 1=right in player view", "y": "0=rear/backglass end, 1=apron end in player view"},
		"coverage": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"]},
		"definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
		"transformation": SEED["transformation"] + " Objects are frozen in tools/seeds/bally/paragon-1979-spatial.json.",
		"source_hashes": {
			"vpx_table_sha256": SEED["table_sha256"],
			"extraction_manifest_sha256": SEED["extraction_manifest_sha256"],
			"spatial_seed_sha256": file_sha256(SPATIAL_SEED_PATH),
			"callout_seed_sha256": file_sha256(CALLOUT_SEED_PATH),
			"manual_sha256": MANUAL_SHA,
			"schematic_sha256": SCHEMATIC_SHA,
		},
		"placement_status_counts": dict(sorted(by_status.items())),
		"not_applicable_counts": dict(sorted(not_applicable_counts.items())),
		"callout_check": {
			"pages": {key: {"locator": seed["pages"][key]["locator"], "image_sha256": seed["pages"][key]["image"]["sha256"]} for key in sorted(seed["pages"])},
			"checked": len(decisions["placements"]),
			"validated": sum(1 for d in decisions["placements"].values() if d["agrees"]),
			"limit": decisions["limit"],
			"excluded": seed["excluded_checks"],
		},
		"lamp_validation": "Every playfield lamp placement is the table light L<address> the script binds by name; each light sits on an insert whose printed art names the lamp's function (value, letter or caption), or, for the four uncaptioned spinner inserts, on the column the factory sheet orders bottom (1) to top (4); the two uncaptioned Treasure Chamber inserts are named by the captions on the plastic beside them.",
		"projection_disclosures": [
			{"devices": ["device.in-line-drop-target-reset"], "class": "hidden assembly projected onto the mean of the four in-line target walls sw1-sw4"},
			{"devices": ["device.waterfall-drop-target-reset"], "class": "hidden assembly projected onto the waterfall bank's middle target sw18"},
			{"devices": ["switch.500-point-rebound", "switch.top-right-golden-cliffs-rollover-button-and-drop-target-rebound"], "class": "parallel contacts on one address, one placement per contact; the rebound rubbers are pieces of the baked collidable primitives sw27a and sw34b"},
			{"devices": ["device.left-flippers", "device.right-flippers"], "class": "two flipper coils per output, one placement per flipper pivot"},
		],
		"unplaced_physical_devices": unplaced,
		"unvalidated_placements": unvalidated,
		"promotion_decision": (
			"Promoted: every placement is validated by the factory drawing's callout check or by the playfield art under the bound light, and no used playfield device is unplaced."
			if promoted else
			"Not promotable: the placements listed as unvalidated did not pass the factory drawing's callout check."
		),
	}
	lines = [
		"# Paragon (Bally 1979) spatial audit",
		"",
		f"Coverage: **{definition['coverage']['status']}**" + (f"; missing {', '.join(f'`{m}`' for m in definition['coverage']['missing'])}." if definition["coverage"]["missing"] else "."),
		"",
		f"The coordinate source is the retained `Paragon (Bally 1979).vpx` (bord v2.37) at SHA-256 `{SEED['table_sha256']}`, bounds `left=0 top=0 right={BOUNDS['right']:g} bottom={BOUNDS['bottom']:g}`, so every coordinate is x/{BOUNDS['right']:g} and y/{BOUNDS['bottom']:g} rounded to six places. "
		"The lower flipper pivots land at y 0.832 and the drain at 0.952.",
		"",
		f"Placements by status: {', '.join(f'{count} {status}' for status, count in sorted(by_status.items()))}. Cabinet, backglass, option-switch and unused devices carry controlled `not_applicable` records ({', '.join(f'{count} {reason}' for reason, count in sorted(not_applicable_counts.items()))}).",
		"",
		"## Evidence decisions",
		"",
		f"- Switch and coil placements are the objects the script binds, checked against the manual's Figure V with `tools/drawing_callouts.py`: {report['callout_check']['validated']} of {report['callout_check']['checked']} checked placements land within 0.07 normalized of their own callout under both the control fit and the leave-one-out callout fit. Figure V prints solenoid self-test numbers in squares and switch numbers in circles, so the two are checked as separate pages of one image.",
		"- Lamp placements are the table lights L<address>. Every one sits on an insert whose art names it (bonus values, the two PARAGON rows, golden-cliff, drop-target and waterlane values, the 2x/3x/5x multipliers, SHOOT AGAIN, the saucer special and the 5X treasure insert); the two uncaptioned Treasure Chamber inserts take the captions printed on the plastic beside them (SPECIAL above EXTRA BALL); the four uncaptioned spinner inserts follow the factory sheet's numbering, 1 at the bottom to 4 at the top, and a fifth insert below them is lit from the table's GI.",
		"- The rebound switches 27 and 34 have parallel contacts; each contact has its own placement, the rubbers being connected pieces of the baked collidable primitives sw27a (two pieces) and sw34b, whose OBJ vertices scaled by the primitive size give world coordinates (checked on the visible baked primitive rubbers_visible against a vpxtool OBJ export).",
		"- Switch 8 and the outhole kicker take the table's Drain kicker, the outhole Figure V marks; the BallRelease kicker in the shooter lane is a table helper.",
		"- The in-line drop-target reset is projected onto the centre of its four targets and the waterfall reset onto its middle target; both coils are hidden assemblies under their banks.",
		"- Backbox lamps 11, 13, 27, 29, 45 and 61, the knocker, the coin lockout, the K1 relay, all cabinet and service switches, the DIPs and the displays take controlled `not_applicable` records.",
		"",
		"## Excluded objects",
		"",
		"- Lights L11, L16, L27 and L29 (members of the table's GI collection in the four star rollovers) and GIxx (the fifth spinner-column insert): general illumination, no lamp output.",
		"- The sw1a-sw4a and sw17a-sw19a secondary drop-target walls and the psw primitives: animation parts of the drop-target system.",
		"- TriggerLF, TriggerRF and TriggerRF1: flipper physics helpers with no switch.",
		"",
	]
	if unvalidated:
		lines += ["## Unvalidated placements", "", *(f"- `{item}`" for item in unvalidated), ""]
	return report, chr(10).join(lines)


def build_knowledge() -> str:
	return KNOWLEDGE_SOURCE_PATH.read_text(encoding="utf-8")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--definition", type=Path, default=None, help="definition path to check or write instead of the one its coverage status names (tests use a copy)")
	parser.add_argument("--knowledge", type=Path, default=KNOWLEDGE_PATH)
	parser.add_argument("--report-json", type=Path, default=REPORT_JSON_PATH)
	parser.add_argument("--report-md", type=Path, default=REPORT_MD_PATH)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="fail on drift; never write")
	mode.add_argument("--regenerate", action="store_true", help="rewrite the artifacts")
	args = parser.parse_args()
	built = build_definition()
	named = AUTHOR_READY_PATH if built["coverage"]["status"] == "author_ready" else PARTIAL_PATH
	stale = PARTIAL_PATH if named == AUTHOR_READY_PATH else AUTHOR_READY_PATH
	target = args.definition or named
	definition = canonical_bytes(built)
	note = build_knowledge().encode("utf-8")
	report, report_md = build_report(built)
	outputs = ((target, definition), (args.knowledge, note), (args.report_json, canonical_bytes(report)), (args.report_md, report_md.encode("utf-8")))
	if args.check:
		drifted = stale.exists()
		if drifted:
			print(f"stale artifact for the other coverage status: {stale}", file=sys.stderr)
		for path, want in outputs:
			if not path.exists() or path.read_bytes() != want:
				print(f"canonical content mismatch: {path}", file=sys.stderr)
				drifted = True
		if drifted:
			return 1
		print("Paragon definition, knowledge note and spatial audit match the deterministic curator.")
		return 0
	if stale.exists():
		stale.unlink()
		print(f"removed {stale.relative_to(ROOT).as_posix()}")
	for path, want in outputs:
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(want)
		print(f"wrote {path.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
