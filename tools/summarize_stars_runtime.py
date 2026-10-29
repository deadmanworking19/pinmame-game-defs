"""Recompute compact Stars evidence from retained, immutable fresh-state runs."""
from __future__ import annotations

import hashlib
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from build_external_evidence_manifest import check_manifest

GLYPHS = {value: str(i) for i, value in enumerate((63, 6, 91, 79, 102, 109, 125, 7, 127, 111))}
COIL_TEST = {1: 1, 11: 2, 2: 3, 12: 4, 3: 5, 13: 6, 4: 7, 7: 8,
             14: 9, 9: 10, 5: 11, 8: 12, 10: 13, 15: 14, 6: 15, 19: 16, 18: 17}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def number(segments: list[int]) -> int | None:
    text = "".join(" " if (v & 127) == 0 else GLYPHS.get(v & 127, "?") for v in segments).strip()
    return int(text) if text.isdigit() else None


def build(directory: Path) -> dict:
    runs = {name: load_json(directory / f"{name}.json") for name in
            ("self-test", "solenoid-test", "switch-test", "gameplay")}
    result = {"format": "pinmame-stars-runtime-evidence", "version": 1,
              "pinmame_revision": "46e1a01a0f73dc5ce163d98db1ae435883ecc450",
              "rom_archive_sha256": "e6bda46142255332e6d38b8b530840c8faed9e1f08023068b64879a2218c5b72",
              "scope": "Original stars only; callbacks are host-timed. Writes/readback are not ROM evidence.",
              "runs": {}, "coil_test": {}, "switch_test": {}}
    for name, run in runs.items():
        if run["failure"] is not None or run["game"] != "stars" or run["handle_mechanics"] != 0:
            raise RuntimeError(f"Unsuccessful or wrong Stars run: {name}")
        result["runs"][name] = {"path": f"stern.stars.1978/harness/{name}.json",
                                 "sha256": digest(directory / f"{name}.json"),
                                 "library_sha256": run["library_sha256"], "scenario_sha256": run["scenario"]["sha256"],
                                 "initial_switches": run["initial_switches"],
                                 "steps": [{"label": s["label"], "transitions": {
                                     channel: [{"number": row["number"], "states": sorted(set(row["states"])),
                                                "count": len(row["states"])} for row in rows]
                                     for channel, rows in s.get("transitions", {}).items()}}
                                     for s in run["steps"]]}
    coil = runs["solenoid-test"]
    start = next(s["time_s"] for s in coil["snapshots"] if s["label"] == "coil test checkpoint")
    for event in coil["events"]:
        if event["event"] != "solenoid" or not event["state"] or event["time_s"] < start:
            continue
        frames = [e for e in coil["events"] if e["event"] == "display" and e["index"] == 0
                  and e["time_s"] <= event["time_s"] + 0.25]
        value = number(frames[-1]["segments"]) if frames else None
        if value is None:
            raise RuntimeError(f"Unreadable Stars coil-test display: {event}")
        address = event["number"]
        if COIL_TEST.get(address) != value:
            raise RuntimeError(f"Stars coil-test pairing changed: {address} -> {value}")
        result["coil_test"][str(address)] = value
    if len(result["coil_test"]) != len(COIL_TEST):
        raise RuntimeError("Stars coil-test cycle is incomplete")
    switch_run = runs["switch-test"]
    for step in switch_run["steps"]:
        if not step["label"].startswith("matrix diagnostic "):
            continue
        address = step["switch"]
        edges = [e for e in switch_run["events"] if e["event"] == "switch" and e.get("step") == step["step"]]
        start, end = edges[0]["time_s"], edges[-1]["time_s"]
        frames = [e for e in switch_run["events"] if e["event"] == "display" and e["index"] == 0
                  and start + 0.2 <= e["time_s"] <= end]
        # This ROM alternates the contact number with zero; a blank snapshot
        # alone would incorrectly classify approximately half the sweep absent.
        values = sorted({n for e in frames if (n := number(e["segments"])) not in (None, 0)})
        result["switch_test"][str(address)] = {"displayed_numbers": values,
                                               "own_number_seen": address in values,
                                               "segments": next((e["segments"] for e in frames if number(e["segments"]) == address), None)}
        # Intermediate multiplexed frames can contain only one digit of a
        # two-digit number. Keep them in the evidence, rather than relabel them.
        if (address <= 40 and address not in values) or (address > 40 and values):
            raise RuntimeError(f"Stars switch diagnostic changed: {address}: {values}")
    if len(result["switch_test"]) != 56:
        raise RuntimeError("Stars full switch diagnostic sweep is incomplete")
    observations = {}
    raw_runs = []
    for name, run in runs.items():
        if run["library_sha256"] != "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5":
            raise RuntimeError("Stars run used a different native binary")
        raw_runs.append({"name": name, "sha256": digest(directory / f"{name}.json"),
                         "scenario_path": f"tools/harness-scenarios/stern/stars-{name}.json",
                         "scenario_sha256": run["scenario"]["sha256"], "action_count": len(run["steps"]),
                         "self_test_pulses": sum(s.get("switch") == -7 for s in run["steps"]),
                         "nvram_initialization": "Fresh newly created isolated state directory; no inherited NVRAM",
                         "boot_wait_s": 25, "initial_switches": run["initial_switches"]})
        actions = []
        for step in run["steps"]:
            if step.get("switch") is None:
                continue
            changed = step.get("transitions", {}).get("solenoids", [])
            actions.append({"label": step["label"], "input_kind": "switch", "input_address": step["switch"],
                            "observed_switch_addresses": [], "host_stimulus_switch_addresses": [step["switch"]],
                            "active_solenoid_addresses": [r["number"] for r in changed if 1 in r["states"]],
                            "transitioned_solenoid_addresses": [r["number"] for r in changed],
                            "result": "observed" if changed else "no_matching_transition"})
            if name == "switch-test" and step["label"].startswith("matrix diagnostic "):
                response = result["switch_test"][str(step["switch"])]
                actions[-1]["result"] = "observed" if response["own_number_seen"] else "no_matching_transition"
                actions[-1]["display_responses"] = ([] if not response["own_number_seen"] else [{
                    "snapshot_label": step["label"] + " during held window (complete multiplexed frame)",
                    "display_index": 0, "segments": response["segments"],
                    "decoded_segment_positions": list(range(6)), "interpreted_text": str(step["switch"]),
                    "diagnostic_address": step["switch"]}])
        observations[name] = {"solenoid_addresses_seen": sorted({e["number"] for e in run["events"] if e["event"] == "solenoid"}),
                              "named_action_observations": actions,
                              "note": "Direct writes, keyboard/mechanics disabled; host readback is not ROM observation. Callback times are host times, not physical timings."}
    return {"format": "pinmame-machine-evidence", "version": 1,
            "extractor": {"id": "tools/summarize_stars_runtime.py", "version": 1},
            "source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame",
                       "revision": result["pinmame_revision"], "path": "external:pinmame-review-artifacts/stern.stars.1978/harness",
                       "sha256": check_manifest(directory, "stars"), "license": "NOASSERTION",
                       "attribution": "User-authorized original Stars ROM; project-generated traces",
                       "quality": "observed", "manifest_algorithm": "tools/build_external_evidence_manifest.py: case-sensitive sorted POSIX relative paths, byte sizes and SHA256; canonical UTF-8 compact sorted-key JSON plus LF, excluding root manifest.json/manifest.sha256; SHA256 of those bytes"},
            "driver_ids": ["stars"], "machine_ids": ["stern.stars.1978"],
            "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
            "runtime": {"game": "stars", "rom_archive_sha256": result["rom_archive_sha256"],
                        "emulator": {"binary": "pinmame64.dll", "sha256": runs["gameplay"]["library_sha256"],
                                     "built_from_revision": result["pinmame_revision"]}, "raw_runs": raw_runs,
                        "command_template": "python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-46e1a01a/Release/pinmame64.dll --game stars --rom-path <authorized-ROM-library> --work-dir <fresh-state-directory> --scenario tools/harness-scenarios/stern/stars-<name>.json --output <review-artifacts>/stern.stars.1978/harness/<name>.json; default binary outputs, mechanics 0, direct switch writes only",
                        "observations": {"physical_service_solenoid_to_public": {str(v): int(k) for k, v in result["coil_test"].items()},
                                         "switch_to_lamp": {"7": 61}, "runs": observations}}}
