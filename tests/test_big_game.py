"""Gates for the Stern Big Game (1980) definition.

They lock down what was expensive to establish and cheap to lose: the lamp decoder arithmetic and the SCR pairs that are easy to transpose,
the physical-to-public solenoid mapping the ROM's own test proves, the seven physically identical drivers, the two continuous outputs whose
treatment differs, and the boundary between what the retained runs measured and what they did not. Fixtures that restate a printed sheet are
read from the committed excerpts, not from the curator's data module: a test that checks the generator against its own input only proves the
generator is self-consistent.
"""
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

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402

import curate_big_game as curator  # noqa: E402

DEFINITION_PATH = ROOT / "machines/partial/stern/big-game-1980.json"
SEED_PATH = ROOT / "tools/seeds/stern/big-game-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/big-game-1980.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/big-game-1980.json"
EXCERPTS = ROOT / "evidence/excerpts/stern.big-game.1980"
RUNTIME_PATH = ROOT / "evidence/runtime/stern/big-game-diagnostics-and-gameplay.json"
MACHINE_ID = "stern.big-game.1980"
DRIVER_IDS = {"biggame", "biggamfp", "biggameb", "biggamec", "biggamed", "biggamee", "biggamef"}
EXPECTED_MISSING = ["output_semantics", "spatial_placement"]
# Public address -> the words the device label must carry, from the printed Solenoid Identification list via the ROM's test pairing.
SOLENOID_WORDS = {1: ("top", "thumper"), 2: ("lower", "left", "thumper"), 3: ("lower", "right", "thumper"), 4: ("left", "slingshot"), 5: ("right", "slingshot"),
	6: ("knocker",), 7: ("top", "left", "bank"), 8: ("top", "right", "bank"), 9: ("lower", "right", "bank"), 10: ("saucer",), 11: ("out-hole",), 18: ("coin",), 19: ("flipper", "relay")}
UNUSED_SOLENOIDS = {12, 13, 14, 15, 17}
UNUSED_LAMPS = {14, 15, 31, 47}
BACKBOX_LAMPS = {13: "high score", 45: "game over", 61: "tilt", 63: "match"}
LETTER_LAMPS = {42: "b", 26: "i", 10: "g", 57: "g", 41: "a", 25: "m", 9: "e"}


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
			key = (jack, int(match.group(1)))
			if key in table:
				raise AssertionError(f"duplicate connector row {key}")
			table[key] = int(match.group(2))
		# a colliding J1 row with a settled reading: | Q24 | <as printed> | 5 |
		match = re.match(r"^\| Q(\d+) \| [^|]+ \| (\d+) \|$", line)
		if match:
			key = ("J1", int(match.group(2)))
			if key in table:
				raise AssertionError(f"a colliding row's reading reuses a pin: {key}")
			table[key] = int(match.group(1))
	return table


def decoder_table() -> dict[int, int]:
	"""Public lamp address -> SCR number, read from the decoder excerpt (public = 16k + a + 1)."""
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


def lamp_list() -> list[tuple[str, str, str, int]]:
	return [(row[1], row[2], row[3], int(row[4])) for row in markdown_rows(EXCERPTS / "lamp-driver-lamp-list.md") if row[0].isdigit()]


class BigGameDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		group = lambda name: {item["binding"]["device"]: item for item in cls.definition["inputs"] + cls.definition["outputs"] if item["binding"]["group"] == name}
		cls.switches = group("pinmame.input.switch")
		cls.dips = group("pinmame.input.dip")
		cls.direct = group("physical.input.direct")
		cls.solenoids = group("pinmame.output.solenoid")
		cls.lamps = group("pinmame.output.lamp")
		cls.runtime = load_json(RUNTIME_PATH)

	def test_deterministic_artifacts_match_the_curator(self) -> None:
		curator.check(ROOT)
		self.assertEqual(canonical_bytes(self.definition), SEED_PATH.read_bytes())

	def test_identity_and_driver_group(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((machine["id"], machine["name"], machine["year"], machine["ipdb_id"], machine["model_number"]), (MACHINE_ID, "Big Game", 1980, 249, "121"))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(set(drivers), DRIVER_IDS)
		self.assertNotIn("clone_of", drivers["biggame"])
		for identifier in DRIVER_IDS - {"biggame"}:
			self.assertEqual(drivers[identifier]["clone_of"], "biggame")
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in drivers.values()))
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") == MACHINE_ID}
		self.assertEqual(claimed, DRIVER_IDS)

	def test_coverage_is_partial_with_exactly_the_documented_blockers(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual(coverage["status"], "partial")
		self.assertEqual(coverage["missing"], EXPECTED_MISSING)
		self.assertFalse(unresolved_conflicts(self.definition))
		self.assertFalse((ROOT / "machines/author-ready/stern/big-game-1980.json").exists())

	def test_every_matrix_address_is_enumerated_named_and_normally_open(self) -> None:
		self.assertEqual(set(self.switches), {-7, -6, -5, *range(1, 41), 81, 82, 83, 84})
		printed = {int(row[0]): row[1] for row in markdown_rows(EXCERPTS / "switch-identification.md") if row[0].isdigit()}
		printed.update({int(row[2]): row[3] for row in markdown_rows(EXCERPTS / "switch-identification.md") if len(row) > 3 and row[2].isdigit()})
		self.assertEqual(set(printed), set(range(1, 41)))
		for address in range(1, 41):
			item = self.switches[address]
			self.assertEqual(item["availability"], "used", address)
			self.assertIs(item["normally_closed"], False, address)
			self.assertIn(f"`{printed[address]}`", item["physical"]["notes"], address)
		self.assertTrue(self.switches[33]["initial_active"])
		self.assertEqual({address for address in (81, 83) if self.switches[address]["availability"] == "unused"}, {81, 83})

	def test_switch_wiring_follows_the_strobe_and_return_arithmetic(self) -> None:
		for address in range(1, 41):
			wiring = self.switches[address]["wiring"]
			strobe, row = divmod(address - 1, 8)
			if address in (1, 2, 3, 6, 7, 8):
				self.assertEqual(wiring["control_connection"], "A4J3-2")
				self.assertEqual(wiring["return_connection"], f"A4J3-{9 + row}")
			else:
				self.assertEqual(wiring["control_connection"], f"A4J2-{strobe + 1}")
				self.assertEqual(wiring["return_connection"], f"A4J2-{8 + row}")

	def test_switch_test_shows_every_address_as_its_own_number(self) -> None:
		note = self.runtime["runtime"]["observations"]["runs"]["switch-test"]["note"]
		for address in range(1, 41):
			self.assertIn(f"{address}->{address}", note)

	def test_solenoid_translation_matches_the_printed_list_and_the_rom_test(self) -> None:
		printed = {int(row[0]): row[1] for row in markdown_rows(EXCERPTS / "solenoid-identification.md") if row[0].isdigit()}
		mapping = {int(key): value for key, value in self.runtime["runtime"]["observations"]["physical_service_solenoid_to_public"].items()}
		self.assertEqual(mapping, {1: 2, 2: 1, 3: 6, 4: 7, 5: 3, 6: 4, 7: 5, 8: 8, 9: 11, 10: 12, 11: 14, 12: 13, 13: 9, 14: 10, 15: 19, 16: 15, 17: 17, 18: 20, 19: 18})
		for physical, public in mapping.items():
			item = self.solenoids[public]
			self.assertIn({"namespace": "manual.self-test", "value": str(physical)}, item["aliases"])
			self.assertEqual(item["wiring"]["driver_transistor"], f"Q{physical}")
			if printed[physical] == "OPEN":
				self.assertIn(public, UNUSED_SOLENOIDS | {20}, public)
		for public, words in SOLENOID_WORDS.items():
			label = self.solenoids[public]["label"].lower()
			self.assertTrue(all(word in label for word in words), (public, label))
			self.assertEqual(self.solenoids[public]["availability"], "used")
		for public in UNUSED_SOLENOIDS:
			self.assertEqual(self.solenoids[public]["availability"], "unused", public)
		self.assertNotIn(16, self.solenoids)

	def test_the_two_continuous_outputs_are_treated_as_documented(self) -> None:
		seventeen, twenty = self.solenoids[17], self.solenoids[20]
		self.assertEqual(seventeen["availability"], "unused")
		self.assertIn("GEN. ILLUM. RELAY", seventeen["physical"]["notes"])
		self.assertEqual(twenty["availability"], "unknown")
		self.assertEqual(twenty["provenance"]["status"], "observed")
		self.assertIn("7777777", twenty["physical"]["notes"])
		note = self.runtime["runtime"]["observations"]["runs"]["gameplay"]["note"]
		self.assertIn("Public 20 is on", note)

	def test_lamp_addresses_follow_the_decoder_and_the_connector_table(self) -> None:
		decoder = decoder_table()
		self.assertEqual(set(decoder), {*range(1, 16), *range(17, 32), *range(33, 48), *range(49, 64)})
		self.assertEqual(sorted(decoder.values()), list(range(1, 61)))
		connectors = connector_scr_table()
		q_to_public = {q: public for public, q in decoder.items()}
		listed: dict[int, list[str]] = {}
		for description, wire, jack, pin in lamp_list():
			public = q_to_public[connectors[(jack, pin)]]
			listed.setdefault(public, []).append(description)
			self.assertEqual(self.lamps[public]["wiring"]["drive_connection"], f"A5{jack}-{pin}", description)
			self.assertEqual(self.lamps[public]["wiring"]["drive_wire"], wire, description)
		self.assertEqual(len(lamp_list()), 56)
		self.assertTrue(all(len(rows) == 1 for rows in listed.values()))
		self.assertEqual(set(self.lamps), set(decoder))
		self.assertEqual(set(decoder) - set(listed), UNUSED_LAMPS)
		for public, q in decoder.items():
			self.assertEqual(self.lamps[public]["wiring"]["driver_transistor"], f"Q{q}")

	def test_the_transposable_scr_pairs(self) -> None:
		decoder = decoder_table()
		self.assertEqual((decoder[24], decoder[25]), (25, 24))
		self.assertEqual((decoder[42], decoder[58]), (41, 46))

	def test_lamp_names_follow_the_printed_rows(self) -> None:
		for public, letter in LETTER_LAMPS.items():
			lamp = self.lamps[public]
			self.assertIn(f"letter {letter}", lamp["label"].lower())
			self.assertEqual(lamp["physical"]["quantity"], 2)
		for public, words in BACKBOX_LAMPS.items():
			self.assertIn(words, self.lamps[public]["label"].lower())
			self.assertEqual(self.lamps[public]["spatial"]["reason"], "cabinet_or_service")
		for public in UNUSED_LAMPS:
			self.assertEqual(self.lamps[public]["availability"], "unused")
		outside = set(self.runtime["runtime"]["observations"]["lamp_addresses_driven_outside_self_test"])
		self.assertFalse(outside & UNUSED_LAMPS)
		self.assertTrue({9, 10, 25, 26, 41, 42, 57} <= outside)

	def test_flippers_two_per_side(self) -> None:
		for address in (46, 48):
			self.assertEqual(self.solenoids[address]["physical"]["quantity"], 2)
		for address in (1, 2):
			self.assertEqual(self.direct[address]["physical"]["quantity"], 2)
			self.assertIs(self.direct[address]["normally_closed"], True)
		self.assertEqual(self.solenoids[45]["kind"], "virtual")
		self.assertEqual(self.solenoids[47]["kind"], "virtual")

	def test_option_switches(self) -> None:
		self.assertEqual(set(self.dips), set(range(1, 33)))
		self.assertEqual({address for address, item in self.dips.items() if item["availability"] == "unused"}, {14, 24})
		self.assertIn("corrected", self.dips[8]["label"])
		self.assertIn("corrected", self.dips[22]["label"])

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

	def test_spatial_report_states_the_blockers(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(report["readiness"]["missing"], EXPECTED_MISSING)
		self.assertEqual([item["id"] for item in report["unplaced_records"]], ["gi.general-illumination"])
		self.assertTrue(any("Public 20" in blocker for blocker in report["blockers"]))
		self.assertEqual(set(report["table_lamp_defects"]), {"5", "6", "30", "37"})

	def test_every_playfield_device_is_placed_inside_the_playfield(self) -> None:
		for collection in ("inputs", "outputs"):
			for item in self.definition[collection]:
				spatial = item.get("spatial")
				if item["id"] == "gi.general-illumination":
					self.assertIsNone(spatial)
					continue
				self.assertIsNotNone(spatial, item["id"])
				for placement in spatial.get("placements", []):
					self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
					self.assertIn(placement["provenance"]["status"], ("observed", "validated"), placement["id"])
		for address in range(1, 41):
			placed = self.switches[address]["spatial"]["status"] != "not_applicable"
			self.assertEqual(placed, address not in (1, 2, 3, 6, 7, 8), address)
		self.assertEqual(len(self.switches[37]["spatial"]["placements"]), 2)
		for address in (46, 48):
			self.assertEqual(len(self.solenoids[address]["spatial"]["placements"]), 2)
		for address in LETTER_LAMPS:
			self.assertEqual(len(self.lamps[address]["spatial"]["placements"]), 2, address)
		self.assertTrue(all(placement["provenance"]["status"] == "observed" for lamp in self.lamps.values() for placement in (lamp.get("spatial") or {}).get("placements", [])))

	def test_flipper_and_side_geometry(self) -> None:
		left, right = self.solenoids[48]["spatial"]["placements"], self.solenoids[46]["spatial"]["placements"]
		self.assertTrue(all(placement["x"] < 0.5 for placement in left) and all(placement["x"] > 0.5 for placement in right))
		# lower flipper first, upper second: the upper one is nearer the rear and further out
		self.assertLess(left[1]["y"], left[0]["y"])
		self.assertLess(left[1]["x"], left[0]["x"])
		self.assertGreater(right[1]["x"], right[0]["x"])

	def test_lamps_follow_the_printed_rows_not_the_tables_binding(self) -> None:
		import big_game_data as data
		def point(name):
			_, x, y, _ = data.OBJECTS[name]
			return (round(x / data.TABLE_WIDTH, 6), round(y / data.TABLE_HEIGHT, 6))
		def placed(address):
			return [(placement["x"], placement["y"]) for placement in self.lamps[address]["spatial"]["placements"]]
		self.assertEqual(placed(6), [point("l72")])
		self.assertEqual(placed(30), [point("l6")])
		self.assertEqual(placed(37), [point("l37"), point("l48")])
		self.assertEqual(placed(5), [point("l5"), point("l64")])
		self.assertEqual(placed(34), [point("l34")])
		self.assertNotIn("quantity", self.lamps[53]["physical"])
		self.assertEqual(self.lamps[5]["physical"]["quantity"], 2)
		self.assertEqual(self.lamps[37]["physical"]["quantity"], 2)

	def test_knowledge_note_states_the_blockers_and_the_translations(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("1->2, 2->1, 3->6", "GEN. ILLUM. RELAY", "7777777", "16 * k + a + 1", "public 14, 15, 31 and 47"):
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

	def test_sources_are_complete_and_scripts_are_pinned(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		for identifier in (curator.MANUAL_SOURCE, curator.CORRECTIONS_SOURCE, curator.SCHEMATIC_SOURCE, curator.SCRIPT_SOURCE, curator.OLD_SCRIPT_SOURCE, *curator.RUN_SOURCES.values()):
			self.assertIn(identifier, sources)
		self.assertEqual(sources[curator.SCRIPT_SOURCE]["sha256"], "828168766f0dcaf8e9f2bdf197ef8ac4a69550b2f3edc01d39be2832556097d1")
		self.assertEqual(sources[curator.OLD_SCRIPT_SOURCE]["sha256"], "89fc207c9329ec69100e5ed88d3fffd510e2bd73eae9de0a62f14ae87c4cf366")
		self.assertNotIn("known_working", sources[curator.OLD_SCRIPT_SOURCE])
		runs = {run["name"]: run["sha256"] for run in self.runtime["runtime"]["raw_runs"]}
		for name, identifier in curator.RUN_SOURCES.items():
			self.assertEqual(sources[identifier]["sha256"], runs[name])


class BigGameRetainedEvidenceTests(unittest.TestCase):
	"""Exact retained artifacts, checked only when the external roots are configured."""

	def test_harness_runs_reproduce_the_runtime_summary(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_big_game_runtime as summary
		self.assertEqual(canonical_bytes(summary.build(Path(root) / "big-game-1980" / "harness")), RUNTIME_PATH.read_bytes())

	def test_retained_table_extraction_and_coordinates(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		import big_game_data as data
		from build_external_evidence_manifest import check_manifest
		from pinmame_game_defs.spatial import _item_point
		folder = Path(root) / curator.TABLE_RELATIVE
		self.assertEqual(hashlib.sha256((folder / curator.TABLE_FILENAME).read_bytes()).hexdigest(), curator.TABLE_SHA256)
		self.assertEqual(hashlib.sha256((folder / curator.TABLE_ARCHIVE_FILENAME).read_bytes()).hexdigest(), curator.TABLE_ARCHIVE_SHA256)
		extraction = Path(root) / curator.EXTRACTION_RELATIVE
		self.assertEqual(check_manifest(extraction, "biggame"), curator.EXTRACTION_MANIFEST_SHA256)
		self.assertEqual(hashlib.sha256((extraction / "script.vbs").read_bytes()).hexdigest(), curator.TABLE_SCRIPT_SHA256)
		bounds = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
		self.assertEqual((bounds["left"], bounds["top"], bounds["right"], bounds["bottom"]), (0.0, 0.0, data.TABLE_WIDTH, data.TABLE_HEIGHT))
		for name, (item_type, x, y, file) in data.OBJECTS.items():
			document = json.loads((extraction / "gameitems" / file).read_text(encoding="utf-8"))
			self.assertEqual(next(iter(document)), item_type, name)
			value = document[item_type]
			self.assertEqual(value["name"], name)
			self.assertEqual(_item_point(item_type, value)[:2], (x, y), name)
			if item_type == "Light":
				self.assertIs(value["is_bulb_light"], True, name)

	def test_drawing_callout_artifacts_match_their_manifest(self) -> None:
		manuals, reviews = os.environ.get("PINMAME_MANUALS_ROOT"), os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not manuals or not reviews:
			self.skipTest("PINMAME_MANUALS_ROOT and PINMAME_REVIEW_ARTIFACTS_ROOT are needed")
		from build_external_evidence_manifest import check_manifest
		seed = load_json(ROOT / curator.CALLOUT_SEED_PATH)
		self.assertEqual(check_manifest(Path(reviews) / seed["retained_artifacts"]["directory"], "biggame"), seed["retained_artifacts"]["manifest_sha256"])
		for page in seed["pages"].values():
			self.assertEqual(hashlib.sha256((Path(manuals) / page["image"]["path"]).read_bytes()).hexdigest(), page["image"]["sha256"])

	def test_retained_documents_match_their_pinned_hashes(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("PINMAME_MANUALS_ROOT is not set")
		folder = Path(root) / "by-machine" / MACHINE_ID / "ipdb"
		for name, digest in ((curator.MANUAL_PDF, curator.MANUAL_SHA256), (curator.CORRECTIONS_PDF, curator.CORRECTIONS_SHA256), (curator.SCHEMATIC_PDF, curator.SCHEMATIC_SHA256),
				("photos/image-19.jpg", curator.CARD_PHOTO_SHA256), ("photos/image-4.jpg", curator.PLAYFIELD_PHOTO_SHA256), ("photos/image-12.jpg", curator.UPPER_PHOTO_SHA256)):
			self.assertEqual(hashlib.sha256((folder / name).read_bytes()).hexdigest(), digest, name)


if __name__ == "__main__":
	unittest.main()
