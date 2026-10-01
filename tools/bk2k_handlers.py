"""Per-run observation builders for the Black Knight 2000 compact evidence (used by bk2k_summarize_runtime_evidence.py)."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import bk2k_analysis as A
import bk2k_lib as L

FLASH_GROUP = (9, 10, 11, 12, 25, 26, 27, 28, 29, 30, 31, 32)


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def name_table(driver: str) -> dict[str, Any]:
	return json.loads((L.stage_root() / "rom-name-tables" / f"{driver}.json").read_text(encoding="utf-8"))


def checkpoint(run: dict[str, Any], text: str) -> dict[str, Any]:
	step = next(s for s in run["steps"] if s["type"] == "pulse_until_display" and s["matched_text"] == text)
	return {"matched_text": text, "after_service_pulses": step["pulses"]}


def compact_list(values: list[int]) -> str:
	return ", ".join(str(v) for v in values) if values else "none"


def switch_observation(driver: str, run: dict[str, Any], title: str) -> tuple[dict[str, Any], dict[str, Any]]:
	entries = name_table(driver)["switch_table"]["entries"]
	sweep = A.switch_sweep(run, entries, title)
	rows = sweep["rows"]
	responses = A.switch_responses(run, rows, title)
	idle = A.step_by_label(run, "idle observation with every switch at 0")
	idle_window = A.switch_window(run, idle["_start"], idle["_end"], title)
	named_actions = []
	for row in rows:
		address = row["address"]
		item: dict[str, Any] = {
			"label": f"switch {address} written to 1 in the {title.title()} test: ROM reaction {row['reaction'].replace('_', ' ')}",
			"input_kind": "switch",
			"input_address": address,
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [address],
			"result": "observed" if row["reaction"] != "none" else "no_matching_transition",
		}
		response = responses.get(address)
		if response:
			displays = []
			if response["d0"]:
				displays.append({"snapshot_label": row["label"], "display_index": 0, "segments": response["d0"]["segments"], "decoded_segment_positions": list(range(16)), "interpreted_text": response["d0"]["text"]})
			if response["d1"]:
				digits = L.decode_digits(response["d1"]["segments"], (4, 5)).strip()
				displays.append({"snapshot_label": row["label"], "display_index": 1, "segments": response["d1"]["segments"], "decoded_segment_positions": [4, 5], "interpreted_text": digits, "diagnostic_address": int(digits)})
			if displays:
				item["display_responses"] = displays
		named_actions.append(item)
	by_reaction = {kind: [r["address"] for r in rows if r["reaction"] == kind] for kind in ("name_and_number", "number_only", "none")}
	mismatches = [r["address"] for r in rows if r["reaction"] != "none" and (r["name_equals_rom_table"] is False or r["number_equals_address"] is False)]
	not_back = [r["address"] for r in rows if not r["back_to_title_after_return_to_0"]]
	control_names = sorted({name for c in sweep["controls"] for name in c["names_while_1"]})
	note = (
		f"{title.title()} test reached after {checkpoint(run, title)['after_service_pulses']} Advance pulses. Idle window with every switch at 0: "
		f"{'title only, no switch named' if idle_window['title_only'] else 'NOT title only'}. Each address was written to 1 for 1.5 s and then back to 0 for 1.0 s, one address per step. "
		f"Name and number shown: {compact_list(by_reaction['name_and_number'])}. Number shown with a blank name line: {compact_list(by_reaction['number_only'])}. No reaction: {compact_list(by_reaction['none'])}. "
		f"Addresses whose shown number differs from the address or whose shown name differs from the ROM name table (82 and 84 show the copied matrix switches 57 and 58): {compact_list(mismatches)}. "
		f"Control 39 ({len(sweep['controls'])} stimulations) always named {control_names}. Title back as the last stable frame within the 1.0 s after returning to 0 for every address except: {compact_list(not_back)}."
	)
	obs = {
		"diagnostic_checkpoints": [checkpoint(run, title)],
		"named_action_observations": named_actions,
		"note": note,
		"limitation": (
			"Host writes to public switches only: the ROM names a switch while the matrix scan reads it closed (Switch Levels) or for about 1.5 s after the closing edge (Switch Edges); the release edge draws nothing. "
			"Addresses 57 and 58 are rewritten from the flipper switch column every update (FLIP_SWNO(58,57)), so a direct write is at most a one-frame blip and is not a usable input; 82 and 84 are the consumer inputs. "
			"Address 2 is overwritten with the A/C relay state (S11_MUXSW2). A level-1 reaction says which public level the ROM reads as active, not what physical event closes the contact."
		),
	}
	analysis = {"idle_window": idle_window, "rows": rows, "controls": sweep["controls"], "by_reaction": by_reaction}
	return obs, analysis


def lamp_observation(run: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, int], list[int]]:
	rows = A.single_lamps(run)
	bad = [r["step"] for r in rows if r["blinking_lamps"] != [r["step"]] or r["d1_step"] != f"{r['step']:02d}" or r["d1_test"] != "04" or len(r["names"]) != 1]
	if bad:
		raise RuntimeError(f"single-lamp steps with inconsistent pairing: {bad}")
	named = {f"lamp-{r['step']:02d}-{slug(r['names'][0])}": r["step"] for r in rows}
	obs = {
		"diagnostic_checkpoints": [checkpoint(run, "SINGLE LAMPS")],
		"note": (
			"Single Lamps test (04) stepped with the Credit button (public 3), 64 steps; every step blinked exactly one public lamp whose number equals the step number shown on the player 3 line. step=name as drawn on the player 1/2 line: "
			+ "; ".join(f"{r['step']}={r['names'][0]}" for r in rows) + "."
		),
		"limitation": "Names are the display's stable text. The display draws the digit 0 as the letter O and the digit 5 as the letter S, so CENTER SOOOO reads as CENTER 50000; the ROM stores these lamp names as shared message fragments, not as a 16-byte table, so no name table was anchored in the ROM bytes.",
	}
	return obs, {"rows": rows}, named, [r["step"] for r in rows]


def boot_observation(run: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
	probe = A.boot_probe(run)
	parts = []
	for address, info in probe["solenoids"].items():
		spans = info["on_spans_s"]
		if info["pulse_count"] == 1:
			parts.append(f"{address}: one pulse {spans[0][0]}-{spans[0][1]} s")
		else:
			parts.append(f"{address}: {info['pulse_count']} pulses from {spans[0][0]} s to {spans[-1][0]} s, gaps {info['gaps_between_pulse_starts_s']}")
	obs = {
		"solenoid_addresses_seen": sorted(int(a) for a in probe["solenoids"]),
		"note": f"Power-up probe with switches {', '.join(f'{s}={v}' for s, v in probe['held_switches'])} held from emulator start; first {probe['window_s']} s. Solenoid on-spans: " + "; ".join(parts) + ".",
		"limitation": "Static host switches only; the harness never moves a ball or a mechanism, so repeated pulses are ROM retries against a host-held switch.",
	}
	return obs, probe


def motor_observation(run: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
	result = A.motor_bank(run)
	timeline = "; ".join(f"{item['t']:+.2f} s {item['what']}" for item in result["timeline"] if "display 0 shows ''" not in item["what"])
	obs = {
		"diagnostic_checkpoints": [checkpoint(run, "MOTOR BANK TEST")],
		"solenoid_addresses_seen": sorted({e["number"] for e in L.solenoid_events(run) if e["state"]}),
		"note": f"MOTOR BANK TEST (test 08), times relative to the title appearing: {timeline}.",
		"limitation": "Synthetic host stimulus on switches 16 (UP) and 24 (DOWN) at scripted times; no model of the bank's travel. The test is not described in the retained manual.",
	}
	return obs, result


def game_observation(run: dict[str, Any], stem: str) -> tuple[dict[str, Any], dict[str, Any]]:
	if stem.startswith("droptargets-"):
		phases = A.game_phases(run)
		start = A.step_by_label(run, "Start (Credit button)")["_start"]
		window = 25.0
		pulses = {}
		for address in (3, 4):
			pulses[address] = [round(e["time_s"] - start, 2) for e in L.solenoid_events(run, start, start + window) if e["number"] == address and e["state"]]
		attract_step = A.step_by_label(run, "observe attract mode")
		attract = A.phase_events(run, attract_step["_start"], attract_step["_end"])
		held = [f"{i['switch']}={i['state']}" for i in run["initial_switches"] if i["switch"] not in (-6, 11, 12, 13)]
		serves = sum(1 for e in L.solenoid_events(run, start, start + window) if e["number"] == 2 and e["state"])
		restart = next((round(e["time_s"] - start, 2) for e in L.display_events(run, 0) if e["time_s"] > start and "PRESS ADVANCE" in A.display_text(e)), None)
		drop_23 = next((round(b - start, 2) for b, end in L.solenoid_spans(run, 23, start) if end is not None for b in [end]), None)
		obs = {
			"solenoid_addresses_seen": sorted({e["number"] for e in L.solenoid_events(run) if e["state"]}),
			"note": (
				f"Auto-Up (-6 = 1) and trough 11-13 held at 1 from emulator start; target switches held at 1: {', '.join(held) or 'none'}. Attract mode (Game Over mode) observed 12 s: solenoids 3 and 4 fired "
				f"{attract['solenoid_on_counts'].get('3', 0)} and {attract['solenoid_on_counts'].get('4', 0)} time(s). Two coins (switch 4) then Start (switch 3). "
				f"In the first {window:.0f} s after Start the left 3-bank reset (3) pulsed {('at ' + str(pulses[3]) + ' s') if pulses[3] else 'never'} and the right 3-bank reset (4) {('at ' + str(pulses[4]) + ' s') if pulses[4] else 'never'} (times after the Start press). "
				f"Game-on enable (23) on-spans (absolute s): {phases['solenoid_23_spans_s']}. Ball serve (2) pulses in that window: {serves}. "
				f"Game-on enable dropped {('at ' + str(drop_23) + ' s') if drop_23 is not None else 'never'} after Start and the power-up message PRESS ADVANCE (ROM restart) {('first showed at ' + str(restart) + ' s') if restart is not None else 'never showed'} in the 30 s observed."
			),
			"limitation": "The harness never moves a ball or a drop target, so repeated resets are ROM retries against host-held switch states. The Auto-Up/Manual-Down switch (-6) is held at Auto-Up, the normal play position; at the harness default (Manual-Down) the ROM restarted itself into FACTORY SETTING 0.2-35 s after Start in earlier game-phase runs, which are superseded and not cited.",
		}
		return obs, {"phases": phases, "reset_pulses_after_start_s": {"3": pulses[3], "4": pulses[4]}, "window_s": window, "serves_in_window": serves, "game_on_dropped_after_start_s": drop_23, "restart_message_after_start_s": restart}
	steps = A.step_windows(run)
	start = A.step_by_label(run, "Start (Credit button)")["_start"]
	end = steps[-1]["_end"]
	table = [{"step": s["step"], "label": s["label"], "t_start_s": round(s["_start"] - start, 2), "t_end_s": round(s["_end"] - start, 2)} for s in steps]
	on = [[round(e["time_s"] - start, 2), e["number"]] for e in L.solenoid_events(run, start, end) if e["state"] and e["number"] not in FLASH_GROUP]
	flash = Counter(e["number"] for e in L.solenoid_events(run, start, end) if e["state"] and e["number"] in FLASH_GROUP)
	text = A.text_timeline(run, start, end, minimum=0.3, limit=30)
	obs = {
		"solenoid_addresses_seen": sorted({e["number"] for e in L.solenoid_events(run) if e["state"]}),
		"note": (
			"Host-scripted ball-handling probe (times in seconds after the Start press; steps: "
			+ "; ".join(f"{r['label']} {r['t_start_s']}..{r['t_end_s']}" for r in table if r["step"] > 4)
			+ f"). Solenoid on-events other than the relay/flasher/G.I. group, as [time, address]: {on}. Relay/flasher/G.I. group on-counts: {dict(sorted(flash.items()))}. Stable display text: "
			+ "; ".join(f"{r['t']} L{r['line']} {r['text']!r}" for r in text) + "."
		),
		"limitation": "Synthetic host script, not a ball model; the stimulus order and timing are the host's. The Auto-Up/Manual-Down switch (-6) is held at Auto-Up, the normal play position (at Manual-Down the ROM restarted itself into FACTORY SETTING during game phases).",
	}
	return obs, {"steps": table, "solenoid_on_events": on, "flash_group_counts": dict(sorted(flash.items())), "text_timeline": text}
