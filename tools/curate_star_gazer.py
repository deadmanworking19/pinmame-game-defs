#!/usr/bin/env python3
"""Deterministic curator for Stern Star Gazer (1980).

Regenerates ``machines/partial/stern/star-gazer-1980.json`` and its knowledge note from the tables
below, so the artifact reproduces byte for byte and drift is detected. ``--check`` refuses drift
and never writes; ``--regenerate`` writes.

The tables are the curated result of the evidence in the priority the runbook sets out: the
retained ROM's own service and gameplay behaviour for runtime semantics and the public-address
translation, the IPDB manual and schematics for physical construction, wiring and the printed
identification numbers, the retained known-working table for runtime bindings and coordinates,
and the pinned PinMAME source for emulator topology. Three facts here look like tidy-ups and are
not; each is argued in ``knowledge/stern/star-gazer-1980.md`` and in the device note it affects:

- the printed solenoid numbers are test-display and driver-position numbers, not public addresses;
- public lamps 24 and 25 reach the transistors the chart prints as Q25 and Q24, not Q24 and Q25;
- the matrix drawing names switches 19 and 20 SCORPIO and LIBRA, the ROM lights the Libra lamp for
  switch 19, and that disagreement stays an open conflict.
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

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "star-gazer-1980.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "star-gazer-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "star-gazer-1980.md"
REPORT_JSON_PATH = ROOT / "reports" / "spatial" / "stern" / "star-gazer-1980.json"
REPORT_MD_PATH = ROOT / "reports" / "spatial" / "stern" / "star-gazer-1980.md"
SPATIAL_SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "star-gazer-1980-spatial.json"
EXCERPT_SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "star-gazer-1980-excerpts.json"
KNOWLEDGE_SOURCE_PATH = ROOT / "tools" / "seeds" / "stern" / "star-gazer-1980-knowledge.md"
RUNTIME_SUMMARY = "evidence/runtime/by35/star-gazer-1980-harness.json"
EXCERPT_DIR = "evidence/excerpts/stern.star-gazer.1980"

MACHINE_ID = "stern.star-gazer.1980"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

S_CATALOG = "pinmame.catalog.8371478a7640"
S_CORE = "pinmame.core.8371478a7640"
S_PROFILE = "controller-profile.pinmame-stern-mpu200"
S_IPDB = "ipdb.2346"
S_MANUAL = "manual.stern.star-gazer.1980"
S_SCHEMATIC = "schematic.stern.star-gazer.1980"
S_LIBRARY = "vpinmame-library.stern-vbs"
S_SCRIPT = "vpx-script.star-gazer.v2-0-0"
S_TABLE = "vpx-table.star-gazer.v2-0-0"
S_RUNTIME = "runtime.star-gazer.harness"
S_CALLOUTS = "drawing-callouts.star-gazer.2026-10-02"
CALLOUT_SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "star-gazer-1980-callouts.json"

SEED = json.loads(SPATIAL_SEED_PATH.read_text(encoding="utf-8"))
OBJECTS = SEED["objects"]
BOUNDS = SEED["bounds"]

sys.path.insert(0, str(ROOT / "tools"))
from star_gazer_spatial_seed import SWITCH_OBJECTS  # noqa: E402
import drawing_callouts  # noqa: E402


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


# ----------------------------------------------------------------------------------------------
# Switches
# ----------------------------------------------------------------------------------------------

STROBES = [("W-R", "A4J2-1"), ("BRN-W", "A4J2-2"), ("W-BLU", "A4J2-3"), ("W-Y", "A4J2-4"), ("Y-R", "A4J2-5")]
RETURNS = [("BRN", "A4J2-8"), ("GREY", "A4J2-9"), ("W-O", "A4J2-10"), ("W-B", "A4J2-11"), ("W-G", "A4J2-12"), ("W-BRN", "A4J2-13"), ("BRN-Y", "A4J2-14"), ("O", "A4J2-15")]
# Switches the matrix drawing prints a capacitor symbol across.
CAPACITOR = {7, 8, 10, 11, 15, 16, 17, 18, 19, 20, 21, 31, 32, 36, 37, 38, 39, 40}

# number -> (label, switch_type, pulse, roles, location, drawn label)
SWITCHES = {
	1: ("Left coin chute", "other", True, ["cabinet.coin-door"], "Coin door, left chute", ""),
	2: ("Center coin chute", "other", True, ["cabinet.coin-door"], "Coin door, center chute", ""),
	3: ("Right coin chute", "other", True, ["cabinet.coin-door"], "Coin door, right chute", ""),
	4: ("Left spinner", "leaf", True, [], "Spinner on the left wall", "(L) SPIN."),
	5: ("Right spinner", "leaf", True, [], "Spinner at the lower end of the right-hand lane", "(R) SPIN."),
	6: ("Credit button", "button", False, ["cabinet.credit-button"], "Coin door", ""),
	7: ("Tilt (ball-roll and plumb-bob pendulum)", "tilt", False, ["cabinet.tilt"], "Cabinet: ball-roll tilt and plumb-bob pendulum tilt", ""),
	8: ("Slam and vibration tilt", "tilt", False, ["cabinet.slam"], "Tilt board, coin door and playfield vibration switch", "SLAM"),
	9: ("Center spinner", "leaf", True, [], "Spinner at the upper-left lane mouth", "(CNTR.) SPIN."),
	10: ("Gemini stand-up target", "leaf", True, [], "Upper-left arch", 'S.U. "GEMINI"'),
	11: ("Cancer stand-up target", "leaf", True, [], "Upper-left arch", 'S.U. "CANCER"'),
	12: ("Left thumper bumper", "leaf", True, [], "Left thumper bumper skirt", "(L) THUMPER"),
	13: ("Right thumper bumper", "leaf", True, [], "Right thumper bumper skirt", "(R) THUMPER"),
	14: ("Center thumper bumper", "leaf", True, [], "Center thumper bumper skirt", "(CNTR) THUMPER"),
	15: ("Right slingshot", "leaf", True, [], "Right slingshot", "(R) SLINGSHOT"),
	16: ("Left slingshot", "leaf", True, [], "Left slingshot", "(L) SLINGSHOT"),
	17: ("Leo stand-up target", "leaf", True, [], "Upper-left arch", 'S.U. "LEO"'),
	18: ("Virgo stand-up target", "leaf", True, [], "Upper-left arch", 'S.U. "VIRGO"'),
	19: ("Libra stand-up target", "leaf", True, [], "Upper-right arch", 'S.U. "SCORPIO"'),
	20: ("Scorpio stand-up target", "leaf", True, [], "Upper-right arch", 'S.U. "LIBRA"'),
	21: ("Sagittarius stand-up target", "leaf", True, [], "Upper-right arch", 'S.U. "SAGITTARIUS"'),
	22: ("Lower-left drop target, bottom", "leaf", False, [], "Left drop-target bank", "BOT.(L) D.T."),
	23: ("Lower-left drop target, middle", "leaf", False, [], "Left drop-target bank", "MID.(L) D.T."),
	24: ("Lower-left drop target, top", "leaf", False, [], "Left drop-target bank", "TOP (L) D.T."),
	25: ("Upper-left drop target, left", "leaf", False, [], "Upper-left drop-target bank", "(L) CNTR. D.T."),
	26: ("Upper-left drop target, middle", "leaf", False, [], "Upper-left drop-target bank", "(M) CNTR. D.T."),
	27: ("Upper-left drop target, right", "leaf", False, [], "Upper-left drop-target bank", "(R) CNTR D.T."),
	28: ("Right drop target, top", "leaf", False, [], "Right drop-target bank", "TOP (R) D.T."),
	29: ("Right drop target, middle", "leaf", False, [], "Right drop-target bank", "MID.(R) D.T."),
	30: ("Right drop target, bottom", "leaf", False, [], "Right drop-target bank", "BOT.(R) D.T."),
	31: ("Capricorn stand-up target", "leaf", True, [], "Right wall of the upper-right arch", 'S.U. "CAPRICORN"'),
	32: ("Aquarius stand-up target", "leaf", True, [], "Right wall of the upper-right arch", 'S.U. "AQUARIUS"'),
	33: ("Outhole", "leaf", False, [], "Outhole between the flipper bays", "OUT HOLE"),
	34: ("Right outlane", "leaf", True, [], "Right outlane", "(R) OUT LANE"),
	35: ("Left outlane", "leaf", True, [], "Left outlane", "(L) OUT LANE"),
	36: ("Right star roll-over button", "leaf", True, [], "Right inlane, above the flipper", "(R) R.O.B."),
	37: ("Left star roll-over button", "leaf", True, [], "Left inlane, above the flipper", "(L) R.O.B."),
	38: ("Pisces stand-up target", "leaf", True, [], "Right wall of the upper-right arch", 'S.U. "PISCES"'),
	39: ("Aries stand-up target", "leaf", True, [], "Lower right wall", 'S.U. "ARIES"'),
	40: ("Taurus stand-up target", "leaf", True, [], "Lower right wall", 'S.U. "TAURUS"'),
}

# Extra provenance and prose per switch.
SWITCH_NOTES = {
	1: "The manual lists 1 as CHUTE (LEFT). The ROM's switch test displays 1 when public 1 is closed and a coin on it posts a credit.",
	2: "The manual lists 2 as CHUTE (CENTER).",
	3: "The manual lists 3 as CHUTE (RIGHT).",
	4: "The manual calls 4 the left spin target and the left spinner. The ROM scores 200 for a closure.",
	5: "The manual calls 5 the right spin target and the right spinner. The ROM scores 200 for a closure.",
	6: "A credit with a ball in the outhole starts the game: the ROM fires the three drop-bank resets and the outhole kicker and raises the flipper-enable relay.",
	7: "The manual's location list gives two contacts for 7, ROLL-TILT and PENDULUM, and its adjustment text names three normally open tilts (plumb bob, ball roll above it, and a panel tilt under the playfield). Closing public 7 in play makes the ROM drop the flipper-enable relay and kills the flippers and bumpers until the ball is served again.",
	8: "The manual lists 8 as SLAM & VIB. TILTS, with the tilt board and the door and playfield vibration contacts on it, and describes a slam switch on the front door and one on the tilt board.",
	9: "The manual calls 9 SPIN TARGET (CENTER); the playfield drawing puts it at the upper-left lane mouth, level with the upper-left drop-target bank, and the table models a spinner there. The ROM scores 200 for a closure, or the lit value shown by the left upper bank.",
	12: "The manual lists 12 as THUMPER (LEFT) and the playfield drawing numbers the top-left bumper 12. A closure makes the ROM fire public coil 5.",
	13: "The manual lists 13 as THUMPER (RIGHT) and the playfield drawing numbers the top-right bumper 13. A closure makes the ROM fire public coil 11.",
	14: "The manual lists 14 as THUMPER (CENTER) and the playfield drawing numbers the lower centre bumper 14. A closure makes the ROM fire public coil 8.",
	15: "The manual lists 15 as RIGHT SLINGSHOT. A closure makes the ROM fire public coil 1; the factory location drawing prints 15 at the right slingshot and prints no number at the left one.",
	16: "The manual lists 16 as LEFT SLINGSHOT. A closure makes the ROM fire public coil 2.",
	19: "OPEN CONFLICT with the printed matrix label. The matrix drawing prints this switch S.U. \"SCORPIO\" and the factory location drawing prints 19 to the right of 20 on the upper-right arch. The ROM lights the Libra lamp (public 2) when this switch closes and scores it as a zodiac target, and the retained table puts it left of switch 20 beside the Libra constellation. The definition follows the ROM for the sign association; see the conflict.",
	20: "OPEN CONFLICT with the printed matrix label. The matrix drawing prints this switch S.U. \"LIBRA\" and the factory location drawing prints 20 at the left end of the upper-right arch. The ROM lights the Scorpio lamp (public 18) when this switch closes and scores it as a zodiac target, and the retained table puts it right of switch 19. The definition follows the ROM for the sign association; see the conflict.",
	33: "The ROM kicks the outhole (public coil 12) while this switch is closed after a credit starts a game and again after a drain. The retained table models the outhole as a kicker beside the shooter lane that feeds the shooter; the manual's drawing numbers 33 at the outhole between the flipper bays, which is where the table's drain kicker sits.",
	34: "The manual lists 34 as RIGHT OUT LANE; the ROM scores 5,000 for a closure.",
	35: "The manual lists 35 as LEFT OUT LANE; the ROM scores 5,000 for a closure.",
	36: "The manual lists 36 as RIGHT ROLL-OVER BUTTON; the factory drawing draws a star on it. The ROM scored 4,000 for the first closure in the retained run (the manual: 2,000, plus spotting a zodiac target worth 1,000 and advancing the bonus 1,000).",
	37: "The manual lists 37 as LEFT ROLL-OVER BUTTON; the factory drawing draws a star on it. The ROM scored 2,000 for the closure in the retained run.",
}

ZODIAC = {10: "Gemini", 11: "Cancer", 17: "Leo", 18: "Virgo", 19: "Libra", 20: "Scorpio", 21: "Sagittarius", 31: "Capricorn", 32: "Aquarius", 38: "Pisces", 39: "Aries", 40: "Taurus"}
# The public lamp each zodiac closure lights in the retained gameplay run.
ZODIAC_LAMP = {10: 1, 11: 17, 17: 33, 18: 49, 19: 2, 20: 18, 21: 34, 31: 50, 32: 3, 38: 19, 39: 35, 40: 51}


def switch_sources(number: int) -> list[str]:
	refs = [S_MANUAL, S_SCHEMATIC, S_RUNTIME]
	if number in {1, 2, 3, 6, 7, 8}:
		refs.append(S_LIBRARY)
	if number in SWITCH_OBJECTS or number == 33:
		refs.extend([S_SCRIPT, S_TABLE])
	if number in {7, 8}:
		refs.append(S_CORE)
	return refs


def matrix_switch(number: int) -> dict:
	label, switch_type, pulse, roles, location, drawn = SWITCHES[number]
	strobe, row = (number - 1) // 8, (number - 1) % 8
	conflicted = number in (19, 20)
	physical: dict = {"switch_type": switch_type, "location": location}
	notes = []
	if number in ZODIAC:
		notes.append(f"Matrix drawing label {drawn}. Closing it in play scores 1,000 and lights the {ZODIAC[number]} lamp (public {ZODIAC_LAMP[number]}) in the retained gameplay run.")
	if number in SWITCH_NOTES:
		notes.append(SWITCH_NOTES[number])
	if number in CAPACITOR:
		notes.append("The matrix drawing prints a capacitor symbol across this switch's contact.")
	if number in range(22, 31):
		notes.append("Held closed while the target is down and released when the bank reset raises it.")
	if notes:
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
		"wiring": {
			"board": "MPU module A4",
			"control_wire": STROBES[strobe][0],
			"control_connection": STROBES[strobe][1],
			"return_wire": RETURNS[row][0],
			"return_connection": RETURNS[row][1],
		},
		"provenance": prov("conflicted" if conflicted else "validated", *switch_sources(number)),
	}
	if roles:
		item["roles"] = roles
	item["spatial"] = switch_spatial(number, roles)
	return item


def switch_spatial(number: int, roles: list[str]) -> dict:
	if roles:
		return not_applicable("cabinet_or_service", S_MANUAL, S_LIBRARY)
	name = SWITCH_OBJECTS[number][1]
	# A table placement is an observation until the factory drawing's callout check promotes it.
	return located("observed", placement(f"switch.{slug(SWITCHES[number][0])}.sensor", "sensor", at(name), "observed", S_TABLE, S_MANUAL))


def service_switch(number: int, label: str, location: str, notes: str) -> dict:
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
		"roles": ["service.diagnostic"] if number != -7 else ["service.self-test"],
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
		item["normally_closed"] = False
		item["pulse"] = False
		item["roles"] = [f"flipper.{side}.button"]
		item["physical"]["notes"] = (
			f"Public {number} is the cabinet flipper button. The ROM publishes the lower flipper callback ({46 if side == 'right' else 48}) only while the flipper-enable relay is raised, "
			"and ignores the button in attract mode. The manual's flipper wiring page draws the button wired to the solenoid driver's flipper circuit, not to the switch matrix."
		)
		item["provenance"] = prov("validated", S_LIBRARY, S_CORE, S_RUNTIME, S_MANUAL)
		item["spatial"] = not_applicable("cabinet_or_service", S_LIBRARY, S_CORE)
	else:
		item["physical"]["notes"] = (
			f"Public {number} is the generic upper-{side} flipper button position that PinMAME declares for every flipper board. Star Gazer has no upper flippers, "
			"and closing it in the retained gameplay run changed nothing."
		)
		item["provenance"] = prov("validated", S_CORE, S_LIBRARY, S_RUNTIME)
		item["spatial"] = not_applicable("unused", S_CORE, S_RUNTIME)
	return item


EOS_NOTE = (
	"Hard-wired contact of the {side} flipper's dual-winding assembly: the manual's flipper wiring page draws it across the hold winding, closed at rest, and "
	"opening at the end of the flipper stroke so only the hold winding stays energized. It is not a PinMAME switch address and the ROM never sees it."
)


def eos_switch(address: int, side: str) -> dict:
	flipper = "LeftFlipper" if side == "left" else "RightFlipper"
	return {
		"id": f"switch.{side}-flipper-end-of-stroke",
		"label": f"{side.title()} flipper end-of-stroke contact",
		"kind": "switch",
		"binding": {"group": "physical.input.direct", "device": address},
		"aliases": aliases(("manual.address", f"{side}-flipper-eos")),
		"normally_closed": True,
		"pulse": False,
		"availability": "used",
		"physical": {"switch_type": "leaf", "location": f"{side.title()} flipper assembly", "notes": EOS_NOTE.format(side=side)},
		"provenance": prov("validated", S_MANUAL, S_SCHEMATIC, S_PROFILE),
		"spatial": located("observed", placement(f"switch.{side}-flipper-end-of-stroke.sensor", "sensor", at(flipper), "observed", S_TABLE, S_MANUAL)),
	}


# Option switches: number -> function as the manual's assignment chart prints it.
DIP_FUNCTIONS = {
	1: "Coin chute #1 credit ratio", 2: "Coin chute #1 credit ratio", 3: "Coin chute #1 credit ratio", 4: "Coin chute #1 credit ratio",
	5: "Flashing value lite speed (ON slow, OFF fast)", 6: "High score feature (ON replay, OFF extra ball)",
	7: "Balls per game (ON 5, OFF 3)", 8: "Background sound (ON off, OFF on)",
	9: "Coin chute #2 credit ratio", 10: "Coin chute #2 credit ratio", 11: "Coin chute #2 credit ratio", 12: "Coin chute #2 credit ratio",
	13: "Add-a-ball memory", 14: "Maximum add-a-balls", 15: "High game to date award (with 16)", 16: "High game to date award (with 15)",
	17: "Extra ball lite control", 18: "Maximum credits (with 19)", 19: "Maximum credits (with 18)", 20: "Credit display",
	21: "Match feature", 22: "Special on complete zodiac (with 24)", 23: "Special alternation", 24: "Special on complete zodiac (with 22)",
	25: "Coin chute #3 credit ratio", 26: "Coin chute #3 credit ratio", 27: "Coin chute #3 credit ratio", 28: "Coin chute #3 credit ratio",
	29: "Bottom banks spot next zodiac target", 30: "Extra ball award", 31: "Special award (with 32)", 32: "Special award (with 31)",
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
			"location": "MPU module, back box",
			"notes": f"Printed function: {DIP_FUNCTIONS[number]}. The assignment chart and the pages after it are transcribed in the DIP excerpt, including three places where the manual's own pages disagree.",
		},
		"provenance": prov("validated", S_MANUAL, S_CORE),
		"spatial": not_applicable("dip_switch", S_MANUAL),
	}


def all_inputs() -> list[dict]:
	items = [
		service_switch(-7, "Self-test button", "Inside the coin door", "The manual's self-test button: five presses step through the burn-in, lamp, display, solenoid and switch tests, and later presses step through the bookkeeping pages."),
		service_switch(-6, "CPU diagnostic button", "MPU module", "Named swCPUDiag in the retained Stern VPinMAME library; the manual does not describe this input."),
		service_switch(-5, "Sound diagnostic button", "Sound module", "Named swSoundDiag in the retained Stern VPinMAME library; the manual does not describe this input."),
	]
	items.extend(matrix_switch(number) for number in range(1, 41))
	items.extend([
		flipper_button(81, "Upper-right flipper button position", "unused", "right"),
		flipper_button(82, "Lower-right flipper button", "used", "right"),
		flipper_button(83, "Upper-left flipper button position", "unused", "left"),
		flipper_button(84, "Lower-left flipper button", "used", "left"),
	])
	items.extend(dip_switch(number) for number in range(1, 33))
	items.extend([eos_switch(1, "left"), eos_switch(2, "right")])
	return items


# ----------------------------------------------------------------------------------------------
# Solenoids
# ----------------------------------------------------------------------------------------------

# public -> printed test number, label, kind, driver, wire, connection, part, availability, placement, role, notes
COILS = {
	1: (2, "Right slingshot", "coil", "G-BLU", "A3J2-4", "J-26-1200", "used", "RightSlingshot", None,
		"Fired by switch 15. The manual's test list calls its position 2, RIGHT SLING-SHOT."),
	2: (1, "Left slingshot", "coil", "G-O", "A3J2-9", "J-26-1200", "used", "LeftSlingshot", None,
		"Fired by switch 16. The manual's test list calls its position 1, LEFT SLING-SHOT."),
	3: (5, "Upper-left drop bank reset", "coil", "G-Y", "A3J2-10", "B-27-2300", "used", "sw26", None,
		"Resets drop targets 25, 26 and 27 (the retained ROM fires it when that bank is completed and when a credit starts a game). The manual's list calls its position 5, TOP DROP BANK, and the schematic TOP DROP TARGET. It is placed on the bank's middle target because the coil is a hidden assembly behind the bank."),
	4: (6, "Right drop bank reset", "coil", "G-R", "A3J2-11", "B-27-2300", "used", "sw29", None,
		"Resets drop targets 28, 29 and 30. The manual's list calls its position 6, RIGHT DROP BANK. It is placed on the bank's middle target because the coil is a hidden assembly behind the bank."),
	5: (7, "Left thumper bumper", "coil", "R-Y", "A3J2-12", "J-26-1200", "used", "Bumper1", None,
		"Fired by switch 12. The manual's test list calls its position 7, LEFT THUMPER."),
	6: (3, "Knocker", "coil", "B-Y", "A3J2-5", "N-26-1200", "used", None, "cabinet.knocker",
		"The manual's solenoid drawing lists the knocker among the solenoids not on the playfield. The retained ROM never fired it in the gameplay probes; its address follows from the burn-in test order and the table's SolCallback(6)."),
	7: (4, "Left drop bank reset", "coil", "B-BLU", "A3J1-5", "B-27-2300", "used", "sw23", None,
		"Resets drop targets 22, 23 and 24. The manual's list calls its position 4, LEFT DROP TARGET. The playfield sheet draws it on connector A3J1 pin 5, and the solenoid sheet shows pins 5, 2 and 3 of J1 on it. It is placed on the bank's middle target because the coil is a hidden assembly behind the bank."),
	8: (8, "Center thumper bumper", "coil", "B-O", "A3J5-10", "J-26-1200", "used", "Bumper3", None,
		"Fired by switch 14. The manual's test list calls its position 8, MIDDLE THUMPER."),
	9: (13, "Unused momentary output 13", "coil", None, None, None, "unused", None, None, ""),
	10: (14, "Unused momentary output 14", "coil", None, None, None, "unused", None, None, ""),
	11: (9, "Right thumper bumper", "coil", "R-BLU", "A3J5-9", "J-26-1200", "used", "Bumper2", None,
		"Fired by switch 13. The manual's test list calls its position 9, RIGHT THUMPER."),
	12: (10, "Outhole kicker", "coil", "O-W", "A3J5-15", "JX-26-1200", "used", "Drain", "internal.trough",
		"Kicks the ball from the outhole to the shooter lane. The ROM fires it while switch 33 is closed after a credit starts a game and again after a drain."),
	13: (12, "Unused momentary output 12", "coil", None, None, None, "unused", None, None, ""),
	14: (11, "Unused momentary output 11", "coil", None, None, None, "unused", None, None, ""),
	15: (16, "Unused momentary output 16", "coil", None, None, None, "unused", None, None, ""),
	17: (17, "Unused continuous output 17", "relay", None, "J5 pin 7", None, "unused", None, None, ""),
	18: (19, "Coin lockout coil", "coil", "Y-W", "A3J2-8", "C-36-5300", "used", None, "cabinet.coin-door",
		"The ROM holds it energized from power-up (attract mode and game over); the manual says the coin lock-out coil is energized when the game is ready for play."),
	19: (15, "Flipper enable relay", "relay", "Y-W", "A3J3-5", None, "used", None, "cabinet.relay",
		"Raised by the ROM from a credit's game start until game over and dropped by a tilt; the lower flippers do nothing while it is down. The manual's solenoid list prints this position as ENABLE REPLAY, the schematic names the load wired to the position the flipper enable relay, and the schematic draws the relay's supply as 43 VDC through A2J3-8; the printed words disagree and the flipper behaviour is the ROM's."),
	20: (18, "Unused continuous output 18", "relay", None, "A3J2-15", None, "unused", None, None, ""),
}


def coil_output(address: int) -> dict:
	test, label, kind, wire, connection, part, availability, obj, role, notes = COILS[address]
	device_id = f"device.{slug(label)}"
	physical: dict = {"location": label}
	if part:
		physical["part_number"] = part
	text = f"Printed self-test number {test:02d}, which is also the driver transistor position Q{test}; the printed number is a test order and a driver position, not a public address, and the retained ROM pairs it with this public address."
	if availability == "unused":
		text += " The manual's solenoid list prints this position OPEN and the parts list names no coil for it, and the burn-in test fires it as part of its sweep of every driver."
		if address == 20:
			text += " The solenoid sheet labels the Q18 load BALL KICKER (R-W) on connector J2 pin 15, but the manual calls the position OPEN and the parts list has no ball-kicker coil."
		if address == 17:
			text += " The solenoid sheet draws the Q17 load as an unlabeled box on connector J5 pin 7."
	if notes:
		text += " " + notes
	physical["notes"] = text
	wiring = {
		"board": "Solenoid Driver / Voltage Regulator module SDU A3",
		"driver_transistor": f"Q{test}",
		"nominal_voltage_v": 43,
		"voltage_type": "dc",
	}
	if wire:
		wiring["drive_wire"] = wire
	if connection:
		wiring["drive_connection"] = connection
	if availability == "unused":
		sources = (S_MANUAL, S_SCHEMATIC, S_RUNTIME)
	else:
		sources = (S_MANUAL, S_SCHEMATIC, S_RUNTIME, S_SCRIPT) if address in (3, 4, 6, 7, 12, 19) else (S_MANUAL, S_SCHEMATIC, S_RUNTIME)
	item = {
		"id": device_id,
		"label": label,
		"kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.solenoid", address), ("manual.self-test", test)),
		"availability": availability,
		"physical": physical,
		"wiring": wiring,
		"provenance": prov("validated", *sources),
	}
	if role:
		item["roles"] = [role]
	if availability == "unused":
		item["spatial"] = not_applicable("unused", S_MANUAL, S_RUNTIME)
	elif obj is None:
		item["spatial"] = not_applicable("cabinet_or_service", S_MANUAL)
	else:
		item["spatial"] = located("observed", placement(f"{device_id}.effect", "effect", at(obj), "observed", S_TABLE, S_MANUAL))
	return item


def flipper_output(address: int, side: str) -> dict:
	flipper = "LeftFlipper" if side == "left" else "RightFlipper"
	wire, connection = ("G", "A3J1-8") if side == "left" else ("O", "A3J1-9")
	button_wire, button_connection = ("BLU", "A3J2-2") if side == "left" else ("R", "A3J2-1")
	return {
		"id": f"device.{side}-flipper",
		"label": f"{side.title()} lower flipper dual-winding coil",
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.solenoid", address), ("manual.address", f"{side}-flipper")),
		"availability": "used",
		"physical": {
			"part_number": "J-25-475/34-4500",
			"location": f"{side.title()} flipper assembly",
			"notes": (
				f"The lower flippers are hard-wired dual-winding circuits (a J-25-475/34-4500 assembly each) gated by the flipper enable relay (public 19). PinMAME publishes the generic lower-{side} flipper callback at {address} "
				f"while the {side} button is held with the relay raised, and also sets {address - 1} (PinMAME's sL{'L' if side == 'left' else 'R'}FlipPow bit) in the same press; PinMAME fabricates both bits together for a cabinet-wired flipper, "
				f"only {address} is an addressable output in the controller profile, and which physical winding {address - 1} stands for is not settled by any source here."
			),
		},
		"wiring": {
			"board": "Hard-wired flipper circuit gated by output 19",
			"power_wire": "BLU-W",
			"power_connection": "A2J1-6",
			"drive_wire": wire,
			"drive_connection": connection,
			"control_wire": button_wire,
			"control_connection": button_connection,
			"nominal_voltage_v": 43,
			"voltage_type": "dc",
		},
		"provenance": prov("validated", S_MANUAL, S_SCHEMATIC, S_SCRIPT, S_CORE, S_RUNTIME),
		"spatial": located("observed", placement(f"device.{side}-flipper.effect", "effect", at(flipper), "observed", S_TABLE, S_MANUAL)),
	}


# ----------------------------------------------------------------------------------------------
# Lamps
# ----------------------------------------------------------------------------------------------

# Printed chart rows: (description, wire, jack, pin, transistor number, marked MCR106-1)
CHART = [
	("AQUARIUS", "PUR", "J1", 17, 13, False), ("ARIES", "B-R", "J3", 19, 44, False),
	("BONUS 1K", "BLU-W", "J1", 23, 8, True), ("BONUS 2K", "R-G", "J1", 3, 35, True), ("BONUS 3K", "Y-BLU", "J3", 17, 49, True),
	("BONUS 4K", "W-BLU", "J3", 11, 54, True), ("BONUS 5K", "GREY-O", "J1", 14, 9, True), ("BONUS 6K", "PUR-W", "J1", 2, 34, True),
	("BONUS 7K", "R-B", "J3", 16, 48, True), ("BONUS 8K", "O", "J3", 9, 55, True), ("BONUS 9K", "GREY-Y", "J1", 15, 10, True),
	("BONUS 10K", "GREY-BLU", "J1", 10, 22, True), ("BONUS 11K", "W", "J3", 23, 37, True), ("BONUS 12K", "G", "J3", 3, 60, True),
	("BONUS 12,000", "PUR", "J2", 8, 23, True), ("BONUS 24,000", "GREY", "J2", 9, 40, True),
	("CANCER", "BLU-R", "J1", 1, 29, False), ("CAPRICORN", "G-R", "J3", 12, 50, False), ("GAME OVER", "O-G", "J2", 11, 33, True),
	("GEMINI", "BRN-B", "J1", 18, 14, True), ("HIGH SCORE TO DATE", "GREY-O", "J2", 22, 16, True), ("L. BANK", "G", "J2", 16, 5, True),
	("L. B 1", "BLU", "J2", 15, 19, False), ("L. B 3 STAR ROLL", "B", "J2", 2, 31, False), ("L. B 3 STAR ROLL-OVER", "B-G", "J3", 21, 42, True),
	("L OUT L", "BLU-W", "J2", 7, 43, False), ("L. R B 4 STAR ROLL-OVER", "GREY-B", "J3", 10, 56, True), ("L. SPINNER LITE", "B-Y", "J2", 5, 52, False),
	("L. 3 FROM TOP STAR ROLL-OVER", "BLU-O", "J1", 5, 27, False), ("LEO", "B", "J3", 26, 36, False), ("LIBRA", "GREY-G", "J1", 19, 12, False),
	("MATCH", "GREY-Y", "J2", 1, 45, False), ("PISCES", "G-B", "J1", 8, 28, False), ("R. BANK L", "G-O", "J2", 20, 18, False),
	("R. OUT L", "Y", "J2", 6, 30, False), ("R. SPINNER", "W", "J2", 23, 15, True), ("SAGITTARIUS", "R-Y", "J3", 25, 38, False),
	("SCORPIO", "GREY", "J1", 9, 27, False), ("SHOOT AGAIN", "GREY-R", "J1", 26, 3, True), ("SHOOT AGAIN", "GREY-R", "J2", 21, 3, True),
	("SPINNER & BANK 500", "B", "J1", 16, 11, False), ("SPINNER & BANK 1000", "Y-G", "J1", 7, 26, False),
	("SPINNER & BANK 1500", "O-W", "J3", 27, 32, False), ("SPINNER & BANK 2000", "R-W", "J3", 4, 59, False),
	("SPINNER & BANK 2500", "B-W", "J1", 28, 4, False), ("SPINNER & BANK 3000", "BRN-R", "J1", 6, 25, False),
	("SPINNER & BANK 3500", "W-BLU", "J1", 13, 20, False), ("SPINNER & BANK 4000", "Y-BLU", "J3", 2, 58, False),
	("STAR ROLL-OVER BOTTOM", "BRN-BLU", "J1", 24, 1, True), ("TAURUS", "W-B", "J3", 15, 51, False), ("TILT", "GREY-B", "J2", 10, 47, True),
	("VIRGO", "R-G", "J3", 1, 57, False), ("ZODIAC TARGET 1000", "PUR-B", "J1", 25, 2, True), ("ZODIAC TARGET 2000", "B-O", "J1", 11, 17, True),
	("ZODIAC TARGET 3000", "G-B", "J3", 20, 41, True), ("ZODIAC TARGET 4000", "R-BLU", "J3", 18, 46, False),
	("1 X", "GREY-G", "J2", 13, 7, False), ("2 X", "W-Y", "J2", 12, 21, False), ("3 X", "PUR-B", "J2", 4, 39, False), ("4 X", "B-W", "J2", 3, 53, False),
]

# The chart prints Q27 on the "L. 3 FROM TOP" row; the lamp-driver schematic draws J1 pin 5 at Q24.
CHART_TRANSISTOR_CORRECTION = {("L. 3 FROM TOP STAR ROLL-OVER", "J1", 5): 24}

# Public lamp -> transistor. Fifty-eight of the sixty follow the LDA board's decoder order shared by
# every Stern MPU-200 machine; public 24 and 25 are the pair this machine's ROM and chart show
# transposed relative to that order (the ROM's vari-value sweep puts 3000 at public 24).
PUBLIC_LAMP_Q = {
	1: 14, 2: 12, 3: 13, 4: 8, 5: 9, 6: 10, 7: 11, 8: 4, 9: 1, 10: 2, 11: 3, 12: 7, 13: 16, 14: 5, 15: 6,
	17: 29, 18: 27, 19: 28, 20: 35, 21: 34, 22: 22, 23: 26, 24: 25, 25: 24, 26: 17, 27: 23, 28: 21, 29: 15, 30: 18, 31: 19,
	33: 36, 34: 38, 35: 44, 36: 49, 37: 48, 38: 37, 39: 32, 40: 20, 41: 42, 42: 46, 43: 40, 44: 39, 45: 33, 46: 30, 47: 31,
	49: 57, 50: 50, 51: 51, 52: 54, 53: 55, 54: 60, 55: 59, 56: 58, 57: 56, 58: 41, 59: 52, 60: 53, 61: 47, 62: 43, 63: 45,
}

BACKBOX_LAMPS = {13: "High score to date", 45: "Game over", 61: "Tilt", 63: "Match"}
# Lamps whose socket the playfield art itself identifies: the twelve signs (constellation drawings), the eight
# spinner-and-bank values (printed 500 to 4000) and the two lites the art captions (extra ball, special). Every other
# placed lamp rests on the table's light-to-lamp-number binding alone, which a pixel test on same-sized insert holes
# cannot tell apart, so it stays observed.
ART_IDENTIFIED_LAMPS = {1, 2, 3, 17, 18, 19, 33, 34, 35, 49, 50, 51, 7, 8, 23, 24, 39, 40, 55, 56, 14, 30}
SECOND_BULB = {9: "l90", 25: "l250", 41: "l410", 57: "l570"}
# Lamps the retained table binds by TimerInterval; 31, 47 have no light and 13, 45, 61, 63 drive backglass reels.
UNPLACED = {31, 47}

LAMP_LABELS = {
	1: "Gemini", 2: "Libra", 3: "Aquarius", 4: "Bonus 1K", 5: "Bonus 5K", 6: "Bonus 9K", 7: "Spinner and bank 500", 8: "Spinner and bank 2500",
	9: "Star roll-over bottom", 10: "Zodiac target 1000", 11: "Shoot again", 12: "Bonus multiplier 1X", 13: "High score to date", 14: "Left bank lite",
	15: "Unused lamp-driver output Q6", 17: "Cancer", 18: "Scorpio", 19: "Pisces", 20: "Bonus 2K", 21: "Bonus 6K", 22: "Bonus 10K",
	23: "Spinner and bank 1000", 24: "Spinner and bank 3000", 25: "Left 3 from top star roll-over", 26: "Zodiac target 2000", 27: "Bonus 12,000",
	28: "Bonus multiplier 2X", 29: "Right spinner lite", 30: "Right bank lite", 31: "Left B 1 lamp", 33: "Leo", 34: "Sagittarius", 35: "Aries",
	36: "Bonus 3K", 37: "Bonus 7K", 38: "Bonus 11K", 39: "Spinner and bank 1500", 40: "Spinner and bank 3500", 41: "Left B 3 star roll-over",
	42: "Zodiac target 4000", 43: "Bonus 24,000", 44: "Bonus multiplier 3X", 45: "Game over", 46: "Right outlane lite", 47: "Left B 3 star roll lamp",
	49: "Virgo", 50: "Capricorn", 51: "Taurus", 52: "Bonus 4K", 53: "Bonus 8K", 54: "Bonus 12K", 55: "Spinner and bank 2000", 56: "Spinner and bank 4000",
	57: "Left right B 4 star roll-over", 58: "Zodiac target 3000", 59: "Left spinner lite", 60: "Bonus multiplier 4X", 61: "Tilt", 62: "Left outlane lite", 63: "Match",
}
LAMP_WHERE = {
	"sign": "playfield insert beside the {name} constellation art",
	"bonus": "bonus star insert at the centre of the playfield",
	"spinner": "spinner and bank value chart in the red banner left of centre",
	"zodiac": "zodiac target value column at the upper centre, beside the raven art",
	"multiplier": "bonus multiplier column in the lower centre",
	"lane": "star roll-over lane arrow in the left and right lower lanes",
}


# The page-4 lamp-driver diagram marks MCR106-1 positions with a triangle and the chart marks them with an
# asterisk; they disagree on these two rows (Q14 and Q24, as read on the J1 block). The structured driver type follows the chart where the row is
# unambiguous and is omitted where the corrected row is the only reading.
TRIANGLE_NOTES = {
	1: "The chart marks Q14 with an asterisk (MCR106-1); the page-4 lamp-driver diagram draws no triangle at pin J1-18. The chart's type is recorded.",
	25: "The transistor type is not recorded: the chart row prints no asterisk (2N5060) under its misprinted Q27, while the page-4 diagram draws Q24 with a triangle (MCR106-1) and labels it MCR106-1.",
}

LAMP_SPECIAL_WHERE = {
	14: "insert on the lower-left drop bank marked CENTER TARGET SCORES EXTRA BALL WHEN LIT",
	29: "insert beside the right spinner",
	30: "insert on the right drop bank marked ALL TARGETS DOWN SCORES SPECIAL WHEN LIT",
	46: "right outlane insert",
	59: "insert beside the left spinner",
	62: "left outlane insert",
}


def lamp_kind(public: int) -> str:
	if public in (1, 2, 3, 17, 18, 19, 33, 34, 35, 49, 50, 51):
		return "sign"
	if public in (4, 5, 6, 20, 21, 22, 27, 36, 37, 38, 43, 52, 53, 54):
		return "bonus"
	if public in (7, 8, 23, 24, 39, 40, 55, 56):
		return "spinner"
	if public in (10, 26, 42, 58):
		return "zodiac"
	if public in (12, 28, 44, 60):
		return "multiplier"
	if public in (9, 25, 41, 57):
		return "lane"
	return ""


def chart_rows(public: int) -> list[tuple[str, str, int, int, bool]]:
	q = PUBLIC_LAMP_Q[public]
	rows = []
	for description, wire, jack, pin, printed, mcr in CHART:
		real = CHART_TRANSISTOR_CORRECTION.get((description, jack, pin), printed)
		if real == q:
			rows.append((wire, jack, pin, printed, mcr))
	return rows


SIGN_NAMES = {1: "Gemini", 2: "Libra", 3: "Aquarius", 17: "Cancer", 18: "Scorpio", 19: "Pisces", 33: "Leo", 34: "Sagittarius", 35: "Aries", 49: "Virgo", 50: "Capricorn", 51: "Taurus"}
RUNTIME_LAMPS = set(SIGN_NAMES) | {7, 23, 39, 55, 8, 24, 40, 56, 11, 13, 45, 61, 63, 9, 25, 41, 57, 31, 47}


def lamp_output(public: int) -> dict:
	label = LAMP_LABELS[public]
	q = PUBLIC_LAMP_Q[public]
	device_id = f"lamp.{slug(label)}"
	rows = chart_rows(public)
	aliases_ = aliases(("pinmame.lamp", public), ("manual.address", f"Q{q}"))
	if public == 15:
		return {
			"id": device_id,
			"label": label,
			"kind": "lamp",
			"binding": {"group": "pinmame.output.lamp", "device": public},
			"aliases": aliases_,
			"availability": "unused",
			"physical": {"location": "none", "notes": "The lamp-driver chart prints sixty rows and no row for Q6, the lamp-driver schematic draws J2 pin 14 at Q6 with nothing named, the retained table binds no light to public 15, and the retained ROM drives it only while its lamp test sweeps every output."},
			"wiring": {"board": "Lamp Driver module LDA-100 (parts list B-431)", "driver_transistor": "Q6", "drive_connection": "LDA J2-14"},
			"provenance": prov("validated", S_SCHEMATIC, S_SCRIPT, S_RUNTIME),
			"spatial": not_applicable("unused", S_SCHEMATIC, S_RUNTIME),
		}
	wire, jack, pin, printed, mcr = rows[0]
	connections = [f"LDA {j}-{p}" for _, j, p, _, _ in rows]
	scr = "MCR106-1" if mcr else "2N5060"
	notes = [f"Chart row {', '.join(repr(d) for d, w, j, p, t, m in CHART if (CHART_TRANSISTOR_CORRECTION.get((d, j, p), t)) == q)} on transistor Q{q}{'' if public == 25 else f' ({scr})'}, connector {', '.join(connections)}, wire {wire}."]
	kind = lamp_kind(public)
	physical: dict = {"location": ""}
	if public in BACKBOX_LAMPS:
		physical["location"] = "backglass"
		notes.append("Backglass lamp: the retained table drives a backglass reel from it and no playfield insert, and the manual calls it a feature lite of the back box.")
	elif public in UNPLACED:
		physical["location"] = "unknown"
		notes.append(
			"No retained source places this lamp. The chart lists it as a circuit, the table binds no light to it, and the retained ROM drives it in lockstep with public "
			f"{9 if public == 31 else 41} in play. Whether it is the opposite-side bulb of that lane arrow or something else is not settled, so it carries no placement."
		)
	elif public == 11:
		physical["location"] = "playfield insert and backglass"
		notes.append("One SCR reaches two connector pins (the chart lists J1-26 and J2-21 on Q3), which the retained table treats as a playfield insert and a backglass Shoot Again reel it reads from this lamp. The chart gives no bulb counts, so no quantity is stated and only the playfield light carries a placement.")
	else:
		where = LAMP_WHERE[kind] if kind else LAMP_SPECIAL_WHERE[public]
		physical["location"] = where.format(name=SIGN_NAMES.get(public, ""))
		if public in SECOND_BULB:
			notes.append("The retained table lights a second bulb with the same lamp number in the opposite lane, and the art draws the arrow in both lanes; the chart gives no bulb counts and circuits 31 and 47 may be further lane bulbs, so both lights are kept as observed placements and no quantity is stated.")
	if public == 24:
		notes.append("The printed chart gives the 3000 row Q25 and connector pin J1-6. The retained ROM sweeps the eight spinner and bank value lamps 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000 as public 7, 23, 39, 55, 8, 24, 40, 56, so public 24 is the 3000 lamp; this makes public 24 reach Q25 and public 25 reach Q24, the opposite pairing to the board order.")
	if public == 25:
		notes.append("The printed chart gives this row Q27, the transistor it also gives SCORPIO; the lamp-driver schematic draws connector pin J1-5 at Q24 and the pin below it, J1-6, at Q25. The row is read as Q24, which the ROM sweep agrees with, since public 25 is not one of the eight value lamps and blinks with the lane arrows.")
	if public in SIGN_NAMES:
		switch_no = [n for n, p in ZODIAC_LAMP.items() if p == public][0]
		notes.append(f"Closing switch {switch_no} in play lights this lamp in the retained gameplay run.")
	if public in TRIANGLE_NOTES:
		notes.append(TRIANGLE_NOTES[public])
	if public == 46:
		notes.append("The chart's second copy on schematic PDF page 4 prints the pin of this row as a bold glyph that reads 5, where the copy on page 2 prints 6; the lamp-driver schematic on page 4 draws pin 6 at Q30, so pin 6 is recorded (a wiring-detail disagreement between two copies of one table).")
	if public in (2, 18):
		notes.append("This is the end of the open conflict about stand-up switches 19 and 20: the lamp is where the playfield art draws its sign, and the ROM pairs it with the other switch from the one the matrix drawing implies.")
	physical["notes"] = " ".join(notes)
	wiring = {
		"board": "Lamp Driver module LDA-100 (parts list B-431)",
		"driver_transistor": f"Q{q}" if public == 25 else f"Q{q} ({scr})",
		"drive_wire": wire,
		"drive_connection": ", ".join(connections),
	}
	sources = [S_SCHEMATIC, S_SCRIPT, S_TABLE]
	if public in RUNTIME_LAMPS:
		sources.append(S_RUNTIME)
	item = {
		"id": device_id,
		"label": label,
		"kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": public},
		"aliases": aliases_,
		"availability": "used",
		"physical": physical,
		"wiring": wiring,
	}
	if public in BACKBOX_LAMPS:
		item["roles"] = ["cabinet.backglass"]
		item["provenance"] = prov("validated", S_SCHEMATIC, S_SCRIPT, S_RUNTIME, S_MANUAL)
		item["spatial"] = not_applicable("cabinet_or_service", S_SCRIPT, S_MANUAL)
		return item
	if public in UNPLACED:
		item["provenance"] = prov("observed", S_SCHEMATIC, S_RUNTIME)
		return item
	item["provenance"] = prov("validated", *sources)
	status = "validated" if public in ART_IDENTIFIED_LAMPS else "observed"
	points = [placement(f"{device_id}.emitter-1", "emitter", at(f"l{public}"), status, S_TABLE, S_SCHEMATIC)]
	if public in SECOND_BULB:
		points.append(placement(f"{device_id}.emitter-2", "emitter", at(SECOND_BULB[public]), status, S_TABLE, S_SCHEMATIC))
	item["spatial"] = located(status, *points)
	return item


def all_outputs() -> list[dict]:
	items = [coil_output(address) for address in sorted(COILS)]
	items.extend([flipper_output(46, "right"), flipper_output(48, "left")])
	items.extend(lamp_output(public) for public in sorted(PUBLIC_LAMP_Q))
	items.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return items


# ----------------------------------------------------------------------------------------------
# Mechanisms, relationships, displays, sources
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
			"mechanism.outhole", "Outhole and manual shooter feed", "kicker", ["device.outhole-kicker"], [sid(33)],
			"Star Gazer is a one-ball game with no trough: the ball drains into the outhole between the flipper bays, closing switch 33, and the outhole kicker (public 12) kicks it to the shooter lane, where the player launches it with the plunger. "
			"The ROM scores the bonus when switch 33 closes, then kicks the ball; after a credit starts a game it kicks the ball waiting in the outhole at once, and the three drop banks are reset in the same step. "
			"The retained table models the outhole as a drain hole feeding a release kicker beside the shooter lane, kicked at about 57 degrees with force 10.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="JX-26-1200"),
		mechanism(
			"mechanism.lower-left-drop-bank", "Lower-left three-bank drop targets", "drop_target_bank", ["device.left-drop-bank-reset"], [sid(22), sid(23), sid(24)],
			"Three drop targets, bottom to top switches 22, 23 and 24, each held closed while its target is down. One shared reset coil (public 7) raises all three. Completing the bank advances the bonus multiplier (to 10x), and the middle target scores the extra ball when its lite is on. "
			"The retained ROM fires the reset after the bank is completed and at game start.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="B-27-2300"),
		mechanism(
			"mechanism.upper-left-drop-bank", "Upper-left three-bank drop targets", "drop_target_bank", ["device.upper-left-drop-bank-reset"], [sid(25), sid(26), sid(27)],
			"Three drop targets, left to right switches 25, 26 and 27, held closed while down, with one shared reset coil (public 3). Hitting one target stops the flashing value lite at its value and fixes the center spinner's value; hitting all three awards points. The manual calls this bank the left upper bank.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="B-27-2300"),
		mechanism(
			"mechanism.right-drop-bank", "Right three-bank drop targets", "drop_target_bank", ["device.right-drop-bank-reset"], [sid(28), sid(29), sid(30)],
			"Three drop targets, top to bottom switches 28, 29 and 30, held closed while down, with one shared reset coil (public 4). Completing the bank advances the bonus multiplier and, while the red special lite is lit, awards the special.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="B-27-2300"),
		mechanism(
			"mechanism.thumper-bumpers", "Three thumper bumpers", "other", ["device.left-thumper-bumper", "device.right-thumper-bumper", "device.center-thumper-bumper"], [sid(12), sid(13), sid(14)],
			"Each bumper's skirt switch makes the ROM fire its own coil: switch 12 fires public 5, switch 13 public 11 and switch 14 public 8, each scoring 1,000. The pairing is the ROM's, observed with one closure at a time.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="J-26-1200"),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], [sid(16), sid(15)],
			"Switch 16 makes the ROM fire public coil 2 (the left slingshot, printed test number 1) and switch 15 public coil 1 (the right, printed number 2); each scores 10 points. The reversed-looking numbering is the ROM's own and was confirmed by closing each switch alone.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="J-26-1200"),
		mechanism(
			"mechanism.spinners", "Three spinners", "other", [], [sid(4), sid(5), sid(9)],
			"The left spinner (switch 4), the right spinner (switch 5) and the center spinner (switch 9, at the upper-left lane mouth) each close their switch once per rotation and score 200, or 2,000 when lit; the center spinner scores the value the upper-left bank has locked in.",
			S_MANUAL, S_SCRIPT, S_RUNTIME),
		mechanism(
			"mechanism.flippers", "Two lower dual-winding flippers", "other", ["device.left-flipper", "device.right-flipper", "device.flipper-enable-relay"],
			["switch.lower-left-flipper-button", "switch.lower-right-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-end-of-stroke"],
			"The flipper enable relay (public 19) gates both hard-wired 43 V flipper circuits: it is raised from a credit's game start until game over, dropped by a tilt and raised again when the next ball is served, and the lower buttons (82 right, 84 left) do nothing in attract mode. "
			"Each J-25-475/34-4500 assembly's normally closed end-of-stroke contact opens at the end of the stroke so only the hold winding stays energized.",
			S_MANUAL, S_SCHEMATIC, S_SCRIPT, S_RUNTIME, S_CORE, part="J-25-475/34-4500"),
	]


def relationships() -> list[dict]:
	items = [
		("rel.right-slingshot", "direct", sid(15), "device.right-slingshot", (S_MANUAL, S_RUNTIME)),
		("rel.left-slingshot", "direct", sid(16), "device.left-slingshot", (S_MANUAL, S_RUNTIME)),
		("rel.left-thumper-bumper", "direct", sid(12), "device.left-thumper-bumper", (S_MANUAL, S_RUNTIME)),
		("rel.right-thumper-bumper", "direct", sid(13), "device.right-thumper-bumper", (S_MANUAL, S_RUNTIME)),
		("rel.center-thumper-bumper", "direct", sid(14), "device.center-thumper-bumper", (S_MANUAL, S_RUNTIME)),
		("rel.outhole", "pulse", sid(33), "device.outhole-kicker", (S_MANUAL, S_RUNTIME)),
		("rel.left-flipper", "relay_gated", "switch.lower-left-flipper-button", "device.left-flipper", (S_MANUAL, S_SCHEMATIC, S_RUNTIME)),
		("rel.right-flipper", "relay_gated", "switch.lower-right-flipper-button", "device.right-flipper", (S_MANUAL, S_SCHEMATIC, S_RUNTIME)),
	]
	return [{"id": rid, "kind": kind, "source": source, "destination": destination, "provenance": prov("validated", *refs)} for rid, kind, source, destination, refs in items]


def displays() -> list[dict]:
	refs = (S_CORE, S_MANUAL, S_RUNTIME)
	items = []
	for number, start in enumerate((1, 9, 17, 25), start=1):
		items.append({
			"id": f"display.player-{number}-score", "label": f"Player {number} score, seven digits", "kind": "segment",
			"controller_index": number - 1, "segment_start": start, "width": 7,
			"provenance": prov("validated", *refs), "spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
		})
	items.append({
		"id": "display.credits", "label": "Credits, two digits", "kind": "segment", "controller_index": 4, "segment_start": 35, "width": 2,
		"provenance": prov("validated", *refs), "spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
	})
	items.append({
		"id": "display.ball-in-play-match", "label": "Ball in play and match, two digits", "kind": "segment", "controller_index": 5, "segment_start": 38, "width": 2,
		"provenance": prov("validated", *refs), "spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
	})
	return items


def drivers() -> list[dict]:
	return [
		{"id": "stargzr", "description": "Star Gazer", "year": "1980", "manufacturer": "Stern", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "The 1980 production ROM set (U1, U2, U5 and U6 from the manual's parts list) and the reference for this definition."},
		{"id": "stargzfp", "clone_of": "stargzr", "description": "Star Gazer (Free Play)", "year": "1980", "manufacturer": "Stern", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "Stern free-play ROMs for the same hardware: the same game data (GEN_STMPU200, seven-digit displays, the left-flipper configuration, ST300 sound) and, in the retained burn-in run, the same sixty lamp and nineteen solenoid addresses in the same test order."},
		{"id": "stargzrb", "clone_of": "stargzr", "description": "Star Gazer (modified rules rev. 9)", "year": "2006", "manufacturer": "Stern / Oliver", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "A 2006 modified-rules ROM set (IPDB's Home ROM V9) for the same hardware: PinMAME declares the same game data as the production set and the retained burn-in run published the same sixty lamp and nineteen solenoid addresses in the same test order."},
	]


def excerpt_entries(source_id: str) -> list[dict]:
	seed = json.loads(EXCERPT_SEED_PATH.read_text(encoding="utf-8"))
	entries = []
	for item in seed["excerpts"]:
		if item["source"] != source_id:
			continue
		path = ROOT / EXCERPT_DIR / f"{item['name']}.md"
		entry = {
			"id": f"excerpt.star-gazer.{item['name']}",
			"locator": item["locator"],
			"path": f"{EXCERPT_DIR}/{item['name']}.md",
			"sha256": file_sha256(path),
			"method": "manual",
			"transcribed_by": "curator, read from the rendered page",
			"reviewed": True,
		}
		image = ROOT / EXCERPT_DIR / f"{item['name']}.webp"
		if item.get("image_derivation"):
			entry["image"] = f"{EXCERPT_DIR}/{item['name']}.webp"
			entry["image_sha256"] = file_sha256(image)
			entry["image_derivation"] = item["image_derivation"]
		entries.append(entry)
	return entries


def sources() -> list[dict]:
	summary_sha = file_sha256(ROOT / RUNTIME_SUMMARY)
	return [
		{"id": S_CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
		 "locator": "PinmameGetGames entries stargzr, stargzfp (clone of stargzr) and stargzrb (clone of stargzr)", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
		 "locator": "src/wpc/stgames.c lines 7-16 (dispst6 and dispst7 layouts) and 887-917 (stargzr, stargzfp and stargzrb: GEN_STMPU200, dispst7, FLIP_SW(FLIP_L), SNDBRD_ST300; ST200_ROMSTART8888 ROM sets); src/wpc/by35.c (pia handlers, by35_lampStrobe, SWITCH_UPDATE cabinet port); src/wpc/by35.h",
		 "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/stern-mpu200.json", "revision": PINMAME_REVISION,
		 "locator": "Controller profile pinmame.stern-mpu200: public ranges for switches, the two direct flipper end-of-stroke identities, option switches, solenoids and lamps",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs contributors"},
		{"id": S_IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=2346", "acquired_at": "2026-10-01T22:43:41Z",
		 "sha256": "cdb1cb74b36841a16f09c26ed34ae4baaa34b94b20291c71ff3d3ea2aa1a51be",
		 "locator": "IPDB machine id 2346: Star Gazer, Stern Electronics, Incorporated, Chicago, August 1980, model number 127, MPU Stern M-200, four players, 869 units, design by Brian Poklacki, art by Gerry Simkus; notable features line 'Flippers (2), Pop bumpers (3), Slingshots (2), 3-bank drop targets (3), Spinning targets (3), Stand-up targets (12, one for each Zodiac sign)'. The manual's own parts list heads its table 'STAR GAZER #127', matching the model number, and every count matches the enumerated devices. IPDB answers plain HTTP with 403; the retained page is the Internet Archive capture https://web.archive.org/web/20250119091028id_/https://www.ipdb.org/machine.cgi?id=2346 and lists the manual and schematic files this definition cites, a game-ROM zip and a home ROM V9.",
		 "license": "NOASSERTION", "attribution": "The Internet Pinball Database", "rights": "Rights not asserted; the retained copy is the page only, kept locally for curation"},
		{"id": S_MANUAL, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/stern.star-gazer.1980/ipdb/Stern_1980_Star_Gazer_Manual.pdf",
		 "sha256": "0cd28e0b807c9674727a1888c90d0c95697939c4db95a98cdace3a6738ccf8f8", "original_filename": "Stern_1980_Star_Gazer_Manual.pdf",
		 "source_id": "ipdb-2346", "acquired_at": "2026-10-01T22:43:41Z", "rights": "Copyright Stern Electronics, Inc.; retained locally for curation and not redistributed",
		 "locator": "23-page scan of the Stern Star Gazer #127 game manual, image-only (no text layer; read from renders). PDF page 5-6: general operation and self test; pages 8-10: feature operation and scoring; page 11: MPU option-switch assignment; pages 12-15: option-switch prose; page 16: parts list; page 18: switch identification; page 19: switch locations; page 20: solenoid identification; page 21: solenoid locations; page 22: MPU-200 jumpers and flipper wiring.",
		 "license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; hosted by IPDB", "excerpts": excerpt_entries(S_MANUAL)},
		{"id": S_SCHEMATIC, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/stern.star-gazer.1980/ipdb/Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf",
		 "sha256": "d99a94939a23cf00455eb19eb33f0019e62de1db0b6324c0082d0926c330109b", "original_filename": "Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf",
		 "source_id": "ipdb-2346", "acquired_at": "2026-10-01T22:43:41Z", "rights": "Copyright Stern Electronics, Inc.; retained locally for curation and not redistributed",
		 "locator": "Four 2960 x 2000 scans. PDF page 1: transformer schematic 12B-16B-6A; page 2: playfield sheet with the switch matrix, coil block, general illumination lamp and the LDA lamp chart; page 3: solenoid driver / voltage regulator schematic; page 4: lamp driver schematic 2B-4315-127 sheet 1 of 3 with a second copy of the lamp chart.",
		 "license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; hosted by IPDB", "excerpts": excerpt_entries(S_SCHEMATIC)},
		{"id": S_LIBRARY, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/stern/star-gazer-1980/library/stern.vbs",
		 "sha256": "b835ce5b0c11c6d268f58c92e534c1677e64cb47e103b33179b82c6c337be0e5",
		 "locator": "stern.vbs (header 'Last Updated in VBS v3.61') and core.vbs (SHA-256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69), the VPinMAME libraries the table loads: cabinet-switch constants and key handlers.",
		 "license": "NOASSERTION", "attribution": "VPinMAME contributors", "excerpts": excerpt_entries(S_LIBRARY)},
		{"id": S_SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/Star%20Gazer%20%28Stern%201980%29%20v2.0.0.vbs",
		 "revision": SCRIPT_REVISION, "sha256": "6227ec5440f373b2413d3c2349fbf58c64a612ee9a287d20e5bac09206a2b829", "known_working": True,
		 "locator": "Star Gazer (Stern 1980) v2.0.0.vbs: cGameName stargzr, SolCallback and flipper callbacks, switch and lamp bindings, backglass lamp reads. The embedded script of the retained table equals this file except for whitespace.",
		 "license": "NOASSERTION", "attribution": "UnclePaulie, VPW contributors and vpxtable_scripts contributors", "excerpts": excerpt_entries(S_SCRIPT)},
		{"id": S_TABLE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/stern/star-gazer-1980/source/Star Gazer (Stern 1980) v2.0.0.vpx",
		 "sha256": "b15a49d6902164ae27b946b2f67d1c5682f92bd382288f2c94e2641045128085", "original_filename": "Star Gazer (Stern 1980) v2.0.0.vpx", "known_working": True,
		 "acquired_at": "2026-10-01T22:46:00Z",
		 "locator": f"vpxtool git:v0.33.3 extraction, canonical manifest 0d5764e06bd013668c6d43ed552125533be59396e2915b812755de4c2bcb43ec; playfield bounds left=0 top=0 right={BOUNDS['right']} bottom={BOUNDS['bottom']}, so normalized coordinates are x/{BOUNDS['right']} and y/{BOUNDS['bottom']}. Lamp positions are the centers of the Light objects whose TimerInterval is the public lamp number; switch positions are the objects the script binds (see the geometry excerpt).",
		 "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "UnclePaulie, VPW contributors", "excerpts": excerpt_entries(S_TABLE)},
		{"id": S_CALLOUTS, "kind": "human_review", "uri": "internal:tools/seeds/stern/star-gazer-1980-callouts.json", "sha256": file_sha256(CALLOUT_SEED_PATH),
		 "locator": "2026-10-02 factory location-drawing callout check of the manual's switch drawing (PDF 19, printed 18) and solenoid drawing (PDF 21, printed 20): every callout transcribed independently on gridded tiles of the retained renders, one verifier correction recorded with its reason, per-page control and callout fits; a table placement whose own callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads and overlays are retained under review-artifacts with a pinned manifest.",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs contributors", "rights": "NOASSERTION"},
		{"id": S_RUNTIME, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_SUMMARY}", "revision": PINMAME_REVISION, "sha256": summary_sha,
		 "locator": "Pinned LibPinMAME harness runs of stargzr, stargzfp and stargzrb from empty NVRAM: the burn-in test, the solenoid test paired with its displayed numbers, the switch test over all forty matrix addresses, and gameplay probes of coils, zodiac lamps, flippers and tilt. Raw runs, scenarios and hashes are listed in the summary.",
		 "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	]


def conflicts() -> list[dict]:
	return [{
		"id": "conflict.stand-up-switches-19-20-order",
		"path": "inputs.switch.libra-stand-up-target",
		"description": (
			"The factory switch matrix prints switch 19 as S.U. \"SCORPIO\" and switch 20 as S.U. \"LIBRA\", and the factory playfield drawing numbers the upper-right arch `20`, `19`, `21` from its apex, so both pages put the Libra target at the left end of the pair. "
			"The retained ROM lights the Libra lamp (public 2, chart row LIBRA) when switch 19 closes and the Scorpio lamp (public 18) when switch 20 closes, and the retained table, whose lamps sit on the playfield art's own constellations, puts switch 19 left of switch 20. "
			"The two documents agree with each other, the ROM and the table agree with each other, and the pairs disagree about which switch number belongs to the left target and which sign it is. "
			"A recreation must pair each target with the lamp the ROM lights for its switch, which is what the definition's labels do; where the two targets stand and what the printed sign beside each reads is not settled. "
			"Resolution path: a photograph or a switch test of a production machine showing which stand-up on the upper-right arch reports as switch 19, or a playfield photograph that names the sign printed beside each of the first two arch targets. "
			"The retained ROM, table and manual cannot settle it, because the ROM and table are internally consistent and the manual's two pages agree with each other."
		),
		"source_refs": [S_SCHEMATIC, S_MANUAL, S_RUNTIME, S_TABLE],
	}]


def build_definition() -> dict:
	definition = _build_definition()
	seed = json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8"))
	drawing_callouts.apply_to_definition(definition, seed, S_CALLOUTS)
	return definition


def _build_definition() -> dict:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Star Gazer", "manufacturer": "Stern", "year": 1980, "kind": "physical_pinball",
			"ipdb_id": 2346, "opdb_id": "GrZY2-ML0Rb",
			"playfield": {"width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx", "provenance": prov("validated", S_TABLE)},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
				"mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "display_inventory": "validated",
				"spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.stern-mpu200", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": all_inputs(),
		"outputs": all_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": sources(),
		"knowledge": {"path": "knowledge/stern/star-gazer-1980.md", "status": "partial"},
		"conflicts": conflicts(),
	}


def build_report(definition: dict) -> tuple[dict, str]:
	"""The machine-specific spatial blocker report: what is placed, how, and why the record is not promotable."""
	seed = json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8"))
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition))
	by_status: dict[str, int] = {}
	unplaced = []
	not_applicable: dict[str, int] = {}
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			spatial = device.get("spatial")
			if spatial is None:
				if device.get("availability") == "used":
					unplaced.append({"id": device["id"], "binding": device["binding"], "reason": "no retained source places this used device"})
				continue
			if spatial["status"] == "not_applicable":
				not_applicable[spatial["reason"]] = not_applicable.get(spatial["reason"], 0) + 1
				continue
			for item in spatial["placements"]:
				by_status[item["provenance"]["status"]] = by_status.get(item["provenance"]["status"], 0) + 1
	observed = sorted(
		item["id"]
		for collection in ("inputs", "outputs") for device in definition[collection]
		for item in (device.get("spatial") or {}).get("placements", []) if item["provenance"]["status"] != "validated"
	)
	report = {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {"space": "playfield", "x": "0=left, 1=right in player view", "y": "0=rear/backglass end, 1=apron end in player view"},
		"coverage": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"]},
		"definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
		"transformation": f"x = raw_x / {BOUNDS['right']}, y = raw_y / {BOUNDS['bottom']} (playfield left=0 top=0), rounded to six places by extract_spatial_candidates; objects frozen in tools/seeds/stern/star-gazer-1980-spatial.json",
		"source_hashes": {
			"vpx_table_sha256": SEED["table_sha256"],
			"extraction_manifest_sha256": "0d5764e06bd013668c6d43ed552125533be59396e2915b812755de4c2bcb43ec",
			"spatial_seed_sha256": file_sha256(SPATIAL_SEED_PATH),
			"callout_seed_sha256": file_sha256(CALLOUT_SEED_PATH),
			"manual_sha256": "0cd28e0b807c9674727a1888c90d0c95697939c4db95a98cdace3a6738ccf8f8",
			"schematic_sha256": "d99a94939a23cf00455eb19eb33f0019e62de1db0b6324c0082d0926c330109b",
		},
		"placement_status_counts": dict(sorted(by_status.items())),
		"not_applicable_counts": dict(sorted(not_applicable.items())),
		"callout_check": {
			"pages": {key: {"locator": seed["pages"][key]["locator"], "image_sha256": seed["pages"][key]["image"]["sha256"]} for key in sorted(seed["pages"])},
			"checked": len(decisions["placements"]),
			"validated": sum(1 for d in decisions["placements"].values() if d["agrees"]),
			"limit": decisions["limit"],
			"excluded": seed["excluded_checks"],
		},
		"projection_disclosures": [
			{"devices": ["device.upper-left-drop-bank-reset", "device.right-drop-bank-reset", "device.left-drop-bank-reset"], "class": "hidden assembly projected onto the bank's middle drop target (sw26, sw29, sw23)"},
			{"devices": ["switch.outhole", "device.outhole-kicker"], "class": "placed on the table's Drain kicker, the outhole hole, not on the BallRelease kicker the script binds switch 33 to"},
			{"devices": ["lamp.shoot-again"], "class": "one SCR drives a playfield insert and a backglass lamp; only the playfield bulb is placed"},
			{"devices": ["lamp.star-roll-over-bottom", "lamp.left-3-from-top-star-roll-over", "lamp.left-b-3-star-roll-over", "lamp.left-right-b-4-star-roll-over"], "class": "one lamp number lights a bulb in each lower lane; both lights are placements"},
		],
		"unplaced_physical_devices": unplaced,
		"unvalidated_placements": observed,
		"open_conflicts": [c["id"] for c in definition["conflicts"]],
		"promotion_decision": "Not promotable. Lamp circuits 31 and 47 are fitted and wired but no retained source places them, and the order of the two upper-right arch stand-ups (switches 19 and 20) is an open conflict between the factory pages and the ROM and table. Seven checked placements and five unchecked ones (the left slingshot switch, the two end-of-stroke contacts and the two arch stand-ups) stay observed.",
	}
	lines = [
		"# Star Gazer (Stern 1980) spatial blockers",
		"",
		f"Coverage: **{definition['coverage']['status']}**; missing {', '.join(f'`{item}`' for item in definition['coverage']['missing'])}.",
		"",
		f"Placements by status: {', '.join(f'{count} {status}' for status, count in sorted(by_status.items()))}. Cabinet, backglass, option-switch and unused devices carry controlled `not_applicable` records ({', '.join(f'{count} {reason}' for reason, count in sorted(not_applicable.items()))}).",
		"",
		f"Factory-drawing callout check: {report['callout_check']['validated']} of {report['callout_check']['checked']} checked placements validate within 0.07 normalized (the switch drawing PDF 19 and solenoid drawing PDF 21 of the manual).",
		"",
		"## Blockers",
		"",
		"- Unplaced used devices: " + ", ".join(f"`{item['id']}` (public lamp {item['binding']['device']})" for item in unplaced) + ".",
		"- Open conflict `conflict.stand-up-switches-19-20-order`: the two stand-up switches at the left of the upper-right arch; both placements stay `observed`.",
		"- Placements that stay `observed`: " + ", ".join(f"`{item}`" for item in observed) + ".",
		"",
		"See `knowledge/stern/star-gazer-1980.md` for the evidence and the resolution path.",
		"",
	]
	return report, chr(10).join(lines)


def build_knowledge() -> str:
	return KNOWLEDGE_SOURCE_PATH.read_text(encoding="utf-8")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--definition", type=Path, default=DEFINITION_PATH, help="definition path to check or write (tests use a copy)")
	parser.add_argument("--knowledge", type=Path, default=KNOWLEDGE_PATH)
	parser.add_argument("--report-json", type=Path, default=REPORT_JSON_PATH)
	parser.add_argument("--report-md", type=Path, default=REPORT_MD_PATH)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="fail on drift; never write")
	mode.add_argument("--regenerate", action="store_true", help="rewrite the artifacts")
	args = parser.parse_args()
	built = build_definition()
	definition = canonical_bytes(built)
	note = build_knowledge().encode("utf-8")
	report, report_md = build_report(built)
	report_bytes = canonical_bytes(report)
	report_md_bytes = report_md.encode("utf-8")
	if AUTHOR_READY_PATH.exists():
		print(f"stale author-ready artifact: {AUTHOR_READY_PATH}", file=sys.stderr)
		return 1
	if args.check:
		drifted = False
		for path, want in ((args.definition, definition), (args.knowledge, note), (args.report_json, report_bytes), (args.report_md, report_md_bytes)):
			if not path.exists() or path.read_bytes() != want:
				print(f"canonical content mismatch: {path}", file=sys.stderr)
				drifted = True
		if drifted:
			return 1
		print("Star Gazer definition and knowledge note match the deterministic curator.")
		return 0
	for path, want in ((args.definition, definition), (args.knowledge, note), (args.report_json, report_bytes), (args.report_md, report_md_bytes)):
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(want)
		print(f"wrote {path.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
