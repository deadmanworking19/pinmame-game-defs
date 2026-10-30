"""Summarize the retained Gladiators harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/gottlieb.gladiators.1993/runtime/`` (written by ``tools/run_pinmame_harness.py`` with the
pinned library: the ``nvram-init`` run from an empty state directory, every other run from a new state
directory holding only that run's initialized NVRAM), checks that every run succeeded on the pinned emulator
binary with an unchanged committed scenario, reads the DMD text of every snapshot with
``tools/gts3_dmd_text.py`` and writes ``evidence/runtime/gts3/gladiators-gladiatr-service-tests.json``: the
Lamp Matrix and Relay & Solenoid tests and the Switch Matrix Test that follows the Inoperative Switches list,
each step paired with the public address it drove or the host held, plus the Front Door Test, a
tournament/coin-door probe, one scripted game and a ramp-motor probe.

A Lamp Matrix step pairs the displayed ``LAMP:nn`` with the one lamp that blinked during the step; a Relay &
Solenoid step pairs the displayed driver with the output its credit-button press fired; a Switch Matrix step
reads the frame taken while the host held the address at 1. A pairing that disagrees with the expected
arithmetic stops the build. ``--check`` re-derives everything and refuses any drift.

    python tools/gladiators_runtime_evidence.py            # write
    python tools/gladiators_runtime_evidence.py --check    # re-derive and compare, write nothing
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

import gts3_dmd_text  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
MACHINE_ID = "gottlieb.gladiators.1993"
GAME = "gladiatr"
ROM_ARCHIVE_SHA256 = "97a90dcafabd3207d8242a0712e651cc6205dff547b0c83a7fd35ffa74243a43"
SCENARIO_DIRECTORY = "tools/harness-scenarios/gts3"
# The power-up frame's lines, read from the retained frame by eye; the third is in a font the glyph table does not cover.
BOOT_SCREEN = "GLADIATORS / (Install 4 Balls) / Game #737, ID #000000 / GPROM CHECKSUM-FC59"
RUNS = ("nvram-init", "lamp-matrix", "solenoids", "switch-matrix", "front-door", "tournament-door", "gameplay", "mechanism-sensors")
RUNTIME_RELATIVE = Path("gottlieb.gladiators.1993/runtime")
SOURCE_PATH = "external:pinmame-review-artifacts/gottlieb.gladiators.1993/runtime"
EVIDENCE_PATH = ROOT / "evidence/runtime/gts3/gladiators-gladiatr-service-tests.json"
MANIFEST_GAME = GAME
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (the raw "
	"run JSON and log of every run, every saved DMD frame, and every state-directory file including the inherited and written "
	"NVRAM) except manifest.json and manifest.sha256, sorted by POSIX relative path. tools/build_external_evidence_manifest.py "
	"writes and re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game gladiatr --rom-path <vpinmame-roms> "
	"--work-dir <state-directory> --scenario tools/harness-scenarios/gts3/gladiators-<name>.json --dmd-dir <frames> "
	"--output <external-run.json>. The nvram-init run starts from an empty state directory (state-init-gladiatr) and loads "
	"factory settings; every other run starts from a new state directory (states/gladiatr-<name>) holding only that NVRAM. "
	"Every scenario sets switch_converter gts3, so the harness checks PINMAME_HARDWARE_GEN_GTS3 before touching a switch."
)
FLIPPER_SYNTHETIC = {45, 46, 47, 48}
SERVICE_LIMITATION = "A pulsed address is ROM activity, not proof that a load is fitted."
SWITCH_LIMITATION = (
	"The Switch Matrix Test names the switch the ROM sees closed, so a name shown while the host holds an address at 1 proves "
	"that the ROM scans that address under that name and reads 1 as closed; it does not show how the contact is built."
)
STATIC_LIMITATION = (
	"The host answers the ROM with fixed, scripted switch changes; it never moves a ball or a mechanism, so a pulse the ROM "
	"fires proves only that the address changed under these conditions."
)


def working_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is required: the raw runs live under the working root's review-artifacts")
	return Path(value).expanduser().resolve()


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def fold(text: str) -> str:
	"""Repeat the decoder's O/0 fold until it is stable, so a run of two such glyphs next to a digit reads 00, not 0O."""
	previous = None
	while previous != text:
		previous, text = text, re.sub(r"(?<=\d)O|O(?=\d)", "0", text)
	return text


class Run:
	def __init__(self, runtime: Path, name: str, glyphs: dict[str, str]) -> None:
		self.name = name
		self.path = runtime / "runs" / f"{GAME}-{name}.json"
		self.data = json.loads(self.path.read_text(encoding="utf-8"))
		self.scenario_path = f"{SCENARIO_DIRECTORY}/gladiators-{name}.json"
		scenario_bytes = (ROOT / self.scenario_path).read_bytes()
		if self.data.get("failure"):
			raise RuntimeError(f"{self.path.name}: the run failed: {self.data['failure']}")
		if self.data.get("library_sha256") != LIBRARY_SHA256:
			raise RuntimeError(f"{self.path.name}: not recorded on the pinned library")
		if self.data.get("game") != GAME:
			raise RuntimeError(f"{self.path.name}: recorded for {self.data.get('game')!r}")
		if self.data["scenario"]["sha256"] != hashlib.sha256(scenario_bytes).hexdigest():
			raise RuntimeError(f"{self.path.name}: the committed scenario changed since the run")
		if self.data.get("switch_converter") != "gts3":
			raise RuntimeError(f"{self.path.name}: not run with the gts3 switch converter")
		self.frames = runtime / "dmd" / f"{GAME}-{name}"
		self.text: dict[int, list[str]] = {}
		self.held_text: dict[int, list[str]] = {}
		for index, snapshot in enumerate(self.data["snapshots"]):
			displays = snapshot.get("displays") or []
			if len(displays) != 1:
				raise RuntimeError(f"{self.path.name}: snapshot {index} has {len(displays)} displays")
			frame = self.frames / Path(displays[0]["artifact"]).name
			if not frame.is_file():
				raise RuntimeError(f"{self.path.name}: retained frame missing: {frame}")
			lines = [fold(line) for line in gts3_dmd_text.decode(frame.read_bytes(), glyphs)]
			if snapshot["label"].endswith(" (held)"):
				self.held_text[index] = lines
			else:
				self.text[index] = lines
		# Snapshot 0 is the boot snapshot; step n's settle snapshot follows it, and a step with a
		# held snapshot adds one more just before. Pair them by label in order.
		self.step_text: dict[int, list[str]] = {}
		self.step_held_text: dict[int, list[str]] = {}
		snapshots = self.data["snapshots"]
		cursor = 1
		for step in self.data["steps"]:
			if cursor < len(snapshots) and snapshots[cursor]["label"] == f"{step['label']} (held)":
				self.step_held_text[step["step"]] = self.held_text[cursor]
				cursor += 1
			if cursor >= len(snapshots) or snapshots[cursor]["label"] != step["label"]:
				raise RuntimeError(f"{self.path.name}: no settle snapshot for step {step['step']} ({step['label']})")
			self.step_text[step["step"]] = self.text[cursor]
			cursor += 1

	def raw_record(self, nvram_note: str) -> dict[str, Any]:
		scenario = json.loads((ROOT / self.scenario_path).read_text(encoding="utf-8"))
		record: dict[str, Any] = {
			"name": self.name,
			"sha256": sha256(self.path),
			"scenario_path": self.scenario_path,
			"scenario_sha256": self.data["scenario"]["sha256"],
			"action_count": len(scenario["actions"]),
			"self_test_pulses": sum(1 for action in scenario["actions"] if action.get("switch") == -8),
			"nvram_initialization": nvram_note,
			"snapshot_count": len(self.data["snapshots"]),
			"watch_switches": self.data["watch_switches"],
		}
		if self.data.get("initial_switches"):
			record["initial_switches"] = self.data["initial_switches"]
		return record

	def solenoid_events(self, numbers: set[int]) -> list[tuple[int, int, float]]:
		return [
			(event["number"], event["state"], event["time_s"]) for event in self.data["events"]
			if event.get("event") == "solenoid" and event["number"] in numbers
		]


def solenoids_on(step: dict[str, Any]) -> list[int]:
	return sorted(item["number"] for item in step["transitions"]["solenoids"] if 1 in item["states"])


def blinking_lamps(step: dict[str, Any], minimum: int = 3) -> list[int]:
	return sorted(item["number"] for item in step["transitions"]["lamps"] if len(item["states"]) >= minimum)


def lamp_matrix(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	for step in run.data["steps"]:
		if not step["label"].startswith("right flipper: lamp step") and step["label"] != "lamp 00 settle":
			continue
		found = gts3_dmd_text.labelled(run.step_text[step["step"]], "LAMP")
		if found is None:
			raise RuntimeError(f"{run.path.name}: step {step['step']} shows no LAMP number")
		number, name = found
		blinking = blinking_lamps(step)
		if blinking != [number]:
			raise RuntimeError(f"{run.path.name}: LAMP:{number} blinked {blinking}")
		if number in names and names[number] != name:
			raise RuntimeError(f"{run.path.name}: LAMP:{number} named {names[number]!r} and {name!r}")
		names[number] = name
	expected = [column * 10 + row for column in range(12) for row in range(8)]
	if sorted(names) != expected:
		raise RuntimeError(f"{run.path.name}: the walk did not cover every lamp: {sorted(set(expected) - set(names))}")
	observation = {
		"diagnostic_checkpoints": [{"after_service_pulses": 4, "matched_text": "LAMP MATRIX TEST"}],
		"limitation": SERVICE_LIMITATION,
		"note": (
			"Self-test 3 stepped forward with the right flipper; after LAMP:B7 the walk wraps to LAMP:00. In every step exactly one "
			"public lamp blinked (three or more state changes) and it was the displayed LAMP number, A0-B7 meaning 100-117. "
			"Address = name: " + "; ".join(f"{number} = {names[number]}" for number in expected) + "."
		),
	}
	return names, observation


def solenoid_test(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	addresses: dict[int, int] = {}
	extras: dict[int, list[int]] = {}
	sequence: list[int] = []
	for step in run.data["steps"]:
		if not step["label"].startswith("start: fire solenoid"):
			continue
		found = gts3_dmd_text.labelled(run.step_text[step["step"]], "SOLENOID")
		if found is None:
			raise RuntimeError(f"{run.path.name}: step {step['step']} shows no SOLENOID number")
		number, name = found
		fired = [address for address in solenoids_on(step) if address not in FLIPPER_SYNTHETIC]
		target = number + 1
		if target not in fired:
			raise RuntimeError(f"{run.path.name}: SOLENOID:{number} fired {fired}, not {target}")
		if number in names and names[number] != name:
			raise RuntimeError(f"{run.path.name}: SOLENOID:{number} named {names[number]!r} and {name!r}")
		names[number] = name
		addresses[number] = target
		others = [address for address in fired if address != target]
		if others:
			extras[number] = others
		sequence.append(target)
	if sorted(names) != list(range(32)):
		raise RuntimeError(f"{run.path.name}: the walk did not cover drivers 0-31")
	note = (
		"Self-test 4: the right flipper steps the displayed SOLENOID number and the credit button fires it; the solenoid that "
		"rose on each press is the displayed number plus 1. Solenoid = public solenoid: name: "
		+ "; ".join(f"{number} = {addresses[number]}: {names[number]}" for number in sorted(names))
		+ "."
	)
	if extras:
		note += " Also rising during the press: " + "; ".join(
			f"Solenoid {number}: {', '.join(str(address) for address in others)}" for number, others in sorted(extras.items())
		) + "."
	observation: dict[str, Any] = {
		"limitation": SERVICE_LIMITATION,
		"note": note,
		"ordered_solenoid_on_sequence": sequence,
		"solenoid_addresses_seen": sorted(set(sequence) | {address for others in extras.values() for address in others}),
	}
	return names, observation


def switch_matrix(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	silent: list[int] = []
	texts: dict[int, list[str]] = {}
	idle = None
	for step in run.data["steps"]:
		if step["label"].startswith("inoperative switch list finishes"):
			idle = " / ".join(run.step_text[step["step"]])
		match = re.fullmatch(r"close switch (-?\d+)(?: through flipper button (141|143))?", step["label"])
		if not match:
			continue
		address = int(match.group(1))
		texts[address] = [line for line in run.step_held_text[step["step"]] if "?" not in line]
		found = gts3_dmd_text.labelled(run.step_held_text[step["step"]], "SWITCH")
		if found is None:
			silent.append(address)
			continue
		number, name = found
		if number != address:
			if address >= 0:
				raise RuntimeError(f"{run.path.name}: holding {address} showed SWITCH:{number}")
			silent.append(address)
			continue
		names[address] = name
	if idle != "SELF-TEST 5 / SWITCH MATRIX TEST / ALL SWITCHES OPEN":
		raise RuntimeError(f"{run.path.name}: the Switch Matrix Test was not idle before the walk: {idle!r}")
	note = (
		"Self-test 5 lists the Inoperative Switches by itself and then shows SWITCH MATRIX TEST / ALL SWITCHES OPEN (the frame "
		"before the walk). With each address held at 1 alone for 400 ms (82 and 83 through the flipper buttons 143 and 141 that "
		"core_updateSw copies into them), the frame taken while held shows SWITCH:nn (A0-B7 meaning 100-117) and the ROM's "
		"name, and nn was the held address every time. Address = name: "
		+ "; ".join(f"{address} = {names[address]}" for address in sorted(names))
		+ "."
	)
	if silent:
		note += (
			" No SWITCH line of its own while held: "
			+ ", ".join(f"{address} (\"{' / '.join(texts[address])}\")" for address in silent) + "."
		)
	return names, {"limitation": SWITCH_LIMITATION, "note": note, "switch_addresses_observed_while_held": sorted(names)}


def step_notes(run: Run) -> list[str]:
	notes = []
	for step in run.data["steps"]:
		on = [address for address in solenoids_on(step) if address not in FLIPPER_SYNTHETIC]
		synthetic = [address for address in solenoids_on(step) if address in FLIPPER_SYNTHETIC]
		text = " / ".join(line for line in run.step_text[step["step"]] if "?" not in line)
		part = f"{step['step']} {step['label']}: solenoids rising {on or 'none'}"
		if synthetic:
			part += f", synthetic flipper outputs {synthetic}"
		if text:
			part += f"; display \"{text}\""
		notes.append(part)
	return notes


def scripted(run: Run, summary: str, timed: set[int] | None = None) -> dict[str, Any]:
	seen = sorted({address for step in run.data["steps"] for address in solenoids_on(step)})
	observation = {"limitation": STATIC_LIMITATION, "note": summary + " Steps: " + "; ".join(step_notes(run)) + ".", "solenoid_addresses_seen": seen}
	if timed:
		events = ", ".join(f"{number} {'on' if state else 'off'} at {time} s" for number, state, time in run.solenoid_events(timed))
		observation["note"] += f" Solenoid edges of {sorted(timed)}, timed from the start of the run: {events}."
	return observation


def front_door(run: Run) -> dict[str, Any]:
	counts = []
	for step in run.data["steps"]:
		lines = run.step_held_text.get(step["step"]) or run.step_text[step["step"]]
		counts.append(f"{step['label']}: \"{' / '.join(lines)}\"")
	return {"limitation": STATIC_LIMITATION, "note": "Self-test 8; display after each step: " + "; ".join(counts) + "."}


def build(root: Path) -> dict[str, Any]:
	runtime = root / RUNTIME_RELATIVE
	glyphs = gts3_dmd_text.load_glyphs()
	manifest_sha = manifests.check_manifest(runtime, MANIFEST_GAME)
	if manifest_sha != sha256(runtime / "manifest.json"):
		raise RuntimeError("the retained manifest digest does not match manifest.json")
	runs = {name: Run(runtime, name, glyphs) for name in RUNS}
	init_nv = runtime / f"state-init-{GAME}" / "nvram" / f"{GAME}.nv"
	init_note = f"Fresh state directory holding only nvram/{GAME}.nv (SHA-256 {sha256(init_nv)}) from the nvram-init run."
	raw = [runs["nvram-init"].raw_record(f"Empty state directory state-init-{GAME}; this run loads factory settings and its NVRAM is the only state any later run inherits.")]
	raw += [runs[name].raw_record(init_note) for name in RUNS[1:]]
	observations: dict[str, Any] = {}
	init_texts = [" / ".join(line for line in run_text if "?" not in line) for run_text in runs["nvram-init"].step_text.values()]
	init_texts = [text for text in init_texts if text]
	observations["nvram-init"] = {
		"limitation": STATIC_LIMITATION,
		"note": (
			f"The power-up frame (pixel SHA-256 {runs['nvram-init'].data['snapshots'][0]['displays'][0]['pixel_sha256']}) "
			f"reads {BOOT_SCREEN}; its third line is in a font the glyph table does not cover. Displays after each step: "
			+ "; ".join(f"\"{text}\"" for text in init_texts) + "."
		),
	}
	lamp_names, observations["lamp-matrix"] = lamp_matrix(runs["lamp-matrix"])
	sol_names, observations["solenoids"] = solenoid_test(runs["solenoids"])
	_, observations["switch-matrix"] = switch_matrix(runs["switch-matrix"])
	observations["front-door"] = front_door(runs["front-door"])
	observations["tournament-door"] = scripted(runs["tournament-door"], "Attract mode, coin door and tournament switches.")
	observations["gameplay"] = scripted(
		runs["gameplay"], "One game started with two coins on chute 1, the trough (33) and ramp motor (30) switches closed.",
		{6, 7, 10, 11, 12, 13, 23, 28, 29, 32},
	)
	observations["mechanism-sensors"] = scripted(
		runs["mechanism-sensors"], "One game started with the ramp motor switch (30) open, then 30 closed, opened and closed again.",
		{13, 23},
	)
	named = {}
	for number, name in sorted(lamp_names.items()):
		named[f"lamp-{number:03d}-{slug(name) or 'unnamed'}"] = number
	for number, name in sorted(sol_names.items()):
		named[f"solenoid-{number:02d}-{slug(name)}"] = number + 1
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "gladiators-harness-runs", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": SOURCE_PATH,
			"sha256": manifest_sha,
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes, NVRAM and DMD frames remain external.",
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
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": REVISION},
			"raw_runs": raw,
			"command_template": COMMAND_TEMPLATE,
			"observations": {
				"service_language": "English",
				"named_output_addresses": named,
				"solenoid_addresses_seen": sorted({address for step in runs["solenoids"].data["steps"] for address in solenoids_on(step)}),
				"runs": observations,
			},
		},
	}


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="re-derive the bundle and refuse drift, writing nothing")
	args = parser.parse_args()
	expected = canonical_bytes(build(working_root()))
	if args.check:
		if not EVIDENCE_PATH.is_file() or EVIDENCE_PATH.read_bytes() != expected:
			print("drift: " + EVIDENCE_PATH.relative_to(ROOT).as_posix())
			return 1
		print("Gladiators runtime evidence matches the retained runs.")
		return 0
	EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
	EVIDENCE_PATH.write_bytes(expected)
	print(f"wrote {EVIDENCE_PATH.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
