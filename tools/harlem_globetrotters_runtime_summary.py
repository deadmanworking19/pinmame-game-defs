#!/usr/bin/env python3
"""Build the compact runtime-evidence summary for Bally Harlem Globetrotters On Tour from its retained raw runs.

The raw LibPinMAME harness traces stay outside the repository. This tool reads them, derives every
observation the definition cites (the printed-number to public-address pairing of the ROM's
solenoid test on both drivers, the switch test's displayed numbers, the coil or lamp each playfield
switch drives in gameplay, the free-ball gate and flipper-enable reactions, the tilt), refuses runs
that do not show them, and writes ``evidence/runtime/by35/harlem-globetrotters-on-tour-1979-harness.json``.

Every display reading it cites is pinned in
``tools/seeds/bally/harlem-globetrotters-on-tour-1979-frame-readings.json`` by the run, the event's
time and display index, the SHA-256 of its segment words and the digits they show. A run whose cited
display event differs in any of those is refused, so a re-recorded or substituted frame cannot inherit
a reading. ``--pin-readings`` rewrites that seed from the runs; review it before committing.

    python tools/harlem_globetrotters_runtime_summary.py --runs <review-artifacts/harlem-globetrotters-on-tour-1979/runs> [--check | --pin-readings]
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

OUTPUT = ROOT / "evidence" / "runtime" / "by35" / "harlem-globetrotters-on-tour-1979-harness.json"
READINGS_PATH = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-frame-readings.json"
MACHINE_ID = "bally.harlem-globetrotters-on-tour.1979"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
SCENARIO_DIR = "tools/harness-scenarios/by35"
RETAINED_ROOT = "external:pinmame-review-artifacts/harlem-globetrotters-on-tour-1979/runs"
SEGMENTS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
# PinMAME raises 45 with 46 and 47 with 48 for the same held button; the coin-firing checks below ignore the duplicates.
FLIPPER_DUPLICATES = {45, 47}
COIN_LOCKOUT = 18

# name -> (directory, driver, scenario file)
RUNS = {
	"solenoid-test-hglbtrtr": ("solenoid-test", "hglbtrtr", "hglbtrtr-solenoid-test.json"),
	"solenoid-test-hglbtrtb": ("solenoid-test", "hglbtrtb", "hglbtrtr-solenoid-test.json"),
	"switch-test-hglbtrtr": ("switch-test", "hglbtrtr", "hglbtrtr-switch-test.json"),
	"switch-test-hglbtrtb": ("switch-test", "hglbtrtb", "hglbtrtr-switch-test.json"),
	"gameplay-hglbtrtr": ("gameplay", "hglbtrtr", "hglbtrtr-gameplay.json"),
	"gameplay-hglbtrtb": ("gameplay", "hglbtrtb", "hglbtrtr-gameplay.json"),
	"tilt-hglbtrtr": ("tilt", "hglbtrtr", "hglbtrtr-tilt.json"),
}
ROM_ARCHIVES = {
	"hglbtrtr": "e1bf1c869aa00e0cfc2d526eac265aca42cea94726192f974b0bf7b178083fad",
	"hglbtrtb": "a97ca0ec417a0edd442994934f3829638ec0860ca56e16a8ed671de152edaffa",
}
# Printed solenoid test number -> public address the ROM fires while it displays that number.
EXPECTED_PAIRS = {1: 7, 2: 6, 3: 13, 4: 14, 5: 12, 6: 11, 7: 9, 8: 8, 9: 10, 10: 15, 11: 18, 12: 19, 13: 17}
# Playfield switch -> the public coils its closure fires in gameplay.
EXPECTED_COILS = {37: [11], 36: [12], 40: [9], 39: [8], 38: [10], 24: [13], 32: [14, 15]}
# Switch -> a lamp its closure turns on in gameplay.
EXPECTED_LAMPS_ON = {24: 15, 3: 12, 2: 28, 1: 44, 32: 56, 25: 20, 30: 58, 35: 37}
# Players target -> the side-target lamp its closure puts out.
EXPECTED_LAMPS_OFF = {26: 10, 27: 57, 28: 41, 29: 25}
# Matrix positions the switch test reads and shows (five strobes); 41-48 show nothing.
SWITCH_TEST_RANGE = range(1, 41)


def decode(segments: list[int]) -> str:
	return "".join(SEGMENTS.get(value & 0x7F, "?") for value in segments)


def segments_sha256(segments: list[int]) -> str:
	return hashlib.sha256(json.dumps(segments, separators=(",", ":")).encode("ascii")).hexdigest()


def load_run(runs: Path, name: str) -> dict:
	directory, driver, _ = RUNS[name]
	return json.loads((runs / directory / driver / "run.json").read_text(encoding="utf-8"))


def display_events(run: dict, index: int = 0) -> list[dict]:
	return [e for e in run["events"] if e["event"] == "display" and e["index"] == index and "segments" in e]


def reading_of(event: dict) -> dict:
	return {"time_s": event["time_s"], "index": event["index"], "segments_sha256": segments_sha256(event["segments"]), "reading": decode(event["segments"]).strip()}


def verify_cited(pins: dict, name: str, label: str, event: dict) -> str:
	"""The pinned reading of one cited display event; refuses an event that is not the pinned one."""
	pinned = (pins.get(name) or {}).get(label)
	if pinned is None:
		raise SystemExit(f"{name}: no pinned reading for {label!r}")
	if reading_of(event) != pinned:
		raise SystemExit(f"{name}: the display event cited as {label!r} differs from its pinned reading {pinned}")
	return pinned["reading"]


def solenoid_test_events(run: dict) -> list[tuple[dict, dict]]:
	"""(solenoid on-event, the player-1 display event in effect 0.25 s later) for the first full cycle."""
	shown = display_events(run)
	times = [e["time_s"] for e in shown]
	pairs: list[tuple[dict, dict]] = []
	started = False
	for event in run["events"]:
		if event["event"] != "solenoid" or event["state"] != 1:
			continue
		position = bisect.bisect_right(times, event["time_s"] + 0.25) - 1
		if position < 0:
			continue
		text = decode(shown[position]["segments"]).strip()
		if not started:
			started = text == "01"
		if started and text.isdigit():
			if pairs and int(text) <= int(decode(pairs[-1][1]["segments"]).strip()):
				break
			pairs.append((event, shown[position]))
	return pairs


def solenoid_test_pairs(pins: dict, name: str, run: dict) -> list[tuple[int, int]]:
	return [(int(verify_cited(pins, name, f"solenoid test {int(decode(shown['segments']).strip()):02d}", shown)), pulse["number"]) for pulse, shown in solenoid_test_events(run)]


def verify_repeating_cycle(run: dict, pairs: list[tuple[int, int]], minimum: int = 2) -> int:
	"""After the test starts, every pulse follows the paired order, for at least `minimum` full cycles."""
	start = next(e["time_s"] for e in display_events(run) if decode(e["segments"]).strip() == "01")
	sequence = [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] >= start - 0.25]
	cycle = [public for _, public in pairs]
	expected = (cycle * (len(sequence) // len(cycle) + 1))[: len(sequence)]
	if sequence != expected or len(sequence) < minimum * len(cycle):
		raise SystemExit("the solenoid test does not repeat its first cycle")
	return len(sequence) // len(cycle)


def addresses(run: dict, kind: str) -> list[int]:
	return sorted({e["number"] for e in run["events"] if e["event"] == kind})


def switch_windows(run: dict) -> list[tuple[int, float, float]]:
	switches = [e for e in run["events"] if e["event"] == "switch" and e["number"] > 0]
	windows = []
	for index, event in enumerate(switches):
		if event["state"] != 1:
			continue
		release = next(x["time_s"] for x in switches[index + 1:] if x["number"] == event["number"] and x["state"] == 0)
		windows.append((event["number"], event["time_s"], release))
	return windows


def switch_test_events(run: dict) -> dict[int, dict]:
	"""Public N -> the first player-1 display event showing N while N is closed in the switch test.

	The display flashes, so every display event between the closure and 0.05 s after its release is read.
	"""
	shown = display_events(run)
	found: dict[int, dict] = {}
	for number, closed, release in switch_windows(run):
		window = [e for e in shown if closed <= e["time_s"] <= release + 0.05]
		match = next((e for e in window if decode(e["segments"]).strip() == f"{number:02d}"), None)
		if number in SWITCH_TEST_RANGE:
			if match is None:
				raise SystemExit(f"the switch test did not show {number:02d} for public {number}")
			found[number] = match
		elif any(decode(e["segments"]).strip() for e in window):
			raise SystemExit(f"the switch test showed something for public {number}")
	if sorted(found) != list(SWITCH_TEST_RANGE) or sorted(n for n, _, _ in switch_windows(run)) != list(range(1, 49)):
		raise SystemExit(f"the switch test covered {sorted(found)}")
	return found


def verify_switch_test(pins: dict, name: str, run: dict) -> None:
	for number, event in switch_test_events(run).items():
		if verify_cited(pins, name, f"switch test {number:02d}", event) != f"{number:02d}":
			raise SystemExit(f"{name}: switch test reading for {number} is not {number:02d}")
	# The ROM, not the host, fires the slingshot and bumper coils for their switches even in the switch test.
	for number, closed, release in switch_windows(run):
		fired_now = sorted({e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1 and closed <= e["time_s"] <= release + 0.6})
		want = EXPECTED_COILS.get(number) if number in (36, 37, 38, 39, 40) else []
		if fired_now != want:
			raise SystemExit(f"{name}: switch test closure {number} fired {fired_now}")


def power_up_version(pins: dict, name: str, run: dict) -> str:
	event = next(e for e in display_events(run) if decode(e["segments"]).strip() == "090")
	return verify_cited(pins, name, "power-up version", event)


def step_of(run: dict, switch: int, kind: str, state: int | None = None) -> dict:
	matches = [s for s in run["steps"] if s["type"] == kind and s.get("switch") == switch and (state is None or s.get("state") == state)]
	if len(matches) != 1:
		raise SystemExit(f"expected one {kind} step for switch {switch}, found {len(matches)}")
	return matches[0]


def labelled(run: dict, label: str) -> dict:
	matches = [s for s in run["steps"] if s.get("label") == label]
	if len(matches) != 1:
		raise SystemExit(f"expected one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def fired(step: dict) -> list[int]:
	"""Outputs a step turned on, leaving out the coin lockout (18), which the ROM drives on its own schedule."""
	return sorted({t["number"] for t in step["transitions"]["solenoids"] if 1 in t["states"]} - FLIPPER_DUPLICATES - {COIN_LOCKOUT})


def dropped(step: dict) -> list[int]:
	return sorted({t["number"] for t in step["transitions"]["solenoids"] if t["states"][-1] == 0} - FLIPPER_DUPLICATES - {COIN_LOCKOUT})


def lamps_on(step: dict) -> set[int]:
	return {t["number"] for t in step["transitions"]["lamps"] if t["states"][-1] == 1}


def lamps_off(step: dict) -> set[int]:
	return {t["number"] for t in step["transitions"]["lamps"] if t["states"][-1] == 0}


def switch_step(run: dict, switch: int) -> dict:
	held = [s for s in run["steps"] if s["type"] == "set_switch" and s.get("switch") == switch and s.get("state") == 1]
	if held:
		return step_of(run, switch, "set_switch", 1)
	return step_of(run, switch, "pulse")


def verify_gameplay_solenoids(run: dict) -> None:
	start = labelled(run, "credit button (public 6)")
	if fired(start) != [7, 15, 17, 19]:
		raise SystemExit(f"the game start fired {fired(start)}")
	for switch, coils in EXPECTED_COILS.items():
		if fired(switch_step(run, switch)) != coils:
			raise SystemExit(f"switch {switch} fired {fired(switch_step(run, switch))}, expected {coils}")
	for switch in (4, 3, 2, 1, 17, 25, 33, 26, 27, 28, 29, 30, 22, 31, 34):
		if fired(switch_step(run, switch)):
			raise SystemExit(f"switch {switch} fired {fired(switch_step(run, switch))}")
	dunk = switch_step(run, 35)
	if fired(dunk) or dropped(dunk) != [17]:
		raise SystemExit(f"the lit dunk shot target dropped {dropped(dunk)}")
	outlane = switch_step(run, 23)
	if fired(outlane) != [17]:
		raise SystemExit(f"the right outlane with the gate open fired {fired(outlane)}")
	left = step_of(run, 84, "set_switch", 1)
	right = step_of(run, 82, "set_switch", 1)
	if sorted({t["number"] for t in left["transitions"]["solenoids"] if 1 in t["states"]}) != [47, 48]:
		raise SystemExit("the left flipper button did not raise 47 and 48")
	if sorted({t["number"] for t in right["transitions"]["solenoids"] if 1 in t["states"]}) != [45, 46]:
		raise SystemExit("the right flipper button did not raise 45 and 46")
	for switch in (81, 83):
		if step_of(run, switch, "set_switch", 1)["transitions"]["solenoids"]:
			raise SystemExit(f"generic flipper position {switch} changed an output")
	drain = labelled(run, "public 8 outhole hold closed")
	if fired(drain) != [7, 15]:
		raise SystemExit(f"the drain fired {fired(drain)}")


def verify_gameplay_lamps(run: dict) -> None:
	for switch, lamp in EXPECTED_LAMPS_ON.items():
		if lamp not in lamps_on(switch_step(run, switch)):
			raise SystemExit(f"switch {switch} did not turn lamp {lamp} on")
	for switch, lamp in EXPECTED_LAMPS_OFF.items():
		if lamp not in lamps_off(switch_step(run, switch)):
			raise SystemExit(f"switch {switch} did not put lamp {lamp} out")
	if 37 not in lamps_off(switch_step(run, 23)):
		raise SystemExit("the right outlane did not put the gate-open lamp out")


def coin_lockout_during_bonus(run: dict) -> int:
	"""How many times the ROM re-energized the coin lockout while the outhole bonus counted down."""
	step = labelled(run, "public 8 outhole hold closed")["step"]
	drain = next(e["time_s"] for e in run["events"] if e["event"] == "switch" and e["number"] == 8 and e["state"] == 1 and e.get("step") == step)
	kick = next(e["time_s"] for e in run["events"] if e["event"] == "solenoid" and e["number"] == 7 and e["state"] == 1 and e["time_s"] > drain)
	return len([e for e in run["events"] if e["event"] == "solenoid" and e["number"] == COIN_LOCKOUT and e["state"] == 1 and drain - 1.0 < e["time_s"] < kick])


def verify_tilt(run: dict) -> None:
	held = step_of(run, 82, "set_switch", 1)
	if sorted({t["number"] for t in held["transitions"]["solenoids"] if 1 in t["states"]}) != [45, 46]:
		raise SystemExit("the right flipper did not fire before the tilt")
	step = step_of(run, 7, "pulse")
	gone = sorted({t["number"] for t in step["transitions"]["solenoids"] if t["states"][-1] == 0})
	if gone != [17, 19, 45, 46] or 61 not in lamps_on(step):
		raise SystemExit(f"the tilt dropped {gone} and lit {sorted(lamps_on(step))}")
	after = labelled(run, "public 84 left flipper button held after tilt")
	if after["transitions"]["solenoids"]:
		raise SystemExit("a flipper still fired after the tilt")
	drain = labelled(run, "public 8 ball drains to the outhole")
	if fired(drain) != [7, 15, 17, 19] or 61 not in lamps_off(drain):
		raise SystemExit(f"the next ball after the tilt fired {fired(drain)}")


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
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"transitioned_solenoid_addresses": transitioned,
			"result": "observed" if transitioned else "no_matching_transition",
		})
	return items


def raw_run_entry(runs: Path, name: str) -> dict:
	directory, driver, scenario = RUNS[name]
	path = runs / directory / driver / "run.json"
	run = json.loads(path.read_text(encoding="utf-8"))
	entry: dict = {
		"name": name,
		"sha256": file_sha256(path),
		"self_test_pulses": len([step for step in run["steps"] if step.get("switch") == -7]),
		"nvram_initialization": "empty; the run created its own isolated PinMAME state directory (state/ beside run.json) and sends no keyboard input",
		"snapshot_count": len(run["snapshots"]),
		"retained_from": f"{RETAINED_ROOT}/{directory}/{driver}/run.json",
		"scenario_path": f"{SCENARIO_DIR}/{scenario}",
		"scenario_sha256": file_sha256(ROOT / SCENARIO_DIR / scenario),
		"action_count": run["scenario"]["action_count"],
	}
	if run["watch_switches"]:
		entry["watch_switches"] = sorted(run["watch_switches"])
	if run["initial_switches"]:
		entry["initial_switches"] = sorted(run["initial_switches"], key=lambda item: item["switch"])
	return entry


def canonical_json(manifest: dict) -> bytes:
	return json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def check_clean(loaded: dict[str, dict]) -> None:
	for name, run in loaded.items():
		_, driver, scenario = RUNS[name]
		if run["failure"] is not None or run["library_sha256"] != LIBRARY_SHA256 or run["game"] != driver or run["handle_mechanics"] != 0:
			raise SystemExit(f"run {name} is not a clean pinned-library run")
		if run["scenario"]["sha256"] != file_sha256(ROOT / SCENARIO_DIR / scenario):
			raise SystemExit(f"run {name} used another scenario than {scenario}")


def pin_readings(runs: Path) -> dict:
	"""The display events this tool cites, read from the runs (for review before committing)."""
	loaded = {name: load_run(runs, name) for name in RUNS}
	check_clean(loaded)
	pins: dict[str, dict] = {}
	for driver in ("hglbtrtr", "hglbtrtb"):
		name = f"solenoid-test-{driver}"
		pins[name] = {f"solenoid test {int(decode(shown['segments']).strip()):02d}": reading_of(shown) for _, shown in solenoid_test_events(loaded[name])}
		name = f"switch-test-{driver}"
		pins[name] = {f"switch test {number:02d}": reading_of(event) for number, event in switch_test_events(loaded[name]).items()}
	event = next(e for e in display_events(loaded["solenoid-test-hglbtrtb"]) if decode(e["segments"]).strip() == "090")
	pins["solenoid-test-hglbtrtb"]["power-up version"] = reading_of(event)
	return {
		"format": "pinmame-segment-readings",
		"machine_id": MACHINE_ID,
		"note": (
			"Every player-1 display event the compact runtime evidence cites, pinned by run, event time, display index, the SHA-256 of the event's seven-segment words "
			"(compact JSON of the list, as the harness recorded it) and the digits they show (segment words decoded with the standard 0-9 seven-segment patterns, blanks stripped). "
			"tools/harlem_globetrotters_runtime_summary.py refuses a run whose cited event differs in any of them."
		),
		"runs": pins,
	}


def build(runs: Path) -> dict:
	pins = json.loads(READINGS_PATH.read_text(encoding="utf-8"))["runs"]
	loaded = {name: load_run(runs, name) for name in RUNS}
	check_clean(loaded)
	reference = loaded["solenoid-test-hglbtrtr"]
	pairs = solenoid_test_pairs(pins, "solenoid-test-hglbtrtr", reference)
	if dict(pairs) != EXPECTED_PAIRS or [n for n, _ in pairs] != list(range(1, 14)):
		raise SystemExit(f"the solenoid test pairing differs: {pairs}")
	cycles = verify_repeating_cycle(reference, pairs)
	lamps, solenoids = addresses(reference, "lamp"), addresses(reference, "solenoid")
	variant = loaded["solenoid-test-hglbtrtb"]
	if solenoid_test_pairs(pins, "solenoid-test-hglbtrtb", variant) != pairs or addresses(variant, "lamp") != lamps or addresses(variant, "solenoid") != solenoids:
		raise SystemExit("hglbtrtb differs from hglbtrtr in its solenoid test or published addresses")
	if verify_repeating_cycle(variant, pairs) < 2:
		raise SystemExit("hglbtrtb does not repeat its solenoid test")
	version = power_up_version(pins, "solenoid-test-hglbtrtb", variant)
	if any(len(e["segments"]) != 7 for e in display_events(variant)) or any(len(e["segments"]) != 6 for e in display_events(reference)):
		raise SystemExit("the player displays are not six digits on hglbtrtr and seven on hglbtrtb")
	power_on = sorted({e["number"] for e in reference["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] < 6.0})
	if power_on != [17, 18, 19, 20]:
		raise SystemExit(f"the power-on pulse drove {power_on}")
	for driver in ("hglbtrtr", "hglbtrtb"):
		verify_switch_test(pins, f"switch-test-{driver}", loaded[f"switch-test-{driver}"])
		verify_gameplay_solenoids(loaded[f"gameplay-{driver}"])
	gameplay = loaded["gameplay-hglbtrtr"]
	verify_gameplay_lamps(gameplay)
	tilt = loaded["tilt-hglbtrtr"]
	verify_tilt(tilt)
	lockout_pulses = coin_lockout_during_bonus(gameplay)
	if lockout_pulses < 3 or coin_lockout_during_bonus(loaded["gameplay-hglbtrtb"]) != lockout_pulses:
		raise SystemExit("the coin lockout behaviour during the bonus count differs")
	# After the power-on pulse, nothing drives 1-5, 16 or 20.
	in_game = sorted({e["number"] for run in loaded.values() for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] >= 6.0})
	if any(a in in_game for a in (1, 2, 3, 4, 5, 16, 20)):
		raise SystemExit(f"an output the definition calls unused was driven: {in_game}")
	observed: list[dict] = []
	for name in ("gameplay-hglbtrtr", "tilt-hglbtrtr"):
		observed.extend(step_observations(loaded[name], name.split("-")[0]))
	per_run = {
		"solenoid-test-hglbtrtr": {
			"ordered_solenoid_on_sequence": [public for _, public in pairs],
			"note": "Self-test pressed three times after a 30 s boot; the solenoid test then fires one output at a time while showing its number on every player display. Paired with the number on player 1's display 0.25 s after each pulse, in test order 1 to 13: "
			+ ", ".join(f"{number}->{public}" for number, public in pairs) + f". Every later pulse of the run follows the same order ({cycles} full cycles). Before the test the power-on reset pulsed outputs "
			+ ", ".join(map(str, power_on)) + " together, and the ROM's start-up fired the saucer kickers (13, 14) and the drop-target reset (15) and raised the gate (17), the coin lockout (18) and the flipper relay (19).",
		},
		"solenoid-test-hglbtrtb": {"note": f"Same pairing, cycle and published lamp and solenoid addresses as hglbtrtr. The player displays carry seven digits, and at power-up player 1 shows {version}, the conversion's revision."},
		"switch-test-hglbtrtr": {"note": "Self-test pressed five times (the fourth press ends the cycling solenoid test, the fifth starts the switch test). Closing each of public 1 to 40 alone made the ROM show that number on the player displays; closing 41 to 48 showed nothing. The ROM fired the slingshot and thumper bumper coils for their switches in the switch test too (36->12, 37->11, 38->10, 39->8, 40->9)."},
		"switch-test-hglbtrtb": {"note": "Same as hglbtrtr: 1 to 40 shown, 41 to 48 not, and the same slingshot and bumper coils fired."},
		"gameplay-hglbtrtr": {"note": (
			"Coin on public 10, credit on public 6 with the ball held on the outhole (8): the start fired 7 and 15 and raised 17 and 19. One closure at a time: slingshots 37 and 36 fired 11 and 12; thumper bumpers 40, 39 and 38 fired 9, 8 and 10; "
			"the globe saucer 24 fired 13 and lit the centre G (15). Drop targets 4, 3, 2 and 1 fired nothing; the second lit 2X (12), the third 3X (28) and the fourth 5X (44). The target saucer 32 with all four down fired 14 and 15 and lit the saucer target special (56). "
			"The centre right spinner 25 lit lamp 20. Players targets 26, 27, 28 and 29 put out lamps 10, 57, 41 and 25; the fifth (30) relit them and lit lamp 58. The dunk shot target 35 dropped 17 and lit lamp 37; the right outlane 23 raised 17 again and put 37 out. "
			"Holding 84 raised 47 and 48 and holding 82 raised 45 and 46; holding 81 or 83 changed no output. The drain fired 7 and 15. "
			f"While the outhole bonus counted down, the ROM dropped the coin lockout (18) and raised it {lockout_pulses} times before the outhole kick, each time for a few tens of milliseconds except the last, which it held."
		)},
		"gameplay-hglbtrtb": {"note": "The same stimuli fired the same solenoids at every step as on hglbtrtr, including the coin lockout's behaviour during the bonus count; lamp observations are cited from hglbtrtr only."},
		"tilt-hglbtrtr": {"note": "With a game running and the right flipper button held (45 and 46 up), pulsing the tilt (7) dropped 17, 19, 45 and 46 and lit lamp 61 (TILT); holding 84 afterwards raised nothing. At the drain the next ball fired 7 and 15, raised 17 and 19 and put 61 out."},
	}
	raw = [raw_run_entry(runs, name) for name in RUNS]
	manifest = build_manifest(runs, "hglbtrtr")
	digest = hashlib.sha256(canonical_json(manifest) + b"\n").hexdigest()
	files = len(manifest["files"])
	total = sum(item["size"] for item in manifest["files"])
	return {
		"driver_ids": ["hglbtrtr", "hglbtrtb"],
		"extractor": {"id": "tools/harlem_globetrotters_runtime_summary.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": (
				"python tools/run_pinmame_harness.py --library <libpinmame> --game <driver> --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --handle-mechanics 0 "
				"--scenario tools/harness-scenarios/by35/<scenario>.json --output <external-run.json>; keyboard handling off for every run. "
				f"Runs of hglbtrtb used the ROM archive with SHA-256 {ROM_ARCHIVES['hglbtrtb']}. "
				"Each set_switch or pulse is a host stimulus, never a ROM observation; the display values are the harness's seven-segment words read as digits, and every cited one is pinned in tools/seeds/bally/harlem-globetrotters-on-tour-1979-frame-readings.json "
				f"(SHA-256 {file_sha256(READINGS_PATH)}). observations.switch_to_lamp lists the lamp each closure lit in the hglbtrtr gameplay run; the lamps closures put out and the coils they fired are in the gameplay run note and named_action_observations."
			),
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
			"game": "hglbtrtr",
			"observations": {
				"lamp_addresses_seen": lamps,
				"lamp_decoder_holes_not_seen": [16, 32, 48],
				"solenoid_addresses_seen": solenoids,
				"public_solenoid_decoder_holes_not_seen": [16],
				"physical_service_solenoid_to_public": {str(number): public for number, public in pairs},
				"switch_to_lamp": {str(switch): lamp for switch, lamp in sorted(EXPECTED_LAMPS_ON.items())},
				"display_indices_seen": sorted({e["index"] for e in reference["events"] if e["event"] == "display"}),
				"named_action_observations": observed,
				"runs": per_run,
			},
			"raw_runs": raw,
			"rom_archive_sha256": ROM_ARCHIVES["hglbtrtr"],
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. PinMAME raises its generic flipper outputs in pairs, 45 with 46 for the right button and 47 with 48 for the left, and the observations keep both members of each pair.",
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
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--pin-readings", action="store_true")
	args = parser.parse_args()
	if args.pin_readings:
		READINGS_PATH.write_bytes((json.dumps(pin_readings(args.runs), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
		print(f"wrote {READINGS_PATH.relative_to(ROOT).as_posix()}")
		return 0
	text = canonical_bytes(build(args.runs))
	if args.check:
		if not OUTPUT.exists() or OUTPUT.read_bytes() != text:
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
