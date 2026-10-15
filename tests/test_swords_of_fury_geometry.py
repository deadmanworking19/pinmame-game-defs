"""Recompute every seeded anchor from the exact retained extraction."""
import json
import os
import unittest
from pathlib import Path

from pinmame_game_defs.spatial import extract_spatial_candidates

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "optional retained VPX root is absent")
class SwordsOfFuryGeometryTests(unittest.TestCase):
	def test_all_anchors_recompute_from_gameitems_not_from_the_transcription(self):
		base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams/swords-of-fury-1988/primary"
		candidates = extract_spatial_candidates(base / "extracted", base / "Swords of Fury (Williams 1988).vpx", "git:v0.33.3")
		objects = {item["name"].casefold(): item for item in candidates["objects"]}
		definition = json.loads((ROOT / "tools/seeds/williams/swords-of-fury-1988.json").read_bytes())
		checked = 0
		for device in definition["inputs"] + definition["outputs"]:
			for point in device.get("spatial", {}).get("placements", []):
				with self.subTest(placement=point["id"]):
					name = point["id"].split(".")[-1]
					obj = objects[name]
					self.assertEqual((obj["x"], obj["y"]), (point["x"], point["y"]))
					checked += 1
		self.assertGreater(checked, 60)
