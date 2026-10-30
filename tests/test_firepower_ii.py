from __future__ import annotations

import copy
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_against_schema, validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_firepower_ii as curator


def tempdir():
    return tempfile.TemporaryDirectory(dir=os.environ.get("PINMAME_TEST_TMP_ROOT"))


class FirepowerIICurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = curator.build()
        cls.switches = {d["binding"]["device"]: d for d in cls.game["inputs"] if d["binding"]["group"] == "pinmame.input.switch"}
        cls.coils = {d["binding"]["device"]: d for d in cls.game["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {d["binding"]["device"]: d for d in cls.game["outputs"] if d["binding"]["group"] == "pinmame.output.lamp"}

    def test_identity_and_conversion_are_not_collapsed(self):
        identity = {k:v for k,v in self.game["machine"].items() if k != "playfield"}
        self.assertEqual(identity, {"id": "williams.firepower-ii.1983", "name": "Firepower II", "manufacturer": "Williams", "year": 1983,
                         "model_number": "521", "kind": "physical_pinball", "ipdb_id": 857, "opdb_id": "GRWYk-Mb5OV"})
        drivers = {d["id"]: d for d in self.game["drivers"]}
        self.assertEqual(set(drivers), {"fpwr2_l2"})
        self.assertEqual(drivers["fpwr2_l2"]["physical_compatibility"], "identical")
        converted = curator.conversion()
        self.assertEqual(converted["machine"], {"id": "unknown-manufacturer.wild-texas", "name": "Wild Texas",
                         "manufacturer": "Unknown Manufacturer", "year": None, "kind": "physical_conversion", "ipdb_id": 5500})
        self.assertEqual([d["id"] for d in converted["drivers"]], ["wldtexas"])
        self.assertEqual(converted["drivers"][0]["clone_of"], "fpwr2_l2")
        self.assertNotIn("opdb_id", converted["machine"])
        self.assertEqual(validate_machine(converted, ROOT), [])
        self.assertEqual(validate_against_schema(converted, ROOT / "schemas/machine.schema.json", "conversion"), [])
        catalog = load_json(ROOT / "catalog/pinmame.json")
        claims = [m for m in catalog["machines"] if m["id"] == curator.MACHINE_ID]
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0]["driver_count"], 1)
        self.assertEqual({d["id"] for d in catalog["drivers"] if d["machine_id"] == curator.MACHINE_ID}, set(drivers))
        self.assertEqual([d["machine_id"] for d in catalog["drivers"] if d["id"] == "wldtexas"], [curator.CONVERSION_ID])
        claim_paths = [p for p in (ROOT/"machines").glob("**/*.json")
                       if any(d["id"] == "wldtexas" for d in load_json(p).get("drivers", []))]
        self.assertEqual(claim_paths, [ROOT/curator.CONVERSION])
        stale = list((ROOT / "machines/stubs").glob("**/*fpwr2*"))
        self.assertEqual(stale, [])

    def test_complete_legal_transport_dispositions(self):
        self.assertEqual(set(self.switches), {*range(-7, -2), *range(1, 65), *range(81, 89)})
        self.assertEqual(set(self.coils), {*range(1, 26), *range(45, 49), *range(51, 61)})
        self.assertEqual(set(self.lamps), set(range(1, 97)))
        dips = {d["binding"]["device"] for d in self.game["inputs"] if d["binding"]["group"] == "pinmame.input.dip"}
        self.assertEqual(dips, {1, 2, *range(9, 25)})
        report = curator.spatial_report(self.game)
        self.assertEqual(report["transport_holes"]["solenoid"], [*range(26, 45), 49, 50])
        self.assertEqual(self.game["controller"]["hardware_generation"], "0x10000")

    def test_meaningful_switch_labels_and_connector_order(self):
        for address, label in {9: "Outhole", 10: "Right Ball Ramp", 11: "Left Ball Ramp", 12: "Ball Shooter Trough", 13: "Lane Change",
                               18: "Spinner", 23: "Eject Hole", 24: "Release Target", 33: "R Target (last)", 38: "Left Outlane",
                               39: "Right Outlane", 40: "Orbit Out Gate", 49: "Playfield Tilt"}.items():
            self.assertEqual(self.switches[address]["label"], label)
        self.assertEqual(self.switches[41]["wiring"]["drive_connection"], "2J2-3")
        self.assertEqual(self.switches[48]["wiring"]["return_connection"], "2J3-1")
        self.assertEqual(self.switches[1]["wiring"]["return_wire"], "WHT-BRN")
        self.assertEqual(self.switches[21]["availability"], "unused")
        for address in range(50, 65):
            self.assertEqual(self.switches[address]["availability"], "unused")
        aliases = {a["value"] for a in self.switches[9]["aliases"] if a["namespace"] == "pinmame.switch"}
        self.assertEqual(aliases, {"9", "09", "009"})

    def test_flipper_copy_and_used_virtual_states(self):
        lane = self.switches[13]
        self.assertEqual(lane["kind"], "virtual")
        self.assertEqual(lane["spatial"]["reason"], "virtual")
        self.assertIn("overwrites direct writes", lane["physical"]["notes"])
        for address in [82, 84]:
            self.assertEqual(self.switches[address]["availability"], "used")
        for address in [81, 83, 85, 86, 87, 88]:
            self.assertEqual(self.switches[address]["availability"], "unused")
        for address in range(45, 49):
            self.assertEqual((self.coils[address]["kind"], self.coils[address]["availability"]), ("virtual", "used"))
        self.assertEqual(self.coils[25]["id"], "relay.game-on-flipper-enable")
        self.assertEqual(self.coils[23]["availability"], "unused")

    def test_manual_solenoids_are_physical_classes(self):
        self.assertEqual((self.coils[4]["kind"], self.coils[4]["physical"]["part_number"]), ("flasher", "Type 83"))
        self.assertEqual(self.coils[11]["kind"], "relay")
        self.assertEqual(self.coils[15]["physical"]["part_number"], "SM-29-1000-DC")
        self.assertEqual(self.coils[16]["physical"]["quantity"], 2)
        expected = {17: "Left Kicker", 18: "Right Kicker", 19: "Lower Left Jet Bumper", 20: "Upper Right Jet Bumper", 21: "Upper Left Jet Bumper", 22: "Lower Right Jet Bumper"}
        self.assertEqual({n:self.coils[n]["label"] for n in expected}, expected)
        self.assertEqual(self.coils[21]["wiring"]["drive_connection"], "2P12-8, 8P3-12")
        self.assertIn("8P3-21", self.coils[21]["physical"]["notes"])
        self.assertNotIn("quantity", self.coils[4]["physical"])
        self.assertFalse(any(d["binding"]["group"] == "pinmame.output.gi" for d in self.game["outputs"]))
        self.assertFalse(any("sPlumbTilt" in d["label"] for d in self.game["outputs"]))

    def test_lamps_preserve_backbox_and_unresolved_fitment(self):
        self.assertEqual(self.lamps[6]["label"], "Shoot Again (playfield)")
        self.assertEqual(self.lamps[40]["label"], "Ball in Play")
        self.assertEqual(self.lamps[40]["kind"], "lamp")
        self.assertEqual(self.lamps[40]["availability"], "unknown")
        self.assertEqual(self.lamps[40]["spatial"]["reason"], "cabinet_or_service")
        self.assertEqual(self.lamps[6]["provenance"]["status"], "conflicted")
        self.assertEqual(self.lamps[40]["provenance"]["status"], "conflicted")
        self.assertTrue({curator.MANUAL, curator.INSERT, "photo.firepower-ii-50038"} <= set(self.lamps[6]["provenance"]["source_refs"]))
        self.assertEqual(self.game["conflicts"][0]["path"], "outputs")
        self.assertIn("public 6", self.lamps[40]["physical"]["notes"])
        self.assertIn("shared backbox load", self.lamps[6]["physical"]["notes"])
        self.assertEqual([c["id"] for c in self.game["conflicts"]], ["lamp6-40-insert-routing"])
        self.assertIn("Resolution path:", self.game["conflicts"][0]["description"])
        self.assertEqual(self.lamps[8]["label"], "Bonus Holdover (orbit)")
        self.assertEqual(self.lamps[23]["label"], "Bonus Holdover (bonus)")
        for n in range(1, 6):
            self.assertEqual(self.lamps[n]["spatial"]["reason"], "cabinet_or_service")
        for n in range(61, 97):
            self.assertEqual(self.lamps[n]["availability"], "unused")
        self.assertEqual(self.lamps[57]["wiring"]["drive_connection"], "2J5-2")
        self.assertEqual(self.lamps[63]["wiring"]["return_connection"], "2J7-9")

    def test_mechanism_causality_and_display_topology(self):
        mechanisms = {m["id"]:m for m in self.game["mechanisms"]}
        self.assertEqual(mechanisms["mech.eject-lock"]["actuators"], ["coil.eject-hole"])
        self.assertEqual(mechanisms["mech.eject-lock"]["sensors"], ["switch.eject-hole", "switch.release-target"])
        self.assertEqual(mechanisms["mech.orbit"]["actuators"], [])
        self.assertFalse(any(m["kind"] == "drop_target_bank" for m in mechanisms.values()))
        relationships = {(r["source"],r["destination"]) for r in self.game["relationships"]}
        self.assertIn(("switch.left-kicker", "coil.left-kicker"), relationships)
        self.assertNotIn(("coil.outhole", "switch.left-ball-ramp"), relationships)
        self.assertEqual([(d["controller_index"], d["segment_start"], d["width"]) for d in self.game["displays"]],
                         [(2,1,7),(3,9,7),(0,21,7),(1,29,7),(4,0,1),(5,8,1),(6,20,1),(7,28,1)])
        self.assertTrue(all(d["spatial"]["reason"] == "cabinet_or_service" for d in self.game["displays"]))

    def test_excerpts_and_schema(self):
        curator.verify_files()
        self.assertEqual(validate_against_schema(self.game, ROOT / "schemas/machine.schema.json", "game"), [])
        self.assertEqual(validate_machine(self.game, ROOT), [])
        evidence = load_json(ROOT / curator.RUNTIME)
        self.assertEqual(validate_against_schema(evidence, ROOT / "schemas/evidence.schema.json", "runtime"), [])
        manual = next(s for s in self.game["sources"] if s["id"] == curator.MANUAL)
        self.assertEqual(manual["revision"], "16-521-101 July 1983")
        self.assertEqual(len(manual["excerpts"]), 10)
        self.assertEqual(manual["acquired_at"], "2026-10-29T23:57:07Z")
        self.assertIn("Copyright", manual["rights"])
        for e in manual["excerpts"]:
            self.assertTrue(e["reviewed"])
            self.assertEqual(e["method"], "manual")
        scripts = [s for s in self.game["sources"] if s["kind"] == "vpx_script"]
        self.assertTrue(all(s["known_working"] is False for s in scripts))

    def test_cpu_bom_does_not_override_the_drawn_electrical_topology(self):
        dips = {d["binding"]["device"]:d for d in self.game["inputs"] if d["binding"]["group"] == "pinmame.input.dip"}
        for n in [1,2]:
            self.assertEqual((dips[n]["kind"], dips[n]["availability"]), ("dip_switch", "used"))
        for n in range(9,25):
            self.assertEqual((dips[n]["kind"], dips[n]["availability"]), ("virtual", "optional"))
            self.assertIn("IC34", dips[n]["physical"]["notes"])
            self.assertIn("photo.firepower-ii-50056", dips[n]["provenance"]["source_refs"])
            self.assertEqual(dips[n]["spatial"]["reason"], "dip_switch")
        photo = next(s for s in self.game["sources"] if s["id"] == "photo.firepower-ii-50056")
        self.assertEqual(photo["uri"], "https://www.ipdb.org/images/857/image-6.jpg")
        self.assertEqual(photo["sha256"], "28adfc5d7fb28b4cce0c4c37fb7d54163877000d11d078ccd29da5dedd69b352")
        self.assertEqual(photo["acquired_at"], "2026-10-30T07:36:19.702475+00:00")
        self.assertIn("https://www.ipdb.org/showpic.pl?id=857&picno=50056", photo["locator"])
        self.assertEqual((self.switches[-3]["kind"], self.switches[-3]["availability"]), ("virtual", "optional"))
        bom = (ROOT/"evidence/excerpts/williams.firepower-ii.1983/cpu-board.md").read_text()
        self.assertIn("74154 4 TO 16 DECODER", bom)
        self.assertIn("R23, R26 | RESISTOR FC 33K", bom)
        self.assertIn("W14, W17, [blank], W20", bom)
        self.assertIn("5341-09233-00", bom)
        self.assertIn("5341-09234-00", bom)
        self.assertIn("8T97 HEX TRISTATE BUFFER", bom)
        self.assertNotIn("BT97 HEX", bom)
        for number in range(1,66):
            self.assertEqual(sum(line.startswith(f"| {number} |") for line in bom.splitlines()), 1)
        for literal in ["DS1, DS2", "5043-08980-00", "5040-08986-00", "5041-09031-00", "5700-09004-00", "1502-1"]:
            self.assertIn(literal, bom)

    def test_only_concrete_remaining_requirements_block_promotion(self):
        self.assertEqual(self.game["coverage"]["missing"], ["output_enumeration", "output_semantics", "spatial_placement", "unresolved_conflicts"])
        self.assertNotIn("Opus", curator.KNOWLEDGE_TEXT)
        self.assertNotIn("review", curator.CONVERSION_TEXT)
        self.assertIn("stock GI socket inventory", curator.KNOWLEDGE_TEXT)
        self.assertIn("owner/technician", curator.KNOWLEDGE_TEXT)
        tilt = load_json(ROOT/curator.TILT)
        self.assertEqual(validate_against_schema(tilt, ROOT/"schemas/evidence.schema.json", "tilt"), [])

    def test_partial_gate_and_every_nonspatial_disposition(self):
        self.assertEqual(self.game["coverage"]["status"], "partial")
        self.assertEqual(self.game["coverage"]["missing"], curator.MISSING)
        report = curator.spatial_report(self.game)
        self.assertEqual(report["format"], "pinmame-spatial-blockers")
        self.assertEqual(report["counts"], {"lamp": 54, "solenoid": 9, "switch": 36})
        for group in ["inputs", "outputs"]:
            for d in self.game[group]:
                if d["availability"] == "unused" or d["kind"] in {"virtual", "dip_switch"} or d.get("roles") in [["cabinet"], ["service"], ["backbox"], ["internal"]]:
                    self.assertEqual(d["spatial"]["status"], "not_applicable", d["id"])
                else:
                    self.assertTrue(d["id"] in report["unplaced_devices"] or d.get("spatial", {}).get("placements"), d["id"])
        promoted = copy.deepcopy(self.game)
        promoted["coverage"]["status"] = "author_ready"
        promoted["coverage"]["missing"] = []
        errors = validate_machine(promoted, ROOT)
        self.assertTrue(any("conflict" in e for e in errors))
        self.assertTrue(any("spatial" in e for e in errors))

    def _fixture(self, destination):
        files = [*curator.expected_artifacts(), curator.RUNTIME, curator.TILT, curator.RETAINED]
        files.extend([curator.spatial.SEED, curator.spatial.EXCERPT])
        files.extend(Path("evidence/excerpts") / curator.MACHINE_ID / n for n in curator.EXCERPTS)
        files.extend(Path("evidence/excerpts") / curator.MACHINE_ID / spec[0] for spec in curator.IMAGES.values())
        files.extend(Path(r["scenario_path"]) for relative in [curator.RUNTIME, curator.TILT]
                     for r in load_json(ROOT / relative)["runtime"]["raw_runs"])
        for rel in files:
            (destination / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, destination / rel)

    def test_determinism_and_all_local_guards_fail(self):
        curator.check()
        self.assertEqual((ROOT / curator.SEED).read_bytes(), (ROOT / curator.DEFINITION).read_bytes())
        with tempdir() as t:
            root = Path(t)
            self._fixture(root)
            before = curator.expected_artifacts(root)
            curator.regenerate(root)
            curator.regenerate(root)
            curator.check(root)
            self.assertEqual(before, curator.expected_artifacts(root))
            for rel in [curator.SEED, curator.KNOWLEDGE, curator.REPORT, curator.REPORT_MD,
                        curator.CONVERSION, curator.CONVERSION_SEED, curator.CONVERSION_KNOWLEDGE]:
                original = (root/rel).read_bytes()
                (root/rel).write_bytes(original+b"drift")
                with self.assertRaisesRegex(RuntimeError, "drift"):
                    curator.check(root)
                (root/rel).write_bytes(original)
            guarded = [curator.RUNTIME, curator.TILT, curator.RETAINED]
            guarded += [curator.spatial.SEED, curator.spatial.EXCERPT]
            guarded += [Path("evidence/excerpts")/curator.MACHINE_ID/n for n in curator.EXCERPTS]
            guarded += [Path("evidence/excerpts")/curator.MACHINE_ID/spec[0] for spec in curator.IMAGES.values()]
            guarded += [Path(r["scenario_path"]) for relative in [curator.RUNTIME, curator.TILT]
                        for r in load_json(ROOT/relative)["runtime"]["raw_runs"]]
            for rel in guarded:
                original = (root/rel).read_bytes()
                (root/rel).write_bytes(original+b"changed")
                with self.assertRaises(RuntimeError):
                    curator.check(root)
                (root/rel).write_bytes(original)
            promoted = copy.deepcopy(self.game)
            promoted["coverage"]["status"] = "author_ready"
            (root/curator.DEFINITION).write_bytes(canonical_bytes(promoted))
            with self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.regenerate(root)
            (root/curator.DEFINITION).write_bytes(canonical_bytes(self.game))
            stale = root/"machines/author-ready/williams/firepower-ii-1983.json"
            stale.parent.mkdir(parents=True)
            stale.write_text("{}")
            with self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.check(root)

    def test_missing_configured_external_root_fails(self):
        for name in ["PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_SOURCE_ROOT", "PINMAME_VPX_SCRIPTS_ROOT", "PINMAME_ROM_LIBRARY_ROOT"]:
            with self.subTest(root=name), patch.dict(os.environ, {name:""}, clear=True):
                with self.assertRaisesRegex(RuntimeError, "configured evidence root unavailable"):
                    curator.verify_external()

    def test_missing_local_evidence_is_refused(self):
        with tempdir() as t:
            root = Path(t)
            self._fixture(root)
            (root/curator.RUNTIME).unlink()
            with self.assertRaisesRegex(RuntimeError, "runtime evidence absent"):
                curator.check(root)

    def test_external_hash_guards_reject_changed_or_missing_files(self):
        for variable, files in [("PINMAME_SOURCE_ROOT", curator.SOURCE_FILES),
                                ("PINMAME_VPX_SCRIPTS_ROOT", curator.SCRIPT_FILES)]:
            with self.subTest(variable=variable), tempdir() as t:
                directory = Path(t)
                for name in files:
                    p = directory/name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(b"wrong artifact")
                with patch.dict(os.environ, {variable:t}, clear=True):
                    with self.assertRaisesRegex(RuntimeError, "absent or changed"):
                        curator.verify_external()
        with tempdir() as t:
            with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT":t}, clear=True):
                with self.assertRaisesRegex(RuntimeError, "manual/capture absent"):
                    curator.verify_external()
            with patch.dict(os.environ, {"PINMAME_ROM_LIBRARY_ROOT":t}, clear=True):
                with self.assertRaisesRegex(RuntimeError, "ROM archive absent"):
                    curator.verify_external()


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained runtime root not configured")
class FirepowerIIRuntimeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.SESSION / "harness"
        cls.runs = {n:load_json(cls.directory/f"{n}.json") for n in ["init","sol","sw","sw-slow","play"]}

    @staticmethod
    def _text(snapshot, indexes):
        glyph = {63:"0",6:"1",91:"2",79:"3",102:"4",109:"5",125:"6",7:"7",127:"8",111:"9",0:" "}
        displays = {d["index"]:d for d in snapshot["displays"]}
        return "".join("".join(glyph[v & 127] for v in displays[i]["segments"]) for i in indexes)

    def _configured(self, variable):
        # Skips the enclosing subTest, or the whole test when called outside one.
        value = os.environ.get(variable)
        if not value:
            self.skipTest(f"{variable} not configured")
        return Path(value)

    def test_exact_retained_evidence(self):
        curator.verify_external()

    def test_rom_service_selectors_are_recomputed(self):
        run = self.runs["sol"]
        snaps = {s["label"]:s for s in run["snapshots"]}
        seen = set()
        for step in run["steps"]:
            if step["label"] == "hold selected solenoid" or step["label"].startswith("next solenoid selector"):
                number = int(self._text(snaps[step["label"]], [4,5]))
                changes = {v["number"]:v["states"] for v in step["transitions"]["solenoids"]}
                self.assertIn(number, changes)
                self.assertIn(0 if number == 16 else 1, changes[number])
                seen.add(number)
        self.assertEqual(seen, set(range(1,26)))

    def test_switch_test_uses_rom_display_and_a_copied_button_control(self):
        run = self.runs["sw-slow"]
        snaps = {s["label"]:s for s in run["snapshots"]}
        for n in range(1,65):
            self.assertEqual(self._text(snaps[f"matrix {n} (held)"], [4,5]), f"{n:02}" if n <= 49 else "  ")
        self.assertEqual(self._text(snaps["flipper column 82 held"], [4,5]), "13")
        # 13 in a repeated pulse is not overwrite proof. Use the one-shot gameplay
        # write and compare with the button-caused ROM display above.
        game = {s["label"]:s for s in self.runs["play"]["snapshots"]}
        copy_state = {s["number"]:s["state"] for s in game["one write to matrix lane change is overwritten"]["watched_switches"]}
        self.assertEqual(copy_state[13], 0)

    def test_gameplay_causality_and_release_with_ball_present(self):
        run = self.runs["play"]
        steps = {s["label"]:s for s in run["steps"]}
        for label, output in [("start game",2),("special scoring switch 41",19),("special scoring switch 42",20),
                              ("special scoring switch 43",21),("special scoring switch 44",22),("special scoring switch 47",17),
                              ("special scoring switch 48",18),("ball held in eject hole",2),("release target",3),
                              ("ball rests in outhole",1),("orbit completion",4)]:
            changes = {v["number"]:v["states"] for v in steps[label]["transitions"]["solenoids"]}
            self.assertIn(1, changes[output])
        snap = next(s for s in run["snapshots"] if s["label"] == "release target")
        self.assertEqual(next(v["state"] for v in snap["watched_switches"] if v["number"] == 23), 1)
        tilt = {v["number"]:v["states"] for v in steps["plumb tilt warning three"]["transitions"]["solenoids"]}
        self.assertIn(0, tilt[25])
        start_lamps = {v["number"]:v["states"] for v in steps["start game"]["transitions"]["lamps"]}
        tilt_lamps = {v["number"]:v["states"] for v in steps["plumb tilt warning three"]["transitions"]["lamps"]}
        self.assertIn(1, start_lamps[40])
        self.assertIn(0, tilt_lamps[40])

    def test_script_tilt7_really_has_slam_behavior(self):
        folder = self.directory.parent/"tilt-probes"
        evidence = load_json(ROOT/curator.TILT)
        for address in [1,7,49]:
            raw = load_json(folder/f"tilt-{address}.json")
            steps = {s["label"]:s["transitions"] for s in raw["steps"]}
            for n in [1,2,3]:
                label=f"tilt {address} closure {n}"
                derived=next(v for v in evidence["runtime"]["observations"]["runs"][f"tilt-{address}"]["named_action_observations"] if v["label"] == label)
                coils=[v for v in steps[label]["solenoids"] if v["number"] in {11,25}]
                self.assertEqual(derived["active_solenoid_addresses"], [v["number"] for v in coils if 1 in v["states"]])
                self.assertEqual(derived["transitioned_solenoid_addresses"], [v["number"] for v in coils])
                self.assertEqual(derived["observed_switch_addresses"], [])
            first={v["number"]:v["states"] for v in steps[f"tilt {address} closure 1"]["solenoids"]}
            if address == 1:
                self.assertEqual(first[11], [1,0])
                self.assertNotIn(25, first)
                third={v["number"]:v["states"] for v in steps["tilt 1 closure 3"]["solenoids"]}
                self.assertEqual(third[25], [0])
            else:
                self.assertEqual(first[25], [0])
            if address == 7:
                self.assertTrue(any(v["number"]==1 and set(v["states"])=={0,1} for v in steps["tilt 7 closure 1"]["lamps"]))
            if address == 49:
                lamps={v["number"]:v["states"] for v in steps["tilt 49 closure 1"]["lamps"]}
                self.assertEqual(lamps[3], [1])
        core = (self.directory.parent/"installed-vbs/core.vbs").read_text()
        s7 = (self.directory.parent/"installed-vbs/s7.vbs").read_text()
        self.assertIn("vpmTimer.PulseSw TiltSwitch", core)
        self.assertIn("Case keyBangBack     vpmNudge.DoMechTilt", s7)
        with self.subTest(root="PINMAME_VPX_SCRIPTS_ROOT"):
            script = (self._configured("PINMAME_VPX_SCRIPTS_ROOT")/"FirePower II (Williams 1983) 1.1.vbs").read_text()
            self.assertIn("vpmNudge.TiltSwitch = 7", script)
            self.assertIn("If vpmKeyDown(KeyCode) Then Exit Sub", script)

    def test_every_retained_physical_input_hash_is_guarded(self):
        source = self._configured("PINMAME_MANUALS_ROOT")/"by-machine"/curator.MACHINE_ID
        specs = curator.retained_inputs()["files"]
        with tempdir() as t:
            target=Path(t)/"by-machine"/curator.MACHINE_ID
            for spec in specs:
                p=target/spec["path"];p.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source/spec["path"],p)
            with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT":t}, clear=True):
                curator.verify_external()
                for spec in specs:
                    p=target/spec["path"];original=p.read_bytes()
                    with self.subTest(path=spec["path"]):
                        p.write_bytes(original+b"changed")
                        with self.assertRaisesRegex(RuntimeError,"manual/capture absent or changed"):
                            curator.verify_external()
                        p.write_bytes(original)

    def test_every_raw_manifest_and_installed_library_guard(self):
        source=Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
        with tempdir() as t:
            target=Path(t)
            for name in ["harness", "tilt-probes", "installed-vbs"]:
                shutil.copytree(source/curator.SESSION/name,target/curator.SESSION/name)
            snapshot=Path("opdb-import/latest-opdb.json")
            (target/snapshot).parent.mkdir(parents=True)
            shutil.copyfile(source/snapshot,target/snapshot)
            guarded=[snapshot,*(curator.SESSION/"installed-vbs"/name for name in curator.VBS_FILES)]
            spatial_seed = curator.spatial.read_seed(ROOT)
            for spec in [spatial_seed["world_obj"], *(p["external_crop"] for p in spatial_seed["pages"].values()), *spatial_seed["correction_crops"]]:
                relative = curator.spatial.SESSION/spec["path"]
                (target/relative).parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source/relative,target/relative)
                guarded.append(relative)
            for relative,folder in [(curator.RUNTIME,"harness"),(curator.TILT,"tilt-probes")]:
                guarded += [curator.SESSION/folder/(r["name"]+".json") for r in load_json(ROOT/relative)["runtime"]["raw_runs"]]
                guarded += [curator.SESSION/folder/name for name in ["manifest.json","manifest.sha256"]]
            guarded += [curator.SESSION/"harness/init-state/nvram/fpwr2_l2.nv"]
            with patch.dict(os.environ,{"PINMAME_REVIEW_ARTIFACTS_ROOT":t},clear=True):
                curator.verify_external()
                for rel in guarded:
                    p=target/rel;original=p.read_bytes()
                    with self.subTest(path=str(rel)):
                        p.write_bytes(original+b"changed")
                        with self.assertRaises((RuntimeError,ValueError)):
                            curator.verify_external()
                        p.write_bytes(original)

    def test_each_pinned_code_file_and_rom_member_guard(self):
        for variable, specs in [("PINMAME_SOURCE_ROOT",curator.SOURCE_FILES), ("PINMAME_VPX_SCRIPTS_ROOT",curator.SCRIPT_FILES)]:
            with self.subTest(root=variable):
                source=self._configured(variable)
                with tempdir() as t:
                    target=Path(t)
                    for name in specs:
                        p=target/name;p.parent.mkdir(parents=True,exist_ok=True)
                        shutil.copyfile(source/name,p)
                    with patch.dict(os.environ,{variable:t},clear=True):
                        curator.verify_external()
                        for name in specs:
                            p=target/name;original=p.read_bytes()
                            with self.subTest(file=name):
                                p.write_bytes(original+b"changed")
                                with self.assertRaisesRegex(RuntimeError,"absent or changed"):
                                    curator.verify_external()
                                p.write_bytes(original)
        with self.subTest(root="PINMAME_ROM_LIBRARY_ROOT"):
            source=self._configured("PINMAME_ROM_LIBRARY_ROOT")
            with tempdir() as t:
                p=Path(t)/"fpwr2_l2.zip";shutil.copyfile(source/p.name,p)
                with patch.dict(os.environ,{"PINMAME_ROM_LIBRARY_ROOT":t},clear=True):
                    curator.verify_external()
                    for name,(size,digest) in curator.ROM_MEMBERS.copy().items():
                        with self.subTest(member=name), patch.dict(curator.ROM_MEMBERS,{name:(size,"0"*40)}):
                            with self.assertRaisesRegex(RuntimeError,"ROM members differ"):
                                curator.verify_external()
                    with p.open("ab") as stream:
                        stream.write(b"changed")
                    with self.assertRaisesRegex(RuntimeError,"ROM archive absent or changed"):
                        curator.verify_external()


if __name__ == "__main__":
    unittest.main()
