"""Fail-closed tests for the seed materializer, independent of retained evidence."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_dr_dude as curator
from build_external_evidence_manifest import write_manifest
from pinmame_game_defs.jsonio import canonical_bytes


def put_json(path: Path, data: dict) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_bytes(canonical_bytes(data))


def fixture(prototype: bool = False) -> dict:
	def device(group: str, address: int) -> dict:
		return {"binding": {"group": group, "device": address}}
	if prototype:
		return {
			"machine": {"id": curator.PROTOTYPE_ID}, "coverage": {"status": "partial"},
			"knowledge": {"path": f"knowledge/bally/{curator.PROTOTYPE}.md"},
			"inputs": [device(curator.SWITCH_GROUP, n) for n in sorted(curator.WPC_SWITCHES)] + [device(curator.DIP_GROUP, n) for n in range(1, 9)],
			"outputs": [device(curator.SOLENOID_GROUP, n) for n in sorted(curator.SOLENOIDS)] + [device(curator.LAMP_GROUP, n) for n in sorted(curator.WPC_MATRIX)] + [device(curator.GI_GROUP, n) for n in range(5)], "sources": [],
		}
	return {
		"machine": {"id": curator.PRODUCTION_ID}, "coverage": {"status": "partial"},
		"knowledge": {"path": f"knowledge/bally/{curator.PRODUCTION}.md"},
		"inputs": [device(curator.SWITCH_GROUP, n) for n in sorted(curator.SWITCHES)] + [device(curator.DIP_GROUP, 0)],
		"outputs": [device(curator.SOLENOID_GROUP, n) for n in sorted(curator.SOLENOIDS)] + [device(curator.LAMP_GROUP, n) for n in sorted(curator.LAMPS)], "sources": [],
	}


def setup(root: Path) -> None:
	for slug, machine_id, is_prototype in ((curator.PRODUCTION, curator.PRODUCTION_ID, False), (curator.PROTOTYPE, curator.PROTOTYPE_ID, True)):
		put_json(root / curator.SEEDS / f"{slug}.json", fixture(is_prototype))
		(root / curator.SEEDS / f"{slug}.md").write_bytes(b"# fixture\r\n")
		put_json(root / curator.SEEDS / f"{slug}-spatial.json", {"format": "pinmame-spatial-blockers", "version": 1,
			"machine_id": machine_id, "markdown": "# fixture report\n"})


class MaterializerTests(unittest.TestCase):
	def test_enumeration_and_duplicate_mutations_fail(self) -> None:
		data = fixture()
		curator._production_contract(data)
		data["inputs"].pop()
		with self.assertRaisesRegex(RuntimeError, "inputs must enumerate"):
			curator._production_contract(data)
		data = fixture()
		data["outputs"].pop()
		with self.assertRaisesRegex(RuntimeError, "outputs must enumerate"):
			curator._production_contract(data)
		data = fixture()
		data["outputs"].append(data["outputs"][0])
		with self.assertRaisesRegex(RuntimeError, "duplicate"):
			curator._production_contract(data)

	def test_prototype_enumeration_rejects_missing_and_extra(self) -> None:
		data = fixture(True)
		curator._prototype_contract(data)
		data["inputs"].pop()
		with self.assertRaisesRegex(RuntimeError, "prototype inputs"):
			curator._prototype_contract(data)
		data = fixture(True)
		data["outputs"].pop()
		with self.assertRaisesRegex(RuntimeError, "prototype outputs"):
			curator._prototype_contract(data)
		data = fixture(True)
		data["outputs"].append({"binding": {"group": curator.LAMP_GROUP, "device": 19}})
		with self.assertRaisesRegex(RuntimeError, "prototype outputs"):
			curator._prototype_contract(data)

	def test_prototype_opposing_status_fails_before_writes(self) -> None:
		with tempfile.TemporaryDirectory() as temp, patch.object(curator, "validate_against_schema", return_value=[]), patch.object(curator, "validate_machine", return_value=[]):
			root = Path(temp)
			setup(root)
			opposing = root / "machines/author-ready/bally" / f"{curator.PROTOTYPE}.json"
			opposing.parent.mkdir(parents=True)
			opposing.write_bytes(b"keep")
			with self.assertRaisesRegex(RuntimeError, "opposing-status"):
				curator.generate(root)
			self.assertEqual(opposing.read_bytes(), b"keep")
			self.assertFalse((root / "machines/partial/bally" / f"{curator.PRODUCTION}.json").exists())

	def test_generation_drift_and_opposing_status(self) -> None:
		with tempfile.TemporaryDirectory() as temp, patch.object(curator, "validate_against_schema", return_value=[]), patch.object(curator, "validate_machine", return_value=[]):
			root = Path(temp)
			setup(root)
			curator.generate(root)
			curator.check(root)
			paths = curator._outputs(root)
			curator.generate(root)
			self.assertTrue(all(path.read_bytes() == data for path, data in paths))
			paths[-1][0].write_text("drift", encoding="utf-8")
			with self.assertRaisesRegex(RuntimeError, "drifted"):
				curator.check(root)
			opposing = root / "machines/author-ready/bally" / f"{curator.PRODUCTION}.json"
			opposing.parent.mkdir(parents=True)
			opposing.write_bytes(b"keep")
			with self.assertRaisesRegex(RuntimeError, "opposing-status"):
				curator.generate(root)
			self.assertEqual(b"keep", opposing.read_bytes())

	def test_report_envelope_and_mandatory_seeds_fail_before_writes(self) -> None:
		with tempfile.TemporaryDirectory() as temp, patch.object(curator, "validate_against_schema", return_value=[]), patch.object(curator, "validate_machine", return_value=[]):
			root = Path(temp)
			setup(root)
			report = json.loads((root / curator.SPATIAL_SEED).read_bytes())
			report["format"] = "pinmame-spatial-audit"
			put_json(root / curator.SPATIAL_SEED, report)
			with self.assertRaisesRegex(RuntimeError, "envelope"):
				curator.generate(root)
			self.assertFalse((root / "machines/partial/bally" / f"{curator.PRODUCTION}.json").exists())
			setup(root)
			for slug in (curator.PRODUCTION, curator.PROTOTYPE):
				for suffix, label in ((".json", "machine seed"), (".md", "knowledge seed"), ("-spatial.json", "spatial seed")):
					setup(root)
					(root / curator.SEEDS / f"{slug}{suffix}").unlink()
					with self.subTest(slug=slug, suffix=suffix), self.assertRaisesRegex(RuntimeError, label):
						curator.generate(root)
					self.assertFalse((root / "machines/partial/bally" / f"{curator.PRODUCTION}.json").exists())
			setup(root)
			wpc_report = root / curator.SEEDS / f"{curator.PROTOTYPE}-spatial.json"
			data = json.loads(wpc_report.read_bytes())
			data["machine_id"] = curator.PRODUCTION_ID
			put_json(wpc_report, data)
			with self.assertRaisesRegex(RuntimeError, "envelope"):
				curator.generate(root)


	def test_excerpt_hash_and_path_safety(self) -> None:
		with tempfile.TemporaryDirectory() as temp:
			root = Path(temp)
			path = root / "evidence/excerpts/fixture/file.md"
			path.parent.mkdir(parents=True)
			path.write_bytes(b"fixture")
			data = {"sources": [{"excerpts": [{"path": "evidence/excerpts/fixture/file.md", "sha256": hashlib.sha256(b"fixture").hexdigest()}]}]}
			curator._excerpts(data, root)
			path.write_bytes(b"changed")
			with self.assertRaisesRegex(RuntimeError, "drift"):
				curator._excerpts(data, root)
			for value in ("../escape", "/absolute", "a/../escape", "C:/escape", "a\\b"):
				with self.subTest(value=value), self.assertRaises(RuntimeError):
					curator._safe_path(root, value)

	def test_retained_manifest_rechecks_content_counts_and_roots(self) -> None:
		with tempfile.TemporaryDirectory() as temp:
			root = Path(temp)
			vpx, manuals, review = (root / name for name in ("vpx", "manuals", "review"))
			for path in (vpx, manuals, review):
				path.mkdir()
			extract = vpx / "extraction"
			extract.mkdir()
			(extract / "script.vbs").write_bytes(b"original")
			digest = write_manifest(extract, "dd_l2")
			(manuals / "manual.pdf").write_bytes(b"manual")
			register = {"files": [{"root": "manuals", "path": "manual.pdf", "size": 6,
				"sha256": hashlib.sha256(b"manual").hexdigest()}], "extraction": {"root": "vpx",
				"path": "extraction", "game": "dd_l2", "manifest_sha256": digest, "file_count": 1, "total_bytes": 8}}
			put_json(root / curator.EVIDENCE_REGISTER, register)
			curator.verify_retained(vpx, manuals, review, root=root)
			with self.assertRaisesRegex(RuntimeError, "review root"):
				curator.verify_retained(vpx, manuals, None, root=root)
			register["extraction"]["file_count"] = 2
			put_json(root / curator.EVIDENCE_REGISTER, register)
			with self.assertRaisesRegex(RuntimeError, "file count"):
				curator.verify_retained(vpx, manuals, review, root=root)
			register["extraction"]["file_count"] = 1
			put_json(root / curator.EVIDENCE_REGISTER, register)
			(extract / "script.vbs").write_bytes(b"changed!")
			with self.assertRaisesRegex(RuntimeError, "manifest verification failed"):
				curator.verify_retained(vpx, manuals, review, root=root)
			# A newly regenerated, self-consistent manifest must not defeat the original pin.
			write_manifest(extract, "dd_l2")
			with self.assertRaisesRegex(RuntimeError, "digest, file count, or total bytes drifted"):
				curator.verify_retained(vpx, manuals, review, root=root)

	def test_retained_runtime_manifest_checks_raw_trace_bytes(self) -> None:
		with tempfile.TemporaryDirectory() as temp:
			root = Path(temp)
			vpx, manuals, review = (root / name for name in ("vpx", "manuals", "review"))
			for directory in (vpx, manuals, review):
				directory.mkdir()
			extract = vpx / "extraction"
			extract.mkdir()
			(extract / "script.vbs").write_bytes(b"original")
			digest = write_manifest(extract, "dd_l2")
			(review / "trace.json").write_bytes(b"raw trace")
			write_manifest(review, "dd_l2")
			manifest = review / "manifest.json"
			register = {"files": [{"root": "review", "path": "manifest.json", "size": manifest.stat().st_size,
				"sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()}], "extraction": {"root": "vpx",
				"path": "extraction", "game": "dd_l2", "manifest_sha256": digest, "file_count": 1, "total_bytes": 8}}
			put_json(root / curator.EVIDENCE_REGISTER, register)
			curator.verify_retained(vpx, manuals, review, root=root)
			(review / "trace.json").write_bytes(b"changed raw trace")
			with self.assertRaisesRegex(RuntimeError, "bundle manifest verification failed"):
				curator.verify_retained(vpx, manuals, review, root=root)

def by_binding(definition: dict, collection: str, group: str, address: int) -> dict:
	return next(item for item in definition[collection] if item["binding"]["group"] == group and item["binding"]["device"] == address)


class CuratedSeedTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.prod = curator._json(ROOT / curator.SEEDS / f"{curator.PRODUCTION}.json", "production seed")
		cls.wpc = curator._json(ROOT / curator.SEEDS / f"{curator.PROTOTYPE}.json", "prototype seed")
		cls.report = curator._json(ROOT / curator.SPATIAL_SEED, "production spatial seed")

	def test_both_generated_artifact_sets_are_deterministic_and_checked(self) -> None:
		curator.check(ROOT)
		curator.check(ROOT)
		self.assertEqual(8, len(curator._outputs(ROOT)))
		for definition in (self.prod, self.wpc):
			curator._excerpts(definition, ROOT)
			self.assertTrue(any(source.get("excerpts") for source in definition["sources"]))

	def test_identity_and_driver_split(self) -> None:
		p = {x["id"] for x in self.prod["drivers"]}
		w = {x["id"] for x in self.wpc["drivers"]}
		self.assertEqual({"dd_l2", "dd_lu1", "dd_l3c", "dd_p6"}, p)
		self.assertEqual({"dd_p06", "dd_p7"}, w)
		self.assertFalse(p & w)
		self.assertEqual(curator.PRODUCTION_ID, self.prod["machine"]["id"])
		self.assertEqual(curator.PROTOTYPE_ID, self.wpc["machine"]["id"])
		a, b = self.prod["machine"].get("opdb_id"), self.wpc["machine"].get("opdb_id")
		self.assertFalse(a is not None and a == b)
		self.assertIsNone(b)
		self.assertEqual("partial", self.prod["coverage"]["status"])
		self.assertEqual({"spatial_placement", "variant_differences"}, set(self.prod["coverage"]["missing"]))
		self.assertEqual("partial", self.wpc["coverage"]["status"])
		self.assertTrue({"spatial_placement", "output_semantics", "identity"} <= set(self.wpc["coverage"]["missing"]))

	def test_mechanism_inventory_displays_and_readable_utf8(self) -> None:
		expected = {"trough", "shooter", "left-popper", "right-popper", "drop-bank", "magnet", "mixmaster", "big-shot"}
		for definition, slug in ((self.prod, curator.PRODUCTION), (self.wpc, curator.PROTOTYPE)):
			mechanisms = {m["id"]: m for m in definition["mechanisms"]}
			self.assertEqual({f"mechanism.{name}" for name in expected}, set(mechanisms))
			self.assertEqual([], mechanisms["mechanism.shooter"]["actuators"])
			self.assertEqual(4, len(mechanisms["mechanism.drop-bank"]["sensors"]))
			mixer = mechanisms["mechanism.mixmaster"]
			self.assertEqual(9, sum(sensor.startswith("switch.mixer-") for sensor in mixer["sensors"]))
			self.assertEqual(["coil.motor"], mixer["actuators"])
			self.assertEqual([(0, 0, 16), (1, 20, 16)], [(d["controller_index"], d["segment_start"], d["width"]) for d in definition["displays"]])
			knowledge = (ROOT / curator.SEEDS / f"{slug}.md").read_text(encoding="utf-8")
			self.assertNotIn("\ufffd", knowledge, "replacement characters hide source text")
			self.assertNotIn("\u00e2\u20ac", knowledge, "UTF-8 must not be decoded as Windows-1252")
			self.assertNotIn("\ufffd", json.dumps(definition, ensure_ascii=False))
			self.assertEqual(knowledge.encode("utf-8"), (ROOT / definition["knowledge"]["path"]).read_bytes())

	def test_addresses_and_controller_routing(self) -> None:
		curator._production_contract(self.prod)
		curator._prototype_contract(self.wpc)
		for definition, mapping in ((self.prod, ((82, 57), (84, 58))), (self.wpc, ((112, 81), (114, 82)))):
			pairs = {(r["source"], r["destination"]) for r in definition["relationships"] if r["kind"] == "direct"}
			for source, destination in mapping:
				a = by_binding(definition, "inputs", curator.SWITCH_GROUP, source)
				b = by_binding(definition, "inputs", curator.SWITCH_GROUP, destination)
				self.assertIn((a["id"], b["id"]), pairs)
		self.assertEqual("virtual", by_binding(self.prod, "inputs", curator.SWITCH_GROUP, 2)["kind"])
		self.assertEqual("used", by_binding(self.prod, "inputs", curator.SWITCH_GROUP, 2)["availability"])
		for number, kind in ((10, "gi"), (12, "relay"), (23, "virtual"), (49, "virtual")):
			output = by_binding(self.prod, "outputs", curator.SOLENOID_GROUP, number)
			self.assertEqual(kind, output["kind"])
			self.assertEqual("used", output["availability"])
		for number in (82, 84):
			self.assertEqual(f"switch.flipper-column-{number}", by_binding(self.prod, "inputs", curator.SWITCH_GROUP, number)["id"])
		for number in (29, 30, 31):
			output = by_binding(self.wpc, "outputs", curator.SOLENOID_GROUP, number)
			self.assertEqual("used", output["availability"])
			self.assertIn("internal.wpc-state", output["roles"])
		zero = by_binding(self.wpc, "outputs", curator.SOLENOID_GROUP, 32)
		self.assertEqual("unused", zero["availability"])
		self.assertEqual(["internal.unused.wpc-output"], zero["roles"])
		self.assertEqual("virtual", zero["spatial"]["reason"])
		self.assertIn("zero", zero["physical"]["notes"].lower())

	def test_physical_counts_and_spatial_guardrails(self) -> None:
		for definition in (self.prod, self.wpc):
			identifiers = {device["id"] for device in definition["inputs"]}
			self.assertTrue({"switch.big-shot-target", "switch.magnet-target"} <= identifiers)
			self.assertFalse({"switch.big-shot", "switch.magnet"} & identifiers)
		for n in (22, 23, 24):
			self.assertEqual(1, by_binding(self.prod, "outputs", curator.LAMP_GROUP, n)["physical"]["quantity"])
		self.assertEqual(2, by_binding(self.prod, "outputs", curator.LAMP_GROUP, 40)["physical"]["quantity"])
		for n in (25, 26, 27):
			device = by_binding(self.prod, "outputs", curator.SOLENOID_GROUP, n)
			self.assertEqual(2, device["physical"]["quantity"])
			self.assertFalse(device.get("spatial", {}).get("placements", []))
			self.assertFalse(any(r["binding"] == device["binding"] for r in self.report["records"]))
		gi = by_binding(self.prod, "outputs", curator.SOLENOID_GROUP, 10)
		self.assertNotIn("quantity", gi["physical"])
		self.assertEqual("candidate", gi["spatial"]["status"])
		self.assertEqual(32, len(gi["spatial"]["placements"]))
		for group, n in ((curator.SWITCH_GROUP, 52), (curator.SOLENOID_GROUP, 17)):
			coll = "inputs" if group == curator.SWITCH_GROUP else "outputs"
			placement = by_binding(self.prod, coll, group, n)["spatial"]["placements"][0]
			self.assertEqual((0.238406, 0.138642), (placement["x"], placement["y"]))
		for n, operator in ((19, "right"), (20, "left")):
			device = by_binding(self.prod, "inputs", curator.SWITCH_GROUP, n)
			x = device["spatial"]["placements"][0]["x"]
			self.assertTrue(x > 0.5 if operator == "right" else x < 0.5)
			self.assertIn("defect", device["physical"]["notes"].lower())

	def test_retained_evidence_and_coordinate_recomputation(self) -> None:
		names = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
		values = [os.environ.get(name) for name in names]
		if not any(values):
			self.skipTest("external evidence roots not configured")
		self.assertTrue(all(values), "all three evidence roots are required when any is configured")
		vpx, manuals, review = (Path(value) for value in values)
		curator.verify_retained(vpx, manuals, review, root=ROOT)
		register = curator._json(ROOT / curator.EVIDENCE_REGISTER, "register")
		entries = {(x["root"], x["path"]): x for x in register["files"]}
		for source_id, suffix in (("runtime.dr-dude.s11", "/runtime/summary.json"), ("runtime.dr-dude.wpc", "/runtime-wpc/summary.json")):
			matches = [entry for (root, path), entry in entries.items() if root == "review" and path.endswith(suffix)]
			self.assertEqual(1, len(matches), f"register must pin {source_id}")
			source = next(x for d in (self.prod, self.wpc) for x in d["sources"] if x["id"] == source_id)
			self.assertEqual(source["sha256"], matches[0]["sha256"])
			summary = json.loads(curator._safe_path(review, matches[0]["path"]).read_text(encoding="utf-8"))
			self.assertTrue(all(summary["comparisons"].values()))
		extract = curator._safe_path(vpx, register["extraction"]["path"])
		bounds = json.loads((extract / "gamedata.json").read_text(encoding="utf-8"))
		from pinmame_game_defs.spatial import _round_point
		for group, number in ((curator.SWITCH_GROUP, 52), (curator.SOLENOID_GROUP, 17), (curator.SWITCH_GROUP, 19), (curator.SWITCH_GROUP, 20)):
			record = next(r for r in self.report["records"] if r["binding"] == {"group": group, "device": number})
			item = json.loads(curator._safe_path(extract, record["item_file"]).read_text(encoding="utf-8"))
			center = next(iter(item.values()))["center"]
			self.assertEqual((record["raw_x"], record["raw_y"]), (center["x"], center["y"]))
			device = by_binding(self.prod, "inputs" if group == curator.SWITCH_GROUP else "outputs", group, number)
			placement = next(p for p in device["spatial"]["placements"] if p["id"] == record["placement_id"])
			self.assertEqual(placement["x"], _round_point((center["x"] - bounds["left"]) / (bounds["right"] - bounds["left"])))
			self.assertEqual(placement["y"], _round_point((center["y"] - bounds["top"]) / (bounds["bottom"] - bounds["top"])))
		obj_entry = next(entry for (root, path), entry in entries.items() if root == "vpx" and path.lower().endswith(".obj"))
		record = next(r for r in self.report["records"] if r["object"].lower() == "primguy" and r["coordinate_method"] == "exported_OBJ_world_mesh_AABB_center")
		vertices = []
		inside = False
		with curator._safe_path(vpx, obj_entry["path"]).open(encoding="utf-8") as stream:
			for line in stream:
				if line.startswith("o "):
					if inside:
						break
					inside = line[2:].strip().lower() == record["object"].lower()
				elif inside and line.startswith("v "):
					values = line.split()
					vertices.append((float(values[1]), float(values[2])))
		self.assertTrue(vertices)
		self.assertAlmostEqual(record["raw_x"], (min(v[0] for v in vertices) + max(v[0] for v in vertices)) / 2)
		self.assertAlmostEqual(record["raw_y"], (min(v[1] for v in vertices) + max(v[1] for v in vertices)) / 2)


	def test_runtime_summaries_recomputed_from_raw_traces(self) -> None:
		"""Compare derived observations, not host switch readback or physical fitment."""
		names = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
		values = [os.environ.get(name) for name in names]
		if not any(values):
			self.skipTest("external evidence roots not configured")
		self.assertTrue(all(values), "all three evidence roots are required when any is configured")
		import diner_runtime_evidence as system11
		import funhouse_runtime_evidence as wpc

		base = Path(values[2]) / "bally.dr-dude-and-his-excellent-ray.1990/session-20261029"

		def load_summary(directory: str, definition: dict, source_id: str) -> dict:
			path = base / directory / "summary.json"
			source = next(s for s in definition["sources"] if s["id"] == source_id)
			self.assertEqual(source["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
			return json.loads(path.read_text(encoding="utf-8"))

		def raw(directory: str, entry: dict, game: str, library_sha256: str) -> dict:
			path = curator._safe_path(base / directory, entry["trace"])
			data = path.read_bytes()
			self.assertEqual(entry["trace_sha256"], hashlib.sha256(data).hexdigest())
			run = json.loads(data)
			self.assertEqual(game, run["game"])
			self.assertIsNone(run["failure"])
			self.assertEqual(library_sha256, run["library_sha256"])
			return run

		summary = load_summary("runtime", self.prod, "runtime.dr-dude.s11")
		for game in ("dd_l2", "dd_p6"):
			runs = summary["runs"][game]["runs"]
			for kind, decode in (("switch", system11.switch_levels), ("lamp", system11.single_lamps), ("coil", system11.coil_test)):
				with self.subTest(game=game, kind=kind):
					trace = raw("runtime", runs[kind], game, summary["library_sha256"])
					derived = decode(trace)
					self.assertEqual(runs[kind]["steps"], derived)
					if kind == "coil":
						self.assertEqual(runs[kind]["relay_12_held_on_addresses"], system11.relay_held(trace, derived))

		prototype = load_summary("runtime-wpc", self.wpc, "runtime.dr-dude.wpc")
		for game in ("dd_p06", "dd_p7"):
			runs = prototype["runs"][game]["runs"]
			for kind in ("switch", "lamp"):
				with self.subTest(game=game, kind=kind):
					trace = raw("runtime-wpc", runs[kind], game, prototype["library_sha256"])
					self.assertEqual(64, len(runs[kind]["steps"]))
					for expected in runs[kind]["steps"]:
						n = expected["address"] if kind == "switch" else expected["test_step"]
						label = f"hold switch {n} (held)" if kind == "switch" else ("first lamp" if n == 1 else f"Start step {n}")
						snapshot, = [item for item in trace["snapshots"] if item["label"] == label]
						displays = {item["index"]: item for item in snapshot["displays"]}
						rows = [wpc._fold(wpc.decode(displays[i]["segments"])) for i in (0, 1)]
						if kind == "switch":
							self.assertEqual(expected["rows"], rows, f"{game} switch {n}")
						else:
							self.assertEqual(expected["display"], rows[0], f"{game} lamp {n}")
							# Ignore a transition from the previous lamp during the step;
							# the final half-second is the stable sampled lamp.
							end = snapshot["time_s"]
							lit = sorted({e["number"] for e in trace["events"] if e["event"] == "lamp" and e["state"] == 1 and end - 0.5 <= e["time_s"] <= end})
							self.assertEqual(expected["transitioned_lamps"], lit, f"{game} lamp {n}")

			coil = runs["coil"]
			trace = raw("runtime-wpc", coil, game, prototype["library_sha256"])
			frames = []
			for event in trace["events"]:
				if event["event"] == "display" and event.get("index") == 0:
					try:
						frames.append((event["time_s"], wpc._fold(wpc.decode(event["segments"]))))
					except ValueError:
						pass  # Intermediate multiplex frames may not form valid characters.
			rises = [(e["number"], e["time_s"]) for e in trace["events"] if e["event"] == "solenoid" and e["state"] == 1]
			self.assertEqual(2, len(coil["coil_cycles"]))
			self.assertEqual(coil["coil_cycles"][0], coil["coil_cycles"][1])
			for step in coil["coil_cycles"][0]:
				if step["display"] == "NOT USED":
					continue  # A named unused step need not produce a callback.
				matches = [t for address, t in rises if address == step["address"] and any(abs(t - at) <= 0.12 and text == step["display"] for at, text in frames)]
				self.assertGreaterEqual(len(matches), 2, f"{game} coil {step}")
			self.assertEqual(set(range(5)), {event["address"] for event in coil["gi_off_events"]})
			for event in coil["gi_off_events"]:
				self.assertTrue(any(e["event"] == "gi" and e["number"] == event["address"] and e["state"] == 0 and e["time_s"] == event["time_s"] for e in trace["events"]))
				self.assertEqual(event["display"], [text for at, text in frames if at <= event["time_s"] + 0.12][-1])
			for event in coil["output_28_named_steps"]:
				self.assertIn((28, event["time_s"]), rises)
				self.assertTrue(any(abs(event["time_s"] - at) <= 0.12 and text == event["display"] for at, text in frames))


if __name__ == "__main__":
	unittest.main()
