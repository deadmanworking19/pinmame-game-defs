"""Build the compact Lord of the Rings flash-lamp test evidence from its two retained harness runs.

Each run walks the ROM's own DIAG > TEST FLASH LAMPS on one driver: ``lotr`` (10.00, the 2003
production machine) and ``lotr_le`` (10.02, the 2009 Limited Edition). Entering the test shows
CYCLING FLASHERS and pulses every flasher the firmware knows; the next Begin Test returns to the menu.
Comparing the two sets is what separates the editions: 10.00 never drives public solenoid 28, while
10.02 drives 28 in every cycle, alongside 14 - the address the Limited Edition's wiring moved its
right Helm's Deep flasher to.

Each cited DMD frame is pinned below by its pixel digest together with the text it was read as; a
rerun whose frames differ is refused rather than relabelled.

    python -B tools/lotr_flash_test_evidence.py --write
    python -B tools/lotr_flash_test_evidence.py --check
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
ROM_ARCHIVE_SHA256 = {
	"lotr": "f9a390c1ac9c7ab48b2c810f847d23761c34ab7431d48ed77524e2fb3deda26c",
	"lotr_le": "4999a0032bef06bf00bab90e069e65a676e48959333c338b13ef601a1cc31cc6",
}
HARNESS = "lord-of-the-rings-2003/completion-2026-10-22/harness"
# The flashers each firmware's own test pulses on every CYCLING FLASHERS step.
COMMON_FLASHERS = [14, 23, 25, 26, 27, 29, 30, 31, 32]
RUNS = {
	"lotr": {
		"machine_id": "stern.lord-of-the-rings.2003",
		"run": f"{HARNESS}/flash-test-lotr.json",
		"sha256": "cab1a3b6d33a0f5e0c10da8ef3da825371d571b70ab293e635c86ea581a3154b",
		"scenario": "tools/harness-scenarios/whitestar/lotr-flash-test.json",
		"evidence": "evidence/runtime/whitestar/lord-of-the-rings-flash-test.json",
		"flashers": COMMON_FLASHERS,
	},
	"lotr_le": {
		"machine_id": "stern.lord-of-the-rings-limited-edition.2009",
		"run": f"{HARNESS}/flash-explore-lotr_le.json",
		"sha256": "fa7f39065344204560b2723def0826b4a5d52535921ac75c12aa54c9f27d30b9",
		"scenario": "tools/harness-scenarios/whitestar/lotr-le-flash-test.json",
		"evidence": "evidence/runtime/whitestar/lord-of-the-rings-limited-edition-flash-test.json",
		"flashers": sorted(COMMON_FLASHERS + [28]),
	},
}
CYCLING = "CYCLING FLASHERS / PREV QUIT ?"
MENU = "DIAG / TEST FLASH LAMPS"
# Frame pixel digest -> the text it reads. The test blinks its highlight, so each screen has several
# frames; every one was read from the retained frame at 3x.
FRAMES = {
	"4a4c07f6c3f1c564b89d009a0e9617c994f66a890b9e3f5776f4ae72d849b113": CYCLING,
	"662e15d2ae2daf02d9330f8dfe5ee6c99cd1c494c191c4c68a6e35ff64f1e0ab": CYCLING,
	"86d3c6ea5a93afe5ec29f24cc0104f2cce67c63f75ddc0be98519aa47cb40150": CYCLING,
	"cf0fc05adf1d83e4154076ca0c415d21406f8a2badadf148de86dfbab3e05d85": CYCLING,
	"d920eb8f1bdd198037f50b811f373bc51bcd386ad390d72438141f9eedb0873f": CYCLING,
	"dd76a91b1b4e6812613043ec9ef71363107c08216333232605d99b55114619de": CYCLING,
	"11c80a5fa15073e5dd0c1be8b8d6196de5c2521cf983e1f213b26256b177f8ce": MENU,
	"5e221863e40edebd490c7495a9f2cbed0e0ac11b0ccf2488241f3962db611779": MENU,
	"71920227676014ee9fab568140253f4b3caafb7aed67b4d7fb37c08fe273e867": MENU,
	"8af466a95ca911be35da0c2d64a2e4fd895abe79f543990d0d1f939a9352f9d8": MENU,
	"b65febfaa126abae2471cdf8deae17dbab12a63cf91f3b4b276e56d05f95c898": MENU,
}
# The steps cited: the menu the walk lands on, then entering the test and every Begin Test after it.
CITED = ["diagnostics right 3", "enter flash test", *(f"flash test advance {n}" for n in range(1, 16))]


def _pulsed(step: dict) -> list[int]:
	return sorted(entry["number"] for entry in step["transitions"]["solenoids"])


def build(driver: str, run_path: Path) -> dict:
	spec = RUNS[driver]
	payload = run_path.read_bytes()
	if hashlib.sha256(payload).hexdigest() != spec["sha256"]:
		raise SystemExit(f"retained flash-test run changed: {run_path}")
	run = json.loads(payload)
	if run["failure"] is not None or run["game"] != driver or run["library_sha256"] != LIBRARY_SHA256:
		raise SystemExit(f"the retained run is not the successful pinned {driver} flash-lamp test run")
	if run["scenario"]["sha256"] != hashlib.sha256((ROOT / spec["scenario"]).read_bytes()).hexdigest():
		raise SystemExit(f"{spec['scenario']} is not the scenario the retained run executed")
	steps = {step["label"]: step for step in run["steps"]}
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	cited, cycles = [], 0
	for label in CITED:
		frame = snapshots[label]["displays"][0]
		text = FRAMES.get(frame["pixel_sha256"])
		if text is None:
			raise SystemExit(f"{driver} {label}: frame {frame['pixel_sha256']} has no pinned reading")
		pulsed = _pulsed(steps[label])
		if label == "diagnostics right 3":
			if text != MENU or pulsed:
				raise SystemExit(f"{driver}: the walk did not land on TEST FLASH LAMPS")
		elif text == CYCLING:
			if pulsed != spec["flashers"]:
				raise SystemExit(f"{driver} {label}: CYCLING FLASHERS pulsed {pulsed}, not {spec['flashers']}")
			cycles += 1
		elif pulsed not in ([], [25]):
			# Back at the menu only the three-bulb pop-bumper flasher can still be finishing its pulse.
			raise SystemExit(f"{driver} {label}: the menu step pulsed {pulsed}")
		cited.append({"label": label, "display_index": frame["index"], "pixel_sha256": frame["pixel_sha256"],
		              "nonzero_pixels": frame["nonzero_pixels"], "interpreted_text": text,
		              "active_solenoid_addresses": sorted(snapshots[label]["active_solenoids"])})
	if cycles != 8:
		raise SystemExit(f"{driver}: expected eight CYCLING FLASHERS steps, saw {cycles}")
	seen = sorted({number for label in CITED for number in _pulsed(steps[label])})
	edition = (
		"10.00 is the 2003 production machine's firmware. Its test never pulses 28, which the 2003 coils chart prints NOT USED."
		if driver == "lotr" else
		"10.02 is the 2009 Limited Edition's firmware. Its test pulses 28, the address the Limited Edition's wiring gives the right Helm's Deep flasher, in every cycle, and still pulses 14, the 2003 machine's address for that flasher."
	)
	return {
		"driver_ids": [driver],
		"extractor": {"id": "tools/lotr_flash_test_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [spec["machine_id"]],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": f"python tools/run_pinmame_harness.py --library <libpinmame> --game {driver} --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario {spec['scenario']} --dmd-dir <external-dmd-dir> --watch-switch -3 --watch-switch -1 --watch-switch 0 --output <external-run.json>. Every input is a direct write to the dedicated Begin Test (0) and Service Credit (-1) switches, with Memory Protect (-3) held at 0.",
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": LIBRARY_REVISION, "sha256": LIBRARY_SHA256},
			"game": driver,
			"observations": {
				"diagnostic_snapshots": cited,
				"display_indices_seen": [0],
				"runs": {
					"flash-test": {
						"note": f"The walk lands on TEST FLASH LAMPS; each Begin Test then alternates between CYCLING FLASHERS, which pulses every flasher the firmware's test knows, and the menu. All eight CYCLING FLASHERS steps pulse exactly solenoids {', '.join(str(n) for n in spec['flashers'])}. {edition}",
						"limitation": "The test pulses what the firmware believes is fitted. It proves which public addresses this firmware drives in its own flash test, not which load a particular cabinet has wired to them.",
						"solenoid_addresses_seen": seen,
					},
				},
				"service_language": "English",
			},
			"raw_runs": [{
				"action_count": run["scenario"]["action_count"],
				"name": f"{driver}-flash-test",
				"nvram_initialization": "empty; the run created its own isolated PinMAME state directory",
				"retained_from": f"external:pinmame-review-artifacts/{spec['run']}",
				"scenario_path": spec["scenario"],
				"scenario_sha256": run["scenario"]["sha256"],
				"self_test_pulses": 0,
				"sha256": spec["sha256"],
				"snapshot_count": len(run["snapshots"]),
				"watch_switches": run["watch_switches"],
			}],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256[driver],
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{spec['run']}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": LIBRARY_REVISION,
			"sha256": spec["sha256"],
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
	for driver, spec in RUNS.items():
		evidence = build(driver, artifacts / spec["run"])
		path = ROOT / spec["evidence"]
		if args.write:
			write_json(path, evidence)
			print(f"Wrote {spec['evidence']}")
		elif not path.is_file() or json.loads(path.read_text(encoding="utf-8")) != evidence:
			raise SystemExit(f"{spec['evidence']} does not match the retained run")
	if args.check:
		print("Lord of the Rings flash-lamp test evidence matches its retained runs.")


if __name__ == "__main__":
	main()
