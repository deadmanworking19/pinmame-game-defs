from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "midway" / "world-cup-soccer-1994.json"
SEED_PATH = ROOT / "tools" / "seeds" / "midway" / "world-cup-soccer-1994.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "midway" / "world-cup-soccer-1994.json"
CALLOUT_SEED_PATH = ROOT / "tools" / "seeds" / "midway" / "world-cup-soccer-1994-callouts.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "midway" / "world-cup-soccer-1994.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-security.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "midway" / "world-cup-soccer-1994.json"
KNOWLEDGE_NOTE_PATH = ROOT / "knowledge" / "williams" / "world-cup-soccer.md"
SCENARIO_PATH = ROOT / "tools" / "harness-scenarios" / "wpc" / "wcs-flipper-button-polarity.json"
JETS_SCENARIO_PATH = ROOT / "tools" / "harness-scenarios" / "wpc" / "wcs-jet-bumper-coil-pairing.json"
LOOP_GATE_SCENARIO_PATH = ROOT / "tools" / "harness-scenarios" / "wpc" / "wcs-loop-gate-travel.json"
# Retained-table objects: the jet bumpers and the one-way gate at the top of the right orbit.
BUMPER1, BUMPER2, BUMPER3 = (0.819085, 0.214142), (0.835502, 0.119845), (0.63906, 0.159845)
GATE003 = (0.818856, 0.035613)
DIVERTER_FLAP = (0.20819, 0.064358)

DRIVER_IDS = {
	"wcs_l2", "wcs_l3c", "wcs_la2", "wcs_l1", "wcs_la1", "wcs_d2",
	"wcs_p2", "wcs_p5", "wcs_p3", "wcs_p6",
	"wcs_f10", "wcs_f50", "wcs_f62", "wcs_f62b",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 46, 57, 58, 68, 73}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 45, 51, 52, 53}


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
	import curate_world_cup_soccer as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_world_cup_soccer.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


def _switch_positions(switches: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in switches.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


def _emitter_positions(lamps: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in lamps.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class WorldCupSoccerDefinitionTests(unittest.TestCase):
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
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			self.assertEqual("validated", state, dimension)
		self.assertEqual("midway.world-cup-soccer.1994", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(2811, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1994, self.definition["machine"]["year"])
		self.assertEqual("Bally", self.definition["machine"]["manufacturer"])
		self.assertEqual("pinmame.wpc-security", self.definition["controller"]["platform"])
		self.assertEqual("0x20", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_stale_partial_artifact_is_gone(self) -> None:
		self.assertFalse(PARTIAL_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_wcs_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for freewpc in ("wcs_f10", "wcs_f50", "wcs_f62", "wcs_f62b"):
			self.assertEqual("compatible", by_id[freewpc]["physical_compatibility"])
			self.assertEqual("wcs_l2", by_id[freewpc]["clone_of"])
		self.assertNotIn("clone_of", by_id["wcs_l2"])

	def test_the_full_wpc_security_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_matches_pinmame_with_zero_disagreement_in_the_ordinary_matrix(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_wcs_game_data_inverted_switch_mask_is_re_derived_in_code(self) -> None:
		import curate_world_cup_soccer as curator

		# Column index is the array index (0=coin/dedicated .. 11=Fliptronic); this is re-derived by
		# bit position, not hand-copied, so a transcription slip cannot silently survive.
		mask = (0x00, 0x00, 0x00, 0x3f, 0x1f, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		normalized_by_column = {
			3: {31 + row for row in range(6) if (mask[3] >> row) & 1},
			4: {41 + row for row in range(5) if (mask[4] >> row) & 1},
			5: {51 + row for row in range(3) if (mask[5] >> row) & 1},
		}
		expected = set().union(*normalized_by_column.values())
		self.assertEqual(expected, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		# The Fliptronic column is not normalized through invSw; wpc.c's WPC_FLIPPERS read complements
		# the whole column instead (see test_flipper_button_optos_are_normalized_by_the_column_read).
		self.assertEqual(0x00, mask[11])
		for address in (112, 114):
			self.assertNotIn(address, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)

	def test_flipper_positions_and_cabinet_optos(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[112]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		self.assertFalse(self.switches[114]["normally_closed"])
		self.assertEqual("not_applicable", self.switches[112]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.switches[112]["spatial"]["reason"])
		self.assertEqual("internal_nonvisual", self.switches[111]["spatial"]["reason"])

	def test_no_conflict_remains(self) -> None:
		# conflict.flipper-cabinet-opto-not-normalized was withdrawn: its premise (invSw[11] = 0x00
		# means 112/114 are not normalized) ignored the WPC_FLIPPERS column complement, and the
		# harness run shows public 1 is a pressed button. It must not be reintroduced.
		# conflict.jet-bumper-script-binding-vs-physical-position is settled by both location drawings
		# and the jet-bumper harness run (test_jet_bumpers_follow_the_manuals_absolute_names).
		self.assertEqual([], self.definition["conflicts"])
		self.assertNotIn(b"flipper-cabinet-opto-not-normalized", DEFINITION_PATH.read_bytes())
		self.assertNotIn("flipper-cabinet-opto-not-normalized", KNOWLEDGE_NOTE_PATH.read_text(encoding="utf-8"))

	def test_flipper_button_optos_are_normalized_by_the_column_read(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		runtime = sources["runtime-scenario.wcs-flipper-button-polarity"]
		self.assertEqual("runtime_scenario", runtime["kind"])
		self.assertRegex(runtime["sha256"], r"^[0-9a-f]{64}$")
		self.assertNotEqual("0" * 64, runtime["sha256"])
		self.assertTrue(runtime["uri"].startswith("external:pinmame-review-artifacts/world-cup-soccer/harness-runs/"))
		for phrase in ("112 = 1 pulses solenoid 45", "114 = 1 does the same on 47/48", "idle at 0"):
			self.assertIn(phrase, runtime["locator"])
		for address in (112, 114):
			switch = self.switches[address]
			self.assertEqual("validated", switch["provenance"]["status"])
			self.assertIn("runtime-scenario.wcs-flipper-button-polarity", switch["provenance"]["source_refs"])
			notes = switch["physical"]["notes"]
			self.assertIn("already normalized (1 = button pressed)", notes)
			self.assertIn("WPC_FLIPPERS", notes)
		for address in (111, 113):
			self.assertNotIn(
				"runtime-scenario.wcs-flipper-button-polarity",
				self.switches[address]["provenance"]["source_refs"],
			)
		scenario = load_json(SCENARIO_PATH)
		self.assertEqual("wcs_l2", scenario["game"])
		held = [action["switch"] for action in scenario["actions"] if action["type"] == "set_switch" and action["state"] == 1]
		self.assertIn(112, held)
		self.assertIn(114, held)
		self.assertFalse(any(action["type"] in {"pulse_key", "set_key"} for action in scenario["actions"]))

	def test_flipper_button_optos_rest_open_despite_the_printed_shading(self) -> None:
		# docs/PLATFORMS.md: the printed "typically closed" halftone marks opto construction only. The
		# Fliptronic column is read complemented and the ROM treats public 1 as pressed, so the contact the
		# matrix sees closes only while the button is pressed and rests open.
		sources = {source["id"]: source for source in self.definition["sources"]}
		library = sources["vpm-script-library.wpc-vbs"]
		self.assertEqual("vpx_script", library["kind"])
		self.assertEqual("external:pinmame-review-artifacts/vpm-script-libs/wpc.vbs", library["uri"])
		self.assertEqual("1a290886eb2c2fd2c13f82e5f8a1961fdc95238122096642d32fddf1cfbb1a8d", library["sha256"])
		for phrase in ("swLRFlip = 112", "swLLFlip = 114"):
			self.assertIn(phrase, library["locator"])
		for address in (112, 114):
			switch = self.switches[address]
			self.assertIs(False, switch["normally_closed"], address)
			self.assertEqual("opto", switch["physical"]["switch_type"], address)
			notes = switch["physical"]["notes"]
			self.assertNotIn("typically closed", notes)
			self.assertIn("Printed shaded as an opto (construction", notes)
			self.assertIn("the contact rests open", notes)
			self.assertIn("vpm-script-library.wpc-vbs", switch["provenance"]["source_refs"])

	def test_the_controller_profile_states_the_fliptronic_column_is_normalized(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		notes = " ".join(str(group.get("notes", "")) for group in profile["groups"])
		self.assertIn("WPC_FLIPPERS", notes)
		self.assertIn("The public Fliptronic state is already normalized here", notes)

	def test_pinned_pinmame_complements_the_fliptronic_column_for_wpc_security(self) -> None:
		from pinmame_game_defs.workspace import resolve_working_root

		checkout = os.environ.get("PINMAME_SOURCE_ROOT")
		root = Path(checkout) if checkout else resolve_working_root(ROOT) / "source-checkouts" / "pinmame"
		wpc = root / "src/wpc/wpc.c"
		wcs = root / "src/wpc/sims/wpc/full/wcs.c"
		if not wpc.is_file() or not wcs.is_file():
			self.skipTest("pinned PinMAME checkout is not available")
		wpc_text = wpc.read_text(encoding="utf-8", errors="replace")
		self.assertRegex(
			wpc_text,
			r"case WPC_FLIPPERS: /\* Flipper switches \*/\s*"
			r"if \(\(core_gameData->gen & GENWPC_HASWPC95\) == 0\)\s*"
			r"return ~coreGlobals\.swMatrix\[CORE_FLIPPERSWCOL\];",
		)
		self.assertRegex(wpc_text, r"#define GENWPC_HASWPC95\s+\(GEN_WPC95 \| GEN_WPC95DCS\)")
		wcs_text = wcs.read_text(encoding="utf-8", errors="replace")
		self.assertIn("GEN_WPCSECURITY, wpc_dispDMD", wcs_text)
		self.assertIn("{ 0x00, 0x00, 0x00, 0x3f, 0x1f, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}", wcs_text)

	def test_the_full_wpc_security_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 52))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in (17, 18, 19, 20, 22, 25, 26, 27, 28):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (21, 23, 24):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in range(37, 45):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		for address in (49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
		for address in (29, 30, 31):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
			self.assertEqual(["internal.wpc-state"], self.solenoids[address]["roles"], address)

	def test_the_lower_flipper_solenoids_carry_the_manuals_own_printed_numbers_unchanged(self) -> None:
		# Unlike WPC-95, WPC-Security has no LPDC board, so the printed circuit numbers already
		# equal the public addresses -- no manual.address remap is expected here.
		for address in (45, 46, 47, 48):
			manual_aliases = {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			self.assertEqual({f"{address:02d}"}, manual_aliases, address)
			self.assertEqual("coil", self.solenoids[address]["kind"])
			self.assertEqual("used", self.solenoids[address]["availability"])

	def test_solenoid_36_is_unfitted_and_none_is_mislabelled(self) -> None:
		self.assertEqual("unused", self.solenoids[36]["availability"])
		self.assertEqual("unused", self.solenoids[36]["spatial"]["reason"])
		# The manual genuinely fits a knocker on this machine (unlike some other WPC-era games in
		# this project), so it must be present, fitted, and cabinet-mounted -- not absent.
		self.assertEqual("used", self.solenoids[7]["availability"])
		self.assertEqual("not_applicable", self.solenoids[7]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])
		self.assertIn("knocker", self.solenoids[7]["label"].lower())
		# Solenoid 4 (Lock Release) must NOT be flagged unfitted -- an early transcription error
		# briefly claimed it had no table row; the corrected manual reading has it fully populated.
		self.assertEqual("used", self.solenoids[4]["availability"])
		self.assertEqual("validated", self.solenoids[4]["spatial"]["status"])

	def test_the_loop_gate_sits_on_the_gate_at_the_top_of_the_right_orbit(self) -> None:
		gate = self.solenoids[34]
		self.assertEqual("used", gate["availability"])
		self.assertEqual("A-17796", gate["physical"]["assembly_part_number"])
		[placement] = gate["spatial"]["placements"]
		self.assertEqual(GATE003, (placement["x"], placement["y"]))
		self.assertIn("drawing-callouts.world-cup-soccer.2026-10-23", placement["provenance"]["source_refs"])
		self.assertIn("runtime-scenario.wcs-loop-gate-travel", gate["provenance"]["source_refs"])
		for phrase in ("Gate003", "A-17797-1", "3.5 s", "Travel lamp (63)"):
			self.assertIn(phrase, gate["physical"]["notes"])
		mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.loop-gate")
		self.assertEqual([], mechanism["sensors"])
		self.assertEqual({"closed", "open"}, {position["id"] for position in mechanism["positions"]})
		self.assertIn("runtime-scenario.wcs-loop-gate-travel", mechanism["provenance"]["source_refs"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("pinmame-spatial-audit", report["format"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual([], report["no_spatial_key_outputs"])

	def test_jet_bumpers_follow_the_manuals_absolute_names(self) -> None:
		# Both location drawings put 81/9 on the left bumper, 82/10 on the upper one and 83/11 on the lower
		# one, and the harness run pairs each switch with its own coil. The retained table's script binds
		# the switches to rotated objects; that defect must not come back into the placements.
		for switch, coil, bumper in ((81, 9, BUMPER3), (82, 10, BUMPER2), (83, 11, BUMPER1)):
			for device in (self.switches[switch], self.solenoids[coil]):
				[placement] = device["spatial"]["placements"]
				self.assertEqual(bumper, (placement["x"], placement["y"]), device["id"])
				self.assertIn("runtime-scenario.wcs-jet-bumper-coil-pairing", device["provenance"]["source_refs"])
			self.assertIn("a defect of that table", self.switches[switch]["physical"]["notes"])
		mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.jet-bumpers")
		descriptions = {position["id"]: position["description"] for position in mechanism["positions"]}
		self.assertIn("Bumper3; the ROM fires solenoid 9 when switch 81 closes", descriptions["left"])
		self.assertIn("Bumper2; the ROM fires solenoid 10 when switch 82 closes", descriptions["upper"])
		self.assertIn("Bumper1; the ROM fires solenoid 11 when switch 83 closes", descriptions["lower"])
		self.assertNotIn("fire coils 10, 9, and 11", mechanism["behavior"])

	def test_the_ramp_diverter_coils_sit_on_the_diverter_flap(self) -> None:
		for address in (8, 16):
			[placement] = self.solenoids[address]["spatial"]["placements"]
			self.assertEqual(DIVERTER_FLAP, (placement["x"], placement["y"]), address)
			self.assertIn("BM_diverterside01", self.solenoids[address]["physical"]["notes"])

	def test_the_goalie_target_projects_onto_the_goalie(self) -> None:
		goalie = _switch_positions(self.switches)[43]
		self.assertEqual(goalie, _switch_positions(self.switches)[48])
		self.assertIn("BM_goalkeeper", self.switches[48]["physical"]["notes"])

	def test_the_shooter_lane_has_a_manual_plunger(self) -> None:
		mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.shooter-lane")
		self.assertEqual("A-17730", mechanism["assembly_part_number"])
		self.assertIn("manual plunger", mechanism["behavior"])
		self.assertIn("dead code", mechanism["behavior"])
		self.assertIn("manual plunger", self.solenoids[49]["physical"]["notes"])
		self.assertNotIn("automatic impulse plunger", DEFINITION_PATH.read_text(encoding="utf-8"))
		self.assertNotIn("**automatic** plunger", KNOWLEDGE_NOTE_PATH.read_text(encoding="utf-8"))

	def test_flasher_quantities_count_backbox_bulbs_and_place_only_playfield_ones(self) -> None:
		# Printed 2-48: playfield bulbs, then a backbox #906 on every flasher but 22.
		expected = {17: (2, 1), 18: (3, 2), 19: (3, 2), 20: (2, 1), 22: (2, 2), 25: (2, 1), 26: (2, 1), 27: (3, 2), 28: (3, 2)}
		actual = {
			address: (self.solenoids[address]["physical"]["quantity"], len(self.solenoids[address]["spatial"]["placements"]))
			for address in expected
		}
		self.assertEqual(expected, actual)
		for address in expected:
			notes = self.solenoids[address]["physical"]["notes"]
			self.assertIn("Printed flashlamp complement:", notes)
			self.assertEqual(address != 22, "on the backbox" in notes, address)

	def test_solenoid_51_is_a_virtual_mirror_not_a_fourth_diverter_device(self) -> None:
		self.assertEqual("virtual", self.solenoids[51]["kind"])
		self.assertEqual("used", self.solenoids[51]["availability"])
		self.assertEqual(["internal.duplicate.mirror"], self.solenoids[51]["roles"])
		self.assertEqual("not_applicable", self.solenoids[51]["spatial"]["status"])
		self.assertEqual("virtual", self.solenoids[51]["spatial"]["reason"])

	def test_gi_playfield_strings_are_located_and_insert_panel_strings_are_cabinet(self) -> None:
		for address in (0, 1, 4):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(11, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(11, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(22, len(self.gi[4]["spatial"]["placements"]))
		for address in (2, 3):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_gi_top_clamped_placements_stay_in_range(self) -> None:
		for placement in self.gi[4]["spatial"]["placements"]:
			self.assertGreaterEqual(placement["y"], 0.0)
			self.assertLessEqual(placement["y"], 1.0)
		zero_y = [p for p in self.gi[4]["spatial"]["placements"] if p["y"] == 0.0]
		self.assertEqual(3, len(zero_y))

	def test_lamp_quantities_and_cabinet_lamps_are_explicit(self) -> None:
		for address in (46, 47, 71, 78):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		# Lamp 53 "Goal (2)": both bulbs under the one kidney-shaped GOAL insert the drawing marks once.
		self.assertEqual(2, self.lamps[53]["physical"]["quantity"])
		self.assertEqual(1, len(self.lamps[53]["spatial"]["placements"]))
		for address in sorted(MATRIX_ADDRESSES - {46, 47, 53, 71, 78, 87, 88}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in (87, 88):
			self.assertEqual("used", self.lamps[address]["availability"], address)
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual('Chicago "P"', self.lamps[11]["label"])
		self.assertEqual("Start Button", self.lamps[88]["label"])

	def test_no_lamp_is_marked_not_used(self) -> None:
		for address in MATRIX_ADDRESSES:
			self.assertEqual("used", self.lamps[address]["availability"], address)

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device.get("spatial")
			if spatial is None:
				continue
			if spatial["status"] == "not_applicable":
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
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _switch_positions(self.switches).items()}
		switch_y = {addr: pos[1] for addr, pos in _switch_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _emitter_positions(self.lamps).items()}
		lamp_y = {addr: pos[1] for addr, pos in _emitter_positions(self.lamps).items()}

		# Jet bumpers by absolute position, as both location drawings name them: Left (81) leftmost,
		# Upper (82) furthest back, Lower (83) furthest forward.
		self.assertLess(switch_x[81], switch_x[82])
		self.assertLess(switch_x[81], switch_x[83])
		self.assertLess(switch_y[82], switch_y[81])
		self.assertLess(switch_y[81], switch_y[83])

		# Trough kickers descend in x from Trough 1 (nearest eject) to Trough 5 (nearest drain),
		# and ascend in y (moving further from the top of the table) in the same order.
		self.assertGreater(switch_x[31], switch_x[32])
		self.assertGreater(switch_x[32], switch_x[33])
		self.assertGreater(switch_x[33], switch_x[34])
		self.assertGreater(switch_x[34], switch_x[35])
		self.assertLess(switch_y[31], switch_y[32])
		self.assertLess(switch_y[32], switch_y[33])
		self.assertLess(switch_y[33], switch_y[34])
		self.assertLess(switch_y[34], switch_y[35])

		# Left/right slingshots stay on their printed sides.
		self.assertLess(switch_x[84], 0.5)
		self.assertGreater(switch_x[85], 0.5)

		# Upper left/right lanes ascend left -> right for both switches and lamps.
		self.assertLess(switch_x[87], switch_x[88])
		self.assertLess(lamp_x[66], lamp_x[67])

		# Rollovers 1 (High) through 4 (Low) ascend in both x and y together (a single arc).
		self.assertLess(switch_x[61], switch_x[62])
		self.assertLess(switch_x[62], switch_x[63])
		self.assertLess(switch_x[63], switch_x[64])
		self.assertLess(switch_y[61], switch_y[62])
		self.assertLess(switch_y[62], switch_y[63])
		self.assertLess(switch_y[63], switch_y[64])

		# Skill shot lane: Front (nearest the player/apron) has the largest y; Rear (deepest into
		# the playfield) has the smallest, descending in that printed order.
		self.assertGreater(switch_y[51], switch_y[52])
		self.assertGreater(switch_y[52], switch_y[53])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.skill-shot",
				"mechanism.goalie", "mechanism.spinning-ball", "mechanism.magna-goalie",
				"mechanism.lock-magnet", "mechanism.ramp-lock-post", "mechanism.ramp-diverter",
				"mechanism.loop-gate", "mechanism.goal-tv-poppers", "mechanism.eject-holes",
				"mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.kickback",
				"mechanism.knocker", "mechanism.lower-flippers",
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
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"} and device["availability"] == "used"
		}
		self.assertEqual(set(), physical - set(owners))
		self.assertIn("35-segment", mechanisms["mechanism.goalie"]["behavior"])
		self.assertIn("MECH_LINEAR|MECH_REVERSE|MECH_ONESOL", mechanisms["mechanism.goalie"]["behavior"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.trough-eject-stack-pulse"}, set(relationships))
		self.assertEqual("switch.matrix-36", relationships["relationship.trough-eject-stack-pulse"]["destination"])
		self.assertEqual("pulse", relationships["relationship.trough-eject-stack-pulse"]["kind"])

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
		self.assertIn("vpx-script.wcs-vpw-1-5", sources)
		self.assertTrue(sources["vpx-script.wcs-vpw-1-5"]["known_working"])
		self.assertEqual(
			"c18cfbaa4e8c3b67259ac5d6c7b6842dfdaaf308b0fd71a64071118b57ac73c5",
			sources["vpx-script.wcs-vpw-1-5"]["sha256"],
		)
		self.assertEqual(
			"ab7e07fce7b589f9732f458a7a09ad08b87237852d97d7b5bf9a74f6b0f6d23d",
			sources["vpx-table.wcs-vpw-1-5"]["sha256"],
		)
		runtime_sources = [source["id"] for source in self.definition["sources"] if source["kind"] == "runtime_scenario"]
		self.assertEqual(
			[
				"runtime-scenario.wcs-flipper-button-polarity",
				"runtime-scenario.wcs-jet-bumper-coil-pairing",
				"runtime-scenario.wcs-loop-gate-travel",
			],
			runtime_sources,
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

	def test_manual_source_carries_every_expected_excerpt(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.midway.world-cup-soccer.1994"]
		excerpt_ids = {excerpt["id"] for excerpt in manual["excerpts"]}
		self.assertEqual(
			{
				"excerpt.world-cup-soccer.switch-matrix",
				"excerpt.world-cup-soccer.switch-locations",
				"excerpt.world-cup-soccer.lamp-matrix",
				"excerpt.world-cup-soccer.lamp-locations",
				"excerpt.world-cup-soccer.solenoid-flasher-wiring",
				"excerpt.world-cup-soccer.solenoid-flasher-locations",
				"excerpt.world-cup-soccer.general-illumination",
				"excerpt.world-cup-soccer.boards-and-assemblies",
				"excerpt.world-cup-soccer.solenoid-flasher-drawing",
				"excerpt.world-cup-soccer.upper-playfield-gate",
				"excerpt.world-cup-soccer.ball-shooter",
			},
			excerpt_ids,
		)
		for excerpt in manual["excerpts"]:
			self.assertTrue(excerpt["reviewed"], excerpt["id"])
			self.assertEqual("manual", excerpt["method"], excerpt["id"])
		matrix = next(e for e in manual["excerpts"] if e["id"] == "excerpt.world-cup-soccer.switch-matrix")
		self.assertIn("image", matrix)
		self.assertLessEqual((ROOT / matrix["image"]).stat().st_size, 100_000)

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-security", profile["id"])
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


class WorldCupSoccerDrawingCalloutTests(unittest.TestCase):
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
		self.assertEqual(135, len(decisions["placements"]))
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

	def test_drawing_measurements_reproduce_and_cite_their_corroboration(self) -> None:
		import curate_world_cup_soccer as curator

		self.assertEqual(12, len(self.seed["measurements"]))
		devices = {
			placement["id"]: placement
			for collection in ("inputs", "outputs")
			for device in self.definition[collection]
			for placement in (device.get("spatial") or {}).get("placements") or []
		}
		for placement_id in self.seed["measurements"]:
			placement = devices[placement_id]
			self.assertEqual(self.dc.measured(self.seed, placement_id), (placement["x"], placement["y"]))
			refs = placement["provenance"]["source_refs"]
			self.assertEqual("validated", placement["provenance"]["status"])
			self.assertIn("manual.midway.world-cup-soccer.1994", refs)
			self.assertIn("drawing-callouts.world-cup-soccer.2026-10-23", refs)
			corroboration = curator.MEASUREMENT_CORROBORATION[placement_id]
			expected = "human-review.wcs-physical-corroboration-2026-10-23" if corroboration == "photos" else "vpx-table.wcs-vpw-1-5"
			self.assertIn(expected, refs)
			self.assertIn(placement_id, curator.TABLE_OFFSETS)

	def test_drawing_measurements_lie_inside_their_pages_control_hull(self) -> None:
		# On the page itself: every measured pixel lies strictly inside the convex hull of the control pixels.
		def cross(o: tuple, a: tuple, b: tuple) -> float:
			return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

		def hull(points: list) -> list:
			points = sorted(set(points))
			lower: list = []
			upper: list = []
			for p in points:
				while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
					lower.pop()
				lower.append(p)
			for p in reversed(points):
				while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
					upper.pop()
				upper.append(p)
			return lower[:-1] + upper[:-1]

		for placement_id, item in self.seed["measurements"].items():
			outline = hull([tuple(control["pixel"]) for control in self.seed["pages"][item["page"]]["controls"]])
			for a, b in zip(outline, outline[1:] + outline[:1]):
				self.assertGreater(cross(a, b, tuple(item["pixel"])), 0, placement_id)
		for key, page in self.seed["pages"].items():
			frame = [control["xy"] for control in page["controls"] if control["object"] == "playfield-frame"]
			self.assertEqual([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]], frame, key)
			# The drawn frame has no bottom-right corner; the ball shooter switch slot closes the hull there.
			slot = [control["xy"] for control in page["controls"] if control["object"] == "sw38"]
			self.assertEqual([[0.936637, 0.885851]], slot, key)
			pairs = [(tuple(control["pixel"]), tuple(control["xy"])) for control in page["controls"]]
			self.assertLessEqual(max(self.dc.leave_one_out(pairs)), 0.015, key)

	def test_the_curator_refuses_a_measurement_outside_the_hull_but_inside_the_bounding_box(self) -> None:
		import copy

		import curate_world_cup_soccer as curator

		placement_id = "device.skill-shot.emitter.2"
		x, y = self.dc.measured(self.seed, placement_id)
		self.assertTrue(curator._within_control_hull(self.seed, placement_id, x, y))
		without_slot = copy.deepcopy(self.seed)
		page = without_slot["pages"][without_slot["measurements"][placement_id]["page"]]
		page["controls"] = [control for control in page["controls"] if control["object"] != "sw38"]
		xs = [control["xy"][0] for control in page["controls"]]
		ys = [control["xy"][1] for control in page["controls"]]
		self.assertTrue(min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys))
		self.assertFalse(curator._within_control_hull(without_slot, placement_id, x, y))

	def test_the_paired_balloons_and_the_kidney_insert_read_are_recorded_corrections(self) -> None:
		corrected = {
			(key, read["label"]): read
			for key, page in self.seed["pages"].items()
			for read in page["reads"]
			if "verifier_note" in read
		}
		self.assertEqual({("2-49", "8/16"), ("2-49", "23/24"), ("2-45", "53")}, set(corrected))
		self.assertEqual("symbol_centre", corrected[("2-45", "53")]["point"])
		self.assertEqual([1552.0, 709.0], corrected[("2-45", "53")]["reader_pixel"])

	def test_the_drawing_crops_match_the_seed(self) -> None:
		self.assertEqual(3, self.dc.verify_retained(self.seed, ROOT, None, None))


class WorldCupSoccerCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_world_cup_soccer as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_world_cup_soccer as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_world_cup_soccer as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"World Cup Soccer", b"World Cup Soccerr", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_world_cup_soccer as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class WorldCupSoccerRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_world_cup_soccer as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_world_cup_soccer as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "midway/world-cup-soccer-1994/source/World Cup Soccer (Bally 1994) VPW v1.5.vpx"
		script = source_root / "midway/world-cup-soccer-1994/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_world_cup_soccer as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "world-cup-soccer" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))

	def test_flipper_button_harness_run_matches_its_pinned_hash_and_claims(self) -> None:
		import curate_world_cup_soccer as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		sources = {source["id"]: source for source in curator.source_records()}
		uri = sources[curator.RUNTIME_FLIPPER_SOURCE]["uri"]
		run_path = Path(root) / uri.removeprefix("external:pinmame-review-artifacts/")
		self.assertEqual(curator.RUNTIME_FLIPPER_RUN_SHA256, curator._file_sha256(run_path))
		self.assertEqual(curator.RUNTIME_FLIPPER_SCENARIO_SHA256, curator._file_sha256(SCENARIO_PATH))
		run = load_json(run_path)
		self.assertIsNone(run["failure"])
		self.assertEqual("wcs_l2", run["game"])
		self.assertEqual(curator.RUNTIME_LIBRARY_SHA256, run["library_sha256"])
		self.assertEqual(curator.RUNTIME_FLIPPER_SCENARIO_SHA256, run["scenario"]["sha256"])
		self.assertIn(curator.RUNTIME_LIBRARY_REVISION, sources[curator.RUNTIME_FLIPPER_SOURCE]["locator"])
		# The run folder's canonical manifest pins run.json and the state/ NVRAM and cfg files.
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(run_path.parent, Path(root) / curator.RUNTIME_FLIPPER_RUN_DIRECTORY)
		self.assertEqual(curator.RUNTIME_FLIPPER_RUN_MANIFEST_SHA256, check_manifest(run_path.parent, "wcs_l2"))
		self.assertIn(curator.RUNTIME_FLIPPER_RUN_MANIFEST_SHA256, sources[curator.RUNTIME_FLIPPER_SOURCE]["locator"])
		# Re-derive the claim from the raw events: every lower-flipper output energizes while the matching
		# button address is held at public 1, each held press energizes both outputs, and each hold output
		# (46, 48) drops when its button returns to 0, within one output poll (about 16 ms) of the release.
		poll_s = 0.02
		held: dict[int, bool] = {112: False, 114: False}
		released_at: dict[int, float | None] = {112: None, 114: None}
		pressed_outputs: dict[int, set[int]] = {112: set(), 114: set()}
		hold_drops: dict[int, int] = {112: 0, 114: 0}
		button_for_output = {45: 112, 46: 112, 47: 114, 48: 114}
		hold_output = {112: 46, 114: 48}
		for event in run["events"]:
			if event["event"] == "switch" and event["number"] in held:
				held[event["number"]] = bool(event["state"])
				released_at[event["number"]] = None if event["state"] else event["time_s"]
			elif event["event"] == "solenoid" and event["number"] in button_for_output:
				button = button_for_output[event["number"]]
				if event["state"]:
					self.assertTrue(held[button], event)
					pressed_outputs[button].add(event["number"])
				elif event["number"] == hold_output[button]:
					self.assertFalse(held[button], event)
					self.assertIsNotNone(released_at[button], event)
					self.assertLessEqual(event["time_s"] - released_at[button], poll_s, event)
					hold_drops[button] += 1
		self.assertEqual({45, 46}, pressed_outputs[112])
		self.assertEqual({47, 48}, pressed_outputs[114])
		self.assertEqual({112: 1, 114: 1}, hold_drops)

	def _run(self, directory_constant: str, run_sha_constant: str, manifest_constant: str, scenario_constant: str, scenario_path: Path) -> dict:
		import curate_world_cup_soccer as curator
		from build_external_evidence_manifest import check_manifest

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		directory = Path(root) / getattr(curator, directory_constant)
		run_path = directory / "run.json"
		self.assertEqual(getattr(curator, run_sha_constant), curator._file_sha256(run_path))
		self.assertEqual(getattr(curator, scenario_constant), curator._file_sha256(scenario_path))
		self.assertEqual(getattr(curator, manifest_constant), check_manifest(directory, "wcs_l2"))
		run = load_json(run_path)
		self.assertIsNone(run["failure"])
		self.assertEqual("wcs_l2", run["game"])
		self.assertEqual(curator.PINNED_LIBRARY_SHA256, run["library_sha256"])
		self.assertEqual(getattr(curator, scenario_constant), run["scenario"]["sha256"])
		return run

	def test_jet_bumper_harness_run_pairs_each_switch_with_its_own_coil(self) -> None:
		run = self._run("RUNTIME_JETS_RUN_DIRECTORY", "RUNTIME_JETS_RUN_SHA256", "RUNTIME_JETS_RUN_MANIFEST_SHA256", "RUNTIME_JETS_SCENARIO_SHA256", JETS_SCENARIO_PATH)
		pairs = {81: 9, 82: 10, 83: 11}
		last_switch = None
		fired: list[tuple[int, int]] = []
		for event in run["events"]:
			if event["event"] == "switch" and event["number"] in pairs and event["state"] and not event.get("initial"):
				last_switch = (event["number"], event["time_s"])
			elif event["event"] == "solenoid" and event["number"] in pairs.values() and event["state"]:
				self.assertIsNotNone(last_switch, event)
				switch, closed_at = last_switch
				self.assertEqual(pairs[switch], event["number"], event)
				self.assertLessEqual(event["time_s"] - closed_at, 0.07, event)
				fired.append((switch, event["number"]))
		self.assertEqual([(81, 9), (82, 10), (83, 11), (83, 11), (81, 9), (82, 10)], fired)

	def test_loop_gate_harness_run_shows_the_travel_rule(self) -> None:
		run = self._run("RUNTIME_LOOP_GATE_RUN_DIRECTORY", "RUNTIME_LOOP_GATE_RUN_SHA256", "RUNTIME_LOOP_GATE_RUN_MANIFEST_SHA256", "RUNTIME_LOOP_GATE_SCENARIO_SHA256", LOOP_GATE_SCENARIO_PATH)
		travel_lit = False
		closures: list[tuple[int, float, bool]] = []
		energized: list[tuple[float, float]] = []
		for event in run["events"]:
			if event["event"] == "lamp" and event["number"] == 63:
				travel_lit = bool(event["state"])
			elif event["event"] == "switch" and event["number"] in (27, 47) and event["state"] and not event.get("initial"):
				closures.append((event["number"], event["time_s"], travel_lit))
			elif event["event"] == "solenoid" and event["number"] == 34:
				if event["state"]:
					energized.append((event["time_s"], -1.0))
				else:
					energized[-1] = (energized[-1][0], event["time_s"])
		self.assertEqual([(47, False), (27, False), (27, True), (47, True)], [(n, lit) for n, _, lit in closures])
		self.assertEqual(2, len(energized))
		for (switch, closed_at, _), (on, off) in zip(closures[2:], energized):
			self.assertLessEqual(on - closed_at, 0.05, switch)
			self.assertAlmostEqual(3.5, off - on, delta=0.1)
		for _, closed_at, _ in closures[:2]:
			self.assertFalse(any(closed_at <= on <= closed_at + 4.0 for on, _ in energized))

	def test_callout_check_artifacts_and_physical_photos_are_retained(self) -> None:
		import curate_world_cup_soccer as curator
		import drawing_callouts
		from build_external_evidence_manifest import check_manifest

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		seed = load_json(CALLOUT_SEED_PATH)
		self.assertGreater(drawing_callouts.verify_retained(seed, ROOT, None, Path(root)), 3)
		photos = Path(root) / curator.PHYSICAL_EVIDENCE_DIRECTORY
		self.assertEqual(curator.PHYSICAL_EVIDENCE_MANIFEST_SHA256, check_manifest(photos, "wcs_l2"))

	def test_retained_wpc_vbs_library_matches_its_pinned_hash(self) -> None:
		import curate_world_cup_soccer as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		library = Path(root) / curator.VPM_WPC_LIBRARY_URI.removeprefix("external:pinmame-review-artifacts/")
		self.assertEqual(curator.VPM_WPC_SHA256, curator._file_sha256(library))
		self.assertEqual(curator.VPM_CORE_SHA256, curator._file_sha256(library.parent / "core.vbs"))
		text = library.read_text(encoding="latin-1")
		self.assertIn("Const swLRFlip = 112", text)
		self.assertIn("Const swLLFlip = 114", text)


if __name__ == "__main__":
	unittest.main()
