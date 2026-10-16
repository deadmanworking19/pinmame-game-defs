"""Fail-closed tests for the Bally Paragon (1979) definition.

Paragon's printed solenoid numbers are test order, its lamp functions come from the board chain plus
its own lamp sheets, and its placements were checked against the manual's Figure V. Each of those
is asserted separately, against the retained runtime summary where the ROM decided it, so a
regression names the fact that broke.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "paragon-1979.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "paragon-1979.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "paragon-1979.md"
SUMMARY_PATH = ROOT / "evidence" / "runtime" / "by35" / "paragon-1979-harness.json"
SPATIAL_SEED = ROOT / "tools" / "seeds" / "bally" / "paragon-1979-spatial.json"
CALLOUT_SEED = ROOT / "tools" / "seeds" / "bally" / "paragon-1979-callouts.json"
REPORT_JSON = ROOT / "reports" / "spatial" / "bally" / "paragon-1979.json"
REPORT_MD = ROOT / "reports" / "spatial" / "bally" / "paragon-1979.md"

# Printed solenoid self-test number -> (public address, device id), as paired by the ROM's own test.
TEST_TO_PUBLIC = {
	1: (7, "device.outhole-kicker"), 2: (6, "device.knocker"), 3: (8, "device.treasure-chamber-saucer-kicker"),
	4: (10, "device.paragon-saucer-kicker"), 5: (9, "device.golden-cliffs-saucer-kicker"), 6: (14, "device.left-slingshot"),
	7: (15, "device.right-slingshot"), 8: (11, "device.left-thumper-bumper"), 9: (12, "device.right-thumper-bumper"),
	10: (1, "device.bottom-thumper-bumper"), 11: (13, "device.center-thumper-bumper"), 12: (2, "device.in-line-drop-target-reset"),
	13: (17, "device.waterfall-drop-target-reset"), 14: (18, "device.coin-lockout-door"), 15: (19, "device.k1-relay-flipper-enable"),
}
# Playfield switch -> the coil its closure fires in gameplay.
SWITCH_TO_COIL = {36: 14, 35: 15, 40: 11, 39: 12, 37: 1, 38: 13, 31: 8, 32: 9, 24: 10}
UNUSED_SWITCHES = {5, 12, 13, 14, 15, 20, 21, 25, *range(41, 49)}
BACKBOX_LAMPS = {11: "Shoot again", 13: "Ball in play", 27: "Match", 29: "High score to date", 45: "Game over", 61: "Tilt"}
# The plug-connector sheet's Table B: the A5 J2 pins routed on to the playfield, and their lamps.
TABLE_B = {"A5J2-14": 15, "A5J2-2": 47, "A5J2-15": 31, "A5J2-16": 14, "A5J2-20": 30, "A5J2-1": 63, "A5J2-6": 46, "A5J2-7": 62}
LAMP_ADDRESSES = [n for n in range(1, 64) if n % 16 != 0]


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def file_digest(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


class ParagonDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.summary = load(SUMMARY_PATH)
		cls.seed = load(SPATIAL_SEED)
		cls.inputs = cls.definition["inputs"]
		cls.outputs = cls.definition["outputs"]
		cls.switches = {d["binding"]["device"]: d for d in cls.inputs if d["binding"]["group"] == "pinmame.input.switch"}
		cls.dips = {d["binding"]["device"]: d for d in cls.inputs if d["binding"]["group"] == "pinmame.input.dip"}
		cls.solenoids = {d["binding"]["device"]: d for d in cls.outputs if d["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {d["binding"]["device"]: d for d in cls.outputs if d["binding"]["group"] == "pinmame.output.lamp"}

	def placement(self, device: dict, index: int = 0) -> tuple[float, float]:
		item = device["spatial"]["placements"][index]
		return item["x"], item["y"]

	# ------------------------------------------------------------- identity --
	def test_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.paragon.1979", "Paragon", "Bally", 1979, 1755, "GrXy3-ML0Ey"), (machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["opdb_id"]))
		self.assertEqual({"width": 1257.0, "height": 1974.0}, {k: machine["playfield"][k] for k in ("width", "height")})
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_drivers_and_the_seven_digit_conversion(self) -> None:
		drivers = {d["id"]: d for d in self.definition["drivers"]}
		self.assertEqual({"paragon", "paragonb", "paragonc", "paragond"}, set(drivers))
		self.assertEqual("compatible", drivers["paragonb"]["physical_compatibility"])
		self.assertEqual({1, 9, 17, 25}, {o["segment_start"] for o in drivers["paragonb"]["display_overrides"]})
		self.assertEqual({7}, {o["width"] for o in drivers["paragonb"]["display_overrides"]})
		for driver in ("paragon", "paragonc", "paragond"):
			self.assertEqual("identical", drivers[driver]["physical_compatibility"], driver)
			self.assertNotIn("display_overrides", drivers[driver])
		self.assertEqual(sorted(drivers), sorted(self.summary["driver_ids"]))

	def test_no_other_bally_machine_id_or_driver_appears(self) -> None:
		"""The lamp chain is borrowed from the Kiss record by reasoning, never by copying its device data."""
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign_drivers = {d["id"] for d in catalog["drivers"] if d["machine_id"].startswith("bally.") and d["machine_id"] != "bally.paragon.1979"}
		self.assertIn("kiss", foreign_drivers)
		text = json.dumps(self.definition) + KNOWLEDGE_PATH.read_text(encoding="utf-8")
		tokens = set(re.findall(r"[a-z0-9_]{3,}", text))
		self.assertEqual(set(), tokens & foreign_drivers)
		foreign_machines = {m["id"] for m in catalog["machines"] if m["id"] != "bally.paragon.1979"}
		self.assertEqual([], [m for m in foreign_machines if m in text])

	# ----------------------------------------------------------- solenoids --
	def test_printed_test_numbers_are_paired_by_the_rom(self) -> None:
		observed = self.summary["runtime"]["observations"]["physical_service_solenoid_to_public"]
		self.assertEqual({str(t): p for t, (p, _) in TEST_TO_PUBLIC.items()}, observed)
		for test, (public, device_id) in TEST_TO_PUBLIC.items():
			device = self.solenoids[public]
			self.assertEqual(device_id, device["id"], public)
			self.assertIn({"namespace": "manual.self-test", "value": str(test)}, device["aliases"], public)

	def test_unused_and_missing_solenoid_addresses(self) -> None:
		self.assertEqual({3, 4, 5, 20}, {a for a, d in self.solenoids.items() if d["availability"] == "unused"})
		self.assertNotIn(16, self.solenoids)
		self.assertIn("power-on pulse", self.solenoids[20]["physical"]["notes"])
		seen = set(self.summary["runtime"]["observations"]["solenoid_addresses_seen"])
		self.assertEqual(set(), seen & {3, 4, 5})
		self.assertEqual(set(range(1, 16)) | set(range(17, 21)) | {46, 48}, set(self.solenoids))

	def test_gameplay_closures_fire_their_own_coils(self) -> None:
		notes = self.summary["runtime"]["observations"]["runs"]["gameplay-paragon"]["note"]
		for switch, coil in SWITCH_TO_COIL.items():
			self.assertIn(f"Fired by switch {switch}", self.solenoids[coil]["physical"]["notes"].replace("Fired by the ball resting on switch", "Fired by switch"), coil)
		self.assertIn("thumper bumpers 40, 39, 37 and 38 fired 11, 12, 1 and 13", notes)
		self.assertIn("saucers 31, 32 and 24 fired 8, 9 and 10", notes)
		relationships = {(r["source"], r["destination"]) for r in self.definition["relationships"]}
		for switch, coil in SWITCH_TO_COIL.items():
			self.assertIn((self.switches[switch]["id"], self.solenoids[coil]["id"]), relationships)

	def test_flipper_outputs_drive_two_flippers_each(self) -> None:
		for address, side in ((46, "right"), (48, "left")):
			device = self.solenoids[address]
			self.assertEqual(f"device.{side}-flippers", device["id"])
			self.assertEqual(2, device["physical"]["quantity"])
			self.assertEqual(2, len(device["spatial"]["placements"]))
			self.assertEqual("validated", device["spatial"]["status"])
		self.assertIn("three flippers", self.solenoids[46]["physical"]["notes"])
		self.assertEqual("used", self.switches[82]["availability"])
		self.assertEqual("used", self.switches[84]["availability"])
		self.assertEqual("unused", self.switches[81]["availability"])
		self.assertEqual("unused", self.switches[83]["availability"])

	# ------------------------------------------------------------ switches --
	def test_switch_inventory(self) -> None:
		self.assertEqual(set(range(-7, -4)) | set(range(1, 49)) | {81, 82, 83, 84}, set(self.switches))
		self.assertEqual(UNUSED_SWITCHES | {81, 83}, {a for a, d in self.switches.items() if d["availability"] == "unused"})
		self.assertEqual(set(range(1, 33)), set(self.dips))
		for address, device in self.switches.items():
			if device["availability"] == "used":
				self.assertIs(False, device["normally_closed"], address)

	def test_parallel_contacts_have_one_placement_each(self) -> None:
		for address, quantity in {7: 3, 16: 2, 27: 2, 34: 3}.items():
			self.assertEqual(quantity, self.switches[address]["physical"]["quantity"], address)
		self.assertEqual(2, len(self.switches[27]["spatial"]["placements"]))
		self.assertEqual(3, len(self.switches[34]["spatial"]["placements"]))

	def test_switch_test_showed_every_address(self) -> None:
		note = self.summary["runtime"]["observations"]["runs"]["switch-test-paragon"]["note"]
		self.assertIn("public 1 to 40", note)

	def test_library_defaults_are_not_taken_as_names(self) -> None:
		self.assertEqual("switch.in-line-drop-target-c", self.switches[2]["id"])
		self.assertEqual("switch.coin-i-left", self.switches[10]["id"])
		self.assertEqual("switch.coin-ii-middle", self.switches[11]["id"])

	# ---------------------------------------------------------------- lamps --
	def test_sixty_lamps_all_used(self) -> None:
		self.assertEqual(LAMP_ADDRESSES, sorted(self.lamps))
		self.assertTrue(all(d["availability"] == "used" for d in self.lamps.values()))
		self.assertEqual(LAMP_ADDRESSES, self.summary["runtime"]["observations"]["lamp_addresses_seen"])

	def test_backbox_lamps(self) -> None:
		backbox = {a for a, d in self.lamps.items() if d["spatial"]["status"] == "not_applicable"}
		self.assertEqual(set(BACKBOX_LAMPS), backbox)
		for address, label in BACKBOX_LAMPS.items():
			self.assertEqual(label, self.lamps[address]["label"])
		self.assertEqual("Same player shoots again", self.lamps[43]["label"])
		self.assertEqual("playfield", self.lamps[43]["physical"]["location"])

	def test_table_b_pins_are_the_j2_playfield_lamps(self) -> None:
		j2 = {d["wiring"]["drive_connection"]: a for a, d in self.lamps.items() if d["wiring"]["drive_connection"].startswith("A5J2-") and a not in BACKBOX_LAMPS}
		self.assertEqual(TABLE_B, j2)

	def test_lamp_rows_run_in_their_printed_order(self) -> None:
		"""Cheap guards on the art identification: letter rows spell PARAGON left to right."""
		for row in ((9, 25, 41, 57, 10, 26, 42), (7, 23, 39, 55, 8, 24, 40)):
			xs = [self.placement(self.lamps[a])[0] for a in row]
			self.assertEqual(sorted(xs), xs, row)
		spinner_ys = [self.placement(self.lamps[a])[1] for a in (14, 30, 46, 62)]
		self.assertEqual(sorted(spinner_ys, reverse=True), spinner_ys)
		treasure = [self.placement(self.lamps[a])[1] for a in (53, 54, 56)]
		self.assertEqual(sorted(treasure, reverse=True), treasure)
		self.assertEqual({"1": 22, "2": 6, "33": 14}, self.summary["runtime"]["observations"]["switch_to_lamp"])

	# --------------------------------------------------------------- spatial --
	def test_placements_match_the_frozen_table_objects(self) -> None:
		objects = self.seed["objects"]
		for address, device in self.lamps.items():
			if address not in BACKBOX_LAMPS:
				self.assertEqual((objects[f"L{address}"]["x"], objects[f"L{address}"]["y"]), self.placement(device), address)
		for name, address in (("Bumper1", 37), ("Bumper2", 38), ("Bumper3", 39), ("Bumper4", 40), ("Drain", 8), ("sw33", 33)):
			self.assertEqual((objects[name]["x"], objects[name]["y"]), self.placement(self.switches[address]), address)
		for name, item in objects.items():
			self.assertAlmostEqual(item["raw_x"] / self.seed["bounds"]["right"], item["x"], places=5, msg=name)
			self.assertAlmostEqual(item["raw_y"] / self.seed["bounds"]["bottom"], item["y"], places=5, msg=name)

	def test_callout_check_decides_exactly_two_blockers(self) -> None:
		seed = load(CALLOUT_SEED)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		failing = {pid for pid, d in decisions["placements"].items() if not d["agrees"]}
		self.assertEqual({"switch.500-point-rebound.upper-rebound", "switch.spinner.sensor"}, failing)
		unvalidated = {
			p["id"] for d in self.inputs + self.outputs for p in (d.get("spatial") or {}).get("placements", []) if p["provenance"]["status"] != "validated"
		}
		self.assertEqual(failing, unvalidated)
		self.assertEqual({"status": "partial", "missing": ["spatial_placement"]}, {k: self.definition["coverage"][k] for k in ("status", "missing")})
		self.assertIn("**partial**", KNOWLEDGE_PATH.read_text(encoding="utf-8"))

	def test_flipper_controls_are_within_the_limit(self) -> None:
		seed = load(CALLOUT_SEED)
		controls = seed["pages"]["figure-v-solenoids"]["controls"]
		offsets = drawing_callouts.leave_one_out([(tuple(c["pixel"]), tuple(c["xy"])) for c in controls])
		for control, offset in zip(controls, offsets):
			self.assertLess(offset, seed["limit"], control["object"])
			self.assertEqual((self.seed["objects"][control["object"]]["x"], self.seed["objects"][control["object"]]["y"]), tuple(control["xy"]))

	def test_spatial_report_matches_the_definition(self) -> None:
		report = load(REPORT_JSON)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(file_digest(DEFINITION_PATH), report["definition_sha256"])
		ids = {d["id"] for d in self.inputs + self.outputs}
		for disclosure in report["projection_disclosures"]:
			self.assertTrue(set(disclosure["devices"]) <= ids, disclosure["devices"])
		self.assertEqual([], report["unplaced_physical_devices"])
		self.assertEqual(sorted(["switch.500-point-rebound.upper-rebound", "switch.spinner.sensor"]), report["unvalidated_placements"])

	# ----------------------------------------------------------- determinism --
	def test_curator_reproduces_the_artifacts(self) -> None:
		result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "curate_paragon.py"), "--check"], capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, result.returncode, result.stderr)

	def test_curator_detects_drift_in_an_isolated_copy(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			copies = {name: base / name for name in ("definition.json", "knowledge.md", "report.json", "report.md")}
			for name, source in zip(copies, (DEFINITION_PATH, KNOWLEDGE_PATH, REPORT_JSON, REPORT_MD)):
				copies[name].write_bytes(source.read_bytes())
			command = [
				sys.executable, "-B", str(ROOT / "tools" / "curate_paragon.py"), "--check",
				"--definition", str(copies["definition.json"]), "--knowledge", str(copies["knowledge.md"]),
				"--report-json", str(copies["report.json"]), "--report-md", str(copies["report.md"]),
			]
			untouched = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertEqual(0, untouched.returncode, untouched.stderr)
			copies["definition.json"].write_bytes(copies["definition.json"].read_bytes().replace(b'"Paragon"', b'"Paragone"', 1))
			tampered = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertNotEqual(0, tampered.returncode)
			self.assertIn("canonical content mismatch", tampered.stderr)

	def test_excerpts_are_attached_to_their_bytes(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], file_digest(ROOT / excerpt["path"]), excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], file_digest(ROOT / excerpt["image"]), excerpt["id"])

	# ------------------------------------------------- retained evidence roots --
	def test_runtime_summary_is_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		runs = Path(root) / "paragon-1979" / "harness"
		for run in self.summary["runtime"]["raw_runs"]:
			directory, driver = run["retained_from"].split("/harness/")[1].rsplit("/", 1)[0].split("/")
			path = runs / directory / driver / "run.json"
			self.assertEqual(run["sha256"], file_digest(path), run["name"])
			if "scenario_path" in run:
				self.assertEqual(run["scenario_sha256"], file_digest(ROOT / run["scenario_path"]), run["name"])
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "paragon_runtime_summary.py"), "--runs", str(runs), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(self.summary["source"]["sha256"], check_manifest(runs, "paragon"))

	def test_table_geometry_is_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		base = Path(root) / "bally" / "paragon-1979"
		vpx = base / "source" / "Paragon (Bally 1979).vpx"
		self.assertEqual(self.seed["table_sha256"], file_digest(vpx))
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "paragon_spatial_seed.py"), "--extracted", str(base / "extracted-vpxtool"), "--vpx", str(vpx), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(self.seed["extraction_manifest_sha256"], check_manifest(base / "extracted-vpxtool", "paragon"))
		for name, digest in {"Bally.vbs": "d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c", "core.vbs": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"}.items():
			self.assertEqual(digest, file_digest(base / "library" / name), name)

	def test_manuals_and_callout_renders_are_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		base = Path(root) / "by-machine" / "bally.paragon.1979"
		sources = {s["id"]: s for s in self.definition["sources"]}
		for source_id, name in (
			("manual.bally.paragon.1979", "Bally_1979_Paragon_Manual.pdf"),
			("schematic.bally.paragon.1979", "Bally_1979_Paragon_Schematic_Diagrams_paginated.pdf"),
			("ipdb.1755.kmiec-treasure-chamber", "Bally_1979_Paragon_Greg_Kmiec_Discusses_Treasure_Chamber_Design.pdf"),
			("ipdb.1755", "ipdb1755.html"),
		):
			self.assertEqual(sources[source_id]["sha256"], file_digest(base / name), name)
		artifacts = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		checked = drawing_callouts.verify_retained(load(CALLOUT_SEED), ROOT, Path(root), Path(artifacts) if artifacts else None)
		self.assertGreaterEqual(checked, 2)


if __name__ == "__main__":
	unittest.main()
