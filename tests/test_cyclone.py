"""Fail-closed tests for the Williams Cyclone (1988) definition.

Each test pins one fact against the evidence that decided it: the ROM's Coil Test, Single Lamps, Switch Levels and
Mystery Wheel tests for names and addresses, pinned PinMAME's Cyclone game data for the A/C bank at 12, the flipper
copy into 57 and 58 and the ROM-fired specials, the manual, parts manual and service bulletins for wiring, parts and
the stepper board, and the retained table for the placements. The retained-evidence class re-derives the compact
evidence from the configured roots and skips cleanly without them.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_cyclone as curator  # noqa: E402
import cyclone_data as data  # noqa: E402
import cyclone_runtime_evidence as runtime_tool  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

MACHINE_ID = "williams.cyclone.1988"
DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "cyclone-1988.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "cyclone-1988.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "cyclone-1988.md"
REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "cyclone-1988.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / MACHINE_ID
RUNTIME_PATHS = {
	"cycln_l5": ROOT / "evidence" / "runtime" / "system-11" / "cyclone-l5-service-and-mechanisms.json",
	"cycln_l4": ROOT / "evidence" / "runtime" / "system-11" / "cyclone-l4-coil-test.json",
	"cycln_l1": ROOT / "evidence" / "runtime" / "system-11" / "cyclone-l1-coil-test.json",
}

DRIVERS = {"cycln_l5", "cycln_l4", "cycln_l1"}
# The Coil Test's pulse order in every revision: A-side n, then C-side n + 24 for steps 1-8, then 9-22 without the
# stepper outputs 13 and 14, which the test skips.
COIL_TEST = [1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22]
# Blank Switch-Matrix Table cells, and the flipper-column positions System 11 publishes but Cyclone wires nowhere.
UNUSED_SWITCHES = {2, 12, 33, 38, 39, 40} | set(range(42, 53)) | {81, 83, 85, 86, 87, 88}
UNUSED_SOLENOIDS = {2, 6, 8, 22, 24} | set(range(33, 45)) | {49, 50}
BACKBOX_LAMPS = set(range(33, 49)) | set(range(55, 65))
UNPLACED_LAMPS = set(range(1, 33)) | set(range(49, 55))
UNPLACED_FLASHERS = {9, 15, 25, 26, 27, 28, 32}
PLACED_FLASHERS = {29, 30, 31}
SPECIALS = {17: 1, 18: 2, 19: 3, 20: 4, 21: 5}
MODEL_NAMES = re.compile(r"\b(claude|opus|sonnet|haiku|anthropic|openai|codex|gpt[- ]?\w*|chatgpt|gemini|copilot)\b", re.IGNORECASE)


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def aliases(device: dict, namespace: str) -> list[str]:
	return [alias["value"] for alias in device.get("aliases", []) if alias["namespace"] == namespace]


def cyclone_files() -> list[Path]:
	paths = [DEFINITION_PATH, KNOWLEDGE_PATH, REPORT_PATH, REPORT_PATH.with_suffix(".md"), *RUNTIME_PATHS.values()]
	paths += sorted(EXCERPTS.iterdir())
	paths += sorted((ROOT / "tools" / "seeds" / "williams").glob("cyclone-1988*"))
	paths += sorted((ROOT / "tools" / "harness-scenarios" / "system-11").glob("cycln-*.json"))
	paths += [ROOT / "tools" / name for name in ("curate_cyclone.py", "cyclone_data.py", "cyclone_rom_name_tables.py", "cyclone_runtime_evidence.py")]
	return paths


class CycloneDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		groups = {}
		for collection in ("inputs", "outputs"):
			for device in cls.definition[collection]:
				groups.setdefault(device["binding"]["group"], {})[device["binding"]["device"]] = device
		cls.switches = groups["pinmame.input.switch"]
		cls.dips = groups["pinmame.input.dip"]
		cls.solenoids = groups["pinmame.output.solenoid"]
		cls.lamps = groups["pinmame.output.lamp"]
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}
		cls.runtime = {game: load(path) for game, path in RUNTIME_PATHS.items()}
		cls.runs = cls.runtime["cycln_l5"]["runtime"]["observations"]["runs"]
		cls.named = cls.runtime["cycln_l5"]["runtime"]["observations"]["named_output_addresses"]

	def test_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_definition_validates_and_stays_honestly_partial(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("observed", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, 617, "G4O2b-MJpn4", "564", 1988), (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["model_number"], machine["year"]))
		self.assertEqual({"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True}, self.definition["controller"])

	def test_driver_tree_is_exactly_the_cyclone_clone_tree(self) -> None:
		self.assertEqual(DRIVERS, {driver["id"] for driver in self.definition["drivers"]})
		self.assertEqual({"identical"}, {driver["physical_compatibility"] for driver in self.definition["drivers"]})
		catalog = load(ROOT / "catalog" / "pinmame.json")
		owners = {driver["id"]: driver.get("machine_id") for driver in catalog["drivers"] if driver["id"].startswith("cycln")}
		self.assertEqual(DRIVERS, set(owners))
		self.assertEqual({MACHINE_ID}, set(owners.values()))

	def test_every_controller_address_is_enumerated(self) -> None:
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		self.assertEqual({0}, set(self.dips))
		self.assertEqual(4, len(self.definition["displays"]))
		self.assertEqual([1, 9, 21, 29], [display["segment_start"] for display in self.definition["displays"]])

	def test_coil_test_walks_the_a_c_bank_in_every_revision(self) -> None:
		for game, document in self.runtime.items():
			observations = document["runtime"]["observations"]
			run = observations["runs"][f"coil-test-{game[-2:]}"]
			self.assertEqual(COIL_TEST, run["ordered_solenoid_on_sequence"], game)
			self.assertEqual(game, document["runtime"]["game"])
			self.assertEqual(data.ROM_ARCHIVE_SHA256[game], document["runtime"]["rom_archive_sha256"])
			self.assertEqual(curator.RUNTIME_MANIFEST_SHA256, document["source"]["sha256"])
			for index, address in enumerate(COIL_TEST):
				step = address if address <= 24 else address - 24
				name = data.ROM_COIL_STEPS[step][1 if address > 24 else 0].replace("p", "/")
				self.assertEqual(address, observations["named_output_addresses"][f"coil-{step:02d}-{slug(name)}"], (game, index))
		self.assertEqual((13, 14), data.COIL_TEST_SKIPPED_STEPS)

	def test_lamp_names_follow_the_single_lamps_test(self) -> None:
		for address in range(1, 65):
			self.assertEqual(address, self.named[f"lamp-{address:02d}-{slug(data.ROM_LAMP_NAMES[address])}"], address)
			self.assertIn(data.ROM_LAMP_NAMES[address], self.lamps[address]["physical"]["notes"] if "physical" in self.lamps[address] else self.lamps[address]["notes"])

	def test_ac_bank_shares_drivers_and_the_relay_is_12(self) -> None:
		for pair in range(1, 9):
			a, c = self.solenoids[pair], self.solenoids[pair + 24]
			self.assertEqual([f"{pair:02d}A"], aliases(a, "manual.address"))
			self.assertEqual([f"{pair:02d}C"], aliases(c, "manual.address"))
			self.assertEqual(a["wiring"]["driver_transistor"], c["wiring"]["driver_transistor"])
			self.assertIn("through the A/C Select Relay", c["wiring"]["control_connection"])
		self.assertEqual("relay", self.solenoids[12]["kind"])
		self.assertEqual("Solenoid A/C Select Relay", self.solenoids[12]["label"])

	def test_special_solenoids_are_fired_by_the_rom_alone(self) -> None:
		self.assertFalse(any("special-solenoid" in relationship["id"] for relationship in self.definition["relationships"]))
		for address, number in SPECIALS.items():
			self.assertEqual([f"Special #{number}"], aliases(self.solenoids[address], "manual.special-solenoid"))
		observed = {item["input_address"]: set(item["transitioned_solenoid_addresses"]) for item in self.runs["gameplay-l5"]["named_action_observations"]}
		for switch, coil in runtime_tool.SPECIAL_RESPONSES.items():
			self.assertIn(coil, observed[switch], switch)
		self.assertEqual({60: 17, 61: 19, 62: 21, 63: 18, 64: 20}, runtime_tool.SPECIAL_RESPONSES)
		self.assertEqual("unused", self.solenoids[22]["availability"])

	def test_flipper_buttons_are_copied_into_the_lane_change_switches(self) -> None:
		relations = {(relationship["source"], relationship["destination"]) for relationship in self.definition["relationships"]}
		self.assertEqual({("switch.flipper-column-82", "switch.matrix-58"), ("switch.flipper-column-84", "switch.matrix-57")}, relations)
		self.assertEqual("Left Flipper Lane Change", self.switches[57]["label"])
		self.assertEqual("Right Flipper Lane Change", self.switches[58]["label"])
		for address in (45, 46, 47, 48):
			self.assertEqual("virtual", self.solenoids[address]["kind"])
			self.assertTrue(self.solenoids[address]["label"].startswith("Synthetic Lower"))

	def test_unused_cells_and_every_fitted_switch_is_normally_open(self) -> None:
		self.assertEqual(UNUSED_SWITCHES, {address for address, device in self.switches.items() if device["availability"] == "unused"})
		self.assertEqual({5}, {address for address, device in self.switches.items() if device["availability"] == "optional"})
		self.assertEqual(UNUSED_SOLENOIDS, {address for address, device in self.solenoids.items() if device["availability"] == "unused"})
		self.assertFalse(any(device.get("normally_closed") for device in self.switches.values()))
		for address in range(1, 65):
			if address not in UNUSED_SWITCHES:
				self.assertIs(False, self.switches[address]["normally_closed"], address)
		for address in (18, 41):
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"])

	def test_mystery_wheel_is_a_two_input_stepper_with_a_home_opto(self) -> None:
		self.assertEqual("Mystery Wheel Stepper Coil B", self.solenoids[13]["label"])
		self.assertEqual("Mystery Wheel Stepper Coil A", self.solenoids[14]["label"])
		for address in (13, 14):
			self.assertEqual("motor", self.solenoids[address]["kind"])
			self.assertEqual("14-7948/D-12045", self.solenoids[address]["physical"]["part_number"])
			self.assertIn(curator.BULLETINS, self.solenoids[address]["provenance"]["source_refs"])
		wheel = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.mystery-wheel")
		self.assertEqual(["switch.matrix-41"], wheel["sensors"])
		self.assertEqual({self.solenoids[13]["id"], self.solenoids[14]["id"]}, set(wheel["actuators"]))
		self.assertEqual("5490-10159-00", self.switches[41]["physical"]["part_number"])
		for address in range(33, 49):
			self.assertTrue(self.lamps[address]["label"].startswith("Mystery Wheel"), address)
		bulletin = (EXCERPTS / "service-bulletins.md").read_text(encoding="utf-8")
		for text in ("Subassembly D-12046", "`input A`", "`input B`", "stepper motor coil A", "Q9 2N3906"):
			self.assertIn(text, bulletin)
		reactive = self.runs["wheel-test-reactive-l5"]["note"]
		self.assertIn("\"home opto closes (synthetic flag)\" (41 = 1): M. WHEEL BLU 1OK |  08Err1 |     098", reactive)
		for name in ("wheel-test-41-0-l5", "wheel-test-41-1-l5", "wheel-test-reactive-l5"):
			self.assertTrue({13, 14} <= set(self.runs[name]["solenoid_addresses_seen"]), name)

	def test_parts_manual_settles_the_kicker_and_bumper_coils(self) -> None:
		for address in (17, 19, 21):
			self.assertEqual("AE-23-800", self.solenoids[address]["physical"]["part_number"], address)
		for address in (4, 18, 20):
			self.assertEqual("AE-26-1500", self.solenoids[address]["physical"]["part_number"], address)
		self.assertEqual("AE-24-900", self.solenoids[3]["physical"]["part_number"])
		for address in (20, 21):
			self.assertIn(curator.PARTS, self.solenoids[address]["provenance"]["source_refs"])
		parts = (EXCERPTS / "parts-assemblies.md").read_text(encoding="utf-8")
		self.assertIn("`AE-26-1500 COIL ASSEMBLY`", parts)
		self.assertIn("| 8 | AE-23-800 | Coil |", parts)
		solenoid_table = (EXCERPTS / "solenoid-table.md").read_text(encoding="utf-8")
		self.assertIn("AE-23-800", solenoid_table)

	def test_backbox_and_unplaced_records_are_exactly_the_disclosed_ones(self) -> None:
		for address in BACKBOX_LAMPS:
			self.assertEqual(("not_applicable", "cabinet_or_service"), (self.lamps[address]["spatial"]["status"], self.lamps[address]["spatial"]["reason"]), address)
		self.assertEqual(UNPLACED_LAMPS, {address for address, device in self.lamps.items() if "spatial" not in device})
		self.assertEqual(UNPLACED_FLASHERS, {address for address, device in self.solenoids.items() if "spatial" not in device})
		for address in PLACED_FLASHERS:
			self.assertEqual("flasher", self.solenoids[address]["kind"])
			self.assertEqual(1, len(self.solenoids[address]["spatial"]["placements"]), address)
		gi = self.solenoids[10]
		self.assertEqual("gi", gi["kind"])
		self.assertEqual(32, len(gi["spatial"]["placements"]))
		self.assertNotIn("quantity", gi["physical"])
		report = load(REPORT_PATH)
		self.assertEqual(len(UNPLACED_LAMPS) + len(UNPLACED_FLASHERS), len(report["unplaced"]))
		self.assertEqual({("switch", 57), ("switch", 58), ("solenoid", 4), ("solenoid", 5), ("solenoid", 16)}, {(item["kind"], item["address"]) for item in report["projections"]})
		self.assertEqual({"status": "partial", "missing": ["spatial_placement"], "unresolved_conflicts": 0}, report["readiness"])

	def test_placements_are_observed_in_range_and_unique(self) -> None:
		identifiers = []
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				spatial = device.get("spatial")
				if not spatial or spatial["status"] == "not_applicable":
					continue
				self.assertEqual("observed", spatial["status"], device["id"])
				for placement in spatial["placements"]:
					identifiers.append(placement["id"])
					self.assertEqual("observed", placement["provenance"]["status"], placement["id"])
					self.assertEqual("playfield", placement["space"])
					for axis in ("x", "y"):
						value = placement[axis]
						self.assertTrue(0 <= value <= 1, placement["id"])
						self.assertEqual(value, round(value, 6), placement["id"])
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_excerpts_are_pinned_reviewed_and_all_cited(self) -> None:
		cited = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
				self.assertTrue(excerpt["reviewed"], excerpt["path"])
				self.assertRegex(excerpt["transcribed_by"], r"^(curator|tools/cyclone_rom_name_tables\.py), ", excerpt["path"])
				cited.add(path.name)
		self.assertEqual({path.name for path in EXCERPTS.iterdir()}, cited)
		self.assertEqual({filename for filename, _ in curator.EXCERPT_FILES.values()}, cited)
		for key, (filename, _) in curator.EXCERPT_FILES.items():
			self.assertEqual(curator.EXCERPT_DIGESTS[key], hashlib.sha256((EXCERPTS / filename).read_bytes()).hexdigest(), key)
			self.assertNotIn(b"\r", (EXCERPTS / filename).read_bytes(), key)

	def test_sources_carry_acquisition_provenance_without_local_paths(self) -> None:
		text = DEFINITION_PATH.read_text(encoding="utf-8")
		for local in ("E:/", "E:\\", "C:\\", "L:/", "L:\\", "Users/"):
			self.assertNotIn(local, text)
		for key, filename in ((curator.MANUAL, curator.MANUAL_FILENAME), (curator.PARTS, curator.PARTS_FILENAME), (curator.BULLETINS, curator.BULLETINS_FILENAME)):
			source = self.sources[key]
			self.assertEqual(f"https://web.archive.org/web/20240406112543id_/https://www.ipdb.org/files/617/{filename}", source["uri"])
			self.assertEqual(filename, source["original_filename"])
			self.assertEqual("ipdb.617", source["source_id"])
			self.assertRegex(source["acquired_at"], r"^2026-10-31T06:\d\d:\d\dZ$")
			self.assertTrue(source["license"] and source["attribution"])
		self.assertEqual((curator.MANUAL_SHA256, curator.PARTS_SHA256, curator.BULLETINS_SHA256), tuple(self.sources[key]["sha256"] for key in (curator.MANUAL, curator.PARTS, curator.BULLETINS)))
		self.assertEqual(curator.IPDB_PAGE_SHA256, self.sources[curator.IPDB]["sha256"])
		self.assertIn("https://web.archive.org/web/20230517161009id_/https://www.ipdb.org/machine.cgi?id=617", self.sources[curator.IPDB]["locator"])
		script = self.sources[curator.SCRIPT]
		self.assertEqual(curator.SCRIPT_SHA256, script["sha256"])
		self.assertEqual(
			"https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Cyclone%20%28Williams%201988%29%20v1.5.vbs",
			script["uri"],
		)

	def test_committed_text_names_no_other_machine_and_no_model(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if not driver["id"].startswith("cycln") and len(driver["id"]) >= 5 and "_" in driver["id"]}
		for path in cyclone_files():
			text = path.read_text(encoding="utf-8")
			words = set(re.findall(r"\b[a-z0-9]+_[a-z0-9_]+\b", text))
			if path.suffix != ".py":
				self.assertEqual(set(), words & foreign, path.name)
			self.assertIsNone(MODEL_NAMES.search(text), path.name)

	def test_scenarios_are_pinned_lf_and_cited_by_the_runs(self) -> None:
		cited = set()
		for game, document in self.runtime.items():
			for run in document["runtime"]["raw_runs"]:
				scenario = ROOT / run["scenario_path"]
				data_bytes = scenario.read_bytes()
				self.assertEqual(run["scenario_sha256"], hashlib.sha256(data_bytes).hexdigest(), run["name"])
				self.assertNotIn(b"\r", data_bytes, run["name"])
				json.loads(data_bytes)
				cited.add(scenario.name)
			self.assertEqual(list(runtime_tool.RUNS[game]), [run["name"] for run in document["runtime"]["raw_runs"]])
		on_disk = {path.name for path in (ROOT / "tools" / "harness-scenarios" / "system-11").glob("cycln-*.json")}
		self.assertEqual(on_disk, cited | {"cycln-nvram-init.json"})
		self.assertNotIn(b"\r", (ROOT / runtime_tool.INIT_SCENARIO).read_bytes())

	def test_frame_pins_refuse_a_substituted_or_reworded_frame(self) -> None:
		pins = load(runtime_tool.FRAME_SEED_PATH)["runs"]
		runtime_tool.check_pins(copy.deepcopy(pins))
		swapped = copy.deepcopy(pins)
		readings = swapped["switch-levels-l5"]
		readings["no switch closed"] = list(readings["hold public switch 41 (held)"])
		with self.assertRaisesRegex(RuntimeError, r"switch-levels-l5: frames or readings differ from the pinned seed at \['no switch closed'\]"):
			runtime_tool.check_pins(swapped)
		reworded = copy.deepcopy(pins)
		label = "coil step 20 public 20"
		reworded["coil-test-l5"][label] = [reworded["coil-test-l5"][label][0], "LEFT KICKER |  05 20  | "]
		with self.assertRaisesRegex(RuntimeError, "frames or readings differ"):
			runtime_tool.check_pins(reworded)
		dropped = copy.deepcopy(pins)
		del dropped["wheel-test-reactive-l5"]["home opto closes (synthetic flag)"]
		with self.assertRaisesRegex(RuntimeError, "cited frame labels differ"):
			runtime_tool.check_pins(dropped)

	def test_check_refuses_drift_and_generation_refuses_an_author_ready_record(self) -> None:
		products = curator.products(ROOT)
		drifted = dict(products)
		drifted[curator.DEFINITION] = products[curator.DEFINITION] + b" "
		with mock.patch.object(curator, "products", return_value=drifted):
			with self.assertRaisesRegex(RuntimeError, "missing or drifted"):
				curator.check(ROOT)
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			(root / curator.AUTHOR_READY).parent.mkdir(parents=True)
			(root / curator.AUTHOR_READY).write_bytes(b"{}\n")
			with mock.patch.object(curator, "products", return_value=products):
				with self.assertRaisesRegex(RuntimeError, "stale opposing-status record"):
					curator.check(root)
				with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite an author-ready Cyclone record"):
					curator.generate(root)
			self.assertEqual(b"{}\n", (root / curator.AUTHOR_READY).read_bytes())
			self.assertFalse((root / curator.DEFINITION).exists())

	def test_an_altered_excerpt_is_refused(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			shutil.copytree(EXCERPTS, root / curator.EXCERPTS)
			curator.verify_excerpts(root)
			target = root / curator.EXCERPTS / "service-bulletins.md"
			target.write_bytes(target.read_bytes().replace(b"`Coil B`", b"`Coil A`", 1))
			with self.assertRaisesRegex(RuntimeError, "excerpt missing or changed"):
				curator.verify_excerpts(root)


class CycloneRetainedEvidenceTests(unittest.TestCase):
	def _root(self, name: str) -> Path:
		value = os.environ.get(name)
		if not value:
			self.skipTest(f"{name} is not set")
		return Path(value).expanduser().resolve()

	def test_retained_manuals_ipdb_page_and_script_library(self) -> None:
		folder = self._root("PINMAME_MANUALS_ROOT") / curator.MANUAL_FOLDER
		if not folder.is_dir():
			self.skipTest("the retained Cyclone manuals are not under this manuals root")
		for filename, digest in (
			(curator.MANUAL_FILENAME, curator.MANUAL_SHA256), (curator.PARTS_FILENAME, curator.PARTS_SHA256),
			(curator.BULLETINS_FILENAME, curator.BULLETINS_SHA256), (curator.IPDB_PAGE, curator.IPDB_PAGE_SHA256),
		):
			self.assertEqual(digest, hashlib.sha256((folder / filename).read_bytes()).hexdigest(), filename)
		library = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "vpm-script-libs" / "s11.vbs"
		self.assertEqual(curator.VPM_S11_SHA256, hashlib.sha256(library.read_bytes()).hexdigest())

	def _review_root(self) -> Path:
		root = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not (root / runtime_tool.HARNESS_RELATIVE).is_dir():
			self.skipTest("the retained Cyclone harness runs are not under this review-artifacts root")
		return root

	def test_raw_runs_rebuild_the_compact_evidence_and_frame_pins(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		manifest_bytes, evidence, pins = runtime_tool.build(self._review_root())
		runtime_tool.check_pins(pins)
		self.assertEqual(curator.RUNTIME_MANIFEST_SHA256, hashlib.sha256(manifest_bytes).hexdigest())
		for game, path in RUNTIME_PATHS.items():
			self.assertEqual(canonical_bytes(evidence[game]), path.read_bytes(), game)

	def test_a_substituted_raw_frame_is_refused(self) -> None:
		root = self._review_root()
		original = runtime_tool.load_run

		def substituted(harness: Path, name: str, game: str) -> dict:
			run = original(harness, name, game)
			if name == "switch-levels-l5":
				snapshots = {item.get("label"): item for item in run["snapshots"]}
				snapshots["no switch closed"]["displays"] = copy.deepcopy(snapshots["hold public switch 41 (held)"]["displays"])
			return run

		with mock.patch.object(runtime_tool, "load_run", substituted):
			_, _, pins = runtime_tool.build(root)
		with self.assertRaisesRegex(RuntimeError, r"switch-levels-l5: frames or readings differ from the pinned seed at \['no switch closed'\]"):
			runtime_tool.check_pins(pins)

	def test_retained_table_extraction_and_geometry(self) -> None:
		vpx = self._root("PINMAME_VPX_SOURCES_ROOT")
		geometry = load(ROOT / curator.GEOMETRY)
		if not (vpx / geometry["table"]["extraction"]).is_dir():
			self.skipTest("the retained Cyclone table extraction is not under this VPX sources root")
		curator.verify_geometry(vpx, ROOT)

	def test_rom_name_tables_decode_to_the_excerpt(self) -> None:
		roms = self._root(curator.ROM_LIBRARY_VARIABLE)
		if not all((roms / f"{name}.zip").is_file() for name in data.DRIVER_IDS):
			self.skipTest("the Cyclone ROM sets are not all in this ROM library")
		curator.verify_rom_tables(roms, ROOT)


if __name__ == "__main__":
	unittest.main()
