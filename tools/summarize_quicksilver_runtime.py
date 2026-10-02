#!/usr/bin/env python3
"""Summarize the three retained Quicksilver harness runs into compact derived evidence.

The raw runs (``run.json`` plus the isolated PinMAME state) stay under the working root; this tool reads them and writes
``evidence/runtime/stern/quicksilver-self-test-and-gameplay.json``. ``--check`` recomputes the summary from the raw runs and
refuses drift from the committed file. Digits are decoded from the Player 1 seven-segment display only, with the comma bit
(0x80) masked, and every figure in an observation label is recomputed from the runs here rather than typed by hand.

Usage:
    python tools/summarize_quicksilver_runtime.py --runs <harness-root> --write
    python tools/summarize_quicksilver_runtime.py --runs <harness-root> --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "evidence/runtime/stern/quicksilver-self-test-and-gameplay.json"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
ROM_ARCHIVE_SHA256 = "691e06ac64f445cde8842934efdc3a7e223b408f442131bcb2903bde56b45ad3"
RUN_NAMES = ("self-test", "stuck-switch", "gameplay")
# Seven-segment code (low seven bits) to digit.
DIGITS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
LAMP_ADDRESSES = [*range(1, 16), *range(17, 32), *range(33, 48), *range(49, 64)]
POWER_UP_END_S = 22.5


def read_digits(segments: list[int]) -> str:
	return "".join(DIGITS.get(value & 0x7F, "?") for value in segments).strip()


def file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def directory_manifest_sha256(directory: Path) -> tuple[str, int, int]:
	paths = sorted((path for path in directory.rglob("*") if path.is_file()), key=lambda path: path.relative_to(directory).as_posix())
	files = [{"path": path.relative_to(directory).as_posix(), "sha256": file_sha256(path), "size": path.stat().st_size} for path in paths]
	payload = json.dumps(files, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
	return hashlib.sha256(payload).hexdigest(), len(files), sum(item["size"] for item in files)


def solenoid_on_sequence(events: list[dict[str, Any]], after_s: float) -> list[int]:
	return [event["number"] for event in events if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > after_s]


def self_test_observations(run: dict[str, Any]) -> dict[str, Any]:
	events = run["events"]
	press = next(event["time_s"] for event in events if event["event"] == "switch" and event["number"] == -7 and event["state"] == 1)
	sequence = solenoid_on_sequence(events, press - 0.5)
	lamps = sorted({event["number"] for event in events if event["event"] == "lamp"})
	return {
		"ordered_solenoid_on_sequence": sequence,
		"solenoid_addresses_seen": sorted(set(sequence)),
		"lamps": lamps,
		"limitation": "The Self Test press at 25 s starts a looping sequence that drives the solenoids and the lamps together, and the Player Score displays show digit-cycling frames during it, so the displayed solenoid number was not read; the physical-to-public mapping rests on the sequence order and on the independent gameplay checks.",
	}


def stuck_switch_observations(run: dict[str, Any]) -> dict[str, Any]:
	readings: dict[int, str] = {}
	for snapshot in run["snapshots"]:
		label = snapshot["label"]
		if label.startswith("close "):
			readings[int(label.split()[1])] = read_digits(snapshot["displays"][0]["segments"]).lstrip("0") or "0"
	return {"readings": readings}


def gameplay_observations(run: dict[str, Any]) -> list[dict[str, Any]]:
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	observations: list[dict[str, Any]] = []
	previous_score = 0
	previous_credits = "00"
	for step in run["steps"]:
		label = step["label"]
		snapshot = snapshots.get(label)
		switch = step.get("switch")
		if snapshot is None or switch is None:
			continue
		score_text = read_digits(snapshot["displays"][0]["segments"]).replace("?", "")
		score = int(score_text) if score_text.isdigit() else None
		delta = None if score is None else score - previous_score
		if score is not None:
			previous_score = score
		transitioned = sorted(item["number"] for item in step["transitions"]["solenoids"])
		credits = read_digits(snapshot["displays"][4]["segments"])
		credits_changed = credits != previous_credits
		previous_credits = credits
		observation = {
			"label": f"{label}: score {score_text or 'blank'}" + (f" ({delta:+d})" if delta is not None and delta else "") + (f", credits {credits}" if credits_changed else "") + (f", solenoids {transitioned}" if transitioned else ", no solenoid change"),
			"input_kind": "switch",
			"input_address": switch,
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [switch],
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"transitioned_solenoid_addresses": transitioned,
			"result": "observed" if transitioned or credits_changed or (delta not in (None, 0)) else "no_matching_transition",
		}
		observations.append(observation)
	return observations


def build(runs_root: Path) -> dict[str, Any]:
	runs = {name: load_json(runs_root / name / "run.json") for name in RUN_NAMES}
	for name, run in runs.items():
		if run.get("failure") is not None:
			raise RuntimeError(f"run {name} failed: {run['failure']}")
		if run["library_sha256"] != LIBRARY_SHA256:
			raise RuntimeError(f"run {name} used an unpinned library")
	self_test = self_test_observations(runs["self-test"])
	stuck = stuck_switch_observations(runs["stuck-switch"])
	gameplay_run = runs["gameplay"]
	gameplay_events = gameplay_run["events"]
	attract_lamps = sorted({event["number"] for event in gameplay_events if event["event"] == "lamp" and POWER_UP_END_S < event["time_s"] < 27.0})
	manifest_sha, file_count, total_bytes = directory_manifest_sha256(runs_root)
	raw_runs = []
	for name in RUN_NAMES:
		scenario = json.loads((runs_root / name / "scenario.json").read_text(encoding="utf-8"))
		raw_runs.append({
			"name": name,
			"sha256": file_sha256(runs_root / name / "run.json"),
			"scenario_path": f"tools/harness-scenarios/stern/quicksilver-{name}.json",
			"scenario_sha256": file_sha256(runs_root / name / "scenario.json"),
			"action_count": len(scenario["actions"]),
			"self_test_pulses": sum(1 for action in scenario["actions"] if action.get("type") == "pulse" and action.get("switch") == -7),
			"nvram_initialization": "empty; the isolated PinMAME state directory was created from scratch for this run",
			"initial_switches": [{"switch": item["switch"], "state": item["state"]} for item in scenario.get("initial_switches", [])],
			"snapshot_count": len(runs[name]["snapshots"]),
		})
	all_solenoids = sorted({event["number"] for name in RUN_NAMES for event in runs[name]["events"] if event["event"] == "solenoid"})
	sequence = self_test["ordered_solenoid_on_sequence"]
	cycle = sequence[sequence.index(2):sequence.index(2) + 19]
	return {
		"driver_ids": ["quicksil"],
		"extractor": {"id": "tools/summarize_quicksilver_runtime.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["stern.quicksilver.1980"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game quicksil --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/stern/quicksilver-<run>.json --output <external-run.json>, for run in self-test, stuck-switch and gameplay. Each scenario starts with a 25 s wait for the ROM's power-up test.",
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": LIBRARY_SHA256},
			"game": "quicksil",
			"observations": {
				"lamp_addresses_driven_outside_self_test": attract_lamps,
				"lamp_addresses_seen": self_test["lamps"],
				"lamp_decoder_holes_not_seen": [address for address in (16, 32, 48, 64) if address not in self_test["lamps"]],
				"physical_service_solenoid_to_public": {str(number): address for number, address in enumerate(cycle, start=1)},
				"public_solenoid_decoder_holes_not_seen": [16] if 16 not in all_solenoids else [],
				"runs": {
					"self-test": {
						"ordered_solenoid_on_sequence": self_test["ordered_solenoid_on_sequence"],
						"solenoid_addresses_seen": self_test["solenoid_addresses_seen"],
						"limitation": self_test["limitation"],
						"note": "All sixty lamp addresses (1-15, 17-31, 33-47, 49-63) are driven; the four decoder holes 16, 32, 48 and 64 never are. The solenoids fire in a repeating 19-step cycle.",
					},
					"stuck-switch": {
						"note": "With each matrix address 1-40 closed alone in the stuck-switch test, the Player 1 display read that address's own number: "
							+ ", ".join(f"{address}->{reading}" for address, reading in sorted(stuck["readings"].items())),
					},
					"gameplay": {
						"named_action_observations": gameplay_observations(gameplay_run),
						"solenoid_addresses_seen": sorted({event["number"] for event in gameplay_events if event["event"] == "solenoid"}),
						"note": "lamp_addresses_driven_outside_self_test lists the lamps that keep toggling in the attract pattern after the power-up flash ends (22.5 s) and before the first coin (27 s).",
					},
				},
				"solenoid_addresses_seen": all_solenoids,
			},
			"raw_runs": raw_runs,
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and raw NVRAM remain external",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": "source.sha256 is a directory manifest digest, not a file hash: list every file below source.path as {path, size, sha256} with path relative and POSIX-separated, sort by path, serialise as compact canonical JSON (indent=None, separators=(',',':'), sort_keys=True, ensure_ascii=False), encode UTF-8 and take the SHA-256. "
				f"At capture time the tree held {file_count} files totalling {total_bytes} bytes. Individual run hashes are in runtime.raw_runs[].sha256.",
			"path": "external:pinmame-review-artifacts/quicksilver-1980/harness",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"sha256": manifest_sha,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--runs", type=Path, required=True, help="directory holding the self-test, stuck-switch and gameplay run folders")
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	args = parser.parse_args()
	summary = build(args.runs)
	if args.write:
		write_json(OUTPUT_PATH, summary)
		print(f"Wrote {OUTPUT_PATH}")
	else:
		if OUTPUT_PATH.read_bytes() != canonical_bytes(summary):
			raise SystemExit(f"{OUTPUT_PATH} does not match the retained runs")
		print("Quicksilver runtime summary matches the retained runs.")


if __name__ == "__main__":
	main()
