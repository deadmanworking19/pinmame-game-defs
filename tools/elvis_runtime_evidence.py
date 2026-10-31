"""Derive the compact Elvis (Stern) runtime evidence from the retained raw harness runs.

Each raw run is a ``run.json`` the pinned LibPinMAME build wrote under the external review-artifacts root
(``elvis-2004/harness/<run>/``), beside a copy of its scenario and a canonical directory manifest. This tool checks that
every run executed the committed scenario on the pinned binary with the built-in mechanisms off and without a failure
block, then writes the per-step output transitions a curator cites. Switch 33 (Elvis Home) is special: LibPinMAME's
``elvis.c`` writes it itself, from its own count of the stepper phases written to solenoids 25-28, on every non-zero phase
write. A level of 33 that changes during a step the scenario did not write is therefore reported as an observed
emulator write, never as a host stimulus or a ROM observation, and only the Switch Test run may write 33 at all. A
diagnostic snapshot's ``interpreted_text`` is the curator's visual reading of that snapshot's retained DMD frame, pinned
with the frame's pixel SHA-256 in the frame-readings seed; the tool refuses a snapshot whose retained frame carries other
pixels or is blank. ``--check`` refuses drift between the raw runs and the committed documents.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from harley_davidson_runtime_evidence import (
	LIBRARY_SHA256,
	REVISION,
	SCENARIO_DIRECTORY,
	_addresses,
	_diagnostics,
	_levels,
	_load_run,
	_sha256,
	review_artifacts_root,
)
from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "stern.elvis.2004"
GAME = "elvis"
ROM_ARCHIVE_SHA256 = "41c03d0d0fab430d29ff382d86d091139f482e23e61964f43672c15fdf7eb34b"
HARNESS_DIRECTORY = "elvis-2004/harness"
FRAME_READINGS_PATH = ROOT / "tools/seeds/stern/elvis-2004-frame-readings.json"
DOCUMENT_PATH = "evidence/runtime/whitestar/elvis-service-tests-and-gameplay.json"
# Retained run directory -> SHA-256 of its manifest.json. Every run kept the built-in mechanisms off (mask 0).
RUNS = {
	"elvis-switch-test": "48aeb1628a2055d8f99b33eb0524d0c646ff87d8d7ab4b31e1624d39c8077b82",
	"elvis-switch-timing-probe": "c3f5e3602901a3942d67bdb200581113f9a3f2c6c5fb4d8f26fb079cbcc7ec87",
	"elvis-dedicated-switch-test": "c99c5cc5da4d36ea674eb0294f67a361a598493a57ce54d599c6870482b1b034",
	"elvis-single-coil-test": "c1247d97fe5c97346b30b0d4f0a4aa402a5089fb4d157f4802384283ac4e9f69",
	"elvis-single-lamp-test": "1aa40d05953353fac69cc84e3b2650ba494a2af39a8227d14ab4a482ca056566",
	"elvis-elvis-test": "8e64c2edd1c67b7e0b9101f47ee591d17a773bf796724ecb411ffcb864dc902d",
	"elvis-stacking-opto": "15b5ec75a3ab2268c8b64b5ad01dc27ae731045b692fbae95b00c07ad3c6fc1e",
	"elvis-gameplay": "1107ea371c63b9e4531275f288d676586e62522e800a6b87629a51f6e59ecf7e",
	"elvis-hound-dog-probe": "fcb00a9da6a59e7f23336a00a263aa5fd2bfa285bc830c7d2047d0f99dc79317",
}
# The Elvis Home switch, which elvis.c writes from its own model of the stepper.
EMULATOR_SWITCH = 33
# The only run that writes 33 itself: the Switch Test, during which the ROM writes no stepper phase after boot.
HOST_33_RUNS = ("elvis-switch-test",)
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch "
	"writes are host stimuli, never ROM observations, and every level of 33 the scenario did not write is LibPinMAME's own "
	"elvis.c stepper model. Each run directory's manifest (tools/build_external_evidence_manifest.py) lists the raw trace, "
	"the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)


def _actions(name: str, run: dict[str, Any]) -> list[dict[str, Any]]:
	"""One named-action observation per scenario step, in order, with every solenoid that changed during it."""
	scenario = load_json(ROOT / SCENARIO_DIRECTORY / f"{name}.json")
	steps, snapshots = run["steps"], run["snapshots"]
	if len(scenario["actions"]) != len(steps) or len(snapshots) != len(steps) + 1:
		raise RuntimeError(f"{name}: the run's steps do not match the scenario's actions")
	written = {action["switch"] for action in scenario["actions"] if "switch" in action}
	if EMULATOR_SWITCH in written and name not in HOST_33_RUNS:
		raise RuntimeError(f"{name}: the host wrote {EMULATOR_SWITCH}, which elvis.c owns in this run")
	if any(item["switch"] == EMULATOR_SWITCH for item in scenario.get("initial_switches", [])):
		raise RuntimeError(f"{name}: an initial level for {EMULATOR_SWITCH} would hide elvis.c's own write")
	stimulus = sorted({item["switch"] for item in scenario.get("initial_switches", [])} | written)
	held = scenario["initial_switches"][0]["switch"]
	observations = []
	for index, (action, step) in enumerate(zip(scenario["actions"], steps)):
		if snapshots[index + 1]["label"] != step["label"]:
			raise RuntimeError(f"{name}: snapshot {index + 1} does not belong to step {step['step']}")
		held = action.get("switch", held)
		transitions = step.get("transitions", {})
		changed = sorted(item["number"] for item in transitions.get("solenoids", []))
		active = sorted(item["number"] for item in transitions.get("solenoids", []) if any(item["states"]))
		before, after = _levels(snapshots[index]), _levels(snapshots[index + 1])
		emulated = []
		if EMULATOR_SWITCH in after and before.get(EMULATOR_SWITCH) != after[EMULATOR_SWITCH] and action.get("switch") != EMULATOR_SWITCH:
			emulated = [EMULATOR_SWITCH]
		label = f"{name} step {step['step']}: {step['label']}"
		if emulated:
			label += f"; LibPinMAME's elvis.c stepper model left {EMULATOR_SWITCH} at {after[EMULATOR_SWITCH]}"
		gi = [item for item in transitions.get("gis", []) if item["number"] == 0]
		if gi:
			label += f"; GI 0 states during the step: {', '.join(str(state) for state in gi[0]['states'])}"
		observations.append({
			"label": label,
			"input_kind": "switch",
			"input_address": held,
			"observed_switch_addresses": emulated,
			"host_stimulus_switch_addresses": stimulus,
			"active_solenoid_addresses": active,
			"transitioned_solenoid_addresses": changed,
			"result": "observed" if changed or emulated else "no_matching_transition",
		})
	return observations


def build(root: Path) -> dict[str, Any]:
	raw_runs = []
	observations: list[dict[str, Any]] = []
	diagnostics: list[dict[str, Any]] = []
	pins = load_json(FRAME_READINGS_PATH)["runs"]
	lamps: set[int] = set()
	solenoids: set[int] = set()
	gis: set[int] = set()
	displays: set[int] = set()
	for name, manifest_sha256 in RUNS.items():
		run, listed = _load_run(root, name, GAME, manifest_sha256, 0, HARNESS_DIRECTORY)
		scenario_path = f"{SCENARIO_DIRECTORY}/{name}.json"
		raw_runs.append({
			"name": name,
			"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{name}/run.json",
			"sha256": listed["run.json"],
			"scenario_path": scenario_path,
			"scenario_sha256": _sha256(ROOT / scenario_path),
			"initial_switches": run["initial_switches"],
			"watch_switches": run["watch_switches"],
			"nvram_initialization": "empty; each run created its own isolated PinMAME state directory",
			"action_count": len(run["steps"]),
			"snapshot_count": len(run["snapshots"]),
			"self_test_pulses": 0,
		})
		observations.extend(_actions(name, run))
		if name in pins:
			diagnostics.extend(_diagnostics(root, name, run, listed, pins[name], HARNESS_DIRECTORY))
		lamps.update(_addresses(run, "lamp"))
		solenoids.update(_addresses(run, "solenoid"))
		gis.update(_addresses(run, "gi"))
		displays.update(event["index"] for event in run["events"] if event["event"] == "display_available")
	last = list(RUNS)[-1]
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"machine_ids": [MACHINE_ID],
		"driver_ids": [GAME],
		"extractor": {"id": "tools/elvis_runtime_evidence.py", "version": 1},
		"switches": [],
		"outputs": [],
		"mechanisms": [],
		"states": [],
		"recreation_notes": [],
		"runtime": {
			"game": GAME,
			"command_template": (
				f"python tools/run_pinmame_harness.py --library <libpinmame> --game {GAME} --rom-path <vpinmame-roms> --work-dir "
				"<new-isolated-state> --scenario tools/harness-scenarios/whitestar/<run>.json --dmd-dir <external-dmd-dir> "
				"--handle-mechanics 0 --output <external-run.json>; keyboard handling stays off. Mask 0 in every run: elvis.c's "
				"stepper model is not a built-in mechanism and runs regardless, writing switch 33 whenever the ROM writes a "
				"non-zero stepper phase"
			),
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
			"raw_runs": raw_runs,
			"observations": {
				**({"diagnostic_snapshots": diagnostics} if diagnostics else {}),
				"display_indices_seen": sorted(displays),
				"lamp_addresses_seen": sorted(lamps),
				"solenoid_addresses_seen": sorted(solenoids),
				"gi_addresses_seen": sorted(gis),
				"named_action_observations": observations,
			},
		},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}",
			"sha256": RUNS[last],
			"license": "NOASSERTION",
			"quality": "validated",
			"attribution": ATTRIBUTION,
		},
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="Refuse drift between the raw runs and the committed evidence")
	args = parser.parse_args()
	root = review_artifacts_root(required=True)
	assert root is not None
	if not set(load_json(FRAME_READINGS_PATH)["runs"]) <= set(RUNS):
		raise SystemExit("Elvis frame readings name a run the document does not derive")
	path = ROOT / DOCUMENT_PATH
	document = build(root)
	if args.check:
		if not path.is_file() or path.read_bytes() != canonical_bytes(document):
			raise SystemExit(f"Elvis runtime evidence drift: {path}")
		print("Elvis runtime evidence matches the retained raw runs.")
		return
	write_json(path, document)
	print(f"Wrote {path}")


if __name__ == "__main__":
	main()
