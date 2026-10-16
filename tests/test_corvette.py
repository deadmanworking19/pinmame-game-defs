from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_corvette as curator  # noqa: E402
import corvette_runtime_evidence as evidence_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "corvette-1994.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "corvette-1994.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "corvette-1994.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "corvette-1994.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-security"
SCENARIO_DIRECTORY = ROOT / "tools" / "harness-scenarios" / "wpc-security"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.corvette.1994"

DRIVER_IDS = {"corv_21", "corv_px3", "corv_px4", "corv_px5", "corv_la1", "corv_lx1", "corv_dx1", "corv_la2", "corv_lx2", "corv_f61"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
# src/wpc/sims/wpc/prelim/corv.c corvGameData inverted switches: Coin, columns 1-8, 9, 10, Cab., Cust.
CORV_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x00, 0x7F, 0x07, 0x33, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00)
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "20e161d4e397650d436fc85ef01ce78bc144905444bd7e5fb4331f58edd5e211"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class CorvetteTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
		cls.switches = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		cls.coils = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.gi = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.gi"}

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.corvette.1994", 570, 1994, "50036", "GrjDz-MJKN6"), (machine["id"], machine["ipdb_id"], machine["year"], machine["model_number"], machine["opdb_id"]))
		self.assertEqual(("pinmame.wpc-security", "0x20"), (self.definition["controller"]["platform"], self.definition["controller"]["hardware_generation"]))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertEqual({"corv_px3", "corv_px4", "corv_px5"}, {k for k, v in drivers.items() if v["physical_compatibility"] == "unknown"})
		self.assertEqual("identical", drivers["corv_f61"]["physical_compatibility"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["variant_differences", "mechanism_behavior", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(len(self.switches), sum(1 for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"})
		self.assertEqual(set(range(1, 54)), set(self.coils))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gi))
		identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))
		self.assertEqual({53, 54, 73, 74, 85, 115}, {a for a, s in self.switches.items() if s["availability"] == "unused"})
		self.assertEqual({4, 25, 26, 27, 28}, {a for a, s in self.switches.items() if s["availability"] == "optional"})
		self.assertEqual({6, 14, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}, {a for a, c in self.coils.items() if c["availability"] == "unused"})

	def test_inverted_switch_mask_arithmetic_and_polarity(self) -> None:
		candidates = MATRIX_ADDRESSES | set(range(111, 119))
		inverted = {number for number in candidates if (CORV_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual(set(curator.MASKED_SWITCHES), inverted)
		self.assertEqual(inverted, set(evidence_tool.PINMAME_MASKED))
		self.assertEqual(curator.SHADED_SWITCHES - {112, 114, 116, 118}, inverted)
		for address in inverted:
			self.assertTrue(self.switches[address]["normally_closed"], address)
		for address in set(self.switches) - inverted - {24}:
			self.assertFalse(self.switches[address].get("normally_closed", False), address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[22]["initial_active"])

	def test_fliptronic_column_roles(self) -> None:
		self.assertEqual(["flipper.lower.right.button"], self.switches[112]["roles"])
		self.assertEqual(["flipper.lower.right.button"], self.switches[116]["roles"])
		self.assertEqual(["flipper.lower.left.button"], self.switches[114]["roles"])
		self.assertEqual(["flipper.upper.left.button"], self.switches[118]["roles"])
		self.assertIn("writes 112 and 116 together", self.switches[116]["physical"]["notes"])
		self.assertIn("writes 114 and 118 together", self.switches[118]["physical"]["notes"])
		for address in (111, 113, 117):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			self.assertIn("read back 0", self.switches[address]["physical"]["notes"], address)
		self.assertIn("J906-4 Not Used", self.switches[115]["physical"]["notes"])

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			if address == 24:
				continue
			self.assertIn(f'The ROM names it "{name}"', self.switches[address]["physical"]["notes"], address)
		self.assertEqual(curator.ROM_SWITCH_NAMES, {k: v for k, v in evidence_tool.EDGE_NAMES.items() if v != "NOT USED"})
		for address, (name, wires) in curator.ROM_SOLENOID_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {wires}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T4_NAMES}, evidence_tool.T4_NAMES)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T5_NAMES}, evidence_tool.T5_NAMES)
		self.assertEqual({number: (name, wires) for number, name, wires, _ in evidence_tool.T12_ORDER}, {
			{45: 1, 46: 2, 47: 3, 48: 4, 35: 7, 36: 8}[a]: v for a, v in curator.ROM_SOLENOID_NAMES.items() if a in curator.T12_ADDRESSES
		})
		self.assertEqual(curator.SWITCH_FIRES, {address: fired for address, (fired, _) in evidence_tool.SWITCH_FIRES.items()})
		self.assertEqual(curator.ROM_LAMP_NAMES, evidence_tool.LAMP_NAMES)
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertIn(f'names it "{name}"', self.lamps[address]["physical"]["notes"], address)

	def test_outputs_kinds_and_the_engine_and_race_controls(self) -> None:
		self.assertEqual(set(range(20, 29)), {a for a, c in self.coils.items() if c["kind"] == "flasher"})
		self.assertEqual({17, 51, 52, 53}, {a for a, c in self.coils.items() if c["kind"] == "control_signal"})
		self.assertEqual({18, 19}, {a for a, c in self.coils.items() if c["kind"] == "motor"})
		for address in (22, 23, 24, 25, 26, 27):
			self.assertEqual(2, self.coils[address]["physical"]["quantity"], address)
		self.assertNotIn("quantity", self.coils[28]["physical"])
		self.assertIn("engine power enable", self.coils[51]["physical"]["notes"])
		self.assertIn("EXTBOARD", json.dumps(self.definition["sources"]))
		self.assertEqual(["flipper.upper.left"], self.coils[35]["roles"])
		self.assertEqual(("device.diverter-power", "device.diverter-hold"), (self.coils[33]["id"], self.coils[34]["id"]))
		for address in (7, 20):
			self.assertEqual("not_applicable", self.coils[address]["spatial"]["status"], address)
		self.assertEqual({87: ["cabinet.buy-in"], 88: ["cabinet.start-button-lamp"]}, {a: self.lamps[a]["roles"] for a in (87, 88)})
		self.assertEqual("not_applicable", self.gi[4]["spatial"]["status"])

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		engine = mechanisms["mechanism.zr1-engine"]
		self.assertEqual([self.coils[a]["id"] for a in (51, 52, 53)], engine["actuators"])
		self.assertEqual(["switch.matrix-71", "switch.matrix-72"], engine["sensors"])
		self.assertIn("GetMech(2)", engine["behavior"])
		self.assertIn("four coils", engine["behavior"])
		self.assertIn("ENGINE COILS (4)", (EXCERPT_DIRECTORY / "unit-disassembly-engine.md").read_text(encoding="utf-8"))
		race = mechanisms["mechanism.race-track"]
		self.assertEqual([self.coils[a]["id"] for a in (17, 18, 19)], race["actuators"])
		self.assertEqual([f"switch.matrix-{a}" for a in (51, 55, 52, 56)], race["sensors"])
		self.assertIn("No retained source says", mechanisms["mechanism.zr1-lock"]["behavior"])
		self.assertEqual([], self.definition["relationships"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
			spatial = item.get("spatial") or {}
			cited.update(spatial.get("provenance", {}).get("source_refs", []))
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertLessEqual(cited, set(sources))
		self.assertEqual(set(sources), cited | {curator.CATALOG_SOURCE})
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")}, excerpts)
		for path in EXCERPT_DIRECTORY.glob("*.md"):
			self.assertIsNone(re.search(r"[A-Z]:[\\/]", path.read_text(encoding="utf-8")), path.name)

	def test_no_artifact_names_another_machines_driver_or_record(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		# Catalog driver ids that are ordinary words in this record's prose.
		ordinary_words = {"corvette", "engine", "pitstop", "race", "racetrack", "real"}
		forbidden = ({driver["id"] for driver in catalog["drivers"]} - DRIVER_IDS - ordinary_words) | (
			{machine["id"] for machine in catalog["machines"]} - {"bally.corvette.1994"}
		)
		self.assertIn("ts_lx5", forbidden)
		paths = [
			DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md"),
			ROOT / "tools" / "curate_corvette.py", ROOT / "tools" / "corvette_runtime_evidence.py",
			*sorted((ROOT / "tools" / "seeds" / "bally").glob("corvette-1994*")),
			*[RUNTIME_DIRECTORY / filename for filename in evidence_tool.RUNS],
			*sorted(SCENARIO_DIRECTORY.glob("cv-*.json")),
		]
		for path in paths:
			text = path.read_text(encoding="utf-8")
			found = sorted(item for item in forbidden if re.search(rf"(?<![\w.-]){re.escape(item)}(?![\w-])", text))
			self.assertEqual([], found, path.name)

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("engine", "race track", "GetMech(2)", "shifter", "spatial_placement", "mechanism_behavior", "112 and 116"):
			self.assertIn(phrase.casefold(), note.casefold(), phrase)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (_directory, scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = SCENARIO_DIRECTORY / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertNotIn(b"\r", scenario_path.read_bytes(), filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["bally.corvette.1994"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertIn(f"--handle-mechanics {mechanics} ", document["runtime"]["command_template"], filename)
			self.assertEqual(len(load(scenario_path)["actions"]), raw["action_count"], filename)
		sources = {source["id"]: source for source in self.definition["sources"]}
		for source_id, name, _ in curator.RUNTIME_SOURCES:
			self.assertTrue((ROOT / sources[source_id]["uri"].removeprefix("internal:")).is_file(), source_id)
		edges = load(RUNTIME_DIRECTORY / "corvette-corv_21-switch-edges.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		for address in curator.MASKED_SWITCHES:
			self.assertTrue(texts[f"{address} -> 1"].startswith(curator.ROM_SWITCH_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
		self.assertTrue(texts["24 -> 0"].startswith("ALWAYS CLOSED"))
		for address in curator.UNUSED_MATRIX_ADDRESSES:
			self.assertTrue(texts[f"{address} -> 1"].startswith("NOT USED"), address)
		self.assertTrue(texts["115 -> 1"].startswith("SWITCH EDGES"))
		solenoids = load(RUNTIME_DIRECTORY / "corvette-corv_21-solenoid-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([[a] for a in evidence_tool.T4_ORDER], [item["transitioned_solenoid_addresses"] for item in solenoids])
		lamps = load(RUNTIME_DIRECTORY / "corvette-corv_21-single-lamps.json")["runtime"]["observations"]["diagnostic_snapshots"]
		self.assertEqual(65, len(lamps))

	def test_every_reading_is_pinned_to_its_frame(self) -> None:
		seed = load(evidence_tool.FRAME_SEED_PATH)
		self.assertEqual(set(evidence_tool.RUNS), set(seed))
		for filename in evidence_tool.RUNS:
			snapshots = load(RUNTIME_DIRECTORY / filename)["runtime"]["observations"]["diagnostic_snapshots"]
			self.assertEqual(seed[filename], {item["label"]: {"pixel_sha256": item["pixel_sha256"], "reading": item["interpreted_text"]} for item in snapshots}, filename)
		with self.assertRaises(ValueError):
			observations = {"diagnostic_snapshots": [dict(item) for item in load(RUNTIME_DIRECTORY / "corvette-corv_21-engine-test.json")["runtime"]["observations"]["diagnostic_snapshots"]]}
			observations["diagnostic_snapshots"][1]["pixel_sha256"] = "0" * 64
			evidence_tool._check_pinned_frames("corvette-corv_21-engine-test.json", observations)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (directory, _scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			path = root / evidence_tool.HARNESS_DIRECTORY / directory
			check_manifest(path, "corv_21")
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(mechanics, run["handle_mechanics"], filename)
			self.assertEqual([{"state": 0, "switch": 22}], run["initial_switches"], filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_builders_refuse_transitions_in_the_wrong_direction(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY

		def mutated(directory: str, label: str, channel: str, number: int, states: list[int]) -> dict:
			run = json.loads((root / directory / "run.json").read_bytes())
			step = next(item for item in run["steps"] if item["label"] == label)
			for item in step["transitions"][channel]:
				if item["number"] == number:
					item["states"] = states
			return run

		with self.assertRaises(ValueError):
			evidence_tool.build_lamps(mutated("cv-single-lamps", "T.8 Up 1", "lamps", 12, [0]))
		with self.assertRaises(ValueError):
			evidence_tool.build_engine_failed(mutated("cv-engine-test-no-mech", "SELF TEST 6", "solenoids", 51, [1]))
		with self.assertRaises(ValueError):
			evidence_tool.build_zr1_adjust(mutated("cv-zr1-adjust", "Enter (start T.18)", "solenoids", 51, [0]))
		extra = mutated("cv-single-lamps", "T.8 Up 1", "lamps", 12, [1, 0, 1])
		next(item for item in extra["steps"] if item["label"] == "T.8 Up 1")["transitions"]["lamps"].append({"number": 88, "states": [1]})
		with self.assertRaises(ValueError):
			evidence_tool.build_lamps(extra)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_readings_are_checked_against_the_retained_frame_files(self) -> None:
		directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / "cv-zr1-adjust"
		run = evidence_tool._load_run(directory, "cv-zr1-adjust", 7)
		snapshot = next(item for item in run["snapshots"] if item["label"] == "Enter (start T.18)")
		display = next(item for item in snapshot["displays"] if item["index"] == 0)
		self.assertTrue(evidence_tool._frame_matches(run, display))
		display["pixel_sha256"] = "0" * 64
		self.assertFalse(evidence_tool._frame_matches(run, display))
		display["artifact"] = "dmd/missing-frame.pgm"
		with self.assertRaises(OSError):
			evidence_tool._frame_matches(run, display)


if __name__ == "__main__":
	unittest.main()
