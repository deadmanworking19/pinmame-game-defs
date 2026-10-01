from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "the-getaway-high-speed-ii-1992.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "the-getaway-high-speed-ii-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "the-getaway-high-speed-ii-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "the-getaway-high-speed-ii-1992.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "the-getaway-high-speed-ii-1992.json"

DRIVER_IDS = {
	"gw_l5", "gw_d5", "gw_l5c", "gw_pb", "gw_pc", "gw_pd", "gw_p7", "gw_p8",
	"gw_l1", "gw_d1", "gw_l2", "gw_d2", "gw_l3", "gw_d3",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 35, 47, 48, 64, 66, 68}
OPTO_ADDRESSES = {81, 82, 83, 84, 85}
PINNED_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
SWITCH_EDGES_SOURCES = {
	"gw_l5": "runtime.getaway.gw-l5.switch-edges",
	"gw_l1": "runtime.getaway.gw-l1.switch-edges",
}
FLIPPER_ENABLE_SOURCE = "runtime.getaway.gw-l5.flipper-enable-31"
RUNTIME_DIR = ROOT / "evidence" / "runtime" / "wpc-fliptronic"
EDGES_SCENARIO = ROOT / "tools" / "harness-scenarios" / "wpc-fliptronic" / "gw-switch-edges-84-85.json"
PLAY_SCENARIO = ROOT / "tools" / "harness-scenarios" / "wpc-fliptronic" / "gw-flipper-enable-31.json"
ROM_NAMES = {45: "R BANK MID", 81: "OPTO 1", 84: "ENTER LEFT RAMP", 85: "OPTO MADE LOOP"}
EDGE_SEQUENCE = [45, 45, 81, 81, 84, 84, 85, 85, 84, 84, 85, 85, 45, 45]
GAME_IDENTIFICATION = {"gw_l5": "HIGH SPEED II / 50004 REV. L-5", "gw_l1": "HIGH SPEED II / 50004 REV. L-1"}


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
	import curate_getaway as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_getaway.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class GetawayDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(
			["recreation_notes", "spatial_placement"],
			self.definition["coverage"]["missing"],
		)
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["semantic_naming"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["output_semantics"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("williams.the-getaway-high-speed-ii.1992", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1000, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1992, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])

	def test_both_former_conflicts_are_settled_by_the_rom(self) -> None:
		self.assertEqual([], self.definition["conflicts"])
		self.assertNotIn("conflict.", json.dumps(self.definition))
		# The ROM's T.1 SWITCH EDGES names decide 84/85; both printed pages carry them transposed.
		self.assertEqual("Enter Left Ramp", self.switches[84]["label"])
		self.assertEqual("Opto Made Loop", self.switches[85]["label"])
		for address, printed in ((84, "Opto Made Loop"), (85, "Enter Left Ramp")):
			switch = self.switches[address]
			self.assertEqual("validated", switch["provenance"]["status"])
			self.assertLessEqual(set(SWITCH_EDGES_SOURCES.values()), set(switch["provenance"]["source_refs"]))
			notes = switch["physical"]["notes"]
			self.assertIn(f'print this address as "{printed}"', notes)
			self.assertIn(ROM_NAMES[address], notes)
			self.assertTrue(switch["normally_closed"])
		for address in OPTO_ADDRESSES - {84, 85}:
			self.assertFalse(set(SWITCH_EDGES_SOURCES.values()) & set(self.switches[address]["provenance"]["source_refs"]), address)
		# Public 31 mirrors WPC_GILAMPS bit 7, which the ROM drives in step with its flipper enable.
		solenoid = self.solenoids[31]
		self.assertEqual("used", solenoid["availability"])
		self.assertEqual("virtual", solenoid["kind"])
		self.assertIn(FLIPPER_ENABLE_SOURCE, solenoid["provenance"]["source_refs"])
		self.assertIn("FastFlips.TiltSol", solenoid["physical"]["notes"])
		self.assertIn("third plumb-bob tilt pulse", solenoid["physical"]["notes"])
		for address in (29, 30):
			self.assertNotIn(FLIPPER_ENABLE_SOURCE, self.solenoids[address]["provenance"]["source_refs"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_gw_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for driver_id in DRIVER_IDS - {"gw_l5"}:
			self.assertEqual("gw_l5", by_id[driver_id]["clone_of"], driver_id)
		self.assertNotIn("clone_of", by_id["gw_l5"])

	def test_the_full_wpc_fliptronic_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {23}):
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual("optional", self.switches[23]["availability"])

	def test_printed_opto_polarity_matches_pinmames_inverted_switch_mask_exactly(self) -> None:
		# gwGameData's mask ({...,0x1f,0x00,0x00,0x00}) sets column 8 bits 0-4 (rows 1-5): exactly
		# addresses 81-85. Every other switch must not be normally_closed=True.
		mask = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00)
		self.assertEqual(0x1f, mask[8])
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_switches_with_no_vpx_geometry_have_no_spatial_key(self) -> None:
		for address in (33, 34, 56, 57, 58):
			self.assertNotIn("spatial", self.switches[address], address)
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_upper_left_flipper_is_confirmed_unfitted_by_three_independent_sources(self) -> None:
		for address in (111, 112, 113, 114, 115, 116):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		description = self.switches[117]["physical"]["notes"]
		self.assertIn("NOT USED", description)
		self.assertIn("Black/Blue(NU)", description)
		self.assertIn("A-15205-L", description)

	def test_the_full_wpc_fliptronic_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 29)) | {33, 34, 35, 36, 45, 46, 47, 48} | {29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(17, 25):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (25, 26, 27, 28):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_flipper_coil_solenoids_match_the_switch_fitment(self) -> None:
		for address in (33, 34, 45, 46, 47, 48):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
			self.assertEqual("coil", self.solenoids[address]["kind"], address)
		for address in (35, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)

	def test_driver_guessed_slingshot_solenoid_labels_are_corrected_by_the_manual(self) -> None:
		left = self.solenoids[5]
		right = self.solenoids[6]
		self.assertEqual("Left Slingshot", left["label"])
		self.assertEqual("Right Slingshot", right["label"])
		self.assertIn("sRSling", left["physical"]["notes"])
		self.assertIn("guessed", left["physical"]["notes"])

	def test_solenoid_27_is_backbox_and_solenoid_7_is_cabinet(self) -> None:
		mars_lamp = self.solenoids[27]
		self.assertEqual("Revolving Lamp", mars_lamp["label"])
		self.assertEqual("not_applicable", mars_lamp["spatial"]["status"])
		self.assertEqual("cabinet_or_service", mars_lamp["spatial"]["reason"])
		self.assertIn("Mars Lamp", mars_lamp["physical"]["notes"])
		knocker = self.solenoids[7]
		self.assertEqual("not_applicable", knocker["spatial"]["status"])
		self.assertEqual("cabinet_or_service", knocker["spatial"]["reason"])

	def test_solenoids_with_no_confirmed_vpx_object_have_no_spatial_key(self) -> None:
		for address in (1, 25, 26, 28):
			self.assertNotIn("spatial", self.solenoids[address], address)
			self.assertEqual("used", self.solenoids[address]["availability"], address)

	def test_gi_playfield_strings_are_undifferentiated_and_backbox_strings_are_cabinet(self) -> None:
		for address in (0, 1):
			self.assertNotIn("spatial", self.gi[address], address)
			self.assertEqual(["playfield.gi"], self.gi[address]["roles"], address)
		for address in (2, 3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamp_quantities_and_stop_light_gap_are_explicit(self) -> None:
		doubled = {16, 18, 35, 63, 64, 65}
		for address in doubled:
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in sorted(MATRIX_ADDRESSES - doubled - {68, 73, 74, 75}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		self.assertEqual("not_applicable", self.lamps[68]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[68]["spatial"]["reason"])
		for address in (73, 74, 75):
			self.assertNotIn("spatial", self.lamps[address], address)

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
		self.assertEqual(located, report["placement_count"])
		self.assertEqual("partial", report["status"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		lamp_pos = _positions(self.lamps)
		# Freeway loops: left is left of right on both switches and lamps.
		self.assertLess(switch_pos[15][0], switch_pos[17][0])
		self.assertLess(switch_pos[16][0], switch_pos[18][0])
		# Outlanes are outboard of return lanes on both sides.
		self.assertLess(switch_pos[25][0], switch_pos[26][0])
		self.assertGreater(switch_pos[28][0], switch_pos[27][0])
		# Right bank targets ascend bottom(44) -> middle(45) -> top(46) in y (top has smaller y).
		self.assertGreater(switch_pos[44][1], switch_pos[45][1])
		self.assertGreater(switch_pos[45][1], switch_pos[46][1])
		# Left bank targets: same ascending pattern for 86/87/88.
		self.assertGreater(switch_pos[86][1], switch_pos[87][1])
		self.assertGreater(switch_pos[87][1], switch_pos[88][1])
		# Lock ladder: top (74) has the smallest y, bottom (76) the largest.
		self.assertLess(switch_pos[74][1], switch_pos[75][1])
		self.assertLess(switch_pos[75][1], switch_pos[76][1])
		# Left slingshot switch is left of right slingshot switch.
		self.assertLess(switch_pos[31][0], switch_pos[32][0])
		# Lamp side check: Left Return Lane (62) is left of Right Return Lane (61).
		self.assertLess(lamp_pos[62][0], lamp_pos[61][0])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.supercharger-loop", "mechanism.supercharger-diverter", "mechanism.ramp-lift",
				"mechanism.ball-lock", "mechanism.kickback", "mechanism.trough", "mechanism.shooter-lane",
				"mechanism.slingshots", "mechanism.jet-bumpers", "mechanism.eject-hole",
				"mechanism.gear-shifter", "mechanism.lower-flippers", "mechanism.upper-right-flipper",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)
		diverter = mechanisms["mechanism.supercharger-diverter"]
		self.assertIn("84 ENTER LEFT RAMP and 85 OPTO MADE LOOP", diverter["behavior"])
		self.assertLessEqual(set(SWITCH_EDGES_SOURCES.values()), set(diverter["provenance"]["source_refs"]))

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
		self.assertIn("vpx-script.gw-v1.2", sources)
		self.assertTrue(sources["vpx-script.gw-v1.2"]["known_working"])
		self.assertEqual(
			"4f91dbf71bf134b1113939a517900c27d87fa1a142109e79ad64306a40aeb78e",
			sources["vpx-script.gw-v1.2"]["sha256"],
		)
		self.assertEqual(
			"22e7257316dcb3c414f62a0543f6a68063e8f50524ad9559f1ff98bd38184efc",
			sources["vpx-table.gw-v1.2"]["sha256"],
		)
		runtime = {source["id"]: source for source in self.definition["sources"] if source["kind"] == "runtime_scenario"}
		self.assertEqual(set(SWITCH_EDGES_SOURCES.values()) | {FLIPPER_ENABLE_SOURCE}, set(runtime))
		for game, source_id in SWITCH_EDGES_SOURCES.items():
			self.assertEqual(f"internal:evidence/runtime/wpc-fliptronic/getaway-{game}-switch-edges.json", runtime[source_id]["uri"])
		self.assertEqual(
			"internal:evidence/runtime/wpc-fliptronic/getaway-gw_l5-flipper-enable-31.json",
			runtime[FLIPPER_ENABLE_SOURCE]["uri"],
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
		self.assertEqual("pinmame.wpc-fliptronic", profile["id"])
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


class GetawayRuntimeEvidenceTests(unittest.TestCase):
	"""The compact runtime summaries are tied to their scenarios here and to the raw runs when retained."""

	def _common(self, evidence: dict[str, object], game: str, scenario: Path) -> dict[str, object]:
		import hashlib

		self.assertNotIn("game", load_json(scenario))
		self.assertEqual(game, evidence["runtime"]["game"])
		self.assertEqual([game], evidence["driver_ids"])
		self.assertEqual(["williams.the-getaway-high-speed-ii.1992"], evidence["machine_ids"])
		self.assertEqual(PINNED_LIBRARY_SHA256, evidence["runtime"]["emulator"]["sha256"])
		(raw,) = evidence["runtime"]["raw_runs"]
		self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), raw["scenario_sha256"])
		self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
		self.assertEqual(scenario.relative_to(ROOT).as_posix(), raw["scenario_path"])
		return raw

	def test_switch_edges_name_84_enter_left_ramp_and_85_opto_made_loop_on_both_roms(self) -> None:
		edge_frames: dict[str, list[str]] = {}
		rom_hashes = set()
		for game in SWITCH_EDGES_SOURCES:
			with self.subTest(game=game):
				evidence = load_json(RUNTIME_DIR / f"getaway-{game}-switch-edges.json")
				raw = self._common(evidence, game, EDGES_SCENARIO)
				rom_hashes.add(evidence["runtime"]["rom_archive_sha256"])
				observations = evidence["runtime"]["observations"]["named_action_observations"]
				self.assertEqual(EDGE_SEQUENCE, [item["input_address"] for item in observations])
				snapshots = evidence["runtime"]["observations"]["diagnostic_snapshots"]
				self.assertEqual(16, len(snapshots))
				self.assertEqual(GAME_IDENTIFICATION[game], snapshots[0]["interpreted_text"])
				self.assertEqual("SWITCH EDGES / T.1", snapshots[1]["interpreted_text"])
				by_level: dict[tuple[int, int], set[str]] = {}
				for snapshot, item in zip(snapshots[2:], observations, strict=True):
					address = item["input_address"]
					state = 1 if item["host_stimulus_switch_addresses"] else 0
					self.assertEqual([], item["observed_switch_addresses"])
					self.assertEqual([], item["transitioned_solenoid_addresses"])
					self.assertIn(f"public {address} (", snapshot["label"])
					self.assertIn(f"was set to {state}", snapshot["label"])
					top = ROM_NAMES[address] if state else "SWITCH EDGES"
					self.assertTrue(snapshot["interpreted_text"].startswith(f"{top} / T.1 LAST SW {address} / "), snapshot["label"])
					if state:
						self.assertIn(f"names it {ROM_NAMES[address]}", item["label"])
					by_level.setdefault((address, state), set()).add(snapshot["pixel_sha256"])
				for key, hashes in by_level.items():
					# A repeated level draws the identical frame; a menu left blinking would not.
					self.assertEqual(1, len(hashes), key)
				for address in ROM_NAMES:
					self.assertTrue(by_level[(address, 1)].isdisjoint(by_level[(address, 0)]), address)
				edge_frames[game] = [snapshot["pixel_sha256"] for snapshot in snapshots[1:]]
				self._check_retained_edges(game, raw, snapshots)
		self.assertEqual(2, len(rom_hashes))
		# L-5 and L-1 draw identical T.1 pages for every edge.
		self.assertEqual(edge_frames["gw_l5"], edge_frames["gw_l1"])

	def test_public_31_follows_the_roms_flipper_enable(self) -> None:
		evidence = load_json(RUNTIME_DIR / "getaway-gw_l5-flipper-enable-31.json")
		raw = self._common(evidence, "gw_l5", PLAY_SCENARIO)
		observations = evidence["runtime"]["observations"]
		actions = observations["named_action_observations"]
		self.assertEqual([112, 112, 14, 112, 112], [item["input_address"] for item in actions])
		attract, ball_one, tilt, tilted, ball_two = actions
		for item in (attract, tilted):
			self.assertEqual([], item["transitioned_solenoid_addresses"])
			self.assertEqual("no_matching_transition", item["result"])
			self.assertNotIn(31, item["active_solenoid_addresses"])
		for item in (ball_one, ball_two):
			self.assertLessEqual({45, 46}, set(item["transitioned_solenoid_addresses"]))
			self.assertIn(31, item["active_solenoid_addresses"])
			self.assertIn(46, item["active_solenoid_addresses"])
		self.assertEqual([25, 26, 28, 31], tilt["transitioned_solenoid_addresses"])
		self.assertEqual([], tilt["active_solenoid_addresses"])
		sequence = observations["ordered_solenoid_on_sequence"]
		# Every flipper pulse comes after 31 has risen.
		self.assertLess(sequence.index(31), sequence.index(45))
		self.assertEqual(2, sequence.count(31))
		self.assertEqual(2, sequence.count(45))
		self._check_retained_play(raw, observations)

	def _retained(self, raw: dict[str, object], game: str) -> dict[str, object] | None:
		import hashlib

		import build_external_evidence_manifest as manifest

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return None
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		manifest.check_manifest(path.parent, game)
		run = load_json(path)
		self.assertIsNone(run["failure"])
		self.assertEqual(game, run["game"])
		self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
		self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
		return run

	def _check_retained_edges(self, game: str, raw: dict[str, object], snapshots: list[dict[str, object]]) -> None:
		run = self._retained(raw, game)
		if run is None:
			return
		raw_frames = []
		for snap in run["snapshots"]:
			if snap["label"] in {"Enter 2 (game identification)", "Enter 5 (start T.1)"} or " -> " in snap["label"]:
				raw_frames.append((snap["displays"][0]["pixel_sha256"], snap["displays"][0]["nonzero_pixels"]))
			if " -> " not in snap["label"]:
				continue
			address, state = (int(part.split()[0]) for part in snap["label"].split(" -> "))
			levels = {w["number"]: w["state"] for w in snap["watched_switches"]}
			self.assertEqual({45: 0, 81: 0, 84: 0, 85: 0} | {address: state}, {a: levels[a] for a in (45, 81, 84, 85)}, snap["label"])
		# Every summary snapshot is the raw frame of the step it names, in order.
		self.assertEqual(raw_frames, [(item["pixel_sha256"], item["nonzero_pixels"]) for item in snapshots])

	def _check_retained_play(self, raw: dict[str, object], observations: dict[str, object]) -> None:
		run = self._retained(raw, "gw_l5")
		if run is None:
			return
		events = [e for e in run["events"] if e["event"] == "solenoid"]
		self.assertEqual(observations["ordered_solenoid_on_sequence"], [e["number"] for e in events if e["state"]])
		transitions = [(e["time_s"], e["state"]) for e in events if e["number"] == 31]
		self.assertEqual([(46.641, 1), (57.125, 0), (63.188, 1)], transitions)
		# The ROM fires the flipper windings only while public 31 is high.
		for event in events:
			if event["number"] in {45, 46} and event["state"]:
				self.assertTrue(46.641 < event["time_s"] < 57.125 or event["time_s"] > 63.188, event)
		snaps = {snap["label"]: snap for snap in run["snapshots"]}
		for item in observations["diagnostic_snapshots"]:
			self.assertIn(item["pixel_sha256"], {display["pixel_sha256"] for snap in run["snapshots"] for display in snap["displays"]})
		self.assertNotIn(31, snaps["right flipper button in attract mode (held)"]["active_solenoids"])
		self.assertNotIn(31, snaps["right flipper button after the tilt (held)"]["active_solenoids"])


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class GetawayCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_getaway as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_getaway as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_getaway as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"The Getaway", b"The Getawoy", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_getaway as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class GetawayRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_getaway as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_getaway as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/the-getaway-high-speed-ii-1992/source/Getaway, The - High Speed II v1.2.vpx"
		script = source_root / "williams/the-getaway-high-speed-ii-1992/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_getaway as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "getaway" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
