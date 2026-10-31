"""Gates for the Stern Nine Ball (1980) definition.

They lock down what was expensive to establish and cheap to lose: the physical-to-public solenoid mapping and the knock-down coil order the ROM's
own tests prove, the lamp decoder arithmetic with its two crossed SCR pairs, the game's own light list against the lamp-driver sheet's four
differing J2 pins, the option-switch reading the spinner probe settled and the one it could not, and the boundary between what the retained runs
measured and what they did not. Fixtures that restate a printed sheet are read from the committed excerpts, not from the curator's data module:
a test that checks the generator against its own input only proves the generator is self-consistent.
"""
from __future__ import annotations

import copy
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

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402

import curate_nine_ball as curator  # noqa: E402

DEFINITION_PATH = ROOT / "machines/partial/stern/nine-ball-1980.json"
SEED_PATH = ROOT / "tools/seeds/stern/nine-ball-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/nine-ball-1980.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/nine-ball-1980.json"
EXCERPTS = ROOT / "evidence/excerpts/stern.nine-ball.1980"
RUNTIME_PATH = ROOT / "evidence/runtime/stern/nine-ball-diagnostics-and-gameplay.json"
MACHINE_ID = "stern.nine-ball.1980"
DRIVER_IDS = {"nineball", "ninebafp", "ninebala", "ninebalb", "ninebalc", "ninebald"}
EXPECTED_MISSING = ["spatial_placement", "unresolved_conflicts"]
CABINET_SWITCHES = (1, 2, 3, 6, 7, 8)
TROUGH_SWITCHES = (33, 36, 37)
# Printed solenoid I.D. -> public address, from the ROM's solenoid test (retained run).
PHYSICAL_TO_PUBLIC = {1: 2, 2: 1, 3: 6, 4: 7, 5: 3, 6: 4, 7: 5, 8: 8, 9: 11, 10: 12, 11: 14, 12: 13, 13: 9, 14: 10, 15: 19, 16: 15, 17: 17, 18: 20, 19: 18}
# Public address -> the words its label must carry, from the printed solenoid table via that pairing.
SOLENOID_WORDS = {1: ("right", "slingshot"), 2: ("left", "slingshot"), 3: ("right", "bank", "reset"), 4: ("center", "bank", "reset"), 5: ("pop", "bumper"), 6: ("knocker",),
	7: ("outhole",), 8: ("kick-out",), 17: ("eight", "reset"), 18: ("coin",), 19: ("flipper", "relay"), 20: ("loop", "reset")}
BACKBOX_LAMPS = {13: "high score", 45: "game over", 61: "tilt", 63: "match"}
LAMPS_NOT_DRIVEN_IN_PLAY = {14, 15, 31}
SPINNER_LAMPS = (12, 28, 44, 60)
# Q number -> (jack, the light list's pin, the lamp-driver sheet's connector-block reading)
PIN_DISAGREEMENTS = {3: ("J2", 21, 2), 5: ("J2", 16, 6), 7: ("J2", 13, 3), 39: ("J2", 4, 1)}


def markdown_rows(path: Path) -> list[list[str]]:
	rows = []
	for line in path.read_text(encoding="utf-8").splitlines():
		if line.startswith("|") and not re.match(r"^\|\s*:?-+", line):
			rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
	return rows


def decoder_table() -> dict[int, int]:
	"""Public lamp address -> SCR number, read from the decoder excerpt (public = 16k + a + 1); every cell's resistor must end at its own SCR."""
	result: dict[int, int] = {}
	for row in markdown_rows(EXCERPTS / "lamp-driver-decoder-outputs.md"):
		match = re.match(r"^U(\d)$", row[0])
		if not match:
			continue
		chip = int(match.group(1)) - 1
		for output, cell in enumerate(row[1:]):
			resistor, transistor = re.match(r"^R(\d+) / Q(\d+)$", cell).groups()
			assert resistor == transistor, cell
			result[16 * chip + output + 1] = int(transistor)
	return result


def light_list() -> list[tuple[str, str, str, int, int]]:
	"""The game's own LDA LIGHT LOCATION rows: description, wire, jack, pin, SCR."""
	return [(row[0], row[1], row[2], int(row[3]), int(row[4][1:])) for row in markdown_rows(EXCERPTS / "lda-light-location.md") if re.match(r"^Q\d+$", row[-1])]


def connector_entries() -> dict[str, list[tuple[int, int]]]:
	"""jack -> [(pin as read, SCR)] from the lamp-driver sheet's connector blocks."""
	entries: dict[str, list[tuple[int, int]]] = {}
	jack = None
	for line in (EXCERPTS / "lamp-driver-connector-labels.md").read_text(encoding="utf-8").splitlines():
		match = re.match(r"^`(J\d)`:$", line)
		if match:
			jack = match.group(1)
			continue
		match = re.match(r"^\| (\d+)[^|]* \| [^|]+ \| Q(\d+) \|$", line)
		if match and jack:
			entries.setdefault(jack, []).append((int(match.group(1)), int(match.group(2))))
	return entries


class NineBallDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		group = lambda name: {item["binding"]["device"]: item for item in cls.definition["inputs"] + cls.definition["outputs"] if item["binding"]["group"] == name}
		cls.switches = group("pinmame.input.switch")
		cls.dips = group("pinmame.input.dip")
		cls.direct = group("physical.input.direct")
		cls.solenoids = group("pinmame.output.solenoid")
		cls.lamps = group("pinmame.output.lamp")
		cls.gi = group("physical.output.gi")
		cls.runtime = load_json(RUNTIME_PATH)
		cls.observations = cls.runtime["runtime"]["observations"]

	def test_deterministic_artifacts_match_the_curator(self) -> None:
		curator.check(ROOT)
		self.assertEqual(canonical_bytes(self.definition), SEED_PATH.read_bytes())

	def test_identity_and_driver_group(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((machine["id"], machine["name"], machine["year"], machine["ipdb_id"], machine["model_number"], machine["opdb_id"]),
			(MACHINE_ID, "Nine Ball", 1980, 1678, "125", "G4jjx-MDbz2"))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(set(drivers), DRIVER_IDS)
		self.assertNotIn("clone_of", drivers["nineball"])
		for identifier in DRIVER_IDS - {"nineball"}:
			self.assertEqual(drivers[identifier]["clone_of"], "nineball")
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in drivers.values()))
		self.assertEqual({identifier: drivers[identifier]["year"] for identifier in ("ninebala", "ninebalb", "ninebalc", "ninebald")},
			{"ninebala": "2020", "ninebalb": "2007", "ninebalc": "2021", "ninebald": "2021"})
		for identifier in ("ninebala", "ninebalc", "ninebald"):
			self.assertIn("no harness run was made", drivers[identifier]["variant_notes"])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") == MACHINE_ID}
		self.assertEqual(claimed, DRIVER_IDS)
		record = next(item for item in catalog["machines"] if item["id"] == MACHINE_ID)
		self.assertEqual(record["missing"], EXPECTED_MISSING)
		self.assertFalse((ROOT / "machines/stubs/stern/nine-ball-1980.json").exists())

	def test_coverage_is_partial_with_exactly_the_documented_blockers(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual(coverage["status"], "partial")
		self.assertEqual(coverage["missing"], EXPECTED_MISSING)
		self.assertFalse((ROOT / "machines/author-ready/stern/nine-ball-1980.json").exists())
		conflicts = unresolved_conflicts(self.definition)
		self.assertEqual([conflict["id"] for conflict in conflicts], ["conflict.option-switch-8-background-sound-setting"])
		self.assertIn("Resolution path:", conflicts[0]["description"])
		self.assertEqual(self.dips[8]["provenance"]["status"], "conflicted")
		self.assertEqual({address for address, item in self.dips.items() if item["provenance"]["status"] != "validated"}, {8})

	def test_every_matrix_address_is_enumerated_named_and_normally_open(self) -> None:
		self.assertEqual(set(self.switches), {-7, -6, -5, *range(1, 41), 81, 82, 83, 84})
		printed = {int(row[0]): row for row in markdown_rows(EXCERPTS / "switch-identification.md") if row[0].isdigit()}
		self.assertEqual(set(printed), set(range(1, 41)))
		for address in range(1, 41):
			item = self.switches[address]
			self.assertEqual(item["availability"], "used", address)
			self.assertIs(item["normally_closed"], False, address)
			self.assertIn(f"`{printed[address][3]}`", item["physical"]["notes"], address)
			self.assertTrue(item["wiring"]["return_connection"].endswith(printed[address][2]), address)
			# The table prints the single-colour O and Y returns as `-O-` and `-Y-`.
			self.assertEqual(item["wiring"]["return_wire"], printed[address][1].strip("-"), address)
			self.assertEqual("NO DIODE" in item["physical"]["notes"], address in (1, 2, 3), address)
			self.assertEqual(".05 capacitor" in item["physical"]["notes"], printed[address][4] == "filled dot", address)
		self.assertEqual({address for address in range(1, 41) if self.switches[address].get("initial_active")}, set(TROUGH_SWITCHES))
		self.assertEqual({address for address in (81, 82, 83, 84) if self.switches[address]["availability"] == "unused"}, {81, 83})

	def test_switch_wiring_follows_the_strobe_and_return_arithmetic(self) -> None:
		for address in range(1, 41):
			wiring = self.switches[address]["wiring"]
			strobe, row = divmod(address - 1, 8)
			if address in CABINET_SWITCHES:
				self.assertEqual((wiring["control_wire"], wiring["control_connection"]), ("R-Y", "J3-3"))
				self.assertEqual(wiring["return_connection"], f"J3-{9 + row}")
			else:
				self.assertEqual(wiring["control_connection"], f"A4J2-{strobe + 1}")
				self.assertEqual(wiring["return_connection"], f"A4J2-{8 + row}")

	def test_switch_test_shows_every_address_as_its_own_number(self) -> None:
		note = self.observations["runs"]["switch-test"]["note"]
		for address in range(1, 41):
			self.assertIn(f" {address}->{address},", note.replace("40->40.", "40->40,"))

	def test_solenoid_translation_matches_the_printed_table_and_the_rom_test(self) -> None:
		printed = {int(row[0]): row for row in markdown_rows(EXCERPTS / "solenoid-identification.md") if row[0].isdigit()}
		self.assertEqual(set(printed), set(range(1, 20)))
		mapping = {int(key): value for key, value in self.observations["physical_service_solenoid_to_public"].items()}
		self.assertEqual(mapping, PHYSICAL_TO_PUBLIC)
		for physical, public in mapping.items():
			item = self.solenoids[public]
			_, transistor, jack, wire, description = printed[physical]
			self.assertIn({"namespace": "manual.self-test", "value": str(physical)}, item["aliases"])
			self.assertEqual(item["wiring"]["driver_transistor"], transistor)
			self.assertEqual(item["wiring"]["drive_connection"], f"A3{jack}")
			self.assertEqual(item["wiring"]["drive_wire"], wire)
			self.assertIn(f"`{description}`", item["physical"]["notes"])
			self.assertEqual(item["availability"], "used")
		for public, words in SOLENOID_WORDS.items():
			label = self.solenoids[public]["label"].lower()
			self.assertTrue(all(word in label for word in words), (public, label))
		self.assertNotIn(16, self.solenoids)
		self.assertEqual(self.observations["public_solenoid_decoder_holes_not_seen"], [16])

	def test_knock_down_coils_are_public_sixteen_minus_the_object(self) -> None:
		printed = {int(row[0]): row[4] for row in markdown_rows(EXCERPTS / "solenoid-identification.md") if row[0].isdigit()}
		relationships = {(item["source"], item["destination"]): item["kind"] for item in self.definition["relationships"]}
		for physical, description in printed.items():
			match = re.match(r"^DROP TARGET #(\d)$", description)
			if not match:
				continue
			number = int(match.group(1))
			public = PHYSICAL_TO_PUBLIC[physical]
			self.assertEqual(public, 16 - number, description)
			coil = self.solenoids[public]
			self.assertEqual(coil["label"], f"Drop target {number} knock-down coil")
			self.assertEqual(relationships[(coil["id"], self.switches[8 + number]["id"])], "pulse")
		knock_downs = sorted(int(re.match(r"^Drop target (\d) knock-down coil$", item["label"]).group(1)) for item in self.solenoids.values() if "knock-down" in item["label"])
		self.assertEqual(knock_downs, list(range(1, 8)))

	def test_continuous_outputs_and_flipper_relay(self) -> None:
		for address in (17, 20):
			self.assertEqual(self.solenoids[address]["kind"], "coil")
			self.assertIn("continuous-section driver", self.solenoids[address]["physical"]["notes"])
		self.assertEqual(self.solenoids[18]["spatial"]["reason"], "cabinet_or_service")
		self.assertEqual(self.solenoids[6]["spatial"]["reason"], "cabinet_or_service")
		self.assertEqual((self.solenoids[19]["kind"], self.solenoids[19]["spatial"]["reason"]), ("relay", "internal_nonvisual"))
		self.assertIn("which the run does not explain", self.solenoids[20]["physical"]["notes"])
		self.assertNotIn("part_number", self.solenoids[20]["physical"])

	def test_lamp_addresses_follow_the_decoder_and_the_games_own_light_list(self) -> None:
		decoder = decoder_table()
		self.assertEqual(set(decoder), {*range(1, 16), *range(17, 32), *range(33, 48), *range(49, 64)})
		self.assertEqual(sorted(decoder.values()), list(range(1, 61)))
		self.assertEqual(set(self.lamps), set(decoder))
		q_to_public = {q: public for public, q in decoder.items()}
		rows = light_list()
		self.assertEqual(len(rows), 60)
		self.assertEqual(sorted(q for *_, q in rows), list(range(1, 61)))
		for description, wire, jack, pin, q in rows:
			lamp = self.lamps[q_to_public[q]]
			self.assertEqual(lamp["wiring"]["drive_connection"], f"A5{jack}-{pin}", description)
			self.assertEqual(lamp["wiring"]["drive_wire"], wire, description)
			self.assertEqual(lamp["wiring"]["driver_transistor"], f"Q{q}", description)
			self.assertIn(f"`{description}`", lamp["physical"]["notes"])
			self.assertEqual(lamp["availability"], "used")
		self.assertEqual(self.observations["lamp_decoder_holes_not_seen"], [16, 32, 48, 64])

	def test_the_four_connector_pin_readings_follow_the_light_list(self) -> None:
		entries = connector_entries()
		listed = {(jack, pin, q) for _, _, jack, pin, q in light_list()}
		drawn = {(jack, pin, q) for jack, values in entries.items() for pin, q in values}
		self.assertEqual({q for jack, pin, q in listed - drawn}, set(PIN_DISAGREEMENTS))
		decoder = decoder_table()
		q_to_public = {q: public for public, q in decoder.items()}
		for q, (jack, listed_pin, drawn_pin) in PIN_DISAGREEMENTS.items():
			self.assertIn((jack, listed_pin, q), listed)
			self.assertIn((jack, drawn_pin, q), drawn)
			lamp = self.lamps[q_to_public[q]]
			self.assertEqual(lamp["wiring"]["drive_connection"], f"A5{jack}-{listed_pin}")
			self.assertIn(f"prints this SCR on {jack} pin {drawn_pin}", lamp["physical"]["notes"])
		self.assertEqual(sum("connector block prints this SCR" in lamp["physical"]["notes"] for lamp in self.lamps.values()), 4)

	def test_the_crossed_scr_pairs_and_the_roms_object_lamps(self) -> None:
		decoder = decoder_table()
		self.assertEqual((decoder[24], decoder[25]), (25, 24))
		self.assertEqual((decoder[42], decoder[58]), (41, 46))
		named = {int(key.split("-")[3]): value for key, value in self.observations["named_output_addresses"].items()}
		self.assertEqual(named, {1: 58, 2: 42, 3: 26, 4: 10, 5: 57, 6: 41, 7: 25})
		by_q = {q: description for description, _, _, _, q in light_list()}
		for index, public in named.items():
			self.assertTrue(by_q[decoder[public]].startswith(f"BONUS TARGET {index}"), (index, public))
			self.assertIn(f"lamp lit for object {index}", self.lamps[public]["physical"]["notes"])

	def test_backbox_lamps_and_lamps_not_driven_in_play(self) -> None:
		for public, words in BACKBOX_LAMPS.items():
			lamp = self.lamps[public]
			self.assertIn(words, lamp["label"].lower())
			self.assertEqual(lamp["spatial"]["reason"], "cabinet_or_service")
			self.assertNotIn("backglass light", lamp["physical"]["notes"])
		outside = set(self.observations["lamp_addresses_driven_outside_self_test"])
		self.assertEqual(set(self.lamps) - outside, LAMPS_NOT_DRIVEN_IN_PLAY)
		for public in LAMPS_NOT_DRIVEN_IN_PLAY:
			self.assertEqual(self.lamps[public]["availability"], "used")
			self.assertIn("no play run lit it", self.lamps[public]["physical"]["notes"])
		for public in set(self.lamps) - set(BACKBOX_LAMPS):
			self.assertNotIn("spatial", self.lamps[public], public)
		self.assertEqual([self.lamps[public]["label"] for public in SPINNER_LAMPS], [f"Spinner value {n}" for n in range(1, 5)])
		self.assertEqual(self.lamps[27]["label"], "Shoot Again")

	def test_flippers_one_per_side(self) -> None:
		for address in (46, 48):
			self.assertEqual(self.solenoids[address]["physical"]["quantity"], 1)
			self.assertNotIn("manual.self-test", {alias["namespace"] for alias in self.solenoids[address]["aliases"]})
		for address in (1, 2):
			self.assertEqual(self.direct[address]["physical"]["quantity"], 1)
			self.assertIs(self.direct[address]["normally_closed"], True)
		self.assertIs(self.direct[3]["normally_closed"], False)
		self.assertEqual((self.solenoids[45]["kind"], self.solenoids[47]["kind"]), ("virtual", "virtual"))
		left, right = self.solenoids[48]["spatial"]["placements"], self.solenoids[46]["spatial"]["placements"]
		self.assertTrue(all(placement["x"] < 0.5 for placement in left) and all(placement["x"] > 0.5 for placement in right))

	def test_option_switches_and_the_spinner_probe(self) -> None:
		self.assertEqual(set(self.dips), set(range(1, 33)))
		self.assertTrue(all(item["availability"] == "used" for item in self.dips.values()))
		self.assertIn("OFF = the center targets", self.dips[17]["label"])
		self.assertIn(curator.SPINNER_OPTION_SOURCE, self.dips[17]["provenance"]["source_refs"])
		note = self.observations["runs"]["spinner-option"]["note"]
		for fragment in ("center target 19 down -> [12]", "center target 23 down -> [28]", "outside target 18 down -> []", "outside target 22 down -> []"):
			self.assertIn(fragment, note)
		self.assertIn("not attributed", note)
		self.assertIn("Balls per game (ON = 5, OFF = 3)", self.dips[7]["label"])

	def test_mechanisms_name_existing_devices_and_each_actuator_once(self) -> None:
		devices = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		actuators = []
		for mechanism in self.definition["mechanisms"]:
			for reference in mechanism["actuators"] + mechanism["sensors"]:
				self.assertIn(reference, devices, mechanism["id"])
			actuators += mechanism["actuators"]
		self.assertEqual(len(actuators), len(set(actuators)))
		for relationship in self.definition["relationships"]:
			self.assertIn(relationship["source"], devices)
			self.assertIn(relationship["destination"], devices)
		eight_bank = next(item for item in self.definition["mechanisms"] if item["id"] == "mech.eight-target-bank")
		self.assertEqual(len(eight_bank["actuators"]), 8)
		self.assertEqual(len(eight_bank["sensors"]), 8)

	def test_displays_match_the_pinned_dispst7_layout(self) -> None:
		layout = [(item["controller_index"], item["segment_start"], item["width"]) for item in self.definition["displays"]]
		self.assertEqual(layout, [(0, 1, 7), (1, 9, 7), (2, 17, 7), (3, 25, 7), (4, 35, 2), (5, 38, 2)])

	def test_excerpts_are_pinned_and_present(self) -> None:
		count = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				count += 1
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"])
		self.assertEqual(count, len(list(EXCERPTS.glob("*.md"))))
		self.assertEqual(count, 19)
		self.assertEqual(len(list(EXCERPTS.glob("*.webp"))), 10)

	def test_spatial_report_states_the_blockers(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(report["readiness"]["missing"], EXPECTED_MISSING)
		self.assertEqual(report["readiness"]["unresolved_conflicts"], 1)
		unplaced = {(item["group"], item["address"]) for item in report["unplaced_records"]}
		expected = {("pinmame.output.lamp", address) for address in set(self.lamps) - set(BACKBOX_LAMPS)}
		expected |= {("pinmame.input.switch", address) for address in TROUGH_SWITCHES} | {("pinmame.output.solenoid", 7)}
		self.assertEqual(unplaced, expected)
		self.assertTrue(any("No playfield lamp is placed (56 of the 60)" in blocker for blocker in report["blockers"]))

	def test_every_placement_is_observed_and_inside_the_playfield(self) -> None:
		for collection in ("inputs", "outputs"):
			for item in self.definition[collection]:
				for placement in (item.get("spatial") or {}).get("placements", []):
					self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
					self.assertEqual(placement["provenance"]["status"], "observed", placement["id"])
		for address in range(1, 41):
			spatial = self.switches[address].get("spatial")
			if address in CABINET_SWITCHES:
				self.assertEqual(spatial["reason"], "cabinet_or_service")
			elif address in TROUGH_SWITCHES:
				self.assertIsNone(spatial)
			else:
				self.assertEqual(len(spatial["placements"]), 1, address)
		self.assertNotIn("spatial", self.solenoids[7])
		gi = self.gi[1]
		self.assertEqual(len(gi["spatial"]["placements"]), 25)
		self.assertNotIn("quantity", gi["physical"])
		# The lock lane: 39 sits above 38, which sits above the kick-out hole.
		y = lambda item: item["spatial"]["placements"][0]["y"]
		self.assertLess(y(self.switches[39]), y(self.switches[38]))
		self.assertLess(y(self.switches[38]), y(self.switches[34]))

	def test_knowledge_note_states_the_blockers_and_the_translations(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("1->2, 2->1, 3->6, 4->7", "16 * k + a + 1", "public 58, 42, 26, 10, 57, 41 and 25", "Page 11 is right", "unresolved conflict",
				"## What would complete the record", "`sw38` writes switch 39"):
			self.assertIn(phrase, text)

	def test_no_other_machines_leak_into_the_artifacts(self) -> None:
		catalog = load_json(ROOT / "catalog/pinmame.json")
		forbidden = {machine["id"] for machine in catalog["machines"]} - {MACHINE_ID}
		# Short names of every other Stern driver, the family a copied sibling record would come from (other makers' names include plain words).
		forbidden |= {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") != MACHINE_ID and str(driver.get("machine_id", "")).startswith("stern.")}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		tokens = set()
		for text in texts:
			tokens |= set(re.findall(r"[a-z0-9][a-z0-9_.-]*[a-z0-9]", text))
		self.assertFalse(tokens & forbidden, sorted(tokens & forbidden)[:10])

	def test_sources_are_complete_and_pinned(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		for identifier in (curator.MANUAL_SOURCE, curator.SCHEMATIC_SOURCE, curator.IPDB_SOURCE, curator.SCRIPT_SOURCE, curator.STANDALONE_SOURCE, curator.TABLE_SOURCE,
				curator.TABLE_SCRIPT_SOURCE, curator.EXTRACTION_SOURCE, *curator.RUN_SOURCES.values()):
			self.assertIn(identifier, sources)
		self.assertEqual(sources[curator.SCRIPT_SOURCE]["sha256"], "ba079814b12d95496cb893954386092009da7aa14c413feebc2e941ebdde8d78")
		self.assertEqual(sources[curator.STANDALONE_SOURCE]["sha256"], "53e98ab906854109115f19f4d006f8c7c65c6b9e38cf2446198460733bcddfa8")
		self.assertTrue(sources[curator.SCRIPT_SOURCE]["known_working"] and sources[curator.STANDALONE_SOURCE]["known_working"])
		self.assertEqual(sources[curator.TABLE_SOURCE]["sha256"], "fdd7e6c53a9046e29d96b4acbbf01743d892447851b28f880df5367af2759270")
		self.assertEqual(sources[curator.EXTRACTION_SOURCE]["sha256"], curator.EXTRACTION_MANIFEST_SHA256)
		runs = {run["name"]: run for run in self.runtime["runtime"]["raw_runs"]}
		self.assertEqual(list(runs), list(curator.RUN_SOURCES))
		for name, identifier in curator.RUN_SOURCES.items():
			self.assertEqual(sources[identifier]["sha256"], runs[name]["sha256"])
			scenario = ROOT / runs[name]["scenario_path"]
			self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), runs[name]["scenario_sha256"], name)
			self.assertNotIn(b"\r\n", scenario.read_bytes(), name)
			self.assertEqual(curator.RUN_AT[name], sources[identifier]["acquired_at"], name)
		self.assertEqual({source["kind"] for identifier, source in sources.items() if identifier in curator.RUN_SOURCES.values()}, {"service_diagnostic", "runtime_scenario"})
		for identifier, source in sources.items():
			self.assertRegex(source.get("acquired_at", ""), r"^20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$", identifier)


class NineBallRetainedEvidenceTests(unittest.TestCase):
	"""Exact retained artifacts, checked only when the external roots are configured."""

	@staticmethod
	def _harness_root() -> Path | None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		return Path(root) / "nine-ball-1980" / "harness" if root else None

	def test_harness_runs_reproduce_the_runtime_summary(self) -> None:
		runs_root = self._harness_root()
		if runs_root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_nine_ball_runtime as summary
		self.assertEqual(canonical_bytes(summary.build(runs_root)), RUNTIME_PATH.read_bytes())

	def test_a_substituted_display_frame_is_refused(self) -> None:
		runs_root = self._harness_root()
		if runs_root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_nine_ball_runtime as summary
		original = summary._load_run

		def substituted(root: Path, name: str):
			run = original(root, name)
			if name == "switch-test":
				run = copy.deepcopy(run)
				snapshot = next(item for item in run["snapshots"] if item["label"] == "close 5")
				segments = snapshot["displays"][0]["segments"]
				# Show 6 where the ROM showed 5: same digit count, a different frame.
				index = next(position for position, word in enumerate(segments) if word & 0x7F == 0x6D)
				segments[index] = (segments[index] & 0x80) | 0x7D
			return run

		with mock.patch.object(summary, "_load_run", substituted):
			with self.assertRaisesRegex(RuntimeError, "does not carry the frame"):
				summary.build(runs_root)
		# A solenoid-test run whose cited frames were blanked cannot keep the pinned driver numbers either.
		solenoid = copy.deepcopy(original(runs_root, "solenoid-test"))
		last = summary.self_test_presses(solenoid)[-1]
		for event in solenoid["events"]:
			if event["event"] == "display" and event.get("index") == 0 and event["time_s"] > last and "segments" in event:
				event["segments"] = [0x00] * len(event["segments"])
		with self.assertRaisesRegex(RuntimeError, "does not carry the frame"):
			summary.solenoid_test_pairs(solenoid)

	def test_ipdb_page_matches_its_pinned_hash(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		page = Path(root) / "nine-ball-1980" / "ipdb" / "machine-1678.html"
		self.assertEqual(hashlib.sha256(page.read_bytes()).hexdigest(), curator.IPDB_PAGE_SHA256)

	def test_retained_table_extraction_and_coordinates(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		import nine_ball_data as data
		from pinmame_game_defs.spatial import _item_point
		folder = Path(root) / curator.TABLE_RELATIVE
		table = folder / curator.TABLE_FILENAME
		self.assertEqual(table.stat().st_size, curator.TABLE_BYTES)
		self.assertEqual(hashlib.sha256(table.read_bytes()).hexdigest(), curator.TABLE_SHA256)
		curator.verify_extraction_manifest(Path(root))
		extraction = Path(root) / curator.EXTRACTION_RELATIVE
		self.assertEqual(hashlib.sha256((extraction / "script.vbs").read_bytes()).hexdigest(), curator.TABLE_SCRIPT_SHA256)
		bounds = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
		self.assertEqual((bounds["left"], bounds["top"], bounds["right"], bounds["bottom"]), (0.0, 0.0, data.TABLE_WIDTH, data.TABLE_HEIGHT))
		for name, (item_type, x, y, file) in data.OBJECTS.items():
			document = json.loads((extraction / "gameitems" / file).read_text(encoding="utf-8"))
			self.assertEqual(next(iter(document)), item_type, name)
			value = document[item_type]
			self.assertEqual(value["name"], name)
			self.assertAlmostEqual(_item_point(item_type, value)[0], x, places=4, msg=name)
			self.assertAlmostEqual(_item_point(item_type, value)[1], y, places=4, msg=name)
		for name, (x, y, light) in data.GI_BULBS.items():
			primitive = json.loads((extraction / "gameitems" / f"Primitive.{name}.json").read_text(encoding="utf-8"))["Primitive"]
			self.assertAlmostEqual(primitive["position"]["x"], x, places=3, msg=name)
			self.assertAlmostEqual(primitive["position"]["y"], y, places=3, msg=name)
			bulb = json.loads((extraction / "gameitems" / f"Light.{light}.json").read_text(encoding="utf-8"))["Light"]
			self.assertLess(((bulb["center"]["x"] - x) ** 2 + (bulb["center"]["y"] - y) ** 2) ** 0.5, 16, name)
		lights = [json.loads(path.read_text(encoding="utf-8"))["Light"] for path in (extraction / "gameitems").glob("Light.*.json")]
		self.assertEqual(len(lights), 188)
		self.assertFalse(any(light.get("show_bulb_mesh") for light in lights))

	def test_retained_documents_match_their_pinned_hashes(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("PINMAME_MANUALS_ROOT is not set")
		folder = Path(root) / "by-machine" / MACHINE_ID / "ipdb"
		for name, digest in ((curator.MANUAL_PDF, curator.MANUAL_SHA256), (curator.SCHEMATIC_PDF, curator.SCHEMATIC_SHA256)):
			self.assertEqual(hashlib.sha256((folder / name).read_bytes()).hexdigest(), digest, name)

	def test_rom_archives_match_the_runs(self) -> None:
		root = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
		if not root:
			self.skipTest("user-authorized ROM library root is not configured")
		for driver, digest in curator.ROM_ARCHIVES.items():
			self.assertEqual(hashlib.sha256((Path(root) / f"{driver}.zip").read_bytes()).hexdigest(), digest, driver)
		for driver in ("ninebala", "ninebalc", "ninebald"):
			self.assertFalse((Path(root) / f"{driver}.zip").exists(), driver)


if __name__ == "__main__":
	unittest.main()
