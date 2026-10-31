#!/usr/bin/env python3
"""Deterministic curator for Bally Frontier (1980).

Regenerates the Frontier definition, its knowledge note and its spatial report from the tables below
and the pinned seeds, so the artifacts reproduce byte for byte and drift is detected. ``--check``
refuses drift and never writes; ``--regenerate`` writes. ``--write-extraction-manifest`` and
``--verify-extraction`` write or verify the canonical manifest of the retained table extraction
under ``PINMAME_VPX_SOURCES_ROOT``. Generation never reads the external evidence roots;
``tests/test_frontier.py`` rechecks the seeds against them when they are present.

The tables are the curated result of the evidence in the priority the runbook sets out: the
retained ROM's own self tests and gameplay for the public-address translation and runtime
semantics, the IPDB manual and schematics for construction, wiring and the printed identification
numbers, the known-working table for runtime bindings and coordinates, and pinned PinMAME for
emulator topology. Facts here that look like tidy-ups and are not:

- the printed solenoid numbers are self-test numbers, not public addresses (the ROM pairs them);
- public lamp 43 is the playfield SAME PLAYER S.A. insert, not the backglass Shoot Again (public 11);
- the wiring sheet's names for the eight A5 J2 playfield lamps are stale; the lamp driver and
  plug-connector sheets and the ROM agree on the names used here;
- no lamp is placed, because no light of the retained table marks a bulb.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256  # noqa: E402
import build_external_evidence_manifest as evidence_manifest  # noqa: E402

MACHINE_ID = "bally.frontier.1980"
PARTIAL_PATH = ROOT / "machines" / "partial" / "bally" / "frontier-1980.json"
AUTHOR_READY_DIR = ROOT / "machines" / "author-ready"
AUTHOR_READY_PATH = AUTHOR_READY_DIR / "bally" / "frontier-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "frontier-1980.md"
REPORT_JSON_PATH = ROOT / "reports" / "spatial" / "bally" / "frontier-1980.json"
REPORT_MD_PATH = ROOT / "reports" / "spatial" / "bally" / "frontier-1980.md"
SPATIAL_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "frontier-1980-spatial.json"
EXCERPT_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "frontier-1980-excerpts.json"
KNOWLEDGE_SOURCE_PATH = ROOT / "tools" / "seeds" / "bally" / "frontier-1980-knowledge.md"
RUNTIME_SUMMARY = "evidence/runtime/by35/frontier-1980-harness.json"
EXCERPT_DIR = "evidence/excerpts/bally.frontier.1980"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
PINMAME_COMMITTED_AT = "2026-10-25T20:16:49Z"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
SCRIPT_COMMITTED_AT = "2026-07-07T06:37:05Z"
SCRIPT_PATH = "Frontier (Bally 1980).vbs"
SCRIPT_SHA = "1016be1239e4fddb0791e77621f9988b4319afb49b3a06b057f939fd0b58484b"
EMBEDDED_SCRIPT_SHA = "bb0e1773227f75632558b8c42431e1b87d92cf5c38255d8df3179a1aa959b769"
MANUAL_SHA = "e45e64c4e5946fe30b7b9edf9deabb581ea283263e6c20adf8643f54148c8b26"
SCHEMATIC_SHA = "4f8e723eba888c5c17b2ebc8694bc47759097d459212949565d8ce9c5f8e2ce8"
IPDB_SHA = "86d78c714b215c35da6dd52cae4450c83ba00b91d705e712327e1b877f2482db"
LIBRARY_SHA = "d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c"
CORE_VBS_SHA = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
DIRECTB2S_SHA = "570e36792ab44bb4e9baf1245e5f5be49036ea1595d72802fe83c79aff9cce17"

# Acquisition times: the committer date of a pinned revision, the retention time of a retained file,
# the completion of the last retained harness run.
MANUAL_ACQUIRED_AT = "2026-10-31T09:28:53Z"
SCHEMATIC_ACQUIRED_AT = "2026-10-31T09:28:55Z"
IPDB_ACQUIRED_AT = "2026-10-31T09:29:17Z"
TABLE_ACQUIRED_AT = "2026-10-31T09:33:20Z"
LIBRARY_ACQUIRED_AT = "2026-10-31T10:05:51Z"
RUNTIME_ACQUIRED_AT = "2026-10-31T10:34:14Z"

EXTRACTION_RELATIVE_PATH = Path("bally") / "frontier-1980" / "extracted-vpxtool"
EXTRACTION_FILE_COUNT = 1068
EXTRACTION_TOTAL_BYTES = 68276966
EXTRACTION_MANIFEST_SHA256 = "a463dacd3606d3ecc9920adb64223b9c2b9d2d5a79f76209a7571efbad7950ec"

S_CATALOG = "pinmame.catalog.46e1a01a0f73"
S_CORE = "pinmame.core.46e1a01a0f73"
S_PROFILE = "controller-profile.pinmame-by35"
S_IPDB = "ipdb.959"
S_MANUAL = "manual.bally.frontier.1980"
S_SCHEMATIC = "schematic.bally.frontier.1980"
S_LIBRARY = "vpinmame-library.bally-vbs"
S_SCRIPT = "vpx-script.frontier.2-0"
S_TABLE = "vpx-table.frontier.2-0"
S_RUNTIME = "runtime.frontier.harness"

SEED = json.loads(SPATIAL_SEED_PATH.read_text(encoding="utf-8"))
OBJECTS = SEED["objects"]
BOUNDS = SEED["bounds"]
LAMP_LIGHTS = SEED["lamp_lights"]
BULB_MESHES = SEED["bulb_meshes"]


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


def mean_point(*names: str) -> tuple[float, float]:
	xs = [OBJECTS[name]["raw_x"] for name in names]
	ys = [OBJECTS[name]["raw_y"] for name in names]
	return round(sum(xs) / len(xs) / BOUNDS["right"], 6), round(sum(ys) / len(ys) / BOUNDS["bottom"], 6)


LEAF_NOTE = (
	"The manual's assembly adjustments state that all switch assemblies are leaf springs \"adjusted for a 1/16\\\" gap in the open position\", "
	"and the ROM's switch test registers this address when the host closes it on a matrix the CPU reads uninverted, so the contact rests open."
)
I1_WIRE_NOTE = (
	"Its return line is I1, A4J2-9: the plug-connector sheet prints wire 63 there, while the playfield wiring sheet prints 56, the number it also prints on I5; "
	"the record follows the plug-connector sheet, and the disagreement changes no switch."
)

# ----------------------------------------------------------------------------------------------
# Switches
# ----------------------------------------------------------------------------------------------

# number -> (label, switch_type, pulse, roles, location, printed description, table objects)
SWITCHES = {
	1: ("30 point rebound", "leaf", True, [], "Four rebound rubbers: two on the upper-left lane guide, one on the left side below the left target and one on the guide right of the top lanes", "30 POINT REBOUND (4)", ["sw1a1", "sw1a2", "sw1a3", "sw1a4"]),
	2: ("Right outlane", "leaf", True, [], "Right outlane", "RIGHT OUT", ["sw2"]),
	3: ("Right flipper feed lane", "leaf", True, [], "Right return lane feeding the right flipper", "RIGHT FLIPPER FEED", ["sw3"]),
	4: ("Left flipper feed lane", "leaf", True, [], "Left return lane feeding the left flipper", "LEFT FLIPPER FEED", ["sw4"]),
	5: ("Left outlane", "leaf", True, [], "Left outlane", "LEFT OUT", ["sw5"]),
	6: ("Credit button", "button", False, ["cabinet.credit-button"], "Coin door", "CREDIT BUTTON", []),
	7: ("Tilt (panel, plumb bob and ball tilts)", "tilt", False, ["cabinet.tilt"], "Panel tilt under the playfield; plumb bob and ball tilt on the left cabinet side near the door", "TILT (3)", []),
	8: ("Outhole", "leaf", False, ["internal.trough"], "Outhole below the flippers", "OUTHOLE", ["Drain"]),
	9: ("Coin III (right)", "other", True, ["cabinet.coin-door"], "Coin door, right chute (chute #3)", "COIN III (RIGHT)", []),
	10: ("Coin I (left)", "other", True, ["cabinet.coin-door"], "Coin door, left chute (chute #1, hinge side)", "COIN I (LEFT)", []),
	11: ("Coin II (middle)", "other", True, ["cabinet.coin-door"], "Coin door, middle chute (chute #2)", "COIN II (MIDDLE)", []),
	12: ("Saucer", "leaf", False, [], "Saucer at the lower end of the upper-right lane", "SAUCER", ["sw12"]),
	13: ('"A" rollover lane', "leaf", True, [], "Top rollover lanes, left", '"A" ROLLOVER', ["sw13"]),
	14: ('"B" rollover lane', "leaf", True, [], "Top rollover lanes, centre", '"B" ROLLOVER', ["sw14"]),
	15: ('"C" rollover lane', "leaf", True, [], "Top rollover lanes, right", '"C" ROLLOVER', ["sw15"]),
	16: ("Slam (door and cabinet)", "tilt", False, ["cabinet.slam-tilt"], "Front door slam switch and a slam switch on the left side of the cabinet", "SLAM (2)", []),
	21: ("3rd in-line drop target", "leaf", False, [], "In-line drop targets along the left orbit, rearmost", "3RD INLINE DROP TARGET", ["sw21"]),
	22: ("2nd in-line drop target", "leaf", False, [], "In-line drop targets along the left orbit, middle", "2ND INLINE DROP TARGET", ["sw22"]),
	23: ("1st in-line drop target", "leaf", False, [], "In-line drop targets along the left orbit, frontmost", "1ST INLINE DROP TARGET", ["sw23"]),
	24: ("Grizzly target", "leaf", True, [], "Stand-up target at the end of the upper-left orbit, beyond the in-line targets", "GRIZZLY TARGET", ["sw24"]),
	25: ("Saucer rollover button", "leaf", True, [], "Star rollover in the upper-right lane, between the saucer and the gate", "SAUCER ROLLOVER BUTTON", ["sw25"]),
	27: ("Spinner", "leaf", True, [], "Spinner right of centre, below the saucer lane", "SPINNER", ["sw27"]),
	29: ("Left target", "leaf", True, [], "Stand-up target on the left side", "LEFT TARGET", ["sw29"]),
	30: ("Center target", "leaf", True, [], "Stand-up target below the bottom thumper bumper", "CENTER TARGET", ["sw30"]),
	31: ("Right target", "leaf", True, [], "Stand-up target right of centre, beside the spinner", "RIGHT TARGET", ["sw31"]),
	33: ("Bottom side drop target", "leaf", False, [], "Right-side three-bank drop targets, bottom", "BOTTOM SIDE D.T.", ["sw33"]),
	34: ("Middle side drop target", "leaf", False, [], "Right-side three-bank drop targets, middle", "MIDDLE SIDE D.T.", ["sw34"]),
	35: ("Top side drop target", "leaf", False, [], "Right-side three-bank drop targets, top", "TOP SIDE DROP TARGET", ["sw35"]),
	36: ("Right slingshot", "leaf", True, [], "Right slingshot", "RIGHT SLINGSHOT", ["RightSlingShot"]),
	37: ("Left slingshot", "leaf", True, [], "Left slingshot", "LEFT SLINGSHOT", ["LeftSlingShot"]),
	38: ("Bottom thumper bumper", "leaf", True, [], "Thumper bumper in the centre, below the other two", "BOTTOM THUMPER BUMPER", ["sw38"]),
	39: ("Right thumper bumper", "leaf", True, [], "Upper-right thumper bumper", "RIGHT THUMPER BUMPER", ["sw39"]),
	40: ("Left thumper bumper", "leaf", True, [], "Upper-left thumper bumper", "LEFT THUMPER BUMPER", ["sw40"]),
}
QUANTITY = {1: 4, 7: 3, 16: 2}
CABINET = {6, 7, 9, 10, 11, 16}
BLANK = (17, 18, 19, 20, 26, 28, 32)
CAPACITOR = {24, 29, 30, 31, 38, 39, 40}
PLACEMENT_SUFFIX = {1: ("upper-left-rebound-upper", "upper-left-rebound-lower", "left-side-rebound", "top-right-rebound")}
# Wire numbers from the plug-connector sheet: A4J2 (playfield) and A4J3 (cabinet) strobes and returns.
PLAYFIELD_STROBE_WIRES = ("51", "70", "93", "53", "31")
PLAYFIELD_RETURN_WIRES = ("54", "63", "57", "78", "60", "56", "65", "52")
CABINET_STROBE_WIRES = ("13", "14")
CABINET_RETURN_WIRES = ("15", "65", "20", "21", "23", "25", "27", "30")
# Every named cell of the playfield wiring sheet's matrix (W-1192-25c); its cabinet cells are blank.
WIRING_SHEET_NAMES = {
	1: "30 POINT REBOUND (4)", 2: "RIGHT OUT SPECIAL", 3: "RIGHT FLIPPER FEED LANE", 4: "LEFT FLIPPER FEED LANE", 5: "LEFT OUT SPECIAL", 7: "TILT", 8: "OUTHOLE",
	12: "SAUCER", 13: '"A" ROLLOVER LANE', 14: '"B" ROLLOVER LANE', 15: '"C" ROLLOVER LANE',
	21: "3RD. IN LINE DROP TARGET", 22: "2ND IN LINE DROP TARGET", 23: "1ST. IN LINE DROP TARGET", 24: "GRIZZLY TARGET",
	25: "SAUCER ROLLOVER BUTTON", 27: "SPINNER", 29: "LEFT TARGET", 30: "CENTER TARGET", 31: "RIGHT TARGET",
	33: "BOTTOM SIDE DROP TARGET", 34: "MIDDLE SIDE DROP TARGET", 35: "TOP SIDE DROP TARGET", 36: "RIGHT SLINGSHOT", 37: "LEFT SLINGSHOT",
	38: "BOTTOM THUMPER BUMPER", 39: "RIGHT THUMPER BUMPER", 40: "LEFT THUMPER BUMPER",
}

SWITCH_NOTES = {
	1: "The switch table prints (4): four rebound contacts on one address, each scoring 30. The retained table binds the four rubbers sw1a1-sw1a4 to it, and Figure V prints 01 at the same four places.",
	2: "The VPinMAME Bally library's generic constant swBallRollTilt also names public 2; it is a Bally-wide default the Frontier table does not use, and the game's own manual and ROM make public 2 the right outlane (the ball tilt is one of the three contacts on public 7). "
	"In play it scored 1,000 with its special unlit. " + I1_WIRE_NOTE,
	3: "In play, with the right feed lane lamp (12) lit, it scored 15,000.",
	4: "In play, with its lamp (28) unlit, it scored 500.",
	5: "In play, with the left outlane special lamp (60) lit, it scored 1,000 and the special: the ROM fired the knocker (6) and lit the credit lamp (59).",
	6: "Pressing it with credits and the ball in the outhole starts a game: the ROM kicks the outhole (7), fires both drop-target resets (8, 9) and the saucer kicker (10) and raises the flipper-enable relay (19). Pressing it again on ball 1 adds a player.",
	7: "The manual's installation page lists three normally open tilt switches on this address: the panel tilt on the bottom of the playfield panel, the plumb bob on the left side of the cabinet near the front door, and the ball tilt above the plumb bob. "
	"The playfield wiring sheet draws the panel tilt as TILT in the playfield matrix (ST0/I6, A4J2-1 and A4J2-14); the other two are cabinet switches on A4J3. Closing it in play made the ROM drop the flipper-enable relay (19) and light the TILT lamp (61).",
	8: "The ball drains into the outhole and closes this switch; the ROM scores the bonus and fires the outhole kicker (7) and both drop-target resets (8, 9). Figure V prints 08 beside the outhole and 01 (the kicker) at it.",
	9: "Figure V's legend puts 09 on the door. The manual's adjustment and bookkeeping pages say that pressing the coin chute #3 switch, like button S33 on the MPU, sets a displayed score level or bookkeeping register to zero.",
	10: "Figure V's legend puts 10 on the door. The VPinMAME Bally library calls public 10 swCoin2 and public 11 swCoin1; the game's own manual calls 10 Coin I (left), and its coin options call the left chute #1 (hinge side). A coin here gave a credit in play.",
	11: "Figure V's legend puts 11 on the door.",
	12: "The ROM fires the saucer kicker (10) while the ball rests on this switch, after collecting the Frontier bonus (10,000 in play, with the 10K FRONTIER lamp lit).",
	13: "Each closure lights the next animal of the left Den of Predators column and the left thumper bumper lamp (10); it scored 5,000 in play.",
	14: "Each closure lights the next animal of the centre Den of Predators column and the bottom thumper bumper lamp (26); it scored 5,000 in play.",
	15: "Each closure lights the next animal of the right Den of Predators column and the right thumper bumper lamp (42); it scored 5,000 in play. Completing A-B-C the first time lit the A-B-C extra ball (49) and the right flipper feed lane (12), the second time the shoot-again lamps (11, 43) and the A-B-C special (50).",
	16: "The manual says two slam switches are factory installed, one on the front door and one on the left side of the cabinet, and that operators may add more; Figure V's legend puts 16 on both the cabinet and the door, and the switch table prints (2).",
	21: "The rearmost in-line target; the ball reaches it only once 23 and 22 are down. Knocked down in play it scored 15,000 and lit the Frontier 3X (58) and the grizzly target lamps (54, 56). The script raises 21-23 together from output 8.",
	22: "The middle in-line target. Knocked down in play it scored 10,000 and lit the Frontier 2X (57).",
	23: "The frontmost in-line target. Knocked down in play it scored 5,000, raised the gate output (17) and lit the gate arrow (15) and the spinner value (40). The manual's feature page says the first target scores 1,000; the runs used PinMAME's default option switches, which turn on the undocumented S21.",
	24: "Beyond the in-line targets at the end of the left orbit. It scored 30,000 in play and lit the Frontier 4X (52). The manual says hitting it also opens the gate.",
	25: "With the gate open (17 on), rolling over it made the ROM drop 17; with the gate closed it did nothing. The retained script comments it 'Falls'.",
	27: "It scored 10 a closure until the first in-line target lit the spinner lamp (40), then 1,000.",
	29: "Each hit lights the next animal of the left Den of Predators column; it scored 500 in play. Figure V marks it with an arrow.",
	30: "Each hit lights the next animal of the centre Den of Predators column; it scored 500 in play. Figure V marks it with an arrow.",
	31: "Each hit lights the next animal of the right Den of Predators column; it scored 500 in play. Figure V marks it with an arrow.",
	33: "Each of the three side targets scored 500 in play. The script raises 33-35 together from output 9, which the ROM fires as soon as all three are down.",
	34: "Each of the three side targets scored 500 in play. " + I1_WIRE_NOTE,
	35: "Each of the three side targets scored 500 in play. Knocking it down last completed the bank and made the ROM fire the reset (9).",
	36: "The ROM fires the right slingshot coil (15) for a closure; it scored 30 in play.",
	37: "The ROM fires the left slingshot coil (14) for a closure; it scored 30 in play.",
	38: "The ROM fires the bottom thumper bumper coil (13) for a closure; it scored 100 unlit in play.",
	39: "The ROM fires the right thumper bumper coil (12) for a closure; it scored 100 unlit in play.",
	40: "The ROM fires the left thumper bumper coil (11) for a closure; it scored 100 unlit in play.",
}


def matrix_wiring(number: int) -> dict:
	column, row = (number - 1) // 8, (number - 1) % 8
	if number in CABINET:
		return {
			"board": "MPU module A4", "control_connection": f"A4J3-{2 + column}", "control_wire": CABINET_STROBE_WIRES[column],
			"return_connection": f"A4J3-{9 + row}", "return_wire": CABINET_RETURN_WIRES[row],
		}
	return {
		"board": "MPU module A4", "control_connection": f"A4J2-{1 + column}", "control_wire": PLAYFIELD_STROBE_WIRES[column],
		"return_connection": f"A4J2-{8 + row}", "return_wire": PLAYFIELD_RETURN_WIRES[row],
	}


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
	if number in WIRING_SHEET_NAMES:
		notes.append(f'The playfield wiring sheet names the matrix cell "{WIRING_SHEET_NAMES[number]}".')
	else:
		notes.append("The playfield wiring sheet leaves this matrix cell blank: it is a cabinet switch, which the plug-connector sheet brings out on the MPU's cabinet connector A4J3.")
	if number in SWITCH_NOTES:
		notes.append(SWITCH_NOTES[number])
	if number in QUANTITY:
		notes.append(f"{QUANTITY[number]} physical contacts are wired in parallel on this one address, so the controller cannot tell which closed.")
		physical["quantity"] = QUANTITY[number]
	if number in CAPACITOR:
		notes.append("The playfield wiring sheet draws a .05 MFD capacitor across this switch.")
	notes.append(LEAF_NOTE if switch_type == "leaf" else "The ROM's switch test registers this address when the host closes it on a matrix the CPU reads uninverted, so the contact rests open." + (" The manual calls the tilt switches normally open." if number == 7 else ""))
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
			f"The manual's switch table prints {number:02d} with no description, the playfield wiring sheet names nothing in that matrix cell, Figure V has no {number:02d}, and the retained table binds nothing to it. "
			f"The ROM's switch test still shows {number:02d} when the host closes it, which proves only that the matrix position is readable, not that a switch is fitted."
		)
		refs = (S_MANUAL, S_SCHEMATIC, S_SCRIPT, S_RUNTIME)
	else:
		note = (
			"Frontier wires five switch columns: the manual's switch table stops at 40, the MPU's playfield and cabinet strobe connectors carry ST0-ST4 and ST0-ST1 only, "
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
		pin, wire, printed = ("A3J2-1", "10", "R. FLIP. SW.") if side == "right" else ("A3J2-2", "20", "L. FLIP SW.")
		item["normally_closed"] = False
		item["pulse"] = False
		item["roles"] = [f"flipper.button.{side}"]
		item["physical"]["notes"] = (
			f"Public {number} is the {side} cabinet flipper button. Frontier's buttons are not in the switch matrix: the plug-connector sheet wires them to the solenoid driver ({pin} \"{printed}\", wire {wire}) "
			f"so each switches its side's flipper coil through the K1 flipper-enable relay. The driver declares FLIP_SW(FLIP_L) without FLIP_SOL, so PinMAME reads this position of its own flipper column "
			f"and raises the {side} flipper output {output} while the button is held and the relay (19) is up; the ROM never reads it. In play, holding {number} raised {output}, and after a tilt it raised nothing."
		)
		item["wiring"] = {"board": "Solenoid driver / voltage regulator A3", "control_connection": pin, "control_wire": wire}
		item["provenance"] = prov("validated", S_CORE, S_LIBRARY, S_SCHEMATIC, S_RUNTIME)
		item["spatial"] = not_applicable("cabinet_or_service", S_CORE, S_SCHEMATIC)
	else:
		eos = "CORE_SWLRFLIPEOSBIT" if side == "right" else "CORE_SWLLFLIPEOSBIT"
		library = "swURFlip" if side == "right" else "swULFlip"
		item["physical"]["notes"] = (
			f"Public {number} is column 11, bit {number - 81} of PinMAME's generic flipper column (core_swSeq2m), which core.h names {eos}: the lower-{side} flipper's end-of-stroke position. "
			"core_updateSw simulates that contact only for a driver declaring FLIP_EOS; Frontier's declares FLIP_SW(FLIP_L) only, so its flipper mask leaves the bit alone and the ROM never reads column 11. "
			f"The VPinMAME Bally library calls the same address {library}, an upper-{side} flipper button, and writes it from the {side} flipper key whenever the table leaves its upper flipper solenoid number non-zero. "
			"core.vbs sets that number by default and zeroes it only through NoUpperLeftFlipper and NoUpperRightFlipper. The known-working script calls both, so it never writes the position; "
			"the retained table's embedded script lacks those calls and defines neither cSingleLFlip nor cSingleRFlip, so its flipper keys can write it as well. Either way nothing on this driver reads it, "
			"and holding it in play changed no output. Frontier has no upper flipper and nothing is fitted behind it."
		)
		item["provenance"] = prov("validated", S_CORE, S_LIBRARY, S_RUNTIME)
		item["spatial"] = not_applicable("unused", S_CORE, S_RUNTIME)
	return item


# Public flipper-column position -> the core.h bit name of the position (public n is column 11, bit n - 81).
FLIPPER_COLUMN_REST = {
	85: ("CORE_SWURFLIPEOSBIT", "upper-right end-of-stroke switch"),
	86: ("CORE_SWURFLIPBUTBIT", "upper-right flipper button"),
	87: ("CORE_SWULFLIPEOSBIT", "upper-left end-of-stroke switch"),
	88: ("CORE_SWULFLIPBUTBIT", "upper-left flipper button"),
}


def flipper_column_unused(number: int) -> dict:
	bit, meaning = FLIPPER_COLUMN_REST[number]
	note = (
		f"Public {number} is a position of PinMAME's generic flipper column, which the BY35 controller profile declares at 81-88: core_swSeq2m makes it column 11, bit {number - 81}, "
		f"which core.h names {bit}, the {meaning}. Frontier has no upper flipper. The driver declares FLIP_SW(FLIP_L) without FLIP_SWNO, FLIP_BUT or FLIP_EOS, so core_updateSw's flipper mask "
		"covers only the lower buttons 82 and 84: no solenoid, no game-matrix switch and no simulated end-of-stroke contact is derived from this bit, and the ROM never reads column 11; the VPinMAME Bally library writes only 81-84 and the table scripts none of the column directly. "
		"Nothing is fitted behind it."
	)
	return {
		"id": f"switch.unused-flipper-column-{number}",
		"label": f"Unused flipper-column position {number}",
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases(("pinmame.switch", number)),
		"availability": "unused",
		"physical": {"notes": note},
		"provenance": prov("validated", S_CORE, S_PROFILE, S_LIBRARY),
		"spatial": not_applicable("unused", S_CORE, S_PROFILE),
	}


CHUTE_1 = "Credits per coin, coin chute #1 (hinge side), bit of S1-S5"
CHUTE_3 = "Credits per coin, coin chute #3 (right side), bit of S9-S13"
CHUTE_2 = "Credits per coin, coin chute #2 (center), bit of S17-S20 (all off = same as chute #1)"
DIP_FUNCTIONS = {
	**{number: CHUTE_1 for number in range(1, 6)},
	6: "A and C rollover lane lites (ON liberal: making A or C puts both lites out; OFF only that lane's)",
	7: "A-B-C extra ball lite (ON liberal: on at the start of the game; OFF after making A-B-C)",
	8: "Special outlane lites (ON liberal: both come on; OFF one comes on, then alternates)",
	**{number: CHUTE_3 for number in range(9, 14)},
	14: "Special outlane lites and side targets (ON liberal: specials come on with the side drop target 4X; OFF with the side drop target special)",
	15: "A-B-C lane lites recall (ON liberal: a lite put out stays out for the next ball; OFF it comes back on)",
	16: "Frontier bonus score (ON liberal: collected in the outhole; OFF not collected there)",
	**{number: CHUTE_2 for number in range(17, 21)},
	23: "Frontier bonus lite (ON liberal: stops at 110,000; OFF at 60,000)",
	24: "Gate recall (ON liberal: an open gate stays open for the next ball; OFF it closes)",
	25: "Maximum credits, with S26 (10, 15, 25 or 40)",
	26: "Maximum credits, with S25",
	27: "Credit display (ON shown)",
	28: "Match feature (ON enabled)",
	30: "Flipper feed lane 15,000 lite (ON liberal: both come on; OFF one comes on, then alternates)",
	31: "Balls per game, with S32 (2, 3, 4 or 5)",
	32: "Balls per game, with S31",
}
UNDOCUMENTED_DIPS = (21, 22, 29)
DIP_DEFAULT_ON = (20, 21)


def dip_switch(number: int) -> dict:
	default = (
		f" PinMAME's BY35 input ports default it {'on' if number in DIP_DEFAULT_ON else 'off'} (src/wpc/by35.h BY35_COMPORTS), and the harness never changes it, so every retained run had it {'on' if number in DIP_DEFAULT_ON else 'off'}."
	)
	if number in UNDOCUMENTED_DIPS:
		notes = (
			f"The manual's game adjustment pages (PDF 9-12) assign S1-S20, S23-S28 and S30-S32 and never mention S{number}; no other page of the manual, no sheet and the retained table's option form name it either, "
			f"so its function is unknown and no function is asserted.{default}"
		)
		return {
			"id": f"dip.option-switch-{number}",
			"label": f"Undocumented option switch S{number}",
			"kind": "dip_switch",
			"binding": {"group": "pinmame.input.dip", "device": number},
			"aliases": aliases(("pinmame.dip", number), ("manual.address", f"S{number}")),
			"availability": "unknown",
			"physical": {"switch_type": "dip", "location": "MPU module A4, back box", "notes": notes},
			"provenance": prov("validated", S_MANUAL, S_CORE, S_SCRIPT),
			"spatial": not_applicable("dip_switch", S_MANUAL),
		}
	notes = f"Printed function: {DIP_FUNCTIONS[number]}. The manual's game-adjustment pages assign it; their tables are transcribed in the game-adjustment excerpt.{default}"
	if number in (25, 26):
		notes += " On frontiea, the Bally/Oliver free-play ROM, S25 and S26 both on enable free play instead (its info.txt)."
	if number == 14:
		notes += (
			" The retained table's option form disagrees on the OFF setting: its frame \"Outlane Special lights when\" offers \"3X lights\" (off) and \"4X lights\" (on), where the manual prints SW. 14 ON "
			"\"Special lites come on when side drop target 4X is on.\" and SW. 14 OFF \"Special lites come on when side drop target special is on.\" The ON readings agree. This record follows the manual: "
			"with S14 off, the ROM lit the outlane special (60) together with the drop-target special (62) on the right bank's third completion, not with the 3X drop-target lamp (30) on the first. "
			"The form's OFF label is a defect in the table."
		)
	if number == 30:
		notes += (
			" The retained table's option form calls it \"Feeder Lane Special lights\" (Alternate, Both light); the manual's lite is the 15,000 award, and in play the lit right feed lane scored 15,000, "
			"so the form's word \"Special\" is a wording slip in the table. Its Alternate and Both light settings match the manual's."
		)
	refs = [S_MANUAL, S_CORE]
	if number in (14, 30):
		refs.extend([S_SCRIPT, S_RUNTIME])
	elif number in (25, 26):
		refs.append(S_RUNTIME)
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
		service_switch(-7, "Self-test button", "Inside the coin door", "The manual's self-test button inside the front door. In the retained runs, three presses reach the solenoid test, a fourth the sound test and a fifth the stuck-switch test, as the manual's self-test page lists them; its bookkeeping page says ten presses reach the first bookkeeping entry.", "service.self-test"),
		service_switch(-6, "CPU diagnostic button", "MPU module", "Named swCPUDiag in the retained VPinMAME Bally library; the manual does not describe this input.", "service.diagnostic"),
		service_switch(-5, "Sound diagnostic button", "Sound module", "Named swSoundDiag in the retained VPinMAME Bally library; the manual does not describe this input.", "service.diagnostic"),
	]
	for number in range(1, 49):
		items.append(matrix_switch(number) if number in SWITCHES else unused_switch(number))
	items.extend([
		flipper_button(81, "Lower-right flipper end-of-stroke position", "unused", "right"),
		flipper_button(82, "Right flipper button", "used", "right"),
		flipper_button(83, "Lower-left flipper end-of-stroke position", "unused", "left"),
		flipper_button(84, "Left flipper button", "used", "left"),
	])
	items.extend(flipper_column_unused(number) for number in sorted(FLIPPER_COLUMN_REST))
	items.extend(dip_switch(number) for number in range(1, 33))
	return items


# ----------------------------------------------------------------------------------------------
# Solenoids
# ----------------------------------------------------------------------------------------------

# public -> (self-test number, label, kind, connection, wire, printed connector name, part, object, roles, notes)
COILS = {
	6: (2, "Knocker", "coil", "A3J2-5", "85", "KNOCKER", "AR-26-1200", None, ["cabinet.knocker"],
		"Figure V's legend puts solenoid 02 in the cabinet, and the drawing prints 02 on the cabinet side right of the shooter lane. The ROM fired it when the left outlane scored its lit special; the known-working script's SolKnocker only plays a sound."),
	7: (1, "Outhole kicker", "coil", "A3J1-5", "95", "OUTHOLE", "AN-26-1200", "Drain", ["internal.trough"],
		"Kicks the ball from the outhole to the shooter lane. The ROM fires it when a credit starts a game and after each drain while switch 8 is closed."),
	8: (5, "In-line drop target reset", "coil", "A3J5-10", "85", "DROP TARGET(IN LINE)", "NO-26-1900", "inline-bank", [],
		"Raises the three in-line targets 21-23 together. The ROM fires it at power-on, at game start and at each drain, not when the bank is completed. It is placed at the bank's centre (the mean of the three target positions) because the coil is a hidden assembly under the bank; Figure V prints 05 below the bank."),
	9: (3, "Right drop target reset", "coil", "A3J5-12", "80", "3 DROP TARGET", "NO-26-1900", "sw34", [],
		"Raises the three right-side targets 33-35 (the manual's 3 DROP TARGET RESET). The ROM fires it at power-on, at game start, at each drain and as soon as all three are down. It is placed on the bank's middle target because the coil is a hidden assembly behind the bank; Figure V prints 03 below the bank."),
	10: (4, "Saucer kicker", "coil", "A3J5-11", "78", "SAUCER", "AO-27-1300", "sw12", [],
		"Fired by the ball resting on switch 12; the ROM also fires it at power-on and at game start. The retained table kicks with sw12.Kick -10, and the manual's eject-saucer drawing shows the kick running up the lane and through the gate."),
	11: (6, "Left thumper bumper", "coil", "A3J5-9", "71", "LEFT THUMPER BUMPER", "AN-26-1200", "sw40", [], "Fired by switch 40."),
	12: (7, "Right thumper bumper", "coil", "A3J5-15", "74", "RIGHT THUMPER BUMPER", "AN-26-1200", "sw39", [], "Fired by switch 39."),
	13: (8, "Bottom thumper bumper", "coil", "A3J5-13", "67", "BOTTOM THUMPER BUMPER", "AN-26-1200", "sw38", [], "Fired by switch 38."),
	14: (9, "Left slingshot", "coil", "A3J5-14", "83", "LEFT SLINGSHOT", "AO-26-1200", "LeftSlingShot", [], "Fired by switch 37."),
	15: (10, "Right slingshot", "coil", "A3J5-8", "18", "RIGHT SLINGSHOT", "AO-26-1200", "RightSlingShot", [], "Fired by switch 36."),
	17: (11, "Gate", "coil", "A3J5-7", "81", "GATE", "GO-36-6900", "Gate2", [],
		"A continuous output (PIA1 port B bit 4, published at 17). The ROM holds it on to open the gate at the top of the saucer lane: in play from the first in-line target (the manual says any in-line target or the grizzly target) until the ball rolled over the saucer rollover (25), or until the drain; option S24 keeps it open for the next ball. Adding a player left it on. "
		"The known-working script holds its invisible one-way gate Gate2 open while 17 is on, and the placement is that gate; Figure V prints 11 on the gate with an arrow."),
	18: (12, "Coin lockout door", "coil", "A3J2-8", "36", "COIN LOCKOUT", "FO-36-7000", None, ["cabinet.coin-door"],
		"A continuous output. Figure V's legend puts solenoid 12 on the door. The ROM energizes it shortly after power-on; in the gameplay probe it dropped briefly while the saucer collected its bonus and while the drained ball's bonus was counted, and came back on afterwards."),
	19: (13, "K1 relay (flipper enable)", "relay", None, None, None, None, None, ["cabinet.relay"],
		"A continuous output. Raised by the ROM when a credit starts a game and held until game over; a tilt drops it and the flipper buttons then do nothing. Figure V's legend puts solenoid 13 in the back box, and the drawing prints 13 beside both flippers, whose coils it switches. The page prints KI for K1."),
}
UNUSED_MOMENTARY = (1, 2, 3, 4, 5)
SCRIPT_COILS = (6, 7, 8, 9, 10, 17, 19)
INLINE_BANK_CENTRE = mean_point("sw21", "sw22", "sw23")


def coil_output(address: int) -> dict:
	test, label, kind, connection, wire, printed, part, obj, roles, notes = COILS[address]
	device_id = f"device.{slug(label)}"
	physical: dict = {"location": label}
	if part:
		physical["part_number"] = part
	text = (
		f"Printed self-test number {test:02d}. The printed number is the order in which the ROM's solenoid test fires the coils, not a public address; "
		f"the retained solenoid test fires public {address} while it shows {test:02d}, identically on frontier and frontiea."
	)
	if printed:
		text += f' The plug-connector sheet names connector pin {connection} "{printed}" (wire {wire}), and the playfield wiring sheet runs the same wire to the coil.' if obj else f' The plug-connector sheet names connector pin {connection} "{printed}" (wire {wire}).'
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
		"provenance": prov("validated", S_MANUAL, S_SCHEMATIC, S_RUNTIME, *((S_SCRIPT,) if address in SCRIPT_COILS else ())),
	}
	if connection:
		item["wiring"] = {"board": "Solenoid driver / voltage regulator A3", "drive_connection": connection, "drive_wire": wire}
	if roles:
		item["roles"] = roles
	if obj is None:
		item["spatial"] = not_applicable("cabinet_or_service", S_MANUAL)
	else:
		point = INLINE_BANK_CENTRE if obj == "inline-bank" else at(obj)
		item["spatial"] = located("observed", placement(f"{device_id}.effect", "effect", point, "observed", S_TABLE, S_MANUAL))
	return item


def unused_coil(address: int) -> dict:
	if address == 20:
		note = (
			"The fourth continuous output. The manual's solenoid table names thirteen loads and none of them is on this address, the plug-connector sheet names no load for it, "
			"and the retained runs show it asserted only in the power-on pulse that briefly drives all four continuous outputs, never during the self tests or a game."
		)
		label = "Unused continuous output 20"
	else:
		note = (
			f"The manual's solenoid table names thirteen loads and the ROM's solenoid test fires thirteen public addresses, none of them {address}; "
			f"the retained runs never assert {address}. The A3 J1, J2 and J5 load connectors name no further coil."
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
	obj = "LeftFlipper" if side == "left" else "RightFlipper"
	connection, wire, printed = ("A3J1-8", "40", "L. FLIP COIL") if side == "left" else ("A3J1-9", "70", "R. FLIP COIL")
	button = 84 if side == "left" else 82
	notes = (
		f"The {side} flipper coil, AQ-25-500/34-4500 (the parts list counts Flipper (2)). It is not on a driver transistor: the plug-connector sheet runs it to {connection} \"{printed}\" (wire {wire}) "
		f"and the {side} button to the solenoid driver, switched through the K1 flipper-enable relay (19); the playfield wiring sheet draws it as two windings with an end-of-stroke switch. "
		f"PinMAME publishes the generic lower-{side} flipper output {address} while the {side} button ({button}) is held with the relay up, together with its duplicate state {address - 1}, "
		f"which has its own virtual record. The known-working script drives {obj} from {address}."
	)
	return {
		"id": f"device.{side}-flipper",
		"label": f"{side.title()} flipper",
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address)),
		"availability": "used",
		"physical": {"location": f"{side.title()} flipper assembly", "part_number": "AQ-25-500/34-4500", "notes": notes},
		"wiring": {
			"board": "Hard-wired flipper circuit switched by the K1 relay", "drive_connection": connection, "drive_wire": wire,
			"control_connection": "A3J2-1" if side == "right" else "A3J2-2", "control_wire": "10" if side == "right" else "20",
		},
		"provenance": prov("validated", S_MANUAL, S_SCHEMATIC, S_SCRIPT, S_CORE, S_RUNTIME),
		"spatial": located("observed", placement(f"device.{side}-flipper.effect", "effect", at(obj), "observed", S_TABLE, S_MANUAL)),
	}


def flipper_state_output(address: int, side: str) -> dict:
	pair = address + 1
	button = 82 if side == "right" else 84
	letter = "R" if side == "right" else "L"
	notes = (
		f"PinMAME's synthetic {side} flipper state beside {pair}, not a second coil and not a measured power winding. Frontier's flipper coils are hard-wired, so the driver declares FLIP_SW(FLIP_L) without FLIP_SOL "
		f"and core_updateSw fabricates the {side} pair {address}/{pair} (CORE_L{letter}FLIPSOLBITS; core.h names {address} sL{letter}FlipPow and {pair} sL{letter}Flip) from the {side} button ({button}) "
		f"while the K1 flipper-enable relay (19) is up: both rise together, stay asserted for the whole closure and fall together, so {address} carries the same state as {pair}. "
		"The BY35 controller profile declares it as meaningful duplicate state. "
		f"In play, holding {button} raised {address} with {pair}"
		+ (", and the tilt, which dropped the relay, dropped 45 with 46." if side == "right" else ".")
		+ " The known-working script binds nothing to it."
	)
	return {
		"id": f"output.{side}-flipper-power-state",
		"label": f"{side.title()} synthetic flipper power state",
		"kind": "virtual",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases(("pinmame.coil", address)),
		"availability": "used",
		"physical": {"notes": notes},
		"provenance": prov("validated", S_CORE, S_PROFILE, S_RUNTIME),
		"spatial": not_applicable("virtual", S_CORE, S_RUNTIME),
	}


# ----------------------------------------------------------------------------------------------
# Lamps
# ----------------------------------------------------------------------------------------------

# public -> (label, connector pin, plug-connector wire, function printed on the lamp driver sheet)
LAMPS = {
	1: ("Snake (left)", "A5J1-18", "58", "SNAKE (LEFT)"),
	2: ("Hawk (left)", "A5J1-19", "60", "HAWK (LEFT)"),
	3: ("Lion (left)", "A5J1-17", "57", "LION(LEFT)"),
	4: ("Wolf (left)", "A5J1-23", "12", "WOLF(LEFT)"),
	5: ("Bear (left)", "A5J1-14", "54", "BEAR(LEFT)"),
	6: ('"A" rollover lane', "A5J1-15", "13", '"A" ROLLOVER LANE'),
	7: ("10K Frontier", "A5J1-16", "90", "10K FRONTIER"),
	8: ("50K Frontier", "A5J1-28", "78", "50K FRONTIER"),
	9: ("Left target arrow", "A5J1-24", "50", "LEFT TARGET ARROW"),
	10: ("Left thumper bumper", "A5J1-25", "75", "LEFT THUMPER BUMPER"),
	11: ("Shoot again", "A5J2-21", "47", "SHOOT AGAIN"),
	12: ("Right flipper feed lane", "A5J1-27", "53", "RIGHT FLIP. FEED LANE"),
	13: ("Ball in play", "A5J2-22", "62", "BALL IN PLAY"),
	14: ("2X drop target", "A5J2-16", "34", "2X DROP TARGET"),
	15: ("Gate arrow", "A5J2-14", "12", "GATE ARROW"),
	17: ("Snake (center)", "A5J1-1", "41", "SNAKE(CENTER)"),
	18: ("Hawk (center)", "A5J1-9", "43", "HAWK(CENTER)"),
	19: ("Lion (center)", "A5J1-8", "51", "LION(CENTER)"),
	20: ("Wolf (center)", "A5J1-3", "45", "WOLF(CENTER)"),
	21: ("Bear (center)", "A5J1-2", "52", "BEAR(CENTER)"),
	22: ('"B" rollover lane', "A5J1-10", "23", '"B" ROLLOVER LANE'),
	23: ("20K Frontier", "A5J1-7", "34", "20K FRONTIER"),
	24: ("60K Frontier", "A5J1-6", "25", "60K FRONTIER"),
	25: ("Center target arrow", "A5J1-5", "48", "CENTER TARGET ARROW"),
	26: ("Bottom thumper bumper", "A5J1-11", "65", "BOTTOM THUMPER BUMPER"),
	27: ("Match", "A5J2-8", "70", "MATCH"),
	28: ("Left flipper feed lane", "A5J1-12", "61", "LEFT FLIP. FEED LANE"),
	29: ("High score to date", "A5J2-23", "97", "HIGH SCORE TO DATE"),
	30: ("3X drop target", "A5J2-20", "35", "3X DROP TARGET"),
	31: ("2X predators", "A5J2-15", "23", "2X PREDATORS"),
	33: ("Snake (right)", "A5J3-26", "43", "SNAKE(RIGHT)"),
	34: ("Hawk (right)", "A5J3-25", "36", "HAWK (RIGHT)"),
	35: ("Lion (right)", "A5J3-19", "67", "LION(RIGHT)"),
	36: ("Wolf (right)", "A5J3-17", "13", "WOLF(RIGHT)"),
	37: ("Bear (right)", "A5J3-16", "25", "BEAR(RIGHT)"),
	38: ('"C" rollover lane', "A5J3-23", "98", '"C" ROLLOVER LANE'),
	39: ("30K Frontier", "A5J3-27", "40", "30K FRONTIER"),
	40: ("Spinner 1000", "A5J1-13", "96", "SPINNER 1000"),
	41: ("Right target arrow", "A5J3-21", "30", "RIGHT TARGET ARROW"),
	42: ("Right thumper bumper", "A5J3-20", "64", "RIGHTTHUMPER BUMPER"),
	43: ("Same player shoots again", "A5J3-22", "23", "SAME PLAYER S. A."),
	44: ("Right out special", "A5J3-24", "72", "RIGHT OUT SPECIAL"),
	45: ("Game over", "A5J2-11", "95", "GAME OVER"),
	46: ("4X drop target", "A5J2-6", "85", "4X DROP TARGET"),
	47: ("3X predators", "A5J2-2", "20", "3X PREDATORS"),
	49: ("A-B-C extra ball", "A5J3-1", "10", "A-B-C EXTRA BALL"),
	50: ("A-B-C special", "A5J3-12", "21", "A-B-C SPECIAL"),
	51: ("45K predators", "A5J3-15", "53", "45K PREDATORS"),
	52: ("4X Frontier", "A5J3-11", "20", "4X FRONTIER"),
	53: ("Predators special", "A5J3-9", "15", "PREDATORS SPECIAL"),
	54: ("4X grizzly target", "A5J3-3", "81", "4X GRIZZLY TARGET"),
	55: ("40K Frontier", "A5J3-4", "14", "40K FRONTIER"),
	56: ("30K grizzly target", "A5J3-2", "95", "30K GRIZZLY TARGET"),
	57: ("2X Frontier", "A5J3-10", "91", "2X FRONTIER"),
	58: ("3X Frontier", "A5J3-18", "56", "3X FRONTIER"),
	59: ("Credit indicator", "A5J3-13", "35", "CREDIT INDICATOR"),
	60: ("Left out special", "A5J3-14", "84", "LEFT OUT SPECIAL"),
	61: ("Tilt", "A5J2-10", "35", "TILT"),
	62: ("Special drop target", "A5J2-7", "91", "SPECIAL DROP TARGET"),
	63: ("4X predators", "A5J2-1", "60", "4X PREDATORS"),
}
BACKBOX_LAMPS = {11, 13, 27, 29, 45, 61}
# The playfield wiring sheet's stale names for the eight A5 J2 playfield lamp pins.
J2_PLAYFIELD = {63: 'CENTER "B"', 47: 'CENTER "O"', 15: 'CENTER "G"', 31: 'CENTER "L"', 14: "10K BONUS", 30: "20K BONUS", 46: "30K BONUS", 62: "40K BONUS"}
BUMPER_COLLECTIONS = {10: ("BumperLeft", "BumperLight2"), 26: ("BumperCenter", "BumperLight3"), 42: ("BumperRight", "BumperLight1")}
SWAPPED_SIDE = {
	12: ("left feed lane", "LightLeftReturnLane"),
	28: ("right feed lane", "LightRightReturnLane"),
	44: ("left outlane", "LightLeftLaneSpecial"),
	60: ("right outlane", "LightRightLaneSpecial"),
}
RUNTIME_LAMP_NOTES = {
	1: "In play the A lane lit it first in the left column.",
	2: "In play the left target lit it second in the left column.",
	3: "In play the A lane's second round lit it third in the left column.",
	6: "In play the A lane put it out.",
	7: "It was lit at the start of the game, and the first completed row of animals moved the bonus from it to 20K (23).",
	10: "In play the A lane lit it.",
	11: "The ROM lit it together with the playfield SAME PLAYER S.A. (43) when A-B-C was completed the second time.",
	12: "In play, completing A-B-C the first time lit it, and with it lit the right flipper feed lane (switch 3) scored 15,000.",
	14: "It was lit at the start of the game; the first completion of the right bank put it out and lit 30.",
	15: "In play the first in-line target lit it as the gate opened.",
	17: "In play the B lane lit it first in the centre column.",
	18: "In play the centre target lit it second in the centre column.",
	19: "In play the B lane's second round lit it third in the centre column.",
	22: "In play the B lane put it out.",
	23: "In play the first completed row of animals lit it.",
	26: "In play the B lane lit it.",
	30: "In play the first completion of the right bank lit it and the second put it out.",
	31: "In play the first completion of the right bank lit it.",
	33: "In play the C lane lit it first in the right column.",
	34: "In play the right target lit it second in the right column.",
	35: "In play the C lane's second round lit it third in the right column.",
	39: "In play the second completed row of animals lit it.",
	40: "In play the first in-line target lit it, and the spinner then scored 1,000 a closure instead of 10.",
	42: "In play the C lane lit it.",
	43: "The ROM lit it together with the back box SHOOT AGAIN (11) when A-B-C was completed the second time.",
	44: "In play, with the outlane specials lit, the right slingshot moved the lit special here from 60.",
	46: "In play the second completion of the right bank lit it.",
	47: "In play the second completion of the right bank lit it.",
	49: "In play, completing A-B-C the first time lit it and the second time put it out.",
	50: "In play, completing A-B-C the second time lit it.",
	52: "In play the grizzly target lit it.",
	54: "In play the third in-line target lit it and the grizzly target put it out.",
	55: "In play the third completed row of animals lit it.",
	56: "In play the third in-line target lit it.",
	57: "In play the second in-line target lit it and the third put it out.",
	58: "In play the third in-line target lit it and the grizzly target put it out.",
	59: "In play the left outlane's special lit it with the credit it awarded.",
	60: "In play the third completion of the right bank lit it, and with it lit the left outlane (switch 5) awarded the special.",
	61: "A tilt in play lit it.",
	62: "In play the third completion of the right bank lit it.",
	63: "In play the third completion of the right bank lit it.",
}

LAMP_CHAIN = (
	"PinMAME publishes the main lamp board as public = 16 * d + a + 1 (d the lamp-data line PD0-PD3, a the latched decoder address 0-14), and the AS-2518-23 board takes each decoder output "
	"through its own SCR to a fixed connector pin; this record takes that board chain from the Kiss record, which carries the same board and derived it from its own sheets. "
	"The function on each pin is read from Frontier's own A5 lamp driver schematic (W-1182-29c) and plug-connector sheet (W-1187-25c), which agree pin for pin."
)


def light_note(public: int) -> str:
	if public in BUMPER_COLLECTIONS:
		collection, bumper_light = BUMPER_COLLECTIONS[public]
		flags = LAMP_LIGHTS[f"L{public}"]
		assert flags["is_bulb_light"] and not flags["show_bulb_mesh"]
		return (
			f"The retained table binds Lights({public}) to its collection {collection}, which holds {bumper_light} and L{public}; both are bulb-mode lights that show no bulb mesh, "
			"and no bulb primitive of the table sits on either, so neither marks a socket and the lamp is not placed."
		)
	if public == 43:
		return "The retained table has no light L43 and its binding for 43 is commented out; it binds the back box SHOOT AGAIN (11) to a playfield light L11 instead. The lamp is not placed."
	flags = LAMP_LIGHTS[f"L{public}"]
	assert not flags["is_bulb_light"] and not flags["show_bulb_mesh"]
	text = f"The retained table binds Lights({public}) to its light L{public}, a classic light drawn over the insert, not a bulb-mode light and showing no bulb mesh, so it marks no socket and the lamp is not placed."
	if public in SWAPPED_SIDE:
		lane, comment = SWAPPED_SIDE[public]
		text += (
			f" That light sits over the {lane}, at raw x {flags['raw_x']:.0f}, and the script comments the binding {comment}: the opposite side to the factory sheets and the ROM, "
			"a defect in the table that this record does not follow."
		)
	if public == 59:
		raw = LAMP_LIGHTS["L59"]
		text += f" L59 lies outside the playfield, at raw ({raw['raw_x']}, {raw['raw_y']})."
	return text


def lamp_output(public: int) -> dict:
	label, connection, wire, printed = LAMPS[public]
	device_id = f"lamp.{slug(label)}"
	notes = [f'Connector pin {connection}, printed "{printed}" on the lamp driver sheet.']
	physical: dict = {}
	if public in BACKBOX_LAMPS:
		physical["location"] = "backglass"
		notes.append("The A5 J2 connector goes to the back box, and the plug-connector sheet's A1 insert lamp column labels this line, so it is a back box lamp with no playfield position.")
		if public == 11:
			notes.append("It is the backglass Shoot Again; the playfield SAME PLAYER S.A. insert is public 43. The retained script binds Lights(11) to a playfield light L11 above the apron, a defect in the table.")
		if public in (13, 27, 29, 45, 61):
			notes.append(f"The retained script leaves Lights({public}) commented out.")
	else:
		physical["location"] = "playfield (apron credit window)" if public == 59 else "playfield"
		if public in J2_PLAYFIELD:
			notes.append(
				"Its pin is on A5 J2, the back box connector, but the function is a playfield lamp: the plug-connector sheet's Table B routes this pin on through the panel-to-back-cab plug to the playfield, "
				f"and the A1 insert column leaves it unlabelled. The playfield wiring sheet W-1192-25c lists the same pin and wire with the stale name {J2_PLAYFIELD[public]}, a feature Frontier does not have; this record follows the lamp driver and plug-connector sheets, which the ROM supports."
			)
		if public == 30:
			notes.append(
				"The sheets disagree on its wire: the plug-connector sheet's A5 J2 block (pin 20, wire 98) and its A1 insert lamp column (wire 98 on A5J2-20) print 98, while the same sheet's Table B (A5J2-20 to plug pin 5, wire 35) "
				"and the separate playfield wiring sheet W-1192-25c (wire 35 on A5J2-20) print 35. The drive wire follows the two tables that agree, 35; the disagreement changes no lamp, and both readings stay in the excerpts."
			)
		if public == 43:
			notes.append("It is the playfield shoot-again insert, distinct from the backglass SHOOT AGAIN on public 11.")
		notes.append(light_note(public))
	if public in RUNTIME_LAMP_NOTES:
		notes.append(RUNTIME_LAMP_NOTES[public])
	notes.append(LAMP_CHAIN)
	physical["notes"] = " ".join(notes)
	wiring = {"board": "Lamp driver A5 (AS-2518-23)", "drive_connection": connection}
	if wire:
		wiring["drive_wire"] = wire
	sources = [S_SCHEMATIC, S_RUNTIME]
	if public not in BACKBOX_LAMPS and public != 43:
		sources.extend([S_SCRIPT, S_TABLE])
	item = {
		"id": device_id,
		"label": label,
		"kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": public},
		"aliases": aliases(("pinmame.lamp", public), ("manual.address", connection)),
		"availability": "used",
		"physical": physical,
		"wiring": wiring,
	}
	if public in BACKBOX_LAMPS:
		item["roles"] = ["cabinet.backglass"]
		item["provenance"] = prov("validated", S_SCHEMATIC, S_MANUAL, S_RUNTIME)
		item["spatial"] = not_applicable("cabinet_or_service", S_SCHEMATIC, S_MANUAL)
		return item
	item["provenance"] = prov("validated", *sources)
	return item


def all_outputs() -> list[dict]:
	items = [coil_output(address) for address in sorted(COILS)]
	items.extend(unused_coil(address) for address in (*UNUSED_MOMENTARY, 20))
	items.extend([flipper_state_output(45, "right"), flipper_output(46, "right"), flipper_state_output(47, "left"), flipper_output(48, "left")])
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
			"Frontier is a one-ball game with no trough: the ball drains into the outhole below the flippers, closing switch 8, and the outhole kicker (public 7) serves it to the shooter alley, where the player launches it with the plunger. "
			"The ROM adds the bonus when the ball enters the outhole and fires both drop-target resets (8, 9) with the kick; a credit with the ball in the outhole starts the game, kicks the ball, fires both resets and the saucer kicker (10) in the same step.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.in-line-drop-targets", "Three in-line drop targets and the grizzly target", "drop_target_bank", ["device.in-line-drop-target-reset"], [sid(23), sid(22), sid(21), sid(24)],
			"Three drop targets standing one behind the other along the left orbit, the 1st (switch 23) at the front to the 3rd (switch 21) at the rear, with the grizzly stand-up target (switch 24) beyond them at the end of the orbit; the ball reaches each only once the ones in front of it are down. "
			"The manual says any of them opens the gate; the first lights the spinner for 1,000, the second the Frontier 2X, the third the Frontier 3X and the grizzly target's values, and the grizzly target the Frontier 4X and 30,000. "
			"Completing the bank does not reset it: the ROM fires the shared reset coil (public 8) at power-on, at game start and at each drain.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="NO-26-1900"),
		mechanism(
			"mechanism.right-side-drop-targets", "Right-side three-bank drop targets", "drop_target_bank", ["device.right-drop-target-reset"], [sid(33), sid(34), sid(35)],
			"Three drop targets on the right side, bottom (switch 33), middle (34) and top (35), each scoring 500. Knocking all three down makes the ROM fire the shared reset coil (public 9) at once and steps the award: the Den of Predators 2X, then 3X, then 4X with the drop-target special lite, then a replay each time (manual). "
			"The outlane specials light with the second completion (option S14 on) or the third (S14 off). The ROM also fires the reset at power-on, at game start and at each drain.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="NO-26-1900"),
		mechanism(
			"mechanism.saucer", "Saucer", "kicker", ["device.saucer-kicker"], [sid(12)],
			"A saucer at the lower end of the upper-right lane. It collects the Frontier bonus (multiplied by any lit Frontier multiplier, per the manual) and the ROM kicks the ball out (public 10) straight up the lane, past the star rollover (25) and through the gate into the arch, as the manual's eject-saucer drawing shows.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AO-27-1300"),
		mechanism(
			"mechanism.saucer-lane-gate", "Saucer lane gate", "gate", ["device.gate"], [sid(25)],
			"A gate at the top of the upper-right lane, where it meets the arch. The ROM holds its coil (public 17, a continuous output) on to open it: in play from the first in-line target until the ball rolled over the saucer rollover (25), or until the drain. Option S24 keeps an open gate for the next ball. "
			"On the production ROM adding a player leaves it open; the frontieg Gate Fix ROM closes it then. The known-working table models it as an invisible one-way gate held open while 17 is on.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="GO-36-6900"),
		mechanism(
			"mechanism.thumper-bumpers", "Three thumper bumpers", "other",
			["device.left-thumper-bumper", "device.right-thumper-bumper", "device.bottom-thumper-bumper"], [sid(40), sid(39), sid(38)],
			"Two bumpers in the upper middle (left and right) and one below them in the centre. Each skirt switch makes the ROM fire its own coil: 40 fires 11, 39 fires 12 and 38 fires 13. The A, B and C lanes and their targets light the left, bottom and right bumper lamps (10, 26, 42), which the manual says score 1,000.",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AN-26-1200"),
		mechanism(
			"mechanism.slingshots", "Two slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], [sid(37), sid(36)],
			"The pair above the flippers: switch 37 makes the ROM fire the left slingshot (14) and switch 36 the right (15).",
			S_MANUAL, S_SCRIPT, S_RUNTIME, part="AO-26-1200"),
		mechanism(
			"mechanism.spinner", "Spinner", "other", [], [sid(27)],
			"A spinner right of centre below the saucer lane whose switch closes once per rotation: 10 a closure, or 1,000 once the first in-line target has lit the spinner lamp (40).",
			S_MANUAL, S_SCRIPT, S_RUNTIME),
		mechanism(
			"mechanism.flippers", "Two flippers", "other", ["device.left-flipper", "device.right-flipper", "device.k1-relay-flipper-enable"],
			["switch.left-flipper-button", "switch.right-flipper-button"],
			"Two flippers, each fired by its cabinet button. The K1 relay (public 19) switches the flipper circuits: it is raised from game start to game over and dropped by a tilt.",
			S_MANUAL, S_SCHEMATIC, S_SCRIPT, S_RUNTIME, part="AQ-25-500/34-4500"),
	]


def relationships() -> list[dict]:
	items = [
		("rel.left-slingshot", "direct", sid(37), "device.left-slingshot"),
		("rel.right-slingshot", "direct", sid(36), "device.right-slingshot"),
		("rel.left-thumper-bumper", "direct", sid(40), "device.left-thumper-bumper"),
		("rel.right-thumper-bumper", "direct", sid(39), "device.right-thumper-bumper"),
		("rel.bottom-thumper-bumper", "direct", sid(38), "device.bottom-thumper-bumper"),
		("rel.saucer", "pulse", sid(12), "device.saucer-kicker"),
		("rel.outhole", "pulse", sid(8), "device.outhole-kicker"),
		("rel.left-flipper", "relay_gated", "switch.left-flipper-button", "device.left-flipper"),
		("rel.right-flipper", "relay_gated", "switch.right-flipper-button", "device.right-flipper"),
	]
	return [{"id": rid, "kind": kind, "source": source, "destination": destination, "provenance": prov("validated", S_MANUAL, S_RUNTIME)} for rid, kind, source, destination in items]


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
		"id": "display.ball-in-play-match", "label": "Match and ball in play, two digits", "kind": "segment", "controller_index": 5, "segment_start": 38, "width": 2,
		"provenance": prov("validated", *refs), "spatial": not_applicable("cabinet_or_service", S_CORE, S_MANUAL),
	})
	return items


def drivers() -> list[dict]:
	return [
		{"id": "frontier", "description": "Frontier", "year": "1980", "manufacturer": "Bally", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "The 1980 production ROM set (U1 819-08_1.716, U2 819-07_2.716, U6 720-40_6.732, sound 819-09_4.716) and the reference for this definition: GEN_BY35, seven-digit displays (dispBy7), FLIP_SW(FLIP_L), lampCol 0, sound board SNDBRD_BY51."},
		{"id": "frontiea", "clone_of": "frontier", "description": "Frontier (Free Play)", "year": "2004", "manufacturer": "Bally / Oliver", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "A 2004 Bally/Oliver free-play ROM (rev. 1) for the production hardware, replacing U2 and U6 with frnt2732.u2 and 7406fn.u6. Its info.txt enables free play when option switches S25 and S26 are both on, which on the production ROM set the maximum credits to 40. Its retained solenoid test fires the same thirteen outputs in the same order and publishes the same sixty lamps as the production set."},
		{"id": "frontieg", "clone_of": "frontier", "description": "Frontier (Gate Fix)", "year": "2011", "manufacturer": "Bally / Scott", "flags": 0, "physical_compatibility": "identical",
		 "variant_notes": "A 2011 patch of the production U6 (720-40_6g.732) for the same hardware. PinMAME's source quotes the patch, and applying it to the retained production U6 gives the SHA-1 PinMAME lists; the new code sets the U11 PIA port B bit that PinMAME publishes as output 17, closing the gate when a game starts or a player is added. The authorized ROM library holds no frontieg set, so it was not run."},
	]


def excerpt_entries(source_id: str) -> list[dict]:
	seed = json.loads(EXCERPT_SEED_PATH.read_text(encoding="utf-8"))
	entries = []
	for item in seed["excerpts"]:
		if item["source"] != source_id:
			continue
		path = ROOT / EXCERPT_DIR / f"{item['name']}.md"
		entry = {
			"id": f"excerpt.frontier.{item['name']}",
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
		 "locator": "PinmameGetGames entries frontier, frontiea and frontieg (the last two clones of frontier)", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED_AT,
		 "locator": "src/wpc/by35games.c lines 23-26 (dispBy7 layout), 32-38 (INITGAME, INITGAME2 with BY35GD_NOSOUNDE) and 906-941 (frontier, frontieg with the quoted rec.games.pinball U6 patch, frontiea: INITGAME2 GEN_BY35, dispBy7, FLIP_SW(FLIP_L), lampCol 0, SNDBRD_BY51, machine by35_mBY35_51S); src/wpc/by35.h BY35_COMPORTS (option-switch defaults: S20 and S21 on); src/wpc/by35.c (memory map with the U11 PIA at 0x0090-0x0093, pia1b_w publishing port B bits 4-7 inverted as solenoids 17-20, by35_lampStrobe, core_updateSw(core_getSol(19))); src/wpc/core.c core_updateSw (flipper column and the synthetic flipper pairs 45/46 and 47/48), the flipMask set-up and core_swSeq2m (public n = matrix index n + 7, so 81-88 are column 11); src/wpc/core.h sLRFlipPow 45, sLRFlip 46, sLLFlipPow 47, sLLFlip 48, CORE_LRFLIPSOLBITS and CORE_LLFLIPSOLBITS, and the flipper-column bits CORE_SWLRFLIPEOSBIT to CORE_SWULFLIPBUTBIT; src/wpc/driver.c line 242",
		 "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": S_PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/by35.json", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED_AT,
		 "locator": "Controller profile pinmame.by35: public ranges for switches (-7..-5, 1..48, 81..88), option switches 1..32, solenoids 1..15, 17..20 and 45..48, and lamps; momentary address = selector + 1, continuous outputs at 17-20; the synthetic flipper pairs 45/46 and 47/48, whose 45 and 47 publish meaningful duplicate state; the generic flipper column at 81-88",
		 "license": "NOASSERTION", "attribution": "pinmame-game-defs contributors"},
		{"id": S_IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=959", "acquired_at": IPDB_ACQUIRED_AT,
		 "sha256": IPDB_SHA, "original_filename": "ipdb959.html",
		 "locator": "IPDB machine id 959: Frontier, Bally Manufacturing Corporation, project date May 19, 1980, manufactured November 1980, model number 1217 (the notes say Bally's documentation shows it without the usual -E), MPU Bally AS-2518-35, 1,850 units, 4 players; notable features 'Flippers (2), Pop bumpers (3), Slingshots (2), Standup targets (4), 3-bank drop targets (1), Spinning target (1), Kick-out hole (1), Star rollover (1), 3-in-line drop targets'; design George Christian, art Greg Freres, Margaret Hudson and Kevin O'Connor. Retained as the Internet Archive capture https://web.archive.org/web/20240204054501id_/https://www.ipdb.org/machine.cgi?id=959.",
		 "license": "NOASSERTION", "attribution": "The Internet Pinball Database", "rights": "Rights not asserted; the retained copy is the page only, kept locally for curation"},
		{"id": S_MANUAL, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/bally.frontier.1980/Bally_1980_Frontier_Manual.pdf",
		 "sha256": MANUAL_SHA, "original_filename": "Bally_1980_Frontier_Manual.pdf", "source_id": "ipdb.959", "acquired_at": MANUAL_ACQUIRED_AT,
		 "rights": "Copyright Bally Manufacturing Corporation; retained locally for curation and not redistributed",
		 "locator": "37-page image-only scan of the Bally game #1217 Frontier installation and general game operation instructions (IPDB file Bally_1980_Frontier_Manual.pdf, fetched through https://web.archive.org/web/20180815004948id_/https://www.ipdb.org/files/959/Bally_1980_Frontier_Manual.pdf). PDF pages 4-8: installation, general operation, feature operation and scoring; 6: bookkeeping; 9-12: game adjustments; 17-18: self-diagnostic tests; 21: solenoid and switch identification; 22: Figure V switch and solenoid locations; 23-24: assembly adjustments and parts list; 37: vector drawing for the eject saucer.",
		 "license": "NOASSERTION", "attribution": "Bally Manufacturing Corporation; hosted by IPDB", "excerpts": excerpt_entries(S_MANUAL)},
		{"id": S_SCHEMATIC, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/bally.frontier.1980/Bally_1980_Frontier_Schematic_Diagrams_paginated.pdf",
		 "sha256": SCHEMATIC_SHA, "original_filename": "Bally_1980_Frontier_Schematic_Diagrams_paginated.pdf", "source_id": "ipdb.959", "acquired_at": SCHEMATIC_ACQUIRED_AT,
		 "rights": "Copyright Bally Manufacturing Corporation; retained locally for curation and not redistributed",
		 "locator": "Ten scanned schematic sheets (IPDB file Bally_1980_Frontier_Schematic_Diagrams_paginated.pdf, fetched through https://web.archive.org/web/20180815004959id_/https://www.ipdb.org/files/959/Bally_1980_Frontier_Schematic_Diagrams_paginated.pdf). PDF page 7: A5 lamp driver schematic W-1182-29c; page 8: plug connectors W-1187-25c marked FRONTIER; page 10: playfield wiring sheet SWITCH MATRIX W-1192-25c (PLAYFIELD A6).",
		 "license": "NOASSERTION", "attribution": "Bally Manufacturing Corporation; hosted by IPDB", "excerpts": excerpt_entries(S_SCHEMATIC)},
		{"id": S_LIBRARY, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/frontier-1980/library/Bally.vbs",
		 "sha256": LIBRARY_SHA, "acquired_at": LIBRARY_ACQUIRED_AT,
		 "locator": f"Bally.vbs (header 'Last Updated in VBS v3.61') and core.vbs (SHA-256 {CORE_VBS_SHA}), the VPinMAME libraries the table loads, copied from the local VPinMAME scripts folder: cabinet-switch constants, flipper key handlers and the flipper solenoid constants.",
		 "license": "NOASSERTION", "attribution": "VPinMAME contributors", "excerpts": excerpt_entries(S_LIBRARY)},
		{"id": S_SCRIPT, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{SCRIPT_REVISION}/Frontier%20%28Bally%201980%29.vbs",
		 "revision": SCRIPT_REVISION, "sha256": SCRIPT_SHA, "known_working": True, "acquired_at": SCRIPT_COMMITTED_AT,
		 "locator": f"{SCRIPT_PATH}, bord's v2.0 with Thalamus's 2018 changes: cGameName frontier, SolCallback and flipper callbacks, trough, tilt and drop-target setup, switch handlers, lamp bindings and the option-switch form. The retained table embeds a script (SHA-256 {EMBEDDED_SCRIPT_SHA}) whose controller-facing lines match it apart from whitespace, sound calls, UseSolenoids (True against 2), the missing vpminit me, NoUpperRightFlipper and NoUpperLeftFlipper lines, and the position of the GameName block.",
		 "license": "NOASSERTION", "attribution": "bord, Thalamus and vpxtable_scripts contributors", "excerpts": excerpt_entries(S_SCRIPT)},
		{"id": S_TABLE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/frontier-1980/source/Frontier (Bally 1980).vpx",
		 "sha256": SEED["table_sha256"], "original_filename": "Frontier (Bally 1980).vpx", "known_working": True, "acquired_at": TABLE_ACQUIRED_AT,
		 "locator": f"bord's table (\"Sept 2016\", \"Update to 2.0 March 2017\", saved by VP 10.2), retained with its backglass Frontier (Bally 1980).directb2s (SHA-256 {DIRECTB2S_SHA}). vpxtool git:v0.33.3 extraction, canonical manifest {SEED['extraction_manifest_sha256']} ({EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes); playfield bounds left=0 top=0 right={BOUNDS['right']:g} bottom={BOUNDS['bottom']:g}, so normalized coordinates are x/{BOUNDS['right']:g} and y/{BOUNDS['bottom']:g}. Switch, coil and flipper positions are the objects the script binds, and every lamp light and bulb primitive is listed with its bulb flags (see the geometry excerpt), frozen in tools/seeds/bally/frontier-1980-spatial.json.",
		 "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "bord, Thalamus and VPX contributors", "excerpts": excerpt_entries(S_TABLE)},
		{"id": S_RUNTIME, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_SUMMARY}", "revision": PINMAME_REVISION, "sha256": file_sha256(ROOT / RUNTIME_SUMMARY), "acquired_at": RUNTIME_ACQUIRED_AT,
		 "locator": "Pinned LibPinMAME harness runs from empty NVRAM with PinMAME's default option switches: the solenoid test of frontier and frontiea paired with its displayed numbers, the switch test over all forty matrix addresses, and gameplay, tilt and gate probes of frontier. Raw runs, scenarios, pinned display readings and hashes are listed in the summary; the frontiea ROM archive's info.txt is quoted in the knowledge note.",
		 "license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	]


def build_definition() -> dict:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Frontier", "manufacturer": "Bally", "year": 1980, "kind": "physical_pinball",
			"ipdb_id": 959, "opdb_id": "GRwjq-MJwrd",
			"playfield": {"width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx", "provenance": prov("validated", S_TABLE)},
		},
		"coverage": {
			"status": "partial",
			"missing": ["input_semantics", "spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate", "physical_wiring": "validated",
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
		"knowledge": {"path": "knowledge/bally/frontier-1980.md", "status": "partial"},
		"conflicts": [],
	}


def nearest_lamp_light_to_bulbs() -> tuple[str, float]:
	"""The lamp light nearest to any bulb primitive, and its distance in table units."""
	best = min(
		(math.dist((bulb["raw_x"], bulb["raw_y"]), (light["raw_x"], light["raw_y"])), name)
		for bulb in BULB_MESHES.values() for name, light in LAMP_LIGHTS.items()
	)
	return best[1], round(best[0], 1)


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
	nearest_light, nearest_distance = nearest_lamp_light_to_bulbs()
	bulb_gi_distance = max(item["distance"] for item in BULB_MESHES.values())
	bulb_lights = sorted({item["nearest_light"] for item in BULB_MESHES.values()})
	report = {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {"space": "playfield", "x": "0=left, 1=right in player view", "y": "0=rear/backglass end, 1=apron end in player view"},
		"coverage": {"status": definition["coverage"]["status"], "missing": definition["coverage"]["missing"]},
		"definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
		"transformation": SEED["transformation"] + " Objects are frozen in tools/seeds/bally/frontier-1980-spatial.json.",
		"source_hashes": {
			"vpx_table_sha256": SEED["table_sha256"],
			"extraction_manifest_sha256": SEED["extraction_manifest_sha256"],
			"spatial_seed_sha256": file_sha256(SPATIAL_SEED_PATH),
			"manual_sha256": MANUAL_SHA,
			"schematic_sha256": SCHEMATIC_SHA,
		},
		"placement_status_counts": dict(sorted(by_status.items())),
		"not_applicable_counts": dict(sorted(not_applicable_counts.items())),
		"lamp_bulb_audit": {
			"lamp_lights": len(LAMP_LIGHTS),
			"bulb_mode_lamp_lights": sorted((name for name, item in LAMP_LIGHTS.items() if item["is_bulb_light"]), key=lambda name: int(name[1:])),
			"lamp_lights_showing_bulb_mesh": sorted((name for name, item in LAMP_LIGHTS.items() if item["show_bulb_mesh"]), key=lambda name: int(name[1:])),
			"bulb_primitives": len(BULB_MESHES),
			"bulb_primitive_nearest_lights": bulb_lights,
			"max_bulb_primitive_to_nearest_light": bulb_gi_distance,
			"nearest_lamp_light_to_any_bulb_primitive": {"light": nearest_light, "distance": nearest_distance},
		},
		"projection_disclosures": [
			{"devices": ["device.in-line-drop-target-reset"], "class": "hidden assembly projected onto the mean of the three in-line target positions sw21-sw23"},
			{"devices": ["device.right-drop-target-reset"], "class": "hidden assembly projected onto the right bank's middle target sw34"},
			{"devices": ["switch.30-point-rebound"], "class": "four parallel contacts on one address, one placement per rebound rubber wall"},
		],
		"unplaced_physical_devices": unplaced,
		"unvalidated_placements": unvalidated,
		"promotion_decision": (
			"Not promotable: no lamp light of the retained table marks a bulb (the bulb primitives all sit on general-illumination lights), so the 54 playfield lamps are unplaced, "
			"and the switch, coil and flipper placements are observed table objects that no factory-drawing check has validated."
		),
	}
	lines = [
		"# Frontier (Bally 1980) spatial blockers",
		"",
		f"Coverage: **{definition['coverage']['status']}**; missing {', '.join(f'`{m}`' for m in definition['coverage']['missing'])}.",
		"",
		f"The coordinate source is the retained `Frontier (Bally 1980).vpx` (bord v2.0) at SHA-256 `{SEED['table_sha256']}`, bounds `left=0 top=0 right={BOUNDS['right']:g} bottom={BOUNDS['bottom']:g}`, so every coordinate is x/{BOUNDS['right']:g} and y/{BOUNDS['bottom']:g} rounded to six places. "
		"The flipper pivots land at y 0.832 and the drain at 0.927.",
		"",
		f"Placements by status: {', '.join(f'{count} {status}' for status, count in sorted(by_status.items()))}. Cabinet, backglass, option-switch, unused and virtual devices carry controlled `not_applicable` records ({', '.join(f'{count} {reason}' for reason, count in sorted(not_applicable_counts.items()))}). {len(unplaced)} used devices are unplaced.",
		"",
		"## Evidence decisions",
		"",
		"- Switch, coil and flipper placements are the objects the script binds (the switch handlers, the drop-target banks, the Drain and sw12 kickers, Gate2, the flippers). Each sits where the manual's Figure V draws the part, but no callout check was made, so they stay `observed`.",
		"- Switch 1 has four rebound contacts; each rubber wall sw1a1-sw1a4 has its own placement, at the four places Figure V prints 01.",
		"- Switch 8 and the outhole kicker take the table's Drain kicker, the outhole Figure V marks; the BallRelease kicker in the shooter lane is a table helper.",
		"- The in-line drop-target reset is projected onto the mean of its three targets and the right-bank reset onto its middle target; both coils are hidden assemblies under their banks.",
		"- The gate (17) takes the table's invisible gate Gate2 at the top of the saucer lane, where Figure V prints 11.",
		"- Back box lamps 11, 13, 27, 29, 45 and 61, the knocker, the coin lockout, the K1 relay, all cabinet and service switches, the option switches, the displays and the synthetic flipper states 45 and 47 (virtual) take controlled `not_applicable` records.",
		"",
		"## Why no lamp is placed",
		"",
		f"- The table has {len(LAMP_LIGHTS)} lamp lights `L<n>`. Only {', '.join(f'`{name}`' for name in report['lamp_bulb_audit']['bulb_mode_lamp_lights'])} are bulb-mode lights (the bumper lamps, bound through the BumperLeft, BumperCenter and BumperRight collections with BumperLight1-3), and none of the lamp lights shows a bulb mesh; the rest are classic lights drawn over the inserts.",
		f"- The table models bulbs as {len(BULB_MESHES)} `BulbFil`/`BulbTop` primitives. Every one sits on a general-illumination light, a `GI_<n>` or `Light8` of the table's `GI` collection or `GI_12a`, `GI_13a` or `GI_14a` of its drop-target light collections ({', '.join(f'`{name}`' for name in bulb_lights)}), at most {bulb_gi_distance:g} units away; the nearest lamp light to any of them is `{nearest_light}`, {nearest_distance:g} units away.",
		"- A light that marks no bulb marks no socket, so the 54 playfield lamps are unplaced. A table that models the lamp bulbs, or a registered playfield photograph, would settle them.",
		"",
		"## Excluded objects",
		"",
		"- L48: a light beside the saucer rollover that the script leaves unbound; 48 is a lamp decoder hole.",
		"- The `GI_<n>` and `Light8` lights of the `GI` collection, and the `GI_12a`-`GI_14c` drop-target lights of the `DTLeftLights`/`DTRightLights` collections that the drop-target handlers and resets switch: table-side lights bound to no lamp output. Frontier has no general-illumination output; the wiring sheet feeds the G.I. from the transformer's 5.9 VAC.",
		"- BallRelease: the kicker that throws the ball into the shooter lane, a table helper.",
		"",
		"## Unplaced used devices",
		"",
		*(f"- `{item}`" for item in unplaced),
		"",
	]
	return report, chr(10).join(lines)


def build_knowledge() -> str:
	return KNOWLEDGE_SOURCE_PATH.read_text(encoding="utf-8")


def configured_vpx_sources_root() -> Path:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		raise SystemExit("PINMAME_VPX_SOURCES_ROOT is required to write or verify the retained Frontier extraction manifest")
	return Path(value).expanduser().resolve()


def verify_extraction(source_root: Path) -> str:
	extraction = source_root / EXTRACTION_RELATIVE_PATH
	digest = evidence_manifest.check_manifest(extraction, "frontier")
	manifest = json.loads((extraction / evidence_manifest.MANIFEST_FILENAME).read_text(encoding="utf-8"))
	identity = (len(manifest["files"]), sum(item["size"] for item in manifest["files"]), digest)
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise SystemExit(f"Frontier retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return digest


def shown(path: Path) -> str:
	return path.resolve().relative_to(ROOT).as_posix() if path.resolve().is_relative_to(ROOT) else str(path)


def regenerate_refusal(status: str, target: Path, explicit: bool) -> str | None:
	"""Why --regenerate must not write anything, or None. It is decided before any file is touched.

	An existing author-ready definition is never overwritten or removed: a partial build would
	delete it, and an author-ready build would replace a promoted artifact without review. An
	explicit --definition never points into the author-ready tree.
	"""
	if explicit and target.resolve().is_relative_to(AUTHOR_READY_DIR.resolve()):
		return f"refusing to regenerate: --definition {target} points into {AUTHOR_READY_DIR}"
	if AUTHOR_READY_PATH.exists():
		if status != "author_ready":
			return f"refusing to regenerate: the curator builds a {status} record, which would remove the existing author-ready definition {AUTHOR_READY_PATH}"
		return f"refusing to overwrite the existing author-ready definition {AUTHOR_READY_PATH}"
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
	mode.add_argument("--write-extraction-manifest", action="store_true", help="write the canonical manifest of the retained table extraction")
	mode.add_argument("--verify-extraction", action="store_true", help="verify the retained table extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		extraction = configured_vpx_sources_root() / EXTRACTION_RELATIVE_PATH
		print(f"Frontier extraction manifest written: {evidence_manifest.write_manifest(extraction, 'frontier')}")
		return 0
	if args.verify_extraction:
		print(f"Frontier retained extraction matches its pinned manifest identity: {verify_extraction(configured_vpx_sources_root())}")
		return 0
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
		print("Frontier definition, knowledge note and spatial report match the deterministic curator.")
		return 0
	refusal = regenerate_refusal(built["coverage"]["status"], target, args.definition is not None)
	if refusal:
		print(refusal, file=sys.stderr)
		return 1
	if args.definition is None and stale.exists():
		# Only a promotion reaches here with a stale file: the guard above refuses whenever an
		# author-ready definition exists, so the file removed is always the partial one.
		if stale != PARTIAL_PATH:
			raise SystemExit(f"refusing to remove {stale}")
		stale.unlink()
		print(f"removed {shown(stale)}")
	for path, want in outputs:
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(want)
		print(f"wrote {shown(path)}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
