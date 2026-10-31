"""Recompute schema-conformant Batman Forever runtime evidence from immutable external runs.

The reading seed binds visually checked DMD frames to pixel digests. Raw traces, source PGMs,
NVRAM and ROMs stay external. The builder refuses changed traces, scenarios, manifests, frames,
libraries and harness implementations, and checks every step a claim rests on. Exploratory and
failed runs live beside the final runs under harness/ and are never read here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import zipfile

from build_external_evidence_manifest import canonical_bytes, check_manifest
from recorded_repository_source import verify_recorded_source

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "tools/seeds/sega/batman-forever-1995-runtime-readings.json"
OUTPUT = ROOT / "evidence/runtime/data-east/batman-forever-batmanf-service-tests.json"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
# Repository revision whose runner bytes were recorded in the runtime seed.
HARNESS_REVISION = "3552ec1db9dd6c658058f3bd52918bb3f02c4e01"
KEY = "sega.batman-forever.1995"
MANIFEST_SHA = "153f5ea6e48d7722d0f15f8d1a78fd9040b4ea3a129a282b710bbfe9e39f3ee2"
GAMEPLAY = {
    "trough-lockout": 1, "trough-upkick": 2, "gun-trigger-autolaunch": 3, "top-eject-kick": 5,
    "output-17": 17, "output-18": 18, "output-19": 19, "output-20": 20, "output-21": 21, "output-22": 22,
    "drop-bank-reset": 7, "vuk-kick": 4, "lock-reserve-lockout": 1, "second-upkick": 2, "second-launch": 3,
    "batcave-exit-kick": 16, "cannon-motor-starts": 14, "gun-trigger-fires-cannon": 15,
}
# The host write each checkpoint answers; a wait observes the response to the write just before it.
STIMULUS = {"drop-bank-reset": [18, 19, 20, 21], "lock-reserve-lockout": [62], "trough-lockout": [3, 82]}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_rom(seed):
    """Only the explicitly supplied existing ROM root is read."""
    if not (rom_root := os.environ.get("PINMAME_ROM_LIBRARY_ROOT")):
        return
    archive = Path(rom_root) / "batmanf.zip"
    if digest(archive) != seed["rom_archive_sha256"]:
        raise ValueError("Batman Forever ROM archive changed")
    with zipfile.ZipFile(archive) as zipped:
        members = []
        for item in zipped.infolist():
            data = zipped.read(item)
            members.append({"name": item.filename, "size": item.file_size, "crc32": f"{item.CRC:08x}",
                            "sha1": hashlib.sha1(data).hexdigest(), "sha256": hashlib.sha256(data).hexdigest()})
    if sorted(members, key=lambda m: m["name"]) != seed["rom_members"]:
        raise ValueError("Batman Forever ROM member inventory changed")


def verified_runs(review_root):
    seed = read_json(SEED)
    base = review_root / KEY / "final"
    verify_recorded_source(ROOT, HARNESS_REVISION, "tools/run_pinmame_harness.py", seed["base_harness_sha256"])
    if check_manifest(base, "batmanf") != MANIFEST_SHA:
        raise ValueError("Batman Forever raw evidence manifest changed")
    runs = {}
    for name, pin in seed["runs"].items():
        path = base / name / "run.json"
        if digest(path) != pin["sha256"]:
            raise ValueError(f"Batman Forever raw run changed: {name}")
        run = read_json(path)
        if (run["failure"] or run["game"] != "batmanf" or run["handle_mechanics"] != 0
                or run["library_sha256"] != seed["library_sha256"]):
            raise ValueError(f"not a successful, pinned Batman Forever run: {name}")
        scenario = base / name / PureWindowsPath(run["scenario"]["path"]).name
        if digest(scenario) != run["scenario"]["sha256"] or read_json(ROOT / pin["scenario_path"]) != read_json(scenario):
            raise ValueError(f"Batman Forever scenario changed: {name}")
        runs[name] = run
    if len({run["work_dir"] for run in runs.values()}) != len(runs):
        raise ValueError("Batman Forever runs must use distinct fresh state directories")
    verify_rom(seed)
    return seed, runs


def snapshot(run, label):
    matches = [s for s in run["snapshots"] if s["label"] == label]
    if len(matches) != 1:
        raise ValueError(f"expected one snapshot {label}")
    return matches[0]


def step(run, label):
    matches = [s for s in run["steps"] if s["label"] == label]
    if len(matches) != 1:
        raise ValueError(f"expected one step {label}")
    return matches[0]


def watched(snap):
    return {w["number"]: w["state"] for w in snap["watched_switches"]}


def transitions(run, label):
    return {t["number"]: t["states"] for t in step(run, label)["transitions"]["solenoids"]}


def diagnostic_readings(review_root, seed, runs):
    from PIL import Image

    readings = []
    for reading in seed["readings"]:
        run = runs[reading["run"]]
        snap = snapshot(run, reading["label"])
        display = snap["displays"][0]
        frame = review_root / KEY / "final" / reading["run"] / "dmd" / PureWindowsPath(display["artifact"]).name
        with Image.open(frame) as pixels:
            valid = (pixels.size == (192, 64)
                     and hashlib.sha256(pixels.tobytes()).hexdigest() == reading["pixel_sha256"]
                     and display["pixel_sha256"] == reading["pixel_sha256"])
        if not valid:
            raise ValueError(f"Batman Forever visually read DMD frame changed: {frame}")
        group, address = reading["group"], reading.get("address")
        levels = watched(snap)
        if group == "switch":
            # A closed public address and every other address open; 63/64 are overwritten by the
            # flipper column, so the button copy is checked at 84 instead.
            expected = {84: {84: 1, 63: 1}}.get(address, {} if address in (63, 64) else {address: 1})
            others = {n: s for n, s in levels.items() if n not in expected and n not in (63, 64, 82, 84)}
            if any(levels.get(n) != s for n, s in expected.items()) or any(others.values()):
                raise ValueError(f"switch reading without its public level: {reading['label']}")
        elif group == "lamp" and snap["active_lamps"] != [address]:
            raise ValueError(f"lamp reading without its lamp: {reading['label']}")
        elif group == "solenoid":
            entry = int(reading["label"].split("-")[1])
            fired = None if address == 6 else transitions(run, f"entry-{entry}-fired")
            if address != 6 and 1 not in fired.get(address, []):
                raise ValueError(f"coil reading without its output: {reading['label']}")
        elif group == "screen" and (any(levels.values()) or snap["active_lamps"] not in ([], [33, 34])):
            raise ValueError(f"rest screen with an active input or lamp: {reading['label']}")
        item = {"label": f"{reading['run']}: {reading['label']}", "display_index": 0,
                "pixel_sha256": reading["pixel_sha256"], "interpreted_text": interpreted(reading),
                "active_solenoid_addresses": snap["active_solenoids"]}
        readings.append(item)
    return readings


def interpreted(reading):
    parts = [reading["name"]]
    if reading["group"] == "switch":
        parts += [p for p in (reading.get("part"), f"{reading['return_wire']} RETURN {reading['return_pin']}",
                              f"DRIVE {reading['drive_wire']} {reading['drive']}") if p]
    elif reading["group"] == "lamp" and reading.get("bulb"):
        parts += [f"bulb {reading['bulb']}", f"{reading['return_wire']} {reading['return_pin']}",
                  f"{reading['drive_wire']} {reading['drive']}"]
    elif reading["group"] == "solenoid" and reading.get("cpu"):
        parts.append(f"CPU {reading['cpu']}")
    return "; ".join(parts)


def coil_test_observations(run):
    observations = []
    for entry in range(1, 31):
        if entry == 11:
            continue
        fired = transitions(run, f"entry-{entry}-fired")
        observations.append({
            "label": f"entry-{entry}-fired", "input_kind": "switch", "input_address": 3,
            "observed_switch_addresses": [], "host_stimulus_switch_addresses": [3],
            "active_solenoid_addresses": [],
            "transitioned_solenoid_addresses": sorted(n for n, states in fired.items() if 1 in states and n not in (10, 23)),
            "result": "observed",
        })
    held = transitions(run, "entry-20-select-plus")
    if transitions(run, "entry-20-fired").get(13) != [1] or held.get(13) != [0]:
        raise ValueError("driver 13 hold in the COIL TEST changed")
    return observations


def gameplay_observations(run):
    observations = []
    steps = run["steps"]
    for index, item in enumerate(steps):
        if item["label"] not in GAMEPLAY:
            continue
        address = GAMEPLAY[item["label"]]
        if address not in {m["number"] for m in item["matched_outputs"] if 1 in m["states"]}:
            raise ValueError(f"Batman Forever gameplay checkpoint did not fire: {item['label']}")
        stimulus = item if "switch" in item else steps[index - 1]
        observations.append({
            "label": item["label"], "input_kind": "switch", "input_address": stimulus["switch"],
            "observed_switch_addresses": [],
            "host_stimulus_switch_addresses": STIMULUS.get(item["label"], [stimulus["switch"]]),
            "active_solenoid_addresses": [], "transitioned_solenoid_addresses": [address], "result": "observed",
        })
    for label, addresses in (("left-button", {47, 48}), ("right-button", {45, 46})):
        states = transitions(run, label)
        if {n for n, s in states.items() if s == [1, 0]} != addresses:
            raise ValueError(f"Batman Forever paired button states changed: {label}")
        observations.append({
            "label": label + ": paired states asserted and released together", "input_kind": "switch",
            "input_address": step(run, label)["switch"], "observed_switch_addresses": [],
            "host_stimulus_switch_addresses": [step(run, label)["switch"]], "active_solenoid_addresses": [],
            "held_synthetic_solenoid_addresses": sorted(addresses),
            "transitioned_solenoid_addresses": sorted(addresses), "result": "observed",
        })
    return observations


def build(review_root):
    seed, runs = verified_runs(review_root)
    readings = diagnostic_readings(review_root, seed, runs)
    switch_run = runs["switch-test"]
    copies = {82: 64, 84: 63}
    for button, matrix in copies.items():
        if watched(snapshot(switch_run, f"switch-{button}-closed")).get(matrix) != 1:
            raise ValueError(f"flipper column copy {button}->{matrix} not observed")
    if any(watched(snapshot(switch_run, f"switch-{n}-closed")).get(n) != 0 for n in (63, 64)):
        raise ValueError("a direct matrix write to 63/64 was not overwritten")
    cycle = [e["number"] for e in runs["cycling-coils"]["events"] if e["event"] == "solenoid" and e["state"]]
    if not {6, 13} <= set(cycle):
        raise ValueError("cycling test no longer publishes drivers 6 and 13")
    for name, run in runs.items():
        if any(e["event"] == "solenoid" and 37 <= e["number"] <= 44 for e in run["events"]):
            raise ValueError(f"a printer line transition appeared in {name}")
    run_notes = {
        "switch-test": "SWITCH TEST: every public address 1-64 and 81-88 held 0.45 s, then 0.3 s snapshots for "
                       "the slow-debounce addresses 32, 44, 45, 46 and 60-62, whose names appear only after "
                       "0.6-1.2 s. The display can lag one address; readings cite only frames whose watched "
                       "levels show the read address alone. Direct writes to 63/64 read back 0 (the flipper "
                       "column overwrites them); 82 and 84 read back as 64 and 63.",
        "lamp-test": "SINGLE LAMP TEST: each Start press lit exactly the stepped lamp 1-64. Frames at steps 1 "
                     "and 21 show the display board's power-up version screen instead of the test, so those "
                     "two readings come from lamp-test-2.",
        "lamp-test-2": "Same scenario re-run in a new state directory; cited only for lamps 1 and 21.",
        "coil-test": "COIL TEST: + shows the next entry with its wiring and RUN fires it; each entry fired "
                     "only its own public address (the 1R-8R entries switch relay 10 first). #6L: NOT USED "
                     "offers no RUN. RUN on #13: NOT USED holds public 13 on until the selection leaves RUN. "
                     "Relay 10 has no entry of its own.",
        "cycling-coils": "CYCLING COILS walks 1-9 with each muxed 25-32 behind relay 10, then 11-22, and also "
                         "pulses 6 and holds 13 although its display names both NOT USED. Neither 6 nor 13 "
                         "published state in any gameplay or attract run.",
        "gameplay": "Fresh four-ball trough, cannon at home. Same-run checkpoints: lockout serve, up-kick, "
                    "gun-trigger skill-shot launch, top eject, bumpers, slings, Laser Kick, C-A-V-E bank "
                    "reset on the fourth target, VUK, lock at 62 answered by a replacement serve (with an "
                    "automatic launch of that ball), Batcave exit kicker, cannon load starting motor relay 14 "
                    "after about 2 s, and the gun trigger firing cannon 15. Both cabinet buttons assert and "
                    "release their paired synthetic states.",
        "sega-adjustments": "MAIN MENU: the right flipper button steps DIAG, AUD, ADJ, RESET, QUIT and HELP and "
                            "wraps; the manual's PRNT icon is absent. ADJ > SEGA, stepped with Start, ends at "
                            "Adjustment 43 GAME ID and wraps to 1 (Adjustment 2 has two pages), with no printer "
                            "adjustment. No 37-44 transition.",
        "bat-adjustments": "ADJ > BAT, stepped with Start, runs 44-52 and wraps from 52 NOVICE GAME AVAILABLE "
                           "to 44; the manual's printer adjustments 52-54 are absent. No 37-44 transition.",
    }
    raw_runs, attributed = [], {}
    for name, run in runs.items():
        pin = seed["runs"][name]
        raw_runs.append({
            "name": name, "sha256": pin["sha256"], "self_test_pulses": 0,
            "scenario_path": pin["scenario_path"], "scenario_sha256": digest(ROOT / pin["scenario_path"]),
            "action_count": run["scenario"]["action_count"], "snapshot_count": len(run["snapshots"]),
            "watch_switches": run["watch_switches"], "initial_switches": run["initial_switches"],
            "nvram_initialization": "New empty run-specific state directory; no inherited NVRAM.",
            "boot_wait_s": 2,
        })
        canonical_scenario = hashlib.sha256(canonical_bytes(read_json(ROOT / pin["scenario_path"]))).hexdigest()
        attributed[name] = {
            "solenoid_addresses_seen": sorted({e["number"] for e in run["events"] if e["event"] == "solenoid"}),
            "ordered_solenoid_on_sequence": [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"]],
            "note": run_notes[name] + " Raw scenario SHA256 " + run["scenario"]["sha256"]
                    + "; canonical parsed repository scenario SHA256 " + canonical_scenario + ".",
        }
    attributed["coil-test"]["named_action_observations"] = coil_test_observations(runs["coil-test"])
    attributed["gameplay"]["named_action_observations"] = gameplay_observations(runs["gameplay"])
    all_events = [e for run in runs.values() for e in run["events"]]
    return {
        "format": "pinmame-machine-evidence", "version": 1,
        "extractor": {"id": "tools/build_batman_forever_runtime.py", "version": 1},
        "source": {
            "kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame",
            "revision": REVISION, "path": "review-artifacts/" + KEY + "/final",
            "sha256": MANIFEST_SHA, "quality": "observed", "license": "NOASSERTION",
            "attribution": "Primary curator; user-authorized existing batmanf (USA CPU 4.01) ROM",
            "manifest_algorithm": "tools/build_external_evidence_manifest.py --game batmanf; case-sensitive "
                                  "relative POSIX sort, path/size/SHA256 per file, canonical JSON plus LF; "
                                  "manifest.json/manifest.sha256 excluded.",
        },
        "driver_ids": ["batmanf"], "machine_ids": [KEY],
        "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
        "runtime": {
            "game": "batmanf", "rom_archive_sha256": seed["rom_archive_sha256"],
            "emulator": {"binary": "pinmame64.dll", "sha256": seed["library_sha256"], "built_from_revision": REVISION},
            "raw_runs": raw_runs,
            "command_template": "python tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game batmanf "
                                "--rom-path <authorized-existing-rom-root> --work-dir <new-empty-state-directory> "
                                "--scenario <raw_run.scenario_path> --dmd-dir <external-run-dmd> --output "
                                "<external-run.json>. Keyboard handling off, mechanisms off, binary solenoid "
                                "mode, default 2 s boot wait. DMD menus are reached by counted presses; the "
                                "frame readings are pinned to pixel digests in "
                                "tools/seeds/sega/batman-forever-1995-runtime-readings.json (SHA256 "
                                + digest(SEED) + "), with the ROM members, library and harness digests.",
            "observations": {
                "service_language": "English, USA CPU 4.01NV / display A4.01, November 1, 1995",
                "lamp_addresses_seen": sorted({e["number"] for e in all_events if e["event"] == "lamp"}),
                "solenoid_addresses_seen": sorted({e["number"] for e in all_events if e["event"] == "solenoid"}),
                "diagnostic_snapshots": readings, "runs": attributed,
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(args.review_root), indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        if OUTPUT.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise ValueError("Batman Forever runtime evidence drifted")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(payload)


if __name__ == "__main__":
    main()
