from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
DEFINITION_PATH = ROOT / "machines/author-ready/williams/terminator-2-judgment-day-1991.json"
AUDIT_PATH = ROOT / "reports/spatial/williams/terminator-2-judgment-day-1991.json"
SEED_PATH = ROOT / "tools/seeds/williams/terminator-2-judgment-day-1991-callouts.json"


def load(path: Path) -> dict[str, object]:
	return json.loads(path.read_text(encoding="utf-8"))


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def xy(device: dict[str, object]) -> list[tuple[float, float]]:
	return [(item["x"], item["y"]) for item in device["spatial"]["placements"]]


class Terminator2DefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.audit = load(AUDIT_PATH)

	def test_definition_is_author_ready_with_only_an_ignored_wiring_detail(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual({"validated"}, set(self.definition["coverage"]["dimensions"].values()))
		self.assertFalse((ROOT / "machines/partial/williams/terminator-2-judgment-day-1991.json").exists())
		(conflict,) = self.definition["conflicts"]
		self.assertEqual("conflict.lamp-schematic-connector-labels", conflict["id"])
		self.assertEqual("ignored", conflict["status"])
		for lamp in (item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"):
			self.assertEqual("validated", lamp["provenance"]["status"])
			self.assertIn(f"J137-{lamp['binding']['device'] // 10}", lamp["physical"]["notes"])
			self.assertIn("conflict.lamp-schematic-connector-labels is ignored", lamp["physical"]["notes"])
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				self.assertEqual("validated", device["provenance"]["status"], device["id"])
				self.assertIn(device["spatial"]["status"], {"validated", "not_applicable"}, device["id"])

	def test_switch_matrix_and_controller_inputs_are_complete(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		self.assertEqual(set(range(1, 9)) | {column * 10 + row for column in range(1, 9) for row in range(1, 9)} | set(range(111, 119)), set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		self.assertEqual("constant", switches[24]["kind"])
		self.assertTrue(switches[24]["constant_active"])
		self.assertEqual("constant", switches[24]["spatial"]["reason"])
		self.assertTrue(switches[22]["normally_closed"])
		self.assertEqual(["cabinet.slam-tilt"], switches[21]["roles"])
		self.assertEqual("cabinet_or_service", switches[21]["spatial"]["reason"])
		self.assertEqual("Gun Loaded", switches[31]["label"])
		# The printed matrix itself names both 38 and 47 "Mid Right Stand-up Target".
		self.assertEqual("Mid Right Standup Target", switches[47]["label"])
		self.assertEqual("Top Lane Center", switches[57]["label"])
		self.assertEqual("Shooter", switches[78]["label"])
		self.assertEqual("unused", switches[88]["availability"])
		self.assertIn("Printed WPC switch matrix column 1, row 5", switches[15]["physical"]["notes"])
		self.assertEqual({"namespace": "manual.address", "value": "1-5"}, switches[15]["aliases"][1])

	def test_flipper_buttons_are_the_generic_column_button_bits(self) -> None:
		# t2GameData declares FLIP_SWNO(12,11) with no FLIP_SOL: core_updateSw copies the generic
		# button bits 112/114 into matrix 11/12.
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		for address, matrix, side in ((112, 11, "right"), (114, 12, "left")):
			button = switches[address]
			self.assertEqual("used", button["availability"])
			self.assertEqual([f"flipper.lower.{side}.button"], button["roles"])
			self.assertFalse(button["normally_closed"])
			self.assertEqual("cabinet_or_service", button["spatial"]["reason"])
			self.assertIn(f"copies it to matrix switch {matrix}", button["physical"]["notes"])
			self.assertEqual([f"flipper.lower.{side}.button"], switches[matrix]["roles"])
			self.assertEqual("cabinet_or_service", switches[matrix]["spatial"]["reason"])
			self.assertIn(f"from generic cabinet input {address}", switches[matrix]["physical"]["notes"])
			self.assertIn("cannot be driven directly", switches[matrix]["physical"]["notes"])
		# Nothing synthesizes the EOS bits and no contact is wired; only the FreeWPC build reads the register.
		for address, side in ((111, "right"), (113, "left")):
			eos = switches[address]
			self.assertEqual("optional", eos["availability"])
			self.assertEqual([f"internal.flipper.lower.{side}.eos"], eos["roles"])
			self.assertFalse(eos["normally_closed"])
			self.assertIn("FreeWPC 0.19", eos["physical"]["notes"])
			self.assertEqual("internal_nonvisual", eos["spatial"]["reason"])
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", switches[address]["availability"])
			self.assertEqual(["internal.unused.flipper"], switches[address]["roles"])

	def test_solenoid_12_is_the_fitted_knock_down_coil(self) -> None:
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		knock_down = solenoids[12]
		self.assertEqual(("Knock Down", "coil", "used"), (knock_down["label"], knock_down["kind"], knock_down["availability"]))
		self.assertEqual("SM1-26-600", knock_down["physical"]["part_number"])
		self.assertEqual("A-14908", knock_down["physical"]["assembly_part_number"])
		self.assertEqual({"control_wire": "Brn-Yel", "control_connection": "J127-5", "driver_transistor": "Q52"}, {key: knock_down["wiring"][key] for key in ("control_wire", "control_connection", "driver_transistor")})
		for text in ("Target Knock Down Assembly", "KNOCK DOWN", "Not Used", "no SolCallback(12)"):
			self.assertIn(text, knock_down["physical"]["notes"])
		self.assertIn("runtime.terminator-2.t2-l8.solenoid-flasher-tests", knock_down["provenance"]["source_refs"])
		self.assertNotIn("vpx-script.t2-vpw-0022", knock_down["provenance"]["source_refs"])
		drop_target = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.drop-target")
		self.assertEqual(["device.drop-target", "device.knock-down"], drop_target["actuators"])
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual(("device.knock-down", "switch.matrix-77"), (relationships["relationship.drop-target-knock-down"]["source"], relationships["relationship.drop-target-knock-down"]["destination"]))
		self.assertEqual({"relationship.trough-release", "relationship.drop-target-reset", "relationship.drop-target-knock-down"}, set(relationships))
		excerpt = (ROOT / "evidence/excerpts/williams.terminator-2-judgment-day.1991/drop-target-assembly.md").read_text(encoding="utf-8")
		self.assertIn("| 23. | A-14908 | Target Knock Down Assembly |", excerpt)
		self.assertIn("| c) | SM1-26-600 | Coil Assembly |", excerpt)

	def test_gi_strings_follow_the_rom_test(self) -> None:
		gi = bindings(self.definition, "outputs", "pinmame.output.gi")
		expected = {
			0: ("Top Insert String", "Wht-Brn", "J120-7", "Q18", "TOP INSERT"),
			1: ("Bottom Insert String", "Wht-Orn", "J120-8", "Q10", "BOTTOM INSERT"),
			2: ("Right Playfield String", "Wht-Yel", "J121-9", "Q14", "RIGHT PLAYFIELD"),
			3: ("CPU String", "Wht-Grn", "J121-10", "Q16", "CPU STRING"),
			4: ("Left Playfield String", "Wht-Vio", "J121-11 + J119-1", "Q12", "LEFT PLAYFIELD"),
		}
		self.assertEqual(set(expected), set(gi))
		for address, (label, wire, connection, triac, rom) in expected.items():
			device = gi[address]
			self.assertEqual((label, "used"), (device["label"], device["availability"]))
			self.assertEqual((wire, connection, triac), (device["wiring"]["control_wire"], device["wiring"]["control_connection"], device["wiring"]["driver_transistor"]))
			self.assertIn(rom, device["physical"]["notes"])
			self.assertIn("runtime.terminator-2.t2-l8.gi-test", device["provenance"]["source_refs"])
			# The triac is fixed to its pins on the power driver board, which two other games' tables print.
			for board in ("manual-chart.bally.doctor-who.1992", "manual.bally.the-addams-family.1992.handbook"):
				self.assertIn(board, device["provenance"]["source_refs"])
		for address in (0, 1):
			self.assertEqual(["cabinet.insert-panel"], gi[address]["roles"])
			self.assertEqual("cabinet_or_service", gi[address]["spatial"]["reason"])
		self.assertEqual(4, gi[3]["physical"]["quantity"])
		self.assertEqual("A-14518", gi[3]["physical"]["assembly_part_number"])
		self.assertEqual(["light2", "light3", "light4", "light5"], sorted(item["id"].rsplit(".", 1)[1] for item in gi[3]["spatial"]["placements"]))
		self.assertEqual(20, len(gi[2]["spatial"]["placements"]))
		# A render light over no modelled bulb is not a socket.
		self.assertIn("GI_11", self.audit["general_illumination"]["not_placed"])
		self.assertEqual(7, len(gi[4]["spatial"]["placements"]))
		self.assertTrue(all(x > 0.39 for x, _ in xy(gi[2])))
		self.assertTrue(all(x < 0.27 for x, _ in xy(gi[4])))
		for address in (2, 4):
			self.assertNotIn("quantity", gi[address]["physical"])
		for address in (2, 3, 4):
			for item in gi[address]["spatial"]["placements"]:
				self.assertEqual("validated", item["provenance"]["status"])
				self.assertIn("vpx-table.t2-nfozzy-1-12a", item["provenance"]["source_refs"])
		placed = {item["id"].rsplit(".", 1)[1] for address in (2, 3, 4) for item in gi[address]["spatial"]["placements"]}
		self.assertFalse(placed & {name.lower().replace("_", "-") for name in self.audit["general_illumination"]["not_placed"]})

	def test_outputs_displays_mechanisms_and_variants_are_explicit(self) -> None:
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 51)), set(solenoids))
		self.assertEqual({"used"}, {solenoids[address]["availability"] for address in range(1, 29)})
		for address in (29, 30):
			self.assertEqual(("virtual", "used", ["internal.wpc-state"]), (solenoids[address]["kind"], solenoids[address]["availability"], solenoids[address]["roles"]))
		self.assertEqual(("relay", "used", ["internal.wpc-state", "cabinet.game-on-relay"]), (solenoids[31]["kind"], solenoids[31]["availability"], solenoids[31]["roles"]))
		self.assertEqual("cabinet_or_service", solenoids[31]["spatial"]["reason"])
		self.assertIn("real Game-On solenoid", solenoids[31]["physical"]["notes"])
		self.assertEqual("unused", solenoids[32]["availability"])
		self.assertIn("constant zero", solenoids[32]["physical"]["notes"])
		for address, side, roles in ((45, "Right", ["internal.synthetic-flipper"]), (46, "Right", ["internal.synthetic-flipper", "flipper.lower.right"]), (47, "Left", ["internal.synthetic-flipper"]), (48, "Left", ["internal.synthetic-flipper", "flipper.lower.left"])):
			self.assertEqual(("virtual", "used", roles), (solenoids[address]["kind"], solenoids[address]["availability"], solenoids[address]["roles"]))
			self.assertIn(side, solenoids[address]["label"])
			self.assertEqual("virtual", solenoids[address]["spatial"]["reason"])
		self.assertIn("J109-7", solenoids[46]["physical"]["notes"])
		self.assertIn("J109-5", solenoids[48]["physical"]["notes"])
		self.assertEqual({"unused"}, {solenoids[address]["availability"] for address in (33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50)})
		self.assertEqual(set(row * 10 + column for row in range(1, 9) for column in range(1, 9)), set(lamps))
		# The 2-35 lamp lists, transcribed whole, give every lamp's bulb.
		self.assertEqual({16, 17, 51, 52, 84, 85}, {address for address, lamp in lamps.items() if lamp["physical"].get("part_number") == "#44"})
		self.assertEqual(set(lamps) - {16, 17, 18, 51, 52, 84, 85}, {address for address, lamp in lamps.items() if lamp["physical"].get("part_number") == "#555"})
		self.assertNotIn("part_number", lamps[18]["physical"])
		lamp_list = (ROOT / "evidence/excerpts/williams.terminator-2-judgment-day.1991/lamp-list.md").read_text(encoding="utf-8")
		for address, lamp in lamps.items():
			if address != 18:
				self.assertRegex(lamp_list, rf"\n\| {address} \| {lamp['physical']['part_number']} \|")
		# The manual and the ROM's flasher test agree on 24; the script's missing callback is a table gap.
		self.assertIn("F.L. C. BACKGLASS", solenoids[24]["physical"]["notes"])
		self.assertIn("gap in the table", solenoids[24]["physical"]["notes"])
		self.assertEqual(["cabinet.backbox"], solenoids[24]["roles"])
		self.assertEqual({17: 4, 18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 1, 25: 2, 26: 2, 27: 2}, {address: solenoids[address]["physical"]["quantity"] for address in range(17, 28)})
		for address in (18, 19, 20, 21, 22, 23, 24, 25, 26):
			self.assertIn("half a row lower", solenoids[address]["physical"]["notes"])
		self.assertEqual("J126-4 + J125-2", solenoids[20]["wiring"]["control_connection"])
		self.assertEqual("flasher", solenoids[17]["kind"])
		self.assertEqual("coil", solenoids[28]["kind"])
		self.assertEqual({"control_wire": "Vio-Brn", "control_connection": "J130-1", "driver_transistor": "Q82"}, {key: solenoids[1]["wiring"][key] for key in ("control_wire", "control_connection", "driver_transistor")})
		self.assertEqual("dmd", self.definition["displays"][0]["kind"])
		self.assertEqual(10, len(self.definition["mechanisms"]))
		flippers = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.flippers")
		self.assertEqual(["device.synthetic-lower-right-flipper", "device.synthetic-lower-left-flipper"], flippers["actuators"])
		self.assertEqual({"t2_d2", "t2_d3", "t2_d4", "t2_d6", "t2_d8", "t2_l2", "t2_l2sp1", "t2_l3", "t2_l4", "t2_l6", "t2_l8", "t2_l81", "t2_l82", "t2_l83", "t2_l84", "t2_p2f", "t2_p2g", "t2_f19", "t2_f20", "t2_f32"}, {driver["id"] for driver in self.definition["drivers"]})
		self.assertTrue(all(driver["physical_compatibility"] == "compatible" for driver in self.definition["drivers"] if driver["id"].startswith("t2_f")))
		self.assertFalse((ROOT / "machines/stubs/t2_l8.json").exists())
		self.assertEqual("Data Base 3", lamps[25]["label"])
		self.assertEqual({51: 2, 52: 2}, {address: lamps[address]["physical"]["quantity"] for address in (51, 52)})

	def test_retained_script_semantics_and_spatial_placements_are_exact(self) -> None:
		trough = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.three-ball-trough")
		gun = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.gun-traverse")
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		self.assertIn("18,17,16,15", trough["behavior"])
		knowledge = (ROOT / "knowledge/williams/terminator-2-judgment-day-1991.md").read_text(encoding="utf-8")
		self.assertIn("switch 18 as the outhole/exit and switches 17, 16, and 15 as the three stack seats", knowledge)
		self.assertIn("length 240", gun["behavior"])
		self.assertIn("CurrentPos=aNewPos/3", gun["behavior"])
		self.assertEqual([(0.938104, 0.899932)], xy(switches[78]))
		self.assertEqual([(0.614497, 0.922582)], xy(switches[15]))
		self.assertEqual([(0.48207, 0.184143)], xy(switches[41]))
		# Both factory drawings put the Right Jet on the right-hand bumper and the Bottom Jet on the lowest one.
		self.assertEqual([(0.716717, 0.208798)], xy(switches[42]))
		self.assertEqual([(0.559494, 0.271911)], xy(switches[43]))
		self.assertEqual(xy(switches[42]), xy(solenoids[14]))
		self.assertEqual(xy(switches[43]), xy(solenoids[15]))
		self.assertIn("swaps the two bindings", switches[42]["physical"]["notes"])
		self.assertEqual([(0.206389, 0.738286)], xy(switches[44]))
		self.assertEqual([(0.204672, 0.237459)], xy(switches[61]))
		# SolAPlunger fires Plunger1 (kickback); SolShooter kicks the shooter-lane saucer.
		self.assertEqual([(0.052587, 0.891072)], xy(solenoids[8]))
		self.assertEqual(xy(switches[78]), xy(solenoids[9]))
		self.assertEqual(xy(switches[77]), xy(solenoids[12]))
		self.assertEqual([(0.30151, 0.142518)], xy(lamps[52]))
		self.assertEqual("not_applicable", switches[34]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", switches[34]["spatial"]["reason"])
		self.assertEqual("not_applicable", solenoids[7]["spatial"]["status"])
		self.assertEqual("not_applicable", solenoids[24]["spatial"]["status"])
		for device in [*self.definition["inputs"], *self.definition["outputs"]]:
			for item in device.get("spatial", {}).get("placements", []):
				refs = item["provenance"]["source_refs"]
				self.assertTrue("vpx-table.t2-vpw-0022" in refs or refs == ["manual.williams.terminator-2-judgment-day.1991", "drawing-callouts.terminator-2.2026-10-22"], item["id"])
				self.assertLessEqual(len(str(item["x"]).split(".")[-1]), 6)

	def test_measured_placements_reproduce_from_the_seed(self) -> None:
		import drawing_callouts

		seed = load(SEED_PATH)
		placed = drawing_callouts.placements_of(self.definition)
		self.assertEqual({
			"switch.matrix-62.sensor.2-37-callout-62-leader-end", "switch.matrix-64.sensor.2-37-callout-64-leader-end",
			"device.left-lock-flashlamps.emitter.2-39-balloon-20",
			"device.targets-flashlamps.emitter.2-39-callout-25-upper-socket", "device.targets-flashlamps.emitter.2-39-callout-25-lower-socket",
		}, set(seed["measurements"]))
		for key in seed["measurements"]:
			self.assertEqual(drawing_callouts.measured(seed, key), placed[key])
			self.assertNotIn(key, seed["checks"])
		self.assertEqual({"device.plunger.effect.kicker-sw78", "device.left-lock.effect.kicker-sw51"}, set(seed["excluded_checks"]))
		self.assertFalse(set(seed["excluded_checks"]) & set(seed["checks"]))

	def test_drawing_check_recomputes_from_the_seed_alone(self) -> None:
		import curate_terminator_2_spatial as spatial
		import drawing_callouts

		seed = load(SEED_PATH)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(spatial.located_definition()))
		disagree = {pid: decision for pid, decision in decisions["placements"].items() if not decision["agrees"]}
		self.assertEqual({"device.gun-flashlamps.emitter.f121", "device.hot-dog-flashlamps.emitter.f117"}, set(disagree))
		self.assertTrue(all(decision["read"] is None for decision in disagree.values()))
		self.assertEqual(127, len(decisions["placements"]))
		for page in decisions["pages"].values():
			self.assertEqual(5, page["controls"])
			self.assertLessEqual(page["control_loo_max"], 0.025)
		self.assertEqual(self.audit["drawing_callout_check"]["validated"], 125)
		# A placement moved off its callout is refused.
		moved = spatial.located_definition()
		target = next(device for device in moved["outputs"] if device["id"] == "device.gun-motor")
		target["spatial"]["placements"][0]["x"] = 0.5
		with self.assertRaises(RuntimeError):
			spatial.promote_from_drawings(moved, seed)

	def test_audit_is_author_ready_evidence(self) -> None:
		self.assertEqual("pinmame-spatial-audit", self.audit["format"])
		self.assertEqual("author_ready", self.audit["status"])
		self.assertEqual([], self.audit["unresolved"])
		self.assertEqual([], self.audit["blockers"])
		self.assertTrue(self.audit["extraction"]["fail_closed"])
		self.assertEqual("f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9", self.audit["extraction"]["manifest_sha256"])
		self.assertEqual("ce5765a02329975e00b0e52d9bba1be86eea49f01def99c62221b8621a902213", self.audit["comparison_extraction"]["manifest_sha256"])
		self.assertEqual(hashlib.sha256(SEED_PATH.read_bytes()).hexdigest(), self.audit["source_hashes"]["callout_seed_sha256"])
		self.assertEqual(16, len(self.audit["general_illumination"]["not_placed"]))
		sources = {item["id"]: item for item in self.definition["sources"]}
		manual = sources["manual.williams.terminator-2-judgment-day.1991"]
		self.assertEqual("8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b", manual["sha256"])
		self.assertEqual(24, len(manual["excerpts"]))
		self.assertTrue(all("scanned page rendered at its native resolution" in excerpt["image_derivation"] for excerpt in manual["excerpts"]))
		self.assertEqual("3727bf57102fceb13b9f8e6370bd7bc4fbd2571d95affb7bff34eb7c5f2e9f8c", sources["vpx-table.t2-vpw-0022"]["sha256"])
		self.assertEqual("2bae1ce5cf8c17233b5d4679032d6aa8c81e31ed32b2219a9363ad8cba244ded", sources["vpx-table.t2-nfozzy-1-12a"]["sha256"])
		self.assertEqual(hashlib.sha256(SEED_PATH.read_bytes()).hexdigest(), sources["drawing-callouts.terminator-2.2026-10-22"]["sha256"])

	def test_curator_check_is_clean(self) -> None:
		environment = {**os.environ, "PYTHONPATH": os.pathsep.join(["src", "tools"])}
		result = subprocess.run([sys.executable, "tools/curate_terminator_2.py", "--check"], cwd=ROOT, env=environment, capture_output=True, text=True)
		self.assertEqual(0, result.returncode, result.stdout + result.stderr)

	def test_retained_extractions_rederive_the_gi_sockets_and_skull(self) -> None:
		source_root_value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not source_root_value:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_terminator_2 as semantic
		import curate_terminator_2_spatial as spatial

		source_root = Path(source_root_value)
		self.assertEqual(548, len(semantic.verify_extraction_manifest(source_root)["files"]))
		self.assertEqual(938, len(semantic.verify_nfozzy_manifest(source_root)["files"]))
		spatial.verify_gi_sockets(source_root)
		spatial.verify_skull_mesh(source_root)
		derived = spatial.derive_gi_sockets(source_root)
		self.assertEqual({2: 20, 3: 4, 4: 7}, {address: len(sockets) for address, sockets in derived.items()})
		# Only modelled bulbs make a socket: no evidence label names an nFozzy render light or sprite.
		labels = {label for sockets in derived.values() for *_, evidence in sockets for label in evidence}
		self.assertEqual({"GI_bulbR piece", "GI_bulbL piece", "GIjet_BulbP1", "GIjet_BulbP2", "GIjet_BulbP3", "VPW UpdateGI Case 3"}, labels)

	def test_retained_callout_artifacts_match_the_seed(self) -> None:
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import drawing_callouts

		self.assertGreater(drawing_callouts.verify_retained(load(SEED_PATH), ROOT, None, Path(review_root)), 3)


class Terminator2SolenoidFlasherTestEvidence(unittest.TestCase):
	"""Each test step ties a printed name to the address that pulsed; the raw run is checked when retained."""

	PATH = ROOT / "evidence" / "runtime" / "wpc-alpha" / "terminator-2-t2_l8-solenoid-flasher-tests.json"
	SCENARIO = ROOT / "tools" / "harness-scenarios" / "wpc-alpha" / "t2-solenoid-flasher-tests.json"
	LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"

	def test_the_rom_names_and_pulses_12_and_24(self) -> None:
		evidence = json.loads(self.PATH.read_text(encoding="utf-8"))
		self.assertEqual(["t2_l8"], evidence["driver_ids"])
		runtime = evidence["runtime"]
		self.assertEqual(self.LIBRARY_SHA256, runtime["emulator"]["sha256"])
		(raw,) = runtime["raw_runs"]
		self.assertEqual(hashlib.sha256(self.SCENARIO.read_bytes()).hexdigest(), raw["scenario_sha256"])
		self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
		actions = runtime["observations"]["named_action_observations"]
		pulsed = [item["transitioned_solenoid_addresses"] for item in actions]
		self.assertEqual([[n] for n in range(1, 15)] + [[17]] + [[n] for n in range(18, 28)] + [[17]], pulsed)
		by_address = {item["transitioned_solenoid_addresses"][0]: item["label"] for item in actions}
		self.assertIn("prints KNOCK DOWN", by_address[12])
		self.assertIn("prints F.L. C. BACKGLASS", by_address[24])
		texts = {item["label"]: item["interpreted_text"] for item in runtime["observations"]["diagnostic_snapshots"]}
		self.assertEqual("KNOCK DOWN / T.4 12 REPEAT / BRN-YEL VIO-ORN", texts["T.4 SOLENOID TEST at solenoid 12"])
		self.assertEqual("F.L. C. BACKGLASS / T.5 24 REPEAT / BLU-GRY RED-WHT", texts["T.5 FLASHER TEST at flasher 24"])
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		import build_external_evidence_manifest as manifest

		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		digest = manifest.check_manifest(path.parent, "t2_l8")
		self.assertIn(f"t2_l8/manifest.json SHA-256 {digest}", evidence["source"]["attribution"])
		run = json.loads(path.read_text(encoding="utf-8"))
		self.assertIsNone(run["failure"])
		self.assertEqual(self.LIBRARY_SHA256, run["library_sha256"])
		# The summary and the raw run agree on driver, library and scenario.
		self.assertEqual("t2_l8", run["game"])
		self.assertEqual(runtime["game"], run["game"])
		self.assertEqual(runtime["emulator"]["sha256"], run["library_sha256"])
		self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
		steps = {step["label"]: step for step in run["steps"]}
		for label, address in (("solenoid test up to 12", 12), ("flasher test up to 24", 24)):
			fired = {item["number"] for item in steps[label]["transitions"]["solenoids"] if any(item["states"])}
			self.assertEqual({address}, fired, label)
		raw_frames = {snap["label"]: (snap["displays"][0]["pixel_sha256"], snap["displays"][0]["nonzero_pixels"]) for snap in run["snapshots"] if snap["displays"]}
		summary = {item["label"]: (item["pixel_sha256"], item["nonzero_pixels"]) for item in runtime["observations"]["diagnostic_snapshots"]}
		# Every summary frame is the raw frame of the step it names.
		raw_label = {
			"game identification": "Enter 2 (game identification)",
			"T.4 SOLENOID TEST at solenoid 11": "solenoid test up to 11",
			"T.4 SOLENOID TEST at solenoid 12": "solenoid test up to 12",
			"T.4 SOLENOID TEST at solenoid 13": "solenoid test up to 13",
			"T.5 FLASHER TEST started at flasher 17 (name line dimmed mid-blink)": "Enter 6 (start T.5 at flasher 17)",
			"T.5 FLASHER TEST wrapped back to flasher 17 (name and number in their blink-off phase)": "flasher test up, wrapping to 17",
			"T.5 FLASHER TEST at flasher 23": "flasher test up to 23",
			"T.5 FLASHER TEST at flasher 24": "flasher test up to 24",
			"T.5 FLASHER TEST at flasher 25": "flasher test up to 25",
		}
		self.assertEqual(set(raw_label), set(summary))
		for label, frame in summary.items():
			self.assertEqual(raw_frames[raw_label[label]], frame, label)


class Terminator2GiTestEvidence(unittest.TestCase):
	"""The ROM's T.6 test names each public G.I. string; the compact evidence is rebuilt from the retained run when present."""

	PATH = ROOT / "evidence" / "runtime" / "wpc-alpha" / "terminator-2-t2_l8-gi-test.json"
	SCENARIO = ROOT / "tools" / "harness-scenarios" / "wpc-alpha" / "t2-gi-test.json"

	def test_the_rom_names_each_public_string(self) -> None:
		evidence = load(self.PATH)
		runtime = evidence["runtime"]
		self.assertEqual(["t2_l8"], evidence["driver_ids"])
		self.assertEqual("dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead", runtime["emulator"]["sha256"])
		self.assertEqual("97aa922bf8e4b6970126192ec1ac1fb0305a4f62", runtime["emulator"]["built_from_revision"])
		(raw,) = runtime["raw_runs"]
		self.assertEqual(hashlib.sha256(self.SCENARIO.read_bytes()).hexdigest(), raw["scenario_sha256"])
		self.assertNotIn(b"\r\n", self.SCENARIO.read_bytes())
		self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
		labels = [item["label"] for item in runtime["observations"]["named_action_observations"]]
		for address, name in ((0, "TOP INSERT (WHT-BRN BRN)"), (1, "BOTTOM INSERT (WHT-ORN ORN)"), (2, "RIGHT PLAYFIELD (WHT-YEL YEL)"), (3, "CPU STRING (WHT-GRN GRN)"), (4, "LEFT PLAYFIELD (WHT-VIO VIO)")):
			self.assertIn(f"T.6 {name}: Up steps the brightness of public GI {address} alone", labels)
		self.assertEqual("After the fresh-NVRAM restart the ROM brings public GI 0-4 up from the common reset blanking, keeps 0, 1, 2 and 4 on, and switches public GI 3 from on to off by itself (40 times in this run)", labels[0])
		stimuli = {item["label"]: item["host_stimulus_switch_addresses"] for item in runtime["observations"]["named_action_observations"]}
		self.assertEqual([7], stimuli["T.6 ALL ILLUMINATION steps the brightness of public GI 0, 1, 2, 3 and 4 together"])
		scenario = load(self.SCENARIO)
		self.assertEqual({7}, {action["switch"] for action in scenario["actions"] if action["label"].startswith("T.6 Up")})
		seed = load(ROOT / "tools/seeds/williams/terminator-2-judgment-day-1991-frames.json")[self.PATH.name]
		self.assertEqual(seed, {item["label"]: {"pixel_sha256": item["pixel_sha256"], "reading": item["interpreted_text"]} for item in runtime["observations"]["diagnostic_snapshots"]})

	def test_the_builder_reproduces_and_refuses_drift(self) -> None:
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import terminator_2_runtime_evidence as builder
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(review_root)
		self.assertEqual(canonical_bytes(builder.build(root)), self.PATH.read_bytes())
		run = builder._load_run(root / builder.HARNESS_DIRECTORY / builder.RUN_DIRECTORY)
		builder.build_observations(run)
		# A string that changes with another one is refused.
		mixed = copy.deepcopy(run)
		step = next(item for item in mixed["steps"] if item["label"] == "T.6 Up 34")
		step["transitions"]["gis"].append({"number": 2, "states": [0, 8]})
		with self.assertRaises(ValueError):
			builder.build_observations(mixed)
		# Another string switching off after the restart is refused; its reset blanking alone is not.
		flicker = copy.deepcopy(run)
		restart = next(item for item in flicker["steps"] if item["label"] == builder.RESTART_LABEL)
		next(item for item in restart["transitions"]["gis"] if item["number"] == 2)["states"].extend([0, 8])
		with self.assertRaises(ValueError):
			builder.build_observations(flicker)
		# A reading pinned to another frame is refused.
		swapped = copy.deepcopy(run)
		snapshot = next(item for item in swapped["snapshots"] if item["label"] == "T.6 Up 33 (held)")
		donor = next(item for item in swapped["snapshots"] if item["label"] == "T.6 Up 41 (held)")
		snapshot["displays"] = copy.deepcopy(donor["displays"])
		with self.assertRaises(ValueError):
			builder._check_pinned_frames(builder.build_observations(swapped))


if __name__ == "__main__":
	unittest.main()
