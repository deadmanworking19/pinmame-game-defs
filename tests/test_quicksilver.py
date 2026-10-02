"""Gates for the Stern Quicksilver (1980) definition.

They lock down what was expensive to establish and cheap to lose: the lamp decoder arithmetic and the two SCR pairs that are easy to
transpose, the physical-to-public solenoid mapping, the identity of the four drivers, the one unresolved lamp, and the boundary between what
the retained table and runs measured and what they did not. Fixtures that restate a printed sheet are kept apart from the curator on
purpose: a test that checks the generator against its own output only proves the generator is self-consistent.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402

import curate_quicksilver as curator  # noqa: E402
import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines/partial/stern/quicksilver-1980.json"
SEED_PATH = ROOT / "tools/seeds/stern/quicksilver-1980.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/quicksilver-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/quicksilver-1980.md"
EXCERPTS = ROOT / "evidence/excerpts/stern.quicksilver.1980"
RUNTIME_PATH = ROOT / "evidence/runtime/stern/quicksilver-self-test-and-gameplay.json"
MACHINE_ID = "stern.quicksilver.1980"

# Printed switch identification table (manual page 16), keyed by public address, as one distinctive word each.
MANUAL_SWITCHES = {
	1: "chute", 2: "chute", 3: "chute", 4: "spinner", 5: "spinner", 6: "credit", 7: "tilt", 8: "slam", 9: "pop", 10: "pop", 11: "pop", 12: "slingshot", 13: "slingshot",
	14: "stand-up", 15: "stand-up", 16: "stand-up", 17: "lane", 18: "lane", 19: "lane", 20: "lane", 21: "drop", 22: "drop", 23: "drop", 24: "drop",
	25: "stand-up", 26: "stand-up", 27: "stand-up", 28: "roll-over", 29: "kick-out", 30: "drop", 31: "drop", 32: "drop", 33: "out-hole",
	34: "outside", 35: "outside", 36: "return", 37: "return", 38: "bounce", 39: "roll-over", 40: "stand-up",
}
# Printed solenoid identification table (manual page 14): physical number -> text. The public address of each comes from the retained self-test.
# physical number -> (printed words that the public device's label must contain, public address), from the Solenoid Driver Schematic's list.
MANUAL_SOLENOIDS = {
	1: (("left", "thumper"), 2), 2: (("right", "thumper"), 1), 3: (("knocker",), 6), 4: (("center", "bank"), 7), 5: (("lower", "thumper"), 3), 6: (("left", "sling"), 4), 7: (("right", "sling"), 5),
	8: (("right", "bank"), 8), 13: (("kick-out",), 9), 14: (("out-hole",), 10), 15: (("flipper", "relay"), 19), 19: (("lock",), 18),
}
MANUAL_OPEN_SOLENOIDS = {9: 11, 10: 12, 11: 14, 12: 13, 16: 15, 17: 17, 18: 20}
# (jack, pin) -> (description fragment) transcribed from the Lamp Driver Schematic's list; independent of tools/quicksilver_data.py.
LAMP_LIST = {
	("J1", 18): "bonus 1,000", ("J1", 1): "bonus 2,000", ("J3", 26): "bonus 3,000", ("J3", 1): "bonus 4,000", ("J1", 19): "bonus 5,000", ("J1", 9): "bonus 6,000",
	("J3", 25): "bonus 7,000", ("J3", 12): "bonus 8,000", ("J1", 17): "bonus 9,000", ("J1", 8): "bonus 10,000", ("J3", 19): "bonus 20,000", ("J3", 15): "super bonus",
	("J1", 14): "bonus 2x", ("J1", 2): "bonus 3x", ("J3", 16): "bonus 4x", ("J3", 9): "bonus 5x", ("J1", 3): "center bank target 10,000", ("J3", 17): "center bank target 15,000",
	("J3", 11): "center bank target 20,000", ("J1", 24): "flashing extra ball", ("J2", 14): "left special", ("J2", 11): "game over", ("J2", 7): "left spinner",
	("J2", 16): "left return lanes", ("J2", 22): "high score to date", ("J2", 1): "match", ("J2", 20): "right return lanes", ("J2", 6): "right spinner",
	("J2", 15): "right special", ("J1", 16): "right bank target 2x", ("J1", 7): "right bank target 3x", ("J3", 27): "right bank target 4x", ("J3", 4): "right bank target 5x",
	("J1", 28): "right bank target 25,000", ("J2", 21): "shoot again", ("J3", 3): "lamp s", ("J3", 23): "lamp i", ("J1", 10): "lamp l", ("J1", 6): "lamp v", ("J1", 13): "lamp e",
	("J3", 2): "lamp r", ("J2", 10): "tilt", ("J3", 18): "divider 1", ("J3", 20): "divider 2", ("J1", 11): "divider 3", ("J1", 25): "divider 4", ("J3", 10): "divider 5",
	("J2", 3): "lane q", ("J2", 4): "lane u", ("J2", 12): "lane i", ("J2", 13): "lane c", ("J2", 5): "lamp k", ("J2", 2): "top special", ("J1", 23): "center bank target 5,000",
}
UNUSED_LAMPS = {25, 27, 29, 41, 43}
UNRESOLVED_LAMP = 6
EXPECTED_MISSING = ["output_semantics", "spatial_placement"]
DRIVER_IDS = {"quicksil", "quicksfp", "quicksib", "quicksic"}


def markdown_rows(path: Path) -> list[list[str]]:
	rows = []
	for line in path.read_text(encoding="utf-8").splitlines():
		if line.startswith("|") and not re.match(r"^\|\s*:?-+", line):
			rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
	return rows


def connector_scr_table() -> dict[tuple[str, int], int]:
	"""(jack, pin) -> SCR number, read from the connector-label excerpt."""
	table: dict[tuple[str, int], int] = {}
	jack = None
	for line in (EXCERPTS / "lamp-driver-connector-labels.md").read_text(encoding="utf-8").splitlines():
		match = re.match(r"^### (J\d)$", line)
		if match:
			jack = match.group(1)
			continue
		match = re.match(r"^\| (\d+) \| Q(\d+) \|$", line)
		if match and jack:
			table[(jack, int(match.group(1)))] = int(match.group(2))
	return table


def decoder_table() -> dict[int, int]:
	"""public lamp address -> SCR number, read from the decoder excerpt (public = 16k + a + 1)."""
	result: dict[int, int] = {}
	chip = None
	for line in (EXCERPTS / "lamp-driver-decoder-outputs.md").read_text(encoding="utf-8").splitlines():
		match = re.match(r"^### U(\d) \(MC14514B\)$", line)
		if match:
			chip = int(match.group(1)) - 1
			continue
		match = re.match(r"^\| S(\d+) \| \d+ \| R(\d+) \| Q(\d+) \|$", line)
		if match and chip is not None:
			assert match.group(2) == match.group(3), line
			result[16 * chip + int(match.group(1)) + 1] = int(match.group(3))
	return result


class QuicksilverDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.inputs = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		cls.dips = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"}
		cls.direct = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "physical.input.direct"}
		cls.solenoids = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}

	def test_deterministic_artifacts_match_the_curator(self) -> None:
		curator.check(ROOT)
		self.assertEqual(canonical_bytes(self.definition), SEED_PATH.read_bytes())

	def test_identity_and_driver_group(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, "Stern", "Quicksilver", 1980, 1895), (machine["id"], machine["manufacturer"], machine["name"], machine["year"], machine["ipdb_id"]))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertEqual({"identical"}, {driver["physical_compatibility"] for driver in drivers.values()})
		self.assertTrue(all("display_overrides" not in driver for driver in drivers.values()))
		self.assertEqual(None, drivers["quicksil"].get("clone_of"))
		self.assertEqual({"quicksil"}, {driver["clone_of"] for driver in drivers.values() if driver["id"] != "quicksil"})
		catalog = load_json(ROOT / "catalog/pinmame.json")
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") == MACHINE_ID})
		self.assertEqual("pinmame.stern-mpu200", self.definition["controller"]["platform"])

	def test_coverage_is_partial_with_exactly_the_documented_blockers(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(EXPECTED_MISSING, coverage["missing"])
		self.assertEqual([], unresolved_conflicts(self.definition))
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual(2, self.definition["schema_version"])

	def test_every_matrix_address_is_enumerated_named_and_normally_open(self) -> None:
		self.assertEqual(set(MANUAL_SWITCHES), {address for address in self.inputs if 1 <= address <= 40})
		for address, word in MANUAL_SWITCHES.items():
			label = self.inputs[address]["label"].lower()
			self.assertIn(word.replace("-", " "), label.replace("-", " "), address)
			self.assertEqual("used", self.inputs[address]["availability"], address)
			self.assertIs(False, self.inputs[address]["normally_closed"], address)
		for address in (-7, -6, -5, 81, 82, 83, 84):
			self.assertIn(address, self.inputs)
		self.assertEqual("unused", self.inputs[81]["availability"])
		self.assertEqual("unused", self.inputs[83]["availability"])
		self.assertEqual("used", self.inputs[82]["availability"])
		self.assertEqual("used", self.inputs[84]["availability"])
		self.assertEqual({1, 2}, set(self.direct))
		self.assertTrue(all(item["normally_closed"] is True for item in self.direct.values()))
		self.assertEqual(set(range(1, 33)), set(self.dips))

	def test_switch_wiring_follows_the_strobe_and_return_arithmetic(self) -> None:
		strobes = ["A4J2-1", "A4J2-2", "A4J2-3", "A4J2-4", "A4J2-5"]
		returns = ["A4J2-8", "A4J2-9", "A4J2-10", "A4J2-11", "A4J2-12", "A4J2-13", "A4J2-14", "A4J2-15"]
		for address in range(1, 41):
			wiring = self.inputs[address]["wiring"]
			if address in (1, 2, 3, 6, 7, 8):
				self.assertTrue(wiring["return_connection"].startswith("A4J3-"), address)
				continue
			self.assertEqual(strobes[(address - 1) // 8], wiring["control_connection"], address)
			self.assertEqual(returns[(address - 1) % 8], wiring["return_connection"], address)

	def test_solenoid_translation_matches_the_printed_list_and_the_retained_self_test(self) -> None:
		by_physical = {int(item["aliases"][-1]["value"]): address for address, item in self.solenoids.items() if address not in (46, 48) and item["aliases"][-1]["namespace"] == "manual.self-test"}
		for physical, (word, address) in MANUAL_SOLENOIDS.items():
			self.assertEqual(address, by_physical[physical], physical)
			self.assertEqual("used", self.solenoids[address]["availability"], physical)
			label = self.solenoids[address]["label"].lower()
			for part in word:
				self.assertIn(part, label, f"physical solenoid {physical} is printed {word} but public {address} is {label!r}")
		for physical, address in MANUAL_OPEN_SOLENOIDS.items():
			self.assertEqual(address, by_physical[physical], physical)
			self.assertEqual("unused", self.solenoids[address]["availability"], physical)
		self.assertEqual({46, 48}, {address for address in self.solenoids if address > 20})
		self.assertNotIn(16, self.solenoids)
		self.assertEqual("relay", self.solenoids[19]["kind"])
		for address, side in ((46, "right"), (48, "left")):
			self.assertIn(side, self.solenoids[address]["label"].lower())
			self.assertEqual("effect", self.solenoids[address]["spatial"]["placements"][0]["role"])
		# The harness-proved pairs: switch -> the coil the ROM fires.
		pairs = {9: 1, 10: 2, 11: 3, 12: 4, 13: 5}
		for switch, coil in pairs.items():
			relationship = [item for item in self.definition["relationships"] if item["source"] == self.inputs[switch]["id"]]
			self.assertEqual([self.solenoids[coil]["id"]], [item["destination"] for item in relationship], switch)

	def test_lamp_addresses_follow_the_decoder_and_the_connector_table(self) -> None:
		expected = {*range(1, 16), *range(17, 32), *range(33, 48), *range(49, 64)}
		self.assertEqual(expected, set(self.lamps))
		decoder = decoder_table()
		self.assertEqual(expected, set(decoder))
		self.assertEqual(list(range(1, 61)), sorted(decoder.values()), "every SCR Q1-Q60 must appear exactly once on the decoders")
		connectors = connector_scr_table()
		listed_pubs = set()
		for (jack, pin), fragment in LAMP_LIST.items():
			scr = connectors[(jack, pin)]
			address = next(address for address, q in decoder.items() if q == scr)
			listed_pubs.add(address)
			lamp = self.lamps[address]
			self.assertEqual(f"Q{scr}", lamp["wiring"]["driver_transistor"], (jack, pin))
			self.assertEqual("used", lamp["availability"], (jack, pin))
			self.assertIn(f"LDA-{jack}-{pin}", {alias["value"] for alias in lamp["aliases"]}, (jack, pin))
			self.assertIn(fragment, lamp["label"].lower(), (jack, pin))
		self.assertEqual(set(self.lamps) - UNUSED_LAMPS - {UNRESOLVED_LAMP}, listed_pubs)

	def test_the_transposable_scr_pairs(self) -> None:
		# U2 outputs S7/S8 drive Q25/Q24 and the U3/U4 S9 outputs drive Q41/Q46: a transposition of either pair moves a named lamp.
		self.assertEqual("Q25", self.lamps[24]["wiring"]["driver_transistor"])
		self.assertEqual("Q24", self.lamps[25]["wiring"]["driver_transistor"])
		self.assertEqual("lamp.standup-v", self.lamps[24]["id"])
		self.assertEqual("Q41", self.lamps[42]["wiring"]["driver_transistor"])
		self.assertEqual("Q46", self.lamps[58]["wiring"]["driver_transistor"])
		self.assertEqual("lamp.top-rollover-divider-2", self.lamps[42]["id"])
		self.assertEqual("lamp.top-rollover-divider-1", self.lamps[58]["id"])
		self.assertEqual("lamp.left-spinner", self.lamps[62]["id"])
		self.assertEqual("lamp.right-spinner", self.lamps[46]["id"])
		self.assertEqual({"J2-7"}, {part for part in ("J2-7",) if f"LDA-{part}" in {alias["value"] for alias in self.lamps[62]["aliases"]}})

	def test_unlisted_lamps_and_the_one_unresolved_circuit(self) -> None:
		for address in UNUSED_LAMPS:
			self.assertEqual("unused", self.lamps[address]["availability"], address)
			self.assertEqual("unused", self.lamps[address]["spatial"]["reason"], address)
		unresolved = self.lamps[UNRESOLVED_LAMP]
		self.assertEqual("unknown", unresolved["availability"])
		self.assertNotIn("spatial", unresolved)
		self.assertEqual([UNRESOLVED_LAMP], [address for address, lamp in self.lamps.items() if lamp["availability"] == "unknown"])
		for address in (13, 45, 61, 63):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual(2, self.lamps[11]["physical"]["quantity"])
		self.assertEqual("emitter", self.lamps[11]["spatial"]["placements"][0]["role"])
		self.assertEqual([10, 26, 42, 57, 58], sorted(address for address, lamp in self.lamps.items() if "spatial" not in lamp and lamp["availability"] == "used"))

	def test_placements_are_inside_the_playfield_and_only_callout_agreement_validates(self) -> None:
		count = 0
		statuses: dict[str, int] = {}
		validated = set()
		for item in [*self.definition["inputs"], *self.definition["outputs"]]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			for placement in spatial["placements"]:
				count += 1
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				status = placement["provenance"]["status"]
				statuses[status] = statuses.get(status, 0) + 1
				if status == "validated":
					validated.add(placement["id"])
					self.assertIn(curator.CALLOUT_SOURCE, placement["provenance"]["source_refs"], placement["id"])
		self.assertGreater(count, 90)
		self.assertEqual({"observed", "validated"}, set(statuses))
		seed = curator.callout_seed()
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
		self.assertEqual(agreeing, validated)
		# The right flipper and the kick-out hole are the two checked placements the drawings do not confirm; lamps are never checked.
		self.assertEqual({"device.right-flipper.effect", "switch.kick-out-hole.sensor"}, set(decisions["placements"]) - agreeing)
		for pid in ("device.left-flipper.effect", "device.out-hole-kicker.effect", "switch.left-pop-bumper.sensor"):
			self.assertIn(pid, validated)
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(count, report["placement_count"])
		self.assertEqual(len(validated), report["callout_check"]["validated"])
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(sorted(agreeing), sorted(validated))
		# Report-level projection entries must name real bindings.
		direct = {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "physical.input.direct"}
		for entry in report["projections"]:
			if entry["group"] == "physical.input.direct":
				self.assertIn(entry["address"], direct)

	def test_mechanisms_name_existing_devices_and_each_actuator_once(self) -> None:
		devices = {item["id"] for item in [*self.definition["inputs"], *self.definition["outputs"]]}
		owners: dict[str, str] = {}
		for mechanism in self.definition["mechanisms"]:
			for ref in [*mechanism["actuators"], *mechanism["sensors"]]:
				self.assertIn(ref, devices, mechanism["id"])
			for ref in mechanism["actuators"]:
				self.assertNotIn(ref, owners)
				owners[ref] = mechanism["id"]
		self.assertEqual(
			{"mech.out-hole", "mech.kick-out-hole", "mech.center-drop-bank", "mech.right-drop-bank", "mech.spinners", "mech.thumper-bumpers", "mech.slingshots", "mech.flippers"},
			{mechanism["id"] for mechanism in self.definition["mechanisms"]},
		)

	def test_displays_match_the_pinned_dispst7_layout(self) -> None:
		displays = {item["id"]: item for item in self.definition["displays"]}
		self.assertEqual([(0, 1, 7), (1, 9, 7), (2, 17, 7), (3, 25, 7), (4, 35, 2), (5, 38, 2)], [(item["controller_index"], item["segment_start"], item["width"]) for item in self.definition["displays"]])
		self.assertEqual(6, len(displays))

	def test_the_excerpt_tables_agree_with_the_definition(self) -> None:
		rows = markdown_rows(EXCERPTS / "switch-identification.md")
		printed = {int(row[0]): row[1] for row in rows if len(row) == 4 and row[0].isdigit()} | {int(row[2]): row[3] for row in rows if len(row) == 4 and row[2].isdigit()}
		self.assertEqual(set(range(1, 41)), set(printed))
		for address, text in printed.items():
			self.assertTrue(text and text != "---", address)
		self.assertIn("LEFT SPINNER", printed[5])
		self.assertIn("RIGHT SPINNER", printed[4])
		self.assertIn("SLAM", printed[8])

	def test_service_switch_and_flipper_pairing(self) -> None:
		self.assertEqual("service.button", self.inputs[-7]["roles"][0])
		self.assertEqual("flipper.lower.left.button", self.inputs[84]["roles"][0])
		self.assertEqual("flipper.lower.right.button", self.inputs[82]["roles"][0])
		self.assertEqual("device.left-flipper", self.solenoids[48]["id"])
		self.assertEqual("device.right-flipper", self.solenoids[46]["id"])

	def test_the_retained_slingshot_defect_is_a_device_note_and_not_a_conflict(self) -> None:
		self.assertEqual([], self.definition["conflicts"])
		self.assertIn("pulses 20", self.inputs[12]["physical"]["notes"])
		self.assertIn("pulses 21", self.inputs[13]["physical"]["notes"])

	def test_knowledge_note_states_the_blockers_and_the_translations(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for fragment in ("Coverage: **partial", "`2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18`", "SCR Q10", "availability `unknown`", "Q25 and Q24", "Q41 and Q46", "dispst7", "quicksib", "quicksic"):
			self.assertIn(fragment, text)

	def test_no_other_machines_leak_into_the_artifacts(self) -> None:
		catalog = load_json(ROOT / "catalog/pinmame.json")
		foreign = {record["id"] for record in catalog["machines"] if record.get("id") and record["id"] != MACHINE_ID}
		# Full machine ids only: short driver ids fire inside ordinary English (there is a PinMAME driver called `rotation`).
		texts = [json.dumps(self.definition), KNOWLEDGE_PATH.read_text(encoding="utf-8"), json.dumps(load_json(SPATIAL_REPORT_PATH))]
		texts += [path.read_text(encoding="utf-8") for path in sorted(EXCERPTS.glob("*.md"))]
		for text in texts:
			for token in sorted(foreign):
				self.assertIsNone(re.search(rf"(?<![A-Za-z0-9._-]){re.escape(token)}(?![A-Za-z0-9._-])", text), token)

	def test_sources_are_complete_and_scripts_are_pinned(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		for identifier in ("manual.stern.quicksilver.1980", "schematic.stern.quicksilver.lamp-driver", "schematic.stern.quicksilver.solenoid-driver", "vpx-table.quicksilver-vpw-1-0", "runtime.quicksilver.gameplay"):
			self.assertIn(identifier, sources)
		self.assertEqual(curator.TABLE_SHA256, sources["vpx-table.quicksilver-vpw-1-0"]["sha256"])
		self.assertEqual(curator.SCRIPT_SHA256, sources["vpx-script.quicksilver-vpw-1-0"]["sha256"])
		for scenario, digest in curator.SCENARIO_SHA256.items():
			path = ROOT / f"tools/harness-scenarios/stern/quicksilver-{scenario}.json"
			self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest(), scenario)

	def test_runtime_summary_declares_the_translations(self) -> None:
		evidence = load_json(RUNTIME_PATH)
		observations = evidence["runtime"]["observations"]
		self.assertEqual({str(number): address for number, address in enumerate((2, 1, 6, 7, 3, 4, 5, 8, 11, 12, 14, 13, 9, 10, 19, 15, 17, 20, 18), start=1)}, observations["physical_service_solenoid_to_public"])
		self.assertEqual([16, 32, 48, 64], observations["lamp_decoder_holes_not_seen"])
		self.assertEqual(set(self.lamps), set(observations["lamp_addresses_seen"]))
		self.assertTrue(UNUSED_LAMPS.isdisjoint(observations["lamp_addresses_driven_outside_self_test"]))
		self.assertIn(UNRESOLVED_LAMP, observations["lamp_addresses_driven_outside_self_test"])
		self.assertEqual({"self-test", "stuck-switch", "gameplay"}, {run["name"] for run in evidence["runtime"]["raw_runs"]})


class QuicksilverRetainedEvidenceTests(unittest.TestCase):
	"""Run only when the retained external roots are configured; the no-evidence run skips them cleanly."""

	def test_harness_runs_reproduce_the_runtime_summary(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		runs = Path(root) / "quicksilver-1980" / "harness" if root else None
		if not runs or not runs.is_dir():
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT does not hold the retained Quicksilver runs")
		completed = subprocess.run([sys.executable, str(ROOT / "tools/summarize_quicksilver_runtime.py"), "--runs", str(runs), "--check"], capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

	def test_drawing_callout_artifacts_match_their_manifest(self) -> None:
		manuals, reviews = os.environ.get("PINMAME_MANUALS_ROOT"), os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not manuals or not reviews or not (Path(reviews) / "quicksilver-1980" / "callout-check").is_dir():
			self.skipTest("PINMAME_MANUALS_ROOT and PINMAME_REVIEW_ARTIFACTS_ROOT do not hold the retained callout check")
		self.assertGreater(drawing_callouts.verify_retained(curator.callout_seed(), ROOT, Path(manuals), Path(reviews)), 2)

	def test_retained_extraction_matches_its_manifest(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root or not (Path(root) / curator.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("PINMAME_VPX_SOURCES_ROOT does not hold the retained Quicksilver extraction")
		curator.verify_extraction_manifest(Path(root))

	def test_every_raw_coordinate_matches_the_retained_extraction(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		extraction = Path(root) / curator.EXTRACTION_RELATIVE_PATH if root else None
		if not extraction or not extraction.is_dir():
			self.skipTest("PINMAME_VPX_SOURCES_ROOT does not hold the retained Quicksilver extraction")
		import quicksilver_data as data

		centres: dict[tuple[str, str], tuple[float, float]] = {}
		lights: dict[int, tuple[float, float]] = {}
		for path in (extraction / "gameitems").glob("*.json"):
			kind = path.name.split(".")[0]
			if kind in ("Primitive", "Reel", "Timer", "Flasher"):
				continue
			body = next(iter(json.loads(path.read_text(encoding="utf-8")).values()))
			centre = None
			for key in ("center", "position"):
				if isinstance(body.get(key), dict) and "x" in body[key]:
					centre = (body[key]["x"], body[key]["y"])
					break
			if centre is None and body.get("drag_points"):
				points = body["drag_points"]
				centre = (sum(p["x"] for p in points) / len(points), sum(p["y"] for p in points) / len(points))
			if centre is None:
				continue
			centres[(kind, body["name"])] = centre
			if kind == "Light" and re.fullmatch(r"L\d\d", body["name"]):
				lights[body["timer_interval"]] = centre
		collection = json.loads((extraction / "collections.json").read_text(encoding="utf-8"))
		insert_lamps = next(item["items"] for item in collection if item["name"] == "InsertLamps")
		for number, raw in data.LIGHTS.items():
			self.assertIn(f"L{number:02d}", insert_lamps, number)
			self.assertAlmostEqual(raw[0], lights[number][0], places=1, msg=number)
			self.assertAlmostEqual(raw[1], lights[number][1], places=1, msg=number)
		for spec in [*data.SWITCHES.values(), *data.SOLENOIDS.values(), *data.FLIPPERS.values()]:
			if not spec.get("positions") or ".." in spec.get("table", "") :
				continue
			kind, names = spec["table"].split(" ", 1)
			parts = [name.strip() for name in names.split(",")]
			self.assertEqual(len(parts), len(spec["positions"]), spec["id"] if "id" in spec else spec["table"])
			for name, position in zip(parts, spec["positions"]):
				self.assertAlmostEqual(position[0], centres[(kind, name)][0], places=2, msg=spec["table"])
				self.assertAlmostEqual(position[1], centres[(kind, name)][1], places=2, msg=spec["table"])
		for address, names, in ((7, ["sw21", "sw22", "sw23", "sw24"]), (8, ["sw30", "sw31", "sw32"])):
			mean = (sum(centres[("Wall", n)][0] for n in names) / len(names), sum(centres[("Wall", n)][1] for n in names) / len(names))
			self.assertAlmostEqual(data.SOLENOIDS[address]["positions"][0][0], mean[0], places=2)
			self.assertAlmostEqual(data.SOLENOIDS[address]["positions"][0][1], mean[1], places=2)


if __name__ == "__main__":
	unittest.main()
