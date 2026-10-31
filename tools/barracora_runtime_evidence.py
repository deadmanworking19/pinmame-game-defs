"""Derive Barracora's compact runtime evidence from its retained raw harness runs.

The four raw runs (``init``, ``sol``, ``sw`` and ``play``) stay outside Git under the review-artifacts
root. This module rebuilds ``evidence/runtime/system-7/barracora-1981.json`` from them and refuses a
run from another game, build or scenario, a step or snapshot that does not line up with its scenario,
and any cited display frame that differs from the reading pinned in
``tools/seeds/williams/barracora-1981-display-readings.json``. Every pinned frame must be cited exactly
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
GAME = "barra_l1"
MACHINE_ID = "williams.barracora.1981"
BASE = "40fe189b4cfd47786350e667303aa3789b095563"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_SHA = "3f9e8a3b4cce3112a1293c26746552a91e0c8e9c35b7d0027b982e0b9115f88d"
INIT_NVRAM_SHA = "9bdd907251c4ef7b765bbf9f02fddeb38fd21ba9ee7bd03e7d76ed1bbb1afd79"
HARNESS = Path("barracora-1981/harness")
OUTPUT = Path("evidence/runtime/system-7/barracora-1981.json")
READINGS = Path("tools/seeds/williams/barracora-1981-display-readings.json")
SCENARIOS = {
	"init": "tools/harness-scenarios/system-7/barracora-nvram-init.json",
	"sol": "tools/harness-scenarios/system-7/barracora-solenoid-test.json",
	"sw": "tools/harness-scenarios/system-7/barracora-switch-test.json",
	"play": "tools/harness-scenarios/system-7/barracora-gameplay.json",
}
# Seven-segment code (low seven bits) to character; bit 0x80 is the comma.
DECODER = {0: " ", 63: "0", 6: "1", 91: "2", 79: "3", 102: "4", 109: "5", 125: "6", 124: "6", 7: "7", 127: "8", 111: "9", 103: "9"}
BALL_IN_PLAY = (4, 5)
CREDITS = (6, 7)
PLAYER_1 = 2
SPECIALS = {20: 18, 21: 19, 22: 20, 29: 21, 30: 22}

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
			raise RuntimeError("display-readings seed is not Barracora's")
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

	def pair(self, run: str, snapshot: int, indices: tuple[int, int], address: int | None = None) -> tuple[list[dict[str, Any]], str]:
		responses = [self.response(run, snapshot, i, address) for i in indices]
		return responses, "".join(r["interpreted_text"] for r in responses)

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
	bip, bip_text = frames.pair("init", 1, BALL_IN_PLAY)
	credit, credit_text = frames.pair("init", 1, CREDITS)
	if (credit_text, bip_text) != ("04", "00"):
		raise RuntimeError("init run is not on the Diagnostic Mode screen")
	return {
		"named_action_observations": [{
			"label": f"power-up from empty CMOS: credits {credit_text}, ball in play {bip_text}, player 1 '{p1['interpreted_text']}'",
			"input_kind": "key", "input_name": "power-up with no host input", "observed_switch_addresses": [],
			"display_responses": [p1, *bip, *credit], "active_solenoid_addresses": sorted(snap[1]["active_solenoids"]),
			"transitioned_solenoid_addresses": [], "result": "observed"}],
		"note": "The drawing set's Power Turn-On page describes the Diagnostic Mode as credits 04, ball in play 00 and the game identification in the player 1 display; one power-up from empty CMOS stops there. This run writes the NVRAM every later run starts from.",
	}


def solenoid_test_observations(frames: Frames, run: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
	steps, snaps = run["steps"], run["snapshots"]
	if len(snaps) != len(steps) + 1 or any(s["label"] != t["label"] for s, t in zip(snaps[1:], steps)):
		raise RuntimeError("solenoid-test snapshots do not pair one-to-one with steps")
	entry = next(i for i, t in enumerate(steps) if t["label"].startswith("Advance: Test 02"))
	actions, mapping = [], {}
	credit, credit_text = frames.pair("sol", entry + 1, CREDITS)
	bip, bip_text = frames.pair("sol", entry + 1, BALL_IN_PLAY, 1)
	if credit_text != "02" or bip_text != "01" or step_solenoids(steps[entry]) != [1]:
		raise RuntimeError("Test 02 entry does not show 02 / 01 with solenoid 1")
	mapping["1"] = 1
	actions.append({"label": "Advance into Test 02: credits 02, ball in play 01, solenoid 1 pulses", "input_kind": "switch", "input_address": -7,
		"observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7], "display_responses": [*credit, *bip],
		"active_solenoid_addresses": sorted(snaps[entry + 1]["active_solenoids"]), "transitioned_solenoid_addresses": [1], "result": "observed"})
	expected = 2
	for index in range(entry + 1, len(steps)):
		step = steps[index]
		if not step["label"].startswith("Advance: next solenoid step"):
			continue
		number = expected if expected <= 25 else 1
		responses, text = frames.pair("sol", index + 1, BALL_IN_PLAY, number)
		transitioned = step_solenoids(step)
		if text != f"{number:02d}" or transitioned != [number]:
			raise RuntimeError(f"Test 02 step {number} is not shown and pulsed alone")
		if expected <= 25:
			mapping[str(number)] = transitioned[0]
		states = next(t["states"] for t in step["transitions"]["solenoids"])
		actions.append({"label": f"Advance: Test 02 step {text}, public solenoid {number} transitions {states}", "input_kind": "switch",
			"input_address": -7, "observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7], "display_responses": responses,
			"active_solenoid_addresses": sorted(snaps[index + 1]["active_solenoids"]), "transitioned_solenoid_addresses": transitioned, "result": "observed"})
		expected += 1
	if sorted(mapping, key=int) != [str(n) for n in range(1, 26)]:
		raise RuntimeError("Test 02 did not step through 01-25")
	lamps = sorted({e["number"] for e in run["events"] if e["event"] == "lamp"})
	sequence = [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"] == 1]
	return {
		"named_action_observations": actions,
		"ordered_solenoid_on_sequence": sequence,
		"solenoid_addresses_seen": sorted(set(sequence)),
		"note": f"Each Advance in Manual-Down shows the next step number in the ball-in-play display and transitions that public solenoid alone; step 25 wraps to 01. Step 16 pulses the coin lockout from its energized game-over rest and leaves it off; step 25 pulses game-on 25 off from its energized rest, which is the booklet's 'Flipper relay is de-energized with subtest 25'. Steps 23 and 24 are pulsed although Table 4 fits no load there. Test 01 (lamps) drove {len(lamps)} lamp addresses, {lamps[0]}-{lamps[-1]}.",
	}, mapping


def switch_test_observations(frames: Frames, run: dict[str, Any]) -> dict[str, Any]:
	snaps, steps = run["snapshots"], run["steps"]
	by_label: dict[str, int] = {}
	for index, snap in enumerate(snaps):
		if snap["label"] in by_label:
			by_label[snap["label"]] = -1
		else:
			by_label[snap["label"]] = index

	def find(label: str) -> int:
		index = by_label.get(label, -1)
		if index < 0:
			raise RuntimeError(f"switch-test snapshot missing or repeated: {label}")
		return index

	entry = find("Advance: Test 03 switch test, 03 in the credit display, nothing reported at rest")
	credit, credit_text = frames.pair("sw", entry, CREDITS)
	bip, bip_text = frames.pair("sw", entry, BALL_IN_PLAY)
	if credit_text != "03" or bip_text.strip():
		raise RuntimeError("Test 03 entry is not 03 with a blank ball-in-play display")
	actions = [{"label": "Advance into Test 03: credits 03, ball in play blank", "input_kind": "switch", "input_address": -7,
		"observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7], "display_responses": [*credit, *bip],
		"active_solenoid_addresses": sorted(snaps[entry]["active_solenoids"]), "transitioned_solenoid_addresses": [], "result": "observed"}]
	shown, blank = [], []
	for number in range(1, 65):
		index = find(f"close public switch {number} and read the ball-in-play display (held)")
		if watched(snaps[index]).get(number) != 1:
			raise RuntimeError(f"switch {number} was not held in its snapshot")
		responses, text = frames.pair("sw", index, BALL_IN_PLAY, number if number <= 48 else None)
		if number <= 48 and text != f"{number:02d}":
			raise RuntimeError(f"Test 03 does not name held switch {number}")
		if number > 48 and text.strip():
			raise RuntimeError(f"Test 03 names unfitted switch {number}")
		(shown if number <= 48 else blank).append(number)
		actions.append({"label": f"hold public switch {number}: ball in play '{text}'", "input_kind": "switch", "input_address": number,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [number], "display_responses": responses,
			"active_solenoid_addresses": sorted(snaps[index]["active_solenoids"]), "transitioned_solenoid_addresses": [],
			"result": "observed" if number <= 48 else "no_matching_transition"})
	for number in (33, 34, 35):
		label = ("one-shot control: write public 33 once and read the ball-in-play display" if number == 33
			else f"one-shot: write lane-change matrix {number} once and read the ball-in-play display")
		index = find(label)
		state = watched(snaps[index]).get(number)
		responses, text = frames.pair("sw", index, BALL_IN_PLAY, 33 if number == 33 else None)
		if (number == 33) != (state == 1 and text == "33") or (number != 33 and (state != 0 or text.strip())):
			raise RuntimeError(f"one-shot write to {number} did not behave as recorded")
		actions.append({"label": f"one-shot write of public {number}: watched state {state}, ball in play '{text}'"
			+ ("" if number == 33 else "; PinMAME's flipper-button copy overwrote the write"), "input_kind": "switch", "input_address": number,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [number], "display_responses": responses,
			"active_solenoid_addresses": sorted(snaps[index]["active_solenoids"]), "transitioned_solenoid_addresses": [],
			"result": "observed" if number == 33 else "no_matching_transition"})
	for button, copy, pair in ((84, 34, [47, 48]), (82, 35, [45, 46])):
		side = "left" if button == 84 else "right"
		index = find(f"hold synthetic {side} flipper button {button} and read the ball-in-play display (held)")
		levels = watched(snaps[index])
		responses, text = frames.pair("sw", index, BALL_IN_PLAY, copy)
		held = sorted(set(snaps[index]["active_solenoids"]) & {45, 46, 47, 48})
		step = next(s for s in steps if s.get("switch") == button)
		if levels.get(button) != 1 or levels.get(copy) != 1 or text != str(copy) or held != pair or step_solenoids(step) != pair:
			raise RuntimeError(f"button {button} is not copied into {copy} with outputs {pair}")
		actions.append({"label": f"hold {side} flipper button {button}: matrix {copy} reads 1, ball in play '{text}', outputs {pair}",
			"input_kind": "switch", "input_address": button, "observed_switch_addresses": [copy], "host_stimulus_switch_addresses": [button],
			"display_responses": responses, "active_solenoid_addresses": sorted(snaps[index]["active_solenoids"]),
			"transitioned_solenoid_addresses": pair, "held_synthetic_solenoid_addresses": held, "result": "observed"})
	return {
		"named_action_observations": actions,
		"note": f"Held closures of public {shown[0]}-{shown[-1]} each show their own number in the ball-in-play display; {blank[0]}-{blank[-1]} show nothing. A one-shot write survives on 33 but not on 34 or 35, which PinMAME rewrites from the flipper buttons on every update; holding 84 reports 34 and holding 82 reports 35.",
		"limitation": "The booklet says Test 03 shows a switch number only momentarily; readings are taken from held snapshots. A blank reading for 49-64 agrees with the matrix's NOT USED cells but is not itself proof that no contact is fitted.",
	}


# Expected solenoid turn-on order in the window after each named gameplay input.
GAMEPLAY_ORDER = {
	"coin on the right coin switch": [15, 15, 15],
	"credit button: start a one-player game; the ball ramp thrower serves a ball": [25, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 12],
	"ball plunged": [17],
	"left jet bumper scoring switch": [18],
	"right jet bumper scoring switch": [19],
	"bottom jet bumper scoring switch": [20],
	"left kicker scoring switch": [21],
	"right kicker scoring switch": [22],
	"1/4 top lane rollover": [],
	"right flipper button (synthetic 82): lane change": [45, 46],
	"left flipper button (synthetic 84): lane change": [47, 48],
	"B-A-RR bank: RR target down out of sequence": [3],
	"B-A-RR bank: RR target down, bank complete in sequence": [3, 2, 1],
	"A-C-O-R-A bank: last A target down, bank complete in sequence": [8, 7, 6, 5, 4],
	"ball enters the lit upper eject hole": [12],
	"second ball plunged": [],
	"ball enters the lit lower eject hole": [12],
	"third ball plunged": [17, 13],
	"upper eject hole empties": [14],
	"one ball drains into the outhole": [11],
	"ball roll tilt, first closure": [],
}
# Lamps 17-24 that change state after the top-lane and lane-change inputs: (lit, extinguished).
LANE_LAMPS = {
	"1/4 top lane rollover": ([17], []),
	"right flipper button (synthetic 82): lane change": ([18], [17]),
	"left flipper button (synthetic 84): lane change": ([], []),
}


def gameplay_observations(run: dict[str, Any]) -> dict[str, Any]:
	steps, events, snaps = run["steps"], run["events"], run["snapshots"]
	host = [e for e in events if e["event"] == "switch" and "step" in e]
	solenoid_events = [e for e in events if e["event"] == "solenoid"]
	labels = [s["label"] for s in snaps]
	if len(set(labels)) != len(labels):
		raise RuntimeError("gameplay snapshot labels repeat")
	groups: list[list[dict[str, Any]]] = []
	for step in steps:
		if "switch" in step:
			groups.append([step])
		elif groups:
			groups[-1].append(step)
	starts = []
	for group in groups:
		times = [e["time_s"] for e in host if e["step"] == group[0]["step"]]
		if not times:
			raise RuntimeError(f"no host input recorded for step {group[0]['step']}")
		starts.append(min(times))
	actions, facts = [], {}
	for position, group in enumerate(groups):
		start = starts[position]
		end = starts[position + 1] if position + 1 < len(groups) else float("inf")
		on = [e for e in solenoid_events if e["state"] == 1 and start <= e["time_s"] < end]
		off = [e for e in solenoid_events if e["state"] == 0 and start <= e["time_s"] < end]
		order = [e["number"] for e in on]
		name, switch = group[0]["label"], group[0]["switch"]
		lit = sorted({t["number"] for s in group for t in s["transitions"]["lamps"] if t["states"][-1] == 1 and 17 <= t["number"] <= 24})
		out = sorted({t["number"] for s in group for t in s["transitions"]["lamps"] if t["states"][-1] == 0 and 17 <= t["number"] <= 24})
		if name in GAMEPLAY_ORDER and order != GAMEPLAY_ORDER[name]:
			raise RuntimeError(f"gameplay order changed after '{name}': {order}")
		if name in LANE_LAMPS and (lit, out) != LANE_LAMPS[name]:
			raise RuntimeError(f"lane lamps changed after '{name}': {lit} {out}")
		held = f"{name} (held)"
		snapshot = snaps[labels.index(held)] if held in labels else snaps[labels.index(group[-1]["label"])]
		observed = [n for n in (34, 35) if switch in (82, 84) and watched(snapshot).get(n) == 1]
		if switch in (82, 84) and observed != [34 if switch == 84 else 35]:
			raise RuntimeError(f"button {switch} was not copied into its lane-change switch")
		text = f"{name}: solenoids on in order {order}" if order else f"{name}: no solenoid turns on in the window"
		if off and not order:
			text += f"; off {[e['number'] for e in off]}"
		if name in LANE_LAMPS:
			text += f"; lamps lit {lit}, extinguished {out} among 17-24"
		action = {"label": text, "input_kind": "switch", "input_address": switch, "observed_switch_addresses": observed,
			"host_stimulus_switch_addresses": sorted({s["switch"] for s in group if "switch" in s}),
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"transitioned_solenoid_addresses": sorted({n for s in group for n in step_solenoids(s)}),
			"result": "observed" if on or off or lit or out else "no_matching_transition"}
		if switch in (82, 84):
			action["held_synthetic_solenoid_addresses"] = sorted(set(snapshot["active_solenoids"]) & {45, 46, 47, 48})
		actions.append(action)
		facts[name] = {"start": start, "on": on, "off": off}
	if set(GAMEPLAY_ORDER) - set(facts):
		raise RuntimeError(f"gameplay inputs missing: {sorted(set(GAMEPLAY_ORDER) - set(facts))}")
	plunge = facts["ball plunged"]
	third = facts["third ball plunged"]
	lower = facts["ball enters the lit lower eject hole"]
	upper = facts["ball enters the lit upper eject hole"]
	tilt = facts["ball roll tilt, first closure"]
	if [e["number"] for e in tilt["off"]] != [25]:
		raise RuntimeError("ball roll tilt did not drop game-on 25 alone")
	gate_close = next(e for e in solenoid_events if e["number"] == 17 and e["state"] == 0)
	return {
		"named_action_observations": actions,
		"ordered_solenoid_on_sequence": [e["number"] for e in solenoid_events if e["state"] == 1],
		"solenoid_addresses_seen": sorted({e["number"] for e in solenoid_events}),
		"note": (
			"Coin switch 4 fires the bell 15 three times. Start fires game-on 25, both bank releases 9 and 10, the eight single-target resets 1-8 in order and the ball ramp thrower 12. "
			f"The upper eject hole gate 17 energizes {plunge['on'][0]['time_s'] - plunge['start']:.2f} s after the shooter switch 16 opens and drops "
			f"{gate_close['time_s'] - upper['on'][0]['time_s']:.2f} s after the thrower serves the next ball for an upper eject hole lock. "
			"An out-of-sequence RR target fires only its own reset 3; a completed B-A-RR bank fires 3, 2, 1 and a completed A-C-O-R-A bank 8, 7, 6, 5, 4, each raising its targets one by one with no bank release. "
			"Switches 20, 21, 22, 29 and 30 fire 18, 19, 20, 21 and 22 within 20 ms. Top lane 17 lit lane lamp 17; the right button moved it to 18; the left button changed nothing with no lamp of 20-22 lit. "
			f"A ball in the lit upper eject hole fires the thrower {upper['on'][0]['time_s'] - upper['start']:.2f} s later; in the lit lower eject hole {lower['on'][0]['time_s'] - lower['start']:.2f} s later. "
			f"{third['on'][0]['time_s'] - third['start']:.2f} s after the third plunge the gate energizes and the upper eject hole kicks, and the lower eject hole kicks when the upper hole switch opens. "
			f"An outhole closure fires the ball release 11; the ball roll tilt drops game-on 25 {tilt['off'][0]['time_s'] - tilt['start']:.2f} s after the closure."),
		"limitation": "The host writes every ball-presence switch itself (ramp positions, shooter lane, eject holes, outhole); those writes are stimulus, not ROM evidence, and a wait that ends on an output censors how long that output would have stayed on. Lamp numbers are public addresses only.",
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
		"extractor": {"id": "tools/barracora_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [{"line_start": 1, "line_end": 1, "status": "candidate", "text": (
			"barra_l1 Test 02 steps 01-25 pulse public solenoids 1-25 one at a time; Test 03 names held switches 1-48 and nothing for 49-64; "
			"buttons 84 and 82 are copied into 34 and 35 and fabricate 47/48 and 45/46. Gameplay shows the five switch-fired specials, "
			"the start sequence, bank resets, the eject-hole lock, 3-ball Multi-Ball, the outhole kick and the ball roll tilt. "
			"No run establishes bulb quantity, physical location or mechanical timing.")}],
		"runtime": {
			"command_template": "python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-46e1a01a/Release/pinmame64.dll --game barra_l1 --rom-path <authorized-rom-root> --work-dir <working-root>/review-artifacts/barracora-1981/harness/<name>-state --scenario <scenario_path> --output <working-root>/review-artifacts/barracora-1981/harness/<name>.json",
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
			"path": "external:pinmame-review-artifacts/barracora-1981/harness/manifest.json",
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
