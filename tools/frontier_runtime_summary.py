#!/usr/bin/env python3
"""Build the compact runtime-evidence summary for Bally Frontier from its retained raw runs.

The raw LibPinMAME harness traces stay outside the repository. This tool reads them, derives every
observation the definition cites (the printed-number to public-address pairing of the ROM's
solenoid test for frontier and frontiea, the switch test's displayed numbers, the coil each
playfield switch fires in gameplay, the lamps the features light, the score each cited closure
adds, the flipper, tilt and gate reactions), refuses runs that do not show them, and writes
``evidence/runtime/by35/frontier-1980-harness.json``. A test recomputes it when the runs are present.

Every display frame the summary reads a number from is pinned, with its segment words, their digest
and the reading, in ``tools/seeds/bally/frontier-1980-display-readings.json``; a run whose cited
frame differs in any way is refused, so a substituted or re-recorded frame cannot inherit a reading.

    python tools/frontier_runtime_summary.py --runs <review-artifacts/frontier-1980/harness> [--check]
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

OUTPUT = ROOT / "evidence" / "runtime" / "by35" / "frontier-1980-harness.json"
READINGS_PATH = ROOT / "tools" / "seeds" / "bally" / "frontier-1980-display-readings.json"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
SCENARIO_DIR = "tools/harness-scenarios/by35"
RETAINED_ROOT = "external:pinmame-review-artifacts/frontier-1980/harness"
SEGMENTS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
# PinMAME's synthetic flipper pairs, right 45/46 and left 47/48: core_updateSw raises both members
# of a pair together from the enabled button, so 45 and 47 carry the same state as 46 and 48. The
# BY35 controller profile declares all four, and the summary keeps them.
FLIPPER_PAIRS = {45, 46, 47, 48}
# The coin lockout (18) is re-energized by the ROM on its own schedule and is left out of "fired".
COIN_LOCKOUT = 18
# Everything before this time is the boot: the PIA reset pulse of 17-20 at about 5.8 s and the
# ROM's power-on kicks (10, 9, 8) and relay blip (19) at about 8.5 s.
BOOT_END_S = 10.0

# name -> (directory, driver, scenario file or None, command line options)
RUNS = {
	"solenoid-test-frontier": ("solenoid-test", "frontier", None, "--boot-wait 30 --pulse=-7:250:1.2 (x3) --observe 40"),
	"solenoid-test-frontiea": ("solenoid-test", "frontiea", None, "--boot-wait 30 --pulse=-7:250:1.2 (x3) --observe 40"),
	"switch-test-frontier": ("switch-test", "frontier", "frontier-switch-test.json", ""),
	"gameplay-frontier": ("gameplay", "frontier", "frontier-gameplay.json", ""),
	"tilt-frontier": ("tilt", "frontier", "frontier-tilt.json", ""),
	"gate-frontier": ("gate", "frontier", "frontier-gate.json", ""),
}
ROM_ARCHIVES = {
	"frontier": "6c8b4de20bb7a2d923f2dada33c6452001a2d78c9e48c35b91d3e370641f8606",
	"frontiea": "65c890dabfc3a818ce850a16b10041d10372223aefedbc497a2a1dad6efc8e80",
}
# Printed solenoid test number -> public address the ROM fires while it displays that number.
EXPECTED_PAIRS = {1: 7, 2: 6, 3: 9, 4: 10, 5: 8, 6: 11, 7: 12, 8: 13, 9: 14, 10: 15, 11: 17, 12: 18, 13: 19}
# Playfield switch pulse -> the one public coil its closure fires in gameplay.
EXPECTED_COILS = {37: 14, 36: 15, 40: 11, 39: 12, 38: 13}
# Gameplay step -> (coils fired, lamps that must end on, lamps that must end off).
EXPECTED_STEPS = {
	"credit button (public 6)": ([7, 8, 9, 10, 19], {13, 14}, set()),
	"public 12 saucer: ball enters": ([10], {7}, set()),
	"public 25 saucer rollover button, gate closed": ([], set(), set()),
	"public 23 1st in-line drop target down": ([17], {15, 40}, set()),
	"public 22 2nd in-line drop target down": ([], {57}, set()),
	"public 21 3rd in-line drop target down": ([], {54, 56, 58}, {57}),
	"public 24 grizzly target": ([], {52}, {54, 58}),
	"right bank, 1st completion: public 33 bottom side drop target down": ([], set(), set()),
	"right bank, 1st completion: public 34 middle side drop target down": ([], set(), set()),
	"right bank, 1st completion: public 35 top side drop target down": ([9], {30, 31}, {14}),
	"right bank, 2nd completion: public 35 top side drop target down": ([9], {46, 47}, {30, 31}),
	"right bank, 3rd completion: public 35 top side drop target down": ([9], {60, 62, 63}, {46, 47}),
	"public 36 right slingshot, specials lit": ([15], {44}, {60}),
	"public 37 left slingshot, specials lit": ([14], {60}, {44}),
	"public 13 A rollover lane": ([], {1, 10}, {6}),
	"public 14 B rollover lane": ([], {17, 26}, {22}),
	"public 15 C rollover lane": ([], {12, 23, 33, 42, 49}, {7}),
	"public 29 left target": ([], {2}, set()),
	"public 30 center target": ([], {18}, set()),
	"public 31 right target": ([], {34, 39}, {23}),
	"public 4 left flipper feed lane": ([], set(), set()),
	"public 3 right flipper feed lane": ([], set(), set()),
	"public 13 A rollover lane, second round": ([], {3}, {6}),
	"public 14 B rollover lane, second round": ([], {19}, {22}),
	"public 15 C rollover lane, second round": ([], {11, 35, 43, 50, 55}, {39, 49}),
	"public 2 right out lane": ([], set(), set()),
	"public 5 left out lane": ([6], {59}, set()),
	"left flipper button (public 84) held": ([47, 48], set(), set()),
	"right flipper button (public 82) held": ([45, 46], set(), set()),
	"upper left generic position (public 83) held": ([], set(), set()),
	"upper right generic position (public 81) held": ([], set(), set()),
	"outhole hold closed": ([7, 8, 9], set(), set()),
}
# The gameplay snapshots whose player-1 score the summary cites: every snapshot from the first to the
# last of these labels, in run order, so each closure's score is the difference of two pinned frames.
SCORE_FIRST = "ball leaves the outhole"
SCORE_LAST = "public 5 left out lane"
# Gate run step -> (coils fired, coils that must end off).
GATE_STEPS = {
	"credit button (public 6)": ([7, 8, 9, 10, 19], set()),
	"public 23 1st in-line drop target down: opens the gate": ([17], set()),
	"credit button (public 6): add player 2 on ball 1": ([], set()),
	"drain: ball enters the outhole": ([7, 8, 9], {17}),
}


def decode(segments: list[int]) -> str:
	return "".join(SEGMENTS.get(value & 0x7F, "?") for value in segments)


def segments_sha256(segments: list[int]) -> str:
	return hashlib.sha256(json.dumps(segments, separators=(",", ":")).encode("utf-8")).hexdigest()


def load_run(runs: Path, name: str) -> dict:
	directory, driver, _, _ = RUNS[name]
	return json.loads((runs / directory / driver / "run.json").read_text(encoding="utf-8"))


def display_events(run: dict, index: int = 0) -> list[dict]:
	return [e for e in run["events"] if e["event"] == "display" and e["index"] == index and "segments" in e]


def frame(run_name: str, source: str, key: str, segments: list[int], cited_as: str) -> dict:
	return {
		"run": run_name, "source": source, "key": key, "display_index": 0, "segments": list(segments),
		"segments_sha256": segments_sha256(segments), "reading": decode(segments).strip(), "cited_as": cited_as,
	}


def solenoid_test_pairs(run: dict, run_name: str) -> tuple[list[tuple[int, int]], list[dict]]:
	"""(displayed number, public solenoid) for the first full cycle of the solenoid test, with the frames read.

	The ROM writes the number to every player display as it fires each coil; the pairing reads player
	1's display 0.25 s after the output turns on, once the multiplexed digits are stable. Only pulses
	after the first self-test press count: frontiea shows its version number, 01, at power-on.
	"""
	events = display_events(run)
	times = [e["time_s"] for e in events]
	first_press = test_start(run)
	pairs: list[tuple[int, int]] = []
	frames: list[dict] = []
	started = False
	for event in run["events"]:
		if event["event"] != "solenoid" or event["state"] != 1 or event["time_s"] < first_press:
			continue
		position = bisect.bisect_right(times, event["time_s"] + 0.25) - 1
		if position < 0:
			continue
		shown = events[position]
		text = decode(shown["segments"]).strip()
		if not started:
			started = text == "01"
		if started and text.isdigit():
			number = int(text)
			if pairs and number <= pairs[-1][0]:
				break
			pairs.append((number, event["number"]))
			frames.append(frame(run_name, "display_event", f"{shown['time_s']:.6f}", shown["segments"], f"solenoid test number {number:02d} while public {event['number']} fires"))
	return pairs, frames


def test_start(run: dict) -> float:
	"""Time of the first self-test press (public -7 closing)."""
	return next(e["time_s"] for e in run["events"] if e["event"] == "switch" and e["number"] == -7 and e["state"] == 1)


def verify_repeating_cycle(run: dict, pairs: list[tuple[int, int]], minimum: int = 2) -> int:
	"""After the test starts, every pulse follows the paired order, for at least `minimum` full cycles."""
	first_press = test_start(run)
	start = next(e["time_s"] for e in display_events(run) if e["time_s"] >= first_press and decode(e["segments"]).strip() == "01")
	sequence = [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] >= start - 0.25]
	cycle = [public for _, public in pairs]
	expected = (cycle * (len(sequence) // len(cycle) + 1))[: len(sequence)]
	if sequence != expected or len(sequence) < minimum * len(cycle):
		raise SystemExit("the solenoid test does not repeat its first cycle")
	return len(sequence) // len(cycle)


def addresses(run: dict, kind: str) -> list[int]:
	return sorted({e["number"] for e in run["events"] if e["event"] == kind})


def verify_switch_test(run: dict, run_name: str) -> list[dict]:
	"""Closing public N in the switch test makes the ROM show N on player 1's display, for N = 1..40.

	The display flashes, so the first display event between the closure and 0.05 s after its release
	that shows N is the frame read.
	"""
	switches = [e for e in run["events"] if e["event"] == "switch" and e["number"] > 0]
	events = display_events(run)
	shown, frames = [], []
	for index, event in enumerate(switches):
		if event["state"] != 1:
			continue
		release = next(x["time_s"] for x in switches[index + 1:] if x["number"] == event["number"] and x["state"] == 0)
		number = f"{event['number']:02d}"
		match = next((e for e in events if event["time_s"] <= e["time_s"] <= release + 0.05 and decode(e["segments"]).strip() == number), None)
		if match is None:
			raise SystemExit(f"the switch test did not show {number} for public {event['number']}")
		shown.append(event["number"])
		frames.append(frame(run_name, "display_event", f"{match['time_s']:.6f}", match["segments"], f"switch test shows {number} while public {event['number']} is closed"))
	if shown != list(range(1, 41)):
		raise SystemExit(f"the switch test covered {shown}")
	return frames


def steps_labelled(run: dict, label: str) -> dict:
	matches = [s for s in run["steps"] if s.get("label") == label]
	if len(matches) != 1:
		raise SystemExit(f"expected one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def fired(step: dict) -> list[int]:
	"""Outputs a step turned on, leaving out the coin lockout."""
	return sorted({t["number"] for t in step["transitions"]["solenoids"] if 1 in t["states"]} - {COIN_LOCKOUT})


def ended_off(step: dict) -> set[int]:
	return {t["number"] for t in step["transitions"]["solenoids"] if t["states"][-1] == 0}


def lamps_on(step: dict) -> set[int]:
	return {t["number"] for t in step["transitions"]["lamps"] if t["states"][-1] == 1}


def lamps_off(step: dict) -> set[int]:
	return {t["number"] for t in step["transitions"]["lamps"] if t["states"][-1] == 0}


def verify_gameplay(run: dict) -> list[dict]:
	findings = []
	for switch, coil in EXPECTED_COILS.items():
		step = steps_labelled(run, next(s["label"] for s in run["steps"] if s["type"] == "pulse" and s.get("switch") == switch))
		if fired(step) != [coil]:
			raise SystemExit(f"switch {switch} fired {fired(step)}, expected [{coil}]")
	for label, (coils, on, off) in EXPECTED_STEPS.items():
		step = steps_labelled(run, label)
		if fired(step) != coils:
			raise SystemExit(f"{label}: fired {fired(step)}, expected {coils}")
		if not on <= lamps_on(step) or not off <= lamps_off(step):
			raise SystemExit(f"{label}: lamps on {sorted(lamps_on(step))} off {sorted(lamps_off(step))}")
		findings.append({"step": label, "fired": coils, "lamps_on": sorted(lamps_on(step)), "lamps_off": sorted(lamps_off(step))})
	# The in-line bank completes without a reset coil; the right bank fires 9 on each completion.
	for label in ("public 22 2nd in-line drop target down", "public 21 3rd in-line drop target down"):
		if fired(steps_labelled(run, label)):
			raise SystemExit(f"{label} fired a coil")
	if 17 not in ended_off(steps_labelled(run, "public 25 saucer rollover button, gate open")):
		raise SystemExit("the saucer rollover did not drop the gate output")
	return findings


def verify_tilt(run: dict) -> None:
	step = steps_labelled(run, "tilt (public 7)")
	if sorted(ended_off(step)) != [19, 45, 46] or 61 not in lamps_on(step):
		raise SystemExit(f"the tilt dropped {sorted(ended_off(step))} and lit {sorted(lamps_on(step))}")
	held = steps_labelled(run, "right flipper button (public 82) held after tilt")
	if fired(held):
		raise SystemExit("the right flipper still fired after the tilt")
	if fired(steps_labelled(run, "right flipper button (public 82) held")) != [45, 46]:
		raise SystemExit("the right flipper button did not raise 45 and 46 before the tilt")


def verify_gate(run: dict) -> None:
	for label, (coils, off) in GATE_STEPS.items():
		step = steps_labelled(run, label)
		if fired(step) != coils or not off <= ended_off(step):
			raise SystemExit(f"gate run {label}: fired {fired(step)}, dropped {sorted(ended_off(step))}")
	add = steps_labelled(run, "credit button (public 6): add player 2 on ball 1")
	if any(t["number"] == 17 for t in add["transitions"]["solenoids"]):
		raise SystemExit("adding a player changed the gate output on the original ROM")


def score_frames(run: dict, run_name: str) -> list[dict]:
	labels = [snapshot["label"] for snapshot in run["snapshots"]]
	if labels.count(SCORE_FIRST) != 1 or labels.count(SCORE_LAST) != 1:
		raise SystemExit("the gameplay run does not have the cited score snapshots")
	frames = []
	for snapshot in run["snapshots"][labels.index(SCORE_FIRST): labels.index(SCORE_LAST) + 1]:
		displays = {d["index"]: d for d in snapshot["displays"]}
		if 0 not in displays or "segments" not in displays[0]:
			raise SystemExit(f"no player 1 display in snapshot {snapshot['label']!r}")
		frames.append(frame(run_name, "snapshot", snapshot["label"], displays[0]["segments"], f"player 1 score after {snapshot['label']}"))
	return frames


def check_frames(computed: list[dict], seed: dict) -> None:
	"""Refuse any cited frame that is not exactly the pinned one, and any pin that is not self-consistent."""
	pinned = seed["frames"]
	for item in pinned:
		if segments_sha256(item["segments"]) != item["segments_sha256"] or decode(item["segments"]).strip() != item["reading"]:
			raise SystemExit(f"pinned frame {item['run']} {item['key']} is not self-consistent")
	if len(computed) != len(pinned):
		raise SystemExit(f"{len(computed)} cited frames against {len(pinned)} pinned")
	for want, have in zip(pinned, computed):
		if want != have:
			raise SystemExit(f"cited frame {have['run']} {have['key']} ({have['cited_as']}) differs from the pinned frame")


def step_observations(run: dict, name: str) -> list[dict]:
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	items = []
	for step in run["steps"]:
		if step["type"] not in ("pulse", "set_switch"):
			continue
		snapshot = snapshots[step["label"]]
		transitioned = sorted({item["number"] for item in step["transitions"]["solenoids"]})
		items.append({
			"label": f"{name}: {step['label']}",
			"input_kind": "switch",
			"input_address": step["switch"],
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [step["switch"]],
			"active_solenoid_addresses": sorted(set(snapshot["active_solenoids"])),
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
		if run["scenario"]["sha256"] != entry["scenario_sha256"]:
			raise SystemExit(f"run {name} was made from a different scenario than {entry['scenario_path']}")
		entry["action_count"] = run["scenario"]["action_count"]
		entry["watch_switches"] = sorted(run["watch_switches"])
	else:
		entry["pulses"] = [{"switch": step["switch"], "hold_ms": step["hold_ms"], "settle_s": step["settle_s"]} for step in run["steps"] if step["type"] == "pulse"]
	if run["initial_switches"]:
		entry["initial_switches"] = sorted(run["initial_switches"], key=lambda item: item["switch"])
	return entry


def canonical_json(manifest: dict) -> bytes:
	return json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def cited_frames(loaded: dict) -> tuple[list[dict], list[tuple[int, int]]]:
	pairs, frames = solenoid_test_pairs(loaded["solenoid-test-frontier"], "solenoid-test-frontier")
	pairs_a, frames_a = solenoid_test_pairs(loaded["solenoid-test-frontiea"], "solenoid-test-frontiea")
	if pairs_a != pairs:
		raise SystemExit(f"frontiea pairs its solenoid test differently: {pairs_a}")
	frames = frames + frames_a
	frames += verify_switch_test(loaded["switch-test-frontier"], "switch-test-frontier")
	frames += score_frames(loaded["gameplay-frontier"], "gameplay-frontier")
	return frames, pairs


def build(runs: Path, rom_archives: dict[str, str], readings: dict, loaded: dict | None = None) -> dict:
	loaded = loaded if loaded is not None else {name: load_run(runs, name) for name in RUNS}
	for name, run in loaded.items():
		if run["failure"] is not None or run["library_sha256"] != LIBRARY_SHA256 or run["game"] != RUNS[name][1] or run["handle_mechanics"] != 0:
			raise SystemExit(f"run {name} is not a clean pinned-library run")
	frames, pairs = cited_frames(loaded)
	check_frames(frames, readings)
	reference = loaded["solenoid-test-frontier"]
	if dict(pairs) != EXPECTED_PAIRS or [n for n, _ in pairs] != list(range(1, 14)):
		raise SystemExit(f"the solenoid test pairing differs: {pairs}")
	cycles = verify_repeating_cycle(reference, pairs)
	lamps, solenoids = addresses(reference, "lamp"), addresses(reference, "solenoid")
	# Every run's published solenoid addresses: the solenoid test's, and the flipper pairs 45-48,
	# which only play raises.
	solenoids_seen = sorted({number for run in loaded.values() for number in addresses(run, "solenoid")})
	if solenoids_seen != sorted(set(solenoids) | FLIPPER_PAIRS):
		raise SystemExit(f"the runs published solenoid addresses {solenoids_seen}, not the solenoid test's and the flipper pairs")
	free_play = loaded["solenoid-test-frontiea"]
	if addresses(free_play, "lamp") != lamps or addresses(free_play, "solenoid") != solenoids or verify_repeating_cycle(free_play, pairs) < 2:
		raise SystemExit("frontiea differs from frontier in its solenoid test or published addresses")
	boot_outputs = sorted({e["number"] for e in reference["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] < BOOT_END_S})
	gameplay = loaded["gameplay-frontier"]
	findings = verify_gameplay(gameplay)
	verify_tilt(loaded["tilt-frontier"])
	verify_gate(loaded["gate-frontier"])
	after_boot = sorted({
		e["number"] for run in loaded.values() for e in run["events"]
		if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] >= BOOT_END_S
	})
	if any(address in after_boot for address in (1, 2, 3, 4, 5, 20)):
		raise SystemExit(f"an output the definition calls unused was driven after the boot: {after_boot}")
	scores = "; ".join(f"{item['key']} {item['reading']}" for item in frames if item["run"] == "gameplay-frontier")
	steps = "; ".join(
		f"{item['step']}: fired {item['fired'] or 'nothing'}, lamps on {item['lamps_on'] or 'none'}, off {item['lamps_off'] or 'none'}"
		for item in findings
	)
	observed: list[dict] = []
	observed.extend(step_observations(gameplay, "gameplay"))
	observed.extend(step_observations(loaded["tilt-frontier"], "tilt"))
	observed.extend(step_observations(loaded["gate-frontier"], "gate"))
	per_run = {
		"solenoid-test-frontier": {
			"ordered_solenoid_on_sequence": [public for _, public in pairs],
			"note": "Self-test pressed three times; the solenoid test then fires one output at a time while showing its number on every player display. Paired with the number on player 1's display 0.25 s after each pulse, in test order 1 to 13: "
			+ ", ".join(f"{number}->{public}" for number, public in pairs) + f". Every later pulse of the run follows the same order ({cycles} full cycles). Before the test, the boot drove outputs "
			+ ", ".join(map(str, boot_outputs)) + ": the PIA reset pulses 17-20 together at about 5.8 s, then at about 8.5 s the ROM kicks 10, 9 and 8, energizes the coin lockout (18) and blips the relay (19). "
			f"After the boot, across all six runs, only outputs {', '.join(map(str, after_boot))} were driven; 1-5 never were, and 20 only in the reset pulse. {len(frames)} display frames are pinned.",
		},
		"solenoid-test-frontiea": {"note": "Same pairing, cycle and published lamp and solenoid addresses as frontier."},
		"switch-test-frontier": {"note": "Self-test pressed five times (the fourth press ends the cycling solenoid test, the fifth starts the switch test, which flashes 0 on the match/ball display with everything open). Closing each of public 1 to 40 in turn made the ROM show that same number on the player displays (the first frame showing it between closure and release is pinned)."},
		"gameplay-frontier": {
			"note": "Coin on public 10, credit on public 6 with the ball held on the outhole (8): the start fired 7, 8, 9 and 10 and raised 19. One closure at a time: slingshots 37 and 36 fired 14 and 15; thumper bumpers 40, 39 and 38 fired 11, 12 and 13; the saucer (12) fired 10. "
			"The first in-line target (23) raised the gate output 17 and lit 15 and 40; the second (22) lit 57 and the third (21) lit 54, 56 and 58, firing no coil; the grizzly target (24) lit 52; the saucer rollover (25) dropped 17 once the gate was open. "
			"Each completion of the right bank 33-35 fired 9 and stepped the lamps 14 -> 30/31 -> 46/47 -> 60/62/63. The slingshots alternate lamps 44 and 60. The A, B and C lanes and the left, centre and right targets light the animal lamps and the bonus ladder as listed in steps. "
			"With lamp 12 lit the right feed lane (3) scored 15,000 and the left (4) 500; with lamp 60 lit the left outlane (5) fired the knocker (6) and lit the credit lamp 59, the right outlane (2) neither. "
			"Holding 84 raised the left pair 47 and 48 and holding 82 the right pair 45 and 46, each pair rising and falling together; holding 81 or 83 changed no output. The drain fired 7, 8 and 9. "
			f"Steps (coils fired, lamps whose final state changed): {steps}. "
			f"Player 1 score after each step, every frame pinned: {scores}.",
		},
		"tilt-frontier": {"note": "With a game running and the right flipper button held (45 and 46 raised), pulsing the tilt (7) dropped 19, 45 and 46 and lit lamp 61 (TILT); holding 82 again afterwards raised nothing."},
		"gate-frontier": {"note": "With the default option switches (S24, gate recall, off): the first in-line target (23) raised the gate output 17 on ball 1; adding a second player with the credit button left 17 raised; the drain fired 7, 8 and 9 and dropped 17."},
	}
	raw = [raw_run_entry(runs, name) for name in RUNS]
	manifest = build_manifest(runs, "frontier")
	digest = hashlib.sha256(canonical_json(manifest) + b"\n").hexdigest()
	files = len(manifest["files"])
	total = sum(item["size"] for item in manifest["files"])
	return {
		"driver_ids": ["frontier", "frontiea"],
		"extractor": {"id": "tools/frontier_runtime_summary.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["bally.frontier.1980"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": (
				"python tools/run_pinmame_harness.py --library <libpinmame> --game <driver> --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
				"{--boot-wait 30 --pulse=-7:250:1.2 --pulse=-7:250:1.2 --pulse=-7:250:1.2 --observe 40 | --scenario tools/harness-scenarios/by35/<scenario>.json} --output <external-run.json>; "
				f"handle-mechanics 0 and keyboard handling off for every run. The frontiea run used the ROM archive with SHA-256 {rom_archives['frontiea']}. "
				"The harness never calls PinmameSetDIP, so every run used the driver's input-port option-switch defaults from src/wpc/by35.h BY35_COMPORTS: S20 and S21 on, every other switch off. "
				"Each set_switch or pulse is a host stimulus, never a ROM observation; the display values are the harness's seven-segment words read as digits, every cited one pinned in tools/seeds/bally/frontier-1980-display-readings.json."
			),
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
			"game": "frontier",
			"observations": {
				"lamp_addresses_seen": lamps,
				"lamp_decoder_holes_not_seen": [16, 32, 48],
				"solenoid_addresses_seen": solenoids_seen,
				"public_solenoid_decoder_holes_not_seen": [16],
				"physical_service_solenoid_to_public": {str(number): public for number, public in pairs},
				"display_indices_seen": sorted({e["index"] for e in reference["events"] if e["event"] == "display"}),
				"named_action_observations": observed,
				"runs": per_run,
			},
			"raw_runs": raw,
			"rom_archive_sha256": rom_archives["frontier"],
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. The synthetic flipper pairs 45/46 and 47/48 are kept in the observations: 45 and 47 publish the same state as 46 and 48, and the BY35 controller profile declares all four.",
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
	readings = json.loads(READINGS_PATH.read_text(encoding="utf-8"))
	text = canonical_bytes(build(args.runs, ROM_ARCHIVES, readings))
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
