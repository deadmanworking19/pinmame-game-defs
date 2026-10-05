from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


from scratch_repository import copy_curator_files
from test_excerpts import DRAWING_LIMIT, IMAGE_LIMIT, PAGE_SCALE_DRAWINGS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "junkyard-1996.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "junkyard-1996.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "junkyard-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "junkyard-1996.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "junkyard-1996.json"

DRIVER_IDS = {"jy_12", "jy_12c", "jy_11", "jy_03"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {23, 25, 55, 75, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44}
RUNTIME_SOURCES = {
	"jy_12": "runtime.junkyard.jy-12.switch-edges",
	"jy_11": "runtime.junkyard.jy-11.switch-edges",
	"jy_03": "runtime.junkyard.jy-03.switch-edges",
}
PINNED_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"


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
	import curate_junkyard as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_junkyard.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class JunkyardDefinitionTests(unittest.TestCase):
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
			["spatial_placement", "unresolved_conflicts"],
			self.definition["coverage"]["missing"],
		)
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			self.assertIn(state, {"validated", "not_applicable", "candidate", "conflicted"}, dimension)
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("williams.junkyard.1996", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1996, self.definition["machine"]["year"])
		self.assertEqual("16-50052-101", self.definition["machine"]["model_number"])
		self.assertEqual(952.0, self.definition["machine"]["playfield"]["width"])
		self.assertEqual(2162.0, self.definition["machine"]["playfield"]["height"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertEqual(1, len(self.definition["conflicts"]))

	def test_the_stale_author_ready_artifact_is_gone_and_the_stub_is_superseded(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertFalse((ROOT / "machines" / "stubs" / "jy_12.json").exists())

	def test_every_junkyard_driver_is_claimed_exactly_once(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["jy_12"])
		for driver_id in ("jy_12c", "jy_11", "jy_03"):
			self.assertEqual("jy_12", by_id[driver_id]["clone_of"])
		self.assertEqual("identical", by_id["jy_11"]["physical_compatibility"])
		self.assertEqual("identical", by_id["jy_03"]["physical_compatibility"])
		self.assertEqual("compatible", by_id["jy_12c"]["physical_compatibility"])

	def test_the_full_wpc95_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_only_the_masked_optos_rest_closed(self) -> None:
		# A masked opto the ROM reads active at public 1 rests closed; the unmasked opto 44, which the
		# ROM's T.1 SWITCH EDGES test also reads active at public 1, rests open like an ordinary switch.
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES - {44}, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_the_inverted_switch_mask_normalizes_31_37_and_41_43_but_not_44(self) -> None:
		# jyGameData's inverted-switch mask: column 3 = 0x7f (rows 1-7 = 31-37), column 4 = 0x07
		# (rows 1-3 = 41-43). Re-derive in code; switch 44 (Past Crane) is the one opto the mask
		# does not cover, and the ROM's own switch-edges test shows that needs no inversion.
		mask = (0x00, 0x00, 0x00, 0x7f, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		normalized = set()
		for column in range(1, 9):
			for row in range(1, 9):
				if (mask[column] >> (row - 1)) & 1:
					normalized.add(column * 10 + row)
		self.assertEqual({31, 32, 33, 34, 35, 36, 37, 41, 42, 43}, normalized)
		self.assertNotIn(44, normalized)
		self.assertEqual(OPTO_ADDRESSES - normalized, {44})
		self.assertEqual("opto", self.switches[44]["physical"]["switch_type"])
		self.assertEqual("A-16908 (LED) / A-16909 (PHOTO TRANS)", self.switches[44]["physical"]["part_number"])

	def test_the_past_crane_conflict_is_withdrawn_on_the_roms_switch_edges_test(self) -> None:
		(lamp_conflict,) = self.definition["conflicts"]
		self.assertEqual("conflict.junkyard.lamp-86-plane", lamp_conflict["id"])
		self.assertEqual("unresolved", lamp_conflict["status"])
		self.assertIn("Resolution path:", lamp_conflict["description"])
		switch = self.switches[44]
		self.assertFalse(switch["normally_closed"])
		self.assertEqual("validated", switch["provenance"]["status"])
		self.assertLessEqual(set(RUNTIME_SOURCES.values()), set(switch["provenance"]["source_refs"]))
		notes = switch["physical"]["notes"]
		self.assertIn("T.1 SWITCH EDGES", notes)
		self.assertIn("never inverts it", notes)
		self.assertIn("normally_closed is false", notes)
		sources = {source["id"]: source for source in self.definition["sources"]}
		for game, source_id in RUNTIME_SOURCES.items():
			self.assertEqual("runtime_scenario", sources[source_id]["kind"], game)
			self.assertEqual(f"internal:evidence/runtime/wpc-95/junkyard-{game}-switch-edges.json", sources[source_id]["uri"])
		for address in OPTO_ADDRESSES - {44}:
			self.assertFalse(set(RUNTIME_SOURCES.values()) & set(self.switches[address]["provenance"]["source_refs"]), address)

	def test_switch_edges_evidence_shows_44_active_at_public_one_like_its_controls(self) -> None:
		import hashlib

		scenario = ROOT / "tools" / "harness-scenarios" / "wpc-95" / "jy-switch-edges-44.json"
		self.assertNotIn("game", load_json(scenario))
		scenario_sha256 = hashlib.sha256(scenario.read_bytes()).hexdigest()
		rom_hashes = set()
		edge_frames: dict[str, list[str]] = {}
		for game in RUNTIME_SOURCES:
			with self.subTest(game=game):
				evidence = load_json(ROOT / "evidence" / "runtime" / "wpc-95" / f"junkyard-{game}-switch-edges.json")
				self.assertEqual(game, evidence["runtime"]["game"])
				self.assertEqual([game], evidence["driver_ids"])
				self.assertEqual(["williams.junkyard.1996"], evidence["machine_ids"])
				self.assertEqual(PINNED_LIBRARY_SHA256, evidence["runtime"]["emulator"]["sha256"])
				rom_hashes.add(evidence["runtime"]["rom_archive_sha256"])
				(raw,) = evidence["runtime"]["raw_runs"]
				self.assertEqual(scenario_sha256, raw["scenario_sha256"])
				self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
				observations = evidence["runtime"]["observations"]["named_action_observations"]
				self.assertEqual([45, 45, 41, 41, 44, 44, 44, 44, 45, 45], [item["input_address"] for item in observations])
				for item in observations:
					# Host-written levels are stimulus, never ROM observations.
					self.assertEqual([], item["observed_switch_addresses"])
					address = item["input_address"]
					if item["host_stimulus_switch_addresses"]:
						self.assertEqual([address], item["host_stimulus_switch_addresses"])
						self.assertIn(f"reads public {address} = 1 as active", item["label"])
					else:
						self.assertIn("returns to SWITCH EDGES", item["label"])
				snapshots = evidence["runtime"]["observations"]["diagnostic_snapshots"]
				self.assertEqual(12, len(snapshots))
				self.assertTrue(snapshots[0]["interpreted_text"].startswith("JUNK YARD / 50052 REV."))
				self.assertEqual("SWITCH EDGES / T.1", snapshots[1]["interpreted_text"])
				by_level: dict[tuple[int, int], set[str]] = {}
				for snapshot, item in zip(snapshots[2:], observations, strict=True):
					address = item["input_address"]
					state = 1 if item["host_stimulus_switch_addresses"] else 0
					self.assertIn(f"public {address} (", snapshot["label"])
					self.assertIn(f"was set to {state}", snapshot["label"])
					top = {45: "RAMP EXIT", 41: "PAST SPINNER", 44: "PAST CRANE"}[address] if state else "SWITCH EDGES"
					self.assertTrue(snapshot["interpreted_text"].startswith(f"{top} / T.1 LAST SW {address} / "), snapshot["label"])
					by_level.setdefault((address, state), set()).add(snapshot["pixel_sha256"])
				for key, hashes in by_level.items():
					# A repeated level draws the identical frame; a menu left blinking would not.
					self.assertEqual(1, len(hashes), key)
				for address in (41, 44, 45):
					self.assertTrue(by_level[(address, 1)].isdisjoint(by_level[(address, 0)]), address)
				edge_frames[game] = [snapshot["pixel_sha256"] for snapshot in snapshots[1:]]
				self._check_retained_run(game, raw, snapshots)
		self.assertEqual(3, len(rom_hashes))
		# The two production ROMs print identical T.1 pages; the prototype's wire caption differs.
		self.assertEqual(edge_frames["jy_12"], edge_frames["jy_11"])
		self.assertTrue(set(edge_frames["jy_03"][1:]).isdisjoint(edge_frames["jy_12"][1:]))

	def _check_retained_run(self, game: str, raw: dict[str, object], snapshots: list[dict[str, object]]) -> None:
		import hashlib

		import build_external_evidence_manifest as manifest

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		# The canonical directory manifest covers the raw trace, scenario copy, DMD frames and state.
		digest = manifest.check_manifest(path.parent, game)
		self.assertIn(f"{game}/manifest.json SHA-256 {digest}", load_json(ROOT / "evidence" / "runtime" / "wpc-95" / f"junkyard-{game}-switch-edges.json")["source"]["attribution"])
		run = load_json(path)
		self.assertIsNone(run["failure"])
		self.assertEqual(game, run["game"])
		self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
		self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
		raw_frames = []
		for snap in run["snapshots"]:
			if snap["label"] in {"Enter 1 (game identification)", "Enter 4 (start T.1)"} or " -> " in snap["label"]:
				raw_frames.append((snap["displays"][0]["pixel_sha256"], snap["displays"][0]["nonzero_pixels"]))
			if " -> " not in snap["label"]:
				continue
			address, state = (int(part.split()[0]) for part in snap["label"].split(" -> "))
			levels = {w["number"]: w["state"] for w in snap["watched_switches"]}
			self.assertEqual({41: 0, 44: 0, 45: 0} | {address: state}, {a: levels[a] for a in (41, 44, 45)}, snap["label"])
		# Every summary snapshot is the raw frame of the step it names, in order.
		self.assertEqual(raw_frames, [(item["pixel_sha256"], item["nonzero_pixels"]) for item in snapshots])

	def test_flipper_positions_lower_fitted_upper_unfitted_spinner_on_f5(self) -> None:
		for address in (111, 112, 113, 114, 115):
			self.assertEqual("used", self.switches[address]["availability"], address)
		# 116/118 (upper-right/left buttons) and 117 (upper-left EOS) are all unfitted; under
		# LibPinMAME the button bits round-trip unchanged and the upper EOS has no FLIP_EOS bit,
		# so none publishes meaningful emulator state and all are unused.
		for address in (116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		# The lower EOS contacts 111/113 are forced every VBLANK by PinMAME (recomputed from
		# core_getSol + CORE_FLIPSTROKETIME), so a recreation must not drive them.
		for address in (111, 113):
			self.assertIn("must not drive", self.switches[address]["physical"]["notes"])
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		# F5 is a playfield spinner, not a flipper contact.
		self.assertEqual("Spinner", self.switches[115]["label"])
		self.assertEqual("playfield.spinner", self.switches[115]["roles"][0])
		self.assertFalse(self.switches[115]["normally_closed"])
		self.assertIn("spatial", self.switches[115])

	def test_the_full_wpc95_output_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		# Flashers 17-20, 22-28 (with 18 a backbox flasher).
		for address in (17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (29, 30, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		self.assertEqual("used", self.solenoids[31]["availability"])

	def test_unfitted_solenoids_are_honestly_enumerated_not_created(self) -> None:
		# 4, 8, 12, 13, 14 are printed NOT USED; 33-36 are upper-flipper circuits that are not fitted.
		for address in (4, 8, 12, 13, 14):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)
			self.assertIn("NOT USED", self.solenoids[address]["physical"]["notes"])
		for address in (33, 34, 35, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertIn("not fitted", self.solenoids[address]["physical"]["notes"])

	def test_flipper_manual_address_mapping(self) -> None:
		manual_aliases = {
			address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			for address in (45, 46, 47, 48)
		}
		self.assertEqual({"29"}, manual_aliases[45])
		self.assertEqual({"30"}, manual_aliases[46])
		self.assertEqual({"31"}, manual_aliases[47])
		self.assertEqual({"32"}, manual_aliases[48])
		self.assertEqual("Lower Right Flipper Power", self.solenoids[45]["label"])
		self.assertEqual("Lower Right Flipper Hold", self.solenoids[46]["label"])
		self.assertEqual("Lower Left Flipper Power", self.solenoids[47]["label"])
		self.assertEqual("Lower Left Flipper Hold", self.solenoids[48]["label"])

	def test_knocker_is_a_cabinet_service_coil(self) -> None:
		self.assertEqual("coil", self.solenoids[7]["kind"])
		self.assertEqual(["cabinet.knocker"], self.solenoids[7]["roles"])
		self.assertEqual("not_applicable", self.solenoids[7]["spatial"]["status"])

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_cabinet(self) -> None:
		for address in (0, 1):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(self.gi[address]["spatial"]["placements"]), address)
		self.assertEqual(28, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(4, len(self.gi[1]["spatial"]["placements"]))
		for address in (2, 3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamp_labels_and_insert_panel_lamps(self) -> None:
		self.assertEqual("Top Left Bank Bottom", self.lamps[11]["label"])
		self.assertEqual("Jackpot", self.lamps[31]["label"])
		self.assertEqual("DO(G)", self.lamps[63]["label"])
		self.assertEqual("Not Used Lamp Position 56", self.lamps[56]["label"])
		self.assertEqual("unused", self.lamps[56]["availability"])
		self.assertEqual("unused", self.lamps[87]["availability"])
		for address in (81, 82, 83, 84, 85):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		# Lamp 86 (Gen. Crane) is placed on the playfield from the retained table, with its
		# manual insert-panel-vs-playfield contradiction recorded as a conflict.
		self.assertEqual("validated", self.lamps[86]["spatial"]["status"])
		self.assertIn("conflict.junkyard.lamp-86-plane", self.lamps[86]["physical"]["notes"])
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])

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
		self.assertEqual("validated", report["status"])
		self.assertEqual([28, 42], report["unresolved_input_addresses"])
		self.assertEqual(located, report["placement_count"])

	def test_unresolved_switches_omit_spatial_rather_than_place_off_apron(self) -> None:
		# Switch 28 (Crane Down) and 42 (In The Sewer) have only off-apron objects (y > 1).
		self.assertNotIn("spatial", self.switches[28])
		self.assertNotIn("spatial", self.switches[42])

	def test_no_flasher_claims_internal_nonvisual_and_unplaced_outputs_are_listed(self) -> None:
		# A device with no coordinate must omit spatial (and be listed in the report's unresolved
		# output bindings), never be labelled "internal_nonvisual", which would falsely assert it
		# has no visible location. Regression guard for the removed catch-all fallback.
		report = load_json(SPATIAL_REPORT_PATH)
		unresolved = {b["address"] for b in report["unresolved_output_bindings"]}
		for device in self.definition["outputs"]:
			if device["binding"]["group"] != "pinmame.output.solenoid":
				continue
			spatial = device.get("spatial")
			self.assertNotEqual(
				"internal_nonvisual",
				spatial.get("reason") if spatial else None,
				device["id"],
			)
			if device["kind"] == "flasher" and device["availability"] == "used":
				if spatial is None:
					self.assertIn(device["binding"]["device"], unresolved, device["id"])
				elif spatial["status"] == "not_applicable":
					self.assertEqual("cabinet_or_service", spatial["reason"], device["id"])
				else:
					self.assertEqual("validated", spatial["status"], device["id"])
		# The hold-crane coil (15) and the genuinely unbound flashers 25/27/28 are unresolved.
		for address in (15, 25, 27, 28):
			self.assertIn(address, unresolved)
		# The backbox-only flasher 18 and knocker 7 are cabinet_or_service, not unresolved.
		self.assertNotIn(18, unresolved)
		self.assertNotIn(7, unresolved)
		# The script-bound flashers 19/20/23/24/26 and the scoop/crane coils are placed.
		for address in (5, 19, 20, 21, 23, 24, 26):
			self.assertEqual("validated", self.solenoids[address]["spatial"]["status"], address)
		# The lower flipper coils are placed at the flipper assemblies.
		for address in (45, 46, 47, 48):
			self.assertEqual("validated", self.solenoids[address]["spatial"]["status"], address)

	def test_scoop_coils_are_at_the_scoop_mechanism_not_the_top_left_lane(self) -> None:
		# Solenoids 5 (Scoop Down) and 21 (Scoop Up) must sit at the scoop mechanism beside their own
		# sensors (switch 73), not at the top-left lane switch 44, whose position once leaked into this slot.
		scoop_73 = self.switches[73]["spatial"]["placements"][0]
		lane_44 = self.switches[44]["spatial"]["placements"][0]
		for address in (5, 21):
			placement = self.solenoids[address]["spatial"]["placements"][0]
			dx = abs(placement["x"] - scoop_73["x"])
			dy = abs(placement["y"] - scoop_73["y"])
			self.assertLess(dx, 0.15, address)
			self.assertLess(dy, 0.15, address)
			self.assertGreater(abs(placement["x"] - lane_44["x"]), 0.3, address)

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		# Slingshots: left is left of right.
		self.assertLess(switch_pos[51][0], switch_pos[52][0])
		# Lower Left 3-bank top/middle/bottom descend the playfield (ascending y).
		self.assertLess(switch_pos[58][1], switch_pos[57][1])
		self.assertLess(switch_pos[57][1], switch_pos[56][1])
		# Upper Right 3-bank top/middle/bottom.
		self.assertLess(switch_pos[63][1], switch_pos[62][1])
		self.assertLess(switch_pos[62][1], switch_pos[61][1])
		# Car targets ascend left -> right.
		self.assertLess(switch_pos[46][0], switch_pos[47][0])
		self.assertLess(switch_pos[47][0], switch_pos[48][0])
		# Outlanes are on the outer edges of return lanes.
		self.assertLess(switch_pos[16][0], switch_pos[17][0])
		self.assertLess(switch_pos[26][0], switch_pos[27][0])

	def test_mechanism_inventory_covers_every_used_coil(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.crane",
				"mechanism.refrigerator-popper", "mechanism.bus-diverter", "mechanism.dog",
				"mechanism.scoop", "mechanism.toaster-gun",
				"mechanism.three-banks", "mechanism.slingshots", "mechanism.spinner",
				"mechanism.lower-flippers",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		owners: dict[str, str] = {}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owners, actuator)
				owners[actuator] = mechanism["id"]
		# Every fitted physical coil/motor is owned by a mechanism (the knocker is a cabinet
		# service coil, not a documented mechanism).
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"} and device["availability"] == "used"
			and "cabinet.knocker" not in device.get("roles", [])
		}
		self.assertEqual(set(), physical - set(owners))

	def test_crane_is_the_arm_switch_and_the_wrecking_ball_target_arc(self) -> None:
		# The Moving Crane Assembly (2-20) carries switch 28's micro mini switch and the one A-20099
		# coil; the Wreck Ball Target Assembly (2-29) wires exactly the five car targets. The arm only
		# lifts and drops, so 15/38 (red standup targets) and 44 (a lane switch) are not its sensors.
		crane = {item["id"]: item for item in self.definition["mechanisms"]}["mechanism.crane"]
		arc = {"switch.matrix-46", "switch.matrix-47", "switch.matrix-48", "switch.matrix-53", "switch.matrix-54"}
		self.assertEqual("toy", crane["kind"])
		self.assertEqual(["device.power-crane", "device.hold-crane"], crane["actuators"])
		self.assertEqual({"switch.matrix-28"} | arc, set(crane["sensors"]))
		positions = {position["id"]: position for position in crane["positions"]}
		self.assertEqual(["switch.matrix-28"], positions["down"]["sensors"])
		self.assertEqual(["switch.matrix-28"], positions["up"]["sensors"])
		self.assertEqual(arc, {sensor for key, position in positions.items() if key.startswith("swing-") for sensor in position["sensors"]})
		sensed = {sensor for mechanism in self.definition["mechanisms"] for sensor in mechanism["sensors"]}
		for address in (15, 38, 44):
			self.assertNotIn(f"switch.matrix-{address}", sensed, address)
			self.assertIn("not a crane position switch", self.switches[address]["physical"]["notes"], address)
		for address in (15, 38):
			self.assertEqual("A-18530-4", self.switches[address]["physical"]["part_number"], address)
			self.assertIn("Red Standup Target", self.switches[address]["physical"]["notes"], address)
		self.assertEqual("5647-12693-31", self.switches[28]["physical"]["part_number"])
		self.assertIn("Moving Crane Assembly A-21523", self.switches[28]["physical"]["notes"])
		for address in (46, 47, 48, 53, 54):
			self.assertIn("Wreck Ball Target Assembly A-21247", self.switches[address]["physical"]["notes"], address)
		# The Power Crane coil sits at the crane arm's mount, not at the CraneHole kickout far top left.
		(placement,) = self.solenoids[3]["spatial"]["placements"]
		self.assertEqual((0.539391, 0.038179), (placement["x"], placement["y"]))
		self.assertIn("PCraneArm", self.solenoids[3]["physical"]["notes"])
		excerpts = {
			excerpt["id"]
			for source in self.definition["sources"]
			for excerpt in source.get("excerpts", [])
		}
		for name in (
			"wrecking-ball-back-panel-parts", "wreck-ball-target-assembly", "upper-playfield-parts",
			"upper-playfield-parts-drawing", "switch-locations-crane-area",
		):
			self.assertIn(f"excerpt-junkyard.{name}", excerpts)

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual(
			{"relationship.trough-eject-opto", "relationship.scoop-down-sets-scoop-down-switch", "relationship.scoop-up-clears-scoop-down-switch"},
			set(relationships),
		)
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
		self.assertIn("vpx-script.junkyard-mfuegemann", sources)
		self.assertTrue(sources["vpx-script.junkyard-mfuegemann"]["known_working"])
		self.assertEqual(
			"b583aed396fea3cf6e2f862fdb51989aa01a99e624bbae8b30e8aeba7eeb4033",
			sources["vpx-script.junkyard-mfuegemann"]["sha256"],
		)
		self.assertEqual(
			"8ff2c1c8ae3457a4b88ff2207bc506d07435b049343301ded4dbf8e855bef07f",
			sources["vpx-table.junkyard-mfuegemann"]["sha256"],
		)
		self.assertEqual(
			"08819a08990c61070c4a3a99a4d5f00d9d082b6d00477ffaf9b0a58fddce3fe1",
			sources["manual.williams.junkyard.1996"]["sha256"],
		)
		runtime = {source["id"] for source in self.definition["sources"] if source["kind"] == "runtime_scenario"}
		self.assertEqual(set(RUNTIME_SOURCES.values()), runtime)
		for source in self.definition["sources"]:
			self.assertNotEqual("rom_static_analysis", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("l:\\", value.lower())
					self.assertNotIn("l:/", value.lower())

	def test_manual_source_excerpts_exist_and_hash_match(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.williams.junkyard.1996"]
		self.assertGreaterEqual(len(manual["excerpts"]), 6)
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file(), excerpt["path"])
			import hashlib

			digest = hashlib.sha256(path.read_bytes()).hexdigest()
			self.assertEqual(excerpt["sha256"], digest, excerpt["id"])
			# Vision-worker transcriptions stay unreviewed until a curator checks them; the crane-page
			# excerpts were read by the curator from the native render.
			self.assertEqual(excerpt["method"] == "manual", excerpt["reviewed"], excerpt["id"])
			if "image" in excerpt:
				image_path = ROOT / excerpt["image"]
				self.assertTrue(image_path.is_file(), excerpt["image"])
				image_digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
				self.assertEqual(excerpt["image_sha256"], image_digest, excerpt["id"])
				limit = DRAWING_LIMIT if excerpt["id"] in PAGE_SCALE_DRAWINGS else IMAGE_LIMIT
				self.assertLessEqual(image_path.stat().st_size, limit, excerpt["id"])

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


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class JunkyardCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_junkyard as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_junkyard as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_junkyard as curator

		with tempfile.TemporaryDirectory() as directory:
			root = copy_curator_files(curator, Path(directory))
			curator.check(root)
			definition = root / DEFINITION_PATH.relative_to(ROOT)
			original = definition.read_bytes()
			drifted = original.replace(b"Junk Yard", b"Junkeyard", 1)
			self.assertNotEqual(original, drifted)
			definition.write_bytes(drifted)
			with self.assertRaises(RuntimeError):
				curator.check(root)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_junkyard as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class JunkyardRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_junkyard as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_junkyard as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/junkyard-1996/source/Junk Yard (Williams 1996).vpx"
		script = source_root / "williams/junkyard-1996/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))


if __name__ == "__main__":
	unittest.main()
