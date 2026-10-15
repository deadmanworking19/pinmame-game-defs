"""Seawitch's independent semantic, provenance, runtime and promotion gates."""
from __future__ import annotations

import copy
import io
import os
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import validate_machine
from pinmame_game_defs.conflicts import unresolved_conflicts
import curate_seawitch as curator
import seawitch_data as data

MACHINE_ID = "stern.seawitch.1980"
DRIVERS = {"seawitch", "seawitfp", "seawitcha", "seawitchb", "seawitchc", "seawitchd", "seawitche", "seawitchf"}
MATRIX = set(range(1, 41))
LAMPS = set(range(1, 64)) - {16, 32, 48}
SOLENOIDS = set(range(1, 16)) | set(range(17, 21)) | {45, 46, 47, 48}
EVIDENCE_NAMES = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")


class SeawitchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(ROOT / curator.DEFINITION)
        cls.inputs = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.switch"}
        cls.dips = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.dip"}
        cls.direct = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "physical.input.direct"}
        cls.solenoids = {i["binding"]["device"]: i for i in cls.definition["outputs"] if i["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {i["binding"]["device"]: i for i in cls.definition["outputs"] if i["binding"]["group"] == "pinmame.output.lamp"}
        cls.runtime = load_json(ROOT / curator.RUNTIME)
        cls.sources = {s["id"]: s for s in cls.definition["sources"]}

    def test_identity_variants_catalog_and_stale_stubs(self):
        m = self.definition["machine"]
        self.assertEqual((MACHINE_ID, "Seawitch", "Stern", 1980, "123", 2089, "GR6kB-MDz81"),
                         (m["id"], m["name"], m["manufacturer"], m["year"], m["model_number"], m["ipdb_id"], m["opdb_id"]))
        self.assertEqual(DRIVERS, {d["id"] for d in self.definition["drivers"]})
        self.assertTrue(all(d["physical_compatibility"] == "identical" and "display_overrides" not in d for d in self.definition["drivers"]))
        for d in self.definition["drivers"]:
            self.assertEqual(None if d["id"] == "seawitch" else "seawitch", d.get("clone_of"))
        catalog = load_json(ROOT / "catalog/pinmame.json")
        self.assertEqual(DRIVERS, {d["id"] for d in catalog["drivers"] if d.get("machine_id") == MACHINE_ID})
        for path in (ROOT / "machines/stubs").rglob("*.json"):
            self.assertFalse(DRIVERS & {d["id"] for d in load_json(path)["drivers"]}, path)

    def test_full_controller_and_physical_address_dispositions(self):
        self.assertEqual(MATRIX | {-7, -6, -5, 81, 82, 83, 84}, set(self.inputs))
        self.assertEqual(set(range(1, 33)), set(self.dips))
        self.assertEqual({1, 2, 3}, set(self.direct))
        self.assertEqual(SOLENOIDS, set(self.solenoids))
        self.assertEqual(LAMPS, set(self.lamps))
        self.assertEqual({11, 15, 16, 26, 27, 28}, {a for a in MATRIX if self.inputs[a]["availability"] == "unused"})
        self.assertEqual({5, 13}, {a for a, d in self.dips.items() if d["availability"] == "unused"})
        self.assertEqual({81, 83}, {a for a in (81, 82, 83, 84) if self.inputs[a]["availability"] == "unused"})
        self.assertTrue(all(self.inputs[a]["kind"] == "switch" for a in MATRIX | {81, 82, 83, 84}))
        for a in MATRIX - {11, 15, 16, 26, 27, 28}:
            self.assertFalse(self.inputs[a]["normally_closed"], a)
        for a in (1, 2):
            self.assertTrue(self.direct[a]["normally_closed"])
            self.assertEqual(2, self.direct[a]["physical"]["quantity"])
        self.assertFalse(self.direct[3]["normally_closed"])
        self.assertEqual("A4J3-5", self.direct[3]["wiring"]["control_connection"])
        self.assertEqual("virtual", self.inputs[-5]["kind"])
        self.assertEqual("used", self.inputs[-5]["availability"])
        self.assertIn("st300_switch_w", self.inputs[-5]["physical"]["notes"])

    def test_game_specific_switches_and_wiring(self):
        expected = {4: "Top roll-over button", 5: "Spinning target", 9: "Top thumper", 10: "Left thumper", 14: "Right thumper", 17: "Stand-up target top right", 25: "Runway roll-over button", 33: "Out-hole", 38: "Left bank target 1", 40: "Left bank target 3"}
        for a, label in expected.items():
            self.assertEqual(label, self.inputs[a]["label"])
        self.assertIn("pulses 42", self.inputs[13]["physical"]["notes"])
        self.assertEqual("A4J2-2", self.inputs[13]["wiring"]["control_connection"])
        self.assertEqual("A4J2-12", self.inputs[13]["wiring"]["return_connection"])
        self.assertEqual("A4J3-2", self.inputs[2]["wiring"]["control_connection"])
        self.assertEqual("BRN-W", self.inputs[2]["wiring"]["return_wire"])
        self.assertTrue(self.inputs[33]["initial_active"])
        self.assertNotIn("spatial", self.inputs[8])
        self.assertNotIn("quantity", self.inputs[8]["physical"])
        for a, values in ((7, {"7", "07", "007"}), (13, {"13", "013"})):
            self.assertEqual(values, {v["value"] for v in self.inputs[a]["aliases"] if v["namespace"] == "vpe-legacy.switch"})

    def test_sdu_translation_fitment_and_legacy_provider_aliases(self):
        expected_q = {1:2, 2:1, 3:5, 4:6, 5:7, 6:3, 7:4, 8:8, 9:13, 10:14, 11:9, 12:10, 13:12, 14:11, 15:16, 17:17, 18:19, 19:15, 20:18}
        for a, q in expected_q.items():
            self.assertEqual(f"Q{q}", self.solenoids[a]["wiring"]["driver_transistor"])
            self.assertIn({"namespace": "manual.self-test", "value": str(q)}, self.solenoids[a]["aliases"])
        self.assertEqual({3,12,13,14,15,17,20}, {a for a,i in self.solenoids.items() if i["availability"] == "unused"})
        self.assertTrue(all(self.solenoids[a]["kind"] == "coil" for a in (3,12,13,14,15,17,20)))
        self.assertEqual("Right thumper", self.solenoids[11]["label"])
        self.assertEqual("A3J1-5", self.solenoids[7]["wiring"]["drive_connection"])
        self.assertEqual("A3J5-12", self.solenoids[9]["wiring"]["drive_connection"])
        self.assertEqual("A3J5-11", self.solenoids[10]["wiring"]["drive_connection"])
        for a in (6,7,8,9,10):
            self.assertIn({"namespace": "pinmame.solenoid", "value": str(a)}, self.solenoids[a]["aliases"])
        self.assertFalse(any(v["namespace"] == "pinmame.coil" for i in self.solenoids.values() for v in i["aliases"]))
        for power, held in ((45,46),(47,48)):
            self.assertEqual("virtual", self.solenoids[power]["kind"])
            self.assertEqual("used", self.solenoids[power]["availability"])
            self.assertEqual(2, self.solenoids[held]["physical"]["quantity"])
            self.assertEqual(2, len(self.solenoids[held]["spatial"]["placements"]))

    def test_lda_crossings_own_lists_and_unknown_fitment(self):
        expected = {24:("Q25","Spinner, 2nd. bottom","A5J1-6"),25:("Q24","Right return","A5J1-5"),42:("Q41","Left special","A5J3-20"),58:("Q46","Middle drop target (last tar.) 10,000","A5J3-18")}
        for a,(q,label,pin) in expected.items():
            self.assertEqual((q,label,pin), (self.lamps[a]["wiring"]["driver_transistor"],self.lamps[a]["label"],self.lamps[a]["wiring"]["drive_connection"]))
        self.assertEqual({29,41,51,57}, {a for a,i in self.lamps.items() if i["availability"] == "unknown"})
        for a in (29,41,51,57):
            self.assertNotIn("part_number", self.lamps[a]["physical"])
            self.assertNotIn("quantity", self.lamps[a]["physical"])
            self.assertNotIn("spatial", self.lamps[a])
        shoot = self.lamps[11]
        self.assertEqual("Q3", shoot["wiring"]["driver_transistor"])
        self.assertEqual("A5J2-21; A5J1-26", shoot["wiring"]["drive_connection"])
        self.assertNotIn("quantity", shoot["physical"])
        self.assertNotIn("spatial", shoot)
        self.assertTrue(all(self.lamps[a]["spatial"]["reason"] == "cabinet_or_service" for a in (13,45,61,63)))
        driver = (ROOT/"evidence/excerpts/stern.seawitch.1980/lamp-identification.md").read_text(encoding="utf-8")
        playfield = (ROOT/"evidence/excerpts/stern.seawitch.1980/playfield-lamp-list.md").read_text(encoding="utf-8")
        table_rows = lambda text: [line for line in text.splitlines() if re.match(r"^\| [A-Z0-9].*\| J[123] \| \d+ \|$",line)]
        self.assertEqual((57,52),(len(table_rows(driver)),len(table_rows(playfield))))
        for label in ("GAME OVER","HIGH SCORE TO DATE","MATCH","TILT","SHOOT AGAIN (INSERT)"):
            self.assertTrue(any(line.startswith("| "+label+" |") for line in table_rows(driver)))
            self.assertFalse(any(line.startswith("| "+label+" |") for line in table_rows(playfield)))
        # Read the independent circuit transcription, not the curator's mapping array.
        rows = re.findall(r"^\| U(\d) \| S(\d+) \| R(\d+) \| Q(\d+) \| (\d+) \|$", (ROOT/"evidence/excerpts/stern.seawitch.1980/lamp-circuit.md").read_text(), re.M)
        self.assertEqual(60,len(rows))
        for u,s,r,q,a in rows:
            self.assertEqual(r,q)
            self.assertEqual(16*(int(u)-1)+int(s)+1,int(a))
            self.assertEqual("Q"+q,self.lamps[int(a)]["wiring"]["driver_transistor"])

    def test_displays_and_mechanism_topology(self):
        self.assertEqual([(0,1,7),(1,9,7),(2,17,7),(3,25,7),(4,35,2),(5,38,2)], [(d["controller_index"],d["segment_start"],d["width"])for d in self.definition["displays"]])
        self.assertTrue(all(d["physical_location"] == "cabinet_or_service" for d in self.definition["displays"]))
        mechanisms = {m["id"]:m for m in self.definition["mechanisms"]}
        for name,targets,coil in (("center",[21,22,23,24],7),("left",[38,39,40],8),("top-right",[29,30,31,32],9)):
            m=mechanisms[f"mech.{name}-drop-bank"]
            self.assertEqual([self.inputs[a]["id"]for a in targets],m["sensors"])
            self.assertEqual([self.solenoids[coil]["id"]],m["actuators"])
        outhole=mechanisms["mech.outhole-and-launch"]
        self.assertEqual([self.inputs[33]["id"]],outhole["sensors"])
        self.assertIn("no storage trough",outhole["behavior"].lower())
        self.assertFalse(any(r["source"]==self.solenoids[10]["id"]and r["destination"]==self.inputs[33]["id"]for r in self.definition["relationships"]))
        self.assertEqual([],mechanisms["mech.runway-gate"]["actuators"])
        self.assertEqual([],mechanisms["mech.spinner"]["actuators"])

    def test_spatial_frame_projections_and_no_glow_as_bulbs(self):
        self.assertEqual((956,1979),(self.definition["machine"]["playfield"]["width"],self.definition["machine"]["playfield"]["height"]))
        p=self.inputs[9]["spatial"]["placements"][0]
        self.assertEqual((0.50954,0.193381),(p["x"],p["y"]))
        drain=self.inputs[33]["spatial"]["placements"][0]
        self.assertEqual((round(449.12253/956,6),round(1906.0793/1979,6)),(drain["x"],drain["y"]))
        self.assertEqual((drain["x"],drain["y"]),(self.solenoids[10]["spatial"]["placements"][0]["x"],self.solenoids[10]["spatial"]["placements"][0]["y"]))
        self.assertTrue(all("placements"not in i.get("spatial",{})for i in self.lamps.values()))
        report=load_json(ROOT/curator.REPORT)
        self.assertEqual("pinmame-spatial-blockers",report["format"])
        self.assertTrue(report["lamp_overlay_candidates"])
        self.assertTrue(all(not r["canonical_emitter"]and not r["is_bulb_light"]and not r["show_bulb_mesh"]for r in report["lamp_overlay_candidates"]))
        gi=next(o for o in self.definition["outputs"]if o["kind"]=="gi")
        self.assertEqual({"group":"physical.output.gi","device":1},gi["binding"])
        self.assertNotIn("quantity",gi["physical"])
        self.assertNotIn("spatial",gi)
        self.assertNotIn("A2J3",gi["wiring"]["power_connection"])

    def test_runtime_recomputable_contract_and_no_host_readback_claim(self):
        r=self.runtime["runtime"]
        self.assertEqual("2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591",r["emulator"]["sha256"])
        self.assertEqual("97aa922bf8e4b6970126192ec1ac1fb0305a4f62",r["emulator"]["built_from_revision"])
        self.assertEqual("bbed2206f4b5bb00362f6dc4aa0d5b00b9635af6c1ade127f498f7a066dad88b",r["rom_archive_sha256"])
        obs=r["observations"]["runs"]
        switch=obs["switch-test"]["named_action_observations"]
        self.assertEqual(list(range(1,41)),[x["input_address"]for x in switch])
        for row in switch:
            response=next(d for d in row["display_responses"]if d["display_index"]==0)
            self.assertEqual(row["input_address"],int(response["interpreted_text"]))
            self.assertEqual([],row["observed_switch_addresses"])
        game={x["label"]:x for x in obs["gameplay"]["named_action_observations"]}
        for sw,coil in ((9,1),(10,2),(12,4),(13,5),(14,11)):
            self.assertEqual([coil],game[f"isolated switch {sw}"]["transitioned_solenoid_addresses"])
        for sw,coil in ((24,7),(40,8),(32,9)):
            self.assertIn(coil,game[f"bank target {sw} down"]["transitioned_solenoid_addresses"])
        self.assertEqual([47,48],game["flipper button position 84"]["held_synthetic_solenoid_addresses"])
        self.assertEqual([45,46],game["flipper button position 82"]["held_synthetic_solenoid_addresses"])
        self.assertEqual([],game["flipper button position 83"]["held_synthetic_solenoid_addresses"])
        self.assertEqual([],game["flipper button position 81"]["held_synthetic_solenoid_addresses"])
        self.assertIn(51,r["observations"]["lamp_addresses_driven_outside_self_test"])
        self.assertEqual("unknown",self.lamps[51]["availability"])
        self.assertIn("background",obs["gameplay"]["note"])

    def test_exact_portable_sources_and_partial_gate(self):
        self.assertEqual([],validate_machine(self.definition,ROOT))
        self.assertEqual("partial",self.definition["coverage"]["status"])
        self.assertEqual(["output_semantics","spatial_placement"],self.definition["coverage"]["missing"])
        self.assertEqual([],unresolved_conflicts(self.definition))
        self.assertEqual("03094f08af30bce956e56340acf95f9063ccdd88696d2ddbe6ba2a9c2064b5bb",self.sources[curator.MANUAL]["sha256"])
        self.assertEqual("2db99344ac439fe1a2622e515f40eef4a4af158500f51a9e3770f67fb45b417d",self.sources[curator.SCHEMATIC]["sha256"])
        self.assertEqual("cb91d8d726d8a451ba6f158e49e459812e8dca888b896e72dca69168d616e434",self.sources[curator.TABLE]["sha256"])
        self.assertEqual("a3483e9c4e00c68add7135cd0f3a0dbe216a418d17b9c4f02177da27f1239031",self.sources[curator.SCRIPT]["sha256"])
        curator.verify_portable_evidence(ROOT)
        curator.check(ROOT)
        self.assertEqual((ROOT/curator.DEFINITION).read_bytes(),(ROOT/curator.SEED).read_bytes())
        promoted=copy.deepcopy(self.definition)
        promoted["coverage"]["status"]="author_ready"
        promoted["coverage"]["missing"]=[]
        self.assertTrue(validate_machine(promoted,ROOT))

    def test_guards_fail_for_real_drift_missing_inputs_and_promotion(self):
        original=curator.sha256
        target=ROOT/"evidence/excerpts/stern.seawitch.1980/lamp-identification.md"
        with mock.patch.object(curator,"sha256",side_effect=lambda p:"0"*64 if p==target else original(p)):
            with self.assertRaisesRegex(RuntimeError,"excerpt missing or changed"):
                curator.verify_portable_evidence(ROOT)
        original_file=Path.is_file
        with mock.patch.object(Path,"is_file",lambda p:False if p==target else original_file(p)):
            with self.assertRaisesRegex(RuntimeError,"excerpt missing or changed"):
                curator.verify_portable_evidence(ROOT)
        altered_crops=load_json(ROOT/curator.CROPS)
        altered_crops["lamp-circuit"]["image_derivation"]="unreviewed replacement"
        original_load=curator.load_json
        with mock.patch.object(curator,"load_json",side_effect=lambda p:altered_crops if p==ROOT/curator.CROPS else original_load(p)):
            with self.assertRaisesRegex(RuntimeError,"crop metadata changed"):
                curator.verify_portable_evidence(ROOT)
        with mock.patch.object(data,"SWITCH_LABELS",data.SWITCH_LABELS[:-1]):
            with self.assertRaisesRegex(RuntimeError,"inventory is incomplete"):
                curator.build_definition(ROOT)
        original_exists=Path.exists
        with mock.patch.object(Path,"exists",lambda p:True if p==ROOT/curator.AUTHOR_READY else original_exists(p)),mock.patch.object(Path,"write_bytes",side_effect=AssertionError("must not write")):
            with self.assertRaisesRegex(RuntimeError,"author-ready"):
                curator.generate(ROOT)
            with self.assertRaisesRegex(RuntimeError,"author-ready"):
                curator.check(ROOT)
        original_bytes=Path.read_bytes
        with mock.patch.object(Path,"read_bytes",lambda p:b"drift" if p==ROOT/curator.DEFINITION else original_bytes(p)):
            with self.assertRaisesRegex(RuntimeError,"artifact missing or drifted"):
                curator.check(ROOT)
        env={n:str(ROOT/"missing-evidence-root")for n in EVIDENCE_NAMES}
        with mock.patch.dict(os.environ,env):
            with self.assertRaises((RuntimeError,ValueError,FileNotFoundError)):
                curator.verify_evidence(ROOT)

    def test_profile_transports_and_no_sibling_artifacts(self):
        profile=load_json(ROOT/"controllers/pinmame/stern-mpu200.json")
        self.assertEqual({},next(g for g in profile["groups"]if g["id"]=="physical.output.gi")["transports"])
        catalog=load_json(ROOT/"catalog/pinmame.json")
        foreign_machine_ids={r["machine_id"]for r in catalog["drivers"]if r.get("machine_id") and r["machine_id"]!=MACHINE_ID}
        payload=(ROOT/curator.DEFINITION).read_text(encoding="utf-8")+(ROOT/curator.KNOWLEDGE).read_text(encoding="utf-8")+(ROOT/curator.REPORT).read_text(encoding="utf-8")
        for identifier in foreign_machine_ids:
            self.assertNotIn(identifier,payload)
        # No generated stub or sibling curator is an input to this builder.
        self.assertFalse(any("stub.pinmame"in s["id"]for s in self.definition["sources"]))

    @unittest.skipUnless(all(os.environ.get(n) for n in EVIDENCE_NAMES),"Seawitch retained evidence roots are not configured")
    def test_full_retained_extraction_runtime_native_and_coordinate_evidence(self):
        curator.verify_evidence(ROOT)


try:
    import fitz
    from PIL import Image
    import render_excerpt_image as cropper
except ImportError:
    fitz=None


@unittest.skipIf(fitz is None,"PDF rendering dependencies are not installed")
class TiledSchematicResolutionTests(unittest.TestCase):
    def image_bytes(self,width=400):
        image=Image.new("RGB",(width,200),"white")
        stream=io.BytesIO()
        image.save(stream,format="PNG")
        return stream.getvalue()

    def test_adjacent_strips_use_scan_resolution_not_vector_fallback(self):
        with fitz.open() as document:
            page=document.new_page(width=120,height=180)
            for y in (0,60,120):
                page.insert_image(fitz.Rect(0,y,120,y+60),stream=self.image_bytes())
            result=cropper.analyze(page,page.rect,11)
            self.assertEqual("raster",result.kind)
            self.assertAlmostEqual(240,result.dpi)
            self.assertIn("tiled scan",result.detail)

    def test_duplicate_overlapping_strips_do_not_inflate_coverage(self):
        rectangles=[fitz.Rect(0,0,4,4),fitz.Rect(2,2,6,6),fitz.Rect(0,0,4,4)]
        self.assertEqual(28,cropper._rectangle_union_area(rectangles))
        with fitz.open() as document:
            page=document.new_page(width=120,height=180)
            for _ in range(3):
                page.insert_image(fitz.Rect(0,0,120,40),stream=self.image_bytes())
            self.assertIsNone(cropper._native_raster_dpi(page,page.rect))

    def test_different_resolution_figures_are_not_joined_as_one_scan(self):
        with fitz.open() as document:
            page=document.new_page(width=120,height=180)
            page.insert_image(fitz.Rect(0,0,120,60),stream=self.image_bytes(400))
            page.insert_image(fitz.Rect(0,60,120,120),stream=self.image_bytes(800),keep_proportion=False)
            self.assertIsNone(cropper._native_raster_dpi(page,page.rect))


if __name__=="__main__":
    unittest.main()
