"""Independently verify the retained Swords of Fury System 11 runtime traces.

This module deliberately has no project imports and never runs retained helper scripts.  It
reads the committed compact evidence plus the retained JSON traces and rederives the bounded
controller behaviour from raw events, snapshots, and display segments.

The compact evidence record must contain ``source_revision``, ``library_sha256``, the exact
17-entry ``successful_runs`` list, ``per_variant`` entries for l2/l1/rr1/rr1b, and
``coil_order`` copied from ``coil-order.json``.  ``source_register.files`` is optional; when
present it is a list of portable ``{path, sha256}`` records rooted at runtime-research.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any


MACHINE_ID = "williams.swords-of-fury.1988"
COMPACT_EVIDENCE = Path("tools/seeds/williams/swords-of-fury-runtime.json")
TAGS = ("l2", "l1", "rr1", "rr1b")
RUN_KINDS = ("init", "coil", "switch-edges", "gameplay-v2")
EXPECTED_RUNS = tuple(f"runs/{tag}-{kind}.json" for tag in TAGS for kind in RUN_KINDS) + ("runs/l2-switch-levels.json",)
DROP_RESETS = {17: 15, 18: 5, 19: 8, 20: 21, 21: 22}
COIL_OUTPUTS = tuple(range(1, 24)) + tuple(range(25, 33))
SYNTHETIC_FLIPPERS = {82: (60, (45, 46)), 84: (58, (47, 48))}

# The portable 16-segment table used by the harness.  Keep this local: retained decoder
# scripts are evidence inputs, not verifier dependencies.
SEGMENT_16 = {
    0x0000: " ", 0x0309: "!", 0x0220: '"', 0x2A4E: "#", 0x2A6D: "$",
    0x6E65: "%", 0x135D: "&", 0x0400: "'", 0x1400: "(", 0x4100: ")",
    0x7F40: "*", 0x2A40: "+", 0x0080: ",", 0x0840: "-", 0x0008: ".",
    0x4400: "/", 0x443F: "0", 0x2200: "1", 0x085B: "2", 0x084F: "3",
    0x0866: "4", 0x087D: "6", 0x0007: "7", 0x087F: "8", 0x086F: "9",
    0x0009: ":", 0x4001: ";", 0x4408: "<", 0x0848: "=", 0x1108: ">",
    0x2803: "?", 0x205F: "@", 0x0877: "A", 0x2A0F: "B", 0x0039: "C",
    0x220F: "D", 0x0079: "E", 0x0071: "F", 0x083D: "G", 0x0876: "H",
    0x2209: "I", 0x001E: "J", 0x1470: "K", 0x0038: "L", 0x0536: "M",
    0x1136: "N", 0x003F: "O", 0x0873: "P", 0x103F: "Q", 0x1873: "R",
    0x086D: "S", 0x2201: "T", 0x003E: "U", 0x4430: "V", 0x5036: "W",
    0x5500: "X", 0x2500: "Y", 0x4409: "Z", 0x1100: "\\", 0x000F: "]",
    0x5000: "^", 0x0006: "1",
}
DIGITS = {0x003F: "0", 0x0006: "1", 0x005B: "2", 0x004F: "3", 0x0066: "4", 0x006D: "5", 0x007D: "6", 0x0007: "7", 0x007F: "8", 0x006F: "9"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path, errors: list[str], label: str) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{label}: missing {path}")
        return None
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: cannot read {path}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label}: expected a JSON object in {path}")
        return None
    return value


def _normal(text: str) -> str:
    return " ".join(text.replace("0", "O").split())


def _segments_text(segments: Any) -> str | None:
    if not isinstance(segments, list) or not all(isinstance(value, int) for value in segments):
        return None
    output = []
    for value in segments:
        base = value & 0x7FFF
        output.append(SEGMENT_16.get(base, f"<0x{base:04x}>") + ("." if value & 0x8000 else ""))
    return "".join(output)


def _snapshot_text(snapshot: dict[str, Any]) -> str | None:
    displays = snapshot.get("displays")
    if not isinstance(displays, list):
        return None
    by_index = {item.get("index"): item for item in displays if isinstance(item, dict)}
    first = by_index.get(0)
    second = by_index.get(1)
    if not isinstance(first, dict) or not isinstance(second, dict):
        return None
    first_text = _segments_text(first.get("segments"))
    second_text = _segments_text(second.get("segments"))
    return None if first_text is None or second_text is None else first_text + second_text


def _snapshot_number(snapshot: dict[str, Any]) -> str | None:
    displays = snapshot.get("displays")
    if not isinstance(displays, list):
        return None
    display = next((item for item in displays if isinstance(item, dict) and item.get("index") == 2), None)
    if not isinstance(display, dict) or not isinstance(display.get("segments"), list) or len(display["segments"]) < 6:
        return None
    digits: list[str] = []
    for value in display["segments"][4:6]:
        if not isinstance(value, int) or value & 0x8000:
            return None
        base = value & 0x7FFF
        if base == 0:
            digits.append(" ")
        elif base in DIGITS:
            digits.append(DIGITS[base])
        else:
            return None
    return "".join(digits).strip()


def _snapshot(run: dict[str, Any], label: str, errors: list[str], run_label: str) -> dict[str, Any] | None:
    snapshots = run.get("snapshots")
    matches = [item for item in snapshots if isinstance(item, dict) and item.get("label") == label] if isinstance(snapshots, list) else []
    if len(matches) != 1:
        errors.append(f"{run_label}: expected exactly one snapshot {label!r}, found {len(matches)}")
        return None
    return matches[0]


def _step(run: dict[str, Any], label: str, errors: list[str], run_label: str) -> dict[str, Any] | None:
    steps = run.get("steps")
    matches = [item for item in steps if isinstance(item, dict) and item.get("label") == label] if isinstance(steps, list) else []
    if len(matches) != 1:
        errors.append(f"{run_label}: expected exactly one step {label!r}, found {len(matches)}")
        return None
    return matches[0]


def _active_solenoids(snapshot: dict[str, Any]) -> set[int] | None:
    values = snapshot.get("active_solenoids")
    return set(values) if isinstance(values, list) and all(isinstance(value, int) for value in values) else None


def _switch_state(snapshot: dict[str, Any], number: int) -> int | None:
    watched = snapshot.get("watched_switches")
    if not isinstance(watched, list):
        return None
    values = [item.get("state") for item in watched if isinstance(item, dict) and item.get("number") == number]
    return values[0] if len(values) == 1 and isinstance(values[0], int) else None


def _step_turns_on(step: dict[str, Any], number: int) -> bool:
    transitions = step.get("transitions")
    solenoids = transitions.get("solenoids") if isinstance(transitions, dict) else None
    if not isinstance(solenoids, list):
        return False
    return any(item.get("number") == number and 1 in item.get("states", []) for item in solenoids if isinstance(item, dict) and isinstance(item.get("states"), list))


def _relative_path(root: Path, value: str, errors: list[str], label: str) -> Path | None:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes retained root: {value!r}")
        return None
    return candidate


def _source_register_entries(compact: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    register = compact.get("source_register")
    if register is None:
        return []
    if not isinstance(register, dict) or not isinstance(register.get("files"), list):
        errors.append("compact source_register must be an object with a files list")
        return []
    entries = [entry for entry in register["files"] if isinstance(entry, dict)]
    if len(entries) != len(register["files"]):
        errors.append("compact source_register.files must contain only objects")
    return entries


def _verify_source_register(root: Path, entries: list[dict[str, Any]], errors: list[str]) -> None:
    for entry in entries:
        path = entry.get("path")
        expected = entry.get("sha256")
        if not isinstance(path, str) or not isinstance(expected, str):
            errors.append(f"compact source_register entry must have path and sha256 strings: {entry!r}")
            continue
        source = _relative_path(root, path, errors, "compact source_register")
        if source is not None and source.is_file() and _sha256(source) != expected:
            errors.append(f"source_register hash mismatch for {path}: expected {expected}, got {_sha256(source)}")
        elif source is not None and not source.is_file():
            errors.append(f"source_register path is not a file: {path}")


def _run_kind(relative: str) -> tuple[str, str] | None:
    name = Path(relative).stem
    for tag in TAGS:
        prefix = f"{tag}-"
        if name.startswith(prefix):
            return tag, name[len(prefix):]
    return None


def _verify_run_inventory(compact: dict[str, Any], root: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
    successful = compact.get("successful_runs")
    if not isinstance(successful, list):
        errors.append("compact successful_runs must be a list")
        return {}
    by_path = {item.get("run"): item for item in successful if isinstance(item, dict) and isinstance(item.get("run"), str)}
    if len(successful) != 17 or len(by_path) != 17 or set(by_path) != set(EXPECTED_RUNS):
        errors.append(f"compact successful_runs must name exactly the 17 retained runs; found {sorted(str(key) for key in by_path)}")
    loaded: dict[str, dict[str, Any]] = {}
    for relative in EXPECTED_RUNS:
        entry = by_path.get(relative)
        if not isinstance(entry, dict):
            continue
        run_path = _relative_path(root, relative, errors, "compact successful_runs")
        if run_path is None or not run_path.is_file():
            errors.append(f"retained raw run missing: {relative}")
            continue
        digest = _sha256(run_path)
        if entry.get("sha256") != digest:
            errors.append(f"{relative}: raw SHA-256 mismatch: expected {entry.get('sha256')!r}, got {digest}")
        run = _load_json(run_path, errors, relative)
        if run is None:
            continue
        loaded[relative] = run
        kind = _run_kind(relative)
        if kind is None:
            errors.append(f"{relative}: cannot derive variant and scenario kind")
            continue
        tag, scenario_kind = kind
        run_label = f"{tag} {scenario_kind}"
        if run.get("game") != f"swrds_{tag}":
            errors.append(f"{run_label}: game must be swrds_{tag!s}, got {run.get('game')!r}")
        if run.get("failure") is not None:
            errors.append(f"{run_label}: raw run reports failure {run.get('failure')!r}")
        if run.get("handle_mechanics") != 0:
            errors.append(f"{run_label}: handle_mechanics must be 0, got {run.get('handle_mechanics')!r}")
        initial = run.get("initial_switches", [])
        if not initial or initial[0] != {"switch": -6, "state": 1}:
            errors.append(f"{run_label}: initial service state must begin with switch -6 at 1")
        command = root / "logs" / f"{Path(relative).stem}.command.json"
        command_data = _load_json(command, errors, f"{run_label} command")
        if command_data is not None and command_data.get("exit_code") != 0:
            errors.append(f"{run_label}: command exit_code must be 0, got {command_data.get('exit_code')!r}")
        if entry.get("exit_code") != 0 or entry.get("failure") is not None:
            errors.append(f"compact {relative}: completion must record exit_code 0 and failure null")
        scenario = run.get("scenario")
        if not isinstance(scenario, dict):
            errors.append(f"{run_label}: missing raw scenario metadata")
            continue
        scenario_relative = entry.get("scenario")
        scenario_path = _relative_path(root, scenario_relative, errors, f"compact {relative} scenario") if isinstance(scenario_relative, str) else None
        if scenario_path is None or not scenario_path.is_file():
            errors.append(f"{run_label}: retained scenario missing for {scenario_relative!r}")
            continue
        scenario_hash = _sha256(scenario_path)
        if entry.get("scenario_sha256") != scenario_hash or scenario.get("sha256") != scenario_hash:
            errors.append(f"{run_label}: scenario SHA-256 does not agree with retained {scenario_relative}")
        raw_scenario_path = scenario.get("path")
        if not isinstance(raw_scenario_path, str) or not raw_scenario_path.replace("\\", "/").endswith("/" + scenario_relative):
            errors.append(f"{run_label}: raw scenario path {raw_scenario_path!r} is not {scenario_relative}")
        scenario_data = _load_json(scenario_path, errors, f"{run_label} scenario")
        steps = run.get("steps")
        action_count = len(steps) if isinstance(steps, list) else -1
        if not isinstance(steps, list):
            errors.append(f"{run_label}: steps must be a list")
        expected_action_count = entry.get("action_count")
        if action_count != expected_action_count or (scenario_data is not None and len(scenario_data.get("actions", [])) != action_count):
            errors.append(f"{run_label}: action count must agree among raw run, scenario, and compact evidence")
        expected_checkpoints = entry.get("checkpoint_matches")
        actual_checkpoints = [{key: step[key] for key in ("label", "matched_text", "pulses") if key in step} for step in steps if isinstance(step, dict) and step.get("type") in {"pulse_until_display", "pulse_until_output"}] if isinstance(steps, list) else []
        if actual_checkpoints != expected_checkpoints:
            errors.append(f"{run_label}: compact checkpoint_matches does not match raw actions")
    return loaded


def _static_switch_names(root: Path, errors: list[str]) -> dict[str, dict[int, str]]:
    raw = _load_json(root / "static-name-tables.json", errors, "static name tables")
    output: dict[str, dict[int, str]] = {}
    if raw is None:
        return output
    for tag in TAGS:
        details = raw.get(tag)
        switches = details.get("switches") if isinstance(details, dict) else None
        mapping = {item.get("address"): item.get("text") for item in switches if isinstance(item, dict) and isinstance(item.get("address"), int) and isinstance(item.get("text"), str)} if isinstance(switches, list) else {}
        if set(mapping) != set(range(1, 65)):
            errors.append(f"static name tables {tag}: expected switch names 1 through 64")
        else:
            output[tag] = mapping
    return output


def _expected_switch_response(static_names: dict[int, str], number: int) -> tuple[str, str]:
    if number <= 64 and number not in {58, 60}:
        return f"{number:02}", static_names[number]
    if number in SYNTHETIC_FLIPPERS:
        copied, _ = SYNTHETIC_FLIPPERS[number]
        return f"{copied:02}", static_names[copied]
    return "", "SWITCH EDGES"


def _walk_rows(run: dict[str, Any], tag: str, static_names: dict[int, str], errors: list[str], kind: str) -> list[dict[str, Any]]:
    run_label = f"{tag} {kind}"
    rows: list[dict[str, Any]] = []
    for number in range(1, 89):
        high = _snapshot(run, f"switch{number} level1", errors, run_label)
        low = _snapshot(run, f"switch{number} level0", errors, run_label)
        if high is None or low is None:
            continue
        expected_number, expected_text = _expected_switch_response(static_names, number)
        high_number = _snapshot_number(high)
        high_text = _snapshot_text(high)
        low_number = _snapshot_number(low)
        low_text = _snapshot_text(low)
        if high_number != expected_number or high_text is None or _normal(high_text) != _normal(expected_text):
            errors.append(f"{run_label}: switch {number} level1 expected diagnostic {expected_number!r} {_normal(expected_text)!r}, got {high_number!r} {_normal(high_text or '')!r}")
        if low_number != "" or low_text is None or _normal(low_text) != "SWITCH EDGES":
            errors.append(f"{run_label}: switch {number} level0 must restore SWITCH EDGES with no diagnostic number")
        active = _active_solenoids(high)
        if active is None:
            errors.append(f"{run_label}: switch {number} level1 lacks integer active_solenoids")
            active_list: list[int] = []
        else:
            active_list = sorted(active)
        if number in {58, 60} and _switch_state(high, number) != 0:
            errors.append(f"{run_label}: direct matrix {number} write must be overwritten to 0")
        if number <= 64 and number not in {58, 60} and _switch_state(high, number) != 1:
            errors.append(f"{run_label}: switch {number} level1 was not retained by the public matrix")
        if number in SYNTHETIC_FLIPPERS:
            copied, outputs = SYNTHETIC_FLIPPERS[number]
            low_active = _active_solenoids(low)
            if _switch_state(high, copied) != 1 or _switch_state(low, copied) != 0:
                errors.append(f"{run_label}: cabinet {number} must copy to matrix {copied} only while held")
            if active is None or not set(outputs).issubset(active) or low_active is None or set(outputs) & low_active:
                errors.append(f"{run_label}: cabinet {number} must hold synthetic outputs {outputs} only at level1")
        rows.append({"host_address": number, "level1_diagnostic_number": high_number, "level1_text": high_text, "level0_text": low_text, "level1_active_solenoids": active_list})
    return rows


def _verify_levels(run: dict[str, Any], names: dict[int, str], errors: list[str]) -> None:
    """Check ROM display frames during each hold, including periodic display blanks."""
    events = run.get("events", [])
    for number in range(1, 89):
        high = _snapshot(run, f"switch{number} level1", errors, "l2 switch-levels")
        low = _snapshot(run, f"switch{number} level0", errors, "l2 switch-levels")
        if high is None or low is None:
            continue
        expected_number, expected_text = _expected_switch_response(names, number)
        if _snapshot_number(low) != "":
            errors.append(f"l2 switch-levels: switch {number} release retained a diagnostic number")
        if not expected_number:
            if _snapshot_number(high) != "":
                errors.append(f"l2 switch-levels: unreachable switch {number} produced a diagnostic number")
            continue
        step = _step(run, f"switch{number} level1", errors, "l2 switch-levels")
        if step is None:
            continue
        starts = [e.get("time_s") for e in events if e.get("event") == "switch" and e.get("step") == step.get("step")]
        if not starts or not isinstance(starts[0], (int, float)) or not isinstance(high.get("time_s"), (int, float)):
            errors.append(f"l2 switch-levels: switch {number} has no bounded host hold interval")
            continue
        frames = {}
        matched = False
        for event in events:
            if event.get("event") != "display" or "segments" not in event:
                continue
            frames[event["index"]] = {"index": event["index"], "segments": event["segments"]}
            if starts[0] <= event.get("time_s", -1) <= high["time_s"] and all(index in frames for index in (0, 1, 2)):
                candidate = {"displays": list(frames.values())}
                if _snapshot_number(candidate) == expected_number and _normal(_snapshot_text(candidate) or "") == _normal(expected_text):
                    matched = True
                    break
        if not matched:
            errors.append(f"l2 switch-levels: switch {number} lacks its coherent ROM display response during the hold")


def _verify_switch_walks(compact: dict[str, Any], loaded: dict[str, dict[str, Any]], static: dict[str, dict[int, str]], errors: list[str]) -> None:
    variants = compact.get("per_variant")
    if not isinstance(variants, dict):
        errors.append("compact per_variant must be an object")
        return
    for tag in TAGS:
        run = loaded.get(f"runs/{tag}-switch-edges.json")
        if run is None or tag not in static:
            continue
        rows = _walk_rows(run, tag, static[tag], errors, "switch-edges")
        steps = run.get("steps")
        texts = [step.get("matched_text") for step in steps if isinstance(step, dict) and step.get("type") == "pulse_until_display"] if isinstance(steps, list) else []
        if texts != ["SWITCH EDGES"]:
            errors.append(f"{tag} switch-edges: expected only the SWITCH EDGES service checkpoint")
        variant = variants.get(tag)
        expected_rows = variant.get("switch_responses") if isinstance(variant, dict) else None
        if expected_rows is not None:
            if not isinstance(expected_rows, list) or len(expected_rows) != 88:
                errors.append(f"compact per_variant.{tag}.switch_responses must contain all 88 rows when present")
            else:
                expected_by_address = {item.get("host_address"): item for item in expected_rows if isinstance(item, dict)}
                for row in rows:
                    expected = expected_by_address.get(row["host_address"])
                    if not isinstance(expected, dict) or any(expected.get(key) != row[key] for key in row):
                        errors.append(f"compact per_variant.{tag}.switch_responses disagrees with raw switch {row['host_address']}")
    levels = loaded.get("runs/l2-switch-levels.json")
    if levels is not None and "l2" in static:
        _verify_levels(levels, static["l2"], errors)
        steps = levels.get("steps")
        texts = [step.get("matched_text") for step in steps if isinstance(step, dict) and step.get("type") == "pulse_until_display"] if isinstance(steps, list) else []
        if texts != ["SWITCH LEVELS"]:
            errors.append("l2 switch-levels: expected only the SWITCH LEVELS service checkpoint")


def _verify_coils(compact: dict[str, Any], root: Path, loaded: dict[str, dict[str, Any]], errors: list[str]) -> None:
    raw_order = _load_json(root / "coil-order.json", errors, "coil order")
    if raw_order is not None and compact.get("coil_order") != raw_order:
        errors.append("compact coil_order must exactly match retained coil-order.json")
    variants = compact.get("per_variant")
    if not isinstance(variants, dict):
        return
    for tag in TAGS:
        run = loaded.get(f"runs/{tag}-coil.json")
        variant = variants.get(tag)
        if run is None or not isinstance(variant, dict):
            continue
        events = run.get("events")
        seen = sorted({event.get("number") for event in events if isinstance(event, dict) and event.get("event") == "solenoid" and event.get("state") == 1 and isinstance(event.get("number"), int)}) if isinstance(events, list) else []
        if seen != list(COIL_OUTPUTS):
            errors.append(f"{tag} coil: expected coil walk outputs {list(COIL_OUTPUTS)}, got {seen}")
        if variant.get("coil_outputs_seen") != list(COIL_OUTPUTS):
            errors.append(f"compact per_variant.{tag}.coil_outputs_seen must be {list(COIL_OUTPUTS)}")
        steps = run.get("steps")
        texts = [step.get("matched_text") for step in steps if isinstance(step, dict) and step.get("type") == "pulse_until_display"] if isinstance(steps, list) else []
        if texts != ["COIL TEST"]:
            errors.append(f"{tag} coil: expected only the COIL TEST service checkpoint")
        order = compact.get("coil_order", {}).get(tag, {}).get("map", [])
        if {row.get("public_output") for row in order} != set(COIL_OUTPUTS) - {23} or len(order) != 30:
            errors.append(f"{tag} coil: named mapping must cover exactly the 30 physical service slots")
            continue
        snapshots = {item.get("label"): item for item in run.get("snapshots", [])}
        for row in order:
            matched = False
            for step in steps:
                label = step.get("label", "")
                snapshot = snapshots.get(label)
                if not label.startswith("coil observation") or snapshot is None:
                    continue
                if (_step_turns_on(step, row["public_output"])
                        and _snapshot_number(snapshot) == f'{row["rom_selector"]:02}'
                        and _normal(_snapshot_text(snapshot) or "") == _normal(row["name"])):
                    matched = True
                    break
            if not matched:
                errors.append(f'{tag} coil: output {row["public_output"]} lacks its named selector/display transition')


def _verify_gameplay(compact: dict[str, Any], loaded: dict[str, dict[str, Any]], errors: list[str]) -> None:
    variants = compact.get("per_variant")
    if not isinstance(variants, dict):
        return
    for tag in TAGS:
        run = loaded.get(f"runs/{tag}-gameplay-v2.json")
        variant = variants.get(tag)
        if run is None or not isinstance(variant, dict):
            continue
        run_label = f"{tag} gameplay-v2"
        if variant.get("gameplay_contract_passed") is not True:
            errors.append(f"compact per_variant.{tag}.gameplay_contract_passed must be true")
        levels = variant.get("drop_active_levels")
        if not isinstance(levels, dict) or set(levels) != {str(number) for number in DROP_RESETS}:
            errors.append(f"compact per_variant.{tag}.drop_active_levels must cover exactly {sorted(DROP_RESETS)}")
            levels = {}
        start_step = _step(run, "start game and prove ball release", errors, run_label)
        start_snapshot = _snapshot(run, "start game and prove ball release", errors, run_label)
        if start_step is not None and (not _step_turns_on(start_step, 2) or not _step_turns_on(start_step, 23)):
            errors.append(f"{run_label}: start must turn on ball release 2 and enable 23")
        if start_snapshot is not None and (active := _active_solenoids(start_snapshot)) is not None and 23 not in active:
            errors.append(f"{run_label}: start snapshot must retain enable 23")
        for switch, output in DROP_RESETS.items():
            expected = levels.get(str(switch))
            if not isinstance(expected, dict) or expected.get("rom_active_public_level") != 1 or expected.get("inactive_public_level") != 0 or expected.get("reset_output") != output or expected.get("inactive_stops_retries") is not True:
                errors.append(f"compact per_variant.{tag}: drop switch {switch} must be public1/reset {output}/public0-stop")
            down = _step(run, f"game drop bank switch{switch} down", errors, run_label)
            reset = _step(run, f"game drop bank switch{switch} reset modelled", errors, run_label)
            if down is not None and not _step_turns_on(down, output):
                errors.append(f"{run_label}: drop switch {switch} level1 did not turn on its reset output {output}")
            if reset is not None and _step_turns_on(reset, output):
                errors.append(f"{run_label}: drop switch {switch} level0 did not stop reset output {output}")
        for cabinet, (copied, outputs) in SYNTHETIC_FLIPPERS.items():
            overwritten = _snapshot(run, f"one-shot copied matrix{copied} write must be overwritten", errors, run_label)
            if overwritten is not None and _switch_state(overwritten, copied) != 0:
                errors.append(f"{run_label}: direct matrix {copied} write must be overwritten")
            for phase in ("attract", "game", "tilted"):
                snapshot = _snapshot(run, f"{phase} cabinet{cabinet} one-shot held", errors, run_label)
                if snapshot is None:
                    continue
                active = _active_solenoids(snapshot)
                if _switch_state(snapshot, copied) != 1:
                    errors.append(f"{run_label}: {phase} cabinet {cabinet} must copy to matrix {copied}")
                enabled = phase == "game"
                if active is None or (not set(outputs).issubset(active) if enabled else bool(set(outputs) & active)):
                    errors.append(f"{run_label}: {phase} cabinet {cabinet} synthetic outputs {outputs} have wrong hold state")
            held = _snapshot(run, f"game cabinet{cabinet} still held", errors, run_label)
            released = _snapshot(run, f"game cabinet{cabinet} release", errors, run_label)
            if held is not None and (active := _active_solenoids(held)) is not None and not set(outputs).issubset(active):
                errors.append(f"{run_label}: game cabinet {cabinet} must keep synthetic outputs {outputs} held")
            if released is not None and (active := _active_solenoids(released)) is not None and set(outputs) & active:
                errors.append(f"{run_label}: game cabinet {cabinet} release must clear synthetic outputs {outputs}")
        tilt = _snapshot(run, "after tilt game-on and flipper state", errors, run_label)
        next_ball = _snapshot(run, "postdrain next-ball observation", errors, run_label)
        if tilt is not None and (active := _active_solenoids(tilt)) is not None and 23 in active:
            errors.append(f"{run_label}: tilt must clear enable 23")
        if next_ball is not None and (active := _active_solenoids(next_ball)) is not None and 23 not in active:
            errors.append(f"{run_label}: next ball must restore enable 23")
        drain = _step(run, "ball drains outhole", errors, run_label)
        if drain is not None and not _step_turns_on(drain, 1):
            errors.append(f"{run_label}: drain must turn on outhole 1")


def verify(compact_path: Path, retained_root: Path) -> list[str]:
    """Return all deterministic verification failures; an empty list means success."""
    errors: list[str] = []
    compact = _load_json(compact_path, errors, "compact runtime evidence")
    if compact is None:
        return errors
    if not retained_root.is_dir():
        return [f"retained runtime root is missing: {retained_root}"]
    entries = _source_register_entries(compact, errors)
    _verify_source_register(retained_root, entries, errors)
    preflight = _load_json(retained_root / "preflight.json", errors, "retained preflight")
    if preflight is not None:
        if compact.get("source_revision") != preflight.get("source_revision"):
            errors.append("compact source_revision does not match retained preflight.json")
    loaded = _verify_run_inventory(compact, retained_root, errors)
    expected_library = compact.get("library_sha256")
    if not isinstance(expected_library, str):
        errors.append("compact library_sha256 must be a string")
    for relative, run in loaded.items():
        if run.get("library_sha256") != expected_library:
            errors.append(f"{relative}: library_sha256 does not match compact evidence")
    static = _static_switch_names(retained_root, errors)
    _verify_coils(compact, retained_root, loaded, errors)
    _verify_switch_walks(compact, loaded, static, errors)
    _verify_gameplay(compact, loaded, errors)
    return errors


def _default_retained_root() -> Path | None:
    configured = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT", "").strip()
    return Path(configured).resolve() / MACHINE_ID / "runtime-research" if configured else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify raw traces (the default action)")
    parser.add_argument("--compact", type=Path, default=Path(__file__).resolve().parents[1] / COMPACT_EVIDENCE, help="committed compact runtime evidence")
    parser.add_argument("--retained-root", type=Path, help="runtime-research directory; overrides PINMAME_REVIEW_ARTIFACTS_ROOT")
    args = parser.parse_args(argv)
    retained = args.retained_root.resolve() if args.retained_root else _default_retained_root()
    if retained is None:
        print("SKIP: PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
        return 0
    errors = verify(args.compact.resolve(), retained)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: Swords of Fury retained runtime verified ({retained})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
