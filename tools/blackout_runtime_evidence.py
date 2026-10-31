"""Derive Blackout's compact runtime evidence from its retained raw harness runs.

The four raw runs (``init``, ``sol``, ``sw`` and ``play``) stay outside Git under the review-artifacts
root. This module rebuilds ``evidence/runtime/system-6/blackout-1980.json`` from them and refuses a
run from another game, build or scenario, a step or snapshot that does not line up with its scenario,
and any cited display frame that differs from the reading pinned in
``tools/seeds/williams/blackout-1980-display-readings.json``. Every pinned frame must be cited exactly
once, so a substituted, blank or missing frame fails instead of silently changing a reading.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_external_evidence_manifest import check_manifest  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes, content_sha256, load_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GAME = "blkou_l1"
MACHINE_ID = "williams.blackout.1980"
BASE = "2506047a1f986894b6b9fe8982fbe8ef8676b473"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_SHA = "88d335971251be6aa26901e51bc47bae6febaaaf0917ed1b8aac4a2fdd306dc1"
INIT_NVRAM_SHA = "f99409fbe04cff06460649a5b9a5befe6824aa9423f9d6578fa19410a012c9f1"
HARNESS = Path("blackout-1980/harness")
OUTPUT = Path("evidence/runtime/system-6/blackout-1980.json")
READINGS = Path("tools/seeds/williams/blackout-1980-display-readings.json")
SCENARIOS = {
	"init": "tools/harness-scenarios/system-6/blackout-nvram-init-boot.json",
	"sol": "tools/harness-scenarios/system-6/blackout-solenoid-test.json",
	"sw": "tools/harness-scenarios/system-6/blackout-switch-test.json",
	"play": "tools/harness-scenarios/system-6/blackout-gameplay.json",
}
# Seven-segment code (low seven bits) to character; bit 0x80 is the comma.
DECODER = {0: " ", 63: "0", 6: "1", 91: "2", 79: "3", 102: "4", 109: "5", 125: "6", 124: "6", 7: "7", 127: "8", 111: "9", 103: "9"}
PLAYER_1 = 0
CREDITS = 4
BALL_IN_PLAY = 5
# Sound-board command lines: excluded from the gameplay solenoid orders below.
SOUND_LINES = {9, 10, 11, 12, 13}
SPECIALS = {22: 17, 21: 18, 23: 19, 44: 20, 43: 21}

RunLoader = Callable[[str], dict[str, Any]]


def sha(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(segments: list[int]) -> str:
	text = ""
	for value in segments:
		if value & 0x7F not in DECODER:
			raise ValueError(f"undecodable segment value {value}")
		text += DECODER[value & 0x7F] + ("," if value & 0x80 else "")
	return text


def raw_loader(review_root: Path) -> RunLoader:
	return lambda name: load_json(review_root / HARNESS / f"{name}.json")


class Frames:
	"""Pinned display readings; each must be cited once and match its raw frame exactly."""

	def __init__(self, root: Path, runs: dict[str, dict[str, Any]]) -> None:
		seed = load_json(root / READINGS)
		if seed.get("format") != "pinmame-segment-readings" or seed.get("game") != GAME:
			raise RuntimeError("display-readings seed is not Blackout's")
		self.pinned = {(f["run"], f["snapshot"], f["display_index"]): f for f in seed["frames"]}
		if len(self.pinned) != len(seed["frames"]):
			raise RuntimeError("display-readings seed pins one frame twice")
		self.runs = runs
		self.cited: set[tuple[str, int, int]] = set()

	def response(self, run: str, snapshot: int, display_index: int, address: int | None = None) -> dict[str, Any]:
		key = (run, snapshot, display_index)
		pin = self.pinned.get(key)
		if pin is None:
			raise RuntimeError(f"cited frame is not pinned: {key}")
		if key in self.cited:
			raise RuntimeError(f"pinned frame cited twice: {key}")
		self.cited.add(key)
		snap = self.runs[run]["snapshots"][snapshot]
		if snap["label"] != pin["label"]:
			raise RuntimeError(f"pinned frame label differs: {key}")
		display = next((d for d in snap["displays"] if d["index"] == display_index), None)
		if display is None or display.get("segments") != pin["segments"] or content_sha256(display) != pin["display_sha256"]:
			raise RuntimeError(f"raw frame differs from the pinned reading: {key}")
		if decode(pin["segments"]) != pin["reading"]:
			raise RuntimeError(f"pinned reading does not decode from its segments: {key}")
		out = {"snapshot_label": snap["label"], "display_index": display_index, "segments": pin["segments"],
			"decoded_segment_positions": list(range(len(pin["segments"]))), "interpreted_text": pin["reading"]}
		if address is not None:
			out["diagnostic_address"] = address
		return out

	def finish(self) -> None:
		if self.cited != set(self.pinned):
			raise RuntimeError(f"pinned frames not cited: {sorted(set(self.pinned) - self.cited)}")


def check_run(name: str, run: dict[str, Any], root: Path) -> None:
	if run.get("failure") is not None or run.get("game") != GAME or run.get("library_sha256") != LIBRARY_SHA:
		raise RuntimeError(f"raw run {name} failed or comes from another game or build")
	if run.get("handle_mechanics") != 0 or run.get("pulses") != []:
		raise RuntimeError(f"raw run {name} used mechanics handling or self-test pulses")
	scenario = root / SCENARIOS[name]
	if run["scenario"]["sha256"] != sha(scenario):
		raise RuntimeError(f"raw run {name} used another scenario")
	actions = load_json(scenario)["actions"]
	if len(run["steps"]) != len(actions) or run["scenario"]["action_count"] != len(actions):
		raise RuntimeError(f"raw run {name} does not cover its scenario")
	for step, action in zip(run["steps"], actions):
		if step["label"] != action["label"] or step["type"] != action["type"] or step.get("switch") != action.get("switch"):
			raise RuntimeError(f"raw run {name} step differs from its scenario action: {action['label']}")


def watched(snapshot: dict[str, Any]) -> dict[int, int]:
	return {w["number"]: w["state"] for w in snapshot["watched_switches"]}


def step_solenoids(step: dict[str, Any]) -> list[int]:
	return sorted({t["number"] for t in step["transitions"]["solenoids"]})


def init_observations(frames: Frames, run: dict[str, Any]) -> dict[str, Any]:
	snap = run["snapshots"]
	if len(snap) != 2 or snap[1]["label"] != run["steps"][0]["label"]:
		raise RuntimeError("init run snapshots do not line up")
	p1 = frames.response("init", 1, PLAYER_1)
	credit = frames.response("init", 1, CREDITS)
	bip = frames.response("init", 1, BALL_IN_PLAY)
	if (credit["interpreted_text"], bip["interpreted_text"], p1["interpreted_text"]) != ("04", "00", "1495 1"):
		raise RuntimeError("init run is not on the game-identification screen")
	return {
		"named_action_observations": [{
			"label": f"power-up from empty CMOS: credits {credit['interpreted_text']}, ball in play {bip['interpreted_text']}, player 1 '{p1['interpreted_text']}'",
			"input_kind": "key", "input_name": "power-up with no host input", "observed_switch_addresses": [],
			"display_responses": [p1, credit, bip], "active_solenoid_addresses": sorted(snap[1]["active_solenoids"]),
			"transitioned_solenoid_addresses": [], "result": "observed"}],
		"note": ("The drawing set's Power Turn-On page describes the diagnostic mode as credits 04, ball in play 00 and the game identification in the player 1 display, "
			"and Table 1 prints Function 00 as 1495 1; one power-up from empty CMOS stops there. This run writes the NVRAM every later run starts from."),
	}


def solenoid_test_observations(frames: Frames, run: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
	steps, snaps = run["steps"], run["snapshots"]
	if len(snaps) != len(steps) + 1 or any(s["label"] != t["label"] for s, t in zip(snaps[1:], steps)):
		raise RuntimeError("solenoid-test snapshots do not pair one-to-one with steps")
	lamp_entry = next(i for i, t in enumerate(steps) if t["label"] == "Advance: Test 01 lamp test")
	lamp_credit = frames.response("sol", lamp_entry + 1, CREDITS)
	if lamp_credit["interpreted_text"] != "01":
		raise RuntimeError("Test 01 is not shown in the credits display")
	entry = next(i for i, t in enumerate(steps) if t["label"] == "Advance: Test 02, solenoid 01")
	credit = frames.response("sol", entry + 1, CREDITS)
	bip = frames.response("sol", entry + 1, BALL_IN_PLAY, 1)
	if credit["interpreted_text"] != "02" or bip["interpreted_text"] != "01" or step_solenoids(steps[entry]) != [1, 23]:
		raise RuntimeError("Test 02 entry does not show 02 / 01 with solenoid 1 and game-on 23")
	mapping = {"1": 1}
	actions = [
		{"label": "Advance into Test 01: credits 01, every lamp address flashes", "input_kind": "switch", "input_address": -7,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7], "display_responses": [lamp_credit],
			"active_solenoid_addresses": sorted(snaps[lamp_entry + 1]["active_solenoids"]), "transitioned_solenoid_addresses": [], "result": "observed"},
		{"label": "Advance into Test 02: credits 02, ball in play 01, solenoid 1 pulses and game-on 23 energizes", "input_kind": "switch", "input_address": -7,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7], "display_responses": [credit, bip],
			"active_solenoid_addresses": sorted(snaps[entry + 1]["active_solenoids"]), "transitioned_solenoid_addresses": [1, 23], "result": "observed"},
	]
	shown = 1
	wrapped = False
	for index in range(entry + 1, len(steps)):
		step = steps[index]
		if step["label"] != "Advance: next solenoid":
			raise RuntimeError(f"unexpected solenoid-test step: {step['label']}")
		number = shown + 1 if shown < 22 else 1
		previous = shown
		response = frames.response("sol", index + 1, BALL_IN_PLAY, number)
		transitions = {t["number"]: t["states"] for t in step["transitions"]["solenoids"]}
		extra = set(transitions) - {number}
		if response["interpreted_text"] != f"{number:02d}" or number not in transitions:
			raise RuntimeError(f"Test 02 step {number} is not shown and pulsed")
		# The previous step's repeated pulse may finish inside this window; nothing else may move.
		if extra - {previous} or (previous in extra and transitions[previous][-1] != 0):
			raise RuntimeError(f"Test 02 step {number} moves another solenoid: {sorted(extra)}")
		if number == 1:
			wrapped = True
		elif not wrapped:
			mapping[str(number)] = number
		actions.append({"label": f"Advance: Test 02 step {number:02d}, public solenoid {number} transitions {transitions[number]}", "input_kind": "switch",
			"input_address": -7, "observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7], "display_responses": [response],
			"active_solenoid_addresses": sorted(snaps[index + 1]["active_solenoids"]), "transitioned_solenoid_addresses": sorted(transitions), "result": "observed"})
		shown = number
	if sorted(mapping, key=int) != [str(n) for n in range(1, 23)] or not wrapped:
		raise RuntimeError("Test 02 did not step through 01-22 and wrap to 01")
	lamps = sorted({e["number"] for e in run["events"] if e["event"] == "lamp"})
	sequence = [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1]
	sixteen = next(t["states"] for t in steps[entry + 15]["transitions"]["solenoids"] if t["number"] == 16)
	if sixteen != [0, 1, 0]:
		raise RuntimeError("Test 02 step 16 no longer pulses the coin lockout from its energized rest")
	return {
		"named_action_observations": actions,
		"ordered_solenoid_on_sequence": sequence,
		"solenoid_addresses_seen": sorted(set(sequence)),
		"note": (f"Test 01 drove {len(lamps)} lamp addresses, {lamps[0]}-{lamps[-1]}, including 11, which the lamp matrix prints NOT USED. "
			"Entering Test 02 energizes game-on 23 and pulses solenoid 1; each further Advance in Manual-Down shows the next step number in the ball-in-play display and pulses that public solenoid, "
			"whose repeated pulse may finish in the next window. Step 16 pulses the coin lockout off from its energized game-over rest and leaves it off. "
			"Step 22 is pulsed although Table 3 prints it Not Used and the solenoid sheet draws its driver output N/C, and so are 02, 03, 07 and 08. After 22 the test wraps to 01; game-on 23 is not a test step."),
	}, mapping


def switch_test_observations(frames: Frames, run: dict[str, Any]) -> dict[str, Any]:
	snaps, steps = run["snapshots"], run["steps"]
	by_label: dict[str, int] = {}
	for index, snap in enumerate(snaps):
		by_label[snap["label"]] = -1 if snap["label"] in by_label else index

	def find(label: str) -> int:
		index = by_label.get(label, -1)
		if index < 0:
			raise RuntimeError(f"switch-test snapshot missing or repeated: {label}")
		return index

	entry = find("Advance: Test 03 switch test, 03 in the credit display, nothing reported at rest")
	credit = frames.response("sw", entry, CREDITS)
	bip = frames.response("sw", entry, BALL_IN_PLAY)
	if credit["interpreted_text"] != "03" or bip["interpreted_text"].strip():
		raise RuntimeError("Test 03 entry is not 03 with a blank ball-in-play display")
	actions = [{"label": "Advance into Test 03: credits 03, ball in play blank", "input_kind": "switch", "input_address": -7,
		"observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7], "display_responses": [credit, bip],
		"active_solenoid_addresses": sorted(snaps[entry]["active_solenoids"]), "transitioned_solenoid_addresses": [], "result": "observed"}]
	for number in range(1, 65):
		index = find(f"close public switch {number} and read the ball-in-play display (held)")
		if watched(snaps[index]).get(number) != 1:
			raise RuntimeError(f"switch {number} was not held in its snapshot")
		response = frames.response("sw", index, BALL_IN_PLAY, number if number <= 46 else None)
		text = response["interpreted_text"]
		if number <= 46 and text != f"{number:02d}":
			raise RuntimeError(f"Test 03 does not name held switch {number}")
		if number > 46 and text != "46":
			raise RuntimeError(f"Test 03 changes its reading for unfitted switch {number}")
		active = sorted(snaps[index]["active_solenoids"])
		fired = sorted(set(active) & set(SPECIALS.values()))
		if fired != ([SPECIALS[number]] if number in SPECIALS else []):
			raise RuntimeError(f"held switch {number} drives special solenoids {fired}")
		actions.append({"label": f"hold public switch {number}: ball in play '{text}'" + (" (unchanged from 46)" if number > 46 else "")
			+ (f"; special solenoid {fired[0]} held on" if fired else ""), "input_kind": "switch", "input_address": number,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [number], "display_responses": [response],
			"active_solenoid_addresses": active, "transitioned_solenoid_addresses": [], "result": "observed" if number <= 46 else "no_matching_transition"})
	for label, number, expected, state in [
		("one-shot control: write public 45 once and read the ball-in-play display", 45, "45", 1),
		("one-shot: write lane-change matrix 46 once and read the ball-in-play display", 46, "46", 0),
		("one-shot control again: write public 45 once so the next reading starts from 45", 45, "45", 1),
	]:
		index = find(label)
		response = frames.response("sw", index, BALL_IN_PLAY, number)
		if response["interpreted_text"] != expected or watched(snaps[index]).get(number) != state:
			raise RuntimeError(f"one-shot write to {number} did not behave as recorded")
		actions.append({"label": f"one-shot write of public {number}: watched state {state}, ball in play '{expected}'"
			+ ("; PinMAME's flipper-button copy had already rewritten 46 to the button's 0, but Test 03 latched the closure" if number == 46 else ""),
			"input_kind": "switch", "input_address": number, "observed_switch_addresses": [], "host_stimulus_switch_addresses": [number],
			"display_responses": [response], "active_solenoid_addresses": sorted(snaps[index]["active_solenoids"]), "transitioned_solenoid_addresses": [], "result": "observed"})
	for button, side, pair, expected, copy in ((84, "left", [47, 48], "45", None), (82, "right", [45, 46], "46", 46)):
		index = find(f"hold synthetic {side} flipper button {button} and read the ball-in-play display (held)")
		levels = watched(snaps[index])
		response = frames.response("sw", index, BALL_IN_PLAY, copy)
		held = sorted(set(snaps[index]["active_solenoids"]) & {45, 46, 47, 48})
		step = next(s for s in steps if s.get("switch") == button)
		copied = levels.get(46) == 1
		if levels.get(button) != 1 or copied != (copy is not None) or response["interpreted_text"] != expected or held != pair or step_solenoids(step) != pair:
			raise RuntimeError(f"button {button} did not behave as recorded")
		actions.append({"label": (f"hold {side} flipper button {button}: matrix 46 reads {1 if copied else 0}, ball in play '{expected}', outputs {pair}"
			+ ("" if copied else "; no matrix switch receives the left button")),
			"input_kind": "switch", "input_address": button, "observed_switch_addresses": [46] if copied else [], "host_stimulus_switch_addresses": [button],
			"display_responses": [response], "active_solenoid_addresses": sorted(snaps[index]["active_solenoids"]),
			"transitioned_solenoid_addresses": pair, "held_synthetic_solenoid_addresses": held, "result": "observed"})
	return {
		"named_action_observations": actions,
		"note": ("Held closures of public 1-46 each show their own number in the ball-in-play display, including 16, 17 and 24, which the switch matrix prints NOT USED; "
			"holding 47-64 leaves the last reading, 46, unchanged. "
			"Holding 22, 21, 23, 44 and 43 also holds special solenoids 17, 18, 19, 20 and 21 on, and no other held switch drives a special. "
			"A one-shot write to 46 reads back 0 at once because PinMAME rewrites 46 from the right flipper button on every update, although Test 03 latched it; "
			"holding 82 reports 46 and fabricates 45/46, holding 84 fabricates 47/48 and reaches no matrix switch."),
		"limitation": "The booklet does not say how long Test 03 holds a reading; readings are taken from held snapshots. A reading shows that the ROM scans an address, not that a contact is fitted there (16, 17 and 24 are reported although no contact is drawn); an unchanged reading for 47-64 agrees with the matrix's NOT USED cells but is not itself proof that no contact is fitted.",
	}


# Non-sound solenoid turn-on order in each named gameplay input's window, and the off events where no solenoid turns on.
GAMEPLAY_ORDER = {
	"coin on the right coin switch": ([14], [14]),
	"credit button: start a one-player game": ([23, 4, 5, 1], [4, 5]),
	"outhole empties; the served ball is plunged": ([], [1]),
	"left jet bumper scoring switch": ([17], [17]),
	"right jet bumper scoring switch": ([18], [18]),
	"bottom jet bumper scoring switch": ([19], [19]),
	"left kicker scoring switch": ([20], [20]),
	"right kicker scoring switch": ([21], [21]),
	"1 rollover": ([], []),
	"right flipper button (synthetic 82): lane change": ([45, 46], [45, 46]),
	"left flipper button (synthetic 84)": ([47, 48], [47, 48]),
	"right flipper button (synthetic 82) again: lane change": ([45, 46], [45, 46]),
	"green target #1 (bottom)": ([], []),
	"green target #2": ([], []),
	"green target #3": ([], []),
	"green target #4": ([], []),
	"green target #5 (top)": ([], []),
	"centre 3-bank: left target down": ([], []),
	"centre 3-bank: centre target down": ([], []),
	"centre 3-bank: right target down, series switch still open": ([], []),
	"centre 3-bank series switch closes": ([4], [4]),
	"centre 3-bank: left target raised": ([], []),
	"centre 3-bank: centre target raised": ([], []),
	"centre 3-bank: right target raised": ([], []),
	"centre 3-bank: series switch opens": ([], []),
	"top 3-bank: left target down": ([], []),
	"top 3-bank: centre target down": ([], []),
	"top 3-bank: right target down, series switch still open": ([], []),
	"top 3-bank series switch closes": ([5], [5]),
	"top 3-bank: left target raised": ([], []),
	"top 3-bank: centre target raised": ([], []),
	"top 3-bank: right target raised": ([], []),
	"top 3-bank: series switch opens": ([], []),
	"ball enters the eject hole": ([15, 15, 15, 15, 15, 15, 15, 16, 6], [16, 15, 15, 15, 15, 15, 15, 15]),
	"eject hole empties": ([], [6]),
	"ball drains into the outhole": ([4, 5, 1], [4, 5]),
	"outhole empties; the second ball is plunged": ([], [1]),
	"ball roll tilt, first closure": ([], [23]),
}
# Lamps whose state differs between the start and the end of a window: (lit, extinguished) among LAMP_WATCH.
# The coin and credit windows start in attract mode, whose lamp cycle changes the playfield lamps at random
# points; there only the playfield credits lamp 56, which the booklet keeps out of that cycle, is compared.
LAMP_WATCH = {28, 29, 30, 43, 44, 45, 46, 61}
ATTRACT_WINDOWS = {"coin on the right coin switch", "credit button: start a one-player game"}
LAMP_CHANGES = {
	"coin on the right coin switch": ([56], []),
	"credit button: start a one-player game": ([], [56]),
	"1 rollover": ([28], []),
	"right flipper button (synthetic 82): lane change": ([29], [28]),
	"left flipper button (synthetic 84)": ([], []),
	"right flipper button (synthetic 82) again: lane change": ([30], [29]),
	"green target #5 (top)": ([43], []),
	"centre 3-bank series switch closes": ([45], []),
	"top 3-bank series switch closes": ([44, 46], []),
	"ball enters the eject hole": ([], [43, 44, 45, 46]),
	"ball roll tilt, first closure": ([61], []),
}


def gameplay_observations(run: dict[str, Any]) -> dict[str, Any]:
	steps, events, snaps = run["steps"], run["events"], run["snapshots"]
	labels = [s["label"] for s in snaps]
	if len(set(labels)) != len(labels):
		raise RuntimeError("gameplay snapshot labels repeat")
	groups: list[list[dict[str, Any]]] = []
	for step in steps:
		if "switch" in step:
			groups.append([step])
		elif groups:
			groups[-1].append(step)
	# A wait that ends on an output shares its timestamp with the next host write, so windows are cut by
	# event-list position (first host write of each group) rather than by time.
	starts = []
	for group in groups:
		positions = [i for i, e in enumerate(events) if e["event"] == "switch" and e.get("step") == group[0]["step"]]
		if not positions:
			raise RuntimeError(f"no host input recorded for step {group[0]['step']}")
		starts.append(min(positions))
	if starts != sorted(starts):
		raise RuntimeError("gameplay host inputs are out of order")
	lamp_state: dict[int, int] = {}
	position = 0

	def lamps_until(stop: int) -> dict[int, int]:
		nonlocal position
		while position < stop:
			event = events[position]
			if event["event"] == "lamp":
				lamp_state[event["number"]] = event["state"]
			position += 1
		return dict(lamp_state)

	actions, facts = [], {}
	for index, group in enumerate(groups):
		start = starts[index]
		end = starts[index + 1] if index + 1 < len(groups) else len(events)
		window = events[start:end]
		before = lamps_until(start)
		after = lamps_until(end)
		on = [e for e in window if e["event"] == "solenoid" and e["state"] == 1 and e["number"] not in SOUND_LINES]
		off = [e for e in window if e["event"] == "solenoid" and e["state"] == 0 and e["number"] not in SOUND_LINES]
		order, released = [e["number"] for e in on], [e["number"] for e in off]
		name, switch = group[0]["label"], group[0]["switch"]
		watch = {56} if name in ATTRACT_WINDOWS else LAMP_WATCH
		lit = sorted(n for n in watch if after.get(n, 0) == 1 and before.get(n, 0) == 0)
		out = sorted(n for n in watch if after.get(n, 0) == 0 and before.get(n, 0) == 1)
		if name not in GAMEPLAY_ORDER:
			raise RuntimeError(f"unexpected gameplay input: {name}")
		if (order, released) != GAMEPLAY_ORDER[name]:
			raise RuntimeError(f"gameplay solenoids changed after '{name}': on {order}, off {released}")
		if (lit, out) != LAMP_CHANGES.get(name, ([], [])):
			raise RuntimeError(f"gameplay lamps changed after '{name}': lit {lit}, extinguished {out}")
		held = f"{name} (held)"
		snapshot = snaps[labels.index(held)] if held in labels else snaps[labels.index(group[-1]["label"])]
		copied = [46] if switch == 82 and watched(snapshot).get(46) == 1 else []
		if switch in (82, 84) and copied != ([46] if switch == 82 else []):
			raise RuntimeError(f"button {switch} copy into 46 changed")
		text = f"{name}: solenoids on in order {order}" if order else f"{name}: no solenoid turns on in the window"
		if released and not order:
			text += f"; off {released}"
		if lit or out:
			text += f"; lamps lit {lit}, extinguished {out}"
		action = {"label": text, "input_kind": "switch", "input_address": switch, "observed_switch_addresses": copied,
			"host_stimulus_switch_addresses": sorted({s["switch"] for s in group if "switch" in s}),
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"transitioned_solenoid_addresses": sorted({n for s in group for n in step_solenoids(s)}),
			"result": "observed" if order or released or lit or out else "no_matching_transition"}
		if switch in (82, 84):
			action["held_synthetic_solenoid_addresses"] = sorted(set(snapshot["active_solenoids"]) & {45, 46, 47, 48})
		actions.append(action)
		facts[name] = {"start": events[start]["time_s"], "position": start, "on": on, "off": off, "window": window}
	if set(GAMEPLAY_ORDER) - set(facts):
		raise RuntimeError(f"gameplay inputs missing: {sorted(set(GAMEPLAY_ORDER) - set(facts))}")

	def delay(name: str, number: int, nth: int = 0) -> float:
		return [e["time_s"] for e in facts[name]["on"] if e["number"] == number][nth] - facts[name]["start"]

	start_game = facts["credit button: start a one-player game"]
	specials = {switch: delay(name, solenoid) for switch, solenoid, name in [
		(22, 17, "left jet bumper scoring switch"), (21, 18, "right jet bumper scoring switch"), (23, 19, "bottom jet bumper scoring switch"),
		(44, 20, "left kicker scoring switch"), (43, 21, "right kicker scoring switch")]}
	if max(specials.values()) > 0.02:
		raise RuntimeError(f"a special fired late: {specials}")
	eject = facts["ball enters the eject hole"]
	relay = [e for e in eject["window"] if e["event"] == "solenoid" and e["number"] == 15]
	pulses = [(a["time_s"], b["time_s"]) for a, b in zip(relay[0::2], relay[1::2])]
	if [a["state"] for a in relay] != [1, 0] * len(pulses) or len(pulses) != 7:
		raise RuntimeError("the eject-hole special relay sequence changed")
	longest = max(pulses, key=lambda p: p[1] - p[0])
	running = {e["number"]: e["state"] for e in events[:eject["position"]] if e["event"] == "lamp"}
	lamp_counts = []
	dark = None
	for event in eject["window"]:
		if event["event"] == "lamp":
			running[event["number"]] = event["state"]
			lamp_counts.append(sum(running.values()))
			if dark is None and sum(running.values()) == 0:
				dark = event["time_s"]
	sweep = [e["number"] for e in eject["window"] if e["event"] == "lamp" and e["state"] == 1 and longest[0] <= e["time_s"] <= longest[1]]
	if dark is None or sweep[:64] != list(range(1, 65)) or max(lamp_counts) != 64:
		raise RuntimeError("the eject-hole lamp sequence changed")
	lockout = [e for e in eject["window"] if e["event"] == "solenoid" and e["number"] == 16]
	tilt = facts["ball roll tilt, first closure"]
	return {
		"named_action_observations": actions,
		"ordered_solenoid_on_sequence": [e["number"] for e in events if e["event"] == "solenoid" and e["state"] == 1],
		"solenoid_addresses_seen": sorted({e["number"] for e in events if e["event"] == "solenoid"}),
		"note": (
			"Sound lines 9-13 are left out of every order. The coin on switch 4 fires the credit knocker 14 and lights the playfield credits lamp 56. "
			f"The credit button energizes game-on 23 {delay('credit button: start a one-player game', 23):.2f} s later, fires the centre and top 3-bank resets 4 and 5 at "
			f"{delay('credit button: start a one-player game', 4):.2f} s and {delay('credit button: start a one-player game', 5):.2f} s, and the outhole ball release 1 at "
			f"{delay('credit button: start a one-player game', 1):.2f} s. Switches 22, 21, 23, 44 and 43 fire 17, 18, 19, 20 and 21 within "
			f"{max(specials.values()) * 1000:.0f} ms. The 1 rollover lit lamp 28 (\"1\"); the right button moved it to 29 and then 30, and the left button changed nothing. "
			"The fifth green target lit eject-hole lamp 43; neither 3-bank fired its reset while its three targets were down and its series switch open, and each "
			f"reset ({delay('centre 3-bank series switch closes', 4):.3f} s and {delay('top 3-bank series switch closes', 5):.3f} s) followed its series switch 28 or 36 at once, "
			"lighting 45 (centre) and 44 and 46 (top). "
			f"With 43-46 lit, a ball in the eject hole pulsed the special relay 15 seven times, the fourth time holding it {longest[1] - longest[0]:.2f} s; "
			f"every lamp address went out {dark - eject['start']:.2f} s after the entry, and during the long hold lamps 1-64 lit one by one. "
			f"Coin lockout 16 dropped at {lockout[0]['time_s'] - eject['start']:.2f} s and re-energized at {lockout[1]['time_s'] - eject['start']:.2f} s, and the eject kicker 6 "
			f"fired {delay('ball enters the eject hole', 6):.2f} s after the entry; 43-46 were then out. "
			f"A drain on 9 fired 4 and 5 again and the ball release 1 {delay('ball drains into the outhole', 1):.2f} s later, and the ball roll tilt 2 dropped game-on 23 "
			f"{tilt['off'][0]['time_s'] - tilt['start']:.2f} s after the closure and lit TILT 61."),
		"limitation": ("The host writes every ball-presence and drop-target switch itself (outhole, eject hole, bank targets and series switches); those writes are stimulus, not ROM evidence, "
			"and a wait that ends on an output censors how long that output would have stayed on. The run entered the eject hole only with BLACKOUT 46 lit, so whether the relay sequence "
			"also runs without it is not observed. Lamp numbers are public addresses only."),
	}


def build(review_root: Path, root: Path = ROOT, loader: RunLoader | None = None) -> dict[str, Any]:
	"""Build the evidence document; ``loader`` may substitute raw runs (tests use it to mutate a frame)."""
	runs = {name: (loader or raw_loader(review_root))(name) for name in SCENARIOS}
	for name, run in runs.items():
		check_run(name, run, root)
	frames = Frames(root, runs)
	init = init_observations(frames, runs["init"])
	sol, mapping = solenoid_test_observations(frames, runs["sol"])
	sw = switch_test_observations(frames, runs["sw"])
	play = gameplay_observations(runs["play"])
	frames.finish()
	lamps = sorted({e["number"] for e in runs["sol"]["events"] if e["event"] == "lamp"})
	manifest = check_manifest(review_root / HARNESS, GAME)
	raw_runs = []
	for name, run in runs.items():
		scenario = load_json(root / SCENARIOS[name])
		raw_runs.append({
			"name": name, "sha256": sha(review_root / HARNESS / f"{name}.json"),
			"scenario_path": SCENARIOS[name], "scenario_sha256": run["scenario"]["sha256"], "action_count": len(scenario["actions"]),
			"watch_switches": run["watch_switches"], "self_test_pulses": 0, "boot_wait_s": 2.0, "snapshot_count": len(run["snapshots"]),
			"nvram_initialization": ("Empty CMOS: a new state directory and one 20 s power-up." if name == "init" else
				f"A new state directory seeded only with init-state/nvram/{GAME}.nv, SHA-256 {INIT_NVRAM_SHA}, and the init run's cfg files."),
		})
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/blackout_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [{"line_start": 1, "line_end": 1, "status": "candidate", "text": (
			"blkou_l1 Test 02 steps 01-22 pulse public solenoids 1-22 one at a time and wrap to 01; Test 03 names held switches 1-46 and leaves 46 shown for 47-64; "
			"button 82 is copied into 46 and fabricates 45/46, button 84 fabricates 47/48 only. Gameplay shows the knocker, the start sequence, the five switch-fired specials, "
			"both 3-bank resets from their series switches, the eject-hole Blackout sequence on the special relay 15, the outhole release and the ball roll tilt. "
			"No run establishes bulb quantity, physical location or mechanical timing.")}],
		"runtime": {
			"command_template": "python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-46e1a01a/Release/pinmame64.dll --game blkou_l1 --rom-path <authorized-rom-root> --work-dir <working-root>/review-artifacts/blackout-1980/harness/<name>-state --scenario <scenario_path> --output <working-root>/review-artifacts/blackout-1980/harness/<name>.json",
			"emulator": {"binary": "builds/pinmame-46e1a01a/Release/pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA},
			"game": GAME,
			"observations": {
				"lamp_addresses_seen": lamps,
				"physical_service_solenoid_to_public": mapping,
				"service_language": "numeric seven-segment diagnostics",
				"runs": {"init": init, "sol": sol, "sw": sw, "play": play},
			},
			"raw_runs": raw_runs,
			"rom_archive_sha256": ROM_SHA,
		},
		"source": {
			"attribution": "pinmame-game-defs curator",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": "tools/build_external_evidence_manifest.py: all relative POSIX paths, byte sizes and SHA256 sorted case-sensitively; exclude only manifest.json and manifest.sha256; canonical sorted-key compact UTF-8 JSON plus LF; SHA256 of those manifest bytes",
			"path": "external:pinmame-review-artifacts/blackout-1980/harness/manifest.json",
			"quality": "observed",
			"repository": "pinmame-game-defs",
			"revision": BASE,
			"sha256": manifest,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def check(review_root: Path, root: Path = ROOT) -> None:
	"""Refuse a committed evidence file that differs from the one the raw runs produce."""
	if (root / OUTPUT).read_bytes() != canonical_bytes(build(review_root, root)):
		raise RuntimeError(f"{OUTPUT.as_posix()} differs from the evidence its raw runs produce")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	parser.add_argument("--review-root", type=Path, default=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"))
	args = parser.parse_args()
	if args.review_root is None:
		parser.error("--review-root or PINMAME_REVIEW_ARTIFACTS_ROOT is required")
	if args.write:
		(ROOT / OUTPUT).parent.mkdir(parents=True, exist_ok=True)
		(ROOT / OUTPUT).write_bytes(canonical_bytes(build(Path(args.review_root))))
	else:
		check(Path(args.review_root))
	print(f"{OUTPUT.as_posix()}: {'written' if args.write else 'verified'}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
