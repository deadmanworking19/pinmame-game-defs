"""Summarize the retained Mousin' Around harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/mousin-around-1989/runtime/runs/`` (written by ``tools/run_pinmame_harness.py`` with the
pinned library, each from a new state directory that inherits only its set's retained initialization run's
NVRAM), checks that every run succeeded on the pinned emulator binary with an unchanged committed scenario, and
writes three files:

* ``evidence/runtime/system-11/mousin-around-l4-service-and-mechanisms.json``: the mousn_l4 service tests,
  Motor Bank Test probes, power-up probes and gameplay run;
* ``evidence/runtime/system-11/mousin-around-<set>-service-tests.json`` for mousn_l1 and mousn_lu: their Coil,
  Single Lamps and Switch Levels names, compared with mousn_l4's.

Display text is decoded from the raw sixteen-segment values of the two alphanumeric rows: the low fifteen bits
are the glyph and bit 15 is the period; the ROM draws the numeral 1 as 0x0006 and uses one glyph for 0 and O and
one for 5 and S, which the decoder writes as O and S. A Coil Test step is the text on the upper row when the
step's output rises; a Single Lamps step is the upper-row text shown longest between two Credit presses; a Switch
Levels step is the snapshot taken while the address is held; a Motor Bank Test reading is the lower row when the
Motor Relay (11) rises or falls.

Every cited display reading is pinned in ``tools/seeds/bally/mousin-around-1989-frame-readings.json`` by the
SHA-256 of the raw segment values it was decoded from. The builder refuses a run whose cited frame carries other
segment values or another reading, and a run that cites a different set of frames than the seed pins, so a
substituted or re-recorded frame cannot inherit a reading. Every claimed mechanism response (the trap-up retries,
the motor relay's stop on a limit switch, the kickback, the mouse hole eject, game-on and the outhole) is checked
against the raw transitions. Every number written is recomputed from the raw runs, and ``--check`` refuses any
drift.

    python tools/mousin_around_runtime_evidence.py            # write
    python tools/mousin_around_runtime_evidence.py --check    # re-derive and compare, write nothing
    python tools/mousin_around_runtime_evidence.py --draft-frame-readings  # print the seed body for review
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402
from run_pinmame_harness import SEGMENT_16_CHARACTERS  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
MACHINE_ID = "bally.mousin-around.1989"
GAME = "mousn_l4"
VARIANT_GAMES = ("mousn_l1", "mousn_lu")
ROM_ARCHIVE_SHA256 = {
	"mousn_l4": "028dbe18f0183a213a88558cbd9e542283acdcbe0c14958ce50a947784923a74",
	"mousn_l1": "141200ceef7cc2ce7ea664bf0ae07ddc786a71448350e746b86f32241dc22e44",
	"mousn_lu": "64cb997c842cae7e906b69c5e22ab74689fd15f8439585d88355dfdfd92851f7",
}
SCENARIO_DIRECTORY = "tools/harness-scenarios/system-11"
SCENARIO_PREFIX = "mousn"
EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/mousin-around-l4-service-and-mechanisms.json"
FRAME_READINGS_PATH = ROOT / "tools/seeds/bally/mousin-around-1989-frame-readings.json"


def variant_evidence_path(game: str) -> Path:
	return ROOT / f"evidence/runtime/system-11/mousin-around-{game.split('_', 1)[1]}-service-tests.json"


RUNTIME_RELATIVE = Path("mousin-around-1989/runtime")
SOURCE_PATH = "external:pinmame-review-artifacts/mousin-around-1989/runtime"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (the raw "
	"run JSON and log of every run, and every state-directory file including the inherited and written NVRAM) except "
	"manifest.json and manifest.sha256, sorted by POSIX relative path. tools/build_external_evidence_manifest.py writes and "
	"re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game <set> --rom-path <vpinmame-roms> "
	"--work-dir <new-state-directory> --scenario tools/harness-scenarios/system-11/mousn-<name>.json --boot-wait 0 "
	"--output <external-run.json>. Each set's initialization run (mousn-nvram-init.json) starts from an empty state "
	"directory and stops on FACTORY SETTING; every other run of that set starts from a new state directory holding only "
	"that run's NVRAM. Diagnostic scenarios wait 8 s, set Manual-Down (-6 = 0), pulse Advance (-7) to enter the tests, set "
	"Auto-Up (-6 = 1) and pulse Advance until the checkpoint text is displayed."
)
INIT_RUN = "nvram-init"
SERVICE_RUNS = ("coil-test", "single-lamps", "switch-levels")
MOTOR_RUNS = ("motor-bank-no-switch", "motor-bank-up-held", "motor-bank-up-down-up")
BOOT_RUNS = (
	"boot-baseline", "boot-outhole-9", "boot-trough-11-13", "boot-shooter-14", "boot-traps-33-34", "boot-traps-ball-41-42",
	"boot-mouse-hole-59", "boot-mouse-hole-59-61", "boot-motor-up-43", "boot-motor-down-50", "boot-diverter-49",
	"boot-trough-traps-33-34", "boot-trough-motor-up-43", "boot-trough-motor-down-50", "boot-trough-diverter-49",
	"boot-trough-mouse-hole-59",
)
RUN_NAMES = (INIT_RUN, *SERVICE_RUNS, "c-side-test", *MOTOR_RUNS, *BOOT_RUNS, "gameplay")
VARIANT_RUN_NAMES = (INIT_RUN, *SERVICE_RUNS)
STATIC_LIMITATION = (
	"Static host switches only; the harness never moves a ball or a mechanism, so repeated pulses are ROM retries against a "
	"host-held switch."
)
SCRIPTED_LIMITATION = (
	"The host answers the ROM's drives with fixed, scripted switch changes; a pulse the ROM fires proves only that the address "
	"changed under these conditions, not a mechanism's travel time or the physical device's identity."
)
ROM_GLYPHS = {0x0006: "1"}
# The A/C Select relay (12) toggles with every C-side flasher of the attract-mode lamp show and the G.I. relays (9, 10) follow
# the show; they say nothing about the probed device and are left out of the per-run span notes.
ATTRACT_BACKGROUND = {9, 10, 12, *range(25, 33)}


def working_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is required: the raw runs live under the working root's review-artifacts")
	return Path(value).expanduser().resolve()


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def frame_digest(*rows: list[int]) -> str:
	"""SHA-256 of the raw segment values of one or more display rows, as compact JSON."""
	return hashlib.sha256(json.dumps([list(row) for row in rows], separators=(",", ":")).encode("ascii")).hexdigest()


def decode_alpha(values: list[int]) -> str:
	text = []
	for value in values:
		glyph = ROM_GLYPHS.get(value & 0x7FFF, SEGMENT_16_CHARACTERS.get(value & 0x7FFF))
		text.append(("?" if value & 0x7FFF else " ") if glyph is None else glyph)
		if value & 0x8000:
			text.append(".")
	return "".join(text)


def normalized(text: str) -> str:
	return " ".join(text.split())


def run_file(runs: Path, game: str, name: str) -> Path:
	return runs / f"{game}-{name}.json"


class Pins:
	"""The pinned readings of one run, and the set of frames the builder actually cites from it."""

	def __init__(self, key: str, pinned: dict[str, Any]) -> None:
		self.key = key
		self.pinned = pinned
		self.cited: set[str] = set()

	def check(self, label: str, digest: str, reading: str) -> str:
		pin = self.pinned.get(label)
		if pin is None:
			raise RuntimeError(f"{self.key}: cited frame {label!r} is not pinned in {FRAME_READINGS_PATH.name}")
		if pin["segments_sha256"] != digest:
			raise RuntimeError(f"{self.key}: frame {label!r} carries other segment values than the pinned frame")
		if pin["reading"] != reading:
			raise RuntimeError(f"{self.key}: frame {label!r} decodes as {reading!r}, pinned as {pin['reading']!r}")
		self.cited.add(label)
		return reading

	def finish(self) -> None:
		if self.cited != set(self.pinned):
			missing = sorted(set(self.pinned) - self.cited)
			raise RuntimeError(f"{self.key}: pinned frames not cited by the run: {missing[:5]}")


def load_run(runs: Path, game: str, name: str) -> dict[str, Any]:
	run = json.loads(run_file(runs, game, name).read_text(encoding="utf-8"))
	if run.get("failure") is not None or run.get("game") != game:
		raise RuntimeError(f"{game} {name}: not a successful run")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise RuntimeError(f"{game} {name}: not produced by the pinned library")
	scenario = ROOT / SCENARIO_DIRECTORY / f"{SCENARIO_PREFIX}-{name}.json"
	if run["scenario"]["sha256"] != sha256(scenario):
		raise RuntimeError(f"{game} {name}: scenario drift against {scenario}")
	return run


def row_timeline(run: dict[str, Any], index: int) -> list[tuple[float, list[int]]]:
	timeline = []
	for event in run["events"]:
		if event["event"] == "display" and event.get("index") == index and isinstance(event.get("segments"), list):
			timeline.append((event["time_s"], event["segments"]))
	return timeline


def text_timeline(run: dict[str, Any], index: int = 0) -> list[tuple[float, str]]:
	return [(at, normalized(decode_alpha(segments))) for at, segments in row_timeline(run, index)]


def frame_at(timeline: list[tuple[float, list[int]]], time: float) -> list[int]:
	current: list[int] = []
	for at, segments in timeline:
		if at > time:
			break
		current = segments
	return current


def longest_frame(timeline: list[tuple[float, list[int]]], start: float, end: float) -> list[int]:
	"""The segment values shown longest in [start, end); ties go to the earliest frame."""
	durations: dict[str, float] = {}
	frames: dict[str, list[int]] = {}
	order: list[str] = []

	def add(segments: list[int], seconds: float) -> None:
		key = json.dumps(segments)
		if key not in frames:
			frames[key] = segments
			order.append(key)
		durations[key] = durations.get(key, 0.0) + seconds

	current, at = frame_at(timeline, start), start
	for when, segments in timeline:
		if when <= start:
			continue
		if when >= end:
			break
		add(current, when - at)
		current, at = segments, when
	add(current, end - at)
	best = max(order, key=lambda key: (durations[key], -order.index(key)))
	return frames[best]


def solenoid_spans(run: dict[str, Any]) -> dict[int, list[tuple[float, float | None]]]:
	open_at: dict[int, float] = {}
	spans: dict[int, list[tuple[float, float | None]]] = {}
	for event in run["events"]:
		if event["event"] != "solenoid":
			continue
		number, time = event["number"], round(event["time_s"], 3)
		if event["state"]:
			open_at.setdefault(number, time)
		elif number in open_at:
			spans.setdefault(number, []).append((open_at.pop(number), time))
	for number, time in open_at.items():
		spans.setdefault(number, []).append((time, None))
	return spans


def describe_spans(spans: dict[int, list[tuple[float, float | None]]], end: float) -> str:
	parts = []
	for number in sorted(spans):
		if number in ATTRACT_BACKGROUND:
			continue
		items = spans[number]
		if len(items) <= 3:
			parts.append(f"{number}: " + ", ".join(f"{a}-{'end' if b is None else b} s" for a, b in items))
		else:
			gaps = [round(items[i + 1][0] - items[i][0], 2) for i in range(len(items) - 1)]
			parts.append(f"{number}: {len(items)} pulses from {items[0][0]} s to {items[-1][0]} s, spacing {min(gaps)}-{max(gaps)} s")
	return "; ".join(parts) + f" (observed to {end} s)"


def end_time(run: dict[str, Any]) -> float:
	return round(max(event["time_s"] for event in run["events"]), 3)


def service_pulses(run: dict[str, Any]) -> int:
	total = 0
	for step in run["steps"]:
		if step.get("type") == "pulse" and step.get("switch") == -7:
			total += 1
		elif step.get("type") == "pulse_until_display" and step.get("switch") == -7:
			total += step["pulses"]
	return total


def checkpoints(run: dict[str, Any]) -> list[dict[str, Any]]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
	        for step in run["steps"] if step.get("type") == "pulse_until_display"]


def step_by_label(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [step for step in run["steps"] if step.get("label") == label]
	if len(matches) != 1:
		raise RuntimeError(f"expected one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def coil_test(run: dict[str, Any], pins: Pins) -> list[dict[str, Any]]:
	"""Each coil-test step: the address that rises and the upper-row text then, for two complete cycles."""
	upper = row_timeline(run, 0)
	begin = next(at for at, segments in upper if normalized(decode_alpha(segments)) == "COIL TEST")
	steps = []
	for event in run["events"]:
		if event["event"] != "solenoid" or not event["state"] or event["time_s"] <= begin or event["number"] == 23:
			continue
		segments = frame_at(upper, event["time_s"])
		text = normalized(decode_alpha(segments))
		# The A/C select relay (12) is energized ahead of every C-side step; it is a step of its own only where the ROM names it.
		if event["number"] == 12 and text != "A/C SELECT":
			continue
		steps.append({"address": event["number"], "display": text, "digest": frame_digest(segments), "time_s": round(event["time_s"], 3)})
	period = next(index for index in range(1, len(steps)) if steps[index]["address"] == steps[0]["address"] and index > 2)
	first, second = steps[:period], steps[period:2 * period]
	if [step["address"] for step in first] != [step["address"] for step in second]:
		raise RuntimeError("coil test second cycle differs from the first")
	if [step["display"] for step in first] != [step["display"] for step in second]:
		raise RuntimeError("coil test second cycle names differ from the first")
	result = []
	for index, (step, repeat) in enumerate(zip(first, second), start=1):
		pins.check(f"coil step {index:02d}, cycle 1", step["digest"], step["display"])
		pins.check(f"coil step {index:02d}, cycle 2", repeat["digest"], repeat["display"])
		result.append({"step": index, "address": step["address"], "display": step["display"]})
	return result


def relay_held(run: dict[str, Any], steps: list[dict[str, Any]]) -> list[int]:
	"""Addresses whose coil-test pulse falls inside an energized span of the A/C relay (12)."""
	timeline = text_timeline(run)
	begin = next(at for at, text in timeline if text == "COIL TEST")
	relay = solenoid_spans(run).get(12, [])
	held = []
	rises = [(event["time_s"], event["number"]) for event in run["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] > begin]
	for step in steps:
		time = next(t for t, n in rises if n == step["address"])
		if step["address"] != 12 and any(a <= time and (b is None or time < b) for a, b in relay):
			held.append(step["address"])
	if held != list(range(25, 33)):
		raise RuntimeError(f"the A/C relay was held for {held}, not exactly the C-side bank 25-32")
	if not any(step["address"] == 12 and step["display"] == "A/C SELECT" for step in steps):
		raise RuntimeError("the coil test has no A/C SELECT step of its own")
	return held


def single_lamps(run: dict[str, Any], pins: Pins) -> list[dict[str, Any]]:
	upper = row_timeline(run, 0)
	presses = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event.get("number") == 3 and event.get("state") == 1]
	steps = [step for step in run["steps"] if step.get("label", "").startswith(("Credit: step to designator", "first lamp"))]
	title = next(at for at, segments in upper if normalized(decode_alpha(segments)) == "SINGLE LAMPS")
	# The first lamp's window starts when the test title gives way to the first lamp name.
	begin = next(at for at, segments in upper if at > title and normalized(decode_alpha(segments)) != "SINGLE LAMPS")
	bounds = [begin] + presses
	pairs = []
	for index, step in enumerate(steps):
		designator = 1 if step["label"].startswith("first lamp") else int(step["label"].rsplit(" ", 1)[1])
		changed = sorted({lamp["number"] for lamp in step["transitions"]["lamps"]})
		start, end = bounds[index] + 0.3, bounds[index + 1]
		blinked = sorted({event["number"] for event in run["events"] if event["event"] == "lamp" and start <= event["time_s"] < end})
		if blinked != [designator]:
			raise RuntimeError(f"single lamps designator {designator} blinked {blinked}")
		segments = longest_frame(upper, start, end)
		display = pins.check(f"lamp designator {designator:02d}", frame_digest(segments), normalized(decode_alpha(segments)))
		pairs.append({"designator": designator, "address": designator, "display": display, "step_changed": changed})
	if [pair["designator"] for pair in pairs] != list(range(1, 65)):
		raise RuntimeError("single lamps did not step through designators 01-64")
	return pairs


def switch_levels(run: dict[str, Any], pins: Pins) -> list[dict[str, Any]]:
	results = []
	for step in run["steps"]:
		label = step.get("label", "")
		if not label.startswith("hold public switch"):
			continue
		address = int(label.rsplit(" ", 1)[1])
		snapshot = next(item for item in run["snapshots"] if item.get("label") == label + " (held)")
		rows = {display["index"]: display["segments"] for display in snapshot["displays"] if display["index"] in (0, 1)}
		upper, lower = normalized(decode_alpha(rows[0])), normalized(decode_alpha(rows[1]))
		pins.check(f"switch {address} held", frame_digest(rows[0], rows[1]), f"{upper} / {lower}")
		results.append({"address": address, "upper": upper, "lower": lower})
	return results


def boot_note(run: dict[str, Any]) -> str:
	holds = ", ".join(f"{item['switch']}={item['state']}" for item in run["initial_switches"])
	return f"Power-up probe with switches {holds} held from emulator start. Solenoid on-spans: {describe_spans(solenoid_spans(run), end_time(run))}."


def motor_test(run: dict[str, Any], name: str, pins: Pins) -> str:
	"""The Motor Relay (11) spans and the lower-row reading at each of its edges."""
	lower = row_timeline(run, 1)
	upper = text_timeline(run, 0)
	begin = next(at for at, text in upper if text == "MOTOR BANK TEST")
	spans = [span for span in solenoid_spans(run).get(11, []) if span[0] > begin]
	if not spans:
		raise RuntimeError(f"{name}: the Motor Relay (11) never energized in the Motor Bank Test")
	parts = []
	end = end_time(run)
	for index, (rise, fall) in enumerate(spans, start=1):
		rise_frame = frame_at(lower, rise + 0.1)
		on = pins.check(f"motor span {index} rise", frame_digest(rise_frame), normalized(decode_alpha(rise_frame)))
		if fall is None:
			if index != len(spans):
				raise RuntimeError(f"{name}: an earlier Motor Relay (11) span never closed")
			parts.append(f"11 on from {rise} s and still energized when the run ends at {end} s, lower display '{on}' after the rise")
			continue
		fall_frame = frame_at(lower, fall + 0.1)
		off = pins.check(f"motor span {index} fall", frame_digest(fall_frame), normalized(decode_alpha(fall_frame)))
		parts.append(f"11 on {rise}-{fall} s ({round(fall - rise, 3)} s), lower display '{on}' after the rise and '{off}' after the fall")
	switches = [f"{event['number']}={event['state']} at {round(event['time_s'], 3)} s" for event in run["events"]
	            if event["event"] == "switch" and event.get("number") in (43, 50) and event["time_s"] > begin]
	held = ", ".join(f"{item['switch']}={item['state']}" for item in run["initial_switches"]) or "none"
	expected = {
		"motor-bank-no-switch": lambda: len(spans) == 1 and spans[0][1] is not None and spans[0][1] - spans[0][0] > 14.0,
		"motor-bank-up-held": lambda: (
			len(spans) == 2 and None not in (spans[0][1], spans[1][1])
			and spans[0][1] - spans[0][0] < 0.2 and spans[1][1] - spans[1][0] > 7.0
		),
		"motor-bank-up-down-up": lambda: (
			len(spans) == 3 and _stops_on(run, spans[0], 50) and _stops_on(run, spans[1], 43) and spans[2][1] is None
		),
	}[name]
	if not expected():
		raise RuntimeError(f"{name}: the Motor Relay spans {spans} do not show the recorded behaviour")
	return (
		f"Advance walk to MOTOR BANK TEST (lower display 09) with switches held from start: {held}. Host switch changes after the "
		f"title: {', '.join(switches) or 'none'}. " + "; ".join(parts) + "."
	)


def _stops_on(run: dict[str, Any], span: tuple[float, float | None], switch: int) -> bool:
	"""True when the span ends within 0.3 s after the host closes ``switch``, and not before."""
	rise, fall = span
	closes = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event.get("number") == switch and event["state"] == 1 and rise < event["time_s"]]
	return fall is not None and bool(closes) and 0 < fall - closes[0] < 0.3


C_SIDE_TITLE = "C-SIDE SW. TEST"
C_SIDE_EXPECTED = {
	"rise upper": "SELECTED C-SIDE", "rise lower": "C-SIDE O8", "fall upper": "SELECTED A-SIDE", "fall lower": "O8",
}


def c_side_test(run: dict[str, Any], pins: Pins) -> str:
	"""The A/C Select relay (12) spans in the C-Side test and both display rows 0.2 s after each of its edges."""
	upper, lower = row_timeline(run, 0), row_timeline(run, 1)
	begin = next(at for at, segments in upper if normalized(decode_alpha(segments)) == C_SIDE_TITLE)
	title = pins.check("title upper", frame_digest(frame_at(upper, begin)), normalized(decode_alpha(frame_at(upper, begin))))
	title_lower = pins.check("title lower", frame_digest(frame_at(lower, begin + 0.01)), normalized(decode_alpha(frame_at(lower, begin + 0.01))))
	spans = [span for span in solenoid_spans(run).get(12, []) if span[0] > begin]
	if len(spans) < 4 or any(fall is None for _, fall in spans):
		raise RuntimeError(f"c-side-test: the A/C Select relay (12) spans {spans} are not complete alternations")
	for index, (rise, fall) in enumerate(spans, start=1):
		for edge, at in (("rise", rise), ("fall", fall)):
			for row, timeline in (("upper", upper), ("lower", lower)):
				frame = frame_at(timeline, at + 0.2)
				reading = pins.check(f"span {index} {edge} {row}", frame_digest(frame), normalized(decode_alpha(frame)))
				if reading != C_SIDE_EXPECTED[f"{edge} {row}"]:
					raise RuntimeError(f"c-side-test: span {index} {edge} {row} reads {reading!r}")
	durations = [round(fall - rise, 3) for rise, fall in spans]
	gaps = [round(spans[i + 1][0] - spans[i][1], 3) for i in range(len(spans) - 1)]
	others = {number: items for number, items in solenoid_spans(run).items() if number != 12}
	return (
		f"Advance walk to the C-Side test: upper display '{title}', lower display '{title_lower}'. The A/C Select relay (12) was "
		f"then energized {len(spans)} times for {min(durations)}-{max(durations)} s, {min(gaps)}-{max(gaps)} s apart ("
		+ ", ".join(f"{rise}-{fall} s" for rise, fall in spans)
		+ "). 0.2 s after every rise the upper display read 'SELECTED C-SIDE' and the lower 'C-SIDE O8'; 0.2 s after every "
		"fall they read 'SELECTED A-SIDE' and 'O8'. Other solenoid on-spans: " + describe_spans(others, end_time(run)) + "."
	)


def rises(run: dict[str, Any], number: int, after: float, before: float) -> list[float]:
	return [round(event["time_s"], 3) for event in run["events"] if event["event"] == "solenoid" and event["number"] == number
	        and event["state"] and after <= event["time_s"] < before]


def falls(run: dict[str, Any], number: int, after: float, before: float) -> list[float]:
	return [round(event["time_s"], 3) for event in run["events"] if event["event"] == "solenoid" and event["number"] == number
	        and not event["state"] and after <= event["time_s"] < before]


def host_time(run: dict[str, Any], number: int, state: int, after: float = 0.0) -> float:
	return next(round(event["time_s"], 3) for event in run["events"] if event["event"] == "switch" and event.get("number") == number
	            and event.get("state") == state and event["time_s"] >= after)


def gameplay(run: dict[str, Any]) -> str:
	"""Check every response the gameplay notes claim and describe it."""
	end = end_time(run)
	start = host_time(run, 3, 1)
	game_on = rises(run, 23, start, start + 0.5)
	serve = rises(run, 2, start, start + 2.0)
	sling_jets = {}
	for switch, coil in ((52, 17), (53, 19), (54, 21), (55, 18), (56, 20)):
		closed = host_time(run, switch, 1)
		fired = rises(run, coil, closed, closed + 0.1)
		if len(fired) != 1:
			raise RuntimeError(f"gameplay: switch {switch} did not fire solenoid {coil} once within 0.1 s")
		sling_jets[switch] = (coil, round(fired[0] - closed, 3))
	trap_press = host_time(run, 28, 1)
	open_33, open_34 = host_time(run, 33, 0), host_time(run, 34, 0)
	trap1, trap2 = rises(run, 3, trap_press, end), rises(run, 4, trap_press, end)
	if len(trap1) < 2 or len(trap2) < 2 or max(trap1) > open_33 or max(trap2) > open_34 or trap1[0] - trap_press > 0.5:
		raise RuntimeError("gameplay: the trap-up coils did not retry while 33/34 were closed and stop once they opened")
	retry_gap = round(trap1[1] - trap1[0], 3)
	if max(open_33, open_34) + 2 * retry_gap > end:
		raise RuntimeError("gameplay: the run ends before a further trap-up retry could have been seen")
	target = host_time(run, 31, 1)
	motor_rise = rises(run, 11, target, target + 0.2)
	down_close = host_time(run, 50, 1, target)
	motor_fall = falls(run, 11, target, down_close + 0.3)
	if len(motor_rise) != 1 or len(motor_fall) != 1 or not motor_fall[0] > down_close:
		raise RuntimeError("gameplay: the motor relay did not start on the third center standup and stop when 50 closed")
	kick = host_time(run, 51, 1)
	kickback = rises(run, 13, kick, kick + 0.1)
	lock = host_time(run, 59, 1)
	eject = rises(run, 16, lock, lock + 2.0)
	raise_bank = rises(run, 11, lock, lock + 1.0)
	tilts = [round(event["time_s"], 3) for event in run["events"] if event["event"] == "switch" and event.get("number") == 1 and event["state"] == 1]
	tilt_off = falls(run, 23, tilts[-1], tilts[-1] + 0.2) if len(tilts) == 3 else []
	drain = host_time(run, 9, 1)
	outhole = rises(run, 1, drain, drain + 1.0)
	next_ball = rises(run, 23, drain, end)
	next_serve = rises(run, 2, drain, end)
	if not (game_on and serve and kickback and eject and raise_bank and tilt_off and outhole and next_ball and next_serve):
		raise RuntimeError("gameplay: a claimed response is missing from the raw run")
	return (
		f"Credit button (3) at {start} s raised game-on (23) at {game_on[0]} s and the ball shooter lane feeder (2) fired at {serve[0]} s. "
		+ "; ".join(f"switch {switch} fired solenoid {coil} {delay} s later" for switch, (coil, delay) in sling_jets.items())
		+ f". TRAP - P (28) at {trap_press} s completed MOUSE TRAP: TRAP 1 UP (3) rose at {', '.join(map(str, trap1))} s and TRAP 2 UP "
		f"(4) at {', '.join(map(str, trap2))} s while the host held 33 and 34 closed, about every {retry_gap} s, and neither rose again "
		f"after the host opened 33 at {open_33} s and 34 at {open_34} s. The third center standup (31) at {target} s energized the "
		f"Motor Relay (11) at {motor_rise[0]} s; it released at {motor_fall[0]} s, after the host closed the bank-down switch 50 at "
		f"{down_close} s. The kickback lane (51) at {kick} s fired the kickback (13) at {kickback[0]} s. Mouse hole lock 1 (59) "
		f"closed at {lock} s: the motor relay rose again at {raise_bank[0]} s with 43 open and 50 closed, and MOUSE HOLE EJECT (16) "
		f"fired at {eject[0]} s. The third plumb-bob closure at {tilts[-1]} s dropped game-on (23) at {tilt_off[0]} s; the outhole "
		f"(9) at {drain} s fired the outhole kicker (1) at {outhole[0]} s, and game-on rose again at {next_ball[0]} s before the "
		f"feeder served ball 2 at {next_serve[0]} s. Solenoid on-spans: {describe_spans(solenoid_spans(run), end)}."
	)


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def raw_entry(runtime: Path, runs: Path, game: str, name: str, run: dict[str, Any]) -> dict[str, Any]:
	init_dir = "state-init" if game == GAME else f"state-init-{game}"
	init_nv = sha256(runtime / init_dir / "nvram" / f"{game}.nv")
	entry: dict[str, Any] = {
		"name": name,
		"sha256": sha256(run_file(runs, game, name)),
		"scenario_path": f"{SCENARIO_DIRECTORY}/{SCENARIO_PREFIX}-{name}.json",
		"scenario_sha256": run["scenario"]["sha256"],
		"action_count": run["scenario"]["action_count"],
		"watch_switches": run["watch_switches"],
		"self_test_pulses": service_pulses(run),
		"boot_wait_s": 0,
		"snapshot_count": len(run["snapshots"]),
		"nvram_initialization": (
			f"Fresh empty state directory; this is the one retained {game} initialization run (FACTORY SETTING), whose "
			f"nvram/{game}.nv is the only state any later {game} run inherits."
			if name == INIT_RUN
			else f"Fresh state directory holding only nvram/{game}.nv (SHA-256 {init_nv}) from the retained {game} initialization run."
		),
	}
	if run["initial_switches"]:
		entry["initial_switches"] = [{"switch": item["switch"], "state": item["state"]} for item in run["initial_switches"]]
	return entry


def service_observations(run: dict[str, Any], name: str, pins: Pins) -> tuple[dict[str, Any], dict[str, int], list[Any]]:
	"""The observation for a Coil, Single Lamps or Switch Levels run, its named addresses and its raw pairing."""
	spans = solenoid_spans(run)
	observation: dict[str, Any] = {"solenoid_addresses_seen": sorted(spans), "diagnostic_checkpoints": checkpoints(run)}
	named: dict[str, int] = {}
	if name == "coil-test":
		steps = coil_test(run, pins)
		held = relay_held(run, steps)
		for step in steps:
			named[f"coil-{step['step']:02d}-{slug(step['display'])}"] = step["address"]
		observation.update({
			"ordered_solenoid_on_sequence": [step["address"] for step in steps],
			"note": (
				f"Advance walk to COIL TEST (lower display 05), then two identical cycles of {len(steps)} named steps. "
				"Step:address = upper display: " + "; ".join(f"{s['step']}:{s['address']} = {s['display']}" for s in steps)
				+ f". The A/C select relay (12) is energized before and held through each step that pulses {', '.join(map(str, held))}, "
				"pulsed by itself in its own A/C SELECT step, and released for every other step."
			),
			"limitation": "A pulsed address is ROM activity, not proof that a load is fitted.",
		})
		return observation, named, [{"address": s["address"], "display": s["display"]} for s in steps]
	if name == "single-lamps":
		pairs = single_lamps(run, pins)
		for pair in pairs:
			named[f"lamp-{pair['designator']:02d}-{slug(pair['display'])}"] = pair["address"]
		observation.update({
			"note": (
				"Advance walk to SINGLE LAMPS (lower display 04); each Credit press (public 3) steps the designator, and designator n "
				"blinks public lamp n alone for every n from 1 to 64. Designator = upper display: "
				+ "; ".join(f"{p['designator']} = {p['display']}" for p in pairs) + "."
			),
		})
		return observation, named, [{"address": p["address"], "display": p["display"]} for p in pairs]
	results = switch_levels(run, pins)
	observation.update({
		"note": (
			"Advance walk to SWITCH LEVELS (lower display 06); each public address 1-64 and 81-88 held at 1 alone for 1.5 s. "
			"Address = upper display / lower display while held: " + "; ".join(f"{r['address']} = {r['upper']} / {r['lower']}" for r in results) + "."
		),
		"limitation": "Host-held levels written on every poll; a name shown while public n is held at 1 means the ROM reads that address as active at 1.",
	})
	return observation, named, results


def evidence_record(game: str, extractor: str, manifest_bytes: bytes, raw_runs: list[dict[str, Any]], observations: dict[str, Any]) -> dict[str, Any]:
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": extractor, "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": SOURCE_PATH,
			"sha256": hashlib.sha256(manifest_bytes).hexdigest(),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external.",
			"quality": "observed",
			"manifest_algorithm": MANIFEST_ALGORITHM,
		},
		"driver_ids": [game],
		"machine_ids": [MACHINE_ID],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": game,
			"rom_archive_sha256": ROM_ARCHIVE_SHA256[game],
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"raw_runs": raw_runs,
			"command_template": COMMAND_TEMPLATE,
			"observations": observations,
		},
	}


def frame_pins(game: str, name: str, draft: bool) -> Pins:
	key = f"{game}/{name}"
	if draft:
		return _DraftPins(key)
	runs = json.loads(FRAME_READINGS_PATH.read_bytes())["runs"]
	return Pins(key, runs.get(key, {}))


class _DraftPins(Pins):
	"""Records every cited frame instead of checking it, so the curator can review the readings before pinning them."""

	def __init__(self, key: str) -> None:
		super().__init__(key, {})

	def check(self, label: str, digest: str, reading: str) -> str:
		self.pinned[label] = {"segments_sha256": digest, "reading": reading}
		self.cited.add(label)
		return reading


def build(review_root: Path, draft: bool = False, load=load_run) -> tuple[bytes, dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
	runtime = review_root / RUNTIME_RELATIVE
	runs_dir = runtime / "runs"
	manifest_bytes = (json.dumps(manifests.build_manifest(runtime, GAME), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
	raw_runs, observations = [], {}
	seen: set[int] = set()
	named: dict[str, int] = {}
	reference: dict[str, list[Any]] = {}
	drafted: dict[str, Any] = {}
	for name in RUN_NAMES:
		run = load(runs_dir, GAME, name)
		pins = frame_pins(GAME, name, draft)
		raw_runs.append(raw_entry(runtime, runs_dir, GAME, name, run))
		spans = solenoid_spans(run)
		seen.update(spans)
		if name in SERVICE_RUNS:
			observation, run_named, reference[name] = service_observations(run, name, pins)
			named.update(run_named)
		elif name == INIT_RUN:
			observation = {
				"solenoid_addresses_seen": sorted(spans),
				"note": "Boot to FACTORY SETTING from an empty state directory; the NVRAM written on stop is the only state later mousn_l4 runs inherit.",
			}
		elif name in MOTOR_RUNS:
			observation = {
				"solenoid_addresses_seen": sorted(spans),
				"diagnostic_checkpoints": checkpoints(run),
				"note": motor_test(run, name, pins),
				"limitation": SCRIPTED_LIMITATION if name == "motor-bank-up-down-up" else STATIC_LIMITATION,
			}
		elif name.startswith("boot-"):
			observation = {"solenoid_addresses_seen": sorted(spans), "note": boot_note(run), "limitation": STATIC_LIMITATION}
		elif name == "gameplay":
			observation = {"solenoid_addresses_seen": sorted(spans), "note": gameplay(run), "limitation": SCRIPTED_LIMITATION}
		elif name == "c-side-test":
			observation = {
				"solenoid_addresses_seen": sorted(spans),
				"diagnostic_checkpoints": checkpoints(run),
				"note": c_side_test(run, pins),
				"limitation": STATIC_LIMITATION,
			}
		else:
			raise RuntimeError(f"no summary is defined for run {name}")
		pins.finish()
		if pins.pinned:
			drafted[pins.key] = pins.pinned
		observations[name] = observation
	evidence = evidence_record(GAME, "mousin-around-harness-runs", manifest_bytes, raw_runs, {
		"service_language": "English",
		"solenoid_addresses_seen": sorted(seen),
		"named_output_addresses": named,
		"runs": observations,
	})
	variants = {}
	for game in VARIANT_GAMES:
		game_runs, game_observations, game_named = [], {}, {}
		for name in VARIANT_RUN_NAMES:
			run = load(runs_dir, game, name)
			game_runs.append(raw_entry(runtime, runs_dir, game, name, run))
			if name == INIT_RUN:
				game_observations[name] = {
					"solenoid_addresses_seen": sorted(solenoid_spans(run)),
					"note": f"Boot to FACTORY SETTING from an empty state directory; the NVRAM written on stop is the only state later {game} runs inherit.",
				}
				continue
			pins = frame_pins(game, name, draft)
			observation, run_named, pairing = service_observations(run, name, pins)
			pins.finish()
			drafted[pins.key] = pins.pinned
			game_named.update(run_named)
			same = pairing == reference[name]
			observation["note"] += f" Every pairing and displayed name is {'identical to' if same else 'DIFFERENT from'} the mousn_l4 run of the same test."
			game_observations[name] = observation
		variants[game] = evidence_record(game, "mousin-around-variant-harness-runs", manifest_bytes, game_runs, {
			"service_language": "English",
			"named_output_addresses": game_named,
			"runs": game_observations,
		})
	return manifest_bytes, evidence, variants, drafted


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--draft-frame-readings", action="store_true", help="print every cited frame's digest and reading for review")
	args = parser.parse_args()
	review_root = working_root()
	runtime = review_root / RUNTIME_RELATIVE
	if args.draft_frame_readings:
		drafted = build(review_root, draft=True)[3]
		sys.stdout.write(json.dumps({"runs": drafted}, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
		return
	manifest_bytes, evidence, variants, _ = build(review_root)
	if args.check:
		if (runtime / "manifest.json").read_bytes() != manifest_bytes:
			raise SystemExit(f"{runtime / 'manifest.json'} does not match the files beside it")
		manifests.check_manifest(runtime, GAME)
		if EVIDENCE_PATH.read_bytes() != canonical_bytes(evidence):
			raise SystemExit(f"{EVIDENCE_PATH} is not the summary of the raw runs in {runtime}")
		for game, record in variants.items():
			if variant_evidence_path(game).read_bytes() != canonical_bytes(record):
				raise SystemExit(f"{variant_evidence_path(game)} is not the summary of the raw runs in {runtime}")
		print("Mousin' Around runtime evidence and manifest match the raw runs.")
		return
	manifests.write_manifest(runtime, GAME)
	EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
	EVIDENCE_PATH.write_bytes(canonical_bytes(evidence))
	for game, record in variants.items():
		variant_evidence_path(game).write_bytes(canonical_bytes(record))
	print(f"wrote {EVIDENCE_PATH} and {len(variants)} variant files")


if __name__ == "__main__":
	main()
