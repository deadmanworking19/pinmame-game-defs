#!/usr/bin/env python3
"""Recompute compact Space Shuttle evidence from the retained fresh-state harness runs.

ROM bytes, NVRAM and raw traces stay outside Git. A diagnostic number is read
from the ROM's own seven-segment response, never from host switch readback.
Every claim the definition makes from these runs is checked here and the
summary refuses to build when a run does not support it.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json
from build_external_evidence_manifest import check_manifest
import space_shuttle_data as data

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
	"sshtl_l7": Path("evidence/runtime/williams/space-shuttle-l7-diagnostics-and-gameplay.json"),
	"sshtl_l3": Path("evidence/runtime/williams/space-shuttle-l3-solenoid-test.json"),
}
SCENARIOS = Path("tools/harness-scenarios/system-11")
# run folder: (game, scenario file)
RUNS = {
	"solenoid-test-l7": ("sshtl_l7", "space-shuttle-l7-solenoid-test.json"),
	"switch-test-l7": ("sshtl_l7", "space-shuttle-l7-switch-test.json"),
	"gameplay-l7": ("sshtl_l7", "space-shuttle-l7-gameplay.json"),
	"credit-award-l7": ("sshtl_l7", "space-shuttle-l7-credit-award.json"),
	"solenoid-test-l3": ("sshtl_l3", "space-shuttle-l3-solenoid-test.json"),
}
INIT_SCENARIO = {"sshtl_l7": "space-shuttle-l7-nvram-init-boot.json", "sshtl_l3": "space-shuttle-l3-nvram-init-boot.json"}
MANIFEST_NAME = "space-shuttle"
DIGITS = {0: " ", 0x3F: "0", 6: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 7: "7", 0x7F: "8", 0x6F: "9"}
# LibPinMAME display indices for dispSshtl: 0-3 are players 1-4 (segment starts 21, 29, 1, 9),
# 4 and 5 the credit digits, 6 and 7 the ball-in-play / match digits.
PLAYER_1, CREDIT, MATCH = (0,), (4, 5), (6, 7)


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def digits(segments: list[int]) -> str:
	return "".join(DIGITS.get(value & 0x7F, "?") for value in segments)


def display_text(snapshot: dict, indices: tuple[int, ...]) -> str:
	by_index = {d["index"]: d for d in snapshot["displays"] if "segments" in d}
	return "".join(digits(by_index[i]["segments"]) for i in indices)


def responses(snapshot: dict, indices: tuple[int, ...], diagnostic_address: int | None = None) -> list[dict]:
	by_index = {d["index"]: d for d in snapshot["displays"] if "segments" in d}
	rows = []
	for index in indices:
		row = {"snapshot_label": snapshot["label"], "display_index": index, "segments": by_index[index]["segments"],
		       "decoded_segment_positions": list(range(len(by_index[index]["segments"]))),
		       "interpreted_text": digits(by_index[index]["segments"])}
		if diagnostic_address is not None:
			row["diagnostic_address"] = diagnostic_address
		rows.append(row)
	return rows


def step_snapshots(run: dict) -> list[dict]:
	"""One snapshot after boot, then one per step in order; step labels may repeat."""
	snapshots = [s for s in run["snapshots"] if not s["label"].endswith(" (held)")][1:]
	if len(snapshots) != len(run["steps"]) or any(s["label"] != st["label"] for s, st in zip(snapshots, run["steps"])):
		raise RuntimeError("Snapshots do not pair one-to-one with steps")
	return snapshots


def turned_on(step: dict) -> list[int]:
	return sorted({t["number"] for t in step["transitions"]["solenoids"] if 1 in t["states"]})


def transitioned(step: dict) -> list[int]:
	return sorted({t["number"] for t in step["transitions"]["solenoids"]})


def seen(run: dict) -> list[int]:
	return sorted({e["number"] for e in run["events"] if e["event"] == "solenoid"})


def action(step: dict, snapshot: dict, display: list[dict] | None = None, held: dict | None = None) -> dict:
	row = {"label": step["label"], "input_kind": "switch", "input_address": step["switch"],
	       "observed_switch_addresses": [], "host_stimulus_switch_addresses": [step["switch"]],
	       "active_solenoid_addresses": sorted((held or snapshot)["active_solenoids"]),
	       "transitioned_solenoid_addresses": transitioned(step),
	       "result": "observed" if transitioned(step) or display else "no_matching_transition"}
	if display:
		row["display_responses"] = display
	return row


def solenoid_test(run: dict, name: str) -> tuple[list[dict], dict[str, int]]:
	actions, mapping = [], {}
	held = False
	for step, snapshot in zip(run["steps"], step_snapshots(run)):
		if step["label"].startswith("Manual-Down: hold"):
			held = True
		if not held:
			continue
		if display_text(snapshot, CREDIT) != "02":
			raise RuntimeError(f"{name}: left Test 02 at step {step['step']}")
		shown = display_text(snapshot, MATCH)
		if not shown.isdigit():
			raise RuntimeError(f"{name}: unreadable step number {shown!r}")
		number = int(shown)
		pulsed = turned_on(step)
		if number not in pulsed or any(s not in (number - 1, number + 1) for s in pulsed if s != number):
			raise RuntimeError(f"{name}: step {shown} pulsed {pulsed}")
		mapping[str(number)] = number
		actions.append(action(step, snapshot, responses(snapshot, MATCH)))
	if sorted(mapping.values()) != list(range(1, 17)):
		raise RuntimeError(f"{name}: solenoid test did not step exactly 01-16")
	if any(s in data.UNUSED_SOLENOIDS - {12} or s in range(17, 23) for s in seen(run)):
		raise RuntimeError(f"{name}: solenoid test drove a special or an unscanned output")
	return actions, mapping


def switch_test(run: dict) -> list[dict]:
	snapshots = {s["label"]: s for s in run["snapshots"] if s["label"].endswith(" (held)")}
	actions = []
	for step in run["steps"]:
		if step.get("type") != "pulse" or step.get("switch", 0) < 1:
			continue
		held = snapshots[step["label"] + " (held)"]
		if display_text(held, CREDIT) != "03":
			raise RuntimeError(f"Switch test left Test 03 at {step['label']!r}")
		address = step["switch"]
		shown = display_text(held, MATCH).strip()
		if address in data.SWITCHES and shown != f"{address:02d}":
			raise RuntimeError(f"Switch test did not name {address}: {shown!r}")
		if address in data.UNUSED_SWITCHES and shown:
			raise RuntimeError(f"Switch test named unscanned {address}: {shown!r}")
		specials = sorted(set(held["active_solenoids"]) & set(range(17, 23)))
		expected = [data.PINMAME_SPECIAL_SWITCH_SOLENOIDS[address]] if address in data.PINMAME_SPECIAL_SWITCH_SOLENOIDS else []
		if specials != expected:
			raise RuntimeError(f"Switch {address} drove specials {specials}")
		actions.append(action(step, held, responses(held, MATCH, address), held))
	if [r["input_address"] for r in actions] != list(range(1, 65)):
		raise RuntimeError("Switch test sweep is incomplete")
	return actions


def require(condition: bool, message: str) -> None:
	if not condition:
		raise RuntimeError("Space Shuttle gameplay claim not supported by the run: " + message)


def solenoid_times(run: dict, number: int) -> list[float]:
	return [e["time_s"] for e in run["events"] if e["event"] == "solenoid" and e["number"] == number and e["state"] == 1]


def gameplay(run: dict) -> list[dict]:
	held = {s["label"]: s for s in run["snapshots"] if s["label"].endswith(" (held)")}
	steps = {st["label"]: st for st in run["steps"]}
	snaps = {st["label"]: snap for st, snap in zip(run["steps"], step_snapshots(run))}
	require(transitioned(steps["observe attract mode with three balls home"]) == [], "attract mode drives no solenoid")
	require({5, 6, 8, 23} <= set(turned_on(steps["credit button: start a one-player game"])), "game start resets the T drop target (5) and the 3-bank (6), lowers the post (8) and enables 23")
	require(2 in turned_on(steps["ROM serves a ball with the ball-ramp release (2)"]), "the ROM serves with the ball-ramp release (2)")
	for switch, coil in data.PINMAME_SPECIAL_SWITCH_SOLENOIDS.items():
		require(any(st.get("switch") == switch and coil in turned_on(st) for st in run["steps"]), f"switch {switch} fires special {coil}")
	right = held["right flipper button (flipper column 82) (held)"]
	left = held["left flipper button (flipper column 84) (held)"]
	watched = lambda snap: {w["number"]: w["state"] for w in snap["watched_switches"] if w["number"] in (41, 82, 84)}
	require(watched(right) == {41: 1, 82: 1, 84: 0} and {45, 46} <= set(right["active_solenoids"]), "82 copies into 41 and fabricates 45/46")
	require(watched(left) == {41: 0, 82: 0, 84: 1} and {47, 48} <= set(left["active_solenoids"]), "84 fabricates 47/48 and leaves 41")
	require(13 in turned_on(steps["right outlane rollover"]) and 13 in snaps["3-bank: right drop target down, bank complete"]["active_solenoids"], "the right outlane rollover energizes the gate (13) and it stays held")
	require(6 in turned_on(steps["ROM resets the 3-bank (6)"]), "completing the 3-bank resets it (6)")
	require(13 not in snaps["3-bank reset: right target up"]["active_solenoids"], "the gate (13) is released after the 3-bank is completed")
	require(5 in turned_on(steps["ROM resets the T drop target (5)"]), "the ramp bull's-eye after the T target resets the T drop target (5)")
	for label in ("ROM serves the second ball with the ball-ramp release (2)", "ROM serves the third ball with the ball-ramp release (2)"):
		require(2 in turned_on(steps[label]) and {9, 10, 14} <= set(turned_on(steps[label])), f"a locked ball makes the ROM serve the next ball (2) and flash 9, 10 and 14: {label}")
	require(7 in turned_on(steps["long ramp upper switch: multi-ball release shot"]), "the long ramp shot raises the post (7)")
	eject_3, eject_4 = solenoid_times(run, 3), solenoid_times(run, 4)
	require(len(eject_4) == 1 and eject_3 and 2.0 < eject_4[0] - eject_3[0] < 4.0, "the left eject (3) fires first and the right eject (4) about 3 s later")
	require(8 in turned_on(steps["left flipper return lane"]), "the left return lane lowers the post (8)")
	for label in ("ROM kicks the outhole (1)", "ROM kicks the outhole (1) again", "ROM kicks the outhole (1) a third time"):
		require(1 in turned_on(steps[label]), f"each outhole closure kicks (1): {label}")
	require(2 in turned_on(steps["ROM serves ball 2 with the ball-ramp release (2)"]) and display_text(snaps["ball 2 plunged"], MATCH).strip() == "2", "the ROM serves ball 2 after all three balls drain")
	for label in ("playfield tilt closure 1", "playfield tilt closure 2"):
		require(23 in snaps[label]["active_solenoids"], f"{label} does not yet tilt")
	tilt = {t["number"]: t["states"] for t in steps["playfield tilt closure 3"]["transitions"]["solenoids"]}
	require(tilt.get(23) == [0] and 11 in snaps["playfield tilt closure 3"]["active_solenoids"], "the third playfield-tilt closure tilts: 23 drops and the GI relay (11) turns the GI off")
	require(not (set(seen(run)) & data.UNUSED_SOLENOIDS), "gameplay drives no unfitted solenoid")
	actions = []
	for step, snapshot in zip(run["steps"], step_snapshots(run)):
		if "switch" not in step:
			continue
		snap = held.get(step["label"] + " (held)")
		row = action(step, snapshot, held=snap)
		if snap is not None:
			row["held_synthetic_solenoid_addresses"] = sorted(set(snap["active_solenoids"]) & {45, 46, 47, 48})
		actions.append(row)
	return actions


def credit_award(run: dict) -> list[dict]:
	snapshots = step_snapshots(run)
	credits = [display_text(s, CREDIT) for s in snapshots]
	changes = [i for i in range(1, len(credits)) if credits[i] != credits[i - 1] and run["steps"][i].get("switch") in (32, 45)]
	if len(changes) != 1 or credits[changes[0] - 1] != "00" or credits[changes[0]] != "01":
		raise RuntimeError(f"Credit-award run: expected one credit 00 -> 01 during the ramp shots, got {changes}")
	award = run["steps"][changes[0]]
	if 15 not in turned_on(award):
		raise RuntimeError("Credit-award run: the bell did not ring with the award")
	if set(seen(run)) & data.UNUSED_SOLENOIDS:
		raise RuntimeError("Credit-award run: an output the manual prints Not Used moved")
	return [action(award, snapshots[changes[0]], responses(snapshots[changes[0]], CREDIT))]


def raw_run(runs_root: Path, name: str, game: str, scenario_name: str, run: dict) -> dict:
	scenario_path = ROOT / SCENARIOS / scenario_name
	init_path = ROOT / SCENARIOS / INIT_SCENARIO[game]
	init = load_json(runs_root / name / "init.json")
	for label, value, scenario in (("run", run, scenario_path), ("init", init, init_path)):
		if value["failure"] is not None or value["game"] != game or value["library_sha256"] != data.LIBRARY_SHA256:
			raise RuntimeError(f"Unsuccessful or unpinned Space Shuttle {label}: {name}")
		if value["handle_mechanics"] != 0 or value["scenario"]["sha256"] != sha256(scenario):
			raise RuntimeError(f"Unexpected mechanism model or scenario drift: {name} {label}")
	scenario = load_json(scenario_path)
	return {
		"name": name, "sha256": sha256(runs_root / name / "run.json"), "retained_from": f"{name}/run.json",
		"scenario_path": (SCENARIOS / scenario_name).as_posix(), "scenario_sha256": sha256(scenario_path),
		"action_count": len(scenario["actions"]), "watch_switches": scenario["watch_switches"],
		"self_test_pulses": sum(a.get("switch") == -7 for a in scenario["actions"]),
		"nvram_initialization": f"A newly created state directory initialized by one 20 s empty-CMOS power-up ({name}/init.json, SHA-256 {sha256(runs_root / name / 'init.json')}, scenario {(SCENARIOS / INIT_SCENARIO[game]).as_posix()} SHA-256 {sha256(init_path)}); no state from any other run.",
		"snapshot_count": len(run["snapshots"]), "initial_switches": [],
	}


def envelope(game: str, manifest_digest: str, raw_runs: list[dict], observations: dict) -> dict:
	return {
		"format": "pinmame-machine-evidence", "version": 1,
		"extractor": {"id": "tools/summarize_space_shuttle_runtime.py", "version": 1},
		"source": {
			"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": data.PINMAME_REVISION,
			"path": "external:pinmame-review-artifacts/space-shuttle-1984/harness", "sha256": manifest_digest,
			"license": "NOASSERTION", "quality": "validated",
			"attribution": "Locally generated from the user-authorized ROMs and pinned PinMAME; ROM bytes and mutable state remain external.",
			"manifest_algorithm": "tools/build_external_evidence_manifest.py: case-sensitive sorted relative POSIX paths, every file except root manifest.json and manifest.sha256; SHA-256 of the canonical manifest bytes.",
		},
		"driver_ids": [game], "machine_ids": [data.MACHINE_ID],
		"switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
		"runtime": {
			"game": game, "rom_archive_sha256": data.ROM_SHA256[game],
			"emulator": {"binary": "pinmame64.dll", "sha256": data.LIBRARY_SHA256, "built_from_revision": data.PINMAME_REVISION},
			"raw_runs": raw_runs,
			"command_template": f"python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-46e1a01a/Release/pinmame64.dll --game {game} --rom-path <authorized-read-only-ROM-root> --work-dir <new-state-directory> --scenario <init scenario> --output init.json, then the same command with the evidentiary scenario and --output run.json. Direct switch writes only: no keyboard handling, mechanics mask 0.",
			"observations": observations,
		},
	}


def build(runs_root: Path) -> dict[str, dict]:
	manifest_digest = check_manifest(runs_root, MANIFEST_NAME)
	runs = {name: load_json(runs_root / name / "run.json") for name in RUNS}
	raws = {name: raw_run(runs_root, name, game, scenario, runs[name]) for name, (game, scenario) in RUNS.items()}

	sol_l7, map_l7 = solenoid_test(runs["solenoid-test-l7"], "L-7")
	sol_l3, map_l3 = solenoid_test(runs["solenoid-test-l3"], "L-3")
	l7_runs = [n for n in RUNS if RUNS[n][0] == "sshtl_l7"]
	l7 = envelope("sshtl_l7", manifest_digest, [raws[n] for n in l7_runs], {
		"solenoid_addresses_seen": sorted(set().union(*(seen(runs[n]) for n in l7_runs))),
		"physical_service_solenoid_to_public": map_l7,
		"display_indices_seen": sorted({d["index"] for d in runs["gameplay-l7"]["snapshots"][-1]["displays"]}),
		"runs": {
			"solenoid-test-l7": {
				"named_action_observations": sol_l7, "solenoid_addresses_seen": seen(runs["solenoid-test-l7"]),
				"note": "Test 02 shows 02 in the credit display (indices 4-5); each Advance steps the ball-in-play display (indices 6-7) through 01-16 and wraps to 01, and the shown step pulses the same public solenoid, so the manual's printed solenoid numbers are the public addresses. The sweep includes 12, which the manual prints Not Used; the specials 17-22 are not stepped.",
				"limitation": "The manual's procedure says the display sequences 01 through 25 and that sub-test 25 de-energizes the flipper relay; this ROM steps 01-16 only, so the test does not exercise the game-on enable 23.",
			},
			"switch-test-l7": {
				"named_action_observations": switch_test(runs["switch-test-l7"]),
				"note": "Test 03: each isolated closure of public 1-49 shows its own number in the ball-in-play display (indices 6-7); 50-64 show nothing, so the ROM does not scan them. Closures of 39, 40, 27, 26 and 25 also publish specials 17, 18, 19, 20 and 21 (PinMAME sxx.ssSw while the enable 23 is set).",
			},
			"gameplay-l7": {
				"named_action_observations": gameplay(runs["gameplay-l7"]), "solenoid_addresses_seen": seen(runs["gameplay-l7"]),
				"note": "Direct-write game. No solenoid moves in 20 s of attract mode with three balls on the ball ramp. Start resets the T drop target (5) and the 3-bank (6), lowers the post (8), sets 23, and serves with the ball-ramp release (2). Specials follow PinMAME's switch table. Holding 82 sets 41 and 45/46; holding 84 sets 47/48 and leaves 41 at 0. The right outlane rollover energizes the gate (13), which stays held until the 3-bank is completed; completing the 3-bank resets it (6). The ramp bull's-eye after the T target resets the T drop target (5). A ball resting in either eject hole (16, 24) is locked and the ROM serves the next ball (2) with the space (9), shuttle (10) and insert (14) flash lamps. With both locked, the long-ramp shot (32) raises the post (7) and starts multi-ball: the left eject (3) fires at once and the right eject (4) about 3 s later. The left return lane lowers the post (8). Each outhole closure kicks 1, and after all three balls drain the ROM serves ball 2. Two playfield-tilt closures warn; the third tilts, dropping 23 and turning the GI off with 11. No output the manual prints Not Used (12, 22) moves.",
			},
			"credit-award-l7": {
				"named_action_observations": credit_award(runs["credit-award-l7"]), "solenoid_addresses_seen": seen(runs["credit-award-l7"]),
				"note": "Repeated long-ramp shots pass the factory first replay score: the credit display goes from 00 to 01 while the ROM rings the bell (15). The bell also rings with ordinary ramp scoring, so it is the game's only award sounder; no output the manual prints Not Used (12, 22) moves.",
			},
		},
	})
	l3 = envelope("sshtl_l3", manifest_digest, [raws["solenoid-test-l3"]], {
		"solenoid_addresses_seen": seen(runs["solenoid-test-l3"]),
		"physical_service_solenoid_to_public": map_l3,
		"runs": {"solenoid-test-l3": {
			"named_action_observations": sol_l3,
			"note": "The L-3 ROM's Test 02 steps the identical 01-16 sequence, the shown step pulsing the same public solenoid.",
		}},
	})
	return {"sshtl_l7": l7, "sshtl_l3": l3}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--runs", type=Path, required=True)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	args = parser.parse_args()
	results = build(args.runs)
	for game, result in results.items():
		if args.write:
			write_json(ROOT / OUTPUTS[game], result)
		elif (ROOT / OUTPUTS[game]).read_bytes() != canonical_bytes(result):
			raise RuntimeError(f"Space Shuttle runtime evidence for {game} drifted from the retained runs")
	print("Space Shuttle runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
