"""Derive the compact Doctor Who runtime evidence from the retained raw harness runs.

Each document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts root),
checks that it ran the committed scenario and the pinned binary and ROM, and writes the derived observations beside the other
runtime evidence. A diagnostic snapshot's ``interpreted_text`` is the curator's visual reading of that snapshot's retained DMD
frame; its ``pixel_sha256`` pins the frame. The tool refuses a raw run whose transitions no longer support a stated observation.
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
MACHINE_ID = "bally.doctor-who.1992"
GAME = "dw_l2"
REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
ROM_ARCHIVE_SHA256 = "9e0a1e1257ca595f06f1367d7f96773ceb12d20be43061a9630216a8f0c5a162"
HARNESS_DIRECTORY = "doctor-who-1992/harness"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/wpc-fliptronic"
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are "
	"host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation "
	"is counted pulses; every diagnostic snapshot's interpreted_text is the curator's visual reading of its retained DMD frame, "
	"identified by its pixel SHA-256. The exact external directory manifest (built by tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)

ROW_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "BLK", 6: "BLU", 7: "VIO", 8: "GRY"}


def _wires(address: int) -> str:
	column, row = divmod(address, 10)
	return f"WHT-{ROW_WIRES[row]} GRN-{COLUMN_WIRES[column]}"


# --- T.1 SWITCH EDGES ----------------------------------------------------------------------------------
# The name the ROM prints on the top line while it reads the switch as active (read from the retained frames).
EDGE_NAMES = {
	41: "<E>S-C-A-P-E", 78: "Mini. Lites Lock", 57: "Trap Door. Down", 47: "Hangon Score", 82: "Playfield Glass",
	68: "Mini. Door. Left", 88: "Mini. Door. Right", 38: "Mini. Door. Mid", 31: "Opto Popper", 32: "Mini. Home Opto",
	33: "Enter T.Ramp Opto", 71: "Mini.Opto.5Bank R1", 72: "Mini.Opto.5Bank R2", 73: "Mini.Opto.5Bank M",
	74: "Mini.Opto.5Bank L2", 75: "Mini.Opto.5Bank L1", 76: "Mini. L. OptoEject", 77: "Mini. R. OptoEject",
}
EDGE_SWITCHES = (41, 78, 57, 47, 82, 68, 88, 38, 112, 114, 31, 32, 33, 71, 72, 73, 74, 75, 76, 77)
OPTO_SWITCHES = (31, 32, 33, 71, 72, 73, 74, 75, 76, 77)
# The ROM's active level for each ordinary or opto switch: 1 for every one except 32.
ROM_ACTIVE_LEVEL = {address: (0 if address == 32 else 1) for address in EDGE_SWITCHES if address not in (112, 114)}
FLIPPER_EDGES = {112: ("R FLIPPER EOS", "F1", "BLK-GRN BLK"), 114: ("L FLIPPER EOS", "F3", "BLK-BLU BLK")}
IDENTIFICATION = "Dr. Who / 20006 REV. L-2"


def _edge_reading(label: str) -> str | None:
	"""Visual reading of the T.1 frame for one snapshot label, or None when the frame is not retained as evidence."""
	if label == "T.1 started, every watched switch at public 0":
		return "SWITCH EDGES / T.1"
	if label == "Enter 2 (game identification)":
		return IDENTIFICATION
	parts = label.split(" -> ")
	if len(parts) != 2:
		return None
	address = int(parts[0])
	level = int(parts[1][0])
	if address in FLIPPER_EDGES:
		name, last, wires = FLIPPER_EDGES[address]
		return f"{name} / T.1 LAST SW {last} / {wires}" if level else f"SWITCH EDGES / T.1 LAST SW {last} / {wires}"
	if label == "32 -> 1":
		# 31 is still held at 1 here: the ROM sees 32 leave its initial active state without naming a new switch.
		return f"{EDGE_NAMES[31]} / T.1 LAST SW 31 / {_wires(31)}"
	named = level == ROM_ACTIVE_LEVEL[address]
	text = f"{EDGE_NAMES[address]} / T.1 LAST SW {address} / {_wires(address)}" if named else f"SWITCH EDGES / T.1 LAST SW {address} / {_wires(address)}"
	return text


# --- T.4 SOLENOID TEST ---------------------------------------------------------------------------------
T4_ORDER = (1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 13, 15, 16, 25)
T4_NAMES = {
	1: "Trap Door", 2: "Shooter", 3: "Opto Popper", 4: "Mini. L. Opto.Eject", 5: "Mini. R. Opto.Eject", 7: "Knocker",
	9: "Left Sling", 10: "Right Sling", 11: "Left Jet", 12: "Right Jet", 13: "Bottom Jet", 15: "Outhole", 16: "Trough", 25: "Unused",
}
T4_WIRES = {
	1: "VIO-BRN VIO-YEL", 2: "VIO-RED VIO-YEL", 3: "VIO-ORN VIO-YEL", 4: "VIO-YEL VIO-YEL", 5: "VIO-GRN VIO-YEL", 7: "VIO-BLK VIO-YEL",
	9: "BRN-BLK VIO-ORN", 10: "BRN-RED VIO-ORN", 11: "BRN-ORN VIO-ORN", 12: "BRN-YEL VIO-ORN", 13: "BRN-GRN VIO-ORN",
	15: "BRN-VIO VIO-ORN", 16: "BRN-GRY VIO-ORN", 25: "BLU-BRN VIO-GRN",
}


def _t4_label(address: int) -> str:
	step = T4_ORDER.index(address)
	return "T.4 step 0, frame 1" if step == 0 else f"T.4 step {step}"


def _t4_reading(label: str) -> str | None:
	if label == "Enter 2 (game identification)":
		return IDENTIFICATION
	for address in T4_ORDER:
		if label == _t4_label(address):
			return f"{T4_NAMES[address]} / T.4 {address:02d} REPEAT / {T4_WIRES[address]}"
	return None


# --- T.14 MINI-PLAYFIELD TEST --------------------------------------------------------------------------
MINI_READINGS = {
	"Enter 2 (game identification)": IDENTIFICATION,
	"T.14 sub-test 1, frame 1": "CW MidL / T.14 RUNNING / MINIPLYFLD.FAULTS 00 / PRESS BOTH FLIPPERS",
	"T.14 sub-test 1 with both flipper buttons held, second 1": "CW MidL / T.14 RUNNING / MINIPLYFLD.FAULTS 01 / ERROR",
	"T.14 sub-test 1 with both flipper buttons held, second 4": "CCW Down / T.14 RUNNING / MINIPLYFLD.FAULTS 01 / MOVING",
	"112 -> 0": None,
	"T.14 sub-test 2, frame 1": "L Kicker / T.14 RUNNING / MINIPLYFLD.FAULTS 01 / KICKING",
	"T.14 sub-test 2 with both flipper buttons held, second 1": "R Kicker / T.14 RUNNING / MINIPLYFLD.FAULTS 01 / KICKING",
	"T.14 sub-test 3, frame 1": "Flasher / T.14 RUNNING / MINIPLYFLD.FAULTS 01",
	"T.14 sub-test 3 with both flipper buttons held, second 1": "CCW MidR / T.14 RUNNING / MINIPLYFLD.FAULTS 01 / MOVING",
	"T.14 sub-test 4 with both flipper buttons held, second 2": "CCW Up / T.14 STOPPED / MINIPLYFLD.FAULTS 02 / ERROR",
}
MINI_READINGS = {label: text for label, text in MINI_READINGS.items() if text is not None}


# --- Shared helpers ------------------------------------------------------------------------------------
def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(directory: Path, scenario: str) -> tuple[dict[str, Any], Path]:
	run_path = directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / "tools/harness-scenarios/wpc-fliptronic" / f"{scenario}.json"
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful Doctor Who {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != 0:
		raise ValueError(f"built-in mechanisms must be disabled: {run_path}")
	return run, scenario_path


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


def _diagnostic(run: dict[str, Any], label: str, text: str) -> dict[str, Any]:
	snapshot = _snapshot(run, label)
	displays = [item for item in snapshot["displays"] if item["index"] == 0]
	if len(displays) != 1:
		raise ValueError(f"snapshot {label!r} must carry display 0 exactly once")
	return {
		"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
		"display_index": 0,
		"interpreted_text": text,
		"label": label,
		"nonzero_pixels": displays[0]["nonzero_pixels"],
		"pixel_sha256": displays[0]["pixel_sha256"],
	}


def _background(run: dict[str, Any], label: str) -> list[int]:
	"""Active public solenoids in the labelled snapshot, without 31, the always-active WPC GILAMPS bit-7 mirror."""
	return sorted(set(_snapshot(run, label)["active_solenoids"]) - {31})


def _seen(run: dict[str, Any]) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]})


def _document(name: str, directory: str, scenario: str, run: dict[str, Any], observations: dict[str, Any], command: str, initialization: str) -> dict[str, Any]:
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/doctor_who_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": command,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": GAME,
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": name,
					"nvram_initialization": initialization,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}/{GAME}/run.json",
					"scenario_path": f"tools/harness-scenarios/wpc-fliptronic/{scenario}.json",
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
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}/{GAME}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


NVRAM_NOTE = (
	"empty; the run created its own isolated PinMAME state directory, so the ROM performed its own factory reset before the "
	"scenario left the message loop with Escape"
)


def build_edges(review_root: Path) -> dict[str, Any]:
	directory = review_root / HARNESS_DIRECTORY / "switch-edges" / GAME
	run, _ = _load_run(directory, "dw-switch-edges-optos")
	snapshots = [_diagnostic(run, snapshot["label"], text) for snapshot in run["snapshots"] if (text := _edge_reading(snapshot["label"])) is not None]
	named = []
	for address in EDGE_SWITCHES:
		if address in FLIPPER_EDGES:
			name, last, wires = FLIPPER_EDGES[address]
			rising = _risen(_step(run, f"{address} -> 1"))
			if not {45, 46} & rising and not {47, 48} & rising:
				raise ValueError(f"the ROM did not fire the flipper for public {address}")
			named.append({
				"active_solenoid_addresses": _background(run, f"{address} -> 1"),
				"host_stimulus_switch_addresses": [address], "input_address": address, "input_kind": "switch",
				"label": f"T.1 with host public {address} set to 1: the ROM fires the flipper and names {last} ({name}); at 0 the name clears",
				"observed_switch_addresses": [], "result": "observed", "transitioned_solenoid_addresses": sorted(rising),
			})
			continue
		level = ROM_ACTIVE_LEVEL[address]
		active = _snapshot(run, f"{address} -> {level}")
		if address in OPTO_SWITCHES and address != 32:
			held = {item["number"]: item["state"] for item in active["watched_switches"]}
			if held[address] != 1:
				raise ValueError(f"host did not drive {address} to its active level")
		named.append({
			"active_solenoid_addresses": _background(run, f"{address} -> {level}"),
			"host_stimulus_switch_addresses": [address], "input_address": address, "input_kind": "switch",
			"label": f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is {level} and clears it at {1 - level}",
			"observed_switch_addresses": [], "result": "observed", "transitioned_solenoid_addresses": [],
		})
	# 32 is the one switch the ROM names at public 0 and clears at 1, checked from its own frames.
	if "Mini. Home Opto" not in _edge_reading("32 -> 0") or not _edge_reading("32 -> 1 again").startswith("SWITCH EDGES"):
		raise ValueError("unexpected 32 readings")
	observations = {
		"diagnostic_snapshots": snapshots,
		"named_action_observations": named,
		"solenoid_addresses_seen": _seen(run),
	}
	command = (
		"python tools/run_pinmame_harness.py --library <libpinmame> --game dw_l2 --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
		"--handle-mechanics 0 --scenario tools/harness-scenarios/wpc-fliptronic/dw-switch-edges-optos.json --dmd-dir <external-dmd-dir> "
		"--output <external-run.json>. Built-in mechanisms stay disabled. Each set_switch holds one public level for 2 s; the snapshot after "
		"it records the ROM's T.1 display and the watched public switch levels. The ROM names a switch on its top line while it reads the "
		"switch as active; the ten optos PinMAME's mask inverts are each driven 1, 0, 1."
	)
	return _document("dw-l2-switch-edges", "switch-edges", "dw-switch-edges-optos", run, observations, command, NVRAM_NOTE)


def build_solenoids(review_root: Path) -> dict[str, Any]:
	directory = review_root / HARNESS_DIRECTORY / "solenoid-test" / GAME
	run, _ = _load_run(directory, "dw-solenoid-test")
	snapshots = [_diagnostic(run, snapshot["label"], text) for snapshot in run["snapshots"] if (text := _t4_reading(snapshot["label"])) is not None]
	checkpoint = _step(run, "checkpoint: T.4 pulses solenoid 1")
	named = []
	for index, address in enumerate(T4_ORDER):
		if index == 0:
			risen = {item["number"] for item in checkpoint["matched_outputs"]}
		else:
			risen = _risen(_step(run, f"T.4 step {index}, frame 1"))
		if risen != {address}:
			raise ValueError(f"T.4 step {index} pulsed {sorted(risen)}, not {address}")
		named.append({
			"active_solenoid_addresses": [],
			"host_stimulus_switch_addresses": [7] if index else [8], "input_address": 7 if index else 8, "input_kind": "switch",
			"label": f"T.4 SOLENOID TEST selects public {address} ({T4_NAMES[address]}, {T4_WIRES[address]}): the ROM pulses it repeatedly",
			"observed_switch_addresses": [], "result": "observed", "transitioned_solenoid_addresses": [address],
		})
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"python tools/run_pinmame_harness.py --library <libpinmame> --game dw_l2 --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
		"--handle-mechanics 0 --scenario tools/harness-scenarios/wpc-fliptronic/dw-solenoid-test.json --dmd-dir <external-dmd-dir> "
		"--output <external-run.json>. Each Up press selects the next solenoid; in repeat mode the ROM pulses it until the next press, so the "
		"first frame after a press shows the address it selected. The test cycles fourteen coils (1-5, 7, 9-13, 15, 16 and 25) and then repeats."
	)
	return _document("dw-l2-solenoid-test", "solenoid-test", "dw-solenoid-test", run, observations, command, NVRAM_NOTE)


def build_mini_playfield(review_root: Path) -> dict[str, Any]:
	directory = review_root / HARNESS_DIRECTORY / "mini-playfield-test-exploratory" / GAME
	run, _ = _load_run(directory, "dw-mini-playfield-test")
	snapshots = [_diagnostic(run, label, text) for label, text in MINI_READINGS.items()]
	motor_alone = _risen(_step(run, "114 -> 1 (left flipper button held)"))
	first_wait = _step(run, "T.14 sub-test 1 with both flipper buttons held, second 1")
	if 28 not in motor_alone or 27 in motor_alone:
		raise ValueError("the first T.14 attempt must drive 28 without 27")
	together = _risen(_step(run, "T.14 sub-test 1 with both flipper buttons held, second 4"))
	if 27 not in _risen(first_wait) or not {27, 28} <= together:
		raise ValueError("T.14 must also drive 27 with 28 after its first attempt")
	kicker_left = _risen(_step(run, "T.14 sub-test 2, frame 1"))
	kicker_right = _risen(_step(run, "T.14 sub-test 2 with both flipper buttons held, second 1"))
	flasher = _risen(_step(run, "T.14 sub-test 3, frame 2"))
	if kicker_left != {4} or kicker_right != {5} or flasher != {17}:
		raise ValueError(f"unexpected T.14 sub-test outputs: {kicker_left}, {kicker_right}, {flasher}")
	named = [
		{
			"active_solenoid_addresses": [],
			"host_stimulus_switch_addresses": [112, 114], "input_address": 114, "input_kind": "switch",
			"label": "T.14 sub-test 1 with both flipper buttons held: the ROM moves the mini-playfield clockwise with 28 alone",
			"observed_switch_addresses": [], "result": "observed", "transitioned_solenoid_addresses": [28],
		},
		{
			"active_solenoid_addresses": [],
			"host_stimulus_switch_addresses": [112, 114], "input_address": 114, "input_kind": "switch",
			"label": "After its error (no feedback switch answers with built-in mechanisms off) T.14 moves counter-clockwise with 27 and 28 together",
			"observed_switch_addresses": [], "result": "observed", "transitioned_solenoid_addresses": [27, 28],
		},
		{
			"host_stimulus_switch_addresses": [7], "input_address": 7, "input_kind": "switch",
			"active_solenoid_addresses": [], "label": "T.14 L Kicker sub-test pulses 4", "observed_switch_addresses": [], "result": "observed",
			"transitioned_solenoid_addresses": [4],
		},
		{
			"host_stimulus_switch_addresses": [112, 114], "input_address": 114, "input_kind": "switch",
			"active_solenoid_addresses": [], "label": "T.14 R Kicker sub-test pulses 5", "observed_switch_addresses": [], "result": "observed",
			"transitioned_solenoid_addresses": [5],
		},
		{
			"host_stimulus_switch_addresses": [7], "input_address": 7, "input_kind": "switch",
			"active_solenoid_addresses": [], "label": "T.14 Flasher sub-test pulses 17", "observed_switch_addresses": [], "result": "observed",
			"transitioned_solenoid_addresses": [17],
		},
	]
	observations = {
		"diagnostic_snapshots": snapshots,
		"named_action_observations": named,
		"solenoid_addresses_seen": _seen(run),
	}
	command = (
		"python tools/run_pinmame_harness.py --library <libpinmame> --game dw_l2 --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
		"--handle-mechanics 0 --scenario tools/harness-scenarios/wpc-fliptronic/dw-mini-playfield-test.json --dmd-dir <external-dmd-dir> "
		"--output <external-run.json>. The scenario starts T.14 MINI-PLAYFIELD TEST, confirms its warning and holds both flipper buttons "
		"(112 and 114), which the test requires before it moves the mini-playfield. The test's own sub-tests are timing-dependent: a rerun "
		"may stop after its second fault before it reaches the later sub-tests, so this run, not the scenario, is the evidence. With built-in "
		"mechanisms disabled no feedback switch answers the motor, so the ROM reports faults; the run shows which outputs it drives, not the "
		"mini-playfield's travel or timing."
	)
	return _document("dw-l2-mini-playfield-test", "mini-playfield-test-exploratory", "dw-mini-playfield-test", run, observations, command, NVRAM_NOTE)


BUILDERS = {
	"doctor-who-dw_l2-switch-edges.json": build_edges,
	"doctor-who-dw_l2-solenoid-test.json": build_solenoids,
	"doctor-who-dw_l2-mini-playfield-test.json": build_mini_playfield,
}
DIRECTORIES = {
	"doctor-who-dw_l2-switch-edges.json": "switch-edges",
	"doctor-who-dw_l2-solenoid-test.json": "solenoid-test",
	"doctor-who-dw_l2-mini-playfield-test.json": "mini-playfield-test-exploratory",
}


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	for filename, builder in BUILDERS.items():
		document = builder(review_root)
		directory = review_root / HARNESS_DIRECTORY / DIRECTORIES[filename] / GAME
		run_sha = _sha256(directory / "run.json")
		manifest_sha = _sha256(directory / "manifest.json")
		document["runtime"]["raw_runs"][0]["sha256"] = run_sha
		document["source"]["sha256"] = run_sha
		document["source"]["attribution"] += f" Exact external directory manifest {GAME}/manifest.json SHA-256 {manifest_sha}."
		documents[filename] = document
	return documents


def write(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		write_json(EVIDENCE_DIRECTORY / filename, document)


def check(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		path = EVIDENCE_DIRECTORY / filename
		if not path.is_file() or path.read_bytes() != canonical_bytes(document):
			raise ValueError(f"Doctor Who compact runtime evidence drift: {path}")


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
		print("Doctor Who compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
