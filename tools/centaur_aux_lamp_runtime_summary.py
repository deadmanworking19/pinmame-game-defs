#!/usr/bin/env python3
"""Build the compact runtime-evidence summary for Bally Centaur's auxiliary lamp probe.

The raw LibPinMAME harness trace stays outside the repository. This tool reads it, derives every
observation the definition cites, and writes ``evidence/runtime/by35/centaur-aux-lamps-in-play.json``:
which auxiliary lamp each top-lane, slingshot and thumper-bumper closure lights, how the shared
flipper-button switch rotates the top-lane lamps, and every transition of public lamp 113. Each
derivation refuses a run that does not show it, so a rerun that behaves differently fails rather
than being relabelled. A test recomputes the summary when the retained run is present.

    python tools/centaur_aux_lamp_runtime_summary.py --run-dir <review-artifacts/centaur-1981/harness-aux-lamps/centaur> [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256  # noqa: E402
from build_external_evidence_manifest import build_manifest, canonical_bytes as manifest_bytes  # noqa: E402

OUTPUT = ROOT / "evidence" / "runtime" / "by35" / "centaur-aux-lamps-in-play.json"
SCENARIO = "tools/harness-scenarios/by35/centaur-aux-lamps-in-play.json"
RETAINED = "external:pinmame-review-artifacts/centaur-1981/harness-aux-lamps/centaur"
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "bd01d071981b9b2c4afd144e46d47a657e9fca5f73673bf6cc0a75399aead625"
# When the harness wrote run.json; the trace itself carries no wall-clock time.
CAPTURED_AT = "2026-10-22T20:45:59Z"

RING = (65, 81, 97, 113)
AUXILIARY = tuple(range(65, 69)) + tuple(range(81, 85)) + tuple(range(97, 101)) + tuple(range(113, 117))
# slingshot or thumper-bumper switch -> (lamp it must flick, solenoid it must fire)
STRIKES = {37: (66, 13), 38: (82, 12), 39: (98, 11), 40: (114, 10)}
# expected (lit, extinguished) top-lane lamps for each flipper-button press, in order
LANE_CHANGES = (
	({81}, {65}),
	({97}, {81}),
	({65, 113}, {97}),
	({81}, {65, 113}),
	({97}, {81}),
	({65, 113}, {97}),
)
WINDOW_S = 0.3
# A struck lamp must come back on this soon after it goes out.
RELIGHT_S = 0.5
# The two lamp groups the ROM writes at once in its power-up and game-start flashes, each containing
# 113: lamp-data line PD3 on both boards, and latched lamp address 0 on every data line of both boards.
FLASH_GROUPS = {
	"data line PD3": frozenset(range(49, 64)) | {113, 114, 115, 116},
	"lamp address 0": frozenset({1, 17, 33, 49, 65, 81, 97, 113}),
}
# A flash turns its lamps on and back off within this time.
FLASH_PHASE_S = 0.3


def lamp_events(run: dict) -> list[dict]:
	return [event for event in run["events"] if event["event"] == "lamp"]


def press_times(run: dict, switch: int) -> list[float]:
	return [
		event["time_s"]
		for event in run["events"]
		if event["event"] == "switch" and event.get("number") == switch and event["state"] == 1 and not event.get("initial")
	]


def changed_after(events: list[dict], start: float, numbers: tuple[int, ...], state: int) -> set[int]:
	return {
		event["number"]
		for event in events
		if event["number"] in numbers and event["state"] == state and start < event["time_s"] <= start + WINDOW_S
	}


def lit_between(events: list[dict], start: float, end: float) -> set[int]:
	return {event["number"] for event in events if event["state"] == 1 and start < event["time_s"] <= end}


def verify_top_lanes(run: dict, events: list[dict]) -> dict[str, int]:
	"""Each top-lane closure lights one lane lamp that was not already made.

	A newly made lane blinks for a while, so a lamp lit since play began (or since the lanes were last
	cleared) is excluded from what the next closure lights. The third distinct lane completes the set:
	it lights nothing new and leaves every lane lamp dark, and public 3 on the cleared lanes then lights
	its own lamp again.
	"""
	released = [
		event["time_s"] for event in run["events"]
		if event["event"] == "switch" and event.get("number") == 8 and event["state"] == 0 and not event.get("initial")
	]
	if len(released) != 1:
		raise SystemExit("expected the outhole to be released exactly once")
	play = released[0]
	(left,), (middle,) = press_times(run, 5), press_times(run, 4)
	completing, cleared = press_times(run, 3)
	pairing: dict[str, int] = {}
	for switch, press, since, lamp in ((5, left, play, 97), (4, middle, play, 81)):
		lit = changed_after(events, press, AUXILIARY, 1) - lit_between(events, since, press)
		if lit != {lamp}:
			raise SystemExit(f"public {switch} lit auxiliary lamps {sorted(lit)}, expected {lamp}")
		pairing[str(switch)] = lamp
	if changed_after(events, completing, AUXILIARY, 1) - lit_between(events, play, completing):
		raise SystemExit("completing the top lanes lit a lane lamp that was not already made")
	state = {number: 0 for number in RING}
	for event in events:
		if event["number"] in RING and event["time_s"] < cleared:
			state[event["number"]] = event["state"]
	if any(state.values()):
		raise SystemExit(f"top-lane lamps were not all dark before the second closure of public 3: {state}")
	lit = changed_after(events, cleared, AUXILIARY, 1) - lit_between(events, completing, cleared)
	if lit != {65}:
		raise SystemExit(f"public 3 on cleared lanes lit {sorted(lit)}, expected 65")
	pairing["3"] = 65
	return pairing


def verify_strikes(run: dict, events: list[dict]) -> dict[str, int]:
	"""A struck slingshot or thumper bumper fires its coil and flicks its own lamp off and on.

	Exactly one auxiliary lamp goes out in the window after the closure, and that lamp comes back on
	within RELIGHT_S of going out.
	"""
	pairing: dict[str, int] = {}
	for switch, (lamp, solenoid) in STRIKES.items():
		presses = press_times(run, switch)
		if len(presses) != 1:
			raise SystemExit(f"expected one closure of public {switch}, saw {len(presses)}")
		flicked = changed_after(events, presses[0], AUXILIARY, 0)
		if flicked != {lamp}:
			raise SystemExit(f"public {switch} flicked auxiliary lamps {sorted(flicked)}, expected {lamp}")
		out = min(
			e["time_s"] for e in events
			if e["number"] == lamp and e["state"] == 0 and presses[0] < e["time_s"] <= presses[0] + WINDOW_S
		)
		if not any(e["number"] == lamp and e["state"] == 1 and out < e["time_s"] <= out + RELIGHT_S for e in events):
			raise SystemExit(f"lamp {lamp} did not come back on within {RELIGHT_S} s of the public {switch} strike")
		fired = {
			e["number"] for e in run["events"]
			if e["event"] == "solenoid" and e["state"] == 1 and presses[0] <= e["time_s"] <= presses[0] + WINDOW_S
		}
		if solenoid not in fired:
			raise SystemExit(f"public {switch} did not fire solenoid {solenoid}")
		pairing[str(switch)] = lamp
	return pairing


def verify_lane_changes(run: dict, events: list[dict]) -> list[dict]:
	presses = press_times(run, 21)
	if len(presses) != len(LANE_CHANGES):
		raise SystemExit(f"expected {len(LANE_CHANGES)} flipper-button presses, saw {len(presses)}")
	changes = []
	for index, (press, (on, off)) in enumerate(zip(presses, LANE_CHANGES), start=1):
		lit = changed_after(events, press, AUXILIARY, 1)
		dark = changed_after(events, press, AUXILIARY, 0)
		if lit != on or dark != off:
			raise SystemExit(f"lane change {index}: lit {sorted(lit)} and extinguished {sorted(dark)}, expected {sorted(on)} and {sorted(off)}")
		changes.append({"press": index, "lit": sorted(lit), "extinguished": sorted(dark)})
	return changes


def classify_113(run: dict, events: list[dict]) -> dict[str, int]:
	"""Every transition of public 113 is either part of a top-lane rotation or part of a lamp flash.

	A rotation is a change within the window after a flipper-button press in which 65 makes the same
	change in the same update and no auxiliary address outside the lane lamps 65, 81 and 97 changes;
	main-board lamps are refreshed in the same frames and may change beside it.

	A flash is a change before the ball is served in which 113 and at least three other lamps of one
	flash group change in the same update, every lamp that changes belongs to that group, and every one
	of them makes the same change as 113. Flashes come in phases: each flash that lights 113 is followed
	within FLASH_PHASE_S by a flash of the same group that puts it out.

	Anything else refuses the run.
	"""
	flipper = press_times(run, 21)
	served = min(
		event["time_s"] for event in run["events"]
		if event["event"] == "switch" and event.get("number") == 8 and event["state"] == 0 and not event.get("initial")
	)
	by_time: dict[float, dict[int, int]] = {}
	for event in events:
		by_time.setdefault(event["time_s"], {})[event["number"]] = event["state"]
	counts = {"whole_row_flash": 0, "lane_rotation_with_65": 0}
	flashes: list[tuple[float, int, str]] = []
	for event in events:
		if event["number"] != 113:
			continue
		time, state = event["time_s"], event["state"]
		together = {number: value for number, value in by_time[time].items() if number != 113}
		auxiliary = {number for number in together if number in AUXILIARY}
		after_press = any(0 < time - press <= WINDOW_S for press in flipper)
		if after_press and together.get(65) == state and auxiliary <= {65, 81, 97}:
			counts["lane_rotation_with_65"] += 1
			continue
		group = next(
			(
				name for name, members in FLASH_GROUPS.items()
				if set(together) <= members and len(together) >= 3 and all(value == state for value in together.values())
			),
			None,
		)
		if not after_press and time < served and group is not None:
			counts["whole_row_flash"] += 1
			flashes.append((time, state, group))
			continue
		raise SystemExit(f"lamp 113 changed at {time} s outside a lamp flash or a lane rotation: {sorted(together.items())}")
	if not counts["lane_rotation_with_65"]:
		raise SystemExit("the run never rotated the top lanes through 113")
	if len(flashes) % 2 or not flashes:
		raise SystemExit("the lamp flashes do not pair 113 on with 113 off")
	for (on_time, on_state, on_group), (off_time, off_state, off_group) in zip(flashes[0::2], flashes[1::2]):
		if (on_state, off_state) != (1, 0) or on_group != off_group or not 0 < off_time - on_time <= FLASH_PHASE_S:
			raise SystemExit(f"the {on_group} flash at {on_time} s is not followed by its own off phase")
	return counts


def step_observations(run: dict) -> list[dict]:
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	items = []
	for step in run["steps"]:
		if step["type"] not in ("pulse", "set_switch"):
			continue
		snapshot = snapshots[step["label"]]
		transitioned = sorted({item["number"] for item in step["transitions"]["solenoids"]})
		items.append({
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"host_stimulus_switch_addresses": [step["switch"]],
			"input_address": step["switch"],
			"input_kind": "switch",
			"label": f"aux lamps in play: {step['label']}",
			"observed_switch_addresses": [],
			"result": "observed" if transitioned else "no_matching_transition",
			"transitioned_solenoid_addresses": transitioned,
		})
	return items


def verify(run: dict) -> tuple[dict[str, int], list[dict], dict[str, int]]:
	"""Every check the summary relies on, on a loaded trace: the switch-to-lamp pairing, the lane
	rotation and the classification of lamp 113. Refuses a trace that does not show them."""
	if run["failure"] is not None or run["library_sha256"] != LIBRARY_SHA256 or run["game"] != "centaur" or run["handle_mechanics"] != 0:
		raise SystemExit("the run is not a clean pinned-library centaur run")
	events = lamp_events(run)
	pairing = verify_top_lanes(run, events)
	pairing.update(verify_strikes(run, events))
	changes = verify_lane_changes(run, events)
	counts = classify_113(run, events)
	return pairing, changes, counts


def build(run_dir: Path) -> dict:
	path = run_dir / "run.json"
	run = json.loads(path.read_text(encoding="utf-8"))
	if file_sha256(ROOT / SCENARIO) != file_sha256(run_dir / "scenario.json"):
		raise SystemExit("the retained scenario copy differs from the committed scenario")
	pairing, changes, counts = verify(run)
	events = lamp_events(run)
	lamps = sorted({event["number"] for event in events})
	solenoids = sorted({event["number"] for event in run["events"] if event["event"] == "solenoid"})
	manifest = build_manifest(run_dir, "centaur")
	digest = hashlib.sha256(manifest_bytes(manifest) + b"\n").hexdigest()
	files = len(manifest["files"])
	total = sum(item["size"] for item in manifest["files"])
	rotation = "; ".join(
		f"press {item['press']}: lit {', '.join(map(str, item['lit']))}, extinguished {', '.join(map(str, item['extinguished']))}"
		for item in changes
	)
	return {
		"driver_ids": ["centaur"],
		"extractor": {"id": "tools/centaur_aux_lamp_runtime_summary.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["bally.centaur.1981"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": (
				"python tools/run_pinmame_harness.py --library <libpinmame> --game centaur --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
				f"--handle-mechanics 0 --scenario {SCENARIO} --output <external-run.json>. Every pulse and set_switch is a host stimulus, never a ROM "
				"observation; the trough switches 1, 2, 17 and 33 and the outhole 8 are held closed from power-up so the ROM can serve a ball."
			),
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": LIBRARY_SHA256},
			"game": "centaur",
			"observations": {
				"lamp_addresses_seen": lamps,
				"named_action_observations": step_observations(run),
				"runs": {
					"centaur-aux-lamps-in-play": {
						"note": (
							"Each top-lane closure lit one lane lamp: public 5 (printed TOP LEFT LANE) lit 97, public 4 (TOP MIDDLE LANE) lit 81, and public 3 "
							"(TOP RIGHT LANE) completed the three lanes, which left every lane lamp dark, and on the cleared lanes lit 65. The shared flipper-button "
							f"switch 21 rotated the lit lane through 65, 81 and 97 ({rotation}); whenever the lit lane wrapped from 97 to 65 the ROM also raised 113 "
							"in the same update and cleared it again with 65 on the next rotation, so 113 is the carry bit of a four-bit top-lane register. Over "
							f"the whole run lamp 113 changed {counts['whole_row_flash']} times as part of power-up and game-start lamp flashes, in each of which "
							"it and at least three other lamps of its lamp-data line PD3 or of lamp address 0 made the same change in one update, every lighting "
							f"put out again by the same group within {FLASH_PHASE_S} s, and "
							f"{counts['lane_rotation_with_65']} times with 65 at a lane rotation, and never otherwise. "
							"A struck slingshot or thumper bumper flicked its own lamp off and back on and fired its own coil: 37 flicked 66 and fired 13, 38 flicked 82 and fired 12, "
							"39 flicked 98 and fired 11, and 40 flicked 114 and fired 10. Every one of these is derived from the lamp and solenoid events of the "
							"retained trace by tools/centaur_aux_lamp_runtime_summary.py, which refuses a trace that does not show it."
						),
					},
				},
				"solenoid_addresses_seen": solenoids,
				"switch_to_lamp": dict(sorted(pairing.items(), key=lambda item: int(item[0]))),
			},
			"raw_runs": [{
				"action_count": run["scenario"]["action_count"],
				"initial_switches": sorted(run["initial_switches"], key=lambda item: item["switch"]),
				"name": "centaur-aux-lamps-in-play",
				"nvram_initialization": "empty; the run created its own isolated PinMAME state directory (state/ beside run.json), sends no keyboard or service input, and coins up and starts a game with direct switch writes",
				"retained_from": f"{RETAINED}/run.json",
				"scenario_path": SCENARIO,
				"scenario_sha256": file_sha256(ROOT / SCENARIO),
				"self_test_pulses": 0,
				"sha256": file_sha256(path),
				"snapshot_count": len(run["snapshots"]),
				"watch_switches": sorted(run["watch_switches"]),
			}],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": (
				f"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Captured {CAPTURED_AT} "
				"(the time the harness wrote run.json). Public switch writes are host stimuli, never ROM observations. The raw trace has no DMD frames."
			),
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": (
				"source.sha256 is a directory manifest digest, not a file hash: the SHA-256 recorded in manifest.sha256 beside manifest.json, built by "
				"tools/build_external_evidence_manifest.py, which lists every file below source.path as {path, size, sha256} with path relative and "
				"POSIX-separated, sorted by path, serialised as compact canonical JSON (separators=(',',':'), sort_keys=True, ensure_ascii=False) plus a "
				f"newline, encoded UTF-8. At capture time the tree held {files} files totalling {total} bytes: the raw trace, the copied scenario and the "
				"isolated mutable state, with no ROM bytes. The run's own hash is in runtime.raw_runs[].sha256."
			),
			"path": RETAINED,
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
	parser.add_argument("--run-dir", type=Path, required=True)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = canonical_bytes(build(args.run_dir))
	if args.check:
		if OUTPUT.read_bytes() != text:
			print("runtime summary drift", file=sys.stderr)
			return 1
		print("runtime summary matches the retained run")
		return 0
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	OUTPUT.write_bytes(text)
	print(f"wrote {OUTPUT.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
