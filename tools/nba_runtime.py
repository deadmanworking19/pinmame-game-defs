"""Summarize the retained Stern NBA (2009) harness runs into compact committed evidence.

The raw runs (``run.json``, DMD frames, isolated state) stay under the working root's
``review-artifacts/nba-2009/harness/<kind>-<driver>/``; this script copies the scenario beside
each run, seals the directory with ``build_external_evidence_manifest`` and writes one summary per
run to ``evidence/runtime/sam/``. Every ``interpreted_text`` is a visual reading of the frame whose
pixel hash it carries (the readings are transcribed in
``evidence/excerpts/stern.nba.2009/rom-service-tests.md``); the pixel hashes and nonzero-pixel
counts are copied from the raw run, so a misreading cannot change them. The two fast-flip
diagnostic runs under ``review-artifacts/nba-2009/diagnostics/`` are sealed the same way.

Usage (needs ``PINMAME_REVIEW_ARTIFACTS_ROOT``)::

	python tools/nba_runtime.py --write
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
	sys.path.insert(0, str(TOOLS))

import build_external_evidence_manifest as manifest  # noqa: E402
import nba_devices as dev  # noqa: E402

ROOT = TOOLS.parent
RUNTIME_ROOT = ROOT / "evidence/runtime/sam"
MACHINE_ID = "stern.nba.2009"
PINNED_LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
SCENARIOS = {
	"switch": ROOT / "tools/harness-scenarios/stern/nba-2009-switch-test-sweep.json",
	"coil": ROOT / "tools/harness-scenarios/stern/nba-2009-coil-sweep.json",
	"lamp": ROOT / "tools/harness-scenarios/stern/nba-2009-lamp-sweep.json",
	"gameplay": ROOT / "tools/harness-scenarios/stern/nba-2009-gameplay-probe.json",
	"pops": ROOT / "tools/harness-scenarios/stern/nba-2009-bumper-sling-probe.json",
}
RUN_DIRECTORIES = {"switch": "switch-sweep", "coil": "coil-sweep", "lamp": "lamp-sweep", "gameplay": "gameplay-probe", "pops": "bumper-sling-probe"}
SWEEP_DRIVERS = ("nba_802", "nba_801", "nba_700", "nba_600", "nba_500")
VERSIONS = {"nba_802": "V8.02", "nba_801": "V8.01", "nba_700": "V7.0", "nba_600": "V6.0", "nba_500": "V5.0"}
HARNESS_RELATIVE = "nba-2009/harness"
DIAGNOSTICS_RELATIVE = "nba-2009/diagnostics"
SWITCH_ADDRESSES = [*range(1, 73), *range(81, 89), -7, -6, -5, -4]
COIL_POSITIONS = 40


def sha256_file(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def artifacts_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
	return Path(value)


def snapshot_map(run: dict[str, Any]) -> dict[str, dict[str, Any]]:
	return {snapshot["label"]: snapshot for snapshot in run["snapshots"]}


def step_map(run: dict[str, Any]) -> dict[str, dict[str, Any]]:
	return {step["label"]: step for step in run["steps"]}


def solenoid_changes(step: dict[str, Any]) -> dict[int, int]:
	return {item["number"]: len(item["states"]) for item in step.get("transitions", {}).get("solenoids", [])}


def snapshot_record(snapshot: dict[str, Any], label: str, text: str) -> dict[str, Any]:
	display = snapshot["displays"][0]
	return {"active_solenoid_addresses": sorted(snapshot.get("active_solenoids", [])), "display_index": display["index"], "interpreted_text": text, "label": label, "nonzero_pixels": display["nonzero_pixels"], "pixel_sha256": display["pixel_sha256"]}


def boot_text(driver: str) -> str:
	return f"NBA / U.S.A. {VERSIONS[driver]} / ENGLISH"


_ROM_SHA_CACHE: dict[str, str] = {}


def rom_archive_sha256(driver: str) -> str:
	if driver not in _ROM_SHA_CACHE:
		roms = os.environ.get("PINMAME_ROM_LIBRARY_ROOT", r"L:\Visual Pinball\VPinMAME\roms")
		_ROM_SHA_CACHE[driver] = sha256_file(Path(roms) / f"{driver}.zip")
	return _ROM_SHA_CACHE[driver]


def command(driver: str, scenario: Path) -> str:
	return f"python tools/run_pinmame_harness.py --library <libpinmame> --game {driver} --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --handle-mechanics 0 --ready-timeout 90 --scenario {scenario.relative_to(ROOT).as_posix()} --dmd-dir <external-dmd-dir> --output <external-run.json>"


def seal(directory: Path, driver: str, scenario: Path | None) -> str:
	if scenario is not None:
		shutil.copyfile(scenario, directory / "scenario.json")
	return manifest.write_manifest(directory, driver)


def load_run(root: Path, kind: str, driver: str) -> tuple[Path, dict[str, Any]]:
	path = root / HARNESS_RELATIVE / f"{RUN_DIRECTORIES[kind]}-{driver}" / "run.json"
	if not path.is_file():
		raise SystemExit(f"missing retained run {path}")
	run = json.loads(path.read_text(encoding="utf-8"))
	if run.get("failure"):
		raise SystemExit(f"{path}: the run failed")
	if run["library_sha256"] != PINNED_LIBRARY_SHA256:
		raise SystemExit(f"{path}: unexpected library")
	if run["game"] != driver:
		raise SystemExit(f"{path}: driver {run['game']!r}")
	scenario = SCENARIOS[kind]
	if run["scenario"]["sha256"] != sha256_file(scenario):
		raise SystemExit(f"{path}: scenario differs from {scenario}")
	return path, run


def evidence_shell(name: str, driver: str, run: dict[str, Any], run_path: Path, directory_digest: str, command_template: str, observations: dict[str, Any], scenario_path: Path | None, extra_raw: dict[str, Any], relative: str = HARNESS_RELATIVE) -> dict[str, Any]:
	raw = {
		"action_count": run["scenario"]["action_count"] if run.get("scenario") else 0,
		"initial_switches": run["initial_switches"],
		"name": name,
		"nvram_initialization": "empty; the run created its own isolated PinMAME state directory and the ROM reached attract mode without a factory-reset message to dismiss",
		"retained_from": f"external:pinmame-review-artifacts/{relative}/{run_path.parent.name}/run.json",
		"self_test_pulses": 0,
		"sha256": sha256_file(run_path),
		"snapshot_count": len(run["snapshots"]),
	}
	if scenario_path is not None:
		raw["scenario_path"] = scenario_path.relative_to(ROOT).as_posix()
		raw["scenario_sha256"] = run["scenario"]["sha256"]
	raw.update(extra_raw)
	return {
		"driver_ids": [driver], "extractor": {"id": "tools/run_pinmame_harness.py", "version": 1}, "format": "pinmame-machine-evidence", "machine_ids": [MACHINE_ID],
		"mechanisms": [], "outputs": [], "recreation_notes": [],
		"runtime": {
			"command_template": command_template,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": run["library_sha256"]},
			"game": driver, "observations": observations, "raw_runs": [raw],
			"rom_archive_sha256": rom_archive_sha256(driver),
		},
		"source": {
			"attribution": f"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation is counted key pulses; every retained DMD frame cited here was read visually and each diagnostic snapshot's interpreted_text is that reading of its pixel SHA-256. Exact external directory manifest {run_path.parent.name}/manifest.json SHA-256 {directory_digest} (built by tools/build_external_evidence_manifest.py); it lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes.",
			"kind": "runtime_scenario", "license": "NOASSERTION", "path": f"external:pinmame-review-artifacts/{relative}/{run_path.parent.name}", "quality": "validated",
			"repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "sha256": raw["sha256"],
		},
		"states": [], "switches": [], "version": 1,
	}


def action(label: str, kind: str, host: list[int], transitioned: list[int], address: int | None = None, name: str | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {"active_solenoid_addresses": [], "host_stimulus_switch_addresses": host, "input_kind": kind, "label": label, "observed_switch_addresses": [], "result": "observed" if transitioned else "no_matching_transition", "transitioned_solenoid_addresses": transitioned}
	if address is not None:
		item["input_address"] = address
	if name is not None:
		item["input_name"] = name
	return item


def switch_text(address: int) -> str:
	if 1 <= address <= 64:
		name = dev.SWITCHES[address][6] if address in dev.SWITCHES else dev.ROM_UNUSED_SWITCH_NAME.format(n=address)
		wires = " / ".join(dev.matrix_wires(address))
		return f"SWITCH TEST / {name} / LAST SW. #{address} / {wires}"
	name, last, wires = dev.DEDICATED_ROM_TEXT[address]
	return f"SWITCH TEST / {name} / LAST SW. {last} / {wires}"


def switch_summary(root: Path, driver: str) -> dict[str, Any]:
	path, run = load_run(root, "switch", driver)
	digest = seal(path.parent, driver, SCENARIOS["switch"])
	snaps, steps = snapshot_map(run), step_map(run)
	records = [snapshot_record(snaps["booted"], "power-up version screen", boot_text(driver)), snapshot_record(snaps["Select 5: switch test"], "switch test started with every public switch at 0; the grid marks no switch active", "SWITCH TEST / NONE")]
	actions = []
	for address in SWITCH_ADDRESSES:
		text = switch_text(address)
		records.append(snapshot_record(snaps[f"hold {address} (held)"], f"switch test while public {address} is held at 1", text))
		step = steps[f"hold {address}"]
		if step["observed_while_held"] != 1 or step["observed_after_release"] != 0:
			raise SystemExit(f"{driver}: public {address} did not read 1 while held and 0 after release")
		actions.append(action(f"public {address} held at 1 for 1.2 s: the ROM prints {text.split(' / ')[1]}", "switch", [address], sorted(solenoid_changes(step)), address=address))
	observations = {"diagnostic_snapshots": records, "named_action_observations": actions}
	note = ". The scenario uses the named S.A.M. Back and Select keys only to reach the switch test; every held address is a direct public switch write. Public 81-88 are the flipper button and EOS pairs: pinned sam.c samswitch_r copies each button bit (D-9, D-11, D-13, D-15) into its EOS bit as the CPU reads the dedicated word, so the test names the EOS of the pair whichever bit is held. Each held frame's interpreted_text transcribes the four display lines: title, name, LAST SW line and wire colours."
	return evidence_shell(f"switch-test-sweep-{driver}", driver, run, path, digest, command(driver, SCENARIOS["switch"]) + note, observations, SCENARIOS["switch"], {"watch_switches": run["watch_switches"]})


def coil_number(position: int) -> int:
	return (position - 1) % 32 + 1


def coil_text(number: int) -> str:
	coil = dev.COILS[number]
	return f"COIL TEST / {coil[3]} / #{number} / {coil[4]} / {coil[5]}"


def coil_summary(root: Path, driver: str) -> dict[str, Any]:
	path, run = load_run(root, "coil", driver)
	digest = seal(path.parent, driver, SCENARIOS["coil"])
	snaps, steps = snapshot_map(run), step_map(run)
	records = [snapshot_record(snaps["booted"], "power-up version screen", boot_text(driver)), snapshot_record(snaps["Select 4: coil menu"], "coil menu", "TEST CYC PREV QUIT HELP / SINGLE COIL TEST")]
	actions = []
	for position in range(1, COIL_POSITIONS + 1):
		number = coil_number(position)
		label = "Select 5: single coil test, coil 1 shown" if position == 1 else f"advance coil test {position}"
		text = coil_text(number) + (" (selector wrapped)" if position > 32 else "")
		records.append(snapshot_record(snaps[label], f"selector position {position}", text))
		changed = sorted(solenoid_changes(steps[f"fire coil test {position}"]))
		expected = [] if number == 24 else [6, 22] if number == 6 else [number]
		if changed != expected:
			raise SystemExit(f"{driver}: selector position {position} shows #{number} but fired {changed}")
		actions.append(action(f"selector position {position} ({dev.COILS[number][3]}, #{number}): SELECT fires public solenoid {', '.join(map(str, changed)) or 'none'}", "key", [], changed, name="service_select"))
	note = ". SELECT energizes the coil on display. The selector steps #1-#32 in order and wraps to #1 at position 33. Firing #6 SPINNING DISK MOTOR also changes public 22 (#22 SPINNING DISK MOTOR RELAY); firing #24 OPTIONAL COIL changes no public solenoid."
	return evidence_shell(f"coil-test-sweep-{driver}", driver, run, path, digest, command(driver, SCENARIOS["coil"]) + note, {"diagnostic_snapshots": records, "named_action_observations": actions}, SCENARIOS["coil"], {})


def lamp_text(number: int) -> str:
	name = dev.LAMPS[number][1] if number in dev.LAMPS else "NOT USED"
	return f"SINGLE LAMP TEST / {name} / LAMP #{number} / {' / '.join(dev.lamp_wires(number))}"


def lamp_summary(root: Path, driver: str) -> dict[str, Any]:
	path, run = load_run(root, "lamp", driver)
	digest = seal(path.parent, driver, SCENARIOS["lamp"])
	snaps, steps = snapshot_map(run), step_map(run)
	records = [snapshot_record(snaps["booted"], "power-up version screen", boot_text(driver)), snapshot_record(snaps["Select 4: lamp menu, ONE highlighted"], "lamp menu", "ONE ALL ROW COL PREV QUIT HELP / SINGLE LAMP TEST")]
	actions = []
	for position in range(1, 83):
		number = (position - 1) % 80 + 1
		label = "Select 5: single lamp test, lamp 1 shown" if position == 1 else f"advance lamp test {position}"
		records.append(snapshot_record(snaps[label], f"selector position {position}", lamp_text(number) + (" (selector wrapped)" if position > 80 else "")))
		lamps = steps[label].get("transitions", {}).get("lamps", [])
		lit = {item["number"] for item in lamps if any(item["states"])}
		previous = (position - 2) % 80 + 1 if position > 1 else None
		if number not in lit or lit - {number, previous}:
			raise SystemExit(f"{driver}: lamp test position {position} shows lamp {number} but the lamps lit are {sorted(lit)}")
		name = dev.LAMPS[number][1] if number in dev.LAMPS else "NOT USED"
		actions.append(action(f"selector position {position} ({name}, lamp {number}): lamp {number} is the only lamp address that turns on while the position is shown", "key", [], [], name="service_plus"))
	seen: set[int] = set()
	for step in run["steps"]:
		seen.update(item["number"] for item in step.get("transitions", {}).get("lamps", []))
	observations = {"diagnostic_snapshots": records, "named_action_observations": actions, "lamp_addresses_seen": sorted(seen)}
	note = ". Positions 81 and 82 wrap to lamps 1 and 2. While a position is shown its lamp blinks and no other lamp address turns on; the lamp of the previous position may still be turning off. lamp_addresses_seen also includes the attract-mode lamps published before the test was entered."
	return evidence_shell(f"lamp-test-sweep-{driver}", driver, run, path, digest, command(driver, SCENARIOS["lamp"]) + note, observations, SCENARIOS["lamp"], {})


def probe_summary(root: Path, kind: str, driver: str, first_step: int, note: str) -> dict[str, Any]:
	path, run = load_run(root, kind, driver)
	digest = seal(path.parent, driver, SCENARIOS[kind])
	actions = []
	for step in run["steps"]:
		if step["step"] < first_step:
			continue
		changes = solenoid_changes(step)
		detail = ", ".join(f"public {number} changed {count} times" for number, count in sorted(changes.items())) or "no public solenoid changed"
		lamps = sorted(item["number"] for item in step.get("transitions", {}).get("lamps", []) if any(item["states"]))
		if "switch" in step:
			text = f"{step['label']}: {detail}; lamps turned on: {', '.join(map(str, lamps)) or 'none'}"
			actions.append(action(text, "switch", [step["switch"]], sorted(changes), address=step["switch"]))
	return evidence_shell(f"{RUN_DIRECTORIES[kind]}-{driver}", driver, run, path, digest, command(driver, SCENARIOS[kind]) + note, {"named_action_observations": actions}, SCENARIOS[kind], {"watch_switches": run["watch_switches"]})


GAMEPLAY_NOTE = ". Every public switch write is a host stimulus, never a ROM observation; each observation lists the public solenoids that changed during the step and the lamps that turned on. Steps before the coins only seat the four trough balls. Public solenoid 33 (the synthetic game-on state) never appears here: the pinned LibPinMAME build does not report it through OnSolenoidUpdated (see the fast-flip diagnostic runs)."
POPS_NOTE = ". Every public switch write is a short host pulse, never a ROM observation. Each bumper hit fires its own coil and lamp (30: Q9 and lamp 60; 31: Q10 and lamp 61; 32: Q11 and lamp 62), the shaker Q8 and the pop-bumper flash Q31; each slingshot hit fires its own coil (26: Q17; 27: Q18) and the slingshot flash Q32. The first top-bumper hit also coincides with the disk motor Q6 and relay Q22 and the orbit post Q21, which the ROM drives on its own timing."


def boot_summary(root: Path, driver: str) -> dict[str, Any]:
	path = root / HARNESS_RELATIVE / f"boot-start-{driver}" / "run.json"
	run = json.loads(path.read_text(encoding="utf-8"))
	if run.get("failure") or run["library_sha256"] != PINNED_LIBRARY_SHA256 or run["game"] != driver:
		raise SystemExit(f"{path}: unusable boot run")
	digest = manifest.write_manifest(path.parent, driver)
	seen: dict[str, set[int]] = {"solenoid": set(), "lamp": set(), "gi": set()}
	for event in run["events"]:
		if event.get("event") in seen:
			seen[event["event"]].add(event["number"])
	observations = {
		"display_layouts_seen": [{"depth": 4, "height": 32, "type": 14, "width": 128}],
		"gi_addresses_seen": sorted(seen["gi"]), "lamp_addresses_seen": sorted(seen["lamp"]), "solenoid_addresses_seen": sorted(seen["solenoid"]),
	}
	command_template = f"python tools/run_pinmame_harness.py --library <libpinmame> --game {driver} --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --ready-timeout 90 --boot-wait 30 --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65:300:0.7 (four times) --pulse 16:500:4 --observe 8 --dmd-dir <external-dmd-dir> --output <external-run.json>. Public solenoid 1 is the trough up-kicker serving the first ball and 24 the optional coil pulsed once per coin; the synthetic game-on solenoid 33 is not reported by this LibPinMAME build's callback."
	return evidence_shell(f"boot-start-{driver}", driver, run, path, digest, command_template, observations, None, {"pulses": run["pulses"]})


DIAGNOSTIC_RUNS = ("fastflip-getter-nba_802", "fg-boot-pinned-dll")


def seal_diagnostics(root: Path) -> dict[str, str]:
	"""Seal the fast-flip diagnostic runs; their readings are transcribed in the fast-flip excerpt."""
	digests = {}
	for name in DIAGNOSTIC_RUNS:
		directory = root / DIAGNOSTICS_RELATIVE / name
		run = json.loads((directory / "run.json").read_text(encoding="utf-8"))
		if run.get("failure") or run["library_sha256"] != PINNED_LIBRARY_SHA256:
			raise SystemExit(f"{directory}: unusable diagnostic run")
		digests[name] = manifest.write_manifest(directory, run["game"])
	return digests


def build_all(root: Path) -> dict[str, dict[str, Any]]:
	"""Every committed summary, keyed by file name, derived from the retained runs under ``root``."""
	outputs: dict[str, dict[str, Any]] = {}
	for driver in ("nba_802", "nba_801"):
		outputs[f"nba-{driver}-boot-start.json"] = boot_summary(root, driver)
		outputs[f"nba-{driver}-gameplay-probe.json"] = probe_summary(root, "gameplay", driver, 6, GAMEPLAY_NOTE)
	outputs["nba-nba_802-bumper-sling-probe.json"] = probe_summary(root, "pops", "nba_802", 15, POPS_NOTE)
	for driver in SWEEP_DRIVERS:
		outputs[f"nba-{driver}-switch-test-sweep.json"] = switch_summary(root, driver)
		outputs[f"nba-{driver}-coil-test-sweep.json"] = coil_summary(root, driver)
		outputs[f"nba-{driver}-lamp-test-sweep.json"] = lamp_summary(root, driver)
	return outputs


def write_all() -> None:
	root = artifacts_root()
	RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
	for name, document in build_all(root).items():
		(RUNTIME_ROOT / name).write_bytes((json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
		print(f"wrote {name}")
	for name, digest in seal_diagnostics(root).items():
		print(f"sealed {name}: {digest}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--write", action="store_true", required=True)
	parser.parse_args()
	write_all()
