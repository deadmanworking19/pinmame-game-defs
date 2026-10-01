"""Shared decoding and event helpers for the Black Knight 2000 runtime analysis.

Everything here works on the raw ``pinmame-harness-run`` JSON written by ``tools/run_pinmame_harness.py``
(events carry ``time_s``/``event``; display events carry the raw 16-bit ``segments``).

Display decoding (checked against this ROM's own text, never guessed):

* each of the 16 cells of display 0 (player 1/2 line) and display 1 (player 3 line) is a 16-bit
  segment word; bit 15 (0x8000) is the cell's period segment, the other 15 bits are looked up in the
  harness's PinMAME 16-segment table;
* this ROM draws the digit 1 as 0x0006 and the digit 0 as the letter O (0x003F) on display 1, so
  display 1 numeric fields use ``DIGITS`` below instead of the letter table;
* an unknown segment pattern decodes to ``?`` and is never silently dropped.
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable

TOOLS_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = TOOLS_DIR.parent
if str(REPOSITORY_ROOT / "src") not in sys.path:
	sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
_spec = importlib.util.spec_from_file_location("run_pinmame_harness_for_bk2k", TOOLS_DIR / "run_pinmame_harness.py")
_harness = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_harness)
MACHINE_ID_DIRECTORY = "williams.black-knight-2000.1989"


def stage_root() -> Path:
	"""The external runtime-stage folder (raw runs, ROM name tables, analysis) under the review-artifacts root."""
	configured = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT", "").strip()
	if configured:
		root = Path(configured).resolve()
	else:
		from pinmame_game_defs.workspace import resolve_working_root

		root = resolve_working_root(REPOSITORY_ROOT, required=True) / "review-artifacts"
	return root / MACHINE_ID_DIRECTORY / "runtime-stage"


SEGMENT_16_CHARACTERS: dict[int, str] = dict(_harness.SEGMENT_16_CHARACTERS)

DIGITS = {0x003F: "0", 0x0006: "1", 0x085B: "2", 0x084F: "3", 0x0866: "4", 0x086D: "5", 0x087D: "6", 0x0007: "7", 0x087F: "8", 0x086F: "9", 0x443F: "0", 0x2200: "1"}


# This ROM also draws the numeral 1 as 0x0006 inside names (for example LEVEL 1 G.I.).
SEGMENT_16_CHARACTERS.setdefault(0x0006, "1")


def decode_cell(value: int) -> str:
	base = value & 0x7FFF
	character = SEGMENT_16_CHARACTERS.get(base)
	if character is None:
		return "?"
	return character + ("." if value & 0x8000 else "")


def decode_alpha(segments: list[int]) -> str:
	return "".join(decode_cell(value) for value in segments)


def normalize(text: str) -> str:
	return " ".join(text.split())


def decode_digits(segments: list[int], positions: Iterable[int]) -> str:
	"""Decode selected display-1 cells as decimal digits; ``?`` for anything unrecognised, ' ' for blank."""
	out = []
	for position in positions:
		value = segments[position]
		if value == 0:
			out.append(" ")
		elif value & 0x8000:
			out.append("?")
		else:
			out.append(DIGITS.get(value, "?"))
	return "".join(out)


def display_events(run: dict[str, Any], index: int) -> list[dict[str, Any]]:
	return [event for event in run["events"] if event["event"] == "display" and event["index"] == index and "segments" in event]


def solenoid_events(run: dict[str, Any], start: float = 0.0, end: float = float("inf")) -> list[dict[str, Any]]:
	return [event for event in run["events"] if event["event"] == "solenoid" and start <= event["time_s"] < end]


def lamp_events(run: dict[str, Any], start: float = 0.0, end: float = float("inf")) -> list[dict[str, Any]]:
	return [event for event in run["events"] if event["event"] == "lamp" and start <= event["time_s"] < end]


def solenoid_spans(run: dict[str, Any], address: int, start: float = 0.0, end: float = float("inf")) -> list[tuple[float, float | None]]:
	"""On-spans of one solenoid; an open span ends with None."""
	spans: list[tuple[float, float | None]] = []
	begin = None
	for event in solenoid_events(run, 0.0, end):
		if event["number"] != address:
			continue
		if event["state"] and begin is None:
			begin = event["time_s"]
		elif not event["state"] and begin is not None:
			if begin >= start:
				spans.append((begin, event["time_s"]))
			begin = None
	if begin is not None and begin >= start:
		spans.append((begin, None))
	return spans


def frames_between(run: dict[str, Any], index: int, start: float, end: float) -> list[dict[str, Any]]:
	"""Display frames shown in [start, end): the frame in force at start plus every change before end."""
	frames = display_events(run, index)
	before = [event for event in frames if event["time_s"] < start]
	inside = [event for event in frames if start <= event["time_s"] < end]
	return (before[-1:] if before else []) + inside


def texts_between(run: dict[str, Any], index: int, start: float, end: float) -> list[str]:
	return [normalize(decode_alpha(event["segments"])) for event in frames_between(run, index, start, end)]


STEP_PATTERN = re.compile(r'^(\d\d) (\d\d) "([A-C])" SIDE$')


def coil_step_label(segments: list[int]) -> dict[str, Any]:
	"""Parse the coil test's second line, e.g. ' 05 01  "A" SIDE' (cells 1-2 test id, 4-5 step, 8-15 side text)."""
	test_id = decode_digits(segments, (1, 2))
	step = decode_digits(segments, (4, 5))
	tail = normalize(decode_alpha(segments[8:16]))
	return {"test_id": test_id, "step": step, "side_text": tail}
