from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from champion_pub_mech_probe import dmd_checkpoints


# Seven native pixel rows from visually inspected English cp_16 DMD frames,
# independent of the reader's glyph dictionary. The surrounding frame is blank.
MAIN_MENU = (
	"4438384400447c444400000000000000", "6c441044006c40444400000000000000",
	"54441064005440644400000000000000", "547c1054005478544400000000000000",
	"4444104c0044404c4400000000000000", "44441044004440444400000000000000",
	"4444384400447c443800000000000000",
)
SWITCH_EDGES = (
	"100000080003d139f3d101f78e7cf000", "10000008000411104411010451410000",
	"10000008000411104411010450410000", "fffffffe00039510441f01e45078e000",
	"10381c08000055104411010453401000", "54aa550a00005b104411010451401000",
	"10381c080007913843d101f78f7de000",
)
RIGHT_JAB = (
	"1000000801e38e45f00139e01139e7c0", "1000000801111144400145101b451400",
	"10000008011110444001451015451400", "fffffffe01e1107c40017de0157d1780",
	"10381c08014113444001451011451400", "54aa550a012111444011451011451400",
	"10381c0801138f44400e45e01145e7c0",
)


def frame(rows: tuple[str, ...], intensity: int = 1) -> bytearray:
	pixels = bytearray(128 * 32)
	for y, row in enumerate(rows, 1):
		bits = int(row, 16)
		for x in range(128):
			pixels[y * 128 + x] = intensity if bits & (1 << (127 - x)) else 0
	return pixels


class ChampionPubDmdCheckpoints(unittest.TestCase):
	def test_actual_menu_and_diagnostic_headers(self):
		self.assertEqual(dmd_checkpoints(frame(MAIN_MENU), 128, 32), "MAIN MENU")
		self.assertEqual(dmd_checkpoints(frame(SWITCH_EDGES), 128, 32), "DIAGNOSTIC SWITCH EDGES")

	def test_device_caption_cannot_satisfy_diagnostic_checkpoint(self):
		self.assertEqual(dmd_checkpoints(frame(RIGHT_JAB), 128, 32), "")

	def test_unknown_glyph_and_wrong_dimensions_fail_closed(self):
		pixels = frame(MAIN_MENU)
		pixels[128 + 1] = 0
		self.assertEqual(dmd_checkpoints(pixels, 128, 32), "")
		self.assertEqual(dmd_checkpoints(frame(MAIN_MENU), 64, 64), "")
		self.assertEqual(dmd_checkpoints(b"", 128, 32), "")

	def test_intensity_does_not_change_a_checkpoint(self):
		self.assertEqual(dmd_checkpoints(frame(SWITCH_EDGES, 255), 128, 32), "DIAGNOSTIC SWITCH EDGES")


class ChampionPubRuntimeEvidence(unittest.TestCase):
	def test_all_bundles_and_scenarios_validate(self):
		evidence_schema = json.loads((ROOT / "schemas/evidence.schema.json").read_text(encoding="utf-8"))
		scenario_schema = json.loads((ROOT / "schemas/harness-scenario.schema.json").read_text(encoding="utf-8"))
		for path in (ROOT / "evidence/runtime/wpc-95").glob("champion-pub-*.json"):
			with self.subTest(path=path.name):
				Draft202012Validator(evidence_schema).validate(json.loads(path.read_text(encoding="utf-8")))
		for path in (ROOT / "tools/harness-scenarios/wpc-95").glob("cp-*.json"):
			with self.subTest(path=path.name):
				Draft202012Validator(scenario_schema).validate(json.loads(path.read_text(encoding="utf-8")))

	def test_each_run_has_the_four_rom_display_checkpoints(self):
		expected = ["MAIN MENU", "MAIN MENU T TESTS", "TEST MENU T1 SWITCH EDGES", "DIAGNOSTIC SWITCH EDGES"]
		for path in (ROOT / "evidence/runtime/wpc-95").glob("champion-pub-*.json"):
			evidence = json.loads(path.read_text(encoding="utf-8"))
			name = evidence["runtime"]["raw_runs"][0]["name"]
			with self.subTest(path=path.name):
				checkpoints = evidence["runtime"]["observations"]["runs"][name]["diagnostic_checkpoints"]
				self.assertEqual([row["matched_text"] for row in checkpoints], expected)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "Retained runtime artifacts are external")
	def test_retained_runs_and_all_derived_snapshots_reconcile(self):
		review_root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		probe_sha = hashlib.sha256((ROOT / "tools/champion_pub_mech_probe.py").read_bytes()).hexdigest()
		for path in (ROOT / "evidence/runtime/wpc-95").glob("champion-pub-*.json"):
			evidence = json.loads(path.read_text(encoding="utf-8"))
			uri = evidence["source"]["path"]
			self.assertTrue(uri.startswith("external:pinmame-review-artifacts/"))
			raw_path = review_root / uri.removeprefix("external:pinmame-review-artifacts/")
			with self.subTest(path=path.name):
				self.assertEqual(hashlib.sha256(raw_path.read_bytes()).hexdigest(), evidence["source"]["sha256"])
				run = json.loads(raw_path.read_text(encoding="utf-8"))
				self.assertIsNone(run["failure"])
				self.assertEqual(run["host_model"]["implementation_sha256"], probe_sha)
				self.assertEqual(run["library_sha256"], evidence["runtime"]["emulator"]["sha256"])
				self.assertEqual(run["scenario"]["sha256"], evidence["runtime"]["raw_runs"][0]["scenario_sha256"])
				suspensions = [event for event in run["events"] if event["event"] == "host_mech_feedback_suspended"]
				self.assertEqual(len(suspensions), 1)
				self.assertEqual(suspensions[0]["before_step"], 7)
				self.assertFalse(any(event["event"] == "host_mech_feedback" and event["time_s"] > suspensions[0]["time_s"] for event in run["events"]))
				by_label = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
				for derived in evidence["runtime"]["observations"]["diagnostic_snapshots"]:
					snapshot = by_label[derived["label"]]
					self.assertEqual(snapshot["displays"][0]["pixel_sha256"], derived["pixel_sha256"])
					self.assertEqual(snapshot["active_solenoids"], derived["active_solenoid_addresses"])


if __name__ == "__main__":
	unittest.main()
