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
		self.definition = load_json(ROOT / "machines/partial/stern/spider-man-the-pin-2016.json")

	def test_own_physical_identity_exact_root_and_honest_partial(self):
		d = self.definition
		self.assertEqual("stern.spider-man-the-pin.2016", d["machine"]["id"])
		self.assertEqual("G2Ld3-MnKE5", d["machine"]["opdb_id"])
		self.assertEqual(6438, d["machine"]["ipdb_id"])
		self.assertEqual(["smancp_101"], [r["id"] for r in d["drivers"]])
		self.assertNotIn("clone_of", d["drivers"][0])
		self.assertEqual("unknown", d["drivers"][0]["physical_compatibility"])
		self.assertEqual("partial", d["coverage"]["status"])
		self.assertTrue({"spatial_placement", "polarity", "mechanism_behavior", "output_semantics"} <= set(d["coverage"]["missing"]))
		self.assertFalse(any(s["kind"] in {"vpx_table", "vpx_script"} for s in d["sources"]))
		self.assertEqual({"smancp_101.rom.map"},{s["id"] for s in d["sources"] if s["kind"]=="rom_static_analysis"})
		self.assertEqual({"smancp_101.runtime.bounded"},{s["id"] for s in d["sources"] if s["kind"]=="runtime_scenario"})
		self.assertEqual([], validate_against_schema(d, ROOT / "schemas/machine.schema.json", "home model"))

	def test_full_current_source_envelopes_do_not_claim_fitment(self):
		groups = {}
		for device in self.definition["inputs"] + self.definition["outputs"]:
			groups.setdefault(device["binding"]["group"], []).append(device["binding"]["device"])
			self.assertNotIn("normally_closed", device)
			if "initial_active" in device:
				self.assertEqual("pinmame.input.switch",device["binding"]["group"])
				self.assertIn(device["binding"]["device"],{18,19,20,21,33,49,116})
				self.assertIs(True,device["initial_active"])
			self.assertNotIn("quantity", device.get("physical", {}))
			self.assertNotIn("placements", device.get("spatial", {}))
		self.assertEqual(set(range(96)) | set(range(101,133)), set(groups["pinmame.input.switch"]))
		self.assertEqual(set(range(1,9)), set(groups["pinmame.input.dip"]))
		self.assertEqual(set(range(1,34)) | set(range(45,49)) | set(range(51,73)), set(groups["pinmame.output.solenoid"]))
		self.assertEqual(set(range(1,137)), set(groups["pinmame.output.lamp"]))
		self.assertTrue(all(len(v)==len(set(v)) for v in groups.values()))
		game_on=next(x for x in self.definition["outputs"] if x["id"]=="virtual.game-on")
		self.assertEqual({"group":"pinmame.output.solenoid","device":33},game_on["binding"])
		self.assertEqual("virtual",game_on["kind"])
		self.assertEqual({18,19,20,21,33,49,116},{x["binding"]["device"] for x in self.definition["inputs"] if x.get("initial_active")})

	def test_exact_firmware_rows_and_own_manual_node_positions(self):
		facts=load_json(ROOT/"evidence/excerpts/stern.spider-man-the-pin.2016/rom-routing.json.txt")
		self.assertEqual({"switches":58,"coils":12,"leds":65},facts["validation"]["counts"])
		self.assertTrue(facts["validation"]["elf_and_current_loader_rows_match"])
		self.assertTrue(facts["validation"]["all_rows_use_rom_manual_numbers"])
		self.assertTrue(facts["manual_reconciliation"]["all_existing_manual_node_addresses_match_exact_firmware"])
		self.assertTrue(all(r["matched"] for r in facts["manual_reconciliation"]["rows"]))
		self.assertEqual(4,facts["validation"]["installed_balls_from_source_loader"])
		self.assertEqual(136,facts["controller"]["padded_lamp_limit"])
		self.assertEqual(53,facts["controller"]["nSolenoids"])
		devices={(x["binding"]["group"],x["binding"]["device"]):x for x in self.definition["inputs"]+self.definition["outputs"]}
		for section,group in [("switches","pinmame.input.switch"),("coils","pinmame.output.solenoid"),("leds","pinmame.output.lamp")]:
			for values in facts[section]["rows"]:
				row=dict(zip(facts[section]["columns"],values))
				self.assertEqual("firmware_string",row["name_origin"])
				self.assertIn({"namespace":"rom.label","value":row["name"]},devices[group,row["public_address"]]["aliases"])
		coils={dict(zip(facts["coils"]["columns"],r))["public_address"]:dict(zip(facts["coils"]["columns"],r)) for r in facts["coils"]["rows"]}
		self.assertEqual({51:"COIN METER",52:"TICKET METER",53:"TICKET DISPENSER"},{n:coils[n]["name"] for n in (51,52,53)})
		self.assertEqual([33,34,35],[coils[n]["reference"] for n in (51,52,53)])
		for n in (51,52,53):self.assertEqual("unknown",devices["pinmame.output.solenoid",n]["availability"])
		for n in (1,2,3):
			lamp=devices["pinmame.output.lamp",n]
			self.assertEqual(2,len([a for a in lamp["aliases"] if a["namespace"]=="rom.label"]))
			self.assertIn("modulated level",lamp["physical"]["notes"])
		self.assertEqual(62,len({dict(zip(facts["leds"]["columns"],r))["public_address"] for r in facts["leds"]["rows"]}))

	def test_fresh_runtime_requires_actual_outputs_and_rgb_frames(self):
		run=load_json(ROOT/"evidence/excerpts/stern.spider-man-the-pin.2016/runtime-bounded.json.txt")
		self.assertEqual(0,run["exit_code"])
		self.assertIsNone(run["failure"])
		self.assertEqual(11,len(run["steps"]))
		for step,switch,coil,level in [(1,13,1,210),(4,15,2,255),(6,8,3,255),(7,10,4,255),(8,6,5,194),(9,37,7,235),(10,38,8,255)]:
			s=run["steps"][step-1]
			self.assertEqual(switch,s["switch"])
			self.assertEqual(coil,s["matched_outputs"][0]["number"])
			self.assertIn(level,s["matched_outputs"][0]["states"])
			self.assertIn(0,s["matched_outputs"][0]["states"])
		self.assertIn({"number":33,"states":[255]},run["steps"][0]["solenoid_transitions"])
		self.assertEqual([255,30,0],run["steps"][5]["matched_outputs"][0]["states"])
		self.assertEqual(0,run["stop_states"][-1])
		layout=run["display_callbacks"][0]
		self.assertEqual((0,15,64,32,24),(layout["index"],layout["type"],layout["width"],layout["height"],layout["depth"]))
		self.assertGreater(run["video_summary"]["0"]["changed_frames"],0)
		self.assertEqual({},run["dmd_summary"])
		self.assertTrue(any("NVRAM" in text for text in run["limitations"]))

	def test_reproduction_layout_and_all_portable_digests(self):
		d=self.definition
		self.assertEqual([{'id': 'display.rgb-matrix', 'label': 'Public 64x32 RGB matrix layout', 'kind': 'video', 'controller_index': 0, 'width': 64, 'height': 32, 'provenance': {'status': 'observed', 'source_refs': ['smancp_101.source.driver']}}],d["displays"])
		curate_spike1.check("smancp_101",ROOT)
		curate_spike1.check("smancp_101",ROOT)
		self.assertEqual(canonical_bytes(d),(ROOT/"tools/seeds/stern/spike1/smancp_101.json").read_bytes())
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
		acq=load_json(ROOT/"evidence/excerpts/stern.spider-man-the-pin.2016/rom-acquisition.json.txt")
		self.assertEqual("0c5c51f509475a64fbbed6997fccad738c0c024facac81261af1ffce8f112c28",acq["archive_sha256"])
		self.assertEqual(9,len(acq["members"]))
		import zipfile
		import zlib
		with zipfile.ZipFile(working/acq["archive"]) as archive:
			self.assertEqual({r["name"] for r in acq["members"]},set(archive.namelist()))
			for member in acq["members"]:
				payload=archive.read(member["name"])
				self.assertEqual(member["size"],len(payload))
				self.assertEqual(member["crc32"],f"{zlib.crc32(payload):08x}")
				self.assertEqual(member["sha1"],hashlib.sha1(payload).hexdigest())
				self.assertEqual(member["sha256"],hashlib.sha256(payload).hexdigest())
		from build_external_evidence_manifest import check_manifest
		run=load_json(ROOT/"evidence/excerpts/stern.spider-man-the-pin.2016/runtime-bounded.json.txt")
		self.assertEqual(run["provenance"]["manifest"]["sha256"],check_manifest(working/Path(run["provenance"]["manifest"]["path"]).parent,"smancp_101"))

	def test_manual_blank_rows_and_combined_drivers_are_not_shifted(self):
		d=self.definition
		outputs={(x["binding"]["group"],x["binding"]["device"]):x for x in d["outputs"]}
		coils={n:x for (g,n),x in outputs.items() if g=="pinmame.output.solenoid"}
		self.assertEqual("Left/Right Pop Bumper",coils[7]["label"])
		self.assertEqual(("virtual","unused"),(coils[6]["kind"],coils[6]["availability"]))
		self.assertEqual("090-5044-ND",coils[7]["physical"]["part_number"])
		self.assertEqual("ORG BLK",coils[7]["wiring"]["drive_wire"])
		self.assertEqual("flasher",outputs["pinmame.output.lamp",76]["kind"])
		self.assertTrue(all(outputs["pinmame.output.lamp",n]["kind"]=="gi" for n in (80,81,82)))
		self.assertEqual("unknown",outputs["pinmame.output.lamp",130]["availability"])
		trough=next(x for x in d["mechanisms"] if x["id"]=="mech.trough")
		self.assertEqual([f"sw.{n}" for n in range(16,23)],trough["sensors"])
		switches={x["binding"]["device"]:x for x in d["inputs"] if x["binding"]["group"]=="pinmame.input.switch"}
		self.assertEqual("leaf",switches[9]["physical"]["switch_type"])
		self.assertEqual("virtual",switches[9]["kind"])
		self.assertEqual("opto",switches[40]["physical"]["switch_type"])
		for filename in ("switches-page15","switches-page17","drivers","lamps-page18","lamps-page20"):
			text=(ROOT/f"evidence/excerpts/stern.spider-man-the-pin.2016/manual-{filename}.md").read_text(encoding="utf-8")
			self.assertIn("BLANK",text)
			self.assertIn("every column",text)


if __name__ == "__main__":
	unittest.main()
