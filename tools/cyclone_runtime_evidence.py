"""Summarize the retained Cyclone harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/cyclone-1988/harness/<run>/`` (written by ``tools/run_pinmame_harness.py`` with the pinned
library). Each run directory holds its own initialization run (``init.json``, scenario
``cycln-nvram-init.json``, booted from an empty state directory) and then the evidentiary run (``run.json``)
started from the NVRAM that initialization wrote. The builder checks that every run succeeded on the pinned
emulator binary with an unchanged committed scenario, and writes one evidence file per ROM revision under
``evidence/runtime/system-11/``.

Display readings are decoded from the raw segment values: the player 1 and 2 displays (controller indices 0 and
1) are seven 16-segment characters each, joined with a space, where the low fifteen bits are the glyph, bit 15 the
period, the ROM draws the numeral 1 as 0x0006 and one glyph serves 0 and O and another 5 and S (written O and S);
the player 3 and 4 displays (indices 2 and 3) are seven-segment digits, whose letter-shaped patterns are written
A, C, d, E, H, L, r, and a lone upper-right or upper-left segment as an apostrophe. Every reading cited is pinned with the SHA-256 of its whole four-display frame in
``tools/seeds/williams/cyclone-1988-display-frames.json``; a run whose cited frame or reading differs is refused
until the new frame has been read again and the seed updated by the curator (``--pin-frames``). Each Coil Test
and Switch Levels reading is also checked against the ROM's own name table.

    python tools/cyclone_runtime_evidence.py               # write
    python tools/cyclone_runtime_evidence.py --check       # re-derive and compare, write nothing
    python tools/cyclone_runtime_evidence.py --pin-frames  # curator only: rewrite the frame seed from the runs
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402
from run_pinmame_harness import SEGMENT_16_CHARACTERS  # noqa: E402
import cyclone_data as data  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

GAME = "cycln_l5"
SCENARIO_DIRECTORY = "tools/harness-scenarios/system-11"
INIT_SCENARIO = f"{SCENARIO_DIRECTORY}/cycln-nvram-init.json"
HARNESS_RELATIVE = Path("cyclone-1988/harness")
SOURCE_PATH = "external:pinmame-review-artifacts/cyclone-1988/harness"
FRAME_SEED_PATH = ROOT / "tools/seeds/williams/cyclone-1988-display-frames.json"
EVIDENCE_PATHS = {
	"cycln_l5": ROOT / "evidence/runtime/system-11/cyclone-l5-service-and-mechanisms.json",
	"cycln_l4": ROOT / "evidence/runtime/system-11/cyclone-l4-coil-test.json",
	"cycln_l1": ROOT / "evidence/runtime/system-11/cyclone-l1-coil-test.json",
}
RUNS = {
	"cycln_l5": (
		"coil-test-l5", "single-lamps-l5", "switch-levels-l5", "wheel-test-41-0-l5", "wheel-test-41-1-l5",
		"wheel-test-reactive-l5", "boot-baseline-l5", "boot-held-l5", "gameplay-l5",
	),
	"cycln_l4": ("coil-test-l4",),
	"cycln_l1": ("coil-test-l1",),
}
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (each "
	"run directory's init.json, init.log, run.json and run.log and every state-directory file, including the NVRAM the "
	"initialization wrote and the run then rewrote) except manifest.json and manifest.sha256, sorted by POSIX relative "
	"path. tools/build_external_evidence_manifest.py writes and re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game <set> --rom-path <vpinmame-roms> "
	"--work-dir <run>/state --scenario tools/harness-scenarios/system-11/cycln-nvram-init.json --output <run>/init.json, "
	"then the same command with --scenario tools/harness-scenarios/system-11/cycln-<name>.json --output <run>/run.json in "
	"the same, newly created state directory. Diagnostic scenarios wait 8 s, set Manual-Down (-6 = 0), pulse Advance (-7) "
	"to enter the tests, set Auto-Up (-6 = 1) and pulse Advance until the test's title is displayed."
)
STATIC_LIMITATION = (
	"Static host switches only; the harness never moves a ball or a mechanism, so repeated pulses are ROM retries against a "
	"host-held switch."
)
SCRIPTED_LIMITATION = (
	"The host answers the ROM's drives with fixed, scripted switch changes; a pulse the ROM fires proves only that the address "
	"changed under these conditions, not a mechanism's travel time or the physical device's identity."
)
REACTIVE_LIMITATION = (
	"The home closure is a synthetic host write on a fixed schedule, not a measurement of the wheel; the run shows only how the "
	"ROM's display and drive react to one closure of 41."
)
ROM_GLYPHS = {0x0006: "1"}
SEGMENT_7 = {
	0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " ",
	0x40: "-", 0x77: "A", 0x39: "C", 0x5E: "d", 0x79: "E", 0x76: "H", 0x38: "L", 0x50: "r", 0x02: "'", 0x20: "'",
}
# Attract-mode G.I. relays, the A/C relay and the C-side flasher bank repeat for as long as the game is idle and say
# nothing about the probed device.
ATTRACT_BACKGROUND = {10, 11, 12, 25, 26, 27, 28, 29, 30, 31, 32}
# Gameplay switch -> the special solenoid the ROM fired while it was closed (Solenoid Table pairing).
SPECIAL_RESPONSES = {60: 17, 61: 19, 62: 21, 63: 18, 64: 20}
WHEEL_SNAPSHOTS = {
	"wheel-test-41-0-l5": ("locate WHEEL TEST", "observe the automatic wheel test"),
	"wheel-test-41-1-l5": ("locate WHEEL TEST", "observe the automatic wheel test"),
	"wheel-test-reactive-l5": (
		# "home opto opens" is left out: its snapshot is taken at the instant of the release, before the display updates.
		"locate WHEEL TEST", "wheel stepping", "home opto closes (synthetic flag)", "observe the rest of the wheel test",
	),
}


def working_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is required: the raw runs live under the working root's review-artifacts")
	return Path(value).expanduser().resolve()


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_alpha(values: list[int]) -> str:
	text = []
	for value in values:
		glyph = ROM_GLYPHS.get(value & 0x7FFF, SEGMENT_16_CHARACTERS.get(value & 0x7FFF))
		text.append(("?" if value & 0x7FFF else " ") if glyph is None else glyph)
		if value & 0x8000:
			text.append(".")
	return "".join(text)


def decode_numeric(values: list[int]) -> str:
	return "".join(SEGMENT_7.get(value & 0x7F, "?") for value in values)


def normalized(text: str) -> str:
	return " ".join(text.split())


def rom_folded(text: str) -> str:
	"""A ROM name as the display draws it: one glyph for 0 and O, one for 5 and S, and the ROM's 'p' as a slash."""
	return normalized(text.replace("p", "/").replace("0", "O").replace("5", "S")).replace(" ", "")


def frame_digest(frame: tuple[tuple[int, ...], ...]) -> str:
	return hashlib.sha256(json.dumps([list(row) for row in frame], separators=(",", ":")).encode("ascii")).hexdigest()


def frame_reading(frame: tuple[tuple[int, ...], ...]) -> str:
	return f"{normalized(decode_alpha(list(frame[0])) + ' ' + decode_alpha(list(frame[1])))} | {decode_numeric(list(frame[2]))} | {decode_numeric(list(frame[3]))}"


def scenario_for(name: str) -> str:
	return f"{SCENARIO_DIRECTORY}/cycln-{name.rsplit('-', 1)[0]}.json"


def load_run(harness: Path, name: str, game: str) -> dict[str, Any]:
	directory = harness / name
	init = json.loads((directory / "init.json").read_text(encoding="utf-8"))
	run = json.loads((directory / "run.json").read_text(encoding="utf-8"))
	for label, record, scenario in (("initialization", init, INIT_SCENARIO), ("run", run, scenario_for(name))):
		if record.get("failure") is not None or record.get("game") != game:
			raise RuntimeError(f"{name}: the {label} is not a successful {game} run")
		if record.get("library_sha256") != data.LIBRARY_SHA256:
			raise RuntimeError(f"{name}: the {label} was not produced by the pinned library")
		if record.get("handle_mechanics") != 0:
			raise RuntimeError(f"{name}: the {label} ran with PinMAME mechanics enabled")
		if record["scenario"]["sha256"] != sha256(ROOT / scenario):
			raise RuntimeError(f"{name}: the {label} scenario drifted from {scenario}")
	return run


def frames(run: dict[str, Any]) -> list[tuple[float, tuple[tuple[int, ...], ...]]]:
	rows: dict[int, tuple[int, ...]] = {index: () for index in range(4)}
	timeline = []
	for event in run["events"]:
		if event["event"] == "display" and event.get("index") in rows and isinstance(event.get("segments"), list):
			rows[event["index"]] = tuple(event["segments"])
			timeline.append((event["time_s"], tuple(rows[index] for index in range(4))))
	return timeline


def frame_at(timeline: list[tuple[float, tuple[tuple[int, ...], ...]]], time: float) -> tuple[tuple[int, ...], ...]:
	current: tuple[tuple[int, ...], ...] = ((), (), (), ())
	for at, frame in timeline:
		if at > time:
			break
		current = frame
	return current


def longest_frame(timeline: list[tuple[float, tuple[tuple[int, ...], ...]]], start: float, end: float) -> tuple[tuple[int, ...], ...]:
	durations: dict[tuple[tuple[int, ...], ...], float] = {}
	current, at = frame_at(timeline, start), start
	for when, frame in timeline:
		if when <= start:
			continue
		if when >= end:
			break
		durations[current] = durations.get(current, 0.0) + (when - at)
		current, at = frame, when
	durations[current] = durations.get(current, 0.0) + (end - at)
	return max(sorted(durations), key=lambda frame: durations[frame])


def snapshot_frame(run: dict[str, Any], label: str) -> tuple[tuple[int, ...], ...]:
	snapshot = next(item for item in run["snapshots"] if item.get("label") == label)
	displays = {display["index"]: tuple(display["segments"]) for display in snapshot["displays"] if isinstance(display.get("segments"), list)}
	return tuple(displays[index] for index in range(4))


def solenoid_spans(run: dict[str, Any]) -> dict[int, list[tuple[float, float | None]]]:
	open_at: dict[int, float] = {}
	spans: dict[int, list[tuple[float, float | None]]] = {}
	for event in run["events"]:
		if event["event"] != "solenoid":
			continue
		number, time = event["number"], round(event["time_s"], 3)
		if event["state"]:
			open_at.setdefault(number, time)
		elif number in open_at:
			spans.setdefault(number, []).append((open_at.pop(number), time))
	for number, time in open_at.items():
		spans.setdefault(number, []).append((time, None))
	return spans


def describe_spans(spans: dict[int, list[tuple[float, float | None]]], end: float, skip: set[int] = ATTRACT_BACKGROUND) -> str:
	parts = []
	for number in sorted(spans):
		if number in skip:
			continue
		items = spans[number]
		if len(items) <= 3:
			parts.append(f"{number}: " + ", ".join(f"{a}-{'end' if b is None else b} s" for a, b in items))
		else:
			gaps = [round(items[i + 1][0] - items[i][0], 2) for i in range(len(items) - 1)]
			parts.append(f"{number}: {len(items)} pulses from {items[0][0]} s to {items[-1][0]} s, spacing {min(gaps)}-{max(gaps)} s")
	return "; ".join(parts) + f" (observed to {end} s)"


def end_time(run: dict[str, Any]) -> float:
	return round(max(event["time_s"] for event in run["events"]), 3)


def service_pulses(run: dict[str, Any]) -> int:
	total = 0
	for step in run["steps"]:
		if step.get("type") == "pulse" and step.get("switch") == -7:
			total += 1
		elif step.get("type") == "pulse_until_display" and step.get("switch") == -7:
			total += step["pulses"]
	return total


def checkpoints(run: dict[str, Any]) -> list[dict[str, Any]]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]} for step in run["steps"] if step.get("type") == "pulse_until_display"]


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------------------------------------------------------------- service tests


def coil_test(run: dict[str, Any], cited: dict[str, tuple[str, str]]) -> list[dict[str, Any]]:
	"""Each coil-test pulse with its step number (player 3 display) and name, for two identical cycles."""
	timeline = frames(run)
	begin = next(at for at, frame in timeline if normalized(decode_alpha(list(frame[0])) + " " + decode_alpha(list(frame[1]))) == "COIL TEST")
	pulses = []
	for event in run["events"]:
		if event["event"] != "solenoid" or not event["state"] or event["time_s"] <= begin or event["number"] == 23:
			continue
		frame = frame_at(timeline, event["time_s"])
		step_text = normalized(decode_numeric(list(frame[2])))
		match = re.fullmatch(r"05 (\d\d)", step_text)
		if not match:
			raise RuntimeError(f"coil test pulse of {event['number']} at {event['time_s']} s shows no step number ({step_text!r})")
		step = int(match.group(1))
		# The A/C select relay (12) is switched around every C-side pulse; it is a step of its own only at step 12.
		if event["number"] == 12 and step != 12:
			continue
		pulses.append({"step": step, "address": event["number"], "frame": frame})
	period = next(index for index in range(2, len(pulses)) if pulses[index]["address"] == pulses[0]["address"])
	first, second = pulses[:period], pulses[period:2 * period]
	if [(p["step"], p["address"]) for p in first] != [(p["step"], p["address"]) for p in second]:
		raise RuntimeError("coil test second cycle differs from the first")
	expected = []
	for step in range(1, 23):
		if step in data.COIL_TEST_SKIPPED_STEPS:
			continue
		expected += [(step, step), (step, step + 24)] if step <= 8 else [(step, step)]
	if [(p["step"], p["address"]) for p in first] != expected:
		raise RuntimeError(f"coil test steps differ from the expected A/C walk: {[(p['step'], p['address']) for p in first]}")
	results = []
	for pulse in first:
		label = f"coil step {pulse['step']:02d} public {pulse['address']}"
		reading = frame_reading(pulse["frame"])
		cited[label] = (frame_digest(pulse["frame"]), reading)
		first_name, second_name = data.ROM_COIL_STEPS[pulse["step"]]
		name = second_name if pulse["address"] > 24 else first_name
		shown = reading.split(" | ")[0]
		if shown.replace(" ", "") != rom_folded(name):
			raise RuntimeError(f"{label}: the display reads {shown!r}, not the ROM's coil name {name!r}")
		side = reading.split(" | ")[2]
		results.append({"step": pulse["step"], "address": pulse["address"], "display": shown, "player_4": normalized(side)})
	return results


def relay_spans(run: dict[str, Any], steps: list[dict[str, Any]]) -> list[int]:
	"""Addresses whose first coil-test pulse falls inside an energized span of the A/C relay (12)."""
	relay = solenoid_spans(run).get(12, [])
	timeline = frames(run)
	begin = next(at for at, frame in timeline if normalized(decode_alpha(list(frame[0])) + " " + decode_alpha(list(frame[1]))) == "COIL TEST")
	rises = [(event["time_s"], event["number"]) for event in run["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] > begin]
	held = []
	for step in steps:
		time = next(t for t, n in rises if n == step["address"])
		if step["address"] != 12 and any(a <= time and (b is None or time < b) for a, b in relay):
			held.append(step["address"])
	if held != list(range(25, 33)):
		raise RuntimeError(f"the A/C relay was held for {held}, not exactly the C-side bank 25-32")
	return held


def single_lamps(run: dict[str, Any], cited: dict[str, tuple[str, str]]) -> list[dict[str, Any]]:
	timeline = frames(run)
	presses = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event.get("number") == 3 and event.get("state") == 1]
	steps = [step for step in run["steps"] if step.get("label", "").startswith(("Credit: step to designator", "first lamp"))]
	title = next(at for at, frame in timeline if normalized(decode_alpha(list(frame[0])) + " " + decode_alpha(list(frame[1]))) == "SINGLE LAMPS")
	begin = next(at for at, frame in timeline if at > title and normalized(decode_alpha(list(frame[0])) + " " + decode_alpha(list(frame[1]))) != "SINGLE LAMPS")
	bounds = [begin] + presses + [end_time(run)]
	results = []
	for index, step in enumerate(steps):
		designator = 1 if step["label"].startswith("first lamp") else int(step["label"].rsplit(" ", 1)[1])
		start, end = bounds[index] + 0.3, bounds[index + 1]
		blinked = sorted({event["number"] for event in run["events"] if event["event"] == "lamp" and start <= event["time_s"] < end})
		if blinked != [designator]:
			raise RuntimeError(f"single lamps designator {designator} blinked {blinked}")
		frame = longest_frame(timeline, start, end)
		reading = frame_reading(frame)
		label = f"lamp designator {designator:02d}"
		cited[label] = (frame_digest(frame), reading)
		shown, number = reading.split(" | ")[0], normalized(reading.split(" | ")[1])
		if number != f"04 {designator:02d}":
			raise RuntimeError(f"{label}: the player 3 display reads {number!r}")
		if shown.replace(" ", "") != rom_folded(data.ROM_LAMP_NAMES[designator]):
			raise RuntimeError(f"{label}: the display reads {shown!r}, not the ROM's lamp name {data.ROM_LAMP_NAMES[designator]!r}")
		results.append({"designator": designator, "address": designator, "display": shown})
	if [item["designator"] for item in results] != list(range(1, 65)):
		raise RuntimeError("single lamps did not step through designators 01-64")
	return results


def switch_levels(run: dict[str, Any], cited: dict[str, tuple[str, str]]) -> list[dict[str, Any]]:
	results = []
	frame = snapshot_frame(run, "no switch closed")
	cited["no switch closed"] = (frame_digest(frame), frame_reading(frame))
	for step in run["steps"]:
		label = step.get("label", "")
		if not label.startswith("hold public switch"):
			continue
		address = int(label.rsplit(" ", 1)[1])
		snapshot_label = label + " (held)"
		snapshot = next(item for item in run["snapshots"] if item.get("label") == snapshot_label)
		held = {item["number"]: item["state"] for item in snapshot["watched_switches"]}
		if held.get(address) != 1:
			raise RuntimeError(f"{snapshot_label}: the switch is not held at 1")
		frame = snapshot_frame(run, snapshot_label)
		reading = frame_reading(frame)
		cited[snapshot_label] = (frame_digest(frame), reading)
		name, number = reading.split(" | ")[0], normalized(reading.split(" | ")[1])
		shown_address = {82: 58, 84: 57}.get(address, address)
		if address <= 64 or address in (82, 84):
			if number != f"06 {shown_address:02d}" or name.replace(" ", "") != rom_folded(data.ROM_SWITCH_NAMES[shown_address]):
				raise RuntimeError(f"{snapshot_label}: the Switch Levels test reads {reading!r}")
		elif number != "06" or name != "SWITCH LEVELS":
			raise RuntimeError(f"{snapshot_label}: a flipper-column position other than 82 and 84 showed {reading!r}")
		results.append({"address": address, "name": name, "number": number, "solenoids": sorted(snapshot["active_solenoids"])})
	if [item["address"] for item in results] != list(range(1, 65)) + list(range(81, 89)):
		raise RuntimeError("switch levels did not hold every public address 1-64 and 81-88")
	return results


def wheel_test(name: str, run: dict[str, Any], cited: dict[str, tuple[str, str]]) -> str:
	parts = []
	for label in WHEEL_SNAPSHOTS[name]:
		frame = snapshot_frame(run, label)
		reading = frame_reading(frame)
		cited[label] = (frame_digest(frame), reading)
		snapshot = next(item for item in run["snapshots"] if item.get("label") == label)
		level = {item["number"]: item["state"] for item in snapshot["watched_switches"]}[41]
		parts.append(f"\"{label}\" (41 = {level}): {reading}")
	readings = [cited[label][1].split(" | ") for label in WHEEL_SNAPSHOTS[name]]
	if readings[0][0] != "M. WHEEL TEST" or normalized(readings[0][1]) != "08":
		raise RuntimeError(f"{name}: the run did not reach the Mystery Wheel Test")
	# Player 4's left digit is the home indicator: "H" while the ROM reads 41 open, blank while it reads 41 closed.
	for label, reading in zip(WHEEL_SNAPSHOTS[name][1:], readings[1:]):
		snapshot = next(item for item in run["snapshots"] if item.get("label") == label)
		level = {item["number"]: item["state"] for item in snapshot["watched_switches"]}[41]
		if (reading[2][0] == "H") != (level == 0):
			raise RuntimeError(f"{name} {label!r}: home indicator {reading[2][0]!r} with 41 = {level}")
	return "; ".join(parts)


# ---------------------------------------------------------------- gameplay


def gameplay_actions(run: dict[str, Any]) -> list[dict[str, Any]]:
	"""Each scripted gameplay switch action with the solenoids that rose in its window."""
	# The harness takes one snapshot at boot and one at the end of every step, in step order, so step k's window runs from
	# snapshot k to snapshot k + 1.
	snapshots = run["snapshots"]
	if len(snapshots) != len(run["steps"]) + 1 or [item["label"] for item in snapshots[1:]] != [step["label"] for step in run["steps"]]:
		raise RuntimeError("gameplay snapshots do not follow the steps one to one")
	actions = []
	for index, step in enumerate(run["steps"]):
		if step.get("type") not in ("pulse", "set_switch") or step.get("switch") is None:
			continue
		start, end = snapshots[index]["time_s"], snapshots[index + 1]["time_s"]
		risen = sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"] and start < event["time_s"] <= end})
		actions.append({"label": step["label"], "switch": step["switch"], "state": step.get("state", 1), "risen": risen})
	return actions


def gameplay_observations(run: dict[str, Any]) -> list[dict[str, Any]]:
	observed = []
	actions = {action["switch"]: action for action in gameplay_actions(run) if action["switch"] in SPECIAL_RESPONSES}
	for switch, coil in sorted(SPECIAL_RESPONSES.items()):
		action = actions[switch]
		specials = [number for number in action["risen"] if 17 <= number <= 22]
		if specials != [coil]:
			raise RuntimeError(f"gameplay: closing {switch} raised specials {specials}, not {coil}")
		observed.append({
			"label": action["label"], "input_kind": "switch", "input_address": switch, "observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [switch], "transitioned_solenoid_addresses": action["risen"], "result": "observed",
		})
	return observed


# ---------------------------------------------------------------- evidence


def raw_entry(harness: Path, name: str, run: dict[str, Any], game: str) -> dict[str, Any]:
	entry: dict[str, Any] = {
		"name": name,
		"sha256": sha256(harness / name / "run.json"),
		"scenario_path": scenario_for(name),
		"scenario_sha256": run["scenario"]["sha256"],
		"action_count": run["scenario"]["action_count"],
		"watch_switches": run["watch_switches"],
		"self_test_pulses": service_pulses(run),
		"boot_wait_s": 0,
		"snapshot_count": len(run["snapshots"]),
		"nvram_initialization": (
			f"Newly created state directory: the initialization run {name}/init.json (scenario cycln-nvram-init.json, SHA-256 "
			f"of its record {sha256(harness / name / 'init.json')}) booted {game} from empty NVRAM and wrote nvram/{game}.nv, which "
			"this run inherited and no other run shares."
		),
	}
	if run["initial_switches"]:
		entry["initial_switches"] = [{"switch": item["switch"], "state": item["state"]} for item in run["initial_switches"]]
	return entry


def boot_note(run: dict[str, Any]) -> str:
	holds = ", ".join(f"{item['switch']}={item['state']}" for item in run["initial_switches"])
	return f"Power-up probe with switches {holds} held from emulator start. Solenoid on-spans: {describe_spans(solenoid_spans(run), end_time(run))}."


def observation_for(name: str, run: dict[str, Any], cited: dict[str, tuple[str, str]], named: dict[str, int]) -> dict[str, Any]:
	spans = solenoid_spans(run)
	observation: dict[str, Any] = {"solenoid_addresses_seen": sorted(spans)}
	if name.startswith("coil-test"):
		steps = coil_test(run, cited)
		held = relay_spans(run, steps)
		for step in steps:
			# Key by the ROM's own coil name: the display folds 0/O and 5/S, which coil_test allows for. The ROM's 'p'
			# is its '/' glyph.
			rom_name = data.ROM_COIL_STEPS[step["step"]][1 if step["address"] > 24 else 0].replace("p", "/")
			named[f"coil-{step['step']:02d}-{slug(rom_name)}"] = step["address"]
		observation.update({
			"diagnostic_checkpoints": checkpoints(run),
			"ordered_solenoid_on_sequence": [step["address"] for step in steps],
			"note": (
				f"Advance walk to COIL TEST (player 3 display 05), then two identical cycles of {len(steps)} pulses. Step:address = "
				"player 1 and 2 displays [player 4 display]: "
				+ "; ".join(f"{s['step']:02d}:{s['address']} = {s['display']}" + (f" [{s['player_4']}]" if s["player_4"] else "") for s in steps)
				+ f". Steps 01-08 pulse the A-side address n with the A/C select relay (12) released and then, with 12 energized, "
				f"the C-side address n+24 ({', '.join(map(str, held))}); step 12 pulses 12 itself; steps 13 and 14 are skipped."
			),
			"limitation": "A pulsed address is ROM activity, not proof that a load is fitted: steps 02, 06, 08 and 22 pulse drives the ROM names NOT USED.",
		})
	elif name.startswith("single-lamps"):
		pairs = single_lamps(run, cited)
		for pair in pairs:
			named[f"lamp-{pair['designator']:02d}-{slug(data.ROM_LAMP_NAMES[pair['designator']])}"] = pair["address"]
		observation.update({
			"diagnostic_checkpoints": checkpoints(run),
			"note": (
				"Advance walk to SINGLE LAMPS (player 3 display 04); each Credit press (public 3) steps the designator, and designator "
				"n blinks public lamp n alone for every n from 1 to 64 while the player 3 display shows 04 n. Designator = player 1 "
				"and 2 displays: " + "; ".join(f"{p['designator']:02d} = {p['display']}" for p in pairs) + "."
			),
		})
	elif name.startswith("switch-levels"):
		results = switch_levels(run, cited)
		observation.update({
			"diagnostic_checkpoints": checkpoints(run),
			"note": (
				"Advance walk to SWITCH LEVELS (player 3 display 06); each public address 1-64 and 81-88 held at 1 alone for 1.5 s. "
				"Address = player 1 and 2 displays / player 3 display [active solenoids] while held: "
				+ "; ".join(f"{r['address']} = {r['name']} / {r['number']} {r['solenoids']}" for r in results) + "."
			),
			"limitation": (
				"Host-held levels written on every poll; a name shown while public n is held at 1 means the ROM reads that address as "
				"active at 1. A held write to 57 or 58 also overrides core_updateSw's copy from the flipper column on every poll."
			),
		})
	elif name.startswith("wheel-test"):
		observation.update({
			"diagnostic_checkpoints": checkpoints(run),
			"note": (
				"Advance walk to the Mystery Wheel Test (player 3 display 08). Snapshot readings, player 1 and 2 | player 3 | player 4: "
				+ wheel_test(name, run, cited) + f". Solenoid on-spans: {describe_spans(spans, end_time(run), skip={23})}."
			),
			"limitation": REACTIVE_LIMITATION if "reactive" in name else STATIC_LIMITATION,
		})
	elif name.startswith("boot-"):
		observation.update({"note": boot_note(run), "limitation": STATIC_LIMITATION})
	else:
		observation.update({
			"named_action_observations": gameplay_observations(run),
			"note": (
				f"Scripted gameplay scenario ({run['scenario']['action_count']} actions, see the scenario notes). Solenoids that rose in "
				"each switch action's window: "
				+ "; ".join(f"{a['label']} [{a['switch']}={a['state']}] -> {a['risen']}" for a in gameplay_actions(run))
				+ f". Solenoid on-spans: {describe_spans(spans, end_time(run))}."
			),
			"limitation": SCRIPTED_LIMITATION,
		})
	return observation


def evidence_record(game: str, manifest_bytes: bytes, raw_runs: list[dict[str, Any]], observations: dict[str, Any], named: dict[str, int], seen: set[int]) -> dict[str, Any]:
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "cyclone-harness-runs", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": data.PINMAME_REVISION,
			"path": SOURCE_PATH,
			"sha256": hashlib.sha256(manifest_bytes).hexdigest(),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external.",
			"quality": "observed",
			"manifest_algorithm": MANIFEST_ALGORITHM,
		},
		"driver_ids": [game],
		"machine_ids": [data.MACHINE_ID],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": game,
			"rom_archive_sha256": data.ROM_ARCHIVE_SHA256[game],
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": data.PINMAME_REVISION, "sha256": data.LIBRARY_SHA256},
			"raw_runs": raw_runs,
			"command_template": COMMAND_TEMPLATE,
			"observations": {
				"service_language": "English",
				"solenoid_addresses_seen": sorted(seen),
				"named_output_addresses": named,
				"runs": observations,
			},
		},
	}


def build(review_root: Path) -> tuple[bytes, dict[str, dict[str, Any]], dict[str, dict[str, list[str]]]]:
	harness = review_root / HARNESS_RELATIVE
	manifest_bytes = (json.dumps(manifests.build_manifest(harness, GAME), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
	evidence: dict[str, dict[str, Any]] = {}
	pins: dict[str, dict[str, list[str]]] = {}
	for game, names in RUNS.items():
		raw_runs, observations, named, seen = [], {}, {}, set()
		for name in names:
			run = load_run(harness, name, game)
			raw_runs.append(raw_entry(harness, name, run, game))
			cited: dict[str, tuple[str, str]] = {}
			observations[name] = observation_for(name, run, cited, named)
			seen.update(solenoid_spans(run))
			if cited:
				pins[name] = {label: [digest, reading] for label, (digest, reading) in sorted(cited.items())}
		evidence[game] = evidence_record(game, manifest_bytes, raw_runs, observations, named, seen)
	return manifest_bytes, evidence, pins


def check_pins(pins: dict[str, dict[str, list[str]]]) -> None:
	"""Refuse any cited frame or reading that differs from the curator's pinned seed."""
	seed = json.loads(FRAME_SEED_PATH.read_bytes())
	if seed.get("format") != "cyclone-display-frame-readings" or seed.get("version") != 1:
		raise RuntimeError(f"{FRAME_SEED_PATH} is not a Cyclone frame-reading seed")
	pinned = seed["runs"]
	if sorted(pinned) != sorted(pins):
		raise RuntimeError(f"the runs citing frames differ from the pinned seed: {sorted(set(pinned) ^ set(pins))}")
	for name, labels in pins.items():
		if sorted(pinned[name]) != sorted(labels):
			raise RuntimeError(f"{name}: the cited frame labels differ from the pinned seed: {sorted(set(pinned[name]) ^ set(labels))[:5]}")
		changed = [label for label in labels if pinned[name][label] != labels[label]]
		if changed:
			raise RuntimeError(f"{name}: frames or readings differ from the pinned seed at {changed[:5]}")


def seed_bytes(pins: dict[str, dict[str, list[str]]]) -> bytes:
	return canonical_bytes({
		"format": "cyclone-display-frame-readings",
		"version": 1,
		"machine_id": data.MACHINE_ID,
		"frame_digest": "SHA-256 of the compact JSON [[player 1 segments], [player 2], [player 3], [player 4]] of the raw values",
		"reading": "player 1 and 2 decoded and joined with a space | player 3 | player 4, read by the curator from the cited frame",
		"runs": pins,
	})


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--pin-frames", action="store_true")
	args = parser.parse_args()
	review_root = working_root()
	harness = review_root / HARNESS_RELATIVE
	manifest_bytes, evidence, pins = build(review_root)
	if args.pin_frames:
		FRAME_SEED_PATH.write_bytes(seed_bytes(pins))
		print(f"wrote {FRAME_SEED_PATH}; review every reading against its frame before committing it")
		return
	check_pins(pins)
	if args.check:
		if (harness / "manifest.json").read_bytes() != manifest_bytes:
			raise SystemExit(f"{harness / 'manifest.json'} does not match the files beside it")
		manifests.check_manifest(harness, GAME)
		for game, path in EVIDENCE_PATHS.items():
			if path.read_bytes() != canonical_bytes(evidence[game]):
				raise SystemExit(f"{path} is not the summary of the raw runs in {harness}")
		print("Cyclone runtime evidence, frame pins and manifest match the raw runs.")
		return
	manifests.write_manifest(harness, GAME)
	for game, path in EVIDENCE_PATHS.items():
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(canonical_bytes(evidence[game]))
		print(f"wrote {path}")


if __name__ == "__main__":
	main()
