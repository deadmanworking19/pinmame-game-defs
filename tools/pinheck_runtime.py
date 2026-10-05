"""Compact runtime evidence for the four Spooky Pinball pinHeck games.

Reads the retained harness runs (tools/pinheck_harness_scenarios.py scenarios, recorded under
``<review-artifacts>/<machine-id>/session-20261005/runtime/<game>-<test>/``) and derives, for every step,
what the ROM did: the public outputs that changed and, for each switch closure, which pixels of the
held display frame differ from the frame before it. The Switch Edge test draws a matrix closure as one
cell of an 8x8 grid laid out like the factory chart (column 7 at the left, row 0 at the top), so the
changed cell decodes the factory switch number the ROM read for that public address.

Displayed texts are not decoded here: tools/pinheck_frame_texts.json holds the curator's visual reading
of the frames, keyed by game, test and step label. This builder copies each reading next to the step's
frame SHA-256 and refuses a reading for a step the run does not have.

``--write <review-artifacts-root>`` rebuilds tools/pinheck_runtime.json; ``--check`` refuses drift.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "pinheck_runtime.json"
TEXTS = ROOT / "tools" / "pinheck_frame_texts.json"
SESSION = "session-20261005"
GAMES = {
	"amh": ("spooky-pinball.america-s-most-haunted.2014", ("switch", "solenoid", "lamp", "servo", "rgb", "game")),
	"dominos": ("spooky-pinball.domino-s-spectacular-pinball-adventure.2016", ("switch", "solenoid", "lamp", "servo", "rgb", "game")),
	"rzspook": ("spooky-pinball.rob-zombie-s-spookshow-international.2016", ("switch", "solenoid", "lamp", "servo", "rgb", "game")),
	"jetsons": ("spooky-pinball.the-jetsons.2017", ("switch", "solenoid", "lamp", "rgb", "game")),
}
MATRIX = [d * 10 + r for d in range(1, 9) for r in range(1, 9)]
CABINET = [*range(1, 9), *range(91, 98)]
GRID_RIGHT = 38
# Switch Edge grid layout per firmware: x of matrix column 7 (columns step +4 towards column 0), and the x of the
# cabinet column holding cabinet inputs 0-7 and of the one holding 8-15. Rows step +4 from y=1 everywhere.
LAYOUTS = {"amh": (1, 37, 33), "dominos": (1, 37, 33), "rzspook": (1, 37, 33), "jetsons": (9, 5, 1)}


def read_frame(path: Path) -> tuple[int, int, list[tuple[int, ...]]]:
	"""Parse the harness's binary PGM (P5) or PPM (P6) snapshot into (width, height, pixels)."""
	data = path.read_bytes()
	fields: list[bytes] = []
	offset = 0
	while len(fields) < 4:
		while data[offset:offset + 1].isspace():
			offset += 1
		end = offset
		while not data[end:end + 1].isspace():
			end += 1
		fields.append(data[offset:end])
		offset = end
	offset += 1
	magic, width, height = fields[0], int(fields[1]), int(fields[2])
	channels = 3 if magic == b"P6" else 1
	body = data[offset:offset + width * height * channels]
	pixels = [tuple(body[i:i + channels]) for i in range(0, len(body), channels)]
	return width, height, pixels


def changed_dots(before: Path, after: Path) -> list[list[int]]:
	"""Top-left corners of the switch-grid dots (2x2 pixels on a 4-pixel lattice from x=1, y=1) that changed."""
	width, _height, a = read_frame(before)
	_, _, b = read_frame(after)
	dots = {((i % width) - (i % width - 1) % 4, (i // width) - (i // width - 1) % 4)
	        for i, (p, q) in enumerate(zip(a, b)) if p != q and i % width <= GRID_RIGHT and i // width < 32}
	return [list(dot) for dot in sorted(dots)]


def frame_of(snapshot: dict[str, Any], run_dir: Path) -> tuple[Path, str]:
	display = snapshot["displays"][0]
	return run_dir / "dmd" / Path(display["artifact"]).name, display["pixel_sha256"]


def summarize(run_dir: Path) -> dict[str, Any]:
	run = json.loads((run_dir / "run.json").read_bytes())
	if run["failure"] is not None:
		raise ValueError(f"{run_dir.name}: failed run")
	snapshots = run["snapshots"]
	steps = []
	for step in run["steps"]:
		label = step["label"]
		if label.startswith(("Next after item", "Menu step")):
			continue
		index = next(i for i, snap in enumerate(snapshots) if snap["label"] == label)
		path, digest = frame_of(snapshots[index], run_dir)
		item: dict[str, Any] = {"label": label, "frame_sha256": digest,
		                        "solenoid_peaks": {str(t["number"]): max(t["states"]) for t in step["transitions"]["solenoids"]},
		                        "lamps_changed": sorted(t["number"] for t in step["transitions"]["lamps"]),
		                        "active_solenoids": sorted(snapshots[index]["active_solenoids"]),
		                        "active_lamps": sorted(snapshots[index]["active_lamps"])}
		if step.get("snapshot_while_held") or any(snap["label"] == f"{label} (held)" for snap in snapshots):
			held_index = next(i for i, snap in enumerate(snapshots) if snap["label"] == f"{label} (held)")
			held_path, held_digest = frame_of(snapshots[held_index], run_dir)
			before_path, _ = frame_of(snapshots[held_index - 1], run_dir)
			item["held_frame_sha256"] = held_digest
			item["held_changed_dots"] = changed_dots(before_path, held_path)
			del item["active_solenoids"], item["active_lamps"]
		steps.append(item)
	return {"run_sha256": hashlib.sha256((run_dir / "run.json").read_bytes()).hexdigest(),
	        "scenario_sha256": hashlib.sha256((run_dir / "scenario.json").read_bytes()).hexdigest(),
	        "library_sha256": run["library_sha256"], "manifest_sha256": hashlib.sha256((run_dir / "manifest.json").read_bytes()).hexdigest(),
	        "steps": steps}


def decode_switches(game: str, switch_steps: list[dict[str, Any]]) -> dict[str, Any]:
	"""Decode every closure's changed grid dot into the factory number the ROM drew, and compare with the formulas."""
	column7, cabinet_low, cabinet_high = LAYOUTS[game]
	decoded: dict[str, list[str]] = {}
	for step in switch_steps:
		if "held_changed_dots" not in step:
			continue
		names = []
		for x, y in step["held_changed_dots"]:
			row = (y - 1) // 4
			if x == cabinet_low:
				names.append(f"cabinet {row}")
			elif x == cabinet_high:
				names.append(f"cabinet {row + 8}")
			elif column7 <= x <= column7 + 28:
				names.append(f"matrix {(7 - (x - column7) // 4) * 8 + row}")
			else:
				names.append(f"other {x},{y}")
		decoded[step["label"].split()[1]] = names
	expected = {str(n): [f"matrix {(n // 10 - 1) * 8 + n % 10 - 1}"] for n in MATRIX}
	expected.update({str(n): [f"cabinet {n if n < 9 else n - 82}"] for n in CABINET if n != 1})
	return {"drawn_by_public": decoded,
	        "matrix_matches_formula": all(decoded.get(key) == value for key, value in expected.items() if int(key) in MATRIX),
	        "mismatches": {key: decoded.get(key) for key, value in expected.items() if decoded.get(key) != value}}


def build(review_root: Path) -> dict[str, Any]:
	texts = json.loads(TEXTS.read_bytes()) if TEXTS.is_file() else {}
	result: dict[str, Any] = {"format": "pinheck-runtime-summary", "version": 1, "games": {}}
	for game, (machine, tests) in GAMES.items():
		runs = {}
		for test in tests:
			run_dir = review_root / machine / SESSION / "runtime" / f"{game}-{test}"
			runs[test] = summarize(run_dir)
			readings = texts.get(game, {}).get(test, {})
			by_label = {step["label"]: step for step in runs[test]["steps"]}
			held = {label.removesuffix(" (held)"): text for label, text in readings.items() if label.endswith(" (held)")}
			plain = {label: text for label, text in readings.items() if not label.endswith(" (held)")}
			unknown = sorted((set(plain) - set(by_label)) | {label for label in held if "held_frame_sha256" not in by_label.get(label, {})})
			if unknown:
				raise ValueError(f"{game} {test}: readings for steps the run does not have: {unknown[:5]}")
			for label, text in plain.items():
				by_label[label]["displayed_text"] = text
			for label, text in held.items():
				by_label[label]["held_displayed_text"] = text
		runs["switch"]["grid"] = decode_switches(game, runs["switch"]["steps"])
		result["games"][game] = {"machine_id": machine, "runs": runs}
	return result


def payload(review_root: Path) -> bytes:
	return (json.dumps(build(review_root), indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode()


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("review_root", type=Path)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	args = parser.parse_args()
	data = payload(args.review_root)
	if args.check:
		if OUTPUT.read_bytes() != data:
			sys.exit("pinHeck runtime summary drift")
		print("pinHeck runtime summary matches")
	else:
		OUTPUT.write_bytes(data)
		print(f"wrote {OUTPUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
	main()
