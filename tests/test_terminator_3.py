from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import sys
import unittest
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_terminator_3 as curator  # noqa: E402
import terminator_3_runtime_evidence as evidence_tool  # noqa: E402
import terminator_3_spatial_seed as seed_tool  # noqa: E402

MACHINE_ID = "stern.terminator-3-rise-of-the-machines.2003"
DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "terminator-3-rise-of-the-machines-2003.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "terminator-3-rise-of-the-machines-2003.json"
STUB_PATH = ROOT / "machines" / "stubs" / "stern" / "terminator-3-rise-of-the-machines-2003.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "terminator-3-rise-of-the-machines-2003.md"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "terminator-3-rise-of-the-machines-2003-spatial.json"
FRAME_SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "terminator-3-rise-of-the-machines-2003-frame-readings.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "terminator-3-term3-service-tests-and-gameplay.json"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / MACHINE_ID

DRIVER_IDS = {"term3", "term3_2", "term3_3", "term3f", "term3f_2", "term3f_3", "term3g", "term3g_3", "term3i", "term3i_2", "term3i_3", "term3l", "term3l_2", "term3l_3"}
# The Switch Matrix Grid's NOT USED cells (excerpt switch-matrix.md); the ROM's Switch Test prints NONE for 3, which the
# grid labels but the ROM does not read.
NOT_USED_SWITCHES = {9, 26, 27, 47, 48, 63, 64}
# The UK-only cabinet buttons, the coin-door slots beyond the three stock ones and the tournament kit's start button.
OPTIONAL_SWITCHES = {1, 2, 7, 8, 53}
# The coil chart's NOT USED rows, the PinMAME-only addresses nothing publishes and the UK-only auxiliary board outputs.
UNUSED_SOLENOIDS = {6, 7, 16, 19, 25, *range(36, 45), 49, 50}
OPTIONAL_SOLENOIDS = {24, 33, 34, 35}
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_SHA256 = "64503f35d34ec28a6bb69eaf2b77e6e870dfff988c49364b07c2c6f0ed5a76b6"
LAMP_TEST_RUN = "term3-single-lamp-test"
# Lamps the retained script binds to a bulb-mode Light: Kombilicht copies of 1-52, 55-62, 72 and 80, and l64/l71.
BOUND_LAMPS = set(range(1, 53)) | set(range(55, 63)) | {64, 71, 72, 80}
# Playfield lamps with no placement: every bound lamp, and 73-78, which the script copies onto no Light.
UNPLACED_LAMPS = BOUND_LAMPS | set(range(73, 79))


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def steps(run: str) -> dict[str, dict]:
	prefix = f"{run} step "
	return {item["label"].split(": ", 1)[1].split(";")[0]: item for item in load(EVIDENCE_PATH)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith(prefix)}


def raw_run(name: str) -> dict:
	return load(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / name / "run.json")


def events(run: dict, kind: str, number: int) -> list[tuple[float, int]]:
	return [(event["time_s"], event["state"]) for event in run["events"] if event["event"] == kind and event["number"] == number and not event.get("initial")]


def rises(run: dict, kind: str, number: int) -> list[float]:
	return [time for time, state in events(run, kind, number) if state]


def falls(run: dict, kind: str, number: int) -> list[float]:
	return [time for time, state in events(run, kind, number) if not state]


class TerminatorThreeTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, 4787, "GR91N-MLOyE", 2003, "Stern"), (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["year"], machine["manufacturer"]))
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual(dict.fromkeys(DRIVER_IDS, "identical"), compatibility)
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["output_semantics", "spatial_placement"], coverage["missing"])
		self.assertEqual(("candidate", "observed"), (coverage["dimensions"]["semantic_naming"], coverage["dimensions"]["spatial_placement"]))
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertFalse(STUB_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual([], self.definition["relationships"])
		catalog = load(ROOT / "catalog/pinmame.json")
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID})
		record = next(item for item in catalog["machines"] if item["id"] == MACHINE_ID)
		self.assertEqual(("partial", 88, ["term3"]), (record["coverage_status"], record["completion_score"], record["root_drivers"]))
		self.assertEqual(sha256(DEFINITION_PATH), record["definition_sha256"])

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		def addresses(group: str) -> set[int]:
			return {item["binding"]["device"] for item in self.definition["inputs"] + self.definition["outputs"] if item["binding"]["group"] == group}
		self.assertEqual(set(range(-3, 65)) | set(range(81, 89)), addresses("pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), addresses("pinmame.input.dip"))
		self.assertEqual(set(range(1, 51)), addresses("pinmame.output.solenoid"))
		self.assertEqual(set(range(1, 81)), addresses("pinmame.output.lamp"))
		self.assertEqual({0}, addresses("pinmame.output.gi"))
		keys = [(item["binding"]["group"], item["binding"]["device"]) for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(keys), len(set(keys)))
		identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_unused_optional_and_unresolved_cells_follow_the_grids(self) -> None:
		def availability(group: str, addresses: range | set[int], state: str) -> set[int]:
			return {address for address in addresses if self.device(group, address)["availability"] == state}
		self.assertEqual(NOT_USED_SWITCHES | {3}, availability("input.switch", range(1, 65), "unused"))
		self.assertEqual(OPTIONAL_SWITCHES, availability("input.switch", range(1, 65), "optional"))
		self.assertEqual({85, 86, 87, 88}, availability("input.switch", range(81, 89), "unused"))
		self.assertEqual(UNUSED_SOLENOIDS, availability("output.solenoid", range(1, 51), "unused"))
		self.assertEqual(OPTIONAL_SOLENOIDS, availability("output.solenoid", range(1, 51), "optional"))
		self.assertEqual({70}, availability("output.lamp", range(1, 81), "unused"))
		self.assertEqual({54, 79}, availability("output.lamp", range(1, 81), "optional"))
		self.assertEqual({63}, availability("output.lamp", range(1, 81), "unknown"))
		lamp = self.device("output.lamp", 63)
		self.assertEqual("candidate", lamp["provenance"]["status"])
		self.assertNotIn("spatial", lamp)
		self.assertIn("Resolution path:", lamp["physical"]["notes"])
		self.assertEqual({1, 2, 3, 4, 5}, availability("input.dip", range(1, 9), "used"))

	def test_polarity_follows_the_read_path(self) -> None:
		for address in range(1, 65):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertTrue(self.device("input.switch", 81)["normally_closed"])
		self.assertTrue(self.device("input.switch", 83)["normally_closed"])
		for address in (82, 84, 85, 86, 87, 88, -3, -2, -1, 0):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertEqual({11, 12, 13, 14}, {address for address in range(1, 65) if self.device("input.switch", address).get("initial_active")})
		self.assertTrue(self.device("input.switch", -3)["initial_active"])
		self.assertEqual({14, 15, 33}, {address for address in range(1, 65) if self.device("input.switch", address)["physical"].get("switch_type") == "opto"})
		self.assertEqual("unknown", self.device("input.switch", 52)["physical"]["switch_type"])
		self.assertIn(curator.RUNTIME_SOURCE, self.device("input.switch", 15)["provenance"]["source_refs"])

	def test_flipper_remap_and_published_states(self) -> None:
		left = self.device("output.solenoid", 48)
		right = self.device("output.solenoid", 46)
		self.assertEqual(("device.q15-left-flipper", "coil"), (left["id"], left["kind"]))
		self.assertEqual(("device.q16-right-flipper", "coil"), (right["id"], right["kind"]))
		for address in (15, 45, 47):
			self.assertEqual(("virtual", "used"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		for address in (16, *range(36, 45), 49, 50):
			self.assertEqual(("virtual", "unused"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		# The coil chart's FLASH rows Q26-Q32; Q4 switches the backbox G.I. and Q20 is the backbox motor relay.
		self.assertEqual(set(range(26, 33)), {address for address in range(1, 51) if self.device("output.solenoid", address)["kind"] == "flasher"})
		self.assertEqual(("gi", "relay"), (self.device("output.solenoid", 4)["kind"], self.device("output.solenoid", 20)["kind"]))
		for address in (33, 34, 35):
			auxiliary = self.device("output.solenoid", address)
			self.assertEqual(("coil", "Whitestar Solenoid Expander Auxiliary board 520-5068-01"), (auxiliary["kind"], auxiliary["wiring"]["board"]), address)

	def test_wiring_comes_from_the_printed_tables(self) -> None:
		trough = self.device("output.solenoid", 1)["wiring"]
		self.assertEqual(("Q1", "BRN-BLK", "J8-P1", "YEL-VIO", "J10-P4/5", 50), (trough["driver_transistor"], trough["control_wire"], trough["control_connection"], trough["power_wire"], trough["power_connection"], trough["nominal_voltage_v"]))
		backbox = self.device("output.solenoid", 4)["wiring"]
		self.assertEqual(("GRY / GRY-GRN", "J17-P2/3", 19, "ac"), (backbox["power_wire"], backbox["power_connection"], backbox["nominal_voltage_v"], backbox["voltage_type"]))
		# A NOT USED row prints its transistor and control wire but no power.
		self.assertEqual({"board", "control_connection", "control_wire", "driver_transistor"}, set(self.device("output.solenoid", 6)["wiring"]))
		# The chart prints ORG power for Q30; the ROM's coil test prints BRN, which the note keeps.
		self.assertEqual("ORG", self.device("output.solenoid", 30)["wiring"]["power_wire"])
		self.assertIn('"#30 FLASH: BACK PANEL X4 / BRN BLK-BLU"', self.device("output.solenoid", 30)["physical"]["notes"])
		self.assertEqual("GRY-YEL~3A Fuse~RED-YEL", self.device("output.solenoid", 48)["wiring"]["power_wire"])
		for address, drive, return_wire in ((54, ("GRN-VIO", "CN5-P8"), ("WHT-BLU", "CN7-P3")), (55, ("GRN-VIO", "CN5-P8"), ("WHT-VIO", "CN7-P2")), (1, ("GRN-BRN", "CN5-P1"), ("WHT-BRN", "CN7-P9")), (8, ("GRN-BRN", "CN5-P1"), ("WHT-GRY", "CN7-P1"))):
			wiring = self.device("input.switch", address)["wiring"]
			self.assertEqual((drive, return_wire), ((wiring["drive_wire"], wiring["drive_connection"]), (wiring["return_wire"], wiring["return_connection"])), address)
		flipper = self.device("input.switch", 84)["wiring"]
		self.assertEqual(("GRY-BRN", "CN6-P2"), (flipper["drive_wire"], flipper["drive_connection"]))
		for address, drive, return_wire in ((79, ("YEL-VIO", "J13-P3"), ("RED", "J12-P11")), (63, ("YEL-VIO", "J13-P3"), ("RED-GRY", "J12-P9")), (1, ("YEL-BRN", "J13-P9"), ("RED-BRN", "J12-P1"))):
			wiring = self.device("output.lamp", address)["wiring"]
			self.assertEqual((drive, return_wire), ((wiring["drive_wire"], wiring["drive_connection"]), (wiring["return_wire"], wiring["return_connection"])), address)

	def test_mechanisms_reference_declared_devices(self) -> None:
		ids = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= ids, mechanism["id"])
		by_id = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		self.assertEqual({
			"mechanism.trough", "mechanism.auto-launch", "mechanism.kickback", "mechanism.vuk", "mechanism.tx-cannon", "mechanism.drop-target",
			"mechanism.up-posts", "mechanism.back-panel-ball-stop", "mechanism.rpg-cannon", "mechanism.bumpers", "mechanism.slingshots",
			"mechanism.lower-flippers", "mechanism.uk-post-save", "mechanism.captive-ball", "mechanism.heads",
		}, set(by_id))
		self.assertEqual(["device.q1-trough-up-kicker"], by_id["mechanism.trough"]["actuators"])
		self.assertIn("switch.15-4-ball-stacking-opto", by_id["mechanism.trough"]["sensors"])
		self.assertEqual(["switch.16-shooter-lane", "switch.55-gun-trigger"], by_id["mechanism.auto-launch"]["sensors"])
		cannon = by_id["mechanism.rpg-cannon"]
		self.assertEqual(("motorized", ["device.q20-backbox-motor-relay", "device.q5-backbox-kicker"]), (cannon["kind"], cannon["actuators"]))
		self.assertEqual([f"switch.{address}" for address in (41, 42, 43, 44, 45)], [sensor.split("-")[0] for sensor in cannon["sensors"]])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		# The catalog, extraction, ROM-archive and corpus-copy records identify evidence rather than support one device.
		self.assertEqual(set(), declared - cited - {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE, curator.ROM_SOURCE, curator.VPX_CORPUS_HANIBAL_SOURCE})
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
		# The retained table, its script and its extraction carry their acquisition times and the extraction tool version.
		sources = {source["id"]: source for source in self.definition["sources"]}
		for source_id in (curator.VPX_TABLE_SOURCE, curator.VPX_SCRIPT_SOURCE, curator.VPX_EXTRACTION_SOURCE):
			self.assertRegex(sources[source_id].get("acquired_at", ""), r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$", source_id)
		for source_id in (curator.VPX_SCRIPT_SOURCE, curator.VPX_EXTRACTION_SOURCE):
			self.assertIn("vpxtool git:v0.33.3", sources[source_id]["locator"], source_id)

	def test_assembly_pages_qualify_the_grid_part_and_bulb_readings(self) -> None:
		# Page 113: four 500-6698-08 targets and one -79, whose switch subassembly is the grid's 515-6027-08.
		for address in range(41, 46):
			notes = self.device("input.switch", address)["physical"]["notes"]
			self.assertIn("four Stand-Up Targets", notes, address)
			self.assertIn("one 500-6698-08-79 (item 13", notes, address)
			self.assertIn("Switch & White Rectangular Target Sub-Assy. (515-6027-08)", notes, address)
			self.assertEqual("515-6027-08", self.device("input.switch", address)["physical"]["assembly_part_number"], address)
		# Page 101 names a #555 bulb in each bumper; the G.I. wiring page counts them as #44. Both readings stay.
		gi = self.device("output.gi", 0)["physical"]["notes"]
		self.assertIn("20 #44 including 'GIs in Pop Bumpers (X3)'", gi)
		self.assertIn("'#555 Wedge Base Bulb' 165-5002-00, one per bumper", gi)
		self.assertIn("'Note: GI above P/F is #555 Bulb.'", gi)
		self.assertEqual([], [conflict for conflict in self.definition.get("conflicts", []) if "bumper" in json.dumps(conflict).casefold()])
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("no run outside that test saw it driven", knowledge)
		self.assertNotIn("no run saw it lit", knowledge)

	def test_committed_text_names_no_other_machine(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID and len(driver["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		words = set(re.findall(r"[a-z0-9_]{5,}", "\n".join(texts)))
		# Lamp 75 is printed MAX ESCAPE; the word is not a reference to the driver of that name.
		self.assertEqual(set(), words & foreign - {"escape"})

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
		# The retained table draws no bulb for Q26 or Q29; its lamp lights show no bulb mesh, and it copies 73-78 onto none.
		expected = {("pinmame.output.solenoid", 26), ("pinmame.output.solenoid", 29)} | {("pinmame.output.lamp", address) for address in UNPLACED_LAMPS}
		self.assertEqual(expected, missing)
		self.assertEqual(sorted(self.by_binding[key]["id"] for key in expected), load(curator.SPATIAL_REPORT_PATH)["without_placements"])
		gi = self.device("output.gi", 0)
		self.assertEqual((43, 75), (len(gi["spatial"]["placements"]), gi["physical"]["quantity"]))
		for address in (31, 32):
			self.assertEqual(2, len(self.device("output.solenoid", address)["spatial"]["placements"]), address)
		# Cabinet, backbox and back-panel devices carry a controlled not_applicable record.
		for group, address in (("input.switch", 54), ("input.switch", 55), ("input.switch", 52), ("output.solenoid", 20), ("output.solenoid", 24), ("output.solenoid", 30), ("output.lamp", 79)):
			self.assertEqual("not_applicable", self.device(group, address)["spatial"]["status"], (group, address))

	def test_no_lamp_is_placed_on_a_light_without_a_bulb(self) -> None:
		for address in range(1, 81):
			spatial = self.device("output.lamp", address).get("spatial")
			self.assertTrue(spatial is None or spatial["status"] == "not_applicable", address)
		seed = load(SEED_PATH)
		self.assertEqual({}, seed["lamp"])
		self.assertEqual(BOUND_LAMPS, {int(address) for address in seed["lamp_unplaced"]})
		for address, entries in seed["lamp_unplaced"].items():
			for entry in entries:
				self.assertEqual((True, False), (entry["is_bulb_light"], entry["show_bulb_mesh"]), entry["object"])
		self.assertEqual(["l64", "l64a"], [entry["object"] for entry in seed["lamp_unplaced"]["64"]])
		self.assertEqual(
			{"l64": ["LED8"], "l64a": ["LED9"], "l71": ["LED7"]},
			{entry["object"]: [item["object"] for item in entry["bulb_primitives"]] for entries in seed["lamp_unplaced"].values() for entry in entries if entry["bulb_primitives"]},
		)
		for address in BOUND_LAMPS:
			notes = self.device("output.lamp", address)["physical"]["notes"]
			for entry in seed["lamp_unplaced"][str(address)]:
				self.assertIn(entry["object"], notes, address)
			self.assertRegex(notes, r"which shows? no bulb mesh, so (it marks|they mark) no socket and the lamp is not placed\.", address)
			self.assertNotIn("Placement from", notes, address)
		for address in range(73, 79):
			self.assertIn("copies no lamp in 73-79 onto a Light, so it is not placed", self.device("output.lamp", address)["physical"]["notes"], address)
		self.assertIn("does not take them as the lamp sockets", self.device("output.lamp", 64)["physical"]["notes"])
		self.assertIn("does not take it as the lamp socket", self.device("output.lamp", 71)["physical"]["notes"])
		report = load(curator.SPATIAL_REPORT_PATH)
		self.assertTrue(report["projection_classes"]["lamp"].startswith("None placed."))
		self.assertTrue(any("a table that models the insert bulbs or a reproducible measurement on the lamp location drawing" in item for item in report["unresolved_geometry"]))
		# Flashers 31 and 32 stay on the bulb Lights at their Flupper domes.
		for address, domes in ((31, ["Flasher31p1", "Flasher31p2"]), (32, ["Flasher32p1", "Flasher32p2"])):
			self.assertEqual(domes, [entry["dome"] for entry in seed["solenoid"][str(address)]], address)

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_scenarios_name_only_their_game_and_evidence_pins_its_runs(self) -> None:
		document = load(EVIDENCE_PATH)
		self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
		self.assertEqual(curator.RUNTIME_LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
		self.assertEqual((ROM_SHA256, ROM_SHA256, ROM_SHA256), (document["runtime"]["rom_archive_sha256"], curator.ROM_ARCHIVE_SHA256, evidence_tool.ROM_ARCHIVE_SHA256))
		self.assertEqual(curator.PINMAME_REVISION, document["source"]["revision"])
		self.assertEqual(curator.RUNTIME_PATH, evidence_tool.DOCUMENT_PATH)
		self.assertEqual({name: value[0] for name, value in evidence_tool.RUNS.items()}, curator.RUN_MANIFESTS)
		self.assertEqual(set(evidence_tool.RUNS), {run["name"] for run in document["runtime"]["raw_runs"]})
		for run in document["runtime"]["raw_runs"]:
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(run["scenario_sha256"], sha256(scenario), run["name"])
			self.assertEqual("term3", load(scenario)["game"])
			self.assertNotIn(b"\r", scenario.read_bytes(), run["name"])

	def test_gameplay_steps_support_the_switch_to_coil_claims(self) -> None:
		play = steps("term3-gameplay")
		expected = {
			"skill shot (public 52) closed once": [21], "right top lane (public 39) closed once": [3],
			"left bumper (public 49) closed once": [9], "right bumper (public 50) closed once": [10], "bottom bumper (public 51) closed once": [11],
			"left slingshot (public 59) closed once": [17], "right slingshot (public 62) closed once": [18],
			"right 3-bank bottom (public 22) closed once": [4], "captive ball (public 23) closed once": [4, 30, 31, 32],
			"left orbit bottom (public 28) closed once": [22, 23], "left orbit top (public 29) closed once": [22, 23],
			"right orbit top (public 46) closed once": [22, 23], "right orbit bottom (public 24) closed once": [22, 23],
			"T-X made (public 31) closed once": [4, 30, 31, 32], "backbox 5-bank 3 (public 43) closed once": [8],
			"backbox 5-bank 4 (public 44) closed once": [3], "left outlane (public 57) closed once": [12],
			"drop target (public 25) knocked down and left down": [8], "drop target (public 25) back up": [8],
			"a ball rests in the VUK (public 36)": [3, 8, 13, 30], "a ball rests at lockup 1 (right), the T-X cannon trough opto (public 33)": [4, 14, 26, 30],
			"UK left cabinet button (public 1) held": [], "UK left cabinet button (public 1) released": [8],
			"UK right cabinet button (public 8) held": [3, 8], "UK right cabinet button (public 8) released": [],
			"left flipper button (public 84) held": [47, 48], "right flipper button (public 82) held": [45, 46],
			"host writes 1 to the left end-of-stroke input (public 83) while the left flipper button is held": [],
			"host writes 0 to the left end-of-stroke input (public 83)": [],
			"gun trigger (public 55) pulled once": [2, 8, 26], "Start button (public 54)": [3, 4, 30, 31, 32],
		}
		for label, coils in expected.items():
			self.assertEqual(coils, play[label]["active_solenoid_addresses"], label)
		quiet = {10, 17, 18, 19, 20, 21, 30, 32, 37, 38, 40, 41, 42, 45, 58, 60, 61}
		self.assertEqual(quiet, set(curator.GAMEPLAY_QUIET))
		for address in quiet:
			label = next(key for key in play if re.search(rf"\(public {address}\) closed once$", key))
			self.assertEqual([], play[label]["active_solenoid_addresses"], label)
		# The served ball reached 16 before the ROM served one: the ROM raised game-on 15 and fired the auto launch 2 itself.
		self.assertTrue({2, 15} <= set(play["the served ball rests on the shooter lane switch 16"]["active_solenoid_addresses"]))
		serve = steps("term3-ball-serve")
		self.assertEqual([], serve["the served ball rests on the shooter lane switch 16 for 10 s"]["active_solenoid_addresses"])
		self.assertEqual([2, 8, 26], serve["gun trigger (public 55) pulled once"]["active_solenoid_addresses"])
		self.assertIn(1, serve["the trough up-kicker (solenoid 1) fires after Start"]["active_solenoid_addresses"])
		for run in (play, serve):
			for coin in range(1, 5):
				self.assertEqual([24], run[f"coin {coin} on the center coin slot (public 5)"]["active_solenoid_addresses"], coin)
		stack = steps("term3-stacking-opto")
		self.assertEqual(([1, 2], [], [1, 2]), tuple(stack[label]["active_solenoid_addresses"] for label in ("public 15 raised to 1 in attract mode", "public 15 lowered back to 0", "public 15 raised to 1 a second time")))

	def test_only_the_coil_test_drives_unused_and_uk_outputs(self) -> None:
		observations = load(EVIDENCE_PATH)["runtime"]["observations"]
		outside = set()
		for observation in observations["named_action_observations"]:
			if not observation["label"].startswith("term3-single-coil-test "):
				outside |= set(observation["transitioned_solenoid_addresses"])
		self.assertEqual(set(), outside & (UNUSED_SOLENOIDS | {33, 34, 35}))
		self.assertFalse(set(observations["solenoid_addresses_seen"]) & {16, *range(36, 45), 49, 50})
		self.assertEqual([0], observations["gi_addresses_seen"])
		lamps = set(observations["lamp_addresses_driven_outside_self_test"])
		self.assertEqual(set(range(1, 81)) - {54, 70}, lamps)

	def test_service_tests_name_every_address(self) -> None:
		evidence = curator.load_runtime()
		switches = curator.switch_test_readings(evidence)
		self.assertEqual(set(range(1, 65)), set(switches))
		self.assertEqual(("LT BUTTON (UK ONLY)", "GRN-BRN WHT-BRN #01"), switches[1])
		self.assertEqual(("NONE", ""), switches[3])
		self.assertEqual(("GUN TRIGGER", "GRN-VIO WHT-VIO #55"), switches[55])
		dedicated = curator.dedicated_test_readings(evidence)
		self.assertEqual({81: ("NONE", ""), 83: ("NONE", ""), 82: ("#3 RIGHT FLIPPER BUTTON", "CN6-4 GRY-ORG CN6-1 BLK"), 84: ("#1 LEFT FLIPPER BUTTON", "CN6-2 GRY-BRN CN6-1 BLK"), 88: ("#5 NOT USED", "CN6-7 GRY-GRN CN6-1 BLK")}, dedicated)
		lamps = curator.lamp_test_readings(evidence)
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertEqual((("NOT USED", "YEL-VIO RED-GRY #63"), ("NOT USED", "YEL-BLU RED-WHT #70")), (lamps[63], lamps[70]))
		self.assertEqual(("AUTO LAUNCH (OPT.)", "YEL-VIO RED #79"), lamps[79])
		coils = curator.coil_test_readings(evidence)
		self.assertEqual(set(range(1, 15)) | set(range(17, 36)) | {46, 48}, set(coils))
		self.assertEqual(("#15 LEFT FLIPPER (50V RED/YEL)", "GRY-YEL ORG-GRY"), coils[48])
		self.assertEqual(("#16 RIGHT FLIPPER (50V RED/YEL)", "BLU-YEL ORG-VIO"), coils[46])
		self.assertEqual(("#6 NOT USED", "YEL-VIO BRN-BLU"), coils[6])
		self.assertEqual(("AUX 1: LEFT UP/DOWN POST", "BRN WHT"), coils[33])

	def test_service_test_checks_refuse_tampered_readings(self) -> None:
		evidence = curator.load_runtime()

		def snapshot(document: dict, label: str) -> dict:
			return next(item for item in document["runtime"]["observations"]["diagnostic_snapshots"] if item["label"] == label)

		def action(document: dict, label: str) -> dict:
			return next(item for item in document["runtime"]["observations"]["named_action_observations"] if item["label"] == label)

		renamed = copy.deepcopy(evidence)
		snapshot(renamed, "term3-switch-test snapshot: switch 54 closed in the Switch Test")["interpreted_text"] = "SWITCH TEST / SHOOTER LANE / GRN-VIO WHT-BLU #54 / DOOR BUTTONS OPERATE MENU"
		with self.assertRaisesRegex(RuntimeError, "switch 54"):
			curator.switch_test_readings(renamed)
		rewired = copy.deepcopy(evidence)
		snapshot(rewired, "term3-switch-test snapshot: switch 54 closed in the Switch Test")["interpreted_text"] = "SWITCH TEST / START BUTTON / GRN-VIO WHT-VIO #54 / DOOR BUTTONS OPERATE MENU"
		with self.assertRaisesRegex(RuntimeError, "switch 54"):
			curator.switch_test_readings(rewired)
		eos = copy.deepcopy(evidence)
		snapshot(eos, "term3-dedicated-switch-test snapshot: left flipper end-of-stroke input (public 83) held in the Dedicated Switch Test")["interpreted_text"] = "DEDICATED SWITCH TEST / #2 LEFT FLIPPER EOS / PRESS START TO EXIT TEST"
		with self.assertRaisesRegex(RuntimeError, "dedicated input 83"):
			curator.dedicated_test_readings(eos)
		missing = copy.deepcopy(evidence)
		missing["runtime"]["observations"]["diagnostic_snapshots"].remove(snapshot(missing, "term3-single-lamp-test snapshot: Black ENTER button (public 0) pressed on +: lamp step 63"))
		with self.assertRaisesRegex(RuntimeError, "lacks the frame"):
			curator.lamp_test_readings(missing)
		spread = copy.deepcopy(evidence)
		action(spread, "term3-single-lamp-test step 48: Black ENTER button (public 0) pressed on +: lamp step 40; lamps changed during the step: 40")["label"] += ", 63"
		with self.assertRaisesRegex(RuntimeError, "lamp 40"):
			curator.lamp_test_readings(spread)
		misfired = copy.deepcopy(evidence)
		action(misfired, "term3-single-coil-test step 54: Black ENTER button (public 0) pressed on RUN: coil step 12 fired")["transitioned_solenoid_addresses"] = [12, 13]
		with self.assertRaisesRegex(RuntimeError, "coil step 12"):
			curator.coil_test_readings(misfired)
		leaked = copy.deepcopy(evidence)
		action(leaked, "term3-gameplay step 61: drain: the drained ball lands on trough position 11, leaving four balls on 11-14; GI 0 states during the step: 0")["transitioned_solenoid_addresses"].append(33)
		with self.assertRaisesRegex(RuntimeError, "UK-only outputs"):
			curator._check_unused_outputs(self.definition, leaked)

	def test_frame_readings_seed_matches_every_snapshot(self) -> None:
		pins = load(FRAME_SEED_PATH)
		self.assertEqual(MACHINE_ID, pins["machine_id"])
		self.assertEqual({"term3-switch-test", "term3-dedicated-switch-test", "term3-single-lamp-test", "term3-single-coil-test"}, set(pins["runs"]))
		snapshots = {item["label"]: item for item in load(EVIDENCE_PATH)["runtime"]["observations"]["diagnostic_snapshots"]}
		pinned = set()
		for run, readings in pins["runs"].items():
			for label, pin in readings.items():
				key = f"{run} snapshot: {label}"
				pinned.add(key)
				self.assertEqual((pin["pixel_sha256"], pin["reading"]), (snapshots[key]["pixel_sha256"], snapshots[key]["interpreted_text"]), key)
		self.assertEqual(set(snapshots), pinned)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained harness runs are not available")
	def test_frame_readings_refuse_a_substituted_frame(self) -> None:
		root = evidence_tool.base.review_artifacts_root(required=True)
		original = evidence_tool.base._load_run

		def swapped(*args):
			run, listed = original(*args)
			if args[1] == "term3-dedicated-switch-test":
				labels = [item["label"] for item in run["snapshots"]]
				held = labels.index("dedicated input 88 (DS-5) (public 88) held in the Dedicated Switch Test")
				run["snapshots"][held]["displays"] = run["snapshots"][labels.index("left flipper button (public 84) held in the Dedicated Switch Test")]["displays"]
			return run, listed

		with mock.patch.object(evidence_tool.base, "_load_run", swapped):
			with self.assertRaisesRegex(RuntimeError, "does not carry the frame the curator read"):
				evidence_tool.build(root)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		self.assertEqual(canonical_bytes(evidence_tool.build(root)), EVIDENCE_PATH.read_bytes())

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_lamp_63_follows_lamp_64_outside_the_lamp_test(self) -> None:
		for name in evidence_tool.RUNS:
			if name == LAMP_TEST_RUN:
				continue
			run = raw_run(name)
			mirrored, tx = events(run, "lamp", 63), events(run, "lamp", 64)
			self.assertTrue(mirrored, name)
			self.assertEqual([state for _, state in tx], [state for _, state in mirrored], name)
			self.assertTrue(all(abs(left - right) < 0.001 for (left, _), (right, _) in zip(mirrored, tx)), name)
			self.assertAlmostEqual(9.3, mirrored[0][0], delta=0.1)
			for address in (54, 70):
				self.assertEqual([], events(run, "lamp", address), (name, address))

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_retained_runs_support_the_launch_timing_notes(self) -> None:
		serve = raw_run("term3-ball-serve")
		game_on = rises(serve, "solenoid", 15)[0]
		self.assertAlmostEqual(5.4, game_on - rises(serve, "switch", 54)[0], delta=0.05)
		self.assertEqual(1, len(rises(serve, "solenoid", 1)))
		self.assertAlmostEqual(0.7, rises(serve, "solenoid", 1)[0] - game_on, delta=0.05)
		ball, gun = rises(serve, "switch", 16)[0], rises(serve, "switch", 55)[0]
		self.assertAlmostEqual(10.0, gun - ball, delta=0.05)
		launches = rises(serve, "solenoid", 2)
		self.assertEqual(3, len(launches))
		self.assertAlmostEqual(0.081, launches[0] - gun, delta=0.005)
		self.assertAlmostEqual(1.67, launches[1] - launches[0], delta=0.01)
		self.assertAlmostEqual(3.34, launches[2] - launches[0], delta=0.01)
		self.assertAlmostEqual(1.6, rises(serve, "solenoid", 26)[0] - gun, delta=0.1)
		play = raw_run("term3-gameplay")
		self.assertEqual([], rises(play, "solenoid", 1))
		ball, gun, left = rises(play, "switch", 16)[0], rises(play, "switch", 55)[0], falls(play, "switch", 16)[0]
		self.assertLess(ball, rises(play, "solenoid", 15)[0])
		launches = rises(play, "solenoid", 2)
		self.assertEqual(7, len(launches))
		self.assertAlmostEqual(0.76, launches[0] - ball, delta=0.01)
		triggered = [time for time in launches if 0 <= time - gun < 0.1]
		self.assertEqual(1, len(triggered))
		self.assertAlmostEqual(0.043, triggered[0] - gun, delta=0.005)
		self.assertTrue(all(1.55 <= later - earlier <= 1.72 for earlier, later in zip(launches, launches[1:]) if later not in triggered))
		self.assertTrue(all(time < left for time in launches[:-1]))
		self.assertAlmostEqual(0.18, launches[-1] - left, delta=0.01)
		flasher = events(play, "solenoid", 26)
		self.assertEqual([1, 0, 1, 0], [state for _, state in flasher])
		self.assertAlmostEqual(1.6, flasher[0][0] - gun, delta=0.1)
		self.assertAlmostEqual(15.8, flasher[1][0] - flasher[0][0], delta=0.05)
		self.assertAlmostEqual(14.5, flasher[3][0] - flasher[2][0], delta=0.05)
		lockup = rises(play, "switch", 33)[0]
		self.assertTrue(lockup < flasher[2][0] < falls(play, "switch", 33)[0])
		for run in (serve, play):
			# Lamp 79 blinked from the game-on rise until about 1.4-1.6 s after the trigger pull.
			launch_lamp = events(run, "lamp", 79)
			on = rises(run, "solenoid", 15)[0]
			self.assertTrue(0 < launch_lamp[0][0] - on < 0.2)
			self.assertTrue(1.35 <= launch_lamp[-1][0] - rises(run, "switch", 55)[0] <= 1.65)
			# 45-48 rise for one update just before the game-on state 15.
			for address in (45, 46, 47, 48):
				first = events(run, "solenoid", address)[:2]
				self.assertEqual([1, 0], [state for _, state in first], address)
				self.assertLess(first[1][0] - first[0][0], 0.03, address)
				self.assertAlmostEqual(on, first[1][0], delta=0.01)
			# Each coin pulsed the coin meter 24 four times.
			coins = rises(run, "switch", 5)
			for coin, following in zip(coins, coins[1:] + [coins[-1] + 1.6]):
				self.assertEqual(4, len([time for time in rises(run, "solenoid", 24) if coin <= time < following]))

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_retained_runs_support_the_stacking_opto_and_up_post_notes(self) -> None:
		stack = raw_run("term3-stacking-opto")
		edges = events(stack, "switch", 15)
		self.assertEqual([1, 0, 1], [state for _, state in edges])
		for rise in (edges[0][0], edges[2][0]):
			kicks = [time for time in rises(stack, "solenoid", 1) if rise < time < rise + 20]
			self.assertEqual(6, len(kicks))
			self.assertAlmostEqual(1.0, kicks[0] - rise, delta=0.1)
			self.assertTrue(all(0.75 <= later - earlier <= 0.9 for earlier, later in zip(kicks, kicks[1:])))
			launches = [time for time in rises(stack, "solenoid", 2) if rise < time < rise + 20]
			self.assertEqual(1, len(launches))
			self.assertAlmostEqual(9.1, launches[0] - rise, delta=0.1)
		self.assertEqual([], [event for event in stack["events"] if event["event"] == "solenoid" and event["state"] and edges[1][0] <= event["time_s"] < edges[2][0]])
		play = raw_run("term3-gameplay")
		for address in (24, 28, 29, 46):
			closed = rises(play, "switch", address)[0]
			starts = []
			for post in (22, 23):
				on = next(time for time in rises(play, "solenoid", post) if closed <= time)
				off = next(time for time in falls(play, "solenoid", post) if on < time)
				self.assertTrue(2.05 <= off - on <= 2.25, (address, post))
				starts.append(on)
			self.assertTrue(0.15 <= abs(starts[0] - starts[1]) <= 0.5, address)
			self.assertLess(min(starts) - closed, 0.1, address)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_extraction_script_and_seed_match(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		curator.verify_extraction_manifest(root)
		base = root / curator.EXTRACTION_MANIFEST_RELATIVE_PATH.parent
		table = base / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, sha256(table))
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, sha256(script))
		self.assertEqual(script.read_bytes(), (base / "Terminator 3 (Stern 2003) Hanibal v1.5.vbs").read_bytes())
		self.assertEqual(curator.HANIBAL_CORPUS_LF_SHA256, hashlib.sha256(script.read_bytes().replace(b"\r\n", b"\n")).hexdigest())
		built = seed_tool.canonical(seed_tool.build(root / curator.EXTRACTION_RELATIVE_PATH, table))
		self.assertEqual(built.encode("utf-8"), SEED_PATH.read_bytes())
		code = "\n".join(re.sub(r"'.*", "", line) for line in script.read_text(encoding="latin-1").splitlines())
		self.assertIn('cGameName = "term3"', code)
		self.assertIn('LoadVPM "01560000", "SEGA.VBS"', code)
		self.assertIn(".InitSw 0, 14, 13, 12, 11, 0, 0, 0", code)
		self.assertIn("vpmNudge.TiltSwitch = 56", code)
		# The defects the knowledge note lists: 15, 1, 8, 81 and 83 are never written, Solcallback(29) is empty, and no line
		# copies lamps 53, 54, 63, 70 or 73-79 onto a light.
		written = {int(number) for number in re.findall(r"(?:PulseSw|pulseswitch)\s*\(?\s*(\d+)", code, re.IGNORECASE)}
		written |= {int(number) for number in re.findall(r"Switch\(\s*(\d+)\s*\)", code, re.IGNORECASE)}
		self.assertEqual(set(), written & {1, 8, 15, 81, 83})
		self.assertRegex(code, r'Solcallback\(29\) = ""\s*\n')
		bound = {int(number) for number in re.findall(r"^\s*Kombilicht\s+(\d+),", code, re.MULTILINE)}
		self.assertEqual(set(), bound & {53, 54, 63, 70, *range(73, 80)})
		self.assertIn("Kombiflasher 134, l71, FlasherTLicht", code)
		self.assertIn("Kombiflasher 135, l64, FlasherTx1", code)
		names = {path.stem.split(".", 1)[-1].casefold() for path in (root / curator.EXTRACTION_RELATIVE_PATH / "gameitems").glob("*.json")}
		# Every Light the script drives for a lamp is a bulb-mode Light that shows no bulb mesh, so none is placed.
		gameitems = root / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		bound = {f"l{address}a" for address in BOUND_LAMPS - {64, 71}} | {"l64", "l64a", "l71"}
		for name in bound:
			light = json.loads((gameitems / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]
			self.assertEqual((True, False), (light["is_bulb_light"], light["show_bulb_mesh"]), name)
		self.assertEqual(bound, {entry["object"] for entries in load(SEED_PATH)["lamp_unplaced"].values() for entry in entries})
		# Each placed flasher Light coincides with its Flupper dome, which draws DomeOff at rest.
		by_key = seed_tool._candidates(root / curator.EXTRACTION_RELATIVE_PATH, table)
		for light_name, dome in seed_tool.DOMES.items():
			primitive = json.loads((gameitems / f"Primitive.{dome}.json").read_text(encoding="utf-8"))["Primitive"]
			self.assertEqual("domeoff", primitive["image"].casefold(), dome)
			distance = math.dist(seed_tool._point(by_key, "Light", light_name), seed_tool._point(by_key, "Primitive", dome))
			self.assertLess(distance, seed_tool.DOME_DISTANCE, light_name)
		self.assertTrue({"ballrelease", "txshot", "swplunger", "sw52", "sw57", "sw60"} <= names)

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_manual_and_ipdb_page_match_their_pins(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / MACHINE_ID / "ipdb"
		self.assertEqual(curator.MANUAL_SHA256, sha256(root / curator.MANUAL_NAME))
		self.assertEqual(curator.IPDB_PAGE_SHA256, sha256(root / curator.IPDB_PAGE_NAME))

	@unittest.skipUnless(os.environ.get("PINMAME_ROM_LIBRARY_ROOT"), "authorized ROM library root is not configured")
	def test_the_rom_archive_the_harness_booted_matches_its_pin(self) -> None:
		archive = Path(os.environ["PINMAME_ROM_LIBRARY_ROOT"]) / "term3.zip"
		self.assertEqual(ROM_SHA256, sha256(archive))
		with zipfile.ZipFile(archive) as members:
			crcs = {item.filename: f"{item.CRC:08x}" for item in members.infolist()}
		self.assertEqual(("872f9351", "6b7cc4f8"), (crcs["t3cpu.400"], crcs["t3dispa.400"]))
		self.assertEqual({"t3100.u7", "t3100.u17", "t3100.u21", "t3100.u36", "t3100.u37"}, set(crcs) - {"t3cpu.400", "t3dispa.400"})


if __name__ == "__main__":
	unittest.main()
