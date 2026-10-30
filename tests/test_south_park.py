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

import curate_south_park as curator  # noqa: E402
import south_park_runtime_evidence as evidence_tool  # noqa: E402
import south_park_spatial_seed as seed_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "sega" / "south-park-1999.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "sega" / "south-park-1999.json"
SEED_PATH = ROOT / "tools" / "seeds" / "sega" / "south-park-1999-spatial.json"
EVIDENCE_103_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "south-park-sprk-103-stacking-opto-and-gameplay.json"
EVIDENCE_096_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "south-park-sprk-096-gameplay.json"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "sega.south-park.1999"

DRIVER_IDS = {"sprk_090", "sprk_096", "sprk_103"}
# The Switch Matrix Grid's NOT USED cells (excerpt switch-matrix.md), and the Lamp Matrix Grid's (lamp-matrix.md).
NOT_USED_SWITCHES = {9, 27, 28, 29, 30, 31, 32, 33, 39, 40, 41, 52, 53, 63, 64}
NOT_USED_LAMPS = {31, 32, 47, 49} | set(range(65, 81))
# The UK-only cabinet buttons and the coin-door positions beyond the three stock slots.
OPTIONAL_SWITCHES = {1, 2, 3, 7, 8}
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def steps(path: Path, run: str) -> dict[str, dict]:
	prefix = f"{run} "
	return {item["label"].split(": ", 1)[1].split(";")[0]: item for item in load(path)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith(prefix)}


class SouthParkTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("sega.south-park.1999", 4444, "G4qbD-MQpxv", 1999, "71"), (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["year"], machine["model_number"]))
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual({"sprk_103": "identical", "sprk_096": "identical", "sprk_090": "compatible"}, compatibility)
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])
		catalog = load(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == "sega.south-park.1999"}
		self.assertEqual(DRIVER_IDS, claimed)

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

	def test_unused_and_optional_cells_follow_the_grids(self) -> None:
		unused = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "unused"}
		self.assertEqual(NOT_USED_SWITCHES, unused)
		optional = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "optional"}
		self.assertEqual(OPTIONAL_SWITCHES, optional)
		self.assertEqual(NOT_USED_LAMPS, {address for address in range(1, 81) if self.device("output.lamp", address)["availability"] == "unused"})
		self.assertEqual({8, 21, 22, 23, 24}, {address for address in range(1, 51) if self.device("output.solenoid", address)["availability"] == "optional"})
		self.assertEqual("unused", self.device("input.switch", 88)["availability"])

	def test_polarity_follows_the_read_path_and_the_wiring_diagrams(self) -> None:
		for address in range(1, 65):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertTrue(self.device("input.switch", 81)["normally_closed"])
		self.assertTrue(self.device("input.switch", 83)["normally_closed"])
		for address in (82, 84, -3, -2, -1, 0):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertEqual({10, 11, 12, 13, 14}, {address for address in range(1, 65) if self.device("input.switch", address).get("initial_active")})
		self.assertTrue(self.device("input.switch", -3)["initial_active"])
		for address in (14, 15, 42):
			self.assertEqual("opto", self.device("input.switch", address)["physical"]["switch_type"], address)
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
		# The coil chart's FLASH rows: Q7 and Q18 among the high-current outputs, and F1-F8 at Q25-Q32.
		self.assertEqual({7, 18, 25, 26, 27, 28, 29, 30, 31, 32}, flashers)

	def test_only_the_production_set_publishes_the_game_on_state(self) -> None:
		production = steps(EVIDENCE_103_PATH, "sprk-103-gameplay")
		prototype = steps(EVIDENCE_096_PATH, "sprk-096-gameplay")
		self.assertIn(15, production["the served ball rests on the shooter lane switch 16"]["active_solenoid_addresses"])
		self.assertNotIn(15, prototype["the served ball rests on the shooter lane switch 16"]["active_solenoid_addresses"])
		self.assertNotIn(15, load(EVIDENCE_096_PATH)["runtime"]["observations"]["solenoid_addresses_seen"])

	def test_wiring_comes_from_the_printed_tables(self) -> None:
		trough = self.device("output.solenoid", 1)["wiring"]
		self.assertEqual(("Q1", "BRN-BLK", "J8-P1", "YEL-VIO", "J10-P4/5", 50), (trough["driver_transistor"], trough["control_wire"], trough["control_connection"], trough["power_wire"], trough["power_connection"], trough["nominal_voltage_v"]))
		self.assertEqual("BRN-YEL", self.device("output.solenoid", 4)["wiring"]["control_wire"])
		self.assertIn("BRY-YEL", self.device("output.solenoid", 4)["physical"]["notes"])
		self.assertEqual("J7-P10", self.device("output.solenoid", 24)["wiring"]["control_connection"])
		switch = self.device("input.switch", 54)["wiring"]
		self.assertEqual(("GRN-VIO", "CN5-P8", "WHT-BLU", "CN7-P3"), (switch["drive_wire"], switch["drive_connection"], switch["return_wire"], switch["return_connection"]))
		for address, wire, pin in ((1, "WHT-BRN", "CN7-P9"), (8, "WHT-GRY", "CN7-P1")):
			wiring = self.device("input.switch", address)["wiring"]
			self.assertEqual((wire, pin), (wiring["return_wire"], wiring["return_connection"]), address)
		lamp = self.device("output.lamp", 80)["wiring"]
		self.assertEqual(("YEL-GRY", "J13-P1", "RED", "J12-P11"), (lamp["drive_wire"], lamp["drive_connection"], lamp["return_wire"], lamp["return_connection"]))

	def test_mechanisms_reference_declared_devices(self) -> None:
		ids = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= ids, mechanism["id"])
		names = {mechanism["id"] for mechanism in self.definition["mechanisms"]}
		self.assertTrue({"mechanism.trough", "mechanism.top-vuk", "mechanism.super-vuk", "mechanism.toilet", "mechanism.kenny", "mechanism.uk-sav-a-ball"} <= names)

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		paths = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], sha256(ROOT / excerpt["path"]), excerpt["id"])
				paths.add(Path(excerpt["path"]).name)
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], sha256(ROOT / excerpt["image"]), excerpt["id"])
					paths.add(Path(excerpt["image"]).name)
		self.assertEqual({path.name for path in EXCERPT_DIRECTORY.iterdir()}, paths)

	def test_committed_text_names_no_other_machine(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != "sega.south-park.1999" and len(driver["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), (ROOT / "knowledge/sega/south-park-1999.md").read_text(encoding="utf-8")]
		words = set(re.findall(r"[a-z0-9_]{5,}", "\n".join(texts)))
		# Lamp 7 is the playfield's own "Spooky Vision" insert, not a reference to the driver of that name.
		self.assertEqual(set(), words & foreign - {"spooky"})

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
		missing = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"] if item.get("availability") in {"used", "optional"} and "spatial" not in item}
		self.assertEqual(set(), missing)
		self.assertEqual(32, len(self.device("output.gi", 0)["spatial"]["placements"]))
		self.assertEqual(33, self.device("output.gi", 0)["physical"]["quantity"])

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_scenarios_name_only_their_game_and_evidence_pins_its_runs(self) -> None:
		manifests = {}
		for path, game, rom in ((EVIDENCE_103_PATH, "sprk_103", curator.ROM_ARCHIVE_SHA256), (EVIDENCE_096_PATH, "sprk_096", curator.ROM_096_ARCHIVE_SHA256)):
			document = load(path)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
			self.assertEqual(curator.RUNTIME_LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
			self.assertEqual(rom, document["runtime"]["rom_archive_sha256"])
			self.assertEqual(curator.PINMAME_REVISION, document["source"]["revision"])
			relative = path.relative_to(ROOT).as_posix()
			self.assertEqual((game, rom), evidence_tool.DOCUMENTS[relative][:2])
			self.assertEqual(set(evidence_tool.DOCUMENTS[relative][2]), {run["name"] for run in document["runtime"]["raw_runs"]})
			manifests.update(evidence_tool.DOCUMENTS[relative][2])
			for run in document["runtime"]["raw_runs"]:
				scenario = ROOT / run["scenario_path"]
				self.assertEqual(run["scenario_sha256"], sha256(scenario), run["name"])
				self.assertEqual(game, load(scenario)["game"])
				self.assertNotIn(b"\r", scenario.read_bytes(), run["name"])
		self.assertEqual(manifests, curator.RUN_MANIFESTS)

	def test_gameplay_steps_support_the_switch_to_coil_claims(self) -> None:
		for path, run in ((EVIDENCE_103_PATH, "sprk-103-gameplay"), (EVIDENCE_096_PATH, "sprk-096-gameplay")):
			observed = steps(path, run)
			expected = {
				"left turbo bumper (public 49) closed once": 9, "right turbo bumper (public 50) closed once": 10, "bottom turbo bumper (public 51) closed once": 11,
				"left slingshot (public 59) closed once": 12, "right slingshot (public 62) closed once": 17, "Start button (public 54)": 1,
				"a ball enters the super VUK (public 45) and stays": 3, "under-trough super VUK (public 48) closed once": 3,
				"under-trough (Kenny) (public 44) closed once": 3, "coin 1 on the center coin slot (public 5)": 24,
			}
			for label, coil in expected.items():
				self.assertIn(coil, observed[label]["active_solenoid_addresses"], (run, label))
			self.assertTrue({14, 19, 20, 30} <= set(observed["Kenny opto (public 42) closed once"]["active_solenoid_addresses"]), run)
			self.assertEqual([], observed["under-trough (toilet) (public 43) closed once"]["active_solenoid_addresses"], run)
			self.assertTrue({47, 48} <= set(observed["left flipper button (public 84) held 1.5 s"]["active_solenoid_addresses"]), run)
			self.assertTrue({45, 46} <= set(observed["right flipper button (public 82) held 1.5 s"]["active_solenoid_addresses"]), run)
			self.assertTrue({1, 13} <= set(observed["the ball drains: trough position 10 fills again"]["active_solenoid_addresses"]), run)
		self.assertIn(4, steps(EVIDENCE_103_PATH, "sprk-103-gameplay")["the top VUK (public 46) empties"]["active_solenoid_addresses"])
		for path in (EVIDENCE_103_PATH, EVIDENCE_096_PATH):
			seen = set(load(path)["runtime"]["observations"]["solenoid_addresses_seen"])
			self.assertFalse(seen & {2, 5, 6, 8, 21, 22, 23}, path.name)
			self.assertFalse(set(load(path)["runtime"]["observations"]["lamp_addresses_seen"]) - set(range(1, 65)), path.name)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		for relative, (game, rom, runs) in evidence_tool.DOCUMENTS.items():
			self.assertEqual(canonical_bytes(evidence_tool.build(root, game, rom, runs)), (ROOT / relative).read_bytes(), relative)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_stacking_opto_run_draws_no_coil_in_attract_mode(self) -> None:
		run = load(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / "sprk-stacking-opto" / "run.json")
		edges = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event["number"] == 15 and not event.get("initial")]
		self.assertEqual(3, len(edges))
		fired = {event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] >= edges[0]}
		self.assertEqual(set(), fired - {13})

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_extraction_script_and_seed_match(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		curator.verify_extraction_manifest(root)
		base = root / "sega/south-park-1999/v1-3"
		table = base / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, sha256(table))
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, sha256(script))
		built = seed_tool.canonical(seed_tool.build(root / curator.EXTRACTION_RELATIVE_PATH, table))
		self.assertEqual(built.encode("utf-8"), SEED_PATH.read_bytes())
		code = "\n".join(line for line in script.read_text(encoding="latin-1").splitlines() if not line.strip().startswith("'"))
		self.assertIn('Const cGameName = "sprk_103"', code)
		self.assertIn("Set bsTrough = New cvpmBallStack", code)
		self.assertIn(".InitSw 0, 14, 13, 12, 11, 10, 0, 0", code)
		# The avoidance claims behind the stacking-opto and EOS notes: no live write to 15, 81 or 83.
		for address in (15, 81, 83):
			self.assertIsNone(re.search(rf"(Switch\(\s*{address}\s*\)|PulseSw\s*\(?\s*{address}\b)", code, re.IGNORECASE), address)

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_manual_matches_its_pin(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / curator.MACHINE_ID / "ipdb"
		self.assertEqual(curator.MANUAL_SHA256, sha256(root / curator.MANUAL_NAME))


if __name__ == "__main__":
	unittest.main()
