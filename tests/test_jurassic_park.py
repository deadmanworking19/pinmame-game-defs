"""Game-specific regression and retained-evidence gates for Data East Jurassic Park (1993)."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_jurassic_park as curator
import jurassic_park_data as data
import jurassic_park_harness as harness
import jurassic_park_runtime as runtime

KEY = "data-east.jurassic-park.1993"
SCENARIOS = ["active-switch-test", "lamp-test", "coil-cycle", "coil-cycle-trex-homed", "laser-kick-test", "trex-test"]
# Printed names the ROM spells differently; every other label equals its ROM name once case and punctuation are ignored.
SWITCH_ROM_SPELLINGS = {13, 41, 42, 48, 49, 50, 52, 55, 56, 57, 58, 37, 60, 38, 39, 40, 53, 31, 32, 36, 63, 64}
LAMP_ROM_SPELLINGS = set(range(1, 65))


def squash(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch.isalnum())


class JurassicParkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine = load_json(ROOT / "machines/partial/data-east/jurassic-park-1993.json")
        cls.switches = {d["binding"]["device"]: d for d in cls.machine["inputs"]
                        if d["binding"]["group"] == "pinmame.input.switch"}
        cls.solenoids = {d["binding"]["device"]: d for d in cls.machine["outputs"]
                         if d["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {d["binding"]["device"]: d for d in cls.machine["outputs"]
                     if d["binding"]["group"] == "pinmame.output.lamp"}
        cls.runtime = load_json(ROOT / "tools/jurassic_park_runtime.json")

    def test_identity_variants_display_and_partial_gate(self):
        self.assertEqual(KEY, self.machine["machine"]["id"])
        self.assertEqual((1343, "500-5520-01", 1993), tuple(self.machine["machine"][k] for k in ("ipdb_id", "model_number", "year")))
        self.assertEqual({"jupk_513", "jupk_501", "jupk_g51", "jupk_305", "jupk_307", "jupk_600"},
                         {d["id"] for d in self.machine["drivers"]})
        self.assertEqual({"jupk_513"}, {d["id"] for d in self.machine["drivers"] if "clone_of" not in d})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in self.machine["drivers"]))
        self.assertEqual((128, 32, 0), tuple(self.machine["displays"][0][k] for k in ["width", "height", "controller_index"]))
        self.assertEqual("0x4000", self.machine["controller"]["hardware_generation"])
        self.assertEqual("partial", self.machine["coverage"]["status"])
        self.assertEqual({"output_semantics", "spatial_placement", "unresolved_conflicts"}, set(self.machine["coverage"]["missing"]))
        self.assertEqual(["conflict.flash-bank-1r-bulb-count"], [c["id"] for c in self.machine["conflicts"]])
        self.assertIn("Resolution path:", self.machine["conflicts"][0]["description"])
        self.assertEqual("unresolved", self.machine["conflicts"][0]["status"])
        self.assertFalse((ROOT / "machines/author-ready/data-east/jurassic-park-1993.json").exists())
        self.assertEqual([], validate_machine(self.machine, ROOT))
        catalog = {m["id"]: m for m in load_json(ROOT / "catalog/pinmame.json")["machines"]}
        self.assertEqual(81, catalog[KEY]["completion_score"])

    def test_complete_outer_namespaces_and_precise_dispositions(self):
        self.assertEqual(set(range(1, 65)) | {-7, -6} | set(range(81, 89)), set(self.switches))
        self.assertEqual(set(range(1, 65)), set(self.solenoids))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        self.assertEqual([0], [d["binding"]["device"] for d in self.machine["inputs"]
                               if d["binding"]["group"] == "pinmame.input.dip"])
        self.assertEqual({8, 28, 30, 51, 54, 62}, {n for n in range(1, 65) if self.switches[n]["availability"] == "unused"})
        self.assertEqual({82, 84}, {n for n in range(81, 89) if self.switches[n]["availability"] == "used"})
        self.assertTrue(all(d["availability"] == "used" for d in self.lamps.values()))
        self.assertEqual({24, 33, 34, 35, 36, 49, 50, *range(51, 65)},
                         {n for n, d in self.solenoids.items() if d["availability"] == "unused"})
        self.assertEqual(set(range(37, 45)), {n for n, d in self.solenoids.items() if d["availability"] == "unknown"})
        self.assertEqual({23, 45, 46, 47, 48}, {n for n, d in self.solenoids.items() if d["kind"] == "virtual" and d["availability"] == "used"})

    def test_switch_and_lamp_labels_follow_the_factory_tables_and_the_rom(self):
        for address in range(1, 65):
            self.assertEqual(data.SWITCH_NAMES[address - 1], self.switches[address]["label"])
        self.assertEqual({8, 28, 30, 51, 54, 62}, {n for n, name in enumerate(data.ROM_SWITCH_NAMES, 1) if name == "NOT USED"})
        for address in range(1, 65):
            manual = data.LAMP_LABEL_OVERRIDES.get(address, data.LAMP_NAMES[address - 1])
            self.assertEqual(manual, self.lamps[address]["label"])
        # The ROM and the manual disagree on these lamps' names; each settlement is stated on the device.
        for address, text in {6: "BARYONYX - MAP", 20: "MULTI MOSQUITO MILLIONS", 30: "JACKPOT RAMP",
                              48: "ARCH \"E\"", 50: "GALLIMIMUS"}.items():
            self.assertIn(text, self.lamps[address]["physical"]["notes"])
        self.assertEqual(["Map", "Raptor Multi-Million", "Jackpot Map", "\"C\" Arch", "#2"],
                         [data.LAMP_NAMES[n - 1] for n in (6, 20, 30, 48, 50)])
        self.assertEqual("Credit Button", self.lamps[9]["label"])
        self.assertEqual(data.TWO_BULB_LAMPS | {37}, {n for n, d in self.lamps.items() if d["physical"]["quantity"] == 2})
        self.assertEqual(1, len(self.lamps[37]["spatial"]["placements"]))
        self.assertIn("two separate 37 locations", self.lamps[37]["physical"]["notes"])

    def test_matrix_wiring_is_complete_and_keyed(self):
        for address in range(1, 65):
            col, row = divmod(address - 1, 8)
            wiring = self.switches[address]["wiring"]
            self.assertEqual((data.SWITCH_COLUMNS[col][0], data.SWITCH_ROWS[row][0]), (wiring["drive_wire"], wiring["return_wire"]))
            lamp = self.lamps[address]["wiring"]
            self.assertEqual((data.LAMP_COLUMNS[col][0], data.LAMP_ROWS[row][0]), (lamp["drive_wire"], lamp["return_wire"]))
        self.assertEqual({"CN8-1", "CN8-2", "CN8-3", "CN8-4", "CN8-5", "CN8-7", "CN8-8", "CN8-9"},
                         {c[1] for c in data.SWITCH_COLUMNS})
        self.assertEqual({"CN10-1", "CN10-2", "CN10-3", "CN10-5", "CN10-6", "CN10-7", "CN10-8", "CN10-9"},
                         {r[1] for r in data.SWITCH_ROWS})
        self.assertEqual("CN6-9", self.lamps[64]["wiring"]["return_connection"])
        self.assertEqual("Q55", self.switches[1]["wiring"]["driver_transistor"])
        self.assertEqual("Q71", self.lamps[1]["wiring"]["driver_transistor"])
        # The lamp rows skip CN6-4 and the lamp columns CN7-5 for the CPU board's keyed pins.
        self.assertEqual(["CN6-1", "CN6-2", "CN6-3", "CN6-5", "CN6-6", "CN6-7", "CN6-8", "CN6-9"], [r[1] for r in data.LAMP_ROWS])
        self.assertEqual(["CN7-1", "CN7-2", "CN7-3", "CN7-4", "CN7-6", "CN7-7", "CN7-8", "CN7-9"], [c[1] for c in data.LAMP_COLUMNS])

    def test_polarity_trough_start_state_and_trex_sensors(self):
        used = [n for n in range(1, 65) if self.switches[n]["availability"] == "used"]
        self.assertTrue(all(self.switches[n]["normally_closed"] is False for n in used))
        self.assertEqual({9, 10, 11, 12, 13, 14, 36, 57}, {n for n, d in self.switches.items() if d.get("initial_active")})
        for address, label in data.TREX_TEST_LABELS.items():
            self.assertIn(f"ON beside {label}", self.switches[address]["physical"]["notes"])
            self.assertEqual("microswitch", self.switches[address]["physical"]["switch_type"])
        self.assertEqual("180-5123-00", self.switches[36]["physical"]["part_number"])
        self.assertEqual({31: "T.Rex Right", 32: "T.Rex Left", 36: "T.Rex Center", 57: "T.Rex Top (Up)", 58: "T.Rex Bottom (Down)"},
                         {n: self.switches[n]["label"] for n in data.TREX_TEST_LABELS})
        self.assertEqual("switch", self.switches[15]["kind"])
        self.assertIn("seventh trough contact", self.switches[15]["physical"]["notes"])
        for n in range(63, 65):
            self.assertIn("direct writes", self.switches[n]["physical"]["notes"])

    def test_flipper_aliases_do_not_invent_hardware(self):
        for n in (45, 46, 47, 48):
            self.assertEqual("virtual", self.solenoids[n]["kind"])
            self.assertNotIn("quantity", self.solenoids[n].get("physical", {}))
        self.assertEqual({"device.right-flipper", "device.left-flipper"}, {self.solenoids[46]["id"], self.solenoids[48]["id"]})
        upper = next(m for m in self.machine["mechanisms"] if m["id"] == "mechanism.upper-right-flipper")
        self.assertEqual([], upper["actuators"])
        self.assertIn("same right button", upper["behavior"])
        for n in (81, 83, 85, 86, 87, 88):
            self.assertEqual("unused", self.switches[n]["availability"])
        self.assertEqual({"relationship.flipper-column-82-to-matrix-64", "relationship.flipper-column-84-to-matrix-63"},
                         {r["id"] for r in self.machine["relationships"] if "flipper-column" in r["id"]})

    def test_coil_names_wiring_parts_and_the_left_right_mux(self):
        for coil, name in data.ROM_COIL_NAMES.items():
            self.assertIn(name.split(": ", 1)[1], self.solenoids[coil]["physical"]["notes"].upper() if coil <= 22 else
                          self.solenoids[coil]["physical"]["notes"].upper() + self.solenoids[coil]["label"].upper())
        self.assertEqual({n: "Q%d" % (47 - n) for n in range(1, 9)},
                         {n: self.solenoids[n]["wiring"]["driver_transistor"] for n in range(1, 9)})
        self.assertEqual({9: "Q30", 10: "Q29", 11: "Q28", 12: "Q27", 13: "Q26", 14: "Q25", 15: "Q24", 16: "Q23"},
                         {n: self.solenoids[n]["wiring"]["driver_transistor"] for n in range(9, 17)})
        self.assertEqual({17: "Q11", 18: "Q9", 19: "Q8", 20: "Q10", 21: "Q12", 22: "Q13"},
                         {n: self.solenoids[n]["wiring"]["driver_transistor"] for n in range(17, 23)})
        self.assertEqual({3, 5, 9}, {n for n in range(1, 23) if self.solenoids[n]["wiring"].get("nominal_voltage_v") == 50})
        # The cabinet shaker is a 12VDC motor fed from 9VAC (PDF 55), not a 32V coil.
        self.assertEqual((12, "PS CN1-11 / CN1-10 (9VAC, fused and rectified)"),
                         (self.solenoids[22]["wiring"]["nominal_voltage_v"], self.solenoids[22]["wiring"]["power_connection"]))
        self.assertTrue(all(self.solenoids[n]["wiring"]["nominal_voltage_v"] == 32 for n in (17, 18, 19, 20, 21)))
        self.assertEqual({1: "090-5636-02", 2: "090-5001-00", 3: "090-5001-01", 4: "090-5001-01", 5: "090-5001-01", 6: "090-5004-02", 7: "090-5004-02",
                          8: "090-5001-01", 9: "090-5001-01", 13: "090-5034-00", 16: "090-5034-00", 17: "090-5001-00",
                          18: "090-5001-00", 19: "090-5001-00", 20: "090-5001-02", 21: "090-5001-02"},
                         {n: d["physical"]["part_number"] for n, d in self.solenoids.items() if n <= 22 and "part_number" in d["physical"]})
        self.assertEqual({"relay"}, {self.solenoids[n]["kind"] for n in (10, 11, 12, 14, 15)})
        self.assertEqual("motor", self.solenoids[22]["kind"])
        self.assertEqual({f"relationship.mux-{n}" for n in range(25, 33)}, {r["id"] for r in self.machine["relationships"] if "mux" in r["id"]})
        self.assertTrue(all(r["source"] == self.solenoids[10]["id"] for r in self.machine["relationships"] if "mux" in r["id"]))
        self.assertIn("reversed #44 6.3 VAC", self.solenoids[11]["physical"]["notes"])
        self.assertIn("F1 Playfield, F2 Backbox Door & Speaker Panel, F3 Playfield & Coin Door, F4 Backbox Door", self.solenoids[11]["physical"]["notes"])

    def test_flash_banks_have_four_bulbs_and_only_playfield_bulbs_are_placed(self):
        placed = {n: len(self.solenoids[n].get("spatial", {}).get("placements", [])) for n in range(25, 33)}
        self.assertEqual({25: 1, 26: 1, 27: 4, 28: 3, 29: 3, 30: 1, 31: 4, 32: 1}, placed)
        self.assertTrue(all(self.solenoids[n]["physical"]["quantity"] == 4 for n in range(25, 33)))
        for n in range(25, 33):
            for placement in self.solenoids[n]["spatial"]["placements"]:
                self.assertEqual(("emitter", "observed"), (placement["role"], placement["provenance"]["status"]))

    def test_geometry_is_per_object_not_glow_or_flasher_sprite(self):
        allowed_primitives = {"TrexPlastic", "TrexJaw"}
        for name, obj in curator.GEOMETRY["objects"].items():
            if obj["type"] == "Primitive":
                self.assertIn(name, allowed_primitives)
            self.assertNotEqual("Flasher", obj["type"])
            self.assertEqual([round(obj["raw_xy"][0] / 952, 6), round(obj["raw_xy"][1] / 2162, 6)], obj["xy"], name)
            self.assertTrue(all(0 <= v <= 1 for v in obj["xy"]), name)
        for name, obj in curator.GEOMETRY["objects"].items():
            if obj["type"] == "Light":
                light = obj["light"]
                # A bulb is an insert sprite or a modelled bulb mesh with a small falloff; never a glow or halo light.
                self.assertTrue(light["image"] in {"PlayfieldLights", "JurassicParkRedraw-4", "pf0"} or light["show_bulb_mesh"], name)
                self.assertLessEqual(light["falloff_radius"], 160.0, name)
        self.assertEqual(2, len(self.lamps[55]["spatial"]["placements"]))
        self.assertEqual(2, len(self.lamps[1]["spatial"]["placements"]))
        self.assertEqual({17, 18, 33, 34, 46, 57, 58}, {n for n, d in self.lamps.items() if "spatial" not in d})
        self.assertEqual("cabinet_or_service", self.lamps[9]["spatial"]["reason"])
        self.assertTrue(all("spatial" not in self.switches[n] for n in range(9, 16)))
        for switch, coil in ((43, 20), (44, 21)):
            self.assertEqual([(p["x"], p["y"]) for p in self.solenoids[coil]["spatial"]["placements"]],
                             [(p["x"], p["y"]) for p in self.switches[switch]["spatial"]["placements"]])
        self.assertTrue(all(p["provenance"]["status"] == "observed" for d in self.machine["inputs"] + self.machine["outputs"]
                            for p in (d.get("spatial") or {}).get("placements", [])))
        report = load_json(ROOT / "reports/spatial/data-east/jurassic-park-1993.json")
        self.assertEqual("pinmame-spatial-blockers", report["format"])
        self.assertEqual(curator.report(self.machine), report)

    def test_trex_sensors_and_controls_project_onto_the_toy_pivot(self):
        pivot = curator.OBJECTS["TrexPlastic"]["xy"]
        for n in data.TREX_TEST_LABELS:
            self.assertEqual([pivot], [[p["x"], p["y"]] for p in self.switches[n]["spatial"]["placements"]])
        for n in (12, 14, 15):
            self.assertEqual([pivot], [[p["x"], p["y"]] for p in self.solenoids[n]["spatial"]["placements"]])
        self.assertEqual(curator.OBJECTS["TrexJaw"]["xy"], [self.solenoids[13]["spatial"]["placements"][0][k] for k in ("x", "y")])

    def test_runtime_summary_agrees_with_the_definition_tables(self):
        summary = self.runtime
        records = summary["active_switch_test"]["records"]
        self.assertEqual(list(range(1, 65)), [r["address"] for r in records])
        for record in records:
            self.assertEqual(data.ROM_SWITCH_NAMES[record["address"] - 1], record["displayed_name"])
            self.assertEqual(f"#{record['address']:02d}", record["displayed_number"])
            column, row = divmod(record["address"] - 1, 8)
            # Independent expectation from the factory matrix, not from the record under test.
            self.assertEqual(f"{data.SWITCH_COLUMNS[column][0]} {data.SWITCH_ROWS[row][0]}", record["displayed_wires"])
        self.assertEqual("GRN-GRY WHT-VIO", records[62]["displayed_wires"])
        self.assertEqual("GRN-GRY WHT-GRY", records[63]["displayed_wires"])
        self.assertEqual({"47": [1, 0], "48": [1, 0]}, {str(k): v for k, v in summary["active_switch_test"]["flipper_buttons"]["Left"].items()})
        self.assertEqual({"45": [1, 0], "46": [1, 0]}, {str(k): v for k, v in summary["active_switch_test"]["flipper_buttons"]["Right"].items()})
        lamps = summary["lamp_test"]["records"]
        self.assertEqual(list(range(1, 65)), [r["address"] for r in lamps])
        for record in lamps:
            self.assertEqual([record["address"]], record["active_lamps"])
            self.assertEqual(data.ROM_LAMP_NAMES[record["address"] - 1], record["displayed_name"])
        self.assertEqual(sorted(data.ROM_COIL_NAMES), sorted(r["address"] for r in summary["coil_cycle"]["records"]))
        for record in summary["coil_cycle"]["records"]:
            self.assertEqual(data.ROM_COIL_NAMES[record["address"]], record["displayed_name"])
            self.assertEqual(record["address"] in (14, 15), record["pulse_time_s"] is None)
            if record["pulse_time_s"] is not None:
                self.assertLessEqual(record["snapshot_time_s"] - record["pulse_time_s"], 1.5)
        order = summary["coil_cycle"]["first_cycle_order"]
        self.assertTrue({1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32} <= set(order))
        self.assertFalse({14, 15} & set(order))
        self.assertEqual({str(a): [str(c)] for a, c in data.LASER_KICK_PAIRS.items()},
                         {str(r["address"]): sorted(r["solenoids"]) for r in summary["laser_kick_test"]["records"] if r["solenoids"]})
        controls = summary["trex_test"]["controls"]
        self.assertEqual({"15"}, set(controls["Left flipper with Top closed"]))
        self.assertEqual({"12", "15"}, set(controls["Right flipper with Top closed"]))
        self.assertEqual([1], controls["Right flipper with Top closed"]["12"])
        self.assertEqual({"14": [1, 0]}, controls["Start with Top closed, Center open"])
        self.assertEqual({"13": [1, 0]}, controls["Launch trigger (41) with the T-Rex homed"])
        self.assertEqual({a: label for a, label in data.TREX_TEST_LABELS.items()},
                         {r["address"]: r["on_label"] for r in summary["trex_test"]["closures"]})
        homed = summary["boot_homing"]["coil-cycle-trex-homed"]
        self.assertEqual([36, 57], [s["switch"] for s in homed["initial_switches"]])
        self.assertEqual([14, 15, 14, 13, 15, 13, 12, 12], [e[1] for e in homed["boot_events"]])
        # Open T-Rex switches: the up/down motor runs about 3.4 s and nothing else starts.
        unhomed = summary["boot_homing"]["coil-cycle"]["boot_events"]
        self.assertEqual([(14, 1), (14, 0)], [(e[1], e[2]) for e in unhomed])
        self.assertTrue(3.2 < unhomed[1][0] - unhomed[0][0] < 3.7)
        for key in ("active_switch_test", "lamp_test", "coil_cycle", "laser_kick_test", "trex_test"):
            self.assertRegex(summary[key]["raw_sha256"], "^[0-9a-f]{64}$")

    def test_runtime_provenance_binds_scenarios_library_rom_and_manifest(self):
        provenance = load_json(ROOT / "tools/jurassic_park_runtime_provenance.json")
        self.assertEqual(runtime.LIBRARY_SHA256, provenance["library_sha256"])
        self.assertEqual(runtime.PINMAME_REVISION, provenance["pinmame_revision"])
        self.assertEqual(SCENARIOS, [Path(r["raw"]).parts[0] for r in provenance["runs"]])
        for run in provenance["runs"]:
            path = ROOT / run["scenario"]
            self.assertEqual(run["scenario_sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), run["scenario"])
            self.assertEqual(run["sha256"], self.runtime[{"active-switch-test": "active_switch_test", "lamp-test": "lamp_test",
                             "coil-cycle": "coil_cycle", "laser-kick-test": "laser_kick_test",
                             "trex-test": "trex_test"}.get(Path(run["raw"]).parts[0], "coil_cycle")]["raw_sha256"]
                             if Path(run["raw"]).parts[0] != "coil-cycle-trex-homed" else
                             self.runtime["boot_homing"]["coil-cycle-trex-homed"]["raw_sha256"])
        self.assertEqual({"jpcpua.513", "jpdspa.510", "jpu17.dat", "jpu21.dat", "jpu7.dat"}, set(provenance["rom"]["members"]))
        self.assertRegex(provenance["manifest"]["sha256"], "^[0-9a-f]{64}$")

    def test_legacy_identifiers_and_aliases_are_preserved(self):
        for key, original in curator.LEGACY["inputs"].items():
            current = self.switches[int(key)]
            self.assertEqual(original["id"], current["id"])
            self.assertEqual(original["aliases"], current["aliases"])
        for key, original in curator.LEGACY["outputs"].items():
            namespace, n = key.rsplit(":", 1)
            devices = self.lamps if namespace == "pinmame.output.lamp" else self.solenoids
            if int(n) not in devices:
                # Legacy lamp numbers 100-128 were the retained script's SetLamp helpers, not controller lamps.
                self.assertEqual("pinmame.output.lamp", namespace)
                self.assertGreater(int(n), 64)
                continue
            self.assertEqual(original["id"], devices[int(n)]["id"])
            self.assertEqual(original["aliases"], devices[int(n)]["aliases"])

    def test_scripted_sources_are_pinned_and_the_embedded_script_is_the_authority(self):
        sources = {s["id"]: s for s in self.machine["sources"]}
        self.assertTrue(sources[curator.SCRIPT]["known_working"])
        self.assertEqual(curator.SCRIPT_SHA, sources[curator.SCRIPT]["sha256"])
        self.assertTrue(sources[curator.TABLE]["uri"].endswith("Jurassic Park (Data East 1993)1.03.vpx"))
        self.assertEqual("0c036bb61b4b4e8c778c37559f6795df8cd1521e", sources[curator.VPW]["revision"])
        for source in sources.values():
            self.assertTrue(all("reviewed" in e and e["transcribed_by"] for e in source.get("excerpts", [])))
        self.assertEqual(KEY, curator.MANUAL_PROVENANCE["machine_id"])
        self.assertEqual(1343, curator.MANUAL_PROVENANCE["ipdb"]["machine_id"])
        self.assertTrue(curator.MANUAL_PROVENANCE["ipdb"]["capture_url"].startswith("https://web.archive.org/web/2025"))

    def test_canonical_seed_curator_and_complete_excerpts(self):
        for path, payload in curator.artifacts().items():
            self.assertEqual(payload, (ROOT / path).read_bytes().replace(b"\r\n", b"\n"), str(path))
        self.assertEqual(canonical_bytes(self.machine), (ROOT / "tools/seeds/data-east/jurassic-park-1993.json").read_bytes())
        for name in ["switch-chart.md", "lamp-chart.md"]:
            text = (ROOT / curator.EXCERPTS / name).read_text(encoding="utf-8")
            self.assertEqual(64, sum(line.startswith("| ") and line[2:].split(" | ")[0].isdigit() for line in text.splitlines()))
        promoted = copy.deepcopy(self.machine)
        promoted["coverage"] = {"status": "author_ready", "missing": [], "dimensions": self.machine["coverage"]["dimensions"]}
        self.assertTrue(validate_machine(promoted, ROOT), "Dishonest promotion must fail")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "machines/author-ready" / f"{curator.STEM}.json"
            target.parent.mkdir(parents=True)
            target.write_text("existing author-ready artifact", encoding="utf-8")
            with patch.object(sys, "argv", ["curate_jurassic_park.py", "--regenerate", "--repository-root", directory]):
                with self.assertRaisesRegex(ValueError, "author-ready"):
                    curator.main()
            self.assertEqual("existing author-ready artifact", target.read_text(encoding="utf-8"))
            self.assertFalse((Path(directory) / "machines/partial").exists())

    def test_no_sibling_machine_names_leak_into_the_artifacts(self):
        catalog = load_json(ROOT / "catalog/pinmame.json")
        forbidden = {driver["id"] for driver in catalog["drivers"] if not driver["id"].startswith("jupk_")}
        text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in (
            "machines/partial/data-east/jurassic-park-1993.json", "knowledge/data-east/jurassic-park-1993.md"))
        # The Lost World Jurassic Park is a different machine; only long unambiguous short names are checked.
        self.assertFalse({name for name in forbidden if len(name) >= 6 and f'"{name}"' in text}, "sibling driver names in artifacts")
        self.assertNotIn("gnr_300", text)
        self.assertNotIn("Guns N", text)
        self.assertNotIn("Lost World", text)

    def test_reusable_scenarios_validate_and_the_title_adapter_fails_closed(self):
        schema = load_json(ROOT / "schemas/harness-scenario.schema.json")
        for name in SCENARIOS:
            scenario = load_json(ROOT / "tools/harness-scenarios/data-east" / f"jupk-513-{name}.json")
            Draft202012Validator(schema).validate(scenario)
            self.assertEqual("jupk_513", scenario["game"])
        # Direct cabinet writes are only valid with keyboard handling off: the active-switch run uses no named keys at all.
        active = load_json(ROOT / "tools/harness-scenarios/data-east/jupk-513-active-switch-test.json")
        self.assertEqual([], [a for a in active["actions"] if "key" in a])
        self.assertEqual(19, len(harness.TEMPLATES))
        self.assertEqual(19, len({digest for _, digest in harness.TEMPLATES.values()}))
        self.assertEqual("", harness.match_title(bytes(4096), 128, 32))
        self.assertEqual("", harness.match_title(bytes(4096), 128, 64))
        # A bitmap fingerprint ignores the row a line is drawn on and fails when one pixel changes.
        frame = bytearray(4096)
        for x in range(20, 60):
            for y in (5, 6, 7):
                frame[y * 128 + x] = 255 if (x + y) % 3 else 0
        shifted = bytearray(4096)
        for y in (5, 6, 7):
            shifted[(y + 9) * 128 + 20:(y + 9) * 128 + 60] = frame[y * 128 + 20:y * 128 + 60]
        self.assertEqual(harness.line_signature(frame), harness.line_signature(shifted))
        altered = bytearray(frame)
        altered[5 * 128 + 21] ^= 255
        self.assertNotEqual(harness.line_signature(frame), harness.line_signature(altered))
        self.assertEqual("", harness.line_signature(bytes(4096)))
        self.assertTrue(all(len(digest) == 64 for _, digest in harness.TEMPLATES.values()))


class JurassicParkExternalTests(unittest.TestCase):
    def setUp(self):
        root = os.environ.get("PINMAME_WORKING_ROOT")
        if not root:
            self.skipTest("PINMAME_WORKING_ROOT not supplied; external verification intentionally skipped")
        self.working = Path(root)

    def test_complete_retained_extraction_manual_and_runtime(self):
        curator.verify_external(self.working)

    def test_templates_match_their_retained_exploratory_frames(self):
        explore = self.working / "review-artifacts" / KEY / "session-20261001" / "explore2" / "dmd"
        templates = load_json(ROOT / "tools/jurassic_park_runtime.json")  # force the summary to be loadable
        self.assertTrue(templates)
        for title, (region, digest) in harness.TEMPLATES.items():
            hits = []
            for path in explore.glob("*-black-*-display-0.pgm"):
                raw = path.read_bytes()
                header, _, rest = raw.split(b"\n", 3)[0], None, raw.split(b"\n", 3)[3]
                frame = list(rest[-4096:])
                if harness.line_signature(frame, region) == digest:
                    hits.append(path.name)
            self.assertTrue(hits, title)

    def test_summary_rejects_a_changed_run_or_scenario(self):
        base = self.working / "review-artifacts" / KEY / "session-20261001" / "runtime"
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "runtime"
            for name in SCENARIOS:
                (copy_root / name).mkdir(parents=True)
                raw = json.loads((base / name / "run.json").read_text(encoding="utf-8"))
                (copy_root / name / "run.json").write_text(json.dumps(raw), encoding="utf-8")
            wrong = json.loads((copy_root / "lamp-test" / "run.json").read_text(encoding="utf-8"))
            wrong["game"] = "jupk_307"
            (copy_root / "lamp-test" / "run.json").write_text(json.dumps(wrong), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "wrong game"):
                runtime.run_meta(copy_root, "lamp-test")
            right = json.loads((base / "lamp-test" / "run.json").read_text(encoding="utf-8"))
            right["scenario"]["sha256"] = "0" * 64
            (copy_root / "lamp-test" / "run.json").write_text(json.dumps(right), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "committed scenario"):
                runtime.run_meta(copy_root, "lamp-test")


if __name__ == "__main__":
    unittest.main()
