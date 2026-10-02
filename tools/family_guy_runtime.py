"""Summarize the retained Family Guy harness runs into compact committed evidence.

The raw runs (``run.json``, DMD frames, isolated state) stay under the working root's
``review-artifacts/family-guy-2007/harness/<kind>-sweep-<driver>/``; this script copies the
scenario beside each run, seals the directory with ``build_external_evidence_manifest`` and
writes one summary per run to ``evidence/runtime/sam/``. Every ``interpreted_text`` is a visual
reading of the frame whose pixel hash it carries (the DMD font defeats Windows OCR); the pixel
hashes and nonzero-pixel counts are copied from the raw run, so a misreading cannot change them.

Usage (needs ``PINMAME_REVIEW_ARTIFACTS_ROOT``)::

	python tools/family_guy_runtime.py --write
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
import family_guy_devices as dev  # noqa: E402

ROOT = TOOLS.parent
RUNTIME_ROOT = ROOT / "evidence/runtime/sam"
MACHINE_ID = "stern.family-guy.2007"
PINNED_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
SCENARIOS = {
	"switch": ROOT / "tools/harness-scenarios/stern/bbh-switch-test-sweep.json",
	"dedicated": ROOT / "tools/harness-scenarios/stern/family-guy-2007-dedicated-switch-sweep.json",
	"coil": ROOT / "tools/harness-scenarios/stern/family-guy-2007-coil-sweep.json",
	"lamp": ROOT / "tools/harness-scenarios/stern/family-guy-2007-lamp-sweep.json",
	"closed": ROOT / "tools/harness-scenarios/stern/family-guy-2007-evil-monkey-probe.json",
	"open": ROOT / "tools/harness-scenarios/stern/family-guy-2007-evil-monkey-probe-open.json",
}
SWEEP_DRIVERS = ("fg_1200ag", "fg_300ai", "fg_400a", "fg_800al", "fg_1100al")
HARNESS_RELATIVE = "family-guy-2007/harness"

# The ROM prints "#n" for lamp/coil numbers it names; the dedicated-switch test prints "D-n".
DEDICATED_ADDRESSES = list(range(65, 73)) + list(range(81, 89)) + [-7, -6, -5, -4]
# What the dedicated-switch test printed for each held address (read from the frames).
DEDICATED_TEXT = {
	65: "LEFT COIN SLOT / LAST SW. D-1", 66: "CENTER COIN SLOT / LAST SW. D-2", 67: "RIGHT COIN SLOT / LAST SW. D-3", 68: "FOURTH COIN SLOT / LAST SW. D-4",
	69: "FIFTH COIN SLOT / LAST SW. D-5", 70: "DEDICATED SW. #6 / LAST SW. D-6", 71: "L. POST SAVE / LAST SW. D-7", 72: "R. POST SAVE / LAST SW. D-8",
	81: "RIGHT FLIPPER E.O.S. / LAST SW. D-12", 82: "RIGHT FLIPPER E.O.S. / LAST SW. D-12", 83: "LEFT FLIPPER E.O.S. / LAST SW. D-10", 84: "LEFT FLIPPER E.O.S. / LAST SW. D-10",
	85: "U.R. FLIPPER E.O.S. / LAST SW. D-16", 86: "U.R. FLIPPER E.O.S. / LAST SW. D-16", 87: "U.L. FLIPPER E.O.S. / LAST SW. D-14", 88: "U.L. FLIPPER E.O.S. / LAST SW. D-14",
	-7: "TILT PENDULUM / LAST SW. D-17", -6: "SLAM TILT / LAST SW. D-18", -5: "TICKET NOTCH / LAST SW. D-19", -4: "DEDICATED SW. #20 / LAST SW. D-20",
}
# Coil test: the selector positions the ROM visits in order (selector position -> coil number), and the ROM's names.
COIL_SELECTOR = [*range(1, 20), *range(21, 24), *range(25, 33)]
COIL_TEXT = dev.COIL_ROM_NAMES
# V3.00 and V4.00 firmware continue past #32 with two optional ticket-dispenser auxiliary coils before wrapping to #1.
OLD_AUX = {31: "AUX 1: TICKET ADVANCE / #33", 32: "AUX 3: TICKET ENABLE / #35"}
AUX_DRIVERS = {"fg_300ai", "fg_400a", "fg_800al", "fg_1100al"}


def sha256_file(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def artifacts_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
	return Path(value)


def snapshot_map(run: dict[str, Any]) -> dict[str, dict[str, Any]]:
	return {snapshot["label"]: snapshot for snapshot in run["snapshots"]}


def display_of(snapshot: dict[str, Any]) -> dict[str, Any]:
	return snapshot["displays"][0]


def solenoids_changed(step: dict[str, Any]) -> list[int]:
	return sorted(item["number"] for item in step.get("transitions", {}).get("solenoids", []))


def snapshot_record(snapshot: dict[str, Any], label: str, text: str, step: dict[str, Any] | None = None) -> dict[str, Any]:
	display = display_of(snapshot)
	return {"active_solenoid_addresses": sorted(snapshot.get("active_solenoids", [])), "display_index": display["index"], "interpreted_text": text, "label": label, "nonzero_pixels": display["nonzero_pixels"], "pixel_sha256": display["pixel_sha256"]}


def evidence_shell(kind: str, driver: str, run: dict[str, Any], run_path: Path, directory_digest: str, command_template: str, observations: dict[str, Any], scenario_path: Path | None, extra_raw: dict[str, Any]) -> dict[str, Any]:
	raw = {
		"action_count": run["scenario"]["action_count"] if run.get("scenario") else 0,
		"initial_switches": run["initial_switches"],
		"name": f"{kind}-{driver}",
		"nvram_initialization": "empty; the run created its own isolated PinMAME state directory and the ROM reached attract mode without a factory-reset message to dismiss",
		"retained_from": f"external:pinmame-review-artifacts/{HARNESS_RELATIVE}/{run_path.parent.name}/run.json",
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
			"attribution": f"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation is counted key pulses; every retained DMD frame was read visually and each diagnostic snapshot's interpreted_text is that reading of its pixel SHA-256. Exact external directory manifest {run_path.parent.name}/manifest.json SHA-256 {directory_digest} (built by tools/build_external_evidence_manifest.py); it lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes.",
			"kind": "runtime_scenario", "license": "NOASSERTION", "path": f"external:pinmame-review-artifacts/{HARNESS_RELATIVE}/{run_path.parent.name}", "quality": "validated",
			"repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "sha256": raw["sha256"],
		},
		"states": [], "switches": [], "version": 1,
	}


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


def run_directory(kind: str, driver: str) -> str:
	return f"evil-monkey-probe-{kind}-{driver}" if kind in {"closed", "open"} else f"{kind}-sweep-{driver}"


def load_run(root: Path, kind: str, driver: str) -> tuple[Path, dict[str, Any]]:
	path = root / HARNESS_RELATIVE / run_directory(kind, driver) / "run.json"
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


def action(label: str, kind: str, host: list[int], transitioned: list[int], address: int | None = None, name: str | None = None, active: list[int] | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {"active_solenoid_addresses": active or [], "host_stimulus_switch_addresses": host, "input_kind": kind, "label": label, "observed_switch_addresses": [], "result": "observed" if transitioned else "no_matching_transition", "transitioned_solenoid_addresses": transitioned}
	if address is not None:
		item["input_address"] = address
	if name is not None:
		item["input_name"] = name
	return item


def switch_summary(root: Path, driver: str) -> dict[str, Any]:
	path, run = load_run(root, "switch", driver)
	digest = seal(path.parent, driver, SCENARIOS["switch"])
	snaps = snapshot_map(run)
	records = [snapshot_record(snaps["booted"], "power-up attract mode", "ATTRACT MODE"), snapshot_record(snaps["Select 5: switch test"], "switch test started with every public switch at 0; the grid marks no switch active", "SWITCH TEST / NONE")]
	actions = []
	steps = {step["label"]: step for step in run["steps"]}
	for address in range(1, 65):
		name = dev.SWITCHES[address][6] if address in dev.SWITCHES else f"SWITCH #{address}"
		records.append(snapshot_record(snaps[f"hold {address} (held)"], f"switch test while public {address} is held at 1", f"SWITCH TEST / {name} / LAST SW. #{address}"))
		step = steps[f"hold {address}"]
		if step["observed_while_held"] != 1 or step["observed_after_release"] != 0:
			raise SystemExit(f"{driver}: public {address} did not read 1 while held and 0 after release")
		actions.append(action(f"public {address} held at 1 for 1.2 s: the ROM prints {name}", "switch", [address], solenoids_changed(step), address=address))
	observations = {"diagnostic_snapshots": records, "named_action_observations": actions}
	return evidence_shell("switch-test-sweep", driver, run, path, digest, command(driver, SCENARIOS["switch"]) + ". The scenario uses the named S.A.M. Back and Select keys only to reach the switch test; every held address is a direct public switch write in the playfield matrix. Each held frame's interpreted_text transcribes the switch name and LAST SW line; the wire-colour line below them is not transcribed.", observations, SCENARIOS["switch"], {"watch_switches": run["watch_switches"]})


def dedicated_summary(root: Path, driver: str) -> dict[str, Any]:
	path, run = load_run(root, "dedicated", driver)
	digest = seal(path.parent, driver, SCENARIOS["dedicated"])
	snaps = snapshot_map(run)
	steps = {step["label"]: step for step in run["steps"]}
	records = [snapshot_record(snaps["booted"], "power-up attract mode", "ATTRACT MODE"), snapshot_record(snaps["Select 5: switch test"], "switch test started", "SWITCH TEST / NONE")]
	actions = []
	for address in DEDICATED_ADDRESSES:
		text = DEDICATED_TEXT[address]
		records.append(snapshot_record(snaps[f"hold {address} (held)"], f"switch test while public {address} is held at 1", f"SWITCH TEST / {text}"))
		step = steps[f"hold {address}"]
		if address != -6 and (step["observed_while_held"] != 1 or step["observed_after_release"] != 0):
			raise SystemExit(f"{driver}: public {address} did not read 1 while held and 0 after release")
		actions.append(action(f"public {address} held at 1 for 1.2 s: the ROM prints {text.split(' / ')[0]}", "switch", [address], solenoids_changed(step), address=address))
	return evidence_shell("dedicated-switch-sweep", driver, run, path, digest, command(driver, SCENARIOS["dedicated"]) + ". Public 81-88 are the flipper button and EOS pairs: pinned sam.c samswitch_r copies each button bit (D-9, D-11, D-13, D-15) into its EOS bit as the CPU reads the dedicated word, so the switch test names the EOS of the pair whichever bit is held; the two lower EOS bits are also rewritten by core_updateSw from the flipper coil timers. Every held write reads back 1 in this run except the slam-tilt write (-6), which reads back 0 in some runs although the frame names SLAM TILT (a host-side readback, not ROM evidence).", {"diagnostic_snapshots": records, "named_action_observations": actions}, SCENARIOS["dedicated"], {})


def coil_summary(root: Path, driver: str) -> dict[str, Any]:
	path, run = load_run(root, "coil", driver)
	digest = seal(path.parent, driver, SCENARIOS["coil"])
	snaps = snapshot_map(run)
	steps = {step["label"]: step for step in run["steps"]}
	records = [snapshot_record(snaps["booted"], "power-up attract mode", "ATTRACT MODE"), snapshot_record(snaps["Select 4: coil menu"], "coil menu", "SINGLE COIL TEST (icon menu)")]
	actions = []
	for position in range(1, 36):
		label = "Select 5: single coil test, coil 1 shown" if position == 1 else f"advance coil test {position}"
		snapshot = snaps[label]
		if position <= len(COIL_SELECTOR):
			number = COIL_SELECTOR[position - 1]
			text = f"COIL TEST / {COIL_TEXT[number]} / #{number}"
		elif position in OLD_AUX and driver in AUX_DRIVERS:
			number = None
			text = f"COIL TEST / {OLD_AUX[position]}"
		else:
			number = COIL_SELECTOR[position - 1 - len(COIL_SELECTOR) - (2 if driver in AUX_DRIVERS else 0)]
			text = f"COIL TEST / {COIL_TEXT[number]} / #{number} (selector wrapped)"
		records.append(snapshot_record(snapshot, f"selector position {position}", text))
		fire = steps[f"fire coil test {position}"]
		changed = solenoids_changed(fire)
		if number is not None and changed != [number]:
			raise SystemExit(f"{driver}: selector position {position} shows #{number} but fired {changed}")
		actions.append(action(f"selector position {position} ({text.replace(' / ', '; ')}): SELECT fires public solenoid {', '.join(map(str, changed)) or 'none'}", "key", [], changed, name="service_select"))
	return evidence_shell("coil-test-sweep", driver, run, path, digest, command(driver, SCENARIOS["coil"]) + ". SELECT energizes the coil on display; the Single Coil Test skips Q20 (exercised by the separate Stewie Motor Test) and Q24.", {"diagnostic_snapshots": records, "named_action_observations": actions}, SCENARIOS["coil"], {})


def lamp_summary(root: Path, driver: str) -> dict[str, Any]:
	path, run = load_run(root, "lamp", driver)
	digest = seal(path.parent, driver, SCENARIOS["lamp"])
	snaps = snapshot_map(run)
	steps = {step["label"]: step for step in run["steps"]}
	records = [snapshot_record(snaps["booted"], "power-up attract mode", "ATTRACT MODE"), snapshot_record(snaps["Select 4: lamp menu, ONE highlighted"], "lamp menu", "SINGLE LAMP TEST (icon menu)")]
	actions = []
	seen: set[int] = set()
	for position in range(1, 82):
		number = position if position <= 80 else 1
		label = "Select 5: single lamp test, lamp 1 shown" if position == 1 else f"advance lamp test {position}"
		snapshot = snaps[label]
		name = dev.LAMP_ROM_NAMES[number]
		records.append(snapshot_record(snapshot, f"selector position {position}", f"SINGLE LAMP TEST / {name} / LAMP #{number}"))
		lamps = steps[label].get("transitions", {}).get("lamps", [])
		matrix = [item for item in lamps if item["number"] <= 80]
		# the selector lamp blinks; the previous selection may still be on or turning off, and no other matrix lamp lights
		lit = {item["number"] for item in matrix if any(item["states"])}
		previous = (position - 2) % 80 + 1 if position > 1 else None
		if number not in lit or lit - {number, previous}:
			raise SystemExit(f"{driver}: lamp test position {position} shows lamp {number} but the matrix lamps lit are {sorted(lit)}")
		actions.append(action(f"selector position {position} ({name}, lamp {number}): lamp {number} is the lamp-matrix address that blinks while the position is shown", "key", [], [], name="service_plus"))
	for step in run["steps"]:
		seen.update(item["number"] for item in step.get("transitions", {}).get("lamps", []))
	observations = {"diagnostic_snapshots": records, "named_action_observations": actions, "lamp_addresses_seen": sorted(seen)}
	return evidence_shell("lamp-test-sweep", driver, run, path, digest, command(driver, SCENARIOS["lamp"]) + ". Position 81 wraps to lamp 1. lamp_addresses_seen lists every lamp address that published a state change during the run, including the mini-playfield LED-board addresses, which the ROM drives throughout (attract and service mode) independently of the lamp-matrix selector.", observations, SCENARIOS["lamp"], {})


def probe_summary(root: Path, variant: str, driver: str = "fg_1200ag") -> dict[str, Any]:
	path, run = load_run(root, variant, driver)
	digest = seal(path.parent, driver, SCENARIOS[variant])
	actions = []
	for step in run["steps"]:
		if step["step"] < 16:
			continue
		solenoids = {item["number"]: len(item["states"]) for item in step.get("transitions", {}).get("solenoids", [])}
		fired = sorted(number for number in solenoids if number not in {20, 24})
		detail = ", ".join(f"public {number} changed {count} times" for number, count in sorted(solenoids.items())) or "no public solenoid changed"
		if "switch" not in step:
			continue
		address = step["switch"]
		item = action(f"{step['label']}: {detail}", "switch", [address], fired, address=address)
		actions.append(item)
	observations = {"named_action_observations": actions}
	state = "closed" if variant == "closed" else "open"
	return evidence_shell(f"evil-monkey-probe-{state}", driver, run, path, digest, f"python tools/run_pinmame_harness.py --library <libpinmame> --game {driver} --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --handle-mechanics 0 --ready-timeout 90 --scenario {SCENARIOS[variant].relative_to(ROOT).as_posix()} --dmd-dir <external-dmd-dir> --output <external-run.json>. Every public switch write is a host stimulus, never a ROM observation; the observations are the public solenoids that changed during each step. Evil Monkey switch 35 starts "+variant+". Public solenoid 20 (the Stewie stepper homing) and 24 (the credit-sound output) change during most steps and are listed in each label but not counted as responses.", observations, SCENARIOS[variant], {"watch_switches": run["watch_switches"]})


def boot_summary(root: Path) -> dict[str, Any]:
	path = root / HARNESS_RELATIVE / "boot-start-fg_1200ag" / "run.json"
	run = json.loads(path.read_text(encoding="utf-8"))
	if run.get("failure") or run["library_sha256"] != PINNED_LIBRARY_SHA256 or run["game"] != "fg_1200ag":
		raise SystemExit(f"{path}: unusable boot run")
	digest = manifest.write_manifest(path.parent, "fg_1200ag")
	solenoids: set[int] = set()
	lamps: set[int] = set()
	gis: set[int] = set()
	for event in run["events"]:
		kind = event.get("event")
		if kind == "solenoid":
			solenoids.add(event["number"])
		elif kind == "lamp":
			lamps.add(event["number"])
		elif kind == "gi":
			gis.add(event["number"])
	observations = {
		"display_layouts_seen": [{"depth": 4, "height": 32, "type": 14, "width": 128}],
		"gi_addresses_seen": sorted(gis), "lamp_addresses_seen": sorted(lamps), "solenoid_addresses_seen": sorted(solenoids),
	}
	command_template = "python tools/run_pinmame_harness.py --library <libpinmame> --game fg_1200ag --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --ready-timeout 90 --boot-wait 30 --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --initial-switch 55 --initial-switch 83 --initial-switch 81 --pulse 65:300:0.7 (six times) --pulse 16:500:4 --observe 6 --dmd-dir <external-dmd-dir> --output <external-run.json>"
	return evidence_shell("boot-start", "fg_1200ag", run, path, digest, command_template, observations, None, {"initial_switches": run["initial_switches"]})


def write_all() -> None:
	root = artifacts_root()
	RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
	outputs: dict[str, dict[str, Any]] = {"family-guy-fg_1200ag-boot-start.json": boot_summary(root), "family-guy-fg_1200ag-dedicated-switch-sweep.json": dedicated_summary(root, "fg_1200ag"), "family-guy-fg_1200ag-evil-monkey-probe-closed.json": probe_summary(root, "closed"), "family-guy-fg_1200ag-evil-monkey-probe-open.json": probe_summary(root, "open")}
	for driver in SWEEP_DRIVERS:
		if not (root / HARNESS_RELATIVE / f"lamp-sweep-{driver}" / "run.json").is_file():
			continue
		outputs[f"family-guy-{driver}-switch-test-sweep.json"] = switch_summary(root, driver)
		outputs[f"family-guy-{driver}-coil-test-sweep.json"] = coil_summary(root, driver)
		outputs[f"family-guy-{driver}-lamp-test-sweep.json"] = lamp_summary(root, driver)
	for name, document in outputs.items():
		(RUNTIME_ROOT / name).write_bytes((json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
		print(f"wrote {name}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--write", action="store_true", required=True)
	parser.parse_args()
	write_all()
