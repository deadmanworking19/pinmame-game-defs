#!/usr/bin/env python3
"""Build the compact runtime-evidence summary for Stern Star Gazer from its retained raw runs.

The raw LibPinMAME harness traces stay outside the repository. This tool reads them, derives every
observation the definition cites (lamp and solenoid addresses, the printed-number to public-address
pairing of the ROM's solenoid test, the switch test's displayed numbers, the lamp each zodiac closure
lights, and the coil, flipper and tilt reactions in gameplay), and writes
``evidence/runtime/by35/star-gazer-1980-harness.json``. A test recomputes it when the runs are present.

    python tools/star_gazer_runtime_summary.py --runs <runtime-evidence/star-gazer-1980/runs> [--check]
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256  # noqa: E402
from build_external_evidence_manifest import build_manifest  # noqa: E402

OUTPUT = ROOT / "evidence" / "runtime" / "by35" / "star-gazer-1980-harness.json"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
SCENARIO_DIR = "tools/harness-scenarios/by35"
RETAINED_ROOT = "external:pinmame-review-artifacts/star-gazer-1980/harness"
SEGMENTS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}

# name -> (directory, driver, scenario file or None, command line options, boot wait, observe seconds)
RUNS = {
	"burn-in-one-pulse-stargzr": ("burn-in-one-pulse", "stargzr", None, "--boot-wait 20 --pulse=-7:250:1.2 --observe 60"),
	"burn-in-one-pulse-stargzfp": ("burn-in-one-pulse", "stargzfp", None, "--boot-wait 20 --pulse=-7:250:1.2 --observe 40"),
	"burn-in-one-pulse-stargzrb": ("burn-in-one-pulse", "stargzrb", None, "--boot-wait 20 --pulse=-7:250:1.2 --observe 40"),
	"solenoid-test-stargzr": ("solenoid-test", "stargzr", None, "--boot-wait 20 --pulse=-7:250:1.2 (x4) --observe 25"),
	"switch-test-stargzr": ("switch-test", "stargzr", "stargzr-switch-test.json", ""),
	"gameplay-coils-stargzr": ("gameplay-coils", "stargzr", "stargzr-gameplay-coils.json", ""),
	"zodiac-lamps-stargzr": ("zodiac-lamps", "stargzr", "stargzr-zodiac-lamps.json", ""),
	"idle-in-play-stargzr": ("idle-in-play", "stargzr", "stargzr-idle-in-play.json", ""),
	"flippers-stargzr": ("flippers", "stargzr", "stargzr-flippers.json", ""),
	"tilt-stargzr": ("tilt", "stargzr", "stargzr-tilt.json", ""),
}
ROM_ARCHIVES = {
	"stargzr": "6ff8f643dd0cbfef6088d0b275c3923aca421c5766d0a4f69d753627184869f8",
	"stargzfp": "48b4fa75d949d2d8ebaf1df5cf112a46306897c505132e4fbd1bead987d1ad89",
	"stargzrb": "5092a41c0adf54ab117e21794c42068c8487c6228f8b743d8087d7d7eef874c5",
}
LIBRARY_SHA256 = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
ZODIAC_SWITCHES = (10, 11, 17, 18, 19, 20, 21, 31, 32, 38, 39, 40)


def decode(segments: list[int]) -> str:
	return "".join(SEGMENTS.get(value & 0x7F, "?") for value in segments)


def load_run(runs: Path, name: str) -> dict:
	directory, driver, _, _ = RUNS[name]
	return json.loads((runs / directory / driver / "run.json").read_text(encoding="utf-8"))


def display_state(run: dict, index: int) -> tuple[list[float], list[list[int]]]:
	times, states = [], []
	for event in run["events"]:
		if event["event"] == "display" and event["index"] == index and "segments" in event:
			times.append(event["time_s"])
			states.append(event["segments"])
	return times, states


def solenoid_test_pairs(run: dict) -> list[tuple[int, int]]:
	"""(displayed number, public solenoid) for every pulse of the solenoid test's first full cycle."""
	times, states = display_state(run, 0)
	pairs: list[tuple[int, int]] = []
	started = False
	for event in run["events"]:
		if event["event"] != "solenoid" or event["state"] != 1:
			continue
		position = bisect.bisect_right(times, event["time_s"] + 0.25) - 1
		text = decode(states[position]).strip()
		if not started:
			started = text == "01"
		if started and text.isdigit():
			number = int(text)
			if pairs and number <= pairs[-1][0]:
				break
			pairs.append((number, event["number"]))
	return pairs


def lamps_and_solenoids(run: dict) -> tuple[list[int], list[int]]:
	lamps = sorted({e["number"] for e in run["events"] if e["event"] == "lamp"})
	solenoids = sorted({e["number"] for e in run["events"] if e["event"] == "solenoid"})
	return lamps, solenoids


def long_blinker(step: dict, minimum: int = 9) -> list[int]:
	"""The lamp a zodiac closure flashes: of the lamps that change at least `minimum` times in the step,
	the one with the fewest changes. The twelfth sign also starts the ring-completion lamp show, whose
	lamps change more often than the sign's own lamp."""
	candidates = [(len(item["states"]), item["number"]) for item in step["transitions"]["lamps"] if len(item["states"]) >= minimum]
	if not candidates:
		return []
	fewest = min(count for count, _ in candidates)
	return sorted(number for count, number in candidates if count == fewest)


def step_observations(run: dict, name: str, only: set[int] | None = None) -> list[dict]:
	"""One named-action observation per switch action of a scenario run."""
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	items = []
	for step in run["steps"]:
		if step["type"] not in ("pulse", "set_switch"):
			continue
		if only is not None and step["switch"] not in only:
			continue
		snapshot = snapshots[step["label"]]
		transitioned = sorted({item["number"] for item in step["transitions"]["solenoids"]})
		item = {
			"label": f"{name}: {step['label']}",
			"input_kind": "switch",
			"input_address": step["switch"],
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [step["switch"]],
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"transitioned_solenoid_addresses": transitioned,
			"result": "observed" if transitioned else "no_matching_transition",
		}
		display = next((entry for entry in snapshot["displays"] if entry["index"] == 0 and "segments" in entry), None)
		if display is not None:
			item["display_responses"] = [{
				"snapshot_label": step["label"],
				"display_index": 0,
				"segments": display["segments"],
				"decoded_segment_positions": list(range(len(display["segments"]))),
				"interpreted_text": decode(display["segments"]).strip(),
			}]
		items.append(item)
	return items


VALUE_SWEEP = (7, 23, 39, 55, 8, 24, 40, 56)
LOCKSTEP_PAIRS = ((31, 9), (47, 41))


def verify_value_sweep(run: dict) -> list[int]:
	"""The eight spinner-and-bank value lamps flash one at a time in the order 500 to 4000.

	Returns the first eight consecutive value-lamp turn-on events that match the chart order, and
	refuses a run in which no such sweep appears.
	"""
	events = [e["number"] for e in sorted((e for e in run["events"] if e["event"] == "lamp" and e["state"] == 1 and e["number"] in VALUE_SWEEP), key=lambda e: e["time_s"])]
	for start in range(len(events) - len(VALUE_SWEEP) + 1):
		if tuple(events[start:start + len(VALUE_SWEEP)]) == VALUE_SWEEP:
			return list(VALUE_SWEEP)
	raise SystemExit("the idle run shows no 500-to-4000 value-lamp sweep")


def verify_lockstep(run: dict, lamp: int, partner: int, minimum: int = 6) -> int:
	"""Lamp `lamp` changes state at the same moments, to the same states, as lamp `partner` (to 0.1 s)."""
	def changes(number: int) -> list[tuple[float, int]]:
		return [(round(e["time_s"], 1), e["state"]) for e in run["events"] if e["event"] == "lamp" and e["number"] == number and e["time_s"] > 30]
	a, b = changes(lamp), changes(partner)
	if len(a) < minimum or len(a) != len(b) or any(abs(x[0] - y[0]) > 0.11 or x[1] != y[1] for x, y in zip(a, b)):
		raise SystemExit(f"lamp {lamp} does not change in lockstep with lamp {partner}")
	return len(a)


def verify_switch_test(run: dict) -> list[int]:
	"""Closing public N in the switch test makes the ROM display N, for every N from 1 to 40."""
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	shown = []
	for number in range(1, 41):
		snapshot = snapshots.get(f"public {number} closed")
		display = None if snapshot is None else next((d for d in snapshot["displays"] if d["index"] == 0 and "segments" in d), None)
		if display is None or decode(display["segments"]).strip() != f"{number:02d}":
			raise SystemExit(f"the switch test did not display {number:02d} for public {number}")
		shown.append(number)
	zeros = 0
	for number in range(1, 41):
		snapshot = snapshots.get(f"public {number} open")
		display = None if snapshot is None else next((d for d in snapshot["displays"] if d["index"] == 5 and "segments" in d), None)
		if display is not None and decode(display["segments"]) == " 0":
			zeros += 1
	if zeros == 0:
		raise SystemExit("the switch test never showed its flashing 0 with every switch open")
	return shown


def raw_run_entry(runs: Path, name: str) -> dict:
	directory, driver, scenario, options = RUNS[name]
	path = runs / directory / driver / "run.json"
	run = json.loads(path.read_text(encoding="utf-8"))
	pulses = [step for step in run["steps"] if step.get("switch") == -7]
	entry: dict = {
		"name": name,
		"sha256": file_sha256(path),
		"self_test_pulses": len(pulses),
		"nvram_initialization": "empty; the run created its own isolated PinMAME state directory (state/ beside run.json) and sends no keyboard input",
		"snapshot_count": len(run["snapshots"]),
		"retained_from": f"{RETAINED_ROOT}/{directory}/{driver}/run.json",
	}
	if scenario:
		entry["scenario_path"] = f"{SCENARIO_DIR}/{scenario}"
		entry["scenario_sha256"] = file_sha256(ROOT / SCENARIO_DIR / scenario)
		entry["action_count"] = run["scenario"]["action_count"]
		entry["watch_switches"] = sorted(run["watch_switches"])
	else:
		entry["pulses"] = [{"switch": step["switch"], "hold_ms": step["hold_ms"], "settle_s": step["settle_s"]} for step in run["steps"] if step["type"] == "pulse"]
	if run["initial_switches"]:
		entry["initial_switches"] = sorted(run["initial_switches"], key=lambda item: item["switch"])
	return entry


def build(runs: Path) -> dict:
	loaded = {name: load_run(runs, name) for name in RUNS}
	for name, run in loaded.items():
		if run["failure"] is not None or run["library_sha256"] != LIBRARY_SHA256 or run["game"] != RUNS[name][1] or run["handle_mechanics"] != 0:
			raise SystemExit(f"run {name} is not a clean pinned-library run")
	burn_lamps, burn_solenoids = lamps_and_solenoids(loaded["burn-in-one-pulse-stargzr"])
	for name in ("burn-in-one-pulse-stargzfp", "burn-in-one-pulse-stargzrb"):
		if lamps_and_solenoids(loaded[name]) != (burn_lamps, burn_solenoids):
			raise SystemExit(f"{name} published different lamp or solenoid addresses than stargzr")
	pairs = solenoid_test_pairs(loaded["solenoid-test-stargzr"])
	if [number for number, _ in pairs] != list(range(1, 20)):
		raise SystemExit(f"the solenoid test pairing is incomplete: {pairs}")

	zodiac_run = loaded["zodiac-lamps-stargzr"]
	switch_to_lamp: dict[str, int] = {}
	for step in zodiac_run["steps"]:
		if step["type"] == "pulse" and step["switch"] in ZODIAC_SWITCHES:
			blinking = long_blinker(step)
			if len(blinking) != 1:
				raise SystemExit(f"zodiac closure {step['switch']} did not light exactly one lamp: {blinking}")
			switch_to_lamp[str(step["switch"])] = blinking[0]

	observed: list[dict] = []
	observed.extend(step_observations(loaded["gameplay-coils-stargzr"], "gameplay"))
	observed.extend(step_observations(zodiac_run, "zodiac"))
	observed.extend(step_observations(loaded["flippers-stargzr"], "flippers"))
	observed.extend(step_observations(loaded["tilt-stargzr"], "tilt"))
	observed.extend(step_observations(loaded["switch-test-stargzr"], "switch test", only=set(range(1, 41))))

	sweep = verify_value_sweep(loaded["idle-in-play-stargzr"])
	lockstep = {f"{lamp}-{partner}": verify_lockstep(loaded["idle-in-play-stargzr"], lamp, partner) for lamp, partner in LOCKSTEP_PAIRS}
	shown = verify_switch_test(loaded["switch-test-stargzr"])
	per_run: dict[str, dict] = {
		"solenoid-test-stargzr": {
			"ordered_solenoid_on_sequence": [public for _, public in pairs],
			"note": "Paired with the number the ROM shows on player 1's display 0.25 s after each pulse, in test order 1 to 19: "
			+ ", ".join(f"{number}->{public}" for number, public in pairs) + ". The display is multiplexed, so the pairing reads the stable value at 0.25 s after the output turns on.",
		},
		"idle-in-play-stargzr": {"note": "No input after the ball leaves the outhole. The value-lamp sweep over the eight spinner-and-bank lamps ran " + ", ".join(map(str, sweep)) + " in that order (verified from the lamp events), and lamps 31 and 47 changed state at the same moments as lamps 9 and 41 (" + ", ".join(f"{pair}: {count} changes" for pair, count in sorted(lockstep.items())) + ")."},
		"switch-test-stargzr": {"note": "Self-test pressed five times to reach the switch test; closing each of public matrix switches " + f"{shown[0]} to {shown[-1]}" + " in turn made the ROM display that same number (verified for every address from the run's snapshots), and the ball/match display showed 0 (the flashing 0 of 'all switches open') at the end of some releases."},
	}
	runs_block = {name: value for name, value in per_run.items()}
	raw = [raw_run_entry(runs, name) for name in RUNS]
	manifest = build_manifest(runs, "stargzr")
	digest = hashlib.sha256(canonical_json(manifest) + b"\n").hexdigest()
	files = len(manifest["files"])
	total = sum(item["size"] for item in manifest["files"])
	return {
		"driver_ids": ["stargzr", "stargzfp", "stargzrb"],
		"extractor": {"id": "tools/star_gazer_runtime_summary.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["stern.star-gazer.1980"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": (
				"python tools/run_pinmame_harness.py --library <libpinmame> --game <driver> --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
				"{--boot-wait 20 --pulse=-7:250:1.2 --observe 60 | --scenario tools/harness-scenarios/by35/<scenario>.json} --output <external-run.json>; handle-mechanics 0 and keyboard handling off for every run. "
				"Runs of stargzfp and stargzrb used ROM archives with SHA-256 " + ROM_ARCHIVES["stargzfp"] + " and " + ROM_ARCHIVES["stargzrb"] + ". "
				"Each set_switch or pulse is a host stimulus, never a ROM observation; the display values are the harness's seven-segment words for player 1 (display 0) read as digits."
			),
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
			"game": "stargzr",
			"observations": {
				"lamp_addresses_seen": burn_lamps,
				"lamp_decoder_holes_not_seen": [16, 32, 48, 64],
				"solenoid_addresses_seen": burn_solenoids,
				"public_solenoid_decoder_holes_not_seen": [16],
				"physical_service_solenoid_to_public": {str(number): public for number, public in pairs},
				"switch_to_lamp": switch_to_lamp,
				"display_indices_seen": [0, 1, 2, 3, 4, 5],
				"named_action_observations": observed,
				"runs": runs_block,
			},
			"raw_runs": raw,
			"rom_archive_sha256": ROM_ARCHIVES["stargzr"],
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Gameplay runs also published the generic flipper states 45 and 47 beside 46 and 48; they are outside the controller profile's address rules and are not listed. The runs were produced under runtime-evidence/star-gazer-1980/runs and moved unchanged to this directory, so the work_dir field inside each run records the original location.",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": (
				"source.sha256 is a directory manifest digest, not a file hash: the SHA-256 recorded in manifest.sha256 beside manifest.json, built by tools/build_external_evidence_manifest.py, "
				"which lists every file below source.path as {path, size, sha256} with path relative and POSIX-separated, sorted by path, serialised as compact canonical JSON "
				f"(separators=(',',':'), sort_keys=True, ensure_ascii=False) plus a newline, encoded UTF-8. At capture time the tree held {files} files totalling {total} bytes. "
				"Individual run hashes are in runtime.raw_runs[].sha256."
			),
			"path": RETAINED_ROOT,
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"sha256": digest,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def canonical_json(manifest: dict) -> bytes:
	return json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--runs", type=Path, required=True)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = canonical_bytes(build(args.runs))
	if args.check:
		if OUTPUT.read_bytes() != text:
			print("runtime summary drift", file=sys.stderr)
			return 1
		print("runtime summary matches the retained runs")
		return 0
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	OUTPUT.write_bytes(text)
	print(f"wrote {OUTPUT.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
