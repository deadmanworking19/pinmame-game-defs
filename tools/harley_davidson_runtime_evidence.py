"""Derive the compact Harley-Davidson (Stern) runtime evidence from the retained raw harness runs.

Each raw run is a ``run.json`` the pinned LibPinMAME build wrote under the external review-artifacts root
(``harley-davidson-stern-1999/harness/<run>/``), beside a copy of its scenario and a canonical directory manifest. This
tool checks that every run executed the committed scenario on the pinned binary with its expected built-in mechanism
mask and without a failure block, then writes the per-step output transitions a curator cites: one document for the
harl_a40 runs and one for the harl_a30 run, because a runtime record carries one game. Runs with PinMAME's motorcycle
simulation enabled (``--handle-mechanics 1``) report the Motor Up/Down levels that simulation wrote as observed switch
changes, never as host stimuli. A diagnostic snapshot's ``interpreted_text`` is the curator's visual reading of that
snapshot's retained DMD frame, pinned with the frame's pixel SHA-256 in the frame-readings seed; the tool refuses a
snapshot whose retained frame carries other pixels or is blank. ``--check`` refuses drift between the raw runs and the
committed documents.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "stern.harley-davidson.1999"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
HARNESS_DIRECTORY = "harley-davidson-stern-1999/harness"
SCENARIO_DIRECTORY = "tools/harness-scenarios/whitestar"
FRAME_READINGS_PATH = ROOT / "tools/seeds/stern/harley-davidson-1999-frame-readings.json"
# Document -> (game, ROM archive SHA-256, {retained run directory: (SHA-256 of its manifest.json, built-in mechanism mask)}).
DOCUMENTS = {
	"evidence/runtime/whitestar/harley-davidson-harl-a40-motorcycle-and-gameplay.json": (
		"harl_a40", "44b92f640fea2b9769fcdb50b2745b50c6d56be747efc360fd8acf20f7b3133f", {
			"harl-a40-motorcycle-home-search": ("b5b1652b85c5ea18cf933168ae8fea9cafa8acd541c872e85f403843ae0c43bc", 0),
			"harl-a40-motorcycle-up-at-boot": ("e33a9563155600a0808659178623d1ea9c8e0e40ced4f9e3777107952e94a303", 0),
			"harl-a40-motorcycle-down-at-boot": ("ab722436d9dc30c86c5c6b5d3de40ca1ba7643755c93ecc0a14f1499b4b56cdd", 0),
			"harl-a40-motorcycle-ball-start-lift": ("c5cf2be5b730b80633be12bbf6816c1295668fa0058717a0a09b445a87d29721", 0),
			"harl-a40-stacking-opto": ("f58375074e35f7ac681f56ce61caeffa8d904c89bdb4870591369868d2b280c2", 1),
			"harl-a40-gameplay": ("64ad60eb6410fc13edc32dedf90696bf2c008aaee64ff770bfd76d2d31ca34e4", 1),
			"harl-a40-launch-scoop-opto": ("33081f05b4e3e9976e1e1aed002f4656d3cee6b5eea43e96907b2c80a03d09ee", 1),
			"harl-a40-ds5-probe": ("03eb45b89755b60c573863128f26133b6cd89fb203fc03981cf985719508598e", 1),
			"harl-a40-dedicated-switch-test": ("0eac4e3108c51f6bda3ca464a4adb0b5d7741bc6b9b82f9349802c9da7713c85", 1),
		},
	),
	"evidence/runtime/whitestar/harley-davidson-harl-a30-gameplay.json": (
		"harl_a30", "741d57f93a6ac346e07decc3ae668bbfe145a6c717c0c52b96537bc5a91ff07c", {
			"harl-a30-gameplay": ("099691b8988b6cddea825f9a72714893e8b14de6e75e4fea61971f5cf1f5923d", 1),
		},
	),
}
# The Motor Up and Motor Down switches, which harley_handleMech writes while the built-in mechanism is enabled.
SIMULATED_SWITCHES = (35, 36)
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch "
	"writes are host stimuli, never ROM observations. Each run directory's manifest (tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def review_artifacts_root(required: bool) -> Path | None:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_REVIEW_ARTIFACTS_ROOT is required to read the retained Harley-Davidson harness runs")
		return None
	return Path(value).expanduser().resolve()


def _load_run(root: Path, name: str, game: str, manifest_sha256: str, mechanics: int) -> tuple[dict[str, Any], dict[str, str]]:
	directory = root / HARNESS_DIRECTORY / name
	manifest = directory / "manifest.json"
	if _sha256(manifest) != manifest_sha256:
		raise RuntimeError(f"{name}: retained manifest does not match its pinned SHA-256")
	listed = {entry["path"]: entry["sha256"] for entry in load_json(manifest)["files"]}
	for relative, digest in listed.items():
		if _sha256(directory / relative) != digest:
			raise RuntimeError(f"{name}: retained file {relative} changed")
	run = load_json(directory / "run.json")
	scenario = ROOT / SCENARIO_DIRECTORY / f"{name}.json"
	if load_json(directory / "scenario.json") != load_json(scenario) or run["scenario"]["sha256"] != _sha256(scenario):
		raise RuntimeError(f"{name}: the retained scenario differs from the committed one")
	if run.get("failure") is not None or run.get("game") != game or run.get("library_sha256") != LIBRARY_SHA256:
		raise RuntimeError(f"{name}: not a successful pinned run of {game}")
	if run.get("handle_mechanics") != mechanics:
		raise RuntimeError(f"{name}: expected built-in mechanism mask {mechanics}, found {run.get('handle_mechanics')}")
	return run, listed


def _levels(snapshot: dict[str, Any]) -> dict[int, int]:
	return {item["number"]: item["state"] for item in snapshot["watched_switches"]}


def _actions(name: str, run: dict[str, Any], mechanics: int) -> list[dict[str, Any]]:
	"""One named-action observation per scenario step, in order, with every solenoid that changed during it.

	A wait step names the switch whose host-held level it observes: the one the previous step wrote, or the first
	initial switch before any write. With the built-in mechanism enabled, a Motor Up/Down level that differs between the
	snapshots around a step is the simulation's write, so it is reported as observed rather than as stimulus.
	"""
	scenario = load_json(ROOT / SCENARIO_DIRECTORY / f"{name}.json")
	steps, snapshots = run["steps"], run["snapshots"]
	if len(scenario["actions"]) != len(steps) or len(snapshots) != len(steps) + 1:
		raise RuntimeError(f"{name}: the run's steps do not match the scenario's actions")
	written = {action["switch"] for action in scenario["actions"] if "switch" in action}
	if mechanics and written & set(SIMULATED_SWITCHES):
		raise RuntimeError(f"{name}: the host wrote a switch the built-in mechanism owns")
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
		simulated = sorted(address for address in SIMULATED_SWITCHES if mechanics and before.get(address) != after.get(address))
		label = f"{name} step {step['step']}: {step['label']}"
		if simulated:
			label += "; the built-in motorcycle simulation left " + ", ".join(f"{address} at {after[address]}" for address in simulated)
		gi = [item for item in transitions.get("gis", []) if item["number"] == 0]
		if gi:
			label += f"; GI 0 states during the step: {', '.join(str(state) for state in gi[0]['states'])}"
		observations.append({
			"label": label,
			"input_kind": "switch",
			"input_address": held,
			"observed_switch_addresses": simulated,
			"host_stimulus_switch_addresses": stimulus,
			"active_solenoid_addresses": active,
			"transitioned_solenoid_addresses": changed,
			"result": "observed" if changed else "no_matching_transition",
		})
	return observations


def _diagnostics(root: Path, name: str, run: dict[str, Any], listed: dict[str, str], pins: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
	"""The curator's reading of each pinned frame, in run order, refused unless the retained PGM carries the snapshot's pixels."""
	snapshots = []
	for snapshot in run["snapshots"]:
		pin = pins.get(snapshot["label"])
		if pin is None:
			continue
		label = snapshot["label"]
		displays = [item for item in snapshot["displays"] if item["index"] == 0]
		if len(displays) != 1:
			raise RuntimeError(f"{name}: snapshot {label!r} must carry display 0 exactly once")
		relative = "dmd/" + Path(displays[0]["artifact"].replace("\\", "/")).name
		if relative not in listed:
			raise RuntimeError(f"{name}: the frame for {label!r} is not in the run's manifest")
		data = (root / HARNESS_DIRECTORY / name / relative).read_bytes()
		pixels = data[len(data) - 128 * 32:]
		if not data.startswith(b"P5\n128 32\n") or hashlib.sha256(pixels).hexdigest() != displays[0]["pixel_sha256"]:
			raise RuntimeError(f"{name}: the retained frame for {label!r} does not carry the snapshot's pixels")
		if displays[0]["nonzero_pixels"] == 0 or not any(pixels):
			raise RuntimeError(f"{name}: a reading cannot cite a blank frame: {label!r}")
		if pin["pixel_sha256"] != displays[0]["pixel_sha256"]:
			raise RuntimeError(f"{name}: snapshot {label!r} does not carry the frame the curator read as {pin['reading']!r}")
		snapshots.append({
			"label": f"{name} snapshot: {label}",
			"display_index": 0,
			"pixel_sha256": displays[0]["pixel_sha256"],
			"nonzero_pixels": displays[0]["nonzero_pixels"],
			"interpreted_text": pin["reading"],
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
		})
	if len(snapshots) != len(pins) or len({item["label"] for item in snapshots}) != len(pins):
		raise RuntimeError(f"{name}: every pinned frame must be exactly one snapshot of the run")
	return snapshots


def _addresses(run: dict[str, Any], kind: str) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == kind})


def build(root: Path, game: str, rom_archive_sha256: str, runs: dict[str, tuple[str, int]]) -> dict[str, Any]:
	raw_runs = []
	observations: list[dict[str, Any]] = []
	diagnostics: list[dict[str, Any]] = []
	pins = load_json(FRAME_READINGS_PATH)["runs"]
	lamps: set[int] = set()
	solenoids: set[int] = set()
	gis: set[int] = set()
	displays: set[int] = set()
	for name, (manifest_sha256, mechanics) in runs.items():
		run, listed = _load_run(root, name, game, manifest_sha256, mechanics)
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
		observations.extend(_actions(name, run, mechanics))
		if name in pins:
			diagnostics.extend(_diagnostics(root, name, run, listed, pins[name]))
		lamps.update(_addresses(run, "lamp"))
		solenoids.update(_addresses(run, "solenoid"))
		gis.update(_addresses(run, "gi"))
		displays.update(event["index"] for event in run["events"] if event["event"] == "display_available")
	masks = ", ".join(f"{name} {mechanics}" for name, (_, mechanics) in runs.items())
	last = list(runs)[-1]
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"machine_ids": [MACHINE_ID],
		"driver_ids": [game],
		"extractor": {"id": "tools/harley_davidson_runtime_evidence.py", "version": 1},
		"switches": [],
		"outputs": [],
		"mechanisms": [],
		"states": [],
		"recreation_notes": [],
		"runtime": {
			"game": game,
			"command_template": (
				f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game} --rom-path <vpinmame-roms> --work-dir "
				"<new-isolated-state> --scenario tools/harness-scenarios/whitestar/<run>.json --dmd-dir <external-dmd-dir> "
				"--handle-mechanics <mask> --output <external-run.json>; keyboard handling stays off. Mask per run: "
				f"{masks}. Mask 1 enables PinMAME's harley_handleMech, which writes the Motor Up (35) and Motor Down (36) "
				"switches from its own model of the lift while solenoid 19 is on; mask 0 leaves both to the scenario"
			),
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"rom_archive_sha256": rom_archive_sha256,
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
			"sha256": runs[last][0],
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
	documented = {name for _, _, runs in DOCUMENTS.values() for name in runs}
	if not set(load_json(FRAME_READINGS_PATH)["runs"]) <= documented:
		raise SystemExit("Harley-Davidson frame readings name a run no document derives")
	for relative, (game, rom_archive_sha256, runs) in DOCUMENTS.items():
		path = ROOT / relative
		document = build(root, game, rom_archive_sha256, runs)
		if args.check:
			if not path.is_file() or path.read_bytes() != canonical_bytes(document):
				raise SystemExit(f"Harley-Davidson runtime evidence drift: {path}")
			continue
		write_json(path, document)
		print(f"Wrote {path}")
	if args.check:
		print("Harley-Davidson runtime evidence matches the retained raw runs.")


if __name__ == "__main__":
	main()
