from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_harley_davidson as curator  # noqa: E402
import harley_davidson_runtime_evidence as evidence_tool  # noqa: E402
import harley_davidson_spatial_seed as seed_tool  # noqa: E402

MACHINE_ID = "stern.harley-davidson.1999"
DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "harley-davidson-1999.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "harley-davidson-1999.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "harley-davidson-1999.md"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "harley-davidson-1999-spatial.json"
EVIDENCE_A40_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "harley-davidson-harl-a40-motorcycle-and-gameplay.json"
EVIDENCE_A30_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "harley-davidson-harl-a30-gameplay.json"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / MACHINE_ID

DRIVER_IDS = {f"harl_{language}{version}" for language in "afgil" for version in ("18", "30", "40")}
# The Switch Matrix Grid's NOT USED cells (excerpt switch-matrix.md), and the Lamp Matrix Grid's (lamp-matrix.md).
NOT_USED_SWITCHES = {9, 10, 38, 39, 40, 47, 63, 64}
NOT_USED_LAMPS = {52, 53, 54, 55, 56, 60, 61, 62, 63, 64} | set(range(73, 81))
# Printed NOT USED, yet both exercised ROMs drive them during play.
UNRESOLVED_LAMPS = {52, 53, 54}
# The UK-only left cabinet button and the coin-door positions beyond the three stock slots.
OPTIONAL_SWITCHES = {1, 2, 3, 7}
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
# The Stern record's own text names the Sega record's two root drivers, to tell the machines apart.
SEGA_DRIVERS = {"harl_a10", "harl_a13"}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def steps(path: Path, run: str) -> dict[str, dict]:
	prefix = f"{run} "
	return {item["label"].split(": ", 1)[1].split(";")[0]: item for item in load(path)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith(prefix)}


def raw_run(name: str) -> dict:
	return load(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / name / "run.json")


def rises(run: dict, kind: str, number: int) -> list[float]:
	return [event["time_s"] for event in run["events"] if event["event"] == kind and event["number"] == number and event["state"] and not event.get("initial")]


class HarleyDavidsonTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, 4455, "G56lO-MDXpW", 1999, "PINBALL-HD"), (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["year"], machine["model_number"]))
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual(dict.fromkeys(DRIVER_IDS, "identical"), compatibility)
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["output_semantics", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["semantic_naming"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])
		catalog = load(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID}
		self.assertEqual(DRIVER_IDS, claimed)
		# Sega's own machine keeps its own drivers.
		self.assertTrue(SEGA_DRIVERS <= {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == "sega.harley-davidson.1999"})

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		def addresses(group: str) -> set[int]:
			return {item["binding"]["device"] for item in self.definition["inputs"] + self.definition["outputs"] if item["binding"]["group"] == group}
		self.assertEqual(set(range(-3, 1)) | set(range(1, 65)) | set(range(81, 89)), addresses("pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), addresses("pinmame.input.dip"))
		self.assertEqual(set(range(1, 51)), addresses("pinmame.output.solenoid"))
		self.assertEqual(set(range(1, 81)), addresses("pinmame.output.lamp"))
		self.assertEqual({0}, addresses("pinmame.output.gi"))
		keys = [(item["binding"]["group"], item["binding"]["device"]) for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(keys), len(set(keys)))

	def test_unused_optional_and_unresolved_cells_follow_the_grids(self) -> None:
		unused = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "unused"}
		self.assertEqual(NOT_USED_SWITCHES, unused)
		optional = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "optional"}
		self.assertEqual(OPTIONAL_SWITCHES, optional)
		self.assertEqual("used", self.device("input.switch", 8)["availability"])
		self.assertEqual(NOT_USED_LAMPS - UNRESOLVED_LAMPS, {address for address in range(1, 81) if self.device("output.lamp", address)["availability"] == "unused"})
		for address in UNRESOLVED_LAMPS:
			lamp = self.device("output.lamp", address)
			self.assertEqual(("unknown", "candidate"), (lamp["availability"], lamp["provenance"]["status"]), address)
			self.assertNotIn("spatial", lamp)
			self.assertIn("Resolution path:", lamp["physical"]["notes"])
		self.assertEqual({8, 21, 22, 24}, {address for address in range(1, 51) if self.device("output.solenoid", address)["availability"] == "optional"})
		self.assertEqual("unused", self.device("input.switch", 88)["availability"])
		self.assertEqual({1, 2, 3, 4, 5}, {address for address in range(1, 9) if self.device("input.dip", address)["availability"] == "used"})

	def test_polarity_follows_the_read_path_and_the_wiring_diagrams(self) -> None:
		for address in range(1, 65):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertTrue(self.device("input.switch", 81)["normally_closed"])
		self.assertTrue(self.device("input.switch", 83)["normally_closed"])
		for address in (82, 84, -3, -2, -1, 0):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertEqual({11, 12, 13, 14, 36}, {address for address in range(1, 65) if self.device("input.switch", address).get("initial_active")})
		self.assertTrue(self.device("input.switch", -3)["initial_active"])
		for address in (14, 15, 37):
			self.assertEqual("opto", self.device("input.switch", address)["physical"]["switch_type"], address)
		for address in (16, 28):
			self.assertEqual("unknown", self.device("input.switch", address)["physical"]["switch_type"], address)
		self.assertIn(curator.RUNTIME_SOURCE, self.device("input.switch", 15)["provenance"]["source_refs"])

	def test_flipper_remap_and_synthetic_states(self) -> None:
		left = self.device("output.solenoid", 48)
		right = self.device("output.solenoid", 46)
		self.assertEqual(("device.q15-left-flipper", "coil"), (left["id"], left["kind"]))
		self.assertEqual(("device.q16-right-flipper", "coil"), (right["id"], right["kind"]))
		for address in (15, 45, 47):
			self.assertEqual(("virtual", "used"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		for address in (16, *range(33, 45), 49, 50):
			self.assertEqual(("virtual", "unused"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		flashers = {address for address in range(1, 33) if self.device("output.solenoid", address)["kind"] == "flasher"}
		# The coil chart's FLASH rows: the scoop flasher Q20 and F1-F8 at Q25-Q32.
		self.assertEqual({20, 25, 26, 27, 28, 29, 30, 31, 32}, flashers)
		self.assertEqual(("relay", "motor", "magnet"), tuple(self.device("output.solenoid", address)["kind"] for address in (19, 13, 14)))

	def test_only_harl_a30_publishes_the_game_on_state(self) -> None:
		a30 = steps(EVIDENCE_A30_PATH, "harl-a30-gameplay")
		a40 = steps(EVIDENCE_A40_PATH, "harl-a40-gameplay")
		served = "the served ball rests on the shooter lane switch 16"
		self.assertIn(15, a30[served]["active_solenoid_addresses"])
		self.assertNotIn(15, a40[served]["active_solenoid_addresses"])
		self.assertIn(15, load(EVIDENCE_A30_PATH)["runtime"]["observations"]["solenoid_addresses_seen"])
		self.assertNotIn(15, load(EVIDENCE_A40_PATH)["runtime"]["observations"]["solenoid_addresses_seen"])
		self.assertEqual([15], a30["behind top VUK (metal under-trough) (public 48) closed once"]["transitioned_solenoid_addresses"])

	def test_wiring_comes_from_the_printed_tables(self) -> None:
		trough = self.device("output.solenoid", 1)["wiring"]
		self.assertEqual(("Q1", "BRN-BLK", "J8-P1", "YEL-VIO", "J10-P4/5", 50), (trough["driver_transistor"], trough["control_wire"], trough["control_connection"], trough["power_wire"], trough["power_connection"], trough["nominal_voltage_v"]))
		self.assertNotIn("nominal_voltage_v", self.device("output.solenoid", 13)["wiring"])
		self.assertEqual(("VIO-ORG", "J7-P4", 20), tuple(self.device("output.solenoid", 19)["wiring"][key] for key in ("control_wire", "control_connection", "nominal_voltage_v")))
		self.assertEqual("J7-P10", self.device("output.solenoid", 24)["wiring"]["control_connection"])
		switch = self.device("input.switch", 54)["wiring"]
		self.assertEqual(("GRN-VIO", "CN5-P8", "WHT-BLU", "CN7-P3"), (switch["drive_wire"], switch["drive_connection"], switch["return_wire"], switch["return_connection"]))
		for address, wire, pin in ((1, "WHT-BRN", "CN7-P9"), (8, "WHT-GRY", "CN7-P1")):
			wiring = self.device("input.switch", address)["wiring"]
			self.assertEqual((wire, pin), (wiring["return_wire"], wiring["return_connection"]), address)
		lamp = self.device("output.lamp", 80)["wiring"]
		self.assertEqual(("YEL-GRY", "J13-P1", "RED", "J12-P11"), (lamp["drive_wire"], lamp["drive_connection"], lamp["return_wire"], lamp["return_connection"]))
		# The cabinet diagram's Launch button lamp: RED-BLU to J12-6 and YEL-VIO to J13-3, the grid's row 6 and column 7.
		launch = self.device("output.lamp", 47)["wiring"]
		self.assertEqual(("YEL-VIO", "J13-P3", "RED-BLU", "J12-P6"), (launch["drive_wire"], launch["drive_connection"], launch["return_wire"], launch["return_connection"]))

	def test_mechanisms_reference_declared_devices(self) -> None:
		ids = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= ids, mechanism["id"])
		by_id = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		self.assertTrue({"mechanism.trough", "mechanism.motorcycle-lift", "mechanism.kick-out-trough", "mechanism.super-vuk", "mechanism.scoop", "mechanism.uk-post-save", "mechanism.stop-light"} <= set(by_id))
		lift = by_id["mechanism.motorcycle-lift"]
		self.assertEqual(("motorized", ["device.q19-motor-relay"]), (lift["kind"], lift["actuators"]))
		self.assertEqual({"mechanism.motorcycle-lift.up": ["switch.35-motor-up"], "mechanism.motorcycle-lift.down": ["switch.36-motor-down"]}, {position["id"]: position["sensors"] for position in lift["positions"]})
		self.assertEqual([], self.definition["relationships"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		self.assertEqual(set(), declared - cited - {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE, curator.ROM_SOURCE, curator.ROM_A30_SOURCE})
		paths = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], sha256(ROOT / excerpt["path"]), excerpt["id"])
				self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])
				paths.add(Path(excerpt["path"]).name)
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], sha256(ROOT / excerpt["image"]), excerpt["id"])
					paths.add(Path(excerpt["image"]).name)
		self.assertEqual({path.name for path in EXCERPT_DIRECTORY.iterdir()}, paths)

	def test_committed_text_names_no_other_machine(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID and len(driver["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		words = set(re.findall(r"[a-z0-9_]{5,}", "\n".join(texts)))
		# Relay 19's "white diamond" is the coil location drawing's marker shape, not a reference to the driver of that name.
		self.assertEqual(set(), words & foreign - SEGA_DRIVERS - {"diamond"})

	def test_placements_are_in_range_unique_and_from_the_seed(self) -> None:
		seed = load(SEED_PATH)
		self.assertEqual(curator.TABLE_SHA256, seed["table"]["sha256"])
		placement_ids = []
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			self.assertEqual("observed", spatial["status"], item["id"])
			for placement in spatial["placements"]:
				placement_ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
		self.assertEqual(len(placement_ids), len(set(placement_ids)))
		missing = {(item["binding"]["group"], item["binding"]["device"]) for item in self.definition["inputs"] + self.definition["outputs"] if item.get("availability") in {"used", "optional"} and "spatial" not in item}
		expected = {("pinmame.input.switch", 27)} | {("pinmame.output.lamp", address) for address in (57, 58, 59, 72)} | {("pinmame.output.solenoid", address) for address in (20, 25, 27, 29, 30, 31, 32)}
		self.assertEqual(expected, missing)
		self.assertEqual(sorted(self.by_binding[key]["id"] for key in expected), load(curator.SPATIAL_REPORT_PATH)["without_placements"])
		gi = self.device("output.gi", 0)
		self.assertEqual(20, len(gi["spatial"]["placements"]))
		self.assertEqual(40, gi["physical"]["quantity"])
		self.assertEqual(2, len(self.device("output.lamp", 70)["spatial"]["placements"]))
		for address in (26, 28):
			self.assertEqual(2, len(self.device("output.solenoid", address)["spatial"]["placements"]), address)

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_scenarios_name_only_their_game_and_evidence_pins_its_runs(self) -> None:
		manifests = {}
		for path, game, rom in ((EVIDENCE_A40_PATH, "harl_a40", curator.ROM_ARCHIVE_SHA256), (EVIDENCE_A30_PATH, "harl_a30", curator.ROM_A30_ARCHIVE_SHA256)):
			document = load(path)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
			self.assertEqual(curator.RUNTIME_LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
			self.assertEqual(rom, document["runtime"]["rom_archive_sha256"])
			self.assertEqual(curator.PINMAME_REVISION, document["source"]["revision"])
			relative = path.relative_to(ROOT).as_posix()
			self.assertEqual((game, rom), evidence_tool.DOCUMENTS[relative][:2])
			self.assertEqual(set(evidence_tool.DOCUMENTS[relative][2]), {run["name"] for run in document["runtime"]["raw_runs"]})
			manifests.update({name: value[0] for name, value in evidence_tool.DOCUMENTS[relative][2].items()})
			for run in document["runtime"]["raw_runs"]:
				scenario = ROOT / run["scenario_path"]
				self.assertEqual(run["scenario_sha256"], sha256(scenario), run["name"])
				self.assertEqual(game, load(scenario)["game"])
				self.assertNotIn(b"\r", scenario.read_bytes(), run["name"])
		self.assertEqual(manifests, curator.RUN_MANIFESTS)

	def test_gameplay_steps_support_the_switch_to_coil_claims(self) -> None:
		for path, run in ((EVIDENCE_A40_PATH, "harl-a40-gameplay"), (EVIDENCE_A30_PATH, "harl-a30-gameplay")):
			observed = steps(path, run)
			expected = {
				"left turbo bumper (public 49) closed once": {9, 13}, "right turbo bumper (public 50) closed once": {10, 13, 27},
				"bottom turbo bumper (public 51) closed once": {11, 13, 27}, "top turbo bumper (public 52) closed once": {12, 13, 27},
				"left slingshot (public 59) closed once": {13, 17, 25}, "right slingshot (public 62) closed once": {13, 18, 31},
				"right ramp enter (public 25) closed once": {32}, "right ramp mid (public 27) closed once": {32},
				"right ramp exit (public 26) closed once": {13, 28}, "spinner (public 28) closed once": {13},
				"right orbit (public 34) closed once": {26}, "left outlane (public 57) closed once": {25},
				"left return lane (public 58) closed once": {13, 28}, "right outlane (public 60) closed once": {31},
				"right return lane (public 61) closed once": {13, 31}, "Start button (public 54)": {1},
				"left 4-bank drop target (public 20) knocked down and left down": {6}, "right 4-bank drop target (public 24) knocked down and left down": {7},
				"coin 1 on the center coin slot (public 5)": {24, 27}, "left flipper button (public 84) held 1.5 s": {47, 48},
				"right flipper button (public 82) held 1.5 s": {45, 46},
			}
			for label, coils in expected.items():
				self.assertTrue(coils <= set(observed[label]["active_solenoid_addresses"]), (run, label))
			for address in (29, 30, 31, 32):
				label = next(key for key in observed if f"(public {address}) closed once" in key)
				self.assertEqual([13, 30], observed[label]["active_solenoid_addresses"], (run, address))
			for address in (17, 18, 19):
				self.assertEqual([], observed[f"left 4-bank drop target (public {address}) knocked down and left down"]["active_solenoid_addresses"], (run, address))
			self.assertEqual([], observed["left orbit (public 33) closed once"]["active_solenoid_addresses"], run)
			self.assertEqual([], observed["behind top VUK (metal under-trough) (public 48) closed once"]["active_solenoid_addresses"], run)
			self.assertIn(23, observed["right cabinet button (public 8, the USA up/down post button) held 1.5 s"]["active_solenoid_addresses"], run)
			self.assertIn(3, observed["a ball enters the super VUK (public 45) and stays"]["active_solenoid_addresses"], run)
			# The scoop hold later in a game drew no kick; the motorcycle trough hold drew no Q5 and switched relay 19 off.
			self.assertNotIn(4, observed["a ball enters the power scoop (public 46) and stays"]["active_solenoid_addresses"], run)
			trough = observed["a ball reaches the bottom of the motorcycle kick-out trough (public 44) and stays"]
			self.assertEqual(([1, 13, 29, 30], [1, 13, 19, 29, 30]), (trough["active_solenoid_addresses"], trough["transitioned_solenoid_addresses"]), run)
			self.assertEqual({1, 13, 25, 26, 27, 28, 29, 30, 31, 32}, set(observed["the ball drains: trough position 11 fills again"]["active_solenoid_addresses"]), run)
		launch = steps(EVIDENCE_A40_PATH, "harl-a40-launch-scoop-opto")
		self.assertEqual([4, 20], launch["a ball enters the power scoop (public 46) and stays, with no other switch closed"]["active_solenoid_addresses"])
		for label in ("motorcycle enter opto (public 37) pulsed to 1 once, with the power scoop empty", "motorcycle enter opto (public 37) pulsed to 1 a second time"):
			self.assertEqual([], launch[label]["active_solenoid_addresses"], label)
		self.assertEqual([], launch["Launch button (public 53) pressed once with the ball still on the shooter lane switch 16"]["active_solenoid_addresses"])
		for path in (EVIDENCE_A40_PATH, EVIDENCE_A30_PATH):
			observations = load(path)["runtime"]["observations"]
			self.assertFalse(set(observations["solenoid_addresses_seen"]) & {5, 8, 21, 22}, path.name)
			lamps = set(observations["lamp_addresses_seen"])
			self.assertTrue(UNRESOLVED_LAMPS <= lamps, path.name)
			self.assertFalse(lamps & (NOT_USED_LAMPS - UNRESOLVED_LAMPS), path.name)
			self.assertNotIn(47, lamps, path.name)

	def test_ds5_probe_shows_the_rom_ignores_input_88(self) -> None:
		self.assertIn(curator.RUNTIME_SOURCE, self.device("input.switch", 88)["provenance"]["source_refs"])
		probe = steps(EVIDENCE_A40_PATH, "harl-a40-ds5-probe")
		holds = [label for label in probe if label.startswith("dedicated input 88 (DS-5) held 1.5 s")]
		self.assertEqual(4, len(holds))
		for label in holds:
			self.assertEqual([], probe[label]["active_solenoid_addresses"], label)
			self.assertEqual(88, probe[label]["input_address"], label)
		self.assertEqual([23], probe["right cabinet button (public 8, the USA up/down post button) held 1.5 s as the control"]["active_solenoid_addresses"])

	def test_dedicated_switch_test_names_ds5_not_used(self) -> None:
		prefix = "harl-a40-dedicated-switch-test snapshot: "
		snapshots = {item["label"].removeprefix(prefix): item for item in load(EVIDENCE_A40_PATH)["runtime"]["observations"]["diagnostic_snapshots"]}
		pins = load(ROOT / "tools/seeds/stern/harley-davidson-1999-frame-readings.json")["runs"]
		self.assertEqual({"harl-a40-dedicated-switch-test"}, set(pins))
		self.assertEqual(set(pins["harl-a40-dedicated-switch-test"]), set(snapshots))
		for label, pin in pins["harl-a40-dedicated-switch-test"].items():
			self.assertEqual((pin["pixel_sha256"], pin["reading"]), (snapshots[label]["pixel_sha256"], snapshots[label]["interpreted_text"]), label)
		not_used = "DEDICATED SWITCH TEST / #5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK / PRESS START TO EXIT TEST"
		self.assertEqual(not_used, snapshots["dedicated input 88 (DS-5) held in the Dedicated Switch Test"]["interpreted_text"])
		self.assertEqual(not_used, snapshots["dedicated input 88 (DS-5) still held"]["interpreted_text"])
		self.assertIn("#1 LEFT FLIPPER BUTTON / CN6-2 GRY-BRN", snapshots["left flipper button (public 84) held in the Dedicated Switch Test"]["interpreted_text"])
		self.assertIn("#3 RIGHT FLIPPER BUTTON / CN6-4 GRY-ORG", snapshots["right flipper button (public 82) held in the Dedicated Switch Test"]["interpreted_text"])
		for label in ("left flipper button (public 84) released", "dedicated input 88 (DS-5) released", "right flipper button (public 82) released"):
			self.assertIn("/ NONE /", snapshots[label]["interpreted_text"], label)
		self.assertIn("'#5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK'", self.device("input.switch", 88)["physical"]["notes"])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained harness runs are not available")
	def test_frame_readings_refuse_a_substituted_frame(self) -> None:
		root = evidence_tool.review_artifacts_root(required=True)
		game, rom, runs = evidence_tool.DOCUMENTS[EVIDENCE_A40_PATH.relative_to(ROOT).as_posix()]
		original = evidence_tool._load_run

		def swapped(*args):
			run, listed = original(*args)
			if args[1] == "harl-a40-dedicated-switch-test":
				labels = [item["label"] for item in run["snapshots"]]
				held = labels.index("dedicated input 88 (DS-5) held in the Dedicated Switch Test")
				run["snapshots"][held]["displays"] = run["snapshots"][labels.index("left flipper button (public 84) held in the Dedicated Switch Test")]["displays"]
			return run, listed

		with mock.patch.object(evidence_tool, "_load_run", swapped):
			with self.assertRaisesRegex(RuntimeError, "does not carry the frame the curator read"):
				evidence_tool.build(root, game, rom, runs)

	def test_motorcycle_runs_support_the_lift_claims(self) -> None:
		home = steps(EVIDENCE_A40_PATH, "harl-a40-motorcycle-home-search")
		self.assertEqual([19], home["wait for the motor relay with neither motorcycle position switch closed"]["active_solenoid_addresses"])
		up = steps(EVIDENCE_A40_PATH, "harl-a40-motorcycle-up-at-boot")
		self.assertEqual([19], up["wait for the motor relay with the Motor Up switch 35 closed"]["active_solenoid_addresses"])
		down = steps(EVIDENCE_A40_PATH, "harl-a40-motorcycle-down-at-boot")
		self.assertTrue(all(item["active_solenoid_addresses"] == [] for item in down.values()))
		lift = steps(EVIDENCE_A40_PATH, "harl-a40-motorcycle-ball-start-lift")
		self.assertIn(19, lift["the served ball reaches the shooter lane switch 16"]["active_solenoid_addresses"])
		self.assertIn(19, lift["the motorcycle reaches the up position: public 35 raised to 1"]["transitioned_solenoid_addresses"])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		for relative, (game, rom, runs) in evidence_tool.DOCUMENTS.items():
			self.assertEqual(canonical_bytes(evidence_tool.build(root, game, rom, runs)), (ROOT / relative).read_bytes(), relative)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_retry_counts_behind_the_operator_alert_notes(self) -> None:
		# The notes say: an auto-launch kick 40 ms after the ball arrives, another 2.3 s later and eight more about 0.5 s
		# apart; and ten scoop kicks, the first about 1.1 s after the ball arrives and then every 0.75 s.
		run = raw_run("harl-a40-launch-scoop-opto")
		ball = rises(run, "switch", 16)[0]
		launches = [time for time in rises(run, "solenoid", 2) if ball <= time < ball + 10]
		self.assertEqual(10, len(launches))
		self.assertAlmostEqual(0.04, launches[0] - ball, delta=0.02)
		self.assertAlmostEqual(2.3, launches[1] - launches[0], delta=0.1)
		self.assertTrue(all(0.4 <= later - earlier <= 0.6 for earlier, later in zip(launches[1:], launches[2:])))
		scoop = rises(run, "switch", 46)[0]
		kicks = [time for time in rises(run, "solenoid", 4) if scoop <= time < scoop + 15]
		self.assertEqual(10, len(kicks))
		self.assertAlmostEqual(1.1, kicks[0] - scoop, delta=0.1)
		self.assertTrue(all(0.65 <= later - earlier <= 0.85 for earlier, later in zip(kicks, kicks[1:])))
		self.assertEqual(3, len([time for time in rises(run, "solenoid", 20) if scoop <= time < kicks[0]]))

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_unresolved_lamps_light_only_during_play(self) -> None:
		for name in ("harl-a40-gameplay", "harl-a30-gameplay"):
			run = raw_run(name)
			start = rises(run, "switch", 54)[0]
			ball = rises(run, "switch", 16)[0]
			for address in UNRESOLVED_LAMPS:
				lit = rises(run, "lamp", address)
				self.assertTrue(lit, (name, address))
				self.assertGreater(min(lit), ball, (name, address))
				self.assertGreater(min(lit), start, (name, address))
			for address in (55, 56):
				self.assertEqual([], rises(run, "lamp", address), (name, address))

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_stacking_opto_run_draws_no_coil_in_attract_mode(self) -> None:
		run = raw_run("harl-a40-stacking-opto")
		edges = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event["number"] == 15 and not event.get("initial")]
		self.assertEqual(3, len(edges))
		fired = {event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] >= edges[0]}
		self.assertEqual(set(), fired)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_extraction_script_and_seed_match(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		curator.verify_extraction_manifest(root)
		base = root / "stern/harley-davidson-1999/v1-2"
		table = base / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, sha256(table))
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, sha256(script))
		self.assertEqual(script.read_bytes(), (base / "Harley Davidson (Sega 1999) 1.2.vbs").read_bytes())
		built = seed_tool.canonical(seed_tool.build(root / curator.EXTRACTION_RELATIVE_PATH, table))
		self.assertEqual(built.encode("utf-8"), SEED_PATH.read_bytes())
		code = "\n".join(line for line in script.read_text(encoding="latin-1").splitlines() if not line.strip().startswith("'"))
		self.assertIn('Const cGameName="harl_a30"', code)
		self.assertIn("vpmNudge.TiltSwitch=14", code)
		self.assertIn("bsTrough.InitSw 0,14,13,12,11,0,0,0", code)
		self.assertIn('SolCallback(5)="bsCycle.SolOut"', code)
		# The commented-out callbacks the notes cite never appear in live code.
		for address in (9, 10, 11, 12, 14, 17, 18, 19):
			self.assertNotIn(f"SolCallback({address})", code, address)
		# The avoidance claims behind the stacking-opto, EOS and switch-27 notes: 15 is written only inside SolTrough, which
		# nothing calls; 81 and 83 are never written; and the table has no object named trigger27.
		self.assertEqual(1, len(re.findall(r"PulseSw\s*\(?\s*15\b|Switch\(\s*15\s*\)", code, re.IGNORECASE)))
		self.assertEqual(["Sub SolTrough(Enabled)"], [line.strip() for line in code.splitlines() if "soltrough" in line.casefold()])
		for address in (81, 83):
			self.assertIsNone(re.search(rf"PulseSw\s*\(?\s*{address}\b|Switch\(\s*{address}\s*\)", code, re.IGNORECASE), address)
		names = {path.stem.split(".", 1)[-1].casefold() for path in (root / curator.EXTRACTION_RELATIVE_PATH / "gameitems").glob("*.json")}
		self.assertNotIn("trigger27", names)
		self.assertIn("trigger27q", names)
		self.assertIn("sw25", names)

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_manual_and_bulletin_match_their_pins(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / MACHINE_ID / "ipdb"
		self.assertEqual(curator.MANUAL_SHA256, sha256(root / curator.MANUAL_NAME))
		self.assertEqual(curator.TECH_BRIEF_SHA256, sha256(root / curator.TECH_BRIEF_NAME))


if __name__ == "__main__":
	unittest.main()
