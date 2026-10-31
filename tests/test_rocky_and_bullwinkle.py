"""Gates for the Data East The Adventures of Rocky and Bullwinkle and Friends (1993) definition.

These lock down the facts that were expensive to establish and cheap to lose: the column-major address
arithmetic, the cabinet flipper addresses PinMAME mirrors, the Left/Right relay pairing, what the ROM's own
service tests said about every public address, the hat-target disagreement, and the boundary between what the
retained recreation measured and what it did not (a lamp or flash lamp is placed only on a bulb). The fixtures
below are typed from the printed charts and the read DMD frames and kept apart from the curator on purpose: a
test that checks the generator against its own output only proves the generator is self-consistent.

Tests that need retained evidence run only when its root is set and skip cleanly otherwise:
PINMAME_VPX_SOURCES_ROOT (the table extraction), PINMAME_REVIEW_ARTIFACTS_ROOT (the harness runs and the
world-space export), PINMAME_MANUALS_ROOT (the manual scan) and PINMAME_ROM_LIBRARY_ROOT (the ROM archive).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import load_json  # noqa: E402

KEY = "data-east.adventures-of-rocky-and-bullwinkle-and-friends.1993"
SLUG = "adventures-of-rocky-and-bullwinkle-and-friends-1993"
DEFINITION_PATH = ROOT / f"machines/partial/data-east/{SLUG}.json"
AUTHOR_READY_PATH = ROOT / f"machines/author-ready/data-east/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/data-east/{SLUG}.json"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.json"
SPATIAL_MARKDOWN_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.md"
KNOWLEDGE_PATH = ROOT / f"knowledge/data-east/{SLUG}.md"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/adventures-of-rocky-and-bullwinkle-and-friends-rab_320-service-tests.json"
PLACES_PATH = ROOT / "tools/rab_places.json"
EXCERPTS = ROOT / "evidence/excerpts" / KEY
VPX_ROOT = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
REVIEW_ROOT = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
MANUALS_ROOT = os.environ.get("PINMAME_MANUALS_ROOT")
ROM_ROOT = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
EXTRACTION_RELATIVE = Path("data-east/adventures-of-rocky-and-bullwinkle-and-friends-1993/extracted-vpxtool")
WORLD_OBJ_RELATIVE = Path(
    "adventures-of-rocky-and-bullwinkle-and-friends-1993/world-obj/The Adventures of Rocky and Bullwinkle and Fiends (Data East 1993) 1.0.obj"
)
MANUAL_RELATIVE = Path(f"by-machine/{KEY}/ipdb-23/Data_East_1993_Adventures_of_Rocky_and_Bullwinkle_and_Friends_Full_Manual.pdf")
MANUAL_SHA256 = "1f50634e743bccf6276e170dcb5da05c92e5c4769a4650147338fab59b36a381"
ROM_SHA256 = "efe4c395840d66c2b51b63f38686429d4889e9915f364f1f8471714800c2d788"
TOOL_PATH = os.pathsep.join([str(ROOT / "src"), str(ROOT / "tools")])

# --- Independent fixtures ----------------------------------------------------------------------------------
# Printed switch chart cells, spread over all eight columns.
MANUAL_SWITCHES = {
    1: "Plumb Tilt", 2: "4th Coin", 3: "Credit Button", 7: "Slam Tilt", 9: "Launch Button", 10: "Outhole", 13: "Trough #3 Right",
    14: "Shooter Lane", 15: "Left EOS", 16: "Right EOS", 22: "Hat Target Bottom", 23: "Hat Target Middle", 24: "Hat Target Top",
    29: "Super VUK", 32: "Left Outlane", 37: "Under Trough", 44: "Left Turbo Bumper", 45: "Center Turbo Bumper", 46: "Right Turbo Bumper",
    52: "VUK",
}
UNUSED_SWITCHES = {8, 51, *range(53, 65)}
# The ROM's Active Switch Test names, read from the retained frames.
ROM_SWITCHES = {
    1: "PLUMB TILT", 2: "4TH COIN", 3: "CREDIT BUTTON", 9: "LAUNCH BUTTON", 14: "SHOOTER LANE", 15: "LEFT FLIPPER", 16: "RIGHT FLIPPER",
    22: "TOP HAT TARGET", 24: "BOTTOM HAT TARGET", 29: "SUPER VUK", 37: "UNDER TROUGH", 44: "LEFT TURBO BUMPER", 45: "CENTER TURBO BUMPER",
    46: "RIGHT TURBO BUMPER", 52: "VUK", 8: "NOT USED", 64: "NOT USED",
}
MANUAL_LAMPS = {
    1: "Top Blue", 14: "Spin & Win", 15: "Credit Button", 16: "Left Ramp Entr.", 33: "WABAC ???", 48: "Launch Button", 53: "Right Ramp Entr.",
    54: "Jackpot", 57: "Top Hat Target", 60: "Hat Trick", 61: "Rhino Bonus", 64: "Shoot Again",
}
ROM_LAMPS = {
    1: "TOP BLUE", 15: "CREDIT BUTTON", 16: "LEFT RAMP ENTRANCE", 33: "???", 48: "LAUNCH BUTTON", 53: "RIGHT RAMP ENTRANCE", 57: "TOP HAT TARGET",
    60: "HAT TRICK", 61: "RHINO BONUS",
}
# Coil Test entries: (printed number, ROM name, public addresses Start fires).
ROM_COIL_TEST = {
    "#1L": ("COIL: OUTHOLE", [1]), "#1R": ("FL: PLFD X3, INSERT X1", [10, 25]), "#3L": ("COIL: LION INSERT", [3]),
    "#5R": ("FL: PLFD X2, RAMP X2", [10, 29]), "#7L": ("COIL: RHINO INSERT", [7]), "#8L": ("COIL: KNOCKER", [8]), "#09": ("RELAY: SAW MOTOR", [9]),
    "#11": ("RELAY: G.I. RELAY", [11]), "#16": ("COIL: BALL LAUNCHER", [16]), "#18": ("COIL: CENTER POP", [18]), "#22": ("COIL: LASER KICK", [22]),
}
DRIVER_ROMS = {
    "rab_320": ("rabcpua.320", "rbdspa.300"), "rab_130": ("rabcpua.130", "rbdspa.130"), "rab_110be": ("Rocky-Bull_1.10_Belgium-C5.bin", "rbdspa.130"),
    "rab_103it": ("rabcpu.103", "Rocky-Bull_1.03_Italian_Disp-rom0.bin"), "rab_103": ("rabcpu.103", "rabdspsp.103"),
}
# Every output the record leaves without a coordinate, and why it has no not_applicable record instead.
UNPLACED_SOLENOIDS = {8, 11, 25, 26, 28, 30, 31, 32}
PLACED_FLASH_LAMPS = {27: 1, 29: 2}
CABINET_OR_BACKBOX_SOLENOIDS = {3, 6, 7, 10}
UNPLACED_KEYS = {
    "solenoid.8", "solenoid.11", "solenoid.25", "solenoid.26", "solenoid.28", "solenoid.30", "solenoid.31", "solenoid.32",
    *(f"lamp.{n}" for n in range(1, 65)),
}
# Keys whose placements must be bulbs (docs/SPATIAL.md, picking the bulb).
BULB_KEYS = {"solenoid.11", *(f"solenoid.{n}" for n in range(25, 33)), *(f"lamp.{n}" for n in range(1, 65))}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def gameitems(extraction: Path) -> dict[str, tuple[str, dict]]:
    items = {}
    for path in (extraction / "gameitems").glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        kind = next(iter(data))
        items[data[kind]["name"].lower()] = (kind, data[kind])
    return items


class DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.inputs = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
        cls.solenoids = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}

    def test_identity_and_variants(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual((KEY, "Data East", 1993, 23, "G5vnL-MJP3y", "500-5522-01"),
                         (machine["id"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["opdb_id"], machine["model_number"]))
        drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
        self.assertEqual(set(DRIVER_ROMS), set(drivers))
        self.assertNotIn("clone_of", drivers["rab_320"])
        for driver_id, (cpu, display) in DRIVER_ROMS.items():
            driver = drivers[driver_id]
            self.assertEqual("identical", driver["physical_compatibility"], driver_id)
            if driver_id != "rab_320":
                self.assertEqual("rab_320", driver["clone_of"], driver_id)
                if cpu != "rabcpua.320":
                    self.assertIn(cpu, driver["variant_notes"], driver_id)
                if display != "rbdspa.300":
                    self.assertIn(display, driver["variant_notes"], driver_id)
        self.assertIn("BULLWINKLE A3.00", drivers["rab_320"]["variant_notes"])

    def test_controller_platform(self) -> None:
        self.assertEqual({"platform": "pinmame.dataeast", "hardware_generation": "0x4000", "inversion_applied_by_emulator": True}, self.definition["controller"])

    def test_every_address_is_enumerated_once(self) -> None:
        self.assertEqual({*range(1, 65), -7, -6, *range(81, 89)}, set(self.inputs))
        self.assertEqual(set(range(1, 51)), set(self.solenoids))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(["display.dmd"], [display["id"] for display in self.definition["displays"]])
        self.assertEqual((128, 32), (self.definition["displays"][0]["width"], self.definition["displays"][0]["height"]))

    def test_the_matrix_is_column_major(self) -> None:
        for address in range(1, 65):
            column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
            self.assertTrue(self.inputs[address]["physical"]["notes"].startswith(f"Printed switch-matrix column {column}, row {row};"), address)
            self.assertTrue(self.lamps[address]["physical"]["notes"].startswith(f"Printed lamp-matrix column {column}, row {row};"), address)
        self.assertEqual(("Q53", "CN8-3", "WHT-BLU", "CN10-3"), tuple(self.inputs[22]["wiring"][key] for key in ("driver_transistor", "drive_connection", "return_wire", "return_connection")))

    def test_rom_names_and_unused_switches(self) -> None:
        for address, name in ROM_SWITCHES.items():
            self.assertIn(f"'{name}'", self.inputs[address]["physical"]["notes"], address)
        for address in UNUSED_SWITCHES:
            self.assertEqual("unused", self.inputs[address]["availability"], address)
            self.assertEqual("unused", self.inputs[address]["spatial"]["reason"], address)
        for address, name in ROM_LAMPS.items():
            self.assertIn(f"under '{name}'", self.lamps[address]["physical"]["notes"], address)

    def test_polarity_follows_construction(self) -> None:
        for address, item in self.inputs.items():
            if 1 <= address <= 64 and address not in UNUSED_SWITCHES:
                self.assertIs(False, item["normally_closed"], address)
            if address in UNUSED_SWITCHES:
                self.assertNotIn("normally_closed", item, address)
        self.assertIs(False, self.inputs[-7]["normally_closed"])
        self.assertNotIn("normally_closed", self.inputs[-6])
        self.assertIs(False, self.inputs[82]["normally_closed"])
        self.assertIs(False, self.inputs[84]["normally_closed"])
        self.assertIn("polarity", self.definition["coverage"]["missing"])

    def test_flipper_column_and_the_matrix_copies(self) -> None:
        self.assertEqual("switch.left-flipper-copy", self.inputs[15]["id"])
        self.assertEqual("switch.right-flipper-copy", self.inputs[16]["id"])
        self.assertEqual(["flipper.lower.left.button"], self.inputs[84]["roles"])
        self.assertEqual(["flipper.lower.right.button"], self.inputs[82]["roles"])
        for address in (81, 83, 85, 86, 87, 88):
            self.assertEqual("unused", self.inputs[address]["availability"], address)
        self.assertIn("A consumer drives 84, not 15", self.inputs[15]["physical"]["notes"])
        self.assertIn("A consumer drives 82, not 16", self.inputs[16]["physical"]["notes"])
        for address in range(45, 49):
            self.assertEqual("virtual", self.solenoids[address]["kind"], address)
            self.assertEqual("used", self.solenoids[address]["availability"], address)

    def test_lamps_cover_the_whole_matrix(self) -> None:
        self.assertEqual(["cabinet.start-button-lamp"], self.lamps[15]["roles"])
        self.assertEqual(["cabinet.launch-button-lamp"], self.lamps[48]["roles"])
        for address, item in self.lamps.items():
            self.assertEqual("lamp", item["kind"], address)
            self.assertIn("and no other lamp", item["physical"]["notes"], address)
        for address in (16, 53):
            self.assertIn("crossed against the chart", self.lamps[address]["physical"]["notes"], address)

    def test_solenoid_address_model(self) -> None:
        kinds = {address: item["kind"] for address, item in self.solenoids.items()}
        self.assertEqual("motor", kinds[9])
        self.assertEqual("relay", kinds[10])
        self.assertEqual("gi", kinds[11])
        self.assertEqual(["playfield.general-illumination"], self.solenoids[11]["roles"])
        self.assertEqual("control_signal", kinds[23])
        self.assertEqual({"flasher"}, {kinds[address] for address in range(25, 33)})
        self.assertEqual({"coil"}, {kinds[address] for address in (*range(1, 9), *range(12, 23))})
        for address in (24, 33, 34, 35, 36, 49, 50):
            self.assertEqual("unused", self.solenoids[address]["availability"], address)
        for address in range(37, 45):
            self.assertEqual(("unknown", "candidate"), (self.solenoids[address]["availability"], self.solenoids[address]["provenance"]["status"]), address)

    def test_rom_coil_test_names_and_responses(self) -> None:
        facts = load_json(ROOT / "tools/rab_runtime.json")
        entries = {entry["number"]: entry for entry in facts["coil_test"]}
        self.assertNotIn("#10", entries)
        for number, (name, fired) in ROM_COIL_TEST.items():
            self.assertEqual((name, fired), (entries[number]["name"], entries[number]["fired"]), number)
            public = fired[-1]
            self.assertIn(f"entry {number} is named '{name}'", self.solenoids[public]["physical"]["notes"], number)

    def test_right_hand_flash_lamps_pair_with_the_relay(self) -> None:
        gated = sorted(item["destination"] for item in self.definition["relationships"] if item["kind"] == "relay_gated" and item["source"] == "relay.left-right-relay")
        self.assertEqual([f"flasher.{n}r" for n in range(1, 9)], gated)

    def test_the_hat_target_conflict_is_actionable(self) -> None:
        (conflict,) = self.definition["conflicts"]
        self.assertEqual("hat-target-switch-order", conflict["id"])
        self.assertEqual("unresolved", conflict["status"])
        self.assertEqual("inputs[id=switch.hat-target-22]; inputs[id=switch.hat-target-24]", conflict["path"])
        self.assertGreaterEqual(len(conflict["source_refs"]), 2)
        self.assertRegex(conflict["description"], r"Resolution path: [^.]+\.[^.]*$")
        for address in (22, 24):
            self.assertEqual("conflicted", self.inputs[address]["provenance"]["status"], address)
            self.assertEqual("conflicted", self.inputs[address]["spatial"]["status"], address)
        self.assertEqual("conflicted", {m["id"]: m for m in self.definition["mechanisms"]}["mechanism.hat-targets"]["provenance"]["status"])

    def test_wiring_disagreements_are_notes_not_conflicts(self) -> None:
        self.assertNotIn("part_number", self.solenoids[8]["physical"])
        self.assertNotIn("part_number", self.solenoids[16]["physical"])
        self.assertIn("WHT-BRN", self.solenoids[22]["physical"]["notes"])
        self.assertIn("BLK-BRN", self.solenoids[25]["physical"]["notes"])
        self.assertIn("swapped against the drawing", self.inputs[45]["physical"]["notes"])
        self.assertEqual(1, len(self.definition["conflicts"]))

    def test_coverage_gate(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(
            ["input_semantics", "output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"], coverage["missing"]
        )
        self.assertEqual("complete", self.definition["knowledge"]["status"])
        self.assertFalse(AUTHOR_READY_PATH.exists())
        entry = next(machine for machine in load_json(ROOT / "catalog/pinmame.json")["machines"] if machine["id"] == KEY)
        self.assertEqual(63, entry["completion_score"])

    def test_the_curator_check_passes_and_refuses_drift(self) -> None:
        import curate_rocky_and_bullwinkle as curator

        curator.check(ROOT)
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_MARKDOWN_PATH, KNOWLEDGE_PATH):
                target = root / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
            curator.check(root)
            knowledge = root / KNOWLEDGE_PATH.relative_to(ROOT)
            knowledge.write_bytes(knowledge.read_bytes().replace(b"column-major", b"row-major", 1))
            with self.assertRaises(RuntimeError):
                curator.check(root)
            shutil.copyfile(KNOWLEDGE_PATH, knowledge)
            stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_bytes(DEFINITION_PATH.read_bytes())
            with self.assertRaises(RuntimeError):
                curator.check(root)
            with self.assertRaises(RuntimeError):
                curator.generate(root)

    def test_seed_is_byte_identical_to_the_definition(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

    def test_other_machines_are_not_named_in_the_artifacts(self) -> None:
        catalog = load_json(ROOT / "catalog/pinmame.json")
        paths = [DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_MARKDOWN_PATH, EVIDENCE_PATH, *sorted(EXCERPTS.iterdir())]
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for machine in catalog["machines"]:
            if machine["id"] != KEY:
                self.assertNotIn(machine["id"], text)
        for forbidden in ("Tommy", "tomy_", "tftc", "Tales from the Crypt", "gnr_", "Guns N", "Star Trek", "Jurassic", "Lethal Weapon", "Simpsons", "Batman", "Hook"):
            self.assertNotIn(forbidden, text, forbidden)

    def test_knowledge_note_states_the_platform_facts(self) -> None:
        text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        for phrase in (
            "rab_320", "no GI channel", "Left/Right relay", "S11_PRINTERLINE", "never 15 or 16", "column-major", "28 VAC", "Resolution path", "Q55",
            "BULLWINKLE A3.00", "What would complete the record", "show_bulb_mesh",
        ):
            self.assertIn(phrase, text, phrase)
        self.assertNotIn("{", re.sub(r"`[^`]*`", "", text))


class ExcerptTests(unittest.TestCase):
    def test_parsed_tables_match_the_independent_fixtures(self) -> None:
        import rab_manual

        switches = rab_manual.switch_data()["chart"]
        for address, printed in MANUAL_SWITCHES.items():
            self.assertEqual(printed, switches[address]["printed"], address)
        for address in UNUSED_SWITCHES:
            self.assertEqual("Not Used", switches[address]["printed"], address)
        lamps = rab_manual.lamp_data()["chart"]
        for address, printed in MANUAL_LAMPS.items():
            self.assertEqual(printed, lamps[address]["printed"], address)
        coils = rab_manual.coil_data()
        self.assertEqual("Q46", coils["drives"][1]["Transistor"])
        self.assertEqual("KNOCKER 23-800", coils["drives"][8]["Coil as drawn"])
        self.assertEqual("Q30", coils["direct"][9]["Transistor"])
        self.assertEqual("Q13", coils["switched"][22]["Drive transistor"])
        self.assertEqual("(2) LEFT RAMP (2) PLFD (4) NO. 89", coils["drives"][5]["Bulb note as drawn"])

    def test_the_parser_rejects_a_ragged_table(self) -> None:
        import rab_manual

        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "bad.md"
            path.write_bytes(b"## Table\n\n| a | b |\n| --- | --- |\n| 1 | 2 | 3 |\n")
            with self.assertRaises(ValueError):
                rab_manual.read_tables(path)

    def test_every_recorded_excerpt_digest_matches_its_file(self) -> None:
        definition = load_json(DEFINITION_PATH)
        recorded = [excerpt for source in definition["sources"] for excerpt in source.get("excerpts", [])]
        self.assertEqual(sorted(path.name for path in EXCERPTS.iterdir()), sorted(Path(item["path"]).name for item in recorded))
        for excerpt in recorded:
            self.assertEqual(sha256_file(ROOT / excerpt["path"]), excerpt["sha256"], excerpt["id"])
            self.assertTrue(excerpt["reviewed"], excerpt["id"])
            self.assertEqual("manual", excerpt["method"], excerpt["id"])
            self.assertTrue(excerpt["transcribed_by"].startswith("curator"), excerpt["id"])

    def test_the_readings_agree_with_the_manual_wires(self) -> None:
        import build_rab_runtime_evidence as builder
        import rab_manual

        readings = load_json(ROOT / "tools/rab_readings.json")
        switches = rab_manual.switch_data()["chart"]
        lamps = rab_manual.lamp_data()["chart"]
        for key, reading in readings["switches"].items():
            chart = switches[int(key)]
            self.assertEqual(f"{chart['drive']['wire']} {chart['return']['wire']}", builder.normalize_wires(reading["wires"]), key)
        for key, reading in readings["lamps"].items():
            chart = lamps[int(key)]
            drive = re.sub(r"-\s+", "-", chart["drive"]["wire"])
            self.assertEqual(f"{drive} {chart['return']['wire']}", builder.normalize_wires(reading["wires"]), key)


class SpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.places = load_json(PLACES_PATH)
        cls.report = load_json(SPATIAL_REPORT_PATH)
        cls.devices = cls.definition["inputs"] + cls.definition["outputs"]

    def test_every_placement_is_in_range_unique_and_observed(self) -> None:
        identifiers = []
        for device in self.devices:
            spatial = device.get("spatial")
            if not spatial or spatial["status"] == "not_applicable":
                continue
            for placement in spatial["placements"]:
                identifiers.append(placement["id"])
                self.assertTrue(0.0 <= placement["x"] <= 1.0 and 0.0 <= placement["y"] <= 1.0, placement["id"])
                self.assertEqual(spatial["status"], placement["provenance"]["status"], placement["id"])
            expected = "conflicted" if device["id"] in ("switch.hat-target-22", "switch.hat-target-24") else "observed"
            self.assertEqual(expected, spatial["status"], device["id"])
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(len(identifiers), self.report["placement_count"])

    def test_normalization_matches_the_raw_coordinates(self) -> None:
        self.assertEqual({"width": 952.0, "height": 2162.0}, self.places["table_bounds"])
        for key, hits in self.places["placements"].items():
            for hit in hits:
                self.assertEqual(round(hit["raw"]["x"] / 952.0, 6), hit["x"], key)
                self.assertEqual(round(hit["raw"]["y"] / 2162.0, 6), hit["y"], key)

    def test_the_definition_carries_exactly_the_resolved_placements(self) -> None:
        resolved = {
            key: sorted((hit["x"], hit["y"]) for hit in hits) for key, hits in self.places["placements"].items()
        }
        placed = {}
        for device in self.devices:
            spatial = device.get("spatial")
            if not spatial or spatial["status"] == "not_applicable":
                continue
            prefix = "switch" if device["binding"]["group"] == "pinmame.input.switch" else "solenoid"
            placed[f"{prefix}.{device['binding']['device']}"] = sorted((p["x"], p["y"]) for p in spatial["placements"])
        self.assertEqual(resolved, placed)

    def test_the_unplaced_set_is_exact(self) -> None:
        self.assertEqual(UNPLACED_KEYS, {entry["key"] for entry in self.places["unplaced"]})
        self.assertEqual(UNPLACED_KEYS, {entry["key"] for entry in self.report["unresolved"]})
        without = {
            ("solenoid" if device["binding"]["group"] == "pinmame.output.solenoid" else "lamp", device["binding"]["device"])
            for device in self.definition["outputs"] if "spatial" not in device
        }
        expected = {("solenoid", n) for n in UNPLACED_SOLENOIDS} | {("lamp", n) for n in range(1, 65) if n not in (15, 48)}
        self.assertEqual(expected, without)
        reported = {(b["group"], b["address"]) for b in self.report["unplaced_output_bindings"]}
        self.assertEqual({("pinmame.output.solenoid" if g == "solenoid" else "pinmame.output.lamp", n) for g, n in expected}, reported)
        for device in self.definition["inputs"]:
            self.assertIn("spatial", device, device["id"])

    def test_flash_lamps_and_lamps_are_placed_only_on_bulbs(self) -> None:
        placed = {key: hits for key, hits in self.places["placements"].items() if key in BULB_KEYS}
        self.assertEqual({f"solenoid.{n}" for n in PLACED_FLASH_LAMPS}, set(placed))
        for key, hits in placed.items():
            self.assertEqual(PLACED_FLASH_LAMPS[int(key.split(".")[1])], len(hits), key)
            for hit in hits:
                self.assertEqual(("Primitive", "mesh-bounds-center"), (hit["object_type"], hit["coordinate_origin"]), key)
                self.assertTrue(hit["object"].startswith("pBulbBase"), key)
                self.assertEqual(3, len(hit["bulb_parts"]), key)
        for key, hits in self.places["placements"].items():
            for hit in hits:
                if hit["object_type"] == "Primitive":
                    self.assertEqual("mesh-bounds-center", hit["coordinate_origin"], key)
        for entry in self.places["unplaced"]:
            for name in re.findall(r"\b(f\d[a-z]\d?)\b", entry["reason"]):
                self.assertIn(
                    {"key": entry["key"], "object": name},
                    [{"key": r["key"], "object": r["object"]} for r in self.places["rejected"]],
                    f"{entry['key']} names {name} but the builder did not verify it",
                )

    def test_the_builder_refuses_a_light_that_draws_no_bulb(self) -> None:
        import build_rab_places as builder

        class FakeTable:
            def __init__(self, value: dict) -> None:
                self.value = value

            def get(self, name: str, typ: str) -> dict:
                return self.value

            def find_lines(self, pattern: str) -> list[int]:
                return [1]

        light = {"name": "l57", "center": {"x": 166.0, "y": 1000.0}}
        choice = builder.Choice("l57", "Light", "fixture", [r"NFadeL 57, l57"])
        for flags in ({"is_bulb_light": True, "show_bulb_mesh": False}, {"is_bulb_light": False, "show_bulb_mesh": True}, {}):
            with self.assertRaises(builder.BuildError, msg=flags):
                builder.resolve(FakeTable({**light, **flags}), "lamp.57", choice)
        placed = builder.resolve(FakeTable({**light, "is_bulb_light": True, "show_bulb_mesh": True}), "lamp.57", choice)
        self.assertEqual((0.17437, 0.462535), (placed["x"], placed["y"]))
        overlay = builder.Choice("pSawBlade", "Primitive", "fixture", [r"x"], mode="mesh")
        with self.assertRaises(builder.BuildError):
            builder.resolve(FakeTable({"name": "pSawBlade", "is_visible": True}), "solenoid.25", overlay)

    def test_cabinet_and_backbox_devices_are_not_placed(self) -> None:
        solenoids = {d["binding"]["device"]: d for d in self.definition["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}
        for address in CABINET_OR_BACKBOX_SOLENOIDS:
            self.assertEqual("cabinet_or_service", solenoids[address]["spatial"]["reason"], address)
        self.assertNotIn("spatial", solenoids[8])
        self.assertNotIn("spatial", solenoids[11])

    def test_the_reset_coil_is_a_declared_projection(self) -> None:
        self.assertEqual([{"group": "pinmame.output.solenoid", "address": 15}], [{k: p[k] for k in ("group", "address")} for p in self.report["projections"]])
        self.assertEqual("t19", self.places["placements"]["solenoid.15"][0]["object"])

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_the_placements_equal_the_extraction(self) -> None:
        extraction = Path(VPX_ROOT) / EXTRACTION_RELATIVE
        command = [sys.executable, "-B", str(ROOT / "tools/build_rab_places.py"), "--extracted", str(extraction), "--output", str(PLACES_PATH), "--check"]
        if REVIEW_ROOT:
            command += ["--world-obj", str(Path(REVIEW_ROOT) / WORLD_OBJ_RELATIVE)]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": TOOL_PATH})
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_every_placed_light_draws_its_bulb(self) -> None:
        items = gameitems(Path(VPX_ROOT) / EXTRACTION_RELATIVE)
        script = (Path(VPX_ROOT) / EXTRACTION_RELATIVE / "script.vbs").read_bytes().decode("latin-1")
        for key, hits in self.places["placements"].items():
            for hit in hits:
                kind, value = items[hit["object"].lower()]
                self.assertEqual(hit["object_type"], kind, hit["object"])
                if kind == "Light":
                    self.assertTrue(value["is_bulb_light"] and value["show_bulb_mesh"], f"{key}: {hit['object']} draws no bulb")
                if key in BULB_KEYS:
                    lamp = 100 + int(key.split(".")[1]) - 24
                    filament = hit["bulb_parts"][1]
                    self.assertRegex(script, rf"FadePri4m {lamp}, {filament}\b", key)
                    self.assertTrue(items[hit["bound_light"].lower()][1]["is_bulb_light"], key)
        for entry in self.places["rejected"]:
            if "draws no bulb" in entry["reason"]:
                kind, value = items[entry["object"].lower()]
                self.assertEqual("Light", kind, entry["object"])
                self.assertTrue(value["is_bulb_light"] and not value["show_bulb_mesh"], entry["object"])
        drawn = sorted(name for name, (kind, value) in items.items() if kind == "Light" and value.get("is_bulb_light") and value.get("show_bulb_mesh"))
        self.assertEqual(["gi5a", "gi6a"], drawn)

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_extraction_manifest_is_recomputable(self) -> None:
        import curate_rocky_and_bullwinkle as curator

        curator.verify_extraction_manifest(Path(VPX_ROOT))

    @unittest.skipUnless(REVIEW_ROOT, "PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
    def test_the_mesh_bounds_rederive_from_the_world_export(self) -> None:
        import build_rab_places as builder

        builder.check_mesh_bounds(Path(REVIEW_ROOT) / WORLD_OBJ_RELATIVE)
        with tempfile.TemporaryDirectory() as scratch:
            other = Path(scratch) / "other.obj"
            other.write_bytes(b"o pSawBlade\nv 0 0 0\n")
            with self.assertRaises(builder.BuildError):
                builder.check_mesh_bounds(other)


class RuntimeEvidenceTests(unittest.TestCase):
    def test_the_definition_records_the_evidence_digest(self) -> None:
        definition = load_json(DEFINITION_PATH)
        (source,) = [s for s in definition["sources"] if s["id"] == "runtime.adventures-of-rocky-and-bullwinkle-and-friends.rab-320-service-tests"]
        self.assertEqual(sha256_file(EVIDENCE_PATH), source["sha256"])

    def test_cycling_coils_order_is_the_public_address_order(self) -> None:
        facts = load_json(ROOT / "tools/rab_runtime.json")
        expected = [address for drive in range(1, 9) for address in (drive, drive + 24)] + [9, *range(11, 23)]
        self.assertEqual(expected, facts["cycling_coils_order"])

    def test_every_scenario_is_committed_and_valid(self) -> None:
        import rab_harness

        evidence = load_json(EVIDENCE_PATH)
        runs = evidence["runtime"]["raw_runs"]
        self.assertEqual(13, len(runs))
        for run in runs:
            path = ROOT / run["scenario_path"]
            self.assertNotIn(b"\r\n", path.read_bytes(), run["name"])
            self.assertEqual(run["scenario_sha256"], sha256_file(path), run["name"])
            scenario = load_json(path)
            self.assertEqual("rab_320", scenario["game"])
            self.assertEqual(run["action_count"], len(scenario["actions"]))
            self.assertFalse([a for a in scenario["actions"] if a["type"] in ("pulse_key", "set_key")], "named keys would enable keyboard handling")
            rab_harness.check_targets(scenario)

    def test_the_harness_refuses_ambiguous_title_targets(self) -> None:
        import rab_harness

        rab_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["ACTIVE SWITCH TEST"]}]})
        with self.assertRaises(ValueError):
            rab_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["SWITCH TEST"]}]})
        with self.assertRaises(ValueError):
            rab_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["NOT A TITLE"]}]})

    def test_a_substituted_frame_is_refused(self) -> None:
        import build_rab_runtime_evidence as builder

        read = bytes([0, 3] * (128 * 16))
        substitute = bytes([3, 0] * (128 * 16))
        item = {"displays": [{
            "artifact": "dmd\\frame.pgm", "pixel_sha256": hashlib.sha256(read).hexdigest(), "layout": {"width": 128, "height": 32, "depth": 2},
        }]}
        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "run" / "dmd" / "frame.pgm"
            path.parent.mkdir(parents=True)
            path.write_bytes(b"P5\n128 32\n3\n" + read)
            self.assertIs(item["displays"][0], builder.frame(Path(scratch), "run", item))
            path.write_bytes(b"P5\n128 32\n3\n" + substitute)
            with self.assertRaises(SystemExit):
                builder.frame(Path(scratch), "run", item)

    def test_every_cited_frame_is_pinned_by_its_reading(self) -> None:
        readings = load_json(ROOT / "tools/rab_readings.json")
        pinned = [reading for group in ("switches", "lamps") for reading in readings[group].values()]
        self.assertTrue(pinned)
        for reading in pinned:
            self.assertRegex(reading["pixel_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(reading["name"])

    @unittest.skipUnless(REVIEW_ROOT, "PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
    def test_the_evidence_rebuilds_from_the_retained_runs(self) -> None:
        session = Path(REVIEW_ROOT) / "adventures-of-rocky-and-bullwinkle-and-friends-1993/final/rab_320"
        manifest_files = [session / "manifest.json", session / "manifest.sha256"]
        before = [(path.stat().st_mtime_ns, path.read_bytes()) for path in manifest_files]
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/build_rab_runtime_evidence.py"), "--check"],
            capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": TOOL_PATH},
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        # --check verifies the pinned external manifest and must never rewrite it.
        self.assertEqual(before, [(path.stat().st_mtime_ns, path.read_bytes()) for path in manifest_files])


class RetainedSourceTests(unittest.TestCase):
    @unittest.skipUnless(MANUALS_ROOT, "PINMAME_MANUALS_ROOT is not set")
    def test_the_retained_manual_is_the_cited_scan(self) -> None:
        self.assertEqual(MANUAL_SHA256, sha256_file(Path(MANUALS_ROOT) / MANUAL_RELATIVE))
        manual = next(s for s in load_json(DEFINITION_PATH)["sources"] if s["kind"] == "manual")
        self.assertEqual(MANUAL_SHA256, manual["sha256"])

    @unittest.skipUnless(ROM_ROOT, "PINMAME_ROM_LIBRARY_ROOT is not set")
    def test_the_rom_archive_is_the_one_the_runs_used(self) -> None:
        self.assertEqual(ROM_SHA256, sha256_file(Path(ROM_ROOT) / "rab_320.zip"))
        self.assertEqual(ROM_SHA256, load_json(EVIDENCE_PATH)["runtime"]["rom_archive_sha256"])


if __name__ == "__main__":
    unittest.main()
