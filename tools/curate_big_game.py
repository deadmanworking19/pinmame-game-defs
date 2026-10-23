#!/usr/bin/env python3
"""Curate the physical Stern Big Game (1980) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and retained-table coordinate is a literal in
``tools/big_game_data.py`` or here, so regeneration reproduces the canonical definition, its pinned seed, the spatial report and the
knowledge note byte for byte without reading the external evidence roots. ``--check`` refuses drift and ``--regenerate`` is the only path
that writes.

Evidence authority follows the runbook. The known-working VPX scripts own runtime semantics, this game's own manual, corrections sheet and
schematic set own physical construction, wiring and device presence, pinned PinMAME owns controller topology, and the retained harness runs
pair printed numbers with public addresses. Where the machine's own sheets disagree only about a connector pin or wire colour the
disagreement is a device note, not a conflict.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402
import big_game_data as data  # noqa: E402
import drawing_callouts  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = Path("machines/partial/stern/big-game-1980.json")
AUTHOR_READY_PATH = Path("machines/author-ready/stern/big-game-1980.json")
SEED_PATH = Path("tools/seeds/stern/big-game-1980.json")
KNOWLEDGE_PATH = Path("knowledge/stern/big-game-1980.md")
SPATIAL_REPORT_PATH = Path("reports/spatial/stern/big-game-1980.json")
SPATIAL_REPORT_MARKDOWN_PATH = Path("reports/spatial/stern/big-game-1980.md")
RUNTIME_EVIDENCE_PATH = Path("evidence/runtime/stern/big-game-diagnostics-and-gameplay.json")
EXCERPT_ROOT = "evidence/excerpts/stern.big-game.1980"

MACHINE_ID = "stern.big-game.1980"
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "e5cedcdb33f648a2a735fa4c250b9a379a935c06370c7c67500fe2cf70bc8043"
CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-stern-mpu200"
MANUAL_SOURCE = "manual.stern.big-game.1980"
CORRECTIONS_SOURCE = "manual.stern.big-game.corrections-1980-03"
SCHEMATIC_SOURCE = "schematic.stern.big-game.wiring-set"
IPDB_SOURCE = "ipdb.249"
CARD_SOURCE = "photo.ipdb-249.instruction-card"
PHOTO_SOURCE = "photo.ipdb-249.playfield"
SCRIPT_SOURCE = "vpx-script.big-game-vr-1-5-1"
OLD_SCRIPT_SOURCE = "vpx-script.big-game-1-0-4"
SELF_TEST_SOURCE = "runtime.big-game.self-test"
SOLENOID_TEST_SOURCE = "runtime.big-game.solenoid-test"
SWITCH_TEST_SOURCE = "runtime.big-game.switch-test"
GAMEPLAY_SOURCE = "runtime.big-game.gameplay"
GAME_OVER_SOURCE = "runtime.big-game.game-over-and-slam"

MANUAL_PDF = "Stern_1980_Big_Game_Manual.pdf"
CORRECTIONS_PDF = "Stern_1980_Big_Game_Corrections_to_Game_Manual_March_1980.pdf"
SCHEMATIC_PDF = "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf"
MANUAL_SHA256 = "8f3977afc8650c993166873e169acdf271368a0a43bee77317dc3fb67deb9f6a"
CORRECTIONS_SHA256 = "104441047a9eadc9b58a1a6c408fbd526a4eac096e15e283ded5c307c25a07a3"
SCHEMATIC_SHA256 = "7930424122aaece9256fd7966e21356a08cdbcc15e17227323f97a10a0eeb89a"
CARD_PHOTO_SHA256 = "0882a8d7a4c96c2c589bdd68470399e93f011415e96086f8b2e34824c4d820bb"
PLAYFIELD_PHOTO_SHA256 = "224249f6fd70135beb7ff29ccfab077a8476756d5f01f868d429e3d53154e5e9"
UPPER_PHOTO_SHA256 = "1715f143aac55b1bbae420bcfed18fabe27facda77ca466676127738fab8fc4c"
SCRIPT_SHA256 = "828168766f0dcaf8e9f2bdf197ef8ac4a69550b2f3edc01d39be2832556097d1"
OLD_SCRIPT_SHA256 = "89fc207c9329ec69100e5ed88d3fffd510e2bd73eae9de0a62f14ae87c4cf366"

TABLE_SOURCE = "vpx-table.big-game-redbone-1-2-0"
TABLE_SCRIPT_SOURCE = "vpx-script.big-game-redbone-1-2-0"
EXTRACTION_SOURCE = "vpx-extraction.big-game-redbone-1-2-0"
CALLOUT_SOURCE = "review.big-game.drawing-callouts"
CALLOUT_SEED_PATH = Path("tools/seeds/stern/big-game-1980-callouts.json")
TABLE_FILENAME = "Big Game (Stern 1980) - redbone(MOD) v1.2.0.vpx"
TABLE_ARCHIVE_FILENAME = "Big Game (Stern 1980) - redbone(MOD) v1.2.0.rar"
TABLE_SHA256 = "6d37ab3ac46fdc116c3324c46bffae19ce784fc4bbece209b13f31840f823bfe"
TABLE_ARCHIVE_SHA256 = "7682567a9edf0d00647949b8d18a43442645b97b6fc119e426fea7632708ad24"
TABLE_SCRIPT_SHA256 = "61b2cf1d0cd6e6e09e7582a1ab5f8c3c092d54da113a74c436de552646d93e85"
TABLE_RELATIVE = Path("stern/big-game-1980/redbone-1.2.0")
EXTRACTION_RELATIVE = TABLE_RELATIVE / "Big Game (Stern 1980) - redbone(MOD) v1.2.0"
EXTRACTION_MANIFEST_SHA256 = "ca8c7886640ec273ad41afd4884d5abee5be71a65ca0b2805c0526800808a691"
EXTRACTION_FILE_COUNT = 689
EXTRACTION_TOTAL_BYTES = 22106949
TABLE_REFS = (TABLE_SOURCE, TABLE_SCRIPT_SOURCE)

RUN_NAMES = ("self-test", "solenoid-test", "switch-test", "gameplay", "game-over-and-slam")
RUN_SOURCES = {"self-test": SELF_TEST_SOURCE, "solenoid-test": SOLENOID_TEST_SOURCE, "switch-test": SWITCH_TEST_SOURCE,
	"gameplay": GAMEPLAY_SOURCE, "game-over-and-slam": GAME_OVER_SOURCE}

BOARD_MPU = "MPU module M-200 A4"
BOARD_SDU = "Solenoid Driver / Voltage Regulator module SDU B-432 A3"
BOARD_LDA = "Lamp Driver module LDA-100 B-431 A5"


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


def run_digests(root: Path = ROOT) -> dict[str, str]:
	runtime = load_json(root / RUNTIME_EVIDENCE_PATH)
	return {run["name"]: run["sha256"] for run in runtime["runtime"]["raw_runs"]}


# --- Inputs -------------------------------------------------------------------------------------------------------------


def matrix_wiring(address: int, cabinet: bool) -> dict[str, Any]:
	strobe, row = (address - 1) // 8, (address - 1) % 8
	strobe_wire, strobe_connection = data.CABINET_STROBE0 if cabinet else data.STROBES[strobe]
	return_wire, return_connection = data.CABINET_RETURNS[row] if cabinet else data.RETURNS[row]
	return {"board": BOARD_MPU, "control_wire": strobe_wire, "control_connection": strobe_connection, "return_wire": return_wire, "return_connection": return_connection}


def build_inputs() -> list[dict[str, Any]]:
	inputs: list[dict[str, Any]] = []
	for address, spec in sorted(data.SERVICE_SWITCHES.items()):
		refs = {"manual-and-harness": (MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, SELF_TEST_SOURCE, SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE), "core": (CORE_SOURCE,)}[spec["evidence"]]
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
		refs = [MANUAL_SOURCE, SCHEMATIC_SOURCE, SWITCH_TEST_SOURCE]
		refs += [GAMEPLAY_SOURCE] if address not in (8,) else [GAME_OVER_SOURCE]
		if not cabinet:
			refs += [SCRIPT_SOURCE]
		physical: dict[str, Any] = {"switch_type": spec["type"]}
		if spec.get("quantity"):
			physical["quantity"] = spec["quantity"]
		construction = ("Normally open contact, drawn on the cabinet sheet without the series diode the sheet gives its other contacts" if address in data.NO_DIODE_SWITCHES
			else "Normally open contact with a series 1N4004 diode on the " + ("cabinet sheet" if cabinet else "playfield wiring diagram"))
		physical["notes"] = f"Switch Identification table: `{spec['printed']}`; matrix sheet: `{spec['matrix']}`. {construction}. " + spec["notes"]
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
		else:
			names, projection = data.SWITCH_OBJECTS[address]
			item["spatial"] = located(spec["id"], "sensor", [[name] for name in names], *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SCRIPT_SOURCE]))
			physical["notes"] += " Placed on the retained table's " + " and ".join(f"{data.OBJECTS[name][0]} `{name}`" for name in names) + ", which its script binds to this address."
			if projection:
				physical["notes"] += " " + projection
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
				"notes": "PinMAME's synthetic cabinet flipper button position (FLIP_SW(FLIP_L)). The physical button is hard-wired through the flipper enable relay's contacts to both flipper coils of "
					"its side, not to the switch matrix, so the switch test does not show it (manual: `FLIPPER BUTTON CABINET SWITCHES DO NOT APPEAR ON TEST`). The retained gameplay run shows PinMAME's "
					"flipper outputs answering this address.",
				"quantity": 1,
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE),
			"pulse": False,
			"roles": [role],
			"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
			"wiring": {"board": "Hard-wired flipper button circuit through the SDU flipper enable relay", "control_wire": wire, "control_connection": connection,
				"return_wire": "O", "return_connection": "A2J2-9"},
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
				"notes": "PinMAME's generic upper flipper button position. Big Game has two flippers on each side, but each side's pair shares one cabinet button and one drive wire "
					"(the playfield sheet draws both right flippers on A3J1-9 and both left flippers on A3J1-8), and the driver declares FLIP_SW(FLIP_L) only, so no button reaches this position; "
					"pressing it changed no output in the retained gameplay run.",
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE),
			"pulse": False,
			"spatial": not_applicable("unused", MANUAL_SOURCE, CORE_SOURCE),
		})

	for address in sorted(data.DIPS):
		unused = address in data.UNUSED_DIPS
		inputs.append({
			"aliases": [{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": "S%d" % address}],
			"availability": "unused" if unused else "used",
			"binding": {"device": address, "group": "pinmame.input.dip"},
			"id": "dip.option-switch-%d" % address,
			"kind": "dip_switch",
			"label": data.DIPS[address],
			"physical": {
				"location": "MPU module option-switch packages in the backbox",
				"notes": "One of the thirty-two MPU option switches in the four sixteen-lead packages S1-8, S9-16, S17-24 and S25-32, with the ON position marked on the assembly (manual Figure 1 and page 11). "
					"The assignment is the `BIG GAME SWITCH ASSIGNMENT` and the adjustment tables of pages 11-15; the March 1980 corrections sheet reverses the printed settings of S8 and S22. "
					"S33 on the same module is a momentary memory-clear pushbutton, not an option switch.",
				"switch_type": "dip",
			},
			"provenance": provenance(MANUAL_SOURCE, CORRECTIONS_SOURCE, CORE_SOURCE) if address in (8, 22) else provenance(MANUAL_SOURCE, CORE_SOURCE),
			"spatial": not_applicable("dip_switch", MANUAL_SOURCE),
		})

	for side, address, button in (("left", 1, 84), ("right", 2, 82)):
		identifier = f"switch.{side}-flipper-end-of-stroke-contacts"
		inputs.append({
			"aliases": [{"namespace": "manual.address", "value": f"{side}-flipper-eos"}],
			"availability": "used",
			"binding": {"device": address, "group": "physical.input.direct"},
			"id": identifier,
			"kind": "switch",
			"label": f"{side.title()} flipper end-of-stroke contacts (two)",
			"normally_closed": True,
			"physical": {
				"location": f"{side.title()} flipper assemblies (lower and upper)",
				"notes": "Hard-wired contacts of the two dual-winding flipper coils of this side, not PinMAME switch addresses. The playfield wiring diagram draws each coil assembly with a contact across its "
					"first winding, conducting at rest and opening at the end of the stroke to insert the second winding (normally closed), plus an `E.O.S.` mark between the two assemblies' return leads, "
					"which is kept literally in the excerpt and adds no further contact. Placed by projection on the side's two flipper pivots in the retained table (lower, then upper), "
					"because each contact is mounted on its flipper assembly and has no object of its own.",
				"quantity": 2,
				"switch_type": "leaf",
			},
			"provenance": provenance(SCHEMATIC_SOURCE, MANUAL_SOURCE),
			"pulse": False,
			"spatial": located(identifier, "sensor", [[name] for name in data.DIRECT_OBJECTS[address]], TABLE_SOURCE, SCHEMATIC_SOURCE),
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
			"notes": "The door-mounted `(MEMORY CLEAR) S-33` of Figure 1, drawn on the cabinet sheet as `S33 MEMORY CLEAR` from A4J3-5 (-W-) to A3J2-7 (Y-R), the same return as the Self Test button. "
				"It reaches the MPU's external memory-clear input rather than a matrix position; the manual's high-score text uses S33 to set a level quickly to `00`. This profile-local physical binding "
				"has no controller transport, and no ROM effect is claimed from a host write.",
			"switch_type": "button",
		},
		"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE),
		"pulse": False,
		"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE, SCHEMATIC_SOURCE),
		"wiring": {"board": "MPU external memory-clear circuit", "control_wire": "W", "control_connection": "A4J3-5", "return_wire": "Y-R", "return_connection": "A3J2-7"},
	})
	return inputs


# --- Outputs ------------------------------------------------------------------------------------------------------------


def coil_wiring(spec: dict[str, Any], physical_number: int) -> dict[str, Any]:
	wiring: dict[str, Any] = {"board": BOARD_SDU, "driver_transistor": f"Q{physical_number}", "nominal_voltage_v": 43, "voltage_type": "dc"}
	if spec.get("wire"):
		wiring["drive_wire"] = spec["wire"]
	if spec.get("conn"):
		wiring["drive_connection"] = spec["conn"]
	return wiring


def build_solenoid_outputs() -> list[dict[str, Any]]:
	outputs: list[dict[str, Any]] = []
	public_to_physical = {public: number for number, public in data.PHYSICAL_TO_PUBLIC.items()}
	for address, spec in sorted(data.SOLENOIDS.items()):
		physical_number = public_to_physical[address]
		if spec.get("phys") and spec["phys"] != physical_number:
			raise RuntimeError(f"solenoid {address}: data names driver {spec['phys']}, the ROM test pairs {physical_number}")
		unused = bool(spec.get("unused"))
		availability = "unused" if unused else spec.get("availability", "used")
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)]
		aliases += [{"namespace": "manual.self-test", "value": str(physical_number)}, {"namespace": "manual.address", "value": f"SDU-Q{physical_number}"}]
		refs = [MANUAL_SOURCE, SCHEMATIC_SOURCE, SOLENOID_TEST_SOURCE, SELF_TEST_SOURCE]
		if address in (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 18, 19):
			refs.append(GAMEPLAY_SOURCE)
		if address in (6, 7, 8, 9, 10, 11, 19):
			refs.append(SCRIPT_SOURCE)
		if address in (17, 19, 20):
			refs.append(GAME_OVER_SOURCE)
		physical: dict[str, Any] = {}
		if spec.get("part"):
			physical["part_number"] = spec["part"]
			physical["quantity"] = 1
		printed = data.PRINTED_SOLENOIDS[physical_number]
		physical["notes"] = f"SDU driver Q{physical_number}, printed solenoid {physical_number} `{printed}`; the ROM's solenoid test shows {physical_number} while public {address} fires. " + spec["notes"]
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": availability,
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": spec["kind"],
			"label": spec["label"],
			"physical": physical,
			"provenance": provenance(*refs, status="observed" if availability == "unknown" else "validated"),
			"wiring": coil_wiring(spec, physical_number),
		}
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if unused:
			item["spatial"] = not_applicable("unused", MANUAL_SOURCE, SCHEMATIC_SOURCE, SOLENOID_TEST_SOURCE)
		elif spec.get("cabinet"):
			physical["location"] = "Cabinet"
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, SCHEMATIC_SOURCE)
		elif spec.get("internal"):
			physical["location"] = "Solenoid driver board in the backbox"
			item["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, SCHEMATIC_SOURCE)
		elif availability == "unknown":
			item["spatial"] = not_applicable("internal_nonvisual", SCHEMATIC_SOURCE)
		else:
			names, projection = data.SOLENOID_OBJECTS[address]
			groups = [names] if projection and len(names) > 1 else [[name] for name in names]
			item["spatial"] = located(spec["id"], "effect", groups, *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SCRIPT_SOURCE]))
			if not projection:
				physical["notes"] += f" Placed on the retained table's {data.OBJECTS[names[0]][0]} `{names[0]}`, which its script drives from this address."
			else:
				physical["notes"] += " " + projection
		outputs.append(item)

	for address, spec in sorted(data.FLIPPERS.items()):
		power = spec["power"]
		outputs.append({
			"aliases": [
				{"namespace": "pinmame.solenoid", "value": str(address)},
				*({"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)),
				{"namespace": "manual.self-test", "value": "15"},
			],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": "coil",
			"label": spec["label"],
			"physical": {
				"part_number": "J-25-475/34-4500 (lower); J-25-500/34-5050 (upper)",
				"quantity": 2,
				"notes": f"The two {spec['side']} flippers (parts list `Flipper Lower L & R` J-25-475/34-4500 and `Flipper Upper L & R` J-25-500/34-5050) are dual-winding coils wired in parallel on one drive wire, "
					f"hard-wired from the +43 VDC supply A2J1-6 (BLU-W) through the flipper enable relay's contacts to the {spec['side']} cabinet button; no numbered solenoid transistor drives them. "
					f"Public {address} is PinMAME's synthetic held-coil output for the {spec['side']} side (FLIP_SW(FLIP_L)); PinMAME also asserts public {power} for the same interval. "
					"Both outputs are button states, not measurements of either winding, and one callback moves both flippers of the side. "
					f"Placed on the retained table's two {spec['side']} flipper pivots (`{data.FLIPPER_OBJECTS[address][0]}` lower, `{data.FLIPPER_OBJECTS[address][1]}` upper), both moved by this callback.",
			},
			"provenance": provenance(MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE, SCRIPT_SOURCE, TABLE_SCRIPT_SOURCE),
			"spatial": located(spec["id"], "effect", [[name] for name in data.FLIPPER_OBJECTS[address]], *TABLE_REFS, MANUAL_SOURCE),
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
				"(retained gameplay run). It is not another coil and does not measure the power winding."},
			"provenance": provenance(CORE_SOURCE, GAMEPLAY_SOURCE),
			"spatial": not_applicable("virtual", CORE_SOURCE, GAMEPLAY_SOURCE),
		})
	return outputs


def lamp_rows() -> dict[int, list[tuple[str, str, str, int]]]:
	q_to_public = {q: public for public, q in data.LAMP_TO_Q.items()}
	rows: dict[int, list[tuple[str, str, str, int]]] = {}
	for description, wire, jack, pin in data.LAMP_LIST:
		q = data.LDA_CONNECTORS[jack][int(pin)]
		rows.setdefault(q_to_public[q], []).append((description, wire, jack, int(pin)))
	return rows


def build_lamp_outputs() -> list[dict[str, Any]]:
	rows = lamp_rows()
	if set(rows) | set(data.UNUSED_LAMPS) != set(data.LAMP_TO_Q) or set(rows) & set(data.UNUSED_LAMPS) or set(rows) != set(data.LAMP_NAMES):
		raise RuntimeError("Big Game lamp inventory does not partition the sixty SCR outputs")
	outputs: list[dict[str, Any]] = []
	for address in sorted(data.LAMP_TO_Q):
		q = data.LAMP_TO_Q[address]
		k, a = divmod(address - 1, 16)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.lamp", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.address", "value": f"LDA-Q{q}"})
		wiring: dict[str, Any] = {"board": BOARD_LDA, "driver_transistor": f"Q{q}"}
		detail = f"Lamp Driver SCR Q{q}, decoder U{k + 1} output S{a}, resistor R{q}. Discrete SCR output on the LDA-100, not a lamp matrix."
		if address in data.UNUSED_LAMPS:
			pins = [f"A5{jack}-{pin}" for jack, pins in data.LDA_CONNECTORS.items() for pin, scr in pins.items() if scr == q]
			wiring["drive_connection"] = ", ".join(pins)
			outputs.append({
				"aliases": aliases,
				"availability": "unused",
				"binding": {"device": address, "group": "pinmame.output.lamp"},
				"id": f"lamp.unused-scr-q{q}",
				"kind": "lamp",
				"label": f"Unused lamp driver SCR Q{q}",
				"physical": {"notes": detail + f" The connector table brings it out on {', '.join(pins)}, but neither this game's Lamp Driver Schematic list nor its playfield wiring list prints a load "
					"for it, and the ROM drives it only in its own burn-in and lamp tests: it never changes in attract mode, play, drain, tilt, game over or slam in the retained runs."},
				"provenance": provenance(SCHEMATIC_SOURCE, SELF_TEST_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE),
				"spatial": not_applicable("unused", SCHEMATIC_SOURCE, SELF_TEST_SOURCE),
				"wiring": wiring,
			})
			continue
		identifier, label = data.LAMP_NAMES[address]
		lamp_list = rows[address]
		description, wire, jack, pin = lamp_list[0]
		wiring["drive_connection"] = f"A5{jack}-{pin}"
		wiring["drive_wire"] = wire
		aliases.append({"namespace": "manual.address", "value": f"LDA-{jack}-{pin}"})
		backbox = description in data.BACKBOX_ROWS
		detail += f" Printed load: `{description}` ({wire}, LDA {jack} pin {pin})"
		detail += " on the Lamp Driver Schematic's list only (the playfield list omits it), so a backbox lamp." if backbox else ", on both this game's lamp lists."
		physical: dict[str, Any] = {"part_number": "#44 (8A-101)", "notes": detail}
		refs = [SCHEMATIC_SOURCE, SELF_TEST_SOURCE]
		if address in (5, 6, 9, 10, 25, 26, 30, 41, 42, 53, 57, 61, 13, 45, 63, 21, 37):
			refs.append(GAMEPLAY_SOURCE)
		refs.append(SCRIPT_SOURCE)
		if address in data.TWO_INSERT_LAMPS:
			physical["quantity"] = 2
			physical["notes"] += (" The letter has two inserts on one output: one at its own lane or target and one in the B-I-G-G-A-M-E column of the eject-pocket lane "
				"(instruction card item 2 and the IPDB playfield photographs); the known-working scripts drive two lights from this lamp number.")
			refs += [CARD_SOURCE, PHOTO_SOURCE]
		if address in (5, 37):
			physical["quantity"] = 2
			physical["notes"] += " The printed row names two features on this one output, the card's selection circle and a value insert, so it lights two inserts."
			refs += [PHOTO_SOURCE]
		if address == 25:
			physical["notes"] += (" The lamp list prints `\"M\"` on J1 pin 5, but the connector block's J1 row for SCR Q24 prints a flat-topped figure that reads as 3 (Q35's pin) or 5; the ROM settles it: when the saucer collects "
				"the letters, public 25 flashes with the six other letter lamps (retained gameplay run).")
		if address == 29:
			physical["notes"] += " The playfield list includes it (a playfield insert between the flippers in the scripts), and the backglass also prints SHOOT AGAIN; no list prints a second row for it."
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.lamp"},
			"id": identifier,
			"kind": "lamp",
			"label": label,
			"physical": physical,
			"provenance": provenance(*refs),
			"wiring": wiring,
		}
		if backbox:
			physical["location"] = "Backbox"
			item["roles"] = ["cabinet.backglass"]
			item["spatial"] = not_applicable("cabinet_or_service", SCHEMATIC_SOURCE, CORE_SOURCE)
		else:
			names = data.LAMP_OBJECTS[address]
			item["spatial"] = located(identifier, "emitter", [[name] for name in names], *TABLE_REFS, SCHEMATIC_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SOURCE, TABLE_SCRIPT_SOURCE]))
			if address in data.LAMP_TABLE_NOTES:
				physical["notes"] += " " + data.LAMP_TABLE_NOTES[address]
			else:
				physical["notes"] += " Placed on the retained table's " + " and ".join(f"light `{name}`" for name in names) + ", which its script drives from this address."
		outputs.append(item)
	return outputs


def build_gi() -> dict[str, Any]:
	return {
		"aliases": [],
		"availability": "used",
		"binding": {"device": 1, "group": "physical.output.gi"},
		"id": "gi.general-illumination",
		"kind": "gi",
		"label": "Uncontrolled general illumination",
		"physical": {
			"notes": "Transformer-fed general illumination with no controller address. The playfield wiring diagram draws `GEN. ILLUM` from A2J1-8 (W) at 6 VAC returning on A2J1-1 (R), the cabinet sheet "
				"draws `FRONT DOOR LITES` from A2J2-1 (Y-B) returning on A2J2-5 (G-R), and the shared transformer and wiring sheets take the backbox general illumination from A2J3 pins 10 and 11 (returns on "
				"pins 1 and 2) at 5.9 VAC. None of these draws a relay or driver in the circuit. Bulb quantity and positions are not established.",
		},
		"provenance": provenance(SCHEMATIC_SOURCE),
		"wiring": {"board": "Transformer/rectifier A2, uncontrolled general-illumination buses", "power_connection": "A2J1-8 (playfield); A2J2-1 (front door); A2J3-10, A2J3-11 (backbox)",
			"return_connection": "A2J1-1; A2J2-5; A2J3-1, A2J3-2", "voltage_type": "ac", "nominal_voltage_v": 6},
	}


def build_outputs() -> list[dict[str, Any]]:
	outputs = build_solenoid_outputs() + build_lamp_outputs() + [build_gi()]
	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return outputs


# --- Mechanisms, relationships --------------------------------------------------------------------------------------------


def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *sources: str, part: str | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {"actuators": actuators, "behavior": behavior, "id": identifier, "kind": kind, "label": label, "provenance": provenance(*sources), "sensors": sensors}
	if part:
		item["assembly_part_number"] = part
	return item


BANKS = (
	("top-left", "Top left three-target drop bank (1A)", "device.top-left-bank-reset", (14, 15, 16), 7, "D-580-3D-1",
		"Three drop targets printed 3, 2, 1 from top to bottom on the bank (switches 14, 15, 16), angled below the top-left roll-over button. "),
	("top-right", "Top right three-target drop bank (1B)", "device.top-right-bank-reset", (24, 23, 22), 8, "D-580-3D-2",
		"Three drop targets printed 4, 5, 6 from top to bottom (switches 24, 23, 22), angled below the right roll-over lane. "),
	("lower-right", "Lower right three-target drop bank (1C)", "device.lower-right-bank-reset", (32, 31, 30), 9, "D-580-3D-3",
		"Three drop targets printed 7, 8, 9 from top to bottom (switches 32, 31, 30) along the right side above the right return lane. "),
)


def build_mechanisms() -> list[dict[str, Any]]:
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	mechanisms = [
		mechanism(
			"mech.out-hole", "Single-ball out-hole and shooter feed", "kicker", ["device.out-hole-kicker"], ["switch.outhole"],
			"Big Game is a single-ball machine with no trough. The known-working scripts start with the ball on the out-hole switch (public 33). When the credit button starts a game the ROM resets the three "
			"drop banks (public 7, 8 and 9) and kicks the out-hole (public 11, J-26-1000), repeating the kick and the bank resets for as long as public 33 stays closed; the retained runs show the repeats "
			"stop once 33 opens. The kick sends the ball to the shooter lane, where the player launches it with the plunger. After every drain the bonus is counted, the player and ball advance, and the kick "
			"repeats; an extra ball is played without advancing (manual).",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE,
		),
		mechanism(
			"mech.eject-pocket", "Top eject pocket (saucer)", "kicker", ["device.saucer-eject"], ["switch.saucer"],
			"A saucer at the top of the left loop (parts list `Saucer Eject` J-28-2300). A ball in it holds public 34 closed and the ROM answers with a pulse on public 10 that ejects it back into the loop "
			"(retained gameplay run). The pocket scores 5,000 for each lit letter of B-I-G-G-A-M-E and 35,000 more when the word is made (manual). The known-working scripts eject at 55 degrees with force 20.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, CARD_SOURCE,
		),
	]
	for name, label, actuator, switches, coil, part, where in BANKS:
		mechanisms.append(mechanism(
			f"mech.{name}-drop-bank", label, "drop_target_bank", [actuator], [switch_id[address] for address in switches],
			where + f"A target's switch is closed while it is down; one reset coil (public {coil}, B-27-2300) raises the whole bank and there is no individual knock-down coil. Home state is all three up. "
			f"The ROM resets the bank at game start and after every drain, and again when the bank's last target goes down (retained gameplay run: public {coil} fires on the third closure). Each target "
			"scores 500 and spots its number in the selected card or cards (manual and retained run); once a bank's numbers are spotted on all three cards, each further completion scores 25,000 (manual).",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, part=part,
		))
	mechanisms += [
		mechanism(
			"mech.left-loop-spinners", "Two spinning targets across the left loop", "other", [], ["switch.left-spinner", "switch.right-spinner"],
			"Two spin target assemblies (A-563-11, target and wire 14A-7-10) hang on one wire across the left loop, left spinner (switch 4) at the outer end and right spinner (switch 5) beside the top-left "
			"drop bank. Each rotation closes its contact once; there is no coil or home sensor. The left spinner's value is lit with card X and the right one's when B-I-G is made (manual; lamps 37 and 30).",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.thumper-bumpers", "Three thumper bumpers", "kicker",
			["device.top-thumper-bumper", "device.lower-left-thumper-bumper", "device.lower-right-thumper-bumper"],
			["switch.top-thumper-bumper", "switch.lower-left-thumper-bumper", "switch.lower-right-thumper-bumper"],
			"Three J-26-1200 thumper bumpers. The ROM fires each coil when its own switch closes and scores 1,000 on the 3-ball setting (100 on 5-ball, manual): switch 9 (top) fires public 1, switch 10 "
			"(lower left) public 2 and switch 11 (lower right) public 3 in the retained gameplay run. The top bumper also changes the card selection. Printed solenoid numbers are 2, 1 and 5.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, SOLENOID_TEST_SOURCE,
		),
		mechanism(
			"mech.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"],
			"Two J-27-1500 slingshots. The ROM fires each coil when its switch closes, scores 10 and changes the card selection: switch 12 fires public 4 and switch 13 public 5 (retained gameplay run). "
			"Printed solenoid numbers are 6 and 7.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, SOLENOID_TEST_SOURCE,
		),
		mechanism(
			"mech.flippers", "Four dual-winding flippers, two per button", "other",
			["device.left-flippers", "device.right-flippers", "device.flipper-enable-relay"],
			["switch.left-flipper-button", "switch.right-flipper-button", "switch.left-flipper-end-of-stroke-contacts", "switch.right-flipper-end-of-stroke-contacts"],
			"Two flippers on each side, one above the other at the bottom of the playfield (playfield-parts drawing; IPDB `Flippers (4)`). Each side's lower (J-25-475/34-4500) and upper (J-25-500/34-5050) "
			"coils are wired in parallel on one drive wire (right A3J1-9, left A3J1-8) from the +43 VDC supply A2J1-6, through the contacts of the flipper enable relay to the side's single cabinet button "
			"(right A3J2-1, left A3J2-2). The relay is public 19 (printed solenoid 15): the ROM raises it when a game starts and drops it on a tilt and at game over (retained runs). Each coil's end-of-stroke "
			"contact is closed at rest and opens at the end of the stroke to insert the hold winding. PinMAME publishes one callback per side (46 right, 48 left, with 45 and 47 alongside), so a recreation "
			"moves both flippers of a side together.",
			MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE,
		),
		mechanism(
			"mech.ball-gates", "Passive ball gates", "gate", [], [],
			"Two one-way ball gates with no coil or switch: `BALL GATE ASS'Y. A-104-R2` at the top of the right lane and `LEFT GATE ASS'Y. A-104-L` at the top of the left loop (playfield-parts drawing). "
			"They route the ball by its own motion; do not invent a powered diverter.",
			MANUAL_SOURCE,
		),
	]
	return mechanisms


def build_relationships() -> list[dict[str, Any]]:
	relationships = []
	for source, destination in (
		("switch.top-thumper-bumper", "device.top-thumper-bumper"),
		("switch.lower-left-thumper-bumper", "device.lower-left-thumper-bumper"),
		("switch.lower-right-thumper-bumper", "device.lower-right-thumper-bumper"),
		("switch.left-slingshot", "device.left-slingshot"),
		("switch.right-slingshot", "device.right-slingshot"),
	):
		relationships.append({"id": f"rel.{destination.split('.', 1)[1]}-fired-by-its-switch", "kind": "direct", "source": source, "destination": destination, "provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.out-hole-kicker-follows-the-out-hole-switch", "kind": "pulse", "source": "switch.outhole", "destination": "device.out-hole-kicker", "provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.saucer-eject-follows-the-saucer-switch", "kind": "pulse", "source": "switch.saucer", "destination": "device.saucer-eject", "provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	for name, _, actuator, switches, _, _, _ in BANKS:
		for address in switches:
			relationships.append({"id": f"rel.{name}-bank-reset-raises-target-{address}", "kind": "pulse", "source": actuator, "destination": switch_id[address], "provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	for side in ("left", "right"):
		relationships.append({"id": f"rel.{side}-flipper-button-gated-by-the-enable-relay", "kind": "relay_gated", "source": f"switch.{side}-flipper-button", "destination": f"device.{side}-flippers",
			"provenance": provenance(SCHEMATIC_SOURCE, GAMEPLAY_SOURCE)})
	relationships.sort(key=lambda item: item["id"])
	return relationships


# --- Sources ------------------------------------------------------------------------------------------------------------

# excerpt name -> (source key, locator, has image)
EXCERPTS: dict[str, tuple[str, str, bool]] = {
	"switch-identification": (MANUAL_SOURCE, "PDF page 18, BIG GAME SWITCH IDENTIFICATION SELF TEST DISPLAY NUMBERS, all forty rows and the coin-door drawings", False),
	"switch-locations": (MANUAL_SOURCE, "PDF page 19, BIG GAME SWITCHES location drawing and the list of switches not on the playfield (PDF page 22 reprints it)", True),
	"solenoid-identification": (MANUAL_SOURCE, "PDF page 20, BIG GAME SOLENOID IDENTIFICATION SELF TEST DISPLAY NUMBERS", False),
	"solenoid-locations": (MANUAL_SOURCE, "PDF page 21, BIG GAME SOLENOIDS location drawing", True),
	"playfield-parts": (MANUAL_SOURCE, "PDF page 17, BIG GAME PLAYFIELD PARTS drawing and lists", True),
	"parts-list": (MANUAL_SOURCE, "PDF page 16, PARTS LIST BIG GAME #121", False),
	"mpu-switch-assignment": (MANUAL_SOURCE, "PDF pages 11-15, BIG GAME SWITCH ASSIGNMENT and the credit and game adjustment tables", False),
	"self-test": (MANUAL_SOURCE, "PDF pages 3 and 6, game self-diagnostic tests and the self-test and bookkeeping tables", False),
	"general-operation": (MANUAL_SOURCE, "PDF pages 2, 4 and 5, tilt switches, Figure 1 and III. GENERAL GAME OPERATION", False),
	"feature-operation": (MANUAL_SOURCE, "PDF pages 8-10, VI. FEATURE OPERATION & SCORING", False),
	"corrections": (CORRECTIONS_SOURCE, "The single page of the March 1980 corrections sheet", False),
	"lamp-driver-lamp-list": (SCHEMATIC_SOURCE, "PDF page 2, Lamp Driver Schematic 12B-432-S-121 for BIG GAME, typed lamp list", False),
	"lamp-driver-connector-labels": (SCHEMATIC_SOURCE, "PDF page 2, Lamp Driver Schematic, connector blocks J1, J2 and J3 with their SCR labels", True),
	"lamp-driver-decoder-outputs": (SCHEMATIC_SOURCE, "PDF page 2, Lamp Driver Schematic, decoder chips U1-U4 with their output resistors", True),
	"playfield-switch-matrix": (SCHEMATIC_SOURCE, "PDF page 9, Playfield Wiring Diagram BIG GAME, switch matrix", True),
	"playfield-coil-wiring": (SCHEMATIC_SOURCE, "PDF page 9, Playfield Wiring Diagram BIG GAME, coil and flipper wiring", True),
	"playfield-lamp-wiring-list": (SCHEMATIC_SOURCE, "PDF page 9, Playfield Wiring Diagram BIG GAME, typed lamp list", False),
	"cabinet-switch-matrix": (SCHEMATIC_SOURCE, "PDF page 8, Cabinet and Front Door Wiring, service buttons, cabinet matrix and cabinet loads", True),
	"solenoid-driver-j2-table": (SCHEMATIC_SOURCE, "PDF page 5, Solenoid Driver Voltage Regulator Schematic for BIG GAME, J2 table", True),
	"solenoid-driver-pin-labels": (SCHEMATIC_SOURCE, "PDF page 5, Solenoid Driver Voltage Regulator Schematic, output connector column", True),
	"solenoid-driver-continuous-section": (SCHEMATIC_SOURCE, "PDF page 5, Solenoid Driver Voltage Regulator Schematic, continuous outputs and flipper enable relay", True),
	"general-illumination": (SCHEMATIC_SOURCE, "PDF pages 6 and 7, Transformer Schematic and Wiring Diagram (shared drawings), general-illumination buses", False),
	"instruction-card": (CARD_SOURCE, "IPDB image-19.jpg, the apron instruction card 12B-2-121-21", False),
	"playfield-photographs": (PHOTO_SOURCE, "IPDB image-4.jpg (Playfield) and image-12.jpg (Upper Playfield)", False),
}

CROP_DERIVATIONS: dict[str, str] = {
	"lamp-driver-connector-labels": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 2, crop box 0.1216,0.3744,0.827,0.4177, scanned page rendered at its native resolution (embedded image xref 3, 3328px across 11.00in), rendered at 303 dpi, grayscale, rotated 270 degrees counter-clockwise, 224x2349 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"lamp-driver-decoder-outputs": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 2, crop box 0.1703,0.6026,0.827,0.7442, scanned page rendered at its native resolution (embedded image xref 3, 3328px across 11.00in), rendered at 152 dpi, capped to 1100px wide, grayscale, rotated 270 degrees counter-clockwise, 368x1101 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"playfield-switch-matrix": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 9, crop box 0.1459,0.5554,0.6841,0.8387, scanned page rendered at its native resolution (embedded image xref 17, 3328px across 11.00in), rendered at 166 dpi, capped to 980px wide, grayscale, rotated 270 degrees counter-clockwise, 799x981 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"playfield-coil-wiring": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 9, crop box 0.1459,0.3803,0.7601,0.5672, scanned page rendered at its native resolution (embedded image xref 17, 3328px across 11.00in), rendered at 133 dpi, capped to 900px wide, grayscale, rotated 270 degrees counter-clockwise, 424x901 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"cabinet-switch-matrix": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 8, crop box 0.073,0.5869,0.754,0.882, scanned page rendered at its native resolution (embedded image xref 15, 3328px across 11.00in), rendered at 174 dpi, capped to 1300px wide, grayscale, rotated 270 degrees counter-clockwise, 872x1301 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"solenoid-driver-j2-table": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 5, crop box 0.5169,0.7147,0.7449,0.8623, scanned page rendered at its native resolution (embedded image xref 9, 3328px across 11.00in), rendered at 303 dpi, grayscale, rotated 270 degrees counter-clockwise, 761x760 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"solenoid-driver-pin-labels": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 5, crop box 0.1368,0.3586,0.7449,0.4885, scanned page rendered at its native resolution (embedded image xref 9, 3328px across 11.00in), rendered at 224 dpi, capped to 1500px wide, grayscale, rotated 270 degrees counter-clockwise, 496x1501 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"solenoid-driver-continuous-section": "Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf page 5, crop box 0.1003,0.0026,0.3801,0.4295, scanned page rendered at its native resolution (embedded image xref 9, 3328px across 11.00in), rendered at 211 dpi, capped to 650px wide, grayscale, rotated 270 degrees counter-clockwise, 1534x651 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"switch-locations": "Stern_1980_Big_Game_Manual.pdf page 19, crop box 0,0,1,1, scanned page rendered at its native resolution (embedded image xref 90, 597px across 8.29in), rendered at 72 dpi, grayscale, 597x787 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"solenoid-locations": "Stern_1980_Big_Game_Manual.pdf page 21, crop box 0,0,1,1, scanned page rendered at its native resolution (embedded image xref 100, 599px across 8.32in), rendered at 72 dpi, grayscale, 599x788 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"playfield-parts": "Stern_1980_Big_Game_Manual.pdf page 17, crop box 0,0,1,1, scanned page rendered at its native resolution (embedded image xref 80, 596px across 8.28in), rendered at 72 dpi, grayscale, 596x786 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
}


def excerpt_record(name: str, root: Path) -> dict[str, Any]:
	_, locator, has_image = EXCERPTS[name]
	path = root / EXCERPT_ROOT / f"{name}.md"
	if not path.is_file():
		raise RuntimeError(f"Big Game excerpt is missing: {path}")
	record: dict[str, Any] = {
		"id": f"excerpt.big-game.{name}",
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
			raise RuntimeError(f"Big Game excerpt image is missing: {image}")
		record["image"] = f"{EXCERPT_ROOT}/{name}.webp"
		record["image_sha256"] = hashlib.sha256(image.read_bytes()).hexdigest()
		record["image_derivation"] = CROP_DERIVATIONS[name]
	if name in ("instruction-card", "playfield-photographs"):
		record["transcribed_by"] = "curator, read from the retained photograph"
	return record


def excerpts_for(source: str, root: Path) -> list[dict[str, Any]]:
	return [excerpt_record(name, root) for name, (key, _, _) in EXCERPTS.items() if key == source]


def build_sources(root: Path) -> list[dict[str, Any]]:
	digests = run_digests(root)
	runtime = load_json(root / RUNTIME_EVIDENCE_PATH)
	scenario = {run["name"]: run["scenario_sha256"] for run in runtime["runtime"]["raw_runs"]}
	manifest = runtime["source"]["sha256"]
	ipdb = "external:pinmame-manuals/by-machine/stern.big-game.1980/ipdb/"
	sources = [
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "src/wpc/stgames.c CORE_GAMEDEFNV(biggame) and the six CORE_CLONEDEFNV entries biggamfp, biggameb, biggamec, biggamed, biggamee and biggamef that name it as parent",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "src/wpc/stgames.c INITGAME(biggame, GEN_STMPU200, dispst7, FLIP_SW(FLIP_L), 0, SNDBRD_ST300, 0) and the identical INITGAME lines of its six clones, dispst7 layout; "
				"src/wpc/by35.c by35_lampStrobe, pia1b_w (solenoid decoder low nibble and the inverted continuous high nibble PB4-PB7); src/wpc/core.h sLRFlip/sLLFlip power and hold addresses 45-48",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/stern-mpu200.json", "revision": "repository",
			"locator": "Stern MPU-200 controller profile: matrix 1-40, diagnostics -7 to -5, flipper-button positions 81-84, option switches 1-32, decoder solenoids 1-15, continuous 17-20 and synthetic flipper outputs 45-48, "
				"sixty discrete SCR lamps 1-63, physical direct inputs 1-3 and uncontrolled GI identity 1",
			"license": "MIT", "attribution": "pinmame-game-defs curation"},
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://www.ipdb.org/files/249/Stern_1980_Big_Game_Manual.pdf", "original_filename": MANUAL_PDF, "sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-23T00:00:00Z",
			"locator": f"Stern Big Game game manual (IPDB 249 `English Manual [Stern Electronics, Inc.]`), 22 pages, 72 dpi colour JPEG scans without a text layer, retained at {ipdb}. Retrieved through the "
				"Internet Archive's Wayback Machine copy of the IPDB file. Pages 2-5 installation, maintenance, self test and operation; 6 self-test and bookkeeping table; 7 front-door adjustments; 8-10 "
				"feature operation; 11-15 option switches; 16 parts list; 17 playfield parts; 18 switch identification; 19 switch locations; 20 solenoid identification; 21 solenoid locations; 22 reprint of 19.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(MANUAL_SOURCE, root)},
		{"id": CORRECTIONS_SOURCE, "kind": "service_bulletin", "uri": "https://www.ipdb.org/files/249/Stern_1980_Big_Game_Corrections_to_Game_Manual_March_1980.pdf", "original_filename": CORRECTIONS_PDF,
			"sha256": CORRECTIONS_SHA256, "acquired_at": "2026-10-23T00:00:00Z",
			"locator": f"Stern `IMPORTANT` corrections sheet 12G-5C-121, March 1980 (IPDB 249 `Corrections to Game Manual (March 1980)`), one page, retained at {ipdb}. It corrects the bonus start, the bookkeeping "
				"pushes 20-24, the S8 and S22 settings and the ROM part numbers.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(CORRECTIONS_SOURCE, root)},
		{"id": SCHEMATIC_SOURCE, "kind": "manual", "uri": "https://www.ipdb.org/files/249/Stern_1980_Big_Game_Schematics_And_Wiring_Diagrams_Hi_resolution.pdf", "original_filename": SCHEMATIC_PDF,
			"sha256": SCHEMATIC_SHA256, "acquired_at": "2026-10-23T00:00:00Z",
			"locator": f"Stern schematics and wiring diagrams for Big Game (IPDB 249 `Schematics And Wiring Diagrams (Hi-resolution)`), nine 3328x5080 grayscale scans at about 300 dpi stored sideways, retained at {ipdb}. "
				"Page 1 MPU; 2 Lamp Driver Schematic 12B-432-S-121 for BIG GAME; 3-4 display boards; 5 Solenoid Driver Voltage Regulator Schematic for BIG GAME; 6 Transformer Schematic (general use); 7 Wiring Diagram "
				"(solid state, general); 8 Cabinet and Front Door Wiring (standard); 9 Playfield Wiring Diagram BIG GAME.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(SCHEMATIC_SOURCE, root)},
		{"id": IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=249", "acquired_at": "2026-10-23T00:00:00Z",
			"locator": "IPDB machine 249: Big Game, Stern Electronics, March 1980, model number 121, MPU Stern M-200, 2,713 units, widebody; notable features 'Flippers (4), Pop bumpers (3), Slingshots (2), Star rollovers (5), "
				"3-bank drop targets (3), Spinning targets (2), Standup targets (2), Kick-out hole (1)'; design Harry Williams, art Gerry Simkus and Doug Watson, software Alan McNeil. The page was read in a browser; "
				"its title and machine number match, and the retained manual, corrections sheet, schematics and photographs were downloaded from its links.",
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database"},
		{"id": CARD_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/images/249/image-19.jpg", "original_filename": "image-19.jpg", "sha256": CARD_PHOTO_SHA256, "acquired_at": "2026-10-23T00:00:00Z",
			"locator": f"IPDB 249 photograph `Instruction Card` by John Gray, 640x480, retained at {ipdb}photos/.",
			"license": "NOASSERTION", "attribution": "John Gray; hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(CARD_SOURCE, root)},
		{"id": PHOTO_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=249", "acquired_at": "2026-10-23T00:00:00Z",
			"locator": f"IPDB 249 photographs `Playfield` (image-4.jpg, 1024x771, SHA-256 {PLAYFIELD_PHOTO_SHA256}) and `Upper Playfield` by Darryl Macon (image-12.jpg, 750x563, SHA-256 {UPPER_PHOTO_SHA256}), retained at {ipdb}photos/.",
			"license": "NOASSERTION", "attribution": "Darryl Macon and IPDB contributors; hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(PHOTO_SOURCE, root)},
		{"id": SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{CORPUS_REVISION}/Big%20Game%20%28Stern%201980%29%20w%20VR%20Room%201.5.1.vbs",
			"revision": CORPUS_REVISION, "sha256": SCRIPT_SHA256,
			"locator": "Big Game (Stern 1980) w VR Room 1.5.1.vbs in the pinned known-working script corpus (jpsalas 4.1.1 reworked by Redbone and TastyWasps, December 2023), cGameName = \"biggame\": "
				"SolCallback 6 knocker, 7, 8 and 9 the drop banks (sw16-14, sw24-22, sw32-30), 10 the saucer (InitSaucer sw34, 34), 11 the out-hole (InitNoTrough, switch 33), 19 vpmNudge.SolGameOn; "
				"PulseSw 4, 5, 9-13, 20, 21, 37; Controller.Switch 17-19, 25-29, 35, 36, 38-40; NFadeL lamp bindings.",
			"license": "NOASSERTION", "attribution": "jpsalas, Redbone, TastyWasps and repository contributors", "known_working": True},
		{"id": OLD_SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{CORPUS_REVISION}/Big%20Game%20v1.0.4.vbs",
			"revision": CORPUS_REVISION, "sha256": OLD_SCRIPT_SHA256,
			"locator": "Big Game v1.0.4.vbs in the pinned script corpus (jpsalas 2017, updated by Thalamus 2018), the ancestor of the 1.5.1 script with the same solenoid, switch and lamp bindings. Its header says "
				"`Table not verified yet` and that the light and solenoid definitions came from an older script because of missing pages and errors in the manual; it is a lead and supplements only.",
			"license": "NOASSERTION", "attribution": "jpsalas, Thalamus and repository contributors"},
		{"id": TABLE_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{(TABLE_RELATIVE / TABLE_FILENAME).as_posix()}", "original_filename": TABLE_FILENAME, "sha256": TABLE_SHA256,
			"revision": "redbone MOD v1.2.0 (table version 4.1.1)", "acquired_at": "2026-10-23T00:00:00Z",
			"locator": f"Big Game (Stern 1980) - redbone(MOD) v1.2.0, jpsalas' table 4.1.1 (15.02.2023) with redbone's graphics, 18,329,600 bytes, from the operator's table folder; the VPU download archive "
				f"`{TABLE_ARCHIVE_FILENAME}` (SHA-256 {TABLE_ARCHIVE_SHA256}) holds the identical file and is retained beside it. Exact playfield bounds left 0, top 0, right 1093, bottom 2115; normalized "
				"coordinates are x/1093 and y/2115. The geometry source for every located placement; it models four flippers, two per side, the three banks, the saucer and the two spinners on the left loop wire as the "
				"factory drawings do. The later 1.5.1 build whose script is pinned here says it corrects the dimensions, so this build's geometry may differ from it.",
			"license": "NOASSERTION", "attribution": "jpsalas and redbone; redistribution rights not granted", "rights": "NOASSERTION"},
		{"id": TABLE_SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"external:pinmame-vpx-sources/{(EXTRACTION_RELATIVE / 'script.vbs').as_posix()}", "original_filename": "script.vbs", "sha256": TABLE_SCRIPT_SHA256,
			"locator": "Embedded script of the retained table (jpsalas VPX version 4.1.1), 30,888 bytes, cGameName = \"biggame\". Its SolCallback, switch-handler and lamp bindings are identical to the pinned 1.5.1 "
				"and 1.0.4 corpus scripts (74 lamp-to-light pairs, nine solenoid callbacks and 22 switch handlers compared); it binds each placement's object.",
			"license": "NOASSERTION", "attribution": "jpsalas and redbone", "known_working": True},
		{"id": EXTRACTION_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE.as_posix()}", "sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": f"Retained vpxtool git:v0.33.3 extraction of the table; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256} (tools/build_external_evidence_manifest.py: every file as sorted relative POSIX path, "
				f"size and SHA-256, compact canonical JSON plus LF, the manifest files excluded); {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
			"license": "NOASSERTION", "attribution": "jpsalas and redbone; redistribution rights not granted"},
		{"id": CALLOUT_SOURCE, "kind": "human_review", "uri": f"internal:{CALLOUT_SEED_PATH.as_posix()}", "sha256": hashlib.sha256((root / CALLOUT_SEED_PATH).read_bytes()).hexdigest(),
			"locator": "Factory location-drawing callout check of the manual's switch drawing (PDF page 19) and solenoid drawing (PDF page 21): every callout transcribed independently from gridded tiles of 216 dpi "
				"renders without table data, verified by overlay, with per-page control and callout fits; a table placement whose own callout lands within 0.07 normalized under both fits is validated "
				"(tools/drawing_callouts.py). Reads, overlays and tiles are retained under external:pinmame-review-artifacts/big-game-1980/callout-check with a pinned manifest.",
			"license": "NOASSERTION", "attribution": "pinmame-game-defs contributors", "rights": "NOASSERTION"},
	]
	for name in RUN_NAMES:
		sources.append({
			"id": RUN_SOURCES[name],
			"kind": "service_diagnostic" if name in ("self-test", "solenoid-test", "switch-test") else "runtime_scenario",
			"uri": f"external:pinmame-review-artifacts/big-game-1980/harness/{name}/run.json",
			"sha256": digests[name],
			"locator": f"tools/run_pinmame_harness.py with pinmame64.dll SHA-256 {LIBRARY_SHA256} (built from {PINMAME_REVISION[:12]}), driver biggame, ROM archive SHA-256 {ROM_ARCHIVE_SHA256}; "
				f"scenario tools/harness-scenarios/stern/biggame-{name}.json (SHA-256 {scenario[name]}), fresh state directory. Run directory manifest SHA-256 {manifest}; compact derived evidence in {RUNTIME_EVIDENCE_PATH.as_posix()}.",
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		})
	return sources


# --- Definition ---------------------------------------------------------------------------------------------------------

MISSING = ["output_semantics", "spatial_placement"]


def build_definition(root: Path = ROOT) -> dict[str, Any]:
	if len(data.SWITCHES) != 40 or set(data.DIPS) != set(range(1, 33)):
		raise RuntimeError("Big Game switch or option-switch inventory is incomplete")
	if sorted(data.PHYSICAL_TO_PUBLIC) != list(range(1, 20)) or set(data.SOLENOIDS) != set(data.PHYSICAL_TO_PUBLIC.values()):
		raise RuntimeError("Big Game solenoid inventory is incomplete")
	if {q for qs in data.DECODER.values() for q in qs} != set(range(1, 61)):
		raise RuntimeError("Big Game decoder map does not cover SCRs 1-60 exactly once")
	runtime = load_json(root / RUNTIME_EVIDENCE_PATH)["runtime"]["observations"]
	if {int(key): value for key, value in runtime["physical_service_solenoid_to_public"].items()} != data.PHYSICAL_TO_PUBLIC:
		raise RuntimeError("Big Game solenoid translation disagrees with the retained solenoid test")
	definition = build_unchecked_definition(root)
	drawing_callouts.apply_to_definition(definition, callout_seed(root), CALLOUT_SOURCE)
	return definition


def callout_seed(root: Path = ROOT) -> dict[str, Any]:
	return load_json(root / CALLOUT_SEED_PATH)


def build_unchecked_definition(root: Path = ROOT) -> dict[str, Any]:
	return {
		"conflicts": [],
		"controller": {"inversion_applied_by_emulator": True, "platform": "pinmame.stern-mpu200"},
		"coverage": {
			"dimensions": {
				"address_enumeration": "validated",
				"catalog_identity": "validated",
				"causal_exercise": "observed",
				"diagnostic_enumeration": "validated",
				"emulator_normalization": "validated",
				"mechanisms": "validated",
				"physical_wiring": "validated",
				"recreation_knowledge": "validated",
				"runtime_observation": "observed",
				"semantic_naming": "observed",
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
		"inputs": build_inputs(),
		"knowledge": {"path": KNOWLEDGE_PATH.as_posix(), "status": "complete"},
		"machine": {"id": MACHINE_ID, "ipdb_id": 249, "kind": "physical_pinball", "manufacturer": "Stern", "model_number": "121", "name": "Big Game", "opdb_id": "G4jQw-MJ5rl", "year": 1980,
			"playfield": {"height": data.TABLE_HEIGHT, "provenance": provenance(TABLE_SOURCE), "units": "vpx", "width": data.TABLE_WIDTH}},
		"mechanisms": build_mechanisms(),
		"outputs": build_outputs(),
		"relationships": build_relationships(),
		"schema_version": 2,
		"sources": build_sources(root),
	}


# --- Spatial report -----------------------------------------------------------------------------------------------------


def build_spatial_report(definition: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
	located: list[dict[str, Any]] = []
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
				located.append({**record, "placements": len(spatial["placements"])})
				for placement in spatial["placements"]:
					statuses[placement["provenance"]["status"]] = statuses.get(placement["provenance"]["status"], 0) + 1
	projections = [{"address": address, "group": "pinmame.input.switch", "reason": reason} for address, (_, reason) in sorted(data.SWITCH_OBJECTS.items()) if reason]
	projections += [{"address": address, "group": "pinmame.output.solenoid", "reason": reason} for address, (_, reason) in sorted(data.SOLENOID_OBJECTS.items()) if reason]
	projections += [{"address": address, "group": "physical.input.direct", "reason": f"Placed on the {side} flipper pivots (lower, upper): each end-of-stroke contact is mounted on its flipper assembly."}
		for address, side in ((1, "left"), (2, "right"))]
	projections += [{"address": address, "group": "pinmame.output.solenoid", "reason": f"Placed on the two {side} flipper pivots, both moved by this one callback."} for address, side in ((46, "right"), (48, "left"))]
	seed = callout_seed(root)
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition), seed.get("limit", drawing_callouts.LIMIT))
	check = drawing_callouts.summary(seed, decisions, CALLOUT_SEED_PATH.as_posix(), hashlib.sha256((root / CALLOUT_SEED_PATH).read_bytes()).hexdigest())
	return {
		"blockers": [
			"Public 20 (continuous driver Q18) is driven by the ROM in attract mode with no documented load, so its availability stays unknown and output semantics stays missing; see the knowledge note.",
			"Every lamp placement is `observed`: the manual prints no lamp-location drawing, and there is one retained factory-layout table, so nothing independent can check the lamp positions; the IPDB "
			"photographs confirm order and side by eye only.",
			"General illumination has no placement: no retained source gives its bulb quantity or positions, and the table's GI light collection is render membership, not a socket count.",
			"Switch and coil placements the factory drawings do not confirm under the callout check stay `observed`; they are listed under `callout_check.not_validated`.",
		],
		"callout_check": check,
		"coordinate_convention": {"source_bounds": {"bottom": data.TABLE_HEIGHT, "left": 0.0, "right": data.TABLE_WIDTH, "top": 0.0}, "space": "playfield",
			"x": f"x/{data.TABLE_WIDTH}; 0=left, 1=right", "y": f"y/{data.TABLE_HEIGHT}; 0=rear/backglass, 1=apron/player"},
		"excluded_object_classes": [
			"gi*, Light001-Light007 and accent* lights: render and general-illumination helpers; Big Game's general illumination has no controller address and no bulb inventory in any retained source",
			"l13, l29, l45, l61, l63: backglass text boxes of the backbox lamps (a controlled cabinet_or_service record each)",
			"l14, l15, l16, l30, l31: glows under the five star roll-over buttons (not bulb lights); the script binds them to lamp numbers 14, 15, 16, 30 and 31 and keeps them lit, and no printed row names a lamp under a button",
			"BallRelease: the shooter-lane kicker the script serves the ball from, a virtual destination rather than the out-hole kicker",
			"Gate2: a hidden gate in the shooter lane; Gate1 and Gate3 are the two passive gates of the mechanism record and carry no controller binding",
		],
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_algorithm": "tools/build_external_evidence_manifest.py: every file as sorted relative POSIX path, size and SHA-256, compact canonical JSON plus LF, manifest files excluded",
			"manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE.as_posix()}/manifest.json", "source_ref": EXTRACTION_SOURCE, "total_bytes": EXTRACTION_TOTAL_BYTES,
			"table_sha256": TABLE_SHA256, "script_sha256": TABLE_SCRIPT_SHA256, "vpxtool_version": "git:v0.33.3"},
		"format": "pinmame-spatial-blockers",
		"located_records": sorted(located, key=lambda item: item["id"]),
		"machine_id": MACHINE_ID,
		"not_applicable_records": {reason: sorted(ids) for reason, ids in sorted(not_applicable_records.items())},
		"placement_statuses": dict(sorted(statuses.items())),
		"projections": projections,
		"readiness": {"missing": definition["coverage"]["missing"], "status": definition["coverage"]["status"], "unresolved_conflicts": len(unresolved_conflicts(definition))},
		"table_lamp_defects": {str(address): note for address, note in sorted(data.LAMP_TABLE_NOTES.items()) if address in (5, 6, 30, 37)},
		"unplaced_records": sorted(unplaced, key=lambda item: item["id"]),
		"version": 1,
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["callout_check"]
	lines = [
		"# Big Game (Stern, 1980) spatial review",
		"",
		"Status: incomplete. Every lamp placement is `observed` and general illumination has none, so the machine record stays `partial` at `machines/partial/stern/big-game-1980.json`.",
		"",
		f"The geometry source is the retained `{TABLE_FILENAME}` at SHA-256 `{TABLE_SHA256}`; its embedded script (SHA-256 `{TABLE_SCRIPT_SHA256}`) binds the same lamps, switches and coils as the pinned "
		f"known-working 1.5.1 script. Exact playfield bounds are left 0, top 0, right {data.TABLE_WIDTH:g}, bottom {data.TABLE_HEIGHT:g}, and every canonical coordinate is x/{data.TABLE_WIDTH:g} and y/{data.TABLE_HEIGHT:g} "
		"rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, in normalized VPX/player view.",
		"",
		"## Evidence decisions",
		"",
		"- The script's bindings choose each switch's and coil's object. Lamps are placed on the light at the insert their printed row names; where no row names an insert, on the light the script binds.",
		"- Four lamps are bound differently by the table than by this game's Lamp Driver Schematic. The ROM sides with the sheet wherever it can tell: the left spinner and the right roll-over buttons "
		"scored their lit values while the sheet's lamps (37 and 5) were on and the table's (6 and 34) were off. The placements follow the sheet and the defects are stated on the devices:",
	]
	lines += [f"  - lamp {address}: {note}" for address, note in report["table_lamp_defects"].items()]
	lines += ["", "## Explicit projections", ""]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += ["", "## Factory drawing callout check", "", check["rule"], ""]
	for key, page in check["pages"].items():
		lines.append(f"- {page['locator']}: {page['controls']} controls (leave-one-out max {page['control_loo_max']}), {page.get('callout_pairs', 0)} callout pairs, "
			f"callout fit on {page.get('callout_fit_pairs', 0)} (leave-one-out max {page.get('callout_loo_max')})")
	lines.append(f"- Validated {check['validated']} of {check['checked']} checked placements" + (f"; not validated: {', '.join(sorted(check['not_validated']))}" if check["not_validated"] else ""))
	lines += ["", "## Counts", ""]
	lines.append(f"- Placements: {sum(item['placements'] for item in report['located_records'])} ({', '.join(f'{count} {name}' for name, count in report['placement_statuses'].items())}) on {len(report['located_records'])} records")
	for reason, ids in report["not_applicable_records"].items():
		lines.append(f"- Records with a controlled `{reason}` record: {len(ids)}")
	lines.append(f"- Records with no spatial key: {len(report['unplaced_records'])} ({', '.join(item['id'] for item in report['unplaced_records']) or 'none'})")
	lines += ["", "## Excluded table objects", ""]
	lines += [f"- {entry}" for entry in report["excluded_object_classes"]]
	lines += ["", "## Blockers", ""]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Promotion decision", "",
		"Promotion to `author_ready` is refused: public 20's output is unexplained, every lamp placement rests on one table with no lamp-location drawing to check it, and general illumination has no "
		"placement. The record stays `partial` with `coverage.missing = [\"output_semantics\", \"spatial_placement\"]`.", "",
		"## Retained evidence", "",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Object-centre dump of every extracted game item at `external:pinmame-review-artifacts/big-game-1980/redbone-1.2.0-geometry.tsv`.",
		f"- Callout reads, tiles and overlays under `external:pinmame-review-artifacts/{check['retained_artifacts']['directory']}`.", ""]
	return "\n".join(lines)


# --- Knowledge note -----------------------------------------------------------------------------------------------------

KNOWLEDGE = """# Big Game (Stern, 1980)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; one continuous output's purpose is unexplained, the lamp placements rest on one table and general illumination is unplaced**

## Identity and evidence precedence

This is the one physical Stern Big Game (IPDB 249, March 1980, model 121, Stern M-200 MPU, 2,713 units, Stern's first widebody). PinMAME `biggame` is the production root and `biggamfp` its stock free-play clone;
`biggameb`, `biggamec`, `biggamed`, `biggamee` and `biggamef` are the community rules revisions 7, 8, 9, 12 and 13 (2019-2024). All seven use the same game-data line (`GEN_STMPU200`, seven-digit `dispst7`
displays, `FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound), so they are physically identical and only the ROM rules differ. Only `biggame.zip` was used for the harness runs.

Evidence order is the runbook's. The two pinned corpus scripts give runtime bindings (the 1.5.1 VR build is the working one; the older 1.0.4 script says it was not verified), this game's own manual, March 1980
corrections sheet and schematic set give construction and wiring, pinned PinMAME gives the controller topology, and five retained harness runs of `biggame` (burn-in, solenoid test, switch test, a scripted game, and a
game-over and slam run) pair the printed numbers with public addresses. The manual is a 72 dpi scan without a lamp-location drawing; the schematic set is a 300 dpi scan whose Lamp Driver, Solenoid Driver and Playfield
Wiring sheets are drawn for this game.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty (retained run), so the Switch Identification
numbers are the public addresses. All forty positions are fitted. Cabinet switches 1-3 (coin chutes), 6 (credit), 7 (tilt) and 8 (slam) are wired on the cabinet sheet to MPU connector A4J3, the others on the playfield
sheet to A4J2. Every matrix contact is normally open, and the sheets draw a series 1N4004 diode on each except coin chutes 2 and 3, which the cabinet sheet draws without one. PinMAME's BY35 read path takes them unmasked, so public 1 is a closed contact. Service inputs are -7 (Self Test), -6 (CPU diagnostic
NMI) and -5 (sound diagnostic); the last two are PinMAME routes with no documented button. The flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' end-of-stroke
contacts and the door's remote S33 memory-clear button are hard-wired and have only profile-local identities (physical direct inputs 1-3).

**Solenoids.** The printed solenoid numbers are SDU driver transistor positions, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires, pairing them as
`1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over three identical cycles. In public terms: 1 top thumper, 2 lower left thumper,
3 lower right thumper, 4 left slingshot, 5 right slingshot, 6 knocker, 7 top-left bank reset, 8 top-right bank reset, 9 lower-right bank reset, 10 saucer eject, 11 out-hole kicker, 18 coin lockout, 19 flipper
enable relay. Public 12-15 (drivers 10, 12, 11, 16) are printed OPEN and unused; 16 is an unaddressable decoder slot. The gameplay run independently confirms 1-5 and 7-11 and 19.

**Continuous outputs 17 and 20.** Public 17 is driver Q17 (PIA PB4). The manual prints it OPEN and the parts list names no relay, but the Solenoid Driver Schematic drawn for this game labels its J5 pin 7
`GEN. ILLUM. RELAY`. No other sheet has a relay in any general-illumination circuit, and the ROM drives 17 only in the power-up initialisation pulse it gives all four continuous lines and in its own tests.
It is recorded unused, with the label stated, as Star Gazer's record treats its own solenoid-sheet label on an OPEN position. Award events were not exercised, because PinMAME's default option switches
disable them. Public 20 is driver Q18 (PB7). The manual prints it OPEN and the schematic wires it only to N/U pins, yet the ROM holds it on for about 1.5 s whenever the displays flash `7777777` in
attract mode. Nothing documents a load or a reason, so it stays `unknown` and `output_semantics` stays in `coverage.missing`. Settling it needs the ROM's attract routine decoded, or an owner's check of whether
anything is connected to SDU J2 pin 15, J3 pin 9 or J5 pin 3. Static analysis found the ROM's generic set and clear routines for the four continuous bits at 0x1816 and 0x1829, but not yet their callers.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`; this game's sheet
was read for all sixty lines and matches the LDA-100 order other Stern MPU-200 games use, including the transposable U2 S7/S8 (Q25/Q24) and U3/U4 S9 (Q41/Q46) pairs. The connector blocks give each SCR its pin.
The Lamp Driver Schematic's list has 56 rows, the playfield list the same rows without the four backbox lamps (GAME OVER 45, HIGH SCORE TO DATE 13, MATCH 63, TILT 61), and the 56 rows land on 56 different public
addresses. Every lamp the ROM lit for a switch in the gameplay run is the one its row names: B, I and G for the top lanes (42, 26, 10), the second G and A for the stand-ups (57, 41), E for the right return lane (9), the
card numbers each drop target spots, and the B-I-G awards (6 and 30). The four SCRs without a row, public 14, 15, 31 and 47, change only in the burn-in and lamp tests and are unused. Public 25, the letter M, sits on J1
pin 5, but the connector block's J1 row for its SCR (Q24) prints a flat-topped figure that reads as 3 or 5; the ROM flashes 25 with the other six letters when the saucer collects them.

The seven letter lamps (9, 10, 25, 26, 41, 42, 57) each light two inserts, the letter at its own lane or target and the letter in the B-I-G-G-A-M-E column beside the eject-pocket lane (instruction card, IPDB
photographs). General illumination is an uncontrolled 6 VAC playfield string, the front-door lamp and 5.9 VAC backbox lamps straight from the transformer.

## Ball lifecycle

Big Game is a single-ball game with no trough. The ball starts on the out-hole switch (33). When a game starts the ROM resets the three drop banks (7, 8, 9) and kicks the out-hole (11), repeating both for as long as 33
stays closed; a real ball leaves 33 on the first kick and rolls to the shooter lane, where the player launches it. After a drain the bonus and multiplier are added, the ball-in-play digit advances and the kick repeats;
an extra ball is played without advancing. Tilt drops the flipper enable relay (19) and disqualifies the ball only (instruction card); a slam (8) ends the game and the ROM restarts through its power-up test.

## Mechanisms

- **Three drop banks**, each three targets with one reset coil: top-left 1A (targets 3, 2, 1 top to bottom = switches 14, 15, 16; reset 7), top-right 1B (4, 5, 6 = switches 24, 23, 22; reset 8) and lower-right 1C
  (7, 8, 9 = switches 32, 31, 30; reset 9). The ROM resets a bank when its last target goes down and at every serve. Each target spots its number in the selected cards.
- **Eject pocket (saucer)** at the top of the left loop: switch 34, eject coil 10.
- **Spinners**: two on one wire across the left loop, left (4) at the outer end and right (5) beside the top-left bank; no coil.
- **Thumper bumpers** 9 (top), 10 (lower left), 11 (lower right) fire public 1, 2 and 3; **slingshots** 12 and 13 fire 4 and 5.
- **Flippers**: four, two per side at the bottom of the playfield, each side's lower (J-25-475/34-4500) and upper (J-25-500/34-5050) coils in parallel on one drive wire and one cabinet button, gated by the flipper
  enable relay. PinMAME publishes one callback per side (46 right, 48 left, with 45 and 47 alongside).
- **Passive gates** at the top of the right lane and the top of the left loop.

## Rules summary

From the instruction card and the manual's feature pages: three bingo-style cards X, Y and Z of nine numbers each; drop targets spot their numbers in the selected card or cards, and the card selection changes on
the top bumper, the slingshots, the center roll-over button and the top lanes. Each lit number adds 1,000 bonus; a full set of cards moves the 27,000 bonus to the reserve. Lines on the cards light 2X and 3X, the 5,000
extra score per line, the right outlane extra ball and the left outlane special. Spotting B-I-G-G-A-M-E lights the letters in the eject-pocket lane; the pocket scores 5,000 per lit letter and 35,000 more when the word is
made, and the left center side lane awards the extra ball the first time and the special the second. The top lanes score 500 and 5,000 for the middle lane when BIG is lit; the right roll-over buttons score 2,000 when Z is
lit.

## Scoring checkpoints from the retained gameplay run

Thumpers 1,000; slingshots 10; top lanes, stand-ups and drop targets 500; the left spinner 2,000 with card X selected and the right spinner 100 before B-I-G; the center roll-over, the left center side lane and the return
lanes 5,000; the outlanes 10,000; the top 10-point switches 10; the right roll-over buttons 2,000 with card Z selected; the top-left roll-over 5,000 after B-I-G (the manual says 3,000, the playfield art and the ROM
5,000); the saucer 35,000 after B-I-G-G-A-M-E. These are first-ball ROM scores and only checkpoints.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32 (Figure 1, page 11). Coin chutes 2, 3 and 1 take S1-5, S9-13 and S27-30. S6 high-score award, S7 balls per game, S8 background sound, S15-16 high game to date,
S17 extra ball, S18-19 maximum credits, S20 credit display, S21 match, S22 special replay limit, S23 card selection order, S25-26 the ball on which the 5,000-per-line feature comes on, S31-32 special award; S14 and S24 are
not used. The March 1980 corrections sheet reverses the printed S8 (ON = sound off) and S22 (ON = one replay per ball) settings. S33 on the MPU is a memory-clear pushbutton, repeated on the coin door.

## Displays and sound

Four seven-digit player displays (indices 0-3, segment starts 1, 9, 17 and 25), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME `dispst7`.
Big Game was the first electronic game with seven-digit displays; in attract mode all four count `1234567` and flash `7777777`. Sound is the Stern B-605 sound board (ST300); sound commands add no playfield devices.

## Disagreements between this game's own documents

- The feature text names the top bumper `SWS-#11` once and `SW-#9` once; the switch table, the matrix sheet, the location drawing and the ROM put it on 9.
- The credit tables call coin switch 1 `BLUE` and switch 3 `RED-WHITE`; the cabinet sheet prints `R-W` on switch 1's return and `BLU` on switch 3's. A wire-colour difference only.
- The switch table calls switch 27 a roll-over button; the matrix sheet, the location drawing and the parts drawing make it a roll-over wire, which is what the definition records.
- The manual says the top-left roll-over scores 3,000 when BIG is made; the playfield art and the ROM give 5,000.

## Recreation checklist

- Build the full inventory: 40 matrix switches, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 with the two flipper callbacks, the sixty SCR lamp addresses
  and the six displays.
- Start with the ball on the out-hole switch, all nine drop targets up, the saucer empty and the flipper enable relay off until a game starts.
- Reproduce the ROM-fired thumpers and slingshots, the three bank resets, the saucer eject, the out-hole serve loop and the tilt behaviour as the harness runs show.
- Drive both flippers of a side from one callback; drive both inserts of a letter from one lamp.
- Treat the instruction card and the ROM as the rules authority; the community MOD ROMs change rules, not hardware.
- Wire lamps 5, 6, 30 and 37 to the inserts this game's lamp sheet names, not the ones the retained table drives (next section).
- Placements: switches and coils come from the retained table and are checked against the factory drawings (the spatial report lists the outcome); lamps are observed from the table only; general illumination is unplaced.

## Retained table and its lamp-binding defects

The geometry comes from `Big Game (Stern 1980) - redbone(MOD) v1.2.0`, jpsalas' table 4.1.1 with redbone's graphics. Its script binds exactly the same lamps, switches and coils as the pinned 1.5.1 and 1.0.4 corpus scripts.
It models four flippers, two per side, and the drop banks, saucer and spinner wire where the factory drawings put them. Its lamp map comes from an older script (its header says so, because of "missing pages and errors on the manual").
It matches this game's Lamp Driver Schematic everywhere except four lamps:

- Lamp 6 (`TOP R.O.W. "I" 5,000`) is bound to the two spinner value inserts; the table lights the `5.000 WHEN LIT` insert above the middle lane itself whenever B, I and G are lit, the same condition the ROM uses for lamp 6.
- Lamp 30 (`RIGHT SPIN. TARG. 1,000`) is bound to a glow under the top-left roll-over button; the right spinner's `100 OR 1000 WHEN LIT` insert is on lamp 6 in the table.
- Lamp 37 (`"X" & LEFT SPIN. TARG.`): the table drives the left spinner's `200 OR 2000 WHEN LIT` insert from lamp 6. The ROM scored the left spinner at 2,000 with card X (37) on and lamp 6 off, so the table is wrong.
- Lamp 5 (`"Z" & R. 1,000 WHEN LIT`): the table drives the right roll-over buttons' `2.000 WHEN LIT` insert from lamp 34 (the reserve bonus). The ROM scored those buttons at 2,000 with card Z (5) on and lamp 34 off, so the table is wrong.

The definition places each of these lamps on the insert its printed row names. The eject pocket's `15.000 WHEN LIT` insert is named by no printed row; it is placed under lamp 53, as the script binds it, with the bulb count left unstated. The top-left roll-over button's `500 OR 5000 WHEN LIT` has no lamp in any printed row and is not placed.

## Sources

- `manual.stern.big-game.1980`: the 22-page IPDB manual, with transcribed excerpts of its identification tables, location drawings, parts pages, option switches and operating text.
- `manual.stern.big-game.corrections-1980-03`: the March 1980 corrections sheet.
- `schematic.stern.big-game.wiring-set`: the nine-page IPDB schematic set, with excerpts of the lamp driver, solenoid driver, playfield and cabinet sheets.
- `photo.ipdb-249.instruction-card` and `photo.ipdb-249.playfield`: IPDB photographs of the instruction card and the playfield.
- `vpx-script.big-game-vr-1-5-1` and `vpx-script.big-game-1-0-4`: the pinned corpus scripts.
- `vpx-table.big-game-redbone-1-2-0`, its embedded script and its retained extraction: the geometry of every placement.
- `review.big-game.drawing-callouts`: the factory location-drawing callout check.
- `runtime.big-game.*`: five isolated harness runs of `biggame` (ROM archive SHA-256 `e5cedcdb33f648a2a735fa4c250b9a379a935c06370c7c67500fe2cf70bc8043`) on the pinned `pinmame64.dll`; ROM bytes and raw NVRAM
  remain outside the repository.
- `pinmame.core.97aa922bf8e4`: driver declarations, MPU-200 implementation, public-address conversion and display layout.
"""


# --- Generation and checking ------------------------------------------------------------------------------------------


def products(root: Path = ROOT) -> dict[Path, bytes]:
	definition = build_definition(root)
	errors = validate_machine(definition, root)
	if errors:
		raise RuntimeError("Invalid Big Game definition: " + "; ".join(errors[:20]))
	report = build_spatial_report(definition, root)
	return {
		DEFINITION_PATH: canonical_bytes(definition),
		SEED_PATH: canonical_bytes(definition),
		SPATIAL_REPORT_PATH: canonical_bytes(report),
		SPATIAL_REPORT_MARKDOWN_PATH: render_spatial_report(report).encode("utf-8"),
		KNOWLEDGE_PATH: KNOWLEDGE.encode("utf-8"),
	}


def generate(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Big Game artifact")
	for path, payload in products(root).items():
		(root / path).parent.mkdir(parents=True, exist_ok=True)
		(root / path).write_bytes(payload)


def check(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("A Big Game author-ready definition is present although the record is partial")
	for path, payload in products(root).items():
		if not (root / path).is_file() or (root / path).read_bytes() != payload:
			raise RuntimeError(f"Big Game deterministic artifact missing or drifted: {path}")
	print("Big Game definition, seed, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, knowledge note and spatial report")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		generate(ROOT)
		print(f"Wrote {DEFINITION_PATH}")


if __name__ == "__main__":
	main()
