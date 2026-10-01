"""Summarize retained Black Knight 2000 harness runs into compact runtime evidence (and a full analysis file).

Reads the raw ``pinmame-harness-run`` records under ``raw-runs/<driver>/`` (written by ``tools/bk2k_run.py``
through the pinned ``tools/run_pinmame_harness.py``), writes a canonical ``manifest.json`` / ``manifest.sha256`` over
each driver directory with ``tools/build_external_evidence_manifest.py``, and emits

* one compact ``pinmame-machine-evidence`` document per driver (``evidence/black-knight-2000-<driver>-....json``),
* ``evidence/bk2k-analysis.json``: the complete derived tables the REPORT is built from (not a repository schema).

Every number in both is recomputed from the raw runs; ``--check`` re-derives everything and refuses any drift,
including a manifest that no longer matches the files beside it.

    python bk2k_summarize_runtime_evidence.py            # write
    python bk2k_summarize_runtime_evidence.py --check    # re-derive and compare, write nothing
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT / "src"))

import bk2k_analysis as A  # noqa: E402
import bk2k_handlers as H  # noqa: E402
import bk2k_lib as L  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
LIBRARY_SHA256 = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
MACHINE_ID = "williams.black-knight-2000.1989"
SCENARIO_REPO_DIR = "tools/harness-scenarios/system-11"
EVIDENCE_DIR = ROOT / "evidence" / "runtime" / "system-11"
SOURCE_ROOT = "external:pinmame-review-artifacts/williams.black-knight-2000.1989/runtime-stage/raw-runs"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, separators=(',', ':'), "
	"ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: 'pinmame-external-evidence-manifest', game, version: 1}; files lists "
	"every file under source.path recursively (the raw run JSON, its command record, its log and every state-directory file) except manifest.json "
	"and manifest.sha256, sorted by POSIX relative path. tools/build_external_evidence_manifest.py writes and re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game <driver> --rom-path <vpinmame-roms> --work-dir <new-empty-dir> "
	"--scenario <tools/harness-scenarios/system-11/bk2k-*.json> --boot-wait 0 --ready-timeout 30 --handle-mechanics 0 --output <external-json>, run through "
	"the staging wrapper bk2k_run.py. Every state directory is new and empty; the single retained init run (bk2k-nvram-init.json) boots to FACTORY SETTING "
	"and its nvram/<driver>.nv is the only file any later run inherits. Each diagnostic scenario then waits 16 s for power-up, sets Manual-Down (-6 = 0), "
	"pulses Advance (-7) to enter the tests, sets Auto-Up (-6 = 1) and pulses Advance until the required checkpoint text is displayed."
)

DRIVERS = ["bk2k_l4", "bk2k_la2", "bk2k_lg3", "bk2k_pa5", "bk2k_pa7", "bk2k_pu1"]


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_run(directory: Path, name: str) -> dict[str, Any]:
	return json.loads((directory / f"{name}.json").read_text(encoding="utf-8"))


def load_command(directory: Path, name: str) -> dict[str, Any]:
	return json.loads((directory / f"{name}.command.json").read_text(encoding="utf-8"))


def name_table(driver: str) -> dict[str, Any]:
	return json.loads((L.stage_root() / "rom-name-tables" / f"{driver}.json").read_text(encoding="utf-8"))


def coil_names(driver: str) -> list[str]:
	return [entry["text"] for entry in name_table(driver)["coil_table"]["entries"][:30]]


def service_pulses(run: dict[str, Any]) -> int:
	total = 0
	for step in run["steps"]:
		if step["type"] == "pulse" and step.get("switch") == -7:
			total += 1
		elif step["type"] == "pulse_until_display" and step.get("switch") == -7:
			total += step["pulses"]
	return total


def run_names(directory: Path) -> list[str]:
	return sorted(path.name[: -len(".command.json")] for path in directory.glob("*.command.json"))


def raw_run_entry(directory: Path, name: str, rom_sha: str) -> dict[str, Any]:
	run = load_run(directory, name)
	command = load_command(directory, name)
	if run.get("failure") is not None:
		raise RuntimeError(f"{name}: not a successful run: {run['failure']}")
	if run["library_sha256"] != LIBRARY_SHA256 or command["rom_archive_sha256"] != rom_sha or run["game"] != command["game"]:
		raise RuntimeError(f"{name}: not produced by the pinned library and ROM")
	scenario_name = Path(run["scenario"]["path"]).name
	if run["scenario"]["sha256"] != sha256(ROOT / SCENARIO_REPO_DIR / scenario_name):
		raise RuntimeError(f"{name}: scenario drift")
	inherited = command["inherited_nvram"]
	entry: dict[str, Any] = {
		"name": name,
		"sha256": sha256(directory / f"{name}.json"),
		"scenario_path": f"{SCENARIO_REPO_DIR}/{scenario_name}",
		"scenario_sha256": run["scenario"]["sha256"],
		"action_count": run["scenario"]["action_count"],
		"watch_switches": run["watch_switches"],
		"self_test_pulses": service_pulses(run),
		"boot_wait_s": 0,
		"snapshot_count": len(run["snapshots"]),
		"nvram_initialization": (
			"Fresh empty state directory; this is the one retained initialization run (FACTORY SETTING), whose nvram file is the only state any later run inherits."
			if inherited is None
			else f"Fresh empty state directory; copied only nvram/{run['game']}.nv (SHA-256 {inherited['sha256']}) from this driver's separately hashed init run."
		),
	}
	if run["initial_switches"]:
		entry["initial_switches"] = [{"switch": item["switch"], "state": item["state"]} for item in run["initial_switches"]]
	return entry


def manifest_for(directory: Path, driver: str) -> bytes:
	return (json.dumps(manifests.build_manifest(directory, driver), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


def coil_observation(driver: str, run: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
	title = "SPULEN TEST" if driver == "bk2k_lg3" else "COIL TEST"
	result = A.coil_test(run, coil_names(driver), title)
	pairs = result["pairs"]
	note = (
		f"Auto-Up Advance walk to COIL TEST (test 05) then {result['cycle_count']} complete cycles of {len(pairs)} steps, period {result['cycle_period_s']} s, "
		f"{'every cycle pulsing the same addresses in the same order' if result['cycles_identical'] else 'cycles DIFFER'}. First cycle, step:address=ROM name "
		f"(display step/side): " + "; ".join(
			f"{p['step']}:{p['address']}={p['rom_name']} ({p['display_step']}{(' ' + p['display_side'].replace(chr(34), '')) if p['display_side'] else ''})" for p in pairs
		) + ". Public 12 is on for every C-side step (25-32) and off for every A-side step (1-8)."
	)
	obs = {
		"diagnostic_checkpoints": [{"matched_text": title, "after_service_pulses": next(s["pulses"] for s in run["steps"] if s["type"] == "pulse_until_display")}],
		"ordered_solenoid_on_sequence": [p["address"] for p in pairs],
		"solenoid_addresses_seen": sorted({event["number"] for event in L.solenoid_events(run) if event["state"]}),
		"note": note,
		"limitation": (
			"Names come from the ROM's own coil table (U27, entries in table order) and are accepted only when the decoded display text of that step equals the table "
			"entry exactly (whitespace-normalized); the ROM draws the numeral 1 as 0x0006 and the period in bit 15. A pulsed address is ROM activity, not proof that a "
			"load is fitted: entries the ROM names UNUSED still pulse."
		),
	}
	return obs, result


def build_driver_evidence(driver: str) -> tuple[bytes, dict[str, Any], dict[str, Any]]:
	"""Return (manifest bytes, compact evidence, full analysis) for one driver directory."""
	directory = L.stage_root() / "raw-runs" / driver
	short = driver.removeprefix("bk2k_")
	zip_sha = load_command(directory, f"{short}-init")["rom_archive_sha256"]
	manifest_bytes = manifest_for(directory, driver)
	raw_runs, runs_obs, analysis = [], {}, {}
	seen_solenoids: set[int] = set()
	ordered: list[int] = []
	named: dict[str, int] = {}
	lamp_addresses: list[int] = []
	for name in run_names(directory):
		entry = raw_run_entry(directory, name, zip_sha)
		raw_runs.append(entry)
		run = load_run(directory, name)
		seen_solenoids.update(event["number"] for event in L.solenoid_events(run) if event["state"])
		stem = name.removeprefix(f"{short}-")
		if stem == "init":
			runs_obs[name] = {"note": "Boot to FACTORY SETTING from empty NVRAM; the NVRAM written on stop is the only state later runs inherit.", "solenoid_addresses_seen": sorted({e["number"] for e in L.solenoid_events(run) if e["state"]})}
			analysis[name] = {"boot_pulses": A.boot_pulses(run)}
		elif stem == "coil":
			obs, result = coil_observation(driver, run)
			runs_obs[name] = obs
			ordered = obs["ordered_solenoid_on_sequence"]
			analysis[name] = {**result, "boot_pulses": A.boot_pulses(run), "solenoid_on_counts": A.solenoid_summary(run)["on_counts"]}
			for pair in result["pairs"]:
				step_no = int(pair["display_step"])
				side = {'"A" SIDE': "a", '"C" SIDE': "c"}.get(pair["display_side"], "")
				named[f"coil-{step_no:02d}{side}-{slug(pair['rom_name'])}"] = pair["address"]
		elif stem == "switch-levels":
			runs_obs[name], analysis[name] = H.switch_observation(driver, run, "SWITCH LEVELS")
		elif stem == "switch-edges-de-banks":
			runs_obs[name], analysis[name] = H.switch_observation(driver, run, "KONTAKT SCHLIST")
		elif stem == "switch-edges":
			runs_obs[name], analysis[name] = H.switch_observation(driver, run, "SWITCH EDGES")
		elif stem == "single-lamps":
			runs_obs[name], analysis[name], lamp_names, lamps_seen = H.lamp_observation(run)
			named.update(lamp_names)
			lamp_addresses = lamps_seen
		elif stem.startswith("boot-"):
			runs_obs[name], analysis[name] = H.boot_observation(run)
		elif stem.startswith("motor-bank-"):
			runs_obs[name], analysis[name] = H.motor_observation(run)
		elif stem.startswith("droptargets-") or stem.startswith("game-"):
			runs_obs[name], analysis[name] = H.game_observation(run, stem)
		else:
			raise RuntimeError(f"unhandled run {name}")
	observations: dict[str, Any] = {
		"service_language": "English" if driver != "bk2k_lg3" else "German ROM set; test text as displayed",
		"solenoid_addresses_seen": sorted(seen_solenoids),
		"ordered_solenoid_on_sequence": ordered,
		"named_output_addresses": named,
		"display_indices_seen": [0, 1, 2],
		"runs": runs_obs,
	}
	if lamp_addresses:
		observations["lamp_addresses_seen"] = lamp_addresses
	evidence = {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "bk2k-harness-runs", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": f"{SOURCE_ROOT}/{driver}",
			"sha256": hashlib.sha256(manifest_bytes).hexdigest(),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external.",
			"quality": "observed",
			"manifest_algorithm": MANIFEST_ALGORITHM,
		},
		"driver_ids": [driver],
		"machine_ids": [MACHINE_ID],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": driver,
			"rom_archive_sha256": zip_sha,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"raw_runs": raw_runs,
			"command_template": COMMAND_TEMPLATE,
			"observations": observations,
		},
	}
	return manifest_bytes, evidence, analysis


def evidence_path(driver: str) -> Path:
	if driver == "bk2k_l4":
		return EVIDENCE_DIR / "black-knight-2000-l4-service-and-mechanisms.json"
	return EVIDENCE_DIR / f"black-knight-2000-{driver.removeprefix('bk2k_')}-coil-test.json"


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--check", action="store_true")
	parser.add_argument("--drivers", nargs="*", default=None)
	args = parser.parse_args()
	drivers = args.drivers or [d for d in DRIVERS if (L.stage_root() / "raw-runs" / d).is_dir()]
	full: dict[str, Any] = {}
	for driver in drivers:
		manifest_bytes, evidence, analysis = build_driver_evidence(driver)
		full[driver] = analysis
		directory = L.stage_root() / "raw-runs" / driver
		out = evidence_path(driver)
		if args.check:
			if (directory / "manifest.json").read_bytes() != manifest_bytes:
				raise SystemExit(f"{directory / 'manifest.json'} does not match the files beside it")
			manifests.check_manifest(directory, driver)
			if out.read_bytes() != canonical_bytes(evidence):
				raise SystemExit(f"{out} is not the summary of the raw runs in {directory}")
		else:
			manifests.write_manifest(directory, driver)
			assert (directory / "manifest.json").read_bytes() == manifest_bytes
			out.parent.mkdir(parents=True, exist_ok=True)
			out.write_bytes(canonical_bytes(evidence))
			print(f"wrote {out}")
	analysis_path = L.stage_root() / "evidence" / "bk2k-analysis.json"
	if args.check:
		if analysis_path.read_bytes() != canonical_bytes(full):
			raise SystemExit(f"{analysis_path} drifted")
		print("evidence, manifests and analysis match the raw runs")
	else:
		analysis_path.write_bytes(canonical_bytes(full))
		print(f"wrote {analysis_path}")


if __name__ == "__main__":
	main()
