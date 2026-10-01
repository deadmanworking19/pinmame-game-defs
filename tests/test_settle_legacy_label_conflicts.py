from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import settle_legacy_label_conflicts as tool  # noqa: E402

PINNED_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
# The ROM's own printed name for each settled address, as the evidence summary transcribes it.
ROM_NAMES = {
	"runtime.black-rose.br-l4.flasher-test": "RIGHT BOTTOM",
	"runtime.no-fear.nf-23x.flasher-test": "FLS. NO FEAR",
}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class LegacyLabelSettlementTests(unittest.TestCase):
	def test_every_settlement_is_applied_exactly(self) -> None:
		for settlement in tool.SETTLEMENTS:
			with self.subTest(machine=settlement["machine_id"]):
				path = ROOT / settlement["path"]
				record = load_json(path)
				self.assertNotIn(settlement["conflict_id"], {conflict["id"] for conflict in record["conflicts"]})
				# Re-applying the settlement is a no-op on the committed bytes.
				from pinmame_game_defs.jsonio import canonical_bytes

				self.assertEqual(path.read_bytes(), canonical_bytes(tool.settle(record, settlement)))
				(device,) = [item for item in record["outputs"] + record["inputs"] if item["binding"] == settlement["binding"]]
				self.assertEqual(settlement["label"], device["label"])
				self.assertEqual(settlement["kind"], device["kind"])
				self.assertEqual(f"device.{tool.slug(settlement['label'])}", device["id"])
				for alias in settlement["drop_aliases"]:
					self.assertNotIn(alias, device["aliases"])
				self.assertEqual("observed", device["provenance"]["status"])
				self.assertIn(settlement["source"]["id"], device["provenance"]["source_refs"])
				unresolved = [item for item in record["conflicts"] if item.get("status", "unresolved") == "unresolved"]
				self.assertEqual(bool(unresolved), "unresolved_conflicts" in record["coverage"]["missing"])
				sources = {item["id"]: item for item in record["sources"]}
				self.assertEqual("runtime_scenario", sources[settlement["source"]["id"]]["kind"])

	def test_each_settlement_is_tied_to_its_rom_run(self) -> None:
		for settlement in tool.SETTLEMENTS:
			source = settlement["source"]
			with self.subTest(source=source["id"]):
				evidence = load_json(ROOT / source["uri"][len("internal:"):])
				runtime = evidence["runtime"]
				self.assertEqual(PINNED_LIBRARY_SHA256, runtime["emulator"]["sha256"])
				self.assertEqual([settlement["machine_id"]], evidence["machine_ids"])
				(raw,) = runtime["raw_runs"]
				scenario = ROOT / raw["scenario_path"]
				self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), raw["scenario_sha256"])
				self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
				address = settlement["binding"]["device"]
				name = ROM_NAMES[source["id"]]
				steps = [item for item in runtime["observations"]["named_action_observations"] if item["transitioned_solenoid_addresses"] == [address]]
				self.assertTrue(steps)
				self.assertTrue(any(f"prints {name} " in item["label"] for item in steps))
				texts = {item["label"]: item for item in runtime["observations"]["diagnostic_snapshots"]}
				frame = [item for label, item in texts.items() if label.endswith(f" {address}")][0]
				self.assertTrue(frame["interpreted_text"].startswith(f"{name} / "))
				root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
				if not root:
					continue
				import build_external_evidence_manifest as manifest

				path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
				self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
				game = runtime["game"]
				digest = manifest.check_manifest(path.parent, game)
				self.assertIn(f"{game}/manifest.json SHA-256 {digest}", evidence["source"]["attribution"])
				run = load_json(path)
				self.assertIsNone(run["failure"])
				self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
				# The summary and the raw run agree on driver, library and scenario.
				self.assertEqual(game, run["game"])
				self.assertEqual(runtime["emulator"]["sha256"], run["library_sha256"])
				self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
				by_label = {snap["label"]: snap for snap in run["snapshots"]}
				raw_steps = {step["label"]: step for step in run["steps"]}
				for item in runtime["observations"]["diagnostic_snapshots"]:
					matches = [snap for snap in run["snapshots"] if snap["displays"] and snap["displays"][0]["pixel_sha256"] == item["pixel_sha256"]]
					self.assertTrue(matches, item["label"])
				# The step whose frame names the address is the step that pulsed it.
				pulsed = [label for label, step in raw_steps.items() if {t["number"] for t in step["transitions"]["solenoids"] if any(t["states"])} == {address}]
				self.assertTrue(any(by_label[label]["displays"][0]["pixel_sha256"] == frame["pixel_sha256"] for label in pulsed))

	def test_the_tool_check_mode_passes(self) -> None:
		import subprocess

		result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "settle_legacy_label_conflicts.py"), "--check"], capture_output=True, text=True, cwd=ROOT)
		self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
	unittest.main()
