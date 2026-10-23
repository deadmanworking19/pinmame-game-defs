"""Summarize the retained Space Station harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/williams.space-station.1987/harness/<run>/run.json`` (written by
``tools/run_pinmame_harness.py`` with the pinned library, each from a new state directory that inherits
only the retained initialization run's NVRAM), checks that every run succeeded on the pinned emulator
binary with an unchanged committed scenario, and writes
``evidence/runtime/system-11/space-station-l5-service-and-mechanisms.json``.

Display text is decoded from the raw sixteen-segment values of the two alphanumeric player displays
(controller indices 0 and 1, seven characters each), joined with a space: the low fifteen bits are the
glyph and bit 15 is the period; the ROM draws the numeral 1 as 0x0006 and uses one glyph for 0 and O and
one for 5 and S, which the decoder writes as O and S. The numeric player 3 display (index 2, seven-segment)
carries the test and step numbers. A Coil Test step is the alphanumeric text when the step's output rises;
a Single Lamps step is the text shown longest between two Credit presses; a Switch Levels step is the
snapshot taken while the address is held. Every number written is recomputed from the raw runs, and
``--check`` refuses any drift.

    python tools/space_station_runtime_evidence.py            # write
    python tools/space_station_runtime_evidence.py --check    # re-derive and compare, write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402
from run_pinmame_harness import SEGMENT_16_CHARACTERS  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
MACHINE_ID = "williams.space-station.1987"
GAME = "spstn_l5"
ROM_ARCHIVE_SHA256 = "8c5cdaf5a8e6a4b112873f17c6a66ca34de6ac15eb830474965cdfa035434f7c"
SCENARIO_DIRECTORY = "tools/harness-scenarios/system-11"
EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/space-station-l5-service-and-mechanisms.json"
HARNESS_RELATIVE = Path("williams.space-station.1987/harness")
SOURCE_PATH = "external:pinmame-review-artifacts/williams.space-station.1987/harness"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (each "
	"run's run.json, copied scenario.json, stdout and stderr logs, and every state-directory file including the inherited "
	"and written NVRAM) except manifest.json and manifest.sha256, sorted by POSIX relative path. "
	"tools/build_external_evidence_manifest.py writes and re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game spstn_l5 --rom-path <vpinmame-roms> "
	"--work-dir <run>/state --scenario tools/harness-scenarios/system-11/spstn-<run>.json --boot-wait 0 --output "
	"<run>/run.json. The initialization run (spstn-nvram-init.json) starts from an empty state directory and stops on "
	"FACTORY SETTING; every other run starts from a new state directory holding only that run's nvram/spstn_l5.nv. "
	"Diagnostic scenarios wait 8 s, set Manual-Down (-6 = 0), pulse Advance (-7) to enter the tests, set Auto-Up (-6 = 1) "
	"and pulse Advance until the checkpoint text is displayed."
)
INIT_RUN = "nvram-init"
RUN_NAMES = (
	"nvram-init", "coil-test", "single-lamps", "switch-levels",
	"boot-baseline", "boot-outhole-10", "boot-trough-11-13", "boot-poppers-41-42", "boot-shooter-43",
	"boot-locks-45-47", "boot-lock-45", "boot-lock-47", "boot-drop-33", "boot-drops-57-59",
	"boot-station-52", "boot-station-53", "boot-station-52-53", "station-reactive-ccw", "station-reactive-cw",
	"gameplay",
)
STATIC_LIMITATION = (
	"Static host switches only; the harness never moves a ball or a mechanism, so repeated pulses are ROM retries against a "
	"host-held switch."
)
SCRIPTED_LIMITATION = (
	"The host answers the ROM's drives with fixed, scripted switch changes; a pulse the ROM fires proves only that the address "
	"changed under these conditions, not a mechanism's travel time or the physical device's identity."
)
REACTIVE_LIMITATION = (
	"The position pattern is a synthetic host model written on a fixed schedule, not a measurement of the physical cam; the "
	"run shows only at which modelled pattern the ROM released the motor relay."
)
ROM_GLYPHS = {0x0006: "1"}
# The attract-mode G.I. relays, the A/C relay, the flasher bank and the panel flashers repeat for as long as the game is
# idle and say nothing about the probed device.
ATTRACT_BACKGROUND = {9, 10, 11, 12, 15, 25, 26, 27, 28, 29, 30, 31}
SEGMENT_7 = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}


def working_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is required: the raw runs live under the working root's review-artifacts")
	return Path(value).expanduser().resolve()


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_alpha(values: list[int]) -> str:
	text = []
	for value in values:
		glyph = ROM_GLYPHS.get(value & 0x7FFF, SEGMENT_16_CHARACTERS.get(value & 0x7FFF))
		text.append(("?" if value & 0x7FFF else " ") if glyph is None else glyph)
		if value & 0x8000:
			text.append(".")
	return "".join(text)


def decode_numeric(values: list[int]) -> str:
	return "".join(SEGMENT_7.get(value & 0x7F, "?") for value in values)


def normalized(text: str) -> str:
	return " ".join(text.split())


def glyph_folded(text: str) -> str:
	"""A name as this ROM's font draws it: 0 and O, and 5 and S, share a glyph."""
	return text.replace("0", "O").replace("5", "S")


def run_dir(harness: Path, name: str) -> Path:
	return harness / name


def load_run(harness: Path, name: str) -> dict[str, Any]:
	run = json.loads((run_dir(harness, name) / "run.json").read_text(encoding="utf-8"))
	if run.get("failure") is not None or run.get("game") != GAME:
		raise RuntimeError(f"{name}: not a successful {GAME} run")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise RuntimeError(f"{name}: not produced by the pinned library")
	scenario = ROOT / SCENARIO_DIRECTORY / f"spstn-{name}.json"
	if run["scenario"]["sha256"] != sha256(scenario):
		raise RuntimeError(f"{name}: scenario drift against {scenario}")
	if sha256(run_dir(harness, name) / "scenario.json") != sha256(scenario):
		raise RuntimeError(f"{name}: the retained scenario copy differs from {scenario}")
	return run


def alpha_timeline(run: dict[str, Any]) -> list[tuple[float, str]]:
	rows = {0: "", 1: ""}
	timeline = []
	for event in run["events"]:
		if event["event"] == "display" and event.get("index") in rows and isinstance(event.get("segments"), list):
			rows[event["index"]] = decode_alpha(event["segments"])
			timeline.append((event["time_s"], normalized(rows[0] + " " + rows[1])))
	return timeline


def text_at(timeline: list[tuple[float, str]], time: float) -> str:
	current = ""
	for at, text in timeline:
		if at > time:
			break
		current = text
	return current


def longest_text(timeline: list[tuple[float, str]], start: float, end: float) -> str:
	durations: dict[str, float] = {}
	current = text_at(timeline, start)
	at = start
	for when, text in timeline:
		if when <= start:
			continue
		if when >= end:
			break
		durations[current] = durations.get(current, 0.0) + (when - at)
		current, at = text, when
	durations[current] = durations.get(current, 0.0) + (end - at)
	return max(sorted(durations), key=lambda text: durations[text])


def solenoid_spans(run: dict[str, Any]) -> dict[int, list[tuple[float, float | None]]]:
	open_at: dict[int, float] = {}
	spans: dict[int, list[tuple[float, float | None]]] = {}
	for event in run["events"]:
		if event["event"] != "solenoid":
			continue
		number, time = event["number"], round(event["time_s"], 3)
		if event["state"]:
			open_at.setdefault(number, time)
		elif number in open_at:
			spans.setdefault(number, []).append((open_at.pop(number), time))
	for number, time in open_at.items():
		spans.setdefault(number, []).append((time, None))
	return spans


def describe_spans(spans: dict[int, list[tuple[float, float | None]]], end: float, skip: set[int] = ATTRACT_BACKGROUND) -> str:
	parts = []
	for number in sorted(spans):
		if number in skip:
			continue
		items = spans[number]
		if len(items) <= 3:
			parts.append(f"{number}: " + ", ".join(f"{a}-{'end' if b is None else b} s" for a, b in items))
		else:
			gaps = [round(items[i + 1][0] - items[i][0], 2) for i in range(len(items) - 1)]
			parts.append(f"{number}: {len(items)} pulses from {items[0][0]} s to {items[-1][0]} s, spacing {min(gaps)}-{max(gaps)} s")
	return "; ".join(parts) + f" (observed to {end} s)"


def end_time(run: dict[str, Any]) -> float:
	return round(max(event["time_s"] for event in run["events"]), 3)


def service_pulses(run: dict[str, Any]) -> int:
	total = 0
	for step in run["steps"]:
		if step.get("type") == "pulse" and step.get("switch") == -7:
			total += 1
		elif step.get("type") == "pulse_until_display" and step.get("switch") == -7:
			total += step["pulses"]
	return total


def checkpoints(run: dict[str, Any]) -> list[dict[str, Any]]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
	        for step in run["steps"] if step.get("type") == "pulse_until_display"]


def coil_test(run: dict[str, Any]) -> list[dict[str, Any]]:
	"""Each coil-test step: the address that rises and the display text then, for two complete cycles."""
	timeline = alpha_timeline(run)
	begin = next(at for at, text in timeline if text == "COIL TEST")
	steps = []
	for event in run["events"]:
		if event["event"] != "solenoid" or not event["state"] or event["time_s"] <= begin or event["number"] == 23:
			continue
		text = text_at(timeline, event["time_s"])
		# The A/C select relay (12) is energized ahead of the C-side steps; it is a step of its own only where the ROM names it.
		if event["number"] == 12 and text != "AC SELECT":
			continue
		steps.append({"address": event["number"], "display": text, "time_s": round(event["time_s"], 3)})
	period = next(index for index in range(1, len(steps)) if steps[index]["address"] == steps[0]["address"] and index > 2)
	first, second = steps[:period], steps[period:2 * period]
	if [step["address"] for step in first] != [step["address"] for step in second]:
		raise RuntimeError("coil test second cycle differs from the first")
	if [step["display"] for step in first] != [step["display"] for step in second]:
		raise RuntimeError("coil test second cycle names differ from the first")
	return [{"step": index, "address": step["address"], "display": step["display"]} for index, step in enumerate(first, start=1)]


def relay_held(run: dict[str, Any], steps: list[dict[str, Any]]) -> list[int]:
	"""Addresses whose coil-test pulse falls inside an energized span of the A/C relay (12)."""
	timeline = alpha_timeline(run)
	begin = next(at for at, text in timeline if text == "COIL TEST")
	relay = solenoid_spans(run).get(12, [])
	held = []
	rises = [(event["time_s"], event["number"]) for event in run["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] > begin]
	for step in steps:
		time = next(t for t, n in rises if n == step["address"])
		if step["address"] != 12 and any(a <= time and (b is None or time < b) for a, b in relay):
			held.append(step["address"])
	if held != list(range(25, 33)):
		raise RuntimeError(f"the A/C relay was held for {held}, not exactly the C-side bank 25-32")
	if not any(step["address"] == 12 and step["display"] == "AC SELECT" for step in steps):
		raise RuntimeError("the coil test has no AC SELECT step of its own")
	return held


def single_lamps(run: dict[str, Any]) -> list[dict[str, Any]]:
	timeline = alpha_timeline(run)
	presses = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event.get("number") == 3 and event.get("state") == 1]
	steps = [step for step in run["steps"] if step.get("label", "").startswith(("Credit: step to designator", "first lamp"))]
	title = next(at for at, text in timeline if text == "SINGLE LAMPS")
	# The first lamp's window starts when the test title gives way to the first lamp name.
	begin = next(at for at, text in timeline if at > title and text != "SINGLE LAMPS")
	bounds = [begin] + presses + [end_time(run)]
	pairs = []
	for index, step in enumerate(steps):
		designator = 1 if step["label"].startswith("first lamp") else int(step["label"].rsplit(" ", 1)[1])
		start, end = bounds[index] + 0.3, bounds[index + 1]
		blinked = sorted({event["number"] for event in run["events"] if event["event"] == "lamp" and start <= event["time_s"] < end})
		if blinked != [designator]:
			raise RuntimeError(f"single lamps designator {designator} blinked {blinked}")
		pairs.append({"designator": designator, "address": designator, "display": longest_text(timeline, start, end)})
	if [pair["designator"] for pair in pairs] != list(range(1, 65)):
		raise RuntimeError("single lamps did not step through designators 01-64")
	return pairs


def switch_levels(run: dict[str, Any]) -> list[dict[str, Any]]:
	results = []
	for step in run["steps"]:
		label = step.get("label", "")
		if not label.startswith("hold public switch"):
			continue
		address = int(label.rsplit(" ", 1)[1])
		snapshot = next(item for item in run["snapshots"] if item.get("label") == label + " (held)")
		displays = {display["index"]: display for display in snapshot["displays"]}
		name = normalized(decode_alpha(displays[0]["segments"]) + " " + decode_alpha(displays[1]["segments"]))
		number = normalized(decode_numeric(displays[2]["segments"]))
		results.append({"address": address, "name": name, "number": number, "solenoids": sorted(snapshot["active_solenoids"])})
	return results


def boot_note(run: dict[str, Any]) -> str:
	holds = ", ".join(f"{item['switch']}={item['state']}" for item in run["initial_switches"])
	return f"Power-up probe with switches {holds} held from emulator start. Solenoid on-spans: {describe_spans(solenoid_spans(run), end_time(run))}."


def station_note(run: dict[str, Any]) -> str:
	"""The modelled (52, 53) pattern and every motor-relay (16) transition, in time order."""
	pattern = {52: 0, 53: 0}
	items = []
	for event in run["events"]:
		if event["event"] == "switch" and event.get("number") in (52, 53):
			pattern[event["number"]] = event["state"]
			items.append((event["time_s"], f"(52,53)=({pattern[52]},{pattern[53]})"))
		elif event["event"] == "solenoid" and event["number"] == 16:
			items.append((event["time_s"], f"16={event['state']}"))
	compact = []
	for time, text in items:
		if compact and compact[-1][1] == text:
			continue
		compact.append((time, text))
	return "Motor relay (16) against the modelled position pattern: " + "; ".join(f"{round(t, 3)} s {text}" for t, text in compact) + f" (observed to {end_time(run)} s)."


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def raw_entry(harness: Path, name: str, run: dict[str, Any]) -> dict[str, Any]:
	init_nv = sha256(run_dir(harness, INIT_RUN) / "state" / "nvram" / f"{GAME}.nv")
	entry: dict[str, Any] = {
		"name": name,
		"sha256": sha256(run_dir(harness, name) / "run.json"),
		"scenario_path": f"{SCENARIO_DIRECTORY}/spstn-{name}.json",
		"scenario_sha256": run["scenario"]["sha256"],
		"action_count": run["scenario"]["action_count"],
		"watch_switches": run["watch_switches"],
		"self_test_pulses": service_pulses(run),
		"boot_wait_s": 0,
		"snapshot_count": len(run["snapshots"]),
		"nvram_initialization": (
			f"Fresh empty state directory; this is the one retained {GAME} initialization run (FACTORY SETTING), whose "
			f"nvram/{GAME}.nv is the only state any later run inherits."
			if name == INIT_RUN
			else f"Fresh state directory holding only nvram/{GAME}.nv (SHA-256 {init_nv}) from the retained initialization run."
		),
	}
	if run["initial_switches"]:
		entry["initial_switches"] = [{"switch": item["switch"], "state": item["state"]} for item in run["initial_switches"]]
	return entry


def service_observations(run: dict[str, Any], name: str) -> tuple[dict[str, Any], dict[str, int]]:
	spans = solenoid_spans(run)
	observation: dict[str, Any] = {"solenoid_addresses_seen": sorted(spans), "diagnostic_checkpoints": checkpoints(run)}
	named: dict[str, int] = {}
	if name == "coil-test":
		steps = coil_test(run)
		held = relay_held(run, steps)
		for step in steps:
			named[f"coil-{step['step']:02d}-{slug(step['display'])}"] = step["address"]
		observation.update({
			"ordered_solenoid_on_sequence": [step["address"] for step in steps],
			"note": (
				f"Advance walk to COIL TEST (player 3 display 05), then two identical cycles of {len(steps)} named steps. "
				"Step:address = player 1 and 2 displays: " + "; ".join(f"{s['step']}:{s['address']} = {s['display']}" for s in steps)
				+ f". The A/C select relay (12) is energized before and held through each step that pulses {', '.join(map(str, held))}, "
				"pulsed by itself in its own AC SELECT step, and released for every other step. No step pulses 5 or 14."
			),
			"limitation": "A pulsed address is ROM activity, not proof that a load is fitted.",
		})
		return observation, named
	if name == "single-lamps":
		pairs = single_lamps(run)
		for pair in pairs:
			named[f"lamp-{pair['designator']:02d}-{slug(pair['display'])}"] = pair["address"]
		observation.update({
			"note": (
				"Advance walk to SINGLE LAMPS (player 3 display 04); each Credit press (public 3) steps the designator, and designator "
				"n blinks public lamp n alone for every n from 1 to 64. Designator = player 1 and 2 displays: "
				+ "; ".join(f"{p['designator']} = {p['display']}" for p in pairs) + "."
			),
		})
		return observation, named
	results = switch_levels(run)
	observation.update({
		"note": (
			"Advance walk to SWITCH LEVELS (player 3 display 06); each public address 1-64 and 81-88 held at 1 alone for 1.5 s. "
			"Address = player 1 and 2 displays / player 3 display [active solenoids] while held: "
			+ "; ".join(f"{r['address']} = {r['name'] or '(blank)'} / {r['number']} {r['solenoids']}" for r in results) + "."
		),
		"limitation": (
			"Host-held levels written on every poll; a name shown while public n is held at 1 means the ROM reads that address as "
			"active at 1. A held pulse also rewrites the FLIP_SWNO targets 55 and 56 on every poll, masking core_updateSw's copy."
		),
	})
	return observation, named


def build(review_root: Path) -> tuple[bytes, dict[str, Any]]:
	harness = review_root / HARNESS_RELATIVE
	manifest_bytes = (json.dumps(manifests.build_manifest(harness, GAME), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
	raw_runs, observations = [], {}
	seen: set[int] = set()
	named: dict[str, int] = {}
	for name in RUN_NAMES:
		run = load_run(harness, name)
		raw_runs.append(raw_entry(harness, name, run))
		spans = solenoid_spans(run)
		seen.update(spans)
		if name in ("coil-test", "single-lamps", "switch-levels"):
			observation, run_named = service_observations(run, name)
			named.update(run_named)
		elif name == INIT_RUN:
			observation = {
				"solenoid_addresses_seen": sorted(spans),
				"note": f"Boot to FACTORY SETTING from an empty state directory; the NVRAM written on stop is the only state later {GAME} runs inherit.",
			}
		elif name.startswith("station-reactive"):
			observation = {"solenoid_addresses_seen": sorted(spans), "note": station_note(run), "limitation": REACTIVE_LIMITATION}
		elif name.startswith("boot-"):
			note = boot_note(run)
			if name.startswith("boot-station"):
				note += " " + station_note(run)
			observation = {"solenoid_addresses_seen": sorted(spans), "note": note, "limitation": STATIC_LIMITATION}
		else:
			observation = {
				"solenoid_addresses_seen": sorted(spans),
				"diagnostic_checkpoints": checkpoints(run),
				"note": f"Scripted scenario ({run['scenario']['action_count']} actions, see the scenario notes). Solenoid on-spans: {describe_spans(spans, end_time(run))}.",
				"limitation": SCRIPTED_LIMITATION,
			}
		observations[name] = observation
	evidence = {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "space-station-harness-runs", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": SOURCE_PATH,
			"sha256": hashlib.sha256(manifest_bytes).hexdigest(),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external.",
			"quality": "observed",
			"manifest_algorithm": MANIFEST_ALGORITHM,
		},
		"driver_ids": [GAME],
		"machine_ids": [MACHINE_ID],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": GAME,
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"raw_runs": raw_runs,
			"command_template": COMMAND_TEMPLATE,
			"observations": {
				"service_language": "English",
				"solenoid_addresses_seen": sorted(seen),
				"named_output_addresses": named,
				"runs": observations,
			},
		},
	}
	return manifest_bytes, evidence


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	review_root = working_root()
	harness = review_root / HARNESS_RELATIVE
	manifest_bytes, evidence = build(review_root)
	if args.check:
		if (harness / "manifest.json").read_bytes() != manifest_bytes:
			raise SystemExit(f"{harness / 'manifest.json'} does not match the files beside it")
		manifests.check_manifest(harness, GAME)
		if EVIDENCE_PATH.read_bytes() != canonical_bytes(evidence):
			raise SystemExit(f"{EVIDENCE_PATH} is not the summary of the raw runs in {harness}")
		print("Space Station runtime evidence and manifest match the raw runs.")
		return
	manifests.write_manifest(harness, GAME)
	EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
	EVIDENCE_PATH.write_bytes(canonical_bytes(evidence))
	print(f"wrote {EVIDENCE_PATH}")


if __name__ == "__main__":
	main()
