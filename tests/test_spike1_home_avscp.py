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
		self.definition = load_json(ROOT / "machines/partial/stern/avengers-the-pin-2013.json")

	def test_own_physical_identity_exact_root_and_honest_partial(self):
		d = self.definition
		self.assertEqual("stern.avengers-the-pin.2013", d["machine"]["id"])
		self.assertEqual("Gxv3q-MXrBj", d["machine"]["opdb_id"])
		self.assertEqual(6373, d["machine"]["ipdb_id"])
		self.assertEqual(["avscp_103"], [r["id"] for r in d["drivers"]])
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
		self.assertEqual(set(range(1,65)), set(groups["pinmame.output.lamp"]))
		self.assertTrue(all(len(v)==len(set(v)) for v in groups.values()))
		game_on=next(x for x in self.definition["outputs"] if x["id"]=="virtual.game-on")
		self.assertEqual({"group":"pinmame.output.solenoid","device":33},game_on["binding"])
		self.assertEqual("virtual",game_on["kind"])

	def test_reproduction_layout_and_all_portable_digests(self):
		d=self.definition
		self.assertEqual([{'id': 'display.alphanumeric', 'label': 'Public 16-character alphanumeric line', 'kind': 'segment', 'controller_index': 0, 'width': 16, 'height': 1, 'provenance': {'status': 'observed', 'source_refs': ['avscp_103.source.driver']}, 'segment_start': 0}],d["displays"])
		curate_spike1.check("avscp_103",ROOT)
		curate_spike1.check("avscp_103",ROOT)
		self.assertEqual(canonical_bytes(d),(ROOT/"tools/seeds/stern/spike1/avscp_103.json").read_bytes())
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


if __name__ == "__main__":
	unittest.main()
