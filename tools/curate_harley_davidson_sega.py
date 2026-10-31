"""Curate the physical Sega Harley-Davidson (1999) machine definition.

Sega built Harley-Davidson as its model 67 until Stern Pinball took the production run over and continued it as its
own 1st edition, which tools/curate_harley_davidson.py curates. The two records describe one playfield, one wiring and
one controller routing, so this builder derives the Sega record from that curator's build: every construction, wiring,
mechanism and placement fact comes over unchanged. It replaces the identity, the drivers and the sources, rewrites
every runtime claim the Stern record bases on the Stern ROMs with what Sega's firmware 1.03 (harl_a13) did in its own
harness runs, and compares every matrix switch, lamp and coil name and wire pair the 1.03 ROM's Portals service tests
print against the manual's tables, refusing any difference it does not list.

The builder is side-effect free and deterministic and reads only committed files: the Stern curator's literals and
seeds, the committed harl_a13 runtime evidence and this record's knowledge seed. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the definition, its knowledge note and its spatial report.
"""

from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
import curate_harley_davidson as base
from harley_davidson_sega_runtime_evidence import RUNS as RUN_MANIFESTS


ROOT = base.ROOT

MACHINE_ID = "sega.harley-davidson.1999"
PARTIAL_PATH = ROOT / "machines/partial/sega/harley-davidson-1999.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/sega/harley-davidson-1999.json"
KNOWLEDGE_PATH = ROOT / "knowledge/sega/harley-davidson-1999.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/sega/harley-davidson-1999-knowledge.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/sega/harley-davidson-1999.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/sega/harley-davidson-1999.md"
RUNTIME_PATH = "evidence/runtime/whitestar/harley-davidson-harl-a13-service-tests-and-gameplay.json"
EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"

IDENTITY_SOURCE = "identity.sega.harley-davidson.1999"
README_SOURCE = "service-bulletin.stern.harley-davidson.rom-readme"
BULLETIN_SOURCES = {
	113: "service-bulletin.stern.harley-davidson.113",
	114: "service-bulletin.stern.harley-davidson.114",
	121: "service-bulletin.stern.harley-davidson.121",
}
ROM_SOURCE = "rom.sega.harley-davidson.1-03"
RUNTIME_SOURCE = "runtime.harley-davidson.harl-a13"
# Stern sources that describe the Stern ROMs' runs and files: replaced by this record's run, or dropped. The Stern
# record's IPDB source stays, because device notes quote its 2nd- and 3rd-edition pages.
REPLACED_SOURCES = {base.RUNTIME_SOURCE: RUNTIME_SOURCE, base.RUNTIME_A30_SOURCE: None, base.ROM_SOURCE: None, base.ROM_A30_SOURCE: None}
ROM_ARCHIVE_SHA256 = "8027994701250356303a4eb68ae1c37cd0080afbffe13ca9364b58647ba9996f"
README_SHA256 = "abff199c436651916bc8ff78c9b0ac12779e1200b49b0084a6c1d56991d23bb0"
README_URL = "https://web.archive.org/web/20060512000521/http://www.sternpinball.com/downloads/hdROMreadme.txt"
README_RELATIVE_PATH = f"pinmame-manuals/by-machine/{MACHINE_ID}/stern-site-wayback/hdROMreadme-20060512000521.txt"
# Bulletin -> (date, SHA-256, Internet Archive SHA-1, acquisition time, locator).
BULLETINS = {
	113: (
		"December 10, 1999", "065b3d07c3332950928a67067b98d8381ae71aefe34494da43be672c47694613",
		"3f695945c06e3d4ccddc9ec01c2f2c451c705fc8", "2026-10-30T23:57:35Z",
		"three pages: the H-D ball guide wire forms with flanged ends that protect the motorcycle-entrance optos (serials "
		"148598-149648) and the -16 plastic support plate kit 500-6408-67 (serials 148598-150600)",
	),
	114: (
		"February 11, 2000", "07fb777e5d06770f4ca82f6a5cb7e6f7822834511542716f080cf0f16990a22a",
		"966949f25339a448d7441032c470137d976a0cb9", "2026-10-30T23:57:39Z",
		"two pages: Operator Alert #19 Motor Relay, the lift assembly's link, spring, cam and set screw, the cam stopping on "
		"the Up switch 35 and the Down switch 36, and the motor test's RUN and PULSE icons for the relay Q19 drives",
	),
	121: (
		"February 5, 2001", "764b86fa9fd3199d4f38e38d85ad70a5afb8ecd492fa8b08373543dd243a92b6",
		"33da206b076a32dab2841937fedd53ef2874d4f4", "2026-10-30T23:57:42Z",
		"one page: the metal support plate kit 502-5003-67 for the -15 plastic at the left of the motorcycle",
	),
}
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=4453"
EXCERPT_CREDIT = "curator, read from the rendered page"
QUOTE_CREDIT = "curator, quoted from the source file"


# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("harl_a10", "harl_a13", "harl_f13", "harl_g13", "harl_i13", "harl_l13", "harl_u13")
BASE_DRIVER_NOTE = (
	"src/wpc/sims/se/prelim/harley.c builds the seven Sega Harley-Davidson drivers (lines 476-510) on the de_mSES1 machine "
	"driver with the HARLEY_SOUND set and the init_harl every Stern set uses, which installs harlGameData: GEN_WS, a 128x32 "
	"DMD, FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), lamp columns 2, no custom solenoids, no auxiliary board, and harley_handleMech. "
	"The controller routing, lamp columns and display are therefore those of the Stern sets. MACHINE_INIT(se) gives none of "
	"the seven the fast-flip byte, so public 15 never rises. "
)
# driver -> (game ROM, CRC, display ROM, CRC, language, display version)
DRIVER_ROMS = {
	"harl_a13": ("harcpu.103", "2a812c75", "hddispa.104", "fc7c2924", "English", "1.04"),
	"harl_u13": ("harcpuk.103", "e39130a7", "hddispa.104", "fc7c2924", "English", "1.04"),
	"harl_a10": ("harcpu.103", "2a812c75", "hddispa.100", "bdeac0fd", "English", "1.00"),
	"harl_f13": ("harcpu.103", "2a812c75", "hddispf.104", "5f80436e", "French", "1.04"),
	"harl_g13": ("harcpu.103", "2a812c75", "hddispg.104", "c7f197a0", "German", "1.04"),
	"harl_i13": ("harcpu.103", "2a812c75", "hddispi.104", "387a5aad", "Italian", "1.04"),
	"harl_l13": ("harcpu.103", "2a812c75", "hddisps.104", "2d26514a", "Spanish", "1.04"),
}
# Display ROM -> the checksum Stern's ROM readme prints for it.
README_DISPLAY_CHECKSUMS = {
	"hddispa.104": "$FC7C", "hddispf.104": "$B8E1", "hddispg.104": "$09ED", "hddispi.104": "$79B7", "hddisps.104": "$F9B5",
	"hddispa.100": "$EFBA",
}


def _driver_note(driver_id: str) -> str:
	cpu, cpu_crc, display, display_crc, language, version = DRIVER_ROMS[driver_id]
	note = f"Game ROM 1.03 ({cpu}, CRC {cpu_crc}) with the {language} display ROM {version} ({display}, CRC {display_crc})."
	if driver_id == "harl_a13":
		note += (
			" The 3rd-edition manual's firmware appendix gives this pair, game ROM A1.03 ($3EFF) and display A1.04 ($FC7C), as the "
			"'Original (1999-2001)' firmware. Stern's ROM readme dates game ROM 1.03 to October 1, 1999 and lists display 1.04 "
			f"({README_DISPLAY_CHECKSUMS[display]}) in an undated block before the 1.05 release of October 28, 2002. "
			f"{len(RUN_MANIFESTS)} harness runs booted it."
		)
		return note
	if driver_id == "harl_u13":
		note += (
			" Pinned PinMAME calls it '1.03 English'. Stern's ROM readme lists harcpuk.101, harcpuk.102 and harcpuk.103 beside the "
			"harcpu ROMs of the same releases, with the same checksums, and does not say what the k variant changes."
		)
	elif driver_id == "harl_a10":
		note += (
			" Stern's ROM readme lists hddispa.100 ($EFBA) in the initial release of September 7, 1999, and IPDB's page 4453 lists "
			"the set as 'PinMAME Romset (1.03) display version 1.00'."
		)
	else:
		note += f" Stern's ROM readme lists {display} ({README_DISPLAY_CHECKSUMS[display]}) in the undated display 1.04 block."
	return note + " No harness run booted it."


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {driver["id"]: driver for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
	if set(by_id) != set(DRIVER_IDS):
		raise RuntimeError(f"Sega Harley-Davidson driver family differs from the catalog: {sorted(set(DRIVER_IDS) ^ set(by_id))}")
	records = []
	for driver_id in sorted(DRIVER_IDS):
		source = by_id[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = BASE_DRIVER_NOTE + _driver_note(driver_id)
		records.append(record)
	return records


# --- The 1.03 ROM's service tests --------------------------------------------------------------------
# Where the ROM's wording differs from the manual's beyond spacing and case: address -> (the manual's exact text, the
# ROM's exact text). Both sides are pinned, so a changed manual transcription cannot ride on an allowed difference.
SWITCH_WORDING = {
	1: ("LEFT BUTTON (UK ONLY)", "LT BUTTON (UK ONLY)"), 8: ("RIGHT BUTTON (SKILL)", "RT BUTTON (SKILL)"),
	41: ("M-CYCLE TROUGH #4 (TOP)", "M-CYCLE TROUGH #4"), 44: ("M-CYCLE TROUGH #1 (BOT)", "M-CYCLE TROUGH #1"),
}
LAMP_WORDING = {
	7: ("SUPER JACK-PO T (RED)", "SUPER JACKPOT (RED)"), 8: ("SUPER JACK-PO T (GRN)", "SUPER JACKPOT (GRN)"),
	25: ("M-CYCLE GRN LIGHT", "M-CYCLE GREEN LIGHT"), 26: ("M-CYCLE YEL LIGHT", "M-CYCLE YELLOW LIGHT"),
	29: ("RT TURBO BUMPER", "RIGHT TURBO BUMPER"), 30: ("BOT TURBO BUMPER", "BOTTOM TURBO BUMPER"),
	32: ("SPEEDO- METER X2", "SPEEDOMETER x2"), 33: ("SUPER VUK GRN LIGHT", "SUPER VUK GREEN LIGHT"),
	34: ("SUPER VUK YEL LIGHT", "SUPER VUK YELLOW LIGHT"), 41: ("RT RAMP GRN LIGHT", "RT RAMP  GREEN LIGHT"),
	42: ("RT RAMP YEL LIGHT", "RT RAMP  YELLOW LIGHT"), 48: ("LITE MYST- ERY RIDER", "LITE MYSTERY RIDER"),
	49: ("RT ORBIT GRN LIGHT", "RT ORBIT GREEN LIGHT"), 50: ("RT ORBIT YEL LIGHT", "RT ORBIT YELLOW LIGHT"),
	67: ("LITE MYSTERY... RT RETURN", "LITE MYSTERY RT RETURN"), 70: ("RIDE AGAIN X2", "RIDE AGAIN #2"),
}
COIL_WORDING = {31: ("FLASH: RT. DROP TARGET X2", "FLASH: RIGHT DROP TARGET x2")}
COIL_PUBLIC = {15: [47, 48], 16: [45, 46]}


def _normalized(text: str) -> str:
	return re.sub(r"\s+", "", text).casefold()


def _snapshots(evidence: dict[str, Any]) -> dict[str, str]:
	return {item["label"]: item["interpreted_text"] for item in evidence["runtime"]["observations"]["diagnostic_snapshots"]}


def _reading(snapshots: dict[str, str], run: str, label: str, title: str, parts: int) -> list[str]:
	text = snapshots.get(f"{run} snapshot: {label}")
	if text is None:
		raise RuntimeError(f"Sega Harley-Davidson runtime evidence lacks the frame '{run}: {label}'")
	fields = text.split(" / ")
	if len(fields) != parts or fields[0] != title:
		raise RuntimeError(f"Sega Harley-Davidson frame '{run}: {label}' does not read as a {title} frame: {text!r}")
	return fields[1:]


def _check_name(kind: str, address: int, printed: str, rom: str, wording: dict[int, tuple[str, str]]) -> None:
	if address in wording:
		manual, expected = wording[address]
		if printed != manual or rom != expected or _normalized(rom) == _normalized(printed):
			raise RuntimeError(f"Sega Harley-Davidson {kind} {address}: the ROM prints {rom!r} where the manual prints {printed!r}; the wording table expects {expected!r} against {manual!r}")
	elif _normalized(rom) != _normalized(printed):
		raise RuntimeError(f"Sega Harley-Davidson {kind} {address}: the ROM prints {rom!r} where the manual prints {printed!r}")


def switch_test_readings(evidence: dict[str, Any]) -> dict[int, tuple[str, str]]:
	"""Matrix switch -> (name, wire text) the 1.03 Portals Switch Test printed while the scenario held it closed, refused
	unless the name matches the Switch Matrix Grid and the wires and number match the matrix drive and return."""
	snapshots = _snapshots(evidence)
	readings: dict[int, tuple[str, str]] = {}
	for address in range(1, 65):
		run = "harl-a13-switch-test-41-45" if 41 <= address <= 45 else "harl-a13-switch-test"
		name, wires, footer = _reading(snapshots, run, f"switch {address} closed in the Switch Test", "SWITCH TEST", 4)
		column, row = divmod(address - 1, 8)
		if footer != "DOOR BUTTONS OPERATE MENU" or wires != f"{base.MATRIX_DRIVE[column][0]} {base.MATRIX_RETURN[row][0]} #{address:02d}":
			raise RuntimeError(f"Sega Harley-Davidson switch {address}: the Switch Test prints {wires!r} / {footer!r}")
		printed = base.SWITCHES[address][1] if address in base.SWITCHES else "NOT USED"
		if address not in base.SWITCHES and address not in base.UNUSED_SWITCHES:
			raise RuntimeError(f"Sega Harley-Davidson switch {address} is in neither switch table")
		_check_name("switch", address, printed, name, SWITCH_WORDING)
		readings[address] = (name, wires)
	return readings


def lamp_test_readings(evidence: dict[str, Any]) -> dict[int, tuple[str, str]]:
	"""Lamp -> (name, wire text) the 1.03 Single Lamp Test printed at that step, refused unless the name matches the Lamp
	Matrix Grid (NOT USED for every unused and unresolved cell), the wires match the lamp matrix, and the step changed this
	lamp and at most the one the previous step lit."""
	snapshots = _snapshots(evidence)
	changed: dict[int, set[int]] = {}
	for observation in evidence["runtime"]["observations"]["named_action_observations"]:
		match = re.fullmatch(r"harl-a13-single-lamp-test step \d+: Black ENTER button \(public 0\) pressed on \+: lamp step (\d+); lamps changed during the step: (.+)", observation["label"])
		if match:
			changed[int(match.group(1))] = set() if match.group(2) == "none" else {int(item) for item in match.group(2).split(", ")}
	readings: dict[int, tuple[str, str]] = {}
	for address in range(1, 81):
		name, wires = _reading(snapshots, "harl-a13-single-lamp-test", f"Black ENTER button (public 0) pressed on +: lamp step {address}", "SINGLE LAMP TEST", 3)
		row, column = divmod(address - 1, 8)
		if wires != f"{base.LAMP_DRIVE[column][0]} {base.LAMP_RETURN[row][0]} #{address:02d}":
			raise RuntimeError(f"Sega Harley-Davidson lamp {address}: the Single Lamp Test prints {wires!r}")
		if address not in changed.get(address, set()) or changed[address] - {address - 1, address}:
			raise RuntimeError(f"Sega Harley-Davidson lamp {address}: its Single Lamp Test step changed lamps {sorted(changed.get(address, ()))}")
		printed = base.LAMPS[address][1] if address in base.LAMPS else "NOT USED"
		_check_name("lamp", address, printed, name, LAMP_WORDING)
		readings[address] = (name, wires)
	return readings


def coil_test_readings(evidence: dict[str, Any]) -> dict[int, tuple[str, str]]:
	"""Driver Q1-Q32 -> (name, wire text) the 1.03 Single Coil Test printed when it was selected, refused unless the name
	matches the coil chart, the wires match its power and control wires, and firing it there pulsed exactly its public
	address (both published flipper states for Q15 and Q16)."""
	snapshots = _snapshots(evidence)
	fired = {}
	for observation in evidence["runtime"]["observations"]["named_action_observations"]:
		match = re.fullmatch(r"harl-a13-single-coil-test step \d+: Black ENTER button \(public 0\) pressed on RUN: coil step (\d+) fired(?:;.*)?", observation["label"])
		if match and int(match.group(1)) <= 32:
			fired[int(match.group(1))] = observation["transitioned_solenoid_addresses"]
	readings: dict[int, tuple[str, str]] = {}
	for number in range(1, 33):
		name, wires = _reading(snapshots, "harl-a13-single-coil-test", f"Black ENTER button (public 0) pressed on +: coil step {number} selected", "SINGLE COIL TEST", 3)
		label, printed, *_, power_wire, _power_connection, _voltage, control_wire, _control_connection = base.Q_OUTPUTS[number]
		prefix = f"#{number} " if number <= 24 else f"#F{number - 24} "
		power, _, control = wires.partition(" ")
		if not name.startswith(prefix) or power not in power_wire.split(" / ") or control != control_wire:
			raise RuntimeError(f"Sega Harley-Davidson coil {number}: the Single Coil Test prints {name!r} / {wires!r}")
		_check_name("coil", number, printed, name.removeprefix(prefix), COIL_WORDING)
		if fired.get(number) != COIL_PUBLIC.get(number, [number]):
			raise RuntimeError(f"Sega Harley-Davidson coil {number}: firing it in the Single Coil Test pulsed {fired.get(number)}")
		readings[number] = (name, wires)
	return readings


# --- Runtime claims ----------------------------------------------------------------------------------
LAMPS_SEEN_SENTENCE = " The harness runs saw both ROMs drive it."
GLOBAL_REWRITES = (
	# (Stern text, Sega text, occurrences across device notes and mechanism behaviours)
	(LAMPS_SEEN_SENTENCE, " Outside the Single Lamp Test the harness runs saw the ROM drive it.", 60),
	("The gameplay harness runs closed it once", "The gameplay harness run closed it once", 7),
	("In the gameplay harness runs,", "In the gameplay harness run,", 2),
	("In the gameplay runs", "In the gameplay run", 11),
	("in the gameplay runs", "in the gameplay run", 3),
	(
		" No harness run saw the ROM drive it, and the retained script assigns no Light to it.",
		" Outside the Single Lamp Test, which lights every address from 1 to 80 in turn, no harness run saw the ROM drive it, "
		"and the retained script assigns no Light to it.", 7,
	),
	("; no harness run drove an address above 72.", "; outside the Single Lamp Test no harness run drove an address above 72.", 8),
)
SCOOP_RELEASE_KICK = "2.96 s"
# device or mechanism id -> [(Stern text, Sega text)], each applied exactly once after GLOBAL_REWRITES.
DEVICE_REWRITES = {
	"switch.16-shooter-lane": [(" On harl_a30 the game-on state 15 rose when the served ball reached it.", "")],
	"switch.33-left-orbit": [(
		"The gameplay harness run closed it once in a game and the ROM fired no coil or flasher of its own in response, which says "
		"nothing against its fitment.",
		"The gameplay harness run closed it once in a game and the ROM fired no coil in response; the super-VUK flashers 30, lit "
		"since the stand-up target 32 closed 3 s earlier, went dark 0.08 s after the closure and lit once more from 0.14 to 0.34 s "
		"after it, which may answer either switch.",
	)],
	"switch.37-motorcycle-enter-opto": [(
		"In the gameplay run a 1 pulse three seconds after the scenario had emptied the scoop, which the ROM had not kicked while "
		"the ball stayed, was followed about 20 ms later by a scoop kick (4); the record claims no coil response for 37 from that "
		"one coincidence.",
		f"In the gameplay run the ROM kicked the scoop (4) {SCOOP_RELEASE_KICK} after the scenario had emptied it, having not "
		"kicked while the ball stayed, and 40 ms before a 1 pulse on 37, so that kick was no response to 37.",
	)],
	"switch.46-ball-eject-scoop": [(
		"a ball held on it for 6 s flashed 25 and 30 and drew no kick while it stayed.",
		f"a ball held on it for 6 s flashed 25 and 30 and drew no kick while it stayed, and the ROM kicked the empty scoop "
		f"{SCOOP_RELEASE_KICK} after the scenario released 46.",
	)],
	"switch.48-behind-top-vuk": [("; on harl_a30 the game-on state 15 fell about 2 s later", "")],
	"switch.88-not-used-ds-5": [("harl_a40's Portals Dedicated Switch Test", "harl_a13's Portals Dedicated Switch Test")],
	"device.q4-power-scoop-kick-big": [(
		"a 6 s hold later in a game drew none;",
		f"a 6 s hold later in a game drew none while the ball stayed and one kick {SCOOP_RELEASE_KICK} after the scenario "
		"emptied the scoop;",
	)],
	"device.q5-motorcycle-ball-launch": [(
		"No harness run fired the motorcycle ball launch: no run had the ROM eject the motorcycle trough.",
		"Only the Single Coil Test, which fires each driver on request, fired the motorcycle ball launch: no run had the ROM "
		"eject the motorcycle trough in play.",
	)],
	"device.q14-magnet": [(
		"In the harness runs its only activity was the ROM's ball search;",
		"In the harness runs its only activity outside the Single Coil Test was the ROM's ball search;",
	)],
	"device.q20-scoop-flasher": [("; no other step drew it.", "; no other step outside the Single Coil Test drew it.")],
	"lamp.47-auto-launch": [("No harness run saw the ROM light it,", "Outside the Single Lamp Test no harness run saw the ROM light it,")],
	"lamp.69-motorcycle-headlight": [(
		"Only the harl_a30 gameplay run saw the ROM light it; the harl_a40 runs never did, which says nothing against its fitment.",
		"Every harl_a13 harness run saw the ROM blink it in attract mode from 9.3 s after power-up, and the gameplay run during "
		"play as well; Stern's ROM readme lists 'removed headlight from lightshows' for game ROM 3.01 (November 22, 2004).",
	)],
	"mechanism.kick-out-trough": [("; no run fired Q5.", "; no run but the Single Coil Test fired Q5.")],
}
UNRESOLVED_LAMP_TAIL = (
	" Yet both exercised ROMs (harl_a40 and harl_a30) switch 52, 53 and 54 during play: from about 1 s after the served ball "
	"reaches the shooter lane, usually all three at the same instant and in step with lamp effects on 36, 37, 42 and 49, never "
	"in attract mode, while 55 and 56 stay dark. No retained script binds them. Nothing available here explains what that state "
	"reaches, so availability stays unknown. Resolution path: the 1st- or 2nd-edition manual's lamp grid (manual part numbers "
	"780-5067-01 and 780-5067-10, neither retained) or the ROM's Single Lamp test, read on a harness run, would show whether an "
	"earlier edition fitted bulbs here."
)
SEGA_UNRESOLVED_LAMP_TAIL = (
	" The 1.03 ROM's own Single Lamp Test agrees and names 52 to 56 NOT USED. Yet harl_a13 switches 52, 53 and 54 during play: "
	"in the gameplay run from about 1 s after the served ball reached the shooter lane, usually all three at the same instant "
	"and in step with lamp effects on 36, 37, 42 and 49, never in attract mode, while 55 and 56 stayed dark. No retained script "
	"binds them. Nothing available here explains what that state reaches, so availability stays unknown. Resolution path: the "
	"1st-edition manual's lamp grid (manual part number 780-5067-01, dated AUG 99 in the 3rd-edition manual's production "
	"appendix, not retained) or a look under an early production playfield would show whether anything was ever fitted here."
)
FAST_FLIP_NOTE = (
	"se.c sets public 15 while the ROM's fast-flip byte is non-zero, i.e. while the flippers are enabled in a game; MACHINE_INIT(se) "
	"places that byte at CPU RAM 0x00 for the Stern harl_a30 set only and sets none for the seven Sega sets, so PinMAME never "
	"raises 15 for this machine: no harl_a13 run saw it rise, although the gameplay run enabled the flippers. sega.vbs still "
	"declares GameOnSolenoid = 15. Physical Q15 is the left flipper at public 48; never wire this state to a transistor."
)
STERN_RUNTIME_WORDS = re.compile(r"harl_a40|harl_a30|both ROMs|both exercised|gameplay runs|gameplay harness runs|No harness run (?:saw|fired|had)")
# Lamps whose rewritten notes say no run drove them outside the Single Lamp Test.
LAMPS_NOT_SEEN = (47, 55, 56, 60, 61, 62, 63, 64) + tuple(range(73, 81))


def _text_fields(definition: dict[str, Any]) -> list[tuple[dict[str, Any], str, str]]:
	"""(container, key, owner id) for every device note and mechanism behaviour."""
	fields = [(device["physical"], "notes", device["id"]) for device in definition["inputs"] + definition["outputs"] if "notes" in device.get("physical", {})]
	fields += [(mechanism, "behavior", mechanism["id"]) for mechanism in definition["mechanisms"]]
	return fields


def _replace_once(text: str, old: str, new: str, owner: str) -> str:
	if text.count(old) != 1:
		raise RuntimeError(f"Sega Harley-Davidson rewrite of {owner} expects one {old[:60]!r}, found {text.count(old)}")
	return text.replace(old, new)


def rewrite_runtime_claims(definition: dict[str, Any], evidence: dict[str, Any]) -> None:
	observations = evidence["runtime"]["observations"]
	outside = set(observations["lamp_addresses_driven_outside_self_test"])
	fields = _text_fields(definition)
	for device in definition["outputs"]:
		if LAMPS_SEEN_SENTENCE in device.get("physical", {}).get("notes", "") and device["binding"]["device"] not in outside:
			raise RuntimeError(f"Sega Harley-Davidson lamp {device['binding']['device']}: no harl_a13 run drove it outside the Single Lamp Test")
	for old, new, expected in GLOBAL_REWRITES:
		found = sum(container[key].count(old) for container, key, _ in fields)
		if found != expected:
			raise RuntimeError(f"Sega Harley-Davidson rewrite expects {expected} of {old[:60]!r}, found {found}")
		for container, key, _ in fields:
			container[key] = container[key].replace(old, new)
	by_owner = {owner: (container, key) for container, key, owner in fields}
	for owner, rewrites in DEVICE_REWRITES.items():
		container, key = by_owner[owner]
		for old, new in rewrites:
			container[key] = _replace_once(container[key], old, new, owner)
	for address in base.UNRESOLVED_LAMPS:
		container, key = by_owner[base.lamp_id(address)]
		container[key] = _replace_once(container[key], UNRESOLVED_LAMP_TAIL, SEGA_UNRESOLVED_LAMP_TAIL, base.lamp_id(address))
	if 15 in observations["solenoid_addresses_seen"] or set(base.UNRESOLVED_LAMPS) - outside or 69 not in outside or outside & set(LAMPS_NOT_SEEN):
		raise RuntimeError("Sega Harley-Davidson runtime evidence contradicts the fast-flip, lamp 52-54, headlight or unlit-lamp claims")
	fast_flip = next(device for device in definition["outputs"] if device["id"] == "virtual.15-fast-flip-game-on")
	fast_flip["availability"] = "unused"
	fast_flip["physical"]["notes"] = FAST_FLIP_NOTE
	leftovers = [owner for container, key, owner in _text_fields(definition) if owner != fast_flip["id"] and STERN_RUNTIME_WORDS.search(container[key])]
	if leftovers:
		raise RuntimeError(f"Sega Harley-Davidson notes still describe the Stern ROMs' runs: {leftovers}")


def append_service_test_readings(definition: dict[str, Any], evidence: dict[str, Any]) -> None:
	switches, lamps, coils = switch_test_readings(evidence), lamp_test_readings(evidence), coil_test_readings(evidence)
	sentences: dict[tuple[str, int], str] = {}
	for address, (name, wires) in switches.items():
		sentences[(base.SWITCH_GROUP, address)] = f' The 1.03 ROM\'s Portals Switch Test prints "{name} / {wires}" while it is closed.'
	for address, (name, wires) in lamps.items():
		sentences[(base.LAMP_GROUP, address)] = f' The 1.03 ROM\'s Single Lamp Test prints "{name} / {wires}" and lights it at that step.'
	for number, (name, wires) in coils.items():
		public = COIL_PUBLIC.get(number, [number])
		effect = f"raised public {public[0]} and {public[1]}" if len(public) == 2 else f"pulsed public {number}"
		sentences[(base.SOLENOID_GROUP, public[-1])] = f' The 1.03 ROM\'s Single Coil Test prints "{name} / {wires}" for Q{number}, and firing it there {effect}.'
	for device in definition["inputs"] + definition["outputs"]:
		sentence = sentences.pop((device["binding"]["group"], device["binding"]["device"]), None)
		if sentence is None:
			continue
		device["physical"]["notes"] += sentence
		refs = device["provenance"]["source_refs"]
		if RUNTIME_SOURCE not in refs:
			refs.append(RUNTIME_SOURCE)
	if sentences:
		raise RuntimeError(f"Sega Harley-Davidson service-test readings name no device: {sorted(sentences)}")


# Device or mechanism id -> (sentence appended to its note or behaviour, the source it cites).
DOCUMENT_CITATIONS = {
	"switch.35-motor-up": (
		" Stern's Service Bulletin 114 (February 11, 2000): 'The switches are supposed to be set so the cam can stop on the "
		"Up-Switch (#35) and the Down-Switch (#36).'", BULLETIN_SOURCES[114],
	),
	"switch.36-motor-down": (
		" Stern's Service Bulletin 114 (February 11, 2000): 'The switches are supposed to be set so the cam can stop on the "
		"Up-Switch (#35) and the Down-Switch (#36).'", BULLETIN_SOURCES[114],
	),
	"switch.37-motorcycle-enter-opto": (
		" Stern's Service Bulletin 113 (December 10, 1999): on some early machines (serials 148598-149648) the two 5/8\" ball "
		"guides at the left and right of the motorcycle entrance, which protect its opto switches from the ball, lack stamped "
		"flange ends and can be hammered into the playfield; its kit replaces them with flanged guides 535-5356-19.",
		BULLETIN_SOURCES[113],
	),
	"device.q19-motor-relay": (
		" Stern's Service Bulletin 114 (February 11, 2000) traces 'Operator Alert #19-Motor Relay' mostly to the lift's mechanics "
		"rather than the relay, and drives the relay from the motor test's RUN and PULSE icons with the power interlock switch "
		"pulled out.", BULLETIN_SOURCES[114],
	),
	"mechanism.motorcycle-lift": (
		" Service Bulletin 114 (February 11, 2000) lists the lift faults behind Operator Alert #19 (Motor Relay): the spring "
		"popping off the link in shipping, a link binding on the rotating cam, a loose cam set screw, the cam catching the motor "
		"mounting screws and a dead spot in the motor.", BULLETIN_SOURCES[114],
	),
	"lamp.69-motorcycle-headlight": ("", README_SOURCE),
}


def cite_documents(definition: dict[str, Any]) -> None:
	owners = {item["id"]: item for item in definition["inputs"] + definition["outputs"] + definition["mechanisms"]}
	for owner, (sentence, source) in DOCUMENT_CITATIONS.items():
		item = owners[owner]
		if "behavior" in item:
			item["behavior"] += sentence
		else:
			item["physical"]["notes"] += sentence
		refs = item["provenance"]["source_refs"]
		if source in refs:
			raise RuntimeError(f"Sega Harley-Davidson {owner} already cites {source}")
		refs.append(source)


def swap_source_refs(node: Any) -> None:
	"""Replace the Stern runtime source with this record's throughout the tree and drop the Stern-only runs and ROMs."""
	if isinstance(node, dict):
		for key, value in node.items():
			if key == "source_refs":
				swapped: list[str] = []
				for ref in value:
					ref = REPLACED_SOURCES[ref] if ref in REPLACED_SOURCES else ref
					if ref is not None and ref not in swapped:
						swapped.append(ref)
				node[key] = swapped
			else:
				swap_source_refs(value)
	elif isinstance(node, list):
		for item in node:
			swap_source_refs(item)


# --- Sources -------------------------------------------------------------------------------------------
def _excerpt(name: str, locator: str, *, reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	path = EXCERPT_ROOT / f"{name}.md"
	return {
		"id": f"excerpt.harley-davidson-sega.{name}", "locator": locator, "path": path.relative_to(ROOT).as_posix(),
		"sha256": base._file_sha256(path), "method": "manual", "transcribed_by": credit, "reviewed": reviewed,
	}


def source_records(stern_sources: list[dict[str, Any]], evidence: dict[str, Any]) -> list[dict[str, Any]]:
	by_id = {source["id"]: copy.deepcopy(source) for source in stern_sources}
	if set(REPLACED_SOURCES) - set(by_id):
		raise RuntimeError("Sega Harley-Davidson: the Stern build no longer carries a source this curator replaces")
	by_id[base.CATALOG_SOURCE]["locator"] = "Pinned catalog driver records for the harl_a13 clone tree (" + ", ".join(DRIVER_IDS) + ")"
	by_id[base.CORE_SOURCE]["locator"] = (
		"src/wpc/sims/se/prelim/harley.c harlGameData (GEN_WS, se_dmd128x32, FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), swCol 0, lampCol 2, "
		"custSol 0, harley_handleMech, invSw all zero, start/tilt/slam 54/56/55), init_harl and the seven Sega ROM sets on "
		"de_mSES1 (lines 476-510); src/wpc/se.c MACHINE_INIT(se) (fast-flip byte at CPU RAM 0x00 for the Stern harl_a30 only, none "
		"for a Sega set), the fast-flip block publishing public 15, the harl_ PWM bulb model on 20 and 25-32, switch_r "
		"(~core_getSwCol), dedswitch_r (flipper column swapped into U206 order, complemented), dip_r, se_solenoid_w (Q15/Q16 masked "
		"off and published at 47/45), the G.I. relay at gi[0], ram_w's memory-protect gate on -3; src/wpc/core.c core_updateSw (no "
		"FLIP_EOS: EOS bits untouched)."
	)
	by_id[base.VPX_SCRIPT_SOURCE]["locator"] += (
		" The table runs the Stern 3.00 set; every harl_ set shares harlGameData, so its controller bindings apply to harl_a13."
	)
	ipdb_4455 = base.IPDB_PAGE_SHA256
	ipdb_4453 = base.IPDB_PAGE_SHA256S[4453]
	identity = {
		"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "sha256": ipdb_4453, "acquired_at": "2026-10-30T18:49:00Z",
		"locator": (
			"IPDB machine 4453 'Harley-Davidson®' (Sega Pinball, Incorporated, September 1999, model 67, page SHA-256 "
			f"{ipdb_4453}), fetched live through an authenticated browser session because the site is Cloudflare-gated, with the "
			f"page of Stern's 1st edition, machine 4455 (page SHA-256 {ipdb_4455}), whose note calls it the continuation of the "
			f"production run of Sega's model 67. Both pages are retained, each with a gzip-compressed Wayback Machine capture, under "
			f"{base.MANUALS_DIRECTORY}."
		),
		"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
		"excerpts": [_excerpt("ipdb-pages", "IPDB machine pages 4453 and 4455", reviewed=False)],
	}
	readme = {
		"id": README_SOURCE, "kind": "service_bulletin", "uri": f"external:{README_RELATIVE_PATH}", "original_filename": "hdROMreadme.txt",
		"sha256": README_SHA256, "acquired_at": "2026-10-31T00:13:56Z",
		"locator": (
			"Stern Pinball's Harley-Davidson ROM release notes ('(C) COPYRIGHT 1999-2004'), every release from the initial 1.00 of "
			"September 7, 1999 through 1.03 (October 1, 1999), the undated display 1.04 block, 1.05-1.08, 3.00, 3.01 and 4.00 (June "
			f"29, 2005), with each ROM's file name, board location and checksum. Retained from the Wayback Machine capture {README_URL}."
		),
		"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Stern Pinball, Inc.; archived by the Internet Archive's Wayback Machine",
		"excerpts": [_excerpt("rom-readme", "The whole file, in file order", credit=QUOTE_CREDIT)],
	}
	bulletins = []
	for number, (date, sha256, sha1, acquired_at, summary) in BULLETINS.items():
		item = f"Stern_Pinball_Service_Bulletin_{number}"
		bulletins.append({
			"id": BULLETIN_SOURCES[number], "kind": "service_bulletin", "uri": f"https://archive.org/details/{item}",
			"original_filename": f"sb{number}.pdf", "sha256": sha256, "acquired_at": acquired_at, "source_id": item,
			"locator": (
				f"Stern Technical Service Bulletin Nº {number}, {date}, {summary}. Internet Archive item {item}, file "
				f"https://archive.org/download/{item}/sb{number}.pdf (the item's SHA-1 {sha1} matches), uploaded 2017-08-05 by "
				"the uploader its metadata names, with no rights or licence field; the item metadata is retained beside the PDF "
				f"under pinmame-manuals/by-machine/{MACHINE_ID}/archive-org."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Stern Pinball, Inc.; hosted by the Internet Archive",
			"excerpts": [_excerpt("service-bulletins", f"Service Bulletin Nº {number}, from the PDF's text layer and a render of every page")],
		})
	runtime = evidence["runtime"]
	if runtime["emulator"]["sha256"] != base.RUNTIME_LIBRARY_SHA256 or runtime["rom_archive_sha256"] != ROM_ARCHIVE_SHA256:
		raise RuntimeError("Sega Harley-Davidson runtime evidence names another library or ROM archive")
	runs = ", ".join(f"{raw['name']} (run.json SHA-256 {raw['sha256'][:12]}..., directory manifest {RUN_MANIFESTS[raw['name']][0][:12]}...)" for raw in runtime["raw_runs"])
	rom = {
		"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/harl_a13.zip", "revision": "1.03", "sha256": ROM_ARCHIVE_SHA256,
		"locator": "User-authorized read-only archive whose members match the pinned harl_a13 ROM set (harcpu.103 CRC 2a812c75, hddispa.104 CRC fc7c2924); used to identify the ROM the harness booted. ROM bytes stay external.",
		"license": "NOASSERTION", "attribution": "Sega Pinball game code; ROM bytes remain external",
	}
	runtime_source = {
		"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_PATH}", "revision": base.PINMAME_REVISION,
		"locator": (
			f"{len(runtime['raw_runs'])} hash-pinned LibPinMAME harness runs of harl_a13 (library SHA-256 {base.RUNTIME_LIBRARY_SHA256[:12]}..., "
			f"built from {base.PINMAME_REVISION[:8]}) from empty NVRAM: {runs}. The Portals Switch Test (two runs, the second for "
			"switches 41-45), Single Lamp Test and Single Coil Test walks and the four motorcycle runs have built-in mechanisms off; "
			"the stacking-opto, gameplay, launch-scoop-opto, ds5-probe and dedicated-switch-test runs let PinMAME's motorcycle "
			"simulation write 35 and 36. Those five and the four motorcycle runs repeat the Stern record's harl_a40 scenarios step "
			"for step. Scenarios under "
			"tools/harness-scenarios/whitestar; tools/harley_davidson_sega_runtime_evidence.py derives the committed per-step "
			"transitions from the retained runs, and the Portals frames as diagnostic snapshots whose readings "
			"tools/seeds/sega/harley-davidson-1999-frame-readings.json pins by pixel SHA-256."
		),
		"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
	}
	order = [base.CATALOG_SOURCE, base.CORE_SOURCE, base.SIM_SOURCE, base.CONTROLLER_SOURCE]
	records = [by_id.pop(identifier) for identifier in order] + [identity, by_id.pop(base.IDENTITY_SOURCE)]
	records += [by_id.pop(base.MANUAL_SOURCE), by_id.pop(base.TECH_BRIEF_SOURCE), readme, *bulletins]
	for identifier in REPLACED_SOURCES:
		by_id.pop(identifier)
	records += [by_id.pop(source["id"]) for source in stern_sources if source["id"] in by_id]
	return records + [rom, runtime_source]


# --- Build ---------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	evidence = load_json(ROOT / RUNTIME_PATH)
	definition = copy.deepcopy(base.build())
	stern_sources = definition["sources"]
	definition["machine"] = {
		"id": MACHINE_ID, "name": "Harley Davidson", "manufacturer": "Sega", "year": 1999, "kind": "physical_pinball", "model_number": "67",
		"ipdb_id": 4453, "opdb_id": "G56lO-Mx00O",
		"playfield": {"width": base.PLAYFIELD_WIDTH, "height": base.PLAYFIELD_HEIGHT, "units": "vpx"},
	}
	definition["drivers"] = drivers()
	rewrite_runtime_claims(definition, evidence)
	swap_source_refs(definition)
	append_service_test_readings(definition, evidence)
	cite_documents(definition)
	definition["sources"] = source_records(stern_sources, evidence)
	definition["knowledge"] = {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"}
	known_sources = {source["id"] for source in definition["sources"]}
	cited: set[str] = set()

	def collect(node: Any) -> None:
		if isinstance(node, dict):
			cited.update(node.get("source_refs", []))
			for value in node.values():
				collect(value)
		elif isinstance(node, list):
			for item in node:
				collect(item)

	collect(definition)
	if cited - known_sources:
		raise RuntimeError(f"Sega Harley-Davidson cites sources it does not carry: {sorted(cited - known_sources)}")
	return definition


# --- Knowledge note ------------------------------------------------------------------------------------
STERN_SECTION = re.compile(r"^<!-- stern-section: (.+) -->$", re.MULTILINE)
# Stern-section text the Sega ROM's runs contradict: (Stern text, Sega text).
KNOWLEDGE_REWRITES = (
	("No harness run had the ROM fire Q5;", "Outside the Single Coil Test no harness run had the ROM fire Q5;"),
	(
		"Later in a game a 6 s hold drew no kick, so the ROM can keep the ball there;",
		f"Later in a game a 6 s hold drew no kick while the ball stayed, and one {SCOOP_RELEASE_KICK} after it left, so the ROM can keep the ball there;",
	),
)


def _stern_sections() -> dict[str, str]:
	text = base.KNOWLEDGE_SEED_PATH.read_text(encoding="utf-8")
	sections: dict[str, str] = {}
	for block in re.split(r"(?m)^(?=## )", text)[1:]:
		heading, _, _ = block.partition("\n")
		sections[heading.removeprefix("## ")] = block.rstrip("\n") + "\n"
	return sections


def render_knowledge() -> str:
	sections = _stern_sections()
	seed = KNOWLEDGE_SEED_PATH.read_text(encoding="utf-8")

	def embed(match: re.Match[str]) -> str:
		name = match.group(1)
		if name not in sections:
			raise RuntimeError(f"Sega Harley-Davidson knowledge seed embeds a Stern section that does not exist: {name}")
		return sections[name].rstrip("\n")

	text = STERN_SECTION.sub(embed, seed)
	for old, new in KNOWLEDGE_REWRITES:
		text = _replace_once(text, old, new, "knowledge note")
	if STERN_RUNTIME_WORDS.search(text.replace("harl_a40 scenarios", "")):
		raise RuntimeError("Sega Harley-Davidson knowledge note still describes the Stern ROMs' runs")
	return text


# --- Spatial report ------------------------------------------------------------------------------------
DERIVATION = (
	"Sega's model 67 is the production run Stern continued as its 1st edition (IPDB 4453 and 4455), one playfield and one "
	"wiring, so every placement comes over unchanged from the Stern record's placement seed "
	"tools/seeds/stern/harley-davidson-1999-spatial.json, built from the retained table, whose title calls it the Sega 1999 "
	"machine; tools/curate_harley_davidson_sega.py derives this record from tools/curate_harley_davidson.py."
)


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	report = base.build_spatial_report(definition)
	report["machine_id"] = MACHINE_ID
	report["derivation"] = DERIVATION
	return report


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = base.render_spatial_report(report).split("\n")
	if lines[0] != "# Harley-Davidson (Stern, 1999) spatial blockers":
		raise RuntimeError("Stern Harley-Davidson spatial report heading changed")
	return "\n".join(["# Harley-Davidson (Sega, 1999) spatial blockers", "", report["derivation"], *lines[1:]])


# --- Generation ----------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready Sega Harley-Davidson artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	write_text(KNOWLEDGE_PATH, render_knowledge())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Sega Harley-Davidson author-ready artifact: {AUTHOR_READY_PATH}")
	definition = build()
	report = build_spatial_report(definition)
	expected = (
		(PARTIAL_PATH, canonical_bytes(definition)),
		(SPATIAL_REPORT_PATH, canonical_bytes(report)),
		(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report).encode("utf-8")),
		(KNOWLEDGE_PATH, render_knowledge().encode("utf-8")),
	)
	for path, content in expected:
		if not path.is_file() or path.read_bytes() != content:
			raise RuntimeError(f"Sega Harley-Davidson deterministic artifact drift: {path}")
	print("Sega Harley-Davidson definition, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and its generated artifacts")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, knowledge note and spatial report")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
