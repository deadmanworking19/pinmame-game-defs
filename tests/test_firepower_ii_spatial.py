from __future__ import annotations

import copy
import difflib
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import curate_firepower_ii as curator
import firepower_ii_spatial as spatial
import drawing_callouts as drawing
from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]


class FirepowerIISpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = curator.build()
        cls.seed, cls.decisions, cls.rows = spatial.geometry(ROOT)
        cls.report = spatial.report(cls.game, ROOT)

    def test_every_fitted_public_device_is_placed_or_has_a_specific_reason(self):
        devices = [d for k in ["inputs", "outputs"] for d in self.game[k]]
        missing = {d["id"] for d in devices if "spatial" not in d}
        self.assertEqual(missing, {"switch.right-ball-ramp", "switch.left-ball-ramp", "switch.playfield-tilt", "flasher.orbit-complete-flash-lamps"})
        self.assertEqual(missing, set(self.report["unplaced_reasons"]))
        self.assertTrue(all(len(v) > 80 for v in self.report["unplaced_reasons"].values()))
        addresses = {g: {r["address"] for r in self.rows if r["group"] == g} for g in ["switch", "solenoid", "lamp"]}
        self.assertEqual(addresses["switch"], {9, 12, *range(14, 21), *range(22, 49)})
        self.assertEqual(addresses["solenoid"], {1, 2, 3, *range(17, 23)})
        self.assertEqual(addresses["lamp"], {*range(6, 40), *range(41, 61)})
        self.assertEqual(self.report["counts"], {g:len(v) for g,v in addresses.items()})
        ids = [p["id"] for d in devices for p in d.get("spatial", {}).get("placements", [])]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), len(self.rows))
        self.assertEqual(validate_machine(self.game, ROOT), [])
        self.assertEqual(self.game["coverage"]["missing"], curator.MISSING)
        self.assertIn("spatial_placement", curator.MISSING)
        self.assertEqual(self.game["coverage"]["status"], "partial")
        self.assertFalse(any(d["binding"]["group"] == "pinmame.output.gi" for d in self.game["outputs"]))

    def test_all_coordinates_and_projection_roles_recompute(self):
        calls, candidates = spatial.callout_seed(self.seed)
        for row in self.rows:
            with self.subTest(row=row["placement_id"]):
                if row["method"] == "drawing_symbol":
                    page = calls["pages"][row["page"]]
                    transform = drawing.fit([(tuple(c["pixel"]),tuple(c["xy"])) for c in page["controls"]])
                    xy = tuple(round(v,3) for v in drawing.apply(transform,row["pixel"]))
                    self.assertEqual(row["status"], "observed")
                    self.assertEqual(row["coordinate_source"], "factory lamp-location symbol")
                else:
                    xy = spatial.normalized(self.seed, spatial.object_point(self.seed,row["object"],row["method"]))
                self.assertEqual((row["x"],row["y"]), xy)
                self.assertTrue(all(0 <= v <= 1 and round(v,6) == v for v in xy))
                if row["extrapolated"] or "projection" in row["classification"]:
                    self.assertEqual(row["status"], "observed")
        lamps = [r for r in self.rows if r["group"] == "lamp"]
        self.assertEqual(sum(r["method"] == "drawing_symbol" for r in lamps), 50)
        for row in lamps:
            if row["method"] != "drawing_symbol":
                self.assertTrue(self.seed["objects"][row["object"]]["fields"]["show_bulb_mesh"])
        self.assertEqual(drawing.evaluate(calls,candidates), self.decisions)
        self.assertEqual(spatial.export_controls(self.seed), self.report["export_geometry_controls"])
        unbound = self.report["unbound_gi_geometry"]
        self.assertEqual(len(unbound["render_light_geometry"]),len(self.seed["unbound_gi"]["lights"]))
        self.assertEqual(len(unbound["model_bulb_geometry"]),len(self.seed["unbound_gi"]["model_bulb_primitives"]))
        for item in [*unbound["render_light_geometry"],*unbound["model_bulb_geometry"]]:
            method = "world_bounds" if "world_bounds_center" in item else "center"
            self.assertEqual(item["normalized_center"],list(spatial.normalized(self.seed,spatial.object_point(self.seed,item["object"],method))))

    def test_lamp_notes_name_each_coordinate_source(self):
        lamps = {d["binding"]["device"]: d for d in self.game["outputs"]
                 if d["binding"]["group"] == "pinmame.output.lamp"}
        rows = [r for r in self.rows if r["group"] == "lamp"]
        self.assertEqual({r["address"] for r in rows if r["classification"] == "bulb_mesh"}, {41, 42, 43, 44})
        self.assertEqual(sum(r["method"] == "drawing_symbol" for r in rows), 50)
        for row in rows:
            with self.subTest(lamp=row["address"]):
                notes = lamps[row["address"]]["physical"]["notes"]
                self.assertNotIn(spatial.LAMP_DISCLAIMER, notes)
                if row["classification"] == "bulb_mesh":
                    self.assertIn("Figure 2 shows one located lamp symbol at the jet bumper", notes)
                    self.assertIn("retained table's own bulb-mesh center", notes)
                    self.assertNotIn("manual playfield-plane projection", notes)
                else:
                    self.assertEqual(row["method"], "drawing_symbol")
                    self.assertIn("manual playfield-plane projection", notes)
                    self.assertNotIn("retained table's own bulb-mesh center", notes)

    def test_curator_rejects_missing_or_duplicate_lamp_disclaimer(self):
        original_outputs = curator.outputs
        for address in (6, 41):
            for occurrences in (0, 2):
                with self.subTest(address=address, occurrences=occurrences):
                    outputs = original_outputs()
                    lamp = next(d for d in outputs if d["binding"]["group"] == "pinmame.output.lamp"
                                and d["binding"]["device"] == address)
                    lamp["physical"]["notes"] = lamp["physical"]["notes"].replace(
                        spatial.LAMP_DISCLAIMER, " ".join([spatial.LAMP_DISCLAIMER] * occurrences))
                    with patch.object(curator, "outputs", return_value=outputs):
                        with self.assertRaisesRegex(RuntimeError, rf"lamp {re.escape(lamp['id'])} \(public {address}\).*found {occurrences}"):
                            curator.build()

    def test_independent_controls_callout_uniqueness_and_leave_one_out(self):
        calls, candidates = spatial.callout_seed(self.seed)
        for key,page in calls["pages"].items():
            self.assertGreaterEqual(len(page["controls"]),drawing.MIN_CONTROLS)
            ys = [c["xy"][1] for c in page["controls"]]
            self.assertGreaterEqual(max(ys)-min(ys),drawing.MIN_CONTROL_SPAN)
            summary = self.decisions["pages"][key]
            self.assertLess(summary["control_loo_max"],0.02)
            # Pixels derived from the table fit would have near-zero residuals.
            self.assertGreater(summary["control_rms"],0.0005)
        lamp_checks = [d for k,d in self.decisions["placements"].items() if k.startswith("reconcile.lamp-")]
        self.assertEqual(len(lamp_checks),54)
        self.assertEqual(len({d["read"] for d in lamp_checks}),54)
        self.assertTrue(all(d["agrees"] for d in lamp_checks))
        # The table insert proxies are checked, never their manual measurements.
        self.assertTrue(all(k.startswith("reconcile.") for k in calls["checks"]))
        duplicate = copy.deepcopy(calls)
        duplicate["checks"]["reconcile.extra-lamp-6"] = {"page":"pdf-14","label":"6"}
        points = dict(candidates, **{"reconcile.extra-lamp-6":candidates["reconcile.lamp-6"]})
        result = drawing.evaluate(duplicate,points)
        self.assertFalse(all(result["placements"][k]["agrees"] for k in ["reconcile.extra-lamp-6","reconcile.lamp-6"]))
        moved = copy.deepcopy(calls)
        next(r for r in moved["pages"]["pdf-14"]["reads"] if r["label"] == "6")["pixel"] = [1400,400]
        self.assertFalse(drawing.evaluate(moved,candidates)["placements"]["reconcile.lamp-6"]["agrees"])
        short = copy.deepcopy(calls)
        short["pages"]["pdf-14"]["controls"] = short["pages"]["pdf-14"]["controls"][:3]
        with self.assertRaisesRegex(ValueError,"control fit"):
            drawing.evaluate(short,candidates)

    def test_mesh_origins_helpers_and_convex_hull_cannot_grant_credit(self):
        orbit = next(r for r in self.rows if r["group"] == "switch" and r["address"] == 40)
        self.assertEqual(orbit["method"], "world_bounds")
        self.assertNotEqual(spatial.object_point(self.seed,"OrbitGate","world_bounds"),
                            tuple(self.seed["objects"]["OrbitGate"]["fields"]["position"][a] for a in ["x","y"]))
        with self.assertRaisesRegex(ValueError,"world bounds"):
            spatial.object_point(self.seed,"OrbitGate")
        altered = copy.deepcopy(self.seed)
        altered["world_obj"]["bounds"]["Bumper1Base"]["minimum"][0] += 100
        with self.assertRaisesRegex(RuntimeError,"geometry control"):
            spatial.export_controls(altered)
        page = {"controls":[{"xy":p} for p in [[0,0],[1,0],[0.6,1],[0.4,1]]]}
        self.assertTrue(spatial.outside_controls(page,(0.1,0.9)))
        self.assertFalse(spatial.outside_controls(page,(0.5,0.9)))
        bad_edge = copy.deepcopy(self.seed)
        sling = next(r["object"] for r in self.rows if r["group"] == "switch" and r["address"] == 47)
        for p in bad_edge["objects"][sling]["fields"]["drag_points"]:
            p["is_slingshot"] = False
        with self.assertRaisesRegex(ValueError,"active sling edge"):
            spatial.object_point(bad_edge,sling,"slingshot_edge_midpoint")
        extra = copy.deepcopy(self.game)
        next(d for d in extra["outputs"] if d["id"] == "lamp.f").pop("spatial")
        with self.assertRaisesRegex(RuntimeError,"unresolved-device accounting"):
            spatial.report(extra,ROOT)

    def test_corrected_pivots_retain_old_reads_and_native_source_identity(self):
        corrections = {
            ("pdf-14","LeftFlipper"): ([542,2534],[540,2550]),
            ("pdf-14","RightFlipper"): ([978,2538],[980,2550]),
            ("pdf-17","LeftFlipper"): ([645,2536],[645,2545]),
            ("pdf-17","RightFlipper"): ([1085,2534],[1085,2545]),
        }
        recorded = {(r["page"],r["object"]):r for r in self.seed["read_corrections"] if "object" in r}
        self.assertEqual(set(recorded),set(corrections))
        for (page,obj),(old,new) in corrections.items():
            control = next(c for c in self.seed["pages"][page]["controls"] if c["object"] == obj)
            self.assertEqual(control["pixel"],new)
            entry = recorded[page,obj]
            self.assertEqual((entry["old_pixel"],entry["new_pixel"]),(old,new))
            self.assertEqual(entry["source_sha256"],self.seed["pages"][page]["sha256"])
            self.assertEqual(entry["precision_pixels"],5)
            self.assertTrue(all(value % entry["precision_pixels"] == 0 for value in new))
            crop = next(c for c in self.seed["correction_crops"] if c["path"] == entry["native_crop"])
            self.assertEqual(crop["sha256"],entry["native_crop_sha256"])
            self.assertEqual(crop["box"],entry["native_crop_box"])
        pivots15 = {c["object"]:c["pixel"] for c in self.seed["pages"]["pdf-15"]["controls"] if "Flipper" in c["object"]}
        self.assertEqual(pivots15,{"LeftFlipper":[548,2522],"RightFlipper":[987,2525]})

    def test_regional_raw_observations_are_excluded_from_every_precise_fit(self):
        excluded = {"pdf-15":{"17":[531,2170],"18":[999,2173]},
                    "pdf-17":{"9":[960,2875],"12":[1500,2600]}}
        calls,candidates = spatial.callout_seed(self.seed)
        for page,reads in excluded.items():
            pg = self.seed["pages"][page]
            self.assertTrue(set(reads).isdisjoint(r["label"] for r in pg["reads"]))
            raw = {r["label"]:r for r in pg["excluded_reads"]}
            group = "solenoid" if page == "pdf-15" else "switch"
            for label,pixel in reads.items():
                self.assertEqual(raw[label]["pixel"],pixel)
                self.assertEqual(raw[label]["reason"],pg["excluded"][label])
                pid = f"reconcile.{group}-{label}"
                self.assertNotIn(pid,calls["checks"])
                self.assertNotIn(pid,candidates)
                self.assertNotIn(pid,self.decisions["placements"])
                row = next(r for r in self.rows if r["group"] == group and r["address"] == int(label))
                self.assertEqual(row["status"],"observed")
                self.assertIsNone(row["reconciliation"])
                self.assertEqual(row["reconciliation_excluded_reason"],pg["excluded"][label])
                changed = copy.deepcopy(self.seed)
                # Leading-zero normalization must not bypass the exclusion guard.
                changed["pages"][page]["reads"].append({**raw[label],"label":"0"+label})
                with self.assertRaisesRegex(ValueError,"excluded/regional read"):
                    spatial.callout_seed(changed)
                changed = copy.deepcopy(self.seed)
                del changed["pages"][page]["excluded"][label]
                with self.assertRaisesRegex(ValueError,"lacks an explicit exclusion"):
                    spatial.callout_seed(changed)
        self.assertEqual(self.decisions["pages"]["pdf-15"]["callout_pairs"],4)
        self.assertEqual(self.decisions["pages"]["pdf-17"]["callout_pairs"],31)

    def test_spatial_sources_keep_launch_and_lamp_routing_unknown(self):
        sources = {s["id"]:s for s in self.game["sources"]}
        for identifier in [spatial.TABLE,spatial.SCRIPT]:
            self.assertFalse(sources[identifier]["known_working"])
            self.assertIn("rights",sources[identifier])
            self.assertIn("acquired_at",sources[identifier])
        lamps = {d["binding"]["device"]:d for d in self.game["outputs"] if d["kind"] == "lamp"}
        self.assertNotIn("quantity",lamps[6]["physical"])
        self.assertEqual(lamps[6]["provenance"]["status"],"conflicted")
        self.assertEqual(lamps[40]["availability"],"unknown")
        self.assertEqual(lamps[40]["spatial"]["reason"],"cabinet_or_service")
        self.assertEqual(self.seed["unbound_gi"]["authority"],"Table render grouping only, not stock socket quantity or branch membership.")

    def test_vpx_file_hash_is_checked_before_extraction(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("PINMAME_TEST_TMP_ROOT")) as temp:
            t = self.seed["table"]
            path = Path(temp)/t["path"]/t["filename"]
            path.parent.mkdir(parents=True);path.write_bytes(b"changed VPX")
            def configured(name):
                return Path(temp) if name == "PINMAME_VPX_SOURCES_ROOT" else None
            with self.assertRaisesRegex(RuntimeError,"spatial VPX absent or changed"):
                spatial.verify_external(ROOT,configured)


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"),"retained table root not configured")
class FirepowerIISpatialExternalTests(unittest.TestCase):
    def test_every_retained_source_and_derived_field_matches(self):
        spatial.verify_external(ROOT,curator.configured_root)

    def test_retention_metadata_digest_is_fail_closed(self):
        original_sha = spatial.sha
        def changed(path):
            return "0"*64 if path.name == "retention.json" else original_sha(path)
        with patch.object(spatial,"sha",side_effect=changed), self.assertRaisesRegex(RuntimeError,"retention metadata"):
            spatial.verify_external(ROOT,curator.configured_root)

    def test_derived_sources_and_transforms_fail_closed(self):
        seed = spatial.read_seed(ROOT)
        changes = [
            (lambda s:s["table"].update(file_count=s["table"]["file_count"]+1),"totals"),
            (lambda s:s["table"]["inputs"].update({"script.vbs":"0"*64}),"source changed"),
            (lambda s:s["table"]["bounds"].update(right=1001),"normalization bounds"),
            (lambda s:s["objects"]["L6"]["fields"]["center"].update(x=500),"derived fields"),
            (lambda s:s["unbound_gi"]["lights"].pop(),"GI grouping"),
        ]
        if os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
            changes.append((lambda s:s["world_obj"]["bounds"]["SLING1"]["maximum"].__setitem__(0,999),"world mesh bounds"))
        for mutate,error in changes:
            with self.subTest(error=error):
                changed = copy.deepcopy(seed); mutate(changed)
                with patch.object(spatial,"read_seed",return_value=changed), self.assertRaisesRegex(RuntimeError,error):
                    spatial.verify_external(ROOT,curator.configured_root)

    def test_drawing_crops_reproduce_at_native_resolution(self):
        if not all(os.environ.get(v) for v in ["PINMAME_MANUALS_ROOT","PINMAME_REVIEW_ARTIFACTS_ROOT"]):
            self.skipTest("manual and review roots needed")
        from PIL import Image
        seed = spatial.read_seed(ROOT)
        for page in seed["pages"].values():
            native = Image.open(Path(os.environ["PINMAME_MANUALS_ROOT"])/"by-machine"/spatial.MACHINE_ID/page["render"])
            crop = Image.open(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])/spatial.SESSION/page["external_crop"]["path"])
            self.assertEqual(list(native.size),page["pixel_size"])
            self.assertEqual(native.crop(page["external_crop"]["box"]).tobytes(),crop.tobytes())
        for spec in seed["correction_crops"]:
            native = Image.open(Path(os.environ["PINMAME_MANUALS_ROOT"])/"by-machine"/spatial.MACHINE_ID/spec["render"])
            crop = Image.open(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])/spatial.SESSION/spec["path"])
            self.assertEqual(list(native.size),spec["source_size"])
            self.assertEqual(native.crop(spec["box"]).tobytes(),crop.tobytes())

    def test_script_bindings_bulb_doubles_and_substantive_diff(self):
        seed = spatial.read_seed(ROOT)
        extracted = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])/seed["table"]["path"]/"extracted"
        script = (extracted/"script.vbs").read_text(encoding="cp1252")
        self.assertRegex(script,r'cGameName="fpwr2_l2"')
        lamps = re.findall(r'^\s*NFadeL(m)?\s+(\d+),\s*(\w+)',script,re.I|re.M)
        self.assertEqual({int(n) for _,n,_ in lamps},{*range(6,40),*range(41,61)})
        self.assertEqual({int(n):name.lower() for multi,n,name in lamps if multi},{n:f"l{n}a" for n in range(41,45)})
        self.assertIn("bsTrough.InitSw 9, 11, 10",script)
        self.assertIn("bsTrough.InitKick BallRelease",script)
        self.assertIn("vpmNudge.TiltSwitch = 7",script)
        self.assertRegex(script,r'(?i)SolCallback\(4\)\s*=\s*"FLOrbitFlasher"')
        self.assertRegex(script,r'(?i)light62.state\s*=\s*LightStateOn')
        if not os.environ.get("PINMAME_VPX_SCRIPTS_ROOT"):
            self.skipTest("corpus comparator not configured")
        corpus = (Path(os.environ["PINMAME_VPX_SCRIPTS_ROOT"])/"FirePower II (Williams 1983) 1.1.vbs").read_text(encoding="utf-8-sig")
        def tokens(text):
            result = []
            for line in text.splitlines():
                quoted,chars,i = False,[],0
                while i < len(line):
                    ch = line[i]
                    if ch == '"':
                        if quoted and i+1 < len(line) and line[i+1] == '"':
                            chars.extend(['"','"']);i+=2;continue
                        quoted = not quoted
                    if ch == "'" and not quoted:break
                    if quoted or not ch.isspace():chars.append(ch if quoted else ch.lower())
                    i+=1
                if chars:result.append(''.join(chars))
            return result
        old,new = tokens(corpus),tokens(script)
        differences = [op for op in difflib.SequenceMatcher(a=old,b=new,autojunk=False).get_opcodes() if op[0] != "equal"]
        self.assertEqual(len(differences),1)
        kind,a,b,c,d = differences[0]
        self.assertEqual(kind,"replace")
        self.assertEqual((b-a,d-c),(2,1))
        self.assertTrue(all("aball.velz=" in line for line in old[a:b]))
        self.assertNotIn("aball.velz=",new[c])
