#!/usr/bin/env python3
"""Summarize the ten retained Nine Ball harness runs into compact derived evidence.

The raw runs (``run.json`` plus the isolated PinMAME state) stay under the working root; this tool reads them and writes
``evidence/runtime/stern/nine-ball-diagnostics-and-gameplay.json``. ``--check`` recomputes the summary from the raw runs and refuses drift
from the committed file. Digits are decoded from the seven-segment displays with the comma bit (0x80) masked. Every display frame the
evidence cites (the solenoid-test driver numbers and the switch-test readings) is pinned by the SHA-256 of its segment words in
``tools/seeds/stern/nine-ball-1980-frame-readings.json`` together with the curator's reading, and a run whose cited frame differs is refused.

Usage:
    python tools/summarize_nine_ball_runtime.py --runs <harness-root> --write
    python tools/summarize_nine_ball_runtime.py --runs <harness-root> --check
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
OUTPUT_PATH = ROOT / "evidence/runtime/stern/nine-ball-diagnostics-and-gameplay.json"
FRAME_READINGS_PATH = ROOT / "tools/seeds/stern/nine-ball-1980-frame-readings.json"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVES = {
	"nineball": "4311155374bd000db727c74747cfec8707755a899e5bfd25cc35c133851da971",
	"ninebafp": "48ff10c6b97ca72bd9cffa2768d442bdf0cac8f98020d3a51ba4ec0c9803acac",
	"ninebalb": "21543f3f65d5f80f1892e34881c7ff1087f9dc3a285f8b8c14e8dacce62ed2bc",
}
# run name -> (driver, scenario file stem)
RUNS: dict[str, tuple[str, str]] = {
	"self-test": ("nineball", "nineball-self-test"),
	"solenoid-test": ("nineball", "nineball-solenoid-test"),
	"switch-test": ("nineball", "nineball-switch-test"),
	"gameplay": ("nineball", "nineball-gameplay"),
	"game-over-and-slam": ("nineball", "nineball-game-over-and-slam"),
	"kick-out-spot": ("nineball", "nineball-kick-out-spot"),
	"lock-lane": ("nineball", "nineball-lock-lane"),
	"spinner-option": ("nineball", "nineball-spinner-option"),
	"ninebafp-variant-io": ("ninebafp", "ninebafp-variant-io"),
	"ninebalb-variant-io": ("ninebalb", "ninebalb-variant-io"),
}
RUN_NAMES = tuple(RUNS)
SERVICE_RUNS = ("self-test", "solenoid-test", "switch-test")
PLAY_RUNS = ("gameplay", "game-over-and-slam", "kick-out-spot", "lock-lane", "spinner-option")
SPINNER_LAMPS = (12, 28, 44, 60)
# Seven-segment code (low seven bits) to digit.
DIGITS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
DECODER_HOLES = (16, 32, 48, 64)
# The step from which a run's later responses are confounded, and why.
CONFOUNDED_FROM: dict[str, tuple[str, str]] = {
	"gameplay": (
		"eight bank: object 1 (sw9) raised",
		"From the step `eight bank: object 1 (sw9) raised` on, this run raised the eight-bank targets without modelling the reset and knock-down coils, and once the kick-out hole "
		"closed the ROM began retrying public 9 (object 7's knock-down coil) every {retry:.2f} s (median) while it waited for switch 15, which the run never closed. Public 9 and the bank coils "
		"in every later action are that retry, not a response to the action; the flipper outputs 45-48, the tilt's drop of 19 and its pulse of 8 are read beside it. The retained "
		"kick-out-spot and lock-lane runs model the targets and are the evidence for the knock-down and spot behaviour.",
	),
	"ninebafp-variant-io": (
		"ball enters the kick-out hole before object 5 is lit",
		"From the step `ball enters the kick-out hole before object 5 is lit` on, the knock-down targets are not modelled, so ninebafp retries public 9 every {retry:.2f} s (median) for the rest "
		"of the run exactly as nineball does in the gameplay run; the flipper outputs are read beside it, and the drain and tilt responses are not attributed.",
	),
}


def read_digits(segments: list[int]) -> str:
	return "".join(DIGITS.get(value & 0x7F, "?") for value in segments)


def segments_sha256(segments: list[int]) -> str:
	return hashlib.sha256(json.dumps(segments, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _load_run(runs_root: Path, name: str) -> dict[str, Any]:
	"""One retained run; a separate function so a test can substitute a run's content."""
	return load_json(runs_root / name / "run.json")


def frame_readings() -> dict[str, dict[str, dict[str, str]]]:
	seed = load_json(FRAME_READINGS_PATH)
	if seed.get("format") != "pinmame-frame-readings" or seed.get("machine_id") != "stern.nine-ball.1980":
		raise RuntimeError("the Nine Ball frame-readings seed is not the expected document")
	return seed["runs"]


def pinned_reading(run: str, label: str, segments: list[int]) -> str:
	"""The curator's reading of a cited frame, refusing a frame other than the one that was read."""
	pin = frame_readings().get(run, {}).get(label)
	if pin is None:
		raise RuntimeError(f"{run}: no pinned reading for {label!r}")
	if segments_sha256(segments) != pin["segments_sha256"]:
		raise RuntimeError(f"{run}: {label!r} does not carry the frame the curator read as {pin['reading']!r}")
	if read_digits(segments).strip() != pin["reading"]:
		raise RuntimeError(f"{run}: {label!r} decodes differently from its pinned reading")
	return pin["reading"]


def self_test_presses(run: dict[str, Any]) -> list[float]:
	return [event["time_s"] for event in run["events"] if event["event"] == "switch" and event["number"] == -7 and event["state"] == 1]


def display_frames(run: dict[str, Any], index: int) -> list[tuple[float, list[int]]]:
	return [(event["time_s"], event["segments"]) for event in run["events"] if event["event"] == "display" and event.get("index") == index and "segments" in event]


def frame_at(frames: list[tuple[float, list[int]]], time_s: float) -> list[int]:
	value: list[int] = []
	for event_time, segments in frames:
		if event_time > time_s:
			break
		value = segments
	return value


def solenoid_test_pairs(run: dict[str, Any]) -> list[tuple[int, int]]:
	"""(displayed driver number, public address) for every pulse after the last Self Test press; display 0 is read 0.25 s after each pulse,
	and every frame must be the pinned frame of its position in the 19-step cycle."""
	last = self_test_presses(run)[-1]
	frames = display_frames(run, 0)
	pulses = [event for event in run["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > last]
	pairs = []
	for index, event in enumerate(pulses):
		reading = pinned_reading("solenoid-test", f"pulse {index % 19 + 1}", frame_at(frames, event["time_s"] + 0.25))
		pairs.append((int(reading), event["number"]))
	return pairs


def switch_test_readings(run: dict[str, Any]) -> dict[int, str]:
	readings: dict[int, str] = {}
	for snapshot in run["snapshots"]:
		label = snapshot["label"]
		if label.startswith("close "):
			readings[int(label.split()[1])] = pinned_reading("switch-test", label, snapshot["displays"][0]["segments"]).lstrip("0") or "0"
	return readings


def step_windows(run: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any], float, float]]:
	"""(step, end snapshot, start time, end time); snapshot 0 is taken at boot and snapshot i + 1 at the end of step i."""
	snapshots = run["snapshots"]
	if len(snapshots) != len(run["steps"]) + 1:
		raise RuntimeError("run snapshots do not follow its steps")
	windows = []
	for index, step in enumerate(run["steps"]):
		if snapshots[index + 1]["label"] != step["label"]:
			raise RuntimeError(f"snapshot {index + 1} does not close step {step['label']!r}")
		windows.append((step, snapshots[index + 1], snapshots[index]["time_s"], snapshots[index + 1]["time_s"]))
	return windows


def describe_on_order(addresses: list[int]) -> str:
	order: list[int] = []
	counts: dict[int, int] = {}
	for address in addresses:
		if address not in counts:
			order.append(address)
		counts[address] = counts.get(address, 0) + 1
	return ", ".join(f"{address}" + (f" x{counts[address]}" if counts[address] > 1 else "") for address in order)


def action_observations(run_name: str, run: dict[str, Any]) -> list[dict[str, Any]]:
	"""One observation per host switch step. The response window runs from the step's start to the end of the wait steps that follow it, so a
	coil the scenario waited for is credited to the stimulus before it; lamps lit are the lamps that turned on in the window and were on at its end."""
	windows = step_windows(run)
	confounded_label = CONFOUNDED_FROM.get(run_name, (None, ""))[0]
	if confounded_label is not None and confounded_label not in {step["label"] for step, _, _, _ in windows}:
		raise RuntimeError(f"{run_name}: confound step {confounded_label!r} is missing")
	observations: list[dict[str, Any]] = []
	confounded = False
	for index, (step, _, start, _) in enumerate(windows):
		switch = step.get("switch")
		if switch is None:
			continue
		if step["label"] == confounded_label:
			confounded = True
		last = index
		while last + 1 < len(windows) and windows[last + 1][0].get("switch") is None:
			last += 1
		end_snapshot, end = windows[last][1], windows[last][3]
		steps = [windows[position][0] for position in range(index, last + 1)]
		transitioned = sorted({change["number"] for item in steps for change in item["transitions"]["solenoids"]})
		on_order = [event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"] == 1 and start < event["time_s"] <= end]
		lamp_state: dict[int, int] = {}
		for event in run["events"]:
			if event["event"] == "lamp" and start < event["time_s"] <= end:
				lamp_state[event["number"]] = event["state"]
		lit = sorted(address for address, state in lamp_state.items() if state)
		closes = step.get("state", step.get("active_state", 1))
		stimulus = f"host {'pulses' if step['type'].startswith('pulse') else ('closes' if closes else 'opens')} switch {switch}"
		parts = [f"{step['label']} ({stimulus})"]
		parts.append(f"solenoids on in order {describe_on_order(on_order)}" if on_order else ("solenoids off " + str(transitioned) if transitioned else "no solenoid change"))
		if lit:
			parts.append(f"lamps lit {lit}")
		label = ": ".join(parts[:2]) + ("; " + parts[2] if len(parts) > 2 else "")
		if confounded:
			label += " (after the confound named in the run limitation)"
		observations.append({
			"label": label,
			"input_kind": "switch",
			"input_address": switch,
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [switch],
			"active_solenoid_addresses": sorted(end_snapshot["active_solenoids"]),
			"transitioned_solenoid_addresses": transitioned,
			"result": "observed" if transitioned or lit else "no_matching_transition",
		})
	return observations


def lamps_lit_after(run: dict[str, Any], switch: int) -> list[int]:
	"""Lamps on at the end of the run that last came on after the first closure of ``switch``, in the order they came on."""
	first = next(event["time_s"] for event in run["events"] if event["event"] == "switch" and event["number"] == switch and event["state"] == 1)
	state: dict[int, int] = {}
	last_on: dict[int, float] = {}
	for event in run["events"]:
		if event["event"] == "lamp":
			if event["state"] and not state.get(event["number"]):
				last_on[event["number"]] = event["time_s"]
			state[event["number"]] = event["state"]
	final = run["snapshots"][-1]["active_lamps"]
	return sorted((address for address in final if last_on.get(address, 0.0) > first), key=lambda address: last_on[address])


def spinner_steps(run: dict[str, Any]) -> list[tuple[str, list[int]]]:
	"""For each three-bank target step, the spinner value lamps that ended that step lit after being off."""
	result = []
	for step in run["steps"]:
		if step.get("type") != "set_switch" or step.get("switch") not in (18, 19, 20, 22, 23, 24):
			continue
		lit = sorted(change["number"] for change in step["transitions"].get("lamps", []) if change["number"] in SPINNER_LAMPS and change["states"] and change["states"][-1] == 1)
		result.append((step["label"], lit))
	if len(result) != 6:
		raise RuntimeError(f"spinner-option run does not hold six three-bank steps: {result}")
	return result


def retry_interval(run: dict[str, Any], address: int) -> float:
	"""Median spacing of consecutive pulses of ``address`` closer than 2 s apart: the ROM's retry period for a coil whose switch never answers."""
	on = [event["time_s"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == address and event["state"] == 1]
	gaps = sorted(later - earlier for earlier, later in zip(on, on[1:]) if later - earlier < 2.0)
	if len(gaps) < 5:
		raise RuntimeError(f"public {address} shows no retry loop")
	return gaps[len(gaps) // 2]


def intervals(run: dict[str, Any], address: int) -> list[tuple[float, float | None]]:
	result: list[tuple[float, float | None]] = []
	start = None
	for event in run["events"]:
		if event["event"] != "solenoid" or event["number"] != address:
			continue
		if event["state"] and start is None:
			start = event["time_s"]
		elif not event["state"] and start is not None:
			result.append((start, event["time_s"]))
			start = None
	if start is not None:
		result.append((start, None))
	return result


def build(runs_root: Path) -> dict[str, Any]:
	runs = {name: _load_run(runs_root, name) for name in RUN_NAMES}
	for name, run in runs.items():
		if run.get("failure") is not None:
			raise RuntimeError(f"run {name} failed: {run['failure']}")
		if run["library_sha256"] != LIBRARY_SHA256:
			raise RuntimeError(f"run {name} used an unpinned library")
		if run["game"] != RUNS[name][0]:
			raise RuntimeError(f"run {name} booted {run['game']}")

	self_run = runs["self-test"]
	press = self_test_presses(self_run)[0]
	self_sequence = [event["number"] for event in self_run["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > press - 0.5]
	self_lamps = sorted({event["number"] for event in self_run["events"] if event["event"] == "lamp"})
	if [address for address in DECODER_HOLES if address in self_lamps] or len(self_lamps) != 60:
		raise RuntimeError(f"burn-in lamps are not the sixty SCR outputs: {self_lamps}")

	solenoid_run = runs["solenoid-test"]
	first_step = solenoid_run["steps"][1]
	ignored = [check["after_pulses"] for check in first_step.get("pulse_checks", []) if not check["matched_outputs"]]
	pairs = solenoid_test_pairs(solenoid_run)
	first_cycle = pairs[:19]
	if [number for number, _ in first_cycle] != list(range(1, 20)):
		raise RuntimeError(f"solenoid test did not show drivers 1-19 in order: {first_cycle}")
	cycles = [pairs[index:index + 19] for index in range(0, len(pairs) - 18, 19)]
	if any(cycle != first_cycle for cycle in cycles):
		raise RuntimeError("solenoid test cycles disagree")
	physical_to_public = {str(number): address for number, address in first_cycle}

	readings = switch_test_readings(runs["switch-test"])
	if sorted(readings) != list(range(1, 41)) or any(readings[address] != str(address) for address in range(1, 41)):
		raise RuntimeError(f"switch test readings disagree with the addresses: {readings}")

	all_lamps = sorted({event["number"] for name in RUN_NAMES for event in runs[name]["events"] if event["event"] == "lamp"})
	outside = sorted({event["number"] for name in PLAY_RUNS for event in runs[name]["events"] if event["event"] == "lamp"})
	if sorted({event["number"] for event in runs["gameplay"]["events"] if event["event"] == "lamp"}) != outside:
		raise RuntimeError("the gameplay run no longer drives every lamp the play runs drive; the curator cites it for each of them")
	if [address for address in DECODER_HOLES if address in all_lamps]:
		raise RuntimeError("a lamp decoder hole changed state")
	bonus_lamps = lamps_lit_after(runs["lock-lane"], 9)
	if len(bonus_lamps) != 7:
		raise RuntimeError(f"lock-lane run did not leave seven object lamps lit: {bonus_lamps}")

	manifest_sha, file_count, total_bytes = directory_manifest_sha256(runs_root)
	raw_runs = []
	for name in RUN_NAMES:
		run = runs[name]
		scenario_path = ROOT / f"tools/harness-scenarios/stern/{RUNS[name][1]}.json"
		scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
		if file_sha256(scenario_path) != run["scenario"]["sha256"]:
			raise RuntimeError(f"scenario for {name} no longer matches the run")
		record: dict[str, Any] = {
			"name": name,
			"sha256": file_sha256(runs_root / name / "run.json"),
			"scenario_path": f"tools/harness-scenarios/stern/{RUNS[name][1]}.json",
			"scenario_sha256": run["scenario"]["sha256"],
			"action_count": len(scenario["actions"]),
			"self_test_pulses": len(self_test_presses(run)),
			"nvram_initialization": "empty; the isolated PinMAME state directory was created from scratch for this run",
			"initial_switches": [{"switch": item["switch"], "state": item["state"]} for item in scenario.get("initial_switches", [])],
			"snapshot_count": len(run["snapshots"]),
		}
		if run.get("watch_switches"):
			record["watch_switches"] = sorted(set(run["watch_switches"]))
		raw_runs.append(record)

	all_solenoids = sorted({event["number"] for name in RUN_NAMES for event in runs[name]["events"] if event["event"] == "solenoid"})
	play_solenoids = sorted({event["number"] for name in PLAY_RUNS for event in runs[name]["events"] if event["event"] == "solenoid"})
	power_up = {address: intervals(runs["game-over-and-slam"], address)[0] for address in (8, 17, 18, 19, 20)}

	def seen(name: str) -> list[int]:
		return sorted({event["number"] for event in runs[name]["events"] if event["event"] == "solenoid"})

	def play_entry(name: str, note: str) -> dict[str, Any]:
		entry: dict[str, Any] = {"named_action_observations": action_observations(name, runs[name]), "solenoid_addresses_seen": seen(name), "note": note}
		if name in CONFOUNDED_FROM:
			entry["limitation"] = CONFOUNDED_FROM[name][1].format(retry=retry_interval(runs[name], 9))
		return entry

	return {
		"driver_ids": ["nineball", "ninebafp", "ninebalb"],
		"extractor": {"id": "tools/summarize_nine_ball_runtime.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["stern.nine-ball.1980"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game <driver> --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/stern/<scenario>.json --output <external-run.json>, "
				"for the eight nineball runs (self-test, solenoid-test, switch-test, gameplay, game-over-and-slam, kick-out-spot, lock-lane, spinner-option) and one run each of ninebafp and ninebalb. "
				f"ROM archives: nineball {ROM_ARCHIVES['nineball']}, ninebafp {ROM_ARCHIVES['ninebafp']}, ninebalb {ROM_ARCHIVES['ninebalb']}. Each scenario starts with a 25 s wait for the ROM's "
				"power-up test. Each set_switch or pulse is a host stimulus, never a ROM observation; display readings are player 1's seven-segment words read as digits.",
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": LIBRARY_SHA256},
			"game": "nineball",
			"observations": {
				"lamp_addresses_driven_outside_self_test": outside,
				"lamp_addresses_seen": self_lamps,
				"lamp_decoder_holes_not_seen": [address for address in DECODER_HOLES if address not in all_lamps],
				"named_output_addresses": {f"lock-lane-object-{index}-lamp": address for index, address in enumerate(bonus_lamps, start=1)},
				"physical_service_solenoid_to_public": physical_to_public,
				"public_solenoid_decoder_holes_not_seen": [16] if 16 not in all_solenoids else [],
				"runs": {
					"self-test": {
						"ordered_solenoid_on_sequence": self_sequence,
						"solenoid_addresses_seen": sorted(set(self_sequence)),
						"note": f"One Self Test press starts the burn-in test. All sixty lamp addresses ({len(self_lamps)} seen) are driven and the four decoder holes 16, 32, 48 and 64 never are; "
							f"the solenoids fire in a repeating 19-step cycle that starts with public {self_sequence[0]}.",
						"limitation": "The burn-in drives the displays with test frames, so the driver numbers are read from the solenoid-test run instead.",
					},
					"solenoid-test": {
						"ordered_solenoid_on_sequence": [address for _, address in pairs],
						"solenoid_addresses_seen": sorted({address for _, address in pairs}),
						"note": f"Four accepted Self Test presses start the solenoid test, which pulses one driver at a time and shows its number on the player displays (read 0.25 s after each pulse; "
							f"every frame read is pinned in the frame-readings seed). The ROM ignored press " + ", ".join(str(number) for number in ignored) + f" of the first step, made {self_test_presses(solenoid_run)[0]:.1f} s into the run, so the scenario repeated it until "
							f"the burn-in's first pulse appeared. Over {len(cycles)} complete cycles, driver numbers 1-19 pair with public addresses "
							+ ", ".join(f"{number}->{address}" for number, address in first_cycle) + ".",
					},
					"switch-test": {
						"note": "Five Self Test presses reach the switch test; with each matrix address 1-40 closed alone, the player 1 display read that address's own number (every frame pinned in the "
							"frame-readings seed): " + ", ".join(f"{address}->{reading}" for address, reading in sorted(readings.items())) + ".",
					},
					"gameplay": play_entry("gameplay",
						"A credited game with the trough modelled: each scoring switch is closed once, the three-banks and the loop target go down and up, the eight-bank objects 1-8 are made in "
						"order with their switches held, then the kick-out hole, the lock lane, the flipper buttons, a drain and the tilt. Every lamp address the play runs drive outside the self test "
					f"changes state in this run ({len(outside)} addresses). Public 20 is on "
						+ "; ".join(f"{start:.2f}-{end:.2f} s" for start, end in intervals(runs["gameplay"], 20) if end is not None) + "."),
					"game-over-and-slam": play_entry("game-over-and-slam",
						"Three balls are served, scored on the pop bumper and drained until game over, a second game is started and the slam switch (public 8) is closed. The power-up initialisation "
						"pulses the continuous and kick-out outputs once each: " + ", ".join(f"public {address} at {start:.2f} s" for address, (start, _) in sorted(power_up.items())) + "."),
					"kick-out-spot": play_entry("kick-out-spot",
						"A ball enters the kick-out hole before object 5 is lit, and each knock-down coil's target switch is closed once the coil fires, so the ROM's spot sequence and eject run to completion."),
					"lock-lane": play_entry("lock-lane",
						"Objects 1-4 are made in order with the eight-bank reset and knock-down coils modelled, then three balls are captured in the kick-out hole, on the lane middle switch and on the "
						"lane top switch, and released. The lamps lit at the end of the run that came on after object 1 was hit, in the order they came on: "
						+ ", ".join(str(address) for address in bonus_lamps) + "."),
					"spinner-option": play_entry("spinner-option",
						"Option switch 17 at PinMAME's default (every option switch OFF; the same default gives the three-ball games of the other runs, which the manual prints as switch 7 OFF). With a game started, the three-bank targets are held down one at a time; the spinner value lamps (public 12, 28, 44 and 60) that came on at each step: "
						+ "; ".join(f"{label} -> {lamps}" for label, lamps in spinner_steps(runs["spinner-option"])) + ". The last step completes both banks and the ROM pulses both bank resets while the host keeps every target down, so its lamps are not attributed to one target."),
					"ninebafp-variant-io": play_entry("ninebafp-variant-io",
						"The free-play clone ninebafp: a credited game, the slingshots, pop bumper and dead bumper, the kick-out hole without target modelling, the flipper buttons, a drain and the tilt."),
					"ninebalb-variant-io": play_entry("ninebalb-variant-io",
						"The modified-rules ROM ninebalb: the same actions as the ninebafp run. Public 18 (coin lockout) is on only "
						+ "; ".join(f"{start:.2f}-{end:.2f} s" for start, end in intervals(runs["ninebalb-variant-io"], 18) if end is not None) + " in this run."),
				},
				"solenoid_addresses_seen": all_solenoids,
			},
			"raw_runs": raw_runs,
			"rom_archive_sha256": ROM_ARCHIVES["nineball"],
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and raw NVRAM remain external",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": "source.sha256 is a directory manifest digest, not a file hash: list every file below source.path as {path, size, sha256} with path relative and POSIX-separated, sort by path, serialise as compact canonical JSON (indent=None, separators=(',',':'), sort_keys=True, ensure_ascii=False), encode UTF-8 and take the SHA-256. "
				f"At capture time the tree held {file_count} files totalling {total_bytes} bytes. Individual run hashes are in runtime.raw_runs[].sha256. Play runs observed solenoid addresses {play_solenoids}.",
			"path": "external:pinmame-review-artifacts/nine-ball-1980/harness",
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
	parser.add_argument("--runs", type=Path, required=True, help="directory holding the ten run folders")
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	args = parser.parse_args()
	summary = build(args.runs)
	if args.write:
		write_json(OUTPUT_PATH, summary)
		print(f"Wrote {OUTPUT_PATH}")
	else:
		if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != canonical_bytes(summary):
			raise SystemExit(f"{OUTPUT_PATH} does not match the retained runs")
		print("Nine Ball runtime summary matches the retained runs.")


if __name__ == "__main__":
	main()
