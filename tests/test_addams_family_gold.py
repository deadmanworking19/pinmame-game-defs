from __future__ import annotations

import copy
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_addams_family_gold as curator
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json
from pinmame_game_defs.validation import validate_machine


def sibling_claims(value: object, catalog: dict) -> set[str]:
	"""Check compound machine/ROM identifiers without flagging words like 'real'."""
	forbidden = ({v["id"] for v in catalog["machines"]} | {v["id"] for v in catalog["drivers"]}) - curator.DRIVERS - {curator.MACHINE_ID}
	tokens = {v.lower() for v in re.findall(r"\b[a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)+\b", json.dumps(value))}
	return tokens & forbidden


class GoldDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.d = curator.build()
		cls.e = curator.evidence_seed()

	def test_utf8_sensitive_prose_survives_generation_and_source_hash_checks(self) -> None:
		mechanism = next(v for v in self.d["mechanisms"] if v["id"] == "mechanism.bookcase")
		for text in ("53\u201356", "0\u20131", "89\u201390"):
			self.assertIn(text, mechanism["behavior"])
		flasher = next(v for v in self.d["outputs"] if v["id"] == "device.telephone-upper-right-ramp-flasher")
		self.assertIn("19\u201321", flasher["physical"]["notes"])
		payloads = curator.artifacts()
		paths = {curator.SEED_PATH, curator.EVIDENCE_PATH, *payloads}
		paths.update(Path(excerpt["path"]) for source in self.d["sources"] for excerpt in source.get("excerpts", []))
		for path in paths:
			with self.subTest(path=path):
				raw = (ROOT / path).read_bytes()
				text = raw.decode("utf-8", "strict")
				self.assertFalse(any(marker in text for marker in curator.MOJIBAKE_MARKERS))
				if path in payloads:
					self.assertEqual(payloads[path], raw)
		self.assertEqual(curator.SEED_SHA256, file_sha256(ROOT / curator.SEED_PATH))
		self.assertEqual(curator.EVIDENCE_SHA256, file_sha256(ROOT / curator.EVIDENCE_PATH))
		self.assertEqual((ROOT / curator.SEED_PATH).read_bytes(), (ROOT / curator.DEFINITION_PATH).read_bytes())
		for target in ("mechanism", "flasher"):
			changed = copy.deepcopy(self.d)
			if target == "mechanism":
				item = next(v for v in changed["mechanisms"] if v["id"] == "mechanism.bookcase")
				item["behavior"] = item["behavior"].replace("\u2013", "\u00e2\u20ac\u201c")
			else:
				item = next(v for v in changed["outputs"] if v["id"] == "device.telephone-upper-right-ramp-flasher")
				item["physical"]["notes"] = item["physical"]["notes"].replace("\u2013", "\u00e2\u20ac\u201c")
			with self.assertRaisesRegex(ValueError, "UTF-8 prose"):
				curator.assert_reviewed_contract(changed)

	def test_exact_gold_identity_driver_ownership_and_complete_contract(self) -> None:
		d = self.d
		self.assertEqual("bally.the-addams-family-gold.1994", d["machine"]["id"])
		self.assertEqual(21, d["machine"]["ipdb_id"])
		self.assertEqual("50038", d["machine"]["model_number"])
		self.assertEqual(curator.DRIVERS, {v["id"] for v in d["drivers"]})
		self.assertEqual("author_ready", d["coverage"]["status"])
		self.assertEqual([], d["coverage"]["missing"])
		self.assertEqual("complete", d["knowledge"]["status"])
		self.assertFalse((ROOT / curator.PARTIAL_PATH).exists())
		self.assertEqual([], validate_machine(d, ROOT))
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claims = copy.deepcopy(d)
		# Two explicit shared-geometry sources may identify their source
		# machine and runtime solely to locate their own physical objects.
		claims["sources"] = [v for v in claims["sources"] if v["id"] not in {"vpx.geometry.shared.g5k-2-3-2", "vpx-script.geometry.shared.g5k-2-3-2"}]
		self.assertFalse(sibling_claims(claims, catalog))
		for text in (curator.knowledge(d), curator.spatial_report(d, self.e)):
			self.assertFalse(sibling_claims(text, catalog))
		original = next(v["id"] for v in catalog["machines"] if v["id"] == "bally.the-addams-family.1992")
		claims["mechanisms"][0]["behavior"] += " Machine: " + original
		self.assertEqual({original}, sibling_claims(claims, catalog))

	def test_gold_construction_and_virtual_channels_are_not_copied_from_original(self) -> None:
		s = curator.bindings(self.d, "inputs", "pinmame.input.switch")
		c = curator.bindings(self.d, "outputs", "pinmame.output.solenoid")
		l = curator.bindings(self.d, "outputs", "pinmame.output.lamp")
		self.assertEqual("20-9663-9", s[11]["physical"]["part_number"])
		self.assertEqual(2, s[21]["physical"]["quantity"])
		self.assertEqual("A-16908/A-16909", s[57]["physical"]["assembly_part_number"])
		self.assertEqual("AE-27-1200", c[26]["physical"]["part_number"])
		self.assertEqual("cabinet", c[2]["physical"]["location"])
		self.assertEqual(("used", "virtual"), (c[49]["availability"], c[49]["kind"]))
		self.assertEqual(("unused", "lamp"), (l[41]["availability"], l[41]["kind"]))
		self.assertEqual("unused", l[41]["spatial"]["reason"])
		for a in (81, 82):
			self.assertEqual("microswitch", s[a]["physical"]["switch_type"])
		for a in (84, 85):
			self.assertEqual("opto", s[a]["physical"]["switch_type"])
		for a in (112, 114, 116, 118):
			self.assertEqual("opto", s[a]["physical"]["switch_type"])
			self.assertFalse(s[a]["normally_closed"])
		for a in curator.MATRIX - curator.UNUSED_SWITCHES - {24}:
			self.assertEqual(a in curator.OPTOS, s[a]["normally_closed"])

	def test_each_physical_bulb_is_counted_and_located_in_its_own_space(self) -> None:
		c = curator.bindings(self.d, "outputs", "pinmame.output.solenoid")
		l = curator.bindings(self.d, "outputs", "pinmame.output.lamp")
		g = curator.bindings(self.d, "outputs", "pinmame.output.gi")
		for a in (13, 26):
			self.assertEqual(2, l[a]["physical"]["quantity"])
			self.assertEqual(2, len(l[a]["spatial"]["placements"]))
		for a, total in {17: 2, 18: 2, 19: 3, 20: 2, 21: 2, 22: 4}.items():
			self.assertEqual(total, c[a]["physical"]["quantity"])
			self.assertEqual(total if a != 22 else 1, len(c[a]["spatial"]["placements"]))
		for a in range(81, 89):
			self.assertEqual("cabinet_or_service", l[a]["spatial"]["reason"])
		self.assertEqual([15, 15, 15, 10], [g[a]["physical"]["quantity"] for a in (0, 1, 2, 4)])
		self.assertEqual([15, 8], [len(g[a]["spatial"]["placements"]) for a in (0, 4)])
		self.assertEqual("unused", g[3]["availability"])
		for v in self.d["outputs"]:
			if v["kind"] in {"lamp", "flasher", "gi"}:
				for source in self.e["spatial_candidates"].get(v["id"], []):
					self.assertIs(True, source["physical_emitter"])

	def test_raw_geometry_pixels_and_quantities_reproduce_without_external_files(self) -> None:
		curator.reconcile_spatial(self.d, self.e)
		for v in self.d["inputs"] + self.d["outputs"]:
			for p, source in zip(v["spatial"].get("placements", []), self.e["spatial_candidates"].get(v["id"], [])):
				x, y = curator.source_xy(source, self.e)
				self.assertEqual((p["x"], p["y"]), (round(x, 6), round(y, 6)))
				self.assertTrue(0 <= x <= 1 and 0 <= y <= 1)
		for s in self.d["sources"]:
			for excerpt in s.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], file_sha256(ROOT / excerpt["path"]))
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], file_sha256(ROOT / excerpt["image"]))

	def test_functional_trough_contacts_are_separate_disclosed_projections(self) -> None:
		s = curator.bindings(self.d, "inputs", "pinmame.input.switch")
		positions = []
		for a in (15, 16, 17):
			p = s[a]["spatial"]["placements"][0]
			positions.append((p["x"], p["y"]))
			self.assertTrue(self.e["spatial_candidates"][s[a]["id"]][0]["projection"])
		self.assertEqual(3, len(set(positions)))
		self.assertLess(positions[0][0], positions[1][0])
		self.assertLess(positions[1][0], positions[2][0])

	def test_phone_projection_is_explicit_and_cannot_turn_into_a_helper_coordinate(self) -> None:
		g = curator.bindings(self.d, "outputs", "pinmame.output.gi")[4]
		source = self.e["spatial_candidates"][g["id"]][-1]
		self.assertEqual("stock-socket-envelope-to-own-mount", source["projection_class"])
		self.assertTrue(source["projection"])
		self.assertEqual(0.125, curator.phone_projection_uncertainty(source, self.e))
		self.assertFalse(source["observed_glass_centre"])
		self.assertEqual((0.936675, 0.105180), tuple(g["spatial"]["placements"][-1][k] for k in ("x", "y")))
		self.assertEqual([2580, 561], source["photo_identity_controls"]["photo235"]["own_flat_rivet"])
		self.assertIn("manufacturer.socket.cec4087-3", g["spatial"]["placements"][-1]["provenance"]["source_refs"])
		for key, value in {"object": "GI40", "bounds": [[828, 317, -197], [829, 318, -196]], "projection_class": "photographed-bulb-to-adjacent-fixed-edge", "observed_glass_centre": True, "normalized_uncertainty": 0.025}.items():
			with self.subTest(key=key):
				changed = copy.deepcopy(source); changed[key] = value
				with self.assertRaises(ValueError): curator.source_xy(changed, self.e)
		for key, value in {"assembly_part_number": "A-12336-1", "dimensioned_replacement": "077-5030-00", "original_manufacturing_dimensions_claimed": True, "pose_scope": ["stock_above_plate"], "model_glass_bounds": [[0, 0, 0], [1, 1, 1]], "socket_inches": {}, "mount_xy": [876.2725, 253.4988]}.items():
			with self.subTest(template_key=key):
				changed = copy.deepcopy(source); changed["socket_template"][key] = value
				with self.assertRaises(ValueError): curator.source_xy(changed, self.e)
		changed = copy.deepcopy(self.d)
		curator.bindings(changed, "outputs", "pinmame.output.gi")[4]["spatial"]["placements"][-1]["provenance"]["source_refs"].remove("manufacturer.socket.cec4087-3")
		with self.assertRaises(ValueError): curator.reconcile_spatial(changed, self.e)

	def test_phone_scale_crosscheck_uses_raw_operands_and_both_source_roles(self) -> None:
		source = self.e["spatial_candidates"]["gi.string-5"][-1]
		metrics = curator.phone_projection_metrics(source, self.e)
		for expected, actual in zip([12.516, 21.406, 57.28], metrics["extents_mm"]):
			self.assertAlmostEqual(expected, actual)
		self.assertAlmostEqual(62.416868649428416, metrics["radius_mm"])
		self.assertAlmostEqual((1 + 1 / 16) * 25.4, metrics["ball_mm"])
		self.assertAlmostEqual(18.405197 / 10.3, metrics["mesh_vpu_per_mm"])
		self.assertAlmostEqual(50 / 26.9875, metrics["ball_vpu_per_mm"])
		self.assertGreater(metrics["ball_vpu_per_mm"], metrics["mesh_vpu_per_mm"])
		self.assertEqual(max(metrics["mesh_vpu_per_mm"], metrics["ball_vpu_per_mm"]), metrics["selected_vpu_per_mm"])
		self.assertAlmostEqual(0.0029813331452308574, metrics["mount_disagreement"])
		self.assertAlmostEqual(0.12432926406138085, metrics["raw_normalized_uncertainty"])
		self.assertAlmostEqual(metrics["radius_mm"] * metrics["selected_vpu_per_mm"] / 952.965 + metrics["mount_disagreement"], metrics["raw_normalized_uncertainty"])
		for key, value in {"selection": "mesh_only", "ball_diameter_inches": 27 / 25.4, "vpx_ball_diameter": 49,
			"physical_source_ref": "manual.parts.socket-family", "physical_locator": "unsourced cabinet width",
			"script_source_ref": "vpx-script.gold.sliderpoint-1-4-1", "script_locator": "changelog",
			"exact_global_cad_scale_claimed": True}.items():
			with self.subTest(key=key):
				changed = copy.deepcopy(source); changed["socket_template"]["scale_calibration"][key] = value
				with self.assertRaises(ValueError): curator.phone_projection_uncertainty(changed, self.e)
		for ref in ("parts.gold.ipdb", "vpx-script.geometry.shared.vpw-2-4-41"):
			changed = copy.deepcopy(self.d)
			curator.bindings(changed, "outputs", "pinmame.output.gi")[4]["spatial"]["placements"][-1]["provenance"]["source_refs"].remove(ref)
			with self.assertRaises(ValueError): curator.reconcile_spatial(changed, self.e)

	def test_unused_gold_lamps_do_not_invent_fitted_bulbs(self) -> None:
		lamps = curator.bindings(self.d, "outputs", "pinmame.output.lamp")
		self.assertEqual({41, 76}, {a for a, v in lamps.items() if v["availability"] == "unused"})
		for address in (41, 76):
			self.assertNotIn("quantity", lamps[address]["physical"])
			self.assertEqual("unused", lamps[address]["spatial"]["reason"])
			self.assertIn("Not Used", lamps[address]["physical"]["notes"])
			changed = copy.deepcopy(self.d)
			curator.bindings(changed, "outputs", "pinmame.output.lamp")[address]["physical"]["quantity"] = 1
			with self.assertRaises(ValueError): curator.assert_reviewed_contract(changed)

	def test_contract_guards_reject_the_actual_historical_errors(self) -> None:
		cases = [
			("edition", lambda d: d["machine"].update(year=1992)),
			("model", lambda d: d["machine"].update(model_number="20017")),
			("partial", lambda d: d["coverage"].update(status="partial")),
			("missing", lambda d: d["coverage"].update(missing=["spatial_placement"])),
			("knowledge", lambda d: d["knowledge"].update(status="partial")),
			("dimension", lambda d: d["coverage"]["dimensions"].update(spatial_placement="observed")),
			("driver", lambda d: d["drivers"].pop()),
			("duplicate driver", lambda d: d["drivers"].append(copy.deepcopy(d["drivers"][0]))),
			("duplicate input", lambda d: d["inputs"].append(copy.deepcopy(d["inputs"][0]))),
			("missing output", lambda d: d["outputs"].pop()),
			("switch namespace", lambda d: d["inputs"][0]["binding"].update(device=999)),
			("unvalidated device", lambda d: d["inputs"][0]["provenance"].update(status="observed")),
			("unknown device", lambda d: d["inputs"][0].update(availability="unknown")),
			("observed spatial", lambda d: curator.bindings(d, "inputs", "pinmame.input.switch")[31]["spatial"].update(status="observed")),
			("observed placement", lambda d: curator.bindings(d, "inputs", "pinmame.input.switch")[31]["spatial"]["placements"][0]["provenance"].update(status="observed")),
			("compatibility", lambda d: d["drivers"][0].update(physical_compatibility="unknown")),
			("source", lambda d: d["sources"][0].update(sha256="0" * 64)),
			("generation", lambda d: d["controller"].update(hardware_generation="0x80000")),
		]
		for name, mutate in cases:
			with self.subTest(name=name):
				d = copy.deepcopy(self.d); mutate(d)
				with self.assertRaises(ValueError): curator.assert_reviewed_contract(d)
		device_cases = [
			("inputs", "pinmame.input.switch", 11, "availability", "unused"),
			("inputs", "pinmame.input.switch", 53, "normally_closed", False),
			("inputs", "pinmame.input.switch", 112, "normally_closed", True),
			("outputs", "pinmame.output.solenoid", 49, "availability", "unused"),
			("outputs", "pinmame.output.lamp", 41, "kind", "virtual"),
			("outputs", "pinmame.output.lamp", 41, "availability", "used"),
		]
		for collection, group, address, key, value in device_cases:
			with self.subTest(group=group, address=address):
				d = copy.deepcopy(self.d); curator.bindings(d, collection, group)[address][key] = value
				with self.assertRaises(ValueError): curator.assert_reviewed_contract(d)
		physical_cases = [
			("inputs", "pinmame.input.switch", 21, "quantity", 1),
			("inputs", "pinmame.input.switch", 57, "assembly_part_number", "A-14231/A-14232"),
			("inputs", "pinmame.input.switch", 81, "switch_type", "opto"),
			("outputs", "pinmame.output.solenoid", 2, "location", "under playfield"),
			("outputs", "pinmame.output.solenoid", 26, "part_number", "AE-30-2000"),
			("outputs", "pinmame.output.solenoid", 19, "quantity", 2),
			("outputs", "pinmame.output.solenoid", 22, "quantity", 1),
			("outputs", "pinmame.output.lamp", 13, "quantity", 1),
			("outputs", "pinmame.output.gi", 4, "quantity", 7),
		]
		for collection, group, address, key, value in physical_cases:
			with self.subTest(group=group, address=address, key=key):
				d = copy.deepcopy(self.d); curator.bindings(d, collection, group)[address]["physical"][key] = value
				with self.assertRaises(ValueError): curator.assert_reviewed_contract(d)
		for group, address in (("pinmame.output.gi", 4), ("pinmame.output.lamp", 13)):
			d = copy.deepcopy(self.d)
			placements = curator.bindings(d, "outputs", group)[address]["spatial"]["placements"]
			placements[1].update(x=placements[0]["x"], y=placements[0]["y"])
			with self.assertRaises(ValueError): curator.assert_reviewed_contract(d)

	def test_geometry_guards_reject_missing_bulbs_helpers_drift_and_false_hull_claims(self) -> None:
		for name in ("gap", "missing anchor", "helper", "coordinate", "false hull", "bad second figure", "missing controls", "short controls", "missing secondary"):
			with self.subTest(name=name):
				d, e = copy.deepcopy(self.d), copy.deepcopy(self.e)
				measured = next((v, i, s) for v in d["outputs"] for i, s in enumerate(e["spatial_candidates"].get(v["id"], [])) if "pixel" in s and not s["inside_control_hull"])
				v, i, source = measured
				if name == "gap": e["remaining_research"] = ["missing phone bulb"]
				elif name == "missing anchor": e["spatial_candidates"][v["id"]].pop()
				elif name == "helper": source["physical_emitter"] = False
				elif name == "coordinate": v["spatial"]["placements"][i]["x"] += .01
				elif name == "false hull": source["inside_control_hull"] = True
				elif name == "missing controls": e["coordinate_fits"][source["fit_key"]]["controls"] = []
				elif name == "short controls":
					for c in e["coordinate_fits"][source["fit_key"]]["controls"]: c["xy"][1] = .4
				elif name == "missing secondary": source.pop("secondary_check")
				else: source["secondary_check"]["pixel"] = [0, 0]
				with self.assertRaises(ValueError): curator.reconcile_spatial(d, e)

	def test_curator_check_is_deterministic_and_external_roots_fail_closed(self) -> None:
		self.assertEqual(curator.SEED_SHA256, file_sha256(ROOT / curator.SEED_PATH))
		self.assertEqual(curator.EVIDENCE_SHA256, file_sha256(ROOT / curator.EVIDENCE_PATH))
		self.assertEqual((ROOT / curator.SEED_PATH).read_bytes(), (ROOT / curator.DEFINITION_PATH).read_bytes())
		self.assertEqual(canonical_bytes(self.d), canonical_bytes(curator.build()))
		curator.check(); curator.check()
		with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": str(ROOT / "definitely-missing-gold-evidence")}, clear=False):
			with self.assertRaises(ValueError): curator.verify_external()

	def test_check_and_regeneration_refuse_changed_artifacts_and_unknown_partial(self) -> None:
		with tempfile.TemporaryDirectory(prefix="gold-curator-") as tmp:
			root = Path(tmp)
			for directory in ("schemas", "controllers"):
				shutil.copytree(ROOT / directory, root / directory)
			shutil.copytree(ROOT / "evidence/excerpts/bally.the-addams-family-gold.1994", root / "evidence/excerpts/bally.the-addams-family-gold.1994")
			for path in (curator.SEED_PATH, curator.EVIDENCE_PATH, curator.KNOWLEDGE_PATH):
				(root / path).parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(ROOT / path, root / path)
			with patch.dict(os.environ, {}, clear=True):
				curator.generate(root)
				curator.check(root)
				knowledge = root / curator.KNOWLEDGE_PATH
				knowledge.write_text("drift\n", encoding="utf-8")
				with self.assertRaises(ValueError): curator.check(root)
				definition = root / curator.DEFINITION_PATH
				definition.write_text("{}\n", encoding="utf-8")
				with self.assertRaises(ValueError): curator.generate(root)
				definition.unlink()
				partial = root / curator.PARTIAL_PATH
				partial.parent.mkdir(parents=True, exist_ok=True)
				partial.write_text("{}\n", encoding="utf-8")
				with self.assertRaises(ValueError): curator.generate(root)

	def test_pinned_seeds_and_existing_wrong_external_bytes_fail_closed(self) -> None:
		with tempfile.TemporaryDirectory(prefix="gold-corrupt-") as tmp:
			root = Path(tmp)
			for relative, check in ((curator.SEED_PATH, curator.build), (curator.EVIDENCE_PATH, curator.evidence_seed)):
				path = root / relative; path.parent.mkdir(parents=True, exist_ok=True)
				path.write_text("{}\n", encoding="utf-8")
				with self.assertRaises(ValueError): check(root)
			source = next(s for s in self.d["sources"] if s["id"] == "vpx.gold.sliderpoint-1-4-1")
			path = root / source["uri"].split("/", 1)[1]
			path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(b"wrong VPX bytes")
			with patch.dict(os.environ, {"PINMAME_VPX_SOURCES_ROOT": str(root)}, clear=True):
				with self.assertRaises(ValueError): curator.verify_external()


if __name__ == "__main__":
	unittest.main()
