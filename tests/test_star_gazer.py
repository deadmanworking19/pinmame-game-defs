"""Fail-closed tests for the Stern Star Gazer (1980) definition.

Star Gazer is an MPU-200 machine whose printed numbers (solenoid test order, switch matrix labels,
lamp chart rows) differ from PinMAME's public addresses in ways that look like tidy-ups and are
not. Each of those is asserted separately, against the retained runtime summary where the ROM
decided it, so a regression names the fact that broke.
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
sys.path.insert(0, str(ROOT / "src"))

import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "star-gazer-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "star-gazer-1980.md"
SUMMARY_PATH = ROOT / "evidence" / "runtime" / "by35" / "star-gazer-1980-harness.json"
SPATIAL_SEED = ROOT / "tools" / "seeds" / "stern" / "star-gazer-1980-spatial.json"
CALLOUT_SEED = ROOT / "tools" / "seeds" / "stern" / "star-gazer-1980-callouts.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "stern.star-gazer.1980"

# Printed solenoid test number -> public address, as paired by the ROM's own solenoid test.
TEST_TO_PUBLIC = {1: 2, 2: 1, 3: 6, 4: 7, 5: 3, 6: 4, 7: 5, 8: 8, 9: 11, 10: 12, 11: 14, 12: 13, 13: 9, 14: 10, 15: 19, 16: 15, 17: 17, 18: 20, 19: 18}
# Closing a zodiac switch in play flashes this public lamp.
ZODIAC_LAMP = {10: 1, 11: 17, 17: 33, 18: 49, 19: 2, 20: 18, 21: 34, 31: 50, 32: 3, 38: 19, 39: 35, 40: 51}
SIGNS = {1: "Gemini", 17: "Cancer", 33: "Leo", 49: "Virgo", 2: "Libra", 18: "Scorpio", 34: "Sagittarius", 50: "Capricorn", 3: "Aquarius", 19: "Pisces", 35: "Aries", 51: "Taurus"}
UNUSED_SOLENOIDS = {9, 10, 13, 14, 15, 17, 20}
LAMP_ADDRESSES = [n for n in range(1, 64) if n % 16 != 0]


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def file_digest(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def synthetic_display(text: str) -> list[int]:
	glyphs = {"0": 0x3F, "1": 0x06, "2": 0x5B, "3": 0x4F, "4": 0x66, "5": 0x6D, "6": 0x7D, "7": 0x07, "8": 0x7F, "9": 0x6F, " ": 0x00}
	return [glyphs[character] for character in text]


class StarGazerSummaryGuardTests(unittest.TestCase):
	"""The summary generator must refuse runs that do not show what its notes would claim."""

	@staticmethod
	def lamp_events(order: list[int], start: float = 31.0, step: float = 0.6) -> list[dict]:
		return [{"event": "lamp", "number": number, "state": 1, "time_s": start + step * index} for index, number in enumerate(order)]

	def test_value_sweep_accepts_the_chart_order_and_rejects_others(self) -> None:
		import star_gazer_runtime_summary as summary

		self.assertEqual([7, 23, 39, 55, 8, 24, 40, 56], summary.verify_value_sweep({"events": self.lamp_events([7, 23, 39, 55, 8, 24, 40, 56])}))
		self.assertEqual([7, 23, 39, 55, 8, 24, 40, 56], summary.verify_value_sweep({"events": self.lamp_events([9, 7, 23, 39, 55, 8, 24, 40, 56, 9])}))
		for bad in ([], [7, 23, 39, 55, 24, 8, 40, 56], [7, 23, 39, 55, 8, 24, 40], [56, 40, 24, 8, 55, 39, 23, 7]):
			with self.assertRaises(SystemExit, msg=str(bad)):
				summary.verify_value_sweep({"events": self.lamp_events(bad)})

	def test_lockstep_rejects_a_missing_or_shifted_partner(self) -> None:
		import star_gazer_runtime_summary as summary

		def run(a_times: list[float], b_times: list[float]) -> dict:
			events = []
			for number, times in ((31, a_times), (9, b_times)):
				for index, moment in enumerate(times):
					events.append({"event": "lamp", "number": number, "state": 1 - index % 2, "time_s": moment})
			return {"events": events}

		times = [40.4 + 0.8 * index for index in range(8)]
		self.assertEqual(8, summary.verify_lockstep(run(times, list(times)), 31, 9))
		with self.assertRaises(SystemExit):
			summary.verify_lockstep(run(times, times[:-1]), 31, 9)
		with self.assertRaises(SystemExit):
			summary.verify_lockstep(run(times, [moment + 0.5 for moment in times]), 31, 9)
		with self.assertRaises(SystemExit):
			summary.verify_lockstep(run([], []), 31, 9)

	def test_switch_test_requires_each_number_and_the_flashing_zero(self) -> None:
		import star_gazer_runtime_summary as summary

		def run(wrong: int | None = None, zero: bool = True) -> dict:
			snapshots = []
			for number in range(1, 41):
				shown = number if number != wrong else number - 1
				snapshots.append({"label": f"public {number} closed", "displays": [{"index": 0, "segments": synthetic_display(f"{shown:02d}")}]})
				snapshots.append({"label": f"public {number} open", "displays": [{"index": 5, "segments": synthetic_display(" 0" if zero and number == 7 else "  ")}]})
			return {"snapshots": snapshots}

		self.assertEqual(list(range(1, 41)), summary.verify_switch_test(run()))
		with self.assertRaises(SystemExit):
			summary.verify_switch_test(run(wrong=40))
		with self.assertRaises(SystemExit):
			summary.verify_switch_test(run(zero=False))
		with self.assertRaises(SystemExit):
			summary.verify_switch_test({"snapshots": []})


class StarGazerDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = cls.definition["inputs"]
		cls.outputs = cls.definition["outputs"]
		cls.switches = {i["binding"]["device"]: i for i in cls.inputs if i["binding"]["group"] == "pinmame.input.switch"}
		cls.dips = {i["binding"]["device"]: i for i in cls.inputs if i["binding"]["group"] == "pinmame.input.dip"}
		cls.direct = {i["binding"]["device"]: i for i in cls.inputs if i["binding"]["group"] == "physical.input.direct"}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.outputs if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.outputs if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.summary = load(SUMMARY_PATH)
		cls.seed = load(SPATIAL_SEED)

	def test_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("stern.star-gazer.1980", machine["id"])
		self.assertEqual((2346, "GrZY2-ML0Rb", 1980, "Stern"), (machine["ipdb_id"], machine["opdb_id"], machine["year"], machine["manufacturer"]))
		self.assertEqual("pinmame.stern-mpu200", self.definition["controller"]["platform"])
		self.assertEqual({"stargzr", "stargzfp", "stargzrb"}, {d["id"] for d in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertNotIn("display_overrides", driver)

	def test_is_partial_with_exactly_the_named_blockers(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], coverage["missing"])
		self.assertEqual(1, len(self.definition["conflicts"]))
		conflict = self.definition["conflicts"][0]
		self.assertNotEqual("ignored", conflict.get("status"))
		self.assertIn("Resolution path:", conflict["description"])
		self.assertFalse((ROOT / "machines" / "author-ready" / "stern" / "star-gazer-1980.json").exists())

	def test_every_matrix_address_is_enumerated_and_used(self) -> None:
		self.assertEqual(set(range(1, 41)) | {-7, -6, -5, 81, 82, 83, 84}, set(self.switches))
		for number in range(1, 41):
			item = self.switches[number]
			self.assertEqual("used", item["availability"], number)
			self.assertIs(False, item["normally_closed"], number)
			self.assertEqual("MPU module A4", item["wiring"]["board"])
		self.assertEqual(set(range(1, 33)), set(self.dips))
		self.assertEqual({1, 2}, set(self.direct))
		for item in self.direct.values():
			self.assertIs(True, item["normally_closed"])

	def test_matrix_wiring_follows_strobe_and_return(self) -> None:
		strobes = ["A4J2-1", "A4J2-2", "A4J2-3", "A4J2-4", "A4J2-5"]
		returns = [f"A4J2-{n}" for n in range(8, 16)]
		for number in range(1, 41):
			wiring = self.switches[number]["wiring"]
			self.assertEqual(strobes[(number - 1) // 8], wiring["control_connection"], number)
			self.assertEqual(returns[(number - 1) % 8], wiring["return_connection"], number)

	def test_only_the_lower_flipper_buttons_are_used(self) -> None:
		self.assertEqual("used", self.switches[82]["availability"])
		self.assertEqual("used", self.switches[84]["availability"])
		self.assertEqual("unused", self.switches[81]["availability"])
		self.assertEqual("unused", self.switches[83]["availability"])
		self.assertIn("flipper.right.button", self.switches[82]["roles"])
		self.assertIn("flipper.left.button", self.switches[84]["roles"])

	def test_solenoid_addresses_and_printed_numbers(self) -> None:
		self.assertEqual(set(range(1, 16)) | {17, 18, 19, 20, 46, 48}, set(self.solenoids))
		self.assertNotIn(16, self.solenoids)
		for test, public in TEST_TO_PUBLIC.items():
			aliases = {(a["namespace"], a["value"]) for a in self.solenoids[public]["aliases"]}
			self.assertIn(("manual.self-test", str(test)), aliases, public)
			self.assertEqual(f"Q{test}", self.solenoids[public]["wiring"]["driver_transistor"], public)
		self.assertNotEqual(list(range(1, 20)), [TEST_TO_PUBLIC[n] for n in range(1, 20)])

	def test_runtime_summary_pairs_the_printed_numbers(self) -> None:
		observed = self.summary["runtime"]["observations"]["physical_service_solenoid_to_public"]
		self.assertEqual({str(k): v for k, v in TEST_TO_PUBLIC.items()}, observed)
		self.assertEqual(sorted(TEST_TO_PUBLIC.values()), self.summary["runtime"]["observations"]["solenoid_addresses_seen"])

	def test_used_and_unused_solenoids(self) -> None:
		for address, item in self.solenoids.items():
			if address in UNUSED_SOLENOIDS:
				self.assertEqual("unused", item["availability"], address)
				self.assertEqual("unused", item["spatial"]["reason"], address)
			else:
				self.assertEqual("used", item["availability"], address)
		self.assertIn("BALL KICKER", self.solenoids[20]["physical"]["notes"])
		self.assertIn("ENABLE REPLAY", self.solenoids[19]["physical"]["notes"])

	def test_gameplay_pairs_each_switch_with_its_coil(self) -> None:
		expected = {15: 1, 16: 2, 12: 5, 13: 11, 14: 8}
		runs = {item["label"]: item for item in self.summary["runtime"]["observations"]["named_action_observations"]}
		for switch, coil in expected.items():
			matches = [v for k, v in runs.items() if k.startswith(f"gameplay: public {switch} ")]
			self.assertEqual(1, len(matches), switch)
			self.assertEqual([coil], matches[0]["transitioned_solenoid_addresses"], switch)
		relationships = {r["source"]: r["destination"] for r in self.definition["relationships"] if r["kind"] == "direct"}
		for switch, coil in expected.items():
			self.assertEqual(self.solenoids[coil]["id"], relationships[self.switches[switch]["id"]], switch)

	def test_drop_bank_resets_follow_the_roms_pairing(self) -> None:
		runs = self.summary["runtime"]["observations"]["named_action_observations"]
		by_label = {item["label"]: item for item in runs}
		self.assertEqual([7], by_label["gameplay: lower-left 22-24: 24 down completes"]["transitioned_solenoid_addresses"])
		self.assertEqual([3], by_label["gameplay: upper-left 25-27: 27 down completes"]["transitioned_solenoid_addresses"])
		self.assertEqual([4], by_label["gameplay: right 28-30: 30 down completes"]["transitioned_solenoid_addresses"])
		self.assertEqual("device.left-drop-bank-reset", self.solenoids[7]["id"])
		self.assertEqual("device.upper-left-drop-bank-reset", self.solenoids[3]["id"])
		self.assertEqual("device.right-drop-bank-reset", self.solenoids[4]["id"])
		self.assertEqual({22, 23, 24}, self._bank_sensors("mechanism.lower-left-drop-bank"))
		self.assertEqual({25, 26, 27}, self._bank_sensors("mechanism.upper-left-drop-bank"))
		self.assertEqual({28, 29, 30}, self._bank_sensors("mechanism.right-drop-bank"))

	def _bank_sensors(self, mechanism_id: str) -> set[int]:
		mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == mechanism_id)
		by_id = {item["id"]: number for number, item in self.switches.items()}
		return {by_id[sensor] for sensor in mechanism["sensors"]}

	def test_flipper_enable_relay_gates_the_flippers(self) -> None:
		labels = {i["label"]: i for i in self.summary["runtime"]["observations"]["named_action_observations"]}
		self.assertEqual([19], labels["tilt: tilt switch 7 closed in play"]["transitioned_solenoid_addresses"])
		self.assertEqual([], labels["tilt: after the tilt: right flipper button 82"]["transitioned_solenoid_addresses"])
		self.assertEqual([], labels["flippers: attract: right flipper button 82"]["transitioned_solenoid_addresses"])
		self.assertIn(46, labels["flippers: in play: right flipper button 82"]["transitioned_solenoid_addresses"])
		self.assertIn(48, labels["flippers: in play: left flipper button 84"]["transitioned_solenoid_addresses"])
		kinds = {(r["id"], r["kind"]) for r in self.definition["relationships"]}
		self.assertIn(("rel.left-flipper", "relay_gated"), kinds)
		self.assertIn(("rel.right-flipper", "relay_gated"), kinds)

	def test_lamp_addresses_exclude_the_decoder_holes(self) -> None:
		self.assertEqual(set(LAMP_ADDRESSES), set(self.lamps))
		for hole in (16, 32, 48, 64):
			self.assertNotIn(hole, self.lamps)
		self.assertEqual(LAMP_ADDRESSES, self.summary["runtime"]["observations"]["lamp_addresses_seen"])

	def test_lamp_chart_is_read_row_by_row(self) -> None:
		"""Every chart row in the excerpt reaches the lamp whose connector pin and transistor it names."""
		text = (EXCERPTS / "schematic-lamp-chart.md").read_text(encoding="utf-8")
		rows = re.findall(r"^\| (?!DESCRIPTION|---)(.+?) \| (.+?) \| (J\d) \| (\d+) \| Q(\d+)( \*)? \|$", text, re.M)
		self.assertEqual(60, len(rows))
		by_connection = {}
		for lamp in self.lamps.values():
			for connection in lamp.get("wiring", {}).get("drive_connection", "").split(", "):
				if connection:
					by_connection[connection] = lamp
		for description, wire, jack, pin, transistor, star in rows:
			lamp = by_connection[f"LDA {jack}-{pin}"]
			self.assertEqual(wire, lamp["wiring"]["drive_wire"], description)
			if (description, jack, pin) == ("L. 3 FROM TOP STAR ROLL-OVER", "J1", "5"):
				transistor = "24"
			if (description, jack, pin) == ("L. 3 FROM TOP STAR ROLL-OVER", "J1", "5"):
				# The corrected row's type is deliberately unrecorded: chart and diagram disagree.
				self.assertEqual("Q24", lamp["wiring"]["driver_transistor"])
				self.assertIn("transistor type is not recorded", lamp["physical"]["notes"])
				continue
			self.assertTrue(lamp["wiring"]["driver_transistor"].startswith(f"Q{transistor} "), (description, lamp["wiring"]["driver_transistor"]))
			expected_type = "MCR106-1" if star else "2N5060"
			self.assertIn(expected_type, lamp["wiring"]["driver_transistor"], description)
		self.assertEqual(58, len({int(r[4]) for r in rows}))

	def test_lamps_24_and_25_cross_the_printed_pairing(self) -> None:
		self.assertTrue(self.lamps[24]["wiring"]["driver_transistor"].startswith("Q25"))
		self.assertEqual("Q24", self.lamps[25]["wiring"]["driver_transistor"])
		self.assertIn("3000", self.lamps[24]["label"])
		self.assertIn("star roll-over", self.lamps[25]["label"].lower())
		self.assertEqual("LDA J1-6", self.lamps[24]["wiring"]["drive_connection"])
		self.assertEqual("LDA J1-5", self.lamps[25]["wiring"]["drive_connection"])

	def test_zodiac_pairs_follow_the_rom(self) -> None:
		observed = self.summary["runtime"]["observations"]["switch_to_lamp"]
		self.assertEqual({str(k): v for k, v in ZODIAC_LAMP.items()}, observed)
		for switch, lamp in ZODIAC_LAMP.items():
			sign = SIGNS[lamp]
			self.assertIn(sign.lower(), self.switches[switch]["label"].lower(), switch)
			self.assertIn(sign.lower(), self.lamps[lamp]["label"].lower(), lamp)
			self.assertEqual("conflicted" if switch in (19, 20) else "validated", self.switches[switch]["provenance"]["status"], switch)

	def test_the_matrix_label_disagreement_is_recorded_on_both_switches(self) -> None:
		for switch, drawn in ((19, "SCORPIO"), (20, "LIBRA")):
			notes = self.switches[switch]["physical"]["notes"]
			self.assertIn("OPEN CONFLICT", notes)
			self.assertIn(drawn, notes)
			self.assertEqual("observed", self.switches[switch]["spatial"]["status"])
		matrix = (EXCERPTS / "schematic-switch-matrix.md").read_text(encoding="utf-8")
		self.assertIn('S.U. "SCORPIO" = 19', matrix)
		self.assertIn('S.U. "LIBRA" = 20', matrix)

	def test_unused_and_unplaced_lamps(self) -> None:
		self.assertEqual("unused", self.lamps[15]["availability"])
		self.assertEqual("unused", self.lamps[15]["spatial"]["reason"])
		for address in (31, 47):
			self.assertEqual("used", self.lamps[address]["availability"])
			self.assertNotIn("spatial", self.lamps[address], address)
		for address in (13, 45, 61, 63):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
			self.assertIn("cabinet.backglass", self.lamps[address]["roles"], address)

	def test_lamps_with_two_lights_have_two_placements_and_no_invented_quantity(self) -> None:
		for address in (9, 25, 41, 57):
			self.assertNotIn("quantity", self.lamps[address]["physical"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
			self.assertEqual("observed", self.lamps[address]["spatial"]["status"], address)
		self.assertNotIn("quantity", self.lamps[11]["physical"])
		self.assertEqual(1, len(self.lamps[11]["spatial"]["placements"]))
		self.assertEqual("LDA J1-26, LDA J2-21", self.lamps[11]["wiring"]["drive_connection"])
		for address, lamp in self.lamps.items():
			placements = lamp.get("spatial", {}).get("placements", [])
			if address not in (9, 25, 41, 57):
				self.assertLessEqual(len(placements), 1, address)

	def test_only_art_identified_lamp_placements_are_validated(self) -> None:
		art_identified = set(SIGNS) | {7, 23, 39, 55, 8, 24, 40, 56, 14, 30}
		for address, lamp in self.lamps.items():
			spatial = lamp.get("spatial", {})
			if spatial.get("status") in (None, "not_applicable"):
				continue
			self.assertEqual("validated" if address in art_identified else "observed", spatial["status"], address)
			for placement in spatial["placements"]:
				self.assertEqual(spatial["status"], placement["provenance"]["status"], address)

	def test_displays_are_seven_digit_player_displays(self) -> None:
		displays = {d["id"]: d for d in self.definition["displays"]}
		players = [displays[f"display.player-{n}-score"] for n in range(1, 5)]
		self.assertEqual([1, 9, 17, 25], [d["segment_start"] for d in players])
		self.assertEqual({7}, {d["width"] for d in players})
		self.assertEqual((35, 2), (displays["display.credits"]["segment_start"], displays["display.credits"]["width"]))
		self.assertEqual((38, 2), (displays["display.ball-in-play-match"]["segment_start"], displays["display.ball-in-play-match"]["width"]))

	def test_no_general_illumination_output_is_invented(self) -> None:
		self.assertEqual([], [o for o in self.outputs if o["kind"] == "gi"])
		self.assertIn("always on", KNOWLEDGE_PATH.read_text(encoding="utf-8"))

	def test_placements_are_the_frozen_table_objects(self) -> None:
		bounds = self.seed["bounds"]
		self.assertEqual((0.0, 0.0, 952.941, 1976.471), (bounds["left"], bounds["top"], bounds["right"], bounds["bottom"]))
		objects = self.seed["objects"]
		seen: set[str] = set()
		for collection in (self.inputs, self.outputs):
			for device in collection:
				for placement in device.get("spatial", {}).get("placements", []):
					self.assertNotIn(placement["id"], seen)
					seen.add(placement["id"])
					self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1)
					self.assertTrue(any(abs(o["x"] - placement["x"]) < 1e-9 and abs(o["y"] - placement["y"]) < 1e-9 for o in objects.values()), placement["id"])

	def test_each_switch_is_placed_on_the_object_the_script_binds(self) -> None:
		from star_gazer_spatial_seed import SWITCH_OBJECTS

		for number, (kind, name) in SWITCH_OBJECTS.items():
			item = self.switches[number]
			point = (self.seed["objects"][name]["x"], self.seed["objects"][name]["y"])
			placement = item["spatial"]["placements"][0]
			self.assertEqual(point, (placement["x"], placement["y"]), number)
		self.assertEqual("Drain", SWITCH_OBJECTS[33][1])
		for left, right in ((12, 13), (4, 5)):
			self.assertLess(self.switches[left]["spatial"]["placements"][0]["x"], self.switches[right]["spatial"]["placements"][0]["x"])
		self.assertLess(self.switches[22]["spatial"]["placements"][0]["y"], 1)
		self.assertGreater(self.switches[22]["spatial"]["placements"][0]["y"], self.switches[24]["spatial"]["placements"][0]["y"])

	def test_zodiac_arch_order_matches_the_table(self) -> None:
		placements = {n: self.switches[n]["spatial"]["placements"][0] for n in ZODIAC_LAMP}
		self.assertLess(placements[19]["x"], placements[20]["x"])
		self.assertLess(placements[20]["x"], placements[21]["x"])

	def test_callout_check_is_recomputed_from_its_seed(self) -> None:
		seed = load(CALLOUT_SEED)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		agreeing = {pid for pid, d in decisions["placements"].items() if d["agrees"]}
		self.assertEqual(35, len(agreeing))
		for collection in (self.inputs, self.outputs):
			for device in collection:
				for placement in device.get("spatial", {}).get("placements", []):
					if placement["id"] in decisions["placements"]:
						expected = "validated" if placement["id"] in agreeing else "observed"
						self.assertEqual(expected, placement["provenance"]["status"], placement["id"])
		self.assertEqual({"pdf-19", "pdf-21"}, set(seed["pages"]))
		self.assertNotIn("switch.libra-stand-up-target.sensor", decisions["placements"])
		self.assertNotIn("switch.scorpio-stand-up-target.sensor", decisions["placements"])

	def test_recorded_hashes_match_the_files(self) -> None:
		sources = {s["id"]: s for s in self.definition["sources"]}
		self.assertEqual(file_digest(SUMMARY_PATH), sources["runtime.star-gazer.harness"]["sha256"])
		self.assertEqual(file_digest(CALLOUT_SEED), sources["drawing-callouts.star-gazer.2026-10-02"]["sha256"])
		self.assertEqual("0cd28e0b807c9674727a1888c90d0c95697939c4db95a98cdace3a6738ccf8f8", sources["manual.stern.star-gazer.1980"]["sha256"])
		self.assertEqual("d99a94939a23cf00455eb19eb33f0019e62de1db0b6324c0082d0926c330109b", sources["schematic.stern.star-gazer.1980"]["sha256"])
		self.assertEqual("b15a49d6902164ae27b946b2f67d1c5682f92bd382288f2c94e2641045128085", sources["vpx-table.star-gazer.v2-0-0"]["sha256"])
		self.assertEqual(self.seed["table_sha256"], sources["vpx-table.star-gazer.v2-0-0"]["sha256"])

	def test_sibling_curators_leave_no_trace(self) -> None:
		"""No artifact names another Stern machine's short names, which a copied curator would carry.

		The forbidden set is built from the catalog; a hand-written blacklist only tests memory.
		Other manufacturers' short names are ordinary English words (``gemini``, ``raven``) and
		would match prose, so the set is restricted to Stern drivers.
		"""
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {d["id"] for d in catalog["drivers"] if d["machine_id"].startswith("stern.") and d["machine_id"] != self.definition["machine"]["id"]}
		self.assertIn("alifp", foreign)
		text = json.dumps(self.definition) + KNOWLEDGE_PATH.read_text(encoding="utf-8")
		tokens = set(re.findall(r"[a-z0-9_]{3,}", text))
		self.assertEqual(set(), tokens & foreign, "another Stern machine's driver ids appear in the artifacts")

	def test_curator_reproduces_the_artifacts(self) -> None:
		result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "curate_star_gazer.py"), "--check"], capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, result.returncode, result.stderr)

	def test_curator_detects_drift_in_an_isolated_copy(self) -> None:
		"""The drift check must fail on a tampered copy and pass on an untouched one, without writing into the checkout."""
		import tempfile

		report_json = ROOT / "reports" / "spatial" / "stern" / "star-gazer-1980.json"
		report_md = ROOT / "reports" / "spatial" / "stern" / "star-gazer-1980.md"
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			copies = {name: base / name for name in ("definition.json", "knowledge.md", "report.json", "report.md")}
			for name, source in zip(copies, (DEFINITION_PATH, KNOWLEDGE_PATH, report_json, report_md)):
				copies[name].write_bytes(source.read_bytes())
			command = [
				sys.executable, "-B", str(ROOT / "tools" / "curate_star_gazer.py"), "--check",
				"--definition", str(copies["definition.json"]), "--knowledge", str(copies["knowledge.md"]),
				"--report-json", str(copies["report.json"]), "--report-md", str(copies["report.md"]),
			]
			untouched = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertEqual(0, untouched.returncode, untouched.stderr)
			original = copies["definition.json"].read_bytes()
			copies["definition.json"].write_bytes(original.replace(b'"Star Gazer"', b'"Star Gazed"', 1))
			tampered = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertNotEqual(0, tampered.returncode)
			self.assertIn("canonical content mismatch", tampered.stderr)

	def test_excerpts_are_attached_to_their_bytes(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], file_digest(ROOT / excerpt["path"]), excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], file_digest(ROOT / excerpt["image"]), excerpt["id"])
					self.assertTrue(excerpt["reviewed"])

	def test_spatial_report_matches_the_definition(self) -> None:
		report = load(ROOT / "reports" / "spatial" / "stern" / "star-gazer-1980.json")
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(file_digest(DEFINITION_PATH), report["definition_sha256"])
		ids = {d["id"] for d in self.inputs + self.outputs}
		for disclosure in report["projection_disclosures"]:
			self.assertTrue(set(disclosure["devices"]) <= ids, disclosure["devices"])
		self.assertEqual({"lamp.left-b-1-lamp", "lamp.left-b-3-star-roll-lamp"}, {d["id"] for d in report["unplaced_physical_devices"]})
		self.assertEqual(self.definition["coverage"]["missing"], report["coverage"]["missing"])

	def test_conflict_names_both_pages_and_the_rom(self) -> None:
		conflict = self.definition["conflicts"][0]
		self.assertEqual({"schematic.stern.star-gazer.1980", "manual.stern.star-gazer.1980", "runtime.star-gazer.harness", "vpx-table.star-gazer.v2-0-0"}, set(conflict["source_refs"]))

	def test_runtime_summary_is_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		runs = Path(root) / "star-gazer-1980" / "harness"
		for run in self.summary["runtime"]["raw_runs"]:
			directory, driver = run["retained_from"].split("/harness/")[1].rsplit("/", 1)[0].split("/")
			path = runs / directory / driver / "run.json"
			self.assertTrue(path.is_file(), str(path))
			self.assertEqual(run["sha256"], file_digest(path), run["name"])
			if "scenario_path" in run:
				self.assertEqual(run["scenario_sha256"], file_digest(ROOT / run["scenario_path"]), run["name"])
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "star_gazer_runtime_summary.py"), "--runs", str(runs), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(self.summary["source"]["sha256"], check_manifest(runs, "stargzr"))

	def test_table_geometry_is_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		base = Path(root) / "stern" / "star-gazer-1980"
		vpx = base / "source" / "Star Gazer (Stern 1980) v2.0.0.vpx"
		self.assertEqual(self.seed["table_sha256"], file_digest(vpx))
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "star_gazer_spatial_seed.py"), "--extracted", str(base / "extracted-vpxtool"), "--vpx", str(vpx), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		for name, digest in {"stern.vbs": "b835ce5b0c11c6d268f58c92e534c1677e64cb47e103b33179b82c6c337be0e5", "core.vbs": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"}.items():
			self.assertEqual(digest, file_digest(base / "library" / name), name)

	def test_manuals_and_callout_renders_are_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		base = Path(root) / "by-machine" / "stern.star-gazer.1980"
		self.assertEqual("0cd28e0b807c9674727a1888c90d0c95697939c4db95a98cdace3a6738ccf8f8", file_digest(base / "ipdb" / "Stern_1980_Star_Gazer_Manual.pdf"))
		self.assertEqual("d99a94939a23cf00455eb19eb33f0019e62de1db0b6324c0082d0926c330109b", file_digest(base / "ipdb" / "Stern_1980_Star_Gazer_Schematic_Diagrams_paginated.pdf"))
		self.assertEqual("cdb1cb74b36841a16f09c26ed34ae4baaa34b94b20291c71ff3d3ea2aa1a51be", file_digest(base / "ipdb" / "ipdb-machine-2346.html"))
		artifacts = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		checked = drawing_callouts.verify_retained(load(CALLOUT_SEED), ROOT, Path(root), Path(artifacts) if artifacts else None)
		self.assertGreaterEqual(checked, 2)


if __name__ == "__main__":
	unittest.main()
