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
	("runtime.black-rose.br-l4.flasher-test", 19): "RIGHT BOTTOM",
	("runtime.no-fear.nf-23x.flasher-test", 19): "FLS. NO FEAR",
	("runtime.nba-fastbreak.nbaf-31.switch-edges", 1): "LEFT COIN SLOT",
	("runtime.nba-fastbreak.nbaf-31.switch-edges", 2): "CENTER COIN SLOT",
	("runtime.nba-fastbreak.nbaf-31.switch-edges", 3): "RIGHT COIN SLOT",
	("runtime.nba-fastbreak.nbaf-31.flasher-test", 19): "UPPER LEFT",
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
				self.assertEqual(settlement.get("id", f"device.{tool.slug(settlement['label'])}"), device["id"])
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
				name = ROM_NAMES[(source["id"], address)]
				switch = settlement["binding"]["group"] == "pinmame.input.switch"
				observations = runtime["observations"]
				if switch:
					# A switch is named on the ROM's top line while the host holds it at 1.
					steps = [item for item in observations["named_action_observations"] if item["host_stimulus_switch_addresses"] == [address]]
					self.assertTrue(steps)
					self.assertTrue(all(f"names it {name} " in item["label"] and not item["transitioned_solenoid_addresses"] for item in steps))
					frames = [item for item in observations["diagnostic_snapshots"] if f"after public {address} (" in item["label"] and "set to 1" in item["label"]]
				else:
					steps = [item for item in observations["named_action_observations"] if item["transitioned_solenoid_addresses"] == [address]]
					self.assertTrue(steps)
					self.assertTrue(any(f"prints {name} " in item["label"] for item in steps))
					frames = [item for item in observations["diagnostic_snapshots"] if item["label"].endswith(f" {address}")]
				(frame,) = frames
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
				if switch:
					# The frame that names the switch is the one taken while only it was held at 1.
					held = by_label[f"{address} -> 1"]
					self.assertEqual(frame["pixel_sha256"], held["displays"][0]["pixel_sha256"])
					self.assertEqual(1, raw_steps[f"{address} -> 1"]["observed_state"])
					self.assertEqual({address}, {item["number"] for item in held["watched_switches"] if item["state"] and item["number"] in run["watch_switches"]})
					self.assertEqual([], raw_steps[f"{address} -> 1"]["transitions"]["solenoids"])
				else:
					# The step whose frame names the address is the step that pulsed it.
					pulsed = [label for label, step in raw_steps.items() if {t["number"] for t in step["transitions"]["solenoids"] if any(t["states"])} == {address}]
					self.assertTrue(any(by_label[label]["displays"][0]["pixel_sha256"] == frame["pixel_sha256"] for label in pulsed))

	def test_the_tool_refuses_the_wrong_device_and_inconsistent_coverage(self) -> None:
		settlement = tool.SETTLEMENTS[0]
		settled = load_json(ROOT / settlement["path"])
		binding = settlement["binding"]

		# Swapping the settled device with its neighbour's binding puts another device at the address.
		swapped = json.loads(json.dumps(settled))
		(target,) = [item for item in swapped["outputs"] if item["binding"] == binding]
		(neighbour,) = [item for item in swapped["outputs"] if item["binding"] == {**binding, "device": binding["device"] - 1}]
		target["binding"], neighbour["binding"] = neighbour["binding"], target["binding"]
		with self.assertRaisesRegex(RuntimeError, "expected"):
			tool.settle(swapped, settlement)

		# A device that kept the settled id but whose public-number alias names another address.
		aliased = json.loads(json.dumps(settled))
		(target,) = [item for item in aliased["outputs"] if item["binding"] == binding]
		target["aliases"] = [{**alias, "value": "18"} if alias["namespace"] == "pinmame.coil" else alias for alias in target["aliases"]]
		with self.assertRaisesRegex(RuntimeError, "aliases"):
			tool.settle(aliased, settlement)

		# An unsettled record whose device is no longer the one import-legacy wrote.
		renamed = json.loads(json.dumps(settled))
		renamed["conflicts"].append({"id": settlement["conflict_id"], "path": f"binding:{binding['group']}/{binding['device']}/None", "description": "x", "source_refs": []})
		renamed["coverage"]["missing"].append("unresolved_conflicts")
		with self.assertRaisesRegex(RuntimeError, "expected"):
			tool.settle(renamed, settlement)

		# A conflict recorded on another binding is not this settlement's.
		misplaced = json.loads(json.dumps(renamed))
		misplaced["conflicts"][-1]["path"] = f"binding:{binding['group']}/18/None"
		with self.assertRaisesRegex(RuntimeError, "is not on"):
			tool.settle(misplaced, settlement)

		# An unresolved conflict remaining while coverage.missing omits it.
		inconsistent = json.loads(json.dumps(settled))
		inconsistent["conflicts"].append({"id": "conflict.other", "path": "binding:pinmame.output.solenoid/18/None", "description": "x", "source_refs": []})
		with self.assertRaisesRegex(RuntimeError, "omits unresolved_conflicts"):
			tool.settle(inconsistent, settlement)

	def test_the_tool_check_mode_passes(self) -> None:
		import subprocess

		result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "settle_legacy_label_conflicts.py"), "--check"], capture_output=True, text=True, cwd=ROOT)
		self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
	unittest.main()
