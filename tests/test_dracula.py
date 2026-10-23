from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "bram-stoker-s-dracula-1993.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "bram-stoker-s-dracula-1993.json"
CALLOUT_SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "bram-stoker-s-dracula-1993-callouts.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "bram-stoker-s-dracula-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "dracula.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "bram-stoker-s-dracula-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "bram-stoker-s-dracula-1993.md"

DRIVER_IDS = {"drac_l1", "drac_d1", "drac_l2c", "drac_p11", "drac_p12"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 18, 23, 32, 33, 45, 46, 47, 74, 75, 76, 78}
OPTO_ADDRESSES = {51, 52, 53, 54, 55, 56, 57, 71, 72, 73, 82}


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
	import curate_dracula as curator

	argv = sys.argv
	sys.argv = ["curate_dracula.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class DraculaDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_on_the_flasher_19_count_alone(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		# Flasher 19's playfield bulb count is the one unresolved question; everything else is validated.
		self.assertEqual(["unresolved_conflicts"], self.definition["coverage"]["missing"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			self.assertEqual("conflicted" if dimension == "physical_wiring" else "validated", state, dimension)
		self.assertEqual("williams.bram-stoker-s-dracula.1993", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(3072, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1993, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_driver_set_matches_physical_family(self) -> None:
		driver_ids = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, driver_ids)
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["drac_l1"])
		for clone_id in DRIVER_IDS - {"drac_l1"}:
			self.assertEqual("drac_l1", by_id[clone_id]["clone_of"])
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"])

	def test_unconfigured_fast_flip_channel_uses_gilamps_state(self) -> None:
		self.assertIn("WPC_GILAMPS bit 7", self.solenoids[31]["physical"]["notes"])
		self.assertNotIn("fast-flip RAM flag", self.solenoids[31]["physical"]["notes"])

	def test_switch_matrix_covers_every_address_exactly_once(self) -> None:
		matrix_switches = {address: item for address, item in self.switches.items() if address in MATRIX_ADDRESSES}
		self.assertEqual(MATRIX_ADDRESSES, set(matrix_switches))
		for address, item in matrix_switches.items():
			expected_availability = "unused" if address in UNUSED_MATRIX_ADDRESSES else "used"
			self.assertEqual(expected_availability, item["availability"], address)

	def test_opto_addresses_match_pinmame_inverted_switch_mask_with_zero_disagreement(self) -> None:
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			item = self.switches[address]
			if item["kind"] != "switch":
				continue
			expected_normally_closed = address in OPTO_ADDRESSES
			self.assertEqual(expected_normally_closed, item["normally_closed"], address)
			expected_type = "opto" if address in OPTO_ADDRESSES else item["physical"].get("switch_type")
			self.assertEqual(expected_type, item["physical"].get("switch_type"), address)

	def test_no_upper_flippers_are_modeled_as_used(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			item = self.switches[address]
			self.assertEqual("unused", item["availability"], address)
			self.assertEqual("not_applicable", item["spatial"]["status"], address)
			self.assertEqual("unused", item["spatial"]["reason"], address)

	def test_upper_flipper_circuit_solenoids_are_repurposed_not_flippers(self) -> None:
		labels = {33: "Up/Down Post Diverter", 34: "Right Gate", 35: "Castle Release Post", 36: "Left Gate Actuator"}
		for address, label in labels.items():
			item = self.solenoids[address]
			self.assertEqual(label, item["label"], address)
			self.assertEqual("used", item["availability"], address)

	def test_flipper_coils_are_at_the_wpc_fliptronic_addresses(self) -> None:
		for address in (45, 46, 47, 48):
			self.assertEqual("used", self.solenoids[address]["availability"], address)

	def test_single_drop_target_not_a_three_bank(self) -> None:
		mechanism_ids = {mechanism["id"] for mechanism in self.definition["mechanisms"]}
		self.assertIn("mechanism.drop-target", mechanism_ids)
		mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.drop-target")
		self.assertEqual(["switch.matrix-15", "switch.matrix-16"], sorted(mechanism["sensors"]))

	def test_the_flasher_19_bulb_count_conflict_is_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		conflict = conflicts["conflict.flasher-19-playfield-bulb-count"]
		self.assertEqual("unresolved", conflict.get("status", "unresolved"))
		self.assertEqual("binding:pinmame.output.solenoid/19", conflict["path"])
		for text in ("(1) #89", "#89(1)", "two callouts 19", "F19 and F19a", "Resolution path:"):
			self.assertIn(text, conflict["description"])
		solenoid = self.solenoids[19]
		self.assertEqual("conflicted", solenoid["provenance"]["status"])
		self.assertEqual(3, solenoid["physical"]["quantity"])
		self.assertIn("conflict.flasher-19-playfield-bulb-count", solenoid["physical"]["notes"])
		# Both drawn sockets stay placed and checked against their callouts.
		self.assertEqual(
			["validated", "validated"],
			[placement["provenance"]["status"] for placement in solenoid["spatial"]["placements"]],
		)

	def test_the_upper_flipper_circuit_side_naming_conflict_is_recorded_and_ignored(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual({"conflict.upper-flipper-circuit-side-naming", "conflict.flasher-19-playfield-bulb-count"}, set(conflicts))
		conflict = conflicts["conflict.upper-flipper-circuit-side-naming"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		# Both readings stay on the record; the device and its address agree, so it does not block.
		self.assertEqual("ignored", conflict["status"])
		self.assertIn("naming and board-designator disagreement", conflict["rationale"])
		for label in ("sURFlipPow", "Up Lt. F.", "Up Rt. F."):
			self.assertIn(label, conflict["description"])
		for address in (33, 34, 35, 36):
			self.assertIn(str(address), conflict["path"])
			solenoid = self.solenoids[address]
			self.assertEqual("validated", solenoid["provenance"]["status"])
			self.assertIn("conflict.upper-flipper-circuit-side-naming is ignored", solenoid["physical"]["notes"])

	def test_no_author_ready_copy_exists(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_lamp_53_rides_the_magnet_carrier_and_projects_onto_the_insert_row(self) -> None:
		lamp = self.lamps[53]
		self.assertEqual("used", lamp["availability"])
		self.assertEqual("Mist Magnet carrier, below the playfield", lamp["physical"]["location"])
		for text in ("A-16205 Light Socket & Bulb Assembly", "moves in unison", "ml7", "never reads it"):
			self.assertIn(text, lamp["physical"]["notes"])
		(placement,) = lamp["spatial"]["placements"]
		self.assertEqual((0.487873, 0.528631), (placement["x"], placement["y"]))
		self.assertEqual("validated", placement["provenance"]["status"])
		self.assertIn("manual.williams.bram-stoker-s-dracula.1993", placement["provenance"]["source_refs"])

	def test_the_carrier_coil_and_motor_project_onto_the_magnet_zone_centroid(self) -> None:
		for address in (27, 28):
			(placement,) = self.solenoids[address]["spatial"]["placements"]
			self.assertEqual((0.48705, 0.488832), (placement["x"], placement["y"]), address)
			self.assertIn("Trigger.Magnet", self.solenoids[address]["physical"]["notes"], address)

	def test_the_magnet_switches_sit_where_they_act_on_the_carriage_track(self) -> None:
		expected = {81: (0.116482, 0.561548), 82: (0.132222, 0.576111), 83: (0.891975, 0.408)}
		for address, xy in expected.items():
			(placement,) = self.switches[address]["spatial"]["placements"]
			self.assertEqual(xy, (placement["x"], placement["y"]), address)
			self.assertIn("vpx-script.drac-vpw-1-0", placement["provenance"]["source_refs"], address)
		# The carriage line is y = -0.44 x + 1238 and the beam line runs through (126, 1220).
		self.assertAlmostEqual(-0.44 * 111 + 1238, 0.561548 * 2117.647, delta=0.01)
		self.assertAlmostEqual(-0.44 * 850 + 1238, 0.408 * 2117.647, delta=0.01)

	def test_switch_34_is_the_cabinet_launch_button(self) -> None:
		switch = self.switches[34]
		self.assertEqual(["cabinet.launch"], switch["roles"])
		self.assertEqual("not_applicable", switch["spatial"]["status"])
		self.assertEqual("cabinet_or_service", switch["spatial"]["reason"])
		self.assertEqual("A-15896-1", switch["physical"]["part_number"])
		self.assertIn("swLaunch", switch["physical"]["notes"])

	def test_lower_flipper_windings_have_their_own_drive_pins(self) -> None:
		expected = {45: ("J902-13", "Blu-Vio", "Q4"), 46: ("J902-11", "Org-Grn", "Q11"), 47: ("J902-9", "Blu-Gry", "Q3"), 48: ("J902-7", "Org-Blu", "Q9")}
		for address, (pin, wire, transistor) in expected.items():
			wiring = self.solenoids[address]["wiring"]
			self.assertEqual((pin, wire, transistor), (wiring["control_connection"], wiring["control_wire"], wiring["driver_transistor"]), address)
			self.assertEqual("WPC Fliptronic II board", wiring["board"], address)

	def test_upper_flipper_circuits_follow_the_board_mapping(self) -> None:
		# PinMAME, the controller profile and Twilight Zone's runtime binding put 33/34 on the upper-right pair.
		expected = {33: ("Q2", "J902-6", "Blk-Yel"), 34: ("Q7", "J902-4", "Org-Vio"), 35: ("Q1", "J902-3", "Blk-Blu"), 36: ("Q5", "J902-1", "Org-Gry")}
		for address, (transistor, pin, wire) in expected.items():
			solenoid = self.solenoids[address]
			wiring = solenoid["wiring"]
			self.assertEqual((transistor, pin, wire), (wiring["driver_transistor"], wiring["control_connection"], wiring["control_wire"]), address)
			self.assertEqual("WPC Fliptronic II board", wiring["board"], address)
			self.assertIn("human-review.fliptronic-ii-upper-circuits", solenoid["provenance"]["source_refs"], address)
		# The printed 3-8 rows stay verbatim in the excerpt.
		excerpt = (ROOT / "evidence/excerpts/williams.bram-stoker-s-dracula.1993/solenoid-flasher-wiring.md").read_text(encoding="utf-8")
		self.assertIn("| 33 Up/Down Post Diverter | Up Lt. F. Power | J907-2 | Q1 | — | J902-3 | Blk-Blu |", excerpt)

	def test_every_solenoid_row_carries_its_printed_drive_wire(self) -> None:
		for address, solenoid in self.solenoids.items():
			if solenoid["kind"] == "virtual":
				continue
			self.assertIn("control_wire", solenoid["wiring"], address)

	def test_flasher_quantities_count_printed_bulbs_and_place_playfield_ones(self) -> None:
		quantities = {17: 4, 18: 2, 19: 3, 20: 3, 21: 3, 22: 2, 23: 2, 24: 2, 26: 3}
		placed = {17: 3, 18: 1, 19: 2, 20: 2, 21: 2, 22: 1, 23: 1, 24: 1}
		for address, quantity in quantities.items():
			solenoid = self.solenoids[address]
			self.assertEqual(quantity, solenoid["physical"]["quantity"], address)
			if address in placed:
				self.assertEqual(placed[address], len(solenoid["spatial"]["placements"]), address)
			else:
				self.assertEqual("not_applicable", solenoid["spatial"]["status"], address)

	def test_back_panel_lamps_are_placed_on_the_panel_plane(self) -> None:
		for address in (58, 61, 62, 63):
			lamp = self.lamps[address]
			self.assertEqual("playfield back panel", lamp["physical"]["location"], address)
			self.assertIn("A-16399 Back Panel & Decal Assembly (printed 2-39)", lamp["physical"]["notes"], address)
			self.assertEqual("validated", lamp["spatial"]["status"], address)
			(placement,) = lamp["spatial"]["placements"]
			self.assertLess(placement["y"], 0.011, address)
			self.assertEqual("validated", placement["provenance"]["status"], address)
		# The inset draws 61, 62, 63 left to right with 58 right of them, as the table lights run.
		xs = [self.lamps[address]["spatial"]["placements"][0]["x"] for address in (61, 62, 63, 58)]
		self.assertEqual(sorted(xs), xs)

	def test_gi_playfield_strings_have_placements_and_backbox_strings_do_not(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			self.assertGreater(len(self.gi[address]["spatial"]["placements"]), 0, address)
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)

	def test_gi_playfield_placement_counts_match_retained_light_collections(self) -> None:
		self.assertEqual(8, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(20, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(10, len(self.gi[2]["spatial"]["placements"]))

	def test_dracula_name_chase_addresses_spell_dracula_in_documented_order(self) -> None:
		chase_order = [48, 36, 23, 71, 67, 72, 82]
		self.assertEqual({48, 36, 23, 71, 67, 72, 82}, set(chase_order))
		expected_letters = "DRACULA"
		for address, letter in zip(chase_order, expected_letters):
			self.assertIn(letter, self.lamps[address]["label"].upper(), address)

	def test_left_right_switch_geometry_is_on_the_correct_side(self) -> None:
		def x_of(address: int) -> float:
			return self.switches[address]["spatial"]["placements"][0]["x"]

		self.assertLess(x_of(35), 0.5)  # Left Drain
		self.assertGreater(x_of(38), 0.5)  # Right Drain
		self.assertLess(x_of(36), 0.5)  # Left Return
		self.assertGreater(x_of(37), 0.5)  # Right Return
		self.assertLess(x_of(64), 0.5)  # Left Slingshot
		self.assertGreater(x_of(65), 0.5)  # Right Slingshot

	def test_trough_switches_are_monotonically_ordered(self) -> None:
		positions = [self.switches[address]["spatial"]["placements"][0]["y"] for address in (41, 42, 43, 44)]
		self.assertEqual(sorted(positions), positions)

	def test_no_duplicate_device_identifiers(self) -> None:
		identifiers = [device["id"] for device in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_seed_is_byte_identical_to_canonical_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_controller_profile_is_reused_unchanged(self) -> None:
		self.assertTrue(CONTROLLER_PATH.is_file())
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-fliptronic", profile["id"])

	def test_knowledge_file_exists_and_is_referenced(self) -> None:
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertEqual("knowledge/williams/dracula.md", self.definition["knowledge"]["path"])

	def test_spatial_report_files_exist(self) -> None:
		self.assertTrue(SPATIAL_REPORT_PATH.is_file())
		self.assertTrue(SPATIAL_REPORT_MARKDOWN_PATH.is_file())
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("williams.bram-stoker-s-dracula.1993", report["machine_id"])
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(1, len(report["blockers"]))
		self.assertTrue(report["blockers"][0].startswith("conflict.flasher-19-playfield-bulb-count:"))
		self.assertEqual(["conflict.flasher-19-playfield-bulb-count"], [entry["conflict"] for entry in report["unresolved"]])
		self.assertEqual([], report["no_spatial_key_outputs"])

	def test_curator_check_mode_is_idempotent(self) -> None:
		import curate_dracula as curator

		curator.check(curator.ROOT)

	def test_curator_cli_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()


class DraculaDrawingCalloutTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		import drawing_callouts

		cls.dc = drawing_callouts
		cls.definition = load_json(DEFINITION_PATH)
		cls.seed = load_json(CALLOUT_SEED_PATH)
		cls.placements = drawing_callouts.placements_of(cls.definition)

	def test_every_checked_placement_agrees_with_its_drawing(self) -> None:
		decisions = self.dc.evaluate(self.seed, self.placements, self.seed["limit"])
		disagreeing = sorted(pid for pid, decision in decisions["placements"].items() if not decision["agrees"])
		self.assertEqual([], disagreeing)
		self.assertEqual(120, len(decisions["placements"]))
		self.assertEqual({"2-44", "2-45", "2-46"}, set(decisions["pages"]))
		for page in decisions["pages"].values():
			self.assertLessEqual(page["control_loo_max"], 0.015)
			self.assertEqual(page["callout_pairs"], page["callout_fit_pairs"])

	def test_every_placement_is_checked_excluded_measured_or_gi(self) -> None:
		accounted = set(self.seed["checks"]) | set(self.seed["excluded_checks"]) | set(self.seed["measurements"])
		self.assertEqual(set(), set(self.seed["checks"]) & set(self.seed["measurements"]))
		self.assertEqual(set(), set(self.seed["excluded_checks"]) & set(self.seed["measurements"]))
		for placement_id in self.placements:
			if placement_id.startswith("gi."):
				self.assertNotIn(placement_id, accounted)
			else:
				self.assertIn(placement_id, accounted)
		for placement, status in ((p["id"], p["provenance"]["status"]) for c in ("inputs", "outputs") for d in self.definition[c] for p in (d.get("spatial") or {}).get("placements") or []):
			self.assertEqual("validated", status, placement)

	def test_the_frame_corners_match_the_table_bounds_on_every_page(self) -> None:
		for key, page in self.seed["pages"].items():
			frame = [control["xy"] for control in page["controls"] if control["object"].startswith("playfield bounds")]
			self.assertEqual([[0.0, 0.0], [1.0, 0.0]], frame, key)
			pairs = [(tuple(control["pixel"]), tuple(control["xy"])) for control in page["controls"]]
			self.assertLessEqual(max(self.dc.leave_one_out(pairs)), 0.015, key)

	def test_the_coffin_flasher_domes_are_measured_inside_the_control_hull(self) -> None:
		import curate_dracula as curator

		self.assertEqual({"device.t-r-corner-dracula-flasher.emitter.2", "device.t-r-corner-dracula-flasher.emitter.3"}, set(self.seed["measurements"]))
		for placement_id in self.seed["measurements"]:
			x, y = self.dc.measured(self.seed, placement_id)
			self.assertEqual((x, y), self.placements[placement_id])
			self.assertTrue(curator._within_control_hull(self.seed, placement_id, x, y), placement_id)
			placement = next(p for d in self.definition["outputs"] for p in (d.get("spatial") or {}).get("placements") or [] if p["id"] == placement_id)
			for ref in ("manual.williams.bram-stoker-s-dracula.1993", "drawing-callouts.dracula.2026-10-23", "human-review.dracula-physical-corroboration-2026-10-23"):
				self.assertIn(ref, placement["provenance"]["source_refs"])

	def test_the_verifier_corrections_are_recorded(self) -> None:
		corrected = {(key, read["label"]): read for key, page in self.seed["pages"].items() for read in page["reads"] if "verifier_note" in read}
		self.assertEqual({("2-46", "57"), ("2-46", "73"), ("2-44", "53")}, set(corrected))
		self.assertEqual("pair_midpoint", corrected[("2-46", "73")]["point"])
		for read in corrected.values():
			self.assertIn("reader_pixel", read)

	def test_the_magnet_beam_switch_leader_ends_at_the_beam_line(self) -> None:
		decisions = self.dc.evaluate(self.seed, self.placements, self.seed["limit"])
		decision = decisions["placements"]["switch.matrix-82.sensor"]
		self.assertTrue(decision["agrees"])
		self.assertLessEqual(max(decision["control_offset"], decision["callout_offset"]), 0.005)

	def test_the_drawing_crops_match_the_seed(self) -> None:
		self.assertEqual(3, self.dc.verify_retained(self.seed, ROOT, None, None))


class DraculaRetainedEvidenceTests(unittest.TestCase):
	def _review_artifacts(self) -> Path:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		return Path(root)

	def test_callout_check_artifacts_match_the_pinned_manifest(self) -> None:
		import drawing_callouts

		seed = load_json(CALLOUT_SEED_PATH)
		checked = drawing_callouts.verify_retained(seed, ROOT, None, self._review_artifacts())
		self.assertGreater(checked, 3)

	def test_physical_photographs_match_the_pinned_manifest(self) -> None:
		import curate_dracula as curator
		from build_external_evidence_manifest import check_manifest

		directory = self._review_artifacts() / curator.PHYSICAL_EVIDENCE_DIRECTORY
		self.assertEqual(curator.PHYSICAL_EVIDENCE_MANIFEST_SHA256, check_manifest(directory, "drac_l1"))


class DraculaRetainedTableTests(unittest.TestCase):
	"""Recompute the table-derived projections and placements from the retained extraction."""

	WIDTH = 952.941
	HEIGHT = 2117.647

	@classmethod
	def setUpClass(cls) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			raise unittest.SkipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_dracula as curator

		cls.extraction = Path(root) / curator.EXTRACTION_RELATIVE_PATH
		cls.script = (cls.extraction / "script.vbs").read_text(encoding="utf-8", errors="replace")
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def _item(self, name: str) -> dict[str, object]:
		data = load_json(self.extraction / "gameitems" / f"{name}.json")
		(item,) = data.values()
		return item

	def _normalized(self, x: float, y: float) -> tuple[float, float]:
		return round(x / self.WIDTH, 6), round(y / self.HEIGHT, 6)

	def _script_constant(self, name: str) -> float:
		import re

		match = re.search(rf"^const {name} = (-?[0-9.]+)", self.script, re.MULTILINE)
		self.assertIsNotNone(match, name)
		return float(match.group(1))

	def test_the_carrier_projection_is_the_magnet_zone_area_centroid(self) -> None:
		points = [(p["x"], p["y"]) for p in self._item("Trigger.Magnet")["drag_points"]]
		self.assertEqual(4, len(points))
		cross = [x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1])]
		area = sum(cross) / 2
		cx = sum((x0 + x1) * c for ((x0, _), (x1, _)), c in zip(zip(points, points[1:] + points[:1]), cross)) / (6 * area)
		cy = sum((y0 + y1) * c for ((_, y0), (_, y1)), c in zip(zip(points, points[1:] + points[:1]), cross)) / (6 * area)
		for address in (27, 28):
			(placement,) = self.solenoids[address]["spatial"]["placements"]
			self.assertEqual(self._normalized(cx, cy), (placement["x"], placement["y"]), address)

	def test_lamp_53_projects_onto_ml7_which_the_script_never_binds_to_lamp_53(self) -> None:
		ml7 = self._item("Light.ml7")
		(placement,) = self.lamps[53]["spatial"]["placements"]
		self.assertEqual(self._normalized(ml7["center"]["x"], ml7["center"]["y"]), (placement["x"], placement["y"]))
		collections = load_json(self.extraction / "collections.json")
		(lamps,) = [c for c in collections if c["name"] == "alllamps"]
		self.assertIn("vpmMapLights AllLamps", self.script)
		intervals = {self._item(f"Light.{name}")["timer_interval"] for name in lamps["items"]}
		self.assertNotIn(53, intervals)
		self.assertNotIn("ml7", lamps["items"])
		self.assertNotRegex(self.script, r"(?i)lamp\w*\(\s*53\s*\)")

	def test_the_magnet_switches_follow_the_script_carriage_line(self) -> None:
		x1, x2 = self._script_constant("motorx1"), self._script_constant("motorx2")
		y2, span = self._script_constant("motory2"), self._script_constant("motorxrange")
		slope, intercept = self._script_constant("motorslope"), self._script_constant("motoryint")
		expected = {
			81: self._normalized(x1 - span, slope * (x1 - span) + intercept),
			82: self._normalized(x2, y2),
			83: self._normalized(x1, slope * x1 + intercept),
		}
		for address, xy in expected.items():
			(placement,) = self.switches[address]["spatial"]["placements"]
			self.assertEqual(xy, (placement["x"], placement["y"]), address)

	def test_back_panel_lamps_take_their_script_bound_lights(self) -> None:
		import curate_dracula as curator

		for address, (name, position) in curator.BACK_PANEL_LAMPS.items():
			light = self._item(f"Light.{name}")
			self.assertEqual(address, light["timer_interval"], name)
			self.assertEqual(self._normalized(light["center"]["x"], light["center"]["y"]), position, name)
			(placement,) = self.lamps[address]["spatial"]["placements"]
			self.assertEqual(position, (placement["x"], placement["y"]), address)
			self.assertEqual("playfield back panel", self.lamps[address]["physical"]["location"], address)

	def test_flasher_19_drives_a_light_at_each_three_bank(self) -> None:
		self.assertRegex(self.script, r'SolModCallback\(19\) = "Flasher19"')
		self.assertRegex(self.script, r"Sub Flasher19\(pwm\)[^\n]*\n(?:[^\n]*\n)*?\s*F19\.State = pwm\s*\n\s*F19a\.State = pwm")
		placements = [(p["x"], p["y"]) for p in self.solenoids[19]["spatial"]["placements"]]
		for name in ("F19", "F19a"):
			light = self._item(f"Light.{name}")
			self.assertIn(self._normalized(light["center"]["x"], light["center"]["y"]), placements, name)


if __name__ == "__main__":
	unittest.main()
