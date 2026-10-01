"""Fail-closed tests for the Stern Big Buck Hunter Pro (2010) definition.

The load-bearing assertions here are the ones that survive every schema check but would not
survive a wrong derivation: the trough's manual-labelled construction, the dedicated-switch
repurposing the retained table performs, the SAM auxiliary-write dead range, the stacked-
primitive lamps that must never grow a fabricated placement, and the coordinate convention's
979-unit width (the divisor trap this table's bounds set up).
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "big-buck-hunter-pro-2010.json"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "big-buck-hunter-pro-2010.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "big-buck-hunter-pro-2010.json"
SUPERSEDED_STUB_PATH = ROOT / "machines" / "stubs" / "bbh_170.json"
SUPERSEDED_STUB_KNOWLEDGE_PATH = ROOT / "knowledge" / "stubs" / "bbh_170.md"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "big-buck-hunter-pro-2010.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "sam.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "stern" / "big-buck-hunter-pro-2010.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "stern" / "big-buck-hunter-pro-2010.md"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "stern.big-buck-hunter-pro.2010"

MACHINE_ID = "stern.big-buck-hunter-pro.2010"
PARENT_DRIVER = "bbh_170"
CLONE_DRIVERS = {"bbh_140", "bbh_150", "bbh_160"}
UNRELATED_BBH_PREFIX_GAMES = frozenset()  # no other bbh_* driver exists in the pinned catalog

PLAYFIELD_WIDTH = 979.0
PLAYFIELD_HEIGHT = 2162.0

MATRIX_ADDRESSES = set(range(1, 65))
SERVICE_SWITCH_ADDRESSES = set(range(-7, 1))
DEDICATED_SWITCH_ADDRESSES = set(range(65, 73))
EXTENDED_SWITCH_ADDRESSES = set(range(73, 81))
FLIPPER_SWITCH_ADDRESSES = set(range(81, 89))
DIP_POSITIONS = set(range(1, 9))

GAME_ON_SOLENOID = 33
VIRTUAL_SOLENOID_ADDRESSES = set(range(33, 51))
AUX_SOLENOID_ADDRESSES = set(range(51, 67))
LAMP_ADDRESSES = set(range(1, 81))
SCRIPT_BOUND_LAMPS = {
	3, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
	29, 30, 31, 32, 33, 35, 38, 39, 40, 41, 42, 43, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55,
	57, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69, 70,
}
ATTRACT_OBSERVED_LAMPS = set(range(3, 81))
STACKED_PRIMITIVE_LAMPS = {27, 28, 29, 30}

EXPECTED_CONFLICT_IDS = {
	"conflict.elk-button-physical-control",
}
PINNED_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
SWITCH_TEST_SCENARIO = ROOT / "tools" / "harness-scenarios" / "stern" / "bbh-switch-test-sweep.json"
SWITCH_TEST_SOURCES = {
	"bbh_160": "runtime.big-buck-hunter-pro.bbh-160.switch-test-sweep",
	"bbh_170": "runtime.big-buck-hunter-pro.bbh-170.switch-test-sweep",
}
SWITCH_TEST_CONTROL_SOURCE = "runtime.avengers-limited-edition.switch-test-loki-control"
ROM_SWITCH_TEST_OPTOS = {21: "TROUGH #1 (R)", 22: "TROUGH JAM", 34: "RAM OPTO", 37: "BUCK WHEEL OPTO #1", 43: "BIRD OPTO", 45: "BUCK WHEEL OPTO #2"}
# Holding these in the switch test fires the coil the ROM pairs with the switch.
SWITCH_TEST_COILS = {23: [2], 26: [17], 27: [18], 30: [9], 31: [10], 32: [11], 34: [12]}


def _load_definition() -> dict:
	return json.loads(DEFINITION_PATH.read_text(encoding="utf-8"))


def _inputs_by_device(definition: dict) -> dict[int, dict]:
	return {int(device["binding"]["device"]): device for device in definition["inputs"] if device["binding"]["group"] == "pinmame.input.switch"}


def _outputs(definition: dict, group: str) -> dict[int, dict]:
	return {int(device["binding"]["device"]): device for device in definition["outputs"] if device["binding"]["group"] == group}


class IdentityTests(unittest.TestCase):
	def setUp(self) -> None:
		self.definition = _load_definition()

	def test_machine_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(machine["id"], MACHINE_ID)
		self.assertEqual(machine["manufacturer"], "Stern")
		self.assertEqual(machine["year"], 2010)
		self.assertEqual(machine["kind"], "physical_pinball")
		self.assertEqual(machine["ipdb_id"], 5513)
		self.assertEqual(machine["opdb_id"], "G4N6n-MLxER")

	def test_controller_platform(self) -> None:
		controller = self.definition["controller"]
		self.assertEqual(controller["platform"], "pinmame.sam")
		self.assertEqual(controller["hardware_generation"], "0x100000000000")

	def test_driver_family_is_exactly_four_identical_revisions(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(set(drivers), {PARENT_DRIVER, *CLONE_DRIVERS})
		self.assertNotIn("clone_of", drivers[PARENT_DRIVER])
		for driver_id in CLONE_DRIVERS:
			self.assertEqual(drivers[driver_id]["clone_of"], PARENT_DRIVER)
			self.assertEqual(drivers[driver_id]["physical_compatibility"], "identical")
		self.assertEqual(drivers[PARENT_DRIVER]["physical_compatibility"], "identical")

	def test_catalog_points_the_whole_family_here(self) -> None:
		catalog = json.loads((ROOT / "catalog" / "pinmame.json").read_text(encoding="utf-8"))
		machine_records = [record for record in catalog["machines"] if record["id"] == f"stub.pinmame.{PARENT_DRIVER}"]
		self.assertEqual(len(machine_records), 0, "the superseded stub must be pruned from the catalog")
		for record in catalog["drivers"]:
			if record["id"].startswith("bbh_"):
				self.assertNotEqual(record["machine_id"], f"stub.pinmame.{PARENT_DRIVER}")
				self.assertEqual(record["machine_id"], MACHINE_ID)

	def test_no_other_catalog_machine_shares_the_family(self) -> None:
		catalog = json.loads((ROOT / "catalog" / "pinmame.json").read_text(encoding="utf-8"))
		claimed = {record["id"] for record in catalog["drivers"] if record.get("machine_id") == MACHINE_ID}
		self.assertEqual(claimed, {PARENT_DRIVER, *CLONE_DRIVERS})


class CoverageTests(unittest.TestCase):
	def setUp(self) -> None:
		self.definition = _load_definition()

	def test_status_is_partial_with_exact_missing_list(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual(coverage["status"], "partial")
		self.assertEqual(
			coverage["missing"],
			[
				"input_semantics",
				"output_semantics",
				"polarity",
				"recreation_notes",
				"spatial_placement",
				"unresolved_conflicts",
			],
		)

	def test_unknown_address_sets_drive_semantic_dimensions(self) -> None:
		dimensions = self.definition["coverage"]["dimensions"]
		self.assertEqual(dimensions["semantic_naming"], "candidate")
		self.assertEqual(dimensions["physical_wiring"], "candidate")
		self.assertEqual(dimensions["address_enumeration"], "validated")
		self.assertEqual(dimensions["variant_coverage"], "validated")

	def test_conflicts_are_exactly_the_expected_set_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(set(conflicts), EXPECTED_CONFLICT_IDS)
		for conflict in conflicts.values():
			self.assertNotEqual(conflict.get("status"), "ignored")
			self.assertIn("Resolution path:", conflict["description"])


class AddressEnumerationTests(unittest.TestCase):
	def setUp(self) -> None:
		self.definition = _load_definition()
		self.switches = _inputs_by_device(self.definition)
		self.solenoids = _outputs(self.definition, "pinmame.output.solenoid")
		self.lamps = _outputs(self.definition, "pinmame.output.lamp")
		self.gi = _outputs(self.definition, "pinmame.output.gi")
		self.dips = {int(device["binding"]["device"]): device for device in self.definition["inputs"] if device["binding"]["group"] == "pinmame.input.dip"}

	def test_switch_envelope_is_complete_without_duplicates(self) -> None:
		expected = (
			SERVICE_SWITCH_ADDRESSES
			| MATRIX_ADDRESSES
			| DEDICATED_SWITCH_ADDRESSES
			| EXTENDED_SWITCH_ADDRESSES
			| FLIPPER_SWITCH_ADDRESSES
		)
		self.assertEqual(set(self.switches), expected)

	def test_extended_block_is_enumerated_unknown_with_the_v1_10_evidence(self) -> None:
		for address in sorted(EXTENDED_SWITCH_ADDRESSES):
			device = self.switches[address]
			self.assertEqual(device["availability"], "unknown", f"switch {address}")
			self.assertEqual(device["id"], f"switch.extended-{address}")
			self.assertIn("swMatrix[10]", device["physical"]["notes"])
		self.assertIn("left-flipper key", self.switches[73]["physical"]["notes"])
		self.assertIn("right-flipper key", self.switches[75]["physical"]["notes"])
		self.assertIn("front key", self.switches[79]["physical"]["notes"])

	def test_dip_bank_is_complete(self) -> None:
		self.assertEqual(set(self.dips), DIP_POSITIONS)

	def test_solenoid_space_is_complete(self) -> None:
		self.assertEqual(set(self.solenoids), set(range(1, 67)))
		self.assertEqual(set(self.lamps), LAMP_ADDRESSES)
		self.assertEqual(set(self.gi), {0})

	def test_display_inventory(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(len(displays), 1)
		self.assertEqual(displays[0]["kind"], "dmd")
		self.assertEqual((displays[0]["width"], displays[0]["height"]), (128, 32))

	def test_trough_switches_carry_the_manual_construction(self) -> None:
		for address in (18, 19, 20):
			physical = self.switches[address]["physical"]
			self.assertEqual(physical["part_number"], "180-5119-02")
			self.assertEqual(physical["switch_type"], "microswitch")
		for address in (21, 22):
			physical = self.switches[address]["physical"]
			self.assertEqual(physical["switch_type"], "opto")
			self.assertIn("515-0173-00", physical["part_number"])
			self.assertIn("515-0174-00", physical["part_number"])

	def test_unbound_addresses_are_unknown_never_unused(self) -> None:
		for address in (2, 3, 4, 12, 17, 46, 50, 55, 60, 64):
			self.assertEqual(self.switches[address]["availability"], "unknown", f"switch {address}")
		for address in (6, 8, 9, 10, 11, 13, 17, 18, 24, 28, 30):
			self.assertEqual(self.solenoids[address]["availability"], "unknown", f"solenoid {address}")
		for address in (1, 2):
			self.assertEqual(self.lamps[address]["availability"], "unknown", f"lamp {address}")

	def test_attract_observed_lamps_are_used_on_runtime_evidence(self) -> None:
		for address in sorted(ATTRACT_OBSERVED_LAMPS - SCRIPT_BOUND_LAMPS):
			device = self.lamps[address]
			self.assertEqual(device["availability"], "used", f"lamp {address}")
			self.assertEqual(device["provenance"]["status"], "observed")
			self.assertIn("runtime-scenario.bbh-attract-observe", device["provenance"]["source_refs"])
			self.assertIn("not that a physical bulb is fitted", device["physical"]["notes"])
			self.assertNotIn("spatial", device)

	def test_script_bound_lamps_are_used(self) -> None:
		for address in sorted(SCRIPT_BOUND_LAMPS):
			self.assertEqual(self.lamps[address]["availability"], "used", f"lamp {address}")

	def test_sam_aux_range_is_structurally_dead(self) -> None:
		for address in sorted(AUX_SOLENOID_ADDRESSES):
			device = self.solenoids[address]
			self.assertEqual(device["availability"], "unused")
			self.assertEqual(device["spatial"]["status"], "not_applicable")
			self.assertIn("SAM_NO_AUX", device["physical"]["notes"])

	def test_game_on_state_is_virtual_and_used(self) -> None:
		device = self.solenoids[GAME_ON_SOLENOID]
		self.assertEqual(device["kind"], "virtual")
		self.assertEqual(device["availability"], "used")
		self.assertIn("0x0106acae", device["physical"]["notes"])

	def test_virtual_range_dispositions(self) -> None:
		for address in sorted(VIRTUAL_SOLENOID_ADDRESSES - {GAME_ON_SOLENOID}):
			device = self.solenoids[address]
			self.assertEqual(device["availability"], "unused")
			self.assertEqual(device["spatial"]["reason"], "virtual")

	def test_uk_post_save_repurposing_is_disclosed_not_fabricated(self) -> None:
		for address in (71, 72):
			device = self.switches[address]
			self.assertEqual(device["availability"], "used")
			self.assertIn("not fitted", device["label"])
			self.assertIn("substitute", device["physical"]["notes"])

	def test_start_and_tournament_buttons_live_in_the_matrix_range(self) -> None:
		for address, token in ((15, "Tournament"), (16, "Start")):
			device = self.switches[address]
			self.assertEqual(device["availability"], "used", f"switch {address}")
			self.assertIn(token, device["label"])
			self.assertEqual(device["spatial"]["reason"], "cabinet_or_service")
			self.assertEqual(device["physical"]["switch_type"], "button")

	def test_elk_button_is_the_flipper_column_device(self) -> None:
		device = self.switches[85]
		self.assertEqual(device["availability"], "used")
		self.assertIn("Elk", device["label"])
		self.assertEqual(device["spatial"]["status"], "not_applicable")

	def test_flipper_eos_addresses_are_synthesized_and_undriven(self) -> None:
		for address in (82, 84, 86):
			device = self.switches[address]
			self.assertIn("emulator-synthesized", device["label"])
		for address in (87, 88):
			self.assertEqual(self.switches[address]["availability"], "unused")
			self.assertIn("not fitted", self.switches[address]["label"])

	def test_sam_platform_inversion_fact_is_carried(self) -> None:
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])


class SpatialTests(unittest.TestCase):
	def setUp(self) -> None:
		self.definition = _load_definition()

	def _placements(self) -> list[dict]:
		placements = []
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			if spatial and spatial["status"] != "not_applicable":
				placements += spatial["placements"]
		return placements

	def test_playfield_bounds_and_divisor(self) -> None:
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual(playfield["width"], PLAYFIELD_WIDTH)
		self.assertEqual(playfield["height"], PLAYFIELD_HEIGHT)
		self.assertEqual(playfield["units"], "vpx")

	def test_every_placement_is_in_range_with_six_decimals(self) -> None:
		for placement in self._placements():
			self.assertGreaterEqual(placement["x"], 0.0, placement["id"])
			self.assertLessEqual(placement["x"], 1.0, placement["id"])
			self.assertGreaterEqual(placement["y"], 0.0, placement["id"])
			self.assertLessEqual(placement["y"], 1.0, placement["id"])
			for coordinate in (placement["x"], placement["y"]):
				decimal_count = len(str(coordinate).split(".")[1]) if "." in str(coordinate) else 0
				self.assertLessEqual(decimal_count, 6, placement["id"])

	def test_placement_ids_are_unique(self) -> None:
		identifiers = [placement["id"] for placement in self._placements()]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_stacked_primitive_lamps_have_no_spatial_key(self) -> None:
		lamps = _outputs(self.definition, "pinmame.output.lamp")
		for address in sorted(STACKED_PRIMITIVE_LAMPS):
			self.assertNotIn("spatial", lamps[address], f"lamp {address} must not carry a fabricated placement")
			self.assertIn("stacked", lamps[address]["physical"]["notes"])

	def test_gi_carries_no_spatial_key(self) -> None:
		gi = _outputs(self.definition, "pinmame.output.gi")[0]
		self.assertNotIn("spatial", gi)

	def test_cabinet_devices_are_not_applicable_not_placed(self) -> None:
		switches = _inputs_by_device(self.definition)
		for address in (-7, -6, 16, 65, 66, 67, 68, 69, 81, 83, 85):
			self.assertEqual(switches[address]["spatial"]["reason"], "cabinet_or_service")

	def test_left_of_right_orderings(self) -> None:
		switches = _inputs_by_device(self.definition)
		# The retained table's own geometry: left slingshot left of right; bumper 30 (Bumper2)
		# right of bumper 32 (Bumper1); top lanes 7 < 8 < 9.
		self.assertLess(switches[26]["spatial"]["placements"][0]["x"], switches[27]["spatial"]["placements"][0]["x"])
		self.assertLess(switches[32]["spatial"]["placements"][0]["x"], switches[30]["spatial"]["placements"][0]["x"])
		self.assertLess(switches[7]["spatial"]["placements"][0]["x"], switches[8]["spatial"]["placements"][0]["x"])
		self.assertLess(switches[8]["spatial"]["placements"][0]["x"], switches[9]["spatial"]["placements"][0]["x"])

	def test_trough_positions_share_the_documented_kicker_projection(self) -> None:
		switches = _inputs_by_device(self.definition)
		points = {
			(switches[address]["spatial"]["placements"][0]["x"], switches[address]["spatial"]["placements"][0]["y"])
			for address in (18, 19, 20, 21, 22)
		}
		self.assertEqual(len(points), 1)
		provenance = switches[18]["spatial"]["placements"][0]["provenance"]
		self.assertEqual(provenance["status"], "observed")


class MechanismTests(unittest.TestCase):
	def setUp(self) -> None:
		self.definition = _load_definition()
		self.mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}

	def test_expected_mechanisms_exist(self) -> None:
		expected = {
			"mech.ball-trough",
			"mech.auto-launch",
			"mech.kickback-ram",
			"mech.buck-target",
			"mech.elk-diverter",
			"mech.up-down-posts",
			"mech.spinner",
		}
		self.assertEqual(set(self.mechanisms), expected)

	def test_trough_mechanism_topology(self) -> None:
		trough = self.mechanisms["mech.ball-trough"]
		self.assertEqual(trough["actuators"], ["solenoid.1"])
		self.assertEqual(
			trough["sensors"],
			["switch.matrix-18", "switch.matrix-19", "switch.matrix-20", "switch.matrix-21", "switch.matrix-22"],
		)

	def test_buck_mechanism_names_the_commented_feedback_optos(self) -> None:
		buck = self.mechanisms["mech.buck-target"]
		self.assertIn("switch.matrix-37", buck["sensors"])
		self.assertIn("switch.matrix-45", buck["sensors"])
		self.assertIn("solenoid.5", buck["actuators"])

	def test_device_ids_referenced_by_mechanisms_exist(self) -> None:
		known_ids = {device["id"] for device in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			for reference in mechanism.get("actuators", []) + mechanism.get("sensors", []):
				self.assertIn(reference, known_ids, f"{mechanism['id']} references missing {reference}")


class ProvenanceTests(unittest.TestCase):
	def setUp(self) -> None:
		self.definition = _load_definition()

	def test_sources_are_well_formed(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		for required in (
			"pinmame.catalog.8371478a7640",
			"pinmame.core.8371478a7640",
			"controller-profile.pinmame-sam",
			"manual.stern.big-buck-hunter-pro.2010",
			"ipdb.machine-5513",
			"vpx-table.bbh-stern-2010",
			"vpx-script.bbh-stern-2010",
			"vpx-extraction.bbh-stern-2010",
			"vpx-table.bbh-stern-2010-v1.10",
			"vpx-script.bbh-stern-2010-v1.10",
			"vpx-extraction.bbh-stern-2010-v1.10",
			"runtime-scenario.bbh-attract-observe",
			"rom.stern.big-buck-hunter-pro",
		):
			self.assertIn(required, sources)

	def test_v1_10_table_corroborates_without_overriding_geometry(self) -> None:
		v10_table = {source["id"]: source for source in self.definition["sources"]}["vpx-table.bbh-stern-2010-v1.10"]
		self.assertIn("not used for geometry", v10_table["locator"].lower())

	def test_manual_source_commits_all_excerpts_with_matching_digests(self) -> None:
		import hashlib

		manual = {source["id"]: source for source in self.definition["sources"]}["manual.stern.big-buck-hunter-pro.2010"]
		self.assertGreaterEqual(len(manual["excerpts"]), 7)
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file(), excerpt["path"])
			self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["sha256"], excerpt["path"])
			if excerpt.get("image"):
				image_path = ROOT / excerpt["image"]
				self.assertTrue(image_path.is_file(), excerpt["image"])
				self.assertEqual(hashlib.sha256(image_path.read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["image"])

	def test_no_local_paths_in_source_locators(self) -> None:
		for source in self.definition["sources"]:
			self.assertNotIn("L:\\", source.get("locator", ""), source["id"])
			self.assertNotIn("E:\\", source.get("locator", ""), source["id"])

	def test_170_rom_mismatch_is_disclosed(self) -> None:
		rom = {source["id"]: source for source in self.definition["sources"]}["rom.stern.big-buck-hunter-pro"]
		self.assertIn("NOT matching", rom["locator"])
		parent_note = {driver["id"]: driver for driver in self.definition["drivers"]}[PARENT_DRIVER]["variant_notes"]
		self.assertIn("5c292f8093130d2a3aef919aa57d9d8c5f8e7756", parent_note)

	def test_knowledge_note_exists_and_is_reachable(self) -> None:
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertEqual(self.definition["knowledge"]["path"], "knowledge/stern/big-buck-hunter-pro-2010.md")

	def test_every_used_device_carries_a_provenance_status(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"]:
			self.assertIn(device["provenance"]["status"], {"candidate", "observed", "validated", "conflicted"})
			if device["availability"] == "used":
				self.assertTrue(device["provenance"]["source_refs"], device["id"])


class CuratorDeterminismTests(unittest.TestCase):
	def test_curator_check_passes(self) -> None:
		import subprocess

		environment = dict(os.environ)
		environment["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), str(ROOT / "tools")])
		environment["PYTHONDONTWRITEBYTECODE"] = "1"
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "curate_big_buck_hunter_pro.py"), "--check"],
			capture_output=True,
			text=True,
			env=environment,
			cwd=ROOT,
		)
		self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

	def test_seed_is_byte_identical_to_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_no_author_ready_file_exists(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_superseded_stub_is_untouched_or_pruned(self) -> None:
		if SUPERSEDED_STUB_PATH.is_file():
			stub = json.loads(SUPERSEDED_STUB_PATH.read_text(encoding="utf-8"))
			self.assertEqual(stub["machine"]["id"], f"stub.pinmame.{PARENT_DRIVER}")

	def test_spatial_report_matches_definition_state(self) -> None:
		report = json.loads(SPATIAL_REPORT_PATH.read_text(encoding="utf-8"))
		self.assertEqual(report["machine_id"], MACHINE_ID)
		self.assertEqual(report["status"], "partial")
		self.assertEqual(
			report["coordinate_convention"]["source_bounds"],
			{"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
		)
		markdown = SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")
		self.assertIn("x/979.0", markdown)
		self.assertIn("Promotion to `author_ready` is refused", markdown)

	def test_forbidden_tokens_do_not_leak_into_artifacts(self) -> None:
		"""Every other machine id, driver id, and short name must stay out of this game's artifacts."""
		catalog = json.loads((ROOT / "catalog" / "pinmame.json").read_text(encoding="utf-8"))
		forbidden = set()
		for record in catalog["drivers"]:
			if record["id"].startswith("bbh_"):
				continue
			forbidden.add(record["id"])
			forbidden.update((record.get("description") or "").split())
		# Trim the noisy single-word descriptions; keep the machine-identity tokens.
		forbidden = {token for token in forbidden if len(token) >= 5 and "_" in token or token.startswith("stub.")}
		for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, KNOWLEDGE_PATH):
			text = path.read_text(encoding="utf-8")
			for token in forbidden:
				self.assertNotIn(token, text, f"{path.name} leaked {token}")


class RetainedExtractionTests(unittest.TestCase):
	def test_extraction_gates_are_evidence_optional(self) -> None:
		"""Without PINMAME_VPX_SOURCES_ROOT the retained-extraction paths must fail loudly, not silently pass."""
		sys.path.insert(0, str(ROOT / "tools"))
		import curate_big_buck_hunter_pro as curator

		previous = os.environ.pop("PINMAME_VPX_SOURCES_ROOT", None)
		try:
			with self.assertRaises(RuntimeError):
				curator.configured_vpx_sources_root(required=True)
		finally:
			if previous is not None:
				os.environ["PINMAME_VPX_SOURCES_ROOT"] = previous

	def test_extraction_verification_against_retained_evidence(self) -> None:
		working_root = ROOT.parent.parent
		sources_root = working_root / "vpx-sources"
		if not (sources_root / "stern" / "big-buck-hunter-pro-2010" / "extracted-vpxtool").is_dir():
			self.skipTest("retained VPX extraction not present")
		sys.path.insert(0, str(ROOT / "tools"))
		import curate_big_buck_hunter_pro as curator

		manifest = curator.verify_extraction_manifest(sources_root)
		self.assertEqual(len(manifest["files"]), curator.EXTRACTION_FILE_COUNT)



ROM_SWITCH_NAMES = {
	1: 'BUCK HIT',
	5: 'L. RAMP ENTRANCE',
	6: 'LEFT ORBIT',
	7: 'LEFT TOP LANE',
	8: 'CENTER TOP LANE',
	9: 'RIGHT TOP LANE',
	10: 'BU(C)K',
	13: 'RIGHT ORBIT',
	14: 'L. RAMP EXIT',
	15: 'TOURNAMENT START',
	16: 'START BUTTON',
	18: 'TROUGH #4 (L)',
	19: 'TROUGH #3',
	20: 'TROUGH #2',
	21: 'TROUGH #1 (R)',
	22: 'TROUGH JAM',
	23: 'SHOOTER LANE',
	24: 'LEFT OUTLANE',
	25: '(E)LK',
	26: 'LEFT SLINGSHOT',
	27: 'RIGHT SLINGSHOT',
	28: 'E(L)K',
	29: 'RIGHT OUTLANE',
	30: 'LEFT BUMPER',
	31: 'RIGHT BUMPER',
	32: 'BOTTOM BUMPER',
	33: 'EL(K)',
	34: 'RAM OPTO',
	35: 'BIRD TARGET',
	36: 'B(U)CK',
	37: 'BUCK WHEEL OPTO #1',
	38: '(B)UCK',
	39: 'BUC(K)',
	40: 'JUG 1 (TOP)',
	41: 'JUG 2',
	42: 'JUG 3 (BOT)',
	43: 'BIRD OPTO',
	44: 'SPINNER',
	45: 'BUCK WHEEL OPTO #2',
}


class SwitchTestEvidenceTests(unittest.TestCase):
	"""The ROM's switch-test sweep settles the six optos; the summaries are tied to the raw runs when retained."""

	def test_the_six_rom_named_optos_are_active_high_and_nothing_else_claims_polarity(self) -> None:
		definition = _load_definition()
		switches = _inputs_by_device(definition)
		refs = set(SWITCH_TEST_SOURCES.values()) | {SWITCH_TEST_CONTROL_SOURCE}
		for address, device in switches.items():
			if device["binding"]["group"] != "pinmame.input.switch":
				continue
			if address in ROM_SWITCH_TEST_OPTOS:
				self.assertIs(False, device["normally_closed"], address)
				self.assertEqual("opto", device["physical"]["switch_type"], address)
				self.assertIn(ROM_SWITCH_TEST_OPTOS[address], device["physical"]["notes"], address)
				self.assertIn("never inverts it", device["physical"]["notes"], address)
				self.assertLessEqual(refs, set(device["provenance"]["source_refs"]), address)
			else:
				self.assertNotIn("normally_closed", device, address)
				self.assertFalse(refs & set(device["provenance"]["source_refs"]), address)
		self.assertEqual("Ram Opto", switches[34]["label"])
		self.assertEqual("Bird Opto", switches[43]["label"])
		self.assertEqual("Buck Wheel Opto #1", switches[37]["label"])
		self.assertEqual("Buck Wheel Opto #2", switches[45]["label"])
		self.assertIn("kickback ram, solenoid 12", switches[34]["physical"]["notes"])
		self.assertNotIn("conflict.sam-invsw-never-populated", json.dumps(definition))

	def _retained(self, evidence: dict, game: str) -> dict | None:
		import hashlib
		import os

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return None
		import build_external_evidence_manifest as manifest

		(raw,) = evidence["runtime"]["raw_runs"]
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		digest = manifest.check_manifest(path.parent, game)
		# The digest on disk must be the one the summary cites, so a resealed directory cannot pass.
		self.assertIn(f"{game}/manifest.json SHA-256 {digest}", evidence["source"]["attribution"])
		run = json.loads(path.read_text(encoding="utf-8"))
		self.assertIsNone(run["failure"])
		self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
		self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
		return run

	def test_the_sweep_names_every_matrix_switch_only_while_it_is_held(self) -> None:
		import hashlib

		scenario_sha256 = hashlib.sha256(SWITCH_TEST_SCENARIO.read_bytes()).hexdigest()
		self.assertNotIn("game", json.loads(SWITCH_TEST_SCENARIO.read_text(encoding="utf-8")))
		sources = {source["id"]: source for source in _load_definition()["sources"]}
		frames: dict[str, list[str]] = {}
		for game, source_id in SWITCH_TEST_SOURCES.items():
			with self.subTest(game=game):
				path = ROOT / "evidence" / "runtime" / "sam" / f"big-buck-hunter-pro-{game}-switch-test-sweep.json"
				self.assertEqual("internal:" + path.relative_to(ROOT).as_posix(), sources[source_id]["uri"])
				evidence = json.loads(path.read_text(encoding="utf-8"))
				self.assertEqual([game], evidence["driver_ids"])
				self.assertEqual(["stern.big-buck-hunter-pro.2010"], evidence["machine_ids"])
				runtime = evidence["runtime"]
				self.assertEqual(PINNED_LIBRARY_SHA256, runtime["emulator"]["sha256"])
				(raw,) = runtime["raw_runs"]
				self.assertEqual(scenario_sha256, raw["scenario_sha256"])
				self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
				actions = runtime["observations"]["named_action_observations"]
				snapshots = runtime["observations"]["diagnostic_snapshots"]
				self.assertEqual(list(range(1, 65)), [item["input_address"] for item in actions])
				self.assertEqual(66, len(snapshots))
				self.assertEqual("SWITCH TEST / NONE", snapshots[1]["interpreted_text"])
				for item, snapshot in zip(actions, snapshots[2:], strict=True):
					address = item["input_address"]
					name = ROM_SWITCH_NAMES.get(address, f"SWITCH #{address}")
					self.assertEqual(f"SWITCH TEST / {name} / LAST SW. #{address}", snapshot["interpreted_text"])
					self.assertIn(f"prints {name} ", item["label"])
					self.assertEqual([address], item["host_stimulus_switch_addresses"])
					self.assertEqual(SWITCH_TEST_COILS.get(address, []), item["transitioned_solenoid_addresses"])
				frames[game] = [snapshot["pixel_sha256"] for snapshot in snapshots[1:]]
				run = self._retained(evidence, game)
				if run is None:
					continue
				by_label = {snap["label"]: snap for snap in run["snapshots"]}
				expected = [by_label["booted"], by_label["Select 5: switch test"]] + [by_label[f"hold {address} (held)"] for address in range(1, 65)]
				self.assertEqual(
					[(snap["displays"][0]["pixel_sha256"], snap["displays"][0]["nonzero_pixels"]) for snap in expected],
					[(item["pixel_sha256"], item["nonzero_pixels"]) for item in snapshots],
				)
				for address in range(1, 65):
					levels = {w["number"]: w["state"] for w in by_label[f"hold {address} (held)"]["watched_switches"]}
					self.assertEqual(1, levels[address])
		# Firmware 1.6 and 1.7 draw the identical switch-test page for every switch.
		self.assertEqual(frames["bbh_160"], frames["bbh_170"])

	def test_the_control_run_is_cited_by_its_own_artifact_name(self) -> None:
		source = {source["id"]: source for source in _load_definition()["sources"]}[SWITCH_TEST_CONTROL_SOURCE]
		path = ROOT / source["uri"][len("internal:"):]
		evidence = json.loads(path.read_text(encoding="utf-8"))
		self.assertEqual(["stern.avengers-limited-edition.2012"], evidence["machine_ids"])
		texts = [item["interpreted_text"] for item in evidence["runtime"]["observations"]["diagnostic_snapshots"]]
		self.assertEqual("SWITCH TEST / NONE / LAST SW. #47", texts[4])
		self.assertTrue(texts[5].startswith("SWITCH TEST / LOKI LOCK 1 (BOT) / LAST SW. #49"))


if __name__ == "__main__":
	unittest.main()
