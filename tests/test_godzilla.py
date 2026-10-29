"""Checks for the retained Godzilla factory-reference evidence.

These do not assert that the machine's I/O inventory or spatial data is complete.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "machines/partial/sega/godzilla-1998.json"
MANUAL_SHA256 = "fc71e6584b2a8ad715100f94b5d4d690b0cd3864cd9abd6746c2441ad4d6c1c5"
SCRIPT_SHA256 = "95d77a6678cc735792091e582abd66983a709b28e9bde307679d10029598949b"


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def required_evidence_file(root_variable: str, relative_path: str, digest: str) -> None:
	"""A configured evidence root must exist and contain the pinned bytes."""
	value = os.environ.get(root_variable)
	if not value:
		raise unittest.SkipTest(f"{root_variable} is not configured")
	path = Path(value) / relative_path
	if not path.is_file():
		raise AssertionError(f"Configured {root_variable} does not contain {relative_path}: {path}")
	if sha256(path) != digest:
		raise AssertionError(f"Evidence hash mismatch: {path}")


class GodzillaEvidenceTests(unittest.TestCase):
	def setUp(self) -> None:
		definition = load_json(MACHINE)
		self.assertEqual("partial", definition["coverage"]["status"])
		self.source = next(s for s in definition["sources"] if s["id"] == "manual.sega.godzilla.1998.gameex")
		self.excerpts = {Path(e["path"]).name: e for e in self.source["excerpts"]}

	def test_manual_and_literal_transcriptions_are_pinned(self) -> None:
		self.assertEqual(MANUAL_SHA256, self.source["sha256"])
		self.assertEqual(
			{"coils-front.md", "dip-settings-front.md", "gi-wiring.md", "lamp-matrix-front.md", "switch-matrix-front.md", "trough-parts.md", "factory-location-drawings.md", "mechanism-facts.md", "flipper-wiring.md"},
			set(self.excerpts),
		)
		for excerpt in self.excerpts.values():
			with self.subTest(excerpt=excerpt["id"]):
				self.assertEqual(excerpt["sha256"], sha256(ROOT / excerpt["path"]))
				self.assertTrue(excerpt["transcribed_by"])
		self.assertTrue(self.excerpts["dip-settings-front.md"]["reviewed"])
		self.assertTrue(self.excerpts["trough-parts.md"]["reviewed"])
		for name in ("switch-matrix-front.md", "lamp-matrix-front.md", "coils-front.md", "gi-wiring.md"):
			self.assertFalse(self.excerpts[name]["reviewed"])

	def test_specific_printed_cells_and_unresolved_reads(self) -> None:
		def read(name: str) -> str:
			return (ROOT / self.excerpts[name]["path"]).read_text(encoding="utf-8")

		switches = read("switch-matrix-front.md")
		self.assertIn("14 4-BALL TROUGH VUK OPTO", switches)
		self.assertIn("15 4-BALL STACKING OPTO", switches)
		self.assertIn("1 LEFT SAV-A-BALL (UK ONLY)", switches)
		self.assertIn("8 RIGHT SAV-A-BALL (UK ONLY)", switches)
		lamps = read("lamp-matrix-front.md")
		self.assertIn("40 UP/DOWN POST (UK ONLY)", lamps)
		self.assertIn("80 NOT USED", lamps)
		coils = read("coils-front.md")
		self.assertIn("#8 EUROPEAN TOKEN DISPENSER | Q8 | BRN-GRY | J8-P9", coils)
		self.assertIn("#21 LT OUTLANE (UK ONLY)", coils)
		self.assertIn("[part number unclear]", coils)
		gi = read("gi-wiring.md")
		self.assertIn("J15-P8 to J15-P3 (Fuse F26)", gi)
		self.assertIn("7 ea. #44 Bulb plus 2 ea. #555 Bulb on coin door", gi)
		trough = read("trough-parts.md")
		self.assertIn("Micro-Switch (Roller Actuator) | 3 | 180-5119-00", trough)
		self.assertIn("Dual OPTO Receiver (REC) Board | 1 | 520-5174-00", trough)

	def test_retained_manual_when_configured(self) -> None:
		required_evidence_file("PINMAME_MANUALS_ROOT", "by-machine/sega.godzilla.1998/godzilla-gameex-manual.pdf", MANUAL_SHA256)

	def test_retained_script_when_configured(self) -> None:
		required_evidence_file("PINMAME_VPX_SOURCES_ROOT", "sega/godzilla-1998/extracted/script.vbs", SCRIPT_SHA256)

	def test_configured_root_fails_closed(self) -> None:
		previous = os.environ.get("PINMAME_MANUALS_ROOT")
		os.environ["PINMAME_MANUALS_ROOT"] = str(ROOT / "this-evidence-root-must-not-exist")
		try:
			with self.assertRaisesRegex(AssertionError, "does not contain"):
				required_evidence_file("PINMAME_MANUALS_ROOT", "by-machine/sega.godzilla.1998/godzilla-gameex-manual.pdf", MANUAL_SHA256)
		finally:
			if previous is None:
				os.environ.pop("PINMAME_MANUALS_ROOT", None)
			else:
				os.environ["PINMAME_MANUALS_ROOT"] = previous

	def test_curator_check_is_deterministic_and_rejects_bad_root(self) -> None:
		environment = os.environ.copy()
		environment["PYTHONPATH"] = str(ROOT / "src")
		environment["PYTHONDONTWRITEBYTECODE"] = "1"
		command = [sys.executable, "-B", str(ROOT / "tools/curate_godzilla.py"), "--check"]
		for _ in range(2):
			result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, check=False)
			self.assertEqual(0, result.returncode, result.stderr)
		environment["PINMAME_MANUALS_ROOT"] = str(ROOT / "this-evidence-root-must-not-exist")
		result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, check=False)
		self.assertNotEqual(0, result.returncode)
		self.assertIn("does not contain the pinned evidence", result.stderr)

	def test_curator_rejects_noncanonical_seed_bytes(self) -> None:
		from tools import curate_godzilla

		with tempfile.TemporaryDirectory() as directory:
			seed = Path(directory) / "seed.json"
			seed.write_bytes(curate_godzilla.SEED.read_bytes() + b"\n")
			with patch.object(curate_godzilla, "SEED", seed):
				with self.assertRaisesRegex(ValueError, "not in canonical byte format"):
					curate_godzilla.build()

	def test_public_inventory_and_factory_semantics(self) -> None:
		definition = load_json(MACHINE)
		def group(collection: str, name: str) -> dict[int, dict]:
			return {d["binding"]["device"]: d for d in definition[collection] if d["binding"]["group"] == name}
		switches = group("inputs", "pinmame.input.switch")
		self.assertEqual(set(range(-3, 1)) | set(range(1, 65)) | set(range(81, 89)), set(switches))
		self.assertEqual(set(range(1, 9)), set(group("inputs", "pinmame.input.dip")))
		solenoids = group("outputs", "pinmame.output.solenoid")
		lamps = group("outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 51)), set(solenoids))
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertEqual({0}, set(group("outputs", "pinmame.output.gi")))
		self.assertEqual("switch.trough-vuk-opto", switches[14]["id"])
		self.assertEqual("switch.trough-stacking-opto", switches[15]["id"])
		self.assertEqual(["pinmame.core.46e1a01a0f73"], switches[-3]["provenance"]["source_refs"])
		self.assertEqual(["pinmame.core.46e1a01a0f73"], switches[-3]["spatial"]["provenance"]["source_refs"])
		for address in (14, 15):
			self.assertEqual("opto", switches[address]["physical"]["switch_type"])
			self.assertIs(switches[address]["normally_closed"], False)
		self.assertEqual([True, True, True, True, False], [switches[n]["initial_active"] for n in range(11, 16)])
		for address in (8, 21, 22, 23, 24):
			self.assertEqual("optional", solenoids[address]["availability"])
		self.assertEqual("optional", lamps[40]["availability"])
		for address in range(9, 14):
			self.assertEqual("coil", solenoids[address]["kind"])
			self.assertEqual("used", solenoids[address]["availability"])
		self.assertEqual("virtual", solenoids[45]["kind"])
		self.assertEqual("coil", solenoids[46]["kind"])
		self.assertEqual("virtual", solenoids[47]["kind"])
		self.assertEqual("coil", solenoids[48]["kind"])
		self.assertEqual(["flipper.lower.right"], solenoids[46]["roles"])
		self.assertEqual(["flipper.lower.left"], solenoids[48]["roles"])
		self.assertEqual(["flipper.lower.right.button"], switches[82]["roles"])
		self.assertEqual(["flipper.lower.left.button"], switches[84]["roles"])
		self.assertEqual("used", solenoids[15]["availability"])
		self.assertEqual(38, group("outputs", "pinmame.output.gi")[0]["physical"]["quantity"])
		self.assertNotIn("spatial", group("outputs", "pinmame.output.gi")[0])
		self.assertEqual({"identical", "unknown"}, {d["physical_compatibility"] for d in definition["drivers"]})
		self.assertEqual("unknown", next(d for d in definition["drivers"] if d["id"] == "godz_090")["physical_compatibility"])
		all_ids = {d["id"] for d in definition["inputs"] + definition["outputs"]}
		for mechanism in definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= all_ids)
		self.assertEqual({"mechanism.trough", "mechanism.auto-launch", "mechanism.ramp-diverter", "mechanism.captive-balls",
			"mechanism.shaker", "mechanism.uk-posts", "mechanism.token-dispenser", "mechanism.magnet-top-orbit",
			"mechanism.magnet-middle-playfield", "mechanism.magnet-bottom-playfield", "mechanism.magnet-left-lane"},
			{item["id"] for item in definition["mechanisms"]})
		self.assertIn("left turbo bumper", solenoids[9]["label"].lower())
		self.assertIn("right turbo bumper", solenoids[10]["label"].lower())
		self.assertIn("left slingshot", solenoids[12]["label"].lower())
		self.assertIn("right slingshot", solenoids[13]["label"].lower())
		self.assertIn("save new york", lamps[39]["label"].lower())
		self.assertIn("taxi", lamps[55]["label"].lower())

	def test_factory_coordinates_are_recomputed_from_pixels(self) -> None:
		from tools import curate_godzilla
		from tools.drawing_callouts import fit, apply
		seed = load_json(curate_godzilla.SPATIAL_SEED)
		self.assertEqual(curate_godzilla.SPATIAL_SHA256, sha256(curate_godzilla.SPATIAL_SEED))
		self.assertEqual(53, sum(len(v) for v in seed["pages"]["lamps"]["measurements"].values()))
		self.assertEqual(22, sum(len(v) for v in seed["pages"]["flashers"]["measurements"].values()))
		self.assertEqual([[741, 234], [806, 188]], [v["pixel"] for v in seed["pages"]["flashers"]["measurements"]["26"]])
		definition = load_json(MACHINE)
		for group, name in (("pinmame.output.lamp", "lamps"), ("pinmame.output.solenoid", "flashers")):
			page = seed["pages"][name]
			transform = fit([(c["pixel"], c["xy"]) for c in page["controls"]])
			for number, readings in page["measurements"].items():
				device = next(d for d in definition["outputs"] if d["binding"] == {"group":group, "device":int(number)})
				actual = device["spatial"]["placements"]
				self.assertEqual(len(readings), len(actual))
				for read, point in zip(readings, actual):
					expected = tuple(round(v, 6) for v in apply(transform, read["pixel"]))
					self.assertEqual(expected, (point["x"], point["y"]))
					self.assertEqual("observed", point["provenance"]["status"])
					self.assertTrue(0 <= point["x"] <= 1 and 0 <= point["y"] <= 1)
					self.assertEqual("emitter", point["role"])

	def test_each_configured_evidence_root_fails_closed(self) -> None:
		for variable in ("PINMAME_MANUALS_ROOT", "PINMAME_VPX_SOURCES_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"):
			with self.subTest(root=variable):
				env = os.environ.copy()
				env["PYTHONPATH"] = str(ROOT / "src")
				env["PYTHONDONTWRITEBYTECODE"] = "1"
				env[variable] = str(ROOT / "this-evidence-root-must-not-exist")
				result = subprocess.run([sys.executable,"-B",str(ROOT / "tools/curate_godzilla.py"),"--check"],
					cwd=ROOT,env=env,capture_output=True,text=True,check=False)
				self.assertNotEqual(0,result.returncode)

	def test_pinned_driver_source_when_configured(self) -> None:
		value = os.environ.get("PINMAME_SOURCE_CHECKOUT")
		if not value:
			self.skipTest("PINMAME_SOURCE_CHECKOUT is not configured")
		root = Path(value)
		games = (root / "src/wpc/segames.c").read_text(encoding="utf-8")
		se = (root / "src/wpc/se.c").read_text(encoding="utf-8")
		header = (root / "src/wpc/se.h").read_text(encoding="utf-8")
		self.assertIn("#define SE_SWMEMORYPROTECT -3", header)
		self.assertIn("Coin door memory protect switch", se)
		for name in ("godzilla", "godz_100", "godz_090"):
			self.assertIn(f"INITGAME({name},GEN_WS,se_dmd128x32,0)", games)
		self.assertIn("64 + core_gameData->hw.lampCol * 8", se)
		self.assertIn("CORE_FIRSTCUSTSOL - 1 + core_gameData->hw.custSol", se)
		self.assertIn("return ~core_getSwCol(selocals.swCol)", se)
		self.assertIn('strncasecmp(gn, "godzilla", 8)', se)

	def test_legacy_address_aliases_survive(self) -> None:
		definition = load_json(MACHINE)
		seed = load_json(ROOT / "tools/data/godzilla/definition.json")
		for section in ("inputs", "outputs"):
			new = {(d["binding"]["group"],d["binding"]["device"]):d for d in definition[section]}
			for old in seed[section]:
				key = (old["binding"]["group"],old["binding"]["device"])
				if key in new:
					legacy = {(a["namespace"],a["value"]) for a in old["aliases"] if a["namespace"].startswith("vpe-legacy.")}
					actual = {(a["namespace"],a["value"]) for a in new[key]["aliases"]}
					self.assertTrue(legacy <= actual, key)

	def test_runtime_scenarios_and_observation_boundaries(self) -> None:
		from tools import curate_godzilla
		for driver, (_, digest) in curate_godzilla.RUNTIME_EVIDENCE.items():
			with self.subTest(driver=driver):
				path = curate_godzilla.runtime_path(driver)
				self.assertEqual(digest, sha256(path))
				evidence = load_json(path)
				runtime = evidence["runtime"]
				self.assertEqual([driver], evidence["driver_ids"])
				self.assertEqual(driver, runtime["game"])
				self.assertEqual([], evidence["switches"])
				raw = runtime["raw_runs"][0]
				self.assertEqual(raw["scenario_sha256"], sha256(ROOT / raw["scenario_path"]))
				observations = runtime["observations"]["runs"][raw["name"]]
				self.assertEqual(driver == "godzilla", 15 in observations["solenoid_addresses_seen"])
				responses = {a["input_address"]: a for a in observations["named_action_observations"]}
				for switch, coils in {54: {1}, 53: {2}, 49: {9}, 50: {10}, 51: {11},
					59: {12}, 62: {13}, 82: {45, 46}, 84: {47, 48}}.items():
					self.assertTrue(coils <= set(responses[switch]["active_solenoid_addresses"]))
					self.assertEqual([], responses[switch]["observed_switch_addresses"])
					self.assertEqual([switch], responses[switch]["host_stimulus_switch_addresses"])

	def test_runtime_summaries_match_retained_traces_when_configured(self) -> None:
		from tools import curate_godzilla
		value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not value:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		for driver in curate_godzilla.RUNTIME_EVIDENCE:
			evidence = load_json(curate_godzilla.runtime_path(driver))
			runtime = evidence["runtime"]
			run = runtime["raw_runs"][0]
			path = Path(value) / run["retained_from"].removeprefix("external:pinmame-review-artifacts/")
			self.assertEqual(run["sha256"], sha256(path))
			raw = load_json(path)
			self.assertIsNone(raw["failure"])
			self.assertEqual(run["action_count"], len(raw["steps"]))
			observations = runtime["observations"]["runs"][run["name"]]
			self.assertEqual(observations["solenoid_addresses_seen"], sorted({
				e["number"] for e in raw["events"] if e["event"] == "solenoid" and e["state"]}))
			for observation in observations["named_action_observations"]:
				step = next(s for s in raw["steps"] if s["label"] == observation["label"])
				self.assertEqual(observation["input_address"], step["switch"])
				self.assertEqual(observation["active_solenoid_addresses"], sorted(
					e["number"] for e in step["transitions"]["solenoids"] if any(e["states"])))

	def test_drawing_placements_disclose_calibration_sources(self) -> None:
		from tools import curate_godzilla
		definition = load_json(MACHINE)
		for output in definition["outputs"]:
			if output["binding"]["group"] == "pinmame.output.lamp" or (
				output["binding"]["group"] == "pinmame.output.solenoid" and 25 <= output["binding"]["device"] <= 32):
				for placement in output.get("spatial", {}).get("placements", []):
					self.assertTrue({curate_godzilla.MANUAL, curate_godzilla.TABLE, curate_godzilla.SCRIPT}
						<= set(placement["provenance"]["source_refs"]))


if __name__ == "__main__":
	unittest.main()
