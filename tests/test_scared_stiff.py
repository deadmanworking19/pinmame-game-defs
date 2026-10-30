from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "bally" / "scared-stiff-1996.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "bally" / "scared-stiff-1996.json"
PROTOTYPE_PATH = ROOT / "machines" / "partial" / "bally" / "scared-stiff-d01r-prototype-1996.json"
PROTOTYPE_KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "scared-stiff-d01r-prototype-1996.md"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "scared-stiff-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "scared-stiff-1996.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "scared-stiff-1996.json"

DRIVER_IDS = {"ss_15", "ss_14", "ss_12", "ss_11", "ss_11s10", "ss_03"}
PROTOTYPE_DRIVER_IDS = {"ss_01", "ss_01b"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 15, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {12, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48}
AUX_LAMP_ADDRESSES = {91, 92, 93, 94, 95, 96, 97, 98, 101, 102, 103, 104, 105, 106, 107, 108}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


def _run_curator_without_mode() -> None:
	"""Invoke the curator's CLI with no mode so argparse rejects it instead of writing files."""
	import curate_scared_stiff as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_scared_stiff.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class ScaredStiffDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_author_ready_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertFalse(PARTIAL_PATH.exists())
		self.assertEqual("bally.scared-stiff.1996", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1996, self.definition["machine"]["year"])
		self.assertEqual("Bally", self.definition["machine"]["manufacturer"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertEqual(952.941, self.definition["machine"]["playfield"]["width"])
		self.assertEqual(2164.706, self.definition["machine"]["playfield"]["height"])
		self.assertEqual("vpx", self.definition["machine"]["playfield"]["units"])

	def test_the_skull_driver_board_is_recorded_unused_from_the_manufacturer_notes(self) -> None:
		# The 16-LED Skull Driver PCB was removed before production (Midway's development notes),
		# so its sixteen lamp outputs, its clock/data lines and their LPDC mirrors are unused.
		for address in AUX_LAMP_ADDRESSES:
			lamp = self.lamps[address]
			self.assertEqual("unused", lamp["availability"], address)
			self.assertEqual("not_applicable", lamp["spatial"]["status"], address)
			self.assertEqual("unused", lamp["spatial"]["reason"], address)
			self.assertTrue(lamp["label"].startswith("Not Fitted Skull Driver"), address)
			self.assertIn("manufacturer-notes.bally.scared-stiff.1996", lamp["provenance"]["source_refs"], address)
			self.assertIn("runtime.scared-stiff.aux-lamp-probe", lamp["provenance"]["source_refs"], address)
			self.assertNotIn("A-21287", lamp["physical"]["notes"], address)
			self.assertIn("A-20781", lamp["physical"]["notes"], address)
		for address in (37, 38):
			line = self.solenoids[address]
			self.assertEqual("unused", line["availability"], address)
			self.assertEqual("unused", line["spatial"]["reason"], address)
			self.assertNotIn("part_number", line["physical"], address)
			self.assertIn("manufacturer-notes.bally.scared-stiff.1996", line["provenance"]["source_refs"], address)
		for address in (41, 42):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_knowledge_note_exists(self) -> None:
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_ss_driver_is_claimed_exactly_once_and_is_physically_identical(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for clone_id in ("ss_14", "ss_12", "ss_11", "ss_11s10", "ss_03"):
			self.assertEqual("ss_15", by_id[clone_id]["clone_of"], clone_id)
		self.assertNotIn("clone_of", by_id["ss_15"])

	def test_the_full_wpc95_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertIn(self.switches[address]["availability"], {"used", "optional"}, address)

	def test_scared_stiff_has_no_unused_matrix_gap_that_monster_bash_does_not_share(self) -> None:
		# Scared Stiff's manual marks no "not fitted" solenoid/switch position inside 1-40 or
		# 11-88 beyond the printed Not Used set; this is a real difference from Monster Bash
		# (which has four such gaps) and must not be silently harmonized away.
		self.assertEqual(14, len(UNUSED_MATRIX_ADDRESSES))

	def test_printed_opto_polarity_matches_pinmame_with_zero_disagreement(self) -> None:
		import curate_scared_stiff as curator

		self.assertEqual(curator.OPTO_SWITCHES, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		self.assertEqual(OPTO_ADDRESSES, curator.OPTO_SWITCHES)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_inverted_switch_mask_decoding_produces_exactly_the_opto_set(self) -> None:
		# ssGameData's inverted-switch mask, indexed by column with bit = row-1.
		mask = (0x00, 0x02, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		normalized: set[int] = set()
		for column in range(1, 9):
			for row in range(1, 9):
				if mask[column] & (1 << (row - 1)):
					normalized.add(column * 10 + row)
		self.assertEqual(OPTO_ADDRESSES, normalized)

	def test_flipper_positions_scared_stiff_has_no_upper_flippers(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
			self.assertNotIn("wiring", self.switches[address])
		# WPC-95 reads the flipper column complemented and the ROM treats public 1 as pressed, so
		# the button contacts rest open whatever their opto construction.
		self.assertFalse(self.switches[112]["normally_closed"])
		self.assertFalse(self.switches[114]["normally_closed"])
		for address in (112, 114):
			self.assertIn("runtime.scared-stiff.flipper-button-polarity", self.switches[address]["provenance"]["source_refs"], address)
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])

	def test_the_full_wpc95_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 51))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES | AUX_LAMP_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in list(range(17, 29)) + [35, 36]:
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (39, 40):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (37, 38):
			self.assertEqual("control_signal", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		for address in AUX_LAMP_ADDRESSES:
			self.assertEqual("unused", self.lamps[address]["availability"], address)
			self.assertEqual("unused", self.lamps[address]["spatial"]["reason"], address)

	def test_solenoid_1_40_has_no_unfitted_gap_but_the_skull_driver_lines(self) -> None:
		for address in list(range(1, 29)) + [33, 34, 35, 36, 39, 40, 45, 46, 47, 48]:
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		for address in (37, 38):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_left_diverter_and_repurposed_flashers_have_no_translation(self) -> None:
		for address in (33, 34, 35, 36):
			manual_aliases = {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			self.assertEqual({f"{address:02d}"}, manual_aliases, address)
		self.assertEqual("Left Diverter Power", self.solenoids[33]["label"])
		self.assertEqual("Left Diverter Hold", self.solenoids[34]["label"])
		self.assertEqual("Lower Left Flasher", self.solenoids[35]["label"])
		self.assertEqual("Lower Right Flasher", self.solenoids[36]["label"])

	def test_lower_flipper_manual_address_mapping(self) -> None:
		manual_aliases = {
			address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			for address in (45, 46, 47, 48)
		}
		self.assertEqual({"45"}, manual_aliases[45])
		self.assertEqual({"46"}, manual_aliases[46])
		self.assertEqual({"47"}, manual_aliases[47])
		self.assertEqual({"48"}, manual_aliases[48])

	def test_lpdc_mirrors_are_virtual_and_reference_all_four_backbox_drive_lines(self) -> None:
		self.assertEqual("Aux Lamp Clock LPDC Mirror", self.solenoids[41]["label"])
		self.assertEqual("Aux Lamp Data LPDC Mirror", self.solenoids[42]["label"])
		self.assertEqual("Spider Wheel 1 LPDC Mirror", self.solenoids[43]["label"])
		self.assertEqual("Spider Wheel 2 LPDC Mirror", self.solenoids[44]["label"])
		for address in (41, 42, 43, 44):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("used" if address in {43, 44} else "unused", self.solenoids[address]["availability"], address)
			self.assertNotIn("wiring", self.solenoids[address], address)

	def test_no_solenoid_is_labelled_a_motorized_crate(self) -> None:
		for device in self.solenoids.values():
			label = device["label"].lower()
			self.assertNotIn("crate motor", label)
		crate_kickout = self.solenoids[6]
		self.assertEqual("Crate Kickout", crate_kickout["label"])
		self.assertEqual("coil", crate_kickout["kind"])
		spider_1 = self.solenoids[39]
		self.assertEqual("motor", spider_1["kind"])
		self.assertIn("Spider Wheel", spider_1["physical"]["notes"])

	def test_physical_solenoid_wiring_connections_are_unique(self) -> None:
		connections: dict[tuple[object, object], int] = {}
		for address, device in self.solenoids.items():
			if device["kind"] == "virtual" or device["availability"] != "used":
				continue
			wiring = device.get("wiring", {})
			connection = wiring.get("control_connection")
			if not connection:
				continue
			key = (wiring.get("board"), connection)
			self.assertNotIn(key, connections, f"{address} duplicates {connections.get(key)}")
			connections[key] = address
		self.assertEqual("J116-1", self.solenoids[1]["wiring"]["control_connection"])
		self.assertEqual("Q72", self.solenoids[1]["wiring"]["driver_transistor"])

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_cabinet(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(17, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(8, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(12, len(self.gi[2]["spatial"]["placements"]))
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_web_award_lamps_are_backbox_and_skull_lane_lamps_are_playfield(self) -> None:
		web_award = {64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83}
		self.assertEqual(16, len(web_award))
		for address in web_award:
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		for address in (84, 85, 86):
			self.assertEqual("validated", self.lamps[address]["spatial"]["status"], address)
		for address in (87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device.get("spatial")
			if spatial is None or spatial["status"] == "not_applicable":
				continue
			self.assertEqual("validated", spatial["status"], device["id"])
			for placement in spatial["placements"]:
				located += 1
				self.assertNotIn(placement["id"], seen)
				seen.add(placement["id"])
				self.assertEqual("playfield", placement["space"])
				for axis in ("x", "y"):
					self.assertGreaterEqual(placement[axis], 0.0)
					self.assertLessEqual(placement[axis], 1.0)
					self.assertLessEqual(len(str(placement[axis]).partition(".")[2]), 6)
				self.assertEqual("validated", placement["provenance"]["status"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("pinmame-spatial-audit", report["format"])
		self.assertEqual("validated", report["status"])
		self.assertEqual(located, report["placement_count"])
		self.assertEqual([], report["unresolved"])
		unused_lamps = {item["address"] for item in report["not_applicable_outputs"]["unused"] if item["group"] == "pinmame.output.lamp"}
		self.assertEqual(AUX_LAMP_ADDRESSES, unused_lamps)

	def test_trough_and_flippers_land_near_the_front_and_top_lanes_near_the_rear(self) -> None:
		# Sanity check demanded by the task brief: trough/flipper y near 1.0, top lanes near 0.0.
		for address in (32, 33, 34, 35):
			y = self.switches[address]["spatial"]["placements"][0]["y"]
			self.assertGreater(y, 0.85, address)
		for address in (45, 46, 47, 48):
			y = self.solenoids[address]["spatial"]["placements"][0]["y"]
			self.assertGreater(y, 0.8, address)
		for address in (71, 72, 73, 74):
			y = self.switches[address]["spatial"]["placements"][0]["y"]
			self.assertLess(y, 0.15, address)

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		lamp_pos = _positions(self.lamps)
		solenoid_pos = _positions(self.solenoids)
		# Top lanes/Skull Lanes ascend left -> center -> right for both switches and lamps.
		self.assertLess(switch_pos[71][0], switch_pos[72][0])
		self.assertLess(switch_pos[72][0], switch_pos[73][0])
		self.assertLess(lamp_pos[84][0], lamp_pos[85][0])
		self.assertLess(lamp_pos[85][0], lamp_pos[86][0])
		# Lamp position agrees with the switch the manual names for the same feature (Left/
		# Center/Right Skull Lane): within a few thousandths of normalized x.
		self.assertAlmostEqual(switch_pos[71][0], lamp_pos[84][0], delta=0.01)
		self.assertAlmostEqual(switch_pos[72][0], lamp_pos[85][0], delta=0.01)
		self.assertAlmostEqual(switch_pos[73][0], lamp_pos[86][0], delta=0.01)
		# Slingshots and flippers: left is left of right.
		self.assertLess(solenoid_pos[10][0], solenoid_pos[11][0])
		self.assertLess(solenoid_pos[47][0], solenoid_pos[45][0])
		# Coffin trough ascends left (release position, 41) -> center (42) -> right (43).
		self.assertLess(switch_pos[41][0], switch_pos[42][0])
		self.assertLess(switch_pos[42][0], switch_pos[43][0])
		# Left/Right ramp enters: left is left of right.
		self.assertLess(switch_pos[44][0], switch_pos[45][0])
		# Jets ascend in y (front-most/lowest jet has the largest y, i.e. closest to the flippers).
		self.assertLess(solenoid_pos[13][1], solenoid_pos[12][1])
		self.assertLess(solenoid_pos[12][1], solenoid_pos[14][1])
		# Trough ascends toward the front: Ball 1 (nearest eject) has a smaller y than Ball 4
		# (nearest drain).
		self.assertLess(switch_pos[32][1], switch_pos[35][1])

	def test_mechanism_inventory_covers_the_documented_toys_and_kickers(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.spider-wheel",
				"mechanism.crate", "mechanism.coffin", "mechanism.left-diverter",
				"mechanism.loop-gate", "mechanism.boogie-monsters",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)
		# The Boogie Monsters mechanism has no actuators or sensors -- confirmed cosmetic, not a
		# drop-target bank -- and its own behavior text must say so explicitly.
		self.assertEqual([], mechanisms["mechanism.boogie-monsters"]["actuators"])
		self.assertEqual([], mechanisms["mechanism.boogie-monsters"]["sensors"])
		self.assertIn("not drop targets", mechanisms["mechanism.boogie-monsters"]["behavior"])
		self.assertEqual("motorized", mechanisms["mechanism.spider-wheel"]["kind"])
		self.assertIn("backbox", mechanisms["mechanism.spider-wheel"]["label"].lower())
		self.assertIn("not motorized", mechanisms["mechanism.crate"]["label"].lower())
		self.assertNotEqual("motorized", mechanisms["mechanism.crate"]["kind"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.trough-eject-opto"}, set(relationships))
		self.assertEqual("switch.matrix-31", relationships["relationship.trough-eject-opto"]["destination"])
		self.assertEqual("pulse", relationships["relationship.trough-eject-opto"]["kind"])

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		self.assertEqual("dmd", displays[0]["kind"])
		self.assertEqual(128, displays[0]["width"])
		self.assertEqual(32, displays[0]["height"])
		self.assertEqual("not_applicable", displays[0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.ss-vpw-1-0", sources)
		self.assertTrue(sources["vpx-script.ss-vpw-1-0"]["known_working"])
		self.assertEqual(
			"4c9a63e77e10ea65d1146e33f81197bb41b719d70027d8fa0c2d258f823211b4",
			sources["vpx-script.ss-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"bede6f6c5b7592c4610af444a196c42432949468f708e79b4b112a73692cdc1e",
			sources["vpx-table.ss-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"f96109c68c7e0cc008f72e9be9f18405a216d5c40165aed130f1e87b65c44b09",
			sources["manual.bally.scared-stiff.1996"]["sha256"],
		)
		self.assertEqual(
			{"runtime.scared-stiff.aux-lamp-probe", "runtime.scared-stiff.flipper-button-polarity"},
			{source["id"] for source in self.definition["sources"] if source["kind"] == "runtime_scenario"},
		)
		self.assertEqual(
			"29b617dd43df7139cabc9c01966d1fc44219d3cb705dc2f0d1ba4b1cd990d182",
			sources["manufacturer-notes.bally.scared-stiff.1996"]["sha256"],
		)
		for source in self.definition["sources"]:
			self.assertNotEqual("rom_static_analysis", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("l:\\", value.lower())
					self.assertNotIn("l:/", value.lower())

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-95", profile["id"])
		self.assertTrue(profile["inversion_applied_by_emulator"])
		groups = {group["id"]: group for group in profile["groups"]}
		used = {device["binding"]["group"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		self.assertTrue(used <= set(groups))

		def allowed(group_id: str, address: int) -> bool:
			for rule in groups[group_id]["address_rules"]:
				if "values" in rule and address in rule["values"]:
					return True
				if "minimum" in rule and rule["minimum"] <= address <= rule["maximum"]:
					return True
			return False

		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			self.assertTrue(allowed(device["binding"]["group"], device["binding"]["device"]), device["id"])


class ScaredStiffPrototypeTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.prototype = load_json(PROTOTYPE_PATH)

	def test_the_d01r_drivers_live_in_their_own_partial_record(self) -> None:
		self.assertEqual("bally.scared-stiff-d01r-prototype.1996", self.prototype["machine"]["id"])
		self.assertEqual("partial", self.prototype["coverage"]["status"])
		self.assertNotIn("driver_mapping", self.prototype["coverage"]["missing"])
		self.assertIn("identity", self.prototype["coverage"]["missing"])
		self.assertEqual(PROTOTYPE_DRIVER_IDS, {driver["id"] for driver in self.prototype["drivers"]})
		for driver in self.prototype["drivers"]:
			self.assertEqual("ss_15", driver["clone_of"], driver["id"])
			self.assertIn("auxiliary lamp", driver["variant_notes"], driver["id"])
		self.assertEqual([], self.prototype["inputs"])
		self.assertEqual([], self.prototype["outputs"])
		self.assertTrue(PROTOTYPE_KNOWLEDGE_PATH.is_file())
		source_ids = {source["id"] for source in self.prototype["sources"]}
		self.assertIn("manufacturer-notes.bally.scared-stiff.1996", source_ids)
		self.assertIn("runtime.scared-stiff.aux-lamp-probe", source_ids)

	def test_the_catalog_maps_every_ss_driver_exactly_once(self) -> None:
		catalog = load_json(CATALOG_PATH)
		owners = {driver["id"]: driver["machine_id"] for driver in catalog["drivers"] if driver["id"].startswith("ss_")}
		self.assertEqual(DRIVER_IDS | PROTOTYPE_DRIVER_IDS, set(owners))
		for driver_id in DRIVER_IDS:
			self.assertEqual("bally.scared-stiff.1996", owners[driver_id], driver_id)
		for driver_id in PROTOTYPE_DRIVER_IDS:
			self.assertEqual("bally.scared-stiff-d01r-prototype.1996", owners[driver_id], driver_id)


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class ScaredStiffCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_scared_stiff as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_scared_stiff as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_scared_stiff as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Scared Stiff", b"Scared Stuff", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_curator_check_mode_refuses_a_stale_partial(self) -> None:
		import curate_scared_stiff as curator

		PARTIAL_PATH.write_bytes(DEFINITION_PATH.read_bytes())
		try:
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			PARTIAL_PATH.unlink()
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_scared_stiff as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class ScaredStiffRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_scared_stiff as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_scared_stiff as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "bally/scared-stiff-1996/source/Scared Stiff (Bally 1996) VPW v1.0.vpx"
		script = source_root / "bally/scared-stiff-1996/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_scared_stiff as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "scared-stiff-1996" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.scared-stiff.1996"


def _table_rows(text: str, columns: int) -> list[list[str]]:
	"""Return the cells of every Markdown table row with ``columns`` cells whose first cell is a driver id."""
	rows = []
	for line in text.splitlines():
		cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
		if len(cells) == columns and cells[0].startswith("`ss_"):
			rows.append(cells)
	return rows


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "review-artifacts root is not configured")
class ScaredStiffRuntimeAndCaptureEvidenceTests(unittest.TestCase):
	"""Re-derive the excerpts' harness tables and capture hashes from the retained raw evidence."""

	@classmethod
	def setUpClass(cls) -> None:
		from pinmame_game_defs.workspace import resolve_working_root

		cls.runtime_root = resolve_working_root(ROOT) / "runtime-evidence" / "scared-stiff-1996"
		cls.captures = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "scared-stiff-1996" / "aux-lamp-sources"
		cls.sources = {source["id"]: source for source in load_json(DEFINITION_PATH)["sources"]}

	def run_directory(self, name: str) -> tuple[Path, dict[str, object]]:
		import hashlib

		from build_external_evidence_manifest import check_manifest

		directory = self.runtime_root / name
		digest = check_manifest(directory, name.split("-", 1)[0])
		manifest = load_json(directory / "manifest.json")
		self.assertEqual(digest, hashlib.sha256((directory / "manifest.json").read_bytes()).hexdigest(), name)
		return directory, {
			"manifest": digest,
			"files": len(manifest["files"]),
			"bytes": sum(item["size"] for item in manifest["files"]),
			"run": hashlib.sha256((directory / "run.json").read_bytes()).hexdigest(),
		}

	def test_aux_lamp_probe_tables_are_recomputed_from_the_six_runs(self) -> None:
		text = (EXCERPT_DIRECTORY / "aux-lamp-probe.md").read_text(encoding="utf-8")
		counts = _table_rows(text, 7)
		identities = _table_rows(text, 5)
		self.assertEqual(6, len(counts))
		self.assertEqual([row[0] for row in counts], [row[0] for row in identities])
		for count_row, identity_row in zip(counts, identities):
			driver = count_row[0].strip("`")
			directory, identity = self.run_directory(f"{driver}-aux-lamp-probe")
			self.assertEqual(
				[f"`{identity['run']}`", f"`{identity['manifest']}`", str(identity["files"]), str(identity["bytes"])],
				identity_row[1:],
				driver,
			)
			run = load_json(directory / "run.json")
			self.assertEqual(driver, run["game"])
			self.assertIsNone(run["failure"], driver)
			self.assertEqual("8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5", run["library_sha256"])
			self.assertEqual("0b7367d8040988cde7c1b4182522845492479e152ded91617504379edf353ce8", run["scenario"]["sha256"])
			lamp_events = [event for event in run["events"] if event["event"] == "lamp" and event["number"] in AUX_LAMP_ADDRESSES]
			solenoid_counts: dict[int, int] = {}
			for event in run["events"]:
				if event["event"] == "solenoid" and event["number"] in {37, 38, 41, 42}:
					solenoid_counts[event["number"]] = solenoid_counts.get(event["number"], 0) + 1
			recomputed = [
				str(len({event["number"] for event in lamp_events})),
				str(len(lamp_events)),
				", ".join(f"{number}: {solenoid_counts[number]}" for number in sorted(solenoid_counts)) or "0",
				f"{lamp_events[0]['time_s']:.3f} s" if lamp_events else "-",
			]
			self.assertEqual(recomputed, count_row[3:], driver)

	def test_flipper_button_events_are_recomputed_from_the_run(self) -> None:
		import re

		directory, identity = self.run_directory("ss_15-flipper-button-polarity")
		self.assertEqual(self.sources["runtime.scared-stiff.flipper-button-polarity"]["sha256"], identity["run"])
		text = (EXCERPT_DIRECTORY / "flipper-button-polarity.md").read_text(encoding="utf-8")
		flat = " ".join(text.split())
		self.assertIn(f"`run.json` SHA-256 `{identity['run']}`", flat)
		self.assertIn(f"(SHA-256 `{identity['manifest']}`, {identity['files']} files, {identity['bytes']} bytes)", flat)
		run = load_json(directory / "run.json")
		self.assertIsNone(run["failure"])
		self.assertEqual("fddec3f6677aa7eadb0000c301e2fd9527b30598800cc66447c93cb1fd684f80", run["scenario"]["sha256"])
		eject = next(event["time_s"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == 9 and event["state"])
		self.assertIn(f"first fires at {eject:.3f} s", flat)
		rows: dict[float, tuple[list[str], list[str]]] = {}
		for event in run["events"]:
			if event["event"] == "switch" and event["number"] in {112, 114} and not event.get("initial"):
				rows.setdefault(event["time_s"], ([], []))[0].append(f"switch {event['number']} written {event['state']}")
			elif event["event"] == "solenoid" and event["number"] in {45, 46, 47, 48}:
				rows.setdefault(event["time_s"], ([], []))[1].append(f"solenoid {event['number']} {event['state']}")
		recomputed = [[f"{time:.3f}", "; ".join(", ".join(part) for part in parts if part)] for time, parts in sorted(rows.items())]
		printed = []
		for line in text.splitlines():
			match = re.fullmatch(r"\| (\d+\.\d{3}) \| (.+) \|", line.strip())
			if match:
				printed.append([match.group(1), re.sub(r" \([^)]*\)", "", match.group(2))])
		self.assertEqual(recomputed, printed)

	def test_retained_captures_match_the_manifest_and_source_hashes(self) -> None:
		import hashlib

		from build_external_evidence_manifest import check_manifest

		self.assertEqual("292cedb949dc7898378f3573d6c8ce028592d5b02561a56fbe835908a0c6bde4", check_manifest(self.captures, "ss_15"))
		for source_id, filename in (
			("manufacturer-notes.bally.scared-stiff.1996", "pinball-wms-com-games-stiff-dev.wayback-19970129085638.htm"),
			("owner-reports.bally.scared-stiff.1996.skull-driver", "pinside-scared-stiff-club-page-82.html"),
		):
			self.assertEqual(self.sources[source_id]["sha256"], hashlib.sha256((self.captures / filename).read_bytes()).hexdigest(), source_id)


if __name__ == "__main__":
	unittest.main()
