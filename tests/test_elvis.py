from __future__ import annotations

import hashlib
import json
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

import curate_elvis as curator  # noqa: E402
import elvis_runtime_evidence as evidence_tool  # noqa: E402
import elvis_spatial_seed as seed_tool  # noqa: E402

MACHINE_ID = "stern.elvis.2004"
DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "elvis-2004.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "elvis-2004.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "elvis-2004.md"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "elvis-2004-spatial.json"
FRAME_READINGS_PATH = ROOT / "tools" / "seeds" / "stern" / "elvis-2004-frame-readings.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "elvis-service-tests-and-gameplay.json"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / MACHINE_ID

DRIVER_IDS = {"elvis", "elvisl", "elvisg", "elvisf", "elvisi", "elv100"} | {
	f"elv{version}{language}" for version in ("400", "303", "302") for language in ("", "l", "g", "f", "i")
}
# The Switch Matrix Grid's NOT USED cells (excerpt switch-matrix.md).
NOT_USED_SWITCHES = {29, 35, 44}
# The UK-only cabinet buttons, the coin-door positions beyond the three stock slots, and the tournament kit's button.
OPTIONAL_SWITCHES = {1, 2, 3, 7, 8, 55}
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
# Members of the user-authorized elvis.zip and their CRCs, as elvis.c's elvis ROM set pins them.
ROM_MEMBERS = {
	"elvscpua.500": "aae9d65d", "elvsdspa.500": "76a672cb", "elvis.u7": "1df6c1b5", "elvis.u17": "ff032897",
	"elvis.u21": "c3c19a40", "elvis.u36": "e98f0dc9", "elvis.u37": "88ba0966",
}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def steps(run: str) -> dict[str, dict]:
	prefix = f"{run} step "
	return {item["label"].split(": ", 1)[1].split(";")[0]: item for item in load(EVIDENCE_PATH)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith(prefix)}


def raw_run(name: str) -> dict:
	return load(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / name / "run.json")


def edges(run: dict, kind: str, number: int, state: bool) -> list[float]:
	return [event["time_s"] for event in run["events"] if event["event"] == kind and event.get("number") == number and bool(event["state"]) == state and not event.get("initial")]


class ElvisTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, 4983, "G4qbX-MJw5r", 2004, "I-0084", "Stern"), (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["year"], machine["model_number"], machine["manufacturer"]))
		self.assertEqual(21, len(DRIVER_IDS))
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual(dict.fromkeys(DRIVER_IDS, "identical"), compatibility)
		self.assertEqual({"elvis"}, {driver["clone_of"] for driver in self.definition["drivers"] if "clone_of" in driver})
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("observed", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])
		catalog = load(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID}
		self.assertEqual(DRIVER_IDS, claimed)
		record = next(item for item in catalog["machines"] if item["id"] == MACHINE_ID)
		self.assertEqual(94, record["completion_score"])

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
		switches = {address: self.device("input.switch", address)["availability"] for address in list(range(1, 65)) + list(range(81, 89))}
		self.assertEqual(NOT_USED_SWITCHES | {85, 86, 87}, {address for address, value in switches.items() if value == "unused"})
		self.assertEqual(OPTIONAL_SWITCHES, {address for address, value in switches.items() if value == "optional"})
		self.assertEqual("used", switches[88])
		self.assertEqual({4, 24}, {address for address in range(1, 51) if self.device("output.solenoid", address)["availability"] == "optional"})
		self.assertEqual({79}, {address for address in range(1, 81) if self.device("output.lamp", address)["availability"] == "optional"})
		self.assertEqual(set(), {address for address in range(1, 81) if self.device("output.lamp", address)["availability"] == "unused"})
		self.assertEqual({1, 2, 3, 4, 5}, {address for address in range(1, 9) if self.device("input.dip", address)["availability"] == "used"})
		for address in NOT_USED_SWITCHES:
			notes = self.device("input.switch", address)["physical"]["notes"]
			self.assertIn("prints this cell NOT USED", notes, address)
			self.assertIn("printed \"NOT USED / ", notes, address)
			self.assertIn(f"#{address}\".", notes, address)

	def test_polarity_follows_the_read_path_the_rom_and_the_wiring_diagrams(self) -> None:
		self.assertEqual({64}, {address for address in range(1, 65) if self.device("input.switch", address)["normally_closed"]})
		for address, role in ((81, "internal.flipper.lower.right.eos"), (83, "internal.flipper.lower.left.eos")):
			eos = self.device("input.switch", address)
			self.assertTrue(eos["normally_closed"], address)
			self.assertEqual([role], eos["roles"])
			self.assertIn("A host write is overwritten", eos["physical"]["notes"])
			self.assertIn("core_updateSw", eos["physical"]["notes"])
		for address in (82, 84, 88, -3, -2, -1, 0):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertEqual({11, 12, 13, 14, 33, 64}, {address for address in range(1, 65) if self.device("input.switch", address).get("initial_active")})
		self.assertTrue(self.device("input.switch", -3)["initial_active"])
		for address in (14, 15):
			self.assertEqual("opto", self.device("input.switch", address)["physical"]["switch_type"], address)
		for address in (16, 25):
			self.assertEqual("unknown", self.device("input.switch", address)["physical"]["switch_type"], address)
		self.assertFalse(self.device("input.switch", 64)["pulse"])
		self.assertIn(curator.RUNTIME_SOURCE, self.device("input.switch", 64)["provenance"]["source_refs"])
		self.assertIn(curator.SIM_SOURCE, self.device("input.switch", 33)["provenance"]["source_refs"])
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("leave 81 and 83 to PinMAME", knowledge)
		self.assertNotIn("PinMAME never writes them", knowledge)

	def test_flipper_remap_and_synthetic_states(self) -> None:
		left = self.device("output.solenoid", 48)
		right = self.device("output.solenoid", 46)
		self.assertEqual(("device.q15-left-flipper", "coil", "Q15"), (left["id"], left["kind"], left["wiring"]["driver_transistor"]))
		self.assertEqual(("device.q16-right-flipper", "coil", "Q16"), (right["id"], right["kind"], right["wiring"]["driver_transistor"]))
		self.assertEqual(("device.q13-upper-left-flipper", "device.q14-upper-right-flipper"), (self.device("output.solenoid", 13)["id"], self.device("output.solenoid", 14)["id"]))
		for address in (15, 45, 47):
			self.assertEqual(("virtual", "used"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		for address in (16, *range(33, 45), 49, 50):
			self.assertEqual(("virtual", "unused"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		kinds = {address: self.device("output.solenoid", address)["kind"] for address in list(range(1, 15)) + list(range(17, 33))}
		self.assertEqual({20, 21, 22, 23, 31, 32}, {address for address, kind in kinds.items() if kind == "flasher"})
		self.assertEqual({4, 25, 26, 27, 28}, {address for address, kind in kinds.items() if kind == "motor"})
		self.assertEqual({5}, {address for address, kind in kinds.items() if kind == "magnet"})
		self.assertEqual({20: 2, 21: 1, 22: 1, 23: 2, 32: 2}, {address: self.device("output.solenoid", address)["physical"]["quantity"] for address in kinds if "quantity" in self.device("output.solenoid", address)["physical"]})

	def test_wiring_comes_from_the_printed_tables(self) -> None:
		trough = self.device("output.solenoid", 1)["wiring"]
		self.assertEqual(("Q1", "BRN-BLK", "J8-P1", "YEL-VIO", "J10-P4/5", 50), (trough["driver_transistor"], trough["control_wire"], trough["control_connection"], trough["power_wire"], trough["power_connection"], trough["nominal_voltage_v"]))
		self.assertNotIn("nominal_voltage_v", self.device("output.solenoid", 4)["wiring"])
		self.assertEqual(("VIO-ORG", "J7-P4", 20), tuple(self.device("output.solenoid", 19)["wiring"][key] for key in ("control_wire", "control_connection", "nominal_voltage_v")))
		self.assertEqual(("VIO-GRY", "J7-P10", "J16-P7", 5), tuple(self.device("output.solenoid", 24)["wiring"][key] for key in ("control_wire", "control_connection", "power_connection", "nominal_voltage_v")))
		self.assertEqual([("RED", "J6-P1"), ("GRN", "J6-P2"), ("BLK", "J6-P3"), ("BLU", "J6-P4")], [(self.device("output.solenoid", address)["wiring"]["control_wire"], self.device("output.solenoid", address)["wiring"]["control_connection"]) for address in (25, 26, 27, 28)])
		switch = self.device("input.switch", 54)["wiring"]
		self.assertEqual(("GRN-VIO", "CN5-P8", "WHT-BLU", "CN7-P3"), (switch["drive_wire"], switch["drive_connection"], switch["return_wire"], switch["return_connection"]))
		for address, wire, pin in ((1, "WHT-BRN", "CN7-P9"), (8, "WHT-GRY", "CN7-P1"), (64, "WHT-GRY", "CN7-P1")):
			wiring = self.device("input.switch", address)["wiring"]
			self.assertEqual((wire, pin), (wiring["return_wire"], wiring["return_connection"]), address)
		for address, wire, pin in ((84, "GRY-BRN", "CN6-P2"), (83, "GRY-RED", "CN6-P3"), (82, "GRY-ORG", "CN6-P4"), (81, "GRY-YEL", "CN6-P6"), (88, "GRY-GRN", "CN6-P7")):
			wiring = self.device("input.switch", address)["wiring"]
			self.assertEqual((wire, pin), (wiring["drive_wire"], wiring["drive_connection"]), address)
		lamp = self.device("output.lamp", 80)["wiring"]
		self.assertEqual(("YEL-GRY", "J13-P1", "RED", "J12-P11"), (lamp["drive_wire"], lamp["drive_connection"], lamp["return_wire"], lamp["return_connection"]))
		bulbs = {address: self.device("output.lamp", address)["physical"]["part_number"] for address in range(1, 81)}
		self.assertEqual(set(range(33, 39)) | set(range(45, 49)) | {60, 61, 62} | set(range(73, 79)), {address for address, part in bulbs.items() if part == "165-5000-44-HF"})
		self.assertEqual(("165-5053-05", "165-5053-02", "165-5053-07"), (bulbs[70], bulbs[71], bulbs[72]))

	def test_mechanisms_reference_declared_devices(self) -> None:
		ids = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		owners: dict[str, str] = {}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= ids, mechanism["id"])
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owners, actuator)
				owners[actuator] = mechanism["id"]
		by_id = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		figure = by_id["mechanism.elvis-figure"]
		self.assertEqual(("motorized", [f"device.q{number}-{name}" for number, name in ((25, "stepper-phase-1"), (26, "stepper-phase-2"), (27, "stepper-phase-3"), (28, "stepper-phase-4"), (29, "elvis-legs"), (30, "elvis-arms"))]), (figure["kind"], figure["actuators"]))
		self.assertEqual({"mechanism.elvis-figure.home": ["switch.33-elvis-home"]}, {position["id"]: position["sensors"] for position in figure["positions"]})
		self.assertEqual(([], ["switch.64-hound-dog"]), (by_id["mechanism.hound-dog"]["actuators"], by_id["mechanism.hound-dog"]["sensors"]))
		self.assertEqual(([], ["switch.1-left-cabinet-button-uk-only", "switch.8-right-cabinet-button-uk-only"]), (by_id["mechanism.uk-post-save"]["actuators"], by_id["mechanism.uk-post-save"]["sensors"]))
		self.assertEqual(["switch.84-left-flipper-button", "switch.88-upper-right-flipper-button"], by_id["mechanism.upper-flippers"]["sensors"])
		self.assertEqual([], self.definition["relationships"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		self.assertEqual(set(), declared - cited - {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE, curator.ROM_SOURCE, curator.VPX_CORPUS_SOURCE})
		paths = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], sha256(ROOT / excerpt["path"]), excerpt["id"])
				self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])
				self.assertIn(excerpt["transcribed_by"], {"curator, read from the rendered page", "curator, quoted from the source file"}, excerpt["id"])
				paths.add(Path(excerpt["path"]).name)
		self.assertEqual({path.name for path in EXCERPT_DIRECTORY.iterdir()}, paths)
		corpus = next(source for source in self.definition["sources"] if source["id"] == curator.VPX_CORPUS_SOURCE)
		self.assertTrue(corpus["uri"].endswith("/Elvis%20%28Stern%202004%29%20WED%20SSF%20Mod.vbs"), corpus["uri"])

	def test_committed_text_names_no_other_machine(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID and len(driver["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		words = set(re.findall(r"[a-z0-9_]{5,}", "\n".join(texts)))
		# BREAK is the name of lamp 61 and part of HEART BREAK HOTEL, not a reference to another game's driver.
		self.assertEqual(set(), words & foreign - {"break"})
		for path in (DEFINITION_PATH, KNOWLEDGE_PATH, curator.SPATIAL_REPORT_PATH, curator.SPATIAL_REPORT_MARKDOWN_PATH):
			self.assertNotIn(b"\r", path.read_bytes(), path.name)

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
		expected = {("pinmame.input.switch", 10)} | {("pinmame.output.solenoid", address) for address in (20, 21, 23, 31)} | {("pinmame.output.lamp", address) for address in range(1, 79)}
		self.assertEqual(expected, missing)
		self.assertEqual(sorted(self.by_binding[key]["id"] for key in expected), load(curator.SPATIAL_REPORT_PATH)["without_placements"])
		# Every seeded lamp is an insert overlay the curator must not place.
		self.assertEqual({str(address) for address in list(range(1, 60)) + [63, 64]}, set(seed["lamp"]))
		gi = self.device("output.gi", 0)
		self.assertEqual(["gi10", "gi11", "gi13", "gi14", "gi27", "gi9"], [entry["object"] for entry in seed["gi"]["0"]])
		self.assertEqual(6, len(gi["spatial"]["placements"]))
		self.assertEqual(26, len(seed["gi_without_bulb"]["0"]))
		self.assertEqual(48, gi["physical"]["quantity"])
		self.assertEqual(2, len(self.device("output.solenoid", 32)["spatial"]["placements"]))
		self.assertEqual(2, self.device("output.solenoid", 23)["physical"]["quantity"])
		for address in (79, 80):
			self.assertEqual("not_applicable", self.device("output.lamp", address)["spatial"]["status"], address)

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_scenarios_name_only_their_game_and_evidence_pins_its_runs(self) -> None:
		document = load(EVIDENCE_PATH)
		self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
		self.assertEqual(curator.RUNTIME_LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
		self.assertEqual(curator.ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"])
		self.assertEqual(curator.ROM_ARCHIVE_SHA256, evidence_tool.ROM_ARCHIVE_SHA256)
		self.assertEqual(curator.PINMAME_REVISION, document["source"]["revision"])
		self.assertEqual(set(evidence_tool.RUNS), {run["name"] for run in document["runtime"]["raw_runs"]})
		self.assertEqual(evidence_tool.RUNS, curator.RUN_MANIFESTS)
		for run in document["runtime"]["raw_runs"]:
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(run["scenario_sha256"], sha256(scenario), run["name"])
			self.assertEqual("elvis", load(scenario)["game"])
			self.assertNotIn(b"\r", scenario.read_bytes(), run["name"])

	def test_gameplay_steps_support_the_switch_to_coil_claims(self) -> None:
		observed = steps("elvis-gameplay")
		expected = {
			"left bumper (public 49) closed once": {4, 9}, "right bumper (public 50) closed once": {4, 10},
			"bottom bumper (public 51) closed once": {4, 11}, "left slingshot (public 59) closed once": {17, 32},
			"right slingshot (public 62) closed once": {18, 32}, "TC(B) target (public 24) closed once": {21, 30, 31},
			"spinner (public 25) closed once": {22}, "top hotel standup (public 52) closed once": {19, 20, 21},
			"ELVI(S) drop target (public 21) knocked down and left down": {3, 22, 32},
			"a ball rests in the center saucer (public 34)": {6, 19}, "a ball rests in the top saucer (public 32)": {12, 19},
			"left flipper button (public 84) held 1.5 s": {13, 47, 48}, "right flipper button (public 82) held 1.5 s": {45, 46},
			"dedicated input 88 (DS-5) held 1.5 s": {14}, "dedicated input 88 (DS-5) held down with 82 still held": {14},
			"Start button (public 54)": {1, 3, 15},
		}
		for label, coils in expected.items():
			self.assertTrue(coils <= set(observed[label]["active_solenoid_addresses"]), label)
		for label in ("right flipper button (public 82) held 1.5 s", "right flipper button (public 82) held down"):
			self.assertNotIn(14, observed[label]["active_solenoid_addresses"], label)
		self.assertIn(14, observed["dedicated input 88 (DS-5) released"]["transitioned_solenoid_addresses"])
		self.assertNotIn(7, observed["a ball rests on the hotel post switch (public 48)"]["active_solenoid_addresses"])
		self.assertNotIn(2, observed["the served ball rests on the shooter lane switch 16"]["active_solenoid_addresses"])
		for label in ("spot note standup (public 9) closed once", "(T)CB target (public 22) closed once", "T(C)B target (public 23) closed once",
				"inner loop (public 27) closed once", "left ramp exit (public 31) closed once", "ELV(I)S drop target (public 20) knocked down and left down"):
			self.assertEqual([], observed[label]["active_solenoid_addresses"], label)
		self.assertEqual([4, 30], observed["(E)LVIS drop target (public 17) knocked down and left down"]["active_solenoid_addresses"])
		search = set(observed["right flipper button (public 82) released"]["active_solenoid_addresses"]) | set(observed["the ball drains: trough position 11 fills again"]["active_solenoid_addresses"])
		self.assertTrue({2, 3, 5, 6, 7, 9, 10, 11, 12, 17, 18, 19} <= search)
		stacking = steps("elvis-stacking-opto")
		self.assertEqual([1, 2], stacking["public 15 raised to 1 in attract mode"]["active_solenoid_addresses"])
		self.assertEqual([], stacking["public 15 lowered back to 0"]["active_solenoid_addresses"])
		probe = steps("elvis-hound-dog-probe")
		self.assertIn(19, probe["round 1: hotel door (public 63) raised to 1 and held 2.5 s"]["active_solenoid_addresses"])
		self.assertEqual([19], probe["round 2: hound dog (public 64) lowered to 0 and left 2.5 s"]["active_solenoid_addresses"])
		test = steps("elvis-elvis-test")
		self.assertEqual([29], test["Black ENTER button (public 0) pressed on LEGS: legs coil energized"]["active_solenoid_addresses"])
		self.assertEqual([30], test["Black ENTER button (public 0) pressed on ARMS: arms coil energized"]["active_solenoid_addresses"])
		observations = load(EVIDENCE_PATH)["runtime"]["observations"]
		self.assertEqual(set(range(1, 81)), set(observations["lamp_addresses_seen"]))
		self.assertFalse(set(observations["solenoid_addresses_seen"]) & ({16, 49, 50} | set(range(33, 45))))

	def test_service_test_frames_back_the_names(self) -> None:
		snapshots = {item["label"]: item for item in load(EVIDENCE_PATH)["runtime"]["observations"]["diagnostic_snapshots"]}
		pins = load(FRAME_READINGS_PATH)["runs"]
		for run, readings in pins.items():
			for label, pin in readings.items():
				snapshot = snapshots[f"{run} snapshot: {label}"]
				self.assertEqual((pin["pixel_sha256"], pin["reading"]), (snapshot["pixel_sha256"], snapshot["interpreted_text"]), label)
		dedicated = pins["elvis-dedicated-switch-test"]
		self.assertIn("#5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK", dedicated["dedicated input 88 (DS-5) (public 88) held in the Dedicated Switch Test"]["reading"])
		for label in ("right flipper end-of-stroke (public 81) held in the Dedicated Switch Test", "left flipper end-of-stroke (public 83) held in the Dedicated Switch Test"):
			self.assertIn("NONE", dedicated[label]["reading"], label)
		switches = pins["elvis-switch-test"]
		for address in (3, 64):
			self.assertEqual("SWITCH TEST / NONE", switches[f"switch {address} closed in the Switch Test"]["reading"], address)
		self.assertIn("HOUND DOG", pins["elvis-switch-timing-probe"]["switch 64 open, 0.50 s after its release"]["reading"])
		self.assertIn("ELVIS COMPLETED", pins["elvis-single-lamp-test"]["Black ENTER button (public 0) pressed on +: lamp step 15"]["reading"])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained harness runs are not available")
	def test_frame_readings_refuse_a_substituted_frame(self) -> None:
		root = evidence_tool.review_artifacts_root(required=True)
		original = evidence_tool._load_run

		def swapped(*args):
			run, listed = original(*args)
			if args[1] == "elvis-dedicated-switch-test":
				labels = [item["label"] for item in run["snapshots"]]
				held = labels.index("dedicated input 88 (DS-5) (public 88) held in the Dedicated Switch Test")
				run["snapshots"][held]["displays"] = run["snapshots"][labels.index("left flipper button (public 84) held in the Dedicated Switch Test")]["displays"]
			return run, listed

		with mock.patch.object(evidence_tool, "_load_run", swapped):
			with self.assertRaisesRegex(RuntimeError, "does not carry the frame the curator read"):
				evidence_tool.build(root)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		self.assertEqual(canonical_bytes(evidence_tool.build(root)), EVIDENCE_PATH.read_bytes())

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_raw_timings_behind_the_notes(self) -> None:
		run = raw_run("elvis-gameplay")
		start = edges(run, "switch", 54, True)[0]
		self.assertAlmostEqual(1.1, edges(run, "solenoid", 1, True)[0] - start, delta=0.1)
		fifth = edges(run, "switch", 21, True)[0]
		resets = [time - fifth for time in edges(run, "solenoid", 3, True) if fifth <= time < fifth + 3]
		self.assertEqual(3, len(resets))
		for actual, expected in zip(resets, (0.33, 0.74, 1.14)):
			self.assertAlmostEqual(expected, actual, delta=0.05)
		saucer = edges(run, "switch", 34, True)[0]
		kicks = [time for time in edges(run, "solenoid", 6, True) if saucer <= time < edges(run, "switch", 34, False)[0]]
		self.assertEqual(3, len(kicks))
		self.assertAlmostEqual(4.3, kicks[0] - saucer, delta=0.1)
		self.assertTrue(all(0.6 <= later - earlier <= 0.8 for earlier, later in zip(kicks, kicks[1:])))
		top = edges(run, "switch", 32, True)[0]
		top_kicks = [time for time in edges(run, "solenoid", 12, True) if top <= time < edges(run, "switch", 32, False)[0]]
		self.assertEqual(1, len(top_kicks))
		self.assertAlmostEqual(5.7, top_kicks[0] - top, delta=0.1)
		served, left = edges(run, "switch", 16, True)[0], edges(run, "switch", 16, False)[0]
		self.assertGreaterEqual(left - served, 6.0)
		self.assertEqual([], [time for time in edges(run, "solenoid", 2, True) if served <= time <= left])
		self.assertAlmostEqual(0.6, next(time for time in edges(run, "gi", 0, True) if time > served) - served, delta=0.1)
		post, released = edges(run, "switch", 48, True)[0], edges(run, "switch", 48, False)[0]
		self.assertEqual([], [time for time in edges(run, "solenoid", 7, True) if post <= time <= released])
		press = edges(run, "switch", 82, True)[-1]
		self.assertAlmostEqual(0.17, next(time for time in edges(run, "solenoid", 2, True) if time > press) - press, delta=0.03)
		probe = raw_run("elvis-hound-dog-probe")
		door = edges(probe, "switch", 63, True)[0]
		self.assertAlmostEqual(0.13, next(time for time in edges(probe, "solenoid", 19, True) if time > door) - door, delta=0.03)
		for rise, fall in zip(edges(probe, "switch", 64, True), edges(probe, "switch", 64, False)):
			off = next(time for time in edges(probe, "solenoid", 19, False) if time > rise)
			self.assertTrue(2.0 <= off - rise <= 2.55, off - rise)
			on = next(time for time in edges(probe, "solenoid", 19, True) if time > fall)
			self.assertAlmostEqual(0.065, on - fall, delta=0.01)
		stacking = raw_run("elvis-stacking-opto")
		for rise in edges(stacking, "switch", 15, True):
			window = [time for time in edges(stacking, "solenoid", 1, True) if rise <= time < rise + 8]
			self.assertEqual(6, len(window))
			self.assertAlmostEqual(1.1, window[0] - rise, delta=0.1)
			self.assertTrue(all(0.75 <= later - earlier <= 0.95 for earlier, later in zip(window, window[1:])))
			self.assertEqual(1, len([time for time in edges(stacking, "solenoid", 2, True) if window[-1] < time < rise + 10]))

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_extraction_script_and_seed_match(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		curator.verify_extraction_manifest(root)
		table = root / "stern/elvis-2004" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, sha256(table))
		extraction = root / curator.EXTRACTION_RELATIVE_PATH
		script = extraction / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, sha256(script))
		built = seed_tool.canonical(seed_tool.build(extraction, table))
		self.assertEqual(built.encode("utf-8"), SEED_PATH.read_bytes())
		code = "\n".join(line for line in script.read_text(encoding="latin-1").splitlines() if not line.strip().startswith("'"))
		self.assertIn('Const cGameName = "elvis"', code)
		self.assertIn("vpmNudge.TiltSwitch = 56", code)
		self.assertIn(".InitSw 0, 14, 13, 12, 11, 0, 0, 0", code)
		self.assertIn(".Sol1 = 25", code)
		self.assertIn(".AddSw 33, 0, 0", code)
		# 15 is written only by the PulseSw in SolTrough, 64 only by its PulseSw, and 81, 83 and 88 never.
		def writes(address: int) -> list[str]:
			return re.findall(rf"PulseSw\s*\(?\s*{address}\b|Switch\(\s*{address}\s*\)", code, re.IGNORECASE)
		self.assertEqual(1, len(writes(15)))
		self.assertEqual(["PulseSw 64"], writes(64))
		for address in (81, 83, 88):
			self.assertEqual([], writes(address), address)
		self.assertEqual(2, len(writes(55)))
		self.assertIsNone(re.search(r"\b(Dim|Const|Public|Private)\b[^\n]*\bkeyUpperLeft\b|\bkeyUpperLeft\s*=", code, re.IGNORECASE))
		self.assertIsNone(re.search(r"SolCallback\(\s*(13|14)\s*\)", code, re.IGNORECASE))
		names = {path.stem.split(".", 1)[-1].casefold() for path in (extraction / "gameitems").glob("*.json")}
		self.assertNotIn("sw10", names)
		self.assertTrue({"sw9", "sw64", "sw63", "pstand", "ballrelease"} <= names)
		# A G.I. or flasher placement sits only on a Light that draws its bulb mesh; the rest sit on no bulb.
		def light(name: str) -> dict:
			return json.loads((extraction / "gameitems" / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]
		seed = load(SEED_PATH)
		for entry in seed["gi"]["0"]:
			self.assertTrue(light(entry["object"])["is_bulb_light"] and light(entry["object"])["show_bulb_mesh"], entry["object"])
		for name in seed["gi_without_bulb"]["0"] + ["f23", "f23a"]:
			self.assertFalse(light(name)["show_bulb_mesh"], name)

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_manual_and_ipdb_capture_match_their_pins(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine"
		self.assertEqual(curator.MANUAL_SHA256, sha256(root / "stern.elvis-2004" / curator.MANUAL_NAME))
		archive = root / MACHINE_ID / "ipdb-archive"
		self.assertEqual(curator.IPDB_PAGE_SHA256, sha256(archive / "ipdb-4983-20261016065404.html"))
		self.assertEqual(curator.IPDB_CAPTURE_GZIP_SHA256, sha256(archive / "ipdb-4983-20261016065404.html.gz"))

	def test_the_user_authorized_rom_archive_matches_the_pinned_set(self) -> None:
		value = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
		if not value:
			self.skipTest("user-authorized ROM library root is not configured")
		archive = Path(value) / "elvis.zip"
		self.assertEqual(curator.ROM_ARCHIVE_SHA256, sha256(archive))
		with zipfile.ZipFile(archive) as bundle:
			members = {info.filename: f"{info.CRC:08x}" for info in bundle.infolist()}
		self.assertTrue(set(ROM_MEMBERS.items()) <= set(members.items()), members)


if __name__ == "__main__":
	unittest.main()
