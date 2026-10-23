from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "funhouse-1990.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "funhouse-1990.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "funhouse-1990.json"
CALLOUT_SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "funhouse-1990-callouts.json"
RUNTIME_PATH = ROOT / "evidence" / "runtime" / "wpc-alpha" / "funhouse-fh_l9-gi-test.json"
SCENARIO_PATH = ROOT / "tools" / "harness-scenarios" / "wpc-alpha" / "fh-gi-test.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "funhouse-1990.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-alpha.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "funhouse-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "funhouse-1990.md"

DRIVER_IDS = {
	"fh_l9", "fh_d9", "fh_l9b", "fh_d9b", "fh_905h", "fh_905hbs", "fh_906h", "fh_907h", "fh_pa1",
	"fh_l2", "fh_l3", "fh_d3", "fh_l4", "fh_d4", "fh_l5", "fh_d5", "fh_f91",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {23, 78, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {51, 55}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def _run_curator_without_mode() -> None:
	import curate_funhouse as curator

	argv = sys.argv
	sys.argv = ["curate_funhouse.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class FunHouseDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_names_the_apron_gi_blocker(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		# Every placement the record makes is validated, but the apron G.I. bulbs of public 4 have no source position.
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		dimensions = self.definition["coverage"]["dimensions"]
		self.assertEqual("unknown", dimensions["spatial_placement"])
		self.assertEqual({"validated"}, {value for key, value in dimensions.items() if key != "spatial_placement"})
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertIn("under the apron", self.gi[4]["physical"]["notes"])
		self.assertIn("Resolution path:", KNOWLEDGE_PATH.read_text(encoding="utf-8"))
		self.assertEqual("williams.funhouse.1990", self.definition["machine"]["id"])
		self.assertEqual("Williams", self.definition["machine"]["manufacturer"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1990, self.definition["machine"]["year"])
		self.assertEqual(966, self.definition["machine"]["ipdb_id"])
		self.assertEqual("pinmame.wpc-alpha", self.definition["controller"]["platform"])
		self.assertEqual("0x2", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_driver_tree_matches_pinned_catalog(self) -> None:
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(by_id))
		self.assertNotIn("clone_of", by_id["fh_l9"])
		for driver_id in DRIVER_IDS - {"fh_l9"}:
			self.assertEqual("fh_l9", by_id[driver_id]["clone_of"], driver_id)
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"})
			self.assertGreater(len(driver["variant_notes"]), 0)
		self.assertEqual("compatible", by_id["fh_pa1"]["physical_compatibility"])
		self.assertIn("GEN_WPCALPHA_1", by_id["fh_pa1"]["variant_notes"])
		self.assertIn("gameSpecific1=1", by_id["fh_pa1"]["variant_notes"])
		self.assertIn("WPC_CFTBL", by_id["fh_pa1"]["variant_notes"])
		self.assertIn("internal PWM lamp slots 65-72", by_id["fh_pa1"]["variant_notes"])

	def test_retained_source_identity_and_tool_version_are_pinned(self) -> None:
		by_id = {source["id"]: source for source in self.definition["sources"]}
		manual = by_id["manual.williams.funhouse.1990"]
		self.assertEqual("arcademanual_Funhouse_OPS", manual["source_id"])
		self.assertEqual("https://archive.org/details/arcademanual_Funhouse_OPS", manual["uri"])
		self.assertEqual("2026-08-07T00:18:16Z", manual["acquired_at"])
		self.assertIn("manuallibrary@textfiles.com", manual["locator"])
		self.assertEqual("2026-08-14T17:36:41Z", by_id["manual.williams.funhouse.1990.operator-handbook"]["acquired_at"])
		self.assertEqual("2026-08-14T17:37:39Z", by_id["photo.williams.funhouse.1990.a13"]["acquired_at"])
		self.assertEqual("2026-08-07T15:17:32Z", by_id["vpx-table.fh-1-3"]["acquired_at"])
		self.assertEqual("2026-08-07T15:17:33Z", by_id["vpx-script.fh-1-3"]["acquired_at"])
		self.assertIn("vpxtool git:v0.33.3", by_id["vpx-extraction.fh-1-3"]["locator"])
		self.assertEqual("45ee7c7bb500749feecabd96eef6b5ffe1d4a9ff4b611176bf1155a60ca2b413", by_id["vpx-table.fh-2-0c"]["sha256"])
		self.assertIn("f05e57012e5f7290f74bd50e986e6668b5721c066cf9d1c0612c18747f5b7595", by_id["vpx-extraction.fh-2-0c"]["locator"])

	def test_controller_profile_reused_unchanged(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-alpha", profile["id"])
		self.assertEqual({"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp", "pinmame.output.gi"}, {group["id"] for group in profile["groups"]})

	def test_switch_and_dip_enumeration(self) -> None:
		matrix_switches = {address: switch for address, switch in self.switches.items() if address in MATRIX_ADDRESSES}
		self.assertEqual(MATRIX_ADDRESSES, set(matrix_switches))
		for address, switch in matrix_switches.items():
			if address in UNUSED_MATRIX_ADDRESSES:
				self.assertEqual("unused", switch["availability"], address)
				self.assertEqual("unused", switch["spatial"]["reason"], address)
			else:
				self.assertEqual("used", switch["availability"], address)
		for address in range(1, 9):
			self.assertEqual(f"switch.cabinet-{address}", self.switches[address]["id"])
		self.assertEqual(set(range(111, 119)), {address for address in self.switches if 111 <= address <= 118})
		for address in {112, 114}:
			self.assertEqual("used", self.switches[address]["availability"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
		for address in {111, 113, 115, 116, 117, 118}:
			self.assertEqual("unused", self.switches[address]["availability"])
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"])
		for address in {11, 12}:
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
			self.assertIn("matrix state is copied", self.switches[address]["physical"]["notes"])
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))

	def test_optos_and_constant_switch_are_normalized(self) -> None:
		for address, switch in self.switches.items():
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"].get("switch_type"), address)
				self.assertTrue(switch["normally_closed"], address)
			elif address in MATRIX_ADDRESSES and address not in UNUSED_MATRIX_ADDRESSES and address != 24:
				self.assertNotEqual("opto", switch["physical"].get("switch_type"), address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])

	def test_right_trough_switch_is_resolved_on_ballrelease(self) -> None:
		switch = self.switches[63]
		self.assertEqual("Right Trough", switch["label"])
		self.assertEqual("validated", switch["spatial"]["status"])
		placement = switch["spatial"]["placements"][0]
		self.assertAlmostEqual(0.877269, placement["x"], places=6)
		self.assertAlmostEqual(0.863859, placement["y"], places=6)
		self.assertIn("manual.williams.funhouse.1990.operator-handbook", placement["provenance"]["source_refs"])

	def test_public_solenoid_contract_is_complete(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		for address in {17, 18, 19, 20, 23, 24}:
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
			placements = len(self.solenoids[address]["spatial"]["placements"])
			# Both Clock bulbs light the clock from under its centre and share one placement.
			self.assertEqual(1 if address == 19 else self.solenoids[address]["physical"]["quantity"], placements, address)
		self.assertEqual(2, self.solenoids[19]["physical"]["quantity"])
		self.assertEqual(2, len({(placement["x"], placement["y"]) for placement in self.solenoids[20]["spatial"]["placements"]}))
		self.assertEqual(
			[(0.446452, 0.46247), (0.460268, 0.512137)],
			[(placement["x"], placement["y"]) for placement in self.solenoids[20]["spatial"]["placements"]],
		)
		self.assertIn("vpx-script.funhouse-community-current", self.solenoids[20]["provenance"]["source_refs"])
		self.assertEqual("motor", self.solenoids[21]["kind"])
		self.assertEqual("motor", self.solenoids[22]["kind"])
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])

	def test_wpc_state_and_virtual_output_dispositions(self) -> None:
		for address in (29, 30):
			self.assertEqual("virtual", self.solenoids[address]["kind"])
			self.assertEqual("used", self.solenoids[address]["availability"])
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"])
		self.assertEqual("relay", self.solenoids[31]["kind"])
		self.assertEqual("used", self.solenoids[31]["availability"])
		self.assertEqual(["internal.wpc-state", "cabinet.game-on-relay"], self.solenoids[31]["roles"])
		self.assertEqual("cabinet_or_service", self.solenoids[31]["spatial"]["reason"])
		for address in {32, *range(33, 45), 50}:
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		self.assertEqual("virtual", self.solenoids[49]["kind"])
		self.assertEqual("used", self.solenoids[49]["availability"])
		self.assertEqual(["internal.simulator-ball-shooter"], self.solenoids[49]["roles"])
		self.assertIn("sShooterRel", self.solenoids[49]["physical"]["notes"])

	def test_synthetic_flipper_states_are_not_physical_coils(self) -> None:
		for address in range(45, 49):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("used", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		flippers = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.flippers")
		self.assertEqual(["device.synthetic-lower-right-flipper", "device.synthetic-left-flipper"], flippers["actuators"])
		self.assertEqual({"lower-right", "lower-left", "upper-left"}, {position["id"] for position in flippers["positions"]})
		self.assertIn("FL-11753", flippers["behavior"])
		self.assertIn("both LeftFlipper and LeftFlipper1", flippers["behavior"])
		self.assertIn("must not", flippers["behavior"])

	def test_lamp_matrix_and_multi_bulb_quantities(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertTrue(all(lamp["availability"] == "used" for lamp in self.lamps.values()))
		for address in (53, 61, 82):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in (51, 52, 72):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)

	def test_steps_switches_and_lamps_are_drawing_measurements_in_order(self) -> None:
		import drawing_callouts

		seed = load_json(CALLOUT_SEED_PATH)
		for collection, addresses, role, suffix in ((self.switches, (36, 26, 15), "sensor", "hb-9-slot"), (self.lamps, (56, 55, 54), "emitter", "hb-7-socket")):
			ys = []
			for address in addresses:
				device = collection[address]
				self.assertEqual("validated", device["spatial"]["status"])
				(placement,) = device["spatial"]["placements"]
				self.assertEqual(f"{device['id']}.{role}.{suffix}", placement["id"])
				self.assertEqual(drawing_callouts.measured(seed, placement["id"]), (placement["x"], placement["y"]))
				self.assertEqual(["manual.williams.funhouse.1990.operator-handbook", "human-review.funhouse.drawing-callouts"], placement["provenance"]["source_refs"])
				ys.append(placement["y"])
			# Top, middle and bottom step run from the rear forwards.
			self.assertEqual(sorted(ys), ys)
		for address in (54, 55, 56):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"])
			self.assertIn("_finger_1", self.lamps[address]["physical"]["notes"])

	def test_gangway_typo_is_resolved_and_no_conflicts_remain(self) -> None:
		self.assertEqual("Gangway 100,000", self.lamps[12]["label"])
		self.assertIn("resolved one-digit typo", self.lamps[12]["physical"]["notes"])
		refs = set(self.lamps[12]["provenance"]["source_refs"])
		self.assertIn("manual.williams.funhouse.1990.operator-handbook", refs)
		self.assertIn("photo.williams.funhouse.1990.a13", refs)
		self.assertEqual([], self.definition["conflicts"])

	def test_gi_strings_follow_the_rom_test(self) -> None:
		self.assertEqual(set(range(5)), set(self.gi))
		expected = {
			0: ("Backglass Upper G.I.", "Brown", "White-Brown", "J120-1", "Q18", "F110"),
			1: ("Rudy / Backglass G.I.", "Orange", "White-Orange", "J120-2", "Q10", "F109"),
			2: ("Rear Playfield G.I.", "Yellow", "White-Yellow", "J120-3", "Q14", "F108"),
			3: ("Backglass Center G.I.", "Green", "White-Green", "J120-5", "Q16", "F107"),
			4: ("Front Playfield G.I.", "Violet", "White-Violet", "J120-6 / J119-3", "Q12", "F106"),
		}
		for address, (label, feed, return_wire, connection, triac, fuse) in expected.items():
			device = self.gi[address]
			self.assertEqual(label, device["label"])
			wiring = device["wiring"]
			self.assertEqual((feed, return_wire, connection, triac, fuse), (wiring["control_wire"], wiring["return_wire"], wiring["control_connection"], wiring["driver_transistor"], wiring["return_component"]), address)
			self.assertIn("runtime.funhouse.fh-l9.gi-test", device["provenance"]["source_refs"])
			self.assertNotIn("quantity", device["physical"])
		for address in (0, 3):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"])
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"])
			self.assertEqual(["cabinet.backglass"], self.gi[address]["roles"])
		self.assertIn("not a playfield branch", self.gi[3]["physical"]["notes"])
		for address, count in ((1, 1), (2, 14), (4, 11)):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"])
			self.assertEqual(count, len(self.gi[address]["spatial"]["placements"]), address)
		# Rudy's spotlight is the RudyShade Light, not the f_refl glow sprites painted on him.
		(spotlight,) = self.gi[1]["spatial"]["placements"]
		self.assertEqual((0.76868, 0.317499), (spotlight["x"], spotlight["y"]))
		self.assertIn("forum.pinside.funhouse-gi-orange-string", spotlight["provenance"]["source_refs"])
		lower = {(placement["x"], placement["y"]) for placement in self.gi[4]["spatial"]["placements"]}
		self.assertIn((0.563099, 0.472939), lower)  # LowerGI_B19, the double that shows its bulb mesh
		self.assertIn((0.060409, 0.506492), lower)  # Light38 on BulbFil6
		self.assertNotIn((0.219483, 0.780739), lower)  # LowerGI_B14, a render double of Light33's socket
		# The Bottom_GI render lights below the flippers sit on no bulb in either table.
		self.assertNotIn((0.747153, 0.944086), lower)
		self.assertNotIn((0.175111, 0.944281), lower)
		upper = {(placement["x"], placement["y"]) for placement in self.gi[2]["spatial"]["placements"]}
		self.assertNotIn((0.523551, 0.112567), upper)  # Light22, a render light under no bulb
		self.assertIn("forum.pinside.funhouse-gi-violet-string", self.gi[4]["provenance"]["source_refs"])

	def test_gi_sockets_are_bulbs_the_revision_table_models(self) -> None:
		import curate_funhouse as curator

		for address in (2, 4):
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual([position for _, _, position in curator.GI_SOCKETS[address]], [(item["x"], item["y"]) for item in placements])
			for placement in placements:
				self.assertIn("vpx-table.fh-2-0c", placement["provenance"]["source_refs"])
			self.assertEqual(len(placements), len({bulb for _, bulb, _ in curator.GI_SOCKETS[address]}))
		source_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not source_root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		root = Path(source_root)
		curator.verify_extraction_manifest(root)
		curator.verify_revision_manifest(root)
		self.assertEqual((curator.GI_SOCKETS, curator.GI_UNMATCHED), curator.derive_gi_sockets(root))

	def test_gi_runtime_evidence_pins_every_rom_screen(self) -> None:
		evidence = load_json(RUNTIME_PATH)
		runtime = evidence["runtime"]
		self.assertEqual("fh_l9", runtime["game"])
		self.assertEqual("97aa922bf8e4b6970126192ec1ac1fb0305a4f62", runtime["emulator"]["built_from_revision"])
		self.assertEqual(hashlib.sha256(SCENARIO_PATH.read_bytes()).hexdigest(), runtime["raw_runs"][0]["scenario_sha256"])
		labels = [item["label"] for item in runtime["observations"]["named_action_observations"]]
		for address, screens in (
			(0, "BACKGLASS UPPER: Up steps the brightness of public GI 0 alone, and Start then Up show WHT-BRN BRN / P.F. J120-7 120-1 / B.B. J121-7 121-1 / F110 5 AMP S.B. / DRIVER Q18"),
			(1, "RUDY / BACKGLASS: Up steps the brightness of public GI 1 alone, and Start then Up show WHT-ORN ORN / P.F. J120-8 120-2 / B.B. J121-8 121-2 / F109 5 AMP S.B. / DRIVER Q10"),
			(2, "REAR PLAYFIELD: Up steps the brightness of public GI 2 alone, and Start then Up show WHT-YEL YEL / P.F. J120-9 120-3 / B.B. J121-9 121-3 / F108 5 AMP S.B. / DRIVER Q14"),
			(3, "BACKGLASS CENTER: Up steps the brightness of public GI 3 alone, and Start then Up show WHT-GRN GRN / P.F. J120-10 120-5 / B.B. J121-10 121-5 / F107 5 AMP S.B. / DRIVER Q16"),
			(4, "FRONT PLAYFIELD: Up steps the brightness of public GI 4 alone, and Start then Up show WHT-VIO VIO / P.F. J120-11 120-6 / B.B. J121-11 121-6 / F106 5 AMP S.B. / DRIVER Q12"),
		):
			self.assertIn(f"T.6 circuit {screens}", labels, address)
		self.assertEqual([0, 1, 2, 3, 4], runtime["observations"]["gi_addresses_seen"])

	def test_runtime_segment_decoding_refuses_a_changed_reading(self) -> None:
		import funhouse_runtime_evidence as builder

		evidence = load_json(RUNTIME_PATH)
		responses = [
			response
			for item in evidence["runtime"]["observations"]["named_action_observations"]
			for response in item.get("display_responses", [])
		]
		# Every retained response decodes to the text it records.
		for response in responses:
			self.assertEqual(response["interpreted_text"], builder.decode(response["segments"]))
		upper = [r for r in responses if r["snapshot_label"] == "String 3 info Up 4 (driver)" and r["display_index"] in (0, 1, 2)]
		snapshot = {"label": "String 3 info Up 4 (driver)", "displays": [{"index": r["display_index"], "segments": r["segments"]} for r in upper]}
		self.assertEqual(3, len(builder._responses(snapshot, (0, 1, 2), "BACKGLASS CENTER")))
		with self.assertRaises(ValueError):
			builder._responses(snapshot, (0, 1, 2), "TOP PLAYFIELD")
		changed = copy.deepcopy(snapshot)
		changed["displays"][0]["segments"][0] = 0x0079  # an E where the line starts with B
		with self.assertRaises(ValueError):
			builder._responses(changed, (0, 1, 2), "BACKGLASS CENTER")

	def test_runtime_builder_reproduces_and_refuses_drift(self) -> None:
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import funhouse_runtime_evidence as builder
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(review_root)
		self.assertEqual(canonical_bytes(builder.build(root)), RUNTIME_PATH.read_bytes())
		run = builder._load_run(root / builder.HARNESS_DIRECTORY / builder.RUN_DIRECTORY)
		builder.build_observations(run)
		# A press that changes another string as well is refused: every brightness step of a circuit and of ALL,
		# the empty press at full brightness, each selection and the return to ALL.
		for label in ("T.6 Up 33", "T.6 Up 14", "T.6 Up 6", "T.6 Up 15", "T.6 Up 7", "T.6 Up 24", "T.6 Up 48"):
			mixed = copy.deepcopy(run)
			step = next(item for item in mixed["steps"] if item["label"] == label)
			number = next(n for n in (2, 0, 3, 5) if n not in {item["number"] for item in step["transitions"]["gis"]})
			step["transitions"]["gis"].append({"number": number, "states": [0, 8]})
			with self.assertRaises(ValueError, msg=label):
				builder.build_observations(mixed)
		# A brightness press that changes nothing is refused too.
		quiet = copy.deepcopy(run)
		next(item for item in quiet["steps"] if item["label"] == "T.6 Up 14")["transitions"]["gis"] = []
		with self.assertRaises(ValueError):
			builder.build_observations(quiet)
		# An info screen swapped in from another circuit is refused.
		swapped = copy.deepcopy(run)
		snapshot = next(item for item in swapped["snapshots"] if item["label"] == "String 3 info Up 3 (fuse)")
		donor = next(item for item in swapped["snapshots"] if item["label"] == "String 1 info Up 3 (fuse)")
		snapshot["displays"] = copy.deepcopy(donor["displays"])
		with self.assertRaises(ValueError):
			builder.build_observations(swapped)

	def test_drawing_check_validates_every_marked_placement(self) -> None:
		import curate_funhouse as curator

		seed = load_json(CALLOUT_SEED_PATH)
		definition, decisions = curator.build_with_decisions()
		self.assertEqual(102, len(decisions["placements"]))
		agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
		self.assertEqual(100, len(agreeing))
		# The two others are second bulbs under an insert the drawing marks once.
		self.assertEqual({"lamp.matrix-53.emitter.2", "device.2-superdog-flashers.emitter.2"}, set(decisions["placements"]) - agreeing)
		for pid in set(decisions["placements"]) - agreeing:
			self.assertIsNone(decisions["placements"][pid]["read"])
		for page in decisions["pages"].values():
			self.assertEqual(8, page["controls"])
			self.assertLessEqual(page["control_loo_max"], 0.05)
		placements = {placement["id"]: placement for collection in ("inputs", "outputs") for device in definition[collection] for placement in (device.get("spatial") or {}).get("placements") or []}
		for pid in agreeing:
			self.assertIn("human-review.funhouse.drawing-callouts", placements[pid]["provenance"]["source_refs"], pid)
		self.assertTrue(set(seed["excluded_checks"]).isdisjoint(seed["checks"]))
		self.assertTrue(set(seed["measurements"]).isdisjoint(seed["checks"]))
		self.assertEqual(hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest(), {source["id"]: source for source in definition["sources"]}["human-review.funhouse.drawing-callouts"]["sha256"])
		# A placement moved off its callout is refused.
		moved = curator.build()
		lamp = next(device for device in moved["outputs"] if device["id"] == "lamp.matrix-17")
		lamp["spatial"]["placements"][0]["y"] = round(lamp["spatial"]["placements"][0]["y"] - 0.1, 6)
		with self.assertRaises(RuntimeError):
			curator.check_against_drawings(moved, seed)

	def test_multiball_release_and_rudy_coils_sit_on_their_parts(self) -> None:
		release = self.solenoids[8]["spatial"]["placements"][0]
		self.assertEqual((0.194789, 0.184393), (release["x"], release["y"]))
		lock = self.switches[28]["spatial"]["placements"][0]
		self.assertLess(abs(release["x"] - lock["x"]) + abs(release["y"] - lock["y"]), 0.05)
		clock_centre = self.lamps[28]["spatial"]["placements"][0]
		self.assertGreater(abs(release["y"] - clock_centre["y"]), 0.3)
		for address in (25, 26, 27, 28):
			(placement,) = self.solenoids[address]["spatial"]["placements"]
			self.assertEqual((0.65028, 0.229335), (placement["x"], placement["y"]), address)
			self.assertIn("PrLids", self.solenoids[address]["physical"]["notes"])
		for address in (21, 22):
			self.assertEqual(self.switches[51]["spatial"]["placements"][0]["x"], self.solenoids[address]["spatial"]["placements"][0]["x"])

	def test_lamps_and_domes_sit_on_their_bulbs_not_glow_sprites(self) -> None:
		import curate_funhouse as curator

		objects = curator.WORLD_BOUNDS["objects"]
		parts = {("lamp", 57): "BulbFil2", ("lamp", 58): "BulbFil1", **{("lamp", address): f"L{address}" for address in (71, 74, 75, 76, 77, 78)}}
		for (_, address), name in parts.items():
			(placement,) = self.lamps[address]["spatial"]["placements"]
			self.assertEqual(tuple(objects[name]["centre"]), (placement["x"], placement["y"]), address)
		for address, name in ((17, "Flasher1"), (23, "Flasher2"), (24, "Flasher6")):
			placement = self.solenoids[address]["spatial"]["placements"][0]
			self.assertEqual(tuple(objects[name]["centre"]), (placement["x"], placement["y"]), address)
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if review_root:
			export = Path(review_root) / "funhouse-1990" / "vpx-world-obj" / "Funhouse (Williams 1990)_1.3.obj"
			self.assertEqual(curator.WORLD_BOUNDS["export_sha256"], hashlib.sha256(export.read_bytes()).hexdigest())
			bounds: dict[str, list[float]] = {}
			current = None
			with export.open(encoding="utf-8") as stream:
				for line in stream:
					if line.startswith("o "):
						current = line[2:].strip()
					elif line.startswith("v ") and current in objects:
						x, y = (float(value) for value in line.split()[1:3])
						box = bounds.setdefault(current, [x, x, y, y])
						box[:] = [min(box[0], x), max(box[1], x), min(box[2], y), max(box[3], y)]
			for name, item in objects.items():
				box = bounds[name]
				self.assertEqual(item["centre"], [round((box[0] + box[1]) / 2 / 964, 6), round((box[2] + box[3]) / 2 / 2162, 6)], name)
		source_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not source_root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		gameitems = Path(source_root) / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		sprites = set()
		for path in gameitems.glob("Flasher.*.json"):
			item = json.loads(path.read_text(encoding="utf-8"))["Flasher"]
			sprites.add((round(item["pos_x"] / 964, 6), round(item["pos_y"] / 2162, 6)))
		for device in [*self.lamps.values(), *(self.solenoids[address] for address in range(17, 25) if address not in (21, 22))]:
			for placement in device.get("spatial", {}).get("placements", []):
				self.assertNotIn((placement["x"], placement["y"]), sprites, placement["id"])

	def test_retained_callout_artifacts_match_the_seed(self) -> None:
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import drawing_callouts

		self.assertGreater(drawing_callouts.verify_retained(load_json(CALLOUT_SEED_PATH), ROOT, None, Path(review_root)), 3)

	def test_displays_and_mechanisms_are_complete(self) -> None:
		self.assertEqual(2, len(self.definition["displays"]))
		for display in self.definition["displays"]:
			self.assertEqual("segment", display["kind"])
			self.assertEqual(16, display["width"])
			self.assertEqual("not_applicable", display["spatial"]["status"])
		self.assertEqual({0, 1}, {display["controller_index"] for display in self.definition["displays"]})
		self.assertEqual({"mechanism.rudy-jaw", "mechanism.rudy-eyes", "mechanism.trap-door", "mechanism.step-gate", "mechanism.ramp-diverter", "mechanism.trough-and-shooters", "mechanism.tunnel-kickout", "mechanism.rudys-hideout", "mechanism.dummy-eject-hole", "mechanism.multiball-lock", "mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.flippers"}, {mechanism["id"] for mechanism in self.definition["mechanisms"]})

	def test_every_device_has_a_validated_or_controlled_spatial_record(self) -> None:
		for collection in (self.switches, self.solenoids, self.lamps, self.gi):
			for device in collection.values():
				spatial = device["spatial"]
				self.assertIn(spatial["status"], {"validated", "not_applicable"}, device["id"])
				for placement in spatial.get("placements", []):
					self.assertEqual("validated", placement["provenance"]["status"], placement["id"])
					for axis in ("x", "y"):
						self.assertGreaterEqual(placement[axis], 0.0)
						self.assertLessEqual(placement[axis], 1.0)
						self.assertLessEqual(len(str(placement[axis]).partition(".")[2]), 6)

	def test_geometric_ordering_regressions(self) -> None:
		switch_x = {address: switch["spatial"]["placements"][0]["x"] for address, switch in self.switches.items() if switch.get("spatial") and switch["spatial"]["status"] == "validated"}
		switch_y = {address: switch["spatial"]["placements"][0]["y"] for address, switch in self.switches.items() if switch.get("spatial") and switch["spatial"]["status"] == "validated"}
		lamp_x = {address: lamp["spatial"]["placements"][0]["x"] for address, lamp in self.lamps.items() if lamp.get("spatial") and lamp["spatial"]["status"] == "validated"}
		self.assertLess(switch_x[41], switch_x[53])
		self.assertLess(switch_x[43], switch_x[52])
		self.assertLess(switch_x[18], switch_x[68])
		self.assertLess(switch_x[68], switch_x[77])
		self.assertLess(switch_x[47], switch_x[62])
		for left, right in zip(range(11, 16), range(12, 17)):
			self.assertLess(lamp_x[left], lamp_x[right])
		self.assertLess(self.lamps[61]["spatial"]["placements"][0]["x"], self.lamps[61]["spatial"]["placements"][1]["x"])
		self.assertLess(self.lamps[82]["spatial"]["placements"][0]["x"], self.lamps[82]["spatial"]["placements"][1]["x"])
		self.assertAlmostEqual(self.lamps[51]["spatial"]["placements"][0]["x"], self.switches[68]["spatial"]["placements"][0]["x"], delta=0.01)

	def test_seed_and_curator_are_deterministic(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
		self.assertFalse(AUTHOR_READY_PATH.exists())
		import curate_funhouse as curator

		curator.check(ROOT)

	def test_curator_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_spatial_audit_matches_curator(self) -> None:
		import curate_funhouse as curator

		report = curator.build_spatial_report(*curator.build_with_decisions())
		self.assertEqual(report, load_json(SPATIAL_REPORT_PATH))
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual("partial", report["status"])
		self.assertEqual([curator.APRON_GI_BLOCKER], report["blockers"])
		self.assertIn("Resolution path:", curator.APRON_GI_BLOCKER)
		self.assertEqual([], report["unresolved"])
		self.assertEqual(36, len(report["excluded_checks"]))
		self.assertEqual(6, len(report["drawing_measurements"]))
		self.assertEqual([0, 3], report["general_illumination"]["backbox_only"])
		self.assertEqual(hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest(), report["source_hashes"]["callout_seed_sha256"])
		self.assertEqual("vpxtool git:v0.33.3", report["extraction"]["vpxtool_version"])
		self.assertEqual(curator.render_spatial_report(report), SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))

	def test_device_identifiers_are_unique(self) -> None:
		identifiers = [device["id"] for device in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_all_committed_excerpts_exist_and_hash_match(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertTrue(path.is_file(), excerpt["path"])
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
				if "image" in excerpt:
					image_path = ROOT / excerpt["image"]
					self.assertTrue(image_path.is_file(), excerpt["image"])
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256(image_path.read_bytes()).hexdigest(), excerpt["image"])


if __name__ == "__main__":
	unittest.main()
