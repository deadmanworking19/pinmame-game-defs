"""Build the committed Rocky and Bullwinkle runtime evidence from the retained harness runs.

Reads the retained raw runs of the 3.20 (``rab_320``) service tests, a game start and five in-game probes
(``PINMAME_REVIEW_ARTIFACTS_ROOT``), pairs the curator's visual DMD readings (``tools/rab_readings.json``) with each
frame's pixel digest, derives the switch-to-coil, switch-to-lamp and test-button observations, and writes two
committed files:

* ``evidence/runtime/data-east/adventures-of-rocky-and-bullwinkle-and-friends-rab_320-service-tests.json``, a
  ``pinmame-machine-evidence`` bundle, and
* ``tools/rab_runtime.json``, the compact facts the curator consumes.

The raw runs, DMD frames and isolated state directories stay external under the working root, covered by a
canonical manifest (``tools/build_external_evidence_manifest.py``). ``--check`` rebuilds both files and refuses
any difference; a frame whose pixels no longer hash to the digest that was read is refused.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

import build_external_evidence_manifest as manifest
import rab_manual

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.adventures-of-rocky-and-bullwinkle-and-friends.1993"
SESSION = "adventures-of-rocky-and-bullwinkle-and-friends-1993/final/rab_320"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/adventures-of-rocky-and-bullwinkle-and-friends-rab_320-service-tests.json"
RUNTIME_PATH = ROOT / "tools/rab_runtime.json"
READINGS_PATH = ROOT / "tools/rab_readings.json"
SCENARIO_DIR = "tools/harness-scenarios/data-east"
RUNS = (
    "active-switches", "lamp-test", "diagnostic-tour", "cycling-coils", "cycling-flashers", "coil-test-fire",
    "laser-kick-test", "trough-serve", "hat-targets", "game-switches", "hat-trick-award", "save-nell", "nell-expires",
)
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "efe4c395840d66c2b51b63f38686429d4889e9915f364f1f8471714800c2d788"
ROM_ARCHIVE = Path("L:/Visual Pinball/VPinMAME/roms/rab_320.zip")
# The ROM prints ORG where the manual's matrix tables print ORN; nothing else differs in the abbreviations.
WIRE_SPELLING = {"ORG": "ORN"}
# Outputs that the ROM's own light shows and the game-on line drive by themselves.
BACKGROUND_OUTPUTS = {10, 11, 23, *range(25, 33), 45, 46, 47, 48}
LASER_KICK_CANDIDATES = (32, 40, 10, 13, 14, 29, 52, 30, 38, 44, 45, 46, 31, 39, 37, 22, 23, 24, 9)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_wires(text: str) -> str:
    text = re.sub(r"-\s+", "-", text)
    return " ".join("-".join(WIRE_SPELLING.get(part, part) for part in token.split("-")) for token in text.split())


def load_run(base: Path, name: str) -> dict:
    """A retained run, refused unless it is a clean rab_320 run on the pinned emulator build."""
    run = json.loads((base / name / "run.json").read_text(encoding="utf-8"))
    if run.get("game") != "rab_320" or run.get("library_sha256") != LIBRARY_SHA256 or run.get("failure"):
        raise SystemExit(f"{name}: not a clean rab_320 run on pinmame64.dll {LIBRARY_SHA256} (game {run.get('game')!r}, failure {run.get('failure')!r})")
    return run


def snapshot(run: dict, label: str) -> dict:
    matches = [item for item in run["snapshots"] if item["label"] == label]
    if len(matches) != 1:
        raise SystemExit(f"expected one snapshot labelled {label!r}, found {len(matches)}")
    return matches[0]


def step(run: dict, label: str) -> dict:
    matches = [item for item in run["steps"] if item["label"] == label]
    if len(matches) != 1:
        raise SystemExit(f"expected one step labelled {label!r}, found {len(matches)}")
    return matches[0]


def frame(base: Path, run_name: str, item: dict) -> dict:
    """The snapshot's DMD frame, refused unless the retained PGM's pixels hash to the recorded digest."""
    (display,) = [entry for entry in item["displays"] if entry.get("pixel_sha256")]
    path = base / run_name / "dmd" / Path(display["artifact"].replace("\\", "/")).name
    data = path.read_bytes()
    header, payload = data.split(b"\n", 2)[:2], data.split(b"\n", 3)[3]
    max_level = (1 << max(int(display["layout"].get("depth", 1)), 1)) - 1
    scaled = {round(level * 255 / max_level) for level in range(max_level + 1)}
    candidates = [payload] + ([bytes(round(value * max_level / 255) for value in payload)] if set(payload) <= scaled else [])
    if header != [b"P5", f"{display['layout']['width']} {display['layout']['height']}".encode("ascii")] or display["pixel_sha256"] not in {
        hashlib.sha256(raw).hexdigest() for raw in candidates
    }:
        raise SystemExit(f"{path}: the retained frame's pixels do not hash to the recorded digest {display['pixel_sha256']}")
    return display


def fired(run: dict, label: str, *, ignore=BACKGROUND_OUTPUTS) -> list[int]:
    return sorted({item["number"] for item in step(run, label)["transitions"]["solenoids"] if 1 in item["states"] and item["number"] not in ignore})


def intervals(run: dict, number: int, *, start: float = 0.0, end: float = float("inf")) -> list[tuple[float, float]]:
    """Every (on, off) interval of one solenoid in [start, end), from the run's timed events."""
    spans: list[tuple[float, float]] = []
    on_at = None
    for event in run["events"]:
        if event["event"] != "solenoid" or event["number"] != number or not start <= event["time_s"] < end:
            continue
        if event["state"] and on_at is None:
            on_at = event["time_s"]
        elif not event["state"] and on_at is not None:
            spans.append((on_at, event["time_s"]))
            on_at = None
    if on_at is not None:
        raise SystemExit(f"solenoid {number} is still on at the end of the window")
    return spans


def switch_times(run: dict, number: int, state: int) -> list[float]:
    return [event["time_s"] for event in run["events"] if event["event"] == "switch" and event["number"] == number and event["state"] == state]


def build(base: Path, *, write_manifest: bool) -> tuple[dict, dict]:
    readings = json.loads(READINGS_PATH.read_text(encoding="utf-8"))
    runs = {name: load_run(base, name) for name in RUNS}
    switch_chart = rab_manual.switch_data()["chart"]
    lamp_chart = rab_manual.lamp_data()["chart"]
    snapshots: list[dict] = []

    def read(reading: dict, label: str, text: str) -> dict:
        item = snapshot(runs[reading["run"]], reading["snapshot"])
        display = frame(base, reading["run"], item)
        if display["pixel_sha256"] != reading["pixel_sha256"]:
            raise SystemExit(f"{label}: frame {display['pixel_sha256']} is not the frame that was read ({reading['pixel_sha256']}); read it again")
        snapshots.append({
            "label": label, "display_index": 0, "pixel_sha256": display["pixel_sha256"], "nonzero_pixels": display["nonzero_pixels"],
            "interpreted_text": text, "active_solenoid_addresses": item["active_solenoids"],
        })
        return item

    # --- Screens: the diagnostics tour, the test baselines and wraps ----------------------------------------------
    for key in sorted(readings["screens"]):
        read(readings["screens"][key], f"Screen {key}", readings["screens"][key]["text"])
    tour = [step_["matched_text"] for step_ in runs["diagnostic-tour"]["steps"] if step_["type"] == "pulse_until_display"]

    # --- Active Switch Test -------------------------------------------------------------------------------------
    switch_names = {}
    for address in range(1, 65):
        reading = readings["switches"][str(address)]
        chart = switch_chart[address]
        if normalize_wires(reading["wires"]) != normalize_wires(f"{chart['drive']['wire']} {chart['return']['wire']}") or reading["number"] != address:
            raise SystemExit(f"switch {address}: ROM wires {reading['wires']} #{reading['number']} disagree with the manual chart")
        read(reading, f"Active Switch Test, public switch {address} held 900 ms", f"-ACTIVE SWITCH TEST- | {reading['name']} | {reading['wires']} #{address:02d}")
        switch_names[str(address)] = {"name": reading["name"], "wires": reading["wires"]}
    for key, reading in sorted(readings["flipper_column"].items()):
        text = "-ACTIVE SWITCH TEST- | NONE" if reading["name"] is None else f"-ACTIVE SWITCH TEST- | {reading['name']} | {reading['wires']} #{reading['number']}"
        read(reading, f"Active Switch Test, flipper-column public switch {key} held 900 ms", text)
    flipper_column = {key: reading["number"] for key, reading in readings["flipper_column"].items() if reading["name"]}
    if flipper_column != {"82": 16, "84": 15}:
        raise SystemExit(f"only 82 and 84 should reach the ROM from the flipper column, as 16 and 15: {flipper_column}")

    # --- Lamp Test ------------------------------------------------------------------------------------------------
    lamp_names = {}
    for address in range(1, 65):
        reading = readings["lamps"][str(address)]
        chart = lamp_chart[address]
        if normalize_wires(reading["wires"]) != normalize_wires(f"{chart['drive']['wire']} {chart['return']['wire']}") or reading["number"] != address:
            raise SystemExit(f"lamp {address}: ROM wires {reading['wires']} #{reading['number']} disagree with the manual chart")
        item = read(reading, f"Lamp Test, lamp {address} selected", f"-LAMP TEST- | {reading['name']} | {reading['wires']} #{address:02d}")
        lit = [entry["number"] for entry in step(runs["lamp-test"], reading["snapshot"])["transitions"]["lamps"] if 1 in entry["states"]]
        # One press must step exactly one lamp: a press that steps twice lights a lamp between snapshots.
        if item["active_lamps"] != [address] or lit != [address]:
            raise SystemExit(f"lamp test: {address} selected but lamps {item['active_lamps']} lit and {lit} turned on during the press")
        lamp_names[str(address)] = {"name": reading["name"], "wires": reading["wires"]}

    # --- Cycling Coils and Cycling Flashers ------------------------------------------------------------------------
    cycling = runs["cycling-coils"]
    entered = snapshot(cycling, "cycling coils tick 1")["time_s"]
    ons = [(event["time_s"], event["number"]) for event in cycling["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["number"] not in (10, 23)]
    start = [time_s for time_s, number in ons if number == 1 and time_s >= entered][0]
    order: list[int] = []
    for time_s, number in ons:
        if time_s < start:
            continue
        if number == 1 and order:
            break
        order.append(number)
    expected = [n for drive in range(1, 9) for n in (drive, drive + 24)] + [9, *range(11, 23)]
    if order != expected:
        raise SystemExit(f"unexpected cycling order: {order}")
    relay_before_right = []
    for number in range(25, 33):
        on_at = [time_s for time_s, n in ((e["time_s"], e["number"]) for e in cycling["events"] if e["event"] == "solenoid" and e["state"] == 1) if n == number and time_s >= start][0]
        relay = [e for e in cycling["events"] if e["event"] == "solenoid" and e["number"] == 10 and e["time_s"] <= on_at]
        relay_before_right.append(bool(relay) and relay[-1]["state"] == 1)
    if not all(relay_before_right):
        raise SystemExit("Cycling Coils: the relay at 10 is not on when a right-side output fires")
    flasher_ons = [event["number"] for event in runs["cycling-flashers"]["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["number"] in range(25, 33)]
    if flasher_ons[:16] != [*range(25, 33), *range(25, 33)]:
        raise SystemExit(f"unexpected cycling-flashers order {flasher_ons[:16]}")

    # --- Coil Test (select with the right flipper button, fire with Start) -------------------------------------------
    coil_test = []
    for reading in readings["coil_test"]:
        entry = reading["entry"]
        read(reading, f"Coil Test, entry {entry} {reading['number']}", f"-COIL TEST- | {reading['name']} | {reading['wires']} {reading['number']}")
        outputs = fired(runs["coil-test-fire"], f"entry {entry}: Start short press fires the selected entry", ignore={23, 45, 46, 47, 48})
        coil_test.append({"entry": entry, "number": reading["number"], "name": reading["name"], "wires": reading["wires"], "fired": outputs})
    expected_numbers = [f"#{n}{side}" for n in range(1, 9) for side in "LR"] + ["#09", *(f"#{n}" for n in range(11, 23))]
    if [entry["number"] for entry in coil_test] != expected_numbers:
        raise SystemExit("the Coil Test entries are not #1L-#8R, #09 and #11-#22")
    for entry in coil_test:
        tag = entry["number"][1:]
        public = int(tag[:-1]) + (24 if tag.endswith("R") else 0) if tag[-1] in "LR" else int(tag)
        if public not in entry["fired"] or any(n not in (public, 10) for n in entry["fired"]) or ((10 in entry["fired"]) != tag.endswith("R")):
            raise SystemExit(f"Coil Test {entry['number']}: fired {entry['fired']}, expected {public}" + (" after the relay at 10" if tag.endswith("R") else ""))
        entry["public"] = public

    # --- Laser Kick Test and the in-game switch probes ---------------------------------------------------------------
    laser = {}
    for number in LASER_KICK_CANDIDATES:
        laser[str(number)] = fired(runs["laser-kick-test"], f"Laser Kick Test: close public switch {number} for 1500 ms")
    if {key: value for key, value in laser.items() if value} != {"32": [22], "29": [5], "52": [4]}:
        raise SystemExit(f"unexpected Laser Kick Test responses {laser}")
    game_switches = {}
    for round_ in (1, 2):
        for number in (44, 45, 46, 30, 38):
            outputs = [n for n in fired(runs["game-switches"], f"round {round_}: close switched-solenoid switch {number} for 100 ms") if 17 <= n <= 22]
            game_switches.setdefault(str(number), []).append(outputs)
    pairs = {"44": [17], "45": [18], "46": [19], "30": [20], "38": [21]}
    if any(value != [pairs[key], pairs[key]] for key, value in game_switches.items()):
        raise SystemExit(f"unexpected switched-solenoid responses {game_switches}")

    # --- Hat targets: which lamp the ROM lights for each switch --------------------------------------------------------
    hat = []
    hat_run = runs["hat-targets"]
    for round_ in (1, 2):
        for number in (22, 23, 24):
            label = f"round {round_}: the ball hits hat target switch {number}"
            after = [n for n in snapshot(hat_run, label)["active_lamps"] if 57 <= n <= 60]
            moved = sorted({entry["number"] for entry in step(hat_run, label)["transitions"]["lamps"] if 57 <= entry["number"] <= 60})
            hat.append({"round": round_, "switch": number, "lamps_57_60_lit_after": after, "lamps_57_60_changed": moved})
    expected_hat = [
        (22, [57], [57]), (23, [57, 58], [58]), (24, [60], [57, 58, 59, 60]),
        (22, [57, 60], [57]), (23, [57, 58, 60], [58]), (24, [60], [57, 58, 59]),
    ]
    if [(h["switch"], h["lamps_57_60_lit_after"], h["lamps_57_60_changed"]) for h in hat] != expected_hat:
        raise SystemExit(f"unexpected hat target lamp responses {hat}")

    # --- Outputs 37-44 and the custom range over every run -------------------------------------------------------------
    moved_extra = sorted({event["number"] for run in runs.values() for event in run["events"] if event["event"] == "solenoid" and (37 <= event["number"] <= 44 or event["number"] >= 51)})
    if moved_extra:
        raise SystemExit(f"outputs {moved_extra} changed; the readings expect 37-44 and 51+ to stay at 0")

    # --- Game start (trough serve) ----------------------------------------------------------------------------------------
    serve = runs["trough-serve"]
    def pulses(label: str, number: int) -> int:
        return sum(entry["states"].count(1) for entry in step(serve, label)["transitions"]["solenoids"] if entry["number"] == number)
    eject_after_start = pulses("Press Start", 2) + sum(pulses(f"after Start tick {i}", 2) for i in range(1, 11))
    eject_in_shooter = sum(pulses(f"ball in shooter lane tick {i}", 2) for i in range(1, 9))
    launch = fired(serve, "press the Launch Button 9 with the ball on 14")
    outhole = pulses("Drain: the ball reaches the outhole 10", 1) + sum(pulses(f"ball on outhole tick {i}", 1) for i in range(1, 6))
    eject_after_drain = sum(pulses(f"after drain tick {i}", 2) for i in range(1, 9))
    idle = sorted({n for i in range(1, 9) for n in fired(serve, f"ball in shooter lane tick {i}")})
    serve_facts = {
        "trough_eject_pulses_after_start_with_13_closed": eject_after_start,
        "trough_eject_pulses_with_the_ball_on_14": eject_in_shooter,
        "launch_button_with_ball_on_14_fired": launch,
        "outhole_pulses_while_10_closed": outhole,
        "trough_eject_pulses_after_the_drained_ball_reached_11": eject_after_drain,
        "outputs_while_the_ball_rested_on_14": idle,
    }
    if eject_after_start < 5 or eject_in_shooter or launch != [16] or outhole < 3 or eject_after_drain < 3 or idle:
        raise SystemExit(f"trough serve: unexpected pulses {serve_facts}")

    # --- Hat Trick award: the playfield diverter, the backbox hat coils and the VUK kick -----------------------------
    award_run = runs["hat-trick-award"]
    starts = switch_times(award_run, 22, 1)
    if len(starts) != 4:
        raise SystemExit(f"hat trick award: expected four rounds, found {len(starts)}")
    awards = []
    for index, began in enumerate(starts, start=1):
        ended = starts[index] if index < len(starts) else float("inf")
        if fired(award_run, f"award {index}: the ball rolls over the left orbit bottom 33") != [13]:
            raise SystemExit(f"award {index}: the ROM did not fire only the playfield diverter 13 at the left orbit bottom")
        hat_coil = fired(award_run, f"award {index}: the ball rolls over the left orbit top 34")
        if len(hat_coil) != 1 or hat_coil[0] not in (3, 6, 7):
            raise SystemExit(f"award {index}: the left orbit top fired {hat_coil}, not one backbox hat coil")
        (closed_52,) = [t for t in switch_times(award_run, 52, 1) if began <= t < ended]
        (diverter,) = intervals(award_run, 13, start=began, end=ended)
        (kick,) = intervals(award_run, 4, start=began, end=ended)
        coil_spans = intervals(award_run, hat_coil[0], start=began, end=ended)
        if not (diverter[0] < closed_52 < diverter[1] <= kick[0]) or not 0 < kick[0] - closed_52 < 3.0:
            raise SystemExit(f"award {index}: the diverter {diverter}, the hole {closed_52} and the kick {kick} are out of order")
        after = sorted({
            entry["number"] for tick in range(11, 21)
            for entry in step(award_run, f"award {index}: after the kick tick {tick}")["transitions"]["lamps"] if entry["number"] in (47, 54, 61)
        })
        awards.append({
            "award": index, "hat_coil": hat_coil[0],
            "hat_coil_on_s": [round(off - on, 1) for on, off in coil_spans],
            "hat_coil_first_on_after_34_closed_s": round(coil_spans[0][0] - switch_times(award_run, 34, 1)[index - 1], 1),
            "diverter_13_on_s": round(diverter[1] - diverter[0], 1),
            "diverter_13_off_after_52_closed_s": round(diverter[1] - closed_52, 1),
            "vuk_4_kick_after_52_closed_s": round(kick[0] - closed_52, 1),
            "award_lamps_flashing_5_to_10_s_after_the_kick": after,
        })
    if [award["hat_coil"] for award in awards] != [3, 3, 7, 7] or [award["award_lamps_flashing_5_to_10_s_after_the_kick"] for award in awards] != [[54], [54], [61], [61]]:
        raise SystemExit(f"hat trick award: unexpected coils or award lamps {awards}")

    # --- Save Nell: the saw motor relay 9 ------------------------------------------------------------------------------
    nell = {}
    for name in ("save-nell", "nell-expires"):
        run = runs[name]
        completed = switch_times(run, 21, 1)
        (motor,) = intervals(run, 9)
        if not 0 <= motor[0] - completed[1] < 0.5:
            raise SystemExit(f"{name}: relay 9 did not start with the second completed bank ({motor}, {completed})")
        drops_while_on = [t for n in range(17, 22) for t in switch_times(run, n, 1) if motor[0] < t < motor[1]]
        if name == "save-nell":
            if len(drops_while_on) != 1 or not 0 <= motor[1] - drops_while_on[0] < 0.5:
                raise SystemExit(f"save-nell: relay 9 {motor} did not stop on the one drop target hit {drops_while_on}")
        elif drops_while_on:
            raise SystemExit(f"nell-expires: a drop target was hit while relay 9 ran: {drops_while_on}")
        first_bank_resets = len(intervals(run, 15, start=completed[0], end=completed[0] + 3.0))
        nell[name] = {
            "relay_9_on_after_bank_2_completed_s": round(motor[0] - completed[1], 1),
            "relay_9_on_s": round(motor[1] - motor[0], 1),
            "relay_9_on_after_bank_1": bool(intervals(run, 9, start=completed[0], end=completed[1])),
            "reset_15_pulses_after_bank_1_with_the_targets_held_down": first_bank_resets,
        }
        if name == "save-nell":
            nell[name]["relay_9_off_after_the_save_hit_s"] = round(motor[1] - drops_while_on[0], 1)

    # --- Raw-run records ----------------------------------------------------------------------------------------------------
    raw_runs = []
    per_run: dict[str, dict] = {}
    all_solenoids: set[int] = set()
    for name in RUNS:
        run = runs[name]
        scenario_path = ROOT / f"{SCENARIO_DIR}/rab-320-{name}.json"
        scenario_sha = sha256_file(scenario_path)
        if sha256_file(base / name / "scenario.json") != scenario_sha:
            raise SystemExit(f"{name}: retained scenario differs from the committed scenario")
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        checkpoints = [
            {"matched_text": step_["matched_text"], "after_service_pulses": step_["pulses"]}
            for step_ in run["steps"] if step_["type"] == "pulse_until_display"
        ]
        solenoids = sorted({event["number"] for event in run["events"] if event["event"] == "solenoid"})
        all_solenoids.update(solenoids)
        raw_runs.append({
            "name": name, "sha256": sha256_file(base / name / "run.json"),
            "scenario_path": f"{SCENARIO_DIR}/rab-320-{name}.json", "scenario_sha256": scenario_sha,
            "action_count": len(scenario["actions"]), "watch_switches": scenario.get("watch_switches", []),
            "self_test_pulses": sum(item["after_service_pulses"] for item in checkpoints),
            "nvram_initialization": "new empty isolated state directory; no NVRAM inherited", "boot_wait_s": 8.0,
            "snapshot_count": len(run["snapshots"]),
        })
        per_run[name] = {"diagnostic_checkpoints": checkpoints, "solenoid_addresses_seen": solenoids}
    per_run["cycling-coils"]["ordered_solenoid_on_sequence"] = order
    per_run["cycling-flashers"]["ordered_solenoid_on_sequence"] = flasher_ons[:16]
    per_run["laser-kick-test"]["named_action_observations"] = [{
        "label": f"Laser Kick Test: close public switch {number} for 1500 ms", "input_kind": "switch", "input_address": number,
        "observed_switch_addresses": [], "host_stimulus_switch_addresses": [number], "active_solenoid_addresses": [],
        "transitioned_solenoid_addresses": laser[str(number)], "result": "observed" if laser[str(number)] else "no_matching_transition",
    } for number in LASER_KICK_CANDIDATES]
    per_run["game-switches"]["named_action_observations"] = [{
        "label": f"round {round_}: close switched-solenoid switch {number} for 100 ms", "input_kind": "switch", "input_address": number,
        "observed_switch_addresses": [], "host_stimulus_switch_addresses": [number], "active_solenoid_addresses": [],
        "transitioned_solenoid_addresses": game_switches[str(number)][round_ - 1], "result": "observed",
    } for round_ in (1, 2) for number in (44, 45, 46, 30, 38)]
    per_run["trough-serve"]["note"] = (
        "The host moved the balls: a ball reached or left a switch only when the host wrote it, so the pulse counts measure the ROM's retries, not travel times. "
        "Counts exclude the light-show outputs (10, 11, 23 and 25-32)."
    )
    per_run["hat-targets"]["note"] = "Lamp states 57-60 after each hit are in the curator facts; flash-lamp pulses during the hits belong to the ROM's light shows."
    per_run["hat-trick-award"]["note"] = (
        "The host held the VUK switch 52 closed from the ball's arrival until the ROM fired 4, and opened it at once. Times are host-clock seconds between the "
        "harness's switch and solenoid callbacks, rounded to 0.1 s, so a loaded host can stretch them; the per-award figures are in the curator facts."
    )
    for name in ("save-nell", "nell-expires"):
        per_run[name]["note"] = (
            "The host held each drop target switch closed while its target was down and released all five about 3 s after the bank was completed, so the "
            "reset coil 15 retried while they stayed closed. Relay 9 timings are in the curator facts."
        )

    # Regeneration writes the external manifest; --check only verifies it and never touches the retained runs.
    try:
        manifest_digest = manifest.write_manifest(base, "rab_320") if write_manifest else manifest.check_manifest(base, "rab_320")
    except ValueError as error:
        raise SystemExit(f"retained runs: {error}") from error
    source_locator = (
        f"3.20 (rab_320) in {len(RUNS)} fresh-state harness runs: the Active Switch Test of public 1-64 and 81-88, the discrete Lamp Test, Cycling Coils, "
        "Cycling Flashers, the Coil Test fired entry by entry, the Laser Kick Test, a diagnostics tour, a game start with the host serving a ball from the trough, "
        "and five in-game probes (the hat targets, the switched-solenoid switches, four Hat Trick awards, a saved and an unsaved Save Nell timer); "
        f"{len(snapshots)} visually read 128x32 frames paired with their pixel digests; the raw runs stay under the working root with a canonical manifest"
    )
    facts = {
        "format": "pinmame-rab-runtime-facts",
        "version": 1,
        "source": EVIDENCE_PATH.relative_to(ROOT).as_posix(),
        "source_locator": source_locator,
        "diagnostics_tour": tour,
        "display_version": readings["screens"]["tour-display-version"]["text"],
        "rom_switch_names": switch_names,
        "rom_lamp_names": lamp_names,
        "cycling_coils_order": order,
        "coil_test": coil_test,
        "laser_kick_test": {key: value for key, value in laser.items() if value},
        "switched_solenoid_pairs": {key: value[0] for key, value in game_switches.items()},
        "hat_targets": hat,
        "trough_serve": serve_facts,
        "hat_trick_awards": awards,
        "save_nell": nell,
    }
    evidence = {
        "driver_ids": ["rab_320"],
        "extractor": {"id": "tools/build_rab_runtime_evidence.py", "version": 1},
        "format": "pinmame-machine-evidence",
        "machine_ids": [KEY],
        "mechanisms": [],
        "outputs": [],
        "recreation_notes": [],
        "runtime": {
            "game": "rab_320",
            "rom_archive_sha256": ROM_ARCHIVE_SHA256,
            "emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
            "raw_runs": raw_runs,
            "command_template": (
                "python tools/rab_harness.py --library <libpinmame> --game rab_320 --rom-path <read-only-rom-root> --work-dir <new-isolated-state> "
                f"--scenario {SCENARIO_DIR}/rab-320-<run>.json --boot-wait 8 --dmd-dir <external-dmd-dir> --output <external-run.json>. "
                "No keyboard handling: every stimulus is a direct public switch write (the Black Advance button at -7, the Green input at -6, then playfield and "
                "cabinet addresses). tools/rab_harness.py replaces only the display-title checkpoint with exact title-band matches of visually read retained "
                "frames (tools/rab_header_templates.json). Each DMD reading in diagnostic_snapshots was read by a curator from the retained 128x32 frame whose "
                "pixel digest is recorded beside it."
            ),
            "observations": {
                "service_language": "US English 3.20 (display ROM A3.00)",
                "solenoid_addresses_seen": sorted(all_solenoids),
                "lamp_addresses_seen": list(range(1, 65)),
                "diagnostic_snapshots": snapshots,
                "runs": per_run,
            },
        },
        "source": {
            "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external.",
            "kind": "runtime_scenario",
            "license": "NOASSERTION",
            "manifest_algorithm": (
                "source.sha256 is SHA-256 of manifest.json's exact UTF-8 bytes. manifest.json is compact canonical JSON with sorted keys, separators=(',', ':'), "
                "ensure_ascii=False, plus one LF; it lists every file below source.path except manifest.json and manifest.sha256 as {path, sha256, size}, using "
                "sorted POSIX-relative paths."
            ),
            "path": f"external:pinmame-review-artifacts/{SESSION}",
            "quality": "observed",
            "repository": "https://github.com/vpinball/pinmame",
            "revision": PINMAME_REVISION,
            "sha256": manifest_digest,
        },
        "states": [],
        "switches": [],
        "version": 1,
    }
    return evidence, facts


def _bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Rebuild and refuse any difference from the committed files.")
    args = parser.parse_args()
    root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if not root:
        raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT must point at the working root's review-artifacts directory")
    if ROM_ARCHIVE.is_file() and sha256_file(ROM_ARCHIVE) != ROM_ARCHIVE_SHA256:
        raise SystemExit(f"{ROM_ARCHIVE} is not the ROM archive the runs used")
    evidence, facts = build(Path(root) / SESSION, write_manifest=not args.check)
    outputs = ((EVIDENCE_PATH, _bytes(evidence)), (RUNTIME_PATH, _bytes(facts)))
    if args.check:
        for path, payload in outputs:
            if not path.is_file() or path.read_bytes().replace(b"\r\n", b"\n") != payload:
                raise SystemExit(f"{path} differs from the retained runs")
        print("Rocky and Bullwinkle runtime evidence matches the retained runs.")
        return
    for path, payload in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    print(f"Wrote {EVIDENCE_PATH.relative_to(ROOT)} and {RUNTIME_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
