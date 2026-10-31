#!/usr/bin/env python3
"""Deterministic curator for Bally Harlem Globetrotters On Tour (1979).

Regenerates the Harlem Globetrotters definition, its knowledge note and its spatial blocker report
from the tables below and the pinned seeds, so the artifacts reproduce byte for byte and drift is
detected. ``--check`` refuses drift and never writes; ``--regenerate`` writes. Generation never reads
the external evidence roots; ``tests/test_harlem_globetrotters.py`` rechecks the seeds against them
when they are present. ``--write-extraction-manifest`` and ``--verify-extraction`` write and check the
canonical full-file manifest of the retained table extraction under ``PINMAME_VPX_SOURCES_ROOT``.

The tables are the curated result of the evidence in the priority the runbook sets out: the retained
ROM's own self tests and gameplay for the public-address translation and runtime semantics, the IPDB
manual and its schematics for construction, wiring and the printed identification numbers, the
known-working table for runtime bindings and coordinates, and pinned PinMAME for emulator topology.
Two facts here look like tidy-ups and are not:

- the printed solenoid numbers are self-test numbers, not public addresses (the ROM pairs them);
- public lamp 43 drives two lines from one SCR, the back box SHOOT AGAIN and the playfield S.P.S.A.

The record stays partial: the retained table draws every playfield insert as an overlay with no bulb,
so 53 playfield lamps have no position.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256  # noqa: E402

MACHINE_ID = "bally.harlem-globetrotters-on-tour.1979"
PARTIAL_PATH = ROOT / "machines" / "partial" / "bally" / "harlem-globetrotters-on-tour-1979.json"
AUTHOR_READY_DIR = ROOT / "machines" / "author-ready"
AUTHOR_READY_PATH = AUTHOR_READY_DIR / "bally" / "harlem-globetrotters-on-tour-1979.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "harlem-globetrotters-on-tour-1979.md"
REPORT_JSON_PATH = ROOT / "reports" / "spatial" / "bally" / "harlem-globetrotters-on-tour-1979.json"
REPORT_MD_PATH = ROOT / "reports" / "spatial" / "bally" / "harlem-globetrotters-on-tour-1979.md"
SPATIAL_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-spatial.json"
EXCERPT_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-excerpts.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-legacy-aliases.json"
KNOWLEDGE_SOURCE_PATH = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-knowledge.md"
RUNTIME_SUMMARY = "evidence/runtime/by35/harlem-globetrotters-on-tour-1979-harness.json"
SWITCH2_SUMMARY = "evidence/runtime/by35/harlem-globetrotters-on-tour-hglbtrtr-switch-2-in-play.json"
EXCERPT_DIR = "evidence/excerpts/bally.harlem-globetrotters-on-tour.1979"
EXTRACTION_RELATIVE_PATH = Path("bally") / "harlem-globetrotters-on-tour-1979" / "extracted-vpxtool"
EXTRACTION_GAME = "hglbtrtb"
EXTRACTION_FILE_COUNT = 551
EXTRACTION_BYTE_COUNT = 10339644

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
PINMAME_COMMITTED_AT = "2026-10-25T20:16:49Z"
SWITCH2_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
PROFILE_REVISION = "628192de7dca7bc1ccfd363fb70431c3274f5b7c"
PROFILE_COMMITTED_AT = "2026-10-22T09:15:55Z"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
SCRIPT_COMMITTED_AT = "2026-07-07T06:37:05Z"
SCRIPT_SHA = "0b0b6727dcf0ba223d0fc4c1a7ab64bfb48e041428bd524e5a9bdd5fdaa24e9d"
EMBEDDED_SCRIPT_SHA = "4452891ab2589728b21d1d2766ead76d56bfdb107038197a8da268a82ed4ffae"
MANUAL_SHA = "5ffb8f9aacec60ee84574edbe44e2a2cfec676b89dcd273e9cb11cd22322a842"
IPDB_PAGE_SHA = "744c6d1db63a984b8b470d08e8cc853472a5d824d646240be37993a70e4a4503"
BALLY_VBS_SHA = "d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c"
CORE_VBS_SHA = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"

S_CATALOG = "pinmame.catalog.46e1a01a0f73"
S_CORE = "pinmame.core.46e1a01a0f73"
S_PROFILE = "controller-profile.pinmame-by35"
S_IPDB = "ipdb.1125"
S_MANUAL = "manual.bally.harlem-globetrotters-on-tour.1979"
S_LIBRARY = "vpinmame-library.bally-vbs"
S_SCRIPT = "vpx-script.harlem-globetrotters.1-2-0"
S_TABLE = "vpx-table.harlem-globetrotters.1-0"
S_RUNTIME = "runtime.harlem-globetrotters-on-tour.harness"
S_SWITCH2 = "runtime.harlem-globetrotters-on-tour.hglbtrtr.switch-2-in-play"

SEED = json.loads(SPATIAL_SEED_PATH.read_text(encoding="utf-8"))
OBJECTS = SEED["objects"]
BOUNDS = SEED["bounds"]
LEGACY = json.loads(LEGACY_ALIAS_SEED_PATH.read_text(encoding="utf-8"))["aliases"]


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def prov(status: str, *refs: str) -> dict:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def aliases(*pairs: tuple[str, object]) -> list[dict]:
	return [{"namespace": namespace, "value": str(value)} for namespace, value in pairs]


def with_legacy(device: dict) -> dict:
	"""Append the legacy import's aliases for this binding, kept while compatibility needs them."""
	legacy = LEGACY.get(device["binding"]["group"], {}).get(str(device["binding"]["device"]))
	if legacy:
		device["aliases"] = list(device["aliases"]) + [{"namespace": namespace, "value": value} for namespace, value in legacy]
	return device


def at(name: str) -> tuple[float, float]:
	item = OBJECTS[name]
	return item["x"], item["y"]


def placement(placement_id: str, role: str, point: tuple[float, float], status: str, *refs: str) -> dict:
	return {"id": placement_id, "role": role, "space": "playfield", "x": point[0], "y": point[1], "provenance": prov(status, *refs)}


def located(status: str, *placements: dict) -> dict:
	return {"status": status, "placements": list(placements)}


def not_applicable(reason: str, *refs: str) -> dict:
	return {"status": "not_applicable", "reason": reason, "provenance": prov("validated", *refs)}


LEAF_NOTE = "The manual's switch assembly adjustments say all leaf springs are \"adjusted for a 1/16\" gap in the open position\", so the contact rests open."
READ_NOTE = "The CPU reads the matrix uninverted: the ROM's switch test shows this number only while the host closes the address."
CAPACITOR_NOTE = "The playfield sheet draws a .05 MFD capacitor across this matrix cell, as it does for the five side targets, the dunk shot target and the three thumper bumpers only."
COIL_TEST_NOTE = "The manual's switch table notes that the slingshot and thumper bumper coils are energized when their switch is made."

# ----------------------------------------------------------------------------------------------
# Switches
# ----------------------------------------------------------------------------------------------

# number -> (label, switch_type, pulse, roles, location, printed description, table objects)
SWITCHES = {
	1: ('Drop target "D" (top)', "leaf", False, [], "Free throw in-line drop targets on the right below the top saucers, rearmost", "DROP TARGET (D) TOP", ["d1"]),
	2: ('Drop target "C"', "leaf", False, [], "Free throw in-line drop targets, third from the front", "DROP TARGET (C)", ["d2"]),
	3: ('Drop target "B"', "leaf", False, [], "Free throw in-line drop targets, second from the front", "DROP TARGET (B)", ["d3"]),
	4: ('Drop target "A" (bottom)', "leaf", False, [], "Free throw in-line drop targets, frontmost", "DROP TARGET (A) BOTTOM", ["d4"]),
	6: ("Credit button", "button", False, ["cabinet.credit-button"], "Coin door", "CREDIT BUTTON", []),
	7: ("Tilt (panel, plumb bob and ball tilts)", "tilt", False, ["cabinet.tilt"], "Panel tilt under the playfield; plumb bob and ball tilt on the left cabinet side near the front door", "TILT (3)", []),
	8: ("Outhole", "leaf", False, ["internal.trough"], "Outhole between the flippers", "OUTHOLE", ["Drain"]),
	9: ("Coin III (right)", "other", True, ["cabinet.coin-door"], "Coin door, right chute (chute #3)", "COIN III (RIGHT)", []),
	10: ("Coin I (left)", "other", True, ["cabinet.coin-door"], "Coin door, left chute (chute #1, hinge side)", "COIN I (LEFT)", []),
	11: ("Coin II (middle)", "other", True, ["cabinet.coin-door"], "Coin door, middle chute (chute #2)", "COIN II (MIDDLE)", []),
	16: ("Slam (door and cabinet)", "tilt", False, ["cabinet.slam-tilt"], "Front door slam switch and a cabinet slam switch", "SLAM (2)", []),
	17: ("Left side spinner", "leaf", True, [], "Spinner on the left wall, beside its four value lamps", "LEFT SIDE SPINNER", ["sw17"]),
	22: ("Right flipper feed lane", "leaf", True, [], "Right flipper return (feed) lane", "FLIP/FEED LANE (RT)", ["sw22"]),
	23: ("Right outlane", "leaf", True, [], "Right outlane, above the free ball gate", "RIGHT OUTLANE", ["sw23"]),
	24: ("Globe saucer", "leaf", False, [], "Top centre G-L-O-B-E saucer (the top basket)", "GLOBE SAUCER", ["sw24"]),
	25: ("Center right spinner", "leaf", True, [], "Right end of the centre spinner bar below the bumpers", "CENTER RIGHT SPINNER", ["sw25"]),
	26: ('Side target "1" (bottom)', "leaf", True, [], "Left side \"Players\" stand-up targets, bottom", 'TARGET "1" (BOTTOM)', ["sw26"]),
	27: ('Side target "2"', "leaf", True, [], "Left side \"Players\" stand-up targets, second from the bottom", 'TARGET "2"', ["sw27"]),
	28: ('Side target "3"', "leaf", True, [], "Left side \"Players\" stand-up targets, middle", 'TARGET "3"', ["sw28"]),
	29: ('Side target "4"', "leaf", True, [], "Left side \"Players\" stand-up targets, second from the top", 'TARGET "4"', ["sw29"]),
	30: ('Side target "5" (top)', "leaf", True, [], "Left side \"Players\" stand-up targets, top", 'TARGET "5" (TOP)', ["sw30"]),
	31: ("Left outlane", "leaf", True, [], "Left outlane", "LEFT OUTLANE", ["sw31"]),
	32: ("Target saucer", "leaf", False, [], "Top right target (free throw) saucer", "TARGET SAUCER", ["sw32"]),
	33: ("Center left spinner", "leaf", True, [], "Left end of the centre spinner bar below the bumpers", "CENTER LEFT SPINNER", ["sw33"]),
	34: ("300 point rebound", "leaf", True, [], "Two rebound rubbers: in the upper left and on the right below the dunk shot target", "300 PT. REBOUND (2)", ["Sling1", "Sling2"]),
	35: ("Dunk shot target", "leaf", True, [], "Slam dunk stand-up target on the right side, below the in-line drop targets", "DUNK SHOT TARGET", ["sw35"]),
	36: ("Right slingshot", "leaf", True, [], "Right slingshot", "RIGHT SLINGSHOT", ["RightSlingshot"]),
	37: ("Left slingshot", "leaf", True, [], "Left slingshot", "LEFT SLINGSHOT", ["LeftSlingshot"]),
	38: ("Bottom thumper bumper", "leaf", True, [], "Bottom (centre) thumper bumper skirt", "BOTTOM THUMPER BUMPER", ["Bumper2"]),
	39: ("Right thumper bumper", "leaf", True, [], "Upper right thumper bumper skirt", "RIGHT THUMPER BUMPER", ["Bumper3"]),
	40: ("Left thumper bumper", "leaf", True, [], "Upper left thumper bumper skirt", "LEFT THUMPER BUMPER", ["Bumper1"]),
}
QUANTITY = {7: 3, 16: 2, 34: 2}
CABINET = {6, 9, 10, 11, 16}
BLANK = (5, 12, 13, 14, 15, 18, 19, 20, 21)
CAPACITOR = {26, 27, 28, 29, 30, 35, 38, 39, 40}
PLACEMENT_SUFFIX = {34: ("upper-left-rebound", "right-rebound")}
PLAYFIELD_STROBE_WIRES = ("51", None, "52", "53", "31")
PLAYFIELD_RETURN_WIRES = ("54", "56", "57", "58", "60", "63", "65", "70")
CABINET_STROBE_WIRES = ("13", "14")
CABINET_RETURN_WIRES = ("15", "65", "20", "21", "23", "25", "27", "30")
PLAYFIELD_SHEET_NAMES = {
	17: "LEFT SIDE SPINNER", 22: "RIGHT FLIPPER FEEDER LANE", 25: "RIGHT CENTER SPINNER", 26: 'LEFT SIDE TARGETS "1" (BOTTOM)',
	33: "LEFT CENTER SPINNER", 34: "300 POINT REBOUND",
}

SWITCH_NOTES = {
	1: "The script raises 1-4 together from output 15 (dtDrop.SolDropUp). In play, knocking this target down fourth, the last of the bank, lit the 5X bonus lamp (public 44), the award the manual gives target #4.",
	2: (
		"In play, knocking this target down third lit the 3X bonus lamp (public 28), the award the manual gives target #3. "
		"The VPinMAME Bally library's generic constant swBallRollTilt names public 2; it is a Bally-wide default, the table does not use it, and the game's own manual and ROM make public 2 this drop target "
		"(the ball tilt is one of the three contacts on public 7). An earlier gameplay run with targets 1, 3 and 4 down showed that closing 2 scores 5,000 as each of them did, lights lamps none of their closures lit, "
		"and keeps the flipper-enable relay (19) raised, so the ROM does not read it as a tilt."
	),
	3: "In play, knocking this target down second lit the 2X bonus lamp (public 12), the award the manual gives target #2.",
	4: "The front target of the bank: the ball reaches the three behind it only after it falls.",
	6: "Pressing it with credits and the ball in the outhole starts a game: the ROM fires the outhole kicker (7) and the drop-target reset (15) and raises the right gate (17) and the flipper-enable relay (19).",
	7: (
		"The manual's installation page lists three normally open tilt switches on this address: the panel tilt on the bottom of the playfield panel, the plumb bob on the left side of the cabinet near the front door, "
		"and the ball tilt above the plumb bob. The playfield sheet draws TILT in the ST0/I6 cell of the playfield connector (A4J2-1, wire 51, and A4J2-14, wire 65), which the wiring below records; "
		"Figure V's legend puts 07 in the cabinet, where the same cell is the cabinet connector's ST0 (A4J3-2, wire 13) and I6 (A4J3-15, wire 27). "
		"Closing it in play makes the ROM drop the flipper-enable relay (19) and the right gate (17) and light the TILT lamp (61)."
	),
	8: "The ball drains into the outhole and closes this switch; the ROM adds and counts down the bonus, then fires the outhole kicker (7) and the drop-target reset (15). Figure V prints 08 below the outhole and 01 (the kicker) in it.",
	9: "Figure V's legend puts 09 on the door. The VPinMAME Bally library calls public 9 swCoin3.",
	10: (
		"Figure V's legend puts 10 on the door. The VPinMAME Bally library calls public 10 swCoin2 and public 11 swCoin1, and the legacy aliases s_coin_2 and s_coin_1 follow it; "
		"the game's own manual calls 10 Coin I (left), and its coin options call the left chute #1 (hinge side)."
	),
	11: "Figure V's legend puts 11 on the door. The VPinMAME Bally library calls public 11 swCoin1; the manual calls it Coin II (middle).",
	16: "The manual says there is one factory slam switch on the front door and that operators may add more; Figure V's legend puts 16 on both the cabinet and the door, and the switch table prints (2).",
	17: "Its four value lamps (100, 200, 1K and 2K: public 6, 22, 38 and 54) sit beside it on the left wall.",
	22: "The manual's bonus feature advances the bonus three steps when the ball goes through the right flipper return lane.",
	23: "With the free ball gate open, a ball entering this outlane scores 3,000 and is directed back onto the right flipper; in play its closure made the ROM raise the gate (17) again and put out GATE OPEN W/LIT (37).",
	24: "The ROM fires the globe saucer kicker (13) while the ball rests on this switch, after scoring and spotting the lit G-L-O-B-E letter; in play an entry lit CENTER \"G\" (15).",
	25: "In play its closure lit SPINNERS ② (20).",
	26: "The manual's feature pages call the five side targets the \"Players\" targets. In play its closure put out SIDE TARGET ① BOTTOM (10).",
	27: "In play its closure put out SIDE TARGET ② (57).",
	28: "In play its closure put out SIDE TARGET ③ (41).",
	29: "In play its closure put out SIDE TARGET ④ (25).",
	30: "In play, knocking out the fifth lite relit the five side-target lamps and lit DUNK SHOT EXTRA BALL (58), the manual's advance of the slam dunk target value.",
	31: "The 25K LEFT OUTLANE lamp (40) lights its value.",
	32: "The ROM fires the target saucer kicker (14) while the ball rests on this switch; in play, with all four in-line targets down, the entry also fired the drop-target reset (15) and lit SAUCER TARGET SPECIAL (56).",
	34: (
		"The switch table prints (2): two rebound contacts on one address, which Figure V draws in the upper left and on the right below the dunk shot target and the retained table binds to its rubber walls Sling1 and Sling2. "
		"The legacy import's source script pulses a separate address, 134, for the second contact; the BY35 matrix ends at 48, and this record carries no binding there."
	),
	35: "In play, hitting it while lit made the ROM drop the right gate (17), opening the free ball gate, and light GATE OPEN W/LIT (37).",
	36: "The ROM fires the right slingshot coil (12) for a closure, in play and in the switch test.",
	37: "The ROM fires the left slingshot coil (11) for a closure, in play and in the switch test.",
	38: "The ROM fires the bottom thumper bumper coil (10) for a closure, in play and in the switch test.",
	39: "The ROM fires the right thumper bumper coil (8) for a closure, in play and in the switch test.",
	40: "The ROM fires the left thumper bumper coil (9) for a closure, in play and in the switch test.",
}


def matrix_wiring(number: int) -> dict:
	column, row = (number - 1) // 8, (number - 1) % 8
	if number in CABINET:
		return {
			"board": "MPU module A4", "control_connection": f"A4J3-{2 + column}", "control_wire": CABINET_STROBE_WIRES[column],
			"return_connection": f"A4J3-{9 + row}", "return_wire": CABINET_RETURN_WIRES[row],
		}
	wiring = {"board": "MPU module A4", "control_connection": f"A4J2-{1 + column}", "return_connection": f"A4J2-{8 + row}", "return_wire": PLAYFIELD_RETURN_WIRES[row]}
	if PLAYFIELD_STROBE_WIRES[column]:
		wiring["control_wire"] = PLAYFIELD_STROBE_WIRES[column]
	return dict(sorted(wiring.items()))


def switch_sources(number: int) -> list[str]:
	refs = [S_MANUAL, S_RUNTIME]
	if SWITCHES[number][6]:
		refs.extend([S_SCRIPT, S_TABLE])
	if number in (2, 6, 7, 9, 10, 11, 16):
		refs.append(S_LIBRARY)
	if number == 2:
		refs.append(S_SWITCH2)
	return refs


def switch_placements(number: int) -> dict:
	label, _, _, roles, _, _, objects = SWITCHES[number]
	if not objects:
		return not_applicable("cabinet_or_service", S_MANUAL)
	base = f"switch.{slug(label)}"
	suffixes = PLACEMENT_SUFFIX.get(number, ("sensor",))
	points = [
		placement(f"{base}.{suffix}", "sensor", at(name), "observed", S_TABLE, S_SCRIPT, S_MANUAL)
		for suffix, name in zip(suffixes, objects)
	]
	return located("observed", *points)


def matrix_switch(number: int) -> dict:
	label, switch_type, pulse, roles, location, printed, objects = SWITCHES[number]
	physical: dict = {"switch_type": switch_type, "location": location}
	notes = [f'Printed switch description "{printed}", self-test display number {number:02d}; the ROM\'s switch test shows {number:02d} when public {number} closes.']
	if number in PLAYFIELD_SHEET_NAMES:
		notes.append(f'The playfield wiring sheet names the cell "{PLAYFIELD_SHEET_NAMES[number]}".')
	if number in SWITCH_NOTES:
		notes.append(SWITCH_NOTES[number])
	if number in (36, 37, 38, 39, 40):
		notes.append(COIL_TEST_NOTE)
	if number in CAPACITOR:
		notes.append(CAPACITOR_NOTE)
	if number in QUANTITY:
		notes.append(f"{QUANTITY[number]} physical contacts are wired in parallel on this one address, so the controller cannot tell which closed.")
		physical["quantity"] = QUANTITY[number]
	if switch_type == "leaf":
		notes.append(LEAF_NOTE)
	notes.append(READ_NOTE)
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
	return with_legacy(item)


def unused_switch(number: int) -> dict:
	if number in BLANK:
		note = (
			f"The manual's switch table prints {number:02d} with no description, Figure V has no {number:02d}, the playfield sheet draws the cell with no label, and the retained table binds nothing to it. "
			f"The ROM's switch test still shows {number:02d} when the host closes it, which proves only that the matrix position is readable, not that a switch is fitted."
		)
		if 9 <= number <= 16:
			note += (
				" Column 2 (9-16) holds only door and cabinet switches; the playfield sheet's ST1 column is empty. "
				"The plug-connector sheet draws a wire on the playfield strobe pin A4J2-2 (ST1) with no wire number, where the playfield sheet prints 93."
			)
		refs = (S_MANUAL, S_SCRIPT, S_RUNTIME)
	else:
		note = (
			"Harlem Globetrotters wires five switch columns: the manual's switch table stops at 40, the MPU's playfield and cabinet strobe connectors carry ST0-ST4 and ST0-ST1 only, "
			"and the retained table binds nothing above 40. The ROM's switch test showed nothing when the host closed 41-48; PinMAME's sixth column has nothing behind it on this game."
		)
		refs = (S_MANUAL, S_CORE, S_RUNTIME)
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
	return with_legacy({
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
		"provenance": prov("validated", S_LIBRARY, S_CORE, S_MANUAL, *((S_RUNTIME,) if number == -7 else ())),
		"spatial": not_applicable("cabinet_or_service", S_LIBRARY, S_CORE),
	})


FLIPPER_COLUMN_BITS = {81: 0x01, 82: 0x02, 83: 0x04, 84: 0x08, 85: 0x10, 86: 0x20, 87: 0x40, 88: 0x80}
# public -> (label, core.h bit name) for the flipper-column positions this machine does not use.
UNUSED_FLIPPER_COLUMN = {
	81: ("Lower-right flipper end-of-stroke position", "CORE_SWLRFLIPEOSBIT"),
	83: ("Lower-left flipper end-of-stroke position", "CORE_SWLLFLIPEOSBIT"),
	85: ("Upper-right flipper end-of-stroke position", "CORE_SWURFLIPEOSBIT"),
	86: ("Upper-right flipper button position", "CORE_SWURFLIPBUTBIT"),
	87: ("Upper-left flipper end-of-stroke position", "CORE_SWULFLIPEOSBIT"),
	88: ("Upper-left flipper button position", "CORE_SWULFLIPBUTBIT"),
}
FLIPPER_COLUMN_NOTE = (
	"PinMAME keeps a generic flipper column at internal column 11 (CORE_FLIPPERSWCOL), which core_swSeq2m publishes at 81-88 (public = matrix index - 7), "
	"so public {number} is bit 0x{bit:02X}, {macro}."
)


def flipper_button(number: int, label: str, side: str) -> dict:
	outputs = (45, 46) if side == "right" else (47, 48)
	pin = "A3J2-1 R. FLIP. SW. (wire 10)" if side == "right" else "A3J2-2 L. FLIP. SW. (wire 20)"
	macro = "CORE_SWLRFLIPBUTBIT" if side == "right" else "CORE_SWLLFLIPBUTBIT"
	return with_legacy({
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases(("pinmame.switch", number)),
		"normally_closed": False,
		"pulse": False,
		"availability": "used",
		"physical": {
			"switch_type": "button",
			"location": "Cabinet side",
			"notes": (
				f"Public {number} is the {side} cabinet flipper button. The buttons are not in the switch matrix: the plug-connector sheet wires them to the solenoid driver ({pin}), "
				"and each reaches its coil line only through a contact of the K1 flipper-enable relay. "
				+ FLIPPER_COLUMN_NOTE.format(number=number, bit=FLIPPER_COLUMN_BITS[number], macro=macro)
				+ f" The driver declares FLIP_SW(FLIP_L) without FLIP_SOL or FLIP_SWNO, so core_updateSw raises the {side} flipper outputs {outputs[0]} and {outputs[1]} from this bit while the button is held and the relay (19) is up, "
				"and never copies it into the game matrix: the ROM never reads it. "
				+ ("In play, holding 82 raised 45 and 46, and a tilt dropped them while it was held." if side == "right" else "In play, holding 84 raised 47 and 48, and after a tilt holding it raised nothing.")
			),
		},
		"roles": [f"flipper.button.{side}"],
		"provenance": prov("validated", S_CORE, S_PROFILE, S_LIBRARY, S_MANUAL, S_RUNTIME),
		"spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
	})


def unused_flipper_column(number: int) -> dict:
	label, macro = UNUSED_FLIPPER_COLUMN[number]
	notes = [
		FLIPPER_COLUMN_NOTE.format(number=number, bit=FLIPPER_COLUMN_BITS[number], macro=macro),
		"The driver declares FLIP_SW(FLIP_L) with no FLIP_SWNO, FLIP_SOL or FLIP_EOS, so core_updateSw's flipper mask holds only the two lower button bits (82 and 84): "
		"it never sets this bit, FLIP_SWL and FLIP_SWR are zero so it copies nothing from the column into the game matrix, the synthetic flipper outputs 45-48 follow only the lower button bits, "
		"and whatever a host writes here is kept but never read.",
	]
	if macro.endswith("EOSBIT"):
		notes.append(
			"The flippers' end-of-stroke contacts are in their coil circuits, not MPU inputs: the playfield sheet draws an \"N.C.\" contact across the upper winding of the left and right flippers "
			"(the upper left flipper's is unlabelled), and returns the upper left flipper's coil through the normally open \"LEFT FLIPPER E.O.S.\" contact."
		)
	else:
		notes.append("The game has no upper flipper button: its upper left flipper shares the left button, and it has no upper right flipper.")
	if number in (81, 83):
		name, key, sol = ("swURFlip", "right", 34) if number == 81 else ("swULFlip", "left", 36)
		notes.append(
			f"The VPinMAME Bally library calls public {number} {name} and writes it for the staged {key} flipper key while its upper {key} flipper solenoid number is non-zero; "
			f"core.vbs defaults that number to {sol} and this table never clears it, so a staged {key} key does write {number}. Nothing on this driver reads the bit, and in play holding {number} changed no output."
		)
	refs = [S_CORE, S_PROFILE, S_MANUAL]
	if number in (81, 83):
		refs.extend([S_LIBRARY, S_RUNTIME])
	return with_legacy({
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases(("pinmame.switch", number)),
		"availability": "unused",
		"physical": {"notes": " ".join(notes)},
		"provenance": prov("validated", *refs),
		"spatial": not_applicable("unused", S_CORE, S_PROFILE),
	})


DIP_FUNCTIONS = {
	**{n: "Credits per coin, coin chute #1 (hinge side), bit of S1-S5" for n in range(1, 6)},
	6: "High score feature award with S7 (replay, extra ball or no award), and with S7 the special award mode (replay, extra ball or novelty)",
	7: "High score feature award and special award mode, with S6",
	8: "Saucer targets reset (ON at the next ball in play only, OFF also when the ball enters the target saucer)",
	**{n: "Credits per coin, coin chute #3, bit of S9-S13" for n in range(9, 14)},
	14: "Globe saucer scanning (ON the G-L-O-B-E lites keep scanning, OFF they step one at a time)",
	15: "Super bonus memory (ON 20,000, 30,000 and 40,000 held in memory)",
	16: "Centre spinners (ON both spinner lites on, OFF the left spinner only, alternating)",
	**{n: "Credits per coin, coin chute #2, bit of S17-S20 (all off = same as chute #1)" for n in range(17, 21)},
	21: "High score to date award, with S22 (no award, one, two or three credits)",
	22: "High score to date award, with S21",
	23: "Dunk shot target special (ON the special can be collected more than once per ball)",
	24: "Side target memory (ON any side target made is held for the next ball)",
	25: "Maximum credits, with S26 (10, 15, 25 or 40)",
	26: "Maximum credits, with S25",
	27: "Credit display (ON shown)",
	28: "Match feature (ON enabled)",
	29: "Sound option, with S30",
	30: "Sound option, with S29",
	31: "Balls per game (ON 5, OFF 3)",
	32: "Globe special lite (ON the left outlane 25,000 and the G-L-O-B-E special lites, OFF the left outlane 25,000 only)",
}
DIP_FORM_NOTE = (
	" The pinned script's option-switch form, titled for the seven-digit conversion, labels S21 \"Score version\" (6 or 7 digit scoring) and S22 \"High game to date\" (no award or 3 credits); "
	"the manual gives S21 and S22 together as the high score to date award. The form may describe the conversion ROM's own use of S21; nothing retained settles it."
)


def dip_switch(number: int) -> dict:
	notes = f"Printed function: {DIP_FUNCTIONS[number]}. The manual's game-adjustment pages assign all thirty-two switches; their tables are transcribed in the game-adjustment excerpt."
	refs = [S_MANUAL, S_CORE]
	if number in (21, 22):
		notes += DIP_FORM_NOTE
		refs.append(S_SCRIPT)
	return {
		"id": f"dip.option-switch-{number}",
		"label": f"MPU option switch S{number}",
		"kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": number},
		"aliases": aliases(("pinmame.dip", number), ("manual.address", f"S{number}")),
		"availability": "used",
		"physical": {"switch_type": "dip", "location": "MPU module A4, back box", "notes": notes},
		"provenance": prov("validated", *refs),
		"spatial": not_applicable("dip_switch", S_MANUAL),
	}


def all_inputs() -> list[dict]:
	items = [
		service_switch(
			-7, "Self-test button", "Inside the coin door",
			"The manual's self-test button inside the front door. Its Figure IV runs the lamp, display, solenoid, sound and stuck-switch tests on successive presses; in the retained runs three presses reach the solenoid test, "
			"a fourth ends it and a fifth starts the switch test. The front door adjustments reach the first high score level after about six presses.",
			"service.self-test",
		),
		service_switch(-6, "CPU diagnostic button", "MPU module", "Named swCPUDiag in the retained VPinMAME Bally library; the manual does not describe this input.", "service.diagnostic"),
		service_switch(-5, "Sound diagnostic button", "Sound module", "Named swSoundDiag in the retained VPinMAME Bally library; the manual does not describe this input.", "service.diagnostic"),
	]
	for number in range(1, 49):
		items.append(matrix_switch(number) if number in SWITCHES else unused_switch(number))
	items.extend([
		unused_flipper_column(81),
		flipper_button(82, "Right flipper button", "right"),
		unused_flipper_column(83),
		flipper_button(84, "Left flipper button", "left"),
	])
	items.extend(unused_flipper_column(number) for number in range(85, 89))
	items.extend(dip_switch(number) for number in range(1, 33))
	return items


# ----------------------------------------------------------------------------------------------
# Solenoids
# ----------------------------------------------------------------------------------------------

FUSED = "fused +43 VDC"
# public -> (self-test number, label, kind, connection, wire, printed connector name, part, object, roles, supply, transistor, notes)
COILS = {
	7: (1, "Outhole kicker", "coil", "A3J1-5", "95", "OUTHOLE", "AN-26-1200", "Drain", ["internal.trough"], FUSED, None,
		"Kicks the ball from the outhole to the shooter alley. The ROM fires it when a credit starts a game and after each drain while switch 8 is closed, together with the drop-target reset (15). "
		"The playfield sheet draws it fed through the playfield fuse \"1A.S.B.\" (wire 30 after the fuse), which the parts list prints \"Fuse, 1 Amp. 3 A6 Slow Blow (Playfield Solenoid Protection)\", E-133-44; "
		"\"3 A6\" is kept as the scan prints it."),
	6: (2, "Knocker", "coil", "A3J2-5", "85", "KNOCKER", "AR-26-1200", None, ["cabinet.knocker"], None, None,
		"Figure V's legend puts solenoid 02 in the cabinet, and the sound option table fires the knocker for a replay credit. "
		"The A3 sheet's dashed route for the unused continuous output CONT. 3 (public 20) also ends at A3J2-5, labelled N/U there; that is a drawing route, and the solenoid test fires this coil at public 6."),
	13: (3, "Globe saucer kicker", "coil", "A3J5-13", "80", "GLOBE SAUCER", "AO-27-1300", "sw24", [], FUSED, None,
		"Fired by the ball resting on switch 24. The ROM also fires it once at power-up."),
	14: (4, "Target saucer kicker", "coil", "A3J5-14", "83", "TARGET SAUCER", "AO-27-1300", "sw32", [], FUSED, None,
		"Fired by the ball resting on switch 32. The ROM also fires it once at power-up."),
	12: (5, "Right slingshot", "coil", "A3J5-15", "85", "RIGHT SLINGSHOT", "AN-26-1200", "RightSlingshot", [], FUSED, None, "Fired by switch 36."),
	11: (6, "Left slingshot", "coil", "A3J5-9", "71", "LEFT SLINGSHOT", "AN-26-1200", "LeftSlingshot", [], FUSED, None, "Fired by switch 37."),
	9: (7, "Left thumper bumper", "coil", "A3J5-12", "75", "LEFT THUMPER BUMPER", "AN-26-1200", "Bumper1", [], FUSED, None, "Fired by switch 40."),
	8: (8, "Right thumper bumper", "coil", "A3J5-10", "74", "RIGHT THUMPER BUMPER", "AN-26-1200", "Bumper3", [], FUSED, None, "Fired by switch 39."),
	10: (9, "Bottom thumper bumper", "coil", "A3J5-11", "78", "BOTTOM THUMPER BUMPER", "AN-26-1200", "Bumper2", [], FUSED, None, "Fired by switch 38."),
	15: (10, "Drop target reset", "coil", "A3J5-8", "18", "DROP TARGET RESET", "NO-26-1900", "in-line-bank", [], FUSED, None,
		"Raises the four in-line targets 1-4 together. The ROM fires it at power-up, when a credit starts a game, with the outhole kick of each new ball and, in the retained runs, when the ball entered the target saucer "
		"with all four targets down; the manual makes that saucer reset depend on option S8. It is placed at the bank's centre (the mean of the four target positions) because the coil is a hidden assembly under the bank."),
	18: (11, "Coin lockout door", "coil", "A3J2-8", "36", "COIN LOCKOUT", "FO-36-700", None, ["cabinet.coin-door"], None, "Q19",
		"A continuous output: the A3 sheet's CONT. 4 driver (PB5, Q19), labelled COIN LOCK OUT on A3J4-9 and COIN LO. at J2 pin 8. Figure V's legend puts solenoid 11 on the door. "
		"The ROM holds it energized in attract mode and play; while the outhole bonus counts down it drops it and raises it five times, each time for a few tens of milliseconds except the last, which it holds."),
	19: (12, "K1 relay (flipper enable)", "relay", None, None, None, None, None, ["cabinet.relay"], None, "Q15",
		"A continuous output: the A3 sheet's CONT. 1 driver (PB6, Q15), whose A3J4-8 line it labels FLIPPER DISABLE and whose relay coil it labels \"FLIPPER ENABLE RLY.\", returned directly to 43 V with suppression diode CR20 across it; the relay sits on the A3 board. "
		"Raised by the ROM when a credit starts a game and held until game over; a tilt drops it and the flipper buttons then do nothing. "
		"Figure V's legend puts solenoid 12 in the back box, and the drawing prints 12 beside all three flippers, whose coil lines its contacts switch."),
	17: (13, "Right gate", "coil", "A3J5-7", "81", "RIGHT GATE", "GA-34-4000", "RightLaneGate", [], FUSED, "Q17",
		"A continuous output: the A3 sheet's CONT. 2 driver (PB4, Q17), drawn to J5 pin 7 \"RIGHT GATE\". It is the free ball gate in the right outlane, and energized means closed: "
		"the ROM raises it when a credit starts a game and at each new ball, drops it when the lit dunk shot target (35) is hit, lighting GATE OPEN W/LIT (37), and raises it again when the ball goes down the right outlane (23). "
		"The manual says \"A tilt closes the FREE BALL GATE\"; the ROM instead drops 17 with the flipper relay on a tilt, so the gate rests in its unpowered, open position for the rest of the tilted ball, and the next ball raises it again. "
		"What the ROM does is what a recreation receives. The known-working script swings the invisible RightLaneGate flipper open while 17 is off and closed while it is on, and Figure V prints its number 13 in the right outer lane below switch 23."),
}
UNUSED_MOMENTARY = (1, 2, 3, 4, 5)


def coil_output(address: int) -> dict:
	test, label, kind, connection, wire, printed, part, obj, roles, supply, transistor, notes = COILS[address]
	device_id = f"device.{slug(label)}"
	physical: dict = {"location": label}
	if part:
		physical["part_number"] = part
	text = (
		f"Printed self-test number {test:02d}. The printed number is the order in which the ROM's solenoid test fires the coils, not a public address; "
		f"the retained solenoid test fires public {address} while it shows {test:02d}, identically on both drivers."
	)
	if printed:
		text += f' The plug-connector sheet names connector pin {connection} "{printed}" (wire {wire}).'
	text += " " + notes
	physical["notes"] = text
	refs = [S_MANUAL, S_RUNTIME]
	if address in (6, 7, 13, 14, 15, 17, 19):
		refs.append(S_SCRIPT)
	item = {
		"id": device_id,
		"label": label,
		"kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address), ("manual.self-test", test)),
		"availability": "used",
		"physical": physical,
		"provenance": prov("validated", *refs),
	}
	wiring: dict = {"board": "Solenoid driver / voltage regulator A3"}
	if connection:
		wiring["drive_connection"] = connection
		wiring["drive_wire"] = wire
	if transistor:
		wiring["driver_transistor"] = transistor
	if supply == FUSED:
		wiring.update({"power_wire": "30", "nominal_voltage_v": 43, "voltage_type": "dc"})
	item["wiring"] = wiring
	if roles:
		item["roles"] = roles
	if obj is None:
		item["spatial"] = not_applicable("cabinet_or_service", S_MANUAL)
	else:
		point = IN_LINE_BANK_CENTRE if obj == "in-line-bank" else at(obj)
		item["spatial"] = located("observed", placement(f"{device_id}.effect", "effect", point, "observed", S_TABLE, S_MANUAL))
	return with_legacy(item)


def _in_line_bank_centre() -> tuple[float, float]:
	names = ("d1", "d2", "d3", "d4")
	xs = [OBJECTS[name]["raw_x"] for name in names]
	ys = [OBJECTS[name]["raw_y"] for name in names]
	return round(sum(xs) / 4 / BOUNDS["right"], 6), round(sum(ys) / 4 / BOUNDS["bottom"], 6)


IN_LINE_BANK_CENTRE = _in_line_bank_centre()


def unused_coil(address: int) -> dict:
	if address == 20:
		note = (
			"The fourth continuous output: the A3 sheet's CONT. 3 driver (PB7, Q13). The sheet's dashed route takes it to A3J2-5, J5-3 and J3-9, each labelled N/U, and the manual's solenoid table names no load for it; "
			"the retained runs show it asserted only in the power-on pulse that briefly drives all four continuous outputs together, never during the self tests or a game. "
			"The plug-connector sheet prints A3J2-5 as KNOCKER (wire 85), the knocker's own pin, which the solenoid test fires at public 6; the disagreement is about a drawing route, not a load on 20."
		)
		label = "Unused continuous output 20"
	else:
		note = (
			f"The manual's solenoid table names thirteen loads and the ROM's solenoid test fires public 6-15 and 17-19, never {address}; the retained runs never assert {address}. "
			"The A3 J1, J2 and J5 load connectors carry no further named coil: their remaining pins are printed N/U."
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
		"provenance": prov("validated", S_MANUAL, S_RUNTIME),
		"spatial": not_applicable("unused", S_MANUAL, S_RUNTIME),
	}


FLIPPER_SYNTHETIC_NOTE = "Synthetic pair 45/46 (right) or 47/48 (left) rises together for the enabled cabinet-button closure; neither is physical winding/EOS telemetry."


def flipper_output(address: int, side: str) -> dict:
	if side == "left":
		notes = (
			"Two flipper coils: the lower left flipper and the upper left flipper below the left slingshot, above it. The parts list counts \"Flipper (3)\", AQ-25-500/34-4500. "
			"The coils are not on a driver transistor: the plug-connector sheet runs them to A3J1-8 \"L. FLIP. COIL\" (wire 40) and the left button to A3J2-2, switched through the K1 flipper-enable relay (19). "
			"The upper left flipper has no connector of its own: the playfield sheet returns its coil (wire 91) through the normally open \"LEFT FLIPPER E.O.S.\" contact to A3J1-8, so it fires only once the lower left flipper reaches end of stroke. "
			"Both take +43 VDC before the playfield fuse. PinMAME publishes the generic lower-left flipper output 48 while the left button (84) is held with the relay up, and raises 47 with it; "
			"the known-working script moves LeftFlipper and LeftFlipper1 together from 48. Figure V prints 12, the K1 relay's number, beside both. " + FLIPPER_SYNTHETIC_NOTE
		)
		label, device_id, quantity, objects = "Left flippers (lower and upper-left)", "device.left-flippers", 2, (("lower", "LeftFlipper"), ("upper", "LeftFlipper1"))
		wiring = {"board": "Hard-wired flipper circuit switched by the K1 relay", "control_connection": "A3J2-2", "control_wire": "20", "drive_connection": "A3J1-8", "drive_wire": "40", "nominal_voltage_v": 43, "voltage_type": "dc"}
	else:
		notes = (
			"One flipper coil, the lower right flipper; on the right a long guide rail runs where a matching upper flipper would be. The parts list counts \"Flipper (3)\", AQ-25-500/34-4500. "
			"The coil is not on a driver transistor: the plug-connector sheet runs it to A3J1-9 \"R. FLIP. COIL\" (wire 70) and the right button to A3J2-1, switched through the K1 flipper-enable relay (19); it takes +43 VDC before the playfield fuse. "
			"PinMAME publishes the generic lower-right flipper output 46 while the right button (82) is held with the relay up, and raises 45 with it; the known-working script moves RightFlipper from 46. "
			"Figure V prints 12, the K1 relay's number, beside it. " + FLIPPER_SYNTHETIC_NOTE
		)
		label, device_id, quantity, objects = "Right flipper", "device.right-flipper", 1, (("lower", "RightFlipper"),)
		wiring = {"board": "Hard-wired flipper circuit switched by the K1 relay", "control_connection": "A3J2-1", "control_wire": "10", "drive_connection": "A3J1-9", "drive_wire": "70", "nominal_voltage_v": 43, "voltage_type": "dc"}
	return with_legacy({
		"id": device_id,
		"label": label,
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address)),
		"availability": "used",
		"physical": {"location": f"{side.title()} flipper assemblies" if side == "left" else "Lower right flipper assembly", "part_number": "AQ-25-500/34-4500", "quantity": quantity, "notes": notes},
		"wiring": wiring,
		"provenance": prov("validated", S_MANUAL, S_SCRIPT, S_CORE, S_PROFILE, S_RUNTIME),
		"spatial": located("observed", *(
			placement(f"{device_id}.{suffix}" if quantity > 1 else f"{device_id}.effect", "effect", at(name), "observed", S_TABLE, S_MANUAL)
			for suffix, name in objects
		)),
	})


def synthetic_flipper(address: int, side: str) -> dict:
	return with_legacy({
		"id": f"device.{side}-flipper-synthetic-duplicate",
		"label": f"{side.title()} flipper synthetic duplicate",
		"kind": "virtual",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address)),
		"availability": "used",
		"physical": {
			"notes": FLIPPER_SYNTHETIC_NOTE + f" In play, holding {'82' if side == 'right' else '84'} raised {address} with {address + 1}; the known-working script binds nothing to {address}.",
		},
		"provenance": prov("validated", S_CORE, S_PROFILE, S_RUNTIME),
		"spatial": not_applicable("virtual", S_CORE, S_RUNTIME),
	})


# ----------------------------------------------------------------------------------------------
# Lamps
# ----------------------------------------------------------------------------------------------

# public -> (label, connector pin, wire, function printed on the lamp driver sheet W-1182-18c)
LAMPS = {
	1: ("1K bonus", "A5J1-18", "58", "1K BONUS"),
	2: ("5K bonus", "A5J1-19", "60", "5K BONUS"),
	3: ("9K bonus", "A5J1-17", "57", "9K BONUS"),
	4: ("Spinners 1 (bottom)", "A5J1-23", "56", "SPINNERS ① BOTTOM"),
	5: ("Spinners 5 (top)", "A5J1-14", "54", "SPINNERS ⑤ TOP"),
	6: ("Left side spinner 100", "A5J1-15", "13", "LEFT SIDE SPINNER 100"),
	7: ('Saucer "G"', "A5J1-16", "12", 'SAUCER "G"'),
	8: ('Saucer "E"', "A5J1-28", "78", 'SAUCER "E"'),
	9: ("Side target 5 (top)", "A5J1-24", "50", "SIDE TARGET ⑤ TOP"),
	10: ("Side target 1 (bottom)", "A5J1-25", "90", "SIDE TARGET ① BOTTOM"),
	11: ('Center "E"', "A5J1-26", "91", 'CENTER "E"'),
	12: ("2X bonus", "A5J1-27", "53", "2 X BONUS"),
	13: ("Ball in play", "A5J2-22", "62", "BALL IN PLAY"),
	14: ("10K bonus", "A5J2-16", "34", "10K BONUS"),
	15: ('Center "G"', "A5J2-14", "12", 'CENTER "G"'),
	17: ("2K bonus", "A5J1-1", "41", "2 K BONUS"),
	18: ("6K bonus", "A5J1-9", "52", "6 K BONUS"),
	19: ("Dunk shot 5K", "A5J1-8", "51", "DUNK SHOT 5K"),
	20: ("Spinners 2", "A5J1-3", "45", "SPINNERS ②"),
	21: ("Dunk shot opens gate", "A5J1-2", "43", "DUNK SHOT OPENS GATE"),
	22: ("Left side spinner 200", "A5J1-10", "23", "LEFT SIDE SPINNER 200"),
	23: ('Saucer "L"', "A5J1-7", "34", 'SAUCER "L"'),
	24: ("Dunk shot special", "A5J1-6", "25", "DUNK SHOT SPECIAL"),
	25: ("Side target 4", "A5J1-5", "48", "SIDE TARGET ④"),
	26: ("Bottom thumper bumper", "A5J1-11", "65", "BOTTOM THUMPER BUMPER"),
	27: ("Match", "A5J2-8", "93", "MATCH"),
	28: ("3X bonus", "A5J1-12", "61", "3X BONUS"),
	29: ("High score to date", "A5J2-23", "97", "HIGH SCORE TO DATE"),
	30: ("20K bonus", "A5J2-20", "35", "20 K BONUS"),
	31: ('Center "L"', "A5J2-15", "23", 'CENTER "L"'),
	33: ("3K bonus", "A5J3-26", "38", "3K BONUS"),
	34: ("7K bonus", "A5J3-25", "36", "7K BONUS"),
	35: ("Right spinner advance bonus", "A5J3-19", "67", "RIGHT SPIN. ADV. BONUS"),
	36: ("Spinners 3", "A5J3-17", "27", "SPINNERS ③"),
	37: ("Gate open when lit", "A5J3-16", "25", "GATE OPEN W/LIT"),
	38: ("Left side spinner 1K", "A5J3-23", "98", "LEFT SIDE SPINNER 1K"),
	39: ('Saucer "O"', "A5J3-27", "40", 'SAUCER "O"'),
	40: ("25K left outlane", "A5J1-13", "96", "25K LEFT OUTLANE"),
	41: ("Side target 3", "A5J3-21", "30", "SIDE TARGET ③"),
	42: ("Left and right thumper bumpers", "A5J3-20", "64", "LEFT AND RIGHT THUMPER BUMPER"),
	43: ("Shoot again", "A5J3-22", "23", "S.P.S.A."),
	44: ("5X bonus", "A5J3-24", "72", "5 X BONUS"),
	45: ("Game over", "A5J2-11", "95", "GAME OVER"),
	46: ("30K bonus", "A5J2-6", "85", "30 K BONUS"),
	47: ('Center "O"', "A5J2-2", "20", 'CENTER "O"'),
	49: ("4K bonus", "A5J3-1", "10", "4 K BONUS"),
	50: ("8K bonus", "A5J3-12", "21", "8 K BONUS"),
	51: ("Left spinner advance bonus", "A5J3-15", "53", "LEFT SPIN. ADV. BONUS"),
	52: ("Spinners 4", "A5J3-11", "20", "SPINNERS ④"),
	53: ("Target saucer 25K", "A5J3-9", "15", "TARGET SAUCER 25K"),
	54: ("Left side spinner 2K", "A5J3-3", "81", "LEFT SIDE SPINNER 2K"),
	55: ('Saucer "B"', "A5J3-4", "14", 'SAUCER "B"'),
	56: ("Saucer target special", "A5J3-2", "95", "SAUCER TARGET SPECIAL"),
	57: ("Side target 2", "A5J3-10", "91", "SIDE TARGET ②"),
	58: ("Dunk shot extra ball", "A5J3-18", "56", "DUNK SHOT EXTRA BALL"),
	59: ("Credit indicator", "A5J3-13", "13", "CREDIT INDICATOR"),
	60: ("G-L-O-B-E special", "A5J3-14", "84", "G-L-O-B-E SPECIAL"),
	61: ("Tilt", "A5J2-10", "98", "TILT"),
	62: ("40K bonus", "A5J2-7", "91", "40 K BONUS"),
	63: ('Center "B"', "A5J2-1", "60", 'CENTER "B"'),
}
BACKBOX_LAMPS = {13, 27, 29, 45, 61}
J2_PLAYFIELD = {14, 15, 30, 31, 46, 47, 62, 63}
# The plug-connector sheet's wording where it differs from the lamp driver sheet's.
PLUG_WORDING = {
	5: "SPINNER ⑤ TOP", 6: "LT. SIDE SPIN. 100", 9: "SIDE TAR. ⑤ TOP", 22: "LT. SIDE SPIN. 200", 26: "BOTTOM T. B.", 35: "RT. SPIN. ADV. BONUS",
	37: "GATE OPENS W/LIT", 38: "LT. SIDE SPIN. 1K", 42: "LEFT AND RIGHT T.B.", 51: "LT. SPIN. ADV. BONUS", 54: "LT. SIDE SPIN. 2K", 58: "DUNK SHOT EX. B.",
}
# A second pin on the same SCR that both sheets print N/U.
NOT_USED_BRANCH = {11: "A5J2-21", 12: "A5J2-13", 27: "A5J1-4", 28: "A5J2-12", 44: "A5J2-4", 59: "A5J2-5", 60: "A5J2-3"}
DOUBLE_INSERTS = {5: ("l5", "l500"), 20: ("l20", "l200"), 36: ("l36", "l360"), 52: ("l52", "l520")}
BULB_PLACEMENTS = {26: (("bottom-bumper-cap", "bumper2l"),), 42: (("left-bumper-cap", "bumper1l"), ("right-bumper-cap", "bumper3l"))}
RUNTIME_LAMP_NOTES = {
	10: "Players target \"1\" (26) put it out in play, and the fifth target relit it.",
	12: "Knocking down the second in-line target lit it in play.",
	15: "The globe saucer's entry lit it in play.",
	20: "A closure of the centre right spinner (25) lit it in play.",
	25: "Players target \"4\" (29) put it out in play, and the fifth target relit it.",
	28: "Knocking down the third in-line target lit it in play.",
	37: "Hitting the lit dunk shot target (35) lit it in play, and the ball going down the right outlane (23) put it out.",
	41: "Players target \"3\" (28) put it out in play, and the fifth target relit it.",
	44: "Knocking down the fourth in-line target lit it in play.",
	56: "The target saucer's entry with all four in-line targets down lit it in play.",
	57: "Players target \"2\" (27) put it out in play, and the fifth target relit it.",
	58: "Knocking out the fifth players target (30) lit it in play.",
	61: "A tilt in play lit it, and the next ball's serve put it out.",
}

LAMP_CHAIN = (
	"PinMAME publishes the main lamp board as public = 16 * d + a + 1 (d the lamp-data line PD0-PD3, a the latched decoder address 0-14), and the AS-2518-23 board takes each decoder output "
	"through its own SCR to fixed connector pins; this record takes that board chain from the Kiss record, which carries the same board and derived it from its own sheets. "
	"The function on each pin is read from this game's A5 lamp driver sheet (W-1182-18c) and plug-connector sheet (W-1187-14c), which agree pin for pin."
)


def lamp_output(public: int) -> dict:
	label, connection, wire, printed = LAMPS[public]
	device_id = f"lamp.{slug(label)}"
	notes = [f'Connector pin {connection} (wire {wire}), printed "{printed}" on the lamp driver sheet.']
	if public in PLUG_WORDING:
		notes.append(f'The plug-connector sheet abbreviates it "{PLUG_WORDING[public]}".')
	physical: dict = {}
	extra_aliases: list[tuple[str, object]] = []
	if public in BACKBOX_LAMPS:
		physical["location"] = "backglass"
		notes.append("The A5 J2 connector is marked TO BACK BOX, this pin is not one of the eight that Table \"B\" routes on to the playfield, and the retained table has no light for this lamp number, so it is a back box lamp with no playfield position.")
	elif public == 43:
		physical["location"] = "playfield and back box"
		physical["quantity"] = 2
		extra_aliases.append(("manual.address", "A5J2-9"))
		notes.append(
			"One SCR drives two lamps here: the playfield S.P.S.A. (same player shoots again) insert on A5J3-22 (wire 23), which the wiring records, and the back box SHOOT AGAIN on A5J2-9 (wire 47). "
			"The retained table draws the playfield insert (light l43) and its backglass is a static image, so a recreation shows both from public 43."
		)
	else:
		physical["location"] = "playfield"
		if public in J2_PLAYFIELD:
			notes.append("Its pin is on A5 J2, which the sheet marks TO BACK BOX, but the function is a playfield lamp: the plug-connector sheet's Table \"B\" routes this pin on through the panel-to-back-cab plug, and the playfield sheet brackets the same eight J2 lamps.")
		if public == 59:
			notes.append("It is the apron's credit window, on J3 TO PLAYFIELD and on the playfield sheet; the retained table puts its light there.")
	if public in NOT_USED_BRANCH:
		notes.append(f"The same SCR also reaches {NOT_USED_BRANCH[public]}, which both sheets print N/U; that branch carries no lamp on this game.")
	if public in RUNTIME_LAMP_NOTES:
		notes.append(RUNTIME_LAMP_NOTES[public])
	if public in DOUBLE_INSERTS:
		first, second = DOUBLE_INSERTS[public]
		notes.append(f"The retained table draws two insert lights for it ({first} and {second}); the wiring sheet draws one lamp symbol per line, including the N/U line, so this record asserts no bulb count.")
	if public in BULB_PLACEMENTS:
		names = [name for _, name in BULB_PLACEMENTS[public]]
		notes.append(
			"Its placement" + ("s are" if len(names) > 1 else " is") + " the table's bumper cap bulb" + ("s " if len(names) > 1 else " ") + " and ".join(names)
			+ ", bulb lights with a bulb model on the " + ("left and right thumper bumpers" if public == 42 else "bottom thumper bumper") + "; the sheet's one lamp symbol per line gives no bulb count."
		)
	elif public not in BACKBOX_LAMPS:
		light = DOUBLE_INSERTS.get(public, (f"l{public}",))[0]
		notes.append(f"The retained table draws it as an insert overlay (light {light}, not a bulb light and with no bulb model), which marks no lamp socket, so it has no placement.")
	notes.append(LAMP_CHAIN)
	physical["notes"] = " ".join(notes)
	sources = [S_MANUAL, S_SCRIPT, S_TABLE]
	if public in RUNTIME_LAMP_NOTES:
		sources.append(S_RUNTIME)
	item = {
		"id": device_id,
		"label": label,
		"kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": public},
		"aliases": aliases(("pinmame.lamp", public), ("manual.address", connection), *extra_aliases),
		"availability": "used",
		"physical": physical,
		"wiring": {"board": "Lamp driver A5 (AS-2518-23)", "drive_connection": connection, "drive_wire": wire},
	}
	if public in BACKBOX_LAMPS:
		item["roles"] = ["cabinet.backglass"]
		item["provenance"] = prov("validated", S_MANUAL, S_TABLE, *((S_RUNTIME,) if public in RUNTIME_LAMP_NOTES else ()))
		item["spatial"] = not_applicable("cabinet_or_service", S_MANUAL)
		return with_legacy(item)
	item["provenance"] = prov("validated", *sources)
	if public in BULB_PLACEMENTS:
		item["spatial"] = located("observed", *(
			placement(f"{device_id}.{suffix}", "emitter", at(name), "observed", S_TABLE, S_SCRIPT, S_MANUAL) for suffix, name in BULB_PLACEMENTS[public]
		))
	return with_legacy(item)


def all_outputs() -> list[dict]:
	items = [coil_output(address) for address in sorted(COILS)]
	items.extend(unused_coil(address) for address in (*UNUSED_MOMENTARY, 20))
	items.extend([synthetic_flipper(45, "right"), flipper_output(46, "right"), synthetic_flipper(47, "left"), flipper_output(48, "left")])
	items.extend(lamp_output(public) for public in sorted(LAMPS))
	items.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return items


# ----------------------------------------------------------------------------------------------
# Mechanisms, relationships, displays, drivers, sources
# ----------------------------------------------------------------------------------------------

def sid(number: int) -> str:
	return f"switch.{slug(SWITCHES[number][0])}"


def did(address: int) -> str:
	return f"device.{slug(COILS[address][1])}"


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, part: str | None = None) -> dict:
	item = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": prov("validated", *refs)}
	if part:
		item["assembly_part_number"] = part
	return item


def mechanisms() -> list[dict]:
	return [
		mechanism(
			"mechanism.outhole", "Outhole and shooter feed", "kicker", [did(7)], [sid(8)],
			"A one-ball game with no trough: the ball drains into the outhole between the flippers, closing switch 8, and the outhole kicker (public 7) serves it to the shooter alley, where the player launches it with the plunger. "
			"The ROM adds the bonus when the ball enters the outhole and counts it down, toggling the coin lockout (18), then kicks the ball and fires the drop-target reset (15) in the same step; "
			"a credit with the ball in the outhole starts the game, fires 7 and 15, and raises the gate (17) and the flipper relay (19).",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.free-throw-in-line-drop-targets", "Free throw in-line drop targets", "drop_target_bank", [did(15)], [sid(4), sid(3), sid(2), sid(1)],
			"Four drop targets standing one behind the other on the right below the top saucers, A (switch 4) at the front to D (switch 1) at the back; the ball reaches each only once the ones in front of it are down. "
			"Each scores, advances the bonus and the Trotter fast break spinner value and spots the lit G-L-O-B-E letter; the second awards the 2X multiplier, the third 3X and the fourth 5X. "
			"The shared reset coil (public 15) raises all four: the ROM fires it at game start, with each new ball's serve and, with option S8 off, when the ball enters the target saucer; with S8 on only at each new ball.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="NO-26-1900"),
		mechanism(
			"mechanism.target-saucer", "Target (free throw) saucer", "kicker", [did(14)], [sid(32)],
			"A top right saucer that kicks the ball out (public 14) after scoring. Its first entry in a ball scores 25,000 (TARGET SAUCER 25K, lamp 53) and its second, with the in-line targets down again, a special (SAUCER TARGET SPECIAL, lamp 56).",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AO-27-1300"),
		mechanism(
			"mechanism.globe-saucer", "Top basket G-L-O-B-E saucer", "kicker", [did(13)], [sid(24)],
			"A top centre saucer ringed by the G-L-O-B-E letters. Each entry scores 3,000, spots the lit letter in the centre of the playfield, advances the bonus and kicks the ball out (public 13). "
			"All five letters spotted scores and flashes 50,000 and, by how many times the letters have been completed and option S32, lights the left outlane 25,000 lite, the G-L-O-B-E special lite or scores a special, then resets the letters, "
			"which are remembered ball to ball. Option S14 chooses between letters that keep scanning and letters that step one at a time.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AO-27-1300"),
		mechanism(
			"mechanism.players-targets", "Left side \"Players\" targets", "other", [], [sid(26), sid(27), sid(28), sid(29), sid(30)],
			"Five stand-up targets on the left wall, switch 26 at the bottom to 30 at the top, each scoring 300 and putting out its lite. Knocking out all five scores 10,000, advances the slam dunk target value (extra ball, special, 5,000) and relights them; option S24 remembers them from ball to ball.",
			S_MANUAL, S_SCRIPT, S_RUNTIME),
		mechanism(
			"mechanism.slam-dunk-target", "Slam dunk target", "other", [], [sid(35)],
			"A stand-up target on the right below the in-line drop targets. It scores 300 or the lit value, and when DUNK SHOT OPENS GATE (21) is lit it opens the free ball gate. Option S23 keeps its special lit for the rest of the ball.",
			S_MANUAL, S_SCRIPT, S_RUNTIME),
		mechanism(
			"mechanism.free-ball-gate", "Free ball gate", "gate", [did(17)], [sid(23)],
			"A gate in the right outlane, powered by the continuous output 17: energized means closed. The ROM closes it at game start and each new ball and opens it (drops 17) when the lit slam dunk target is hit; "
			"a ball entering the open right outlane (switch 23) then scores 3,000, is directed back onto the right flipper, and the ROM closes the gate again. A tilt drops 17 with the flipper relay, so the gate rests open for the rest of a tilted ball, "
			"although the manual says a tilt closes it.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="GA-34-4000"),
		mechanism(
			"mechanism.thumper-bumpers", "Three thumper bumpers", "other", [did(9), did(8), did(10)], [sid(40), sid(39), sid(38)],
			"Two bumpers in the upper middle (left and right) and one below them in the centre (bottom). Each skirt switch makes the ROM fire its own coil: 40 fires 9, 39 fires 8 and 38 fires 10. "
			"Lit bumpers score 1,000; all are lit on a three-ball game and they alternate on a five-ball game. The bottom bumper's cap lamp is 26 and the left and right caps share 42.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.slingshots", "Two slingshots", "other", [did(11), did(12)], [sid(37), sid(36)],
			"The pair above the lower flippers: switch 37 makes the ROM fire the left slingshot (11) and switch 36 the right (12).",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.spinners", "Three spinners", "other", [], [sid(17), sid(33), sid(25)],
			"The left side spinner (switch 17) on the left wall beside its four value lamps (100, 200, 1K and 2K: 6, 22, 38 and 54), and the two centre spinners, left (33) and right (25), at the two ends of the centre spinner bar below the bumpers, "
			"with the SPINNERS 1 to 5 column (4, 20, 36, 52 and 5) and the advance-bonus lamps 51 (left) and 35 (right). A completed centre spinner sequence advances the bonus; option S16 lights both spinners or only an alternating one.",
			S_MANUAL, S_SCRIPT, S_RUNTIME),
		mechanism(
			"mechanism.flippers", "Three flippers", "other", ["device.left-flippers", "device.right-flipper", did(19)],
			["switch.left-flipper-button", "switch.right-flipper-button"],
			"Two lower flippers and an upper left flipper below the left slingshot. The left button fires the lower left flipper, whose normally open end-of-stroke contact then fires the upper left one; the right button fires the right flipper. "
			"The K1 relay (public 19) switches the button-to-coil circuits: it is raised from game start to game over and dropped by a tilt.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, S_IPDB, part="AQ-25-500/34-4500"),
	]


def relationships() -> list[dict]:
	items = [
		("rel.left-slingshot", "direct", sid(37), did(11)),
		("rel.right-slingshot", "direct", sid(36), did(12)),
		("rel.left-thumper-bumper", "direct", sid(40), did(9)),
		("rel.right-thumper-bumper", "direct", sid(39), did(8)),
		("rel.bottom-thumper-bumper", "direct", sid(38), did(10)),
		("rel.globe-saucer", "pulse", sid(24), did(13)),
		("rel.target-saucer", "pulse", sid(32), did(14)),
		("rel.outhole", "pulse", sid(8), did(7)),
		("rel.left-flippers", "relay_gated", "switch.left-flipper-button", "device.left-flippers"),
		("rel.right-flipper", "relay_gated", "switch.right-flipper-button", "device.right-flipper"),
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
		{"id": "hglbtrtr", "description": "Harlem Globetrotters", "year": "1979", "manufacturer": "Bally", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "The 1979 production ROM set (750-07_1.716, 750-08_2.716, U6 720-35_6.716, sound 729-51_3.123) and the reference for this definition: GEN_BY35, six-digit displays (dispBy6), FLIP_SW(FLIP_L), lampCol 0, sound board SNDBRD_BY50."},
		{"id": "hglbtrtb", "clone_of": "hglbtrtr", "description": "Harlem Globetrotters (7-digit conversion)", "year": "2004", "manufacturer": "Bally / Oliver", "flags": 0, "physical_compatibility": "compatible",
		 "variant_notes": (
			 "A Bally/Oliver conversion ROM (one 2732 game ROM harl2732.u2 and a 2732 U6 720-3532.u6b, the same sound ROM) that widens the four player displays to seven digits (dispBy7); it needs seven-digit display hardware and otherwise drives the same machine. "
			 "The catalog dates it 2004 and pinned driver.c's comment 11/02; at power-up it shows its revision, 090, on player 1. In the retained runs it fires the same thirteen solenoid-test outputs in the same order, publishes the same sixty lamps, "
			 "shows the same forty switches in the switch test and fires the same solenoids for the same gameplay stimuli. The known-working table runs this driver."
		 ),
		 "display_overrides": seven},
	]


def excerpt_entries(source_id: str) -> list[dict]:
	seed = json.loads(EXCERPT_SEED_PATH.read_text(encoding="utf-8"))
	entries = []
	for item in seed["excerpts"]:
		if item["source"] != source_id:
			continue
		path = ROOT / EXCERPT_DIR / f"{item['name']}.md"
		entry = {
			"id": f"excerpt.harlem-globetrotters-on-tour.{item['name']}",
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


def sources() -> list[dict]:
	return [
		{"id": S_CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED_AT,
		 "locator": "PinmameGetGames entries hglbtrtr and hglbtrtb (a clone of hglbtrtr); acquired_at is the pinned revision's commit time", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED_AT,
		 "locator": (
			 "src/wpc/by35games.c lines 18-27 (dispBy6 and dispBy7 layouts) and 563-581 (hglbtrtr and hglbtrtb: INITGAME GEN_BY35, FLIP_SW(FLIP_L), lampCol 0, SNDBRD_BY50; hglbtrtb dispBy7, comment rev. 90); "
			 "src/wpc/driver.c lines 214-215 (BY35-750, dated 09/79 and 11/02); src/wpc/by35.c (PIA handlers, by35_lampStrobe, core_updateSw(core_getSol(19))); "
			 "src/wpc/core.c lines 1793-1870 (core_updateSw: the flipper column, FLIP_SWL/FLIP_SWR copied into the game matrix only for FLIP_SWNO, the synthetic flipper outputs raised from the lower button bits while the enable is up, "
			 "the end-of-stroke simulation only for bits in flipMask, every other column bit kept as written), lines 2832-2838 (flipMask: the lower button bits, plus the upper and end-of-stroke bits only for FLIP_UL/FLIP_UR or FLIP_EOS) "
			 "and line 2208 (core_swSeq2m: public = matrix index - 7); src/wpc/core.h line 332 (CORE_FLIPPERSWCOL 11), lines 351-358 (the eight flipper-column bits) and sLRFlip 46, sLLFlip 48. acquired_at is the pinned revision's commit time"
		 ),
		 "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/by35.json", "revision": PROFILE_REVISION, "acquired_at": PROFILE_COMMITTED_AT,
		 "locator": "Controller profile pinmame.by35 as last changed at the revision given: public ranges for switches (-7..-5, 1..48, 81..88), option switches 1..32, solenoids 1..15, 17..20 and 45..48, and lamps; momentary address = selector + 1, continuous outputs at 17-20, the synthetic flipper pairs 45/46 and 47/48",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs contributors"},
		{"id": S_IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=1125", "acquired_at": "2026-10-31T09:47:40Z",
		 "sha256": IPDB_PAGE_SHA, "original_filename": "ipdb1125.html",
		 "locator": (
			 "IPDB machine id 1125: Harlem Globetrotters On Tour, Bally Manufacturing Corporation, project date August 28, 1978, manufactured September 1979, model number 1161-E, MPU Bally AS-2518-35, 14,550 units; "
			 "notable features 'Flippers (3), Pop bumpers (3), Slingshots (2), Standup targets (6), Kick-out holes (2), Spinning targets (3), 4-in-line drop targets, Right outlane detour gate'; design Greg Kmiec, art Greg Freres; "
			 "notes on insert colours. Retained as the Internet Archive capture https://web.archive.org/web/20240214190623id_/https://www.ipdb.org/machine.cgi?id=1125 (29,294 bytes)."
		 ),
		 "license": "NOASSERTION", "attribution": "The Internet Pinball Database", "rights": "Rights not asserted; the retained copy is the page only, kept locally for curation", "excerpts": excerpt_entries(S_IPDB)},
		{"id": S_MANUAL, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/bally.harlem-globetrotters-on-tour.1979/Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf",
		 "sha256": MANUAL_SHA, "original_filename": "Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf", "source_id": "ipdb.1125", "acquired_at": "2026-10-31T09:29:06Z",
		 "rights": "Copyright Bally Manufacturing Corporation; retained locally for curation and not redistributed",
		 "locator": (
			 "46-page image-only scan of the Bally game #1161-E Harlem Globetrotters installation and general game operation instructions with its schematics (IPDB file Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf, 7,067,665 bytes, "
			 "fetched through https://web.archive.org/web/20170605015240id_/http://www.ipdb.org/files/1125/Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf). PDF pages 4-5 and 8-9: installation, general operation, feature operation and scoring; "
			 "10-13: game adjustments; 19: self diagnostic test; 22: solenoid and switch identification; 23: Figure V switch and solenoid locations; 24-25: assembly adjustments and parts list; "
			 "42: A3 solenoid driver W-1183-18c; 43: plug connectors W-1187-14c; 44: A5 lamp driver W-1182-18c; 45: switch matrix and playfield wiring W-1192-14c."
		 ),
		 "license": "NOASSERTION", "attribution": "Bally Manufacturing Corporation; hosted by IPDB", "excerpts": excerpt_entries(S_MANUAL)},
		{"id": S_LIBRARY, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/harlem-globetrotters-on-tour-1979/library/Bally.vbs",
		 "sha256": BALLY_VBS_SHA, "acquired_at": "2026-10-31T09:48:34Z",
		 "locator": f"Bally.vbs (header 'Last Updated in VBS v3.61') and core.vbs (SHA-256 {CORE_VBS_SHA}), the VPinMAME libraries the table loads, copied from the local VPinMAME scripts folder: cabinet-switch constants, flipper key handlers, the flipper solenoid constants, and core.vbs's upper flipper solenoid defaults and Init check (lines 2061-2062, 2090 and 2111-2116).",
		 "license": "NOASSERTION", "attribution": "VPinMAME contributors", "excerpts": excerpt_entries(S_LIBRARY)},
		{"id": S_SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/Harlem_Globetrotters_1.2.0.vbs",
		 "revision": SCRIPT_REVISION, "sha256": SCRIPT_SHA, "known_working": True, "acquired_at": SCRIPT_COMMITTED_AT,
		 "locator": (
			 "Harlem_Globetrotters_1.2.0.vbs (554 lines), JPSalas's 2009 VPX table script on a base script by Gaston: cGameName hglbtrtb, SolCallback and flipper callbacks, the vpmSolDiverter right lane gate, ball stacks, the drop target bank, "
			 f"switch handlers, vpmMapLights and the option-switch form. The retained table's embedded script (SHA-256 {EMBEDDED_SCRIPT_SHA}) is the same table before a later sound update and binds the same switches, solenoids and lamps. "
			 "acquired_at is the pinned corpus revision's commit time."
		 ),
		 "license": "NOASSERTION", "attribution": "JPSalas, Gaston (base script), arngrim (DOF), Inkochnito (option-switch form) and vpxtable_scripts contributors", "excerpts": excerpt_entries(S_SCRIPT)},
		{"id": S_TABLE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/harlem-globetrotters-on-tour-1979/source/Harlem Globetrotters On Tour (Bally 1979).vpx",
		 "sha256": SEED["table_sha256"], "original_filename": "Harlem Globetrotters On Tour (Bally 1979).vpx", "known_working": True, "acquired_at": "2026-10-31T09:33:54Z",
		 "locator": (
			 f"JPSalas's 2009 VPX version 1.0 (6,864,896 bytes), copied from the user's tables archive; vpxtool git:v0.33.3 extraction of {EXTRACTION_FILE_COUNT} files and {EXTRACTION_BYTE_COUNT:,} bytes, canonical manifest {SEED['extraction_manifest_sha256']}; "
			 f"playfield bounds left=0 top=0 right={BOUNDS['right']:g} bottom={BOUNDS['bottom']:g}, so normalized coordinates are x/{BOUNDS['right']:g} and y/{BOUNDS['bottom']:g}. "
			 "Switch and coil positions are the objects the script binds, lamp lights carry their lamp number in the timer interval, and every object used is frozen in tools/seeds/bally/harlem-globetrotters-on-tour-1979-spatial.json."
		 ),
		 "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "JPSalas, Gaston and arngrim", "excerpts": excerpt_entries(S_TABLE)},
		{"id": S_RUNTIME, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_SUMMARY}", "revision": PINMAME_REVISION, "sha256": file_sha256(ROOT / RUNTIME_SUMMARY), "acquired_at": "2026-10-31T10:02:57Z",
		 "locator": "Pinned LibPinMAME harness runs from empty NVRAM: the solenoid test of hglbtrtr and hglbtrtb paired with its displayed numbers, the switch test over all forty-eight matrix addresses on both drivers, and gameplay probes of both drivers and a tilt probe of hglbtrtr. Raw runs, scenarios and hashes are listed in the summary; acquired_at is the time its retained run manifest was written.",
		 "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": S_SWITCH2, "kind": "runtime_scenario", "uri": f"internal:{SWITCH2_SUMMARY}", "revision": SWITCH2_REVISION, "sha256": file_sha256(ROOT / SWITCH2_SUMMARY), "acquired_at": "2026-10-01T12:14:46Z",
		 "locator": (
			 "One hash-pinned LibPinMAME harness run of hglbtrtr from empty NVRAM (scenario tools/harness-scenarios/by35/hglbtrtr-switch-2-in-play.json) that starts a game, closes drop-target switches 1, 3 and 4 and then public 2. "
			 "Each closure scores 5,000; closing 2 also lights lamps 2, 8, 44, 53 and 63, which none of the other closures lit, and the flipper-enable relay (19) stays raised throughout."
		 ),
		 "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	]


def build_definition() -> dict:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Harlem Globetrotters on Tour", "manufacturer": "Bally", "year": 1979, "kind": "physical_pinball",
			"ipdb_id": 1125, "opdb_id": "GRnwQ-M9R5d",
			"playfield": {"width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx", "provenance": prov("validated", S_TABLE)},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
				"mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "display_inventory": "validated",
				"spatial_placement": "observed",
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
		"knowledge": {"path": "knowledge/bally/harlem-globetrotters-on-tour-1979.md", "status": "partial"},
		"conflicts": [],
	}


PROJECTIONS = {"device.drop-target-reset.effect": "the centre of the four in-line target positions d1-d4"}


def build_report(definition: dict) -> tuple[dict, str]:
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
	report = {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {"space": "playfield", "x": "0=left, 1=right in player view", "y": "0=rear/backglass end, 1=apron end in player view"},
		"coverage": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"]},
		"definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
		"transformation": SEED["transformation"] + " Objects are frozen in tools/seeds/bally/harlem-globetrotters-on-tour-1979-spatial.json.",
		"source_hashes": {
			"vpx_table_sha256": SEED["table_sha256"],
			"extraction_manifest_sha256": SEED["extraction_manifest_sha256"],
			"spatial_seed_sha256": file_sha256(SPATIAL_SEED_PATH),
			"manual_sha256": MANUAL_SHA,
		},
		"extraction": {"tool": "vpxtool git:v0.33.3", "file_count": EXTRACTION_FILE_COUNT, "byte_count": EXTRACTION_BYTE_COUNT, "manifest_game": EXTRACTION_GAME},
		"placement_status_counts": dict(sorted(by_status.items())),
		"not_applicable_counts": dict(sorted(not_applicable_counts.items())),
		"callout_check": None,
		"lamp_validation": (
			"No lamp placement is validated. The retained table draws every playfield insert with a Light that is not a bulb light and shows no bulb model, which marks no socket, so those lamps are unplaced; "
			"the only bulb lights with a bulb model on lamp outputs are the three thumper bumper caps (26 and 42), which are observed."
		),
		"projection_disclosures": [
			{"devices": ["device.drop-target-reset"], "class": "hidden assembly projected onto the mean of the four in-line target positions d1-d4"},
			{"devices": ["switch.300-point-rebound"], "class": "parallel contacts on one address, one placement per contact on the rubber walls Sling1 and Sling2"},
			{"devices": ["device.left-flippers"], "class": "two flipper coils on one output, one placement per flipper pivot"},
			{"devices": ["lamp.left-and-right-thumper-bumpers"], "class": "one lamp output lighting two bumper caps, one placement per cap bulb"},
			{"devices": ["device.right-gate"], "class": "the invisible RightLaneGate flipper the script swings as the free ball gate"},
		],
		"unplaced_physical_devices": unplaced,
		"unvalidated_placements": unvalidated,
		"promotion_decision": (
			f"Not promotable: {len(unplaced)} used playfield lamps have no placement because the retained table models their inserts without bulbs, and no placement has had a factory-drawing callout check. "
			"Completing the record needs a table that models the insert bulbs, retained with its geometry and checked against the art, and then a callout check of the switch and coil placements against Figure V."
		),
	}
	lines = [
		"# Harlem Globetrotters On Tour (Bally 1979) spatial blockers",
		"",
		f"Coverage: **{definition['coverage']['status']}**; missing {', '.join(f'`{m}`' for m in definition['coverage']['missing'])}.",
		"",
		f"The coordinate source is the retained `Harlem Globetrotters On Tour (Bally 1979).vpx` (JPSalas VPX version 1.0) at SHA-256 `{SEED['table_sha256']}`, extracted with vpxtool git:v0.33.3 "
		f"({EXTRACTION_FILE_COUNT} files, {EXTRACTION_BYTE_COUNT:,} bytes, canonical manifest `{SEED['extraction_manifest_sha256']}`). Its bounds are `left=0 top=0 right={BOUNDS['right']:g} bottom={BOUNDS['bottom']:g}`, "
		f"so every coordinate is x/{BOUNDS['right']:g} and y/{BOUNDS['bottom']:g} rounded to six places. The lower flipper pivots land at y 0.826 and the drain at 0.974.",
		"",
		f"Placements by status: {', '.join(f'{count} {status}' for status, count in sorted(by_status.items()))}. Cabinet, back box, option-switch, virtual and unused devices carry controlled `not_applicable` records "
		f"({', '.join(f'{count} {reason}' for reason, count in sorted(not_applicable_counts.items()))}).",
		"",
		"## Evidence decisions",
		"",
		"- Switch and coil placements are the objects the script binds: the drop targets d1-d4, the saucer kickers sw24 and sw32, the trough's Drain kicker for the outhole switch and kicker, the spinners, triggers and stand-up targets, "
		"the bumper and slingshot objects the ROM fires for their own switches, and the flipper pivots. They stay `observed`: no factory-drawing callout check has been made.",
		"- Switch 34 has two parallel contacts, each placed on its rubber wall (Sling1 in the upper left, Sling2 on the right).",
		"- The drop-target reset is projected onto the centre of the four in-line targets; the coil is a hidden assembly under the bank.",
		"- The right gate (17) is the invisible `RightLaneGate` flipper the script swings with `vpmSolDiverter`; Figure V prints its number in the right outer lane below switch 23.",
		"- The thumper bumper lamps sit on the bumper cap bulbs `bumper2l` (26) and `bumper1l` and `bumper3l` (42), the only lamp lights the table draws as bulbs with a bulb model.",
		"- Back box lamps 13, 27, 29, 45 and 61, the knocker, the coin lockout, the K1 relay, every cabinet and service switch, the option switches and the displays take controlled `not_applicable` records.",
		"",
		"## The blocker",
		"",
		f"The other {len(unplaced)} used playfield lamps have no position. The retained table draws each insert with a Light whose `is_bulb_light` and `show_bulb_mesh` are both false; such a light marks no socket, "
		"the manual has no lamp location drawing, and nothing else retained places one. Completing the record needs a table that models the insert bulbs, retained with its geometry and checked against the art, "
		"and then a callout check of the switch and coil placements against Figure V with `tools/drawing_callouts.py`.",
		"",
		*(f"- `{item}`" for item in unplaced),
		"",
		"## Excluded objects",
		"",
		"- `gi1`-`gi20` (timer interval 100): the table's twenty general illumination bulb lights, which no PinMAME output drives.",
		"- `BallRelease`: the trough's kick object in the shooter lane, a table helper.",
		"- The second insert lights `l500`, `l200`, `l360` and `l520` of lamps 5, 20, 36 and 52: insert overlays like the first ones.",
		"",
	]
	return report, chr(10).join(lines)


def build_knowledge() -> str:
	return KNOWLEDGE_SOURCE_PATH.read_text(encoding="utf-8")


def _source_root() -> Path:
	root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not root:
		raise SystemExit("PINMAME_VPX_SOURCES_ROOT is required to write or verify the retained Harlem Globetrotters extraction manifest")
	return Path(root)


def write_extraction_manifest() -> str:
	from build_external_evidence_manifest import write_manifest

	return write_manifest(_source_root() / EXTRACTION_RELATIVE_PATH, EXTRACTION_GAME)


def verify_extraction() -> str:
	"""Recompute the retained extraction's canonical manifest and refuse any identity that is not the pinned one."""
	from build_external_evidence_manifest import build_manifest, check_manifest

	extracted = _source_root() / EXTRACTION_RELATIVE_PATH
	digest = check_manifest(extracted, EXTRACTION_GAME)
	files = build_manifest(extracted, EXTRACTION_GAME)["files"]
	identity = (len(files), sum(item["size"] for item in files), digest)
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_BYTE_COUNT, SEED["extraction_manifest_sha256"]):
		raise SystemExit(f"Harlem Globetrotters retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return digest


def shown(path: Path) -> str:
	"""A path for the console: repository-relative when it lies inside the repository."""
	try:
		return path.resolve().relative_to(ROOT.resolve()).as_posix()
	except ValueError:
		return str(path)


def inside(path: Path, directory: Path) -> bool:
	try:
		path.resolve().relative_to(directory.resolve())
	except ValueError:
		return False
	return True


def author_ready_refusal(status: str, explicit: Path | None, target: Path, definition: bytes, writing: bool) -> str | None:
	"""Why this run must not touch the author-ready tree, or None.

	Checked before anything is written or removed. A build that is not author ready never replaces,
	removes or shadows an author-ready definition: demoting one is a reviewed change, never a side
	effect of regeneration. An explicit ``--definition`` exists for test copies and may never point
	into ``machines/author-ready/``. Even an author-ready build refuses to overwrite an author-ready
	definition whose bytes differ from what it would write.
	"""
	if status != "author_ready" and AUTHOR_READY_PATH.exists():
		return (
			f"refusing: this build is {status}, but an author-ready definition exists at {shown(AUTHOR_READY_PATH)}; "
			"demote it through a reviewed change instead of regenerating over it"
		)
	if explicit is not None and inside(explicit, AUTHOR_READY_DIR):
		return f"refusing: --definition {shown(explicit)} points into {shown(AUTHOR_READY_DIR)}; use a copy outside the author-ready tree"
	if writing and status == "author_ready" and target.exists() and target.read_bytes() != definition:
		return f"refusing to overwrite a changed author-ready definition: {shown(target)}"
	return None


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--definition", type=Path, default=None, help="definition path to check or write instead of the one its coverage status names (tests use a copy)")
	parser.add_argument("--knowledge", type=Path, default=KNOWLEDGE_PATH)
	parser.add_argument("--report-json", type=Path, default=REPORT_JSON_PATH)
	parser.add_argument("--report-md", type=Path, default=REPORT_MD_PATH)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="fail on drift; never write")
	mode.add_argument("--regenerate", action="store_true", help="rewrite the artifacts")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		print(f"Harlem Globetrotters extraction manifest written: {write_extraction_manifest()}")
		return 0
	if args.verify_extraction:
		print(f"Harlem Globetrotters retained extraction matches its pinned manifest identity: {verify_extraction()}")
		return 0
	built = build_definition()
	status = built["coverage"]["status"]
	named = AUTHOR_READY_PATH if status == "author_ready" else PARTIAL_PATH
	target = args.definition or named
	definition = canonical_bytes(built)
	refusal = author_ready_refusal(status, args.definition, target, definition, writing=args.regenerate)
	if refusal:
		print(refusal, file=sys.stderr)
		return 2
	note = build_knowledge().encode("utf-8")
	report, report_md = build_report(built)
	outputs = ((target, definition), (args.knowledge, note), (args.report_json, canonical_bytes(report)), (args.report_md, report_md.encode("utf-8")))
	# Only a promotion retires the other status's file, and only the partial one: nothing here ever removes an author-ready definition.
	stale = PARTIAL_PATH if status == "author_ready" and args.definition is None else None
	if args.check:
		drifted = stale is not None and stale.exists()
		if drifted:
			print(f"stale partial definition beside the author-ready one: {stale}", file=sys.stderr)
		for path, want in outputs:
			if not path.exists() or path.read_bytes() != want:
				print(f"canonical content mismatch: {path}", file=sys.stderr)
				drifted = True
		if drifted:
			return 1
		print("Harlem Globetrotters definition, knowledge note and spatial report match the deterministic curator.")
		return 0
	if stale is not None and stale.exists():
		stale.unlink()
		print(f"removed {shown(stale)}")
	for path, want in outputs:
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(want)
		print(f"wrote {shown(path)}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
