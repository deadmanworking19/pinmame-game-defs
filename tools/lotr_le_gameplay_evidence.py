"""Build the compact Lord of the Rings Limited Edition gameplay evidence from its two retained harness runs.

The same scenario plays a game on ``lotr_le`` (10.02, the 2009 Limited Edition) and on ``lotr``
(10.00, the 2003 production machine): it boots with four balls in the trough, starts a game, serves
a ball and closes every ordinary playfield switch twice. The comparison is about the right Helm's
Deep flasher. 10.00 drives it on public solenoid 14 and never touches 28. 10.02 drives 14 and 28
together: every on and every off transition of one has the same transition of the other at the same
emulated time, so 28 is a mirror of 14 in play, not only in the flash-lamp test. That is why a
Limited Edition, whose loom moves the flasher to driver 28 and leaves 14 unconnected, lights it,
and why the firmware still works in a cabinet wired like the 2003 machine.

    python -B tools/lotr_le_gameplay_evidence.py --write
    python -B tools/lotr_le_gameplay_evidence.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import write_json  # noqa: E402
from pinmame_game_defs.workspace import resolve_working_root  # noqa: E402

LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
LIBRARY_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
ROM_ARCHIVE_SHA256 = "4999a0032bef06bf00bab90e069e65a676e48959333c338b13ef601a1cc31cc6"
HARNESS = "lord-of-the-rings-limited-edition-2009/curation-2026-10-23/harness"
EVIDENCE = "evidence/runtime/whitestar/lord-of-the-rings-limited-edition-gameplay.json"
# Two transitions are the same event when the emulator reports them within this many seconds; the
# runner timestamps each callback separately, so simultaneous outputs differ in the fourth decimal.
SAME_INSTANT_S = 0.001
RUNS = {
	"lotr_le": {
		"run": f"{HARNESS}/gameplay-lotr_le/run.json",
		"sha256": "979721dbaba82b50761e488160d978cedad9698293b7cc97b4603209a4dd50c3",
		"scenario": "tools/harness-scenarios/whitestar/lotr-le-gameplay.json",
	},
	"lotr": {
		"run": f"{HARNESS}/gameplay-lotr/run.json",
		"sha256": "4d00cdf778b7bebede5becc10eb949b5ec2e30f5a767e17551dbc580cf751bcb",
		"scenario": "tools/harness-scenarios/whitestar/lotr-gameplay.json",
	},
}


def _transitions(run: dict, number: int) -> list[tuple[float, int]]:
	return [(event["time_s"], event["state"]) for event in run["events"]
	        if event.get("event") == "solenoid" and event["number"] == number]


def _mirrored(first: list[tuple[float, int]], second: list[tuple[float, int]]) -> bool:
	return len(first) == len(second) and all(
		state_a == state_b and abs(time_a - time_b) <= SAME_INSTANT_S
		for (time_a, state_a), (time_b, state_b) in zip(first, second)
	)


def _load(driver: str, artifacts: Path) -> dict:
	spec = RUNS[driver]
	payload = (artifacts / spec["run"]).read_bytes()
	if hashlib.sha256(payload).hexdigest() != spec["sha256"]:
		raise SystemExit(f"retained gameplay run changed: {spec['run']}")
	run = json.loads(payload)
	if run["failure"] is not None or run["game"] != driver or run["library_sha256"] != LIBRARY_SHA256:
		raise SystemExit(f"the retained run is not the successful pinned {driver} gameplay run")
	if run["scenario"]["sha256"] != hashlib.sha256((ROOT / spec["scenario"]).read_bytes()).hexdigest():
		raise SystemExit(f"{spec['scenario']} is not the scenario the retained run executed")
	return run


def _on_sequence(run: dict) -> list[int]:
	return [event["number"] for event in run["events"] if event.get("event") == "solenoid" and event["state"]]


def build(artifacts: Path) -> dict:
	le, original = _load("lotr_le", artifacts), _load("lotr", artifacts)
	le14, le28 = _transitions(le, 14), _transitions(le, 28)
	if not le14 or not _mirrored(le14, le28):
		raise SystemExit("10.02 does not drive solenoid 28 as an exact mirror of 14 in the retained run")
	original14, original28 = _transitions(original, 14), _transitions(original, 28)
	if not original14 or original28:
		raise SystemExit("10.00 must drive solenoid 14 and never 28 in the retained run")
	activations = sum(state for _, state in le14)
	raw_runs, runs = [], {}
	for driver, run in (("lotr_le", le), ("lotr", original)):
		spec = RUNS[driver]
		name = f"{driver.replace('_', '-')}-gameplay"
		raw_runs.append({
			"action_count": run["scenario"]["action_count"],
			"initial_switches": run["initial_switches"],
			"name": name,
			"nvram_initialization": "empty; the run created its own isolated PinMAME state directory",
			"retained_from": f"external:pinmame-review-artifacts/{spec['run']}",
			"scenario_path": spec["scenario"],
			"scenario_sha256": run["scenario"]["sha256"],
			"self_test_pulses": 0,
			"sha256": spec["sha256"],
			"snapshot_count": len(run["snapshots"]),
			"watch_switches": run["watch_switches"],
		})
		seen = sorted({number for number in _on_sequence(run)})
		if driver == "lotr_le":
			note = (f"10.02, the Limited Edition's firmware. Solenoid 14 switched on {activations} times during the game, and every on and off "
			        f"transition of 14 has the same transition of 28 within {SAME_INSTANT_S * 1000:g} ms of emulated time, and vice versa: "
			        "the firmware drives 28 as a mirror of 14, so the right Helm's Deep flasher lights on either driver.")
		else:
			note = (f"10.00, the 2003 production machine's firmware, under the same scenario. Solenoid 14 switched on "
			        f"{sum(state for _, state in original14)} times and 28 never did.")
		runs[name] = {
			"limitation": "A transition proves which public address the firmware drives under this scenario, not which load a particular cabinet wires to it. Absence of an address in this run is not proof that it is unused.",
			"note": note,
			"ordered_solenoid_on_sequence": _on_sequence(run),
			"solenoid_addresses_seen": seen,
		}
	return {
		"driver_ids": ["lotr_le"],
		"extractor": {"id": "tools/lotr_le_gameplay_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["stern.lord-of-the-rings-limited-edition.2009"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game <lotr_le|lotr> --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario <tools/harness-scenarios/whitestar/lotr-le-gameplay.json|lotr-gameplay.json> --output <external-run.json>. Every input is a direct switch write; the scenario's initial switches put four balls on trough switches 11-14.",
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": LIBRARY_REVISION, "sha256": LIBRARY_SHA256},
			"game": "lotr_le",
			"observations": {"runs": runs, "service_language": "English"},
			"raw_runs": raw_runs,
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{RUNS['lotr_le']['run']}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": LIBRARY_REVISION,
			"sha256": RUNS["lotr_le"]["sha256"],
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	parser.add_argument("--review-artifacts", type=Path, default=None)
	args = parser.parse_args()
	artifacts = args.review_artifacts or resolve_working_root(ROOT) / "review-artifacts"
	evidence = build(artifacts)
	path = ROOT / EVIDENCE
	if args.write:
		write_json(path, evidence)
		print(f"Wrote {EVIDENCE}")
	elif not path.is_file() or json.loads(path.read_text(encoding="utf-8")) != evidence:
		raise SystemExit(f"{EVIDENCE} does not match the retained runs")
	else:
		print("Lord of the Rings Limited Edition gameplay evidence matches its retained runs.")


if __name__ == "__main__":
	main()
