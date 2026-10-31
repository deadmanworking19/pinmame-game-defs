"""Fail-closed tests for the Bally Frontier (1980) definition.

Frontier's printed solenoid numbers are test order, its lamp functions come from the board chain plus
its own lamp sheets, and no lamp can be placed because the only retained table models no lamp bulb.
Each of those is asserted separately, against the retained runtime summary where the ROM decided
it, so a regression names the fact that broke. The external-evidence checks skip cleanly when their
root is not configured.
"""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import ExitStack, redirect_stderr
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import frontier_runtime_summary  # noqa: E402

MACHINE_ID = "bally.frontier.1980"
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "frontier-1980.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "frontier-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "frontier-1980.md"
SUMMARY_PATH = ROOT / "evidence" / "runtime" / "by35" / "frontier-1980-harness.json"
SPATIAL_SEED = ROOT / "tools" / "seeds" / "bally" / "frontier-1980-spatial.json"
READINGS_SEED = ROOT / "tools" / "seeds" / "bally" / "frontier-1980-display-readings.json"
REPORT_JSON = ROOT / "reports" / "spatial" / "bally" / "frontier-1980.json"
REPORT_MD = ROOT / "reports" / "spatial" / "bally" / "frontier-1980.md"
CURATOR = ROOT / "tools" / "curate_frontier.py"
SCENARIOS = sorted((ROOT / "tools" / "harness-scenarios" / "by35").glob("frontier-*.json"))

# Printed solenoid self-test number -> (public address, device id), as paired by the ROM's own test.
TEST_TO_PUBLIC = {
	1: (7, "device.outhole-kicker"), 2: (6, "device.knocker"), 3: (9, "device.right-drop-target-reset"),
	4: (10, "device.saucer-kicker"), 5: (8, "device.in-line-drop-target-reset"), 6: (11, "device.left-thumper-bumper"),
	7: (12, "device.right-thumper-bumper"), 8: (13, "device.bottom-thumper-bumper"), 9: (14, "device.left-slingshot"),
	10: (15, "device.right-slingshot"), 11: (17, "device.gate"), 12: (18, "device.coin-lockout-door"), 13: (19, "device.k1-relay-flipper-enable"),
}
# Playfield switch -> the coil its closure fires in gameplay.
SWITCH_TO_COIL = {37: 14, 36: 15, 40: 11, 39: 12, 38: 13, 12: 10, 8: 7}
UNUSED_SWITCHES = {17, 18, 19, 20, 26, 28, 32, *range(41, 49)}
UNDOCUMENTED_DIPS = {21, 22, 29}
BACKBOX_LAMPS = {11: "Shoot again", 13: "Ball in play", 27: "Match", 29: "High score to date", 45: "Game over", 61: "Tilt"}
# The plug-connector sheet's Table B: the A5 J2 pins routed on to the playfield, and their lamps.
TABLE_B = {"A5J2-14": 15, "A5J2-2": 47, "A5J2-15": 31, "A5J2-16": 14, "A5J2-20": 30, "A5J2-1": 63, "A5J2-6": 46, "A5J2-7": 62}
LAMP_ADDRESSES = [n for n in range(1, 64) if n % 16 != 0]
PINMAME_COMMITTED_AT = "2026-10-25T20:16:49Z"
ACQUIRED_AT = {
	"pinmame.catalog.46e1a01a0f73": PINMAME_COMMITTED_AT,
	"pinmame.core.46e1a01a0f73": PINMAME_COMMITTED_AT,
	"controller-profile.pinmame-by35": PINMAME_COMMITTED_AT,
	"ipdb.959": "2026-10-31T09:29:17Z",
	"manual.bally.frontier.1980": "2026-10-31T09:28:53Z",
	"schematic.bally.frontier.1980": "2026-10-31T09:28:55Z",
	"vpinmame-library.bally-vbs": "2026-10-31T10:05:51Z",
	"vpx-script.frontier.2-0": "2026-07-07T06:37:05Z",
	"vpx-table.frontier.2-0": "2026-10-31T09:33:20Z",
	"runtime.frontier.harness": "2026-10-31T10:34:14Z",
}
ROM_ARCHIVES = {
	"frontier": "6c8b4de20bb7a2d923f2dada33c6452001a2d78c9e48c35b91d3e370641f8606",
	"frontiea": "65c890dabfc3a818ce850a16b10041d10372223aefedbc497a2a1dad6efc8e80",
}
FRONTIEG_U6_SHA1 = "caf44646d29211ddc5c2eea17ebb4a2e94eaa0f4"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def file_digest(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def configured(name: str) -> Path | None:
	value = os.environ.get(name)
	return Path(value) if value else None


class FrontierDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.summary = load(SUMMARY_PATH)
		cls.seed = load(SPATIAL_SEED)
		cls.inputs = cls.definition["inputs"]
		cls.outputs = cls.definition["outputs"]
		cls.switches = {d["binding"]["device"]: d for d in cls.inputs if d["binding"]["group"] == "pinmame.input.switch"}
		cls.dips = {d["binding"]["device"]: d for d in cls.inputs if d["binding"]["group"] == "pinmame.input.dip"}
		cls.solenoids = {d["binding"]["device"]: d for d in cls.outputs if d["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {d["binding"]["device"]: d for d in cls.outputs if d["binding"]["group"] == "pinmame.output.lamp"}
		cls.sources = {s["id"]: s for s in cls.definition["sources"]}

	def placement(self, device: dict, index: int = 0) -> tuple[float, float]:
		item = device["spatial"]["placements"][index]
		return item["x"], item["y"]

	# ------------------------------------------------------------- identity --
	def test_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, "Frontier", "Bally", 1980, 959, "GRwjq-MJwrd"), (machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["opdb_id"]))
		self.assertEqual({"width": 952.0, "height": 1974.0}, {k: machine["playfield"][k] for k in ("width", "height")})
		self.assertEqual("pinmame.by35", self.definition["controller"]["platform"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_three_drivers_one_machine(self) -> None:
		drivers = {d["id"]: d for d in self.definition["drivers"]}
		self.assertEqual({"frontier", "frontiea", "frontieg"}, set(drivers))
		for driver in drivers.values():
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertNotIn("display_overrides", driver)
		self.assertEqual("frontier", drivers["frontiea"]["clone_of"])
		self.assertEqual("frontier", drivers["frontieg"]["clone_of"])
		self.assertEqual(["frontier", "frontiea"], self.summary["driver_ids"])
		catalog = load(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({"frontier", "frontiea", "frontieg"}, {d["id"] for d in catalog["drivers"] if d["machine_id"] == MACHINE_ID})

	def test_coverage_is_honestly_partial(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["input_semantics", "spatial_placement"], coverage["missing"])
		self.assertEqual("candidate", coverage["dimensions"]["semantic_naming"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertIn("**partial**", KNOWLEDGE_PATH.read_text(encoding="utf-8"))
		catalog = load(ROOT / "catalog" / "pinmame.json")
		record = next(m for m in catalog["machines"] if m["id"] == MACHINE_ID)
		self.assertEqual((88, ["input_semantics", "spatial_placement"]), (record["completion_score"], record["missing"]))

	def test_every_source_records_when_it_was_acquired(self) -> None:
		self.assertEqual(ACQUIRED_AT, {source_id: source.get("acquired_at") for source_id, source in self.sources.items()})
		for value in ACQUIRED_AT.values():
			self.assertRegex(value, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

	# ----------------------------------------------------------- solenoids --
	def test_printed_test_numbers_are_paired_by_the_rom(self) -> None:
		observed = self.summary["runtime"]["observations"]["physical_service_solenoid_to_public"]
		self.assertEqual({str(t): p for t, (p, _) in TEST_TO_PUBLIC.items()}, observed)
		for test, (public, device_id) in TEST_TO_PUBLIC.items():
			device = self.solenoids[public]
			self.assertEqual(device_id, device["id"], public)
			self.assertIn({"namespace": "manual.self-test", "value": str(test)}, device["aliases"], public)

	def test_unused_and_missing_solenoid_addresses(self) -> None:
		self.assertEqual({1, 2, 3, 4, 5, 20}, {a for a, d in self.solenoids.items() if d["availability"] == "unused"})
		self.assertNotIn(16, self.solenoids)
		self.assertIn("power-on pulse", self.solenoids[20]["physical"]["notes"])
		seen = set(self.summary["runtime"]["observations"]["solenoid_addresses_seen"])
		self.assertEqual(set(), seen & {1, 2, 3, 4, 5})
		self.assertEqual(set(range(6, 16)) | set(range(17, 21)) | {45, 46, 47, 48}, seen)
		self.assertEqual(set(range(1, 16)) | set(range(17, 21)) | {45, 46, 47, 48}, set(self.solenoids))
		# Every address the BY35 profile allows for solenoids has a record.
		profile = load(ROOT / "controllers" / "pinmame" / "by35.json")
		group = next(g for g in profile["groups"] if g["id"] == "pinmame.output.solenoid")
		allowed = set()
		for rule in group["address_rules"]:
			allowed |= set(rule["values"]) if "values" in rule else set(range(rule["minimum"], rule["maximum"] + 1))
		self.assertEqual(allowed, set(self.solenoids))

	def test_gameplay_closures_fire_their_own_coils(self) -> None:
		notes = self.summary["runtime"]["observations"]["runs"]["gameplay-frontier"]["note"]
		self.assertIn("thumper bumpers 40, 39 and 38 fired 11, 12 and 13", notes)
		self.assertIn("slingshots 37 and 36 fired 14 and 15", notes)
		relationships = {(r["source"], r["destination"]): r["kind"] for r in self.definition["relationships"]}
		for switch, coil in SWITCH_TO_COIL.items():
			self.assertIn((self.switches[switch]["id"], self.solenoids[coil]["id"]), relationships, switch)
		for address, button in ((46, 82), (48, 84)):
			self.assertEqual("relay_gated", relationships[(self.switches[button]["id"], self.solenoids[address]["id"])])

	def test_gate_is_a_continuous_output_closed_by_the_saucer_rollover(self) -> None:
		gate = self.solenoids[17]
		self.assertEqual("device.gate", gate["id"])
		self.assertIn("continuous output", gate["physical"]["notes"])
		notes = self.summary["runtime"]["observations"]["runs"]
		self.assertIn("the saucer rollover (25) dropped 17 once the gate was open", notes["gameplay-frontier"]["note"])
		self.assertIn("adding a second player with the credit button left 17 raised", notes["gate-frontier"]["note"])
		self.assertEqual((self.seed["objects"]["Gate2"]["x"], self.seed["objects"]["Gate2"]["y"]), self.placement(gate))

	def test_flippers(self) -> None:
		for address, side, button in ((46, "right", 82), (48, "left", 84)):
			device = self.solenoids[address]
			self.assertEqual(f"device.{side}-flipper", device["id"])
			self.assertEqual("AQ-25-500/34-4500", device["physical"]["part_number"])
			self.assertEqual(1, len(device["spatial"]["placements"]))
			self.assertEqual("used", self.switches[button]["availability"])
		for address, side, bit, library in ((81, "right", "CORE_SWLRFLIPEOSBIT", "swURFlip"), (83, "left", "CORE_SWLLFLIPEOSBIT", "swULFlip")):
			device = self.switches[address]
			self.assertEqual("unused", device["availability"])
			# core.h: column 11 bits 0 and 2 are the lower flippers' end-of-stroke positions, not upper buttons.
			self.assertEqual((f"switch.lower-{side}-flipper-end-of-stroke-position", f"Lower-{side} flipper end-of-stroke position"), (device["id"], device["label"]))
			self.assertIn(f"column 11, bit {address - 81}", device["physical"]["notes"])
			self.assertIn(bit, device["physical"]["notes"])
			self.assertIn(library, device["physical"]["notes"])
			self.assertIn("embedded script lacks those calls", device["physical"]["notes"])
		self.assertIn("dropped 19, 45 and 46", self.summary["runtime"]["observations"]["runs"]["tilt-frontier"]["note"])

	def test_synthetic_flipper_states_45_and_47_are_used_virtual_duplicates(self) -> None:
		observations = {item["label"]: item for item in self.summary["runtime"]["observations"]["named_action_observations"]}
		for address, pair, side, button in ((45, 46, "right", 82), (47, 48, "left", 84)):
			device = self.solenoids[address]
			self.assertEqual((f"output.{side}-flipper-power-state", "virtual", "used"), (device["id"], device["kind"], device["availability"]))
			self.assertEqual({"status": "not_applicable", "reason": "virtual"}, {k: device["spatial"][k] for k in ("status", "reason")})
			self.assertEqual({"pinmame.core.46e1a01a0f73", "controller-profile.pinmame-by35", "runtime.frontier.harness"}, set(device["provenance"]["source_refs"]))
			self.assertIn(f"pair {address}/{pair}", device["physical"]["notes"])
			self.assertNotIn("does not declare", self.solenoids[pair]["physical"]["notes"])
			held = observations[f"gameplay: {side} flipper button (public {button}) held"]
			self.assertEqual([address, pair], held["transitioned_solenoid_addresses"])
			self.assertTrue({address, pair} <= set(held["active_solenoid_addresses"]))
			released = observations[f"gameplay: {side} flipper button (public {button}) released"]
			self.assertEqual([address, pair], released["transitioned_solenoid_addresses"])
			self.assertEqual(set(), {address, pair} & set(released["active_solenoid_addresses"]))
		self.assertEqual([19, 45, 46], observations["tilt: tilt (public 7)"]["transitioned_solenoid_addresses"])
		self.assertNotIn("left out of the observations", self.summary["source"]["attribution"])

	# ------------------------------------------------------------ switches --
	def test_switch_inventory(self) -> None:
		self.assertEqual(set(range(-7, -4)) | set(range(1, 49)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(UNUSED_SWITCHES | {81, 83, 85, 86, 87, 88}, {a for a, d in self.switches.items() if d["availability"] == "unused"})
		for address, bit in ((85, "CORE_SWURFLIPEOSBIT"), (86, "CORE_SWURFLIPBUTBIT"), (87, "CORE_SWULFLIPEOSBIT"), (88, "CORE_SWULFLIPBUTBIT")):
			device = self.switches[address]
			self.assertIn(f"column 11, bit {address - 81}", device["physical"]["notes"])
			self.assertIn(bit, device["physical"]["notes"])
			self.assertIn("81-88", device["physical"]["notes"])
			self.assertEqual("unused", device["spatial"]["reason"])
		# Every address the BY35 profile allows for switches has a record.
		profile = load(ROOT / "controllers" / "pinmame" / "by35.json")
		group = next(g for g in profile["groups"] if g["id"] == "pinmame.input.switch")
		allowed = set()
		for rule in group["address_rules"]:
			allowed |= set(range(rule["minimum"], rule["maximum"] + 1))
		self.assertEqual(allowed, set(self.switches))
		for address, device in self.switches.items():
			if device["availability"] == "used":
				self.assertIs(False, device["normally_closed"], address)

	def test_option_switches_and_the_three_undocumented_ones(self) -> None:
		self.assertEqual(set(range(1, 33)), set(self.dips))
		self.assertEqual(UNDOCUMENTED_DIPS, {a for a, d in self.dips.items() if d["availability"] == "unknown"})
		self.assertEqual(set(range(1, 33)) - UNDOCUMENTED_DIPS, {a for a, d in self.dips.items() if d["availability"] == "used"})
		for address in UNDOCUMENTED_DIPS:
			self.assertEqual(f"Undocumented option switch S{address}", self.dips[address]["label"])
		self.assertIn("default it on", self.dips[21]["physical"]["notes"])
		self.assertIn("default it off", self.dips[22]["physical"]["notes"])
		self.assertIn("free play", self.dips[25]["physical"]["notes"])

	def test_option_form_disagreements_are_table_defects(self) -> None:
		form = (ROOT / "evidence" / "excerpts" / MACHINE_ID / "vpx-script.md").read_text(encoding="utf-8")
		manual = (ROOT / "evidence" / "excerpts" / MACHINE_ID / "manual-game-adjustments.md").read_text(encoding="utf-8")
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn('Array("3X lights", 0, "4X lights", &H00002000)', form)
		self.assertIn("| | Conservative | SW. 14 OFF | Special lites come on when side drop target special is on. |", manual)
		self.assertIn("| Special outlane lites and side targets adjustment | Liberal | SW. 14 ON | Special lites come on when side drop target 4X is on. |", manual)
		for text in (form, knowledge, self.dips[14]["physical"]["notes"]):
			self.assertIn('"3X lights"', text)
			self.assertIn("SW. 14 OFF", text)
			self.assertNotIn("same meanings", text)
		self.assertIn("defect in the table", self.dips[14]["physical"]["notes"])
		self.assertIn("runtime.frontier.harness", self.dips[14]["provenance"]["source_refs"])
		self.assertIn("Feeder Lane Special lights", self.dips[30]["physical"]["notes"])
		self.assertEqual([], self.definition["conflicts"])
		# The ROM run (S14 off) lit the outlane special on the third completion, with the drop-target special.
		note = self.summary["runtime"]["observations"]["runs"]["gameplay-frontier"]["note"]
		self.assertIn("right bank, 1st completion: public 35 top side drop target down: fired [9], lamps on [30, 31], off [14]", note)
		self.assertIn("right bank, 3rd completion: public 35 top side drop target down: fired [9], lamps on [60, 62, 63], off [46, 47]", note)
		self.assertIn("S20 and S21 on, every other switch off", self.summary["runtime"]["command_template"])

	def test_parallel_contacts(self) -> None:
		for address, quantity in {1: 4, 7: 3, 16: 2}.items():
			self.assertEqual(quantity, self.switches[address]["physical"]["quantity"], address)
		self.assertEqual(4, len(self.switches[1]["spatial"]["placements"]))
		objects = self.seed["objects"]
		self.assertEqual([(objects[f"sw1a{n}"]["x"], objects[f"sw1a{n}"]["y"]) for n in range(1, 5)], [self.placement(self.switches[1], i) for i in range(4)])

	def test_switch_test_showed_every_address(self) -> None:
		note = self.summary["runtime"]["observations"]["runs"]["switch-test-frontier"]["note"]
		self.assertIn("public 1 to 40", note)

	def test_library_defaults_are_not_taken_as_names(self) -> None:
		self.assertEqual("switch.right-outlane", self.switches[2]["id"])
		self.assertEqual("switch.coin-i-left", self.switches[10]["id"])
		self.assertEqual("switch.coin-ii-middle", self.switches[11]["id"])
		self.assertEqual("switch.coin-iii-right", self.switches[9]["id"])

	def test_matrix_wiring_follows_the_plug_connector_sheet(self) -> None:
		self.assertEqual({"control_connection": "A4J2-1", "control_wire": "51", "return_connection": "A4J2-9", "return_wire": "63"}, {k: self.switches[2]["wiring"][k] for k in ("control_connection", "control_wire", "return_connection", "return_wire")})
		self.assertIn("prints 56", self.switches[2]["physical"]["notes"])
		self.assertEqual(("A4J3-3", "A4J3-9"), (self.switches[9]["wiring"]["control_connection"], self.switches[9]["wiring"]["return_connection"]))
		self.assertEqual(("A4J2-5", "A4J2-15"), (self.switches[40]["wiring"]["control_connection"], self.switches[40]["wiring"]["return_connection"]))

	# ---------------------------------------------------------------- lamps --
	def test_sixty_lamps_all_used(self) -> None:
		self.assertEqual(LAMP_ADDRESSES, sorted(self.lamps))
		self.assertTrue(all(d["availability"] == "used" for d in self.lamps.values()))
		self.assertEqual(LAMP_ADDRESSES, self.summary["runtime"]["observations"]["lamp_addresses_seen"])

	def test_backbox_lamps(self) -> None:
		backbox = {a for a, d in self.lamps.items() if "spatial" in d}
		self.assertEqual(set(BACKBOX_LAMPS), backbox)
		for address, label in BACKBOX_LAMPS.items():
			self.assertEqual(label, self.lamps[address]["label"])
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"])
		self.assertEqual("Same player shoots again", self.lamps[43]["label"])
		self.assertEqual("playfield", self.lamps[43]["physical"]["location"])

	def test_table_b_pins_are_the_j2_playfield_lamps(self) -> None:
		j2 = {d["wiring"]["drive_connection"]: a for a, d in self.lamps.items() if d["wiring"]["drive_connection"].startswith("A5J2-") and a not in BACKBOX_LAMPS}
		self.assertEqual(TABLE_B, j2)
		self.assertEqual("35", self.lamps[30]["wiring"]["drive_wire"])
		self.assertIn("20K BONUS", self.lamps[30]["physical"]["notes"])
		self.assertIn("print 98", self.lamps[30]["physical"]["notes"])
		sheet = (ROOT / "evidence" / "excerpts" / MACHINE_ID / "schematic-plug-connectors.md").read_text(encoding="utf-8")
		self.assertIn("| A5J2-20 | 5 | 35 |", sheet)
		self.assertIn("| 20 | 98 | 3X DROP TARGET |", sheet)
		self.assertIn("| 98 | A5J2-20 | (none) |", sheet)
		self.assertIn("| 35 | A5J2-20 | 20K BONUS |", (ROOT / "evidence" / "excerpts" / MACHINE_ID / "schematic-switch-matrix.md").read_text(encoding="utf-8"))

	def test_rom_confirms_the_lamp_chain_where_play_reaches_it(self) -> None:
		note = self.summary["runtime"]["observations"]["runs"]["gameplay-frontier"]["note"]
		self.assertIn("stepped the lamps 14 -> 30/31 -> 46/47 -> 60/62/63", note)
		self.assertIn("The first in-line target (23) raised the gate output 17 and lit 15 and 40", note)

	# --------------------------------------------------------------- spatial --
	def test_no_lamp_is_placed_because_no_table_light_marks_a_bulb(self) -> None:
		playfield = sorted(d["id"] for a, d in self.lamps.items() if a not in BACKBOX_LAMPS)
		self.assertEqual(54, len(playfield))
		self.assertTrue(all("spatial" not in self.lamps[a] for a in self.lamps if a not in BACKBOX_LAMPS))
		lights = self.seed["lamp_lights"]
		self.assertEqual([], [name for name, item in lights.items() if item["show_bulb_mesh"]])
		self.assertEqual({"L10", "L26", "L42"}, {name for name, item in lights.items() if item["is_bulb_light"]})
		for name, bulb in self.seed["bulb_meshes"].items():
			self.assertIsNone(re.fullmatch(r"L\d+", bulb["nearest_light"]), name)
		report = load(REPORT_JSON)
		self.assertEqual(playfield, sorted(report["unplaced_physical_devices"]))
		self.assertEqual({"light": "L9", "distance": 64.6}, report["lamp_bulb_audit"]["nearest_lamp_light_to_any_bulb_primitive"])

	def test_placements_match_the_frozen_table_objects(self) -> None:
		objects = self.seed["objects"]
		for name, address in (("sw38", 38), ("sw39", 39), ("sw40", 40), ("Drain", 8), ("sw12", 12), ("sw33", 33), ("sw25", 25), ("RightSlingShot", 36)):
			self.assertEqual((objects[name]["x"], objects[name]["y"]), self.placement(self.switches[address]), address)
		for name, address in (("Drain", 7), ("sw12", 10), ("sw34", 9), ("LeftFlipper", 48), ("RightFlipper", 46)):
			self.assertEqual((objects[name]["x"], objects[name]["y"]), self.placement(self.solenoids[address]), address)
		mean = tuple(round(sum(objects[n][k] for n in ("sw21", "sw22", "sw23")) / 3, 6) for k in ("raw_x", "raw_y"))
		x, y = self.placement(self.solenoids[8])
		self.assertAlmostEqual(mean[0] / self.seed["bounds"]["right"], x, places=5)
		self.assertAlmostEqual(mean[1] / self.seed["bounds"]["bottom"], y, places=5)
		for name, item in objects.items():
			self.assertAlmostEqual(item["raw_x"] / self.seed["bounds"]["right"], item["x"], places=5, msg=name)
			self.assertAlmostEqual(item["raw_y"] / self.seed["bounds"]["bottom"], item["y"], places=5, msg=name)
		statuses = {p["provenance"]["status"] for d in self.inputs + self.outputs for p in (d.get("spatial") or {}).get("placements", [])}
		self.assertEqual({"observed"}, statuses)

	def test_spatial_report_matches_the_definition(self) -> None:
		report = load(REPORT_JSON)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(file_digest(DEFINITION_PATH), report["definition_sha256"])
		self.assertEqual(file_digest(SPATIAL_SEED), report["source_hashes"]["spatial_seed_sha256"])
		ids = {d["id"] for d in self.inputs + self.outputs}
		for disclosure in report["projection_disclosures"]:
			self.assertTrue(set(disclosure["devices"]) <= ids, disclosure["devices"])
		self.assertEqual(42, len(report["unvalidated_placements"]))

	# ----------------------------------------------------------- determinism --
	def test_curator_reproduces_the_artifacts(self) -> None:
		result = subprocess.run([sys.executable, "-B", str(CURATOR), "--check"], capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, result.returncode, result.stderr)

	def test_curator_detects_drift_in_an_isolated_copy(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			copies = {name: base / name for name in ("definition.json", "knowledge.md", "report.json", "report.md")}
			for name, source in zip(copies, (DEFINITION_PATH, KNOWLEDGE_PATH, REPORT_JSON, REPORT_MD)):
				copies[name].write_bytes(source.read_bytes())
			command = [
				sys.executable, "-B", str(CURATOR), "--check",
				"--definition", str(copies["definition.json"]), "--knowledge", str(copies["knowledge.md"]),
				"--report-json", str(copies["report.json"]), "--report-md", str(copies["report.md"]),
			]
			untouched = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertEqual(0, untouched.returncode, untouched.stderr)
			copies["definition.json"].write_bytes(copies["definition.json"].read_bytes().replace(b'"Frontier"', b'"Frontiers"', 1))
			tampered = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertNotEqual(0, tampered.returncode)
			self.assertIn("canonical content mismatch", tampered.stderr)

	def regenerate_in_isolation(self, base: Path, arguments: list[str]) -> tuple[int, str]:
		"""Run the curator's --regenerate in-process with every path it could write or remove under base.

		Path's writers are mocks as well, so a broken guard fails this test instead of touching any
		tree; the caller asserts that nothing appeared under base either.
		"""
		import curate_frontier

		author_ready = base / "machines" / "author-ready"
		paths = {
			"PARTIAL_PATH": base / "machines" / "partial" / "bally" / "frontier-1980.json",
			"AUTHOR_READY_DIR": author_ready,
			"AUTHOR_READY_PATH": author_ready / "bally" / "frontier-1980.json",
			"KNOWLEDGE_PATH": base / "knowledge.md",
			"REPORT_JSON_PATH": base / "report.json",
			"REPORT_MD_PATH": base / "report.md",
		}
		stderr = io.StringIO()
		with ExitStack() as stack:
			for name, value in paths.items():
				stack.enter_context(mock.patch.object(curate_frontier, name, value))
			writers = [stack.enter_context(mock.patch.object(Path, name, autospec=True)) for name in ("write_bytes", "write_text", "unlink", "mkdir")]
			stack.enter_context(mock.patch.object(sys, "argv", ["curate_frontier.py", "--regenerate", *arguments]))
			stack.enter_context(redirect_stderr(stderr))
			status = curate_frontier.main()
		self.assertEqual({"write_bytes": 0, "write_text": 0, "unlink": 0, "mkdir": 0}, {name: writer.call_count for name, writer in zip(("write_bytes", "write_text", "unlink", "mkdir"), writers)})
		return status, stderr.getvalue()

	def test_regenerate_refuses_to_remove_an_author_ready_definition(self) -> None:
		import curate_frontier

		self.assertEqual(ROOT / "machines" / "author-ready", curate_frontier.AUTHOR_READY_DIR)
		self.assertEqual(AUTHOR_READY_PATH, curate_frontier.AUTHOR_READY_PATH)
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			promoted = base / "machines" / "author-ready" / "bally" / "frontier-1980.json"
			promoted.parent.mkdir(parents=True)
			promoted.write_bytes(b"{}\n")
			status, message = self.regenerate_in_isolation(base, [])
			self.assertEqual(1, status)
			self.assertIn("builds a partial record, which would remove the existing author-ready definition", message)
			self.assertEqual(b"{}\n", promoted.read_bytes())
			self.assertEqual([promoted], [path for path in base.rglob("*") if path.is_file()])

	def test_regenerate_refuses_a_definition_path_in_the_author_ready_tree(self) -> None:
		import curate_frontier

		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			inside = base / "machines" / "author-ready" / "bally" / "copy.json"
			status, message = self.regenerate_in_isolation(base, ["--definition", str(inside)])
			self.assertEqual(1, status)
			self.assertIn("points into", message)
			self.assertEqual([], list(base.rglob("*")))
			# The guard is not a blanket refusal: a copy outside that tree, with no promoted file, is allowed.
			with mock.patch.object(curate_frontier, "AUTHOR_READY_DIR", base / "machines" / "author-ready"), mock.patch.object(curate_frontier, "AUTHOR_READY_PATH", base / "machines" / "author-ready" / "bally" / "frontier-1980.json"):
				self.assertIsNone(curate_frontier.regenerate_refusal("partial", base / "copy.json", True))
				self.assertIsNotNone(curate_frontier.regenerate_refusal("partial", inside, True))

	def test_extraction_commands_fail_closed_without_their_root(self) -> None:
		environment = {k: v for k, v in os.environ.items() if k != "PINMAME_VPX_SOURCES_ROOT"}
		result = subprocess.run([sys.executable, "-B", str(CURATOR), "--verify-extraction"], capture_output=True, text=True, encoding="utf-8", env=environment)
		self.assertNotEqual(0, result.returncode)
		self.assertIn("PINMAME_VPX_SOURCES_ROOT", result.stderr)

	def test_excerpts_are_attached_to_their_bytes(self) -> None:
		count = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				count += 1
				self.assertEqual(excerpt["sha256"], file_digest(ROOT / excerpt["path"]), excerpt["id"])
				self.assertTrue(excerpt["path"].startswith("evidence/excerpts/bally.frontier.1980/"), excerpt["id"])
				self.assertTrue(excerpt["transcribed_by"].startswith("curator"), excerpt["id"])
				self.assertIn(excerpt["method"], {"manual", "mixed"}, excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], file_digest(ROOT / excerpt["image"]), excerpt["id"])
					self.assertLess((ROOT / excerpt["image"]).stat().st_size, 100_000, excerpt["id"])
		self.assertEqual(13, count)

	def test_scenarios_are_lf_and_match_the_summary(self) -> None:
		self.assertEqual(4, len(SCENARIOS))
		for path in SCENARIOS:
			self.assertNotIn(b"\r", path.read_bytes(), path.name)
		digests = {run["scenario_path"]: run["scenario_sha256"] for run in self.summary["runtime"]["raw_runs"] if "scenario_path" in run}
		self.assertEqual({f"tools/harness-scenarios/by35/{p.name}" for p in SCENARIOS}, set(digests))
		for relative, digest in digests.items():
			self.assertEqual(digest, file_digest(ROOT / relative), relative)

	def test_pinned_readings_refuse_a_substituted_frame(self) -> None:
		readings = load(READINGS_SEED)
		cited = copy.deepcopy(readings["frames"])
		frontier_runtime_summary.check_frames(cited, readings)
		# A frame with the same reading but different segment words is refused.
		same_reading = copy.deepcopy(cited)
		same_reading[0]["segments"] = same_reading[0]["segments"][:-1] + [same_reading[0]["segments"][-1] | 0x80]
		same_reading[0]["segments_sha256"] = frontier_runtime_summary.segments_sha256(same_reading[0]["segments"])
		self.assertEqual(cited[0]["reading"], frontier_runtime_summary.decode(same_reading[0]["segments"]).strip())
		with self.assertRaises(SystemExit):
			frontier_runtime_summary.check_frames(same_reading, readings)
		# A different, self-consistent frame in place of a pinned one: 02 shown where 01 was read.
		substituted = copy.deepcopy(cited)
		segments = list(substituted[0]["segments"])
		segments[-1] = 0x5B
		substituted[0].update(segments=segments, segments_sha256=frontier_runtime_summary.segments_sha256(segments), reading=frontier_runtime_summary.decode(segments).strip())
		with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as refused:
			frontier_runtime_summary.check_frames(substituted, readings)
		self.assertIn("differs from the pinned frame", str(refused.exception))
		# A pin whose reading does not decode from its own segment words.
		tampered = copy.deepcopy(readings)
		tampered["frames"][0]["reading"] = "07"
		with self.assertRaises(SystemExit) as inconsistent:
			frontier_runtime_summary.check_frames(cited, tampered)
		self.assertIn("not self-consistent", str(inconsistent.exception))
		with self.assertRaises(SystemExit):
			frontier_runtime_summary.check_frames(cited[:-1], readings)

	def test_no_other_bally_machine_id_appears(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign_machines = {m["id"] for m in catalog["machines"] if m["id"] != MACHINE_ID}
		text = json.dumps(self.definition) + KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertEqual([], [m for m in foreign_machines if m in text])

	# ------------------------------------------------- retained evidence roots --
	def test_runtime_summary_is_reproduced_from_the_retained_runs(self) -> None:
		root = configured("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		runs = root / "frontier-1980" / "harness"
		for run in self.summary["runtime"]["raw_runs"]:
			relative = run["retained_from"].split("/harness/", 1)[1]
			self.assertEqual(run["sha256"], file_digest(runs / relative), run["name"])
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "frontier_runtime_summary.py"), "--runs", str(runs), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(self.summary["source"]["sha256"], check_manifest(runs, "frontier"))
		self.assertEqual(self.sources["runtime.frontier.harness"]["sha256"], file_digest(SUMMARY_PATH))

	def test_a_substituted_display_frame_in_a_retained_run_is_refused(self) -> None:
		root = configured("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		runs = root / "frontier-1980" / "harness"
		readings = load(READINGS_SEED)
		loaded = {name: frontier_runtime_summary.load_run(runs, name) for name in frontier_runtime_summary.RUNS}
		first = readings["frames"][0]
		self.assertEqual(("solenoid-test-frontier", "display_event"), (first["run"], first["source"]))
		events = [e for e in loaded["solenoid-test-frontier"]["events"] if e["event"] == "display" and e["index"] == 0 and f"{e['time_s']:.6f}" == first["key"]]
		self.assertEqual(1, len(events))
		self.assertEqual(first["segments"], events[0]["segments"])
		# Same reading (the decimal-point bit is not part of a digit), different segment words.
		events[0]["segments"] = events[0]["segments"][:-1] + [events[0]["segments"][-1] | 0x80]
		self.assertEqual(first["reading"], frontier_runtime_summary.decode(events[0]["segments"]).strip())
		with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as refused:
			frontier_runtime_summary.build(runs, frontier_runtime_summary.ROM_ARCHIVES, readings, loaded=loaded)
		self.assertIn("differs from the pinned frame", str(refused.exception))

	def test_table_geometry_is_reproduced_from_the_retained_extraction(self) -> None:
		root = configured("PINMAME_VPX_SOURCES_ROOT")
		if root is None:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		base = root / "bally" / "frontier-1980"
		vpx = base / "source" / "Frontier (Bally 1980).vpx"
		self.assertEqual(self.seed["table_sha256"], file_digest(vpx))
		self.assertEqual(self.sources["vpx-table.frontier.2-0"]["sha256"], file_digest(vpx))
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "frontier_spatial_seed.py"), "--extracted", str(base / "extracted-vpxtool"), "--vpx", str(vpx), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		verified = subprocess.run([sys.executable, "-B", str(CURATOR), "--verify-extraction"], capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, verified.returncode, verified.stderr)
		self.assertIn(self.seed["extraction_manifest_sha256"], verified.stdout)
		self.assertEqual("570e36792ab44bb4e9baf1245e5f5be49036ea1595d72802fe83c79aff9cce17", file_digest(base / "source" / "Frontier (Bally 1980).directb2s"))
		self.assertEqual("bb0e1773227f75632558b8c42431e1b87d92cf5c38255d8df3179a1aa959b769", file_digest(base / "extracted-vpxtool" / "script.vbs"))
		for name, digest in {"Bally.vbs": "d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c", "core.vbs": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"}.items():
			self.assertEqual(digest, file_digest(base / "library" / name), name)
		self.assertEqual(self.sources["vpinmame-library.bally-vbs"]["sha256"], file_digest(base / "library" / "Bally.vbs"))
		for number in (1, 2, 3):
			light = next(iter(load(base / "extracted-vpxtool" / "gameitems" / f"Light.BumperLight{number}.json").values()))
			self.assertEqual((True, False), (light["is_bulb_light"], light["show_bulb_mesh"]), number)

	def test_manuals_are_reachable_when_configured(self) -> None:
		root = configured("PINMAME_MANUALS_ROOT")
		if root is None:
			self.skipTest("PINMAME_MANUALS_ROOT is not configured")
		base = root / "by-machine" / MACHINE_ID
		for source_id, name in (
			("manual.bally.frontier.1980", "Bally_1980_Frontier_Manual.pdf"),
			("schematic.bally.frontier.1980", "Bally_1980_Frontier_Schematic_Diagrams_paginated.pdf"),
			("ipdb.959", "ipdb959.html"),
		):
			self.assertEqual(self.sources[source_id]["sha256"], file_digest(base / name), name)

	def test_rom_archives_and_the_static_variant_readings(self) -> None:
		root = configured("PINMAME_ROM_LIBRARY_ROOT")
		if root is None:
			self.skipTest("PINMAME_ROM_LIBRARY_ROOT is not configured")
		for driver, digest in ROM_ARCHIVES.items():
			self.assertEqual(digest, file_digest(root / f"{driver}.zip"), driver)
		self.assertEqual(ROM_ARCHIVES, frontier_runtime_summary.ROM_ARCHIVES)
		self.assertEqual(ROM_ARCHIVES["frontier"], self.summary["runtime"]["rom_archive_sha256"])
		with zipfile.ZipFile(root / "frontier.zip") as archive:
			u6 = bytearray(archive.read("720-40_6.732"))
		# The rec.games.pinball patch PinMAME quotes for frontieg, applied to the production U6.
		self.assertEqual((0xAB, bytes.fromhex("FE5090AD00")), (u6[0], bytes(u6[0x289:0x28E])))
		self.assertEqual(bytes.fromhex("439A92979239"), bytes(u6[0xEEB:0xEF1]))
		u6[0] = 0xBB
		u6[0x289:0x28E] = bytes.fromhex("86EFBD5EEB")
		self.assertEqual(FRONTIEG_U6_SHA1, hashlib.sha1(u6).hexdigest())
		with zipfile.ZipFile(root / "frontiea.zip") as archive:
			info = " ".join(archive.read("info.txt").decode("latin-1").split())
		for text in ("1 031004 add free play", "if dip switch 25 = on and dip switch 26 = on freeplay is enable: decrease credits not lower then 01", "FRONTIER FRNT2732.U2"):
			self.assertIn(text, info)


if __name__ == "__main__":
	unittest.main()
