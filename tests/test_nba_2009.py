"""Fail-closed tests for the Stern NBA (2009) definition.

The load-bearing assertions are the ones that survive every schema check but would not survive a
wrong derivation: the public-address contract the ROM's own service tests prove (their names and
wire colours, transcribed in the excerpt, must agree with the device tables), the matrix polarity
rule, the firmware equivalence of the five drivers, the bumper and slingshot pairings, the
game-on solenoid that only nba_802 publishes, and the one conflict that keeps the pop-bumper sides
open.
"""

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

import nba_devices as dev  # noqa: E402
import nba_spatial as spatial  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "nba-2009.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "nba-2009.md"
RUNTIME_ROOT = ROOT / "evidence" / "runtime" / "sam"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "stern.nba.2009"
SPATIAL_SEED = ROOT / "tools" / "seeds" / "stern" / "nba-2009-spatial.json"
AUDIT = ROOT / "reports" / "spatial" / "stern" / "nba-2009.json"
MACHINE_ID = "stern.nba.2009"
PINNED_LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
TABLE_SHA256 = "ae322910ad7f74f984e0216c5bf05cd0984ab727bff455f13992d5afb708eb58"
SWEEP_DRIVERS = ["nba_802", "nba_801", "nba_700", "nba_600", "nba_500"]

USED_MATRIX_SWITCHES = set(range(1, 17)) | set(range(18, 38)) | {47}
OPTO_SWITCHES = {11, 12, 13, 21, 22, 34}
UNUSED_LAMPS = {8, 11, 29, 34, 38, 53, 55, 56} | set(range(65, 81))
CONFLICTED = {("pinmame.input.switch", 31), ("pinmame.input.switch", 32), ("pinmame.output.solenoid", 10), ("pinmame.output.solenoid", 11), ("pinmame.output.lamp", 61), ("pinmame.output.lamp", 62)}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def by_binding(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def excerpt_table(heading: str) -> dict[int, list[str]]:
	"""Rows of the first table under ``heading`` in the ROM service-test excerpt, keyed by their first cell."""
	text = (EXCERPT_ROOT / "rom-service-tests.md").read_text(encoding="utf-8")
	section = text.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
	rows = {}
	for line in section.splitlines():
		cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
		if line.startswith("|") and re.fullmatch(r"-?\d+", cells[0].strip("`")):
			rows[int(cells[0].strip("`"))] = cells[1:]
	return rows


class NbaDefinitionTests(unittest.TestCase):
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
		self.assertEqual((MACHINE_ID, 5442, 2009, "G5K19-MBRlz", "NBA"), (machine["id"], machine["ipdb_id"], machine["year"], machine["opdb_id"], machine["name"]))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["mechanism_behavior", "spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual({"platform": "pinmame.sam", "inversion_applied_by_emulator": True}, self.definition["controller"])
		self.assertFalse((ROOT / "machines" / "stubs" / "nba_802.json").exists())
		self.assertEqual(81, next(item for item in self.catalog["machines"] if item["id"] == MACHINE_ID)["completion_score"])
		import curate_nba

		self.assertEqual(self.definition, json.loads(json.dumps(curate_nba.build())))
		self.assertEqual(self.knowledge, curate_nba.knowledge_text())
		self.assertEqual(load_json(AUDIT), json.loads(json.dumps(curate_nba.audit(self.definition))))

	def test_driver_family_is_exhaustive_and_firmware_only(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual({driver["id"] for driver in self.catalog["drivers"] if driver["id"].startswith("nba_")}, set(drivers))
		self.assertEqual(set(SWEEP_DRIVERS), set(drivers))
		self.assertEqual({MACHINE_ID}, {driver["machine_id"] for driver in self.catalog["drivers"] if driver["id"] in drivers})
		self.assertEqual({"nba_802"}, {driver_id for driver_id, driver in drivers.items() if "clone_of" not in driver})
		for driver_id, driver in drivers.items():
			self.assertEqual("identical", driver["physical_compatibility"])
			self.assertIn("pixel for pixel", driver["variant_notes"])
			self.assertEqual(driver_id == "nba_802", "publishes the synthetic game-on solenoid 33" in driver["variant_notes"], driver_id)

	def test_input_spaces_polarity_and_used_set(self) -> None:
		self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(self.inputs))
		self.assertEqual(set(range(1, 9)), set(by_binding(self.definition, "inputs", "pinmame.input.dip")))
		self.assertEqual(USED_MATRIX_SWITCHES, {n for n in range(1, 65) if self.inputs[n]["availability"] == "used"})
		self.assertEqual(OPTO_SWITCHES, {n for n in range(1, 65) if self.inputs[n]["physical"]["switch_type"] == "opto"})
		for number in range(1, 65):
			self.assertFalse(self.inputs[number]["normally_closed"], number)
		self.assertEqual({18, 19, 20, 21}, {n for n in range(1, 65) if self.inputs[n].get("initial_active")})
		self.assertEqual({83: True, 81: True, 84: False, 82: False, -6: False, -7: False}, {n: self.inputs[n]["normally_closed"] for n in (83, 81, 84, 82, -6, -7)})
		self.assertEqual({"used"}, {self.inputs[n]["availability"] for n in (84, 83, 82, 81)})
		self.assertEqual({"unused"}, {self.inputs[n]["availability"] for n in (88, 87, 86, 85, 70, 71, 72, -4)})
		self.assertEqual({-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter"}, {n: self.inputs[n]["roles"][0] for n in (-3, -2, -1, 0)})

	def test_matrix_names_and_wires_match_the_rom_excerpt(self) -> None:
		rows = excerpt_table("Switch test, matrix switches 1–64")
		self.assertEqual(set(range(1, 65)), set(rows))
		for number, (name, wires) in rows.items():
			expected = dev.SWITCHES[number][6] if number in dev.SWITCHES else f"SWITCH #{number}"
			self.assertEqual(expected, name, number)
			device = self.inputs[number]
			self.assertEqual(wires, f"{device['wiring']['drive_wire']} / {device['wiring']['return_wire']}", number)
			self.assertIn(f'"{name}"', device["physical"]["notes"], number)
		dedicated = excerpt_table("Switch test, dedicated switches")
		self.assertEqual({65, 66, 67, 68, 69, 70, 71, 72, 81, 82, 83, 84, 85, 86, 87, 88, -7, -6, -5, -4}, set(dedicated))
		for number, (display, wires) in dedicated.items():
			name, last, rom_wires = dev.DEDICATED_ROM_TEXT[number]
			self.assertEqual((f"{name} / LAST SW. {last}", rom_wires), (display, wires), number)

	def test_solenoid_space_matches_the_coil_test(self) -> None:
		self.assertEqual(set(range(1, 34)) | set(range(51, 67)), set(self.solenoids))
		rows = excerpt_table("Single Coil Test")
		self.assertEqual(set(range(1, 33)), set(rows))
		for number, (name, wires, fired) in rows.items():
			device = self.solenoids[number]
			self.assertEqual(dev.COILS[number][3], name, number)
			self.assertEqual(wires, f"{device['wiring']['power_wire']} / {device['wiring']['control_wire']}", number)
			self.assertEqual(f"Q{number}", device["wiring"]["driver_transistor"])
			self.assertEqual([int(n) for n in re.findall(r"\d+", fired)], [] if number == 24 else [6, 22] if number == 6 else [number], number)
		self.assertEqual({8, 24}, {n for n in range(1, 33) if self.solenoids[n]["availability"] == "optional"})
		self.assertEqual({"relay": [22], "motor": [6, 8], "magnet": [3], "flasher": [13, 14, 19, 23, 25, 26, 27, 28, 29, 30, 31, 32]}, {kind: sorted(n for n in range(1, 33) if self.solenoids[n]["kind"] == kind) for kind in ("relay", "motor", "magnet", "flasher")})
		game_on = self.solenoids[33]
		self.assertEqual(("virtual.game-on", "virtual", "used"), (game_on["id"], game_on["kind"], game_on["availability"]))
		self.assertIn(dev.RT_FASTFLIP, game_on["provenance"]["source_refs"])
		self.assertIn("OnSolenoidUpdated", game_on["physical"]["notes"])
		self.assertEqual({"unused"}, {self.solenoids[n]["availability"] for n in range(51, 67)})

	def test_lamp_space_names_and_wires_match_the_lamp_test(self) -> None:
		self.assertEqual(set(range(1, 81)), set(self.lamps))
		self.assertEqual(UNUSED_LAMPS, {n for n, lamp in self.lamps.items() if lamp["availability"] == "unused"})
		rows = excerpt_table("Single Lamp Test")
		self.assertEqual(set(range(1, 81)), set(rows))
		for number, (name, wires) in rows.items():
			self.assertEqual(dev.LAMPS[number][1] if number in dev.LAMPS else "NOT USED", name, number)
			wiring = self.lamps[number]["wiring"]
			self.assertEqual(wires, f"{wiring['drive_wire']} / {wiring['return_wire']}", number)
		self.assertEqual([0], list(by_binding(self.definition, "outputs", "pinmame.output.gi")))

	def test_parts_book_is_cited_only_where_it_speaks(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"]:
			refs = device["provenance"]["source_refs"]
			if dev.MANUAL in refs:
				text = json.dumps(device.get("physical", {}))
				self.assertTrue("parts book" in text or "part_number" in device.get("physical", {}), device["id"])
		self.assertNotIn(dev.MANUAL, self.solenoids[23]["provenance"]["source_refs"])
		self.assertNotIn(dev.MANUAL, self.inputs[1]["provenance"]["source_refs"])

	def test_pop_bumper_sides_stay_conflicted_with_a_resolution_path(self) -> None:
		(conflict,) = self.definition["conflicts"]
		self.assertEqual("conflict.pop-bumper-sides", conflict["id"])
		self.assertNotIn("status", conflict)
		self.assertIn("Resolution path:", conflict["description"])
		self.assertIn("61 (RIGHT) 62 (LEFT)", conflict["description"])
		self.assertTrue({dev.ROM, dev.RT_POPS, dev.MANUAL, dev.TABLE} <= set(conflict["source_refs"]))
		conflicted = {(item["binding"]["group"], item["binding"]["device"]) for group in ("inputs", "outputs") for item in self.definition[group] if item["provenance"]["status"] == "conflicted"}
		self.assertEqual(CONFLICTED, conflicted)
		self.assertEqual(("Left pop bumper", "Right pop bumper"), (self.inputs[31]["label"], self.inputs[32]["label"]))
		self.assertEqual(("Left pop bumper", "Right pop bumper"), (self.solenoids[10]["label"], self.solenoids[11]["label"]))
		self.assertEqual(("Left pop bumper", "Right pop bumper"), (self.lamps[61]["label"], self.lamps[62]["label"]))
		placements = {group_device: pl for group in ("inputs", "outputs") for item in self.definition[group] for group_device in [(item["binding"]["group"], item["binding"]["device"])] for pl in (item.get("spatial") or {}).get("placements", [])}
		for key in CONFLICTED:
			self.assertEqual("conflicted", placements[key]["provenance"]["status"], key)
		# The ROM's left bumper (switch 31, lamp 61) is placed left of its right bumper (switch 32, lamp 62).
		self.assertLess(placements[("pinmame.input.switch", 31)]["x"], placements[("pinmame.input.switch", 32)]["x"])
		self.assertLess(placements[("pinmame.output.lamp", 61)]["x"], placements[("pinmame.output.lamp", 62)]["x"])
		self.assertIn("61 (RIGHT) 62 (LEFT)", (EXCERPT_ROOT / "manual-blue-pages.md").read_text(encoding="utf-8"))

	def test_mechanisms_reference_declared_devices(self) -> None:
		declared = {item["id"] for group in ("inputs", "outputs") for item in self.definition[group]}
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertTrue(set(mechanism["actuators"]) | set(mechanism["sensors"]) <= declared, mechanism["id"])
		self.assertEqual("conflicted", mechanisms["mechanism.pop-bumpers"]["provenance"]["status"])
		self.assertEqual([dev.output_id(6), dev.output_id(22)], mechanisms["mechanism.spinning-disk"]["actuators"])
		self.assertEqual({"observed"}, {mechanisms[key]["provenance"]["status"] for key in ("mechanism.left-eject", "mechanism.magna-hoop", "mechanism.ramp-diverter", "mechanism.basket-diverter", "mechanism.orbit-post", "mechanism.spinning-disk")})

	def test_excerpt_digests_and_sources(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		cited = set()
		for source in sources.values():
			for excerpt in source.get("excerpts", []):
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				self.assertFalse(excerpt["reviewed"])
				cited.add(Path(excerpt["path"]).name)
		self.assertEqual({path.name for path in EXCERPT_ROOT.glob("*.md")}, cited)
		self.assertEqual("f74e8c1c8ad5c724d51b8f472b9163ee2f5de685558f99686863e35e4d268243", sources[dev.MANUAL]["sha256"])
		self.assertEqual(TABLE_SHA256, sources[dev.TABLE]["sha256"])
		self.assertNotIn("known-working", sources[dev.TABLE]["locator"].replace("not verified it as known-working", ""))
		# Every acquired or generated source records when; only the pinned PinMAME records and the read-only ROM archive do not.
		for source in sources.values():
			if source["id"] in {dev.CATALOG, dev.CORE, dev.ROM}:
				self.assertNotIn("acquired_at", source)
			else:
				self.assertRegex(source["acquired_at"], r"^2026-10-30T\d\d:\d\d:\d\dZ$", source["id"])
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if root:
			manual = Path(root) / "by-machine" / MACHINE_ID / "official-stern" / "NBA-Manual.pdf"
			self.assertEqual(sources[dev.MANUAL]["sha256"], hashlib.sha256(manual.read_bytes()).hexdigest())
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if root:
			source = Path(root) / "stern" / "nba-2009" / "source"
			self.assertEqual(TABLE_SHA256, hashlib.sha256((source / "NBA (Stern 2009).vpx").read_bytes()).hexdigest())
			self.assertEqual(sources[dev.SCRIPT]["sha256"], hashlib.sha256((source / "NBA (Stern 2009).vbs").read_bytes()).hexdigest())

	def test_spatial_seed_and_audit_are_pinned(self) -> None:
		seed = load_json(SPATIAL_SEED)
		audit = load_json(AUDIT)
		self.assertEqual(hashlib.sha256(SPATIAL_SEED.read_bytes()).hexdigest(), audit["source_seed_sha256"])
		self.assertEqual(TABLE_SHA256, seed["table_sha256"])
		self.assertEqual(seed["table_manifest_sha256"], audit["extraction_manifest_sha256"])
		placements = [pl for group in ("inputs", "outputs", "displays") for item in self.definition[group] for pl in (item.get("spatial") or {}).get("placements", [])]
		self.assertEqual(len(placements), audit["located_placements"])
		self.assertEqual(0, audit["validated_placements"])
		# Insert render lights sit on no bulb, so the insert lamps are candidates only; the bumper lamps keep their bulb lights.
		lamps = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		self.assertEqual(51, len(spatial.INSERT_LAMPS))
		self.assertEqual({"candidate"}, {lamps[n]["spatial"]["status"] for n in spatial.INSERT_LAMPS})
		self.assertEqual({"candidate"}, {pl["provenance"]["status"] for n in spatial.INSERT_LAMPS for pl in lamps[n]["spatial"]["placements"]})
		self.assertEqual(51, audit["candidate_placements"])
		self.assertEqual([lamps[n]["id"] for n in spatial.INSERT_LAMPS], audit["candidate_spatial_ids"])
		self.assertEqual({60: "observed", 61: "conflicted", 62: "conflicted"}, {n: lamps[n]["spatial"]["status"] for n in sorted(spatial.BULB_LAMPS)})
		self.assertEqual(["switch.18-trough-4-left", "switch.19-trough-3", "switch.20-trough-2", "switch.21-trough-1-right", "switch.22-trough-jam", dev.output_id(13), dev.output_id(19), dev.output_id(31), "gi.master"], audit["missing_spatial_ids"])
		self.assertEqual(["conflict.pop-bumper-sides"], audit["unresolved_conflict_ids"])
		# No placement rests on a VPX Flasher sprite.
		self.assertFalse([pl["id"] for pl in placements if any("Flasher." in str(value) for value in pl.values())])
		self.assertEqual({"cabinet_or_service"}, {self.solenoids[n]["spatial"]["reason"] for n in (8, 24)})
		self.assertEqual("internal_nonvisual", self.solenoids[22]["spatial"]["reason"])
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if root:
			manifest = Path(root) / "stern" / "nba-2009" / "manifest.json"
			self.assertEqual(seed["table_manifest_sha256"], hashlib.sha256(manifest.read_bytes()).hexdigest())
			gameitems = Path(root) / "stern" / "nba-2009" / "analysis" / "vpxtool-extracted" / "gameitems"
			bulbs = {n: load_json(gameitems / f"{name}.json")["Light"]["is_bulb_light"] for n, name in spatial.LAMP_OBJECTS.items()}
			self.assertEqual(spatial.BULB_LAMPS, {n for n, bulb in bulbs.items() if bulb})


class NbaRuntimeEvidenceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
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
		self.assertEqual(evidence["runtime"]["game"], run["game"])
		if run.get("scenario"):
			self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
			self.assertEqual(raw["scenario_sha256"], hashlib.sha256((ROOT / raw["scenario_path"]).read_bytes()).hexdigest())
		return run

	def test_every_runtime_source_cites_its_summary_and_raw_run(self) -> None:
		cited = {source["uri"] for source in self.definition["sources"] if source["kind"] == "runtime_scenario" and source["uri"].startswith("internal:")}
		self.assertEqual({"internal:evidence/runtime/sam/" + path.name for path in RUNTIME_ROOT.glob("nba-*.json")}, cited)
		self.assertEqual(20, len(cited))
		for source in self.definition["sources"]:
			if source["kind"] != "runtime_scenario" or not source["uri"].startswith("internal:"):
				continue
			evidence = load_json(ROOT / source["uri"][len("internal:"):])
			self.assertEqual(source["sha256"], evidence["runtime"]["raw_runs"][0]["sha256"])
			self.assertEqual([MACHINE_ID], evidence["machine_ids"])
			self.assertEqual(PINNED_LIBRARY_SHA256, evidence["runtime"]["emulator"]["sha256"])
			self.retained(evidence, source["id"])

	def test_firmware_revisions_draw_the_same_test_frames(self) -> None:
		for kind, frames, actions in (("switch", 86, 84), ("coil", 42, 40), ("lamp", 84, 82)):
			base = self.summary(f"nba-nba_802-{kind}-test-sweep.json")["runtime"]["observations"]
			self.assertEqual((frames, actions), (len(base["diagnostic_snapshots"]), len(base["named_action_observations"])))
			for driver in SWEEP_DRIVERS[1:]:
				with self.subTest(kind=kind, driver=driver):
					other = self.summary(f"nba-{driver}-{kind}-test-sweep.json")["runtime"]["observations"]
					self.assertNotEqual(base["diagnostic_snapshots"][0]["pixel_sha256"], other["diagnostic_snapshots"][0]["pixel_sha256"])
					self.assertEqual([snap["pixel_sha256"] for snap in base["diagnostic_snapshots"][1:]], [snap["pixel_sha256"] for snap in other["diagnostic_snapshots"][1:]])
					self.assertEqual([item["transitioned_solenoid_addresses"] for item in base["named_action_observations"]], [item["transitioned_solenoid_addresses"] for item in other["named_action_observations"]])

	def test_sweeps_pair_every_address_with_its_rom_reading(self) -> None:
		import nba_runtime as runtime

		for driver in SWEEP_DRIVERS:
			with self.subTest(driver=driver):
				switch = self.summary(f"nba-{driver}-switch-test-sweep.json")
				snapshots = switch["runtime"]["observations"]["diagnostic_snapshots"]
				self.assertEqual("SWITCH TEST / NONE", snapshots[1]["interpreted_text"])
				self.assertEqual([runtime.switch_text(address) for address in runtime.SWITCH_ADDRESSES], [snap["interpreted_text"] for snap in snapshots[2:]])
				coil = self.summary(f"nba-{driver}-coil-test-sweep.json")["runtime"]["observations"]["named_action_observations"]
				expected = [[] if n == 24 else [6, 22] if n == 6 else [n] for n in (runtime.coil_number(p) for p in range(1, 41))]
				self.assertEqual(expected, [item["transitioned_solenoid_addresses"] for item in coil])
				lamp = self.summary(f"nba-{driver}-lamp-test-sweep.json")
				self.assertEqual(list(range(1, 81)), lamp["runtime"]["observations"]["lamp_addresses_seen"])
				self.retained(switch, driver)
				self.retained(lamp, driver)

	def test_bumper_and_slingshot_probe_pairs_each_switch_with_its_coil_and_lamp(self) -> None:
		actions = self.summary("nba-nba_802-bumper-sling-probe.json")["runtime"]["observations"]["named_action_observations"]
		expected = {30: (9, 60), 31: (10, 61), 32: (11, 62), 26: (17, None), 27: (18, None)}
		seen = set()
		for item in actions:
			switch = item["input_address"]
			coil, lamp = expected[switch]
			seen.add(switch)
			changed = set(item["transitioned_solenoid_addresses"])
			self.assertIn(coil, changed, item["label"])
			self.assertFalse(changed & ({9, 10, 11, 17, 18} - {coil}), item["label"])
			self.assertIn(8 if lamp else 32, changed, item["label"])
			if lamp:
				self.assertIn(31, changed)
				lit = {int(n) for n in item["label"].split("lamps turned on: ", 1)[1].split(", ") if n.isdigit()}
				self.assertEqual({lamp}, lit & {60, 61, 62}, item["label"])
		self.assertEqual(set(expected), seen)
		self.assertEqual(10, len(actions))

	def test_boot_and_gameplay_probes(self) -> None:
		boot = self.summary("nba-nba_802-boot-start.json")["runtime"]["observations"]
		self.assertEqual(([0], [1, 24]), (boot["gi_addresses_seen"], boot["solenoid_addresses_seen"]))
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], boot["display_layouts_seen"])
		steps = {item["label"].split(":", 1)[0]: item for item in self.summary("nba-nba_802-gameplay-probe.json")["runtime"]["observations"]["named_action_observations"]}
		self.assertTrue({3, 4} <= set(steps["ball in the left eject (switch 35 closed)"]["transitioned_solenoid_addresses"]))
		self.assertIn(20, steps["ball in the right eject (switch 9 closed)"]["transitioned_solenoid_addresses"])
		self.assertTrue({7, 8} <= set(steps["MV(P) drop target 11 down"]["transitioned_solenoid_addresses"]))
		self.assertEqual([], steps["ball in shooter lane"]["transitioned_solenoid_addresses"])
		self.assertIn(15, steps["left flipper button held"]["transitioned_solenoid_addresses"])
		self.assertIn(16, steps["right flipper button held"]["transitioned_solenoid_addresses"])
		for name in ("nba-nba_802-gameplay-probe.json", "nba-nba_801-gameplay-probe.json", "nba-nba_802-boot-start.json", "nba-nba_801-boot-start.json", "nba-nba_802-bumper-sling-probe.json"):
			evidence = self.summary(name)
			observed = {n for item in evidence["runtime"]["observations"].get("named_action_observations", []) for n in item["transitioned_solenoid_addresses"]} | set(evidence["runtime"]["observations"].get("solenoid_addresses_seen", []))
			self.assertNotIn(33, observed, name)
			self.retained(evidence, name)

	def test_summaries_reproduce_from_the_retained_runs(self) -> None:
		"""Every committed summary, frame hashes and transitions included, is what the retained runs derive."""
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		roms = Path(os.environ.get("PINMAME_ROM_LIBRARY_ROOT", r"L:\Visual Pinball\VPinMAME\roms"))
		if not root or not (roms / "nba_802.zip").is_file():
			self.skipTest("retained harness runs or the ROM library are not available")
		import build_external_evidence_manifest as manifest
		import nba_runtime as runtime

		# Read-only: verify each run directory's manifest instead of rewriting it or copying the scenario.
		seal = mock.patch.object(runtime, "seal", lambda directory, driver, scenario: manifest.check_manifest(directory, driver))
		write = mock.patch.object(runtime.manifest, "write_manifest", manifest.check_manifest)
		with seal, write:
			rebuilt = json.loads(json.dumps(runtime.build_all(Path(root))))
		committed = {path.name: load_json(path) for path in RUNTIME_ROOT.glob("nba-*.json")}
		self.assertEqual(set(committed), set(rebuilt))
		for name, document in committed.items():
			self.assertEqual(document, rebuilt[name], name)
		# The comparison sees a single changed frame hash.
		mutated = json.loads(json.dumps(committed["nba-nba_802-switch-test-sweep.json"]))
		mutated["runtime"]["observations"]["diagnostic_snapshots"][5]["pixel_sha256"] = "0" * 64
		self.assertNotEqual(mutated, rebuilt["nba-nba_802-switch-test-sweep.json"])

	def test_fast_flip_diagnostic_is_retained(self) -> None:
		source = self.sources[dev.RT_FASTFLIP]
		self.assertEqual("external:pinmame-review-artifacts/nba-2009/diagnostics/fastflip-getter-nba_802", source["uri"])
		text = (EXCERPT_ROOT / "fast-flip-diagnostic.md").read_text(encoding="utf-8")
		self.assertIn(source["sha256"], text)
		self.assertIn("`0100080000000004 get33=1`", text)
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		import build_external_evidence_manifest as manifest

		directory = Path(root) / "nba-2009" / "diagnostics" / "fastflip-getter-nba_802"
		self.assertEqual(source["sha256"], hashlib.sha256((directory / "run.json").read_bytes()).hexdigest())
		digest = manifest.check_manifest(directory, "nba_802")
		self.assertIn(digest, text)
		log = (directory / "fastflip-word.json").read_bytes()
		self.assertIn(hashlib.sha256(log).hexdigest(), text)
		run = json.loads((directory / "run.json").read_text(encoding="utf-8"))
		self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
		self.assertNotIn(33, {event["number"] for event in run["events"] if event.get("event") == "solenoid"})


if __name__ == "__main__":
	unittest.main()
