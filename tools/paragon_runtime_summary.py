#!/usr/bin/env python3
"""Build the compact runtime-evidence summary for Bally Paragon from its retained raw runs.

The raw LibPinMAME harness traces stay outside the repository. This tool reads them, derives every
observation the definition cites (the printed-number to public-address pairing of the ROM's
solenoid test for all four drivers, the switch test's displayed numbers, the coil each playfield
switch fires in gameplay, the lamps three closures light, the flipper and tilt reactions), refuses
runs that do not show them, and writes ``evidence/runtime/by35/paragon-1979-harness.json``. A test
recomputes it when the runs are present.

    python tools/paragon_runtime_summary.py --runs <review-artifacts/paragon-1979/harness> [--check]
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

OUTPUT = ROOT / "evidence" / "runtime" / "by35" / "paragon-1979-harness.json"
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
SCENARIO_DIR = "tools/harness-scenarios/by35"
RETAINED_ROOT = "external:pinmame-review-artifacts/paragon-1979/harness"
SEGMENTS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
# Generic flipper power states PinMAME fabricates beside 46 and 48; outside the BY35 profile's rules.
UNPROFILED_FLIPPER_STATES = {45, 47}

# name -> (directory, driver, scenario file or None, command line options)
RUNS = {
	"solenoid-test-paragon": ("solenoid-test", "paragon", None, "--boot-wait 20 --pulse=-7:250:1.2 (x3) --observe 40"),
	"solenoid-test-paragonb": ("solenoid-test", "paragonb", None, "--boot-wait 20 --pulse=-7:250:1.2 (x3) --observe 40"),
	"solenoid-test-paragonc": ("solenoid-test", "paragonc", None, "--boot-wait 20 --pulse=-7:250:1.2 (x3) --observe 40"),
	"solenoid-test-paragond": ("solenoid-test", "paragond", None, "--boot-wait 20 --pulse=-7:250:1.2 (x3) --observe 40"),
	"switch-test-paragon": ("switch-test", "paragon", "paragon-switch-test.json", ""),
	"gameplay-paragon": ("gameplay", "paragon", "paragon-gameplay.json", ""),
	"tilt-paragon": ("tilt", "paragon", "paragon-tilt.json", ""),
}
ROM_ARCHIVES = {
	"paragon": "10658131055e35b5c2ec2baa60636e034c007e0d78a49b178c80806b424b5027",
	"paragonb": "5773350a2c86ab86a02732de7c05e6d1602bca5b3849587d381d16b807495128",
	"paragonc": "3203e58d28c9684016e1d4b8ee02df766943e4a096df1a0d39350c8fa63f1962",
	"paragond": "84d8b90b5d2540b201de661c693d1bdcdd22e5abb92845e1439bf9008134bb83",
}
# Printed solenoid test number -> public address the ROM fires while it displays that number.
EXPECTED_PAIRS = {1: 7, 2: 6, 3: 8, 4: 10, 5: 9, 6: 14, 7: 15, 8: 11, 9: 12, 10: 1, 11: 13, 12: 2, 13: 17, 14: 18, 15: 19}
# Playfield switch -> the one public coil its closure fires in gameplay.
EXPECTED_COILS = {36: 14, 35: 15, 40: 11, 39: 12, 37: 1, 38: 13, 31: 8, 32: 9, 24: 10}
# Switch -> a lamp its closure turns on in gameplay (spinner value, 2X and 3X bonus multipliers).
EXPECTED_LAMPS = {33: 14, 2: 6, 1: 22}


def decode(segments: list[int]) -> str:
	return "".join(SEGMENTS.get(value & 0x7F, "?") for value in segments)


def load_run(runs: Path, name: str) -> dict:
	directory, driver, _, _ = RUNS[name]
	return json.loads((runs / directory / driver / "run.json").read_text(encoding="utf-8"))


def solenoid_test_pairs(run: dict) -> list[tuple[int, int]]:
	"""(displayed number, public solenoid) for the first full cycle of the solenoid test.

	The ROM writes the number to every player display as it fires each coil; the pairing reads player
	1's display 0.25 s after the output turns on, once the multiplexed digits are stable.
	"""
	times, states = [], []
	for event in run["events"]:
		if event["event"] == "display" and event["index"] == 0 and "segments" in event:
			times.append(event["time_s"])
			states.append(event["segments"])
	pairs: list[tuple[int, int]] = []
	started = False
	for event in run["events"]:
		if event["event"] != "solenoid" or event["state"] != 1:
			continue
		position = bisect.bisect_right(times, event["time_s"] + 0.25) - 1
		text = decode(states[position]).strip() if position >= 0 else ""
		if not started:
			started = text == "01"
		if started and text.isdigit():
			number = int(text)
			if pairs and number <= pairs[-1][0]:
				break
			pairs.append((number, event["number"]))
	return pairs


def verify_repeating_cycle(run: dict, pairs: list[tuple[int, int]], minimum: int = 2) -> int:
	"""After the test starts, every pulse follows the paired order, for at least `minimum` full cycles."""
	start = next(e["time_s"] for e in run["events"] if e["event"] == "display" and e["index"] == 0 and "segments" in e and decode(e["segments"]).strip() == "01")
	sequence = [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] >= start - 0.25]
	cycle = [public for _, public in pairs]
	expected = (cycle * (len(sequence) // len(cycle) + 1))[: len(sequence)]
	if sequence != expected or len(sequence) < minimum * len(cycle):
		raise SystemExit("the solenoid test does not repeat its first cycle")
	return len(sequence) // len(cycle)


def addresses(run: dict, kind: str) -> list[int]:
	return sorted({e["number"] for e in run["events"] if e["event"] == kind})


def verify_switch_test(run: dict) -> None:
	"""Closing public N in the switch test makes the ROM show N on player 1's display, for N = 1..40.

	The display flashes, so every display event between the closure and its release is read.
	"""
	switches = [e for e in run["events"] if e["event"] == "switch" and e["number"] > 0]
	shown = []
	for index, event in enumerate(switches):
		if event["state"] != 1:
			continue
		release = next(x["time_s"] for x in switches[index + 1:] if x["number"] == event["number"] and x["state"] == 0)
		texts = {
			decode(e["segments"]).strip()
			for e in run["events"]
			if e["event"] == "display" and e["index"] == 0 and "segments" in e and event["time_s"] <= e["time_s"] <= release + 0.05
		}
		if f"{event['number']:02d}" not in texts:
			raise SystemExit(f"the switch test did not show {event['number']:02d} for public {event['number']}")
		shown.append(event["number"])
	if shown != list(range(1, 41)):
		raise SystemExit(f"the switch test covered {shown}")


def step_of(run: dict, switch: int, kind: str, state: int | None = None) -> dict:
	matches = [s for s in run["steps"] if s["type"] == kind and s.get("switch") == switch and (state is None or s.get("state") == state)]
	if len(matches) != 1:
		raise SystemExit(f"expected one {kind} step for switch {switch}, found {len(matches)}")
	return matches[0]


def fired(step: dict) -> list[int]:
	"""Outputs a step turned on, leaving out the coin lockout (18), which the ROM re-energizes on its own schedule."""
	return sorted({t["number"] for t in step["transitions"]["solenoids"] if 1 in t["states"]} - UNPROFILED_FLIPPER_STATES - {18})


def lamps_on(step: dict) -> set[int]:
	return {t["number"] for t in step["transitions"]["lamps"] if t["states"][-1] == 1}


def verify_gameplay(run: dict) -> None:
	for switch, coil in EXPECTED_COILS.items():
		kind = "set_switch" if switch in (24, 31, 32) else "pulse"
		step = step_of(run, switch, kind, 1 if kind == "set_switch" else None)
		if fired(step) != [coil]:
			raise SystemExit(f"switch {switch} fired {fired(step)}, expected [{coil}]")
	for switch, lamp in EXPECTED_LAMPS.items():
		kind = "pulse" if switch == 33 else "set_switch"
		if lamp not in lamps_on(step_of(run, switch, kind, 1 if kind == "set_switch" else None)):
			raise SystemExit(f"switch {switch} did not turn lamp {lamp} on")
	# The in-line bank (1-4) completes without a reset; the waterfall bank (17-19) completes with output 17.
	for switch in (4, 3, 2, 1):
		if fired(step_of(run, switch, "set_switch", 1)):
			raise SystemExit(f"in-line target {switch} fired a coil")
	if fired(step_of(run, 19, "set_switch", 1)) != [17]:
		raise SystemExit("completing the waterfall bank did not fire output 17")
	start = next(s for s in run["steps"] if s.get("label") == "credit button (public 6)")
	if fired(start) != [2, 7, 17, 19]:
		raise SystemExit(f"the game start fired {fired(start)}")
	left = step_of(run, 84, "set_switch", 1)
	right = step_of(run, 82, "set_switch", 1)
	if fired(left) != [48] or fired(right) != [46]:
		raise SystemExit("the flipper buttons did not raise 48 and 46")
	for switch in (81, 83):
		if fired(step_of(run, switch, "set_switch", 1)):
			raise SystemExit(f"generic flipper position {switch} fired an output")


def verify_tilt(run: dict) -> None:
	step = step_of(run, 7, "pulse")
	dropped = sorted({t["number"] for t in step["transitions"]["solenoids"] if t["states"][-1] == 0} - UNPROFILED_FLIPPER_STATES)
	if dropped != [19, 46] or 61 not in lamps_on(step):
		raise SystemExit(f"the tilt dropped {dropped} and lit {sorted(lamps_on(step))}")
	held = [s for s in run["steps"] if s.get("label") == "right flipper button (public 82) held after tilt"]
	if len(held) != 1 or fired(held[0]):
		raise SystemExit("the right flipper still fired after the tilt")


def step_observations(run: dict, name: str, only: set[int] | None = None) -> list[dict]:
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	items = []
	for step in run["steps"]:
		if step["type"] not in ("pulse", "set_switch"):
			continue
		if only is not None and step["switch"] not in only:
			continue
		snapshot = snapshots[step["label"]]
		transitioned = sorted({item["number"] for item in step["transitions"]["solenoids"]} - UNPROFILED_FLIPPER_STATES)
		items.append({
			"label": f"{name}: {step['label']}",
			"input_kind": "switch",
			"input_address": step["switch"],
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [step["switch"]],
			"active_solenoid_addresses": sorted(set(snapshot["active_solenoids"]) - UNPROFILED_FLIPPER_STATES),
			"transitioned_solenoid_addresses": transitioned,
			"result": "observed" if transitioned else "no_matching_transition",
		})
	return items


def raw_run_entry(runs: Path, name: str) -> dict:
	directory, driver, scenario, _ = RUNS[name]
	path = runs / directory / driver / "run.json"
	run = json.loads(path.read_text(encoding="utf-8"))
	entry: dict = {
		"name": name,
		"sha256": file_sha256(path),
		"self_test_pulses": len([step for step in run["steps"] if step.get("switch") == -7]),
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


def canonical_json(manifest: dict) -> bytes:
	return json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def build(runs: Path, rom_archives: dict[str, str]) -> dict:
	loaded = {name: load_run(runs, name) for name in RUNS}
	for name, run in loaded.items():
		if run["failure"] is not None or run["library_sha256"] != LIBRARY_SHA256 or run["game"] != RUNS[name][1] or run["handle_mechanics"] != 0:
			raise SystemExit(f"run {name} is not a clean pinned-library run")
	reference = loaded["solenoid-test-paragon"]
	pairs = solenoid_test_pairs(reference)
	if dict(pairs) != EXPECTED_PAIRS or [n for n, _ in pairs] != list(range(1, 16)):
		raise SystemExit(f"the solenoid test pairing differs: {pairs}")
	cycles = verify_repeating_cycle(reference, pairs)
	lamps, solenoids = addresses(reference, "lamp"), addresses(reference, "solenoid")
	for driver in ("paragonb", "paragonc", "paragond"):
		run = loaded[f"solenoid-test-{driver}"]
		if solenoid_test_pairs(run) != pairs or addresses(run, "lamp") != lamps or addresses(run, "solenoid") != solenoids:
			raise SystemExit(f"{driver} differs from paragon in its solenoid test or published addresses")
		if verify_repeating_cycle(run, pairs) < 2:
			raise SystemExit(f"{driver} differs from paragon in its solenoid test or published addresses")
	power_on = sorted({e["number"] for e in reference["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] < 6.0})
	gameplay = loaded["gameplay-paragon"]
	verify_gameplay(gameplay)
	verify_tilt(loaded["tilt-paragon"])
	verify_switch_test(loaded["switch-test-paragon"])
	# The boot (first 6 s) includes the power-on pulse of all four continuous outputs; after it nothing drives 3, 4, 5 or 20.
	in_game = sorted({e["number"] for run in (gameplay, loaded["tilt-paragon"]) for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] >= 6.0} - UNPROFILED_FLIPPER_STATES)
	if 20 in in_game or any(a in in_game for a in (3, 4, 5)):
		raise SystemExit(f"an output the definition calls unused was driven in play: {in_game}")
	observed: list[dict] = []
	observed.extend(step_observations(gameplay, "gameplay"))
	observed.extend(step_observations(loaded["tilt-paragon"], "tilt"))
	per_run = {
		"solenoid-test-paragon": {
			"ordered_solenoid_on_sequence": [public for _, public in pairs],
			"note": "Self-test pressed three times; the solenoid test then fires one output per second while showing its number on every player display. Paired with the number on player 1's display 0.25 s after each pulse, in test order 1 to 15: "
			+ ", ".join(f"{number}->{public}" for number, public in pairs) + f". Every later pulse of the run follows the same order ({cycles} full cycles). Before the test, the power-on reset pulsed outputs "
			+ ", ".join(map(str, power_on)) + " together.",
		},
		"solenoid-test-paragonb": {"note": "Same pairing, cycle and published lamp and solenoid addresses as paragon; the player displays show seven digits."},
		"solenoid-test-paragonc": {"note": "Same pairing, cycle and published lamp and solenoid addresses as paragon."},
		"solenoid-test-paragond": {"note": "Same pairing, cycle and published lamp and solenoid addresses as paragon."},
		"switch-test-paragon": {"note": "Self-test pressed five times (the fourth press ends the cycling solenoid test, the fifth starts the switch test, which flashes 0 on the match/ball display with everything open). Closing each of public 1 to 40 in turn made the ROM show that same number on the player displays (every display event between closure and release was read, because the number flashes)."},
		"gameplay-paragon": {"note": "Coin on public 10, credit on public 6 with the ball held on the outhole (8): the start fired 2, 7 and 17 and raised 19. One closure at a time: slingshots 36 and 35 fired 14 and 15; thumper bumpers 40, 39, 37 and 38 fired 11, 12, 1 and 13; saucers 31, 32 and 24 fired 8, 9 and 10. The in-line targets 4, 3, 2 and 1 fired nothing when the bank completed; target 2 lit lamp 6 (2X) and target 1 lamp 22 (3X). Completing the waterfall bank 17-19 fired 17. The spinner (33) lit lamp 14. Holding 84 raised 48 and holding 82 raised 46; holding 81 or 83 changed no output. PinMAME also raised 47 and 45 with 48 and 46; those are omitted here."},
		"tilt-paragon": {"note": "With a game running and the right flipper button held, pulsing the tilt (7) dropped 19 and 46 and lit lamp 61 (TILT); holding 82 again afterwards raised nothing."},
	}
	raw = [raw_run_entry(runs, name) for name in RUNS]
	manifest = build_manifest(runs, "paragon")
	digest = hashlib.sha256(canonical_json(manifest) + b"\n").hexdigest()
	files = len(manifest["files"])
	total = sum(item["size"] for item in manifest["files"])
	return {
		"driver_ids": ["paragon", "paragonb", "paragonc", "paragond"],
		"extractor": {"id": "tools/paragon_runtime_summary.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["bally.paragon.1979"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": (
				"python tools/run_pinmame_harness.py --library <libpinmame> --game <driver> --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
				"{--boot-wait 20 --pulse=-7:250:1.2 --pulse=-7:250:1.2 --pulse=-7:250:1.2 --observe 40 | --scenario tools/harness-scenarios/by35/<scenario>.json} --output <external-run.json>; "
				"handle-mechanics 0 and keyboard handling off for every run. Runs of paragonb, paragonc and paragond used ROM archives with SHA-256 "
				+ ", ".join(rom_archives[d] for d in ("paragonb", "paragonc", "paragond"))
				+ ". Each set_switch or pulse is a host stimulus, never a ROM observation; the display values are the harness's seven-segment words read as digits."
			),
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
			"game": "paragon",
			"observations": {
				"lamp_addresses_seen": lamps,
				"lamp_decoder_holes_not_seen": [16, 32, 48],
				"solenoid_addresses_seen": solenoids,
				"public_solenoid_decoder_holes_not_seen": [16],
				"physical_service_solenoid_to_public": {str(number): public for number, public in pairs},
				"switch_to_lamp": {str(switch): lamp for switch, lamp in sorted(EXPECTED_LAMPS.items())},
				"display_indices_seen": sorted({e["index"] for e in reference["events"] if e["event"] == "display"}),
				"named_action_observations": observed,
				"runs": per_run,
			},
			"raw_runs": raw,
			"rom_archive_sha256": rom_archives["paragon"],
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. PinMAME also publishes its generic flipper power states 45 and 47 beside 46 and 48; they are outside the BY35 controller profile's address rules and are left out of the observations.",
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


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--runs", type=Path, required=True)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = canonical_bytes(build(args.runs, ROM_ARCHIVES))
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
