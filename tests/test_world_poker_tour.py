from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path, PureWindowsPath
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import drawing_callouts  # noqa: E402

NAME = "world-poker-tour-2006"
MACHINE = ROOT / "machines/partial/stern" / f"{NAME}.json"
AUDIT = ROOT / "reports/spatial/stern" / f"{NAME}.json"
SCRIPT = ROOT / "tools/curate_world_poker_tour.py"
SEED = ROOT / "tools/seeds/stern" / f"{NAME}.json"
SPATIAL = ROOT / "tools/seeds/stern" / f"{NAME}-spatial.json"
CALLOUTS = ROOT / "tools/seeds/stern" / f"{NAME}-callouts.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def address_map(records: list[dict], group: str) -> dict[int, dict]:
    return {item["binding"]["device"]: item for item in records if item["binding"]["group"] == group}


class WorldPokerTourDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load(MACHINE)
        cls.seed = load(SEED)
        cls.spatial = load(SPATIAL)

    def test_one_physical_game_and_all_46_variants(self) -> None:
        definition = self.definition
        self.assertEqual(("stern.world-poker-tour.2006", 5134, "G5poe-MQrb5"), (
            definition["machine"]["id"], definition["machine"]["ipdb_id"], definition["machine"]["opdb_id"]))
        self.assertEqual("partial", definition["coverage"]["status"])
        self.assertEqual(46, len(definition["drivers"]))
        self.assertEqual({d["id"] for d in definition["drivers"]},
                         {d["id"] for d in load(ROOT / "catalog/pinmame.json")["drivers"] if d["id"].startswith("wpt_")})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in definition["drivers"]))
        variants = {d["id"]: d for d in definition["drivers"]}
        self.assertIn("immediate auto-launch", variants["wpt_103a"]["variant_notes"])
        self.assertIn("without auto-launch", variants["wpt_111a"]["variant_notes"])
        self.assertIn("without auto-launch", variants["wpt_140l"]["variant_notes"])
        self.assertFalse((ROOT / "machines/author-ready/stern" / f"{NAME}.json").exists())

    def test_full_public_address_disposition(self) -> None:
        switches = address_map(self.definition["inputs"], "pinmame.input.switch")
        self.assertEqual(set(range(-7, 1)) | set(range(1, 73)) | set(range(81, 89)), set(switches))
        self.assertEqual(set(range(1, 9)), set(address_map(self.definition["inputs"], "pinmame.input.dip")))
        self.assertEqual({1, 2, 17, 64}, {i for i in range(1, 65) if switches[i]["availability"] == "unused"})
        self.assertEqual("used", switches[21]["availability"])
        self.assertEqual("optional", switches[15]["availability"])
        self.assertEqual("opto", switches[21]["physical"]["switch_type"])
        self.assertEqual("conflicted", switches[54]["provenance"]["status"])
        self.assertNotIn("quantity", switches[54]["physical"])
        self.assertEqual("validated", switches[56]["provenance"]["status"])
        self.assertEqual("opto", switches[56]["physical"]["switch_type"])
        self.assertEqual("cabinet_or_service", switches[56]["spatial"]["reason"])
        self.assertEqual({"unknown"}, {switches[i]["physical"]["switch_type"] for i in (30, 31, 32)})
        self.assertEqual({"leaf"}, {switches[i]["physical"]["switch_type"] for i in (14, 26, 27, 41)})
        self.assertEqual({"microswitch"}, {switches[i]["physical"]["switch_type"] for i in (9, 51, 53)})
        self.assertEqual("J2-P2", switches[65]["wiring"]["drive_connection"])
        self.assertEqual("J2-P6", switches[68]["wiring"]["drive_connection"])
        self.assertEqual("J2-P1/11 and J3-P10", switches[65]["wiring"]["return_connection"])
        self.assertEqual({"J2-P1/11 and J3-P10"},
                         {switches[i]["wiring"]["return_connection"] for i in (*range(65, 73), *range(81, 89))})
        self.assertEqual({"unknown"}, {switches[i]["physical"]["switch_type"] for i in (65, 66, 67, 68, 69, -5)})
        self.assertTrue(all(switches[i]["normally_closed"] for i in (83, 81, 87, 85)))
        self.assertTrue(all(not switches[i]["normally_closed"] for i in (84, 82, 88, 86)))
        for i in (83, 81, 87, 85):
            self.assertEqual("flipper assembly", switches[i]["physical"]["location"])
            self.assertEqual(("not_applicable", "internal_nonvisual"),
                             (switches[i]["spatial"]["status"], switches[i]["spatial"]["reason"]))
        for i in (84, 82, 88, 86):
            self.assertEqual("cabinet", switches[i]["physical"]["location"])
            self.assertEqual("cabinet_or_service", switches[i]["spatial"]["reason"])
        solenoids = address_map(self.definition["outputs"], "pinmame.output.solenoid")
        lamps = address_map(self.definition["outputs"], "pinmame.output.lamp")
        self.assertEqual(set(range(1, 67)), set(solenoids))
        self.assertEqual(set(range(1, 340)), set(lamps))
        self.assertEqual("unused", lamps[77]["availability"])
        self.assertEqual("Queen of spades", lamps[42]["label"])
        self.assertEqual("optional", solenoids[24]["availability"])
        self.assertNotIn("spatial", solenoids[24])
        self.assertEqual("conflicted", solenoids[32]["provenance"]["status"])
        self.assertNotIn("part_number", solenoids[32]["physical"])
        self.assertIn("090-5034-ND", solenoids[32]["physical"]["notes"])
        self.assertIn("090-5044-ND", solenoids[32]["physical"]["notes"])
        self.assertEqual(("ORG", "J6-P10", "BLK-GRY", "J6-P8"),
                         (solenoids[32]["wiring"]["power_wire"], solenoids[32]["wiring"]["power_connection"],
                          solenoids[32]["wiring"]["control_wire"], solenoids[32]["wiring"]["control_connection"]))
        self.assertEqual({0}, set(address_map(self.definition["outputs"], "pinmame.output.gi")))

    def test_displays_mechanisms_and_spatial_limits(self) -> None:
        displays = self.definition["displays"]
        self.assertEqual(15, len(displays))
        self.assertEqual((128, 32), (displays[0]["width"], displays[0]["height"]))
        self.assertEqual({(5, 7)}, {(d["width"], d["height"]) for d in displays[1:]})
        self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])
        self.assertEqual("playfield", {d["physical_location"] for d in displays[1:]}.pop())
        self.assertTrue(all(d["spatial"]["status"] == "observed" for d in displays[1:]))
        self.assertEqual(["display"] * 14, [d["spatial"]["placements"][0]["role"] for d in displays[1:]])
        self.assertEqual([(0.255515, 0.577235), (0.645221, 0.612791)],
                         [(displays[i]["spatial"]["placements"][0]["x"], displays[i]["spatial"]["placements"][0]["y"]) for i in (1, 14)])
        self.assertEqual(list(range(1, 15)), [d["controller_index"] for d in displays[1:]])
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        for ident in ("four-ball-trough", "left-eight-bank", "middle-four-bank",
                      "right-four-bank", "jail-bars", "left-ramp", "right-ramp"):
            self.assertIn(f"mechanism.{ident}", mechanisms)
        self.assertEqual(2, len([m for m in mechanisms.values() if m["kind"] == "drop_target_bank" and len(m["sensors"]) == 4]))
        lamps = address_map(self.definition["outputs"], "pinmame.output.lamp")
        self.assertEqual(("validated", 0.448267, 0.525167),
                         (lamps[9]["spatial"]["status"], lamps[9]["spatial"]["placements"][0]["x"], lamps[9]["spatial"]["placements"][0]["y"]))
        for number in (1, 2, 67, 68, 75, 76, 77):
            self.assertEqual("not_applicable", lamps[number]["spatial"]["status"])
        self.assertNotIn("spatial", lamps[3])  # Apron lamp has no proved socket coordinate.
        audit = load(AUDIT)
        self.assertEqual("pinmame-spatial-blockers", audit["format"])
        self.assertEqual(self.spatial["table_manifest_sha256"], audit["extraction_manifest_sha256"])
        self.assertEqual(["switch.14-lower-right-10-point", "switch.18-trough-4-left", "switch.19-trough-3",
                          "switch.20-trough-2", "switch.21-trough-1-right", "switch.22-trough-stacking-opto",
                          "switch.41-lower-left-10-point", "switch.54-left-ramp-made", "coil.24-optional-coil",
                          "lamp.3-deal-again", "gi.aggregate"], audit["missing_spatial_ids"])
        self.assertEqual({"conflict.sw54-fitment", "conflict.q32-coil"},
                         set(audit["unresolved_conflict_ids"]))
        self.assertEqual(5, len(audit["drawing_reconciliation"]["controls"]))
        self.assertTrue(all(c["residual_vpu"] <= 12 for c in audit["drawing_reconciliation"]["controls"]))

    def test_script_bound_mechanism_anchors(self) -> None:
        objects = self.spatial["objects"]
        # SW43 is bound through its Spinner; the same-numbered trigger has no handler.
        self.assertNotIn("sw43", objects)
        switches = address_map(self.definition["inputs"], "pinmame.input.switch")
        expected = {3: "LaneKicker", 8: "sw8s", 26: "LeftSlingShot", 27: "RightSlingShot",
                    30: "Bumper1b", 31: "Bumper2b", 32: "Bumper3b", 43: "sw43s"}
        for number, name in expected.items():
            placement = switches[number]["spatial"]["placements"][0]
            self.assertEqual(("sensor", objects[name][0], objects[name][1]), (placement["role"], placement["x"], placement["y"]))
        coils = address_map(self.definition["outputs"], "pinmame.output.solenoid")
        anchors = {1: "BallRelease", 2: "sw23", 3: "LaneKicker", 9: "Bumper1b", 10: "Bumper2b", 11: "Bumper3b",
                   13: "UpLeftFlipper", 14: "UpRightFlipper", 15: "LeftFlipper", 16: "RightFlipper",
                   17: "LeftSlingShot", 18: "RightSlingShot", 20: "LeftPost", 21: "sw49",
                   22: "f22b", 23: "f23b", 25: "F25a", 31: "f31b"}
        for number, name in anchors.items():
            placement = coils[number]["spatial"]["placements"][0]
            role = "emitter" if coils[number]["kind"] == "flasher" else "effect"
            self.assertEqual((role, objects[name][0], objects[name][1]), (placement["role"], placement["x"], placement["y"]))
        for number, targets in {5: (33, 34, 35, 36), 6: (37, 38, 39, 40), 7: (10, 11, 12, 13), 8: (4, 5, 6, 7)}.items():
            placement = coils[number]["spatial"]["placements"][0]
            self.assertEqual((round(sum(objects[f"sw{t}"][0] for t in targets) / 4, 6),
                              round(sum(objects[f"sw{t}"][1] for t in targets) / 4, 6)),
                             (placement["x"], placement["y"]))
        for number in (4, 12, 19, 26, 27, 28, 29, 30, 32):
            self.assertEqual("not_applicable", coils[number]["spatial"]["status"])
        ids = [p["id"] for group in ("inputs", "outputs", "displays") for item in self.definition[group]
               for p in item.get("spatial", {}).get("placements", [])]
        self.assertEqual(len(ids), len(set(ids)))

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not configured")
    def test_seed_objects_recompute_from_extraction(self) -> None:
        base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "stern/world-poker-tour-2006/wpt-062018a"
        for name, (x, y, kind, relative) in self.spatial["objects"].items():
            item = load(base / relative)[kind]
            if kind == "Wall":
                points = [(p["x"], p["y"]) for p in item["drag_points"]]
                raw = (sum(p[0] for p in points) / len(points), sum(p[1] for p in points) / len(points))
            else:
                point = item.get("center") or item.get("position")
                raw = (point["x"], point["y"])
            self.assertEqual((name, round(raw[0] / 952, 6), round(raw[1] / 2250, 6)), (item["name"], x, y))

    def test_drawing_callout_check_decides_every_placement_status(self) -> None:
        seed = load(CALLOUTS)
        decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
        source = "review.wpt-drawing-callouts-2026-10-01"
        self.assertIn(source, {s["id"] for s in self.definition["sources"]})
        checked = 0
        for device in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
            for placement in (device.get("spatial") or {}).get("placements") or []:
                decision = decisions["placements"].get(placement["id"])
                status = placement["provenance"]["status"]
                if decision is None:
                    self.assertEqual("observed", status, placement["id"])
                    continue
                checked += 1
                self.assertEqual("validated" if decision["agrees"] else "observed", status, placement["id"])
                self.assertEqual(decision["agrees"], source in placement["provenance"]["source_refs"], placement["id"])
                notes = (device.get("physical") or {}).get("notes") or ""
                self.assertEqual(not decision["agrees"], f"draws callout {decision['label']}" in notes, placement["id"])
        self.assertEqual(len(seed["checks"]), checked)
        self.assertEqual(drawing_callouts.summary(seed, decisions, f"tools/seeds/stern/{NAME}-callouts.json",
                                                  hashlib.sha256(CALLOUTS.read_bytes()).hexdigest()),
                         load(AUDIT)["drawing_callout_check"])
        # Every page is fitted on independently read controls, never on borrowed ones.
        for page in seed["pages"].values():
            self.assertGreaterEqual(len(page["controls"]), 5)
            self.assertFalse({c["feature"] for c in page["controls"]} & {c["feature"] for c in page["excluded_controls"]})

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review artifacts not configured")
    def test_drawing_callout_renders_and_reads_are_retained(self) -> None:
        seed = load(CALLOUTS)
        roots = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
        self.assertGreater(drawing_callouts.verify_retained(seed, ROOT, None, roots), 3)
        tampered = json.loads(json.dumps(seed))
        tampered["pages"]["pdf-9"]["image"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "render missing or changed"):
            drawing_callouts.verify_retained(tampered, ROOT, None, roots)

    def test_excerpt_and_scenario_integrity(self) -> None:
        sources = {s["id"]: s for s in self.definition["sources"]}
        for source in sources.values():
            for excerpt in source.get("excerpts", []):
                path = ROOT / excerpt["path"]
                self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        scenario = load(ROOT / "tools/harness-scenarios/stern" / f"{NAME}-switch-test.json")
        self.assertEqual("wpt_140a", scenario["game"])
        self.assertEqual([3, 21, 63], [a["switch"] for a in scenario["actions"] if a["type"] == "pulse"])
        self.assertIn("DMD frames", scenario["notes"])
        coil_scenario = load(ROOT / "tools/harness-scenarios/stern" / f"{NAME}-coil-sweep.json")
        self.assertEqual(31, sum(a.get("label", "").startswith("advance coil diagnostic") for a in coil_scenario["actions"]))
        self.assertIn("skips Q24", coil_scenario["notes"])
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])

    def test_deterministic_curator_and_fail_closed_wrong_root(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        for key in ("PINMAME_MANUALS_ROOT", "PINMAME_VPX_SOURCES_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_SOURCE_ROOT", "PINMAME_SCRIPTS_ROOT"):
            env.pop(key, None)
        for _ in range(2):
            checked = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check"], cwd=ROOT, env=env,
                                     capture_output=True, text=True, check=False)
            self.assertEqual(0, checked.returncode, checked.stdout + checked.stderr)
        with tempfile.TemporaryDirectory() as temp:
            env["PINMAME_MANUALS_ROOT"] = temp
            checked = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check"], cwd=ROOT, env=env,
                                     capture_output=True, text=True, check=False)
            self.assertNotEqual(0, checked.returncode)
            self.assertIn("missing or wrong retained artifact", checked.stderr)

    def test_runtime_trace_content_rejects_wrong_native_or_failed_run(self) -> None:
        spec = importlib.util.spec_from_file_location("wpt_curator", SCRIPT)
        self.assertIsNotNone(spec)
        curator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(curator)
        scenario = ROOT / "tools/harness-scenarios/stern" / f"{NAME}-switch-test.json"
        valid = {
            "failure": None,
            "library_sha256": curator.PINNED_LIBRARY_SHA256,
            "game": "wpt_140a",
            "scenario": {"sha256": hashlib.sha256(scenario.read_bytes()).hexdigest()},
            "snapshots": [{}] * 14,
        }
        curator.verify_runtime_content(valid, scenario, 14)
        for change in (
            {"library_sha256": "ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d"},
            {"failure": {"message": "failed"}},
            {"scenario": {"sha256": "0" * 64}},
            {"snapshots": [{}] * 13},
        ):
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "untrusted pinned"):
                curator.verify_runtime_content(valid | change, scenario, 14)

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not configured")
    def test_retained_vpx_manifest_recomputes(self) -> None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("external_manifest", ROOT / "tools/build_external_evidence_manifest.py")
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "stern/world-poker-tour-2006/wpt-062018a"
        self.assertEqual(self.spatial["table_sha256"], hashlib.sha256((base / "wpt 062018a.vpx").read_bytes()).hexdigest())
        self.assertEqual(self.spatial["table_manifest_sha256"],
                         module.check_manifest(base / "extract-vpxtool-v1", "wpt_140a"))
        alternate = base.parent / "world-poker-tour-stern-2006"
        self.assertEqual("92a9720af51c825c9603d9dc78acc2423b7f86c907e1c4a6e92393156a22d9b8",
                         hashlib.sha256((alternate / "World Poker Tour (Stern 2006).vpx").read_bytes()).hexdigest())
        self.assertEqual("368e8262d51e6db70f8f05a8919f008d8d0a92340d29b1527ff8e9c700ada9e6",
                         module.check_manifest(alternate / "extract-vpxtool-v1", "wpt_140a"))
        self.assertEqual(14, len(self.spatial["mini_displays"]))
        for i, center in enumerate(self.spatial["mini_displays"]):
            number = 18 + 35 * i
            self.assertEqual((i + 1, f"D{number}"), (center["controller_index"], center["center_pixel"]))
            extracted = base / "extract-vpxtool-v1/gameitems" / f"Light.D{number}.json"
            point = load(extracted)["Light"]["center"]
            self.assertEqual((round(point["x"] / 952, 6), round(point["y"] / 2250, 6)), (center["x"], center["y"]))
            pixels = [load(base / "extract-vpxtool-v1/gameitems" / f"Light.D{1 + 35 * i + j}.json")["Light"]["center"] for j in range(35)]
            x_values = sorted({pixel["x"] for pixel in pixels})
            y_values = sorted({pixel["y"] for pixel in pixels})
            self.assertEqual((5, 7), (len(x_values), len(y_values)))
            self.assertEqual((x_values[2], y_values[3]), (point["x"], point["y"]))
        table_script = (base / "extract-vpxtool-v1/script.vbs").read_text(encoding="utf-8", errors="replace")
        self.assertIn("LED(69)=Array(D484,D485,D486,D487,D488,D489,D490", table_script)
        older_script = (alternate / "extract-vpxtool-v1/script.vbs").read_text(encoding="utf-8", errors="replace")
        self.assertIn("UpLeftFlipper.RotateToEnd", older_script)
        self.assertIn("UpRightFlipper.RotateToEnd", older_script)

    def test_runtime_verifier_uses_evidence_root_outside_a_managed_worktree(self) -> None:
        spec = importlib.util.spec_from_file_location("wpt_curator_paths", SCRIPT)
        curator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(curator)
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            checkout = base / "ordinary-checkout"
            review_root = base / "retained-working-dir/review-artifacts"
            session = review_root / "stern.world-poker-tour.2006/session-20260930"
            session.mkdir(parents=True)
            native = review_root.parent / "builds/pinmame-8371478/Release/pinmame64.dll"
            native.parent.mkdir(parents=True)
            native.write_bytes(b"fixture native library")
            native_hash = hashlib.sha256(native.read_bytes()).hexdigest()
            trace_hashes = []
            for kind, count in (("switch-test", 14), ("coil-sweep", 40)):
                relative = Path("tools/harness-scenarios/stern") / f"{NAME}-{kind}.json"
                scenario = checkout / relative
                scenario.parent.mkdir(parents=True, exist_ok=True)
                scenario.write_bytes((ROOT / relative).read_bytes())
                trace = {
                    "failure": None, "game": "wpt_140a", "library_sha256": native_hash,
                    "scenario": {"sha256": hashlib.sha256(scenario.read_bytes()).hexdigest()},
                    "snapshots": [{}] * count,
                    "dmd_dir": rf"Z:\old-machine\evidence\{kind}-frames",
                }
                frames = session / f"{kind}-frames"
                frames.mkdir()
                for index in range(count):
                    (frames / f"{index}.pgm").write_bytes(b"P5\n1 1\n255\n\0")
                filename = "wpt-switch-test-pinned-frames-run.json" if kind == "switch-test" else "wpt-coil-diagnostic-pinned-frames-run.json"
                path = session / filename
                path.write_text(json.dumps(trace), encoding="utf-8")
                trace_hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
            # Fixture drawing-reconciliation directory with its own manifest.
            spatial = json.loads(json.dumps(self.spatial))
            drawing_dir = review_root / spatial["drawing_reconciliation"]["retained_artifacts"]["directory"].split("review-artifacts/", 1)[1]
            drawing_dir.mkdir(parents=True)
            for render in ("wpt200_sw-007.png", "wpt200_lamp-009.png", "wpt200_coil-011.png"):
                (drawing_dir / render).write_bytes(render.encode("ascii"))
            for key, render in (("pdf_page_7", "wpt200_sw-007.png"), ("pdf_page_9", "wpt200_lamp-009.png"), ("pdf_page_11", "wpt200_coil-011.png")):
                spatial["drawing_reconciliation"]["renders"][key]["sha256"] = hashlib.sha256((drawing_dir / render).read_bytes()).hexdigest()
            manifest_spec = importlib.util.spec_from_file_location("wpt_manifest", ROOT / "tools/build_external_evidence_manifest.py")
            manifest_module = importlib.util.module_from_spec(manifest_spec)
            manifest_spec.loader.exec_module(manifest_module)
            spatial["drawing_reconciliation"]["retained_artifacts"]["manifest_sha256"] = manifest_module.write_manifest(drawing_dir, "wpt_140a")
            with patch.dict(os.environ, {"PINMAME_REVIEW_ARTIFACTS_ROOT": str(review_root)}, clear=True), \
                    patch.multiple(curator, ROOT=checkout, PINNED_LIBRARY_SHA256=native_hash,
                                   PINNED_SWITCH_TRACE_SHA256=trace_hashes[0], PINNED_COIL_TRACE_SHA256=trace_hashes[1]),                     patch.object(curator.drawing_callouts, "verify_retained", lambda *args: 0):
                curator.verify_external(self.seed, spatial)
                missing_frame = session / "coil-sweep-frames/39.pgm"
                missing_frame.unlink()
                with self.assertRaisesRegex(ValueError, "missing retained DMD frames"):
                    curator.verify_external(self.seed, spatial)
                missing_frame.write_bytes(b"P5\n1 1\n255\n\0")
                (drawing_dir / "wpt200_lamp-009.png").write_bytes(b"tampered")
                with self.assertRaisesRegex(ValueError, "wrong drawing reconciliation file"):
                    curator.verify_external(self.seed, spatial)
                (drawing_dir / "wpt200_lamp-009.png").write_bytes(b"wpt200_lamp-009.png")
                native.write_bytes(b"wrong native library")
                with self.assertRaisesRegex(ValueError, "wrong verified pinned native"):
                    curator.verify_external(self.seed, spatial)

    @unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root not configured")
    def test_retained_manual_and_bulletin(self) -> None:
        base = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine/stern.world-poker-tour.2006"
        sources = {s["id"]: s for s in self.definition["sources"]}
        self.assertEqual(sources["manual.stern-wpt-2006"]["sha256"],
                         hashlib.sha256((base / "World_Poker_Tour_Manual.pdf").read_bytes()).hexdigest())
        for number in (163, 164, 165):
            self.assertEqual(sources[f"bulletin.stern-wpt-{number}"]["sha256"],
                             hashlib.sha256((base / f"sb{number}.pdf").read_bytes()).hexdigest())
        archive = load(Path(os.environ["PINMAME_MANUALS_ROOT"]) / "manifest.json")
        entries = [item for item in archive["documents"] if item["machine_id"] == "stern.world-poker-tour.2006"]
        self.assertEqual(4, len(entries))
        for entry in entries:
            self.assertEqual(entry["sha256"], hashlib.sha256((Path(os.environ["PINMAME_MANUALS_ROOT"]) / entry["relative_path"]).read_bytes()).hexdigest())

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained runtime root not configured")
    def test_retained_rom_diagnostic(self) -> None:
        base = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "stern.world-poker-tour.2006/session-20260930"
        source = next(s for s in self.definition["sources"] if s["id"] == "runtime.wpt-140a-switch-test")
        run = base / "wpt-switch-test-pinned-frames-run.json"
        self.assertEqual(source["sha256"], hashlib.sha256(run.read_bytes()).hexdigest())
        switch_data = load(run)
        self.assertIsNone(switch_data["failure"])
        pinned_library = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
        self.assertEqual(pinned_library, switch_data["library_sha256"])
        self.assertEqual("wpt_140a", switch_data["game"])
        events = switch_data["events"]
        switch_scenario = ROOT / "tools/harness-scenarios/stern" / f"{NAME}-switch-test.json"
        self.assertEqual(hashlib.sha256(switch_scenario.read_bytes()).hexdigest(), switch_data["scenario"]["sha256"])
        self.assertEqual(15, sum(e["event"] == "display_available" for e in events))
        self.assertEqual({3, 21, 63}, {e["number"] for e in events if e.get("event") == "switch" and e.get("state") == 1 and e.get("number") in {3, 21, 63}})
        coil_source = next(s for s in self.definition["sources"] if s["id"] == "runtime.wpt-140a-coil-test")
        coil_run = base / "wpt-coil-diagnostic-pinned-frames-run.json"
        self.assertEqual(coil_source["sha256"], hashlib.sha256(coil_run.read_bytes()).hexdigest())
        coil_data = load(coil_run)
        self.assertIsNone(coil_data["failure"])
        self.assertEqual(40, len(coil_data["snapshots"]))
        scenario = ROOT / "tools/harness-scenarios/stern" / f"{NAME}-coil-sweep.json"
        self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), coil_data["scenario"]["sha256"])
        self.assertEqual(pinned_library, coil_data["library_sha256"])
        self.assertEqual("wpt_140a", coil_data["game"])
        self.assertEqual(40, len(list((base / PureWindowsPath(coil_data["dmd_dir"]).name).glob("*.pgm"))))
        self.assertEqual(14, len(list((base / PureWindowsPath(switch_data["dmd_dir"]).name).glob("*.pgm"))))
        native = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve().parent / "builds/pinmame-8371478/Release/pinmame64.dll"
        self.assertEqual(pinned_library, hashlib.sha256(native.read_bytes()).hexdigest())
        source_check = load(base / "existing-native-source-check.json")
        self.assertEqual((self.seed["pinmame_revision"], 1842, []),
                         (source_check["revision"], source_check["checked_files"], source_check["differences"]))
        export = load(base / "pinned-native-catalog.json")
        self.assertEqual((pinned_library, self.seed["pinmame_revision"], 2895),
                         (export["library_sha256"], export["source_revision"], len(export["drivers"])))
        if rom_root := os.environ.get("PINMAME_ROM_LIBRARY_ROOT"):
            rom = Path(rom_root) / "wpt_140a.zip"
            self.assertEqual("b4f98abae8cecb80a603285357c39688182b90ef376c46c80de5facb4e302463", hashlib.sha256(rom.read_bytes()).hexdigest())
            with zipfile.ZipFile(rom) as archive:
                self.assertEqual("43dd7bdf25ff1bc205f3552841318d47424324d9f9d0049d400a168d2ad9f383",
                                 hashlib.sha256(archive.read("wpt1400a.bin")).hexdigest())

    @unittest.skipUnless(os.environ.get("PINMAME_SOURCE_ROOT") and os.environ.get("PINMAME_SCRIPTS_ROOT"), "pinned managed source roots not configured")
    def test_exact_managed_sources(self) -> None:
        checkout = Path(os.environ["PINMAME_SOURCE_ROOT"])
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=checkout, capture_output=True, text=True, check=True).stdout.strip()
        self.assertEqual(self.seed["pinmame_revision"], revision)
        source = (checkout / "src/wpc/sam.c").read_text(encoding="utf-8", errors="replace")
        self.assertIn("drawSeg[35 * dmd_y + 5 * dmd_x + 4 - x]", source)
        self.assertIn("const core_tLCDLayout* layout = &core_gameData->lcdLayout[1 + i]", source)
        script = Path(os.environ["PINMAME_SCRIPTS_ROOT"]) / "World Poker Tour (Stern 2006) v.2.3.1.vbs"
        source = next(s for s in self.definition["sources"] if s["id"] == "vpx.script.wpt-known-working")
        self.assertEqual(source["sha256"], hashlib.sha256(script.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
