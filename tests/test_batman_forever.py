"""Regression gates for Batman Forever's physical machine, public paths and retained evidence.

The fixtures below protect independently read facts rather than copying the curator's arrays.
External gates recompute manifests, raw observations, frame readings and geometry when evidence
roots are supplied, and refuse mutated runs.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_batman_forever as curator
from pinmame_game_defs.jsonio import canonical_bytes, load_json

KEY = "sega.batman-forever.1995"
RUNTIME = ROOT / "evidence/runtime/data-east/batman-forever-batmanf-service-tests.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def devices(definition, field, group):
    return {d["binding"]["device"]: d for d in definition[field] if d["binding"]["group"] == group}


class BatmanForeverDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(curator.DEFINITION_PATH)
        cls.switches = devices(cls.definition, "inputs", "pinmame.input.switch")
        cls.coils = devices(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.lamps = devices(cls.definition, "outputs", "pinmame.output.lamp")
        cls.sources = {s["id"]: s for s in cls.definition["sources"]}
        cls.readings = load_json(curator.READINGS_PATH)
        cls.runtime = load_json(RUNTIME)["runtime"]

    def test_identity_variants_and_controller_are_data_east_3b(self):
        machine = self.definition["machine"]
        self.assertEqual((KEY, 3593, "38", "G59zN-MLy0N", 1995),
                         (machine["id"], machine["ipdb_id"], machine["model_number"], machine["opdb_id"], machine["year"]))
        drivers = {d["id"]: d for d in self.definition["drivers"]}
        self.assertEqual(23, len(drivers))
        self.assertEqual({"batmanf1", "batmanf2", "batmanf3", "batmanf5", "batmanf501"} | {f"bmf_{x}" for x in
                         ("at", "be", "ch", "cn", "de", "fr", "it", "it2", "it3", "jp", "nl", "nl302", "no", "sp", "sv", "time", "uk")},
                         {n for n, d in drivers.items() if d.get("clone_of") == "batmanf"})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in drivers.values()))
        self.assertEqual(("2024", "2025"), (drivers["batmanf5"]["year"], drivers["batmanf501"]["year"]))
        self.assertEqual("pinmame.dataeast", self.definition["controller"]["platform"])
        self.assertEqual("0x8000", self.definition["controller"]["hardware_generation"])
        self.assertEqual([(192, 64)], [(d["width"], d["height"]) for d in self.definition["displays"]])
        self.assertEqual((1093, 2162), (machine["playfield"]["width"], machine["playfield"]["height"]))

    def test_entire_public_inventory_and_availability(self):
        self.assertEqual({-7, -6, *range(1, 65), *range(81, 89)}, set(self.switches))
        self.assertEqual(set(range(1, 65)), set(self.coils))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        self.assertEqual({9, 10, 17, 31}, {n for n in range(1, 65) if self.switches[n]["availability"] == "unused"})
        self.assertEqual(set(range(37, 45)), {n for n, d in self.coils.items() if d["availability"] == "unknown"})
        self.assertEqual({6, 13, 24, *range(33, 37), *range(49, 65)}, {n for n, d in self.coils.items() if d["availability"] == "unused"})
        self.assertEqual({36, 37, 38, 60}, {n for n, d in self.lamps.items() if d["availability"] == "unused"})
        self.assertEqual({1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14, 15, 16, *range(17, 24), *range(25, 33), *range(45, 49)},
                         {n for n, d in self.coils.items() if d["availability"] == "used"})

    def test_unfitted_drivers_explain_their_diagnostic_state(self):
        for n in (6, 13):
            notes = self.coils[n]["physical"]["notes"]
            self.assertEqual("virtual", self.coils[n]["kind"])
            self.assertIn("NOT USED", notes)
            self.assertIn("No gameplay or attract run published it", notes)
            self.assertIn(curator.RUNTIME, self.coils[n]["provenance"]["source_refs"])
        self.assertIn("NO COIL AT THIS LOCATION", self.coils[6]["physical"]["notes"])
        self.assertIn("CN12-6", self.coils[13]["physical"]["notes"])

    def test_physical_contacts_rest_open_and_the_opto_is_not_reinverted(self):
        for n in range(1, 65):
            if n not in (9, 10, 17, 31):
                self.assertIs(False, self.switches[n]["normally_closed"], n)
        self.assertEqual("opto", self.switches[15]["physical"]["switch_type"])
        self.assertIn("blocked beam a closed one", self.switches[15]["physical"]["notes"])
        for n in (-7, -6, 82, 84):
            self.assertIs(False, self.switches[n]["normally_closed"])
        self.assertTrue(self.switches[-7]["pulse"] and self.switches[-6]["pulse"])
        self.assertIn("does not say which wire serves which button", self.switches[-6]["physical"]["notes"])
        self.assertNotIn("wiring", self.switches[-7])
        rest = [r for r in self.readings["readings"] if r["label"] == "to-switch-test"]
        self.assertEqual(["SWITCH TEST NONE (no switch closed)"], [r["name"] for r in rest])

    def test_rom_and_grid_correct_the_parts_list_misprints(self):
        self.assertEqual(("Right Bad Heads Stand-up", "Left Ramp Exit", "Middle Ramp Exit"),
                         tuple(self.switches[n]["label"] for n in (51, 53, 54)))
        rom = {r["address"]: r["name"] for r in self.readings["readings"] if r["group"] == "switch"}
        self.assertEqual("#51 RIGHT BAD HEADS S-U", rom[51])
        self.assertEqual(("#53 LEFT RAMP EXIT", "#54 MIDDLE RAMP EXIT"), (rom[53], rom[54]))
        excerpt = (curator.EXCERPTS / "switches.md").read_text(encoding="utf-8")
        self.assertIn("| 53 | LEFT RAMP EXIT | MIDDLE RAMP EXIT (On Ramp) | 180-5093-00 |", excerpt)
        self.assertIn("| 51 | RIGHT BAD HEADS S-U | RIGHT GOOD HEADS STAND-UP BOTTOM | 515-5162-08 |", excerpt)
        self.assertIn("Manual is wrong", self.switches[53]["physical"]["notes"])

    def test_rom_service_names_cover_every_address(self):
        groups = {}
        for reading in self.readings["readings"]:
            groups.setdefault(reading["group"], set()).add(reading.get("address"))
        self.assertEqual(set(range(1, 65)) | {84}, groups["switch"])
        copy84 = next(r for r in self.readings["readings"] if r["group"] == "switch" and r["address"] == 84)
        self.assertEqual(("#63 L FLIPPERS (Q7)", "WHT-VIO", "CN10-P2", "CN8-P9 Q48"),
                         (copy84["name"], copy84["return_wire"], copy84["return_pin"], copy84["drive"]))
        self.assertEqual(set(range(1, 65)), groups["lamp"])
        self.assertEqual({*range(1, 10), *range(11, 23), *range(25, 33)}, groups["solenoid"])
        for reading in self.readings["readings"]:
            if reading["group"] in ("switch", "lamp") and reading["address"] <= 64:
                self.assertTrue(reading["name"].startswith(f"#{reading['address']:02d} "), reading["name"])
            self.assertRegex(reading["pixel_sha256"], "^[0-9a-f]{64}$")
        self.assertEqual(173, len(self.runtime["observations"]["diagnostic_snapshots"]))
        screens = {r["label"]: r["name"] for r in self.readings["readings"] if r["group"] == "screen"}
        self.assertEqual("ADJUSTMENT 43 GAME ID 0", screens["sega-press-43"])
        self.assertTrue(screens["sega-press-44"].startswith("ADJUSTMENT 1 "))
        self.assertEqual("ADJUSTMENT 52 NOVICE GAME AVAILABLE YES", screens["bat-adjustment-52"])
        self.assertNotIn("PRNT", screens["main-menu-diag"])
        self.assertEqual({"unknown"}, {self.coils[n]["availability"] for n in range(37, 45)})

    def test_literal_driver_cells_and_wiring_follow_the_chart(self):
        self.assertEqual(("Q44/Q5", "CPU/PPB", "VIO-ORG", "PPB J8-2", "YEL-VIO", "PPB J7-8"),
                         tuple(self.coils[3]["wiring"][k] for k in ("driver_transistor", "board", "control_wire", "control_connection", "power_wire", "power_connection")))
        self.assertEqual(("Q46", "VIO-BRN", "PPB J2-1"), tuple(self.coils[1]["wiring"][k] for k in ("driver_transistor", "control_wire", "control_connection")))
        self.assertEqual(("Q46", "BLK-BRN", "PPB J9-1"), tuple(self.coils[25]["wiring"][k] for k in ("driver_transistor", "control_wire", "control_connection")))
        self.assertEqual("Q13/Q1", self.coils[22]["wiring"]["driver_transistor"])
        self.assertEqual({25: "4X #89 0X #906", 28: "3X #89 1X #906", 30: "2X #89 2X #906", 32: "3X #89 1X #906"},
                         {n: self.coils[n]["physical"]["part_number"] for n in (25, 28, 30, 32)})
        self.assertTrue(all(self.coils[n]["physical"]["quantity"] == 4 for n in range(25, 33)))
        self.assertEqual(("motor", "515-6383-00"), (self.coils[14]["kind"], self.coils[14]["physical"]["part_number"]))
        self.assertIn("520-5010-00", self.coils[14]["physical"]["notes"])
        self.assertEqual(("relay", "gi"), (self.coils[10]["kind"], self.coils[11]["kind"]))
        self.assertEqual(("Q55", "GRN-BRN", "CN8-1", "WHT-BRN", "CN10-9"),
                         tuple(self.switches[1]["wiring"][k] for k in ("driver_transistor", "drive_wire", "drive_connection", "return_wire", "return_connection")))
        self.assertEqual(("Q48", "CN8-9", "WHT-GRY", "CN10-1"),
                         tuple(self.switches[64]["wiring"][k] for k in ("driver_transistor", "drive_connection", "return_wire", "return_connection")))

    def test_lamp_bulbs_follow_the_chart_and_rom_where_the_grid_differs(self):
        self.assertEqual("#44 bayonet 165-5000-44", self.lamps[50]["physical"]["part_number"])
        self.assertIn("The manual grid prints #555", self.lamps[50]["physical"]["notes"])
        self.assertEqual("#555 wedge 165-5002-00", self.lamps[51]["physical"]["part_number"])
        self.assertEqual("#44 bayonet 165-5000-44", self.lamps[49]["physical"]["part_number"])
        self.assertIn("names no lamp numbers", self.lamps[49]["physical"]["notes"])
        self.assertEqual(("Q67", "CN7-5"), (self.lamps[33]["wiring"]["driver_transistor"], self.lamps[33]["wiring"]["drive_connection"]))
        self.assertIn("GN7-5", self.lamps[33]["physical"]["notes"])
        self.assertEqual(("Q79", "RED-GRY", "CN6-9"),
                         tuple(self.lamps[64]["wiring"][k] for k in ("return_component", "return_wire", "return_connection")))

    def test_table_lamp_binding_defects_do_not_become_sockets(self):
        for n in (33, 34):
            placements = self.lamps[n]["spatial"]["placements"]
            self.assertEqual(["candidate"], [p["provenance"]["status"] for p in placements])
            self.assertEqual([curator.MANUAL, curator.CALLOUTS], placements[0]["provenance"]["source_refs"])
            self.assertIn("TimerInterval 33", self.lamps[n]["physical"]["notes"])
        self.assertEqual((0.417, 0.191), (self.lamps[33]["spatial"]["placements"][0]["x"], self.lamps[33]["spatial"]["placements"][0]["y"]))
        placement = self.lamps[59]["spatial"]["placements"][0]
        self.assertNotIn(curator.SCRIPT, placement["provenance"]["source_refs"])
        self.assertNotIn(curator.SCRIPT, self.lamps[59]["provenance"]["source_refs"])
        self.assertIn("TimerInterval 58", self.lamps[59]["physical"]["notes"])
        self.assertEqual(1, len(self.lamps[58]["spatial"]["placements"]))

    def test_cabinet_buttons_drive_the_copy_and_synthetic_pairs(self):
        self.assertEqual(["flipper.lower.left.button"], self.switches[84]["roles"])
        self.assertEqual(["flipper.lower.right.button"], self.switches[82]["roles"])
        self.assertEqual(["flipper.lower.left.matrix-copy"], self.switches[63]["roles"])
        self.assertIn("upper right flipper", self.switches[82]["physical"]["notes"])
        for n in (45, 46, 47, 48):
            self.assertEqual(("virtual", "used"), (self.coils[n]["kind"], self.coils[n]["availability"]))
        copies = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["kind"] == "direct"}
        self.assertEqual({(self.switches[82]["id"], self.switches[64]["id"]), (self.switches[84]["id"], self.switches[63]["id"])}, copies)
        observations = self.runtime["observations"]["runs"]["gameplay"]["named_action_observations"]
        self.assertEqual({(45, 46), (47, 48)}, {tuple(o["held_synthetic_solenoid_addresses"]) for o in observations if "held_synthetic_solenoid_addresses" in o})

    def test_mechanisms_own_the_right_devices(self):
        mech = {m["id"]: m for m in self.definition["mechanisms"]}
        ids = {**{n: d["id"] for n, d in self.switches.items()}}
        sol = {n: d["id"] for n, d in self.coils.items()}
        self.assertEqual(([sol[1], sol[2]], [ids[n] for n in (11, 12, 13, 14, 15)]), (mech["mech.trough"]["actuators"], mech["mech.trough"]["sensors"]))
        self.assertEqual(([sol[14], sol[15]], [ids[n] for n in (44, 45, 46, 49)]),
                         (mech["mech.batwing-cannon"]["actuators"], mech["mech.batwing-cannon"]["sensors"]))
        self.assertEqual("motorized", mech["mech.batwing-cannon"]["kind"])
        self.assertEqual(([sol[9]], [ids[n] for n in (62, 61, 60)]), (mech["mech.batcave-lock"]["actuators"], mech["mech.batcave-lock"]["sensors"]))
        self.assertEqual([sol[16]], mech["mech.batcave-exit"]["actuators"])
        self.assertEqual([sol[12]], mech["mech.ramp-diverter"]["actuators"])
        self.assertEqual(([sol[7]], [ids[n] for n in (18, 19, 20, 21)]), (mech["mech.drops"]["actuators"], mech["mech.drops"]["sensors"]))
        pulses = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["kind"] == "pulse"}
        self.assertEqual({(ids[s], sol[o]) for s, o in ((57, 17), (58, 18), (59, 19), (35, 20), (36, 21))}, pulses)
        gated = {r["destination"] for r in self.definition["relationships"] if r["kind"] == "relay_gated"}
        self.assertEqual({sol[n] for n in range(25, 33)}, gated)

    def test_gameplay_checkpoints_name_each_stimulus(self):
        observations = {o["label"]: o for o in self.runtime["observations"]["runs"]["gameplay"]["named_action_observations"]}
        expected = {"trough-upkick": (15, 2), "gun-trigger-autolaunch": (49, 3), "top-eject-kick": (41, 5), "vuk-kick": (32, 4),
                    "batcave-exit-kick": (30, 16), "cannon-motor-starts": (44, 14), "gun-trigger-fires-cannon": (49, 15),
                    "output-22": (33, 22), "lock-reserve-lockout": (62, 1), "drop-bank-reset": (21, 7)}
        for label, (switch, output) in expected.items():
            self.assertEqual((switch, [output]), (observations[label]["input_address"], observations[label]["transitioned_solenoid_addresses"]), label)
        self.assertEqual([18, 19, 20, 21], observations["drop-bank-reset"]["host_stimulus_switch_addresses"])
        coil_test = {o["label"]: o["transitioned_solenoid_addresses"] for o in self.runtime["observations"]["runs"]["coil-test"]["named_action_observations"]}
        self.assertEqual([13], coil_test["entry-20-fired"])
        self.assertEqual([29], coil_test["entry-10-fired"])
        self.assertNotIn("entry-11-fired", coil_test)

    def test_placements_are_observed_or_drawing_validated_with_explicit_omissions(self):
        report = load_json(curator.SPATIAL_REPORT_PATH)
        for n in (11, 12, 13, 14, 45, 46, 60, 61, 62):
            self.assertNotIn("spatial", self.switches[n])
            self.assertIn(self.switches[n]["id"], report["omitted_spatial_key_devices"])
        self.assertNotIn("spatial", self.coils[1])
        statuses = {}
        for group in (self.switches, self.coils, self.lamps):
            for item in group.values():
                for placement in item.get("spatial", {}).get("placements", []):
                    statuses[placement["provenance"]["status"]] = statuses.get(placement["provenance"]["status"], 0) + 1
                    self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1)
                    if placement["provenance"]["status"] == "validated":
                        self.assertIn(curator.CALLOUTS, placement["provenance"]["source_refs"])
        self.assertEqual({"validated": 108, "observed": 45, "candidate": 2}, statuses)
        check = report["drawing_callout_check"]
        self.assertEqual((118, 108), (check["checked"], check["validated"]))
        self.assertEqual({"12", "5L", "3R", "30", "44", "53", "54", "56", "36", "41"},
                         {item["label"] for item in check["not_validated"].values()})
        # Leader-less top-rail boxes check nothing, so the back-panel flasher lights are excluded.
        seed = load_json(curator.CALLOUT_SEED)
        self.assertEqual({28, 29, 30, 31}, {self.coils[n]["binding"]["device"] for n in range(25, 33)
                                             if any(p["id"] in seed["excluded_checks"] for p in self.coils[n]["spatial"]["placements"])})
        self.assertEqual({"top-rail"}, {r["region"] for r in seed["pages"]["pdf-33-flash"]["reads"] if r["point"] == "label_beside_part" and r["pixel"][1] < 250})
        self.assertEqual(["validated"], [p["provenance"]["status"] for p in self.switches[57]["spatial"]["placements"]])
        self.assertIn("parts list's way", self.switches[53]["physical"]["notes"])
        self.assertIn("ramp socket", self.coils[27]["physical"]["notes"])
        self.assertEqual(31, len(self.coils[11]["spatial"]["placements"]))
        self.assertIn("projected", report["projection_notes"]["solenoid.7"])
        self.assertIn("spatial_placement", self.definition["coverage"]["missing"])

    def test_no_sibling_record_leak_and_precise_partial_dimensions(self):
        text = curator.DEFINITION_PATH.read_text(encoding="utf-8")
        for sibling in ("baywatch", "Baywatch", "shark", "SHARK"):
            self.assertNotIn(sibling, text)
        self.assertEqual(["input_semantics", "output_semantics", "spatial_placement"], self.definition["coverage"]["missing"])
        self.assertEqual([], self.definition["conflicts"])
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertTrue(curator.DEFINITION_PATH.parent.name == "sega" and "partial" in curator.DEFINITION_PATH.parts)
        self.assertFalse(any(s["id"].startswith("vpx-script.") and len(s["id"]) == 27 for s in self.definition["sources"]))

    def test_curator_seed_and_all_generated_artifacts_are_deterministic(self):
        for path, payload in curator.artifacts():
            self.assertEqual(path.read_bytes().replace(b"\r\n", b"\n"), payload.replace(b"\r\n", b"\n"), path.name)
        self.assertEqual(canonical_bytes(self.definition), curator.SEED_PATH.read_bytes().replace(b"\r\n", b"\n"))

    def test_curator_guards_fail_on_missing_rows_and_promotion(self):
        original = curator.rows

        def drop_one(filename, columns, first=r"\d+[LR]?"):
            result = original(filename, columns, first)
            return result[:-1] if filename == "lamps.md" and columns == 3 else result

        with patch.object(curator, "rows", drop_one):
            with self.assertRaisesRegex(ValueError, "incomplete"):
                curator.build()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / f"machines/author-ready/sega/{curator.SLUG}.json"
            target.parent.mkdir(parents=True)
            target.write_text("{}", encoding="utf-8")
            with patch.object(sys, "argv", ["curate", "--check", "--repository-root", directory]), patch.dict(os.environ, {}, clear=False):
                for name in ("PINMAME_MANUALS_ROOT", "PINMAME_VPX_SOURCES_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"):
                    os.environ.pop(name, None)
                with self.assertRaisesRegex(ValueError, "author-ready"):
                    curator.main()


class BatmanForeverRetainedEvidenceTests(unittest.TestCase):
    def root(self, name):
        if not os.environ.get(name):
            self.skipTest(f"{name} is not declared")
        return Path(os.environ[name])

    def test_recompute_exact_table_geometry_and_extraction(self):
        from build_batman_forever_places import build
        vpx = self.root("PINMAME_VPX_SOURCES_ROOT")
        review = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")
        world = review / KEY / "world-obj/Batman Forever (Sega 1995) 1.3.obj"
        self.assertEqual(load_json(ROOT / "tools/batman_forever_places.json"), build(vpx, world))

    def test_retained_script_bindings_match_the_curated_routes(self):
        script = (self.root("PINMAME_VPX_SOURCES_ROOT") / "sega/batman-forever-1995/extracted-vpxtool/script.vbs").read_text(encoding="latin-1")
        callbacks = {int(n): value for n, value in re.findall(r'(?im)^SolCallback\((\d+)\)\s*=\s*"([^"]+)"', script)}
        self.assertEqual({1: "SolTroughBall", 2: "bsBallRelease.SolOut", 3: "Autoplunger", 4: "SolVUK", 5: "SolTopEject",
                          7: "DropTargetBankSolDropUp", 9: "bsBallLock.SolOut", 12: "SolRampDiverter", 14: "SolBatwingMotor",
                          15: "SolFireBWGun", 16: "SolBatCaveExit", 22: "KickSaver"},
                         {n: callbacks[n] for n in (1, 2, 3, 4, 5, 7, 9, 12, 14, 15, 16, 22)})
        self.assertNotIn(6, callbacks)
        self.assertNotIn(13, callbacks)
        for binding in ("bsTrough.InitSw 0,14,13,12,11,0,0,0", "bsBallLock.InitSw 0,62,61,60,0,0,0,0", "mBWGun.Sol1 = 14",
                        "mBWGun.AddSw 46,0,3", "Controller.Switch(49)  = 1", "LoadVPM \"01560000\",\"DE.VBS\",3.1"):
            self.assertIn(binding, script)

    def test_pinned_driver_block_and_rom_members_match_the_initializer(self):
        from pinmame_game_defs.workspace import resolve_working_root
        working = resolve_working_root(ROOT)
        source = Path(os.environ["PINMAME_SOURCE_ROOT"]) if os.environ.get("PINMAME_SOURCE_ROOT") else working / "source-checkouts/pinmame" if working else None
        if source is None or not (source / "src/wpc/degames.c").is_file():
            self.skipTest("pinned PinMAME source is unavailable")
        text = (source / "src/wpc/degames.c").read_text(encoding="utf-8")
        self.assertIn("INITGAMES11(batmanf, GEN_DEDMD64, de_192x64DMD, FLIP6364, SNDBRD_DE2S, SNDBRD_DEDMD64, S11_PRINTERLINE)", text)
        block = text[text.index("INITGAMES11(batmanf,"):text.index("#define input_ports_batmanf input_ports_des112")]
        for member in load_json(curator.READINGS_PATH)["rom_members"]:
            self.assertIn(member["name"], block)
            self.assertIn(member["sha1"], block)
        for driver in self.__class__.clones():
            self.assertIn(f"#define init_{driver}", text)

    @staticmethod
    def clones():
        return [d["id"] for d in load_json(curator.DEFINITION_PATH)["drivers"] if d["id"] != "batmanf"]

    def test_drawing_callout_renders_and_reading_artifacts_are_retained(self):
        import drawing_callouts
        seed = load_json(curator.CALLOUT_SEED)
        checked = drawing_callouts.verify_retained(seed, ROOT, self.root("PINMAME_MANUALS_ROOT"), self.root("PINMAME_REVIEW_ARTIFACTS_ROOT"))
        self.assertGreater(checked, 4)
        for pid in seed["measurements"]:
            self.assertEqual(seed["measurements"][pid]["normalized"], list(drawing_callouts.measured(seed, pid)))

    def test_manual_pins_fail_when_declared_root_is_wrong(self):
        self.root("PINMAME_MANUALS_ROOT")
        curator.verify_external()
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": directory}):
                with self.assertRaisesRegex(ValueError, "manual missing or changed"):
                    curator.verify_external()

    def test_raw_runtime_manifest_frame_readings_and_checkpoints_recompute(self):
        from build_batman_forever_runtime import build
        self.assertEqual(load_json(RUNTIME), build(self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")))

    def test_runtime_builder_refuses_changed_runs_scenarios_and_claims(self):
        import build_batman_forever_runtime as builder
        review = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")
        original_digest = builder.digest
        with patch.object(builder, "digest", side_effect=lambda p: "0" * 64 if p.parent.name == "coil-test" and p.name == "run.json" else original_digest(p)):
            with self.assertRaisesRegex(ValueError, "raw run changed"):
                builder.build(review)
        original_read = builder.read_json
        scenario = ROOT / "tools/harness-scenarios/data-east/batmanf-gameplay.json"

        def changed_scenario(path):
            data = original_read(path)
            if Path(path) == scenario:
                data = copy.deepcopy(data)
                data["notes"] = "changed"
            return data

        with patch.object(builder, "read_json", changed_scenario):
            with self.assertRaisesRegex(ValueError, "scenario changed"):
                builder.build(review)

        def mutated(change):
            def read(path):
                data = original_read(path)
                if Path(path).name == "run.json":
                    data = copy.deepcopy(data)
                    change(Path(path).parent.name, data)
                return data
            return read

        def lamp(name, run):
            if name == "lamp-test":
                next(s for s in run["snapshots"] if s["label"] == "lamp-step-40")["active_lamps"] = [41]

        def frame(name, run):
            if name == "switch-test":
                next(s for s in run["snapshots"] if s["label"] == "switch-30-closed")["displays"][0]["pixel_sha256"] = "0" * 64

        def checkpoint(name, run):
            if name == "gameplay":
                step = next(s for s in run["steps"] if s["label"] == "vuk-kick")
                step["matched_outputs"] = []

        def level(name, run):
            if name == "switch-test":
                snap = next(s for s in run["snapshots"] if s["label"] == "switch-41-closed")
                next(w for w in snap["watched_switches"] if w["number"] == 41)["state"] = 0

        def coil(name, run):
            if name == "coil-test":
                step = next(s for s in run["steps"] if s["label"] == "entry-17-fired")
                step["transitions"]["solenoids"] = []

        # Raw-run digests are pinned, so bypass that guard to reach each claim check.
        with patch.object(builder, "digest", side_effect=lambda p: load_json(builder.SEED)["runs"][p.parent.name]["sha256"] if p.name == "run.json" else original_digest(p)):
            for name, change, message in (("lamp", lamp, "lamp reading"), ("frame", frame, "frame changed"),
                                          ("checkpoint", checkpoint, "checkpoint did not fire"),
                                          ("level", level, "public level"), ("coil", coil, "coil reading")):
                with self.subTest(name=name):
                    with patch.object(builder, "read_json", mutated(change)):
                        with self.assertRaisesRegex(ValueError, message):
                            builder.build(review)


if __name__ == "__main__":
    unittest.main()
