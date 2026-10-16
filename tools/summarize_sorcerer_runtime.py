#!/usr/bin/env python3
"""Recompute compact Sorcerer evidence from the retained fresh-state harness runs.

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
import sorcerer_data as data

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
	"sorcr_l2": Path("evidence/runtime/williams/sorcerer-l2-diagnostics-and-gameplay.json"),
	"sorcr_l1": Path("evidence/runtime/williams/sorcerer-l1-solenoid-test.json"),
}
SCENARIOS = Path("tools/harness-scenarios/system-11")
# run folder: (game, scenario file)
RUNS = {
	"solenoid-test-l2": ("sorcr_l2", "sorcerer-l2-solenoid-test.json"),
	"switch-test-l2": ("sorcr_l2", "sorcerer-l2-switch-test.json"),
	"gameplay-l2": ("sorcr_l2", "sorcerer-l2-gameplay.json"),
	"special-award-l2": ("sorcr_l2", "sorcerer-l2-special-award.json"),
	"solenoid-test-l1": ("sorcr_l1", "sorcerer-l1-solenoid-test.json"),
}
INIT_SCENARIO = {"sorcr_l2": "sorcerer-l2-nvram-init-boot.json", "sorcr_l1": "sorcerer-l1-nvram-init-boot.json"}
DIGITS = {0: " ", 0x3F: "0", 6: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 7: "7", 0x7F: "8", 0x6F: "9"}
# LibPinMAME display indices for s11_dispS9: 2 and 3 are players 1 and 2, 0 and 1 players 3 and 4,
# 4 and 5 the credit digits, 6 and 7 the ball-in-play / match digits.
CREDIT, MATCH = (4, 5), (6, 7)


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
		if address <= 45 and shown != f"{address:02d}":
			raise RuntimeError(f"Switch test did not name {address}: {shown!r}")
		if address > 45 and shown:
			raise RuntimeError(f"Switch test named unscanned {address}: {shown!r}")
		specials = sorted(set(held["active_solenoids"]) & set(range(17, 23)))
		expected = [data.SPECIAL_SWITCH_SOLENOIDS[address]] if address in data.SPECIAL_SWITCH_SOLENOIDS else []
		if specials != expected:
			raise RuntimeError(f"Switch {address} drove specials {specials}")
		actions.append(action(step, held, responses(held, MATCH, address), held))
	if [r["input_address"] for r in actions] != list(range(1, 65)):
		raise RuntimeError("Switch test sweep is incomplete")
	return actions


def require(condition: bool, message: str) -> None:
	if not condition:
		raise RuntimeError("Sorcerer gameplay claim not supported by the run: " + message)


def gameplay(run: dict) -> list[dict]:
	held = {s["label"]: s for s in run["snapshots"] if s["label"].endswith(" (held)")}
	steps = {st["label"]: st for st in run["steps"]}
	require(transitioned(steps["observe attract mode with both balls home"]) == [], "attract mode drives no solenoid")
	require({2, 4, 23} <= set(turned_on(steps["credit button: start a one-player game"])), "game start serves (2), resets the bank (4) and enables 23")
	for switch, coil in data.SPECIAL_SWITCH_SOLENOIDS.items():
		require(any(st.get("switch") == switch and coil in turned_on(st) for st in run["steps"]), f"switch {switch} fires special {coil}")
	right = held["right flipper button (flipper column 82) (held)"]
	left = held["left flipper button (flipper column 84) (held)"]
	watched = lambda snap: {w["number"]: w["state"] for w in snap["watched_switches"] if w["number"] in (44, 82, 84)}
	require(watched(right) == {44: 1, 82: 1, 84: 0} and {45, 46} <= set(right["active_solenoids"]), "82 copies into 44 and fabricates 45/46")
	require(watched(left) == {44: 0, 82: 0, 84: 1} and {47, 48} <= set(left["active_solenoids"]), "84 fabricates 47/48 and leaves 44")
	require({7, 8, 11} <= set(turned_on(steps["right spinner R"])), "completing SORCERER flashes 7 and 8 and blinks GI 11")
	require({4, 15} <= set(turned_on(steps["ROM resets the 3-bank (4)"])), "completing the 3-bank resets it (4) and rings the bell (15)")
	require({2, 5, 8} <= set(turned_on(steps["ROM serves the second ball with the ramp eject (2)"])), "a locked ball makes the ROM serve the next ball and flash 5 and 8")
	require(3 in turned_on(steps["ROM ejects the lock with the multi-ball eject (3)"]), "a second ball on the ramp switch fires the multi-ball eject (3)")
	require(1 in turned_on(steps["ROM kicks the outhole (1)"]) and 1 in turned_on(steps["ROM kicks the outhole (1) again"]), "each outhole closure kicks (1)")
	require(2 in turned_on(steps["ROM serves ball 2 with the ramp eject (2)"]), "the ROM serves ball 2 after both balls drain")
	tilt = {t["number"]: t["states"] for t in steps["playfield tilt closure 1"]["transitions"]["solenoids"]}
	require(tilt.get(23) == [0], "one playfield-tilt closure drops the game-on enable 23")
	flashes = [st for st in run["steps"] if any(t["number"] == 8 and len(t["states"]) >= 10 for t in st["transitions"]["solenoids"])]
	require(len(flashes) >= 3, "solenoid 8 flashes repeatedly with game effects")
	require(not ({e["number"] for e in run["events"] if e["event"] == "solenoid"} & data.UNUSED_SOLENOIDS), "gameplay drives no unfitted solenoid")
	demon_lamp_identities(run)
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


def demon_lamp_identities(run: dict) -> dict[str, int]:
	"""The lamp behaviour that settles the manual's swapped 22/23 names.

	The manual's rules: S-O-R-C-E-R-E-R lights DEMON; completing the 3-bank with DEMON lit spots BONUS HELD
	OVER, which holds over to the next ball. Returns the public lamps that behave as each.
	"""
	pairs = list(zip(run["steps"], step_snapshots(run)))
	index = {st["label"]: i for i, (st, _snap) in enumerate(pairs)}
	lit = lambda label: set(pairs[index[label]][1]["active_lamps"]) & {22, 23}
	turned = lambda label: {t["number"] for t in pairs[index[label]][0]["transitions"]["lamps"] if 1 in t["states"]} & {22, 23}
	require(lit("SORCERER target 15") == set(), "neither 22 nor 23 is lit before S-O-R-C-E-R-E-R is complete")
	require(turned("right spinner R") == {22} and lit("right spinner R") == {22}, "completing S-O-R-C-E-R-E-R lights lamp 22 and not 23")
	require(lit("3-bank: right drop target down, bank complete") == {22}, "lamp 22 stays lit until the 3-bank is completed")
	require(23 in turned("ROM resets the 3-bank (4)") and lit("3-bank reset: right target up") == {23}, "completing the 3-bank with 22 lit clears 22 and lights 23")
	require(23 in turned("ball 2 plunged") and lit("ball 2 plunged") == {23}, "lamp 23 is lit into the next ball while 22 is not")
	return {"demon-lamp": 22, "bonus-hold-over-lamp": 23}


def special_award(run: dict) -> list[dict]:
	snapshots = step_snapshots(run)
	credits = [display_text(s, CREDIT) for s in snapshots]
	award = [st for st in run["steps"] if any(t["number"] == 14 for t in st["transitions"]["solenoids"])]
	unfitted = sorted({e["number"] for e in run["events"] if e["event"] == "solenoid" and e["number"] in data.UNUSED_SOLENOIDS})
	pulses = [e for e in run["events"] if e["event"] == "solenoid" and e["number"] == 14 and e["state"] == 1]
	releases = [e for e in run["events"] if e["event"] == "solenoid" and e["number"] == 14 and e["state"] == 0]
	if len(award) != 1 or len(pulses) != 1 or unfitted != [14]:
		raise RuntimeError(f"Special-award run: expected one solenoid-14 pulse and no other unfitted output, got {unfitted}")
	if len(releases) != 1 or not 0 < releases[0]["time_s"] - pulses[0]["time_s"] <= 0.25:
		raise RuntimeError("Special-award run: solenoid 14 must release once, within 0.25 s of its pulse")
	index = run["steps"].index(award[0])
	if credits[index - 1] != "00" or credits[index] != "01":
		raise RuntimeError(f"Special-award run: the credit display did not go from 00 to 01 at the award: {credits[index - 1:index + 1]}")
	if 15 not in turned_on(award[0]):
		raise RuntimeError("Special-award run: the bell did not ring with the award")
	return [action(award[0], snapshots[index], responses(snapshots[index], CREDIT))]


def raw_run(runs_root: Path, name: str, game: str, scenario_name: str, run: dict) -> dict:
	scenario_path = ROOT / SCENARIOS / scenario_name
	init_path = ROOT / SCENARIOS / INIT_SCENARIO[game]
	init = load_json(runs_root / name / "init.json")
	for label, value, scenario in (("run", run, scenario_path), ("init", init, init_path)):
		if value["failure"] is not None or value["game"] != game or value["library_sha256"] != data.LIBRARY_SHA256:
			raise RuntimeError(f"Unsuccessful or unpinned Sorcerer {label}: {name}")
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
		"extractor": {"id": "tools/summarize_sorcerer_runtime.py", "version": 1},
		"source": {
			"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": data.PINMAME_REVISION,
			"path": f"external:pinmame-review-artifacts/{data.MACHINE_ID}/harness", "sha256": manifest_digest,
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
			"command_template": f"python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-97aa922/Release/pinmame64.dll --game {game} --rom-path <authorized-read-only-ROM-root> --work-dir <new-state-directory> --scenario <init scenario> --output init.json, then the same command with the evidentiary scenario and --output run.json. Direct switch writes only: no keyboard handling, mechanics mask 0.",
			"observations": observations,
		},
	}


def build(runs_root: Path) -> dict[str, dict]:
	manifest_digest = check_manifest(runs_root, "sorcerer")
	runs = {name: load_json(runs_root / name / "run.json") for name in RUNS}
	raws = {name: raw_run(runs_root, name, game, scenario, runs[name]) for name, (game, scenario) in RUNS.items()}

	sol_l2, map_l2 = solenoid_test(runs["solenoid-test-l2"], "L-2")
	sol_l1, map_l1 = solenoid_test(runs["solenoid-test-l1"], "L-1")
	l2_runs = [n for n in RUNS if RUNS[n][0] == "sorcr_l2"]
	l2 = envelope("sorcr_l2", manifest_digest, [raws[n] for n in l2_runs], {
		"solenoid_addresses_seen": sorted(set().union(*(seen(runs[n]) for n in l2_runs))),
		"physical_service_solenoid_to_public": map_l2,
		"named_output_addresses": demon_lamp_identities(runs["gameplay-l2"]),
		"display_indices_seen": sorted({d["index"] for d in runs["gameplay-l2"]["snapshots"][-1]["displays"]}),
		"runs": {
			"solenoid-test-l2": {
				"named_action_observations": sol_l2, "solenoid_addresses_seen": seen(runs["solenoid-test-l2"]),
				"note": "Test 02 shows 02 in the credit display (indices 4-5); each Advance steps the match display (indices 6-7) through 01-16 and wraps to 01, and the shown step pulses the same public solenoid, so the manual's printed solenoid numbers are the public addresses. The specials 17-22 are not stepped.",
				"limitation": "The manual's procedure says the match display sequences 01 through 25 and that sub-test 25 de-energizes the flipper relay; this ROM steps 01-16 only, so the test does not exercise the game-on enable 23.",
			},
			"switch-test-l2": {
				"named_action_observations": switch_test(runs["switch-test-l2"]),
				"note": "Test 03: each isolated closure of public 1-45 shows its own number in the ball-in-play display (indices 6-7), including the unfitted 41; 46-64 show nothing, so the ROM does not scan them. Closures of 21, 22, 23, 32 and 33 also publish specials 19, 20, 21, 17 and 18 (PinMAME sxx.ssSw while the enable 23 is set).",
			},
			"gameplay-l2": {
				"named_action_observations": gameplay(runs["gameplay-l2"]), "solenoid_addresses_seen": seen(runs["gameplay-l2"]),
				"note": "Direct-write game. No solenoid moves in 40 s of attract mode. Start serves with 2, resets the 3-bank with 4 and sets 23. Specials follow their switches. Holding 82 sets 44 and 45/46; holding 84 sets 47/48 and leaves 44 at 0. Completing SORCERER flashes 7 and 8 and blinks GI 11; completing the 3-bank resets it (4) and rings the bell (15). A ball resting in the lock (37) makes the ROM serve the next ball (2) with flashers 5 and 8; a second ball resting on the ramp switch (38) fires the multi-ball eject (3). Each outhole closure kicks 1, and after both balls drain the ROM serves ball 2. One playfield-tilt closure drops 23. Lamp 22 is dark until S-O-R-C-E-R-E-R is complete, then lit until the 3-bank is completed, which clears it and lights lamp 23, still lit while ball 2 is in play: by the manual's rules 22 behaves as DEMON and 23 as BONUS HELD OVER (named_output_addresses). Solenoid 8 flashes with game effects and is never held through play. No output the manual prints Not Used moves.",
			},
			"special-award-l2": {
				"named_action_observations": special_award(runs["special-award-l2"]), "solenoid_addresses_seen": seen(runs["special-award-l2"]),
				"note": "The third S-O-R-C-E-R-E-R spelling awards a credit: the credit display goes from 00 to 01 while the ROM rings the bell (15) and pulses solenoid 14 once for about 0.1 s, the knocker routine. No other output the manual prints Not Used (9, 10, 12, 13, 22) moves.",
			},
		},
	})
	l1 = envelope("sorcr_l1", manifest_digest, [raws["solenoid-test-l1"]], {
		"solenoid_addresses_seen": seen(runs["solenoid-test-l1"]),
		"physical_service_solenoid_to_public": map_l1,
		"runs": {"solenoid-test-l1": {
			"named_action_observations": sol_l1,
			"note": "The L-1 ROM's Test 02 steps the identical 01-16 sequence, the shown step pulsing the same public solenoid.",
		}},
	})
	return {"sorcr_l2": l2, "sorcr_l1": l1}


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
			raise RuntimeError(f"Sorcerer runtime evidence for {game} drifted from the retained runs")
	print("Sorcerer runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
