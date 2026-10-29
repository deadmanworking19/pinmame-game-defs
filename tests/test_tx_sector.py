from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_tx_sector as curator
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_game_defs.validation import validate_machine
from build_external_evidence_manifest import write_manifest


class TxSectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(curator.PARTIAL)
        cls.devices = {(d["binding"]["group"].rsplit(".", 1)[-1], d["binding"]["device"]): d for d in cls.definition["inputs"] + cls.definition["outputs"]}

    def test_identity_variants_and_unique_catalog_claim(self):
        self.assertEqual("712", self.definition["machine"]["model_number"])
        self.assertEqual(2699, self.definition["machine"]["ipdb_id"])
        expected = {"txsector", "txsectrf", "txsectrg", "txsectfp", "txsecffp", "txsecgfp"}
        self.assertEqual(expected, {d["id"] for d in self.definition["drivers"]})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in self.definition["drivers"]))
        claimants = []
        for path in (ROOT / "machines").rglob("*.json"):
            machine = load_json(path)
            if expected & {d["id"] for d in machine.get("drivers", [])}:
                claimants.append(machine["machine"]["id"])
        self.assertEqual([curator.MACHINE_ID], claimants)

    def test_complete_ranges_and_blank_is_not_unused(self):
        self.assertEqual(set(range(-8, 0)) | {10 * s + r for s in range(8) for r in range(8)} | set(range(111, 119)), {n for (g, n) in self.devices if g == "switch"})
        self.assertEqual(set(range(1, 43)), {n for g, n in self.devices if g == "dip"})
        self.assertEqual(set(range(64)), {n for g, n in self.devices if g == "lamp"})
        self.assertEqual(set(range(1, 12)) | set(range(45, 49)), {n for g, n in self.devices if g == "solenoid"})
        self.assertEqual("unknown", self.devices["switch", 0]["availability"])
        for (group, number), device in self.devices.items():
            if group == "switch" and 0 <= number <= 77 and device["availability"] == "unknown":
                self.assertEqual("switch", device["kind"])
                self.assertEqual("unknown", device["physical"]["switch_type"])
                self.assertNotIn("normally_closed", device)
                self.assertNotIn("spatial", device)
        self.assertEqual("used", self.devices["switch", 47]["availability"])
        self.assertEqual("unused", self.devices["switch", 67]["availability"])
        self.assertEqual("unused", self.devices["switch", 77]["availability"])
        for number in [67, 77]:
            cell = self.devices["switch", number]
            self.assertEqual("switch", cell["kind"])
            self.assertEqual("unused", cell["spatial"]["reason"])
            self.assertNotIn("normally_closed", cell)
            for field in ["quantity", "switch_type", "location", "part_number"]:
                self.assertNotIn(field, cell["physical"])
        self.assertEqual("unknown", self.devices["lamp", 14]["availability"])

    def test_button_copies_polarity_and_local_mechanisms(self):
        self.assertEqual("virtual", self.devices["switch", 6]["kind"])
        self.assertIn("114", self.devices["switch", 6]["physical"]["notes"])
        self.assertIn("112", self.devices["switch", 16]["physical"]["notes"])
        self.assertTrue(self.devices["switch", -1]["normally_closed"])
        self.assertFalse(self.devices["switch", -1]["initial_active"])
        self.assertFalse(self.devices["switch", 35]["normally_closed"])
        for n in range(45, 49):
            self.assertEqual("virtual", self.devices["solenoid", n]["kind"])
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        self.assertEqual([], mechanisms["mech.local-kickers"]["actuators"])
        self.assertEqual([], mechanisms["mech.flippers"]["actuators"])
        self.assertEqual(4, len([m for m in mechanisms if m.endswith("-hole")]))
        self.assertIn(self.devices["lamp", 13]["id"], mechanisms["mech.rollover-drop"]["actuators"])
        for n in [1, 2, 5, 6]:
            self.assertIn("two #67", self.devices["solenoid", n]["physical"]["notes"])

    def test_emitters_are_not_render_double_counts(self):
        for n in range(15, 20):
            lamp = self.devices["lamp", n]
            self.assertEqual(3, lamp["physical"]["quantity"])
            self.assertEqual(3, len(lamp["spatial"]["placements"]))
        self.assertEqual(1, self.devices["lamp", 11]["physical"]["quantity"])
        self.assertEqual(1, len(self.devices["lamp", 11]["spatial"]["placements"]))
        self.assertEqual(2, self.devices["lamp", 29]["physical"]["quantity"])
        self.assertNotIn("spatial", self.devices["lamp", 29])
        self.assertNotIn("spatial", self.devices["switch", 76])
        self.assertEqual(2, self.devices["lamp", 3]["physical"]["quantity"])
        self.assertNotIn("quantity", self.devices["gi", 0]["physical"])
        self.assertNotIn("spatial", self.devices["switch", 56])

    def test_driver_provisions_do_not_assert_fitted_loads(self):
        expected = {14: ("Q15 (MPS-U45)", "A3J3-22"), 48: ("Q49 (MPS-U45)", "A3J3-E"), 49: ("Q50 (MPS-U45)", "A3J3-H")}
        for number, (transistor, connector) in expected.items():
            driver = self.devices["lamp", number]
            self.assertEqual("control_signal", driver["kind"])
            self.assertTrue(driver["id"].startswith("control_signal."))
            self.assertEqual("unknown", driver["availability"])
            self.assertEqual("observed", driver["provenance"]["status"])
            self.assertNotIn("spatial", driver)
            self.assertNotIn("virtual", driver["id"])
            for field in ["quantity", "location", "part_number"]:
                self.assertNotIn(field, driver["physical"])
            self.assertEqual(transistor, driver["wiring"]["driver_transistor"])
            self.assertEqual(connector, driver["wiring"]["drive_connection"])
        relationships = {row["id"]: row for row in self.definition["relationships"]}
        for number in [48, 49]:
            relation = relationships["relationship.complement-" + str(number)]
            self.assertEqual("inverted", relation["kind"])
            self.assertEqual(self.devices["lamp", number - 4]["id"], relation["source"])
            self.assertEqual(self.devices["lamp", number]["id"], relation["destination"])
            self.assertEqual(["pinmame.tx-sector"], relation["provenance"]["source_refs"])
            notes = self.devices["lamp", number]["physical"]["notes"]
            self.assertIn("selector 12 write", notes)
            self.assertIn("Out-of-range binary selectors 13-15", notes)

    def test_game_declarations_stay_in_game_scope(self):
        note = (ROOT / self.definition["knowledge"]["path"]).read_text(encoding="utf-8")
        for fact in ["invSw = 0", "FLIP_SWNO(6,16)", "no `FLIP_SOL` or EOS flags", "hw.lampCol = 0", "nLamps = 64", "gts80bs2"]:
            self.assertIn(fact, note)
        excerpt = (ROOT / "evidence/excerpts" / curator.MACHINE_ID / "pinmame-controller.txt").read_text(encoding="utf-8")
        for driver in self.definition["drivers"]:
            self.assertIn("INITGAME(" + driver["id"], excerpt)

    def test_reviewed_switch_65_wire_code_matches_native_glyph(self):
        excerpt = (ROOT / "evidence/excerpts" / curator.MACHINE_ID / "manual-switch-matrix.md").read_text(encoding="utf-8")
        self.assertIn("| 6 | 5 | SW 65 | TOP RIGHT HOLE | 366 |", excerpt)
        self.assertNotIn("| 6 | 5 | SW 65 | TOP RIGHT HOLE | 566 |", excerpt)

    def test_wiring_readings_do_not_resolve_harness_from_runtime_binding(self):
        directory = ROOT / "evidence/excerpts" / curator.MACHINE_ID
        table = (directory / "manual-lamps-direct-coils.md").read_text(encoding="utf-8")
        self.assertIn("| P/O A3J3 pin 22 | 322 | L21 |", table)
        self.assertIn("| P/O A3J3 pin 9 | 344 | L24 |", table)
        self.assertIn("| P/O A3J3 pin 10 | 355 | L25 |", table)
        self.assertIn("| P/O A3J3 pin C? | 588 | L3 |", table)
        for row in ["| P/O A3J3 pin Z | GROUND (L12–L19) | 2 |", "| P/O A3J3 pin U | GROUND (L28–L35) | 4 |", "| P/O A3J3 pin [S or 5; ambiguous] | GROUND (L40–L43) | 5 |", "| P/O A3J3 pin [G or C; ambiguous] | GROUND (L44–L51) | 6 |"]:
            self.assertIn(row, table)
        self.assertIn("| P/O A3J3 pin [E or 2; ambiguous] | 744 | L43 |", table)
        self.assertNotIn("| P/O A3J3 pin E | 744 | L43 |", table)
        board = (directory / "manual-driver-board.md").read_text(encoding="utf-8")
        for row in ["| 14 | Q15 MPS-U45 | A3J3-22 |", "| 21 | Q22 MPS-U45 | A3J3-20 |", "| 43 | Q44 MPS-A13 | A3J3-2 |", "| 48 | Q49 MPS-U45 | A3J3-E |"]:
            self.assertIn(row, board)
        for number, code in [(14, "322"), (21, "322"), (43, "744"), (48, "744")]:
            self.assertIn(code, self.devices["lamp", number]["physical"]["notes"])
        for number in [21, 43]:
            device = self.devices["lamp", number]
            self.assertNotIn("wiring", device)
            self.assertIn("No structured harness pin", device["physical"]["notes"])
        for number in [14, 48]:
            self.assertIn("board-internal", self.devices["lamp", number]["physical"]["notes"])
            self.assertEqual("unknown", self.devices["lamp", number]["availability"])
        self.assertIn("E or 2; ambiguous", self.devices["lamp", 43]["physical"]["notes"])
        self.assertIn("E or 2; ambiguous", self.devices["lamp", 48]["physical"]["notes"])

    def test_projection_notes_identify_the_single_retained_anchor(self):
        for number, name, point in [(2, "BallRelease", (0.870625, 0.854313)), (13, "SW42", (0.215, 0.358875))]:
            device = self.devices["lamp", number]
            self.assertIn(name, device["physical"]["notes"])
            self.assertNotIn(" or ", device["physical"]["notes"])
            placement, = device["spatial"]["placements"]
            self.assertEqual(point, (placement["x"], placement["y"]))
            self.assertEqual("effect", placement["role"])
            self.assertEqual("observed", placement["provenance"]["status"])

    def test_neutral_attribution_and_retained_derivation_references(self):
        audit = load_json(curator.AUDIT_SEED)
        guarded = {item["relative_path"]: item["sha256"] for item in audit["retained_artifacts"] if item["environment"] == "PINMAME_REVIEW_ARTIFACTS_ROOT"}
        prefix = curator.MACHINE_ID + "/session-20261029/"
        for path in guarded:
            self.assertTrue(path.startswith(prefix))
            local = path.removeprefix(prefix)
            self.assertTrue(local.startswith(("derivations/", "parent-browser/", "parent-more-photos/")) or local in {"harness", "runtime-observations.json"}, path)
        index = load_json(ROOT / "evidence/excerpts" / curator.MACHINE_ID / "derivations.txt")
        self.assertEqual("PINMAME_REVIEW_ARTIFACTS_ROOT", index["root_environment"])
        self.assertEqual(5, len(index["scripts"]))
        for item in [*index["scripts"], *index["retained_inputs"], index["instructions"]]:
            self.assertTrue(item["path"].startswith(prefix + "derivations/"))
            self.assertNotIn("..", Path(item["path"]).parts)
            self.assertEqual(item["sha256"], guarded[item["path"]])
        for source in self.definition["sources"]:
            for excerpt in source.get("excerpts", []):
                self.assertTrue(excerpt["transcribed_by"].startswith("curator "))
        shared = load_json(ROOT / "controllers/pinmame/gts80b.json")["sources"][0]["locator"]
        self.assertIn("shared evidence", shared)
        self.assertIn("relink every consumer", shared)

    def test_runtime_source_uses_the_actual_license_validation_rule(self):
        index = next(i for i, source in enumerate(self.definition["sources"]) if source["id"] == "runtime.tx-sector")
        runtime = self.definition["sources"][index]
        self.assertEqual("runtime_scenario", runtime["kind"])
        self.assertNotIn("license", runtime)
        self.assertNotIn("attribution", runtime)
        self.assertEqual([], validate_machine(self.definition, ROOT))
        document = copy.deepcopy(self.definition)
        document["sources"][index]["kind"] = "manual"
        errors = validate_machine(document, ROOT)
        for field in ["license", "attribution"]:
            self.assertTrue(any(f"$.sources[{index}].{field}" in error for error in errors))

    def test_partial_gate_rejects_cosmetic_promotion(self):
        self.assertEqual([], validate_machine(self.definition, ROOT))
        promoted = copy.deepcopy(self.definition)
        promoted["coverage"]["status"] = "author_ready"
        promoted["coverage"]["missing"] = []
        promoted["coverage"]["dimensions"] = {k: "validated" for k in promoted["coverage"]["dimensions"]}
        errors = validate_machine(promoted, ROOT)
        self.assertTrue(any("availability" in e for e in errors))
        self.assertTrue(any("spatial" in e for e in errors))
        self.assertEqual([], unresolved_conflicts(self.definition))
        self.assertNotIn("unresolved_conflicts", self.definition["coverage"]["missing"])
        conflict = self.definition["conflicts"][0]
        self.assertEqual("ignored", conflict["status"])
        self.assertIn("Resolution path:", conflict["description"])
        self.assertIn("cannot change the public routing", conflict["rationale"])
        self.assertIn("output_semantics", self.definition["coverage"]["missing"])
        self.assertIn("polarity", self.definition["coverage"]["missing"])
        with patch.object(curator, "load_json", return_value=promoted):
            with self.assertRaisesRegex(ValueError, "cannot authorize promotion"):
                curator.build()

    def test_committed_replay_scenarios_match_the_recorded_raw_run_pins(self):
        summary = load_json(ROOT / "evidence/excerpts" / curator.MACHINE_ID / "runtime-observations.txt")
        scenarios = ROOT / "tools/harness-scenarios/gts80/tx-sector-1988"
        retained = {row["name"]: row for row in summary["runs"]}
        expected = {
            "tx-sector-service-sweep.json": retained["service-sweep"]["scenario_sha256"],
            "tx-sector-gameplay-probe.json": retained["gameplay-probe"]["scenario_sha256"],
        }
        self.assertEqual(set(expected), {path.name for path in scenarios.glob("*.json")})
        for filename, digest in expected.items():
            self.assertEqual(digest, curator.digest(scenarios / filename))

    def test_curator_is_deterministic_and_refuses_incomplete_inventory(self):
        self.assertEqual(curator.PARTIAL.read_bytes(), canonical_bytes(curator.build()))
        first = curator.artifacts()
        self.assertEqual(first, curator.artifacts())
        for path, expected in first.items():
            self.assertEqual(expected, path.read_bytes(), str(path))
        incomplete = copy.deepcopy(self.definition)
        incomplete["inputs"] = [d for d in incomplete["inputs"] if d["binding"] != {"group": "pinmame.input.switch", "device": 0}]
        with patch.object(curator, "load_json", return_value=incomplete):
            with self.assertRaisesRegex(ValueError, "Incomplete controller address inventory"):
                curator.build()

    def test_excerpt_and_external_guards_reject_missing_or_changed_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file = root / "fact.txt"
            file.write_bytes(b"actual fact\n")
            digest = curator.digest(file)
            definition = {"sources": [{"excerpts": [{"path": "fact.txt", "sha256": digest}]}]}
            with patch.object(curator, "ROOT", root):
                curator.verify_excerpts(definition)
                file.write_bytes(b"100 tokens truncated\n")
                truncated = {"sources": [{"excerpts": [{"path": "fact.txt", "sha256": curator.digest(file)}]}]}
                with self.assertRaisesRegex(ValueError, "Truncated source excerpt"):
                    curator.verify_excerpts(truncated)
                file.write_bytes(b"changed\n")
                with self.assertRaisesRegex(ValueError, "changed excerpt"):
                    curator.verify_excerpts(definition)
                file.unlink()
                with self.assertRaisesRegex(ValueError, "Missing"):
                    curator.verify_excerpts(definition)
            artifact = {"environment": "TX_TEST_EVIDENCE", "relative_path": "fact.txt", "sha256": digest}
            with patch.dict(os.environ, {"TX_TEST_EVIDENCE": str(root)}):
                with self.assertRaisesRegex(ValueError, "Missing retained"):
                    curator.verify_external({"retained_artifacts": [artifact]})
                file.write_bytes(b"wrong root bytes\n")
                with self.assertRaisesRegex(ValueError, "Changed retained"):
                    curator.verify_external({"retained_artifacts": [artifact]})
                manifest = write_manifest(root, "txsector")
                directory = {"environment": "TX_TEST_EVIDENCE", "relative_path": ".", "sha256": manifest, "directory_manifest": True}
                curator.verify_external({"retained_artifacts": [directory]})
                file.write_bytes(b"manifest drift\n")
                with self.assertRaisesRegex(ValueError, "manifest content is stale"):
                    curator.verify_external({"retained_artifacts": [directory]})

    def test_check_refuses_drift_and_regeneration_refuses_ready_artifact(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file = root / "canonical.txt"
            file.write_bytes(b"drift\n")
            ready = root / "ready.json"
            with patch.object(curator, "READY", ready), patch.object(curator, "artifacts", return_value={file: b"expected\n"}), patch.object(sys, "argv", ["curator", "--check"]):
                with self.assertRaisesRegex(ValueError, "Curator drift"):
                    curator.main()
                self.assertEqual(b"drift\n", file.read_bytes())
            ready.write_bytes(b"promoted\n")
            with patch.object(curator, "READY", ready), patch.object(sys, "argv", ["curator", "--regenerate"]):
                with self.assertRaisesRegex(ValueError, "author-ready artifact"):
                    curator.main()
                self.assertEqual(b"promoted\n", ready.read_bytes())

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not configured")
    def test_retained_extraction_manifest_and_coordinates(self):
        curator.verify_external(load_json(curator.AUDIT_SEED))
        extracted = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "gottlieb/tx-sector-1988/full-extraction-vpxtool"
        names = {}
        for file in (extracted / "gameitems").glob("*.json"):
            body = next(iter(load_json(file).values()))
            names[body.get("name", "").lower()] = body
        for device in self.definition["inputs"] + self.definition["outputs"]:
            for placement in device.get("spatial", {}).get("placements", []):
                if "spatial.tx-sector" not in placement["provenance"]["source_refs"]:
                    continue
                body = names[placement["id"].rsplit(".", 1)[-1].lower()]
                point = body.get("center") or body.get("position")
                if point is None:
                    points = body["drag_points"]
                    point = {axis: sum(p[axis] for p in points) / len(points) for axis in ("x", "y")}
                self.assertEqual(round(point["x"] / 1000, 6), placement["x"])
                self.assertEqual(round(point["y"] / 2000, 6), placement["y"])

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not configured")
    def test_newer_mesh_observations_recompute_without_promoting_socket_identity(self):
        items = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "gottlieb/tx-sector-1988/newer-sg1bson-1-1/full-extraction-vpxtool/gameitems"
        evidence = load_json(ROOT / "evidence/excerpts" / curator.MACHINE_ID / "newer-socket-meshes.txt")
        self.assertEqual(16, len(evidence["items"]))
        matches = []
        for row in evidence["items"]:
            object_path, mesh_path = items / row["json"], items / row["obj"]
            self.assertEqual(row["json_sha256"], curator.digest(object_path))
            self.assertEqual(row["obj_sha256"], curator.digest(mesh_path))
            primitive = load_json(object_path)["Primitive"]
            self.assertFalse(any(primitive["rot_and_tra"]))
            vertices = [[float(v) for v in line.split()[1:4]] for line in mesh_path.read_text().splitlines() if line.startswith("v ")]
            center = []
            for axis, extent in enumerate("xyz"):
                low, high = min(v[axis] for v in vertices), max(v[axis] for v in vertices)
                center.append(primitive["position"][extent] + primitive["size"][extent] * (low + high) / 2)
            self.assertEqual([round(center[0] / 952, 6), round(center[1] / 1974, 6)], row["normalized_xy"])
            if row["nearby_bound_ramp_light"]:
                match = row["nearby_bound_ramp_light"]
                self.assertLess(match["distance"], 0.003)
                matches.append((match["address"], match["light"]))
        self.assertEqual(15, len(set(matches)))
        sources = {source["id"]: source for source in self.definition["sources"]}
        self.assertFalse(sources["newer-vpx.tx-sector"]["known_working"])
        self.assertEqual("partial", self.definition["coverage"]["status"])

    @unittest.skipUnless(all(os.environ.get(name) for name in ["PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"]), "retained derivation roots not configured")
    def test_portable_derivations_reproduce_retained_values(self):
        review = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
        work = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).parent
        session = review / curator.MACHINE_ID / "session-20261029"
        derivations = session / "derivations"
        index = load_json(ROOT / "evidence/excerpts" / curator.MACHINE_ID / "derivations.txt")
        for item in [*index["scripts"], *index["retained_inputs"], index["instructions"]]:
            self.assertEqual(item["sha256"], curator.digest(review / item["path"]))

        def relocated(value):
            if isinstance(value, dict):
                return {key: relocated(item) for key, item in value.items()}
            if isinstance(value, list):
                return [relocated(item) for item in value]
            if isinstance(value, str) and (value.startswith("/") or len(value) > 2 and value[1] == ":"):
                posix = value.replace("\\", "/")
                for marker in ["/vpx-sources/", "/manuals/", "/review-artifacts/"]:
                    if marker in posix:
                        return marker + posix.split(marker, 1)[1]
            return value

        with tempfile.TemporaryDirectory(prefix="reproduction-", dir=derivations) as temporary:
            output = Path(temporary)
            commands = [
                ["photo/fit_photo.py", "--output-root", str(output / "photo")],
                ["photo/create_pixel_reads.py", "--photo-root", str(session / "parent-more-photos"), "--output-root", str(output / "photo")],
                ["spatial/map_candidates.py", "--working-root", str(work), "--repository-root", str(ROOT), "--photo-root", str(session / "parent-browser"), "--output-root", str(output / "spatial")],
                ["newer-comparison/compare.py", "--working-root", str(work), "--repository-root", str(ROOT), "--output-root", str(output / "newer-comparison")],
                ["newer-comparison/inspect_socket_meshes.py", "--working-root", str(work), "--output-root", str(output / "newer-comparison")],
            ]
            for script, *args in commands:
                completed = subprocess.run([sys.executable, "-B", str(derivations / script), *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120)
                self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            for record in index["output_comparisons"]:
                expected = load_json(review / record["retained_path"])
                actual = load_json(output / record["output"])
                if record["output"] == "newer-comparison/comparison.json":
                    expected["source"]["old_mapping"] = str(derivations / "spatial/inputs/mapping.json")
                self.assertEqual(relocated(expected), relocated(actual), record["output"])

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review root not configured")
    def test_raw_runtime_recomputes_observations_and_hashes(self):
        session = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.MACHINE_ID / "session-20261029"
        summary = load_json(ROOT / "evidence/excerpts" / curator.MACHINE_ID / "runtime-observations.txt")
        for retained in summary["runs"]:
            path = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / retained["raw_run"]
            self.assertEqual(retained["sha256"], curator.digest(path))
            raw = load_json(path)
            self.assertIsNone(raw["failure"])
            self.assertEqual(retained["event_count"], len(raw["events"]))
            for channel in ("lamp", "solenoid"):
                self.assertEqual(retained["observed_" + ("lamps" if channel == "lamp" else "solenoids")], sorted({e["number"] for e in raw["events"] if e["event"] == channel}))
            self.assertEqual(retained["scenario_sha256"], curator.digest(session / retained["scenario"]))

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review root not configured")
    def test_s_routing_excerpt_distinguishes_host_inputs_and_native_outputs(self):
        root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
        excerpt = (ROOT / "evidence/excerpts" / curator.MACHINE_ID / "s-relay-polarity.md").read_text(encoding="utf-8")
        data = json.loads(excerpt.split("```json\n", 1)[1].split("\n```", 1)[0])
        path = root / data["raw_run"]
        self.assertEqual(data["raw_sha256"], curator.digest(path))
        raw = load_json(path)
        self.assertEqual(raw["scenario"]["sha256"], data["scenario_sha256"])
        self.assertEqual(raw["initial_switches"], data["initial_explicit_host_inputs"])
        holes, shared = {45, 55, 65, 75}, {1, 2, 5, 6}
        host = [e for e in raw["events"] if e["event"] == "switch" and e["number"] in holes]
        lamps = [e for e in raw["events"] if e["event"] == "lamp" and e["number"] == 12]
        outputs = [e for e in raw["events"] if e["event"] == "solenoid" and e["number"] in shared]
        self.assertEqual(host, data["host_hole_input_history"])
        self.assertEqual(lamps, data["native_lamp_12_transitions"])
        self.assertEqual(outputs, data["native_shared_solenoid_transitions"])
        self.assertEqual(8, len(host))
        asserted = {e["switch"] for e in raw["initial_switches"] if e["switch"] in holes and e["state"]}
        level, rises = None, []
        for event in raw["events"]:
            if event["event"] == "switch" and event["number"] in holes:
                if event["state"]:
                    asserted.add(event["number"])
                else:
                    asserted.discard(event["number"])
            elif event["event"] == "lamp" and event["number"] == 12:
                level = event["state"]
            elif event["event"] == "solenoid" and event["number"] in shared and event["state"]:
                rises.append({"time_s": event["time_s"], "solenoid": event["number"], "last_native_public_lamp_12_state": level, "host_asserted_hole_inputs": sorted(asserted)})
        self.assertEqual(rises, data["shared_rises_with_recorded_context"])
        self.assertTrue(all(row["last_native_public_lamp_12_state"] == 1 and not row["host_asserted_hole_inputs"] for row in rises[:6]))
        intervals = []
        for index, event in enumerate(lamps):
            if event["state"]:
                continue
            end = next((e["time_s"] for e in lamps[index + 1:] if e["state"]), None)
            intervals.append({"start_s": event["time_s"], "end_s": end, "duration_s": round(end - event["time_s"], 6) if end is not None else None, "native_shared_rises": [r for r in rises if r["time_s"] >= event["time_s"] and (end is None or r["time_s"] < end)]})
        self.assertEqual(intervals, data["native_zero_level_intervals"])
        self.assertEqual([5, 2], [i["native_shared_rises"][0]["solenoid"] for i in intervals if i["end_s"] is not None])
        self.assertIn("Host input/readback is not", (ROOT / self.definition["knowledge"]["path"]).read_text(encoding="utf-8"))
        self.assertIn("Both host release writes precede", excerpt)
        self.assertIn("durations are not emulated or factory timing measurements", excerpt)


if __name__ == "__main__":
    unittest.main()
