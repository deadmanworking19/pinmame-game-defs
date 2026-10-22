"""Derive the compact Terminator 2 G.I. test evidence from the retained raw harness run.

The document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts
root), checks that it ran the committed scenario, the pinned binary and the expected mechanism mask, and writes the derived
observations beside the other WPC-Alpha runtime evidence. A diagnostic snapshot's ``interpreted_text`` is the curator's
visual reading of that snapshot's retained DMD frame, pinned by its pixel SHA-256 in a committed seed; a run whose frame or
reading differs is refused until the new frame has been read again and the seed updated by hand. The tool also refuses a
raw run whose transitions no longer support a stated observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.terminator-2-judgment-day.1991"
GAME = "t2_l8"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "4cdd95d435334c3bd6fe19556b410b558e67266b30e7fb767f52f4d14ed525b1"
HARNESS_DIRECTORY = "terminator-2-1991/harness"
RUN_DIRECTORY = "gi-test/t2_l8"
SCENARIO = "tools/harness-scenarios/wpc-alpha/t2-gi-test.json"
EVIDENCE_PATH = ROOT / "evidence/runtime/wpc-alpha/terminator-2-t2_l8-gi-test.json"
FRAME_SEED_PATH = ROOT / "tools/seeds/williams/terminator-2-judgment-day-1991-frames.json"
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are "
	"host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation "
	"is counted pulses; every diagnostic snapshot's interpreted_text is the curator's visual reading of its retained DMD frame, "
	"identified by its pixel SHA-256. The exact external directory manifest (built by tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)
NVRAM_NOTE = (
	"empty; the run created its own isolated PinMAME state directory, so the ROM restored its factory settings before the "
	"scenario left the message loop with Escape"
)
COMMAND = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game t2_l8 --rom-path <vpinmame-roms> "
	"--work-dir <new-isolated-state> --handle-mechanics 0 --scenario tools/harness-scenarios/wpc-alpha/t2-gi-test.json "
	"--dmd-dir <external-dmd-dir> --watch-switch 5 --watch-switch 7 --watch-switch 8 --watch-switch 22 --output <external-run.json>. "
	"T.6 GEN'L. ILLUM. in stop mode first steps all illumination through its brightness levels, then each string in turn; "
	"every Up press while a string is selected changes that one public G.I. output alone."
)
IDENTIFICATION_LABEL = "Enter 2 (game identification)"
IDENTIFICATION = "TERMINATOR 2 / 50013 REV. L-8"
ALL_LABEL = "T.6 Up 1 (held)"
ALL_TEXT = "ALL ILLUMINATION / T.6 BRIGHT=2 STOP"
# T.6: (public GI string, snapshot read, ROM text, the Up presses whose transitions change that string alone).
GI_STRINGS = (
	(0, "T.6 Up 9 (held)", "TOP INSERT / T.6 BRIGHT=2 STOP / WHT-BRN BRN", range(9, 15)),
	(1, "T.6 Up 17 (held)", "BOTTOM INSERT / T.6 BRIGHT=2 STOP / WHT-ORN ORN", range(17, 23)),
	(2, "T.6 Up 25 (held)", "RIGHT PLAYFIELD / T.6 BRIGHT=2 STOP / WHT-YEL YEL", range(25, 31)),
	(3, "T.6 Up 33 (held)", "CPU STRING / T.6 BRIGHT=2 STOP / WHT-GRN GRN", range(33, 39)),
	(4, "T.6 Up 41 (held)", "LEFT PLAYFIELD / T.6 BRIGHT=2 STOP / WHT-VIO VIO", range(41, 47)),
)
RESTART_LABEL = "Escape out of the fresh-NVRAM loop"
# After the fresh-NVRAM restart the ROM turns every string on, and switches the CPU string from on to off by itself.
RESTART_MIN_CPU_OFFS = 5


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(directory: Path) -> dict[str, Any]:
	run_path = directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / SCENARIO
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful Terminator 2 {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != 0:
		raise ValueError(f"unexpected built-in mechanism mask in {run_path}")
	run["_directory"] = directory
	return run


def _frame_matches(run: dict[str, Any], display: dict[str, Any]) -> bool:
	"""Whether the retained PGM frame reproduces the snapshot's pixel SHA-256.

	run_pinmame_harness.py hashes the raw levels and writes them to the PGM unchanged when any exceeds the layout's depth, or
	scaled to 0-255 (level * 255 / max_level) otherwise; either encoding is accepted.
	"""
	path = run["_directory"] / "dmd" / display["artifact"].replace("\\", "/").rsplit("/", 1)[1]
	layout = display["layout"]
	header = f"P5\n{layout['width']} {layout['height']}\n255\n".encode("ascii")
	data = path.read_bytes()
	if not data.startswith(header) or len(data) != len(header) + layout["width"] * layout["height"]:
		raise ValueError(f"unexpected DMD frame file: {path}")
	payload = data[len(header):]
	max_level = max((1 << max(int(layout.get("depth", 1)), 1)) - 1, 1)
	candidates = {hashlib.sha256(payload).hexdigest(), hashlib.sha256(bytes(round(value * max_level / 255) for value in payload)).hexdigest()}
	return display["pixel_sha256"] in candidates


def _snapshot(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [item for item in run["snapshots"] if item["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one snapshot labelled {label!r}, found {len(matches)}")
	return matches[0]


def _step(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [item for item in run["steps"] if item["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def _changed(step: dict[str, Any], channel: str) -> set[int]:
	return {item["number"] for item in step["transitions"][channel]}


def _states(step: dict[str, Any], channel: str, number: int) -> list[int]:
	for item in step["transitions"][channel]:
		if item["number"] == number:
			return list(item["states"])
	return []


def _switch_offs(states: list[int]) -> int:
	"""Count on-to-off transitions; the zero every string starts from is the common reset blanking, not a switch-off."""
	return sum(1 for before, after in zip(states, states[1:]) if before > 0 and after == 0)


def _diagnostics(run: dict[str, Any], readings: dict[str, str]) -> list[dict[str, Any]]:
	"""Pin each reading to its frame; one interpreted text must always come from one frame."""
	result = []
	by_text: dict[str, str] = {}
	for label, text in readings.items():
		snapshot = _snapshot(run, label)
		displays = [item for item in snapshot["displays"] if item["index"] == 0]
		if len(displays) != 1:
			raise ValueError(f"snapshot {label!r} must carry display 0 exactly once")
		pixel = displays[0]["pixel_sha256"]
		if not _frame_matches(run, displays[0]):
			raise ValueError(f"retained DMD frame of snapshot {label!r} does not reproduce its pixel SHA-256")
		if by_text.setdefault(text, pixel) != pixel:
			raise ValueError(f"the reading {text!r} is pinned to two different frames (at {label!r})")
		result.append({
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"display_index": 0,
			"interpreted_text": text,
			"label": label,
			"nonzero_pixels": displays[0]["nonzero_pixels"],
			"pixel_sha256": pixel,
		})
	return result


def _observation(label: str, inputs: list[int]) -> dict[str, Any]:
	return {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": inputs, "input_address": inputs[0], "input_kind": "switch",
		"label": label, "observed_switch_addresses": [], "result": "observed",
		"transitioned_solenoid_addresses": [],
	}


def build_observations(run: dict[str, Any]) -> dict[str, Any]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION, ALL_LABEL: ALL_TEXT}
	named = []
	restart = _step(run, RESTART_LABEL)
	offs = {number: _switch_offs(_states(restart, "gis", number)) for number in range(5)}
	if offs[3] < RESTART_MIN_CPU_OFFS or any(offs[number] for number in (0, 1, 2, 4)):
		raise ValueError(f"after the restart the ROM must flicker public GI 3 alone, saw on-to-off counts {offs}")
	named.append(_observation(
		f"After the fresh-NVRAM restart the ROM brings public GI 0-4 up from the common reset blanking, keeps 0, 1, 2 and 4 on, and switches public GI 3 from on to off by itself ({offs[3]} times in this run)",
		[5],
	))
	for press in range(1, 7):
		if _changed(_step(run, f"T.6 Up {press}"), "gis") != {0, 1, 2, 3, 4}:
			raise ValueError("T.6 ALL ILLUMINATION must step public GI 0-4 together")
	named.append(_observation("T.6 ALL ILLUMINATION steps the brightness of public GI 0, 1, 2, 3 and 4 together", [7]))
	for channel, label, text, presses in GI_STRINGS:
		readings[label] = text
		changed = [_changed(_step(run, f"T.6 Up {press}"), "gis") for press in presses]
		if any(item != {channel} for item in changed):
			raise ValueError(f"T.6 {text} must change public GI {channel} alone, saw {changed}")
		named.append(_observation(f"T.6 {text.split(' / ')[0]} ({text.split(' / ')[-1]}): Up steps the brightness of public GI {channel} alone", [7]))
	seen = sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]})
	return {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": seen}


def _check_pinned_frames(observations: dict[str, Any]) -> None:
	pinned = json.loads(FRAME_SEED_PATH.read_bytes())[EVIDENCE_PATH.name]
	read = {item["label"]: {"pixel_sha256": item["pixel_sha256"], "reading": item["interpreted_text"]} for item in observations["diagnostic_snapshots"]}
	if read != pinned:
		changed = sorted(label for label in set(read) | set(pinned) if read.get(label) != pinned.get(label))
		raise ValueError(f"{EVIDENCE_PATH.name}: readings or frames differ from the pinned seed at {changed[:5]}")


def build(review_root: Path) -> dict[str, Any]:
	path = review_root / HARNESS_DIRECTORY / RUN_DIRECTORY
	check_manifest(path, GAME)
	run = _load_run(path)
	observations = build_observations(run)
	_check_pinned_frames(observations)
	run_sha = _sha256(path / "run.json")
	manifest_sha = _sha256(path / "manifest.json")
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/terminator_2_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": COMMAND,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": GAME,
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": "t2_l8-gi-test",
					"nvram_initialization": NVRAM_NOTE,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{RUN_DIRECTORY}/run.json",
					"scenario_path": SCENARIO,
					"scenario_sha256": run["scenario"]["sha256"],
					"self_test_pulses": 0,
					"sha256": run_sha,
					"snapshot_count": len(run["snapshots"]),
					"watch_switches": run["watch_switches"],
				}
			],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": f"{ATTRIBUTION} Exact external directory manifest {RUN_DIRECTORY}/manifest.json SHA-256 {manifest_sha}.",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{RUN_DIRECTORY}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"sha256": run_sha,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--review-root", type=Path, default=None)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--write", action="store_true")
	args = parser.parse_args()
	root = args.review_root or (Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) if os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT") else None)
	if root is None:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT or --review-root is required")
	document = build(root)
	if args.write:
		write_json(EVIDENCE_PATH, document)
	elif not EVIDENCE_PATH.is_file() or EVIDENCE_PATH.read_bytes() != canonical_bytes(document):
		raise SystemExit(f"Terminator 2 compact runtime evidence drift: {EVIDENCE_PATH}")
	else:
		print("Terminator 2 G.I. test runtime evidence matches the retained run.")


if __name__ == "__main__":
	main()
