from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import creature_runtime_evidence as evidence_tool  # noqa: E402
import curate_creature as curator  # noqa: E402
import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "creature-from-the-black-lagoon-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "creature-from-the-black-lagoon-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "creature-from-the-black-lagoon-1992.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "creature-from-the-black-lagoon-1992.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-fliptronic"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.creature-from-the-black-lagoon.1992"

MACHINE_ID = "bally.creature-from-the-black-lagoon.1992"
DRIVER_IDS = {"cftbl_l4", "cftbl_l4c", "cftbl_d4", "cftbl_l3", "cftbl_d3", "cftbl_l2", "cftbl_d2", "cftbl_p3"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 24, 31, 32, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# cftblGameData's inverted-switch mask (src/wpc/sims/wpc/full/cftbl.c), Coin, then columns 1-10, Cab., Cust.
CFTBL_INVERTED_SWITCH_MASK = (0x00, 0x10, 0x00, 0xC8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
SCRIPT_SHA256 = "110d85325e33cbaf465f5a60f3aeeb2069329c55719435e7b76380748ba70ea6"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = {"cftbl_l4": "a1eb5cb3d1f8a7b48592f9ed8b789c45d201260b37bf6bf7ac6db88d6cec1b09",
	"cftbl_p3": "8717d3e7f77871fd9fe032829a26d3d0aa253f7773c568f8c10090a8757ce2ba"}
# compact evidence file -> (scenario, retained run directory, ROM)
RUNTIME_FILES = {
	"creature-cftbl_l4-flasher-test.json": ("cftbl-flasher-test", "cftbl-flasher-test", "cftbl_l4"),
	"creature-cftbl_l4-switch-edges-fliptronic.json": ("cftbl-switch-edges-fliptronic", "cftbl-switch-edges-fliptronic", "cftbl_l4"),
	"creature-cftbl_l4-flipper-coil-test.json": ("cftbl-flipper-coil-test", "cftbl-flipper-coil-test", "cftbl_l4"),
	"creature-cftbl_l4-ramp-lights-test.json": ("cftbl-ramp-lights-test", "cftbl-ramp-lights-test", "cftbl_l4"),
	"creature-cftbl_l4-subway-awards.json": ("cftbl-subway-awards", "cftbl-subway-awards", "cftbl_l4"),
	"creature-cftbl_p3-flasher-test.json": ("cftbl-flasher-test", "p3-cftbl-flasher-test", "cftbl_p3"),
	"creature-cftbl_p3-switch-edges-fliptronic.json": ("cftbl-switch-edges-fliptronic", "p3-cftbl-switch-edges-fliptronic", "cftbl_p3"),
	"creature-cftbl_p3-flipper-coil-test.json": ("cftbl-flipper-coil-test", "p3-cftbl-flipper-coil-test", "cftbl_p3"),
	"creature-cftbl_p3-ramp-lights-test.json": ("cftbl-ramp-lights-test", "p3-cftbl-ramp-lights-test", "cftbl_p3"),
}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class CreatureTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		cls.coils = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.gi = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.gi"}

	def _placement(self, placement_id: str) -> dict:
		for item in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (item.get("spatial") or {}).get("placements", []):
				if placement["id"] == placement_id:
					return placement
		raise AssertionError(placement_id)

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, 588, 1992, "GrNWn-MQdqZ"), (machine["id"], machine["ipdb_id"], machine["year"], machine["opdb_id"]))
		self.assertEqual(("pinmame.wpc-fliptronic", "0x8"), (self.definition["controller"]["platform"], self.definition["controller"]["hardware_generation"]))
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual({"cftbl_p3"}, {key for key, value in compatibility.items() if value == "compatible"})
		self.assertEqual(DRIVER_IDS - {"cftbl_p3"}, {key for key, value in compatibility.items() if value == "identical"})
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["variant_coverage"])
		catalog = load(ROOT / "catalog/pinmame.json")
		self.assertEqual(DRIVER_IDS, {item["id"] for item in catalog["drivers"] if item.get("machine_id") == MACHINE_ID})
		record = next(item for item in catalog["machines"] if item["id"] == MACHINE_ID)
		self.assertEqual(88, record["completion_score"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(len(self.switches), sum(1 for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"})
		self.assertEqual(set(range(1, 51)), set(self.coils))
		self.assertEqual(MATRIX_ADDRESSES | set(range(91, 99)), set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gi))
		identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))
		self.assertEqual(UNUSED_MATRIX_ADDRESSES, curator.UNUSED_MATRIX_ADDRESSES)
		for address in MATRIX_ADDRESSES:
			expected = "unused" if address in UNUSED_MATRIX_ADDRESSES else "used"
			self.assertEqual(expected, self.switches[address]["availability"], address)

	def test_the_inverted_switch_mask_and_switch_polarity(self) -> None:
		inverted = {number for number in MATRIX_ADDRESSES if (CFTBL_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual({15, 34, 37, 38}, inverted)
		self.assertEqual(inverted, curator.PINMAME_INVERTED_SWITCHES)
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			switch = self.switches[address]
			self.assertIs(address in {34, 37}, switch["normally_closed"], address)
			self.assertIs(address in {34, 37}, switch["physical"]["switch_type"] == "opto", address)
		# 15 is an ordinary rollover whose public level PinMAME publishes inverted; the retained script starts it at 1.
		self.assertIn("publishes 1 while no ball is on the rollover", self.switches[15]["physical"]["notes"])
		self.assertIs(True, self.switches[15]["initial_active"])
		self.assertIs(True, self.switches[22]["initial_active"])
		self.assertIn("Public 1 means the ramp is down", self.switches[38]["physical"]["notes"])
		self.assertEqual("microswitch", self.switches[15]["physical"]["switch_type"])

	def test_the_fliptronic_block_and_flipper_windings(self) -> None:
		for address in (115, 117):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
		for address in (111, 112, 113, 114, 116, 118):
			self.assertEqual("used", self.switches[address]["availability"], address)
			self.assertIs(False, self.switches[address]["normally_closed"], address)
		self.assertEqual(["flipper.lower.right.button-second-opto"], self.switches[116]["roles"])
		self.assertEqual(["flipper.lower.left.button-second-opto"], self.switches[118]["roles"])
		edges = {item["label"]: item for item in load(RUNTIME_DIRECTORY / "creature-cftbl_l4-switch-edges-fliptronic.json")["runtime"]["observations"]["diagnostic_snapshots"]}
		self.assertEqual({31, 46}, set(edges["116 -> 1"]["active_solenoid_addresses"]))
		self.assertEqual({31, 48}, set(edges["118 -> 1"]["active_solenoid_addresses"]))
		self.assertEqual({116: {45, 46}, 118: {47, 48}}, evidence_tool.T1_COILS)
		for address in (45, 46, 47, 48):
			entry = curator.FLIPPER_COILS[address]
			self.assertEqual((evidence_tool.T12_NAMES[address], evidence_tool.T12_WIRES[address]), entry[9:], address)
			self.assertIn(f'names it "{entry[9]}" with the wires {entry[10]}', self.coils[address]["physical"]["notes"], address)
			self.assertEqual("coil", self.coils[address]["kind"], address)

	def test_rom_flasher_names_are_literal_in_the_device_notes(self) -> None:
		self.assertEqual(tuple(sorted(curator.T5_NAMES)), tuple(sorted(evidence_tool.T5_ORDER)))
		for address, (name, wire) in curator.T5_NAMES.items():
			self.assertEqual((evidence_tool.T5_NAMES[address], evidence_tool.T5_WIRES[address]), (name, wire), address)
			self.assertIn(f'prints "{name}" with the wires {wire} RED-WHT', self.coils[address]["physical"]["notes"], address)
		for address in (33, 34, 35, 36):
			coil = self.coils[address]
			self.assertEqual(("flasher", ["cabinet.insert-panel"], "cabinet_or_service"), (coil["kind"], coil["roles"], coil["spatial"]["reason"]), address)
			self.assertEqual(curator.INSERT_FLASHER_LINES[address][0], coil["wiring"]["control_connection"], address)

	def test_output_kinds_and_availability(self) -> None:
		kinds = {address: coil["kind"] for address, coil in self.coils.items()}
		self.assertEqual(("control_signal", "control_signal"), (kinds[20], kinds[24]))
		self.assertEqual(("coil", "coil"), (kinds[23], kinds[26]))
		self.assertEqual(("motor", "motor"), (kinds[21], kinds[27]))
		for address in (29, 30, 31):
			self.assertEqual(("virtual", "used"), (kinds[address], self.coils[address]["availability"]), address)
		for address in [32, *range(37, 45), 49, 50]:
			self.assertEqual(("virtual", "unused"), (kinds[address], self.coils[address]["availability"]), address)
		for address, (playfield, insert) in curator.FLASHER_BULBS.items():
			coil = self.coils[address]
			self.assertEqual(playfield + insert, coil["physical"]["quantity"], address)
			placements = coil["spatial"].get("placements") or []
			self.assertEqual(playfield, len(placements), address)
		self.assertEqual([], self.definition["relationships"])

	def test_chase_lamps_are_the_dark_string_and_stay_unplaced(self) -> None:
		for address in range(91, 99):
			lamp = self.lamps[address]
			self.assertNotIn("spatial", lamp, address)
			self.assertNotIn("quantity", lamp["physical"], address)
			self.assertEqual("conflicted", lamp["provenance"]["status"], address)
			self.assertIn("this address is 1 while string", lamp["physical"]["notes"], address)
		for address in (0, 3):
			self.assertNotIn("spatial", self.gi[address], address)
			self.assertEqual("conflicted", self.gi[address]["provenance"]["status"], address)
		(conflict,) = self.definition["conflicts"]
		self.assertEqual("conflict.chase-light-board-group-assignment", conflict["id"])
		self.assertIn("Resolution path:", conflict["description"])
		self.assertNotIn("status", conflict)
		chase = load(RUNTIME_DIRECTORY / "creature-cftbl_l4-ramp-lights-test.json")["runtime"]["observations"]
		self.assertEqual(list(range(91, 99)), chase["lamp_addresses_seen"])
		self.assertEqual([20, 24, 31], chase["solenoid_addresses_seen"])
		# PinMAME's chase lamps carry the decoder selection whatever the G.I.: stopping T.15 switches G.I. 0 and 3 off and the pair stays.
		self.assertIn("selected chase pair (93 and 97), so lamps 91-98 carry the decoder selection whatever the G.I.", chase["named_action_observations"][1]["label"])
		self.assertIn("whatever the G.I. does", self.lamps[91]["physical"]["notes"])
		self.assertNotIn("conducting AND", self.lamps[91]["physical"]["notes"])
		self.assertIn("lights three strings and darkens the", (EXCERPT_DIRECTORY / "chase-light-board.md").read_text(encoding="utf-8"))
		self.assertIn("Sol 20 to Chase Light II P.C. J2-2", (EXCERPT_DIRECTORY / "power-driver-board-connectors.md").read_text(encoding="utf-8"))

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		self.assertIn("mechanism.sequential-gi-chase", {mechanism["id"] for mechanism in self.definition["mechanisms"]})

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"]:
			cited.update(item["provenance"]["source_refs"])
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial") or {}
			cited.update(spatial.get("provenance", {}).get("source_refs", []))
			for placement in spatial.get("placements", []):
				cited.update(placement["provenance"]["source_refs"])
		for conflict in self.definition["conflicts"]:
			cited.update(conflict["source_refs"])
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertLessEqual(cited, set(sources))
		self.assertEqual(set(sources), cited | {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE})
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["id"])
					self.assertIn("WebP", excerpt["image_derivation"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")}, excerpts)
		self.assertTrue(sources[curator.VPX_SCRIPT_SOURCE]["known_working"])
		self.assertEqual(SCRIPT_SHA256, sources[curator.VPX_SCRIPT_SOURCE]["sha256"])

	def test_placements_are_in_range_unique_and_quantities_align(self) -> None:
		ids = []
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				for value in (placement["x"], placement["y"]):
					self.assertLessEqual(len(f"{value:.10f}".rstrip("0").split(".")[1]), 6, placement["id"])
			if item["kind"] == "lamp":
				self.assertEqual(item["physical"]["quantity"], len(spatial["placements"]), item["id"])
		self.assertEqual(len(ids), len(set(ids)))
		for address in (28, 37, 44):
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		self.assertEqual(0.0, self._placement("lamp.matrix-18.emitter")["y"])

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition), seed.get("limit", drawing_callouts.LIMIT))
		agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
		self.assertEqual(set(seed["checks"]), set(decisions["placements"]))
		self.assertEqual({"lamp.matrix-25.emitter", "lamp.matrix-26.emitter"}, set(seed["checks"]) - agreeing)
		self.assertEqual(88, len(seed["checks"]))
		for pid in seed["checks"]:
			placement = self._placement(pid)
			self.assertEqual("validated" if pid in agreeing else "observed", placement["provenance"]["status"], pid)
			self.assertIs(pid in agreeing, curator.CALLOUT_SOURCE in placement["provenance"]["source_refs"], pid)
		for pid, measurement in seed["measurements"].items():
			placement = self._placement(pid)
			self.assertEqual("observed", placement["provenance"]["status"], pid)
			self.assertEqual([curator.MANUAL_SOURCE, curator.CALLOUT_SOURCE], placement["provenance"]["source_refs"], pid)
			expected = tuple(min(max(value, 0.0), 1.0) for value in measurement["normalized"])
			self.assertEqual(expected, (placement["x"], placement["y"]), pid)
		for pid in seed["excluded_checks"]:
			expected = "observed" if pid in curator.UNCHECKED_TROUGH_PLACEMENTS else "validated"
			self.assertEqual(expected, self._placement(pid)["provenance"]["status"], pid)
		self.assertLessEqual(curator.UNCHECKED_TROUGH_PLACEMENTS, set(seed["excluded_checks"]))
		self.assertEqual(set(curator.callout_checks()) - set(seed["excluded_checks"]), set(seed["checks"]))
		# The drawing transposes 16 and 17; the ROM's awards follow the table.
		subways = load(RUNTIME_DIRECTORY / "creature-cftbl_l4-subway-awards.json")["runtime"]["observations"]
		self.assertEqual({"16": 21, "17": 53}, subways["switch_to_lamp"])
		self.assertLess(self._placement("switch.matrix-16.sensor")["x"], self._placement("switch.matrix-17.sensor")["x"])

	def test_gi_light_map_sources_are_only_candidates(self) -> None:
		for address in (1, 2, 4):
			spatial = self.gi[address]["spatial"]
			self.assertEqual("candidate", spatial["status"], address)
			self.assertTrue(all(p["provenance"]["status"] == "candidate" for p in spatial["placements"]), address)
			self.assertNotIn("quantity", self.gi[address]["physical"], address)
		report = load(SPATIAL_REPORT_PATH)
		self.assertEqual(sorted([f"lamp.chase-{address}" for address in range(91, 99)] + ["gi.string-0", "gi.string-3"]), report["without_placements"])

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check()
		self.assertEqual(DEFINITION_PATH.read_bytes(), curator.SEED_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertNotIn("\r", note)
		for phrase in ("conflict.chase-light-board-group-assignment", "three strings", "Resolution", "116", "CREATURE FL. 1"):
			self.assertIn(phrase, note)
		result = subprocess.run([sys.executable, str(ROOT / "tools/curate_creature.py")], capture_output=True, text=True, encoding="utf-8",
			env={**os.environ, "PYTHONPATH": f"{ROOT / 'src'}{os.pathsep}{ROOT / 'tools'}"})
		self.assertNotEqual(0, result.returncode)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		pins = load(evidence_tool.FRAME_READINGS_PATH)["runs"]
		self.assertEqual({directory for _, directory, _ in RUNTIME_FILES.values()}, set(pins))
		self.assertEqual(set(RUNTIME_FILES), {path.name for path in RUNTIME_DIRECTORY.glob("creature-*.json")})
		for filename, (scenario, directory, game) in RUNTIME_FILES.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = ROOT / "tools" / "harness-scenarios" / "wpc-fliptronic" / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertNotIn(b"\r", scenario_path.read_bytes(), filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256[game], document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual([game], document["driver_ids"], filename)
			self.assertEqual([MACHINE_ID], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertEqual(f"external:pinmame-review-artifacts/creature/harness/{directory}/run.json", raw["retained_from"], filename)
			self.assertEqual(len(load(scenario_path)["actions"]), raw["action_count"], filename)
			snapshots = document["runtime"]["observations"]["diagnostic_snapshots"]
			self.assertEqual(
				{label: (pin["pixel_sha256"], pin["reading"]) for label, pin in pins[directory].items()},
				{item["label"]: (item["pixel_sha256"], item["interpreted_text"]) for item in snapshots},
				filename,
			)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (_scenario, directory, game) in RUNTIME_FILES.items():
			path = root / "creature" / "harness" / directory
			check_manifest(path, game)
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(0, run["handle_mechanics"], filename)
			self.assertEqual(hashlib.sha256((path / "run.json").read_bytes()).hexdigest(), load(RUNTIME_DIRECTORY / filename)["runtime"]["raw_runs"][0]["sha256"], filename)
		seed = load(curator.CALLOUT_SEED_PATH)
		self.assertGreater(drawing_callouts.verify_retained(seed, ROOT, None, root), 0)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_vpx_extraction_matches_its_pinned_identity(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
		table = root / "bally" / "creature-from-the-black-lagoon-1992" / "vpw-1-0" / "source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		lines = script.read_bytes().decode("latin-1").splitlines()
		excerpt = (EXCERPT_DIRECTORY / "vpw-script-bindings.md").read_text(encoding="utf-8")
		self.assertIn(SCRIPT_SHA256, excerpt)
		quoted = [line for line in excerpt.split("```vbscript", 1)[1].split("```", 1)[0].splitlines() if line.strip()]
		self.assertGreater(len(quoted), 150)
		for line in quoted:
			number, body = int(line[:5]), line[7:]
			self.assertEqual(lines[number - 1].rstrip().replace("\t", "    "), body, number)


if __name__ == "__main__":
	unittest.main()
