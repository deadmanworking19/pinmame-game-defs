"""Build the compact Lord of the Rings LED Test evidence from its retained harness run.

The run (``tools/harness-scenarios/whitestar/lotr-led-test.json`` on ``lotr``) walks the ROM's own
LOTR TESTS > LED TEST: ALL ON, then LED #1 to LED #19, then ALL OFF. The manual's LED Test text says
LED #1 is the board's L1 and #2-#19 follow suit, so pairing each displayed number with the one public
lamp that rose on that step names every public address 81-99 by its factory designator.

Each cited DMD frame is pinned below by its pixel digest together with the text it was read as; a
rerun whose frames differ is refused rather than relabelled.

    python -B tools/lotr_led_test_evidence.py --write [--run <external lotr-led-test.json>]
    python -B tools/lotr_led_test_evidence.py --check [--run <external lotr-led-test.json>]
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

EVIDENCE_PATH = ROOT / "evidence/runtime/whitestar/lord-of-the-rings-led-test.json"
SCENARIO_PATH = ROOT / "tools/harness-scenarios/whitestar/lotr-led-test.json"
RUN_RELATIVE = "lord-of-the-rings-2003/completion-2026-10-22/harness/lotr-led-test.json"
RUN_SHA256 = "3c8ab5021eff93b1698a90a97a09531d7badc8fd38b379b073f408b43641b9ab"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
LIBRARY_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
ROM_ARCHIVE_SHA256 = "f9a390c1ac9c7ab48b2c810f847d23761c34ab7431d48ed77524e2fb3deda26c"

# Step label -> (frame pixel digest, the text the frame reads). Read at 2x from the retained frames.
READINGS = {
	"LED test advance 1": ("7b2b74375a2b1b41cb66fce0aaf4a47fee8f68e06ae6b83370d9debc83dd3700", "LED TEST / ALL ON"),
	"LED test advance 2": ("101ff8ad28afbd6874490e6dbeae2a78fcee4561c632960d8fbea56cf88b64ee", "LED TEST / LED #1"),
	"LED test advance 3": ("c44cd03d1fd16e5e2e7f6aa30386c1117173c85f32ce74840b46948bbca9708a", "LED TEST / LED #2"),
	"LED test advance 4": ("487b27621565ec4c71f2a82540e766de39d0498500bcf9c156568fada439b333", "LED TEST / LED #3"),
	"LED test advance 5": ("3492b60622f044d31cb44ec054b6553ff1b381208060fd6409f487bd5ad6028b", "LED TEST / LED #4"),
	"LED test advance 6": ("035f53f1a5fc9837474e46df2c11fafb49688f0c098ee6824082ed79e6849daf", "LED TEST / LED #5"),
	"LED test advance 7": ("4d6f77679f47296cf21209e42a8568272b57a62c995d151ba62689383085bc28", "LED TEST / LED #6"),
	"LED test advance 8": ("1147ecb15a16d384d9cfc6b3ba4af6ab183b7a07c2ccf23f82e6fdc191a51bfb", "LED TEST / LED #7"),
	"LED test advance 9": ("0f11ed1be090fc26f23400c5997416e2f8db6fcee206aaaf4b097cdb57c8fe80", "LED TEST / LED #8"),
	"LED test advance 10": ("4e45a72ca9a538a1b43aefbe9a1d0d0e17c3be887c726b97fc6533a210cd3add", "LED TEST / LED #9"),
	"LED test advance 11": ("866fb78a98246459eb1c84810d054fbc57479ca45530bbefa244b2e2fb37eb5c", "LED TEST / LED #10"),
	"LED test advance 12": ("65ef97b668901009fbc358b5e40b67e56616ad71ab6b51ed3bd48ebabcc1f8fe", "LED TEST / LED #11"),
	"LED test advance 13": ("b54e19480a373e29ba8c07bf2ffdd292a6820ed733da76f30dd8cd7314808038", "LED TEST / LED #12"),
	"LED test advance 14": ("9279efc29434791b7468abffb1f6029ad42ac3863ab1d50d047729d4d5f7e942", "LED TEST / LED #13"),
	"LED test advance 15": ("3319b3d6e1e87926202a455c9c8002c9a2f23ad087089d5729e5baba594795f5", "LED TEST / LED #14"),
	"LED test advance 16": ("176efd236a92cb762e651ae19fc445b03aefb7b1f2f6c6ff5da0b7b91d5edf14", "LED TEST / LED #15"),
	"LED test advance 17": ("b8a7cfab5ceec09fdf3465f54fa78c2c10d1222cc3b169d947b99b975dbeb6d4", "LED TEST / LED #16"),
	"LED test advance 18": ("792ea366910f2a5e53865caaffe114e633d0b8a26f84ec4410b934b7b60f23b0", "LED TEST / LED #17"),
	"LED test advance 19": ("09ba311a4f6035cc9ebd53cd7e9aef93deb78d608757f2ea29e598335e2793c2", "LED TEST / LED #18"),
	"LED test advance 20": ("1558089f9d7f03aacce2f31a544957fb30d5cc26ecc243b811d0a9ea44aefbdd", "LED TEST / LED #19"),
	"LED test advance 21": ("844f451358eb48199cd5c177bcf2c704b1e00045a1658e144ef2b24e33477ed4", "LED TEST / ALL OFF"),
}


def default_run() -> Path:
	return resolve_working_root(ROOT) / "review-artifacts" / RUN_RELATIVE


def _raised(step: dict) -> list[int]:
	return sorted(entry["number"] for entry in step["transitions"]["lamps"] if 1 in entry["states"])


def build(run_path: Path) -> dict:
	payload = run_path.read_bytes()
	if hashlib.sha256(payload).hexdigest() != RUN_SHA256:
		raise SystemExit(f"retained LED Test run changed: {run_path}")
	run = json.loads(payload)
	if run["failure"] is not None or run["game"] != "lotr" or run["library_sha256"] != LIBRARY_SHA256:
		raise SystemExit("the retained run is not the successful pinned lotr LED Test run")
	if run["scenario"]["sha256"] != hashlib.sha256(SCENARIO_PATH.read_bytes()).hexdigest():
		raise SystemExit("the committed scenario is not the one the retained run executed")
	steps = {step["label"]: step for step in run["steps"]}
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	snapshots_out, named = [], {}
	for label, (digest, text) in READINGS.items():
		frame = snapshots[label]["displays"][0]
		if frame["pixel_sha256"] != digest:
			raise SystemExit(f"{label}: frame differs from the pinned reading {text!r}")
		snapshots_out.append({"label": label, "display_index": frame["index"], "pixel_sha256": digest,
		                      "nonzero_pixels": frame["nonzero_pixels"], "interpreted_text": text, "active_solenoid_addresses": []})
		raised = _raised(steps[label])
		if text.endswith("ALL ON"):
			if raised != list(range(81, 100)):
				raise SystemExit(f"ALL ON raised {raised}, not exactly 81-99")
		elif text.endswith("ALL OFF"):
			if raised:
				raise SystemExit(f"ALL OFF raised {raised}")
		else:
			number = int(text.rsplit("#", 1)[1])
			if len(raised) != 1:
				raise SystemExit(f"{label} ({text}) raised {raised}, not exactly one lamp")
			named[f"led-l{number:02d}"] = raised[0]
	if sorted(named.values()) != list(range(81, 100)):
		raise SystemExit("LED #1-#19 do not cover public lamps 81-99 exactly once")
	return {
		"driver_ids": ["lotr"],
		"extractor": {"id": "tools/lotr_led_test_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["stern.lord-of-the-rings.2003"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game lotr --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/whitestar/lotr-led-test.json --dmd-dir <external-dmd-dir> --boot-wait 0 --observe 0 --output <external-run.json>. Keyboard handling stays off: every input is a direct write to the dedicated Begin Test (0) and Service Credit (-1) switches, with Memory Protect (-3) held at 0.",
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": LIBRARY_REVISION, "sha256": LIBRARY_SHA256},
			"game": "lotr",
			"observations": {
				"diagnostic_snapshots": snapshots_out,
				"display_indices_seen": [0],
				"lamp_addresses_seen": sorted({entry["number"] for step in run["steps"] for entry in step["transitions"]["lamps"] if 1 in entry["states"]}),
				"named_output_addresses": dict(sorted(named.items())),
				"runs": {
					"led-test": {
						"note": "Each LED TEST advance shows the selected test on the DMD and blinks only that LED: ALL ON raises exactly public lamps 81-99, LED #n raises exactly one of them, and ALL OFF raises none. named_output_addresses pairs led-lNN with the public lamp LED #NN raised; the manual's LED Test text (PDF 42) identifies LED #1 as the board's L1 and #2-#19 as following suit.",
						"limitation": "The run identifies which public lamp each factory designator is. It says nothing about where on the playfield each LED sits; that comes from the factory drawings.",
					},
				},
				"service_language": "English",
			},
			"raw_runs": [{
				"action_count": run["scenario"]["action_count"],
				"name": "lotr-led-test",
				"nvram_initialization": "empty; the run created its own isolated PinMAME state directory",
				"retained_from": f"external:pinmame-review-artifacts/{RUN_RELATIVE}",
				"scenario_path": "tools/harness-scenarios/whitestar/lotr-led-test.json",
				"scenario_sha256": run["scenario"]["sha256"],
				"self_test_pulses": 0,
				"sha256": RUN_SHA256,
				"snapshot_count": len(run["snapshots"]),
				"watch_switches": run["watch_switches"],
			}],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{RUN_RELATIVE}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": LIBRARY_REVISION,
			"sha256": RUN_SHA256,
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
	parser.add_argument("--run", type=Path, default=None)
	args = parser.parse_args()
	evidence = build(args.run or default_run())
	if args.write:
		write_json(EVIDENCE_PATH, evidence)
		print(f"Wrote {EVIDENCE_PATH.relative_to(ROOT)}")
		return
	if json.loads(EVIDENCE_PATH.read_text(encoding="utf-8")) != evidence:
		raise SystemExit(f"{EVIDENCE_PATH.relative_to(ROOT)} does not match the retained run")
	print("Lord of the Rings LED Test evidence matches its retained run.")


if __name__ == "__main__":
	main()
