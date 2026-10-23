"""Derive the compact Creature from the Black Lagoon runtime evidence from the retained raw harness runs.

Each document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts root),
checks that it ran the committed scenario, the pinned binary and the cftbl_l4 ROM (the prototype cftbl_p3 ROM for the runs
prefixed p3-) with built-in mechanisms disabled, and writes the derived observations beside the other runtime evidence. A
diagnostic snapshot's ``interpreted_text`` is the curator's visual reading of that snapshot's retained DMD frame; its
``pixel_sha256`` pins the frame. The tool refuses a raw run whose transitions no longer support a stated observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.creature-from-the-black-lagoon.1992"
GAME = "cftbl_l4"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "a1eb5cb3d1f8a7b48592f9ed8b789c45d201260b37bf6bf7ac6db88d6cec1b09"
# The prototype P-3 ROM replays the same scenarios; its runs live beside the L-4 runs with a "p3-" prefix.
P3_GAME = "cftbl_p3"
P3_ROM_ARCHIVE_SHA256 = "8717d3e7f77871fd9fe032829a26d3d0aa253f7773c568f8c10090a8757ce2ba"
ROMS = {GAME: ("", ROM_ARCHIVE_SHA256), P3_GAME: ("p3-", P3_ROM_ARCHIVE_SHA256)}
HARNESS_DIRECTORY = "creature/harness"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/wpc-fliptronic"
SCENARIO_DIRECTORY = "tools/harness-scenarios/wpc-fliptronic"
FRAME_READINGS_PATH = ROOT / "tools/seeds/bally/creature-from-the-black-lagoon-1992-frame-readings.json"
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are "
	"host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation "
	"is counted pulses; every diagnostic snapshot's interpreted_text is the curator's visual reading of its retained DMD frame, "
	"identified by its pixel SHA-256. The exact external directory manifest (built by tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)
NVRAM_NOTE = (
	"empty; the run created its own isolated PinMAME state directory, so the ROM performed its own factory reset before the "
	"scenario left the message loop with Escape"
)
IDENTIFICATION_LABEL = "Enter 1 (game identification)"

# T.5 FLASHER TEST: the order the ROM steps with Up, each name and drive/supply wire pair as printed.
T5_ORDER = (2, 8, 9, 10, 11, 16, 17, 18, 19, 22, 25, 33, 34, 35, 36)
T5_NAMES = {
	2: "LFT SUBWAY FLSHR", 8: "BOTM RGHT FLSHR", 9: "BACK FLASHERS", 10: "BOWL FLASHER", 11: "3D FLSHR", 16: "R. POPPER FLSHR",
	17: "BOTM LFT FLSHR", 18: "RGHT RAMP FLSHR", 19: "LFT RMP FLSHR", 22: "CNTR HOLE FLSHR", 25: "START MOVIE FL.",
	33: "CREATURE FL. 1", 34: "CREATURE FL. 2", 35: "CREATURE FL. 3", 36: "CREATURE FL. 4",
}
# The P-3 prototype ROM prints two of the names differently; the addresses and wires are the same.
P3_T5_NAMES = {2: "LFT SUBWAY FLHR", 11: "CREATURE FLSHR"}
T5_WIRES = {
	2: "VIO-RED", 8: "VIO-GRY", 9: "BRN-BLK", 10: "BRN-RED", 11: "BRN-ORN", 16: "BRN-GRY", 17: "BLK-BRN", 18: "BLK-RED",
	19: "BLK-ORN", 22: "BLU-BLK", 25: "BLU-BRN", 33: "BLK-YEL", 34: "ORN-VIO", 35: "BLK-BLU", 36: "ORN-GRY",
}

# T.1 SWITCH EDGES: the stimulus addresses and the coils the ROM answered with.
T1_ADDRESSES = (25, 34, 115, 116, 117, 118)
T1_COILS = {116: {45, 46}, 118: {47, 48}}

# T.12 FLIPPER COIL TEST: the ROM's four steps; a power step publishes the hold winding with the power winding.
T12_ORDER = (45, 46, 47, 48)
T12_NAMES = {45: "R. FLIP. POWER", 46: "R. FLIP. HOLD", 47: "L. FLIP. POWER", 48: "L. FLIP. HOLD"}
T12_WIRES = {45: "BLU-VIO BLU-YEL", 46: "ORN-GRN BLU-YEL", 47: "BLU-GRY GRY-YEL", 48: "ORN-BLU GRY-YEL"}
T12_PUBLISHED = {45: {45, 46}, 46: {46}, 47: {47, 48}, 48: {48}}
T12_FRAMES = {45: "T.12 step 0, frame 1", 46: "T.12 step 1", 47: "T.12 step 2", 48: "T.12 step 3"}

CHASE_LAMPS = tuple(range(91, 99))


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(review_root: Path, directory: str, game: str = GAME) -> dict[str, Any]:
	name = ROMS[game][0] + directory
	run_directory = review_root / HARNESS_DIRECTORY / name
	run_path = run_directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / SCENARIO_DIRECTORY / f"{directory}.json"
	if run.get("failure") is not None or run.get("game") != game:
		raise ValueError(f"not a successful Creature {game} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(run_directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != 0:
		raise ValueError(f"built-in mechanisms must be disabled: {run_path}")
	run["_directory"] = run_directory
	run["_game"] = game
	run["_name"] = name
	run["_scenario"] = directory
	run["_pins"] = json.loads(FRAME_READINGS_PATH.read_bytes())["runs"][name]
	return run


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


def _risen(step: dict[str, Any], channel: str = "solenoids") -> set[int]:
	"""Addresses whose recorded transitions during the step include an active state, without 31 (the WPC GILAMPS bit-7 mirror)."""
	return {item["number"] for item in step["transitions"].get(channel, []) if any(item["states"])} - {31}


def _moved(step: dict[str, Any], channel: str) -> set[int]:
	return {item["number"] for item in step["transitions"].get(channel, [])}


def _window(run: dict[str, Any], prefix: str, channel: str = "solenoids") -> set[int]:
	"""Addresses that rose over a step and the frames taken after it.

	Read from the event log between the snapshot before the step and the step's last frame: a step's own transition summary can
	drop a pulse shorter than one poll that straddles two actions, while the event log keeps every edge.
	"""
	labels = [item["label"] for item in run["snapshots"]]
	members = [index for index, label in enumerate(labels) if label == prefix or label.startswith(prefix + ", frame")]
	if not members:
		raise ValueError(f"no snapshot for {prefix!r}")
	start = run["snapshots"][members[0] - 1]["time_s"]
	end = run["snapshots"][members[-1]]["time_s"]
	event = {"solenoids": "solenoid", "lamps": "lamp", "gis": "gi"}[channel]
	return {item["number"] for item in run["events"] if item["event"] == event and item["state"] and start < item["time_s"] <= end} - {31}


def _diagnostic(run: dict[str, Any], label: str) -> dict[str, Any]:
	"""A visual reading of one retained frame, refused unless that frame's own PGM file carries the snapshot's pixels and is not blank."""
	snapshot = _snapshot(run, label)
	displays = [item for item in snapshot["displays"] if item["index"] == 0]
	if len(displays) != 1:
		raise ValueError(f"snapshot {label!r} must carry display 0 exactly once")
	frame = run["_directory"] / "dmd" / Path(displays[0]["artifact"].replace("\\", "/")).name
	data = frame.read_bytes()
	pixels = data[len(data) - 128 * 32:]
	if not data.startswith(b"P5\n128 32\n") or hashlib.sha256(pixels).hexdigest() != displays[0]["pixel_sha256"]:
		raise ValueError(f"retained frame for {label!r} does not carry the snapshot's pixels: {frame}")
	if displays[0]["nonzero_pixels"] == 0 or not any(pixels):
		raise ValueError(f"a reading cannot cite a blank frame: {label!r}")
	pin = run["_pins"].get(label)
	if pin is None or pin["pixel_sha256"] != displays[0]["pixel_sha256"]:
		raise ValueError(f"snapshot {label!r} does not carry the frame the curator read")
	return {
		"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
		"display_index": 0,
		"interpreted_text": pin["reading"],
		"label": label,
		"nonzero_pixels": displays[0]["nonzero_pixels"],
		"pixel_sha256": displays[0]["pixel_sha256"],
	}


def _reading(run: dict[str, Any], label: str) -> str:
	return run["_pins"][label]["reading"]


def _seen(run: dict[str, Any], event: str = "solenoid") -> list[int]:
	return sorted({item["number"] for item in run["events"] if item["event"] == event and item["state"]})


def _observation(label: str, stimulus: list[int], solenoids: list[int] | None = None) -> dict[str, Any]:
	return {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": stimulus,
		"input_address": stimulus[-1],
		"input_kind": "switch",
		"label": label,
		"observed_switch_addresses": [],
		"result": "observed",
		"transitioned_solenoid_addresses": solenoids or [],
	}


def _command(scenario: str, extra: str, game: str = GAME) -> str:
	return (
		f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game} --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
		f"--handle-mechanics 0 --scenario {SCENARIO_DIRECTORY}/{scenario}.json --dmd-dir <external-dmd-dir> --output <external-run.json>. "
		+ extra
	)


def _document(run: dict[str, Any], observations: dict[str, Any], command: str) -> dict[str, Any]:
	directory = run["_name"]
	return {
		"driver_ids": [run["_game"]],
		"extractor": {"id": "tools/creature_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": command,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": run["_game"],
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": directory,
					"nvram_initialization": NVRAM_NOTE,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}/run.json",
					"scenario_path": f"{SCENARIO_DIRECTORY}/{run['_scenario']}.json",
					"scenario_sha256": run["scenario"]["sha256"],
					"self_test_pulses": 0,
					"snapshot_count": len(run["snapshots"]),
					"watch_switches": run["watch_switches"],
				}
			],
			"rom_archive_sha256": ROMS[run["_game"]][1],
		},
		"source": {
			"attribution": ATTRIBUTION,
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def build_flashers(review_root: Path, game: str = GAME) -> dict[str, Any]:
	run = _load_run(review_root, "cftbl-flasher-test", game)
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL)]
	matched = {item["number"] for item in _step(run, "checkpoint: T.5 pulses a flasher").get("matched_outputs") or []}
	if matched != {2}:
		raise ValueError(f"T.5 must start on flasher 2, matched {sorted(matched)}")
	named = []
	for index, address in enumerate((*T5_ORDER, T5_ORDER[0])):
		label = "T.5 step 0, frame 1" if index == 0 else f"T.5 step {index}"
		window = _window(run, f"T.5 step {index}") | (_risen(_step(run, "Enter (start T.5 FLASHER TEST)")) if index == 0 else set())
		previous = T5_ORDER[index - 1] if index else address
		if address not in window or not window <= {address, previous}:
			raise ValueError(f"T.5 step {index} pulsed {sorted(window)}, not {address}")
		names = {**T5_NAMES, **(P3_T5_NAMES if game == P3_GAME else {})}
		expected = f"{names[address]} / T.5 {address:02d} REPEAT / {T5_WIRES[address]} RED-WHT"
		if _reading(run, label) != expected:
			raise ValueError(f"the reading of {label!r} does not name public {address}")
		snapshots.append(_diagnostic(run, label))
		if index < len(T5_ORDER):
			named.append(_observation(
				f"T.5 FLASHER TEST selects public {address} ({names[address]}, drive wire {T5_WIRES[address]}, supply RED-WHT): "
				"the ROM pulses it repeatedly",
				[8] if index == 0 else [7], [address],
			))
	if set(_seen(run)) - {*T5_ORDER, 20, 24, 31}:
		raise ValueError(f"T.5 pulsed an unexpected address: {_seen(run)}")
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"cftbl-flasher-test",
		"Each Up press selects the next flasher; in repeat mode the ROM pulses it until the next press and prints its own name, its "
		"number (which equals the public address PinMAME publishes) and the drive and supply wire colours. The test steps fifteen "
		"flashers, 02 to 36, and wraps to 02. Solenoids 20 and 24 move throughout because the attract-mode chase-light decoder runs "
		"in the background.",
		game,
	)
	return _document(run, observations, command)


def build_edges(review_root: Path, game: str = GAME) -> dict[str, Any]:
	run = _load_run(review_root, "cftbl-switch-edges-fliptronic", game)
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL)]
	named = []
	for address in T1_ADDRESSES:
		for level in (1, 0):
			held = {item["number"]: item["state"] for item in _snapshot(run, f"{address} -> {level}")["watched_switches"]}
			if held.get(address) != level:
				raise ValueError(f"host did not drive {address} to {level}")
			snapshots.append(_diagnostic(run, f"{address} -> {level}"))
		rising = _risen(_step(run, f"{address} -> 1")) | _window(run, f"T.1 with {address} at 1")
		expected = T1_COILS.get(address, set())
		if rising != expected:
			raise ValueError(f"public {address} fired {sorted(rising)}, expected {sorted(expected)}")
		on = _snapshot(run, f"{address} -> 1")["displays"][0]["pixel_sha256"]
		off = _snapshot(run, f"{address} -> 0")["displays"][0]["pixel_sha256"]
		if on == off:
			raise ValueError(f"public {address} at 1 must change the T.1 frame")
		head = _reading(run, f"{address} -> 1").split(" / ")[0]
		if address in T1_COILS:
			label = (
				f"T.1 with host public {address} set to 1: the ROM fires the lower {'right' if address == 116 else 'left'} flipper "
				f"({'/'.join(map(str, sorted(expected)))}, power then hold while the input stays at 1) and names the synthesized "
				f"end-of-stroke bit ({head}); at 0 the hold winding drops and the name clears"
			)
		elif head == "SWITCH EDGES":
			label = f"T.1 with host public {address} at 1: the switch grid marks it closed, the ROM names no switch and drives no output; at 0 the mark clears"
		else:
			label = f"T.1 names {head!r} while host public {address} is 1 and clears it at 0; no output moves"
		named.append(_observation(label, [address], sorted(rising)))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"cftbl-switch-edges-fliptronic",
		"Built-in mechanisms stay disabled. Each set_switch holds one public level for 1.5 s; the snapshot after it records the ROM's "
		"T.1 display and the watched public switch levels. An ordinary rollover (25) and a masked opto (34) are controls; 115-118 "
		"are the upper Fliptronic positions, which cftblGameData does not synthesize (FLIP_SOL(FLIP_L) only).",
		game,
	)
	return _document(run, observations, command)


def build_flippers(review_root: Path, game: str = GAME) -> dict[str, Any]:
	run = _load_run(review_root, "cftbl-flipper-coil-test", game)
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL)]
	named = []
	for index, address in enumerate(T12_ORDER):
		window = _window(run, f"T.12 step {index}") | (_risen(_step(run, "Enter (start T.12 FLIPPER COIL TEST)")) if index == 0 else set())
		if window != T12_PUBLISHED[address]:
			raise ValueError(f"T.12 step {index} published {sorted(window)}, not {sorted(T12_PUBLISHED[address])}")
		expected = f"{T12_NAMES[address]} / T.12 {index + 1:02d} REPEAT / {T12_WIRES[address]}"
		if _reading(run, T12_FRAMES[address]) != expected:
			raise ValueError(f"the reading of {T12_FRAMES[address]!r} does not name public {address}")
		snapshots.append(_diagnostic(run, T12_FRAMES[address]))
		named.append(_observation(
			f"T.12 FLIPPER COIL TEST item {index + 1:02d} ({T12_NAMES[address]}, {T12_WIRES[address]}) publishes {'/'.join(map(str, sorted(T12_PUBLISHED[address])))}",
			[8] if index == 0 else [7], sorted(T12_PUBLISHED[address]),
		))
	if _window(run, "T.12 step 4") != T12_PUBLISHED[45] or _reading(run, "T.12 step 4") != _reading(run, T12_FRAMES[45]):
		raise ValueError("T.12 must wrap to item 01 after four items")
	snapshots.append(_diagnostic(run, "T.12 step 4"))
	if set(_seen(run)) & {33, 34, 35, 36}:
		raise ValueError("T.12 must not drive the upper Fliptronic outputs 33-36")
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"cftbl-flipper-coil-test",
		"Each Up press selects the next flipper winding; in repeat mode the ROM pulses it. The test has four items, the two lower "
		"flippers' power and holding windings, and wraps; it never drives the upper Fliptronic outputs 33-36.",
		game,
	)
	return _document(run, observations, command)


def build_chase(review_root: Path, game: str = GAME) -> dict[str, Any]:
	run = _load_run(review_root, "cftbl-ramp-lights-test", game)
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL)]
	for label in ("Enter (start T.15 RAMP LIGHTS TEST)", "Enter (T.15 stopped)", "Enter (T.15 cycling again)"):
		snapshots.append(_diagnostic(run, label))
	cycling = [step for step in run["steps"] if step["label"].startswith("T.15 cycling, frame")]
	for step in cycling:
		lamps = {item["number"]: item["states"] for item in step["transitions"].get("lamps", [])}
		if set(lamps) != set(CHASE_LAMPS):
			raise ValueError(f"{step['label']}: the chase must move all of 91-98, moved {sorted(lamps)}")
		for number in range(91, 95):
			if lamps[number] != lamps[number + 4]:
				raise ValueError(f"{step['label']}: lamp {number + 4} does not mirror lamp {number}")
	start = _snapshot(run, "Enter (start T.15 RAMP LIGHTS TEST)")["time_s"]
	end = _snapshot(run, "T.15 cycling, frame 12")["time_s"]
	rises = [event["number"] for event in run["events"] if event["event"] == "lamp" and event["number"] in range(91, 95) and event["state"] and start < event["time_s"] <= end]
	steps = [number for index, number in enumerate(rises) if index == 0 or number != rises[index - 1]]
	if len(steps) < 40 or any(b != (a - 90) % 4 + 91 for a, b in zip(steps, steps[1:])):
		raise ValueError("the chase must advance 91, 92, 93, 94 and wrap throughout the first cycling phase")
	stopped = _step(run, "Enter (T.15 stopped)")
	if {item["number"]: item["states"][-1] for item in stopped["transitions"].get("gis", [])} != {0: 0, 3: 0}:
		raise ValueError("stopping T.15 must switch G.I. 0 and 3 off and leave the other strings")
	# While stopped, every frame has G.I. 0 and 3 off; PinMAME's chase lamps still publish one selected pair (the P-3 ROM keeps
	# pulsing its selection, so some of its frames fall between pulses and publish none).
	pairs = set()
	for index in range(1, 5):
		frame = _snapshot(run, f"T.15 stopped, frame {index}")
		published = set(frame["active_lamps"]) & set(CHASE_LAMPS)
		if {0, 3} & set(frame["active_gis"]) or (published and not any(published == {n, n + 4} for n in range(91, 95))):
			raise ValueError(f"T.15 stopped, frame {index}: G.I. 0 and 3 must be off and the chase lamps must show at most one pair")
		if published:
			pairs.add(tuple(sorted(published)))
	if len(pairs) != 1:
		raise ValueError(f"while T.15 is stopped PinMAME must publish one chase pair, saw {sorted(pairs)}")
	stopped_pair = list(pairs.pop())
	restarted = _step(run, "Enter (T.15 cycling again)")
	if {item["number"]: item["states"][-1] for item in restarted["transitions"].get("gis", [])} != {0: 8, 3: 8}:
		raise ValueError("restarting T.15 must switch G.I. 0 and 3 back on")
	start_solenoids = _moved(_step(run, "Enter (start T.15 RAMP LIGHTS TEST)"), "solenoids")
	if not {20, 24} <= start_solenoids:
		raise ValueError("T.15 must drive the chase-select solenoids 20 and 24")
	named = [
		_observation(
			"T.15 RAMP LIGHTS TEST cycling: the ROM steps solenoids 20 and 24 through the four decoder codes and PinMAME's computed "
			"chase lamps come on in the order 91, 92, 93, 94 and wrap, each of 95-98 changing with its partner 91-94",
			[8], [20, 24],
		),
		_observation(
			"Enter stops T.15: the ROM switches G.I. strings 0 and 3 off and no other string changes, while PinMAME keeps publishing the "
			f"selected chase pair ({stopped_pair[0]} and {stopped_pair[1]}), so lamps 91-98 carry the decoder selection whatever the "
			"G.I.; Enter again restores both strings to full brightness",
			[8], [],
		),
	]
	observations = {
		"diagnostic_snapshots": snapshots,
		"gi_addresses_seen": sorted({item["number"] for item in run["events"] if item["event"] == "gi"}),
		"lamp_addresses_seen": sorted(set(_seen(run, "lamp")) & set(CHASE_LAMPS)),
		"named_action_observations": named,
		"solenoid_addresses_seen": _seen(run),
	}
	command = _command(
		"cftbl-ramp-lights-test",
		"T.15 RAMP LIGHTS TEST runs in its cycling mode, is stopped with Enter and restarted. Twelve frames 0.25 s apart cover the "
		"first cycling phase; the lamp transitions recorded in each frame are the chase lamps 91-98 PinMAME computes from solenoids 20 "
		"and 24 (WPC_CFTBL), and the G.I. transitions are the strings the ROM switches.",
		game,
	)
	return _document(run, observations, command)


def build_subways(review_root: Path, game: str = GAME) -> dict[str, Any]:
	run = _load_run(review_root, "cftbl-subway-awards", game)
	snapshots = [_diagnostic(run, "center subway 17"), _diagnostic(run, "left subway 16 again")]
	first = _moved(_step(run, "left subway 16"), "lamps")
	if 21 not in first or 53 in first:
		raise ValueError("the first left-subway closure must flash K (lamp 21) and leave the Cola lamp 53")
	center = _step(run, "center subway 17")
	if 53 not in _risen(center, "lamps") or {22, 23, 24} & _moved(center, "lamps"):
		raise ValueError("the center-subway closure must light the Cola target lamp 53 and leave K-I-S-S where it was")
	second = _moved(_step(run, "left subway 16 again"), "lamps")
	if 22 not in second:
		raise ValueError("the second left-subway closure must advance K-I-S-S to I (lamp 22)")
	for label in ("checkpoint: lower right popper", "checkpoint: lower right popper again"):
		if {item["number"] for item in _step(run, label).get("matched_outputs") or []} != {3}:
			raise ValueError(f"{label!r} must see the lower right popper (3) kick")
	named = [
		_observation("In a game, closing the left subway switch 16 flashes the K of K-I-S-S (lamp 21); a second closure advances to I (lamp 22) and shows the kissing-couple animation", [16]),
		_observation("In a game, closing the center subway switch 17 lights the first Snack Bar target lamp (53, Cola) and shows HIT TARGETS TO OPEN SNACKBAR", [17]),
		_observation("A ball delivered to the lower right popper switch 37 after either subway is kicked out by solenoid 3", [37], [3]),
	]
	observations = {
		"diagnostic_snapshots": snapshots,
		"named_action_observations": named,
		"solenoid_addresses_seen": _seen(run),
		"switch_to_lamp": {"16": 21, "17": 53},
	}
	command = _command(
		"cftbl-subway-awards",
		"A game is started from four coins and Start with the three trough switches closed; the host moves the served ball to the "
		"shooter lane and plunges it. The lamp transitions after each subway closure show the feature the ROM awards, which ties "
		"each switch number to its shot: the K-I-S-S (Taillight Park) hole and the Snack Bar hole.",
		game,
	)
	return _document(run, observations, command)


BUILDERS = {
	"creature-cftbl_l4-flasher-test.json": ("cftbl-flasher-test", build_flashers, GAME),
	"creature-cftbl_l4-switch-edges-fliptronic.json": ("cftbl-switch-edges-fliptronic", build_edges, GAME),
	"creature-cftbl_l4-flipper-coil-test.json": ("cftbl-flipper-coil-test", build_flippers, GAME),
	"creature-cftbl_l4-ramp-lights-test.json": ("cftbl-ramp-lights-test", build_chase, GAME),
	"creature-cftbl_l4-subway-awards.json": ("cftbl-subway-awards", build_subways, GAME),
	"creature-cftbl_p3-flasher-test.json": ("p3-cftbl-flasher-test", build_flashers, P3_GAME),
	"creature-cftbl_p3-switch-edges-fliptronic.json": ("p3-cftbl-switch-edges-fliptronic", build_edges, P3_GAME),
	"creature-cftbl_p3-flipper-coil-test.json": ("p3-cftbl-flipper-coil-test", build_flippers, P3_GAME),
	"creature-cftbl_p3-ramp-lights-test.json": ("p3-cftbl-ramp-lights-test", build_chase, P3_GAME),
}


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	pins = json.loads(FRAME_READINGS_PATH.read_bytes())["runs"]
	if set(pins) != {directory for directory, _, _ in BUILDERS.values()}:
		raise ValueError("the frame readings must cover exactly the documented runs")
	for filename, (directory, builder, game) in BUILDERS.items():
		document = builder(review_root, game)
		cited = {item["label"] for item in document["runtime"]["observations"]["diagnostic_snapshots"]}
		if cited != set(pins[directory]):
			raise ValueError(f"{directory}: the cited frames differ from the pinned readings: {sorted(set(pins[directory]) ^ cited)}")
		run_directory = review_root / HARNESS_DIRECTORY / directory
		run_sha = _sha256(run_directory / "run.json")
		manifest_sha = _sha256(run_directory / "manifest.json")
		document["runtime"]["raw_runs"][0]["sha256"] = run_sha
		document["source"]["sha256"] = run_sha
		document["source"]["attribution"] += f" Exact external directory manifest {directory}/manifest.json SHA-256 {manifest_sha}."
		documents[filename] = document
	return documents


def write(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		write_json(EVIDENCE_DIRECTORY / filename, document)


def check(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		path = EVIDENCE_DIRECTORY / filename
		if not path.is_file() or path.read_bytes() != canonical_bytes(document):
			raise ValueError(f"Creature compact runtime evidence drift: {path}")


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
	if args.write:
		write(root)
	else:
		check(root)
		print("Creature compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
