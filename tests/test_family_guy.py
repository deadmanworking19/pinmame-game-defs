"""Fail-closed tests for the Stern Family Guy (2007) definition.

The load-bearing assertions are the ones that survive every schema check but would not survive a
wrong derivation: the public-address contract the ROM's own service tests prove, the matrix
polarity rule, the manual-derived mini-playfield LED mapping, the firmware-version differences, and
the Evil Monkey probes that keep the latch gate's behavior open.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "family-guy-2007.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "family-guy-2007.md"
RUNTIME_ROOT = ROOT / "evidence" / "runtime" / "sam"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "stern.family-guy.2007"
MACHINE_ID = "stern.family-guy.2007"
CALLOUTS = ROOT / "tools" / "seeds" / "stern" / "family-guy-2007-callouts.json"
SPATIAL_SEED = ROOT / "tools" / "seeds" / "stern" / "family-guy-2007-spatial.json"
AUDIT = ROOT / "reports" / "spatial" / "stern" / "family-guy-2007.json"
CALLOUT_SOURCE = "review.family-guy-drawing-callouts-2026-10-02"
PINNED_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
FIRMWARE_WITH_AUX_COILS = {"fg_300ai", "fg_400a", "fg_800al", "fg_1100al"}
SWEEP_DRIVERS = ["fg_1200ag", "fg_300ai", "fg_400a", "fg_800al", "fg_1100al"]

USED_MATRIX_SWITCHES = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 57, 64}
OPTO_SWITCHES = {9, 21, 22, 44, 45, 46, 47, 52, 53, 54, 55}
USED_LAMPS = set(range(1, 59)) | set(range(61, 71))
UNUSED_LAMPS = {59, 60} | set(range(71, 81))
LED_LAMPS = {81, 82, 83, 84, 89, 90, 91, 92, 97, 98, 99, 100, 105, 106, 107, 108, 114, 121, 122, 123, 124, 125}
FLIPPER_COLUMN = {81: "RIGHT FLIPPER E.O.S.", 82: "RIGHT FLIPPER E.O.S.", 83: "LEFT FLIPPER E.O.S.", 84: "LEFT FLIPPER E.O.S."}
LED_NAMES = {
	"Brian": {"B": 84, "R": 83, "I": 82, "A": 81, "N": 97},
	"Chris": {"C": 125, "H": 124, "R": 123, "I": 122, "S": 121},
	"Lois": {"L": 108, "O": 107, "I": 106, "S": 105},
	"Meg": {"M": 98, "E": 99, "G": 100},
}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def by_binding(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def read_pgm(path: Path) -> list[bytes]:
	"""Return the rows of a binary PGM."""
	data = path.read_bytes()
	tokens: list[bytes] = []
	index = 0
	while len(tokens) < 4:
		while data[index:index + 1].isspace():
			index += 1
		start = index
		while not data[index:index + 1].isspace():
			index += 1
		tokens.append(data[start:index])
	index += 1
	width, height = int(tokens[1]), int(tokens[2])
	return [data[index + row * width:index + (row + 1) * width] for row in range(height)]


class FamilyGuyDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		cls.catalog = load_json(ROOT / "catalog" / "pinmame.json")
		cls.inputs = by_binding(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = by_binding(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = by_binding(cls.definition, "outputs", "pinmame.output.lamp")

	def test_identity_coverage_and_regeneration(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, 5219, 2007, "G5LW9-MQ6N5"), (machine["id"], machine["ipdb_id"], machine["year"], machine["opdb_id"]))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["mechanism_behavior", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual({"platform": "pinmame.sam", "inversion_applied_by_emulator": True}, self.definition["controller"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "stubs" / "fg_1200ag.json").exists())
		import curate_family_guy

		self.assertEqual(self.definition, json.loads(json.dumps(curate_family_guy.build())))
		self.assertEqual(self.knowledge, curate_family_guy.knowledge_text(self.definition))

	def test_driver_family_is_exhaustive_and_firmware_only(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		catalog_drivers = {driver["id"] for driver in self.catalog["drivers"] if driver["id"].startswith("fg_")}
		self.assertEqual(catalog_drivers, set(drivers))
		self.assertEqual(19, len(drivers))
		self.assertEqual({MACHINE_ID}, {driver["machine_id"] for driver in self.catalog["drivers"] if driver["id"] in drivers})
		self.assertEqual({"fg_1200ag"}, {driver_id for driver_id, driver in drivers.items() if "clone_of" not in driver})
		for driver in drivers.values():
			self.assertEqual("identical", driver["physical_compatibility"])
			self.assertNotIn("display_overrides", driver)
		self.assertIn("No ROM for this driver is retained", drivers["fg_200a"]["variant_notes"])
		self.assertIn("different dump", drivers["fg_1200af"]["variant_notes"])
		# Every ROM that was swept says so; none of the others does.
		swept = {driver_id for driver_id, driver in drivers.items() if "exercised in the retained harness sweeps" in driver["variant_notes"]}
		self.assertEqual(set(SWEEP_DRIVERS), swept)

	def test_input_spaces_and_used_set(self) -> None:
		self.assertEqual(set(range(1, 65)) | {65, 66, 67, 68, 69, 70, 71, 72} | set(range(81, 89)) | set(range(-7, 1)), set(self.inputs))
		self.assertEqual(set(range(1, 9)), set(by_binding(self.definition, "inputs", "pinmame.input.dip")))
		used = {number for number in range(1, 65) if self.inputs[number]["availability"] == "used"}
		self.assertEqual(USED_MATRIX_SWITCHES, used)
		for number in range(1, 65):
			device = self.inputs[number]
			self.assertFalse(device["normally_closed"], number)
			self.assertEqual("opto" if number in OPTO_SWITCHES else device["physical"]["switch_type"], device["physical"]["switch_type"], number)
		for number in OPTO_SWITCHES:
			self.assertEqual("opto", self.inputs[number]["physical"]["switch_type"])
		self.assertEqual({"ball.position"}, {role for number in (18, 19, 20, 21, 22) for role in self.inputs[number]["roles"]})
		self.assertEqual({18, 19, 20, 21, 55}, {number for number in range(1, 65) if self.inputs[number].get("initial_active")})
		self.assertEqual("Start button", self.inputs[16]["label"])
		self.assertEqual("Tournament Start", self.inputs[15]["label"])

	def test_dedicated_switches_follow_the_manual_and_the_flipper_column(self) -> None:
		labels = {device: self.inputs[device]["label"] for device in (65, 66, 67, 84, 83, 82, 81, 88, -7, -6, -5, -3, -2, -1, 0)}
		self.assertEqual("Left coin slot", labels[65])
		self.assertEqual("Left flipper button", labels[84])
		self.assertEqual("Left flipper end-of-stroke", labels[83])
		self.assertEqual("Right flipper end-of-stroke", labels[81])
		self.assertEqual("Upper left flipper button", labels[88])
		self.assertTrue(self.inputs[83]["normally_closed"])
		self.assertTrue(self.inputs[81]["normally_closed"])
		self.assertIn("rests at 0", self.inputs[83]["physical"]["notes"])
		self.assertFalse(self.inputs[-6]["normally_closed"])
		self.assertFalse(self.inputs[-7]["normally_closed"])
		self.assertEqual("optional", self.inputs[-6]["availability"])
		self.assertEqual("unused", self.inputs[86]["availability"])
		self.assertEqual("unused", self.inputs[87]["availability"])
		self.assertEqual("unused", self.inputs[85]["availability"])
		self.assertIn("L. POST SAVE", self.inputs[71]["physical"]["notes"])
		self.assertEqual("unused", self.inputs[71]["availability"])
		self.assertEqual(["flipper.upper.left.button"], self.inputs[88]["roles"])
		self.assertEqual({-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter"}, {device: self.inputs[device]["roles"][0] for device in (-3, -2, -1, 0)})

	def test_solenoid_space_matches_the_coil_test(self) -> None:
		coils = {number for number in self.solenoids if 1 <= number <= 32}
		self.assertEqual(set(range(1, 33)), coils)
		self.assertEqual({"used"}, {self.solenoids[number]["availability"] for number in range(1, 33) if number != 24})
		self.assertEqual("optional", self.solenoids[24]["availability"])
		self.assertEqual("motor", self.solenoids[20]["kind"])
		self.assertEqual({23, 25, 26, 27, 28, 29, 30, 31, 32}, {number for number in coils if self.solenoids[number]["kind"] == "flasher"})
		self.assertEqual("virtual", self.solenoids[33]["kind"])
		self.assertEqual(set(range(51, 67)), {number for number, device in self.solenoids.items() if number >= 51})
		self.assertEqual({"unused"}, {self.solenoids[number]["availability"] for number in range(51, 67)})
		self.assertEqual(33 + 16, len(self.solenoids))
		# Manual labels, with the pop bumpers paired to the switches the factory names.
		self.assertEqual("Bottom pop bumper", self.solenoids[9]["label"])
		self.assertEqual("Top pop bumper", self.solenoids[11]["label"])
		self.assertEqual("Bottom pop bumper", self.inputs[32]["label"])
		self.assertEqual("Top pop bumper", self.inputs[30]["label"])
		self.assertIn("BRN-ORG", self.solenoids[3]["physical"]["notes"])
		self.assertEqual("BRN-ORG", self.solenoids[3]["wiring"]["control_wire"])
		for number in (18, 19, 20, 21):
			self.assertIn("types public solenoids 18-21 as #89 bulb outputs", self.solenoids[number]["physical"]["notes"], number)
		self.assertEqual(50, self.solenoids[1]["wiring"]["nominal_voltage_v"])
		self.assertEqual(20, self.solenoids[17]["wiring"]["nominal_voltage_v"])
		self.assertEqual(5, self.solenoids[20]["wiring"]["nominal_voltage_v"])

	def test_lamp_space_and_led_board(self) -> None:
		self.assertEqual(set(range(1, 129)), set(self.lamps))
		self.assertEqual(USED_LAMPS, {number for number in range(1, 81) if self.lamps[number]["availability"] == "used"})
		self.assertEqual(UNUSED_LAMPS, {number for number in range(1, 81) if self.lamps[number]["availability"] == "unused"})
		self.assertEqual(LED_LAMPS, {number for number in range(81, 129) if self.lamps[number]["availability"] == "used"})
		self.assertEqual(22, len(LED_LAMPS))
		self.assertEqual({"112-5024-08"}, {self.lamps[61]["physical"]["part_number"]})
		self.assertEqual("165-5103-00", self.lamps[2]["physical"]["part_number"])
		self.assertEqual("165-5002-00", self.lamps[3]["physical"]["part_number"])
		self.assertEqual("165-5000-44-HF", self.lamps[4]["physical"]["part_number"])
		self.assertIn("Above the playfield", self.lamps[61]["physical"]["location"])
		for name, letters in LED_NAMES.items():
			for letter, address in letters.items():
				self.assertIn(f"{name} letter {letter} ", self.lamps[address]["label"], (name, letter))
		self.assertEqual({"Peter": {"P": 114, "E (second)": 89, "T": 90, "E (first)": 91, "R": 92}}["Peter"], {self.lamps[address]["label"].split(" letter ")[1].split(" (LED")[0]: address for address in (114, 89, 90, 91, 92)})
		# The knowledge note's table lists the same words and addresses as the definition.
		for name, letters in LED_NAMES.items():
			row = next(line for line in self.knowledge.splitlines() if line.startswith(f"| {name.upper()} |"))
			for letter, address in letters.items():
				self.assertIn(f"{letter} {address}", row)
		peter_row = next(line for line in self.knowledge.splitlines() if line.startswith("| PETER |"))
		for fragment in ("P 114", "E 89", "T 90", "E 91", "R 92"):
			self.assertIn(fragment, peter_row)
		gi = by_binding(self.definition, "outputs", "pinmame.output.gi")
		self.assertEqual({0}, set(gi))
		for circuit in ("F1", "F2", "F3", "F4"):
			self.assertIn(circuit, gi[0]["physical"]["notes"])

	def test_script_defects_are_stated_not_copied(self) -> None:
		for fragment in ("rear pop-bumper object is bound to switch 32", "Shrek (Stern 2008)", "lamps 81-84 and 97 as CHRIS"):
			self.assertIn(fragment, self.knowledge)
		table = next(source for source in self.definition["sources"] if source["id"] == "vpx.table.family-guy-2020")
		self.assertFalse(table["known_working"])
		self.assertIn("Shrek (Stern 2008)", table["locator"])

	def test_mechanisms_reference_declared_devices_and_keep_the_open_item(self) -> None:
		ids = {device["id"] for device in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertLessEqual(set(mechanism["actuators"] + mechanism["sensors"]), ids, mechanism["id"])
			for position in mechanism.get("positions", []):
				self.assertLessEqual(set(position["sensors"]), ids, mechanism["id"])
		monkey = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.evil-monkey-gate")
		self.assertEqual("observed", monkey["provenance"]["status"])
		self.assertIn("not documented or observed", monkey["behavior"])
		self.assertEqual(16, len(self.definition["mechanisms"]))
		fart = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.fart-drop-targets")
		self.assertEqual({44, 45, 46, 47}, {self.inputs_by_id(sensor) for sensor in fart["sensors"]})

	def inputs_by_id(self, identifier: str) -> int:
		return next(device["binding"]["device"] for device in self.definition["inputs"] if device["id"] == identifier)

	def test_excerpt_digests_and_known_pages(self) -> None:
		manual = next(source for source in self.definition["sources"] if source["id"] == "manual.stern-family-guy.2007-service")
		self.assertEqual("2bbcfa34ad70ab90c0fadabaf825850cecae58c8028af9aaabf8be1ad01979cd", manual["sha256"])
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["id"])
		text = (EXCERPT_ROOT / "manual-switch-matrix.md").read_text(encoding="utf-8")
		self.assertIn("| 40 | DEATH RETURN [INNER LT.] | 500-6227-02 |", text)
		self.assertIn("| 29 | RIGHT OUTLANE | 500-6227--01 (printed with a double hyphen) |", text)
		coil = (EXCERPT_ROOT / "manual-coil-chart.md").read_text(encoding="utf-8")
		self.assertIn("| 19 | EVIL MONKEY (LEFT RAMP GATE) | Q19 | BROWN | J7-P1 | 20v DC | VIO-ORG | J7-P4 | 32-1250 (515-6916-01-ND) |", coil)
		for path in EXCERPT_ROOT.glob("*.md"):
			self.assertNotIn(b"\r", path.read_bytes(), path.name)


	def placement_of(self, device: dict) -> dict:
		return device["spatial"]["placements"][0]

	def test_spatial_placements_follow_the_manual_not_the_table_bindings(self) -> None:
		seed = load_json(SPATIAL_SEED)["objects"]
		# The retained table binds its rear object to the manual's front bumper; the manual's drawing puts switch 30 and Q11 at the rear.
		for switch, coil, name in ((30, 11, "Bumper.Bumper1"), (31, 10, "Bumper.Bumper2"), (32, 9, "Bumper.Bumper3")):
			expected = seed[name][:2]
			self.assertEqual(expected, [self.placement_of(self.inputs[switch])["x"], self.placement_of(self.inputs[switch])["y"]], switch)
			self.assertEqual(expected, [self.placement_of(self.solenoids[coil])["x"], self.placement_of(self.solenoids[coil])["y"]], coil)
			self.assertIn("table", (self.inputs[switch].get("physical") or {}).get("notes", "") + (self.solenoids[coil].get("physical") or {}).get("notes", ""))
		self.assertLess(self.placement_of(self.inputs[30])["y"], self.placement_of(self.inputs[32])["y"])
		# The retained table lights the BRIAN and CHRIS letters under each other's names; the placements follow the printed letters.
		for lamp in LED_LAMPS:
			self.assertIn("lamp", self.lamps[lamp]["id"])
			self.assertEqual("observed", self.lamps[lamp]["spatial"]["status"], lamp)
			self.assertIn("LED", self.lamps[lamp]["physical"]["notes"], lamp)
		# Placements that cannot be supplied stay absent rather than guessed.
		for address in (18, 19, 20, 21, 22):
			self.assertNotIn("placements", self.inputs[address].get("spatial") or {}, address)
		for address in (25, 26, 27, 28):
			self.assertNotIn("placements", self.solenoids[address].get("spatial") or {}, address)
		ids = [pl["id"] for group in ("inputs", "outputs") for item in self.definition[group] for pl in (item.get("spatial") or {}).get("placements", [])]
		self.assertEqual(len(ids), len(set(ids)))
		for group in ("inputs", "outputs"):
			for item in self.definition[group]:
				for pl in (item.get("spatial") or {}).get("placements", []):
					self.assertTrue(0 <= pl["x"] <= 1 and 0 <= pl["y"] <= 1, pl["id"])
		self.assertIn("spatial_placement", self.definition["coverage"]["missing"])

	def test_spatial_seed_and_audit_are_pinned(self) -> None:
		seed = load_json(SPATIAL_SEED)
		audit = load_json(AUDIT)
		self.assertEqual("pinmame-spatial-blockers", audit["format"])
		self.assertEqual(MACHINE_ID, audit["machine_id"])
		self.assertEqual(hashlib.sha256(SPATIAL_SEED.read_bytes()).hexdigest(), audit["source_seed_sha256"])
		self.assertEqual(seed["table_sha256"], audit["table_sha256"])
		self.assertEqual("159558a39efd5a784bf0e587e9f07563e4fcd92765eeda02c9abc8bad015e2ff", seed["table_sha256"])
		self.assertEqual(sum(1 for group in ("inputs", "outputs", "displays") for item in self.definition[group] for _ in (item.get("spatial") or {}).get("placements", [])), audit["located_observations"])

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		seed = load_json(CALLOUTS)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		self.assertIn(CALLOUT_SOURCE, {source["id"] for source in self.definition["sources"]})
		checked = 0
		for device in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			for placement in (device.get("spatial") or {}).get("placements") or []:
				decision = decisions["placements"].get(placement["id"])
				status = placement["provenance"]["status"]
				if decision is None:
					self.assertEqual("observed", status, placement["id"])
					continue
				checked += 1
				self.assertEqual("validated" if decision["agrees"] else "observed", status, placement["id"])
				self.assertEqual(decision["agrees"], CALLOUT_SOURCE in placement["provenance"]["source_refs"], placement["id"])
				notes = (device.get("physical") or {}).get("notes") or ""
				self.assertEqual(not decision["agrees"], f"draws callout {decision['label']}" in notes, placement["id"])
		self.assertEqual(len(seed["checks"]), checked)
		self.assertEqual(drawing_callouts.summary(seed, decisions, "tools/seeds/stern/family-guy-2007-callouts.json", hashlib.sha256(CALLOUTS.read_bytes()).hexdigest()),
		                 load_json(AUDIT)["drawing_callout_check"])
		# Mini-playfield inset devices and the unfitted coil page are never checked against a drawing.
		for pid in [f"placement.switch-{n}.sensor" for n in range(50, 56)] + ["placement.lamp-68.emitter"]:
			self.assertNotIn(pid, seed["checks"], pid)
		self.assertEqual({"pdf-7", "pdf-9"}, set(seed["pages"]))
		for page in seed["pages"].values():
			self.assertGreaterEqual(len(page["controls"]), 5)
			self.assertFalse({c["feature"] for c in page["controls"]} & {c["feature"] for c in page["excluded_controls"]})

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review artifacts not configured")
	def test_drawing_callout_renders_and_reads_are_retained(self) -> None:
		seed = load_json(CALLOUTS)
		roots = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		self.assertGreaterEqual(drawing_callouts.verify_retained(seed, ROOT, None, roots), 2)
		retained = roots / seed["retained_artifacts"]["directory"].split("review-artifacts/", 1)[-1]
		manifest = retained / "manifest.json"
		self.assertEqual(seed["retained_artifacts"]["manifest_sha256"], hashlib.sha256(manifest.read_bytes()).hexdigest())
		for entry in load_json(manifest)["files"]:
			self.assertEqual(entry["sha256"], hashlib.sha256((retained / entry["path"]).read_bytes()).hexdigest(), entry["path"])


class FamilyGuyRuntimeEvidenceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.inputs = by_binding(cls.definition, "inputs", "pinmame.input.switch")
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}

	def summary(self, name: str) -> dict:
		return load_json(RUNTIME_ROOT / name)

	def retained(self, evidence: dict, label: str):
		import build_external_evidence_manifest as manifest

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return None
		(raw,) = evidence["runtime"]["raw_runs"]
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), label)
		digest = manifest.check_manifest(path.parent, evidence["runtime"]["game"])
		self.assertIn(f"{path.parent.name}/manifest.json SHA-256 {digest}", evidence["source"]["attribution"], label)
		run = json.loads(path.read_text(encoding="utf-8"))
		self.assertIsNone(run["failure"])
		self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
		self.assertEqual(evidence["runtime"]["emulator"]["sha256"], run["library_sha256"])
		self.assertEqual(evidence["runtime"]["game"], run["game"])
		if run.get("scenario"):
			self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
			self.assertEqual(raw["scenario_sha256"], hashlib.sha256((ROOT / raw["scenario_path"]).read_bytes()).hexdigest())
		return run

	def test_every_runtime_source_cites_its_summary_and_raw_run(self) -> None:
		cited = {source["uri"] for source in self.definition["sources"] if source["kind"] == "runtime_scenario"}
		files = {"internal:evidence/runtime/sam/" + path.name for path in RUNTIME_ROOT.glob("family-guy-*.json")}
		self.assertEqual(files, cited)
		for source in self.definition["sources"]:
			if source["kind"] != "runtime_scenario":
				continue
			evidence = load_json(ROOT / source["uri"][len("internal:"):])
			self.assertEqual(source["sha256"], evidence["runtime"]["raw_runs"][0]["sha256"])
			self.assertEqual([MACHINE_ID], evidence["machine_ids"])
			self.assertEqual(PINNED_LIBRARY_SHA256, evidence["runtime"]["emulator"]["sha256"])
			self.retained(evidence, source["id"])

	def test_switch_sweeps_name_every_matrix_switch_only_while_held(self) -> None:
		import family_guy_devices as dev

		for driver in SWEEP_DRIVERS:
			with self.subTest(driver=driver):
				evidence = self.summary(f"family-guy-{driver}-switch-test-sweep.json")
				actions = evidence["runtime"]["observations"]["named_action_observations"]
				snapshots = evidence["runtime"]["observations"]["diagnostic_snapshots"]
				self.assertEqual(list(range(1, 65)), [item["input_address"] for item in actions])
				self.assertEqual(66, len(snapshots))
				self.assertEqual("SWITCH TEST / NONE", snapshots[1]["interpreted_text"])
				for item, snapshot in zip(actions, snapshots[2:], strict=True):
					address = item["input_address"]
					name = dev.SWITCHES[address][6] if address in dev.SWITCHES else f"SWITCH #{address}"
					self.assertEqual(f"SWITCH TEST / {name} / LAST SW. #{address}", snapshot["interpreted_text"])
					self.assertEqual([address], item["host_stimulus_switch_addresses"])
					self.assertEqual([], item["observed_switch_addresses"])
					if address in dev.SWITCHES:
						self.assertIn(f'the ROM\'s switch test prints "{name}"', self.inputs[address]["physical"]["notes"])
				run = self.retained(evidence, driver)
				if run is None:
					continue
				by_label = {snap["label"]: snap for snap in run["snapshots"]}
				for address in range(1, 65):
					held = by_label[f"hold {address} (held)"]
					levels = {w["number"]: w["state"] for w in held["watched_switches"]}
					if driver == "fg_1200ag":
						# The held snapshot reads exactly the held address; on V8.00 the snapshot of public 15 reads 0
						# although the step's own read-back during the hold is 1 and the ROM names the switch.
						self.assertEqual(1, levels[address])
						self.assertEqual(sum(levels.values()), 1)
					else:
						self.assertLessEqual(sum(levels.values()), 1)
					display = held["displays"][0]
					self.assertEqual((display["pixel_sha256"], display["nonzero_pixels"]), (snapshots[address + 1]["pixel_sha256"], snapshots[address + 1]["nonzero_pixels"]))

	def test_firmware_versions_print_the_same_switch_and_lamp_names(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("retained harness frames are not available")
		harness = Path(root) / "family-guy-2007" / "harness"

		def region(path: Path, rows: tuple[int, int]) -> str:
			return hashlib.sha256(b"".join(row[24:] for row in read_pgm(path)[rows[0]:rows[1]])).hexdigest()

		def frames(kind: str, driver: str, label: str) -> dict[str, Path]:
			import re

			result = {}
			for path in sorted((harness / f"{kind}-sweep-{driver}" / "dmd").glob("*.pgm")):
				match = re.match(rf"\d+-({label})-display-0\.pgm", path.name)
				if match:
					result[match.group(1)] = path
			return result

		for driver in SWEEP_DRIVERS[1:]:
			with self.subTest(driver=driver, kind="switch"):
				base, other = frames("switch", "fg_1200ag", r"hold-\d+-held"), frames("switch", driver, r"hold-\d+-held")
				self.assertEqual(64, len(base))
				self.assertEqual(set(base), set(other))
				self.assertEqual([], [key for key in base if region(base[key], (0, 16)) != region(other[key], (0, 16))])
			with self.subTest(driver=driver, kind="lamp"):
				base, other = frames("lamp", "fg_1200ag", r"advance-lamp-test-\d+"), frames("lamp", driver, r"advance-lamp-test-\d+")
				self.assertEqual(80, len(base))
				self.assertEqual([], [key for key in base if hashlib.sha256(base[key].read_bytes()).hexdigest() != hashlib.sha256(other[key].read_bytes()).hexdigest()])

	def test_dedicated_sweep_shows_the_flipper_column_mirror(self) -> None:
		evidence = self.summary("family-guy-fg_1200ag-dedicated-switch-sweep.json")
		actions = {item["input_address"]: item["label"] for item in evidence["runtime"]["observations"]["named_action_observations"]}
		self.assertEqual({65, 66, 67, 68, 69, 70, 71, 72, 81, 82, 83, 84, 85, 86, 87, 88, -7, -6, -5, -4}, set(actions))
		for address, name in FLIPPER_COLUMN.items():
			self.assertIn(name, actions[address])
		self.assertIn("U.R. FLIPPER E.O.S.", actions[85])
		self.assertIn("U.L. FLIPPER E.O.S.", actions[88])
		self.assertIn("TILT PENDULUM", actions[-7])
		self.assertIn("SLAM TILT", actions[-6])
		self.assertIn("L. POST SAVE", actions[71])

	def test_coil_sweeps_pair_each_displayed_coil_with_its_solenoid(self) -> None:
		import family_guy_runtime as runtime

		for driver in SWEEP_DRIVERS:
			with self.subTest(driver=driver):
				evidence = self.summary(f"family-guy-{driver}-coil-test-sweep.json")
				actions = evidence["runtime"]["observations"]["named_action_observations"]
				self.assertEqual(35, len(actions))
				shown = runtime.COIL_SELECTOR
				for position, number in enumerate(shown, start=1):
					self.assertEqual([number], actions[position - 1]["transitioned_solenoid_addresses"])
				self.assertNotIn(20, {item for action in actions for item in action["transitioned_solenoid_addresses"]})
				self.assertNotIn(24, {item for action in actions for item in action["transitioned_solenoid_addresses"]})
				aux_positions = [action for action in actions[30:33] if action["transitioned_solenoid_addresses"] == []]
				if driver in FIRMWARE_WITH_AUX_COILS:
					self.assertEqual(2, len(aux_positions))
					self.assertIn("AUX 1: TICKET ADVANCE", actions[30]["label"])
					self.assertIn("AUX 3: TICKET ENABLE", actions[31]["label"])
					self.assertEqual([1], actions[32]["transitioned_solenoid_addresses"])
				else:
					self.assertEqual([1], actions[30]["transitioned_solenoid_addresses"])
					self.assertEqual([2], actions[31]["transitioned_solenoid_addresses"])
				self.retained(evidence, driver)

	def test_lamp_sweeps_drive_lamp_n_at_position_n_and_the_led_board_throughout(self) -> None:
		for driver in SWEEP_DRIVERS:
			with self.subTest(driver=driver):
				evidence = self.summary(f"family-guy-{driver}-lamp-test-sweep.json")
				observations = evidence["runtime"]["observations"]
				seen = set(observations["lamp_addresses_seen"])
				self.assertEqual(LED_LAMPS, {number for number in seen if number > 80})
				self.assertTrue(set(range(1, 81)) <= seen | {1})
				self.assertEqual(83, len(observations["diagnostic_snapshots"]))
				self.assertEqual(81, len(observations["named_action_observations"]))
				self.retained(evidence, driver)

	def test_boot_start_records_game_on_gi_and_stewie_homing(self) -> None:
		evidence = self.summary("family-guy-fg_1200ag-boot-start.json")
		observations = evidence["runtime"]["observations"]
		self.assertEqual([0], observations["gi_addresses_seen"])
		self.assertEqual({1, 19, 20, 24, 33}, set(observations["solenoid_addresses_seen"]))
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], observations["display_layouts_seen"])
		self.assertTrue(LED_LAMPS <= set(observations["lamp_addresses_seen"]))
		run = self.retained(evidence, "boot")
		if run is not None:
			self.assertEqual({18, 19, 20, 21, 55, 83, 81}, {item["switch"] for item in run["initial_switches"]})

	def test_evil_monkey_probes_keep_the_latch_gate_open(self) -> None:
		closed = self.summary("family-guy-fg_1200ag-evil-monkey-probe-closed.json")["runtime"]["observations"]["named_action_observations"]
		opened = self.summary("family-guy-fg_1200ag-evil-monkey-probe-open.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([], [item["label"] for item in closed if 19 in item["transitioned_solenoid_addresses"]])
		firing = [item["label"] for item in opened if 19 in item["transitioned_solenoid_addresses"]]
		self.assertTrue(firing[0].startswith("Start button (switch 35 open)"))
		self.assertEqual([], [label for label in firing if label.startswith("switch 35 closes again") or label.startswith("Chris target (switch 3) hit again")])
		self.assertTrue(any("Chris target" in item["label"] and 27 in item["transitioned_solenoid_addresses"] for item in closed))
		for name in ("closed", "open"):
			evidence = self.summary(f"family-guy-fg_1200ag-evil-monkey-probe-{name}.json")
			self.retained(evidence, name)



if __name__ == "__main__":
	unittest.main()
