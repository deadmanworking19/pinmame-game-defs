from __future__ import annotations

import copy
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_stars as curator
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine
from summarize_stars_runtime import COIL_TEST, build as runtime_build
from drawing_callouts import evaluate, placements_of


class StarsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(ROOT / curator.DEFINITION)
        cls.evidence = load_json(ROOT / curator.EVIDENCE)
        cls.runtime = load_json(ROOT / curator.RUNTIME)

    def group(self, collection, group):
        return {d["binding"]["device"]: d for d in self.definition[collection] if d["binding"]["group"] == group}

    def scratch(self):
        return tempfile.TemporaryDirectory(prefix="pinmame-stars-gate-")

    def test_identity_family_and_exact_display_override(self):
        self.assertEqual("pinmame.stern-mpu100", self.definition["controller"]["platform"])
        self.assertEqual("0x800000", self.definition["controller"]["hardware_generation"])
        self.assertEqual((1978, "103", 2366, "GrXEW-MDEwr"), tuple(self.definition["machine"][k] for k in ("year", "model_number", "ipdb_id", "opdb_id")))
        drivers = {d["id"]: d for d in self.definition["drivers"]}
        self.assertEqual({"stars", "starsfp", "starsb", "starsb7"}, set(drivers))
        self.assertEqual("unknown", drivers["starsb"]["physical_compatibility"])
        self.assertEqual("compatible", drivers["starsb7"]["physical_compatibility"])
        self.assertEqual([1, 9, 17, 25], [d["segment_start"] for d in drivers["starsb7"]["display_overrides"]])
        self.assertEqual([7]*4, [d["width"] for d in drivers["starsb7"]["display_overrides"]])
        self.assertEqual([2, 10, 18, 26, 35, 38], [d["segment_start"] for d in self.definition["displays"]])
        self.assertEqual([6]*4+[2, 2], [d["width"] for d in self.definition["displays"]])
        catalog = load_json(ROOT / "catalog/pinmame.json")
        record = next(m for m in catalog["machines"] if m["id"] == curator.MACHINE_ID)
        self.assertEqual(curator.DEFINITION.as_posix(), record["definition"])
        self.assertEqual(4, record["driver_count"])
        self.assertEqual(set(drivers), {d["id"] for d in catalog["drivers"] if d["machine_id"] == curator.MACHINE_ID})
        self.assertFalse(any(p.name == "stars.json" for p in (ROOT / "machines/stubs").rglob("*.json")))

    def test_complete_address_disposition_and_shared_contacts(self):
        switches = self.group("inputs", "pinmame.input.switch")
        self.assertEqual({-7, -6, -5} | set(range(1, 49)) | set(range(81, 89)), set(switches))
        self.assertEqual(set(curator.SWITCHES) | {-7, -6, 82, 84}, {n for n, d in switches.items() if d["availability"] == "used"})
        self.assertEqual("unused", switches[2]["availability"])
        self.assertEqual("Tilt", switches[7]["label"])
        self.assertEqual("MPU diagnostic S33", switches[-6]["label"])
        self.assertIn({"namespace": "manual.mpu", "value": "S33"}, switches[-6]["aliases"])
        self.assertEqual(1, switches[-6]["physical"]["quantity"])
        self.assertEqual((2, 2, 3, 7), tuple(switches[n]["physical"]["quantity"] for n in (7, 15, 16, 25)))
        self.assertNotIn("spatial", switches[16])
        self.assertTrue(switches[8]["initial_active"])
        self.assertEqual(set(range(1, 33)), set(self.group("inputs", "pinmame.input.dip")))
        eos = self.group("inputs", "physical.input.direct")
        self.assertEqual({1, 2}, set(eos))
        self.assertTrue(all(d["normally_closed"] for d in eos.values()))
        self.assertTrue(all(not switches[n]["normally_closed"] for n in curator.SWITCHES))
        lamps = self.group("outputs", "pinmame.output.lamp")
        self.assertEqual({16*d+s+1 for d in range(4) for s in range(15)}, set(lamps))
        self.assertEqual({9, 18, 23, 34, 37, 39, 40, 41, 50, 53, 55, 56, 57}, {n for n, d in lamps.items() if d["availability"] == "unknown"})
        self.assertFalse(any(d["availability"] == "unused" for d in lamps.values()))
        self.assertEqual("Tilt", lamps[61]["label"])

    def test_factory_decoder_and_coil_numbers_are_not_public_ordinals(self):
        lamps = load_json(ROOT / curator.LAMPS)
        self.assertEqual({f"Q{i}" for i in range(1, 61)}, {r["scr"] for r in lamps})
        self.assertEqual(68, len({e["pin"] for r in lamps for e in r["endpoints"]}))
        self.assertEqual("Q25", next(r for r in lamps if r["public"] == 24)["scr"])
        self.assertEqual("Q24", next(r for r in lamps if r["public"] == 25)["scr"])
        self.assertEqual("Q41", next(r for r in lamps if r["public"] == 42)["scr"])
        coils = self.group("outputs", "pinmame.output.solenoid")
        self.assertEqual(set(range(1, 16)) | set(range(17, 21)) | set(range(45, 49)), set(coils))
        self.assertEqual(curator.UNFITTED_COILS, {n for n, d in coils.items() if d["availability"] == "unused"})
        self.assertEqual(COIL_TEST, {v: int(k) for k, v in self.runtime["runtime"]["observations"]["physical_service_solenoid_to_public"].items()})
        for n, printed in COIL_TEST.items():
            self.assertIn({"namespace": "manual.self-test", "value": str(printed)}, coils[n]["aliases"])
        for n in (45, 47):
            self.assertEqual("used", coils[n]["availability"])
            self.assertEqual("virtual", coils[n]["spatial"]["reason"])
        self.assertEqual({1}, set(self.group("outputs", "physical.output.gi")))

    def test_rom_observations_and_bank_topology(self):
        observations = self.runtime["runtime"]["observations"]
        sweep = {str(s["input_address"]): s for s in observations["runs"]["switch-test"]["named_action_observations"] if s["label"].startswith("matrix diagnostic ")}
        self.assertEqual(set(range(1, 49)) | set(range(81, 89)), {int(n) for n in sweep})
        self.assertTrue(all(sweep[str(n)]["display_responses"][0]["diagnostic_address"] == n for n in range(1, 41)))
        self.assertTrue(all(not sweep[str(n)]["display_responses"] for n in list(range(41, 49))+list(range(81, 89))))
        steps = {s["label"]: s for s in observations["runs"]["gameplay"]["named_action_observations"]}
        def on(label):
            return set(steps[label]["active_solenoid_addresses"])
        self.assertIn(13, on("thumper bumper"))
        self.assertIn(15, on("left slingshot"))
        self.assertIn(14, on("right slingshot"))
        self.assertTrue({9, 10} <= on("left bank target three"))
        self.assertTrue({9, 10} <= on("upper bank target six"))
        self.assertEqual({47, 48}, on("left flipper button"))
        self.assertEqual({45, 46}, on("right flipper button"))
        self.assertEqual(61, observations["switch_to_lamp"]["7"])
        self.assertIn(19, steps["tilt ends flipper enable"]["transitioned_solenoid_addresses"])
        self.assertNotIn(19, on("tilt ends flipper enable"))
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        self.assertEqual(12, len(mechanisms))
        self.assertEqual(["switch.drop-target-1", "switch.drop-target-2", "switch.drop-target-3"], mechanisms["mechanism.left-drop-bank"]["sensors"])
        self.assertEqual(["switch.drop-target-4", "switch.drop-target-5", "switch.drop-target-6"], mechanisms["mechanism.upper-right-drop-bank"]["sensors"])
        self.assertEqual(6, sum(r["kind"] == "inverted" for r in self.definition["relationships"]))

    def test_drop_contact_latching_behavior_is_confined_to_bank_sensors(self):
        switches = self.group("inputs", "pinmame.input.switch")
        sensors = {s for m in self.definition["mechanisms"] if m["kind"] == "drop_target_bank" for s in m["sensors"]}
        def guard(records):
            latching = {n for n, d in records.items() if "remain closed while down" in d.get("physical", {}).get("notes", "")}
            self.assertEqual({27, 28, 29, 30, 31, 32}, latching)
            self.assertEqual(sensors, {records[n]["id"] for n in latching})
            self.assertTrue(all("open when reset raises the targets" in records[n]["physical"]["notes"] for n in latching))
        guard(switches)
        historical = copy.deepcopy(switches)
        historical[6]["physical"]["notes"] += " Drop contacts remain closed while down, and open when reset raises the targets."
        with self.assertRaises(AssertionError):
            guard(historical)

    def test_native_collector_routing_preserves_loads_and_all_branches(self):
        coils = self.group("outputs", "pinmame.output.solenoid")
        expected = {
            1: ("Q2", ["A3J2-4", "A3J1-3"]), 2: ("Q1", ["A3J2-9", "A3J1-2"]),
            3: ("Q5", ["A3J2-10"]), 4: ("Q6", ["A3J2-11"]), 5: ("Q7", ["A3J2-12"]),
            6: ("Q3", ["A3J3-4", "A3J2-5"]), 7: ("Q4", ["A3J1-5"]), 8: ("Q8", ["A3J5-10"]),
            9: ("Q13", ["A3J5-12"]), 10: ("Q14", ["A3J5-11"]),
            11: ("Q9", ["A3J5-9"]), 12: ("Q10", ["A3J5-15"]),
            13: ("Q12", ["A3J5-13"]), 14: ("Q11", ["A3J5-14"]),
            15: ("Q16", ["A3J5-8", "A3J2-6", "A3J3-7"]),
            17: ("Q17", ["A3J5-7"]), 18: ("Q19", ["A3J2-8"]),
            19: ("Q15", ["On-board flipper enable relay terminal 8"]),
            20: ("Q18", ["A3J5-3", "A3J2-15", "A3J3-9"])}
        def guard(records):
            self.assertEqual(expected, {n: (records[n]["wiring"]["driver_transistor"],
                                           records[n]["wiring"]["drive_connection"].split(" / ")) for n in expected})
        guard(coils)
        loads = {1: "Ten point chime", 2: "Hundred point chime", 3: "Thousand point chime", 4: "Ten thousand point chime",
                 6: "Knocker", 7: "Outhole kicker", 9: "Left drop bank reset", 10: "Upper right drop bank reset",
                 13: "Thumper bumper", 14: "Right slingshot", 15: "Left slingshot", 18: "Coin lockout", 19: "Flipper enable relay"}
        self.assertEqual(loads, {n: coils[n]["label"] for n in loads})
        for n, wrong_q, wrong_pin in ((1, "Q1", "A3J2-4"), (6, "Q8", "A3J3-4"),
                                      (7, "Q16", "A3J5-5"), (9, "Q9", "A3J5-9"),
                                      (20, "Q18", "A3J2-15 / A3J3-9")):
            historical = copy.deepcopy(coils)
            historical[n]["wiring"].update(driver_transistor=wrong_q, drive_connection=wrong_pin)
            with self.assertRaises(AssertionError):
                guard(historical)
        for n in (5, 8, 11, 12):
            self.assertIn("printed test number is blank", coils[n]["physical"]["notes"])
            self.assertIn({"namespace": "manual.self-test", "value": str(COIL_TEST[n])}, coils[n]["aliases"])
        routing = load_json(ROOT / curator.COIL_DECODER)
        self.assertEqual("validated", routing["status"])
        self.assertEqual(expected, {r["public"]: (r["driver_transistor"], r["drive_connections"])
                                    for r in routing["routes"] + routing["continuous_routes"]})
        self.assertEqual(list(range(15)), [r["selector"] for r in routing["routes"]])
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16], [r["u2_pin"] for r in routing["routes"]])
        self.assertEqual({5, 8, 11, 12}, {r["public"] for r in routing["routes"] if r["printed_test"] == "[blank]"})
        excerpt = (ROOT / "evidence/excerpts/stern.stars.1978/solenoid-wiring.md").read_text(encoding="utf-8")
        for n in (5, 8, 11, 12):
            q, pins = expected[n]
            self.assertIn(f"| {n} | {q} | {pins[0]} | N/U | [blank] | [blank] |", excerpt)
        relay = coils[19]["wiring"]
        self.assertEqual(("A3J3-5", "Y-W", 43), (relay["power_connection"], relay["power_wire"], relay["nominal_voltage_v"]))
        self.assertNotIn("drive_wire", relay)
        report = load_json(ROOT / curator.REPORT)
        self.assertEqual(routing, report["coil_decoder_routing"]["readings"])
        prose = excerpt + (ROOT / curator.KNOWLEDGE).read_text(encoding="utf-8") + str(self.definition)
        for wrong in ("wiring-detail disagreement", "contradictory decoder", "conditional decoder candidates", "assignments remain unresolved"):
            self.assertNotIn(wrong, prose)
        source = next(s for s in self.definition["sources"] if s["id"] == curator.MANUAL)
        drawing = next(e for e in source["excerpts"] if e["id"] == "excerpt.stars.solenoid-wiring")
        self.assertEqual(curator.sha256(ROOT / drawing["image"]), drawing["image_sha256"])
        self.assertIn("native resolution", drawing["image_derivation"])

    def test_ca3081_base_and_collector_pins_match_bulletin9(self):
        routing = load_json(ROOT / curator.COIL_DECODER)
        def guard(rows):
            by_q = {r["driver_transistor"]: (r["stage"], r["base_pin"], r["collector_pin"]) for r in rows}
            self.assertEqual(("U1", 16, 1), by_q["Q1"])
            self.assertEqual(("U3", 16, 1), by_q["Q8"])
        guard(routing["routes"])
        for q in ("Q1", "Q8"):
            historical = copy.deepcopy(routing["routes"])
            next(r for r in historical if r["driver_transistor"] == q).update(base_pin=1, collector_pin=16)
            with self.assertRaises(AssertionError):
                guard(historical)
        excerpt = (ROOT / "evidence/excerpts/stern.stars.1978/coils-and-options.md").read_text(encoding="utf-8")
        for row in routing["routes"]:
            self.assertIn(f"| {row['driver_transistor']} | {row['stage']} | {row['base_pin']} | {row['collector_pin']} |", excerpt)
        self.assertIn("jack J1, J2 or J5 (Point B)", excerpt)
        coils = self.group("outputs", "pinmame.output.solenoid")
        self.assertTrue(all("bulletin.stars.9" in coils[n]["provenance"]["source_refs"] for n in range(1, 16)))

    def test_lamp_split_branches_keep_unknown_location_and_computed_counts(self):
        rows = load_json(ROOT / curator.LAMPS)
        lamps = self.group("outputs", "pinmame.output.lamp")
        partial = {r["public"]: r for r in rows if any(e["label"] == "[blank]" for e in r["endpoints"])
                   and any(e["label"] != "[blank]" for e in r["endpoints"])}
        self.assertEqual({11, 12, 27, 28, 43, 44, 59, 60}, set(partial))
        def guard(records):
            for n in partial:
                self.assertNotIn("spatial", records[n], f"Partially named split {n} cannot be exempted as cabinet-only")
                self.assertNotIn("quantity", records[n]["physical"])
                self.assertNotIn("location", records[n]["physical"])
        guard(lamps)
        historical = copy.deepcopy(lamps)
        historical[27]["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service"}
        with self.assertRaises(AssertionError):
            guard(historical)
        for n, row in partial.items():
            self.assertIn("physical location and quantity are unknown", lamps[n]["physical"]["notes"])
            for e in row["endpoints"]:
                if e["label"] == "[blank]":
                    self.assertIn(e["pin"], lamps[n]["physical"]["notes"])
        match = partial[27]["endpoints"]
        self.assertEqual({("A5J2-8", "MATCH"), ("A5J1-4", "[blank]")}, {(e["pin"], e["label"]) for e in match})
        self.assertIn(lamps[27]["id"], load_json(ROOT / curator.REPORT)["unplaced_devices"])
        stats = curator.lamp_inventory(rows)
        self.assertEqual((60, 68, 13, 21, 8), (stats["output_count"], stats["endpoint_count"], len(stats["unnamed_outputs"]),
                                           stats["blank_endpoint_count"], stats["blank_split_endpoint_count"]))
        self.assertEqual(stats, load_json(ROOT / curator.REPORT)["lamp_inventory"])
        changed = copy.deepcopy(rows)
        next(e for r in changed if r["public"] == 27 for e in r["endpoints"] if e["label"] == "[blank]")["label"] = "test named branch"
        changed_stats = curator.lamp_inventory(changed)
        self.assertEqual((20, 7), (changed_stats["blank_endpoint_count"], changed_stats["blank_split_endpoint_count"]))
        self.assertIn("20 connector endpoints", curator.lamp_inventory_summary(changed_stats))
        self.assertIn("7 additional blank branches", curator.lamp_inventory_summary(changed_stats))
        self.assertIn(curator.lamp_inventory_summary(stats), (ROOT / curator.KNOWLEDGE).read_text(encoding="utf-8"))

    def test_spatial_proxies_and_partial_gate(self):
        self.assertEqual([], validate_machine(self.definition, ROOT))
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertEqual({"output_semantics", "variant_differences", "provenance", "spatial_placement"}, set(self.definition["coverage"]["missing"]))
        self.assertEqual([], self.definition["conflicts"])
        profile = load_json(ROOT / "controllers/pinmame/stern-mpu100.json")
        self.assertEqual(curator.REVISION, profile["sources"][0]["revision"])
        self.assertEqual(self.definition["controller"]["platform"], profile["id"])
        switches = self.group("inputs", "pinmame.input.switch")
        self.assertGreater(switches[36]["spatial"]["placements"][0]["x"], .5)
        self.assertLess(switches[37]["spatial"]["placements"][0]["x"], .5)
        lamps = self.group("outputs", "pinmame.output.lamp")
        self.assertTrue(all("placements" not in d.get("spatial", {}) for d in lamps.values()))
        gi = self.group("outputs", "physical.output.gi")[1]
        self.assertEqual(19, len(gi["spatial"]["placements"]))
        self.assertNotIn("quantity", gi["physical"])
        table = self.evidence["tables"]["primary"]
        for i, placement in zip(range(2, 39, 2), gi["spatial"]["placements"], strict=True):
            obj = table["objects"][f"GI_{i}"]
            self.assertTrue(obj["show_bulb_mesh"])
            self.assertEqual(round(obj["x"]/952, 6), placement["x"])
            self.assertEqual(round(obj["y"]/1974, 6), placement["y"])
        promoted = copy.deepcopy(self.definition)
        promoted["coverage"]["status"] = "author_ready"
        promoted["coverage"]["missing"] = []
        self.assertTrue(validate_machine(promoted, ROOT), "Unresolved physical evidence must block promotion")

    def test_reproducible_products_and_mutation_guards(self):
        curator.check(ROOT)
        self.assertEqual((ROOT / curator.SEED).read_bytes(), (ROOT / curator.DEFINITION).read_bytes())
        first = curator.products(ROOT)
        self.assertEqual(first, curator.products(ROOT))
        with self.scratch() as temporary:
            root = Path(temporary)
            metadata = load_json(ROOT / curator.PROVENANCE)
            for path in list(metadata["portable_sha256"])+[curator.PROVENANCE.as_posix()]:
                dest = root / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, dest)
            curator.verify_portable(root)
            with (root / curator.EVIDENCE).open("ab") as stream:
                stream.write(b" ")
            with self.assertRaisesRegex(RuntimeError, "pinned portable evidence"):
                curator.verify_portable(root)
        with self.scratch() as temporary:
            root = Path(temporary)
            path = root / curator.AUTHOR_READY
            path.parent.mkdir(parents=True)
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.check(root)
            with self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.generate(root)

    def test_source_roles_exact_hashes_and_retained_evidence(self):
        curator.verify_portable(ROOT)
        source = {s["id"]: s for s in self.definition["sources"]}
        self.assertEqual(curator.REVISION, source[curator.CORE]["revision"])
        self.assertFalse(source[curator.TABLE]["known_working"])
        self.assertEqual("87a44c8d8cdffb275482afa2e43de2fe923944ae175786034730e3c5706f28ed", source[curator.SCRIPT]["sha256"])
        for s in self.definition["sources"]:
            for excerpt in s.get("excerpts", []):
                self.assertEqual(curator.sha256(ROOT / excerpt["path"]), excerpt["sha256"])
        self.assertEqual("pinmame-spatial-blockers", load_json(ROOT / curator.REPORT)["format"])
        names = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not any(os.environ.get(n) for n in names):
            self.skipTest("Optional retained Stars roots not configured; portable checks above still ran")
        self.assertTrue(all(os.environ.get(n) for n in names), "Partially configured evidence roots must not silently skip")
        curator.verify_evidence(ROOT)
        actual_sha256 = curator.sha256
        def changed_native(path):
            return "0"*64 if path.name == "Stern_1978_Stars_Manual-p25.png" else actual_sha256(path)
        with patch.object(curator, "sha256", side_effect=changed_native):
            with self.assertRaisesRegex(RuntimeError, "collector retrace native render changed"):
                curator.verify_evidence(ROOT)
        review = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
        self.assertEqual(canonical_bytes(runtime_build(review / curator.MACHINE_ID / "harness")), (ROOT / curator.RUNTIME).read_bytes())
        with self.scratch() as temporary, patch.dict(os.environ, {n: temporary for n in names}):
            with self.assertRaises((OSError, ValueError, RuntimeError)):
                curator.verify_evidence(ROOT)

    def test_new_table_and_independent_drawing_reconciliation(self):
        bord = self.evidence["tables"]["bord-1.0.2"]
        self.assertEqual((952.9412, 1976.4706), (bord["bounds"]["right"], bord["bounds"]["bottom"]))
        self.assertEqual("4a6362487f2628e5d1685e2f51a05fb21f003a12be4f7ff4a727c825bbb0f6a3", bord["table_sha256"])
        self.assertEqual((34, 44, 16), (len(bord["lamp_bindings"]), sum(map(len, bord["lamp_bindings"].values())), len(bord["gi_collection"])))
        self.assertEqual([], bord["visible_bulb_mesh_lights"])
        self.assertTrue(all(not o["show_bulb_mesh"] for o in bord["objects"].values() if o["type"] == "Light"))
        seed = load_json(ROOT / curator.CALLOUTS)
        self.assertIn(curator.CALLOUTS.as_posix(), load_json(ROOT / curator.PROVENANCE)["portable_sha256"])
        decisions = evaluate(seed, placements_of(self.definition), seed["limit"])
        report = load_json(ROOT / curator.REPORT)
        self.assertEqual(decisions["pages"], report["manual_callouts"]["pages"])
        self.assertEqual(decisions["placements"], report["manual_callouts"]["placements"])
        switches = {p: d for p, d in decisions["placements"].items() if p.startswith("switch.")}
        self.assertEqual(30, len(switches))
        self.assertEqual(["switch.bonus-rollovers.sensor.1"], [p for p, d in switches.items() if not d["agrees"]])
        self.assertEqual(0.1063, switches["switch.bonus-rollovers.sensor.1"]["control_offset"])
        changed = copy.deepcopy(seed)
        changed["pages"]["pdf-19"]["reads"][15]["pixel"] = [0, 0]
        self.assertFalse(evaluate(changed, placements_of(self.definition))["placements"]["switch.left-outlane.sensor.1"]["agrees"])
        self.assertEqual("observed", self.group("inputs", "pinmame.input.switch")[15]["spatial"]["status"])
        with self.scratch() as temporary:
            self.assertTrue(Path(temporary).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve()))


if __name__ == "__main__":
    unittest.main()
