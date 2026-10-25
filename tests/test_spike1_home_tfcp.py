from __future__ import annotations

import hashlib
import os
from pathlib import Path
import sys
import unittest

from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.schema_validation import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_spike1


class HomeModelFactsTests(unittest.TestCase):
	def setUp(self):
		self.definition = load_json(ROOT / "machines/partial/stern/transformers-the-pin-2012.json")

	def test_own_physical_identity_exact_root_and_honest_partial(self):
		d = self.definition
		self.assertEqual("stern.transformers-the-pin.2012", d["machine"]["id"])
		self.assertEqual("Grd2o-MQK8Z", d["machine"]["opdb_id"])
		self.assertEqual(5861, d["machine"]["ipdb_id"])
		self.assertEqual(["tfcp_1018"], [r["id"] for r in d["drivers"]])
		self.assertNotIn("clone_of", d["drivers"][0])
		self.assertEqual("unknown", d["drivers"][0]["physical_compatibility"])
		self.assertEqual("partial", d["coverage"]["status"])
		self.assertTrue({"spatial_placement", "polarity", "mechanism_behavior", "output_semantics"} <= set(d["coverage"]["missing"]))
		self.assertFalse(any(s["kind"] in {"vpx_table", "vpx_script"} for s in d["sources"]))
		self.assertEqual({"tfcp_1018.rom.map"}, {s["id"] for s in d["sources"] if s["kind"] == "rom_static_analysis"})
		self.assertEqual({"tfcp_1018.runtime.bounded"}, {s["id"] for s in d["sources"] if s["kind"] == "runtime_scenario"})
		self.assertEqual([], validate_against_schema(d, ROOT / "schemas/machine.schema.json", "home model"))

	def test_full_current_source_envelopes_do_not_claim_fitment(self):
		groups = {}
		for device in self.definition["inputs"] + self.definition["outputs"]:
			groups.setdefault(device["binding"]["group"], []).append(device["binding"]["device"])
			self.assertNotIn("normally_closed", device)
			if "initial_active" in device:
				self.assertEqual("pinmame.input.switch",device["binding"]["group"])
				self.assertIn(device["binding"]["device"],{26,27,28})
				self.assertIs(True,device["initial_active"])
			self.assertNotIn("quantity", device.get("physical", {}))
			self.assertNotIn("placements", device.get("spatial", {}))
		self.assertEqual(set(range(96)) | set(range(101,133)), set(groups["pinmame.input.switch"]))
		self.assertEqual(set(range(1,9)), set(groups["pinmame.input.dip"]))
		self.assertEqual(set(range(1,34)) | set(range(45,49)) | set(range(51,73)), set(groups["pinmame.output.solenoid"]))
		self.assertEqual(set(range(1,65)), set(groups["pinmame.output.lamp"]))
		self.assertTrue(all(len(v)==len(set(v)) for v in groups.values()))
		game_on=next(x for x in self.definition["outputs"] if x["id"]=="virtual.game-on")
		self.assertEqual({"group":"pinmame.output.solenoid","device":33},game_on["binding"])
		self.assertEqual("virtual",game_on["kind"])
		self.assertEqual({26,27,28},{x["binding"]["device"] for x in self.definition["inputs"] if "initial_active" in x})

	def test_exact_elg_rows_and_source_generated_lamp_names(self):
		facts=load_json(ROOT/"evidence/excerpts/stern.transformers-the-pin.2012/rom-routing.json.txt")
		self.assertEqual((46,8,64),(len(facts["switches"]["rows"]),len(facts["coils"]["rows"]),len(facts["leds"]["rows"])))
		self.assertEqual(64,facts["controller"]["padded_lamp_limit"])
		self.assertNotIn("raw_tables",facts)
		for key,collection,group in [("switches","inputs","pinmame.input.switch"),("coils","outputs","pinmame.output.solenoid"),("leds","outputs","pinmame.output.lamp")]:
			rows=facts[key]
			namespace="pinmame.label" if key=="leds" else "rom.label"
			self.assertEqual("pinmame_source_synthesized" if key=="leds" else "firmware_string",rows["name_origin"])
			devices={x["binding"]["device"]:x for x in self.definition[collection] if x["binding"]["group"]==group}
			for raw in rows["rows"]:
				row=dict(zip(rows["columns"],raw))
				self.assertIn({"namespace":namespace,"value":row["name"]},devices[row["public_address"]]["aliases"])
				if key=="leds":
					self.assertFalse(any(a["namespace"]=="rom.label" for a in devices[row["public_address"]]["aliases"]))
					self.assertEqual("unknown",devices[row["public_address"]]["availability"])
		coils={r[0]:r[1] for r in facts["coils"]["rows"]}
		self.assertEqual("POP BUMPER - BOTTOM & RIGHT",coils[6])
		self.assertEqual("POP BUMPER - TOP",coils[7])
		for device in self.definition["outputs"]:
			if device["binding"]["group"]=="pinmame.output.solenoid" and device["binding"]["device"] not in set(range(1,9))|{33,45,46,47,48}:
				self.assertEqual(("virtual","unused"),(device["kind"],device["availability"]))

	def test_bounded_runtime_requires_causal_actual_outputs(self):
		run=load_json(ROOT/"evidence/excerpts/stern.transformers-the-pin.2012/runtime-bounded.json.txt")
		self.assertEqual(0,run["exit_code"])
		self.assertIsNone(run["failure"])
		self.assertEqual(11,len(run["steps"]))
		self.assertEqual("8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5",run["library_sha256"])
		for step,switch,coil,states in [(1,1,4,[127,0]),(6,2,2,[255,44,0]),(7,3,3,[255,44,0]),(8,6,1,[255,0]),(9,7,7,[255,0]),(10,8,6,[255,0])]:
			s=run["steps"][step-1]
			self.assertEqual(switch,s["switch"])
			self.assertEqual([{"number":coil,"states":states}],s["matched_outputs"])
		self.assertIn({"number":33,"states":[255]},run["steps"][0]["solenoid_transitions"])
		self.assertEqual(0,run["stop_states"][-1])
		self.assertGreater(run["segment_frame_count"],0)
		self.assertTrue(any("NVRAM" in text for text in run["limitations"]))

	def test_reproduction_layout_and_all_portable_digests(self):
		d=self.definition
		self.assertEqual([{'id': 'display.alphanumeric', 'label': 'Public 16-character alphanumeric line', 'kind': 'segment', 'controller_index': 0, 'width': 16, 'height': 1, 'provenance': {'status': 'observed', 'source_refs': ['tfcp_1018.source.driver']}, 'segment_start': 0}],d["displays"])
		curate_spike1.check("tfcp_1018",ROOT)
		curate_spike1.check("tfcp_1018",ROOT)
		self.assertEqual(canonical_bytes(d),(ROOT/"tools/seeds/stern/spike1/tfcp_1018.json").read_bytes())
		for source in d["sources"]:
			for excerpt in source.get("excerpts",[]):
				self.assertEqual(excerpt["sha256"],hashlib.sha256((ROOT/excerpt["path"]).read_bytes()).hexdigest())

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"),"Retained evidence root is optional")
	def test_exact_retained_source_and_identity_artifacts(self):
		working=Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve().parent
		for source in self.definition["sources"]:
			self.assertTrue(source["uri"].startswith("working-root:"))
			path=(working/source["uri"].removeprefix("working-root:")).resolve()
			self.assertTrue(path.is_relative_to(working))
			self.assertEqual(source["sha256"],hashlib.sha256(path.read_bytes()).hexdigest())
		facts=load_json(ROOT/"evidence/excerpts/stern.transformers-the-pin.2012/rom-routing.json.txt")
		self.assertEqual(facts["retained_full_facts_sha256"],hashlib.sha256((working/"review-artifacts/spike1-refresh-2026-10-25/home-games/tfcp-rom-routing.json").read_bytes()).hexdigest())
		sys.path.insert(0,str(ROOT/"tools"))
		from build_external_evidence_manifest import check_manifest
		run=load_json(ROOT/"evidence/excerpts/stern.transformers-the-pin.2012/runtime-bounded.json.txt")
		self.assertEqual(run["manifest_sha256"],check_manifest(working/Path(run["manifest_path"]).parent,"tfcp_1018"))
		acq=load_json(ROOT/"evidence/excerpts/stern.transformers-the-pin.2012/official-rom-acquisition.json.txt")
		self.assertEqual(289,acq["zip_member_count"])
		self.assertEqual(acq["zip_sha256"],hashlib.sha256((working/"roms/spike1/tfcp_1018.zip").read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
