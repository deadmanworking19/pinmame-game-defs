"""Derive the compact Harley-Davidson (Sega) runtime evidence from the retained raw harl_a13 harness runs.

The Sega machine runs firmware 1.03 (``harl_a13``), the manual's original A1.03 game ROM with display A1.04. Its runs
repeat the Stern record's harl_a40 scenarios on this ROM and add three Portals service walks: the Switch Test, which
prints every matrix switch's name and wire colours as it closes, the Single Lamp Test, which steps through lamps 1-80,
and the Single Coil Test, which names and fires every driver. The raw runs live under the external review-artifacts root
(``harley-davidson-sega-1999/harness/<run>/``). This tool reuses ``tools/harley_davidson_runtime_evidence.py`` for the
checks every run must pass (the committed scenario, the pinned binary, the built-in mechanism mask, no failure block, and
a pinned pixel SHA-256 for every frame the curator read) and adds what the service walks need:

- every Single Lamp Test step must change the lamp it names and no other lamp but the one it leaves; the step's lamp
  changes are appended to its observation label, because the named-action schema records solenoids only;
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
MACHINE_ID = "sega.harley-davidson.1999"
GAME = "harl_a13"
HARNESS_DIRECTORY = "harley-davidson-sega-1999/harness"
FRAME_READINGS_PATH = ROOT / "tools/seeds/sega/harley-davidson-1999-frame-readings.json"
DOCUMENT_PATH = "evidence/runtime/whitestar/harley-davidson-harl-a13-service-tests-and-gameplay.json"
ROM_ARCHIVE_SHA256 = "8027994701250356303a4eb68ae1c37cd0080afbffe13ca9364b58647ba9996f"
# Retained run directory -> (SHA-256 of its manifest.json, built-in mechanism mask).
RUNS = {
	"harl-a13-switch-test": ("d3e4b343183379b899b81dafb77bc0166cff92aa21aa51638d5faecd633b0000", 0),
	"harl-a13-switch-test-41-45": ("552fddb8c2c546d04308539bc39aa8a9b83454149754d50e2489bb3a9996a936", 0),
	"harl-a13-single-lamp-test": ("d4079f66909b6a2095ef01e9c5af86cfc2f548c600038a65a12f07cf78795b2a", 0),
	"harl-a13-single-coil-test": ("0ec2c3d74fd4ef1b202d551a983ac9b6cf638cc0632e7692c2e07b7bd61300c0", 0),
	"harl-a13-motorcycle-home-search": ("7c6294ab9cbdf27ed2f6d005a5089b01e019f8f386a998783261a3582ce18c72", 0),
	"harl-a13-motorcycle-up-at-boot": ("29032972a2c601a023c57eca688f762405ec012e3d719a95076a0a7f8bef63f4", 0),
	"harl-a13-motorcycle-down-at-boot": ("4af1d07fc26af68e337d60268921bbe6af3096e6e52a074285d70bc80c446592", 0),
	"harl-a13-motorcycle-ball-start-lift": ("1efbe869e10df960b0bbeacdcca6a5df6e5607d791ce426fc3fb1c133ae1025c", 0),
	"harl-a13-stacking-opto": ("00818176f2445d5e7e8a1752388b588d85e174ea32b649902cae085a2db7339f", 1),
	"harl-a13-gameplay": ("c1c40e8c7ef938140db0b3c12e2ce32e653977c081f6c52158bca33910b5692e", 1),
	"harl-a13-launch-scoop-opto": ("2f6687542adf22434b487c050f50230afe0e2b351162210ff866a10c24f0a06f", 1),
	"harl-a13-dedicated-switch-test": ("f836d2a18e26ce5de2c761384d2d1c5c62e75cbf01aa6f799e8c4a927c1606f3", 1),
	"harl-a13-ds5-probe": ("0068a077c09ff216e263272cae71b9e1a566dce113aa5c8ee04756c4038fbb53", 1),
}
LAMP_TEST_RUN = "harl-a13-single-lamp-test"
LAMP_STEP = re.compile(r"Black ENTER button \(public 0\) pressed on \+: lamp step (\d+)")
LAMP_COUNT = 80


def _lamp_test_changes(run: dict[str, Any]) -> dict[int, list[int]]:
	"""Scenario step number -> the lamps that changed during that Single Lamp Test step, refused unless each step lights
	the lamp it names (step 81 shows NONE and step 82 wraps to lamp 1) and changes no lamp but the one it leaves."""
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
		changed = sorted(item["number"] for item in step["transitions"].get("lamps", []))
		lit = [item["number"] for item in step["transitions"].get("lamps", []) if any(item["states"])]
		if named is not None and lit != [named]:
			raise RuntimeError(f"{LAMP_TEST_RUN}: lamp step {number} lit {lit}, not lamp {named}")
		if named is None and lit:
			raise RuntimeError(f"{LAMP_TEST_RUN}: lamp step {number} (NONE) lit {lit}")
		if not set(changed) <= {named, left} - {None}:
			raise RuntimeError(f"{LAMP_TEST_RUN}: lamp step {number} changed {changed}")
		changes[step["step"]] = changed
	if expected_step != LAMP_COUNT + 3:
		raise RuntimeError(f"{LAMP_TEST_RUN}: expected {LAMP_COUNT + 2} lamp steps")
	return changes


def build(root: Path) -> dict[str, Any]:
	document = base.build(
		root, GAME, ROM_ARCHIVE_SHA256, RUNS, machine_id=MACHINE_ID, harness_directory=HARNESS_DIRECTORY,
		frame_readings_path=FRAME_READINGS_PATH, extractor_id="tools/harley_davidson_sega_runtime_evidence.py",
	)
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
		raise SystemExit("Harley-Davidson (Sega) frame readings name a run this document does not derive")
	path = ROOT / DOCUMENT_PATH
	document = build(root)
	if args.check:
		if not path.is_file() or path.read_bytes() != canonical_bytes(document):
			raise SystemExit(f"Harley-Davidson (Sega) runtime evidence drift: {path}")
		print("Harley-Davidson (Sega) runtime evidence matches the retained raw runs.")
		return
	write_json(path, document)
	print(f"Wrote {path}")


if __name__ == "__main__":
	main()
