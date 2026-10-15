#!/usr/bin/env python3
"""Recompute compact Seawitch evidence from the retained fresh-state runs.

ROM bytes, NVRAM and raw traces stay outside Git. Host switch readback is
deliberately absent from observed_switch_addresses. A diagnostic number is
read from the ROM's seven-segment response, never from PinmameGetSwitch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json
from build_external_evidence_manifest import check_manifest
import seawitch_data as data

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("evidence/runtime/stern/seawitch-diagnostics-and-gameplay.json")
RUNS = {"self-test": "self-test", "switch-test": "switch-test-v2", "gameplay": "gameplay"}
DIGITS = {0: " ", 0x3f: "0", 6: "1", 0x5b: "2", 0x4f: "3", 0x66: "4", 0x6d: "5", 0x7d: "6", 7: "7", 0x7f: "8", 0x6f: "9"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digits(segments: list[int]) -> str:
    return "".join(DIGITS.get(value & 0x7f, "?") for value in segments).strip()


def responses(snapshot: dict, *, diagnostic_address: int | None = None) -> list[dict]:
    result = []
    for display in snapshot["displays"]:
        if display["index"] not in (0, 4, 5) or "segments" not in display:
            continue
        row = {"snapshot_label": snapshot["label"], "display_index": display["index"],
               "segments": display["segments"], "decoded_segment_positions": list(range(len(display["segments"]))),
               "interpreted_text": digits(display["segments"])}
        if diagnostic_address is not None and display["index"] == 0:
            row["diagnostic_address"] = diagnostic_address
        result.append(row)
    return result


def action_observations(run: dict, diagnostic: bool = False) -> list[dict]:
    snapshots = {s["label"]: s for s in run["snapshots"]}
    result = []
    previous_text = [r["interpreted_text"] for r in responses(snapshots["boot stabilization"])]
    for step in run["steps"]:
        if "switch" not in step:
            continue
        address = step["switch"]
        if diagnostic and address < 1:
            continue
        label = step["label"]
        snapshot = snapshots.get(label + " (held)", snapshots[label])
        reading = digits(snapshot["displays"][0]["segments"])
        if diagnostic and (not reading.isdigit() or int(reading) != address):
            raise RuntimeError(f"Switch test did not name {address}: {reading!r}")
        transitions = sorted(row["number"] for row in step["transitions"]["solenoids"])
        display_responses = responses(snapshot, diagnostic_address=address if diagnostic else None)
        current_text = [r["interpreted_text"] for r in display_responses]
        row = {"label": label, "input_kind": "switch", "input_address": address,
               "observed_switch_addresses": [], "host_stimulus_switch_addresses": [address],
               "display_responses": display_responses,
               "active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
               "transitioned_solenoid_addresses": transitions,
               "result": "observed" if diagnostic or transitions or current_text != previous_text else "no_matching_transition"}
        previous_text = current_text
        if label.startswith("flipper button position"):
            row["held_synthetic_solenoid_addresses"] = sorted(set(snapshot["active_solenoids"]) & {45, 46, 47, 48})
        result.append(row)
    return result


def build(runs_root: Path) -> dict:
    manifest_digest = check_manifest(runs_root, "seawitch")
    runs = {name: load_json(runs_root / folder / "run.json") for name, folder in RUNS.items()}
    raw_runs = []
    for name, run in runs.items():
        if run["failure"] is not None or run["game"] != "seawitch" or run["library_sha256"] != data.LIBRARY_SHA256:
            raise RuntimeError(f"Unsuccessful or unpinned Seawitch run: {name}")
        if run["handle_mechanics"] != 0:
            raise RuntimeError(f"Unexpected built-in mechanism model: {name}")
        scenario_path = ROOT / "tools/harness-scenarios/stern" / f"seawitch-{name}.json"
        if run["scenario"]["sha256"] != sha256(scenario_path):
            raise RuntimeError(f"Scenario drift: {name}")
        scenario = load_json(scenario_path)
        raw_runs.append({"name": name, "sha256": sha256(runs_root / RUNS[name] / "run.json"),
                         "retained_from": RUNS[name] + "/run.json",
                         "scenario_path": scenario_path.relative_to(ROOT).as_posix(), "scenario_sha256": sha256(scenario_path),
                         "action_count": len(scenario["actions"]), "self_test_pulses": sum(a.get("switch") == -7 for a in scenario["actions"]),
                         "nvram_initialization": "Empty: each run began in its own newly created state directory; no inherited NVRAM.",
                         "initial_switches": scenario.get("initial_switches", []), "boot_wait_s": 2, "snapshot_count": len(run["snapshots"])})

    self_run = runs["self-test"]
    press = next(e["time_s"] for e in self_run["events"] if e["event"] == "switch" and e["number"] == -7 and e["state"] == 1)
    sequence = [e["number"] for e in self_run["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["time_s"] > press]
    # The first partial cycle may miss Q1. Start at the next complete cycle.
    cycle = sequence[sequence.index(2):sequence.index(2) + 19]
    expected = [next(a for a, q in zip(data.SOLENOID_ADDRESSES, data.PUBLIC_TO_Q) if q == number) for number in range(1, 20)]
    if cycle != expected:
        raise RuntimeError(f"Burn-in order disagrees with the independently read SDU circuit: {cycle}")
    lamp_addresses = sorted({e["number"] for e in self_run["events"]
                             if e["event"] == "lamp" and e["state"] > 0 and e["time_s"] > press})
    public_lamps = sorted(16*k + a + 1 for k in range(4) for a in range(15))
    if lamp_addresses != public_lamps:
        raise RuntimeError("Burn-in did not exercise all sixty lamp outputs")

    gameplay = runs["gameplay"]
    gameplay_obs = action_observations(gameplay)
    diagnostic_obs = action_observations(runs["switch-test"], diagnostic=True)
    if [row["input_address"] for row in diagnostic_obs] != list(range(1, 41)):
        raise RuntimeError("Switch diagnostic sweep is incomplete")
    def seen(run: dict, event: str) -> list[int]:
        return sorted({e["number"] for e in run["events"] if e["event"] == event})
    return {
        "format": "pinmame-machine-evidence", "version": 1,
        "extractor": {"id": "tools/summarize_seawitch_runtime.py", "version": 1},
        "source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": data.PINMAME_REVISION,
                   "path": "external:pinmame-review-artifacts/stern.seawitch.1980/harness", "sha256": manifest_digest,
                   "license": "NOASSERTION", "attribution": "Locally generated from the user-authorized ROM and pinned PinMAME; ROM bytes and mutable state remain external.",
                   "quality": "validated", "manifest_algorithm": "tools/build_external_evidence_manifest.py: case-sensitive sorted relative POSIX paths, every file except root manifest.json and manifest.sha256; each path, byte size and SHA-256 in compact sort_keys=True ensure_ascii=False JSON, UTF-8 plus final LF. SHA-256 of those canonical manifest bytes."},
        "driver_ids": ["seawitch"], "machine_ids": [data.MACHINE_ID], "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
        "runtime": {
            "game": "seawitch", "rom_archive_sha256": data.ROM_SHA256,
            "emulator": {"binary": "pinmame64.dll", "sha256": data.LIBRARY_SHA256, "built_from_revision": data.PINMAME_REVISION},
            "raw_runs": raw_runs,
            "command_template": "python -B tools/run_pinmame_harness.py --library <working-root>/builds/seawitch-pinned/Release/pinmame64.dll --game seawitch --rom-path <authorized-read-only-ROM-root> --work-dir <new-state-directory> --scenario tools/harness-scenarios/stern/seawitch-<name>.json --output <external-run.json>. No keyboard handling, mechanics mask 0, default binary output mode. The linked official pinned CMake project was path-absolutized in an external project; native-and-rom-identity.json records the source and build hashes.",
            "observations": {
                "lamp_addresses_seen": lamp_addresses, "lamp_decoder_holes_not_seen": [16, 32, 48, 64],
                "lamp_addresses_driven_outside_self_test": sorted({e["number"] for e in gameplay["events"] if e["event"] == "lamp" and e["state"] > 0}),
                "solenoid_addresses_seen": sorted(set(seen(self_run, "solenoid")) | set(seen(gameplay, "solenoid"))),
                "physical_service_solenoid_to_public": {str(q): a for q, a in enumerate(cycle, 1)},
                "public_solenoid_decoder_holes_not_seen": [16],
                "runs": {
                    "self-test": {"ordered_solenoid_on_sequence": sequence, "solenoid_addresses_seen": seen(self_run, "solenoid"),
                                  "note": "The complete 19-position burn-in order agrees with the SDU decoder circuit. OPEN positions are swept too. A transition is not proof of physical fitment.",
                                  "limitation": "Burn-in multiplexes digit cycling, so the physical-to-public map is read from this game's own decoder/SCR circuit and corroborated by the sequence and gameplay, not by assigning semantic names to burn-in digits."},
                    "switch-test": {"named_action_observations": diagnostic_obs,
                                    "note": "Each isolated public 1-40 closure displays its own number. The six factory Not Used positions are included; ROM recognition does not establish a fitted contact. Three-second held snapshots decode the low seven segment bits; bit 0x80 is the comma. The earlier switch-test folder remained in the solenoid test and is retained for diagnosis only; switch-test-v2 is the accepted sweep."},
                    "gameplay": {"named_action_observations": gameplay_obs, "solenoid_addresses_seen": seen(gameplay, "solenoid"),
                                 "note": "Each bumper and sling fires its own coil; the final target of each bank causes its reset; held outhole causes repeat serves/resets, release advances play; tilt drops relay 19. Lower button inputs publish both synthetic outputs of their pair. Lamp 51 changes during this game despite having no printed load; its transition during the upper-button-83 action is background activity and is not evidence that 83 controls it. All four unlisted SCR fitments remain unknown."},
                },
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.runs)
    if args.write:
        write_json(ROOT / OUTPUT, result)
    elif (ROOT / OUTPUT).read_bytes() != canonical_bytes(result):
        raise RuntimeError("Seawitch runtime evidence drifted from retained runs")
    print("Seawitch runtime evidence matches the retained runs.")


if __name__ == "__main__":
    main()
