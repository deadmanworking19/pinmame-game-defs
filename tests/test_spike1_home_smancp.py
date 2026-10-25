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
		self.assertFalse(any(s["kind"] in {"rom_static_analysis", "runtime_scenario", "vpx_table", "vpx_script"} for s in d["sources"]))
		self.assertEqual([], validate_against_schema(d, ROOT / "schemas/machine.schema.json", "home model"))

	def test_full_current_source_envelopes_do_not_claim_fitment(self):
		groups = {}
		for device in self.definition["inputs"] + self.definition["outputs"]:
			groups.setdefault(device["binding"]["group"], []).append(device["binding"]["device"])
			self.assertNotIn("normally_closed", device)
			self.assertNotIn("initial_active", device)
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

	def test_manual_blank_rows_and_combined_drivers_are_not_shifted(self):
		d=self.definition
		outputs={(x["binding"]["group"],x["binding"]["device"]):x for x in d["outputs"]}
		coils={n:x for (g,n),x in outputs.items() if g=="pinmame.output.solenoid"}
		self.assertEqual("Left/Right Pop Bumper",coils[7]["label"])
		self.assertEqual("unknown",coils[6]["availability"])
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
