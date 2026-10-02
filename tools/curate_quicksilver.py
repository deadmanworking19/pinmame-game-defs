#!/usr/bin/env python3
"""Curate the physical Stern Quicksilver (1980) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and retained-table coordinate is a
literal in ``tools/quicksilver_data.py`` or here, so regeneration reproduces the canonical definition, its pinned seed, the
spatial report and the knowledge note byte for byte without reading the external evidence roots. ``--check`` refuses drift
and ``--regenerate`` is the only path that writes.

Evidence authority follows the runbook. The known-working VPX script owns runtime semantics, this game's own manual and
driver-board schematics own physical construction, wiring and device presence, and pinned PinMAME owns controller topology.
Where the machine's own sheets disagree with each other the disagreement is a device note when only a connector pin or wire
colour differs, and a ``conflicts`` entry otherwise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402
import drawing_callouts  # noqa: E402
import quicksilver_data as data  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/stern/quicksilver-1980.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/quicksilver-1980.json"
SEED_PATH = ROOT / "tools/seeds/stern/quicksilver-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/quicksilver-1980.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/quicksilver-1980.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/stern/quicksilver-1980.md"
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/stern/quicksilver-self-test-and-gameplay.json"
EXCERPT_ROOT = "evidence/excerpts/stern.quicksilver.1980"

MACHINE_ID = "stern.quicksilver.1980"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-stern-mpu200"
MANUAL_SOURCE = "manual.stern.quicksilver.1980"
LAMP_SCHEMATIC_SOURCE = "schematic.stern.quicksilver.lamp-driver"
SOLENOID_SCHEMATIC_SOURCE = "schematic.stern.quicksilver.solenoid-driver"
CARD_SOURCE = "manual.stern.quicksilver.instruction-card"
IPDB_SOURCE = "ipdb.1895"
TABLE_SOURCE = "vpx-table.quicksilver-vpw-1-0"
SCRIPT_SOURCE = "vpx-script.quicksilver-vpw-1-0"
CORPUS_SCRIPT_SOURCE = "vpx-script.quicksilver-corpus-1-0"
ARCHIVE_TABLE_SOURCE = "vpx-table.quicksilver-archive"
ARCHIVE_SCRIPT_SOURCE = "vpx-script.quicksilver-archive"
EXTRACTION_SOURCE = "vpx-extraction.quicksilver-vpw-1-0"
SELF_TEST_SOURCE = "runtime.quicksilver.self-test"
STUCK_SWITCH_SOURCE = "runtime.quicksilver.stuck-switch-test"
GAMEPLAY_SOURCE = "runtime.quicksilver.gameplay"
CALLOUT_SOURCE = "review.quicksilver.drawing-callouts"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/stern/quicksilver-1980-callouts.json"

MANUAL_SHA256 = "140216dc27e97084e0b523fe0d5ff5417961723fea069b1fad3dd594b9723728"
LAMP_SCHEMATIC_SHA256 = "bea05d384e1f7ddf2dc98793cc1c9c82a38aece048b6750fe67371b2262870ee"
SOLENOID_SCHEMATIC_SHA256 = "f71e59b6d72e7d1315eeb3eaca940479bd882d9d3bcbfb008905180f92078a5d"
MPU_SCHEMATIC_SHA256 = "c9e867b02441299f7d5e9ce0855c5432307420b3da77e21a998401551c20e2ae"
CARD_SHA256 = "f85d0a60e1a03bf904623816fa5747d64020a0a81192964915cd717180be3f67"
IPDB_PAGE_SHA256 = "f606cbcefc726c8fc77284101adfa7b30839e71b05879d4e0a3ed4f40c3a2ef6"
TABLE_SHA256 = "a81901b68745a1132c7fdb6fb3609a665a45b89b7bedb32348517c1a514c2b64"
SCRIPT_SHA256 = "44338d1e352558783d78c33ea1d575d4792fb843a1248e5427ecbe9eb9d0648a"
CORPUS_SCRIPT_SHA256 = "94f9f06f2ce2b617430f9fd525a3b012374b678860c673bd0fa61e58cb2ce944"
CORPUS_OLD_SCRIPT_SHA256 = "02908fc918da9debab8dfcf257d667803d7cab6361e97fd9e24338a356c59553"
CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
ARCHIVE_TABLE_SHA256 = "c30a8f9c08083e5732c287006c688b9c819295f5e886eb50f7f2d2991edf075f"
ARCHIVE_SCRIPT_SHA256 = "bb51e9d3390dad5cea1cc6fe7a128f2a4e309da753650981b9e9b51f2df18d82"
ARCHIVE_MANIFEST_SHA256 = "45c57819a3aa49c3dad717b23555b9d49c235fa9be9a45cf78d0f0be46baabe4"
ROM_ARCHIVE_SHA256 = "691e06ac64f445cde8842934efdc3a7e223b408f442131bcb2903bde56b45ad3"

EXTRACTION_RELATIVE_PATH = Path("stern/quicksilver-1980/vpw-1.0/Quicksilver (Stern 1980) VPW 1.0")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("stern/quicksilver-1980/vpw-1.0/Quicksilver (Stern 1980) VPW 1.0.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "87a93746e47a892290eea8ea03a4b68e70fa3dc73d838c0638392a61335b52bf"
EXTRACTION_FILE_COUNT = 1988
EXTRACTION_TOTAL_BYTES = 438666984

RUN_SHA256 = {
	"self-test": "e01a53727548bc5908d6193b982e8187766d259de80b467b3f9f9ca2213b0aa8",
	"stuck-switch": "32f014e6290a95dedcf541b9e1486710a8ef7e4f0b4634bd58c51c03194b2da3",
	"gameplay": "fc753e8985d83286390558accc71b9f854dec24a81383378f084d8bb7f45dbb7",
}
RUN_MANIFEST_SHA256 = {
	"self-test": "2558ae5402558e3d1ea7277c45093ff274271385bf298082339c6c5f885fe453",
	"stuck-switch": "836347eae78d76b90d2f7485e0294b5ae5685a488f490526384256662e988c4e",
	"gameplay": "6f361df4b4f857159a76702a683fa26c4da427f95617535827bf2deff42313a7",
}
SCENARIO_SHA256 = {
	"self-test": "fd7fa20ca62fbb24a4138cef55293a27855d00e29eaf52af41bc62dee7814e78",
	"stuck-switch": "dcc2f9ee3bb971fea21abaa56cddb4a413c0d15bd3027af9ac7d167c92fdc2aa",
	"gameplay": "fd817ffe7eb0d99f7b8788a79ecf677ce6ae56525c0be96a565fa80cc1e68e86",
}

# The retained table's own playfield bounds; every canonical coordinate is x/TABLE_WIDTH and y/TABLE_HEIGHT.
TABLE_WIDTH = 952.941
TABLE_HEIGHT = 1976.471
TABLE_BOUNDS = "left=0 top=0 right=952.941 bottom=1976.471"

BOARD_MPU = "MPU module M-200 A4"
BOARD_SDU = "Solenoid Driver / Voltage Regulator module SDU B-432 A3"
BOARD_LDA = "Lamp Driver module LDA B-431 A5"


def normalize(x: float, y: float) -> tuple[float, float]:
	return round(x / TABLE_WIDTH, 6), round(y / TABLE_HEIGHT, 6)


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "observed") -> dict[str, Any]:
	placements = []
	for index, (raw_x, raw_y) in enumerate(positions, start=1):
		x, y = normalize(raw_x, raw_y)
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": provenance(*source_refs, status=status),
		})
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def legacy_numeric(address: int) -> list[str]:
	"""The legacy corpus exposed each address bare, then two-digit, then three-digit."""
	return list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))


# --- Inputs -------------------------------------------------------------------------------------------------------------


def matrix_wiring(address: int, cabinet: bool) -> dict[str, Any]:
	strobe, row = (address - 1) // 8, (address - 1) % 8
	strobe_wire, strobe_connection = data.CABINET_STROBE0 if cabinet else data.STROBES[strobe]
	return_wire, return_connection = (data.CABINET_RETURNS[row] if cabinet else data.RETURNS[row])
	return {
		"board": BOARD_MPU,
		"control_wire": strobe_wire,
		"control_connection": strobe_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
	}


def build_inputs() -> list[dict[str, Any]]:
	inputs: list[dict[str, Any]] = []
	for address, spec in sorted(data.SERVICE_SWITCHES.items()):
		refs = {"manual-and-harness": (MANUAL_SOURCE, CORE_SOURCE, SELF_TEST_SOURCE), "core": (CORE_SOURCE,)}[spec["evidence"]]
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": spec["availability"],
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"normally_closed": False,
			"physical": {"location": "Coin door and MPU module", "notes": spec["notes"], "switch_type": "button"},
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
		refs = [MANUAL_SOURCE, SCRIPT_SOURCE, STUCK_SWITCH_SOURCE] if not cabinet else [MANUAL_SOURCE, STUCK_SWITCH_SOURCE]
		if address in (1, 2, 3, 6, 7) or address in (9, 10, 11, 12, 13, 21, 22, 23, 24, 28, 29, 30, 31, 32):
			refs.append(GAMEPLAY_SOURCE)
		physical: dict[str, Any] = {"switch_type": spec["type"]}
		if spec.get("quantity"):
			physical["quantity"] = spec["quantity"]
		physical["notes"] = spec["notes"]
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"normally_closed": False,
			"physical": physical,
			"provenance": provenance(*dict.fromkeys(refs)),
			"pulse": bool(spec.get("pulse", False)),
			"wiring": matrix_wiring(address, cabinet),
		}
		if spec.get("initial_active"):
			item["initial_active"] = True
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if spec.get("positions"):
			item["spatial"] = located(spec["id"], "sensor", spec["positions"], TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
		elif cabinet:
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
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
				"notes": "PinMAME's synthetic cabinet flipper button position (FLIP_SW(FLIP_L)). The physical button is hard-wired to the flipper circuit through the "
					"Solenoid Driver relay, not to the switch matrix; the retained gameplay run shows the ROM-side output answering this address.",
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, SOLENOID_SCHEMATIC_SOURCE, GAMEPLAY_SOURCE),
			"pulse": False,
			"roles": [role],
			"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
			"wiring": {"board": "Hard-wired flipper button circuit", "control_wire": wire, "control_connection": connection},
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
				"notes": "PinMAME's generic upper flipper button position. Quicksilver has two lower flippers only (parts list `FLIPPER (2)`); closing this address "
					"changed no output in the retained gameplay run.",
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE),
			"pulse": False,
			"spatial": not_applicable("unused", MANUAL_SOURCE, CORE_SOURCE),
		})

	for address in sorted(data.DIPS):
		inputs.append({
			"aliases": [
				{"namespace": "pinmame.dip", "value": str(address)},
				{"namespace": "manual.address", "value": "S%d" % address},
			],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.dip"},
			"id": "dip.option-switch-%d" % address,
			"kind": "dip_switch",
			"label": data.DIPS[address],
			"physical": {
				"switch_type": "dip",
				"notes": "One of the thirty-two MPU option switches in the back box, supplied as four sixteen-lead packages numbered S1-8, S9-16, S17-24 and S25-32 with the ON position marked on the assembly. "
					"The assignment is the `QUICK SILVER SWITCH ASSIGNMENT` figure of the manual. S33 on the same module is a momentary memory-clear pushbutton, not an option switch.",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE),
			"spatial": not_applicable("dip_switch", MANUAL_SOURCE),
		})

	for side, address in (("left", 1), ("right", 2)):
		flipper = data.FLIPPERS[48 if side == "left" else 46]
		inputs.append({
			"aliases": [{"namespace": "manual.address", "value": f"{side}-flipper-eos"}],
			"availability": "used",
			"binding": {"device": address, "group": "physical.input.direct"},
			"id": f"switch.{side}-flipper-end-of-stroke",
			"kind": "switch",
			"label": f"{side.title()} flipper end-of-stroke contact",
			"normally_closed": True,
			"physical": {
				"location": f"{side.title()} flipper assembly",
				"notes": "Hard-wired contact of the dual-winding flipper, not a PinMAME switch address. The manual's FLIPPER WIRING figure draws it across the first winding of the coil, so it conducts at rest "
					"and opens at the end of the stroke to insert the second winding (normally closed). Placed on the flipper it belongs to.",
				"switch_type": "leaf",
			},
			"provenance": provenance(MANUAL_SOURCE, SOLENOID_SCHEMATIC_SOURCE),
			"pulse": False,
			"spatial": located(f"switch.{side}-flipper-end-of-stroke", "sensor", flipper["positions"], TABLE_SOURCE, MANUAL_SOURCE),
		})
	return inputs


# --- Outputs ------------------------------------------------------------------------------------------------------------


def coil_wiring(spec: dict[str, Any], physical_number: int) -> dict[str, Any]:
	wiring: dict[str, Any] = {
		"board": BOARD_SDU,
		"driver_transistor": f"Q{physical_number}",
		"nominal_voltage_v": 43,
		"voltage_type": "dc",
	}
	if spec.get("wire"):
		wiring["drive_wire"] = spec["wire"]
	if spec.get("conn"):
		wiring["drive_connection"] = spec["conn"]
	return wiring


def build_solenoid_outputs() -> list[dict[str, Any]]:
	outputs: list[dict[str, Any]] = []
	for address, spec in sorted(data.SOLENOIDS.items()):
		physical_number = spec.get("phys") or next(number for number, public in data.PHYSICAL_TO_PUBLIC.items() if public == address)
		unused = bool(spec.get("unused"))
		aliases = [{"namespace": "pinmame.coil", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.self-test", "value": str(physical_number)})
		refs = [MANUAL_SOURCE, SOLENOID_SCHEMATIC_SOURCE, SELF_TEST_SOURCE]
		if not unused and address in (1, 2, 3, 4, 5, 7, 8, 9, 10, 19):
			refs.append(GAMEPLAY_SOURCE)
		physical: dict[str, Any] = {}
		if spec.get("part"):
			physical["part_number"] = spec["part"]
		physical["notes"] = spec["notes"]
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "unused" if unused else "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": spec["kind"],
			"label": spec["label"],
			"physical": physical,
			"provenance": provenance(*dict.fromkeys(refs)),
			"wiring": coil_wiring(spec, physical_number),
		}
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if unused:
			item["spatial"] = not_applicable("unused", MANUAL_SOURCE, SELF_TEST_SOURCE)
		elif spec.get("cabinet"):
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		elif spec.get("internal"):
			item["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, SOLENOID_SCHEMATIC_SOURCE)
		else:
			item["spatial"] = located(spec["id"], "effect", spec["positions"], TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
		outputs.append(item)

	for address, spec in sorted(data.FLIPPERS.items()):
		power = spec["power"]
		item = {
			"aliases": [
				{"namespace": "pinmame.coil", "value": str(address)},
				*({"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)),
				{"namespace": "vpe-legacy.coil", "value": f"c_flipper_lower_{spec['side']}"},
				{"namespace": "manual.self-test", "value": "15"},
			],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": "coil",
			"label": f"{spec['label']} (dual-winding coil)",
			"physical": {
				"part_number": "J-25-475/34-4500",
				"notes": f"Lower {spec['side']} flipper: a dual-winding coil with an end-of-stroke contact (parts list `FLIPPER (2)`, `J-25-475/34-4500`), hard-wired from the +43 VDC bus A2J1-6 (BLU-W) through the flipper-enable relay, "
					f"not driven by a numbered solenoid transistor. Public {address} is PinMAME's synthetic held-coil output for the {spec['side']} flipper (FLIP_SW(FLIP_L)); the same press also asserts public {power} for exactly the same interval "
					"(PinMAME's core asserts both bits of the pair while the button is closed); the Stern MPU-200 controller profile does not declare {power}, so this definition does not bind it.",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, SOLENOID_SCHEMATIC_SOURCE, GAMEPLAY_SOURCE),
			"spatial": located(spec["id"], "effect", spec["positions"], TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE),
			"wiring": {
				"board": "Hard-wired flipper circuit gated by the flipper-enable relay (public 19)",
				"control_connection": spec["button_conn"],
				"control_wire": spec["button_wire"],
				"drive_connection": spec["conn"],
				"drive_wire": spec["wire"],
				"nominal_voltage_v": 43,
				"power_connection": "A2J1-6",
				"power_wire": "BLU-W",
				"voltage_type": "dc",
			},
		}
		outputs.append(item)
	return outputs


def lamp_physical(address: int, spec: dict[str, Any]) -> dict[str, Any]:
	q = data.LAMP_TO_Q[address]
	k, a = divmod(address - 1, 16)
	detail = f"Lamp Driver SCR Q{q}, decoder U{k + 1} output S{a}"
	if spec["pins"]:
		detail += ", connector " + " and ".join(f"{jack} pin {pin}" for jack, pin in spec["pins"])
	detail += ". Discrete SCR circuit on the Lamp Driver module; this is not a row/column lamp matrix."
	if spec.get("notes"):
		detail += " " + spec["notes"]
	physical: dict[str, Any] = {"notes": detail}
	if spec.get("availability") not in ("unused",):
		physical["quantity"] = spec.get("quantity", 1)
	if spec.get("location"):
		physical["location"] = spec["location"]
	elif spec.get("backbox"):
		physical["location"] = "backbox"
	return physical


def build_lamp_outputs() -> list[dict[str, Any]]:
	outputs: list[dict[str, Any]] = []
	for address in sorted(data.LAMPS):
		spec = data.LAMPS[address]
		q = data.LAMP_TO_Q[address]
		availability = spec.get("availability", "used")
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.lamp", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.address", "value": f"Q{q}"})
		for jack, pin in spec["pins"]:
			aliases.append({"namespace": "manual.address", "value": f"LDA-{jack}-{pin}"})
		wiring: dict[str, Any] = {"board": BOARD_LDA, "driver_transistor": f"Q{q}"}
		if spec["pins"]:
			wiring["drive_connection"] = ", ".join(f"LDA {jack}-{pin}" for jack, pin in spec["pins"])
		if spec["wire"]:
			wiring["drive_wire"] = spec["wire"]
		refs = [LAMP_SCHEMATIC_SOURCE, SELF_TEST_SOURCE]
		if spec["pins"]:
			refs.insert(0, MANUAL_SOURCE)
		if spec.get("light"):
			refs.extend([TABLE_SOURCE, SCRIPT_SOURCE])
		elif address in (45, 61, 63, 13, 11):
			refs.append(SCRIPT_SOURCE)
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": availability,
			"binding": {"device": address, "group": "pinmame.output.lamp"},
			"id": spec["id"],
			"kind": "lamp",
			"label": spec["label"],
			"physical": lamp_physical(address, spec),
			"provenance": provenance(*dict.fromkeys(refs), status="observed" if availability == "unknown" else "validated"),
			"wiring": wiring,
		}
		if availability == "unused":
			item["spatial"] = not_applicable("unused", LAMP_SCHEMATIC_SOURCE, SELF_TEST_SOURCE)
			item["physical"].pop("location", None)
		elif spec.get("backbox"):
			item["roles"] = ["cabinet.backglass"]
			item["spatial"] = not_applicable("cabinet_or_service", LAMP_SCHEMATIC_SOURCE, CORE_SOURCE)
		elif spec.get("light"):
			item["spatial"] = located(spec["id"], "emitter", [data.LIGHTS[spec["light"]]], TABLE_SOURCE, SCRIPT_SOURCE, LAMP_SCHEMATIC_SOURCE)
		outputs.append(item)
	return outputs


def build_outputs() -> list[dict[str, Any]]:
	outputs = build_solenoid_outputs() + build_lamp_outputs()
	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return outputs


# --- Mechanisms, relationships --------------------------------------------------------------------------------------------


def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *sources: str, part: str | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {
		"actuators": actuators,
		"behavior": behavior,
		"id": identifier,
		"kind": kind,
		"label": label,
		"provenance": provenance(*sources),
		"sensors": sensors,
	}
	if part:
		item["assembly_part_number"] = part
	return item


def build_mechanisms() -> list[dict[str, Any]]:
	return [
		mechanism(
			"mech.out-hole", "Single-ball out-hole and shooter feed", "kicker", ["device.out-hole-kicker"], ["switch.outhole"],
			"Quicksilver is a single-ball machine: there is no trough. The known-working tables initialise the game with the ball on the out-hole switch (public 33). At game start the ROM "
			"kicks the out-hole (public 10, the JX-26-1200 out-hole kicker) and repeats the kick for as long as public 33 stays closed, which is what the retained gameplay run shows with the ball held on the switch. "
			"The kick delivers the ball to the shooter lane (the tables release it from the shooter-lane kicker at 90 degrees, strength 5) and the player launches it with the plunger. After every drain the bonus is "
			"counted, the player-up and ball-in-play advance, and the kick repeats.",
			MANUAL_SOURCE, SCRIPT_SOURCE, SOLENOID_SCHEMATIC_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.kick-out-hole", "Left kick-out hole", "kicker", ["device.kick-out-hole-eject"], ["switch.kick-out-hole"],
			"A hole at the left edge of the playfield (parts list `EJECT HOLE`, J-28-2300). A ball in the hole holds public 29 closed; the ROM answers with a pulse on public 9 that ejects it back into play "
			"(the retained gameplay run: closing 29 fires 9 once, and 9 also pulses once at game start). The instruction card says the kick-out target scores 5,000 and advances the center target value. "
			"The known-working VPW table ejects at 150 degrees, velocity 15, with a 5 vertical velocity; the older retained table's saucer ejects at 110 degrees, force 7.",
			MANUAL_SOURCE, SCRIPT_SOURCE, ARCHIVE_SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.center-drop-bank", "Center four-target drop bank", "drop_target_bank", ["device.center-bank-reset"],
			["switch.center-drop-target-1", "switch.center-drop-target-2", "switch.center-drop-target-3", "switch.center-drop-target-4"],
			"Four drop targets in a slanted line across the middle of the playfield (`4 Bank Target D-580-4`), numbered 1 (highest) to 4 (lowest). A target's switch closes while it is down; one reset coil (public 7, B-27-2300) "
			"raises the whole bank and there are no individual down coils. Home state is all four up. The ROM resets the bank at game start and again when the fourth target closes (retained gameplay run: public 7 fires on the closure of 24). "
			"Each target scores 1,000 plus its lit value, and downing all four spots the next letter (instruction card). The center-bank value inserts are public lamps 4, 20, 36 and 52.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, CARD_SOURCE, part="D-580-4",
		),
		mechanism(
			"mech.right-drop-bank", "Right three-target drop bank", "drop_target_bank", ["device.right-bank-reset"],
			["switch.right-drop-target-1", "switch.right-drop-target-2", "switch.right-drop-target-3"],
			"Three drop targets in a vertical line beside the right rail (`3 Bank Target D-580-3`), numbered 1 (highest) to 3 (lowest), with one reset coil (public 8, B-27-2300). Home state is all three up. The ROM resets it "
			"at game start and when the third target closes (retained gameplay run: public 8 fires on the closure of 32). Downing the bank raises the bonus multiplier (instruction card); the multiplier inserts are public lamps 7, 23, 39 and 55 and the bank's 25,000 insert is 8.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, CARD_SOURCE, part="D-580-3",
		),
		mechanism(
			"mech.spinners", "Left and right spinning targets", "other", [], ["switch.left-spinner", "switch.right-spinner"],
			"Two spin target assemblies (`14A-7-13`, target and wire only), one on each side. Each completed rotation closes the contact once and scores 200 in the retained gameplay run. "
			"Their lamps are public 62 (left) and 46 (right); per the instruction card the spinner value increases when the ball enters the opposite return lane and must be re-lit after the spinner is hit.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, CARD_SOURCE, LAMP_SCHEMATIC_SOURCE,
		),
		mechanism(
			"mech.thumper-bumpers", "Three thumper bumpers", "kicker",
			["device.right-thumper-bumper", "device.left-thumper-bumper", "device.lower-thumper-bumper"],
			["switch.right-pop-bumper", "switch.left-pop-bumper", "switch.bottom-pop-bumper"],
			"Three J-26-1200 thumper bumpers. The ROM fires each coil when its own switch closes and scores 1,000: switch 9 (right) fires public 1, switch 10 (left) public 2 and switch 11 (bottom) public 3, all proved in the "
			"retained gameplay run. The printed solenoid numbers are 2 (right), 1 (left) and 5 (lower).",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, SELF_TEST_SOURCE,
		),
		mechanism(
			"mech.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"],
			["switch.left-slingshot", "switch.right-slingshot"],
			"Two J-26-1500 slingshots. The ROM fires each coil when its switch closes and scores 10: switch 12 (left) fires public 4 and switch 13 (right) public 5 (retained gameplay run). The printed solenoid numbers are 6 and 7.",
			MANUAL_SOURCE, SCRIPT_SOURCE, ARCHIVE_SCRIPT_SOURCE, GAMEPLAY_SOURCE, SELF_TEST_SOURCE,
		),
		mechanism(
			"mech.flippers", "Two lower dual-winding flippers", "other",
			["device.left-flipper", "device.right-flipper", "device.flipper-enable-relay"],
			["switch.lower-left-flipper-button", "switch.lower-right-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-end-of-stroke"],
			"Two lower flippers (`FLIPPER (2)`, J-25-475/34-4500), each a dual-winding coil fed from the +43 VDC bus A2J1-6 (BLU-W) through the Solenoid Driver's flipper-enable relay. The relay is driven by public 19 (printed solenoid 15, Q15): "
			"the ROM raises it when a game starts and drops it when a tilt closes switch 7 (retained gameplay run). The cabinet buttons are hard-wired to the circuit on A3J2-2 (left, BLU) and A3J2-1 (right, R); PinMAME represents them as "
			"public switches 84 and 82 and the coils as public 48 and 46. Each assembly's end-of-stroke contact is closed at rest and opens at the end of the stroke, inserting the second winding to hold the flipper.",
			MANUAL_SOURCE, SOLENOID_SCHEMATIC_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE,
		),
	]


def build_relationships() -> list[dict[str, Any]]:
	direct = [
		("switch.right-pop-bumper", "device.right-thumper-bumper"),
		("switch.left-pop-bumper", "device.left-thumper-bumper"),
		("switch.bottom-pop-bumper", "device.lower-thumper-bumper"),
		("switch.left-slingshot", "device.left-slingshot"),
		("switch.right-slingshot", "device.right-slingshot"),
	]
	relationships = [
		{"id": f"rel.{destination.split('.', 1)[1]}-energized-by-its-switch", "kind": "direct", "source": source, "destination": destination, "provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)}
		for source, destination in direct
	]
	relationships.append({"id": "rel.out-hole-kicker-follows-the-out-hole-switch", "kind": "pulse", "source": "switch.outhole", "destination": "device.out-hole-kicker", "provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.kick-out-hole-eject-follows-its-switch", "kind": "pulse", "source": "switch.kick-out-hole", "destination": "device.kick-out-hole-eject", "provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.left-flipper-button-gated-by-the-enable-relay", "kind": "relay_gated", "source": "switch.lower-left-flipper-button", "destination": "device.left-flipper", "provenance": provenance(MANUAL_SOURCE, SOLENOID_SCHEMATIC_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.right-flipper-button-gated-by-the-enable-relay", "kind": "relay_gated", "source": "switch.lower-right-flipper-button", "destination": "device.right-flipper", "provenance": provenance(MANUAL_SOURCE, SOLENOID_SCHEMATIC_SOURCE, GAMEPLAY_SOURCE)})
	relationships.sort(key=lambda item: item["id"])
	return relationships


# --- Sources ------------------------------------------------------------------------------------------------------------

# (source key, excerpt id suffix, markdown file stem, image file or None, locator, image derivation or None)
PDF = "Stern_1980_Quicksilver_Manual.pdf"
LDA_JPG = "Stern_1980_Quicksilver_Lamp_Driver_Schematic.jpg"
SDU_JPG = "Stern_1980_Quicksilver_Solenoid_Driver_Schematic.jpg"


def _pdf_crop(page: int, box: str, width: int, name: str = PDF) -> str:
	return f"{name} page {page}, crop box {box} of the page, rendered at 300 dpi with pdftoppm, reduced to {width}px wide grayscale, quality 75 WebP"


def _jpg_crop(name: str, box: str, width: int, scale: str = "") -> str:
	return f"{name} (scanned JPEG), pixel crop box {box}{scale}, reduced to {width}px wide grayscale WebP"


EXCERPTS: dict[str, list[tuple[str, str, str | None, str, str | None]]] = {
	MANUAL_SOURCE: [
		("switch-identification", "switch-identification", "webp", "PDF page 16, QUICK SILVER SWITCH IDENTIFICATION SELF TEST DISPLAY NUMBERS, all 40 rows and the three-chute drawing", _pdf_crop(16, "0.0,0.04,0.95,0.77", 1100)),
		("switch-locations", "switch-locations", "webp", "PDF page 17, SWITCHES QUICKSILVER location drawing and the list of switches not on the playfield", _pdf_crop(17, "0.0,0.0,1.0,1.0", 1400)),
		("solenoid-identification", "solenoid-identification", "webp", "PDF page 14, solenoid and SDU Q transistor numbers 1-29", _pdf_crop(14, "0.10,0.04,0.80,0.51", 1000)),
		("solenoid-locations", "solenoid-locations", "webp", "PDF page 15, SOLENOIDS QUICKSILVER location drawing", _pdf_crop(15, "0.0,0.0,1.0,1.0", 1400)),
		("playfield-switch-matrix", "playfield-switch-matrix", "webp", "PDF page 20, wiring diagram 12B-432-S-117 sheet 2 of 3, playfield switch matrix (five strobes by eight returns)", _pdf_crop(20, "0.13,0.10,0.76,0.80", 1400)),
		("cabinet-switch-matrix", "cabinet-switch-matrix", "webp", "PDF page 22, cabinet and door wiring 12B-432-S-121, test switch and cabinet matrix", _pdf_crop(22, "0.17,0.06,0.76,0.80", 1400)),
		("front-door-jack", "front-door-jack", "webp", "PDF page 23, cabinet and front door wiring, FRONT DOOR JACK pin table", _pdf_crop(23, "0.50,0.43,0.85,0.71", 700)),
		("playfield-coil-wiring-sheet-a", "playfield-coil-wiring-sheet-a", "webp", "PDF page 20, right part of the playfield wiring diagram: left flipper and the left-hand coils", _pdf_crop(20, "0.74,0.10,1.0,0.64", 800)),
		("playfield-coil-wiring-sheet-b", "playfield-coil-wiring-sheet-b", "webp", "PDF page 21, left edge of the playfield wiring diagram: right flipper, out-hole and the right-hand coils", _pdf_crop(21, "0.0,0.10,0.30,0.64", 700)),
		("playfield-lamp-wiring-list-a", "playfield-lamp-wiring-list-a", "webp", "PDF page 21, typed playfield lamp wiring list, rows 1-23", _pdf_crop(21, "0.42,0.14,0.78,0.45", 900)),
		("playfield-lamp-wiring-list-b", "playfield-lamp-wiring-list-b", "webp", "PDF page 21, typed playfield lamp wiring list, rows 24-50", _pdf_crop(21, "0.42,0.43,0.78,0.75", 900)),
		("mpu-switch-assignment", "mpu-switch-assignment", "webp", "PDF page 9, QUICK SILVER SWITCH ASSIGNMENT for the thirty-two MPU option switches", _pdf_crop(9, "0.15,0.39,0.85,0.84", 1100)),
		("parts-list", "parts-list", "webp", "PDF page 19, PARTS LIST QUICK SILVER", _pdf_crop(19, "0.0,0.05,1.0,0.55", 1000)),
		("flipper-wiring", "flipper-wiring", "webp", "PDF page 7, generic FLIPPER WIRING figure", _pdf_crop(7, "0.0,0.30,1.0,0.80", 1100)),
		("self-test", "self-test", None, "PDF page 4, II. ROUTINE MAINTENANCE ON LOCATION, MPU module and game self-diagnostic tests", None),
		("general-operation", "general-operation", None, "PDF page 5, IV. GENERAL GAME OPERATION", None),
	],
	LAMP_SCHEMATIC_SOURCE: [
		("lamp-driver-lamp-list-a", "lamp-driver-lamp-list-a", "webp", "Lamp Driver Schematic 12B-432-S-116, printed lamp list, first part", _jpg_crop(LDA_JPG, "1650,100,2330,820", 900)),
		("lamp-driver-lamp-list-b", "lamp-driver-lamp-list-b", "webp", "Lamp Driver Schematic 12B-432-S-116, printed lamp list, second part and the title block", _jpg_crop(LDA_JPG, "1650,780,2330,1000", 900)),
		("lamp-driver-connector-labels", "lamp-driver-connector-labels", "webp", "Lamp Driver Schematic 12B-432-S-116, connector blocks J1, J2 and J3 with their SCR labels", _jpg_crop(LDA_JPG, "1480,90,1640,545; 1480,530,1640,870; 1480,850,1640,1480 (three blocks side by side)", 1000, ", each block scaled 2x")),
		("lamp-driver-decoder-outputs", "lamp-driver-decoder-outputs", "webp", "Lamp Driver Schematic 12B-432-S-116, decoder chips U1-U4 with their output resistors and SCRs", _jpg_crop(LDA_JPG, "560,140,1250,1400", 1380, ", scaled 2x")),
	],
	SOLENOID_SCHEMATIC_SOURCE: [
		("solenoid-driver-j2-pins", "solenoid-driver-j2-pins", "webp", "Solenoid Driver Schematic 12B-432-S-117 sheet 3 of 3, J2 coil pin table", _jpg_crop(SDU_JPG, "100,570,340,850", 600)),
		("solenoid-driver-j5-pins", "solenoid-driver-j5-pins", "webp", "Solenoid Driver Schematic 12B-432-S-117 sheet 3 of 3, J1 and J5 coil pins and their notes", _jpg_crop(SDU_JPG, "780,420,1090,830", 800)),
		("solenoid-driver-flipper-section", "solenoid-driver-flipper-section", "webp", "Solenoid Driver Schematic 12B-432-S-117 sheet 3 of 3, flipper, flipper-enable relay and continuous-output section", _jpg_crop(SDU_JPG, "850,70,1601,500", 1300)),
	],
	CARD_SOURCE: [
		("instruction-card", "instruction-card", "webp", "Instruction card, QUICK SILVER", _pdf_crop(1, "0.06,0.01,0.73,0.31", 1000, "Stern_1980_Quicksilver_Instruction_Card.pdf")),
	],
}

INSTRUCTION_CARD_TEXT = """Source: `Stern_1980_Quicksilver_Instruction_Card.pdf` (IPDB machine 1895, "Instruction Card [Stern Electronics, Inc.]", one page, 300 dpi color JPEG scan of a typed
instruction card). Transcribed by hand from the render; every line below was checked against it.

Heading, verbatim: `QUICK SILVER`.

| Feature | Card text, verbatim |
| --- | --- |
| POP BUMPERS: | SCORE 1000 |
| BONUS MULTIPLIER: | INCREASES WHEN RIGHT 3 BANK TARGETS DOWN. |
| ADVANCE BONUS: | Q-U-I-C-K S-I-L-V-E-R TARGETS ADVANCE BONUS ONLY WHEN NOT LIT. 75,000 BONUS LITES AFTER MAXIMUM 20,000 IS LIT. LIT 75,000 DOES NOT COLLECT MULTIPLIER. |
| SPECIAL: | ALL Q-U-I-C-K S-I-L-V-E-R TARGETS LIT. LITES TOP AND OUTLANE SPECIAL. |
| SPINNERS: | INCREASED VALUE WHEN BALL ENTERS OPPOSITE RETURN LANE. MUST BE RE-LIT AFTER HITTING SPINNER. |
| KICKOUT TARGET: | SCORES 5,000 AND ADVANCES CENTER TARGET VALUE. |
| CENTER BANK: | EACH TARGET SCORES 1,000 PLUS LIT VALUE. ALL TARGETS DOWN SPOT NEXT LETTER. |
| EXTRA BALL: | SPOTTING Q-U-I-C-K TARGETS, THEN HITTING FLASHING TARGET AWARDS EXTRA BALL. |
| TILT: | DISQUALIFIES BALL IN PLAY ONLY. |
"""


def excerpt_record(source_key: str, entry: tuple[str, str, str | None, str, str | None]) -> dict[str, Any]:
	name, stem, image_ext, locator, derivation = entry
	record: dict[str, Any] = {
		"id": f"excerpt.quicksilver.{name}",
		"locator": locator,
		"method": "manual",
		"path": f"{EXCERPT_ROOT}/{stem}.md",
		"reviewed": True,
		"sha256": f"@{stem}.md",
		"transcribed_by": "curator, read from the retained rendered page",
	}
	if image_ext:
		record["image"] = f"{EXCERPT_ROOT}/{stem}.{image_ext}"
		record["image_sha256"] = f"@{stem}.{image_ext}"
		record["image_derivation"] = derivation
	if name in ("self-test", "general-operation"):
		record["method"] = "mixed"
		record["transcribed_by"] = "curator, Windows.Media.Ocr text checked line by line against the rendered page"
	return record


def build_sources() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "src/wpc/stgames.c CORE_GAMEDEFNV(quicksil) and the three CORE_CLONEDEFNV entries quicksfp, quicksib and quicksic that name it as parent",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "src/wpc/stgames.c INITGAME(quicksil, GEN_STMPU200, dispst7, FLIP_SW(FLIP_L), 0, SNDBRD_ST300, 0) and the identical INITGAME lines of quicksfp, quicksib and quicksic; "
				"src/wpc/by35.c by35_lampStrobe, the solenoid selector and the continuous-output nibble; src/wpc/core.h CORE_FIRSTLFLIPSOL and the sLRFlip/sLLFlip power and hold addresses 45-48",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/stern-mpu200.json",
			"revision": "repository",
			"locator": "Stern MPU-200 controller profile: matrix 1-40, diagnostics -7 to -5, flipper-button positions 81-84, DIP banks 1-32, decoder solenoids 1-15 and continuous 17-20 with synthetic flipper outputs 46 and 48, sixty discrete SCR lamps 1-63",
			"license": "MIT",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/1895/Stern_1980_Quicksilver_Manual.pdf",
			"original_filename": PDF,
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-02T00:00:00Z",
			"locator": "Stern Quicksilver game manual (IPDB 1895 `English Manual [Stern Electronics]`), 35 pages, 300 dpi bilevel scan without a text layer, retained at "
				"external:pinmame-manuals/by-machine/stern.quicksilver.1980/ipdb/. Retrieved through the Internet Archive's Wayback Machine copy of the IPDB file because IPDB is Cloudflare-gated. "
				"Pages 4-5 operation and self test, 7 flipper wiring, 9-13 option switches, 14-15 solenoids, 16-17 switches, 18-19 playfield and parts, 20-21 playfield wiring diagram 12B-432-S-117, 22-23 cabinet wiring 12B-432-S-121.",
			"license": "NOASSERTION",
			"attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [excerpt_record(MANUAL_SOURCE, entry) for entry in EXCERPTS[MANUAL_SOURCE]],
		},
		{
			"id": LAMP_SCHEMATIC_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/1895/Stern_1980_Quicksilver_Lamp_Driver_Schematic.jpg",
			"original_filename": LDA_JPG,
			"sha256": LAMP_SCHEMATIC_SHA256,
			"acquired_at": "2026-10-02T00:00:00Z",
			"locator": "Lamp Driver Schematic 12B-432-S-116 sheet 1 of 3, a 2330x1555 pixel JPEG. The title block names `CHEETAH` struck through by hand and `Quicksilver` written beside it: the drawing was relabelled for this game. "
				"It carries the complete 54-row lamp list, the connector blocks J1-J3 with SCR labels and the four MC14514B decoders U1-U4. Retained at external:pinmame-manuals/by-machine/stern.quicksilver.1980/ipdb/.",
			"license": "NOASSERTION",
			"attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [excerpt_record(LAMP_SCHEMATIC_SOURCE, entry) for entry in EXCERPTS[LAMP_SCHEMATIC_SOURCE]],
		},
		{
			"id": SOLENOID_SCHEMATIC_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/1895/Stern_1980_Quicksilver_Solenoid_Driver_Schematic.jpg",
			"original_filename": SDU_JPG,
			"sha256": SOLENOID_SCHEMATIC_SHA256,
			"acquired_at": "2026-10-02T00:00:00Z",
			"locator": "Solenoid Driver / Voltage Regulator Schematic 12B-432-S-117 sheet 3 of 3 `FOR QUICK SILVER`, a 1601x1097 pixel JPEG: J1/J2/J5 coil pins with wire colours, the flipper-enable relay and the continuous outputs. "
				"Retained at external:pinmame-manuals/by-machine/stern.quicksilver.1980/ipdb/.",
			"license": "NOASSERTION",
			"attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [excerpt_record(SOLENOID_SCHEMATIC_SOURCE, entry) for entry in EXCERPTS[SOLENOID_SCHEMATIC_SOURCE]],
		},
		{
			"id": CARD_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/1895/Stern_1980_Quicksilver_Instruction_Card.pdf",
			"original_filename": "Stern_1980_Quicksilver_Instruction_Card.pdf",
			"sha256": CARD_SHA256,
			"acquired_at": "2026-10-02T00:00:00Z",
			"locator": "Stern Quicksilver instruction card (IPDB 1895 `Instruction Card [Stern Electronics, Inc.]`), the game's rules summary, retained at external:pinmame-manuals/by-machine/stern.quicksilver.1980/ipdb/.",
			"license": "NOASSERTION",
			"attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [excerpt_record(CARD_SOURCE, entry) for entry in EXCERPTS[CARD_SOURCE]],
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=1895",
			"sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-10-02T00:00:00Z",
			"locator": "IPDB machine 1895: Quicksilver, Stern Electronics, June 1980, model number 117, MPU Stern M-200, 1,201 units, design Joe Joos Jr., art Doug Watson, software Bill Pfutzenreuter; notable features "
				"'Flippers (2), Pop bumpers (3), Slingshots (2), 4-bank drop targets (1), 3-bank drop targets (1), Standup targets (7), Spinning targets (2), Kick-out hole (1)'. Retrieved through the Wayback Machine capture of the IPDB page; "
				"the title and machine number were checked against the page itself, and the retained manual, schematics and card were downloaded from the links on it.",
			"license": "NOASSERTION",
			"attribution": "The Internet Pinball Database",
		},
		{
			"id": TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/quicksilver-1980/vpw-1.0/Quicksilver (Stern 1980) VPW 1.0.vpx",
			"original_filename": "Quicksilver (Stern 1980) VPW 1.0.vpx",
			"sha256": TABLE_SHA256,
			"revision": "VPW 1.0",
			"locator": f"Quicksilver (Stern 1980) VPW 1.0, a Visual Pixel Wizards Blender-baked recreation by MetaTed with playfield art by BorgDog, 257466368 bytes, from the operator's table folder. Exact playfield bounds {TABLE_BOUNDS}; "
				"normalized coordinates are x/952.941 and y/1976.471. The geometry authority for every located placement. A raw object-centre dump is retained at external:pinmame-review-artifacts/quicksilver-1980/vpw-geometry.tsv.",
			"license": "NOASSERTION",
			"attribution": "MetaTed and the Visual Pixel Wizards team; BorgDog (playfield image)",
			"rights": "NOASSERTION",
			"known_working": True,
		},
		{
			"id": SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/stern/quicksilver-1980/vpw-1.0/Quicksilver (Stern 1980) VPW 1.0/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"locator": "Embedded script of the retained VPW 1.0 table, 188204 bytes, cGameName = \"quicksic\" and UseLamps = 1: SolCallback(7-10) for the drop banks, kick-out hole and out-hole, vpmMapLights InsertLamps (a light's TimerInterval is its lamp number), "
				"UpdateMultipleLamps for lamps 45, 13, 63, 61 and 11, Controller.Switch/PulseSw calls for switches 4-5, 9-11, 14-40. The runtime address and causality authority. It is identical to the pinned corpus script apart from trailing whitespace.",
			"license": "NOASSERTION",
			"attribution": "MetaTed and the Visual Pixel Wizards team",
			"known_working": True,
		},
		{
			"id": CORPUS_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{CORPUS_REVISION}/Quicksilver%20%28Stern%201980%29%201.0.vbs",
			"revision": CORPUS_REVISION,
			"sha256": CORPUS_OLD_SCRIPT_SHA256,
			"locator": "Quicksilver (Stern 1980) 1.0.vbs in the pinned known-working script corpus (cGameName = \"quicksil\", Light Numbers by Destruk): the earlier community table's script, whose sling handlers pulse switches 12 and 13. "
				"The VPW 1.0 script in the same corpus (SHA-256 94f9f06f2ce2b617430f9fd525a3b012374b678860c673bd0fa61e58cb2ce944) is the retained table's script. The earlier script shares ancestry with the retained table, so it supplements and does not corroborate independently.",
			"license": "NOASSERTION",
			"attribution": "sverrewl/vpxtable_scripts contributors; Destruk (light numbers)",
			"known_working": True,
		},
		{
			"id": ARCHIVE_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/quicksilver-1980/Quicksilver (Stern 1980).vpx",
			"original_filename": "Quicksilver (Stern 1980).vpx",
			"sha256": ARCHIVE_TABLE_SHA256,
			"locator": "Earlier community Quicksilver table from the operator's Tables Archive, 29216768 bytes, playfield bounds left=0 top=0 right=952 bottom=1974. Extraction manifest SHA-256 "
				f"{ARCHIVE_MANIFEST_SHA256}, 783 files, 37809418 bytes. Used only as a supplement: its lamp lights agree with the retained VPW table to within 0.026 normalized, but it shares the numbering of the same ancestral light list, "
				"and its Bumper1 and Bumper2 objects are on the opposite sides from the switches their handlers pulse (left object pulses the right bumper's switch 9), which is that table's defect.",
			"license": "NOASSERTION",
			"attribution": "Community VPX table authors; redistribution rights not granted",
			"rights": "NOASSERTION",
		},
		{
			"id": ARCHIVE_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/stern/quicksilver-1980/Quicksilver (Stern 1980)/script.vbs",
			"original_filename": "script.vbs",
			"sha256": ARCHIVE_SCRIPT_SHA256,
			"locator": "Embedded script of the earlier retained table, 21920 bytes, cGameName = \"quicksil\": vpmTimer.PulseSw 12 and 13 from the slingshots, bsKicker.InitSaucer sw29,29,110,7 for the kick-out hole, bsTrough.InitSw 0,33 with one ball.",
			"license": "NOASSERTION",
			"attribution": "Community VPX table authors; redistribution rights not granted",
			"known_working": True,
		},
		{
			"id": CALLOUT_SOURCE,
			"kind": "human_review",
			"uri": "internal:tools/seeds/stern/quicksilver-1980-callouts.json",
			"sha256": hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest(),
			"locator": "2026-10-02 factory location-drawing callout check of the manual's switch drawing (PDF page 17) and solenoid drawing (PDF page 15): every callout transcribed independently on gridded tiles of the retained 300 dpi renders, no read corrected, "
				"per-page control and callout fits; a table placement whose own callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays and tiles are retained under external:pinmame-review-artifacts/quicksilver-1980/callout-check with a pinned manifest.",
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs contributors",
			"rights": "NOASSERTION",
		},
		{
			"id": EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/quicksilver-1980/vpw-1.0/Quicksilver (Stern 1980) VPW 1.0",
			"sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": f"Retained vpxtool 0.33.3 extraction of the VPW 1.0 table; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes. "
				"Manifest algorithm: canonical JSON of format/version and every file as sorted relative POSIX path, byte size and SHA-256.",
			"license": "NOASSERTION",
			"attribution": "MetaTed and the Visual Pixel Wizards team; redistribution rights not granted",
		},
		{
			"id": SELF_TEST_SOURCE,
			"kind": "service_diagnostic",
			"uri": "external:pinmame-review-artifacts/quicksilver-1980/harness/self-test/run.json",
			"sha256": RUN_SHA256["self-test"],
			"locator": f"tools/run_pinmame_harness.py with pinmame64.dll SHA-256 {LIBRARY_SHA256} (built from {PINMAME_REVISION[:12]}), driver quicksil, ROM archive SHA-256 {ROM_ARCHIVE_SHA256}; scenario tools/harness-scenarios/stern/quicksilver-self-test.json "
				f"(SHA-256 {SCENARIO_SHA256['self-test']}): one Self Test press after the 25 s power-up test, observed for 60 s. Canonical external manifest SHA-256 {RUN_MANIFEST_SHA256['self-test']}. Shows all sixty lamp addresses driven, the decoder holes 16/32/48/64 absent, "
				"and the repeating 19-step solenoid sequence 2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18.",
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": STUCK_SWITCH_SOURCE,
			"kind": "service_diagnostic",
			"uri": "external:pinmame-review-artifacts/quicksilver-1980/harness/stuck-switch/run.json",
			"sha256": RUN_SHA256["stuck-switch"],
			"locator": f"Same emulator and ROM as the self-test run; scenario tools/harness-scenarios/stern/quicksilver-stuck-switch.json (SHA-256 {SCENARIO_SHA256['stuck-switch']}): five Self Test presses reach the stuck-switch display, then every matrix address 1-40 is closed alone. "
				f"The Player Score display reads the closed address's own number for all forty. Canonical external manifest SHA-256 {RUN_MANIFEST_SHA256['stuck-switch']}.",
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": GAMEPLAY_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-review-artifacts/quicksilver-1980/harness/gameplay/run.json",
			"sha256": RUN_SHA256["gameplay"],
			"locator": f"Same emulator and ROM; scenario tools/harness-scenarios/stern/quicksilver-gameplay.json (SHA-256 {SCENARIO_SHA256['gameplay']}): three coins, the credit button and a released out-hole start a game, then each playfield switch is closed alone. "
				f"Records the score and solenoid response of every switch, the drop-bank resets, the kick-out eject, the flipper outputs and the tilt. Canonical external manifest SHA-256 {RUN_MANIFEST_SHA256['gameplay']}.",
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
	]


# --- Definition ---------------------------------------------------------------------------------------------------------


def build() -> dict[str, Any]:
	return {
		"conflicts": [],
		"controller": {"inversion_applied_by_emulator": True, "platform": "pinmame.stern-mpu200"},
		"coverage": {
			"dimensions": {
				"address_enumeration": "validated",
				"catalog_identity": "validated",
				"mechanisms": "validated",
				"physical_wiring": "validated",
				"recreation_knowledge": "validated",
				"semantic_naming": "observed",
				"spatial_placement": "observed",
				"variant_coverage": "validated",
			},
			"missing": ["output_semantics", "spatial_placement"],
			"status": "partial",
		},
		"displays": [
			{
				"controller_index": index,
				"id": identifier,
				"kind": "segment",
				"label": label,
				"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
				"segment_start": start,
				"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
				"width": width,
			}
			for identifier, label, index, start, width in data.DISPLAYS
		],
		"drivers": [
			{
				"description": data.DRIVERS[driver_id][0],
				"flags": 0,
				"id": driver_id,
				"manufacturer": data.DRIVERS[driver_id][2],
				"physical_compatibility": "identical",
				"variant_notes": data.DRIVERS[driver_id][4],
				"year": data.DRIVERS[driver_id][1],
				**({"clone_of": data.DRIVERS[driver_id][3]} if data.DRIVERS[driver_id][3] else {}),
			}
			for driver_id in sorted(data.DRIVERS)
		],
		"format": "pinmame-machine-definition",
		"inputs": build_inputs(),
		"knowledge": {"path": "knowledge/stern/quicksilver-1980.md", "status": "complete"},
		"machine": {
			"id": MACHINE_ID,
			"ipdb_id": 1895,
			"kind": "physical_pinball",
			"manufacturer": "Stern",
			"model_number": "117",
			"name": "Quicksilver",
			"opdb_id": "GRBZl-Mb5Zq",
			"playfield": {
				"height": TABLE_HEIGHT,
				"provenance": provenance(TABLE_SOURCE),
				"units": "vpx",
				"width": TABLE_WIDTH,
			},
			"year": 1980,
		},
		"mechanisms": build_mechanisms(),
		"outputs": build_outputs(),
		"relationships": build_relationships(),
		"schema_version": 2,
		"sources": build_sources(),
	}


def resolve_excerpt_digests(document: dict[str, Any], root: Path) -> None:
	"""Replace ``@<file>`` digest placeholders with the real digest of the committed excerpt."""
	for source in document["sources"]:
		for excerpt in source.get("excerpts", []) or []:
			for field in ("sha256", "image_sha256"):
				value = excerpt.get(field)
				if isinstance(value, str) and value.startswith("@"):
					target = root / EXCERPT_ROOT / value[1:]
					if not target.is_file():
						raise RuntimeError(f"Quicksilver excerpt is missing: {target}")
					excerpt[field] = hashlib.sha256(target.read_bytes()).hexdigest()


def callout_seed(root: Path = ROOT) -> dict[str, Any]:
	return json.loads((root / CALLOUT_SEED_PATH.relative_to(ROOT)).read_text(encoding="utf-8"))


def build_definition(root: Path = ROOT) -> dict[str, Any]:
	document = build()
	resolve_excerpt_digests(document, root)
	drawing_callouts.apply_to_definition(document, callout_seed(root), CALLOUT_SOURCE)
	return document


# --- Spatial report -----------------------------------------------------------------------------------------------------


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	placements = 0
	resolved_inputs: list[int] = []
	resolved_direct: list[int] = []
	resolved_outputs: list[dict[str, Any]] = []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	no_spatial_inputs: list[int] = []
	no_spatial_outputs: list[dict[str, Any]] = []
	for item in definition["inputs"]:
		binding = item["binding"]
		address = binding["device"]
		spatial = item.get("spatial")
		direct = binding["group"] == "physical.input.direct"
		if spatial is None:
			no_spatial_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			na_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			placements += len(spatial["placements"])
			(resolved_direct if direct else resolved_inputs).append(address)
	for item in definition["outputs"]:
		binding = {"address": item["binding"]["device"], "group": item["binding"]["group"]}
		spatial = item.get("spatial")
		if spatial is None:
			no_spatial_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			na_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placements += len(spatial["placements"])
			resolved_outputs.append(binding)
	projections = [
		{"address": address, "group": "pinmame.output.solenoid", "reason": data.SOLENOIDS[address]["projection"]}
		for address in sorted(data.SOLENOIDS)
		if data.SOLENOIDS[address].get("projection")
	]
	projections += [
		{"address": address, "group": "physical.input.direct", "reason": f"Placed on the {side} flipper object (its centre) because the end-of-stroke contact is mounted on the flipper assembly and has no object of its own."}
		for address, side in ((1, "left"), (2, "right"))
	]
	projections += [
		{"address": address, "group": "pinmame.output.solenoid", "reason": f"The {spec['label'].lower()} coil is placed on the flipper object it drives (its centre)."}
		for address, spec in sorted(data.FLIPPERS.items())
	]
	statuses: dict[str, int] = {}
	for item in [*definition["inputs"], *definition["outputs"]]:
		for placement in (item.get("spatial") or {}).get("placements") or []:
			statuses[placement["provenance"]["status"]] = statuses.get(placement["provenance"]["status"], 0) + 1
	seed = callout_seed()
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition))
	check = drawing_callouts.summary(seed, decisions, CALLOUT_SEED_PATH.relative_to(ROOT).as_posix(), hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest())
	return {
		"blockers": [
			"Five lamp addresses have no spatial key because the retained tables model no light for them: the top roll-over dividers, public 10, 26, 42, 57 and 58. They are fitted (the Lamp Driver Schematic's list names them "
			"`TOP R.O. DIVIDERS (L TO R)`, five rows), but no retained object lies on them and the manual's playfield drawings carry no lamp-location page.",
			"Public lamp 6 (SCR Q10) has no spatial key and is unresolved: no lamp list prints a load for it, yet the ROM drives it in the attract-mode lamp pattern. See the knowledge note.",
			"Every lamp placement is `observed`, not `validated`: it comes from one retained factory-layout table, the manual carries no lamp-location drawing, and the earlier retained table agrees on the lamps to within 0.026 normalized but shares their numbering and "
			"the ancestral light list, so it only supplements. The callout check validated the switch and solenoid placements that agree with the manual's two location drawings (see the counts); the placements it left observed are listed under `callout_check.not_validated`.",
		],
		"callout_check": check,
		"coordinate_convention": {
			"source_bounds": {"bottom": TABLE_HEIGHT, "left": 0.0, "right": TABLE_WIDTH, "top": 0.0},
			"space": "playfield",
			"x": f"x/{TABLE_WIDTH}; 0=left, 1=right",
			"y": f"y/{TABLE_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"excluded_object_classes": [
			"GI light objects and their collection (gi001-gi026, gi_Bumper1-3, gi_Star1-2, gi_Saucer, gi-bg): Quicksilver's general illumination is a plain 6 VAC lamp string with no driver-board output and no controller address, so it is not a device in this definition",
			"cr_<n><letter> and mb_<n><letter> and p<n>_<n><letter> Light objects, the retained table's bake and multi-ball render helpers rather than emitters",
			"go, hstd, ma, tilt and sa Light objects, the backbox copies of public lamps 45, 13, 63, 61 and 11 (they are backbox lamps with a controlled cabinet_or_service record; the playfield copy of Shoot Again is placed)",
			"sw38a, the fifth bounce rubber at the far left, which the manual's location drawing does not show (the matrix sheet prints four)",
			"sw21a-sw24a, sw30a-sw32a, sw4hit, sw5hit and similar helper walls and triggers beside the objects that carry the switches",
		],
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/stern/quicksilver-1980/vpw-1.0/Quicksilver (Stern 1980) VPW 1.0.manifest.json",
			"source_ref": EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "0.33.3",
		},
		"format": "pinmame-spatial-blockers",
		"machine_id": MACHINE_ID,
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(values, key=lambda item: (item["group"], item["address"]))
			for reason, values in sorted(na_outputs.items())
		},
		"placement_count": placements,
		"placement_statuses": dict(sorted(statuses.items())),
		"projections": projections,
		"resolved_direct_inputs": sorted(resolved_direct),
		"resolved_input_addresses": sorted(resolved_inputs),
		"resolved_output_bindings": sorted(resolved_outputs, key=lambda item: (item["group"], item["address"])),
		"unplaced_input_addresses": sorted(no_spatial_inputs),
		"unplaced_output_bindings": sorted(no_spatial_outputs, key=lambda item: (item["group"], item["address"])),
		"version": 1,
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Quicksilver (Stern, 1980) spatial review",
		"",
		"Status: incomplete. Six lamp addresses carry no placement and every lamp placement is `observed`, so the machine record stays `partial` at "
		"`machines/partial/stern/quicksilver-1980.json`.",
		"",
		f"The geometry source is the retained known-working `Quicksilver (Stern 1980) VPW 1.0.vpx` at SHA-256 `{TABLE_SHA256}`. Its embedded script at SHA-256 `{SCRIPT_SHA256}` is the runtime address and causality authority. "
		f"Exact playfield bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/{TABLE_WIDTH} and y/{TABLE_HEIGHT} rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script owns runtime addresses and causality, this game's own manual and driver-board schematics own physical construction, wiring, quantity and device presence, pinned PinMAME owns controller topology, "
		"and the retained table supplies geometry.",
		"- Lamp bindings come from the table's own `vpmMapLights InsertLamps` collection (a light's TimerInterval is its public lamp number) and from `UpdateMultipleLamps` for the backbox lamps, and each was checked against the function the "
		"Lamp Driver Schematic prints against the SCR that public address reaches. The names fall in the right places: the Q-U-I-C-K lamps run left to right along the top, the S-I-L and V-E-R stand-up lamps run top to bottom down the left and "
		"right arcs, and the two spinner lamps sit beside their own spinners once the schematic's hand correction of the left spinner's pin is applied.",
		"- The retained VPW script pulses switches 20 and 21 from its slingshots, which is a defect of that script (the older retained table and the corpus 1.0 script pulse 12 and 13, and the ROM fires the sling coils on 12 and 13); the slingshots are placed "
		"on the table's own sling walls and the defect is stated on the devices.",
		"- General illumination is not a device on this machine: the playfield sheet draws it as a 6 VAC lamp string with no driver-board connection and the Stern MPU-200 controller profile declares no general-illumination group.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({', '.join(f'{count} {name}' for name, count in report['placement_statuses'].items())})",
		f"- Callout check: {report['callout_check']['validated']} of {report['callout_check']['checked']} checked placements validated against the manual's location drawings"
		+ (f"; not validated: {', '.join(sorted(report['callout_check']['not_validated']))}" if report['callout_check']['not_validated'] else ""),
		f"- Located input addresses: {len(report['resolved_input_addresses'])} matrix switches and {len(report['resolved_direct_inputs'])} direct end-of-stroke contacts",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		f"- Inputs with no spatial key at all: {len(report['unplaced_input_addresses'])} ({', '.join(str(value) for value in report['unplaced_input_addresses']) or 'none'})",
		f"- Outputs with no spatial key at all: {len(report['unplaced_output_bindings'])} ({', '.join(str(item['address']) for item in report['unplaced_output_bindings']) or 'none'})",
		"",
		"## Blockers",
		"",
	]
	for blocker in report["blockers"]:
		lines.append(f"- {blocker}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Promotion to `author_ready` is refused. Public lamp 6 is driven by the ROM but listed by no wiring sheet, so its fitment is unresolved and `output_semantics` stays missing; five fitted top-divider lamps have no retained object; "
		"and every lamp placement rests on one factory-layout table with no lamp-location drawing to check it against. The record stays `partial` with `coverage.missing = [\"output_semantics\", \"spatial_placement\"]`.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Object-centre dump of the extracted game items, raw and normalized, at `external:pinmame-review-artifacts/quicksilver-1980/vpw-geometry.tsv`.",
		f"- Manual `{PDF}`, SHA-256 `{MANUAL_SHA256}`, with transcribed excerpts under `{EXCERPT_ROOT}/`.",
		"",
	]
	return "\n".join(lines)


# --- Knowledge note -----------------------------------------------------------------------------------------------------


KNOWLEDGE = """# Quicksilver (Stern, 1980)

Coverage: **partial - the physical inventory, controller bindings, wiring and mechanisms are validated; one lamp circuit's fitment and the playfield placements are not**

## Identity and evidence precedence

This is the one physical Stern Quicksilver (IPDB 1895, June 1980, model 117, Stern M-200 MPU, 1,201 units). PinMAME `quicksil` is the production root and `quicksfp` its stock free-play clone; both use the same game-data line (`GEN_STMPU200`, seven-digit
`dispst7` displays, `FLIP_SW(FLIP_L)`, ST300 sound), and the community rules revisions `quicksib` (07D, 2021) and `quicksic` (8.1, 2024) use the same line again, so all four are physically identical; only the rules ROMs differ. The ROM archives `quicksil.zip` and
`quicksfp.zip` were available; `quicksib` and `quicksic` were not, so nothing here was measured on them.

The evidence order is the runbook's. The known-working VPW 1.0 script and the earlier retained tables give runtime semantics, this game's own manual, Lamp Driver Schematic (12B-432-S-116) and Solenoid Driver Schematic (12B-432-S-117 sheet 3) give construction and wiring, pinned PinMAME gives
the controller topology, and three retained harness runs (a Self Test sweep, the stuck-switch test and a scripted game) give the public addresses. The Lamp Driver Schematic was drawn for a sister game, `CHEETAH`, and relabelled by hand for this one; its list is Quicksilver's own and its
SCR numbering is the board's.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's stuck-switch display shows the closed address's own number for every one of the forty (retained run). The printed Self Test numbers are therefore the public addresses.
All forty positions are fitted: coin chutes 1-3, spinners 4-5, credit 6, tilt 7, slam 8, bumpers 9-11, slingshots 12-13, stand-ups 14-16, 25-27 and 40, top lanes 17-20, center drop targets 21-24, special roll-over 28, kick-out hole 29, right drop targets 30-32, out-hole 33,
outlanes and return lanes 34-37, bounce rubbers 38 and roll-over button 39. Every matrix contact is drawn as a normally open contact with a series 1N4004 diode. The cabinet switches (1-3, 6-8) are wired on the cabinet sheet through the front-door jack to MPU connector A4J3, the others on the
playfield sheet to A4J2. Service inputs are -7 (Self Test), -6 (CPU diagnostic NMI) and -5 (sound diagnostic); -6 and -5 are PinMAME routes whose physical buttons the manual does not document. The cabinet flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are the
unused upper positions. Each flipper's end-of-stroke contact is a hard-wired normally closed contact drawn across the first winding of its dual-winding coil and is not a PinMAME address.

**Solenoids.** The printed solenoid list numbers the SDU transistors 1-19 and the public addresses do not follow it. The ROM's own Self Test energizes them in physical order, and the public addresses fire as `2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18`, so physical 1..19 map to public
`1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18`. Nine of those positions were independently confirmed in play: the three thumpers and two slingshots fire on their own switches (public 1, 2, 3, 4, 5 for
switches 9, 10, 11, 12, 13), the two drop-bank resets fire when their last target closes (7 and 8), the kick-out hole fires on its switch (9), the out-hole kicker fires from game start (10) and the flipper-enable relay rises at game start and drops on a tilt (19). Public 16 is an unaddressable decoder slot. Physical 9-12, 16, 17 and 18 are
printed OPEN and are unused. The lower flippers are the synthetic held-coil outputs 46 (right) and 48 (left); PinMAME also asserts 45 and 47 for exactly the same interval as 46 and 48 (retained gameplay run; `core.c` asserts both bits of each pair while the button is closed), which the Stern MPU-200 controller profile does not declare and this definition does not bind.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs, not a matrix. A public lamp is `16 * k + a + 1` for decoder chip `U(k+1)` output `S(a)`, and each of the sixty output lines carries a resistor `R<n>` that ends at SCR `Q<n>` (the schematic's resistor and SCR numbers match on every line). The mapping from public address to SCR therefore
comes from the decoder drawing, and the connector table gives each SCR its jack and pin. This definition gives all sixty. Public 16, 32, 48 and 64 are unaddressable decoder slots. Two of the schematic's readings are easy to transpose and were checked three ways: `U2` outputs S7 and S8 drive SCRs Q25 and Q24, so the right
stand-up lamp V (J1 pin 6, Q25) is public 24 and the unused SCR Q24 is public 25, and `U3` and `U4` output S9 drive Q41 and Q46, so top divider 2 (Q41) is public 42 and top divider 1 (Q46) is public 58. The retained tables bind public 24 to the V insert, and the five dividers (10, 26, 42, 57, 58) light together in the ROM's coin-in lamp show.

The playfield lamp wiring list prints fifty rows and the Lamp Driver Schematic's list prints fifty-four: it adds `GAME OVER` (public 45), `HIGH SCORE TO DATE` (13), `MATCH` (63) and `TILT` (61). The two lists disagree about one pin and one number only: `SHOOT AGAIN` is J1 pin 26 on the playfield list and J2 pin 21 on the schematic (one SCR, Q3, reaches both, and there is a
playfield insert and a backbox bulb), and the playfield list prints jack J2 pin 6 for both spinner lamps while the schematic strikes the left spinner's 6 out by hand and writes 7. Those are wiring-detail differences and are resolved as device notes.

## Lamps with no printed load

Five SCRs have no row in either list and are driven by the ROM only in the power-up lamp flash (which ends about 12.6 s after power-up) and the self-test sweep, never in the attract pattern or in play (retained gameplay run): public 25, 27, 29, 41 and 43. They are recorded `unused`. Public 29 is the lamp a sister machine labels Ball in Play; here the ball in play is a digit on the Match/Ball display module.
**Public 6 (SCR Q10, connector pin J1-15) is different.** No list prints a load for it, yet the ROM keeps toggling it in the attract-mode lamp pattern after the power-up flash, together with 38 lamps that are all listed (retained gameplay run). The evidence available cannot say whether a bulb is fitted behind it, so it is recorded with availability `unknown`
and `output_semantics` stays in `coverage.missing`. A bulb-level answer needs a photograph of an unrestored machine's A5J1 harness at pin 15, or the ROM's lamp-show data decoded to see which feature it accompanies.

General illumination is a 6 VAC lamp string (`A2J1-8` to `A2J1-1`) with no driver-board connection and no controller address.

## Ball lifecycle

Quicksilver is a single-ball game with no trough. The ball starts on the out-hole switch (public 33). When a game starts the ROM resets both drop banks (public 7 and 8), ejects the kick-out hole once (9) and kicks the out-hole (10) repeatedly for as long as 33 stays closed. A real ball leaves 33 after the first kick and rolls to the shooter lane,
where the player launches it with the plunger. After a drain the ball returns to 33, the bonus is counted, the ball-in-play digit advances and the kick repeats. The retained tables release the ball from a shooter-lane kicker at 90 degrees. Tilt disqualifies the ball only: the ROM drops the flipper-enable relay (19) when switch 7 closes, and normal play resumes at the next serve.

## Mechanisms

- **Center bank:** four drop targets on a slant (switches 21 highest to 24 lowest, `4 Bank Target D-580-4`), closed while down, one reset coil (public 7, B-27-2300). The ROM resets the bank when the fourth target closes.
- **Right bank:** three drop targets beside the right rail (30 highest to 32 lowest, `3 Bank Target D-580-3`), one reset coil (public 8). Reset when the third target closes. Downing it raises the bonus multiplier (instruction card).
- **Kick-out hole:** a hole at the left edge with its switch (29) and an eject coil (public 9, J-28-2300) the ROM fires when a ball sits in it.
- **Spinners:** two spin target assemblies, switch 4 on the right and 5 on the left, 200 points per rotation in the retained run. Their lamps are public 46 (right) and 62 (left).
- **Pop bumpers and slingshots:** the ROM fires each coil when its own switch closes (public 1, 2, 3 for switches 9, 10, 11; public 4 and 5 for switches 12 and 13). The printed solenoid numbers are 2, 1 and 5 for the thumpers and 6 and 7 for the slingshots.
- **Flippers:** two lower dual-winding flippers fed from the +43 VDC bus through the flipper-enable relay; the buttons are hard-wired on A3J2-2 (left) and A3J2-1 (right).

## Scoring checkpoints from the retained gameplay run

Pop bumpers score 1,000, slingshots 10, spinners 200, the stand-ups (14, 15, 16, 25, 26, 27, 40) and top lanes 500, the special roll-over 1,000, the outlanes 25,000, the return lanes 5,000, bounce rubbers and the roll-over button 10. Center-bank targets score 1,000 each when closed, and opening the completed bank pays a further 3,000 after its reset fires; right-bank targets 30 and 31 score 500 each, and closing the third target (32) scores 25,500 and fires the bank reset. The kick-out hole scores 5,000. These are first-ball ROM scores
and only checkpoints: the instruction card governs the rules.

## Rules summary (instruction card)

Pop bumpers score 1,000. The bonus multiplier increases when the right three-bank is down. Q-U-I-C-K and S-I-L-V-E-R targets advance the bonus only when not already lit; the 75,000 bonus lights after the 20,000 step and a lit 75,000 does not collect the multiplier. Lighting all QUICK SILVER targets lights the top and outlane specials.
A spinner's value increases when the ball enters the opposite return lane and must be re-lit after the spinner is hit. The kick-out target scores 5,000 and advances the center target value. Each center-bank target scores 1,000 plus its lit value, and downing all four spots the next letter. Spotting Q-U-I-C-K and then hitting the flashing target awards an extra ball. Tilt disqualifies the ball in play only.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32. Coin chutes 1, 2 and 3 take S1-4, S9-12 and S25-28 (the credit catalog); S5 add-a-ball memory, S6 high-score award, S7 balls per game (ON = 5), S8 maximum add-a-balls, S13 flashing-lite retention, S14 background sound, S15-16 high game to date, S17 QUICK extra ball
per game, S18-19 maximum credits (10/15/25/40), S20 credit display, S21 match, S22 QUICK extra ball, S23-24 special lite alternation, S29 QUICK SILVER special carry-over, S30 special replay limit and S31-32 special award. S33 on the MPU is a memory-clear pushbutton.

## Displays and sound

Four seven-digit score displays at layout indices 0-3 and segment-memory starts 1, 9, 17 and 25, a two-digit credits display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME `dispst7`. Sound is the Stern ST300 board (sound module C-605); sound commands add no playfield devices.

## Defects in consumed artifacts

- The retained VPW 1.0 script pulses switches 20 and 21 from its slingshots; the correct addresses are 12 and 13 (the corpus 1.0 script and the older retained table pulse them, and the ROM fires the sling coils on them). It also drives the two right-side coil banks through custom animation code, which does not change the controller contract.
- The older retained table names its two upper bumper objects the other way round: `Bumper1` stands at the left and pulses the right bumper's switch 9.
- The playfield wiring sheet prints `A3J1-5 (B-G)` for the out-hole and `A3J5-12 (D-O)` for the right drop-target bank; the Solenoid Driver Schematic places them on J5 pins 11 and 10, which are the pins used.

## Recreation checklist

- Build the full inventory: 40 matrix switches, three service inputs, four flipper-button positions, 32 option switches, the 18 solenoid addresses and two flipper coils, the 60 SCR lamp addresses and the six displays.
- Start with the ball on the out-hole switch, both drop banks up, the kick-out hole empty and the flipper-enable relay off until a game starts.
- Reproduce the ROM-fired thumpers and slingshots, the two drop-bank resets, the kick-out eject, the out-hole serve loop and the tilt behaviour exactly as the harness runs show.
- The slam quantity is left unstated: the location sheet lists a door and a tilt-board contact, while the operating text (manual page 5) also names one on the playfield, and no retained source settles whether that third contact was fitted. All of them share public address 8.
- Treat the instruction card as the rules summary and the ROM as the rules authority; the community 07D and 8.1 ROMs change rules, not hardware.
- Switch and solenoid placements are validated against the manual's two location drawings where they agree (46 of 48 checked); lamp placements are observed from the retained table only, and the five top-divider lamps have no placement.

## Sources

- `manual.stern.quicksilver.1980`: the 35-page IPDB manual, SHA-256 `140216dc27e97084e0b523fe0d5ff5417961723fea069b1fad3dd594b9723728`, with transcribed excerpts of its identification tables, switch and solenoid drawings, playfield and cabinet wiring, option switches and parts list.
- `schematic.stern.quicksilver.lamp-driver` and `schematic.stern.quicksilver.solenoid-driver`: the IPDB Lamp Driver and Solenoid Driver schematics, SHA-256 `bea05d384e1f7ddf2dc98793cc1c9c82a38aece048b6750fe67371b2262870ee` and `f71e59b6d72e7d1315eeb3eaca940479bd882d9d3bcbfb008905180f92078a5d`.
- `manual.stern.quicksilver.instruction-card`: the rules card, SHA-256 `f85d0a60e1a03bf904623816fa5747d64020a0a81192964915cd717180be3f67`.
- `vpx-table.quicksilver-vpw-1-0`, `vpx-script.quicksilver-vpw-1-0`, the corpus 1.0 script and the earlier archive table: geometry and runtime semantics.
- `runtime.quicksilver.self-test`, `runtime.quicksilver.stuck-switch-test` and `runtime.quicksilver.gameplay`: three isolated harness runs of `quicksil` (ROM archive SHA-256 `691e06ac64f445cde8842934efdc3a7e223b408f442131bcb2903bde56b45ad3`) on the pinned `pinmame64.dll`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.8371478a7640`: driver declarations, MPU-200 implementation, public-address conversion and display layouts.
"""


# --- Generation and checking ------------------------------------------------------------------------------------------


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Quicksilver retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Quicksilver extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Quicksilver retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Quicksilver retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Quicksilver retained extraction identity mismatch: {identity}")
	return actual


def generate(root: Path = ROOT) -> Path:
	write_text(root / EXCERPT_ROOT / "instruction-card.md", INSTRUCTION_CARD_TEXT)
	definition = build_definition(root)
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	write_text(root / KNOWLEDGE_PATH.relative_to(ROOT), KNOWLEDGE)
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError("A Quicksilver author-ready definition is present although the record is partial")
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"Quicksilver artifact is missing: {path}")
	definition = build_definition(root)
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Quicksilver definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Quicksilver seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Quicksilver spatial report drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Quicksilver spatial review drifted from its deterministic curator: {markdown_path}")
	knowledge_path = root / KNOWLEDGE_PATH.relative_to(ROOT)
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != KNOWLEDGE.replace("\r\n", "\n").encode("utf-8"):
		raise RuntimeError(f"Quicksilver knowledge note drifted from its deterministic curator: {knowledge_path}")
	if unresolved_conflicts(definition) and "unresolved_conflicts" not in definition["coverage"]["missing"]:
		raise RuntimeError("Quicksilver holds unresolved conflicts but does not list them as missing")
	print("Quicksilver definition, seed, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, knowledge note and spatial report")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained VPX extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Quicksilver retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
