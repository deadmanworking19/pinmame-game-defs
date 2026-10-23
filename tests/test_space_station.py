"""Fail-closed tests for the Williams Space Station (1987) definition.

Each test pins one fact against the evidence that decided it: the ROM's own Coil, Single Lamps and
Switch Levels tests for names and addresses, pinned PinMAME's spstnGameData for the A/C bank at 12, the
switch-driven special solenoids and the flipper copy, the reactive Space Station probes for the motor's
homing, the manual for wiring and parts, an owner's insert-board comparison for the backbox lamps, and
the retained table for the placements. A regression names the fact that broke.
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
sys.path.insert(0, str(ROOT / "src"))

import curate_space_station  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "space-station-1987.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "space-station-1987.md"
RUNTIME_PATH = ROOT / "evidence" / "runtime" / "system-11" / "space-station-l5-service-and-mechanisms.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "williams.space-station.1987"

# Coil-test step order as the ROM displays it, paired with the address that pulsed (run coil-test).
COIL_TEST = [1, 25, 2, 26, 3, 27, 4, 28, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22]
UNUSED_SWITCHES = {2, 36, 44, 49, 51}
OPTIONAL_SWITCHES = {34}
INSERT_BOARD_LAMPS = {37, 41, 46, 47, 48, 49, 57}
SPECIALS = {18: 63, 19: 61, 20: 64, 21: 60, 22: 62}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def folded(text: str) -> str:
	return text.replace("0", "O").replace("5", "S")


class SpaceStationDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.switch"}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.runtime = load(RUNTIME_PATH)
		cls.runs = cls.runtime["runtime"]["observations"]["runs"]
		cls.named = cls.runtime["runtime"]["observations"]["named_output_addresses"]

	def test_curator_reproduces_every_artifact(self) -> None:
		curate_space_station.check(ROOT)

	def test_definition_validates_and_keeps_only_spatial_open(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("0x100", self.definition["controller"]["hardware_generation"])
		self.assertEqual(1987, self.definition["machine"]["year"])

	def test_driver_tree_is_the_single_l5_driver(self) -> None:
		self.assertEqual(["spstn_l5"], [d["id"] for d in self.definition["drivers"]])
		self.assertEqual("identical", self.definition["drivers"][0]["physical_compatibility"])
		catalog = load(ROOT / "catalog" / "pinmame.json")
		owners = {d["id"]: d.get("machine_id") for d in catalog["drivers"] if d["id"].startswith("spstn_")}
		self.assertEqual({"spstn_l5": "williams.space-station.1987"}, owners)

	def test_every_controller_address_is_enumerated(self) -> None:
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))

	def test_coil_names_follow_the_rom_coil_test(self) -> None:
		self.assertEqual(COIL_TEST, self.runs["coil-test"]["ordered_solenoid_on_sequence"])
		for step, address in enumerate(COIL_TEST, start=1):
			key = f"coil-{step:02d}-{slug(folded(curate_space_station.ROM_COIL_NAMES[address]))}"
			self.assertEqual(address, self.named[key], key)
			self.assertIn(curate_space_station.ROM_COIL_NAMES[address], self.solenoids[address]["physical"]["notes"])

	def test_unused_drives_are_skipped_and_unpublished(self) -> None:
		seen = set(self.runtime["runtime"]["observations"]["solenoid_addresses_seen"])
		for address in (5, 14):
			self.assertEqual("unused", self.solenoids[address]["availability"])
			self.assertNotIn(address, COIL_TEST)
		self.assertNotIn(5, seen)
		# 14 appears only in the power-on pulse of the whole controlled port, which every run shows for 9-16 together.
		# Every run whose note lists solenoid spans must show exactly that one early span for 14 and nothing else.
		checked = 0
		for name, run in self.runs.items():
			note = run.get("note", "")
			if "Solenoid on-spans: " not in note:
				continue
			spans = note.split("Solenoid on-spans: ", 1)[1].split(" (observed to ", 1)[0].split("; ")
			entries = [entry for entry in spans if entry.startswith("14: ")]
			self.assertEqual(1, len(entries), name)
			match = re.fullmatch(r"14: (0\.\d+)-(0\.\d+) s", entries[0])
			self.assertIsNotNone(match, (name, entries[0]))
			self.assertLess(float(match.group(2)), 0.4, name)
			checked += 1
		self.assertGreaterEqual(checked, 14)
		self.assertIn("property of the port", self.solenoids[14]["physical"]["notes"])

	def test_lamp_names_follow_the_single_lamps_test(self) -> None:
		for address in range(1, 65):
			key = f"lamp-{address:02d}-{slug(folded(curate_space_station.ROM_LAMP_NAMES[address]))}"
			self.assertEqual(address, self.named[key], key)

	def test_switch_names_follow_the_switch_levels_test(self) -> None:
		note = self.runs["switch-levels"]["note"].split("while held: ", 1)[1].rstrip(".")
		shown = {}
		for item in note.split("; "):
			address, rest = item.split(" = ", 1)
			name, after = rest.split(" / ", 1)
			shown[int(address)] = (name, after)
		for address, name in curate_space_station.ROM_SWITCH_NAMES.items():
			self.assertEqual(folded(name) or "(blank)", shown[address][0], address)
			self.assertTrue(shown[address][1].startswith(f"06 {address:02d}"), address)
		for coil, switch in SPECIALS.items():
			self.assertIn(str(coil), shown[switch][1].split("[", 1)[1], switch)
		self.assertEqual("RIGHT FLIPPER", shown[82][0])
		self.assertEqual("LEFT FLIPPER", shown[84][0])
		self.assertTrue(shown[82][1].startswith("06 56"))
		self.assertTrue(shown[84][1].startswith("06 55"))

	def test_ac_bank_is_published_at_25_to_32(self) -> None:
		for pair in range(1, 9):
			a, c = self.solenoids[pair], self.solenoids[pair + 24]
			self.assertEqual(f"{pair:02d}A", [x["value"] for x in a["aliases"] if x["namespace"] == "manual.address"][0])
			self.assertEqual(f"{pair:02d}C", [x["value"] for x in c["aliases"] if x["namespace"] == "manual.address"][0])
			self.assertEqual(a["wiring"]["driver_transistor"], c["wiring"]["driver_transistor"])
		self.assertEqual("relay", self.solenoids[12]["kind"])
		self.assertEqual("coil", self.solenoids[32]["kind"])
		self.assertEqual("unused", self.switches[2]["availability"])

	def test_special_solenoids_follow_their_switches(self) -> None:
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["id"].startswith("relationship.switch-")}
		expected = {(f"switch.matrix-{switch}", curate_space_station.output_id(coil)) for coil, switch in SPECIALS.items()}
		self.assertEqual(expected, relations)
		for address in range(17, 23):
			self.assertEqual(f"Special #{address - 16}", [x["value"] for x in self.solenoids[address]["aliases"] if x["namespace"] == "manual.special-solenoid"][0])
		self.assertIn("has no switch", self.solenoids[17]["physical"]["notes"])

	def test_flipper_buttons_are_copied_into_the_lane_change_switches(self) -> None:
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"] if "flipper-column" in r["id"]}
		self.assertEqual({("switch.flipper-column-82", "switch.matrix-56"), ("switch.flipper-column-84", "switch.matrix-55")}, relations)
		for address in (55, 56):
			self.assertIn("cannot drive it directly", self.switches[address]["physical"]["notes"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])

	def test_every_fitted_switch_is_normally_open(self) -> None:
		for address in range(1, 65):
			device = self.switches[address]
			if address in UNUSED_SWITCHES:
				self.assertEqual("unused", device["availability"])
				self.assertNotIn("normally_closed", device)
			elif address in OPTIONAL_SWITCHES:
				self.assertEqual("optional", device["availability"])
				self.assertNotIn("normally_closed", device)
				self.assertNotIn("spatial", device)
				self.assertIn("German", device["physical"]["notes"])
			else:
				self.assertEqual("used", device["availability"])
				self.assertIs(False, device["normally_closed"], address)
		for address in (33, 52, 53, 57, 58, 59):
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"])

	def test_insert_board_lamps_cover_both_production_boards(self) -> None:
		for address in INSERT_BOARD_LAMPS:
			lamp = self.lamps[address]
			self.assertEqual("cabinet_or_service", lamp["spatial"]["reason"])
			self.assertIn(curate_space_station.VARIANT_SOURCE, lamp["provenance"]["source_refs"])
			self.assertIn("Wheel Version", lamp["physical"]["notes"])
		self.assertEqual("optional", self.lamps[41]["availability"])
		self.assertEqual({"used"}, {self.lamps[a]["availability"] for a in INSERT_BOARD_LAMPS - {41}})
		self.assertIn("\"Wheel Version\"", (EXCERPTS / "production-variants.md").read_text(encoding="utf-8"))

	def test_three_bank_order_follows_the_manual_and_the_table(self) -> None:
		y = {address: self.switches[address]["spatial"]["placements"][0]["y"] for address in (57, 58, 59)}
		self.assertLess(y[57], y[58])
		self.assertLess(y[58], y[59])
		self.assertEqual("3-Bank Drop Target (Upper)", self.switches[57]["label"])
		self.assertIn("3 BANK BOTTOM", self.switches[57]["physical"]["notes"])

	def test_ten_point_rubbers_follow_the_machine_not_the_table_binding(self) -> None:
		top, low = self.switches[50]["spatial"]["placements"][0], self.switches[54]["spatial"]["placements"][0]
		self.assertLess(top["y"], low["y"])
		self.assertIn("sw54_rubber", self.switches[50]["physical"]["notes"])
		self.assertIn("crossed", self.switches[50]["physical"]["notes"])

	def test_gi_relays(self) -> None:
		self.assertEqual(51, len(self.solenoids[9]["spatial"]["placements"]))
		self.assertEqual(25, len(self.solenoids[10]["spatial"]["placements"]))
		for address in (9, 10):
			self.assertEqual("gi", self.solenoids[address]["kind"])
			self.assertEqual("observed", self.solenoids[address]["spatial"]["status"])
			self.assertNotIn("quantity", self.solenoids[address]["physical"])
		self.assertEqual("cabinet_or_service", self.solenoids[11]["spatial"]["reason"])
		self.assertIn(10, self.runs["gameplay"]["solenoid_addresses_seen"])

	def test_top_panel_flashers_are_clamped_to_the_rear_edge(self) -> None:
		for address, count in ((15, 3), (29, 2)):
			placements = self.solenoids[address]["spatial"]["placements"]
			self.assertEqual(count, len(placements))
			self.assertEqual({0.0}, {p["y"] for p in placements})
		for address in (30, 31):
			self.assertEqual("cabinet_or_service", self.solenoids[address]["spatial"]["reason"])
		self.assertEqual(4, self.solenoids[25]["physical"]["quantity"])

	def test_space_station_homes_on_the_edge_into_52_open_53_closed(self) -> None:
		self.assertEqual("motor", self.solenoids[16]["kind"])
		pivot = curate_space_station.norm(*curate_space_station.STATION_PIVOT)
		for device in (self.solenoids[16], self.switches[52], self.switches[53]):
			placement = device["spatial"]["placements"][0]
			self.assertEqual(pivot, (placement["x"], placement["y"]))
			self.assertEqual("validated", placement["provenance"]["status"])
		for order in ("ccw", "cw"):
			note = self.runs[f"station-reactive-{order}"]["note"]
			events = [item.strip() for item in note.split(": ", 1)[1].split(";")]
			# The first release of the relay after the host's first pattern change is the ROM's homing stop.
			changed, pattern, stop_pattern = False, None, None
			for item in events:
				if "(52,53)=" in item:
					pattern = item.split("(52,53)=", 1)[1].split(" ")[0]
					changed = changed or pattern != "(0,0)"
				elif item.endswith("16=0") and changed:
					stop_pattern = pattern
					break
			self.assertEqual("(0,1)", stop_pattern, order)
		for name in ("boot-station-52", "boot-station-53", "boot-station-52-53", "boot-baseline"):
			self.assertIn("16: ", self.runs[name]["note"])

	def test_target_mechanism_lists_every_target_sensor(self) -> None:
		targets = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.targets-and-lanes")
		expected = [f"switch.matrix-{address}" for address in list(range(18, 32)) + [35, 50, 54]]
		self.assertEqual(expected, targets["sensors"])

	def test_knocker_is_in_the_backbox(self) -> None:
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])
		self.assertIn("B-10686-2", self.solenoids[7]["physical"]["notes"])
		self.assertIn("INSERT KNOCKER", self.solenoids[7]["physical"]["notes"])

	def test_legacy_aliases_are_carried_by_binding(self) -> None:
		def values(device: dict, namespace: str) -> set[str]:
			return {alias["value"] for alias in device["aliases"] if alias["namespace"] == namespace}

		self.assertIn("c_game_on", values(self.solenoids[23], "vpe-legacy.coil"))
		self.assertTrue({"1", "01", "001"} <= values(self.solenoids[1], "vpe-legacy.coil"))
		seed = load(curate_space_station.LEGACY_ALIAS_SEED_PATH)
		carried = sum(len(aliases) for addresses in seed["aliases"].values() for aliases in addresses.values())
		present = sum(1 for collection in ("inputs", "outputs") for device in self.definition[collection] for alias in device["aliases"] if alias["namespace"].startswith("vpe-legacy."))
		self.assertEqual(carried, present)

	def test_regeneration_refuses_to_replace_an_author_ready_artifact(self) -> None:
		import tempfile

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			stale = root / curate_space_station.STALE_DEFINITION_PATH.relative_to(ROOT)
			stale.parent.mkdir(parents=True)
			stale.write_bytes(b"{}\n")
			with self.assertRaisesRegex(RuntimeError, "refusing to replace the author-ready"):
				curate_space_station.generate(root)
			self.assertEqual(b"{}\n", stale.read_bytes())
			self.assertFalse((root / curate_space_station.DEFINITION_PATH.relative_to(ROOT)).exists())

	def test_manual_sources_carry_acquisition_provenance(self) -> None:
		sources = {s["id"]: s for s in self.definition["sources"]}
		for key in (curate_space_station.MANUAL_SOURCE, curate_space_station.AMENDMENT_SOURCE):
			source = sources[key]
			self.assertRegex(source["acquired_at"], r"^2026-10-23T\d\d:\d\d:\d\dZ$")
			self.assertTrue(source["sha256"] and source["original_filename"] and source["source_id"])
			self.assertIn("https://www.ipdb.org/files/2261/", source["locator"])
		self.assertIn("https://www.ipdb.org/machine.cgi?id=2261", sources[curate_space_station.MANUAL_SOURCE]["locator"])
		self.assertEqual(curate_space_station.EXTRACTION_MANIFEST_SHA256, sources[curate_space_station.VPX_EXTRACTION_SOURCE]["sha256"])

	def test_extraction_verifier_refuses_a_refreshed_manifest(self) -> None:
		import tempfile

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			extraction = root / curate_space_station.EXTRACTION_RELATIVE_PATH
			extraction.mkdir(parents=True)
			(extraction / "script.vbs").write_bytes(b"altered\n")
			curate_space_station.write_extraction_manifest(root)
			with self.assertRaisesRegex(RuntimeError, "not the pinned one"):
				curate_space_station.verify_extraction_manifest(root)

	def test_excerpt_digests_match(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])

	def test_no_other_machine_identity_leaks_in(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {d["id"] for d in catalog["drivers"] if not d["id"].startswith("spstn_") and len(d["id"]) >= 5 and "_" in d["id"]}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		for text in texts:
			words = set(re.findall(r"\b[a-z0-9]+_[a-z0-9_]+\b", text))
			self.assertEqual(set(), words & foreign)


class SpaceStationRetainedEvidenceTests(unittest.TestCase):
	def test_runtime_evidence_matches_the_raw_runs(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import space_station_runtime_evidence
		from pinmame_game_defs.jsonio import canonical_bytes

		review_root = space_station_runtime_evidence.working_root()
		if not (review_root / space_station_runtime_evidence.HARNESS_RELATIVE).is_dir():
			self.skipTest("retained Space Station runs are not present under this review-artifacts root")
		_, evidence = space_station_runtime_evidence.build(review_root)
		self.assertEqual(canonical_bytes(evidence), RUNTIME_PATH.read_bytes())

	def test_address_14_only_pulses_at_power_on_in_every_raw_run(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import space_station_runtime_evidence

		harness = space_station_runtime_evidence.working_root() / space_station_runtime_evidence.HARNESS_RELATIVE
		if not harness.is_dir():
			self.skipTest("retained Space Station runs are not present under this review-artifacts root")
		for name in space_station_runtime_evidence.RUN_NAMES:
			run = load(harness / name / "run.json")
			transitions = [(event["state"], event["time_s"]) for event in run["events"] if event["event"] == "solenoid" and event["number"] == 14]
			self.assertEqual([1, 0], [state for state, _ in transitions], name)
			self.assertLess(transitions[-1][1], 0.4, name)
			self.assertFalse(any(event["event"] == "solenoid" and event["number"] == 5 for event in run["events"]), name)

	def test_retained_extraction_matches_its_manifest(self) -> None:
		root = curate_space_station.configured_vpx_sources_root(required=False)
		if root is None:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT not configured")
		if not (root / curate_space_station.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Space Station extraction is not present under this root")
		curate_space_station.verify_extraction_manifest(root)

	def test_rom_name_table_excerpt_matches_the_rom(self) -> None:
		roms = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
		if not roms:
			self.skipTest("PINMAME_ROM_LIBRARY_ROOT not configured")
		archive = Path(roms) / "spstn_l5.zip"
		if not archive.is_file():
			self.skipTest("spstn_l5 is not in this ROM library")
		import space_station_rom_name_tables

		results = {"spstn_l5": space_station_rom_name_tables.decode_set(archive)}
		self.assertEqual(curate_space_station.ROM_ARCHIVE_SHA256, results["spstn_l5"]["rom_archive_sha256"])
		self.assertEqual(space_station_rom_name_tables.render_markdown(results), (EXCERPTS / "rom-name-tables.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
	unittest.main()
