#!/usr/bin/env python3
"""Curate the physical Stern Nine Ball (1980) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and retained-table coordinate is a literal in
``tools/nine_ball_data.py`` or here, and the runtime facts come from the committed compact evidence, so regeneration reproduces the canonical
definition, its pinned seed, the spatial report and the knowledge note byte for byte without reading the external evidence roots. ``--check``
refuses drift, ``--regenerate`` is the only path that writes the repository artifacts, and ``--write-extraction-manifest`` /
``--verify-extraction`` write and verify the canonical manifest of the retained table extraction under ``PINMAME_VPX_SOURCES_ROOT``.

Evidence authority follows the runbook. The two pinned known-working corpus scripts own runtime bindings, this game's own manual and four-sheet
schematic set own physical construction, wiring and device presence, pinned PinMAME owns controller topology, and the retained harness runs pair
printed numbers with public addresses. Where the machine's own sheets disagree only about a connector pin or a wire colour the disagreement is a
device note, not a conflict.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402
import nine_ball_data as data  # noqa: E402
import summarize_nine_ball_runtime as runtime_summary  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = Path("machines/partial/stern/nine-ball-1980.json")
AUTHOR_READY_PATH = Path("machines/author-ready/stern/nine-ball-1980.json")
SEED_PATH = Path("tools/seeds/stern/nine-ball-1980.json")
FRAME_READINGS_PATH = Path("tools/seeds/stern/nine-ball-1980-frame-readings.json")
KNOWLEDGE_PATH = Path("knowledge/stern/nine-ball-1980.md")
SPATIAL_REPORT_PATH = Path("reports/spatial/stern/nine-ball-1980.json")
SPATIAL_REPORT_MARKDOWN_PATH = Path("reports/spatial/stern/nine-ball-1980.md")
RUNTIME_EVIDENCE_PATH = Path("evidence/runtime/stern/nine-ball-diagnostics-and-gameplay.json")
EXCERPT_ROOT = "evidence/excerpts/stern.nine-ball.1980"

MACHINE_ID = "stern.nine-ball.1980"
PINMAME_REVISION = runtime_summary.PINMAME_REVISION
LIBRARY_SHA256 = runtime_summary.LIBRARY_SHA256
ROM_ARCHIVES = runtime_summary.ROM_ARCHIVES
CORPUS_REPOSITORY = "https://github.com/sverrewl/vpxtable_scripts"
CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_REPOSITORY = "https://github.com/jsm174/vpx-standalone-scripts"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-stern-mpu200"
MANUAL_SOURCE = "manual.stern.nine-ball.1980"
SCHEMATIC_SOURCE = "schematic.stern.nine-ball.wiring-set"
IPDB_SOURCE = "ipdb.1678"
SCRIPT_SOURCE = "vpx-script.nine-ball-corpus"
STANDALONE_SOURCE = "vpx-script.nine-ball-standalone"
TABLE_SOURCE = "vpx-table.nine-ball-bord-1-0"
TABLE_SCRIPT_SOURCE = "vpx-script.nine-ball-bord-1-0"
EXTRACTION_SOURCE = "vpx-extraction.nine-ball-bord-1-0"

MANUAL_PDF = "Stern_1980_Nine_Ball_Manual.pdf"
SCHEMATIC_PDF = "Stern_1980_Nine_Ball_Schematic_Diagrams_paginated.pdf"
MANUAL_SHA256 = "a8810a4084f36a4aac9c206238bedcc70f6ca9c6fae4198f02bfdb08ad466e01"
SCHEMATIC_SHA256 = "db81211f117f235d856702205193fd9244e4cca2cc33d5ea414d9a75f748485c"
IPDB_PAGE_SHA256 = "b109f23450652f4136a459d77a63d131b1424cd8d5cb3a7e21e516e4e90e04d9"
SCRIPT_PATH = "Nine Ball (Stern 1980).vbs"
SCRIPT_SHA256 = "ba079814b12d95496cb893954386092009da7aa14c413feebc2e941ebdde8d78"
STANDALONE_PATH = "Nine Ball (Stern 1980)/Nine Ball (Stern 1980).vbs"
STANDALONE_SHA256 = "53e98ab906854109115f19f4d006f8c7c65c6b9e38cf2446198460733bcddfa8"
STANDALONE_BLOB_SHA256 = "e727f49c8631eddf4d92056429db8d5e68d47ac331810742172c3bd13d7a5a6c"

TABLE_FILENAME = "Nine Ball (Stern 1980).vpx"
TABLE_SHA256 = "fdd7e6c53a9046e29d96b4acbbf01743d892447851b28f880df5367af2759270"
TABLE_BYTES = 83406848
TABLE_SCRIPT_SHA256 = "db63ad0f77f1361e34ee49b13ad852ae34a972de6d64c6331d1f6cfba181e902"
TABLE_RELATIVE = Path("stern/nine-ball-1980/archive")
EXTRACTION_RELATIVE = TABLE_RELATIVE / "extracted-vpxtool"
EXTRACTION_MANIFEST_RELATIVE = TABLE_RELATIVE / "extracted-vpxtool.manifest.json"
EXTRACTION_MANIFEST_SHA256 = "4a4b69caf8ad25f5e082e8581a5cbe97b9c453ea1d8b84f19d6cd309e2019f4f"
EXTRACTION_FILE_COUNT = 1303
EXTRACTION_TOTAL_BYTES = 93067588
VPXTOOL_VERSION = "git:v0.33.3"
TABLE_REFS = (TABLE_SOURCE, TABLE_SCRIPT_SOURCE)

RUN_NAMES = runtime_summary.RUN_NAMES
RUN_SOURCES = {name: f"runtime.nine-ball.{name}" for name in RUN_NAMES}
# Committer times of the pinned revisions read, and of the controller profile's last change before this curation.
PINMAME_COMMITTED = "2026-10-25T20:16:49Z"
CORPUS_COMMITTED = "2026-07-07T06:37:05Z"
STANDALONE_COMMITTED = "2026-06-20T08:33:22Z"
CONTROLLER_COMMITTED = "2026-10-15T11:04:38Z"
# When each retained raw run finished (UTC, from the retained run files).
RUN_AT = {
	"self-test": "2026-10-31T09:03:18Z", "switch-test": "2026-10-31T09:09:20Z", "solenoid-test": "2026-10-31T09:14:32Z",
	"gameplay": "2026-10-31T09:17:15Z", "game-over-and-slam": "2026-10-31T09:19:49Z", "ninebafp-variant-io": "2026-10-31T09:26:16Z",
	"ninebalb-variant-io": "2026-10-31T09:27:37Z", "kick-out-spot": "2026-10-31T09:50:43Z", "lock-lane": "2026-10-31T09:52:18Z",
	"spinner-option": "2026-10-31T10:44:00Z",
}
SELF_TEST_SOURCE = RUN_SOURCES["self-test"]
SOLENOID_TEST_SOURCE = RUN_SOURCES["solenoid-test"]
SWITCH_TEST_SOURCE = RUN_SOURCES["switch-test"]
GAMEPLAY_SOURCE = RUN_SOURCES["gameplay"]
GAME_OVER_SOURCE = RUN_SOURCES["game-over-and-slam"]
KICK_OUT_SOURCE = RUN_SOURCES["kick-out-spot"]
LOCK_LANE_SOURCE = RUN_SOURCES["lock-lane"]
SPINNER_OPTION_SOURCE = RUN_SOURCES["spinner-option"]

BOARD_MPU = "MPU module M-200 A4"
BOARD_SDU = "Solenoid Driver / Voltage Regulator module SDU B-432 A3"
BOARD_LDA = "Lamp Driver module LDA-100 B-431 A5"

# SCR -> (jack, the LDA LIGHT LOCATION list's pin, the Lamp Driver Schematic's connector-block reading) where the two sheets differ.
CONNECTOR_PIN_DISAGREEMENTS = {3: ("J2", 21, 2), 7: ("J2", 13, 3), 5: ("J2", 16, 6), 39: ("J2", 4, 1)}
# The three lamps PinMAME drove in no play run: their feature was not reached.
LAMPS_ONLY_IN_SELF_TEST_NOTE = " In the retained runs the ROM drove it only during its service tests; no play run lit it, which says nothing about its fitment."


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def normalize(x: float, y: float) -> tuple[float, float]:
	return round(x / data.TABLE_WIDTH, 6), round(y / data.TABLE_HEIGHT, 6)


def object_point(names: list[str]) -> tuple[float, float]:
	"""The mean of the named objects' raw centres; one name gives that object's own centre."""
	points = [data.OBJECTS[name][1:3] for name in names]
	return sum(x for x, _ in points) / len(points), sum(y for _, y in points) / len(points)


def located(identifier: str, role: str, groups: list[list[str]], *source_refs: str) -> dict[str, Any]:
	"""One placement per object group; a group of several objects is placed at their mean (a projection)."""
	placements = []
	for index, names in enumerate(groups, start=1):
		x, y = normalize(*object_point(names))
		suffix = f".{index}" if len(groups) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y,
			"provenance": provenance(*source_refs, status="observed")})
	return {"status": "observed", "placements": placements}


def legacy_numeric(address: int) -> list[str]:
	"""The legacy corpus exposed each address bare, then two-digit, then three-digit."""
	return list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))


def runtime_document(root: Path = ROOT) -> dict[str, Any]:
	return load_json(root / RUNTIME_EVIDENCE_PATH)


def runs_exercising_switch(observations: dict[str, Any], address: int) -> list[str]:
	"""The retained runs whose host actions closed or pulsed ``address``."""
	return [RUN_SOURCES[name] for name in RUN_NAMES
		if any(item["input_kind"] == "switch" and item["input_address"] == address for item in observations["runs"][name].get("named_action_observations", []))]


def runs_seeing_solenoid(observations: dict[str, Any], address: int) -> list[str]:
	return [RUN_SOURCES[name] for name in RUN_NAMES if address in observations["runs"][name].get("solenoid_addresses_seen", [])]


def runs_seeing_lamp(observations: dict[str, Any], address: int) -> list[str]:
	"""The burn-in drives all sixty lamps; the gameplay run drives every lamp any play run drives (the summarizer refuses otherwise)."""
	refs = [SELF_TEST_SOURCE] if address in observations["lamp_addresses_seen"] else []
	if address in observations["lamp_addresses_driven_outside_self_test"]:
		refs.append(GAMEPLAY_SOURCE)
	if address in {value for key, value in observations["named_output_addresses"].items() if key.startswith("lock-lane-object-")}:
		refs.append(LOCK_LANE_SOURCE)
	if address in (12, 28):
		refs.append(SPINNER_OPTION_SOURCE)
	return refs


# --- Inputs -------------------------------------------------------------------------------------------------------------


def matrix_wiring(address: int, cabinet: bool) -> dict[str, Any]:
	strobe, row = (address - 1) // 8, (address - 1) % 8
	strobe_wire, strobe_connection = data.CABINET_STROBE0 if cabinet else data.STROBES[strobe]
	return_wire, return_connection = data.CABINET_RETURNS[row] if cabinet else data.RETURNS[row]
	return {"board": BOARD_MPU, "control_wire": strobe_wire, "control_connection": strobe_connection, "return_wire": return_wire, "return_connection": return_connection}


def switch_construction(address: int, cabinet: bool) -> str:
	if address in data.NO_DIODE_SWITCHES:
		text = "Normally open contact with no series diode (Switch I.D. legend `SWS. #1, 2, & 3 NO DIODE`)"
	else:
		text = "Normally open contact with a series 1N4004 diode (Switch I.D. legend `ALL OTHER SWITCHES USE DIODE IN4004`)"
	if address in data.CAPACITOR_SWITCHES:
		text += ", and a .05 capacitor across it: the Switch I.D. marks its row with the filled dot of `SYMBOL IF .05 CAP IS USED`" + ("" if cabinet else " and the playfield sheet draws the capacitor below the contact")
	return text + "."


def build_inputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	inputs: list[dict[str, Any]] = []
	for address, spec in sorted(data.SERVICE_SWITCHES.items()):
		refs = {"manual-and-harness": (MANUAL_SOURCE, CORE_SOURCE, SELF_TEST_SOURCE, SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE), "core": (CORE_SOURCE,)}[spec["evidence"]]
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": spec["availability"],
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"normally_closed": False,
			"physical": {"location": spec["location"], "notes": spec["notes"], "switch_type": "button"},
			"provenance": provenance(*refs),
			"pulse": False,
			"roles": spec["roles"],
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		})

	for address in sorted(data.SWITCHES):
		spec = data.SWITCHES[address]
		cabinet = bool(spec.get("cabinet"))
		aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.switch", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.self-test", "value": str(address)})
		refs = [MANUAL_SOURCE, SCHEMATIC_SOURCE, SWITCH_TEST_SOURCE, *runs_exercising_switch(observations, address)]
		if not cabinet:
			refs += [SCRIPT_SOURCE, STANDALONE_SOURCE]
		physical: dict[str, Any] = {"switch_type": spec["type"]}
		if spec.get("quantity"):
			physical["quantity"] = spec["quantity"]
		sheet = f"playfield sheet: `{spec['matrix']}`" if spec["matrix"] else "the playfield sheet draws an unlabelled contact at this matrix position"
		physical["notes"] = f"Switch I.D. table: `{spec['printed']}`; {sheet}. {switch_construction(address, cabinet)} " + spec["notes"]
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"normally_closed": False,
			"physical": physical,
			"provenance": provenance(*refs),
			"pulse": bool(spec.get("pulse", False)),
			"wiring": matrix_wiring(address, cabinet),
		}
		if spec.get("initial_active"):
			item["initial_active"] = True
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if cabinet:
			physical["location"] = "Coin door and cabinet"
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, SCHEMATIC_SOURCE)
		elif address in data.SWITCH_OBJECTS:
			names, projection = data.SWITCH_OBJECTS[address]
			item["spatial"] = located(spec["id"], "sensor", [[name] for name in names], *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SCRIPT_SOURCE]))
			if address in (38, 39):
				physical["notes"] += " " + projection
			else:
				physical["notes"] += " Placed on the retained table's " + " and ".join(f"{data.OBJECTS[name][0]} `{name}`" for name in names) + ", which its script binds to this address."
				if projection:
					physical["notes"] += " " + projection
		else:
			physical["location"] = "Ball trough under the apron"
			physical["notes"] += (" Not placed: both known-working scripts and the retained table model the trough as a virtual ball stack (`bsTrough.InitSw 0,33,36,37`) fed by a drain kicker, "
				"so no table object marks this switch, and the location drawing prints 37, 36 and 33 under the apron without arrows.")
		inputs.append(item)

	for address, (identifier, label, role, wire, connection) in sorted(data.FLIPPER_BUTTONS.items()):
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": identifier,
			"kind": "switch",
			"label": label,
			"normally_closed": False,
			"physical": {
				"location": "Cabinet side",
				"notes": "PinMAME's synthetic cabinet flipper button position (FLIP_SW(FLIP_L)). The physical button is hard-wired through the flipper enable relay's contact to its side's flipper coil, "
					"not to the switch matrix, so the switch test does not show it (manual: `Flipper Button and flipper End of Stroke switches are not included`). The flipper wiring page draws the button's "
					f"lead `-{wire}-` from {connection} and the two buttons' common `-O-` to `RECT. BRD.` `J2-9`. The retained gameplay runs show PinMAME's flipper outputs answering this address.",
				"quantity": 1,
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, *runs_exercising_switch(observations, address)),
			"pulse": False,
			"roles": [role],
			"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
			"wiring": {"board": "Hard-wired flipper button circuit through the SDU flipper enable relay", "control_wire": wire, "control_connection": connection,
				"return_wire": "O", "return_connection": "RECT. BRD. J2-9"},
		})
	for address, (identifier, label) in sorted(data.UNUSED_FLIPPER_POSITIONS.items()):
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": "unused",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": identifier,
			"kind": "switch",
			"label": label,
			"normally_closed": False,
			"physical": {
				"notes": "PinMAME's generic upper flipper button position. Nine Ball has one flipper per side (parts list `Flippers (2)`; the flipper wiring page's solid lines draw one per side) and the driver "
					"declares FLIP_SW(FLIP_L) only, so no button reaches this position; pressing it changed no flipper output in the retained gameplay run.",
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE),
			"pulse": False,
			"spatial": not_applicable("unused", MANUAL_SOURCE, CORE_SOURCE),
		})

	for address in sorted(data.DIPS):
		conflicted = address == 8
		refs = [MANUAL_SOURCE, CORE_SOURCE] + ([SPINNER_OPTION_SOURCE] if address == 17 else []) + ([GAME_OVER_SOURCE] if address == 7 else [])
		inputs.append({
			"aliases": [{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": "S%d" % address}],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.dip"},
			"id": "dip.option-switch-%d" % address,
			"kind": "dip_switch",
			"label": data.DIPS[address],
			"physical": {
				"location": "MPU module option-switch packages in the backbox",
				"notes": "One of the thirty-two MPU option switches in the four sixteen-lead packages S1-8, S9-16, S17-24 and S25-32, with the ON position marked on the assembly (manual Figure 1 and page 12). "
					"The assignment is the `NINE BALL SWITCH ASSIGNMENTS` page and the adjustment tables of PDF pages 12-15; every one of the 32 is assigned. PinMAME's default setting is OFF for all of them, "
					"and the retained runs at that default play three-ball games, which the manual prints as switch 7 OFF. S33 on the same module is a momentary memory-clear pushbutton, not an option switch."
					+ {8: " The two pages print opposite settings for this switch; see the conflict record.",
						17: " PDF page 14 prints the reverse of PDF page 11. The retained spinner-option run, with the switch at its default OFF, advanced the spinner value lamps for the two center targets "
							"19 and 23 and not for the outside targets 18, 20 and 22, which is the setting PDF page 11 prints for OFF."}.get(address, ""),
				"switch_type": "dip",
			},
			"provenance": provenance(*refs, status="conflicted" if conflicted else "validated"),
			"spatial": not_applicable("dip_switch", MANUAL_SOURCE),
		})

	for side, address, button in (("left", 1, 84), ("right", 2, 82)):
		identifier = f"switch.{side}-flipper-end-of-stroke-contact"
		obj = data.DIRECT_OBJECTS[address]
		inputs.append({
			"aliases": [{"namespace": "manual.address", "value": f"{side}-flipper-eos"}],
			"availability": "used",
			"binding": {"device": address, "group": "physical.input.direct"},
			"id": identifier,
			"kind": "switch",
			"label": f"{side.title()} flipper end-of-stroke contact",
			"normally_closed": True,
			"physical": {
				"location": f"{side.title()} flipper assembly",
				"notes": "Hard-wired contact of the dual-winding flipper coil, not a PinMAME switch address. The manual's flipper wiring page draws it as the `E.O.S.` contact across the coil's first winding, "
					"conducting at rest and opening at the end of the stroke to insert the second winding (normally closed); the playfield sheet draws the same contact across one of the two windings. "
					"The dashed `EXTRA FLIPPER` and its `E.O.S.` `B` contact on the same page are a generic option for more than one flipper per side and are not fitted on Nine Ball. "
					f"Placed by projection on the retained table's `{obj}` pivot, because the contact is mounted on its flipper assembly and has no object of its own.",
				"quantity": 1,
				"switch_type": "leaf",
			},
			"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE),
			"pulse": False,
			"spatial": located(identifier, "sensor", [[obj]], TABLE_SOURCE, MANUAL_SOURCE),
		})
	inputs.append({
		"aliases": [{"namespace": "manual.address", "value": "remote-s33"}],
		"availability": "used",
		"binding": {"device": 3, "group": "physical.input.direct"},
		"id": "switch.remote-memory-clear",
		"kind": "switch",
		"label": "Remote S33 memory clear button (coin door)",
		"normally_closed": False,
		"physical": {
			"location": "Inside the coin door",
			"notes": "Figure 1 draws `S-33 (MEMORY CLEAR)` on the MPU and a second `(MEMORY CLEAR) S-33` on the front door, and the adjustment text says the high game to date `Can be quickly set to "
				"'00' by pressing S33 on the MPU assembly in the back box or front door`. It reaches the MPU's memory-clear input rather than a matrix position. This game's schematic set has no cabinet "
				"wiring sheet, so no connector or wire is asserted for it. This profile-local physical binding has no controller transport, and no ROM effect is claimed from a host write.",
			"switch_type": "button",
		},
		"provenance": provenance(MANUAL_SOURCE),
		"pulse": False,
		"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE),
	})
	return inputs


# --- Outputs ------------------------------------------------------------------------------------------------------------


def build_solenoid_outputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	outputs: list[dict[str, Any]] = []
	public_to_physical = {public: number for number, public in data.PHYSICAL_TO_PUBLIC.items()}
	for address, spec in sorted(data.SOLENOIDS.items()):
		physical_number = public_to_physical[address]
		transistor, jack, wire, printed = data.PRINTED_SOLENOIDS[physical_number]
		if transistor != f"Q{physical_number}":
			raise RuntimeError(f"solenoid {physical_number}: the printed table names transistor {transistor}")
		if "object" in spec and printed != f"DROP TARGET #{spec['object']}":
			raise RuntimeError(f"public {address}: the ROM test pairs printed `{printed}`, not object {spec['object']}")
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)]
		aliases += [{"namespace": "manual.self-test", "value": str(physical_number)}, {"namespace": "manual.address", "value": f"SDU-Q{physical_number}"}]
		refs = [MANUAL_SOURCE, SCHEMATIC_SOURCE, *runs_seeing_solenoid(observations, address)]
		if address not in (18,):
			refs += [SCRIPT_SOURCE, STANDALONE_SOURCE]
		physical: dict[str, Any] = {}
		if spec.get("part"):
			physical["part_number"] = spec["part"]
			physical["quantity"] = 1
		physical["notes"] = (f"SDU driver {transistor}, printed solenoid {physical_number} `{printed}` ({jack}, {wire}); the ROM's solenoid test shows {physical_number} while public {address} fires. "
			+ spec["notes"])
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": spec["kind"],
			"label": spec["label"],
			"physical": physical,
			"provenance": provenance(*refs),
			"wiring": {"board": BOARD_SDU, "driver_transistor": transistor, "drive_connection": f"A3{jack}", "drive_wire": wire, "nominal_voltage_v": 43, "voltage_type": "dc"},
		}
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if spec.get("cabinet"):
			physical["location"] = "Cabinet"
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif spec.get("internal"):
			physical["location"] = "Solenoid driver board in the backbox"
			item["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, SCHEMATIC_SOURCE)
		elif address in data.SOLENOID_OBJECTS:
			names, projection = data.SOLENOID_OBJECTS[address]
			groups = [names] if projection and len(names) > 1 else [[name] for name in names]
			item["spatial"] = located(spec["id"], "effect", groups, *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SOURCE, TABLE_SCRIPT_SOURCE]))
			if projection:
				physical["notes"] += " " + projection
			elif address == 5:
				physical["notes"] += " Placed on the retained table's Bumper `sw31`, the pop bumper this coil fires."
			else:
				physical["notes"] += f" Placed on the retained table's {data.OBJECTS[names[0]][0]} `{names[0]}`, which its script drives from this address."
		else:
			physical["location"] = "Under the apron"
			physical["notes"] += (" Not placed: the solenoid location drawing points at the outhole under the apron, but both known-working scripts and the retained table kick a virtual ball "
				"stack into the shooter lane from a `BallRelease` kicker, so no table object marks the coil.")
		outputs.append(item)

	for address, spec in sorted(data.FLIPPERS.items()):
		power = spec["power"]
		outputs.append({
			"aliases": [
				{"namespace": "pinmame.solenoid", "value": str(address)},
				*({"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)),
			],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": "coil",
			"label": spec["label"],
			"physical": {
				"part_number": "J-25-475/34-4500",
				"quantity": 1,
				"notes": f"The {spec['side']} flipper (parts list `Flippers (2)` J-25-475/34-4500; playfield parts `Flipper Assembly B-634-R-Y and B-634-L-Y`) is a dual-winding coil hard-wired from the "
					f"+43 VDC supply A2J1-6 (BLU-W, fuse F4) through the flipper enable relay's `{spec['side'].upper()} FLIPPER SW.` contact to the {spec['side']} cabinet button; no numbered solenoid "
					f"transistor drives it. The playfield sheet prints its return as {spec['conn']} ({spec['wire']}) and the flipper wiring page as `SDU J1-{spec['conn'][-1]}`. Public {address} is PinMAME's "
					f"synthetic held-coil output for the {spec['side']} side (FLIP_SW(FLIP_L)); PinMAME also asserts public {power} for the same interval. Both outputs are button states, not measurements "
					f"of either winding. Placed on the retained table's `{spec['object']}` pivot, which its flipper callback moves.",
			},
			"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, *runs_seeing_solenoid(observations, address), SCRIPT_SOURCE, STANDALONE_SOURCE, TABLE_SCRIPT_SOURCE),
			"spatial": located(spec["id"], "effect", [[spec["object"]]], *TABLE_REFS, MANUAL_SOURCE),
			"wiring": {
				"board": "Hard-wired flipper circuit gated by the flipper enable relay (public 19)",
				"control_connection": spec["button_conn"],
				"control_wire": spec["button_wire"],
				"drive_connection": spec["conn"],
				"drive_wire": spec["wire"],
				"nominal_voltage_v": 43,
				"power_connection": "A2J1-6",
				"power_wire": "BLU-W",
				"voltage_type": "dc",
			},
		})
		outputs.append({
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(power)}],
			"availability": "used",
			"binding": {"device": power, "group": "pinmame.output.solenoid"},
			"id": f"output.{spec['side']}-flipper-power-state",
			"kind": "virtual",
			"label": f"{spec['side'].title()} synthetic flipper power state",
			"physical": {"notes": f"PinMAME's synthetic power-winding state for the {spec['side']} side, asserted and released together with public {address} for the whole enabled button closure "
				"(retained gameplay runs). It is not another coil and does not measure the power winding."},
			"provenance": provenance(CORE_SOURCE, *runs_seeing_solenoid(observations, power)),
			"spatial": not_applicable("virtual", CORE_SOURCE, GAMEPLAY_SOURCE),
		})
	return outputs


def lamp_rows() -> dict[int, tuple[str, str, str, int, int]]:
	"""Public lamp address -> its LDA LIGHT LOCATION row (description, wire, jack, pin, SCR)."""
	q_to_public = {q: public for public, q in data.LAMP_TO_Q.items()}
	rows: dict[int, tuple[str, str, str, int, int]] = {}
	for description, wire, jack, pin, transistor in data.LAMP_LIST:
		q = int(transistor[1:])
		public = q_to_public[q]
		if public in rows:
			raise RuntimeError(f"two LDA rows name SCR Q{q}")
		rows[public] = (description, wire, jack, int(pin), q)
	if set(rows) != set(data.LAMP_TO_Q) or len(data.LAMP_LIST) != 60:
		raise RuntimeError("Nine Ball's LDA LIGHT LOCATION list does not name the sixty SCR outputs once each")
	return rows


def build_lamp_outputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	rows = lamp_rows()
	named = {int(key.split("-")[3]): value for key, value in observations["named_output_addresses"].items() if key.startswith("lock-lane-object-")}
	for index, public in named.items():
		if rows[public][0] not in (f"BONUS TARGET {index}", f"BONUS TARGET {index} & CAPTURE BALL"):
			raise RuntimeError(f"the ROM's object {index} bonus lamp is public {public}, whose printed row is `{rows[public][0]}`")
	outside = set(observations["lamp_addresses_driven_outside_self_test"])
	outputs: list[dict[str, Any]] = []
	for address in sorted(data.LAMP_TO_Q):
		description, wire, jack, pin, q = rows[address]
		k, a = divmod(address - 1, 16)
		identifier, label = data._lamp_identity(description)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.lamp", "value": value} for value in legacy_numeric(address)]
		aliases += [{"namespace": "manual.address", "value": f"LDA-Q{q}"}, {"namespace": "manual.address", "value": f"LDA-{jack}-{pin}"}]
		notes = (f"Lamp Driver SCR Q{q}, decoder U{k + 1} output S{a}, resistor R{q}; a discrete SCR output on the LDA-100, not a lamp matrix. Printed load: `{description}` ({wire}, LDA {jack} pin {pin}), "
			"the game's own `NINE BALL LDA LIGHT LOCATION` list.")
		if q in CONNECTOR_PIN_DISAGREEMENTS:
			_, listed, drawn = CONNECTOR_PIN_DISAGREEMENTS[q]
			notes += (f" The Lamp Driver Schematic's connector block prints this SCR on {jack} pin {drawn}; the definition follows the game's own list ({jack}-{listed}), a connector-pin reading only.")
		if description in data.TWO_FEATURE_ROWS:
			notes += " The row names two features on this one output; how many bulbs they light is not printed, so no quantity is asserted."
		if address in named.values():
			index = next(number for number, public in named.items() if public == address)
			notes += f" The ROM proves the pairing: in the retained lock-lane run this was the lamp lit for object {index}, in the order the objects were made."
		if address not in outside:
			notes += LAMPS_ONLY_IN_SELF_TEST_NOTE
		refs = [SCHEMATIC_SOURCE, *runs_seeing_lamp(observations, address)]
		physical: dict[str, Any] = {"part_number": "#44 (8A-101)", "notes": notes}
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.lamp"},
			"id": identifier,
			"kind": "lamp",
			"label": label,
			"physical": physical,
			"provenance": provenance(*refs),
			"wiring": {"board": BOARD_LDA, "driver_transistor": f"Q{q}", "drive_connection": f"A5{jack}-{pin}", "drive_wire": wire},
		}
		if description in data.BACKBOX_ROWS:
			physical["location"] = "Backbox"
			physical["notes"] += (" A backbox lamp: the row names a backglass feature (the operating text names the `\"HIGH SCORE\" lite`, the `\"Game Over\" light` and the `\"Match\" light` among "
				"the backglass indications), and the retained table has no light at this lamp number.")
			item["roles"] = ["cabinet.backglass"]
			item["spatial"] = not_applicable("cabinet_or_service", SCHEMATIC_SOURCE, MANUAL_SOURCE)
			refs.append(MANUAL_SOURCE)
			item["provenance"] = provenance(*refs)
		else:
			physical["notes"] += (" Not placed: the retained table, the only one available, draws this insert with lights that show no bulb mesh, and the manual prints no lamp-location drawing, "
				"so no source marks the socket.")
			if description == "SHOOT AGAIN":
				physical["notes"] += (" The table draws two playfield lights (`l27`, `l27b`) for it; whether the backglass also carries a shoot-again lamp on this output is not printed.")
			refs += [SCRIPT_SOURCE, STANDALONE_SOURCE, TABLE_SCRIPT_SOURCE]
			item["provenance"] = provenance(*refs)
		outputs.append(item)
	return outputs


def build_gi() -> dict[str, Any]:
	placements = []
	for index, (name, (x, y, light)) in enumerate(sorted(data.GI_BULBS.items(), key=lambda entry: int(entry[0][7:])), start=1):
		nx, ny = normalize(x, y)
		placements.append({"id": f"gi.general-illumination.emitter.{index}", "role": "emitter", "space": "playfield", "x": nx, "y": ny,
			"provenance": provenance(TABLE_SOURCE, status="observed")})
	return {
		"aliases": [],
		"availability": "used",
		"binding": {"device": 1, "group": "physical.output.gi"},
		"id": "gi.general-illumination",
		"kind": "gi",
		"label": "Uncontrolled general illumination",
		"physical": {
			"notes": "Transformer-fed general illumination with no controller address. The playfield sheet draws `GEN. ILLUM.` from A2J1-8 (W) at 6 VAC returning on A2J1-1 (R); the shared transformer "
				"schematic takes the cabinet `GEN. ILL. BUS` from J2-1 (Y-B, return J2-5 G-R) and the backbox buses from J3-10 (O) and J3-11 (R) (returns J3-1 G and J3-2 W), off a 7.3 VAC winding through fuse "
				"F5 (20 A). No relay, transistor or other switching device is drawn in any of these lines. No sheet prints a bulb count or position; the parts list gives only `Bulb, #44 8A-101`. "
				f"Placed on the {len(placements)} bulb-filament primitives `BulbFil1`-`BulbFil{len(placements)}` of the retained table, each with one of its `GI_<n>` lights at its centre; the table's "
				"grouping is render membership, not the machine's wiring, so no quantity is asserted, and its backbox and cabinet bulbs are not placed.",
		},
		"provenance": provenance(SCHEMATIC_SOURCE, MANUAL_SOURCE, TABLE_SOURCE),
		"spatial": {"status": "observed", "placements": placements},
		"wiring": {"board": "Transformer/rectifier A2, uncontrolled general-illumination buses", "power_connection": "A2J1-8 (playfield); J2-1 (cabinet); J3-10, J3-11 (backbox)",
			"return_connection": "A2J1-1; J2-5; J3-1, J3-2", "voltage_type": "ac", "nominal_voltage_v": 6},
	}


def build_outputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	outputs = build_solenoid_outputs(observations) + build_lamp_outputs(observations) + [build_gi()]
	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return outputs


# --- Mechanisms, relationships --------------------------------------------------------------------------------------------


def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *sources: str, part: str | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {"actuators": actuators, "behavior": behavior, "id": identifier, "kind": kind, "label": label, "provenance": provenance(*sources), "sensors": sensors}
	if part:
		item["assembly_part_number"] = part
	return item


KNOCK_DOWN = {spec["object"]: address for address, spec in data.SOLENOIDS.items() if "object" in spec}


def build_mechanisms() -> list[dict[str, Any]]:
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	return [
		mechanism(
			"mech.outhole-trough", "Three-ball outhole trough and shooter feed", "kicker", ["device.outhole-kicker"], ["switch.outhole", "switch.middle-outhole", "switch.left-outhole"],
			"Three trough switches under the apron, printed 37, 36 and 33 from left to right on the location drawing; the ball at the right end rests on the outhole switch (public 33) in front of the "
			"outhole kicker (public 7, `Outhole Kicker` J-26-1200), and the other two wait on 36 and 37. The known-working scripts start with all three balls in the trough. Pressing the credit button resets "
			"the drop targets and the outhole kicker moves the ball to the shooter lane (manual); in the retained runs the ROM fires the eight-bank reset (17), both three-bank resets (3, 4) and the outhole "
			"kicker (7) together and repeats them about every 1.2 s while 33 stays closed. After a drain the bonus times the multiplier is collected, the ball and player advance and the next ball is served "
			"the same way; an extra ball is played without advancing. Both scripts model the trough as a virtual ball stack and serve from a shooter-lane kicker.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE,
		),
		mechanism(
			"mech.kick-out-hole-and-lock-lane", "Left lane kick-out hole and three-ball lock lane", "kicker", ["device.kick-out-hole"],
			["switch.kick-out-hole", "switch.left-lane-middle", "switch.left-lane-top"],
			"A kick-out hole (switch 34, coil public 8, `Lane Kicker` J-28-2300) at the foot of the left lane, with the lane's middle (38) and top (39) switches above it, each closed by a ball resting "
			"behind the one below. Before object 5 is lit the ROM spots the lit objects with the knock-down coils, waiting for each target's switch before it fires the next, then ejects the ball and resets "
			"the eight-bank (retained kick-out-spot run). Once object 5 is lit the hole captures the ball: the ROM spots, keeps the ball and serves another from the trough; a ball on 38 behind it is captured "
			"the same way, and a third ball on 39 releases all three, the ROM firing public 8 once for each ball as it drops onto 34 (retained lock-lane run; manual: `Making Object No. 9 or capturing all 3 "
			"balls will release all captured balls for play`). Capturing on 34 or 38 can award a shoot-again (manual). Home state: empty.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, KICK_OUT_SOURCE, LOCK_LANE_SOURCE,
		),
		mechanism(
			"mech.eight-target-bank", "Left eight-target drop bank (two four-target banks, programmable)", "drop_target_bank",
			["device.eight-bank-reset", *(data.SOLENOIDS[KNOCK_DOWN[number]]["id"] for number in sorted(KNOCK_DOWN))],
			[switch_id[8 + number] for number in range(1, 9)],
			"Two four-target banks along the left side on one reset coil (`8 Bank Drop Target D-548-9B`; reset public 17, B-24-1600): the upper bank carries objects 2, 4, 6 and 8 from the top (switches 10, 12, "
			"14 and 16) and the lower bank objects 7, 5, 3 and 1 (switches 15, 13, 11 and 9). A target's switch is closed while it is down. Objects 1-7 each have a `Drop Target (Programmable)` knock-down coil "
			"(C1-34-3400) that the ROM fires to put the target down: object k's coil is public 16-k (9 for object 7 up to 15 for object 1); object 8 has none. Home state: all eight up. The game is played "
			"in order: hitting the lit object scores it, advances the bonus and lights the next; when the lit object is made the ROM resets the bank within about 35 ms and knocks the objects made so far down "
			"again, lowest first, each coil fired only after the previous target's switch has closed (retained runs). Lighting object 5 makes the kick-out hole capture; making all eight in order lights the "
			"object 9 target and WOW; later rounds light Special and exclude one more low object each time (manual).",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, KICK_OUT_SOURCE, LOCK_LANE_SOURCE, part="D-548-9B",
		),
		mechanism(
			"mech.center-three-bank", "Center (top) three-target drop bank", "drop_target_bank", ["device.center-bank-reset"], [switch_id[18], switch_id[19], switch_id[20]],
			"Three drop targets at the top centre (switches 18, 19, 20 left to right; `3 Bank Drop Target D-580-3J`) on one reset coil (public 4, B-27-2300); no knock-down coils. Home state: all up. "
			"With option switch 14 OFF the ROM resets both three-banks only after all six targets are down (retained gameplay run: public 4 and 3 fire on the sixth); with it ON one bank resets at random "
			"(manual note 3). The targets score 1,000 or 7,000, completing a bank advances the multiplier, the outside targets award WOW when lit and the targets option switch 17 selects advance the "
			"spinner value.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, SPINNER_OPTION_SOURCE, part="D-580-3J",
		),
		mechanism(
			"mech.right-three-bank", "Right three-target drop bank", "drop_target_bank", ["device.right-bank-reset"], [switch_id[22], switch_id[23], switch_id[24]],
			"Three drop targets on the right (switches 22, 23, 24 top to bottom; `3 Bank Drop Target D-580-3J`) on one reset coil (public 3, B-27-2300); no knock-down coils. Home state: all up. It resets "
			"together with the center bank as that record describes, and scores the same way.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, SPINNER_OPTION_SOURCE, part="D-580-3J",
		),
		mechanism(
			"mech.loop-drop-target", "Single loop drop target", "drop_target_bank", ["device.loop-drop-target-reset"], [switch_id[21]],
			"One drop target below the top-left loop (switch 21; `1 Drop Target C-383-3`) raised by public 20 (Q18, the solenoid table's `LOOP DROP TARGET`). Home state: up. Knocking it down collects and "
			"resets the loop value (manual); in the retained gameplay run the ROM pulsed public 20 about 2.6 s after switch 21 closed and again after the target came back up.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, part="C-383-3",
		),
		mechanism(
			"mech.top-left-loop", "Top-left loop with roll-under gate", "gate", [], [switch_id[4], switch_id[32]],
			"The loop at the top left is entered under a roll-under gate (`Roll-Under Gate Assembly A-791`) whose switch is public 4; the loop's exit passes the loop drop target. The roll-under and the "
			"left lane lower switch (32) score 3,000 and advance the loop value (lamps LOOP 10K to the top value), which the loop target and a lit outlane collect (manual; retained gameplay run). No coil.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.spinner", "Right spinning target", "other", [], [switch_id[5]],
			"A spinning target across the right lane (`Spin Target Assembly A-792`); each rotation closes switch 5 once and scores 100 or the highest lit spinner value, and any spin resets the value. The "
			"value advances on the three-bank targets option switch 17 selects and goes to the top on the advance-spinner stand-up (35). No coil or home sensor.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, GAMEPLAY_SOURCE, SPINNER_OPTION_SOURCE,
		),
		mechanism(
			"mech.pop-bumper", "Pop (thumper) bumper", "kicker", ["device.pop-bumper"], [switch_id[31]],
			"One thumper bumper below the top bank (`Thumper Bumper J-26-1200`). The ROM fires public 5 when switch 31 closes (retained gameplay runs); scores 100 or the highest lit spinner value (manual).",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], [switch_id[30], switch_id[29]],
			"Two J-26-1600 slingshots. The ROM fires each coil when its switch closes: left switch 30 fires public 2 and right switch 29 public 1 (retained gameplay runs). Printed solenoid numbers are 1 (left) "
			"and 2 (right). Each scores 10.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, GAMEPLAY_SOURCE, SOLENOID_TEST_SOURCE,
		),
		mechanism(
			"mech.flippers", "Two dual-winding flippers", "other", ["device.left-flipper", "device.right-flipper", "device.flipper-enable-relay"],
			["switch.left-flipper-button", "switch.right-flipper-button", "switch.left-flipper-end-of-stroke-contact", "switch.right-flipper-end-of-stroke-contact"],
			"One flipper per side (`Flippers (2)` J-25-475/34-4500), each a dual-winding coil fed from +43 VDC (A2J1-6, fuse F4) through a contact of the flipper enable relay (public 19, printed solenoid 15, "
			"CR20 across its coil) to the side's cabinet button. The ROM energizes the relay when a game starts and drops it on a tilt and at game over (retained runs). Each coil's end-of-stroke contact is "
			"closed at rest and opens at the end of the stroke to insert the hold winding. PinMAME publishes 46 (right) and 48 (left) with 45 and 47 alongside.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE,
		),
		mechanism(
			"mech.top-dead-bumper", "Top dead bumper", "other", [], [switch_id[17]],
			"A passive bumper at the upper right with a switch (17) and no coil (parts list `Dead Bumper A-578-2`; playfield parts `Rebound Bumper Assembly A-790`; IPDB `Passive bumper (1)`). When lit it "
			"spots the lit object: the ROM fired object 1's knock-down coil (public 15) in the retained gameplay run.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.passive-gates", "Passive ball gates", "gate", [], [],
			"The playfield parts list names a `Ball Gate Assembly A-611-R` and a `1 Way Gate Assembly A-471` (wire 6A-211), with no coil or switch. They route the ball by its own motion; do not invent a "
			"powered diverter.",
			MANUAL_SOURCE,
		),
	]


def build_relationships() -> list[dict[str, Any]]:
	relationships = []
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	for source, destination in ((switch_id[30], "device.left-slingshot"), (switch_id[29], "device.right-slingshot"), (switch_id[31], "device.pop-bumper")):
		relationships.append({"id": f"rel.{destination.split('.', 1)[1]}-fired-by-its-switch", "kind": "direct", "source": source, "destination": destination,
			"provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.outhole-kicker-follows-the-outhole-switch", "kind": "pulse", "source": switch_id[33], "destination": "device.outhole-kicker",
		"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE)})
	relationships.append({"id": "rel.kick-out-hole-follows-its-switch", "kind": "pulse", "source": switch_id[34], "destination": "device.kick-out-hole",
		"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, KICK_OUT_SOURCE, LOCK_LANE_SOURCE)})
	for actuator, switches in (("device.eight-bank-reset", range(9, 17)), ("device.center-bank-reset", (18, 19, 20)), ("device.right-bank-reset", (22, 23, 24)), ("device.loop-drop-target-reset", (21,))):
		for address in switches:
			relationships.append({"id": f"rel.{actuator.split('.', 1)[1]}-raises-target-{address}", "kind": "pulse", "source": actuator, "destination": switch_id[address],
				"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	for number, address in sorted(KNOCK_DOWN.items()):
		relationships.append({"id": f"rel.knock-down-coil-drops-object-{number}", "kind": "pulse", "source": data.SOLENOIDS[address]["id"], "destination": switch_id[8 + number],
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, KICK_OUT_SOURCE, LOCK_LANE_SOURCE)})
	for side in ("left", "right"):
		relationships.append({"id": f"rel.{side}-flipper-button-gated-by-the-enable-relay", "kind": "relay_gated", "source": f"switch.{side}-flipper-button", "destination": f"device.{side}-flipper",
			"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE, GAMEPLAY_SOURCE)})
	relationships.sort(key=lambda item: item["id"])
	return relationships


# --- Conflicts ----------------------------------------------------------------------------------------------------------


def build_conflicts() -> list[dict[str, Any]]:
	return [{
		"description": "The manual prints opposite settings for option switch 8. The `NINE BALL SWITCH ASSIGNMENTS` page (PDF page 11) gives `8 Background Sound` ON = On and OFF = Off; the adjustment "
			"table on PDF page 13 gives `BACKGROUND SOUND` `SOUND OFF` = ON and `SOUND ON` = OFF. Both are this game's own manual and nothing else retained names the setting: the known-working scripts' "
			"option menu labels this bit with another game's text (`Missile wows light on equal value`), and PinMAME boots with every option switch OFF. A recreation that exposes the option therefore "
			"cannot tell which setting gives background sound. Resolution path: boot nineball with option switch 8 ON and OFF and compare the sound board commands over an idle stretch of play; "
			"tools/run_pinmame_harness.py has no option-switch input yet, so the probe needs one added, or an owner can flip S8 on a machine.",
		"id": "conflict.option-switch-8-background-sound-setting",
		"path": "inputs[pinmame.input.dip:8]",
		"source_refs": [MANUAL_SOURCE, CORE_SOURCE, SCRIPT_SOURCE],
	}]


# --- Sources ------------------------------------------------------------------------------------------------------------

_PYMUPDF = ", PyMuPDF 1.28.2, Pillow 12.3.0 via tools/render_excerpt_image.py"

# excerpt name -> (source key, locator, has image)
EXCERPTS: dict[str, tuple[str, str, bool]] = {
	"switch-identification": (MANUAL_SOURCE, "PDF page 18, SWITCH I.D. NINE BALL, all forty rows with their strobe buses and the legend", False),
	"switch-locations": (MANUAL_SOURCE, "PDF page 19, SWITCHES NINE BALL location drawing and the list of switches not on the playfield", True),
	"solenoid-identification": (MANUAL_SOURCE, "PDF page 20, NINE BALL SOLENOID identification table", False),
	"solenoid-locations": (MANUAL_SOURCE, "PDF page 21, SOLENOIDS NINE BALL location drawing", True),
	"flipper-wiring": (MANUAL_SOURCE, "PDF page 22, FLIPPER WIRING drawing (lower part of the page)", True),
	"playfield-parts": (MANUAL_SOURCE, "PDF page 17, playfield parts drawing and its lists", True),
	"parts-list": (MANUAL_SOURCE, "PDF page 16, PARTS LIST NINE BALL #125", False),
	"mpu-switch-assignment": (MANUAL_SOURCE, "PDF pages 11-15, NINE BALL SWITCH ASSIGNMENTS and the credit and game adjustment tables", False),
	"self-test": (MANUAL_SOURCE, "PDF pages 3 and 6, game self-diagnostic tests and the self-test and bookkeeping tables", False),
	"general-operation": (MANUAL_SOURCE, "PDF pages 2, 4, 5 and 7, tilt switches, Figure 1, III. GENERAL GAME OPERATION and the S33 note", False),
	"feature-operation": (MANUAL_SOURCE, "PDF pages 8-10, VI. FEATURE OPERATION AND SCORING", False),
	"playfield-switch-matrix": (SCHEMATIC_SOURCE, "PDF page 2, NINE BALL PLAYFIELD, switch matrix", True),
	"playfield-coil-wiring": (SCHEMATIC_SOURCE, "PDF page 2, NINE BALL PLAYFIELD, flipper and coil wiring", True),
	"lda-light-location": (SCHEMATIC_SOURCE, "PDF page 2, NINE BALL LDA LIGHT LOCATION list, all sixty rows", False),
	"general-illumination": (SCHEMATIC_SOURCE, "PDF pages 1 and 2, Transformer Schematic 12B-16B-6A general-illumination buses and the playfield GEN. ILLUM. string", False),
	"solenoid-driver-outputs": (SCHEMATIC_SOURCE, "PDF page 3, SOLENOID DRIVER/VOLTAGE REGULATOR SCHEMATIC FOR NINE BALL, momentary solenoid section", True),
	"solenoid-driver-continuous-section": (SCHEMATIC_SOURCE, "PDF page 3, SOLENOID DRIVER/VOLTAGE REGULATOR SCHEMATIC FOR NINE BALL, continuous solenoids and flipper enable relay", True),
	"lamp-driver-connector-labels": (SCHEMATIC_SOURCE, "PDF page 4, LAMP DRIVER SCHEMATIC 12B-431S-128, connector blocks J1, J2 and J3 with their SCR labels", True),
	"lamp-driver-decoder-outputs": (SCHEMATIC_SOURCE, "PDF page 4, LAMP DRIVER SCHEMATIC 12B-431S-128, decoders U1-U4 with their output resistors and SCRs", True),
}

CROP_DERIVATIONS: dict[str, str] = {
	"switch-locations": f"{MANUAL_PDF} page 19, full page, scanned page rendered at its native resolution (embedded image xref 90, 553px across 7.68in), rendered at 72 dpi, grayscale, 553x765 WebP quality 80" + _PYMUPDF,
	"solenoid-locations": f"{MANUAL_PDF} page 21, full page, scanned page rendered at its native resolution (embedded image xref 100, 584px across 8.11in), rendered at 72 dpi, grayscale, 584x804 WebP quality 80" + _PYMUPDF,
	"playfield-parts": f"{MANUAL_PDF} page 17, full page, scanned page rendered at its native resolution (embedded image xref 80, 586px across 8.14in), rendered at 72 dpi, grayscale, 586x773 WebP quality 80" + _PYMUPDF,
	"flipper-wiring": f"{MANUAL_PDF} page 22, crop box 0,0.28,1,0.97, scanned page rendered at its native resolution (embedded image xref 105, 588px across 8.17in), rendered at 72 dpi, grayscale, 588x550 WebP quality 80" + _PYMUPDF,
	"playfield-switch-matrix": f"{SCHEMATIC_PDF} page 2, crop box 0.03,0.08,0.415,0.93, scanned page rendered at its native resolution (embedded image xref 7, 2982px across 41.42in), rendered at 51 dpi, capped to 820px wide, grayscale, 821x1215 WebP quality 80" + _PYMUPDF,
	"playfield-coil-wiring": f"{SCHEMATIC_PDF} page 2, crop box 0.4,0.08,0.665,0.92, scanned page rendered at its native resolution (embedded image xref 7, 2982px across 41.42in), rendered at 62 dpi, capped to 680px wide, grayscale, 681x1447 WebP quality 80" + _PYMUPDF,
	"solenoid-driver-outputs": f"{SCHEMATIC_PDF} page 3, crop box 0.43,0.08,0.98,0.95, scanned page rendered at its native resolution (embedded image xref 9, 2962px across 41.14in), rendered at 42 dpi, capped to 960px wide, grayscale, 961x1026 WebP quality 80" + _PYMUPDF,
	"solenoid-driver-continuous-section": f"{SCHEMATIC_PDF} page 3, crop box 0.05,0.61,0.43,0.97, scanned page rendered at its native resolution (embedded image xref 9, 2962px across 41.14in), rendered at 70 dpi, capped to 1100px wide, grayscale, 1101x704 WebP quality 80" + _PYMUPDF,
	"lamp-driver-connector-labels": f"{SCHEMATIC_PDF} page 4, crop box 0.62,0.09,0.72,0.86, scanned page rendered at its native resolution (embedded image xref 11, 2919px across 40.54in), rendered at 72 dpi, grayscale, 293x1540 WebP quality 80" + _PYMUPDF,
	"lamp-driver-decoder-outputs": f"{SCHEMATIC_PDF} page 4, crop box 0.26,0.12,0.47,0.86, scanned page rendered at its native resolution (embedded image xref 11, 2919px across 40.54in), rendered at 53 dpi, capped to 450px wide, grayscale, 451x1087 WebP quality 80" + _PYMUPDF,
}


def excerpt_record(name: str, root: Path) -> dict[str, Any]:
	_, locator, has_image = EXCERPTS[name]
	path = root / EXCERPT_ROOT / f"{name}.md"
	if not path.is_file():
		raise RuntimeError(f"Nine Ball excerpt is missing: {path}")
	record: dict[str, Any] = {
		"id": f"excerpt.nine-ball.{name}",
		"locator": locator,
		"method": "manual",
		"path": f"{EXCERPT_ROOT}/{name}.md",
		"reviewed": True,
		"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
		"transcribed_by": "curator, read from the retained rendered page",
	}
	if has_image:
		image = root / EXCERPT_ROOT / f"{name}.webp"
		if not image.is_file():
			raise RuntimeError(f"Nine Ball excerpt image is missing: {image}")
		record["image"] = f"{EXCERPT_ROOT}/{name}.webp"
		record["image_sha256"] = hashlib.sha256(image.read_bytes()).hexdigest()
		record["image_derivation"] = CROP_DERIVATIONS[name]
	return record


def excerpts_for(source: str, root: Path) -> list[dict[str, Any]]:
	return [excerpt_record(name, root) for name, (key, _, _) in EXCERPTS.items() if key == source]


def run_locator(name: str, scenario_sha256: str, manifest: str) -> str:
	driver, stem = runtime_summary.RUNS[name]
	return (f"tools/run_pinmame_harness.py with pinmame64.dll SHA-256 {LIBRARY_SHA256} (built from {PINMAME_REVISION[:12]}), driver {driver}, ROM archive SHA-256 {ROM_ARCHIVES[driver]}; "
		f"scenario tools/harness-scenarios/stern/{stem}.json (SHA-256 {scenario_sha256}), fresh state directory. Run directory manifest SHA-256 {manifest}; compact derived evidence in "
		f"{RUNTIME_EVIDENCE_PATH.as_posix()}.")


def build_sources(root: Path, runtime: dict[str, Any]) -> list[dict[str, Any]]:
	raw = {run["name"]: run for run in runtime["runtime"]["raw_runs"]}
	manifest = runtime["source"]["sha256"]
	manuals = f"external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb/"
	wayback = "Retrieved through the Internet Archive's Wayback Machine copy of the IPDB file"
	sources = [
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED,
			"locator": "src/wpc/stgames.c CORE_GAMEDEFNV(nineball) and the five CORE_CLONEDEFNV entries ninebafp, ninebala, ninebalb, ninebalc and ninebald that name it as parent",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED,
			"locator": "src/wpc/stgames.c INITGAME(nineball, GEN_STMPU200, dispst7, FLIP_SW(FLIP_L), 0, SNDBRD_ST300, 0) and the identical game data of its five clones, the clones' source comments, "
				"input_ports_st; src/wpc/by35.c by35_lampStrobe and pia1b_w (solenoid decoder low nibble and the continuous high nibble PB4-PB7); src/wpc/by35.h BY35_COMPORTS (option switches S1-S32, "
				"default 0) and the diagnostic inputs -7 to -5; src/wpc/core.h sLRFlip/sLLFlip power and hold addresses 45-48",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/stern-mpu200.json", "revision": "repository", "acquired_at": CONTROLLER_COMMITTED,
			"locator": "Stern MPU-200 controller profile: matrix 1-40, diagnostics -7 to -5, flipper-button positions 81-84, option switches 1-32, decoder solenoids 1-15, continuous 17-20 and synthetic "
				"flipper outputs 45-48, sixty discrete SCR lamps 1-63, physical direct inputs 1-3 and uncontrolled GI identity 1",
			"license": "MIT", "attribution": "pinmame-game-defs curation"},
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": f"https://www.ipdb.org/files/1678/{MANUAL_PDF}", "original_filename": MANUAL_PDF, "sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-31T08:53:00Z",
			"locator": f"Stern Nine Ball game manual (IPDB 1678 `Manual`), 23 pages, 3,103,420 bytes, 72 dpi colour JPEG scans without a text layer, retained at {manuals}. {wayback} "
				"(https://web.archive.org/web/20221024014411id_/https://www.ipdb.org/files/1678/Stern_1980_Nine_Ball_Manual.pdf). Pages 2-7 installation, maintenance, self test, Figure 1, operation and "
				"front-door adjustments; 8-10 feature operation; 11-15 option switches; 16 parts list; 17 playfield parts; 18 switch I.D.; 19 switch locations; 20 solenoid I.D.; 21 solenoid locations; "
				"22 MPU jumpers and flipper wiring.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(MANUAL_SOURCE, root)},
		{"id": SCHEMATIC_SOURCE, "kind": "manual", "uri": f"https://www.ipdb.org/files/1678/{SCHEMATIC_PDF}", "original_filename": SCHEMATIC_PDF, "sha256": SCHEMATIC_SHA256,
			"acquired_at": "2026-10-31T08:53:00Z",
			"locator": f"Stern Nine Ball schematic diagrams (IPDB 1678 `Schematic Diagrams`, paginated), 4 large-format grayscale scans, 2,681,726 bytes, retained at {manuals}. {wayback} "
				"(https://web.archive.org/web/20221024015932id_/https://www.ipdb.org/files/1678/Stern_1980_Nine_Ball_Schematic_Diagrams_paginated.pdf). Page 1 Transformer Schematic 12B-16B-6A (general use); "
				"2 NINE BALL PLAYFIELD (switch matrix, coil wiring, LDA LIGHT LOCATION list); 3 Solenoid Driver/Voltage Regulator Schematic for NINE BALL; 4 Lamp Driver Schematic 12B-431S-128 lettered for "
				"NINE BALL, whose typed lamp list belongs to another game and is not used.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(SCHEMATIC_SOURCE, root)},
		{"id": IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=1678", "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-31T08:53:00Z",
			"locator": "IPDB machine 1678: Nine Ball, Stern Electronics, December 1980, model number 125, MPU Stern M-200, 2,279 units; notable features `Flippers (2), Pop bumper (1), Passive bumper (1), "
				"4-bank drop targets (2), 3-bank drop targets (2), Solitary drop target (1), Spinning target (1), Horseshoe lane (1), Kick-out hole (1), Rollunder (1), Multiball (3-ball)`; design Steve Kirk, "
				"art Robert Quinn and Jorge Obregon, software Rob Quinn. Read from the Wayback Machine's 2025-11-24 capture of the page, retained as "
				"external:pinmame-review-artifacts/nine-ball-1980/ipdb/machine-1678.html; its title and machine number match, and the retained manual and schematics are the files it links.",
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database"},
		{"id": SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"{CORPUS_REPOSITORY}/blob/{CORPUS_REVISION}/{quote(SCRIPT_PATH, safe='/')}", "revision": CORPUS_REVISION, "sha256": SCRIPT_SHA256, "acquired_at": CORPUS_COMMITTED,
			"locator": f"{SCRIPT_PATH} in the pinned known-working script corpus (116,655 bytes, LF; the Git blob is the file), cGameName = \"nineball\": SolCallback 3 and 4 raise the right (22-24) and "
				"center (18-20) banks, 6 knocker, 7 the trough (bsTrough.InitSw 0,33,36,37), 8 the kick-out hole (InitSaucer sw34), 9-15 knock down objects 7 to 1, 17 the eight-bank, 19 "
				"vpmNudge.SolGameOn, 20 the loop target; Controller.Switch handlers 4, 25-28, 32, 38, 39 and 40 and PulseSw 5, 17, 29-31 and 35. It carries the same option menu, rothbauerw ball control "
				"and Thalamus patches as the retained table's script and adds a VR room.",
			"license": "NOASSERTION", "attribution": "Nine Ball VPX table authors and repository contributors", "known_working": True},
		{"id": STANDALONE_SOURCE, "kind": "vpx_script", "uri": f"{STANDALONE_REPOSITORY}/blob/{STANDALONE_REVISION}/{quote(STANDALONE_PATH, safe='/')}", "revision": STANDALONE_REVISION,
			"sha256": STANDALONE_SHA256, "acquired_at": STANDALONE_COMMITTED,
			"locator": f"vpx-standalone-scripts: {STANDALONE_PATH} (118,041 bytes), the second pinned known-working corpus; its solenoid, switch and lamp bindings are the corpus script's. Checkout SHA256 "
				f"is CRLF materialization; LF-normalized text matches Git blob SHA256 {STANDALONE_BLOB_SHA256}. The `.vbs.patch` beside it adds a drop-target class for standalone play.",
			"license": "NOASSERTION", "attribution": "Nine Ball VPX table authors and repository contributors", "known_working": True},
		{"id": TABLE_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{(TABLE_RELATIVE / TABLE_FILENAME).as_posix()}", "original_filename": TABLE_FILENAME, "sha256": TABLE_SHA256,
			"revision": "bord 1.0 (June 2017)", "acquired_at": "2026-10-31T08:54:00Z",
			"locator": f"Nine Ball by bord, table version 1.0, June 2017 (`Stern 1980 / VPX 10.3 / Custom bracket primitives by randr`), {TABLE_BYTES:,} bytes, copied from the operator's "
				f"local tables archive (file time 2020-01-20), the only local Nine Ball table. Exact playfield bounds left 0, top 0, right {data.TABLE_WIDTH:g}, bottom {data.TABLE_HEIGHT:g}; "
				f"normalized coordinates are x/{data.TABLE_WIDTH:g} and y/{data.TABLE_HEIGHT:g}. The geometry source for every located placement. Its 188 lights show no bulb mesh; its 25 `BulbFil` "
				"primitives are the general-illumination bulbs.",
			"license": "NOASSERTION", "attribution": "bord, with bracket primitives by randr; redistribution rights not granted", "rights": "NOASSERTION"},
		{"id": TABLE_SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"external:pinmame-vpx-sources/{(EXTRACTION_RELATIVE / 'script.vbs').as_posix()}", "original_filename": "script.vbs",
			"sha256": TABLE_SCRIPT_SHA256, "acquired_at": "2026-10-31T08:54:54Z",
			"locator": "Embedded script of the retained table, 69,558 bytes, cGameName = \"nineball\" (ninebafp and ninebalb commented as alternatives). Its solenoid and switch bindings match the "
				"corpus scripts with these defects: trigger sw38 writes switch 39 and no handler writes 38; trigger sw1, at the top of the lock lane, has no handler; SolCallback(5) for the pop bumper is "
				"commented out; sw27_Hit is defined twice. It binds each switch and coil placement's object.",
			"license": "NOASSERTION", "attribution": "bord", "known_working": True},
		{"id": EXTRACTION_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE.as_posix()}", "sha256": EXTRACTION_MANIFEST_SHA256,
			"acquired_at": "2026-10-31T08:54:54Z",
			"locator": f"Retained vpxtool {VPXTOOL_VERSION} extraction of the table; manifest external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE.as_posix()} (format pinmame-vpx-extraction-manifest "
				f"v1: every file as sorted relative POSIX path, size and SHA-256, canonical JSON), SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes. "
				"tools/curate_nine_ball.py --verify-extraction recomputes it.",
			"license": "NOASSERTION", "attribution": "bord; redistribution rights not granted"},
	]
	for name in RUN_NAMES:
		sources.append({
			"id": RUN_SOURCES[name],
			"kind": "service_diagnostic" if name in runtime_summary.SERVICE_RUNS else "runtime_scenario",
			"uri": f"external:pinmame-review-artifacts/nine-ball-1980/harness/{name}/run.json",
			"sha256": raw[name]["sha256"],
			"acquired_at": RUN_AT[name],
			"locator": run_locator(name, raw[name]["scenario_sha256"], manifest),
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		})
	return sources


# --- Definition ---------------------------------------------------------------------------------------------------------

MISSING = ["spatial_placement", "unresolved_conflicts"]


def build_definition(root: Path = ROOT) -> dict[str, Any]:
	if len(data.SWITCHES) != 40 or set(data.SWITCHES) != set(range(1, 41)) or set(data.DIPS) != set(range(1, 33)):
		raise RuntimeError("Nine Ball switch or option-switch inventory is incomplete")
	if sorted(data.PHYSICAL_TO_PUBLIC) != list(range(1, 20)) or set(data.SOLENOIDS) != set(data.PHYSICAL_TO_PUBLIC.values()):
		raise RuntimeError("Nine Ball solenoid inventory is incomplete")
	if {q for qs in data.DECODER.values() for q in qs} != set(range(1, 61)) or any(len(qs) != 15 for qs in data.DECODER.values()):
		raise RuntimeError("Nine Ball decoder map does not cover SCRs 1-60 exactly once")
	if sorted(KNOCK_DOWN) != list(range(1, 8)) or any(address != 16 - number for number, address in KNOCK_DOWN.items()):
		raise RuntimeError("Nine Ball knock-down coils are not public 16-k for objects 1-7")
	runtime = runtime_document(root)
	observations = runtime["runtime"]["observations"]
	if {int(key): value for key, value in observations["physical_service_solenoid_to_public"].items()} != data.PHYSICAL_TO_PUBLIC:
		raise RuntimeError("Nine Ball solenoid translation disagrees with the retained solenoid test")
	if [run["name"] for run in runtime["runtime"]["raw_runs"]] != list(RUN_NAMES):
		raise RuntimeError("Nine Ball runtime evidence does not carry the curator's runs")
	if set(observations["lamp_addresses_seen"]) != set(data.LAMP_TO_Q) or observations["lamp_decoder_holes_not_seen"] != [16, 32, 48, 64]:
		raise RuntimeError("Nine Ball burn-in lamps are not the sixty SCR outputs")
	return build_unchecked_definition(root, runtime)


def build_unchecked_definition(root: Path, runtime: dict[str, Any]) -> dict[str, Any]:
	observations = runtime["runtime"]["observations"]
	return {
		"conflicts": build_conflicts(),
		"controller": {"inversion_applied_by_emulator": True, "platform": "pinmame.stern-mpu200"},
		"coverage": {
			"dimensions": {
				"address_enumeration": "validated",
				"catalog_identity": "validated",
				"causal_exercise": "validated",
				"diagnostic_enumeration": "validated",
				"display_inventory": "validated",
				"emulator_normalization": "validated",
				"mechanisms": "validated",
				"physical_wiring": "validated",
				"recreation_knowledge": "validated",
				"runtime_observation": "validated",
				"semantic_naming": "validated",
				"spatial_placement": "observed",
				"variant_coverage": "validated",
			},
			"missing": list(MISSING),
			"status": "partial",
		},
		"displays": [
			{"controller_index": index, "id": identifier, "kind": "segment", "label": label, "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, GAMEPLAY_SOURCE), "segment_start": start,
				"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE), "width": width}
			for identifier, label, index, start, width in data.DISPLAYS
		],
		"drivers": [
			{"description": data.DRIVERS[driver_id][0], "flags": 0, "id": driver_id, "manufacturer": data.DRIVERS[driver_id][2], "physical_compatibility": "identical",
				"variant_notes": data.DRIVERS[driver_id][4], "year": data.DRIVERS[driver_id][1], **({"clone_of": data.DRIVERS[driver_id][3]} if data.DRIVERS[driver_id][3] else {})}
			for driver_id in sorted(data.DRIVERS)
		],
		"format": "pinmame-machine-definition",
		"inputs": build_inputs(observations),
		"knowledge": {"path": KNOWLEDGE_PATH.as_posix(), "status": "complete"},
		"machine": {"id": MACHINE_ID, "ipdb_id": 1678, "kind": "physical_pinball", "manufacturer": "Stern", "model_number": "125", "name": "Nine Ball", "opdb_id": "G4jjx-MDbz2", "year": 1980,
			"playfield": {"height": data.TABLE_HEIGHT, "provenance": provenance(TABLE_SOURCE), "units": "vpx", "width": data.TABLE_WIDTH}},
		"mechanisms": build_mechanisms(),
		"outputs": build_outputs(observations),
		"relationships": build_relationships(),
		"schema_version": 2,
		"sources": build_sources(root, runtime),
	}


# --- Spatial report -----------------------------------------------------------------------------------------------------


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_records: list[dict[str, Any]] = []
	not_applicable_records: dict[str, list[str]] = {}
	unplaced: list[dict[str, Any]] = []
	statuses: dict[str, int] = {}
	for collection in ("inputs", "outputs", "displays"):
		for item in definition[collection]:
			spatial = item.get("spatial")
			binding = item.get("binding", {})
			record = {"id": item["id"], "group": binding.get("group", "display"), "address": binding.get("device", item.get("controller_index"))}
			if spatial is None:
				unplaced.append(record)
			elif spatial["status"] == "not_applicable":
				not_applicable_records.setdefault(spatial["reason"], []).append(item["id"])
			else:
				located_records.append({**record, "placements": len(spatial["placements"])})
				for placement in spatial["placements"]:
					statuses[placement["provenance"]["status"]] = statuses.get(placement["provenance"]["status"], 0) + 1
	projections = [{"address": address, "group": "pinmame.input.switch", "reason": reason} for address, (_, reason) in sorted(data.SWITCH_OBJECTS.items()) if reason]
	projections += [{"address": address, "group": "pinmame.output.solenoid", "reason": reason} for address, (_, reason) in sorted(data.SOLENOID_OBJECTS.items()) if reason]
	projections += [{"address": address, "group": "physical.input.direct", "reason": f"Placed on the {side} flipper pivot: the end-of-stroke contact is mounted on its flipper assembly."}
		for address, side in ((1, "left"), (2, "right"))]
	unplaced_lamps = [item["address"] for item in unplaced if item["group"] == "pinmame.output.lamp"]
	return {
		"blockers": [
			f"No playfield lamp is placed ({len(unplaced_lamps)} of the 60): the retained table, the only Nine Ball table available, draws every insert with lights that show no bulb mesh, and "
			"the manual prints no lamp-location drawing, so no source marks a socket (docs/SPATIAL.md, Picking the bulb).",
			"The trough switches 33, 36 and 37 and the outhole kicker (public 7) are not placed: both known-working scripts and the table model the trough as a virtual ball stack with no object at "
			"the switches, and the location drawing prints the three switch numbers under the apron without arrows.",
			"Every switch, coil and general-illumination placement is `observed` from the one table; no factory-drawing callout check was made, and the manual's location drawings are 72 dpi scans.",
			"Lock-lane switches 38 and 39 rest on the table's triggers where the drawing puts them, but the table binds neither correctly (its sw38 writes 39 and its sw1 has no handler).",
		],
		"coordinate_convention": {"source_bounds": {"bottom": data.TABLE_HEIGHT, "left": 0.0, "right": data.TABLE_WIDTH, "top": 0.0}, "space": "playfield",
			"x": f"x/{data.TABLE_WIDTH:g}; 0=left, 1=right", "y": f"y/{data.TABLE_HEIGHT:g}; 0=rear/backglass, 1=apron/player"},
		"excluded_object_classes": [
			"L<n>, L<n>a-c, L<n>b and l<n>a-b lights, the Bumper1Light and the f11, f29 and f30 flashers: insert lights and glows the script binds to lamp numbers; none of the table's 188 lights shows a bulb mesh, so none marks a socket",
			"LDrop<bank><n> lights (collection dtLeftLights): drop-target glows the script switches from the target hit events, not lamp outputs",
			"GI_<n> and Light<n> lights (collection GI): placed through the BulbFil<n> bulb-filament primitive each GI_<n> light sits on, not on their own",
			"BulbTop<n> primitives: the glass tops of the same 25 general-illumination bulbs",
			"LED and led display-segment flashers, the BG backglass flashers and the Flasher<n> lighting overlays, none of them bound to a lamp number: backbox and render helpers, not playfield devices",
			"Drain and BallRelease kickers: the virtual trough's entry and its shooter-lane exit, not physical trough positions",
			"Gate1, Gate2, Gate6, BallReleaseGate and the hidden Gate3: passive or helper gates with no controller binding",
		],
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_algorithm": "format pinmame-vpx-extraction-manifest v1: every file as sorted relative POSIX path, size and SHA-256, canonical JSON (tools/curate_nine_ball.py)",
			"manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE.as_posix()}", "source_ref": EXTRACTION_SOURCE, "total_bytes": EXTRACTION_TOTAL_BYTES,
			"table_sha256": TABLE_SHA256, "script_sha256": TABLE_SCRIPT_SHA256, "vpxtool_version": VPXTOOL_VERSION},
		"format": "pinmame-spatial-blockers",
		"located_records": sorted(located_records, key=lambda item: item["id"]),
		"machine_id": MACHINE_ID,
		"not_applicable_records": {reason: sorted(ids) for reason, ids in sorted(not_applicable_records.items())},
		"placement_statuses": dict(sorted(statuses.items())),
		"projections": projections,
		"readiness": {"missing": definition["coverage"]["missing"], "status": definition["coverage"]["status"], "unresolved_conflicts": len(unresolved_conflicts(definition))},
		"unplaced_records": sorted(unplaced, key=lambda item: item["id"]),
		"version": 1,
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Nine Ball (Stern, 1980) spatial review",
		"",
		"Status: incomplete. No playfield lamp is placed and every placement is `observed`, so the machine record stays `partial` at `machines/partial/stern/nine-ball-1980.json`.",
		"",
		f"The geometry source is the retained `{TABLE_FILENAME}` (bord, 1.0, June 2017) at SHA-256 `{TABLE_SHA256}`; its embedded script (SHA-256 `{TABLE_SCRIPT_SHA256}`) binds the same switches "
		f"and coils as the two pinned known-working corpus scripts, apart from the defects listed below. Exact playfield bounds are left 0, top 0, right {data.TABLE_WIDTH:g}, bottom {data.TABLE_HEIGHT:g}, "
		f"and every canonical coordinate is x/{data.TABLE_WIDTH:g} and y/{data.TABLE_HEIGHT:g} rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, "
		"in normalized VPX/player view.",
		"",
		"## Evidence decisions",
		"",
		"- The script's bindings choose each switch's and coil's object. A switch sits on its trigger, target, bumper, kicker or spinner; a coil sits on the object it moves.",
		"- Lamps are not placed. The table's 188 lights include 128 bulb-mode lights, but none shows a bulb mesh, and docs/SPATIAL.md requires a real bulb for a socket.",
		"- General illumination is placed on the 25 `BulbFil` bulb-filament primitives, each with a `GI_<n>` light at its centre (a light at the centre of a separate bulb primitive shows its bulb). "
		"The table's grouping gives no quantity, and nothing machine-side names a G.I. string, so the placements stay `observed`.",
		"- The table mis-binds the lock lane: trigger `sw38` writes switch 39, and trigger `sw1` at the top of the lane has no handler. Both triggers sit where the manual's switch drawing puts 38 and 39, "
		"so 38 is placed on `sw38` and 39 on `sw1`, with the defect stated on each switch.",
		"",
		"## Explicit projections",
		"",
	]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += ["", "## Counts", ""]
	lines.append(f"- Placements: {sum(item['placements'] for item in report['located_records'])} ({', '.join(f'{count} {name}' for name, count in report['placement_statuses'].items())}) on {len(report['located_records'])} records")
	for reason, ids in report["not_applicable_records"].items():
		lines.append(f"- Records with a controlled `{reason}` record: {len(ids)}")
	lines.append(f"- Records with no spatial key: {len(report['unplaced_records'])}")
	lines += ["", "## Excluded table objects", ""]
	lines += [f"- {entry}" for entry in report["excluded_object_classes"]]
	lines += ["", "## Blockers", ""]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Promotion decision", "",
		"Promotion to `author_ready` is refused: no playfield lamp has a socket, the trough has no physical objects, and every placement rests on one table with no factory-drawing check. The record "
		"also carries one unresolved conflict about option switch 8, which does not concern placement. It stays `partial` with "
		f"`coverage.missing = {report['readiness']['missing']}`.".replace("'", "\""), "",
		"## Retained evidence", "",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Object-centre dump of every extracted game item at `external:pinmame-review-artifacts/nine-ball-1980/table-geometry.json`.", ""]
	return "\n".join(lines)


# --- Knowledge note -----------------------------------------------------------------------------------------------------

KNOWLEDGE = """# Nine Ball (Stern, 1980)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; no playfield lamp is placed, and one option switch's printed setting is contradictory**

## Identity and evidence precedence

This is the one physical Stern Nine Ball (IPDB 1678, December 1980, model 125, Stern M-200 MPU, 2,279 units; design Steve Kirk, art Robert Quinn and Jorge Obregon). PinMAME `nineball` is the production root
(ROMs U1, U2, U5 and U6, the parts list's 25A-125-E1E48 to E6E48) and `ninebafp` its free-play clone with free-play U2 and U6. `ninebala` and `ninebalc` are Idleman's ball-handling modifications (beta 18,
2020, and beta 19, 2021), `ninebald` his gameplay modification (beta 21, 2021), and `ninebalb` Oliver's modified rules revision 85 (2007) in one 32 KB image; its source comment says a two-ball multiball
flashes 2X and doubles all scores, a three-ball multiball flashes 4X and quadruples them, the self test is incomplete and it is free play only. All six share one game-data line (`GEN_STMPU200`, seven-digit
`dispst7` displays, `FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound), so they are physically identical and only the ROM program differs. The authorized ROM library holds `nineball`, `ninebafp` and
`ninebalb`; it has no set for `ninebala`, `ninebalc` or `ninebald`, so those three were not run.

Evidence order is the runbook's. The two pinned corpus scripts give runtime bindings, this game's own manual and four-sheet schematic set give construction and wiring, pinned PinMAME gives the controller
topology, and ten retained harness runs (burn-in, solenoid test, switch test, a scripted game, game over and slam, a kick-out spot, the lock lane, an option-switch probe, and one run each of `ninebafp` and
`ninebalb`) pair the printed numbers with public addresses and show the ROM's responses. The manual is a 72 dpi scan; the schematic set is four large-format scans, three of them drawn or lettered for Nine Ball.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty (retained run), so the Switch I.D.
numbers are the public addresses. All forty positions are fitted. The cabinet switches 1-3 (coin chutes), 6 (credit), 7 (tilt) and 8 (slam) are strobed on R-Y (J3-3) and return on MPU connector J3;
the playfield sheet draws them as unlabelled contacts. Every matrix contact is normally open; every one has a series 1N4004 diode except coin chutes 1-3, and 4, 17 and 35 also carry a .05 capacitor.
Service inputs are -7 (Self Test), -6 (CPU diagnostic NMI) and -5 (sound diagnostic); the last two are PinMAME routes with no documented button. The flipper
buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' end-of-stroke contacts and the door's remote S33 memory-clear button are hard-wired and have only profile-local
identities (physical direct inputs 1-3).

**Solenoids.** The printed solenoid numbers are SDU driver transistor positions, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires, pairing them as
`1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over four identical cycles. In public terms: 1 right slingshot,
2 left slingshot, 3 right three-bank reset, 4 center three-bank reset, 5 pop bumper, 6 knocker, 7 outhole kicker, 8 kick-out hole, 9-15 the knock-down coils of objects 7 down to 1 (object k on 16-k),
17 eight-bank reset, 18 coin lockout, 19 flipper enable relay, 20 loop drop target reset. Public 16 is the decoder's unaddressable slot. Every one of the nineteen drivers carries a load.

**Continuous outputs.** Public 17 (Q17, PB4), 18 (Q19, PB5), 19 (Q15, PB6) and 20 (Q18, PB7) are the SDU's continuous section. 18 and 19 are held: the coin lockout is energized from about 8.7 s after
power-up, as the manual's attract description says, and the flipper relay is on only during a game. 17 and 20 are used as pulsed coils. The power-up initialisation pulses all four once, and the kick-out hole
(8) as well. Besides its pulses after switch 21, the ROM pulsed 20 once in the gameplay run about 4.2 s after the left outlane collected the loop value; that may be the loop target's reset after a collect,
but the run does not prove it.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`. This game's
lettered copy of sheet 12B-431S-128 was read for all sixty lines; it crosses `U2` S7/S8 to Q25/Q24 and `U3`/`U4` S9 to Q41/Q46, and the ROM confirms both: the bonus-object lamps it lights in order in the
lock-lane run are public 58, 42, 26, 10, 57, 41 and 25, the SCRs Q46, Q41, Q17, Q2, Q56, Q42 and Q24 that the light list prints for BONUS TARGET 1-7. The game's own lamp assignment is the sixty-row
`NINE BALL LDA LIGHT LOCATION` list on the playfield sheet, which names a load, wire, jack, pin and SCR for every output; the typed list on the lamp-driver sheet belongs to another game and is not used.
Four of the list's J2 pins differ from the lamp-driver sheet's connector block (SCRs Q3, Q5, Q7 and Q39); the definition follows the game's list. GAME OVER (45), HIGH SCORE TO DATE (13), MATCH (63) and TILT
(61) are backbox lamps. SHOOT AGAIN (27) is drawn on the playfield by the table. SUPER BONUS (14), R. BANK BOTTOM WOW (15) and R. BANK TOP WOW (31) changed state only in the service runs and
no play run lit them; they are printed loads and stay used. The spinner value lamps are 12, 28, 44 and 60, and the loop value lamps 55 (10K), 8 (20K), 24 (30K), 40 (40K) and 56 (top value).

**General illumination** is uncontrolled: a 6 VAC playfield string from A2J1-8, the cabinet bus and the backbox buses straight off the transformer, with no relay or driver in any line.

## Ball lifecycle

Three balls sit in the trough under the apron on switches 37, 36 and 33, left to right, the one on 33 in front of the outhole kicker. When a game starts the ROM resets the eight-bank (17) and both
three-banks (3, 4) and kicks the outhole (7), repeating all four about every 1.2 s while 33 stays closed; a real ball leaves 33 on the first kick and rolls to the shooter lane (switch 40). After a drain the
bonus times the multiplier is collected, the ball-in-play advances and the next ball is served; an extra ball is played without advancing. Tilt drops the flipper relay (19), lights TILT (61) and fires the
kick-out hole (8) to free a captured ball. A slam (8) ends the game, and the ROM repeats its power-up initialisation.

## Mechanisms

- **Left eight-target bank**: two four-target banks on one reset coil (17). Upper bank objects 2, 4, 6, 8 from the top (switches 10, 12, 14, 16), lower bank objects 7, 5, 3, 1 (switches 15, 13, 11, 9).
  Objects 1-7 have knock-down coils (public 16-k); object 8 has none. The objects are made in order: when the lit object is made the ROM resets the bank within about 35 ms and knocks down every object
  made so far, lowest first, firing each coil only after the previous target's switch has closed. If a target's switch never closes, the ROM retries that coil about every 0.8 s.
- **Kick-out hole and lock lane** at the left: switch 34 in the hole (coil 8), 38 and 39 above it. Before object 5 is lit the hole spots objects with the knock-down coils and ejects. Once object 5 is lit
  it captures: a ball on 34 is held and a new one served, a ball on 38 behind it the same, and a third ball on 39 releases all three, the ROM firing 8 once per ball.
- **Center (18, 19, 20) and right (22, 23, 24) three-target banks**, each with one reset coil (4 and 3) and no knock-downs. With option switch 14 OFF both reset only after all six targets are down.
- **Loop drop target** (21) at the exit of the top-left loop, raised by 20; the loop's entrance is the roll-under gate switch 4.
- **Spinner** (5) on the right, **pop bumper** (31 fires 5), **slingshots** (30 fires 2, 29 fires 1), the passive **top dead bumper** (17) and two passive gates.
- **Flippers**: one per side, J-25-475/34-4500 dual-winding coils, gated by the flipper enable relay; PinMAME publishes 46 (right) and 48 (left) with 45 and 47 alongside.

## Rules summary

From the manual's feature pages: each of the eight drop targets scores its object number x 1,000, and hitting the lit object advances the bonus and lights the next object (bonus maximum 45,000). The top
dead bumper and the return lanes spot the lit object when lit, and the kick-out hole and the lock-lane switches spot numbers too. Making all eight in order lights the flashing object 9 target and the
flashing WOW lite; making object 9 lights Super Bonus (77,000) for the next ball (option switch 29 moves the WOW lite and option switch 30 the Super Bonus to object 8). Making all the targets again lights Special and excludes target 1 from play,
and each further round excludes the next. Completing a three-bank advances the multiplier (7X maximum; after 6X or 7X it resets to 2X for the next ball), and once the multiplier reaches 6X or 7X a lit
outside three-bank target awards WOW. The spinner scores 100 or the highest lit value and any spin resets it; the targets option switch 17 selects advance the value, and the stand-up 35 scores 7,000 and
sends the value to the top. The loop roll-under and the left lane lower switch score 3,000 and advance the loop value; the loop target and a lit outlane collect it. Capturing all three balls, or making
object 9, releases the captured balls for three-ball play. Option switches 22-24 choose the WOW and Special awards from the chart on PDF page 11.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32 (Figure 1, page 12). Coin chutes 1, 2 and 3 take S1-4, S9-12 and S25-28; S5 add-a-ball, S6 high-score award, S7 balls per game, S8
background sound, S13 spot-number lite, S14 multiplier step-up, S15-16 high score to date, S17 spinner-advance targets, S18-19 maximum credits, S20 credit display, S21 match, S22-24 WOW and Special
awards, S29-30 which object lights the eight-bank WOW and Super Bonus, S31 the three-bank WOW multiplier and S32 the Special limit. PinMAME boots with all of them OFF, which gives the three-ball games of the
retained runs (S7 OFF = 3 balls). Two settings disagree between the manual's pages:

- **S17.** PDF page 11 prints ON = outside targets and OFF = center targets; PDF page 14 prints the reverse. The retained spinner-option run settles it: with S17 OFF the center targets 19 and 23 lit the
  spinner value lamps 12 and 28, and the outside targets 18, 20 and 22 lit none. Page 11 is right.
- **S8.** PDF page 11 prints ON = background sound on; PDF page 13 prints SOUND OFF = ON. Nothing retained settles it, and it stays an unresolved conflict. A harness run with S8 set ON and OFF,
  comparing the sound board commands over an idle stretch of play, would settle it, but `tools/run_pinmame_harness.py` cannot set option switches yet. An owner flipping S8 on a machine would also settle it.

The known-working scripts' option menu copies another game's text for several of these bits, so do not label a recreation's options from it.

## Displays and sound

Four seven-digit player displays (indices 0-3, segment starts 1, 9, 17 and 25), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME `dispst7`.
Sound is the Stern sound module (ST300; Figure 1 labels it B-605 and the parts list C-605); sound commands add no playfield devices.

## Disagreements between this game's own documents

- Option switches 8 and 17, as above.
- The lamp-driver sheet's connector block and the game's light list disagree on four J2 pins (SCRs Q3, Q5, Q7 and Q39); connector-pin readings only, and the light list is followed.
- The playfield sheet draws no coil for drop target 1, which the solenoid table prints as `16 Q16 J5-8 G-W DROP TARGET #1`; the ROM's solenoid test fires public 15 for driver 16, and the knock-down runs
  show it putting object 1 down.
- The installation page names three tilt switches including a `Panel tilt on bottom of playfield panel`, while the location page lists `7 ROLL-TILT`, `7 PENDULUM`, `8 TILT BOARD` and `8 DOOR`; whether the
  panel tilt is the tilt-board slam contact is not settled, so switch 7 counts the two contacts the location page lists.
- The parts list prints a `Stand-Up Target J-26-1200` coil that matches no driver in the solenoid table, and no coil for the single loop drop target; the loop target's reset coil has no part number.
- Figure 1 labels the sound board B-605; the parts list prints C-605.
- The credit table spells the coin-chute colours out (`BRN-WHITE`, `RED-WHITE`) where the Switch I.D. prints `BRN-W` and `R-W`.

## Recreation checklist

- Build the full inventory: 40 matrix switches, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 with the two flipper callbacks, the sixty
  SCR lamp addresses and the six displays.
- Start with three balls in the trough (33, 36 and 37 closed), every drop target up, the lock lane empty and the flipper relay off until a game starts.
- Make each knock-down coil (public 16-k) put its object's target down so that its switch closes; the ROM waits for that switch before the next spot and retries the coil about every 0.8 s until it closes.
- Capture balls in the kick-out hole and the lane behind it once object 5 is lit, and release them one at a time on public 8.
- Treat the manual's feature pages and the ROM as the rules authority; the community ROMs change rules, not hardware.
- Placements: switches, coils and general illumination come from the retained table and are `observed`; lamps are unplaced until a table or drawing marks their sockets.

## What would complete the record

- **Spatial placement**: a Nine Ball table that models its insert bulbs (or a lamp-location drawing), a second independent table or a factory-drawing callout check for the switches and coils, and a
  trough model with objects at 33, 36 and 37.
- **Option switch 8**: the harness probe or owner check described above.

## Retained table and its defects

The geometry comes from `Nine Ball (Stern 1980).vpx` by bord (1.0, June 2017, with bracket primitives by randr), the only local Nine Ball table. Its script binds the same solenoids and switches as the two
pinned corpus scripts, which share its option menu and ball control and add a VR room, except where it is defective: trigger `sw38` writes switch 39 and nothing writes 38, trigger `sw1` at the top of the lock
lane has no handler, the pop bumper's SolCallback(5) is commented out (the bumper kicks on its own hit), and `sw27_Hit` is defined twice. None of these changes what the machine is; they are stated on the
affected devices. Its insert lights show no bulb mesh, so they place no lamp.

## Sources

- `manual.stern.nine-ball.1980`: the 23-page IPDB manual, with transcribed excerpts of its identification tables, location drawings, parts pages, option switches, flipper wiring and operating text.
- `schematic.stern.nine-ball.wiring-set`: the four-page IPDB schematic set, with excerpts of the playfield sheet (switch matrix, coil wiring, light list), the solenoid driver sheet, the lamp driver sheet
  and the general-illumination buses.
- `vpx-script.nine-ball-corpus` and `vpx-script.nine-ball-standalone`: the pinned known-working corpus scripts.
- `vpx-table.nine-ball-bord-1-0`, its embedded script and its retained extraction: the geometry of every placement.
- `runtime.nine-ball.*`: ten isolated harness runs on the pinned `pinmame64.dll`, eight of `nineball` (ROM archive SHA-256 `4311155374bd000db727c74747cfec8707755a899e5bfd25cc35c133851da971`) and one
  each of `ninebafp` and `ninebalb`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.46e1a01a0f73`: driver declarations, MPU-200 implementation, public-address conversion and display layout.
"""


# --- Retained extraction manifest -------------------------------------------------------------------------------------


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Nine Ball retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required for the retained Nine Ball extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE
	if not manifest_path.is_file():
		raise RuntimeError(f"Nine Ball retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(source_root / EXTRACTION_RELATIVE)
	if canonical_bytes(actual) != canonical_bytes(expected) or manifest_path.read_bytes() != canonical_bytes(actual):
		raise RuntimeError(f"Nine Ball retained extraction manifest does not match all files under {source_root / EXTRACTION_RELATIVE}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Nine Ball retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	"""Write the canonical manifest beside the extraction; refuse to replace a manifest whose content differs."""
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE
	payload = canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE))
	if manifest_path.exists() and manifest_path.read_bytes() != payload:
		raise RuntimeError(f"Refusing to overwrite a differing Nine Ball extraction manifest: {manifest_path}")
	manifest_path.write_bytes(payload)
	return manifest_path


# --- Generation and checking ------------------------------------------------------------------------------------------


def products(root: Path = ROOT) -> dict[Path, bytes]:
	definition = build_definition(root)
	errors = validate_machine(definition, root)
	if errors:
		raise RuntimeError("Invalid Nine Ball definition: " + "; ".join(errors[:20]))
	if unresolved_conflicts(definition) and "unresolved_conflicts" not in definition["coverage"]["missing"]:
		raise RuntimeError("Nine Ball holds unresolved conflicts but does not list them as missing")
	report = build_spatial_report(definition)
	return {
		DEFINITION_PATH: canonical_bytes(definition),
		SEED_PATH: canonical_bytes(definition),
		SPATIAL_REPORT_PATH: canonical_bytes(report),
		SPATIAL_REPORT_MARKDOWN_PATH: render_spatial_report(report).encode("utf-8"),
		KNOWLEDGE_PATH: KNOWLEDGE.encode("utf-8"),
	}


def generate(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Nine Ball artifact")
	for path, payload in products(root).items():
		(root / path).parent.mkdir(parents=True, exist_ok=True)
		(root / path).write_bytes(payload)


def check(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("A Nine Ball author-ready definition is present although the record is partial")
	for path, payload in products(root).items():
		if not (root / path).is_file() or (root / path).read_bytes() != payload:
			raise RuntimeError(f"Nine Ball deterministic artifact missing or drifted: {path}")
	print("Nine Ball definition, seed, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, knowledge note and spatial report")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained VPX extraction against its pinned manifest identity (needs PINMAME_VPX_SOURCES_ROOT)")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained extraction's canonical manifest; refuses to replace a differing one")
	args = parser.parse_args()
	if args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Nine Ball retained extraction matches its pinned manifest identity.")
	elif args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Wrote {write_extraction_manifest(source_root)}")
	elif args.check:
		check(ROOT)
	else:
		generate(ROOT)
		print(f"Wrote {DEFINITION_PATH}")


if __name__ == "__main__":
	main()
