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

import curate_harley_davidson as stern  # noqa: E402
import curate_harley_davidson_sega as curator  # noqa: E402
import harley_davidson_runtime_evidence as stern_evidence_tool  # noqa: E402
import harley_davidson_sega_runtime_evidence as evidence_tool  # noqa: E402

MACHINE_ID = "sega.harley-davidson.1999"
DEFINITION_PATH = ROOT / "machines" / "partial" / "sega" / "harley-davidson-1999.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "sega" / "harley-davidson-1999.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "sega" / "harley-davidson-1999.md"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "harley-davidson-harl-a13-service-tests-and-gameplay.json"
FRAME_READINGS_PATH = ROOT / "tools" / "seeds" / "sega" / "harley-davidson-1999-frame-readings.json"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / MACHINE_ID

DRIVER_IDS = {"harl_a10", "harl_a13", "harl_f13", "harl_g13", "harl_i13", "harl_l13", "harl_u13"}
NOT_USED_LAMPS = {52, 53, 54, 55, 56, 60, 61, 62, 63, 64} | set(range(73, 81))
UNRESOLVED_LAMPS = {52, 53, 54}
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
# The committed text names the Stern sets it compares against: the retained table's ROM, the Stern scenarios this
# record's runs repeat, and the one set MACHINE_INIT(se) gives the fast-flip byte.
STERN_DRIVERS = {"harl_a30", "harl_a40"}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def steps(run: str) -> dict[str, dict]:
	prefix = f"{run} "
	return {item["label"].split(": ", 1)[1].split(";")[0]: item for item in load(EVIDENCE_PATH)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith(prefix)}


def raw_run(name: str) -> dict:
	return load(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / name / "run.json")


def rises(run: dict, kind: str, number: int) -> list[float]:
	return [event["time_s"] for event in run["events"] if event["event"] == kind and event["number"] == number and event["state"] and not event.get("initial")]


class HarleyDavidsonSegaTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.stern = load(stern.PARTIAL_PATH)
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}
		cls.snapshots = {item["label"]: item for item in load(EVIDENCE_PATH)["runtime"]["observations"]["diagnostic_snapshots"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, "Sega", 4453, "G56lO-Mx00O", 1999, "67"), (machine["id"], machine["manufacturer"], machine["ipdb_id"], machine["opdb_id"], machine["year"], machine["model_number"]))
		self.assertEqual(dict.fromkeys(DRIVER_IDS, "identical"), {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]})
		self.assertEqual({driver_id: "harl_a13" for driver_id in DRIVER_IDS - {"harl_a13"}}, {driver["id"]: driver["clone_of"] for driver in self.definition["drivers"] if "clone_of" in driver})
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["output_semantics", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])
		catalog = load(ROOT / "catalog/pinmame.json")
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID})
		# Only the root set was booted; the notes say so.
		notes = {driver["id"]: driver["variant_notes"] for driver in self.definition["drivers"]}
		self.assertIn("13 harness runs booted it.", notes["harl_a13"])
		for driver_id in DRIVER_IDS - {"harl_a13"}:
			self.assertTrue(notes[driver_id].endswith("No harness run booted it."), driver_id)

	def test_construction_comes_over_unchanged_from_the_stern_record(self) -> None:
		def construction(definition: dict) -> dict:
			return {
				item["id"]: {key: item.get(key) for key in ("binding", "kind", "label", "normally_closed", "initial_active", "wiring", "spatial")}
				for item in definition["inputs"] + definition["outputs"]
			}
		self.assertEqual(construction(self.stern), construction(self.definition))
		without_provenance = lambda definition: [{key: value for key, value in display.items() if key != "provenance"} for display in definition["displays"]]  # noqa: E731
		self.assertEqual(without_provenance(self.stern), without_provenance(self.definition))
		availability = {item["id"]: item["availability"] for item in self.definition["inputs"] + self.definition["outputs"]}
		stern_availability = {item["id"]: item["availability"] for item in self.stern["inputs"] + self.stern["outputs"]}
		self.assertEqual({"virtual.15-fast-flip-game-on": ("used", "unused")}, {key: (stern_availability[key], value) for key, value in availability.items() if stern_availability[key] != value})
		shape = lambda definition: [(item["id"], item["kind"], item["actuators"], item["sensors"]) for item in definition["mechanisms"]]  # noqa: E731
		self.assertEqual(shape(self.stern), shape(self.definition))
		for key in ("controller", "relationships"):
			self.assertEqual(self.stern[key], self.definition[key], key)

	def test_no_sega_set_publishes_the_game_on_state(self) -> None:
		fast_flip = self.device("output.solenoid", 15)
		self.assertEqual(("virtual", "unused"), (fast_flip["kind"], fast_flip["availability"]))
		self.assertIn("sets none for the seven Sega sets", fast_flip["physical"]["notes"])
		observations = load(EVIDENCE_PATH)["runtime"]["observations"]
		self.assertNotIn(15, observations["solenoid_addresses_seen"])
		gameplay = steps("harl-a13-gameplay")
		self.assertNotIn(15, gameplay["the served ball rests on the shooter lane switch 16"]["active_solenoid_addresses"])
		self.assertEqual({47, 48}, set(gameplay["left flipper button (public 84) held 1.5 s"]["active_solenoid_addresses"]))

	def test_no_note_describes_the_stern_runs(self) -> None:
		for item in self.definition["inputs"] + self.definition["outputs"]:
			if item["id"] != "virtual.15-fast-flip-game-on":
				self.assertIsNone(curator.STERN_RUNTIME_WORDS.search(item["physical"].get("notes", "")), item["id"])
		for mechanism in self.definition["mechanisms"]:
			self.assertIsNone(curator.STERN_RUNTIME_WORDS.search(mechanism["behavior"]), mechanism["id"])
		cited = {ref for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"] for ref in item["provenance"]["source_refs"]}
		self.assertFalse(cited & {stern.RUNTIME_SOURCE, stern.RUNTIME_A30_SOURCE, stern.ROM_SOURCE, stern.ROM_A30_SOURCE})
		self.assertNotIn("harl_a40", KNOWLEDGE_PATH.read_text(encoding="utf-8").replace("harl_a40 scenarios", ""))

	def test_every_frame_reading_is_pinned_to_the_evidence(self) -> None:
		pins = load(FRAME_READINGS_PATH)["runs"]
		self.assertTrue(set(pins) <= set(evidence_tool.RUNS))
		pinned = {f"{run} snapshot: {label}": pin for run, labels in pins.items() for label, pin in labels.items()}
		self.assertEqual(set(pinned), set(self.snapshots))
		for label, pin in pinned.items():
			self.assertEqual((pin["pixel_sha256"], pin["reading"]), (self.snapshots[label]["pixel_sha256"], self.snapshots[label]["interpreted_text"]), label)
		self.assertEqual(59 + 5, len(pins["harl-a13-switch-test"]) + len(pins["harl-a13-switch-test-41-45"]))
		self.assertEqual(82, len(pins["harl-a13-single-lamp-test"]))
		self.assertEqual(33, len(pins["harl-a13-single-coil-test"]))
		self.assertEqual(FRAME_READINGS_PATH.read_bytes(), FRAME_READINGS_PATH.read_bytes().replace(b"\r", b""))

	def test_service_tests_name_every_switch_lamp_and_coil_as_the_manual_does(self) -> None:
		evidence = load(EVIDENCE_PATH)
		switches = curator.switch_test_readings(evidence)
		lamps = curator.lamp_test_readings(evidence)
		coils = curator.coil_test_readings(evidence)
		self.assertEqual((set(range(1, 65)), set(range(1, 81)), set(range(1, 33))), (set(switches), set(lamps), set(coils)))
		self.assertEqual({address for address in range(1, 65) if switches[address][0] == "NOT USED"}, set(stern.UNUSED_SWITCHES))
		self.assertEqual({address for address in range(1, 81) if lamps[address][0] == "NOT USED"}, NOT_USED_LAMPS)
		# The differences the curator allows are spellings only: each is listed, and nothing else differs.
		self.assertEqual((4, 16, 1), (len(curator.SWITCH_WORDING), len(curator.LAMP_WORDING), len(curator.COIL_WORDING)))
		self.assertEqual(("RIDE AGAIN #2", "YEL-BLU RED-WHT #70"), lamps[70])
		self.assertEqual(("#F7 FLASH: RIGHT DROP TARGET x2", "ORG BLK-VIO"), coils[31])
		for address, (name, wires) in switches.items():
			self.assertIn(f'Portals Switch Test prints "{name} / {wires}"', self.device("input.switch", address)["physical"]["notes"], address)
		for address, (name, wires) in lamps.items():
			self.assertIn(f'Single Lamp Test prints "{name} / {wires}"', self.device("output.lamp", address)["physical"]["notes"], address)
		for number, (name, wires) in coils.items():
			public = {15: 48, 16: 46}.get(number, number)
			self.assertIn(f'Single Coil Test prints "{name} / {wires}" for Q{number}', self.device("output.solenoid", public)["physical"]["notes"], number)

	def test_the_name_check_refuses_an_unlisted_difference(self) -> None:
		evidence = load(EVIDENCE_PATH)
		with mock.patch.dict(curator.LAMP_WORDING, clear=False):
			del curator.LAMP_WORDING[70]
			with self.assertRaisesRegex(RuntimeError, "lamp 70: the ROM prints 'RIDE AGAIN #2'"):
				curator.lamp_test_readings(evidence)
		with mock.patch.dict(curator.SWITCH_WORDING, {37: ("OPTO", "OPTO")}):
			with self.assertRaisesRegex(RuntimeError, "switch 37"):
				curator.switch_test_readings(evidence)
		# Both sides of an allowed difference are pinned: a changed manual transcription is refused, listed or not.
		for address in (70, 1):
			with mock.patch.dict(stern.LAMPS, {address: ("Left Outlane", "LEFT OUTLANE", "#555 Bulb")}):
				with self.assertRaisesRegex(RuntimeError, f"lamp {address}: "):
					curator.lamp_test_readings(evidence)
		with mock.patch.dict(stern.Q_OUTPUTS, {31: ("Left Slingshot", "LEFT SLINGSHOT", *stern.Q_OUTPUTS[31][2:])}):
			with self.assertRaisesRegex(RuntimeError, "coil 31: "):
				curator.coil_test_readings(evidence)

	def test_single_coil_test_fires_each_public_address(self) -> None:
		coil = steps("harl-a13-single-coil-test")
		fired = {int(re.search(r"coil step (\d+) fired", label).group(1)): item["transitioned_solenoid_addresses"] for label, item in coil.items() if re.search(r"RUN: coil step \d+ fired$", label)}
		self.assertEqual({number: {15: [47, 48], 16: [45, 46]}.get(number, [number]) for number in range(1, 33)}, {number: value for number, value in fired.items() if number <= 32})
		self.assertIn(5, load(EVIDENCE_PATH)["runtime"]["observations"]["solenoid_addresses_seen"])

	def test_lamps_outside_the_single_lamp_test(self) -> None:
		observations = load(EVIDENCE_PATH)["runtime"]["observations"]
		outside = set(observations["lamp_addresses_driven_outside_self_test"])
		self.assertEqual(set(range(1, 81)), set(observations["lamp_addresses_seen"]))
		self.assertTrue(UNRESOLVED_LAMPS | {69} <= outside)
		self.assertFalse(outside & ((NOT_USED_LAMPS - UNRESOLVED_LAMPS) | {47}))
		for address in UNRESOLVED_LAMPS:
			lamp = self.device("output.lamp", address)
			self.assertEqual(("unknown", "candidate"), (lamp["availability"], lamp["provenance"]["status"]), address)
			self.assertIn("Resolution path:", lamp["physical"]["notes"])
			self.assertIn("names 52 to 56 NOT USED", lamp["physical"]["notes"])
		self.assertIn(curator.README_SOURCE, self.device("output.lamp", 69)["provenance"]["source_refs"])

	def test_gameplay_steps_support_the_switch_to_coil_claims(self) -> None:
		observed = steps("harl-a13-gameplay")
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
			"coin 1 on the center coin slot (public 5)": {24, 27}, "right flipper button (public 82) held 1.5 s": {45, 46},
		}
		for label, coils in expected.items():
			self.assertTrue(coils <= set(observed[label]["active_solenoid_addresses"]), label)
		for address in (29, 30, 31, 32):
			label = next(key for key in observed if f"(public {address}) closed once" in key)
			self.assertEqual([13, 30], observed[label]["active_solenoid_addresses"], address)
		for address in (17, 18, 19):
			self.assertEqual([], observed[f"left 4-bank drop target (public {address}) knocked down and left down"]["active_solenoid_addresses"], address)
		# The left orbit drew no coil; the super-VUK flashers lit by the stand-up target before it went dark and lit again.
		self.assertFalse(set(observed["left orbit (public 33) closed once"]["active_solenoid_addresses"]) - {30})
		self.assertEqual([], observed["behind top VUK (metal under-trough) (public 48) closed once"]["active_solenoid_addresses"])
		self.assertIn(23, observed["right cabinet button (public 8, the USA up/down post button) held 1.5 s"]["active_solenoid_addresses"])
		self.assertIn(3, observed["a ball enters the super VUK (public 45) and stays"]["active_solenoid_addresses"])
		self.assertNotIn(4, observed["a ball enters the power scoop (public 46) and stays"]["active_solenoid_addresses"])
		trough = observed["a ball reaches the bottom of the motorcycle kick-out trough (public 44) and stays"]
		self.assertEqual(([1, 13, 29, 30], [1, 13, 19, 29, 30]), (trough["active_solenoid_addresses"], trough["transitioned_solenoid_addresses"]))
		launch = steps("harl-a13-launch-scoop-opto")
		self.assertEqual([4, 20], launch["a ball enters the power scoop (public 46) and stays, with no other switch closed"]["active_solenoid_addresses"])
		self.assertEqual([], launch["Launch button (public 53) pressed once with the ball still on the shooter lane switch 16"]["active_solenoid_addresses"])

	def test_ds5_probe_and_dedicated_switch_test(self) -> None:
		probe = steps("harl-a13-ds5-probe")
		holds = [label for label in probe if label.startswith("dedicated input 88 (DS-5) held 1.5 s")]
		self.assertEqual(4, len(holds))
		for label in holds:
			self.assertEqual([], probe[label]["active_solenoid_addresses"], label)
		self.assertEqual([23], probe["right cabinet button (public 8, the USA up/down post button) held 1.5 s as the control"]["active_solenoid_addresses"])
		held = self.snapshots["harl-a13-dedicated-switch-test snapshot: dedicated input 88 (DS-5) held in the Dedicated Switch Test"]["interpreted_text"]
		self.assertEqual("DEDICATED SWITCH TEST / #5 NOT USED / CN6-7 GRY-GRN CN6-1 BLK / PRESS START TO EXIT TEST", held)
		self.assertIn("harl_a13's Portals Dedicated Switch Test", self.device("input.switch", 88)["physical"]["notes"])

	def test_motorcycle_runs_support_the_lift_claims(self) -> None:
		self.assertEqual([19], steps("harl-a13-motorcycle-home-search")["wait for the motor relay with neither motorcycle position switch closed"]["active_solenoid_addresses"])
		self.assertEqual([19], steps("harl-a13-motorcycle-up-at-boot")["wait for the motor relay with the Motor Up switch 35 closed"]["active_solenoid_addresses"])
		self.assertTrue(all(item["active_solenoid_addresses"] == [] for item in steps("harl-a13-motorcycle-down-at-boot").values()))
		lift = steps("harl-a13-motorcycle-ball-start-lift")
		self.assertIn(19, lift["the served ball reaches the shooter lane switch 16"]["active_solenoid_addresses"])
		self.assertIn(19, lift["the motorcycle reaches the up position: public 35 raised to 1"]["transitioned_solenoid_addresses"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = {ref for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"] for ref in item["provenance"]["source_refs"]}
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		# The machine identity, the -15 plate bulletin and the files that only pin other sources are read by the knowledge note.
		self.assertEqual({stern.CATALOG_SOURCE, stern.VPX_EXTRACTION_SOURCE, curator.ROM_SOURCE, curator.IDENTITY_SOURCE, curator.BULLETIN_SOURCES[121]}, declared - cited)
		own = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], sha256(ROOT / excerpt["path"]), excerpt["id"])
				self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])
				if excerpt["path"].startswith(f"evidence/excerpts/{MACHINE_ID}/"):
					own.add(Path(excerpt["path"]).name)
		self.assertEqual({path.name for path in EXCERPT_DIRECTORY.iterdir()}, own)
		for number in curator.BULLETINS:
			source = next(item for item in self.definition["sources"] if item["id"] == curator.BULLETIN_SOURCES[number])
			self.assertNotIn("@", source["locator"])

	def test_committed_text_names_no_other_machine(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID and len(driver["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		words = set(re.findall(r"[a-z0-9_]{5,}", "\n".join(texts)))
		# Relay 19's "white diamond" is the coil location drawing's marker shape, not a reference to the driver of that name.
		self.assertEqual(set(), words & foreign - STERN_DRIVERS - {"diamond"})

	def test_the_curators_reproduce_every_artifact(self) -> None:
		curator.check(ROOT)
		stern.check(ROOT)

	def test_scenarios_name_only_their_game_and_evidence_pins_its_runs(self) -> None:
		document = load(EVIDENCE_PATH)
		self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
		self.assertEqual(curator.ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"])
		self.assertEqual(evidence_tool.ROM_ARCHIVE_SHA256, curator.ROM_ARCHIVE_SHA256)
		self.assertEqual(([MACHINE_ID], ["harl_a13"]), (document["machine_ids"], document["driver_ids"]))
		self.assertEqual(list(evidence_tool.RUNS), [run["name"] for run in document["runtime"]["raw_runs"]])
		for run in document["runtime"]["raw_runs"]:
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(run["scenario_sha256"], sha256(scenario), run["name"])
			self.assertEqual("harl_a13", load(scenario)["game"])
			self.assertNotIn(b"\r", scenario.read_bytes(), run["name"])
		# Nine runs repeat the Stern record's scenarios step for step.
		for name in ("motorcycle-home-search", "motorcycle-up-at-boot", "motorcycle-down-at-boot", "motorcycle-ball-start-lift", "stacking-opto", "gameplay", "launch-scoop-opto", "ds5-probe", "dedicated-switch-test"):
			sega = load(ROOT / stern_evidence_tool.SCENARIO_DIRECTORY / f"harl-a13-{name}.json")
			original = load(ROOT / stern_evidence_tool.SCENARIO_DIRECTORY / f"harl-a40-{name}.json")
			self.assertEqual({key: value for key, value in original.items() if key not in {"game", "notes"}}, {key: value for key, value in sega.items() if key not in {"game", "notes"}}, name)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		self.assertEqual(canonical_bytes(evidence_tool.build(root)), EVIDENCE_PATH.read_bytes())

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained harness runs are not available")
	def test_frame_readings_refuse_a_substituted_frame(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		original = stern_evidence_tool._load_run

		def swapped(*args):
			run, listed = original(*args)
			if args[1] == "harl-a13-single-lamp-test":
				labels = [item["label"] for item in run["snapshots"]]
				target = labels.index("Black ENTER button (public 0) pressed on +: lamp step 52")
				run["snapshots"][target]["displays"] = run["snapshots"][labels.index("Black ENTER button (public 0) pressed on +: lamp step 51")]["displays"]
			return run, listed

		with mock.patch.object(stern_evidence_tool, "_load_run", swapped):
			with self.assertRaisesRegex(RuntimeError, "does not carry the frame the curator read"):
				evidence_tool.build(root)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_raw_runs_behind_the_rewritten_notes(self) -> None:
		gameplay = raw_run("harl-a13-gameplay")
		ball = rises(gameplay, "switch", 16)[0]
		for address in UNRESOLVED_LAMPS:
			lit = rises(gameplay, "lamp", address)
			self.assertTrue(lit and min(lit) > ball, address)
		for address in (55, 56):
			self.assertEqual([], rises(gameplay, "lamp", address), address)
		# The headlight blinks in attract mode from about 9.3 s after power-up in every run but the lamp walk.
		for name in evidence_tool.RUNS:
			if name != evidence_tool.LAMP_TEST_RUN:
				lit = rises(raw_run(name), "lamp", 69)
				self.assertTrue(lit, name)
				self.assertAlmostEqual(9.3, min(lit), delta=0.2, msg=name)
		# The scoop kick after the scenario emptied it came 2.96 s later and 40 ms before the next 37 pulse.
		released = [event["time_s"] for event in gameplay["events"] if event["event"] == "switch" and event["number"] == 46 and not event["state"] and not event.get("initial")]
		kick = next(time for time in rises(gameplay, "solenoid", 4) if time > released[0])
		self.assertAlmostEqual(2.96, kick - released[0], delta=0.02)
		self.assertAlmostEqual(0.04, next(time for time in rises(gameplay, "switch", 37) if time > kick) - kick, delta=0.02)

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_bulletins_and_readme_match_their_pins(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / MACHINE_ID
		for number, (_date, digest, *_rest) in curator.BULLETINS.items():
			self.assertEqual(digest, sha256(root / "archive-org" / f"sb{number}.pdf"), number)
		self.assertEqual(curator.README_SHA256, sha256(root / "stern-site-wayback" / "hdROMreadme-20060512000521.txt"))
		ipdb = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / stern.MACHINE_ID / "ipdb"
		self.assertIn(stern.IPDB_PAGE_SHA256S[4453], {sha256(path) for path in ipdb.iterdir() if path.is_file()})


if __name__ == "__main__":
	unittest.main()
