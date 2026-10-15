from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import verify_swords_of_fury_runtime as verifier


TEXT_SEGMENTS = {character: value for value, character in verifier.SEGMENT_16.items()}
TEXT_SEGMENTS["1"] = 0x2200
TEXT_SEGMENTS["0"] = 0x443F
DIGIT_SEGMENTS = {digit: value for value, digit in verifier.DIGITS.items()}


def write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def displays(text: str, number: str = "") -> list[dict[str, object]]:
	text = text.ljust(14)[:14]
	segments = [TEXT_SEGMENTS[character] for character in text]
	number_segments = [0, 0, 0, 0]
	if number:
		number_segments.extend(DIGIT_SEGMENTS[digit] for digit in number.zfill(2))
	else:
		number_segments.extend([0, 0])
	number_segments.append(0)
	return [
		{"index": 0, "segments": segments[:7]},
		{"index": 1, "segments": segments[7:]},
		{"index": 2, "segments": number_segments},
	]


def snapshot(label: str, text: str = "", number: str = "", active: list[int] | None = None, switches: dict[int, int] | None = None) -> dict[str, object]:
	return {
		"label": label,
		"displays": displays(text, number),
		"active_solenoids": active or [],
		"watched_switches": [{"number": key, "state": value} for key, value in sorted((switches or {}).items())],
	}


def solenoid_step(label: str, outputs: list[int], *, checkpoint: bool = False, matched_text: str | None = None) -> dict[str, object]:
	step: dict[str, object] = {
		"label": label,
		"type": "pulse_until_output" if checkpoint and matched_text is None else "pulse_until_display" if checkpoint else "action",
		"transitions": {"solenoids": [{"number": output, "states": [1, 0]} for output in outputs]},
	}
	if checkpoint:
		step["pulses"] = 1
		if matched_text is not None:
			step["matched_text"] = matched_text
	return step


class SwordsOfFuryRuntimeVerifierTests(unittest.TestCase):
	def setUp(self) -> None:
		self.temporary = tempfile.TemporaryDirectory()
		self.retained = Path(self.temporary.name) / "review-artifacts" / verifier.MACHINE_ID / "runtime-research"
		self.compact = Path(self.temporary.name) / "swords-runtime.json"
		self._build_fixture()

	def tearDown(self) -> None:
		self.temporary.cleanup()

	def _walk_snapshots(self, names: dict[int, str]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
		snapshots: list[dict[str, object]] = []
		rows: list[dict[str, object]] = []
		for number in range(1, 89):
			if number <= 64 and number not in {58, 60}:
				level1_number, level1_text, active, watched = f"{number:02}", names[number], [], {number: 1}
			elif number == 82:
				level1_number, level1_text, active, watched = "60", names[60], [45, 46], {60: 1}
			elif number == 84:
				level1_number, level1_text, active, watched = "58", names[58], [47, 48], {58: 1}
			else:
				level1_number, level1_text, active, watched = "", "SWITCH EDGES", [], {number: 0} if number in {58, 60} else {}
			snapshots.append(snapshot(f"switch{number} level1", level1_text, level1_number, active, watched))
			low_switches = {60: 0} if number == 82 else {58: 0} if number == 84 else {number: 0} if number <= 64 else {}
			snapshots.append(snapshot(f"switch{number} level0", "SWITCH EDGES", "", [], low_switches))
			rows.append({
				"host_address": number,
				"level1_diagnostic_number": level1_number,
				"level1_text": level1_text.ljust(14),
				"level0_text": "SWITCH EDGES".ljust(14),
				"level1_active_solenoids": active,
			})
		return snapshots, rows

	def _gameplay(self, tag: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
		steps = [solenoid_step("start game and prove ball release", [2, 23], checkpoint=True)]
		for switch, output in verifier.DROP_RESETS.items():
			steps.append(solenoid_step(f"game drop bank switch{switch} down", [output]))
			steps.append(solenoid_step(f"game drop bank switch{switch} reset modelled", []))
		steps.append(solenoid_step("ball drains outhole", [1]))
		snapshots = [snapshot("start game and prove ball release", active=[23])]
		for cabinet, (copied, outputs) in verifier.SYNTHETIC_FLIPPERS.items():
			snapshots.append(snapshot(f"one-shot copied matrix{copied} write must be overwritten", switches={copied: 0}))
			for phase in ("attract", "game", "tilted"):
				snapshots.append(snapshot(f"{phase} cabinet{cabinet} one-shot held", active=list(outputs) if phase == "game" else [], switches={copied: 1}))
			snapshots.append(snapshot(f"game cabinet{cabinet} still held", active=list(outputs), switches={copied: 1}))
			snapshots.append(snapshot(f"game cabinet{cabinet} release", switches={copied: 0}))
		snapshots.extend([
			snapshot("after tilt game-on and flipper state"),
			snapshot("postdrain next-ball observation", active=[23]),
		])
		return steps, snapshots

	def _write_run(self, tag: str, kind: str, steps: list[dict[str, object]], snapshots: list[dict[str, object]], events: list[dict[str, object]], successful: list[dict[str, object]]) -> None:
		scenario = self.retained / "scenarios" / f"{kind}.json"
		if not scenario.exists():
			write_json(scenario, {"actions": steps})
		scenario_data = json.loads(scenario.read_text(encoding="utf-8"))
		self.assertEqual(len(steps), len(scenario_data["actions"]))
		run_relative = f"runs/{tag}-{kind}.json"
		run_path = self.retained / run_relative
		run = {
			"game": f"swrds_{tag}",
			"failure": None,
			"handle_mechanics": 0,
			"initial_switches": [{"switch": -6, "state": 1}],
			"library_sha256": "library-sha256",
			"scenario": {"path": str(scenario), "sha256": sha256(scenario)},
			"steps": steps,
			"snapshots": snapshots,
			"events": events,
		}
		write_json(run_path, run)
		write_json(self.retained / "logs" / f"{tag}-{kind}.command.json", {"exit_code": 0})
		checkpoints = [{key: step[key] for key in ("label", "matched_text", "pulses") if key in step} for step in steps if step["type"] in {"pulse_until_display", "pulse_until_output"}]
		successful.append({
			"run": run_relative,
			"sha256": sha256(run_path),
			"scenario": f"scenarios/{kind}.json",
			"scenario_sha256": sha256(scenario),
			"exit_code": 0,
			"failure": None,
			"action_count": len(steps),
			"checkpoint_matches": checkpoints,
		})

	def _build_fixture(self) -> None:
		# The alpha display's glyph for digit 5 is electrically identical to S;
		# use letters here so the fixture exercises the portable decoder unambiguously.
		names = {number: f"SWITCH {chr(65 + (number - 1) % 26)}" for number in range(1, 65)}
		static = {tag: {"switches": [{"address": number, "text": names[number]} for number in range(1, 65)]} for tag in verifier.TAGS}
		write_json(self.retained / "static-name-tables.json", static)
		write_json(self.retained / "preflight.json", {"source_revision": "source-revision"})
		coil_map = [{"public_output": output, "rom_selector": output if output < 25 else output - 24, "name": "COIL " + chr(65 + output % 26)} for output in verifier.COIL_OUTPUTS if output != 23]
		coil_order = {tag: {"map": coil_map} for tag in verifier.TAGS}
		write_json(self.retained / "coil-order.json", coil_order)
		successful: list[dict[str, object]] = []
		variant_rows: dict[str, list[dict[str, object]]] = {}
		for tag in verifier.TAGS:
			self._write_run(tag, "init", [{"label": "boot", "type": "action", "transitions": {"solenoids": []}}], [], [], successful)
			coil_steps = [solenoid_step("locate factory COIL TEST", [], checkpoint=True, matched_text="COIL TEST")]
			coil_events = [{"event": "solenoid", "state": 1, "number": output} for output in verifier.COIL_OUTPUTS]
			coil_snapshots = []
			for row in coil_map:
				label = f'coil observation {row["public_output"]}'
				coil_steps.append(solenoid_step(label, [row["public_output"]]))
				coil_snapshots.append(snapshot(label, row["name"], f'{row["rom_selector"]:02}'))
			self._write_run(tag, "coil", coil_steps, coil_snapshots, coil_events, successful)
			walk_snapshots, rows = self._walk_snapshots(names)
			variant_rows[tag] = rows
			edge_steps = [solenoid_step("locate SWITCH EDGES", [], checkpoint=True, matched_text="SWITCH EDGES")]
			self._write_run(tag, "switch-edges", edge_steps, walk_snapshots, [], successful)
			game_steps, game_snapshots = self._gameplay(tag)
			self._write_run(tag, "gameplay-v2", game_steps, game_snapshots, [], successful)
		levels_snapshots, _ = self._walk_snapshots(names)
		levels_steps = [solenoid_step("locate SWITCH LEVELS", [], checkpoint=True, matched_text="SWITCH LEVELS")]
		levels_events = []
		for number in range(1, 89):
			step = solenoid_step(f"switch{number} level1", [])
			step["step"] = number
			levels_steps.append(step)
			levels_events.append({"event": "switch", "step": number, "time_s": number * 10})
			high = levels_snapshots[(number - 1) * 2]
			high["time_s"] = number * 10 + 1
			for display in high["displays"]:
				levels_events.append({"event": "display", "time_s": number * 10 + .5, **display})
		self._write_run("l2", "switch-levels", levels_steps, levels_snapshots, levels_events, successful)
		per_variant = {
			tag: {
				"drop_active_levels": {str(switch): {"rom_active_public_level": 1, "inactive_public_level": 0, "reset_output": output, "inactive_stops_retries": True} for switch, output in verifier.DROP_RESETS.items()},
				"coil_outputs_seen": list(verifier.COIL_OUTPUTS),
				"gameplay_contract_passed": True,
				"switch_responses": variant_rows[tag],
			}
			for tag in verifier.TAGS
		}
		registered = []
		for path in sorted(path for path in self.retained.rglob("*") if path.is_file()):
			registered.append({"path": path.relative_to(self.retained).as_posix(), "sha256": sha256(path)})
		write_json(self.compact, {
			"source_revision": "source-revision",
			"library_sha256": "library-sha256",
			"successful_runs": successful,
			"per_variant": per_variant,
			"coil_order": coil_order,
			"source_register": {"files": registered},
		})

	def _refresh_digests(self, relative: str) -> None:
		compact = json.loads(self.compact.read_text(encoding="utf-8"))
		digest = sha256(self.retained / relative)
		for entry in compact["successful_runs"]:
			if entry["run"] == relative:
				entry["sha256"] = digest
		for entry in compact["source_register"]["files"]:
			if entry["path"] == relative:
				entry["sha256"] = digest
		write_json(self.compact, compact)

	def test_synthetic_retained_contract_passes(self) -> None:
		self.assertEqual([], verifier.verify(self.compact, self.retained))

	def test_drop_reset_mutation_fails_after_all_hashes_are_refreshed(self) -> None:
		path = self.retained / "runs/l2-gameplay-v2.json"
		run = json.loads(path.read_text(encoding="utf-8"))
		step = next(item for item in run["steps"] if item["label"] == "game drop bank switch17 down")
		step["transitions"]["solenoids"][0]["number"] = 99
		write_json(path, run)
		self._refresh_digests("runs/l2-gameplay-v2.json")
		errors = verifier.verify(self.compact, self.retained)
		self.assertTrue(any("drop switch 17 level1 did not turn on its reset output 15" in error for error in errors), errors)

	def test_static_name_table_source_hash_is_checked_when_registered(self) -> None:
		path = self.retained / "static-name-tables.json"
		data = json.loads(path.read_text(encoding="utf-8"))
		data["l2"]["switches"][0]["text"] = "MUTATED"
		write_json(path, data)
		errors = verifier.verify(self.compact, self.retained)
		self.assertTrue(any("source_register hash mismatch for static-name-tables.json" in error for error in errors), errors)

	def test_periodic_blank_uses_raw_frames_and_missing_response_fails_after_rehash(self) -> None:
		path = self.retained / "runs/l2-switch-levels.json"
		run = json.loads(path.read_text(encoding="utf-8"))
		high = next(item for item in run["snapshots"] if item["label"] == "switch59 level1")
		high["displays"] = displays("", "")
		write_json(path, run)
		self._refresh_digests("runs/l2-switch-levels.json")
		self.assertEqual([], verifier.verify(self.compact, self.retained))
		run["events"] = [event for event in run["events"] if event.get("time_s") != 590.5]
		write_json(path, run)
		self._refresh_digests("runs/l2-switch-levels.json")
		self.assertTrue(any("switch 59 lacks its coherent ROM display" in error for error in verifier.verify(self.compact, self.retained)))

	def test_disabled_partial_flipper_pair_fails_after_rehash(self) -> None:
		path = self.retained / "runs/l2-gameplay-v2.json"
		run = json.loads(path.read_text(encoding="utf-8"))
		snapshot = next(item for item in run["snapshots"] if item["label"] == "tilted cabinet82 one-shot held")
		snapshot["active_solenoids"] = [45]
		write_json(path, run)
		self._refresh_digests("runs/l2-gameplay-v2.json")
		self.assertTrue(any("tilted cabinet 82 synthetic outputs" in error for error in verifier.verify(self.compact, self.retained)))

	def test_coil_label_mismatch_fails_even_with_updated_raw_hashes(self) -> None:
		path = self.retained / "runs/l2-coil.json"
		run = json.loads(path.read_text(encoding="utf-8"))
		point = next(item for item in run["snapshots"] if item["label"] == "coil observation 17")
		point["displays"] = displays("WRONG", "17")
		write_json(path, run)
		self._refresh_digests("runs/l2-coil.json")
		self.assertTrue(any("output 17 lacks its named selector" in error for error in verifier.verify(self.compact, self.retained)))

	def test_default_cli_skips_cleanly_without_an_external_root(self) -> None:
		with patch.dict(os.environ, {"PINMAME_REVIEW_ARTIFACTS_ROOT": ""}, clear=False):
			self.assertEqual(0, verifier.main(["--check", "--compact", str(self.compact)]))

	def test_real_retained_evidence_when_both_roots_are_present(self) -> None:
		artifacts = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		compact = ROOT / verifier.COMPACT_EVIDENCE
		if not artifacts or not compact.is_file():
			self.skipTest("committed compact evidence or retained review artifacts are not configured")
		retained = Path(artifacts).resolve() / verifier.MACHINE_ID / "runtime-research"
		self.assertEqual([], verifier.verify(compact, retained))


if __name__ == "__main__":
	unittest.main()
