"""Derive the compact Terminator 3 runtime evidence from the retained raw term3 harness runs.

The runs boot ``term3`` (4.00, the newest US ROM in pinned PinMAME) on the pinned LibPinMAME build with keyboard and
mechanism handling off, and walk four Portals service tests, which print each address's name and wire colours: the
Switch Test, the Dedicated Switch Test, the Single Lamp Test and the Single Coil Test. Three more runs exercise the
trough's stacking opto, a ball serve with the gun-trigger launch, and a scripted game. The raw runs live under the
external review-artifacts root (``terminator-3-rise-of-the-machines-2003/harness/<run>/``). This tool reuses
``tools/harley_davidson_runtime_evidence.py`` for the checks every run must pass (the committed scenario, the pinned
binary, mechanism mask 0, no failure block, and a pinned pixel SHA-256 for every frame the curator read) and adds what
the service walks need:

- every Single Lamp Test step must light the lamp it names, and may change only the lamp the previous step selected,
  which must end dark (the test blinks the selected lamp, so the lamp it leaves can still be mid-blink);
  the step's lamp changes are appended to its observation label, because the named-action schema records solenoids only;
- lamps the Single Lamp Test drove are kept out of ``lamp_addresses_driven_outside_self_test``, which lists only what
  the ROM drove in the other runs.

``--check`` refuses drift between the raw runs and the committed document.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json
import harley_davidson_runtime_evidence as base

ROOT = base.ROOT
MACHINE_ID = "stern.terminator-3-rise-of-the-machines.2003"
GAME = "term3"
HARNESS_DIRECTORY = "terminator-3-rise-of-the-machines-2003/harness"
FRAME_READINGS_PATH = ROOT / "tools/seeds/stern/terminator-3-rise-of-the-machines-2003-frame-readings.json"
DOCUMENT_PATH = "evidence/runtime/whitestar/terminator-3-term3-service-tests-and-gameplay.json"
ROM_ARCHIVE_SHA256 = "64503f35d34ec28a6bb69eaf2b77e6e870dfff988c49364b07c2c6f0ed5a76b6"
# Retained run directory -> (SHA-256 of its manifest.json, built-in mechanism mask).
RUNS = {
	"term3-switch-test": ("2b56dc51fd0bf142e21cf0a0739fc7768f280d94740fb49457dd46a7fef6f9fa", 0),
	"term3-dedicated-switch-test": ("4392d52a214e4c203fa1a17cf1afdd51e1970e90a79c47ea188a1f9688d0e4b3", 0),
	"term3-single-lamp-test": ("850c1f3127882064b2d6a601b65a82b436d7f54443a0ed6a9c76ab332c56b63c", 0),
	"term3-single-coil-test": ("6d8dbaf14ff2b2398e4ea92b8f4289aac56f576294a97e1855d8581b8ae03749", 0),
	"term3-stacking-opto": ("9298cd4150c9b61fabf557a1ee9ce7b06caf6b5f9b7881d087127ee89f0875c2", 0),
	"term3-ball-serve": ("bb0df4fc125f28f535e4a1b8ffbab584301026f8559a9808597623d839fa4804", 0),
	"term3-gameplay": ("de605d80941a83534ca2c25625689db77f07181d5f63c63618c8fe4519a998b5", 0),
}
LAMP_TEST_RUN = "term3-single-lamp-test"
LAMP_STEP = re.compile(r"Black ENTER button \(public 0\) pressed on \+: lamp step (\d+)")
LAMP_COUNT = 80
COMMAND_TEMPLATE = (
	"python tools/run_pinmame_harness.py --library <libpinmame> --game term3 --rom-path <vpinmame-roms> --work-dir "
	"<new-isolated-state> --scenario tools/harness-scenarios/whitestar/<run>.json --dmd-dir <external-dmd-dir> "
	"--handle-mechanics 0 --output <external-run.json>; keyboard handling stays off. term3 has no built-in PinMAME "
	"mechanism, so every switch level in the runs is a host stimulus written by the scenario"
)


def _lamp_test_changes(run: dict[str, Any]) -> dict[int, list[int]]:
	"""Scenario step number -> the lamps that changed during that Single Lamp Test step, refused unless each step lights
	the lamp it names (step 81 shows NONE and step 82 wraps to lamp 1) and changes no other lamp but the one the previous
	step selected, which must end dark."""
	changes: dict[int, list[int]] = {}
	expected_step = 1
	for step in run["steps"]:
		match = LAMP_STEP.fullmatch(step["label"])
		if not match:
			continue
		number = int(match.group(1))
		if number != expected_step:
			raise RuntimeError(f"{LAMP_TEST_RUN}: lamp step {number} is out of order")
		expected_step += 1
		named = None if number == LAMP_COUNT + 1 else (number - 1) % (LAMP_COUNT + 1) + 1
		left = None if number == 1 else LAMP_COUNT if number == LAMP_COUNT + 1 else number - 1 if number <= LAMP_COUNT else None
		states = {item["number"]: item["states"] for item in step["transitions"].get("lamps", [])}
		if named is not None and not any(states.get(named, [])):
			raise RuntimeError(f"{LAMP_TEST_RUN}: lamp step {number} did not light lamp {named}")
		if named is None and states:
			raise RuntimeError(f"{LAMP_TEST_RUN}: lamp step {number} (NONE) changed lamps {sorted(states)}")
		if not set(states) <= {named, left} - {None} or (left in states and states[left][-1]):
			raise RuntimeError(f"{LAMP_TEST_RUN}: lamp step {number} changed {sorted(states)}")
		changes[step["step"]] = sorted(states)
	if expected_step != LAMP_COUNT + 3:
		raise RuntimeError(f"{LAMP_TEST_RUN}: expected {LAMP_COUNT + 2} lamp steps")
	return changes


def build(root: Path) -> dict[str, Any]:
	document = base.build(
		root, GAME, ROM_ARCHIVE_SHA256, RUNS, machine_id=MACHINE_ID, harness_directory=HARNESS_DIRECTORY,
		frame_readings_path=FRAME_READINGS_PATH, extractor_id="tools/terminator_3_runtime_evidence.py",
	)
	document["runtime"]["command_template"] = COMMAND_TEMPLATE
	observations = document["runtime"]["observations"]
	changes = _lamp_test_changes(load_json(root / HARNESS_DIRECTORY / LAMP_TEST_RUN / "run.json"))
	for observation in observations["named_action_observations"]:
		prefix, _, _ = observation["label"].partition(":")
		run_name, _, step = prefix.partition(" step ")
		if run_name == LAMP_TEST_RUN and int(step) in changes:
			observation["label"] += "; lamps changed during the step: " + (", ".join(map(str, changes[int(step)])) or "none")
	outside: set[int] = set()
	for name in RUNS:
		if name != LAMP_TEST_RUN:
			run = load_json(root / HARNESS_DIRECTORY / name / "run.json")
			outside.update(event["number"] for event in run["events"] if event["event"] == "lamp")
	observations["lamp_addresses_driven_outside_self_test"] = sorted(outside)
	return document


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="Refuse drift between the raw runs and the committed evidence")
	args = parser.parse_args()
	root = base.review_artifacts_root(required=True)
	assert root is not None
	if not set(load_json(FRAME_READINGS_PATH)["runs"]) <= set(RUNS):
		raise SystemExit("Terminator 3 frame readings name a run this document does not derive")
	path = ROOT / DOCUMENT_PATH
	document = build(root)
	if args.check:
		if not path.is_file() or path.read_bytes() != canonical_bytes(document):
			raise SystemExit(f"Terminator 3 runtime evidence drift: {path}")
		print("Terminator 3 runtime evidence matches the retained raw runs.")
		return
	write_json(path, document)
	print(f"Wrote {path}")


if __name__ == "__main__":
	main()
