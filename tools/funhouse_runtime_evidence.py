"""Derive the compact FunHouse G.I. test evidence from the retained raw harness run.

The document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts
root), checks that it ran the committed scenario, the pinned binary and the expected mechanism mask, and writes the derived
observations beside the other WPC-Alpha runtime evidence. FunHouse has two sixteen-segment alphanumeric lines, so every
reading is decoded from the snapshot's raw segment words with the font below; a run whose decoded text differs from the
reading pinned here is refused. The tool also refuses a raw run whose transitions no longer support a stated observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json
from build_external_evidence_manifest import check_manifest
from run_pinmame_harness import SEGMENT_16_CHARACTERS

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.funhouse.1990"
GAME = "fh_l9"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "210f6009a1b6b67d7c89564fe673f3e7d75318e6cbdf2bb1d86e2ac0d9daa20d"
HARNESS_DIRECTORY = "funhouse-1990/harness"
RUN_DIRECTORY = "gi-test/fh_l9"
SCENARIO = "tools/harness-scenarios/wpc-alpha/fh-gi-test.json"
EVIDENCE_PATH = ROOT / "evidence/runtime/wpc-alpha/funhouse-fh_l9-gi-test.json"
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are "
	"host stimuli, never ROM observations. Display text is decoded from the retained sixteen-segment words with the harness font "
	"table, the ROM's own glyph 0x0006 for the numeral 1 and bit 0x0080 for a character's period; the font draws 0 and O, and 5 "
	"and S, with the same segments, so each reading is compared after folding those digits. The exact external directory manifest "
	"(built by tools/build_external_evidence_manifest.py) lists the raw trace, the copied scenario and the isolated mutable state, "
	"with no ROM bytes."
)
NVRAM_NOTE = (
	"empty; the run created its own isolated PinMAME state directory, so the ROM restored its factory settings before the "
	"scenario left the message loop with Escape"
)
COMMAND = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game fh_l9 --rom-path <vpinmame-roms> "
	"--work-dir <new-isolated-state> --handle-mechanics 0 --scenario tools/harness-scenarios/wpc-alpha/fh-gi-test.json "
	"--watch-switch 5 --watch-switch 7 --watch-switch 8 --watch-switch 13 --watch-switch 22 --output <external-run.json>. "
	"T.6 GEN'L. ILLUM. in stop mode first steps all illumination through eight brightness levels, then each circuit in turn; "
	"Start on a circuit shows its wire colours, and each further Up its playfield and backbox connector pins, its fuse and its "
	"driver transistor."
)
IDENTIFICATION_LABEL = "Enter 1 (game identification)"
IDENTIFICATION = ("FUN HOUSE", "50003 REV. L-9")
ALL_LABEL = "Enter 4 (start T.6, ALL ILLUMINATION)"
ALL_TEXT = ("ALL ILLUMINATION", "T.6 BRIGHT=1 STOP")
# T.6 circuits in the order the test steps them: (public G.I. output, name line, Start screen, playfield pins, backbox
# pins, fuse, driver). Each reading is the curator's reading of the decoded segments, digits as printed.
GI_CIRCUITS = (
	(0, "BACKGLASS UPPER", "WHT-BRN BRN", "P.F. J120-7 120-1", "B.B. J121-7 121-1", "F110 5 AMP S.B.", "DRIVER Q18"),
	(1, "RUDY / BACKGLASS", "WHT-ORN ORN", "P.F. J120-8 120-2", "B.B. J121-8 121-2", "F109 5 AMP S.B.", "DRIVER Q10"),
	(2, "REAR PLAYFIELD", "WHT-YEL YEL", "P.F. J120-9 120-3", "B.B. J121-9 121-3", "F108 5 AMP S.B.", "DRIVER Q14"),
	(3, "BACKGLASS CENTER", "WHT-GRN GRN", "P.F. J120-10 120-5", "B.B. J121-10 121-5", "F107 5 AMP S.B.", "DRIVER Q16"),
	(4, "FRONT PLAYFIELD", "WHT-VIO VIO", "P.F. J120-11 120-6", "B.B. J121-11 121-6", "F106 5 AMP S.B.", "DRIVER Q12"),
)
INFO_PAGES = ("playfield connector", "backbox connector", "fuse", "driver")
UPPER_DISPLAYS = (0, 1, 2)
LOWER_DISPLAYS = (3, 4, 5)
# The ROM draws the numeral 1 with segments b and c only, which the harness table does not list.
ROM_GLYPHS = {0x0006: "1"}
PERIOD_BIT = 0x0080
# In stop mode each circuit takes eight Up presses: six step its brightness, the seventh changes nothing at full
# brightness, and the eighth selects the next circuit.
PRESSES_PER_CIRCUIT = 8
BRIGHTNESS_PRESSES = 6


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _glyph(value: int) -> str | None:
	if value in ROM_GLYPHS:
		return ROM_GLYPHS[value]
	if value in SEGMENT_16_CHARACTERS:
		return SEGMENT_16_CHARACTERS[value]
	base = value & ~PERIOD_BIT
	if value & PERIOD_BIT and (base in ROM_GLYPHS or base in SEGMENT_16_CHARACTERS):
		return (ROM_GLYPHS.get(base) or SEGMENT_16_CHARACTERS[base]) + "."
	return None


def decode(segments: list[int]) -> str:
	glyphs = [_glyph(value) for value in segments]
	if any(glyph is None for glyph in glyphs):
		raise ValueError(f"undecodable segment word in {segments}")
	return "".join(glyphs)


def _fold(text: str) -> str:
	"""Normalize whitespace and fold the digits this font cannot tell from letters."""
	return " ".join(text.split()).replace("0", "O").replace("5", "S")


def _load_run(directory: Path) -> dict[str, Any]:
	run_path = directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / SCENARIO
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful FunHouse {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != 0:
		raise ValueError(f"unexpected built-in mechanism mask in {run_path}")
	return run


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


def _changed(step: dict[str, Any], channel: str) -> set[int]:
	return {item["number"] for item in step["transitions"][channel]}


def _responses(snapshot: dict[str, Any], indices: tuple[int, ...], expected: str) -> list[dict[str, Any]]:
	"""Decode one display line, refuse it unless it reads ``expected``, and return its raw segment responses."""
	displays = {item["index"]: item for item in snapshot["displays"]}
	if any(index not in displays or "segments" not in displays[index] for index in indices):
		raise ValueError(f"snapshot {snapshot['label']!r} lacks segment displays {indices}")
	text = "".join(decode(displays[index]["segments"]) for index in indices)
	if _fold(text) != _fold(expected):
		raise ValueError(f"snapshot {snapshot['label']!r} reads {text!r}, not {expected!r}")
	return [
		{
			"snapshot_label": snapshot["label"],
			"display_index": index,
			"segments": list(displays[index]["segments"]),
			"decoded_segment_positions": list(range(len(displays[index]["segments"]))),
			"interpreted_text": decode(displays[index]["segments"]),
		}
		for index in indices
	]


def _observation(label: str, inputs: list[int], responses: list[dict[str, Any]] | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": inputs, "input_address": inputs[0], "input_kind": "switch",
		"label": label, "observed_switch_addresses": [], "result": "observed",
		"transitioned_solenoid_addresses": [],
	}
	if responses:
		item["display_responses"] = responses
	return item


def _check_brightness_presses(run: dict[str, Any], selected_at: int, channels: set[int], name: str) -> None:
	"""Refuse unless every brightness press after ``selected_at`` changes exactly ``channels`` and the last one nothing."""
	presses = range(selected_at + 1, selected_at + PRESSES_PER_CIRCUIT)
	changed = [_changed(_step(run, f"T.6 Up {press}"), "gis") for press in presses]
	expected = [channels] * BRIGHTNESS_PRESSES + [set()] * (PRESSES_PER_CIRCUIT - 1 - BRIGHTNESS_PRESSES)
	if changed != expected:
		raise ValueError(f"T.6 {name} must step public GI {sorted(channels)} alone, saw {changed}")


def build_observations(run: dict[str, Any]) -> dict[str, Any]:
	named = []
	identification = _snapshot(run, IDENTIFICATION_LABEL)
	named.append(_observation(
		f"Game identification after the fresh-NVRAM restart: {IDENTIFICATION[0]} / {IDENTIFICATION[1]}",
		[8],
		_responses(identification, UPPER_DISPLAYS, IDENTIFICATION[0]) + _responses(identification, LOWER_DISPLAYS, IDENTIFICATION[1]),
	))
	start = _snapshot(run, ALL_LABEL)
	if sorted(start["active_gis"]) != [0, 1, 2, 3, 4]:
		raise ValueError("T.6 must start with every circuit lit")
	_check_brightness_presses(run, 0, {0, 1, 2, 3, 4}, "ALL ILLUMINATION")
	named.append(_observation(
		f"T.6 {ALL_TEXT[0]} ({ALL_TEXT[1]}): Up steps the brightness of public GI 0, 1, 2, 3 and 4 together",
		[7],
		_responses(start, UPPER_DISPLAYS, ALL_TEXT[0]) + _responses(start, LOWER_DISPLAYS, ALL_TEXT[1]),
	))
	previous = {0, 1, 2, 3, 4}
	for order, (channel, name, wires, playfield, backbox, fuse, driver) in enumerate(GI_CIRCUITS):
		label = f"T.6 Up {PRESSES_PER_CIRCUIT * (order + 1)}"
		selection = _snapshot(run, label)
		if selection["active_gis"] != [channel]:
			raise ValueError(f"selecting {name} must leave public GI {channel} alone lit, saw {selection['active_gis']}")
		if _changed(_step(run, label), "gis") != previous | {channel}:
			raise ValueError(f"selecting {name} must change only public GI {sorted(previous | {channel})}")
		previous = {channel}
		responses = _responses(selection, UPPER_DISPLAYS, name)
		pages = [(f"String {order} Start (wire colours)", wires)] + [
			(f"String {order} info Up {page} ({title})", text)
			for page, (title, text) in enumerate(zip(INFO_PAGES, (playfield, backbox, fuse, driver)), start=1)
		]
		for label, text in pages:
			snapshot = _snapshot(run, label)
			if snapshot["active_gis"] != [channel]:
				raise ValueError(f"{label} must keep public GI {channel} alone lit, saw {snapshot['active_gis']}")
			responses += _responses(snapshot, UPPER_DISPLAYS, name) + _responses(snapshot, LOWER_DISPLAYS, text)
		_check_brightness_presses(run, PRESSES_PER_CIRCUIT * (order + 1), {channel}, name)
		named.append(_observation(
			f"T.6 circuit {name}: Up steps the brightness of public GI {channel} alone, and Start then Up show "
			f"{wires} / {playfield} / {backbox} / {fuse} / {driver}",
			[7, 13],
			responses,
		))
	if _changed(_step(run, f"T.6 Up {PRESSES_PER_CIRCUIT * (len(GI_CIRCUITS) + 1)}"), "gis") != {0, 1, 2, 3, 4}:
		raise ValueError("the press after the last circuit must return T.6 to ALL ILLUMINATION")
	seen = sorted({event["number"] for event in run["events"] if event["event"] == "gi"})
	return {"gi_addresses_seen": seen, "named_action_observations": named}


def build(review_root: Path) -> dict[str, Any]:
	path = review_root / HARNESS_DIRECTORY / RUN_DIRECTORY
	check_manifest(path, GAME)
	run = _load_run(path)
	observations = build_observations(run)
	run_sha = _sha256(path / "run.json")
	manifest_sha = _sha256(path / "manifest.json")
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/funhouse_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": COMMAND,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": GAME,
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": "fh_l9-gi-test",
					"nvram_initialization": NVRAM_NOTE,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{RUN_DIRECTORY}/run.json",
					"scenario_path": SCENARIO,
					"scenario_sha256": run["scenario"]["sha256"],
					"self_test_pulses": 0,
					"sha256": run_sha,
					"snapshot_count": len(run["snapshots"]),
					"watch_switches": run["watch_switches"],
				}
			],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": f"{ATTRIBUTION} Exact external directory manifest {RUN_DIRECTORY}/manifest.json SHA-256 {manifest_sha}.",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{RUN_DIRECTORY}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"sha256": run_sha,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


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
	document = build(root)
	if args.write:
		write_json(EVIDENCE_PATH, document)
	elif not EVIDENCE_PATH.is_file() or EVIDENCE_PATH.read_bytes() != canonical_bytes(document):
		raise SystemExit(f"FunHouse compact runtime evidence drift: {EVIDENCE_PATH}")
	else:
		print("FunHouse G.I. test runtime evidence matches the retained run.")


if __name__ == "__main__":
	main()
