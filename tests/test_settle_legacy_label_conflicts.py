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
	("runtime.doctor-who.dw-l2.flasher-test", 19): "5x3 Right/Right",
	("runtime.nba-fastbreak.nbaf-31.switch-edges", 1): "LEFT COIN SLOT",
	("runtime.nba-fastbreak.nbaf-31.switch-edges", 2): "CENTER COIN SLOT",
	("runtime.nba-fastbreak.nbaf-31.switch-edges", 3): "RIGHT COIN SLOT",
	("runtime.nba-fastbreak.nbaf-31.flasher-test", 19): "UPPER LEFT",
}
# Settlements read from a mechanism test rather than a name: the address, the output it always rises with, and the
# display text of the step in which it does.
PAIRED = {
	("runtime.red-and-ted-s-road-show.rs-l6.ted-test", 19): (20, "MOUTH OPEN / T.17 06 RUNNING"),
}
# Settlements read from scoring in play: the bank's other members and the raw step that closes each, the step that
# closes the address, the points every closure scores, and the relay that drops if the ROM tilts.
BANKS = {
	("runtime.harlem-globetrotters-on-tour.hglbtrtr.switch-2-in-play", 2): {
		"members": {1: "drop target 1 down", 3: "drop target 3 down", 4: "drop target 4 down"},
		"step": "public 2 closed",
		"points": 5000,
		"relay": 19,
	},
}
SEVEN_SEGMENT = {0: "", 63: "0", 6: "1", 91: "2", 79: "3", 102: "4", 109: "5", 125: "6", 7: "7", 127: "8", 111: "9"}
# Settlements read from a gameplay timeline: the raw step in which the address changes, and its new state, in order.
TIMELINES = {
	("runtime.diner.diner-l4.game-on-23", 23): [
		("start button raises game-on", 1),
		("ball 1: plumb-bob tilt 3 drops game-on", 0),
		("checkpoint: game-on rises for ball 2", 1),
		("checkpoint: game over drops game-on", 0),
	],
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
				# The last raw run is the evidentiary one; any earlier run only initialized its NVRAM.
				*setup, raw = runtime["raw_runs"]
				for item in runtime["raw_runs"]:
					scenario = ROOT / item["scenario_path"]
					self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), item["scenario_sha256"])
				self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
				address = settlement["binding"]["device"]
				paired = PAIRED.get((source["id"], address))
				timeline = TIMELINES.get((source["id"], address))
				bank = BANKS.get((source["id"], address))
				switch = settlement["binding"]["group"] == "pinmame.input.switch"
				observations = runtime["observations"]
				if bank:
					# Every member and the address score the same, and only the address's closure says the ROM did not tilt.
					closures = {item["input_address"]: item for item in observations["named_action_observations"] if item["input_kind"] == "switch"}
					for number in [*bank["members"], address]:
						self.assertIn(f"rises by {bank['points']:,}", closures[number]["label"])
						self.assertIn(bank["relay"], closures[number]["active_solenoid_addresses"])
					self.assertIn("does not tilt", closures[address]["label"])
				elif timeline:
					# One named action per change of the address, each listing it among its transitions.
					changes = [item for item in observations["named_action_observations"] if address in item["transitioned_solenoid_addresses"]]
					self.assertEqual(len(timeline), len(changes))
					self.assertNotIn("diagnostic_snapshots", observations)
				elif paired:
					partner, text = paired
					sequence = observations["ordered_solenoid_on_sequence"]
					self.assertIn(address, sequence)
					# Every rise of the address is immediately followed by its partner's, and the partner also runs alone.
					self.assertTrue(all(index + 1 < len(sequence) and sequence[index + 1] == partner for index, number in enumerate(sequence) if number == address))
					self.assertGreater(sequence.count(partner), sequence.count(address))
					frames = [item for item in observations["diagnostic_snapshots"] if item["interpreted_text"] == text]
					self.assertTrue(frames)
					frame = frames[0]
				elif switch:
					# A switch is named on the ROM's top line while the host holds it at 1.
					steps = [item for item in observations["named_action_observations"] if item["host_stimulus_switch_addresses"] == [address]]
					self.assertTrue(steps)
					self.assertTrue(all(not item["transitioned_solenoid_addresses"] for item in steps))
					frames = [item for item in observations["diagnostic_snapshots"] if f"after public {address} (" in item["label"] and "set to 1" in item["label"]]
				else:
					steps = [item for item in observations["named_action_observations"] if item["transitioned_solenoid_addresses"] == [address]]
					self.assertTrue(steps)
					frames = [item for item in observations["diagnostic_snapshots"] if item["label"].endswith(f" {address}")]
				if not paired and not timeline and not bank:
					name = ROM_NAMES[(source["id"], address)]
					if switch:
						self.assertTrue(all(f"names it {name} " in item["label"] for item in steps))
					else:
						self.assertTrue(any(f"prints {name} " in item["label"] for item in steps))
					(frame,) = frames
					self.assertTrue(frame["interpreted_text"].startswith(f"{name} / "))
				root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
				if not root:
					continue
				import build_external_evidence_manifest as manifest

				game = runtime["game"]
				for item in runtime["raw_runs"]:
					retained = Path(root) / item["retained_from"][len("external:pinmame-review-artifacts/"):]
					self.assertEqual(item["sha256"], hashlib.sha256(retained.read_bytes()).hexdigest())
					digest = manifest.check_manifest(retained.parent, game)
					self.assertIn(f"{retained.parent.name}/manifest.json SHA-256 {digest}", evidence["source"]["attribution"])
					self.assertEqual(item["scenario_sha256"], load_json(retained)["scenario"]["sha256"])
				for item in setup:
					# The evidentiary run started from only the .nv file this run wrote, cited by its hash.
					written = Path(root) / item["retained_from"][len("external:pinmame-review-artifacts/"):]
					nv = written.parent / "state" / "nvram" / f"{game}.nv"
					self.assertIn(f"SHA-256 {hashlib.sha256(nv.read_bytes()).hexdigest()}", raw["nvram_initialization"])
				path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
				run = load_json(path)
				self.assertIsNone(run["failure"])
				self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
				# The summary and the raw run agree on driver, library and scenario.
				self.assertEqual(game, run["game"])
				self.assertEqual(runtime["emulator"]["sha256"], run["library_sha256"])
				self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
				by_label = {snap["label"]: snap for snap in run["snapshots"]}
				raw_steps = {step["label"]: step for step in run["steps"]}
				for item in runtime["observations"].get("diagnostic_snapshots", []):
					matches = [snap for snap in run["snapshots"] if snap["displays"] and snap["displays"][0]["pixel_sha256"] == item["pixel_sha256"]]
					self.assertTrue(matches, item["label"])
				if bank:
					def score(label: str) -> int:
						return int("".join(SEVEN_SEGMENT[value] for value in by_label[label]["displays"][0]["segments"]) or "0")

					def lit(label: str) -> set[int]:
						return {item["number"] for item in raw_steps[label]["transitions"]["lamps"] if item["states"][-1]}

					labels = [*bank["members"].values(), bank["step"]]
					positions = [list(raw_steps).index(label) for label in labels]
					self.assertEqual(sorted(positions), positions)
					previous = score(list(raw_steps)[positions[0] - 1])
					for label in labels:
						self.assertEqual(bank["points"], score(label) - previous, label)
						previous = score(label)
						self.assertIn(bank["relay"], by_label[label]["active_solenoids"])
						self.assertEqual([], raw_steps[label]["transitions"]["solenoids"])
					# The address's closure lights lamps that no member's closure lit.
					award = lit(bank["step"])
					self.assertTrue(award)
					for label in bank["members"].values():
						self.assertFalse(award & lit(label), label)
					# The relay stays raised from the start of play until the ball drains.
					rises = [event["time_s"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == bank["relay"] and event["state"]]
					drops = [event["time_s"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == bank["relay"] and not event["state"]]
					start, end = by_label[labels[0]]["time_s"], by_label[bank["step"]]["time_s"]
					self.assertTrue(any(time < start for time in rises))
					self.assertFalse(any(start - 3 <= time <= end for time in drops))
				elif timeline:
					states = [event["state"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == address]
					self.assertEqual([state for _, state in timeline], states)
					for label, state in timeline:
						changed = [item["states"] for item in raw_steps[label]["transitions"]["solenoids"] if item["number"] == address]
						self.assertEqual([[state]], changed, label)
				elif paired:
					rises = [event for event in run["events"] if event["event"] == "solenoid" and event["state"]]
					self.assertEqual(observations["ordered_solenoid_on_sequence"], [event["number"] for event in rises][-len(observations["ordered_solenoid_on_sequence"]):])
					times = {number: [event["time_s"] for event in rises if event["number"] == number] for number in (address, partner)}
					self.assertTrue(times[address])
					self.assertTrue(set(times[address]) <= set(times[partner]))
					self.assertTrue(set(times[partner]) - set(times[address]))
					# The step frame is the snapshot taken right after a step in which the address rose.
					steps = run["steps"]
					after = [
						steps[index + 1]["label"] for index in range(len(steps) - 1)
						if any(t["number"] == address and any(t["states"]) for t in steps[index]["transitions"]["solenoids"])
					]
					self.assertTrue(any(by_label[label]["displays"][0]["pixel_sha256"] == frame["pixel_sha256"] for label in after))
				elif switch:
					# The frame that names the switch is the one taken while only it was held at 1.
					held = by_label[f"{address} -> 1"]
					self.assertEqual(frame["pixel_sha256"], held["displays"][0]["pixel_sha256"])
					self.assertEqual(1, raw_steps[f"{address} -> 1"]["observed_state"])
					self.assertEqual({address}, {item["number"] for item in held["watched_switches"] if item["state"] and item["number"] in run["watch_switches"]})
					self.assertEqual([], raw_steps[f"{address} -> 1"]["transitions"]["solenoids"])
				else:
					# The frame that names the address was taken after the press that selected it and before the next
					# press: repeat mode blinks the name, so it may come from a later frame than the selecting step's.
					steps = run["steps"]
					presses = [index for index, step in enumerate(steps) if step["type"] == "pulse"]
					windows = []
					for index in presses:
						if {t["number"] for t in steps[index]["transitions"]["solenoids"] if any(t["states"])} == {address}:
							following = [later for later in presses if later > index]
							windows.append(range(index, following[0] if following else len(steps)))
					self.assertTrue(windows)
					self.assertTrue(any(
						by_label[steps[position]["label"]]["displays"][0]["pixel_sha256"] == frame["pixel_sha256"]
						for window in windows for position in window
					))

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
