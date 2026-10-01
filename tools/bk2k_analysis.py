"""Deterministic analyses of retained Black Knight 2000 harness runs (no emulator is started here).

Each function takes a parsed raw run (``pinmame-harness-run`` JSON) and returns plain data. They are used both by
``bk2k_summarize_runtime_evidence.py`` (compact evidence) and by the REPORT tables, so the report cannot drift from
the runs.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

import bk2k_lib as L

RELAY_AC = 12
SWITCH_TABLE_ENTRIES = 59
GAME_ON_ENABLE = 23


def display_text(event: dict[str, Any]) -> str:
	return L.normalize(L.decode_alpha(event["segments"]))


def first_display_time(run: dict[str, Any], needle: str, index: int = 0) -> float | None:
	for event in L.display_events(run, index):
		if needle in display_text(event):
			return event["time_s"]
	return None


def relay_state_at(run: dict[str, Any], time_s: float) -> int:
	state = 0
	for event in L.solenoid_events(run, 0.0, time_s):
		if event["number"] == RELAY_AC:
			state = event["state"]
	return state


def coil_pulses(run: dict[str, Any], start: float, end: float = float("inf")) -> list[dict[str, Any]]:
	"""Ordered on-events of the coil test. Relay 12 selecting the C side directly before a C-side output is not a step of its own."""
	window = [event for event in L.solenoid_events(run, start, end) if event["state"]]
	pulses = []
	for index, event in enumerate(window):
		if event["number"] == RELAY_AC:
			following = [other for other in window[index + 1:] if other["time_s"] - event["time_s"] < 0.4]
			if any(25 <= other["number"] <= 32 for other in following):
				continue
		if event["number"] == GAME_ON_ENABLE:
			continue
		pulses.append({"time_s": event["time_s"], "address": event["number"]})
	return pulses


def coil_test(run: dict[str, Any], coil_names: list[str], title: str = "COIL TEST") -> dict[str, Any]:
	"""Pair the coil table (ROM order) with the pulses of the first complete coil-test cycle and verify every later cycle repeats it."""
	start = first_display_time(run, title)
	if start is None:
		raise RuntimeError(f"{title} never displayed")
	pulses = coil_pulses(run, start)
	count = len(coil_names)
	cycles = [pulses[offset:offset + count] for offset in range(0, len(pulses) - count + 1, count)]
	if not cycles:
		raise RuntimeError("no complete coil-test cycle")
	first = cycles[0]
	repeats = all([p["address"] for p in cycle] == [p["address"] for p in first] for cycle in cycles)
	d0 = L.display_events(run, 0)
	d1 = L.display_events(run, 1)
	pairs = []
	for step, (pulse, name) in enumerate(zip(first, coil_names), start=1):
		t = pulse["time_s"]
		shown = [display_text(event) for event in d0 if t - 1.2 <= event["time_s"] <= t + 0.1]
		match = next((text for text in reversed(shown) if text == L.normalize(name)), None)
		if match is None:
			raise RuntimeError(f"coil-test step {step} (address {pulse['address']}) never displayed the ROM name {name!r}; saw {shown[-4:]}")
		labels = [L.coil_step_label(event["segments"]) for event in d1 if t - 1.2 <= event["time_s"] <= t + 0.1]
		labels = [label for label in labels if label["test_id"] == "05" and label["step"].strip().isdigit()]
		label = labels[-1] if labels else None
		off = next((event["time_s"] for event in L.solenoid_events(run, t) if event["number"] == pulse["address"] and not event["state"]), None)
		pairs.append({
			"step": step,
			"address": pulse["address"],
			"rom_name": name,
			"displayed": match,
			"display_step": label["step"] if label else None,
			"display_side": label["side_text"] if label else None,
			"relay_12_on_at_pulse": relay_state_at(run, t + 0.001),
			"pulse_start_s": round(t, 3),
			"pulse_length_s": round(off - t, 3) if off is not None else None,
		})
	extra = sorted({event["number"] for event in L.solenoid_events(run, start) if event["state"]} - {pair["address"] for pair in pairs} - {GAME_ON_ENABLE})
	return {
		"start_s": round(start, 3),
		"pairs": pairs,
		"cycle_count": len(cycles),
		"cycles_identical": repeats,
		"cycle_period_s": round(cycles[1][0]["time_s"] - first[0]["time_s"], 3) if len(cycles) > 1 else None,
		"addresses_in_window_not_in_pairing": extra,
	}


def solenoid_summary(run: dict[str, Any]) -> dict[str, Any]:
	on = Counter(event["number"] for event in L.solenoid_events(run) if event["state"])
	return {"seen": sorted(on), "on_counts": {str(a): on[a] for a in sorted(on)}}


def boot_pulses(run: dict[str, Any], until: float = 12.0) -> list[dict[str, Any]]:
	"""Solenoid on-spans in the first ``until`` seconds after emulator start (the ROM's own power-up behaviour)."""
	rows = []
	for number in sorted({event["number"] for event in L.solenoid_events(run, 0.0, until)}):
		for begin, end in L.solenoid_spans(run, number, 0.0, until):
			rows.append({"address": number, "on_s": round(begin, 3), "off_s": round(end, 3) if end is not None else None})
	return sorted(rows, key=lambda row: row["on_s"])


def step_windows(run: dict[str, Any]) -> list[dict[str, Any]]:
	"""Per-step [_start, _end) windows from the harness snapshots: snapshot 0 is the booted state, snapshot k is taken right after step k."""
	snapshots = run["snapshots"]
	steps = []
	for step in run["steps"]:
		k = step["step"]
		steps.append({**step, "_start": snapshots[k - 1]["time_s"], "_end": snapshots[k]["time_s"]})
	return steps


def single_lamps(run: dict[str, Any]) -> list[dict[str, Any]]:
	"""Pair every Single Lamps step with the ROM's lamp name (display 0, stable frames), the step number (display 1) and the lamp addresses that blinked."""
	start = first_display_time(run, "SINGLE LAMPS")
	if start is None:
		raise RuntimeError("SINGLE LAMPS never displayed")
	boundaries = []
	for s in step_windows(run):
		if s["label"].startswith("single lamp step 1"):
			boundaries.append((1, start, s["_end"]))
		elif s["label"].startswith("Credit press to single lamp step"):
			boundaries.append((int(s["label"].rsplit(" ", 1)[1]), s["_start"], s["_end"]))
	boundaries.sort()
	rows = []
	for number, begin, end in boundaries:
		d0 = [f["text"] for f in stable_frames(run, 0, begin, end)]
		d1 = stable_frames(run, 1, begin, end)
		names = []
		for text in d0:
			if text and "SINGLE LAMPS" not in text and text not in names:
				names.append(text)
		d1_last = d1[-1]["segments"] if d1 else None
		on = {}
		for event in L.lamp_events(run, begin, end):
			if event["state"]:
				on[event["number"]] = on.get(event["number"], 0) + 1
		rows.append({
			"step": number,
			"window_s": [round(begin, 3), round(end, 3)],
			"names": names,
			"d1_test": L.decode_digits(d1_last, (1, 2)) if d1_last else None,
			"d1_step": L.decode_digits(d1_last, (4, 5)) if d1_last else None,
			"lamps_on_events": {str(k): v for k, v in sorted(on.items())},
			"blinking_lamps": sorted(k for k, v in on.items() if v >= 3),
		})
	return rows


BLANK = ""


def stable_frames(run: dict[str, Any], index: int, start: float, end: float, minimum: float = 0.3) -> list[dict[str, Any]]:
	"""Frames of one display that stayed unchanged for at least ``minimum`` seconds inside [start, end) (the refresh/scan glitch frames are shorter)."""
	frames = L.display_events(run, index)
	rows = []
	for position, event in enumerate(frames):
		begin = max(event["time_s"], start)
		finish = min(frames[position + 1]["time_s"] if position + 1 < len(frames) else end, end)
		if finish - begin >= minimum and begin < end:
			rows.append({"from_s": begin, "to_s": finish, "segments": event["segments"], "text": display_text(event)})
	return rows


def switch_window(run: dict[str, Any], start: float, end: float, title: str) -> dict[str, Any]:
	"""What the two alphanumeric lines show, in stable frames, between start and end of one stimulus step."""
	d0 = stable_frames(run, 0, start, end)
	d1 = stable_frames(run, 1, start, end)
	names = []
	for frame in d0:
		text = frame["text"]
		if text and title not in text and text not in names:
			names.append(text)
	numbers = []
	for frame in d1:
		digits = L.decode_digits(frame["segments"], (4, 5)).strip()
		if digits and digits not in numbers:
			numbers.append(digits)
	d0_title_only = bool(d0) and all((not f["text"]) or title in f["text"] for f in d0)
	return {
		"names": names,
		"numbers": numbers,
		"title_only": d0_title_only,
		"d0_stable_texts": sorted({f["text"] for f in d0}),
		"d1_stable_texts": sorted({f["text"] for f in d1}),
	}


def rom_display_text(text: str) -> str:
	"""ROM table text as the display draws it: the font code z is the quotation mark (WIN zWz LANE shows as WIN "W" LANE)."""
	return L.normalize(text.replace("z", '"'))


def switch_sweep(run: dict[str, Any], rom_entries: list[dict[str, Any]], title: str, control: int = 39) -> dict[str, Any]:
	"""One row per stimulated address: ROM reaction while at 1 and after returning to 0, plus the host readback at the end of the 1 window."""
	steps = step_windows(run)
	snapshots = run["snapshots"]
	rows: dict[int, dict[str, Any]] = {}
	controls = []
	rom_by_address = {entry["index"]: entry["text"] for entry in rom_entries[:SWITCH_TABLE_ENTRIES]}
	for position, step in enumerate(steps):
		if step["type"] != "set_switch" or step["switch"] in (-6, -7) or step["state"] != 1:
			continue
		release = steps[position + 1]
		assert release["type"] == "set_switch" and release["switch"] == step["switch"] and release["state"] == 0, (step["label"], release["label"])
		address = step["switch"]
		active = switch_window(run, step["_start"], step["_end"], title)
		rel_frames = stable_frames(run, 0, release["_start"], release["_end"])
		final_text = rel_frames[-1]["text"] if rel_frames else None
		snapshot = snapshots[step["step"]]
		readback = next((w["state"] for w in snapshot.get("watched_switches", []) if w["number"] == address), None)
		row = {
			"address": address,
			"label": step["label"],
			"names_while_1": active["names"],
			"numbers_while_1": active["numbers"],
			"title_only_while_1": active["title_only"],
			"final_stable_text_after_return_to_0": final_text,
			"back_to_title_after_return_to_0": final_text == title,
			"host_readback_at_end_of_1_window": readback,
		}
		rom_name = rom_by_address.get(address)
		row["rom_table_name"] = rom_name
		if address == control:
			controls.append(row)
			continue
		rows[address] = row
	for address, row in rows.items():
		expected = rom_display_text(row["rom_table_name"]) if row["rom_table_name"] is not None else None
		named = row["names_while_1"]
		numbered = row["numbers_while_1"]
		if named and numbered:
			row["reaction"] = "name_and_number"
		elif numbered and not named:
			row["reaction"] = "number_only"
		elif named:
			row["reaction"] = "name_only"
		else:
			row["reaction"] = "none"
		row["name_equals_rom_table"] = (named == ([expected] if expected else [])) if expected is not None else None
		row["number_equals_address"] = (numbered == [f"{address:02d}"]) if numbered else None
	return {"rows": [rows[a] for a in sorted(rows)], "controls": controls}


def step_by_label(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [s for s in step_windows(run) if s["label"] == label]
	if len(matches) != 1:
		raise RuntimeError(f"expected exactly one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def phase_events(run: dict[str, Any], start: float, end: float) -> dict[str, Any]:
	"""Solenoid on-counts, the ordered on-sequence with times relative to ``start``, and lamp activity inside one window."""
	on = [e for e in L.solenoid_events(run, start, end) if e["state"]]
	counts = Counter(e["number"] for e in on)
	lamps = Counter(e["number"] for e in L.lamp_events(run, start, end))
	return {
		"window_s": [round(start, 3), round(end, 3)],
		"solenoid_on_counts": {str(a): counts[a] for a in sorted(counts)},
		"solenoid_on_sequence": [[round(e["time_s"] - start, 2), e["number"]] for e in on],
		"lamp_toggle_counts": {str(a): lamps[a] for a in sorted(lamps)},
	}


def spans_text(run: dict[str, Any], address: int, start: float = 0.0, end: float = float("inf")) -> list[list[float | None]]:
	return [[round(b, 2), round(e, 2) if e is not None else None] for b, e in L.solenoid_spans(run, address, start, end)]


def boot_probe(run: dict[str, Any], until: float = 19.5) -> dict[str, Any]:
	"""The ROM's own power-up behaviour: per solenoid, every on-span and the repeat interval, in the first ``until`` seconds."""
	by_address: dict[int, list[list[float | None]]] = {}
	for row in boot_pulses(run, until):
		by_address.setdefault(row["address"], []).append([row["on_s"], row["off_s"]])
	summary = {}
	for address, spans in sorted(by_address.items()):
		starts = [s[0] for s in spans]
		gaps = [round(b - a, 2) for a, b in zip(starts, starts[1:])]
		summary[str(address)] = {"on_spans_s": spans, "pulse_count": len(spans), "gaps_between_pulse_starts_s": gaps}
	return {"held_switches": [[item["switch"], item["state"]] for item in run["initial_switches"]], "window_s": until, "solenoids": summary}


def motor_bank(run: dict[str, Any]) -> dict[str, Any]:
	"""Timeline of the MOTOR BANK TEST (test 08), times in seconds after the test title first appeared."""
	t0 = first_display_time(run, "MOTOR BANK TEST")
	if t0 is None:
		raise RuntimeError("MOTOR BANK TEST never displayed")
	timeline: list[dict[str, Any]] = []
	for event in run["events"]:
		if event["time_s"] < t0 - 0.3:
			continue
		rel = round(event["time_s"] - t0, 2)
		if event["event"] == "solenoid" and event["number"] == 16:
			timeline.append({"t": rel, "what": f"solenoid 16 {'on' if event['state'] else 'off'}"})
		elif event["event"] == "switch" and event["number"] in (16, 24) and "step" in event and "observed_state" in event:
			timeline.append({"t": rel, "what": f"host sets switch {event['number']} = {event['state']}"})
	for index in (0, 1):
		previous = None
		for frame in stable_frames(run, index, t0 - 0.3, run["events"][-1]["time_s"], minimum=0.15):
			text = frame["text"]
			if text != previous:
				timeline.append({"t": round(frame["from_s"] - t0, 2), "what": f"display {index} shows {text!r}"})
				previous = text
	timeline.sort(key=lambda item: (item["t"], item["what"]))
	relay = [[round(b - t0, 2), round(e - t0, 2) if e is not None else None] for b, e in L.solenoid_spans(run, 16, t0 - 0.3)]
	return {"test_start_s": round(t0, 3), "relay_16_on_spans_after_test_start_s": relay, "timeline": timeline}


def text_timeline(run: dict[str, Any], start: float, end: float, minimum: float = 0.3, limit: int = 40) -> list[dict[str, Any]]:
	"""De-duplicated stable (>= ``minimum`` s) frames of both alphanumeric lines, times relative to ``start``."""
	rows = []
	for index in (0, 1):
		previous = None
		for frame in stable_frames(run, index, start, end, minimum):
			if frame["text"] != previous:
				rows.append({"t": round(frame["from_s"] - start, 2), "line": index, "text": frame["text"]})
				previous = frame["text"]
	rows.sort(key=lambda row: (row["t"], row["line"]))
	return rows[:limit]


def game_phases(run: dict[str, Any]) -> dict[str, Any]:
	"""Power-up, attract and game phases of a coin-and-Start scenario (labels from tools/gen_game_scenarios.py)."""
	attract = step_by_label(run, "observe attract mode")
	start_step = step_by_label(run, "Start (Credit button)")
	last = step_windows(run)[-1]
	end = last["_end"]
	phases = {
		"power_up_and_stabilize": phase_events(run, 0.0, attract["_start"]),
		"attract": phase_events(run, attract["_start"], attract["_end"]),
		"after_start_press": phase_events(run, start_step["_start"], end),
	}
	phases["after_start_press"]["text_timeline"] = text_timeline(run, start_step["_start"], end)
	phases["attract"]["text_timeline"] = text_timeline(run, attract["_start"], attract["_end"], limit=12)
	phases["credit_steps"] = [
		{"label": s["label"], "text_timeline": text_timeline(run, s["_start"], s["_end"], minimum=0.15, limit=8)}
		for s in step_windows(run)
		if s["label"] in ("coin 1", "coin 2", "Start (Credit button)")
	]
	phases["solenoid_23_spans_s"] = spans_text(run, 23)
	return phases


def switch_responses(run: dict[str, Any], rows: list[dict[str, Any]], title: str) -> dict[int, dict[str, Any]]:
	"""Raw stable display frames (name line and number cells) of every switch that drew a name or number while at 1."""
	by_label = {s["label"]: s for s in step_windows(run)}
	out = {}
	for row in rows:
		if row["reaction"] == "none":
			continue
		step = by_label[row["label"]]
		d0 = [f for f in stable_frames(run, 0, step["_start"], step["_end"]) if f["text"] and title not in f["text"]]
		d1 = [f for f in stable_frames(run, 1, step["_start"], step["_end"]) if L.decode_digits(f["segments"], (4, 5)).strip()]
		out[row["address"]] = {"d0": d0[0] if d0 else None, "d1": d1[0] if d1 else None}
	return out
