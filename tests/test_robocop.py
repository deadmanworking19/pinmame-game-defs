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
MACHINE_ID = "data-east.robocop.1989"
DEFINITION_PATH = ROOT / "machines" / "partial" / "data-east" / "robocop-1989.json"
SEED_PATH = ROOT / "tools" / "seeds" / "data-east" / "robocop-1989.json"
MANIFEST_PATH = ROOT / "tools" / "seeds" / "data-east" / "robocop-1989-extraction-manifest.json"
READINGS_PATH = ROOT / "tools" / "seeds" / "data-east" / "robocop-1989-service-readings.json"
REPORT_PATH = ROOT / "reports" / "spatial" / "data-east" / "robocop-1989.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "data-east" / "robocop-1989.md"
RUNTIME_PATH = ROOT / "evidence" / "runtime" / "data-east" / "robocop-service-walk.json"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "data-east.robocop.1989"
OWN_DRIVERS = {"robo_a29", "robo_a30", "robo_a34"}

# Independent fixtures, transcribed from the manual's printed matrix headers (printed pages 20 and 22).
SWITCH_DRIVE_CODES = [51, 52, 53, 54, 50, 56, 57, 58]
SWITCH_RETURN_CODES = [91, 92, 93, 94, 95, 96, 97, 98]
LAMP_DRIVE_CODES = [41, 42, 43, 40, 45, 46, 47, 48]
LAMP_RETURN_CODES = [21, 20, 23, 24, 25, 26, 27, 28]
UNUSED_SWITCHES = {2, 8, 9, 24, 39, 40, *range(49, 65)}
FLASH_SPLIT = {1: (4, 3), 2: (1, 0), 3: (3, 2), 4: (2, 1), 5: (2, 1), 6: (2, 1), 7: (4, 3), 8: (1, 0), 9: (4, 2), 12: (4, 2), 13: (4, 2), 14: (4, 1), 15: (4, 1)}
SPECIAL = {17: ("SP1", "Right Turbo Bumper"), 18: ("SP3", "Left Slingshot"), 19: ("SP4", "Left Turbo Bumper"), 20: ("SP6", "Unfitted Special-Solenoid Driver SP6"), 21: ("SP5", "Right Slingshot"), 22: ("SP2", "Center Turbo Bumper")}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class RoboCopDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.sources = {item["id"]: item for item in cls.definition["sources"]}
        cls.switches = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
        cls.solenoids = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
        cls.runtime = load_json(RUNTIME_PATH)

    def test_identity_and_driver_tree(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual((MACHINE_ID, "Data East", 1989, 1976, "Grlxe-MJ916"), (machine["id"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["opdb_id"]))
        self.assertEqual({"platform": "pinmame.dataeast", "hardware_generation": "0x1000", "inversion_applied_by_emulator": True}, self.definition["controller"])
        drivers = {item["id"]: item for item in self.definition["drivers"]}
        self.assertEqual(OWN_DRIVERS, set(drivers))
        self.assertNotIn("clone_of", drivers["robo_a34"])
        self.assertEqual({"robo_a34"}, {drivers[name]["clone_of"] for name in ("robo_a29", "robo_a30")})
        self.assertTrue(all(item["physical_compatibility"] == "identical" for item in drivers.values()))
        self.assertIn("does not hold it", drivers["robo_a29"]["variant_notes"])
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        rows = {item["id"]: item for item in catalog["drivers"]}
        for name in OWN_DRIVERS:
            self.assertEqual(MACHINE_ID, rows[name]["machine_id"])
            self.assertEqual("machines/partial/data-east/robocop-1989.json", rows[name]["definition"])
        self.assertFalse((ROOT / "machines" / "stubs" / "robo_a34.json").exists())

    def test_coverage_is_partial_with_named_blockers(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["output_semantics", "mechanism_behavior", "polarity", "spatial_placement"], coverage["missing"])
        self.assertEqual([], self.definition["conflicts"])
        report = load_json(REPORT_PATH)
        self.assertEqual(set(coverage["missing"]), {item["dimension"] for item in report["blockers"]})
        self.assertTrue(all(item["would_resolve"] for item in report["blockers"]))

    def test_full_address_enumeration(self) -> None:
        self.assertEqual({-7, -6, *range(1, 65), *range(81, 89)}, set(self.switches))
        self.assertEqual(set(range(1, 51)), set(self.solenoids))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        self.assertEqual([(0, 0, 16), (1, 20, 16)], [(item["controller_index"], item["segment_start"], item["width"]) for item in self.definition["displays"]])
        self.assertEqual(UNUSED_SWITCHES, {number for number in range(1, 65) if self.switches[number]["availability"] == "unused"})
        self.assertEqual({56}, {number for number, item in self.lamps.items() if item["availability"] == "unused"})
        self.assertEqual({20, 31, 32}, {number for number, item in self.solenoids.items() if item["availability"] == "unknown"})
        self.assertEqual({24, *range(33, 45), 49, 50}, {number for number, item in self.solenoids.items() if item["availability"] == "unused"})
        self.assertTrue(all(self.switches[number].get("initial_active") is True for number in (11, 12, 13)))
        self.assertTrue(all(self.switches[number]["normally_closed"] is False for number in range(1, 65) if number not in (15, 16)))

    def test_rom_service_test_names_agree_with_the_curated_labels(self) -> None:
        readings = load_json(READINGS_PATH)
        responses = self.runtime["runtime"]["observations"]["runs"]["robo-a34"]["named_action_observations"]
        switch_names = {item["diagnostic_address"]: item["interpreted_text"] for item in responses[0]["display_responses"][0::2]}
        lamp_names = {item["diagnostic_address"]: item["interpreted_text"] for item in responses[1]["display_responses"][0::2]}
        coil_names = {item["diagnostic_address"]: item["interpreted_text"] for item in responses[2]["display_responses"][0::2]}
        self.assertEqual(set(range(1, 65)), set(switch_names))
        self.assertEqual(set(range(1, 65)), set(lamp_names))
        self.assertEqual({*range(1, 17), *range(25, 33)}, set(coil_names))
        for number, name in switch_names.items():
            if number in (15, 16):
                self.assertEqual("LEFT FLIPPER" if number == 15 else "RIGHT FLIPPER", name)
            else:
                self.assertEqual(readings["switch_test"][str(number)], name, number)
                self.assertEqual(name == "NONE", number in UNUSED_SWITCHES, number)
        self.assertEqual("NONE", lamp_names[56])
        self.assertEqual({"NONE"}, {coil_names[31], coil_names[32]})
        self.assertIn("NONE", self.solenoids[31]["physical"]["notes"])

    def test_rom_wire_codes_match_the_manual_matrix_headers(self) -> None:
        responses = self.runtime["runtime"]["observations"]["runs"]["robo-a34"]["named_action_observations"]
        for observation, drives, returns in ((responses[0], SWITCH_DRIVE_CODES, SWITCH_RETURN_CODES), (responses[1], LAMP_DRIVE_CODES, LAMP_RETURN_CODES)):
            codes = {item["diagnostic_address"]: item["interpreted_text"] for item in observation["display_responses"][1::2]}
            self.assertEqual(set(range(1, 65)), set(codes))
            for number, text in codes.items():
                column, row = divmod(number - 1, 8)
                self.assertEqual(f"{returns[row]}-{drives[column]} {number:02d}", text, number)
        banks = {item["diagnostic_address"]: item["interpreted_text"] for item in responses[2]["display_responses"][1::2]}
        expected = {**{number: f"L{number:02d}" for number in range(1, 9)}, **{number: f"{number:02d}" for number in range(9, 17)}, **{number: f"R{number - 24:02d}" for number in range(25, 33)}}
        self.assertEqual(expected, banks)

    def test_flash_quantities_split_backbox_and_playfield(self) -> None:
        for number, (total, backbox) in FLASH_SPLIT.items():
            item = self.solenoids[number]
            self.assertEqual("flasher", item["kind"], number)
            self.assertEqual(total, item["physical"]["quantity"], number)
            self.assertEqual("playfield and backbox" if backbox else "playfield", item["physical"]["location"], number)
            self.assertIn(f"assigns {backbox} of them to the backbox", item["physical"]["notes"], number)
        self.assertEqual(19, sum(backbox for _total, backbox in FLASH_SPLIT.values()))
        self.assertEqual(("relay", "gi"), (self.solenoids[10]["kind"], self.solenoids[11]["kind"]))

    def test_special_solenoid_mapping_follows_the_de_permutation(self) -> None:
        for number, (printed, label) in SPECIAL.items():
            item = self.solenoids[number]
            self.assertEqual(label, item["label"], number)
            self.assertIn({"namespace": "manual.address", "value": printed}, item["aliases"], number)
            self.assertEqual("validated" if number == 20 else "candidate", item["provenance"]["status"], number)
        self.assertEqual("virtual", self.solenoids[20]["kind"])
        self.assertEqual([], [item for item in self.definition["relationships"] if item["destination"] in {f"coil.driver-{n}" for n in (31, 32)}])
        relay = sorted(item["destination"] for item in self.definition["relationships"] if item["source"] == "coil.driver-10")
        self.assertEqual(sorted(f"coil.driver-{number}" for number in range(25, 31)), relay)

    def test_lamp_planes_and_table_defects(self) -> None:
        for number in (41, 42, 43):
            self.assertEqual("back panel", self.lamps[number]["physical"]["location"])
            self.assertNotIn("spatial", self.lamps[number])
        self.assertIn("pulses 46 instead of 48", self.switches[46]["physical"]["notes"])
        self.assertEqual("candidate", self.switches[48]["spatial"]["status"])
        self.assertNotIn("spatial", self.switches[37])
        self.assertIn("public 84", self.switches[15]["physical"]["notes"])
        self.assertIn("public 82", self.switches[16]["physical"]["notes"])

    def test_excerpts_exist_and_hashes_match(self) -> None:
        excerpts = [excerpt for source in self.definition["sources"] for excerpt in source.get("excerpts", [])]
        self.assertEqual(5, len(excerpts))
        for excerpt in excerpts:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
            self.assertTrue(excerpt["reviewed"])
        self.assertIn("| WHT-BRN | 1 Plumb Tilt |", (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8"))
        self.assertIn("Backbox Flash lamps", (EXCERPT_ROOT / "coil-and-flipper.md").read_text(encoding="utf-8"))
        parts = (EXCERPT_ROOT / "mechanism-construction.md").read_text(encoding="utf-8")
        self.assertEqual([str(item) for item in range(1, 76)], re.findall(r"^\| (\d+) \|", parts, flags=re.M))
        self.assertIn("| 44 | Spin. Sw. Actuator Wire | 535-5319-00 |", parts)
        self.assertEqual(sha256(RUNTIME_PATH), self.sources["runtime.robocop.service-walk"]["sha256"])

    def test_manifest_canonical_digest(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual((2064, 94583062), (manifest["file_count"], manifest["total_bytes"]))
        body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual(manifest["manifest_sha256"], hashlib.sha256(canonical).hexdigest())
        self.assertEqual(sha256(MANIFEST_PATH), self.sources["vpx-extraction.robocop-drakkon-mod-1.2"]["sha256"])

    def test_no_other_machine_identity_leaks(self) -> None:
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        text = "\n".join(path.read_text(encoding="utf-8") for path in (DEFINITION_PATH, REPORT_PATH, KNOWLEDGE_PATH)).casefold()
        tokens = set(re.findall(r"[a-z0-9_]+", text))
        self.assertEqual(set(), tokens & {item["id"].casefold() for item in catalog["drivers"] if item["id"] not in OWN_DRIVERS and re.search(r"[0-9_]", item["id"])})
        machines = set(re.findall(r"[a-z0-9]+(?:[.-][a-z0-9]+)+", text))
        self.assertEqual(set(), machines & {item["id"].casefold() for item in catalog["machines"] if item["id"] != MACHINE_ID})

    def test_seed_is_byte_identical_and_curator_check_is_clean(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
        env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(ROOT / "src"), str(ROOT / "tools")]), "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "curate_robocop.py"), "--check"], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


class RoboCopExternalEvidenceTests(unittest.TestCase):
    def test_retained_table_script_and_extraction(self) -> None:
        root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
        if not root:
            self.skipTest("retained VPX sources are not available")
        base = Path(root) / "data-east" / "robocop-1989"
        self.assertEqual("e6f5545be1155856bd684f13e3910c378f7d6f3689425e3696b7329eb65e8ab8", sha256(base / "Robocop (Data East 1989)_drakkon(mod_1.2).vpx"))
        extraction = base / "vpxtool-extract"
        self.assertEqual("00abf00a3f2e9cc3977e1053765902071a7caf381407b58ad09c4bef8abe3dd8", sha256(extraction / "script.vbs"))
        manifest = load_json(MANIFEST_PATH)
        actual = sorted(path.relative_to(extraction).as_posix() for path in extraction.rglob("*") if path.is_file())
        self.assertEqual(actual, [entry["path"] for entry in manifest["files"]])
        for entry in manifest["files"]:
            self.assertEqual(entry["sha256"], sha256(extraction / entry["path"]), entry["path"])

    def test_retained_manual(self) -> None:
        root = os.environ.get("PINMAME_MANUALS_ROOT")
        if not root:
            self.skipTest("retained manuals are not available")
        manual = Path(root) / "by-machine" / MACHINE_ID / "ipdb" / "Data_East_1989_Robocop_English_Manual.pdf"
        self.assertEqual(64_987_666, manual.stat().st_size)
        self.assertEqual("951b39a17f851a2f2e38d79dfc09e5f9b435d03fdbe16d4d45a3e314a7b69af8", sha256(manual))

    def test_builder_rejects_a_reading_shifted_onto_its_neighbour(self) -> None:
        root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not root:
            self.skipTest("retained review artifacts are not available")
        sys.path.insert(0, str(ROOT / "tools"))
        import build_robocop_runtime_evidence as builder
        readings = load_json(READINGS_PATH)
        run, _digest = builder.load_run(Path(root), "robo_a34")
        builder.walk(run, readings)
        shifted = 0
        for section in ("switch_test", "lamp_test", "coil_test"):
            name = (lambda value: value["name"]) if section == "coil_test" else (lambda value: value)
            keys = list(readings[section])
            for previous, current in zip(keys, keys[1:]):
                if name(readings[section][previous]) == name(readings[section][current]):
                    continue
                mutated = json.loads(json.dumps(readings))
                if section == "coil_test":
                    mutated[section][current]["name"] = readings[section][previous]["name"]
                else:
                    mutated[section][current] = readings[section][previous]
                with self.assertRaises(ValueError, msg=(section, current)):
                    builder.walk(run, mutated)
                shifted += 1
        self.assertGreater(shifted, 100)

    def test_runtime_evidence_rebuilds_from_the_retained_runs(self) -> None:
        root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not root:
            self.skipTest("retained review artifacts are not available")
        env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(ROOT / "src"), str(ROOT / "tools")]), "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "build_robocop_runtime_evidence.py"), root, "--check"], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
