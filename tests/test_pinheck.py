from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location("curate_pinheck", ROOT / "tools" / "curate_pinheck.py")
CURATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CURATOR)
RUNTIME = load_json(ROOT / "tools" / "pinheck_runtime.json")
PROFILE = load_json(ROOT / "controllers" / "pinmame" / "pinheck.json")
GAMES = CURATOR.GAMES


def addresses(rules: list[dict]) -> set[int]:
	return {n for rule in rules for n in range(rule["minimum"], rule["maximum"] + 1)}


class PinheckDefinitionTests(unittest.TestCase):
	def test_curator_output_matches_the_committed_artifacts(self) -> None:
		for game in GAMES:
			for path, payload in CURATOR.artifacts(game).items():
				with self.subTest(path=path.as_posix()):
					self.assertEqual(payload, (ROOT / path).read_bytes().replace(b"\r\n", b"\n"))

	def test_catalog_maps_each_driver_to_its_curated_record(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		drivers = {driver["id"]: driver for driver in catalog["drivers"]}
		for game, config in GAMES.items():
			with self.subTest(game=game):
				self.assertEqual(config["machine"], drivers[game]["machine_id"])
				self.assertEqual("pinheck", drivers[game]["clone_of"])
				self.assertEqual(game, drivers[game]["root_driver"])
				self.assertFalse((ROOT / "machines" / "stubs" / f"{game}.json").exists())

	def test_every_profile_address_is_enumerated_once(self) -> None:
		groups = {group["id"]: addresses(group["address_rules"]) for group in PROFILE["groups"]}
		for game, config in GAMES.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
			for group, expected in groups.items():
				devices = [d["binding"]["device"] for d in definition["inputs"] + definition["outputs"] if d["binding"]["group"] == group]
				with self.subTest(game=game, group=group):
					self.assertEqual(len(devices), len(set(devices)))
					self.assertEqual(expected, set(devices))

	def test_the_rom_switch_grid_proves_the_matrix_and_cabinet_formulas(self) -> None:
		for game in GAMES:
			drawn = RUNTIME["games"][game]["runs"]["switch"]["grid"]["drawn_by_public"]
			with self.subTest(game=game):
				for n in range(64):
					self.assertEqual([f"matrix {n}"], drawn[str(CURATOR.public_number(n))])
				for address in (2, 7, 8, 94):
					self.assertEqual([f"cabinet {address if address < 9 else address - 82}"], drawn[str(address)])
				self.assertEqual(["cabinet 3"], drawn["112"])
				self.assertEqual(["cabinet 4"], drawn["114"])
				self.assertEqual([], drawn["98"])

	def test_solenoid_test_fires_exactly_coil_plus_one(self) -> None:
		for game in GAMES:
			with self.subTest(game=game):
				names = CURATOR.rom_coils(game)
				self.assertEqual(list(range(1, 25)), sorted(names))

	def test_lamp_test_numbers_every_matrix_lamp_and_gi_output(self) -> None:
		for game in GAMES:
			with self.subTest(game=game):
				lamps = CURATOR.rom_lamps(game)
				self.assertEqual(64, len(lamps))
				gi = CURATOR.rom_gi(game)
				self.assertEqual("PLAYFIELD GI #0" if game == "amh" else "PLAYFIELD GI GI = 1", gi[44])
				self.assertEqual("BACKBOX GI #0" if game == "amh" else "BACKBOX GI GI = 0", gi[32])

	def test_game_start_keeps_named_gi_steady_and_flashers_off(self) -> None:
		# The observed GI header mapping: chart pin k is public 25 + k (k < 8) or 29 + k.
		for game in ("dominos", "rzspook", "jetsons"):
			definition = load_json(ROOT / "machines" / "partial" / f"{GAMES[game]['stem']}.json")
			named = {d["binding"]["device"]: d["kind"] for d in definition["outputs"]
			         if d["id"].startswith("gi.") and d["availability"] == "used"}
			seconds = [step for step in RUNTIME["games"][game]["runs"]["game"]["steps"] if step["label"].startswith("Game second")]
			with self.subTest(game=game):
				self.assertTrue(any(kind == "gi" for kind in named.values()))
				self.assertTrue(any(kind == "flasher" for kind in named.values()))
				for address, kind in named.items():
					lit = [address in step["active_solenoids"] for step in seconds]
					if kind == "gi":
						self.assertTrue(all(lit), address)
					else:
						self.assertLess(sum(lit), len(lit), address)

	def test_switch_polarity_and_flipper_buttons(self) -> None:
		for game, config in GAMES.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
			inputs = {d["binding"]["device"]: d for d in definition["inputs"]}
			with self.subTest(game=game):
				self.assertTrue(all(d.get("normally_closed") is False for d in inputs.values() if d["availability"] == "used"))
				self.assertEqual(["flipper.lower.right.button"], inputs[112]["roles"])
				self.assertEqual(["flipper.lower.left.button"], inputs[114]["roles"])
				self.assertTrue(inputs[1]["initial_active"])
				self.assertTrue(all(inputs[address].get("initial_active") for address in config["trough"]))
				self.assertEqual({"platform": "pinmame.pinheck", "hardware_generation": "0x10000000000000",
				                  "inversion_applied_by_emulator": True}, definition["controller"])

	def test_records_stay_partial_with_explicit_blockers(self) -> None:
		for game, config in GAMES.items():
			definition = load_json(ROOT / "machines" / "partial" / f"{config['stem']}.json")
			with self.subTest(game=game):
				self.assertEqual("partial", definition["coverage"]["status"])
				expected = ["input_semantics"] if game == "dominos" else []
				self.assertEqual([*expected, "output_semantics", "spatial_placement"], definition["coverage"]["missing"])
				unknown = [d for d in definition["outputs"] if d["availability"] == "unknown"]
				self.assertTrue(unknown)

	def test_scenarios_are_generated(self) -> None:
		completed = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "pinheck_harness_scenarios.py"), "--check"],
		                           capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

	def test_runtime_summary_matches_the_retained_runs(self) -> None:
		review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not review_root:
			self.skipTest("retained harness runs are not available")
		import pinheck_runtime
		self.assertEqual((ROOT / "tools" / "pinheck_runtime.json").read_bytes(), pinheck_runtime.payload(Path(review_root)))


if __name__ == "__main__":
	unittest.main()
