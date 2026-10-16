"""Derive the compact Corvette runtime evidence from the retained raw harness runs.

Each document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts
root), checks that it ran the committed scenario, the pinned binary and the expected mechanism mask, and writes the derived
observations beside the other WPC-Security runtime evidence. A diagnostic snapshot's ``interpreted_text`` is the curator's
visual reading of that snapshot's retained DMD frame, pinned by its pixel SHA-256; readings of one text must come from identical
frames. The tool refuses a raw run whose transitions no longer support a stated observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable

from pinmame_game_defs.jsonio import canonical_bytes, write_json
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.corvette.1994"
GAME = "corv_21"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "20e161d4e397650d436fc85ef01ce78bc144905444bd7e5fb4331f58edd5e211"
HARNESS_DIRECTORY = "corvette-1994/harness"
SCENARIO_DIRECTORY = "tools/harness-scenarios/wpc-security"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/wpc-security"
# Every diagnostic reading pinned to the frame the curator read: document -> label -> {pixel_sha256, reading}. A run whose
# frame or reading differs is refused until the new frame has been read again and the seed updated by hand.
FRAME_SEED_PATH = ROOT / "tools/seeds/bally/corvette-1994-frames.json"
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
IDENTIFICATION_LABEL = "Enter 1 (game identification)"
IDENTIFICATION = "CORVETTE / 50036 REV. 2.1"
COMMAND = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game corv_21 --rom-path <vpinmame-roms> "
	"--work-dir <new-isolated-state> --handle-mechanics {mech} --scenario {scenario} --dmd-dir <external-dmd-dir> --output <external-run.json>. "
)
# PinMAME's state channels change in every menu; observations about named coils ignore them.
BACKGROUND = frozenset({29, 30, 31})

# --- T.1 SWITCH EDGES sweep ----------------------------------------------------------------------------
# The name the ROM prints on the top display line while it reads the switch as active (read from the retained frames).
EDGE_NAMES = {
	11: "LEFT OUT LANE", 12: "RIGHT OUT LANE", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "PLUNGER", 16: "L. RETURN LANE",
	17: "R. RETURN LANE", 18: "SPINNER", 21: "SLAM TILT", 23: "BUY IN BUTTON", 24: "ALWAYS CLOSED", 25: "1ST GEAR (OPT)",
	26: "2ND GEAR (OPT)", 27: "3RD GEAR (OPT)", 28: "4TH GEAR (OPT)", 31: "TROUGH BALL 1", 32: "TROUGH BALL 2", 33: "TROUGH BALL 3",
	34: "TROUGH BALL 4", 35: "ROUTE 66 ENTRY", 36: "PIT STOP POPPER", 37: "TROUGH EJECT", 38: "INNER LOOP ENTRY",
	41: "ZR1 BOTTOM ENTRY", 42: "ZR1 TOP ENTRY", 43: "SKID PAD ENTRY", 44: "SKID PAD EXIT", 45: "ROUTE 66 EXIT",
	46: "L. STANDUP 3", 47: "L. STANDUP 2", 48: "L. STANDUP 1", 51: "L. RACE START", 52: "R. RACE START", 53: "NOT USED",
	54: "NOT USED", 55: "L. RACE ENCODER", 56: "R. RACE ENCODER", 57: "ROUTE 66 KICKOUT", 58: "SKID RTE66 EXIT",
	61: "L. SLINGSHOT", 62: "R. SLINGSHOT", 63: "LEFT JET", 64: "BOTTOM JET", 65: "RIGHT JET", 66: "L. ROLLOVER",
	67: "M. ROLLOVER", 68: "R. ROLLOVER", 71: "ZR1 FULL LEFT", 72: "ZR1 FULL RIGHT", 73: "NOT USED", 74: "NOT USED",
	75: "ZR1 EXIT", 76: "ZR1 LOCK BALL 1", 77: "ZR1 LOCK BALL 2", 78: "ZR1 LOCK BALL 3", 81: "MILLION STANDUP",
	82: "SKID PAD STANDUP", 83: "R. STANDUP", 84: "R. RUBBER", 85: "NOT USED", 86: "JET RUBBER", 87: "L. OUTER LOOP",
	88: "R. OUTER LOOP",
}
# The ROM names 24 on the 1 -> 0 edge instead: it rests at public 1 from power-up.
NAMED_AT_ZERO = frozenset({24})
EDGE_ROW_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
EDGE_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "BLK", 6: "BLU", 7: "VIO", 8: "GRY"}
# Fliptronic column: the position and wires the ROM shows after each host level, and the name while the host holds 1 (None: no name).
FLIPPER_EDGES = {
	111: ("F1", "BLK-GRN ORN", None), 112: ("F1", "BLK-GRN ORN", "R. FLIPPER E.O.S."), 113: ("F3", "BLK-BLU ORN", None),
	114: ("F3", "BLK-BLU ORN", "L. FLIPPER E.O.S."), 115: ("F3", "BLK-BLU ORN", None), 116: ("F1", "BLK-GRN ORN", "R. FLIPPER E.O.S."),
	117: ("F7", "BLK-GRY ORN", None), 118: ("F7", "BLK-GRY ORN", "U.L. FLIPPER E.O.S."),
}
SWEPT = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9) if column * 10 + row != 22) + tuple(range(111, 119))
# PinMAME rewrites the end-of-stroke bits of the flippers corvGameData declares with FLIP_SOL (lower pair and upper left).
SYNTHESIZED = frozenset({111, 113, 117})
FLIPPER_FIRES = {112: {45, 46}, 114: {47, 48}, 116: {45, 46}, 118: {35, 36}}
SWITCH_FIRES = {61: (9, "left slingshot"), 62: (10, "right slingshot"), 63: (11, "left jet bumper"), 64: (12, "bottom jet bumper"), 65: (13, "right jet bumper")}
# corvGameData inverted switches {0x00,0x00,0x00,0x7f,0x07,0x33,0x00,0x03,...} through wpc_sw2m.
PINMAME_MASKED = (31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 51, 52, 55, 56, 71, 72)


def _matrix_wires(address: int) -> str:
	column, row = divmod(address, 10)
	return f"WHT-{EDGE_ROW_WIRES[row]} GRN-{EDGE_COLUMN_WIRES[column]}"


def _edge_reading(address: int, level: int) -> str:
	idle = "SWITCH EDGES"
	if address in FLIPPER_EDGES:
		position, wires, name = FLIPPER_EDGES[address]
		return f"{name if level and name else idle} / T.1 LAST SW {position} / {wires}"
	if address == 24:
		if level == 0:
			return f"{EDGE_NAMES[24]} / T.1 LAST SW 24 / {_matrix_wires(24)}"
		return f"{idle} / T.1 LAST SW F7 / BLK-GRY ORN"
	return f"{EDGE_NAMES[address] if level else idle} / T.1 LAST SW {address} / {_matrix_wires(address)}"


# --- T.4 SOLENOID TEST, T.5 FLASHER TEST, T.12 FLIPPER COIL TEST, T.6 GI, T.8 LAMPS ----------------------
T4_ORDER = (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 33, 34)
T4_NAMES = {
	1: ("TROUGH EJECT", "VIO-BRN RED-BRN"), 2: ("ZR1 LOW REV GATE", "VIO-RED RED-BRN"), 3: ("KICKBACK", "VIO-ORN RED-BRN"),
	4: ("PIT STOP POPPER", "VIO-YEL RED-BRN"), 5: ("ZR1 UP REV GATE", "VIO-GRN RED-BRN"), 7: ("KNOCKER", "VIO-BLK RED-BRN"),
	8: ("ROUTE 66 KICKOUT", "VIO-GRY RED-BRN"), 9: ("L. SLINGSHOT", "BRN-BLK RED-BLK"), 10: ("R. SLINGSHOT", "BRN-RED RED-BLK"),
	11: ("LEFT JET", "BRN-ORN RED-BLK"), 12: ("BOTTOM JET", "BRN-YEL RED-BLK"), 13: ("RIGHT JET", "BRN-GRN RED-BLK"),
	14: ("NOT USED", "BRN-BLU RED-BLK"), 15: ("ZR1 LOCKUP", "BRN-VIO RED-BLK"), 16: ("LOOP GATE", "BRN-GRY RED-BLK"),
	17: ("RACE DIRECTION", "BLK-BRN RED-WHT"), 18: ("L. RACE ENABLE", "BLK-RED RED-WHT"), 19: ("R. RACE ENABLE", "BLK-ORN RED-WHT"),
	33: ("DIVERTER POWER", "YEL-VIO RED-VIO"), 34: ("DIVERTER HOLD", "ORN-VIO RED-VIO"),
}
T5_ORDER = (20, 21, 22, 23, 24, 25, 26, 27, 28)
T5_NAMES = {
	20: ("TENTH CORVETTE", "BLK-YEL RED-WHT"), 21: ("JETS", "BLU-GRN RED-WHT"), 22: ("R. RAMPS", "BLU-BLK RED-WHT"),
	23: ("U. L. FLIPPER", "BLU-VIO RED-WHT"), 24: ("CATCH ME", "BLU-GRY RED-WHT"), 25: ("ZR1 RAMP", "BLU-BRN RED-WHT"),
	26: ("ZR1 UNDERSIDE", "BLU-RED RED-WHT"), 27: ("R. REAR PANEL", "BLU-ORN RED-WHT"), 28: ("R. STANDUP", "BLU-YEL RED-WHT"),
}
# The frame read for each T.5 item: the first item's first frame, every later item's second (the name blinks).
T5_FRAME = {1: 0}
T12_ORDER = (
	(1, "R. FLIP. POWER", "YEL-GRN RED-GRN", {45, 46}), (2, "R. FLIP. HOLD", "ORN-GRN RED-GRN", {46}),
	(3, "L. FLIP. POWER", "YEL-BLU RED-BLU", {47, 48}), (4, "L. FLIP. HOLD", "ORN-BLU RED-BLU", {48}),
	(7, "U.L. FLIP. POWER", "YEL-GRY RED-GRY", {35, 36}), (8, "U.L. FLIP. HOLD", "ORN-GRY RED-GRY", {36}),
)
# The snapshot read for each T.12 item (the item number the ROM shows, then its label in the run).
T12_LABELS = {1: "T.12 after Up 6", 2: "T.12 after Up 1", 3: "T.12 after Up 2", 4: "T.12 after Up 3", 7: "T.12 after Up 4", 8: "T.12 after Up 5"}
# T.6: (public GI string, snapshot read, ROM text, the Up presses whose transitions dim that string alone).
GI_STRINGS = (
	(0, "T.6 Up 9 (held)", "UPPER LEFT / T.6 BRIGHT=2 STOP / WHT-BRN BRN", range(9, 15)),
	(1, "T.6 Up 16 (held)", "UPPER RIGHT / T.6 BRIGHT=1 STOP / WHT-ORN ORN", range(17, 23)),
	(2, "T.6 Up 25 (held)", "LOWER LEFT / T.6 BRIGHT=2 STOP / WHT-YEL YEL", range(25, 32)),
	(3, "T.6 Up 32 (held)", "LOWER RIGHT / T.6 BRIGHT=1 STOP / WHT-GRN GRN", range(33, 39)),
	(4, "T.6 Up 41 (held)", "BACK BOX TITLE / T.6 BRIGHT=2 STOP / WHT-VIO VIO", range(41, 47)),
)
LAMP_ROW_WIRES = {1: "BRN", 2: "BLK", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMP_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "BLK", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
MATRIX_LAMPS = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))
# T.8 SINGLE LAMPS names, read from the retained frames taken while each Up press was held.
LAMP_NAMES = {
	11: "L. ROLLOVER", 12: "M. ROLLOVER", 13: "R. ROLLOVER", 14: "SKID PAD ARROW", 15: "STICKY TIRES", 16: "SKID PAD JACKPOT",
	17: "ROUTE 66 ARROW", 18: "RACE TODAY", 21: "INNER LOOP ARROW", 22: "FUELIE", 23: "NITROUS", 24: "IN. LOOP JACKPOT",
	25: "R. O. LOOP ARROW", 26: "Z07 SUSPENSION", 27: "BIG BRAKES", 28: "SUPER CHARGER", 31: "L. O. LOOP ARROW", 32: "LITE LOCK",
	33: "QUALIFY", 34: "BIG BLOCK", 35: "ZR1 RAMP LOCK", 36: "6 SPEED TRANS", 37: "HI LIFT CAMS", 38: "ZR1 RAMP ARROW",
	41: "CORVETTE 6", 42: "CORVETTE 3", 43: "CORVETTE 1", 44: "CORVETTE 2", 45: "CORVETTE 4", 46: "L. STANDUP 3",
	47: "L. STANDUP 2", 48: "L. STANDUP 1", 51: "CORVETTE 9", 52: "CORVETTE 8", 53: "PIT STOP", 54: "CORVETTE 7",
	55: "CORVETTE 5", 56: "PIT STOP ARROW", 57: "SPINNER ARROW", 58: "DRIVE AGAIN", 61: "L. OUTER TAIL", 62: "L. INNER TAIL",
	63: "CATCH ME", 64: "R. INNER TAIL", 65: "R. OUTER TAIL", 66: "R. STANDUP ARROW", 67: "LITE KICKBACK", 68: "START CHALLENGE",
	71: "KICKBACK ARROW", 72: "L. RETURN LANE", 73: "R. RETURN LANE", 74: "R. OUT LANE", 75: "MILLION STANDUP", 76: "SIDE PIPE 1",
	77: "SIDE PIPE 2", 78: "SIDE PIPE 3", 81: "R. TREE RED", 82: "L. TREE RED", 83: "TREE BOT. YELLOW", 84: "TREE TOP YELLOW",
	85: "R. TREE GREEN", 86: "L. TREE GREEN", 87: "BUY IN", 88: "START BUTTON",
}

# --- T.16 ZR1-LT5 TEST and T.18 ZR-1 ADJUST -------------------------------------------------------------
ENGINE_READINGS = {
	"Enter (start T.16, SELF TEST)": "ZR1-LT5 TEST / POSITION 230 / LEFT --- [ ] [x] --- RIGHT / SELF TEST",
	"SELF TEST 4": "ZR1-LT5 TEST / POSITION 80 / LEFT --- [ ] [ ] --- RIGHT / SELF TEST",
	"SELF TEST 5": "ZR1-LT5 TEST / POSITION 72 / LEFT 63 [ ] [ ] --- RIGHT / SELF TEST",
	"SELF TEST 10": "ZR1-LT5 TEST / POSITION 141 / LEFT 63 [ ] [ ] 192 RIGHT / SELF TEST",
	"SELF TEST 11": "ZR1-LT5 TEST / POSITION 127 / LEFT 63 [ ] [ ] 192 RIGHT / SELF TEST (finished)",
	"ENGINE CENTER 3": "ZR1-LT5 TEST / POSITION 63 / LEFT 63 [x] [ ] 192 RIGHT / ENGINE LEFT",
}
ENGINE_FAILED_READINGS = {
	"Enter (start T.16, SELF TEST)": "ZR1-LT5 TEST / POSITION 0 / LEFT --- [ ] [ ] --- RIGHT / SELF TEST",
	"SELF TEST 6": "ZR1-LT5 TEST / POSITION OFF / LEFT --- [ ] [ ] --- RIGHT / FAILED",
}
ZR1_ADJUST_READINGS = {"Enter (start T.18)": "ZR 1 ADJUST / TURN ADJUSTMENT / TO CENTER ENGINE / (SEE ADJ. PROCEDURE)"}

# --- T.17 RACE TEST -------------------------------------------------------------------------------------
RACE_READINGS = {
	"SELF TEST 5": "RACE TEST / LEFT: START [ ] POS [x] 115 / RIGHT: START [x] POS [ ] 1 / SELF TEST",
	"SELF TEST 9": "RACE TEST / LEFT: START [ ] POS [ ] 670 / RIGHT: START [ ] POS [x] 33 / SELF TEST",
	"SELF TEST 13": "RACE TEST / LEFT: START [ ] POS [ ] 670 / RIGHT: START [ ] POS [x] 638 / SELF TEST",
	"SELF TEST 18": "RACE TEST / LEFT: START [x] POS [ ] 0 / RIGHT: START [x] POS [ ] 0 / SELF TEST (finished)",
	"Enter held (LEFT FORWARD)": "RACE TEST / LEFT: START [ ] POS [x] 259 / RIGHT: START [x] POS [ ] 1 / LEFT FORWARD",
	"LEFT FORWARD 2": "RACE TEST / LEFT: START [ ] POS [ ] 389 / RIGHT: START [x] POS [ ] 1 / LEFT FORWARD",
}


# --- Shared helpers ------------------------------------------------------------------------------------
def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(directory: Path, scenario: str, mechanics: int) -> dict[str, Any]:
	run_path = directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / SCENARIO_DIRECTORY / f"{scenario}.json"
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful Corvette {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != mechanics:
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


def _risen(step: dict[str, Any], channel: str = "solenoids") -> set[int]:
	"""Addresses whose recorded transitions during the step include an active state."""
	return {item["number"] for item in step["transitions"][channel] if any(item["states"])}


def _states(step: dict[str, Any], channel: str, number: int) -> list[int]:
	for item in step["transitions"][channel]:
		if item["number"] == number:
			return list(item["states"])
	return []


def _named_coils(step: dict[str, Any]) -> set[int]:
	return _risen(step) - BACKGROUND


def _changed(step: dict[str, Any], channel: str) -> set[int]:
	return {item["number"] for item in step["transitions"][channel]}


def _diagnostics(run: dict[str, Any], readings: dict[str, str], grid_marked: frozenset[str] = frozenset()) -> list[dict[str, Any]]:
	"""Pin each reading to its frame; one interpreted text must always come from one frame.

	``grid_marked`` names T.1 frames taken while a switch is held: the switch grid on the left of the display marks that raw cell,
	so frames whose text agrees may still differ there, and they are exempt from the one-text-one-frame rule.
	"""
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
		if label not in grid_marked and by_text.setdefault(text, pixel) != pixel:
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


def _seen(run: dict[str, Any]) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]})


def _observation(label: str, inputs: list[int], solenoids: set[int] | list[int]) -> dict[str, Any]:
	return {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": inputs, "input_address": inputs[0], "input_kind": "switch",
		"label": label, "observed_switch_addresses": [], "result": "observed",
		"transitioned_solenoid_addresses": sorted(solenoids),
	}


def _document(name: str, directory: str, scenario: str, mechanics: int, run: dict[str, Any], observations: dict[str, Any], command: str) -> dict[str, Any]:
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/corvette_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": COMMAND.format(mech=mechanics, scenario=f"{SCENARIO_DIRECTORY}/{scenario}.json") + command,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": GAME,
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": name,
					"nvram_initialization": NVRAM_NOTE,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}/run.json",
					"scenario_path": f"{SCENARIO_DIRECTORY}/{scenario}.json",
					"scenario_sha256": run["scenario"]["sha256"],
					"self_test_pulses": 0,
					"snapshot_count": len(run["snapshots"]),
					"watch_switches": run["watch_switches"],
				}
			],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
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


def _base(run: dict[str, Any]) -> dict[str, str]:
	return {IDENTIFICATION_LABEL: IDENTIFICATION}


# --- Builders ------------------------------------------------------------------------------------------
def build_edges(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for address in SWEPT:
		for level in (1, 0):
			readings[f"{address} -> {level}"] = _edge_reading(address, level)
		held = {item["number"]: item["state"] for item in _snapshot(run, f"{address} -> 1")["watched_switches"]}
		if held[address] != (0 if address in SYNTHESIZED else 1):
			raise ValueError(f"unexpected observed level of {address} after the host wrote 1")
		risen = _named_coils(_step(run, f"{address} -> 1"))
		expected = FLIPPER_FIRES.get(address) or ({SWITCH_FIRES[address][0]} if address in SWITCH_FIRES else set())
		if risen != expected:
			raise ValueError(f"T.1 at public {address} published {sorted(risen)}, expected {sorted(expected)}")
		if address in FLIPPER_FIRES:
			position, _, name = FLIPPER_EDGES[address]
			named.append(_observation(
				f"T.1 with host public {address} set to 1: the ROM fires public {', '.join(map(str, sorted(risen)))} and names "
				f"{name!r} ({position}); the windings drop at 0", [address], risen))
		elif address in SWITCH_FIRES:
			named.append(_observation(
				f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and the ROM fires the {SWITCH_FIRES[address][1]} coil, "
				f"public {SWITCH_FIRES[address][0]}, on the closure", [address], risen))
		elif address in NAMED_AT_ZERO or address in FLIPPER_EDGES:
			continue
		elif EDGE_NAMES[address] == "NOT USED":
			named.append(_observation(f"T.1 shows 'NOT USED' while host public {address} is 1 and clears it at 0: the ROM scans the position without a device", [address], set()))
		else:
			named.append(_observation(f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and clears it at 0", [address], set()))
	named.append(_observation("Public 24 rests at 1 from power-up; T.1 shows no new name for the redundant 1 and names 'ALWAYS CLOSED' on the 1 -> 0 edge", [24], set()))
	named.append(_observation("Public 111, 113 and 117: a host write of 1 reads back 0, because PinMAME rewrites the end-of-stroke bits of the FLIP_SOL flippers from their coil state on every update, and T.1 names nothing", [111, 113, 117], set()))
	named.append(_observation("Public 115 (F5) round-trips at 1 and T.1 names nothing for it; its last-switch line stays at F3", [115], set()))
	observations = {
		"diagnostic_snapshots": _diagnostics(run, readings, frozenset(f"{address} -> 1" for address in SWEPT)),
		"named_action_observations": named,
		"solenoid_addresses_seen": _seen(run),
	}
	command = (
		"Built-in mechanisms stay disabled. Each set_switch holds one public level for 1.5 s; the snapshot after it records the ROM's T.1 "
		"display and the watched public switch levels. The ROM names a switch on its top line on the edge it treats as active. PinMAME's "
		f"corvGameData mask inverts public {', '.join(map(str, PINMAME_MASKED))}; every one of them is named at public 1."
	)
	return observations, command


def build_solenoids(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for index, address in enumerate(T4_ORDER, start=1):
		name, wires = T4_NAMES[address]
		label = "Enter (start T.4)" if index == 1 else f"T.4 after Up {index - 1}"
		readings[label] = f"{name} / T.4 {address:02d} REPEAT / {wires}"
		if index == 1:
			selected = _named_coils(_step(run, "Enter (start T.4)"))
			late: set[int] = set()
		else:
			selected = _named_coils(_step(run, f"T.4 Up {index - 1}")) | _named_coils(_step(run, f"T.4 after Up {index - 1}"))
			late = _named_coils(_step(run, f"T.4 Up {index}"))
		previous = T4_ORDER[index - 2] if index > 1 else None
		if not selected <= {address, previous} or address not in selected | late:
			raise ValueError(f"T.4 item {index} ({address}) published {sorted(selected)} then {sorted(late)}")
		named.append(_observation(f"T.4 SOLENOID TEST item {index} selects {address:02d} ({name}, {wires}): the ROM pulses public {address} repeatedly", [8 if index == 1 else 7], {address}))
	if 1 not in _named_coils(_step(run, f"T.4 Up {len(T4_ORDER)}")):
		raise ValueError("T.4 must wrap to solenoid 1 after 34")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"Each Up press selects the next T.4 item; in repeat mode the ROM pulses it until the next press. The test walks 1-5, 7-19, 33 "
		"and 34 (skipping 6, offering 14 as NOT USED) and wraps to 1. A frame is taken while each press is held and 0.7 s after its "
		"settle; the later one is read."
	)
	return observations, command


def build_flashers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for index, address in enumerate(T5_ORDER, start=1):
		name, wires = T5_NAMES[address]
		readings[f"T.5 item {index} frame {T5_FRAME.get(index, 1)}"] = f"{name} / T.5 {address} REPEAT / {wires}"
		labels = ["Enter (start T.5)"] if index == 1 else [f"T.5 Up {index - 1}"]
		labels += [f"T.5 item {index} frame {frame}" for frame in range(6)]
		risen = set().union(*(_named_coils(_step(run, label)) for label in labels))
		previous = T5_ORDER[index - 2] if index > 1 else None
		if address not in risen or not risen <= {address, previous}:
			raise ValueError(f"T.5 item {index} published {sorted(risen)}, not {address}")
		named.append(_observation(f"T.5 FLASHER TEST item {index} selects {address} ({name}, {wires}): the ROM pulses it repeatedly", [8 if index == 1 else 7], {address}))
	wrap = set().union(*(_named_coils(_step(run, label)) for label in ["T.5 Up 9"] + [f"T.5 item 10 frame {frame}" for frame in range(6)]))
	if 20 not in wrap:
		raise ValueError("T.5 must wrap to 20 after 28")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each Up press selects the next flasher; six frames 0.25 s apart catch the blinking name lit. The test walks 20-28 and wraps to 20."


def build_flippers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for position, (number, name, wires, published) in enumerate(T12_ORDER, start=1):
		readings[T12_LABELS[number]] = f"{name} / T.12 {number:02d} REPEAT / {wires}"
		labels = ["Enter (start T.12)"] if position == 1 else [f"T.12 Up {position - 1}", f"T.12 after Up {position - 1}"]
		risen = set().union(*(_named_coils(_step(run, label)) for label in labels))
		if risen != published:
			raise ValueError(f"T.12 item {number} published {sorted(risen)}, not {sorted(published)}")
		named.append(_observation(f"T.12 FLIPPER COIL TEST item {number:02d} {name} ({wires}) drives public {', '.join(map(str, sorted(published)))}", [8 if position == 1 else 7], risen))
	if _named_coils(_step(run, "T.12 Up 6")) != {45, 46}:
		raise ValueError("T.12 must wrap to the right flipper power item")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The test walks items 01-04 and 07-08 (power drives both windings, hold the hold winding) and wraps; it offers no item 05 or 06 and no item for 33 and 34."


def build_gi(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	readings["T.6 Up 1 (held)"] = "ALL ILLUMINATION / T.6 BRIGHT=2 STOP"
	named = []
	for press in range(1, 7):
		if _changed(_step(run, f"T.6 Up {press}"), "gis") != {0, 1, 2, 3, 4}:
			raise ValueError("T.6 ALL ILLUMINATION must dim public GI 0-4 together")
	named.append(_observation("T.6 ALL ILLUMINATION steps the brightness of public GI 0, 1, 2, 3 and 4 together", [8], set()))
	for channel, label, text, presses in GI_STRINGS:
		readings[label] = text
		changed = [_changed(_step(run, f"T.6 Up {press}"), "gis") for press in presses]
		if any(item != {channel} for item in changed):
			raise ValueError(f"T.6 {text} must dim public GI {channel} alone, saw {changed}")
		named.append(_observation(f"T.6 {text.split(' / ')[0]} ({text.split(' / ')[-1]}): Up steps the brightness of public GI {channel} alone", [7], set()))
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "T.6 stop mode first steps all illumination through eight brightness levels, then each string in turn; every string dims."


def _lamp_reading(step: int, address: int) -> str:
	column, row = divmod(address, 10)
	return f"{LAMP_NAMES[address]} / T.8 {step:02d} LAMP {address} / RED-{LAMP_ROW_WIRES[row]} YEL-{LAMP_COLUMN_WIRES[column]}"


def build_lamps(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	for step, address in enumerate(MATRIX_LAMPS, start=1):
		label = "T.8 Up 64 (held)" if step == 1 else f"T.8 Up {step - 1} (held)"
		readings[label] = _lamp_reading(step, address)
		step_label = "Enter (start T.8)" if step == 1 else f"T.8 Up {step - 1}"
		previous = MATRIX_LAMPS[step - 2] if step > 1 else None
		window = _step(run, step_label)
		risen = _risen(window, "lamps")
		if address not in risen or not risen <= {address, previous}:
			raise ValueError(f"T.8 step {step} must light public lamp {address} and no lamp but the one it leaves, saw {sorted(risen)}")
		if previous is not None and (_states(window, "lamps", previous) or [0])[-1] != 0:
			raise ValueError(f"T.8 step {step} must leave lamp {previous} off")
		if not set(_snapshot(run, label)["active_lamps"]) <= {address}:
			raise ValueError(f"T.8 step {step} shows lamps other than {address} lit")
	if 11 not in _risen(_step(run, "T.8 Up 64"), "lamps"):
		raise ValueError("T.8 must wrap to lamp 11 after 88")
	named = [_observation("T.8 SINGLE LAMPS TEST lights public lamps 11-88 one at a time in matrix order while printing each name, its number and its row and column wires, and wraps to lamp 11", [7], set())]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each Up press, held 0.4 s, selects the next lamp; the frame taken while it is held is read (lamp 11 from the wrap-around press)."


def build_engine(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), **ENGINE_READINGS}
	if _named_coils(_step(run, "Enter (start T.16, SELF TEST)")) != {51}:
		raise ValueError("T.16 must raise public 51 as it starts the self test")
	moving = set().union(*(_changed(_step(run, f"SELF TEST {index}"), "solenoids") for index in range(2, 11)))
	if moving != {52, 53}:
		raise ValueError(f"the self-test sweep must toggle public 52 and 53 only, saw {sorted(moving)}")
	if set().union(*(_changed(_step(run, f"SELF TEST {index}"), "solenoids") for index in (11, 12))):
		raise ValueError("the finished self test must leave the engine outputs still")
	if not any(51 in snapshot["active_solenoids"] for snapshot in run["snapshots"] if snapshot["label"] == "ENGINE CENTER 3"):
		raise ValueError("public 51 must stay on through the engine tests")
	named = [
		_observation("Entering T.16 ZR1-LT5 TEST raises public 51 and keeps it on; the SELF TEST then sweeps the engine-position register, first downwards until the FULL LEFT opto (71) closes and the display records the left edge 63, then upwards until FULL RIGHT (72) closes at 192, and parks it at 127, toggling public 52 and 53 while the engine moves", [8], {51, 52, 53}),
		_observation("ENGINE LEFT drives the position down to 63, where the display marks FULL LEFT closed, toggling 52 and 53 on the way", [8], {52, 53}),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"PinMAME's built-in engine model (mechanism bit 2) closes 71 below register value 64 and 72 above 191. Up while AUTO RUN is "
		"running does not select the next sub-test, so ENGINE LEFT runs at the scenario's last selection (the steps labelled ENGINE CENTER); "
		"Escape would leave the test."
	)
	return observations, command


def build_engine_failed(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), **ENGINE_FAILED_READINGS}
	if not {51, 52, 53} <= _named_coils(_step(run, "Enter (start T.16, SELF TEST)")):
		raise ValueError("T.16 without an engine model must still raise 51, 52 and 53")
	dropped = _states(_step(run, "SELF TEST 6"), "solenoids", 51)
	if not dropped or any(dropped) or not any(51 in snapshot["active_solenoids"] for snapshot in run["snapshots"] if snapshot["label"] == "SELF TEST 5"):
		raise ValueError("the failed self test must drop public 51 from on to off")
	if any(51 in snapshot["active_solenoids"] for snapshot in run["snapshots"] if snapshot["label"] == "SELF TEST 6"):
		raise ValueError("public 51 must stay off after the self test fails")
	named = [
		_observation("With nothing answering FULL LEFT (71) or FULL RIGHT (72), the T.16 SELF TEST drives the engine outputs for about 13 s, then drops public 51, shows POSITION OFF and FAILED", [8], {51, 52, 53}),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Built-in mechanisms stay disabled, so the engine optos never close."


def build_zr1_adjust(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), **ZR1_ADJUST_READINGS}
	step = _step(run, "Enter (start T.18)")
	if _changed(step, "solenoids") - BACKGROUND != {51} or _named_coils(step) != {51}:
		raise ValueError("T.18 must raise public 51 alone")
	named = [_observation("T.18 ZR-1 ADJUST raises public 51 alone and holds the engine at its centre for the potentiometer adjustment", [8], {51})]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The test only enables the engine and waits."


def build_race(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), **RACE_READINGS}
	self_test = set().union(*(_changed(_step(run, label), "solenoids") for label in ["Enter (start T.17, SELF TEST)"] + [f"SELF TEST {index}" for index in range(1, 25)]))
	if self_test - BACKGROUND != {17, 18, 19}:
		raise ValueError(f"the race self test must drive 17, 18 and 19 only, saw {sorted(self_test)}")
	forward = _named_coils(_step(run, "Enter held (LEFT FORWARD)"))
	if forward != {17, 18}:
		raise ValueError(f"LEFT FORWARD must drive 17 and 18, saw {sorted(forward)}")
	named = [
		_observation("T.17 RACE TEST SELF TEST drives the left car forward with the race direction (17) and left race enable (18) on, counting its encoder (55) to 670 while its start opto (51) opens, then the right car with 17 and 19 to 638, then returns both to their start optos at count 0", [8], {17, 18, 19}),
		_observation("Holding Enter on LEFT FORWARD raises 17 and 18 together and the left car's count climbs (259, then 389 where it stops on release); the right car stays at its start", [8], forward),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"PinMAME's built-in race-car models (mechanism bits 0 and 1) hold each car's start switch (51, 52) at home and pulse its encoder "
		"(55, 56) while its enable (18, 19) is on, moving forward while 17 is on; the ROM's self test accepts that pairing. The models' "
		"writes are emulator outputs, not host stimuli."
	)
	return observations, command


Builder = Callable[[dict[str, Any]], tuple[dict[str, Any], str]]
RUNS: dict[str, tuple[str, str, int, Builder]] = {
	"corvette-corv_21-switch-edges.json": ("cv-switch-edges", "cv-switch-edges", 0, build_edges),
	"corvette-corv_21-solenoid-test.json": ("cv-solenoid-test", "cv-solenoid-test", 7, build_solenoids),
	"corvette-corv_21-flasher-test.json": ("cv-flasher-test", "cv-flasher-test", 7, build_flashers),
	"corvette-corv_21-flipper-coil-test.json": ("cv-flipper-coil-test", "cv-flipper-coil-test", 7, build_flippers),
	"corvette-corv_21-gi-test.json": ("cv-gi-test", "cv-gi-test", 7, build_gi),
	"corvette-corv_21-single-lamps.json": ("cv-single-lamps", "cv-single-lamps", 7, build_lamps),
	"corvette-corv_21-engine-test.json": ("cv-engine-test", "cv-engine-test", 7, build_engine),
	"corvette-corv_21-engine-test-no-mech.json": ("cv-engine-test-no-mech", "cv-engine-test", 0, build_engine_failed),
	"corvette-corv_21-zr1-adjust.json": ("cv-zr1-adjust", "cv-zr1-adjust", 7, build_zr1_adjust),
	"corvette-corv_21-race-test.json": ("cv-race-test", "cv-race-test", 7, build_race),
}


def _check_pinned_frames(filename: str, observations: dict[str, Any]) -> None:
	pinned = json.loads(FRAME_SEED_PATH.read_bytes())[filename]
	read = {item["label"]: {"pixel_sha256": item["pixel_sha256"], "reading": item["interpreted_text"]} for item in observations["diagnostic_snapshots"]}
	if read != pinned:
		changed = sorted(label for label in set(read) | set(pinned) if read.get(label) != pinned.get(label))
		raise ValueError(f"{filename}: readings or frames differ from the pinned seed at {changed[:5]}")


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	for filename, (directory, scenario, mechanics, builder) in RUNS.items():
		path = review_root / HARNESS_DIRECTORY / directory
		check_manifest(path, GAME)
		run = _load_run(path, scenario, mechanics)
		observations, command = builder(run)
		_check_pinned_frames(filename, observations)
		document = _document(filename.removeprefix("corvette-").removesuffix(".json"), directory, scenario, mechanics, run, observations, command)
		run_sha = _sha256(path / "run.json")
		manifest_sha = _sha256(path / "manifest.json")
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
			raise ValueError(f"Corvette compact runtime evidence drift: {path}")


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
		print("Corvette compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
