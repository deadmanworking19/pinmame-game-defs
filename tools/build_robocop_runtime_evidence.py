"""Derive compact RoboCop service-walk evidence from the retained robo_a34 and robo_a30 runs.

Each run walks the ROM's own Switch Test, Lamp Test and Coil Auto with the
recorded scenario. For every address the curated reading in
tools/seeds/data-east/robocop-1989-service-readings.json must appear on the
Player 1/2 alpha display (index 0) while the Player 3/4 display (index 1) shows
that address's own wire or bank code, in both runs; otherwise the build fails. The compact evidence retains the matching display
frames of the root driver robo_a34 and states that robo_a30 printed the same
names.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes

ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
SCENARIO_PATH = Path("tools/harness-scenarios/data-east/robo-a34-service-walk.json")
READINGS_PATH = Path("tools/seeds/data-east/robocop-1989-service-readings.json")
EVIDENCE_PATH = Path("evidence/runtime/data-east/robocop-service-walk.json")
MACHINE_ID = "data-east.robocop.1989"
RUN_ROOT = "data-east.robocop.1989/final"
DRIVERS = {
	"robo_a34": {
		"rom_archive_sha256": "a3525015b9266511fc2f4f0d0ecf3cdde9c40b412d30bacb618e5f56a6f98126",
		"manifest_sha256": "4bc69a000ca8539a223c31197f683b180a56af04474edfddf62f6192fa3d3606",
	},
	"robo_a30": {
		"rom_archive_sha256": "3dfe07399e5ea8ff98dd8cd9a18b5811044da1b6d4b9785ea509f0e103874aaa",
		"manifest_sha256": "edf8ef6dda58b8ee658676de1175c50a43bc6fd7c66bd7caa5718b74a6b8fbc6",
	},
}
# PinMAME's decoder has no character for this ROM's 14-segment 1 (0x0006) and
# 9 (0x0867) and renders them '?'. The ROM draws 0 like O and 5 like S, so the
# comparison folds those two pairs; nothing else is normalized.
GLYPHS = {0x0006: "1", 0x0867: "9"}
FOLD = str.maketrans({"0": "O", "5": "S"})


def display_text(event: dict) -> str:
	return "".join(GLYPHS.get(segment, char) if char == "?" else char for char, segment in zip(event["text"], event["segments"]))


def folded(text: str) -> str:
	return " ".join(text.upper().translate(FOLD).split())


def load_run(review_root: Path, driver: str) -> tuple[dict, str]:
	path = review_root / RUN_ROOT / driver / "run.json"
	raw = path.read_bytes()
	run = json.loads(raw)
	scenario_sha256 = hashlib.sha256((ROOT / SCENARIO_PATH).read_bytes()).hexdigest()
	if run.get("failure") is not None or run.get("game") != driver:
		raise ValueError(f"not a successful {driver} run: {path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {path}")
	if run.get("scenario", {}).get("sha256") != scenario_sha256:
		raise ValueError(f"scenario identity drift: {path}")
	manifest = path.parent / "manifest.json"
	if hashlib.sha256(manifest.read_bytes()).hexdigest() != DRIVERS[driver]["manifest_sha256"]:
		raise ValueError(f"external manifest drift: {manifest}")
	return run, hashlib.sha256(raw).hexdigest()


def first_title(events: list[dict], title: str) -> float:
	for event in events:
		if event["event"] == "display" and event["index"] == 0 and folded(display_text(event)) == folded(title):
			return event["time_s"]
	raise ValueError(f"display title {title!r} never appeared")


def frames_in_window(events: list[dict], index: int, start: float, end: float) -> list[dict]:
	"""The frame still shown when the window opened, then every frame inside it.

	The display emits no frame for an unchanged text, so consecutive unfitted
	addresses that all print NONE leave the later windows without a frame.
	"""
	frames = [event for event in events if event["event"] == "display" and event["index"] == index and event["time_s"] < end]
	return [event for event in frames if event["time_s"] < start][-1:] + [event for event in frames if event["time_s"] >= start]


def find_name(events: list[dict], anchor: dict, reading: str, context: str) -> dict:
	"""The name frame shown together with the anchor frame: current when the anchor
	appeared, or appearing before Player 3/4 next changes. This pairs each name
	with the frame that prints its own address, never a neighbour's."""
	start = anchor["time_s"]
	later = [event["time_s"] for event in events if event["event"] == "display" and event["index"] == 1 and event["time_s"] > start]
	end = later[0] if later else float("inf")
	# Both rows refresh at one timestamp, so the frame current with the anchor is the latest at or before it.
	frames = [event for event in events if event["event"] == "display" and event["index"] == 0 and event["time_s"] < end]
	for event in [event for event in frames if event["time_s"] <= start][-1:] + [event for event in frames if event["time_s"] > start]:
		if folded(display_text(event)) == folded(reading):
			return event
	raise ValueError(f"{context}: reading {reading!r} not displayed while its address frame at {start:.3f}s was shown")


def numeric(text: str) -> str:
	"""Undo the 0/O and 5/S folding in a field the ROM prints as digits."""
	return text.replace("O", "0").replace("S", "5")


def find_code(events: list[dict], start: float, end: float, address: int, context: str) -> tuple[dict, str]:
	"""Player 3/4 carries the wire code (return-drive) at 0-4 and the address at 11-12."""
	for event in frames_in_window(events, 1, start, end):
		text = display_text(event)
		code, number = numeric(text[0:5]), numeric(text[11:13])
		if number == f"{address:02d}" and len(code) == 5 and code[2] == "-" and (code[:2] + code[3:]).isdecimal():
			return event, f"{code} {number}"
	raise ValueError(f"{context}: no wire code with address {address:02d} between {start:.3f}s and {end:.3f}s")


def find_bank(events: list[dict], start: float, end: float, bank: str, context: str) -> dict:
	"""Coil Auto prints COIL and the driver's bank code (L01-L08, 09-16, R01-R08) at 11-13."""
	for event in frames_in_window(events, 1, start, end):
		text = display_text(event)
		if text.startswith("COIL") and folded(text[11:14]) == folded(bank):
			return event
	raise ValueError(f"{context}: bank code {bank!r} not displayed between {start:.3f}s and {end:.3f}s")


def response(event: dict, positions: list[int], text: str, address: int) -> dict:
	return {
		"snapshot_label": f"display {event['index']} event at {event['time_s']:.3f}s",
		"display_index": event["index"],
		"segments": list(event["segments"]),
		"decoded_segment_positions": positions,
		"interpreted_text": text,
		"diagnostic_address": address,
	}


def name_response(event: dict, reading: str, address: int) -> dict:
	return response(event, [index for index, segment in enumerate(event["segments"]) if segment], reading, address)


CODE_POSITIONS = [0, 1, 2, 3, 4, 11, 12]
BANK_POSITIONS = [11, 12, 13]


def walk(run: dict, readings: dict) -> dict[str, list]:
	events = run["events"]
	lamp_title = first_title(events, "LAMP TEST")
	coil_title = first_title(events, "COIL AUTO")
	starts: list[tuple[float, object]] = []
	for event in events:
		if event["time_s"] >= lamp_title:
			break
		if event["event"] == "switch" and event["state"] == 1 and 1 <= event["number"] <= 64:
			starts.append((event["time_s"], event["number"]))
		if event["event"] == "key" and event["state"] == 1 and event["key"] in readings["switch_test_keys"]:
			starts.append((event["time_s"], event["key"]))
	starts.sort(key=lambda item: item[0])
	switches: dict[object, list[dict]] = {}
	for index, (start, address) in enumerate(starts):
		if address in switches:
			raise ValueError(f"switch {address} closed twice")
		end = starts[index + 1][0] if index + 1 < len(starts) else lamp_title
		if isinstance(address, int):
			reading, number = readings["switch_test"][str(address)], address
		else:
			number, reading = readings["switch_test_keys"][address]
		code_event, code = find_code(events, start, end, number, f"switch {address}")
		switches[address] = [
			name_response(find_name(events, code_event, reading, f"switch {address}"), reading, number),
			response(code_event, CODE_POSITIONS, code, number),
		]
	if set(switches) != {number for number in range(1, 65) if number not in (15, 16)} | set(readings["switch_test_keys"]):
		raise ValueError("switch walk did not close every scheduled address")
	lamp_ons = [(event["time_s"], event["number"]) for event in events
		if event["event"] == "lamp" and event["state"] == 1 and lamp_title < event["time_s"] < coil_title]
	lamps: dict[int, list[dict]] = {}
	for index, (start, number) in enumerate(lamp_ons):
		if number in lamps:
			continue
		end = lamp_ons[index + 1][0] if index + 1 < len(lamp_ons) else coil_title
		reading = readings["lamp_test"][str(number)]
		code_event, code = find_code(events, start - 0.5, end, number, f"lamp {number}")
		lamps[number] = [
			name_response(find_name(events, code_event, reading, f"lamp {number}"), reading, number),
			response(code_event, CODE_POSITIONS, code, number),
		]
	if sorted(lamps) != list(range(1, 65)):
		raise ValueError(f"lamp test did not step through 1-64: {sorted(lamps)}")
	coil_ons = [(event["time_s"], event["number"]) for event in events
		if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > coil_title]
	coils: dict[int, list[dict]] = {}
	for start, number in coil_ons:
		if number in coils:
			continue
		entry = readings["coil_test"][str(number)]
		bank_event = find_bank(events, start - 0.25, start + 1.5, entry["bank_code"], f"coil {number}")
		coils[number] = [
			name_response(find_name(events, bank_event, entry["name"], f"coil {number}"), entry["name"], number),
			response(bank_event, BANK_POSITIONS, entry["bank_code"], number),
		]
	if sorted(coils) != sorted(int(key) for key in readings["coil_test"]):
		raise ValueError(f"Coil Auto did not fire every scheduled output: {sorted(coils)}")
	return {
		"switches": [item for key in sorted(switches, key=lambda item: (isinstance(item, str), str(item).zfill(3))) for item in switches[key]],
		"lamps": [item for number in sorted(lamps) for item in lamps[number]],
		"coils": [item for number in sorted(coils) for item in coils[number]],
		"coil_sequence": [number for _, number in coil_ons],
	}


def checkpoints(run: dict) -> list[dict]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
		for step in run["steps"] if step["type"] == "pulse_until_display"]


def first_cycle(sequence: list[int]) -> list[int]:
	"""The Coil Auto order up to the first repeat of output 1."""
	if not sequence or sequence[0] != 1:
		raise ValueError(f"Coil Auto did not start at output 1: {sequence[:4]}")
	try:
		end = sequence.index(1, 1)
	except ValueError as error:
		raise ValueError("Coil Auto did not complete one cycle") from error
	return sequence[:end]


def build(review_root: Path) -> dict:
	readings = json.loads((ROOT / READINGS_PATH).read_bytes())
	scenario = json.loads((ROOT / SCENARIO_PATH).read_bytes())
	walks, raw_runs, runs = {}, [], {}
	for driver in DRIVERS:
		run, run_sha256 = load_run(review_root, driver)
		walks[driver] = walk(run, readings)
		raw_runs.append({
			"name": driver, "sha256": run_sha256, "scenario_path": SCENARIO_PATH.as_posix(),
			"scenario_sha256": run["scenario"]["sha256"], "action_count": len(scenario["actions"]),
			"watch_switches": run["watch_switches"], "self_test_pulses": sum(item["after_service_pulses"] for item in checkpoints(run)),
			"nvram_initialization": "new empty isolated state directory; no NVRAM inherited", "boot_wait_s": 2.0,
			"snapshot_count": len(run["snapshots"]), "retained_from": f"{RUN_ROOT}/{driver}/run.json",
		})
		cycle = first_cycle(walks[driver]["coil_sequence"])
		runs[driver.replace("_", "-")] = {
			"diagnostic_checkpoints": checkpoints(run),
			"ordered_solenoid_on_sequence": cycle,
			"solenoid_addresses_seen": sorted(set(walks[driver]["coil_sequence"])),
		}
	root, clone = walks["robo_a34"], walks["robo_a30"]
	for kind in ("switches", "lamps", "coils"):
		if [(item["diagnostic_address"], item["interpreted_text"]) for item in root[kind]] != [(item["diagnostic_address"], item["interpreted_text"]) for item in clone[kind]]:
			raise ValueError(f"robo_a30 {kind} readings differ from robo_a34")
	if runs["robo-a34"]["ordered_solenoid_on_sequence"] != runs["robo-a30"]["ordered_solenoid_on_sequence"]:
		raise ValueError("robo_a30 Coil Auto order differs from robo_a34")
	runs["robo-a34"]["named_action_observations"] = [
		{
			"label": "Switch Test: host closes each matrix address and holds each flipper key; the ROM names it on Player 1/2",
			"input_kind": "switch", "input_address": 1,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [number for number in range(1, 65) if number not in (15, 16)],
			"display_responses": root["switches"], "active_solenoid_addresses": [], "transitioned_solenoid_addresses": [], "result": "observed",
		},
		{
			"label": "Lamp Test: each Start press steps one lamp; the ROM names the lit address on Player 1/2",
			"input_kind": "switch", "input_address": 3,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [3],
			"display_responses": root["lamps"], "active_solenoid_addresses": [], "transitioned_solenoid_addresses": [], "result": "observed",
		},
		{
			"label": "Coil Auto: the ROM fires each output in turn and names it on Player 1/2",
			"input_kind": "switch", "input_address": -7,
			"observed_switch_addresses": [], "host_stimulus_switch_addresses": [-7],
			"display_responses": root["coils"], "active_solenoid_addresses": runs["robo-a34"]["solenoid_addresses_seen"],
			"transitioned_solenoid_addresses": runs["robo-a34"]["solenoid_addresses_seen"], "result": "observed",
		},
	]
	runs["robo-a34"]["limitation"] = (
		"Each address carries two responses: the first Player 1/2 frame in its window whose text equals the curated name after "
		"folding 0/O and 5/S, and the Player 3/4 frame giving its wire code and address (Coil Auto: its bank code). Where several "
		"unfitted addresses print NONE in a row the display emits no new name frame, so the retained name frame is the one still "
		"shown when the window opened. A ROM name identifies the feature the ROM's own test assigns to the address; it does not "
		"prove the feature is fitted, its polarity or its location.")
	runs["robo-a30"]["note"] = "The builder required every Switch Test, Lamp Test and Coil Auto reading of robo_a34 to appear identically in this run, and the Coil Auto order to match; it did, so the frames are not repeated."
	return {
		"format": "pinmame-machine-evidence", "version": 1,
		"extractor": {"id": "tools/build_robocop_runtime_evidence.py", "version": 1},
		"source": {
			"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"path": f"external:pinmame-review-artifacts/{RUN_ROOT}", "sha256": DRIVERS["robo_a34"]["manifest_sha256"],
			"manifest_algorithm": "source.sha256 is SHA-256 of robo_a34/manifest.json's exact UTF-8 bytes; robo_a30/manifest.json has SHA-256 "
				+ DRIVERS["robo_a30"]["manifest_sha256"] + ". Each manifest is compact canonical JSON with sorted keys and one LF, listing every file below its run directory except manifest.json and manifest.sha256 as {path, sha256, size}.",
			"license": "NOASSERTION", "quality": "observed",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external.",
		},
		"driver_ids": list(DRIVERS), "machine_ids": [MACHINE_ID],
		"switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
		"runtime": {
			"game": "robo_a34", "rom_archive_sha256": DRIVERS["robo_a34"]["rom_archive_sha256"],
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
			"raw_runs": raw_runs,
			"command_template": "python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game <robo_a34|robo_a30> --rom-path <legal-ROM-root> --work-dir <fresh-state> --scenario tools/harness-scenarios/data-east/robo-a34-service-walk.json --boot-wait 2 --output <external-run>; robo_a30's ROM archive SHA-256 is " + DRIVERS["robo_a30"]["rom_archive_sha256"] + ".",
			"observations": {"service_language": "English", "display_indices_seen": [0, 1], "runs": runs},
		},
	}


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("review_root", type=Path)
	parser.add_argument("--check", action="store_true", help="refuse drift instead of writing")
	args = parser.parse_args()
	data = canonical_bytes(build(args.review_root))
	if args.check:
		if (ROOT / EVIDENCE_PATH).read_bytes() != data:
			raise SystemExit("RoboCop runtime evidence drift")
		print("RoboCop runtime evidence matches the retained runs.")
	else:
		(ROOT / EVIDENCE_PATH).parent.mkdir(parents=True, exist_ok=True)
		(ROOT / EVIDENCE_PATH).write_bytes(data)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
